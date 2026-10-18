## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) - fit 5/5 for extraction, the cheapest current model, and it runs in Claude Code. Six short snippets with a few format traps is well within its range.
**Effort:** low (E1 minimal) - API: `output_config.effort=low` - App: in Claude Code run `/model haiku` then `/effort low`.
**Est. cost per run:** <$0.01 (about $0.0005, list price, before caching/batch)
**Cheaper:** none in the registry (Haiku 5.5 is the cheapest current Claude; GPT-6 Luna @ low is the same price) - **Stronger:** Claude Sonnet 5.5 @ low (~$0.01) - only worth it if Haiku gets one of the tricky rows (3, 4, 6) wrong in a spot check.
Reference line (other vendor): GPT-6 Luna @ `reasoning.effort=low`, ~$0.0005, tied on fit.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 5 | $0.0005 | $0.50 | **recommended** |
| GPT-6 Luna | low | 5 | $0.0005 | $0.50 | tie, other vendor |
| Claude Sonnet 5.5 | low | 5 | $0.01 | $10.00 | |
| GPT-6.1 Sol | low | 5 | $0.01 | $10.00 | |
| Claude Opus 5.5 | low | 5 | $0.02 | $20.00 | |
| Claude Fable 5.1 | low | 5 | $0.05 | $50.00 | |
| GPT-6 Astra | low | 5 | $0.05 | $50.00 | |
| gpt-oss-120b (open weight) | low | 3.5 | n/a | n/a | self-hosted, no list price |

## Your structured prompt
```xml
<context>
Six short invoice-like text snippets, each with an id. Downstream code will load the result as JSON, so every value must be in a fixed format even though the snippets use different layouts, languages of formatting and currencies.
</context>

<task>
For each snippet, extract the invoice number, the invoice date and the total amount, and return them as a JSON list with one object per snippet.
</task>

<requirements>
- Keys, in this order: id, invoice_no, date, total.
- id: the snippet's number, as an integer.
- invoice_no: the identifier as a string, without a label such as "Inv", "INVOICE NO." or "#". Keep letters, digits, dashes and slashes exactly as written. If the snippet has no invoice or reference number, use null.
- date: the invoice date (issue date) in YYYY-MM-DD. If a snippet also gives a payment date, order date or other date, use only the date that belongs to the invoice itself, unless the snippet gives no invoice date, in which case use the order date. If a snippet states its own date format, follow it when reading the date. If there is no date, use null.
- total: a JSON number only (no currency symbol, no thousands separators, dot as decimal separator). Use the final amount due or charged, after tax, not a subtotal. Convert European formats such as 3.400,50 to 3400.50. If there is no total, use null.
- Do not guess. Use null only when the information is absent from the snippet.
- Return the JSON list and nothing else.
</requirements>

<input>
<snippet id="1">Inv #A-1043 dated 3 March 2026. Amount due: $1,250.00</snippet>
<snippet id="2">INVOICE NO. 88231 // 2026-01-17 // TOTAL USD 99.90 (incl. tax)</snippet>
<snippet id="3">Bill ref: KX/22/7 issued on 07/04/2026 (DD/MM/YYYY). Grand total: EUR 3.400,50</snippet>
<snippet id="4">Thanks for your order! Total charged $45. Order date Feb 2, 2026.</snippet>
<snippet id="5">Invoice 5521-B, date: 12-Dec-2025, subtotal 200.00, tax 36.00, total 236.00</snippet>
<snippet id="6">Re: invoice INV-0091 — paid in full ($780.25) on 2026/05/30, invoice date 2026/05/01</snippet>
</input>

<output_format>
A JSON list only, shaped like this (placeholder values):
[{"id": 1, "invoice_no": "...", "date": "YYYY-MM-DD", "total": 0.00}]
</output_format>
```
Assumptions: complexity is moderate (small batch, but mixed date and number formats and a few traps); priority is balanced; provider is Anthropic because you are in Claude Code; "total" means the final after-tax amount due or charged; for snippet 4 (no invoice number) the order date stands in for the invoice date; no volume given, so this is a one-off run (for structured-output guarantees via the API, pass the schema through `output_config.format`).

## Save tokens on this task
- Stay on the fast tier at low effort; extraction rarely benefits from deeper thinking. Raise effort or move to Sonnet 5.5 only for rows that fail a spot check.
- If you later run this on thousands of snippets, put the instructions and rules first (identical every time) so they are cached, send many snippets per request with ids, and use the Batch API for 50% off.
- Use structured outputs (a JSON schema) through the API instead of asking for "JSON only" in prose, to avoid retries on malformed output.

## Why this works
The tags separate what the data is, what to do, the exact formatting rules and the input, so the model does not mix instructions with snippets. Spelling out the edge cases (which date wins, how to read 3.400,50, what counts as missing) removes the guesses that otherwise cause inconsistent output across rows. Giving a one-line output shape is the most reliable way to get machine-readable output.

<!-- MACHINE -->
ROUTE_MODEL: claude-haiku-5-5
ROUTE_EFFORT: low
TASK: data.extract | COMPLEXITY: moderate | PRIORITY: balanced
PROMPT_START
<context>
Six short invoice-like text snippets, each with an id. Downstream code will load the result as JSON, so every value must be in a fixed format even though the snippets use different layouts, languages of formatting and currencies.
</context>

<task>
For each snippet, extract the invoice number, the invoice date and the total amount, and return them as a JSON list with one object per snippet.
</task>

<requirements>
- Keys, in this order: id, invoice_no, date, total.
- id: the snippet's number, as an integer.
- invoice_no: the identifier as a string, without a label such as "Inv", "INVOICE NO." or "#". Keep letters, digits, dashes and slashes exactly as written. If the snippet has no invoice or reference number, use null.
- date: the invoice date (issue date) in YYYY-MM-DD. If a snippet also gives a payment date, order date or other date, use only the date that belongs to the invoice itself, unless the snippet gives no invoice date, in which case use the order date. If a snippet states its own date format, follow it when reading the date. If there is no date, use null.
- total: a JSON number only (no currency symbol, no thousands separators, dot as decimal separator). Use the final amount due or charged, after tax, not a subtotal. Convert European formats such as 3.400,50 to 3400.50. If there is no total, use null.
- Do not guess. Use null only when the information is absent from the snippet.
- Return the JSON list and nothing else.
</requirements>

<input>
<snippet id="1">Inv #A-1043 dated 3 March 2026. Amount due: $1,250.00</snippet>
<snippet id="2">INVOICE NO. 88231 // 2026-01-17 // TOTAL USD 99.90 (incl. tax)</snippet>
<snippet id="3">Bill ref: KX/22/7 issued on 07/04/2026 (DD/MM/YYYY). Grand total: EUR 3.400,50</snippet>
<snippet id="4">Thanks for your order! Total charged $45. Order date Feb 2, 2026.</snippet>
<snippet id="5">Invoice 5521-B, date: 12-Dec-2025, subtotal 200.00, tax 36.00, total 236.00</snippet>
<snippet id="6">Re: invoice INV-0091 — paid in full ($780.25) on 2026/05/30, invoice date 2026/05/01</snippet>
</input>

<output_format>
A JSON list only, shaped like this (placeholder values):
[{"id": 1, "invoice_no": "...", "date": "YYYY-MM-DD", "total": 0.00}]
</output_format>
PROMPT_END
