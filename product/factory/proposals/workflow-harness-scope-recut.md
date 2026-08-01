# JURATI — goals, re-cut against the wfh-005 evidence

**Status:** proposal · **Author:** owner-directed, drafted at the wfh-005 gate, 2026-08-01
**Supersedes:** the first draft of this file (same date), which framed the object as *a bound, not a
harness*. That was too narrow — the bound is one goal of six.
**Standing:** **not a wfh-005 verdict.** The run is advisory and forbidden from reshaping its own theme
(the failure that closed wfh-002). This is the owner's direction, written down so it can be ruled on. It
does not amend `themes.md`, and it settles neither the architecture option under review nor the
definition-versus-events backend question.
**Evidence:** `product/research/wfh-005/reports/triage.md` + amendments 1 and 2.

---

## What JURATI is

The deterministic control model in front of the substrate — the single edge where LLM calls originate,
where sequencing, authority and spend are decided **outside the model's context**.

## Who it is for

**A solo developer with no infrastructure to run.** No orchestrator, no service mesh, no daemon. They want
their agents and their data bounded, and they will not stand up a control plane to get it. That user is
currently unserved: every shipping instance of real enforcement charges an infrastructure toll.

## The staging rule

**Architect the hard parts for enterprise. Build only the personal, open-source tool.** Enterprise lives in
its own repositories as a second codebase — not a tier, not a feature flag. The move between them is an
extension, not a rewrite, and what makes that true is getting a small number of security seams right on day
one: **principal identity · credential minting · isolation boundary · attestation trust root · the plane
interface.** Name them in the design; do not merge the tiers into one deliverable.

---

## The goals, ranked

### 1. The bound — authority an agent cannot argue with

Two things to build, and only two. Everything else in this space has a shipping counter-example.

- **Bounds derived from demand observed during execution.** Every shipping system derives authority from a
  declaration written *before* the run — a manifest, a policy file, a task string, frontmatter. An agent's
  demand set is discovered while it works. Derive from observation instead. The nearest prior art (AWS
  IAM Access Analyzer, `audit2rbac`) does this for programs, never for agents.
- **Monotone, with approval to widen.** Narrow freely and unilaterally; widen only through an approval
  whose issuer is not the principal. Both halves ship separately in the wild; nothing composes them.

**Enforced by a plane we never build.** Solo tier: a second user account (kernel-enforced, free, already
installed), the harness's own pre-tool hook (evaluated by a process the agent does not control), and a
local egress proxy as the next rung. Enterprise tier, later, in the second codebase: a sidecar and eBPF, or
a CI platform's derived job identity.

**Every plane must prove it is switched on.** Before a run, attempt one action the ceiling forbids and
confirm the right plane refuses it. Record the refusal, and record the **effective** configuration rather
than the declared one. Two of the three serious codebases read in this run were shipping controls that were
present, believed, and inert — and a vacuous guarantee passes every test a real one passes.

### 2. Many agents, many models — and honest comparison across them

- **Run multiple coding agents, and let a workflow choose a different one per task.** Table stakes, not
  differentiation — four-engine support ships under a permissive licence elsewhere, and an AI gateway makes
  model substitution a base-URL change. Build it because it is cheap and necessary, not because it is a moat.
- **Compare outcomes across those choices, anchored to proof rather than opinion.** This is the
  differentiated half and it is not in the eight concerns at all. The best evaluation harness in this space
  measured its own LLM judge and published the result: the conformance score moves a mean of 0.18, and as
  much as 0.92, across paired reads of *identical* code — on a metric whose pass bar is exactly 1.00.
  **Behavioral proof (`done_when` / `proven_by`) is a steadier instrument than a model's opinion, and we
  already run it.**

**Take the ideas, not the code.** Worth integrating: the two-opinion challenge design (the second reader is
handed what the first said was missing and told to go find it) · the third state that says *inconclusive*,
so an infrastructure hiccup is never recorded as a failure · half credit for a self-repaired pass · the
abort that stops a whole experiment when runs write nothing, because a model that cannot do the task still
writes *something* · and recording the effective value of every knob, never the configured one.

**One tension to design for rather than discover.** An evaluation harness deliberately *maximises* agent
authority — a bound is a confound when you are measuring capability, and the best one in the field disables
every permission gate on five of six runners. A governance harness minimises it. **Same product, opposite
settings.** That needs an explicit mode, and the mode must be recorded in the result.

### 3. Workflow definitions people can actually write

Markdown first — authored, versioned, diffable, in the repository. **Visual is not a natural later step.**
The visual authored-workflow canvas category was deprecated at the top of the market eight months after
launch, and an earlier scan already folded the canvas tools into a single dead-end. If we go there, the
scope states why ours is different; it does not assume the progression.

### 4. Cost metering and pre-authorised spend

Ratified as queen-side because the queen makes the calls, and explicitly declined by the knowledge layer.
**But pre-authorised spend per unit of work now ships** — as a cost ceiling checked before dispatch, and as
a gateway that returns a hard error when a budget is exceeded. This is adopt-and-assemble, not build.

### 5. Sequencing determinism

JURATI's founding purpose and still unglamorous: the state machine, wave sequencing, gate invocation,
branch and worktree discipline, commit-before-gate. The control flow a model does unreliably.

### 6. Introspection — of authority, not of traces

Tracing is commoditised and practitioners are satisfied with it. **Authority audit is not.** Scope this to
*what was this role permitted to do and spend, at this step, and why* — plus the live view of a running
workflow. Do not build another tracer.

---

## Deferred, with the condition that would re-open each

**One queen across many repositories** — after the single-repo case is proven. **Domains as subgraphs on a
shared ontology** — after the vocabulary survives a second domain. **Multi-tenant hosting** — see the
tension below. **Separate stores for workflow definition versus telemetry** — after there is telemetry
worth splitting.

## Dropped

The novelty claim (prior art on all three legs, from five unrelated fields) · rebuilding an enforcement
plane of any kind · adopting an evaluation framework wholesale · harness-as-runtime · counting model calls
as a proxy for safety.

## Open, and not settled here

- **The unclaimed asset.** The loudest measured failure in the field is agents reporting success they did
  not achieve. No capability bound touches it; artifact-backed proof does. It appears nowhere in the eight
  concerns, and it is the one thing external measurement independently says is needed.
- **A live tension with the SaaS-from-start premise.** `themes.md` currently states JURATI is built
  multi-tenant from the start, *not* a single-user tool retrofitted later, and makes multi-tenancy the
  trigger that pulls the hardest security substrate forward to foundational-now. **Open-source-first with
  pre-architected seams is a different claim.** Whether that premise is revised, scoped to the second
  codebase, or held as written is an owner decision, and this proposal does not make it.
