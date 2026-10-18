## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) - summarizing one short update into 5 bullets is a light text transform; Haiku fits it (fit 4.5) at the lowest cost.
**Effort:** low (E1 minimal) - API: `output_config.effort=low` - App: in Claude Code run `/model haiku` then `/effort low`.
**Est. cost per run:** <$0.01 (about $0.003; list price, before caching/batch)
**Cheaper:** none in the registry for this task at this quality bar (GPT-6 Luna @ low ties at about $0.003).   **Stronger:** Claude Sonnet 5.5 @ low (about $0.06) - worth it only if the exec readout is going straight to leadership with no review.
Reference (other vendor): GPT-6 Luna @ low, about $0.003, same fit.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 4.5 | $0.003 | $3.00 | **recommended** |
| GPT-6 Luna | low | 4.5 | $0.003 | $3.00 | tie, other vendor |
| Claude Sonnet 5.5 | low | 5 | $0.06 | $60.00 | |
| GPT-6.1 Sol | low | 5 | $0.06 | $60.00 | |
| Claude Opus 5.5 | low | 5 | $0.12 | $120.00 | |
| Claude Fable 5.1 | low | 5 | $0.30 | $300.00 | |
| GPT-6 Astra | low | 5 | $0.30 | $300.00 | |
| gpt-oss-120b (open weight) | low | 3.5 | n/a | n/a | self-hosted, no list price |

## Your structured prompt
```xml
<source>
Q3 update from the logistics platform team. Shipment volume grew 18% quarter over quarter to 2.4 million parcels, driven mainly by the new grocery partner in Bengaluru which alone added 310,000 parcels. On-time delivery slipped from 96.1% to 93.4%, almost entirely because of the Chennai hub, where a sorter breakdown in August caused a nine-day backlog; the sorter was replaced on September 3 and on-time delivery in Chennai has been back above 95% since mid-September. Cost per parcel fell from ₹41 to ₹37, helped by route batching, which went live in five cities. Driver attrition rose to 7% monthly from 5%, and exit interviews point to the new shift rota; HR proposes reverting to the old rota in two pilot cities in October. Customer complaints per 10,000 parcels fell from 22 to 17. The team is asking for approval of ₹2.1 crore capex for a second sorter in Chennai to avoid a single point of failure, with an expected payback of 14 months. The Pune hub launch moves from November to January because the landlord delayed handover.
</source>

<audience>
The executive team. They are time-poor, know the business, and have not seen this update. They care about performance against the prior quarter, risks, and what is being asked of them.
</audience>

<task>
Summarize the Q3 update above in exactly 5 bullets so the exec team can grasp the quarter in under a minute and see the decision they are being asked to make.
</task>

<must_include>
- Volume growth (18% QoQ to 2.4M parcels) and its main driver
- On-time delivery decline (96.1% to 93.4%), its cause, and the current recovery status
- Cost per parcel and complaints improvement (the before and after figures)
- Driver attrition rise and the proposed response
- The approval being requested (capex, payback) and the Pune launch delay
</must_include>

<style>
Plain, direct business English. One bullet is one or two short sentences, leading with the headline number or fact. Keep every figure exactly as given in the source. Don't invent facts, numbers or causes; mark anything you're unsure of as [CHECK]. Put the capex approval request last so it stands out as the action item.
</style>

<output_format>
Exactly 5 bullets, final text only, no preamble.
</output_format>
```
Assumptions: classified as text.transform, moderate, balanced priority; audience is the exec team; the 7 topics in the source are merged into 5 bullets with the capex ask last; all figures kept verbatim; the user's original instruction text ("summarize this for our exec team in 5 bullets") is carried into the task and output format.

## Save tokens on this task
- Low effort is enough: summaries need no deep reasoning, and Haiku at low is the cheapest tier that clears the bar.
- The source is short (under 1K tokens), so no chunking is needed; if you run this weekly, put the fixed audience and style parts in a system prompt so caching applies.
- For many updates, use the Batch API (50% off) instead of one call per update.

## Why this works
The source goes first inside its own tag so the model treats it as material, not instructions, and the task comes after it. Naming the audience and the must-include facts tells the model what to keep when it has to cut from 7 topics to 5. The style and output sections pin the format (exactly 5 bullets, figures verbatim, [CHECK] for doubts), which prevents invented numbers.

Note: Haiku 5.5 may skip a check at low effort in long agent prompts; that does not apply to this short single-step task. Registry cards verified 2026-10-17 (current).

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
TASK: text.transform | COMPLEXITY: moderate | PRIORITY: balanced
PROMPT_START
<source>
Q3 update from the logistics platform team. Shipment volume grew 18% quarter over quarter to 2.4 million parcels, driven mainly by the new grocery partner in Bengaluru which alone added 310,000 parcels. On-time delivery slipped from 96.1% to 93.4%, almost entirely because of the Chennai hub, where a sorter breakdown in August caused a nine-day backlog; the sorter was replaced on September 3 and on-time delivery in Chennai has been back above 95% since mid-September. Cost per parcel fell from ₹41 to ₹37, helped by route batching, which went live in five cities. Driver attrition rose to 7% monthly from 5%, and exit interviews point to the new shift rota; HR proposes reverting to the old rota in two pilot cities in October. Customer complaints per 10,000 parcels fell from 22 to 17. The team is asking for approval of ₹2.1 crore capex for a second sorter in Chennai to avoid a single point of failure, with an expected payback of 14 months. The Pune hub launch moves from November to January because the landlord delayed handover.
</source>

<audience>
The executive team. They are time-poor, know the business, and have not seen this update. They care about performance against the prior quarter, risks, and what is being asked of them.
</audience>

<task>
Summarize the Q3 update above in exactly 5 bullets so the exec team can grasp the quarter in under a minute and see the decision they are being asked to make.
</task>

<must_include>
- Volume growth (18% QoQ to 2.4M parcels) and its main driver
- On-time delivery decline (96.1% to 93.4%), its cause, and the current recovery status
- Cost per parcel and complaints improvement (the before and after figures)
- Driver attrition rise and the proposed response
- The approval being requested (capex, payback) and the Pune launch delay
</must_include>

<style>
Plain, direct business English. One bullet is one or two short sentences, leading with the headline number or fact. Keep every figure exactly as given in the source. Don't invent facts, numbers or causes; mark anything you're unsure of as [CHECK]. Put the capex approval request last so it stands out as the action item.
</style>

<output_format>
Exactly 5 bullets, final text only, no preamble.
</output_format>
PROMPT_END
