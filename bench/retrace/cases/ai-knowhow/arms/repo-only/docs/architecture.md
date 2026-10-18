# Architecture

## Design principles
1. **Knowledge lives in data, not in the model.** Model lineups change monthly and every model's training data is stale. The router never relies on what the running model "remembers". It reads the registry. That's also why the skill can run on a cheap model.
2. **Deterministic where possible.** Classification needs judgment, so the model does it. Ranking is arithmetic, so a script does it, and the same inputs always give the same recommendation. `ROUTING_TABLE.md` is the same logic, pre-computed for tools that can't run scripts.
3. **Portable.** Plain Agent Skills, JSON, Markdown, and a standard-library Python script. No server, no API keys, no dependencies. Each skill folder is self-contained (its registry is inside it), because plugin installers copy only the plugin's folder.
4. **Honest.** Every card has sources and a `verified` date. Fit ratings are labelled as curated judgments. Lessons mark inferred reasoning. Prices are list prices for comparison.

## modelwise data flow
```
                    ┌──────────────────────── registry/ ────────────────────────┐
                    │ models/<provider>/<id>.json   tasks.json   effort-scale.json │
                    └──────────────┬───────────────────────────────┬────────────┘
user prompt                        │                               │
   │                               ▼                               ▼
   ├─► classify (LLM + guides/classify.md) ─► task, complexity, priority, provider
   │                               │
   │                               ▼
   │          route.py: capability filter → status filter → quality bar (min fit)
   │                    → rank by priority → effort mapping (E-level → native level)
   │                    → cost estimate (token profile × price) → alternatives, ties, fallback
   │                               │
   │                               ▼
   └─► template (templates/<task>.md) + vendor guide (guides/prompt-style-*.md) + card prompt_tips
                                   │
                                   ▼
            answer: model · effort · cost · structured prompt · token savers · why
```

## retrace data flow
```
conversation + git diff + prompts + errors
   │
   ▼
retrace SKILL.md ─► capture-checklist (by domain) ─► fill templates/lesson.md ─► redact
   │
   ▼
lesson-<slug>/
  SKILL.md   ← templates/lesson-skill.md: tutoring protocol (overview | walkthrough | rebuild)
  lesson.md  ← goal, steps, decision log, prompts, mistakes, efficiency review, pattern, quiz, exercise
  artifacts/ ← final prompts, key snippets
   │
   ▼
/lesson-<slug>  or  /retrace:teach  → a person is taught
```

## Keeping the registry current
```
weekly GitHub Action ─► tools/watch_models.py (vendor model pages) ─► unknown IDs? ─► issue
human ─► updates the card from official docs ─► tools/validate.py --fix ─► PR ─► CI (validate + tests)
```

## Phase 2
- More vendors: Google (Gemini, Veo for video), Mistral, Meta, xAI, and media specialists (Runway, Kling, Luma, ElevenLabs).
- Optional measured fit: a small public eval set per task type, so fit ratings move from judgment toward data.
- Optional MCP server exposing `route` and `lesson` tools for apps that don't support skills.
