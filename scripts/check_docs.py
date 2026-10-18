#!/usr/bin/env python3
"""Check local Markdown links, heading anchors, and SVG document structure."""
from __future__ import annotations

import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"(?ms)^([`]{3,}|~{3,}).*?^\1\s*$")
HEADING = re.compile(r"(?m)^(#{1,6})\s+(.+?)\s*#*\s*$")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"a", "img", "image", "source"}:
            return
        for name, value in attrs:
            if name in {"href", "src", "xlink:href"} and value:
                self.links.append(value)


def strip_fences(text: str) -> str:
    return FENCE.sub("", text)


def slug_heading(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[`*_~]", "", text).lower()
    chars = []
    for char in text:
        category = unicodedata.category(char)
        if char.isspace():
            chars.append("-")
        elif char == "-" or category[0] not in {"P", "S"}:
            chars.append(char)
    return re.sub(r"-+", "-", "".join(chars)).strip("-")


def heading_ids(text: str) -> set[str]:
    ids: set[str] = set()
    counts: dict[str, int] = {}
    for _, title in HEADING.findall(strip_fences(text)):
        base = slug_heading(title)
        index = counts.get(base, 0)
        ids.add(base if index == 0 else f"{base}-{index}")
        counts[base] = index + 1
    return ids


def links_in(markdown: str) -> list[str]:
    cleaned = strip_fences(markdown)
    links = [match.group(1).strip().split()[0].strip("<>") for match in MARKDOWN_LINK.finditer(cleaned)]
    parser = LinkParser()
    parser.feed(cleaned)
    links.extend(parser.links)
    return links


markdown_files = sorted(
    path for path in ROOT.rglob("*.md")
    if ".git" not in path.parts and "node_modules" not in path.parts
)
headings = {path.resolve(): heading_ids(path.read_text(encoding="utf-8")) for path in markdown_files}

for source in markdown_files:
    source_text = source.read_text(encoding="utf-8")
    for raw_url in links_in(source_text):
        url = raw_url.strip()
        if not url or url.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")) or url.startswith("//"):
            continue
        parts = urlsplit(url)
        path_part = unquote(parts.path)
        fragment = unquote(parts.fragment)
        target = (source.parent / path_part).resolve() if path_part else source.resolve()
        if path_part and not target.exists():
            ERRORS.append(f"{source.relative_to(ROOT)}: broken local link '{url}'")
            continue
        if fragment and target.suffix.lower() in {".md", ".markdown"} and target.exists():
            known = headings.get(target, heading_ids(target.read_text(encoding="utf-8")))
            if fragment.lower() not in known:
                ERRORS.append(f"{source.relative_to(ROOT)}: unknown heading anchor '{url}'")

for svg_path in ROOT.rglob("*.svg"):
    if ".git" in svg_path.parts or "node_modules" in svg_path.parts:
        continue
    svg = svg_path.read_text(encoding="utf-8")
    if "<svg" not in svg or "</svg>" not in svg or 'xmlns="http://www.w3.org/2000/svg"' not in svg:
        ERRORS.append(f"{svg_path.relative_to(ROOT)}: incomplete SVG document")

if ERRORS:
    print("Documentation checks FAILED:")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print(f"Documentation checks OK: {len(markdown_files)} Markdown files and local links/anchors/SVGs.")
