#!/usr/bin/env python3
"""Automated A/B benchmark over the vendor APIs: real token counts, real effort settings, both vendors.

  pip install anthropic openai            # only this runner needs them
  export ANTHROPIC_API_KEY=... OPENAI_API_KEY=...   # either or both; missing vendors are skipped
  python3 bench/run_api.py                          # all tasks, default arms
  python3 bench/run_api.py --tasks ipv4,dedupe --effort-sweep
  python3 bench/score.py --run bench/results/<date>-api   # then score

Arms per task (each runs only if its vendor key is set):
  A        baseline: a strong default model at its default effort, raw prompt     (--baseline, default claude-opus-5-5)
  C        modelwise route (model + effort from route.py using the task's gold label), raw prompt
  B        same route, structured prompt  (needs <task>/structured_prompt.txt from a skill run; copied from --prompts)
  A-oai    OpenAI baseline (gpt-6-astra), raw prompt
  C-oai    route.py's best OpenAI pick and effort, raw prompt
  sweep-*  with --effort-sweep: the routed Claude model at low / medium / high, raw prompt

This spends real money (a full run is typically a few dollars at list prices). Results go to
bench/results/<YYYY-MM-DD>-api/ with meta.json holding per-arm model, effort, tokens, seconds and cost.
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "plugins", "modelwise", "skills", "modelwise", "scripts"))
import route  # noqa: E402

REG = route.load_registry()
CARDS = {c["id"]: c for c in REG[2]}
FALLBACK_MODELS = {"claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5"}


def cost(model, tin, tout):
    p = CARDS[model]["pricing"]
    return round((tin * (p.get("input") or 0) + tout * (p.get("output") or 0)) / 1e6, 6)


def call_anthropic(client, model, effort, prompt):
    import anthropic
    kwargs = dict(model=model, max_tokens=16000, messages=[{"role": "user", "content": prompt}])
    if effort:
        kwargs["output_config"] = {"effort": effort}
    t0 = time.time()
    try:
        if model in FALLBACK_MODELS:
            # Server-side refusal fallback (recommended default). We record when it ran, because a
            # fallback means a different model answered and that row must be read with care.
            resp = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
        else:
            resp = client.messages.create(**kwargs)
    except anthropic.APIStatusError as e:
        return {"error": "%s: %s" % (e.status_code, e.message)}
    text = "".join(b.text for b in resp.content if b.type == "text")
    fallback_ran = any(getattr(i, "type", None) == "fallback_message" for i in (getattr(resp.usage, "iterations", None) or []))
    tin, tout = resp.usage.input_tokens, resp.usage.output_tokens
    return {"text": text, "in_tok": tin, "out_tok": tout, "seconds": round(time.time() - t0, 1),
            "cost_usd": cost(model, tin, tout), "stop_reason": resp.stop_reason, "fallback_ran": fallback_ran}


def call_openai(client, model, effort, prompt):
    t0 = time.time()
    kwargs = dict(model=model, input=prompt)
    if effort:
        kwargs["reasoning"] = {"effort": effort}
    try:
        resp = client.responses.create(**kwargs)
    except Exception as e:  # noqa: BLE001 - report and continue with the other arms
        return {"error": str(e)[:200]}
    tin, tout = resp.usage.input_tokens, resp.usage.output_tokens
    return {"text": resp.output_text, "in_tok": tin, "out_tok": tout, "seconds": round(time.time() - t0, 1),
            "cost_usd": cost(model, tin, tout)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tasks", help="Comma-separated task ids (default: all in e2e/tasks.json).")
    ap.add_argument("--baseline", default="claude-opus-5-5")
    ap.add_argument("--prompts", default=os.path.join(HERE, "results", "2026-10-18"),
                    help="Folder with <task>/structured_prompt.txt from a modelwise skill run (arm B).")
    ap.add_argument("--effort-sweep", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    tasks = json.load(open(os.path.join(HERE, "e2e", "tasks.json"), encoding="utf-8"))["tasks"]
    if args.tasks:
        keep = set(args.tasks.split(","))
        tasks = [t for t in tasks if t["id"] in keep]
    out = args.out or os.path.join(HERE, "results", datetime.date.today().isoformat() + "-api")
    os.makedirs(out, exist_ok=True)

    ac = oc = None
    if os.environ.get("ANTHROPIC_API_KEY"):
        import anthropic
        ac = anthropic.Anthropic()
    if os.environ.get("OPENAI_API_KEY"):
        from openai import OpenAI
        oc = OpenAI()
    if not ac and not oc:
        sys.exit("Set ANTHROPIC_API_KEY and/or OPENAI_API_KEY.")

    meta = {}
    for t in tasks:
        d = os.path.join(out, t["id"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "prompt.txt"), "w", encoding="utf-8") as f:
            f.write(t["prompt"])
        g = t["gold_route"]
        r = route.route(g["task"], g["complexity"][0], "balanced", "any", registry=REG)
        rec = r["recommended"] or r["fallback"]["route"]["recommended"]
        best_a = r["best_per_provider"].get("anthropic") or rec
        best_o = r["best_per_provider"].get("openai")
        sp_src = os.path.join(args.prompts, t["id"], "structured_prompt.txt")
        structured = open(sp_src, encoding="utf-8").read() if os.path.exists(sp_src) else None
        if structured:
            shutil.copy(sp_src, os.path.join(d, "structured_prompt.txt"))

        arms = []
        if ac:
            arms += [("A", "anthropic", args.baseline, None, t["prompt"]),
                     ("C", "anthropic", best_a["model"], best_a["effort"], t["prompt"])]
            if structured:
                arms.append(("B", "anthropic", best_a["model"], best_a["effort"], structured))
            if args.effort_sweep:
                arms += [("sweep-%s" % e, "anthropic", best_a["model"], e, t["prompt"]) for e in ("low", "medium", "high")]
        if oc and best_o:
            arms += [("A-oai", "openai", "gpt-6-astra", None, t["prompt"]),
                     ("C-oai", "openai", best_o["model"], best_o["effort"], t["prompt"])]

        for arm, vendor, model, effort, prompt in arms:
            res = call_anthropic(ac, model, effort, prompt) if vendor == "anthropic" else call_openai(oc, model, effort, prompt)
            if "text" in res:
                with open(os.path.join(d, arm + ".md"), "w", encoding="utf-8") as f:
                    f.write(res.pop("text"))
            meta.setdefault(t["id"], {})[arm] = dict(res, model=model, effort=effort or "default")
            print("%-15s %-10s %-20s %-8s %s" % (t["id"], arm, model, effort or "default",
                                                 res.get("error") or "$%.5f  %ss" % (res["cost_usd"], res["seconds"])))
        with open(os.path.join(out, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
    print("\nNow score: python3 bench/score.py --run %s" % out)


if __name__ == "__main__":
    main()
