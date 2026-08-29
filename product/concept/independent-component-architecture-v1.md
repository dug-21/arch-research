# Independent Component Architecture V1 — Codex Challenge Track

**Track:** independent Codex challenge track for `wfh-012`  
**Status:** claimed conceptual design; not ratified, implemented, validated, or proven  
**Question:** What logical component architecture can realize `target-concept-v1.md` while satisfying A01–A25 and using the Organizational Data Model V5 as directional vocabulary?

## Objective and design position

The architecture must let one collective set intent and invariants while independently operated programs perform bounded work in their own repositories, exchange consequential information, preserve governed knowledge, and report enough normalized state for owner steering. It must support useful autonomy before the whole organization exists.

The proposed shape is a **federated control mesh**: a small collective core publishes definitions, allocates authority and resource envelopes, admits durable knowledge, and composes reporting; program-local execution cells plan and execute reversible work. Communication, model routing, assessment, and effect enforcement are explicit boundaries rather than implicit behavior of an agent or a shared store.

This is a logical partition, not a deployment claim. “Collective” and “program-local” denote custody and authority, not hosts, services, repositories, or databases.

## Architectural rules

| ID | Rule | Provenance | Enforcement point and reachability |
|---|---|---|---|
| R1 | Centralize intent, common semantics, institutional memory, consequential decisions, and authority policy; distribute reasoning, planning, communication, and reversible execution. | **Derived** from A05, A16 and `target-concept-v1.md`. | The Operating-Model Authority classifies definitions and the Program Conformance Boundary checks local manifests. No common checker exists today. A program may submit an extension but cannot write the accepted collective baseline. |
| R2 | Operating definitions, operational state, durable knowledge, and effect authority remain separate logical planes. | **Derived** from A02, A11, A24 and `themes.md` “operations ≠ knowledge.” | Plane-specific admission interfaces and custodians check crossings. No complete common enforcement exists today. Governed actors may request crossings but cannot admit their own knowledge, approve their own gate result, or mint effect authority. |
| R3 | Every Attempt pins immutable versions of its Unit baseline, Workflow, Delegation, relevant Gates, and collective operating-model baseline. | **Adapted** from V5 Attempt/Delegation/Gate plus A08 and A25; adds the operating-model baseline to the pinned set. | The Local Continuity Ledger rejects start/resume without the references; the Assessment Boundary rejects an unpinned subject. No cross-program implementation exists today. The executing actor can propose but cannot alter pinned revisions. |
| R4 | Autonomy grants initiative only. Every consequential effect requires a separately evaluated request at an independently controlled Effect Boundary. | **Derived** from A02, A09, A20 and V5 I12/I17. | The Effect Authority Boundary validates the Delegation chain, effect class, target, expiry, and resource ceiling, then records a disposition. It is unreachable for mutation by the governed Attempt; the actor can only request an effect. |
| R5 | A completion or consequential claim crosses an acceptance boundary only through a pinned Gate whose missingness and independence checks fail closed. | **Derived** from A04, A15, A24 and V5 I6–I9. | The Assessment and Evidence Boundary checks the evidence set and assessor independence and emits assessment and gate-outcome Events. It is outside the executor's write boundary. Nothing enforces this ecosystem-wide today. |
| R6 | Cross-program delivery is addressed, attributable, acknowledged when required, and dispositioned; shared storage is not delivery. | **Authored**, resting on A03, A18, A21 and V5 communication Event. | The Communication Exchange validates sender authority, destination, contract version, and acknowledgement rule; recipient-side intake records acceptance, rejection, routing, or deferral. Participants can author messages but cannot forge the receiver's acknowledgement. No common exchange exists today. |
| R7 | Central reporting is a projection, not an execution controller or source of truth for project work. | **Authored**, resting on A12, A16 and A17. | The Status Projection and Portfolio View accepts normalized reports with evidence references; source programs retain authoritative Unit/Attempt records. The reporting plane cannot schedule or mutate local work. |
| R8 | Resource envelopes are allocated centrally enough to express portfolio priority and consumed locally without central scheduling. | **Authored**, resting on A19 and A20. | Portfolio Steering issues versioned envelopes; Local Resource Accounting refuses or escalates exhaustion, while Model Mediation admits model calls against the same envelope. An executor can observe remaining allowance but cannot enlarge it. |
| R9 | Deterministic checks are used where their required semantics can be mechanically decided; judgment procedures are declared and isolated. | **Derived** from A04 and V5 Gate.procedure. | The Gate definition names `deterministic` or `judgment`; the Assessment Boundary records procedure and assessor. The governed actor cannot relabel a pinned Gate. The criterion for moving a judgment to a deterministic check remains open. |
| R10 | Local extensions may add registered concepts but may not redefine collective identities, relations, or invariants. | **Derived** from A22–A25 and V5 I19. | The Program Conformance Boundary compares the extension manifest to the pinned baseline and reports drift. Programs can edit local definitions but cannot publish them as collective-compatible without this check. No checker exists today. |
| R11 | Stop, hold, redirect, and recovery preserve attribution and partial output without converting it into accepted completion. | **Derived** from A08, A10 and V5 Attempt/I15. | Local Execution Coordination transitions the Attempt to hold/cancel/rework and writes resume requirements; Evidence Admission independently decides whether any partial Record is admitted. The owner/control interface is outside the executing actor. |
| R12 | Stored information retains provenance, epistemic kind, evidence altitude, currentness, missingness, and supersession history; storage alone grants none of truth, admission, or proof. | **Derived** from A11, A15 and V5 I1–I5/I8/I9. | Governed Memory Admission checks category rules; corrections append superseding Records/Events. Writers cannot overwrite history or self-assign acceptance. Current Unimatrix enforces fragments, not this whole contract. |

## Logical component model

### Collective-custody components

#### C1. Operating-Model Authority

Publishes immutable, version-identifiable collective baselines: vocabulary, invariants, extension points, communication obligations, reporting meaning, authority rules, and evidence rules. Resolves which baseline applies to a Scope and supplies approved local-copy metadata. Accepts authorized adaptation decisions but never edits a baseline in place.

**Provenance:** **Derived** from A22–A25 and V5 program ownership, method custody, I18/I19. The candidate centralized rules repository is one possible realization, not this component's identity.

#### C2. Organization and Capability Registry

Maintains discoverable identities and relationships for Scope, Goal, Capability, Actor, Skill, Role, Workflow, Gate, and Technology plus registered types/catalog entries. Supports capability formation by registering new Goals, observable Capabilities, required Skills, team Scopes, Roles, and Workflows without changing the common entity set. Skill evidence is used for matching but grants neither authority nor capability proof.

**Provenance:** **Adapted** from all V5 core/supporting definitions and A06/A14. It adds a composition query that finds dissimilar relevant Skills across program boundaries.

#### C3. Authority and Delegation Administration

Roots authority in Scope, creates versioned standing and dynamic Delegations, verifies attenuation, classifies program/effect risk, manages revocation and escalation, and binds resource ceilings. It describes authority; it does not perform effects.

**Provenance:** **Derived** from A02/A09/A20 and V5 Scope, Role, Delegation, I12/I17/I18.

#### C4. Portfolio Steering and Budget Allocation

Turns owner priorities into bounded, versioned resource envelopes for Programs, Missions, themes, or Units; records allocation, exhaustion policy, reporting cadence, and exception conditions. It prioritizes without assigning the internal sequence of project work.

**Provenance:** **Authored** from A19 and the owner's budget concern. V5 Delegation.resource_ceiling supplies the envelope vocabulary but does not define portfolio allocation.

#### C5. Governed Memory

Preserves admitted Records and durable Events with provenance, epistemic status, evidence altitude, currentness, missingness, and supersession. Category-owned rules govern admission, retrieval, lifecycle, and correction. It provides institutional recall and cross-program learning, not workflow scheduling, raw transcript retention by default, live telemetry control, or effect authority.

**Provenance:** **Derived** from A11/A15, V5 Record/Event/I1–I9, and the `themes.md` operations/knowledge boundary. Unimatrix is the intended initial substrate and may need extension; that is a realization decision, not a logical merger.

#### C6. Status Projection and Portfolio View

Receives normalized, attributable program reports; links summaries to authoritative Units, Attempts, Events, Records, budgets, decisions, risks, blocks, and evidence; composes daily, milestone, exception, and owner-requested views. It detects missing, stale, or incompatible reports and baseline drift. It cannot dispatch work.

**Provenance:** **Authored** from A12/A17/A19/A25 and the owner's daily-or-milestone direction.

### Federated boundary components

These have collective contracts but independently operated endpoints at each program.

#### C7. Communication Exchange

Routes versioned communication Events between addressed Scopes. It supports project research requests, garage finding delivery, status notices, decisions, exceptions, acknowledgements, escalation, and disposition. A theme may serve one, many, or all projects; routing uses declared audience/beneficiary relations rather than one-theme-per-project cardinality.

**Provenance:** **Authored** from A03/A18/A21 and V5 Event.communication. Delivery semantics deliberately remain evolvable.

#### C8. Program Conformance Boundary

Resolves the applicable collective baseline, checks local extension compatibility, supplies an approved local copy during publication outages, and emits drift/conformance evidence. Instruction delivery is an input, never proof of conformance. Higher-risk Programs may require stricter freshness and enforcement without changing logical identities.

**Provenance:** **Authored** from A13/A22–A25 and V5 I19.

#### C9. Assessment and Evidence Boundary

Evaluates identified Units, Records, Capabilities, or Events against pinned Gates. It separates observations, assessments, outcomes, decisions, transitions, effect requests, effect dispositions, and Records; checks eligible evidence, missingness, procedure altitude, and assessor independence; then emits assessment and gate-outcome Events. It admits evidence to memory only through category rules.

**Provenance:** **Derived** from A04/A15/A24 and V5 Gate/Event/Record/I4/I6–I9.

#### C10. Effect Authority Boundary

The sole logical performer/refuser for registered consequential effect classes. It evaluates an effect request against the immutable Delegation chain, Scope, target, budget, expiry, and any gate outcome; retains effect credentials outside the Attempt; and emits a distinct effect-disposition Event with coupling semantics.

**Provenance:** **Derived** from A02/A09/A13/A20/A24 and V5 EffectBoundary, effect Events, I12.

### Program-local execution-cell components

#### C11. Local Execution Coordination

Turns authorized Goals/Missions into Workflow-governed Units and Attempts; composes Actors/Roles/Skills; sequences dependencies; records state transitions; responds to owner stop/redirect; preserves partial outputs and resume requirements; and publishes normalized status. It owns project-local coordination but cannot alter pinned collective rules, its Delegation, Gate definitions, or effect credentials.

**Provenance:** **Adapted** from A07/A08/A10/A14/A16 and V5 Goal/Unit/Workflow/Attempt. It interprets “repository-local” as the initial execution boundary without equating Program and repository.

#### C12. Local Continuity Ledger

Holds authoritative operational state needed to reconstruct current Units and Attempts: baselines, actors, transitions, resource consumption, unresolved residue, pending acknowledgements, safe-stop state, and next admissible action. It references durable knowledge but is not itself the institutional knowledge store.

**Provenance:** **Authored** from A08/A10/A16/A17/A25 and the operations/knowledge separation. V5 Unit, Attempt, and Event supply its state vocabulary.

#### C13. Model Mediation

Selects a model execution target outside the work being routed, applies information-access and resource-envelope constraints, records attributable usage and route metadata, and hides provider/runtime identity from upstream workflow semantics. Local and publicly served targets are interchangeable behind this boundary.

**Provenance:** **Authored** from A01/A04/A13/A19 and `target-concept-v1.md` build-vs-buy direction.

#### C14. Local Resource Accounting

Measures resource use per Delegation, Unit, Attempt, and model route; compares consumption with the allocated envelope; publishes normalized usage; and invokes predeclared exhaustion behavior. It does not decide portfolio priority or expand a ceiling.

**Provenance:** **Authored** from A12/A19/A20 and V5 Delegation.resource_ceiling.

## Interactions and information ownership

1. **Establish context.** C11 asks C8 for the applicable C1 baseline. C8 resolves and pins a current or permitted local copy, overlays program extensions, and records compatibility/drift.
2. **Authorize work.** C3 issues a Delegation rooted in Scope and bounded by autonomy, effect grants, resource ceiling, expiry, escalation, and sub-delegation. C4 supplies the portfolio envelope from which the ceiling is derived.
3. **Form and execute.** C2 supplies Goals, Capabilities, Skills, Roles, Workflows, and candidate Actors. C11 creates Units and Attempts; C12 records operational transitions and recovery state.
4. **Route reasoning.** C11 submits a bounded work request to C13. C13 selects an eligible target and C14 accounts for use. Model output returns as a claim or proposed artifact, never an accepted outcome.
5. **Assess.** C9 evaluates output and baseline under a pinned Gate, recording explicit missingness and independent assessment/outcome Events. Admissible durable knowledge crosses into C5 under its Record Category.
6. **Cause an effect.** C11 emits an effect-request Event to C10. C10 independently performs, refuses, or records unknown and emits the separate disposition. Only that disposition demonstrates the enforced result.
7. **Communicate.** C7 delivers addressed communication Events. A receiver records acknowledgement and disposition; consequential content may be admitted to C5 but delivery does not depend on shared-memory discovery.
8. **Report and steer.** C11/C12/C14 publish normalized status to C6 with source references. C6 composes owner views. Owner redirection becomes a decision/adaptation Event and, where needed, revised Delegation or baseline—not an in-place mutation of an active Attempt.

## Central versus local placement test

| If the capability primarily… | Logical custody |
|---|---|
| defines common meaning, invariants, authority roots, portfolio priority, institutional admission, or owner-wide visibility | collective |
| reasons, plans, schedules project work, maintains live execution state, consumes a local envelope, or performs reversible repository work | program-local |
| carries claims or verifies compatibility between independent Scopes | federated contract with independently controlled endpoints |
| can cause a consequential external change | the Effect Authority Boundary controlling that effect, never the requesting execution cell |

A new component belongs in the collective core only if divergent program implementations would break shared meaning, authority, admission, or owner steering. Convenience and reuse alone are insufficient.

## Organizational Data Model V5 placement

| V5 construct | Primary architectural home | Treatment |
|---|---|---|
| Scope | C2 identity; C3 authority root; cross-cutting all boundaries | **Cross-cutting** organizational, authority, and information boundary. |
| Goal | C2 definition; consumed by C11 | Intent, not a Scope or work item. |
| Capability | C2 definition; delivery assessed by C9 | Observable behavior; delivery and proof remain separate. |
| Actor | C2 identity; used by C3/C9/C11 | Participant identity; declared identity is not attestation or authority. |
| Unit | C11 lifecycle; C12 state | Durable work identity across retries; outcome change creates a new Unit. |
| Event | C12 operational custody, C7 exchange, C5 durable admission | **Cross-cutting** immutable occurrence; durability depends on type/significance. |
| Record | C5 custody; produced by C11 and assessed by C9 | Durable governed information, distinct from Event and effect. |
| Workflow | C2 catalog/definition; executed by C11 | Program-owned method; custodian outside governed Attempt. |
| Skill | C2 catalog and matching | Competence only; no authority or Capability proof. |
| Role | C2 responsibility; C3 standing delegation; C11 composition | Responsibility and independence constraints, not authority by itself. |
| Delegation | C3 definition; pinned by C11/C12; enforced by C10 | **Cross-cutting** grant of initiative, limits, and declared effect classes. |
| Gate | C2 catalog/definition; executed by C9 | Pinned evaluation rule with explicit procedure and missingness. |
| EffectBoundary | C10 | Independently controlled performer/refuser of effects. |
| Attempt | C11 execution; C12 continuity | One execution against a baseline, not a Unit subtype. |
| Technology | C2 catalog; selected downstream of architecture | Mechanism enabling Capability; never the Capability or its proof. |
| Registries (`scope_type`, classifications, event/record/unit/effect types) | C1 common extension semantics; C2 operational catalog; C8 compatibility | **Cross-cutting** controlled extensibility; program entries cannot weaken common invariants. |
| Catalogs (skill, workflow, gate) | C2 | Discoverable definitions with collective/program ownership retained. |
| Value vocabularies | C1 baseline; used by C3/C5/C7/C9/C10/C12 | **Cross-cutting** common semantics. A3/A4 remain insufficient-evidence, not silently ratified. |
| I1–I19 | C1 publication; C8 conformance; component-specific checks | **Cross-cutting** invariants. Their present enforcement gaps remain explicit. |
| V5 excluded constructs | none | **Explicitly excluded as components.** Feature is a `unit_kind`; Qualification is Actor–Skill evidence; Envelope travels with Delegation; AuthorityBasis is Scope/Delegation; EvidenceItem is a Record role; RecordVersion is Record history; Signal/Decision/Transition/Assessment/Outcome/EffectRequest/EffectReceipt are Event types; merged effect event, organizational Capability kinds, Goal-as-Scope, Attempt-as-Unit subtype, lesson-as-Event, universal lifecycle/proof bar/taxonomy, and autonomy-as-authority would violate V5 separations. |

No V5 core or supporting construct is omitted. Registries, catalogs, values, and invariants are cross-cutting definition material rather than additional runtime components.

## Assumption traceability

| Assumption | Architectural response | Status |
|---|---|---|
| A01 | C13 routes outside routed work and hides target identity. | addressed |
| A02 | C3 declares authority; C10 holds credentials and enforces effects outside C11. | addressed |
| A03 | C7 provides addressed delivery and receiver disposition distinct from storage. | addressed |
| A04 | R9 and C9 declare/check deterministic versus judgment procedures. | addressed; movement criterion open |
| A05 | Federated control mesh and placement test keep core small and edge unbounded. | addressed |
| A06 | C2 plus registries form new capabilities without common-schema redesign. | addressed |
| A07 | First slice below exercises a thin end-to-end path. | addressed |
| A08 | C12 reconstructs pinned Attempt state independent of session/model. | addressed |
| A09 | C3 separates graduated initiative from C10 effect authority. | addressed; tier taxonomy provisional |
| A10 | C11/C12 safe-stop and resume; C9 prevents partial-as-complete. | addressed |
| A11 | C5 provides governed, provenance-bearing, corrected memory distinct from transcripts. | addressed |
| A12 | C6 produces milestone/daily/exception views from attributable records. | addressed |
| A13 | C8/C10/C13 expose replaceable assurance seams without semantic change. | addressed |
| A14 | C2 discovers Skills and C11 composes scoped teams through Roles/Delegations. | addressed |
| A15 | C9 pins baseline/proof bar, represents missingness, and isolates assessment. | addressed |
| A16 | C11/C12 coordinate locally; C6 cannot schedule. | addressed |
| A17 | C6 contract preserves source/evidence references across local state models. | addressed; minimum status schema open |
| A18 | C7 uses versioned, evolvable routes/classes/acknowledgements. | addressed |
| A19 | C4 allocates, C14 consumes/reports, C13 meters model usage. | addressed; accounting unit open |
| A20 | C3 classification binds autonomy, effects, budget, gates, reporting, escalation per program/risk. | addressed; risk taxonomy open |
| A21 | C7 supports project demand and garage finding delivery/disposition without fixed theme cardinality. | addressed |
| A22 | C1 publishes and C8 resolves the applicable operating model. | addressed |
| A23 | C8 checks extensions against C1 invariants. | addressed; extension compatibility rules open |
| A24 | C8 instruction/context delivery, C9 conformance evidence, and C10 effect enforcement are separate. | addressed |
| A25 | C8 pins approved copies and detects drift; C12 records governing baseline per Attempt. | addressed; staleness policy open |

No assumption is unresolved at component-placement altitude. Provisional taxonomies and policies remain owner decisions or empirical questions as listed below.

## First autonomy capability slice

The smallest coherent slice is **one owner-authorized research theme loop in one project repository, with a fixed budget and daily-or-milestone centralized reporting**.

Minimum logical path:

1. C1 publishes one immutable collective baseline; C8 pins it for the project.
2. C3 issues one bounded research Delegation with no consequential effect grants, an expiry, escalation rules, and an envelope allocated by C4.
3. C11 creates one Unit and resumable Attempts; C12 records transitions, residue, next action, and governing baselines.
4. C13 routes bounded reasoning and C14 accounts usage.
5. C9 assesses completion claims against the existing garage proof bar; C5 admits eligible findings without treating storage as truth.
6. C6 receives normalized status and emits daily, milestone, exception, blocked, and completion views.
7. C7 can deliver a finding to one addressed project and capture acknowledgement/disposition.

The slice deliberately omits autonomous effect execution: C10 may exist initially as a refusal-only boundary. This tests continuity, budget discipline, problem alignment, reporting, and cross-project delivery—the owner's named early risks—before granting material effect authority. It is a conceptual priority, not a BUILD recommendation or implementation plan.

## Conforming and non-conforming examples

### Conforming

An owner selects the `workflow-harness` theme for a bounded loop and grants a research coordinator a resource ceiling and expiry. The local cell pins operating-model baseline `B17`, Workflow `W4`, Gate `G9`, and Delegation `D22`; records Attempt `A61`; routes three reasoning Units through two eligible model targets; and records usage against `D22`. At the daily boundary it reports progress, spend, one surprise, unresolved residue, and evidence links. A proposed finding is independently assessed under `G9`, admitted as a claimed Record with provenance, then addressed through C7 to a delivery project. That project acknowledges and records “accepted for triage.” A later stop moves `A61` to hold with its next admissible action. No effect credential is exposed to the executor and no incomplete claim becomes complete.

### Non-conforming

An agent reads an unversioned rules file, chooses its own budget, edits its Gate when evidence is missing, calls a provider directly, marks its output proven, writes a summary into shared memory, assumes every project has received it, and pushes a consequential change with repository credentials. Its dashboard says complete but links no Unit, Attempt, baseline, Delegation, assessment, or effect disposition. This violates R2–R8 and R10–R12; instruction receipt, shared storage, and the agent's own completion statement enforce nothing.

## Evolution seams

- **Operating-model realization:** centralized repository first is compatible with later replicated or federated publication because C1 exposes immutable baselines and C8 owns resolution/caching.
- **Program topology:** Program initially maps conveniently to a repository execution cell, but Scope identity and C7 addressing permit one Program across repositories or several Programs in one repository.
- **Communication semantics:** event classes, routes, acknowledgement, delivery guarantees, and escalation evolve behind C7's versioned contract.
- **Memory realization:** C5 may extend or replace storage and retrieval mechanisms while preserving Record/Event admission and provenance semantics.
- **Model estate:** C13 absorbs public, private, and local targets without changing Workflows or Units.
- **Assurance:** C8, C9, C10, and C13 can strengthen identity, isolation, information-flow, credential, and attestation mechanisms without redefining Actor, Delegation, Gate, or Record.
- **Autonomy/risk:** C3 can introduce evidence-based tiers and program/effect risk classes without coupling initiative to effect grants.
- **Budgeting:** C4/C14 can move from coarse activity envelopes to richer currencies and allocation cadences without scheduling local Units.
- **Capability growth:** C2 registries/catalogs add domains, Skills, Workflows, and unit kinds without expanding the common core by default.
- **Reporting:** C6 can evolve views and cadence while the normalized semantic minimum and source authority remain stable.

## Strongest objection

The model may distribute one conceptual control surface into too many independently custodied boundaries before there is operational evidence that each separation earns its coordination cost. In particular, C1/C2/C3/C4 could initially appear as one owner-maintained definition surface, and C8/C9/C10 could appear as one program gateway. The counterweight is that the logical separations correspond to different powers—define meaning, allocate authority, assess evidence, and perform effects—and merging their interfaces must not merge their custody or permit the governed actor to reach the check. The unanswered part is which separations require distinct implementation boundaries at each risk tier; this architecture does not claim that answer.

## Deliberately left out

- Vendor, product, library, protocol, file format, database, transport, scheduler, runtime, identity provider, or repository-host choice.
- Physical, deployment, process, tenant, network, and high-availability topology.
- Ratification of V5 OPEN constructs, the seven-core-entity hypothesis, autonomy A3/A4, or any taxonomy.
- A universal project lifecycle, proof bar, status vocabulary, or one-theme-per-project rule.
- Detailed implementation sequence, estimates, staffing, external spend, POC, BUILD recommendation, grade, or proof claim.
- Automatic portfolio optimization or autonomous strategic priority setting.

## Owner questions and unresolved design decisions

1. What minimum normalized status must every program publish: Unit/Attempt identity, governing baselines, disposition, next action, budget consumed/remaining, risks, decisions, evidence links, and last update—or a smaller set?
2. Is a daily report composed once for the collective, per Program, or per active Delegation, and which events always trigger an immediate exception report?
3. At first, is the resource envelope attached primarily to a theme/Mission, Program, Unit, or calendar period? How are nested ceilings reconciled?
4. Who resolves portfolio contention: the owner alone, a delegated portfolio Role within fixed policy, or deterministic priority rules with owner exceptions?
5. What exact changes count as consequential effects in the first project repositories? Are commits, branches, issues, pull requests, external messages, and graph writes separate effect classes?
6. What staleness is permitted for an approved operating-model copy at each risk tier, and which changes force an active Attempt to hold rather than merely report drift?
7. Which common invariants must be mechanically checked in the first slice, versus documented with an explicit “not enforced” status?
8. What is the receiver's required disposition vocabulary for cross-program findings and requests, and when is acknowledgement mandatory?
9. Should research findings be able to create a proposed project Unit directly, or only a communication Event that a project authority may accept into work?
10. What evidence should increase or reduce research autonomy, and who has authority to revise the tier?
11. Which information classes may never cross C13 to publicly served models, even when the Delegation has budget?
12. Is owner STOP required to halt only new work initiation, all model calls, pending effect requests, or each of these with different safe-boundary rules?

## Claim boundary

This document defines a coherent candidate logical architecture. It is **claimed**, not evidence that the boundaries are feasible, sufficient, secure, economical, implemented, or proven. Each enforcement statement naming “no common checker exists today” is an explicit design gap, not an implied control.
