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

## Token & cost savers
- **Draft at low quality** (and with the faster model) until composition is right, then render the final once at high.
- One change per edit turn. Big multi-change edits cause re-rolls.
- Batch API halves the price of image output for non-urgent bulk jobs.
- Generate several variants (`n`) in one call rather than many separate calls.
