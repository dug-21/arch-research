# SHD-002 — W1: Harness Inventory

**Capability under test (C2):** "An agentic harness drives research+coding tasks to completion." `done_when`: harness finishes a defined multi-step research+code task with NO manual steps, AND can drive a **self-hosted/local** model backend (not a hosted API as the only option).

**Scope of this workstream (W1):** Enumerate candidate agentic coding/research harnesses; profile each. **This is a directional inventory** — fields below are **doc-claims / community-reported signals**, not demonstrated evidence. None of these were installed or run. Star counts and dates are as reported by sources retrieved 2026-06-23 and should be treated as approximate.

---

## Inventory table

| Harness | One-line purpose | Interface | OSS / Proprietary | Autonomous multi-step? | Local/self-hosted backend? | Maturity / activity signal (reported) |
|---|---|---|---|---|---|---|
| **Claude Code** | Anthropic's agentic coding tool in the terminal; plans, edits, runs commands, handles git | CLI + headless (`-p`/`--print`) + Agent SDK (Py/TS) + IDE integrations | Proprietary (Anthropic); Agent SDK is a library | Yes — agent loop (observe->plan->act->verify), headless for automation/CI | **Weak/indirect.** Designed around Anthropic API. Self-hosting requires routing to Bedrock/Vertex or a proxy; no first-class Ollama/vLLM path documented. **Flag: local-backend claim unverified.** | Anthropic-backed; very active; large repo |
| **aider** | AI pair programming in your terminal; edits files in a git repo, atomic commits | CLI / TUI | OSS (Apache-2.0) | Partial->Yes. Strong multi-file edits, architect mode; more pair-programming loop than fully unattended autonomy | **Yes.** Any OpenAI-compatible endpoint; explicit Ollama docs. No proprietary backend. | ~40-46k stars (reported); very active; Aider-AI org |
| **opencode** | Open-source AI coding agent built for the terminal; model-agnostic | CLI / TUI (also IDE/desktop) | OSS (MIT) | Yes — autonomously navigates files, runs tests/builds/linters/git; Plan mode | **Yes.** 75+ providers incl. local via Ollama (`LOCAL_ENDPOINT`/OpenAI-compatible). | Very high stars (reported 100k+); Anomaly org (SST team: Dax Raad et al.); very active. **Note: naming collision — see out-of-scope notes** |
| **OpenHands** (formerly OpenDevin) | Open platform for autonomous SW-dev agents; plans, writes, runs across codebase | Headless/CLI + Web GUI + SDK; Docker sandbox | OSS (MIT core) | **Yes** — built for end-to-end autonomous task completion | **Yes.** Dozens of backends incl. Ollama and **vLLM**; local Docker execution. | ~70k stars (reported); All Hands AI; v1.x (2026); very active |
| **Cline** | Autonomous coding agent (SDK / IDE extension / CLI assistant) | IDE extension (VS Code + others) + SDK + preview CLI | OSS | Yes — plans multi-step changes, runs commands, edits across repo (with per-step approval by default) | **Yes.** Provider-agnostic incl. Ollama and LM Studio. | ~61-63k stars (reported); very active; v3.8x (2026) |
| **Goose** (Block) | On-machine extensible AI agent; build projects, run/debug code, orchestrate workflows | CLI (+ desktop) | OSS (Apache-2.0) | Yes — autonomous task automation; MCP extensions | **Yes.** 15+ providers incl. Ollama; runs entirely on-machine (air-gap capable). | ~27k stars (reported); Block; very active. **Note: repo org appears as `block/goose` and a mirror `aaif-goose/goose` in sources — confirm canonical repo** |
| **Continue** | IDE assistant with chat/autocomplete/edit + Agent mode | IDE extension (VS Code, JetBrains) + CLI | OSS — **but see status** | Partial. Agent mode exists; historically more assistant than fully unattended | **Yes** (Ollama/local), but tool-calling reliability depends on local model | **Acquired by Cursor (June 2026); OSS repo now read-only, v2.0.0 final.** ~34k stars. **Flag: maintenance frozen.** |
| **Roo Code** | "A dev team of AI agents in your editor"; role modes (Architect/Code/Debug/Test) | IDE extension (VS Code + forks) + optional cloud agents | OSS | Yes — multi-mode structured autonomous workflows | **Yes** (BYO keys / local inference via LiteLLM etc.) | ~24k stars. **One source claims the repo was archived May 2026 — CONFLICTS with active-fork signals. Flag: status unverified.** |
| **Cursor** | AI code editor; Agent mode, Composer, background agents; now also CLI | **IDE (primary)** + headless CLI (`cursor agent -p`) | Proprietary | Yes (in-IDE and via CLI/CI) | **No (effectively).** Tied to Cursor subscription/models; not a self-hosted-backend harness. | Well-funded; very active. **Flag: editor-first; CLI headless exists but local-backend requirement not met -> likely out-of-scope for C2's self-hosted clause.** |
| **SWE-agent** | Takes a GitHub issue and autonomously fixes it; research-grade ACI | CLI / headless (batch) | OSS | **Yes** — purpose-built autonomous issue->patch loop | **Yes.** Any LLM via LiteLLM incl. local; mini-swe-agent supports local/docker/podman. | Princeton/Stanford; NeurIPS 2024; active. mini-swe-agent (~100 LOC, >74% SWE-bench verified reported) |
| **gptme** | Personal terminal agent: shell, code exec, file ops, web, vision; build autonomous agents | CLI / headless | OSS | Yes — autonomous run loops; agent-template for persistent agents | **Yes.** Local models via llama.cpp (no key); provider-agnostic, local-first. | ~4.3k stars (reported); active (gptme org); smaller community |
| **Plandex** | Plan-first AI coding agent for large tasks/codebases; 2M-token context | CLI / TUI; self-hostable server (Docker) | OSS | Yes — full autonomy option (load files, plan, implement, exec, auto-debug) | **Yes.** Multi-provider incl. open-source/local; self-host server. | ~15.5k stars. **Flag: "winding down as of 2025-10-03, not accepting new users" — declining.** |
| **Codex CLI** (OpenAI) | OpenAI's lightweight terminal coding agent (Rust) | CLI / headless | OSS (Apache-2.0) — *client*; models are OpenAI's | Yes — read/change/run code; CI/enterprise features | **Partial/Yes.** `--oss` runs a local Ollama model (gpt-oss); OpenAI-compatible endpoint configurable. **Caveat: shift to OpenAI Responses API deprecated Chat Completions — may complicate local-endpoint use. Flag: verify local path still works.** | ~90k stars (reported); OpenAI; very active |
| **Devika** | First OSS "agentic software engineer"; Devin alternative; plan->deploy | Web app + agent backend | OSS | Yes (by design) | **Yes** (Ollama/local claimed) | **Flag: maturity/activity weak — long-stalled, "under testing/select few"; could not confirm active maintenance or non-archived status. Treat as low-confidence / likely dormant.** |
| **Kilo Code** | All-in-one agentic engineering platform (fork lineage w/ Cline/Roo) | IDE extension (VS Code, JetBrains) + CLI + Cloud | OSS | Yes — multi-model agent harness, MCP marketplace | **Yes.** Ollama + LM Studio; explicit local-models docs; BYOK. | "One of fastest-growing" (reported); active; Kilo-Org. Surfaced as a strong additional candidate. |
| **Gemini CLI** (Google) | Google's open-source terminal AI agent | CLI / headless | OSS (client) | Yes | **No (effectively).** Gemini-only; local support limited (LiteRT-LM); community fork `open-gemini-cli` adds llama.cpp/vLLM/MLX. | ~104k stars (reported). **Flag: being RETIRED ~June 18, 2026 for a closed-source successor -> out-of-scope (sunset + no native local).** |

---

## Notes & verification flags

- **C2's load-bearing clause is the self-hosted/local backend.** On that axis the strongest fits are **OpenHands, aider, opencode, Cline, Goose, SWE-agent, gptme, Kilo Code, Plandex** — all expose Ollama and/or OpenAI-compatible/vLLM endpoints as first-class. These should be the front-runners for later proof work.
- **Claude Code**: agentically capable and headless-ready, but its self-hosted-backend story is the weakest of the OSS-adjacent set (designed around the Anthropic API; Bedrock/Vertex are still hosted; no documented native Ollama/vLLM path). **Doc-claim only; not demonstrated.** If C2 strictly requires a *local* backend, Claude Code may satisfy the "harness" half but not the "self-hosted backend" half on its own.
- **Autonomy spectrum (doc-claims):** purpose-built-for-autonomy -> OpenHands, SWE-agent, Devika, Plandex, Codex CLI, opencode. Pair-programming/assistant-leaning (but capable of multi-step) -> aider, Continue, Cline/Roo/Kilo (IDE, per-step approval default).
- **Star counts:** several reported numbers look inflated by aggregator pages (e.g. opencode "100k+/160k", "7.5M devs"). Treat all stars as **approximate, unverified** — confirm against the live GitHub repo before citing in a decision.
- **Repo-identity ambiguities to confirm before any install:**
  - *opencode* — multiple orgs in the wild (`anomalyco/opencode`, `opencode-ai/opencode`, `sst`-associated). Confirm the canonical/maintained repo.
  - *Goose* — `block/goose` vs `aaif-goose/goose` mirror.
  - *SWE-agent* — `SWE-agent/SWE-agent` vs legacy `princeton-nlp/SWE-agent`.

## Out-of-scope / down-weighted candidates

- **Cursor** — editor-first; headless CLI exists but it's proprietary and tied to Cursor's models/subscription with **no self-hosted backend** -> fails C2's local-backend clause.
- **Gemini CLI** — **being retired (~2026-06-18)** for a closed-source successor; native local support is limited (community fork only). Out on both sunset and local-backend grounds.
- **Continue** — **acquired by Cursor; OSS repo read-only / final v2.0.0.** Local path technically intact but **unmaintained**; down-weight for a forward-looking proof.
- **Plandex** — **winding down (2025-10-03), not accepting new users.** Down-weight.
- **Devika** — **likely dormant / never reached production maturity** ("under testing", select access). Low-confidence; include only as historical reference.
- **Roo Code** — keep, but **archive status (claimed May 2026) is unverified and conflicts with other signals** — confirm before relying on it.

## Could-not-verify (explicit)

- Exact current GitHub star counts and last-release dates for every entry (sources are secondary/aggregator; not the live repos).
- Whether Claude Code, Cursor, or Codex CLI can drive a **fully local** model end-to-end in headless mode **without a hosted fallback** — all three are doc-claim "partial/no" and need hands-on confirmation.
- Roo Code archived-or-not; Devika maintenance status; canonical repos for opencode/Goose/SWE-agent.

## Citations (URLs)

- Claude Code: https://github.com/anthropics/claude-code | https://code.claude.com/docs/en/agent-sdk/overview | https://www.mindstudio.ai/blog/claude-code-headless-mode-autonomous-agents
- aider: https://github.com/aider-ai/aider | https://aider.chat/docs/llms/ollama.html
- opencode: https://opencode.ai/ | https://github.com/anomalyco/opencode/ | https://www.infoq.com/news/2026/02/opencode-coding-agent/
- OpenHands: https://github.com/OpenHands/OpenHands | https://www.openhands.dev/ | https://github.com/OpenHands/software-agent-sdk
- Cline: https://github.com/cline/cline | https://cline.bot/
- Goose: https://github.com/block/goose/releases | https://goose-docs.ai/ | https://github.com/aaif-goose/goose/blob/main/documentation/docs/getting-started/providers.md
- Continue: https://github.com/continuedev/continue | https://docs.continue.dev/ide-extensions/agent/model-setup
- Roo Code: https://github.com/RooCodeInc/Roo-Code
- Cursor (CLI/headless): https://cursor.com/docs/cli/headless | https://cursor.com/cli
- SWE-agent: https://github.com/SWE-agent/SWE-agent | https://github.com/SWE-agent/mini-swe-agent
- gptme: https://github.com/gptme/gptme | https://gptme.org/
- Plandex: https://github.com/plandex-ai/plandex | https://plandex.ai/
- Codex CLI: https://github.com/openai/codex | https://developers.openai.com/codex/cli | https://unsloth.ai/docs/basics/codex
- Devika: https://github.com/stitionai/devika
- Kilo Code: https://github.com/Kilo-Org/kilocode | https://kilo.ai/ | https://kilo.ai/docs/ai-providers/ollama
- Gemini CLI: https://github.com/google-gemini/gemini-cli | https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-cli-open-source-ai-agent/ | https://github.com/limkcreply/open-gemini-cli
- Cross-reference directory: https://github.com/bradAGI/awesome-cli-coding-agents
