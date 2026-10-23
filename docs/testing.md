# Testing ai-knowhow end to end

Work top to bottom. Every stage has **pass criteria**, so you know when to move on. Stages 1-3 run before anything is public. Stage 6 runs after you push. Expect about 1-2 hours for everything, or about 20 minutes for stages 1-3.

Paths assume you are in the repo folder:
```bash
cd "/Users/vc/Documents/Shared AI Knowledge Layer/ai-knowhow"
```

---

## Stage 1: Automated checks (2 minutes)

```bash
python3 tools/validate.py
python3 tools/test_route.py
python3 tools/release.py --check
```
**Pass:**
- `0 errors` from validate.py
- `OK` from the router tests
- release.py only complains about the GitHub-username placeholder (expected until you run `--owner`)

Optional, if the Claude CLI is installed:
```bash
claude plugin validate . --strict
```

---

## Stage 2: Claude Code, installed the way users will install it (local marketplace)

Install from the local folder exactly as you would from GitHub. Remove any old manual copies first, so you test the plugin and not a stale copy:
```bash
rm -rf ~/.claude/skills/modelwise ~/.claude/skills/retrace ~/.claude/skills/teach  # teach is now part of retrace
```
Then, inside Claude Code:
```
/plugin marketplace add /Users/vc/Documents/Shared AI Knowledge Layer/ai-knowhow
/plugin install modelwise@ai-knowhow
/plugin install retrace@ai-knowhow
/reload-plugins
```
Use a **cheap model** for running the skill, like real users: `/model haiku`.

### 2a. modelwise scenarios
| # | Type this | Pass if the answer… |
|---|---|---|
| 1 | `/modelwise write a python function is_valid_ipv4(s)` | recommends **Claude Haiku 5.5 @ low**, shows a **Cost across models** table with both Claude and OpenAI rows, gives a structured coding prompt, 2-3 token tips, and "why this works" |
| 2 | `/modelwise landing page for my bakery` | treats it as a vague creative prompt: **"Best now: send your prompt as-is to <model>"**, then an upgrade prompt plus a "To improve the result, tell me" list; no `[[FILL]]` inside the prompt |
| 3 | `/modelwise classify 50,000 support tickets into billing, bug, feature, other - cheapest way` | picks a **fast-tier** model, shows **totals for 50,000 runs and the Batch price**, and suggests Batch plus structured outputs |
| 4 | `/modelwise migrate our monorepo from webpack to vite and fix whatever breaks, autonomously` | routes to an agent task (`agent.longrun`) with a **flagship model at high effort or above**; prompt has outcome, spec, boundaries, verification |
| 5 | `/modelwise 15 second instagram reel ad for my running shoes` | says plainly there's **no video generator** in the registry (the Sora API shut down), gives Phase 1 (text model writes the prompt) and Phase 2, and still writes a full shot list |
| 6 | `/modelwise logo for my coffee brand` | recommends a **GPT Image** model (Claude doesn't generate images), with an image prompt in scene → subject → details → constraints order |
| 7 | `/modelwise I only use ChatGPT - write a launch email` | main pick is **OpenAI** (GPT-6 Luna or 6.1 Sol); the cost table still lists every model |

Also check: **no model, price or effort level that isn't in the registry** appears in any answer. Spot-check one against `plugins/modelwise/skills/modelwise/registry/models/`.

### 2b. retrace scenarios
1. In a scratch project, ask Claude for something small, e.g. "write a CLI that converts CSV to JSON with tests". Let it finish.
2. Type `/retrace` (or "make a lesson from what we just did").
   **Pass:**
   - creates `.claude/skills/lesson-<slug>/` with `SKILL.md`, `lesson.md` and maybe `artifacts/`
   - `lesson.md` has every section: goal, steps, decision log, prompts, mistakes (or "none recorded"), efficiency review, pattern, quiz, exercise
   - no secrets appear in it
   - rationale it inferred is marked *(inferred)*
   - right after saving, it teaches a **short retrace** in the chat: the map, 3–6 moves (looked at → decided → because → result) with turning points marked ↺, what steered it, the cheaper path, and one check question
3. Reply "walkthrough". **Pass:** it teaches one phase at a time and waits for you between phases.
4. Run `/reload-plugins`, then `/lesson-<slug>`. **Pass:** it opens with the short retrace and offers walkthrough or rebuild.
5. Ask "which lessons do we have?". **Pass:** retrace lists the lesson (and `examples/lessons/` if you open the repo itself).

---

## Stage 3: claude.ai chat and Cowork (uses your claude.ai account)

```bash
python3 tools/install.py plugin-zip
```
1. Make sure code execution is on: Settings → Capabilities → *Code execution and file creation*.
2. In claude.ai, go to **Customize → Plugins → Add → Upload plugin** and upload `dist/modelwise-plugin.zip`, then `dist/retrace-plugin.zip`.
3. **Chat:** start a new chat on **Haiku 5.5**. Repeat scenarios 1, 2, 3 and 5 from 2a.
   **Pass:**
   - same routes as in Claude Code
   - the skill finds its own folder (no `${CLAUDE_SKILL_DIR}` errors)
   - the cost table is present
4. **Cowork:** open the Cowork tab and connect a scratch folder. Run scenario 2, then ask Cowork to build something small and type "retrace this, make a lesson".
   **Pass:** the lesson is saved in the connected folder, plus a `lesson-<slug>.zip`.
5. Upload that `lesson-<slug>.zip` under Customize → Skills. Then in a new chat: "teach me how we built <x>". **Pass:** the lesson tutor starts.

Remove the uploaded test plugins afterwards if you will add the GitHub marketplace in Stage 6.

---

## Stage 4: Codex (if you use it)

```bash
python3 tools/install.py codex
```
Restart Codex, then type `$modelwise write a python function is_valid_ipv4(s)`.

**Pass:**
- main pick is OpenAI (**GPT-6 Luna**)
- the cost table includes Claude rows
- the effort is given in Codex terms (Light/Medium/…)

---

## Stage 5: ChatGPT

Follow [adapters/chatgpt/README.md](../adapters/chatgpt/README.md).
- **Business/Enterprise/Edu:** upload the skill ZIPs.
- **Other plans:** create a Project, paste `adapters/chatgpt/project-instructions.md` as its instructions, and upload `ROUTING_TABLE.md`, `guides/*.md` and `templates/*.md`.

Send: `modelwise: classify 50,000 support tickets - cheapest way`

**Pass:**
- recommends **GPT-6 Luna**
- shows a cost table with a 50,000-run total and the Batch price
- gives ChatGPT model-picker advice taken from the routing table header

---

## Stage 6: After pushing to GitHub (the real public path)

Run the Step 0 and Step 1 commands in [publishing.md](publishing.md) first.

| Check | How | Pass |
|---|---|---|
| CI is green | GitHub → Actions → **validate** on your push | All steps pass, including release checks |
| Install from GitHub works | New machine or after `/plugin marketplace remove ai-knowhow`: `/plugin marketplace add <owner>/ai-knowhow`, then install both | Both plugins install; scenario 1 works |
| claude.ai marketplace | Customize → Plugins → Add marketplace → `<owner>/ai-knowhow` | Both plugins listed and installable |
| Update path | `python3 tools/release.py --version 0.1.1 --check`, commit, push, `git tag v0.1.1 && git push origin v0.1.1`, then `claude plugin update modelwise@ai-knowhow` | Release created with 7 ZIPs; the update installs 0.1.1 |
| Watcher | Actions → **watch-models** → Run workflow | Finishes; opens an issue only if something needs attention |
| Benchmark workflow | Actions → **benchmark** → Run workflow (skips cleanly with no API keys) | "No API keys configured; skipping", or results committed if keys are set |

---

## Stage 7 (optional): Re-run the benchmark

- **Free, from Claude Code:** see [bench/README.md](../bench/README.md). It re-uses the same tasks, checkers and blind-judge setup.
- **Over the APIs:** this costs a few dollars and tests effort levels and OpenAI models properly.
  ```bash
  pip install anthropic openai
  python3 bench/run_api.py --effort-sweep
  python3 bench/score.py --run bench/results/$(date +%F)-api
  ```

## Release-ready checklist
- [ ] Stage 1 passes
- [ ] All 7 modelwise scenarios and all 4 retrace steps pass in Claude Code
- [ ] Chat and Cowork pass (Stage 3)
- [ ] `tools/release.py --owner <owner> --version 0.1.0 --check --build` passes
- [ ] Stage 6 passes after push. Then submit to the directories (publishing.md, Steps 3-4).
