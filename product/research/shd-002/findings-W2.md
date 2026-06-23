# shd-002 — W2: Local-backend compatibility

**Workstream:** W2 — Local-backend compatibility (N1 owned-HW/budget · N2 no-outage/offline)
**Confidence:** directional · read-only desk research · **no harness installed or run**
**Date:** 2026-06-23

> Question: For each harness, can it target a self-hosted model served via an OpenAI-compatible
> endpoint / litellm / Ollama / vLLM / llama.cpp server? Is local support first-class (config) or a
> fork/hack? Any hard dependency on a specific cloud provider / proprietary API that blocks
> fully-local operation?

**Evidence grading:** `[DOC]` = claimed in official/vendor docs only · `[DEMO]` = third-party user
demonstrated it working (with caveats noted) · `[DOC+DEMO]` = both.

---

## Compatibility matrix (harness × local-endpoint support)

| Harness | Local support | Mechanism | Native protocol the harness speaks | Blockers to fully-local / offline | Evidence |
|---|---|---|---|---|---|
| **Claude Code** | **config** (not native to a local *protocol*) | Speaks **Anthropic Messages API** only. Point `ANTHROPIC_BASE_URL` at a server exposing `/v1/messages`. Three paths: (a) **native Anthropic endpoint** on Ollama >=0.14 / LM Studio >=0.4.1 / **vLLM** — no proxy; (b) **LiteLLM** proxy translating Anthropic->OpenAI for vLLM/llama.cpp/anything; (c) hosted gateways (OpenRouter/Z.AI/DeepSeek) that speak Anthropic natively. | Anthropic Messages API only | Hard-wired to the **Anthropic wire format** — a raw OpenAI/Ollama-`/v1` endpoint is rejected; needs a backend/proxy that speaks `/v1/messages`. Closed-source. No vendor-API *runtime* dependency once `ANTHROPIC_BASE_URL`+`ANTHROPIC_AUTH_TOKEN` set and `ANTHROPIC_API_KEY` unset — runs offline. | [DOC+DEMO] |
| **aider** | **config (first-class)** | Built on **LiteLLM**. `aider --model ollama_chat/<m>` (+`OLLAMA_API_BASE`), or any OpenAI-compatible endpoint via `OPENAI_API_BASE`/`OPENAI_API_KEY` + `openai/<m>` prefix. | OpenAI-compatible / LiteLLM (100+ providers) | None for connectivity. Offline-capable. Agentic ceiling is the *model*, not the harness. | [DOC+DEMO] |
| **opencode** (SST fork) | **config (first-class)** | `provider.*` config block; for local set `npm: "@ai-sdk/openai-compatible"` + `options.baseURL` (e.g. `http://localhost:11434/v1`) and list models. Also native Ollama path. | OpenAI-compatible (Vercel AI SDK adapters) | Standard providers pull metadata from **models.dev** (network) — bypassed by a manual local provider block, so offline works. No cloud login for local. | [DOC+DEMO] |
| **OpenHands** | **config (first-class)** | Built on **LiteLLM**. UI LLM tab -> Base URL `http://host.docker.internal:<port>/v1` (11434 Ollama, 8000 vLLM/SGLang). | OpenAI-compatible / LiteLLM | Connectivity none. **Requires large context** (`OLLAMA_CONTEXT_LENGTH >= 22000`); docs warn local models may give failed/absent tool calls — *model-capability*, not harness. Dockerized `host.docker.internal` gotcha (GH #8318). | [DOC+DEMO] |
| **Cline** (VS Code) | **config (first-class)** | Provider dropdown: dedicated **Ollama** + **LM Studio** entries (auto-populate models), or **"OpenAI Compatible"** with Base URL + placeholder key. | OpenAI-compatible (+ native Ollama) | None for connectivity. Offline-capable. Remote-Ollama `/v1` path can break tool calling for some models — use native `:11434` (no `/v1`). | [DOC+DEMO] |
| **Goose** (Block) | **config (first-class)** | `GOOSE_PROVIDER=ollama` / custom OpenAI-compatible provider; UI lets you uncheck "requires API key" for keyless local (Ollama/vLLM/LM Studio). | OpenAI / Anthropic / Ollama compatible formats | None for connectivity. Has **toolshim** to synthesize tool calls via system prompt for models lacking native tool-calling — designed for weaker local models (known marker-leakage bugs being fixed). | [DOC+DEMO] |
| **Continue** (VS Code/JetBrains) | **config (first-class)** | `config.yaml`/`models.yaml`: `provider: ollama` (AUTODETECT), `provider: llama.cpp` (`apiBase` to llama-server), or `provider: openai` + `apiBase` to any `/v1`. Per-role models. | OpenAI-compatible / Ollama / llama.cpp native | None for connectivity. More IDE-assistant than fully-autonomous agent (W3 concern, not a local blocker). | [DOC+DEMO] |
| **Roo Code** (VS Code) | **config (first-class)** | Dedicated **Ollama**, **LM Studio**, **OpenAI Compatible** providers; Base URL + model + context window (>=32K advised). | OpenAI-compatible (+ native Ollama) | None for connectivity. **Native tool calling required** — model without OpenAI-style tool calling "cannot be used." Model-capability blocker. | [DOC+DEMO] |
| **OpenAI Codex CLI** *(added)* | **config (first-class)** | `~/.codex/config.toml` `[model_providers.*]` with `base_url=http://localhost:11434/v1`; or `codex --oss` for Ollama/LM Studio. | OpenAI-compatible (Responses API default; Chat Completions via provider) | **2026 wire-API trap:** Codex defaults to `wire_api="responses"`; an Ollama serving only Chat Completions 404s — upgrade Ollama or front with a translating proxy. Otherwise offline-capable. | [DOC+DEMO] |

---

## Cleanly local-capable vs. has blockers

**Cleanly local-capable (config-only, no cloud dependency for connectivity):**
aider, opencode, OpenHands, Cline, Goose, Continue, Roo Code, Codex CLI — all expose first-class
config for OpenAI-compatible / Ollama / vLLM / llama.cpp endpoints. None require a specific cloud
provider or proprietary API *at runtime*. All run fully offline against a local endpoint.

**Caveat / partial blockers (none are hard cloud locks; all surmountable):**
- **Claude Code** — only one tied to a **proprietary wire format** (Anthropic Messages API), *not*
  OpenAI-compatible at the protocol layer. Fully-local works **only** via a backend speaking
  `/v1/messages` natively (vLLM, Ollama >=0.14, LM Studio) **or** a LiteLLM Anthropic-shim. Matches
  methodology candidate **T3a**. Closed-source.
- **opencode** — models.dev metadata is a soft network touch; bypassed by manual local provider block.
- **Codex CLI** — `wire_api="responses"` default vs. Chat-Completions-only local servers (404).
- **OpenHands / Roo Code / Goose** — surface **model-capability** blockers (context size, native tool
  calling), not harness/cloud blockers. This is the **L1 risk** (tool-call streaming on local models),
  to be settled by a live smoke test in shd-003, not docs.

**Hard cloud/proprietary-API locks foreclosing fully-local operation: NONE found.** Every surveyed
harness runs against a local endpoint with no internet. The differentiator is *protocol* (Claude Code
= Anthropic-only; all others = OpenAI-compatible) and *model-capability risk*, not vendor lock-in.

---

## Evidence-grade flags (doc-claim vs demonstrated)

- **Connectivity / config** for every harness is `[DOC]` (official) + `[DEMO]` (multiple independent
  third-party walkthroughs) -> high confidence the *connection* works.
- **End-to-end agentic completion on a local model** is only lightly `[DEMO]`:
  - Claude Code + local vLLM (Qwen3-Coder via LiteLLM): one author **demonstrated** a small Flask app
    built across multiple tool-call iterations (91% prefix-cache hit, ~5 min) — but explicitly
    **untested on a large codebase**; 64K context flagged as future constraint. Robust tool-calling at
    scale **not** demonstrated.
  - OpenHands/Roo/Goose docs themselves **warn** local models often fail tool calls — doc-level
    admission, not a measured result.
- **Net:** "can connect locally" is well-evidenced for all 9. "Can autonomously drive a multi-step task
  to completion on a local model" remains **claim-heavy / lightly-demonstrated** — exactly what
  shd-003's live tool-call smoke (L1) must prove. Do not treat any harness as `proven` local on this
  evidence.

---

## Citations

Claude Code / local endpoints:
- https://docs.vllm.ai/en/stable/serving/integrations/claude_code/ (vLLM native Anthropic endpoint)
- https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models (LiteLLM Anthropic shim)
- https://lmstudio.ai/blog/claudecode (LM Studio Anthropic /v1/messages)
- https://www.shawnmayzes.com/ai-engineering/claude-code-local-llm-2026/
- https://www.morphllm.com/use-different-llm-claude-code
- https://dev.to/dcruver/running-claude-code-with-local-llms-via-vllm-and-litellm-599b ([DEMO] Flask app)
- https://medium.com/@michael.hannecke/connecting-claude-code-to-local-llms-two-practical-approaches-faa07f474b0f

aider:
- https://aider.chat/docs/llms/ollama.html
- https://aider.chat/docs/llms/openai-compat.html
- https://aider.chat/docs/llms.html

opencode:
- https://opencode.ai/docs/providers/
- https://opencode.ai/docs/models/
- https://docs.ollama.com/integrations/opencode
- https://github.com/groxaxo/opencode-local-setup

OpenHands:
- https://docs.openhands.dev/openhands/usage/llms/local-llms
- https://dev.to/lynkr/run-openhands-on-any-model-you-want-1mnd
- https://github.com/OpenHands/OpenHands/issues/8318 (host.docker.internal gotcha)
- https://dev.to/udiko/how-to-run-openhands-with-a-local-llm-using-lm-studio-41j6

Cline:
- https://docs.cline.bot/provider-config/openai-compatible
- https://atlassc.net/2025/02/12/configuring-ollama-models-in-cline-via-openai-compatible-provider

Goose:
- https://goose-docs.ai/docs/getting-started/providers/
- https://www.mintlify.com/block/goose/concepts/providers
- https://github.com/block/goose/issues/1198 (OpenAI-like provider)

Continue:
- https://docs.continue.dev/customize/model-providers/overview
- https://docs.continue.dev/guides/ollama-guide
- https://docs.continue.dev/reference

Roo Code:
- https://docs.roocode.com/advanced-usage/local-models
- https://docs.roocode.com/providers/openai-compatible
- https://docs.roocode.com/providers/ollama
- https://docs.roocode.com/providers/lmstudio

OpenAI Codex CLI (added):
- https://developers.openai.com/codex/config-reference
- https://docs.ollama.com/integrations/codex
- https://www.morphllm.com/codex-provider-configuration
- https://knightli.com/en/2026/06/18/codex-cli-oss-mode-local-model-guide/
