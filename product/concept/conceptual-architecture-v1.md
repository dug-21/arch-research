# Conceptual Architecture V1 — Converged Candidate

**Status:** directional specification; `claimed`, not ratified, implemented, validated, or proven  
**Run:** wfh-012  
**Inputs:** the two independent component models, A01–A25, `target-concept-v1.md`, organizational-data-model V5, and the `workflow-harness` theme

## 1. Objective

Define a logical architecture that lets centralized human intent become distributed, repository-local work while preserving collective rules, cross-program learning, durable memory, budget discipline, trustworthy reporting, rapid redirection, and consequential authority outside the actors being governed.

The converged shape is a **collective control plane joined by federated contracts to repeatable program execution cells**. “Collective,” “federated,” and “program-local” describe custody and authority, not products, processes, hosts, repositories, stores, or deployment.

An LLM is a replaceable execution target, not the authority root. A repository is the first practical carrier of a program cell, not the definition of a Program. No collective component schedules every local Unit.

## 2. Logical topology

```text
                           OWNER / COLLECTIVE AUTHORITY
                                      |
          +---------------------------+---------------------------+
          |                           |                           |
   Operating Model &          Portfolio Direction        Effect Authority
   Organization Registry        and Envelopes               Boundaries
          |                           |                           ^
          +------------- immutable definitions -----------------+
                                      |
                     federated contracts and projections
          +---------------------------+---------------------------+
          |                           |                           |
    Communication              Governed Memory            Portfolio View
      Exchange                    Admission                and Reporting
          ^                           ^                           ^
          |                           |                           |
  +-------+---------------- Program Execution Cell --------------+-------+
  | Context & Conformance | Local Coordination | Continuity Ledger       |
  | Team Formation        | Model Mediation    | Resource Accounting     |
  | Evidence Assessment   | Status Publisher  | Effect-request endpoint |
  +---------------------------------------------------------------------+
```

The collective plane stays small because Programs own Workflows, local state, and reversible execution. It centralizes only shared meaning, authority roots, portfolio scarcity, institutional admission, consequential effect custody, and owner-wide visibility.

## 3. Architectural rules

| ID | Constraint | Provenance | Enforcement point, location, and reachability | Present reality |
|---|---|---|---|---|
| R1 | Common intent, semantics, institutional memory, consequential decisions, and authority policy are centralized; reasoning, planning, communication, and reversible execution are distributed. | **Derived:** A05, A16, target concept. | Operating-Model Authority classifies definitions; Program Conformance checks local manifests. A Program may propose but cannot publish the accepted collective baseline. | No common checker. |
| R2 | Operating definitions, operational state, admitted knowledge, reporting projections, and effect authority remain separate logical planes. | **Derived:** A02, A11, A24, theme operations ≠ knowledge. | Plane-specific admission interfaces and custodians check crossings. Governed Actors can request crossings but cannot self-admit knowledge, self-accept claims, or mint effect authority. | Fragmentary enforcement only. |
| R3 | Every Attempt pins its Unit baseline, Workflow, Delegations, relevant Gates, and collective operating-model baseline. | **Adapted:** V5 Attempt/Gate/Delegation plus A08/A25; adds collective baseline. | Context & Conformance and Continuity Ledger reject start/resume without exact references; the executor cannot amend accepted pins. | No ecosystem-wide checker. |
| R4 | Autonomy grants initiative, never effect authority. Every consequential effect requires independent disposition. | **Derived:** A02, A09, A20, V5 I12/I17. | Effect Authority Boundary validates chain, effect class, target, time, revocation, and ceiling immediately before effect. The requester cannot mutate or bypass it. | No common boundary. |
| R5 | Completion or consequential claims cross acceptance only through a pinned Gate; missing evidence or independence fails closed. | **Derived:** A04, A15, A24, V5 I6–I9. | Evidence Assessment checks eligible evidence, missingness, baseline, procedure, and assessor read/write independence outside the executor's custody. | Garage firewall covers one domain only. |
| R6 | Cross-program delivery is addressed, attributable, acknowledged when required, and dispositioned; shared storage is not delivery. | **Authored:** A03, A18, A21 and V5 communication Event. | Communication Exchange validates sender authority, destination, contract version, and acknowledgement rule. Sender cannot forge receiver acknowledgement. | No common exchange. |
| R7 | Central reporting is a projection, not a scheduler or authoritative store of local work. Silence, staleness, and missing evidence are explicit. | **Authored:** A12, A16, A17. | Local Status Publisher must link normalized claims to source state/evidence; Portfolio View cannot mutate Units. Consequential reliance may require independent verification. | No common contract/checker. |
| R8 | Resources are allocated centrally enough to express portfolio priority and consumed locally without central scheduling. | **Authored:** A19/A20. | Portfolio Direction issues immutable envelopes; Resource Accounting and Model Mediation refuse or escalate exhaustion. Executor can inspect but not enlarge the ceiling. | No common mechanism. |
| R9 | Deterministic checks carry all semantics they can decide; judgment is declared, attributable, and isolated. | **Derived:** A04 and V5 `Gate.procedure`. | Pinned Gate declares procedure; Evidence Assessment records actual procedure/assessor. Governed Actor cannot relabel the Gate. | Migration criterion remains open. |
| R10 | Program extensions can add registered concepts but cannot redefine collective identities, relations, or invariants. | **Derived:** A22–A25 and V5 I19. | Conformance compares extension to pinned baseline and fails or reports drift under compatibility policy. Program cannot self-issue collective-compatible status. | No common checker. |
| R11 | Stop, hold, redirect, and recovery preserve attribution and partial outputs without converting them into completion. | **Derived:** A08/A10 and V5 Attempt/I15. | Local Coordination stops initiation; Effect Boundary refuses revoked effects; Continuity Ledger writes disposition/resume state; Evidence Assessment controls acceptance. | No common stop mechanism. |
| R12 | Storage, admission, truth, grade, currentness, and effect occurrence remain independent; correction never overwrites history. | **Derived:** A11/A15 and V5 I1–I5/I8/I9. | Governed Memory applies category admission and supersession outside submitter custody. | Unimatrix enforces fragments, not the full common contract. |
| R13 | Model routing is outside the routed request and obeys information policy and budget. | **Derived:** A01/A13/A19. | Model Mediation ignores target-selection instructions in payload, applies pinned policy, and records actual route/use. Target cannot mutate routing policy. | No common mediation layer. |
| R14 | Baseline drift never silently changes an active Attempt. | **Authored:** A18/A23/A25. | Context & Conformance compares pinned/current baselines and applies declared continue/report/hold policy. Program cannot alter the authoritative comparison target. | No common checker. |

## 4. Logical components

### C1. Collective Authority and Intent

Establishes Collective and Program Scopes, authority roots, strategic Goals, consequential decisions, autonomy/risk posture, and authority to grant, revoke, stop, or redirect work. It does not execute Program work.

**Placement:** collective. **V5:** `Scope`, `Goal`, `Delegation`, decision/adaptation `Event`. **Provenance:** **derived** from A02/A05/A09/A20 and target §§Structure/Governance.

### C2. Operating-Model Authority and Publication

Custodies and publishes immutable, identifiable baselines containing shared vocabulary, invariants, extension points, authority rules, evidence rules, and communication/reporting obligations. Resolves applicability metadata and accepts authorized adaptations without editing prior baselines.

**Placement:** collective authority; read-only approved copies at Programs. **V5:** custody of common registries, catalogs, values, I1–I19, and common parts of `Workflow`, `Skill`, `Role`, `Gate`, `Delegation`. **Provenance:** **authored convergence** of both tracks' authority/publication split, resting on A22–A25 and V5 I18/I19. A centralized rules repository is one candidate realization only.

### C3. Organization, Capability, and Team Registry

Makes Scopes, Goals, Capabilities, Actors, Skills, Roles, Workflows, Gates, and Technologies discoverable; registers permitted extensions; finds evidence-bearing skill matches; and supports formation of deliberately cross-disciplinary teams and new capabilities without a new common entity.

**Placement:** collective discovery with Program-owned entries/composition. **V5:** all named constructs above plus team `Scope` and catalogs. **Provenance:** **adapted** from V5 and A06/A14/A23; adds dissimilar-skill composition queries without making matching authority.

### C4. Portfolio Direction and Resource Allocation

Turns owner priorities into versioned resource envelopes for Programs, Missions, themes, Units, or time windows; declares exhaustion, exception, and reporting policy; resolves competition for scarce model use. It allocates but never sequences Program Units.

**Placement:** collective decision responsibility; local consumption. **V5:** `Goal`, `Scope`, `Delegation.resource_ceiling`, decision `Event`. **Provenance:** **authored** from A19/A20 and owner budget direction.

### C5. Program Context and Conformance

Resolves the applicable collective baseline, Program extension, Workflow, Delegations, Gates, envelope, memory references, and obligations before start/resume; supplies an approved local copy during publication outage; evaluates compatibility and drift; never treats instruction receipt as conformance.

**Placement:** federated contract with Program-local resolver and collective comparison authority. **V5:** `Scope`, `Workflow`, `Delegation`, `Gate`, `Attempt.baseline_ref`, adaptation `Event`. **Provenance:** **authored** from A08/A13/A22–A25.

### C6. Authority and Delegation Administration

Creates standing/dynamic Delegations rooted in Scope, evaluates attenuation, binds autonomy, risk, effect grants, resource ceilings, expiry, escalation, revocation, and sub-delegation. It declares authority but performs no effect.

**Placement:** collective or independently custodied Program authority, never the governed Attempt. **V5:** `Scope`, `Role`, `Delegation`, I12/I17/I18. **Provenance:** **derived** from A02/A09/A20.

### C7. Local Execution Coordination and Team Formation

Turns authorized Goals/Missions into Workflow-governed Units and Attempts; composes Actors/Roles/Skills; sequences dependencies; selects admissible next transitions; responds to stop/redirect; preserves partial outputs; and proposes new capability formations. It cannot alter its governing baseline, Delegation, Gates, or effect credentials.

**Placement:** Program/repository-local. **V5:** `Goal`, `Capability`, `Actor`, `Skill`, `Role`, `Workflow`, `Unit`, `Attempt`, `Delegation`, transition `Event`. **Provenance:** **adapted** from A06–A10/A14/A16 and V5 I10/I15–I18.

### C8. Local Continuity Ledger

Holds authoritative operational state needed for another authorized Actor to reconstruct work: identities, pinned baselines, progress, transitions, disposition, resource use, unresolved residue, pending acknowledgements, partial outputs, safe boundary, and next admissible action. It references knowledge but is not institutional memory or a transcript archive.

**Placement:** Program-local, durably accessible across sessions. **V5:** `Unit`, `Attempt`, operational `Event`s and category-governed operational `Record`s. **Provenance:** **authored** from A08/A10/A11/A17/A25 and operations ≠ knowledge.

### C9. Model Mediation and Target Adapters

Selects a deterministic component, public model, or locally operated model for a bounded request according to declared work needs, information policy, envelope, availability, and routing policy; invokes it through a stable boundary; reports actual route, resource use, and failure while hiding target identity from Workflow semantics.

**Placement:** Program edge with independently held policy; it may be shared without scheduling work. **V5:** `Actor`, `Technology`, observation `Event`. **Provenance:** **authored convergence** of router and adapter responsibilities from A01/A04/A13/A19.

### C10. Local Resource Accounting

Measures use by envelope, Delegation, Unit, Attempt, and model route; publishes consumed/remaining/unknown; and invokes declared exhaustion behavior. It cannot set priority or enlarge a ceiling.

**Placement:** Program-local meter with C4-controlled envelope. **V5:** `Delegation.resource_ceiling`, observation/exception `Event`. **Provenance:** **authored** from A12/A19/A20.

### C11. Assessment and Evidence Boundary

Evaluates identified Units, Records, Capabilities, or Events against pinned Gates; distinguishes observations, claims, assessments, outcomes, decisions, transitions, effects, and Records; checks evidence, missingness, procedure altitude, and assessor independence; emits assessment/outcome without making the later authority decision or effect.

**Placement:** federated; definition and assessment custody outside the governed executor. **V5:** `Gate`, `Record`, assessment/gate-outcome `Event`, I4/I6–I9. **Provenance:** **derived** from A04/A15/A24 and the garage firewall.

### C12. Effect Authority Boundary

The only logical performer/refuser for registered consequential effect classes. It validates the exact Delegation chain, Scope, target, risk, budget, expiry, revocation, and required gate outcome; retains credentials outside the Attempt; emits a distinct effect disposition with coupling.

**Placement:** independently controlled; logically collective even if physically near a Program. **V5:** `EffectBoundary`, `Delegation`, effect request/disposition `Event`, I12. **Provenance:** **derived** from A02/A09/A13/A20/A24.

### C13. Cross-Program Communication Exchange

Addresses, routes, receives, acknowledges, correlates, and dispositions research requests, findings, risks, proposed work, decisions, exceptions, and escalations across Scope boundaries. Contracts and routing are versioned. Delivery is neither truth, admission, acceptance, nor work creation.

**Placement:** federated endpoints with collective addressing semantics. **V5:** communication `Event` plus payload `Record`; because each Event has one Scope, cross-Scope delivery requires correlated send/receive Events or a future compatible extension. **Provenance:** **authored** from A03/A18/A21, explicitly preserving V5's delivery hole.

### C14. Governed Organizational Memory

Admits, retrieves, supersedes, and relates institutional knowledge while preserving provenance, epistemic kind, evidence altitude/grade, currentness, missingness, and correction history. Operational state enters only through category admission; storage alone establishes nothing.

**Placement:** centralized institutional substrate with scoped contribution/access. **V5:** `Record`, relevant `Event`, `Capability`, `Technology`, values, I1–I5/I8–I11. **Provenance:** **derived** from A03/A08/A11/A15/A21 and the theme memory boundary. Unimatrix is the intended substrate and may be extended, but is not made the orchestrator.

### C15. Local Status Publisher and Collective Portfolio View

The local responsibility derives a normalized, attributable projection from Units, Attempts, Events, Records, Delegations, budgets, decisions, risks, blocks, and evidence links. The collective responsibility composes daily, milestone, exception, and requested views; reports missingness, freshness, drift, and incompatible semantics; and preserves drill-down. Neither mutates Program work.

**Placement:** split local publisher / collective aggregator. **V5:** intentionally cross-cutting read model; durable summaries may be `Record`s and communications are `Event`s. **Provenance:** **authored convergence** from A12/A16/A17/A19/A25.

## 5. Principal interactions

1. **Establish and resolve.** C1 establishes Goal/Scope. C4 allocates priority/envelope. C5 pins the C2 baseline, Program extension, Workflow, Gates, and C6 Delegation.
2. **Form and execute.** C3/C7 find Skills and compose Actors/Roles. C7 creates Units/Attempts and C8 records transitions and resume state.
3. **Route reasoning.** C7 submits a bounded request to C9; C10 accounts use. Output returns as a claim or proposed artifact, never accepted completion.
4. **Assess.** C11 evaluates the pinned subject and evidence. Eligible knowledge crosses into C14 only through category admission.
5. **Cause effects.** C7 issues an effect request; C12 performs/refuses/records unknown and emits a separate disposition. Only the disposition demonstrates the enforced result.
6. **Communicate.** C13 emits sender- and receiver-side records with acknowledgement/disposition. C14 admission is optional and separate.
7. **Report and steer.** C15 publishes normalized local state and composes owner views. Redirection becomes a decision/adaptation and, where needed, revised Delegation or a new baseline—not mutation of an active Attempt.
8. **Interrupt/resume.** Stop reaches C7 and revocation reaches C12; C8 preserves partial state. A later Actor must re-resolve C5 and revalidate C6/C11 prerequisites before resuming.

## 6. Placement test

| A responsibility primarily… | Custody |
|---|---|
| defines common meaning, authority roots, portfolio priority, institutional admission, or owner-wide visibility | collective |
| reasons, sequences project work, maintains live state, consumes an envelope, or performs reversible local work | Program-local |
| transports claims or verifies compatibility between independent Scopes | federated contract with independently controlled endpoints |
| can cause a consequential external change | the C12 boundary controlling that effect, never the requester |

Convenience, reuse, or a shared runtime alone do not justify collective custody. A concern is split when collective authority and local operation are both required.

## 7. V5 placement

| Construct | Placement/treatment |
|---|---|
| `Scope` | Cross-cutting boundary/identity in C1–C15; Collective and Program anchor placement, Mission/Team support bounded composition. |
| `Goal` | C1 intent, prioritized by C4, pursued by C7; never Scope or Unit. |
| `Capability` | C3 definition/formation, delivered by C7, assessed by C11, evidenced in C14. |
| `Actor` | Cross-cutting participant identity used by C3/C6/C7/C9/C11/C12; declaration is not attestation/authority. |
| `Unit` | C7 durable local work identity and C8 state; projected by C15. |
| `Event` | Cross-cutting immutable occurrence in execution, assessment, effects, communication, adaptation, and memory. |
| `Record` | Cross-cutting durable information; C8 operational and C14 knowledge uses remain category-separated. |
| `Workflow` | Program-owned definition published/resolved by C2/C5 and executed by C7; custody outside governed Attempt. |
| `Skill` | C3 catalog/matching and C7 composition; competence only. |
| `Role` | C3 responsibility, C6 standing Delegation, C7 composition, C11 independence. |
| `Delegation` | Cross-cutting authority envelope C1/C4/C5/C6/C7/C9/C10/C12; never inferred from Role/autonomy. |
| `Gate` | C2 definition, C5 pinning, C11 assessment. |
| `EffectBoundary` | C12 exclusively. |
| `Attempt` | C7 execution, C8 continuity; never a Unit subtype. |
| `Technology` | C3/C14 evidence-bearing mechanism catalog and C9 target reference; no Capability/grade transfer. |
| Registries | C2 common admission; C3 operational catalog; C5 compatibility; Programs extend only declared seams. |
| Catalogs | C3 discovery with collective/Program ownership preserved. |
| Values | Cross-cutting semantics published by C2 and consumed by all relevant components; A3/A4 remain unratified. |
| I1–I19 | Cross-cutting baseline in C2, checked by C5 and component-specific enforcement; gaps remain explicit. |

All V5 exclusions remain excluded: Feature is a `unit_kind`; Qualification is Actor–Skill evidence; Envelope travels with Delegation; AuthorityBasis is Scope/Delegation; EvidenceItem is a Record role; RecordVersion belongs to identity history; Signal/Decision/Transition/Assessment/Outcome/EffectRequest/EffectReceipt are Event types; effect request/disposition do not merge; organizational level creates no Capability kind; Goal is not Scope; Attempt is not Unit; lesson is not an Event type; and no universal lifecycle, proof bar, closed taxonomy, or autonomy-as-authority/evidence is introduced.

## 8. Assumption traceability

| Assumption | Response | Status |
|---|---|---|
| A01 | C9/R13 provider-neutral external routing. | accommodated |
| A02 | C1/C6/C12; R2/R4. | accommodated |
| A03 | C13 addressed delivery, C14 learning. | accommodated; delivery semantics open |
| A04 | C9/C11 and R9. | accommodated; migration criterion open |
| A05 | topology/placement test. | accommodated |
| A06 | C3/C7 plus registries. | accommodated |
| A07 | first slice below and replaceable seams. | accommodated |
| A08 | C5/C7/C8. | accommodated |
| A09 | C6 initiative vs C12 authority. | accommodated; tier taxonomy provisional |
| A10 | C7/C8/C12 and interaction 8. | accommodated; safe-boundary classes open |
| A11 | C14 separate from C8. | accommodated |
| A12 | C15. | accommodated |
| A13 | C5/C9/C12 assurance seams. | accommodated; assurance policy open |
| A14 | C3/C7. | accommodated |
| A15 | C11/C14 and R5/R12. | accommodated |
| A16 | Program cell/C7/C8; C15 cannot schedule. | accommodated |
| A17 | C15 normalized attributable projection. | accommodated; minimum contract open |
| A18 | C13 versioned evolving contract and R14. | accommodated; deliberately evolutionary |
| A19 | C4/C9/C10 and R8. | accommodated; currency/hierarchy open |
| A20 | C6/C12 risk-specific grants. | accommodated; taxonomy open |
| A21 | C13/C14, no theme-project cardinality. | accommodated; work-creation rule open |
| A22 | C2/C5. | accommodated |
| A23 | C2/C5 and R10. | accommodated; compatibility rules open |
| A24 | C5 instruction, C11 evidence, C12 enforcement separated. | accommodated |
| A25 | C2/C5/C8/R3/R14. | accommodated; staleness policy open |

No assumption or V5 core/supporting construct is omitted. “Accommodated” is a design statement, not evidence that the assumption is true or the design works.

## 9. Conforming and non-conforming examples

### Conforming bounded research loop

The owner selects one research theme and issues a time-bounded Delegation with a model-use ceiling, no external spend, reversible repository-local effects only, daily/milestone reporting, and escalation on premise change. The Program pins exact operating-model, Workflow, Gate, and Delegation baselines; creates a resumable Unit/Attempt; routes requests through C9; meters use through C10; and records safe-resume state in C8. C11 independently assesses a proposed finding. C14 admits it with provenance and claimed epistemic status. C13 addresses it to a project, which acknowledges “accepted for triage.” C12 refuses any ungranted consequential effect.

### Non-conforming repository agent

An agent reads an unversioned rules file, selects its own model and budget, edits its Gate when evidence is missing, writes directly into shared memory, assumes storage delivered its finding everywhere, reports “proven,” and pushes a consequential change using repository credentials. No exact baseline, Delegation, independent assessment, acknowledgement, effect disposition, or resume state exists. Instruction receipt and narrative success enforce nothing; this violates R2–R14.

## 10. Recommended first bounded capability slice

The recommended conceptual slice is **one owner-authorized research-theme continuation loop in one repository, with a fixed model-use budget, safe cross-session recovery, normalized centralized reporting, and one acknowledged cross-program finding delivery**.

Minimum path:

1. Publish and pin one collective baseline and Program extension (C2/C5).
2. Grant one theme-scoped Delegation with expiry, escalation, no external spend, and only explicitly named reversible local effects (C6/C12).
3. Create/resume one Unit and Attempt with durable residue and next action (C7/C8).
4. Route bounded reasoning and account consumption (C9/C10).
5. Assess claims and admit eligible findings without upgrading them by storage (C11/C14).
6. Publish daily plus milestone/exception/blocked status with evidence links (C15).
7. Deliver one finding to one project and capture acknowledgement/disposition (C13).

This directly tests the owner's earliest risks—wasted model use and work on the wrong problem—plus rule discoverability, continuation, reporting, and repository-to-repository coordination. It excludes autonomous external spend, collective-rule changes, proof-grade changes, and foundational data-platform effects.

**Preserved disagreement:** one track recommends C12 exist initially as a refusal-only boundary; the other requires C12 logically but does not prescribe first-slice realization. The safer convergence recommendation is refusal-only if the slice can request any effect at all; if all possible effects are structurally absent, an explicit refusal implementation may be deferred. This is an owner/risk decision, not a feasibility claim or BUILD recommendation.

## 11. Evolution seams

- Replace operating-model publication/caching/compatibility mechanisms while preserving immutable baseline identity and custody.
- Evolve C13 message classes, routes, acknowledgement, delivery guarantees, and escalation behind versioned contracts.
- Extend or replace C14 storage/retrieval while preserving admission, provenance, grade, currentness, and supersession.
- Add public/private/local execution targets behind C9 without changing Workflow semantics.
- Strengthen identity, isolation, information flow, credentials, and attestation behind C5/C9/C11/C12.
- Refine autonomy tiers, risk classes, budgets, and reporting cadence without conflating initiative, evidence, or effects.
- Add Programs, Workflows, Skills, Roles, categories, event types, unit kinds, and effect classes through registration.
- Allow Program↔repository and theme↔Program cardinalities to change without topology redesign.
- Split or co-locate logical components physically without merging their custody or powers.

## 12. Material convergence decisions and disagreements

Both tracks independently converged on: a small collective core plus Program cells; centralized allocation but local scheduling; operations/knowledge/effect separation; explicit cross-program delivery; immutable baseline pinning; independent assessment; provider-neutral model mediation; durable recovery; and reporting as a projection.

Differences preserved rather than erased:

1. **Component granularity.** One track separated model router/adapter, operating authority/publication, status publisher/aggregator, and capability/team formation; the other grouped more of these. This document preserves distinct responsibilities but does not require distinct implementations.
2. **Organization registry placement.** One track treated formation as a dedicated capability; the other used a broad organization registry. C3/C7 split discovery/common identity from local composition.
3. **First-slice effect boundary.** Refusal-only versus logical-but-not-yet-realized remains risk-dependent as stated above.
4. **Central surface grouping.** C1–C4 may initially appear in one owner-maintained surface, but their powers—intent, semantics, organization discovery, and allocation—remain logically distinct.
5. **Program gateway grouping.** C5/C11/C12 may share a realization, but conformance, assessment, and effect custody must remain independently controlled where they bind the executor.

## 13. Strongest objection

The architecture may demand a common identity/reference discipline across baselines, Delegations, budgets, status, communications, evidence, and effects before a narrow feature feels useful. It may also create too many independently custodied boundaries before operating evidence proves their coordination cost is justified. Collapsing the semantics would erase real powers and create false enforcement. The unresolved question is which logical boundaries must become distinct implementation boundaries at each risk tier. Only a bounded operational trial can answer it; this document does not.

## 14. Deliberately left out

- Vendors, products, libraries, protocols, formats, stores, transports, runtimes, repository hosts, and deployment topology.
- Physical centralization, tenancy, networking, consistency, replication, availability, and disaster recovery.
- Ratification of V5 OPEN constructs, its seven-entity hypothesis, A3/A4, or any autonomy/risk taxonomy.
- Identity attestation, delegation attenuation algorithm, revocation propagation, final effect taxonomy, and information classification.
- A universal lifecycle, proof bar, status vocabulary, one-theme-per-project rule, or Program=repository rule.
- A decision that Unimatrix owns live operational state; it retains the governed durable-memory role.
- Feasibility, implementation detail, estimates, external spend, graph writes, grades, proof, product boundary, or BUILD recommendation.

## 15. Owner decisions

1. What is the minimum normalized status contract: Unit/Attempt, pinned baselines, disposition, next action, budget consumed/remaining, risks, decisions, evidence links, freshness—and can any be omitted?
2. Is the first envelope attached primarily to a theme/Mission, Program, time window, or nested hierarchy?
3. Who resolves portfolio contention: owner, delegated Role within policy, or deterministic rules with owner exception?
4. Which first-slice repository actions are consequential effect classes: working-tree edit, commit, branch, issue, pull request, external message, graph write?
5. Must C12 be visibly refusal-only in the first slice, or are all effect paths structurally absent?
6. Which events force immediate hold rather than report-and-continue?
7. What baseline staleness is allowed by risk tier, and which changes hold active Attempts?
8. When is cross-program acknowledgement mandatory, and what recipient dispositions are required?
9. May a garage finding create a proposed project Unit, or only a communication awaiting project acceptance?
10. Which information classes may never reach publicly served models?
11. What operating evidence increases or reduces autonomy, and who changes the tier?
12. Besides the owner, who may ratify collective operating-model changes?

## 16. Claim boundary

This is a converged candidate definition. Agreement between two design tracks is not evidence that it is feasible, safe, sufficient, economical, implemented, or proven. Every stated enforcement gap remains a gap until independently demonstrated.

