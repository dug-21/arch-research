# shd-005 / W1 — Route-decision signals (the trigger / selector)

**Run:** shd-005 · **Capability:** C3 (intelligent multi-LLM routing) · **Workstream:** W1
**Researcher:** shd-005-researcher-W1 · **Date:** 2026-06-26 · **Mode:** read-only, web-only
**NFR lens:** N1 owned-HW/budget · N2 vendor-not-load-bearing · N3 sensitive code stays local (HARD) · N4 multi-machine.

> **Firewall discipline.** Every reliability claim is tagged **[benchmark-reported]** (a paper/repo reports a measured number) or **[doc-claim]** (asserted in docs/blog without an attached benchmark in the source I read). Nothing is *proven* — these rank the landscape and name the determining constraint. A later validated POC settles whether any works on our local stack.
>
> **Unimatrix note (OBS):** the `context_*` MCP was **not connected** this run (`context_search` → "No such tool available"). No prior-art graph read was possible; findings are web-sourced only. Flag for leader/curator.

## The frame the scope under-specified: signals split into THREE timing classes

The workstream lists signals as if all post-generation triggers. They are not — timing class is the dominant axis, because it determines cost and what the local engine must expose:

- **Pre-hoc (route before any generation):** task/difficulty classifiers, context/capability-match heuristics. Cheapest, **no logprobs needed**, but blind to the actual answer.
- **Post-hoc, output-internal (route after the small model answers):** logprob/entropy/perplexity, self-consistency, semantic entropy, verifier/judge, learned scorer. Pays for ≥1 local generation; the "cascade" family.
- **Harness-level (route after the answer is *acted on*):** test/compile/lint failure, tool-call failure, retry exhaustion. Free (you were running tests anyway), highest-signal for code, but slowest.

A real router stacks all three (cheap gate → cascade → harness backstop). Treating them as one undifferentiated "trigger" is the trap.

## Signal catalog

| # | Signal | Timing | What it measures | Reliability (tag · cite) | Latency / cost overhead | Needs model internals? Exposed by local engines? | Harness-observable? |
|---|--------|--------|------------------|--------------------------|--------------------------|---------------------------------------------------|---------------------|
| 1 | **Token log-prob / mean seq log-prob** | post-hoc | Confidence as (mean) log-prob of generated tokens; low ⇒ uncertain | **[doc-claim]** widely used cascade proxy; **raw token confidence miscalibrated & prompt-sensitive** (C1, C12) | ~0 (free byproduct of decode) | **logprobs.** llama.cpp `n_probs`→`top_logprobs` ✅; vLLM `logprobs`/`prompt_logprobs` ✅; Ollama ✅ since **v0.12.11** (native + OpenAI-compat); unsupported until late-2025 (L1,L2,L3) | indirectly (score thresholding) |
| 2 | **Predictive entropy (per-token / first-token)** | post-hoc | Spread of next-token distribution; high ⇒ uncertain | **[doc-claim]** first-token entropy correlates w/ uncertainty; same calibration caveat (C1) | ~0 (needs top-k logprobs) | **logprobs/top-k.** Same exposure as #1 (need `n_probs`/`top_logprobs` ≥ k) | via score |
| 3 | **Perplexity** | post-hoc | exp(−mean log-prob) over sequence | **[doc-claim]** baseline UQ; weaker than semantic methods (C6) | ~0 | **logprobs.** Same as #1 | via score |
| 4 | **Self-consistency / sampling disagreement** | post-hoc | Sample N answers; disagreement/vote-margin ⇒ uncertainty | **[benchmark-reported]** CISC: confidence-weighted vote → same accuracy, far fewer samples (C4); **fails when model is confidently wrong** N× (C5) | **N× generation**; parallelizable | **No internals** — sampled text only. Any engine (call N×, temp>0) | yes |
| 5 | **Semantic entropy** (Farquhar et al., Nature 2024) | post-hoc | Cluster N samples by *meaning*, entropy over clusters | **[benchmark-reported]** beats logprob/perplexity baselines across model sizes (C6) | **5–10× compute** — adoption blocker (C6) | No internals (text + NLI model). **SEP variant needs hidden states** → C7 | yes |
| 5b | **Semantic-entropy probes (SEP)** | post-hoc | Linear probe on **hidden states** approximates semantic entropy from ONE generation | **[benchmark-reported]** cheap approx of #5, single pass (C7) | ~1× (one generation) | **Needs raw hidden states — NOT exposed by llama.cpp/vLLM/Ollama standard APIs.** Hard feasibility/sovereignty caveat (C7) | no |
| 6 | **Cross-model / ensemble agreement** (ABC) | post-hoc | Agreement among ensemble of *small* models; disagree ⇒ escalate | **[benchmark-reported]** ABC training-free; up to 14× comms / 2–25× price-per-token cut; can beat best single model (C8). Complements self-consistency when SC overconfident (C9) | **M× generation**; parallelizable | No internals (compares outputs). Any engine; **fits N4 multi-machine** | yes |
| 7 | **Verifier / judge model (LLM-as-judge, P(True))** | post-hoc | A model scores answer correctness → escalate if low | **[benchmark-reported]** GPT-4 judge ~80% human agreement ≈ human-human; 77–92% domain (C10). **Fragile:** "one token to fool" flips judges (C11) | +1 model call; cheaper if judge small/local | No internals (P(True) variant needs #1 logprob exposure) | yes |
| 8 | **Learned generation-scoring function** (FrugalGPT) | post-hoc | Trained DistilBERT → reliability score 0–1 on answer | **[benchmark-reported]** matches best single LLM at **up to 98% cost cut**, or +4% acc same cost (C13) | cheap (small BERT); **needs per-task training data** | No LLM internals; needs trained scorer | yes |
| 9 | **Task-type / difficulty classifier (pre-hoc router)** (RouteLLM) | **pre-hoc** | Classify query hard/easy → pick tier *before* generating | **[benchmark-reported]** RouteLLM: **85% cost cut on MT-Bench @ 95% GPT-4 quality**, 35–46% on MMLU/GSM8K; BERT router **<10ms**, no LLM call (C14). RouterBench/LLMRouterBench standardize eval (C15,C16) | **<10ms**, no generation | No internals; needs trained router (preference data) | partially |
| 10 | **Context-size / capability-match heuristic** | **pre-hoc** | Fit local ctx window? need vision/tools/long-ctx/lang local lacks? | **[doc-claim]** deterministic guardrail; capability mismatch is a hard route, not a confidence call | ~0 (length/flags) | No internals | **yes** (token count, modality, tools all harness-visible) |
| 11 | **Harness: test / compile failure** | **harness** | Did generated code build & pass tests? fail ⇒ escalate | **[benchmark-reported]** escalation ladder (8B→GPT-3.5→70B→GPT-4) keyed on **test-case failure** (C17); SWE-agent: execution feedback drives loops (C18) | full attempt + test exec (slow) but **free signal** | No internals — ground truth, not probabilistic | **yes — natively** (exit codes, test reports) |
| 12 | **Harness: lint / type errors** | **harness** | Static failures in generated output | **[doc-claim]** cheap pre-test gate | run linter (cheap) | No internals | **yes** |
| 13 | **Harness: tool-call failure / schema violation** | **harness** | Malformed/failed tool call ⇒ retry-or-escalate | **[doc-claim]** "retryable" flag escalates non-recoverable errors immediately; schema violation → retry/repair/escalate (C19) | ~0 (catch error) | No internals | **yes** |
| 14 | **Harness: retry exhaustion** | **harness** | K self-debug retries spent w/o passing ⇒ escalate | **[doc-claim]** trial-and-error retry w/ error msg standard; exhaustion = natural trigger (C18,C19) | K× attempts (slow) | No internals | **yes** |

## Reading the landscape (directional)

- **Cheapest & strongest measured ROI for general queries:** pre-hoc trained routers (#9 RouteLLM, <10ms, 85% cut **[benchmark-reported]**) and learned scorers (#8 FrugalGPT, up to 98% **[benchmark-reported]**). Cost: need training data + a maintained model.
- **Strongest for *our* domain (code, C3):** **harness signals #11–#14 are highest-fidelity and cheapest-to-trust** — ground truth, not probability; a failing test is not miscalibrated. Fully local, vendor-neutral (N2/N3). Cost is latency (learn only after a full attempt).
- **Best confidence signals without a trained model:** self-consistency (#4) and ensemble agreement (#6/ABC) — training-free, no internals; ABC maps onto N4 multi-machine. Cost is N×/M× generation.
- **Token-level (#1–#3):** nearly free and **now locally exposed across all three engines** — but see the constraint.

### The determining constraint (single biggest reliability caveat)
**Raw token-level confidence (logprob / entropy / perplexity) is systematically miscalibrated and prompt-sensitive** [C1, C5, C12]: a model emits fluent, high-probability text while wrong (and false-escalates on ambiguous-but-correct answers). So the cheap, locally-available signals (#1–#3) are the *least trustworthy raw*. Every serious 2024–2026 system either (a) **calibrates/tunes the threshold** (UCCI, confidence-tuned cascades — C1,C12), (b) moves to **semantic/agreement** space (#4–#6), or (c) backstops with **ground-truth harness signals** (#11–#14). **Implication for C3: do not gate escalation on raw local logprobs alone.**

### Local-engine exposure summary (N3/sovereignty-relevant)
- **logprobs/top-k (#1–#3, P(True) #7):** llama.cpp (`n_probs`→`top_logprobs`) ✅, vLLM (`logprobs`,`prompt_logprobs`) ✅, **Ollama ✅ only since v0.12.11** (Ollama *Cloud* returns null — moot for self-hosted; L4).
- **hidden states/activations (SEP #5b):** **not exposed by any of the three standard servers** — needs custom inference hooks. The cheapest semantic method is effectively off-limits on the stock local stack.
- **No-internals signals (#4,#6,#8,#9,#10,#11–#14):** engine-agnostic; text + exit codes. Most sovereignty-robust (N2/N3).

## New signal / sub-areas surfaced (beyond the brief)

1. **Timing-class is the real taxonomy** (pre-hoc / post-hoc / harness) — not the flat "trigger" list; it determines cost and required internals.
2. **Hidden-state probes (SEP) are a feasibility cliff** for self-hosting — the one cheap semantic method needs activations no local server exposes.
3. **Ollama logprob support is recent (v0.12.11)** — prior-art assuming "Ollama can't do logprobs" is stale; version-pin in the KB.
4. **P(True) couples a "judge" to logprob exposure** — a hybrid between #1 and #7; cheap if the local model self-scores via the "true" token logprob.
5. **Calibration / threshold-tuning is itself a sub-capability**, not a signal (UCCI, confidence-tuning) — C3 likely needs calibration as a first-class component.

## Cites
- **C1** `{type: paper, ref: https://arxiv.org/html/2502.19335v1, title: Improving Model Cascades Through Confidence Tuning}`
- **C2/UCCI** `{type: paper, ref: https://arxiv.org/html/2605.18796, title: UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing}`
- **C4** `{type: paper, ref: https://research.google/pubs/confidence-improves-self-consistency-in-llms/, title: Confidence Improves Self-Consistency in LLMs}`
- **C5/C9** `{type: paper, ref: https://arxiv.org/html/2604.17112, title: Complementing Self-Consistency with Cross-Model Disagreement for UQ}`
- **C6** `{type: paper, ref: https://www.researchgate.net/publication/381550138_Detecting_hallucinations_in_large_language_models_using_semantic_entropy, title: Detecting hallucinations in LLMs using semantic entropy (Nature 2024)}`
- **C7** `{type: paper, ref: https://arxiv.org/abs/2406.15927, title: Semantic Entropy Probes}`
- **C8** `{type: paper, ref: https://arxiv.org/abs/2407.02348, title: Agreement-Based Cascading for Efficient Inference}`
- **C10** `{type: blog, ref: https://www.comet.com/site/blog/llm-as-a-judge/, title: LLM-as-a-Judge: Reliable, Scalable Evaluation}`
- **C11** `{type: paper, ref: https://arxiv.org/pdf/2507.08794, title: One Token to Fool LLM-as-a-Judge}`
- **C12** `{type: blog, ref: https://tianpan.co/blog/2025-11-03-llm-routing-model-cascades, title: LLM Routing and Model Cascades}`
- **C13** `{type: paper, ref: https://arxiv.org/pdf/2305.05176, title: FrugalGPT}`
- **C14** `{type: paper, ref: https://arxiv.org/pdf/2406.18665, title: RouteLLM}` · `{type: blog, ref: https://www.lmsys.org/blog/2024-07-01-routellm/, title: RouteLLM (LMSYS)}`
- **C15** `{type: paper, ref: https://openreview.net/pdf?id=IVXmV8Uxwh, title: RouterBench}`
- **C16** `{type: paper, ref: https://arxiv.org/html/2601.07206v1, title: LLMRouterBench}`
- **C17** `{type: paper, ref: https://arxiv.org/html/2603.04445v2, title: Dynamic Model Routing and Cascading: A Survey}`
- **C18** `{type: paper, ref: https://arxiv.org/pdf/2405.15793, title: SWE-agent}`
- **C19** `{type: blog, ref: https://medium.com/@spacholski99/error-handling-for-ai-agents-a-different-standard-than-classic-apps-5d7f9096c3cc, title: Error Handling for AI Agents}`
- **L1** `{type: docs, ref: https://docs.vllm.ai/en/latest/api/vllm/logprobs/, title: vLLM logprobs}`
- **L2** `{type: docs, ref: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md, title: llama.cpp server README}`
- **L3** `{type: docs, ref: https://docs.ollama.com/api/generate, title: Ollama Generate API}` · `{type: repo, ref: https://github.com/ollama/ollama/issues/16117, title: Add logprobs to /v1/chat/completions}`
- **L4** `{type: repo, ref: https://github.com/ollama/ollama/issues/13638, title: Logprobs not returned from Ollama Cloud API}`
