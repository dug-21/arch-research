# shd-004 — W2: Coding-grade open model survey

**Workstream:** W2 — Coding-grade open-weight model survey (C1 — capable LLM inference on local hardware · N2 offline/no-gating)
**Confidence:** directional · read-only desk research · **nothing demonstrated by us**
**Date:** 2026-06-24

> Question: Which open-weight code models plausibly fit owned/budget hardware (not datacenter), and at what coding tier? Separate doc-claim from benchmark-reported; flag weight-gating that blocks fully-offline use.

**Evidence grading:** `[DOC]` = vendor/card claim only · `[BENCH]` = a specific benchmark number is reported (by vendor or third-party leaderboard — still *reported*, not proven-by-us) · `[BENCH*]` = number contested/multiple conflicting reports. The firewall holds: **no reported benchmark is `proven`**; reproduction by us is a later POC, never settled here.

---

## 1. Model shortlist table

| Model | Sizes | Active params (MoE) | Coding tier — doc-claim vs benchmark-reported | License / gating | Evidence grade |
|---|---|---|---|---|---|
| **Qwen2.5-Coder** | 0.5B · 1.5B · 3B · 7B · 14B · **32B** | dense | 32B-Instruct: **HumanEval 92.7, MBPP 90.2, Aider 73.7** (vendor) — "SOTA open, matches GPT-4o" [BENCH]. Smaller sizes degrade smoothly (3B-Instruct ~45–84 HumanEval depending on harness — contested) [BENCH*] | **Apache-2.0** for 0.5/1.5/7/14/32B; **3B = Qwen-Research (non-commercial)**. Ungated download. Flag: the 3B carve-out only. | High (32B), Med (small) |
| **Qwen3-Coder-30B-A3B** ("Flash") | 30.5B total | **~3.3B active** (128 experts, 8 active) | Agentic-grade. **SWE-bench Verified ~51% (vendor repro) / up to ~72 in some reports** [BENCH*]; 256K ctx (→1M YaRN). Native tool-use/function-call format | **Apache-2.0**, ungated | High structure, Med (SWE# contested) |
| **Qwen3-Coder-480B-A35B** | 480B total | 35B active | Frontier-open. **SWE-bench Verified 69.6, Aider-Polyglot 61.8** (vendor) — "rivals Sonnet-4 / GPT-4.1" [BENCH]. **Datacenter-only** — listed as ceiling reference, not an owned-HW fit | **Apache-2.0**, ungated | High |
| **DeepSeek-Coder-V2-Lite** | 16B total | **2.4B active** (MoE) | **HumanEval 81.1** (reported); 338 languages, strong for its active-param cost [BENCH] | **DeepSeek Model License** — permits commercial use; ungated download. (Custom license, not OSI — read clauses) | High |
| **DeepSeek-Coder (v1)** | 1.3B · 6.7B · 33B | dense | 33B was a 2024 reference point (HumanEval ~79); now superseded by V2-Lite/Qwen | DeepSeek Model License | Med (dated) |
| **Codestral 22B** (v1) | 22B | dense | HumanEval pass@1 reported strong (~81); good FIM/fill-in-middle | **Mistral AI Non-Production License (MNPL) — non-commercial**. *Blocks commercial offline use* | High (license), Med (bench) |
| **Codestral-Mamba 7B** | 7B | dense (Mamba2 SSM) | **HumanEval 75.0** (vendor), beats CodeGemma-7B/CodeLlama-34B; linear-time long context | **Apache-2.0**, ungated | High |
| **Devstral Small 2** | 24B | dense | Agentic specialist. **SWE-bench Verified 68.0** (vendor) — "strongest open-weight at its size, outscores 70B-class"; 256K ctx; built for repo-scale multi-file edits [BENCH] | **Apache-2.0**, ungated | High |
| **Llama-3.3-70B-Instruct** | 70B | dense | **HumanEval 88.4** (reported); general model, decent code [BENCH] | **Llama 3.3 Community License** — gated (acceptance/registration on HF), MAU clause. *Gating + redistribution friction for offline caching* | High |
| **Llama-3.1-70B / 8B** | 8B · 70B · 405B | dense | 70B HumanEval 80.5 [BENCH]; 8B weak-ish for agentic code | Llama Community License (gated) | High |
| **StarCoder2** | 3B · 7B · **15B** | dense | 15B = best-in-class *base* code model at release (HumanEval/MBPP/EvalPlus); weaker on code-fix/explain variants; mostly a **completion/base** model, not instruct-agentic [BENCH] | **BigCode OpenRAIL-M** (open, with use restrictions — not pure Apache) | Med |
| **CodeGemma 7B / 2B** | 2B · 7B | dense | 7B beats most 7B peers except DeepSeek-Coder-7B on HumanEval; good FIM [BENCH]; weaker on fix/explain | **Gemma license** (open, custom terms, ungated) | Med |
| **Granite-Code (IBM)** | 3B · 8B · 20B · 34B | dense | Best avg at 7–8B *base* scale (per IBM paper); strong HumanEvalPack code-fix vs CodeGemma [BENCH] | **Apache-2.0**, ungated | Med |
| **Yi-Coder 9B / 1.5B** | 1.5B · 9B | dense | **HumanEval 85.4** (reported) "≈ DeepSeek-Coder-33B at fraction of size"; 128K ctx [BENCH] | **Apache-2.0**, ungated | Med |
| **GLM-4.x / GLM-5.x (Z.AI)** | large MoE (e.g. 753B/40B-active class) | MoE | Top agentic-coding open leaderboards in 2026 (GLM-5.2 reported leading agentic-coding avg) [BENCH] — but **flagship sizes are datacenter-only**; smaller GLM variants exist but are the weaker tier | Open-weight (MIT-style on several releases — verify per release) | Low/Med (sizing) |

---

## 2. What fits owned HW (qualitative — W4 owns the precise envelope)

Flagging the obvious only; W4 sets the real VRAM/quant envelope:

- **Single 24GB-class GPU (RTX 3090/4090):** comfortable home for **7B–14B dense** at good quant (Qwen2.5-Coder-7B/14B, Codestral-Mamba-7B, Yi-Coder-9B, CodeGemma-7B, Granite-8B). **32B dense** (Qwen2.5-Coder-32B) fits only at aggressive 4-bit quant and tight context — borderline. **Devstral Small 24B** is explicitly pitched at one RTX 4090 / 32GB Mac.
- **Apple Silicon (32–64GB unified):** opens **24B–32B dense** (Devstral 24B, Qwen2.5-Coder-32B) and the **30B-A3B MoE** comfortably — MoE's ~3.3B active params make Qwen3-Coder-30B-A3B unusually cheap to *run* once loaded (memory-resident but low compute/token).
- **CPU-only / small:** **0.5B–3B** (Qwen2.5-Coder small, StarCoder2-3B, CodeGemma-2B) for autocomplete/FIM, not agentic loops.
- **Datacenter-only (out of owned-HW scope, kept as ceiling):** Qwen3-Coder-480B, GLM-5.x flagship. Cite for "what we're giving up," not as candidates.

**MoE caveat:** total params drive *memory to load*; active params drive *compute/token*. A 30B-A3B model needs ~30B-worth of memory but runs like a ~3B for throughput — attractive on Apple-Silicon unified memory, less so where VRAM is the hard cap.

---

## 3. Recommended coding-grade shortlist (3–5 strongest for a local coding loop)

1. **Qwen2.5-Coder-32B-Instruct** — highest *reported* coding benchmarks of any owned-HW-feasible model (HumanEval 92.7 / Aider 73.7), Apache-2.0, ungated. The strongest dense single-model bet; fits 24GB only quantized, comfortable on Apple Silicon. **Determining constraint: VRAM at 32B**, which is exactly the W4 question.
2. **Qwen3-Coder-30B-A3B ("Flash")** — purpose-built for *agentic* coding (tool-use, 256K ctx) with only ~3.3B active params → best throughput-per-quality on unified memory. Apache-2.0. The agentic-loop front-runner; the open SWE-bench number is contested (~51–72), so treat tier as "agentic-capable, magnitude unproven-by-us."
3. **Devstral Small 2 (24B)** — Apache-2.0, explicitly engineered for repo-scale multi-file agentic edits, **SWE-bench Verified 68.0** reported, fits one 4090 / 32GB Mac. The cleanest license+size+agentic-fit triple.
4. **DeepSeek-Coder-V2-Lite (16B/2.4B-active)** — strongest coding-per-active-param at the small end (HumanEval 81.1), runs almost anywhere; license is permissive-but-custom (verify clauses for redistribution/caching).
5. **Codestral-Mamba 7B** — Apache-2.0, HumanEval 75.0, linear-time long-context — the lightweight/CPU-friendly wildcard if the loop needs a tiny footprint.

**Firewall note:** every tier above rests on *reported* benchmarks. None is `proven` for our loop. The completion question (does it actually drive our coding harness to a passing diff on owned HW?) is settled only by a later validated POC — not by this survey.

**License watch-list (N2 offline):** avoid as primary if fully-offline *commercial* redistribution/caching matters — **Codestral 22B (MNPL non-commercial)**, **Qwen2.5-Coder-3B (Qwen-Research non-commercial)**, and the **Llama-3.x family (gated acceptance + MAU clause)**. **StarCoder2 (OpenRAIL-M)** and **CodeGemma/Gemma** carry use-restriction clauses (open but not Apache/MIT) — readable, but not "no-strings." The clean-permissive core is **Qwen2.5/3-Coder (Apache, ex-3B), Devstral, Codestral-Mamba, Yi-Coder, Granite-Code**.

---

## 4. Citations (grouped by family)

**Qwen2.5-Coder / Qwen3-Coder**
- https://qwenlm.github.io/blog/qwen2.5-coder-family/ (sizes 0.5–32B; licenses incl. 3B Qwen-Research)
- https://arxiv.org/pdf/2409.12186 (Qwen2.5-Coder Technical Report)
- https://openlaboratory.ai/models/qwen-2_5-coder-32b (HumanEval 92.7 / MBPP 90.2 / Aider 73.7)
- https://qwen.ai/blog?id=qwen3-coder-next ; https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct/discussions/30 (30B-A3B SWE-bench repro, contested)
- https://artificialanalysis.ai/models/qwen3-coder-30b-a3b-instruct (active params, ctx)
- https://llm-stats.com/models/compare/qwen3-30b-a3b-vs-qwen3-coder-480b-a35b-instruct (480B SWE 69.6 / Aider 61.8, Apache-2.0)
- https://unsloth.ai/docs/models/tutorials/qwen3-coder-how-to-run-locally

**DeepSeek-Coder / V2-Lite**
- https://github.com/deepseek-ai/DeepSeek-Coder-V2 ; https://arxiv.org/pdf/2406.11931 (Technical Report)
- https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Lite-Base (16B/2.4B-active)
- https://openlaboratory.com/models/deepseek-coder-v2-lite/ (HumanEval 81.1)

**Codestral / Codestral-Mamba / Devstral (Mistral)**
- https://mistral.ai/news/codestral/ (Codestral 22B, MNPL non-commercial)
- https://www.datacamp.com/tutorial/codestral-mamba ; https://hatchworks.com/blog/gen-ai/codestral-mamba-guide/ (Mamba 7B HumanEval 75.0, Apache-2.0)
- https://mistral.ai/news/devstral-2507/ ; https://mistral.ai/news/devstral-2-vibe-cli/ (Devstral Small 2, SWE-bench 68.0, Apache-2.0, 4090/32GB-Mac)
- https://openrouter.ai/mistralai/devstral-small

**Llama-3.x (Meta)**
- https://ai.meta.com/blog/meta-llama-3-1/ (3.1 70B HumanEval 80.5)
- https://llm-stats.com/models/llama-3.3-70b-instruct ; https://tokenmix.ai/blog/llama-3-3-70b (3.3 70B HumanEval 88.4)
- https://huggingface.co/meta-llama/Llama-3.1-70B (gated/community license)

**StarCoder2 / CodeGemma / Granite-Code / Yi-Coder / GLM**
- https://developer.nvidia.com/blog/unlock-your-llm-coding-potential-with-starcoder2/ (StarCoder2-15B best large base; OpenRAIL-M)
- https://huggingface.co/blog/codegemma ; https://ai.google.dev/gemma/docs/codegemma/model_card (CodeGemma 7B/2B, Gemma license)
- https://arxiv.org/html/2405.04324v1 (Granite-Code, Apache-2.0, code-fix strength)
- https://pinggy.io/blog/best_open_source_self_hosted_llms_for_coding/ (Yi-Coder 9B HumanEval 85.4, Apache-2.0)
- https://www.morphllm.com/best-open-source-coding-model-2026 ; https://codersera.com/blog/open-source-llms-landscape-2026/ (GLM-5.x agentic-coding leaderboard; datacenter sizing)

---

**Flags for curator/leader:**
- **Firewall:** all tiers are *reported* benchmarks; none demonstrated by us. Treat "tier" as structure, not status.
- **Contested number:** Qwen3-Coder-30B-A3B SWE-bench Verified ranges ~51→72 across sources — flag as `[BENCH*]`, do not pin a single figure.
- **License blockers for N2-offline:** Codestral-22B (non-commercial), Qwen2.5-Coder-**3B** (non-commercial carve-out), Llama-3.x (gated + MAU). StarCoder2/CodeGemma/Gemma = open-with-restrictions, not Apache/MIT.
- **Scope boundary:** Qwen3-Coder-480B and GLM-5.x flagships are datacenter-only — included as ceiling references, excluded from owned-HW candidates.
- **Hand-off to W4:** the determining constraint for the top dense pick (Qwen2.5-Coder-32B) is the **24GB VRAM-vs-quant** envelope — W4's precise call.
