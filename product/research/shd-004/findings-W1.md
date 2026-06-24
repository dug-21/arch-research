# shd-004 — W1: Inference engine / runtime inventory

**Workstream:** W1 — Inference engine / runtime inventory (capability **C1** — capable LLM inference on local hardware)
**Confidence:** directional · read-only desk research · **no engine installed or run by us**
**Date:** 2026-06-24

> Question: Enumerate the engines/runtimes that serve LLM inference locally. For each: capability profile, target hardware, quant formats loaded, and — the hard filter — the **serving protocol** (OpenAI-compatible `/v1/chat/completions`? Anthropic-shimmable `/v1/messages`? or raw/library-only?). The C2 harness slate (aider, Claude Code + local shim, Continue) must be able to speak to the engine.

**Evidence grading:** `[DOC]` = official/vendor docs only · `[DEMO]` = third-party user demonstrated it working (caveats noted) · `[DOC+DEMO]` = both. **Nothing here is demonstrated by us** — every protocol/format claim is doc-claim or community-report. This research moves *structure*, never *status*.

**Protocol legend (the hard filter):**
- **OAI** = native OpenAI-compatible `/v1/chat/completions` HTTP server → speaks to aider & Continue directly.
- **ANT-native** = exposes Anthropic Messages `/v1/messages` natively → Claude Code points `ANTHROPIC_BASE_URL` at it, **no proxy**.
- **ANT-shim** = no native `/v1/messages`, but OAI endpoint can be wrapped by **LiteLLM** (Anthropic→OpenAI translation) for Claude Code.
- **raw-only** = library / no HTTP server (or non-OAI server) → needs a wrapper to reach the C2 slate.

---

## Engine table (engine × hardware × quant × protocol × tool-call caveat)

| Engine | One-line profile | Target HW | Quant formats loaded | Serving protocol (OAI? ANT?) | Tool-call / streaming caveat | Evidence |
|---|---|---|---|---|---|---|
| **llama.cpp** (`llama-server`) | C/C++ reference engine; root of the GGUF ecosystem; CPU-first, broadest backend reach | CUDA · ROCm · Metal · Vulkan · CPU (incl. Arm/KleidiAI) | **GGUF** (all variants: Q2_K…Q8_0, IQ-quants, f16/bf16) | **OAI** (`/v1/chat/completions`, `/v1/completions`, embeddings, responses) **+ ANT-native** (`/v1/messages`) | Function-calling needs `--jinja` + correct chat template; some models need template overrides. SSE streaming supported. Tool-call quality is template/model-dependent. | [DOC+DEMO] |
| **Ollama** | Batteries-included llama.cpp wrapper; model registry + one-command install; default local single-user runtime | CUDA · ROCm · Metal · CPU | **GGUF** (registry pulls; imports GGUF/safetensors) | **OAI** (`/v1/...`, beta) **+ ANT-native** (Anthropic-compat announced **2026-01-16**; streaming + tool calls native) | Anthropic-compat needs `OLLAMA_CONTEXT_LENGTH` raised (e.g. 32768) or tool loops truncate. OAI `/v1` path historically weaker for tool calls than native `/api`. | [DOC+DEMO] |
| **vLLM** | Production throughput server; PagedAttention; the NVIDIA-GPU concurrent-serving default | CUDA · ROCm · (TPU/Gaudi/CPU exp.) · multi-GPU (TP/PP) | **safetensors-fp16/bf16**, **AWQ**, **GPTQ**, **FP8**, GGUF (partial/exp.) | **OAI** (first-class) **+ ANT-native** (`/v1/messages`, documented Claude Code integration) | Tool streaming w/ hermes/mistral parsers has a **history of bugs** (raw text instead of parsed `tool_calls`; users disable streaming to recover) — GH #31871/#21544/#10979. **Claude Code shim trap:** CC ≥ 2.1.154 sends roles that break vLLM Anthropic validation (GH #44000); prefix-cache hash fix only > v0.17.1. | [DOC+DEMO] |
| **SGLang** | Throughput peer to vLLM; **RadixAttention** prefix-cache wins on shared-context / agentic loads (~+29% vs vLLM on shared prefixes) | CUDA · ROCm · multi-GPU | **safetensors-fp16/bf16**, **AWQ**, **GPTQ**, **FP8** | **OAI** (first-class; tool_choice via EBNF/xgrammar) | Tool calling needs explicit `--tool-call-parser` (qwen25, deepseekv3, gpt-oss, pythonic…); `tool_choice` fully supported only on **xgrammar** backend, not outlines. Parser regressions on newer families (GLM5.1, GH #22922). **No native Anthropic → ANT-shim (LiteLLM).** | [DOC+DEMO] |
| **TGI** (text-generation-inference) | HuggingFace's early prod server — **archived / maintenance mode since 2025-12-11**; HF redirects users to vLLM/SGLang/llama.cpp/MLX | CUDA · ROCm · (Gaudi/Inferentia) · multi-GPU | safetensors-fp16, **AWQ**, **GPTQ**, **EETQ**, FP8, GGUF (limited) | **OAI** (`/v1/chat/completions`) — **no native Anthropic** → ANT-shim | Maintenance mode = no new parser/feature work; tool-calling frozen at last release. **De-prioritize.** | [DOC+DEMO] |
| **LM Studio** | Desktop GUI runtime (bundles llama.cpp **+ MLX** engines); developer server mode; popular on Mac | Metal (MLX + GGUF) · CUDA · CPU | **GGUF** + **MLX** | **OAI** (`/v1/...`) **+ ANT-native** (`/v1/messages`, added **2026-01-30** in 0.4.1; streaming + tool calls) | Closed-source app (server mode exists, not headless-pure). Anthropic-compat is recent; tool-call reliability tracks the underlying model/engine. | [DOC+DEMO] |
| **MLX / MLX-LM** (`mlx_lm.server`) | Apple's array framework + LM toolkit; native Apple-Silicon path; unified-memory efficient | **Apple Metal only** (Apple Silicon) | **MLX** (native quant) + safetensors-fp16 (converts) | **OAI** (`/v1/chat/completions`, `/v1/models`; **`/v1/responses`** added 2026) — **no native Anthropic** → ANT-shim | Tool calling via `--tool-call-parser` (qwen3, qwen3_coder, harmony, glm4_moe, minimax_m2…); parser coverage model-family-gated. Third-party `mlx-openai-server` / `vllm-mlx` add batching + (vllm-mlx) **native Anthropic** + MCP. | [DOC+DEMO] |
| **ExLlamaV2 + TabbyAPI** | Fastest single-NVIDIA-GPU INT4 path; **EXL2** measurement-based mixed-bit quant; TabbyAPI is the OAI server shell | CUDA (Ampere+) · multi-GPU (split) | **EXL2** (primary), GPTQ, fp16 | **OAI** (TabbyAPI = "OAI compatible, lightweight, fast"); bare ExLlamaV2 = **raw/library-only** → ANT-shim via LiteLLM | Library alone has no server — **must** use TabbyAPI for HTTP. Tool-calling exists but thinner / less battle-tested than vLLM/SGLang; verify per model. | [DOC+DEMO] |
| **KoboldCpp** | One-binary, zero-install GGUF server + UI; full sampler set (DRY/XTC); creative-writing default (w/ SillyTavern) | CUDA · ROCm · Metal · Vulkan · CPU | **GGUF** | **OAI** (+ own KoboldAI API) — **no native Anthropic** → ANT-shim | OAI tool-calling present but not its focus; built for chat/RP not agentic loops — tool reliability unverified. | [DOC] |
| **llamafile** | Single-executable model+runtime (Cosmopolitan libc); double-click to run; portable | CPU · CUDA · Metal (cross-OS single binary) | **GGUF** | **OAI** (built on llama.cpp server) — **no native Anthropic** → ANT-shim | Distribution gimmick over llama.cpp; tool-calling inherits llama.cpp's `--jinja` path. Lower release cadence than upstream. | [DOC] |
| **Jan** | Desktop app + local server; GGUF via bundled llama.cpp ("Cortex") engine | CUDA · Metal · CPU | **GGUF** | **OAI** (local server) — **no native Anthropic** → ANT-shim | Consumer-desktop framing; tool-calling tracks underlying llama.cpp engine. | [DOC] |
| **LocalAI** | Docker-native, broad OpenAI-API parity (chat/embeddings/image/audio); multi-backend aggregator | CUDA · ROCm · Metal · CPU | **GGUF**, **GPTQ** (+ others via backends) | **OAI** (broad parity) — **no native Anthropic** → ANT-shim | Aggregator → tool-call behavior depends on selected backend; breadth over depth. | [DOC] |
| **nano-vllm** | Minimal (~1.2k-LOC) educational vLLM reimplementation; pedagogy, not production | CUDA | safetensors-fp16 | **raw / library-only** (no hardened OAI server) | Not a serving target — reference implementation. **Excluded from C2 slate.** | [DOC] |
| **TensorRT-LLM** *(surfaced)* | NVIDIA's compiled-kernel max-throughput engine; build-step heavy | CUDA (NVIDIA only) · multi-GPU | TRT engines, FP8, INT4-AWQ, INT8 | **OAI** (via Triton / its OpenAI server) — **no native Anthropic** → ANT-shim | Ahead-of-time engine compilation per model/GPU; least "drop-in." Heavyweight for a local dev loop. | [DOC] |

---

## Disqualified-or-shim-required callout (C2-protocol fit)

The C2 slate speaks two wire formats: **OpenAI** (aider, Continue) and **Anthropic Messages** (Claude Code, via `ANTHROPIC_BASE_URL` + local shim per shd-002 T3a).

**Tier A — speaks Claude Code natively (no proxy) AND OpenAI for aider/Continue:**
- **llama.cpp**, **Ollama**, **vLLM**, **LM Studio** — all four expose **both** `/v1/chat/completions` and a native `/v1/messages`. Lowest-friction C2 targets. (vLLM's Anthropic path carries the CC-version-compat caveat GH #44000 — pin compatible CC/vLLM versions.)

**Tier B — OpenAI-native, needs a LiteLLM Anthropic-shim for Claude Code:**
- **SGLang**, **TGI**, **MLX-LM**, **TabbyAPI** (ExLlamaV2), **KoboldCpp**, **llamafile**, **Jan**, **LocalAI**, **TensorRT-LLM**. All reach aider/Continue directly; Claude Code requires the LiteLLM Anthropic→OpenAI proxy (shd-002 path (b)). No hard blocker — just an extra hop.

**Disqualified / not a serving target (raw-only, no hardened HTTP server):**
- **ExLlamaV2 (bare library)** — usable only **through TabbyAPI**; the library alone can't speak the slate.
- **nano-vllm** — educational reimplementation, no production server. **Drop from the candidate slate.**

**De-prioritize (alive-but-stalled):**
- **TGI** — archived / maintenance mode since 2025-12-11; HuggingFace itself redirects to vLLM/SGLang/llama.cpp/MLX. Keep for completeness only.

---

## Evidence-grade flags (doc-claim vs demonstrated)

- **Protocol existence** (OAI endpoint present; native Anthropic present) is **`[DOC+DEMO]`** for the Tier-A four (llama.cpp, Ollama, vLLM, LM Studio) plus SGLang/MLX-LM/TabbyAPI — official docs **plus** independent third-party walkthroughs. Strong confidence the *connection shape* exists.
- **Tool-call / streaming reliability** is the soft spot and stays **claim-heavy**: vLLM's hermes/mistral streaming-parser bugs (GH #31871, #21544, #10979) and SGLang's parser regressions (GH #22922) are *reported*, not measured by us. This is exactly the **L1 risk** carried from shd-002 — the harness↔proxy↔model tool-call contract is settled by a **live smoke test (C2)**, not by docs.
- Engines marked **`[DOC]`-only** (KoboldCpp, llamafile, Jan, LocalAI, nano-vllm, TensorRT-LLM) have weaker independent agentic-tool-call evidence; their OAI endpoints are documented but fitness for autonomous tool loops is unverified.
- **Nothing is `proven`.** No engine was installed or exercised by us. Treat every cell as structure to be validated, not status.

**Determining constraint (directional ranking):** the binding filter is **not** raw throughput — it is **reliable native-tool-call + streaming over an OAI/Anthropic endpoint on a quant the hardware can hold.** On that axis: the **Tier-A four** (llama.cpp / Ollama / vLLM / LM Studio) lead on protocol-fit; **SGLang** leads on agentic throughput but costs a shim; **MLX-LM** is the only first-class Apple-Silicon path; **ExLlamaV2/TabbyAPI** wins single-GPU INT4 speed but is thinner on tool-calling. The completion question (which actually drives a multi-step agent loop to done on a local model) is **not** settled here — it belongs to the C2 validated POC.

---

## Citations

**llama.cpp**
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md (OAI + `/v1/messages` Anthropic + `--jinja`)
- https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md
- https://github.com/ggml-org/llama.cpp
- https://learn.arm.com/learning-paths/servers-and-cloud-computing/llama-cpu/llama-server/ (Arm/KleidiAI CPU)

**Ollama**
- https://docs.ollama.com/api/anthropic-compatibility (native, 2026-01-16)
- https://renezander.com/guides/claude-code-local-llm-anthropic-base-url/
- https://www.glukhov.org/llm-hosting/comparisons/hosting-llms-ollama-localai-jan-lmstudio-vllm-comparison/

**vLLM**
- https://docs.vllm.ai/en/stable/serving/integrations/claude_code/ (native Anthropic Messages)
- https://github.com/vllm-project/vllm/issues/44000 (CC ≥ 2.1.154 breaks Anthropic validation)
- https://github.com/vllm-project/vllm/issues/31871 (hermes streaming returns raw text)
- https://github.com/vllm-project/vllm/issues/21544 (hermes parser streaming error)
- https://github.com/vllm-project/vllm/pull/10979 (hermes/mistral streaming fixes)
- https://docs.vllm.ai/en/latest/features/tool_calling/

**SGLang**
- https://docs.sglang.ai/advanced_features/function_calling.html
- https://docs.sglang.ai/advanced_features/tool_parser.html (parsers; xgrammar backend)
- https://github.com/sgl-project/sglang/issues/22922 (GLM5.1 parser regression)
- https://tokenmix.ai/blog/sglang-openai-compatible-api

**TGI**
- https://github.com/huggingface/text-generation-inference/blob/main/README.md (maintenance mode; redirect to vLLM/SGLang/llama.cpp/MLX)
- https://huggingface.co/docs/text-generation-inference/en/index

**LM Studio**
- https://lmstudio.ai/docs/developer/anthropic-compat (native `/v1/messages`)
- https://lmstudio.ai/blog/claudecode (0.4.1 Anthropic streaming + tool calls)

**MLX / MLX-LM**
- https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md (OAI endpoints)
- https://github.com/ml-explore/mlx-lm/pull/1207 (`/v1/responses`, 2026)
- https://github.com/cubist38/mlx-openai-server (third-party OAI server w/ tool parsers)
- https://github.com/waybarrios/vllm-mlx (OAI + native Anthropic + MCP on Apple Silicon)

**ExLlamaV2 / TabbyAPI**
- https://github.com/theroyallab/tabbyAPI/ (OAI-compatible Exllama server)
- https://github.com/turboderp-org/exllamav2 (library; EXL2 quant)
- https://localaimaster.com/blog/exllamav2-tabbyapi-guide

**KoboldCpp**
- https://github.com/LostRuins/koboldcpp/ (one-file GGUF server, OAI-compat API)
- https://localaimaster.com/blog/koboldcpp-setup-guide

**llamafile / Jan / LocalAI / nano-vllm**
- https://dev.to/rosgluk/local-llm-hosting-complete-2025-guide-ollama-vllm-localai-jan-lm-studio-more-1dcl
- https://www.sitepoint.com/local-llms-complete-guide/
- https://www.coinfeeds.ai/ai-blog/run-llms-locally

**Cross-engine comparison / TGI-archived / TensorRT-LLM**
- https://tensorfoundry.io/blog/llm-inference-servers-compared
- https://sesamedisk.com/local-inference-engines-2026-comparison/
- https://explore.n1n.ai/blog/llm-inference-engine-comparison-vllm-tgi-tensorrt-sglang-2026-03-13
- https://theaiengineer.substack.com/p/vllm-vs-ollama-vs-sglang-vs-tensorrt

---

**Compact summary:** 14 engines inventoried. **Four are Anthropic-native AND OpenAI-native** (llama.cpp, Ollama, vLLM, LM Studio) → lowest-friction C2 targets. Everything else is OpenAI-native and needs a **LiteLLM Anthropic-shim** for Claude Code (SGLang, TGI, MLX-LM, TabbyAPI, KoboldCpp, llamafile, Jan, LocalAI, TensorRT-LLM). **Disqualified as serving targets:** bare ExLlamaV2 (library-only → use TabbyAPI) and nano-vllm (educational, drop). **De-prioritize:** TGI (archived/maintenance since 2025-12-11). **Open flag (L1):** tool-call/streaming reliability is doc-claim only — vLLM hermes/mistral parser bugs and SGLang parser regressions are reported, not verified by us; settle in the C2 live smoke test.
