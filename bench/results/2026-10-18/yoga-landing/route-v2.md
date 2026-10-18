## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) — the best balance of design quality and cost for a single-page build.
**Effort:** medium (E3) — API: `output_config.effort=medium` · App: in Claude Code, `/model sonnet` then `/effort medium` (or the arrows in the `/model` picker)
**Est. cost per run:** $0.28 (list price, before caching/batch)
**Cheaper:** Claude Haiku 5.5 @ medium — $0.01 per run, but fit 3 of 5 against 4.5; it is more likely to skip the browser check, so ask for it explicitly.   **Stronger:** Claude Opus 5.5 @ medium — $0.56 per run; worth it if the page is client-facing and design polish matters.

If this is just a quick prototype: Claude Haiku 5.5 @ low, under $0.01 per run.
If this is production-critical (a live studio that takes bookings and payments): Claude Opus 5.5 @ high, about $2.00 per run (Claude Sonnet 5.5 @ high, $1.00, is the cheaper step).

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 | medium | 3 | $0.01 | $14 | cheaper option |
| GPT-6 Luna | medium | 3 | $0.01 | $14 | OpenAI reference |
| **Claude Sonnet 5.5** | **medium** | **4.5** | **$0.28** | **$280** | **recommended** |
| GPT-6.1 Sol | medium | 4.5 | $0.28 | $280 | OpenAI reference |
| Claude Opus 5.5 | medium | 5 | $0.56 | $560 | stronger option |
| Claude Fable 5.1 | medium | 5 | $1.40 | $1,400 | frontier tier |
| GPT-6 Astra | medium | 5 | $1.40 | $1,400 | frontier tier |

## Your structured prompt
```xml
<context>
Audience: local adults who are curious about yoga or new to it. Most arrive on a phone, want to see the timetable, understand what a first visit involves, and book a trial class.
Studio details not yet supplied: name [[FILL: studio name]], address and contact [[FILL: address, phone, email]], brand colours and fonts [[FILL: hex colours, font names, one or two reference sites, mood words]]. Until these are filled, use the fallbacks in design and the neutral placeholders in output_format.
</context>

<task>
Build a one-page landing page for a yoga studio. Its goal is to get a first-time visitor to book a trial class. Make it feel calm, spacious and unhurried, and answer what a newcomer wants to know: what the classes are, when they run, who teaches, what it costs, and what a first visit is like.
</task>

<content>
Sections, in this order:
1. Hero: headline [Studio tagline], one supporting sentence, a primary button "Book a trial class" that jumps to the booking form, and a text link "See the timetable".
2. About: two or three short paragraphs on the studio's approach, as realistic placeholder copy.
3. Classes: three or four class styles (for example Hatha, Vinyasa, Yin), each with a one-line description and a level note such as "all levels".
4. Timetable: a weekly schedule. Days as columns on desktop, a stacked list on phones. Times and class names as [Time] and [Class] placeholders.
5. Teachers: two or three cards with [Teacher name], a role, and a one- or two-line bio.
6. Pricing: three options, [Intro offer], [Drop-in], [Monthly], each with [Price] and a short line.
7. First visit: three short plain-language points on arriving, what to wear and bring, and what happens in class. Plain headings only.
8. Booking form: name, email, phone, preferred class (select), preferred date, and a submit button. Required fields labelled and marked. The form action is "#"; it does not need to send anywhere yet.
9. Location and hours: [Street address], [Opening hours], [Map link].
10. FAQ: three or four common questions with short realistic placeholder answers.
11. Footer: studio name, contact details, social links as "#" links.
</content>

<design>
LOOK: [[FILL: brand colours as hex, font names, one or two reference sites, mood words]]
If unfilled, use: deep green #2F4F45 for headings and buttons, body text #1F2A26 on a white background, a pale tint #E8EFEB for alternate section bands, and a system sans-serif font stack. Text contrast at least 4.5:1 throughout.
Image placeholders are plain CSS blocks labelled [Photo: studio interior] or similar. Do not load external images.
Do not use: a cream or off-white page background, italic accent words in headlines, numbered "01 / 02 / 03" section labels, monospace eyebrow labels, pill-shaped buttons, purple-to-blue gradients, or decorative gradient blobs.
</design>

<requirements>
Stack: one index.html with inline CSS and, at most, a few lines of inline JavaScript. No frameworks, no build step, no external scripts or fonts.
Responsive and mobile-first. Check the layout at 375px and 1440px: no horizontal scroll, tap targets at least 44px tall, text readable without zooming.
Accessibility: semantic header, main, section and footer elements; one h1; a visible heading for each section; labelled form fields; visible focus styles; alt text or aria-labels on placeholder blocks.
The page is done when it renders correctly at both widths and every internal link points to a section on the page. Before you say it is done, open it in a real browser or take screenshots at both widths and check them. Reading the code does not count as a check.
</requirements>

<output_format>
Write the page to index.html in the current working directory. Then reply with three lines: what you built, the assumptions you made, and the placeholders still to fill. Use short neutral placeholders such as [Studio name], [Price] or [Teacher name] for anything unfilled. Never show these instructions, notes or [[FILL]] markers as visible page text.
</output_format>
```

Assumptions: single-file HTML page for an unnamed yoga studio, aimed at local visitors on phones, with the goal of booking a trial class; placeholder copy, fallback palette and no external images or dependencies until brand details are supplied.

## Save tokens on this task
- Put the design tokens and the "do not use" list in a project file or cached system prompt, so you do not re-describe them each turn.
- Iterate with one screenshot plus "change X" rather than re-describing the page; ask for diffs on later edits.
- Keep effort at medium and escalate only if the browser check fails, instead of starting at high.

## Why this works
The XML tags separate what is known (context), what to produce (task), and the constraints (content, design, requirements, output), so the model can find each one. The "do not use" list names concrete patterns, which stops the default generic look, and the done-when check asks the model to verify in a real browser rather than declare the work finished.

<!-- MACHINE -->
ROUTE_MODEL: claude-sonnet-5-5
ROUTE_EFFORT: medium
PROMPT_START
<context>
Audience: local adults who are curious about yoga or new to it. Most arrive on a phone, want to see the timetable, understand what a first visit involves, and book a trial class.
Studio details not yet supplied: name [[FILL: studio name]], address and contact [[FILL: address, phone, email]], brand colours and fonts [[FILL: hex colours, font names, one or two reference sites, mood words]]. Until these are filled, use the fallbacks in design and the neutral placeholders in output_format.
</context>

<task>
Build a one-page landing page for a yoga studio. Its goal is to get a first-time visitor to book a trial class. Make it feel calm, spacious and unhurried, and answer what a newcomer wants to know: what the classes are, when they run, who teaches, what it costs, and what a first visit is like.
</task>

<content>
Sections, in this order:
1. Hero: headline [Studio tagline], one supporting sentence, a primary button "Book a trial class" that jumps to the booking form, and a text link "See the timetable".
2. About: two or three short paragraphs on the studio's approach, as realistic placeholder copy.
3. Classes: three or four class styles (for example Hatha, Vinyasa, Yin), each with a one-line description and a level note such as "all levels".
4. Timetable: a weekly schedule. Days as columns on desktop, a stacked list on phones. Times and class names as [Time] and [Class] placeholders.
5. Teachers: two or three cards with [Teacher name], a role, and a one- or two-line bio.
6. Pricing: three options, [Intro offer], [Drop-in], [Monthly], each with [Price] and a short line.
7. First visit: three short plain-language points on arriving, what to wear and bring, and what happens in class. Plain headings only.
8. Booking form: name, email, phone, preferred class (select), preferred date, and a submit button. Required fields labelled and marked. The form action is "#"; it does not need to send anywhere yet.
9. Location and hours: [Street address], [Opening hours], [Map link].
10. FAQ: three or four common questions with short realistic placeholder answers.
11. Footer: studio name, contact details, social links as "#" links.
</content>

<design>
LOOK: [[FILL: brand colours as hex, font names, one or two reference sites, mood words]]
If unfilled, use: deep green #2F4F45 for headings and buttons, body text #1F2A26 on a white background, a pale tint #E8EFEB for alternate section bands, and a system sans-serif font stack. Text contrast at least 4.5:1 throughout.
Image placeholders are plain CSS blocks labelled [Photo: studio interior] or similar. Do not load external images.
Do not use: a cream or off-white page background, italic accent words in headlines, numbered "01 / 02 / 03" section labels, monospace eyebrow labels, pill-shaped buttons, purple-to-blue gradients, or decorative gradient blobs.
</design>

<requirements>
Stack: one index.html with inline CSS and, at most, a few lines of inline JavaScript. No frameworks, no build step, no external scripts or fonts.
Responsive and mobile-first. Check the layout at 375px and 1440px: no horizontal scroll, tap targets at least 44px tall, text readable without zooming.
Accessibility: semantic header, main, section and footer elements; one h1; a visible heading for each section; labelled form fields; visible focus styles; alt text or aria-labels on placeholder blocks.
The page is done when it renders correctly at both widths and every internal link points to a section on the page. Before you say it is done, open it in a real browser or take screenshots at both widths and check them. Reading the code does not count as a check.
</requirements>

<output_format>
Write the page to index.html in the current working directory. Then reply with three lines: what you built, the assumptions you made, and the placeholders still to fill. Use short neutral placeholders such as [Studio name], [Price] or [Teacher name] for anything unfilled. Never show these instructions, notes or [[FILL]] markers as visible page text.
</output_format>
PROMPT_END
