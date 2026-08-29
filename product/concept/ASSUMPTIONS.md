# Component Architecture — Assumptions

Input artifact for the component-architecture run. **Logical only.** An assumption names something the
architecture must accommodate; it never names a vendor, product, library, or protocol. "Model router" is
an assumption. "LiteLLM" is not.

Two tracks (Claude and Codex) consume this file unchanged and each produce an independent component
model. Convergence is by hand afterward. Neither track may edit this file — amendments are append-only
and owner-authorized.

---

## Why assumptions and not requirements

A requirement says what to build. An assumption says what must remain true while we work out what to
build. The component model is the *answer*; this file is the set of things the answer may not violate.

Much of this is already established in the `workflow-harness` theme evidence. Where it is, the
assumption **cites** it rather than re-deriving it — the architect treats it as settled input, not as a
question to reopen.

---

## Schema

```yaml
- id: A##
  type: capability | constraint | structural | evolution
  statement: <one sentence — what must be true or possible>
  basis: owner-declared | evidence-backed | provisional
  provenance: <where this is already established, or `owner-new`>
  implies: <the LOGICAL capability this demands — the component seed>
  variability: <what must be swappable or able to change without redesign>
  not_this: <technology/product choices this assumption does NOT make>
  falsifier: <what would show this assumption is wrong>   # optional
```

**The four types, and why the distinction is load-bearing** — each produces a different architectural
consequence, and conflating them is how a component model turns into a wish list:

| type | what it produces |
|---|---|
| `capability` | a **component** — something must do this |
| `constraint` | a **boundary or placement** — where a thing may or may not sit |
| `structural` | **topology** — how components relate |
| `evolution` | a **seam** — where change is expected and must not require redesign |

**The three bases, and what each licenses the architect to do:**

- `owner-declared` — take as given. Do not relitigate. May be *interpreted*, never challenged.
- `evidence-backed` — established by a cited run or finding. Challengeable only with contrary evidence.
- `provisional` — the owner's current belief, explicitly open to challenge. Say so if it doesn't hold.

**`not_this` is mandatory on every capability assumption.** It is the guard that keeps a logical
architecture logical. If you cannot state what technology choice the assumption is *not* making, the
assumption is written at the wrong altitude.

---

## Worked examples

```yaml
- id: A01
  type: capability
  statement: Work can be routed to different model providers and to locally operated models, and the
    routing decision is made outside the work being routed.
  basis: owner-declared
  provenance: target-concept-v1.md §Build vs Buy, §Determinism vs Non-deterministic
  implies: a logical model router — a placement point that selects an execution target per unit of
    work, and is not itself selectable by the work it routes
  variability: providers appear and disappear; the local/remote mix shifts toward local over time;
    no component above the router may know which target served it
  not_this: no gateway product, no proxy, no inference server, no provider, no local runtime chosen
  falsifier: a unit of work whose correctness depends on which target executed it

- id: A02
  type: constraint
  statement: Consequential governance and effect credentials sit outside the activity they govern;
    an agent cannot alter the rules constraining it during execution.
  basis: owner-declared
  provenance: target-concept-v1.md §Determinism vs Non-deterministic; themes.md workflow-harness lens
  implies: a control plane whose placement is outside every governed actor, holding effect credentials
  variability: what is governed grows over time; the placement must not
  not_this: no policy engine, secret store, or identity system chosen
  falsifier: a governed actor that can reach its own constraint definition at runtime

- id: A03
  type: capability
  statement: Programs communicate with one another — a finding in one program reaches another program
    that can act on it.
  basis: evidence-backed
  provenance: target-concept-v1.md §Structure/Methodology (garage → Unimatrix bugs); wfh-011 — V5 has
    NO construct for cross-Scope delivery; `Signal` was excluded into `Event`, and Events belong to a
    single Scope
  implies: a cross-program communication path with addressing and delivery, distinct from a program's
    internal event record
  variability: the number of programs is unbounded and unknown in advance
  not_this: no bus, queue, protocol, or message format chosen
  falsifier: cross-program need shown to be adequately served by shared storage alone

- id: A04
  type: constraint
  statement: Deterministic capability is preferred wherever it can carry the required semantics;
    non-deterministic reasoning is used where it adds value, never where a deterministic check exists.
  basis: owner-declared
  provenance: target-concept-v1.md §Determinism vs Non-deterministic
  implies: every gate or check has a declared determinism altitude, and mechanical checks are
    distinguishable from judgment at the point of use
  variability: the deterministic/non-deterministic boundary moves as capability improves
  not_this: no rules engine, validator, or model class chosen
  falsifier: a governance decision where determinism is achievable but demonstrably not desirable

- id: A05
  type: structural
  statement: Intent, constraints, consequential decisions and institutional memory are centralized;
    reasoning, exploration, planning, communication and reversible execution are distributed.
  basis: owner-declared
  provenance: themes.md workflow-harness lens; target-concept-v1.md §Structure/Methodology
  implies: a topology with a small centralized core and an unbounded distributed edge, and a stated
    rule for which side any new capability lands on
  variability: the edge grows without bound; the core must not grow proportionally
  not_this: no orchestration framework or repository topology chosen
  falsifier: a capability whose correct placement cannot be decided by the rule

- id: A06
  type: evolution
  statement: Capabilities we cannot currently name (a finance team, e.g.) must be addable without
    redesigning the organization.
  basis: owner-declared
  provenance: target-concept-v1.md §Build sequence
  implies: capability formation is itself a modeled process, not a schema change
  variability: the set of capabilities is open; the mechanism for adding one is closed
  not_this: no plugin system, registry implementation, or repo layout chosen
  falsifier: a plausible new capability that cannot be expressed without new common structure
```

---

## Owner-authorized amendments — 2026-08-29

```yaml
- id: A07
  type: evolution
  statement: The organization can be built and made useful incrementally; no release needs to contain
    the complete target organization before bounded value and learning begin.
  basis: owner-declared
  provenance: owner-new — autonomy-first build direction, 2026-08-29
  implies: an architectural kernel that supports thin end-to-end capability slices and can accept later
    components without invalidating earlier work
  variability: delivery order, breadth, and sophistication change as operating evidence accumulates
  not_this: no MVP feature list, release plan, deployment topology, or implementation sequence chosen
  falsifier: the smallest useful autonomy capability requires the complete target architecture to exist

- id: A08
  type: capability
  statement: Authorized work can continue across execution sessions without depending on any one
    session's transient context, and can resume from an explicit durable state.
  basis: owner-declared
  provenance: owner-new — autonomy-first build direction, 2026-08-29; organizational-data-model-v5.yaml
    Attempt.resume_requirements and I15
  implies: durable work continuity — identity, baseline, progress, unresolved residue, authority, and
    next admissible action can be reconstructed independently of the prior executor
  variability: sessions, actors, models, and runtimes may change between attempts
  not_this: no scheduler, checkpoint format, workflow engine, database, or agent runtime chosen
  falsifier: a different authorized actor cannot safely determine whether and how to resume interrupted work

- id: A09
  type: structural
  statement: Autonomy is graduated, bounded, revocable, and separable from authority to cause effects;
    greater autonomy is earned through observed operation rather than enabled as one system-wide mode.
  basis: provisional
  provenance: owner-new — autonomy-first build direction, 2026-08-29; organizational-data-model-v5.yaml
    authority_chain, Delegation, EffectBoundary, autonomy_tier, I12 and I17
  implies: autonomous initiative flows through explicit delegations and independent effect boundaries,
    with limits on scope, resources, duration, escalation, and sub-delegation
  variability: autonomy may increase, decrease, or differ by program and effect class without changing
    the underlying authority model
  not_this: no autonomy-level taxonomy is ratified, and no policy engine, sandbox, approval product, or
    credential system chosen
  falsifier: safe autonomy requires giving an actor unrestricted effect authority

- id: A10
  type: capability
  statement: The owner can interrupt, redirect, or stop autonomous work, and the organization can reach
    a durable safe boundary without claiming incomplete work as complete.
  basis: provisional
  provenance: owner-new — autonomy-first build direction, 2026-08-29; theme-coordination.md §Surprise
    and stop protocol; organizational-data-model-v5.yaml Attempt
  implies: interrupt handling, safe-stop coordination, preserved partial outputs, and an explicit resume
    point are common execution capabilities
  variability: stop latency and safe-boundary semantics differ by work and effect class
  not_this: no cancellation protocol, process supervisor, transaction mechanism, or user interface chosen
  falsifier: any bounded autonomous activity cannot be stopped without losing attribution or corrupting state

- id: A11
  type: structural
  statement: Durable organizational memory preserves provenance, currentness, epistemic status, evidence,
    decisions, and correction history; it is not a transcript archive and stored content is not true merely
    because it was stored.
  basis: provisional
  provenance: target-concept-v1.md §Structure/Methodology; organizational-data-model-v5.yaml Record,
    Event, evidence_grade, epistemic_kind, currentness, I1-I5 and I8-I9
  implies: a governed memory substrate with admission, retrieval, supersession, provenance, and evidence
    semantics distinct from transient execution context
  variability: schemas, retention, retrieval techniques, and the physical substrate may evolve or be extended
  not_this: no knowledge product, database, embedding model, ontology implementation, or storage topology chosen
  falsifier: safe cross-session autonomy is demonstrated using ungoverned transcripts as the sole durable memory

- id: A12
  type: capability
  statement: Autonomous activity reports material progress, decisions, exceptions, surprises, resource use,
    completion claims, and blocked state in a form the owner can understand without reconstructing execution.
  basis: owner-declared
  provenance: owner-new — autonomy-first build direction, 2026-08-29; theme-coordination.md §Human
    communication rules
  implies: an owner-facing reporting capability derived from durable work, evidence, authority, and effect records
  variability: cadence, detail, audience, and notification threshold vary by delegation and significance
  not_this: no dashboard, chat system, notification service, report format, or observability product chosen
  falsifier: the owner must inspect raw transcripts or internal stores to know what autonomous work did

- id: A13
  type: constraint
  statement: Security controls can strengthen from an initially pragmatic posture to a high-security posture
    without changing the organization's logical identities, authority chain, memory semantics, or workflows.
  basis: owner-declared
  provenance: target-concept-v1.md §Security
  implies: stable trust boundaries and replaceable enforcement seams for identity, isolation, secrets,
    information access, model access, and consequential effects
  variability: assurance level, threat model, deployment environment, and enforcement mechanisms strengthen over time
  not_this: no identity provider, isolation technology, cryptographic scheme, secret store, or network model chosen
  falsifier: raising assurance requires redefining the core organizational model rather than strengthening boundaries

- id: A14
  type: capability
  statement: The organization can discover and deliberately combine actors with dissimilar relevant skills for
    a goal, including skills whose usefulness was not anticipated when the goal was formed.
  basis: owner-declared
  provenance: target-concept-v1.md §Core Principle
  implies: skill discovery, evidence-aware matching, team composition, and scoped delegation are available as
    organizational capabilities
  variability: skills, actors, disciplines, matching criteria, and team duration are open-ended
  not_this: no recommender, directory, taxonomy, staffing algorithm, or organizational chart chosen
  falsifier: effective cross-disciplinary composition always requires a human to already know every relevant skill

- id: A15
  type: constraint
  statement: Completion and consequential claims are accepted only against an explicit baseline and proof bar,
    with missing or unavailable evidence represented directly rather than interpreted as success.
  basis: evidence-backed
  provenance: target-concept-v1.md §Governance/Checks and balances; research-factory-methodology.md §3;
    organizational-data-model-v5.yaml Gate, Record, I6-I9
  implies: evidence admission and independent assessment sit between execution output and organizational acceptance
  variability: proof bars and eligible evidence are owned by each workflow or record category
  not_this: no test framework, CI system, evaluator model, scoring scheme, or review product chosen
  falsifier: a consequential class of work is safer when the executor's unsupported completion claim is accepted
```

### Owner-authorized amendments — distributed autonomy clarification

```yaml
- id: A16
  type: structural
  statement: Autonomous execution is coordinated locally within project repositories; the ecosystem does not
    depend on a central scheduler assigning and sequencing all project work.
  basis: owner-declared
  provenance: owner-new — distributed-ecosystem clarification, 2026-08-29
  implies: each project has a local execution boundary and can govern its own workflows while participating in
    common communication, reporting, memory, and authority semantics
  variability: repositories may use different workflows, actors, models, and execution mechanisms
  not_this: no repository agent, local orchestrator, scheduler, hook system, or repository layout chosen
  falsifier: useful cross-project autonomy requires a central service to schedule every unit of work

- id: A17
  type: capability
  statement: Every participating repository can publish a normalized, attributable account of current work,
    progress, decisions, risks, resource use, blocked state, and completion evidence to centralized reporting.
  basis: owner-declared
  provenance: owner-new — centralized-reporting clarification, 2026-08-29; clarifies A12
  implies: a shared project-status reporting contract and an aggregation capability that preserves links back to
    the project's authoritative evidence
  variability: project-local state models and workflows may differ; the common reporting meaning remains stable
  not_this: no status schema, transport, dashboard, database, polling mechanism, or reporting service chosen
  falsifier: centralized visibility can remain trustworthy while each repository reports only unstructured summaries

- id: A18
  type: evolution
  statement: Cross-project and cross-program communication semantics will be learned through operating iterations;
    routes, message classes, acknowledgement, escalation, and ownership must evolve without redesigning participants.
  basis: owner-declared
  provenance: owner-new — cross-program communication direction, 2026-08-29; extends A03
  implies: versioned communication contracts and replaceable routing policy sit between independent participants
  variability: topology, routing rules, delivery guarantees, message classes, and participating programs evolve
  not_this: no final communication taxonomy, protocol, bus, broker, queue, or delivery topology chosen
  falsifier: the complete cross-program communication model can be specified correctly before operational use

- id: A19
  type: capability
  statement: Scarce model usage and other resources can be budgeted to bounded activities and prioritized across
    projects without centralizing the execution of those activities.
  basis: owner-declared
  provenance: owner-new — public-model dependency and portfolio-budget clarification, 2026-08-29
  implies: portfolio prioritization allocates explicit resource envelopes that local coordinators consume and report
    against, with exhaustion and exception behavior declared in advance
  variability: resource types, prices, providers, project priority, accounting precision, and allocation cadence change
  not_this: no billing system, token counter, quota service, optimizer, currency, or prioritization algorithm chosen
  falsifier: distributed execution cannot respect a portfolio resource ceiling without a central scheduler

- id: A20
  type: structural
  statement: Autonomy is granted per program and effect risk, not as one ecosystem-wide level; research may receive
    broader initiative while foundational data-platform changes remain tightly controlled.
  basis: owner-declared
  provenance: owner-new — risk-based autonomy clarification, 2026-08-29; supersedes the uniform reading of A09
  implies: risk classification is an input to delegation, effect boundaries, budget, evidence bars, reporting cadence,
    and escalation rules
  variability: risk appetite and autonomy differ by program, effect class, maturity, reversibility, and operating evidence
  not_this: no final tier names, risk matrix, approval workflow, enforcement product, or program-specific grant chosen
  falsifier: one autonomy setting is acceptably safe and useful for both exploratory research and foundational data changes

- id: A21
  type: structural
  statement: The research garage and delivery projects exchange needs and findings in both directions: projects can
    request investigation, and garage findings can alter project choices or create project work.
  basis: provisional
  provenance: owner-new — research-garage/project relationship question, 2026-08-29; A03
  implies: explicit demand intake, audience/beneficiary addressing, finding delivery, acknowledgement, and disposition
    cross the garage/project boundary
  variability: one research theme may serve one project, several projects, or an ecosystem-wide concern
  not_this: does not assume one theme per project, and chooses no intake system, roadmap tool, or communication transport
  falsifier: garage research and project delivery remain effective with no explicit bidirectional relationship
```

### Declared design hole

The cardinality between research themes and projects is intentionally unresolved. A theme might be project-specific,
shared by several projects using the same capability or technology, or ecosystem-wide. The logical architecture must
not assume one theme per project until operating evidence shows that boundary carries distinct lifecycle and ownership.

### Owner-authorized amendments — collective operating model clarification

```yaml
- id: A22
  type: capability
  statement: Every program can discover the current collective operating model applicable to it, including shared
    vocabulary, invariants, authority boundaries, communication obligations, evidence rules, and reporting expectations.
  basis: owner-declared
  provenance: owner-new — collective-operation clarification, 2026-08-29
  implies: an authoritative operating-model publication and resolution capability that supplies each program with
    applicable, versioned, provenance-bearing definitions
  variability: programs, local workflows, applicable rule sets, and the collective operating model evolve independently
  not_this: no configuration service, policy language, document format, registry product, or distribution mechanism chosen
  falsifier: autonomous programs can coordinate safely while relying on separately copied and potentially divergent rules

- id: A23
  type: structural
  statement: Programs may extend the collective operating model for local needs but cannot silently redefine or weaken
    its common semantics and invariants.
  basis: provisional
  provenance: organizational-data-model-v5.yaml program_ownership, method_custody and I19; owner clarification, 2026-08-29
  implies: a layered operating model with a governed collective baseline, explicit program extensions, and compatibility
    evaluation between the two
  variability: extension points and program-specific definitions grow without forcing all local concepts into the core
  not_this: no inheritance mechanism, schema language, package system, conformance tool, or governance body chosen
  falsifier: independently evolving programs require unrestricted redefinition of common terms to remain useful

- id: A24
  type: constraint
  statement: An actor's receipt or apparent understanding of operating instructions is distinct from conformance and
    enforcement; consequential boundaries cannot rely solely on an agent remembering or following those instructions.
  basis: evidence-backed
  provenance: organizational-data-model-v5.yaml declared_identity, Delegation, Gate, EffectBoundary, I4, I6, I12 and I18;
    target-concept-v1.md §Governance/Checks and balances
  implies: operating context delivery, conformance evidence, independent gates, and effect enforcement remain separate
    architectural responsibilities
  variability: more operating rules may become mechanically enforceable over time
  not_this: no prompt format, instruction-file convention, policy engine, guardrail product, or attestation mechanism chosen
  falsifier: instruction delivery alone reliably constrains consequential autonomous effects

- id: A25
  type: capability
  statement: Each autonomous attempt can identify the exact collective operating-model baseline that governed it,
    continue safely from an approved local copy when publication is temporarily unavailable, and detect when that
    baseline has diverged from the current authoritative version.
  basis: provisional
  provenance: owner-new — centralized ecosystem-rules repository option, 2026-08-29; extends A08 and A22
  implies: baseline identification, local availability, compatibility evaluation, and drift reporting accompany
    operating-model discovery
  variability: publication location, synchronization cadence, compatibility policy, and permitted staleness vary
    by program and risk class
  not_this: no source-control host, repository structure, synchronization tool, cache, or update mechanism chosen
  falsifier: distributed programs can remain attributable and compatible without identifying which operating-model
    version governed their work
```

#### Candidate physical realization — not a logical commitment

A centralized ecosystem-rules repository is the first candidate for publishing the collective operating model.
Program repositories would reference an identifiable baseline, retain an approved local copy, declare local extensions,
and report compatibility or drift. The repository would publish rules; it would not centrally schedule program work.

---

## Coverage frame

The set is complete when every axis below holds at least one assumption, or is explicitly declared a
hole with the reason. Axes are `target-concept-v1.md`'s own sections, so the concept document is a
first-class input rather than background reading.

| Axis | Source section | Assumptions |
|---|---|---|
| Organization & structure | §Structure/Methodology | A05, A07, A16, A21, A22, A23, A25 |
| Communication pathways | §Structure/Methodology | A03, A12, A17, A18, A21, A22, A25 |
| Structured autonomy & authority | §Governance, §Determinism | A02, A09, A10, A20, A22, A24 |
| Execution pathways | §Structure/Methodology, §Build sequence | A07, A08, A10, A16, A25 |
| Governance & checks/balances | §Governance/Checks and balances | A02, A04, A09, A15, A19, A20, A23, A24 |
| Durable memory & cross-program learning | §Structure/Methodology | A03, A08, A11, A17, A21, A22, A25 |
| Security seams | §Security | A02, A13 |
| Determinism boundary | §Determinism vs Non-deterministic | A04, A15, A24 |
| Provider & runtime flexibility | §Build vs Buy | A01, A13, A19 |
| Capability formation | §Build sequence | A06, A07, A22, A23 |
| Cross-disciplinary recombination | §Core Principle | A14 |

An axis with no assumption is a **declared hole**, named as such. Silence is not coverage.

---

## Rules for both tracks

1. **Logical only.** No vendor, product, library, protocol or repository choice. If a component's name
   implies a technology, rename it.
2. **Cite, do not re-derive.** Where an assumption is `evidence-backed`, the cited run settled it.
3. **A challenge is welcome and must be explicit.** A `provisional` assumption you believe is wrong gets
   a named objection with a reason — not a silent workaround in the model.
4. **Do not resolve an assumption by narrowing it.** If A01 is inconvenient, that is a finding.
5. **Independence.** Neither track reads the other's output before convergence.

<!-- Amendments are append-only and owner-authorized. Never overwrite an assumption; supersede it explicitly. -->
