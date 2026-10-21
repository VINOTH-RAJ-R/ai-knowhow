# How senior engineers specify a coding task

A junior prompt says "build X". A staff engineer's brief says what "done" means, what is out of scope, what can go wrong, how it ships, and how it will be checked. Use this guide for every coding, frontend, debugging and agent task. Put the parts that matter for this task into the prompt; drop the rest. A one-line fix doesn't need a design section.

Sources: Google design docs (industrialempathy.com/posts/design-docs-at-google), Google code review guide (google.github.io/eng-practices), Google SRE launch checklist (sre.google/sre-book/launch-checklist), OWASP threat modeling, Martin Fowler on parallel change, feature toggles, YAGNI and technical debt (martinfowler.com), Stripe on idempotency, online migrations, API versioning and its ledger (docs.stripe.com, stripe.com/blog, stripe.dev/blog), Anthropic's Claude Code best practices (code.claude.com/docs/en/best-practices), Addy Osmani on specs for AI agents, Simon Willison on "vibe engineering", DORA capabilities (dora.dev).

## The core brief (every coding prompt)

1. **Outcome and context.** What changes for which user or system, in two lines. Name the stack and versions, the files or modules involved, and an existing pattern to follow ("follow the structure of `payments/refund.py`").
2. **Goals and non-goals.** Non-goals are things someone might reasonably expect but that are deliberately out of scope ("no UI changes", "no new dependency"). They stop scope creep, which matters more with AI than with people.
3. **Acceptance criteria as examples.** Input → expected output, including the error, edge and concurrency cases. Tests are the contract: "write a failing test that reproduces the bug, then fix it."
4. **Assumptions and questions first.** "List your assumptions and up to 3 blocking questions. If a change is irreversible (schema, data, public API), stop and ask."
5. **Non-functional requirements as numbers.** Latency (p95/p99), availability, throughput, data size, cost ceiling. Only the ones that matter for this task.
6. **Security.** Authentication and authorisation on every entry point, input validation, rate limits, secrets never in code, no personal data in logs. For anything exposed or sensitive, OWASP's four questions: what are we building, what can go wrong, what will we do about it, did we do a good job.
7. **Design depth proportional to ambiguity.** If the diff can be described in one sentence, skip the plan. Otherwise: two options with trade-offs, a recommendation, and a one-line decision record (ADR).
8. **Rollout.** Feature flag with an owner and removal date; expand → migrate → contract for any breaking schema or interface change; backward compatibility; rollback plan; the metric that says go or abort.
9. **Boundaries.** Always / ask first / never. Ask first before schema changes, new dependencies, CI edits, deleting data.
10. **Definition of done and evidence.** Tests, lint, type check and build pass; docs updated; alerts or dashboards updated where relevant; a short "how I verified" section with the commands run and their output; "known gaps".

## Industry overlays (add the one that applies)

### Fintech and payments
- **Money:** integer minor units plus currency code, an explicit rounding mode, never floating point.
- **Idempotency:** every money-moving or state-changing POST takes a client-generated idempotency key. Specify key scope, retention, what a retry with different parameters does, and what happens if a retry arrives while the first request is still running (Stripe's documented behaviour is the reference).
- **Ledger:** append-only, double-entry. Balances are computed from entries; mistakes are corrected with reversing entries, never by editing history.
- **Reconciliation:** against provider and bank files, with tolerance rules and alerts on breaks.
- **Webhooks:** verify the signature, deduplicate on a stable event key, acknowledge fast and process asynchronously, expect retries and out-of-order delivery.
- **Third-party APIs that aren't idempotent:** use your own unique reference (an order or receipt ID) as the key.
- **Audit trail:** who, what, when, before and after, correlation ID; never log card number, CVV, OTP or full account numbers.
- **Card data:** keep it out of your servers with tokenisation or hosted fields to shrink PCI DSS scope.
- **Maker-checker:** any manual action that moves money or changes limits needs a second approver and an audit record.

### Banking
- **Data location:** state where data is stored and processed; many regulators require some data to stay in-country.
- **Outsourcing and cloud:** contract SLAs, audit rights, incident reporting and an exit plan. Accountability stays with the bank.
- **Core banking integration:** an adapter layer, batch windows and end-of-day cut-offs, idempotent calls, and reconciliation against core postings.
- **Change management:** ticketed change, UAT sign-off, rollback plan, deployment window. Segregation of duties: developers don't deploy to production; approvals are logged.
- **Data handling:** classify data; personal and KYC data encrypted at rest and masked in non-production; audit logs immutable with a retention period.

### Investments, asset management and capital markets
- **Valuation and cut-off logic:** time zone, business-day calendar and the source of truth for the request timestamp. Cut-off rules vary by product and are set by the regulator, so they belong in configuration.
- **Recurring investments:** mandate lifecycle (registered, active, paused, cancelled, expired), debit date versus valuation date, failure and retry policy, customer notifications. Payment-rail limits change, so read them from configuration, not code.
- **Settlement files:** a transaction missing from a response file is not a success.
- **Registrar and custodian integration:** ask for the interface spec; plan reconciliation of holdings and reject handling.
- **Precision:** units and prices to the decimal places the fund administrator sets, with explicit rounding.
- **Audit:** every allotment and redemption traceable.

**Regulated domains in every overlay:** tell the model to flag every regulatory assumption for the user to confirm, and never to state limits or deadlines as fact. For a market covered by `guides/regulated.md`, add its engineering points.

### IT services and enterprise IT
- Follow the client's standards and existing architecture; prefer boring, supportable technology.
- **Handover is part of the deliverable:** README, runbook, architecture diagram, decision records, API docs.
- **Operations:** state SLAs, the support model and monitoring the client's ops team can use.
- **Change and release:** dev, UAT and production environments, release notes, rollback, client sign-off on acceptance.
- **Code:** readable by someone who didn't write it. Small modules, clear names, no clever abstractions, and a dependency and licence list.

### Startups
- Build the smallest slice that tests the riskiest assumption. Name the metric that decides keep, iterate or kill.
- **YAGNI:** don't build for needs that don't exist yet. YAGNI is not an excuse to skip tests or refactoring.
- **Technical debt** is fine when it's deliberate and prudent: record each shortcut as a TODO with an owner and a trigger to repay it.
- Use managed services instead of building infrastructure.
- **Never skimp on:** tests on money, auth and data-loss paths, secrets out of code, backups. A startup that handles payments or personal data still uses the fintech overlay.

## Working with an AI coding agent
- Give it a check it can run (tests, build, linter, screenshot) and ask for the output as evidence, not a claim that it works.
- Explore → plan → implement → verify. Skip the plan for one-sentence changes.
- One focused task per prompt. For a large feature: write the spec first, then implement in a fresh session.
- **Keep diffs small.** Stripe migrates in changes of a few hundred lines at most. Small batches are one of the DORA capabilities that offset AI-driven instability.
- **Review with fresh eyes.** Use a second session or reviewer told to flag correctness and requirement gaps only, not style, so it doesn't over-engineer. Don't merge code nobody can explain.
