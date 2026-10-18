# Template: long-running agents & computer use (agent.longrun, agent.computer)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| OUTCOME | The end state, concretely | (required) |
| SPEC | Everything the agent needs up front: requirements, acceptance criteria | Ask: agents fail on missing specs |
| BOUNDARIES | What it may touch, what needs approval (deploys, payments, deleting, emailing) | Read/write in the workspace only; ask before anything external or irreversible |
| TOOLS | Repo, shell, browser, APIs, MCP servers available | Infer from environment |
| CHECKPOINTS | When to report progress or stop and ask | Report at each milestone; stop on ambiguity that changes the outcome |
| VERIFY | How it proves it's done | Tests/build pass + a short demo of the result |
| BUDGET | Time or token ceiling | None; suggest one for frontier tasks |

## Universal skeleton
```
OUTCOME: <end state>
FULL SPEC:
- <requirement / acceptance criterion>
BOUNDARIES: Allowed: <...>. Ask first: <...>. Never: <...>.
TOOLS: <...>
WORK STYLE: Plan briefly, then execute. Keep a running task list. After each milestone, verify before moving on.
CHECKPOINTS: <...>
VERIFY: <...>
FINAL REPORT: what's done, how it was verified, what's left or uncertain.
```

## Rendered for Claude
```xml
<outcome>OUTCOME</outcome>
<spec>FULL SPEC: give it all up front; long runs work best with the whole picture at the start</spec>
<boundaries>BOUNDARIES</boundaries>
<working_style>
Plan briefly, then work through it. Verify each milestone with a real check before moving on.
Give a one-line progress update at each milestone.
If something ambiguous would change the outcome, stop and ask; otherwise make a reasonable choice and note it.
</working_style>
<done_when>VERIFY</done_when>
<final_report>Done / verified how / open items.</final_report>
```
Effort: medium for routine agent work, high/xhigh for long-horizon coding (see the routing). For computer use, give it a way to zoom/crop screenshots for dense UIs.

## Rendered for OpenAI
```markdown
# Objective
OUTCOME

# Specification
FULL SPEC

# Boundaries
BOUNDARIES

# Agentic behavior
- Keep going until the objective is fully met; don't hand back early for confirmation on reversible steps.
- Ask only when a decision is irreversible or materially ambiguous.
- Before each tool call, state the purpose in one line. Keep a TODO list and update it.

# Verification
VERIFY

# Final message
Summary of what changed, how it was verified, open items.
```
Notes: OpenAI's guidance calls this "eagerness" (GPT-6 asks non-blocking questions by default). Explicitly say how persistent vs. how cautious the agent should be, and how many tool calls are reasonable.

## Token savers (biggest wins are here)
- **Prompt caching**: keep the system prompt and tool list byte-identical across turns. Agent loops resend the whole history every turn, and caching reprices it to ~10% of input cost.
- **Subagents / workers**: hand bulky, self-contained reading (search a codebase, read 50 pages) to a cheaper model and bring back a one-line result.
- **Narrow tools**: `get_order(id)` instead of `get_all_orders()`; give list tools `limit`/`fields` parameters.
- **Task budgets** (Claude API, beta): let the model pace itself against a token ceiling.
- **Batch** unattended runs (evals, backfills) for 50% off on both vendors.
