# Benchmarks

How we test whether **modelwise** and **retrace** actually help. Latest report: [`docs/benchmark-report-2026-10.md`](../docs/benchmark-report-2026-10.md).

## What's here
| Path | What |
|---|---|
| `e2e/tasks.json` + `e2e/checks/` | 10 end-to-end tasks, each a basic user prompt plus an automatic checker: unit tests, field accuracy, exact answers, key-fact coverage, HTML checks. Subjective tasks also get a blind judge. |
| `router/prompts.jsonl` | 40 labelled basic prompts for classification accuracy (task, acceptable complexity levels, priority) |
| `retrace/cases/` | Two learner A/B cases (the spendsum CLI and this repo). Each has a ground-truth quiz, the lesson, and both learner arms. |
| `score.py` | Objective scorers. `--run <dir>` scores a whole run. |
| `score_router.py` | Task, complexity and priority accuracy, plus route agreement |
| `cost_analysis.py` | Cost per arm from the real text exchanged, at registry prices |
| `run_api.py` | Automated A/B over the vendor APIs, with real token counts, real effort settings, and both vendors |
| `results/<date>/` | Raw outputs, judgments, usage logs, scores |

## The A/B design (modelwise)
For each basic prompt:
- **A, baseline:** the raw prompt goes to a strong default model (Claude Opus 5.5). This is "one model for everything".
- **B, modelwise:** the skill classifies the prompt and routes it, then the **structured prompt** runs on the **recommended model**.
- **C, route only:** the raw prompt runs on the recommended model. This separates the effect of the model choice (A vs C) from the effect of the prompt rewrite (C vs B).

Scoring is automatic where possible and blind (labels shuffled) where a judge is needed. Cost comes from the text actually exchanged, at list prices.

## The A/B design (retrace)
1. A teammate model builds a real project while keeping a changelog.
2. An independent agent writes a 10-question quiz from the ground truth.
3. The retrace skill turns the evidence into a lesson.
4. **Learner A** gets the code only. **Learner B** gets the code plus the lesson.
5. A blind grader scores both against the quiz.

## Re-running
- **From Claude Code** (no API keys needed): follow the prompts used in `results/2026-10-18/`. Subagents run the skill and the arms, and then `python3 bench/score.py --run <dir>` and `python3 bench/cost_analysis.py <dir> <usage.tsv>`.
- **Over the APIs** (tests effort levels and OpenAI models too):
  ```bash
  pip install anthropic openai
  python3 bench/run_api.py --effort-sweep
  ```
  It runs monthly in GitHub Actions when the repo has `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` secrets. See `docs/maintenance.md`.
