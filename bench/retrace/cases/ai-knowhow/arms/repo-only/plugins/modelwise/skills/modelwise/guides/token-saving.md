# Saving tokens (and money) by task type

Order of levers, from Anthropic's and OpenAI's own cost guidance. **Free wins first, trade-offs last.** Judge cost **per completed task**, not per request: a cheap call that needs three retries isn't cheap.

## Free wins: no quality loss

| Lever | What to do | Typical saving | Vendors |
|---|---|---|---|
| **Prompt caching** | Put stable content first (system prompt, tools, examples, documents) and keep it byte-identical; put the changing request last. Don't put timestamps or the current date at the top. | Cached input bills at ~5-10% of normal. The biggest lever for agents and chats | Anthropic: `cache_control` (or auto caching). OpenAI: automatic, plus a stable `prompt_cache_key` |
| **Batch API** | Send non-urgent jobs (bulk extraction, evals, backfills, image batches) as a batch | 50% off every token | Both |
| **Fresh context** | Start a new chat/session for a new task. Long chats resend the whole history every turn | Large on long sessions | Any app |
| **Send less** | Point to files instead of pasting; paste the first error and 20-50 lines of trace, not the whole log; downscale images (~1280×720); crop screenshots | Often 2-10× on input | Any |
| **Ask for less** | Diffs instead of whole files; exact output shape with one example; `text.verbosity: low` (OpenAI) | Output tokens are 5× the price of input | Any |
| **Structured outputs** | JSON schema instead of "return JSON" text, so there are no retries for malformed output | Removes retry cost | Both |

## Trade-offs: measure before you switch

1. **Lower the effort first, then the model.** Effort scales thinking depth within one model. Current models at lower effort often match older models at high effort. Research and writing curves are nearly flat (low ≈ medium ≈ high); long-horizon coding is a real trade-off.
2. **Escalate on failure.** Run at the recommended effort; re-run only failures one level up (when you have tests or a checker). In Anthropic's runs this kept the pass rate for a little over half the cost.
3. **Right-size the model.** The fast tier (Claude Haiku 5.5, GPT-6 Luna, both $0.10 / $0.50 per M) handles extraction, classification, routing and simple edits. Use the balanced tier (Sonnet 5.5, GPT-6.1 Sol, both $2 / $10) for everyday coding and agents. Use frontier models only where the routing says so.
4. **Plan strong, execute cheap.** Use a strong model for the plan or architecture, then a cheaper model for repetitive per-file edits or bulk work (orchestrator/worker). This only pays when there's real bulk to hand off.
5. **Sub-agents for bulky reading.** Let a cheap worker read 50 files or pages and return a one-paragraph summary, so the main context stays small.
6. **Task budgets** (Claude API, beta) let the model pace itself to a token ceiling. `max_tokens` is only a hard cut-off: it truncates and wastes the attempt.

## By task type

| Task | Biggest savers |
|---|---|
| Coding | Agentic tool reads files itself; ask for diffs; one task per session; escalate effort only on failure |
| Debugging | First error + relevant trace only; let the agent run the repro; start at medium |
| Frontend | Design tokens in a cached system prompt; iterate with screenshots plus "change X" |
| Agents | Caching (stable system prompt + tools); narrow tools with `limit`/`fields`; sub-agents; batch unattended runs |
| Writing | Low/medium effort is enough; outline first for long pieces |
| Extraction | Fast tier + lowest effort + Batch API + cached instructions; several items per request |
| Data analysis | Attach files and let the model run code: only results enter the context |
| Research | Medium effort; parallel cheap sub-questions, one strong synthesis |
| Hard reasoning | High/max only after medium fails; thinking is billed as output |
| Vision | Downscale and crop; Files API for repeated PDFs |
| Images | Draft at low quality on the fast model; final render once; one change per edit |
| Video | Lock script and shot list with a cheap text model first; preview resolution; overlays in editing |
| Audio | Polish the script in text first; smaller transcription model unless audio is hard |

## Sources
- https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://developers.openai.com/api/docs/guides/reasoning
- https://developers.openai.com/api/docs/pricing
