Assumptions: task = reason.hard, complexity = moderate (five well-defined problems, exact numeric answers, no production stakes), priority = balanced, provider = Anthropic because you are in Claude Code.

## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) — best in-session Claude pick for balanced cost and quality on moderate math and combinatorics. GPT-6.1 Sol ranks first overall but cannot run in Claude Code.
**Effort:** medium (E3) — API: `output_config.effort=medium` · App: Claude Code `/model sonnet`, then `/effort medium`
**Est. cost per run:** $0.09 (list price, before caching/batch)
**Cheaper:** Claude Haiku 5.5 @ medium (about $0.004) — weaker on exact counting, so the poker and tiling answers are more likely to be wrong.   **Stronger:** Claude Fable 5.1 @ medium (about $0.43) — worth it only if Sonnet's answers fail your checks.
Reference (other vendor): GPT-6.1 Sol @ medium, about $0.09.
If this is just five quick sanity-check questions: Claude Haiku 5.5 @ low, about $0.001.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 | medium | 3 | $0.0043 | $4.30 | |
| GPT-6 Luna | medium | 3 | $0.0043 | $4.30 | |
| GPT-6.1 Sol | medium | 4.5 | $0.086 | $86 | best overall, OpenAI only |
| **Claude Sonnet 5.5** | medium | 4 | $0.086 | $86 | recommended (in-session) |
| Claude Opus 5.5 | medium | 4.5 | $0.172 | $172 | |
| Claude Fable 5.1 | medium | 5 | $0.43 | $430 | |
| GPT-6 Astra | medium | 5 | $0.43 | $430 | |
| gpt-oss-120b (open weight) | medium | 3 | n/a | n/a | self-hosted, no list price |

## Your structured prompt
```xml
<context>
Five independent exact-answer math and combinatorics questions. Each has a single correct numeric answer, so accuracy matters more than explanation.
</context>

<problem>
1. In how many ways can a 2x10 board be tiled using 1x2 dominoes (either orientation) and 2x2 squares?
2. What is the sum of the digits of 2^100?
3. How many 5-card poker hands (standard 52-card deck) contain exactly one pair and nothing better (no two pair, three of a kind, straight, flush, full house, or four of a kind)?
4. What is the expected number of rolls of a fair six-sided die until every face has appeared at least once? Give a decimal.
5. How many integers from 1 to 10000 are perfect squares or perfect cubes, but not both?
</problem>

<instructions>
Work each question out carefully, then verify it with an independent method (for example a short script, a recurrence versus a closed form, or inclusion-exclusion versus direct counting). If a question is ambiguous, state the assumption you made.
</instructions>

<output_format>
Final answers only, numbered 1 to 5, one line each. For question 4, give a decimal.
</output_format>
```
Assumptions: standard 52-card deck for Q3; "exactly one pair" excludes straights and flushes (a straight or flush hand cannot have a pair anyway); the final answers-only output format was kept from your original request.

## Save tokens on this task
- Medium effort is enough; move to high only if verification shows a wrong answer, since thinking is billed as output.
- Ask for final answers only (already in the prompt), so output stays a few dozen tokens beyond thinking.
- Let the model run a quick script for Q1 to Q5 where tools are available: only results enter the context, not long hand arithmetic.

## Why this works
The tags separate the five problems from the instructions and the output format, so the model returns just numbered answers. The verify instruction makes it check each result with a second method, which catches the usual counting slips. Effort, not "think step by step", controls how much it reasons.

Tip: this skill itself runs fine on Sonnet 5.5 at low effort; you are on that already.

<!-- MACHINE -->
ROUTE_MODEL: claude-sonnet-5-5
ROUTE_EFFORT: medium
TASK: reason.hard | COMPLEXITY: moderate | PRIORITY: balanced
PROMPT_START
<context>
Five independent exact-answer math and combinatorics questions. Each has a single correct numeric answer, so accuracy matters more than explanation.
</context>

<problem>
1. In how many ways can a 2x10 board be tiled using 1x2 dominoes (either orientation) and 2x2 squares?
2. What is the sum of the digits of 2^100?
3. How many 5-card poker hands (standard 52-card deck) contain exactly one pair and nothing better (no two pair, three of a kind, straight, flush, full house, or four of a kind)?
4. What is the expected number of rolls of a fair six-sided die until every face has appeared at least once? Give a decimal.
5. How many integers from 1 to 10000 are perfect squares or perfect cubes, but not both?
</problem>

<instructions>
Work each question out carefully, then verify it with an independent method (for example a short script, a recurrence versus a closed form, or inclusion-exclusion versus direct counting). If a question is ambiguous, state the assumption you made.
</instructions>

<output_format>
Final answers only, numbered 1 to 5, one line each. For question 4, give a decimal.
</output_format>
PROMPT_END
