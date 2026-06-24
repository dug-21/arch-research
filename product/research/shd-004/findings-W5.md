# shd-004 — W5: Multi-machine distribution (N4)

**Workstream:** W5 — for the leading local-inference engines, does the engine's architecture *foreclose* multi-machine / multi-GPU scaling, or *extend* to it? **N4 is a tie-breaker, NOT a gate** (D11). It must not gate the single-box recommendation.
**Date:** 2026-06-24
**Researcher:** read-only, directional. No installs, no runs. **Doc-claims / vendor-doc derived only — nothing here is demonstrated evidence by us.**
**Frame (per shd-002 W4):** *FORECLOSES* = single-machine-bound by design, cross-host needs re-foundation. *EXTENDS* = ships explicit multi-GPU and/or cross-machine distribution features. The interconnect reality is the determining constraint for whether "extends" is *realistically usable on owned consumer hardware* vs. *datacenter-practical only*.

---

## 1. Forecloses / extends table

| Engine | Single-box multi-GPU | Cross-machine mechanism | Realistic on owned HW over Ethernet? | Flag | Evidence grade |
|---|---|---|---|---|---|
| **llama.cpp** | Yes — layer/tensor split across local GPUs (`--tensor-split`); also tensor-parallel-ish offload | **`rpc-server` + `--rpc host:port`** — distributes weights + KV cache across local **and remote** devices by available memory; optional RDMA/RoCEv2, else TCP | **Yes, for memory-pooling** (run a model too big for one box). Works over plain Ethernet/TCP. **But**: self-described "proof-of-concept… fragile and insecure"; overhead is real, not a speedup — it's the *only* engine whose cross-machine path is genuinely consumer-Ethernet-usable | **EXTENDS** (memory-pool); cross-host is POC-grade | Doc-claim, primary (RPC README) |
| **Ollama** | Yes — auto-detects all NVIDIA/AMD GPUs, splits layers via llama.cpp's `--tensor-split` internally; zero config | **None native.** Built on llama.cpp but does **not** expose the RPC backend. Workaround = run N independent Ollama instances + app-level routing | **No** native path; only app-level fan-out of independent instances (no shared model across hosts) | **NEUTRAL** (single-box multi-GPU yes; cross-host foreclosed *in-product*, escapable only by external orchestration) | Doc-claim |
| **vLLM** | Yes — **`--tensor-parallel-size`** (Megatron-LM TP); multiprocessing backend, scales well to ~8 GPUs on NVLink, diminishing returns past ~4 on PCIe | **`--pipeline-parallel-size` + Ray** across nodes (TP within box, PP across boxes) | **Datacenter-practical only.** Docs: "efficient tensor parallelism requires fast internode communication, preferably InfiniBand"; cross-node over plain socket logs `[send] via NET/Socket` = "not efficient." PP across nodes is *less* bandwidth-hungry but still wants real interconnect | **EXTENDS** (single-box TP strong); cross-machine extends but **interconnect-bound** | Doc-claim, primary (vLLM docs) |
| **SGLang** | Yes — TP/PP/EP/DP; strong intra-node TP | **Multi-node** TP+PP (e.g. `tp=8 pp=4`); PP only needs cross-node comms at pipeline-stage boundaries → >80% scaling efficiency to PP4, better comp/comm overlap than large TP | **Datacenter-practical** (benchmarks on H20/H100 clusters). PP design *reduces* cross-node bandwidth need vs TP, but still aimed at cluster interconnect, not consumer Ethernet | **EXTENDS**; cross-machine extends but **cluster-oriented** | Doc-claim |
| **TGI** | Yes — **`--num-shard N`** auto-shards model across local GPUs (tensor parallel, NCCL-synchronized) | Sharding is **intra-node** (NCCL across local GPUs). Multi-node not a first-class documented path; relies on external orchestration (K8s/LWS) for replica fan-out, not a single sharded model across hosts | **No** for a single model across owned boxes over Ethernet; intra-box sharding only | **NEUTRAL→EXTENDS** (single-box multi-GPU yes; cross-host not a native single-model feature) | Doc-claim |
| **ExLlamaV2 / TabbyAPI** | Yes — introduced **tensor parallelism**; TabbyAPI auto-splits / autosplit fallback across local GPUs; GPU-only, INT4-focused | **None.** No documented cross-machine mechanism — TP is intra-node CUDA only | **No** cross-host path; single-box multi-GPU only | **NEUTRAL** (single-box multi-GPU yes; cross-host foreclosed in-product) | Doc-claim |

---

## 2. Verdict — weak tie-breaker; forecloses no one for the single-box recommendation

**N4 does not eliminate any engine, and it should not pull the recommendation.** Mirroring shd-002 W4's "forecloses no one": every candidate handles the cheap, load-bearing unlock — **single-box multi-GPU (2×24GB)** — which is the part N4 actually buys us near-term. vLLM, SGLang, ExLlama/Tabby ship real **tensor parallelism**; llama.cpp/Ollama/TGI ship **layer-split / sharding**. None forecloses the single-box scale-up.

Where the field *does* separate is the **cross-machine-over-owned-Ethernet** question — and here the determining constraint is **interconnect bandwidth, not engine choice**:

- **Only llama.cpp's `rpc-server` is realistically usable across owned consumer machines over plain Ethernet** — and only for *memory pooling* (running an over-large model), not for speedup, and at POC/"fragile, insecure" maturity. Ollama inherits llama.cpp's lineage but **does not expose** this, so its cross-host story is weaker than its base.
- **vLLM / SGLang / TGI cross-node paths are datacenter-practical only**: they assume InfiniBand/NVLink/RDMA. Over consumer Gigabit/10GbE, tensor-parallel cross-node is bandwidth-bound and explicitly "not efficient" (vLLM docs); pipeline-parallel (SGLang's strength) softens but does not remove this.
- **ExLlama/Tabby and TGI** offer no cross-machine path at all — but that is **NEUTRAL, not disqualifying**, since N4 only asks "does it foreclose?"

**Net:** the meaningful, attainable N4 unlock on owned hardware is **single-box 2×24GB tensor parallel**, which *every* serious GPU engine here provides. True cross-machine distribution is either (a) consumer-usable but POC-grade and memory-pool-only (llama.cpp RPC), or (b) production-grade but interconnect-gated to a datacenter we don't own. So **N4 is a weak tie-breaker**: it favors, very mildly, engines with real single-box TP (**vLLM, SGLang, ExLlama/Tabby**) for the cheap unlock, and notes **llama.cpp** as the *only* genuine owned-multi-machine escape hatch if a future model exceeds a single box. **Do not let N4 gate or reorder the single-box-first recommendation** — settle that on the load-bearing constraints (throughput, quant quality, VRAM fit, autonomy), then let N4 nudge ties only.

**Skeptic's flag:** all doc-claim. No distribution path was exercised by us (methodology L1). "EXTENDS" means a documented feature exists, not that it coordinates as advertised — llama.cpp RPC's own "proof-of-concept / fragile" language is the clearest warning to not over-trust the cross-machine column.

---

## 3. Citations (doc-claims, retrieved 2026-06-24)

**llama.cpp (RPC):**
- RPC backend README (primary): https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md — `rpc-server`, `--rpc`, weight+KV distribution by memory, RDMA/RoCEv2 vs TCP, "proof-of-concept… fragile and insecure," "Never run the RPC server on an open network."
- Distributed inference discussion: https://github.com/ggml-org/llama.cpp/discussions/15796
- Multi-GPU & distributed inference (DeepWiki): https://deepwiki.com/ggml-org/llama.cpp/8.4-multi-gpu-and-distributed-inference
- Consumer bare-metal walkthrough: https://medium.com/@soumyajit.swain/distributed-llm-inference-on-consumer-machines-with-llama-cpp-a-bare-metal-approach-55ef6ef81f35

**Ollama:**
- Multi-GPU official behavior / layer split: https://willitrunai.com/blog/ollama-multi-gpu-guide
- "Llama.cpp now supports distributed inference across multiple machines" (Ollama issue — confirms no native Ollama RPC): https://github.com/ollama/ollama/issues/4643
- Local → distributed levels: https://www.bentoml.com/blog/running-local-llms-with-ollama-3-levels-from-local-to-distributed-inference

**vLLM:**
- Parallelism and Scaling (primary): https://docs.vllm.ai/en/stable/serving/parallelism_scaling/ — TP=GPUs/node, PP=nodes, "efficient tensor parallelism requires fast internode communication, preferably InfiniBand," `[send] via NET/Socket` inefficiency.
- Distributed Inference and Serving: https://docs.vllm.ai/en/v0.9.1/serving/distributed_serving.html
- Multi-GPU need (NVLink vs PCIe scaling): https://willitrunai.com/blog/vllm-multi-gpu-setup-guide

**SGLang:**
- Pipeline parallelism doc: https://github.com/sgl-project/sglang/blob/main/docs/advanced_features/pipeline_parallelism.md
- Chunked-prefill pipeline / scaling efficiency: https://www.lmsys.org/blog/2026-01-15-chunked-pipeline/
- Multi-node deployment: https://sgl-project-sglang-93.mintlify.app/deployment/multi-node
- Distributed execution (DeepWiki): https://deepwiki.com/sgl-project/sglang

**TGI:**
- Architecture (sharding / NCCL): https://huggingface.co/docs/text-generation-inference/en/architecture
- Tensor parallelism on TGI (`--num-shard`): https://github.com/huggingface/text-generation-inference/issues/1315
- Guide: https://vife.ai/blog/mastering-text-generation-inference-guide-hugging-face-tgi

**ExLlamaV2 / TabbyAPI:**
- TabbyAPI server options (TP, autosplit): https://github.com/theroyallab/tabbyAPI/wiki/02.-Server-options
- ExLlamaV2 + TabbyAPI guide (INT4, single-GPU/multi-GPU TP): https://localaimaster.com/blog/exllamav2-tabbyapi-guide
- "Use vLLM or ExLlamaV2 for tensor parallelism" (multi-GPU positioning): https://www.ahmadosman.com/blog/do-not-use-llama-cpp-or-ollama-on-multi-gpus-setups-use-vllm-or-exllamav2/

---

## Limits of this finding
- 100% doc-claim / vendor-doc derived. No distribution path exercised by us (methodology L1); a live test could show a "multi-node" or "RPC" mode does not coordinate as advertised on our hardware.
- The single most important carry-forward: the **owned-hardware-over-Ethernet** column is bandwidth-bound for every TP path except llama.cpp RPC's memory-pool mode, which is itself POC-grade. Treat cross-machine as *not foreclosed* but *not free* — and keep it out of the single-box-first decision per D11.
