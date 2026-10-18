# Capture checklist by domain

Use the section that matches the work. Skip items that don't apply; never invent them.

## Software (backend, scripts, full apps)
- Original requirement and any clarifications
- Stack and why it was chosen (or that it was dictated)
- Architecture: main components, data flow, external services
- Files created/changed (`git diff --stat`), and the 2–4 most instructive snippets
- Commands to install, run, test
- Tests/checks that proved it works
- Errors hit: exact message → root cause → fix
- Security/secrets handling (redact values, keep the pattern)
- What was deliberately left out (scope cuts) and why

## Frontend / UI
- Audience and primary action
- Design inputs: brand colors, fonts, references, the "avoid" list
- Iterations: what feedback changed the design (before/after screenshots if small)
- Responsive and accessibility checks done
- Prompts that produced the best layout

## Image generation / editing
- Purpose and where the image is used (size/aspect)
- Model and settings (quality, size, background, number of variants)
- Every prompt in order with the outcome of each (kept / rejected and why)
- The final prompt verbatim, annotated: subject, composition, style, lighting, text, constraints
- Reference images used (describe, don't embed large files)
- Post-processing outside the model

## Video generation
- Purpose, platform, duration, aspect ratio
- Model and settings (resolution, duration, seed, reference/first frame)
- Shot list / storyboard and the per-shot prompts
- Iterations: what changed between attempts (camera, action, lighting) and why
- Audio/dialogue/voiceover approach, editing and assembly steps
- Cost per clip and number of attempts (big efficiency lever)

## Writing / documents
- Audience, goal, voice samples used
- Outline → draft → revisions: what each revision fixed
- Sources and fact-checking done

## Data / analysis / research
- The question and the decision it served
- Data sources, cleaning steps, definitions
- Methods and why; checks for errors
- Findings and their caveats; charts produced
- Sources cited (research)

## Always
- Models and effort used per phase
- Rough time and number of attempts/retries
- The single most important insight for the next person
