# How the top person in each business function works

For each function this guide gives six things:
- **Frame:** what they pin down before acting.
- **Frameworks:** what they actually use.
- **Deliverable:** what a top-quality one contains.
- **Refuse:** what they won't do.
- **Path:** how the work moves to production and who signs off.
- **Decisions:** the ones they make most, with the criteria.

Use the section for the prompt's department in SKILL.md step 2d, and put the parts that matter into the prompt. Market-specific law (employment, privacy, finance) lives in `guides/regulated.md`. Open it only when the prompt's market matches.

**Rules that hold in every function:**
1. **Triage first.** Is the request a draft, a decision or advice? Which market and industry? Who signs off? Is it irreversible, external or regulated?
2. **Never draft blind.** Ask for the facts that change the answer (the numbers, the jurisdiction, the contract type, the headcount), or state labelled assumptions.
3. **Answer first** (Minto's Pyramid Principle): the answer, then the reasons, then the evidence.
4. **The model never supplies facts it can't know.** That covers figures, citations, statutes, case names, thresholds and benchmarks. It writes `[VERIFY: …]` placeholders and a verify list instead. Courts have sanctioned lawyers for AI-invented case law (Mata v. Avianca, 2023; Ayinde v Haringey, 2025), and a consulting firm refunded part of a government fee over fabricated citations.
5. **Every artifact ends with a review block:** the owner who signs off, what to verify, what was assumed, and what this is not (for example, "not legal advice", "not an audit opinion").
6. **Confidential, personal and privileged data** stays out of tools the organisation hasn't approved.

Sources: Barbara Minto (Pyramid Principle), Center for Creative Leadership on SBI feedback (ccl.org), Sackett et al. 2022 on selection validity, SEC SAB 99 on materiality (sec.gov), AFP on driver-based planning (afponline.org), COSO internal control, ABA Formal Opinion 512 on generative AI, SRA guidance for solicitors, ISO 10013 on documented information, Richard Rumelt (Good Strategy/Bad Strategy), Amazon's narrative memos and PR/FAQ, John Doerr on OKRs.

More sources for the go-to-market functions: Gong Labs on discovery calls and cold-email CTAs (gong.io), Huthwaite on SPIN, April Dunford on positioning (aprildunford.com), Mark Ritson on marketing planning (marketingweek.com), Binet and Field (The Long and the Short of It), Google on incrementality testing, Gainsight on QBRs and onboarding, Bain on closing the loop, Zendesk on support replies, Amazon's Working Backwards PR/FAQ, Teresa Torres on opportunity solution trees (producttalk.org), Marty Cagan on the four big risks (svpg.com), Intercom on RICE.

**The pattern across go-to-market work:** diagnose before you produce. That means the buyer's problem before the pitch, the competitive alternative before the message, the outcome before the feature, and the customer's state before the reply.

---

## Sales
- **Frame:**
  - What stage is this? Cold outbound earns a conversation, an active deal needs a specific next step, and a pipeline review inspects evidence, not the story.
  - What's the segment? Enterprise deals with many stakeholders need heavier qualification; SMB and consumer sales need a short flow and a clear offer.
  - What's the pain, who owns it, what does doing nothing cost, and who decides?
- **Frameworks:**
  - **MEDDICC** for complex B2B deals: metrics, economic buyer, decision criteria, decision process, identified pain, champion, competition. Add the paper process (legal, security, procurement).
  - **BANT** only as a light screen for simple, transactional deals.
  - **SPIN** for discovery: few situation questions (research those beforehand), and spend the time on implication questions.
  - **Challenger:** lead with a commercial insight when the buyer thinks they already know what they need.
  - **Discovery craft** (Gong's call data): winning reps ask fewer, better questions, talk a little less, and paraphrase back to the buyer to confirm.
  - **Cold email:**
    - one problem hypothesis tied to a real trigger
    - one proof point
    - one low-friction interest CTA ("worth a conversation?"), which beat a specific-time ask in Gong's cold-email data
    - problem first; ROI language early lowered reply success
    - short: practitioners aim for under about 120 words
  - **Active deals:** a specific time and a mutual action plan (milestones, owners, dates, written with the buyer).
  - **Forecast categories:** pipeline, best case, commit. Inspect the deal data (stage history, slipped dates, activity) before the rep's story.
- **Deliverable:**
  - **Cold email:** the trigger, the problem, a proof point, one CTA.
  - **Discovery notes:** pain, impact in numbers, decision process, stakeholders, next step with a date.
  - **Proposal:** the buyer's own words on the pain, the quantified outcome, scope, price options, plan, and the paper-process steps.
  - **Pipeline review:** per deal, the evidence for its stage, the next step, the risk and the forecast call.
- **Refuse:**
  - Feature dumps before the pain is established.
  - "Hope this finds you well" openers.
  - Several CTAs in one message.
  - Invented personalisation or customer results.
  - Commit deals with no champion or no dated next step.
  - ROI promises with hidden assumptions.
- **Path:**
  - Reps work in the CRM and the sequencer; managers review calls.
  - Discounts go through the deal desk or finance, and non-standard terms through legal.
  - The forecast rolls up from manager to VP of sales to CFO.
- **Decisions:**
  - Qualify in or out: a quantified pain, access to the economic buyer, a decision process the buyer can describe.
  - Which next step: an interest CTA when cold, a specific time and a plan when there's an active buying process.
  - Forecast category: dated next step, champion, buyer-confirmed timeline, history of slips.

## Marketing strategy (plans, positioning, go-to-market, measurement)
Use `guides/practice-design.md` and `guides/practice-content.md` for the creative and the copy itself.
- **Frame:**
  - Is this strategy (where to play and how to win) or a tactic? Most requests arrive as tactics with no diagnosis behind them (Ritson).
  - What's the time horizon? Brand building is long; activation is short.
  - What's the business outcome, the budget and the target?
  - If nobody can explain why the product is different, fix positioning before messaging.
- **Frameworks:**
  - **Ritson's order:** diagnosis (market, customers, competitors, brand health), then strategy (target segment, positioning, objectives), then tactics and budget.
  - **Dunford's positioning steps, in order:**
    1. competitive alternatives, including doing nothing
    2. differentiated capabilities
    3. the value they enable
    4. the customers who care most
    5. the market category that makes the value obvious
    - Test the positioning with prospects; don't use a fill-in-the-blank statement.
  - **Rumelt's kernel** for the strategy itself.
  - **Binet and Field:** a long-term brand and short-term activation split of roughly 60/40 was optimal in the IPA databank. It's a correlational starting point, adjusted for category and sales cycle.
  - **Measurement:** triangulate attribution, media-mix modelling and experiments (holdout or geo tests). Last-click attribution over-credits sales that would have happened anyway.
- **Deliverable:**
  - **Marketing plan:**
    - a diagnosis with data
    - target segment and positioning (what, versus whom, for whom)
    - objectives tied to a lever (awareness, consideration, preference, repeat purchase)
    - tactics mapped to objectives, with costs and timing
    - the brand and activation budget split
    - a measurement plan
  - **Positioning document:** the five components, each with evidence from real deals.
  - **Campaign brief:** a single-minded proposition, the audience insight, the objective, the budget and the measurement, including whether an incrementality test is planned.
- **Refuse:**
  - Starting at tactics or tools.
  - Channel ROI claims based on last-click data.
  - Positioning against everyone.
  - A goal list presented as a strategy.
  - Optimising only for this quarter.
- **Path:**
  - The CMO or marketing director signs off, and finance approves the budget.
  - Analytics reviews the measurement plan.
  - Compliance reviews claims in regulated industries.
- **Decisions:**
  - Target and positioning: where the product is clearly better than the alternatives, for customers who care about that.
  - Brand versus activation split: start near 60/40 and adjust.
  - How to measure: experiment where possible, model the whole, use attribution for daily optimisation.

## Customer support and success
- **Frame:**
  - What state is the customer in, what exactly do they need to do or know, and can it be resolved now or only with a firm expectation?
  - Which segment (strategic, growth, SMB, at-risk)? It sets the depth of service.
  - Is the score or signal a trigger for a conversation?
- **Frameworks:**
  - **Support reply:**
    1. acknowledge the specific problem
    2. apologise and own it if the company is at fault
    3. resolve, or give the next steps and a time
    4. say how a repeat is prevented
    5. confirm and offer further help
    - Never open with policy. Empathy without a fix reads as filler.
  - **Help articles:**
    - a task title starting with a verb, in the customer's own words
    - one topic per article
    - symptoms and preconditions, numbered steps, expected result, what to do if it fails, last-reviewed date
  - **Onboarding:** a documented handoff from sales so customers don't repeat themselves, a week-one kickoff, dated milestones to first value, reviews around days 30, 60 and 90.
  - **Health score:** inputs weighted by what has actually predicted churn, retested over time.
  - **QBR** (Gainsight):
    - executive summary
    - key metrics
    - ROI with stated assumptions
    - progress against last quarter's goals
    - benchmarks and health
    - actions with owners
    - Book the next one before the meeting ends.
  - **CSAT and CES** per interaction, **NPS** for the relationship. Close the loop: contact unhappy customers within about 24 hours, and route the patterns to the team that owns the root cause (Bain).
- **Deliverable:**
  - **Reply:** the problem restated, numbered steps with no jargon, a next step with a time, an apology only when warranted, no overpromising.
  - **QBR:** the customer's goals, outcomes with evidence, risks, next quarter's plan, the asks.
  - **Onboarding plan:** goals, dated milestones, owners, a definition of first value.
- **Refuse:**
  - "Per our policy" or "unfortunately" as the opening.
  - Canned replies that ignore the specifics.
  - Promising outcomes or timelines the team doesn't control.
  - Reporting NPS without acting on it.
  - Individual financial, medical or legal advice in a support reply.
- **Path:**
  - QA samples replies against a rubric, and content owners review macros and articles on a schedule.
  - Escalation runs to tier 2, engineering or legal.
  - Refunds and credits follow the approval matrix.
  - In regulated industries, verify identity before discussing an account, and AI-drafted replies need accuracy checks and an escalation path.
- **Decisions:**
  - Resolve, escalate or decline: entitlement, severity and impact, whether it can be fixed now.
  - At risk or healthy: usage, support history, stakeholder changes, progress to value.
  - Who gets a QBR, and what's in it: segment and value, tied to the customer's goals.

## Product management
- **Frame:**
  - Is this a customer problem, a business outcome or a feature request?
  - Which of Cagan's four risks are open? Value and viability are the PM's; usability and feasibility are shared with design and engineering.
  - What decision should the document support: go or no-go, prioritisation, or alignment?
- **Frameworks:**
  - **Opportunity solution tree** (Teresa Torres):
    - one outcome
    - opportunities taken from customer interviews
    - one target opportunity at a time, with at least three candidate solutions compared
    - test the riskiest assumptions first
  - **Mom Test interviews:** ask about specific past behaviour, not opinions about your idea. Compliments are noise.
  - **Working Backwards PR/FAQ:**
    - a launch-day press release covering the problem, solution, quotes and how to start
    - an external FAQ, and an internal FAQ covering market, economics, risks and the top reasons it could fail
    - reviewers read silently before discussing
  - **RICE** = reach × impact × confidence ÷ effort. An input to judgement, not the answer.
  - **Metrics:** HEART (happiness, engagement, adoption, retention, task success), or a North Star metric that measures the value customers get. Every metric has a baseline and a target.
  - **Launch tiers** (full, moderate, minimal) by reach and risk. Each tier sets its own checklist; sales enablement is part of the launch.
- **Deliverable:**
  - **One-pager or PRD:**
    - the problem, with evidence
    - target customer and outcome
    - success metric with baseline and target
    - the solution at the level needed to decide
    - non-goals
    - risks and assumptions mapped to the four risks
    - open questions with owners
    - the go or no-go ask
  - **Interview guide:** past-behaviour questions only.
  - **Launch plan:** tier, audience, message, enablement, dates, owners, metrics and a hold or rollback criterion.
- **Refuse:**
  - Solution-first specs with no customer problem.
  - Leading interview questions.
  - Treating a RICE score as truth.
  - Metrics with no baseline.
  - A PR/FAQ that sells instead of seeking the truth.
- **Path:**
  - The product trio (PM, designer, tech lead) shapes it, and engineering confirms feasibility.
  - Product marketing owns the launch tier.
  - Legal and compliance review regulated claims; peers and then executives review a PR/FAQ.
- **Decisions:**
  - Which problem to pursue: link to the outcome, evidence from interviews, size of the need. Effort comes later.
  - What to build first: RICE inputs plus the four risks, dependencies, and the cheapest test of the riskiest assumption.
  - Build, test more or stop: whether the riskiest assumptions held, and the unit economics.

---

## HR and people
- **Frame:**
  - What decision or outcome is this for, and in which jurisdiction(s)?
  - Is the person an employee or an applicant, who is the audience, and what's the risk if it's wrong?
  - For exits, classify the type first: resignation, dismissal, contract end or redundancy all follow different rules.
- **Frameworks:**
  - **Structured hiring.** A scorecard of mission, outcomes and competencies, and fixed questions scored on anchored scales. Interviewers score independently before the debrief. Structured interviews are among the strongest predictors of job performance (Sackett et al., 2022).
  - **SBI feedback** (Situation, Behaviour, Impact; Intent as an optional fourth step).
  - **Pay communication:** the rationale, the person's position in the range, and a pay-equity check behind it.
  - **Policy structure:** purpose, scope, eligibility, process, exceptions, roles, breach, review date.
- **Deliverable:**
  - **Job description:** outcomes for the first 12 months, must-haves separated from nice-to-haves, competencies tied to interview questions, inclusive wording, and a pay range where the law requires one.
  - **Interview kit:** 4–6 competencies, 2–3 behavioural questions each, anchored 1–5 scoring, red flags, a debrief template.
  - **Review:** SBI examples and forward-looking expectations.
  - **Exit communication:** the decision, effective date, pay and benefits, next steps and a named contact, plus a manager script and FAQ. Short and unambiguous.
- **Refuse:**
  - Labels ("lazy") instead of behaviours.
  - Criteria that stand in for protected traits (age, gender, marital status, caste, religion).
  - Fully automated rejection without meaningful human review.
  - Invented policy numbers or legal thresholds.
  - Reasons for an exit beyond the approved ones.
- **Path:**
  - The HR business partner drafts and the HR lead reviews.
  - Employment counsel reviews anything sensitive, especially exits and policies with legal effect.
  - The line leader signs off.
  - **Gates:** adverse-impact check on selection, calibration of ratings, pay-equity check before pay changes. Layoffs go to counsel before anyone is told.
- **Decisions:**
  - Hire or not: evidence from independent scorers against the scorecard.
  - Who is affected by a restructure: objective, justifiable criteria, an impact analysis, notice and consultation timing, alternatives considered first.
  - Pay or promotion: market data, internal equity, performance evidence and budget, with the rationale documented per person.

## Finance (FP&A, accounting, reporting)
- **Frame:**
  - What decision will this number support?
  - What's the time basis (actual, budget, forecast) and the accounting basis (management view, IFRS, US GAAP, local standards)?
  - Who's the audience, and what's the materiality threshold?
  - Keep facts, commentary, forecasts and assumptions visibly separate.
- **Frameworks:**
  - **Driver-based planning.** Each P&L line built from the operational drivers behind it, and back-tested against actuals.
  - **Three-statement model** (P&L, balance sheet, cash flow) when the question is runway, financing or covenants.
  - **Variance analysis.** Split the gap into price, volume, mix, cost and FX components that add up to the total. Flag variances on both an amount and a percentage threshold. Comment on each one: driver, size, recurring or one-off, owner, next action.
  - **Unit economics** by segment, never blended. CAC fully loaded with salaries and tools. LTV on gross margin, not revenue. Payback in months.
  - **Scenarios:** base, upside and downside for 6–12 months, showing cash and runway, with the assumptions that move each one.
  - **Materiality is more than a size test** (SEC SAB 99). A small item matters if it flips a loss to a profit, hides a trend, touches a covenant or affects executive pay.
  - **Controls:** segregation of duties, reconciliations, review of unusual entries.
- **Deliverable:**
  - The answer and the ask in the first lines.
  - A bridge chart that ties exactly to the total.
  - KPIs defined consistently (formula, source, period).
  - Assumptions and sensitivities, with actuals clearly separated from forecasts.
  - Cash, runway and covenant headroom.
  - An audit trail: source, version, preparer, reviewer, reconciliation to the ledger.
- **Refuse:**
  - Plugs that force a model to balance.
  - Blended averages that hide a weak segment.
  - "Typical" benchmarks presented as the company's own figures.
  - Invented numbers. The model builds the structure and formulas; the data comes from the ledger or the user.
  - Personal investment advice.
- **Path:**
  - The analyst prepares, the finance manager reviews, the controller or head of FP&A approves, and the CFO signs off.
  - External figures go through the audit committee.
  - **Gates:** reconciliation, flux review, model checks (balance check, cash tie-out).
- **Decisions:**
  - Approve or revise a budget: driver-based, consistent with run-rate, and the downside case is survivable.
  - Investigate a variance: threshold, trend, qualitative materiality, controllability.
  - Invest, hire or cut: payback, margin, scenario results, runway.

## Legal and compliance
- **Frame:**
  - Who's the client or business owner, and which side are we on?
  - Which jurisdiction and governing law, which contract type, what deal value and deadline?
  - Is the output a review aid, a draft or advice? A qualified lawyer owns the advice, and AI output is never final.
  - Check confidentiality and privilege before anything goes into a tool.
- **Frameworks:**
  - **Contract playbook:** preferred position, fallbacks, escalation triggers and approval path.
  - **Risk tiers:** green (approve), amber (manager review), red (senior counsel).
  - **Deviation labels:** accepted, fallback, escalate, rejected, needs commercial approval.
  - **Issues ranked by materiality,** so the fatal ones aren't lost among cosmetic ones (over-flagging makes reviewers ignore alerts).
  - **Key clauses:** liability cap, indemnity, IP, data protection, termination and renewal, governing law, payment, assignment, confidentiality.
  - **Privacy:** lawful basis, impact assessment, data-subject rights, automated decisions. The specific law depends on the market (`guides/regulated.md`).
- **Deliverable:**
  - **Contract review:** a bottom line (sign / sign with changes / don't sign); a ranked issue table (clause, risk, why it matters, our position, fallback, approver); proposed redline language; open questions; assumptions (governing law, deal size).
  - **Policy draft:** the text plus a list of legal points to verify per jurisdiction.
  - **Every legal assertion** has a real source or is marked `[VERIFY]`.
- **Refuse:**
  - Presenting output as final legal advice.
  - Any citation, case or statute that hasn't been checked.
  - Confidential or privileged material in unapproved tools.
  - Unqualified answers on limitation periods or statutory thresholds.
- **Path:**
  - A first-line reviewer applies the playbook.
  - A lawyer reviews amber and red items, and the general counsel approves red and non-standard terms.
  - Outside counsel handles novel, high-value or regulated matters.
  - **Gates:** citation check, deviation log, privilege check, sign-off by a qualified lawyer for anything external.
- **Decisions:**
  - Sign, negotiate or walk away: red issues against deal value and authority limits.
  - Escalate or handle in-house: liability, privacy, regulatory or litigation exposure.
  - Whether a compliance step is required (impact assessment, notice, consent, breach report).

## Operations and procurement
- **Frame:**
  - What's the business need, outcome, budget and timeline?
  - What's the spend category and how critical is it? Who's the incumbent, and what's the risk if a supplier fails?
  - What compliance constraints apply (sanctions, data, anti-bribery)?
  - For a problem, define it with data before looking for causes.
- **Frameworks:**
  - **RFP with criteria and weights fixed before issue** and stated in the RFP. Quality is scored separately from price. Evaluators score independently, then reach consensus.
  - **SOP:** a header (ID, version, owner); purpose; scope and exclusions; roles; definitions; numbered steps; exceptions and escalation; revision history. Walk it end to end before approval.
  - **SLAs** define the metric, how it's measured, the data source, the frequency and the consequence. KPIs are internal.
  - **Root cause:** 5 Whys for a linear chain, a fishbone diagram for many factors. Never stop at "human error".
  - **Projects:** RACI, a living risk register (risk, likelihood, impact, owner, response), and a status report with an honest red/amber/green rating.
- **Deliverable:**
  - **RFP:** objectives, must-have versus nice-to-have requirements, timeline, response format, weighted criteria, terms, Q&A process.
  - **Vendor scorecard:** anchored scores, evidence, a separate price score, due diligence (finances, references, security, compliance), and a recommendation with trade-offs.
  - **Root-cause report:** problem with data, timeline, method, verified root cause, corrective and preventive actions with owners and dates, a check that the fix worked.
  - **Status report:** RAG status, progress against plan, top risks, decisions needed, next steps with owners.
- **Refuse:**
  - Lowest price at the expense of quality.
  - Changing criteria after seeing bids.
  - SLA metrics nobody can measure.
  - Blaming a person instead of the process.
  - Hiding a red item.
  - Invented supplier facts or certifications.
- **Path:**
  - The requester defines the need and procurement runs the process.
  - A cross-functional panel scores, and approval follows the delegation-of-authority limits.
  - Legal reviews the contract, security and privacy review data handling, and finance approves the budget.
- **Decisions:**
  - Which vendor: weighted fit, total cost of ownership, viability, risk.
  - Build, buy or renew: total cost, strategic value, switching cost, lock-in.
  - Escalate, stop or re-baseline a project: variance against tolerance, and the decision the sponsor must make.

## Leadership, strategy and executive communication
- **Frame:**
  - What decision is being asked of whom, and by when?
  - What does the audience already know, and what's the single message?
  - Diagnose before prescribing; Rumelt names the diagnosis as the step most often skipped.
  - Choose the format: decision memo, strategy memo, board pack, or OKRs.
- **Frameworks:**
  - **Rumelt's kernel:**
    - **Diagnosis:** the core challenge.
    - **Guiding policy:** the approach, including what it rules out.
    - **Coherent actions:** steps that reinforce each other.
    - Bad strategy is fluff, goals dressed up as strategy, or a long list of unrelated initiatives.
  - **Pyramid Principle and SCQA** (situation, complication, question, answer). The supporting points don't overlap and leave nothing out (MECE).
  - **Amazon-style narrative memo:** up to six pages of prose, read in silence at the start of the meeting. **PR/FAQ** for a new product: a press release written as if from launch day, plus FAQs.
  - **OKRs:** a few objectives, 2–4 measurable key results each, owners, a review cadence.
- **Deliverable:**
  - **Executive summary:** the answer, the ask and the deadline in the first lines, with at most three reasons.
  - **Decision memo:**
    - context
    - options, including doing nothing
    - recommendation and trade-offs
    - risks and mitigations
    - cost and resources
    - success metrics
    - what we won't do
    - a clear approval request
  - **Board pack:** a one-page summary, financials, KPIs, risks and the decisions needed.
- **Refuse:**
  - Jargon in place of a diagnosis.
  - A goal presented as a strategy ("grow 20%").
  - Burying the ask.
  - Invented market data or quotes.
  - Forecasts presented as certain.
- **Path:**
  - The author drafts and a peer pressure-tests the logic.
  - Finance ties the numbers to source, and legal reviews anything external or forward-looking.
  - The executive owner signs off, then the board or committee approves.
- **Decisions:**
  - What to do and not do: fit with the diagnosis, impact against cost, reversibility, capacity.
  - Invest, pivot or stop: evidence against success metrics, unit economics.
  - Approve a plan: holds in the downside, coherent with the strategy, an owner for each action.
