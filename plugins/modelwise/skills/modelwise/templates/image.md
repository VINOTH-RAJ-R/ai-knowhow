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
**Basic:** "make an image for my coffee shop instagram"
**Structured:**
```
Use: Instagram feed post (square) announcing a new autumn drink.
Scene: Rustic wooden café counter, blurred warm café interior behind.
Subject: A tall glass of iced pumpkin-spice latte with visible layers of espresso and milk, cinnamon dusting on top.
Details: Small orange maple leaves and two cinnamon sticks beside the glass; condensation on the glass.
Style: Photorealistic product photograph, shallow depth of field.
Lighting & mood: Golden late-afternoon window light from the left; cozy, inviting.
Camera: 45-degree angle, close-up, 85mm lens look.
Text: "AUTUMN IS BACK" in bold white sans-serif, top center, once. No other text.
Constraints: No logos, no people, no watermark.
```
Parameters: `size=1024x1024`, `quality=medium`, model per routing (Flare for drafts, Sunburst for the final).

## Poster, festive and social graphics (no logo, text in the image)

Use this when the request is a poster, festival post or social graphic with a heading and subheading. Read the research step first (SKILL.md 2b) and fill the slots from verified facts.

| Slot | Fill with |
|---|---|
| FORMAT | Exact size and use, e.g. "square 1:1 Instagram feed post, 1024×1024". |
| EVENT FACT | One verified sentence on what the event is and why it is held. It shapes the motifs; it is not printed unless asked. |
| LAYOUT | Three zones, top to bottom: heading zone, hero zone, subheading zone. Say where each sits and how much space it leaves. |
| PALETTE | Each colour as hex, role and share of area: e.g. "blue #0a4e9b, base background, ~80%". Describe red and green as accents if their share is small. |
| MOTIFS | 3–5 objects from the verified ritual or tradition. Name only what is safe to depict. |
| TYPE | The exact text, quoted, with its position. Say "clean geometric sans-serif, bold for the heading". |
| AVOID | No logo, no wordmark, no watermark, no extra text, no faces of real people, no deities unless asked. |

**Skeleton**
```
Create a square 1:1 image for a <use>.
Layout: top zone for the heading; middle zone for the hero illustration; bottom zone for the subheading. Leave generous margins.
Background: <colour and hex>, <share> of the canvas.
Hero: <scene and motifs>, in a <style>.
Accents: <colour and hex>, only as <role>, at about <share>.
Text, exactly as written, nothing else: "<heading>" (bold, white, top zone). "<subheading>" (regular, <colour>, bottom zone).
Avoid: <AVOID>.
```

**Rules that prevent the common failures**
- **Text is approximate.** Image models misspell text and can't load a brand font. Keep on-image text short, spell it letter by letter, and tell the user the final type should be set in the real font in Canva or Figma.
- **Percentages describe area, not counts.** Write "about 80%" and say how you read any conflict between a percentage and a word.
- **Different options means different layouts.** Four colour swaps of one layout are not four options.
- **Motifs come from the research.** Never invent a ritual detail. If a script or symbol is needed (e.g. a Malayalam letter), say the image model may misdraw it and suggest overlaying it with real type.

## Token & cost savers
- **Draft at low quality** (and with the faster model) until composition is right, then render the final once at high.
- One change per edit turn. Big multi-change edits cause re-rolls.
- Batch API halves the price of image output for non-urgent bulk jobs.
- Generate several variants (`n`) in one call rather than many separate calls.
