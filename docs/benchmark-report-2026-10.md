# ai-knowhow benchmark report: October 2026

**Run date:** 2026-10-18 · **Registry verified:** 2026-10-17 · **Raw data:** [`bench/results/2026-10-18/`](../bench/results/2026-10-18/), [`bench/retrace/cases/`](../bench/retrace/cases/) · **Method:** [`bench/README.md`](../bench/README.md)

## TL;DR

| Question | Answer | Evidence |
|---|---|---|
| Does modelwise pick cheaper models without losing quality? | **Yes.** Task execution cost fell by **74%**, with the same score on every objectively checked task. | 7 tasks with unit tests, field checks or exact answers: all three arms scored 100% |
| Does it classify basic prompts correctly? | **Yes**, with both the recommended and the budget runner. | 40 labelled prompts: task 100%, complexity 100% (Sonnet and Haiku), priority 95% / 90% |
| Does it work outside Claude Code? | **Yes**, in simulations of claude.ai chat, a no-code-execution environment, and a ChatGPT Project. | 9/9 routes matched the router; the cost table appeared every time |
| Do its structured prompts improve the output? | **No, not without the user's details.** They were equal on objective tasks, but 1-2 points *lower* on vague subjective prompts in all 3 rounds. The skill now recommends sending vague prompts as-is and treats the rewrite as an opt-in upgrade. | Blind Opus judge, 3 tasks × 3 rounds |
| Does running the skill cost more than it saves? | **On Sonnet, for tiny one-off tasks, yes. On Haiku, no.** Overhead fell from about $0.068 to about $0.0045 per run with the same routes and format. | Usage logs for 17 skill runs |
| Does retrace help a person understand how something was built? | **Yes, clearly.** Quiz scores rose from 6.5→9 and 7.5→10 out of 10. | Two cases, blind grader, ground-truth quizzes |

## 1. Setup

- **Runner:** Claude Code subagents (Claude Opus 5.5, Sonnet 5.5, Haiku 5.5). No API keys were used, so **OpenAI models were not executed.** OpenAI routing was tested through classification, the routing table and the ChatGPT simulation only.
- **Effort was not controllable** in the subagent harness, so every run used each model's default effort. The router's *effort* recommendations are therefore **not validated by this run**. `bench/run_api.py --effort-sweep` does this over the APIs.
- **Arms (modelwise):**
  - **A:** raw prompt → Claude Opus 5.5 ("one strong model for everything").
  - **B:** modelwise structured prompt → the routed model.
  - **C:** raw prompt → the routed model.
  - A vs C isolates the effect of model choice. C vs B isolates the effect of the prompt rewrite.
- **Scoring:** automatic checkers where possible (`bench/score.py`). A blind Opus judge with shuffled labels and a rubric for writing, landing-page and summary quality.
- **Cost:** estimated from the text actually exchanged (chars ÷ 4) × registry list price. Hidden thinking tokens are not visible, so absolute costs are understated for all arms.

## 2. modelwise results

### 2.1 Quality by task (round 1)
| Task | Routed to | Check | A (Opus, raw) | B (routed, structured) | C (routed, raw) |
|---|---|---|---|---|---|
| ipv4: validator function | Haiku 5.5 | 20 unit tests | 100% | 100% | 100% |
| dedupe: data function | Haiku 5.5 | 6 unit tests | 100% | 100% | 100% |
| movavg-debug: fix 2 bugs | Haiku 5.5 | 6 unit tests | 100% | 100% | 100% |
| expr-parser: no-eval arithmetic parser | Haiku 5.5 | 20 unit tests | 100% | 100% | 100% |
| invoices: messy-text extraction | Haiku 5.5 | 18 fields | 100% | 100% | 100% |
| reasoning: 4 math problems | Sonnet 5.5 | exact answers | 100% | 100% | 100% |
| hard-reasoning: 5 harder problems | Sonnet 5.5 | exact answers | 100% | 100% | 100% |
| summary: exec bullets | Haiku 5.5 | 7 key facts + judge | 0.90 | 0.85 | 0.90 |
| launch-email | Sonnet 5.5 | judge /10 | 8 | 7 | 8 |
| yoga-landing: landing page | Sonnet 5.5 | 5 HTML checks + judge | 0.95 | 0.85 | 0.90 |
| **Mean** | | | **0.965** | **0.940** | **0.960** |

**Reading it:**
- **Model choice:** the routed models matched Opus everywhere except a 0.05 gap on the landing page (A 0.95 vs C 0.90). Cheaper models were enough for these tasks.
- **Ceiling effect:** even the "hard" tasks were solved by every arm. This set can't show where cheap models fail. That needs harder, longer tasks (see §5).
- **Two classifications were lower than our labels:** the expression parser came out as `code.quick`, and hard-reasoning as `moderate` (our labels said `code.build` / `complex`). Neither cost any quality here.

### 2.2 Cost (execution only, round 1)
| | A: Opus everywhere | B: modelwise | C: route only |
|---|---|---|---|
| Total for 10 tasks | $0.306 | **$0.079** | $0.079 |
| vs A | n/a | **−74%** | −74% |

The largest single saving was the landing page ($0.21 → $0.07). On code and extraction tasks, Haiku cost about 2-3% of Opus.

### 2.3 The skill's own overhead
| Runner | Runs | Content tokens / run (est.) | Cost / run (est.) | Time / run |
|---|---|---|---|---|
| Sonnet 5.5 | 10 | 16k-40k | **$0.046-0.112** (mean ≈ $0.068) | 30-178 s |
| Haiku 5.5 | 7 | 27k-37k | **$0.004-0.005** | 41-90 s |

- **On Sonnet**, the skill cost more than it saved on these small one-off tasks: $0.68 of overhead against $0.23 saved.
- **On Haiku**, net savings were positive on every judged task. Examples, counting the skill's overhead: landing page −71%, launch email −60%, exec summary −21%.
- **Haiku gave the same answers as Sonnet:** the same recommended model on 2 of 2 tasks tested in parallel, every section of the answer format present, and 40/40 on classification.
- **Change made:** Haiku 5.5 / GPT-6 Luna is now the recommended runner, with Sonnet / GPT-6.1 Sol for complex rewrites.
- **Rule of thumb:** modelwise pays off on repeated work (one route, many runs), expensive tasks (agents, large outputs), or whenever it runs on a fast-tier model.

### 2.4 Structured prompts on subjective tasks: three rounds
| Round | What changed | launch-email | yoga-landing | summary | Judge's main complaint about B |
|---|---|---|---|---|---|
| 1 | Original skill (Sonnet runner) | A 8 · **B 7** · C 8 | A 9 · **B 7** · C 8 | A 8 · **B 7** · C 8 | 3 email variants instead of one; `FILL` notes shown as page text |
| 2 | "Safe to run as-is" placeholders, no variants (Haiku runner) | A 8 · **B 4** · C 8 | A 9 · **B 6** · C 8 | A 9 · **B 7** · C 8 | Output "almost entirely bracketed placeholders"; instructions leaked |
| 3 | **Fill or omit**: no empty slots in the prompt; unknowns moved to "To improve the result, tell me" (Haiku runner) | A 7 · **B 6** · C 8 | A 9 · **B 7** · C 8 | A 9 · **B 7** · C 8 | Better than round 2, but still generic: "concise… thin value", omitted facts, a stray reference to an unseen section order |

A and C are the same outputs in every round, and each round used a new judge, so A/C scores vary by ±1 between judges. That is the noise level.

**Conclusion after three rounds:** when the user gives **no details**, rewriting a **vague, subjective** prompt scored **1-2 points below** sending the user's own prompt to the same model. This held across rounds and judges, and against the same executor model (C). The fixes reduced the damage (round 2 → 3: email 4→6, landing page 6→7) but didn't remove it. On objective or detailed tasks, the rewrite was neutral.

**What changed in the skill:** for vague subjective prompts, modelwise now leads with *"Best now: send your prompt as-is to <model>"* and offers the structured version only as an **upgrade**, after the user adds the 3-4 details it lists. For detailed or objective prompts, it still gives the structured prompt. The value it adds on every task is the **model + effort choice, the cost comparison and the token tips**. That is where the measured gains are.

**Not yet measured:** whether the structured prompt *with* the user's details beats the raw prompt. Next run: a simulated user answers the "tell me" questions.

### 2.5 Latency
Executor latency was similar across arms (Haiku 10-65 s, Sonnet 10-105 s, Opus 11-150 s for the same tasks). The skill adds 30-180 s on top. That is acceptable for planning a task, and it's another reason to save modelwise for tasks that matter or repeat.

## 3. Classification and portability

### 3.1 Classification (40 labelled basic prompts, `bench/router/prompts.jsonl`)
| Runner | Task | Complexity (any acceptable level) | Priority | Route agreement |
|---|---|---|---|---|
| Sonnet 5.5 | 100% | 100% | 95% | 100% |
| Haiku 5.5 | 100% | 100% | 90% | 100% |

**Caveat:** the labels are author-written and accept a range of complexities. Real-world prompts are vaguer. Expect lower accuracy there, especially on complexity, where one level can mean an 8× cost difference.

### 3.2 Portability (same 3 prompts on each surface)
| Surface (simulated) | What was different | Routes matched router | Cost table | Main friction found → fix |
|---|---|---|---|---|
| claude.ai chat | `${CLAUDE_SKILL_DIR}` not filled in; skill folder location unknown | 3/3 | 3/3 | No volume option → added `--volume`. Cheaper line empty for the cheapest model → added wording |
| No code execution | Can't run `route.py` | 3/3 | 3/3 | Had to read about 17 files → routing table now shows effort per cell, rules for other priorities and one-vendor users, and app settings |
| ChatGPT Project | Only instructions plus flat files | 3/3 (OpenAI) | 3/3 | No picker-label mapping, template paths didn't match → table header and instructions updated |

**Not tested live:** real claude.ai, Cowork and ChatGPT accounts, which would need the user to upload. Checklist in §6.

## 4. retrace results

| Case | What was built | Learner A: code only | Learner B: code + lesson | Gain |
|---|---|---|---|---|
| spendsum | Bank-statement CLI built by a Sonnet agent; quiz written independently from its changelog | 6.5 / 10 | **9.0 / 10** | +38% |
| ai-knowhow | This repository; author-written quiz | 7.5 / 10 | **10 / 10** | +33% |

- **Where the lesson helped:** "why" and history questions. The code-only learner kept answering "can't tell from the material" on design rationale, replaced approaches, wrong assumptions and test history. On behavior questions answerable from code, the two learners were equal.
- **Lesson quality:** the lesson took one Sonnet run (90 s, 149 lines). It truthfully stated that the build had no recorded failures. It also found **two real bugs** the builder had missed: the keyword `train` matches inside "Cons**train**t Ltd", and the European amount `1.234,50` is silently read as 1.23.
- **Skill fixes from this run:** guidance for when nothing failed, or when details weren't recorded ("not recorded", plus labelled review findings). Wording changed to "design rationale from the visible record" (see below).
- **Safeguard incident:** the first builder prompt, which asked an agent to log its decisions *and thought process*, was stopped by a `reasoning_extraction` safeguard on Sonnet 5.5. Rephrased as an "engineering changelog", it ran fine. retrace's wording now avoids asking a model to reproduce hidden reasoning.

## 5. Limitations
1. **No OpenAI execution and no effort control.** Run `bench/run_api.py --effort-sweep` with API keys to cover both.
2. **Small n, single runs, one judge family** (Claude judging Claude). Differences of about ±1 judge point are noise.
3. **Ceiling effect.** Objective tasks were too easy to separate the models. Needed next: long multi-file agent tasks, larger codebases, and harder reasoning sets.
4. **Author-written labels** for the classification set and the ai-knowhow quiz, which may favor our own conventions.
5. **Token costs are estimates:** visible text only. The harness adds about 55k tokens of fixed overhead per agent run, which a normal chat or API call doesn't pay.

## 6. What to run next
- [ ] **Live surface test (by you):** `python3 tools/install.py plugin-zip`, upload both ZIPs in claude.ai → Customize → Plugins, then run 3 prompts each in chat and Cowork. Do the same in a ChatGPT Project with `adapters/chatgpt/`.
- [ ] **API benchmark with keys:** `python3 bench/run_api.py --effort-sweep` (both vendors, real tokens, validates effort recommendations).
- [ ] **Harder task set** to find where cheap routes break.
- [ ] **Filled-slot test:** re-run B where a simulated user answers the "To improve the result" questions.

## 7. Keeping it current
See [`docs/maintenance.md`](maintenance.md). In short:
- **Daily** automated tripwire for new or retired models and stale cards.
- **Card updates within 48 hours** of a vendor launch.
- **Monthly** API benchmark and full re-verification.
- **Quarterly** skill benchmark (this report) and fit-rating review.
