# Art direction for image prompts (posters, banners, social graphics)

Image models do what the brief says. A brief that says "flat, solid, simple, minimal" gets clip-art on a flat fill. Write the brief the way a senior designer briefs an illustrator: one idea, a clear focal point, depth, light, a controlled colour system, and typographic hierarchy.

## The senior-designer checklist (run it before you send any prompt)

Before this checklist, do the thinking in `guides/practice-design.md`: the brief, the category clichés, and three territories that differ on at least two axes. This checklist covers the craft of each route.

0. **Industry fit first.** Apply `guides/industry-lens.md`. Name the top designer for that industry, the brand personality, and what that industry's best work looks like. Every choice below has to fit it.
1. **Concept.** One idea that goes beyond the literal words, *in the industry's own visual language*, and different from the category clichés. It comes from this brief, not from an example. These show the kind of thinking, not ideas to reuse:
   - **Type-led,** for a bakery's new opening hours: "the times set huge, as if pressed into dough, with flour dusting the letters."
   - **Human-led,** for an accounting app's invoicing feature: "a café owner closing the laptop at 6 pm, chairs already up on the tables."
   - **Graphic-led,** for a bank's savings product: "the brand's own shape repeated as a steady rhythm of tiles, one tile filled in."

   Never use a genre that doesn't fit the industry (a mystical portal for a bank), and never make a category cliché the hero (rising bars for finance). Write the concept in one line.
2. **Focal point and hierarchy.** One hero visual, one headline, one supporting element. Say the reading order.
3. **Composition.** Name the grid and where things sit (left third, centre, rule of thirds). Margins of about 6–8% of the short edge. Empty space should be deliberate, not leftover.
4. **Depth.** Foreground, midground and background layers. A light direction, and the shadows and highlights that come from it.
5. **Colour as visual weight.** "80% blue" means blue dominates what the eye sees. It does not mean a flat fill. Use a tonal range of the primary (3–5 tones, from shade to tint), with gradients and light inside that range. Keep the accents restrained, and check text contrast (4.5:1 for normal text, 3:1 for large display text). `scripts/palette.py` gives the tones and the contrast.
6. **Typography.** The headline is a designed element: dominant size (cap height about 15–25% of the canvas height on a banner), tight tracking, at most two weights, deliberate line breaks.
7. **Finish.** Subtle grain or texture, small highlights, consistent light. These are the details that separate "designed" from "generated".
8. **Edge to edge.** The background fills the whole canvas. Say that a reserved zone is "kept clear of elements, still filled with the background". Otherwise models draw white bars.

## Style families (pick a different one for each option)
A different style family is not enough on its own. Two routes that are both "a 3D object on a blue gradient" are the same idea even in different materials. Vary the focal element too: type-led, object-led, human-led or graphic-led (`guides/practice-design.md`).

| Family | When it fits | Prompt vocabulary | Watch out |
|---|---|---|---|
| **Premium 3D render** | Finance, tech, launches | "soft 3D render, matte and satin materials, studio lighting with a key light from the upper left and soft rim light, shallow depth of field, subtle ambient occlusion" | Can look like generic stock 3D. Fix it with a specific concept and material. |
| **Glass and light** | Fintech, premium, "new" | "layered frosted-glass panels, light refracting through glass, soft glow, translucent depth, gentle bloom" | Text over glass gets muddy. Put text on a calm zone. |
| **Layered paper-cut** | Festivals, culture, warmth | "layered paper-cut illustration, 5–7 depth layers, soft drop shadows between layers, tactile paper texture" | Keep the palette disciplined. Paper invites extra colours. |
| **Editorial photography + type** | Human warmth, trust | "editorial photograph, natural window light, 50mm, shallow depth of field, graded to the brand's blues" | Faces and real people raise compliance and likeness issues. Use hands, objects, places. |
| **Typographic-led** | Announcements, alerts, short copy | "the headline is the hero: oversized bold type, cropped at the edge, layered behind and in front of a graphic element" | Keep the words few. Models misspell long text. |
| **Abstract light and geometry** | Data, growth, modern brands | "abstract flowing ribbons and soft gradient mesh in tonal blues, precise geometric accents, clean studio light" | Without a concept it reads as wallpaper. Tie it to the idea. |
| **Product and UI-led** | Fintech, SaaS, apps | "a clean app screen or card as the hero, shown as a crisp object with soft realistic depth and daylight shadows, brand shapes around it, contemporary and uncluttered" | Never show real numbers or returns. Keep the UI abstract and legible. |
| **Cinematic and epic** | Entertainment, gaming, some festival work only | "cinematic light, volumetric rays, atmospheric haze, epic scale" | It drifts into fantasy or spiritual scenes. Never use it for finance, health, SaaS or corporate brands. |

## Phrases that cause flat, generic output (don't use them unless the user asks)
"flat", "solid background", "simple geometric shapes", "no gradients", "no 3D", "minimal illustration", "icon", "clip-art", "leave empty", "plain".

## Phrases that raise the quality bar
"art-directed", "polished, high detail", "award-level finish", "considered typographic hierarchy", "depth and dimension", "premium brand campaign", "contemporary", "grounded, real-world".

## Phrases that cause genre drift (use only where the industry fits; see `guides/industry-lens.md`)
"cinematic", "epic", "monumental", "volumetric rays", "god-rays", "haze", "mist", "ethereal", "mystical", "portal", "doorway of light", "ancient stone", "dust particles in the light". These turn a fintech or corporate poster into a fantasy or afterlife scene.

## Category clichés (never the hero unless transformed into a brand-owned device)
- **Finance:** rising bars, arrows, upward chart lines, coins, cash, rockets, piggy banks, handshakes, lighthouses, compasses, generic glowing cards floating on a gradient.
- **B2B tech:** globes of glowing dots, circuit boards, padlocks, handshakes.
- **Health:** stethoscopes on white, glowing DNA helixes.
- **Education:** mortarboards, apples, rocket ships.
Name them in the answer, steer away with a specific positive hero, and keep the prompt's Avoid line generic ("no stock finance imagery").

## Regulated categories (finance, health, alcohol)
- Keep compliance text (disclaimers, warnings) out of the image and set it as real type afterwards. Reserve a calm zone for it in the plate. For a category and market covered by `guides/regulated.md`, its section lists the mandatory elements.
- No promised returns, no figures, no celebrities, no faces of real people.
- Concepts should suggest growth or opportunity without implying a guaranteed outcome.
