#!/usr/bin/env python3
"""Validate core SearXNG Railway template and licensing assumptions."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
REQUIRED = [
    "README.md", "README.en.md", "LICENSE", "Dockerfile", "settings.yml",
    "CONTRIBUTING.md", "SECURITY.md", ".gitignore", ".dockerignore",
    "docs/SOURCES.md", "docs/brand.svg", "docs/hero.id.svg",
    "docs/hero.en.svg", "docs/architecture.svg",
    "scripts/check_docs.py", "scripts/validate_repo.py",
    ".github/workflows/validate.yml",
]
for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        ERRORS.append(f"Missing required file: {relative}")


def read(relative: str) -> str:
    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


dockerfile = read("Dockerfile")
if not re.search(r"(?m)^FROM\s+searxng/searxng:[A-Za-z0-9._-]+\s*$", dockerfile):
    ERRORS.append("Dockerfile must use the official searxng/searxng image")
if "COPY settings.yml /etc/searxng/settings.yml" not in dockerfile:
    ERRORS.append("Dockerfile must copy settings.yml to the upstream configuration path")

settings = read("settings.yml")
for token, description in (
    ("use_default_settings: true", "upstream default settings"),
    ("instance_name:", "instance name"),
    ("formats:", "search response formats"),
    ("- json", "JSON Search API"),
    ("secret_key:", "secret key setting"),
    ("limiter: false", "internal-only limiter setting"),
    ("public_instance: false", "non-public instance setting"),
    ("debug: false", "debug mode disabled"),
):
    if token not in settings:
        ERRORS.append(f"settings.yml is missing {description}: {token}")

license_text = read("LICENSE")
for token in (
    "MIT License", "Copyright (c) 2026 DURIAN-ORGANISASI",
    "ANY CLAIM, DAMAGES OR OTHER LIABILITY", "docs/SOURCES.md",
):
    if token not in license_text:
        ERRORS.append(f"LICENSE is missing required scope or warranty text: {token}")

for relative in ("README.md", "README.en.md"):
    document = read(relative).lower()
    if "<h1>searxng railway</h1>" not in document:
        ERRORS.append(f"{relative} must use an explicit title element in its HTML header")
    for token in ("searxng_secret", "agpl-3.0", "mit license", "railway.internal", "docs/sources.md", "security.md"):
        if token not in document:
            ERRORS.append(f"{relative} must document {token}")
    if "img.shields.io/github/license/" in document:
        ERRORS.append(f"{relative} must not present all upstream software as MIT via a repository license badge")
    if "img.shields.io/github/actions/workflow/status/" not in document:
        ERRORS.append(f"{relative} must include the validation workflow badge")

for relative in ("docs/brand.svg", "docs/hero.id.svg", "docs/hero.en.svg", "docs/architecture.svg"):
    svg = read(relative)
    if "<svg" not in svg or "</svg>" not in svg or 'xmlns="http://www.w3.org/2000/svg"' not in svg:
        ERRORS.append(f"{relative} is not a complete SVG document")

if ".env" not in read(".gitignore"):
    ERRORS.append(".gitignore must exclude environment files")
if "!settings.yml" not in read(".dockerignore"):
    ERRORS.append(".dockerignore must include settings.yml in the Docker build context")

if ERRORS:
    print("Repository validation FAILED:")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("Repository validation OK: files, API configuration, license scope, security notes, and assets.")
print("Static validation only; this does not test a live Railway deployment.")
