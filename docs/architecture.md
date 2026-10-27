# Architecture

## Design principles
1. **Knowledge lives in data, not in the model.** Model lineups change monthly and every model's training data is stale. The router never relies on what the running model "remembers". It reads the registry. That's also why the skill can run on a cheap model.
2. **Deterministic where possible.** Classification needs judgment, so the model does it. Ranking is arithmetic, so a script does it, and the same inputs always give the same recommendation. `ROUTING_TABLE.md` is the same logic, pre-computed for tools that can't run scripts.
3. **Portable.** Plain Agent Skills, JSON, Markdown, and a standard-library Python script. No server, no API keys, no dependencies. Each skill folder is self-contained (its registry is inside it), because plugin installers copy only the plugin's folder.
4. **Honest.** Every card has sources and a `verified` date. Fit ratings are labelled as curated judgments. Lessons mark inferred rationale. Prices are list prices for comparison.

## modelwise data flow
```
                    ┌──────────────────────── registry/ ────────────────────────┐
                    │ models/<provider>/<id>.json   tasks.json   effort-scale.json │
                    └──────────────┬───────────────────────────────┬────────────┘
user prompt                        │                               │
   │                               ▼                               ▼
   ├─► classify (LLM + guides/classify.md) ─► department, industry, market, audience
   │                               │
   │                               ▼
   ├─► expert decision (guides/industry-lens.md, practice-*.md, regulated.md for the stated market)
   │       goal · deliverable · approach · success measure · production path · red lines
   │       └─► one or more phases, each with task, complexity, priority, provider
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
                    (one route per phase; each prompt says where it runs and what you get back)
```

**Creative requests** (posters, social posts, carousels, ads) add a creative director's process before the prompts: a brief with one human insight, the category clichés to avoid, three routes that differ in visual metaphor and medium, each with a taste direction from `guides/creative-taste.md`, a judging table, then a text-free production plate and a layout spec for Figma or Canva. Text-heavy layouts go to a design tool, not an image model. Multi-slide formats get a plan for every slide and one series template.

## modelwise-run (Claude Code only)
```
user prompt ─► modelwise-run SKILL.md
   │  steps 1–3 reuse ../modelwise: classify → route.py --provider anthropic → structured prompt
   ▼
confirm card: model @ effort · cost vs other models · the exact prompt   ── user: Run / stronger / cheaper / cancel
   │
   ▼
Agent tool ─► runner agent (agents/modelwise-haiku | -sonnet | -opus | -fable, model fixed in frontmatter)
   │          effort set per call; the helper can't see the chat, so the prompt stands alone
   ▼
result in full + "Ran on <model> @ <effort> · est. $x · vs Opus $y"
```
A skill can't change the model of the chat it runs in, so the work moves to a subagent on the routed model. The session model only classifies and structures, so running the session on Sonnet or Haiku keeps that step cheap. Image, video and audio phases can't run on Claude and fall back to the modelwise prompt. Other surfaces (claude.ai, Cowork, Codex) fall back to the modelwise answer.

## retrace data flow
```
conversation + git diff + prompts + errors
   │
   ▼
retrace SKILL.md ─► capture-checklist (by domain) ─► fill templates/lesson.md ─► redact
   │
   ▼
lesson-<slug>/
  SKILL.md   ← templates/lesson-skill.md: tutoring protocol (short retrace | walkthrough | rebuild)
  lesson.md  ← goal, steps, decision log, prompts, mistakes, efficiency review, pattern, quiz, exercise
  artifacts/ ← final prompts, key snippets
   │
   ▼
/retrace teaches it right away; later: /lesson-<slug> or "teach me <slug>" → a person is taught
```

## Cost estimates
`route.py` prices one typical task from the task's token profile and the card's list price. Rows are sorted and volume totals (`--volume N`, with the 50% Batch price) are computed from the unrounded cost; only the displayed per-run and per-1,000 figures are rounded. They are list-price comparisons, not quotes: caching, regional and priority tiers are left out.

## Keeping the registry current
```
daily GitHub Action ─► tools/watch_models.py (vendor model pages) ─► unknown IDs? ─► issue
human ─► updates the card from official docs ─► tools/validate.py --fix ─► PR ─► CI (validate + tests)
```

## Phase 2
- More vendors: Google (Gemini, Veo for video), Mistral, Meta, xAI, and media specialists (Runway, Kling, Luma, ElevenLabs).
- Optional measured fit: a small public eval set per task type, so fit ratings move from judgment toward data.
- Optional MCP server exposing `route` and `lesson` tools for apps that don't support skills.
