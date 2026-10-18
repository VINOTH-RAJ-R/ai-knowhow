---
name: modelwise
description: Turn a basic prompt into the right model, effort level and a structured, model-specific prompt. Classifies the task (coding, frontend, debugging, writing, research, data, reasoning, vision, image, video, audio, agents), picks the best Anthropic or OpenAI model and reasoning effort from a curated registry of official model docs, estimates cost, rewrites the prompt in the format that model works best with, and gives token-saving tips. Use when the user asks "which model should I use", "what effort", "improve/structure my prompt", "how do I prompt X for Y", "cheapest way to do this", or invokes /modelwise with a prompt.
license: MIT
metadata:
  default-model-claude: "claude-sonnet-5-5 at effort low"
  default-model-openai: "gpt-6.1-sol at effort low"
  budget-model-claude: "claude-haiku-5-5"
  budget-model-openai: "gpt-6-luna"
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
| `ROUTING_TABLE.md` | Pre-computed routes, for environments that can't run scripts |

## Which model should run this skill?
This skill mostly reads files and fills templates, so it doesn't need a frontier model. Recommended: **Claude Sonnet 5.5 at low effort** or **GPT-6.1 Sol at low effort** (budget: Claude Haiku 5.5 / GPT-6 Luna). This is about running *this skill*; it is unrelated to the model and effort you recommend for the user's task. If you are running on a frontier model (Fable, Opus, GPT-6 Astra), mention this once at the end of your answer — the recommendation itself will be the same, just more expensive to produce.

## Workflow

### 1. Get the prompt
Use the text after the command, or the prompt the user is discussing. If there is none, ask for it.

### 2. Classify
Follow `guides/classify.md` → `task`, `complexity`, `priority`, `provider`. Ask at most two questions, only if the answer changes the tier or the prompt; otherwise state assumptions in one line.

### 3. Route
Always run the router across both vendors:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/route.py" --task <task> --complexity <complexity> --priority <priority> --provider any --json
```
The script is standard-library Python 3.8+ and needs no network. **Where it runs:** Claude Code and Cowork fill in `${CLAUDE_SKILL_DIR}` for you. In claude.ai chat the placeholder stays literal: run `scripts/route.py` from the skill's folder, and if you don't know where that is in the sandbox, find it with `find / -path "*modelwise/scripts/route.py" 2>/dev/null | head -1`.
If the user is limited to one vendor (they said so, or they're in an app that only runs one — e.g. Claude Code for in-session work), run it again with `--provider <vendor>` and use *that* result as the main recommendation; take the other vendor's pick from `best_per_provider` in the first result as a reference line.

If you cannot run scripts, look up the task and complexity in `ROUTING_TABLE.md` and apply the priority by hand (cost → the cheaper option; quality → the stronger option).

Then open the recommended model's card (`card` field in the result) and read its `watch_out` and `prompt_tips`.

**Borderline complexity.** If the prompt could reasonably be one level lower or higher (e.g. "landing page for my bakery" — prototype or real site?) and that level routes to a different model, run it too and add one line after the recommendation: *"If this is just a quick prototype: <model @ effort, cost>"* (or *"If this is production-critical: …"*).

**No direct route (`recommended` is null, `fallback` present)** — e.g. video: say plainly why (the fallback `note`), recommend the fallback route as **Phase 1 — write the prompt**, and add **Phase 2 — generate** naming what's missing (no generator in the registry yet; cost not covered). Still produce the full prompt from the original task's template.

### 4. Build the structured prompt
1. Open the task's template (`template` field) and the prompt-style guide for the recommended model's provider.
2. Fill the template's slots from the user's prompt. Slots whose default says "Ask" count against the two-question budget from step 2; when you don't ask, use `[[FILL: …]]`. The template's example is an illustration of the structure — never copy its specifics (names, places, colors, prices) into the user's prompt.
    For missing slots: use the template's default and list it as an assumption, or leave a clear `[[FILL: what's needed]]` placeholder when a guess would be wrong (brand colors, real data, exact numbers).
3. Render it in the **recommended model's style** (Claude → XML-tagged sections; OpenAI → Markdown sections). If the user will run it elsewhere, render for that model instead.
4. Apply the model card's `prompt_tips`.

### 5. Answer in this format
Keep it tight — the user wants to copy and go.

```
## Recommendation
**Model:** <display name> (`<id>`, <provider>) — <one-line why>
**Effort:** <native value> (<E-level name>) — API: `<parameter>=<value>` · App: <how to set it in the app they use>
**Est. cost per run:** <est_cost_usd from route.py, rounded to cents; write "<$0.01" below a cent> (list price, before caching/batch)
**Cheaper:** <model @ effort> — <trade-off>   **Stronger:** <model @ effort> — <when it's worth it>
<If the user is in Claude Code/claude.ai/ChatGPT and the recommendation is a different vendor, give the best in-app option too.>

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
<one row per entry in `cost_comparison` from the `--provider any` result (every current model that can do the task, both vendors, cheapest first). Mark the recommended row in bold, and show "below quality bar" in Note where `meets_quality_bar` is false. Always include this table — even when the user is limited to one vendor — so they can see what the same task costs elsewhere. Without the script, copy the task's cost table from `ROUTING_TABLE.md`.>

## Your structured prompt
<the rendered prompt in a code block, ready to paste>
Assumptions: <one line>

## Save tokens on this task
- <2–3 bullets from guides/token-saving.md and the template, specific to this task>

## Why this works
<2–3 sentences teaching the user what the structure does, so they learn to do it themselves>
```

For a task with distinct phases (plan with a strong model, execute with a cheaper one; write a script then generate video), give one short route per phase.

## Rules
- Never recommend a model that isn't in the registry, and never invent a model ID, price or effort level. If the user asks about a model that's missing, say it isn't in the registry yet and suggest the closest card plus checking the vendor's docs.
- Image and audio models in this registry are OpenAI-only; Claude can still write the prompt. There is no video generator in the registry (Sora 2 API shut down 2026-09-24): when `route.py` returns a `fallback`, explain its note, give the fallback route for writing the prompt, and still produce the full video prompt from `templates/video.md` so the user can paste it into the generator they use.
- Respect the card's `status`: don't recommend `deprecated` models; mention `previous`/`legacy` only when the user is already on them, with the migration target.
- Each card has a `verified` date. If it is more than 90 days old, add one line suggesting the user check the vendor's model page for changes.
- Effort is the main lever for thinking depth and cost — prefer lowering effort to switching to a weaker model.
