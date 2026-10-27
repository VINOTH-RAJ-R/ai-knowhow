# modelwise

**Right model, right effort, right prompt.** Type a basic prompt and get back:

1. **The model**: the best Anthropic or OpenAI model for this task, plus a cheaper and a stronger alternative and the best pick from each vendor.
2. **The effort level**: the exact setting (`output_config.effort` for Claude, `reasoning.effort` for OpenAI) and how to set it in Claude Code, claude.ai, ChatGPT or Codex.
3. **A cost estimate**: list price for one typical run, so you can compare.
4. **A structured prompt**: your prompt rewritten with the template for its task type, in the format that model prefers (XML-tagged sections for Claude, Markdown sections for GPT).
5. **Token savers**: the 2-3 levers that matter most for this kind of task.

## Route and run (Claude Code)
`/modelwise-run <your prompt>` (plugin: `/modelwise:modelwise-run`) goes one step further: it understands the prompt, picks the Claude model and effort, structures the prompt for that model, and shows you the route, the cost compared with other models, and the exact prompt. When you say **Run it**, a helper agent on that model (`modelwise-haiku`, `-sonnet`, `-opus` or `-fable`, in `agents/`) does the task and the result comes back to your chat. It always asks before running. Image, video and audio tasks can't run on Claude, so it gives the modelwise prompt for them instead. Outside Claude Code it falls back to the modelwise answer. Tip: run your own session on Sonnet or Haiku so the routing step itself stays cheap.

## How it decides
```
your prompt
  → classify   (guides/classify.md)       task · complexity · priority · provider
  → route      (scripts/route.py)          filter by capability and status → quality bar → rank
  → template   (templates/<task>.md)       fill slots, render for the chosen vendor
  → answer     model · effort · cost · prompt · token tips · why it works
```

**Ranking rules** (`scripts/route.py`):
- **balanced** (default): the *cheapest* model whose fit clears the bar for this complexity, with one point of headroom.
- **cost**: the cheapest model that clears the bar.
- **quality**: the highest fit.
- **speed**: the fastest model with headroom.

Quality bar by complexity: simple ≥ 2, moderate ≥ 3, complex ≥ 4, frontier = 5 (fit is 0-5 per task, on each model card).

**Effort**: each task maps complexity onto a normalized scale E0-E6 (`registry/effort-scale.json`). Each model card then maps that onto its real levels, rounding to the nearest supported value.

## Files
| Path | What |
|---|---|
| `skills/modelwise/SKILL.md` | The skill instructions |
| `skills/modelwise-run/SKILL.md` | Route-and-run skill (Claude Code) |
| `agents/` | The four runner agents, one per Claude model |
| `skills/modelwise/registry/models/` | 60 model cards (Anthropic, OpenAI) |
| `skills/modelwise/registry/tasks.json` | 21 task types |
| `skills/modelwise/registry/effort-scale.json` | E0-E6 and vendor/app mappings |
| `skills/modelwise/registry/model.schema.json` | Card schema |
| `skills/modelwise/templates/` | 15 prompt templates |
| `skills/modelwise/guides/` | Classification, vendor prompt styles, token saving |
| `skills/modelwise/scripts/route.py` | The router (Python 3.8+, standard library only) |
| `skills/modelwise/ROUTING_TABLE.md` | Generated table for tools that can't run scripts |

## Router CLI
```bash
cd skills/modelwise
python3 scripts/route.py --list-tasks
python3 scripts/route.py --task code.debug --complexity complex
python3 scripts/route.py --task data.extract --priority cost --provider openai --json
python3 scripts/route.py --model claude-opus-5-5
```

## Example prompts
1. `/modelwise landing page for my bakery`: frontend task. Returns the model and effort, a cost table across all current models, and a design prompt (or "send it as-is" plus an upgrade if your prompt is vague).
2. `/modelwise classify 50,000 support tickets into billing, bug, feature request, other - as cheap as possible`: extraction at volume. Returns the cheapest capable model, total and Batch cost for 50,000 runs, and a structured-output prompt.
3. `/modelwise why does my Next.js build fail after upgrading to v16`: debugging. Returns a balanced or flagship model at medium effort and a root-cause-first debugging prompt.
4. `/modelwise 15 second instagram reel ad for my running shoes`: video. Explains that no video generator is in the registry yet, routes the prompt-writing to a text model, and writes a full shot list.
5. `/modelwise-run write a regex for Indian PAN numbers` (Claude Code): routes to Claude Haiku at low effort, shows the cost against Sonnet and Opus and the structured prompt, and after you choose **Run it**, returns the regex with valid and invalid examples.

## What it runs and sends
- Runs one local script, `skills/modelwise/scripts/route.py` (Python 3.8+, standard library only), which reads the JSON files in `skills/modelwise/registry/`.
- **No network access, no data collection, no API keys.** Nothing leaves your session except what your AI assistant normally processes. See [PRIVACY.md](../../PRIVACY.md).
- **`/modelwise-run` (Claude Code only) hands work to a helper agent.** After you confirm, it starts one of the bundled runner agents (`agents/modelwise-haiku.md`, `-sonnet`, `-opus`, `-fable`) on that Claude model with the prompt it showed you. The helper uses your Claude Code session's permissions, so it can read and edit files in your project. It's told not to commit, push, send, publish or delete anything, and Claude Code's own permission prompts still apply. It runs on your Claude plan or API key, like any other Claude Code task. The plain `/modelwise` skill never runs anything beyond the router script.
- If scripts can't run (for example in a ChatGPT Project), it reads the pre-computed `ROUTING_TABLE.md` instead.

## Support
Open an issue on the repository's GitHub Issues page. Model data is maintained under [CONTRIBUTING.md](../../CONTRIBUTING.md); every card links its official source.

## License
MIT. See [LICENSE](LICENSE). Not affiliated with Anthropic or OpenAI.
