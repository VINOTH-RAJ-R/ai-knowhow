# modelwise skill: claude.ai chat simulation

Skill found at `/mnt/skills/user/modelwise/SKILL.md` (sandbox root). `route.py` ran fine with python 3.10 (`--provider any --json`) for all three prompts. Running model for this skill: Claude Sonnet 5.5 (the skill's recommended runner), so no frontier-model note is needed. Context is claude.ai chat, so the in-session answer is Anthropic; the best OpenAI option is shown for reference. All model cards verified 2026-10-17 (under 90 days old).

---
# PROMPT 1: "regex to validate a UK postcode"

Classification: task `code.quick`, complexity `simple`, priority `balanced`, provider `any` (claude.ai, so Anthropic first). Assumption: a standard-format validator (format only, not "does this postcode exist"), no language named, so JavaScript/Python-neutral PCRE-style regex.

## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, anthropic) - fast tier, fit 4/5, plenty for one regex; ties with GPT-6 Luna (openai) on fit and cost.
**Effort:** low (E2) - API: `output_config.effort=low` · App: claude.ai has no effort setting; pick the model in the model picker and leave Extended thinking off (only E4+ needs it). Claude Code: `/model haiku`, `/effort low`.
**Est. cost per run:** <$0.01 (about $0.0006; list price, before caching/batch)
**Cheaper:** none (already the cheapest tier; GPT-6 Luna @ low costs the same)   **Stronger:** Claude Sonnet 5.5 @ low (~$0.01) - fit 5/5, worth it if the regex must cover edge cases like GIR 0AA and Crown dependencies.
OpenAI reference: GPT-6 Luna @ `reasoning.effort=low`, same cost.

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 4 | <$0.01 ($0.0006) | $0.60 | **recommended** |
| GPT-6 Luna | low | 4 | <$0.01 ($0.0006) | $0.60 | tie, OpenAI |
| Claude Sonnet 5.5 | low | 5 | $0.01 ($0.012) | $12.00 | |
| GPT-6.1 Sol | low | 5 | $0.01 ($0.012) | $12.00 | |
| Claude Opus 5.5 | low | 5 | $0.02 ($0.024) | $24.00 | |
| Claude Fable 5.1 | low | 5 | $0.06 | $60.00 | |
| GPT-6 Astra | low | 5 | $0.06 | $60.00 | |
| gpt-oss-120b (open weight) | low | 3 | n/a (self-hosted / no list price in registry) | n/a | |

## Your structured prompt
```xml
<context>
I need to validate user-entered UK postcodes in a form. Wrong rejections annoy users, so the pattern should accept every real format.
</context>
<task>Write a regular expression that validates a UK postcode.</task>
<requirements>
- Language/engine: [[FILL: JavaScript / Python / PCRE / other]]
- Accept the standard formats (A9 9AA, A99 9AA, AA9 9AA, AA99 9AA, A9A 9AA, AA9A 9AA) and the special case GIR 0AA.
- Case-insensitive; the single space between outward and inward code is optional.
- Anchored to the whole string. Do not allow letters that are never used in the relevant position.
- Before saying it's done, run the regex against at least 8 valid and 8 invalid examples in the real engine and show the results. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>All valid examples match, all invalid examples fail, and the notes state what the pattern deliberately does not check (e.g. whether the postcode exists).</done_when>
<output_format>The regex in one code block, a short plain-English breakdown of its parts, then the test table.</output_format>
```
Assumptions: format validation only; engine left as `[[FILL]]`; no existence check.

## Save tokens on this task
- Ask for the regex plus a short test table, not an essay; one task per chat so no history is resent.
- Stay on the fast tier at low effort: effort is the main lever, and raising it for a regex rarely helps.
- If you need this validated against real data, paste 10 sample postcodes rather than describing the formats.

## Why this works
The tags split what you know (context) from what you want (task) and what "correct" means (requirements, done_when). Naming the engine and the special cases removes the two biggest sources of wrong regexes, and asking for a real test run makes the model prove it works instead of declaring it done.

---
# PROMPT 2: "build a REST API in node for a todo app with auth and postgres"

Classification: task `code.build`, complexity `complex` (moderate bumped up one level because auth/security is involved), priority `balanced`, provider `any` (claude.ai, Anthropic first). Assumptions: Express-style JSON API, email+password login with JWT, Postgres via `pg`, single service, no frontend.

## Recommendation
**Model:** Claude Opus 5.5 (`claude-opus-5-5`, anthropic) - flagship tier, fit 5/5; the auth and database parts are where subtle security mistakes happen.
**Effort:** high (E4) - API: `output_config.effort=high` · App: claude.ai - choose Opus 5.5 in the model picker and turn on Extended thinking (the skill's app setting for E4+). Claude Code: `/model opus`, `/effort high`.
**Est. cost per run:** $2.00 (list price, before caching/batch; assumes an agentic-sized run of ~300K input / 40K output tokens, a one-shot chat answer will cost far less)
**Cheaper:** Claude Sonnet 5.5 @ high ($1.00) - quality may drop a little.   **Stronger:** none above this in the registry for this task except Fable 5.1 / GPT-6 Astra @ high ($5.00), only worth it if Opus fails.
OpenAI reference: the router put no OpenAI model first; best OpenAI is GPT-6.1 Sol @ high ($1.00, fit 4.5).
If this is just a quick prototype: Claude Sonnet 5.5 @ medium, about $0.24 (tie: GPT-6.1 Sol @ medium).

## Cost across models
| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| Claude Haiku 5.5 | high | 3 | $0.05 | $50.00 | below quality bar |
| GPT-6 Luna | high | 3 | $0.05 | $50.00 | below quality bar |
| Claude Sonnet 5.5 | high | 4.5 | $1.00 | $1,000.00 | |
| GPT-6.1 Sol | high | 4.5 | $1.00 | $1,000.00 | |
| **Claude Opus 5.5** | high | 5 | $2.00 | $2,000.00 | **recommended** |
| Claude Fable 5.1 | high | 5 | $5.00 | $5,000.00 | |
| GPT-6 Astra | high | 5 | $5.00 | $5,000.00 | |
| gpt-oss-120b (open weight) | high | 2.5 | n/a | n/a | below quality bar |

## Your structured prompt
```xml
<context>
A small team needs the backend for a todo app. It will be called by a web client we are building separately. Users must only ever see and change their own todos, so correctness of auth and ownership checks matters more than extra features.
</context>
<task>Build a REST API in Node.js for a todo app with user authentication, backed by PostgreSQL.</task>
<requirements>
- Stack: Node.js [[FILL: version, default 22 LTS]], Express, `pg`, SQL migrations (plain SQL or node-pg-migrate), password hashing with argon2 or bcrypt, JWT access tokens. Tests with Vitest/Jest + supertest.
- Endpoints: POST /auth/register, POST /auth/login, GET/POST /todos, GET/PATCH/DELETE /todos/:id. Todos have id, title, done, created_at, updated_at, user_id.
- Every /todos route requires auth and is scoped to the authenticated user; accessing another user's todo returns 404.
- Security: parameterized queries only, input validation (zod or similar), secrets from environment variables (no defaults committed), rate limiting on auth routes, no password hashes or stack traces in responses.
- Config via `.env.example`; a docker-compose file for local Postgres.
Before saying it's done, run the migrations and the full test suite against a real Postgres and report the results. A syntax check doesn't count. If you can't run anything, say exactly what you couldn't verify.
</requirements>
<done_when>
- `npm test` passes, including a test proving user A cannot read, update or delete user B's todo.
- `docker compose up -d && npm run migrate && npm start` serves the API and a curl register -> login -> create todo -> list todos sequence works.
</done_when>
<output_format>Full files for a new project, grouped by path, then a 5-line summary of how to run it and what you chose and why (token expiry, hashing, error format).</output_format>
```
Assumptions: Express + JWT + argon2/bcrypt, no refresh tokens or email verification, local Docker for Postgres, new standalone project.

## Save tokens on this task
- Use an agentic tool (Claude Code) if you can: it reads and edits files itself and runs the tests, rather than you pasting files back and forth. In chat, ask for the project in one pass, then request diffs for changes.
- Plan strong, build cheap: have Opus produce the architecture and the auth module, then let Sonnet 5.5 or Haiku 5.5 write repetitive CRUD routes and tests.
- Escalate on failure: start at high (or medium if it's a prototype) and rerun only failing parts one level up; start a fresh chat for each new task.

## Why this works
The prompt states the outcome and the checks that prove it (ownership test, real migration run) instead of dictating each step, which suits current Claude models. Spelling out the security rules once stops the model from taking shortcuts like string-built SQL, and the "run it before saying done" line is the single most useful instruction for code tasks.

---
# PROMPT 3: "classify 50,000 support tickets into billing, bug, feature request, other - as cheap as possible"

Classification: task `data.extract`, complexity `simple` (single-label, four classes), priority `cost` ("as cheap as possible", 50,000 items), provider `any` (claude.ai, Anthropic first). Assumptions: tickets are short (~800 tokens each in the registry's "simple" estimate), one label per ticket, results needed as JSON, not real-time. Note: the router's "per run" cost here is per ticket.

## Recommendation
**Model:** Claude Haiku 5.5 (`claude-haiku-5-5`, anthropic) - fast tier, fit 5/5 for classification; ties with GPT-6 Luna (openai) on fit and cost.
**Effort:** low - API: `output_config.effort=low` (Haiku's lowest level; the router's E0 "none" maps to `low` on Haiku) · App: no setting in claude.ai chat, and chat is the wrong place for 50,000 tickets, so run this through the API. Claude Code: `/model haiku`, `/effort low`.
**Est. cost per run:** <$0.01 per ticket (about $0.0002), so roughly $7.50 for all 50,000 at list price; about $3.75 with the Batch API (50% off), less with prompt caching.
**Cheaper:** none (already the cheapest tier)   **Stronger:** Claude Sonnet 5.5 @ low ($0.0031 per ticket, about $155 for 50,000) - only if a 50-ticket sample shows Haiku mislabels the hard "other" cases.
OpenAI reference: GPT-6 Luna @ `reasoning.effort=none`, same cost.
If this is more complex than assumed (long, multi-issue tickets): Haiku 5.5 @ low at moderate size, about $0.0005 per ticket (about $25 for 50,000), same model.

## Cost across models
Per run = one ticket. Total for 50,000 tickets = per-1,000 value x 50.

| Model | Effort | Fit | Per run | Per 1,000 runs | Note |
|---|---|---|---|---|---|
| **Claude Haiku 5.5** | low | 5 | <$0.01 ($0.0002) | $0.15 | **recommended**, about $7.50 for 50,000 |
| GPT-6 Luna | none | 5 | <$0.01 ($0.0002) | $0.15 | tie, OpenAI |
| Claude Sonnet 5.5 | low | 5 | <$0.01 ($0.0031) | $3.10 | |
| GPT-6.1 Sol | low | 5 | <$0.01 ($0.0031) | $3.10 | |
| Claude Opus 5.5 | low | 5 | <$0.01 ($0.0062) | $6.20 | |
| Claude Fable 5.1 | low | 5 | $0.02 ($0.0155) | $15.50 | |
| GPT-6 Astra | low | 5 | $0.02 ($0.0155) | $15.50 | |
| gpt-oss-120b (open weight) | low | 3.5 | n/a (self-hosted) | n/a | |

## Your structured prompt
Put this in the API system prompt (stable, cached); only the ticket changes per request. Use structured outputs (`output_config.format` with a JSON schema) so the output is always valid.
```xml
<instructions>
Classify each support ticket into exactly one category. Follow the rules exactly and return only JSON matching the schema.
</instructions>
<schema>
{"id": string, "category": "billing" | "bug" | "feature_request" | "other"}
</schema>
<rules>
- billing: charges, invoices, refunds, payment methods, plans and pricing problems.
- bug: something that used to work or should work but fails, errors, crashes, wrong behavior.
- feature_request: asks for new or changed functionality that does not exist today.
- other: anything else (account access questions, praise, spam, unclear).
- If a ticket mixes categories, choose the one the customer needs resolved first.
- Ambiguous or empty tickets: "other".
</rules>
<examples>
[[FILL: 3-5 real, labelled tickets from your data, including one tricky mixed case, as <example><input>...</input><output>{...}</output></example>]]
</examples>
<ticket id="[[ID]]">[[TICKET_TEXT]]</ticket>
```
Assumptions: single label per ticket; category definitions above are my guess and should be adjusted to your product; examples must come from your data.

## Save tokens on this task
- Batch API for the whole run (50% off, results within a day), with the instructions and examples first and byte-identical so prompt caching applies.
- Fastest tier at the lowest effort, and send several short tickets per request (with ids) so the instructions are paid for once per batch.
- Validate a 50-ticket sample at low and medium effort before running all 50,000, and rerun only failures at a higher level.

## Why this works
Classification needs a clear definition of each label, not deep thinking, so a cheap fast model with a strict schema does it reliably. Keeping the fixed instructions first and the changing ticket last is what makes caching and batching cut the bill; a few real examples teach the edge cases better than more rules.

---
## FRICTION

- `${CLAUDE_SKILL_DIR}` stays literal in chat, as the skill warns. Using the skill's relative paths from its own folder worked; I did not run the suggested `find / -path "*modelwise/scripts/route.py"`, because it would search the real host filesystem here, not the sandbox. (In a real chat sandbox that command would work.)
- `route.py` has no volume or item-count option. For prompt 3 the "per run" figure is per ticket, so the 50,000-ticket total (and the Batch discount) had to be calculated by hand. The Step 5 format has no volume or total line.
- The cost estimate for `code.build` complex ($2.00 for Opus) assumes an agentic run of 300K input / 40K output tokens. In chat, one answer is much cheaper, so the figure overstates actual chat cost.
- The effort advice does not fit claude.ai chat well: only "Extended thinking on/off" exists, with no low/medium/high selector. For prompts 1 and 3 there is nothing to set. Batch API, structured outputs and `output_config.effort` are API-only, so prompt 3's best savings cannot be done in chat at all.
- Effort naming is inconsistent between routes: E0 "none" is shown as `low` for Haiku (no `none` level) but `none` for GPT-6 Luna, so the two tied rows show different efforts.
- Complexity bump for auth (prompt 2) jumps the route from Sonnet 5.5 @ medium ($0.24) to Opus 5.5 @ high ($2.00), roughly 8x. The classify guide's "bump up for security" rule is the only guidance; a plain todo-app API arguably stays moderate, so the "quick prototype" line carries a lot of weight.
- Template "Ask" slots conflict with "user unavailable": I used `[[FILL: ...]]` placeholders (engine in prompt 1; real labelled examples in prompt 3) instead of asking.
- Missing `cheaper_option` in the router output for the Haiku/Luna routes, so the "Cheaper:" line had to say "none" by hand.
- The skill cannot confirm which models claude.ai's picker actually offers (e.g. Haiku 5.5, Opus 5.5), so "pick it in the model picker" is unverified.
- Minor: a stale `__pycache__` (cpython-310) ships inside `scripts/`; harmless but should not be in a portable skill folder.

RESULT 1 | task=code.quick | complexity=simple | priority=balanced | model=claude-haiku-5-5 | effort=low | used_script=yes | cost_table=yes
RESULT 2 | task=code.build | complexity=complex | priority=balanced | model=claude-opus-5-5 | effort=high | used_script=yes | cost_table=yes
RESULT 3 | task=data.extract | complexity=simple | priority=cost | model=claude-haiku-5-5 | effort=low | used_script=yes | cost_table=yes
