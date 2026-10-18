#!/usr/bin/env python3
"""Check vendor model pages for model IDs the registry doesn't know yet.

Fetches each vendor's public models page, extracts anything that looks like a model ID,
and compares it with registry/models/. Prints a Markdown report. Exit code 2 when new IDs
are found (the scheduled GitHub workflow turns that into an issue for a human to review).

Standard library only. This is a tripwire, not a source of truth: a human still writes
or updates the model card from the official docs.
"""
import glob
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "plugins", "modelwise", "skills", "modelwise", "registry", "models")

SOURCES = {
    "anthropic": {
        "urls": ["https://platform.claude.com/docs/en/about-claude/models/overview.md"],
        "pattern": r"\bclaude-(?:fable|mythos|opus|sonnet|haiku)-\d+(?:-\d+)?\b",
    },
    "openai": {
        "urls": ["https://developers.openai.com/api/docs/models"],
        "pattern": r"\b(?:gpt-(?:\d+(?:\.\d+)?|image|realtime|live|transcribe|oss|audio)[a-z0-9.\-]*|o\d(?:-(?:pro|mini))?)\b",
    },
}
# Dated snapshots, aliases, image file names and doc-page slugs are not model IDs.
IGNORE = re.compile(r"-\d{4}-\d{2}-\d{2}$|-\d{8}$|-\d{4}$|-latest$|-preview|\.(png|webp|jpg|svg)$"
                    r"|-(and|family|series|deprecations?|completions|texture|updates|models?)\b")
UNTRACKED = os.path.join(os.path.dirname(REG), "watch-ignore.json")


def known_ids():
    ids = set()
    if os.path.exists(UNTRACKED):
        with open(UNTRACKED, encoding="utf-8") as f:
            ids |= set(json.load(f)["ids"])
    for path in glob.glob(os.path.join(REG, "*", "*.json")):
        with open(path, encoding="utf-8") as f:
            ids.add(json.load(f)["id"])
    return ids


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ai-knowhow-model-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    known = known_ids()
    report, found_new, failures = [], {}, []
    for vendor, cfg in SOURCES.items():
        seen = set()
        for url in cfg["urls"]:
            try:
                seen |= set(re.findall(cfg["pattern"], fetch(url)))
            except Exception as e:  # noqa: BLE001 - network problems are reported, not fatal
                failures.append("%s (%s)" % (url, e))
        new = sorted(i for i in seen if i not in known and not IGNORE.search(i))
        if new:
            found_new[vendor] = new
    if found_new:
        report.append("## Model IDs on vendor pages that are not in the registry\n")
        for vendor, ids in found_new.items():
            report.append("**%s**: %s\n" % (vendor, ", ".join("`%s`" % i for i in ids)))
        report.append("\nFor each real model: add `registry/models/<provider>/<id>.json` from the official docs, "
                      "run `python3 tools/validate.py --fix`, and open a PR. Ignore IDs that are only mentioned in passing.")
    else:
        report.append("No unknown model IDs found.")
    if failures:
        report.append("\nCould not fetch: " + "; ".join(failures))
    print("\n".join(report))
    sys.exit(2 if found_new else 0)


if __name__ == "__main__":
    main()
