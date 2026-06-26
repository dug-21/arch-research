# Findings — shd-005 / W2: Standalone routers, gateways & aggregators

**Run:** shd-005 · **Workstream:** W2 · **Agent:** shd-005-researcher-W2 · **Date:** 2026-06-26
**Capability:** C3 — intelligent multi-LLM routing · **Governing NFRs:** N1 budget · N2 no-outage/vendor-not-load-bearing · N3 sensitive code stays local (HARD) · N4 multi-machine-ready
**Mode:** read-only, directional. Evidence tagged **doc-claim** vs **benchmark-reported**. Nothing here is `proven`.

## The governing axis — sovereignty seam

Every option classified **self-hosted / local-control** (routing logic runs on owned hardware; only the chosen frontier *call* egresses) vs **hosted middleman** (all traffic transits a third party's cloud). **Hosted middlemen are disqualified AS the router for sensitive paths** — they see every prompt/completion by construction, violating N3 (HARD) and making a vendor load-bearing (N2). They may appear only as a *frontier egress target* behind a privacy gate, never as the routing brain on a sensitive path.

The decisive split is **where the classifier runs**, not whether the tool is "open." A learned router that is excellent but only callable as a cloud API (Not Diamond, Martian, Unify) still egresses the prompt for the routing decision — so it is a middleman *even when the eventual model call would have stayed local*.

## Landscape table

| Option | Sovereignty class | Models/providers spanned | Routing logic | Harness integration | N2/N3 posture | Savings/quality | Maturity | N4 | C3 tag |
|---|---|---|---|---|---|---|---|---|---|
| **LiteLLM (proxy)** | **Self-hosted** ✅ | 100+ providers / 2,500+ models (doc-claim) incl. Anthropic, OpenAI, Bedrock, Ollama, vLLM | Rule / cost / load-balance / fallback (config-driven; **not** learned by default) | Self-hosted OpenAI-compat endpoint; drop-in. Already the **Anthropic-native shim** in shd-004 #54 | Strong: runs in your network, one uniform data policy you set; only chosen call egresses | Routing savings config-dependent (no learned quality model) — doc-claim | High; de-facto backbone | Extends (multi-instance/clustered) | **easy** |
| **Portkey Gateway (OSS)** | **Self-hosted** ✅ (OSS repo) | 1,600+ models (doc-claim) | Rule-based configs: routing rules, fallback, load-balance, guardrails, circuit breakers | Self-host via npx/Docker/K8s/CF Workers; OpenAI-compat; <1ms added latency (doc-claim) | Strong **when self-hosted** (Apache-2.0, full feature set, no license keys as of Mar-2026). Their **SaaS control plane = middleman** | Reliability/cost via fallback+caching; doc-claim | High; ~2T tokens/day (vendor) | Extends (stateless, K8s-native) | **easy/moderate** |
| **RouteLLM** | **Self-hosted** ✅ (lm-sys, Apache) | Binary **strong-vs-weak** pair you configure (not a broad catalog) | **Learned** (matrix-factorization / BERT / SW-ranking / causal-LLM classifier) — runs locally | Local OpenAI-compat server; drop-in OpenAI client replacement | Strong: classifier runs on your HW; only escalated call egresses | **benchmark-reported**: ~95% of GPT-4 quality at 26%→14% strong-model calls; up to 85% cost cut MT-Bench, 45% MMLU, 35% GSM8K | Medium; research-origin, needs calibration | Extends (stateless) | **moderate** |
| **ruflo** (ruvnet/ruflo, ex-"Claude Flow") | **Self-hosted routing logic** ✅ but **agent meta-harness, not a standalone drop-in router** | Any LLM (Claude/GPT/Gemini/Cohere/local Llama) | 3-tier classifier (configurable, **can be a local model**): WASM/no-LLM → cheap model → Opus; swarm-vs-single | Native Claude Code / MCP (it *is* the harness, not a proxy in front of one) | Routing decision can stay local; failover built-in. Harness-coupling is the catch | "up to 75% API cost" 3-tier (doc-claim) | Active, fast-moving; harness-scoped | Extends (swarm/federate is its premise) | **moderate** (scope-coupled) |
| **OpenRouter** | **Hosted middleman** ⛔ | Hundreds of models, one endpoint | Provider/price/uptime routing in *their* cloud | OpenAI-compat base-url swap | **Disqualified as router for sensitive paths.** ZDR-default + training opt-out + EU-region (doc-claim) reduce but don't remove cloud transit; metadata retained | Cost via provider arbitrage; doc-claim | High | N4-neutral (moot) | **target-only** (egress behind a gate) |
| **Requesty** | **Hosted middleman** ⛔ | 300–400+ models | Auto request-type detection → best model; fallback <20ms (doc-claim) | router.requesty.ai base-url swap; "host nothing" | **Disqualified as router.** Managed-only; all traffic transits Requesty | Cost via cheaper-equivalent routing + caching; doc-claim | Medium/High | N4-neutral | **target-only / disqualified-as-router** |
| **Martian** | **Hosted middleman** ⛔ | Large catalog | **Learned** "model-mapping" interpretability router; cost/willingness-to-pay controls | Drop-in OpenAI-compat endpoint (their cloud) | **Disqualified as router.** SaaS; prompt egresses for routing | "beats GPT-4" via model-mapping (vendor PR; not independently benchmarked) | Funded startup ($9M; Accenture); SaaS | N4-neutral | **disqualified-as-router** |
| **Unify** (unify.ai) | **Hosted middleman** ⛔ | All major models/providers, one endpoint | **Learned** neural router trained on live (10-min-refresh) public benchmarks | Hosted single endpoint | **Disqualified as router.** SaaS; prompt egresses | Balances cost/latency/quality; public live benchmarks (transparency plus), savings doc-claim | **Uncertain** — third-party writeups treat router product as legacy/pivoted; verify | N4-neutral | **disqualified-as-router** |
| **Not Diamond** | **Hosted middleman** ⛔ for sensitive (API-based) | Trained over your candidate-LLM set | **Learned** meta-model; trainable custom router on your eval data | API returns a routing *decision*; works alongside your gateway/harness | **Disqualified for sensitive paths**: prompt egresses to ND for classification. Self-host "possible but considerable engineering effort" (vendor doc) — not productized | "beat every individual model" via meta-model (doc-claim) | Medium; well-regarded framing | Would extend *if* self-hosted (not practical today) | **disqualified-as-router** (concept = dream if local meta-model lands) |

### Others surfaced (not in the brief)
- **freerouter** (openfreerouter/freerouter) — **self-hosted** ✅, uses *your own* API keys, 14-dimension classifier routes to Anthropic/OpenAI/Kimi, "no middleman, no markup." Built for OpenClaw. New/immature — **flag, low maturity**, on-axis. **moderate.**
- **Morph Router**, **ClawRouter** — positioned as OpenRouter/Not-Diamond alternatives; sovereignty class unverified — **unresolved, deprioritized.**

## `ruflo` identification (requested)
**Identified:** `ruflo` = **`ruvnet/ruflo`** on GitHub (~61k★), an **agent meta-harness for Claude**, *formerly named "Claude Flow,"* renamed by "rUv." **Not** RouteLLM, Requesty, or RooFlow. Multi-agent orchestration harness with an **embedded** 3-tier model router (configurable classifier that can be a *local* model; WASM/cheap-model/Opus tiers), native Claude Code + MCP integration. **Caveat for C3:** routing is welded into the harness, so ruflo is a *harness-with-routing*, not a standalone router you can place in front of an arbitrary OpenAI/Anthropic harness — it likely belongs to the harness workstream as much as W2.

## Synthesis for C3
- **Genuinely self-hostable (routing brain on owned HW):** LiteLLM, Portkey-OSS, RouteLLM, freerouter, ruflo's embedded router. Satisfy the sovereignty axis — only the chosen frontier *call* egresses.
- **Hosted middlemen, disqualified AS the router on sensitive paths:** OpenRouter, Requesty, Martian, Unify, Not Diamond. OpenRouter is the only one worth keeping as a *frontier egress target* behind a privacy gate — never the classifier for N3-HARD code.
- **Determining constraint (directional):** **learned routing vs sovereignty**. The strongest *learned* routers (Martian, Unify, Not Diamond) are cloud-API middlemen; the sovereign self-hosted options are mostly **rule/cost-based** (LiteLLM, Portkey). **RouteLLM is the one self-hosted *learned* router** — but binary strong/weak, so a quality-escalation gate, not a full catalog router.
- **Likely C3 shape:** **LiteLLM (or Portkey-OSS) as the self-hosted OpenAI/Anthropic-compat gateway + fallback/cost backbone**, optionally **RouteLLM as a local learned escalation gate** in front. Composes with shd-004 #54.
- **N4:** no self-hosted router forecloses multi-machine; LiteLLM/Portkey/RouteLLM stateless and multi-instance — **N4-extends**. Hosted middlemen N4-neutral but moot.
- **C3 tags:** LiteLLM **easy** · Portkey-OSS **easy/moderate** · RouteLLM **moderate** · ruflo **moderate** (scope-coupled) · freerouter **moderate** (immature) · a self-hosted *learned, broad-catalog, confidence-based* router at frontier-quality parity = **dream**.

## Flags / could-not-verify
- **Unify maturity** — sources hint router product is legacy/pivoted; verify viability (disqualified-as-router regardless).
- **Martian "beats GPT-4"** is vendor PR, not independently benchmarked — doc-claim only.
- **RouteLLM** binary strong/weak constraint + threshold training for *our* model pair unverified — POC-grade.
- **freerouter / Morph / ClawRouter** maturity and data-flow unverified — surfaced, not deeply profiled.
- Savings % for self-hosted rule-based gateways (LiteLLM/Portkey) are **config-dependent**, not a tool property — no benchmark backs a number for our setup.

## Citations
- {type: repo, ref: github.com/BerriAI/litellm, title: "LiteLLM — Python SDK & Proxy AI Gateway"}
- {type: doc, ref: docs.litellm.ai/docs/simple_proxy, title: "LiteLLM AI Gateway (LLM Proxy)"}
- {type: repo, ref: github.com/Portkey-AI/gateway, title: "Portkey AI Gateway — route to 1,600+ LLMs"}
- {type: article, ref: thenewstack.io/portkey-gateway-open-source/, title: "Portkey open-sources its AI gateway"}
- {type: repo, ref: github.com/lm-sys/RouteLLM, title: "RouteLLM — serving & evaluating LLM routers"}
- {type: article, ref: lmsys.org/blog/2024-07-01-routellm/, title: "RouteLLM: cost-effective LLM routing (benchmarks)"}
- {type: repo, ref: github.com/ruvnet/ruflo, title: "ruflo — agent meta-harness for Claude (ex Claude Flow)"}
- {type: doc, ref: github.com/ruvnet/ruflo/blob/main/docs/USERGUIDE.md, title: "ruflo USERGUIDE"}
- {type: doc, ref: openrouter.ai/docs/faq, title: "OpenRouter FAQ — ZDR & data policy"}
- {type: doc, ref: meetily.ai/llm-privacy/openrouter, title: "OpenRouter data retention policy 2026"}
- {type: doc, ref: requesty.ai, title: "Requesty — AI Gateway & LLM Router (managed)"}
- {type: article, ref: techcrunch.com/2023/11/15/martians-tool-automatically-switches-between-llms-to-reduce-costs/, title: "Martian model router"}
- {type: article, ref: dataphoenix.info/unifys-dynamic-routing-aims-to-solve-the-llm-fragmentation-challenge/, title: "Unify dynamic routing"}
- {type: doc, ref: docs.notdiamond.ai/docs/quickstart, title: "Not Diamond — out-of-the-box router"}
- {type: doc, ref: docs.notdiamond.ai/docs/router-training-quickstart, title: "Not Diamond — custom router / self-host note"}
- {type: repo, ref: github.com/openfreerouter/freerouter, title: "freerouter — self-hosted model router, own API keys"}
- {type: kb, ref: shd unimatrix #54, title: "Serving-protocol filter — LiteLLM shim for non-Anthropic-native engines"}
