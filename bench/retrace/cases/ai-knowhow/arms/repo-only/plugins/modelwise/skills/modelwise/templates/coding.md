# Template: coding (code.quick, code.build)

## Fill these slots
Ask the user only for slots that are missing and would change the result. Fill the rest with sensible defaults and state them.

| Slot | Why it matters | Default if missing |
|---|---|---|
| GOAL | The outcome, in one sentence | (required) |
| STACK | Language, framework, versions | Infer from files; otherwise ask |
| EXISTING | Repo, files, APIs it must fit into | "New standalone code" |
| CONSTRAINTS | Libraries allowed/forbidden, style, performance, security | Follow existing project conventions |
| DONE_WHEN | How we'll know it works (tests, command, behavior) | "Tests pass and the example runs" |
| OUTPUT | Full files, a diff, or a single function | Diff for existing code, full file for new |

## Universal skeleton
```
GOAL: <one sentence outcome>
WHY: <who uses it / why it matters, one line>
STACK: <language + framework + versions>
EXISTING CODE: <paths or pasted snippets; long material goes here, before the ask>
CONSTRAINTS:
- <hard rule>
- <hard rule>
DONE WHEN:
- <observable check, e.g. `npm test` passes, endpoint returns 200 with body X>
OUTPUT: <diff | full files | function only> + a 3-line summary of what changed and why
```

## Rendered for Claude (Fable / Opus / Sonnet / Haiku)
```xml
<context>
WHY + EXISTING CODE (paste long files here, at the top)
</context>
<task>GOAL</task>
<requirements>
STACK, CONSTRAINTS
Before saying it's done, run a real check (the tests, the build, or the changed command). A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>DONE_WHEN</done_when>
<output_format>OUTPUT</output_format>
```
Notes: state the outcome rather than step-by-step instructions. Current Claude models plan well and over-scripting hurts. Set effort with the parameter, not with words.

## Rendered for OpenAI (GPT-6 / Codex)
```markdown
# Goal
GOAL. WHY.

# Context
STACK. EXISTING CODE (paths or snippets).

# Requirements
- CONSTRAINTS
- Match the existing code style; keep the change minimal and focused.

# Done when
DONE_WHEN. Run the tests/linters available and report results.

# Output
OUTPUT. End with a short summary of the change.
```
Notes: state goals, constraints and the done-loop (implement → run → inspect → fix); remove contradictory rules and old "double-check" crutches. For Codex models, keep the prompt lean and let its built-in coding instructions do the rest. Use `reasoning.effort` and (where supported) `verbosity` instead of "be brief" text.

## Example (illustrative: shows the structure, never copy its specifics)
**Basic prompt:** "make a python script to rename my photos by date"

**Structured:**
```xml
<context>Personal tool. I have ~3,000 JPG/HEIC photos in one folder on macOS. Python 3.10 is installed.</context>
<task>Write a Python script that renames each photo to YYYY-MM-DD_HHMMSS.ext using the EXIF capture date.</task>
<requirements>
- Standard library plus Pillow only (and pillow-heif for HEIC).
- Fall back to file modified time when EXIF is missing; never overwrite: add _1, _2 on collisions.
- A --dry-run flag that prints planned renames without changing anything.
Run it with --dry-run on a temp folder with two sample files before saying it's done.
</requirements>
<done_when>Dry run lists correct new names; real run renames files; re-running is a no-op.</done_when>
<output_format>One file rename_photos.py, then 3 lines on how to run it.</output_format>
```
**Route:** code.quick, simple → fast tier at low effort.

## Token savers for coding
- Point to files by path in agentic tools (Claude Code, Codex) instead of pasting whole files.
- Ask for a **diff**, not the whole file, when changing existing code.
- One task per conversation. Start fresh rather than dragging a long history into a new task.
- Escalate on failure: run at the recommended effort first and re-run only failures at the next level up.
