## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) - a short summary of a single update is a fast-tier task, and Haiku clears the quality bar at the lowest cost.
**Effort:** low (E1 minimal) - API: `output_config.effort=low` · App: Claude Code `/model haiku`, then `/effort low`
**Est. cost per run:** <$0.01 (list price, before caching/batch)
**Cheaper:** none - already the cheapest model that clears the bar.   **Stronger:** claude-sonnet-5-5 @ low ($0.06) - worth it only if the summary goes to the board or needs careful judgment on what to leave out.
Same-cost reference from another vendor: GPT-6 Luna @ low (<$0.01).

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 4.5 | <$0.01 | $3.00 | **recommended** |
| GPT-6 Luna | low | 4.5 | <$0.01 | $3.00 | same fit and cost, other vendor |
| Claude Sonnet 5.5 | low | 5 | $0.06 | $60.00 | |
| GPT-6.1 Sol | low | 5 | $0.06 | $60.00 | |
| Claude Opus 5.5 | low | 5 | $0.12 | $120.00 | |
| Claude Fable 5.1 | low | 5 | $0.30 | $300.00 | |
| GPT-6 Astra | low | 5 | $0.30 | $300.00 | |
| gpt-oss-120b (open weight) | low | 3.5 | n/a | n/a | cost not covered by the registry |

## Your structured prompt
```text
<source>
Q3 update from the logistics platform team. Shipment volume grew 18% quarter over quarter to 2.4 million parcels, driven mainly by the new grocery partner in Bengaluru which alone added 310,000 parcels. On-time delivery slipped from 96.1% to 93.4%, almost entirely because of the Chennai hub, where a sorter breakdown in August caused a nine-day backlog; the sorter was replaced on September 3 and on-time delivery in Chennai has been back above 95% since mid-September. Cost per parcel fell from ₹41 to ₹37, helped by route batching, which went live in five cities. Driver attrition rose to 7% monthly from 5%, and exit interviews point to the new shift rota; HR proposes reverting to the old rota in two pilot cities in October. Customer complaints per 10,000 parcels fell from 22 to 17. The team is asking for approval of ₹2.1 crore capex for a second sorter in Chennai to avoid a single point of failure, with an expected payback of 14 months. The Pune hub launch moves from November to January because the landlord delayed handover.
</source>

<audience>
Executive team. They read fast, want the decision and business impact first, and do not need operational detail.
</audience>

<task>
Summarize the source update as exactly 5 bullets for the executive team. Bullet 1 is the decision requested: approval of the ₹2.1 crore capex for a second Chennai sorter, with its 14-month payback. The other bullets cover results, then risks and open items. Cover the on-time dip and Chennai recovery, volume and cost per parcel, driver attrition and the Pune delay; add complaints only if there is room.
</task>

<style>
Plain, direct business English. Each bullet is one sentence, two at most, with the key figure in it. Use only numbers that appear in the source, exactly as written. Do not round, estimate, or add recommendations the source does not make. No hype words.
</style>

<output_format>
Exactly 5 bullets, about 120 to 160 words in total. No heading, intro or closing line.
</output_format>
```
Assumptions: the exec team is a senior leadership audience; the figures are used exactly as written in the source; no company name is added.

## Save tokens on this task
- Low effort is enough for a summary; raising effort adds thinking tokens without a visible gain in quality.
- Paste only the source update, not the whole thread; this input is far below the 100K-token threshold where Haiku's price rises.
- For many updates at once, use the Batch API (50% off) and keep the instruction block identical across runs so it can be cached.

## Why this works
The tags separate the source from the instruction, so the model reads the material before the request. Naming the audience and the decision lets it rank facts by what executives need, instead of summarising the update in order. The exact-figure and no-new-recommendation rules stop it from drifting into invented numbers.

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
PROMPT_START
<source>
Q3 update from the logistics platform team. Shipment volume grew 18% quarter over quarter to 2.4 million parcels, driven mainly by the new grocery partner in Bengaluru which alone added 310,000 parcels. On-time delivery slipped from 96.1% to 93.4%, almost entirely because of the Chennai hub, where a sorter breakdown in August caused a nine-day backlog; the sorter was replaced on September 3 and on-time delivery in Chennai has been back above 95% since mid-September. Cost per parcel fell from ₹41 to ₹37, helped by route batching, which went live in five cities. Driver attrition rose to 7% monthly from 5%, and exit interviews point to the new shift rota; HR proposes reverting to the old rota in two pilot cities in October. Customer complaints per 10,000 parcels fell from 22 to 17. The team is asking for approval of ₹2.1 crore capex for a second sorter in Chennai to avoid a single point of failure, with an expected payback of 14 months. The Pune hub launch moves from November to January because the landlord delayed handover.
</source>

<audience>
Executive team. They read fast, want the decision and business impact first, and do not need operational detail.
</audience>

<task>
Summarize the source update as exactly 5 bullets for the executive team. Bullet 1 is the decision requested: approval of the ₹2.1 crore capex for a second Chennai sorter, with its 14-month payback. The other bullets cover results, then risks and open items. Cover the on-time dip and Chennai recovery, volume and cost per parcel, driver attrition and the Pune delay; add complaints only if there is room.
</task>

<style>
Plain, direct business English. Each bullet is one sentence, two at most, with the key figure in it. Use only numbers that appear in the source, exactly as written. Do not round, estimate, or add recommendations the source does not make. No hype words.
</style>

<output_format>
Exactly 5 bullets, about 120 to 160 words in total. No heading, intro or closing line.
</output_format>
PROMPT_END
