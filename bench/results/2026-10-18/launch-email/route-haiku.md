## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) — balanced tier, fit 4.5 for everyday writing, at a fraction of Opus cost.
**Effort:** low (E2, "low") — API: `output_config.effort="low"` · App: in Claude Code run `/model sonnet` then `/effort low`; in claude.ai pick Sonnet 5.5 and leave extended thinking off.
**Est. cost per run:** $0.04 (list price, before caching/batch).
**Cheaper:** Claude Haiku 5.5 @ low — under $0.01 per run; tone and nuance may drop a little.   **Stronger:** Claude Opus 5.5 @ low — fit 5, $0.08 per run; worth it for a high-stakes announcement.
In Claude Code, the best OpenAI reference is GPT-6.1 Sol @ low (`reasoning.effort="low"`): same fit, about the same cost.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 (`claude-haiku-5-5`) | low | 3.5 | <$0.01 | $2 | |
| GPT-6 Luna (`gpt-6-luna`) | low | 3.5 | <$0.01 | $2 | |
| **Claude Sonnet 5.5 (`claude-sonnet-5-5`)** | **low** | **4.5** | **$0.04** | **$40** | **recommended** |
| GPT-6.1 Sol (`gpt-6.1-sol`) | low | 4.5 | $0.04 | $40 | |
| Claude Opus 5.5 (`claude-opus-5-5`) | low | 5 | $0.08 | $80 | |
| Claude Fable 5.1 (`claude-fable-5-1`) | low | 5 | $0.20 | $200 | |
| GPT-6 Astra (`gpt-6-astra`) | low | 5 | $0.20 | $200 | |
| gpt-oss-120b (open weight) | low | 3 | not priced | not priced | no list price in the registry |

## Your structured prompt
```xml
<source>
[[FILL: product name; the 3 or more concrete things the expense tracking feature does; any pricing, availability or launch date; anything from our past emails or brand voice that should set the tone]]
</source>

<audience>
[[FILL: who receives this (all customers, trial users, a segment) and what they already know about the product]]
</audience>

<task>
Write a launch email announcing our new expense tracking feature. After reading, the reader should understand what it does for them and click through to try it.
</task>

<must_include>
[[FILL: at least 3 key points, each a concrete fact about the feature]]
One clear call to action linking to [[FILL: URL]].
</must_include>

<style>
Clear, plain, friendly. Confident without hype. Write for skimmers: a short subject line, a one-line opener, short paragraphs. About 150-200 words in the body. Avoid buzzwords and stacked exclamation marks. Don't invent facts, numbers, customer quotes or dates; mark anything you're unsure of as [CHECK].
</style>

<output_format>
A subject line, then the email body. Final text only, no commentary.
</output_format>
```
Assumptions: no audience, key points, date or link were given, so they are [[FILL]] placeholders; body length is 150-200 words (a launch-email norm); tone is the default clear, friendly voice.

## Save tokens on this task
- Set effort to low explicitly. Sonnet 5.5 defaults to high, and thinking is billed as output; email quality is nearly flat across effort levels.
- Put the product facts and any brand voice sample at the top in a stable block, so reruns hit the prompt cache (cached input $0.20/M vs $2/M for Sonnet 5.5).
- For a longer announcement or a sequence of emails, outline the key points first and fix the outline; rewriting a full draft costs more than fixing bullets.

If this is just a quick prototype or internal draft: Claude Haiku 5.5 @ low, under $0.01 per run.
If this is production-critical (goes to all customers): Claude Opus 5.5 @ medium, about $0.28 per run.

## Why this works
The XML tags separate what you know (source, audience) from what you want (task, must_include, style), so the model can tell which facts to use and which parts are instructions. Stating the goal and the "don't invent" rule up front keeps the email from making up numbers, and the `[[FILL]]` placeholders mark what only you can supply, since a guess there would be wrong.
