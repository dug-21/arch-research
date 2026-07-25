# M5 — Constraint inversion + the residual after full configuration

**Run:** `wfh-004` · Issue #48 · phase `hypothesize` (rebuild) · read-only, zero graph writes.
**Read:** BRIEFING-v2 (full), W0-c (full), W0-b §3–5, W0-b2 §2–3. **32 candidates.**

---

## 1. Candidate register

Fields: **Ab**ility · **Co**ncern · **La**yer · **Me**chanism · **In**ference · **Δ** sec/rel · **Do**main · **Inc** (R=research/S=SDLC) · **Ev** · **Fa**lsifier.

### Cluster A — the C-4 family: necessarily-external authorities

**M5-01 — External binding authority.** The harness binds every agent's authority under a policy the agent cannot alter; any attempt to modify its governing policy is refused and recorded, **regardless of what tools the agent holds**. *Security · HARNESS ·* **Me:** fixed-point — a constraint stored where its subject has write authority is rewritable by the subject and therefore constrains nothing. **In:** D. **Δ:** Sec↑. **Do:** B= (strongest class). **Inc:** R available-but-unflipped (*turns on A-4, A-6*); S platform plane exists and is entirely off. **Ev:** reasoned. **Fa:** A-6 negative *and* no OS confinement deployable → the binding principal doesn't exist here and the ability is vacuous.

**M5-02 — Observer-produced record.** The record of what an agent did is produced by an **observer of** the agent, not by the agent. *Introspection · HARNESS ·* **Me:** self-attestation is not attestation — the reporting channel and reported party must be distinct principals or the report is a claim. **In:** D — collapses a large (P). **Do:** B=; **shared *origin* evidence: P-05/P-06 have SDLC origin #208 — one harness defect, two surfacings.** **Inc:** R hooks fire but attribution doesn't persist (*A-10*); S two stores disagree — **verify/test agreement 44%**. **Ev:** field, both domains. **Fa:** observer records and self-reports never materially diverge across a measured run set.

**M5-03 — Verifier integrity.** The party being graded cannot modify the thing that grades it — writes by a graded principal to verifier definitions, fixtures, or expected-outputs are refused. *Security · HARNESS ·* **Me:** M5-01's fixed-point one level down. **This is the exact altitude at which SDLC's configured enforcement failed — CI was external, the fixture was not.** **In:** D. **Do:** B=. **Inc:** R `factory-researcher` is "read-only" in prose while holding every write tool (*A-3, A-5*); S the fix-that-made-every-failure-read-PASS shipped through running CI. **Ev:** field (S). **Fa:** with verifier paths unprotected over a long series, no graded party ever touches them.

**M5-04 — External completion predicate.** A unit is complete only when a predicate **external to its author** says so; every terminal state names the predicate that granted it. *Structure · HARNESS; predicate content DEFINITION ·* **Me:** self-certified completion is not completion — the merged-on-`CONDITIONAL PASS` unit is the mechanism demonstrated by absence. **In:** P→D for evaluation/recording; **I** where the predicate is semantic. **Ev:** field (census). **Fa:** if authors cannot state completion predicates more cheaply than reviewing completion claims.

**M5-05 — External liveness authority.** A unit that stops making progress is **declared dead by the harness, not discovered by a human**. *Recovery · HARNESS ·* **Me:** a dead process cannot report its own death — the purest member; the reporter must survive the reportee. **In:** D. **Inc:** R no timeout keys (*A-7*); S "git saves the *bytes*, nothing declares the *unit* dead." **Fa:** A-7 positive and timeout keys cover the cases → **configuration, not product; move to §5 backlog.**

**M5-06 — External spend meter with admission control.** Every unit declares a resource envelope before it starts; consumption is metered against it by the harness; breach triggers the declared response. *Cost · HARNESS ·* **Me:** the spender cannot be its own trustworthy meter (under-reporting is free) and the model cannot count. **In:** D — collapses "consumption reconstructed by a parser." **Do:** B= — *"domain-independent and empty on both sides."* **Inc:** R one run built an instrument (*A-1*); S **zero cost incidents in 610 issues = absence of record.** **Fa:** measured variance small and total spend trivially low → ceremony.

**M5-07 — External time and order authority.** The harness, not any agent, assigns timestamp and sequence position; **"did the verdict exist before the dependent action" is answerable from record order alone.** *Introspection · HARNESS ·* **Me:** a party cannot attest *when* it acted. **In:** D. **Δ:** both↑ — ordering guarantees become statable. **Ev:** reasoned; field-adjacent.

**M5-08 — Externally-selected audit sample.** Which outputs get re-checked is decided by the harness **after the fact, unpredictably to the producer**. *Self-improvement/Security · HARNESS ·* **Me:** an audited party choosing its own sample selects its best work. **Unpredictability converts "spot-checks pass" — the dangerous-middle hazard — into a measured rate.** Precedent: tax audits, risk-limiting election audits. **In:** D for selection; re-check may be I or D. **Inc:** neither domain samples — review is 100% or 0%. **Fa:** disagreement rates indistinguishable from zero across producers and epochs.

**M5-09 — Issued identity, bound to the unit.** Every principal's identity is **issued by its spawner** and stamped by the harness onto every action; identity survives the death of the agent **because it is bound to the unit, not the process**. *Introspection/Security · HARNESS ·* **In:** D. **Do:** B= — the one defect with documented shared origin. **Fa:** A-10 positive and attribution persists → configuration; demote.

**M5-10 — Injector-authored context manifest.** What was provided, why, and **what was deliberately excluded**, produced by the injector *before* the step runs. *Context · HARNESS ·* **Me:** the agent cannot know what is not in its context — **the account of provisioning can only come from the provisioner.** **In:** D — pure (P)→D; the injector already computed the selection. **Do:** B= — both per-concern verdicts name the identical residual: *"retrospective only."* **Fa:** manifests never consulted when diagnosing a failed unit.

**M5-11 — Obligation ledger with external discharge (E-1).** Every commitment created during a run exists as a harness-held obligation that **only an observed event can discharge**; a run cannot close with undischarged obligations except by explicit, attributed waiver. *E-1 · HARNESS; obligation types DEFINITION ·* **Me:** a promisor discharging its own obligation by assertion is self-certification. **The census gives the mechanism-by-absence twice: `SCOPE FAIL` declared and fired 0/231; 62/63 units carry no retro trace.** SDLC's xfail-with-mandatory-issue is the working precedent. **In:** D for ledger/discharge/blocking; **P** at capture. **Ev:** field, census-backed, both domains — **the strongest-evidenced candidate in this register.** **Fa:** most obligations end waived rather than discharged.

### Cluster B — what falls out of C-2's jurisdiction

**M5-12 — Verdict as typed record with attempt identity.** Unit id, attempt number, verdict value, verifier identity, evidence reference; **overwriting is structurally impossible.** *Introspection · HARNESS · D ·* **Me:** ≥53 gate failures overwritten *because the verdict lived in a mutable file with no attempt identity* — **the failure names the missing representation exactly.** **Fa:** attempt histories never read by any consumer.

**M5-13 — Closed verdict vocabulary, enforced at admission.** A verdict is accepted only if a member of the declared answer set — **a `CONDITIONAL PASS` cannot enter the record because no definition contains it.** *Structure · HARNESS; vocabulary DEFINITION · D ·* **Δ:** both↑; **honest cost: a genuinely novel situation must route to escalation, not to a new ad-hoc verdict — desired, but a behavior change.** **Fa:** definitions accumulate escape-hatch vocabulary ("OTHER: see prose").

**M5-14 — Verdict-before-action ordering enforced.** A dependent action is refused unless its verdict record exists — **a merge or phase advance without its matching verdict is not discouraged but impossible via the harness**, and the refusal is recorded. *Structure/Security · HARNESS ·* **Me:** **the merge-with-no-gate-trace fix at the correct altitude** — the incumbent checked pipeline health when the question was run-object completeness. **In:** D around an I leaf. **Ev:** field. **Fa:** if every no-verdict action turns out a legitimate emergency override, the gate needed an override channel, not a wall.

**M5-15 — Re-checkable verdict envelopes.** Every model-issued verdict stored with the exact evidence span, question, and answer set — **any verdict can be re-posed later to another model, a human, or a future better judge, as a fair replay.** *Introspection · HARNESS · D capture around an I leaf ·* **Me:** re-checkability requires the input envelope, **known at ask time — capture is free then, impossible later.**

**M5-16 — Verdict-outcome calibration.** Every gate verdict is later scored against the downstream outcome of the unit it passed; **each verifier carries a measured miss rate.** *Self-improvement · HARNESS ·* **Me:** the linkage exists in the field already — **52% of bugfixes name a prior internal unit as origin — a gate-miss signal nobody joins back to the gate that missed.** Also answers the judge-bias epistemics: bias is systematic so voting can't fix it, **but ground truth arriving later can measure it.** **In:** D. **Fa:** origin attributions too noisy to join.

**M5-17 — Kind-diverse verifier composition.** A gate can require concurring verdicts from verifiers of declared **different kinds**; a gate declared kind-diverse cannot pass on any number of same-kind verdicts. *Structure/Security · HARNESS ·* **Me:** two independent agent reviewers ratified a wrong diagnosis; the human caught it — **kind-diversity is the only composition that adds independence rather than variance reduction.** **Ev:** field. **Fa:** cross-kind disagreement as rare as same-kind in practice.

### Cluster C — C-1 inverted

**M5-18 — Substrate-boundary refusal predicates.** Every substrate a run writes to can refuse a write violating a declared precondition **at its own API boundary** — with the harness remaining the only *orchestrator*. *Security/Structure · HARNESS ·* **Me: the counterexample is in production** — the Unimatrix rate limiter refused writes mid-run, deterministically. **Refusal at a boundary is not orchestration:** the store initiates nothing, sees only its own API, decides only admissibility — jurati#12's actual prohibition is untouched. W0-b independently marks the syntactic half of firewall enforcement *"deterministic, cheap, and currently unbuilt."* **In:** D. **Δ:** both↑ — **defense in depth: the invariant survives a compromised or buggy *harness*, which single-plane enforcement does not.** **Fa:** every refusal the substrate would issue is already caught upstream — measure unique catches.

**M5-19 — Authority out-of-band of the token stream.** What an agent is *permitted* to do is never carried in, or derivable from, the content it reads — **injected text can change what an agent says, but cannot change what its actions are allowed to effect.** *Security · HARNESS ·* **Me:** the physics is that the token stream carries no privilege field. **The inversion: stop trying to label the channel — make the channel irrelevant to authority.** Prompt injection is demoted from privilege escalation to influence-within-bounds. **In:** D. **Δ:** Sec sharply↑ — **the only mechanically available answer to the instructions-in-data *cannot*.** **Ev:** reasoned; zero field incidents — the named blind spot. **Fa:** if practical damage flows through *content* rather than *actions*, bounding actions doesn't touch realized risk.

### Cluster D — C-3 inverted in sign

**M5-20 — Run-state with artifact-grade semantics.** The run's own state has the same durability guarantees as SDLC's delivery record: durable, addressable by a stranger, diffable, mutation-leaves-a-trace. *Structure/Recovery · HARNESS ·* **Me: C-3's re-test resolves as — files-as-source-of-truth is not the constraint but the incumbent's *best property*.** The ≥53 overwritten verdicts happened precisely where run-state **lacked** these semantics while the code next to it **had** them. **Substrate-neutral:** any store providing append-only + addressing + delta satisfies it; the file tree is the proven precedent, not the mandate. **Do:** B= — **the candidate that makes the free-for-SDLC list portable to research *and* extends it to state SDLC itself doesn't cover (the run object, which git does not version).**

**M5-21 — Every unit ends in exactly one terminal state.** No unit can be silently abandoned; a run cannot close while any unit is non-terminal. *Recovery · HARNESS; vocabulary DEFINITION ·* **Me:** conservation of units — everything spawned is accounted for. **Fa:** if non-terminal units at close are always intentional dead-ends, refusal becomes waiver-stamping.

### Cluster E — inverted unexamined assumptions

**M5-22 — The disposable population.** A unit that fails verification is **re-run with a fresh instance** rather than corrected in-conversation; success rate vs in-place correction is measured. *Reliability/Recovery · HARNESS ·* **Me:** inverts "the LLM is the thing being controlled." *Stochastic error is detectable by repetition* — **but only if repetition is with fresh sampling, not a context already contaminated by the failure.** Also dissolves part of recovery: **"resume the subagent" (the unit has no key) is replaced by "re-run the unit," which does.** **In:** D orchestration around unchanged I leaves — **removes no inference; changes what inference failure costs.** **Δ:** cost up-front honestly; the wager is verification-per-attempt < debugging-per-conversation. **Fa:** fresh-instance retry no better than in-place at equal spend.

**M5-23 — Invariants that survive a hostile agent.** Every guarantee is stated and tested under the assumption that **any agent's output may be arbitrary**; invariants failing this are labeled *tendencies*, not guarantees. *Security · HARNESS ·* **Me:** the cheapest attacker model is also the most general — **a compromised agent is indistinguishable from a sufficiently unlucky honest one**, so Byzantine-style invariants buy reliability and security with one property. **Makes the guarantee/tendency demotion labeled and auditable.** **Fa:** if every useful behavior is a tendency and the guarantee set is near-empty, the framing partitions without informing — **though even that is the honest map.**

**M5-24 — Escalation-branch drills.** Every declared escalation or failure branch is **exercised** — a branch with no firing record is flagged unverified. *Recovery/Self-improvement · HARNESS ·* **Me:** `SCOPE FAIL` fired **0/231** — **a declared branch with zero executions is unfalsifiable as infrastructure**, and its non-firing is indistinguishable from its being unreachable. W0-e gives the deeper reason: **model compliance drops *terminal* constraints first — and escalation branches are terminal constraints.** Precedent: fire drills, chaos engineering, DR testing. **Ev:** field, census-backed. **Fa:** drills pass but production firings still fail (environment divergence).

**M5-25 — Mid-run steering with delivery receipt.** Human intent enters a running workflow, is recorded, delivered at the next declared boundary, **and its delivery is verifiable**; an undeliverable steer surfaces rather than vanishing. *Human steering · HARNESS; block-vs-surface DEFINITION ·* **Me:** the receipt half is this lens's contribution — **a steering channel without delivery confirmation recreates P-01's refuted folklore** (a file written specifically to steer, and the behavior recurred). **Δ:** security neutral-to-up — **an unauthenticated steering channel would be a new injection surface, so receipt and attribution are load-bearing for the delta being non-negative.** **Inc:** *turns on A-8*. **Fa:** A-8 negative and no alternative injection event → unreachable in the incumbent; a platform requirement, not a harness ability.

**M5-26 — Typed values cross boundaries typed.** A number, count, identifier, or enum crossing an agent boundary travels as a **typed field, never re-encoded into prose and re-extracted**. *Context/Structure · HARNESS ·* **Me:** the (P) reservoir's worked examples are all this shape — **the value was born typed and was flattened into prose by the handoff convention.** **In:** pure (P)→D. **Δ:** Sec↑ — **typed fields are matchable by enforcement predicates**, feeding the residual's "spend/time/phase are not matchable" absence.

**M5-27 — Manifest-based absence detection.** "Is anything missing?" is answered against a declared manifest, **never by asking a model to notice absence**. *Structure/Introspection · HARNESS; manifest DEFINITION ·* **Me:** absence detection is dangerous-middle *for a mechanical reason* — **there is no token for the thing that isn't there.** Set difference has no such limit. **The manifest *is* the independent representation the model lacked.** **Fa:** if the important misses are unenumerable-in-advance, manifests catch only the known shape — a real bound.

**M5-28 — Continuous record reconciliation.** Where two records claim to describe the same events, the harness continuously reconciles and alarms on divergence. *Introspection · HARNESS ·* **Me:** gate 71%, security 78%, design 79%, **verify/test 44%** — **and the disagreement was discovered only by a one-off manual census. Double-entry's actual mechanism is not two books; it is routine reconciliation of two books.** **Fa:** divergence dominated by benign convention drift → alarm fatigue; measurable as time-to-mute.

**M5-29 — Shadow inference as canary over deterministic rules.** Deterministic enforcement paths run with a **non-blocking model shadow** that flags cases where the rule's verdict looks wrong; **zero shadow influence on the outcome.** *Self-improvement · HARNESS ·* **Me:** the strongest counter-thesis — *a wrong rule is wrong systematically and invisible to every statistical instrument, reproduced identically forever.* Repetition can't detect deterministic error — **but a differently-wrong observer can flag it.** Inverts the run's default direction: **here inference audits determinism.** The model sits in its reliably-good envelope; the enforcement path stays inference-free **so the guarantee is not demoted.** **In:** I, deliberately and non-blockingly — **adds** inference, off the enforcement path. **Fa:** disagreements ~always shadow error.

**M5-30 — Definitions mined from observed practice.** The harness can propose a definition, or a delta, **from the record of runs actually executed** — a diff between declared and observed ("declared 2-rework bound; observed up to 4") plus a candidate formalization a human ratifies. *Self-improvement · HARNESS ·* **Me: W0-b2b *is* the manual proof** — the five-definition diff recovered ten shared invariants from artifacts alone, **a mining run performed by hand.** Inverts "humans author the definitions": **humans ratify them.** **In:** I for proposal (reliably-good class, external checker present); D for the conformance diff. **Fa:** mined definitions codify current bad habit — mining without outcome calibration automates the status quo.

**M5-31 — The harness records itself.** The harness's own acts — injections, refusals, spawns, policy evaluations, config in force — are recorded in the same durable, attributed record as agent actions. *Introspection · HARNESS ·* **Me:** inverts "the harness is trusted infrastructure." **Today "what configuration produced this run" is unanswerable even in principle** — `settings.local.json` is gitignored. **Also the precondition for the residual's comparison substrate.** **In:** D.

**M5-32 — Pull-context with a request record.** An agent may *request* context mid-step; every request — granted or refused — is recorded with what was served. *Context/Security · HARNESS ·* **Me:** inverts "context is pushed before the step." **The five definitions deliberately context-starve reviewers — starvation is a *feature* with no relief valve**: an under-provisioned agent silently guesses. **The request log doubles as a security instrument: requests outside declared scope are a probe signature the record has never been able to show.** **Fa:** agents never use the channel, or use it to re-acquire what starvation deliberately withheld.

---

## 2. The constraint verdict table

| Constraint | Verdict | Mechanical reason / unlock / settling test |
|---|---|---|
| **C-1** as written — *a knowledge substrate cannot enforce* | **PRACTICE** | An architecture decision (jurati#12 forbids substrate-as-*orchestrator*); the substrate's own rate limiter is a live counterexample. **Unlocks M5-18, two-plane defense in depth** |
| **C-1** narrowed — *the substrate cannot initiate or observe actions outside its own API* | **PHYSICS** | A store sees only requests made to it; no event loop over the world. **Surviving form: "the substrate cannot orchestrate, but it can refuse"** |
| **C-1(b)** — token-stream trust labeling | **PHYSICS (architecture-relative)** | The representation carries no privilege field. **Route-around exists: make the channel irrelevant to authority (M5-19)** |
| **C-2** as written | **PHYSICS at a much smaller core** | No deterministic procedure decides whether open prose satisfies a criterion. **Precision: the core needs a *semantic judge* — model OR human; C-2 as written under-counts the human option.** Everything else is **PRACTICE**: vocabulary, record, ordering, envelope, attribution, calibration, consequence-routing. **C-2 governs one label per gate; it was being read as governing the gate** |
| **C-3** — files stay source of truth | **CONFIRMED — with sign inverted** | It holds, but it is **not a constraint on the harness; it is the incumbent's strongest asset generalized.** The ≥53-overwrite class happened exactly where run-state lacked git's properties while the code beside it had them. **Unlocks M5-20/21 — extend those semantics to run-state, don't fight them** |
| **C-4** as written | **Premise PRACTICE, core PHYSICS** | The premise (agent holds the credentials) is configuration. The core is physics by fixed-point: **a policy writable by its subject is rewritable by its subject — true for humans and institutions too, which is why the family generalizes so far** |
| **C-5** — fresh-process escape | **UNDECIDED** | Settling test = **A-6**. Until settled, **every Security claim resting on M5-01 is provisional** |
| *Subagent is not a resumable unit* | **PRACTICE** | An addressing-scheme choice; **M5-22 dissolves the need — re-run the unit (which has a key) instead of resuming the agent (which doesn't)** |
| *A/B is not expressible* | **UNDECIDED, leaning PRACTICE** | The *retrospective* half is blocked only by missing capture. Settling test: implement M5-31 capture for two runs and attempt a matched-pair comparison; **what remains impossible after capture is the physics part** |

**Confirmed constraints are findings:** C-1-narrowed, C-2-core, C-3, and C-4-core are load-bearing walls the build can lean on — **every candidate above is placed *on* one of them, not against them.**

---

## 3. The C-4 family — necessarily external authorities

**The generating rule (fixed-point): any authority whose exercise evaluates the party exercising it is void when held by that party.** Fourteen members, as abilities:

1. **Binding** — a bound the subject can rewrite is not a bound. *(M5-01)*
2. **Attestation of record** — a record produced by the recorded party is a claim. *(M5-02, M5-31)*
3. **Grading** — a verifier writable by the graded party is internal in effect. *(M5-03)*
4. **Completion** — self-certified completion is not completion. *(M5-04)*
5. **Liveness** — a dead process cannot report its own death. *(M5-05)*
6. **Metering** — the spender is not its own trustworthy meter; and the model cannot count even honestly. *(M5-06)*
7. **Time and order** — a party cannot attest when it acted. *(M5-07)*
8. **Audit selection** — a party choosing which outputs are inspected selects its best. *(M5-08)*
9. **Identity** — a self-assigned name is a claim. *(M5-09)*
10. **Knowledge of absence** — the agent structurally cannot know what is not in its context. *(M5-10)*
11. **Obligation discharge** — a promise discharged by the promisor's assertion is self-certification. *(M5-11)*
12. **Waiver** — releasing a party from an obligation is an authority the obligated party cannot hold. *(in M5-11/21)*
13. **Retry identity** — the model cannot idempotent-retry; dedup/at-most-once authority is external. *(in M5-22)*
14. **Configuration attribution** — a configuration cannot evaluate itself. *(M5-16, M5-31)*

**The family's practical edge:** members 2, 5, 7, 10, 13 are ***impossible*-class** (the subject structurally lacks the information or the survivability); 1, 3, 4, 6, 8, 9, 11, 12, 14 are ***void-when-self-held*-class**. Both are structurally-impossible-elsewhere in screen-6 terms; **the first class cannot even be approximated by a well-behaved agent.**

---

## 4. The residual after full configuration — the build-decision headline

Assume every switch flipped in both domains: deny rules, per-agent tool restriction, sandbox, telemetry+traces, managed settings, timeouts, `SubagentStop`, branch protection, required reviews, CODEOWNERS, required status checks.

**The SDLC falsification test is decisive about the residual's *kind*.** SDLC had *more* configured than research — and: a merge landed with no gate trace; a fix shipped that made every failure read PASS; a release could not be installed; `SCOPE FAIL` fired 0/231; ≥53 verdicts were overwritten; a unit merged on a verdict from no vocabulary. **No listed switch fixes any of these, because every switch is a predicate over the wrong nouns:** tool calls (hooks), pipelines (CI), sessions (timeouts), files (deny rules), branches (protection). The failures live on nouns no component holds.

> ### The combined residual — one representational absence with five faces
>
> **The unit of work does not exist as an object anywhere a switch can see it.** Therefore, mechanically un-expressible today, in either domain, at any configuration setting:
>
> 1. **A durable run/unit object** between "session" and "tool call" — with identity, attempt count, and lifecycle. *(No hook matcher takes `unit_id`; no branch protection takes "run.")*
> 2. **Verdicts as typed, append-only, vocabulary-closed records ordered before their dependent actions.** *(A required status check sees a pipeline exit code; it cannot see that the gate report was overwritten, off-vocabulary, or absent-but-merged.)*
> 3. **Authority as data on principals and calls** — so enforcement can express role×step×resource, and injection cannot escalate. *(Deny rules are session-global; per-role scoping has no home.)*
> 4. **An obligation ledger with external discharge.** *(SCOPE FAIL 0/231 and 62/63 missing retros are unexpressible as any hook, check, or protection rule — they are commitments over run-lifetime, and nothing holds run-lifetime.)*
> 5. **A comparison substrate** — config-in-force and corpus-version as recorded values joinable to outcomes.

**This confirms the prior five-absence answer and sharpens it:** the SDLC evidence shows the five are **not independent gaps but one missing object model** — absences 2, 4, and half of 3 and 5 are properties *of* the missing unit object in absence 1.

> **"Enforcement at the wrong altitude" means exactly: enforcement exists, attached to nouns adjacent to the one that failed.**

**Per-domain:**
- **Research residual** = the combined residual **plus the entire free-for-SDLC list**, which has no incumbent at all.
- **SDLC residual** = the combined residual **plus an integration bill, not a construction bill** — bind existing git/CI nouns *to* the unit object rather than supply replacements. Plus SDLC-specific hards the object model must respect: irreversibility, verifier latency as cost, shared-substrate concurrency.

**One product or two?** Both readings, stated not decided:
- *One product:* the residual object model is byte-identical across domains — every difference is a declared parameter, and the same hook binary already serves both domains in three repos. **The domains differ only in integration profile** — a deployment parameter, not a product boundary.
- *Two products:* the evidence models differ in kind — SDLC's is an **executable predicate that re-runs**; research's is an **attested artifact of a past demonstration**. If the verification core cannot hold both natively, the "parameter" is a fault line. **Settling observation: whether P-2/P-3 can be expressed as one evidence interface with two sources — a probe-queue item.**

---

## 5. The configuration backlog — explicitly configuration-not-product

**None of these belong on the shortlist; several belong on the drop-list with "solved by configuration" as the reason.**

**Research side:** R1 permission-deny for the `.claude/**` and `product/factory/**` trees + Unimatrix writes for non-curators (*A-4, A-5*) · R2 `tools:`/`disallowedTools:` on all six agent files (*A-3*) · R3 a second blocking `PreToolUse` entry (*A-2*) · R4 `SubagentStop` hook (*A-7* for crash) · R5 telemetry + traces (*A-10*) · R6 sandbox (*A-11*) · R7 disable provisioned bypass · R8 turn/time bounds · R9 version-control `settings.local.json` · **R10 managed-settings tier as the binding principal — *A-6, the load-bearing probe***.

**SDLC side:** S1 branch protection + required APPROVED review · S2 **agent runs on its own token, not the human's** — a distinct principal, precondition for authority-as-data · S3 CODEOWNERS on verifier/fixture/workflow paths (a configuration-grade approximation of M5-03) · S4 required status checks incl. gate-report-presence (borderline: the check script is a small build; the *requirement* is config) · S5 protected paths for gate-report files (blunts the overwrite class; attempt identity still needs M5-12).

**The honest caveat:** on Security and Introspection, *"the incumbent is inadequate" is not yet an available claim.* **The probe queue inherits A-1 through A-12 wholesale.**

---

## 6. Coverage statement

**Populated:** Structure (04, 13, 14, 17, 20, 26, 27) · Context (10, 26, 32) · Security (01, 03, 08, 18, 19, 23) · Introspection (02, 07, 09, 12, 15, 28, 31) · Cost (06) · Self-improvement (08, 16, 29, 30) · Recovery (05, 21, 22, 24) · Human steering (25).

**Thin cells, with reasons:** *Human steering* — constraint inversion sees steering only where an authority or assumption inverts, and the field record is structurally silent. *Cost* — the inversion "cost measured after → admission before" is one move; the field shows an **unmeasured** cell, not a shaped one. **Neither is manufactured to fill the box.**

**E-1 engaged, confirmed:** the two strongest census facts (`SCOPE FAIL` 0/231; 62/63 missing retros) are **obligation failures, not observation failures — no amount of introspection fixes a commitment nobody holds.** The C-4 family contributes its mechanism (discharge and waiver are necessarily external). **E-1 passes the two-tier test from this lens independently.**

**Proposed E-2 (AMBIGUOUS) — record integrity.** The record as a *trustworthy object* — observer-produced (02), append-only with attempt identity (12), reconciled (28), covering the harness itself (31). **Introspection asks *what happened*; E-2 asks *whether the account can be trusted against a party with motive and write access*.** Counter: it may be Introspection's foundation rather than a peer. Both stated; triage decides.

**Shared-surface caveat, live:** BRIEFING §7 itself named double-entry, watchdogs, and capabilities as the superseded round's mature answers, **so M5-05, M5-19, and M5-28's mechanism choices were primed by the surface** even though each is re-derived here against two-domain evidence. The superseded registers themselves were not read.

**One flag for triage:** the run's evidence base is now **census-heavy on SDLC and anecdote-heavy on research**; several "both-identically" claims rest on one census and one story. **A cheap research-side census (the FINDINGS corpus is small) would harden or break the 14-spine before anything is built on it.**
