# ai-knowhow

**Know how it was built. Know what to build it with.**

Two open-source agent skills for anyone who builds with AI: apps, images, videos, documents, analyses.

| Skill | The problem | What it does |
|---|---|---|
| **[modelwise](plugins/modelwise/)** | Everyone uses one model for everything, with a one-line prompt, and overpays. | You type a basic prompt. It tells you **which model** (Anthropic or OpenAI), **which effort level**, roughly **what it costs**, and gives you a **structured prompt** written the way that model works best, plus how to save tokens on this kind of task. |
| **[retrace](plugins/retrace/)** | AI builds the thing and it ships, but nobody learns *how*. | After a task, it captures the goal, the decisions and *why*, the prompts that worked, the mistakes and fixes, and the cheaper path next time, as a **lesson skill**. Anyone can invoke the lesson later and be **taught**, step by step. |

They work in **Claude Code, claude.ai, OpenAI Codex and ChatGPT**, because they're plain [Agent Skills](https://agentskills.io) (Markdown + JSON + one small stdlib-only Python script).

```
 basic prompt ──► modelwise ──► model + effort + cost + structured prompt + token tips
                     │
                     └── reads registry/  (60 model cards built from official Anthropic & OpenAI docs)

 finished work ──► retrace ──► lesson-<slug>/ (SKILL.md + lesson.md) ──► /lesson-<slug> teaches a human
```

---

## Install

### Claude Code (recommended)
```
/plugin marketplace add YOUR-GITHUB-USERNAME/ai-knowhow
/plugin install modelwise@ai-knowhow
/plugin install retrace@ai-knowhow
/reload-plugins
```
Or copy the skills without the plugin system:
```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/ai-knowhow.git && cd ai-knowhow
python3 tools/install.py claude-code          # ~/.claude/skills/  (add --project for ./.claude/skills/)
```

### Other tools
| Tool | How |
|---|---|
| **claude.ai** | `python3 tools/install.py zip`, then upload the ZIPs under Customize → Skills ([details](adapters/claude-ai/README.md)) |
| **OpenAI Codex** | `python3 tools/install.py codex` ([details](adapters/codex/README.md)) |
| **ChatGPT** | Workspace plugin import, skill upload, or a Project with our instructions file ([details](adapters/chatgpt/README.md)) |

---

## Use it

### modelwise
```
/modelwise landing page for my bakery
/modelwise extract invoice number, date and total from 20,000 PDFs, cheapest way
/modelwise why is my Next.js build failing after upgrading to v16
```
(As a plugin skill it's also available as `/modelwise:modelwise`. You can also just ask: *"which model should I use for…"*.)

You get:

```
## Recommendation
Model:  Claude Sonnet 5.5 (claude-sonnet-5-5, anthropic): everyday frontend work at a fifth of Opus cost
Effort: medium (E3). API: output_config.effort=medium · Claude Code: /effort medium
Est. cost per run: $0.28 (list price, before caching/batch)
Cheaper: claude-haiku-5-5 @ medium   Stronger: claude-opus-5-5 @ high
Best OpenAI option: gpt-6.1-sol @ medium

## Your structured prompt
<context>…</context> <task>…</task> <design>… Do not use: pill buttons, gradient blobs …</design> …

## Save tokens on this task
- Put design tokens in the system prompt once; iterate with screenshots + "change X"

## Why this works
…
```

You can run the router on its own:
```bash
python3 plugins/modelwise/skills/modelwise/scripts/route.py --task code.frontend --complexity moderate
python3 plugins/modelwise/skills/modelwise/scripts/route.py --list-tasks
```

### retrace
At the end of any task:
```
/retrace            (or: "make a lesson from what we just did")
```
It writes `.claude/skills/lesson-<slug>/`. Commit it, and your whole team can run `/lesson-<slug>` to be walked through how it was built: overview, step-by-step with check questions, or a hands-on rebuild. `/retrace:teach` lists and teaches any lesson.

See a real one: [examples/lessons/lesson-building-ai-knowhow](examples/lessons/lesson-building-ai-knowhow/lesson.md), the lesson for how this repo was built.

---

## Which model should run these skills?
Your tool's selected model runs the skill, and we can't control that. The skills read data and fill templates, so you don't need a frontier model:

| | Recommended | Budget |
|---|---|---|
| **Claude** (Claude Code, claude.ai) | Claude Sonnet 5.5 @ low effort | Claude Haiku 5.5 |
| **OpenAI** (ChatGPT, Codex) | GPT-6.1 Sol @ low effort | GPT-6 Luna |

The answer doesn't depend on the model's own knowledge. All model facts come from the registry, so a cheaper model gives the same recommendation.

## What's in the registry (Phase 1: Anthropic + OpenAI)
- **60 model cards**: every current, previous, legacy and deprecated Claude and OpenAI model still served, plus image and audio models. Each card has capabilities, context, price, effort levels and defaults, fit ratings per task, prompting tips, and sources, with a `verified` date.
- **21 task types** with effort per complexity, from quick code to long-running agents, images, video and voice.
- **15 prompt templates** with slots, a universal skeleton, Claude and OpenAI renderings, a worked example, and token savers.
- **One normalized effort scale** (E0 to E6) mapped to Claude's `output_config.effort`, OpenAI's `reasoning.effort`, and the in-app settings of Claude Code, claude.ai, ChatGPT and Codex.

Fit ratings are curated judgments built from vendor docs. They are not benchmark scores. Prices are list prices for comparison. Always check the vendor's page before committing to a budget.

**Current gaps:** no video generator is listed. OpenAI shut down the Sora 2 API on 2026-09-24 and Anthropic doesn't generate video. Modelwise still writes a full video prompt. Phase 2 adds Google (Gemini, Veo) and other vendors.

## How it stays current
- `tools/watch_models.py` runs weekly in GitHub Actions. It checks Anthropic's and OpenAI's model pages for IDs the registry doesn't know, and opens an issue.
- A human updates the card from the official docs, then runs `python3 tools/validate.py --fix`, and CI checks it.
- See [CONTRIBUTING.md](CONTRIBUTING.md).

## Repo layout
```
.claude-plugin/marketplace.json     Claude Code / claude.ai / ChatGPT marketplace
.agents/plugins/marketplace.json    Codex marketplace
plugins/modelwise/skills/modelwise/ SKILL.md · registry/ · templates/ · guides/ · scripts/route.py · ROUTING_TABLE.md
plugins/retrace/skills/retrace/     SKILL.md · templates/ (lesson + lesson skill) · guides/capture-checklist.md
plugins/retrace/skills/teach/       SKILL.md
examples/lessons/                   example lessons
adapters/                           per-platform install notes (ChatGPT, Codex, claude.ai)
tools/                              validate.py · test_route.py · install.py · watch_models.py
docs/architecture.md                how it fits together
```

## License
MIT. Not affiliated with Anthropic or OpenAI. Model names are their owners' trademarks.
