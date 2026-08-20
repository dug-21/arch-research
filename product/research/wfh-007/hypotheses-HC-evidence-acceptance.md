# hypotheses — H-C · evidence-qualified commitment & acceptance

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · **agent_id:** `wfh-007-hC-hypothesizer` · divergent phase, zero grades, zero writes
**Inputs read:** OWNER-DIRECTION.md · scout-merged.md (first) · scout-adjacent-annex-clinical-edc.md · scout-literature.md · scout-challenge.md (notary sections) · jurati-001 REPORT.md + reports/gate-feasibility.md
**Sense discipline honored throughout:** *attestation(digest)* = a signed predicate bound to an artifact digest (in-toto/DSSE); *attestation(opinion)* = an auditor's opinion on an assertion (SOX/PCAOB). They are never merged below; where a hypothesis borrows from PCAOB it borrows the *vocabulary and floor*, not the auditor.

Everything below is a `claimed` conjecture. Where a hypothesis brushes against jurati-001's semantic-judging premise, it is explicitly routed *around* it (lesson #265; gated on #266).

---

## Cluster I — What makes a claim durable

### H1 — The insufficiency floor is directly mechanizable at the garage's write chokepoint
**Statement:** PCAOB AS 1105's floor ("inquiry alone does not provide sufficient evidence") could become a write-time predicate: no grade above `claimed` when the only attached evidence is of kind *executor's own report*.
**Mechanism:** a floor over a kinded field is a typed comparison, not a judgment — evaluable by the deterministic checker family jurati-001 actually demonstrated (14/14, fail-closed), pointed at the `proven_by` field instead of a clause vector. The single-writer curator is an existing chokepoint; the check costs one field validation.
**Falsifier:** pull every historical `proven_by` and attempt mechanical kind-assignment. If assigning the kind itself requires semantic judgment for most artifacts, the floor is unenforceable at write time and collapses back into the judge problem.
**Novelty:** obvious. **Cluster:** D, C15. **Owner cost:** zero new gates — tightens an existing one. **Level-up:** linear, but the cheapest move in this file.

### H2 — A commit points at two things: the claim, and the prior claim it discharges
**Statement:** FDA 820.30(f)'s structure could require every grade move to name the specific `done_when` clause it discharges, not merely the node.
**Mechanism:** `context_correct` already implements append-only-by-supersession with id reissue; the same spine can carry clause-level discharge pointers, making "what exactly did this artifact prove" a graph query instead of a re-read of the run report. jurati-001's terminal validator produced exactly this table by hand — the hypothesis is that the table becomes the commit format.
**Falsifier:** inspect existing capability nodes — if `done_when` is a single prose blob rather than addressable clauses, discharge pointers have nothing to point at, and the prerequisite is a schema decision, not this mechanism.
**Novelty:** adjacent. **Cluster:** D, jurati-001. **Owner cost:** none at runtime.

### H3 — Durable = recomputable by a stranger; the jurati-001 gate report is the existence proof
**Statement:** The operational definition of "durable versus merely asserted" could be: *a claim is durable iff a party with no execution context can recompute the acceptance verdict from the record alone* — and the garage has already run this test once.
**Mechanism:** look at the gate-feasibility PASS/FAIL table. Every check that PASSED was a stranger's mechanical recomputation (hash recompute, count arithmetic, Wilson intervals, commit-authorship joins); every check that FAILED required context the record didn't carry. The line between durable and asserted *observably fell exactly at recomputability*, in our own artifact, without anyone designing it that way.
**Falsifier:** sample N historical grade moves and attempt stranger-recompute of each. If recomputable fraction ≈ 0, the definition is aspirational and describes only preregistered proof runs.
**Novelty:** non-obvious. **Cluster:** D, jurati-001. **Owner cost:** zero — it converts owner review from reading prose to spot-checking arithmetic. **Level-up:** step-function — it makes durability *checkable at issuance* (feeds H15).

---

## Cluster II — The declared-kind vocabulary, made enforcing

### H4 — Invert `def:Origin` from retrospective to enforcing: kind declaration as a precondition of the write
**Statement:** Define-XML's Type+Source+DocumentRef triple — shipped, FDA-mandated, machine-readable, and (its load-bearing flaw) authored months after the fact — could move to the *front* of the write: the store/correct call rejects evidence lacking a declared kind, the way FDA's Technical Rejection Criteria reject a submission at the door.
**Mechanism:** the annex's own observation does the work — TRC is the *only* mechanically-enforced gate in the entire clinical stack, and it enforces by refusing intake, not by reviewing content. The garage's MCP tool boundary is structurally identical to the eCTD inbound processor. D14 already made `cites:` fields required-at-write; this extends the posture from citations to evidence.
**Falsifier:** replay the rule against historical writes. If a large fraction of legitimate wide-mouth findings would have been rejected (exploratory material genuinely has no evidence kind yet), the precondition strangles divergence and the rule must be grade-scoped (bind at `partial`+, not at store) — a measurably different hypothesis.
**Novelty:** obvious-to-adjacent. **Cluster:** D, annex stop-points #1/#2. **Owner cost:** zero gates; possible agent friction, which is the falsifier.

### H5 — Grade as a derived value, not an asserted tag
**Statement:** Define-XML's failure #3 (declaration per *column*, silence per *record*) transferred: the enforceable unit is the individual evidence entry, and the node's grade could become a value *computed* from the kinds of attached evidence rather than a tag asserted alongside them.
**Mechanism:** this structurally deletes Cluster H's failure class for the firewall. A control that is "present, believed, inert" requires a control that can drift from the thing it governs; if `grade` is a function of `proven_by` kinds, there is no second object to go stale — the `zeroMergeStreak` failure becomes unrepresentable. It also makes the ~60/hr `context_tag` rate limit irrelevant for grades.
**Falsifier:** compute the derived grade for every current node from its evidence fields and diff against the asserted tag. Every mismatch is either (a) a latent firewall violation — valuable — or (b) a case where the function needs judgment to agree, which kills it. The diff is a one-day probe.
**Novelty:** adjacent. **Cluster:** D, H, C15. **Owner cost:** negative — removes a whole class of audit. **Level-up:** step-function for firewall integrity if the diff is clean.

### H6 — Kind the *corrections*, because that is where fabrication launders
**Statement:** The one place clinical discipline evaporates is `ReasonForChange` (free text, no codelist) — and E6(R3) §4.2.4's rule (*a correction is valid only if it cites source-record evidence*) could require a declared correction-kind and an evidence pointer on every supersession.
**Mechanism:** a fabricated success is rarely defended forever; it is quietly *corrected* later. The correction stream is low-volume, flows through exactly one tool, and is where a self-serving history rewrite must pass. Enforcement at the fraud's exit door rather than its entry door — cheaper, and the annex says it is the industry's clearest unfilled gap after 30 years.
**Falsifier:** mine the garage's correction chains retrospectively; if corrections resist kind-assignment even by hand, the vocabulary is fiction. Secondary: if fabrications in the wfh-005 corpora are abandoned rather than corrected, the exit door is the wrong door.
**Novelty:** non-obvious. **Cluster:** D, annex stop-point #4. **Owner cost:** zero gates.

---

## Cluster III — What a *ranked* lattice buys over an enumerated set

### H7 — Ranking + `Contradicts` edges = a deterministic staleness tripwire
**Statement:** An enumerated kind set can say "this claim has evidence of kind X"; only an *ordered* set with PCAOB's contradiction rule can say "this `proven` claim has acquired contradicting evidence of a *higher* kind" — and the garage already has the `Contradicts` edge, so the join is one rule away.
**Mechanism:** join `Contradicts(finding→finding)` to a kind ordering; when a contradicting finding's kind ≥ the kind in the target's `proven_by`, flag and route to owner. Deliberately *defeasible* per ISA 500 A35 — the rule escalates, never auto-downgrades, keeping it Graydon-Holloway-safe (ordinal comparison for routing, no computed confidence).
**Falsifier:** if real contradicting pairs are of *incomparable* kinds (a lattice with wide antichains), the rule either never fires or always escalates, and ranking buys nothing. Testable against existing Contradicts pairs today.
**Novelty:** adjacent. **Cluster:** D, S4-C1 singleton. **Owner cost:** one new escalation class — replacing silent staleness, which costs unbounded attention at discovery time.

### H8 — Rank routes attention; it never computes truth
**Statement:** The surviving use of an evidence ranking, given Graydon–Holloway, is as a *routing function* — the kind of evidence decides **who must look** (no one / deterministic checker / sampled reperformance / independent validator / owner), never how confident anyone is.
**Mechanism:** the counterexample class that kills quantified-confidence schemes attacks their truth semantics. A routing function has no truth semantics to attack — its failure mode is misrouting, which is priced in attention, observable, and correctable. This is the only form of ranking that addresses Cluster G directly: a router is a throughput allocator by construction.
**Falsifier:** construct the Graydon-Holloway-style counterexample against the routing use — a fabrication whose declared kind routes it to the "no one looks" tier. If the wfh-005 corpora show fabrications concentrated in high-kind claims, kind-routing fails exactly where it matters.
**Novelty:** non-obvious. **Cluster:** D, G, S3-C7. **Owner cost:** this hypothesis *is* the owner-cost model — it makes gates-cleared-per-kind an explicit dial. **Level-up:** step-function; converts the notary from a checker into an attention allocator.

---

## Cluster IV — The bitemporal × attestation(digest) gap

### H9 — A commit with two clocks: "true as of" vs "asserted as of"
**Statement:** Joining bitemporality (solved) to digest-bound attestation (solved) — which no one has done, and which Rekor v2 moved *away* from by removing integrated time — could make the validity interval part of the signed payload: *this evidence demonstrated this claim, about the world as of T_valid, asserted at T_txn*.
**Mechanism:** the garage's `demonstrated_envelope` on #263 is already a valid-time record in disguise (pinned Ollama version, model digest, prompt hash) with no transaction-time anchor and no signature over the pair. The join makes staleness a *query* rather than an audit project. Rekor v2's retreat is evidence the join is genuinely unassembled, not unwanted — they externalized time because their trust model is multi-party; a single-owner system doesn't pay that cost.
**Falsifier:** attempt to express "this proof is stale because its pinned model digest is retired" as a mechanical query over *current* graph fields. If already expressible, the gap is a schema tweak, not a capability.
**Novelty:** adjacent (the gap is scouted; the single-owner cost argument is new). **Cluster:** D. **Owner cost:** zero gates; staleness surfaces as briefing items instead of surprises.

### H10 — Evidence half-life indexed by kind: decay on dependency events, not on the clock
**Statement:** Combining H9 with the kind vocabulary: each evidence kind carries a decay policy — reperformance evidence over pinned inputs does not decay until a pin changes; observational evidence of an external service decays on events or TTL — giving the firewall *scheduled truth maintenance* at near-zero cost.
**Mechanism:** transfer of the velocity-scaling shape from S3-C9: TTL-based invalidation admits damage O(v·TTL) where v is how fast the proven-against world moves, while event-based invalidation bounds damage independent of velocity. The claim: the *revocation* mathematics of authority applies isomorphically to the *staleness* of evidence — same shape, one layer up.
**Falsifier:** for existing `proven` nodes, check whether dependency-change events are observable at all in this estate (model retirements, tool-schema changes, protocol bumps). If not, event-based decay is unenforceable and TTL is the only instrument — which the mathematics says is the wrong one; an honest dead end worth recording.
**Novelty:** non-obvious/whitespace. **Cluster:** D, C (velocity result). **Owner cost:** zero; decay produces flags, and H8's router prices them.

---

## Cluster V — Separating the doer from the recorder (S5's Class 1)

### H11 — The garage already runs doer/recorder separation; the notary is that role split made mechanical
**Statement:** builder ≠ validator ≠ curator ≠ leader — plus jurati-001's builder/custodian commit-authorship check, which PASSED — is a *shipped instance* of the separation S5 says doesn't exist anywhere; the notary primitive could be this role split expressed as an admissibility rule: a completion record is admissible only when recorder-identity ≠ executor-identity, joined mechanically from commit authorship and tool-caller identity.
**Mechanism:** two identity substrates already exist (git commit author; MCP single-writer discipline). The check is a join over fields already recorded, not a build. The jurati-001 validator performed exactly this join by hand.
**Falsifier:** **D6 — attribution does not persist** (`created_by: anonymous`). Today the executor's identity is attested by the executor, making the separation check syntactically satisfiable by a lying doer. The hypothesis is falsified-as-currently-deployable and lives or dies on the platform agent registry landing. Naming that checkable external dependency is the point.
**Novelty:** obvious (observation) / adjacent (admissibility-rule form). **Cluster:** D, S5 Class 1, C15. **Owner cost:** zero gates.

### H12 — Two pens: the doer writes the claim, only the checker writes the verdict field
**Statement:** ODM's `SignatureDef` (Meaning + LegalReason, signed by the signer, not the data enterer) and Spinnaker's role-containment inverted: split the record into an executor-authored segment (claim + declared evidence, append-only) and a checker-authored segment (verdict), under *different write credentials* — so a true and a fabricated completion stop being the same syscall, because the syscall that matters (the verdict write) is not the executor's to make.
**Mechanism:** in Unimatrix terms, `grade:` tags become a credential-scoped namespace writable only by a validator-role principal, while content stays with the curator. The fabricator can still fabricate the claim; it cannot fabricate the *acceptance*, which is what moves status. This narrows Class 1 from "the record" to "the claim half of the record."
**Falsifier:** the single-writer curator is load-bearing for auditability (D5/D8). If two pens break the one-auditable-pen invariant, the cost is a write-discipline redesign; cheapest test is a paper exercise — walk the current audit story with two pens and see whether any audit question becomes unanswerable.
**Novelty:** adjacent. **Cluster:** D, C15. **Owner cost:** zero at runtime; one architecture decision (owner-gated; this run cannot make it).

### H13 — Sampled reperformance as a lottery: deterrence pricing instead of verification pricing
**Statement:** The clinical numbers condemn *exhaustive human* verification — they say nothing about *sampled machine* reperformance. For claims whose declared kind is reperformable (test suite, hash recompute, deterministic replay), random reperformance by a non-doer converts self-graded completion into a lottery the fabricator cannot price, coupling detection-probability × penalty the way FDA's disqualification register (232 records) does — at machine cost instead of $1.6M per trial.
**Mechanism:** deterrence needs P(detect)·penalty > gain, not P(detect)=1. Reperformance of a deterministic check is priced in compute, the cheap side of the ledger. The penalty analog exists: an agent-definition *version* whose claims fail reperformance loses standing to assert that kind — versioned agent defs are already this repo's practice.
**Falsifier:** measure the reperformable fraction of real garage claims. If most are inquiry-kind (prose findings), sampling has nothing to sample and the lottery covers only the tier already safest. Also falsified if reperformance is not actually deterministic in this estate (model calls inside tests).
**Novelty:** non-obvious. **Cluster:** D, annex cost signal, S5 Class 1. **Owner cost:** zero — samples run and only failures escalate.

### H14 — Temporal separation: the completion record is a *diff against a preregistered target*
**Statement:** Separate doer from recorder in *time* rather than identity: the contract (with its scoreable schema) is committed before execution; completion is then a comparison against a record its author did not write, converting "report what you did" from generation into diffing.
**Mechanism:** this is jurati-001's terminal lesson stated as a mechanism — the run failed precisely because prediction and reference shared no preregistered field, and the validator's ruling says *proof schemas must share a preregistered scoreable representation end-to-end*. Preregistration is the only doer/recorder separation that works **without** a verified identity substrate — it dodges H11's D6 dependency entirely: the record's authority comes from its timestamp in an append-only history, not from who signed it.
**Falsifier:** the fraction of real work whose completion *shape* is knowable in advance — the same denominator as H16. Also falsified if the executor can influence the contract text before freeze (contract-authorship capture), checkable from issue/commit history.
**Novelty:** non-obvious. **Cluster:** D, jurati-001. **Owner cost:** zero new gates; moves effort to issuance time.

---

## Cluster VI — Acceptance: checkability as a precondition of issuance

### H15 — The leader's proposal, developed: the issuance validator is jurati-001's checker pointed at a new moment
**Statement:** Making mechanically-checkable `done_when` a precondition of issuing a contract converts the failed problem ("build a semantic judge" — SCOPE FAIL) into a solved one ("refuse to issue what you cannot check"), and the component that tests checkability at issuance already exists: execute the proposed `done_when` against known-green and known-red fixtures, exactly the 14/14 suite the frozen checker passed.
**Mechanism:** decidability moves from runtime to admission control. A `done_when` that cannot be executed against a fixture is rejected at issuance and routed to the owner *by construction* — no judge, no semantics, no #266 dependency. The validator's job is "does this clause run, and does it distinguish a planted green from a planted red," a property of the clause, not of the work.
**Falsifier:** the vacuity attack — clauses that execute and discriminate fixtures but are hollow (`exit 0` of a script the executor will write). If vacuous-but-checkable clauses are easy to author, issuance-checking is a compile check, not an acceptance bar. H17 is the counter-mechanism; if H17 falls, H15 falls with it.
**Novelty:** obvious (the assigned proposal) — the fixture-reuse route is the contribution. **Cluster:** acceptance, jurati-001. **Owner cost:** *reduces* gates — the owner sees only contracts that failed issuance, each with the reason.

### H16 — The attack: Goodhart at the issuance gate, and the remainder is Cluster G wearing a new name
**Statement:** A checkability precondition selects for work *restated* in checkable-but-hollow terms, and pushes genuinely important uncheckable work into the owner-routed queue — which then rebinds on reviewer throughput, having reorganized the queue rather than shrunk it.
**Mechanism:** HA's quality-scale retrofit is the measured precedent for declaration burden suppressing participation (19.7% after 21 months, gold=13); HA's autonomous-contribution ban names maintainer time as the scarce resource. An issuance bar is a declaration burden on the *requester*; the prediction is delegation volume drops or clause quality races to the vacuous floor, both observable.
**Falsifier / the measurement this partition owes triage:** classify one real week of garage + software-delivery work items: what fraction can state a non-vacuous checkable `done_when` today? If high (the delivery corpus is test-shaped; the garage corpus is `done_when`-shaped already), the attack mostly misses. If low, H15 is an attention *re-router* and must be priced as one. **The cheapest high-value probe in the file.**
**Novelty:** adjacent. **Cluster:** acceptance, G. **Owner cost:** gates shift from post-hoc review to issuance triage; net sign unknown until measured.

### H17 — Non-vacuity is mechanically checkable for a useful subclass: gate-input independence as set-disjointness
**Statement:** A `done_when` clause is non-vacuous when its checker's inputs lie outside the executor's write-set — the run's own settled property (*gate-input independence*), checkable at issuance as disjointness of two declared sets.
**Mechanism:** the wild has shipped the degenerate form: `loop.js` runs a skeptical read-only Verify agent as a read-set restriction. At issuance, require each clause to declare its input set; reject clauses whose inputs the contract's own grant can reach. Syntactic, deterministic, no semantics. This is the specific counter to H15's vacuity attack: `exit 0` of an executor-written script fails disjointness by inspection.
**Falsifier:** honesty of the declared input set. If real checker inputs are unenumerable (network, model output, shared state), declared disjointness diverges from actual — HRU's shadow: true reachability is undecidable in general, so this works only in a declared, decidable fragment. Probe: take ten real clauses and attempt honest input-set declaration; count the ones where the set is closed.
**Novelty:** non-obvious. **Cluster:** acceptance, F (loop.js), wfh-005 settled base. **Owner cost:** zero — a rejected clause returns to its author, not to the owner.

### H18 — Declare the acceptance class at issuance, the way Cluster B declares consequence per action
**Statement:** Transfer the run's strongest convergence to acceptance: every contract declares its acceptance class at issuance — *machine-decidable / machine-checkable-with-sampled-reperformance / independent-validator / owner-only* — making the acceptance route a typed field rather than a runtime discovery.
**Mechanism:** the trust posture that made Apple's consequence annotation work and MCP's fail is present here in the *right* configuration by accident: the declarer (requester) is not the executor, so the declaration is not self-graded; and a *mis*declaration in the dangerous direction fails loudly and cheaply at acceptance time rather than silently. §8's field list already reserves the slot; this says its value should be a class from a small closed set, so routing (H8) and issuance-validation (H15) can dispatch on it.
**Falsifier:** distribution collapse — if real contracts all land in the last two classes, the taxonomy adds a field without adding information. Same one-week corpus as H16 answers it.
**Novelty:** non-obvious. **Cluster:** acceptance, B, §8. **Owner cost:** explicit and *legible* — weekly gate load readable off the class distribution.

### H19 — The owner-routed remainder is not overflow; it is the trust-graduation corpus
**Statement:** What routes to the owner under H15 is exactly the record the owner demanded for trust graduation (§5.7's complete record): the uncheckable remainder *generates the evidence that later shrinks the remainder*.
**Mechanism:** every owner acceptance decision on an uncheckable contract is a labeled example of what the owner accepted and why. After ~20 same-class decisions (the owner's own threshold), a stable pattern is a candidate for a new checkable clause — proposed to the owner as a policy recommendation (constraint #3: agents may recommend, owner activates). The funnel eats its own escalations; autonomy expansion becomes an empirical artifact of the acceptance queue instead of a separate program. No LLM judges anything; pattern extraction produces a *proposal*, and the owner remains the only activator.
**Falsifier:** whether owner acceptance decisions are recordable as structured events at all. If each is sui generis prose, nothing accumulates. Cheap test: record ten real owner acceptances in a fixed schema and see if the schema survives contact.
**Novelty:** whitespace. **Cluster:** acceptance, §5. **Owner cost:** the gates the owner was going to clear anyway, now generating a compounding asset per gate. **Level-up:** step-function — the only mechanism in this file that makes the owner's attention *compound* rather than just spend.

### H20 — Cross-program acceptance: the acceptance schema rides inside the signed contract
**Statement:** The owner's round trip fails exactly the way jurati-001 failed — two sides with no common scoreable field — unless the acceptance schema rides inside the contract; DSSE's PAE property (payload type authenticated *with* the payload) is the mechanism that stops either side retrofitting the bar after seeing the work.
**Mechanism:** attestation strictly in the *digest* sense: the contract, including its acceptance block, is content-addressed at issuance; returning evidence binds to that digest. Neither program needs to trust the other's internals or share an ontology — only the acceptance block, which both signed before work began. This makes the notary record the *transport* of cross-program work, and answers §8 Q3 with: *the contract does, for its checkable clauses; the owner, for the rest* — H15's partition applied at the program boundary.
**Falsifier:** run one real round trip through the existing GitHub-Issue adapter carrying a typed acceptance block. The known hard spot is grade translation across instances with different ontologies (§10); if grades don't survive the crossing, the contract needs an ontology bridge it cannot carry, and the schema must shrink to what does survive.
**Novelty:** non-obvious/whitespace. **Cluster:** acceptance, D, §7/§8. **Owner cost:** removes the owner's current job as the human transport layer — the largest single attention refund in this partition.

---

## Cluster VII — Evidence about evidence

### H21 — The bidirectional gap audit: C15 vs the regulated fields
**Statement:** The garage's firewall and the regulated regimes each hold, shipped, the exact piece the other lacks — and the diff is mechanically derivable, making it the cheapest complete requirements source for a notary anywhere in the scan.
**Mechanism:** what C15 has that Define-XML lacks: *enforcement at write time through a single-writer chokepoint* (the curator is a living TRC) and *correction-by-supersession* stronger than the audit trail's "rare circumstances" exemption. What the regulated fields have that C15 lacks: a *kind vocabulary* (a screenshot and a deterministic replay currently clear the same `proven` bar), a *floor*, a *contradiction-resolution rule*, and an *accountable asserter with revocable standing*. Neither side needs invention; each gap names an adopt.
**Falsifier:** pull all `proven_by` fields; if attached artifact kinds are already de facto uniform and high, the missing vocabulary is currently costless and this is a deferred need, honestly parked.
**Novelty:** adjacent. **Cluster:** D, C15, annex. **Owner cost:** zero — an audit, not a gate.

### H22 — Known-red drills: the notary must record evidence that its own gates still fire
**Statement:** Cluster H predicts the notary's most probable end state; the counter-mechanism is *planted fabrications* — synthetic completion records injected by a non-doer, whose rejection is itself a recorded, kinded event, so "this gate last fired on a planted red at date D" becomes queryable meta-evidence.
**Mechanism:** jurati-001's checker suite already contains known-red and prompt-injection fixtures; this extends them from test-time to production sampling. Graydon-Holloway-compliant: the meta-evidence is ordinal freshness, never a computed confidence. A gate with no recent fired-on-red event is flagged inert — the fire drill the ruvnet stack never had.
**Falsifier:** if the gate can fingerprint drills (planted reds distinguishable from real work by any feature the gate reads), the drill measures the fingerprint, not the gate. Testable adversarially and cheaply.
**Novelty:** non-obvious/whitespace. **Cluster:** H, D, S3-C7. **Owner cost:** near zero; one flag class.

### H23 — The workflow-decay inversion: every declared kind needs an asserter with standing to lose
**Statement:** The scan's lone counter-signal — the only field with *no authority model* is the only one that *failed* — implies declarations rot without an accountable asserter; clinical declaration survived cheaply because a named person signs (the 1572) and can be disqualified. A personal system has one human, so the accountable asserter must be the *versioned agent definition* whose per-version claim record accumulates and whose standing is revocable.
**Mechanism:** this repo already versions agent defs as method artifacts; H13's reperformance lottery supplies detection; the standing ledger supplies memory. Together they reproduce the deterrence structure of the disqualification register with zero human verification cost — reputation for prompts, kinded and ordinal, never numeric.
**Falsifier:** two, both named: D6 (attribution doesn't persist — same dependency as H11; triage them together); and volume — a single owner's per-agent-version sample sizes may be too small for standing to mean anything, checkable from existing run telemetry.
**Novelty:** whitespace. **Cluster:** D, S5 Class 1, cost counter-signal. **Owner cost:** zero at runtime; revocations surface as recommendations.

### H24 — Don't build the ledger: the append-only leg is git plus a protection audit
**Statement:** AWS withdrew QLDB; Rekor exists; and jurati-001's validator already used commit SHAs as its entire custody spine. The notary's append-only leg could be git history plus an externally-anchored checkpoint the executor cannot force-push — with the deliverable being not software but a *demonstration*, because 21 CFR 11.10(a) frames append-only as "a validated property you must demonstrate," never one you inherit from a datastore.
**Mechanism:** the run's own evidence says the failure lives in configuration, not technology: ruvnet ran his loop with branch protection off and zero rulesets while believing "the machine never merges." The build is a config audit + one signed-checkpoint job; the proof artifact is the audit result, which is the shape the firewall can consume.
**Falsifier:** threat-model walk — can the executing agent reach the remote's protection settings through any credential it holds? If the boundary's exemption is held by the bounded party (the `dangerouslyDisableSandbox` pattern — **and this very session runs under bypass-permissions, a live in-house instance**), the checkpoint is theater and the hypothesis fails its own audit.
**Novelty:** adjacent. **Cluster:** D, H, cost signal. **Owner cost:** one-time audit; zero recurring gates.

---

## Compact index

| # | One line | Class | Target |
|---|---|---|---|
| H1 | Insufficiency floor as a write-time predicate at the curator chokepoint | obvious | evidence-qualified commit |
| H2 | Commits carry clause-level discharge pointers (820.30(f)) | adjacent | commit / done_when structure |
| H3 | Durable = stranger-recomputable; jurati-001's gate report is the existence proof | non-obvious | the durable/asserted line |
| H4 | `def:Origin` inverted: kind declaration as write precondition (TRC pattern) | obvious | commit intake |
| H5 | Grade as a value derived from evidence kinds, not an asserted tag | adjacent | firewall integrity |
| H6 | Kind the corrections — fabrication launders through `context_correct` | non-obvious | correction path |
| H7 | Ranking × `Contradicts` = deterministic, defeasible staleness tripwire | adjacent | graph maintenance |
| H8 | Rank routes attention, never computes truth | non-obvious | acceptance routing / owner attention |
| H9 | Two-clock commit: bitemporal validity inside the signed payload | adjacent | commit schema (the open combination) |
| H10 | Evidence half-life by kind; decay on dependency events, not clock | whitespace | proof staleness |
| H11 | Doer/recorder separation = the garage's role split as an admissibility rule | obvious/adjacent | Class 1 (blocked on D6) |
| H12 | Two pens: executor writes claims, only checker credentials write verdicts | adjacent | Class 1 / write discipline |
| H13 | Sampled reperformance as deterrence lottery; disqualification as penalty | non-obvious | Class 1 at machine cost |
| H14 | Temporal separation: completion is a diff against a preregistered target | non-obvious | Class 1 without identity substrate |
| H15 | Checkability as issuance precondition; the fixture suite already exists | obvious (assigned) | acceptance |
| H16 | The attack: Goodhart at issuance; remainder rebinds on reviewer throughput | adjacent | acceptance (the denominator probe) |
| H17 | Non-vacuity = gate-input independence as declared-set disjointness | non-obvious | acceptance validation |
| H18 | Acceptance class declared at issuance | non-obvious | contract schema |
| H19 | Owner-routed remainder = the trust-graduation corpus; escalations compound | whitespace | acceptance × owner trust |
| H20 | Acceptance schema rides inside the signed contract (PAE); notary as transport | whitespace | cross-program round trip |
| H21 | Bidirectional gap audit: C15 vs regulated regimes | adjacent | requirements source |
| H22 | Known-red drills: ordinal meta-evidence that gates still fire | whitespace | Cluster H antidote |
| H23 | Asserter-with-standing = the versioned agent definition | whitespace | declaration durability |
| H24 | Append-only = git + protection audit; the deliverable is the demonstration | adjacent | append-only leg |

**Dependency clusters for triage:** H11+H23 share the D6 blocker; H14+H15+H16+H17+H18 form one acceptance stack where H16's one-week corpus measurement prices the rest; **H5 and H12 conflict on the write-discipline question and cannot both be adopted as stated**; H1+H4+H21 are the same adopt seen at three altitudes.

---

## Flags

- **Input quality:** dense, not thin. One ceiling: H-C did not independently re-verify S4's PCAOB/ISA characterization or the Graydon-Holloway result beyond the scouts' declared source discipline; hypotheses resting on them (H1, H7, H8, H22) inherit those citations' standing, and S3 flags C7 as read at abstract level.
- **Live in-house instance of Cluster H:** this session runs under bypass-permissions with instructions to prefer raw Bash over mediated tools — the boundary's exemption held by the bounded party, in the garage's own harness, today. Relevant to H24's falsifier; flagged, not judged.
- **D6 is the single biggest external dependency in this partition** (H11, H23, half of H12's value). Worth stating to the owner as such rather than discovering it per-hypothesis at triage.

---

## The strongest case that the notary should NOT be built

**1. Every regime that ran this primitive at scale is retreating from it, on the same finding.** Six regulators independently concluded the verification half costs everything and finds little: 370 human checks per error; SDV correcting 1.1% of a dataset at 40× the cost of recording it; I-SPY spending $6.1M to change 0.36% of fields and zero conclusions; FDA suspending its own audit-trail enforcement and deleting review independence; AWS withdrawing the managed append-only ledger. The notary is a bet that computing's version will invert the best-measured cost curve in the scan.

**2. The single-owner case is the notary's degenerate case.** Notaries exist to arbitrate between mutually distrusting parties. Here there is one human, one asserter set, one estate. The party the notary defends the owner against is the owner's own agents — and the owner already reviews their output, because Cluster G says reviewer throughput, not record integrity, is the binding constraint. A notary adds a gate *in front of* the bottleneck without widening it; H16 attacks the acceptance half the same way.

**3. The base-rate outcome for a built notary is "present, believed, inert."** Six instances in four unrelated codebases this run alone, including a detector-of-a-dead-detector and a capability system deliberately deleted under latency pressure. The garage would be building precisely the artifact class with the run's worst survival record, and its own precedent (jurati-001) is a sophisticated verification mechanism that returned SCOPE FAIL against its own proof bar.

**4. The load-bearing separation is not currently real.** Doer/recorder separation without a verified identity substrate is syntax, and D6 says attribution does not persist. Until the platform registry lands, the notary's central admissibility check is satisfiable by the party it exists to constrain.

**5. The threat may be mitigated upstream before the notary amortizes.** Fabricated-success is a model-behavior failure the frontier labs are attacking at the model layer; a two-year single-owner horizon is long enough for the trend to turn while the notary is still being validated.

**The honest counterweight:** the same cost evidence shows the *declaration* half is cheap, machine-readable, and the only part that survived everywhere — and the one field that skipped the authority model entirely is the one that failed. The retreat argument condemns the expensive human-verification notary nobody in this file proposed; it does not touch a declaration-plus-deterministic-check-plus-sampled-reperformance shape (H1/H4/H13/H24), which is closer to what the six regimes retreated *to* than what they retreated *from*. Whether that shape still earns a build — or is an afternoon of configuration on C15 — is exactly the adopt/assemble/build cut, and it is the goal-owner's to make.
