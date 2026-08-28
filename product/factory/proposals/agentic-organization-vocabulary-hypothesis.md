# Agentic Organization Vocabulary — Working Hypothesis and Test

**Status:** working hypothesis · owner-aligned 2026-08-28 · not decomposed · not validated
**Theme:** `workflow-harness` *(theme objective pending formal revision)*
**Purpose:** test whether a small common vocabulary can make a distributed agentic organization
manageable across unlike programs without erasing their meaningful differences.

## Target concept

Build a continuously improving agentic organization that turns centralized human intent into distributed,
governed execution, preserves learning across its programs, and can safely create capabilities it does not
yet possess.

The organization centralizes **intent, constraints, consequential decisions, and institutional memory**.
It distributes **reasoning, exploration, planning, communication, and reversible execution**. Shared
organizational intelligence does not imply one omniscient context or an emergent authority root.

The initial operating domains are the research garage and software-product delivery. The intended future
domain is open-ended. Jurati is a candidate implementation component whose boundary should emerge from
the operating model; it is not the premise or required answer.

## H1 — A small organizational vocabulary is sufficient

> A common vocabulary of nine durable nouns, eight lifecycle verbs, three independent governance axes,
> and a small signal taxonomy can express both research-garage and software-delivery work without
> domain-specific exceptions in the common layer.

If true, programs may define different workflows while sharing one organizational protocol. The common
layer supplies identity, delegation, communication, evidence, and governance semantics; a program supplies
its domain-specific activities and proof bars.

### Nine nouns

| Noun | Proposed meaning |
|---|---|
| **Collective** | The whole organization under one human authority root. |
| **Program** | A durable area of responsibility with an objective and operating boundaries. |
| **Mission** | A bounded outcome the collective has chosen to pursue. |
| **Capability** | An assignable behavior the collective has evidence about. |
| **Unit** | One attributable piece of work with identity, lifecycle, inputs, and outputs. |
| **Actor** | A human, agent, service, or deterministic component performing a unit. |
| **Envelope** | The scope, effects, resources, and escalation conditions delegated to an actor. |
| **Signal** | Typed information communicated between actors or programs. |
| **Record** | Durable evidence of intent, action, decision, outcome, or learning. |

The common lifecycle verbs are:

`direct → form → delegate → execute → observe → verify → learn → adapt`

Terms such as team, role, workflow, gate, and tool remain useful but are derived rather than irreducible:

- a **team** is a temporary set of actors formed for a mission;
- a **role** is a reusable capability-and-envelope template;
- a **workflow** defines units, dependencies, and transitions;
- a **gate** is a deterministic condition on a consequential transition;
- a **tool** is an effect interface admitted through an envelope.

### Three independent governance axes

The model must not collapse these into one scale:

1. **Autonomy** — how much judgment and initiative an actor may exercise.
2. **Authority** — which effects and resources the actor may cause or consume.
3. **Evidence** — how strongly the organization has established that a capability or claim works.

An autonomous coordinator may have little effect authority. A deterministic deployment service may hold
powerful credentials while possessing no autonomy. A highly trusted claim does not grant its author more
authority.

### Candidate autonomy tiers

| Tier | Standard decision latitude |
|---|---|
| **A0 — Advise** | Analyze and recommend; cause no effects. |
| **A1 — Act reversibly** | Perform bounded, reversible work; make no consequential publication or commitment. |
| **A2 — Execute mission** | Plan and delegate within an approved mission and envelope. |
| **A3 — Adapt locally** | Change tactics, team composition, and reversible workflow details using evidence. |
| **A4 — Operate program** | Select and launch missions within approved program strategy and budget. |
| **A5 — Govern collectively** | Change organizational policy, authority structures, or strategic objectives. |

The owner initially retains A5. A tier is shorthand for decision latitude, never a substitute for an
explicit envelope. Specific governance powers might later be narrowly delegated; general authority to
redefine the collective's authority root is not implied by this ladder.

Every delegation therefore states at least:

```yaml
autonomy: A2
scope:
  program: <program>
  mission: <mission>
effects:
  reversible: allowed
  irreversible: denied
resources:
  spend: <ceiling>
  concurrency: <ceiling>
escalate:
  - strategic_change
  - security_surprise
  - irreversible_effect
  - evidence_grade_change
```

### Candidate signal classes

| Signal | Meaning |
|---|---|
| **observation** | A mechanically captured fact about what occurred. |
| **claim** | An actor-authored interpretation or assertion. |
| **finding** | A reviewed conclusion connected to evidence. |
| **request** | A need for work, information, capability, or authority. |
| **exception** | A bounded deviation requiring attention. |
| **surprise** | Evidence threatening a load-bearing premise or direction. |
| **decision** | An authoritative resolution. |
| **directive** | Intent or constraint propagated from an authority holder. |

### Candidate record model and the `lesson` question

Unimatrix is an extensible durable-memory platform. Its current categories are not a closed ontology: a
new category is a configuration change when a distinct durable semantic type earns one. The common model
should therefore test a stable **Record envelope** with extensible, program-aware categories rather than
assuming that all durable knowledge is one generic record type.

`lesson` remains deliberately unsettled. The test must compare at least three readings:

1. **Signal:** a lesson is transported between actors or programs as organizational communication.
2. **Record category:** a lesson is durable process knowledge admitted to Unimatrix so actors avoid
   repeating a mistake; examples include workflow corrections and environmental test workarounds that are
   neither evidence findings nor architectural decisions.
3. **Derived construct:** a lesson is the result of transforming one or more observations, claims,
   findings, or failures into reusable guidance; it may be transported by another signal type and stored
   under a distinct category.

The vocabulary must retain `lesson` if removing it makes continual process improvement implicit,
second-class, or indistinguishable from information capture. It must reject or derive it if a separate
primitive adds no behavior, admission rule, retrieval need, or lifecycle of its own.

Signals route by significance rather than flowing into one global context:

- local coordination stays local;
- reusable learning enters institutional memory;
- cross-program needs route to affected programs;
- premise-changing surprises escalate immediately;
- strategic decisions and directives propagate downward.

A disclosure authored by an actor is never relabelled as an observation. Only externally captured facts
may feed a deterministic enforcement decision.

## H0 — The vocabulary is cosmetic or incomplete

The hypothesis is false if the common terms merely rename existing workflow objects, if important work
requires recurring domain-specific exceptions, or if the model cannot distinguish autonomy from effect
authority in real cases. Failure is useful: it identifies either a missing organizational primitive or an
abstraction boundary that should remain domain-specific.

## Test — express two unlike programs in the same language

Use one completed research-garage mission and one completed software-delivery mission. Prefer real,
artifact-backed histories over invented examples. Do not redesign either workflow during the mapping.

For each domain:

1. Reconstruct the actual intent, actors, delegated work, communications, effects, gates, evidence,
   outcomes, learning, and redirections.
2. Express every material object with the nine nouns and every material transition with the eight verbs.
3. Assign autonomy tiers to the actors as they actually operated, then write the authority envelope that
   would have bounded their real effects.
4. Classify every consequential communication using the signal vocabulary; explicitly separate disclosure
   from observation.
5. Classify every durable artifact using the Record envelope and its category semantics. For every lesson,
   test the signal, record-category, and derived-construct readings above.
6. Identify every domain term that cannot be represented without adding meaning to a common noun.
7. Identify every case where equal tiers conceal materially different authority or where an envelope
   cannot express the difference.
8. Replay one direction change: show which signals move, who may decide, which units stop, and which
   records remain durable.
9. Replay one failure or false-success claim: show where it is detected, how it is classified, and what
   prevents it becoming accepted organizational knowledge.

### Candidate cases

- **Research:** `wfh-008`, because it contains distributed work, two coverage reworks, independent audit,
  synthesis, a goal-owner challenge, a directional result, and no firewall grade movement.
- **Software delivery:** select a completed Unimatrix or Jurati feature with delegated implementation,
  deterministic tests, review, an effect-bearing merge, and at least one correction or failed gate.

The cases must differ in proof semantics. Research establishes claims about the world; software delivery
establishes behavior of a built artifact. A vocabulary that works only by flattening that distinction
fails.

## Evaluation

### Pass conditions

The hypothesis survives this first test only if:

1. **Coverage:** every material object, transition, authority delegation, and consequential communication
   in both cases maps without an unclassified residue.
2. **Compression:** the common vocabulary is smaller than the union of both domains' native vocabularies
   and removes repeated governance prose rather than relocating it into free-text exceptions.
3. **Semantic preservation:** a reader can reconstruct each domain's authority boundaries, proof bar,
   lifecycle, and escalation path from the mapping.
4. **Discrimination:** autonomy, authority, and evidence produce different answers in at least one real
   case each; none is functioning as an alias for another.
5. **Portability:** neither domain requires a new common noun or autonomy tier used only by itself.
6. **Interruption:** a direction change has a deterministic stop/hold propagation path and preserves a
   smallest safe resume point.
7. **False-success resistance:** an actor-authored claim cannot become an accepted fact or evidence grade
   without the domain's independent admission rule.

### Falsifiers

Any one is sufficient to reject or revise H1:

- three or more material concepts in either domain require prose exceptions to the common vocabulary;
- the same autonomy tier repeatedly grants incomparable or unsafe decision latitude;
- authority cannot be expressed without embedding domain-specific permission lists in the common model;
- signal routing requires globally sharing local context to preserve organizational awareness;
- `Capability`, `Unit`, or `Record` acquires incompatible meanings across the two domains;
- the common representation loses the distinction between a research finding and demonstrated software
  behavior;
- a direction change or false-success case cannot be explained without bypassing the proposed lifecycle.

## Expected output

The test should produce:

1. a side-by-side mapping of the two real missions;
2. a residue ledger containing every failed or strained mapping;
3. an autonomy-tier and authority-envelope comparison;
4. a signal-routing trace for one redirection and one false-success case;
5. a verdict on `lesson`: signal, record category, derived construct, multiple roles, or reject;
6. a verdict: `retain`, `revise`, or `reject` each noun, verb, tier, and signal class;
7. a minimal vocabulary v2 containing only what survived.

This is a **directional conceptual test**, not proof of runtime enforcement. It may establish a clearer
organizational model and a bounded implementation hypothesis. It cannot establish that any control works,
authorize a build, ratify Jurati's boundary, or advance a capability to `partial` or `proven`.

## Coordination state

`wfh-009` is held before synthesis. Its completed findings remain valid directional inputs, but its
synthesis should be interpreted against the revised organizational target after this vocabulary test.
No new `wfh-009` research work is implied by this document.
