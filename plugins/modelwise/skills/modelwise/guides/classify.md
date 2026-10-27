# Classifying a raw prompt

Turn a basic prompt into seven values: **department**, **industry**, **market**, then **task**, **complexity**, **priority** and **provider**. Takes one pass; don't over-think it.

## 0. Department and industry (who owns this at a top company?)
| If the prompt is about… | Department |
|---|---|
| code, systems, infrastructure, security engineering | engineering |
| visuals, UI/UX, brand assets | design |
| campaigns, positioning, content, social, brand | marketing |
| prospecting, deals, proposals, pricing conversations | sales |
| replies to customers, help articles, onboarding, renewals | customer support and success |
| what to build, requirements, roadmaps, launches | product |
| hiring, policies, reviews, employee communication | HR and people |
| budgets, forecasts, reporting, accounting, unit economics | finance |
| contracts, policies with legal effect, privacy, regulatory | legal and compliance |
| processes, vendors, projects, SOPs, supply chain | operations and procurement |
| strategy, board material, OKRs, company-wide decisions | leadership and strategy |
| analysis, dashboards, research questions | data and research |

**Industry** comes from the prompt, the brand named, or the user's context (`guides/industry-lens.md`). If neither is clear and it changes the answer, it's one of your two questions; otherwise state the assumption.

**Market** is the country or region whose law and conventions apply. It comes from the prompt, the brand, the currency or the user's context.
- If it's unknown and the work is regulated (exits, pay or contracts in HR; ads for finance, health, crypto or alcohol; privacy; legal), it's one of your two questions, asked at the end of the answer.
- Meanwhile write "market: not specified" and apply no market-specific rule.
- Never assume a market from the examples in this skill's guides.

The department sets the top practitioner and their playbook (`guides/practice-functions.md` and the other practice guides). The **task** below is classified from the deliverable that practitioner decides on (SKILL.md step 2d). That can differ from the literal ask: "plan our hiring for next year" becomes a planning task (`reason.hard`) followed by writing (`text.write`).

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
| a live voice agent or live translation | `audio.agent` (for translation only, also name `gpt-realtime-translate`, which the router keeps below the bar for general agents) |

**Common department deliverables:**

| Deliverable | Task |
|---|---|
| Job description, policy, outreach email, support reply, help article, PRD, press release, executive memo | `text.write` |
| Contract review, redline, risk or policy gap check against a supplied document | `reason.hard`, because it means judging risk against a playbook; add `vision.understand` first if it's a scan |
| Summarising or simplifying a contract or policy, with no judgment | `text.transform` |
| Budget or forecast model, variance analysis, pipeline or churn analysis | `data.analysis` |
| Strategy, prioritisation, pricing decision, org design, scenario choice | `reason.hard` |
| Competitive or market scan, regulation lookup | `research.deep` |
| Triage or tagging of many tickets, CVs or invoices | `data.extract` |

**Social posts are visual by default.** "An Instagram / LinkedIn / Facebook post", "a post for our launch", or any post with a headline or on-image text means an image (`image.generate`, step 7 creative structure) plus a caption (`text.write`) as a second phase. Treat it as copy only when the user says so ("write the caption", "LinkedIn text post", "just the copy").

Mixed requests: classify by the **hardest deliverable** ("build an app that also generates logos" → `code.build`, then route the logo separately as `image.generate`). It's fine — and often cheaper — to return two routes for two phases.

## 2. Complexity
| Level | Signals |
|---|---|
| simple | One step, one file, under ~50 lines, a short answer; obvious once you know the facts |
| moderate | A few files/steps; needs judgment; typical daily work (default when unsure) |
| complex | Many files or steps, unfamiliar codebase, production stakes, subtle bugs, strict constraints, long documents |
| frontier | Multi-hour autonomous work, novel research, problems other models already failed, correctness-critical math/proofs |

Bump up one level if: the user mentions production/money/security/legal, the output goes to a board, investors, regulators or all employees, it affects people's jobs or pay, or previous attempts failed. Bump down if: it's a prototype, a draft, or "quick".

## 3. Priority
- `quality` — "best", "most accurate", "critical", "for a client/investor", previous failures
- `cost` — "cheap", "budget", "free tier", "thousands of", "bulk", "at scale"
- `speed` — "fast", "real-time", "latency", "quick reply", live chat/voice
- `balanced` — everything else (default)

## 4. Provider
- Running inside Claude Code / claude.ai → the in-session answer is Anthropic; still show the best OpenAI option for reference.
- Running inside ChatGPT / Codex → OpenAI first.
- The user named a vendor or has only one API key → filter to it.
- Image and audio tasks are OpenAI-only in this registry (Claude doesn't generate media). Video generation has no model in the registry since OpenAI shut down the Sora 2 API (2026-09-24): route the *prompt writing*, name the common generators as unranked options, and say ranked generator choices will come in a future registry update. Say this plainly.
- Otherwise `any`.

## When to ask
Ask at most **two** short questions, and only if the answer would change the model tier or the prompt materially (e.g. "Is this for production or a prototype?", "Roughly how many items?"). Otherwise state your assumptions in one line and continue.
