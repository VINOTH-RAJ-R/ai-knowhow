# How to prompt OpenAI models (GPT-6 and GPT-5.x)

Sources are linked at the bottom. OpenAI's guidance changes with each generation, so this is the current state as of the date in each model card's `verified` field.

## The shape GPT models like

OpenAI's current guidance prescribes **no fixed template and no XML requirement**. Clear Markdown sections work well and are what OpenAI's own GPT-5.5 guide uses:

```markdown
# Role
One or two sentences: who the model is acting as.

# Goal
The outcome.

# Success criteria
What "done" looks like, how it's checked.

# Constraints
Hard rules only. Keep "always/never/must" for true invariants.

# Context
Pasted material, files, data (static content first, so caching works).

# Output
Exact shape. For machine-readable output, use Structured Outputs instead of describing JSON.

# Stop rules
When to stop, and when to ask instead of acting.
```

GPT-5.4's guide also popularized XML-style blocks such as `<output_contract>`, `<completeness_contract>`, `<verification_loop>`, `<tool_persistence_rules>` and `<research_mode>`. They still work as clear section markers. Use whichever style is consistent.

## Rules that matter most (GPT-6 Astra / Sol / Luna)

1. **Goals and constraints over recipes.** Describe the outcome and the definition of done. Spell out the full loop for agents (implement → run → inspect → fix), not every keystroke.
2. **Tune autonomy explicitly ("eagerness").**
   - *More autonomous:* "Infer intent, bias toward action, finish the task. Go ahead with reversible, read-only, or already-authorized steps without asking."
   - *More cautious:* "Do the authorized prep work, then stop and ask for approval with a concrete, reviewable result."
   - Astra asks non-blocking questions by default, so say which you want.
3. **Remove old crutches.** OpenAI's GPT-6 migration advice: drop required-reading lists, "double-check / run the tests" reminders, heavy "ask first" wording, and long overlapping skill descriptions. The model already does these, and the extra text distracts it.
4. **Say which instructions win.** When combining skills, AGENTS.md and user requests, state that the user's instructions override skill guidance when they conflict.
5. **Formatting.** Astra leans toward lists and tables. If you want prose, ask for "concise paragraphs, one idea each, main point first; lists only for parallel or sequential items; no nested lists; no filler transitions."
6. **Length.** Use the `text.verbosity` parameter (low/medium/high) for the default level of detail, and the prompt for task-specific length ("under 150 words", "3 sections").
7. **Thinking depth = `reasoning.effort`, not words.** Don't ask for chain-of-thought in the output. Reasoning models think internally.
8. **Caching.** Put static content (instructions, examples, documents) first and the changing request last. Keep a stable `prompt_cache_key`. Don't put the current date or time at the top.
9. **Narrow clarifying questions only.** Ask only when the missing information materially changes the answer.
10. **Tool preambles.** For agents, ask for a one- or two-sentence purpose line before tool calls, so humans can follow along.

## Effort cheat sheet (OpenAI's own recommendations)

| Effort | Use for |
|---|---|
| `none` | Voice, fast retrieval, classification (only on models that support it) |
| `low` | Extraction, routing, routine rewrites, drafting, tool use, customer support, execution-style coding |
| `medium` | Default. Agentic coding, research, long-horizon delegation |
| `high` | Complex debugging, deep planning |
| `xhigh` | Deep research, long async workflows, security/code review, only when evals justify it |
| `max` | The most complex tasks (GPT-6 / GPT-5.6) |

Also:
- **Pro mode:** `reasoning.mode: "pro"` on GPT-5.6 and GPT-6 for the hardest problems.
- **Codex:** OpenAI suggests starting **Luna at High** and **Astra at Low (Light)**.
- **Changing effort mid-conversation (GPT-6):** send a `configuration_update` input item rather than changing the request-level effort, so the prompt cache survives.

## Codex-specific
- A good Codex prompt names the behavior you want, points to the code or repro steps, keeps the important constraints, and says how to verify the change.
- Use `/plan` for multi-step work and `/goal` for persistent goals.
- Ask it to re-run the repro, lint, and the smallest relevant tests, and to report the commands it ran.

## Images (GPT Image 2.5): see `templates/image.md`
Scene → subject → key details → constraints. Exact text in quotes. For edits, "change only X, keep everything else the same", with one change per turn.

## Sources
- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/api/docs/guides/prompt-guidance
- https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- https://developers.openai.com/api/docs/guides/reasoning
- https://learn.chatgpt.com/docs/prompting (Codex)
- https://developers.openai.com/api/docs/guides/image-prompting
