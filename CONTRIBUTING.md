# Contributing

Thanks for helping keep this accurate. The registry is only as useful as it is current.

## Add or update a model
1. Read the vendor's **official** model page, pricing page and prompting guide. Blog posts and social media are not sources.
2. Create or edit `plugins/modelwise/skills/modelwise/registry/models/<provider>/<id>.json`. The fields are defined in `registry/model.schema.json`. Copy a similar card as a starting point.
3. Rules:
   - `id` is the exact API model ID, and the file is named `<id>.json`.
   - Every price, limit and effort level must be traceable to a URL in `sources`.
   - `verified` is the date you checked those sources.
   - `fit` (0-5 per task) is a judgment. Justify changes in the PR description with vendor docs or public evaluations. 5 means "among the best available for this task".
   - When a model is superseded, set the old card's `status` to `previous` (or `legacy`), and set `retires` once a date is announced.
4. Run:
   ```bash
   python3 tools/validate.py --fix   # validates everything and regenerates ROUTING_TABLE.md and MODELS.md
   python3 tools/test_route.py
   ```
5. Open a PR. In the description, say what changed and link the sources.

## Add a task type or template
- Add the task to `registry/tasks.json`. Effort must not decrease as complexity rises.
- Add `templates/<name>.md` with these sections: slots, universal skeleton, Claude rendering, OpenAI rendering, example, token savers.
- Add `fit` scores for the new task to the relevant model cards.

## Add a vendor (Phase 2)
Add the provider to the `provider` enum in `model.schema.json`, add a `vendor_mappings` entry in `effort-scale.json`, a `guides/prompt-style-<vendor>.md`, cards under `registry/models/<vendor>/`, and a source in `tools/watch_models.py`.

## Improve the skills
`SKILL.md` files must stay within the [Agent Skills standard](https://agentskills.io/specification). Allowed frontmatter fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. claude.ai rejects any other field, and `validate.py` checks this.

## Share a lesson
Good lessons from `retrace` are welcome in `examples/lessons/`. Redact secrets and personal data first.
