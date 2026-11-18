#!/usr/bin/env python3
"""Validate images in public Chinese editions against Git and source figure inventories.

Install scripts/requirements-images.txt, then run this file from any directory.
--allow-untracked is intended only for preparing a change before git add.
The source comparison is recorded in catalog/source-figure-coverage.json.
"""
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from markdown_it import MarkdownIt
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
REPO = BASE
PARSER = MarkdownIt("commonmark", {"html": True})


class ImageTags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.sources.append(dict(attrs).get("src", ""))


def image_sources(text):
    """Use Markdown parsing so code examples and nested links are handled correctly."""
    for token in PARSER.parse(text):
        for child in token.children or []:
            if child.type == "image":
                yield child.attrGet("src")
            elif child.type == "html_inline":
                tags = ImageTags()
                tags.feed(child.content)
                yield from tags.sources
        if token.type == "html_block":
            tags = ImageTags()
            tags.feed(token.content)
            yield from tags.sources


def interactive_placeholders(text):
    """Find unresolved figure placeholders in prose, excluding code examples."""
    placeholder = re.compile(r"^\s*\*交互图[：:][^\n]*可在原页面查看[^\n]*\*\s*$", re.MULTILINE)
    return [match.group().strip()
            for token in PARSER.parse(text) if token.type == "inline"
            for match in placeholder.finditer(token.content)]


def orphan_figure_captions(text):
    """Locate standalone figure captions without a neighboring rendered image."""
    lines = text.splitlines(keepends=True)
    blocks = []
    for token in PARSER.parse(text):
        if token.level != 0 or token.map is None or token.nesting < 0:
            continue
        fragment = "".join(lines[token.map[0]:token.map[1]])
        italic = False
        caption = ""
        if token.type == "paragraph_open":
            inline = next((item for item in PARSER.parse(fragment) if item.type == "inline"), None)
            children = inline.children if inline is not None else []
            if children and children[0].type == "em_open" and children[-1].type == "em_close":
                depth = 0
                italic = True
                for number, child in enumerate(children):
                    depth += (child.type == "em_open") - (child.type == "em_close")
                    if depth == 0 and number != len(children) - 1:
                        italic = False
                        break
                if italic:
                    caption = "".join(child.content if child.type in ("text", "code_inline") else
                                      " " if child.type in ("softbreak", "hardbreak") else ""
                                      for child in children).strip()
        blocks.append({"line": token.map[0] + 1, "image": bool(list(image_sources(fragment))),
                       "italic": italic, "caption": caption})
    errors = []
    for index, block in enumerate(blocks):
        if block["image"] or not re.match(r"^图(?:\s*[A-Za-z0-9]+)?\s*[：:]", block["caption"]):
            continue
        adjacent = False
        for direction in (-1, 1):
            neighbor = index + direction
            if not 0 <= neighbor < len(blocks):
                continue
            if blocks[neighbor]["image"]:
                adjacent = True
            elif blocks[neighbor]["italic"]:
                beyond = neighbor + direction
                if 0 <= beyond < len(blocks) and blocks[beyond]["image"]:
                    adjacent = True
        if not adjacent:
            errors.append({"line": block["line"], "caption": block["caption"]})
    return errors


def coverage_errors(coverage, media_directory, text, referenced):
    """Check declared figure coverage against this translation's rendered images."""
    if not isinstance(coverage, dict):
        return ["coverage must be an object"]
    errors = []
    groups = coverage.get("figure_groups")
    expected = coverage.get("expected_figure_groups")
    if not isinstance(groups, list):
        errors.append("coverage.figure_groups must be a list")
        groups = []
    if type(expected) is not int or expected < 0:
        errors.append("coverage.expected_figure_groups must be a nonnegative integer")
    elif len(groups) != expected:
        errors.append(f"expected {expected} figure groups, found {len(groups)}")
    seen = set()
    for number, group in enumerate(groups, 1):
        if not isinstance(group, dict):
            errors.append(f"figure group {number} must be an object")
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str) or not group_id.strip():
            errors.append(f"figure group {number} has no id")
        elif group_id in seen:
            errors.append(f"duplicate figure group id: {group_id}")
        else:
            seen.add(group_id)
        files = group.get("files")
        if not isinstance(files, list) or not files:
            errors.append(f"figure group {number} must have a nonempty files list")
            continue
        for filename in files:
            if not isinstance(filename, str) or not filename.strip():
                errors.append(f"figure group {number} has an invalid filename")
            elif (media_directory / filename).resolve() not in referenced:
                errors.append(f"figure group {number} image is not referenced by the translation: {filename}")
    return errors


def source_figure_order_errors(coverage, base_directory, image_order):
    """Match shared image resources to a nondecreasing sequence of source groups."""
    if not isinstance(coverage, dict) or not isinstance(coverage.get("figure_groups"), list):
        return []  # coverage_errors reports malformed declarations.
    groups = coverage["figure_groups"]
    explicit_indices = all(isinstance(group, dict) and type(group.get("source_index")) is int
                           and group["source_index"] >= 0 for group in groups)
    candidates = {}
    for position, group in enumerate(groups):
        if not isinstance(group, dict) or not isinstance(group.get("files"), list):
            continue
        rank = group["source_index"] if explicit_indices else position
        for filename in group["files"]:
            if isinstance(filename, str) and filename.strip():
                candidates.setdefault((base_directory / filename).resolve(), set()).add(rank)
    previous = None
    compressed = []
    for image in image_order:
        options = candidates.get(image, set())
        if not options:
            continue
        following = [rank for rank in options if previous is None or rank >= previous]
        if not following:
            return [f"source figure order goes backward after groups {compressed}: "
                    f"{image.name} matches earlier groups {sorted(options)}"]
        # The earliest valid match leaves all later matches possible, including shared files.
        rank = min(following)
        if not compressed or compressed[-1] != rank:
            compressed.append(rank)
        previous = rank
    return []


def requires_source_coverage(article):
    source = urlsplit(article.get("url", ""))
    return source.hostname == "claude.dev" and source.path.startswith("/blog/")


def check(allow_untracked=False):
    catalog = json.loads((BASE / "catalog/articles.json").read_text())
    index = {}
    for entry in subprocess.check_output(
        ["git", "ls-files", "--stage", "-z"], cwd=REPO
    ).decode().split("\0"):
        if entry:
            metadata, path = entry.split("\t", 1)
            index[path] = metadata.split()[1]
    tracked = set(index)
    errors, referenced, counts = [], set(), Counter()
    source_manifest = BASE / "catalog/source-figure-coverage.json"
    source_coverage = None
    if source_manifest.exists():
        try:
            declared = json.loads(source_manifest.read_text())
            if not isinstance(declared, dict) or not isinstance(declared.get("articles"), dict):
                raise ValueError("source-figure coverage manifest must contain an articles object")
            source_coverage = declared["articles"]
        except (OSError, ValueError, TypeError) as error:
            errors.append({"manifest": str(source_manifest.relative_to(BASE)), "source_coverage_error": str(error)})
    elif any(article.get("translation_path") for article in catalog):
        errors.append({"manifest": str(source_manifest.relative_to(BASE)),
                       "source_coverage_error": "required source-figure coverage manifest is missing"})
    for article in catalog:
        if not article.get("translation_path"):
            continue
        doc = BASE / article["translation_path"]
        counts["translations"] += 1
        text = doc.read_text()
        placeholders = interactive_placeholders(text)
        if placeholders:
            errors.append({"file": article["translation_path"], "interactive_placeholders": placeholders})
        if requires_source_coverage(article):
            for caption in orphan_figure_captions(text):
                errors.append({"file": article["translation_path"], "orphan_figure_caption": caption})
        sources = list(image_sources(text))
        article_referenced = set()
        article_image_order = []
        counts["image_references"] += len(sources)
        counts["translations_without_images"] += not sources
        for source in sources:
            parsed = urlsplit(source)
            if parsed.scheme or parsed.netloc:
                errors.append({"file": article["translation_path"], "remote_image": source})
                continue
            path = (doc.parent / unquote(parsed.path)).resolve()
            if not path.is_file():
                errors.append({"file": article["translation_path"], "missing_image": source})
                continue
            if not path.is_relative_to(BASE / "assets"):
                errors.append({"file": article["translation_path"], "outside_assets": source})
                continue
            if not allow_untracked and str(path.relative_to(REPO)) not in tracked:
                errors.append({"file": article["translation_path"], "untracked_image": source})
            referenced.add(path)
            article_referenced.add(path)
            article_image_order.append(path)
        article_id = article.get("article_id") or hashlib.sha256(article["url"].encode()).hexdigest()[:16]
        if source_coverage is not None:
            if article_id in source_coverage:
                counts["source_figure_articles"] += 1
                groups = source_coverage[article_id].get("figure_groups", []) if isinstance(source_coverage[article_id], dict) else []
                if isinstance(groups, list):
                    counts["source_figure_groups"] += len(groups)
                for error in coverage_errors(source_coverage[article_id], BASE, text, article_referenced):
                    errors.append({"file": article["translation_path"], "source_coverage_error": error})
                for error in source_figure_order_errors(source_coverage[article_id], BASE, article_image_order):
                    errors.append({"file": article["translation_path"], "source_figure_order_error": error})
            else:
                errors.append({"file": article["translation_path"],
                               "source_coverage_error": "missing source-figure coverage record"})
        media_path = BASE / "assets/articles" / article_id / "media.json"
        if media_path.exists():
            try:
                media = json.loads(media_path.read_text())
                if "coverage" in media:
                    for error in coverage_errors(media["coverage"], media_path.parent, text, article_referenced):
                        errors.append({"file": article["translation_path"], "coverage_error": error})
            except (OSError, ValueError, TypeError) as error:
                errors.append({"file": article["translation_path"], "coverage_error": str(error)})
    manifest_path = BASE / "catalog/reading-images.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for path in sorted(referenced):
        key = str(path.relative_to(BASE))
        try:
            data = path.read_bytes()
            if path.suffix == ".svg":
                root = ElementTree.parse(path).getroot()
                assert root.tag.endswith("svg"), "not an SVG document"
            else:
                with Image.open(path) as image:
                    image.verify()
            if manifest:
                assert key in manifest, "missing provenance record"
                assert hashlib.sha256(data).hexdigest() == manifest[key]["sha256"], "SHA-256 mismatch"
            if not allow_untracked:
                oid = index.get(str(path.relative_to(REPO)), "")
                hash_function = hashlib.sha256 if len(oid) == 64 else hashlib.sha1
                blob = f"blob {len(data)}\0".encode() + data
                assert hash_function(blob).hexdigest() == oid, "Git index differs from the validated image; stage the final file"
        except Exception as error:
            errors.append({"image": key, "error": str(error)})
    if manifest:
        for key in manifest:
            if (BASE / key).resolve() not in referenced:
                errors.append({"image": key, "error": "manifest image is not referenced"})
    counts["unique_image_files"] = len(referenced)
    counts["image_bytes"] = sum(path.stat().st_size for path in referenced)
    return {"counts": dict(counts), "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-untracked", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check(args.allow_untracked)
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")
    raise SystemExit(bool(result["errors"]))
