#!/usr/bin/env python3
"""Validate the whole repo: model cards, task taxonomy, templates, skills, manifests, routing table.

Standard library only. Exit code 1 on errors; warnings don't fail the build.
  python3 tools/validate.py            # validate
  python3 tools/validate.py --fix      # also regenerate ROUTING_TABLE.md
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MW = os.path.join(ROOT, "plugins", "modelwise", "skills", "modelwise")
REG = os.path.join(MW, "registry")
STALE_DAYS = 45
SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001 - report any parse problem
        err("%s: invalid JSON (%s)" % (rel(path), e))
        return None


def rel(path):
    return os.path.relpath(path, ROOT)


def check_cards(schema, task_ids):
    props = schema["properties"]
    enums = {k: set(v["enum"]) for k, v in props.items() if "enum" in v}
    caps = set(props["capabilities"]["items"]["enum"])
    units = set(props["pricing"]["properties"]["unit"]["enum"])
    seen = set()
    for path in sorted(glob.glob(os.path.join(REG, "models", "*", "*.json"))):
        c = load(path)
        if c is None:
            continue
        name = rel(path)
        for k in schema["required"]:
            if k not in c:
                err("%s: missing required field '%s'" % (name, k))
        for k in c:
            if k not in props:
                err("%s: unknown field '%s'" % (name, k))
        for k, allowed in enums.items():
            if k in c and c[k] not in allowed:
                err("%s: %s='%s' not in %s" % (name, k, c[k], sorted(allowed)))
        mid = c.get("id", "")
        if os.path.basename(path) != mid + ".json":
            err("%s: file name must be <id>.json" % name)
        if os.path.basename(os.path.dirname(path)) != c.get("provider"):
            err("%s: provider must match its folder" % name)
        if mid in seen:
            err("%s: duplicate id" % name)
        seen.add(mid)
        for cap in c.get("capabilities", []):
            if cap not in caps:
                err("%s: unknown capability '%s'" % (name, cap))
        p = c.get("pricing", {})
        if p.get("unit") not in units:
            err("%s: pricing.unit must be one of %s" % (name, sorted(units)))
        eff = c.get("effort", {})
        if eff.get("default") is not None and eff.get("levels") and eff["default"] not in eff["levels"] + ["auto"]:
            err("%s: effort.default '%s' not in effort.levels" % (name, eff["default"]))
        for m in (eff.get("map") or {}).values():
            if eff.get("levels") and m not in eff["levels"]:
                err("%s: effort.map value '%s' not in effort.levels" % (name, m))
        for t, v in c.get("fit", {}).items():
            if t not in task_ids:
                err("%s: fit for unknown task '%s'" % (name, t))
            if not isinstance(v, (int, float)) or not 0 <= v <= 5:
                err("%s: fit[%s] must be 0-5" % (name, t))
        if not c.get("sources"):
            err("%s: needs at least one source" % name)
        guide = c.get("prompt_style")
        if guide and not os.path.exists(os.path.join(MW, "guides", guide)):
            err("%s: prompt_style guide '%s' not found" % (name, guide))
        try:
            d = datetime.date.fromisoformat(c.get("verified", ""))
            if (datetime.date.today() - d).days > STALE_DAYS and c.get("status") in ("current", "previous"):
                warn("%s: verified %s is older than %d days" % (name, d, STALE_DAYS))
        except ValueError:
            err("%s: verified must be YYYY-MM-DD" % name)
        if c.get("status") == "deprecated" and not c.get("retires"):
            warn("%s: deprecated without a retires date" % name)
    return seen


def check_tasks(tasks, model_ids):
    ids = set()
    for t in tasks["tasks"]:
        ids.add(t["id"])
        tpl = os.path.join(MW, t["template"])
        if not os.path.exists(tpl):
            err("tasks.json: %s template %s missing" % (t["id"], t["template"]))
        for cx in ("simple", "moderate", "complex", "frontier"):
            if cx not in t["effort"]:
                err("tasks.json: %s missing effort for %s" % (t["id"], cx))
        fb = t.get("fallback")
        if fb and fb["task"] not in [x["id"] for x in tasks["tasks"]]:
            err("tasks.json: %s fallback task %s unknown" % (t["id"], fb["task"]))
    return ids


def frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    keys, fm = {}, m.group(1)
    for line in fm.splitlines():
        if line and not line.startswith(" ") and ":" in line:
            k, v = line.split(":", 1)
            keys[k.strip()] = v.strip()
    return keys, text


def check_skills():
    for path in glob.glob(os.path.join(ROOT, "plugins", "*", "skills", "*", "SKILL.md")) + \
            glob.glob(os.path.join(ROOT, "examples", "lessons", "*", "SKILL.md")):
        fm, text = frontmatter(path)
        name = rel(path)
        if fm is None:
            err("%s: missing frontmatter" % name)
            continue
        extra = set(fm) - SKILL_KEYS
        if extra:
            err("%s: frontmatter keys %s are not in the Agent Skills standard (claude.ai upload rejects them)" % (name, sorted(extra)))
        folder = os.path.basename(os.path.dirname(path))
        if fm.get("name") != folder:
            err("%s: name '%s' must match folder '%s'" % (name, fm.get("name"), folder))
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm.get("name", "")) or len(fm.get("name", "")) > 64:
            err("%s: name must be lowercase kebab-case, max 64 chars" % name)
        if not 0 < len(fm.get("description", "")) <= 1024:
            err("%s: description must be 1-1024 chars (is %d)" % (name, len(fm.get("description", ""))))
        if text.count("\n") > 500:
            warn("%s: SKILL.md is over 500 lines" % name)


def check_manifests():
    mp = load(os.path.join(ROOT, ".claude-plugin", "marketplace.json"))
    if mp:
        for p in mp["plugins"]:
            src = os.path.join(ROOT, p["source"])
            if not os.path.isdir(src):
                err("marketplace.json: source %s missing" % p["source"])
            pj = load(os.path.join(src, ".claude-plugin", "plugin.json"))
            if pj and pj.get("name") != p["name"]:
                err("plugin.json name '%s' != marketplace entry '%s'" % (pj.get("name"), p["name"]))
    cx = load(os.path.join(ROOT, ".agents", "plugins", "marketplace.json"))
    if cx:
        for p in cx["plugins"]:
            if not os.path.isdir(os.path.join(ROOT, p["source"]["path"])):
                err(".agents marketplace: source %s missing" % p["source"]["path"])


def check_routing_table(fix):
    out = subprocess.run([sys.executable, os.path.join(MW, "scripts", "route.py"), "--table"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        err("route.py --table failed: %s" % out.stderr.strip())
        return
    path = os.path.join(MW, "ROUTING_TABLE.md")
    current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if current != out.stdout:
        if fix:
            with open(path, "w", encoding="utf-8") as f:
                f.write(out.stdout)
            print("Regenerated %s" % rel(path))
        else:
            err("ROUTING_TABLE.md is out of date: run python3 tools/validate.py --fix")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="Regenerate ROUTING_TABLE.md")
    args = ap.parse_args()
    schema = load(os.path.join(REG, "model.schema.json"))
    tasks = load(os.path.join(REG, "tasks.json"))
    load(os.path.join(REG, "effort-scale.json"))
    if schema and tasks:
        task_ids = check_tasks(tasks, set())
        check_cards(schema, task_ids)
    check_skills()
    check_manifests()
    check_routing_table(args.fix)
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    n = len(glob.glob(os.path.join(REG, "models", "*", "*.json")))
    print("\n%d model cards, %d errors, %d warnings" % (n, len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
