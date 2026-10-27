# Template: image generation & editing (image.generate, image.edit)

In this registry, image models are OpenAI's GPT Image family. Claude can't generate images, but it can write this prompt for you.

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| USE | Where the image goes: ad, website hero, app icon, infographic, social post | Ask: drives size, style, text |
| SCENE | Setting/background | Simple, uncluttered |
| SUBJECT | Main subject and what it's doing | (required) |
| DETAILS | Materials, colors, props, clothing, expressions | Fill from context |
| STYLE | Photo / illustration / 3D / flat vector, plus medium, era, artist-free style words | Ask, or choose to match USE |
| LIGHT & MOOD | Lighting, time of day, mood | Soft natural light |
| CAMERA | Shot type, angle, lens (as style cues) | Eye-level medium shot |
| TEXT | Exact words in the image, font, placement | No text |
| CONSTRAINTS | Must-haves and must-nots | No watermark, no extra text |
| SIZE / QUALITY / BACKGROUND | API parameters, not prompt text | Square, quality from routing, opaque |
| EDIT: CHANGE / KEEP | For edits: the one change, and what must stay identical | (required for edits) |

## Prompt skeleton (generation)
```
Use: <USE>
Scene: <SCENE>
Subject: <SUBJECT>
Details: <DETAILS>
Style: <STYLE>
Lighting & mood: <LIGHT & MOOD>
Camera: <CAMERA>
Text: "<EXACT TEXT>" in <font style>, <placement>. No other text.
Constraints: <CONSTRAINTS>
```
API parameters: `size` (1024x1024, 1536x1024, 1024x1536, or custom with edges in multiples of 16), `quality` (from the routing), `background` (`transparent` needs png/webp), `n` for variants.

## Prompt skeleton (edit)
```
Image 1: <what it is>. [Image 2: <what it is, its role>]
Change only: <ONE change>.
Keep exactly the same: identity/face, pose, geometry, layout, lighting, camera angle, colors, background, everything else.
```
Repeat the "keep" list on every iteration, and make one change per turn.

## OpenAI's tips that matter
- Order: scene → subject → key details → constraints. Say the intended use.
- Say "photorealistic" / "real photograph" outright if that's what you want.
- Text: put it in quotes or ALL CAPS, say how many times it appears, and spell tricky words letter by letter. Use quality medium or higher for small text.
- Logos: flat, simple, scalable; ask for several options with `n`.
- UI mockups: describe the screen "as if it already exists".
- Transparent cut-outs: `background="transparent"` and describe no backdrop.

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "product photo of our iced latte for the website menu"
**Structured:**
```
Use: Website menu product photo (square) for an iced latte.
Scene: Rustic wooden café counter, blurred warm café interior behind.
Subject: A tall glass of iced pumpkin-spice latte with visible layers of espresso and milk, cinnamon dusting on top.
Details: Small orange maple leaves and two cinnamon sticks beside the glass; condensation on the glass.
Style: Photorealistic product photograph, shallow depth of field.
Lighting & mood: Golden late-afternoon window light from the left; cozy, inviting.
Camera: 45-degree angle, close-up, 85mm lens look.
Text: none. No words, numbers or logos anywhere.
Constraints: No logos, no people, no watermark.
```
Parameters: `size=1024x1024`, `quality=medium`, model per routing (Flare for drafts, Sunburst for the final).

## Posters, banners and social graphics (art-directed, text in the image)

Use this for any poster, banner, launch, alert or festival graphic. Read `guides/practice-design.md` first. It covers the creative director's brief, the category clichés, three territories that really differ, how to judge them, and how a studio produces the result. Then read `guides/art-direction.md`, which has the senior-designer checklist and the style families. Then run the palette tool on the brand colours:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/palette.py" <primary> <secondary> <accent>
```
It returns a tonal range for each colour and the text colours that pass contrast on the primary.

**Art-direction brief (fill every line; this is what makes the output look designed)**

| Line | What to write |
|---|---|
| FORMAT | Ratio, pixel size and use, e.g. "2:1 landscape banner, 1536×768, for LinkedIn and the website". |
| ART DIRECTION | The route's taste direction from `guides/creative-taste.md`, written as a craft recipe (light, lens, grade or film look, casting, set, materials) plus the style family. Not just "premium, cinematic, high detail". |
| EXPERT LENS | The top designer for this industry and 3–5 brand-personality words, from `guides/industry-lens.md` (e.g. "head of brand design at a leading fintech; trustworthy, clear, calm, modern"). |
| CONCEPT | One-line visual idea in the industry's own visual language, drawn from this brief (`guides/practice-design.md`), never from an example. Run the brand-fit check: no fantasy, mythic or spiritual scenes for corporate, finance or health brands. |
| COMPOSITION | Grid and placement: where the hero sits, where the headline sits, the reading order, and margins. The background runs edge to edge. Reserved zones are "kept clear of elements, still filled with the background". |
| COLOUR | Primary as dominant visual weight, written as a tonal range from the palette tool (shade hex → base → tint hex) with soft gradients and light. Accent for one named role. Secondary only as a tiny mark. Text colour that passes contrast. |
| HERO | Subject, material, rendering, light (key light direction, rim light, glow) and depth (foreground, midground, background). |
| TYPOGRAPHY | Each text in quotes, its role, size relative to the canvas, weight, tracking, alignment and line breaks. "Exactly these words, nothing else." |
| FINISH | Subtle grain, highlights, small supporting details that stay quiet. |
| AVOID | Generic only: "No logos unless asked, no watermark, no extra words or numbers, no stock imagery, no fantasy or mystical scenes, no faces of real people; the background fills the canvas edge to edge." Never name the specific motifs you want to keep out. |

**Skeleton**
```
Create a <ratio> <format> (<px>) for <use>. Designed as <top practitioner> for a <industry> brand that feels <personality words>. Art direction: <taste direction as a craft recipe: light source and direction, lens, grade or film look, casting, set and materials>, <style family>, art-directed. Signature detail: <the one specific, visible craft decision>.
Concept: <one-line visual idea in the industry's visual language>.
Composition: <hero placement>, <headline placement>, reading order <A → B → C>. Margins about 6–8% of the short edge. The background fills the entire canvas edge to edge; keep <zone> clear of elements but filled with the same background.
Colour: <primary> is the dominant colour (<the share the user gave, or "clearly dominant">), built as a tonal range from <shade> to <tint> with soft gradients and directional light, not a flat fill. <accent> for <role> (<user's share, or "restrained">). <secondary> <role and share>. Text in <text colour>.
Hero: <subject>, <material and rendering>, lit by <key light> with <rim light / glow>, with <foreground / midground / background layers>.
Typography: "<headline>" is the dominant element: <weight>, cap height about <x>% of the canvas height, tight tracking, <alignment and line breaks>. "<secondary text>" <role and size>. <Typeface style from the brand or the industry lens, e.g. "clean geometric sans-serif similar to <brand font>" or "refined serif">. Exactly these words, nothing else.
Finish: <subtle grain, highlights, supporting details>.
Avoid: <generic AVOID wording>.
```
Percentages, typefaces and margins come from the user's brand and the industry lens. Never reuse the example values in this template.

**Rules that prevent the common failures**
- **Colour is visual weight, not a flat fill.** Never write "solid", "flat" or "no gradients" unless the user asks for flat design. Use the tonal range.
- **Never write "leave empty" or "plain".** Models draw white bars. Write "kept clear of elements, still filled with the background".
- **Industry before style.** The concept and every style word must pass the brand-fit check in `guides/industry-lens.md`. A beautiful image in the wrong genre is a failure.
- **Keep the Avoid line generic.** Write "no fantasy or mystical scenes", not a list of the motifs you're trying to keep out (portals, mist, rays). Naming a motif can pull it into the image even inside an "avoid" list. Steer with the positive description instead.
- **Aspect ratio in apps.** Chat apps may ignore the requested size and return a square image. Put the ratio first in the prompt, check the result, and if it comes back square, ask the app to "extend to a 2:1 landscape canvas keeping everything else identical", or use the API `size` parameter.
- **Every option is a different territory.** Each pair of options differs on at least two axes: focal element (type-led, object-led, human-led, graphic-led), visual metaphor, tonal register, medium. Two "3D objects on a blue gradient" are one idea, whatever the material. Run the swap test from `guides/practice-design.md`.
- **The hero carries the concept and is not a category cliché.** Never make rising bars, arrows, coins, rockets or generic floating cards the hero of a finance graphic. Use a specific product, human or brand-device moment.
- **Brand colours are not a mood:** a dark or monochrome palette governs type and graphic elements. The image's mood comes from the industry and the offer (`SKILL.md` step 7).
- **Platform size first.** Use the channel's real size (LinkedIn 1.91:1 at 1200×628, Instagram feed 4:5, Stories 9:16). If the user asks for a ratio, use theirs and note any crop. The API size uses edges in multiples of 16 (2:1 → 1536×768).
- **Use only the user's copy, exactly.** Same words, same casing. No added taglines or subheadings. A label like "Alert:" becomes a small tag.
- **Keep the skeleton format.** Write image prompts as the labelled lines above, not as `# Role` / `# Goal` sections.
- **Text is approximate.** Image models misspell and can't load a brand font. Keep on-image text short, spell it exactly, and set the final type in the real font in Canva or Figma.
- **Check contrast.** Never use a text colour that fails contrast on its background. For example, a bright red on a mid blue is often below 2:1, so it can't be used for text. Check with `scripts/palette.py`.
- **Motifs come from the research** for events and cultures. Never invent a ritual detail.

## Production plate and layout spec (for the recommended option)
A studio doesn't ship text rendered by an image model. It generates a text-free plate and sets type, logo and legal copy in Figma or Canva.

**Plate skeleton.** Take the chosen option's prompt and change three lines:
```
Typography: none. This is a text-free background plate: no words, letters, numbers, logos, UI text or watermarks anywhere.
Kept clear (continuous background, nothing drawn there, low detail): the area <x–y% from left, y1–y2% from top>; the area <…>; the <corner> corner <size %>; the bottom band <height %>. Never call these zones, boxes, panels or placeholders: models draw them as rectangles.
Composition: <hero placement> so it never enters a reserved zone; key elements at least 5% inside every edge.
```
Keep every other line (format, art direction, concept, colour, hero, finish, avoid). The plate keeps the route's hero and its taste recipe; it is never a bare gradient. For text-heavy layouts (equations, lists, infographics), the layout lives in Figma, Canva or code, and the image model makes only a hero visual or a crafted backdrop.

**Layout spec** (a small table for the designer):

| Element | Exact text or source | Font, weight | Size (% of canvas height) | Position | Colour, contrast |
|---|---|---|---|---|---|

Include one row for each mandatory element the category requires (`guides/practice-design.md`, section 7). Ask the user for any value you don't have; never invent it.

## Token & cost savers
- **Draft at low quality** (and with the faster model) until composition is right, then render the final once at high.
- One change per edit turn. Big multi-change edits cause re-rolls.
- Batch API halves the price of image output for non-urgent bulk jobs.
- Generate several variants (`n`) in one call rather than many separate calls.
