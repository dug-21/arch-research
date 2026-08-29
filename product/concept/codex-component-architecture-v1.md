# Conceptual Component Architecture — Codex Track V1

**Status:** directional, authored specification, `claimed`; not ratified, implemented, enforced, or proven  
**Run:** wfh-012 · independent Codex track  
**Question:** What logical component architecture can realize the target concept while satisfying A01–A25 and using the organizational data model V5 as directional vocabulary?

## 1. Objective and architectural stance

The architecture turns centralized human intent into distributed, repository-local work while retaining collective communication, memory, reporting, authority, and rapid redirection. It is an organizational architecture, not an agent framework: an LLM is one replaceable executor, a repository is one initial program boundary, and no centralized component schedules every local action.

The smallest stable shape is a **collective plane** plus repeatable **program cells**, joined by versioned contracts. The collective plane owns semantics and consequential boundaries. A program cell owns local method and execution. Some concerns are deliberately cross-cutting and cannot honestly be assigned to one component.

This model is derived from `target-concept-v1.md`, A01–A25, the `workflow-harness` theme lens, and organizational-data-model V5. V5 is directional vocabulary, not an implemented schema. Every component below is therefore a logical responsibility boundary, not a product or deployment unit.

## 2. Logical topology

```text
                         OWNER / COLLECTIVE AUTHORITY ROOT
                                      |
             +------------------------+-------------------------+
             |                        |                         |
     Operating-Model           Portfolio Direction      Effect Authority
       Authority                 & Resource Office          Boundaries
             |                        |                         ^
             v                        v                         |
     Publication &             envelopes/priorities       effect requests
     Compatibility                    |                    & dispositions
             |                        |                         |
   versioned baseline     +-----------+-----------+             |
             |            |                       |             |
             v            v                       v             |
      +------------- Program Cell A -------+  +-- Program Cell B --------+
      | Context Resolver                    |  | same logical boundaries   |
      | Local Work Coordinator              |  | different local workflow |
      | Work Continuity                     |  +---------------------------+
      | Model Router -> Execution Targets   |
      | Evidence & Gate Adapter             |
      | Communications Endpoint ------------+---- Cross-Program Exchange
      | Status Publisher -------------------+---- Reporting Aggregator
      | Memory Admission Client ------------+---- Organizational Memory
      +--------------------------------------+
                         ^                              |
                         +----- findings / needs -------+
```

Centralization means common authority, semantics, or collective visibility; it does not require one runtime, process, store, or deployment. Program cells may be replicated without enlarging the collective plane in proportion to their local work.

## 3. Component definition

### C1. Collective Authority and Intent

**Responsibility.** Establishes Collective and Program Scopes, authority roots, strategic Goals, consequential decisions, common invariants, and the authority to grant, revoke, or redirect work. It approves autonomy and risk posture but does not execute program work.

**Placement.** Collective; outside every governed program cell. **V5:** `Scope`, `Goal`, `Delegation`, decision and adaptation `Event`s. **Provenance:** derived from target concept §§Structure/Governance and A02, A05, A09, A20; adapted from V5 authority chain by separating decision custody from enforcement custody.

### C2. Operating-Model Authority

**Responsibility.** Custodies the common vocabulary, invariants, role and skill definitions, communication/reporting contracts, extension rules, and compatibility policy. It accepts or refuses proposed baseline changes through attributable adaptation decisions. Governed actors may propose changes but cannot publish them as authoritative.

**Placement.** Collective. **V5:** cross-cutting custody of `Workflow`, `Skill`, `Role`, `Gate`, `Delegation`, registries, catalogs, values, and I18–I19; it does not own all program definitions. **Provenance:** authored from A22–A24, resting on V5 program ownership and method custody.

### C3. Operating-Model Publication and Compatibility

**Responsibility.** Publishes immutable, identifiable collective baselines; resolves which baseline applies to a Program Scope; supplies approved local copies; evaluates declared program extensions; detects drift and reports compatibility. Publication conveys definitions, not authority credentials.

**Placement.** Collective publication with a program-local resolver/cache. **V5:** `Record` carries definitions and provenance; adaptation `Event` records change; `Scope` selects applicability. **Provenance:** authored from A22–A25. A centralized rules repository is a candidate realization only.

### C4. Portfolio Direction and Resource Office

**Responsibility.** Prioritizes Goals, Programs, Missions, and themes; allocates explicit resource envelopes; records exhaustion and exception policy; reconciles competing claims on scarce model use. It allocates, but never sequences local Units.

**Placement.** Collective decision responsibility with local consumption accounting. **V5:** `Goal`, `Scope`, `Delegation.resource_ceiling`, significant decision `Event`s. **Provenance:** authored from A05 and A19; the split between allocation and scheduling preserves A16.

### C5. Program Context Resolver

**Responsibility.** Before an Attempt begins, assembles its applicable operating-model baseline, Program extension, Workflow version, Delegations, Gates, resource envelope, memory references, and reporting/communication obligations. It records unresolved incompatibility rather than silently choosing.

**Placement.** Program-local, reading collective and local definitions. **V5:** `Scope`, `Workflow`, `Delegation`, `Gate`, `Record`, `Attempt.baseline_ref`. **Provenance:** authored synthesis of A08, A22–A25.

### C6. Local Work Coordinator

**Responsibility.** Decomposes authorized intent into durable Units, selects admissible next transitions, composes Roles/Actors/Skills, starts Attempts, coordinates local dependencies, handles interrupts, and preserves partial output. It operates only inside resolved Delegations and never grants itself effects.

**Placement.** Program/repository-local. **V5:** `Unit`, `Attempt`, `Workflow`, `Role`, `Skill`, `Actor`, `Delegation`; transition and communication `Event`s. **Provenance:** derived from A06–A10, A14, A16 and V5 I10, I15–I18; adapted by making team formation a coordinator responsibility without introducing a Team component.

### C7. Work Continuity Ledger

**Responsibility.** Maintains durable operational state sufficient for another authorized Actor to reconstruct a Unit and Attempt: identities, pinned baselines, progress, disposition, unresolved residue, admitted partial outputs, authority, resource use, and next admissible transition. It is not institutional knowledge and not a transcript archive.

**Placement.** Program-local authority for live work, with references exposed to collective reporting and memory. **V5:** `Unit`, `Attempt`, operational `Event`s and operational `Record` categories. **Provenance:** derived from A08, A10, A11 and V5 I15–I16; authored separation from C13 to preserve the theme's operations ≠ knowledge boundary.

### C8. Model Router

**Responsibility.** Selects an execution target for a bounded reasoning request according to declared task needs, information policy, resource envelope, availability, and routing policy. The request cannot select or mutate its own route. Callers receive provider-neutral results plus attribution and usage records.

**Placement.** Program edge behind an independently held routing policy; may be shared without becoming a scheduler. **V5:** `Technology` represents targets/mechanisms, `Actor` represents participating agents/services, observations record usage. **Provenance:** derived from A01, A04, A13 and A19.

### C9. Execution Target Adapter

**Responsibility.** Presents a stable invocation/result boundary over deterministic components, public models, and locally operated models; reports actual target, resource use, failure, and information-handling disposition. It has no authority beyond the Attempt's request.

**Placement.** Program edge; replaceable. **V5:** `Actor`, `Technology`, observation `Event`. **Provenance:** authored seam required by A01 and A13, resting on target concept §Build vs Buy.

### C10. Evidence and Gate Service

**Responsibility.** Evaluates an identified subject against a pinned baseline, explicit eligible evidence, missingness policy, proof bar, and independence predicate. It uses a deterministic procedure wherever that semantics can be expressed and judgment only where declared. It emits assessments and outcomes; it does not make the ensuing authority decision or effect.

**Placement.** Gate definition outside the governed activity; assessment may be local or collective provided independence holds. **V5:** `Gate`, `Record`, assessment and gate-outcome `Event`s, I4 and I6–I9. **Provenance:** derived from A04, A15, A24 and the garage firewall.

### C11. Effect Authority Boundary

**Responsibility.** Independently validates a requested effect against the exact Delegation, Scope, target, effect class, time, resource ceiling, and revocation state; performs or refuses it; issues an attributable disposition. Holding instructions or autonomy never substitutes for this decision.

**Placement.** Outside and unreachable for mutation by the governed Actor; logically collective even when physically near a program. **V5:** `EffectBoundary`, `Delegation`, effect-request and effect-disposition `Event`s, I12 and I17–I18. **Provenance:** derived from A02, A09, A13, A20 and A24.

### C12. Cross-Program Exchange

**Responsibility.** Addresses, routes, receives, acknowledges, correlates, and records needs, findings, risks, proposed work, decisions, and escalations across Scope boundaries. Contracts and routing policy are versioned. Delivery is distinct from acceptance and disposition.

**Placement.** Collective mediation with a program-local endpoint; no participant must know all other participants. **V5:** communication `Event` is used, but its single `scope_ref` means an exchange requires correlated send/receive Events or a future model extension; `Record` carries durable payloads. **Provenance:** authored from A03, A18 and A21, explicitly addressing V5's known cross-Scope delivery hole.

### C13. Organizational Memory

**Responsibility.** Admits, retrieves, supersedes, and relates durable knowledge while preserving provenance, epistemic kind, evidence altitude/grade, currentness, missingness, and correction history. Admission is category-governed; storage alone establishes nothing. Operational state enters only through explicit admission.

**Placement.** Centralized institutional substrate with program-scoped access and contribution. **V5:** `Record`, knowledge-relevant `Event`s, `Capability`, `Technology`, evidence values, I1–I5 and I8–I11. **Provenance:** derived from A03, A08, A11, A15, A21 and the workflow-harness knowledge/operations boundary.

### C14. Program Status Publisher

**Responsibility.** Derives a normalized, attributable status projection from local Units, Attempts, Events, Records, Delegations, budgets, risks, and evidence links. It publishes both periodic and milestone/exception updates without treating narrative summaries as authoritative evidence.

**Placement.** Program-local. **V5:** intentionally cross-cutting projection over `Scope`, `Goal`, `Unit`, `Attempt`, `Event`, `Record`, `Delegation`, and `Gate`. **Provenance:** authored from A12 and A17.

### C15. Collective Reporting Aggregator

**Responsibility.** Aggregates program projections into owner-facing portfolio views, preserving source attribution, baseline, freshness, resource use, blocked state, exceptions, decisions, and drill-down links. It does not mutate project state, infer completion from silence, or schedule work.

**Placement.** Collective. **V5:** cross-cutting read model, not a new entity; its durable outputs may be `Record`s and communication `Event`s. **Provenance:** authored from A05, A12, A17 and A19.

### C16. Capability and Team Formation

**Responsibility.** Discovers Skills and Actors, evaluates current competence evidence, proposes a deliberately dissimilar composition, establishes Roles and scoped Delegations, and registers new Capabilities/Workflows without changing the common model. Formation itself remains gated and attributable.

**Placement.** Collective discovery plus Program-owned composition. **V5:** `Capability`, `Actor`, `Skill`, `Role`, `Workflow`, `Delegation`, `Technology`, team `Scope`. **Provenance:** derived from A06, A14, A23 and target concept §Core Principle.

## 4. Interaction contracts

### 4.1 Start and execute

1. C1 establishes a Goal/Scope; C4 attaches priority and a resource envelope.
2. C5 resolves an immutable collective baseline plus explicit Program extension.
3. C6 creates or resumes a Unit and an Attempt under pinned Workflow, Delegation, and Gates.
4. C8 selects C9 targets within information and budget constraints; observations flow to C7.
5. Consequential action is requested from C11, never performed merely because C6 or an executor intends it.
6. C10 assesses completion evidence; a distinct authority decision accepts, rejects, redirects, or holds.

### 4.2 Interrupt and resume

1. Owner stop/revocation reaches C1/C11 and C6.
2. C11 refuses new disallowed effects; C6 drives the Attempt to its declared safe boundary.
3. C7 persists disposition, partial outputs, unresolved residue, pinned baselines, and next admissible transition.
4. A later Actor uses C5 and C7 to revalidate authority, compatibility, and prerequisites before resumption.

### 4.3 Cross-program learning

1. A Program emits an addressed communication through C12, referring to a durable Record where appropriate.
2. The recipient records receipt separately, acknowledges when required, and decides disposition under its own authority.
3. C13 admits a finding only under category rules. C14/C15 expose delivery and disposition without equating either with truth or adoption.

### 4.4 Operating-model evolution

1. A Program proposes an adaptation with evidence and affected baselines.
2. C2 decides through the applicable authority/gates; C3 publishes a new immutable baseline.
3. Program resolvers retain the prior approved baseline, identify drift, and evaluate compatibility. No in-flight Attempt silently changes baseline.

## 5. Constraints and enforcement points

The checks below specify logical enforcement; **none is claimed to exist commonly today**. A checker implemented inside the bound Actor is not sufficient where the rule requires independence.

| Constraint | What checks it | Logical location | Bound party can mutate/bypass it? | Current reality |
|---|---|---|---|---|
| E1: governed work cannot alter its governing baseline | baseline digest/version comparison at Attempt start, transition, and resume | C3/C5, with custody in C2 | No | no common checker |
| E2: derived Delegation cannot exceed parent | mechanical attenuation comparison; unresolved dimensions fail closed | C1/C11 | No | V5 comparison semantics remain open |
| E3: autonomy grants no effect authority | C11 requires a valid effect grant and issues every disposition | independent effect boundary | No | fragments only; no common boundary |
| E4: required evidence or independence missing cannot pass | Gate procedure checks evidence set, missingness, and assessor read/write independence | C10 outside executor | No | garage firewall covers one domain only |
| E5: deterministic checks take precedence where declared | Workflow/Gate definition names procedure; conformance rejects undeclared judgment substitution | C2 definition custody; C10 execution | No | no ecosystem checker |
| E6: local extensions cannot weaken common invariants | compatibility evaluation against pinned core invariant set | C3 | Program can propose, not publish compatible status | no common checker |
| E7: an Attempt identifies its governing baseline | C5 refuses start/resume without exact baseline identity | program boundary, definition external | Executor cannot amend accepted record | no common checker |
| E8: budget exhaustion follows declared disposition | C4 envelope plus C7 metering; C8/C11 refuse or escalate | allocation collective, consumption local, effect independent | Executor cannot raise ceiling | no common mechanism |
| E9: routing is outside the routed request | C8 ignores target-selection instructions from payload and applies policy | outside C9 target | Target cannot mutate policy | no common router |
| E10: stop/revocation prevents new consequential effects | revocation-aware check immediately before effect | C11 | No | no common mechanism |
| E11: status does not invent completion | C14 requires assessment/evidence references; C15 shows unknown/stale explicitly | publisher and aggregator | Local reporter may lie; links permit detection, so assurance requires independent verification for consequential use | no common contract/checker |
| E12: knowledge admission does not equal storage or truth | category admission procedure emits explicit admission; grade/currentness remain separate | C13 outside submitting Actor | Submitter cannot self-admit where independence required | Unimatrix enforces fragments, not this common model |
| E13: cross-program delivery is attributable and acknowledged when required | C12 validates sender authority, recipient address, contract version, and acknowledgement state | exchange endpoints/mediation | Sender cannot forge recipient acknowledgement | no common mechanism |
| E14: model/information controls can strengthen without semantic migration | adapters implement stable logical identity, authority, and event contracts | C8/C9/C11 seams | executor cannot redefine contract | seam only |

## 6. Discriminating examples

### Conforming bounded research autonomy

The owner grants the research Program a time-bounded Delegation to pursue one approved theme with a fixed model-usage ceiling, no external spend, reversible repository-local effects, daily plus milestone reporting, and escalation on premise change. An Attempt pins operating-model and Workflow baselines. C8 chooses models within budget. C7 preserves a safe resume state. Findings are sent through C12 to an affected project and admitted to C13 only under evidence semantics. C10 assesses any completion claim; C11 refuses effects outside the grant.

This conforms because initiative, resources, effects, proof, communication, memory, and reporting are independently represented and bounded.

### Non-conforming “autonomous” repository agent

A repository instruction tells an agent to “work until done,” choose any model, update its own rules when blocked, write directly to shared memory, and report success in prose. The same credentials allow it to merge changes. No exact baseline, Delegation, resource ceiling, independent Gate, effect disposition, safe-stop state, or evidence link exists.

This fails E1–E12. The instruction may influence behavior, but it is neither authority nor enforcement, and its success summary is not proof.

## 7. Central versus local placement rule

Place a responsibility in the collective plane when it defines shared semantics, allocates cross-program scarcity, holds authority over consequential effects, preserves institution-wide memory, or produces collective visibility. Place it in a Program cell when it sequences local reversible work, binds local methods, maintains live execution state, or adapts a common contract without weakening it. Split the concern when collective authority and local operation are both required; budgets, operating-model resolution, communications, reporting, and memory admission all use this pattern.

## 8. V5 vocabulary placement and exclusions

| V5 construct | Architectural placement |
|---|---|
| `Scope` | cross-cutting identity/boundary used by C1–C16; Collective and Program Scopes anchor placement, Mission/Team Scopes remain compositions |
| `Goal` | C1 intent; prioritized by C4 and advanced through C6 Units |
| `Capability` | C16 formation/catalog and C13 evidence-bearing memory; delivered by C6 work, assessed by C10 |
| `Actor` | cross-cutting participant identity; C6 composition, C9 execution, C10 assessment, C11 effects; declaration is never authority |
| `Unit` | C6 durable local work identity; status projected by C14 |
| `Event` | intentionally cross-cutting immutable occurrence vocabulary across all interactions; never the authority or telemetry store itself |
| `Record` | intentionally cross-cutting durable information; C7 operational records and C13 knowledge records remain category-separated |
| `Workflow` | Program-owned definition resolved by C5, executed by C6, custodied under C2/C3 rules |
| `Skill` | C16 discovery and competence; bound locally by Programs |
| `Role` | C16 reusable responsibility; C6 uses role assignments, C10 uses assessor independence |
| `Delegation` | cross-cutting authority envelope from C1/C4 through C5/C6/C8/C11; never inferred from Role or autonomy |
| `Gate` | C10 definition/evaluation, with C2 custody and C5 baseline resolution |
| `EffectBoundary` | C11 exclusively |
| `Attempt` | C6 execution and C7 continuity |
| `Technology` | C13 evidence-bearing mechanism catalog; C8/C9 execution targets may reference it without grade transfer |
| registries | C2 owns common admission semantics; Programs register permitted extension entries through C3 compatibility |
| catalogs | C16 discovers Skills; Programs own Workflow/Gate catalog entries under C2/C3 rules |
| values | common semantics published by C2/C3 and consumed across components; Program vocabularies may extend only where declared |

V5's explicitly excluded constructs remain excluded here: Feature is a `unit_kind`; Qualification is evidence on Actor–Skill; Envelope is part of Delegation; AuthorityBasis is Scope/Delegation; EvidenceItem is a Record role; RecordVersion is versioning; Signal/Decision/Transition/Assessment/Outcome/EffectRequest/EffectReceipt are Event types; request and disposition remain separate; organizational level does not create Capability kinds; Goal is not Scope; Attempt is not Unit; lesson is not an Event type; and there is no universal lifecycle, proof bar, closed taxonomy, or equation of autonomy with authority/evidence.

## 9. Assumption traceability

| Assumption | Realized by | Status in this model |
|---|---|---|
| A01 | C8–C9, E9/E14 | accommodated |
| A02 | C1/C2/C11, E1–E3/E10 | accommodated |
| A03 | C12–C13 | accommodated; delivery semantics remain open |
| A04 | C8/C10, E5 | accommodated |
| A05 | topology and placement rule; C1–C4/C13/C15 vs C5–C9/C14 | accommodated |
| A06 | C16 plus registries/catalogs | accommodated |
| A07 | first slice and component seams | accommodated |
| A08 | C5–C7 | accommodated |
| A09 | C1/C4/C6/C11 | accommodated; tiers provisional |
| A10 | interrupt/resume interaction, C7/C11 | accommodated; safe-boundary taxonomy open |
| A11 | C13 and separation from C7 | accommodated |
| A12 | C14–C15 | accommodated |
| A13 | C8/C9/C11 and E14 | accommodated as seam, assurance unresolved |
| A14 | C16 | accommodated |
| A15 | C10/C13, E4/E12 | accommodated |
| A16 | repeatable Program cell, C6 | accommodated |
| A17 | C14–C15, E11 | accommodated; normalized contract open |
| A18 | C12 versioned contracts | accommodated; intentionally evolutionary |
| A19 | C4/C7/C8, E8 | accommodated; accounting semantics open |
| A20 | C1/C4/C11 risk-sensitive grants | accommodated; classification open |
| A21 | C12/C13/C16 | accommodated; theme/project cardinality unresolved |
| A22 | C2–C5 | accommodated |
| A23 | C2/C3, E6 | accommodated; extension mechanism open |
| A24 | C3/C5 distinct from C10/C11 | accommodated |
| A25 | C3/C5/C7, E7 | accommodated; staleness policy open |

No assumption is excluded. Provisional assumptions are accommodated without being ratified.

## 10. First autonomy capability slice

The smallest useful end-to-end slice is **bounded research-theme continuation with centralized reporting**, not general autonomous software delivery:

1. One research Program resolves an exact collective baseline and one local Workflow.
2. The owner grants one theme-scoped Delegation with time/model-use ceilings, allowed reversible local effects, escalation rules, daily reporting, and absolute stop.
3. The local coordinator runs or resumes one Unit/Attempt, records usage and safe-resume state, and routes model work through a replaceable boundary.
4. Status is published daily and on milestone/exception, with links to evidence and exact baselines.
5. A finding may be delivered to one project through an attributable, acknowledged exchange; acceptance remains that project's decision.
6. No autonomous external spend, proof-grade change, collective-rule change, or foundational data-platform effect is allowed.

This slice exercises the highest-learning seams—cross-session autonomy, budgets, reporting, cross-repository exchange, rule discovery, and stop/recovery—while containing the owner's named early risks: wasted model use and work on the wrong problem. It is a proposed capability slice, not an implementation plan or BUILD recommendation.

## 11. Evolution seams

- Replace publication location, local-copy mechanism, and compatibility checker without changing baseline identity or authority semantics.
- Evolve communication classes, routes, delivery guarantees, and acknowledgements behind C12's versioned exchange contract.
- Strengthen identity, isolation, information flow, credentials, and effect enforcement behind C3/C8/C9/C11.
- Add model providers or local runtimes behind C8/C9 without exposing them above the route boundary.
- Extend organizational memory categories and retrieval behind C13 without admitting runtime state by default.
- Add Programs, Workflows, Skills, Roles, record categories, event types, unit kinds, and effect classes by registration rather than new common entities.
- Change reporting cadence and views without changing the attributable status projection.
- Refine autonomy tiers and risk classes without conflating initiative, evidence, or effect authority.
- Allow one theme to serve one, many, or all Programs; cardinality remains data, not topology.

## 12. Strongest objection

The model may be too semantically ambitious for the first slice: trustworthy baselines, delegations, budgets, status, communication, evidence, and effects together demand a common identity/reference discipline before any one feature feels useful. The countermeasure is not to merge the components; that would erase the safety boundaries. It is to implement only the minimum fields and one narrow path while leaving non-consequential boundaries as explicitly unenforced claims. Whether that still yields enough operational value is unproven and must be tested.

## 13. Deliberately left out

- Vendor, library, product, protocol, storage, repository-host, deployment, and runtime choices.
- Physical centralization, tenancy, networking, replication, consistency, availability, and disaster-recovery design.
- A final autonomy taxonomy, risk matrix, budget currency, status schema, communication taxonomy, or operating-model document format.
- Identity attestation, delegation attenuation algorithms, revocation propagation, effect taxonomy, and information-classification policy.
- A decision that Unimatrix owns operational state; this model assigns it the durable-memory role and leaves extensions subject to category semantics.
- One-theme-per-project mapping, a finance capability, or a universal organization chart.
- Feasibility, proof, grades, implementation, and any recommendation to build a product boundary such as Jurati.

## 14. Owner questions

1. Is the first portfolio budget allocated per theme, per Program, per time window, or as a hierarchy of all three?
2. What is the minimum acceptable local effect set for bounded research autonomy: working-tree edits, commits, branches, issue creation, or fewer?
3. Which events require immediate owner interruption versus daily reporting and continued work?
4. What stale-baseline window is acceptable for the first research Program, and which changes force an immediate hold?
5. Should cross-program delivery require recipient acknowledgement for all messages, or only consequential classes?
6. May garage findings create proposed project Units automatically, or only communications awaiting project acceptance?
7. What normalized status facts must every Program publish before prose is generated?
8. Which information classes are forbidden from public model targets in the initial pragmatic posture?
9. Who may ratify collective operating-model changes besides the owner, if anyone?
10. What operating evidence earns a Program a broader autonomy tier, and what evidence automatically revokes it?

