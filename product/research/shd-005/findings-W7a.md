# shd-005 / W7a — Platform capability-coverage extension (the broad lens)

**Run:** shd-005 · **Workstream:** W7a · **Agent:** shd-005-researcher-W7a · **Date:** 2026-06-26
**Mode:** read-only, directional. Evidence is **doc-claim / vendor-reported** unless tagged otherwise — **nothing demonstrated by us, nothing `proven`.**
**Re-frame (why this workstream exists):** W1–W6 ranked these tools against **C3 alone**, which under-values multi-purpose platforms (platform-blindness). W7a grades each tool on **how much of the WHOLE `shd` loop it covers**, role-scoped — breadth as an asset, *without* letting breadth paper over a HARD-constraint gap.

> **Reuse, not re-survey.** C3/N2/N3 routing profiles already live in W1–W6 (LiteLLM/Portkey/RouteLLM in W2; harness-native in W3; egress gate in W4; gap test in W6). This file adds the **adjacent/ops** columns and the **per-tool role partition**. Where W7a and a prior file agree, I cite the prior file rather than re-derive.

---

## The need-set (fixed matrix columns) and how each is graded

**Grades:** `✓ strong` · `◑ partial/best-effort` · `✗ none` · `⛔ disqualified-for-this-role-by-a-hard-constraint`.
**Grade-class tag:** **[HARD]** = must be 100% or hard-gated (N3 especially; C3-confidence and N2-no-block are HARD-ish) · **[SOFT]** = convenience/platform-reuse grade (80% reuse is a win).

A structural fact that governs three columns: **none of these tools is a model server (C1) or an agentic harness (C2).** They are the *gateway/proxy layer that sits between* the harness (Claude Code) and the serving engine (llama.cpp/vLLM/Ollama) + frontier. So **C1 = ✗ and C2 = ✗ for all eight** (they front a local engine and sit behind a harness; they neither serve nor drive). Grading them down on C1/C2 is not a discount — it is role scope. Their value is C3 + the ops columns.

---

## Master matrix — tool × need

Tools: **LiteLLM** · **Portkey-OSS** · **Kong AI GW** · **Envoy AI GW** · **Bifrost** (self-hostable class) · **OpenRouter** · **Requesty** · **Cloudflare AI GW** (hosted-middleman class).

### Core + NFRs

| Need (class) | LiteLLM | Portkey-OSS | Kong AI GW | Envoy AI GW | Bifrost | OpenRouter | Requesty | Cloudflare AI GW |
|---|---|---|---|---|---|---|---|---|
| **C1 local serving** [n/a-role] | ✗ fronts engine, doesn't serve | ✗ | ✗ | ◑ "tier-two" ingress to a self-hosted serving cluster (closest) | ✗ (Ollama as provider) | ✗ | ✗ | ✗ |
| **C2 harness drive** [n/a-role] | ✗ sits *behind* the harness | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **C3 routing/escalation** [HARD-ish: confidence] | ◑ rule/cost/LB/embedding-auto + **error**-failover; **no confidence trigger** (W2,W6) | ◑ rule/fallback/LB; no confidence trigger | ◑ 6 LB algos + token-budget routing; no confidence trigger | ◑ quota-aware multi-tenant routing + provider fallback; no confidence trigger | ◑ adaptive LB + cluster routing; no confidence trigger | ◑ provider arbitrage + auto-fallback **but ⛔ on sensitive path** | ◑ auto request-type routing **but ⛔ on sensitive path** | ◑ retries+model-fallback **but ⛔ on sensitive path** |
| **N1 budget/cost** [SOFT] | ✓ per-key/team/user budgets, pre-spend block | ✓ virtual-key monthly caps | ◑ token rate-limit; $-cost tracking enterprise-gated | ✓ per-route input/output/cached/reasoning token cost attribution | ✓ hierarchical budgets (key/team/customer) | ✓ per-model/per-key spend dashboard (+5.5%/5% fee) | ✓ per-user limits, real-time cost analytics | ✓ **$-denominated spend limits** (2026), free tier |
| **N2 resilience/offline** [HARD-ish: no-block] | ✓ fallbacks, local-as-terminal, circuit-breaker (W5) | ✓ fallback/circuit-breaker | ✓ failover/LB | ✓ provider fallback | ✓ failover + cluster mode | ⛔ **the gateway IS the cloud dependency** — can't fail *to* local | ⛔ same | ⛔ same |
| **N3 sensitive-code-local** [**HARD**] | ◑ can **host** the deny-by-default gate; guardrail is entity/PII best-effort + silent-no-op bug (W4 #8359) — **mechanism yes, code-class coverage no** | ◑ self-host + 60+ guardrails (PII/injection) — entity-based, best-effort | ◑ self-host + inline DLP/guardrails — entity/pattern, best-effort | ◑ self-host + policy/quota; thinner DLP | ◑ self-host + guardrails, in-VPC, immutable audit — entity-based | ⛔ **prompt transits 3rd party to route** (W2,W4) | ⛔ managed-only, all traffic transits Requesty | ⛔ hosted; DLP runs in Cloudflare cloud |
| **N4 multi-machine** [SOFT] | ✓ stateless, multi-instance | ✓ stateless, K8s-native | ✓ K8s/data-plane scale | ✓ Envoy/K8s-native | ✓ **native cluster mode** | (n/a hosted) | (n/a hosted) | (n/a hosted, edge) |

### Adjacent / ops (the platform-reuse columns — where breadth lives)

| Need (all [SOFT] unless noted) | LiteLLM | Portkey-OSS | Kong AI GW | Envoy AI GW | Bifrost | OpenRouter | Requesty | Cloudflare AI GW |
|---|---|---|---|---|---|---|---|---|
| **Observability / tracing** | ✓ OTel spans, unified per-call log | ◑ rich analytics but **OSS self-host needs your own logging infra** | ✓ Kong observability stack | ✓ OpenInference + OTel GenAI conventions | ✓ **native Prometheus + OTel** (Grafana/Datadog) | ✓ hosted dashboard | ✓ hosted analytics (latency p-tiles, cache-hit) | ✓ hosted analytics + logs |
| **Cost-tracking & attribution** | ✓ per key/team/user across providers | ✓ per virtual key | ◑ enterprise-gated | ✓ per-route token-class attribution | ✓ hierarchical virtual-key attribution | ✓ per-model/key | ✓ per-user/team | ✓ per model/provider/custom-attr |
| **Key / secret management** | ✓ virtual keys | ✓ virtual keys | ✓ API-key platform (Kong's heritage) | ✓ centralized upstream-cred control plane | ✓ virtual keys + **HashiCorp Vault** | ✓ BYOK store | ✓ key mgmt | ◑ BYOK store |
| **Caching** | ✓ Redis (exact) | ✓ **simple + semantic** | ✓ **semantic** (40–70% cost cut claim) | ✗ not a headline feature | ◑ caching present | ◑ prompt-cache passthrough | ✓ caching | ✓ caching |
| **Guardrails / policy** [overlaps N3, SOFT here] | ◑ Presidio integration (buggy, W4) | ✓ **60+ guardrails** | ✓ guardrails + Bedrock Guardrails | ◑ policy/quota; thin DLP | ✓ guardrails | ✗/◑ minimal | ✓ PII/injection/regex | ✓ DLP profiles + content moderation (free) |
| **Audit logging** | ✓ request/key audit | ✓ | ✓ | ✓ | ✓ **immutable audit (SOC2/GDPR/HIPAA)** | ◑ usage logs | ✓ enterprise audit logs | ✓ configurable log retention/export |
| **Load-balancing / rate-limiting** | ✓ | ✓ | ✓ **6 LB algos** (advanced RL enterprise-gated) | ✓ **token rate-limiting is its core strength** | ✓ adaptive LB, <100µs @ 5k RPS | ✓ | ✓ | ✓ |
| **Multi-provider breadth** | ✓ 100+ providers / 2,500+ models | ✓ 1,600+ models | ✓ many | ◑ **16 providers** (v1.0, narrower) | ✓ 23+ providers / 1,000+ models | ✓ 300+ models | ✓ 400+ models | ✓ many |

---

## Per-tool role partition (qualified vs disqualified — role-scoped, NOT a global discount)

### LiteLLM (self-hosted) — the incumbent
- **Qualified roles:** sovereign router/gateway core (C3 plumbing), N2 offline-fallback host, N1 cost-tracking + virtual keys, observability (OTel), caching, LB/rate-limit, multi-provider shim (already KB #54/#70), **host for the N3 deny-by-default gate**. Covers the most loop-needs of any tool.
- **Disqualified roles:** none by construction. **Caveats:** N3 is only ◑ (its guardrail is the *mechanism*, not the code-class coverage — W4); C3 confidence-trigger absent (W6); **N2 supply-chain** — pin/vendor (Mar-2026 PyPI compromise, W6).
- **Reuse note:** already the chosen shim in the graph; W7a strengthens, not changes, that.

### Portkey-OSS (self-hosted; fully Apache-2.0 since Mar-2026)
- **Qualified roles:** router/gateway core, **guardrails-rich** policy layer (60+), caching (semantic), virtual keys/budgets, breadth (1,600+). The most *feature-complete* OSS gateway on paper.
- **Disqualified roles:** none structurally. **Caveat (sharp):** OSS **observability needs you to stand up your own logging infra** — the analytics that make it attractive partly live in the managed tier. A "platform" whose telemetry is gated is a weaker platform than it markets.

### Kong AI Gateway (self-hostable, but tier-gated)
- **Qualified roles:** enterprise routing/LB (6 algos), semantic caching, guardrails, token rate-limiting, key management.
- **Disqualified roles:** none structurally. **Caveat (sharp):** **fully self-hosted control+data plane and advanced token-rate-limiting are enterprise/paid** — for a sovereign, no-vendor-lock goal this re-introduces a commercial dependency. Best fit only if Kong is already the org's API platform.

### Envoy AI Gateway (self-hosted, CNCF/Apache, v1.0)
- **Qualified roles:** **best-in-class token rate-limiting + cost attribution** (per-route input/output/cached/reasoning), centralized upstream-credential management, OTel-native observability, MCP gateway, **tier-two ingress to a self-hosted serving cluster** (the only tool that touches C1's edge).
- **Disqualified roles:** none structurally. **Caveats:** narrower provider breadth (16); **no headline caching**; thinner DLP/guardrails than Portkey/Kong — weaker on the N3-mechanism column. K8s-centric (heavier to stand up than LiteLLM).

### Bifrost (self-hosted, Go, Maxim)
- **Qualified roles:** **strongest OSS governance story shipped in OSS (not enterprise-gated):** virtual keys + hierarchical budgets + immutable audit + Vault + native Prometheus/OTel; adaptive LB; very low overhead (<100µs @ 5k RPS, vendor-reported); native cluster mode (N4). Guardrails present.
- **Disqualified roles:** none structurally. **Caveats:** newer/less battle-tested than LiteLLM; perf numbers are vendor-reported (re-baseline). Same N3 ◑ ceiling as the rest (entity-based guardrails ≠ code-class boundary).

### OpenRouter (hosted middleman)
- **Qualified roles:** **frontier egress *target*** behind a local gate (W2/W5); breadth (300+) + BYOK + usage-accounting/analytics as a *reference* for what a self-hosted platform should expose.
- **Disqualified roles:** ⛔ **as the router on any N3 sensitive path** (sees prompt to route — W2/W4); ⛔ **as the N2 backbone** (it is the cloud dependency). +5.5%/5%-BYOK fee is an N1 + sovereignty cost.

### Requesty (hosted middleman)
- **Qualified roles:** reference for cost-optimization/governance features (per-user limits, cache-hit analytics, EU residency); possible egress target.
- **Disqualified roles:** ⛔ **as router on sensitive path** (managed-only, all traffic transits Requesty — W2); ⛔ as N2 backbone. No self-host path.

### Cloudflare AI Gateway (hosted exemplar)
- **Qualified roles:** reference exemplar — **$-denominated spend limits (2026), free DLP, analytics/logging, caching** are a strong feature *bar* to hold self-hosted options against; usable as an egress/analytics layer for **non-sensitive** traffic only.
- **Disqualified roles:** ⛔ **as router/gate on any N3 path** (W6 names it the disqualified-as-router exemplar — DLP runs in Cloudflare's cloud); ⛔ as N2 sovereign backbone.

---

## Candidate new capabilities / NFRs the platform lens surfaces (feed a D3 decomposition decision)

`shd` decomposed C1/C2/C3 + N1–N4. Grading the *whole platform* reveals **needs the loop will hit that the decomposition has not named.** Each is a candidate node, NOT a settled one:

1. **Spend observability & budget enforcement** — distinct from N1-as-routing-lever. Every platform ships per-key/team/user attribution + pre-spend caps; the loop needs this to *prove* N1, and to attribute escalation cost. **Candidate NFR.** (Cloudflare's $-denominated limits + Envoy's per-token-class attribution are the bar.)
2. **Provider key / secret management** — virtual keys + credential vaulting (Bifrost↔Vault, Envoy upstream-cred plane). A multi-provider escalation path *needs* a key-management story; `shd` hasn't named one. **Candidate NFR/capability.**
3. **Observability / tracing of the loop** — OTel spans per call (which model actually served, latency, tokens). Directly supports the **firewall's doc-claim-vs-demonstrated separation** and cost attribution (W5 `x-litellm-model-id`). **Candidate cross-cutting capability.**
4. **Response caching (exact + semantic)** as an N1 lever — Kong claims 40–70% cost cut; not in the decomposition. **Candidate NFR sub-lever under N1.**
5. **Audit trail of egress decisions** — Bifrost's immutable audit / Cloudflare's exportable logs. The N3 human-consent path (W4 #2) and the firewall both *need* an auditable record of what egressed and why. **Candidate capability — arguably part of N3's enforcement story.**
6. **Guardrails / policy-as-code as a first-class layer** — broader than N3 (prompt-injection, content policy, jailbreak). Currently folded into N3; the platforms treat it as a separate, reusable layer. **Candidate: split policy-layer out of N3.**
7. **Load-balancing / rate-limiting across local serving instances** — N4-adjacent; needed once C1 runs on >1 machine. Not decomposed. **Candidate NFR sub-lever under N4.**

---

## Synthesis (directional)

- **Covers the most of the loop:** **LiteLLM** and **Portkey-OSS** tie on raw column-count; **LiteLLM** wins net (incumbent in graph, breadth, no telemetry-gating). **Bifrost** is the strongest *governance-in-OSS* platform (audit/budgets/keys/OTel all shipped in OSS, not enterprise-gated) and the cleanest single-platform sovereign story if starting fresh.
- **Strongest multi-need self-hosted platform, honestly:** LiteLLM (reuse + breadth) or Bifrost (governance native). **Portkey's telemetry is partly managed-tier; Kong's full self-host + advanced features are enterprise-paid** — both weaker as *sovereign* platforms than they look. Envoy is the cost-attribution/rate-limit specialist, not the broadest.
- **"Extra features we'd otherwise build ourselves" (the platform dividend):** cost-tracking & attribution, virtual-key/secret management, OTel observability, caching, load-balancing/rate-limiting, audit logging — **six ops capabilities** that fall out of adopting *any* mature gateway. W6 sketched "LiteLLM core + 2 thin policy layers"; W7a shows the platform also hands us these six for free, so the **build surface is even smaller than W6 implied** — *and* it exposes six undecomposed loop-needs (above).
- **Hosted-class verdict (role-scoped, not a global zero):** OpenRouter/Requesty/Cloudflare are ⛔ as router/gate/N2-backbone on the sovereign path, but their cost/observability/spend-limit feature sets are the **bar** a self-hosted choice must clear; OpenRouter remains the one viable **frontier egress target** for non-sensitive escalation.

## The sharpest hard-vs-soft trap

**A do-everything platform that is mediocre at a HARD need is a trap — and here the trap is doubly baited.** LiteLLM/Portkey/Bifrost each cover ~12 of the loop's needs at convenience-grade — a genuine, bankable win for the SOFT columns (cost, keys, observability, caching, LB, audit, breadth: take the 80% reuse). **But the two needs that actually gate `shd` — N3 [HARD] and C3-confidence [HARD-ish] — are exactly where every platform is weakest:**
- **N3:** *every* platform's "guardrails / DLP" is **entity/PII/secret pattern-matching, best-effort, recall-bound** (and LiteLLM's Presidio guardrail has shipped a **silent no-op** — W4 #8359). None implements the **deny-by-default, code-class, fail-closed boundary** N3 requires. The platform's green "guardrails ✓" checkbox **is not** N3 satisfaction.
- **C3:** *every* platform's "routing" is **rule/cost/load-balance/error-failover**, never the **local-insufficiency / confidence trigger** the C3 ask names (W6 R2).

**So the trap is:** breadth (12 ✓ columns) makes it tempting to mark the platform "covers the loop" and treat its guardrail/routing checkboxes as closing N3 and C3. They do not. **Tag both N3 and the C3-trigger HARD; let the SOFT breadth be the win it is, but build the two thin HARD layers (W6 components B + C) on top — never let the platform's breadth paper over them.**

## Flags / could-not-verify
- All feature claims are **vendor-doc / review-reported**, not demonstrated by us. Bifrost's perf and Kong's "40–70% cost cut" are vendor numbers — re-baseline before relying.
- **Portkey OSS telemetry gating** and **Kong self-host/advanced-feature enterprise gating** are review-reported (mid-2026); verify the exact OSS/enterprise feature split against current licensing before selection — it changes the "sovereign platform" calculus materially.
- N3 ◑ ceiling is uniform across **all** self-hosted tools — none closes the code-class gap; consistent with W4/W6. The egress-gate's hard half remains a thin novel build, not a platform feature.
- Candidate capabilities (1–7) are **surfaced for a D3 decision**, not decomposed here — leader/curator's call.

## Citations (`{type, ref, title}`)
- `{repo, https://github.com/BerriAI/litellm, "LiteLLM — proxy/AI gateway: cost tracking, guardrails, loadbalancing, logging"}`
- `{doc, https://docs.litellm.ai/docs/proxy/users, "LiteLLM — budgets, rate limits, virtual keys per team/user"}`
- `{doc, https://docs.litellm.ai/docs/proxy/reliability, "LiteLLM — fallbacks / circuit-breaker / retries (N2)"}`
- `{issue, https://github.com/BerriAI/litellm/issues/8359, "LiteLLM Presidio guardrail silent no-op (N3 best-effort caveat)"}`
- `{repo, https://github.com/portkey-ai/gateway, "Portkey OSS AI Gateway — 1,600+ models, 60+ guardrails"}`
- `{review, https://chatforest.com/reviews/portkey-ai-gateway-review/, "Portkey fully open-sourced Mar-2026; OSS observability needs own logging infra"}`
- `{doc, https://developer.konghq.com/ai-gateway/, "Kong AI Gateway — semantic caching, guardrails, token rate-limiting"}`
- `{blog, https://konghq.com/blog/product-releases/ai-gateway-3-8, "Kong AI GW 3.8 — semantic caching + 6 LB algorithms"}`
- `{blog, https://www.truefoundry.com/blog/kong-gateway-pricing-architecture-an-analysis-for-ai-teams-2026-edition, "Kong fully-self-hosted control+data plane is enterprise/custom-priced"}`
- `{doc, https://aigateway.envoyproxy.io/docs/capabilities/, "Envoy AI Gateway — capabilities (token RL, provider fallback, OTel)"}`
- `{blog, https://tetrate.io/blog/envoy-ai-gateway-v1-0-release, "Envoy AI GW v1.0 — per-token-class cost attribution, 16 providers, upstream cred mgmt"}`
- `{repo, https://github.com/maximhq/bifrost, "Bifrost — adaptive LB, cluster mode, guardrails, virtual keys, <100µs overhead"}`
- `{doc, https://docs.getbifrost.ai/overview, "Bifrost — governance via virtual keys, hierarchical budgets, immutable audit, Vault, Prometheus/OTel"}`
- `{doc, https://openrouter.ai/docs/use-cases/usage-accounting, "OpenRouter — usage accounting, per-model/key spend, prompt-cache tokens"}`
- `{doc, https://www.datastudios.org/post/openrouter-pricing-and-byok-explained, "OpenRouter BYOK 5% fee; routing/analytics layer (hosted middleman)"}`
- `{doc, https://www.requesty.ai/, "Requesty — 400+ models, cost optimization, caching, guardrails, governance (managed-only)"}`
- `{doc, https://developers.cloudflare.com/ai-gateway/features/, "Cloudflare AI Gateway — analytics, caching, rate-limiting, logging, DLP"}`
- `{blog, https://blog.cloudflare.com/ai-gateway-spend-limits/, "Cloudflare AI GW — $-denominated spend limits (2026)"}`
- `{kb, unimatrix #70, "LiteLLM — self-hosted routing/egress backbone for C3 (shd-005)"}`
- `{kb, unimatrix #81, "Self-hosted routing-gate composition (LiteLLM core + escalation controller + deny-by-default gate)"}`
- `{kb, unimatrix #87, "Off-the-shelf clears no single tool — gap is ~70% composition (W6)"}`
- `{kb, shd #54, "Serving-protocol filter — non-Anthropic-native engines need a LiteLLM shim"}`
- Reuse: `findings-W2.md`, `findings-W4.md`, `findings-W5.md`, `findings-W6.md`.
