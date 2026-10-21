# Commands used to build and publish ai-knowhow

Run from the repo folder. No secrets appear here. Use your own GitHub login when pushing.

## Check the repo
```bash
python3 tools/validate.py          # registry, skills, manifests, routing table
python3 tools/test_route.py        # router behaviour tests
python3 tools/release.py --check   # directory-style checks
```

## Install for local testing
```bash
python3 tools/install.py claude-code        # copies skills to ~/.claude/skills/
python3 tools/install.py plugin-zip         # dist/*-plugin.zip for claude.ai and Cowork
python3 tools/install.py zip                # single-skill ZIPs for chat and ChatGPT skills
python3 tools/install.py openai-zip         # dist/*-openai.zip for the OpenAI plugin directory
```

## Inside Claude Code (type in the prompt, not the shell)
```
/plugin marketplace add <owner>/ai-knowhow
/plugin install modelwise@ai-knowhow
/plugin install retrace@ai-knowhow
/reload-plugins
```

## Benchmark (optional, spends money)
```bash
pip install anthropic openai
python3 bench/run_api.py --effort-sweep
python3 bench/score.py --run bench/results/<date>-api
```

## Release
```bash
python3 tools/release.py --owner <owner> --version 0.1.1 --check --build
git add -A && git commit -m "ai-knowhow v0.1.1"
git tag v0.1.1 && git push origin main v0.1.1   # the tag starts the release workflow
```

## Remote
```bash
git remote add origin https://github.com/<owner>/ai-knowhow.git
git push -u origin main
```
When asked for a password, use a personal access token with repository access, not your account password.
