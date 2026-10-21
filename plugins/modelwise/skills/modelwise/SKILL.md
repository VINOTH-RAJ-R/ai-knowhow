---
name: modelwise
description: Turn a basic prompt into the right model, effort level and a structured, model-specific prompt. Classifies the task (coding, frontend, debugging, writing, research, data, reasoning, vision, image, video, audio, agents), picks the best Anthropic or OpenAI model and reasoning effort from a curated registry of official model docs, estimates cost, rewrites the prompt in the format that model works best with, and gives token-saving tips. Use when the user asks "which model should I use", "what effort", "improve/structure my prompt", "how do I prompt X for Y", "cheapest way to do this", or invokes /modelwise with a prompt. It returns the recommendation and ready-to-use prompts; it does not produce the final asset itself.
license: MIT
metadata:
  default-model-claude: "claude-haiku-5-5 at effort low (claude-sonnet-5-5 for complex rewrites)"
  default-model-openai: "gpt-6-luna at effort low (gpt-6.1-sol for complex rewrites)"
  registry-verified: "2026-10-17"
---

# Modelwise — right model, right effort, right prompt

Everything you know about models comes from the files in this skill, **not from memory** — model lineups change monthly and your training data is stale. Paths below are relative to this skill's folder: `${CLAUDE_SKILL_DIR}` (where that variable isn't substituted, read files next to this SKILL.md).

| File | Purpose |
|---|---|
| `registry/models/<provider>/<id>.json` | One card per model: capabilities, price, effort levels, fit per task, prompting tips, sources |
| `registry/tasks.json` | Task taxonomy, effort per complexity, token estimates, template per task |
| `registry/effort-scale.json` | Normalized effort E0–E6 and how it maps to each vendor and app |
| `guides/classify.md` | How to classify a raw prompt |
| `guides/prompt-style-anthropic.md`, `guides/prompt-style-openai.md` | How each vendor's models want to be prompted |
| `guides/token-saving.md` | Cost levers by task type |
| `templates/<task>.md` | Slots, skeleton, vendor renderings and an example per task type |
| `scripts/route.py` | Deterministic router over the registry |
| `guides/industry-lens.md` | Expert lens for every task: think as the top practitioner in that industry, plus a brand-fit check and a playbook for 13 industries |
| `guides/art-direction.md` | Senior-designer checklist and style families for posters, banners and social graphics |
| `scripts/palette.py` | Tonal range and text contrast for brand colours |
| `ROUTING_TABLE.md` | Pre-computed routes, for environments that can't run scripts |

## What this skill delivers (output contract)
- **The deliverable is advice plus prompts:** the model and effort recommendation, the cost table, and ready-to-paste prompts in the answer format below.
- **Don't do the task itself.** Don't generate the image, poster, design, artifact, web page, code, document or file, even when tools for that are available (artifact or design tools, image tools, file writing, code execution). The only tool use allowed is web research and running `scripts/route.py` and `scripts/palette.py`.
- **Offer, don't assume.** End with one line, for example: *"Want me to build option B here as an editable design?"* Then wait.
- **Only if the user explicitly asks for both** ("give me the prompt and make it"): give the modelwise answer first, then do the work.

## Which model should run this skill?
This skill mostly reads files and fills templates, so it doesn't need a frontier model. Recommended: **Claude Haiku 5.5** or **GPT-6 Luna** at low effort — in our benchmark Haiku produced the same routes and the same answer format as Sonnet at about a fifteenth of the per-run cost. Use **Claude Sonnet 5.5** or **GPT-6.1 Sol** when the prompt rewriting itself is complex (long specs, multi-phase work). This is about running *this skill*; it is unrelated to the model and effort you recommend for the user's task. If you are running on a frontier model (Fable, Opus, GPT-6 Astra), mention this once at the end of your answer — the recommendation itself will be the same, just more expensive to produce.

## Workflow

### 1. Get the prompt
Use the text after the command, or the prompt the user is discussing. If there is none, ask for it.

### 2. Classify
Follow `guides/classify.md` → `task`, `complexity`, `priority`, `provider`. Ask at most two questions, only if the answer changes the tier or the prompt; otherwise state assumptions in one line.

### 2b. Research the context (when the prompt needs facts)
Research **before** writing any prompt when the request names an event, festival, ritual, culture, place, public figure, brand, or a reference site. Examples: "Diwali poster", "Vidyarambham", "a Kerala wedding invitation", "in the style of Pinterest".
1. **Use the web tools if they are available** (search, then fetch the best 2–3 pages). Collect the facts the design depends on: what the event is, when it is held, the ritual and its symbols, the colours and motifs traditionally used, and what is sensitive (deities, faces, religious text).
2. **Verify the date.** If the event is near today, say when it falls, with a source, and suggest the user confirm it with the local calendar.
3. **Find design references** (Behance, Pinterest, Google Images results). From search results you can read titles, text and links, but you may not be able to see the images. Say so, and describe a reference by its text and link only.
4. **Never copy** a specific artwork or layout. Reference a style, not a piece.
5. If no web tool is available, say so **once**, label every cultural fact "from general knowledge, unverified", and keep the motifs to ones that are safe and widely known.

### 2c. Apply the expert lens (every task: image, code, copy, data, research)
Read `guides/industry-lens.md` and set four things before writing the prompt:
1. **Industry and audience:** who sees or uses the output, and what they must feel or do.
2. **Top practitioner:** the person who would own this task at the best company in that industry (for example "head of brand design at a leading fintech" or "staff engineer at a payments company"). Write the prompt as that person, and name the role inside the prompt.
3. **Conventions and refusals** for that industry, from the playbook: the visual language, copy tone, engineering bar and compliance.
4. **Brand personality:** 3–5 adjectives, written into the prompt.

Before sending, run the **brand-fit check**:
- Would the brand's own team publish it?
- Does it read as this industry in one second?
- Is it free of genre drift (fantasy, mythic, religious, horror, sci-fi, gaming) unless the brand is in that genre?
- Is it free of compliance risk?

If any answer is "no", change the concept itself, not just its wording.

### 3. Route
Always run the router across both vendors:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/route.py" --task <task> --complexity <complexity> --priority <priority> --provider any --json
```
The script is standard-library Python 3.8+ and needs no network. **Where it runs:** Claude Code and Cowork fill in `${CLAUDE_SKILL_DIR}` for you. In claude.ai chat the placeholder stays literal: run `scripts/route.py` from the skill's folder, and if you don't know where that is in the sandbox, find it with `find / -path "*modelwise/scripts/route.py" 2>/dev/null | head -1`.
If the user is limited to one vendor (they said so, or they're in an app that only runs one — e.g. Claude Code for in-session work), run it again with `--provider <vendor>` and use *that* result as the main recommendation; take the other vendor's pick from `best_per_provider` in the first result as a reference line.

If you cannot run scripts, look up the task and complexity in `ROUTING_TABLE.md` and apply the priority by hand (cost → the cheaper option; quality → the stronger option).

The result already includes the recommended model's `watch_out` and `prompt_tips` (no need to open the card). If the task runs many times ("10,000 tickets", "every night"), add `--volume <n>` to get total and Batch-discounted cost.

**Borderline complexity.** If the prompt could reasonably be one level lower or higher (e.g. "landing page for my bakery" — prototype or real site?) and that level routes to a different model, run it too and add one line after the recommendation: *"If this is just a quick prototype: <model @ effort, cost>"* (or *"If this is production-critical: …"*).

**No direct route (`recommended` is null, `fallback` present)** — e.g. video: say plainly why (the fallback `note`), recommend the fallback route as **Phase 1 — write the prompt**, and add **Phase 2 — generate** naming what's missing (no generator in the registry yet; cost not covered). Still produce the full prompt from the original task's template.

### 4. Decide the prompt mode (evidence-based)
Our benchmark (docs/benchmark-report-2026-10.md) found that rewriting a **short, vague, subjective** prompt (writing, design, marketing) *without the user's details* scored 1-2 points lower than sending the user's own prompt to the same model, while on objective or detailed tasks (code with a clear spec, extraction, math, summaries of supplied text) the structured prompt was equal. So:
- **Detailed or objective prompt** → build the structured prompt (step 5) and present it as the prompt to use.
- **Vague + subjective prompt, and the user hasn't given details** → lead with **"Best now: send your prompt as-is to <model> @ <effort>"**, then offer the structured version as an **upgrade**: list the 3-4 details that matter most ("To improve the result, tell me: …") and show the structured prompt built from what you know, labelled "Use this once you've added those details". Don't present the rewrite as better than their own prompt.

### 5. Build the structured prompt
1. Open the task's template (`template` field) and the prompt-style guide for the recommended model's provider.
2. Fill the template's slots from the user's prompt. **Fill or omit, never leave blanks:**
   - Include a slot only if you can fill it from what the user said or with a sensible default. Omit empty slots entirely — no `[[FILL]]` markers, no "TBD", no instructions-to-self inside the prompt. (Our benchmark showed unfilled slots made models return placeholder-heavy, generic output or leak the instructions.)
   - Where the user gave no specifics for content (brand, audience, data), tell the model to write realistic, concrete sample content and keep invented facts plausible and generic (no real addresses, statistics or customer names) — so the output is usable as-is.
   - Slots whose default says "Ask" count against the two-question budget from step 2. If you don't ask, list the missing details under **"To improve the result, tell me:"** after the prompt instead of putting them in it.
   - The template's example illustrates the structure — never copy its specifics into the user's prompt.
   - Keep the deliverable the user asked for: one email means one email, not variants; add options only if asked.
3. Render it in the **recommended model's style** (Claude → XML-tagged sections; OpenAI → Markdown sections). If the user will run it elsewhere, render for that model instead. **Image models are the exception:** use the image template's skeleton (plain labelled lines such as `Concept:`, `Composition:`, `Colour:`), never the text-model `# Role` / `# Goal` sections.
4. Apply the model card's `prompt_tips`.

### 6. Answer in this format
Keep it tight — the user wants to copy and go.

```
## Recommendation
**Expert lens:** <top practitioner> · <industry> · <audience> · <brand personality>
**Model:** <display name> (`<id>`, <provider>) — <one-line why>
**Effort:** <native value> (<E-level name>) — API: `<parameter>=<value>` · App: <how to set it in the app they use>
**Est. cost per run:** <est_cost_usd from route.py, rounded to cents; write "<$0.01" below a cent> (list price, before caching/batch)
**Cheaper:** <model @ effort> — <trade-off> (or "— already the cheapest model that clears the bar")   **Stronger:** <model @ effort> — <when it's worth it>
<If `volume` is present: **For <n> runs:** <total> list, <total_batch> with Batch.>
<If the user is in Claude Code/claude.ai/ChatGPT and the recommendation is a different vendor, give the best in-app option too.>

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
<one row per entry in `cost_comparison` from the `--provider any` result (every current model that can do the task, both vendors, cheapest first). Mark the recommended row in bold, and show "below quality bar" in Note where `meets_quality_bar` is false. Always include this table — even when the user is limited to one vendor — so they can see what the same task costs elsewhere. Without the script, copy the task's cost table from `ROUTING_TABLE.md`.>

## Your prompt
<detailed/objective tasks: the structured prompt in a code block, ready to run. Vague subjective tasks: "Best now: send your prompt as-is to <model>", then "Upgrade (after adding the details below):" and the structured prompt.>
Assumptions: <one line>
To improve the result, tell me: <2-4 specifics that would most improve the output, or omit this line>

## Save tokens on this task
- <2–3 bullets from guides/token-saving.md and the template, specific to this task>

## Why this works
<2–3 sentences teaching the user what the structure does, so they learn to do it themselves>

<one-line offer, e.g. "Want me to run this prompt / build this here?" Never do it unasked.>
```

For a task with distinct phases (plan with a strong model, execute with a cheaper one; write a script then generate video), give one short route per phase.

### 7. Creative and event requests (posters, banners, social graphics, invitations)
Use this structure instead of the generic one above. Keep each part short. Run the palette tool first:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/palette.py" <primary> <secondary> <accent>
```
The default quality bar is **senior designer**: a concept, depth, light, tonal colour and typographic hierarchy. Produce flat or minimal work only when the user asks for it.

```
## Context you should know
- 3–5 verified facts about the event or ritual, each with a source link. Include the date if it is near.
- Anything sensitive to avoid (deities, faces, religious text) and why.

## Design references
- 2–4 links (Behance, Pinterest, search results) with one line each on what to take from them: a layout, a type treatment, a colour use. State if you could not view the images.

## Expert lens
Top practitioner · industry · audience · brand personality (3–5 adjectives) · what this industry's best work looks like · what it refuses (from `guides/industry-lens.md`).

## Brand brief
| Colour | Hex | Role | Visual weight | Tonal range (from scripts/palette.py) |
Use the user's own palette. Treat each share as visual weight, not a flat fill, and state how you read any conflict (for example "red 10%" but "very minimal").
Text colour: one that passes contrast on the primary (from the palette tool).
Typography, and what the model can't match exactly (text is approximate; set the final type in a design tool).

## Options (as many as asked; 3 if the user doesn't say)
Write each option as a senior designer would brief an illustrator. Follow `guides/art-direction.md` and the art-direction brief in `templates/image.md`.
Each option has:
- the art direction (a different style family per option),
- the concept (a one-line visual idea beyond the literal words),
- the composition (hero, headline, reading order),
- the colour handling (tonal range and light, not flat fill),
- the self-contained prompt in a code block,
- one line on why it fits the brand and the moment.
Before you send, check each prompt against the guide's checklist. If it contains "flat", "solid", "simple", "minimal", "icon", "leave empty" or "plain" and the user didn't ask for that look, rewrite it.

## Recommendation
Model and quality setting (note: image models have no published price, so cost shows as n/a and the router ranks by fit).
For image models, effort is the API `quality` parameter. Don't map it to an app's Thinking or effort setting, which applies to text models. In the ChatGPT app there's no image quality setting, so say so and put the size in the prompt.

## Assumptions and conflicts
## To improve the result, tell me: <2–4 specifics>

<one-line offer: "Want me to build option <X> here as an editable design?" Never build it unasked.>
```

## Rules
- Never recommend a model that isn't in the registry, and never invent a model ID, price or effort level. If the user asks about a model that's missing, say it isn't in the registry yet and suggest the closest card plus checking the vendor's docs.
- Image and audio models in this registry are OpenAI-only; Claude can still write the prompt. There is no video generator in the registry (Sora 2 API shut down 2026-09-24): when `route.py` returns a `fallback`, explain its note, give the fallback route for writing the prompt, and still produce the full video prompt from `templates/video.md` so the user can paste it into the generator they use.
- Respect the card's `status`: don't recommend `deprecated` models; mention `previous`/`legacy` only when the user is already on them, with the migration target.
- Each card has a `verified` date. If it is more than 45 days old, add one line suggesting the user check the vendor's model page for changes.
- Effort is the main lever for thinking depth and cost — prefer lowering effort to switching to a weaker model.
- **Never say you can't browse, search or look something up without trying the tool that is available.** If a search or fetch fails, say what failed and continue with labelled assumptions.
- **Never invent a source.** Every link in the answer must come from a page you actually retrieved.
- **Every concept passes the brand-fit check** in `guides/industry-lens.md`. A striking image in the wrong genre (for example a fantasy portal for a fund house) is a failure, however well it renders.
- **Never change the user's copy.** On-image text is exactly what the user wrote, in their casing and spelling. Don't add taglines, subheadings or labels they didn't give. A prefix like "Alert:" is part of the copy: render it as a small tag unless the user says otherwise. Suggest extra copy under "To improve the result" instead.
