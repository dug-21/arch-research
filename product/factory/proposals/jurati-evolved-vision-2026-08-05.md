# Jurati — evolved vision: a phase-aware queen for governed agent work

**Status:** owner-directed working note · **Date:** 2026-08-05  
**Purpose:** capture a design evolution for reflection; this is not a research verdict, an ADR, or settled
Unimatrix knowledge. Nothing in this note advances a firewall grade.  
**Builds on:** `workflow-harness-scope-recut.md`, `workflow-harness-research-plan.md`, the current research
garage protocols under `.claude/workflow/`, the Jurati/WFH research, and SHD's local-model work.  
**Explicitly open:** implementation language, source/authoring representation, runtime substrate, and the
policy for when an LLM judgment is sufficient versus when a human must decide.

---

## The dream

Jurati is the **Borg Queen**: the deterministic control plane that uses agents and models to execute
standardized workflows. It owns workflow definitions and instances, phases, transitions, roles, gates,
budgets, recovery, routing, and authority. Models are capable workers inside that system; they do not own
the workflow or its enforcement.

The existing research garage is the first concrete architecture to lift:

- `.claude/workflow/{decompose-scope,research-scope,theme-scan}.md` defines phase graphs, gates, and
  orchestration;
- `.claude/agents/factory/*.md` defines roles, responsibilities, access boundaries, and output contracts;
- `.claude/skills/*/SKILL.md` defines reusable procedures and specialist capabilities;
- templates and artifact paths define inputs, outputs, evidence, and proof bars;
- Claude Code currently acts as the implicit interpreter/runtime joining them together.

Jurati would make that architecture explicit, executable across models, and visible in a UI resembling an
Obsidian Canvas: linked workflow, phase, agent, skill, policy, gate, and artifact objects; plus a live view
of running instances. Linked Markdown is one plausible authoring representation, **not a settled source
language**. The semantic model and its round-trip behavior matter more than the storage syntax.

The UI is not merely documentation. It is an authoring and operating surface over the same workflow
semantics the runtime executes: active phase, assigned agents, pending decisions, authority, spend,
evidence, denied actions, and transitions.

## Product boundaries

### Jurati — execution and authority

Jurati owns:

- versioned workflow definitions and live workflow state;
- phase, role, task, and transition semantics;
- scheduling, model/agent selection, gates, budgets, retries, and recovery;
- construction of the operating context presented to a model;
- derivation and enforcement of phase-scoped capabilities;
- the sole mediated path from model-proposed intent to external effects;
- high-volume runtime events and real-time behavioral assessment.

Jurati is **not** merely a security proxy. Security is one consequence of making LLM calls subordinate to
a workflow and rules system.

### Unimatrix — durable memory for agentic workflows

Unimatrix remains purposefully **not a workflow engine**. Its product ambition is to be the best durable
memory platform for agentic workflows.

Jurati tells Unimatrix the operating context — workflow, definition version, phase, role, and task — and
Unimatrix returns relevant durable knowledge. Jurati owns and advances the phase; Unimatrix is phase-aware
so it can retrieve well. Jurati may distill durable evidence, lessons, decisions, and capabilities into
Unimatrix, but raw workflow state and event streams do not become knowledge merely because they occurred.

The clean division is:

> Unimatrix remembers what agents need and learn. Jurati directs what agents do.

### SHD — sovereign, economical inference

SHD supplies local-first model capacity and controlled frontier escalation. Deterministic state machines
and policy evaluation are cheap without local inference; what SHD makes economical and sovereign is the
continuous semantic work around them:

- phase-conformance assessment;
- proposed-tool-call inspection;
- long-trace interpretation and drift detection;
- artifact assessment;
- competence and reliability estimation by task;
- shadow evaluation and selective escalation to frontier models.

Together:

> SHD provides sovereign model capacity. Jurati converts that capacity into governed agency. Unimatrix
> supplies durable memory and evidence.

Each remains a product with an independent boundary. Their integration is stronger than collapsing them
into one product.

## Shared phase context, without shared ownership

A standardized workflow makes phase an unusually powerful coordination primitive. Certain activities,
information needs, tools, risks, and outputs are predictable by phase.

Jurati can issue an integrity-bound operating envelope such as:

```text
(workflow instance, definition version, phase, role, task)
```

From that envelope:

- Unimatrix answers **what should this agent know now?**
- Jurati answers **what may this agent do now?**
- the runtime can assess **is what this agent is doing consistent with now?**

The model must not self-report or modify the authoritative phase. Phase changes occur only through the
workflow engine's transition rules.

## Trusted context and the sole tool path

Knowledge injection and security-context injection are related but not identical payloads carried through
the same trusted mediation seam:

- retrieved knowledge may be advisory;
- security context must be integrity-bound, non-overridable, and enforced downstream.

Putting security instructions outside the editable conversation is insufficient. A security boundary
requires:

1. the model cannot modify authoritative workflow or policy state;
2. the model has no alternate tool path;
3. the enforcing broker, not the model process, possesses the useful credentials;
4. every proposed effect is evaluated against trusted workflow/phase/role/task context;
5. widening authority requires a decision from outside the acting principal;
6. shell, networking, plugins, child agents, and alternate sessions cannot bypass the broker.

This implies layered enforcement. Sole-path is a **per-plane property**: tool mediation, credential
minting, filesystem authority, network egress, and deployment controls may require different enforcing
planes. Jurati may compile one declared authority model into several planes rather than attempt to become
one omnipotent enforcement runtime.

## Deterministic workflow around probabilistic judgment

The design should count on LLMs to perform semantic work well. It should not ask them to invent the
decision framework and its answer at the same time.

Jurati makes the **process deterministic**, not the intelligence:

```text
deterministic workflow state
        -> deterministically constructed decision
        -> LLM or human semantic assessment
        -> typed answer with evidence references
        -> deterministic validation and transition
```

Many apparently open-ended gates can be reframed as bounded, multiple-choice decisions. Jurati controls:

- the proposition being decided;
- the admissible evidence;
- mutually exclusive answer choices;
- the observable rubric for each choice;
- whether `insufficient evidence` or abstention is permitted;
- who may judge — code, local model, frontier model, multiple independent models, or human;
- what agreement or escalation policy applies;
- the transition caused by each accepted answer.

An LLM maps evidence to a bounded semantic answer. Jurati validates the response shape and executes the
consequence. Multiple choice does **not** make semantic evaluation deterministic; it makes the answer
bounded, inspectable, comparable, and executable.

### A candidate first-class primitive: the typed decision gate

```yaml
question: Did the artifact clear capability C1's proof bar?

evidence:
  - benchmark.json
  - validator-report.md
  - capability-C1.done_when

choices:
  pass: every required clause is demonstrated
  partial: at least one clause is demonstrated and at least one is not
  fail: the artifact is invalid or contradicts a required clause
  insufficient_evidence: no supported verdict is possible

response_requires:
  - choice
  - result_by_clause
  - evidence_references
  - unresolved_conditions

judge:
  type: policy-selected
  disagreement: escalate
```

The workflow language—whatever its representation—may need to treat this decision contract as a core
object alongside phases, roles, and tasks.

### Authority remains outside the assessor

A more capable model may be a better assessor; it does not automatically receive more authority.
Provisional policy:

- mechanical facts are checked by code;
- low-risk interpretation may accept one bounded LLM judgment;
- ambiguity may require independent judgments and agreement;
- security-sensitive decisions use LLM recommendations under deterministic policy or human approval;
- proof/firewall advancement retains a human gate until autonomous judging is itself proven;
- irreversible or high-impact effects remain human-authorized.

`High trust` may reduce supervision inside an already-authorized envelope. It must never create authority
the workflow did not declare.

## Real-time trust is evidence, not one magic score

Because Jurati knows the expected phase behavior and sees the mediated activity, it can develop real-time
trust assessments of agents, models, and configurations. Avoid collapsing this into an opaque scalar.
Retain an evidence vector including:

- identity and provenance;
- phase conformance;
- capability-use history;
- denied or anomalous attempts;
- artifact validity;
- task-specific competence and reliability;
- context/prompt integrity;
- human interventions and corrections required.

Trust is asymmetric: weak or uncertain evidence may narrow authority, require review, reroute work, or
stop a transition. Strong evidence may reduce supervision, but cannot widen the declared capability set.

## The visual workflow system

The intended UI is a linked canvas for both definition and operation:

- workflow and phase nodes with entry/exit conditions and transitions;
- agent nodes with role contracts, skills, model preferences, and capability envelopes;
- skill nodes with reusable procedures and dependencies;
- policy and decision-gate nodes with authority and evidence requirements;
- artifact nodes with inputs, outputs, and proof bars;
- live overlays for active phase, agent activity, pending decisions, cost, denied actions, and evidence;
- Unimatrix links showing durable context retrieved and knowledge produced.

The UI and any textual representation must not become drifting sources of truth. The semantic workflow
graph needs stable identities, versioning, validation, and lossless enough round-tripping for both human
and machine authors. Whether that graph is authored primarily as linked Markdown, structured data, a graph
store, or a hybrid remains open.

## Model and runtime portability

Claude-specific workflows are the first corpus, not the permanent architecture. Jurati should target
Claude, Codex, Gemini, local models, and other agent runtimes through adapters while reporting honestly
which guarantees survive on each target.

OpenCode is therefore a possible substrate or experimental specimen, not an architectural commitment. Its
implementation language need not determine Jurati's. Prefer a bounded integration/probe before a fork;
fork only if a required interception or isolation boundary cannot be achieved externally. The privileged
core should be chosen for auditability, isolation, deployment targets, policy integration, and the ability
to remain small—not for superficial alignment with a candidate harness.

## Working synthesis

> **Jurati is a visual, workflow-native control plane for governed agent teams. It executes standardized
> phase-based workflows, constructs bounded decisions for models and humans, derives authority from the
> current operating context, mediates the path from model intent to external effects, and uses Unimatrix
> as durable workflow-aware memory. SHD makes continuous local semantic assessment and selective frontier
> escalation economical.**

This is the evolution to sleep on. It is intentionally a working synthesis, not a ratified architecture.

## Questions deliberately left open

1. What is Jurati's implementation language and smallest trusted core?
2. What is the canonical workflow representation, and what must round-trip through the canvas?
3. Which objects belong in the core language: phase, role, task, skill, artifact, policy, decision gate?
4. Which enforcement planes are required for the personal/local tier?
5. How are phase assertions and retrieved context integrity-bound across Jurati and Unimatrix?
6. Which decisions may one LLM make, which require a quorum, and which remain human gates?
7. How is judge quality measured without letting the judge grade itself?
8. What evidence vector supports trust assessment, and which policies may consume it?
9. What is the first end-to-end proof using the existing research garage and Unimatrix MCP surface?

