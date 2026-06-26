# shd-005 — Intelligent multi-LLM routing for the loop: route each task to the right model (local↔frontier), confidence-gated public escalation as the anchor policy (C3)

**Status:** SCOPE
**Goal(s):** `shd` (primary, #3)
**Capability target(s):** **C3 — Tasks selectively escalate to a targeted public LLM when local is insufficient** (#6) — *anchor policy; see "Capability-altitude note" below: discovery may show the delivering capability is general model-routing, of which C3's escalation is one policy.*
**Confidence-required:** directional
**Phase / area:** routing / escalation
**Cycle topic / Issue:** shd-005

Governing NFRs (via `About→ C3`): N1 owned-HW/budget (#7) · **N2 no-outage/vendor-not-load-bearing (#8)** · **N3 sensitive-code-stays-local (#9)** · N4 multi-machine-ready (#10).

---

## The question

Survey the landscape of **intelligent multi-LLM routing** for the self-hosted loop: how to route each task to the **right** model/endpoint — across local-small, local-large, and frontier models, and across frontier providers — rather than treating it as a binary local-vs-public switch. The **anchor policy** that C3 demands (escalate to a public LLM *only* when a local-confidence bar is unmet, and return) is one routing decision inside this broader surface. The survey spans (a) the *route-decision signals* that pick a destination, (b) the *routing mechanisms* that act on them — **standalone routers/gateways AND harness-native routing**, evaluated on a **sovereignty seam** (self-hostable routing logic vs. hosted routing-as-a-middleman), (c) the *privacy gate* that guarantees sensitive code does not leave local unless explicitly routed (N3), and (d) **novel approaches**, explicitly in-bounds, because if nothing off-the-shelf meets the bar we will know what we'd have to build.

> Route each task to the right model — local↔frontier and across providers — so the cloud stays a *fallback, never load-bearing* (N2), *no sensitive code leaks* (N3), and the routing logic itself stays under our control; what's the field, and what must a POC prove to trust the gate?

## Why it matters

C3 is the **release valve** of `shd`: it lets the self-hosted loop take on work beyond local capability without re-making a vendor's cloud load-bearing. The human steer at gate 1 widened the frame: the real problem is not a binary local/public switch but **routing to the best-fit model** — and the technology that delivers it (a router) is a **reusable program-scoped asset** any future goal can pull from, which is exactly the kind of node the library should compound.

The trap the goal must avoid: **"route to the right LLM" is the headline feature of hosted aggregators (OpenRouter, Requesty, Portkey, …), but they route *through their cloud* — every prompt and code fragment crosses a third party.** That is a new load-bearing vendor (N2) and a sensitive-code egress (N3) — the two failure modes `shd` exists to prevent. So this scope's central job is to separate **routing logic/policy** (self-hostable, want it) from **routing-as-a-hosted-service** (a middleman; usable only as a frontier *target* behind the N3 gate, never as the router). Picking a router that quietly becomes load-bearing or leaks code re-foundations the whole sovereignty thesis. This scope ranks the field so the validated follow-on builds a routing gate we can actually trust.

## Known constraints & prior art  *(build on these — do not re-derive)*

- **Reuse-first:** **no `technology` nodes exist for C3 routing/escalation yet** — the KB has C1 inference candidates (#38–#53, `claimed`) and the C2 harness slate (#11–#15, `claimed`). This scope establishes the C3 routing `technology` nodes. Curator searches `category:technology` FIRST before storing, links each new node `Prerequisite→ C3` (#6).
- **Sovereignty seam (the governing evaluation axis).** Every routing option is classified **self-hosted / local-control** (routing logic runs on owned hardware; only the chosen frontier *call* egresses, behind the N3 gate) vs. **hosted middleman** (all traffic transits a third-party router). Hosted-middleman routers are **disqualified as the router** for sensitive paths (N2/N3); they may appear only as a frontier *egress target* downstream of the gate. Name this classification for every option.
- **C2 dependency (shd-002) — harnesses may already route.** The C2 slate (aider · Claude Code + local shim · Continue · OpenHands · Goose, plus Roo/Cline surfaced by the human) is where a task runs; **several harnesses already support multiple model endpoints / per-task model selection.** Survey whether the C2 slate *itself* delivers part of C3 (harness-native routing) before assuming a separate router is needed — that is the cheapest reuse path. The **Claude Code + local-shim (#12, T3a)** is the natural frontier conduit (it already speaks frontier Claude *and* a local OpenAI-compatible endpoint).
- **C1 dependency:** the *local* side of the route is the C1 stack (#38–#53). "Local is insufficient" / "which local model" is measured against the **recommended C1 stack's** ceiling; this scope consumes that ceiling, it does not re-rank local models.
- **N3 (sensitive-code-stays-local) is the hard NFR**, not a tie-breaker. C3's `done_when` is privacy-shaped: *"no sensitive code reaches a public LLM unless explicitly routed."* Every option is judged on **what enforces "explicitly routed"** — and a hosted router that sees all traffic fails this by construction.
- **N2 (no-outage / vendor-not-load-bearing):** routing is a **fallback that must degrade gracefully** — offline / outage / no-key → fail back to local, never block; and the *router itself* must not become a vendor dependency. Flag offline behavior and router-dependency per option.
- **N1 (owned-HW/budget):** frontier calls are the one metered cost — flag cost posture (how much traffic escalates, token exposure) per option.
- **N4 (multi-machine-ready):** does the routing layer foreclose running as a shared router service across owned machines? Tie-breaker, not a gate (D11).
- **Human-named leads (confirm during discovery):** `OpenRouter` (hosted aggregator), `ruflo` (*spelling/identity to confirm — a routing tool the human flagged; routing-space candidates to check: RouteLLM, Requesty, RooFlow*), and "any other tools." **Novel approaches are explicitly acceptable** (per the human + methodology §1) — if the off-the-shelf field fails the sovereignty + confidence-gating bar, sketch the novel approach rather than forcing a poor fit.
- **Carry shd-002's L1 lesson:** doc-claims of "smart/automatic routing" are the silent failure mode — separate doc-claim from benchmark-reported; the live gate test lands in the validated follow-on, not here.

## Bounded investigation (workstreams)

Each workstream is one researcher's partition. State an explicit `Output:` per workstream.

- **W1 — Route-decision signals (the trigger / selector).** Enumerate signals that pick a destination, not just escalate-y/n: token-level uncertainty (logprob/entropy), self-consistency / sampling disagreement, verifier/judge models, task-type & difficulty classifiers, context-size / capability-match heuristics, and **harness-level signals** (test/compile failures, retry exhaustion, tool-call failures). Per signal: what it measures, reliability (doc vs benchmark), overhead, whether it needs model internals (logprobs) the C1 engines expose, harness-observable? *Output:* a signal catalog with those columns.
- **W2 — Standalone routers, gateways & aggregators.** Enumerate the routing/gateway tooling: LiteLLM (proxy), RouteLLM, OpenRouter, Requesty, Portkey, Martian, Unify, Not Diamond, the human-named `ruflo` (identify), and any others surfaced. **Classify each on the sovereignty seam** (self-hosted/local-control vs hosted-middleman), and record: models/providers spanned, routing logic (rule / learned / cost-based / confidence-based), how it integrates with the C2 slate, N2/N3 posture, doc vs benchmark savings/quality, maturity. *Output:* a router landscape table, sovereignty class flagged per row; hosted middlemen marked disqualified-as-router / target-only.
- **W3 — Harness-native routing (reuse-first).** For the C2 slate (aider · Claude Code + shim · Continue · OpenHands · Goose · Roo/Cline): does the harness already route across models/endpoints (per-task model config, profiles, auto-escalation hooks)? How much of C3 does it deliver with no extra router? *Output:* per harness: routing capability (none / manual model-switch / policy-driven) · how it selects · what it can't do — i.e. the gap a router would fill.
- **W4 — Privacy-preserving gate (N3 — the hard NFR).** Map what enforces *"sensitive code never leaves local unless explicitly routed"*: secret/credential/PII scrubbing before egress, code redaction/abstraction, data-classification policy gates, explicit human-consent routing, hard local-only (deny-by-default) boundaries. Per approach: enforces-vs-best-effort, placement in the flow, failure mode, and **how it composes with a router** (esp. whether a hosted router defeats it). *Output:* a privacy-gate map with those columns; approaches with no enforceable gate flagged disqualified-for-sensitive.
- **W5 — Frontier targets, return path, offline fallback & cost (N1/N2).** Which frontier models/providers are the escalation target (Claude frontier the default via the Claude Code path), how the routed result **returns and merges** into the local loop, **offline-fallback** behavior (N2), and **cost posture** (N1). *Output:* a target + return-path map per target: integration · return/merge · offline-fallback · cost flag.
- **W6 — Novel-approach gap analysis (explicitly in-bounds).** If W2/W3 show no off-the-shelf option meets the sovereignty + confidence-gating + N3 bar, sketch the **novel approach** we'd build: a self-hosted router (e.g. LiteLLM-proxy core) + a confidence-signal trigger (W1) + an enforceable egress gate (W4). Name the gap each existing tool leaves and what the novel piece must add. *Output:* a gap matrix (per existing tool: what's missing) + a sketch of the minimum novel router if warranted — or an explicit "off-the-shelf suffices, no novel work needed" verdict.
- **W7 — Distribution (N4) + Synthesis & ranking.** Forecloses/extends flag per leading approach (N4). Then rank the **signal × router × privacy-gate** routing stacks easy / moderate / hard / dream against C3's `done_when` and N3, determining constraint named (usually trigger reliability or privacy-gate enforceability vs sovereignty); recommend a leading pattern as a `position`; specify the **validated follow-on scope** (`shd-006`) and exactly what its POC must demonstrate. *Output:* distribution flags + a ranked stack map + recommendation + drafted follow-on bar.

## Expected output (FINDINGS.md)

1. **Route-decision signal catalog** (W1).
2. **Router / gateway landscape** (W2) — **sovereignty class per row**; hosted middlemen flagged disqualified-as-router / target-only; tagged easy / moderate / hard / dream.
3. **Harness-native routing map** (W3) — how much of C3 the C2 slate already delivers, and the gap.
4. **Privacy-gate map** (W4) — enforces-vs-best-effort, placement, failure mode, composition with a router (N3).
5. **Frontier-target + return-path map** (W5) — integration · return/merge · **offline-fallback** (N2) · **cost flag** (N1).
6. **Novel-approach gap analysis** (W6) — what off-the-shelf leaves missing + a minimum novel-router sketch, or an "off-the-shelf suffices" verdict.
7. **Distribution flags** (W7, N4).
8. **Recommendation** — the leading signal × router × privacy-gate routing pattern + reasoning, as a `position` finding (must respect the sovereignty seam).
9. **Validated follow-on** — a draft `shd-006` scope question + the concrete POC bar (below).

## Proof bar  *(directional)*

**Structure-only — no status change.** This scope produces `finding`s + `technology` nodes left `claimed` (signals, routers, privacy gates) + a `position` recommendation. **Every reliability / savings / quality figure it carries is doc-claim or community-report, never demonstrated by us — nothing reaches `partial` or `proven` here.** It *spawns* a validated follow-on (`shd-006`); this scope proves nothing itself.

The follow-on (`shd-006`) POC must demonstrate, **at runtime altitude, by us**, a concrete `done_when`:
> On a real coding/research task running in the C2 harness against the recommended C1 local stack, the **self-hosted** routing gate sends the task to the public LLM **only when** the local-insufficiency signal **S** trips threshold **T** (and never otherwise), the result **returns and merges** into the local loop, **no sensitive code crosses the boundary unless explicitly routed** (privacy gate **G** demonstrably blocks an unrouted sensitive payload), the **router itself runs on owned hardware** (no hosted middleman in the sensitive path), and the loop **falls back to local** when the target is offline. The recommendation fixes S / T / G / router / target the POC must hit; the POC attaches the routed-vs-not-routed transcript + the blocked-leak demonstration to `proven_by`.

## Explicitly out of scope

- **The local inference stack** — engine/model/quant selection is C1 / shd-004. This scope consumes C1's ceiling; it does not re-rank local models.
- **Re-evaluating the harness slate as harnesses** — that is C2 / shd-002. Here we assess the slate **only for its routing capability** (W3), not its overall fitness.
- **Actually building, wiring, or benchmarking** any router/signal/gate — all measurement is the validated follow-on (`shd-006`). Reliability/savings here are reported, never demonstrated. (W6 *sketches* a novel approach; it does not build one.)
- **Training a custom router/classifier model from scratch** — survey stock routing logic and at most *sketch* a novel composition (W6); a trained router is itself a follow-on bet if W6 names it as the leading direction.
- **General-purpose secret-scanning tooling** beyond its use as an escalation egress gate (N3) — scope it to the boundary, not the whole repo.

## Coverage / done call  *(synthesis)*

Loop-until-dry: stop when **K=2** consecutive searches surface no new signal, router, harness-routing capability, or privacy-gate approach **and** **≥2** independent findings corroborate the leading signal × router × privacy-gate stack. Agent proposes "sufficient"; **human confirms** at the synthesis gate.

## Capability-altitude note  *(D3 / goal-owner — flagged, not yet acted on)*

The human's broadening ("more than local/public — routing to the *right* LLM") suggests the **delivering technology** for C3 is *general multi-model routing*, of which C3's "escalate to public when local insufficient" is **one policy**. This scope proceeds with **C3 as the anchor** (its `done_when` is the proof target) and stores routing as program-scoped `technology` reusable beyond C3. **If discovery confirms the capability itself is broader**, the resolution is decided at synthesis (goal-owner / D3): either **sharpen C3's `done_when`** to "route each task to the best-fit model, with public escalation gated by N3," or **add a sibling capability** (a new 🔴 node + new scope) — a *structure* move, firewall-safe, made with the human at the synthesis gate, not pre-emptively here.
