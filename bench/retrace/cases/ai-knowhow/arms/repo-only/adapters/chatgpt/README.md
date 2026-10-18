# Using ai-knowhow in ChatGPT

There are three options. Pick the first one your plan supports.

## 1. Workspace plugin import (Business / Enterprise / Edu admins)
ChatGPT can import a GitHub repo that contains a `.claude-plugin/marketplace.json`. This repo has one.

1. Admin console → **Plugins** → **Add** → **Import marketplace**
2. Enter the repo URL (`https://github.com/YOUR-GITHUB-USERNAME/ai-knowhow`), branch `main`.
3. Enable **modelwise** and **retrace** for your workspace. It syncs daily.

## 2. Upload as skills (Business / Enterprise / Healthcare / Edu)
```bash
python3 tools/install.py zip
```
Then go to **Plugins** → **Skills** → **Create** → **Upload from your computer**, and upload `dist/modelwise.zip`, `dist/retrace.zip` and `dist/teach.zip` one at a time.

## 3. Other plans: a ChatGPT Project
Skill uploads aren't available on every plan. Projects (custom instructions plus files) are available more widely, so check your plan.

1. Create a Project, e.g. "Modelwise".
2. Paste the contents of [`project-instructions.md`](project-instructions.md) into the project's **Instructions**.
3. Upload these files from `plugins/modelwise/skills/modelwise/` to the project:
   - `ROUTING_TABLE.md` (the pre-computed routes, since ChatGPT can't run the router script here)
   - `guides/classify.md`, `guides/prompt-style-anthropic.md`, `guides/prompt-style-openai.md`, `guides/token-saving.md`
   - the `templates/*.md` you care about (all 15 is fine)
4. In the project, type: `modelwise: <your basic prompt>`

For retrace in a Project, paste `plugins/retrace/skills/retrace/SKILL.md` as instructions and upload `templates/lesson.md` and `guides/capture-checklist.md`.

**Recommended model to run it:** GPT-6 Sol (the default on paid plans) at a low Thinking level. GPT-6 Luna works for the budget option.

Custom GPTs are being retired by OpenAI. Use Projects or skills instead.
