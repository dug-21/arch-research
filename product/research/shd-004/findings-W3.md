# shd-004 — W3: Quantization / format tradeoffs

**Workstream:** W3 — Quant/format tradeoffs (C1 — capable LLM inference on local hardware, #4)
**Confidence:** directional · read-only desk research · **nothing demonstrated by us**
**Date:** 2026-06-24

> Question: Map the local-inference quant/format landscape on the three axes that decide a stack —
> accuracy degradation vs throughput vs VRAM/RAM footprint — and which engines consume which format.
> Name the determining constraint per format.

**Evidence grading:** `[DOC]` = vendor/official docs or original paper · `[COMM]` = community benchmark /
perplexity table (reproducible methodology, but not a controlled lab) · `[REPORT]` = blog/aggregator
secondary claim. **All accuracy/throughput numbers below are *reported*, not proven-by-us** — perplexity
deltas are measurement-sensitive (dataset, context length, imatrix quality) and vary by model.

---

## 1. Quant-format tradeoff matrix

| Format | Typical bpw | Accuracy vs fp16 (reported) | Throughput characteristic | Footprint rule-of-thumb | Engines that consume it | Determining constraint | Grade |
|---|---|---|---|---|---|---|---|
| **GGUF Q8_0** | ~8.5 | ~lossless (PPL Δ ≈ 0.00–0.01) | CPU/GPU/hybrid; mem-bandwidth bound on CPU | ~1.06 GB/B params | llama.cpp, Ollama, LM Studio, KoboldCpp | Footprint (8-bit pays full freight for ~zero quality gain over Q6) | [COMM][DOC] |
| **GGUF Q6_K** | ~6.6 | "almost lossless" (PPL Δ ≈ 0.01–0.03) | same as above | ~0.82 GB/B | llama.cpp, Ollama, LM Studio | Footprint; default when VRAM allows | [COMM] |
| **GGUF Q5_K_M** | ~5.7 | excellent; near-imperceptible (PPL Δ ≈ 0.03–0.06) | same | ~0.71 GB/B | llama.cpp, Ollama, LM Studio | Balance point above the Q4 cliff | [COMM] |
| **GGUF Q4_K_M** | ~4.8 | small penalty; **sweet spot** (PPL Δ ≈ 0.05 over Q8 on 7B; ~6.01 vs 5.96 fp16) | same; ~73% compression | ~0.60 GB/B | llama.cpp, Ollama, LM Studio | **The reference 4-bit CPU/hybrid quant** | [COMM][DOC] |
| **GGUF Q3_K_M / Q2_K** | ~3.9 / ~2.6 | visible degradation; Q2_K notably lossy | same | ~0.49 / ~0.33 GB/B | llama.cpp, Ollama, LM Studio | Accuracy — fit-of-last-resort | [COMM] |
| **GGUF IQ-quants** (IQ2_XXS…IQ4_XS) | 2.06–4.46 | quality-per-byte leader at low bpw **iff good imatrix**; IQ4_XS ≈ Q4_K_M at ~0.43 GB less | slightly faster gen, slower prompt-proc than K-quant (LUT-based) | IQ4_XS ~0.52 GB/B | llama.cpp, Ollama, LM Studio | **imatrix dependency** (IQ1–IQ3 *require* a calibration imatrix; bad imatrix → bad quant) | [DOC][COMM] |
| **AWQ** (INT4, W4A16) | ~4.25 (+scales) | activation-aware; best-in-class 4-bit task accuracy. Reported ~1–3% higher MMLU/HumanEval than GPTQ at same width (e.g. HumanEval 51.8 vs 46) | Marlin-AWQ kernels ~741 tok/s, ITL ~12.6ms (reported); fastest INT4 on vLLM/SGLang | ~0.55 GB/B + scales | **vLLM, SGLang, TGI**, ExLlamaV2, AutoAWQ | **GPU-only**; needs Ampere+ for Marlin path; calibration set | [DOC][COMM] |
| **GPTQ** (INT4, W4A16) | ~4.25 (+scales) | layer-wise 2nd-order; slightly behind AWQ at 4-bit; good with act-order/group128 | strong with Marlin kernels; mature | ~0.55 GB/B + scales | vLLM, SGLang, TGI, ExLlamaV2, AutoGPTQ | GPU-only; act-order/group-size config sensitivity | [DOC][COMM] |
| **FP8** (W8A8, E4M3) | 8 | "negligible" loss on most models (no calibration needed for dynamic) | **+1.6x mem reduction, up to ~1.25–1.6x throughput** vs fp16; gap widens at high batch | ~1.0 GB/B | **vLLM, TGI**, TensorRT-LLM, SGLang | **Hardware: needs CC ≥ 8.9 (Ada/Hopper)**. Ada has FP8 ops but *no* hardware scaling — TE falls back to BF16 silently; true FP8 tensor-core gain is Hopper (H100/H200) | [DOC] |
| **EXL2** (variable bpw) | target 2.0–8.0 (commonly 4.0/4.65/5.0/6.0) | variable per-layer bit allocation; at 4.65 bpw beats uniform 4-bit on PPL (reported ~4.32 vs 4.33–4.34); ≥ Q4_K_M at equal VRAM | **fastest single-GPU**: ~40–70% faster gen than llama.cpp for models fully in VRAM (reported) | ~bpw/8 GB/B (tunable to fit VRAM exactly) | **ExLlamaV2, TabbyAPI** (and ExLlamaV3) | **GPU-VRAM-only** (no CPU offload); must fit entirely in VRAM | [COMM][DOC] |
| **MLX quant** (4-bit/8-bit, group-wise) | 4 / 8 (group size 32–64) | 4-bit retains ~97.3% of fp16 MMLU (reported, vllm-mlx); group ≤32 minimizes loss; uniform 4-bit weak on hard reasoning (GSM8K) unless mixed-precision | unified-memory; M-series GPU/Neural-Accelerator; M5 adds matmul accelerators | ~0.55 GB/B (4-bit) on shared RAM | **MLX / mlx-lm, LM Studio (MLX backend)** | **Apple Silicon only**; tied to unified memory ceiling | [DOC][COMM] |
| **bitsandbytes NF4** | ~4.1 | QLoRA-era 4-bit; info-theoretic optimal for normal weights; quant-type has little inference impact | slower than Marlin/AWQ kernels; primarily a training/QLoRA format | ~0.53 GB/B | transformers, vLLM (bnb), QLoRA pipelines | Inference-throughput (not a speed-optimized serving format) | [DOC] |
| **bitsandbytes INT8** (LLM.int8) | 8 | preserves outlier columns in fp16 → "no significant degradation" | mixed-precision decomposition adds overhead; slower than FP8 | ~1.0 GB/B | transformers, vLLM (bnb) | Throughput overhead from outlier handling; superseded by FP8 on Ada/Hopper | [DOC] |

---

## 2. "Sweet spot" callout

**Single 24GB-class NVIDIA GPU (RTX 4090 / 3090 / A5000), coding-grade model, fully in VRAM:**
The reported best accuracy/footprint tradeoff is **EXL2 at ~4.65–5.0 bpw** (ExLlamaV2/TabbyAPI) when raw
single-stream speed and tightest accuracy-per-VRAM matter — variable per-layer allocation lets you tune
to fill 24GB exactly and it reportedly beats uniform 4-bit on perplexity and beats llama.cpp on
tok/s for in-VRAM models. **For a serving/concurrency profile** (batched, OpenAI-compatible), **AWQ INT4
(W4A16) on vLLM/SGLang** is the reported pick — activation-aware 4-bit gives the best task accuracy
among INT4 formats with the fastest batched throughput via Marlin kernels. If the workload is hybrid
CPU/GPU or portability matters, **GGUF Q4_K_M → Q5_K_M** (llama.cpp/Ollama) is the robust default.
Rule of thumb: a ~32B coding model at 4–5 bpw lands ~18–22 GB weights, leaving thin KV headroom on 24GB
(see §3) — the determining constraint at 24GB is usually **KV-cache + context length, not weights**.

**Apple-Silicon equivalent:** **MLX 4-bit (group size 32–64)** via mlx-lm / LM Studio MLX backend — the
native unified-memory path; for hard-reasoning/coding tasks prefer **MLX 5–8-bit or mixed-precision**
since uniform 4-bit reportedly drops sharply on GSM8K-style tasks. GGUF Q4_K_M/Q5_K_M on llama.cpp Metal
is the portable fallback on the same hardware. Determining constraint on Mac: **unified-memory ceiling**
(weights + KV + OS share one pool), not a discrete VRAM wall.

---

## 3. Footprint rule-of-thumb (for W4/W6 fit reasoning)

**Weights:** `weight_GB ≈ (params_B × 1e9 × bpw / 8) / 1e9 = params_B × bpw / 8`
- Quick table per 1B params: 4-bit ≈ **0.5 GB**, 4.8 bpw (Q4_K_M) ≈ **0.60 GB**, 5.7 (Q5_K_M) ≈ **0.71**, 6.6 (Q6_K) ≈ **0.82**, 8-bit/FP8 ≈ **1.0**, fp16 ≈ **2.0**.
- Add ~3–8% for quant scales/zero-points (AWQ/GPTQ/EXL2) and embeddings/output head kept at higher precision.

**KV-cache (the second, often-binding term):**
`KV_bytes ≈ 2 × n_layers × n_kv_heads × head_dim × seq_len × batch × bytes_per_elem`
- The `2` = K and V. `bytes_per_elem` = 2 (fp16/bf16 KV), **1 (FP8 KV-cache → halves it)**.
- GQA collapses `n_kv_heads` well below `n_heads` — the main KV saver on modern models.
- Per-token shortcut: `≈ 2 × n_layers × hidden_size × bytes_per_elem` (no-GQA upper bound). For a
  32-layer/4096-hidden model at fp16 that's ~0.5 MB/token → **~2 GB per 4K-context sequence**.

**Total fit:** `VRAM_needed ≈ weight_GB + KV_GB(context × batch) + ~1–2 GB runtime/activation overhead`.
On a 24GB card with a 32B model at ~4.5 bpw (~18 GB weights), only ~4–5 GB remains for KV → context/
batch is the binding constraint; FP8 KV-cache or shorter context is the lever. **On Apple Silicon use the
same formula against total unified RAM minus OS/headroom (~reserve 4–8 GB).**

---

## 4. Citations (grouped by format)

**GGUF k-quants / IQ-quants (llama.cpp / Ollama / LM Studio):**
- https://arxiv.org/html/2601.14277v1 — "Which Quantization Should I Use? Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B" (bpw + PPL table)
- https://deepwiki.com/ggml-org/llama.cpp/7.3-quantization-techniques — k-quant/IQ types, bpw
- https://deepwiki.com/qualcomm/llama.cpp/5.2-quantization-pipeline-and-imatrix — imatrix pipeline
- https://kaitchup.substack.com/p/choosing-a-gguf-model-k-quants-i — K vs IQ vs legacy, when imatrix needed
- https://runaihome.com/blog/quantization-q4-q5-q6-q8-quality-loss-2026/ — Q4/Q5/Q6/Q8 quality-loss numbers
- https://vucense.com/dev-corner/gguf-quantization-explained-q4-k-m-vs-q8-0-vs-f16-2026/

**AWQ / GPTQ (vLLM / SGLang / TGI / ExLlama):**
- AWQ paper — Lin et al., "AWQ: Activation-aware Weight Quantization for LLM Compression," https://arxiv.org/abs/2306.00978
- GPTQ paper — Frantar et al., "GPTQ: Accurate Post-Training Quantization for GPT," https://arxiv.org/abs/2210.17323
- https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks — Marlin-AWQ throughput/ITL
- https://aws.amazon.com/blogs/machine-learning/accelerating-llm-inference-with-post-training-weight-and-activation-using-awq-and-gptq-on-amazon-sagemaker-ai/
- https://theaiengineer.substack.com/p/quantization-in-practice-gptq-vs — AWQ vs GPTQ task-accuracy deltas

**FP8 (vLLM / TGI / Hopper-Ada):**
- https://docs.vllm.ai/en/latest/features/quantization/fp8/ — vLLM FP8 W8A8, CC≥8.9 requirement
- https://developers.redhat.com/articles/2024/07/15/vllm-brings-fp8-inference-open-source-community
- https://www.spheron.network/blog/fp8-quantization-inference-performance-hardware-explained/ — Ada-vs-Hopper FP8 scaling caveat, throughput gains

**EXL2 (ExLlamaV2 / TabbyAPI):**
- https://github.com/turboderp-org/exllamav2 — EXL2 variable-bpw format (repo)
- https://insiderllm.com/guides/model-formats-explained-gguf-gptq-awq-exl2/ — EXL2 4.65 bpw PPL vs uniform 4-bit
- https://vife.ai/blog/supercharging-local-llms-exllamav2-guide — speed vs llama.cpp (in-VRAM)
- https://www.hardware-corner.net/quantization-local-llms-formats/

**MLX (Apple Silicon):**
- https://machinelearning.apple.com/research/exploring-llms-mlx-m5 — Apple MLX, M5 accelerators
- https://arxiv.org/pdf/2508.08531 — "Profiling LLM Inference on Apple Silicon: A Quantization Perspective"
- https://contracollective.com/blog/gguf-vs-mlx-quantization-formats-apple-silicon-2026 — GGUF vs MLX on Apple
- https://mlx-optiq.com/docs/faq — mixed-precision MLX, group-size/GSM8K accuracy notes

**bitsandbytes NF4 / INT8:**
- https://huggingface.co/docs/transformers/quantization/bitsandbytes — NF4 / LLM.int8() docs
- https://huggingface.co/blog/4bit-transformers-bitsandbytes — QLoRA NF4, inference impact

**KV-cache / footprint formula:**
- https://lyceum.technology/magazine/kv-cache-memory-calculation-llm/ — GQA KV formula
- https://dev.to/jagmarques/kv-cache-memory-calculator-how-much-does-your-llm-actually-use-85n

---

## Flags / what I could not verify (firewall)

- **Every accuracy delta and tok/s figure is reported by docs/community, not demonstrated by us.** PPL deltas are dataset- and imatrix-sensitive; the AWQ>GPTQ and EXL2>Q4_K_M orderings are reproducible community claims, **not** a controlled benchmark we ran. Treat the §2 "sweet spot" as directional until a POC measures it on the actual target model.
- **EXL2 / EXL3 perplexity numbers** are largely single-author community tables; the 40–70% speed-vs-llama.cpp claim is workload- and context-length-dependent.
- **FP8-on-Ada** is the sharpest hardware trap: docs say CC≥8.9 *compiles*, but the "silent BF16 fallback / no hardware scaling on Ada" claim is from a secondary source — **W6 should verify on the exact target GPU** before assuming FP8 throughput gains on anything below Hopper.
- bpw→GB constants are nominal; real on-disk/in-VRAM size includes higher-precision embeddings/output head and scales (~3–8% over the raw formula).
- **Cross-ref to W1 (engines):** GGUF→llama.cpp/Ollama/LM Studio; AWQ+GPTQ+FP8→vLLM/SGLang/TGI; EXL2→ExLlamaV2/TabbyAPI; MLX→mlx-lm/LM Studio. No single engine consumes all formats — **format choice constrains engine choice and vice-versa** (the key W1×W3 coupling).
