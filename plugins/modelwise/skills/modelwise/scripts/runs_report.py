#!/usr/bin/env python3
"""Compare logged modelwise-run quotes with what each helper run really used.

Standard library only, reads local files only:
  - the run log written by log_run.py (~/.claude/modelwise/runs.jsonl)
  - Claude Code helper transcripts (~/.claude/projects/*/*/subagents/agent-*.jsonl and .meta.json)
Actual cost = the helper's token usage at the registry's list prices (cache writes at 1.25x input).

Example:
  python3 runs_report.py            # table + summary
  python3 runs_report.py --json     # machine-readable
"""
import argparse
import datetime
import glob
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.normpath(os.path.join(HERE, "..", "registry", "models"))
LOG = os.environ.get("MODELWISE_LOG_PATH",
                     os.path.join(os.path.expanduser("~"), ".claude", "modelwise", "runs.jsonl"))
PROJECTS = os.path.join(os.path.expanduser("~"), ".claude", "projects")


def prices(model_id):
    for path in glob.glob(os.path.join(REGISTRY, "*", model_id + ".json")):
        p = json.load(open(path, encoding="utf-8")).get("pricing") or {}
        if p.get("unit") == "usd_per_mtok" and p.get("input") is not None:
            cached = p.get("cached_input") if p.get("cached_input") is not None else p["input"] * 0.1
            return p["input"], p["output"], cached
    return None


def parse_ts(s):
    try:
        return datetime.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
    except (TypeError, ValueError):
        return None


def helper_runs():
    """Every modelwise runner transcript with its token totals."""
    runs = []
    for meta_path in glob.glob(os.path.join(PROJECTS, "*", "*", "subagents", "*.meta.json")):
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if "modelwise" not in (meta.get("agentType") or ""):
            continue
        usage, model, first, steps = {}, None, None, 0
        for line in open(meta_path.replace(".meta.json", ".jsonl"), encoding="utf-8", errors="ignore"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") != "assistant":
                continue
            m = e.get("message") or {}
            first = first or e.get("timestamp")
            model = m.get("model") or model
            if m.get("usage"):
                usage[m.get("id") or len(usage)] = m["usage"]
        tot = {"in": 0, "out": 0, "cr": 0, "cw": 0}
        for u in usage.values():
            tot["in"] += u.get("input_tokens") or 0
            tot["out"] += u.get("output_tokens") or 0
            tot["cr"] += u.get("cache_read_input_tokens") or 0
            tot["cw"] += u.get("cache_creation_input_tokens") or 0
        p = prices(model or "")
        cost = None
        if p:
            pin, pout, pc = p
            cost = (tot["in"] * pin + tot["cw"] * pin * 1.25 + tot["cr"] * pc + tot["out"] * pout) / 1e6
        runs.append({"desc": meta.get("description") or "", "start": parse_ts(first), "model": model,
                     "steps": len(usage), "actual": cost})
    return runs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if not os.path.exists(LOG):
        print("No run log yet at %s. modelwise-run writes one line per run from v0.3.8." % LOG)
        return 0
    logged = [json.loads(l) for l in open(LOG, encoding="utf-8") if l.strip()]
    helpers = helper_runs()
    rows = []
    for entry in logged:
        if entry.get("outcome") == "cancelled":
            rows.append(dict(entry, actual=None, steps=None, ratio=None))
            continue
        t = parse_ts(entry.get("ts"))
        best = None
        for h in helpers:
            if not h["start"] or not t or h["desc"] != entry.get("desc"):
                continue
            gap = abs((t - h["start"]).total_seconds())
            if best is None or gap < best[0]:
                best = (gap, h)
        h = best[1] if best else None
        actual = round(h["actual"], 2) if h and h["actual"] is not None else None
        typical = (entry.get("quoted") or {}).get("typical")
        rows.append(dict(entry, actual=actual, steps=h["steps"] if h else None,
                         ratio=round(actual / typical, 2) if actual and typical else None))
    if args.json:
        print(json.dumps(rows, indent=2, default=str))
        return 0
    print("%-17s %-24s %-8s %-18s %8s %6s %6s  %s" % ("when", "route", "effort", "quoted (range)", "actual", "x", "steps", "run"))
    for r in rows:
        q = r.get("quoted") or {}
        rng = "%s (%s-%s)" % (q.get("typical"), q.get("low"), q.get("high")) if q.get("typical") is not None else "-"
        inside = ""
        if r["actual"] is not None and q.get("low") is not None:
            inside = "" if q["low"] <= r["actual"] <= q["high"] else " OUT"
        print("%-17s %-24s %-8s %-18s %8s %6s %6s  %s%s" % (
            (r.get("ts") or "")[:16], (r["model"].replace("claude-", "") + " " + r["task"])[:24], r.get("effort"),
            rng[:18], "-" if r["actual"] is None else "$%.2f" % r["actual"], r["ratio"] or "-", r["steps"] or "-",
            (r.get("desc") or "") + ("" if r.get("outcome") == "finished" else " [%s]" % r.get("outcome")), inside))
    measured = [r for r in rows if r["ratio"]]
    if measured:
        inside = sum(1 for r in measured if r["quoted"]["low"] <= r["actual"] <= r["quoted"]["high"])
        print("\n%d runs measured · actual / typical quote: median %.2fx · inside the quoted range: %d of %d"
              % (len(measured), statistics.median(r["ratio"] for r in measured), inside, len(measured)))
    unmatched = sum(1 for r in rows if r["actual"] is None and r.get("outcome") != "cancelled")
    if unmatched:
        print("%d logged runs had no matching helper transcript on this machine (other machine, desktop app, or cleared history)." % unmatched)
    return 0


if __name__ == "__main__":
    sys.exit(main())
