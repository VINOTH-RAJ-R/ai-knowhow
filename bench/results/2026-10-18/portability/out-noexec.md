# Modelwise runs (no-exec fallback: ROUTING_TABLE.md + registry cards, nothing executed)

Method note: scripts could not run, so I classified by `guides/classify.md`, looked up task x complexity in `ROUTING_TABLE.md`, applied priority by hand, and opened the recommended model's card. Per-1,000-run figures are computed by hand: tokens from `registry/tasks.json` x list prices from the cards (Fable 5.1 and GPT-6 Astra are $10/$50 per M, 5x Sonnet/Sol). All cards verified 2026-10-17, so none is stale.

---

# Prompt 1: "regex to validate a UK postcode"

Classification: task `code.quick`, complexity simple (one step, short answer; moderate routes to the same model so no borderline line is needed), priority balanced, provider any. Assumption: JavaScript-flavoured regex, format validation only.

## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) - fast tier, fit 4/5 on quick code, and a regex is a one-step answer.
**Effort:** low (E2 low) - API: `output_config.effort=low` - App (Claude Code): `/model haiku` then `/effort low`; claude.ai: pick Haiku in the model menu, no extended thinking.
**Est. cost per run:** <$0.01 (list price, before caching/batch)
**Cheaper:** none - Haiku @ low is already the floor (GPT-6 Luna @ low is the same price)   **Stronger:** Claude Sonnet 5.5 @ medium ($0.08, complex tier) - only if you need every edge case checked against the official postcode spec.
Best OpenAI for reference: GPT-6 Luna (`gpt-6-luna`) @ low, <$0.01.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| gpt-oss-120b | low | 3 | n/a | n/a | self-host, no API price |
| **Claude Haiku 5.5** | low | 4 | <$0.01 | ~$0.60 | recommended |
| GPT-6 Luna | low | 4 | <$0.01 | ~$0.60 | same price |
| Claude Sonnet 5.5 | low | 5 | $0.01 | ~$12 | |
| GPT-6.1 Sol | low | 5 | $0.01 | ~$12 | |
| Claude Opus 5.5 | low | 5 | $0.02 | ~$24 | |
| Claude Fable 5.1 | low | 5 | $0.06 | ~$60 | |
| GPT-6 Astra | low | 5 | $0.06 | ~$60 | |

All rows clear the quality bar at simple.

## Your structured prompt
```xml
<context>
I validate postcodes on a signup form. Users type them in any case, with or without the space.
</context>
<task>Write a single regular expression that validates the format of a UK postcode.</task>
<requirements>
- JavaScript (ECMAScript) regex syntax, case-insensitive, anchored to the whole string, optional single space before the inward code.
- Cover the standard formats (A9, A99, A9A, AA9, AA99, AA9A outward codes + 9AA inward code) and the special case GIR 0AA. Reject invalid inward letters (C, I, K, M, O, V).
- Format check only. It does not need to prove the postcode exists.
Before you finish, run the regex against at least 8 valid and 8 invalid examples and show the results. A syntax check alone does not count; if you cannot run code, say which cases you could not verify.
</requirements>
<done_when>All valid examples match, all invalid examples fail, and "sw1a1aa" and "SW1A 1AA" both match.</done_when>
<output_format>The regex in a code block, a one-line explanation of each part, then a small valid/invalid test table.</output_format>
```
Assumptions: JavaScript flavour; format-only validation; case-insensitive with optional space. Replace the flavour if you use Python/PHP/etc.

## Save tokens on this task
- It is a one-shot answer: use a fresh chat and do not paste docs or the Royal Mail spec; the prompt already names the formats.
- Ask only for the regex, the explanation and a short test table, not a full tutorial (output tokens cost 5x input).
- If the first answer fails a test, re-run once at the next effort level (medium) instead of starting on a bigger model.

## Why this works
The prompt states the outcome (one regex) and the hard constraints (flavour, formats, what counts as invalid), so the model does not guess the dialect. The done-when line gives it a checkable target, and asking it to run real test cases catches the usual edge-case misses.

---

# Prompt 2: "build a REST API in node for a todo app with auth and postgres"

Classification: task `code.build`, complexity moderate (a few files, standard pattern, but auth needs judgment; it is borderline complex because of the security aspect), priority balanced, provider any. No production stakes were stated, so I kept moderate.

## Recommendation
**Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic) - fit 4.5/5 on building features at about a fifth of Opus cost; GPT-6.1 Sol is the equal-priced OpenAI option.
**Effort:** medium (E3 medium) - API: `output_config.effort=medium` - App (Claude Code): `/model sonnet` then `/effort medium`; claude.ai: choose Sonnet 5.5 and turn on extended thinking only if the first answer is wrong.
**Est. cost per run:** $0.24 (list price, before caching/batch)
**Cheaper:** Claude Haiku 5.5 @ medium ($0.01) - fit 3/5, fine for a plain CRUD API but more likely to miss auth details.   **Stronger:** Claude Opus 5.5 @ high ($2.00) - when the auth/security bar is high.
If this is just a quick prototype or learning exercise (simple): Claude Haiku 5.5 @ low (<$0.01).
If this is production-critical (complex): Claude Opus 5.5 @ high ($2.00); cheaper variant Sonnet 5.5 @ high ($1.00).
Best OpenAI for reference: GPT-6.1 Sol @ medium ($0.24).

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| gpt-oss-120b | medium | 2.5 | n/a | n/a | below quality bar; self-host |
| Claude Haiku 5.5 | medium | 3 | $0.01 | ~$12 | cheaper option |
| GPT-6 Luna | medium | 3 | $0.01 | ~$12 | needs higher effort for coding (card) |
| **Claude Sonnet 5.5** | medium | 4.5 | $0.24 | ~$240 | recommended |
| GPT-6.1 Sol | medium | 4.5 | $0.24 | ~$240 | same price |
| Claude Opus 5.5 | medium | 5 | $0.48 | ~$480 | stronger |
| Claude Fable 5.1 | medium | 5 | $1.20 | ~$1,200 | overkill here |
| GPT-6 Astra | medium | 5 | $1.20 | ~$1,200 | overkill here |

## Your structured prompt
```xml
<context>
New standalone project, no existing code. It is a backend for a todo app used by several users, so each user must only see and change their own todos. The next developer should be able to run it from the README alone.
</context>
<task>Build a REST API in Node.js for a todo app with user authentication, backed by PostgreSQL.</task>
<requirements>
- Stack: Node.js [[FILL: version, default 22 LTS]], Express, `pg` (no ORM), `jsonwebtoken`, and a password hashing library (argon2 or bcrypt). Tests with Node's built-in test runner or Jest plus supertest.
- Auth: register and login with email + password; login returns a JWT; todo routes require it. Passwords are hashed, never logged or returned.
- Todos: create, list (own only), get, update, delete, mark complete. Return 404 (not 403) for other users' todos.
- Postgres: SQL migration file for the schema, parameterised queries only, connection settings and the JWT secret from environment variables (provide `.env.example`, never hardcode secrets).
- Validate request bodies and return consistent JSON errors with correct status codes.
Before saying it is done, run a real check: start a test Postgres (Docker or local), run the migration and the test suite, and fix failures. A syntax check does not count. If you cannot run Postgres, say exactly which parts were not verified.
</requirements>
<done_when>`npm test` passes, covering register, login, auth-required rejection, CRUD, and one user being unable to read another user's todo.</done_when>
<output_format>Full files for the new project, then a 3-line summary of how to set up, migrate and run it.</output_format>
```
Assumptions: Express + `pg` + JWT with email/password; Node 22; no refresh tokens, roles or rate limiting (add them to the requirements if needed). Fill in the Node version and any framework preference.

## Save tokens on this task
- Run it in Claude Code so the agent writes files and runs the tests itself; do not paste the generated code back into chat.
- One task per session: add refresh tokens, rate limiting, etc. in fresh sessions with a diff-only request.
- Escalate on failure: if tests still fail at medium, re-run only that step at high rather than rerunning the whole build on Opus.

## Why this works
The prompt states the outcome and the hard constraints (stack, auth rules, data isolation, secrets) and leaves the step-by-step plan to the model, which plans well at this level. The done-when line, plus the instruction to actually run migrations and tests, matters most at medium effort, where Sonnet may otherwise report "done" without running anything.

---

# Prompt 3: "classify 50,000 support tickets into billing, bug, feature request, other - as cheap as possible"

Classification: task `data.extract`, complexity simple (four fixed labels, short inputs; moderate routes to the same model so no borderline line is needed), priority cost ("as cheap as possible", bulk volume), provider any. Cost priority was applied by hand (the table lists balanced picks): the cheapest priced model that clears the bar is a tie between Haiku 5.5 and GPT-6 Luna ($0.10 / $0.50 per M); I chose Haiku because the main route is Anthropic and the in-session answer is Anthropic. gpt-oss-120b is excluded because it has no API price.

## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, Anthropic) - fast tier, fit 5/5 on extraction/classification at the lowest list price.
**Effort:** low (E0 none, Haiku has no off switch so low is the floor) - API: `output_config.effort=low` plus structured outputs (`output_config.format` JSON schema) - App: this is a bulk job, so use the API/Batch API rather than a chat app; in Claude Code use `/model haiku` and `/effort low` only to prototype on a sample.
**Est. cost per run:** <$0.01 per ticket (about $0.00016 each on the registry's 800 in / 150 out estimate). For the 50,000 tickets: about $8 at list price, about $4 on the Batch API, less with cached instructions. This is an estimate from the generic token counts; real tickets may be longer or shorter.
**Cheaper:** GPT-6 Luna @ none (same price; `none` skips reasoning tokens and its cached input is $0.01/M, so it may come out slightly lower)   **Stronger:** Claude Sonnet 5.5 @ low (~$155 for 50,000, about 20x) - only if a 50-ticket sample shows Haiku mislabelling ambiguous tickets.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| gpt-oss-120b | low | 3.5 | n/a | n/a | self-host, no API price; you pay for hardware |
| **Claude Haiku 5.5** | low | 5 | <$0.01 | ~$0.16 | recommended; 50,000 tickets ~ $8 |
| GPT-6 Luna | none | 5 | <$0.01 | ~$0.16 | tie on price; `none` available |
| Claude Sonnet 5.5 | low | 5 | <$0.01 | ~$3.10 | ~20x Haiku |
| GPT-6.1 Sol | low | 5 | <$0.01 | ~$3.10 | no `none` level on this model |
| Claude Opus 5.5 | low | 5 | <$0.01 | ~$6.20 | |
| Claude Fable 5.1 | low | 5 | $0.02 | ~$15.50 | ~100x Haiku |
| GPT-6 Astra | low | 5 | $0.02 | ~$15.50 | `none` returns HTTP 400 |

All rows clear the quality bar at simple.

## Your structured prompt
Put the instructions and examples first and keep them byte-identical across requests (for caching); only the tickets change.
```xml
<instructions>
Classify each support ticket into exactly one category. Follow the rules exactly and return JSON only, matching the schema.
</instructions>
<rules>
- billing: charges, invoices, refunds, payment failures, plan or subscription pricing problems.
- bug: something that is broken or behaving differently from what the product should do (errors, crashes, wrong results).
- feature_request: asks for a capability that does not exist yet, or a change to how something works by design.
- other: anything else (account questions, how-to, praise, spam, unclear).
- If a ticket mixes topics, choose the category of the main thing the customer wants fixed.
- If you cannot tell, use "other". Never invent new categories.
[[FILL: any company-specific rules, e.g. "chargeback mentions are always billing"]]
</rules>
<examples>
[[FILL: replace with 4 real labelled tickets, one per category, including one tricky/ambiguous case]]
<example><input>I was charged twice for March</input><output>{"id":"ex1","category":"billing"}</output></example>
<example><input>The export button throws an error and nothing downloads</input><output>{"id":"ex2","category":"bug"}</output></example>
<example><input>Please add dark mode to the dashboard</input><output>{"id":"ex3","category":"feature_request"}</output></example>
<example><input>Can I change the email on my account?</input><output>{"id":"ex4","category":"other"}</output></example>
</examples>
<output_format>
One JSON object per ticket: {"id": "<ticket id>", "category": "billing" | "bug" | "feature_request" | "other"}. Enforce this with structured outputs (JSON schema, category as an enum) instead of relying on the prompt.
</output_format>

<ticket id="[[ID]]">[[TICKET TEXT]]</ticket>
(You can send 10-20 tickets per request, each with its own id, and return an array.)
```
Assumptions: four categories exactly as you named them (key `feature_request`); ambiguous means "other"; one label per ticket; no confidence score. Please supply real labelled examples and any company-specific rules.

## Save tokens on this task
- Use the **Batch API** (50% off all tokens) since 50,000 tickets are not needed in real time, and cache the instructions + examples block (put it first, keep it identical).
- Fast tier + lowest effort + structured outputs: no retries for malformed JSON, and no reasoning spend on a four-way label.
- Send 10-20 tickets per request with ids to amortise the instructions, and truncate very long tickets (first ~1,500 characters is usually enough to label).
- Validate a 50-ticket sample at two effort levels (or Haiku vs Sonnet) against your own labels before the full 50,000 run; only re-run failures on a stronger setting.

## Why this works
For bulk classification the schema is the product: a fixed set of labels, an explicit rule for ambiguity, and a few examples make the model's output predictable, so you can use the cheapest model with almost no thinking. Structured outputs guarantee valid JSON, and keeping the stable instructions first lets caching and batching drive the cost down.

---

RESULT 1 | task=code.quick | complexity=simple | priority=balanced | model=claude-haiku-5-5 | effort=low | used_script=no | cost_table=yes
RESULT 2 | task=code.build | complexity=moderate | priority=balanced | model=claude-sonnet-5-5 | effort=medium | used_script=no | cost_table=yes
RESULT 3 | task=data.extract | complexity=simple | priority=cost | model=claude-haiku-5-5 | effort=low | used_script=no | cost_table=yes

## FRICTION
- ROUTING_TABLE.md is balanced-priority only. For prompt 3 (priority=cost) I had to apply priority by hand and then open the Haiku, Luna and oss cards to compare prices. The skill says "cost -> the cheaper option" but gives no rule for ties (Haiku vs Luna are the same price) or for how to treat an unpriced model (gpt-oss-120b shows n/a but "clears" the bar). I excluded it and chose Haiku because of the Anthropic context; the router might have chosen differently.
- Per-run costs in the table are rounded ("<$0.01", "$0.01"), so "Per 1,000 runs" had to be computed by hand from tasks.json token estimates and card prices. I also had to infer Fable/Astra pricing from the cards ($10/$50) because the table only gives per-run rounded numbers. Figures like ~$0.16 per 1,000 are my arithmetic, not script output.
- The token estimate in tasks.json is per "run", not per item. For a 50,000-item batch job I extrapolated per-ticket cost from the "simple" estimate (800 in / 150 out); the skill gives no guidance for volume-based tasks, so the 50,000-ticket total is approximate.
- No per-row effort or fit in ROUTING_TABLE's cost table, so I rebuilt the Effort and Fit columns from effort-scale.json and the cards. The E0 mapping ("none" for OpenAI, "low" for Anthropic, but Sol has no `none` and Astra rejects it) required reading several cards to get right.
- Classification judgement: whether "auth" bumps the todo-API from moderate to complex was unclear (the bump rule mentions security but not a toy app); I kept moderate and added the "production-critical" line, which cost an extra table lookup. The skill's step 3 about running the router again with `--provider` is ambiguous when the user says "any vendor".
- The ROUTING_TABLE rows for balanced priority already point at the same model for simple/moderate in prompts 1 and 3, so the borderline-complexity rule was only needed for prompt 2.
- Total reading: SKILL.md, classify.md, ROUTING_TABLE.md, tasks.json, effort-scale.json, token-saving.md, prompt-style-anthropic.md, coding.md, extraction.md, and 8 model cards (about 17 files). Fine without scripts, but slower than a single route.py call.
