#!/usr/bin/env python3
"""Objective scorers for the end-to-end benchmark (standard library only).

  python3 bench/score.py --task ipv4 --answer path/to/answer.md      # score one answer
  python3 bench/score.py --run bench/results/2026-10-18                # score every answer in a run

A run folder holds <task_id>/<arm>.md answers, optional <task_id>/judge.json
({"<arm>": score_1_to_10, ...}), and meta.json with per-arm model/effort/tokens/duration.
Scores are normalized to 0-1. Model-written code runs in a subprocess with a timeout.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
TASKS = {t["id"]: t for t in json.load(open(os.path.join(HERE, "e2e", "tasks.json"), encoding="utf-8"))["tasks"]}

RUNNER = r'''
import importlib.util, json, sys
ns = {}
exec(compile(open(sys.argv[1], encoding="utf-8").read(), "answer", "exec"), ns)
spec = importlib.util.spec_from_file_location("check", sys.argv[2])
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
p, n = mod.run(ns)
print(json.dumps({"passed": p, "total": n}))
'''


def code_blocks(text, langs=("python", "py", "")):
    blocks = re.findall(r"```([a-zA-Z0-9_-]*)\n(.*?)```", text, re.S)
    return [b for lang, b in blocks if lang.lower() in langs]


def score_python(task, text):
    blocks = code_blocks(text)
    if not blocks:
        return {"score": 0.0, "detail": "no python code block"}
    # Use the last block that defines the requested function (answers often show a broken one first).
    fname = re.search(r"def (\w+)\(", task["prompt"]) or re.search(r"function (\w+)\(", task["prompt"])
    name = fname.group(1) if fname else None
    chosen = [b for b in blocks if name and ("def %s(" % name) in b] or blocks
    code = chosen[-1]
    tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"), "bench_answer_%d.py" % os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        out = subprocess.run([sys.executable, "-I", "-c", RUNNER, tmp, os.path.join(HERE, "e2e", task["check"]["file"])],
                             capture_output=True, text=True, timeout=20)
        res = json.loads(out.stdout.strip().splitlines()[-1])
        return {"score": res["passed"] / res["total"], "detail": "%d/%d tests" % (res["passed"], res["total"])}
    except Exception as e:  # noqa: BLE001
        return {"score": 0.0, "detail": "error: %s" % (str(e)[:120])}
    finally:
        os.remove(tmp)


def first_json_array(text):
    for block in code_blocks(text, ("json", "")) + [text]:
        start = block.find("[")
        while start != -1:
            depth = 0
            for i in range(start, len(block)):
                if block[i] == "[":
                    depth += 1
                elif block[i] == "]":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(block[start:i + 1])
                        except ValueError:
                            break
            start = block.find("[", start + 1)
    return None


def score_extract(task, text):
    data = first_json_array(text)
    gold = task["check"]["gold"]
    if not isinstance(data, list):
        return {"score": 0.0, "detail": "no JSON list"}
    by_id = {}
    for i, row in enumerate(data):
        if isinstance(row, dict):
            by_id[str(row.get("id", i + 1))] = row
    ok, total = 0, 0
    for g in gold:
        row = by_id.get(str(g["id"]), {})
        for k in ("invoice_no", "date", "total"):
            total += 1
            want, got = g[k], row.get(k)
            if want is None:
                ok += got in (None, "", "null")
            elif k == "total":
                try:
                    ok += abs(float(str(got).replace(",", "")) - float(want)) < 0.011
                except (TypeError, ValueError):
                    pass
            else:
                ok += str(got).strip().lower() == str(want).lower()
    return {"score": ok / total, "detail": "%d/%d fields" % (ok, total)}


def norm_num(s):
    s = s.strip().rstrip(".").replace(",", "").replace(" ", "")
    try:
        if s.endswith("%"):
            return Fraction(s[:-1]) / 100
        return Fraction(s)
    except (ValueError, ZeroDivisionError):
        return s


def score_numeric(task, text):
    gold = task["check"]["gold"]
    ok = 0
    for i, g in enumerate(gold, 1):
        m = re.search(r"(?m)^\s*(?:\*\*)?%d[.)]\s*(?:\*\*)?\s*(.+)$" % i, text)
        if not m:
            continue
        nums = re.findall(r"-?\d+(?:\.\d+)?(?:/\d+)?%?", m.group(1).replace(",", ""))
        if any(norm_num(n) == norm_num(g) for n in nums):
            ok += 1
    return {"score": ok / len(gold), "detail": "%d/%d correct" % (ok, len(gold))}


def score_keyfacts(task, text):
    low = text.lower()
    facts = task["check"]["facts"]
    hit = sum(any(alt.lower() in low for alt in group) for group in facts)
    bullets = len(re.findall(r"(?m)^\s*(?:[-*•]|\d+[.)])\s+", text))
    detail = "%d/%d facts, %d bullets" % (hit, len(facts), bullets)
    score = hit / len(facts)
    mx = task["check"].get("max_bullets")
    if mx and bullets > mx:
        score *= 0.8
        detail += " (over %d bullets: -20%%)" % mx
    return {"score": score, "detail": detail}


def score_html(task, text):
    blocks = code_blocks(text, ("html", ""))
    html = max(blocks, key=len) if blocks else text
    # Ignore HTML and CSS comments: mentions like "replace with <img>" are not real tags.
    low = re.sub(r"<!--.*?-->|/\*.*?\*/", "", html, flags=re.S).lower()
    imgs = re.findall(r"<img\s[^>]*>", low)
    inputs = re.findall(r"<(?:input|textarea|select)\b[^>]*>", low)
    checks = {
        "complete document": "<html" in low and "</html>" in low,
        "viewport meta": 'name="viewport"' in low,
        "responsive css": "@media" in low or "clamp(" in low or "auto-fit" in low,
        "img alt text": all("alt=" in i for i in imgs),
        "form labels": (not inputs) or all(("aria-label" in i) for i in inputs) or low.count("<label") >= len([i for i in inputs if 'type="submit"' not in i and 'type="hidden"' not in i]),
    }
    passed = sum(checks.values())
    return {"score": passed / len(checks), "detail": ", ".join("%s:%s" % (k, "y" if v else "n") for k, v in checks.items())}


SCORERS = {"python_tests": score_python, "extract": score_extract, "numeric": score_numeric,
           "keyfacts": score_keyfacts, "html": score_html}


def score(task_id, text, judge=None):
    task = TASKS[task_id]
    ctype = task["check"]["type"]
    parts = {}
    if ctype in SCORERS:
        parts["objective"] = SCORERS[ctype](task, text)
    if (ctype == "judge" or task["check"].get("also_judge")) and judge is not None:
        parts["judge"] = {"score": judge / 10.0, "detail": "%s/10" % judge}
    vals = [p["score"] for p in parts.values()]
    return {"score": sum(vals) / len(vals) if vals else None, "parts": parts}


def score_run(run_dir):
    meta = json.load(open(os.path.join(run_dir, "meta.json"), encoding="utf-8"))
    results = {}
    for task_dir in sorted(glob.glob(os.path.join(run_dir, "*", ""))):
        tid = os.path.basename(os.path.dirname(task_dir))
        if tid not in TASKS:
            continue
        jpath = os.path.join(task_dir, "judge.json")
        judge = json.load(open(jpath, encoding="utf-8")) if os.path.exists(jpath) else {}
        for ans in sorted(glob.glob(os.path.join(task_dir, "*.md"))):
            arm = os.path.splitext(os.path.basename(ans))[0]
            text = open(ans, encoding="utf-8").read()
            r = score(tid, text, judge.get(arm))
            r.update(meta.get(tid, {}).get(arm, {}))
            results.setdefault(tid, {})[arm] = r
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task")
    ap.add_argument("--answer")
    ap.add_argument("--judge", type=float)
    ap.add_argument("--run")
    a = ap.parse_args()
    if a.run:
        out = score_run(a.run)
        with open(os.path.join(a.run, "scores.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(json.dumps(out, indent=2))
    else:
        print(json.dumps(score(a.task, open(a.answer, encoding="utf-8").read(), a.judge), indent=2))


if __name__ == "__main__":
    main()
