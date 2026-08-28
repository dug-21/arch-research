# wfh-009 — portable, ruvnet-ecosystem-free concepts in the MetaHarness packages wfh-008 never opened

**Status:** held — tech-discovery artifacts complete; coverage audit and synthesis not started
**Goal(s):** workflow-harness — inform the smallest defensible personal-OS/Jurati substrate (primary)
**Capability target(s):** **none.** This run advances no Unimatrix capability id and no grade, exactly as
wfh-008 did not. It produces a concept register and, if the curator distils it, `finding` nodes and at most
`claimed` structure. Stated plainly rather than invented.
**Confidence-required:** directional
**Phase / area:** workflow-harness · concept harvest · Jurati architecture input
**Cycle topic / Issue:** `wfh-009` · [Issue #67](https://github.com/dug-21/arch-research/issues/67)
**Target pin:** `ruvnet/metaharness` @ `6f8c60216f47eac391a076fe27fd804470a07e10`
(local static checkout `/tmp/wfh-008-metaharness`; `git rev-parse HEAD` confirmed against the pin)
**Predecessor:** wfh-008 ([Issue #66](https://github.com/dug-21/arch-research/issues/66)) — this run is a
deliberate **narrowing** of it, not a broadening.

---

## The question

wfh-008 concluded that MetaHarness's value to this theme is conceptual, not extractable (`#319`). Its own
goal-owner review then established that the conclusion rests on roughly a third of the repository: W5 never
opened ~25 of the 42 npm workspace packages and published no selection criterion, and the run's two best
concepts — the `sandbox.ts` operation-probe and the ARC bridge framing layer — were found by an
**auditor**, in packages W5 had skipped (`#323`). wfh-009 opens the rest, and only harvests ideas.

> Which portable, **ruvnet-ecosystem-free CONCEPTS** exist in the MetaHarness workspace packages wfh-008
> never opened — stated so we could build them ourselves, taking none of the code?

## Why it matters

The theme's objective is the smallest defensible personal-OS/Jurati substrate — one whose enforcement lives
**outside the governed party's reach**. wfh-008 produced a strong negative (no adoptable authority boundary)
and four genuinely new concepts, both from a partial read. Either the unread two-thirds holds more of the
same kind of idea, or it does not; both answers are worth having, and the second one closes the theme's
MetaHarness track honestly instead of leaving an open "we never looked."

The base rate that motivates the run is two-for-two: the last two packages opened by an outsider yielded the
run's two best units. That is a reason to look, not evidence that more exists. **This scope does not
predict a yield, and a run returning "nothing portable" across the board, with per-package reasons, is a
PASS.**

## Constraints — the spine  *(all five bind every workstream)*

### C1 — No code, at any altitude

The human has excluded taking any MetaHarness code. **No extraction dossiers, no minimum dependency
closures, no seam quality assessments, no licence closures, no "reuse candidate" dispositions.** If a
mechanism is interesting, the deliverable is *the idea stated so we could build it ourselves* — never the
file to import, never the import path, never a diff.

This is a genuine narrowing of wfh-008, and it makes the run **cheaper**: everything wfh-008's W5 spent on
seam quality, licence and closure is simply not performed here. Quoting a short line of source **as
evidence for a claim about the idea** is allowed and expected under C3; proposing that any line be taken is
not. If a researcher finds itself pricing extraction, it has left the scope.

### C2 — Zero ruvnet-ecosystem dependency, enforced at the MECHANISM level

wfh-008 found (`#316`, `#317`) that the executable coupling runs harder to **RuVector** than to ruflo, and
that MetaHarness declares **no ruflo/`@claude-flow`/`agentic-flow` package or crate edge at all** — the
ruflo ties are ancestry, copied contracts, aliases and config names. "ruflo-free," read literally, would
therefore wave through a concept welded to the ecosystem anyway. The binding test is:

> A concept qualifies only if it is **statable and implementable with zero dependence on** ruflo, RuVector,
> agentic-flow, branded ecosystem contracts, `RUFLO_*` state/env namespaces, or registry defaults.
> A mechanism that only works because something upstream supplies it is a coupling in disguise: record it
> **disqualified by ecosystem coupling**, and **name the upstream it needs.**

Two precisions, because both mistakes are easy and both are expensive:

- **The test runs on the CONCEPT, not on the package's dependency list.** A package that imports
  `@metaharness/kernel` is not thereby disqualified; the question is whether the *idea* survives with the
  kernel deleted. Applying the test to manifests instead of mechanisms would disqualify most of the
  repository and produce a false negative for the run.
- **It is not only npm edges.** A concept whose statement requires a branded contract shape, a registry
  default, a named env namespace, or an upstream service is coupled even when nothing appears in a
  manifest. Manifest-declared upstreams already visible in this alphabet and requiring the test —
  `agenticow` (declared by `avo`, `jujutsu`), `agentic-jujutsu` (declared by `jujutsu`) — are **named here
  as things to test, not as findings**; this scope asserts nothing about their ownership or nature.

### C3 — Evidence firewall, identical to wfh-008

Every material statement carries exactly one label: **source claim** (documentation, README, manifest
`description`, comment, name, marketing assertion) · **static code evidence** (a traced authored/generated
code or configuration path) · **prior demonstrated evidence** (an artifact demonstrated by an earlier run) ·
**unverified-inference**.

Static reading only, against the pinned commit at `/tmp/wfh-008-metaharness`: clone, read, index, inspect.
**No install, build, test, generator run, service, container, or model run.** Static evidence establishes
structure and reachable-looking paths; it never establishes that a path executes. **Nothing produced here
is demonstrated-by-us evidence, and nothing reaches `partial` or `proven`.**

Note the trap this target sets, `#324`-style: several packages *describe* mechanisms far stronger than they
implement. A `description` field is a **source claim** and must be labelled as one, even when it is the
only thing that made the package interesting.

### C4 — Novelty graded against the live graph, not asserted

Before reporting a concept as new, check it against the live graph via
`context_graph(mode:"current", id:<N>, detail:"full", agent_id:"factory-researcher")` for **#200, #277,
#316, #317, #318, #319, #323, #324, #325, #326**. Read them; do not rely on this scope's summaries of them.

Every reported concept carries **exactly one** grade:

- `new` — no node holds it, in any form.
- `sharpens <id>` — a node holds the ground; this states it more precisely or in a new setting.
- `already held by <id>` — the node already says this.

wfh-008's goal-owner found that several items presented as new (deny precedence, monotone delegation,
external custody as admission condition, gate-input independence, pre-decision/post-receipt) were
**sharpenings of already-`claimed` ground** at `#200`/`#277`. That is the specific error to avoid.

> **Anti-goal, explicit:** volume. **A run that returns four genuinely new concepts and says so is worth
> more than one returning twelve that blur the line.** A `sharpens` grade is a good outcome, not a
> demotion; an over-graded register is a defect the synthesis gate should reject.

### C5 — The custody predicate is an EVALUATION INSTRUMENT, not a finding

wfh-008 recorded the predicate (`#318`, `#319`):

> **A control whose input, custody, or call-site enumeration sits inside the governed party is a label,
> not a control.**

In this run it is an **instrument**. Every candidate control-shaped mechanism is run through it and the
verdict reported in the register: *passes* (input, custody and call-site set all sit outside the governed
party) · *fails on input* · *fails on custody* · *fails on call-site enumeration* · *not control-shaped*.

It caught seven independent MetaHarness subsystems by inspection in wfh-008. This run tests whether it
catches more — **and reports honestly if it catches nothing.** "The instrument found nothing here" is a
result about the instrument and is worth recording; a manufactured eighth instance is not.

## Known constraints & prior art  *(build on these — do not re-derive)*

**Read these before opening the repository. Every one of them is ground already paid for.**

wfh-008 documents (`product/research/wfh-008/`):
`findings-W1.md` · `findings-W2.md` · `findings-W3.md` · `findings-W4.md` · `findings-W5.md` ·
`findings-W6.md` · `findings-W7.md` · `REPORT.md` · `reports/coverage.md` · `reports/coverage-r2.md` ·
`reports/relevance.md` · `SCOPE.md`.

Live graph nodes (read via `context_graph(mode:"current")`, never from a summary):

| id | what it holds, and why it binds this run |
|---|---|
| `#200` | ruflo `policy/` subtree — **ASSEMBLE the envelope algebra**. Holds monotone envelopes, deny precedence, approval machinery, pre-authorised spend, and the inert-by-default position. Most authority-flavoured "new" concepts collide here first. |
| `#277` | Plane-per-leg enforcement admission map — OS sandbox owns resource effects; attribution is self-assertion and cannot authorize. |
| `#316` | MetaHarness `technology` node, `grade:claimed` — the characterization this run must not contradict silently, and the portable-concept list already recorded. |
| `#317` | Architecture as independently closed surfaces; the **enumeration-alphabet** correction. |
| `#318` | Gates establish no independent authority boundary; the fail-open execution boundary; the custody predicate's source. |
| `#319` | The wfh-008 **position** — take the concepts, not the code. The TAKE / DO-NOT-TAKE list this run extends. |
| `#323` | **Alphabet lesson.** A sweep inherits the blindness of its own alphabet; name it or the sweep does not count. This is why the coverage rule below is written the way it is. |
| `#324` | Verification does not spread sideways — a verified claim is no warrant for the sentence beside it. |
| `#325` | Vendored-skill install reverts local skills — why `.claude/` is untouchable in the envelope below. |
| `#326` | Unimatrix write-surface corrections: rejections were payload-shape (512-byte `outcome`, 8000-byte `content`), `agent_id` present. Keep writes inside those bounds. |

Mechanical coverage universe, already committed: `product/research/wfh-009/reports/package-universe.md`.
It is a measurement, not a source — **researchers read the repository, not that file, for anything
substantive.**

## The workstream partition — the RULE, then the assignment

### The rule (reproducible by a later auditor)

> Packages are partitioned by **mechanism family as declared by the package's own manifest `description`
> field, and by its `README.md` where one exists** — **not** by directory name, size, LOC, or alphabetical
> order. Where description and README disagree, the `description` governs (it is the shorter, more
> deliberate self-statement). Where a package declares **no** description and **no** README, it falls to
> the workstream owning its nearest declared first-party dependency; if that is also absent, it is assigned
> by its source-tree entrypoint and the assignment is marked `by-fallback` in the findings file.

**Known applicability gap, stated rather than papered over:** six of the 25 Tier-1 packages —
`evals-extract`, `evals-hle`, `evals-math`, `evals-servedmodel`, `evals-sql`, `evals-toolcall` — carry **no
`README.md`** [static code evidence]. Their assignment rests on the `description` field alone, which in each
case declares "benchmark adapter for `@metaharness/flywheel` … promotion gate" [source claim]. The rule
survives, on its first clause; the auditor should know it is running on one leg for those six.

**A package's home workstream does not restrict which concept family it may report.** The partition
allocates *reading*, not *conclusions*. If `vertical-trading` (W3, by its declared "vertical pack" framing)
turns out to hold a bounded-autonomy mechanism, W3 reports it as such and the register files it by concept,
not by owner. Cross-workstream concepts are handed to the leader, not silently absorbed or duplicated.

### The assignment

**W1 — self-improvement and promotion gates.**
What mechanism does a self-improving harness use to decide that a change earned promotion, and what part of
that is statable without the model, the benchmark, or the ecosystem?
*Tier 1 (9):* `flywheel`, `evals-extract`, `evals-hle`, `evals-math`, `evals-servedmodel`, `evals-sql`,
`evals-toolcall`, `bench`, `weight-eft`.
*Output:* `findings-W1.md`.

**W2 — bounded autonomy, receipts, and adversarial containment.**
How is an autonomous loop bounded, made replayable, and contained against an adversary — and which of those
bounds are real mechanisms rather than declared ones?
*Tier 1 (4):* `avo`, `redblue`, `turn-credit`, `arc-agi-3-chatgpt`. *Tier 2 (2):* `horizon`, `oo-agents`.
*Output:* `findings-W2.md`.

**W3 — host projection, SDK surface, and vertical contracts.**
How is one definition projected onto many heterogeneous hosts, what is lost in each projection, and how is
that loss represented — the portable half of "build once, run under any harness"?
*Tier 1 (8):* `host-codex`, `host-copilot`, `host-hermes`, `host-openclaw`, `host-pi-dev`, `sdk`,
`vertical-base`, `vertical-trading`.
*Tier 2 (5):* `host-claude-code`, `host-github-actions`, `host-opencode`, `host-prime-agent`, `host-rvm`.
*Output:* `findings-W3.md`.
*Note on shape:* eight of the thirteen are 2-file adapters of ~200–380 lines. The concept density is in the
**contract they all satisfy** and in what each one cannot express, not in any single adapter.

**W4 — agent state, coordination, and introspection signals.**
How is agent state versioned, shared between agents, and made observable — and can any of it be stated
without the upstream packages that supply it?
*Tier 1 (4):* `jujutsu`, `radio`, `workspace-lens`, `workspace-probe`. *Tier 2 (1):* `aws-finops`.
*Output:* `findings-W4.md`.
*Note:* `jujutsu` and `avo` declare third-party upstreams (`agentic-jujutsu`, `agenticow`); C2 runs on them
before any concept from those packages is reported.

**Partition dissent recorded at this gate** (the leader/coordinator rules; the scope does not re-cut
silently): three assignments do not follow cleanly from the stated rule — `aws-finops`, `turn-credit`, and
`arc-agi-3-chatgpt`. See *Amendments / open partition questions* at the foot of this file.

## Expected output

`product/research/wfh-009/` containing:

1. `findings-W1.md` … `findings-W4.md` — one per workstream, each opening with its **declared alphabet**
   (C6 below) and containing the per-package coverage table.
2. `reports/coverage.md` — the independent coverage audit. **Its author must have authored none of the
   findings.**
3. `REPORT.md` — whose **core is a concept register**.

### The concept register — the deliverable

One row (or short block) per concept. Required fields, all of them:

| field | content |
|---|---|
| **concept** | the mechanism, named and stated as an idea we could build |
| **why** | why it matters to a substrate whose enforcement must live **outside the governed party's reach** |
| **how** | how it would be used in practice — the concrete setting, not a restatement of the concept |
| **novelty** | exactly one of `new` · `sharpens <id>` · `already held by <id>` (C4) |
| **custody verdict** | the C5 instrument's ruling, including `not control-shaped` |
| **evidence** | source claim · static code evidence · prior demonstrated evidence · unverified-inference (C3) |
| **provenance** | where the package declares an **external origin** for the mechanism (a paper, a named prior system, a standard), record it — see the dissent below |

> **Binding on the synthesis phase: concise entries. The register IS the deliverable; the prose around it
> is not.** No narrative section may restate a register row. If a concept cannot be stated in a register
> entry, it is not yet a concept.

## Coverage rule  *(binding on every workstream — `#323`)*

**C6 — name your alphabet, explicitly, in the findings file, before claiming any sweep complete.** State
the exact enumeration rule, as a reproducible command where possible, and state what is *not* expressible
in it. **A sweep that does not state its alphabet cannot be audited and does not count.** Sweep the
*question* set, not the answer set — mechanism families, not the names of mechanisms already known.

**Coverage is met when every Tier-1 package in the workstream is owned by exactly one row** carrying one
stated verdict:

- `concept found` — with the concept (which then appears in the register);
- `nothing portable` — with **why**, specific to that package;
- `disqualified by ecosystem coupling` — **naming the upstream** it needs.

**Silence about a package is not coverage.** Tier-2 packages are carried on the same row schema but are
**not binding for PASS**; a Tier-2 row may read `not reached`, with that said plainly.

**`#324` — verification does not spread sideways.** A verified claim is no warrant for the sentence beside
it. Audit by *fact* (grep every site asserting it, rule on all at once), and record scope **negatively**:
say what was not checked, not only what passed.

**The coverage auditor must be an agent that authored none of the findings.** Blocking gate. REWORK ≤ 2.

## Proof bar  *(D7 — what would move status)*

**Nothing in this run moves status. Directional; structure only.**

This run produces findings and, at most, `claimed` structure and a `position`. It does not execute
MetaHarness, validate anything, establish runtime behaviour, or advance any technology or capability to
`partial` or `proven`. The owner's tests, CI, benchmark bundles, ADR references and submissions are
**source claims**, never demonstration by us.

Any later claim that a harvested concept *works* requires a separately approved empirical/validated scope
building an artifact at that claim's altitude, **demonstrated and independently validated by us** — and,
per `#319` §7 and the goal-owner's D1, such a follow-on should be built against **our own** intended
enforcement plane, not against MetaHarness.

## Envelope  *(binding)*

- **Confidence:** directional. **External cost: 0. Compute: none. Concurrent runs: 1.**
- **No grade past `claimed`. No capability advanced. No `Prerequisite`, `Cites` or `Tests` edges.**
- Researchers **read** Unimatrix (`context_search`, `context_get`, `context_graph`) and **write nothing**.
  Only the curator writes, and only after the coverage gate. Every `context_*` call carries
  `agent_id` = the acting role (D6).
- Keep writes inside the payload bounds `#326` records: `context_cycle` `outcome` ≤ 512 bytes, `content`
  ≤ 8000 bytes.
- Research documents commit to `main` as produced (D15), **path-scoped to
  `product/research/wfh-009/`**. No executables, so no branch and no PR.
- **`.claude/` and `.devcontainer/` are untouchable** — see `#325`.
- Escalate under coordinator authority: theme revision · material spend · a validated scope · a build
  recommendation · a cross-theme dependency · any `proven` grade change.

## Explicitly out of scope

**Method / posture:**

- Any code-taking activity at any altitude: extraction dossiers, dependency closures, seam-quality
  assessment, licence or provenance closure, `adopt`/`assemble`/`reuse candidate` dispositions (C1).
- Adoption, implementation, migration, procurement, or ratification of `jurati-arch-002`.
- Installation, builds, tests, benchmarks, generator runs, services, containers, model or agent runs, or
  any compute-bearing proof (C3).
- Re-performing wfh-008: its architecture map, dependency graph, ecosystem-coupling ledger, generation
  chains, authority map and maturity assessment are **inputs**, not topics.
- A competitor scan, a fresh literature review, or a survey of other ruvnet repositories.
- Dynamic vulnerability work, exploit development, secret access, or claims about deployed environments.
- Jurati product/UI/data-model design, or a build recommendation of any kind.

**Alphabet — the declared holes.** These are excluded **by this run's scope, not by a finding that they are
empty**, and no statement here should be read as a claim about their contents:

- `crates/*` (`kernel`, `kernel-napi`, `kernel-wasm`, `poker-darwin`, `template-catalog`)
- `apps/web-ui` · `services/apicompletions` · `kimi-k3-harness`
- `examples-packages/*` · `experiments/` · `submissions/` · `scripts/` · `docs/` · `__tests__/`
- The **9 packages wfh-008 already examined**: `agent-harness-generator-lib`, `agntcy`, `arc-agi-3`,
  `create-agent-harness`, `darwin-mode`, `harness`, `kernel-js`, `projects`, `router`.

The run is scoped to **npm workspace packages** (`packages/*`, the glob the root manifest declares). Every
surface above sits outside that scope. Any of them may be a future scope; none is a gap in this one.

## Coverage / done call  *(synthesis)*

Not loop-until-dry — **ledger-based**, because the alphabet here is closed and enumerable (42 workspace
members, 25 Tier-1, 8 Tier-2, 9 excluded as examined). The run is done when:

1. Every Tier-1 package is owned by exactly one row with one of the three verdicts (C6);
2. Every workstream has declared its alphabet, and stated what that alphabet cannot see;
3. Every register entry carries all seven required fields, including a novelty grade checked against the
   live graph and a custody verdict;
4. An auditor **who authored none of the findings** rules PASS on 1–3, auditing by fact and recording its
   own scope negatively.

The leader proposes sufficiency; **the human confirms at the synthesis gate.** A technology discovered
outside this alphabet is captured as a follow-on candidate, never absorbed.

---

## Amendments / open partition questions  *(for the scope gate to rule on)*

*Append-only. Nothing below has been acted on; the partition above is the one in force unless the gate
changes it.*

**Q1 — `aws-finops` is assigned to W4 but reads as W1 under the stated rule.** Its manifest describes
"multi-tier cascade, deterministic execution oracle, shrinking residual … only verified savings are
reported, behind a human review gate" [source claim] — a promotion-gate mechanism family, not agent state,
coordination or introspection. Tier 2, so non-binding for PASS, but applying the rule inconsistently in the
one visible place weakens the rule for the auditor. *Proposed:* move to W1, or record `by-exception` with a
reason.

**Q2 — `turn-credit` (Tier 1) is assigned to W2 but its declared mechanism is a promotion signal.** Its
description states "advisory signals for routing, retry policy, retrieval feedback, and **Darwin mutation
promotion**. Never reverses the verifier's decision" [source claim]. The first half is W1; the second half —
an advisory channel structurally forbidden from overriding the authority channel — is a genuinely W2-shaped
property and may be the portable concept in it. *Proposed:* leave in W2 **and say why in the findings
file**, since the interesting property is the separation, not the credit assignment. This is a borderline
the rule does not resolve on its own, and the auditor should see that it was noticed.

**Q3 — `arc-agi-3-chatgpt` (Tier 1) is a host projection by its leading clause.** "Experimental ARC-AGI-3
remote MCP harness for ChatGPT Developer Mode, with durable memory, guarded plans, supervision" [source
claim]. The leading clause is W3; the trailing clause is W2. Under the rule as written, the description
governs but does not disambiguate within itself. *Proposed:* leave in W2 (the trailing clause names the
mechanisms; the leading clause names the host), with W3 notified so the projection angle is not lost.
Additionally, it is the only Tier-1 package declaring a first-party edge to `arc-agi-3` — a package
wfh-008 **did** examine — so W2 must not re-derive that ground.

**Q4 — a missing register axis: external attribution.** This is the one substantive gap this scope's author
found in the brief's constraint set, and it is why `provenance` appears as a seventh register field above.
Several packages in the alphabet **declare that their mechanism comes from published third-party work**
[source claim, from manifest descriptions]: `turn-credit` cites arXiv:2608.05987 (AgentOPSD); `radio` cites
arXiv:2607.28430 (AgentRadio); `oo-agents` describes itself as "a TypeScript clone of NOOA
(NVIDIA-NeMo/labs-OO-Agents)"; `workspace-lens` cites an Anthropic 2026-07-06 result; `redblue` names NIST
AI RMF and the OWASP LLM Top-10; several packages cite internal ADR numbers.

C4 grades novelty **against our own graph only**. That axis cannot distinguish *"MetaHarness invented this"*
from *"MetaHarness implemented someone else's published mechanism."* A concept graded `new` on the C4 axis
may be a well-known published result, in which case the citation we should carry is the **upstream**, not
MetaHarness, and the honest next move is to read the source rather than the clone. Recording the declared
origin costs nothing — the description fields already state it — and it feeds the theme's derived watchlist
directly, since D14 provenance (`org` / `author` / `year` / `surface`) is what makes "who keeps appearing"
computable. **Recording the declared origin is in scope; reading the upstream paper is not** (that would be
a literature surface, and this run does not open one).

---

## Hold record — 2026-08-28

**Human direction:** hold this run before synthesis while the `workflow-harness` theme is revised around
the broader agentic-organization target and its common-vocabulary hypothesis. This is a strategic pause,
not a failed run and not a ruling on the findings.

**Completed and preserved:** the approved scope, mechanical package universe, four workstream findings,
and their handoff-round addenda. These documents remain readable on `main`.

**Not performed:** independent coverage audit, curator distillation or any Unimatrix knowledge write,
coverage gate, synthesis/`REPORT.md`, goal-owner review, synthesis gate, cycle stop, Issue close, or
retrospective. No technology or capability grade moved.

**Cycle boundary:** the live cycle remains open in `tech-discovery`. The canonical cycle interface has no
hold/park event, and `tech-discovery` cannot honestly end until the independent coverage audit rules on
the existing findings. No synthetic phase event was issued.

**Smallest safe resume point:** first reconcile the approved scope's old personal-OS/Jurati framing with
the owner-approved agentic-organization target and decide whether synthesis needs a bounded scope
amendment. If the existing evidence remains in scope, commission an independent coverage audit over the
four preserved findings; only after a PASS may the curator and synthesis roles begin. Do not rerun the
four workstreams unless that audit returns a protocol-defined `REWORKABLE` verdict or the revised target
requires newly approved research.
