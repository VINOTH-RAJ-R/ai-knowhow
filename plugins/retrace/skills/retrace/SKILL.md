---
name: retrace
description: Retrace a finished AI-assisted task (an app, feature, fix, image, video, document, analysis or plan) and teach it. It reads the whole session, saves a lesson skill, and then walks the person through how the AI approached the work, from the visible record. It covers the goal, what the AI looked at, each decision and why, the turning points, the prompts that worked, the mistakes and fixes, and the cheaper path next time. It also teaches any saved lesson on request. Use when the user says "retrace", "teach me what you just did", "how did you arrive at this", "make a lesson from this", "capture this for the team", "teach me how we built X", "quiz me on", "onboard me to", or asks which lessons exist.
license: MIT
metadata:
  version: "0.3.6"
---

# Retrace: capture the work, then teach it

One skill, two modes:
- **Retrace and teach** (default, at the end of a task): gather the whole session, save a lesson, then teach it straight away.
- **Teach a saved lesson** (the user names a lesson, or says "teach me how we built X", "which lessons do we have?"): skip to Step 6.

**What the user always gets.** A saved lesson, then a lesson taught in the chat in plain, beginner-friendly words (Step 5). Retrace is a teacher looking back at finished work. It is never a status report, a project check, a list of "things to verify before you post", or a continuation of the original task. If the last thing you did was check or fix the work, stop doing that: the user is now asking to *learn* how it was done.

File paths in this skill (`templates/…`, `guides/…`) are relative to this skill's folder: `${CLAUDE_SKILL_DIR}`. Where that variable isn't substituted (claude.ai, Codex), read them next to this SKILL.md.

**Truthfulness.** Everything comes from the visible record: messages, files read and written, searches, commands and their outputs, prompts, errors and fixes. Teach the *approach*, meaning the observable decisions and the reasons the record gives for them. Never present a reconstruction as the model's private internal reasoning. Where you infer why something was done and the record doesn't say, mark it `(inferred)`.

**Which model.** Retracing a long session is reading and judgment over a lot of context. Sonnet at medium effort handles it well. Haiku is fine for short sessions; on a long one it can lose the thread. If you notice that, say so in one line and suggest rerunning on Sonnet, rather than giving a thin lesson.

## Step 1: Gather the whole context
**The conversation is the record.** Read the entire session from the first message, not just the last few turns. If earlier turns were summarized, use the summary as the record and say so in the lesson.

**Look, don't redo.** You may run at most five quick, read-only commands to confirm what exists: `git log --oneline -20`, `git diff --stat`, or a listing of the output folder. Never run builds, renders, type checks, tests, installs or verifications, and never inspect media files: the work is finished, and retrace explains it, it doesn't re-check it.

Collect:
1. **The request:** the user's original words, clarifications, constraints, and what "done" meant.
2. **What the AI looked at:** files read, searches and pages fetched, data inspected, research or sub-agents used, and what each one contributed.
3. **The moves:** each meaningful action in order: what was done, the tool or model used (and effort, if known), and what came back.
4. **Turning points:** where the plan changed: a failed attempt, a user correction, a test result, a new fact. Note what triggered each change.
5. **The artifacts:**
   - **Code:** `git log --oneline -20` and `git diff --stat` where git is available; otherwise, the files created or edited, as named in the conversation.
   - **Images and video:** every generation prompt, the settings, and what was kept or rejected and why.
   - **Documents and analysis:** the outline, sources and revisions.
6. **Cost signals:** models used, retries, long pasted context, time.

If the work happened outside this conversation, ask the user once for the repo path, transcript or prompt history, then proceed with what you have. Use `guides/capture-checklist.md` so nothing is missed.

## Step 2: Extract the lesson
Fill every section of `templates/lesson.md`. In order of value:
- **The moves** (*Step by step*): for each phase, what the AI looked at, what it decided, why (stated or `(inferred)`), and the result. Mark each turning point.
- **Decision log:** each meaningful choice, the options considered, why this one won, and the evidence that settled it.
- **Prompts that worked:** verbatim, with why each worked, plus one that didn't and what changed.
- **Mistakes and fixes:** the real dead ends. Never hide them. If none were recorded, say so; don't invent any.
- **Efficiency review:** models and effort used, where tokens and time went, and the cheaper path. If `modelwise` is installed, name its recommended model and effort for each phase.
- **Reusable pattern**, **check questions** (3–5, including one "what would you do if…") and **try it yourself**.

Write for a smart person who wasn't there: plain words, short sentences, jargon explained once. Write "not recorded" for anything the evidence doesn't show. You may add review findings you discover now (bugs, risks), labelled as found during the retrace.

## Step 3: Redact
Before writing anything, remove secrets and personal data: keys, tokens, passwords, connection strings, private URLs, real people's emails and phone numbers, customer data. Use `<REDACTED:API_KEY>` style placeholders, or describe the shape of the value if removing it would break understanding.

## Step 4: Save the lesson folder
- **Slug:** short kebab-case from the outcome (`stripe-checkout-flow`, `launch-video-plan`).
- **Folder** `lesson-<slug>/`:
  - `SKILL.md` from `templates/lesson-skill.md`, with every `{placeholder}` replaced. The description is plain text with no `<` or `>` (claude.ai rejects XML-like tags) and under 1024 characters.
  - `lesson.md`, the filled lesson.
  - `artifacts/`: only small, useful files (final prompts, key snippets, a before and after).

Where to write it (first match wins):
1. A location the user named.
2. **Claude Code:** `.claude/skills/lesson-<slug>/` in the project (shared through git), or `~/.claude/skills/` if the user wants it personal.
3. **Codex:** `.agents/skills/lesson-<slug>/`.
4. **Cowork:** a connected folder (`<connected folder>/lessons/lesson-<slug>/`), plus `lesson-<slug>.zip`.
5. **claude.ai chat** or anywhere else: the files as downloads, plus `lesson-<slug>.zip`.

Build the ZIP with the folder at the top (`zip -r lesson-<slug>.zip lesson-<slug>/`). It can be uploaded in claude.ai under Customize → Skills → + → Upload a skill.

## Step 5: Teach it now (the easy retrace)
Right after saving, teach the lesson in the chat. Write for a smart beginner who wasn't there: short sentences, everyday words, one idea per line. Explain every technical word the first time, or leave it out. Use one analogy where it makes a step click. Keep it to about one and a half screens, in this shape:

```
## How the AI did it: <outcome, in plain words>
**Saved:** <path> · reopen any time with /lesson-<slug> or "teach me <slug>"

**In one breath:** <2 sentences: what you wanted, and what the AI made. No jargon.>

**The journey:** <Stage> → <Stage> → <Stage> → <Stage> → <Result>   (4–7 short stages)

**How the AI thought, step by step**
**1. <stage name>**
- Saw: <what it looked at or was given>
- Thought: <the decision, and why: from the record, or marked (inferred)>
- Did: <the action, with the tool or model in plain words>
- Got: <the result>
**2. …**   (4–7 steps, matching the journey)
↺ **Turning point:** <what went wrong or changed, what triggered it, and what the AI did next>   (one line per turning point, placed after the step where it happened)

**Why it worked:** 2–3 principles anyone can reuse, each one line ("Fix the timing before the visuals, because the voice sets the pace").

**Words you met:** 3–6 terms from this work, each with a one-line meaning ("Render: turning the code into a video file").

**What steered it:** the 1–2 things you said that changed the result most, quoted, and why they mattered.

**Next time, cheaper:** <one line: which model and effort for each stage, or what to skip>

**Check yourself:** <one question about a key decision>. Answer it, or say "walkthrough" to go step by step, "rebuild" to try it yourself, or "done".
```

Then wait for the learner. Their reply is handled by Step 6's modes.

**Before you send, check:** the answer starts with "## How the AI did it", the lesson file exists, every step has Saw / Thought / Did / Got, every technical word is explained, and nothing in it tells the user to check, fix or post the original work.

## Step 6: Teach a saved lesson (and follow-ups)
**Find the lesson** (when the user names one, or asks what exists):
1. A path or name the user gave (`stripe-checkout-flow`, `lesson-stripe-checkout-flow`, or a folder).
2. `.claude/skills/lesson-*/` and `.agents/skills/lesson-*/` in the project.
3. `~/.claude/skills/lesson-*/` and `~/.agents/skills/lesson-*/`.
4. A `lessons/` or `examples/lessons/` folder in the project or a connected folder.
5. Lesson skills enabled on the account, or a `lesson-<slug>.zip` or `lesson.md` the user attached.

If no lesson was named, list the ones found as `slug — title (domain, difficulty)` and ask which. If none exist, say that lessons are created by running retrace at the end of a task.

**Teach.** Read `lesson.md` completely and use the teaching protocol in that lesson's own `SKILL.md`. If there is none, use these modes:
- **Short retrace:** the Step 5 shape.
- **Walkthrough:** one step per message. For each: what the AI saw, what it thought and why, what it did (with the real prompt or snippet, kept short), and what it got. Add an analogy if the step is technical. Then one check question, and wait. Pull in the matching decision-log row when a choice was made.
- **Rebuild:** give the *Try it yourself* exercise, review the learner's attempt against the lesson, and give hints before answers.

Always cover *Mistakes and fixes* and the *Efficiency review* by the end. Finish with the check questions and one line on applying the pattern to the learner's own work.

## Rules
- **Teach, don't report.** The output is a lesson for a person, never a project status update or a checklist for the original task.
- **Evidence over storytelling.** Don't invent alternatives that were never considered. Label expert suggestions as "Other options an expert might consider".
- **Recorded versus inferred.** Keep the two visibly apart. Never claim to replay the model's private reasoning.
- **Short turns.** Wait for the learner between phases. Compress for advanced learners; slow down and add an analogy for a lost one.
- **Size.** Keep `lesson.md` under ~400 lines and link to artifacts instead of pasting them.
- **One lesson per coherent outcome.** If the session built three unrelated things, offer three lessons.
