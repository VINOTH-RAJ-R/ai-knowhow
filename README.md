# ai-knowhow

**Know what to build it with. Know how it was built.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Works in](https://img.shields.io/badge/works%20in-Claude%20Code%20·%20claude.ai%20·%20Codex%20·%20ChatGPT-black.svg)](#quick-start)

Most people use one AI model for everything, with a one-line prompt. They overpay for simple work, get average results on hard work, and nobody on the team learns how the result was made.

ai-knowhow is two open-source agent skills that fix that:

| | What you type | What you get |
|---|---|---|
| **[modelwise](plugins/modelwise/)** | Any basic prompt, from any department: engineering, marketing, sales, HR, finance, design, legal, operations | What a top practitioner would deliver, the right **model** and **effort** for each phase (Anthropic or OpenAI), the **cost** against other models, and a **prompt written the way that model works best** |
| **[modelwise-run](plugins/modelwise/#route-and-run-claude-code)** · Claude Code | `/modelwise-run <prompt>` | The same route, then, after you confirm, the task **runs on that Claude model** (Haiku, Sonnet, Opus or Fable) and the result comes back to your chat |
| **[retrace](plugins/retrace/)** | `/retrace` at the end of any AI task | A saved **lesson** of how it was done (the moves, decisions, prompts that worked, mistakes and the cheaper path), taught to you on the spot and replayable by your team |

They are plain [Agent Skills](https://agentskills.io): Markdown, JSON and one small Python script with no dependencies. No server, no API keys, no data collection.

## Contents
- [Quick start](#quick-start)
- [Install on other tools](#install-on-other-tools)
- [modelwise: how it works](#modelwise-how-it-works)
- [modelwise-run: route and run](#modelwise-run-route-and-run)
- [retrace: turn work into lessons](#retrace-turn-work-into-lessons)
- [Does it work?](#does-it-work)
- [What's in the registry](#whats-in-the-registry)
- [Privacy and safety](#privacy-and-safety)
- [FAQ](#faq)
- [Repo layout](#repo-layout) · [Contributing](#contributing) · [License](#license)

---

## Quick start
In **Claude Code**:
```
/plugin marketplace add VINOTH-RAJ-R/ai-knowhow
/plugin install modelwise@ai-knowhow
/plugin install retrace@ai-knowhow
/reload-plugins
```

### Your first five minutes

**1. Find out what you're overpaying for**
```
/modelwise sort 5,000 support tickets into billing, bug and feature request, as cheap as possible
```
It picks the cheapest model that still clears the quality bar and prices the whole job: about **$0.78 on Claude Haiku against $31 on Opus**, and half that again with Batch.

**2. Ask like a manager, get a creative director's answer**
```
/modelwise launch post for our new app on Instagram and LinkedIn
```
You get a brief, the clichés to avoid, three really different concepts with a judging table, and a ready image prompt for each, plus the caption.

**3. Let it do the work** (Claude Code)
```
/modelwise-run write a Python function that validates email addresses, with tests
```
A card shows the model, the cost and the exact prompt. Say **Run it**, and Claude Haiku does the job for less than a cent.

**4. Learn what just happened**
```
/retrace
```
It replays the session as a short lesson: the moves, the turning points, the prompts that worked, and the cheaper path next time. Saved for your team.

### Or pick your role
| You are | Try |
|---|---|
| Founder | `/modelwise three pricing tiers for our B2B SaaS, and how to test them` |
| Marketer | `/modelwise festive sale email for our skincare brand` |
| Engineer | `/modelwise why does my Docker build take 12 minutes` |
| HR | `/modelwise job description and interview scorecard for a senior data analyst` |
| Finance | `/modelwise monthly cash-flow forecast from our bank exports` |
| Support lead | `/modelwise reply templates for our top 10 refund questions` |

As plugin skills they're also available as `/modelwise:modelwise`, `/modelwise:modelwise-run` and `/retrace:retrace`. You can also just ask *"which model should I use for…"*.

> No GitHub SSH key? Set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` first. Third-party marketplaces don't auto-update by default: turn it on in `/plugin` → Marketplaces, or run `claude plugin update modelwise@ai-knowhow`.

## Install on other tools
| Tool | How |
|---|---|
| **Claude Code, without the plugin system** | `git clone https://github.com/VINOTH-RAJ-R/ai-knowhow.git && cd ai-knowhow && python3 tools/install.py claude-code` (copies the skills to `~/.claude/skills/` and the runner agents to `~/.claude/agents/`; add `--project` for this project only). Start a new session afterwards. |
| **claude.ai and Cowork** | Download `modelwise-plugin.zip` and `retrace-plugin.zip` from the [latest release](https://github.com/VINOTH-RAJ-R/ai-knowhow/releases/latest), then Customize → Plugins → Add → Upload plugin. Or add the marketplace `VINOTH-RAJ-R/ai-knowhow` there. [Details](adapters/claude-ai/README.md) |
| **OpenAI Codex** | `codex plugin marketplace add VINOTH-RAJ-R/ai-knowhow`, or `python3 tools/install.py codex`. [Details](adapters/codex/README.md) |
| **ChatGPT** | Workspace plugin import, skill upload, or a Project with our instructions file. [Details](adapters/chatgpt/README.md) |

`modelwise-run` needs Claude Code, because only Claude Code can hand work to an agent on another model. Everywhere else, modelwise gives you the route and the prompt to run yourself.

---

## modelwise: how it works
```
your prompt
  1. understand   department · industry · market · audience
  2. decide       what a top practitioner would deliver: goal, deliverable, approach,
                  success measure, production path, red lines
  3. route        each phase → task type → registry → model + effort + cost (scripts/route.py)
  4. write        a prompt in the chosen model's own style, from a task template
  5. answer       expert decision · route per phase · cost across models · ready prompts,
                  each with "Paste into … · You get …"
```
The model does the judgment (steps 1, 2 and 4). A script does the ranking and the costs (step 3), so the same inputs always give the same recommendation. Model facts come from a registry built from official vendor docs, not from what the running model remembers.

**Creative work** (posters, social posts, carousels, ads) gets a creative director's process: a brief with one human insight, the category clichés to avoid, three really different concepts with industry taste, a judging table, then a text-free production image and a layout spec for Figma or Canva.

### Example
`/modelwise landing page for my bakery` returns, in short:

```
## Expert decision
Owner: senior frontend engineer + brand designer · small food business · locals on their phones
Real goal: more walk-ins and pre-orders · Deliverable: one fast, mobile-first page
Red lines: no stock-photo hero, no unreadable menu image, no slow carousel

## Recommendation
Model:  Claude Sonnet 5.5 (claude-sonnet-5-5): fit 4.5/5 for frontend at half of Opus's cost
Effort: medium · API: output_config.effort=medium · Claude Code: /effort medium
Est. cost per run: $0.28 (list price, before caching and batch)
Cheaper: gpt-6.1-terra @ medium, $0.14 · Stronger: claude-opus-5-5 @ medium, $0.56
Same fit from OpenAI: gpt-6.1-sol @ medium, $0.28

## Cost across models
| Model                 | Effort | Fit | Per run | Per 1,000 runs |
| claude-haiku-5-5      | medium | 3   | $0.014  | $14            |
| gpt-6-luna            | high   | 3   | $0.014  | $14            |
| gpt-6.1-terra         | medium | 3.5 | $0.14   | $140           |
| **claude-sonnet-5-5** | medium | 4.5 | $0.28   | $280           |
| gpt-6.1-sol           | medium | 4.5 | $0.28   | $280           |
| claude-opus-5-5       | medium | 5   | $0.56   | $560           |

## Your prompt  (paste into Claude Code or claude.ai · you get the page code)
<context>…</context> <task>…</task> <design>… Do not use: pill buttons, gradient blobs …</design> …
```

Run the router on its own:
```bash
python3 plugins/modelwise/skills/modelwise/scripts/route.py --task code.frontend --complexity moderate
python3 plugins/modelwise/skills/modelwise/scripts/route.py --task data.extract --priority cost --volume 50000   # totals + Batch price
python3 plugins/modelwise/skills/modelwise/scripts/route.py --list-tasks
```

## modelwise-run: route and run
In Claude Code, `/modelwise-run <prompt>`:
1. routes the prompt to a Claude model and effort, using the same steps as modelwise;
2. shows a card with the model, the cost against other models, and the exact prompt it will send;
3. waits for **Run it**, a stronger or cheaper model, or **Cancel**. It never runs without your OK;
4. hands the task to a helper agent on that model (`modelwise-haiku`, `-sonnet`, `-opus` or `-fable`) and returns the result, with what it cost.

A skill can't change the model of the chat it runs in, so the work moves to a helper agent on the routed model. Tip: keep your own session on Sonnet or Haiku, so the routing step itself stays cheap. Image, video and audio tasks can't run on Claude, so it gives you the modelwise prompt for those instead.

## retrace: turn work into lessons
At the end of any task, type `/retrace` (or *"make a lesson from what we just did"*). It:
1. reads the whole session: requests, files, commands, prompts, errors and fixes;
2. saves a lesson to `.claude/skills/lesson-<slug>/` (secrets and personal data removed);
3. teaches you straight away with a short retrace: the map, the moves the AI made and why, the turning points, what steered it, and the cheaper path next time.

Reply *"walkthrough"* to go step by step, or *"rebuild"* to try it yourself. Commit the lesson, and anyone on your team can run `/lesson-<slug>` or ask *"teach me <slug>"* later. Lessons mark anything the record doesn't state as *(inferred)*.

See a real one: [the lesson for how this repo was built](examples/lessons/lesson-building-ai-knowhow/lesson.md).

---

## Does it work?
Benchmark from 2026-10-18 (before the creative and run features). Full report: [docs/benchmark-report-2026-10.md](docs/benchmark-report-2026-10.md).
- **Model choice:** on 7 objectively scored tasks (code with unit tests, extraction, math), the routed cheaper models matched Claude Opus 5.5 on every test, and **task cost fell by about 74%**.
- **Classification:** 40/40 on task and complexity with both Sonnet and Haiku running the skill. ChatGPT and claude.ai simulations matched the script's routes 9/9.
- **retrace:** teammates given the lesson scored **9/10 and 10/10** on how-and-why quizzes, against **6.5 and 7.5** with the code alone.
- **Honest caveats:** rewriting a *vague, subjective* prompt without your details scored 1–2 points *lower* than sending it as-is, so modelwise now says "send it as-is" in that case and offers the structured prompt once you add details. On tiny one-off tasks, running the skill on Sonnet can cost more than it saves; on Haiku it doesn't.

**Which model should run the skills themselves?** They read data and fill templates, so you don't need a frontier model:

| | Recommended | For complex rewrites |
|---|---|---|
| **Claude** (Claude Code, claude.ai, Cowork) | Claude Haiku 5.5 @ low effort | Claude Sonnet 5.5 |
| **OpenAI** (ChatGPT, Codex) | GPT-6 Luna @ low effort | GPT-6.1 Sol |

## What's in the registry
Phase 1 covers Anthropic and OpenAI:
- **61 model cards**: every current, previous, legacy and deprecated Claude and OpenAI model still served, plus image and audio models. Each has capabilities, context, price, effort levels, fit ratings per task, prompting tips, sources and a `verified` date.
- **21 task types**, **15 prompt templates**, and **12 guides** (classification, prompt styles, practice checklists for engineering, design, content and business functions, industry lens, creative taste, regulated markets).
- **One effort scale** (E0 to E6) mapped to Claude's `output_config.effort`, OpenAI's `reasoning.effort`, and the in-app settings of Claude Code, claude.ai, ChatGPT and Codex.

Fit ratings are curated judgments from vendor docs, not benchmark scores. Prices are list prices for comparison, not quotes. **Current gap:** no video generator is ranked (OpenAI shut down the Sora 2 API on 2026-09-24); modelwise still writes the full video prompt and names common tools. Phase 2 adds Google and other vendors.

**How it stays current:** a daily GitHub Action ([`tools/watch_models.py`](tools/watch_models.py)) flags new model IDs on vendor pages, retired models and cards not re-verified in 45 days, and opens an issue. A person updates the card from the official docs, and CI validates it. Schedule: [docs/maintenance.md](docs/maintenance.md).

## Privacy and safety
- **modelwise** runs one local script (`route.py`) that reads the bundled registry. No network calls, no API keys, nothing collected.
- **modelwise-run** starts a helper agent in your Claude Code session after you confirm. It has your session's permissions, is told not to commit, push, send, publish or delete anything, and Claude Code's own permission prompts still apply. It runs on your Claude plan, like any other task.
- **retrace** writes lesson files only where you run it, after removing keys, tokens, passwords and personal data.
- Full details: [PRIVACY.md](PRIVACY.md).

## FAQ
**Does modelwise make the image, video or app itself?** No. It decides, routes and writes the prompt; you run it in the named tool. `modelwise-run` is the one that executes, and only on Claude, only after you confirm.

**Do I need API keys?** No. The skills run inside the AI tool you already use.

**How accurate are the costs?** They are list-price estimates for one typical task of that size, to compare models. Caching and Batch lower them; your real usage may differ.

**Will it recommend OpenAI when I'm in Claude Code?** It shows the best option from each vendor. Being in Claude Code doesn't hide OpenAI; `modelwise-run` only runs Claude models.

**A model I use is missing.** Open an issue, or add a card: see [CONTRIBUTING.md](CONTRIBUTING.md).

## Repo layout
```
plugins/modelwise/skills/modelwise/       SKILL.md · registry/ · templates/ · guides/ · scripts/ · ROUTING_TABLE.md
plugins/modelwise/skills/modelwise-run/   SKILL.md: route, confirm, run on a helper agent
plugins/modelwise/agents/                 runner agents: modelwise-haiku · -sonnet · -opus · -fable
plugins/retrace/skills/retrace/           SKILL.md · templates/ · guides/capture-checklist.md
.claude-plugin/marketplace.json           Claude Code, claude.ai and ChatGPT marketplace
.agents/plugins/marketplace.json          Codex marketplace
examples/lessons/                         example lessons
adapters/                                 install notes for ChatGPT, Codex, claude.ai and Cowork
tools/                                    validate · test_route · install · release · watch_models
bench/                                    A/B benchmark: tasks, checkers, scorers, results
docs/                                     architecture · publishing · testing · maintenance · benchmark report
```
How the pieces fit together: [docs/architecture.md](docs/architecture.md).

## Contributing
Issues and pull requests are welcome: new model cards, fit corrections with evidence, templates, practice guides and lessons. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Every change runs `tools/validate.py` and the router tests in CI.

## License
[MIT](LICENSE). Not affiliated with Anthropic or OpenAI. Model names are their owners' trademarks.
