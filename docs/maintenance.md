# Keeping ai-knowhow current

Model lineups, prices and effort levels change every few weeks. This is the schedule we recommend, with what runs automatically and what needs a person.

| What | How often | Automated? | Cost | Tool |
|---|---|---|---|---|
| **New-model tripwire**: unknown model IDs on vendor pages, cards past retirement, cards not re-verified in 45 days | **Daily** | Yes (GitHub Action opens one issue) | Free | `tools/watch_models.py`, `.github/workflows/watch-models.yml` |
| **Validation + router tests** on every change | Every push/PR | Yes | Free | `tools/validate.py`, `tools/test_route.py` |
| **Add or update model cards** after a vendor launch or price change | Within **48 hours** of the tripwire issue | No: a person reads the official docs and edits JSON | ~30 min per model | `CONTRIBUTING.md` |
| **Full re-verification** of every current card (prices, limits, effort levels, status) | **Monthly** | Partly (the tripwire lists cards older than 45 days) | ~1-2 hours | Vendor model and pricing pages |
| **A/B benchmark over the real APIs** (both vendors, effort sweep) | **Monthly**, and after any change to fit ratings or a new flagship model | Yes, if API keys are set as repo secrets | A few dollars per run at list prices | `bench/run_api.py`, `.github/workflows/benchmark.yml` |
| **Skill benchmark** (classification accuracy, skill-on-Haiku, retrace learner A/B) | **Quarterly**, or when SKILL.md or templates change | No: run from Claude Code (see `bench/README.md`) | ~1-3 hours of agent time | `bench/` |
| **Fit-rating review** using benchmark results and vendor evals | **Quarterly** | No | ~2 hours | Model cards |
| **Prompt-style guides** (`guides/prompt-style-*.md`) | When a vendor publishes a new prompting guide (usually with a new model family) | No | ~1 hour | Vendor prompting docs |

## Why these intervals
- **Daily tripwire:** vendors ship without notice, and a stale "current" model is the most damaging error (wrong recommendation, wrong price). The check is free and opens at most one issue.
- **48-hour card updates:** most users ask about the newest model in the first week after launch.
- **45-day staleness:** prices and effort defaults have changed within a single quarter more than once in 2026 (e.g. Opus 5.5's default effort, GPT-6's removal of `minimal`).
- **Monthly API benchmark:** routing quality depends on fit ratings. A monthly run catches a model that has become relatively better or worse, at low cost.
- **Quarterly skill benchmark:** SKILL.md and templates change less often, and the run costs more agent time.

## Release checklist when a new model ships
1. The tripwire issue lists the new ID.
2. Read the vendor's model page, pricing page and prompting guide.
3. Add `registry/models/<provider>/<id>.json`. Demote the predecessor to `previous`.
4. `python3 tools/validate.py --fix && python3 tools/test_route.py`
5. Run `python3 bench/run_api.py --tasks <a few> --effort-sweep` if you have keys. Adjust `fit` only with evidence.
6. Update `guides/prompt-style-<vendor>.md` if the prompting advice changed.
7. Open a PR that links the sources.
