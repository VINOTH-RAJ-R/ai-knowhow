---
name: modelwise-run
description: Route a prompt to the right Claude model and run it there, in Claude Code. It understands the prompt (department, industry, task, complexity), picks the Claude model and effort from the modelwise registry, rewrites the prompt in that model's preferred structure, shows the route, cost and prompt for the user's OK, then hands the task to a helper agent on that model and returns the result. Use when the user invokes /modelwise-run or /modelwise:modelwise-run with a prompt, or says "route and run this", "run this on the right model", "auto-route this", "use the cheapest model that can do this". For advice only (which model, a prompt to paste elsewhere, image or video prompts), use modelwise.
license: MIT
metadata:
  version: "0.3.4"
---

# Modelwise run: understand, route, structure, confirm, execute

The router, registry, guides and templates live in the sibling `modelwise` skill. Call that folder **MW**: `${CLAUDE_SKILL_DIR}/../modelwise`. Both the plugin and a personal install put the two skills side by side.

**Where it works.** Claude Code, where the Agent tool can start a helper on another model. Anywhere else (claude.ai, Cowork, Codex, or a Claude Code session with no Agent tool), say in one line that this surface can't hand work to another model, then answer with modelwise (follow `MW/SKILL.md`) instead.

**The session model does steps 1–4.** Keep them short. Tell the user once, in the confirm card, that running the session itself on Sonnet or Haiku keeps this routing step cheap.

## Step 1: Understand
Follow `MW/guides/classify.md` to get department, industry, market, task, complexity and priority. Keep the user's stated audience (`MW/SKILL.md`, step 2).
- Read only what you need to classify. If the task depends on project files, name the paths for the helper to read rather than pasting them.
- Never block on questions: assume, and list the assumptions in the confirm card.

## Step 2: Route
```bash
python3 "${CLAUDE_SKILL_DIR}/../modelwise/scripts/route.py" --task <task> --complexity <complexity> --priority <priority> --provider anthropic --json
```
- Take `recommended.model`, `recommended.effort`, `recommended.est_cost_usd`, `cheaper_option`, `stronger_option` and `cost_comparison`.
- **Not runnable on Claude** (`recommended` is null, or the task is `image.*`, `video.*` or `audio.*`): say so, and give the modelwise answer for that task (a prompt to paste into the named tool). In a mixed request, run only the phases Claude can do, and give the others as modelwise prompts.
- **Map the model to a runner.** Walk `ranked` from the top and take the first model whose id maps:

| Model id starts with | Runner agent | Agent `model` |
|---|---|---|
| `claude-haiku` | `modelwise-haiku` | `haiku` |
| `claude-sonnet` | `modelwise-sonnet` | `sonnet` |
| `claude-opus` | `modelwise-opus` | `opus` |
| `claude-fable` | `modelwise-fable` | `fable` |

  If you skipped a model (for example one Claude Code can't select), say which and why in the card.
- **Map the effort:** `none` and `minimal` become `low`; `low`, `medium`, `high`, `xhigh` and `max` pass through.

## Step 3: Structure the prompt
Build it as `MW/SKILL.md` step 5 does: the route's `template` (a path inside MW, such as `templates/coding.md`) and `MW/guides/prompt-style-anthropic.md`. The helper sees nothing of this chat, so the prompt must stand alone:
- the goal and what "done" means,
- the context: facts the user gave (verbatim), file paths to read, the stack or brand,
- the constraints and red lines from the expert lens,
- the output format,
- this line, always: "Don't commit, push, send, publish or delete anything; list those steps for the user instead."

## Step 4: Confirm (always, before running)
Show this card, then ask. Never run before an explicit yes.

```
**Route:** <task> · <complexity> → **<Model> @ <effort>** · est. $<cost> per run
**Compare:** <cheaper model @ effort> $<x> · <Opus @ high> $<y>   (list prices, before caching)
**Why:** <one line>
**Runs in:** helper agent `<runner>`. It can read and edit this project's files but can't see this chat.
**Assumptions:** <one line, or "none">
**Prompt it will get:**
<the structured prompt in a code block>
```

Ask with the AskUserQuestion tool when it's available, otherwise as the last line of your message, offering: **Run it** · **Use <stronger model>** · **Use <cheaper model>** · **Cancel**. If the user edits the prompt or picks another model, update the card and run on their choice; don't re-ask unless the change is large.

## Step 5: Execute
Call the Agent tool:
- `subagent_type`: the runner, as listed in the available agents (`modelwise:modelwise-sonnet` from the plugin, `modelwise-sonnet` from a personal install). If no runner is listed, use `general-purpose` and set `model` to the alias from the table.
- `effort`: the mapped effort. This skill is the explicit instruction to set it.
- `prompt`: the structured prompt. `description`: 3–5 words.

Wait for the result. Don't do the task yourself in parallel, and never predict the result before it arrives.

## Step 6: Report
- The result in full, as the helper returned it (code, text, findings). List files it created or changed. Check a claimed file change before repeating it.
- If the helper failed or the result is weak, say so plainly and offer a rerun on `stronger_option`. Ask first.
- Last lines:
  - `Ran on <Model> @ <effort> · est. $<cost> · <Opus @ high>: $<y> · <cheapest that clears the bar>: $<z>`
  - `modelwise-run v<version>`, using `metadata.version` from this file.

## Rules
- Only say a task ran on a model if the Agent call used that runner or `model`.
- Costs are the router's list-price estimates, not measured usage.
- The helper uses this session's permissions. Anything that commits, pushes, sends, publishes, deletes or buys still needs the user's own yes.
- One prompt, one route. For a multi-phase request, confirm each phase's route in the same card and run them in order, passing each result into the next prompt.
