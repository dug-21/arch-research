# W2 findings — `vnc-045` software-delivery reconstruction and vocabulary mapping

**Workstream:** W2 only · directional · software-delivery case  
**Case:** `dug-21/unimatrix` `vnc-045` · Issue #928 · PR #929 · merge `37c7b09aa0db6ba16f5f95dadd24c58adb4e6e2b`  
**Evidence rule:** actor-authored reports and reviews are claims/records. Test output, repository objects,
diffs, and forge merge metadata are observations only where mechanically captured. This document does
not rerun the historical workflow or tests and makes no `proven` or grade claim.

## Directional finding

The candidate vocabulary can reconstruct most of `vnc-045`, but not without strain. The nine nouns are
usable as a common envelope; the native terms `gate`, `risk`, `acceptance criterion`, `specification`,
`architecture decision`, `commit`, and `merge` must remain category- or workflow-specific semantics.
The eight verbs cover the broad lifecycle but are too coarse to preserve `review`, `reject/hold`,
`correct`, `commit`, and `merge` without subtype semantics. Autonomy and authority are demonstrably
independent: advisory reviewers exercised high judgment with no implementation authority, deterministic
test services exercised consequential admission influence with A0 autonomy, and implementation agents
had bounded write authority without scope authority.

The case decisively rejects any reading of audit/authorization *structure* as effective anti-forgery.
The human direction reduced the feature from protected-tag policy to a value-opaque mechanism, and the
merged implementation deliberately accepts arbitrary values on bare `Capability::Write`. What was
demonstrated is the mechanism's bounded behavior: direct tag mutation, atomic replace, preservation of
specified fields, routing/access checks, and audit-row shape at the tested seam. The anti-forgery policy,
identity attestation, evidence enforcement, and protected-tag vocabulary were deferred.

`lesson` has evidence for **multiple roles**, but not as a primitive lifecycle event: a problem or
correction is communicated as `claim`, `exception`, `surprise`, `decision`, or `directive`; reusable
guidance is derived from that history and may be admitted as a distinct durable `lesson-learned` Record
category when it has cross-work relevance. Feature-local corrections remain ordinary feature records.

## 1. Source alphabet ledger

| ID | Coverage | Use and exact evidence |
|---|---|---|
| S01 | used | Issue [#928](https://github.com/dug-21/unimatrix/issues/928): current body records the human-reduced mechanism-only scope, deferred `protected_tags`, design completion, Stage 3c and security results. Comments dated 2026-07-06 and 2026-07-07 preserve scope/product challenges, including the original anti-forgery overclaim and audit durability concern. The body is edited current state, not an append-only reconstruction of its earlier text. |
| S02 | used | PR [#929](https://github.com/dug-21/unimatrix/pull/929): body, 11 commits, 41-file change set, product-review comment, security review, and merge metadata. Merged 2026-07-07 at commit `37c7b09aa0db6ba16f5f95dadd24c58adb4e6e2b`. |
| S03 | used | `product/features/vnc-045/{SCOPE.md,IMPLEMENTATION-BRIEF.md,ACCEPTANCE-MAP.md,ALIGNMENT-REPORT.md,RISK-TEST-STRATEGY.md,SCOPE-RISK-ASSESSMENT.md}`. These define reduced intent, decisions, delivery units, risk model, acceptance mapping, and alignment claims. |
| S04 | used | `product/features/vnc-045/specification/SPECIFICATION.md` and `architecture/**`. Active ADRs 001/002/004/008/009 define the shipped mechanism; ADRs 003/005/006/007 are explicitly marked deferred and are historical design residue, not shipped behavior. |
| S05 | used | `product/features/vnc-045/pseudocode/**` and `test-plan/**`. These bind component behavior and tests; the gate-3a rework extracted `derive_namespace` and `check_tag_lifecycle` as runnable seams. |
| S06 | used | `product/features/vnc-045/agents/**`. Reports reconstruct delegation and handoffs for architecture, specification, risk, vision, synthesis, pseudocode, test planning, store/service/handler implementation, gate review, testing, and security. They remain actor-authored disclosures unless corroborated by repository/test evidence. |
| S07 | used | `reports/gate-3a-report.md`, `reports/gate-3b-report.md`, `reports/gate-3c-report.md`, and `testing/RISK-COVERAGE-REPORT.md`. Gate 3a records one reworkable interface failure then pass; 3b and 3c report pass; risk coverage records 6,961 workspace tests and 32 smoke tests green plus the audit-log integration gap. |
| S08 | used | PR-enumerated implementation/test files; implementation commits `a63d45f0` (store primitives), `74bc1fd4` (service/audit), `b68c2c43` (handler), `bf7c4812` (integration tests/reports), and merge `37c7b09a`. Repository inspection confirms direct `entry_tags` primitives, `Capability::Write` gate, `check_write_rate`, comment-only retrofit seams, `tokio::spawn` fire-and-forget audit, and the PR file set. |

No transitive artifact outside S01–S08 is relied upon as evidence. Research spikes #926/#927 and
Unimatrix entries named by the case documents explain provenance but were not independently used to
establish a W2 event.

## 2. Actual chronology

| Order | What materially happened | Evidence kind | Candidate expression |
|---|---|---|---|
| 1 | Research spikes `ass-093` and `ass-094` supplied mechanism and authorization/anti-poison inputs to a proposed `context_tag` feature. | Document claim in S01/S03; spikes not independently inspected. | Collective **directs** a Program to **form** a Mission from prior Records. |
| 2 | The initial scope combined a cheap in-place tag mutation mechanism with protected-tag/anti-forgery policy. The 2026-07-06 product scope review said the mechanism was clean but the anti-forgery promise lacked live teeth in OSS unless evidence binding landed; it also found the configuration surface too large. | Durable reviewer claim in Issue comment; the original Issue body was later edited. | Reviewer Actor **observes** source facts only where inspected, emits `finding`/`surprise`, and **verifies** scope semantics. “Observe” is strained because most review output is interpretation. |
| 3 | A human reduced scope on 2026-07-07: ship the value-opaque mechanism only; defer `protected_tags` in full. The surviving contract retained direct writes, atomic replace, complete audit shape, `Write` gate location, rate control, and quarantine refusal; it explicitly rejected any anti-forgery/access-control claim. | Authoritative decision recorded in current Issue body and SCOPE; exact conversational decision is not separately preserved. | A5 human emits `decision` + `directive`; Mission is **adapted** and Units are stopped/reformed. |
| 4 | Design was rerun/recompiled against reduced scope. Architect/spec/risk/vision/synthesizer artifacts defined 11 FRs, 7 NFRs, 7 ACs, 8 risks, active/deferred ADRs, component boundaries, and delivery brief. One stale vision-agent report still describes the pre-reduction `min_trust_level`/config design; the synthesizer report identifies that stale residue. | Actor reports and repository records at design commit `afaa8385`; internal consistency can be inspected, but report assertions remain claims. | Actors **execute** delegated Units; Records are created; synthesizer **adapts** derived deliverables to the directive. |
| 5 | Pseudocode and test plans were authored. Gate 3a initially returned `REWORKABLE FAIL` because inline handler decisions were not exposed at the required test seam. Rework extracted `derive_namespace` and `check_tag_lifecycle`; the repeated gate passed. | Gate record plus changed pseudocode at commit `3afc2c4`; gate judgment is a finding, repository delta is observation. | Gate Actor **verifies**; emits `exception` + `request`; pseudocode Actor **adapts** Unit; gate **verifies** again. No candidate verb directly means reject/hold/correct. |
| 6 | Store primitives were implemented at `a63d45f0`: direct `add_tag`, `remove_tag`, and atomic namespace-scoped `replace_tag`, plus escaped SQL LIKE matching and audit op-list inclusion. | Repository commit/diff observation; agent report claim. | Implementation Actor **executes** Unit within a write envelope. |
| 7 | `StoreTagService` and audit orchestration were implemented at `74bc1fd4`: rate check, primitive dispatch, one audit event, value opacity. Audit emission is fire-and-forget and discards the async write result. | Repository code observation; design-review concern and agent report. | Actor **executes**; deterministic service Actor causes effect. Audit Record admission is best-effort after mutation, not transactionally coupled. |
| 8 | MCP handler was implemented at `b68c2c43`: request context, `Capability::Write`, action parse, namespace/lifecycle checks, comment-only future seams, service delegation. | Repository commit/diff observation. | Actor **executes**; handler/service deterministic Actors apply Envelope constraints. |
| 9 | Gate 3b reported pass after pseudocode/code/security/test inspection. It recorded nonblocking pre-existing CVEs, adjacent clippy warnings, and a cosmetic stale allow. | Reviewer-authored finding; repository facts partly mechanically inspectable. | Reviewer **verifies**, emits `finding` and bounded `exception`; no authority to merge or change scope. |
| 10 | Stage 3c added and ran integration tests at `bf7c4812`. Durable reports state 6,961 workspace tests and 32 smoke tests passed, with 47 feature-specific unit/seam tests. Audit completeness was tested only via raw audit-log unit read-back because no MCP audit-read route existed. | Historical test report is an actor-authored Record containing mechanically generated results; not rerun by W2. Commit and test files are repository observations. | Tester **executes** tests; test runner **observes** results; gate Actor **verifies** admissibility. |
| 11 | Security review found no blocker and bounded blast radius to a single entry's tag rows; product PR review explicitly said the feature did not deliver poison resistance and no capability should move to `proven`. | Independent reviewer findings in PR and S06. | Review Actors **verify**; send `finding`/`exception`; human retains consequence authority. |
| 12 | PR #929 merged to `main` at `37c7b09a` on 2026-07-07. | Forge merge metadata and git object observation. | Authorized human/forge **executes** the irreversible publication effect after gates. Mission outcome becomes a durable repository Record. |
| 13 | Agent reports stored a rollback-test pattern and an async-audit read-back pattern in institutional memory; other agents explicitly recorded “nothing novel.” | Agent-authored stewardship claims in S06; underlying Unimatrix writes not independently inspected here. | Actors **learn** by deriving reusable guidance; curator-capable paths admit lesson/pattern Records. |

## 3. Delegated-agent and effect map

| Actor / service | Actual unit | Autonomy | Explicit authority envelope reconstructed from history | Effects actually evidenced |
|---|---|---:|---|---|
| Human owner | Set/reduce scope; approve priority and merge | A5 | Scope: organization/product and `vnc-045`; may change objective and accept deferral; may authorize irreversible forge effect; no budget evidence in case. Escalation terminates at owner. | Reduced scope; ultimately caused/authorized merge. Exact identity behind forge account is not attested by the records. |
| Primary delivery coordinator / synthesizer | Form work, delegate specialists, compile reduced brief | A2 | Scope: approved `vnc-045`; effects: feature docs and coordination records; may delegate bounded Units; denied scope expansion and final merge; must escalate variances/open questions. | Created/recompiled artifacts and reports; no evidence of program-selection authority. |
| Product reviewer (`uni-zero`) | Scope/design/PR challenge | A0 | Read/reason/recommend only; no code, scope, grade, or merge effect; escalate overclaim, capability impact, and sequencing concerns to human. | Produced consequential review findings, including the anti-forgery challenge. |
| Architect, specification, risk, vision actors | Produce domain designs and checks | A1 | Write only assigned feature documents/knowledge records as role allowed; no implementation, scope, or merge authority; escalate ambiguity/variance. | Created design Records. Vision report's stale pre-reduction content demonstrates that A1 authorship does not make a Record current. |
| Pseudocode and test-plan actors | Translate approved design into executable/testable plans | A1 | Assigned paths only; reversible repository writes; no implementation or acceptance authority; rework on validator request. | Authored plans and corrected seam design after gate-3a failure. |
| Gate 3a validator | Check design-to-plan fidelity | A0 | Read and issue bounded verdict; may block progression through workflow rule but cannot edit artifacts or redefine scope. | Returned reworkable fail, then pass. Consequence depends on process honoring verdict. |
| Store, service, handler implementation actors | Implement three bounded components | A1 | Assigned code/test/report paths; local reversible writes and tests; no scope, PR merge, protected-tag implementation, or grade authority; escalate contract deviation. | Commits `a63d45f0`, `74bc1fd4`, `b68c2c43` and reports. |
| Gate 3b validator | Code review against approved artifacts | A0 | Read/execute checks and emit verdict; no implementation or merge authority. | PASS finding with warnings. |
| Tester | Add/run bounded integration tests and risk report | A1 | Test-infrastructure paths; local build/test execution; may file failures, not waive them or merge. | Commit `bf7c4812`; reported test results and known gap. |
| Test runners / compiler / SQLite | Deterministically execute checks and mutations | A0 | Fixed command/code inputs; filesystem/DB resources as invoked; no initiative, interpretation, or delegation. | Exit/results used by human/agent gates; SQLite transaction provided rollback behavior. |
| Security reviewer | Inspect diff and threat surfaces | A0 | Read-only review/comment; no merge or implementation authority. | Low-risk/no-block finding; identified best-effort audit residual. |
| Git / GitHub forge | Preserve commits, PR metadata, and merge ref | A0 | Credentialed effects defined outside agent reasoning; accept authorized ref update; store immutable objects and mutable refs/metadata. | Recorded commits and effect-bearing merge. |
| Runtime MCP handler/service | Enforce `Write`, lifecycle, rate, then mutate/audit | A0 | Code-defined effect authority over one entry's tags and audit sink; value-opaque; self-declared `agent_id` is audit input, not authz. | Shipped mechanism. Audit effect is not atomic with tag mutation and can be silently lost after success. |

No actor is evidenced at A3 or A4. Local rework was directive-bound A1 action, not general authority to
change team/tactics; mission formation was A2; program selection was not part of this history. This is a
useful non-use result rather than a reason to force-fit actors into every tier.

## 4. Candidate noun mapping

| Candidate noun | Native instances in `vnc-045` | Ruling / strain |
|---|---|---|
| Collective | Human owner plus delegated agents/services operating across the Unimatrix repository and knowledge system | **Strained.** The repository history shows coordinated actors, but no durable object names or bounds “the whole organization”; authority root is inferred from human direction and forge control. |
| Program | Unimatrix product/software-delivery program | **Clean at broad level, weakly instantiated.** Issue/feature labels and repository supply the durable area; no explicit Program Record or budget appears. |
| Mission | Deliver `context_tag` mechanism under `vnc-045`, ultimately mechanism-only | **Clean.** Issue/SCOPE bind outcome and exclusions. Mission identity survived scope revision. |
| Capability | Assignable behaviors (`architecture`, `implementation`, `testing`, `security review`) and product behaviors (`tag mutation`, `audit`) | **Strained/overloaded.** Actor skill and product capability are different native meanings. The case explicitly says the feature completes no capability while still assigning human/agent capabilities. Common model needs `capability.kind` or must choose one meaning. |
| Unit | Scope review, architecture, spec, risk, pseudocode, component implementations, gates, tests, security review, PR/merge | **Clean as envelope; category required.** Units differ in lifecycle and admission rule. |
| Actor | Humans, agents, deterministic runners, MCP handler/service, SQLite, git/forge | **Clean if deterministic components count.** Otherwise effect-authority mapping loses important non-autonomous actors. |
| Envelope | Assigned paths/roles, scope/non-goals, capabilities, test commands, authority boundaries, merge control | **Clean structurally.** Resource ceilings are mostly absent from historical records; reconstructing them must not imply they were enforced. |
| Signal | Reviews, handoffs, gate verdicts, issue directives, reports, test outputs | **Clean if signal is typed transport, not durable artifact.** One Record can carry several signals. |
| Record | Issue, SCOPE, ADR/spec/plan/report, commit, PR, test report, audit row, merge metadata, learned pattern | **Clean only as envelope.** Category, provenance, admission, lifecycle, and current/stale status remain indispensable. |

Derived terms behaved as proposed with qualifications: a team was a temporary actor set; roles supplied
reusable capability/envelope expectations; workflow supplied ordered Units/gates; tools were effect
interfaces. A gate was **not purely deterministic**: mechanical checks fed semantic reviewer verdicts and
human consequence decisions. Defining every gate as “a deterministic condition” would misrepresent the
scope/product/vision reviews and must be revised to allow typed mechanical, semantic, and human-reserved
clauses with deterministic consequence routing.

## 5. Candidate verb mapping

| Verb | Case transitions | Ruling / strain |
|---|---|---|
| direct | Human establishes feature intent, then directs mechanism-only reduction | **Clean.** |
| form | Coordinator assembles feature mission, specialist waves, and review sequence | **Clean but inferred** from durable delegation reports. |
| delegate | Specialist tasks and path ownership assigned | **Clean.** |
| execute | Author documents/code/tests; services mutate; forge merges | **Overloaded.** Reversible authoring, deterministic testing, runtime mutation, and irreversible merge require effect subtypes. |
| observe | Test runner captures pass/fail; git/forge captures commits/merge; reviewers inspect source | **Revise.** Reserve `observe` for mechanically captured facts. Human/agent inspection produces a claim unless its capture mechanism is named. |
| verify | Scope/design/code/security/test/PR reviews evaluate evidence against criteria | **Clean as evaluation family**, but verifier kind and admission authority must be explicit. |
| learn | Agents derive rollback/audit-readback patterns and decide whether to admit them durably | **Clean only for derived reusable change**, not for merely writing any report. |
| adapt | Human reduces scope; design artifacts are recompiled; pseudocode corrected after gate failure | **Clean at broad level**, but must record who authorized the adaptation and which baseline it superseded. |

Material native transitions with no precise verb are `propose`, `challenge`, `hold/reject`, `correct`,
`commit`, `approve`, `merge/publish`, and `defer`. They can be expressed as typed combinations of the
eight verbs plus signals/effects, but repeated prose is required. At minimum, transition subtype and
consequence must be first-class; otherwise H1 risks cosmetic compression.

## 6. Consequential signal ledger

| Historical communication | Candidate class | Route and consequence | Evidence caveat |
|---|---|---|---|
| Initial feature proposal and research carry-forward | `request` + `claim` | Prior work → feature coordinator/human; caused scope formation | Source spikes not independently inspected. |
| Product scope review: anti-forgery has no live OSS teeth without evidence binding | `finding` + `surprise` | Reviewer → human authority; triggered/preceded direction change | Reviewed interpretation, not observation. Its cited code facts are separable observations only if independently inspected. |
| Human mechanism-only reduction | `decision` + `directive` | Authority root → all mission actors; stopped policy/config Units and reformed deliverables | Current Issue/SCOPE preserve decision, not the exact original utterance. |
| Reduced SCOPE/brief constraints (“no validator/config/min_trust_level”) | `directive` | Mission Record → delegated actors and gates | Durable constraint; enforcement partly procedural. |
| Architect/spec/risk/pseudocode handoffs | `claim` | Specialist → coordinator/downstream actor | Authored disclosure, admitted through design reviews rather than relabelled observation. |
| Gate 3a interface mismatch | `exception` + `request` | Validator → pseudocode actor/coordinator; blocked progression and requested extraction | Semantic gate finding corroborated by artifact delta. |
| Gate 3a pass after rework | `finding` + `decision` only if workflow delegates gate consequence | Validator → coordinator; allowed next stage | Verdict is a claim under criteria; not mechanical fact. |
| Implementation agent contract-deviation/warning notes | `exception` or `claim` | Implementer → coordinator/gate reviewer | Self-report cannot establish code behavior. |
| Test command results | `observation` when mechanically captured; enclosing report is `claim` | Runner → tester/gate; supplied evidence for admission | W2 sees durable report and files, not original raw logs; therefore historical numeric result remains reported observation. |
| Gate 3b/3c/security verdicts | `finding` | Independent reviewers → human/forge decision path | Review judgments; do not themselves cause merge absent workflow authority. |
| PR product review: no poison-resistance delivery, no capability flip | `finding` + `directive`/`decision` only when human accepts it | Reviewer → owner before merge | Prevents outcome inflation; exact acceptance is evidenced by final scope/PR language. |
| Merge metadata | `observation` | Forge → repository consumers/institutional history | Mechanically recorded effect, not a signal authored by an agent. |
| Stored rollback/audit-readback guidance | `finding` during admission; later routed as `lesson` only if lesson is a signal | Implementer → Unimatrix → future actors | Storage is actor-reported here; content may be Record-category pattern rather than lesson. |

Candidate `observation`, `claim`, `finding`, `request`, `exception`, `surprise`, `decision`, and
`directive` all occur. Classification is sometimes multi-label: “surprise” describes significance,
whereas “finding” describes epistemic/admission status. Treating them as mutually exclusive would lose
meaning. Signal schema likely needs orthogonal `kind`, `epistemic_status`, `severity`, and `authority`.

## 7. Durable Record, category, and admission ledger

| Durable artifact | Common Record category | Admission rule actually visible | Lifecycle/provenance requirement |
|---|---|---|---|
| Issue #928 body/comments | `mission` / `discussion` / `decision-log` | Forge accepts account-authored edits/comments; human authority determines binding direction | Body is mutable and currently reflects reduced scope; comments are chronological. Must distinguish authoritative decision from account attribution. |
| SCOPE.md | `mission-contract` | Human-locked/reduced scope accepted into git | Version/commit required; current file alone hides pre-reduction state. |
| Specification, architecture, ADRs, risk strategy | `design` with subcategories `specification`, `ADR`, `risk-register` | Specialist authorship plus alignment/design review | Active/deferred status is semantic and must survive Record envelope. Stale vision report proves “durable” is not “current.” |
| Implementation brief / acceptance map | `execution-plan` / `acceptance-map` | Synthesized from approved design; downstream gates check consistency | Supersession/recompile after scope change must be visible. |
| Pseudocode/test plans | `implementation-plan` / `test-plan` | Gate 3a; initial version rejected then corrected | Gate verdict and corrected commit bind admission. |
| Agent reports | `handoff-report` | Authored on completion; later reviewers may corroborate | Disclosure/claim only; never observation by category. |
| Source and test files | `artifact` | Git commit; later code/test review | Commit identity and diff are mechanical provenance; correctness comes from separate evidence. |
| Gate reports | `review-finding` / `gate-verdict` | Named reviewer evaluates frozen/identified artifacts against criteria | Must carry evaluator kind, evidence set, verdict, consequence, and whether advisory/blocking. |
| Risk coverage/test report | `test-evidence-report` | Tester gathers results; gate 3c adjudicates sufficiency | Raw logs absent from alphabet; report numbers cannot be silently promoted to fresh observation. |
| PR review/security review | `review-finding` | Forge-authored review/comment; human/merge policy decides consequence | Review state and commit target matter. |
| Commits and merge | `repository-effect` | Git object creation; forge authorization/ref update | Mechanically verifiable hashes; merge is effect evidence, not behavioral correctness. |
| Runtime audit row | `audit-event` | Service attempts async append after mutation | Append-only once written, but write is fire-and-forget and not coupled to success. Absence is possible; “every mutation audited” outruns implementation guarantee. |
| Stored reusable pattern/lesson | `pattern` or `lesson-learned` | Role-specific knowledge admission, ideally after cross-work applicability check | Must be retrieved by future relevant tasks and corrected/deprecated when stale. Feature-local notes need not become shared lessons. |

The common Record envelope therefore needs at least: stable id, category/schema version, author/source,
authority, created time, content digest/version, status/currentness, admission procedure/verdict, evidence
references, scope, and supersession/lifecycle. A category is not a cosmetic label: it selects admission,
retrieval, and lifecycle rules. Unimatrix category extensibility fits this result; no new category is
recommended or created by W2.

## 8. Direction-change replay — anti-forgery policy to value-opaque mechanism

1. **Starting direction:** proposed Mission combined in-place tag mutation with protected-tag hygiene and
   an anti-forgery outcome. Planned Units included config threading, allow-listing, trust/evidence policy,
   cadence control, and mechanism work (preserved indirectly in the 2026-07-06 scope review and deferred
   ADRs).
2. **Signal:** product reviewer emitted a `finding`/`surprise`: identity controls were inert in the OSS
   single-principal setting; without op-level evidence binding the headline “cannot be forged” claim was
   false, while the config surface was over-large (Issue #928 comment, 2026-07-06).
3. **Decision authority:** human owner selected the alternative the review had named—consciously reframe
   the promise—and reduced scope to mechanism only (Issue/SCOPE, “scope reduced by human 2026-07-07”).
4. **Directive propagation:** current SCOPE and Issue explicitly prohibit `protected_tags`, validator,
   config, `min_trust_level`, identity enforcement, evidence enforcement, and cadence implementation.
5. **Stopped Units:** protected-tag evaluator; five-site per-slug config; vocabulary/allow-list;
   `single_value` policy; trust elevation; anti-self-attestation; cadence; skill-consumer switch and
   evidence coupling. ADRs 003/005/006/007 remain durable but marked deferred.
6. **Continued/reformed Units:** direct `entry_tags` primitives; client-supplied atomic replace; complete
   generic audit schema; `Capability::Write` gate location; rate/op count; quarantine refusal; comment-only
   retrofit seams; reduced spec/risk/brief/test plan.
7. **Admission gate:** design artifacts were regenerated, alignment reported clean against reduced scope,
   and later gates explicitly checked absence of deferred surface.
8. **Durable residue:** current Issue/SCOPE; deferred ADRs; the initial product-review comment; a stale
   pre-reduction vision report; synthesizer note identifying the stale knowledge entry. This residue is
   valuable history but dangerous if Record currentness is omitted.
9. **Smallest safe resume point:** open a new Mission for `protected_tags`; start from the human-reduced
   boundary and deferred ADRs as hypotheses, revalidate them against current code/identity model, and do
   not reopen or mutate the completed mechanism Mission. The first gate must restate the enforceable
   outcome and custody of evidence/identity inputs.

The path is understandable with `adapt`, but it is not deterministic from vocabulary alone. Determinism
came from the binding SCOPE/non-goals plus gates that checked absence. A generic stop/resume protocol must
name decision authority, affected Units, baseline version, cancellation status, durable residue, and
resume preconditions.

## 9. False-success replay — authorization/audit structure mistaken for anti-forgery

1. **Tempting claim:** `context_tag` plus trust/config/audit structure could make trust-bearing tags
   unforgeable or poison-resistant.
2. **Disconfirming evidence:** the product scope review identified that OSS identity controls collapsed to
   one principal and that `agent_id` was self-declared; only an evidence predicate could provide live
   anti-forgery teeth. The later code path is value-opaque and checks only `Capability::Write`; PR review
   confirms arbitrary values are intentionally allowed and poison resistance is deferred.
3. **Detection/classification:** scope/product review treated the promise as an overclaim (`finding` plus
   `surprise`), not as demonstrated behavior. The human reduced the outcome rather than accepting a
   structural proxy.
4. **Independent admission rules:** reduced SCOPE prohibited the claim; design/gate 3a checked plan
   fidelity; tests demonstrated only enumerated mechanism ACs; security/product PR review bounded the
   verdict; human/forge merge admitted the code, not the deferred policy.
5. **What could still falsely succeed:** audit was called the “primary control,” yet the implementation
   commits the mutation before spawning a best-effort audit task whose result is discarded. Unit tests
   demonstrate audit records under the tested environment, but not atomic “mutation implies audit.” A
   report claiming guaranteed accountability would therefore be false success even though AC-04 tests
   passed. Also, self-declared `agent_id` supports reconstruction, not identity attestation.
6. **Prevented organizational claim:** final Issue/PR explicitly say mechanism-only, not access control,
   no evidence enforcement, no protected tags, and no capability movement. PR review repeats that no
   capability should flip to `proven`.
7. **Durable residue:** review comments, reduced scope/non-goals, deferred ADRs, known audit gap, test and
   merge Records.
8. **Safe resume:** a later anti-forgery Mission must independently prove externally custodied identity or
   evidence enforcement and couple claimed guarantees to an admission gate. Reusing `vnc-045` test PASS or
   merge as anti-forgery evidence is prohibited.

This replay supports the candidate false-success condition: an actor-authored claim did not bypass the
domain admission rule. It also shows that a review finding can prevent overclaim without itself being an
observation.

## 10. `lesson` alternatives

| Reading | Case evidence | Behavioral/admission/retrieval consequence | W2 ruling |
|---|---|---|---|
| Signal | Gate-3a rework, scope reduction, audit-review warning, implementation test-race note all communicated guidance | If `lesson` is a signal, it must route reusable guidance beyond the local mission. In this case the contemporaneous messages were better typed `exception`, `finding`, `decision`, or `directive`; “lesson” adds no routing precision. | **Reject as primary signal class.** Allow `lesson` as significance/topic metadata only if useful. |
| Record category | Agent reports say reusable rollback-injection and fire-and-forget audit-readback patterns were stored; other agents deliberately stored nothing novel | A lesson category earns distinct admission when guidance is reusable, actionable, non-ADR process/technique knowledge; retrieval should trigger on similar tasks; correction/deprecation handles stale environment advice. | **Retain as plausible distinct category**, subject to evidence that category-specific retrieval/admission differs from `pattern`. |
| Derived construct | Human scope reduction derives “do not overstate defensive structure”; gate failure derives “extract non-constructible handler logic into seam functions”; async audit race derives content-based matching guidance | Requires source events/findings, a transformation into generalized guidance, reviewer/curator admission, and a reuse target. Keeps learning first-class without misclassifying every correction as a lesson. | **Retain. Strongest common-layer reading.** |
| Multiple roles | A derived lesson Record can later be communicated between programs | Separates durable semantics from transport: Record category/derived content is carried by an ordinary `finding`/`directive` signal or a generic Record reference. | **Retain conditionally.** Multiple roles mean derived + Record, not an independent signal primitive. |
| No primitive | All material feature-local corrections remain represented by existing records/signals | Avoids vocabulary inflation, but shared continual process improvement becomes implicit if no admission/retrieval object distinguishes reusable guidance. | **Reject for this case** unless `pattern` is formally generalized to cover lessons with identical behavior. |

The crucial distinction is locality. The gate-3a correction is not automatically a lesson; its durable
gate and corrected plan are sufficient for the Mission. It becomes a lesson only after deriving reusable
guidance and admitting it for future retrieval. Environmental warnings (pre-existing CVEs and clippy
lints) were explicitly *not* stored as lessons because they were transient facts or maintenance work, not
a demonstrated cross-work technique. That negative evidence supports an admission rule.

## 11. Residue and strain ledger

| ID | Native concept/event | Mapping | Severity | Exact evidence |
|---|---|---|---|---|
| RS-01 | Product capability vs actor capability | `Capability` overload | material | Issue #928 product reviews; SCOPE says no capability completed; specialist reports describe role capabilities implicitly. |
| RS-02 | Semantic/human gates | Derived `gate` definition says deterministic condition | material | Issue scope/design/PR reviews; `reports/gate-3a-report.md`; human scope reduction. Verdict evaluation was not purely deterministic. |
| RS-03 | Reject/hold/rework/approve/merge transitions | Eight verbs require repeated subtyping/prose | material | Gate 3a rework history; PR #929 merge metadata. |
| RS-04 | One signal with epistemic kind plus significance | Signal classes overlap (`finding` + `surprise`, `decision` + `directive`) | moderate | 2026-07-06 scope review and 2026-07-07 reduction. |
| RS-05 | Durable does not mean current | `Record` needs supersession/currentness | material | Deferred ADRs 003/005/006/007; stale `agents/vnc-045-vision-guardian-report.md`; synthesizer reconciliation note. |
| RS-06 | Issue body mutation obscures prior state | Record envelope needs version/source semantics | material | Issue #928 current body versus its earlier scope-review comment describing now-removed controls. |
| RS-07 | Audit row may be absent after successful mutation | Record/admission cannot assume effect coupling | material | `crates/unimatrix-server/src/services/store_tag.rs` at merge; Issue design review; PR security/product reviews. |
| RS-08 | Reported mechanical output vs fresh observation | Observation provenance is layered | material | `testing/RISK-COVERAGE-REPORT.md` reports 6,961/32; raw original logs are not in alphabet and W2 did not rerun tests. |
| RS-09 | A0 deterministic service has powerful effect authority | Autonomy tier alone is unsafe | clean discrimination | Handler/service/store implementation at `a63d45f0`/`74bc1fd4`/`b68c2c43`; Write gate and DB mutation. |
| RS-10 | A0 reviewer can block through workflow while causing no direct effect | Decision latitude vs institutional consequence | moderate | Gate 3a rework; validator report. The process, not reviewer credentials, supplies consequence. |
| RS-11 | Resource ceilings absent | Envelope mapping partly reconstructed, not historical | moderate | SCOPE and agent reports provide path/scope bounds but no explicit spend/concurrency ceilings. |
| RS-12 | A3/A4 unused | Tier ladder not fully tested | insufficient evidence | Entire S alphabet. |
| RS-13 | Collective boundary/authority root inferred | `Collective` weakly instantiated | moderate | Human direction and forge merge show authority, but no explicit Collective Record. |
| RS-14 | Commit/merge are both Records and effects | `Record`/`execute` require effect semantics | moderate | PR #929 commits and merge `37c7b09a`. |
| RS-15 | Lesson vs pattern category | Possible semantic duplication | unresolved | Store/service agent stewardship entries #5612/#5613 named patterns; current garage supports `lesson-learned`. Behavior comparison not present in case. |
| RS-16 | False-success avoided by rhetoric/scope plus gates, not runtime anti-forgery | Vocabulary must not imply enforcement | material | SCOPE Non-Goals 2/4/9; PR #929 product review; handler value opacity. |

Three or more material strains exist (RS-01, RS-02, RS-03, RS-05, RS-06, RS-07, RS-08, RS-16).
Under the hypothesis's own falsifier, H1 in its literal current form requires revision for this domain.
The common-envelope idea survives; the claim that the proposed elements need no common-layer subtype or
exception semantics does not.

## 12. Candidate coverage status

### Nouns

All nine nouns received case evidence. Clean/usable: Program, Mission, Unit, Actor, Envelope, Signal,
Record (with category semantics). Revise: Collective needs explicit boundary/authority-root Record;
Capability needs disambiguation between organizational ability and product behavior; Record needs
currentness/admission/effect provenance.

### Verbs

All eight verbs received case evidence. Revise `observe` to mechanically captured fact only. Revise
`execute` and `adapt` with effect/authority/baseline subtypes. The union lacks compact transition semantics
for hold/reject, correct, approve, defer, commit, and merge.

### Autonomy tiers

A0, A1, A2, and A5 are evidenced. A3 and A4 are unused/insufficient. Equal A0 tiers cover reviewers,
test runners, forge, and runtime services with radically different effect authority; the explicit Envelope
successfully preserves most differences. This supports axis separation and rejects tier-as-permission.

### Signal classes

All eight classes are evidenced, but `surprise` overlaps epistemic classes and `directive` overlaps an
authoritative `decision`. Preserve them only through orthogonal fields or explicit multi-class semantics.
No route required global local-context sharing: specialists handed off scoped Records; only exceptions,
findings, decisions, and directives propagated.

### Record semantics and lesson

Record-as-envelope survives only with category-specific schema, admission, retrieval, lifecycle,
currentness, and provenance. `lesson` is strongest as a derived reusable-guidance construct which may be
admitted to a distinct `lesson-learned` category and later transported via ordinary signals. W2 rejects
`lesson` as a standalone mutually exclusive signal class.

## 13. Gaps, surprises, and falsifiers

- **Gap:** the exact human scope-reduction utterance and original Issue body are not separately preserved;
  the reconstruction triangulates the current reduced body/SCOPE with the earlier scope-review comment.
- **Gap:** raw historical test logs are not in S01–S08 and tests were not rerun. Numeric test results are
  reported historical observations, not W2 demonstrations.
- **Gap:** no explicit resource budget, concurrency ceiling, A3 actor, or A4 actor appears.
- **Surprise:** a stale pre-reduction vision report remained beside the corrected corpus. A Record model
  without currentness/supersession would actively mislead future actors.
- **Surprise:** “audit is primary control” coexists with mutation-first, fire-and-forget audit whose error
  is discarded. The complete audit schema is retrofit-hard and tested, but delivery is not guaranteed.
- **Present falsifier:** at least three material concepts require prose/subtypes beyond the common terms.
- **Present falsifier:** the proposed deterministic-gate derivation does not represent semantic/human gates.
- **Absent in this case:** autonomy, authority, and evidence did not collapse; they produced distinct
  answers repeatedly.
- **Absent in this case:** no actor-authored report alone admitted the anti-forgery claim or moved a grade.
- **Unknown:** whether the vocabulary compresses the union of research and software terms; W3 must count
  both completed maps.
- **Unknown:** universal portability beyond two owner-operated repositories/workflows.

## 14. Citations

- type: product · ref: https://github.com/dug-21/unimatrix/issues/928 · title: “vnc-045: context_tag — in-place tag mutation (mechanism only; protected_tags deferred)” · org: dug-21 · year: 2026
- type: repo · ref: https://github.com/dug-21/unimatrix/pull/929 · title: “[vnc-045] context_tag — in-place tag-mutate MCP op (mechanism)” · org: dug-21 · year: 2026
- type: repo · ref: https://github.com/dug-21/unimatrix/commit/37c7b09aa0db6ba16f5f95dadd24c58adb4e6e2b · title: “vnc-045 merge commit” · org: dug-21 · year: 2026
- type: docs · ref: product/features/vnc-045/SCOPE.md · title: “vnc-045 — context_tag: Domain-Agnostic In-Place Tag Mutation (mechanism only)” · org: Unimatrix · year: 2026
- type: docs · ref: product/features/vnc-045/architecture/ARCHITECTURE.md · title: “vnc-045 architecture” · org: Unimatrix · year: 2026
- type: docs · ref: product/features/vnc-045/specification/SPECIFICATION.md · title: “vnc-045 specification” · org: Unimatrix · year: 2026
- type: docs · ref: product/features/vnc-045/testing/RISK-COVERAGE-REPORT.md · title: “Risk Coverage Report: vnc-045” · org: Unimatrix · year: 2026

## W2 done call

S01–S08 are all `used`; no silent alphabet expansion occurred. Every candidate noun, verb, autonomy tier,
signal class, Record semantic, and `lesson` reading has a ruling. Material actors/services have autonomy
and envelope rulings; consequential communication and durable artifact classes are mapped; both required
replays identify authority, stopped/continued Units, admission, residue, and safe resume. Coverage is
complete for W2 subject to the explicitly recorded historical-source gaps above.
