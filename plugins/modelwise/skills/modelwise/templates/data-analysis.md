# Template: data analysis (data.analysis)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| QUESTION | The business question, not "analyze this" | Ask: the most common gap |
| DATA | File(s), columns, row count, time range | Inspect the file first |
| DEFINITIONS | How metrics are defined (e.g. "active user") | Ask if ambiguous |
| TOOLS | Can the model run code (Python, SQL)? | Use code execution if available |
| OUTPUT | Numbers, chart, SQL query, written insights, dashboard | Key findings + 1-2 charts |
| DECISION | What decision this informs | Optional but sharpens the answer |

## Universal skeleton
```
QUESTION: <...> (to decide <DECISION>)
DATA: <file + columns + size + period>
DEFINITIONS: <metric definitions>
METHOD: Inspect the data first (shape, nulls, odd values) and tell me about quality issues before analyzing. Compute with code, never mental math.
OUTPUT: <top 3 findings with numbers, chart(s), caveats>
```
**How a senior analyst shapes it** (`guides/practice-content.md`):
- Define each metric in writing: numerator, denominator, time grain, time zone and exclusions.
- Check freshness, row counts against the previous period, nulls and duplicates before analysing, because a pipeline gap looks exactly like a real drop.
- Compare against a baseline, and run the check that could prove the finding wrong.
- Lead with the answer and a confidence label.

## Rendered for Claude
```xml
<data>DATA description (attach the file; don't paste 50k rows)</data>
<question>QUESTION. This informs DECISION.</question>
<definitions>DEFINITIONS</definitions>
<method>Inspect first, report data-quality issues, then compute with code. State assumptions.</method>
<output_format>OUTPUT</output_format>
```

## Rendered for OpenAI
```markdown
# Question
QUESTION (decision: DECISION)
# Data
DATA. Definitions: DEFINITIONS.
# Method
Inspect first, flag quality issues, compute with code (Python tool), state assumptions.
# Output
OUTPUT
```

## Token savers
- **Attach files and let the model run code** (Claude code execution / Files API; ChatGPT data analysis). Only the results enter the context, not every row.
- Send a 100-row sample + column descriptions to design the analysis, then run it on the full file.
