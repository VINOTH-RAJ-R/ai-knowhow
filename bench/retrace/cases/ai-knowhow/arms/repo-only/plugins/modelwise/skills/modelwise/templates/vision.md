# Template: understanding images, screenshots, PDFs (vision.understand)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| INPUT | Image/PDF type: invoice, chart, UI screenshot, diagram, photo | (required) |
| ASK | What to extract or decide | (required) |
| PRECISION | Exact numbers vs gist | Exact for documents, gist for photos |
| OUTPUT | Fields (JSON), table, description, answer | Depends on ASK |

## Universal skeleton
```
INPUT: <type>, attached.
ASK: <...>
PRECISION: <...> If something is unreadable, say so instead of guessing.
OUTPUT: <...>
```

## Rendered for Claude
Place images/PDFs **before** the text instruction.
```xml
[image or PDF attached first]
<task>ASK</task>
<requirements>PRECISION. Mark unreadable values as null with a note.</requirements>
<output_format>OUTPUT</output_format>
```
For dense charts or technical drawings, give the model a crop/zoom or code tool. This helps more than raising effort.

## Rendered for OpenAI
```markdown
[image attached]
Task: ASK
Precision: PRECISION. Unreadable → null.
Output: OUTPUT
```
Use `detail: "high"` for small text or dense documents.

## Token savers
- Images cost tokens by pixel area. **Downscale** to what the task needs (≈1280×720 is plenty for most screenshots).
- Crop to the relevant region instead of sending the full screen.
- For many PDFs, use the Files API once and reference by id instead of re-uploading.
