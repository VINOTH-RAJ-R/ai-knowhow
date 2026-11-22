#!/usr/bin/env python3
"""Append one line per modelwise-run hand-off to a local log, so quotes can be checked later.

Standard library only. Writes to ~/.claude/modelwise/runs.jsonl (or $MODELWISE_LOG_PATH).
Stores the route, the quoted price and, when the app reports it, your plan-usage percentages before and
after the run (used to learn how much of your limit a run takes). Never prompt text, file contents or results.
Set MODELWISE_LOG=0 to turn logging off.

Example:
  python3 log_run.py --task code.build --complexity complex --priority balanced \\
      --model claude-opus-5-5 --effort high --typical 13.64 --low 3.62 --high 33.09 \\
      --outcome finished --desc "Backend hardening" --version 0.3.8
"""
import argparse
import datetime
import json
import os
import sys

DEFAULT_PATH = os.path.join(os.path.expanduser("~"), ".claude", "modelwise", "runs.jsonl")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Log one modelwise-run hand-off (local file only).")
    ap.add_argument("--task", required=True)
    ap.add_argument("--complexity", required=True)
    ap.add_argument("--priority", default="balanced")
    ap.add_argument("--model", required=True)
    ap.add_argument("--effort", default="default")
    ap.add_argument("--typical", type=float)
    ap.add_argument("--low", type=float)
    ap.add_argument("--high", type=float)
    ap.add_argument("--outcome", required=True, choices=["finished", "failed", "cancelled"])
    ap.add_argument("--desc", default="", help="The Agent description (3-5 words). No prompt text.")
    ap.add_argument("--version", default="")
    ap.add_argument("--checkpoint", default="", help="Checkpoint file the run wrote, if any.")
    ap.add_argument("--plan", default="", help="Plan name from the usage tool (e.g. Team, Max).")
    for window in ("5h", "week"):
        ap.add_argument("--pct-%s-before" % window, type=float, help="Percent of the %s limit used before the run." % window)
        ap.add_argument("--pct-%s-after" % window, type=float, help="Percent of the %s limit used after the run." % window)
    args = ap.parse_args(argv)

    if os.environ.get("MODELWISE_LOG", "1") == "0":
        print("modelwise log is off (MODELWISE_LOG=0); nothing written.")
        return 0
    path = os.environ.get("MODELWISE_LOG_PATH", DEFAULT_PATH)
    entry = {
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": args.version,
        "task": args.task,
        "complexity": args.complexity,
        "priority": args.priority,
        "model": args.model,
        "effort": args.effort,
        "quoted": {"typical": args.typical, "low": args.low, "high": args.high},
        "outcome": args.outcome,
        "desc": args.desc[:80],
    }
    if args.checkpoint:
        entry["checkpoint"] = args.checkpoint
    usage = {k: v for k, v in (("plan", args.plan or None),
                               ("pct_5h_before", args.pct_5h_before), ("pct_5h_after", args.pct_5h_after),
                               ("pct_week_before", args.pct_week_before), ("pct_week_after", args.pct_week_after))
             if v is not None}
    if usage:
        entry["usage"] = usage
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print("Logged to %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
