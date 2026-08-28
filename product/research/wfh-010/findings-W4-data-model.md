# wfh-010 W4 — Common ontology/data-model specification

**Role:** `factory-architect` (independent of W1–W3)  
**Status:** claimed, directional specification; not ratified or implemented  
**Evidence base:** `SCOPE.md` including the 2026-08-28 Extension; W1–W3; the original coverage audit;
the target concept and vocabulary proposal/run packet; the canonical `uni-capability` contract.  
**Boundary:** this specifies a conceptual model only. It does not select storage, define product
architecture, change Unimatrix, synthesize vocabulary v2, recommend a build, or move any grade.

## 1. Objective and headline ruling

Define the smallest typed organizational envelope that preserves the two histories' identity, work,
communication, durable memory, proof/admission, effect, interruption, and learning distinctions without
turning program-owned semantics into free text.

The corrected **Capability** ruling is **retain**, with a narrowed canonical meaning:

> A Capability is an observable behavior required by a Goal and delivered by Features and/or enabled by
> Technologies. A Capability may be recursively composed and scoped at collective, program, mission, or
> team level; level changes scope and composition, never meaning. An Actor's competence is a
> Qualification/Skill, not a Capability.

This removes, rather than hides, W3's alleged conflict. In W1 the proposed capability target was absent
and unadvanced, not a contrary semantic. In W2, `tag mutation` and `audit production` are Capabilities;
`architecture`, `implementation`, `testing`, and `security review` when attributed to Actors are
Qualifications. “Organizational ability” is a composite Capability whose scope is an organization, not a
third kind. No `capability.kind = actor|product|organization` discriminator is warranted.

The minimal model is five focal constructs plus supporting entities and relations:

- **Capability** — durable entity describing required observable behavior.
- **Unit** — durable work identity; attempts and transitions are related entities/events, not versions of
  the work's meaning.
- **Record** — durable entity envelope whose category owns admission, retrieval, and lifecycle semantics.
- **Signal** — communication event; it may reference a Record but is not made durable by doing so.
- **Admission Contract** — durable, versioned policy entity binding an identified subject/evidence set,
  assessor authority and independence requirements, decision procedure/bar, possible verdicts,
  consequences, and required durable outcome.

The Admission Contract survives its test as a first-class construct because both domains repeatedly need
the same join and because decomposition into a decision Signal plus Record metadata leaves authority,
independence, subject baseline, bar, and consequence scattered. It does **not** absorb evidence, verdict,
effect, or Record existence: an application of the contract creates a distinct Admission Assessment and
Admission Outcome. The evidence is only two cases, so this is a claimed modeling result, not proof of
universal portability.

## 2. Provenance and enforcement notation

Every normative clause below has an identifier and source class:

- **D (derived):** directly required by W1–W3 or the canonical capability contract.
- **A (adapted):** an existing contract is retained with a stated correction.
- **O (authored):** a modeling judgment introduced to resolve the evidence.

“Enforcement” names the conceptual checker that an implementation would need. **None of these common-model
checks exists today as a cross-domain enforcement point.** Native repository workflows, git/forge,
Unimatrix operations, tests, and human gates enforce fragments only. Therefore every table distinguishes
`future checker` from `today`; no clause is represented as operational control.

## 3. Identity, type, scope, version, state, category, and relation

These dimensions are orthogonal:

| Dimension | Meaning | Must not be used as |
|---|---|---|
| identity | which continuing thing this is | content hash, name, current version, category |
| type | stable common semantic shape | organizational level, workflow state, arbitrary program label |
| scope | boundary in which the instance applies | a type discriminator |
| version | immutable revision of one identity's definition/content | work attempt or lifecycle state |
| state | current position in a lifecycle | version or evidence grade |
| category | behavior-bearing Record extension selecting schema/admission/retrieval/lifecycle | cosmetic tag or universal closed taxonomy |
| relation | typed connection between independently identified things | duplicated prose field |

**C01 (D, W3 X03/X05/X06/X16):** every durable entity has an opaque stable identity distinct from its
human name and immutable version identifiers. Supersession preserves the stable identity or explicitly
links predecessor and successor identities; it never silently overwrites audit history. **Future
checker:** schema validator plus append-only version store outside ordinary subject mutation. **Today:**
git/Unimatrix partly preserve versions, but Issue-body mutation demonstrates no uniform enforcement.

**C02 (O):** `scope` is a reference to an organizational boundary plus optional Goal/Mission/Team
boundary; it is not embedded in the type name. **Future checker:** referential-integrity validator.
**Today:** none cross-domain.

**C03 (D, W2 RS-05/06; W3 X06):** lifecycle state, evidence/grade, and currentness are separate. A durable
Record may be active but non-current, current but unadmitted, or admitted at a directional rather than
behavioral altitude. **Future checker:** category lifecycle plus projection validator. **Today:** native
systems differ; the stale vision report is a counterexample.

### 3.1 Focal identity model

| Construct | Ontological form | Durable identity | Version/supersession | Type vs scope/category |
|---|---|---|---|---|
| Capability | entity | required | definition revisions retain identity when behavior is unchanged; semantic replacement creates a new identity and `supersedes` relation | one common type; `scope` carries collective/program/mission/team; composition carries level. `functional|nfr` and `threshold|curve` remain orthogonal classifications, not level meanings |
| Unit | entity | required for attributable work | Unit definition/baseline may version; retry/rework creates an Attempt related to the same Unit unless intended outcome changes | `unit_kind` is a typed extension point; workflow owns states and transitions; scope locates the work |
| Record | entity | required | immutable RecordVersion chain; correction/supersession/currentness explicit | one envelope; `category` selects category-owned schema, admission, retrieval and lifecycle |
| Signal | event/value | event id required when consequential or acknowledgement/replay matters; ephemeral routine Signals may be values without durable identity | Signals are immutable events; correction is a new Signal referencing the prior event, not a version mutation | orthogonal epistemic, action, significance, authority, route and carrier fields; no single flat class |
| Admission Contract | entity | required | immutable contract versions; every assessment pins exactly one version and subject baseline | one common contract type; program/category/workflow supplies typed bar/procedure and allowed verdict/consequence extensions |

**C04 (D, W1/W2 replay requirements):** a Unit's stable identity survives rework, while each execution is
an Attempt with its own identity, baseline, actor assignment, envelope, timestamps, outputs and
disposition. A changed intended outcome is a new Unit related by `replaces` or `derived-from`.
**Future checker:** workflow engine. **Today:** histories reconstruct this from commits/reports; no common
checker.

**C05 (D, W3 Signal ruling):** a Signal is an event, not a durable noun equivalent to Record. A durable
carrier does not merge their identities. **Future checker:** messaging schema/routing layer. **Today:**
none common.

**C06 (A, canonical `uni-capability`):** Capability delivery/evidence state is not content identity and
does not become proven because a Feature exists or merges. The canonical firewall remains: behavioral
evidence must clear the stated behavior. **Adaptation:** the existing goal-to-capability meaning is
generalized by scope and recursive composition, while actor competence is explicitly excluded. **Future
checker:** capability gate plus evidence verifier outside the delivering Actor's custody. **Today:**
Unimatrix capability procedure checks part of this; this W4 performs no grade operation.

## 4. Minimal definitions and invariants

### 4.1 Capability — **retain**

Required fields: `capability_id`, `version_id`, `name`, `observable_behavior`, `scope`, `goal_refs`,
`classification`, `done_when`, `state/grade`, `provenance`, `current_version`.

**CAP-1 (A, owner rule + uni-capability):** every Capability states behavior observable at its declared
scope and at least one Goal that requires or is advanced by it. **Checker:** capability-schema and goal-map
validator; today only the existing capability procedure, not a cross-level checker.

**CAP-2 (O):** recursive composition is allowed at every level: a collective-scoped Capability may be
composed of program-scoped Capabilities; program of mission; mission of team; composition may also skip a
level. Every child remains independently observable. A parent is not satisfied merely because children
exist; its own `done_when` governs. **Checker:** DAG and evidence-rollup validator; today none.

**CAP-3 (D, corrected X02/RS-01):** Actor competence uses Qualification/Skill. `Actor has Qualification`
and `Role requires Qualification`; neither relation implies that a Goal-required Capability exists or is
proven. **Checker:** ontology relation validator; today none.

**CAP-4 (A, canonical contract):** Feature `delivers` Capability; Technology `enables` Capability. Neither
edge proves the Capability. Goal `requires` Capability is mandatory for claim-floor membership;
`is-advanced-by` may express contributory/non-floor relation. **Checker:** graph relation and firewall
gate; today relation vocabulary differs and feature/technology references are partly fields.

Allowed Capability relations and cardinalities:

| Relation | Cardinality | Constraint |
|---|---:|---|
| Goal `requires` Capability | Goal 1..* ↔ Capability 0..* | a Capability may serve multiple Goals; a deliverable Goal has at least one required Capability |
| Goal `is-advanced-by` Capability | Goal 0..* ↔ Capability 0..* | contribution does not imply claim-floor requirement |
| Capability `composed-of` Capability | 0..* ↔ 0..* | acyclic within a versioned composition view; no semantic change by level |
| Capability `prerequisite-of` Capability | 0..* ↔ 0..* | directed acyclic dependency for the evaluated baseline; prerequisite source direction retained |
| Feature `delivers` Capability | Feature 0..* ↔ Capability 0..* | structural delivery only; evidence separate |
| Technology `enables` Capability | Technology 0..* ↔ Capability 0..* | candidate/proven technology grade does not transfer automatically |
| Actor `has` Qualification | Actor 0..* ↔ Qualification 0..* | competence claim has its own evidence/currentness |
| Role `requires` Qualification | Role 0..* ↔ Qualification 0..* | matching does not grant effect authority |

### 4.2 Unit — **revise**

Required common fields: `unit_id`, `unit_kind`, `intended_outcome`, `scope`, `workflow_ref`,
`dependency_refs`, `input_refs`, `output_refs`, `current_state`, `baseline_ref`, `current_attempt_ref`,
`admission_contract_refs`, and `provenance`. Workflow extensions own the state and transition vocabulary.

**UNIT-1 (D, X03/X10):** Unit kind, dependencies, state, baseline and transition consequence are typed;
native `hold|reject|rework|approve|defer|merge` remain workflow-owned values, not universal verbs.
**Checker:** workflow schema/transition engine; today native protocols and forge enforce fragments.

**UNIT-2 (D, both replays):** interruption creates an explicit disposition for every affected Unit:
`continue`, `hold`, `cancel`, `rework`, or a workflow extension; safe resume identifies baseline,
preconditions, unresolved residue and next admissible transition. **Checker:** workflow engine outside the
worker's write custody; today reconstructed, not generically enforced.

**UNIT-3 (O):** dependency is a Unit-to-Unit relation; Attempt is not a Unit subtype. One Unit has zero or
more Attempts and at most one current active Attempt. **Checker:** identity/cardinality validator; today
none common.

### 4.3 Record — **revise**

Required common fields: `record_id`, `version_id`, `category`, `category_schema_version`, `scope`,
`author/source`, `created_at`, `content_digest`, `provenance_refs`, `epistemic/evidence_kind`,
`evidence_altitude`, `admission_outcome_refs`, `lifecycle_state`, `currentness`, `supersedes_refs`,
`effect_receipt_refs`, and explicit `missing/unavailable` references where expected material is absent.

**REC-1 (D, X06/X16):** Record existence, admission, truth, evidence grade, currentness and effect
occurrence are independent facts. **Checker:** category validator plus admission/effect reconciliation;
today none common.

**REC-2 (D, W3 §8):** category is an extensible behavior-bearing type selector. Each category owns its
schema extension, admission eligibility, retrieval behavior, lifecycle and correction rules. The common
model does not enumerate a closed category list. **Checker:** Unimatrix/category configuration validator;
today Unimatrix is flexible but no W4 configuration change is authorized.

**REC-3 (D, RS-07/14):** an effect-bearing commit, merge or mutation and a Record describing it are
separate. An Effect Receipt attests only the bounded effect it identifies and declares coupling
`atomic|ordered-best-effort|reported|unknown`. **Checker:** effect-plane receipt issuer outside requesting
Actor custody; today git/forge supply receipts for some repository effects, while `vnc-045` audit is
best-effort and may be absent.

### 4.4 Signal — **revise**

Required fields for a consequential Signal: `signal_id`, `occurred_at`, `sender`, `route/recipients`,
`scope/topic`, `carrier = inline|record-ref`, `payload_or_record_refs`, `epistemic_kind = observation|claim|reviewed-finding`,
optional `action_kind = request|decision|directive`, `significance = routine|exception|surprise`,
`authority_ref`, `ack_requirement`, and `caused_by/supersedes_signal_refs`.

**SIG-1 (D, X05):** epistemic kind, speech/action, significance, authority, route and carrier are
orthogonal; `finding+surprise` and `decision+directive` are valid combinations, not competing classes.
**Checker:** signal-schema validator; today none common.

**SIG-2 (D, X08):** `observation` requires direct mechanical capture provenance. An authored report of
historical test output is a Claim whose referenced Record may describe a `reported-observation`; it is not
upgraded to direct observation. **Checker:** admission assessor verifies capture custody/provenance; today
case reviewers enforce rhetorically, not universally.

**SIG-3 (D):** a Signal may route a Record reference, but storage of a message does not make Signal and
Record one object. **Checker:** reference/type validator; today none common.

### 4.5 Admission Contract — **retain as newly modeled construct**

Required fields: `contract_id`, `version_id`, `scope`, `subject_type`, `subject_identity_rule`,
`baseline_rule`, `eligible_evidence_kinds`, `evidence_missingness_policy`, `assessor_role/authority`,
`independence_and_custody_predicate`, `decision_procedure`, `admission_bar`, `allowed_verdicts`,
`verdict_consequences`, `required_outcome_record_category`, `expiry/recheck_rule`, and `provenance`.

Application entities/events:

- **Admission Assessment:** one identified contract version applied by one or more Assessors to exactly
  one identified subject baseline with an evidence set.
- **Admission Outcome:** exactly one terminal verdict for an assessment attempt, with rationale,
  missingness, consequence disposition and durable Record reference. Rework creates another assessment
  attempt; it does not erase the rejection.

**ADM-1 (D, X09/X13/X14):** the assessor, input/evidence custodian and governed subject are explicit.
Required independence is a relation/predicate, not an Actor label. A contract fails closed when required
independence or evidence cannot be established. **Checker:** admission service/gate outside governed Actor
custody; today native auditors/humans supply partial independence, with no common service.

**ADM-2 (D, both cases):** verdict and consequence are distinct. An assessor can have no credentials yet
produce a blocking outcome because a workflow maps its verdict to `hold/rework`; a forge can cause merge
without judging behavioral truth. **Checker:** workflow transition engine plus effect plane; today native
workflow/forge.

**ADM-3 (D, RS-08/X16):** unavailable evidence and reported observations are explicit eligible/ineligible
states under the contract, never inferred as PASS. **Checker:** evidence-set validator; today procedural.

**ADM-4 (O):** Record admission and subject admission are different contracts when their consequences
differ. For example, admitting a test report to durable history does not admit the software behavior it
claims, and merging source does not admit an anti-forgery claim. **Checker:** contract-type and consequence
validator; today separate gates partly achieve this.

#### Admission Contract test against alternatives

| Test | Decomposed Signal + Record metadata | First-class Admission Contract | Ruling |
|---|---|---|---|
| `wfh-008` coverage rework | can reconstruct only by repeating assessor, independence, alphabet, bar, verdict and blocking consequence in prose | one versioned contract binds frozen alphabet/evidence, independent auditor, PASS/REWORKABLE/SCOPE-FAIL and phase consequence; each round is an assessment | contract removes recurrent prose while preserving native coverage semantics |
| `wfh-008` relevance/human acceptance | a decision Signal alone cannot distinguish advisory relevance from authoritative close | separate contracts preserve advisory goal-owner outcome versus human decision consequence | contract prevents decision-authority collapse |
| `vnc-045` gate 3a | verdict Record exists, but without contract the frozen target, criteria, rework consequence and assessor relation are scattered | assessment pins pseudocode baseline, semantic bar and REWORKABLE consequence | contract preserves human/semantic gate; procedure need not be deterministic |
| `vnc-045` tests and merge | generic verify/Record risks making green report or merge equal correctness | distinct behavior-admission and repository-effect contracts keep tests, review and forge consequence separate | contract prevents proof/effect collapse |
| audit-row absence | a Record-only model mistakes absence for no effect or assumes atomic coupling | subject Effect Receipt plus missingness/coupling policy records mutation-success/audit-unknown | contract exposes rather than repairs the runtime gap |

**Strong counter-result:** Admission Contract does not make admission deterministic or trustworthy by
itself. A human-semantic bar remains judgment; a contract under the governed party's custody is merely
documentation. The construct earns first-class identity because it makes those facts inspectable and
reusable, not because it supplies enforcement.

## 5. Relationship and cardinality model

| Source — relation → target | Cardinality | Required semantics |
|---|---:|---|
| Goal — requires/is-advanced-by → Capability | each Goal 1..* required; both many-to-many | requirement vs contribution distinct |
| Capability — composed-of/prerequisite-of → Capability | many-to-many DAG per baseline | composition vs execution dependency distinct |
| Feature — delivers → Capability | many-to-many | no automatic grade transfer |
| Technology — enables → Capability | many-to-many | enablement evidence/grade separate |
| Goal/Mission/Team — scopes → Unit | container 0..*; Unit exactly 1 primary scope | scope does not change Unit type |
| Unit — has → Attempt | Unit 0..*; Attempt exactly 1 Unit | rework lineage and baseline explicit |
| Attempt — assigned-to → Actor | Attempt 1..* Actors; Actor 0..* Attempts | role/qualification and authority separate |
| Attempt — governed-by → Envelope | Attempt 1..* envelope versions | grant source, custodian, expiry and effect classes typed |
| Unit — depends-on → Unit | 0..* DAG per workflow baseline | workflow determines readiness |
| Unit/Attempt — consumes/produces → Record | 0..* | output existence does not imply admission |
| Signal — sent-by/to → Actor/Role/route | one sender, 1..* targets or topic | authority is referenced, not inferred from sender name |
| Signal — carries → Record | 0..* | carrier relation only |
| RecordVersion — derived-from/cites/supersedes → RecordVersion | 0..* | provenance and currentness explicit |
| Evidence Item — supports/challenges → Claim/Capability/Assessment | 0..* | evidence kind, custody and baseline pinned |
| Admission Contract — governs → subject type/scope | 1..* | versioned policy, not verdict |
| Assessment — applies → Admission ContractVersion | exactly 1 | immutable pin |
| Assessment — evaluates → subject baseline | exactly 1 | no moving target |
| Assessment — uses → Evidence Item | 0..* subject to contract | missingness represented |
| Assessment — performed-by → Actor/Role | 1..* | independence relation checked |
| Assessment — yields → Admission Outcome | one terminal per attempt | rework is a new attempt |
| Admission Outcome — causes → Unit transition/Decision/Effect request | 0..* | verdict never silently equals consequence |
| Effect Request — performed/refused-by → Effect Plane | exactly 1 terminal disposition | requester and custodian distinct where required |
| Effect Plane — issues → Effect Receipt | 0..1 per request | absence/unknown explicit; receipt states coupling |
| Actor — has → Qualification; Role — requires → Qualification | many-to-many | qualification does not grant authority |

**REL-1 (D, X04/X07/X11/X13):** Envelope must reference typed effect/resource grants, grantor,
custodian/enforcer, scope, baseline/expiry and escalation. It expresses intended authority; only an
external Effect Plane refusal/receipt demonstrates enforcement. **Checker:** policy decision/enforcement
point unreachable by the governed Actor. **Today:** fragmented; no common enforcement.

## 6. Cross-case concrete representation

### 6.1 `wfh-008` research claim admission and rework

```yaml
unit: coverage-audit
unit_kind: research.workflow.coverage-audit
attempts:
  - attempt: 1
    baseline: R01-R08@round-1
    outcome: REWORKABLE
    disposition: hold-synthesis; reopen-owned-findings
  - attempt: 2
    baseline: R01-R08@round-2
    outcome: REWORKABLE
  - attempt: 3
    baseline: R01-R08@final
    outcome: PASS
admission_contract:
  subject: source-bounded directional coverage
  evidence: frozen alphabet + findings + deterministic sweep outputs
  assessor: independent coverage auditor
  bar: no material silent omission; explicit gaps retained
  consequence: PASS permits next phase; REWORKABLE holds and routes bounded repair
records:
  categories: [research-finding, coverage-audit, position, relevance-review]
  altitude: directional/claimed-at-most
  currentness: correction and rejection lineage retained
effect_receipts:
  repository_commits: git object ids
  graph_writes: separate curator effects; no grade movement
```

The Records preserve claims and admitted organizational position; they do not demonstrate that the
world claims are true. Safe resume follows the latest admitted baseline plus retained gaps and rejection
history, not every local thought.

### 6.2 `vnc-045` demonstrated behavior, scope correction and repository effect

```yaml
mission_baseline:
  old: anti-forgery-plus-mechanism
  current: value-opaque-mechanism-only
direction_change:
  signal: {epistemic_kind: reviewed-finding, significance: surprise}
  decision_authority: human owner
  stopped_units: [protected-tag-policy, trust/evidence-binding, config/cadence]
  continued_units: [tag-primitives, service, handler, bounded-tests]
  residue: [deferred-ADRs, stale-vision-report, correction-record]
unit: implementation-and-validation
attempt_lineage:
  gate-3a-1: REWORKABLE
  gate-3a-2: PASS
admission_contracts:
  - subject: bounded mechanism behavior
    evidence: identified tests + reviews at pinned commits
    consequence: eligible-for-publication-review
  - subject: repository ref update
    assessor/enforcer: human/forge
    consequence: merge
records:
  test_report: {epistemic_kind: claim, reports: mechanical-results, raw_logs: unavailable}
  stale_vision_report: {durable: true, current: false}
effects:
  db_mutation: distinct from audit record
  audit: {coupling: ordered-best-effort, receipt_may_be_absent: true}
  merge: {receipt: 37c7b09a, proves: repository-effect, does_not_prove: anti-forgery}
```

The smallest safe resume for anti-forgery is a new Unit/Mission from the reduced baseline and deferred
ADRs as hypotheses. The earlier PASS and merge are ineligible evidence for that Capability.

### 6.3 Conforming and non-conforming examples

**Conforming:** “Goal G requires Capability C: externally custodied refusal of forbidden graph-grade
changes. Technology T enables C; Feature F delivers an enforcement path. Attempt A, governed by Envelope
E, submits a forbidden request. Effect Plane P refuses and issues receipt R. Independent Assessment Q
applies Contract K v2 to R and records PASS.” Identity, behavior, authority, evidence and consequence are
separate.

**Non-conforming:** “Actor X has the graph-writing capability, completed Feature F, wrote a PASS report,
and therefore Capability C is proven.” This confuses Qualification with Capability, Feature delivery with
proof, authored Record with observation, and verdict with externally enforced effect.

## 7. Type-versus-scope and extension boundary

| Construct | Stable common type/fields | Scope/composed variation | Program/category/workflow-owned extension |
|---|---|---|---|
| Capability | observable behavior, Goal relation, done_when, evidence state | organizational level, governed surface, recursive children | domain-specific behavior schema/evidence bar; canonical functional/nfr and threshold/curve classifications remain orthogonal |
| Unit | attributable intended outcome, dependencies, Attempts, baseline | mission/team/program boundary; decomposition | `unit_kind`, states, transitions, gate consequences |
| Record | identity/version/category/provenance/currentness/admission/effect refs | organizational and subject scope | category schema, admission eligibility, retrieval, lifecycle |
| Signal | immutable communication event with orthogonal dimensions | route/topic/recipient scope | action/significance extensions and routing policy, without redefining observation/claim |
| Admission Contract | subject pin, evidence set, authority/independence, bar, verdict set, consequence, outcome durability | governed program/category/workflow and risk scope | procedure, bar, verdict/consequence vocabulary and recheck policy |

No listed extension may weaken the common disclosure/observation distinction, erase custody, treat missing
evidence as success, overwrite lineage, or equate Record/effect/admission.

## 8. Re-adjudication register

| Concept | Ruling | Definition/invariant | Exact unresolved residue |
|---|---|---|---|
| Capability | **retain** | one observable Goal-required behavior; scope/composition changes level, never semantics; Qualifications model Actor competence | W1 instantiated no Capability target; cross-level composition and the revised relations have not been executed |
| Unit | **revise** | durable work identity with typed kind, workflow state, dependencies, baseline and Attempt lineage | common transition vocabulary intentionally absent; generic stop/resume unexecuted |
| Record | **revise** | durable versioned envelope over behavior-bearing extensible categories | category configurations differ; lesson/pattern boundary unresolved; mutable external Records may lack full versions |
| Signal | **revise** | immutable communication event with orthogonal epistemic/action/significance/authority/route/carrier dimensions | acknowledgement and routing policy not exercised as common machinery |
| Admission Contract | **retain, claimed** | durable versioned admission policy; assessment/outcome distinct from evidence, decision, effect and Record existence | only two owner-operated domains; no common enforcement; semantic bars remain judgment; contract custody untested |

### Every alleged Capability conflict re-adjudicated

| Allegation | Corrected usage | Residue after correction | Recommendation |
|---|---|---|---|
| W1 proposed `jurati-arch-002` “capability target” absent | it was a proposed Capability with no durable identity/evidence/state | absence and non-advancement remain; no semantic conflict | no kind/rename |
| W2 architecture/implementation/testing/security-review “capabilities” of Actors | Qualifications required by Roles and held/claimed by Actors | competence evidence/currentness needs modeling, but not Capability semantics | rename those usages to Qualification/Skill |
| W2 tag mutation/audit as product capability | Goal-required observable Capabilities delivered by Features and enabled by Technologies | audit guarantee must be bounded to best-effort behavior; proof remains separate | retain Capability |
| organizational ability at collective/program level | scoped composite Capability, e.g. “the program can independently admit source-bounded research claims” | parent done_when and composition rollup untested | no new kind; use scope/composition |
| team ability | team-scoped Capability only when the behavior is a Goal requirement; member competence remains Qualification | team may be temporary, so scope validity/expiry is needed | no rename unless phrase actually denotes competence |

## 9. Nine-qualifier delta and semantic-compression implication

| W3 recurrent qualifier | Model disposition | Ownership |
|---|---|---|
| unit kind and dependency | typed `Unit.unit_kind`; `depends-on` relation | common field/relation; kind values and transition semantics workflow-owned |
| attempt/baseline | Attempt entity plus immutable baseline reference | common |
| decision authority | Signal/Decision authority reference plus Admission assessor authority | common relation; authority policy program-owned |
| admission bar | versioned Admission Contract | common envelope; bar/procedure category/workflow-owned |
| evidence provenance | Evidence Item/Record provenance, capture kind, custody, missingness | common invariants; eligible kinds contract-owned |
| effect class | typed Effect Request/Receipt and Envelope grant | common structure; effect taxonomy/policy extensible |
| custody/independence | explicit Actor/Effect Plane/Assessor relations and predicate | common invariant; required predicate contract-owned |
| currentness/supersession | RecordVersion chain and independent currentness | common |
| category lifecycle/retrieval | Record category selects behavior | remains category-owned and must not be universalized |

All nine move out of unstructured prose at least at their common boundary. Native proof bars, admission
procedures, transitions, categories, retrieval, lifecycles and consequences remain typed extensions rather
than universal values. Therefore **semantic compression becomes plausible but is not proven**: the model
turns recurrent qualifiers into fields/relations and eliminates the corrected Capability overload, but it
has not been instantiated, measured, or transferred beyond the two histories.

## 10. Residue and contradiction ledger (X01–X16)

| ID | W4 disposition | Surviving residue/falsifier |
|---|---|---|
| X01 | boundary/authority-root references belong to Collective/Program scope and authority relations | exact Collective boundary remains inferred in both cases; unresolved |
| X02 | corrected: Capability means behavior; Actor competence is Qualification; level is scope/composition | W1 absence and unexecuted cross-level composition remain; semantic conflict does not |
| X03 | Unit kind/dependency/state plus Attempt/baseline modeled | workflow transition values and generic resume execution remain native/untested |
| X04 | Envelope includes typed grants, custodian/enforcer, expiry/baseline | historical resource ceilings absent; intended bounds still do not prove enforcement |
| X05 | Signal decomposed into orthogonal dimensions | common routing/ack behavior untested |
| X06 | Record identity/version/category/provenance/admission/currentness/effect refs separated | some mutable historical states/raw sources unavailable; category behavior remains native |
| X07 | execution represented by Attempt plus typed Effect Request/Receipt | common effect taxonomy and external refusal not tested |
| X08 | direct observation vs claim/reporting metadata explicit | original W2 raw logs and W1 telemetry unavailable |
| X09 | verification becomes Assessment applying a typed Contract | semantic judgment remains nondeterministic; no common enforcement |
| X10 | verbs are operations; workflow owns branching transitions | no universal lifecycle claimed; generic stop/resume remains unexecuted |
| X11 | autonomy remains decision latitude only; Envelope/Contract consequence separate | tier semantics beyond observed A0/A1/A2/A5 remain incompletely tested |
| X12 | unchanged | A3 unused; A4 weak/unused; insufficient evidence |
| X13 | independence/custody is explicit relation/predicate | actual external custody is fragmented and untested as a common control |
| X14 | Admission Contract removes repeated join prose | first-class identity is only directionally supported; two-domain portability unknown |
| X15 | `lesson` is derived reusable guidance; distinct Record category remains optional/insufficient | behavioral boundary against `pattern` unresolved |
| X16 | missing/unavailable and reported evidence modeled explicitly | missing historical material stays missing; model cannot reconstruct it |

No residue is closed merely by adding a field. X01, X04, X08, X11–X16 remain live limits; X03, X05–X10
have a coherent proposed representation but remain unimplemented and unvalidated.

## 11. `lesson`, continual improvement, and Record categories

`lesson` does not survive as a Signal type. It **does** survive as a derived construct: source events,
failures, findings or corrections are generalized into actionable guidance with reuse scope, then assessed
for durable admission. Whether the admitted Record category is `lesson-learned`, `pattern`, or another
category remains **insufficient evidence**. Distinct category identity is justified only if admission,
retrieval, reuse measurement, correction or lifecycle behavior differs—not by label preference.

This keeps process improvement first-class: a Unit may consume prior guidance Records; a new outcome may
trigger a lesson-derivation Unit; an Admission Contract determines whether the result enters shared memory;
later reuse outcomes support correction or supersession. It does not create a universal category or imply
that every failure becomes organizational knowledge.

## 12. Strongest objection, exclusions, and owner questions

### Strongest objection that this round cannot answer

The model may be a more disciplined transcription language rather than an organizational substrate. It
names identity, custody, evidence and consequence, but the two cases show those properties only through
different native protocols and human judgment. Until one representation is instantiated and an external
checker rejects a non-conforming case, there is no evidence that Admission Contracts, recursive
Capabilities, or safe-resume lineage reduce operational ambiguity rather than add modeling overhead. This
is unanswerable within a read-only directional round.

### Deliberate exclusions

- No product/service architecture, storage choice, Unimatrix schema/category/configuration change, code,
  workflow mutation, or build recommendation.
- No universal state machine, closed effect taxonomy, closed Record-category taxonomy, generic proof bar,
  or claim that semantic gates are deterministic.
- No vocabulary-v2 synthesis, theme decision, grade movement, `wfh-009` work, or historical-case rerun.
- The newly surfaced idea of a **centralized shared Qualification/Skill catalog with repository-local
  bindings** is recorded only as an untested future Capability hypothesis. This document does not design,
  recommend, select or implement it, and does not use it as evidence.

### Owner questions

1. Should `requires` be the sole claim-floor Goal relation while `is-advanced-by` remains explicitly
   non-floor, or should existing `Advances` remain the storage-level relation with requirement encoded in
   Goal policy?
2. Is a team-scoped behavior worth a durable Capability identity when the team is temporary, or should
   such scope always resolve upward to its Mission?
3. What consequence threshold requires a consequential Signal to receive durable identity and
   acknowledgement rather than remain ephemeral?
4. Should Admission Contract be retained for a later bounded falsification/instantiation test, recognizing
   that this specification establishes no enforcement?
5. What observable behavioral difference would justify separate `lesson-learned` and `pattern` Record
   categories?

## 13. Surprises

- Correcting Actor competence to Qualification removes every observed incompatible Capability meaning;
  no level-specific Capability kind is needed.
- Admission Contract is not a bigger Gate. Its value is separating a reusable policy from each assessment,
  verdict and consequence; this also exposes when a gate has no independent custodian.
- The most dangerous identity error is not duplicate naming but treating currentness as durability. Both
  cases retained useful history that would mislead if projected as current.
- Effect Receipt must represent refusal and missing/unknown coupling, not just successful effects; otherwise
  it launders the exact `vnc-045` audit gap the model is meant to preserve.
- The nine W3 qualifiers fit as typed fields/relations without expanding the common noun list, but that is
  only a plausible route to semantic compression—not evidence that users or agents can operate it reliably.

## W4 done call

All five focal concepts have identity/type/scope/version/state/category/relation rulings; Capability is
re-adjudicated under the binding owner rule; all required relations/cardinalities, nine W3 qualifiers and
X01–X16 residues are accounted for; both proof/admission domains and both interruption lineages remain
distinct. Every behavioral clause names an honest current/future enforcement point. Output remains
claimed/directional and ready only for the supplemental independent audit required by the Scope Extension.

---

## Rework round 1 — 2026-08-28 (D1–D3 only)

**Authority:** targeted correction requested after `reports/gate-coverage-r2.md` ruled `REWORKABLE`.
This append-only section supersedes only the inconsistent D1–D3 clauses identified below. All other W4
claims, residues, exclusions, provenance and enforcement caveats remain unchanged.

### RW1-D1 — Capability is always required by at least one Goal

**Corrected ruling:** Capability remains **retain** and has exactly one meaning:

> A Capability is an observable behavior required by at least one Goal and delivered by Features and/or
> enabled by Technologies. Scope and recursive composition may vary across collective, program, mission
> and team without changing that meaning. Actor competence remains Qualification/Skill.

“Required” is broader than “claim-floor.” A Goal may require threshold Capabilities for its claim-floor
and may also require curve/north-star Capabilities whose bars remain open. `requires` establishes that the
behavior is a Capability for that Goal; claim-floor/north-star is an orthogonal Goal-policy classification.
`is-advanced-by` records a contributory relation only and can never, alone, qualify an object as a
Capability.

**RW-CAP-1 (A, owner rule and canonical `uni-capability`; supersedes CAP-1):** every Capability has one or
more incoming Goal `requires` relations and states observable behavior plus `done_when` at its declared
scope. **Future checker:** capability-schema/goal-map validator. **Today:** the existing capability
procedure partially checks goal association and behavioral proof; no common cross-level checker exists.

**RW-CAP-4 (A, owner rule; supersedes the qualification sentence of CAP-4):** Feature `delivers`
Capability and Technology `enables` Capability remain structural relations and never prove it. Goal
`requires` Capability is mandatory for Capability identity. Goal `is-advanced-by` Capability is optional
and non-qualifying; it may express additional contribution to other Goals. Claim-floor membership is a
separate Goal policy over required Capabilities. **Future checker:** relation/cardinality validator plus
capability firewall. **Today:** no common checker.

Corrected cardinalities:

| Relation | Corrected cardinality | Constraint |
|---|---:|---|
| Goal `requires` Capability | Goal 0..* ↔ Capability **1..*** Goals | every Capability is required by at least one Goal; a Goal may be undecomposed temporarily, but is not deliverable/claimable until required Capabilities exist |
| Goal `is-advanced-by` Capability | Goal 0..* ↔ Capability 0..* | optional contribution only; never establishes Capability identity or claim-floor membership |

**Register reconciliation:** the §8 Capability ruling is narrowed to “one observable behavior required by
at least one Goal.” Its exact residues remain W1's absent instance and unexecuted recursive composition;
there is no surviving semantic conflict and no kind/rename recommendation.

**Owner-question reconciliation:** §12 question 1 is answered for this specification, not left open:
`requires` is the mandatory semantic relation; `is-advanced-by` is optional and non-qualifying. Whether an
implementation reuses storage-level `Advances` with separately validated requirement policy is an
out-of-scope representation choice, but it may not weaken this semantic cardinality.

**Conforming:** Capability C is required by Goal G as a north-star curve behavior and is additionally
`is-advanced-by` Goal H; C is a Capability even though it is not in G's claim-floor.
**Non-conforming:** Technology T helps Goal H and is labelled Capability C solely because H
`is-advanced-by` C; no Goal requires C. C does not satisfy the definition.

### RW1-D2 — one Unit scope-container set; Goal is orthogonal intent

**Authored ruling:** the common organizational `ScopeContainer` set is exactly
`Collective | Program | Mission | Team`. Goal is not a scope container. Goal expresses intent and relates
to Units through `pursued-by`/`advances`, while the Unit's organizational boundary is carried separately by
one primary ScopeContainer. The four container types may nest according to organizational policy; nesting
does not create four Unit meanings.

**RW-UNIT-SCOPE (O; supersedes inconsistent Unit scope rows/phrases in §§3.1, 4.2, 5 and 7):** every Unit
has exactly one primary `scope_container_ref` whose target type is Collective, Program, Mission or Team.
It may reference zero or more Goals as intent. The Unit type, intended-outcome semantics, Attempt model
and workflow lifecycle are identical at every scope level. **Future checker:** referential-integrity and
container-type validator. **Today:** repository protocols imply mission/program boundaries but no common
checker exists.

Corrected Unit fields replace generic `scope` with:

- `scope_container_ref` — exactly one Collective, Program, Mission or Team;
- `goal_refs` — zero or more Goal intent references (at least one when the workflow requires Goal-driven
  attribution);
- all previously specified Unit fields (`unit_id`, `unit_kind`, `intended_outcome`, workflow,
  dependencies, inputs/outputs, state, baseline, Attempt and Admission Contract references) unchanged.

Corrected relationships/cardinalities:

| Relation | Cardinality | Constraint |
|---|---:|---|
| ScopeContainer `(Collective|Program|Mission|Team)` — scopes → Unit | container 0..* Units; Unit exactly 1 primary container | organizational boundary only; no level-specific Unit type or meaning |
| Goal — pursued-by/advanced-by → Unit | Goal 0..* ↔ Unit 0..* | orthogonal intent attribution; does not replace Unit scope |
| ScopeContainer — contains → ScopeContainer | 0..* children; child 0..1 parent within a baseline | permitted nesting is organizational policy; cycles prohibited |

**Table reconciliation:** Capability continues to use the same four organizational scope levels. Record,
Signal and Admission Contract retain their own subject/organizational scope fields. The §7 Unit row now
reads “Collective/Program/Mission/Team boundary; decomposition” and not only program/mission/team. The §5
`Goal/Mission/Team — scopes → Unit` row is superseded by the two corrected rows above.

**Conforming:** a team-scoped code-review Unit has Team T as its sole primary ScopeContainer and advances
Goal G; its retry is another Attempt of the same Unit.
**Non-conforming:** the same Unit is independently typed `team-unit` and `program-unit`, or uses Goal G as
its scope while omitting an organizational ScopeContainer.

### RW1-D3 — Decision is a consequential event, not a Signal facet

**Authored bounded ruling:** a **Decision** is an immutable consequential event in which authorized Actor(s)
select a disposition for identified subject(s) within a declared authority basis. It has durable identity
because both histories require replay of direction changes and authoritative consequences. A Decision may
be conveyed by one or more Signals and documented by one or more Records; it is neither the Signal nor the
Record. An Admission Outcome/verdict may inform a Decision, while a workflow may map a verdict directly to
a transition without creating a discretionary Decision. A Decision may authorize a transition or Effect
Request, but it is not the resulting consequence or effect.

Minimum Decision fields: `decision_id`, `occurred_at`, `maker_refs` (1..* Actors), `authority_basis_ref`
(exactly 1), `scope_container_ref` (exactly 1), `subject_refs` (1..*), `selected_disposition`,
`rationale/evidence_refs` (0..*), `admission_outcome_refs` (0..*), `supersedes_decision_ref` (0..1), and
`provenance`.

**RW-DEC-1 (O):** Decision identity is immutable; reversal/correction creates a new Decision linked by
`supersedes`, never mutation of the old event. **Future checker:** decision-log schema and append-only
store outside ordinary governed-Actor mutation. **Today:** Issue comments/git history preserve fragments;
mutable Issue bodies do not uniformly enforce it.

**RW-DEC-2 (D, W1/W2 authority replays):** every Decision has one or more makers and exactly one explicit
authority basis valid for its organizational scope. Account attribution or autonomy tier alone is not
authority. **Future checker:** authority-policy evaluator. **Today:** human/protocol authority is
procedural; no common evaluator exists.

**RW-DEC-3 (D, X09/X11/X14):** verdict, Decision, Signal, Record, consequence, Unit transition, Effect
Request and Effect Receipt remain distinct. A deterministic workflow consequence may follow an Admission
Outcome without discretionary Decision; a human scope change is a Decision even before any effect occurs.
**Future checker:** typed relationship/cardinality validator plus workflow/effect plane. **Today:** native
workflow and forge enforce portions only.

Minimum Decision relations/cardinalities:

| Relation | Cardinality | Constraint |
|---|---:|---|
| Decision — made-by → Actor | Decision 1..* Actors; Actor 0..* Decisions | maker identity does not itself prove authority |
| Decision — authorized-by → AuthorityBasis | Decision exactly 1; basis 0..* Decisions | basis is version/baseline pinned |
| Decision — concerns → subject (Goal/Mission/Unit/Record/Claim/Effect Request) | Decision 1..* subjects | identified subject, never implicit prose |
| Admission Outcome — informs → Decision | Outcome 0..* ↔ Decision 0..* | verdict is not Decision; relation optional |
| Signal — conveys → Decision | Signal 0..1 Decision; Decision 0..* Signals | removes `action_kind=decision`; action facet may instead be `decision-notice` if needed |
| Record — documents → Decision | Record 0..* ↔ Decision 0..* | durability/carrier does not define Decision identity |
| Decision — authorizes → Unit Transition | Decision 0..* transitions; transition 0..1 Decision | some transitions follow contracts directly rather than Decisions |
| Decision — authorizes → Effect Request | Decision 0..* requests; request 0..1 Decision | authorization is not performance or receipt |
| Decision — supersedes → Decision | Decision 0..1 predecessor; predecessor 0..* successors | competing successors remain explicit rather than overwritten |

**Signal reconciliation:** §4.4's `action_kind = request|decision|directive` is superseded by
`action_kind = request|directive|decision-notice`; a Decision Signal conveys a `decision_ref`. The
epistemic/significance/route/carrier dimensions remain unchanged. §9's “Signal/Decision authority
reference” now means a Signal carries a Decision reference, and authority belongs to the Decision's
`authority_basis_ref`; a Signal may separately carry sender authority for non-Decision directives.

**Admission/consequence reconciliation:** the §5 row “Admission Outcome — causes → Unit
transition/Decision/Effect request” is superseded by three distinctions:

- Admission Outcome `informs` Decision (0..*), when judgment is escalated to an authority holder;
- Admission Outcome `triggers` Unit Transition (0..*) only where its pinned Contract defines that direct
  consequence;
- Decision `authorizes` Unit Transition or Effect Request (0..*) where discretionary authority is used.

**Cross-case discrimination:** `wfh-008` auditor `REWORKABLE` is an Admission Outcome whose contract
directly triggers a hold/rework transition; it need not be relabelled a Decision. The owner's final
accept/reject/redirect is a Decision conveyed in Issue Signals and documented by Records. In `vnc-045`,
gate 3a `REWORKABLE` is likewise an Outcome with workflow consequence; the human mechanism-only scope
reduction is a Decision that authorizes Unit cancellations/reformations; forge merge is an Effect caused
through a separately authorized request, not the Decision itself.

**Conforming:** independent audit Outcome O triggers `hold` under Contract K. Human H later makes Decision
D under owner authority, concerning Mission M and authorizing replacement Units; Signal S conveys D and
Record R documents it. O, D, S, R and the transitions retain separate identities.
**Non-conforming:** a PASS report is stored, so its author is inferred to have decided and performed a
merge. This collapses verdict, Record, authority, Decision and effect.

### Rework residual gaps

- D1 is internally closed at the conceptual level, but recursive Capability composition, parent
  `done_when`, scope expiry and enforcement remain unexecuted and unproven.
- D2 is internally closed by one four-type ScopeContainer set; actual nesting/validity policy and common
  scope enforcement remain program-owned and untested.
- D3 is internally closed as an identity/relationship model; authority-basis semantics, joint-decision
  policy, competing superseding Decisions and durable enforcement remain unimplemented and untested.
- These corrections do not change the W4 conclusion: semantic compression is plausible, not proven, and
  Admission Contract remains claimed rather than enforced.
