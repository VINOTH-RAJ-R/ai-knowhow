# Template: hard reasoning (reason.hard)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| PROBLEM | Full statement with all numbers/constraints | (required) |
| GIVEN | Facts, assumptions, data | Ask for missing numbers |
| OBJECTIVE | What "best" means (cost, time, risk…) | Ask |
| CHECK | How to verify the answer | "Verify by substitution / an independent method" |
| OUTPUT | Final answer format, level of working shown | Answer first, then key steps |

## Universal skeleton
```
PROBLEM: <...>
GIVEN: <...>
OBJECTIVE: <...>
VERIFY: Check the result with <method> and say how confident you are.
OUTPUT: Final answer first, then the key steps.
```

## Rendered for Claude
```xml
<problem>PROBLEM</problem>
<given>GIVEN</given>
<objective>OBJECTIVE</objective>
<instructions>Work it out carefully, then verify with CHECK. If the problem is under-specified, list the assumptions you made.</instructions>
<output_format>OUTPUT</output_format>
```
Don't write "think step by step". Current models reason internally; raise **effort** instead.

## Rendered for OpenAI
```markdown
# Problem
PROBLEM
# Given
GIVEN
# Objective
OBJECTIVE
# Verify
CHECK
# Output
OUTPUT
```
Use a reasoning-capable model with high reasoning effort. Don't ask for chain-of-thought in the output: reasoning models think internally.

## Token savers
- Reasoning is output-heavy (thinking tokens are billed as output). Use `high`/`max` only for problems that fail at medium.
- Re-run only the failures at a higher effort when you have a checker.
