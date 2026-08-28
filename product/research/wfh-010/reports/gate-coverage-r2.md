# wfh-010 — Supplemental ontology/data-model coverage audit

**Role:** `factory-validator`  
**Gate:** supplemental independent audit of the 2026-08-28 Scope Extension only  
**Independence:** satisfied — this validator authored and advised on none of W1–W4  
**Original gate:** `reports/gate-coverage.md` remains **PASS** for W1–W3  
**Verdict:** **REWORKABLE**  
**Grade recommendation:** no grade movement; directional structure only

## Ruling

W4 substantially satisfies the extension: it supplies identity, type-versus-scope, invariants,
cross-case representations, nine-qualifier and X01–X16 reconciliation, enforcement/provenance notation,
and explicit residue for all five focal constructs. It also preserves the required separations among
Signal/Record, admission/evidence/decision/effect/Record existence, disclosure/observation,
custody/independence, currentness/supersession, and effect receipts.

Three exact internal/model-completeness defects prevent `PASS`. All are bounded documentary corrections;
none requires new research, case redesign, implementation, or synthesis.

## Exact defects and targeted remedies

### D1 — Capability's binding Goal requirement is internally weakened

**Failed clauses:** Extension provisional Capability rule; W4 output 4; supplemental requirement to apply
the rule consistently at every organizational level.

The binding candidate meaning says a Capability is an observable behavior **required for a Goal**. W4's
headline definition repeats that rule, but CAP-1 changes it to “at least one Goal that requires **or is
advanced by** it,” and the cardinality table allows a Capability to have zero `requires` relations while
`is-advanced-by` is expressly contributory/non-floor. The owner question in §12 leaves the same semantic
choice open. A retained concept cannot simultaneously require Goal requirement and permit contribution
alone.

**Targeted remedy:** choose one interpretation and make the headline definition, CAP-1/CAP-4,
cardinalities, re-adjudication register, and owner question consistent. Under the binding rule, the narrow
repair is: every Capability has at least one Goal-requirement relation; `is-advanced-by` may remain an
additional non-floor relation but cannot by itself qualify an object as a Capability. If “required” is
intended to include north-star rather than only claim-floor membership, state that distinction explicitly
without creating level-specific kinds or renaming the concept.

### D2 — Unit scope cardinality omits two admitted organizational levels

**Failed clauses:** W4 outputs 2 and 3; recursive/scoped analysis across
collective/program/mission/team.

The identity table and Capability model admit collective, program, mission, and team scopes. The Unit
type-versus-scope table admits program/mission/team. But the relationship/cardinality model states only
`Goal/Mission/Team — scopes → Unit`; Collective and Program are absent, and Goal is introduced as a scope
container without reconciling it with the stated scope model. Thus the exact scope relation does not cover
the model's own levels.

**Targeted remedy:** define the common `scope` target/container set once and use it consistently in the
identity table, Unit fields, type-versus-scope table, and cardinality row. Include or explicitly reject
Collective and Program for Unit scope, and explain whether Goal is itself a scope or an orthogonal intent
relation. Do not create different Unit meanings by level.

### D3 — Decision is named but not coherently related/cardinalized

**Failed clause:** W4 output 2, which requires a relationship/cardinality model connecting decisions to
the other constructs.

W4 correctly separates verdict from consequence, but Decision is represented inconsistently: Signal has
an optional `action_kind=decision`; an Admission Outcome may `cause` a `Decision`; §9 names a
“Signal/Decision authority reference”; and the cross-case representation uses a scalar
`decision_authority`. The relationship model gives no Decision identity/form, no `made-by`/authority
relation, and no relation from a Decision to the Unit transition or Effect Request it authorizes. A reader
cannot tell whether Decision is a Signal facet, a durable entity/event, or both. That leaves decision
authority and consequence partly in prose—the exact compression problem W4 is meant to resolve.

**Targeted remedy:** make one bounded ontological ruling for Decision and add the minimum relations and
cardinalities needed by both histories. If Decision is an event that may be transported by a Signal and
recorded by a Record, state those separations; relate it to its maker/authority, subject or scope, and any
authorized Unit transition/Effect Request. If it is only a Signal action facet, remove entity-like uses
and show how authoritative consequence remains independently represented. Preserve the rule that a
verdict, Decision, effect, and Record are not identical.

## Clause-by-clause audit

| Extension requirement | Result | Audit finding |
|---|---|---|
| Minimal identity model for Capability, Unit, Record, Signal, Admission Contract | **PASS** | §3 distinguishes entity/event/value form, durable identity, versions, attempts, state, category and relations. Consequential versus ephemeral Signal identity is explicit. |
| Relationship/cardinality model over all required constructs | **REWORKABLE** | Most relations and exact cardinalities are present, including attempts, envelopes, evidence, assessments, effects and receipts. D2 omits admitted scope containers; D3 leaves Decision ontologically and relationally incomplete. |
| Type versus scope for all five focal constructs | **REWORKABLE** | The common/extension boundary is explicit and does not hide native workflow/category semantics, but Unit scope is inconsistent across §3, §5 and §7 (D2). |
| Five re-adjudications with definitions, invariants and residue | **REWORKABLE** | Unit, Record, Signal and Admission Contract meet the clause. Capability conflicts are individually re-adjudicated without level-specific kinds, and Actor competence is correctly Qualification/Skill; however CAP-1/cardinalities weaken the binding Goal-required meaning (D1). |
| Concrete cross-case representations | **PASS** | Research admission remains directional; software tests are reported observations; merge proves only repository effect; interruption, rework, baselines, residue and safe resume are retained. |
| Nine recurrent qualifiers | **PASS** | All nine are enumerated and assigned typed common structure versus native ownership. Semantic compression is correctly only plausible, not proven. |
| Residue/contradiction ledger and X01–X16 | **PASS** | Every X01–X16 row is present. Missing evidence, unexecuted composition/resume, weak tiers, category behavior, custody and portability remain live rather than normalized away. |
| Provenance, enforcement and conforming/non-conforming examples | **PASS** | Clauses are marked derived/adapted/authored; future checker and present enforcement are distinguished; examples expose qualification/capability, report/observation, delivery/proof and verdict/effect confusion. |
| Shared skill catalog/local binding restriction | **PASS** | §12 records it only as an untested future Capability hypothesis and does not use it as evidence, design it, select it, configure it or recommend it. |

## Corrected Capability assessment

The evidence supports **retain, conditional on D1 correction**:

> Capability is one observable behavior required by at least one Goal, delivered by Features and/or
> enabled by Technologies. It may be recursively composed and scoped at collective, program, mission or
> team level without changing meaning. Actor competence is Qualification/Skill.

No historical conflict requires `actor|product|organization` kinds. The apparent W2 Actor-capability
usages are competence usages and therefore fall outside Capability under the binding rule; this is a
semantic reclassification, not evidence for an alternate Capability kind. W1's absent target remains
absence, not a conflicting meaning. The surviving residue is real: recursive cross-level composition,
parent `done_when`, scope expiry, and common enforcement have not been executed or proven.

## Preserved boundaries

- Record durability does not imply admission, truth, currentness, evidence grade, or effect occurrence.
- Signal transports information or Record references; it is not Record durability.
- Direct observation requires mechanical capture provenance. Historical authored reports remain claims
  that may reference reported observations.
- Admission Contract, Assessment, Outcome/verdict, Decision, consequence, effect and durable Record remain
  distinct, subject to D3's required relational clarification.
- Custody and gate-input independence are relations/predicates, never self-declared Actor labels.
- Effect receipts prove only their bounded effect and coupling; absence/unknown remains explicit.
- Category retains program-owned schema, admission eligibility, retrieval, lifecycle and correction rules.
- Workflow retains native states, transitions, proof bars and consequences.

## Synthesis implications

Synthesis remains blocked. A targeted W4 correction should address only D1–D3, after which this same
supplemental gate can be re-audited. The likely synthesis input, if those defects close, is a typed-envelope
hypothesis rather than the original flat vocabulary: Capability is retained under one meaning; Unit,
Record and Signal are revised; Admission Contract remains a claimed first-class construct; `lesson`
remains derived while a distinct category remains insufficiently evidenced. No build recommendation,
universal portability claim, enforcement claim, vocabulary-v2 decision, or grade movement follows.

## Surprises

- W4 resolved the alleged Capability overload semantically, but its own non-floor contribution relation
  quietly reintroduced ambiguity about what qualifies as a Capability.
- Decision—not Admission Contract—is the only required supporting construct still oscillating between a
  Signal facet and an entity-like node in the relationship model.
- The strongest remaining defects are internal consistency defects, not missing source coverage. The
  original W1–W3 `PASS` is unaffected.

## Required next action

Return W4 to its independent architect for one targeted rework round limited to D1–D3. Do not repair the
artifact in this validator role. Re-audit the revised W4 before curator synthesis. `wfh-009` remains held
and excluded.

---

## Round-1 re-audit — 2026-08-28

**Artifact audited:** append-only `findings-W4-data-model.md` section “Rework round 1 — 2026-08-28
(D1–D3 only)”
**Verdict:** **PASS**
**Original records preserved:** the W1–W3 coverage verdict remains **PASS**; the initial supplemental
`REWORKABLE` above remains the durable round-0 verdict and is superseded only for D1–D3 by this re-audit.

### D1 — PASS: Goal requirement and claim-floor are now distinct

The correction establishes one invariant consistently: every Capability has one or more Goal `requires`
relations. `is-advanced-by` is optional, contributory and non-qualifying. “Required” includes both
claim-floor threshold Capabilities and north-star/curve Capabilities; claim-floor membership is an
orthogonal Goal-policy classification. The corrected definition, RW-CAP-1, RW-CAP-4, cardinalities,
register reconciliation, examples and owner-question disposition agree.

This closes the defect without introducing level-specific Capability kinds or renaming the concept.

### D2 — PASS: one Unit ScopeContainer set; Goal is orthogonal

The correction defines exactly one organizational scope-container set:
`Collective | Program | Mission | Team`. Every Unit has exactly one primary `scope_container_ref`; all
four levels retain the same Unit meaning and may nest without changing type. Goal is explicitly excluded
from the set and relates independently through zero or more intent references. The corrected fields and
cardinalities supersede the inconsistent §3/§4/§5/§7 rows and cover collective, program, mission and team.

This closes the type-versus-scope and cardinality defect. Actual nesting/validity policy remains properly
program-owned and untested.

### D3 — PASS: Decision has coherent identity and relations

Decision is now one immutable consequential event with durable identity, identified makers, exactly one
authority basis, exactly one organizational scope, identified subjects, disposition, optional evidence
and Admission Outcomes, supersession and provenance. Its relations cover:

- `made-by` Actor and `authorized-by` AuthorityBasis;
- `concerns` identified subjects;
- optional Admission Outcome `informs` Decision;
- Signal `conveys` and Record `documents` Decision without identity collapse;
- Decision `authorizes` Unit Transition and/or Effect Request;
- immutable correction via Decision `supersedes` Decision.

The Signal action facet is reconciled to `decision-notice`, while direct contract consequences remain
Admission Outcome `triggers` Unit Transition. The examples correctly distinguish verdict, Decision,
Signal, Record, transition, request, performed effect and receipt. This closes the relationship and
authority defect without claiming common enforcement.

### No extension regression

The rework is restricted to D1–D3 and explicitly preserves the rest of W4. Independent comparison finds
no regression in the extension requirements:

- all five focal identity/type/scope/version/state/category/relation rulings remain intact;
- category-owned schema, admission eligibility, retrieval, lifecycle and correction semantics remain
  native rather than generic prose;
- workflow-owned states, transitions, proof bars and consequences remain native;
- Signal transport remains distinct from Record durability;
- Admission Contract, Assessment, Outcome/verdict, Decision, evidence, consequence, Effect Request,
  effect and Record existence remain distinct;
- disclosure versus direct observation, custody/gate-input independence, currentness/supersession,
  missing evidence and effect-receipt coupling remain explicit;
- the nine W3 qualifiers and X01–X16 residues are unchanged except for the exact conceptual closure of
  D1–D3;
- shared Qualification/Skill catalog with repository-local bindings remains only an explicitly untested
  future Capability hypothesis; and
- no synthesis, implementation, schema/configuration change, graph write, grade movement, build
  recommendation or `wfh-009` work was introduced.

### Corrected Capability ruling

**RETAIN**, directionally:

> A Capability is an observable behavior required by at least one Goal and delivered by Features and/or
> enabled by Technologies. It may be recursively composed and scoped at collective, program, mission or
> team level without changing meaning. Actor competence is Qualification/Skill.

No observed conflict requires `actor|product|organization` kinds. W1's proposed target remains an absent,
unadvanced Capability rather than a contrary meaning. W2 Actor architecture/implementation/testing/review
usages are Qualifications; its tag-mutation and bounded audit behaviors are Capabilities. Organizational
and team abilities qualify only when they denote observable Goal-required behavior, not member competence.

### Exact residues retained

1. Recursive cross-level Capability composition, parent `done_when`, scope expiry and evidence rollup are
   modeled but unexecuted and unproven.
2. ScopeContainer nesting/validity policy and common scope enforcement remain program-owned and untested.
3. Decision authority-basis semantics, joint-decision policy, competing supersession and durable external
   enforcement remain unimplemented and untested.
4. Admission Contract remains claimed from two owner-operated domains; its common enforcement, custody
   and broader portability remain untested.
5. A3/A4 autonomy evidence remains insufficient; generic stop/resume and common effect refusal remain
   unexecuted.
6. `lesson` survives as derived reusable guidance; a distinct `lesson-learned` versus `pattern` Record
   category remains insufficiently evidenced behaviorally.
7. Missing historical telemetry/raw test logs remain missing, and semantic compression remains plausible
   rather than proven.

These are honest directional limits, not remaining coverage defects.

### Synthesis implications

The supplemental extension gate now permits curator synthesis. Synthesis should use the corrected typed
model: Capability retained under the single Goal-required behavioral meaning; Unit, Record and Signal
revised; Decision made explicit as a consequential event; Admission Contract retained only as a claimed
first-class construct; and `lesson` retained as a derived construct while distinct category placement
remains insufficient.

Synthesis must preserve the residues above and may claim only that semantic compression is plausible
across these two histories. This `PASS` does not establish runtime enforcement, universal portability,
organizational effectiveness, a product boundary, a build recommendation, or any `partial`/`proven`
grade. `wfh-009` remains held and excluded.
