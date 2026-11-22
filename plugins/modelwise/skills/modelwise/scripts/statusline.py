#!/usr/bin/env python3
"""Claude Code status line helper: show plan usage and save it for modelwise-run's limit check.

Claude Code pipes a JSON object to the status line command after each reply. On plans that report it,
that object has `rate_limits.five_hour` and `rate_limits.seven_day` (used_percentage, resets_at). This
script saves those numbers to ~/.claude/modelwise/usage.json (or $MODELWISE_USAGE_PATH), so the skill
can read them, and prints a short status line.

If you already had a status line, `tools/install.py statusline` saves its command to
~/.claude/modelwise/statusline-wrap.txt; this script runs it with the same input and prints its output first.
Standard library only. It never fails loudly: on any error it prints what it can and exits 0.
"""
import datetime
import json
import os
import subprocess
import sys

USAGE_PATH = os.environ.get("MODELWISE_USAGE_PATH",
                            os.path.join(os.path.expanduser("~"), ".claude", "modelwise", "usage.json"))
# Your previous status line command, saved by `tools/install.py statusline`, run first and kept on screen.
WRAP_PATH = os.path.join(os.path.expanduser("~"), ".claude", "modelwise", "statusline-wrap.txt")


def windows(data):
    """Pull the two plan windows out of the status line input, if present."""
    out = {}
    rl = (data or {}).get("rate_limits") or {}
    for key, name in (("five_hour", "5h"), ("seven_day", "week")):
        w = rl.get(key) or {}
        if w.get("used_percentage") is not None:
            out[name] = {"pct": float(w["used_percentage"]), "resets_at": w.get("resets_at")}
    return out


def save(found):
    os.makedirs(os.path.dirname(USAGE_PATH), exist_ok=True)
    found = dict(found, saved_at=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    tmp = USAGE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(found, f)
    os.replace(tmp, USAGE_PATH)


def segment(found):
    parts = []
    for name, label in (("5h", "5h"), ("week", "wk")):
        if name in found:
            parts.append("%s %d%%" % (label, round(found[name]["pct"])))
    return ("usage " + " · ".join(parts)) if parts else ""


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except ValueError:
        data = {}
    wrapped = ""
    cmd = os.environ.get("MODELWISE_STATUSLINE_WRAP")
    if not cmd:
        try:
            cmd = open(WRAP_PATH, encoding="utf-8").read().strip()
        except OSError:
            cmd = ""
    if cmd:
        try:
            wrapped = subprocess.run(cmd, shell=True, input=raw, capture_output=True, text=True,
                                     timeout=5).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            wrapped = ""
    found = windows(data)
    if found:
        try:
            save(found)
        except OSError:
            pass
    mine = segment(found)
    print(" | ".join(x for x in (wrapped, mine) if x))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # a status line must never break the terminal
        sys.exit(0)
