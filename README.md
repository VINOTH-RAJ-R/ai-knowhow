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

> Publishing your own copy or testing before release? See [docs/publishing.md](docs/publishing.md) (all marketplaces, step by step) and [docs/testing.md](docs/testing.md) (end-to-end test plan).

### Claude Code (recommended)
```
/plugin marketplace add VINOTH-RAJ-R/ai-knowhow
/plugin install modelwise@ai-knowhow
/plugin install retrace@ai-knowhow
/reload-plugins
```
Or copy the skills without the plugin system:
```bash
git clone https://github.com/VINOTH-RAJ-R/ai-knowhow.git && cd ai-knowhow
python3 tools/install.py claude-code          # ~/.claude/skills/  (add --project for ./.claude/skills/)
```

### Other tools
| Tool | How |
|---|---|
| **claude.ai chat & Cowork** | `python3 tools/install.py plugin-zip`, then Customize → Plugins → Add → Upload plugin. Works in chat and Cowork, and syncs to Claude Code ([details](adapters/claude-ai/README.md)) |
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
To have it also **run** the task on the right Claude model, in Claude Code:
```
/modelwise-run write a regex for Indian PAN numbers
```
It shows the model, effort, cost and structured prompt, and runs it on a helper agent on that model once you say **Run it**.

(As a plugin skill it's also available as `/modelwise:modelwise`. You can also just ask: *"which model should I use for…"*.)

You get:

```
## Recommendation
Model:  Claude Sonnet 5.5 (claude-sonnet-5-5, anthropic): everyday frontend work at a fifth of Opus cost
Effort: medium (E3). API: output_config.effort=medium · Claude Code: /effort medium
Est. cost per run: $0.28 (list price, before caching/batch)
Cheaper: claude-haiku-5-5 @ medium   Stronger: claude-opus-5-5 @ high
Best OpenAI option: gpt-6.1-sol @ medium

## Cost across models
| Model             | Effort | Fit | Per run | Per 1,000 runs |
| claude-haiku-5-5  | medium | 3   | $0.01   | $14      (below quality bar) |
| gpt-6-luna        | medium | 3   | $0.01   | $14      (below quality bar) |
| **claude-sonnet-5-5** | medium | 4.5 | $0.28 | $280 |
| gpt-6.1-sol       | medium | 4.5 | $0.28   | $280 |
| claude-opus-5-5   | medium | 5   | $0.56   | $560 |
| claude-fable-5-1 / gpt-6-astra | medium | 5 | $1.40 | $1,400 |

## Your prompt
<context>…</context> <task>…</task> <design>… Do not use: pill buttons, gradient blobs …</design> …

## Save tokens on this task
- Put design tokens in the system prompt once; iterate with screenshots + "change X"

## Why this works
…
```

You can run the router on its own:
```bash
python3 plugins/modelwise/skills/modelwise/scripts/route.py --task code.frontend --complexity moderate
python3 plugins/modelwise/skills/modelwise/scripts/route.py --task data.extract --priority cost --volume 50000   # totals + Batch price
python3 plugins/modelwise/skills/modelwise/scripts/route.py --list-tasks
```

### retrace
At the end of any task:
```
/retrace            (or: "make a lesson from what we just did")
```
It reads the whole session, writes `.claude/skills/lesson-<slug>/`, and then teaches you straight away with a short retrace: the map, the moves the AI made (what it looked at, what it decided and why, the result), the turning points, and the cheaper path next time. Reply "walkthrough" or "rebuild" to go deeper. Commit the lesson, and your whole team can run `/lesson-<slug>` or ask "teach me <slug>" later. Teaching is built into retrace; there's no separate teach skill any more.

See a real one: [examples/lessons/lesson-building-ai-knowhow](examples/lessons/lesson-building-ai-knowhow/lesson.md), the lesson for how this repo was built.

---

## Which model should run these skills?
Your tool's selected model runs the skill, and we can't control that. The skills read data and fill templates, so you don't need a frontier model:

| | Recommended | Budget |
|---|---|---|
| | Recommended | For complex rewrites |
|---|---|---|
| **Claude** (Claude Code, claude.ai, Cowork) | Claude Haiku 5.5 @ low effort | Claude Sonnet 5.5 |
| **OpenAI** (ChatGPT, Codex) | GPT-6 Luna @ low effort | GPT-6.1 Sol |

The answer doesn't depend on the model's own knowledge. All model facts come from the registry. In our benchmark, Haiku running the skill gave the same routes and the same answer format as Sonnet, at about a fifteenth of the per-run cost.

## Does it work? (benchmark, 2026-10-18)
Full report: [docs/benchmark-report-2026-10.md](docs/benchmark-report-2026-10.md). In short:
- **modelwise model choice:** on 7 objectively scored tasks (code with unit tests, extraction, math), the routed cheaper models matched Claude Opus 5.5 on every test, and **task execution cost fell by about 74%**.
- **Classification:** 40/40 on task and complexity with both Sonnet and Haiku running the skill. The ChatGPT and claude.ai simulations matched the script's routes 9/9.
- **retrace:** teammates given the lesson scored **9/10 and 10/10** on how-and-why quizzes, against **6.5 and 7.5** with the code alone. The retrace run also found two real bugs the original build had missed.
- **Honest caveats:** auto-rewriting a *vague, subjective* prompt without the user's details scored 1-2 points **lower** than sending it as-is, in 3 rounds. modelwise now says "send it as-is to <model>" in that case and offers the structured prompt as an upgrade once you add details. On objective tasks the rewrite was neutral. Running the skill on Sonnet can cost more than it saves on tiny one-off tasks. On Haiku (now the default) it doesn't.

## What's in the registry (Phase 1: Anthropic + OpenAI)
- **60 model cards**: every current, previous, legacy and deprecated Claude and OpenAI model still served, plus image and audio models. Each card has capabilities, context, price, effort levels and defaults, fit ratings per task, prompting tips, and sources, with a `verified` date.
- **21 task types** with effort per complexity, from quick code to long-running agents, images, video and voice.
- **15 prompt templates** with slots, a universal skeleton, Claude and OpenAI renderings, a worked example, and token savers.
- **One normalized effort scale** (E0 to E6) mapped to Claude's `output_config.effort`, OpenAI's `reasoning.effort`, and the in-app settings of Claude Code, claude.ai, ChatGPT and Codex.

Fit ratings are curated judgments built from vendor docs. They are not benchmark scores. Prices are list prices for comparison. Always check the vendor's page before committing to a budget.

**Current gaps:** no video generator is listed. OpenAI shut down the Sora 2 API on 2026-09-24 and Anthropic doesn't generate video. Modelwise still writes a full video prompt. Phase 2 adds Google (Gemini, Veo) and other vendors.

## How it stays current
- **Daily:** `tools/watch_models.py` (GitHub Action) flags unknown model IDs on vendor pages, cards past their retirement date, and cards not re-verified in 45 days. It opens one issue.
- **Within 48 hours of a launch:** a person updates the card from official docs, then runs `python3 tools/validate.py --fix`, and CI checks it.
- **Monthly:** `bench/run_api.py` re-runs the A/B benchmark over the real APIs with an effort sweep, if API keys are set as repo secrets.
- **Quarterly:** review fit ratings and the skill benchmark.
- Full schedule: [docs/maintenance.md](docs/maintenance.md). How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

## Repo layout
```
.claude-plugin/marketplace.json     Claude Code / claude.ai / ChatGPT marketplace
.agents/plugins/marketplace.json    Codex marketplace
plugins/modelwise/skills/modelwise/ SKILL.md · registry/ · templates/ · guides/ · scripts/route.py · ROUTING_TABLE.md
plugins/retrace/skills/retrace/     SKILL.md · templates/ (lesson + lesson skill) · guides/capture-checklist.md
examples/lessons/                   example lessons
adapters/                           per-platform install notes (ChatGPT, Codex, claude.ai + Cowork)
tools/                              validate.py · test_route.py · install.py · release.py · watch_models.py
bench/                              A/B benchmark: tasks, checkers, scorers, API runner, results
docs/                               architecture · publishing · testing · maintenance · benchmark report
PRIVACY.md                          no data collection; what the skills run
```

## License
MIT. Not affiliated with Anthropic or OpenAI. Model names are their owners' trademarks.
