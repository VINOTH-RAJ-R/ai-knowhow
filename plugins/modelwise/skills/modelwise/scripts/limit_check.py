#!/usr/bin/env python3
"""Will this helper run fit in what's left of your plan's usage limits?

Standard library only, local files only. It learns how many list-price dollars of helper work use 1% of
each limit window from your own logged runs (log_run.py records the percent used before and after each
run; runs_report.py finds the run's real token cost). Until it has 3 such runs it only reports the
headroom and says it is still learning.

Example:
  python3 limit_check.py --typical 13.64 --low 3.62 --high 33.09 --steps 60 220 \\
      --pct-5h 41 --resets-5h "18:19" --pct-week 46 --resets-week "Thu 09:59"
  python3 limit_check.py --calibration          # show the learned rates
"""
import argparse
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runs_report  # noqa: E402

MIN_RUNS = 3
WINDOWS = (("5h", "5-hour limit"), ("week", "weekly limit"))


def calibration(log_path=None):
    """Median list-price dollars per 1% of each window, from logged runs with a measured cost."""
    path = log_path or runs_report.LOG
    if not os.path.exists(path):
        return {w: {"usd_per_pct": None, "runs": 0} for w, _ in WINDOWS}
    logged = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    helpers = runs_report.helper_runs()
    samples = {w: [] for w, _ in WINDOWS}
    for entry in logged:
        usage = entry.get("usage") or {}
        if entry.get("outcome") == "cancelled":
            continue
        t = runs_report.parse_ts(entry.get("ts"))
        match = [h for h in helpers if h["desc"] == entry.get("desc") and h["start"] and t]
        if not match:
            continue
        h = min(match, key=lambda h: abs((t - h["start"]).total_seconds()))
        if not h["actual"]:
            continue
        for w, _ in WINDOWS:
            before, after = usage.get("pct_%s_before" % w), usage.get("pct_%s_after" % w)
            # Skip runs that crossed a reset (after < before) or moved the gauge by less than 1%.
            if before is None or after is None or after - before < 1:
                continue
            samples[w].append(h["actual"] / (after - before))
    return {w: {"usd_per_pct": round(statistics.median(s), 3) if len(s) >= MIN_RUNS else None,
                "runs": len(s)} for w, s in samples.items()}


def predict(usd_per_pct, typical, low, high, pct_used, steps=None):
    """Pure function: percent of the window the run would take, and whether it fits."""
    headroom = max(0.0, 100.0 - pct_used)
    out = {"pct_used": pct_used, "headroom_pct": round(headroom, 1)}
    if not usd_per_pct:
        out["verdict"] = "learning"
        return out
    t, lo, hi = typical / usd_per_pct, low / usd_per_pct, high / usd_per_pct
    out.update({"typical_pct": round(t, 1), "low_pct": round(lo, 1), "high_pct": round(hi, 1)})
    if hi <= headroom:
        out["verdict"] = "fits"
    elif t <= headroom:
        out["verdict"] = "likely fits"
    else:
        out["verdict"] = "likely hits the limit"
        # Keep each phase to about 80% of what's left, so it finishes with room to spare.
        out["phases_needed"] = max(2, math.ceil(t / max(headroom * 0.8, 1e-9))) if headroom > 0 else None
        if steps and t > 0:
            out["stops_near_step"] = int(round((steps[0] + steps[1]) / 2 * min(1.0, headroom / t)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--typical", type=float)
    ap.add_argument("--low", type=float)
    ap.add_argument("--high", type=float)
    ap.add_argument("--steps", type=int, nargs=2)
    ap.add_argument("--pct-5h", type=float)
    ap.add_argument("--pct-week", type=float)
    ap.add_argument("--resets-5h", default="")
    ap.add_argument("--resets-week", default="")
    ap.add_argument("--calibration", action="store_true", help="Only print the learned rates.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    cal = calibration()
    if args.calibration or args.typical is None:
        print(json.dumps(cal, indent=2))
        return 0
    result = {}
    for w, label in WINDOWS:
        pct = getattr(args, "pct_" + w)
        if pct is None:
            continue
        r = predict(cal[w]["usd_per_pct"], args.typical, args.low or args.typical, args.high or args.typical,
                    pct, args.steps)
        r["label"] = label
        r["resets"] = getattr(args, "resets_" + w)
        r["calibration_runs"] = cal[w]["runs"]
        result[w] = r
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    for w, r in result.items():
        head = "%s: %s%% used, %s%% left%s" % (r["label"], r["pct_used"], r["headroom_pct"],
                                             " (resets %s)" % r["resets"] if r["resets"] else "")
        if r["verdict"] == "learning":
            print(head + ". Still learning your rate (%d of %d runs logged with usage)." % (r["calibration_runs"], MIN_RUNS))
            continue
        line = "%s. This run: typically %s%% (range %s–%s%%) -> %s" % (
            head, r["typical_pct"], r["low_pct"], r["high_pct"], r["verdict"])
        if r.get("stops_near_step"):
            line += ", probably near step %d; split into %d phases" % (r["stops_near_step"], r["phases_needed"])
        print(line + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
