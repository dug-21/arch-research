# shd-006 — Validated POC: the sovereign confidence-gated, egress-enforcing routing layer

**Status:** SCOPE (staged — awaits gate-1 scope approval to run)
**Goal(s):** `shd` (primary, #3) · **contributes to** platform-vision `#92` (the wedge)
**Capability target(s):** **C3 — route each task to the best-fit model under sovereignty/security/observability constraints** (#103) · **proof-gate for platform wedge #93** (auditable sovereign boundary)
**Confidence-required:** **validated** (this scope spends real compute and moves status to `proven`/`partial` on a demonstrated-by-us artifact)
**Phase / area:** routing / feasibility
**Cycle topic / Issue:** shd-006

Governing NFRs: N1 cost · **N2 resilience/offline** · **N3 sensitive-code-local (HARD)** · N4 multi-machine · #98 observability/audit · #99 cost-governance.

---

## The question

Build and demonstrate the recommended C3 composition (#81) — a **self-hosted gateway core (LiteLLM/Bifrost) + a confidence trigger + a deny-by-default egress gate** — on a real coding task, and prove the three things no off-the-shelf tool ships.

> Does a sovereign routing layer route to a public LLM **only when local is insufficient**, **block an unrouted sensitive payload**, and **fall back to local when offline** — demonstrated by us, on a real task?

## Why it matters

This is where shd-005's directional landscape becomes proof. C3 (#103) stays `missing` until this artifact exists; the same artifact is the **proof-gate for the platform wedge #93** (auditable sovereign boundary). It is the first exercise of the feasibility/firewall machinery on this lineage.

## Hypotheses & kill criteria  *(goal-owner adjustment 1 — R2 is a bet, not a tuning knob)*

- **H1 (R2 — THE load-bearing bet): a reliable local-insufficiency confidence trigger for *coding* exists.** Lead signal: harness-observable execution signals (test/compile/retry/tool-call failure — #75), not learned classifiers (which collapse OOD on code, ~9–21%).
  **KILL CRITERION:** if no signal routes *only-when-insufficient* above an agreed precision/recall bar on a held-out task set (i.e. it escalates when local would have succeeded, or fails to escalate when local fails), **R2 is unproven → the routing-product thesis has no floor**; report the negative, do not paper over it. This is where shd-006 is most likely to fail, and that failure is a valid, valuable outcome.
- **H2: the egress gate enforces N3 as a hard boundary.** Deny-by-default, fail-closed; egress only on explicit route/allowlist.
- **H3: the loop degrades gracefully offline (N2).** Frontier unreachable/no-key → fall back to local, never block.

## Build (feasibility)

- Stand up the composition: **LiteLLM (or Bifrost) core** + a thin **escalation controller** (consumes H1's signal vs threshold T) + a **deny-by-default egress gate** on the gateway's pre-call hook + **local-as-terminal fallback** (N2). Wire to a local model (C1 — modest model is sufficient; insufficiency is *easier* to trigger on a small model) and a frontier target (Claude via the Anthropic-shaped path).
- Instrument per #98 (every model call + egress decision recorded) — the audit trail is part of the wedge proof.

## Proof bar  *(validated — what moves status; demonstrated by us)*

A real coding/research task in the harness, against the local stack, where **all three** are shown on attached artifacts (transcripts + audit log + the blocked-leak demonstration):
1. **H1:** the trigger escalates **only-when-insufficient** (and not otherwise) — meeting the agreed bar, or the kill criterion fires.
2. **H2:** an **unrouted sensitive payload is blocked** at the gate (deny-by-default, fail-closed) — demonstrated, not asserted.
3. **H3:** with the frontier offline/no-key, the loop **falls back to local** and completes, never blocks.
- Clears H1+H2+H3 → C3 (#103) → `proven`; wedge #93 → `proven`/`partial`. Partial clears → `partial`. R2 kill → C3 stays `missing`, report the negative, re-scope.

## Explicitly out of scope  *(goal-owner adjustment 2 — keep the N3 bar provable)*

- **ML / semantic code-sensitivity classification** — N3 enforcement is **mechanism + coarse explicit-route/allowlist policy**, fail-closed; do NOT attempt to *classify* "sensitive code" (unprovable, lossy — W4). The provable claim is "an unrouted payload is blocked," not "the system correctly recognizes all sensitive code."
- **Building a gateway from scratch** — reuse LiteLLM/Bifrost (pin/vendor it — N2 supply-chain, the Mar-2026 LiteLLM PyPI compromise).
- **Coding-quality benchmarking of the frontier vs local** — this proves the *routing/gating mechanism*, not model quality.
- **Multi-machine distribution** (N4) — tie-breaker only.

## Dependencies

- A working **local model** (C1) — modest hardware sufficient (a small Ollama/llama.cpp model is enough to exercise insufficiency + the gate). *Lighter HW dependency than shd-003.*
- A **frontier API key** (the escalation target).
- The recommended composition #81 / position #102.

## Coverage / done call

Validated scope: done = the three demonstrations on real artifacts (or the R2 kill criterion fires, reported honestly). Human reviews at the firewall + synthesis gates.
