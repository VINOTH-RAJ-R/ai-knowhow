# Template: video generation (video.generate)

**Status (2026-10):** neither vendor in this registry currently offers a video generator. OpenAI shut down the Sora 2 API on 2026-09-24, and Anthropic does not generate video. This template still gives you a strong, generator-agnostic prompt and shot list (it's based on OpenAI's archived Sora guide, which applies to most text-to-video tools). Recommendations for specific generators (Google Veo, Runway, Kling, Luma, etc.) are planned for phase 2. Use the text model from the routing to write and refine the prompt.

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| PURPOSE | Ad, b-roll, explainer, social short, music video | Ask |
| PLATFORM | Aspect ratio and length: 9:16 Reels/TikTok, 16:9 YouTube, 1:1 | Ask |
| DURATION | Total length and number of shots | Short clips (4-8s each) |
| STORY | What happens, beginning → end | (required) |
| SUBJECT | Who/what is on screen; keep a consistent description | (required) |
| LOOK | Visual style, era, color palette (3-5 color anchors), film stock | Natural, cinematic |
| CAMERA | Per shot: framing, angle, one movement, lens | Per shot |
| LIGHT | Light sources and direction, kept consistent across shots | Soft key light |
| SOUND | Dialogue (short lines, labeled speakers), ambience, music | Ambience only |
| REFERENCE | First-frame image or reference images | None |

## Per-shot prompt skeleton
```
[Prose description of the scene: where we are, who is there, what it feels like]

Cinematography:
  Camera shot: <framing + angle, e.g. "medium close-up, low angle">
  Movement: <ONE move, e.g. "slow dolly-in">
  Lens: <e.g. "35mm, shallow depth of field">
  Mood: <...>
Lighting: <sources, direction, color temperature>
Palette: <3-5 color anchors>
Actions (beats):
  - <beat 1, with timing, e.g. "0-2s: she lifts the cup">
  - <beat 2>
Dialogue:
  <SPEAKER>: "<short line>"
Background sound: <ambience / music cue>
Style: <film stock / era / animation style>
```
Set duration, resolution and aspect ratio in the generator's **settings**, not in the prompt text.

## Rules that work across generators
- **One camera move, one subject action, one lighting recipe per shot.** Complex shots misfire.
- **Shorter clips follow instructions better.** Two stitched 4-second shots often beat one 8-second shot.
- **Keep continuity**: repeat the exact subject description, palette and light sources in every shot.
- **Iterate one variable at a time.** If a shot misfires, simplify it, then add complexity back.
- Use a first-frame/reference image to lock the look of a character or product.

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "a 15 second ad for my running shoes"
**Structured shot list (9:16, 3 shots × 5s):**
1. *Dawn street*: a runner's feet in neon-green shoes hitting wet asphalt. Camera: ground-level close-up, tracking alongside. Light: blue pre-dawn with orange streetlamp rim light. Beats: 0-2s stride, 2-5s splash in a puddle in slow motion.
2. *Bridge*: the runner crosses a city bridge as the sun rises. Camera: wide shot, slow crane up. Palette: deep blue, sunrise orange, neon green. Beats: steady run, sun flares behind.
3. *Product*: the shoe rotates on a wet black surface. Camera: macro, slow orbit. Text overlay added in editing, not generated: "RUN BEFORE THE CITY WAKES."

## Token & cost savers
- Lock the script and shot list with a cheap text model before spending on video generation. Video is by far the most expensive modality per attempt.
- Generate the cheapest preview resolution and shortest duration first; upscale and extend only the keepers.
- Add text overlays and music in editing, not in generation.
