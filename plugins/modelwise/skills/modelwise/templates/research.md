# Template: research & synthesis (research.deep)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| QUESTION | Specific research question(s) | (required) |
| PURPOSE | Decision or deliverable it feeds | Ask |
| SCOPE | Regions, time window, industries, what's out of scope | Last 2 years, global |
| SOURCES | Preferred/forbidden sources; provided documents | Primary sources first; cite everything |
| DEPTH | Quick scan vs exhaustive | Medium: 8-15 good sources |
| OUTPUT | Report, comparison table, memo, bullet brief | 1-page brief + table + sources |

## Universal skeleton
```
QUESTION: <...>
FOR: <decision/deliverable>
SCOPE: <in / out>
SOURCES: <rules>. Cite every claim with a link. Say "no reliable source found" rather than guess.
DEPTH: <...>
OUTPUT: <format> + list of open questions
```

## Rendered for Claude
```xml
<documents>Any provided docs, each in <document index="n"> tags (long material first)</documents>
<question>QUESTION</question>
<purpose>PURPOSE</purpose>
<scope>SCOPE</scope>
<sourcing>SOURCES. Verify specifics that may have changed (prices, rules, dates) with search even if you feel confident. Cite each claim.</sourcing>
<output_format>OUTPUT, then "What I couldn't verify".</output_format>
```

## Rendered for OpenAI
```markdown
# Research question
QUESTION. Purpose: PURPOSE.
# Scope
SCOPE
# Sourcing rules
SOURCES. Use web search; cite each claim inline.
# Output
OUTPUT. End with unverified items.
```
Notes: in ChatGPT, use **Deep research** mode for exhaustive multi-source work.

## Token savers
- Research curves are nearly flat with effort: medium usually matches high. Start at medium.
- Split broad research into parallel sub-questions handled by cheaper workers, then synthesize with one strong call.
- Web fetch tools with filtering keep page boilerplate out of context.
