# Template: extraction & classification (data.extract)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| INPUT_KIND | Emails, invoices, reviews, tickets, rows… | (required) |
| FIELDS | Exact fields/labels with types and allowed values | Ask: this is the schema |
| RULES | Edge cases: missing values, multiple matches, ambiguity | Missing → null; ambiguous → "unknown" |
| EXAMPLES | 2-5 labelled examples, including a tricky one | Strongly recommended |
| VOLUME | How many items | Ask: decides batch vs real-time |

## Universal skeleton
```
TASK: For each <INPUT_KIND>, extract/classify into the schema below.
SCHEMA: <JSON schema or field list with types and enums>
RULES: <edge cases>
EXAMPLES: <input → output pairs>
INPUT: <one item or a batch with ids>
OUTPUT: JSON only, matching the schema.
```

## Rendered for Claude
Use **structured outputs** (`output_config.format` with a JSON schema) so output is guaranteed valid. Prompt:
```xml
<instructions>Classify each support ticket. Follow the rules exactly.</instructions>
<rules>RULES</rules>
<examples>
<example><input>…</input><output>{…}</output></example>
</examples>
<ticket id="123">…</ticket>
```

## Rendered for OpenAI
Use **Structured Outputs** (`text.format` with `type: json_schema`, `strict: true` in the Responses API). Prompt:
```markdown
# Task
Classify each ticket per the rules.
# Rules
RULES
# Examples
EXAMPLES
# Input
<ticket id="123">…</ticket>
```

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "sort these 10,000 customer reviews into categories"
**Structured:** schema `{id, sentiment: positive|neutral|negative, topic: delivery|quality|price|support|other, urgent: boolean}`, rule "urgent = mentions refund, legal, or safety", 4 examples incl. a sarcastic one; run through the **Batch API** on the fastest tier.

## Token savers (this task type is where savings are largest)
- **Fastest tier + lowest effort.** Extraction rarely benefits from deep reasoning.
- **Batch API** for anything not needed in real time: 50% off on both Anthropic and OpenAI.
- **Cache the instructions + examples** (put them first and keep them identical); only the item changes.
- Several short items per request (with ids) amortize the instructions.
- Validate a 50-item sample at two effort levels before running 10,000.
