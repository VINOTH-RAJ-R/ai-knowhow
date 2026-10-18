# Template: frontend / UI (code.frontend)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| WHAT | Page/component and its purpose | (required) |
| AUDIENCE | Who visits and what they should do | Infer from WHAT |
| CONTENT | Real copy, sections, data | Realistic placeholder copy |
| STACK | HTML/CSS, React, Tailwind, Next.js… | Match the repo; else single-file HTML/CSS |
| LOOK | Brand colors, fonts, references, mood | Ask: this changes everything |
| AVOID | Specific visual patterns you don't want | See default list below |
| RESPONSIVE / A11Y | Breakpoints, accessibility level | Mobile-first, WCAG AA contrast |
| DONE_WHEN | How it'll be checked | Renders at 375px and 1440px with no horizontal scroll |

## Universal skeleton
```
WHAT: <page/component> for <AUDIENCE>. Primary action: <CTA>.
CONTENT: <sections in order, real copy if available>
STACK: <tech>
LOOK: <brand colors with hex, fonts, 1-2 reference sites, mood words>
AVOID: <concrete patterns>
RESPONSIVE/A11Y: <rules>
DONE WHEN: <checks>
OUTPUT: <files>
```

## Rendered for Claude
```xml
<context>AUDIENCE, brand, and any existing components/design tokens (paste them).</context>
<task>Build WHAT.</task>
<content>CONTENT</content>
<design>
LOOK
Do not use: AVOID (name concrete patterns: generic advice just swaps one default style for another)
</design>
<requirements>STACK, RESPONSIVE/A11Y. Check the layout at 375px and 1440px before finishing.</requirements>
<output_format>OUTPUT. Where details are unknown, write realistic sample content (no real addresses, stats or names); never show instructions or notes as page text.</output_format>
```
Default AVOID list (edit per project): cream/off-white background by default, italic accent words in headlines, numbered "01/02/03" section labels, monospace eyebrow labels, pill-shaped buttons everywhere, purple-to-blue gradients.

## Rendered for OpenAI
```markdown
# Build
WHAT for AUDIENCE. Primary action: CTA.

# Content
CONTENT

# Design system
LOOK. Avoid: AVOID.

# Technical
STACK. RESPONSIVE/A11Y. Reuse existing components and tokens where they exist.

# Output
OUTPUT
```
Notes: GPT models do well with an explicit design system (colors, spacing scale, type scale) and a short list of reference components to match.

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "landing page for my bakery"
**Structured (Claude):**
```xml
<context>Small neighborhood bakery "Crumb & Co" in Pune. Visitors are locals on phones who want today's menu and to pre-order cakes.</context>
<task>Build a one-page landing site.</task>
<content>Hero with tagline "Baked at 5am, gone by noon", today's specials (6 items with prices in ₹), custom-cake pre-order form (name, phone, date, flavor), opening hours, map link, Instagram link.</content>
<design>Warm terracotta #C2552D and deep brown #3B2418 on white; serif headings (Fraunces), sans body (Inter). Photo-forward.
Do not use: pill buttons, gradient blobs, italic accent words, numbered section labels.</design>
<requirements>Single index.html with inline CSS, no frameworks. Mobile-first; check 375px and 1440px. Form posts to a placeholder URL.</requirements>
<output_format>One file, then a 3-line summary.</output_format>
```

## Token savers
- Provide design tokens/components once in the system prompt or a project file. Don't repeat them each turn.
- Iterate on screenshots: one screenshot plus "change X" is far cheaper than re-describing the page.
