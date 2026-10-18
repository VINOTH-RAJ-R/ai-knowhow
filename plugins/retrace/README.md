# retrace

**Turn finished AI work into lessons that teach people how it was done.**

AI can build an app, an image or a video in an afternoon, but the person who asked for it usually can't explain how. `retrace` fixes that. At the end of a task, it reconstructs from the evidence (conversation, commands, diffs, prompts, failed attempts):

- **the goal** and constraints
- **the approach**, step by step, with the tool and model used for each step
- **the decision log**: what was chosen, what else was considered, and why
- **the prompts that worked**, verbatim, and one that didn't
- **mistakes and fixes**: the real dead ends
- **an efficiency review**: where tokens and time went, and the cheaper path next time (uses `modelwise` if installed)
- **the reusable pattern**, check-your-understanding questions, and a hands-on exercise

It saves all of this as a **lesson skill** (`lesson-<slug>/SKILL.md` + `lesson.md`). The lesson is itself a skill, so anyone can later run `/lesson-<slug>` and be tutored through it: a quick overview, a step-by-step walkthrough with check questions, or a guided rebuild.

## Skills in this plugin
| Skill | Use |
|---|---|
| `retrace` | Capture a lesson after a task: `/retrace`, or "make a lesson from this" |
| `teach` | List and teach lessons: `/retrace:teach`, or "teach me how we built X" |

## Where lessons are saved
- Claude Code: `.claude/skills/lesson-<slug>/` in your project. Commit it and your team gets the lesson too.
- Codex: `.agents/skills/lesson-<slug>/`
- claude.ai / ChatGPT: you get the files to download. Zip the folder and upload it as a skill.

## Honesty rules
- Lessons are reconstructed from evidence. Rationale the record doesn't state is marked *(inferred)*. It is not a replay of the model's internal thinking.
- Secrets and personal data are redacted before anything is written.
- Alternatives that were never actually considered are labelled as expert suggestions, not presented as history.

## Example
[`examples/lessons/lesson-building-ai-knowhow`](../../examples/lessons/lesson-building-ai-knowhow/lesson.md) covers how this repository was built.

## Example prompts
1. `/retrace` (or "make a lesson from what we just did") at the end of a task. Writes `lesson-<slug>/` with `SKILL.md` and `lesson.md`.
2. "Teach me how we built the checkout flow" or `/lesson-checkout-flow` to be tutored through a lesson: overview, walkthrough with check questions, or a rebuild exercise.
3. "Which lessons do we have?" or `/retrace:teach` to list the lessons in this project and choose one.

## What it runs and sends
- Reads the conversation and, where available, local files and `git log` / `git diff` in your project. Writes the lesson files to the location described above.
- **No network access, no data collection.** It is instructed to redact secrets and personal data before writing anything. See [PRIVACY.md](../../PRIVACY.md).

## Support
Open an issue on the repository's GitHub Issues page.

## License
MIT. See [LICENSE](LICENSE). Not affiliated with Anthropic or OpenAI.
