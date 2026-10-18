# Privacy

**modelwise** and **retrace** collect no data and send nothing anywhere.

- **What runs:** `modelwise` runs a local Python script (`scripts/route.py`, standard library only) that reads the JSON files bundled with the skill. It makes no network requests. `retrace` and `teach` only read and write files in your project or session.
- **What is stored:** lessons created by `retrace` are written where you choose (by default `.claude/skills/lesson-<slug>/` in your project). They never leave your machine or session unless you share them. `retrace` is told to redact secrets and personal data before writing.
- **No telemetry, accounts, API keys or third-party services** are used by the skills.
- The repository's own maintenance tools (`tools/watch_models.py`, `bench/run_api.py`) are **not part of the plugins**. They are run only by maintainers, in GitHub Actions or by hand. They fetch public vendor documentation pages and, for the optional benchmark, call vendor APIs with the maintainer's own keys.

The AI assistant you run the skills in (Claude, ChatGPT, Codex) processes your prompts under that provider's own privacy policy.

Questions: open an issue in this repository.
