## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) — the cheapest current Claude model that clears the bar for a five-bullet summary of one paragraph.
**Effort:** low (E0 "none": Claude has no true off, so low is the floor) · API: `output_config.effort=low` · App: in Claude Code run `/model claude-haiku-5-5`, then `/effort low` (or use the arrows in the /model picker)
**Est. cost per run:** <$0.01 (list price, before caching/batch)
**Cheaper:** already the cheapest Claude model that clears the bar — GPT-6 Luna ties on price (`gpt-6-luna` @ none, same ~$0.0006 per run) if you move to OpenAI.   **Stronger:** Claude Sonnet 5.5 @ low (~$0.012 per run) — worth it only if this goes to the exec team unedited for a funding decision.

If this is production-critical (it feeds a ₹2.1 crore approval): Claude Sonnet 5.5 @ low, about $0.012 per run.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** (`claude-haiku-5-5`) | low | 4.5 | **<$0.01** | **$0.60** | **recommended** |
| GPT-6 Luna (`gpt-6-luna`) | none | 4.5 | <$0.01 | $0.60 | |
| Claude Sonnet 5.5 (`claude-sonnet-5-5`) | low | 5 | $0.012 | $12.00 | |
| GPT-6.1 Sol (`gpt-6.1-sol`) | low | 5 | $0.012 | $12.00 | |
| Claude Opus 5.5 (`claude-opus-5-5`) | low | 5 | $0.024 | $24.00 | |
| Claude Fable 5.1 (`claude-fable-5-1`) | low | 5 | $0.06 | $60.00 | |
| GPT-6 Astra (`gpt-6-astra`) | low | 5 | $0.06 | $60.00 | |
| gpt-oss-120b (open weight) | low | 3.5 | not priced in registry | not priced in registry | meets bar; no list price |

## Your structured prompt
```
<source>
Q3 update from the logistics platform team. Shipment volume grew 18% quarter over quarter to 2.4 million parcels, driven mainly by the new grocery partner in Bengaluru which alone added 310,000 parcels. On-time delivery slipped from 96.1% to 93.4%, almost entirely because of the Chennai hub, where a sorter breakdown in August caused a nine-day backlog; the sorter was replaced on September 3 and on-time delivery in Chennai has been back above 95% since mid-September. Cost per parcel fell from ₹41 to ₹37, helped by route batching, which went live in five cities. Driver attrition rose to 7% monthly from 5%, and exit interviews point to the new shift rota; HR proposes reverting to the old rota in two pilot cities in October. Customer complaints per 10,000 parcels fell from 22 to 17. The team is asking for approval of ₹2.1 crore capex for a second sorter in Chennai to avoid a single point of failure, with an expected payback of 14 months. The Pune hub launch moves from November to January because the landlord delayed handover.
</source>

<context>
The source is a Q3 operations update from a logistics platform team. The reader is the executive team, who need the status, the risks, and the decision being asked of them.
</context>

<task>
Summarize the update in the source as exactly 5 bullets for the executive team. Lead with the decision requested, then the results, then the risks.
</task>

<requirements>
- Exactly 5 bullets, in this order: (1) the capex request for a second Chennai sorter, (2) volume growth and cost per parcel, (3) on-time delivery and customer complaints, (4) driver attrition and the proposed rota change, (5) the Pune hub delay.
- One sentence per bullet, about 30 words or fewer.
- Use only facts, figures and dates stated in the source. Do not add causes, forecasts or recommendations. Keep the source's hedges (for example "point to").
- Keep numbers, currency and units exactly as written (₹, crore, %, parcels).
- Plain, direct language. No hype.
- If something in the source is unclear, add [CHECK] at the end of that bullet.
</requirements>

<output_format>
Final text only: five bullets, each starting with "- ". No heading, no introduction, no notes.
</output_format>
```
Assumptions: the audience is the executive team and the capex request leads, following the template's decision-first rule; five one-sentence bullets; no figures beyond the source; no slots left unfilled, so no placeholders are needed.

## Save tokens on this task
- Ask for the exact output shape ("five bullets, nothing else"). Output tokens cost about five times input, so a fixed shape keeps the bill down.
- Keep effort at low. Summaries gain nothing from extra thinking, and thinking is billed as output.
- If you summarize many team updates in one run, use the Batch API for 50% off.
- Keep inputs under 100K tokens: Haiku 5.5's price rises five times above that.

## Why this works
The source comes first and the instruction last, so the model reads the material before the task. Naming the lead (the capex decision), the bullet count, the order and the sentence length turns a vague "summarize" into an output you can check at a glance. The "only facts in the source" rule is what stops an exec summary from inventing numbers.

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
PROMPT_START
<source>
Q3 update from the logistics platform team. Shipment volume grew 18% quarter over quarter to 2.4 million parcels, driven mainly by the new grocery partner in Bengaluru which alone added 310,000 parcels. On-time delivery slipped from 96.1% to 93.4%, almost entirely because of the Chennai hub, where a sorter breakdown in August caused a nine-day backlog; the sorter was replaced on September 3 and on-time delivery in Chennai has been back above 95% since mid-September. Cost per parcel fell from ₹41 to ₹37, helped by route batching, which went live in five cities. Driver attrition rose to 7% monthly from 5%, and exit interviews point to the new shift rota; HR proposes reverting to the old rota in two pilot cities in October. Customer complaints per 10,000 parcels fell from 22 to 17. The team is asking for approval of ₹2.1 crore capex for a second sorter in Chennai to avoid a single point of failure, with an expected payback of 14 months. The Pune hub launch moves from November to January because the landlord delayed handover.
</source>

<context>
The source is a Q3 operations update from a logistics platform team. The reader is the executive team, who need the status, the risks, and the decision being asked of them.
</context>

<task>
Summarize the update in the source as exactly 5 bullets for the executive team. Lead with the decision requested, then the results, then the risks.
</task>

<requirements>
- Exactly 5 bullets, in this order: (1) the capex request for a second Chennai sorter, (2) volume growth and cost per parcel, (3) on-time delivery and customer complaints, (4) driver attrition and the proposed rota change, (5) the Pune hub delay.
- One sentence per bullet, about 30 words or fewer.
- Use only facts, figures and dates stated in the source. Do not add causes, forecasts or recommendations. Keep the source's hedges (for example "point to").
- Keep numbers, currency and units exactly as written (₹, crore, %, parcels).
- Plain, direct language. No hype.
- If something in the source is unclear, add [CHECK] at the end of that bullet.
</requirements>

<output_format>
Final text only: five bullets, each starting with "- ". No heading, no introduction, no notes.
</output_format>
PROMPT_END
