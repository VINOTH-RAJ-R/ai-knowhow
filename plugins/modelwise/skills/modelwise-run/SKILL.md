---
name: modelwise-run
description: Route a prompt to the right Claude model and run it there, in Claude Code. It understands the prompt (department, industry, task, complexity), picks the Claude model and effort from the modelwise registry, rewrites the prompt in that model's preferred structure, shows the route, cost, usage-limit check and prompt for the user's OK, then hands the task to a helper agent on that model and returns the result. Long jobs keep a checkpoint, so a stopped run continues cheaply with /modelwise-run continue. Use when the user invokes /modelwise-run or /modelwise:modelwise-run with a prompt, or says "route and run this", "run this on the right model", "auto-route this", "use the cheapest model that can do this", "continue the stopped run". For advice only (which model, a prompt to paste elsewhere, image or video prompts), use modelwise.
license: MIT
metadata:
  version: "0.3.9"
---

# Modelwise run: understand, route, structure, confirm, execute

The router, registry, guides and templates live in the sibling `modelwise` skill. Call that folder **MW**: `${CLAUDE_SKILL_DIR}/../modelwise`. Both the plugin and a personal install put the two skills side by side.

**Where it works.** Claude Code, where the Agent tool can start a helper on another model. Anywhere else (claude.ai, Cowork, Codex, or a Claude Code session with no Agent tool), say in one line that this surface can't hand work to another model, then answer with modelwise (follow `MW/SKILL.md`) instead.

**Continue mode.** `/modelwise-run continue [name]` picks up a stopped or phased job from its checkpoint (see "Checkpoints and continuing" below) instead of starting over.

**The session model does steps 1–4.** Keep them short. Tell the user once, in the confirm card, that running the session itself on Sonnet or Haiku keeps this routing step cheap.

## Step 1: Understand
Follow `MW/guides/classify.md` to get department, industry, market, task, complexity and priority. Keep the user's stated audience (`MW/SKILL.md`, step 2).
- Read only what you need to classify. If the task depends on project files, name the paths for the helper to read rather than pasting them.
- Never block on questions: assume, and list the assumptions in the confirm card.
- **Priority defaults to `balanced`.** Use `quality` only when the user asks for it ("best", "most accurate", "critical", "for a client or investor", "production") or a previous attempt failed. Use `cost` when they say "cheap", "budget" or "at scale". A task feeling important is not a reason for `quality`: the stronger model is one click away in the confirm card.
- **Complexity is the biggest cost lever.** Rate the size of the work, not how much it matters: one document or one page is usually `moderate`; many files, a whole codebase or a long autonomous run is `complex`. At `complex` the router needs a near-top fit, which usually means Opus.
- **Task ids come from the registry only:** the task table in `MW/guides/classify.md`, or `route.py --list-tasks`. Never invent an id (`review.code`, `writing.long_form`); if unsure, run `--list-tasks` first.

## Step 2: Route
```bash
python3 "${CLAUDE_SKILL_DIR}/../modelwise/scripts/route.py" --task <task> --complexity <complexity> --priority <priority> --provider anthropic --json
```
- Take `recommended.model`, `recommended.effort`, `recommended.agent_run`, `cheaper_option`, `stronger_option` and `cost_comparison`.
- **Price it as a helper run, not a chat answer.** A helper agent works in a loop of steps and re-reads the project each step, so use `agent_run` (`typical_usd`, `low_usd`–`high_usd`, `steps`) for every price in the card, never `est_cost_usd`. Measured runs cost 2–13× the old single-call figure.
- **Not runnable on Claude** (`recommended` is null, or the task is `image.*`, `video.*` or `audio.*`): say so, and give the modelwise answer for that task (a prompt to paste into the named tool). In a mixed request, run only the phases Claude can do, and give the others as modelwise prompts.
- **Map the model to a runner.** Walk `ranked` from the top and take the first model whose id maps:

| Model id starts with | Runner agent | Agent `model` |
|---|---|---|
| `claude-haiku` | `modelwise-haiku` | `haiku` |
| `claude-sonnet` | `modelwise-sonnet` | `sonnet` |
| `claude-opus` | `modelwise-opus` | `opus` |
| `claude-fable` | `modelwise-fable` | `fable` |

  If you skipped a model (for example one Claude Code can't select), say which and why in the card.
- **Borderline complexity:** if the task could fairly be one level lower, run the router at that level too and show it in the card as its own option (`If it's moderate: Sonnet @ medium, $0.28`).
- **Opus at a lower effort:** when the route is Opus at `high` or above, run the router again with `--effort-level E3` and show "Opus @ medium" as an option with its own range. Effort mostly changes the thinking, not the step count, so the saving is often small; show the real difference and don't promise more.
- **Stronger option:** if `stronger_option` is empty under `balanced`, rerun the router with `--priority quality` and offer its pick as the stronger button, with its cost.
- **Map the effort:** `none` and `minimal` become `low`; `low`, `medium`, `high`, `xhigh` and `max` pass through.

## Step 2b: Check the usage limit
If a usage tool is available (in the Claude desktop app: `get_usage` from the session-management tools), call it before showing the card. Take the percent used and reset time of the 5-hour and weekly windows, then run:
```bash
python3 "${CLAUDE_SKILL_DIR}/../modelwise/scripts/limit_check.py" --typical <typical_usd> --low <low_usd> --high <high_usd> --steps <a> <b> --pct-5h <pct> --resets-5h "<time>" --pct-week <pct> --resets-week "<time>"
```
It learns how much of each window a run takes from your own logged runs, so its verdict is one of:
- **learning:** fewer than 3 runs logged with usage. Show the headroom only, and say so.
- **fits** / **likely fits:** show the predicted share of the tighter window.
- **likely hits the limit:** say where it would probably stop, and propose phases that each fit (Checkpoints and continuing), or running after the reset.
If no usage tool is available or the plan limits don't apply (an API key), skip this step and say "Usage limit: not visible here" in the card.

## Step 3: Structure the prompt
Build it as `MW/SKILL.md` step 5 does: the route's `template` (a path inside MW, such as `templates/coding.md`) and `MW/guides/prompt-style-anthropic.md`. The helper sees nothing of this chat, so the prompt must stand alone:
- the goal and what "done" means,
- the context: facts the user gave (verbatim), file paths to read, the stack or brand,
- the constraints and red lines from the expert lens,
- the output format,
- this line, always: "Don't commit, push, send, publish or delete anything; list those steps for the user instead."
- for any run with `agent_run.warn` true, or any phased job, the checkpoint instruction: "Keep a checkpoint at `.modelwise/checkpoint-<name>.md` using the template below. Create it before you start, and update it after each phase or about every 25 steps, and before you stop for any reason. Add `.modelwise/` to `.gitignore` if it isn't there." followed by the contents of `${CLAUDE_SKILL_DIR}/checkpoint-template.md`.

## Step 4: Confirm (always, before running)
Show this card, then ask. Never run before an explicit yes.

```
**Route:** <task> · <complexity> → **<Model> @ <effort>** · typical $<typical>, range $<low>–$<high> (about <a>–<b> steps)
**Compare:** <cheaper model @ effort> typical $<x> · <Opus @ medium, when offered> typical $<y> · <stronger> typical $<z>   (list prices for a helper run)
**If it's simpler:** <route at one complexity level lower, with its typical cost>   (only when the task is borderline)
**Usage limit:** 5-hour <pct>% used (resets <time>) · weekly <pct>% · this run: <limit_check verdict, with the predicted share when known>   (from Step 2b)
**⚠ Big run:** up to $<high> at list price; on a Claude plan this can use a large share of your usage limit. A tighter scope cuts steps, and steps drive cost.   (only when `agent_run.warn` is true)
**Why:** <one line>
**Runs in:** helper agent `<runner>`. It can read and edit this project's files but can't see this chat.
**Assumptions:** <one line, or "none">
**Prompt it will get:**
<the structured prompt in a code block>
```

Ask with the AskUserQuestion tool when it's available, otherwise as the last line of your message, offering: **Run it** · **Use <cheaper model>** (or the one-level-lower route, when it's borderline) · **Use <stronger model>** or **Opus @ medium** (when offered) · **Cancel**. Keep it to four options. If the user edits the prompt or picks another model, update the card and run on their choice; don't re-ask unless the change is large.

## Step 5: Execute
Call the Agent tool:
- `subagent_type`: the runner, as listed in the available agents (`modelwise:modelwise-sonnet` from the plugin, `modelwise-sonnet` from a personal install). If no runner is listed, use `general-purpose` and set `model` to the alias from the table.
- `effort`: the mapped effort, on every call. This skill is the explicit instruction to set it. If this app's Agent tool has no `effort` parameter, or rejects it, run without it and record "effort: app default (couldn't be set here)". The report must describe the call as it was actually made.
- `prompt`: the structured prompt. `description`: 3–5 words.

Wait for the result. Don't do the task yourself in parallel, and never predict the result before it arrives.

**Batch small follow-ups.** Each run re-reads the whole project before it starts, so a chain of small runs costs far more than one run with all the changes. When the user asks for a small change right after a run, offer to collect it: **Add to batch** (hold it, and say how many are waiting) or **Run now**. Run the batch as one helper call when the user says go, or when a large change comes in.

**Follow-ups stay routed.** When the user asks for a fix, a change or the next step after a run, route it the same way and confirm with a one-line card (`Route: <task> → <Model> @ <effort> · est. $<cost> · Run it?`), or send it back to the same runner. The session model only does small checks itself: reading a result, listing files, viewing a screenshot. If the session itself is on Opus or Fable, say once that switching it to Sonnet (`/model claude-sonnet-5-5`) keeps follow-ups cheap.

## Checkpoints and continuing
**Why:** when a long run stops at the usage limit and is resumed hours later, the whole helper conversation is sent again with an expired cache, and every remaining step carries that large history. A fresh helper that starts from a short checkpoint re-reads a fraction of it.

- **Split before you start** when Step 2b says the run likely hits the limit, or when `agent_run.high_usd` is above twice the warn level. Propose phases that each fit, name the checkpoint (`.modelwise/checkpoint-<name>.md`) and confirm the phase plan in the card. Each phase is its own helper run with a fresh context: its prompt is the checkpoint plus that phase's goal, never the earlier helper's transcript. So when you split, the prompt in the card covers **phase 1 only** (with the whole phase plan written into the new checkpoint), and the helper stops when phase 1 is done and the checkpoint is updated. Never hand one helper all the phases "in order": that is the long run the split exists to avoid. After each phase, offer the next one as a one-line card (`/modelwise-run continue <name>`).
- **If a run stops mid-way** (usage limit, error, cancelled): report what the checkpoint says is done and next, and the reset time if it was the limit. Don't resume the old helper after more than a few minutes; start a fresh one from the checkpoint. Log the stopped run with `--outcome failed --checkpoint <path>`.
- **`/modelwise-run continue [name]`:** read `.modelwise/checkpoint-<name>.md` (list them if no name is given and there are several), check the limit (Step 2b), then route the "Next step" as a new run with a one-line card. The helper's prompt is: the checkpoint, the next phase's goal, and "Read only the files you need for this phase; update the checkpoint as you go."
- **Keep the main chat lean too:** between phases, keep only short summaries here. Results live in the files and the checkpoint, so a new chat can continue with `/modelwise-run continue`.

## Step 6: Report and log
- The result in full, as the helper returned it (code, text, findings). List files it created or changed. Check a claimed file change before repeating it.
- If the helper failed or the result is weak, say so plainly and offer a rerun on `stronger_option`. Ask first.
- **Log the run** (one local line, so quoted price can be checked against real usage later):
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/../modelwise/scripts/log_run.py" --task <task> --complexity <complexity> --priority <priority> --model <model id> --effort <effort as passed, or default> --typical <typical_usd> --low <low_usd> --high <high_usd> --outcome <finished|failed|cancelled> --desc "<the Agent description, 3–5 words>" --version <this skill's version> [--checkpoint <path>] [--plan <plan> --pct-5h-before <n> --pct-5h-after <n> --pct-week-before <n> --pct-week-after <n>]
  ```
  When a usage tool is available, read it again right after the run and pass the before and after percentages, so `limit_check.py` can learn how much of your limit a run takes. It writes only to `~/.claude/modelwise/runs.jsonl` on this machine, with no prompt text, and does nothing when `MODELWISE_LOG=0`. Log cancelled cards too (`--outcome cancelled`). `python3 "${CLAUDE_SKILL_DIR}/../modelwise/scripts/runs_report.py"` later compares each logged quote with the run's real token cost.
- Last lines:
  - `Ran on <Model> @ <effort as actually passed, or "app default"> · quoted typical $<typical> (range $<low>–$<high>) · <Opus @ high>: typical $<y> · <cheapest that clears the bar>: typical $<z>`
  - `modelwise-run v<version>`: copy the `version:` value from this file's frontmatter, as loaded. Never write it from memory or from another file; if you can't see it, run `grep -m1 'version:' "${CLAUDE_SKILL_DIR}/SKILL.md"`.

## Rules
- Only say a task ran on a model, or at an effort, if the Agent call actually set that runner or `model`, and that `effort`.
- Costs are the router's list-price estimates for a helper run, calibrated on measured runs, not a bill. On a Claude plan the real limit is your usage allowance.
- The helper uses this session's permissions. Anything that commits, pushes, sends, publishes, deletes or buys still needs the user's own yes.
- One prompt, one route. For a multi-phase request, confirm each phase's route in the same card and run them in order, passing each result into the next prompt.
