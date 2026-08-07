# jurati-001 — W5 sealed cross-domain replay protocol

**Workstream:** W5 — sealed cross-domain replay  
**Status:** preregistered protocol; replay not run  
**Researcher:** `jurati-001-researcher-W5`  
**Date:** 2026-08-07

## Finding

The holdout replay must be a **one-way, fail-closed evaluation ceremony**, not another tuning stage. Its
unit is a frozen decision episode, but it preserves three nested outcomes: clause result, reduced verdict,
and exact next action. The replay runner may combine W1 packets and labels, the frozen W2 contract, W3
execution records, and W4 policy outputs only after their identities are preregistered. It may calculate
metrics and dossiers; it may not repair, reinterpret, or rerun a failed item under altered inputs.

This protocol specifies that ceremony without opening W1's sealed labels or executing the interpreter.
It is therefore structural evidence only. No held-out performance, cross-domain coverage, or Jurati premise
claim exists yet.

## 1. Freeze boundary and launch gate

W5 has five independently hashed freeze bundles. Each bundle is canonical JSON or a manifest that hashes
the referenced bytes; directory names and mutable branch names are not identities.

| Bundle | Owner | Minimum frozen contents |
|---|---|---|
| `corpus_freeze` | W1 | corpus version; repository commit; cycle-level split assignment; episode and packet IDs; evidence locators/media types/digests; eligibility/exclusion status and reason; reference-label commitment; ambiguity/adjudication state; split hash |
| `language_freeze` | W2 | language/schema version and digest; clause/result/verdict/action vocabularies; contracts and digests; evidence admissibility; reducer; complete transition tables; prompt/schema bytes consumed by judges |
| `runtime_freeze` | W3 | interpreter and harness commit/artifact digest; dependency/runtime identity; invocation schema; deterministic replay test result; run-log/result schemas; container or reproducible launch command |
| `policy_freeze` | W4 | selected policy for every eligible `(domain, clause_class, criticality)` cell; arm membership/model identity; repetitions/quorum/escalation; decoding controls; prompt digest; blocked-arm declarations; calibration-selection record |
| `replay_preregistration` | W5 | all four bundle digests; eligibility query; execution seed/order; retry and interruption rules; comparison normalization; strata; metrics; confidence method; output paths; analyst access boundary |

The replay may launch only when:

1. corpus-freeze gate approval is recorded and both domain holdout split commitments verify;
2. every eligible episode has one contract and reference-label commitment, while label plaintext remains
   unavailable to the runner and judges;
3. W2 and W3 are frozen after calibration, their hashes match, and W3 passes its deterministic conformance
   suite against the frozen W2 semantics;
4. every eligible policy cell names one production policy or is explicitly `blocked`; there is no implicit
   fallback;
5. the W5 preregistration is committed before label reveal or any holdout invocation; and
6. a clean-room verifier confirms that no development/calibration cycle appears in holdout and that every
   cycle occurs in exactly one partition.

Any failed launch condition produces `replay_not_started`. It does not license partial unsealing.

## 2. Roles, access, and anti-leakage controls

Separate capabilities even if one person performs more than one role at different times:

- **custodian:** W1-controlled access to encrypted/sealed reference labels and split commitments;
- **runner:** reads holdout contracts/evidence and frozen policies, invokes W3/W4, but cannot read reference
  clause results, historical verdict summaries, historical next actions, or adjudication notes;
- **scorer:** receives immutable prediction logs and reference labels only after execution closes; it cannot
  invoke judges or alter contracts;
- **auditor:** verifies digests, cycle-disjointness, ordering, completeness, and output derivation;
- **adjudicator:** may explain an already frozen ambiguous reference after scoring, but cannot silently
  replace it. A changed label creates a separately versioned sensitivity analysis.

Required controls:

1. Historical verdict, recommendation, gate-summary, and next-action fields are removed from judge packets
   unless a contract explicitly declares the field as evidence under test. Redaction is content-aware; a
   renamed `PASS` field is still leakage.
2. Packet construction is frozen by digest. Judges receive only declared evidence for the named clause,
   the frozen proposition/rubric, and their policy prompt. Retrieval, browsing, tool use, sibling outputs,
   prior repetitions, and reference labels are disabled.
3. Prompts, schema, evidence ordering, context truncation behavior, model identities, decoding controls,
   and quorum rules are byte-identical to the frozen policy. A provider substitution or retired snapshot
   blocks the affected arm.
4. Raw responses are append-only and hashed before parsing. Invalid output is retained; it is never edited
   into a valid prediction. Retries follow W4's frozen transport policy and keep the same repetition ID.
5. No analyst examines item-level outputs while execution remains open. Operational monitoring exposes
   request IDs, latency, status, and cost only—not semantic responses.
6. The runner has no write path to W1/W2/W3/W4 frozen artifacts. The output directory is new and
   append-only for the run ID.
7. An interruption resumes from the first uncommitted invocation in the preregistered order. Completed
   invocations are not rerun. If reproducible continuation cannot be established, close the run as
   incomplete and issue a new run/version; do not splice silent replacements into it.

## 3. Preregistered execution order

Execution order is committed before unsealing to prevent selective stopping and time/provider drift from
tracking one domain or consequence.

1. Materialize an **execution index without labels** containing one row per
   `(episode_id, clause_id, arm, repetition_or_member)` for eligible holdout clauses. Arm A mechanical
   evaluations are included; Arm F is the frozen human reference and is not reinvoked by W5.
2. Sort first by the SHA-256 of
   `execution_seed || domain || episode_id || clause_id || arm || repetition_or_member`; the committed
   `execution_seed` is generated before the index exists. This interleaves domains, arms, and clause types.
3. Run all clause invocations exactly once in index order, subject only to frozen transport retries. Record
   blocked rows rather than skipping them.
4. Close the invocation ledger; verify row counts, hashes, model identities, and absence of duplicate
   successful invocation keys.
5. Apply each frozen arm's quorum/abstention rule. Preserve every member result and derive one accepted
   clause result or `insufficient_evidence`/blocked status.
6. For each `(episode, arm)`, require one accepted outcome for every contract clause. Feed accepted results
   to W3's deterministic reducer and transition selector. Repeat reduction/selection from the same clause
   vector at least twice in fresh processes; any mismatch is a runtime reproducibility failure, not model
   disagreement.
7. Seal the prediction ledger and publish its digest. Only then may the custodian reveal reference labels
   to the scorer.
8. Score every preregistered comparison, generate matrices/dossiers, and have the auditor reproduce outputs
   from the two sealed ledgers.

Stopping early because results look good, bad, expensive, or redundant is forbidden. A hard budget or
provider outage stops only according to the preregistered rule and leaves all unexecuted rows visibly
`blocked`/`not_run`; it never changes the denominator of an accuracy claim to “available successful calls.”

## 4. Exact comparison semantics

No fuzzy matching, semantic similarity, or post-hoc equivalence class is allowed.

### Clause result

For every eligible reference clause, compare the normalized enum token exactly:

`demonstrated | contradicted | not_demonstrated | insufficient_evidence`.

The prediction key is `(domain, episode_id, contract_digest, clause_id, arm)`. Reference and prediction
clause IDs must already be aligned by W1/W2 before freeze. Missing, duplicate, invalid, or digest-mismatched
predictions are **not** agreement; they are separately classified control/operational failures and resolve
fail-closed to `insufficient_evidence` for production-policy consequence scoring. Blocked arms have no
semantic prediction and no agreement denominator.

### Verdict

Compare the exact frozen `Verdict` enum after reducing the complete predicted clause vector:

`pass | pass_with_advisory | fail | not_demonstrated | insufficient_evidence`.

The reference verdict must either be W1-adjudicated directly or mechanically reduced from W1's frozen
reference clause vector using the same contract. Record which derivation applies. If the two reference
forms disagree, the episode is `reference_inconsistent`; exclude it from primary agreement, retain it in
the ambiguity denominator and dossier, and report a sensitivity analysis for each frozen interpretation.

### Exact next action

Compare the canonical tuple

`(action_id, kind, target, authority_required)`

for byte-equal canonical values. Matching only `kind`, a prose synonym, or an action that a reviewer judges
“close enough” is a disagreement. W1 must map the historical next action to this tuple before freeze; W5
cannot create aliases. Report `kind`-only agreement as a diagnostic, never as the ≥90% success measure.
Authority execution is outside W5: the comparison establishes selected action, not permission or actual
side effect.

### Safety boundary

Define an advancement-capable prediction as `kind=advance` (including qualified advancement). A **false
advancement** is a predicted advancement-capable action when the frozen reference action kind is any of
`rework | request_evidence | escalate | stop`, or when the reference is `reference_inconsistent` and any
frozen admissible interpretation is non-advancing. Report raw `k/n`, domain, arm, episode, and consequence;
zero observed events is never described as zero population risk.

## 5. Matrices and stratified reports

Produce raw counts before rates. Every table includes eligible `N`, scored `n`, blocked, execution error,
invalid response, reference-inconsistent, agreement count/rate, and a 95% Wilson interval where binomial.
Small cells remain visible; no pooled cell qualifies a domain.

1. **Clause confusion matrices:** 4×4 reference rows × predicted columns, plus side columns for
   invalid/missing control failures. Emit separately by:
   - domain (`sdlc`, `research`, and pooled diagnostic);
   - W4 semantic clause class and `mechanical`/`human_reserved` where applicable;
   - criticality (`blocking`, `advisory`);
   - consequence class if that clause alone crosses or can cross the advancement boundary; and
   - arm/policy, including the selected production policy.
2. **Verdict confusion matrices:** 5×5 by domain and arm, with invalid/incomplete vectors visible.
3. **Action confusion matrices:** reference `kind` × predicted `kind`, by domain and arm. In addition,
   report exact tuple agreement, action-ID agreement, target agreement, and false-advancement cells.
4. **Episode summary:** exact all-clause-vector agreement, exact verdict agreement, exact-next-action
   agreement, deterministic-repeat agreement, and whether any disagreement was localized to named clauses.
5. **Inference-arm comparison:** the same eligible cell set when comparing arms. Pairwise differences use
   paired episode/clause records; blocked arms are “not comparable,” never treated as errors or abstentions.

At minimum, consequence strata are `advance`, `rework`, `request_evidence`, `escalate`, and `stop` by
reference action kind, plus the binary `advancement_boundary`. The primary production-policy report must
show exact-next-action agreement and false advancement separately for each domain.

## 6. Disagreement dossier

Create one dossier per episode with any clause, verdict, action, reproducibility, control, or reference
disagreement. It contains:

- immutable run/bundle/packet/contract/prompt/policy/model hashes;
- domain, cycle, episode, clause type/class/criticality, arm, and reference consequence;
- every raw member result and normalized result, cited evidence IDs, concise rationale, schema validation,
  quorum outcome, abstention/escalation path, and operational errors;
- frozen reference clause/verdict/action plus adjudication provenance revealed after execution;
- predicted clause vector, reducer trace, selected action tuple, and fresh-process repeat traces;
- exact disagreement level(s), advancement-boundary crossing, and whether fail-closed handling prevented an
  unsafe action;
- one or more diagnosis tags from W4's frozen taxonomy:
  `evidence_missing | evidence_ambiguous | reference_ambiguous | prompt/schema_failure |
  stochastic_variance | model_family_difference | context_limit | execution_failure |
  unbounded_or_owner_reserved`;
- analyst commentary clearly marked **post-hoc** and forbidden from changing primary scoring.

A disagreement not localized to named clauses fails the scope's localization criterion. A holdout failure
may motivate a new language/prompt/policy version only after this run closes; that version requires a new
untouched holdout and cannot overwrite this dossier.

## 7. Exclusions, unencodable cases, and blocked arms

Eligibility is frozen by W1 before contract/policy finalization. Allowed primary exclusions are limited to:

- `insufficient_source_artifact` — required historical evidence is absent or integrity cannot be checked;
- `reference_unadjudicable` — independent adjudication cannot bound the historical clause/verdict/action;
- `outside_decision_episode` — no actual gate decision and consequence exists;
- `privacy_or_access_prohibited` — required material cannot enter the corpus;
- `language_unencodable` — W2 cannot encode the historical question without bespoke logic or semantic
  change.

Every exclusion retains domain, cycle, episode candidate, reason, decision date, and approving adjudicator.
`language_unencodable` counts against expressibility and remains in its denominator. The other exclusions
are reported in the sampling flow and may not be invented after predictions are seen. A malformed contract,
missing transition, packet overflow, or interpreter failure is not a corpus exclusion; it is an experiment
failure.

An inference arm is `blocked` only under W4's preregistered protocol: unavailable required endpoint/model
identity, authorization/budget, frozen input, or reference judge. Record affected invocation keys, blocker,
detection time, attempted non-billable probe, and owner action. A blocked arm contributes no accuracy
denominator and cannot support least-cost or reliability claims. It remains in completeness tables. Do not
substitute providers, aliases, public models for local arms, or consensus for the human reference.

If the **selected production policy** is blocked for any eligible holdout cell, production-policy replay is
incomplete and the scope cannot claim the support bar, even if exploratory arms performed well. If a cell's
frozen selected policy is `human_reserved`, Arm F supplies the policy result; that is an explicit result,
not a blocked automation arm.

## 8. Preregistered outputs and decision rules

W5 should emit machine-readable, hash-linked artifacts plus a narrative summary:

- `replay/preregistration.json`
- `replay/execution-index.jsonl`
- `replay/invocations.jsonl`
- `replay/predictions.jsonl`
- `replay/reference-labels.jsonl` (revealed/copy-controlled only after prediction closure)
- `replay/episode-results.jsonl`
- `replay/matrices/*.csv`
- `replay/dossiers/{episode_id}.md`
- `replay/REPORT.md`

The report evaluates, without relaxing them, the scope's frozen thresholds: ≥90% eligible expressibility;
deterministic verdict/action on fixed clause results; zero observed production-policy false advancements;
≥90% exact-next-action agreement in **each** domain; all disagreements localized and contained by
abstention/escalation; and a least-cost reliable policy per semantic class or `human_reserved`. Give raw
counts and confidence intervals beside every percentage. “Blocked,” “not measured,” and “failed” remain
distinct.

## Dependencies and blockers

- **W1 blocking dependency:** approved cycle-disjoint split; episode eligibility and exclusions; evidence
  packets/digests; pre-aligned clause obligations; independently adjudicated reference clause results,
  verdicts, exact action tuples, ambiguity states, and cryptographic commitments. W5 must not inspect label
  plaintext before prediction closure.
- **W3 blocking dependency:** frozen executable artifact/commit and environment; input/output schemas;
  deterministic conformance suite; append-only logging; fresh-process replay command; explicit control-error
  behavior; machine-readable invocation and episode result formats.
- **W2/W4 current dependencies:** `SPEC-v0.1-dev` is provisional and cannot be the holdout language freeze;
  W4 has no executable arm and B–E are blocked. W5 can preregister structure now but cannot launch.
- **Owner/resource blocker inherited from W4:** local endpoint/model identity, frontier budget/model
  authorization, mixed quorum composition, and human raters/adjudicator are unresolved.

## Directional verdict

**Protocol-ready, execution-blocked.** The W2 semantics and W4 measurement plan admit a sealed replay whose
authority boundary is deterministic and whose failures remain visible. Whether it covers either domain is
unknown until W1 freezes the corpus and W3 demonstrates the interpreter. Research moves structure only;
this document does not advance the Jurati premise.

## Citations

- type: docs · ref: `product/research/jurati-001/SCOPE.md` · title: "jurati-001 — Validated probe: a decision-contract language for deterministic next action" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/jurati-001/SPEC-v0.1-dev.md` · title: "Jurati Decision Contract Language — semantic specification v0.1-dev" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/jurati-001/findings-W2.md` · title: "jurati-001 — W2 findings: smallest shared decision-language semantic model" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/jurati-001/findings-W4.md` · title: "jurati-001 W4 — Inference-ladder preregistration" · org: arch-research garage · year: 2026
- type: standard · ref: `https://doi.org/10.6028/NIST.AI.800-3` · title: "Expanding the AI Evaluation Toolbox with Statistical Models" · author: Keller; Kwegyir-Aggrey; Steed; Rao; Sharp; Bergman · org: National Institute of Standards and Technology · year: 2026

