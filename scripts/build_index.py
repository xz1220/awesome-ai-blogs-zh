#!/usr/bin/env python3
"""Build and validate the public reading indexes from the catalog."""

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
TOPICS = {
    "research": ("模型与研究", "模型架构、训练、推理方法与实验发现。"),
    "engineering": ("工程实践", "Agent、软件开发、工具、工作流与生产经验。"),
    "infrastructure": ("基础设施", "推理服务、算力、部署、性能与成本。"),
    "evaluation": ("评测与安全", "评估方法、对齐、安全研究与可靠性。"),
    "products": ("产品与应用", "产品设计、重要发布和有实质经验的应用案例。"),
    "perspectives": ("独立观点", "作者对技术、产品或行业的第一手观察。"),
    "archive": ("历史索引", "早期资料、持续更新页面及其他来源。"),
}
SOURCE_GROUPS = {
    "labs": "研究机构与模型团队",
    "builders": "工程团队与产品博客",
    "community": "开源项目与社区",
    "authors": "独立作者",
}
BEGIN = "<!-- catalog:start -->"
END = "<!-- catalog:end -->"


def load(name):
    return json.loads((ROOT / "catalog" / f"{name}.json").read_text(encoding="utf-8"))


def http_url(value):
    parts = urlsplit(value)
    if (
        parts.scheme not in {"http", "https"}
        or not parts.hostname
        or parts.username is not None
        or parts.password is not None
        or re.search(r"[\s<>]", value)
    ):
        raise ValueError(f"invalid public URL: {value!r}")
    return parts


def url_key(value):
    parts = http_url(value)
    return urlunsplit(("https", parts.netloc.lower(), parts.path.rstrip("/"), parts.query, parts.fragment))


def check_catalog(articles, sources, picks):
    claimed_urls = {}
    article_ids = set()
    paths = set()
    coverage = load("source-figure-coverage")["articles"]
    for article in articles:
        article_id = article["article_id"]
        if not re.fullmatch(r"[a-f0-9]{16}", article_id) or article_id in article_ids:
            raise ValueError(f"invalid or duplicate article id: {article_id}")
        article_ids.add(article_id)
        for url in [article["url"], *article.get("aliases", [])]:
            key = url_key(url)
            existing = claimed_urls.setdefault(key, article_id)
            if existing != article_id:
                raise ValueError(f"URL claimed by {existing} and {article_id}: {url}")
        if article["topic"] not in TOPICS or not article["title"].strip() or not article["company"].strip():
            raise ValueError(f"invalid article metadata: {article_id}")
        if article.get("date"):
            published = article["date"]
            if re.fullmatch(r"\d{4}-\d{2}", published):
                date.fromisoformat(published + "-01")
            elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", published):
                date.fromisoformat(published)
            else:
                raise ValueError(f"invalid date: {article_id}: {published}")
        if article.get("chinese_url"):
            http_url(article["chinese_url"])
        path = article.get("translation_path")
        if path:
            full_path = (ROOT / path).resolve()
            rights = article.get("rights", {})
            if rights.get("basis") not in {"permission", "license"} or not rights.get("reference"):
                raise ValueError(f"missing publication basis: {article_id}")
            if (
                path in paths
                or not full_path.is_relative_to(ROOT / "content")
                or not path.endswith(".中文.md")
                or not full_path.is_file()
            ):
                raise ValueError(f"missing or duplicate Chinese edition: {path}")
            if article.get("edition") not in {"translation", "official-zh"} or article.get("qa") != "passed":
                raise ValueError(f"unreviewed Chinese edition: {article_id}")
            if coverage.get(article_id, {}).get("complete") is not True or coverage[article_id].get("translation_path") != path:
                raise ValueError(f"missing complete source figure inventory: {article_id}")
            paths.add(path)
    actual_files = {path.relative_to(ROOT).as_posix() for path in (ROOT / "content").rglob("*.md")}
    if paths != actual_files:
        raise ValueError(f"Chinese edition files differ from catalog: {sorted(paths ^ actual_files)}")
    known_ids = set()
    known_source_urls = set()
    for source in sources:
        source_url = url_key(source["url"])
        if source["id"] in known_ids or source_url in known_source_urls:
            raise ValueError(f"duplicate source: {source['id']}")
        if source["group"] not in SOURCE_GROUPS or not source["description"].strip():
            raise ValueError(f"invalid source metadata: {source['id']}")
        known_ids.add(source["id"])
        known_source_urls.add(source_url)
        for feed in source.get("feeds", []):
            http_url(feed)
    if len(picks["articles"]) != len(set(picks["articles"])) or not set(picks["articles"]) <= article_ids:
        raise ValueError("featured articles must be unique catalog article IDs")
    if len(picks["sources"]) != len(set(picks["sources"])) or not set(picks["sources"]) <= known_ids:
        raise ValueError("featured sources must be unique catalog source IDs")


def inline(text):
    return re.sub(r"([\\`*\[\]<>])", r"\\\1", " ".join(text.split()))


def external(text, url):
    return f"[{inline(text)}](<{url}>)"


def article_line(article, prefix):
    title = article.get("title_zh") or article["title"]
    source = article.get("author") if article["topic"] == "perspectives" else None
    info = [inline(source or article["company"])]
    if article.get("date"):
        info.append(article["date"])
    if article.get("translation_path"):
        label = "官方中文版" if article["edition"] == "official-zh" else "中文全文"
        info.append(f"[{label}]({prefix}{quote(article['translation_path'])})")
    elif article.get("chinese_url"):
        info.append(external("官方中文版", article["chinese_url"]))
    elif article.get("original_language") == "zh":
        info.append("中文原文")
    description = f" {inline(article['description'])}" if article.get("description") else ""
    return f"- {external(title, article['url'])} — {' · '.join(info)}。{description}"


def source_lines(sources, selected=None):
    result = []
    for group, title in SOURCE_GROUPS.items():
        entries = [source for source in sources if source["group"] == group
                   and (selected is None or source["id"] in selected)]
        if not entries:
            continue
        result.extend([f"### {title}", ""])
        for source in entries:
            feeds = " · ".join(external("订阅", feed) for feed in source.get("feeds", []))
            suffix = f" {feeds}" if feeds else ""
            result.append(f"- {external(source['name'], source['url'])} — {inline(source['description'])}{suffix}")
        result.append("")
    return result


def topic_lines(counts, prefix):
    return [f"- [{name}]({prefix}{topic}.md)（{counts[topic]} 篇）— {description}"
            for topic, (name, description) in TOPICS.items()]


def render(articles, sources, picks):
    ordered = sorted(articles, key=lambda article: (article.get("date") or "", article["article_id"]), reverse=True)
    counts = Counter(article["topic"] for article in articles)
    by_id = {article["article_id"]: article for article in articles}
    editions = [article for article in ordered if article.get("translation_path")]
    main = ["## 按主题阅读", "", f"已收录 {len(articles)} 篇（含历史索引）、{len(sources)} 个推荐博客或栏目，"
            f"其中 {len(editions)} 篇可在仓库阅读中文全文。", ""]
    main += topic_lines(counts, "articles/")
    main += ["", "## 精选文章", ""]
    main += [article_line(by_id[article_id], "") for article_id in picks["articles"]]
    main += ["", "## 近期文章", ""]
    recent = [article for article in ordered if article["topic"] != "archive" and article.get("date")]
    main += [article_line(article, "") for article in recent[:8]]
    main += ["", "## 推荐博客", ""]
    main += source_lines(sources, set(picks["sources"]))
    main += ["[查看所有来源及订阅入口](sources/README.md)"]
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one catalog region")
    before, tail = readme.split(BEGIN, 1)
    _, after = tail.split(END, 1)
    yield readme_path, before + BEGIN + "\n\n" + "\n".join(main) + "\n\n" + END + after
    terms = "主链接进入原文；条目有中文全文时，另附仓库内阅读入口。"
    yield ROOT / "articles/README.md", "\n".join([
        "# 文章目录", "", "[返回首页](../README.md)", "", terms, "", *topic_lines(counts, ""), "",
    ])
    for topic, (name, description) in TOPICS.items():
        lines = [f"# {name}", "", "[文章目录](README.md) · [首页](../README.md)", "",
                 f"{description} 共 {counts[topic]} 篇，按已知的首发日期倒序排列。", ""]
        lines += [article_line(article, "../") for article in ordered if article["topic"] == topic]
        yield ROOT / f"articles/{topic}.md", "\n".join(lines) + "\n"
    yield ROOT / "sources/README.md", "\n".join([
        "# 博客与订阅源", "", "[返回首页](../README.md)", "",
        "每个条目链接到作者或机构的官方页面。有可用的官方订阅源时同时列出；收录以发布者的原页为准。",
        "", "## 来源", "", *source_lines(sources),
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    articles, sources, picks = (load(name) for name in ("articles", "sources", "featured"))
    check_catalog(articles, sources, picks)
    mismatches = []
    for path, text in render(articles, sources, picks):
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                mismatches.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    if mismatches:
        parser.exit(1, "Outdated indexes; run scripts/build_index.py: " + ", ".join(mismatches) + "\n")
    print(f"Catalog OK: {len(articles)} articles, {len(sources)} sources, "
          f"{sum(bool(article.get('translation_path')) for article in articles)} Chinese full texts")


if __name__ == "__main__":
    main()
