---
name: retrace
description: Turn a finished AI-assisted task (an app, feature, fix, image, video, document, or analysis) into a reusable lesson skill that teaches a person how it was built — the goal, the decisions and why, the prompts that worked, the mistakes and fixes, and how to do it cheaper next time. Use when the user says "retrace", "make a lesson from this", "how did we build this", "teach me what you just did", "capture this for the team", or at the end of a task they want to learn from or hand over.
license: MIT
---

# Retrace — capture how it was built

You turn the work just done (in this conversation, or in a repo/transcript the user points to) into a **lesson**: a small skill folder that any person can later invoke to be *taught* how it was done.

File paths in this skill (`templates/…`, `guides/…`) are relative to this skill's folder: `${CLAUDE_SKILL_DIR}`. Where that variable isn't substituted (claude.ai, Codex), read them next to this SKILL.md.

The lesson must be truthful. It is reconstructed from evidence — the conversation, commands, diffs, prompts and outputs — not from imagination. Where you infer *why* something was done and the record doesn't say, mark it `(inferred)`.

## Step 1 — Gather the evidence

Collect, from what is available:

1. **The conversation**: the user's original request, clarifications, what was tried, what failed, what was finally accepted.
2. **The artifacts**:
   - Code: `git log --oneline -20`, `git diff --stat <start>..HEAD` where git is available; otherwise (claude.ai chat, Cowork) the files you created or edited in this conversation, and key snippets.
   - Images/video: every generation prompt in order, settings (model, size, quality, duration, seed), which outputs were kept and why the others were rejected.
   - Documents/analysis: the outline, sources used, revisions.
3. **The process**: tools and models used (and effort level, if known), commands run, errors hit and how each was fixed, rough time and token/cost signals if visible.

If the work happened outside this conversation, ask the user for the repo path, transcript, or prompt history — one question — unless they already pointed you to it or can't answer; then proceed with what you have.

Use the domain checklist in `guides/capture-checklist.md` (path: `${CLAUDE_SKILL_DIR}/guides/capture-checklist.md`) so nothing important is missed.

## Step 2 — Extract the lesson

Fill every section of the lesson template `templates/lesson.md`. The parts that make a lesson valuable, in order of importance:

- **Decision log** — each meaningful choice: what was decided, the options considered, why this one won, and what evidence settled it. This is the "thought process" a learner can't get from the final output.
- **Prompts that worked** — verbatim, with a note on *why* each worked. Include one that didn't and what changed.
- **Mistakes and fixes** — the real dead ends. Learners learn most here. Never hide them.
- **Efficiency review** — which model and effort were used, where tokens/time were wasted (long chats, pasted logs, wrong model tier, retries), and the cheaper path next time. If the `modelwise` skill is installed, name the model/effort it would recommend for each phase.
- **Reusable pattern** — the transferable recipe, stripped of project specifics.
- **Check-your-understanding questions** — 3–5 questions with answers, including one "what would you do if…" scenario.

Write for a smart person who wasn't there. Plain words, short sentences, explain jargon once.

**When the record is thin.** Write "not recorded" for anything the evidence doesn't show (models, effort, prompts, cost) rather than guessing. If nothing failed, say so plainly in *Mistakes and fixes* ("no failures were recorded") — don't invent dead ends. You may add *review findings* you discover by reading or running the code (bugs, edge cases, risks), clearly labelled as found during the retrace, not during the build; they are often the most useful part of the lesson.

## Step 3 — Redact

Before writing anything, remove secrets and personal data: API keys, tokens, passwords, connection strings, private URLs, emails/phone numbers of real people, customer data. Replace with `<REDACTED:API_KEY>` style placeholders. If redaction would break understanding, describe the value's shape instead ("a 40-char Stripe secret key").

## Step 4 — Write the lesson folder

Slug: short kebab-case from the outcome, e.g. `stripe-checkout-flow`, `product-hero-image`, `churn-analysis`.

Folder `lesson-<slug>/` containing:
- `SKILL.md` — from `templates/lesson-skill.md`, with name, description and title filled in. This makes the lesson invocable on its own and contains the tutoring protocol.
- `lesson.md` — the filled lesson.
- `artifacts/` — only small, useful files: final prompts, key code snippets, a before/after, a diagram. Never copy whole repos or large media.

Where to write it (first match wins):
1. A location the user named.
2. **Claude Code**: `.claude/skills/lesson-<slug>/` in the current project (shared with the team via git), or `~/.claude/skills/` if the user wants it personal.
3. **Codex**: `.agents/skills/lesson-<slug>/`.
4. **Cowork**: inside a folder the user has connected (e.g. `<connected folder>/lessons/lesson-<slug>/`), plus a `lesson-<slug>.zip` next to it.
5. **claude.ai chat** (or anywhere else): create the files as downloads, plus `lesson-<slug>.zip`.

Build the ZIP with the folder at the top level (`zip -r lesson-<slug>.zip lesson-<slug>/`, so it contains `lesson-<slug>/SKILL.md`). Tell the user they can upload it in claude.ai under **Customize → Skills → + → Upload a skill**, which makes the lesson available in chat, Cowork and (synced) Claude Code.

## Step 5 — Report

Tell the user, briefly: where the lesson was saved, the 3 most important things it teaches, and how to use it: in Claude Code `/lesson-<slug>`; in claude.ai chat or Cowork, upload the ZIP and then ask "teach me how we built <x>" (or type `/` and pick it). With the `teach` skill installed, `teach <slug>` works everywhere.

## Rules

- Evidence over storytelling. Don't invent alternatives that were never considered; if you add expert alternatives for teaching value, label them "Other options an expert might consider".
- Keep `lesson.md` under ~400 lines. Link to artifacts instead of pasting them.
- One lesson per coherent outcome. If the session built three unrelated things, offer three lessons.
