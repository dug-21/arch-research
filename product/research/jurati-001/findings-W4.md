# jurati-001 W4 — Inference-ladder preregistration

**Workstream:** W4 — inference ladder

**State:** design complete; empirical arms not run

**Researcher:** `jurati-001-researcher-W4`

**Boundary:** no paid inference was authorized or used. No local inference endpoint was reachable at
`127.0.0.1:11434` on 2026-08-07. Arms B–E are therefore blocked, not simulated. Arm A awaits frozen W1
packets and the W2/W3 evaluator; arm F awaits W1's independently adjudicated references.

## Finding

The inference ladder should be a **risk-weighted selective-classification experiment**, not a model
leaderboard. It asks, per semantic clause class, which cheapest frozen policy agrees with the independently
adjudicated reference while abstaining or escalating on uncertainty. It must never optimize aggregate
accuracy at the expense of false advancement. Published judge studies support the need to stratify by
evaluated property and test repeated stability: model reliability varies materially by task/property, and
even semantically equivalent prompt changes can alter judgments [C1][C2]. Those are **external doc-claims**,
not evidence that any arm works on Jurati's corpus.

Two live Unimatrix lessons constrain the design. Entry #237 demonstrates in our own prior work that `n=1`
binary stochastic outcomes produced a plausible but false route difference that disappeared at three
repetitions; repetitions must be fixed before observing results. Entry #238 demonstrates that strong
aggregate evidence cannot override one unmet critical clause. These are **demonstrated internal evidence
for experimental discipline**, not demonstrated Jurati judge performance.

## 1. Unit of evaluation and frozen inputs

The atomic unit is one `(episode_id, clause_id, clause_class, arm, repetition)` judgment. W4 starts only
after W1 freezes evidence packets and adjudicated references and W2 freezes the clause/result schema.
Calibration may select policies; sealed holdout may only execute them.

Every invocation records:

- corpus, packet, contract, clause, prompt-template, schema, and policy versions plus SHA-256 hashes;
- exact ordered evidence IDs and content hashes; historical verdict/next action withheld;
- provider, endpoint class, model identifier and immutable snapshot/digest where available; tokenizer and
  serving-runtime versions for local models;
- system/developer/user prompt bytes and hash, output-schema bytes and hash;
- temperature, top-p, top-k, seed (when supported), maximum output tokens, stop conditions, timeout,
  retry count, and context-window limit; absent/unsupported controls are explicitly recorded;
- repetition index, randomized execution-order seed, request/response timestamps, wall latency, provider
  usage fields, locally counted tokens, billed amount/currency, and error/timeout status;
- raw response hash, parsed bounded result, cited evidence IDs, rationale, schema-validation result, and
  escalation reason.

Retries are not silently substituted for repetitions. A transport retry keeps the same repetition ID and
is logged; more than the predeclared retry limit yields `execution_error`, which is excluded from semantic
accuracy but included in operational reliability. Prompts and evidence order remain byte-identical across
arms. No chain-of-thought is requested or retained; the response contains only result, evidence references,
and concise clause-bounded rationale.

## 2. Clause taxonomy

W2 owns the normative types. W4 should map semantic clauses into this smallest measurement taxonomy before
calibration; creating a new class after seeing holdout results invalidates the holdout.

| Class | Bounded question | Default criticality | Allowed automation |
|---|---|---:|---|
| `evidence_entailment` | Do admissible artifacts directly support the stated proposition? | critical when advancement depends on it | A–F |
| `obligation_coverage` | Does the evidence address every named obligation, including qualifiers? | critical | A–F |
| `boundary_conformance` | Did work remain within the declared scope/authority boundary? | critical | A–F |
| `risk_control_adequacy` | Does evidence demonstrate the named risk/control at the required altitude? | critical | A–F, often escalate |
| `cross_artifact_consistency` | Are named artifacts semantically consistent, or is a contradiction material? | critical when conflict affects advancement | A–F |
| `bounded_alignment` | Does an artifact satisfy an explicit architectural/vision criterion? | contract-defined | A–F, often escalate |
| `human_reserved` | Owner intent changes, value/prioritization, authority grants, or irreducibly ambiguous reference adjudication | contract-defined | F only |

Evidence identity, hash integrity, schema validity, numeric thresholds, test status, set inclusion, transition
reduction, and next-action selection are **mechanical**, not semantic classes. If a supposed semantic clause
can be replaced by a general mechanical predicate during development, retype it before freeze and report the
change. No per-episode evaluator is allowed. If a question cannot be bounded without adding facts or
reframing owner intent, classify it `human_reserved`; do not make the model guess.

## 3. Arms and fixed policies

| Arm | Frozen policy | Repetitions | Current state |
|---|---|---:|---|
| A | General mechanical evaluator only; every residual semantic clause returns `insufficient_evidence` and escalates | 1 (deterministic replay is separately repeated by W3) | blocked on W1–W3 artifacts |
| B | One designated local model, one independent judgment | 1 | **blocked:** no reachable local endpoint/model declaration |
| C | Same designated local model and prompt; five independent judgments | 5 | **blocked:** no reachable local endpoint/model declaration |
| D | One designated frontier model snapshot, one judgment | 1 | **blocked:** no paid-inference authorization/model declaration |
| E | Three independently operated eligible models from at least two model families, including local and frontier; one judgment each | 3 judges | **blocked:** local endpoint and paid-inference authorization absent |
| F | W1's independent human reference/adjudication; judges see the same bounded clause and evidence | W1 protocol; minimum two initial raters for ambiguous labels, third adjudicator on disagreement | blocked on W1 reference set and human assignment |

Arm B deliberately has no within-item variance estimate: it measures the operational single-call policy.
Arm C measures same-model stochastic stability. Five was chosen before results because binary completion
claims need repetition and an odd count gives a non-tied majority. Arm E measures between-model
disagreement; it is not valid if three aliases route to one underlying model snapshot.

For C, a non-critical clause resolves on at least `3/5` identical bounded results; otherwise it escalates.
For a critical clause, advancement-capable results require `5/5` agreement, valid evidence references, and
no abstention; any disagreement escalates. For E, non-critical clauses require `2/3`; critical advancement
requires `3/3`, valid references, and no abstention. Quorum never converts `insufficient_evidence` into a
substantive result. Ties, malformed output, undeclared evidence, execution errors, and rationale/evidence
mismatch escalate. The deterministic reducer—not a judge—maps accepted clause results to verdict/action.

## 4. Reliability bar and policy selection

The calibration partition selects one policy per `(domain, clause_class, criticality)` cell; pooling may
be reported but cannot qualify a failed domain. Selection is lexicographic:

1. reject any policy with an observed critical false advancement;
2. reject any policy whose schema/contract escape rate is nonzero;
3. among survivors, require at least 90% exact result agreement on answered clauses and report the 95%
   binomial interval and raw denominator;
4. minimize empirical unsafe selective risk, then unnecessary escalation, then marginal monetary cost,
   then latency;
5. if evidence is too sparse to distinguish policies or the bar is not cleared, select `human_reserved`.

This is deliberately conservative. A zero observed count is reported as `0/n` with a confidence interval,
never as zero population risk. NIST distinguishes fixed-benchmark performance from generalized performance
and recommends making the estimand and uncertainty assumptions explicit [C3]. This experiment's primary
estimand is performance **conditioned on the frozen Jurati corpus**; any generalized model is exploratory.

## 5. Measurements

Report raw counts and 95% Wilson score intervals wherever the estimand is binomial, by domain and pooled,
then by clause class, criticality, consequence, and arm. Small cells are shown rather than suppressed or
over-interpreted.

- **Reference reliability:** exact bounded-result agreement; per-result confusion matrix; macro-F1;
  critical false-advancement count/rate; verdict and exact-next-action agreement after deterministic replay.
- **Variance:** C's per-item unanimity, majority margin, pairwise disagreement, and result entropy; E's
  between-model equivalents; B/D variance is `not measured`, not zero.
- **Abstention:** coverage, answered-clause risk, risk–coverage table, unsafe guesses avoided, unnecessary
  escalations, and escalation precision. Selective classification trades coverage for risk, but published
  work warns aggregate gains can hide group/cell regressions [C4]; therefore report every domain/class cell.
- **Operational reliability:** success, timeout, transport-error, malformed-output, and invalid-reference
  rates. Semantic accuracy excludes execution failures; production-policy success includes them as
  escalations.
- **Latency:** end-to-end wall time per invocation and per resolved clause/episode; p50/p95, cold/warm local
  status, and quorum wall time under both sequential execution and actual observed parallel execution.
- **Cost:** actual billed amount from provider records plus input/output/cached token counts; local marginal
  energy cost is `not measured` unless instrumented, while hardware/runtime and wall time are reported.
  Quorum cost includes all members and retries. Never impute a blocked arm's cost or quality.
- **Human arm:** rating time, adjudication time, initial inter-rater agreement, disagreement rate, and final
  adjudicated label. The final label is a reference, not proof that the initial human judgment was infallible.

## 6. Disagreement dossiers and escalation

Every disagreement dossier contains packet/clause hashes, all raw bounded results, evidence references,
rationales, whether disagreement crosses an advancement boundary, reference adjudication notes, and the
deterministic consequence of escalation. Diagnose without changing the frozen question:

`evidence_missing | evidence_ambiguous | reference_ambiguous | prompt/schema_failure | stochastic_variance |
model_family_difference | context_limit | execution_failure | unbounded_or_owner_reserved`.

A calibration disagreement may motivate a policy change recorded as a new policy version. A holdout
disagreement may not modify grammar, prompt, taxonomy, evidence, or policy; it becomes evidence in the
dossier. Prompt-robustness research demonstrates that apparently equivalent wording is itself a variance
source [C2], so prompt paraphrases belong in a separate adversarial study, not silent W4 tuning.

## 7. Blocked-arm protocol

An arm is `blocked` when any required endpoint, immutable model identity, authorization/budget, frozen input,
or reference judge is unavailable. Record blocker, detection timestamp, attempted non-billable probe,
owner/action needed, and affected cells. Blocked is neither abstention nor failure and contributes no
accuracy denominator. It remains visible in completeness tables and prevents a claim that the full ladder
or least-cost policy was identified.

Do not replace a local arm with a public model, a frontier arm with a different unapproved provider, a mixed
quorum with repeated aliases, or a human reference with model consensus. If a pinned provider snapshot is
retired before execution, create a new arm/version; do not silently relabel it.

## 8. Current blockers and minimum owner decisions

1. **Local arms B/C:** designate and make reachable one local endpoint; name model artifact/digest, serving
   runtime/version, context limit, and hardware. No monetary API budget is needed.
2. **Frontier arm D:** authorize a hard maximum monetary budget and name the eligible provider/model snapshot
   (or authorize W4 to choose from a stated allow-list). Without both, D remains blocked.
3. **Mixed arm E:** authorize a separate hard maximum budget sufficient for at least two eligible frontier
   families/providers and approve the three-member composition; one member must be the pinned local arm.
4. **Human arm F:** name/authorize at least two independent initial raters and a third adjudicator for
   ambiguous/disagreed labels, and decide whether human time has a reportable internal cost rate. If no rate
   is supplied, report time only and do not claim human-vs-model least-cost ordering.
5. **Shared prerequisite:** W1/W2/W3 must publish frozen packet/reference, schema/prompt, and executable
   interface hashes before any inference call. The calibration cell counts then determine an exact token and
   spend ceiling; authorizing money before those counts exist can only be a cap, not a defensible estimate.

Until these are resolved, W4 can establish the experimental contract but cannot identify the least-cost
reliable judge policy required by H3.

## Citations

- **[C1]** `type: paper` · `ref: 10.18653/v1/2025.acl-short.20` · `title: LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks` · `author: Bavaresco; Bernardi; Bertolazzi; Elliott; Fernández; Gatt; Ghaleb; Giulianelli; Hanna; Koller; Martins; Mondorf; Neplenbroek; Pezzelle; Plank; Schlangen; Suglia; Surikuchi; Takmaz; Testoni` · `org: Association for Computational Linguistics` · `year: 2025` · `venue: ACL 2025`
- **[C2]** `type: paper` · `ref: 10.18653/v1/2026.findings-acl.1929` · `title: All Prompts Are Created Equal? Evaluating Robustness of LLM Judges Against Non-Adversarial Prompt Variations` · `author: Bhat; Varma` · `org: Association for Computational Linguistics` · `year: 2026` · `venue: Findings of ACL 2026`
- **[C3]** `type: standard` · `ref: https://doi.org/10.6028/NIST.AI.800-3` · `title: Expanding the AI Evaluation Toolbox with Statistical Models` · `author: Keller; Kwegyir-Aggrey; Steed; Rao; Sharp; Bergman` · `org: National Institute of Standards and Technology` · `year: 2026`
- **[C4]** `type: paper` · `ref: arXiv:2010.14134` · `title: Selective Classification Can Magnify Disparities Across Groups` · `author: Jones; Sagawa; Koh; Kumar; Liang` · `year: 2020`

## Flags for synthesis

- **No empirical W4 claim exists yet.** All arms are blocked on upstream frozen artifacts; B–E have additional
  endpoint/budget blockers.
- The full scope cannot satisfy its done call or identify a least-cost judge policy while B–E remain blocked,
  though the protocol permits explicitly blocked arms to be honestly reported.
- Human cost must be quantified or least-cost comparisons involving F are structurally incomplete.
- A production policy that clears aggregate agreement but has one observed critical false advancement is
  disqualified.
