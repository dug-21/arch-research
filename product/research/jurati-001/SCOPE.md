# jurati-001 — Validated probe: a decision-contract language for deterministic next action

**Status:** synthesis — terminal feasibility ruling is SCOPE FAIL; failed/inconclusive synthesis in progress.
**Goal(s):** Jurati evolved vision (primary) · `theme:workflow-harness` · SHD model-routing evidence
**Hypothesis target:** the load-bearing Jurati premise derived from position #191 and
`product/factory/proposals/jurati-evolved-vision-2026-08-05.md`: success evaluation can be expressed as a
typed, executable decision contract that deterministically selects the next action, while any irreducible
semantic judgment is isolated and its minimum inference requirement measured.
**Capability target(s):** candidate Jurati capability — **evidence-bound decision evaluation and next-action
resolution**. No active Unimatrix capability node exists yet; this scope tests whether the capability is
coherent before one is asserted. It advances no existing capability grade by implication.
**Confidence-required:** **validated** — requires a working language/interpreter, a frozen cross-domain
corpus, and held-out replay demonstrated by us. A design or literature argument remains `claimed`.
**Phase / area:** workflow semantics · typed decision gates · inference policy
**Cycle topic / Issue:** `jurati-001` · GitHub Issue #58.

---

## The question

Jurati assumes that a workflow can state what success means precisely enough to bound evaluation and make
the resulting transition executable. Today, both the Unimatrix SDLC and the research garage frequently use
human or LLM judgment to interpret prose, decide whether evidence clears a gate, and choose what happens
next. This scope tests whether those decisions share an executable semantic core, and measures what degree
of inference—none, local, frontier, quorum, or human—is actually required for the residue.

> Can one structured decision-contract language represent and replay real SDLC and research-workflow gates
> such that evidence collection and next-action selection are deterministic, semantic judgment is confined
> to explicitly typed clauses, and a measured policy selects the cheapest reliable judge without permitting
> false advancement?

## Why it matters

This is a premise test, not a component choice. If historical decisions cannot be decomposed into explicit
evidence, independently evaluable clauses, bounded verdicts, and deterministic consequences—or if identical
evidence routinely needs an unbounded human reframing to select the next action—then Jurati's proposed typed
decision gate is not a viable core primitive. The broader vision would need to retreat from executable
workflow semantics to advisory orchestration.

If the hypothesis holds, it establishes the semantic kernel on which phase transitions, authority changes,
model routing, recovery, and the visual authoring system can later depend. It also gives SHD a concrete
routing problem: not “which model is best?” but “what is the cheapest judge policy demonstrated reliable
for this typed clause class?”

## Known constraints and prior art  *(build on these — do not re-derive)*

- **Jurati evolved vision** defines the candidate primitive: deterministic workflow state constructs a
  bounded decision; a code/model/human judge returns a typed answer with evidence references; Jurati
  validates the answer and executes the transition. Authority remains outside the assessor.
- **Position #191 (wfh-005)** wounded the scalar “minimize inference” thesis. The deciding leg must be
  deterministic, external, and monotone; inference may propose or assess when a deterministic checker sits
  downstream. The useful variable is the inference call's position and consequence, not the call count.
- **The Unimatrix SDLC corpus is the mature domain.** At scope time,
  `github.com/dug-21/unimatrix/product/features` contains 232 feature-cycle directories, 166 `SCOPE.md`
  files, 161 acceptance maps, 553 gate reports, and 163 risk-coverage reports. Representative cycles expose
  mechanical checks, semantic alignment review, PASS/WARN/FAIL, rework, variance, scope additions, and
  explicit gate consequences.
- **This repository is the younger research domain.** Its scopes, findings, artifacts, firewall rulings,
  amendments, and synthesis reports include partial evidence, insufficient evidence, scope failure, owner
  redirection, and grade advancement/refusal. `shd-007` is load-bearing because strong evidence was correctly
  prevented from advancing after one unmet clause was noticed.
- **wfh-002 is a failure precedent.** An unenforced prose boundary was crossed and an out-of-scope runtime
  decision was made. A language that merely restates prose without making the decision contract executable
  has failed this probe.
- Existing policy/checking technologies (Cedar/AgentCore, Progent, proof-carrying generation, ruflo's
  capability envelopes) demonstrate deterministic checking downstream of model-authored proposals. They do
  not establish that one gate language covers both of our workflow domains.
- Gate reports are evidence, not unquestionable truth. The historical outcome is the reference judgment;
  disagreements must be adjudicated and recorded rather than silently scored as model error.

## Hypotheses under test

### H1 — Cross-domain expressibility

A compact language can express both domains' decisions using shared primitives—evidence inputs, typed
clauses, judge class, verdict algebra, and transition table—without embedding domain-specific prose logic
or a bespoke evaluator for each historical gate.

### H2 — Deterministic consequence

Given accepted clause results, the final verdict and next action are deterministic and reproducible. No
model or human may invent a transition outside the contract.

### H3 — Inference can be isolated and measured

Most clauses are mechanically decidable or reducible to bounded semantic classification. For residual
semantic clauses, repeated evaluation can identify the least costly judge policy that meets the clause's
risk-weighted reliability bar; abstention and escalation are first-class outcomes.

### H4 — The language generalizes

A language and evaluator designed on a development set retain coverage and decision agreement on unseen
SDLC and research cycles. Success on training examples alone is refuted as transcription, not validation.

## The candidate decision contract

The experiment may revise syntax, but the semantic minimum is fixed for the probe:

1. stable decision and clause identities;
2. typed, integrity-addressed evidence inputs and admissibility rules;
3. clause evaluators typed as `mechanical`, `semantic`, or `human_reserved`;
4. bounded clause results such as `demonstrated | contradicted | not_demonstrated | insufficient_evidence`;
5. explicit criticality and fail/abstain behavior per clause;
6. a deterministic verdict algebra over clause results;
7. an exhaustive verdict-to-next-action transition table;
8. a judge policy that names eligible judge classes, repetition/quorum, disagreement, and escalation;
9. evidence references and per-clause rationale in every non-mechanical response;
10. schema validation that prevents a judge from changing the question, evidence set, choices, authority,
    or transition.

The language need not make semantic truth deterministic. It must make the **decision being asked, the
admissible answer, and the consequence** deterministic and inspectable.

## Frozen corpus and sampling

The corpus is frozen before evaluator tuning. A manifest records repository, commit SHA, cycle, artifact
paths, decision point, historical outcome, historical next action, and whether owner intervention changed
the outcome. No raw private transcripts or credentials enter the dataset.

### Domain A — mature SDLC (`dug-21/unimatrix/product/features`)

Select at least **30 decision episodes from at least 15 feature cycles**, stratified across:

- design/specification gate, implementation/code gate, final risk gate, and bug-fix gate;
- PASS, WARN/advisory, FAIL/rework, variance/escalation, and insufficient-evidence outcomes where present;
- mechanical acceptance checks, architectural/vision alignment, risk coverage, security review, and scope
  conformance;
- simple and complex feature cycles, with no single cycle contributing more than three decisions.

At minimum, include one complete mature feature chain (scope → acceptance map → gate 3a → gate 3b → gate
3c → alignment report) and one bug-fix gate. `vnc-047` and `bugfix-444` are candidate exemplars, not
mandatory held-out cases.

### Domain B — research garage (`arch-research/product/research`)

Select at least **12 qualifying decision episodes**, spanning at least:

- scope approval and coverage gates;
- directional synthesis and adopt/assemble/build/park routing;
- a validated firewall decision with `partial` or refused advancement (`shd-007` required);
- insufficient evidence or a declared hole;
- rework, early close, scope redirection, or frontier expansion (`wfh-002` required);
- a decision materially corrected by owner input, so the test does not train only on clean autonomous
  outcomes.

### Leakage control

- Split **by feature/research cycle**, never by individual decision: 50% language-development, 25%
  calibration, 25% sealed holdout in each domain.
- All decisions from one cycle stay in one partition.
- Freeze the holdout manifest and reference outcomes before finalizing the language grammar or prompts.
- A change motivated by a holdout failure creates a new language version and requires a new untouched
  holdout; it may not be rescored as if still blind.
- Historical reports may be transformed into structured evidence, but their verdict summary is withheld
  from judge inputs unless it is itself the evidence under test.

## Bounded investigation (workstreams)

- **W1 — Corpus and reference adjudication.** Build the frozen cross-domain manifest; extract each
  decision's evidence, clause obligations, historical verdict, and actual next action. Have an independent
  reviewer adjudicate ambiguous or internally inconsistent historical outcomes before they become labels.
  *Output:* `corpus/manifest.*`, evidence packets, reference labels, ambiguity register, and split hashes.

- **W2 — Decision-language semantics.** Derive the smallest shared semantic model from the development
  partition only. Specify grammar/schema, type rules, verdict algebra, transition completeness, evidence
  integrity, abstention, and judge-policy semantics. *Output:* versioned language specification plus
  mechanically validated example contracts for both domains.

- **W3 — Interpreter and replay harness.** Implement schema validation, mechanical evaluators, deterministic
  verdict reduction, transition selection, run logging, and a pluggable semantic-judge interface. The
  interpreter must reject missing transitions, undeclared evidence, malformed judge output, and attempts
  to widen the contract. *Output:* executable prototype, tests, and machine-readable replay results.

- **W4 — Inference ladder.** For each semantic clause class, run the same frozen evidence through:
  (A) mechanical-only with abstention; (B) one local model; (C) repeated/independent local judgments;
  (D) one frontier model; (E) independent mixed-model quorum; and (F) human reference. Pin model versions,
  prompts, decoding parameters, evidence, and repetition count. If a local endpoint is unavailable, record
  that arm as blocked—it may not be simulated by a public model. *Output:* clause-level reliability,
  variance, abstention, latency, and cost by judge policy.

- **W5 — Sealed cross-domain replay.** Run the frozen interpreter and predeclared judge policies against
  both holdout partitions without language or prompt edits. Compare clause results, verdict, and next action
  with the adjudicated reference. *Output:* held-out confusion matrices and disagreement dossiers, split by
  domain, clause type, consequence, and inference arm.

- **W6 — Adversarial and counterfactual checks.** Test persuasive prose with missing evidence, contradictory
  artifacts, irrelevant context, prompt injection inside evidence, a correct final verdict paired with an
  illegal transition, and one-clause counterfactuals that should change exactly one consequence. *Output:*
  safety report demonstrating whether the judge can alter the contract or bypass deterministic reduction.

- **W7 — Premise verdict and product consequence.** Classify the result as strong, viable, narrow, or
  refuted; state which Jurati primitive survives, which decisions remain human, and whether SHD routing by
  clause class is justified. *Output:* `REPORT.md`, a position finding, and—only if supported—a proposed
  Jurati capability node and a bounded follow-on product POC scope.

## Expected outputs

1. A frozen, provenance-bearing cross-domain decision corpus and ambiguity register.
2. A versioned decision-contract language specification and schemas.
3. A working interpreter/replay harness with deterministic reduction and transition selection.
4. Encoded development, calibration, and holdout contracts for both workflow domains.
5. Mechanical and semantic clause taxonomies, including unencodable cases.
6. Inference-ladder results with reliability, variance, abstention, cost, and latency.
7. Held-out next-action agreement and false-advancement results by domain.
8. Adversarial/counterfactual results.
9. A premise verdict and the smallest defensible next Jurati step.

## Measurement and proof bar

Report all results by domain and pooled; pooled success may not hide a failed domain. Clause-level and
next-action metrics are both required.

### Required measurements

- **Expressibility:** fraction encoded without changing the historical question or adding bespoke
  per-decision evaluator code; taxonomy of every exclusion or lossy encoding.
- **Mechanical share:** fraction of clauses and complete decisions requiring no inference.
- **Reference agreement:** clause-result, final-verdict, and exact-next-action agreement.
- **Safety:** false advancement rate, especially `advance/approve/proven` when the reference required
  rework, evidence, escalation, or stop.
- **Reproducibility:** repeated-run disagreement for each inference policy.
- **Abstention quality:** unsafe guesses avoided versus unnecessary escalations introduced.
- **Inference requirement:** cheapest policy meeting the predeclared reliability bar for each clause class.
- **Operational envelope:** model/version, prompt hash, repetitions, latency, and marginal cost.

### Validated success

The hypothesis is **supported** only if the sealed holdout demonstrates all of the following:

1. one shared semantic model covers both domains; syntax profiles may differ, but verdict and transition
   semantics do not;
2. at least 90% of eligible holdout decisions are expressible without bespoke per-decision evaluator code,
   with every exclusion explicitly classified;
3. deterministic replay produces the same verdict and next action on every repetition once clause results
   are fixed;
4. **zero false advancements** occur on the frozen holdout across the selected production policy;
5. exact next-action agreement is at least 90% in **each** domain, not merely pooled;
6. every disagreement is localized to named clauses and results in abstention/escalation rather than an
   undeclared transition; and
7. the experiment identifies a least-cost reliable judge policy per semantic clause class, even when that
   policy is `human_reserved`.

The percentages describe this bounded corpus, not universal accuracy. Confidence intervals and raw counts
must accompany them; a zero observed false-advancement count is not represented as proof of zero population
risk.

### Outcome taxonomy

- **Strong support:** the support bar clears and most complete decisions are mechanical or safely handled by
  local inference.
- **Viable support:** the support bar clears, but some bounded clause classes require frontier or human
  judgment. Jurati remains viable as the deterministic contract and router of judgment.
- **Narrow support:** the language prevents false advancement and makes ambiguity explicit, but misses the
  expressibility or automation threshold. Preserve it as a safety/decision-record primitive; do not claim
  autonomous adjudication.
- **Refuted:** cross-domain decisions cannot be decomposed without bespoke or unbounded interpretation;
  accepted clause results do not determine a stable next action; or the selected policy produces a false
  advancement on holdout. The typed decision gate does not support the evolved Jurati premise as stated.

## Explicitly out of scope

- A complete Jurati workflow language, runtime, scheduler, authority broker, or product implementation.
- Canvas/UI design beyond an optional read-only rendering of a decision contract.
- Choosing Jurati's implementation language or runtime substrate.
- Proving model routing, local-model quality, or SHD as a whole; SHD supplies an experimental judge arm.
- Training or fine-tuning a judge model.
- Rewriting historical decisions to make the language look complete.
- Treating historical human judgments as infallible; ambiguity is adjudicated and retained.
- Autonomous firewall-grade advancement. Even a successful prototype only supports the premise; production
  authority remains human-gated until a later scope proves the integrated control.
- General claims about all SDLC or research workflows beyond the frozen corpus.

## Coverage / done call

This is a validated empirical scope; loop-until-dry does not define completion. The run is done when the
corpus and partitions are frozen, the language and interpreter are frozen before holdout, every required
inference arm is run or explicitly blocked, both domains complete sealed replay, adversarial checks run,
and the premise receives one outcome from the taxonomy above. Negative or narrow results are successful
research outcomes if the evidence is complete.

Human gates:

1. **Scope gate:** approve the hypothesis, corpus boundary, thresholds, inference arms, and authority limit.
2. **Corpus-freeze gate:** approve sampling, reference adjudications, exclusions, and sealed holdout hashes
   before language finalization.
3. **Firewall/synthesis gate:** review raw disagreements and rule on the premise verdict. No product build or
   graph-grade advancement follows automatically.

## Dependencies and execution notes

- Read access to the pinned Unimatrix `product/features` corpus and this repository's `product/research`
  corpus.
- A reproducible local-model endpoint for the local arms; unavailable arms remain visibly blocked.
- Model/API access for any approved frontier arms, with a fixed budget set at gate 1.
- Executable prototype and generated datasets follow D15: use a `research/jurati-001` branch and PR;
  research documents land on `main` as produced.
- At execution INIT—not in this planning session—the leader opens the GitHub Issue, starts the stamped
  `context_cycle`, and creates the required git surface per `.claude/workflow/research-scope.md`.

---

<!-- Amendments are append-only (D3). Never overwrite a validated verdict; explicitly reconcile any
this extension changes. -->
## Extensions

None.
