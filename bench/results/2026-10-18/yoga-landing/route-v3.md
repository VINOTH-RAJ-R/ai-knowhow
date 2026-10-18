## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) — the best Claude fit for landing pages (4.5/5) at a balanced price.
**Effort:** medium (E3 medium) — API: `output_config.effort="medium"` · App: in Claude Code, `/model claude-sonnet-5-5`, then `/effort medium`
**Est. cost per run:** $0.28 (list price, before caching/batch)
**Cheaper:** claude-haiku-5-5 @ medium — about $0.01 per run, fit 3/5; quality may drop and it may skip checks on a long task.   **Stronger:** claude-opus-5-5 @ medium — $0.56 per run, fit 5/5; worth it for a client launch where design polish matters.
If this is just a quick prototype: claude-haiku-5-5 @ low, about $0.004 per run; if it is production-critical: claude-opus-5-5 @ high, about $2.00 per run.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 (`claude-haiku-5-5`) | medium | 3 | $0.01 | $14.00 | |
| GPT-6 Luna (`gpt-6-luna`) | medium | 3 | $0.01 | $14.00 | |
| **Claude Sonnet 5.5 (`claude-sonnet-5-5`)** | **medium** | **4.5** | **$0.28** | **$280.00** | **recommended** |
| GPT-6.1 Sol (`gpt-6.1-sol`) | medium | 4.5 | $0.28 | $280.00 | |
| Claude Opus 5.5 (`claude-opus-5-5`) | medium | 5 | $0.56 | $560.00 | |
| Claude Fable 5.1 (`claude-fable-5-1`) | medium | 5 | $1.40 | $1,400.00 | |
| GPT-6 Astra (`gpt-6-astra`) | medium | 5 | $1.40 | $1,400.00 | |

## Your structured prompt
```xml
<context>
Single-page marketing site for a yoga studio. The studio has no existing brand, copy, or design system to match. Most visitors will arrive on a phone from a local search and want to see the class schedule and book a first class, so the mobile layout matters most.
</context>

<task>
Build a one-page landing site for a yoga studio. The primary action is booking a first class.
</task>

<content>
Sections, in this order:
1. Hero: headline and one-line subhead about calm, strength, and community, with a "Book a first class" button.
2. About: a short paragraph on the studio's approach, written for beginners and returning students.
3. Class schedule: a weekly list or table of 6 sample classes (for example Vinyasa, Gentle Hatha, Yin, Restorative) with day, time, level, and teacher.
4. Teachers: 3 sample instructors, each with a short bio and a placeholder photo area.
5. Membership: 3 pricing tiers (drop-in, 10-class pack, unlimited monthly) with sample prices.
6. Testimonials: 2 short quotes, marked as placeholders in an HTML comment.
7. Visit: placeholder address ("123 Example Street, Your City"), opening hours, and a map placeholder.
8. Booking form: name, email, phone, preferred class, and a submit button that posts to a placeholder URL.
9. Footer: studio name, placeholder Instagram and Facebook links, and copyright.
Write realistic, concrete sample copy. Keep invented facts plausible and generic, with no real addresses, statistics, or customer names.
</content>

<design>
Calm, airy, with a warm wellness feel. Define a muted palette of 2 to 3 colors as CSS custom properties on :root, and keep body text clearly readable. Use one serif font for headings and one sans-serif font for body text.
Do not use: cream or off-white backgrounds by default, italic accent words in headlines, numbered "01/02/03" section labels, monospace eyebrow labels, pill-shaped buttons everywhere, purple-to-blue gradients.
</design>

<requirements>
Single index.html with inline CSS and only a few lines of vanilla JavaScript (for example, a mobile menu toggle). No frameworks and no build step.
Mobile-first, with a 16px side gutter. Check the layout at 375px and 1440px: no horizontal scroll, and the booking button is visible without zooming.
Use semantic HTML (header, nav, main, sections with headings, footer), alt text on images, labelled form fields, visible focus styles, and WCAG AA text contrast.
Before you say the page is done, verify it: render it in a headless browser at both widths if you have one, or check the breakpoints by reading the CSS. Say what you verified and what you could not.
</requirements>

<output_format>
One file, index.html, then a three-line summary: what you built, how you verified it, and which parts are still placeholders. Where details are unknown, use realistic sample content. Never show notes or instructions as page text.
</output_format>
```
Assumptions: no studio name, brand, or location was given, so the page uses placeholders; plain HTML/CSS, one file, no framework; list prices only.
To improve the result, tell me: the studio name, city, and real class schedule and prices; brand colors, fonts, or a reference site you like; photos of the space and teachers (or stock placeholders); where bookings go (booking tool URL or email) and what the trial offer is.

## Save tokens on this task
- Keep the brief and any brand tokens (colors, fonts) in a stable system prompt or project file, so repeat edits read cached input at about a tenth of the price.
- Iterate with one screenshot plus "change the hero spacing" instead of re-describing the whole page.
- Ask for targeted edits or a diff on later rounds: output tokens cost five times input ($10 vs $2 per million for Sonnet 5.5).

## Why this works
The XML tags separate what Claude should know from what it should build, and the "Do not use" list names concrete patterns, which works better than vague taste words. The one-sentence reason about phone visitors and the explicit verification step are what keep the output usable and stop Claude from declaring the page done without checking it.

<!-- MACHINE -->
ROUTE_MODEL: claude-sonnet-5-5
ROUTE_EFFORT: medium
PROMPT_START
<context>
Single-page marketing site for a yoga studio. The studio has no existing brand, copy, or design system to match. Most visitors will arrive on a phone from a local search and want to see the class schedule and book a first class, so the mobile layout matters most.
</context>

<task>
Build a one-page landing site for a yoga studio. The primary action is booking a first class.
</task>

<content>
Sections, in this order:
1. Hero: headline and one-line subhead about calm, strength, and community, with a "Book a first class" button.
2. About: a short paragraph on the studio's approach, written for beginners and returning students.
3. Class schedule: a weekly list or table of 6 sample classes (for example Vinyasa, Gentle Hatha, Yin, Restorative) with day, time, level, and teacher.
4. Teachers: 3 sample instructors, each with a short bio and a placeholder photo area.
5. Membership: 3 pricing tiers (drop-in, 10-class pack, unlimited monthly) with sample prices.
6. Testimonials: 2 short quotes, marked as placeholders in an HTML comment.
7. Visit: placeholder address ("123 Example Street, Your City"), opening hours, and a map placeholder.
8. Booking form: name, email, phone, preferred class, and a submit button that posts to a placeholder URL.
9. Footer: studio name, placeholder Instagram and Facebook links, and copyright.
Write realistic, concrete sample copy. Keep invented facts plausible and generic, with no real addresses, statistics, or customer names.
</content>

<design>
Calm, airy, with a warm wellness feel. Define a muted palette of 2 to 3 colors as CSS custom properties on :root, and keep body text clearly readable. Use one serif font for headings and one sans-serif font for body text.
Do not use: cream or off-white backgrounds by default, italic accent words in headlines, numbered "01/02/03" section labels, monospace eyebrow labels, pill-shaped buttons everywhere, purple-to-blue gradients.
</design>

<requirements>
Single index.html with inline CSS and only a few lines of vanilla JavaScript (for example, a mobile menu toggle). No frameworks and no build step.
Mobile-first, with a 16px side gutter. Check the layout at 375px and 1440px: no horizontal scroll, and the booking button is visible without zooming.
Use semantic HTML (header, nav, main, sections with headings, footer), alt text on images, labelled form fields, visible focus styles, and WCAG AA text contrast.
Before you say the page is done, verify it: render it in a headless browser at both widths if you have one, or check the breakpoints by reading the CSS. Say what you verified and what you could not.
</requirements>

<output_format>
One file, index.html, then a three-line summary: what you built, how you verified it, and which parts are still placeholders. Where details are unknown, use realistic sample content. Never show notes or instructions as page text.
</output_format>
PROMPT_END
