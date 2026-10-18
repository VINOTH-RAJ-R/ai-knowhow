## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) - best fit (4.5/5) for a landing page at balanced cost; ties with GPT-6.1 Sol on fit and price.
**Effort:** medium (E3) - API: `output_config.effort=medium` - App: in Claude Code run `/model sonnet` then `/effort medium`
**Est. cost per run:** $0.28 (list price, before caching/batch)
**Cheaper:** Claude Haiku 5.5 @ medium ($0.01) - fine for a rough draft, lower design quality (fit 3/5)   **Stronger:** Claude Opus 5.5 @ medium ($0.56) - worth it only if this is a paying client's site and you want a higher design ceiling
Reference (other vendor): GPT-6.1 Sol @ medium, $0.28 - same fit and cost; use it if you work in ChatGPT or Codex.
If this is just a quick prototype: Claude Haiku 5.5 @ low, <$0.01 (fit 3/5).

Assumptions: task = code.frontend, complexity = moderate (borderline: a quick mock would be simple), priority = balanced, provider = Anthropic because you are in Claude Code. This skill itself ran on Sonnet 5.5, which is the recommended tier for running it.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 | medium | 3 | $0.01 | $14 | |
| GPT-6 Luna | medium | 3 | $0.01 | $14 | |
| **Claude Sonnet 5.5** | **medium** | **4.5** | **$0.28** | **$280** | **recommended** |
| GPT-6.1 Sol | medium | 4.5 | $0.28 | $280 | |
| Claude Opus 5.5 | medium | 5 | $0.56 | $560 | |
| Claude Fable 5.1 | medium | 5 | $1.40 | $1,400 | |
| GPT-6 Astra | medium | 5 | $1.40 | $1,400 | |

## Your structured prompt
```xml
<context>
A yoga studio needs a one-page landing site. Visitors are local people, mostly on phones, who want to see what classes are offered, when, and book a first class. Studio name, location and brand details are not given yet, so use the placeholders below and keep them easy to find and replace.
</context>

<task>
Build a one-page landing site for a yoga studio. Primary action: book a trial class (a clear "Book a class" button in the hero and again near the end of the page).
</task>

<content>
Sections in order, with realistic placeholder copy (clearly marked so it is easy to swap):
1. Hero: studio name [[FILL: studio name]], one-line promise, primary CTA, one supporting image slot.
2. Class styles: 4 to 5 styles (for example vinyasa, yin, beginners, prenatal) with a one-line description and level for each.
3. Weekly schedule: a simple table or list by day and time, readable on a phone.
4. Teachers: 3 short bios with photo slots.
5. Pricing: drop-in, 10-class pack, monthly unlimited, plus a first-class offer. [[FILL: real prices and currency]]
6. Testimonials: 3 short quotes, marked as placeholders.
7. Visit and contact: address and map link [[FILL: address]], opening hours, phone/WhatsApp, Instagram link, short booking form (name, email, phone, preferred class) that posts to a placeholder URL.
</content>

<design>
Calm, welcoming, uncluttered, with generous whitespace and photo-forward layout. [[FILL: brand colors with hex, heading and body fonts, 1-2 reference sites]]. If no brand is given, choose a restrained palette of two or three natural tones with one accent color, one serif or soft sans for headings and one clean sans for body, and state the choices at the top of the CSS as variables.
Do not use: cream or off-white page background by default, italic accent words in headlines, numbered 01/02/03 section labels, monospace eyebrow labels, pill-shaped buttons everywhere, purple-to-blue gradients, stock lotus or om icons as decoration.
</design>

<requirements>
- Single index.html with inline CSS and a small amount of vanilla JS only if needed (no frameworks, no build step). Images are placeholders (solid blocks or inline SVG), not hotlinked.
- Mobile-first. Semantic HTML, alt text, visible focus states, WCAG AA contrast, tap targets of at least 44px.
- Open the page and check the layout at 375px and 1440px: no horizontal scroll, text readable, CTA visible without scrolling at 375px. Fix anything that fails before saying it is done.
</requirements>

<output_format>
The finished file, then a 3-line summary: what was built, which placeholders still need real content, and how it was checked.
</output_format>
```
Assumptions: stack is a single HTML/CSS file; sections, class types and placeholder copy are my guesses for a typical studio; brand look, studio name, address and prices are left as [[FILL: ...]] because a guess would be wrong; the default AVOID list from the template is applied, plus no lotus/om decoration.

## Save tokens on this task
- Put design tokens (colors, fonts, spacing) in a project file or system prompt once, then iterate with a screenshot plus "change X" instead of re-describing the page.
- Ask for the finished file plus a short summary, not a walkthrough, and request diffs for later edits.
- Start a fresh session for each new page; use medium effort first and only go up a level if the design misses.

## Why this works
The XML tags separate who the page is for (context) from what to build (task), the sections (content) and the look (design), so Claude does not have to guess which is which. The explicit avoid list steers away from the generic AI look, since vague advice like "make it not generic" only swaps one default for another. The requirements end with a real check (open it at 375px and 1440px), because Sonnet 5.5 can report "done" without verifying unless asked.

<!-- MACHINE -->
ROUTE_MODEL: claude-sonnet-5-5
ROUTE_EFFORT: medium
TASK: code.frontend | COMPLEXITY: moderate | PRIORITY: balanced
PROMPT_START
<context>
A yoga studio needs a one-page landing site. Visitors are local people, mostly on phones, who want to see what classes are offered, when, and book a first class. Studio name, location and brand details are not given yet, so use the placeholders below and keep them easy to find and replace.
</context>

<task>
Build a one-page landing site for a yoga studio. Primary action: book a trial class (a clear "Book a class" button in the hero and again near the end of the page).
</task>

<content>
Sections in order, with realistic placeholder copy (clearly marked so it is easy to swap):
1. Hero: studio name [[FILL: studio name]], one-line promise, primary CTA, one supporting image slot.
2. Class styles: 4 to 5 styles (for example vinyasa, yin, beginners, prenatal) with a one-line description and level for each.
3. Weekly schedule: a simple table or list by day and time, readable on a phone.
4. Teachers: 3 short bios with photo slots.
5. Pricing: drop-in, 10-class pack, monthly unlimited, plus a first-class offer. [[FILL: real prices and currency]]
6. Testimonials: 3 short quotes, marked as placeholders.
7. Visit and contact: address and map link [[FILL: address]], opening hours, phone/WhatsApp, Instagram link, short booking form (name, email, phone, preferred class) that posts to a placeholder URL.
</content>

<design>
Calm, welcoming, uncluttered, with generous whitespace and photo-forward layout. [[FILL: brand colors with hex, heading and body fonts, 1-2 reference sites]]. If no brand is given, choose a restrained palette of two or three natural tones with one accent color, one serif or soft sans for headings and one clean sans for body, and state the choices at the top of the CSS as variables.
Do not use: cream or off-white page background by default, italic accent words in headlines, numbered 01/02/03 section labels, monospace eyebrow labels, pill-shaped buttons everywhere, purple-to-blue gradients, stock lotus or om icons as decoration.
</design>

<requirements>
- Single index.html with inline CSS and a small amount of vanilla JS only if needed (no frameworks, no build step). Images are placeholders (solid blocks or inline SVG), not hotlinked.
- Mobile-first. Semantic HTML, alt text, visible focus states, WCAG AA contrast, tap targets of at least 44px.
- Open the page and check the layout at 375px and 1440px: no horizontal scroll, text readable, CTA visible without scrolling at 375px. Fix anything that fails before saying it is done.
</requirements>

<output_format>
The finished file, then a 3-line summary: what was built, which placeholders still need real content, and how it was checked.
</output_format>
PROMPT_END
