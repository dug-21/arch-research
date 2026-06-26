# FINDINGS — shd-005 / W5: Frontier targets, return path, offline fallback & cost

**Agent:** shd-005-researcher-W5 · **Date:** 2026-06-26 · **Status:** read-only research; nothing
proven. Evidence is **doc-claim / vendor-reported**, not demonstrated by us. Pricing/throughput
numbers are **reported**, re-verify before any budget commitment.

**Scope frame (C3 / N2):** the local loop is load-bearing; the frontier target is an **escalation
fallback, never load-bearing**. N2 (no-outage / graceful offline fallback) is HARD here: the system
must degrade to local, never block, when the target is unreachable. Directionally, the **determining
constraint is the harness API shape**, not the model menu — the Claude Code harness speaks the
Anthropic Messages API, so the cleanest target and the cleanest return path are the ones that keep
that shape end-to-end.

---

## 1. Targets — realistic escalation destinations

Ranked for *this* run (Claude Code harness, sovereignty-first, frontier as fallback).

| Rank | Target | How reached from a self-hosted router / client | API shape | Reported price (input/output $/MTok) | Evidence |
|---|---|---|---|---|---|
| **1 (default)** | **Anthropic Claude frontier** | Native Messages API. Point harness `ANTHROPIC_BASE_URL` at a gateway serving `/v1/messages`, or direct to `api.anthropic.com`. | **Anthropic Messages** (`/v1/messages`, `anthropic-version` header) — same shape the harness already emits | Fable 5 (most capable) **$10/$50**; Opus 4.8 **$5/$25**; Sonnet 4.6 **$3/$15**; Haiku 4.5 **$1/$5** | claude-api skill (cached 2026-06-04) corroborated by Anthropic pricing reporting |
| 2 | OpenAI (GPT-5.x) | OpenAI `/v1/chat/completions`; reached via router translation from Messages shape | OpenAI Chat Completions | GPT-5.5 **$5/$30** (cached-in $0.50); GPT-5.4 **$2.50/$15** | reported |
| 3 | Google Gemini | Gemini API; router translation | Gemini (or via aggregator) | Gemini 3.1 Pro **$2/$12** (≤200K; $4/$18 above); 3.5 Flash **$1.50/$9** | reported |
| 4 | **Hosted aggregator (OpenRouter)** — as a *target*, not a dependency | OpenAI-compatible `/v1/chat/completions`, single endpoint to 300+ models / 60+ providers | OpenAI Chat Completions | pass-through near cost **+ ~5.5% platform fee**; own fallback/routing built in | reported |

**Key structural finding (the determining constraint):** the harness is **Anthropic-native**, so the
default target (Claude) needs **zero translation** — Messages-shape in, Messages-shape out. Every
non-Anthropic target (OpenAI, Gemini, OpenRouter) requires a **shape translation** somewhere. That
translation is exactly what a self-hosted gateway provides, which is why the gateway — not the model
choice — is the load-bearing integration decision. OpenRouter is attractive breadth but reintroduces
a **vendor in the load path + 5.5% fee + their routing opacity**, which is in tension with N1/N3
sovereignty if used as anything more than an optional escalation target.

## 2. Integration + return path (how the escalated result merges back)

**Recommended topology:** harness → **self-hosted gateway (Anthropic-shaped front door)** → {local
model | frontier target}. LiteLLM is the concrete, OSS, self-hostable instance of this pattern (doc-claim).

- **Front door (return-path-preserving):** the gateway exposes **`/v1/messages`** (Anthropic
  Messages spec). The harness sets `ANTHROPIC_BASE_URL=<gateway>`; on startup Claude Code calls
  `GET /v1/models` against it and lists each returned model in the picker "From gateway." This means
  **the harness never knows it left the Messages shape** — the escalated answer returns as an
  ordinary Messages response and the local loop continues uninterrupted. This is the clean merge-back:
  same wire shape in and out, no adapter in the harness.
- **Behind the door:** the gateway routes the request to local (default) or frontier (escalation),
  translating to OpenAI/Gemini/DeepSeek shape when the chosen target isn't Anthropic, and translating
  the response **back** to Messages shape. Reported response header `x-litellm-model-id` (and Claude
  Code's "From gateway" label) discloses *which* model actually served — useful for the firewall's
  doc-claim/demonstrated separation and for cost attribution.
- **Native alternative for the Anthropic-only case:** Anthropic's own **server-side `fallbacks`
  parameter** (`betas:["server-side-fallback-2026-06-01"]`, `fallbacks:[{model:"claude-opus-4-8"}]`)
  re-serves a *refused/declined* Claude request on a fallback Claude model **inside the same call**,
  with credit-style repricing. This is an in-shape, return-path-native fallback **but only for
  Anthropic→Anthropic and only on refusal** — it does NOT cover outage/offline/no-key, and is not
  available on Bedrock/Vertex/Foundry. Treat it as a complement (handles policy refusals), not the N2
  mechanism. (Source: claude-api skill.)

## 3. Offline fallback (N2) — graceful degradation patterns

The gateway is where N2 lives. Reported LiteLLM mechanics (doc-claim, `docs.litellm.ai`), which
generalize to the pattern regardless of implementation:

- **Fallbacks (in-order, fail *down* to local):** `fallbacks=[{frontier: [local]}]` — on any error
  (429/500/connection) the request is retried on the next group in order. For sovereignty the order
  is inverted from the usual: **local is the terminal fallback**, so an unreachable frontier degrades
  *to local* rather than failing. `default_fallbacks:[local]` gives a universal safety net.
- **Retries with backoff:** `num_retries` on the same group before falling over, fixed + exponential
  backoff.
- **Circuit-breaker / cooldown:** `allowed_fails` + `cooldown_time` take a failing target out of
  rotation; on 429 the deployment is cooled down immediately and routing skips straight to the next
  tier without burning the retry budget. This is the "never block" guarantee — a dead frontier is
  removed from the path within one failure window.
- **Timeouts:** `request_timeout` caps call duration so a hanging frontier can't stall the loop.
- **Typed fallbacks:** `context_window_fallbacks` and `content_policy_fallbacks` route those specific
  error classes separately (e.g. context-exceeded → larger-context local model).

**Cleanest offline-fallback pattern for shd:** gateway with **(local as `default_fallbacks` terminal
target) + per-target cooldown circuit-breaker + short `request_timeout`**. Net behavior: no-key /
outage / offline all collapse to "target removed from rotation, request served locally, loop
continues." This satisfies N2 (never block, graceful) and keeps the public LLM strictly
non-load-bearing by construction — if the frontier is gone, the system still runs, just less capable.

## 4. Cost posture (N1)

- **Escalation is the cost lever.** Token-cost exposure is bounded by *how much traffic escalates*,
  not by frontier list price. If routing keeps the frontier as a true fallback (only escalate on
  local-model low-confidence / failure / explicit hard tasks), escalated share is small and frontier
  spend is a tail cost, not a base cost.
- **Controls (reported):** gateway-level **cost tracking per request/key**, per-key budgets/caps,
  rate limits, and routing rules that gate escalation. Anthropic-side: **batch −50%**, **prompt
  caching −~90% on cached input**, effort controls, and Fast Mode pricing tiers — all reduce
  per-escalation cost. OpenRouter adds a **5.5% platform fee** on top of pass-through (a cost *and* a
  sovereignty cost).
- **Cheapest-viable frontier ladder (reported $/MTok):** Haiku 4.5 $1/$5 < Gemini Flash $1.50/$9 <
  Gemini Pro $2/$12 ≈ GPT-5.4 $2.50/$15 < Sonnet 4.6 $3/$15 < Opus 4.8 $5/$25 < GPT-5.5 $5/$30 <
  Fable 5 $10/$50. Default escalation target (Claude) sits mid-ladder; a budget-tiered escalation
  (escalate to Sonnet first, Opus/Fable only on hardest) is the obvious N1 control.

---

## Biggest risk (cost OR outage)

**Outage risk dominates and it is an *ordering* risk, not a model risk.** The whole N2 guarantee hinges
on the gateway's fallback **order putting local last** and the circuit-breaker firing fast. If the
gateway is misconfigured to fail *up* (local → frontier) or to retry a dead frontier instead of
cooling it down, a frontier outage/no-key event **blocks the loop** — the exact N2 failure. Secondary:
inserting a hosted aggregator (OpenRouter) as a convenience target quietly puts a vendor + 5.5% fee
back in the load path, eroding N1/N3 sovereignty. Cost tail risk (runaway escalation) is real but
**controllable** via per-key budget caps + escalation gating; the outage-ordering risk is the one that
can violate a HARD NFR.

**Could not verify (flags):** (1) all pricing/throughput is vendor/aggregator-reported, not measured by
us — re-baseline before budgeting; (2) LiteLLM fallback/cooldown behavior is doc-claim — the
local-as-terminal-fallback + circuit-breaker config must be **demonstrated by a POC** before N2 is
considered settled; (3) Messages-shape round-trip fidelity through the gateway for *non-Anthropic*
targets (tool-use, thinking blocks, streaming) is unverified and is the most likely place a merge-back
breaks. Completion of N2/C3 is a later validated POC, not this file.

## Citations
- {type: skill, ref: claude-api (bundled, cached 2026-06-04), title: Claude model IDs, pricing, server-side fallbacks parameter}
- {type: doc, ref: https://docs.litellm.ai/docs/proxy/reliability, title: LiteLLM Fallbacks (fallbacks/default_fallbacks/context_window/content_policy, cooldown, retries, timeout)}
- {type: doc, ref: https://docs.litellm.ai/docs/anthropic_unified/, title: LiteLLM /v1/messages (Anthropic Messages spec) endpoint}
- {type: doc, ref: https://docs.litellm.ai/docs/tutorials/claude_responses_api, title: Claude Code Quickstart — ANTHROPIC_BASE_URL, gateway /v1/models discovery}
- {type: doc, ref: https://docs.litellm.ai/docs/providers/anthropic, title: LiteLLM Anthropic provider — custom api_base /v1/messages suffix handling}
- {type: doc, ref: https://openrouter.ai/pricing, title: OpenRouter — OpenAI-compatible aggregator, fallback routing, ~5.5% fee}
- {type: report, ref: https://platform.claude.com/docs/en/about-claude/pricing, title: Claude API pricing 2026 (reported)}
- {type: report, ref: https://developers.openai.com/api/docs/pricing, title: OpenAI GPT-5.x pricing 2026 (reported)}
- {type: report, ref: https://ai.google.dev/gemini-api/docs/pricing, title: Gemini API pricing 2026 (reported)}
