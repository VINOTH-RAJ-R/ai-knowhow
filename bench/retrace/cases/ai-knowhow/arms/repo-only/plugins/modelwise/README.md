# modelwise

**Right model, right effort, right prompt.** Type a basic prompt and get back:

1. **The model**: the best Anthropic or OpenAI model for this task, plus a cheaper and a stronger alternative and the best pick from each vendor.
2. **The effort level**: the exact setting (`output_config.effort` for Claude, `reasoning.effort` for OpenAI) and how to set it in Claude Code, claude.ai, ChatGPT or Codex.
3. **A cost estimate**: list price for one typical run, so you can compare.
4. **A structured prompt**: your prompt rewritten with the template for its task type, in the format that model prefers (XML-tagged sections for Claude, Markdown sections for GPT).
5. **Token savers**: the 2-3 levers that matter most for this kind of task.

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
