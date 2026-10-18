# Using ai-knowhow in claude.ai chat and Claude Cowork

Chat and Cowork both load the skills and plugins **enabled on your claude.ai account**. Install once and they work in both, and they sync to Claude Code when you sign in with the same account.

**Cowork doesn't read `~/.claude/skills/`.** If you installed with `tools/install.py claude-code`, also add the skills here.

## Before you start
Turn on code execution, because skills need it:
- **Free/Pro/Max:** Settings → Capabilities → *Code execution and file creation*.
- **Team/Enterprise owners:** Organization settings → Plugins & skills → turn on *Code execution* and *Skills*.

## Option A: upload the plugins (best for local testing, no GitHub needed)
```bash
python3 tools/install.py plugin-zip
```
Then go to **Customize → Plugins → Add → Upload plugin** and upload `dist/modelwise-plugin.zip`, then `dist/retrace-plugin.zip`.

## Option B: upload the skills one by one
```bash
python3 tools/install.py zip
```
Then go to **Customize → Skills → + → Create skill → Upload a skill** for `dist/modelwise.zip`, `dist/retrace.zip` and `dist/teach.zip`. Turn each one on.

## Option C: add the GitHub marketplace (after you push)
**Customize → Plugins → Add → Add marketplace** → `VINOTH-RAJ-R/ai-knowhow`.

## Use it
- Type `/` and pick **modelwise**, or just ask: "Which model and effort should I use for: build a Shopify app that syncs inventory with Google Sheets?"
- After finishing something: "retrace this, make a lesson".
  - In chat you get the lesson files plus `lesson-<slug>.zip` to upload as a skill.
  - In Cowork the lesson is saved into a folder you've connected.

## How it behaves differently from Claude Code
| | Claude Code | Cowork | claude.ai chat |
|---|---|---|---|
| `${CLAUDE_SKILL_DIR}` filled in | Yes | Yes | No. The skill uses relative paths and finds its folder |
| Runs `scripts/route.py` | Yes | Yes (cloud sandbox) | Yes (code execution sandbox) |
| Where retrace saves lessons | `.claude/skills/lesson-<slug>/` | A connected folder, plus a ZIP | Downloads, plus a ZIP |
| Setting effort for the recommended model | `/effort` | Model picker | Model picker, plus extended thinking on/off |

**Recommended model to run the skills:** Claude Haiku 5.5. Our benchmark found it gave the same routes and format as Sonnet at about a twentieth of the cost. Use Sonnet 5.5 for complex rewrites.
