# Using ai-knowhow in OpenAI Codex (CLI, IDE extension, ChatGPT desktop)

Codex reads Agent Skills (`SKILL.md` folders) from `~/.agents/skills/` (personal) and `.agents/skills/` (per repo).

## Option A: copy the skills (simplest)
```bash
git clone https://github.com/VINOTH-RAJ-R/ai-knowhow.git
cd ai-knowhow
python3 tools/install.py codex            # personal: ~/.agents/skills/
python3 tools/install.py codex --project  # this repo only: ./.agents/skills/ (run from your project folder)
```
Restart Codex, then type `$modelwise build a REST API for a todo app` or open `/skills`.

## Option B: plugin marketplace
This repo ships `.agents/plugins/marketplace.json` (Codex format) and `.claude-plugin/marketplace.json` (which Codex also accepts):
```bash
codex plugin marketplace add VINOTH-RAJ-R/ai-knowhow
```
Then install **modelwise** and **retrace** from `/plugins`.

## Recommended model to run the skills
`gpt-6.1-sol` at effort Light/Medium. The router only reads files and fills templates. Budget option: `gpt-6-luna` (OpenAI suggests High effort for Luna in Codex).

## Where lessons go
`retrace` writes lessons to `.agents/skills/lesson-<slug>/` when it detects Codex, so `$lesson-<slug>` works right away.

## Notes
- The router runs `python3 scripts/route.py`. Codex can run it in its sandbox. If it can't, the skill falls back to `ROUTING_TABLE.md`.
- `${CLAUDE_SKILL_DIR}` in the skill text is a Claude Code variable. In Codex, the skill tells the model to read files relative to the SKILL.md, which works the same way.
