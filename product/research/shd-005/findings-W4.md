# Findings — W4: Privacy-preserving egress gate (N3, the hard NFR)

**Run:** shd-005 · **Workstream:** W4 · **Agent:** shd-005-researcher-W4 (read-only)
**Date:** 2026-06-26
**NFR under test:** **N3 — "sensitive code never leaves local unless explicitly routed"** (hard). Secondary: N2 (no-outage), N1 (cost).
**Evidence discipline:** every row tags *enforces* vs *best-effort*; claims are **doc-claim** or **benchmark-reported**, never "proven." Research moves structure, not status.

---

## Bottom line (directional)

N3 has **two architecturally distinct readings**, and they are not equally enforceable:

- **(A) "Sensitive code never leaves at all"** — a *deny-by-default boundary* decision: this repo / path / classification is local-only, period. **This is enforceable** with a hard guarantee, because it is a binary routing/network decision, not a content judgment.
- **(B) "Sensitive *content within* an otherwise-routed prompt is scrubbed before egress"** — secret/PII/code redaction. **This is best-effort only.** It rests on detector *recall*, and for source code the redaction is semantically lossy. It can reduce leakage; it **cannot guarantee** "never leaves."

**The determining constraint** is therefore not *which scanner* — it is **where the gate sits relative to the router, and whether the router is local or hosted.** Any redaction/policy gate is only as strong as its position: it must sit **on-host, upstream of the first network hop, and own (terminate) the TLS connection.** A **hosted router (OpenRouter and equivalents) placed upstream of the gate defeats N3 outright** — it receives the raw prompt *in order to route it*, so it has already seen the sensitive bytes before any gate downstream of it runs.

---

## The placement principle (load-bearing for every row below)

For a gate to enforce anything, the sensitive bytes must pass *through* it before leaving the machine. Two ways that happens:

1. **The gate is the LLM endpoint the agent talks to** (a local reverse-proxy / shim, e.g. self-hosted LiteLLM with a pre-call guardrail). The agent points at `localhost`; the gate scrubs, then makes the outbound call itself.
2. **The gate is a transparent forward proxy** (`HTTP(S)_PROXY` / network egress firewall). To read HTTPS bodies it must **terminate TLS via a locally-trusted MITM CA** (mitmproxy-style) — otherwise it sees only the destination host (`api.openai.com`), not the payload, and can do host-allowlisting but **not** content redaction. [mitmproxy docs; AWS/GCP NGFW TLS-inspection]

**Corollary — the hosted-router trap:** if the topology is `agent → hosted router (OpenRouter) → provider`, the gate cannot live "after" the router without the router already having the plaintext. OpenRouter's own docs are explicit: *"OpenRouter sees the prompt to route and log usage … the downstream provider receives the prompt to generate the response."* Default is no-logging, and a Zero-Data-Retention mode exists, **but ZDR is a retention/contract promise, not a no-exposure guarantee** — the bytes still transit a third party. For a *sovereignty* goal (shd) and a *hard* N3, **a hosted router is disqualified-for-sensitive as the egress point**; the router that the gate fronts must be **local (self-hosted LiteLLM / OpenHands-style local shim), with hosted *providers* reached only on the explicitly-routed path.**

---

## Privacy-gate map

| # | Approach | Enforces vs best-effort | Placement in flow | Failure mode (what slips through) | Composition w/ router — incl. hosted-router defeat |
|---|---|---|---|---|---|
| 1 | **Hard local-only / deny-by-default boundary** (network egress firewall + allowlist; classify repo/path as `local-only`; route decision = binary) | **Enforces** (the only true hard guarantee for N3-(A)) | At the routing decision *and* at the OS/network egress layer (deny all outbound to frontier hosts unless an explicit allow is granted for a classified-routable request) | Misclassification at the *source* (a sensitive file tagged routable); allow-rule too broad (whole host allowed vs per-request); bypass via a non-proxied process | **Strongest composition:** router only ever sees requests already cleared as routable. Independent of scanner recall. Hosted router still disqualified — but with deny-by-default, sensitive material never enters the routable channel in the first place. |
| 2 | **Explicit human-consent routing** (gate blocks → surfaces a diff of exactly-what-would-egress → human approves per-request) | **Enforces** the *"unless explicitly routed"* clause directly; best-effort on what the human notices | Synchronous interrupt at the gate, before the outbound call | Consent fatigue / rubber-stamping; human can't eyeball a 50KB payload for an embedded secret; no machine guarantee | Composes well with a **local** router (LiteLLM pre-call hook can pause for approval). Meaningless if a hosted router already has the bytes. Pairs with #1 (consent is the "explicit route" act). |
| 3 | **Secret/credential scanners as egress filter** (gitleaks / trufflehog / detect-secrets rules; **llm-redactor** = local transparent proxy, 100+ types via Gitleaks-compatible rules) | **Best-effort** (recall-bound) | Forward proxy (TLS-terminating) or pre-call hook | **False negatives are the whole ballgame:** high-entropy/novel/custom credentials, secrets split across lines, non-pattern secrets (internal hostnames, proprietary algorithms). detect-secrets ~0–5% FP w/ allowlist; gitleaks ~5–15% FP; trufflehog verifies live creds to cut FP — *none publish a recall=100% claim* [benchmark-reported, appsecsanta/arXiv 2307.00714]. Verification (trufflehog) reduces FALSE POSITIVES, does nothing for false negatives. | Good as a **defense-in-depth layer inside a local router** (llm-redactor sits at `HTTP(S)_PROXY`; LiteLLM proxies a pre-call scan). **Cannot be the sole N3 control.** Defeated entirely if placed downstream of a hosted router. |
| 4 | **PII/code redaction & abstraction** (Microsoft Presidio regex+NER; PII Shield privacy-proxy; LiteLLM Presidio guardrail, BLOCK or MASK, self-hosted analyzer+anonymizer containers) | **Best-effort** | Pre-call guardrail in a **local** proxy (LiteLLM `pre_call`) | Presidio tuned for *PII*, not code: **misses domain-specific identifiers, secrets embedded in code/config, structural cues** [benchmark-reported, arXiv PlanTwin / RAG-redaction work]. Known LiteLLM bugs where the Presidio guardrail did not scrub the effective request (issues #8359, #6247, #12898) — **the masking silently no-ops.** | Self-hosted Presidio + self-hosted LiteLLM keeps redaction on-host. A hosted router upstream still sees pre-redaction bytes. |
| 5 | **Data-classification policy gate** (OPA / policy-as-code: deny-by-default, fail-closed; decide routable vs local per request based on labels) | **Enforces the decision**, given trustworthy input labels (garbage-in caveat) | Policy decision point in front of the egress call; OPA fails *closed* if unavailable | Only as good as the **classification feeding it** — if the input isn't reliably labeled sensitive, the policy can't catch it. OPA doesn't *detect* sensitivity, it *acts on* a label. | Excellent with a local router (LiteLLM/OpenHands call OPA pre-egress). Implements #1's allow/deny and #2's consent as code. Hosted router still bypasses it unless the gate runs first. |
| 6 | **Hosted AI-security/DLP gateway** (aidlp, aisecuritygateway, Data443; AI-gateway-as-DLP) | **Best-effort** content scan **+ off-host trust** | A proxy that may be cloud-hosted | Same recall limits as #3/#4, **plus** if the gateway itself is hosted it is *another third party seeing plaintext* — directly contradicts sovereignty | **Disqualified-for-sensitive when hosted.** Only admissible if run fully self-hosted on the local boundary (then it collapses into #3/#4). |

---

## How the rows compose into an N3-satisfying topology (directional)

```
agent (Claude Code / OpenHands)
   │  points at localhost only
   ▼
[ LOCAL gate ]  =  self-hosted LiteLLM/shim  +  classification policy (OPA, deny-by-default, #5)
   │                + secret-scan (#3) and PII/code redaction (#4) as best-effort layers
   │                + human-consent interrupt (#2) on the "explicitly routed" path
   ├──► local model (default; sensitive stays here — satisfies N3 by never leaving)   ← #1 hard boundary
   └──► frontier PROVIDER  (only for requests classified routable AND consented)
        ▲
        └─ NO hosted router in this path. A hosted router here = N3 violated.
```

- **Enforcement comes from #1 + #5 + #2** (binary boundary + policy + consent). #3/#4 are *risk-reduction inside the routable channel*, never the guarantee.
- **The router must be local.** This aligns with the existing graph: shd already favors a **self-hosted LiteLLM shim** for serving (graph node #54 "rest need a LiteLLM shim"; #12 local `/v1/messages` shim) — the same local proxy is the natural host for the egress gate. Reusing it satisfies N2 (no extra hosted dependency to outage) and N1 (no per-call hosted-gateway cost).

---

## Sharpest failure mode found

**Redaction of source code is semantically lossy in a way that structurally forbids a hard guarantee.** Unlike a phone number, code cannot be replaced with a stable placeholder without destroying the structural/data-flow relationships the LLM needs to be useful — "source code demands strict syntactic integrity … structural dependencies … which makes general redaction techniques ineffective for code" [benchmark-reported]. So you face a forced choice: **redact aggressively and the model output is useless, or redact lightly and proprietary logic leaks.** Worse, the failure is **silent** — a missed secret or un-abstracted algorithm produces a *successful* LLM call, no error, and is only discoverable in an after-the-fact audit log (llm-redactor's `detections.jsonl`). And in LiteLLM specifically, the Presidio guardrail has shipped bugs where it **passed the request through unmasked while reporting success** (#8359). **Conclusion: any N3 design that leans on content scrubbing as its primary control is best-effort and should be flagged `disqualified-for-sensitive` as a *sole* guarantee.** The only thing that *enforces* "sensitive code never leaves" is a **deny-by-default boundary that classifies at the source and never lets sensitive material enter the routable channel** — content scrubbing is defense-in-depth on top, not the wall itself.

---

## Flags

- **Disqualified-for-sensitive (as a sole/primary N3 control):** all content-redaction approaches (#3, #4, #6) — recall-bound, code-redaction lossy, fails silently.
- **Disqualified-for-sensitive (topology):** any **hosted router/gateway placed upstream of the gate** (OpenRouter as egress point; hosted DLP gateways) — sees plaintext before the gate; ZDR is a contract promise, not no-exposure. The router fronted by the gate must be **local**.
- **Could not verify:** no tool publishes a recall figure approaching 100% for secret detection; "100+ secret types" (llm-redactor) is a *type-count* claim, not a recall claim. Treat all detector coverage as doc-claim.
- **Open for W-other / curator:** the *classification* input that #1/#5 depend on (how a repo/path/file gets reliably labeled `local-only` vs `routable`) is the real weak link and is upstream of this workstream — worth a dedicated probe.

---

## Citations (`{type, ref, title}`)

- `{doc, https://github.com/WangYihang/llm-redactor, "LLM-Redactor — transparent local egress proxy, Gitleaks-compatible rules, detections.jsonl audit"}`
- `{doc, https://github.com/fabriziosalmi/aidlp, "aidlp — DLP proxy for LLM endpoints, FlashText + Presidio/SpaCy parallel redaction"}`
- `{doc, https://github.com/aisecuritygateway/aisecuritygateway, "AI Security Gateway — self-hosted proxy, redact PII/secrets, route to any provider"}`
- `{doc, https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2, "LiteLLM — Presidio PII/PHI masking guardrail (pre_call, BLOCK/MASK)"}`
- `{issue, https://github.com/BerriAI/litellm/issues/8359, "LiteLLM bug — Presidio guardrail doesn't scrub effective request/response (silent no-op)"}`
- `{doc, https://microsoft.github.io/presidio/, "Microsoft Presidio — regex + NER PII detection/anonymization framework"}`
- `{doc, https://techcommunity.microsoft.com/blog/azuredevcommunityblog/introducing-pii-shield-a-privacy-proxy-for-every-llm-call/4514726, "PII Shield — privacy proxy, placeholder swap + reversible de-anonymization"}`
- `{benchmark, https://appsecsanta.com/secret-scanning-tools/gitleaks-vs-trufflehog, "Gitleaks vs TruffleHog 2026 — FP rates, trufflehog live-credential verification"}`
- `{paper, https://arxiv.org/pdf/2307.00714, "A Comparative Study of Software Secrets Reporting by Secret Detection Tools"}`
- `{paper, https://arxiv.org/pdf/2603.18377, "PlanTwin — Privacy-Preserving Planning Abstractions for Cloud-Assisted LLM Agents (Presidio misses code-embedded secrets/structural cues)"}`
- `{doc, https://openrouter.ai/docs/guides/privacy/provider-logging, "OpenRouter — sees prompt to route; downstream provider receives prompt; default no-log"}`
- `{doc, https://openrouter.ai/docs/guides/features/zdr, "OpenRouter — Zero Data Retention (retention promise; bytes still transit third party)"}`
- `{doc, https://www.openpolicyagent.org/docs, "Open Policy Agent — policy-as-code, fail-closed/deny-by-default, egress allow/deny"}`
- `{doc, https://docs.mitmproxy.org/stable/concepts/how-mitmproxy-works/, "mitmproxy — TLS interception requires locally-trusted MITM CA to read HTTPS bodies"}`
- `{doc, https://docs.cloud.google.com/firewall/docs/about-tls-inspection, "GCP NGFW — egress HTTPS TLS inspection via managed CA (host vs body visibility)"}`
- `{doc, https://data443.com/blog/ai-gateway-vs-dlp-vs-waf-securing-llm-traffic-explained/, "AI Gateway vs DLP vs WAF for LLM traffic"}`
