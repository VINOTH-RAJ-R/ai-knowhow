1. Plugin installers copy only the plugin's own folder, so a skill reading files from a top-level `registry/` would break after install. Keeping the registry inside the skill folder makes the skill self-contained, which also lets it work as a ZIP upload (architecture.md and the lesson both say this).

2. Python's standard library reads JSON everywhere, so the router needs no install step. YAML would require PyYAML, and TOML's `tomllib` needs Python 3.11+. The lesson marks the "zero install steps" priority as inferred.

3. "Balanced" picks the cheapest model that clears the task's quality bar with one point of headroom (min_fit + 1, capped at 5). It replaced a log-cost penalty on fit, which recommended Haiku for moderate feature builds, and Haiku is too weak for that. Headroom gives explainable picks, such as Sonnet for moderate and Opus for complex.

4. claude.ai uploads reject frontmatter keys outside the Agent Skills standard (name, description, license, compatibility, metadata, allowed-tools), and portability mattered more than pinning. The defaults live in `metadata` and in the skill text instead, and `validate.py` checks the allowed fields.

5. The router finds no direct route because there is no video generator in the registry: the Sora 2 API shut down on 2026-09-24 and Anthropic doesn't generate video. Modelwise still writes the full video prompt from the video template, and it presents a "Phase 1: write the prompt" route using the fallback task's picks. It also adds a "Phase 2: generate" note saying no generator is listed yet.

6. One audio task mixed transcription with voice agents and produced nonsense picks in the routing table review. It became audio.transcribe, audio.speak and audio.agent.

7. A weekly GitHub Action runs `tools/watch_models.py`, which scans Anthropic's and OpenAI's model pages for IDs the registry doesn't know and opens an issue. A human then updates the card from official docs and runs `tools/validate.py --fix`. CI runs `validate.py` (schema, skills, manifests, routing-table freshness, 90-day stale `verified` warnings) and `test_route.py`.

8. The agent assumed GPT-5.x was OpenAI's current lineup, but GPT-6 is current, because its training data was stale. A research agent was told not to trust memory, and its "unverified items" list surfaced GPT-6 and the Sora shutdown.

9. Following the lesson's phase-2 steps and CONTRIBUTING.md:
   - Add `google` to the provider enum in `model.schema.json`.
   - Add a `vendor_mappings` entry in `effort-scale.json`.
   - Add `guides/prompt-style-google.md`.
   - Add a card under `registry/models/google/` with `video_out` and `fit` for the video task, sourced from official docs.
   - Add a source to `tools/watch_models.py`.
   - Run `python3 tools/validate.py --fix` and `python3 tools/test_route.py`.
   The video fallback then stops applying automatically.

10. A script gives the same answer for the same inputs, it can be tested, and it keeps recommendations independent of whichever model is running the skill (so a cheap model works). `ROUTING_TABLE.md` is the same logic pre-computed, for tools like ChatGPT Projects that can't run scripts. The model only does the classification, which needs judgment.
