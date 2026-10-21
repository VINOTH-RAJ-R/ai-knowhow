---
title: Building ai-knowhow, a model-routing and lesson-capture plugin pair, with an AI agent
lesson_format: 1
domain: software
created: 2026-10-18
built_with: Claude Code (desktop app). Claude Opus 5.5 as the main agent for the whole session (per the session header); Sonnet 5.5 and Haiku 5.5 subagents for research, skill runs, learners and judging. Main-agent effort not recorded; subagents ran at default effort.
difficulty: intermediate
time_spent: About two working days of sessions (2026-10-17 to 2026-10-18). Exact hours not recorded.
prerequisites: Git, JSON, basic Python. Knows what an agent skill and a Claude Code plugin are.
---

# Building ai-knowhow with an AI agent

## 1. The goal

The user asked for two things:

1. **Teach-back.** After any AI-built work, capture how it was done (the thinking, the prompts, the mistakes) as a lesson that someone can later be taught from. This became **retrace** (plus **teach** to deliver lessons).
2. **Model routing.** Given a very basic prompt, say which model (Anthropic or OpenAI) and which effort level to use, what it costs, and give a structured prompt written for that model and task type. This became **modelwise**.

Constraints the user set along the way:
- Phase 1 covers Anthropic and OpenAI only.
- It must work in Claude Code, and also in claude.ai chat, Cowork, Codex and ChatGPT.
- The user tests from the README, then publishes to GitHub.
- Every answer should show what the same task costs on other models.
- Everything is credited to the user alone, with no other author names.

## 2. The result (as of 2026-10-18)

- **One repo, two plugins.** `modelwise` has a skill, a registry of 60 model cards built from official docs, 21 task types, 15 prompt templates and a deterministic router. `retrace` has the capture skill and `teach`.
- **Installed and loaded in Claude Code.** `/reload-plugins` reported 2 plugins and 120 skills.
- **Benchmarked.** On the objectively scored tasks, routed models matched Opus 5.5 at about 74% lower execution cost. Two learners who had the lesson scored 9/10 and 10/10 on a quiz, against 6.5 and 7.5 without it.
- **One result that went the other way.** Rewriting vague creative prompts scored 1–2 points lower than sending them as-is. The skill now says "send it as-is" first, and offers the rewrite as an upgrade.
- **Published-ready, not yet public.** A private GitHub repo was created and the first commit pushed. Release tooling and directory-submission guides are written. Nothing is in a public directory yet.
- **Commits.** `f7deee5` is the first commit (pushed). `c293256` is the v0.1.1 fix for a claude.ai upload error. Both are authored by the user only.

## 3. The approach in one paragraph

Before writing code, the agent restated the two ideas as layers and asked for the open decisions, then the user said to decide and proceed. Facts that change fast (model lineups, prices, packaging rules, directory policies) came from background research agents told to verify against official pages and not to trust memory. Stable logic was written at the same time: the effort scale, the task taxonomy, the schema, the router. Model cards were generated from a small script, then checked. Quality claims were tested with automatic scorers and a blind judge. Every surface was simulated, then installed for real. Publishing was prepared with checks that mirror the directory rules.

## 4. Step by step

1. **Restate the idea as layers.** *Why:* the request mixed two products. *Output:* a diagram of the two tools and four questions. The user answered the questions by saying "you decide".
2. **Set up the repo and research in parallel.** Three background agents: OpenAI model facts, skill and plugin packaging for each platform, and Anthropic's reference docs. *Why:* these facts were the most likely to be stale. *Output:* GPT-6 is the current OpenAI line, Sora's API had shut down, DALL·E was removed, and a plugin installer copies only the plugin's own folder.
3. **Write the stable core.** `effort-scale.json`, `tasks.json`, `model.schema.json` and `route.py`. *Output:* a router with no model names in its logic.
4. **Generate the model cards** with two throwaway scripts (one per vendor). Smoke-test the router. *Output:* the first routing table, which showed a flaw (see §5, row 5).
5. **Write templates and guides.** One template per task type, each with slots, a skeleton, Claude and OpenAI renderings, an example and token tips. Then write the retrace skill and the teach skill.
6. **Add checks.** `validate.py` (schema, skills, manifests, routing table), `test_route.py` (behaviour tests), `install.py`, and a watcher that checks vendor pages for new model IDs. *Output:* the first watcher run reported about 90 "new models". Most were file names and doc slugs. Filters fixed it.
7. **Dry-run the skill as a user would.** A Sonnet subagent ran `/modelwise` on two prompts and reported 8 issues. *Output:* fixes to the instructions and a cost comparison in every answer.
8. **Build the benchmark.** Ten end-to-end tasks, each with a checker (unit tests, field accuracy, exact answers, key facts, HTML checks), plus 40 labelled classification prompts. Three arms per task: A (raw prompt to Opus), B (structured prompt on the routed model), C (raw prompt on the routed model). A blind judge scored the subjective ones.
9. **Run retrace on a real project.** A Sonnet agent built a small CLI and kept a changelog. A separate agent wrote a ground-truth quiz from that changelog. The retrace skill turned the evidence into a lesson. Two learners answered the quiz, one with the code only and one with the code plus the lesson.
10. **Simulate the other surfaces.** A claude.ai chat, a no-code environment and a ChatGPT Project. *Output:* 9/9 routes matched the router script. Three friction points were fixed (volume totals, one-vendor guidance, the table's rules).
11. **Prepare publishing.** Research on each marketplace's rules, then listing fields, icons, OpenAI manifests, privacy and per-plugin README sections, a release checker, a release workflow, and two guides (publishing and testing).
12. **Commit and push.** The first commit was authored only by the user. The remote was first set to the wrong account name (see §7). Then the upload check failed on the retrace ZIP, which led to v0.1.1.

## 5. Decision log

| # | Decision | Options considered | Why this one | Evidence |
|---|---|---|---|---|
| 1 | One repo, two plugins | Two repos; one plugin | One repo shares CI, tests and the registry. Each plugin still installs on its own. | Plugin marketplaces accept several plugins per repo (docs fetched during research). |
| 2 | Registry inside each skill folder | Registry at the repo root | Plugin installers copy only the plugin's folder. A root registry would be missing after install. | Packaging research: "Files outside the plugin directory aren't copied." |
| 3 | Plain JSON for data | YAML, TOML | Python 3.10 has no `tomllib`, and YAML needs a package. JSON needs nothing. | Local Python version checked: 3.10.17. |
| 4 | A deterministic router script plus a generated `ROUTING_TABLE.md` | Let the model pick from the cards | The same inputs give the same answer. The table serves environments that can't run scripts, such as ChatGPT Projects. | Stated as a design goal at the start. |
| 5 | "Balanced" means the cheapest model that clears the quality bar, with one point of headroom | A log-cost penalty on fit | The first version recommended Haiku for moderate feature builds, which is too weak. Headroom gives picks that can be defended. | Smoke-test output from the first routing table. |
| 6 | One effort scale, E0 to E6 | Use each vendor's names directly | Claude goes low to max, OpenAI goes none to max, and some models reject some levels. | Both vendors' effort docs. |
| 7 | No model or effort in skill frontmatter | Pin `model: sonnet` in the frontmatter | claude.ai rejects unknown frontmatter keys, and portability mattered more. | Frontmatter rules in the skills docs. |
| 8 | For video, write the prompt and recommend no generator | Keep a Sora route | OpenAI's Sora API shut down on 2026-09-24. | OpenAI deprecations page. |
| 9 | Split audio into transcribe, speak and voice-agent tasks | One audio task | One task mixed three jobs and produced odd picks. | Routing-table review. |
| 10 | Haiku 5.5 as the default runner for the skill | Sonnet 5.5 | Same routes and answer format in our tests, at about 1/15 of the per-run cost. | Usage logs: about $0.068 per Sonnet run against about $0.0045 per Haiku run (estimated). |
| 11 | Fill or omit slots; send vague prompts as-is first | Always rewrite the prompt | Rewrites with blank slots scored 1–2 points lower. | Benchmark rounds 1–3 (judge scores in §6). |
| 12 | Retrace avoids asking a model to reproduce hidden reasoning | Ask for "thought process" | A safeguard stopped one builder run. | The first builder's error; see §7. |
| 13 | Two separate directory submissions, one per plugin | One bundle | The Anthropic directory accepts one submission per plugin folder. | Directory docs fetched during research. |

## 6. Prompts that worked

### Prompt: research with a date anchor (OpenAI model facts)

Opening lines, verbatim:

> Today is 2026-10-17. I'm building an open-source model registry and need ACCURATE, CURRENT facts about every OpenAI model available via the OpenAI API and ChatGPT right now. Use official sources first. Do not rely on memory; your training data may be stale. Flag anything you could not verify.

It then listed the exact fields wanted (model ID, release date, status, modalities, context, prices, effort levels, source URL) and ended with "a list of unverified items."

**Why it worked:** the date anchor, the explicit "don't use memory," the exact field list (so the output maps straight onto the schema), and the unverified list. The unverified list is where the surprises showed up: GPT-6 was current and the Sora API had shut down. The research agent's report later also corrected an earlier plan that assumed GPT-5.x was current.

### Prompt that worked after one that didn't: a subagent's work log

The first instruction asked a builder agent to keep a work log of its decisions, including "the alternatives you considered and why you chose one." Sonnet 5.5 flagged that request with a `reasoning_extraction` safeguard and stopped. (The wording is paraphrased. The safeguard error is exact.)

The retry asked for an **engineering changelog**: the steps, the commands, the errors and their fixes, and the design choices. It ran to completion and produced the retrace case.

**Why the retry worked:** it asked for the record of what was done, not for the model's reasoning. Retrace later adopted the same principle.

### Prompt: the fill-or-omit rule (now in the skill)

Summarised: include a slot only if the user's words or a sensible default fill it; never put `[[FILL]]` markers or "TBD" inside the prompt that will be run; list the missing details under "To improve the result, tell me." This came directly from the round-2 judging, where unfilled markers made the output "almost entirely bracketed placeholders."

## 7. Mistakes and fixes

| Symptom | Root cause | Fix | How to avoid it next time |
|---|---|---|---|
| The first routing table recommended Haiku for moderate feature builds | A log-cost penalty outweighed fit | "Balanced" became cheapest-with-headroom | Regenerate the full table and check it before trusting a formula. |
| The plan assumed GPT-5.x was the current OpenAI line | Training memory was out of date | A research agent verified it and found GPT-6 | Never write model facts from memory. Fetch them. |
| The watcher reported about 90 "new models" | The pattern matched file names and doc-page slugs | Filters, plus a `watch-ignore.json` list | Test a tripwire against real pages before shipping it. |
| The claude.ai upload of the retrace plugin failed with "SKILL.md description cannot contain XML tags" | The `teach` description contained `lesson-<slug>`, which the uploader reads as an XML tag | v0.1.1: no angle brackets in descriptions. The validator now blocks them. | Check descriptions for `<` and `>` before any upload. |
| An HTML scorer gave a correct landing page 0.8 instead of 1.0 | It counted `<img>` written inside HTML comments as real images | Strip comments before checking | Check a scorer on a known-good answer. This was done for the code scorers, but not for the HTML one at first. |
| The round-1 judge output was deleted during cleanup | A `rm -rf` was aimed at a folder that still held the only copy | Scores were rebuilt from the per-task files. The per-task notes were partly lost, so the record is incomplete for that round. | Keep raw judge output in a folder that is never cleaned up. |
| `/plugin …` was typed into the macOS shell and failed | Plugin commands belong in the Claude Code prompt, not the shell | The testing guide now says where each command goes | A test guide must say where each command is typed. |
| `git push` said "Repository not found" | The repo lived under a different GitHub account name from the one assumed in about 40 files | Remote and every link repointed to the correct account | Confirm the exact account or organisation before writing URLs into many files. |
| A GitHub access token was pasted into the chat | Convenience | It was not used, and it should be revoked. The value is not recorded here. | Never paste secrets into a chat. Use the credential helper. |
| Structured prompts scored lower on vague creative tasks | Unfilled template slots reached the output | Fill-or-omit, and send vague prompts as-is first | Template blanks must never reach the output. |

## 8. Efficiency review

- **Models and effort used:** the main agent was Opus 5.5 for the whole session. Subagents: Sonnet 5.5 for the builders, learners and the router dry run; Haiku 5.5 for the benchmark runs; Opus for the blind judges and the ground-truth quizzes. Effort for the main agent was not recorded.
- **Where tokens and time went:**
  - Research agents that fetched many pages used roughly 140k to 225k tokens each.
  - Each blind judge round read every answer, at about 100k tokens per judge.
  - The skill itself, run on Sonnet, cost about $0.07 per run (estimated). On Haiku it cost about $0.005.
  - After each prompt fix, every arm was re-run, not just the changed ones.
- **Cheaper path, using modelwise's own recommendations:**
  - Research: `research.deep` at moderate complexity. Sonnet or GPT-6.1 Sol at medium effort. Haiku is enough for list-style lookups.
  - Generating the model cards from a schema: `code.quick` on Haiku at low effort.
  - Designing the router and schema: `code.build` at complex, on Opus at high effort. This is where the strong model earned its cost.
  - Judging: one blind judge per round is enough. Use Opus only where the rubric needs judgment.
  - Re-run only the arms that changed after a fix.

## 9. The reusable pattern

1. Restate a fuzzy request as named layers, and get a yes before building.
2. Separate fast-changing facts (with a source and a date) from stable logic (code, tested).
3. Keep knowledge in data files, and keep the logic over them deterministic and tested.
4. Run research in parallel while building the parts that don't depend on it.
5. Build a benchmark with automatic scorers before you trust a quality claim. Check each scorer on a known-good answer.
6. For every surface you support, simulate it first, then install it for real.
7. Keep raw evidence in a folder you never clean up.
8. Before the first commit, search every file for stray names and secrets.

## 10. Check your understanding

1. **Why is the registry inside each skill folder, not at the repo root?**
   *Answer:* Plugin installers copy only that plugin's folder, so a root registry would be missing after install. A self-contained folder also works as a ZIP upload.

2. **A colleague says "just use Opus for everything." What evidence do you show, and what does it not prove?**
   *Answer:* Show the benchmark: routed cheaper models matched Opus on every objectively checked task, at about 74% lower execution cost. It does not prove quality on long, multi-file agent work, because every arm solved the objective tasks (a ceiling effect). The effort recommendations were not tested either.

3. **A vague "landing page for my bakery" prompt was rewritten and scored lower. What do you change, and why not just write a better rewrite?**
   *Answer:* Use fill-or-omit, and send vague prompts as-is first, then offer the rewrite as an upgrade once the user adds details. The gap came from unfilled slots and leaked instructions, not from the rewrite's style.

4. **Google releases a new video model next month. What do you change?**
   *Answer:* Add `google` to the provider list in the schema, add an effort mapping and a prompt-style guide, and add a model card with `video_out` and fit scores for `video.generate`. Add a watcher source. Run `validate.py --fix` and the tests. The video fallback stops applying on its own once a generator is in the registry.

5. **Scenario: a teammate wants the skill to fetch current prices from the vendor's API at run time. What do you say?**
   *Answer:* Keep the data reviewed and static. The design promises no network access. A live fetch would make answers depend on connectivity, and unreviewed data could change a recommendation. A daily watcher and a monthly review handle freshness instead.

## 11. Try it yourself

Add a fictional model card (for example `example-model`), give it fit scores for three tasks, then run `python3 tools/validate.py --fix` and `python3 tools/test_route.py`. Find it in `plugins/modelwise/skills/modelwise/ROUTING_TABLE.md`.

**Done when:** validation passes, and you can explain whether the model becomes the recommendation for any task and why.

## Review findings (found during this retrace, not during the build)

- **Claude CLI not run.** The build machine had no Claude CLI, so `claude plugin validate --strict` was never run by the builder. `release.py` prints a note asking for it. Run it before publishing.
- **Benchmark ceiling.** Every arm solved the objectively checked tasks, so the benchmark can't show where cheap routes fail. Harder, longer tasks are needed.
- **Effort is untested.** The test environment couldn't set effort per run. `bench/run_api.py --effort-sweep` covers this once API keys are available.
- **Author-written quiz.** The ai-knowhow quiz was written by the same person who built the repo, so it favours that author's conventions.
- **Old example lesson.** `examples/lessons/lesson-building-ai-knowhow/` is an earlier version from before the benchmark and publishing work. It is out of date. This lesson supersedes it.
- **Cost figures are estimates.** They count the visible text only. Hidden thinking tokens aren't counted, so absolute costs are understated for every arm.
