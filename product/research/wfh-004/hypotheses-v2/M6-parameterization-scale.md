# M6 — Parameterization surface + scale extrapolation

**Run:** `wfh-004` · Issue #48 · rebuild · read-only, zero graph writes. **32 candidates.**
**Read:** BRIEFING-v2 (full), W0-b2 §5, W0-b2b §3 (+ §1 census corrections). Superseded registers **not read** — where mechanisms coincide with ones the briefing names (double-entry, watchdogs), the coincidence is **via the briefing digest, not independent corroboration.**

---

## 1. The parameterization register (headline)

**Method:** per concern — what the harness **fixes** (floor: choosing otherwise destroys the record or the guarantee) vs what a definition **declares** (parameter: two real definitions plausibly choose differently, and where possible *did*). **Boundary test: could a definition sanely choose the opposite?** Parameters with <2 real instances marked **(spec)**.

### Structure
**Harness fixes:** addressable units with attempt identity · **a verdict is drawn from a closed declared alphabet, and an out-of-alphabet verdict is detectable** (the field produced `WARN` leakage 29/553 and a self-invented `CONDITIONAL PASS`) · every declared loop has a declared termination policy the harness enforces · **declared-but-never-executed branches are visible** (SCOPE FAIL 0/231 — the floor test case) · status advances only through its declared evidence predicate.

**Definition declares:**

| Parameter | SDLC | Research |
|---|---|---|
| Atomic unit + addressing | commit/PR/`vnc-048` | finding/workstream/`wfh-004` |
| Phase vocabulary | `spec/develop/test/pr-review` | `scan/hypothesize/triage/formalize` |
| **Verdict alphabet content** *(new)* | `PASS / REWORKABLE FAIL / SCOPE FAIL` (+ un-promoted `WARN`) | `proven / partial / missing / asserted` |
| Loop termination policy | bound-2-then-escalate | **exhaustion-is-done** |
| **Escalation destination** *(new)* | SCOPE FAIL → human + issue | re-spawn for range (≤2), then gate |
| Status alphabet + per-transition evidence predicate | `delivery:*` + behavioral test | `grade:*` + attested artifact |
| **Evidence kind per predicate** *(new)* | **executable, re-runnable** | **attested record of past demonstration** |
| **Routing predicate** *(new)* | by file path/language | confidence field skips feasibility |
| **Fan-out semantics** *(new)* | wave planning, disjoint components | **divergent→convergent phase pair** |
| **Irreversible-operation set** *(new; 2nd instance is ∅ — real but weak)* | publish-on-tag with pre-flight | **∅ — research has no irreversible operation at all** |

### Context provisioning
**Fixes:** injection is phase-conditioned (**the configuration-diff proof — the run's strongest layer datum**) · **the hand-list is recorded prospectively — what an agent was given *and what was withheld*** (absent in both; **proposed floor, because an unrecorded exclusion is unrecoverable later**) · retrieve-before-generate emits a record.
**Declares:** per-role slice content · **reviewer hand-list** (diff-only · agent-ID-only · findings-file-only — **three real instances**) · **retrieval sources per phase** — `uni-research-protocol` forbids all graph access while this repo's research definitions require graph search first: **two real instances of opposite choices.**

### Security
**Fixes:** authority bounded outside the agent · **definition-vs-plane reconciliation** — a definition's claimed platform invariants compared against actual configuration (**floor, because a definition that is *wrong about the world* silently voids every guarantee stated over it**) · spawn-chain identity carried in-band · tenant separation.
**Declares:** the **write-authority matrix, role × resource × phase** — the phase dimension is new with two real instances (bugfix's "outputs are GH comments, never the filesystem"; research's "no knowledge writes until after convergence") · verifier class per gate **including whether a platform-recorded human signature is required** (available, never used — so it must be *per-transition* declarable, not global) · **reader-kind diversity requirement per review chain** · boundary predicate content.
**(spec):** anything about an attacker model — zero adversarial incidents; mechanism-only territory.

### Introspection
**Fixes:** **the run is an addressable object** with its own status, distinct from pipeline and repo · attempt history enumerable, verdicts immutable · **artifacts are self-describing** (typed, schema-versioned) — **the filename-census FP-3 reproduction is a direct demonstration that filename heuristics as the census instrument produce confident wrong numbers** · verdicts typed by producing verifier class · **store concordance is computed** (71/78/79/**44**%).
**Declares:** report/check-table content templates · which stores claim to describe the run.

### Cost
**Fixes (proposed — both domains are C, so floor-by-argument not floor-by-instance):** every model call and verifier run attributed unit→run→tenant. **The argument: 610 issues, zero cost incidents = absence of *record*; an unmetered concern cannot even have definition-layer parameters, because there is nothing to parameterize over.**
**Declares (all spec):** budget unit · attribution grain · breach action. **Honestly flagged: conjectural until one metered run exists.**

### Self-improvement
**Fixes:** **the retro's firing is itself verified** — 62/63 units carry no retro trace *despite the tool existing*, so **the trigger being conventional is the failure; a learning step whose non-firing is invisible is not a loop** · every outcome carries the configuration identity that produced it.
**Declares:** the lifecycle event the retro binds to (PR-merge vs cycle-close) · what the version stamp identifies (product vs method) · **(spec)** adoption policy.

### Recovery
**Fixes:** a unit with no liveness signal inside its budget is **declared dead, not silently lost** · OS processes owned by their unit and reaped at unit end (26 orphans / 6 sessions) · **declared escalation branches are exercisable on demand** (**an escalation path that has never run is a belief, not a capability**) · parked work carries a machine-checked re-entry condition.
**Declares:** liveness predicate/heartbeat budget · checkpoint grain · **undo semantics per resource — true rollback vs append-with-supersession** (git revert vs correction-lineage: **two real instances of structurally different reversal**) · re-entry predicate content.

### Human steering
**Fixes:** a blocking checkpoint exists and a **may-not-ask rule is expressible** · every human answer lands as a **typed, recorded decision, not prose** · **(proposed floor)** a question to the human is a first-class object with a latency budget and a declared expiry default.
**Declares:** per-gate block-vs-surface · non-askability rule content · which transitions require a platform-recorded signature · **(spec)** latency values and silence defaults.

**Boundary-test worked examples:** attempt identity — a definition "choosing" mutability destroys the record for every consumer → **floor**. Verdict alphabet — two definitions demonstrably run different alphabets → **parameter**, but *closed-ness* is floor. The ≤2 rework bound — the *policy* is a parameter, and **the *constant* is too: the "independent convergence on 2" is weaker than it looks** (see calibration caveats).

---

## 2. Candidate register (32)

**Structure/verdicts:** **M6-01** closed verdict alphabet enforced at recording · **M6-02** distinct immutable verdict record per attempt (**R: none / S: negative — mutable file, ≥53 overwritten**) · **M6-05** verdict typed by producing verifier class · **M6-06** status advances only on its declared evidence predicate · **M6-07** evidence recorded as *executable predicate* or *attested artifact*, distinguishable in queries · **M6-08** declared evidence-decay: statuses expire or re-confirm on schedule *(spec — no decay policy in either domain; `proven` is currently forever)* · **M6-09** loop termination policy declared and engine-enforced · **M6-15** routing predicate over recorded attributes, decision recorded · **M6-31** fan-out semantics declared · **M6-33** irreversible ops execute only after declared ceremony, ceremony record preceding the op in the durable log · **M6-34** verdict recorded attributable/bounded/timestamped **before** its dependent action, machine-checkable — *(**20 PRs merged before their last check completed** — ordering violated in the field)*.

**Introspection:** **M6-03** never-executed branches reported **and any declared branch exercisable via synthetic trigger** · **M6-18** per-field concordance computed between stores claiming to describe the same run · **M6-19** self-describing artifacts — **a corpus census computable without filename heuristics** · **M6-20** the run as an addressable object, one query returning phase/live agents/open obligations/attempt states/spend · **M6-24** structured defect→origin back-links with continuous compounding-rate rollup (*the 52% and 22-file figures exist only because someone hand-censused once*) · **M6-27** full spawn chain on every action (**the shared-origin spine item**).

**Security:** **M6-04** definition-claimed platform invariants periodically diffed against actual plane configuration · **M6-10** out-of-authority write (role × resource × **phase**) blocked before effect · **M6-11** concurrent writes to a declared-serialized resource queued, order total and recorded · **M6-13** withheld-context reviews spawnable as a primitive, verifiable as such · **M6-14** **a review chain where every layer is the same verifier kind is reported non-independent before its verdict is consumed** · **M6-29** tenant isolation evidence generated from configuration rather than prose · **M6-30** out-of-boundary actions detected against the declared predicate and recorded (**D for path-shaped bounds; I for semantic — record-and-flag, don't auto-block, on the I part**).

**Context:** **M6-12** spawn record states what was handed *and what was withheld* · **M6-32** retrieve-before-generate emits a receipt a definition can gate on.

**Cost:** **M6-25** every model call and verifier run attributed unit→run→tenant, **a per-tenant statement a stranger accepts** · **M6-26** budget breach triggers the declared action, execution recorded *(spec)*.

**Self-improvement:** **M6-17** retro-coverage rate computed over closed units; **non-firing is visible**.

**Recovery:** **M6-21** unit with no liveness signal declared dead, loss recorded · **M6-22** every OS process owned by its unit and reaped, **zero orphans observably** · **M6-23** concurrent units declare disjoint machine-state footprints or are placed so collision is prevented, not observed.

*(Consolidations: escalation-destination folded into M6-09; branch-coverage + fire-drill share M6-03.)*

---

## 3. The step-function list — changes of *kind*

1. **Convention → enforcement.** Threshold: (1 − compliance) × volume ≥ 1 event/period. **A convention has a compliance rate; enforcement has none.** Measured: **98.3% discipline → 6 red merges at 354 PRs; at 3,540 PRs that is 60 — same discipline, different outcome, nobody changed anything.** `field`
2. **Review-by-reading → review-by-exception.** Threshold: units × read-minutes > owner attention. **Human attention is the one non-scaling resource in the system. Already breached: 62/63 units have no retro trace — the reading-based loop collapsed at *current* volume.** `field`
3. **Attribution reconstructable → carried in-band.** Threshold: spawn depth ≥2. Reconstruction cost is per-query and grows with history; in-band carriage is per-action and constant. **Sharpest evidence in the run: #208 predates P-05/P-06 by four months — the defect was *known* and still crossed domains, because knowing is not carrying.** `field`
4. **Single-writer → declared authority + serialization.** Threshold: write demand > one writer's throughput. W0-b2 states it outright: the curator rule *"does not scale to 359 changes."* `field`-adjacent
5. **Ask-the-owner → latency-budgeted queue where silence is a decision.** Threshold: concurrent runs >1. **A blocking question makes run duration unbounded by design; at fleet scale unbounded duration × held resources = unbounded cost.** Zero field evidence **and there can be none yet** — the blind spot is structural. `reasoned`
6. **Isolation believed → isolation demonstrable.** Threshold: **first stranger tenant.** Within one owner, trust substitutes for evidence; **a stranger cannot inherit trust, only verify attestation.** `reasoned`
7. **Retry-forbidden → idempotency-mandatory.** Threshold: fleet size where P(≥1 failure/run) ≈ 1. **W0-e lists idempotent retry as a model *cannot-in-principle*, therefore retry semantics must live entirely in the harness — the component can never supply them.** `reasoned` on `field` premise
8. **Anecdote → base rate.** Threshold: volume where a rate is estimable — 63 bugfixes already yields 52%. **This run's own FP-3 reproduction demonstrates hand-counting at this corpus size already fails.** `field`
9. **Records-as-files → self-describing records.** Threshold: corpus size where filename heuristics are the only census instrument — **already there.** `field`
10. **Shared machine → supervised processes.** Threshold: >1 concurrent session per machine — **the *measured* threshold: 26 orphans at 6 sessions.** `field`
11. **Unmetered → metered-and-attributed.** Threshold: tenant ≥2. **A bill is a contract; a contract needs a number a stranger accepts. "Zero cost incidents in 610 issues" is what the absence of an instrument looks like, not what solvency looks like.** `field` absence-of-record

---

## 4. The dissolved-at-scale list

1. **"Parallel spawn in one message" as an instruction** — **a workaround for the absence of a scheduler. The convergence of all five definitions on it is convergence on a *hole*, not a principle.**
2. **Process-compliance gates that read prose** — the whole model-judged-but-mechanizable column. If the engine sequences phases and holds obligations, *"did the roles run"* is a **query**. **The (P) reservoir dissolving wholesale — the largest single inference-removal in the run, and it costs nothing at generation time because the information was always producible at source.**
3. **Manual retro invocation** — the 1/63 firing rate says it has *already* dissolved; it just wasn't replaced.
4. **Path conventions as isolation** — a rule policing what a boundary would prevent is pure compliance-rate liability.
5. **The human signature on every merge** — dissolves *as a universal* into review-by-exception; survives as the exception class and at declared-irreversible ops. **Note the current operation already abandoned the platform-recorded half (0/359 APPROVED) without replacing it — the worst of both.**
6. **The ≤2 rework constant** — the right bound is *measured per configuration*; **the constant dissolves into a tuned parameter. What survives is that a bound must exist and be engine-held.**
7. **The curator single-writer role** — dissolves per W0-b2's own statement. **What survives is the *declarability* of a serialization constraint.**
8. **Filename conventions as artifact typing** — the census errors prove they are already past their load limit.
9. **"Agent Context Budget" as pasting prose** — dissolves into metered injection.

**Deliberately not on this list:** context-starved reviewers — **scale *strengthens* it, since fresh context is the one independence source that gets cheaper, not dearer, with volume.**

**The honest counter-cut:** **SDLC's own record shows infrastructure does not automatically survive its scale** — the 10× domain had more machinery and its instruments were still wrong (44% concordance; an alarm returning PASS unconditionally; a hand census producing a phantom finding). **The correct extrapolation is not "scale needs more machinery" but "scale needs machinery whose own firing is verified"** — which is why M6-03/17/18 sit in the register rather than being assumed.

---

## 5. Coverage and calibration

**By concern:** Structure richest (01/02/05/06/07/09/15/30/31/33/34) · Context (12/13/32) · Security (04/10/11/13/14/27/29/30/34) · Introspection (02/03/18/19/20/24/27) · **Cost thinnest — both parameters speculative, unavoidable because the concern is unmeasured in both domains: a hole in the world, not the lens** · Self-improvement (08/17/24) · Recovery (03/09/21/22/23/33) · **Human steering (28 + block-vs-surface) — partially reasoned-only; mid-run steering failure is unobservable in principle until steering exists.**

**E-1 engaged**, populated by M6-16 from both domains (xfail→issue + doc-trigger table + stewardship checks SDLC-side; prose commitments research-side), with 62/63 as its base rate.

**Proposed, AMBIGUOUS — E-2 "world concordance":** *the system's descriptions of itself and its platform match reality, verified continuously.* Populated by M6-04 (definition-vs-plane), M6-18 (store-vs-store), M6-03 (declared-vs-executed). **Argued both ways:** it may reduce to Introspection (all three are "look and compare"); **against reduction — Introspection as seeded asks *what happened*; E-2 asks *whether the instruments that answer that question are themselves telling the truth*, and every census failure was a failure of exactly that second-order property while first-order introspection looked healthy.**

**Calibration caveats — the narrow base, named:** (1) **All five definitions are one owner's authorship** — "independent convergence" is convergence of two traditions under one mind, **materially weaker than two organizations; the ≤2 constant especially.** (2) **One model family** — the dangerous-middle rates, the 52%, and every rework intuition may be model-specific. (3) **One toolchain** — the "free-for-SDLC" list is really free-*if-GitHub*; the tenancy and multi-owner extrapolations rest on **zero** field data. (4) **Regression flag honored:** M6-28 is the one candidate whose naive form can *lower* security — a timeout waving through a gate — so **the default's safe direction must itself be declared, fail-closed.**

**Flags:** M6-33's falsifier ("would the pre-flight have caught the uninstallable release?") and M6-30's ("how many boundary events actually occur in 231 units?") are **cheap, unclaimed probes against the existing corpus.**
