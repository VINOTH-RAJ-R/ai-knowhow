# Using ai-knowhow in claude.ai (web, desktop, mobile)

## Option A: add the marketplace (plugins)
**Customize** → **Plugins** → **Add** → **Add marketplace** → enter `YOUR-GITHUB-USERNAME/ai-knowhow` → install **modelwise** and **retrace**.

## Option B: upload the skills as ZIPs
1. Turn on code execution: **Settings** → **Capabilities** → *Code execution and file creation*. Team/Enterprise admins: *Org settings* → *Plugins & skills*.
2. Build the ZIPs:
   ```bash
   python3 tools/install.py zip
   ```
3. **Customize** → **Skills** (claude.ai/customize/skills) → **+** → **Create skill** → **Upload a skill** → choose `dist/modelwise.zip`. Repeat for `retrace.zip` and `teach.zip`. Toggle each one on.

Enabled skills sync to Claude Code when you sign in there with the same account.

## Use it
- "Which model should I use for: build a Shopify app that syncs inventory with Google Sheets?"
- "/modelwise write a launch email for our new feature"
- After finishing something: "retrace this, make a lesson"

**Recommended model to run the skills:** Claude Sonnet 5.5. Turn extended thinking off or keep it at the lowest level. Haiku 5.5 is the budget option.
