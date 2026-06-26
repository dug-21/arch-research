# shd-005 — Selective escalation: local→public-LLM routing landscape for the self-hosted dev/research loop

**Status:** SCOPE
**Goal(s):** `shd` (primary, #3)
**Capability target(s):** **C3 — Tasks selectively escalate to a targeted public LLM when local is insufficient** (#6)
**Confidence-required:** directional
**Phase / area:** routing / escalation
**Cycle topic / Issue:** shd-005

Governing NFRs (via `About→ C3`): N1 owned-HW/budget (#7) · N2 no-outage/offline (#8) · **N3 sensitive-code-stays-local (#9)** · N4 multi-machine-ready (#10).

---

## The question

Survey the landscape of ways to **escalate a task from the local stack to a targeted public LLM only when local is insufficient — and return** — the cross-product of (a) the *insufficiency signal* that triggers escalation, (b) the *routing/cascade mechanism* that acts on it, and (c) the *privacy gate* that guarantees sensitive code does not leave local unless explicitly routed (N3). The output is a directional map (what's reliable, what's brittle, what's a research bet), a leading-candidate escalation pattern, and a validated follow-on that actually gates and routes a real task.

> When and how should a task cross the local→public boundary so that the cloud stays a *fallback, never load-bearing* (N2) and *no sensitive code leaks* (N3) — and what must a POC prove to trust that gate?

## Why it matters

C3 is the **release valve** of `shd`: it is what lets the self-hosted loop take on work that exceeds local capability (C1) without making a vendor's cloud load-bearing again — the entire point of the goal. The hard part is not *calling* a public API; it is **deciding when** (a reliable local-insufficiency signal, not a guess) and **protecting what crosses** (N3 — sensitive code must not leak via escalation). Get the trigger wrong and the loop either escalates everything (cloud becomes load-bearing, N2 violated, cost unbounded — N1) or never escalates (local ceiling caps the loop). Get the gate wrong and sensitive code leaks the moment the bar trips. This scope ranks the field — confidence signals × routing patterns × privacy gates — so the validated follow-on builds the right gate first instead of shipping a leaky or trigger-happy one.

## Known constraints & prior art  *(build on these — do not re-derive)*

- **Reuse-first:** **no `technology` nodes exist for C3 escalation yet** — the KB has C1 inference candidates (#38–#53, `claimed`) and the C2 harness slate (#11–#15, `claimed`). This scope establishes the C3 escalation/routing `technology` nodes. Curator searches `category:technology` FIRST before storing, per the access rules, and links each new node `Prerequisite→ C3` (#6).
- **C2 dependency (shd-002):** escalation lives **in or around the harness** — the C2 slate (aider · Claude Code + local shim · Continue · OpenHands · Goose) is where a task runs and where a router would sit. The **Claude Code + local-shim path (#12, T3a) is the natural escalation conduit** (Claude Code already speaks frontier Claude *and* a local OpenAI-compatible endpoint), so weight escalation patterns by how they integrate with that slate, not as standalone services.
- **C1 dependency:** the *local* side of the gate is the C1 stack (#38–#53). "Local is insufficient" is defined relative to what the **recommended C1 stack** can do; this scope does not re-rank local models — it consumes C1's ceiling as the thing the confidence bar is measured against.
- **N3 (sensitive-code-stays-local) is the governing hard NFR**, not a tie-breaker. C3's `done_when` is privacy-shaped: *"no sensitive code reaches a public LLM unless explicitly routed."* Every escalation pattern is judged on **what enforces "explicitly routed"** — redaction/secret-scrubbing, policy classification, explicit-consent gating, or hard local-only boundaries. A pattern with a strong trigger but no enforceable privacy gate is disqualified for sensitive contexts, however good its routing.
- **N2 (no-outage/offline):** escalation is a **fallback, must degrade gracefully** — when the public LLM is unreachable (offline, outage, no key), the loop must fail back to local, never block. Flag each pattern's offline behavior.
- **N1 (owned-HW/budget):** public-LLM calls are the one metered cost in the stack — flag per-pattern cost posture (how much traffic escalates, token cost exposure).
- **N4 (multi-machine-ready):** does the escalation/routing layer foreclose a future where the router runs as a shared service across owned machines? Tie-breaker, not a gate (D11).
- **Carry shd-002's L1 lesson:** doc-claims about "automatic routing" / "confidence-aware" features are the silent failure mode — separate doc-claim from benchmark-reported; the live gate test lands in the validated follow-on, not here.

## Bounded investigation (workstreams)

Each workstream is one researcher's partition. State an explicit `Output:` per workstream.

- **W1 — Local-insufficiency signals (the trigger).** Enumerate the signals that decide "local is insufficient and we should escalate": token-level uncertainty (logprob/entropy/perplexity), self-consistency / sampling disagreement, a verifier or judge model, explicit difficulty/route classifiers, and **harness-level signals** (test failures, lint/compile errors, retry exhaustion, tool-call failures). For each: what it measures, reliability (doc-claim vs benchmark-reported), latency/cost overhead, and whether it needs model internals (logprobs) the C1 engines actually expose. *Output:* a signal catalog — per signal: mechanism · reliability · overhead · requires-logprob/internals? · harness-observable?
- **W2 — Routing & cascade architectures (the mechanism).** Enumerate the patterns/frameworks that act on a signal to route: LLM cascades (FrugalGPT-style), learned routers (RouteLLM and kin), classifier/rule routers, confidence-thresholded fallback, and harness-native escalation hooks. For each: how it integrates with the C2 slate (esp. Claude Code + local shim, #12), what signal it consumes (ties to W1), and doc-claim vs benchmark-reported quality/savings. *Output:* a router/cascade technology list — per option: pattern · signal consumed · C2-integration profile · reported savings/quality · maturity.
- **W3 — Privacy-preserving escalation gate (N3 — the hard NFR).** Map what can enforce *"sensitive code never leaves local unless explicitly routed"*: secret/PII/credential scrubbing before egress, code redaction/abstraction, data-classification policy gates, explicit human-consent routing, and hard local-only boundaries (deny-by-default). For each: what it guarantees vs. best-effort, where it sits in the flow, and its failure mode. *Output:* a privacy-gate approach map — per approach: enforces-vs-best-effort · placement · failure mode · suitability for "explicitly routed."
- **W4 — Escalation targets & the return path (N1/N2).** Which public LLMs are the escalation target (Claude frontier the default given the C2 Claude Code path), how the escalated result **returns and merges** into the local loop, the **offline-fallback** behavior when the target is unreachable (N2), and **cost posture** (N1 — token exposure, % traffic escalated). *Output:* an escalation-target + return-path map — per target: integration via C2 · return/merge mechanism · offline-fallback behavior · cost flag.
- **W5 — Distribution (N4).** Does each leading routing approach foreclose or extend to a router running as a shared service across owned machines? *Output:* a forecloses / extends flag per leading approach — a tie-breaker, not a gate.
- **W6 — Synthesis & ranking.** Rank the **signal × router × privacy-gate** escalation stacks easy / moderate / hard / dream against C3's `done_when` and N3, with the determining constraint named (usually trigger reliability or privacy-gate enforceability); recommend a leading escalation pattern as a `position`; specify the **validated follow-on scope** (`shd-006`) and exactly what its POC must demonstrate. *Output:* a ranked escalation-stack map + recommendation + drafted follow-on bar.

## Expected output (FINDINGS.md)

1. **Insufficiency-signal catalog** (W1) — per signal: mechanism · reliability (doc-claim vs benchmark) · overhead · requires-logprob/internals? · harness-observable?
2. **Router / cascade landscape** (W2) — per option: pattern · signal consumed · C2-integration profile (esp. Claude Code + shim) · reported savings/quality · maturity, tagged easy / moderate / hard / dream.
3. **Privacy-gate map** (W3) — per approach: enforces-vs-best-effort · placement · failure mode · suitability for N3's "explicitly routed"; approaches with no enforceable gate flagged disqualified-for-sensitive.
4. **Escalation-target + return-path map** (W4) — per target: C2 integration · return/merge · **offline-fallback** (N2) · **cost flag** (N1).
5. **Distribution flags** (W5) — forecloses / extends, per leading approach (N4).
6. **Recommendation** — the leading signal × router × privacy-gate escalation pattern + reasoning, as a `position` finding.
7. **Validated follow-on** — a draft `shd-006` scope question + the concrete POC bar it must clear (below).

## Proof bar  *(directional)*

**Structure-only — no status change.** This scope produces `finding`s + `technology` nodes left `claimed` (signals, routers, privacy gates) + a `position` recommendation. **Every reliability / savings / quality figure it carries is doc-claim or community-report, never demonstrated by us — nothing reaches `partial` or `proven` here.** It *spawns* a validated follow-on (`shd-006`) that will move a technology toward `proven`; this scope proves nothing itself.

The follow-on (`shd-006`) POC must demonstrate, **at runtime altitude, by us**, a concrete `done_when`:
> On a real coding/research task running in the C2 harness against the recommended C1 local stack, the escalation gate routes to the public LLM **only when** the local-insufficiency signal **S** trips a threshold **T** (and never otherwise), the result **returns and merges** into the local loop, **no sensitive code crosses the boundary unless explicitly routed** (privacy gate **G** demonstrably blocks an unrouted secret/sensitive payload), and the loop **falls back to local** when the target is offline. The recommendation from this scope fixes S / T / G / target that the POC must hit; the POC attaches the routed-vs-not-routed transcript + the blocked-leak demonstration to `proven_by`.

## Explicitly out of scope

- **The local inference stack** — engine/model/quant selection is C1 / shd-004. This scope consumes C1's ceiling as the bar; it does not re-rank local models.
- **The agentic harness itself** — that is C2 / shd-002. This scope routes *from within* the harness; it does not re-evaluate the harness slate.
- **Actually building, wiring, or benchmarking** any router/signal/gate — all measurement is the validated follow-on (`shd-006`). Reliability/savings here are reported, never demonstrated.
- **Fine-tuning a custom router/classifier model** — survey stock/off-the-shelf routing; a trained router is a follow-on bet if W2 surfaces it as the leading direction.
- **General secret-scanning tooling** beyond its use as an escalation privacy gate (N3) — scope it to the egress boundary, not the whole repo.

## Coverage / done call  *(synthesis)*

Loop-until-dry: stop when **K=2** consecutive searches surface no new signal, router pattern, or privacy-gate approach **and** **≥2** independent findings corroborate the leading signal × router × privacy-gate stack. Agent proposes "sufficient"; **human confirms** at the synthesis gate.
