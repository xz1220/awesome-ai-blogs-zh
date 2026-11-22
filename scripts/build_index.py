#!/usr/bin/env python3
"""Build and validate the public reading indexes from the catalog."""

import argparse
import json
import re
import subprocess
from datetime import date, datetime, timedelta
from itertools import groupby
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
SHANGHAI = ZoneInfo("Asia/Shanghai")
RECENT_PATH = ROOT / "articles/recent.md"
RECENT_DATE = re.compile(r"^<!-- recent-as-of: (\d{4}-\d{2}-\d{2}) -->$", re.MULTILINE)
TOPICS = {
    "research": "模型与研究",
    "engineering": "工程实践",
    "infrastructure": "基础设施",
    "evaluation": "评测与安全",
    "products": "产品与应用",
    "perspectives": "独立观点",
    "archive": "历史索引",
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


def check_catalog(articles, sources):
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
        if "added_on" in article:
            added_on = article["added_on"]
            if not isinstance(added_on, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", added_on):
                raise ValueError(f"invalid collection date: {article_id}: {added_on}")
            date.fromisoformat(added_on)
        if article.get("chinese_url"):
            http_url(article["chinese_url"])
        if "chinese_archived" in article and not isinstance(article["chinese_archived"], bool):
            raise ValueError(f"invalid Chinese archive flag: {article_id}")
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


def inline(text):
    return re.sub(r"([\\`*\[\]<>])", r"\\\1", " ".join(text.split()))


def external(text, url):
    return f"[{inline(text)}](<{url}>)"


def article_source(article):
    company = article["company"]
    author = article.get("author") if company == "独立作者" or article["topic"] == "perspectives" else None
    if isinstance(author, list):
        author = "、".join(author)
    return " ".join((author or company).split())


def article_line(article, *, root_prefix="", show_context=False):
    title = article.get("title_zh") or article["title"]
    info = [inline(article_source(article)), TOPICS[article["topic"]]] if show_context else []
    if article.get("date"):
        info.append(("首发 " if show_context else "") + article["date"])
    original = article["url"]
    if path := article.get("translation_path"):
        title_link = f"[{inline(title)}]({root_prefix}{quote(path)})"
        info.append("官方中文版" if article["edition"] == "official-zh" else "中文译文")
        info.append(external("原文", original))
    elif chinese_url := article.get("chinese_url"):
        title_link = external(title, chinese_url)
        info.append("官方中文版")
        if chinese_url != original:
            info.append(external("原文", original))
    else:
        title_link = external(title, original)
        if article.get("original_language") == "zh":
            info.append("中文原文")
        elif article.get("chinese_archived"):
            info.append("已有中文全文（本库未公开）")
        else:
            info.append("仅原文")
    return "- " + " · ".join([title_link, *info])


def source_lines(sources):
    result = []
    for group, title in SOURCE_GROUPS.items():
        entries = [source for source in sources if source["group"] == group]
        if not entries:
            continue
        result.extend([f"### {title}", ""])
        for source in entries:
            feeds = " · ".join(external("订阅", feed) for feed in source.get("feeds", []))
            suffix = f" {feeds}" if feeds else ""
            result.append(f"- {external(source['name'], source['url'])} — {inline(source['description'])}{suffix}")
        result.append("")
    return result


def render_recent(articles, as_of):
    start = (as_of - timedelta(days=6)).isoformat()
    end = as_of.isoformat()
    recent = sorted(
        (a for a in articles if start <= a.get("added_on", "") <= end),
        key=lambda a: (a["added_on"], a.get("date") or "", a["article_id"]),
        reverse=True,
    )
    lines = [
        "# 近 7 天新增", "",
        f"<!-- recent-as-of: {end} -->", "",
        "[查看完整目录](../README.md#按主题阅读)", "",
        f"**{start} 至 {end}（北京时间）** · **新增 {len(recent)} 篇**", "",
        "按首次收录日期倒序，含近期补录的旧文，不含建库时批量导入的存量文章。目录每日滚动更新。",
    ]
    for added_on, group in groupby(recent, key=lambda a: a["added_on"]):
        lines += ["", f"## {added_on}", ""]
        lines.extend(article_line(a, root_prefix="../", show_context=True) for a in group)
    if not recent:
        lines += ["", "近 7 天没有新收录的文章。"]
    return "\n".join(lines) + "\n"


def record_additions(articles, as_of):
    baseline = json.loads(subprocess.check_output(
        ["git", "show", "HEAD:catalog/articles.json"], cwd=ROOT, encoding="utf-8",
    ))
    existing_ids = {a["article_id"] for a in baseline}
    changed = False
    for article in articles:
        if article["article_id"] not in existing_ids and "added_on" not in article:
            article["added_on"] = as_of.isoformat()
            changed = True
    return changed


def render(articles, sources, as_of):
    ordered = sorted(articles, key=lambda article: (article.get("date") or "", article["article_id"]), reverse=True)
    by_topic = {topic: {} for topic in TOPICS}
    for article in ordered:
        by_topic[article["topic"]].setdefault(article_source(article), []).append(article)
    main = [
        "## 按主题阅读", "",
        f"已收录 {len(articles)} 篇。每个主题按来源分组，同一来源的文章按首发日期倒序排列，日期不详的放在最后。",
        "",
        "点击标题直接阅读，有公开中文版时优先打开中文。「已有中文全文（本库未公开）」表示已核对存档译文，标题仍指向原文；「仅原文」表示当前只收录了原文。",
        "", "**[近 7 天新增](articles/recent.md)**",
        "", " · ".join(f"[{name}](#{name})" for name in TOPICS.values()),
    ]
    for topic, name in TOPICS.items():
        main += ["", f"### {name}"]
        for source, entries in sorted(by_topic[topic].items(), key=lambda group: group[0].casefold()):
            main += ["", f"#### {inline(source)}", "", *map(article_line, entries)]
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one catalog region")
    before, tail = readme.split(BEGIN, 1)
    _, after = tail.split(END, 1)
    yield readme_path, before + BEGIN + "\n\n" + "\n".join(main) + "\n\n" + END + after
    # Keep the old catalog URLs as pointers to the single list on the homepage.
    yield ROOT / "articles/README.md", "\n".join([
        "# 文章目录", "", "[在首页浏览全部文章](../README.md#按主题阅读) · [近 7 天新增](recent.md)", "",
    ])
    yield RECENT_PATH, render_recent(articles, as_of)
    for topic, name in TOPICS.items():
        yield ROOT / f"articles/{topic}.md", f"# {name}\n\n[在首页浏览本主题的文章](../README.md#{name})\n"
    yield ROOT / "sources/README.md", "\n".join([
        "# 博客与订阅源", "", "[返回首页](../README.md)", "",
        "每个条目链接到作者或机构的官方页面。有可用的官方订阅源时同时列出；收录以发布者的原页为准。",
        "", "## 来源", "", *source_lines(sources),
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--record-added", action="store_true", help="date newly added catalog IDs before generating")
    args = parser.parse_args()
    if args.check:
        # Verify the checked-in snapshot even when CI runs later in another time zone.
        recorded = RECENT_DATE.findall(RECENT_PATH.read_text(encoding="utf-8")) if RECENT_PATH.is_file() else []
        if len(recorded) != 1:
            parser.exit(1, "Missing index date; run scripts/build_index.py\n")
        as_of = date.fromisoformat(recorded[0])
    else:
        as_of = datetime.now(SHANGHAI).date()
    articles, sources = (load(name) for name in ("articles", "sources"))
    recorded_additions = args.record_added and record_additions(articles, as_of)
    check_catalog(articles, sources)
    if recorded_additions:
        (ROOT / "catalog/articles.json").write_text(
            json.dumps(articles, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
    mismatches = []
    for path, text in render(articles, sources, as_of):
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
