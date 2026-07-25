# M4 — Cross-domain recurrence spine

**Run:** `wfh-004` · Issue #48 · phase `hypothesize` (rebuild) · read-only, zero graph writes.
**Read:** BRIEFING-v2, W0-d, W0-d2, W0-f, W0-b2, W0-e, SCOPE A-6/A-7/A-8. **Did not read the superseded registers** — nothing here is contaminated by, or corroborated by, that round.

---

## 1. The recurrence register — the run's spine

Fourteen rows tracking W0-d2 §2, **with three pairings corrected in §4 rather than silently accepted.**

**R-1 — Records unbound from the unit that caused them** *(P-05 ↔ S-21/#208 — shared origin, SDLC first by 4 months)*
**Failure:** work performed inside a spawned execution context produces records not bound to the initiating unit; the run's own accounting cannot enumerate what its sub-executions did. **Ability:** every durable record created during a run is bound **at creation** to the unit-of-work identity that caused it — observable as a per-unit enumeration matching an independent count. **Surface: (P)** — the parent held the child's identity at spawn and discarded it at the boundary → capture makes it **D** (a query, not an inference). **Research:** "Stored: 0" against 38 demonstrated writes; instrumentation present and working. **SDLC:** #208 *"session topic attribution misses feature work done via subagents"*; attribution consumed **20+ issues over 5 months**, still open. **Evidence:** P-05 [R] · S-21 [R]. **Falsifier:** a pilot that propagates identity and still diverges from an independent count — that would show the loss is producer non-emission (the P-15 class), not boundary discard.

**R-2 — Actor identity discarded to restore throughput** *(P-06 ↔ S-11/#46 — causally identical; the strongest row)*
**Failure:** when a role's authorization blocks its work, the repair applied is **re-identifying the actor** rather than granting the role authority; the record then cannot say who acted, and no record of the trade travels with the writes. **Ability:** actor identity is preserved end-to-end — every durable effect is queryable by the role that produced it, and an authorization failure is observable as a **refusal attributed to the role**, never as a write under a different identity. **Surface: (P)** → **D**. **Research:** `created_by: anonymous` on every graph write; single-writer firewall unauditable. **SDLC:** #46's shipped workaround; S-23 — all 359 PRs authored/merged as the human. **Evidence:** P-06 [R] · S-11 [R] — **one defect, two surfacings.** **Falsifier:** identity preserved and never consumed by any audit — S-21's 20+ issues argue against.

**R-3 — Role instantiated below its contract** *(P-09 ↔ S-11, capability half)*
**Ability:** at instantiation the granted capability set is compared against the role's declared contract — observable as a refusal **before** the role starts, and a zero rate of mid-run "tool missing" discoveries. **Surface: D** as a set comparison; **(P)** today only because contracts are prose. **Research:** leader spawned without Task in both wfh-001 converge legs. **SDLC:** agents auto-enroll `Restricted`, blocked from writes their contract requires. **Falsifier:** mismatches occur but never bite — contradicted by both instances, each of which stalled work.

**R-4 — Unit death invisible beneath process health** *(P-10 ↔ S-08, also #158)*
**Ability:** a unit that stops emitting is declared dead within a declared interval — observable as a state transition and alarm occurring **with no human noticing first**. **Surface: D** — heartbeat/timeout, no semantics. W0-d's layering split holds: detecting *whether* needs no addressing; resuming *which* needs R-1's identity. **Research:** specialist died at turn end, 0 bytes; resumed on a manual nudge. **SDLC:** fire-and-forget maintenance tick — one panic stops all maintenance forever while the server keeps serving; *"no observable indication."* **Falsifier:** deaths would all have been caught at the next gate at no marginal cost — record contradicts: S-08's cost is *permanent* staleness.

**R-5 — A declared step can leave no trace and the workflow completes anyway** *(P-13 ↔ S-01/S-02 — census-backed)*
**Ability:** at a unit's terminal transition the declared step set is diffed against recorded executions — observable as a block or flag listing missing traces, produced **without any human reading anything**. **Surface: D** (set difference) — **(P)** today: declarations are prose and traces split across unreconciled stores. **Capture requires execution recorded *independently of the role's own output*** — W0-f §6 is explicit that nothing in the corpus can distinguish "unrecorded" from "did not run." **Research:** no hypothesizer ran; the run reported its funnel anyway; the gate graded its own inputs. **SDLC:** 3–4/63 bugfix units missing traces; 5/161 feature units shipped without declared gates; S-01 — coordinator prose consumed as if the role had produced it. **Evidence:** P-13 [R] · S-02 **[V, census]** · W0-f **[V, census]** — **the best-evidenced row.** **Falsifier:** W0-f's time series — all 5 feature-side failures in one 30-day window, **none since April; 100% May–Jul**. If discipline self-heals, the ability detects an extinct mode. *Counter-weight: the bugfix side still shows 2/61, "no artifact anywhere" remains uninterpretable without independent recording, and the 30-day window went undetected for months.*

**R-6 — A declared quantitative bound unchecked at the moment of the bounded action** *(P-12 ↔ S-12)*
**Ability:** a declared bound is evaluated **at the moment of the bounded action** — observable as a write-time refusal or flag, plus a breach ledger with counts. **Surface: (P) → D.** **Research:** 17 authorized, 33 written, never reconciled. **SDLC:** the 500-line cap *"waived on every feature"*; 12× cap; seven refactor issues filed the day someone finally measured. **Falsifier:** S-12's waiver channel — if post-enforcement every breach is waived, write-time checking converts silent breach into rubber-stamped breach and buys only the ledger. *(The ledger is not nothing: the seven-issue day happened only when the ledger finally existed, by hand.)*

**R-7 — An obligation declared at close has no carrier** *(P-19 ↔ S-24 — the E-1 core)*
**Ability:** a declared obligation is a record with a carrier and a due-condition; unmet obligations surface at their due-condition — observable as a standing list that empties **only by fulfillment or explicit cancellation**. **Surface: (P) → D.** **Research:** wfh-002 closed *on a process defect* with its retro "not performed, not partially performed"; the successor's SCOPE carried no retro workstream. **SDLC: 62/63** bugfix units carry no retrospective trace [V, census]. **Falsifier:** tracked obligations get ignored by the same discipline that dropped them. **Supporting mechanism detail:** the **one** deferral in the corpus that *did* carry (crt-043's deferred tests → #505, closed 3 days later) is exactly the one filed as an addressable artifact rather than left as prose.

**R-8 — The instrument on the load-bearing path was wrong, and nothing exercised the instrument** *(P-16 ↔ S-06 — same class, not same mechanism; §4)*
**Ability:** every instrument on a measurement or enforcement path is periodically exercised against a known-answer case **whose answer was derived independently of the instrument's own definition** — observable as a recorded instrument-check verdict distinct from the instrument's output. **Surface: D** given a fixture, with the independence condition. **Research:** 61× cost undercount; caught only because a POC built an independent instrument on suspicion. **SDLC:** `setsid` without `-w` → **every failing suite and every timeout read PASS**, in the very fix meant to restore gate-signal integrity. **Falsifier:** if fixtures are authored by the same party from the same metric definition, the check is correlated — catches the S-06 class but not the P-16 class.

**R-9 — A defective artifact consumed downstream before any check ran** *(P-14 ↔ S-04 — pairing SPLIT; §4)*
**Ability (a), covering P-14:** an artifact is checked for **machine-decidable validity** — duplicate sections, inconsistent counts, missing verdict line — before a consumer may act. **Surface: D.** **Ability (b), covering S-04:** a review layer added to a verdict path is of a **different kind** than layers already on it — observable as a recorded disagreement rate between unlike readers. **Surface: I** — a wrong-but-coherent diagnosis is semantic; **independence must be bought, not stacked.** **Research:** triage report with §6 duplicated, two different recommendation lists, three inconsistent counts; curator acted on one; undetected 3 days. **SDLC:** #944 — wrong diagnosis ratified by a design reviewer **and** an independent product reviewer; the human caught it.

**R-10 — A stateful external connection fails silently; a human is the reconnect mechanism** *(P-22 ↔ S-22/#830 — literally the same defect)*
**Ability:** a failed dependency connection is detected and re-established, or the stall alarmed within a declared interval. **Surface: D.** **Research:** ~4 stalls in one run; **the access rules still instruct agents to reconnect manually — a standing manual dependency written into the method.** **SDLC:** #830, same client, same behavior. **Falsifier:** stalls a reconnect cannot clear dominate — record says otherwise.

**R-11 — Backpressure stops a declared batch partway and nothing carries the remainder** *(P-24 ↔ #178/#111)*
**Ability:** work refused by backpressure is queued with a due-condition and completed when the ceiling lifts. **Surface: D.** **Likely the same ability as R-10 parameterized** (transient-fault continuation: reconnect-now vs defer-and-resume) — stated for triage, not decided. **Research:** 57 tagged, 3 deferred; **filing policy now shaped by the limit.** **Falsifier:** ceiling hits rare enough that the queue never fires — but the deeper cost is the policy reshaping, which a queue also reverses.

**R-12 — Partial effect reported as success** *(P-25 ↔ #879/#744 — pairing downgraded; §4)*
**Ability:** an operation's completion report enumerates its effect delta — done, skipped, dropped, with counts — and a nonzero skip is surfaced to the caller. **Surface: (P) → D** trivially: **the engine demonstrably knew what it skipped (it logged it).** **Research:** `context_correct` silently skipped incoming edges; count never stated. **SDLC:** `REDIRECT_CEILING=50` *"silently orphans referrers 51+."*

**R-13 — Context omission invisible to the agent and to the run** *(P-27/P-28 ↔ #944 v1 — corrected pairing; §4)*
**Ability:** every context assembly emits a manifest of what was considered, included, and excluded — observable as an inspectable record a checker can diff against the unit's declared need-set. **Surface: (P)** for the manifest — the assembler knew what it had and chose from it. **(I) residual, honestly:** *whether an excluded item was load-bearing* is semantic; **the manifest converts a silent omission into an inspectable decision, which is the whole claim.** **Research:** substrate omitted → half yield; corrected surface **doubled** non-obvious survival. **SDLC:** #944 v1 traced the retired oracle and could not see the omission. **Falsifier:** manifests never read — P-28's mechanism argues otherwise: the owner caught the omission precisely by comparing what was handed against what existed.

**R-14 — A written execution constraint crossed by the run's default behavior** *(P-03 ↔ S-10)*
**Ability:** declared constraints are registered in a form the harness evaluates **before** the constrained action — observable as a refusal at the moment of violation and a ledger of blocked attempts. **Surface:** mostly **(P)**; S-10's sequencing directive is **D** once "single atomic cycle" is a typed execution mode instead of a sentence. **The F-10 mechanism — terminal constraints drop first, and prose constraints live exactly there — is the *why* behind both.** **Research:** W6 decided an explicitly out-of-scope question; the run closed early. **SDLC:** the brief said "single atomic feature cycle"; the parallel worktree pattern overrode it — 4+ forks, 126 compile cycles, 4 orphaned worktrees. **Falsifier:** typed constraints get routed around exactly as prose ones did. **Untested in-house** — external refusal has never once been tried in research, and SDLC never switched its plane on. **The falsifier requires a pilot; the census cannot pre-answer it.**

---

## 2. Candidate register

**M4-01…M4-14** are the recurrence rows as candidates (fields per the R-rows above). Highlights of their non-repeated fields:

- **M4-01** (R-1) *Introspection · HARNESS · both-identically* — **Inc:** research nothing (D6 live >1 month); SDLC 20+ failed attempts at the app layer say the incumbent cannot retrofit it from outside the boundary.
- **M4-02** (R-2) *Security/Introspection · HARNESS* — **Inc:** SDLC's platform identity plane exists and is unused: an **integrate** case for SDLC, a **supply** case for research.
- **M4-03** (R-3) — security ↑ too: the same comparison detects **over**-grant, not just under-grant (untested, reasoned).
- **M4-04** (R-4) — **Inc:** process supervision exists *below* the unit altitude and health checks *above* it; **the unit altitude is empty in both.**
- **M4-05** (R-5) — **Inc:** SDLC's merge could carry this check and does not (98.3% discipline).
- **M4-06** (R-6) — **both-differently — parameterization: whether a waiver channel exists and who may grant it** (SDLC has one and it ate the rule; research has none and the breach was silent).
- **M4-07** (R-7) *E-1* — **Inc:** SDLC's xfail-with-mandatory-issue is the one incumbent instance of the mechanism, definition-authored and gate-verified; research has nothing.
- **M4-08** (R-8) — **Inc:** zero in both; **no instrument in either corpus has ever been exercised against a known answer; both wrong instruments were caught by accident.**
- **M4-09a** (R-9a) — lint against declared template. W0-f found 29/719 unparseable verdicts, 89/553 missing check tables — **the rate is not zero.**
- **M4-09b** (R-9b) — **the harness can express "this gate requires an unlike reader"**; the disagreement rate is the instrument; **a same-kind stacked layer provably bought ~nothing.**
- **M4-10 / M4-11** (R-10/11) — **Inc:** the incumbent's written remedy is *"reconnect manually"* — **the manual step is documented as method.**
- **M4-12** (R-12) — the information exists in engine logs on both sides; **no path to the actor.**
- **M4-13** (R-13) — **the concern where every failure was caught by the owner, never by the system — the only concern with no detector at all.**
- **M4-14** (R-14) — security ↑: **P-04's "violations are undetectable *as* violations" inverts.** Inherits the §11 ambiguity on both sides.

### Census-derived (W0-f)

**M4-15 — Immutable attempt identity for gate records.** Every gate attempt produces a distinct, immutable, addressable record; **the visible failure rate equals the actual failure rate.** *Introspection · HARNESS · D* · **Both-differently — parameterization: which artifact classes are attempt-scoped**; research's graph substrate is already append-with-supersession, its *file* reports are not. **Inc: git actually holds the overwritten verdicts** (`git log --follow`), so for SDLC this may be **surface-what-the-plane-already-preserves**, not supply. **Ev:** ≥53 overwrites; 6.9% visible vs ≥13.9% actual; **the one surviving FAIL survives by accident of a duplicate-filing convention.** **Fa:** if `git log --follow` recovers the history cheaply, the supply-side version is redundant for any git-backed definition — **run that measurement first.**

**M4-16 — Exercised-control telemetry.** Per declared enforcement branch, its lifetime execution count; **a branch with zero executions is reported as *unfalsified*, not verified.** *Introspection/Self-improvement · HARNESS · D* · **Ev:** SCOPE FAIL 0/231 [V]; research's corollary — no blocked-attempt record *can exist*. **Fa:** cannot distinguish "never needed" from "cannot fire" — **composes with M4-08 (drill it) rather than standing alone.**

**M4-17 — Closed verdict vocabulary at the branch field.** The one field an orchestrator branches on accepts only declared literals. *Structure · HARNESS; vocabulary is DEFINITION · D* · **F-2 says small fixed label sets are precisely what the model side is good at — this leaves the verdict judgment on the model and takes the vocabulary off it.** **Ev:** 5.2% nonconformance at the branch field; ≥4 circulating verdict values the definition does not contain, including the one that shipped crt-043. **Fa:** forced vocabulary squeezes nuance into free-text qualifiers beside the field (`PASS (3 WARNs)` is already this) — **measurable.**

**M4-18 — Terminal transition blocked on declared-artifact existence.** *Structure · HARNESS · D* · **The crt-043 case needed only this.** **Does not claim execution-verification** — an artifact can be forged by the same author; that is M4-05's job and the two compose. **Inc:** SDLC's merge is the natural attachment point and checks nothing; research has no terminal transition primitive at all.

**M4-19 — Machine-joined claim-to-artifact resolution.** Every claim row citing an artifact (a coverage row citing a test; a `proven_by` citing an artifact) is machine-joined to that artifact's existence and content — vacuous rows flagged with **no human reading**. *Introspection/Structure · HARNESS* · **The crt-056 validator performed exactly this by hand, by reading, and named it a recurring pattern.** D for existence/assertion-presence; the residual "does the test assert the *right* thing" is I and deliberately left. **This is the research firewall's own `proven_by` discipline generalized.** **Ev:** vacuous coverage is one of three failure classes structurally invisible to "run a reviewer," **and the only machine-checkable one.**

**M4-20 — Definition self-consistency lint.** A workflow definition is validated before runs execute on it — every artifact class has exactly one declared sink; every referenced verdict literal is declared. *Structure · **HARNESS — linting the DEFINITION layer is itself a harness ability*** · **Ev:** the bugfix protocol contradicts itself (line 389 vs 631) and the field split 2:1, **making absence uninterpretable**; W0-b's 12-item ambiguity register on the research side. **Fa:** if definitions stay prose the candidate is inert — a dependency finding, not a falsification.

**M4-21 — Counts carry their case definition.** A reported count is bound machine-readably to its case definition and denominator; mismatched comparisons are flagged. *Introspection · HARNESS · D* · **Ev: FP-3 reproduced inside the run measuring FP-3** — the file-vs-unit error read as a major finding until a second census; P-16's 61× entered the findings chain the same way. **Fa:** reporters route around the overhead by keeping numbers in prose — **enforcement locus determines whether this candidate exists at all.**

### Asymmetry-derived

**M4-22 — Unit-to-caused-defect back-links.** A defect record names its origin unit, queryable both directions. *Self-improvement · HARNESS* · **The prose already names the origin 52% of the time — this captures what is being discarded.** Judgment stays I; **recording and aggregation is (P)→D.** **Both-differently:** SDLC's defects compound in the *substrate*; research's compound in downstream *inputs*. **Ev:** 52%; 22 files fixed by ≥2 bugfixes; 44/53 shipped through the full pipeline.

**M4-23 — One authoritative surface for "did role X run on unit U".** *Introspection · HARNESS · D* · **Ev:** verify/test store agreement **44%** [V, census]. Research's file-vs-graph seam is the same split-store shape. **Fa:** if M4-01's at-creation binding lands, **this is subsumed — possibly one ability at two capture points.**

**M4-24 — Work products durable and addressable by default.** *(the P-20 restatement the charter posed)* Every intermediate work product is durable and addressable **at the moment of creation, without its author acting to persist it** — observable as a resuming agent retrieving prior state by address rather than re-deriving it. *Context/Recovery · HARNESS · D* · **Mechanism:** what git supplies SDLC by construction, generalized. **Both-differently — the largest supply/integrate asymmetry:** research demonstrably lacks it (OBS-7: specialist output exists only as inline markdown until a leader persists it — **binding on this very document**). **Fa:** #944's three investigation rounds are re-derivation *with* durable artifacts — **durability converts memory into lookup but does not eliminate re-derivation.**

> **The charter's question answered:** the ability is **"the work product is the memory"** — durable-and-addressable-by-default, with session continuity as its *consequence*, not its statement. **Session-continuity-as-ability would be a HOW smuggled into a WHAT** (it presupposes sessions as the persistence mechanism).

**M4-25 — The run as an observable object.** The run exists as an addressable object whose declared invariants are evaluated **at run altitude**; run-level alarms fire with zero human reading. *Introspection · HARNESS* · **Mechanism:** both pain records verbatim — *nothing observes the run as an object; SDLC adds one observer (CI) at the wrong altitude* — every census-backed failure happened with CI green, **including the one where the alarm itself returned PASS and CI could not tell.** **Honest note:** this may be the *composition* of M4-05/06/07/18/23 rather than an atom — **but the census suggests the altitude itself is the missing thing, not any single check**, so it is filed rather than dissolved. **Ev:** 6/354 merged red, 20 merged pre-completion, 105/610 issues open since February.

**M4-26 — Verified properties of the bound-to plane.** When the harness binds a declared unit/gate/verdict to an external plane, it **verifies — not assumes — the plane properties it depends on** (enforcement switched on, append discipline, uniqueness). *Security/Introspection · HARNESS · D* · **Ev: the run's headline discovery — the borrowed enforcement was believed on and was off** (98.3% discipline, `reviewDecision: ""` on 359/359, rulesets empty); and the append-ness everyone assumed of gate reports was absent. **Fa:** if plane properties are stable once set, a one-time checklist beats a standing ability — **measured by config-drift rate, which nobody has measured.**

---

## 3. The asymmetry analysis — supply versus integrate

| Pain | What the plane supplies | The harness residue |
|---|---|---|
| P-07 | A merge *requires* a PR — proof-of-completion at the **unit-terminal** altitude only | Role-altitude artifacts uncovered: S-02's merges with no gate trace went straight through. **Integrate at the terminal; supply everything below it** |
| P-08 | Branch/PR uniqueness by construction — 0 duplicates in 359 PRs | Research: supply. SDLC: pure integrate |
| P-11 | git+GH index everything committed | **The split-store problem reappears as store-vs-store disagreement (44%)** — indexing is supplied, **reconciliation never is** |
| P-21 | The merge is a hard terminator | Research: supply a terminal-transition primitive. SDLC: integrate |
| P-26 | Only the *PR* self-alarms | 105/610 issues open since February — **staleness generally is supplied by nobody** |

**The formulation under test** — *"the harness binds a declared unit/gate/verdict to whatever external plane the domain already has, and supplies that plane only where the domain has none."*

**Verdict: right in direction, wrong in two places, incomplete in one.**

1. **"Whatever plane the domain has" assumes the plane's properties are on.** The merge gate is a 98.3% discipline; branch protection unreadable/empty; APPROVED never used; gate-report files mutable with ≥53 FAILs overwritten. **Binding to a plane inherits its *configuration state*, and configuration is not physics.** Needs a verification clause (M4-26).
2. **The unit of binding is the artifact class, not the domain.** One domain's plane covers PRs and not issues; merges and not role artifacts. *"The domain has a plane"* is too coarse to be the branching condition.
3. **Incomplete: no plane in either domain supplies the run-altitude observer.** CI observes the pipeline; git observes the bytes; **nothing observes the run.** That part the harness *always* supplies, in both domains.

> **Improved formulation:** *Per artifact class, the harness binds declared units/gates/verdicts to an external record plane where one exists and supplies one where none does; in either case it **verifies rather than assumes** the plane properties it depends on — immutability, uniqueness, enforcement actually switched on; and **the run-altitude observer it always supplies**, because no incumbent plane in either domain has one.*

**The seven SDLC-only modes — what they demand of a domain-general harness anyway.** Irreversible publication → *actions carry a declared reversibility class, and irreversible ones require their gate traces to exist first*. Credential-through-one-way-channel → *emissions into channels declared irreversible are checked against a declared exclusion set before emission* (S-15's near-miss needed exactly one such check). Shared-machine-state collisions → *isolation keyed on the unit's declared write-scope*. Cascading-dependency parallelism → *units carry declared dependencies, and "the harness cannot tell which case it is in" becomes a lookup* (S-10's 126 compile cycles are the price of not knowing). Isolation-breaking-identity → *unit identity must not be derived from substrate the isolation mechanism mutates*. Compounding defects → M4-22. Test-asserting-a-defect → M4-08 plus provenance on the asserting artifact. **None is generatable from research field evidence — they are the reason the second domain was worth the rebuild.**

**The sobering datum, answered.** What does "enforcement at the wrong altitude" imply that "no enforcement" does not? Three abilities more enforcement would not supply: **(a) altitude binding** — the alarm attaches to the unit/run, not the pipeline (M4-25); **(b) exercised-control evidence** — a control's execution count is itself an observable, and zero means unfalsified (M4-16); **(c) independence of kind, not count** (M4-09b). *"No enforcement" implies "add some"; "wrong altitude" implies these three — and the SDLC corpus is the only place that lesson could have been learned, because research never switched anything on to mis-aim.*

---

## 4. Corrections — pairings weaker than claimed

1. **P-16 ↔ S-06: "same class," not "SAME."** P-16 is a metric-definition error (the addressing worked); S-06 is a status-capture mechanism bug. R-8 holds, but **one ability covers both only with an independence condition on the fixture**: a fixture derived from the same metric definition catches S-06 and sails past P-16.
2. **P-14 ↔ S-04: one pairing, two abilities.** P-14's defect was machine-decidable (a lint); S-04's was a coherent wrong diagnosis — no lint sees it, only bought independence does. **One failure statement, two preventing abilities with different inference surfaces (D vs I)** — split into M4-09a/09b. *This is the parameterization-vs-two-abilities call the method asks for, and here the answer is two abilities.*
3. **P-27/P-28 ↔ S-18: the S-18 half is mis-paired.** #944 v1 is P-28 verbatim and carries the pairing alone. **S-18 is a *provenance-of-change* failure, not a context-omission failure** — re-filed as provenance evidence. **The 14-of-30 count survives; the row's evidence column narrows.**
4. **P-12 ↔ S-12: shape holds, mode differs.** P-12's breach was silent; S-12's were **acknowledged and waived** — a live enforcement branch that rubber-stamped. The parameterization (waiver channel: exists/absent, who grants) is the interesting part. Keep the pair, **weight it below the census-backed rows.**
5. **P-25 ↔ #879/#744: downgrade from "SAME."** #744's ceiling-orphaning is *documented, designed* behavior; P-25's skip was undocumented. **"Same shape, different intentionality"** — and the designed case argues the fix is surfacing, not prevention.
6. **A time-bound the spine must carry:** W0-f's series confines the feature-side gate-skipping failures to one 30-day window, none in the last three months. **Any candidate whose case rests on gate-skipping being *ongoing* (M4-05, M4-18) must cite the census rate with that bound, or it commits the run's own FP-3.**

---

## 5. Coverage statement and emergent concerns

**Populated:** Structure (R-5/6/14; M4-15/17/18/23) · Introspection (R-1/2/8/12; M4-16/19/21/25) · Recovery (R-4/10/11; M4-24) · Self-improvement (R-7; M4-22) · Context (R-13; M4-24) · Security (R-2/3/14; M4-26).

**Holes, with reasons:**
- **Cost.** The spine has **no cost pair and cannot have one**: the SDLC corpus records zero cost incidents in 610 issues — absence of record, not of cost. **A recurrence lens needs incidents in both domains; one domain never looked. Not low demand — *unmeasurable by this method*.**
- **Adversarial security.** Zero incidents in either domain. **Recurrence generates from demonstrated repeated fact; there is no fact here.** Manufacturing a row would violate the no-invented-recurrences rule.
- **Mid-run steering.** Both domains show almost nothing failing *because there is no mid-run steering to exist* — a structural blind spot of any field-evidence lens.

**E-1 — engaged, now two-domain.** Population: P-19↔S-24 (62/63 [V]) · P-12↔S-12 · P-03↔S-10 · P-13↔S-02 (census-backed) · P-26↔105-open-issues. **Every member now has a same-shape counterpart in the second domain, several census-backed — the two-tier test's ≥2-capability condition is met from *both* domains, which was the open question.** One sharpening: the single obligation in 231 units that **did** carry was the one filed as an addressable artifact with an external carrier — **the exception evidences the mechanism.** **Endorsed for admission; not re-derived.**

**E-2 — now two-domain, recommendation unchanged but strengthened.** The census adds decisive members: **the record systematically under-reports its own failure rate** (≥53 overwritten FAILs — *the record store, not the instrument, is the liar*), stores disagreeing at 44%, a measurement silently dropping 9% of its input, and FP-3 reproducing inside this run's own surface work. Both readings stand: (a) reducible to evidence-discipline-applied-to-telemetry; (b) irreducible because Introspection covers *producing* the record, not the record being *correct*. **The census shifts the read toward (b) being at least a named capability cluster** (M4-08/15/21/26) even if not a concern.

**Not promoted:** "exercised-control evidence" reduces cleanly to Introspection-over-the-enforcement-plane; one capability, not a concern.

**Shared-surface caveat:** everything derives from the same W0 corpus every other lens read. **This lens's marginal contribution is the census joins (W0-f) and the pairing corrections.**

**Flags:** (1) the corrected pairing set leaves the 14-of-30 spine intact but **re-weights it**: the census-backed rows are the strongest evidence in the run; R-8/R-9/R-12 carry stated caveats. (2) **W0-f's named cheapest measurement — `git log --follow` over canonical gate-report paths — would settle M4-15's supply-vs-surface question and convert the ≥13.9% floor to an exact rate.** Probe-queue material.
