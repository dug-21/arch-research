# shd-004 — W4: Target-hardware envelopes & throughput

**Workstream:** W4 — Target-hardware envelopes & throughput (N1 owned-HW/budget)
**Capability:** C1 — Capable LLM inference on local hardware (#4)
**Confidence:** directional · read-only desk research · **no tok/s measured by us**
**Date:** 2026-06-24

> Question: For each owned/budget hardware class, which model×quant combinations are *loadable*
> (VRAM/RAM math), and what is the *reported* generation-throughput (tok/s) ballpark, with the engine
> noted? Measuring tok/s ourselves is the validated follow-on (**shd-005**), explicitly out of scope here.

**CRITICAL firewall:** Every throughput number below is **doc/community-reported, NOT demonstrated by
us.** Each tok/s cell carries the **[REPORTED]** flag. tok/s is *memory-bandwidth-bound* and varies
with engine, quant kernel, context length, draft model, and thermal state — treat every figure as a
ballpark, not a spec.

**Evidence grading:** `[DOC]` = vendor/official doc only · `[COMM]` = community/third-party benchmark
(LocalLLaMA, blog, GH discussion) demonstrated it on *their* HW · `[DOC+COMM]` = both. **None are
`[DEMO-by-us]`.**

---

## Footprint math (the loadability basis)

Q4_K_M GGUF weight ≈ **0.55–0.62 GB per billion params**; AWQ/GPTQ INT4 ≈ similar. KV cache and
runtime overhead add **~1–4 GB** depending on context length and engine (vLLM reserves more). Working
estimates used below (weights + modest 8–16K-context KV + overhead):

| Model class | Q4 weights | + KV/overhead | **Total to load (Q4)** |
|---|---|---|---|
| ~7B dense | ~4.3 GB | ~1.5 GB | **~5.5–6.5 GB** |
| ~14B dense | ~8.5 GB | ~2 GB | **~10–12 GB** |
| ~32B dense | ~18–20 GB | ~2–4 GB | **~21–23 GB** (tight on 24 GB) |
| DeepSeek-Coder-V2-Lite-class MoE (16B total / ~2.4B active) | ~10.4 GB | ~2 GB | **~12–13 GB** |
| Qwen3-Coder-30B-A3B-class MoE (30B total / ~3.3B active) | ~18–20 GB | ~1–2 GB | **~19–22 GB** |

**MoE note (load-bearing):** an MoE loads its *full* weight set into memory (so footprint ≈ a dense
model of equal total params), but computes only the *active* params per token — so it **decodes at the
speed of a small dense model while occupying the memory of a large one.** This is why the MoE rows are
the throughput outliers below.

---

## 1. Hardware-envelope table

Decode = generation tok/s. All tok/s rows are **[REPORTED — not demonstrated by us]**.

| HW class | Model×quant that fits | Approx footprint | Reported decode tok/s | Engine the figure is from | Flag | Grade |
|---|---|---|---|---|---|---|
| **Consumer NVIDIA 24 GB** (RTX 3090 / 4090) | 7B Q4_K_M | ~6 GB | **~110–131** (4090); 3090 ~15–25% lower (bandwidth) | llama.cpp | [REPORTED] | [COMM] |
| 24 GB | 14B Q4_K_M | ~10–12 GB | **~59–69** (4090) | llama.cpp | [REPORTED] | [COMM] |
| 24 GB | 14B AWQ/GPTQ INT4 | ~10–12 GB | **single-stream ~50–70; batched 500–900+ aggregate** | vLLM (awq_marlin) | [REPORTED] | [COMM] |
| 24 GB | **32B dense Q4_K_M** (fits *barely* — ~22 GB, little KV room) | ~21–23 GB | **~34** (4090); **~43 mean / 67 peak with 4B draft (spec-decode)** | llama.cpp | [REPORTED] | [COMM] |
| 24 GB | 32B AWQ on vLLM | ~18–20 GB weights, KV pushes >24 GB | runnable only with `--max-model-len ~2048` (short ctx) — **not practical at standard context** | vLLM | [REPORTED] | [COMM] |
| 24 GB | MoE 16B-Lite-class Q4 | ~12–13 GB | **fast (small active set); community: 14B-quality at near-7B speed**, exact 3090 figure not isolated in sources | llama.cpp | [REPORTED] | [COMM] |
| **Consumer NVIDIA 16 GB** (4060 Ti-16G / 4070 Ti S) | up to ~32–34B Q4 *capacity*, but 14B is the comfortable target | 14B ≈ ~10–12 GB (≈14 GB usable after display) | **14B Q4 ~22–34** (4060 Ti-16G ~22; faster 16 GB cards higher) | llama.cpp | [REPORTED] | [COMM] |
| **Consumer NVIDIA 12 GB** (4070) | 7B Q4 comfortable; 14B Q4 tight (~10.8 GB usable) | 7B ~6 GB / 14B borderline | **7–14B ~25–40** | llama.cpp | [REPORTED] | [COMM] |
| **Apple Silicon** unified mem (M2/M3/M4 Pro/Max, 32–128 GB) | 7B Q4 | ~6 GB | **M2 Pro ~38; M3 Pro ~31; M4 Pro ~50** (Q4_0, 7B) | llama.cpp | [REPORTED] | [COMM] |
| Apple Silicon | 32B dense Q4 | ~20 GB (needs ≥32 GB box) | **~15–30** (scales with bandwidth: M3 Max ~400, M4 Max ~546 GB/s) | llama.cpp / MLX | [REPORTED] | [COMM] |
| Apple Silicon | **MoE 30B-A3B-class 4-bit (MLX)** | ~18–20 GB (needs ≥32 GB box) | **M4 Pro ~130; M4 Max ~68–100+** | **MLX** (≈3× the old llama.cpp backend on same chip) | [REPORTED] | [COMM] |
| **CPU / RAM-only** (modern multi-core + DDR5, dual-channel ~80 GB/s) | 7B Q4 | ~6 GB RAM | **~8–22** | llama.cpp | [REPORTED] | [COMM] |
| CPU / RAM-only | 14B Q4 | ~10–12 GB RAM | **~5–15** (≈20 on strong mini-PC builds) | llama.cpp | [REPORTED] | [COMM] |
| CPU / RAM-only | 32B Q4 | ~20 GB RAM (needs 32–64 GB) | **~2–7** | llama.cpp | [REPORTED] | [COMM] |
| CPU / RAM-only | MoE 16B-Lite-class Q4 | ~10–13 GB RAM | **markedly higher than 14B dense** (only ~2.4B active per token) — community-reported "usable on CPU"; exact figure not isolated | llama.cpp | [REPORTED] | [COMM] |
| **Small multi-GPU** 2×24 GB (48 GB) | unlocks **32B dense at full context**, or 70B-class Q4, or large-ctx 32B | 70B Q4 ~40 GB; 32B + big KV comfortable | per-request decode ≈ single-GPU (tensor-parallel adds modest overhead, not 2× single-stream); **big win is concurrency/aggregate via vLLM batching** | vLLM (tensor-parallel) | [REPORTED] | [COMM] |

> **Capacity unlock for 2×24 GB only** — the *distribution mechanism* (tensor parallel vs pipeline vs
> llama.cpp `--split-mode`, NVLink vs PCIe) is **handed off to W5.** W4 records only that 48 GB lifts
> the 32B-at-full-context and 70B-class ceilings; it does not specify how.

---

## 2. Usable-throughput note (open question for the POC, not a verdict)

What counts as "usable" tok/s depends on the **loop shape**, and this is for **shd-005** to settle by
measuring our actual agentic coding loop — not for W4 to declare:

- **Interactive / human-in-the-loop** (chat-style edits, single stream): readability is ~human reading
  speed (~10 tok/s), but an *agentic* loop emits long tool-call/diff sequences, so **~20–40 tok/s is a
  commonly cited comfort floor** for it to feel responsive. This is a **community heuristic, not a
  measured threshold for our harness.**
- **Agentic / batch / autonomous** (multi-step, many tool iterations, possibly concurrent): aggregate
  throughput and **prefill (prompt-processing) speed on long contexts** matter more than single-stream
  decode — a coding agent re-reads large contexts each turn, so **time-to-first-token and prefill
  tok/s can dominate wall-clock** more than decode. vLLM's continuous batching (500–900+ aggregate
  tok/s on a 4090 for small models) is the lever here; llama.cpp wins single-stream TTFT but does not
  batch comparably.
- **Open question the POC must answer:** for *our* specific harness × model × task, what minimum
  decode **and** prefill tok/s makes the loop converge within an acceptable wall-clock and budget?
  Decode tok/s alone is the wrong single metric. **Do not read any row above as "fast enough" — that
  verdict belongs to a measured shd-005 run.**

---

## 3. Best owned-HW value callout (qualitative)

**Single best coding-model-at-usable-tok/s per dollar: a single used RTX 3090 (24 GB).** Reasoning,
directional and qualitative:

- **The determining constraint is the 24 GB VRAM × memory-bandwidth product.** 24 GB is the threshold
  that puts a **32B dense Q4 in reach** (the survey's strongest dense coding tier) and an MoE
  30B-A3B-class model comfortably, and ~936 GB/s bandwidth gives the best $/decode-tok/s of any owned
  option. The 3090 is typically **half the price of a 4090** for the *same* 24 GB and ~85–90% of its
  inference throughput (decode is bandwidth-bound, and the gap between them is far smaller than the
  price gap).
- **Apple Silicon is the strong runner-up where the box already exists** (zero marginal cost) or where
  **>24 GB-but-affordable** matters — a 64–128 GB M-series runs models a single 24 GB GPU cannot hold,
  and **MLX + MoE (130 tok/s on M4 Pro) is the standout combination**, but $/tok/s for a *new* Mac
  purchase is worse than a used 3090 at the 32B-dense tier.
- **16 GB consumer GPU** is the budget floor: comfortable for 7–14B and MoE-16B-Lite, but it **cannot
  hold a 32B dense at usable context**, capping coding-model quality.
- **CPU/RAM-only** maximizes capacity per dollar (128 GB DDR5 is cheap) but **2–7 tok/s on 32B is
  below the plausible interactive comfort floor** — viable for batch/overnight or for **MoE models
  only** (small active set is the CPU's friend), not for an interactive coding loop.
- **2×24 GB** is best *capacity per dollar at the high end* (unlocks 70B / full-context 32B and real
  concurrency via vLLM) but is a **throughput-headroom / concurrency** play, not a single-stream
  $/tok/s win — and the distribution cost/complexity is W5's call.

**Caveat / what I could not verify:** I did **not** isolate a clean 3090-specific 32B-Q4 decode
figure (most community benchmarks report 4090); the 3090 number above is **inferred from the
bandwidth ratio**, flagged accordingly. Exact MoE tok/s on 3090 and on CPU were not pinned in the
sources. **No figure here is demonstrated by us — shd-005 owns the measurement.**

---

## 4. Citations (grouped by HW class)

**Consumer NVIDIA GPU (24 / 16 / 12 GB):**
- https://awesomeagents.ai/leaderboards/home-gpu-llm-leaderboard/ (4090 by-tier: 7B ~131, 14B ~64–69, 32B Q4 ~34 tok/s, llama.cpp)
- https://localllm.in/blog/llamacpp-vram-requirements-for-local-llms (VRAM footprint guide)
- https://github.com/outsourc-e/qwen36-4090-recipes (32B on single 4090; spec-decode 43 mean/67 peak; quant pitfalls)
- https://www.databasemart.com/blog/vllm-gpu-benchmark-rtx4090 (vLLM AWQ single-GPU throughput)
- https://gigagpu.com/rtx-4090-24gb-awq-quantization-guide/ (AWQ INT4 / Marlin kernels, 24 GB sweet spot)
- https://gigagpu.com/rtx-4090-24gb-vllm-setup-3/ (32B AWQ needs `--max-model-len` to fit KV)
- https://www.hardware-corner.net/gpu-llm-benchmarks/rtx-4060-ti-16gb/ (4060 Ti-16G: 14B ~22 t/s gen, ~918 t/s prompt @16K)
- https://www.sitepoint.com/10gb-vram-local-llm-the-complete-setup-guide-2026/ (12 GB / usable-VRAM-after-display caveat)
- https://www.hardware-corner.net/gpu-ranking-local-llm/ (token-gen ranking, memory-bound thesis)
- https://corelab.tech/llmgpu/ (VRAM-per-dollar tier list; 3090 value framing)

**Apple Silicon (unified memory, MLX):**
- https://github.com/ggml-org/llama.cpp/discussions/4167 (canonical M-series tg: M2 Pro 37.9, M3 Pro 30.7, M4 Pro 49.6 tok/s @7B Q4_0; bandwidth per chip)
- https://pub.towardsai.net/apples-mlx-runs-local-llms-3x-faster-than-llama-cpp-until-your-context-hits-40k-715ec441afbb (MLX vs llama.cpp; degrades past ~40K ctx)
- https://siliconscore.com/models/qwen3-coder-30b-a3b/ (30B-A3B MoE on Apple Silicon, benchmark rows)
- https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide (MLX tok/s + memory by RAM tier)
- https://llmcheck.net/benchmarks (Apple Silicon real tok/s by chip/model/quant)
- https://www.sitepoint.com/mac-m3-max-vs-rtx-4090-local-llm-performance-showdown-2026/ (Mac vs 4090 framing)

**CPU / RAM-only:**
- https://45squared.com/llms-that-run-on-cpu-only-hardware/ (CPU sweet spot 1–14B; 8–22 tok/s; 32B 2–7 tok/s)
- https://github.com/ggml-org/llama.cpp/discussions/3167 (canonical CPU performance discussion)
- https://stochasticsandbox.com/posts/deep-dive-mini-pc-local-ai-2026-04-04/ ($550 mini-PC, 28B-class ~20 tok/s build)
- https://carteakey.dev/blog/local-inference/local-llm-optimization/ (CPU bandwidth-bound thesis, DDR5 channels)

**MoE class (DeepSeek-Coder-V2-Lite / Qwen3-Coder-30B-A3B):**
- https://gigagpu.com/deepseek-coder-v2-vram-requirements/ (V2-Lite Q4_K_M ~10.36 GB, ~2.4B active)
- https://gigagpu.com/run-deepseek-on-rtx-3090/ (V2-Lite fits comfortably on 3090)
- https://www.arsturn.com/blog/running-qwen3-coder-30b-at-full-context-memory-requirements-performance-tips (30B-A3B HW/perf)
- https://news.ycombinator.com/item?id=43856489 (Qwen3 on MacBook via MLX, community reports)

**Engine comparison (llama.cpp vs vLLM — why the figure source matters):**
- https://developers.redhat.com/articles/2026/06/15/llamacpp-vs-vllm-choosing-right-local-llm-inference-engine
- https://contracollective.com/blog/vllm-vs-llama-cpp-batching-production-inference-2026 (single-stream ~65 vs ~71 tok/s 4090/8B; batched 920 vs 155 aggregate)
- https://insiderllm.com/guides/llamacpp-vs-ollama-vs-vllm/ (one-user vs many framing)

---

## Flags / what to carry forward

- **Firewall:** zero figures demonstrated by us; all **[REPORTED]**. tok/s measurement is **shd-005**.
- **W5 hand-off:** 2×24 GB distribution mechanism (tensor/pipeline parallel, NVLink/PCIe, vLLM TP vs llama.cpp split) — capacity unlock noted, mechanism not specified here.
- **Determining constraint:** **24 GB VRAM × memory bandwidth** is the line that gates the 32B-dense coding tier; it is the single most decision-relevant envelope variable.
- **Open question for the goal:** "usable tok/s" is undefined until the POC measures *our* harness loop (decode **and** prefill/TTFT on long contexts) — Section 2 is framed as a question, not a verdict.
- **Unverified gaps:** clean 3090-specific 32B-Q4 decode (inferred from bandwidth ratio), exact MoE tok/s on 3090 and CPU — flagged in-line; do not promote to firm numbers.
