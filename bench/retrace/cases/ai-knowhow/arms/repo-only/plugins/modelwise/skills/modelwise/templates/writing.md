# Template: writing & transforming text (text.write, text.transform)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| PIECE | Type: blog, email, LinkedIn post, docs page, script, summary, translation | (required) |
| AUDIENCE | Who reads it and what they already know | Ask: this drives tone and depth |
| GOAL | What the reader should think/do afterwards | Infer from PIECE |
| KEY_POINTS | Facts, arguments, data that must appear | Ask for at least 3 |
| VOICE | Tone, brand voice, a sample of past writing | Clear, plain, friendly |
| LENGTH | Words, characters, or reading time | Platform norm |
| SOURCE | Text to summarize/rewrite/translate | (required for transform) |
| AVOID | Words, claims, clichés to avoid | No hype words, no invented facts |

## Universal skeleton
```
WRITE: <PIECE> for <AUDIENCE>.
GOAL: After reading, they should <...>.
MUST INCLUDE: <KEY_POINTS>
VOICE: <tone> (sample below if available)
LENGTH: <...>
AVOID: <...>
SOURCE / VOICE SAMPLE: <pasted text: at the top for long material>
OUTPUT: <final text only | 3 variants | outline first>
```

## Rendered for Claude
```xml
<source>SOURCE or VOICE SAMPLE (long material first)</source>
<audience>AUDIENCE: what they know, what they care about</audience>
<task>Write PIECE so that the reader GOAL.</task>
<must_include>KEY_POINTS</must_include>
<style>VOICE. LENGTH. Avoid: AVOID. Don't invent facts, numbers or quotes; mark anything you're unsure of as [CHECK].</style>
<output_format>Final text only (or: 3 short variants labelled A/B/C).</output_format>
```

## Rendered for OpenAI
```markdown
# Task
Write PIECE for AUDIENCE. Goal: GOAL.

# Must include
KEY_POINTS

# Style
VOICE. LENGTH. Avoid: AVOID. Never invent facts or quotes.

# Source / sample
SOURCE

# Output
Final text only.
```
Notes: use `verbosity: low` for short pieces where supported, instead of "be concise" text.

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "write a linkedin post about our new feature"
**Structured:** PIECE = LinkedIn post; AUDIENCE = HR managers at 50-500 person companies; GOAL = book a demo; KEY_POINTS = (auto-generated payslips, cuts payroll time from 2 days to 2 hours, live in India and UAE); VOICE = confident, human, no buzzwords; LENGTH = 120-180 words, 1 emoji max; OUTPUT = 2 variants.

## Token savers
- Writing rarely needs high effort: low/medium is usually indistinguishable in quality.
- Summaries and translations at volume → fastest tier + Batch API (50% off).
- Ask for an **outline first** on long pieces. Fixing an outline is cheap; rewriting 2,000 words isn't.
