## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) — a single small function is squarely in the fast tier's range (fit 4), at a fraction of Sonnet's price.
**Effort:** low (E2) — API: `output_config.effort=low` · App: in Claude Code run `/model haiku` then `/effort low`
**Est. cost per run:** <$0.01 (about $0.0006, list price, before caching/batch)
**Cheaper:** none in the registry for Claude; GPT-6 Luna @ low costs the same ($0.0006) — no saving.   **Stronger:** Claude Sonnet 5.5 @ low (~$0.01) — worth it if this feeds production data or you want the higher quality ceiling (fit 5).
Claude Code can only run Claude models in-session, so Haiku 5.5 is the in-session pick. Best OpenAI reference: GPT-6 Luna @ low (tie, same cost).

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 4 | **$0.0006** | **$0.60** | **recommended** |
| GPT-6 Luna | low | 4 | $0.0006 | $0.60 | tie, OpenAI |
| Claude Sonnet 5.5 | low | 5 | $0.012 | $12.00 | |
| GPT-6.1 Sol | low | 5 | $0.012 | $12.00 | |
| Claude Opus 5.5 | low | 5 | $0.024 | $24.00 | |
| Claude Fable 5.1 | low | 5 | $0.06 | $60.00 | |
| GPT-6 Astra | low | 5 | $0.06 | $60.00 | |
| gpt-oss-120b (open weight) | low | 3 | n/a | n/a | self-hosted, no list price |

## Your structured prompt
```xml
<context>
A small utility used to clean a list of records. Each row is a dict with an 'email' string and an 'updated_at' ISO date string.
</context>
<task>Write a Python function `dedupe_by_email(rows)` that keeps only the most recent row per email and returns the kept rows sorted by email.</task>
<requirements>
- Python 3, standard library only.
- Emails match case-insensitively and ignore surrounding whitespace, so " A@x.com" and "a@x.com " are the same email.
- "Most recent" is decided by parsing `updated_at` as an ISO date (not by comparing raw strings). If two rows for one email have the same `updated_at`, keep the later one in the input list.
- Return the original row dicts unchanged, do not mutate the input list, and sort the result by the normalized (stripped, lowercased) email.
- Empty input returns an empty list.
Before saying it's done, run a real check: write a few asserts covering mixed case, surrounding spaces, differing dates, a date tie, and empty input, and run them. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>The asserts pass and the function matches every rule above.</done_when>
<output_format>Only the function (plus the asserts in a separate block), then a 2-line summary.</output_format>
```
Assumptions: Python 3 with standard library only; ties on `updated_at` keep the later input row; input is not mutated; rows are returned unchanged (original email casing kept); every row has a parseable `updated_at` and a string `email` (malformed rows are out of scope, add a rule if you need them skipped or rejected). Treated as simple/balanced.

## Save tokens on this task
- Keep it to one function and ask for the function only, not a full file or long explanation; output tokens cost 5x input.
- Haiku 5.5 at low is already the cheap tier; escalate to Sonnet 5.5 only if the asserts fail, rather than starting higher.
- One task per session so no earlier history is resent.

## Why this works
The tags separate context, the outcome and the hard rules, so the model does not have to guess which part is a constraint. Spelling out the ambiguous cases (case and spaces, date parsing, ties, sort key) removes the decisions a quick prompt would leave to chance. The explicit "run a real check" step matters most at low effort, where the model is otherwise tempted to stop after writing the code.
<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
TASK: code.quick | COMPLEXITY: simple | PRIORITY: balanced
PROMPT_START
<context>
A small utility used to clean a list of records. Each row is a dict with an 'email' string and an 'updated_at' ISO date string.
</context>
<task>Write a Python function `dedupe_by_email(rows)` that keeps only the most recent row per email and returns the kept rows sorted by email.</task>
<requirements>
- Python 3, standard library only.
- Emails match case-insensitively and ignore surrounding whitespace, so " A@x.com" and "a@x.com " are the same email.
- "Most recent" is decided by parsing `updated_at` as an ISO date (not by comparing raw strings). If two rows for one email have the same `updated_at`, keep the later one in the input list.
- Return the original row dicts unchanged, do not mutate the input list, and sort the result by the normalized (stripped, lowercased) email.
- Empty input returns an empty list.
Before saying it's done, run a real check: write a few asserts covering mixed case, surrounding spaces, differing dates, a date tie, and empty input, and run them. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>The asserts pass and the function matches every rule above.</done_when>
<output_format>Only the function (plus the asserts in a separate block), then a 2-line summary.</output_format>
PROMPT_END
