Classified as: writing (`text.write`), moderate complexity, balanced priority, Anthropic (in-session, Claude Code). Assumptions: this is a customer-facing marketing email, not a prototype or a high-stakes legal piece; the audience, product name and brand voice are unknown, so they are left as `[[FILL]]` slots.

## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) — top fit (4.5) for writing at the balanced tier; Opus-level polish isn't needed for a short email.
**Effort:** low (E2) — API: `output_config.effort=low` · App: in Claude Code run `/model sonnet` then `/effort low`; in claude.ai pick Sonnet 5.5 in the model menu and leave extended thinking off.
**Est. cost per run:** $0.04 (list price, before caching/batch)
**Cheaper:** Claude Haiku 5.5 @ low — about $0.002, fit drops to 3.5, so copy may read more generic.   **Stronger:** Claude Opus 5.5 @ low — about $0.08, worth it only for a flagship announcement where voice and polish matter most.
Reference (other vendor): GPT-6.1 Sol @ low (`reasoning.effort=low`), same fit and cost (about $0.04). It can't run in-session in Claude Code.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 | low | 3.5 | $0.002 | $2.00 | |
| GPT-6 Luna | low | 3.5 | $0.002 | $2.00 | |
| **Claude Sonnet 5.5** | **low** | **4.5** | **$0.04** | **$40.00** | **recommended** |
| GPT-6.1 Sol | low | 4.5 | $0.04 | $40.00 | |
| Claude Opus 5.5 | low | 5 | $0.08 | $80.00 | |
| Claude Fable 5.1 | low | 5 | $0.20 | $200.00 | |
| GPT-6 Astra | low | 5 | $0.20 | $200.00 | |
| gpt-oss-120b (open weight) | low | 3 | n/a | n/a | self-hosted, no list price |

## Your structured prompt
```xml
<audience>
[[FILL: who receives this, e.g. existing customers / trial users / a prospect list, and what they already know about the product]]
They are busy and skim; they care about spending less time on expenses and about getting reimbursed correctly.
</audience>

<task>
Write a launch email announcing our new expense tracking feature so that the reader understands what it does for them and clicks through to try it.
</task>

<must_include>
- What the feature does, in one plain sentence: [[FILL: product name and feature name, one-line description]]
- Three concrete benefits, each tied to something the reader does today: [[FILL: e.g. capture receipts, categorize automatically, export or approve reports]]
- One clear call to action: [[FILL: link and button text, e.g. "Try expense tracking"]]
- Availability: [[FILL: who gets it, from when, which plans or regions]]
</must_include>

<style>
Clear, plain, friendly; brand voice: [[FILL: tone words or paste a past email as a sample]]. Length: 120-180 words body, plus one subject line and one preview text under 90 characters. Avoid hype words ("revolutionary", "game-changing"), exclamation marks and filler openers. Don't invent facts, numbers or customer quotes; mark anything you're unsure of as [CHECK].
</style>

<output_format>
Three short variants labelled A, B and C that differ in angle (time saved, money visibility, simplicity). For each: subject line, preview text, body, call-to-action button text. Nothing else.
</output_format>
```
Assumptions: marketing email to existing users, plain friendly voice, 120-180 words, three variants; audience, product name, benefits, link and availability are left as `[[FILL]]` because guessing them would put wrong facts in the email.

## Save tokens on this task
- Low effort is enough: writing quality is nearly flat from low to high, so don't raise effort to "improve" an email.
- Fill the `[[FILL]]` slots before running. Missing facts lead to `[CHECK]` markers and a second round-trip.
- Ask for variants in one request (as above) rather than regenerating, and start a fresh session for the next task so history isn't resent.

## Why this works
The tagged sections separate who it's for, what to write, what must appear, and how it should sound, so Claude doesn't have to guess the audience or goal. Stating the goal (a click) and listing must-include facts keeps the copy specific, and the "don't invent facts, mark [CHECK]" line stops made-up numbers. Describing the output shape (three labelled variants with subject and preview text) gets something you can paste straight into your email tool.

<!-- MACHINE -->
ROUTE_MODEL: claude-sonnet-5-5
ROUTE_EFFORT: low
TASK: text.write | COMPLEXITY: moderate | PRIORITY: balanced
PROMPT_START
<audience>
[[FILL: who receives this, e.g. existing customers / trial users / a prospect list, and what they already know about the product]]
They are busy and skim; they care about spending less time on expenses and about getting reimbursed correctly.
</audience>

<task>
Write a launch email announcing our new expense tracking feature so that the reader understands what it does for them and clicks through to try it.
</task>

<must_include>
- What the feature does, in one plain sentence: [[FILL: product name and feature name, one-line description]]
- Three concrete benefits, each tied to something the reader does today: [[FILL: e.g. capture receipts, categorize automatically, export or approve reports]]
- One clear call to action: [[FILL: link and button text, e.g. "Try expense tracking"]]
- Availability: [[FILL: who gets it, from when, which plans or regions]]
</must_include>

<style>
Clear, plain, friendly; brand voice: [[FILL: tone words or paste a past email as a sample]]. Length: 120-180 words body, plus one subject line and one preview text under 90 characters. Avoid hype words ("revolutionary", "game-changing"), exclamation marks and filler openers. Don't invent facts, numbers or customer quotes; mark anything you're unsure of as [CHECK].
</style>

<output_format>
Three short variants labelled A, B and C that differ in angle (time saved, money visibility, simplicity). For each: subject line, preview text, body, call-to-action button text. Nothing else.
</output_format>
PROMPT_END
