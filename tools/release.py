#!/usr/bin/env python3
"""Pre-publish checks and release prep (standard library only).

  python3 tools/release.py --owner <github-user-or-org>            # replace placeholders, then check
  python3 tools/release.py --version 0.2.0                          # bump every plugin manifest, then check
  python3 tools/release.py --check                                  # checks only
  python3 tools/release.py --check --build                          # checks + all upload ZIPs in dist/

Checks mirror the Anthropic directory pre-submission checklist and the OpenAI plugin guidelines:
README (40+ words) and LICENSE per plugin, no .DS_Store, no non-image file over 256 KiB, repo under
50 MiB, no secrets, no leftover placeholders, matching versions across manifests, valid names,
everything a plugin runs is inside its folder, plus validate.py and the router tests.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER = "YOUR-GITHUB-USERNAME"
SKIP_DIRS = {".git", "dist", "bench", "__pycache__"}  # bench/ keeps historical copies as-is
TEXT_EXT = {".md", ".json", ".yml", ".yaml", ".py", ".txt", ".toml"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".ico", ".woff", ".woff2", ".ttf"}
SECRET = re.compile(r"(sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
RESERVED = ("claude", "anthropic", "official", "plugin", "mcp", "test")
PLUGINS = sorted(os.path.basename(os.path.dirname(os.path.dirname(p)))
                 for p in glob.glob(os.path.join(ROOT, "plugins", "*", ".claude-plugin", "plugin.json")))

problems, notes = [], []


SELF = os.path.abspath(__file__)


def walk_files():
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = os.path.join(folder, f)
            if os.path.abspath(p) != SELF:  # this script names the placeholder on purpose
                yield p


def rel(p):
    return os.path.relpath(p, ROOT)


def set_owner(owner):
    if not re.fullmatch(r"[A-Za-z0-9-]{1,39}", owner):
        sys.exit("Invalid GitHub owner: %s" % owner)
    n = 0
    for p in walk_files():
        if os.path.splitext(p)[1] in TEXT_EXT:
            s = open(p, encoding="utf-8").read()
            if PLACEHOLDER in s:
                open(p, "w", encoding="utf-8").write(s.replace(PLACEHOLDER, owner))
                n += 1
    print("Replaced %s with %s in %d files." % (PLACEHOLDER, owner, n))


def set_version(version):
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit("Version must look like 1.2.3")
    for name in PLUGINS:
        for sub in (".claude-plugin", ".codex-plugin"):
            p = os.path.join(ROOT, "plugins", name, sub, "plugin.json")
            if os.path.exists(p):
                c = json.load(open(p, encoding="utf-8"))
                c["version"] = version
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(c, f, indent=2)
                    f.write("\n")
    print("Set version %s in all plugin manifests." % version)


def check():
    total = 0
    for p in walk_files():
        size = os.path.getsize(p)
        total += size
        ext = os.path.splitext(p)[1].lower()
        if os.path.basename(p) == ".DS_Store":
            problems.append("%s: remove .DS_Store" % rel(p))
        if size > 256 * 1024 and ext not in IMAGE_EXT:
            problems.append("%s: %d KiB non-image file (directory review holds files over 256 KiB)" % (rel(p), size // 1024))
        if ext in TEXT_EXT:
            s = open(p, encoding="utf-8", errors="replace").read()
            if SECRET.search(s):
                problems.append("%s: looks like it contains a secret" % rel(p))
            if PLACEHOLDER in s:
                problems.append("%s: still contains %s (run --owner)" % (rel(p), PLACEHOLDER))
    if total > 50 * 1024 * 1024:
        problems.append("repo is over 50 MiB")

    marketplace = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    for name in PLUGINS:
        d = os.path.join(ROOT, "plugins", name)
        readme = os.path.join(d, "README.md")
        if not os.path.exists(readme):
            problems.append("plugins/%s: missing README.md" % name)
        else:
            prose = re.sub(r"```.*?```", "", open(readme, encoding="utf-8").read(), flags=re.S)
            if len(prose.split()) < 40:
                problems.append("plugins/%s/README.md: needs at least 40 words outside code blocks" % name)
        cm = json.load(open(os.path.join(d, ".claude-plugin", "plugin.json"), encoding="utf-8"))
        if not (os.path.exists(os.path.join(d, "LICENSE")) or cm.get("license")):
            problems.append("plugins/%s: needs LICENSE or a license field" % name)
        if name in RESERVED or name.startswith(("claude-", "anthropic-", "cc-plugin-")):
            problems.append("plugins/%s: reserved plugin name" % name)
        versions = {"claude": cm.get("version")}
        ox = os.path.join(d, ".codex-plugin", "plugin.json")
        if os.path.exists(ox):
            om = json.load(open(ox, encoding="utf-8"))
            versions["openai"] = om.get("version")
            ui = om.get("extensions", {}).get("com.openai", {}).get("interface", {})
            for field in ("displayName", "shortDescription", "longDescription", "developerName", "category", "logo", "composerIcon"):
                if not ui.get(field):
                    problems.append("plugins/%s/.codex-plugin: missing interface.%s" % (name, field))
            if len(ui.get("shortDescription", "")) > 30:
                problems.append("plugins/%s/.codex-plugin: shortDescription over 30 chars" % name)
            for asset in (ui.get("logo"), ui.get("composerIcon")):
                if asset and not os.path.exists(os.path.join(d, asset)):
                    problems.append("plugins/%s: asset %s not found" % (name, asset))
        entry = next((e for e in marketplace["plugins"] if e["name"] == name), None)
        if entry and entry.get("version"):
            versions["marketplace"] = entry["version"]
        if len(set(versions.values())) > 1:
            problems.append("plugins/%s: versions differ %s" % (name, versions))
        # Everything a skill references must be inside the plugin folder.
        for skill in glob.glob(os.path.join(d, "skills", "*", "SKILL.md")):
            if "../" in open(skill, encoding="utf-8").read():
                notes.append("%s references a parent path: make sure it stays inside the plugin" % rel(skill))

    for cmd in (["tools/validate.py"], ["tools/test_route.py"]):
        r = subprocess.run([sys.executable] + cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            problems.append("%s failed:\n%s" % (cmd[0], (r.stdout + r.stderr)[-1500:]))

    if shutil.which("claude"):
        for target in ["."] + ["plugins/%s" % n for n in PLUGINS]:
            r = subprocess.run(["claude", "plugin", "validate", target, "--strict"], cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                problems.append("claude plugin validate %s --strict:\n%s" % (target, (r.stdout + r.stderr)[-1500:]))
    else:
        notes.append("Claude CLI not found: also run `claude plugin validate . --strict` and `claude plugin validate plugins/<name> --strict` before publishing.")


def build():
    for target in ("plugin-zip", "zip", "openai-zip"):
        subprocess.run([sys.executable, "tools/install.py", target], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    print("Built upload ZIPs in dist/: " + ", ".join(sorted(os.listdir(os.path.join(ROOT, "dist")))))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--owner", help="GitHub user/org that will host the repo; replaces %s." % PLACEHOLDER)
    ap.add_argument("--version", help="Set this version in every plugin manifest.")
    ap.add_argument("--check", action="store_true", help="Run checks only.")
    ap.add_argument("--build", action="store_true", help="Also build every upload ZIP into dist/.")
    a = ap.parse_args()
    if a.owner:
        set_owner(a.owner)
    if a.version:
        set_version(a.version)
    check()
    for n in notes:
        print("NOTE  " + n)
    for p in problems:
        print("FAIL  " + p)
    if problems:
        print("\n%d problem(s). Fix them before publishing." % len(problems))
        sys.exit(1)
    print("\nAll release checks passed for: %s" % ", ".join(PLUGINS))
    if a.build:
        build()


if __name__ == "__main__":
    main()
