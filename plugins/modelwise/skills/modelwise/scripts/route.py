#!/usr/bin/env python3
"""Modelwise router: pick a model + effort for a task, using only the registry files.

Standard library only (Python 3.8+), so it runs anywhere the skill is installed.

Examples:
  python3 route.py --task code.build --complexity moderate
  python3 route.py --task image.generate --priority cost --provider openai
  python3 route.py --task research.deep --complexity complex --json
  python3 route.py --list-tasks
  python3 route.py --model claude-sonnet-5-5
  python3 route.py --table > ROUTING_TABLE.md
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.normpath(os.path.join(HERE, "..", "registry"))
E_ORDER = ["E0", "E1", "E2", "E3", "E4", "E5", "E6"]
SPEED_RANK = {"fastest": 3, "fast": 2, "medium": 1, "slow": 0}
DEFAULT_STATUSES = ("current", "previous")
LEGACY_STATUSES = ("current", "previous", "legacy")
# Assumed size of one generation job for per-unit priced media models.
MEDIA_UNITS = {"usd_per_image": 1, "usd_per_second": 8, "usd_per_minute": 1}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_registry(root=REGISTRY):
    tasks = load_json(os.path.join(root, "tasks.json"))
    scale = load_json(os.path.join(root, "effort-scale.json"))
    models = []
    for path in sorted(glob.glob(os.path.join(root, "models", "*", "*.json"))):
        card = load_json(path)
        card["_path"] = os.path.relpath(path, os.path.dirname(root))
        models.append(card)
    return tasks, scale, models


def find_task(tasks, task_id):
    for t in tasks["tasks"]:
        if t["id"] == task_id:
            return t
    ids = ", ".join(t["id"] for t in tasks["tasks"])
    sys.exit("Unknown task '%s'. Known tasks: %s" % (task_id, ids))


def effort_floor(card, task_id, level):
    """Raise the E-level to the card's floor for this task, if it sets one (e.g. {"code.*": "E4"})."""
    floor = None
    for pattern, lvl in ((card.get("effort") or {}).get("floor") or {}).items():
        if pattern == task_id or (pattern.endswith(".*") and task_id.startswith(pattern[:-1])):
            floor = lvl
    if floor and E_ORDER.index(floor) > E_ORDER.index(level):
        return floor
    return level


def native_effort(card, level, scale, round_up, task_id=None):
    """Map a normalized E-level onto the model's own effort setting."""
    if task_id:
        level = effort_floor(card, task_id, level)
    eff = card.get("effort") or {}
    levels = eff.get("levels") or []
    if not eff.get("parameter") or not levels:
        return None
    vendor_map = dict(scale["vendor_mappings"].get(card["provider"], {}).get("map", {}))
    vendor_map.update(eff.get("map") or {})
    wanted = vendor_map.get(level)
    if wanted in levels:
        return wanted
    # Walk the E-scale outward from the wanted level until we hit a supported value.
    idx = E_ORDER.index(level)
    steps = list(range(1, len(E_ORDER)))
    for step in steps:
        for direction in ((1, -1) if round_up else (-1, 1)):
            j = idx + direction * step
            if 0 <= j < len(E_ORDER):
                cand = vendor_map.get(E_ORDER[j])
                if cand in levels:
                    return cand
    return eff.get("default")


def estimate_cost(card, task, complexity):
    p = card.get("pricing") or {}
    unit = p.get("unit")
    if unit == "usd_per_mtok":
        tokens = (task.get("tokens") or {}).get(complexity)
        if not tokens or p.get("input") is None or p.get("output") is None:
            return None
        tin, tout = tokens
        return (tin * p["input"] + tout * p["output"]) / 1_000_000.0
    if unit in MEDIA_UNITS and p.get("per_unit") is not None:
        return p["per_unit"] * MEDIA_UNITS[unit]
    return None


def candidates(task, complexity, models, provider, statuses, tasks):
    need = set(task["requires"])
    min_fit = tasks["min_fit_by_complexity"][complexity]
    pool = []
    for m in models:
        if m["status"] not in statuses:
            continue
        if provider != "any" and m["provider"] != provider:
            continue
        if not need.issubset(set(m.get("capabilities", []))):
            continue
        fit = m.get("fit", {}).get(task["id"], 0)
        if fit <= 0:
            continue
        pool.append((m, fit))
    qualified = [(m, f) for m, f in pool if f >= min_fit]
    relaxed = False
    if not qualified and pool:
        # Nothing clears the bar: keep the strongest options and say so.
        best = max(f for _, f in pool)
        qualified = [(m, f) for m, f in pool if f >= best - 0.5]
        relaxed = True
    return qualified, relaxed


def rank(entries, priority, min_fit):
    """Order candidates for a priority.

    balanced: the cheapest model that clears the quality bar with one point of headroom
              (min_fit + 1, capped at 5). Models below the headroom line come after.
    cost:     the cheapest model that clears the bar.
    quality:  the highest fit, then the cheapest.
    speed:    the fastest model with headroom, then the cheapest.
    """
    big = float("inf")
    target = min(min_fit + 1, 5)

    def cost(e):
        return e["cost"] if e["cost"] is not None else big

    def stale(e):
        return 0 if e["card"]["status"] == "current" else 1

    no_prices = all(e["cost"] is None for e in entries)
    if priority in ("balanced", "cost") and no_prices:
        # No published per-task price (image and audio models): cost can't rank them, so fit decides.
        # For cost priority, speed is the only remaining proxy.
        priority = "speed" if priority == "cost" else "balanced_fit"
    if priority == "balanced_fit":
        key = lambda e: (e["fit"] < target, -e["fit"], stale(e))
    elif priority == "quality":
        key = lambda e: (-e["fit"], stale(e), cost(e))
    elif priority == "cost":
        key = lambda e: (cost(e), -e["fit"], stale(e))
    elif priority == "speed":
        key = lambda e: (e["fit"] < target, -SPEED_RANK.get(e["card"].get("speed", "medium"), 1), cost(e), -e["fit"])
    else:
        key = lambda e: (e["fit"] < target, cost(e), -e["fit"], stale(e))
    return sorted(entries, key=key)


def cost_comparison(task, complexity, models, provider, scale, round_up, min_fit, recommended_id):
    """Every *current* model that can do the task, cheapest first, with its effort, fit and cost.

    Includes models below the quality bar (flagged), so users see what they'd save or risk by switching.
    """
    need = set(task["requires"])
    level = task["effort"][complexity]
    rows = []
    for m in models:
        if m["status"] != "current":
            continue
        if provider != "any" and m["provider"] != provider:
            continue
        fit = m.get("fit", {}).get(task["id"], 0)
        if fit <= 0 or not need.issubset(set(m.get("capabilities", []))):
            continue
        cost = estimate_cost(m, task, complexity)
        if m["id"] == recommended_id:
            note = "recommended"
        elif fit < min_fit:
            note = "below the quality bar for %s tasks" % complexity
        else:
            note = ""
        rows.append({
            "model": m["id"],
            "name": m["display_name"],
            "provider": m["provider"],
            "tier": m["tier"],
            "effort": native_effort(m, level, scale, round_up, task["id"]),
            "fit": fit,
            "meets_quality_bar": fit >= min_fit,
            "est_cost_usd": round(cost, 4) if cost is not None else None,
            "est_cost_per_1000_runs_usd": round(cost * 1000, 2) if cost is not None else None,
            "note": note,
        })
    big = float("inf")
    rows.sort(key=lambda r: (r["est_cost_usd"] if r["est_cost_usd"] is not None else big, -r["fit"], r["model"]))
    return rows


def volume_totals(volume, rows):
    """Totals for running the task `volume` times, at list price and with the 50% Batch discount."""
    if not volume:
        return None
    out = []
    for r in rows:
        c = r["est_cost_usd"]
        out.append({"model": r["model"], "provider": r["provider"],
                    "total_usd": round(c * volume, 2) if c is not None else None,
                    "total_batch_usd": round(c * volume * 0.5, 2) if c is not None else None,
                    "meets_quality_bar": r["meets_quality_bar"]})
    return {"runs": volume, "rows": out,
            "note": "Batch = 50% off for non-urgent jobs (both vendors). Prompt caching of shared instructions lowers it further."}


def route(task_id, complexity="moderate", priority="balanced", provider="any",
          include_legacy=False, registry=None, volume=None):
    registry = registry or load_registry()
    tasks, scale, models = registry
    task = find_task(tasks, task_id)
    level = task["effort"][complexity]
    statuses = LEGACY_STATUSES if include_legacy else DEFAULT_STATUSES
    pool, relaxed = candidates(task, complexity, models, provider, statuses, tasks)
    round_up = priority == "quality" or complexity in ("complex", "frontier")
    entries = []
    for card, fit in pool:
        entries.append({
            "card": card,
            "fit": fit,
            "cost": estimate_cost(card, task, complexity),
            "effort": native_effort(card, level, scale, round_up, task["id"]),
        })
    ranked = rank(entries, priority, tasks["min_fit_by_complexity"][complexity])

    def summary(e, why=None):
        if not e:
            return None
        c = e["card"]
        out = {
            "model": c["id"],
            "name": c["display_name"],
            "provider": c["provider"],
            "tier": c["tier"],
            "status": c["status"],
            "fit": e["fit"],
            "effort": e["effort"],
            "effort_parameter": (c.get("effort") or {}).get("parameter"),
            "est_cost_usd": round(e["cost"], 4) if e["cost"] is not None else None,
            "prompt_style": c.get("prompt_style"),
            "card": c["_path"],
            "watch_out": c.get("watch_out", []),
            "prompt_tips": c.get("prompt_tips", []),
            "verified": c.get("verified"),
        }
        if why:
            out["why"] = why
        return out

    top = ranked[0] if ranked else None
    cheaper = None
    stronger = None
    if top:
        cheaper_pool = [e for e in ranked if e is not top and e["cost"] is not None and top["cost"] is not None and e["cost"] < top["cost"]]
        if cheaper_pool:
            cheaper = sorted(cheaper_pool, key=lambda e: (-e["fit"], e["cost"]))[0]
        stronger_pool = [e for e in ranked if e is not top and e["fit"] > top["fit"]]
        if stronger_pool:
            stronger = sorted(stronger_pool, key=lambda e: (-e["fit"], e["cost"] or 0))[0]
    per_provider = {}
    for e in ranked:
        per_provider.setdefault(e["card"]["provider"], e)
    # A model from another vendor with the same fit and cost is a genuine tie; say so rather than pretend.
    tie = None
    if top:
        for e in ranked[1:]:
            if (e["card"]["provider"] != top["card"]["provider"] and e["fit"] == top["fit"]
                    and e["cost"] is not None and top["cost"] is not None
                    and abs(e["cost"] - top["cost"]) <= 0.05 * top["cost"]):
                tie = e
                break

    min_fit = tasks["min_fit_by_complexity"][complexity]
    comparison = cost_comparison(task, complexity, models, provider, scale, round_up, min_fit,
                                 top["card"]["id"] if top else None)

    fallback = None
    if not top and task.get("fallback"):
        fb = task["fallback"]
        fallback = {"note": fb["note"],
                    "route": route(fb["task"], complexity, priority, provider, include_legacy, registry)}

    return {
        "task": task_id,
        "task_label": task["label"],
        "complexity": complexity,
        "priority": priority,
        "provider_filter": provider,
        "effort_level": level,
        "effort_level_name": next(l["name"] for l in scale["levels"] if l["level"] == level),
        "template": task["template"],
        "relaxed_quality_bar": relaxed,
        "recommended": summary(top),
        "ranking_basis": ("list price" if any(e["cost"] is not None for e in entries)
                          else "fit (no published prices for this task)"),
        "tie_with": summary(tie, "Same fit and about the same cost from another vendor: either is a good choice."),
        "fallback": fallback,
        "cheaper_option": summary(cheaper, "Lower cost; quality may drop a little."),
        "stronger_option": summary(stronger, "Higher quality ceiling at higher cost."),
        "best_per_provider": {k: summary(v) for k, v in per_provider.items()},
        "ranked": [summary(e) for e in ranked[:6]],
        "cost_comparison": comparison,
        "volume": volume_totals(volume, comparison),
        "app_settings": scale.get("app_mappings", {}),
        "cost_note": "List-price estimate for one typical task of this size, without caching or batch discounts. Use it to compare models, not as a quote.",
    }


def fmt_cost(c):
    if c is None:
        return "n/a"
    if c < 0.01:
        return "<$0.01"
    return "$%.2f" % c


def print_human(r):
    print("Task:        %s  (%s)" % (r["task"], r["task_label"]))
    print("Complexity:  %s   Priority: %s   Providers: %s" % (r["complexity"], r["priority"], r["provider_filter"]))
    print("Effort:      %s (%s) on the normalized scale" % (r["effort_level"], r["effort_level_name"]))
    print("Template:    %s" % r["template"])
    print("Ranked by:   %s" % r.get("ranking_basis", "list price"))
    if r["relaxed_quality_bar"]:
        print("NOTE: no model fully clears the quality bar for this complexity; showing the strongest available.")
    rec = r["recommended"]
    if not rec:
        print("\nNo model in the registry can do this task with the current filters.")
        if r.get("fallback"):
            print("\n" + r["fallback"]["note"] + "\n")
            print_human(r["fallback"]["route"])
        return
    print("\nRECOMMENDED  %s  [%s]  effort=%s  fit=%s/5  est=%s" % (
        rec["model"], rec["provider"], rec["effort"] or "-", rec["fit"], fmt_cost(rec["est_cost_usd"])))
    for label, key in (("TIE        ", "tie_with"), ("CHEAPER    ", "cheaper_option"), ("STRONGER   ", "stronger_option")):
        o = r[key]
        if o:
            print("%s  %s  [%s]  effort=%s  fit=%s/5  est=%s" % (
                label, o["model"], o["provider"], o["effort"] or "-", o["fit"], fmt_cost(o["est_cost_usd"])))
    print("\nBest per provider:")
    for prov, o in r["best_per_provider"].items():
        print("  %-10s %s  effort=%s  est=%s" % (prov, o["model"], o["effort"] or "-", fmt_cost(o["est_cost_usd"])))
    print_comparison(r["cost_comparison"])
    if r.get("volume"):
        v = r["volume"]
        print("\nFor %d runs (list / with Batch 50%% off):" % v["runs"])
        for row in v["rows"]:
            if row["total_usd"] is not None:
                print("  %-24s $%-10s $%s" % (row["model"], "{:,.2f}".format(row["total_usd"]), "{:,.2f}".format(row["total_batch_usd"])))
    print("\n" + r["cost_note"])


def print_comparison(rows):
    if not rows:
        return
    print("\nCost across current models (per run / per 1,000 runs):")
    for c in rows:
        per_k = "n/a" if c["est_cost_per_1000_runs_usd"] is None else "$%.2f" % c["est_cost_per_1000_runs_usd"]
        print("  %-24s %-9s effort=%-7s fit=%-3s %-7s %-9s %s" % (
            c["model"], c["provider"], c["effort"] or "-", c["fit"], fmt_cost(c["est_cost_usd"]), per_k, c["note"]))


def print_tasks(tasks):
    for t in tasks["tasks"]:
        print("%-18s %s" % (t["id"], t["label"]))


def print_model(models, model_id):
    for m in models:
        if m["id"] == model_id:
            clean = {k: v for k, v in m.items() if not k.startswith("_")}
            print(json.dumps(clean, indent=2))
            return
    sys.exit("Unknown model '%s'." % model_id)


def table(registry):
    tasks, scale, models = registry
    lines = [
        "# Routing table",
        "",
        "Generated by `scripts/route.py --table` from the registry. Do not edit by hand.",
        "Use this when you can't run scripts (e.g. inside ChatGPT): find the task row and the complexity column.",
        "Each cell shows **model @ effort (cost per run)** for priority = balanced.",
        "",
        "**Per run** = one typical task of that size (for extraction/classification: one item). Multiply by your volume; Batch halves it.",
        "",
        "**Other priorities without the script:** *cost* → the cheapest ✓ row in the task's cost table; *quality* → the highest-fit row (frontier column);",
        "*speed* → the fast/fastest tier with ✓. **One vendor only:** use only that vendor's rows — its cheapest ✓ row is the budget pick, its next row up is the stronger pick.",
        "",
        "**Setting the model and effort in apps:**",
        "",
    ]
    for app, how in scale.get("app_mappings", {}).items():
        if not app.startswith("$"):
            lines.append("- **%s**: %s" % (app, how))
    lines.append("")
    for t in tasks["tasks"]:
        lines.append("## %s: %s" % (t["id"], t["label"]))
        lines.append("")
        lines.append("Template: `%s`" % t["template"])
        lines.append("")
        if t.get("fallback") and not route(t["id"], "moderate", "balanced", "any", registry=registry)["recommended"]:
            lines.append("> %s Routes shown are for `%s`." % (t["fallback"]["note"], t["fallback"]["task"]))
            lines.append("")
            t = dict(find_task(tasks, t["fallback"]["task"]), template=t["template"])
        lines.append("| Complexity | Effort | Recommended | Cheaper | Best Anthropic | Best OpenAI |")
        lines.append("|---|---|---|---|---|---|")
        for cx in ("simple", "moderate", "complex", "frontier"):
            r = route(t["id"], cx, "balanced", "any", registry=registry)

            def cell(o):
                if not o:
                    return "-"
                return "%s @ %s (%s)" % (o["model"], o["effort"] or "default", fmt_cost(o["est_cost_usd"]))

            bp = r["best_per_provider"]
            lines.append("| %s | %s %s | %s | %s | %s | %s |" % (
                cx, r["effort_level"], r["effort_level_name"], cell(r["recommended"]), cell(r["cheaper_option"]),
                cell(bp.get("anthropic")), cell(bp.get("openai"))))
        lines.append("")
        # Cost of every current model at each complexity, so users can compare without the script.
        grid = {cx: {c["model"]: c for c in route(t["id"], cx, "balanced", "any", registry=registry)["cost_comparison"]}
                for cx in ("simple", "moderate", "complex", "frontier")}
        ids = sorted({m for cx in grid for m in grid[cx]},
                     key=lambda m: (next((grid[cx][m]["est_cost_usd"] or 0) for cx in grid if m in grid[cx]), m))
        if ids:
            lines.append("Cost per run across current models (✓ = clears the quality bar at that complexity; @ = effort):")
            lines.append("")
            lines.append("| Model | simple | moderate | complex | frontier |")
            lines.append("|---|---|---|---|---|")
            for m in ids:
                cells = []
                for cx in ("simple", "moderate", "complex", "frontier"):
                    c = grid[cx].get(m)
                    cells.append("-" if not c else "%s%s @%s" % (fmt_cost(c["est_cost_usd"]), " ✓" if c["meets_quality_bar"] else "", c["effort"] or "default"))
                lines.append("| %s | %s |" % (m, " | ".join(cells)))
            lines.append("")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Recommend a model and effort level from the Modelwise registry.")
    ap.add_argument("--task", help="Task id from registry/tasks.json (see --list-tasks).")
    ap.add_argument("--complexity", default="moderate", choices=["simple", "moderate", "complex", "frontier"])
    ap.add_argument("--priority", default="balanced", choices=["quality", "balanced", "cost", "speed"])
    ap.add_argument("--provider", default="any", choices=["any", "anthropic", "openai"])
    ap.add_argument("--include-legacy", action="store_true", help="Also consider legacy models.")
    ap.add_argument("--volume", type=int, help="How many times the task runs (e.g. 50000 tickets): adds total and batch cost.")
    ap.add_argument("--json", action="store_true", help="Machine-readable output.")
    ap.add_argument("--list-tasks", action="store_true")
    ap.add_argument("--model", help="Print one model card.")
    ap.add_argument("--table", action="store_true", help="Print the full routing table as Markdown.")
    args = ap.parse_args(argv)

    registry = load_registry()
    if args.list_tasks:
        print_tasks(registry[0])
    elif args.model:
        print_model(registry[2], args.model)
    elif args.table:
        sys.stdout.write(table(registry))
    elif args.task:
        r = route(args.task, args.complexity, args.priority, args.provider, args.include_legacy, registry, args.volume)
        if args.json:
            print(json.dumps(r, indent=2))
        else:
            print_human(r)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
