## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) — one small, well-specified function is the fast tier's job, and it is the cheapest model that clears the quality bar for this task.
**Effort:** low (E2, low) — API: `output_config.effort=low` · App: in Claude Code, `/model haiku` then `/effort low`
**Est. cost per run:** <$0.01 (list price about $0.0006, before caching or batch discounts)
**Cheaper:** none — Haiku 5.5 is the lowest-cost model in the registry that meets the bar.   **Stronger:** Claude Sonnet 5.5 @ low — $0.012 per run, higher quality ceiling; worth it only if the first run fails the checks below.
Reference (not in-session): GPT-6 Luna @ low ties on fit and cost ($0.0006 per run).

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | **low** | **4** | **<$0.01** | **$0.60** | **recommended** |
| GPT-6 Luna | low | 4 | <$0.01 | $0.60 | |
| Claude Sonnet 5.5 | low | 5 | $0.012 | $12.00 | |
| GPT-6.1 Sol | low | 5 | $0.012 | $12.00 | |
| Claude Opus 5.5 | low | 5 | $0.024 | $24.00 | |
| Claude Fable 5.1 | low | 5 | $0.06 | $60.00 | |
| GPT-6 Astra | low | 5 | $0.06 | $60.00 | |
| gpt-oss-120b (open weight) | low | 3 | n/a | n/a | no list price in registry |

## Your structured prompt
```xml
<context>
Python utility for cleaning a list of contact rows before import. Each row is a dict with 'email' (string) and 'updated_at' (ISO 8601 date string). Python 3, standard library only.
</context>

<task>
Write a Python function `dedupe_by_email(rows)` that keeps only the most recent row per email and returns the kept rows sorted by email.
</task>

<requirements>
- Email matching is case-insensitive and ignores surrounding spaces: "  Ann@X.com " and "ann@x.com" are the same email.
- For each email, keep the row with the latest updated_at. Parse updated_at with datetime.fromisoformat and compare the parsed values, not the raw strings.
- Return the original row dicts, unchanged, not normalized copies. Do not mutate the input list.
- Sort the returned rows by the normalized email.
- Add type hints and a one-line docstring. No CLI, no extra features.
Before saying it's done, run a real check. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>

<done_when>
Run the function on a small sample that includes mixed-case and padded emails, a duplicate whose older row comes first, and an exact timestamp tie. Show the input and output.
</done_when>

<output_format>
The function only, in one code block, then 2 lines on the design: the tie rule (which row is kept on an exact tie) and the sort key.
</output_format>
```
Assumptions: Python 3 standard library only; no existing code to fit into; on an exact timestamp tie the first row seen is kept; the sort key is the normalized (lowercased, trimmed) email; rows with the same email are compared by parsed updated_at only.

## Save tokens on this task
- Ask for only the function, not a module, a test file or a README: output tokens cost about 5x input, so keep the reply to the function plus two lines.
- Run at low effort first; re-run one level up (medium) only if the check in `<done_when>` fails. Escalate on failure instead of starting high.
- Keep this to one task per session. A fresh chat avoids resending earlier history on every turn.

## Why this works
The XML tags separate what you know (the row shape and the rules) from what you want (one function and its output). The `<done_when>` block gives the model a concrete finish line, a sample to run, which matters most at low effort, where a model may otherwise answer without checking. Stating the rules as plain requirements, with the reason for the parsed-datetime compare, lets it generalize to edge cases you didn't list.
