# shd-004 — Local LLM inference engine + model landscape for the self-hosted dev/research loop

**Status:** SCOPE
**Goal(s):** `shd` (primary, #3)
**Capability target(s):** **C1 — Capable LLM inference runs on local hardware** (#4)
**Confidence-required:** directional
**Phase / area:** inference
**Cycle topic / Issue:** shd-004

Governing NFRs (via `About→ C1`): N1 owned-HW/budget (#7) · N2 no-outage/offline (#8) · N4 multi-machine-ready (#10).

---

## The question

Survey the landscape of ways to **serve capable, coding-grade LLM inference on owned local hardware** — the cross-product of inference engine/runtime, coding-grade open model, and quantization format against a target-hardware envelope — and rank it. The output is a directional map (what's easy, what's hard, what's a dream), a leading-candidate stack, and a validated follow-on that actually serves a model and measures it.

> Which engine + model + quantization stack should we POC first to serve a coding-grade model on owned hardware at usable throughput — and what must that POC prove?

## Why it matters

C1 is the **inference floor** of `shd`: it is a `Prerequisite→ C2`, so the agentic harness slate from shd-002 (aider, Claude Code + local shim, Continue) is inert until a local backend serves a coding-grade model fast enough to drive multi-step work. The harness choice also **constrains the serving contract** — the C2 slate speaks OpenAI-compatible `/v1/chat/completions` (and, for the Claude Code shim, an Anthropic `/v1/messages` translation), so the engine we rank must expose the protocol the harness layer speaks, not just raw generation. Picking an engine/model/quant stack that can't hit usable tok/s on owned HW, or can't serve the right protocol, re-foundations the whole loop. This scope ranks the field so the validated follow-on POCs the right stack first instead of burning budget on a dead end.

## Known constraints & prior art  *(build on these — do not re-derive)*

- **Reuse-first:** **no `technology` nodes exist for C1 inference yet** — the KB has only the factory-plane bootstrap entries and the shd-002 harness landscape (still `claimed`). This scope establishes the inference `technology` nodes. Curator searches `category:technology` FIRST before storing, per the access rules, and links each new node `Prerequisite→ C1`.
- **C2 dependency (shd-002):** the harness slate (aider · Claude Code + local shim · Continue) is the consumer. "Coding-grade" is defined by what *that slate* needs to complete tasks, and the **serving protocol is a hard filter** — an engine that cannot expose an OpenAI-compatible endpoint (or be fronted by a translation shim for Anthropic `/v1/messages`) is disqualified regardless of throughput. Carry shd-002's L1 lesson forward: tool-call / streaming reliability on local models is the silent failure mode — flag it per engine, but the live smoke test lands in the validated follow-on, not here.
- **N1 (owned-HW/budget):** rank against *owned/affordable* hardware envelopes only — consumer GPU (e.g. single 24GB-class card), Apple Silicon unified memory, CPU/RAM-only, and small multi-GPU. No datacenter-class assumptions. VRAM/RAM is the dominant gating resource and sets which model×quant combinations are even loadable.
- **N2 (no-outage/offline):** the stack must run fully offline after model download — no license server, no cloud callback, no metered API. Weights must be redistributable/locally-cacheable (flag license/gating per model).
- **N4 (multi-machine-ready):** weight multi-machine distribution (tensor/pipeline parallel, distributed llama.cpp RPC, vLLM distributed) as a **tie-breaker, not a gate** (per D11) — does an engine *foreclose* scaling across owned machines, or extend to it later? It does not gate the single-box recommendation.

## Bounded investigation (workstreams)

Each workstream is one researcher's partition. State an explicit `Output:` per workstream.

- **W1 — Inference engine / runtime inventory.** Enumerate the engines that serve LLM inference locally (llama.cpp, Ollama, vLLM, SGLang, TGI, LM Studio, MLX / MLX-LM, ExLlamaV2/TabbyAPI, and any others surfaced). For each: which hardware it targets, which quant formats it loads, and — critically — **whether it exposes an OpenAI-compatible (and/or Anthropic-shimmable) serving endpoint** the C2 slate can speak to. *Output:* a candidate engine list with a one-line profile each + a serving-protocol column (OpenAI-compatible? Anthropic-shimmable? raw-only?).
- **W2 — Coding-grade open model survey.** Enumerate open models strong at code that plausibly fit owned HW (Qwen2.5-Coder / Qwen3-Coder family, DeepSeek-Coder / DeepSeek-Coder-V2, Codestral, Llama-3.x, StarCoder2, and any others surfaced), across parameter sizes. For each: approximate coding capability tier (doc-claim vs benchmark-reported — keep the firewall), parameter count, and **license / weight-gating** (N2). *Output:* a model shortlist with a capability tier + size + license note each, separating doc-claim from benchmark-reported.
- **W3 — Quantization / format tradeoffs.** Map the format landscape (GGUF k-quants, AWQ, GPTQ, FP8, EXL2, MLX) on the three axes that decide a stack: **accuracy degradation vs throughput vs VRAM/RAM footprint**, and which engines from W1 consume which formats. *Output:* a quant-format tradeoff matrix (accuracy / throughput / footprint / engine-compatibility), with the determining constraint named per format.
- **W4 — Target-hardware envelopes & throughput.** For the owned-HW classes under N1 (consumer GPU, Apple Silicon unified memory, CPU/RAM-only, small multi-GPU), establish which model×quant combinations are *loadable* and what throughput is *reported* (doc/community-reported tok/s — explicitly NOT demonstrated by us; that is the follow-on). *Output:* a hardware-envelope table — per HW class, which model×quant fits and the reported tok/s ballpark, flagged as report-not-demonstrated.
- **W5 — Multi-machine distribution (N4).** Does each leading engine foreclose or extend to multi-machine serving (tensor/pipeline parallel, llama.cpp RPC, vLLM distributed)? *Output:* a forecloses / extends flag per leading engine — a tie-breaker, not a gate.
- **W6 — Synthesis & ranking.** Rank the **engine × model × quant** stacks easy / moderate / hard / dream against the owned-HW envelope, with the determining constraint named (almost always VRAM or protocol-compatibility); recommend a leading stack as a `position`; specify the **validated follow-on scope** (`shd-005`) and exactly what its POC must demonstrate. *Output:* a ranked stack map + recommendation + drafted follow-on bar.

## Expected output (FINDINGS.md)

1. **Engine feasibility map** — each engine tagged easy / moderate / hard / dream for the C1 job, determining constraint named, with the **serving-protocol** column (OpenAI-compatible / Anthropic-shimmable / raw-only) made explicit — engines that can't speak the C2 slate's protocol are flagged disqualified-or-shim-required.
2. **Coding-grade model shortlist** — capability tier + parameter size + license/gating (N2), doc-claim separated from benchmark-reported.
3. **Quantization tradeoff matrix** — accuracy / throughput / footprint / engine-compatibility per format.
4. **Hardware-envelope table** (N1) — per owned-HW class, which model×quant fits and the reported tok/s ballpark, every throughput number flagged **reported, not demonstrated by us**.
5. **Distribution flags** (N4) — forecloses / extends, per leading engine.
6. **Recommendation** — the leading engine × model × quant stack + reasoning, as a `position` finding.
7. **Validated follow-on** — a draft `shd-005` scope question + the concrete POC bar it must clear (below).

## Proof bar  *(directional)*

**Structure-only — no status change.** This scope produces `finding`s + `technology` nodes left `claimed` (engines, models, quant formats) + a `position` recommendation. **Every throughput / capability figure it carries is doc-claim or community-report, never demonstrated by us — nothing reaches `partial` or `proven` here.** It *spawns* a validated follow-on (`shd-005`) that will move a technology toward `proven`; this scope proves nothing itself.

The follow-on (`shd-005`) POC must demonstrate, **at runtime altitude, by us**, a concrete `done_when`:
> Serve coding model **X** under engine **E** at quant **Q** on owned hardware **Y**, exposing the OpenAI-compatible (and/or Anthropic-shimmed) endpoint the C2 slate consumes, sustaining **≥Z tok/s** generation with **acceptable coding quality on task P** (a held-out coding-grade completion). The recommendation from this scope fixes the candidate values of X / E / Q / Y / Z / P that the POC must hit; the POC attaches the served-completion + measured-throughput artifact to `proven_by`.

## Explicitly out of scope

- The **agentic harness layer** — that is C2 / shd-002. This scope serves the model; it does not drive it.
- **Actually building, installing, serving, or benchmarking** any engine/model — all measurement is the validated follow-on (`shd-005`). Throughput here is reported, never demonstrated.
- **Routing / escalation** between local and frontier models — that is C3.
- Final stack selection *by benchmark* — this scope *recommends a direction* and names what to POC; the benchmark verdict belongs to `shd-005`.
- Fine-tuning / training / model adaptation — serving stock open weights only.

## Coverage / done call  *(synthesis)*

Loop-until-dry: stop when **K=2** consecutive searches surface no new engine, model, or quant format **and** **≥2** independent findings corroborate the leading engine × model × quant stack. Agent proposes "sufficient"; **human confirms** at the synthesis gate.
