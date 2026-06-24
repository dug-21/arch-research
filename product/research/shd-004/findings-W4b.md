# shd-004 — W4b: $5K workstation-tier hardware envelope (N1 extension)

**Workstream:** W4b — $5K workstation-tier hardware envelope (N1 raised ceiling)
**Capability:** C1 — Capable LLM inference on local hardware (#4)
**Confidence:** directional · read-only desk research · **no tok/s measured by us**
**Date:** 2026-06-24
**Extends, does not replace:** `findings-W4.md` (minimum owned-HW / 24 GB-and-below tier). Same evidence grading, same [REPORTED] flags, same footprint math.

> Scope shift: N1 budget ceiling raised from "minimum owned HW" to a **~$5K workstation tier** — still owned, still fully offline (N1/N2 hold). Question: at ~$5K, which model×quant combinations become *loadable* that did not fit on a 24 GB card, and at what *reported* decode tok/s — separating **capacity** (what fits) from **memory bandwidth** (what sets decode speed)?

**CRITICAL firewall:** Every throughput number below is **doc/community-reported, NOT demonstrated by us.** Each tok/s cell carries **[REPORTED]**. tok/s is *memory-bandwidth-bound* and varies with engine, quant kernel, context length, draft model, batch size, and thermal state — ballpark, not spec. The completion question (is a >32B model worth the step-up?) is settled by a measured POC (shd-005), not here.

**Evidence grading:** `[DOC]` = vendor/official doc · `[COMM]` = community/third-party benchmark on *their* HW · `[DOC+COMM]` = both. **None are `[DEMO-by-us]`.**

---

## The load-bearing frame: capacity ≠ bandwidth

Two independent variables decide whether a box helps:

- **Capacity (GB)** — does the model+quant+KV cache *fit*? Sets which models are reachable at all. The whole point of the $5K tier is that 96–512 GB unlocks 70B-class dense, full-context 32B, and large MoE that 24 GB cannot hold.
- **Memory bandwidth (GB/s)** — sets **decode tok/s** for the part of the model touched per token. Decode is bandwidth-bound: a *dense* model reads ~all weights per token, so dense tok/s ≈ (bandwidth ÷ active-weight-bytes). An **MoE reads only its active experts per token**, so it decodes far faster than its total size implies (this is the W4 MoE thesis, and it is the hinge of this tier).

**The counterintuitive finding (stated up front, the reason this extension exists):** the unified-memory appliances unlock huge *capacity* but carry *lower bandwidth than a used RTX 3090*:

| Box | Bandwidth | vs RTX 3090 (~936 GB/s) |
|---|---|---|
| NVIDIA DGX Spark / GB10 | **~273 GB/s** | **~0.29× — under a third** |
| AMD Strix Halo (Ryzen AI Max+ 395) | ~256 GB/s theoretical (**~215 GB/s measured**) | **~0.23–0.27×** |
| RTX 3090 (minimum tier baseline) | ~936 GB/s | 1.0× |
| Mac Studio M3 Ultra | ~800 GB/s | ~0.85× |
| RTX 5090 (32 GB) | **~1,790 GB/s** | ~1.9× |
| RTX PRO 6000 Blackwell (96 GB) | ~1,790 GB/s | ~1.9× |

So Spark and Strix Halo **load big dense models the 3090 cannot — and then decode them *slower* than the cheap 24 GB card would** (if it could fit them). They convert a capacity problem into a speed problem. They win precisely where bandwidth-per-active-param is favorable: **MoE (low active params) and long-context experimentation**, not dense single-stream decode.

### Footprint math (extends W4)
Q4 GGUF ≈ 0.55–0.62 GB/B param; INT4 AWQ/GPTQ similar. FP8 ≈ ~1 GB/B. KV cache grows linearly with context and is the silent capacity eater at long context (always ~FP16). Newly-reachable classes at this tier:

| Model class | Q4 weights | FP8 weights | Total to load (Q4, modest ctx) | Fits 24 GB? |
|---|---|---|---|---|
| 70B dense | ~40 GB | ~70 GB | ~42–45 GB | No |
| 32B dense @ full 128K ctx | ~20 GB + large KV | — | ~30–45 GB w/ big KV | No (KV blows past 24 GB) |
| Qwen3-Coder-30B-A3B MoE @ full ctx | ~18–20 GB + KV | — | ~22–40 GB | Borderline→No at long ctx |
| ~120B MoE (e.g. GPT-OSS-120B class) | ~65 GB | — | ~70 GB | No |
| Qwen3-Coder-480B MoE | ~270 GB Q4 | — | **~270+ GB — still out** except 512 GB Mac | **No (ceiling note)** |

**Ceiling note:** even the $5K tier does **not** reach the largest MoE (Qwen3-Coder-480B ≈ 270 GB Q4). Only the 512 GB Mac Studio M3 Ultra holds it, and that box is ~$9.5–10K — *above* the $5K target. The $5K tier's realistic top end is **70B dense, full-context 32B, and ≤120B MoE.**

---

## 1. Workstation-tier hardware-envelope table

Decode = single-stream generation tok/s. All tok/s rows are **[REPORTED — not demonstrated by us]**. Prices are mid-2026 street, USD, configured at/near the $5K ceiling.

| Box | ~Price | Memory (GB + type) | **Bandwidth GB/s** | Newly unlocked vs 24 GB tier | Reported decode tok/s — **dense 32B** | Reported decode tok/s — **MoE 30B-A3B** | Engine | Flag | Grade |
|---|---|---|---|---|---|---|---|---|---|
| **NVIDIA DGX Spark (GB10)** / ASUS Ascent GX10 | **~$3,000–4,000** (GX10 ~$3K; NVIDIA Spark ~$3,999) | **128 GB** unified LPDDR5X | **~273** | 70B dense (FP8/Q4), ≤120B MoE, full-ctx 32B | **very slow — 70B FP8 ~2.7; 32B-class dense ≈ single-digit→low-teens (bandwidth-bound)** | **fast: 30B-A3B in the tens of tok/s; batched throughput high (≈120× single-stream at concurrency)** | SGLang / Ollama / TensorRT-LLM | [REPORTED] | [DOC+COMM] |
| **AMD Ryzen AI Max+ 395 "Strix Halo"** (Framework Desktop / mini-PCs) | **~$2,000** (Framework Desktop 128 GB = $1,999) | **128 GB** unified LPDDR5X | ~256 theoretical / **~215 measured** | same capacity envelope as Spark, lower price | **~14–18** (24B dense ~14.3 measured; 32B a bit lower) | **~72–103** (30B-A3B, llama.cpp Vulkan; ~100 t/s widely reported) | llama.cpp (Vulkan/RADV), ROCm | [REPORTED] | [COMM] |
| **Apple Mac Studio M3 Ultra** (base 96 GB) | **~$3,999** (96 GB); **~$5,500 @ 256 GB**; **~$9.5–10K @ 512 GB** | 96 / 256 / **512 GB** unified | **~800** | 70B dense (96 GB), full-ctx 32B; 480B MoE only at 512 GB | **~24 (Q4 reported low end) up to ~68 (Q4, short ctx); ~42 @ Q8** | **~72–80+ (MLX 4–8 bit); batched ~2,320 agg** | MLX / llama.cpp | [REPORTED] | [DOC+COMM] |
| **2× RTX 5090** (consumer multi-GPU) | **~$4,500–5,500** (5090 street ~$2,200–2,900 ea + host) | **2×32 = 64 GB** GDDR7 | **~1,790 per card** | 70B Q4 across 2 cards (capacity), full-ctx 32B on one card | **~61 (single 5090, 32B Q4, 4K ctx)** — TP across 2 cards **does not speed single-stream (PCIe, no NVLink); 2× can be *slower* 1×** | **fast (small active set); single-card comfortably ≥100** | vLLM / llama.cpp | [REPORTED] | [COMM] |
| **1× RTX PRO 6000 Blackwell (96 GB)** | **~$8,000–9,000** (*above $5K — contrast point*) | **96 GB** GDDR7 | **~1,790** | 70B FP8/INT4 on ONE card, full-ctx 32B, ≤120B MoE, real concurrency | **high single-stream + huge batched (~3,140 agg @ 30B AWQ-class)** | **very fast** | vLLM / SGLang | [REPORTED] | [DOC+COMM] |
| **1× RTX 6000 Ada (48 GB)** | ~$5,000–6,500 (street, falling) | 48 GB GDDR6 | ~960 | 70B Q4 (tight), full-ctx 32B, comfortable concurrency | **~30–45 (32B Q4, bandwidth ≈ 3090-class)** | fast | vLLM / llama.cpp | [REPORTED] | [COMM] |

> Cross-tier anchor (from W4): **used RTX 3090, 24 GB, ~936 GB/s** decodes **32B dense Q4 ~30 tok/s** (inferred from 4090 ~34 and bandwidth ratio) and MoE-30B-A3B fast — at **~$700–900**.

**Multi-GPU caveat (W5's mechanism, noted not specified):** on consumer Blackwell, tensor-parallel across 2× 5090 runs over **PCIe (no NVLink)**; community benchmarks report dual-GPU **under-performing single-GPU** on single-stream and only winning via **replica parallelism** (independent model copies serving concurrent requests). So 2× 5090 buys **capacity (64 GB) + concurrency**, not faster single-stream dense decode. Distribution mechanism handed to W5.

---

## 2. Capacity-vs-bandwidth verdict

**The inversion, stated plainly:** the DGX Spark (~273 GB/s) and Strix Halo (~215 GB/s measured) have **roughly one-quarter to one-third the memory bandwidth of a used RTX 3090** (~936 GB/s). They can *hold* a 70B dense model the 3090 cannot — and will **decode that dense model slower than the 3090 would** on a per-token basis. **Capacity went up; dense decode speed went down.** A 70B FP8 on Spark is ~2.7 tok/s [REPORTED] — below any plausible interactive comfort floor; it is a "can it load" demo, not a working coding model. These boxes are **MoE-and-long-context machines**, where bandwidth-per-active-param is favorable (30B-A3B hits ~72–103 tok/s on Strix Halo, in the tens on Spark).

**Which box wins, by objective:**

- **(a) Best coding quality at usable speed [the PRIMARY optimization].** Among $5K boxes: **Mac Studio M3 Ultra (96 GB, ~$3,999)** for dense, on bandwidth (~800 GB/s gives 32B Q4 ~24–68 tok/s [REPORTED]); or **Strix Halo / Spark running an MoE coder (30B-A3B / Qwen3-Coder-30B-A3B)** at ~72–100 tok/s. **But note:** a single 32 GB **RTX 5090 (~$2.2–2.9K)** decodes 32B dense Q4 ~61 tok/s [REPORTED] — *faster than the Mac and far faster than the unified appliances* — and a used **3090 at ~$800 already does the 32B-dense job at ~30 tok/s.** The high-bandwidth GPU path wins dense tok/s decisively; the unified appliances only win if you commit to MoE.
- **(b) Max capacity / future-proofing.** **Mac Studio M3 Ultra** — uniquely scales to 512 GB (the only $-near option that can hold a ~480B MoE), and 800 GB/s makes that capacity usable. At $5K (256 GB) it future-proofs without the dense-decode penalty of Spark/Strix. Spark/Strix give 128 GB cheaply but the bandwidth ceiling caps what that capacity is good for (MoE/experimentation).
- **(c) Best $/performance.** For **dense coding tok/s per dollar: a single RTX 5090** (~$2.2–2.9K, ~1,790 GB/s, 32B Q4 ~61 tok/s) — and the **used RTX 3090 remains the absolute value floor** (32B Q4 fits, ~30 tok/s, ~$800). For **MoE coding tok/s per dollar: Strix Halo / Framework Desktop** ($1,999 for 128 GB, ~100 tok/s on 30B-A3B) is the standout — but only if the workstream commits to MoE coders.

---

## 3. Recommendation for the $5K tier (directional — POC must measure)

**Leading box at the $5K ceiling, primary-objective (best coding quality at usable speed): a single RTX 5090 (32 GB) workstation (~$3–3.5K built), running Qwen2.5-Coder-32B Q4 dense (~61 tok/s [REPORTED]) or Qwen3-Coder-30B-A3B MoE.** It has the highest bandwidth of any box at/under $5K, runs the strongest 32B dense coder at the highest single-stream tok/s in the survey, and leaves budget headroom. If >32B (70B-class dense) proves *necessary*, the answer changes to **Mac Studio M3 Ultra 256 GB (~$5.5K)** for capacity+bandwidth balance, or accept the unified-appliance MoE path.

**Is stepping up from the 3090 worth it for an agentic coding loop? Directional answer: NO, not by default.** The minimum tier (used 3090, 24 GB, ~$800) already:
- Fits the strongest dense coder in the W2 shortlist (Qwen2.5-Coder-32B Q4, ~30 tok/s [REPORTED]) and the MoE coders comfortably.
- Has **higher memory bandwidth than the $3–4K unified appliances** (Spark/Strix), so it decodes *dense* models faster than they do despite being a tenth the price.

**The $5K tier earns its cost only under specific, measurable conditions:**
1. **A >32B (70B-class) dense model proves necessary** for coding quality — i.e., a measured shd-005 run shows 32B-class is insufficient. Then capacity (Mac 256 GB, RTX PRO 6000, 48 GB Ada) becomes mandatory. **Unproven that 70B is needed** — current evidence (W2) puts strong coding capability at the 32B-dense / 30B-A3B-MoE tier, which the minimum tier already serves.
2. **Long-context agentic loops** where the 24 GB card's KV cache runs out — the extra capacity buys context headroom the 3090 cannot.
3. **Throughput/concurrency** matters (multiple concurrent agents) — high-bandwidth GPUs (5090/PRO 6000) with vLLM batching, *not* the unified appliances.

**Plainly: buy capacity for capacity reasons (a >32B model is proven needed, or long context, or concurrency); buy the $5K tier for dense tok/s only via a high-bandwidth GPU (5090 / PRO 6000), never via the unified appliances.** The unified-memory appliances (Spark, Strix Halo) are an MoE-and-experimentation play whose dense-decode speed is *worse* than the minimum tier — counterintuitive given their price, and the single most decision-relevant finding of this extension. The POC (shd-005) must measure (a) whether 32B-class suffices for our loop, and (b) actual dense **and** MoE decode + prefill on the candidate box before any purchase.

---

## 4. Citations (grouped by box)

**NVIDIA DGX Spark / GB10 (273 GB/s):**
- https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark/ (in-depth review: 273 GB/s bottleneck; Llama 70B FP8 ~2.7 tps decode SGLang; 8B ~20.5 tps; "shines on smaller models + batching")
- https://dendro-logic.com/engineering/nvidia-dgx-spark-concurrency-benchmark/ (~120× throughput at concurrency 256 vs single-stream)
- https://brandonrc.github.io/benchmark-spark/ (TensorRT-LLM benchmarking)
- https://github.com/rossingram/Spark-DGX-Benchmark (memory bandwidth + LLM throughput, unified memory behavior)
- https://github.com/casualcomputer/rtx_pro_6000_vs_dgx_spark (SGLang: RTX PRO 6000 vs DGX Spark)
- https://forums.developer.nvidia.com/t/should-i-buy-asus-gx10-instead-nvidia-dgx-spark/347717 (GX10 ~$1K cheaper than Spark)
- https://www.newegg.com/asus-ascent-gx10-mini-pc/p/N82E16859110044 (ASUS Ascent GX10 / DGX Spark, 128 GB LPDDR5X pricing)

**AMD Ryzen AI Max+ 395 "Strix Halo" (~256 GB/s theoretical, ~215 measured):**
- https://forum.level1techs.com/t/strix-halo-ryzen-ai-max-395-llm-benchmark-results/233796 (Mistral 24B dense ~14.3 tok/s; Qwen3-30B-A3B ~72 tok/s; ~215 GB/s measured; "MoE is where these APUs shine")
- https://github.com/hogeheer499-commits/strix-halo-guide (llama.cpp Vulkan/RADV: ~100 t/s 30B Qwen; 120B GGUF runs)
- https://community.frame.work/t/amd-strix-halo-ryzen-ai-max-395-gpu-llm-performance-tests/72521 (Framework Desktop GPU LLM tests)
- https://zenvanriel.com/ai-engineer-blog/strix-halo-local-ai-workstation-real-world-test/ (real-world: 32B dense high-teens tok/s)
- https://localaimaster.com/blog/strix-halo-ai-max-395-guide (Qwen3-30B-A3B ~103 t/s; Qwen3-Coder ~96–97 t/s)
- https://www.tweaktown.com/news/103516/ (Framework Desktop 128 GB = $1,999)
- https://frame.work/desktop (Framework Desktop config/pricing)

**Apple Mac Studio M3 Ultra (~800 GB/s, up to 512 GB):**
- https://github.com/ml-explore/mlx/discussions/3209 (systematic: 32B F16 ~23–24 t/s, Q8 ~42, Q4 ~68 @1–4K ctx; KV dominates bandwidth at long ctx)
- https://www.macstories.net/notes/notes-on-early-mac-studio-ai-benchmarks-with-qwen3-235b-a22b-and-qwen2-5-vl-72b/ (large-MoE/70B-class on 512 GB)
- https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide (M3 Ultra 512 GB fastest Mac; 80+ t/s on 35B-A3B MLX 8-bit)
- https://www.markus-schall.de/en/2025/11/apple-mlx-vs-nvidia-how-local-ki-inference-works-on-the-mac/ (M3 Ultra vs RTX 5090 efficiency framing)
- https://llmcheck.net/benchmarks (real tok/s by chip/model/quant)
- https://www.apple.com/shop/buy-mac/mac-studio (M3 Ultra 96 GB = $3,999; 256/512 GB step-up pricing → ~$5.5K / ~$9.5–10K)
- https://prices.appleinsider.com/mac-studio-2025 (M3 Ultra street pricing)

**RTX 5090 (32 GB, ~1.79 TB/s) and multi-GPU:**
- https://www.hardware-corner.net/rtx-5090-llm-benchmarks/ (Qwen3 32B dense ~61 t/s @4K ctx; ~10K t/s prompt; 139K ctx)
- https://www.cloudrift.ai/blog/benchmarking-gpu-servers-for-llm-inference (4090 vs 5090 vs PRO 6000; 2× 5090 underperforms 1× on single-stream; PCIe TP fails; replica parallelism scales)
- https://www.spheron.network/blog/rent-nvidia-rtx-5090/ (RTX 5090 cost-per-token benchmarks)
- https://arxiv.org/html/2601.09527v1 (consumer Blackwell inference practical guide)
- https://bestvaluegpu.com/history/new-and-used-rtx-5090-price-history-and-specs/ (5090 street price tracker, mid-2026)

**RTX PRO 6000 Blackwell (96 GB) / RTX 6000 Ada (48 GB) — contrast points:**
- https://www.spheron.network/blog/rent-nvidia-rtx-pro-6000/ (30B AWQ ~8,400 agg t/s; 70B FP8 fits w/ KV headroom; cost-per-token)
- https://www.cloudrift.ai/blog/benchmarking-rtx6000-vs-datacenter-gpus (PRO 6000 ~3,140 agg t/s, beats H100 SXM single-GPU)
- https://www.storagereview.com/review/nvidia-rtx-pro-6000-workstation-gpu-review-blackwell-architecture-and-96-gb-for-pro-workflows (96 GB GDDR7, 1.792 TB/s, NVFP4)
- https://www.yottalabs.ai/post/which-nvidia-rtx-6000-gpu-is-right-for-you-in-2026 (Ada 48 GB / 960 GB/s vs PRO 6000 96 GB / 1.79 TB/s; pricing)
- https://www.bestgpusforai.com/gpu-comparison/rtx-6000-pro-vs-6000-ada (VRAM/bandwidth/tensor-core comparison)

**Cross-tier baseline (from W4):** RTX 3090 ~936 GB/s — see findings-W4.md citations (corelab.tech/llmgpu, awesomeagents.ai home-GPU leaderboard).

---

## Flags / what to carry forward

- **Firewall:** zero figures demonstrated by us; all **[REPORTED]**. tok/s measurement is **shd-005**. The "is 70B worth it" completion question is explicitly NOT answered here.
- **The inversion is the headline:** Spark (273) and Strix Halo (~215) have **lower bandwidth than a used 3090 (936)** — they unlock big-model *capacity* but **decode dense models slower** than the minimum tier. MoE + long-context is where they win; high-bandwidth GPU (5090 / PRO 6000) is where dense tok/s wins.
- **Directional recommendation:** stepping up from the 3090 is **not worth it by default** — the minimum tier already serves the 32B-dense / 30B-A3B-MoE coding tier at higher dense bandwidth than the unified appliances. The $5K tier matters **only if a >32B dense model proves necessary, or for long context, or for concurrency** — and even then, dense speed comes from a GPU (5090/PRO 6000/Mac), never from Spark/Strix.
- **Ceiling note:** Qwen3-Coder-480B-class MoE (~270 GB Q4) is **out** of the $5K tier; only the 512 GB Mac Studio (~$9.5–10K, above ceiling) holds it.
- **W5 hand-off:** consumer multi-GPU distribution (2× 5090 over PCIe, no NVLink; tensor-parallel fails single-stream, replica parallelism works) — capacity/concurrency unlock noted, mechanism not specified here.
- **Unverified gaps:** clean 32B-*dense* decode on Spark not isolated (inferred sub-teens from bandwidth + the 70B 2.7 t/s anchor); exact Qwen2.5-Coder-32B numbers on Strix Halo (24B dense ~14.3 used as proxy); Mac M3 Ultra dense 32B spread is wide across quant/ctx (24→68 t/s) — flagged in-line, do not promote to firm numbers.
