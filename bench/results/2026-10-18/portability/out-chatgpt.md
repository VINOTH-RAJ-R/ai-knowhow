# Modelwise in a ChatGPT Project: three runs

(Simulated. Only the project files were used for model facts. The user has only OpenAI access, so each run uses the "Best OpenAI" column.)

---
# Message 1: "modelwise: regex to validate a UK postcode"

Classification: task = code.quick, complexity = simple, priority = balanced, provider = OpenAI only.
Assumptions: format validation only (not "does this postcode exist"); you didn't name a language, so I assume JavaScript-style regex that also works in Python.

## Recommendation
**Model:** GPT-6 Luna (gpt-6-luna, OpenAI): the fast tier clears the quality bar for a one-line regex at simple complexity, at under $0.01 per run.
**Effort:** low. In ChatGPT: pick GPT-6 Luna with Thinking set to low (the project files don't describe ChatGPT's picker labels, so use the lowest non-"none" Thinking setting your picker offers). Via API: reasoning.effort=low
**Cheaper:** none, Luna is already the cheapest tier in this row (the table shows "-")   **Stronger:** gpt-6.1-sol @ medium (the complex-row pick; the cost table also shows gpt-6-astra clearing the bar here at $0.06)

## Cost across models
code.quick, simple complexity:

| Model | Cost per run (simple) | Per 1,000 runs | Note |
|---|---|---|---|
| gpt-oss-120b | n/a | n/a | ✓ |
| claude-haiku-5-5 | <$0.01 | <$10 | ✓ |
| **gpt-6-luna** | **<$0.01** | **<$10** | **✓ (recommended)** |
| claude-sonnet-5-5 | $0.01 | $10 | ✓ |
| gpt-6.1-sol | $0.01 | $10 | ✓ |
| claude-opus-5-5 | $0.02 | $20 | ✓ |
| claude-fable-5-1 | $0.06 | $60 | ✓ |
| gpt-6-astra | $0.06 | $60 | ✓ |

(All rows carry ✓ in the simple column, so none is below the quality bar.)

## Your structured prompt
```markdown
# Goal
Write one regular expression that validates the format of a UK postcode. It is for a form field that should accept or reject user input.

# Context
Regex flavor: [[FILL: language / regex flavor, e.g. JavaScript, Python re, PCRE. Default if you leave this: JavaScript-compatible, no lookbehind]].
Existing code: none (new standalone snippet).

# Requirements
- Format check only: do not try to verify that the postcode really exists.
- Accept the standard outward + inward code shapes: A9 9AA, A99 9AA, AA9 9AA, AA99 9AA, A9A 9AA, AA9A 9AA, and the special case GIR 0AA.
- The space between outward and inward code is optional. Matching is case-insensitive.
- Anchor the pattern (^ and $) so partial matches fail.
- Do not use constructs that are unsafe for backtracking (no nested quantifiers).
- Keep the change minimal and focused: one pattern, no extra helpers.

# Done when
- The pattern accepts: "SW1A 1AA", "M1 1AE", "B33 8TH", "CR2 6XH", "DN55 1PT", "gir 0aa", "EC1A1BB".
- The pattern rejects: "", "12345", "SW1A 1A", "QV1 1AA", "SW1A  1AAA", "A9 9A".
- Run the examples above against the pattern (if you can run code) and report which passed. If you cannot run code, say so and walk through two accept cases and two reject cases by hand.

# Output
The regex in one code block, then the same regex as a ready-to-paste snippet in the chosen language, then a 3-line summary: what it accepts, what it deliberately does not check, how to test it.
```
Assumptions: language/flavor left as a [[FILL]] (default JavaScript); format-only validation; optional space; case-insensitive; the example postcodes are test cases I picked, edit as needed.

## Save tokens on this task
- Ask for the function or pattern only, with the exact output shape above, rather than a long explanation (output tokens cost 5x input).
- One task per conversation: start a fresh chat for this so no history is resent.
- Escalate on failure: run on Luna at low first, and re-run at the next level up only if the test cases fail.

## Why this works
The prompt states the outcome and a concrete definition of done (accept and reject lists) instead of telling the model how to build the pattern, which is what OpenAI's guidance prefers. The test cases turn "valid UK postcode" from a fuzzy idea into something checkable. Effort is set by the Thinking level and not by words in the prompt.

---
# Message 2: "modelwise: build a REST API in node for a todo app with auth and postgres"

Classification: task = code.build, complexity = moderate, priority = balanced, provider = OpenAI only.
Assumptions: "auth" pushes complexity up (security) but "todo app" pulls it down (prototype-scale), so I kept the default moderate. If this will hold real user data in production, bump to complex: gpt-6-astra @ high (see below).

## Recommendation
**Model:** GPT-6.1 Sol (gpt-6.1-sol, OpenAI): the balanced tier clears the quality bar for a multi-file API at moderate complexity, at about $0.24 per run.
**Effort:** medium. In ChatGPT: pick GPT-6.1 Sol with Thinking set to medium (picker labels are not in the project files; if you build it in Codex, the same model at medium). Via API: reasoning.effort=medium
**Cheaper:** gpt-6-luna @ medium (about $0.01 per run; the cost table shows it clearing the bar at moderate, and the table's own "Cheaper" pick, Haiku, is its Anthropic equivalent)   **Stronger:** gpt-6-astra @ high (about $5.00 per run, the complex-row pick)

## Cost across models
code.build, moderate complexity:

| Model | Cost per run (moderate) | Per 1,000 runs | Note |
|---|---|---|---|
| gpt-oss-120b | n/a | n/a | below quality bar |
| claude-haiku-5-5 | $0.01 | $10 | ✓ |
| gpt-6-luna | $0.01 | $10 | ✓ |
| claude-sonnet-5-5 | $0.24 | $240 | ✓ |
| **gpt-6.1-sol** | **$0.24** | **$240** | **✓ (recommended)** |
| claude-opus-5-5 | $0.48 | $480 | ✓ |
| claude-fable-5-1 | $1.20 | $1,200 | ✓ |
| gpt-6-astra | $1.20 | $1,200 | ✓ |

## Your structured prompt
```markdown
# Goal
Build a REST API for a todo app with user authentication, backed by PostgreSQL. Users register, log in, and manage only their own todos.

# Context
Stack: Node.js (current LTS), Express, PostgreSQL via the `pg` driver, SQL migrations as plain .sql files, JWT access tokens, password hashing with bcrypt (or argon2), validation with zod, tests with the built-in node:test runner plus supertest. [[FILL: swap any of these if you have a preference, e.g. Fastify, Prisma, Drizzle]]
Existing code: none (new standalone project).
Config comes from environment variables (DATABASE_URL, JWT_SECRET, PORT); provide a .env.example.

# Requirements
- Endpoints: POST /auth/register, POST /auth/login; GET/POST /todos, GET/PATCH/DELETE /todos/:id. A todo has id, title, completed, created_at, updated_at, user_id.
- Every /todos route requires a valid bearer token. A user can never read or change another user's todo (return 404, not 403, for someone else's id).
- Passwords are never stored or logged in plain text. Use parameterized queries only. Return consistent JSON errors with correct status codes (400, 401, 404, 409, 500).
- Add basic rate limiting on the auth routes.
- Layout: src/ (app, routes, db, middleware), migrations/, test/. Match common Node conventions; keep the change minimal and focused, no extra features.

# Done when
- `npm test` passes, covering: register, duplicate email (409), login success and failure, unauthenticated access (401), CRUD on own todos, and the cross-user access check.
- A README section lists the exact commands to create the database, run migrations, start the server and run the tests. Run the tests and linters you have available and report the results. If you cannot execute code, say exactly what you could not verify and list the commands I should run.

# Output
Full files for this new project (one block per file with its path), then a short summary of the structure and how to run it.
```
Assumptions: Express + pg + JWT + bcrypt + zod are my defaults, flagged in the prompt as swappable; email+password auth; new standalone project; full files because it is new code (template default); the "run the tests" line is adapted because plain ChatGPT chat usually cannot run Node.

## Save tokens on this task
- If you use Codex or another agentic tool, point it at paths instead of pasting files, and ask for diffs after the first scaffold.
- One task per conversation: build the scaffold in one chat, then start a fresh chat per later feature rather than dragging the history along.
- Escalate on failure: run at medium first and only move the failing part (for example the auth tests) up to high.

## Why this works
The prompt gives the model an outcome, the stack, hard security rules and an observable finish line (`npm test` with named cases), so it can run its own implement, run, inspect, fix loop without a step-by-step recipe. Putting the constraints in short bullets and the checks in "Done when" keeps invariants separate from preferences, which is the Markdown shape OpenAI's guidance recommends.

---
# Message 3: "modelwise: classify 50,000 support tickets into billing, bug, feature request, other - as cheap as possible"

Classification: task = data.extract, complexity = simple, priority = cost, provider = OpenAI only.
Assumptions: one label per ticket, four fixed labels, tickets are short text and not time-critical (so Batch API is fine). You didn't provide examples, so I left a [[FILL]] for them. I did not ask questions: volume and labels are already given.

## Recommendation
**Model:** GPT-6 Luna (gpt-6-luna, OpenAI): for cost priority the row's "Cheaper" cell is "-" (the fast tier is already the cheapest), so I used the Best OpenAI pick for this row, which is the fast tier at under $0.01 per run.
**Effort:** none. In ChatGPT: chat is the wrong tool for 50,000 items; if you only want to test, use GPT-6 Luna with Thinking off/minimal on a 50-ticket sample, and run the full job through the API. Via API: reasoning.effort=none, with the Batch API.
**Cheaper:** none, already the cheapest option in the row   **Stronger:** gpt-6.1-sol @ low (shown with ✓ in the cost table; the row does not list an effort for it, so I used low from the effort cheat sheet's "extraction" line)

## Cost across models
data.extract, simple complexity:

| Model | Cost per run (simple) | Per 1,000 runs | Note |
|---|---|---|---|
| gpt-oss-120b | n/a | n/a | ✓ |
| claude-haiku-5-5 | <$0.01 | <$10 | ✓ |
| **gpt-6-luna** | **<$0.01** | **<$10** | **✓ (recommended)** |
| claude-sonnet-5-5 | <$0.01 | <$10 | ✓ |
| gpt-6.1-sol | <$0.01 | <$10 | ✓ |
| claude-opus-5-5 | <$0.01 | <$10 | ✓ |
| claude-fable-5-1 | $0.02 | $20 | ✓ |
| gpt-6-astra | $0.02 | $20 | ✓ |

(All rows clear the quality bar at simple.)
Rough estimate for your actual job, from token-saving.md prices (Luna at $0.10 in / $0.50 out per M tokens). The "run" unit in the table is not defined, so this is my own arithmetic and not a table value. If each ticket is about 150 input tokens and 15 output tokens: about 7.5M input + 0.75M output is roughly $1.1 at standard rates and roughly half that through Batch (50% off). Ticket length is an assumption.

## Your structured prompt
Use Structured Outputs (Responses API, `text.format` with `type: json_schema`, `strict: true`) for the schema below. The prompt text:
```markdown
# Task
Classify each support ticket into exactly one category, following the rules.

# Categories
- billing: charges, invoices, refunds, payment failures, plan or pricing questions about money.
- bug: something is broken, errors, crashes, or the product behaves differently than documented.
- feature request: the customer asks for a new or changed capability.
- other: anything else (praise, how-to questions, account admin, spam, unclear).

# Rules
- Choose the single best category. If a ticket mixes several, pick the one the customer most wants resolved.
- If you cannot tell, use "other". Never invent new labels.
- Use only the ticket text. Do not guess hidden context.

# Examples
[[FILL: 2-5 real labelled tickets from your data, including one tricky or mixed one, e.g. a ticket about a failed payment caused by a bug]]
Format: <ticket id="e1">…</ticket> -> {"id":"e1","category":"billing"}

# Output
For each ticket, return {"id": <same id>, "category": "billing" | "bug" | "feature request" | "other"}. JSON only, one object per ticket, matching the schema.

# Input
<ticket id="1">…</ticket>
<ticket id="2">…</ticket>
```
Schema to pass as the Structured Outputs definition: an object with an array `results` of `{id: string, category: enum[billing, bug, feature request, other]}`, all fields required, additionalProperties false.
Assumptions: category definitions are my defaults, edit them to match your business; ambiguous tickets go to "other" (the template default is "unknown", but your label set is closed at four); 20 to 50 tickets per request, each with an id.

## Save tokens on this task
- Use the Batch API (50% off) since this isn't real-time, and put the instructions and examples first and keep them identical so they are cached; only the tickets change.
- Send several short tickets per request with ids, so the instructions are paid for once per batch of tickets and not once per ticket.
- Validate a 50-ticket sample at two effort levels (none vs low) before running all 50,000, and only escalate if the sample shows errors.

## Why this works
Classification needs a fixed label set, clear rules for edge cases and a few examples, not deep reasoning, so the cheapest tier at no reasoning effort is enough. Structured Outputs guarantees valid JSON, which removes retry costs. Keeping the instructions static and the tickets last lets caching and batching cut the price further.

---

RESULT 1 | task=code.quick | complexity=simple | priority=balanced | model=gpt-6-luna | effort=low | used_script=no | cost_table=yes
RESULT 2 | task=code.build | complexity=moderate | priority=balanced | model=gpt-6.1-sol | effort=medium | used_script=no | cost_table=yes
RESULT 3 | task=data.extract | complexity=simple | priority=cost | model=gpt-6-luna | effort=none | used_script=no | cost_table=yes

## FRICTION
- "In ChatGPT: which model and Thinking level to pick" has no source in the project files. Nothing maps API ids/effort values to ChatGPT's picker labels. I had to say "pick this model with Thinking at low/medium", with caveats, and could not name picker labels without using memory.
- The files and INSTRUCTIONS.md refer to scripts/registry (route.py, registry/tasks.json) that aren't in the project. The template paths (templates/coding.md) and classify.md's registry reference don't exist as named, so I used the flat files (coding.md, extraction.md). Harmless but confusing.
- ROUTING_TABLE.md's "Cheaper" column is Anthropic-only (haiku) or "-". For the OpenAI-only user I had to infer luna as the OpenAI equivalent (Msg 2), and for cost priority where Cheaper is "-" (Msg 1 and 3) I fell back to Best OpenAI. The instructions don't say what to do for that case. Same for "Stronger": it isn't defined in the table, so I used the next complexity row's Best OpenAI pick.
- The cost table's "per run" unit is undefined, so "Per 1,000 runs" is meaningless for a 50,000-ticket job. For "<$0.01" the 1,000-run column can only be "<$10", and gpt-oss-120b is "n/a". I added a clearly labelled rough estimate from token-saving.md prices.
- The effort for "Stronger" models in the data.extract row isn't given (the row only lists luna), so I used the effort cheat sheet.
- Instructions force the cost table "always", even when all rows tie at <$0.01 or include Anthropic models the OpenAI-only user can't use. I kept all rows as told.
- Complexity for "build a todo API with auth" is ambiguous: classify.md's "bump up for security" and "bump down for prototype" conflict. Chose moderate.
- coding.md's OpenAI template says "Run the tests and linters available", but ChatGPT chat can't run Node, so I added an "if you can't execute code, say so" line.
- extraction.md's default "ambiguous -> unknown" conflicts with the user's closed four-label set. I mapped ambiguous to "other".
- "Ask at most two questions" was moot because the user was unavailable; I used a [[FILL]] for language/flavor, ORM preference and examples instead.
