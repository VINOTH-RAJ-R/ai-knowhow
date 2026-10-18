---
name: teach
description: Tutor a person through any lesson created by retrace (a lesson-<slug> folder with lesson.md) — overview, step-by-step walkthrough with check questions, or a hands-on rebuild exercise. Use when the user says "teach me", "explain how we built", "onboard me to", "quiz me on", or names a lesson, or asks which lessons exist.
license: MIT
---

# Teach — learn from a retrace lesson

## 1. Find the lesson

Look for lesson folders (each has a `lesson.md`), in this order:
1. A path or name the user gave (`stripe-checkout-flow`, `lesson-stripe-checkout-flow`, or a folder path).
2. `.claude/skills/lesson-*/` and `.agents/skills/lesson-*/` in the current project.
3. `~/.claude/skills/lesson-*/` and `~/.agents/skills/lesson-*/`.
4. Any `lessons/` or `examples/lessons/` folder in the current project or a connected folder (Cowork).
5. Lesson skills enabled on the account (claude.ai chat and Cowork load them like any other skill), or a `lesson-<slug>.zip` / `lesson.md` the user attached.

If the user didn't name one, list what you found as `slug — title (domain, difficulty)` and ask which. If none exist, explain that lessons are created with the `retrace` skill after a task is finished.

## 2. Teach it

Read the lesson's `lesson.md` completely, then follow the teaching protocol in that lesson's own `SKILL.md` (modes: overview, walkthrough, rebuild). If the lesson folder has no `SKILL.md`, use this protocol:

1. Ask (once) for the mode: quick overview, full walkthrough, or rebuild it yourself.
2. Walkthrough: phase by phase — what, why, the real prompt/snippet, then a short check question before moving on.
3. Always cover *Mistakes and fixes* and *Efficiency review*.
4. End with *Check your understanding*, give feedback, and suggest how to apply the pattern to the learner's own work.

## 3. Rules

- Teach only what the lesson records; label general advice as such.
- Short turns. Wait for the learner between phases.
- If the learner is clearly advanced, compress; if lost, slow down and add an analogy.
