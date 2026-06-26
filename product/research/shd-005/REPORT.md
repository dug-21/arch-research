# shd-005 — Synthesis Report: C3 routing, the sovereignty seam, and the platform spine

**Run:** shd-005 · **Phase:** synthesis · **Mode:** directional (recommendation, not proof)
**Date:** 2026-06-26 · **Curator:** shd-005-curator-synth

> **Firewall stamp:** Nothing in this run reaches `proven` or `partial`. C3 (#103) stays `missing`.
> A directional landscape moves *structure*, never *status*. Only the shd-006 validated POC — a
> demonstrated-by-us artifact at the claim's altitude — can advance status.

---

## 1. The question, and the gate-1 broadening

shd-005 entered scoped to **C3 — selective escalation to a public LLM** (a routing/escalation
question). At gate 1 the question was broadened from a tool-ranking exercise ("which router wins on
C3?") to a **whole-loop platform-coverage** question: how much of the entire `shd` loop does each
candidate platform cover, role-scoped — so breadth is graded as an asset **without** letting it
paper over a hard-constraint gap.

This broadening is the run's central move. Ranking the slate against C3 alone under-values
multi-purpose platforms (**platform-blindness**); grading the whole loop surfaces needs the
decomposition never named — and exposes exactly where breadth is a trap.

## 2. The sovereignty seam

Routing (C3) is not a standalone feature — it is the **seam** where the loop's sovereignty
constraints bind. The model-selection decision is the same decision point at which **N3 (egress —
sensitive code stays local)**, **live cost governance**, and **observability/audit** are all
enforced or lost. That is why C3 was broadened to outcome-altitude and made **NFR-governed** rather
than left as a narrow "escalate-when-insufficient" trigger.

## 3. The platform-coverage finding — breadth dividend vs. the two hard gaps

The W7a (gateway lens) and W7b (harness lens) passes agree on a single shape:

- **The breadth dividend is real and bankable.** Any mature gateway (LiteLLM, Bifrost, Portkey,
  Envoy) or standards-based harness (Claude Code) hands us ~12 loop-needs at convenience-grade:
  cost-tracking & attribution, virtual-key/secret management, OTEL observability, caching,
  load-balancing/rate-limiting, audit logging, multi-provider breadth. The build surface is even
  smaller than W6 implied — take the ~80% reuse.
- **But the two needs that actually gate `shd` are exactly where every platform is weakest:**
  - **N3 (HARD):** every platform's guardrail/DLP is entity/PII pattern-matching, best-effort,
    recall-bound (LiteLLM's Presidio guardrail shipped a *silent no-op* — W4 #8359). None implements
    the **deny-by-default, code-class, fail-closed** boundary N3 requires. The green "guardrails ✓"
    checkbox is **not** N3 satisfaction.
  - **C3 confidence trigger (HARD-ish):** every platform's "routing" is
    rule/cost/load-balance/error-failover — **never** the local-insufficiency / confidence trigger
    the C3 ask names.
- **The sharpest trap (W7b):** OpenHands' sandbox is the most seductive false-positive — it isolates
  code *execution*, not prompt *egress*. **Sandbox ≠ egress gate.** Likewise Claude Code's global
  base-URL is a *lever*, not an enforced *gate*. No quantity of SOFT breadth nets against the one
  HARD need it cannot touch.

## 4. The position — the platform spine

**(Finding #102, `position`, `claimed`.)**

> Adopt a self-hosted commodity gateway (**LiteLLM** — incumbent #70/#54; or **Bifrost** for
> governance-native OSS) as the routing/egress/ops backbone, **+ Claude Code** as the
> standards-based harness/ops layer. **Do NOT build a gateway.** Build only the two thin **HARD**
> layers nothing ships:
> - **(B)** a local-insufficiency **confidence trigger** from harness-observable execution signals
>   (#75);
> - **(C)** a deny-by-default, **code-class, fail-closed egress gate** (#78) on the gateway's
>   pre-call hook.
>
> Hosted aggregators (#74 OpenRouter, Requesty, Cloudflare) are **role-scoped-disqualified** —
> frontier egress *target* only (non-sensitive escalation), never the router/gate on a sensitive
> path, never the N2 backbone. The platform dividend is bankable for the SOFT needs but **never**
> satisfies N3 or the C3 trigger.

## 5. Adopt-3 NFRs + deferred (D10)

**Adopted this run (new `nfr` capabilities, `claimed`, `Advances→ #3`):**

| ID | NFR | About → | Why distinct |
|----|-----|---------|--------------|
| **#98** | Loop observability & auditability | #4, #5, #6 | proves N1/N3 + powers the demonstrated-vs-claimed firewall |
| **#99** | Live cost governance & attribution | #6 | distinct from N1's owned-HW posture — live caps on metered frontier calls (N1-adjacent) |
| **#100** | Agent-action security policy | #5, #6 | tool-approval + sandbox isolation, SEPARATE from N3 egress (sandbox ≠ egress gate) |

**Deferred (Finding #101, D10 — recorded, build-deferred; decompose when a goal targets them):**
sub-agent/swarm orchestration · MCP/tool-ecosystem access · provider key/secret management ·
semantic caching (N1 lever) · checkpoint/rollback · cross-instance LB/rate-limiting (N4).

## 6. The C3 broadening

**C3 corrected #6 → #103** (status **stays `missing`**). New outcome-altitude, NFR-governed
done_when:

> *Each task routes to the best-fit model under sovereignty / security / observability constraints,
> with escalation to a public LLM gated by N3 (sensitive code stays local unless explicitly routed)
> and returning into the local loop.*

Status is deliberately held at `missing`: a directional landscape does not clear a behavioral
done_when (D7 under-scope guard). It awaits the shd-006 validated proof.

## 7. The shd-006 POC bar (the proof gate)

The shd-006 validated POC must demonstrate, on a **demonstrated-by-us** artifact, all three:

1. the **trigger** routes **only-when-insufficient**;
2. the **gate** **blocks an unrouted sensitive payload** (deny-by-default, fail-closed);
3. **offline falls back to local**.

Only that artifact moves C3 (#103) off `missing`.

## 8. Platform-vision linkage

C3 routing is the shared spine between the `shd` loop and the platform vision:

- **#92** — Sovereign auditable agentic dev/research platform (goal, build-deferred vision).
- **#93** — Auditable sovereign boundary (wedge capability); **#81** (routing-gate composition)
  `Prerequisite→ #93`.
- **#95** — Unified governance & auditability spine (the moat NFR across all three layers).
- **#97** — Unimatrix as the evidence-graded knowledge & governance engine.

Because **#81 delivers both C3 (#103) and wedge #93**, the **shd-006 POC that proves C3 is
simultaneously the proof-gate for the platform wedge** — one artifact, shared lineage. The C3
routing technology feeds the wedge directly.

---

**Node ledger (this run, synthesis):** #98, #99, #100 (NFRs, `claimed`) · #101 (deferred finding) ·
#102 (position finding, `claimed`) · #103 (C3 broadened, `missing`). All tagged `shd-005`.
