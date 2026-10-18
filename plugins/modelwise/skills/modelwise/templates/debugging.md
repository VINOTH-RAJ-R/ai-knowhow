# Template: debugging (code.debug)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| SYMPTOM | What happens vs what should happen | (required) |
| EVIDENCE | Exact error, stack trace, logs, failing test output | Ask: never guess without it |
| REPRO | Steps or command that triggers it | Ask |
| CHANGED | What changed recently (deploy, upgrade, new code) | "Unknown" |
| ENV | OS, runtime versions, prod vs local | Infer from files |
| TRIED | What has already been ruled out | "Nothing yet" |
| SCOPE | Fix only, or fix + root-cause explanation + regression test | Fix + root cause + test |

## Universal skeleton
```
SYMPTOM: Expected <X>, got <Y>.
EVIDENCE: <exact error text / trace / logs: paste verbatim>
REPRO: <command or steps>
RECENT CHANGES: <...>
ENV: <...>
ALREADY TRIED: <...>
ASK: Find the root cause before changing code. Explain it in 2-3 sentences, apply the smallest fix, add a regression test, and show the test passing.
```

## Rendered for Claude
```xml
<evidence>EVIDENCE (verbatim, at the top)</evidence>
<context>ENV, RECENT CHANGES, ALREADY TRIED, relevant file paths</context>
<task>SYMPTOM. Find the root cause first: form a hypothesis, confirm it with the code or a quick experiment, then fix.</task>
<requirements>Smallest change that fixes the cause (not the symptom). Add a regression test. Run it and the existing tests before reporting.</requirements>
<output_format>Root cause (2-3 sentences) → the diff → test output.</output_format>
```

## Rendered for OpenAI
```markdown
# Problem
Expected X, got Y. Repro: REPRO

# Evidence
EVIDENCE

# Context
ENV. Recent changes: CHANGED. Already tried: TRIED.

# Instructions
1. Identify the root cause before editing. State it.
2. Make the minimal fix.
3. Add a regression test and run the suite.

# Output
Root cause, diff, test results.
```

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "my react app shows blank page after deploy"
**Structured:** fill EVIDENCE with the browser console error and the network tab 404s, REPRO with the deployed URL, CHANGED with "moved from CRA to Vite", ENV with the hosting provider. Without the console error, the model can only guess. Ask for it first.

## Token savers
- Paste the **first** error and the relevant 20-50 lines of trace, not 5,000 lines of logs.
- Debug at medium effort first. Raise to high only if the first hypothesis fails.
- In agentic tools, let the agent run the repro itself rather than pasting outputs back and forth.
