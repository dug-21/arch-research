# jurati-001 feasibility / firewall gate

**Verdict:** **SCOPE FAIL**  
**Artifact reviewed:** builder `ed81b1d`; independent custodian score `871466d`  
**Validator:** `jurati-001-validator` (gate-input independent; no build, scoring, or graph-write role)  
**Firewall recommendation:** capability #256 stays **missing**; technology #257 may advance from
**claimed** to **partial**, bounded to the executable deterministic checker and observed local-model
operational envelope below. Do not mark either subject `proven`.  
**Synthesis:** may proceed only as a negative/failed, inconclusive research outcome. It must not classify
the Jurati premise as supported, narrow, or refuted from unavailable reference metrics.

Both permitted feasibility reworks were consumed at the corpus-freeze gate. This terminal ruling is
therefore PASS or SCOPE FAIL; the defects below are not routed to another feasibility rework.

## Artifact reality

The artifact is real, but it demonstrates less than the validated claim:

- the frozen interpreter/checker exists and independently passes all 14 self-tests and fresh-process
  deterministic replay;
- the safe corpus verifier passes twice, including custody commitments, leakage controls, packet integrity,
  split/cap invariants, and outcome exclusion;
- Arm A contains 225 non-advancing deterministic reductions (45 episodes × 5);
- local Arm B attempted 11 calls and accepted 10; Arm C attempted 51 of 55 planned calls and accepted 50;
- two `B2-H03` responses cited undeclared evidence and were rejected before append, with no retry or repair;
  the first C failure stopped the remaining four repetitions, leaving that episode incomplete;
- all ten complete Arm-C episode groups produced one identical clause result across five repetitions;
- the prediction ledger, operational summary, custodian score, and disagreement dossiers are internally
  consistent, integrity-addressed, and free of real identities, source paths, or row-level references.

This proves a bounded checker and operational clause-classification run. It does not prove historical
decision agreement or the capability's `done_when`.

## Independent verification

| Check | Result | Evidence |
|---|---|---|
| Builder/custodian separation | PASS, bounded | Builder commit `ed81b1d` is authored by Codex and contains only predictions/errors/operational summary plus its summarizer. Custodian commit `871466d` is authored by Doug Faist and contains only the public custodian score/report/dossiers. The custodian score pins source commit `ed81b1d`. |
| Ledger and score digests | PASS | SHA-256 of `arm-bc-predictions.jsonl` independently recomputes to `5edfa947...`, matching both operational summary and custodian score. The encrypted-custody digest remains `2006fea9...`. |
| Public arithmetic | PASS | Recomputed B counts are 10 valid: 1 demonstrated, 6 not-demonstrated, 3 insufficient-evidence. C counts are 50 valid: 5, 30, and 15. Published B/C malformed rates and Wilson intervals exactly recompute for 1/11 and 1/51; C repetition interval exactly recomputes for 0/10. |
| Frozen prompt/policy/runner | PASS | Every accepted row carries prompt hash `b54c86a3...`, policy hash `3649607c...`, model digest `b92d6a0b...`; current frozen files independently hash to those prompt/policy values and runner `ffe31bd6...`. No frozen task artifact changed between `baf03aa` and builder execution. |
| Live model envelope | PASS, measured now | Independent API probe reports Ollama server `0.32.5`; `/api/tags` reports `qwen2.5-coder:32b` digest `b92d6a0b...` and `qwen3-coder:30b` digest `06c1097e...`. Builder report attests the same pre/post execution values. Host hardware, residency, energy, and monetary cost remain unmeasured. |
| Malformed output fail-closed | PASS | Two `ContractError: judge cited undeclared evidence` records state `prediction_appended:false`, `retry:false`; ledger has no `B2-H03` row. The validator independently exercises malformed/widened/undeclared evidence cases in the passing checker suite. |
| Incomplete episode handling | PASS operationally; FAIL for coverage | Summary and custodian score preserve planned/attempted/valid 55/51/50 for C and four not-run repetitions. They exclude rather than impute the incomplete episode. This is honest, but sealed replay did not complete both holdout domains for all eligible episodes. |
| Custody leakage | PASS | Structural scan of predictions, errors, custodian JSON/report, and dossiers finds no real repository paths or serialized real-cycle/source-path/reference-label/historical-outcome/next-action/verdict-summary fields. Dossiers explicitly exclude reference labels. |
| Measured versus attested | PASS | Counts, distributions, latency, ledger hashes, fail-closed events, and complete-group reproducibility are measured. Pre/post endpoint identity is builder-attested and independently consistent with the current live API. No zero-cost, energy, hardware, residency, semantic-accuracy, or population-risk claim is made. |

## Critical schema mismatch

The sealed custody reference exposes **episode verdict and exact next action**. The prediction ledger exposes
only **one synthetic clause result** plus rationale/evidence references. Their only common field is opaque
episode identity. There is no reference clause result and no predicted verdict or action.

Applying the interpreter after the fact cannot repair this: the frozen semantic runner did not emit the
contract, criticality vector, accepted complete clause vector, reducer verdict, or transition used for each
historical episode. Mapping `demonstrated | not_demonstrated | insufficient_evidence` directly onto a
historical verdict/action would invent a post-hoc evaluator and violate the frozen-language and no-bespoke-
code conditions. The custodian correctly reports `scoreable_prediction_reference_fields: []`.

Consequently these required measurements are unavailable—not low, not zero, and not inferable:

- clause-result agreement/confusion/macro-F1;
- exact final-verdict agreement;
- exact next-action agreement in either domain;
- false advancement and unsafe-guess avoidance;
- unnecessary escalation / abstention quality;
- 90% reliability qualification;
- least-cost reliable policy per clause class.

## Validated-success clauses

| Scope clause | Ruling | Reason |
|---|---|---|
| 1. One shared semantic model covers both domains | **NOT DEMONSTRATED** | One runner/classifier was used across both domains, but coverage means representing and replaying the historical decision semantics. No scoreable verdict/action output exists, and the garage sample has only two valid episodes per arm. |
| 2. ≥90% eligible holdout expressible without bespoke per-decision evaluator code | **NOT MEASURED** | The artifact supplies a generic single synthetic clause per packet, not an adjudicated expressibility mapping of historical clauses/questions/contracts. No exclusion/lossy-encoding denominator or confidence interval is reported. |
| 3. Fixed clause results replay to identical verdict and exact next action | **PARTIAL ONLY** | The synthetic interpreter fixture and Arm A reducer are deterministic. Semantic B/C records do not contain the per-episode contract/result vector or resulting verdict/action, so held-out exact consequence replay is absent. |
| 4. Zero false advancements on selected production policy | **NOT MEASURED** | Predictions contain no action; reference contains no clause result; no production policy is selected. Arm A's forced abstention is not semantic-policy evidence. |
| 5. ≥90% exact next-action agreement in each domain | **NOT MEASURED** | Predictions have no action. No per-domain numerator, denominator, confidence interval, or disagreement rows exist. |
| 6. Every disagreement localized and fails closed | **PARTIAL ONLY** | The two malformed outputs localize and fail closed, and complete C groups have no internal result disagreement. Reference disagreements cannot be detected or localized because no common score field exists; one episode is incomplete. |
| 7. Least-cost reliable judge policy per semantic clause class | **NOT MEASURED** | B/C reference reliability is unavailable; D/E are blocked by absent provider/immutable frontier snapshot; F is blocked by absent assigned raters/adjudicator; monetary and energy cost are unmeasured. A least-cost reliable policy cannot be selected. |

The capability #256 `done_when` clauses fail for the same reasons: ≥90% expressibility, zero observed false
advancement, and ≥90% exact next-action agreement per domain cannot be ruled on. Only fixed-input reducer
determinism is demonstrated.

## Terminal verdict and grade envelope

**SCOPE FAIL.** The experiment completed a real operational run but its frozen prediction/reference schemas
made the approved proof bar unscoreable. With both reworks exhausted, feasibility stops here.

- **Capability #256 — `missing`:** no attached artifact demonstrates its corpus-level agreement, safety,
  or expressibility `done_when` clauses.
- **Technology #257 — recommend `partial`:** demonstrated by commit lineage `baf03aa` → `ed81b1d` →
  `871466d` within this envelope: Python 3.14.6 on the recorded Linux platform; Ollama 0.32.5;
  `qwen2.5-coder:32b` digest `b92d6a0b...`; prompt `b54c86a3...`; policy `3649607c...`; B=1 and C=5
  requested repetitions; 60 accepted clause predictions across 10 complete episodes; deterministic
  reducer/checker and malformed-response confinement demonstrated. The envelope expressly excludes
  historical clause/verdict/action accuracy, expressibility, false-advancement rate, production-policy
  reliability, frontier/human arms, host hardware/residency, energy, and monetary cost.

Synthesis may now document this as a **failed/inconclusive research outcome** and extract the product lesson:
proof schemas must share a preregistered scoreable decision representation end-to-end. It may not use this
artifact to claim the Jurati premise supported, narrow, or refuted; the premise itself was not measured.

No Unimatrix write or grade mutation was made, and no restricted labels, identity mapping, or custody key
was inspected by the validator.
