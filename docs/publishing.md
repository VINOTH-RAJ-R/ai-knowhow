# Publishing ai-knowhow so everyone can use it

There are **five channels**. Do them in this order. Each one builds on the previous one.

| # | Channel | Who it reaches | Review? | Time |
|---|---|---|---|---|
| 1 | **Your GitHub repo as a marketplace** | Anyone using Claude Code, claude.ai, Cowork, Codex or a ChatGPT workspace, by typing your repo name | None: live as soon as you push | 15 min |
| 2 | **GitHub Release with ZIPs** | People who install by uploading (claude.ai, Cowork, ChatGPT skills) | None | 2 min (automatic on tag) |
| 3 | **Anthropic's official directory** (claude.ai/directory) | Everyone browsing **Customize → Plugins → Discover** in claude.ai and Cowork, plus Claude Code via sync; also mirrored to the community marketplace | Automated scan + human review | Submit: 20 min. Review: not fixed |
| 4 | **OpenAI plugin directory** (ChatGPT + Codex) | Everyone browsing plugins in ChatGPT and Codex | Automated scan + human review; verified developer required | Submit: 30 min. Review: not specified |
| 5 | **Organizations** (optional) | Your company's Team/Enterprise workspace | Your admin | 5 min |

Everything below uses `<owner>` for your GitHub user or organization.

---

## Step 0: Prepare the repo (once)

```bash
cd ai-knowhow
python3 tools/release.py --owner <owner> --version 0.1.0 --check --build
```
This replaces the GitHub-username placeholder in every file with your name, sets the version in all manifests, then runs the directory checks:
- README of 40+ words and a LICENSE per plugin
- no `.DS_Store`, no non-image file over 256 KiB, repo under 50 MiB
- no secrets, valid names, matching versions
- `validate.py` and the router tests

Finally it builds every upload ZIP into `dist/`.

If you have the Claude CLI, also run:
```bash
claude plugin validate . --strict
claude plugin validate plugins/modelwise --strict
claude plugin validate plugins/retrace --strict
```

Then work through [docs/testing.md](testing.md) before you go public.

---

## Step 1: Push to GitHub. Your marketplace is live.

```bash
git add -A
git commit -m "ai-knowhow v0.1.0"
git remote add origin https://github.com/<owner>/ai-knowhow.git
git push -u origin main
```
Make the repository **public**. In repo **Settings → General**, enable **Issues**, because the daily model-watch workflow opens issues there.

**There's no submission step for this channel.** Once `.claude-plugin/marketplace.json` is on GitHub, anyone can install:

| Where | What users type |
|---|---|
| **Claude Code** | `/plugin marketplace add <owner>/ai-knowhow` then `/plugin install modelwise@ai-knowhow` and `/plugin install retrace@ai-knowhow` |
| Claude Code (one step, recent versions) | `/plugin install modelwise --marketplace <owner>/ai-knowhow` |
| **claude.ai / Cowork** | Customize → Plugins → Add → **Add marketplace** → `<owner>/ai-knowhow` |
| **Codex** | `codex plugin marketplace add <owner>/ai-knowhow`, then install from `/plugins` |
| **ChatGPT workspace** (admin) | Admin → Plugins → Add → **Import marketplace** → repo URL (reads `.claude-plugin/marketplace.json` or `.agents/plugins/marketplace.json`) |

Tips to put in your announcement:
- Users without a GitHub SSH key should set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.
- **Auto-update is off by default** for third-party marketplaces. Users turn it on in `/plugin` → Marketplaces → Enable auto-update, or run `claude plugin update modelwise@ai-knowhow`.

---

## Step 2: Tag a release, and the ZIPs are attached automatically

```bash
git tag v0.1.0
git push origin v0.1.0
```
`.github/workflows/release.yml` checks that the tag matches the manifest versions, runs the release checks, and publishes a GitHub Release. Attached ZIPs:
- `*-plugin.zip`: claude.ai/Cowork → Customize → Plugins → Upload plugin
- `modelwise.zip`, `retrace.zip`, `teach.zip`: single skills for claude.ai or ChatGPT skill upload
- `*-openai.zip`: the OpenAI plugin directory (Step 4)

---

## Step 3: Submit to Anthropic's directory (claude.ai, Cowork, Claude Code)

This is the channel with the widest reach. An approved plugin appears in **Discover** for Pro, Max, Team and Enterprise users. It is also mirrored to Anthropic's community marketplace (`anthropics/claude-plugins-community`), which syncs nightly from approved directory plugins. **Pull requests sent directly to that repo are closed automatically.** The directory is the only way in.

**Eligibility**
- A paid Claude plan (Pro, Max, Team or Enterprise). On Team/Enterprise, an Owner submits, or someone with the "Directory" permission.
- Your GitHub account connected on claude.ai, with push access to the repo.

**Submit, once per plugin.** There are two plugin folders, so you make two submissions:
1. Go to **https://claude.ai/directory/manage**, then **Submit new**, then **Plugin bundle**.
2. **Source:** `<owner>/ai-knowhow`. Plugin path `plugins/modelwise` (second submission: `plugins/retrace`). Track branch `main`.
3. **Validate.** It runs the same checks as `tools/release.py`.
4. **Listing details** are read from `plugin.json` and the plugin README. They already include the description, keywords, homepage, documentation, support and privacy URLs, and example prompts.
5. **Data handling:** neither plugin collects data or makes network calls. Point to [PRIVACY.md](../PRIVACY.md).
6. **Compliance:** your contact email plus the four acknowledgements.
7. **Submit for review.** Choose the GitHub push webhook so updates are picked up automatically.

**What reviewers look for** (both plugins are prepared for each):
- Every behavior disclosed: each README has a *What it runs and sends* section.
- No hidden instructions, and nothing pulls instructions from the internet. The skills only read their own bundled files.
- Readable code, no binaries, no secrets.
- At least three example prompts.
- A name that doesn't look official: `modelwise` and `retrace` are fine. Don't rename to anything with "claude", "anthropic" or "official".

**After approval:**
- Press **Publish** in the portal.
- For each update: merge to `main`, bump `version` with `python3 tools/release.py --version X.Y.Z`, then tag. The directory picks it up and re-scans it.
- Review time isn't fixed. Track status in the portal.
- The first organization to submit a repo folder owns the listing, so submit from the account that should own it.

---

## Step 4: Submit to the OpenAI plugin directory (ChatGPT + Codex)

**Eligibility**
- A verified OpenAI developer (individual or organization). Organization owners, or members with **Apps Management Write**, can submit.

**Submit, once per plugin:**
1. Build the ZIPs (Step 0 or the GitHub Release): `dist/modelwise-openai.zip` and `dist/retrace-openai.zip`. Each has the portable `plugin.json` at its root, with the listing fields under `extensions.com.openai.interface`:
   - display name and a short description of 30 characters or less
   - long description, developer name, category
   - default prompts, brand color, logo and composer icon (in `assets/`)
   - website, privacy and terms URLs
2. Go to **https://platform.openai.com/plugins**, then **Upload new or existing plugin**, and upload the ZIP.
3. Run the required skill scan. Then **Submit for review** with the policy attestations.
4. Feedback arrives by email. After approval, press **Publish plugin**.
5. For updates: bump the version, rebuild the ZIP, upload again (it is reviewed again).

**Notes**
- These are **skills-only** plugins (no MCP server), which OpenAI allows. OpenAI notes that skills-only plugins "may face additional eligibility requirements" for the directory, and that an MCP server **can't be added later** to a skills-only plugin.
- OpenAI's guidelines say not to imply OpenAI made or endorses the plugin, and not to put "Plugin" or "MCP" in the name. The descriptions already say "Not affiliated with Anthropic or OpenAI".
- Before submitting, open each ZIP's `plugin.json` and check it against the current fields on the submission page, since OpenAI's listing fields change. The values live in `plugins/<name>/.codex-plugin/plugin.json`.

---

## Step 5 (optional): Publish inside an organization

| Platform | How |
|---|---|
| **Claude Team/Enterprise** | Customize → Plugins → your plugin → **Publish to org**. Or an Owner adds the repo under Organization settings → Plugins & skills (org sync needs a **private/internal** repo, and reads the default branch only). |
| **ChatGPT Business/Enterprise/Edu** | Admin → Plugins → Add → Import marketplace (public or private repo, syncs daily). |

---

## Channels that don't exist (so you don't waste time)
- **agentskills.io** has no registry or listing process. It's the spec only. Use `skills-ref validate` for compliance.
- **Anthropic's `claude-plugins-official`** doesn't take public submissions.
- **Custom GPTs** are being retired by OpenAI. Use plugins or skills instead.

## After launch
- The daily watcher, monthly benchmark and release checks keep it honest: see [maintenance.md](maintenance.md).
- Respond to GitHub issues, because the directory listing links to them as support.
- Announce with the one-line install command for Claude Code, plus the "Discover" listing once it's approved.
