---
title: Building ai-knowhow, an open-source model router and lesson-capture toolkit, with an AI agent
lesson_format: 1
domain: software
created: 2026-10-17
built_with: Claude Code desktop app; Claude Opus 5.5 as the main agent; background research sub-agents
difficulty: intermediate
time_spent: one working session
prerequisites: Comfortable with Git, JSON and basic Python; knows what an "agent skill" or custom instruction is
---

# Building ai-knowhow with an AI agent

## 1. The goal
The user wanted two things, published as open source:
1. *"Every time a task is over… a skill that, when called, teaches a human how it was done, what the thought process was, what was followed."* → **retrace**
2. *"When the user provides a very basic prompt… tell on which model, in which effort, this task needs to run, and what the structured prompt is"*, for coding, image and video tasks, based on each vendor's model documentation, plus *"how to save tokens for each task"*. → **modelwise**

Constraints: Anthropic and OpenAI only in phase 1. Suggest a default model to run the router on each platform. It must work in Claude and in GPT tools. The user would test it from the README and push it to GitHub.

## 2. The result
- A monorepo with two independently installable plugins (`modelwise`, `retrace` + `teach`) and marketplace files for Claude Code, claude.ai, ChatGPT workspaces and Codex.
- A registry of 60 model cards, 21 task types, 15 prompt templates, a normalized effort scale, and a stdlib-only router script with a generated routing table.
- Verification: `tools/validate.py` (schema, skills, manifests, routing table freshness) and `tools/test_route.py` (9 behavior tests), both passing, plus a weekly model-watch GitHub Action.

## 3. The approach in one paragraph
Explain the architecture before writing code, so the user can redirect early. Then research the facts that change fastest (model lineups, packaging formats) in parallel background agents, while writing the parts that don't depend on them (schema, task taxonomy, router, templates, retrace). Put all model knowledge in **data files** rather than in prompts, make the ranking **deterministic**, and validate everything with scripts so the repo can be kept current by contributors.

## 4. Step by step
1. **Clarify the idea as layers.** *Why:* the request was two ideas mixed together. Restating them as "teach-back" and "router" with a diagram let the user confirm scope. *Output:* the architecture explanation and four open decisions (name, license, providers, build order).
2. **Get the go-ahead and delegate decisions.** The user said: Anthropic and OpenAI only, "you can take all the decisions". *Output:* a name (`ai-knowhow`, with `modelwise` and `retrace`), the MIT license, and a monorepo layout.
3. **Research in parallel.** Anthropic model facts came from the bundled Claude API reference. Two background agents fetched (a) OpenAI's current models, pricing and prompting guides, and (b) skill and plugin packaging for Claude Code, Codex, ChatGPT and claude.ai. A third checked skill frontmatter rules. *Why:* these facts change monthly and the agent's training data was stale.
4. **Write the stable core while research ran:** `effort-scale.json`, `tasks.json`, `model.schema.json`, `route.py`. *Why:* none of these depend on specific model names.
5. **Generate the Anthropic cards** with a throwaway script, smoke-test the router, and fix the ranking (see the decision log).
6. **Write the templates and guides** (one per task type, with Claude and OpenAI renderings) and the retrace skills.
7. **Fold in the research results:** GPT-6 is current, the Sora API is shut down, Custom GPTs are being retired, and plugin installs copy only the plugin folder. Adjust cards, tasks and adapters to match.
8. **Validate and test:** add the validator, the router tests and the model watcher. Fix what they found.
9. **Document:** README, per-plugin READMEs, adapters, architecture, contributing guide, and this lesson.

## 5. Decision log
| # | Decision | Options considered | Why this one | Evidence |
|---|---|---|---|---|
| 1 | One repo, two plugins | Two repos; one plugin | The user said either was fine. One repo shares tooling and CI, and separate plugins let people install only what they need | User message; marketplace format supports several plugins |
| 2 | Registry **inside** the modelwise skill folder | Top-level `registry/` | Plugin installers copy only the plugin's own folder, so files outside it break after install | Packaging research: "Files outside the plugin directory aren't copied" |
| 3 | JSON, not YAML | YAML; TOML | Python's standard library reads JSON everywhere. YAML needs PyYAML, and `tomllib` needs Python 3.11+ | Checked the local Python version; the goal of zero install steps *(inferred priority)* |
| 4 | Deterministic `route.py` plus a generated `ROUTING_TABLE.md` | Let the LLM choose from the cards | The same inputs give the same answer, it's testable, and the table covers tools that can't run scripts (ChatGPT Projects) | Design goal: recommendations independent of the running model |
| 5 | "Balanced" = cheapest model clearing the bar **+1 headroom** | A log-cost penalty on fit | The penalty picked Haiku for *moderate* feature builds, which is too weak. Headroom gives explainable picks (Sonnet for moderate, Opus for complex) | Smoke test output |
| 6 | Normalized effort E0-E6 | Using vendor names directly | Claude (low…max) and OpenAI (none…max) differ, and some models reject levels. One scale plus per-card snapping handles both | Effort docs from both vendors |
| 7 | No `model`/`effort` in SKILL.md frontmatter; put defaults in `metadata` and the skill text | Pinning `model: sonnet` | claude.ai uploads reject unknown frontmatter keys, and portability mattered more | Frontmatter check |
| 8 | Video: write the prompt, but recommend no generator | Keep Sora | The OpenAI Sora 2 API shut down on 2026-09-24, and Anthropic doesn't generate video | OpenAI deprecations page |
| 9 | Split audio into transcribe / speak / agent | One audio task | One task mixed transcription with voice agents and gave nonsense picks | Routing table review |

## 6. Prompts that worked
### Prompt: research delegation
```
Today is 2026-10-17. I'm building an open-source model registry and need ACCURATE, CURRENT facts about
every OpenAI model available via the OpenAI API and ChatGPT right now. Use official sources first...
Do not rely on memory; your training data may be stale. Flag anything you could not verify.
For EACH model give: exact API model ID, release date, status..., context window, max output tokens,
price per 1M input/output tokens (and cached input), reasoning_effort levels supported and the default...
Return a structured markdown report... then a list of unverified items.
```
**Why it worked:** it states the date, forbids relying on memory, names official sources, lists exact fields (so the result maps 1:1 onto the schema), and asks for an **unverified list**. That list is where the surprises showed up (GPT-6, Sora shut down).

### What didn't work
No prompt failed outright. The design that failed was the first ranking rule (decision 5). The lesson: check a scoring formula against the *whole* routing table, not one example.

## 7. Mistakes and fixes
| Symptom | Root cause | Fix | How to avoid next time |
|---|---|---|---|
| Haiku recommended for moderate app builds | The log-cost penalty outweighed fit | Cheapest model that clears the bar + 1 headroom | Generate the full table and review it before trusting a formula |
| Plan assumed GPT-5.x was current | The agent's training data was out of date | Research agent with "don't trust memory" | Never write model facts from memory. Fetch them |
| Watcher reported ~90 "new models" | The regex matched file names and doc slugs | Filters plus `watch-ignore.json` | Test tripwires against real pages before shipping |
| Planned to put Custom GPTs in the ChatGPT adapter | They are being retired | Projects / skills / plugin import | Check the platform docs for each adapter |

## 8. Efficiency review
- **Models and effort used:** Claude Opus 5.5 as the main agent; research agents inherited the same model. The effort level wasn't recorded.
- **Where tokens/time went:** reading long reference docs into the main context; three research agents, each fetching many pages; regenerating the routing table several times.
- **Cheaper path** (what modelwise would recommend):
  - Research: `research.deep`, moderate → Sonnet 5.5 or GPT-6.1 Sol at medium, as background agents
  - Card generation: `code.quick` → Haiku 5.5 at low (it's mechanical)
  - Architecture and router design: `code.build`, complex → Opus 5.5 at high (keep the strong model here)
  - Read large references with targeted `grep`/`sed` ranges rather than whole files. This was done partly here.

## 9. The reusable pattern
1. Restate a fuzzy idea as named layers, and get a yes before building.
2. Separate **fast-changing facts** (research, with sources and dates) from **stable logic** (code).
3. Put knowledge in data files, and make the logic over them deterministic and tested.
4. Run research in parallel while building the parts that don't depend on it.
5. Add a validator and a tripwire so the data stays honest after you leave.
6. Write the lesson while the evidence is fresh.

## 10. Check your understanding
1. Why is the registry inside the skill folder instead of at the repo root?
   <details><summary>Answer</summary>Plugin installers copy only the plugin's own folder. A skill that reads files outside it breaks after install, and a self-contained folder also works as a ZIP upload.</details>
2. Why doesn't the router need a frontier model to run?
   <details><summary>Answer</summary>All model knowledge comes from the registry and the ranking is a script. The running model only classifies the prompt and fills a template.</details>
3. **Scenario:** Google releases a new video model next month. What do you change?
   <details><summary>Answer</summary>Phase-2 steps: add `google` to the provider enum, add an effort mapping and a prompt-style guide, add a card with `video_out` and `fit` for `video.generate`, add a watcher source, then run `validate.py --fix` and the tests. The video fallback stops applying automatically.</details>

## 11. Try it yourself
Add a model card for a model the registry doesn't have yet (or a made-up `example-model` in a branch). Give it `fit` scores for three tasks, run `python3 tools/validate.py --fix` and `python3 tools/test_route.py`, then check where it shows up in `ROUTING_TABLE.md`.
**Done when** validation passes and you can explain why it does (or doesn't) become the recommendation for one task.
