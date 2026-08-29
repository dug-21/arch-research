# Agentic Organization — Data Model

**Status:** working model  
**Updated:** 2026-08-28  
**Evidence:** directional · not implemented · not validated

Programs own their workflows, proof bars, Record categories, and domain extensions. The common model
owns identity, relationships, and the distinctions that must remain consistent across programs.

## Status

| Status | Meaning |
|---|---|
| **RESOLVED** | Accepted in the working model. |
| **OPEN** | Requires further resolution or broader testing. |

## Forms

| Form | Meaning | Status |
|---|---|---|
| **Entity** | A continuing thing with stable identity. | **RESOLVED** |
| **Event** | An immutable occurrence. | **RESOLVED** |
| **Value** | A classification or measurement without independent identity. | **RESOLVED** |
| **Derived** | Information produced from other Entities, Events, Records, or Values. | **RESOLVED** |

## Core entities

| Entity | Form | Definition | Identity | Status |
|---|---|---|---|---|
| **Scope** | Entity | An organizational boundary within which work, authority, and information apply. | `scope_id` | **OPEN** |
| **Goal** | Entity | An intended outcome that defines what must become true. | `goal_id` | **RESOLVED** |
| **Capability** | Entity | An observable behavior required by at least one Goal. | `capability_id` | **RESOLVED** |
| **Actor** | Entity | A human, agent, service, or deterministic component participating in work or effects. | `actor_id` | **OPEN** |
| **Unit** | Entity | One durable, attributable piece of work with a defined intended outcome. | `unit_id` | **OPEN** |
| **Event** | Event | An immutable occurrence within an identified Scope. | `event_id` when consequential | **RESOLVED** |
| **Record** | Entity | Durable information governed by an extensible Category. | `record_id` | **OPEN** |

## Scope

**Status:** **OPEN**

Candidate types:

| Type | Definition |
|---|---|
| `collective` | The complete organization under one human authority root. |
| `program` | A durable area responsible for an objective and continuing body of work. |
| `mission` | A bounded organizational effort formed to achieve an outcome. |
| `team` | A bounded composition of Actors formed within another Scope. |

Essential relationships:

- Scope `contains` Scope.
- Scope `owns` Goal.
- Scope `scopes` Capability, Unit, Event, and Record.
- Scope type changes organizational boundary, not the meaning of related entities.

Open:

- type-specific fields;
- nesting constraints;
- federation between Collectives;
- authority-root succession.

## Goal

**Status:** **RESOLVED**

Essential properties:

- statement;
- Scope;
- required Capabilities;
- success criteria;
- claim floor;
- north star;
- lifecycle state;
- current version.

Essential relationships:

- Goal `requires` Capability.
- Goal may be `advanced-by` additional Capabilities that are contributory but not required.
- Goal `directs` Unit without becoming the Unit's Scope.

## Capability

**Status:** **RESOLVED**

> A Capability is an observable behavior required by at least one Goal and delivered by Features and/or
> enabled by Technologies.

Essential properties:

- observable behavior;
- Scope;
- requiring Goals;
- `done_when`;
- evidence grade;
- provenance;
- current version.

Essential relationships:

- Capability `composed-of` Capability.
- Capability `prerequisite-of` Capability.
- Feature `delivers` Capability.
- Technology `enables` Capability.

Invariants:

- Organizational level changes Scope and composition, never meaning.
- Every component Capability remains independently observable.
- A parent Capability clears only its own `done_when`.
- Feature delivery and Technology enablement do not prove a Capability.
- Actor competence is a Qualification, not a Capability.

Open:

- recursive evidence rollup;
- parent and child `done_when` interaction;
- Scope expiry.

## Actor

**Status:** **OPEN**

Essential properties:

- Actor type: `human | agent | service | deterministic-component`;
- identity and identity provenance;
- assigned Roles;
- Qualifications;
- active Delegations.

Invariants:

- Actor identity, autonomy, authority, and evidence are independent.
- Self-declared identity supports reconstruction but does not establish accountability.
- Qualification does not grant authority.

Open:

- identity attestation;
- replacement and continuity;
- composite Actors.

## Unit

**Status:** **OPEN**

Essential properties:

- Unit kind;
- intended outcome;
- one primary Scope;
- related Goals;
- dependencies;
- inputs and outputs;
- workflow and current state;
- baseline;
- current Attempt.

Essential relationships:

- Unit `depends-on` Unit.
- Unit `has` Attempt.
- Unit `consumes` Record.
- Unit `produces` Record.
- Unit is `assigned-to` Actor through a Delegation.

Invariants:

- Retry and rework create Attempts under the same Unit.
- A changed intended outcome creates a new Unit related by `replaces` or `derived-from`.
- Workflow owns Unit kinds, states, transitions, and gate consequences.

Open:

- common Unit kinds;
- interruption and resume requirements;
- concurrent Attempts.

## Event

**Status:** **RESOLVED**

Essential properties:

- Event type;
- occurred time;
- recorded time;
- Scope;
- Actors;
- subjects;
- related Unit and Attempt;
- authority reference when consequential;
- provenance and custody;
- causal and correlation references.

Candidate Event types:

| Type | Definition | Status |
|---|---|---|
| `communication` | Information is conveyed between Actors, Roles, or Scopes. | **OPEN** |
| `decision` | An authority holder selects a consequential disposition. | **OPEN** |
| `observation` | A fact is mechanically captured from an identified source. | **OPEN** |
| `assessment` | A subject and baseline are evaluated under a Gate. | **OPEN** |
| `transition` | A Unit moves between workflow-owned states. | **OPEN** |
| `effect` | An effect is requested, performed, refused, or remains unknown. | **OPEN** |
| `adaptation` | An authorized change modifies an organizational definition, baseline, composition, or process. | **OPEN** |

Invariants:

- Events are immutable.
- Correction creates another Event; it does not rewrite the occurrence.
- Event existence does not establish payload truth.
- An Actor-authored account is not a mechanical observation.
- `occurred_at` and `recorded_at` are distinct.
- Event type selects an extension schema; it does not create another core noun.

Open:

- which Events require durable identity;
- Event admission and retention;
- ordering and clock semantics;
- Event type registry.

## Record

**Status:** **OPEN**

Essential properties:

- Category and Category schema version;
- Scope;
- author or source;
- content digest;
- provenance;
- evidence kind and altitude;
- lifecycle state;
- currentness;
- supersession;
- related Events and effects;
- explicit missing or unavailable references.

Invariants:

- Record existence, admission, truth, evidence grade, currentness, and effect occurrence are independent.
- Categories are extensible and own schema, admission, retrieval, lifecycle, and correction rules.
- A Record may document an Event without becoming the Event.
- Correcting a Record does not change the Event it documents.

Open:

- common Category configuration contract;
- Record admission rules;
- `lesson-learned` versus `pattern` Category boundary.

## Supporting definitions

These support the core model without becoming core organizational nouns.

| Definition | Form | Meaning | Owner | Status |
|---|---|---|---|---|
| **Attempt** | Entity | One execution of a Unit against an identified baseline. | Workflow | **OPEN** |
| **Role** | Entity | Reusable responsibility and Qualification requirements. | Program | **OPEN** |
| **Qualification** | Entity | Evidenced claim that an Actor satisfies an assignment requirement. | Program | **OPEN** |
| **Skill** | Entity | Versioned reusable method for performing a class of work. | Collective or Program | **OPEN** |
| **Workflow** | Entity | Versioned program-owned definition of Unit kinds, dependencies, states, transitions, Gates, and transition consequences. | Program | **OPEN** |
| **Delegation** | Record or relation | Assignment of a Unit to an Actor with decision latitude, allowed effects, resource ceilings, and escalation conditions. | Program or Workflow | **OPEN** |
| **Gate** | Entity or Workflow rule | Rule for evaluating a subject and deciding whether a boundary may be crossed. | Program, Workflow, or Record Category | **OPEN** |
| **Feature** | Program extension | Bounded delivery change intended to provide Capability behavior. | Program | **OPEN** |
| **Technology** | Program extension | Reusable mechanism that may enable Capability behavior. | Program | **OPEN** |

### Delegation

A Delegation answers:

- Who is assigned?
- What Unit and Scope apply?
- How much initiative may the Actor exercise?
- Which effects and resources are allowed?
- Who can enforce those limits?
- When must the Actor stop or escalate?
- When does the Delegation expire?

Autonomy describes initiative. It does not grant effects. A Delegation declaration does not demonstrate
that its limits are enforced.

### Gate

A Gate answers:

- What subject and baseline are evaluated?
- Which evidence is eligible or required?
- Who evaluates it?
- What independence is required?
- What outcomes are possible?
- What happens for each outcome?
- What durable Record is required?

Assessment and outcome are Events. Evidence, outcome, decision, transition, effect, and Record remain
distinct.

## Common values

### Autonomy

**Status:** **OPEN**

Decision and initiative latitude. Autonomy is independent of effect authority and evidence.

| Tier | Meaning | Status |
|---|---|---|
| `A0` | Analyze, evaluate, or recommend without discretionary work initiation. | **OPEN** |
| `A1` | Exercise bounded judgment within an assigned Unit. | **OPEN** |
| `A2` | Plan and delegate within an approved Mission. | **OPEN** |
| `A3` | Adapt local tactics, team composition, or reversible workflow detail. | **OPEN** |
| `A4` | Select and launch Missions within an approved Program. | **OPEN** |
| `A5` | Change Collective policy, authority structures, or strategic objectives. | **OPEN** |

### Evidence grade

**Status:** **RESOLVED**

- `missing`
- `claimed`
- `partial`
- `proven`

`proven` requires evidence at the claim's altitude demonstrated by the organization.

## Core relationships

| Source | Relationship | Target | Status |
|---|---|---|---|
| Scope | contains | Scope | **OPEN** |
| Scope | owns | Goal | **OPEN** |
| Scope (`program`) | owns | Workflow | **OPEN** |
| Goal | requires | Capability | **RESOLVED** |
| Goal | directs | Unit | **OPEN** |
| Capability | composed-of | Capability | **OPEN** |
| Capability | prerequisite-of | Capability | **RESOLVED** |
| Actor | has | Qualification | **RESOLVED** |
| Role | requires | Qualification | **RESOLVED** |
| Delegation | assigns | Actor to Unit | **OPEN** |
| Workflow | defines | Unit kinds, dependencies, states, transitions, and consequences | **OPEN** |
| Workflow | uses | Gate | **OPEN** |
| Unit | follows | Workflow | **OPEN** |
| Unit | has | Attempt | **RESOLVED** |
| Unit | depends-on | Unit | **OPEN** |
| Unit | consumes or produces | Record | **RESOLVED** |
| Event | concerns | Entity or Event | **RESOLVED** |
| Event | caused-by | Event | **RESOLVED** |
| Event | correlated-with | Event | **RESOLVED** |
| Event | documented-by | Record | **RESOLVED** |
| Record | documents | Event | **RESOLVED** |
| Event (`transition`) | conforms-to | Workflow | **OPEN** |
| Gate | evaluates | Entity, Event, Record, Capability, or Unit | **OPEN** |

## Invariants

1. Identity, type, Scope, version, state, Category, currentness, provenance, and relation are distinct.
2. Autonomy, effect authority, and evidence are independent.
3. Capability meaning does not change with organizational level.
4. Actor competence is Qualification, never Capability.
5. Feature delivery and Technology enablement do not prove Capability.
6. Unit identity survives retry and rework; each execution is an Attempt.
7. Event and Record are distinct.
8. Record existence, admission, truth, grade, currentness, and effect occurrence are distinct.
9. Actor disclosure is not mechanical observation.
10. Missing evidence is represented and never inferred as success.
11. Evaluation outcome, decision, transition, effect, and Record are distinct.
12. No program extension may weaken these invariants.

## Excluded

- organizational-level Capability kinds;
- Goal as an organizational Scope;
- Attempt as a Unit subtype;
- Signal or Decision as a separate core noun;
- lesson as an Event type;
- one universal lifecycle or state machine;
- closed Event, effect, or Record Category taxonomies;
- autonomy tier as effect authority or evidence strength;
- a universal proof bar.

## Open decisions

| Question | Affected definitions |
|---|---|
| Which fields and constraints belong to each Scope type? | Scope |
| Is Skill distinct from Qualification in identity and behavior? | Skill, Qualification |
| Is Feature a common extension or a software-specific Unit/Mission form? | Feature, Unit |
| Which Workflow properties are common structure versus Program-owned extensions? | Workflow, Unit, Gate |
| Does Gate require durable identity, or is it always a versioned Workflow/Category rule? | Gate, Event, Record |
| Is Delegation a durable Record, a relation, or both? | Delegation, Actor, Unit |
| Which Events require durable identity and Record admission? | Event, Record |
| Is `lesson-learned` behaviorally distinct from `pattern`? | Record |
| Which autonomy tiers survive broader domain tests? | Actor, Role, Delegation |
| What common effect vocabulary can be enforced across Programs? | Delegation, Event |
