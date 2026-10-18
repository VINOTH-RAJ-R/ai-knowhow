#!/usr/bin/env python3
"""Cost per arm for an end-to-end run, from the actual text sent and received.

  python3 bench/cost_analysis.py bench/results/2026-10-18 [usage.tsv]

Content cost = (chars of the prompt the model saw / 4) x input price
             + (chars of the visible answer / 4) x output price, at registry list prices.
Hidden thinking tokens are not visible here, so absolute costs are understated for every arm.
If usage.tsv (task, arm, model, tokens, ms) is given, harness-measured totals are reported too;
those include a fixed ~55k-token agent-harness overhead per run that a normal chat/API call wouldn't pay.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(HERE, "..", "plugins", "modelwise", "skills", "modelwise", "registry", "models", "anthropic")
ALIAS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5"}
HARNESS_OVERHEAD = 55500  # median total tokens of the smallest executor runs (tiny prompt + tiny answer)


def price(model_id):
    c = json.load(open(os.path.join(REG, model_id + ".json"), encoding="utf-8"))
    return c["pricing"]["input"], c["pricing"]["output"]


def toks(path):
    return len(open(path, encoding="utf-8").read()) / 4.0 if os.path.exists(path) else 0.0


def main(run, usage_path=None):
    usage = {}
    if usage_path:
        for line in open(usage_path, encoding="utf-8").read().splitlines()[1:]:
            t, a, m, n, ms = line.split("\t")
            usage[(t, a)] = {"model": m, "tokens": int(n), "ms": int(ms)}
    rows = []
    for t in sorted(os.listdir(run)):
        d = os.path.join(run, t)
        route = os.path.join(d, "route.md")
        if not os.path.isfile(route):
            continue
        routed = re.search(r"ROUTE_MODEL: (\S+)", open(route, encoding="utf-8").read()).group(1)
        arms = {"A": ("claude-opus-5-5", "prompt.txt"), "B": (routed, "structured_prompt.txt"), "C": (routed, "prompt.txt")}
        row = {"task": t, "routed_model": routed}
        for arm, (model, prompt_file) in arms.items():
            pin, pout = price(model)
            tin, tout = toks(os.path.join(d, prompt_file)), toks(os.path.join(d, arm + ".md"))
            row[arm] = {"model": model, "in_tok": round(tin), "out_tok": round(tout),
                        "cost_usd": round((tin * pin + tout * pout) / 1e6, 5)}
            u = usage.get((t, arm))
            if u:
                row[arm].update({"harness_tokens": u["tokens"], "seconds": round(u["ms"] / 1000, 1)})
        s = usage.get((t, "skill"))
        if s:
            content = max(s["tokens"] - HARNESS_OVERHEAD, 0)
            pin, pout = price("claude-sonnet-5-5")
            # The skill run is read-heavy: assume 90% input / 10% output of its content tokens.
            row["skill"] = {"model": "claude-sonnet-5-5", "content_tok_est": content,
                            "cost_usd_est": round((content * 0.9 * pin + content * 0.1 * pout) / 1e6, 4),
                            "seconds": round(s["ms"] / 1000, 1)}
        rows.append(row)
    tot = {a: sum(r[a]["cost_usd"] for r in rows) for a in "ABC"}
    tot["skill"] = sum(r.get("skill", {}).get("cost_usd_est", 0) for r in rows)
    out = {"rows": rows, "totals_usd": {k: round(v, 4) for k, v in tot.items()},
           "B_vs_A_task_cost_ratio": round(tot["B"] / tot["A"], 3) if tot["A"] else None}
    print(json.dumps(out, indent=2))
    with open(os.path.join(run, "costs.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
