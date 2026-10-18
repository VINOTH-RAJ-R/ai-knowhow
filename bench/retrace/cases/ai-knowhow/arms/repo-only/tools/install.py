#!/usr/bin/env python3
"""Install the skills where your AI tool looks for them, or build upload ZIPs.

Standard library only.

  python3 tools/install.py claude-code            # ~/.claude/skills/  (add --project for ./.claude/skills/)
  python3 tools/install.py codex                  # ~/.agents/skills/  (add --project for ./.agents/skills/)
  python3 tools/install.py zip                    # dist/<skill>.zip for claude.ai / ChatGPT skill upload
  python3 tools/install.py plugin-zip             # dist/<plugin>-plugin.zip for claude.ai + Cowork plugin upload
  python3 tools/install.py claude-code --skills modelwise
  python3 tools/install.py claude-code --dry-run
"""
import argparse
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = {
    "modelwise": os.path.join(ROOT, "plugins", "modelwise", "skills", "modelwise"),
    "retrace": os.path.join(ROOT, "plugins", "retrace", "skills", "retrace"),
    "teach": os.path.join(ROOT, "plugins", "retrace", "skills", "teach"),
}
PLUGINS = {
    "modelwise": os.path.join(ROOT, "plugins", "modelwise"),
    "retrace": os.path.join(ROOT, "plugins", "retrace"),
}
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def target_dir(target, project):
    base = os.getcwd() if project else os.path.expanduser("~")
    sub = {"claude-code": ".claude/skills", "codex": ".agents/skills"}[target]
    return os.path.join(base, sub)


def copy_skill(name, dest_root, dry):
    src, dest = SKILLS[name], os.path.join(dest_root, name)
    print("%s %s -> %s" % ("Would copy" if dry else "Copying", os.path.relpath(src, ROOT), dest))
    if dry:
        return
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=IGNORE)


def zip_plugin(name, out_dir, dry):
    """A plugin ZIP has .claude-plugin/plugin.json at its root (claude.ai: Customize → Plugins → Add → Upload plugin)."""
    src = PLUGINS[name]
    path = os.path.join(out_dir, name + "-plugin.zip")
    print("%s %s" % ("Would build" if dry else "Building", os.path.relpath(path, ROOT)))
    if dry:
        return
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in files:
                if f.endswith(".pyc") or f == ".DS_Store":
                    continue
                full = os.path.join(folder, f)
                z.write(full, os.path.relpath(full, src))


def zip_skill(name, out_dir, dry):
    src = SKILLS[name]
    path = os.path.join(out_dir, name + ".zip")
    print("%s %s" % ("Would build" if dry else "Building", os.path.relpath(path, ROOT)))
    if dry:
        return
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for f in files:
                if f.endswith(".pyc") or f == ".DS_Store":
                    continue
                full = os.path.join(folder, f)
                # The skill folder must be the top level inside the archive.
                z.write(full, os.path.join(name, os.path.relpath(full, src)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", choices=["claude-code", "codex", "zip", "plugin-zip"])
    ap.add_argument("--project", action="store_true", help="Install into the current project instead of your home folder.")
    ap.add_argument("--skills", default="modelwise,retrace,teach", help="Comma-separated subset.")
    ap.add_argument("--dest", help="Override the destination folder.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    names = [s.strip() for s in args.skills.split(",") if s.strip()]
    for n in names:
        if n not in SKILLS:
            sys.exit("Unknown skill '%s'. Choose from: %s" % (n, ", ".join(SKILLS)))

    if args.target == "plugin-zip":
        out = args.dest or os.path.join(ROOT, "dist")
        for n in PLUGINS:
            zip_plugin(n, out, args.dry_run)
        print("\nclaude.ai and Cowork: Customize → Plugins → Add → Upload plugin → choose each *-plugin.zip."
              " Plugins sync to Cowork sessions and to Claude Code (same account).")
        return

    if args.target == "zip":
        out = args.dest or os.path.join(ROOT, "dist")
        for n in names:
            zip_skill(n, out, args.dry_run)
        print("\nUpload each ZIP: claude.ai → Customize → Skills → + → Upload a skill"
              " (needs code execution on). ChatGPT Business/Enterprise/Edu: Plugins → Skills → Create → Upload.")
        return

    dest_root = args.dest or target_dir(args.target, args.project)
    if not args.dry_run:
        os.makedirs(dest_root, exist_ok=True)
    for n in names:
        copy_skill(n, dest_root, args.dry_run)
    if args.target == "claude-code":
        print("\nDone. Restart Claude Code (or run /reload-plugins), then try: /modelwise build a todo app")
    else:
        print("\nDone. Restart Codex, then type $modelwise or /skills.")


if __name__ == "__main__":
    main()
