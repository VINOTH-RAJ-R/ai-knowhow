## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, anthropic) — a single 5-line function with a clear spec is a simple debugging task, and the cheapest model that clears the quality bar handles it.
**Effort:** low (E2) — API: `output_config.effort=low` · App: in Claude Code run `/model haiku` then `/effort low`
**Est. cost per run:** <$0.01 (about $0.0014, list price, before caching/batch)
**Cheaper:** none in the registry for this task — Haiku 5.5 @ low is already the floor.   **Stronger:** Claude Opus 5.5 @ low (~$0.054) — only if Haiku's fix fails the tests.
Reference (other vendor): GPT-6 Luna @ low (~$0.0014), same fit and cost. You are in Claude Code, so the in-session pick is the Claude one above.
If you want extra margin (borderline moderate): Claude Sonnet 5.5 @ medium (~$0.14), the model you are likely running now.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 3 | $0.0014 | $1.35 | **recommended** |
| GPT-6 Luna | low | 3 | $0.0014 | $1.35 | other vendor, same fit |
| Claude Sonnet 5.5 | low | 4.5 | $0.027 | $27.00 | |
| GPT-6.1 Sol | low | 4.5 | $0.027 | $27.00 | |
| Claude Opus 5.5 | low | 5 | $0.054 | $54.00 | |
| Claude Fable 5.1 | low | 5 | $0.135 | $135.00 | |
| GPT-6 Astra | low | 5 | $0.135 | $135.00 | |
| gpt-oss-120b (open weight) | low | 2.5 | n/a | n/a | open weight, no list price |

## Your structured prompt
```xml
<evidence>
Symptom: the first value is wrong and calling the function twice gives odd output.
</evidence>

<input>
def moving_average(values, window, out=[]):
    for i in range(len(values)):
        start = max(0, i - window)
        chunk = values[start:i]
        out.append(sum(chunk) / len(chunk))
    return out
</input>

<context>
Plain Python function. Intended behavior: for each position i, return the average of the last `window` values up to and including i (fewer values at the start). No other files or recent changes are involved.
</context>

<task>
The function returns wrong results. Find the root cause of each problem first: form a hypothesis, confirm it by running the function on a small example, then fix it.
</task>

<requirements>
- Make the smallest change that fixes the causes, not the symptoms. Keep the function name and the (values, window) call signature.
- Add a few regression tests (empty list, window larger than the list, window of 1, calling it twice returns the same result) and run them. Show that they pass before reporting.
</requirements>

<output_format>
Root causes (2-3 sentences) -> the fixed function -> test output.
</output_format>
```
Assumptions: complexity simple, priority balanced, provider Claude (in-session). Fix scope is the function plus regression tests, no other files. Behavior follows your spec: window values ending at and including i, fewer at the start.

## Save tokens on this task
- The code is pasted in full and short, so no extra context is needed. Let the agent run the repro itself instead of pasting outputs back and forth.
- Start at low effort; raise to medium (or switch to Sonnet 5.5) only if the first fix fails the tests.
- Ask for the root cause, the fixed function and the test output only, not a rewritten file or a long walkthrough.

## Why this works
The tags separate the symptom, the code and the intended behavior, so the model cannot confuse "what is wrong" with "what is right". Asking for the root cause first (and a run on a small example) stops it patching one symptom, since this function has several causes: a mutable default argument shared across calls, a slice that excludes position i and is empty at i=0, and a window off-by-one. The tests and the output format define "done", which matters most at low effort.

(Registry cards verified 2026-10-17, within 90 days.)

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
TASK: code.debug | COMPLEXITY: simple | PRIORITY: balanced
PROMPT_START
<evidence>
Symptom: the first value is wrong and calling the function twice gives odd output.
</evidence>

<input>
def moving_average(values, window, out=[]):
    for i in range(len(values)):
        start = max(0, i - window)
        chunk = values[start:i]
        out.append(sum(chunk) / len(chunk))
    return out
</input>

<context>
Plain Python function. Intended behavior: for each position i, return the average of the last `window` values up to and including i (fewer values at the start). No other files or recent changes are involved.
</context>

<task>
The function returns wrong results. Find the root cause of each problem first: form a hypothesis, confirm it by running the function on a small example, then fix it.
</task>

<requirements>
- Make the smallest change that fixes the causes, not the symptoms. Keep the function name and the (values, window) call signature.
- Add a few regression tests (empty list, window larger than the list, window of 1, calling it twice returns the same result) and run them. Show that they pass before reporting.
</requirements>

<output_format>
Root causes (2-3 sentences) -> the fixed function -> test output.
</output_format>
PROMPT_END
