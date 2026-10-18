# Classifying a raw prompt

Turn a basic prompt into four values: **task**, **complexity**, **priority**, **provider**. Takes one pass; don't over-think it.

## 1. Task
Match against `registry/tasks.json` using its `label` and `signals`. Pick the task whose *output* matches what the user wants:

| If the user wants… | Task |
|---|---|
| a regex, snippet, one function, command | `code.quick` |
| a feature, app, API, script built | `code.build` |
| a page, component, UI | `code.frontend` |
| something fixed that's broken | `code.debug` |
| code reviewed, refactored, migrated, explained | `code.review` |
| an agent to work for a long time on its own | `agent.longrun` |
| a UI or website operated for them | `agent.computer` |
| new text written | `text.write` |
| existing text summarized, rewritten, translated | `text.transform` |
| a question answered, ideas | `text.chat` |
| fields pulled out / items labelled, often many | `data.extract` |
| numbers analyzed, SQL, charts | `data.analysis` |
| sources found and synthesized | `research.deep` |
| a hard problem solved (math, planning, strategy) | `reason.hard` |
| an image/PDF/screenshot understood | `vision.understand` |
| a new image | `image.generate` |
| an existing image changed | `image.edit` |
| a video clip | `video.generate` |
| speech transcribed | `audio.transcribe` |
| text spoken aloud (voiceover, TTS) | `audio.speak` |
| a live voice agent or live translation | `audio.agent` |

Mixed requests: classify by the **hardest deliverable** ("build an app that also generates logos" → `code.build`, then route the logo separately as `image.generate`). It's fine — and often cheaper — to return two routes for two phases.

## 2. Complexity
| Level | Signals |
|---|---|
| simple | One step, one file, under ~50 lines, a short answer; obvious once you know the facts |
| moderate | A few files/steps; needs judgment; typical daily work (default when unsure) |
| complex | Many files or steps, unfamiliar codebase, production stakes, subtle bugs, strict constraints, long documents |
| frontier | Multi-hour autonomous work, novel research, problems other models already failed, correctness-critical math/proofs |

Bump up one level if: the user mentions production/money/security/legal, or previous attempts failed. Bump down if: it's a prototype, a draft, or "quick".

## 3. Priority
- `quality` — "best", "most accurate", "critical", "for a client/investor", previous failures
- `cost` — "cheap", "budget", "free tier", "thousands of", "bulk", "at scale"
- `speed` — "fast", "real-time", "latency", "quick reply", live chat/voice
- `balanced` — everything else (default)

## 4. Provider
- Running inside Claude Code / claude.ai → the in-session answer is Anthropic; still show the best OpenAI option for reference.
- Running inside ChatGPT / Codex → OpenAI first.
- The user named a vendor or has only one API key → filter to it.
- Image and audio tasks are OpenAI-only in this registry (Claude doesn't generate media). Video generation has no model in the registry since OpenAI shut down the Sora 2 API (2026-09-24): route the *prompt writing* and say a generator choice comes in phase 2. Say this plainly.
- Otherwise `any`.

## When to ask
Ask at most **two** short questions, and only if the answer would change the model tier or the prompt materially (e.g. "Is this for production or a prototype?", "Roughly how many items?"). Otherwise state your assumptions in one line and continue.
