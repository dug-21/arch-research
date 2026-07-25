# R2-4 — Self-improvement: the adoption half + the C-3 diff

**Run:** `wfh-004` · Issue #48 · phase `hypothesize` round 2, targeted · read-only, zero graph writes.
**Charter:** L3's declared hole (*"nothing on the adoption half"*) + diff the four C-3 attacks (L2-17, L4-38, L6-29/31, L1-35). No fifth attack added.
**Inherited caveat (L3-31):** this register shares the W0 surface with all of round 1; convergence between its candidates and round-1's is correlated by construction.

---

## 1. The adoption analysis (headline)

An improvement in this garage must survive **five crossings**. The record locates a failure at every one, and all five failures have the same mechanical shape.

| # | Crossing | Carrier today | Field failure |
|---|---|---|---|
| **A** | incident → record | the retro step + human memory | P-19: the retro is *"the step that gets dropped,"* ×3 — including by the run that closed *on a process defect*. And W0-d §6: five pains surfaced only from a 2-hour manual sweep — the record that does exist goes unread. |
| **B** | record → decision | a finding in the graph, auto-injected into every specialist | **#179: the diagnosis was in the graph, broadcast into every agent's context, days before wfh-002 closed on exactly the diagnosed failure.** Delivered to everyone; owned by no one. |
| **C** | decision → implementation | prose edits to scattered surfaces | Partially works (16 `wf:` versions shipped) — but note *where* fixes land: P-01's fix went to a user-memory file **outside the repo**; `settings.local.json` is **gitignored**. Implementations land on surfaces of unequal versioning and visibility. |
| **D** | implementation → in force | the runtime reading the changed artifact | W0-b §0-iv: six agent files carry frontmatter keys **nothing reads**. An "implemented" improvement can be a silent no-op, and the harness's documented behavior — silently ignoring unrecognized fields — guarantees the no-op is undetectable. Prose-protocol changes are "in force" only via model compliance (FP-1). |
| **E** | in force → verified | nothing | P-18: *"UNBLOCKED, runnable"* declared 2026-06-26; never run once as of 2026-07-25. |

**The mechanical statement.** Behavior in this system is caused by three channels: the immediate task prompt, enforced mechanism (hooks/permissions — none configured), and model disposition. **The garage's improvement store feeds only the first channel — and feeds it as *advisory tokens at ambient priority*, competing with the task rather than binding it.** An improvement is adopted when it has become **configuration or enforcement**; the graph can only ever make it **context**. That is the precise content of *"a finding in a graph is also just prose"*: the knowledge-as-improvement model routes improvements into the one channel that cannot carry them. **The gap between "the system knows X" and "the system does X" is the gap between context and configuration**, and no actor, record, or check currently moves anything across it.

**The four states, as observables.** An improvement is:
- **Decided** — a disposition record naming the change, its **target artifact**, and its owner (E-1 machinery).
- **Implemented** — the named artifact's content digest differing in the declared way, joined to the decision record.
- **In force** — **behavioral evidence**, not config presence: the first run event the change predicts (a hook firing, a deny landing, a field read). Digest-in-fingerprint is insufficient — §0-iv is the proof that present ≠ read.
- **Verified** — the change's own pre-declared success predicate holding against run records.

P-18 reported *decided* as *in force*. #179 reached *recorded* and was reported as if that were a state at all — it is upstream of decided. **The garage has no vocabulary for these distinctions, so every state-conflation is unfalsifiable in its own records.**

**Consequence for the whole Self-improvement column:** round 1 populated generation and measurement densely and adoption almost not at all — yet the field record contains **zero quality-of-improvement failures and repeated total-loss failures** (the improvement evaporated at a crossing). The demanded build order is the reverse of round-1's density: **adoption first, measurement second, generation last.** A better retro tool today would lengthen the backlog of unadopted improvements, not improve the system.

---

## 2. Candidate register (new only)

**`R2-4-01` — The improvement lifecycle ledger**
- **Ability:** Every accepted improvement is a tracked object with four observable states — decided, implemented, in force, verified — each advancing only on its own evidence class, observable as no improvement ever reported at a state above its evidence (reverted/retired recorded as dispositions, never as evaporation).
- **Concern:** Self-improvement (spans E-1, Introspection).
- **Mechanism:** State machine over (disposition record · artifact digest diff · behavioral first-effect event · success-predicate evaluation). Precedent: **CAPA tracking in regulated quality systems** (FDA 21 CFR 820.100 / ISO 9001) — invented because "we wrote a memo" demonstrably does not change factory-floor behavior; a CAPA closes only on *verified effectiveness*, and open CAPAs age visibly.
- **Inference surface:** State transitions deterministic given the evidence records; whether a success predicate is *satisfied* may be a C-2 forced-binary leaf.
- **Incumbent delta:** **C** — no state vocabulary exists; P-18's conflation is unrepresentable as an error today.
- **Evidence:** P-18, #179, P-19.
- **Differs from:** L6-40/L2-24 track *declared obligations discharged at close*; this tracks a *change moving through states across runs* with per-state evidence classes.
- **Falsifier:** If garage improvement volume (~2/month) makes ledger upkeep cost more than the losses it prevents, it becomes the dropped-retro one level up.

**`R2-4-02` — An improvement lands as a diff, not (only) a finding**
- **Ability:** At acceptance, every process improvement is recorded as a proposed change to a named governing artifact (path + patch or checkable predicate), or explicitly tagged "advisory — no artifact," observable as zero process findings in the improvement stream lacking one of the two tags.
- **Concern:** Self-improvement (spans Structure).
- **Mechanism:** Bifurcation at admission into *advisory* (context channel) and *operative* (config channel); the operative form is a patch/PR — the file ecosystem's native adoption unit, so C-3-aligned by construction. Precedent: fix-as-PR vs fix-as-wiki-page; SRE runbook-to-automation discipline.
- **Inference surface:** Drafting the patch from a prose lesson is a leaf; the presence check is deterministic.
- **Incumbent delta:** **C** — findings carry no target-artifact field; `Motivates` points at technologies, not governing files.
- **Evidence:** #179 (a diagnosis with nowhere to go but context); P-01 (the fix that did land chose an out-of-repo, unversioned surface).
- **Differs from:** L1-34 (anomaly→flight-rule corpus that *fires on recurrence*) is one downstream consumer; this is the upstream generic requirement that *any* improvement name its landing artifact or be demoted to advice.
- **Falsifier:** If most real improvements are genuinely advisory, forcing artifact form produces empty ceremony patches — measurable as the advisory-tag fraction.

**`R2-4-03` — In-force is behaviorally attested, never config-attested**
- **Ability:** Every change to a governing artifact registers the first observable behavioral event it predicts, and is confirmed in force only when that event is seen in a live run; a change with no observed effect after N runs is flagged **inert**, observable as a per-change first-effect record and an inert-change list.
- **Concern:** Self-improvement (spans Introspection, Structure).
- **Mechanism:** Expected-observable registered per change (a smoke expectation); presence checked against run event records — deterministic. Precedent: monitored feature-flag rollout ("flag evaluated" telemetry — a deploy is not done until the flag is *seen evaluated* in production); dead-config detection.
- **Inference surface:** Zero for the check; authoring the expected-observable is part of the change.
- **Incumbent delta:** **C**, with the standing counter-example live: six agent files whose restriction keys nothing reads (W0-b §0-iv) — implemented, inert, silent, for the garage's *cardinal invariants*.
- **Evidence:** W0-b §0-iv; P-30.
- **Differs from:** L2-30 (compile-from-contract) prevents *contract↔artifact drift* but still lands in inert-field hell if the runtime ignores the compiled key; L6-28/L5-26 (fingerprint) proves which config was *present*, not that it *did* anything. **The missing third check.**
- **Falsifier:** Many legitimate changes have no cheap observable (a wording change in a prompt) — if the inert list fills with false positives, the flag gets ignored.

**`R2-4-04` — Regression at n=1: the invariant floor**
- **Ability:** A method-version change ships with the run-level invariants it must not break; every subsequent run's invariant evaluation is keyed to the method version, observable as a per-version conformance record that flags, on the **first** run, a version whose runs breach invariants its predecessor's did not.
- **Concern:** Self-improvement (spans E-1, Recovery).
- **Mechanism:** Regression *testing*, not regression *detection* — boolean invariant evaluation (roles ran, retro performed, surfaces unique, counts reconcile: L2-15/L6-23's set) keyed by config fingerprint. No cohorts, no statistics: **an invariant breach at n=1 is a bug report, not a noisy metric.** Precedent: CI regression suites — you do not need twenty builds to know the build broke.
- **Inference surface:** Zero for every invariant already named by round 1.
- **Incumbent delta:** **C.**
- **Evidence:** P-19, P-03 — a `wf:` version that drops a step would be caught the first time it runs, not after ~50.
- **Differs from:** L4-39 is change-point detection on outcome *metrics* at fleet ≥~50 runs; this is boolean *conformance* at n=1 — **the answer to "what is the n=1 answer?"** It catches breakage, never degradation; L4-39 remains necessary for the latter.
- **Falsifier:** If bad versions harm graded quality rather than breach invariants, the floor passes them — exactly the case the statistical layer exists for; complements, not substitutes.

**`R2-4-05` — Obligations re-arm at successor admission**
- **Ability:** Obligations undischarged at a run's close transfer automatically to the successor surface, and a successor run cannot be admitted until each carried obligation is acknowledged — adopted, re-deferred with reason, or escalated — observable as a SCOPE like wfh-004's being unable to silently omit wfh-002's deferred retro.
- **Concern:** E-1 (spans Self-improvement, Structure).
- **Mechanism:** Admission-time set difference over the obligation ledger — **the check moves from the *closing* run (where deferral is legitimate and the leverage is gone) to the *next admission* (where a deterministic gate already exists: INIT).** Precedent: shift-handover sign-off — the incoming shift signs for open items; the outgoing shift cannot discharge by leaving. Accounting period-close carry-forward.
- **Inference surface:** Zero for carriage and the admission check; "was this discharge adequate" is a leaf.
- **Incumbent delta:** **C** — and the pain is live in this very run: wfh-002's deferred retro was owner-assigned to its successor; the successor's SCOPE carried no retro workstream, and nothing could notice (P-19).
- **Evidence:** P-19 (verbatim reproduction into wfh-004), P-26.
- **Differs from:** L2-24 refuses *close* with obligations open — but P-19 shows deferral-at-close is legitimate and the loss happens *between* runs; L5-27 persists the obligation but names no enforcement moment. **This adds the one deterministic gate the lifecycle actually passes through.**
- **Falsifier:** If successors acknowledge-and-re-defer forever, the check produces a paper trail of evasion rather than discharge — though even that converts silent evaporation into visible aging, which is P-26's ask.

**`R2-4-06` — Improvements are routed to the actor who can adopt them, not broadcast**
- **Ability:** A process-improvement finding is delivered to the principal that owns its target artifact, with delivery and disposition recorded, observable as no process finding marked "delivered" merely because it entered some agent's retrieval context.
- **Concern:** Self-improvement (spans Context provisioning).
- **Mechanism:** Deterministic dispatch on the target-artifact field (from R2-4-02) + disposition tracking (E-1). Precedent: bug-tracker assignment vs mailing-list CC — the difference between a ticket and a newsletter.
- **Inference surface:** Zero given R2-4-02's field; without it, extracting the owner from prose is a leaf.
- **Incumbent delta:** **C** — the incumbent's one delivery channel is the broadcast injection (W0-b #7), which #179 proved is not an adoption channel.
- **Evidence:** #179 — delivered into every agent's context; adopted by none. **Everyone informed, no one responsible.**
- **Differs from:** L3-22 flags the same broadcast channel as an *attack surface*; this repurposes the observation for adoption — broadcast is also *why* uptake fails. L1-31 (ASRS) collects reports inward; this routes decisions outward.
- **Falsifier:** With one owner owning every artifact (today's reality), routing is a no-op over broadcast — pays only at owner/maintainer count ≥ 2, and should say so.

**`R2-4-07` — The loop's own health is a standing fact**
- **Ability:** The improvement pipeline reports its throughput and latency — items and ages per state, and time-to-full-path — observable as a standing answer to "when did an improvement last complete the whole path?" (current true answer: **never**).
- **Concern:** Self-improvement (spans Introspection).
- **Mechanism:** Aggregation over R2-4-01's ledger. Precedent: **DORA metrics** — the industry's standard answer to "is our improvement loop working," which deliberately measures the *pipeline*, not the product. Partially dodges L3's fixed-point objection for loop-*health* (the ledger, not the improved party, produces the numbers) — though not for improvement *quality*, which stays under Goodhart.
- **Inference surface:** Zero.
- **Incumbent delta:** **C** — the only current signal is P-18's binary ("has the A/B ever run"), which answers with "no" and nothing else.
- **Evidence:** P-18, P-19 — items stall at the same crossings repeatedly and nothing counts the stalls.
- **Differs from:** L6-30 scores *a run*; this scores the *improvement pipeline across runs*. **No round-1 candidate observes the reflexive loop as an object** — the same shape as W0-d §4's finding, one level up.
- **Falsifier:** A pipeline metric with one consumer and no decision hanging on it is L4-26's falsifier recursively applied.

**`R2-4-08` — A comparison's design class caps the claims it licenses** *(from the C-3 diff)*
- **Ability:** Every method-comparison record declares which design produced it (paired-concurrent / randomized-cohort / replay-divergence / matched-observational) and the claim ceiling that design licenses, and downstream consumers — a `wf:` bump, a grade move on #66 — are checkable against that ceiling, observable as no version bump citing evidence above its class.
- **Concern:** Self-improvement (spans Structure/evidence discipline).
- **Mechanism:** Evidence-hierarchy labeling (epidemiology's GRADE framework) + deterministic label check at the consuming write — the firewall's existing grade discipline applied to *process* claims.
- **Inference surface:** Zero at the check; the taxonomy is fixed configuration.
- **Incumbent delta:** **C** — P-18's "UNBLOCKED" is exactly a claim above its evidence class, and nothing could represent the error.
- **Evidence:** P-18; the four-way C-3 split itself — four instruments, four different licensed claims, and no round-1 candidate distinguishes their outputs at the consumer.
- **Differs from:** L1-35 states *one* design's limits honestly; this governs all designs *and their consumers*. Complements L3-30 (grade lattice) — same monotone principle applied to method evidence.
- **Falsifier:** If the garage only ever operates one design at a time, the label is a constant and the check idle.

**`R2-4-09` — Replay-to-first-divergence as an n=1 change smoke test** *(from the C-3 diff)*
- **Ability:** A proposed method change is replayed against one recorded run with inference leaves pinned, up to the first behavioral divergence, and the divergence point is reported, observable as "v0.17 first alters behavior at step X of run R" before the version ships — with the claim explicitly limited to *what changed*, never *which is better*.
- **Concern:** Self-improvement (spans Recovery).
- **Mechanism:** Golden-file / snapshot testing with VCR-style cassettes — L6-29's capture machinery scoped down to one recorded run and prefix-pinning only. **The diff shows this is the honest deliverable of the replay attack for prompt-level changes anyway:** once the changed prompt elicits a different completion, pinned cassettes are invalid from that point on — so full-replay A/B degenerates to exactly this, and the degenerate form is buyable years earlier.
- **Inference surface:** The replayed leaves are pinned (zero at replay); the live continuation past divergence is inference as ever.
- **Incumbent delta:** **C** (per C-3), but requiring only single-run capture, not the fleet-wide legibility threshold L6-29 needs.
- **Evidence:** P-18 — sixteen shipped versions whose first behavioral effect nobody could name; several may have had *none* (R2-4-03's inert class) or the wrong sign.
- **Differs from:** L6-29 claims bit-identical re-run and effect *isolation*; this claims only divergence *location* from one recorded run — weaker, orders cheaper, and the pre-ship complement to R2-4-04's post-ship invariant floor.
- **Falsifier:** If nearly every change diverges at step 1, the divergence point carries no information and only the invariant floor pays.

---

## 3. The C-3 comparison table (analysis deliverable)

C-3 as argued (W0-b §4): controlled comparison needs (a) config as versioned value, (b) two runs differing only in it, (c) an outcome metric; (b) is blocked by sampling nondeterminism + a retrieval corpus the run itself mutates; therefore not expressible without an external replay substrate.

| | **L2-17** concurrent paired trials | **L4-38** fleet cohorts | **L6-29/31** record/replay | **L1-35** matched cohorts |
|---|---|---|---|---|
| **What it kills** | Corpus drift *between* arms | Both blockers, statistically: noise averages out, drift randomizes across arms | Sampling nondeterminism entirely (leaves pinned); drift only if the corpus is also snapshotted | Nothing — **concedes both** and lowers the claimed evidence class instead |
| **Load-bearing assumptions** | Write-isolation between arms w.r.t. the shared graph (its own falsifier: without it simultaneity *doubles* contamination — needs L4-20); 2× concurrent capacity; duplicable inputs incl. duplicated-or-withheld mid-run steering; ≥ several pairs | **Fleet volume exists** — ~20 runs/arm against a cadence of 8 runs/5 weeks ≈ **6 months per comparison**; run comparability across heterogeneous work; effect sizes above noise | Every nondeterministic leaf enumerated + captured (effectively the whole L6 program as prerequisite); corpus snapshot; **and the tested variable must act outside the pinned leaves** | Enough comparable runs to match (works on runs you were doing anyway); matching validity at small n; pre-registration discipline (L1-33/L3-08); honesty about the weaker claim |
| **Compatible with** | L4-38 (paired randomization inside a cohort design — textbook variance reduction); L1-35 | L1-35 (same instrument at different n); L2-17 | All three — cassettes tighten L2-17's pairing; gives L4-38 regression triage | L4-38 (it *is* L4-38's bootstrap); L2-17 |
| **Cost** | Moderate: 2× spend + KB write-isolation + assignment harness | Near-zero mechanism; the fleet is the cost — **cannot exist below scale** | Highest build; cheapest marginal comparison | **Cheapest by far**: metrics + registration + a comparison memo; available at n≈2 |
| **Observable as** | Per-input win/loss between named config hashes | Effect size + CI attributed to the definition delta | Bit-identical re-run; divergence point named | Comparison record: matched table, pre-registered metrics, declared confounders |
| **Evidence class** (feeds R2-4-08) | Paired-causal (small n) | Randomized-causal | **Divergence-only** for prompt-level changes; causal isolation only for shell variables | Observational-with-declared-confounders |

**The assumption none of the four states, surfaced by the diff:** L6-29's replay isolates a variable's effect only when the variable acts *outside* the pinned leaves. But a `wf:` version change **is** mostly a prompt change — it changes what the model would say, so the cassettes are invalid from the first divergent completion onward. **For the garage's actual change class, full-replay A/B degenerates to replay-to-first-divergence: a regression instrument, not a comparison instrument.** Unrepresented in round 1; produced R2-4-08 and R2-4-09.

**The composition finding:** the four are not rivals; they are one growth path. **L1-35 → (+L2-17 pairing when concurrency exists) → L4-38 as the fleet accumulates**, with L6-29's capture bought incrementally as R2-4-09 (single-run cassettes) rather than as a substrate rebuild. The only genuine tension is L6-29-as-substrate vs the augment>replace bar — it is the "replace" path; the other three are augments.

**Cheapest viable this quarter: L1-35.** What it takes: (1) un-gitignore `settings.local.json` + stamp a config fingerprint per run (L5-26 — near-free, and prerequisite to *all four* attacks); (2) extract L6-30's countable metrics from existing transcripts/Issues (opcost proves the parse path); (3) a one-page pre-registration before the next run; (4) run the next two comparable runs on different `wf:` versions and write the matched comparison with confounders declared. **No new substrate, no probe dependency.** Its verdicts license `claimed`-grade process findings only (per R2-4-08) — but the current alternative is sixteen versions on assertion, and an honestly-bounded weak comparison is the first rung the firewall can accept.

---

## 4. Sub-areas closed (with covering IDs)

- **Improvement generation / anomaly intake** — closed: L1-31, L1-32, L1-34, L4-37, L6-30.
- **Measurement integrity of the loop** — closed: L3-18, L3-08, L3-09, L4-27, L2-05, L2-12.
- **Config identity / attribution substrate** — closed: L2-07, L6-28, L5-26, L3-07, L4-19.
- **Fleet-scale comparison, regression, rollout** — closed: L4-38, L4-39, L4-40.
- **C-3 attack directions** — closed: the four span the design space (simultaneity, scale, determinism, concession); any fifth is a composition. What was missing was the diff (§3), its consumer discipline (R2-4-08), and the degenerate replay form (R2-4-09) — not another direction.

---

## 5. The counter-case, argued honestly

**Split the concern in half; the halves get opposite answers.**

**Against the *comparison/optimization* half — the case largely holds.** (1) **L3's fixed point:** every outcome metric the garage can currently produce is produced by the workflow being tuned; under optimization pressure the A/B machinery would measure Goodhart compliance, not improvement. Measurement-integrity abilities (L3-18, L2-12) are *sequenced prerequisites* of comparison, not siblings — building the loop first is worse than not building it. (2) **The augment>replace bar:** the thorough instrument (L6-29 substrate) requires rebuilding the workflow below the legibility threshold — precisely *"swapping load-bearing machinery mid-maturation."* (3) **Maturity arithmetic:** the fleet designs cannot exist below ~20 runs/arm, and at ~2 improvements/month heavyweight optimization machinery has almost nothing to optimize. **Verdict: for fleet-scale comparison and any optimization loop, "do not build this yet" is the finding** — buy only the augment forms (L1-35 now, R2-4-04/09 cheaply) and let L4's own scale triggers date the rest.

**Against the *adoption* half — the case fails, with one bootstrap caveat.** The recorded failures are not sign errors; they are **total losses** — the retro never ran, the diagnosis changed nothing, the fix landed outside the repo, the config keys were inert. Adoption's cheap end (a target-artifact field, an admission-time acknowledgment, a first-effect check) is checklist-weight, addresses total loss, and — unlike the comparison half — gets *more* necessary at low maturity, because FP-4's compensating control (owner attention) is the only thing currently carrying improvements across any crossing, and it is the resource the garage is explicitly trying to stop spending. **The garage is not short of self-knowledge — 30 pains, diagnoses days ahead of their failures — it is short of uptake.**

**The caveat:** the adoption machinery is itself an improvement that must be adopted; installed as prose it becomes another #179. Its minimum viable enforcement point is run admission (R2-4-05), the one moment the lifecycle already passes through a deterministic gate — and its installation must be **owner-enforced by mechanism, not filed as a finding.** If the first adoption mechanism arrives through the channel whose failure it fixes, the record predicts its fate exactly.

---

## 6. Emergent concerns (§3.3, honest)

**No new concern proposed.** Adoption is not emergent — SCOPE §3.1's Self-improvement definition already names it (*"improvements **adopted** on evidence"*); round 1 under-populated a *seeded* concern's own clause. Filing a new concern would be a re-cut, failing test 2.

**E-1 engagement — support, with one sharpening.** The adoption lifecycle is E-1 machinery applied to the harness's own method: "decided" *is* an obligation to implement; "implemented" an obligation to verify. This strengthens L6-40's promotion argument (another ≥2-capability population: R2-4-01, R2-4-05) and adds the clause round 1's E-1 discussion mostly lacks: **obligations must survive run boundaries and re-arm at successor admission** — close-time reconciliation alone loses exactly the P-19 class, as wfh-004's own SCOPE demonstrates live. L3's anti-tamper clause applies verbatim: a lifecycle register writable by the improving party tracks nothing.

**Considered and not proposed:** "declared configuration = effective configuration" (the crossing-D failure) is a genuine property no seeded concern owns cleanly, but it is one capability (R2-4-03) wearing a hat — fails test 3.

---

**Flags for the leader:** (1) R2-4-05 and R2-4-01 are E-1 population — route to the E-1 promotion file at W6. (2) The §3 diff table and its composition finding is W6/W7 material — ROUND-1-COVERAGE deferred the C-3 diff to distillation; it is now done and should not be re-derived. (3) The cheapest-viable path's first step (fingerprint + un-gitignore `settings.local.json`) is shared prerequisite of all four attacks and already a round-1 candidate (L5-26) — a convergence worth counting. (4) Per §11: nothing here depends on a W0-b ambiguity except R2-4-03's event capture (A-2 adjacent); if triage turns on it, route `needs-a-probe`.
