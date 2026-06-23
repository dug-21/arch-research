# shd-002 / W3 — Multi-step autonomy & tool-call reliability on LOCAL models

**Status:** DIRECTIONAL research (read-only, no install/run). Date: 2026-06-23.
**Capability:** C2 — agentic harness drives multi-step research+coding to completion on a local backend.
**Governing lesson (methodology §12 L1):** "Three harnesses claimed local support; only one streamed tool-calls correctly — harness viability needs a live tool-call smoke test, never doc-reading."

> **Evidence discipline.** Everything below is **doc-claim** or **user-report**, gathered without
> running anything. NONE is a demonstrated artifact from our own smoke test. Per the firewall this
> moves *structure*, not *status*.

## 0. The core finding (read first)

Local/open models are weaker at **native function-calling** (`tool_calls` JSON) than frontier APIs in three repeatedly-observed ways:

1. **Format drift under load.** A model emitting clean `tool_calls` JSON with few tools silently switches to tool calls as **XML/text in `content`** once the tool count grows — observed on Qwen3-Coder via Ollama in Goose at >~5–6 tools (default extension set = 11 tools). [Goose #6883]
2. **Capability-detection failures in the plumbing.** litellm / `@ai-sdk/openai-compatible` mis-report a self-hosted model's tool support → harness refuses tools or mis-reads the envelope. OpenHands (litellm doesn't recognize vLLM-hosted llama3 as tool-capable) and opencode (`finish_reason:"stop"` returned even with tool calls present, killing the loop after one turn). [OpenHands #8424, opencode #20719]
3. **Compounding per-step failure.** Reliability is multiplicative: 95%/call over 8 steps ≈ 66% completion. The reason one-shot demos mislead.

Harnesses that **degrade gracefully** don't depend on native `tool_calls`: **aider** (text SEARCH/REPLACE / whole-file), **Continue** (XML system-message tools), **Goose** only after its XML-fallback (PR #6882). Native-tool-call harnesses (Cline, opencode, OpenHands native) inherit the model's + proxy's weaknesses directly.

## 1. Per-harness read

- **aider** — text edit formats, no function-calling → **degrades gracefully**; failure = edit-format conformance (recoverable via `whole`). Narrower autonomy. [aider #770/#1208/#2371/#3010]
- **Claude Code (T3a)** — native Anthropic tool-use via LiteLLM/LM Studio `/v1/messages` shim. **Most translation hops = highest L1 risk.** Setup guides only; zero demonstrated multi-step local completion. *Doc-claim.*
- **opencode** — full agent loop; **concretely broken on local (#20719):** loop exits after one call (`finish_reason:stop`). Fix proposed, unconfirmed.
- **OpenHands** — autonomous CodeAct native function-calling; **fails to trigger for self-hosted llama3/vLLM** (litellm detection, #8424 unanswered). Docs warn local models "behave like a chatbot."
- **Cline** — native-tool VS Code agent; **worst local track record** (#4362, 100+ reports): error loops, `You did not use a tool`, 2048-token default context exhaustion. Needs 32–64K Modelfile + tool-trained large model.
- **Goose** — native tool-calls + **XML fallback (#6882)** + toolshim; toolshim **caps at 41%** in Goose's own benchmark. Best degradation engineering, still unreliable on weak models.
- **Continue** — **XML "system-message tools"** (graceful by design), but agent mode **hard-disabled without tool-support metadata** (#6677), blocking arbitrary local models.
- **Roo Code** — Cline-lineage; user reports prefer it over Continue for local agentic (Qwen3-Coder-30B + llama.cpp), but **no hard artifact**. Under-evidenced.

Independent benchmark (J.D. Hodges, 13 local LLMs, 40 tool-call cases, LM Studio): Qwen3.5-class 97.5%, GLM-4.7-Flash/Nemotron 95%, Mistral Nemo 92.5%, Qwen3-8B 85%; some specialized tool-callers failed on chat-template incompatibility. **Per-model rate varies wildly and doesn't track size; the harness's parsing/fallback layer matters as much as the model.**

## 2. Tier read (claim, not proven)

- **Tier 1 (best mechanism):** aider, Continue — avoid native `tool_calls`, sidestep the failure class. aider strongest recovery; Continue metadata-gated. No completion proof.
- **Tier 2 (high ceiling, highest risk):** Claude Code (T3a) — biggest ceiling, most hops, zero demonstrated local completion. The textbook L1 trap.
- **Tier 2 (autonomous, plumbing-gated):** OpenHands (litellm detection), Goose (41% toolshim ceiling).
- **Tier 3 (broken/caveated today):** opencode (#20719), Cline (#4362); Roo Code under-evidenced.

**Bottom line:** the determining variable is the **harness↔proxy↔model tool/edit contract, which only fails in motion.** W3 changes no status. It hands shd-003 a precise POC bar: a live smoke test driving **≥6–8 sequential tool calls** through the **real local proxy**, measuring **completion**, not single-call success. The tier ordering is the hypothesis to test, not a result.

## Citations
Cline #4362 · opencode #20719 · OpenHands #8424/#5111 · Goose #6883/#3748 (+PR #6882) · aider #770/#1208/#2371/#3010 · Continue #6677. Docs: aider edit-formats/architect/edit-errors; OpenHands local-llms; opencode models/agents; Continue agent how-it-works; Goose benchmark (2025-03-31); LiteLLM×Claude Code. Independent: jdhodges.com 13-LLM benchmark; localaimaster Cline+Ollama. (Full URLs in the agent transcript.)

**Source caveat:** several blogs cite future/speculative model names (Qwen3.5/3.6, Gemma4); those model-specific claims were NOT relied on — only harness behaviors and GitHub failure artifacts, and even those are user-reports, not our smoke test.
