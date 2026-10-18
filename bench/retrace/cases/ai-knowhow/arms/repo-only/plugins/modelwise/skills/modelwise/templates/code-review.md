# Template: review, refactor, migrate, explain (code.review)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| MODE | review / refactor / migrate / explain | Infer from the ask |
| TARGET | Files, PR, module, or whole repo | (required) |
| FOCUS | Bugs, security, performance, readability, a specific concern | Correctness first, then security |
| STANDARD | Style guide, conventions, target version for migrations | Existing project conventions |
| SAFETY | Behavior must stay identical? Tests available? | Behavior-preserving; run tests |
| OUTPUT | Findings list, diff, migration plan, written explanation | Depends on MODE |

## Universal skeleton
```
MODE: <review|refactor|migrate|explain> TARGET: <...>
FOCUS: <...>  STANDARD: <...>
SAFETY: <behavior-preserving? tests to run?>
OUTPUT:
- review → findings ranked by severity: file:line, problem, concrete failure scenario, fix
- refactor/migrate → plan first (steps + risks), then diffs in small, testable steps
- explain → architecture overview, key flows, where to start reading
```

## Rendered for Claude
```xml
<target>TARGET (paths; paste only if the tool can't read files)</target>
<task>MODE with focus on FOCUS.</task>
<requirements>STANDARD. SAFETY. For each finding give a concrete input or state that breaks, not just a style opinion. Skip nitpicks unless asked.</requirements>
<output_format>OUTPUT</output_format>
```

## Rendered for OpenAI
```markdown
# Task
MODE of TARGET. Focus: FOCUS.

# Standards
STANDARD. SAFETY.

# Output
OUTPUT. Rank by severity; include file:line and a concrete failure scenario per finding.
```

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "review my PR"
**Structured:** "Review the diff on branch `feature/payments` against `main`. Focus: correctness and security (it handles card webhooks). Report only real bugs with a concrete failure scenario, ranked by severity, file:line. No style nits."

## Token savers
- Review the **diff**, not the whole repo.
- For big migrations, plan with a strong model once, then let a balanced/fast model do the repetitive per-file edits.
