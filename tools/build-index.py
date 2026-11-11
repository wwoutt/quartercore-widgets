#!/usr/bin/env python3
# Builds and checks index.json for the Quartercore widget catalog
# Author: wwoutt (2026-11-11), written by Claude (Anthropic)
# License: GPL-3.0 or later
#
# Copied from the catalog wwoutt/openlinkhub-widgets (same author); widgets
# with an action script now count as running code.
#
# Usage: tools/build-index.py          (writes index.json)
#        tools/build-index.py --check  (fails when a widget is invalid or index.json is outdated)
#
# Quartercore verifies every downloaded file against the SHA-256 in
# index.json, so the content of a widget is pinned by the index.

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDGETS = os.path.join(ROOT, "widgets")
INDEX = os.path.join(ROOT, "index.json")

# Keep these rules in sync with Quartercore (quartercore/customwidgets/store.py)
WIDGET_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
FILE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
EXTENSIONS = {".json", ".html", ".css", ".js", ".py", ".sh", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".md", ".txt"}
CODE_EXTENSIONS = {".py", ".sh"}
MAX_FILES = 30
MAX_FILE_SIZE = 512 * 1024
MAX_TOTAL_SIZE = 2 * 1024 * 1024
LICENSES = {
    "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later", "LGPL-2.1-or-later", "LGPL-3.0-only",
    "LGPL-3.0-or-later", "AGPL-3.0-only", "AGPL-3.0-or-later", "MIT", "BSD-2-Clause", "BSD-3-Clause",
    "Apache-2.0", "ISC", "MPL-2.0", "Unlicense", "CC0-1.0",
}
REQUIRED = ("name", "description", "author", "license", "version")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_widget(widget_id):
    path = os.path.join(WIDGETS, widget_id)
    errors = []
    if not WIDGET_ID.match(widget_id):
        errors.append("folder name must match %s" % WIDGET_ID.pattern)

    names = sorted(os.listdir(path))
    files = {}
    total = 0
    for name in names:
        full = os.path.join(path, name)
        ext = os.path.splitext(name)[1].lower()
        if os.path.isdir(full) or os.path.islink(full):
            errors.append("%s: subfolders and links are not allowed" % name)
            continue
        if not FILE_NAME.match(name) or (ext not in EXTENSIONS and name != "LICENSE"):
            errors.append("%s: file name or type not allowed" % name)
            continue
        size = os.path.getsize(full)
        if size > MAX_FILE_SIZE:
            errors.append("%s: larger than %d KB" % (name, MAX_FILE_SIZE // 1024))
        total += size
        files[name] = sha256(full)
    if len(files) > MAX_FILES:
        errors.append("more than %d files" % MAX_FILES)
    if total > MAX_TOTAL_SIZE:
        errors.append("larger than %d MB in total" % (MAX_TOTAL_SIZE // 1024 // 1024))
    for required in ("widget.json", "widget.html"):
        if required not in files:
            errors.append("%s is missing" % required)

    manifest = {}
    if "widget.json" in files:
        try:
            with open(os.path.join(path, "widget.json"), encoding="utf-8") as f:
                manifest = json.load(f)
        except ValueError as e:
            errors.append("widget.json: %s" % e)
    for field in REQUIRED:
        if not isinstance(manifest.get(field), str) or not manifest.get(field).strip():
            errors.append("widget.json: '%s' is required" % field)
    if manifest.get("license") and manifest["license"] not in LICENSES:
        errors.append("widget.json: license must be one of %s" % ", ".join(sorted(LICENSES)))

    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    source_type = source.get("type") or "none"
    if source_type not in ("none", "url", "script"):
        errors.append("widget.json: unknown source type '%s'" % source_type)
    runs_code = source_type == "script" or "action" in manifest or any(os.path.splitext(n)[1].lower() in CODE_EXTENSIONS for n in files)

    entry = {
        "id": widget_id,
        "name": manifest.get("name", widget_id),
        "description": manifest.get("description", ""),
        "author": manifest.get("author", ""),
        "license": manifest.get("license", ""),
        "version": manifest.get("version", ""),
        "source": source_type,
        "runsCode": runs_code,
        "path": "widgets/%s" % widget_id,
        "files": files,
    }
    return entry, errors


def build():
    widgets, failed = [], False
    for widget_id in sorted(os.listdir(WIDGETS)):
        if not os.path.isdir(os.path.join(WIDGETS, widget_id)):
            continue
        entry, errors = check_widget(widget_id)
        for error in errors:
            print("%s: %s" % (widget_id, error), file=sys.stderr)
        failed = failed or bool(errors)
        widgets.append(entry)
    return {"version": 1, "widgets": widgets}, failed


def main():
    index, failed = build()
    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        try:
            with open(INDEX, encoding="utf-8") as f:
                current = f.read()
        except OSError:
            current = ""
        if current != text:
            print("index.json is outdated, run tools/build-index.py", file=sys.stderr)
            failed = True
        sys.exit(1 if failed else 0)
    if failed:
        sys.exit(1)
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(text)
    print("index.json: %d widgets" % len(index["widgets"]))


if __name__ == "__main__":
    main()
