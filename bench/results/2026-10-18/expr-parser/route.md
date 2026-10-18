Classification: task `code.quick` (one function), complexity moderate, priority balanced, provider Anthropic (in-session Claude Code). Assumptions: standalone Python 3, standard library only, no existing code.

## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) — one self-contained function with a clear spec; fast tier is enough and cheapest.
**Effort:** low (E2) — API: `output_config.effort=low` · App: Claude Code `/model haiku`, then `/effort low`
**Est. cost per run:** $0.0015 (list price, before caching/batch). Rounded: <$0.01
**Cheaper:** none in the registry for this task   **Stronger:** Claude Sonnet 5.5 @ low, about $0.03 — worth it if the precedence/error-handling edge cases fail the checks.
Reference (OpenAI): GPT-6 Luna @ low, about $0.0015 (ties with Haiku).
If this is production-critical: Claude Sonnet 5.5 @ medium, about $0.08.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 4 | $0.0015 | $1.50 | recommended |
| GPT-6 Luna | low | 4 | $0.0015 | $1.50 | |
| Claude Sonnet 5.5 | low | 5 | $0.03 | $30.00 | |
| GPT-6.1 Sol | low | 5 | $0.03 | $30.00 | |
| Claude Opus 5.5 | low | 5 | $0.06 | $60.00 | |
| Claude Fable 5.1 | low | 5 | $0.15 | $150.00 | |
| GPT-6 Astra | low | 5 | $0.15 | $150.00 | |
| gpt-oss-120b (open weight) | low | 3 | n/a | n/a | self-hosted, no list price |

## Your structured prompt
```xml
<context>
Standalone utility, no existing code. It will be tested against edge cases around operator precedence and error handling, so exact semantics matter more than speed.
</context>
<task>
Write a Python function evaluate(expr) that takes an arithmetic expression string and returns its numeric value without using eval or exec.
</task>
<requirements>
- Python 3, standard library only. Do not use eval, exec, compile, ast.literal_eval or similar shortcuts; write a tokenizer and a parser (for example recursive descent).
- Supported: + - * / ** , unary minus, parentheses, integers and decimals. Spaces may appear anywhere, including between a unary minus and its operand.
- Precedence follows Python: ** is right-associative and binds tighter than unary minus on its left (-2 ** 2 == -4, 2 ** -1 == 0.5, 2 ** 3 ** 2 == 512); + - * / are left-associative.
- Malformed input raises ValueError, for example '2 +', '(1', '1 2', '', '()', '1 + * 2', ')'. Reject any unexpected character.
- Division by zero raises ZeroDivisionError (not ValueError).
Before saying it's done, run a real check: write and run a small set of asserts covering the examples above plus decimals like '1.5 * 2' and '  3 -  -2 '. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>All asserts pass: valid expressions return the right values, each malformed example raises ValueError, and '1 / 0' raises ZeroDivisionError.</done_when>
<output_format>The function (with its helpers) in one code block, then 3 lines on the design and what you tested.</output_format>
```
Assumptions: Python 3 stdlib only; evaluation returns int/float as Python would; empty string and stray characters count as malformed; no existing codebase.

## Save tokens on this task
- Ask for the function only (no long explanation) and a short summary; output tokens cost 5x input.
- Start with Haiku at low effort and escalate only if your asserts fail (re-run the failures on Sonnet 5.5).
- One task per session; start fresh rather than carrying earlier history into this one.

## Why this works
The tags separate the situation, the goal, the hard rules and the finish line, so the model does not have to guess which edge cases matter. The precedence examples with exact values replace a long explanation, and the "run a real check" line matters most at low effort, where a model is tempted to skip testing. Effort is set with the parameter rather than words like "think carefully".

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
TASK: code.quick | COMPLEXITY: moderate | PRIORITY: balanced
PROMPT_START
<context>
Standalone utility, no existing code. It will be tested against edge cases around operator precedence and error handling, so exact semantics matter more than speed.
</context>
<task>
Write a Python function evaluate(expr) that takes an arithmetic expression string and returns its numeric value without using eval or exec.
</task>
<requirements>
- Python 3, standard library only. Do not use eval, exec, compile, ast.literal_eval or similar shortcuts; write a tokenizer and a parser (for example recursive descent).
- Supported: + - * / ** , unary minus, parentheses, integers and decimals. Spaces may appear anywhere, including between a unary minus and its operand.
- Precedence follows Python: ** is right-associative and binds tighter than unary minus on its left (-2 ** 2 == -4, 2 ** -1 == 0.5, 2 ** 3 ** 2 == 512); + - * / are left-associative.
- Malformed input raises ValueError, for example '2 +', '(1', '1 2', '', '()', '1 + * 2', ')'. Reject any unexpected character.
- Division by zero raises ZeroDivisionError (not ValueError).
Before saying it's done, run a real check: write and run a small set of asserts covering the examples above plus decimals like '1.5 * 2' and '  3 -  -2 '. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>All asserts pass: valid expressions return the right values, each malformed example raises ValueError, and '1 / 0' raises ZeroDivisionError.</done_when>
<output_format>The function (with its helpers) in one code block, then 3 lines on the design and what you tested.</output_format>
PROMPT_END
