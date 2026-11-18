#!/usr/bin/env python3
"""Check relative Markdown and HTML links in public reading pages."""

from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from build_index import ROOT
from check_images import PARSER


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        field = {"a": "href", "img": "src"}.get(tag)
        value = dict(attrs).get(field)
        if value is not None:
            self.targets.append(value)


def markdown_links(text):
    for token in PARSER.parse(text):
        for item in [token, *(token.children or [])]:
            field = {"link_open": "href", "image": "src"}.get(item.type)
            if field:
                yield item.attrGet(field)
            elif item.type in {"html_inline", "html_block"}:
                parser = Links()
                parser.feed(item.content)
                yield from parser.targets


def check_links():
    roots = ("content", "articles", "sources", "docs", "history")
    files = sorted({*ROOT.glob("*.md"), *(path for directory in roots for path in (ROOT / directory).rglob("*.md"))})
    errors = []
    for file in files:
        for url in markdown_links(file.read_text(encoding="utf-8")):
            if not url:
                continue
            parts = urlsplit(url)
            if parts.scheme and parts.scheme not in {"http", "https", "mailto"}:
                errors.append(f"{file.relative_to(ROOT)}: unsupported link scheme in {url}")
                continue
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = (file.parent / unquote(parts.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"{file.relative_to(ROOT)}: missing local target {url}")
    return files, sorted(set(errors))


if __name__ == "__main__":
    files, errors = check_links()
    print(f"Checked local links in {len(files)} Markdown files.")
    for error in errors:
        print(error)
    raise SystemExit(bool(errors))
