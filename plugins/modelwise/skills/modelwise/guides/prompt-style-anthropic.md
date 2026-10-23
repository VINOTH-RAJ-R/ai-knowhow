# How to prompt Claude models (2026 generation)

This guide applies to Claude Fable 5.x, Opus 5.x, Sonnet 5.x and Haiku 5.5. Sources: Anthropic's prompt engineering docs and the model migration guide (links at the bottom).

## The shape Claude likes

Claude reads XML-style tags as clear section boundaries. Use them to separate *what you know* from *what you want*:

```xml
<context>
Who this is for, what already exists, why the task matters.
</context>

<task>
The one thing to do, stated as an outcome ("Add CSV export to the reports page"),
not a list of keystrokes.
</task>

<requirements>
- Hard constraints (stack, versions, style, length, files it may/may not touch)
- What "done" means and how to check it
</requirements>

<input>
Pasted code, documents, data. Put long material here, ABOVE the question.
</input>

<output_format>
Exactly what to return: a diff, a JSON object matching a schema, 3 bullet options, a 200-word email.
</output_format>
```

Tag names are not magic. Any clear, consistent names work. Nest them when you have several documents (`<document index="1">…</document>`).

## Rules that matter most

1. **Say why.** One sentence of motivation ("this runs on a 512 MB device, so memory matters") beats five rules. Claude generalizes from reasons.
2. **Describe the outcome and the definition of done, not every step.** The 5.x models are strong planners. Over-scripted prompts written for older models measurably *reduce* quality on Fable 5.1 and Opus 5.5.
3. **Long inputs first, question last.** For prompts with large documents or code, put the material at the top and the instruction at the end.
4. **Show, don't just tell, for format.** One short example of the exact output shape is the most reliable formatting instruction. For machine-readable output use **structured outputs** (`output_config.format` with a JSON schema). Don't rely on prose.
5. **No shouting.** `CRITICAL`, `MUST`, and ALL-CAPS were workarounds for older models. The current models follow calm, plain instructions and over-apply shouted ones.
6. **Use effort to control thinking, not words.** To get less (or more) thinking, change the effort level. Prompt requests like "think less" have almost no effect on current models.
7. **Ask for verification on code.** "Run the tests / build / the changed command before saying it's done. A syntax check doesn't count." This matters most at low effort.
8. **Don't discourage tools.** Phrases like "minimize tool calls" are followed literally and cause the model to answer from memory. Say which sources it should prefer instead.
9. **For frontend and UI code, name what to avoid** (not for image-model prompts, which keep a generic Avoid line). "Avoid generic AI look" just swaps one default for another. List concrete patterns: "no cream background, no italic accent words in headlines, no pill buttons, no 01/02/03 section labels".
10. **No assistant prefill.** Prefilling the assistant turn returns an error on current models. Use structured outputs or a system-prompt instruction instead.

## System prompt vs user message

- **System prompt**: the stable part. Role, audience, house style, tools policy, output conventions. Keep it fixed across a session so prompt caching works.
- **User message**: the changing part. This task, this input.
- To change instructions mid-conversation via the API, append a mid-conversation system message rather than editing the original system prompt. That keeps the cache.

## Effort cheat sheet

| Model | Default | Start at | Notes |
|---|---|---|---|
| Fable 5.1 | high | low/medium for routine work | Always thinks. The most expensive tier, so measure before raising |
| Opus 5.5 | **medium** | medium | Opus 5.5 at medium beats Opus 5 at high on coding. Set it explicitly |
| Sonnet 5.5 | high | medium for coding/agents, low for chat/content/extraction | Levels recalibrated vs Sonnet 5 |
| Haiku 5.5 | **medium** | low for chat/high volume, medium otherwise | First Haiku with effort |

In **Claude Code**, set the model with `/model` and effort with `/effort`. In **claude.ai**, pick the model in the model menu and turn on extended thinking for harder tasks.

## Sources

- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- https://platform.claude.com/docs/en/build-with-claude/effort
- https://platform.claude.com/docs/en/about-claude/models/migration-guide
