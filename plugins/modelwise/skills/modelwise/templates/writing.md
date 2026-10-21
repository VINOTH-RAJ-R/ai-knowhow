# Template: writing & transforming text (text.write, text.transform)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| PIECE | Type: blog, email, LinkedIn post, docs page, script, summary, translation | (required) |
| AUDIENCE | Who reads it and what they already know | Ask: this drives tone and depth |
| GOAL | What the reader should think/do afterwards | Infer from PIECE |
| LEAD | For summaries to decision-makers: put the decision/ask first, then results, then risks | Lead with the ask |
| KEY_POINTS | Facts, arguments, data that must appear | Ask for at least 3 |
| VOICE | Tone, brand voice, a sample of past writing | Clear, plain, friendly |
| LENGTH | Words, characters, or reading time | Platform norm |
| SOURCE | Text to summarize/rewrite/translate | (required for transform) |
| AVOID | Words, claims, clichés to avoid | No hype words, no invented facts |
| PROPOSITION | The one thing the reader must take away, in one sentence (marketing and persuasive pieces) | Derive it from GOAL |
| PROOF | Reasons to believe: specific, sourced, permitted | Mark gaps `[NEEDS PROOF]`; never invent stats, quotes or customers |
| COMPLIANCE | Mandatory lines and banned claims for regulated industries (`guides/practice-content.md`) | Omit outside regulated industries |

**Senior copywriter's order** (marketing, launch and ad copy):
1. The audience's tension in their own words, then the proposition.
2. The hierarchy: the one thing, then 2–3 reasons to believe, then detail.
3. Specific claims instead of adjectives.
4. For headlines, 10 variants across angles, then the best 3 with reasons.
5. A claims-and-proof check before handing over.

In regulated industries, end with a "compliance review needed" list.

## Universal skeleton
```
WRITE: <PIECE> for <AUDIENCE>.
GOAL: After reading, they should <...>.
MUST INCLUDE: <KEY_POINTS>
VOICE: <tone> (sample below if available)
LENGTH: <...>
AVOID: <...>
SOURCE / VOICE SAMPLE: <pasted text: at the top for long material>
OUTPUT: <final text only (default) | variants only if the user asked | outline first for long pieces>
```

## Rendered for Claude
```xml
<source>SOURCE or VOICE SAMPLE (long material first)</source>
<audience>AUDIENCE: what they know, what they care about</audience>
<task>Write PIECE so that the reader GOAL.</task>
<must_include>KEY_POINTS</must_include>
<style>VOICE. LENGTH. Avoid: AVOID. Don't invent facts, numbers or quotes; mark anything you're unsure of as [CHECK].</style>
<output_format>Final text only. (Variants only if the user asked for them.)</output_format>
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
