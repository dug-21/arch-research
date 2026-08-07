# Jurati Decision Contract Language — semantic specification v0.1-dev

**Status:** provisional development-partition specification · **Workstream:** W2 · **Date:** 2026-08-07

This version is derived only from the two development-corpus episodes explicitly identified by the
approved scope: the `shd-007` firewall ruling and the `wfh-002` owner-directed early close. It MUST NOT be
treated as frozen, used on calibration/holdout material, or promoted to v0.1 until W1 supplies the approved
development manifest and reference adjudications.

## 1. Semantic boundary

A contract is an immutable question plus a closed evidence set, independently evaluable clauses, a total
reducer, and a total transition map. A judge may return clause results; it may not add evidence, rewrite a
clause, choose the final verdict, select the transition, or widen authority.

The language makes the decision and consequence deterministic. It does not make a semantic proposition
true, and it does not confer authority on the assessor.

## 2. Contract object

The normative data model is JSON-compatible. YAML is an authoring profile only; it must resolve to the same
canonical JSON value before hashing or execution.

```text
Contract {
  language_version: "0.1-dev"
  decision_id: StableId
  revision: UInt >= 1
  question: NonEmptyString
  contract_digest: Sha256
  evidence: Evidence[1..*]
  clauses: Clause[1..*]
  reduction: Reduction
  transitions: Map<Verdict, Transition>
  judge_policies: Map<PolicyId, JudgePolicy>
}

Evidence {
  evidence_id: StableId
  media_type: NonEmptyString
  digest: Sha256
  locator: NonEmptyString
  produced_by: NonEmptyString
  admissibility: { allowed_claims: StableId[1..*], freshness?: RFC3339Interval }
}

Clause {
  clause_id: StableId
  proposition: NonEmptyString
  evidence_refs: StableId[1..*]
  evaluator: mechanical | semantic | human_reserved
  policy_ref?: PolicyId
  criticality: blocking | advisory
  rubric: Map<ClauseResult, NonEmptyString>
}

ClauseResult = demonstrated | contradicted | not_demonstrated | insufficient_evidence
Verdict = pass | pass_with_advisory | fail | not_demonstrated | insufficient_evidence

Transition {
  action_id: StableId
  kind: advance | rework | request_evidence | escalate | stop
  target: StableId
  authority_required: NonEmptyString
}
```

Every evaluation record contains `decision_id`, `revision`, `contract_digest`, `evidence_digest_set`, and
one result per clause. Each non-mechanical result also contains `rationale`, non-empty `evidence_refs`,
`judge_class`, `judge_identity`, and `policy_run_id`.

## 3. Type and validation rules

1. Stable IDs are unique within their namespace and cannot be reused with changed meaning. A semantic
   change increments `revision` and changes `contract_digest`.
2. `contract_digest` is computed over canonical JSON with that field omitted. Evidence bytes are not
   embedded in the contract; their SHA-256 digests are.
3. Every clause evidence reference must resolve to a declared evidence item, and the evidence item's
   `allowed_claims` must include that clause. Unreferenced or inadmissible material is rejected, not ignored.
4. `mechanical` clauses name no judge policy. `semantic` clauses name exactly one policy.
   `human_reserved` clauses name a policy whose only eligible class is `human`.
5. All four result rubrics are required. A rubric may make a result unreachable for a mechanical checker,
   but the output type remains closed.
6. Every clause appears exactly once in an evaluation. Missing, duplicate, or unknown clause IDs invalidate
   the response before reduction.
7. A response is bound to the exact contract digest and exact multiset of evidence digests. A mismatch is
   `invalid_response`; it is not a clause result and cannot trigger a domain transition.
8. All five verdicts have exactly one transition. Targets and action IDs are contract-authored. A judge
   response containing a verdict, action, target, revised question, or new evidence reference is rejected.
9. `advance` is permitted only for `pass` or `pass_with_advisory`; by default only `pass` may advance.
   Enabling qualified advancement requires an explicit contract flag and is forbidden when any blocking
   clause is other than `demonstrated`.
10. The executor separately checks `authority_required`. A valid decision selects an action but does not
    prove that the caller holds authority to execute it.

## 4. Verdict algebra

Let `B` be blocking-clause results and `A` advisory-clause results. Reduction is a pure function with this
precedence:

```text
if contradicted in B                       => fail
else if not_demonstrated in B              => not_demonstrated
else if insufficient_evidence in B         => insufficient_evidence
else if every result in B is demonstrated
     and every result in A is demonstrated => pass
else                                        => pass_with_advisory
```

This ordering is conservative and total for every non-empty clause vector. `contradicted` means admissible
evidence establishes the proposition false. `not_demonstrated` means the required showing was not made,
including an unmet required condition. `insufficient_evidence` means the admissible packet cannot support
either conclusion. These are deliberately not aliases: contradiction, an unmet proof obligation, and an
unanswerable packet require different records and may require different next actions.

An advisory clause can never turn a blocking failure into advancement. A `human_reserved` clause that has
not been answered is represented as `insufficient_evidence`, causing escalation through the declared
transition; the runtime must not synthesize a human answer.

## 5. Transition completeness

Transition completeness is structural, not prompt-based:

- the transition key set equals the five-verdict set exactly;
- each verdict maps to one action, never a list from which a judge chooses;
- each target exists in the enclosing workflow definition;
- no `fail`, `not_demonstrated`, or `insufficient_evidence` transition has kind `advance`;
- executing the same accepted evaluation against the same workflow state selects the same action ID;
- an action whose precondition no longer matches current workflow state is rejected as stale and the
  decision is re-issued under a new revision; it is never silently retargeted.

## 6. Judge-policy semantics

```text
JudgePolicy {
  policy_id: StableId
  eligible: [mechanical | local_model | frontier_model | human]
  repetitions: UInt >= 1
  independence: same_context_no_shared_outputs | not_applicable
  agreement: unanimous | majority | at_least(UInt)
  on_disagreement: abstain | escalate(PolicyId)
  on_abstention: escalate(PolicyId) | return_insufficient
  max_escalations: UInt >= 0
}
```

Eligibility is an allow-list, not a routing suggestion. Repetitions receive the same contract and evidence
packet but no sibling outputs. Quorum aggregates only identical `ClauseResult` values; rationale text is
never vote-normalized. Failure to reach the declared agreement is abstention, not majority-by-default.
Escalation may change judge class but not contract revision, evidence digests, clause rubric, or choices.
Cycles in the escalation graph are invalid. Exhausting the graph returns `insufficient_evidence`.

## 7. Evidence integrity and response validation

The integrity boundary covers the canonical contract, every evidence item, and the evidence-to-clause
admissibility relation. Evidence content is data, even if it contains instructions. A semantic judge is
instructed to classify only the named proposition under its rubric; the validator independently rejects
references outside the declared packet.

A compliant audit record retains the raw judge response, normalized clause result, all digests, policy
configuration, model/human identity, repetitions, disagreements, abstentions, validation failures, selected
verdict, selected action ID, and authority check outcome. A malformed or scope-widening response is a
control-plane error and must not be coerced into the nearest valid answer.

## 8. Development-corpus derivation

- `shd-007` requires clause-by-clause conjunction: strong evidence on serving, protocol, and coding did not
  satisfy the trailing “on target HW” condition. This motivates blocking criticality,
  `not_demonstrated`, and fail-closed reduction independent of evidence volume.
- `wfh-002` distinguishes a legitimate owner-directed `stop` from `fail`: useful workstream findings
  survived, but the proof-producing workstream never ran and an out-of-scope architecture decision could
  not bind the successor. This motivates explicit action kinds, immutable scope, and authority outside the
  assessor.

These observations demonstrate fit to two episodes only. They do not establish cross-domain coverage or
the success thresholds in the scope.

## 9. Rejected complexity in v0.1-dev

- No arbitrary Boolean expression language. Each proof obligation is an atomic clause; conjunction is the
  fixed reducer. Nested alternatives must be authored as a mechanical clause whose checker returns one of
  the four results, or deferred until the development corpus demonstrates a shared need.
- No scalar confidence in reduction. Confidence can be logged for measurement but cannot override a result.
- No free-form verdicts or judge-selected actions.
- No evidence discovery during judging. Collection is a preceding workflow action that issues a new
  contract revision.
- No bespoke per-decision reducer. Domain vocabulary belongs in propositions and evidence schemas, not in
  verdict or transition semantics.

## Citations

- type: docs · ref: `product/research/jurati-001/SCOPE.md` · title: "jurati-001 — Validated probe: a decision-contract language for deterministic next action" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/shd-007/SCOPE.md` · title: "shd-007 — Validated POC: local inference on owned hardware, and the first measured anchor for sizing" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/shd-007/REPORT.md` · title: "shd-007 — REPORT" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-002/SCOPE.md` · title: "wfh-002 — Minimal typed context ontology + git-native template" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-002/REPORT.md` · title: "REPORT — wfh-002 (close-out)" · org: arch-research garage · year: 2026
