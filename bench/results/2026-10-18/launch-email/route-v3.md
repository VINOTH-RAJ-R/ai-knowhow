## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) — a launch email is everyday moderate writing, and this balanced-tier model clears the bar at low effort for about $0.04 per run
**Effort:** low (E2 low) — API: `output_config.effort=low` · App: Claude Code: `/model sonnet`, then `/effort low`
**Est. cost per run:** $0.04 (list price, before caching/batch)
**Cheaper:** Claude Haiku 5.5 @ low — about $0.002; quality may drop a little on tone and polish   **Stronger:** Claude Opus 5.5 @ low — about $0.08; worth it for a major public launch where the copy needs the most polish

If this is just a quick draft: Claude Haiku 5.5 @ low, under $0.01 per run.
If this is production-critical (a major public announcement): Claude Opus 5.5 @ medium, about $0.28 per run.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 | low | 3.5 | $0.002 | $2 | Cheaper option; quality may drop a little |
| GPT-6 Luna | low | 3.5 | $0.002 | $2 | OpenAI equivalent, same cost |
| **Claude Sonnet 5.5** | **low** | **4.5** | **$0.04** | **$40** | **Recommended** |
| GPT-6.1 Sol | low | 4.5 | $0.04 | $40 | OpenAI equivalent, same cost |
| Claude Opus 5.5 | low | 5 | $0.08 | $80 | Stronger option |
| Claude Fable 5.1 | low | 5 | $0.20 | $200 | Frontier tier; more than this task needs |
| GPT-6 Astra | low | 5 | $0.20 | $200 | Frontier tier; more than this task needs |
| gpt-oss-120b | low | 3 | not estimated | not estimated | Meets the bar; cost not in the registry |

## Your structured prompt
```
<audience>Existing customers of our business software: small business owners and the finance or admin staff who handle expenses. They already use the product and have not seen this feature yet.</audience>

<task>Write a launch email announcing our new expense tracking feature, so that readers open it and log their first expense this week.</task>

<must_include>
- What the feature does: one place to record expenses and sort them into categories, so spending is easy to see.
- The benefit in plain terms: less time re-typing receipts and a clearer view of where the money goes before month-end.
- How to start: open the app, go to the expenses section, and add a first expense.
- One clear call to action: open the expenses section today.
</must_include>

<style>Confident, plain and friendly. Short sentences, written to "you". No hype words such as "game-changing", "revolutionary" or "seamless", and no fake urgency or deadlines. Use concrete, realistic wording as finished copy, with no placeholders. Keep any invented detail plausible and generic: refer to the product as "our app", and invent no product name, prices, statistics, dates or customer quotes. Length: a subject line and a body of 120 to 180 words. Sign off as "The team".</style>

<output_format>A subject line, then the email body. Final text only: one email, no variants, no notes.</output_format>
```
Assumptions: the product is business software for small teams with existing customers, the feature is already live, and no product name, date, price or link was given, so the email uses generic wording and signs off as "The team".
To improve the result, tell me: the product name and a one-sentence description of the feature; the two or three things users care about most (for example receipt capture or spending reports); the link or menu path for the call to action; a past email or sample of your brand voice.

## Save tokens on this task
- Put the facts in one short brief (product name, one benefit, the call-to-action link) instead of asking for rewrites. One email is the deliverable, so ask for no variants.
- Writing rarely needs more than low effort. Stay at low and raise it only if the first draft misses the tone.
- If you will send many launch emails, keep your brand voice sample in a stable system prompt so prompt caching bills it at about a tenth of the normal input price.

## Why this works
The structure separates who the email is for, the one goal it serves and the facts it must contain from the style rules, so the model writes the single email you need instead of guessing at the brief. The "leave out what is missing" rule keeps invented facts out of customer-facing copy, which is the main risk when the brief is thin.

<!-- MACHINE -->
ROUTE_MODEL: claude-sonnet-5-5
ROUTE_EFFORT: low
PROMPT_START
<audience>Existing customers of our business software: small business owners and the finance or admin staff who handle expenses. They already use the product and have not seen this feature yet.</audience>

<task>Write a launch email announcing our new expense tracking feature, so that readers open it and log their first expense this week.</task>

<must_include>
- What the feature does: one place to record expenses and sort them into categories, so spending is easy to see.
- The benefit in plain terms: less time re-typing receipts and a clearer view of where the money goes before month-end.
- How to start: open the app, go to the expenses section, and add a first expense.
- One clear call to action: open the expenses section today.
</must_include>

<style>Confident, plain and friendly. Short sentences, written to "you". No hype words such as "game-changing", "revolutionary" or "seamless", and no fake urgency or deadlines. Use concrete, realistic wording as finished copy, with no placeholders. Keep any invented detail plausible and generic: refer to the product as "our app", and invent no product name, prices, statistics, dates or customer quotes. Length: a subject line and a body of 120 to 180 words. Sign off as "The team".</style>

<output_format>A subject line, then the email body. Final text only: one email, no variants, no notes.</output_format>
PROMPT_END
