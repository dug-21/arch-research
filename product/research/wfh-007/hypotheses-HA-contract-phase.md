# hypotheses — H-A · the contract≡phase collapse

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · partition: *is a workflow phase and a cross-program work contract one type?*
**Agent:** `wfh-007-hA-hypothesizer` (Fable 5) · divergent phase · **nothing here is graded; everything is `claimed` conjecture at most**
**Inputs read:** OWNER-DIRECTION.md (full) · scout-merged.md (full, first) · scout-literature.md (Q1/Q2/Q4 + candidates) · scout-challenge.md (verdict + evidence) · scout-adjacent.md (targeted extracts) · hypothesizer role def · graph dedup (`context_search`, read-only)

**Flags, up front:**

1. **The first corpus is unreadable from this disk.** OWNER-DIRECTION §7 names the Unimatrix repo's `.claude/protocols/uni` software-delivery protocols as the first workflow corpus. That repo is not on this disk. Every hypothesis below that quantifies over "what real phases carry" (H2, H5, H14, H24, H27 especially) is tested against *this repo's* six protocols and eight agent defs only, and must be re-run against the software-delivery corpus before triage treats its falsification test as passed or failed.
2. **Three load-bearing mechanism sources are single-author, no-venue** (AIP/IBCT — Prakash; PunkGo — Zhang; Bureaucracy of Speed — Parakhin). Their *measured shapes* are used as mechanisms, per the merge's own discipline; where a hypothesis dies if the measurement is wrong, it says so.
3. **Dedup notes:** #244 (shd declarative routing/escalation contract) and #256 (jurati-001 evidence-bound decision evaluation) are adjacent prior capabilities; H9 and H23 conjecture edges to #256. Nothing in the graph holds the collapse itself.

Four movements: **the collapse works** (H1–H8), **binding time as a dial** (H9–H13), **what else is secretly this object** (H14–H19), **attacks and repairs** (H20–H30). Then the consolidated **where-it-breaks** ledger.

---

## Movement I — the collapse works

### H1 — A phase is a contract whose issuer is the workflow author and whose issuance time is compile time
- **Statement:** One record type could serve both phase and cross-program contract, because every field OWNER-DIRECTION §8 requires of a contract has a phase analogue, and the residue is two parameters: *who signed the grant* and *whether issuer and executor share a verification root*.
- **Mechanism:** Field-by-field mapping. Requesting identity → workflow author (owner, via git `main`). Objective/bounded deliverable → the phase's charge. Authority delegated → phase-indexed authority (TBAC's exact object). Evidence/acceptance → `done_when` + the D7 firewall check (Cluster D, S4 C15 — already running). Expiry → the phase's transition-out. Disposition → accepted/rejected/superseded maps onto gate-pass/gate-fail/protocol-revision. The two residues are representable as *data* (a signer field; a verification-profile field), not as type splits.
- **Class:** obvious. **Level-up:** step-function if true — one schema instead of two subsystems.
- **Cheapest test:** Write the six protocols in this repo *and* one §8 contract in a single candidate field set; count fields null-or-nonsensical on one side. >2 structurally dead fields per side = forced union, not unification.
- **Risk:** that "who issues" and "shared trust domain" really are parameters. Movement IV attacks this. Draws on: **Cluster C, Cluster D, TBAC settled base.**

### H2 — Phases are siblings under a root grant, not links in a chain
- **Statement:** The naive collapse — each phase attenuates from the previous — is false on its face (an implement phase holds write authority a design phase never had; monotone chains cannot widen). It could survive by re-rooting: the *workflow instance* is the root contract carrying the union ceiling, and each phase attenuates *from the root*.
- **Mechanism:** Macaroons/IBCT attenuate from the mint. Nothing requires the delegation graph to be a path; a root block (workflow instance, owner-signed) with per-phase sibling blocks preserves monotonicity (`Mutation::admissible`-style, or 0.049 ms per verify) while letting phase N+1 hold authority phase N lacked.
- **Class:** adjacent. **Level-up:** linear — but it is the choice that keeps Cluster C's solved machinery applicable.
- **Cheapest test:** Take `theme-scan`; write the instance ceiling and per-phase siblings; check no phase needs authority outside the instance union. **Falsified if** any real phase's authority legitimately depends on an *earlier phase's outcome* — see H8 for the repair.
- **Risk:** a ceiling wide enough for all phases is a fat target if per-phase narrowing is inert — Cluster H's exact failure. Draws on: **Cluster C, Cluster H.**

### H3 — Sequence is not primitive: ordering decomposes into data dependency plus resource lease
- **Statement:** The strongest "phases have no contract analogue" objection — *ordering* — could dissolve, because what a workflow gets from ordering is (a) phase N+1 consumes phase N's outputs and (b) non-interference, both expressible on contracts.
- **Mechanism:** in-toto layouts already ship (a): a layout defines steps, each naming authorized functionaries and a threshold, and **step N+1's expected materials must match step N's products** — supply-chain workflow sequence as evidence-linked contract records, deployed for years. (b) is a caveat over a named resource.
- **Class:** non-obvious — in-toto layout as a *phase engine for agent workflows* appears in no scout.
- **Level-up:** step-function — "Jurati's workflow layer" becomes an adoption of a shipped verification model rather than a build.
- **Cheapest test:** Express `theme-scan` as an in-toto layout. What can't be said is the finding: expected gaps are loops, dynamic fan-out (H10), human gates (H12).
- **Risk:** in-toto's static layout surviving dynamic agent workflows; H10 carries the repair. Draws on: **Cluster D, Cluster C.**

### H4 — Separation-of-duty rides along: "validator ≠ builder" is a caveat over identity history, and its price is WSP
- **Statement:** The garage's deepest structural rule is expressible as an identity-history caveat on the acceptance clause — importing the Workflow Satisfiability Problem's complexity as the cost of planning multi-phase assignments.
- **Mechanism:** WSP with SoD is NP-hard and W[1]-hard, FPT for user-independent constraints (settled, quiescent since ~2015). "Executor ∉ signers of chain segment X" is user-independent in most garage cases → the FPT fragment, cheap at personal scale.
- **Class:** adjacent. **Level-up:** linear.
- **Cheapest test:** Encode the garage's three real independence rules as chain predicates; check against wfh-007's actual agent assignment record.
- **Risk:** agent identities stable enough within a run for the predicate to mean something (tension with H21). Draws on: **WSP settled base, Cluster C.**

### H5 — The two "uncovered remainders" are one object: a phase transition IS an evidence-checked commit
- **Statement:** scout-merged §13 names exactly two unshipped gaps — *authority indexed to a phase of a declared task* and *a commit whose evidence kind is checked at write time*. If contract≡phase, these are the same mechanism from two sides: a transition out of phase N is a **commit whose acceptance clause is checked at the transition**, and the authority of phase N+1 is **minted by that same checked transition**. One checker, one seam, not two components.
- **Mechanism:** in-toto's materials/products matching is "the write into the next step is checked against declared evidence"; IBCT's chained blocks are "the next hop's authority derives from the verified chain." Composed: the transition record is simultaneously the acceptance artifact of contract N and the issuance root of contract N+1. Every part is shipped; the *composition* is the residual novelty — the shape wfh-005 settled ("composition, not absence").
- **Class:** **non-obvious** — no scout and not the merge states the identity of the two gaps; it emerges only under the collapse.
- **Level-up:** step-function — it halves the build surface the theme thinks it has.
- **Cheapest test:** Specify the transition record for one real gate (wfh-007's own scout→merge gate); check one record can carry both acceptance of the scout contracts and issuance of the hypothesize contract without field conflict. **Falsified if** acceptance-time and issuance-time information requirements conflict — see H25's disclosure attack.
- **Risk:** the same party may safely both accept N and issue N+1 (in the garage that party is the leader; whether that concentration is acceptable is a triage question). Draws on: **Clusters C + D, the merge's §13.**

### H6 — Acceptance across trust domains without shared ontology, via an evidence-kind floor
- **Statement:** The collapse's hardest semantic objection — acceptance means "did the work satisfy *our* test" intra-program, but programs don't share tests — dissolves if acceptance clauses are written in evidence-*kind* language (ordered, with a floor) rather than domain language.
- **Mechanism:** PCAOB AS 1105/ISA 500 is the only *ordered* evidence vocabulary the scan found: seven procedure kinds, comparative operators, a hard floor ("inquiry alone does not provide sufficient evidence"), a contradiction rule. A cross-program contract can say "acceptance requires ≥ recalculation-kind; assertion-kind insufficient" with zero knowledge of the executing program's domain. Graydon–Holloway independently pushes the same direction: kinded/ordinal, never numeric.
- **Class:** non-obvious. **Level-up:** step-function for cross-program work.
- **Cheapest test:** Write the acceptance clause for §7's round trip using only an evidence-kind lattice; have someone who didn't write it judge a returned deliverable. **Falsified if** judgment can't be made without domain vocabulary leaking back in.
- **Risk:** translating audit kinds to agent-work kinds without becoming a taxonomy-authoring project, which §13.10 forbids through the curator. Draws on: **Cluster D, singletons 2 & 3.**

### H7 — Consequence class is the field neither parent lineage carries, and it attenuates like scope
- **Statement:** Workflow lineage types authority by task state; IAM lineage by principal/action/resource; neither carries consequence. The unified type could carry a consequence ceiling (Idempotent/Reversible/Compensable/Irreversible) behaving like any attenuable caveat.
- **Mechanism:** Revisable-by-Design's four classes form a total order, so "may only narrow" is well-defined; monotone attenuation machinery applies unchanged. The owner's §6 refusal of one generic `dangerous` flag is satisfied structurally: consequence attenuates independently of resource scope and information sensitivity — three monotone dials on one record.
- **Class:** adjacent. **Level-up:** linear-to-step.
- **Cheapest test:** Classify the 15 `context_*` tools by the four classes; check stability under two independent classifiers. **Falsified if** a legitimate delegation needs a *higher* consequence class than its issuer holds (candidate: a low-consequence monitor that must escalate to an irreversible page).
- **Risk:** the declaration is verified, not asserted — Cluster B's open seam. H18 carries the verification half. Draws on: **Clusters B + C.**

### H8 — Earned authority: where a later phase's grant depends on an earlier outcome, the transition-commit mints it
- **Statement:** If H2's falsifier fires, the collapse survives via H5's fused object: the accepted transition *is* the minting event, so conditional authority is issuance-gated-on-disposition.
- **Mechanism:** in-toto layout verification refuses final delivery if any step's link metadata fails threshold/functionary checks — shipped systems already make downstream *possibility* conditional on upstream *verified records*. IBCT's root-block signing is the minting act; sign it inside the checker that just verified the predecessor.
- **Class:** adjacent. **Level-up:** linear.
- **Risk / flag:** the checker holding the minting key becomes the trusted core — a real answer to §14 Q5 ("smallest responsibility a trusted core must hold": *verify predecessor evidence; sign successor roots*; possibly nothing else). **This may be the smallest-core candidate the run was asked to surface.** Draws on: **Clusters C + D.**

---

## Movement II — binding time as a first-class dial

### H9 — Binding time is a per-field property, not a per-contract property
- **Statement:** The three binding times don't partition *contracts*; they partition *fields within one contract*. A phase authored at compile time still late-binds executor identity, instance parameters, actual resource consumption; a run-time-inferred contract still early-binds its ceiling. The dial is a column on the schema, not a type tag.
- **Mechanism:** IBCT demonstrates it natively: the root block early-binds identity, scope ceiling, budget ceiling, max depth, expiry; each hop late-binds the narrowing; the invocation record late-binds actuals. Three binding moments in one shipped object.
- **Class:** non-obvious. **Level-up:** step-function for design clarity — it dissolves the compile-vs-run-time argument into per-field decisions with known answers.
- **Cheapest test:** Take §8's twelve fields; assign each an *earliest possible* and *latest safe* binding time. **Falsified if** some field has no coherent answer. Candidate problem child: "information intentionally disclosed" (H25).
- **Risk:** none beyond the exercise; nearly free to test. Conjectured edge: Supports → #256. Draws on: **Cluster C.**

### H10 — Compile time binds the envelope; run time binds the instances
- **Statement:** Static layouts and dynamic agent workflows reconcile because what must be early-bound is only the *shape envelope* — max delegation depth, budget ceiling, functionary class, threshold — while count and identity of sub-contracts late-bind.
- **Mechanism:** IBCT's max-depth and budget-ceiling are envelope fields enforced cryptographically at each hop; in-toto's threshold is an envelope over how many functionaries must independently attest. Neither needs the instance count at authoring.
- **Class:** adjacent. **Level-up:** linear but load-bearing for H3.
- **Cheapest test:** Express wfh-007's own run inside an envelope authored *before* knowing the counts. **Falsified if** a real run decision changed the envelope mid-run — it did (the S4 amendment and annex were mid-run additions), so H10 depends on H27.
- **Risk:** envelopes wide enough for real runs may be too wide to mean anything. The test must measure envelope-slack, not just admissibility. Draws on: **Clusters C + D.**

### H11 — Attenuation-only run-time intent: the lying agent can only hurt itself — *for actions*
- **Statement:** The leader's proposal holds for the action plane: a run-time intent declaration is safe to consume from an untrusted agent iff it can only *narrow* what the chain already grants. The declaration is simultaneously a free precision gain (measured least-privilege instead of guessed) and a free audit artifact.
- **Mechanism:** monotonicity checked structurally; widening rejected cryptographically at 0.049 ms. The declaration's untrustworthiness becomes irrelevant to safety and valuable to audit — the FORTIS failure mode is structurally capped because *no declaration can escalate*.
- **Class:** adjacent. **Level-up:** step-function for the run-time third of the dial.
- **Cheapest test:** Wrap one garage subagent's tool access in a declare-then-narrow gate; measure (a) zero widenings admitted, (b) ceiling-to-declaration gap, (c) friction.
- **⚠ Risk:** **the claim is false for information flow and false under sequential composition** — H25 and H20 are the strongest attacks in this file. **Do not carry H11 to triage without them attached.** Draws on: **Cluster C, FORTIS.**

### H12 — The owner gate is a third-party caveat; attention cost becomes statically countable at issuance
- **Statement:** Owner approvals are expressible as macaroon-style *third-party caveats*: the contract cannot verify without a discharge signed by the owner's key. Because caveats are fields on the record, the number of owner-discharges a contract can demand is countable *before execution* — turning Cluster G's constraint into a budgetable quantity per contract.
- **Mechanism:** macaroons' first/third-party caveat distinction is a shipped 12-year-old mechanism; the static count is arithmetic over the caveat list. Attention-per-unit-work becomes an issuance-time number the owner can veto ("this workflow wants 9 gates from me; redesign it").
- **Class:** **non-obvious** — no scout connected the caveat mechanism to attention budgeting.
- **Level-up:** step-function — the only hypothesis in this file that makes Cluster G's constraint *legible in advance* rather than measured after.
- **Cheapest test:** Annotate this repo's six protocols with implicit owner-gate points as caveats; check the static count against actual owner-interrupt history (wfh-005/006/007 threads). **Falsified if** real interrupts are dominated by *unplanned* escalations no caveat would predict.
- **Risk:** discharge fatigue — caveats that fire often converge on approval fatigue; a visible count doesn't make it small. Draws on: **Clusters C + G.**

### H13 — What compile time uniquely buys is amortized review: the phase is the attention-optimal binding point
- **Statement:** The three binding times price differently in owner attention: a compile-time phase is reviewed once and runs N times (cost → 0 per run); a request-time contract costs one review per exchange; a run-time declaration costs zero review *only because* H11 caps its harm. The dial's real name is **attention amortization**; "cache intent" = "amortize review."
- **Mechanism:** arithmetic over Cluster G — HA's linear-in-review-capacity growth and ruvnet's 5% both show review as the denominator. Predicts *where* each binding time belongs: recurring work → compile-time phases; novel cross-program asks → request-time contracts; intra-phase tool precision → run-time declarations.
- **Class:** adjacent. **Level-up:** linear but it's the *reason* the dial exists.
- **Cheapest test:** Compute gates-per-run over work that had a protocol (theme-scan runs 5/6/7) vs work that didn't (jurati-001's improvised scope).
- **Risk:** amortization assumes the phase stays correct across N runs; a stale cached intent reviewed once and wrong forever is the inversion — the protocol itself becomes the miscalibrated `zeroMergeStreak`. Phase *re-validation* cadence is the unpriced cost. Draws on: **Clusters G + H.**

---

## Movement III — what else is secretly this object

### H14 — A GitHub Issue is the degenerate contract, and its missing-field list is the adapter spec
- **Statement:** The one real cross-team exchange carried issuer identity, objective, return channel, disposition. It lacked exactly: delegated authority (ambient), evidence floor (prose), expiry (none), disclosure rules (none), provenance (none). The delta list *is* the GH adapter spec — satisfying "transport, not semantic protocol" by construction.
- **Mechanism:** absent fields are precisely those Clusters B/C/D supply shipped mechanisms for; present fields are those GH already enforces.
- **Class:** obvious. **Level-up:** linear.
- **Cheapest test:** Run one exchange with a typed Issue body; record which fields either side consulted. Unconsulted = schema fat; consulted-but-absent = schema holes.
- **Risk:** the typed body degrades into prose under real use — fine *if* the checker, not the reader, consumes the fields. Draws on: **Cluster D, §8.**

### H15 — `done_when` + `proven_by` + grade is half a contract already
- **Statement:** A Unimatrix capability node carries acceptance, evidence, and disposition. The collapse is partly a *recognition* event: adding issuer identity, authority envelope, and expiry to what D7 already enforces upgrades the existing firewall object into the unified type, rather than standing a new system beside it.
- **Mechanism:** S4's C15 identifies D7 as a production instance of Cluster D. The missing fields are the Cluster C (authority) and disposition-lifecycle halves. `context_cycle` already carries phase state.
- **Class:** adjacent. **Level-up:** step-function for sequencing — the collapse can be *dogfooded before Jurati exists*.
- **Cheapest test:** Field-diff `context_cycle` + capability-node schema against §8's twelve fields.
- **⚠ Risk:** Unimatrix becoming the contract plane **contradicts §10's candidate boundary** ("Jurati owns workflow state and exchange metadata; Unimatrix retains knowledge payloads"). This hypothesis deliberately pressures that boundary — treat the two as competing conjectures, not complements. Draws on: **Cluster D, the live capability surface.**

### H16 — This hypothesis assignment is itself an instance, and it exhibits a thirteenth field: the partition
- **Statement:** The task block that launched this agent carries issuer, objective, authority, evidence requirement, expiry, disposition — a complete request-time contract. It also carries one thing §8's list lacks: a **partition claim** — a statement of what *other contracts concurrently exist* and where the boundary lies.
- **Mechanism:** fan-out coordination needs non-overlap; §8 has no field for "the issuer promises sibling deliverable spaces are disjoint from yours." in-toto's layout holds this implicitly (steps enumerated together); free-floating contracts lose it. Without it, N hypothesizers regenerate each other's work — the alias-inflation failure the merge exists to catch, reproduced at the generation layer.
- **Class:** **non-obvious/whitespace** (self-referential evidence — the run's own machinery as corpus).
- **Cheapest test:** Compare H-A/H-B/… outputs at merge; overlap fraction measures how much work the partition field did.
- **Risk:** partition may belong to the *layout* rather than the contract — evidence that layouts are not fully dissolvable into contracts. Draws on: **Cluster F, merge methodology.**

### H17 — A skill invocation is a compile-time contract with the authority field deleted — and FORTIS measured the consequence
- **Statement:** A `SKILL.md` is owner-authored cached intent with **no authority envelope** — and FORTIS found the skill layer is the primary privilege-escalation surface, worst under convenience framing and boundary proximity. Skills-as-contracts closes a measured gap on a corpus this repo owns (20 skills).
- **Mechanism:** FORTIS's own conclusion: enforcement must live outside the model *at the skill or tool invocation layer* — where a contract's verify step sits. Umbrel's 395-line SKILL.md shows the packaging convention exists in the wild; the authority field is the one addition.
- **Class:** adjacent. **Level-up:** linear per skill, step for the pattern.
- **Cheapest test:** Add declared ceilings to 3 skills; drive FORTIS-shaped conditions at them; measure whether the hook-enforced ceiling blocks what the model's judgment didn't.
- **Risk:** hook enforcement is inside the harness's trust domain — `dangerouslyDisableSandbox` shows the harness hands exemptions to the bounded party; a skill ceiling the same runtime can lift is Cluster H instance #7. The test must include the lift-attempt. Draws on: **FORTIS, Clusters F + H.**

### H18 — An MCP tool call is the run-time micro-contract, and the Apple/MCP contrast names its missing half
- **Statement:** The smallest instance is a single tool call. Cluster B's sharpest contrast — Apple enforces self-declared consequence at OS level; MCP declares and enforces nothing — locates the buildable seam: **treat the tool's declaration as a ceiling claim and verify it**, at the one chokepoint the owner controls.
- **Mechanism:** for the 15 `context_*` tools, declared consequence is *checkable by construction*: idempotent → replay-test; compensable → must name its compensator (`deprecate` for `store`); read-only → diff-verify. Verification of consequence declarations — the seam neither Apple nor MCP fills — is cheap precisely where the server is yours.
- **Class:** adjacent. **Level-up:** linear. **Candidate for §7's unselected "first Unimatrix enhancement."**
- **Cheapest test:** Annotate the 15 tools; build the replay/diff checker for two; plant one false declaration and confirm the checker catches it.
- **Risk:** consequence of a *tool* underdetermines consequence of a *call* (`context_tag` is idempotent; tagging `grade:proven` is not low-consequence). Consequence may bind to (tool × argument-class). Draws on: **Cluster B.**

### H19 — Second-brain elevation (§10) is a cross-instance contract, not a new mechanism
- **Statement:** §10's pipeline is field-for-field a work contract issued by a project instance to the owner's instance: nomination = request; provenance/evidence check = acceptance clause; sensitivity = disclosure field; authorized elevation = owner discharge (H12's third-party caveat); origin retention = provenance field; source-correction propagation = `superseded` disposition flowing along the recorded chain.
- **Mechanism:** correction propagation is the interesting mapping — Unimatrix's `Supersedes` chains give elevated knowledge a mechanical stale-detection path (elevated entry pins the source id; `context_graph(mode:"current")` detects supersession — the D5 machinery, cross-instance).
- **Class:** **non-obvious/whitespace** — connects the run's two headline open problems as one.
- **Cheapest test:** Express §10's pipeline in §8's fields; the inexpressibles (contradiction review? cross-ontology grade translation?) measure how much of §10 is *not* the contract problem.
- **Risk:** cross-instance id resolution doesn't exist yet. Draws on: **Cluster D, D5, §10.**

---

## Movement IV — attacks on the collapse, with repairs

### H20 — The aggregation attack arrives through the declaration channel
- **Statement:** H11's safety argument is *per-contract*, and the forty-year-old aggregation problem defeats it *across* contracts: an agent that cannot widen any single grant can still achieve a forbidden composite by requesting a *sequence* of individually-narrow contracts. Attenuation-only makes each hop safe and the trajectory unsafe — and because each request looked disciplined, the audit trail actively launders the trajectory.
- **Mechanism:** the attack needs only legitimate machinery: narrow-read on store A, complete; narrow-write on store B, complete — composite: cross-domain flow nobody granted. Per-contract verification is structurally blind (Bertino: "sequences of individually permissible actions may collectively violate system-level constraints"). The collapse *concentrates* exposure: one type means one verifier means one blind spot.
- **Class:** adjacent (problem is prior art; aiming it at the declaration channel is the contribution).
- **Cheapest test:** Construct the two-contract exfiltration on the garage's own surface; confirm per-contract checks pass while the composite violates a stated invariant.
- **Partial repairs, not verdicts:** (a) per-principal issuance history as a checker input — the chain already exists, so *trajectory-aware caveats* are expressible even if general aggregation is unsolvable; (b) H26's issuance-rate bounds. Neither solves it. Draws on: **Cluster C's open leg, S3 failure mode #1.**

### H21 — Trust graduation and ephemeral executors are in tension; the contract chain arbitrates
- **Statement:** Constraint 7 requires a stable subject accumulating history; per-objective team assembly destroys stable subjects. The collapse resolves it: trust accrues to the **issuing principal** (the program — stable), executors stay ephemeral, and PROV's `actedOnBehalfOf` is the recorded edge making an ephemeral executor's run count toward its program's record.
- **Mechanism:** the chain records both identities per contract; "20 runs in class K" becomes a query over dispositions grouped by root-identity × (action-class, consequence-class) — mechanically derivable, never asserted.
- **Class:** adjacent. **Level-up:** linear.
- **Cheapest test:** Retro-compute "eligible runs per class" for the garage from existing records; if classes can't be reconstructed, today's records are underspecified for the owner's own constraint 7 — a finding regardless.
- **Risk:** program-level trust laundering — a program earns trust on easy executors then deploys it with a worse one; the record must carry model/runtime provenance per hop. Draws on: **Cluster C (PROV), §5.**

### H22 — Revocation vs transition: the intra-domain case must adopt the inter-domain discipline
- **Statement:** Phases end by transition (revocation is free); contracts end by expiry/revocation (costly: O(v·TTL) at agent velocity). The collapse survives only in one direction: phases adopt explicit bounds (execution-count ceilings, D ≤ n), because the reverse — contracts adopting "the issuer will just stop you" — is false the moment a trust domain is crossed.
- **Mechanism:** execution-count bounds fit phases natively: "≤ n tool invocations before re-verification" — the re-auth lands at the chokepoint that already exists, at one extra verify per n calls.
- **Class:** adjacent. **Level-up:** linear.
- **Cheapest test:** Instrument one phase with a count ceiling; measure re-auth overhead and the empirical n distribution.
- **Risk:** Bureaucracy of Speed is single-author simulation-only; the *shape* survives independent of the simulation. Draws on: **Cluster C's unsettled leg #1.**

### H23 — TBAC's hidden assumption is the real fault line: no shared state observer across trust domains
- **Statement:** Phase authority is justified by *where the workflow is*; TBAC unified that with authorization by assuming a central system that *knows* task state. Across ownership boundaries no such observer exists — the requesting program cannot see the garage's internal phase, so "phase-indexed" has no referent for it. The collapse therefore requires **state attestation**: the executor proves its phase-state via evidence-carrying transition records rather than the issuer observing it.
- **Mechanism:** each transition record (signed, append-only, evidence-checked) *is* the attestation; the cross-domain issuer verifies the chain instead of watching state. This converts TBAC's architectural assumption into a verifiable-record discipline — the move Certificate Transparency made against trusted CAs.
- **Class:** **non-obvious** — names the precise architectural assumption separating the parents, and the shipped pattern that removes it.
- **Cheapest test:** For §7's round trip: can the delivery program's checker decide "the garage is in its deliver-phase and its prior gates passed" from chain records alone, zero live queries into garage internals?
- **Risk:** attested state is as fresh as its last record — a stalled-but-attested phase looks identical to a live one (ruvnet's 2.5-months-stale, attested). Liveness needs its own signal. Draws on: **TBAC settled base, Cluster D.**

### H24 — Inversion: abolishing compile time fails on trust accounting, and that failure is the phase's true job description
- **Statement:** If H11 makes run-time declaration safe and H6 makes acceptance domain-neutral, why author phases at all? Two things bind to the phase *definition* and cannot late-bind: (a) the owner's amortized review — you cannot review-once what is generated per-run; (b) constraint 7's equivalence class — "same action and consequence class" needs a stable, pre-authored class for 20 runs to accumulate *in*; classes inferred per-run from contract contents make the denominator itself agent-influenced, so an agent that subtly varies its declared class never accumulates a reviewable record, by construction. **Phases survive as the units of review amortization and trust accounting**, not as authority containers.
- **Mechanism:** graduation requires a denominator outside the graduating party's control; compile-time definitions signed by the owner are the only artifact with that property (git `main`, owner-merged).
- **Class:** **non-obvious.** **Level-up:** step for design clarity.
- **Cheapest test:** Attempt to define constraint-7 classes from run-time contract contents alone over past runs; check whether an adversarial or merely sloppy declarer could fragment its own class history.
- **Risk:** needs the software-delivery corpus to test at scale (flag 1). Draws on: **§5, Cluster G.**

### H25 — Information disclosure does not attenuate: the contract needs a one-way-door field
- **Statement:** The attenuation invariant governs *authority*, not *information*: context once disclosed cannot be narrowed retroactively, and a fork-style executor inheriting the issuer's full context can exfiltrate through its legitimately-narrow output channel — narrow authority, broad knowledge, one permitted write. The unified type needs disclosure as a first-class **non-attenuable, staged** field.
- **Mechanism:** the attack needs no malice-specific machinery — a sub-agent handed a full conversation and a permitted deliverable file *is* the leak path. Staged disclosure = the contract's materials list (in-toto: materials are *enumerated*, not inherited).
- **Class:** adjacent-to-non-obvious. **Level-up:** step for the safety case's honesty.
- **Cheapest test:** Construct the leak on garage machinery (full-context fork + narrow write + planted sensitive token); re-run with enumerated-materials handoff and confirm the checker can *diff* deliverable content against the disclosure list.
- **Note:** this run's own leader-to-hypothesizer handoff was a *curated brief*, not a fork — that choice is the mechanism, and it should be a recorded field, not a habit.
- **Risk:** enumerated disclosure fights agent effectiveness; the disclosure-precision vs task-quality curve is unmeasured here. Draws on: **confused-deputy settled base, Cluster C's open leg, §8.**

### H26 — Contract issuance is itself an action: rate- and budget-bound the *request* channel
- **Statement:** If sequences of narrow contracts are the attack, the issuance channel needs the same discipline as any action: a principal's right to *request* contracts is itself contracted — bounded in rate, count, and cumulative touched-class set.
- **Mechanism:** execution-count bounds applied one level up — n contracts per window per principal, with the append-only chain as the counter; cumulative-class caveats checkable against the same record. Does not solve aggregation; converts the *cheap* serial attack into one that must spend a visible, bounded, recorded resource.
- **Class:** **whitespace** — no scout or prior-art item applies velocity-bounding at the issuance layer.
- **Cheapest test:** Simulation at the contract layer: attacker strategies against per-contract checks alone vs + issuance bounds.
- **Risk:** legitimate bursty work (a merge phase issuing 8 sub-contracts — this run did) must fit under the bound. Draws on: **Cluster C, S3 C9.**

### H27 — Deviation is a typed amendment, not an exception: the MEL pattern, held by a non-operator
- **Statement:** Real runs deviate (this one did: OWNER-DIRECTION mid-run, an S4 amendment, an annex). Today deviation is invisible-or-prose; Cluster H says the default is exemptions held by the bounded party. Aviation's MEL is the counter-pattern: **pre-enumerated, typed, time-boxed permitted-non-compliance, granted by an authority distinct from the operator, recorded as a first-class field.**
- **Mechanism:** an amendment block appended to the chain, typed against a pre-enumerated deviation taxonomy, expiring by its own bound — so a deviated run remains *verifiable*, and deviation history becomes trust-graduation input (constraint 7's "near misses" and "reversals" get a record type).
- **Class:** non-obvious. **Level-up:** linear-to-step.
- **Cheapest test:** Retro-enumerate every deviation in wfh-005/006/007; check whether a small typology covers ≥80%.
- **Risk:** who signs amendments is the whole question — if the leader both operates and amends, this is Cluster H with extra steps. Draws on: **Cluster B (MEL/LCO), Cluster H.**

### H28 — Cluster H is a standing attack on the entire file: a type is not a boundary
- **Statement:** Six independent built-believed-inert instances (plus Nextcloud deleting capability scoping for latency) predict the unified type's most likely failure: beautifully schematized contracts that nothing verifies on the write path. The design consequence is *placement*: the garage has exactly two structural chokepoints — the single-writer curator (graph plane) and owner-merged git `main` (artifact plane) — and contract verification is worth anything only inside one of them, unbypassable by the parties it bounds.
- **Mechanism:** Spinnaker's containment rule works because it evaluates at pipeline runtime on the execution path; HA's permission engine is complete and unreachable because no path leads through it. The garage's bypass inventory is knowable: subagent Bash writes, direct git pushes, non-`context_*` MCP calls.
- **Class:** adjacent. **Level-up:** the difference between the collapse mattering and not.
- **Cheapest test:** Enumerate the garage's write paths; mark which pass through a chokepoint that could verify a contract. The uncovered fraction is the honest ceiling on any enforcement claim in this file.
- **Risk:** none — this is the null-hypothesis generator for everything above and should ride to triage stapled to the front. Draws on: **Cluster H, singleton 4 (Sandstorm — model exonerated, placement/cost convicted).**

### H29 — Derive the schema from the owner's existing manual exchanges before authoring it
- **Statement:** The owner is today the integration mechanism; every manual transfer is an implicit request-time contract already executing. Before any schema is authored (which §13.10 forbids through the curator anyway), the field set could be *derived observationally*: record the next N real exchanges against §8's twelve candidate fields and let field-usage frequency write the first draft.
- **Mechanism:** the derive-don't-assert discipline the repo applies elsewhere; the corpus exists and grows for free.
- **Class:** adjacent. **Level-up:** linear, but it de-risks the step-function ones.
- **Cheapest test:** it *is* the cheapest test — instrument, don't build. Falsified-as-premature if observed field usage is wildly inconsistent across exchanges.
- **Risk:** N is small; derivation may need months of natural corpus. Draws on: **§8/§13.**

### H30 — Expiry denominated in attention and budget, not wall-clock
- **Statement:** A contract's expiry field inherits clock semantics from IAM lineage, but garage phases have no natural clock — the actual death mode is the *stall* (ruvnet: 75 of 80 nights never reviewed, some 2.5 months stale, unnoticed). Expiry could be denominated in the binding resources: a contract expires after consuming X owner-gates or Y budget without reaching acceptance — making abandonment a *detected disposition* rather than an ambient smell.
- **Mechanism:** both denominations are countable (H12's static gate count; IBCT budget ceilings); expiry-by-resource turns Cluster G's constraint into the liveness signal H23 needs, and gives `abandoned` a trigger instead of a vibe.
- **Class:** non-obvious. **Level-up:** linear.
- **Cheapest test:** Retro-apply resource-denominated expiry to ruvnet's public record and to garage stalls: would it fire where clock expiry wouldn't, without false-firing on legitimately slow work?
- **Risk:** cross-domain, the issuer must observe the executor's consumption — H23's observer problem again; a staller can stop attesting, so expiry must fire on attestation *silence*, quietly reintroducing a clock. A real limit, stated. Draws on: **Clusters G + C.**

---

## Where the collapse breaks — the consolidated ledger

Eight fracture lines, descending by how much of the collapse each takes with it.

1. **No shared state observer across trust domains (H23).** The *deepest* fracture — it is the parents' actual point of divergence. Repair exists (state attestation, the CT move) but note what it concedes: the collapse holds only where **every transition is a signed, checkable record** — the collapse is not free; it *costs* the full Cluster D apparatus as a precondition.
2. **Information does not attenuate (H25).** The attenuation-only safety story is an action-plane story. The unified type survives only with disclosure as a separately-governed, non-attenuable, enumerated field — "one type" is really "one type with two incompatible field disciplines inside it," a genuine dent in the elegance claim.
3. **Aggregation crosses contract boundaries (H20, H26).** Forty years unsolved, renamed twice in 2026, and the collapse *concentrates* the blind spot. Partial narrowings exist; no repair closes it. Any verdict must carry aggregation as an explicitly accepted residual risk.
4. **Widening across phases (H2/H8).** Repairable, but the repairs put a minting key inside the checker — quietly answering "smallest trusted core" with "the transition checker," a *bigger* concession than it looks.
5. **Trust accounting cannot late-bind (H24).** The collapse holds, but "phase" and "contract" remain *distinct roles* of the one type — issuance-time is a parameter with teeth.
6. **Revocation asymmetry (H22).** One-directional repair only: phases adopt count-bounds; contracts never get free stopping.
7. **Mutual exclusion and partition (H3, H16).** The fan-out partition lives naturally in the *layout*, not the contract — evidence the workflow-as-whole retains at least one irreducible job.
8. **A type is not a boundary (H28).** The meta-fracture. The likeliest outcome of this whole line is a schema nothing enforces. Placement at an unbypassable chokepoint is not an implementation detail; it is the difference between architecture and documentation.

**Net structural read (conjecture, not verdict):** the collapse survives as *one record type with three parameterized differences* — signer/issuance-time, verification profile (local vs cryptographic — macaroons' first/third-party split proving one type spans it), and disclosure discipline (attenuable authority vs enumerated one-way information). It fails as "phases and contracts are interchangeable": the phase keeps two irreducible jobs (review amortization, trust-accounting denominator) and the layout keeps one (partition). **The most consequential single conjecture in the file is H5** — if the two uncovered remainders are one seam, the theme's residual build surface is roughly half what the framing assumes, and it is checker-shaped, not kernel-shaped, which is where every other line of evidence in this run was already pointing.

---

## Compact index

| # | One-line | Class | Target |
|---|---|---|---|
| H1 | §8 fields map onto phase fields; residue is two parameters | obvious | cross-program coordination |
| H2 | phases attenuate from the instance root, not each other | adjacent | phase-indexed authority |
| H3 | ordering = data-dependency + leases (in-toto as phase engine) | non-obvious | workflow state |
| H4 | SoD as identity-history caveat; WSP is the price, FPT at our scale | adjacent | acceptance/verification |
| H5 | the two uncovered remainders are one object: transition = checked commit | non-obvious | the differentiating seam |
| H6 | cross-domain acceptance via ordered evidence-kind floor | non-obvious | cross-program acceptance |
| H7 | consequence class as a monotone attenuable ceiling | adjacent | typed actions × delegation |
| H8 | earned authority minted by the checked transition | adjacent | smallest-trusted-core candidate |
| H9 | binding time is per-field, not per-contract | non-obvious | schema principle |
| H10 | compile-time binds envelopes; run-time binds instances | adjacent | dynamic fan-out |
| H11 | attenuation-only runtime intent: safe for actions, free audit | adjacent | run-time binding safety |
| H12 | owner gates as third-party caveats → attention statically countable | non-obvious | owner gates × Cluster G |
| H13 | the dial's real name is attention amortization | adjacent | binding-time decision rule |
| H14 | GH Issue = degenerate contract; missing-field delta = adapter spec | obvious | §7 transport |
| H15 | done_when+proven_by+grade is half a contract; dogfood before Jurati | adjacent | Unimatrix as first plane |
| H16 | this assignment is an instance; exhibits a missing `partition` field | whitespace | schema completeness |
| H17 | skills are contracts minus the authority field; FORTIS measured the hole | adjacent | skill invocation |
| H18 | tool call = micro-contract; verify consequence declarations on owned server | adjacent | first Unimatrix enhancement candidate |
| H19 | second-brain elevation is a cross-instance contract | whitespace | §10 product decision |
| H20 | serial attenuated contracts compose into forbidden wholes | adjacent | collapse safety case (attack) |
| H21 | trust accrues to issuing program; executors ephemeral; PROV edge | adjacent | trust graduation |
| H22 | phases must adopt count-bounds; contracts never get free stopping | adjacent | expiry/revocation |
| H23 | TBAC's central-observer assumption is the fault line; attest state | non-obvious | cross-domain viability |
| H24 | abolishing compile time fails on trust accounting | non-obvious | cached-intent framing |
| H25 | disclosure doesn't attenuate; needs a one-way staged field | non-obvious | information flow (attack) |
| H26 | bound the issuance channel itself | whitespace | aggregation narrowing |
| H27 | deviation as typed MEL-style amendment, signed by a non-operator | non-obvious | supervision/recovery |
| H28 | a type is not a boundary; value concentrates at real chokepoints | adjacent | enforcement placement (null-hyp) |
| H29 | derive the schema from observed manual exchanges before authoring | adjacent | pre-architecture input |
| H30 | expiry denominated in attention/budget, not clock | non-obvious | stall detection |

**Attention accounting:** gate-*reducing* — H12, H13, H6, H21, H30. Gate-*adding* if done naively — H25 (disclosure enumeration), H27 (amendment signing), H22 (re-auth round trips, machine-borne, near-zero owner cost). H16/H29 are owner-cost-neutral observation moves.

**For the curator (when routed):** each hypothesis is a `finding` tagged `hypothesis`, `theme:workflow-harness`, `wfh-007`. Conjectured edges: H9/H23 `Supports`-shaped toward #256; H15 `Contradicts`-shaped against the §10 Jurati/Unimatrix boundary candidate; H20/H25/H28 are `Contradicts`-shaped against H11/H5/everything respectively and **should be filed as such rather than smoothed**.
