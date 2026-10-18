## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic). It is the cheapest model that clears the quality bar for a short, simple email, and since you are running in Claude Code an Anthropic model is the in-session route.
**Effort:** low (E1 minimal). API: `output_config.effort=low` · Claude Code: `/model haiku`, then `/effort low`
**Est. cost per run:** <$0.01 (list price, before caching/batch)
**Cheaper:** — already the cheapest model that clears the bar (GPT-6 Luna costs the same, but it runs outside Claude Code)   **Stronger:** Claude Opus 5.5 @ low — sharper prose if this is a major launch to a large list; about $0.026 per run.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | **low** | **3.5** | **$0.0006** | **$0.65** | **recommended** |
| GPT-6 Luna | low | 3.5 | $0.0006 | $0.65 | Same fit and price, OpenAI (not runnable in Claude Code) |
| Claude Sonnet 5.5 | low | 4.5 | $0.013 | $13.00 | |
| GPT-6.1 Sol | low | 4.5 | $0.013 | $13.00 | OpenAI |
| Claude Opus 5.5 | low | 5 | $0.026 | $26.00 | |
| Claude Fable 5.1 | low | 5 | $0.065 | $65.00 | Frontier tier |
| GPT-6 Astra | low | 5 | $0.065 | $65.00 | OpenAI, frontier tier |
| gpt-oss-120b (open weight) | low | 3 | n/a | n/a | No list-price estimate |

## Your structured prompt
```xml
<context>
We are launching a new expense tracking feature in our product. The email goes to existing customers who already use the product and know the brand but not this feature. Its job is to make them understand what the feature does for them and try it.
</context>

<task>
Write one launch email announcing the new expense tracking feature. The reader should finish it understanding what the feature does for them and click the call to action to try it.
</task>

<key_points>
[[FILL: at least 3 facts about the feature: what it records or automates, what it saves the user, which plans, platforms or regions it is on, and the launch date]]
Use only facts given in this prompt, because the email goes to real customers and an invented claim cannot be taken back. Do not invent features, numbers, prices, dates, testimonials or quotes. Where a fact is missing, use a neutral placeholder such as [Product name], [Launch date] or [Price]. Mark anything uncertain with [CHECK].
</key_points>

<style>
Clear, plain, friendly and confident, written for a busy reader. Short paragraphs, no buzzwords, no hype. Open with what the feature does for the reader, not with "We are excited to announce". [[FILL: a short sample of past customer emails for voice, if available]]
</style>

<requirements>
- A subject line, a preview line under 90 characters, then the email body.
- A body of about 150 to 200 words with one call to action, linked as [CTA link].
- Sign off as [Sender name], [Company name].
- One email only. No variants and no commentary.
- Print nothing unfilled as visible instructions. Only neutral bracketed placeholders may appear in the output.
</requirements>

<output_format>
Subject: [subject line]
Preview: [preview line]

[Email body in plain text]
</output_format>
```
Assumptions: the audience is existing customers, the tone is plain and friendly, the length is about 150 to 200 words, and the deliverable is one email with subject and preview. No product name, features, date, price or link were given, so they are placeholders.

## Save tokens on this task
- Low effort is enough for a short email, since writing quality barely changes between low and high. Don't pay for medium or high thinking.
- Ask for one email, not variants. Output tokens cost 5x input tokens, so each extra variant is the expensive part.
- If you will send several launch emails from this prompt, keep the instruction block identical and put the changing facts last, so prompt caching can reuse the instructions.

## Why this works
The XML tags separate what you know (context and facts) from what you want (task and output), so the model does not mix instructions into the email copy. The "use only given facts" rule with neutral placeholders stops it from inventing prices or features. Describing the finished output (subject, preview, one email) instead of step-by-step instructions lets the model plan the email itself.

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
PROMPT_START
<context>
We are launching a new expense tracking feature in our product. The email goes to existing customers who already use the product and know the brand but not this feature. Its job is to make them understand what the feature does for them and try it.
</context>

<task>
Write one launch email announcing the new expense tracking feature. The reader should finish it understanding what the feature does for them and click the call to action to try it.
</task>

<key_points>
[[FILL: at least 3 facts about the feature: what it records or automates, what it saves the user, which plans, platforms or regions it is on, and the launch date]]
Use only facts given in this prompt, because the email goes to real customers and an invented claim cannot be taken back. Do not invent features, numbers, prices, dates, testimonials or quotes. Where a fact is missing, use a neutral placeholder such as [Product name], [Launch date] or [Price]. Mark anything uncertain with [CHECK].
</key_points>

<style>
Clear, plain, friendly and confident, written for a busy reader. Short paragraphs, no buzzwords, no hype. Open with what the feature does for the reader, not with "We are excited to announce". [[FILL: a short sample of past customer emails for voice, if available]]
</style>

<requirements>
- A subject line, a preview line under 90 characters, then the email body.
- A body of about 150 to 200 words with one call to action, linked as [CTA link].
- Sign off as [Sender name], [Company name].
- One email only. No variants and no commentary.
- Print nothing unfilled as visible instructions. Only neutral bracketed placeholders may appear in the output.
</requirements>

<output_format>
Subject: [subject line]
Preview: [preview line]

[Email body in plain text]
</output_format>
PROMPT_END
