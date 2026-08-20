# wfh-007 — owner direction after the scan

**Date:** 2026-08-19  
**Purpose:** product-owner input for the research leader completing `wfh-007`  
**Authority:** owner direction and working synthesis, not a research verdict, architecture decision, or
firewall-grade change  
**Run boundary:** `wfh-007` remains directional. This document steers hypothesize and triage; it does not
authorize a design, implementation, proof run, graph write, or status advancement.

---

## 1. Why this document exists

The scan was scoped around a possible reframe from an agentic workflow harness to a personal operating
system. After the five scout returns and cross-surface merge, the owner clarified the intended product,
deployment trajectory, trust boundary, initial programs, and unresolved growth problem.

The clarification materially changes how the scan should finish:

- **Jarvis is the desired experience, not a claim that Jurati should implement an operating system.**
- **Jurati Core is the first product to build.** It does not exist yet; the prior workflow-harness and
  Borg-Queen framings are earlier iterations of the same evolving concept.
- The first concrete program is **software development**. The **research garage** is the fast follower and
  an invokable service from software delivery.
- Cross-program coordination is load-bearing. Today the owner manually transfers intent, evidence, and
  decisions between independent agent teams; one experimental exchange has occurred through a GitHub
  Issue.
- Local inference is an intended direction, **not a present constraint or a prerequisite for Jurati**.
  Current inference is 100% cloud-hosted. The architecture must allow locality to improve incrementally.
- The unresolved architectural question is how independently-owned programs, repositories, workflows,
  skills, and memory instances compose into a growing personal digital organization without collapsing
  their ownership boundaries.

The research leader should treat these statements as owner-supplied constraints when completing
hypothesize, criticality, and triage. The evidence may still challenge the proposed means.

---

## 2. Owner objective

### Ultimate objective

Build a private, progressively autonomous digital team that helps the owner perform real activities across
changing areas of interest. The long-term experiential analogy is **Jarvis from Iron Man**: a persistent,
trusted collaborator able to learn new domains, coordinate specialist abilities, act within policy, and
escalate decisions appropriately.

The owner expects to operate as product manager and, where useful, advisory architect. The digital team
should increasingly execute the work beneath that role.

The system must not be designed around the owner's current interests. Its value depends on being able to
add new areas over time without rebuilding the core. Current examples are test cases, not a fixed product
taxonomy:

- agentic software development;
- the research garage and novel-technology exploration;
- 3D printing and possible visual intelligence;
- personal health information, research, tracking, and fitness advice;
- accounting and finance support across multiple small businesses.

These examples currently mix three different levels and should not be forced into six arbitrary domains:

1. **subject domains** — software, health, finance, fabrication;
2. **operating capabilities** — research, advise, monitor, plan, execute;
3. **channels/modalities** — repository work, events, voice, visual input, conversation.

One purpose of follow-on architecture is to discover the stable primitives beneath those levels.

### Initial user and market posture

- The sole intended user for approximately the first two years is the owner.
- Potential marketability is optional upside, not an initial design driver.
- Multi-tenant/SaaS concerns remain out of scope unless deliberately reintroduced.
- Personal control, extensibility, and earned trust take priority over optimizing for general onboarding.

---

## 3. Locality and provider posture

### Present reality

Current inference is **100% cloud-based** and therefore does not yet satisfy the long-term locality goal.
That is acceptable: the system is expected to evolve incrementally.

### Intended direction

"Local" means under the owner's control and excluded from provider training or uncontrolled reuse. It does
not require every workload to run on the same physical machine.

The anticipated estate includes:

- the owner's computers and operating systems;
- rented servers;
- controlled cloud compute;
- transports secured with Tailscale;
- authorized tools that access the public internet;
- eventually, more local inference where it is viable and useful.

Jurati must therefore be **model-, provider-, and location-neutral**. Claude, Codex, Gemini, frontier APIs,
controlled hosted models, and future local models must be addressable through explicit adapters and
honest guarantee profiles. Replacing a cloud model with a local one should not require redesigning
workflow, authority, memory, or inter-team communication.

Transport security is necessary but insufficient: Tailscale secures connectivity; Jurati still needs to
establish workload identity, delegated authority, information-flow rules, evidence, and enforcement.

### Directional requirement for triage

Do not reject a useful Jurati Core architecture because inference is not local on day one. Do reject an
architecture that makes one provider's agent semantics, credentials, or conversation format the permanent
coordination model.

---

## 4. Product boundary now emerging

A useful working statement for the remainder of the scan is:

> **Jurati is a provider-neutral coordination and trust substrate for the owner's personal digital
> organization. It connects specialized teams and programs, governs their authority, carries evidence and
> work between them, and enables progressively greater autonomy under owner-controlled policy.**

This is a working synthesis, not a ratified architecture. It sharpens several distinctions:

- **Jarvis** describes the eventual user experience.
- **Jurati Core** is the initial coordination, workflow, and trust substrate.
- **Unimatrix** supplies governed durable memory; it is not the workflow engine.
- The **research garage** is one specialized program operating on that substrate.
- Software-delivery workflows are another specialized program and the first vertical slice.
- Local or hosted model capacity is replaceable execution supply, not the system's source of authority.

### Current physical topology

Today, Jurati, Unimatrix, and the research garage are separate repositories. Each area owns its own:

- agent and role definitions;
- workflows or protocols;
- skills and procedures;
- durable memory in its own Unimatrix instance.

This separation is deliberate and currently useful. The open question is how the structure grows while
preserving local ownership and permitting composition. The scan should not assume that the answer is a
monorepo, one global workflow registry, one global memory instance, or a single always-privileged agent.

---

## 5. Settled owner trust constraints

The following are owner decisions for the current direction:

1. **An LLM cannot police itself or another LLM as the final authority.** Models may interpret, recommend,
   and propose; deterministic policy outside the acting model authorizes effects.
2. **Agents cannot change active policy.** If an agent could change the rules governing itself, the rules
   would not be a boundary.
3. **Agents may recommend policy changes.** The owner authorizes every activation.
4. **Agents cannot spend money without owner approval.** This may be reconsidered only after substantial
   earned trust; it is not categorically impossible forever.
5. **Agents cannot speak publicly for the owner without approval.** The exact boundary—Issues, pull
   requests, comments, email, publishing, and statements of opinion—still needs definition.
6. **The mature system distinguishes autonomous work, owner decisions, and event-triggered execution.**
   It should know what it may complete independently, what must be escalated, and what actions a given
   inbound event and policy permit.
7. **Trust graduation is an owner judgment.** Twenty successful eligible runs in the same action and
   consequence class is the earliest baseline before Jurati should even recommend expanded autonomy.
   Twenty runs do not automatically confer authority.

A future trust recommendation should present the complete record: successes, policy denials, failures,
owner interventions, near misses, reversals, and the precise new authority requested. The owner remains the
only activator.

---

## 6. Failure priorities

The system must be secure by design because the owner eventually wants to trust it with consequential
business and finance capabilities. Priority failure classes named by the owner are:

- deleting data that should not be deleted;
- corrupting durable personal knowledge or the "second brain";
- exposing private or sensitive personal/business information;
- misleading the owner through hallucinated, unsupported, or misapplied information;
- giving harmful or materially bad advice;
- the broader documented failure modes of autonomous agent work, including authority expansion and
  uncontrolled external effects.

The design should not translate these into one generic `dangerous` flag. The evidence in `wfh-007`
supports separate treatment of resource authority, information sensitivity, reversibility/consequence,
evidence quality, and external representation.

---

## 7. The first vertical slice

### First project

**Build Jurati Core.** Jurati does not currently exist as a codebase implementing the intended product.
The first real use of Jurati should assist in building Jurati itself, without assuming that self-hosting
automatically proves the architecture.

### First program: software development

Software delivery is the preferred first slice because the owner has new projects to start and already
has mature workflow definitions under the Unimatrix repository's `.claude/protocols/uni` surface. Those
existing protocols should be the first corpus and operating workflow, not rewritten from scratch merely
to make Jurati look general.

The intended trajectory is:

1. the owner provides product intent and decisions;
2. the software-delivery team structures and implements the work under its existing protocols;
3. Jurati progressively supplies explicit workflow state, phase-aware authority, coordination, policy,
   and supervision;
4. when the delivery team encounters a bounded uncertainty or technology question, it can request a
   research spike from the garage;
5. the garage returns evidence-graded work that the delivery workflow can consume without the owner
   manually translating between teams.

### Fast follower: research garage

Software development and the garage are distinct programs but tightly related. The garage is both:

- a second workflow corpus against which Jurati's primitives must generalize; and
- a callable specialist service for software delivery.

The recommended first cross-program demonstration is one complete round trip:

```text
Unimatrix software-delivery workflow
  -> bounded research request
  -> Jurati-mediated work contract
  -> research garage
  -> evidence-graded response
  -> acceptance against the request contract
  -> software-delivery workflow resumes
```

The actual Unimatrix enhancement used for that demonstration remains to be selected.

---

## 8. Cross-program communication is a first-class capability

The owner is currently the integration mechanism between specialized agent teams. The owner transfers
context, translates vocabulary, authorizes disclosure, decides whether the result satisfies the request,
and routes the next step. Two teams' agents have interacted through a GitHub Issue once, demonstrating a
possible transport but not a complete coordination protocol.

Jurati must progressively assume the mechanical parts of that integration while preserving owner gates.
This is not adequately described as "agents can chat." Free-form conversation obscures delegation,
authority, acceptance, and provenance.

A candidate cross-program work contract should be investigated with at least these fields:

- stable requesting identity and program/repository;
- objective and bounded deliverable;
- workflow instance, phase, role, and task context;
- authority delegated with the request;
- resources and knowledge intentionally disclosed;
- information classification and onward-disclosure rules;
- evidence and acceptance requirements;
- budget, expiry, cancellation, and retry behavior;
- return channel and escalation destination;
- model/provider/runtime provenance;
- final disposition: accepted, rejected, superseded, expired, or abandoned.

GitHub Issues can remain an early adapter and human-visible surface. They must not become the semantic
protocol. The contract should survive transport through GitHub, Unimatrix, local queues, hosted agent
runtimes, and future event or conversational channels.

### Open delegation questions

The scan should carry, not silently answer, these architectural questions:

1. Is a team/program such as `unimatrix-development` or `research-garage` a stable principal, or is every
   team assembled per objective?
2. Does a called team inherit the caller's authority, receive an attenuated derived grant, or receive only
   explicitly packaged material? The current owner preference is toward narrower derived authority, but
   this is not yet a formal decision.
3. Who accepts returned work: deterministic contract checks, an independent verifier, the requesting
   agent, or the owner?
4. What information may cross repository, project, and memory-instance boundaries?
5. Does Jurati retain payloads, or only contracts, state, evidence references, and audit metadata?
6. How are identity and policy represented consistently across heterogeneous models and providers without
   forcing each repository to give up its local definitions?

---

## 9. Why an IAM analogy helps—and where it stops

The owner proposed AWS IAM as a useful analogy: principals receive policies over actions and resources,
with phase-specific policy available for structured workflows. That is a valuable starting point, but
plain IAM semantics do not express the whole problem.

Jurati may also need to bind:

- the declared objective and workflow phase authorizing an action;
- action consequence: idempotent, reversible, compensable, or irreversible;
- the evidence required before a claim, decision, or action becomes durable;
- whether an actor may decide, merely recommend, or only collect evidence;
- escalation behavior when authority, evidence, or confidence is insufficient;
- delegation depth, attenuation, expiry, revocation, and aggregation across individually permitted
  actions;
- information-flow constraints between separately-owned programs and memory stores.

The likely original seam remains narrower than a new sandbox or general authorization engine:

> declared intent and workflow phase -> derived authority -> deterministic enforcement ->
> evidence-qualified commitment -> acceptance or escalation

The research must still determine whether this seam is differentiating and what can be assembled.

---

## 10. Memory and the second brain

### Current boundary

Each project currently retains its own durable memory in its own Unimatrix instance. Memory is deliberately
not one aggregated pot. Existing Unimatrix design and retrospective work has already addressed parts of
retention, project ownership, and deletion; the research leader should reuse that work rather than invent a
parallel memory model from this discussion.

### Unresolved product decision

The open question is **what qualifies for elevation from project memory into the owner's cross-project
second brain**.

Elevation should be investigated as a governed publication act, not automatic aggregation:

```text
project-local observation
  -> reusable-knowledge candidate
  -> provenance and evidence check
  -> sensitivity and scope classification
  -> contradiction/deduplication review
  -> authorized elevation policy
  -> second-brain entry retaining its origin
```

Important unresolved points include:

- who or what may nominate an entry;
- which categories may elevate automatically, if any;
- whether the owner must approve every elevation initially;
- how evidence grades translate across projects with different ontologies;
- how corrections or deletion at the source affect elevated knowledge;
- whether elevated knowledge is copied, referenced, or published into a separate owner-controlled
  instance;
- how sensitive personal, health, financial, and business knowledge is partitioned;
- how ephemeral working context, project history, reusable knowledge, personal preferences, and audit
  records receive different retention policies.

Jurati should not casually become another large memory store. One candidate boundary is for Jurati to own
workflow state and exchange metadata while Unimatrix instances retain knowledge payloads. That remains a
hypothesis for architecture, not a decision from this conversation.

---

## 11. Stable primitives worth testing

The discussion and scan together suggest the following candidate primitive surface. These are prompts for
hypothesis and triage, not an authorized design vocabulary:

1. namespace and stable identity across owner, program, project, workflow, agent, and resource;
2. typed actions with consequence and reversibility properties;
3. resource and information authority;
4. declared workflow state, phase, role, and transitions;
5. deterministic policy decision and multi-plane enforcement;
6. evidence-qualified decisions and durable commitments;
7. governed memory with provenance, correction, sensitivity, and elevation;
8. structured cross-program work contracts and attenuated delegation;
9. acceptance, verification, escalation, and owner gates;
10. events, supervision, cancellation, recovery, and audit;
11. provider/runtime adapters with explicit guarantee profiles;
12. domain/program packages that retain local workflows, agents, skills, and memory ownership.

The research should prefer the smallest semantic core that permits independent programs to compose. It
should be skeptical of both extremes: one universal ontology that absorbs every domain, and unstructured
message passing that leaves the owner as the only reliable integrator.

---

## 12. What is decided, inferred, and open

### Owner-decided direction

- Jurati Core is the first project.
- Software delivery is the first program; the research garage is the fast follower.
- Existing Unimatrix software-delivery protocols are the initial workflow corpus.
- Cross-program interaction is a core capability.
- Policy enforcement is deterministic and external to models.
- Agents cannot activate policy changes.
- Spending and public representation require owner approval initially.
- Trust expansion is subjective and owner-authorized; 20 eligible successful runs is only the earliest
  review threshold.
- Current cloud inference is acceptable; provider neutrality and incremental locality are required.
- Project memories remain separate by default; second-brain elevation needs focused product design.
- The initial user is the owner, not a market or multi-tenant persona.

### Working inferences to test

- Jurati is better framed as a coordination and trust substrate than as a literal operating system.
- A structured work contract, rather than agent chat, is the likely cross-program primitive.
- Stable primitives should be proved against software development and research before generalizing to
  health, finance, fabrication, voice, or visual intelligence.
- Existing isolation, secret management, logs, and delegation should be adopted or assembled.
- The most plausible original seam is phase-derived authority combined with evidence-qualified commit and
  deterministic escalation.
- Jurati may be a control plane over separately-owned repositories and Unimatrix instances, not the owner
  of all payloads or workflows.

### Still open

- the repository/package/deployment topology that permits growth;
- global versus federated identity and namespace;
- how local workflow definitions compile or register into Jurati without losing ownership;
- cross-program information classification and disclosure policy;
- delegation, acceptance, revocation, expiry, and aggregation semantics;
- the exact boundary of public representation;
- the first Unimatrix enhancement used for the end-to-end demonstration;
- the second-brain promotion protocol;
- Jurati's implementation language and smallest trusted core;
- which enforcement planes are required for the first slice;
- what evidence would justify calling the proposed seam differentiating;
- which local-inference step should occur first and when it becomes product-critical.

---

## 13. Instructions to the research leader completing wfh-007

1. **Use this as owner input, not as a verdict.** Carry it into the hypothesizer and goal-owner materials.
   Preserve any evidence-backed contradiction.
2. **Correct the target.** Evaluate what Jurati Core must provide for a growing personal digital
   organization composed of independently-owned programs—not a monolithic six-domain personal OS.
3. **Add cross-program coordination to criticality.** The existing named component list omitted the
   owner's present integration burden. Assess identity, work contracts, delegation, acceptance,
   provenance, and information flow alongside reviewer-throughput matching.
4. **Treat cloud-to-local as a trajectory.** Evaluate provider/runtime portability and the ability to
   substitute local inference incrementally. Do not make current cloud use a scope failure.
5. **Use the real first slice.** Route recommendations against Jurati building Jurati through the existing
   Unimatrix software-delivery protocols, with the garage invoked for one bounded research spike.
6. **Preserve repo and memory ownership as a constraint.** Investigate federation/composition before
   recommending consolidation.
7. **Carry the second-brain question as a named product decision.** Reuse existing Unimatrix design and
   retrospective evidence; identify what remains unanswered about elevation across project instances.
8. **Apply buy-before-build rigor.** The owner does not need a new sandbox, secret store, transparency log,
   or generic IAM implementation if existing pieces cover them. For every ASSEMBLE verdict, name the seam
   and whether it is differentiating. For every BUILD verdict, name what assembly cannot provide.
9. **Keep the instrument caveat visible.** All scouts hit the shared 200/200 search cap. Do not call the
   territory exhausted; distinguish a completed bounded scan from exhaustive external coverage.
10. **Do not design through the curator.** The scope's architect-role gap remains. If completion reveals
    that an authored namespace, action vocabulary, trust constitution, or memory-elevation protocol is the
    next artifact, recommend a separate bounded architecture scope and the role authorized to create it.
11. **Return explicit owner decisions at the gate.** At minimum, present:
    - the recommended Jurati Core boundary;
    - adopt/assemble/build/probe/park verdicts;
    - the criticality ranking including cross-program coordination and reviewer throughput;
    - a proposed first end-to-end Unimatrix -> garage -> Unimatrix demonstration;
    - the theme-revision proposal;
    - the open architecture decisions that must precede implementation.
12. **Do not advance a firewall grade.** This run remains directional and produces structure only.

---

## 14. Recommended handoff outcome

The useful finish for `wfh-007` is not a complete Jurati architecture. It is a hard, evidence-backed neck
decision answering:

1. What existing components should Jurati adopt?
2. What composition can provide most of the trust and coordination substrate?
3. What exact seams remain uncovered, and which of them are differentiating?
4. Is cross-program work exchange a core primitive or merely an adapter concern?
5. Does Jurati earn a trusted core of its own, and what is the smallest responsibility that core must
   hold?
6. What bounded architecture scope should follow before code is written?

The likely next run after owner approval is a dedicated architecture/design scope for Jurati Core, using
one real Unimatrix-development-to-research-garage round trip as its grounding scenario. `wfh-007` should
recommend that scope only if the completed triage supports it.
