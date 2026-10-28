# Privacy

**modelwise** and **retrace** collect no data and send nothing anywhere.

- **What runs:** `modelwise` runs a local Python script (`scripts/route.py`, standard library only) that reads the JSON files bundled with the skill. It makes no network requests. `retrace` only reads your session and writes lesson files in your project.
- **modelwise-run (Claude Code only):** after you confirm, it starts a helper agent in your own Claude Code session on the routed Claude model. The helper has your session's permissions, runs on your Claude plan, and sends nothing anywhere beyond what Claude Code normally does. It is told not to commit, push, send, publish or delete anything, and Claude Code's permission prompts still apply.
- **What is stored:** lessons created by `retrace` are written where you choose (by default `.claude/skills/lesson-<slug>/` in your project). They never leave your machine or session unless you share them. `retrace` is told to redact secrets and personal data before writing.
- **No telemetry, accounts, API keys or third-party services** are used by the skills.
- The repository's own maintenance tools (`tools/watch_models.py`, `bench/run_api.py`) are **not part of the plugins**. They are run only by maintainers, in GitHub Actions or by hand. They fetch public vendor documentation pages and, for the optional benchmark, call vendor APIs with the maintainer's own keys.

The AI assistant you run the skills in (Claude, ChatGPT, Codex) processes your prompts under that provider's own privacy policy.

Questions: open an issue in this repository.
