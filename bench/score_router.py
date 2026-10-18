#!/usr/bin/env python3
"""Score classification predictions against bench/router/prompts.jsonl.

  python3 bench/score_router.py predictions.json

predictions.json: [{"id": 1, "task": "code.quick", "complexity": "simple", "priority": "balanced"}, ...]

Reports task accuracy, complexity accuracy (any acceptable level counts), priority accuracy,
and route agreement: does the model the router picks from the prediction match a model the
router would pick from any acceptable gold label?
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "plugins", "modelwise", "skills", "modelwise", "scripts"))
import route  # noqa: E402


def pick(reg, task, cx, pr):
    try:
        r = route.route(task, cx, pr, "any", registry=reg)
    except SystemExit:
        return None
    rec = r["recommended"] or (r["fallback"] or {}).get("route", {}).get("recommended")
    return rec["model"] if rec else None


def main(path):
    reg = route.load_registry()
    gold = {g["id"]: g for g in (json.loads(l) for l in open(os.path.join(HERE, "router", "prompts.jsonl"), encoding="utf-8"))}
    preds = {p["id"]: p for p in json.load(open(path, encoding="utf-8"))}
    n = len(gold)
    t_ok = c_ok = p_ok = r_ok = 0
    misses = []
    for gid, g in gold.items():
        p = preds.get(gid, {})
        task_ok = p.get("task") == g["task"]
        cx_ok = p.get("complexity") in g["complexity"]
        pr_ok = p.get("priority", "balanced") == g["priority"]
        gold_models = {pick(reg, g["task"], cx, g["priority"]) for cx in g["complexity"]}
        route_ok = pick(reg, p.get("task", ""), p.get("complexity", "moderate"), p.get("priority", "balanced")) in gold_models
        t_ok += task_ok
        c_ok += cx_ok
        p_ok += pr_ok
        r_ok += route_ok
        if not (task_ok and cx_ok and route_ok):
            misses.append({"id": gid, "prompt": g["prompt"][:70], "gold": [g["task"], g["complexity"]],
                           "pred": [p.get("task"), p.get("complexity")], "route_ok": route_ok})
    out = {"n": n, "task_accuracy": round(t_ok / n, 3), "complexity_accuracy": round(c_ok / n, 3),
           "priority_accuracy": round(p_ok / n, 3), "route_agreement": round(r_ok / n, 3), "misses": misses}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
