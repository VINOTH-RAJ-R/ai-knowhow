Assumptions: this is `code.quick` / simple / balanced, run in Claude Code so Anthropic is the main route (OpenAI shown for reference). Python 3.10+, strict dotted-decimal (no leading zeros), non-strings return False.

## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) — one small, well-specified function; the fast tier fits at a fraction of the cost.
**Effort:** low (E2, low) — API: `output_config.effort=low` · App: in Claude Code run `/model haiku` then `/effort low`
**Est. cost per run:** <$0.01 (about $0.0006 at list price, before caching/batch)
**Cheaper:** none in the registry for this task — Haiku 5.5 @ low is already the cheapest Claude option.   **Stronger:** Claude Sonnet 5.5 @ low (about $0.012) — worth it if the validation rules become subtle or this is security-critical.
Reference (OpenAI): GPT-6 Luna @ low (`reasoning.effort=low`, about $0.0006), a tie on fit and cost.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 4 | <$0.01 | $0.60 | **recommended** |
| GPT-6 Luna | low | 4 | <$0.01 | $0.60 | tie, other vendor |
| Claude Sonnet 5.5 | low | 5 | $0.01 | $12.00 |  |
| GPT-6.1 Sol | low | 5 | $0.01 | $12.00 |  |
| Claude Opus 5.5 | low | 5 | $0.02 | $24.00 |  |
| Claude Fable 5.1 | low | 5 | $0.06 | $60.00 | overkill for one function |
| GPT-6 Astra | low | 5 | $0.06 | $60.00 | overkill for one function |
| gpt-oss-120b (open weight) | low | 3 | n/a | n/a | open weight, self-hosted; no list price |

## Your structured prompt
```xml
<context>
Small utility function for a Python codebase that needs to validate user-supplied IPv4 addresses. Strictness matters because accepting malformed addresses causes downstream bugs.
</context>
<task>Write a Python function `is_valid_ipv4(s)` that returns True if `s` is a valid dotted-decimal IPv4 address and False otherwise.</task>
<requirements>
- Python 3.10+, standard library only. Do not use the `ipaddress` module (the logic should be self-contained).
- Valid means exactly four decimal octets separated by single dots, each 0-255.
- Reject: empty octets, whitespace, signs (+/-), non-ASCII digits, hex or other bases, and leading zeros such as "01" (but "0" is valid).
- Return False (never raise) for non-string input such as None or int.
Before saying it's done, run the function against a quick set of asserts covering the valid and invalid cases above. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>All asserts pass, e.g. "192.168.1.1", "0.0.0.0", "255.255.255.255" are True; "256.1.1.1", "1.2.3", "1.2.3.4.5", "01.2.3.4", "1..2.3", " 1.2.3.4", "1.2.3.4\n", "" and None are False.</done_when>
<output_format>The function only (with a one-line docstring), then the asserts you ran, then 2 lines on the assumptions you made.</output_format>
```
Assumptions: Python 3.10+; leading zeros rejected (strict); `ipaddress` module not allowed; non-string input returns False instead of raising. Change these in the requirements if you want different behavior.

## Save tokens on this task
- Ask for the function only, not a full file or long explanation (the output format above does this).
- One task per conversation; start fresh instead of dragging history in.
- Run at low effort first and re-run only on failure at the next level up (Sonnet 5.5 @ low) instead of starting on a stronger model.

## Why this works
The `<task>` states the outcome while `<requirements>` pins down the edge cases (leading zeros, whitespace, non-strings) that make "valid IPv4" ambiguous, so the model doesn't guess. The explicit run-the-asserts line matters most at low effort, where models are likelier to skip verification. The output format keeps the answer short, which saves tokens.

Note: Haiku 5.5's card warns that at low effort it may skip a check in long agent prompts. This prompt is short and asks for the check explicitly, so that risk is small. Card verified 2026-10-17 (current).

*Running this skill on Claude Sonnet 5.5 is the recommended model for the skill itself; no frontier-model note needed.*

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
TASK: code.quick | COMPLEXITY: simple | PRIORITY: balanced
PROMPT_START
<context>
Small utility function for a Python codebase that needs to validate user-supplied IPv4 addresses. Strictness matters because accepting malformed addresses causes downstream bugs.
</context>
<task>Write a Python function `is_valid_ipv4(s)` that returns True if `s` is a valid dotted-decimal IPv4 address and False otherwise.</task>
<requirements>
- Python 3.10+, standard library only. Do not use the `ipaddress` module (the logic should be self-contained).
- Valid means exactly four decimal octets separated by single dots, each 0-255.
- Reject: empty octets, whitespace, signs (+/-), non-ASCII digits, hex or other bases, and leading zeros such as "01" (but "0" is valid).
- Return False (never raise) for non-string input such as None or int.
Before saying it's done, run the function against a quick set of asserts covering the valid and invalid cases above. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>All asserts pass, e.g. "192.168.1.1", "0.0.0.0", "255.255.255.255" are True; "256.1.1.1", "1.2.3", "1.2.3.4.5", "01.2.3.4", "1..2.3", " 1.2.3.4", "1.2.3.4\n", "" and None are False.</done_when>
<output_format>The function only (with a one-line docstring), then the asserts you ran, then 2 lines on the assumptions you made.</output_format>
PROMPT_END
