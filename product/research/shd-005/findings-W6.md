# shd-005 / W6 — Novel-approach gap analysis (does off-the-shelf routing meet ALL four bars?)

**Researcher:** shd-005-researcher-W6 · **Confidence-required:** directional · **Firewall:** doc-claim / benchmark-reported only — nothing demonstrated here, nothing `proven`. Every figure below is vendor-doc or community/paper-reported.

**Scope of this workstream (lighter survey):** the deep landscape is W2 (routers), W3 (harness-native), W4 (privacy gate). W6 asks one question against their field: **does any single off-the-shelf option meet ALL of {self-hosted/sovereign · confidence-gated triggering · enforceable N3 egress gate · graceful offline fallback}?** If not, sketch the *minimum* novel composition — and only if a real gap remains.

---

## 1. The four-bar test (the requirements)

| # | Bar | Source | What "meets it" means |
|---|---|---|---|
| R1 | **Self-hosted / sovereign** | N2 | Routing *logic* runs on owned HW; only the chosen frontier *call* egresses. Hosted-middleman routers (OpenRouter/Requesty/Portkey/Cloudflare AI Gateway) fail by construction — all traffic transits a third party. |
| R2 | **Confidence-gated triggering** | C3 anchor | Escalate to public *only when* a local-insufficiency signal **S** trips threshold **T** — and return. Decides *"did local actually fail this task,"* not *"which model is a-priori better."* |
| R3 | **Enforceable N3 egress gate** | N3 (HARD) | Deny-by-default boundary: sensitive code does **not** leave local unless *explicitly routed*. Must **fail closed**. Best-effort masking ≠ enforceable. |
| R4 | **Graceful offline fallback** | N2 | Offline / outage / no-key → fall back to local, never block. Router itself must not be a vendor dependency. |

---

## 2. Gap matrix — per leading off-the-shelf option

Legend: ✅ meets · ◑ partial / best-effort · ❌ missing or disqualifying.

| Option | Sovereignty class | R1 self-hosted | R2 confidence trigger | R3 enforceable egress gate | R4 offline fallback | Net gap |
|---|---|---|---|---|---|---|
| **LiteLLM proxy** (BerriAI, OSS) | self-hosted core | ✅ OSS, owned HW, OpenAI-compat, speaks local engines + frontier Claude | ❌ routing is rule / cost / load-balance / **semantic-similarity (embedding auto-route)** + **error-failover** fallbacks — *no* local-insufficiency / logprob / verification trigger | ◑ Presidio guardrail can **block** pre-call (deny action) → enforceable *mechanism* exists, but detection is **entity-based (PII/PHI/secrets)**, not "proprietary source code"; + **supply-chain risk**: PyPI v1.82.7/1.82.8 compromised Mar 2026 (clean v1.83.0, Mandiant review) → pin/vendor for N2 | ✅ fallbacks native — but trigger on **error**, not confidence | **R2 entirely; R3 the code-class half** |
| **RouteLLM** (LMSYS, OSS, ICLR'25) | self-hosted (decision layer) | ✅ OSS, BERT/MF router runs local, <10ms | ◑ *learned* quality/cost router, but trained on **Chatbot-Arena chat preference**; **OOD coding collapses to ~9–21%** (classifiers overfit training dist.). Picks model a-priori, not "did local fail." | ❌ no egress / privacy concept | n/a (decision layer only) | **R3 absent; R2 weak for code** |
| **Harness-native** (Roo/Cline · aider · Continue) | self-hosted | ✅ all BYOK + local Ollama | ❌ **manual / mode-based** model-switch (Code/Architect/Debug modes) or error-failover — not automatic confidence escalation | ❌ no deny-by-default block; harness sends whatever the active mode configures to whatever endpoint | ✅ local model via Ollama | **R2 (auto) + R3 both** |
| **Kong / Envoy / Bifrost AI Gateway** (OSS, Apache-2.0) | self-hosted | ✅ self-hostable egress gateways | ❌ governance/DLP/budget focus — no local-insufficiency trigger | ◑ **LLM-aware DLP inline + allow/denylist + blocking** = strongest off-the-shelf egress enforcement; still **entity/pattern-ML** detection, not code-semantic | ✅ | **R2 absent; R3 code-class half** |
| **Hosted aggregators** (OpenRouter, Requesty, Portkey, Cloudflare AI Gateway) | **hosted middleman** | ❌ all prompts+code transit a third party | (varies) | ❌ by construction | ❌ new load-bearing vendor | **DISQUALIFIED as router** — usable only as a frontier *target* behind the gate, never as the router |

**No single off-the-shelf option clears all four bars.** Every self-hosted option is missing **R2 (confidence trigger)**; the egress gate (R3) has a strong *mechanism* off-the-shelf (LiteLLM Presidio block / Kong-Envoy DLP) but a *coverage gap* — none classifies "proprietary source code" as sensitive; they classify PII/secrets.

---

## 3. Verdict — off-the-shelf does NOT suffice as a single tool, but the gap is ~70% composition, not invention

The cheapest-correct answer is **compose existing pieces**, and most of the stack *is* off-the-shelf:

- **Sovereign router core, plumbing, offline fallback, PII/secret scrubbing** → **LiteLLM proxy** (reuse — already named in KB #54 as the required shim for non-Anthropic-native engines). R1 ✅, R4 ✅, R3-mechanism ◑.
- The **only genuinely-missing pieces** are two *thin policy layers*, neither requiring a trained-from-scratch model (explicitly out of scope per SCOPE):
  1. **R2 — a confidence / local-insufficiency trigger.** Nothing off-the-shelf supplies it for coding. RouteLLM is nearest but OOD-fragile; the 2026 *Agent-as-a-Router* work corroborates that **execution-grounded feedback** (sandbox run / test / AST / verifier), not pre-trained classifiers, is what makes coding routing work ("information deficit is the bottleneck, not reasoning"). → the leading signal is **harness-observable** (test/compile fail, retry exhaustion, tool-call failure — W1), which **no router ingests natively**.
  2. **R3 — the code-aware, deny-by-default half of the egress gate.** Off-the-shelf gives entity-based DLP; N3 needs a *coarser, explicit* boundary (default-local; egress only on explicit route/marker or repo-path allowlist), failing closed.

So: **NOT "off-the-shelf suffices," but also NOT "build a router from scratch."** The minimum novel approach is a **small composition shim**: an off-the-shelf LiteLLM-proxy core + two thin self-built policy components + one wiring layer.

---

## 4. Minimum novel-router sketch (only the gap, nothing more)

```
                    [confidence signal S from harness/local engine]
                                     │
   C2 harness ──req──► (B) Escalation Controller ──decision──► (A) LiteLLM proxy core
   (Roo/aider/CC)                    │  escalate? y/n vs T        │   ├─ local engine (C1 stack)   ← default
                                     │                            │   └─ frontier (Claude) ──► (C) Egress Gate ─► public
                                     └─ no-key/offline ─► force-local (R4)        deny-by-default, fail-closed
```

| Component | Off-the-shelf? | What it must do | Buildability | Risk |
|---|---|---|---|---|
| **(A) Sovereign router core** | **Reuse — LiteLLM proxy** | Run on owned HW; OpenAI-compat; route to local C1 stack + frontier Claude; native error-failover + offline fallback (R1, R4) | **Trivial** (config). Pin/vendor the dependency (N2 supply-chain) | **Low** |
| **(B) Escalation controller** *(the genuinely-missing piece)* | **Build (thin policy)** | Ingest local-insufficiency signal S (lead bet: **harness-observable** test/compile/retry/tool-call failure; fallback: local logprob/self-consistency). Decide escalate-y/n vs calibrated **T**. On no-key/offline → force-local, never block (R4). | **Moderate** — a policy wrapper, not a model. But **T-calibration + signal reliability is unproven** | **HIGH — determining constraint** |
| **(C) Egress gate** *(N3)* | **~70% reuse + thin novel** | Deny-by-default boundary at LiteLLM egress hook. Egress only if (i) **explicitly routed/marked-shareable** AND (ii) passes scrub. Reuse Presidio/DLP for secrets/PII; add **coarse code-sensitivity policy** (sensitive repo/path → deny). **Fail closed** on error/uncertainty. | **Moderate** — Presidio/guardrail hook gives ~70%; deny-by-default policy + repo-path class is the ~30% novel | **Medium** — enforceability is *demonstrable* (block an unrouted payload); "code sensitivity" is fuzzy → keep it **coarse/explicit (allowlist/marker), not ML-classified** |
| **(D) Trigger→route wiring** | **Build (glue)** | Carry B's decision + the harness signal into A's route selection (LiteLLM picks by *its own* logic; it does not ingest external confidence) and merge the routed result back into the local loop | **Low–moderate** | **Low** |

**Deliberately excluded** (avoid over-building): training a custom router model (SCOPE out-of-scope; RouteLLM's OOD collapse argues against it); a hosted middleman anywhere in the sensitive path; general repo-wide secret-scanning beyond the egress boundary.

---

## 5. Determining constraint + key buildability risk

**The determining constraint is R2 — the confidence/local-insufficiency trigger (component B).** Everything else is config-grade reuse (A, D) or ~70%-reuse-plus-coarse-policy (C). The open, unproven question is whether a **reliable** local-insufficiency signal exists for *coding* tasks:

- Learned routers (RouteLLM-class) **collapse OOD on code** → the leading bet is **execution-grounded / harness-observable hard signals** (test fails, compile errors, retry exhaustion), corroborated by the 2026 Agent-as-a-Router result that execution feedback beats classifier reasoning.
- This directly carries **shd-002 L1**: doc-claims of "smart/automatic routing" are the silent-failure mode. Trigger reliability **cannot be asserted here** — it is exactly what the shd-006 POC must demonstrate (S trips T only when local actually failed, and never otherwise).

**Net:** off-the-shelf gives a sovereign core + an enforceable egress *mechanism* + offline fallback for free; the novel surface is two thin policy layers; the risk is concentrated almost entirely in whether the trigger signal is reliable enough to trust — a question this directional scope **flags, does not settle.**

---

## Citations
- `{type: web, ref: https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2, title: "LiteLLM — Presidio PII/PHI masking guardrail (block/mask, pre-call)"}`
- `{type: web, ref: https://docs.litellm.ai/docs/proxy/auto_routing, title: "LiteLLM — Auto Routing (embedding/semantic-similarity model selection)"}`
- `{type: web, ref: https://docs.litellm.ai/docs/proxy/reliability, title: "LiteLLM — Fallbacks / reliability (error-triggered failover)"}`
- `{type: web, ref: https://github.com/BerriAI/litellm, title: "BerriAI/litellm — self-hosted AI gateway (incl. Mar-2026 supply-chain note)"}`
- `{type: web, ref: https://github.com/lm-sys/RouteLLM, title: "LMSYS RouteLLM — learned router framework (BERT/MF, Chatbot-Arena trained)"}`
- `{type: paper, ref: arxiv.org/abs/2406.18665, title: "RouteLLM: Learning to Route LLMs with Preference Data (ICLR 2025)"}`
- `{type: paper, ref: arxiv.org/html/2606.22902, title: "Agent-as-a-Router: Agentic Model Routing for Coding Tasks (2026) — execution-grounded feedback, OOD classifier fragility"}`
- `{type: web, ref: https://www.clawrouters.com/blog/best-open-source-llm-router, title: "Open-source LLM router comparison — RouteLLM OOD coding ~9–21%"}`
- `{type: web, ref: https://developers.cloudflare.com/ai-gateway/features/dlp/, title: "Cloudflare AI Gateway DLP (hosted middleman — disqualified-as-router exemplar)"}`
- `{type: web, ref: https://www.getmaxim.ai/articles/best-self-hosted-ai-gateway-in-2026/, title: "Self-hosted AI gateways 2026 — Kong / Envoy / Bifrost (Apache-2.0, DLP + allow/denylist)"}`
- `{type: web, ref: https://www.pkgpulse.com/guides/cline-vs-roo-code-vs-aider-open-source-ai-coding-agents-2026, title: "Cline/Roo/aider — per-mode model selection, BYOK + local Ollama"}`
- `{type: kb, ref: shd #54, title: "Serving-protocol filter — non-Anthropic-native engines need a LiteLLM shim"}`

## Flags
- **Lighter survey by design** — deep router/harness/gate landscapes are W2/W3/W4; W6 only ran the gap test + sketch.
- **Could not verify:** that any coding-specific local-insufficiency signal is *reliable* (the determining constraint) — unprovable at this altitude; it is the shd-006 POC bar.
- **N2 supply-chain:** the reused LiteLLM core needs version-pinning / vendoring (Mar-2026 PyPI compromise) to avoid re-introducing a vendor dependency.
