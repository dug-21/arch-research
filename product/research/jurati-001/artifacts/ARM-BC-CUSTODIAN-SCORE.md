# jurati-001 B/C independent custodian score

**Result:** operational scoring complete; reference-accuracy thresholds are not assessable.

The encrypted reference contains episode verdict and next action, while the prediction ledger contains only clause results. Their only shared datum is opaque episode identity. Mapping clause results to verdict/action would invent the missing deterministic reducer output, so no reference agreement or false-advancement score is reported.

## Operational aggregates

### Arm B

- Planned/attempted/valid: 11/11/10.
- Malformed fail-closed: 1/11 (9.1%; 95% Wilson 1.6–37.7%).
- Not run after fail-closed: 0.
- sdlc: 8 valid; results `{"demonstrated": 1, "insufficient_evidence": 3, "not_demonstrated": 4}`; abstention 3/8 (37.5%; 95% Wilson 13.7–69.4%).
- garage: 2 valid; results `{"not_demonstrated": 2}`; abstention 0/2 (0.0%; 95% Wilson 0.0–65.8%).

### Arm C

- Planned/attempted/valid: 55/51/50.
- Malformed fail-closed: 1/51 (2.0%; 95% Wilson 0.3–10.3%).
- Not run after fail-closed: 4.
- sdlc: 40 valid; results `{"demonstrated": 5, "insufficient_evidence": 15, "not_demonstrated": 20}`; abstention 15/40 (37.5%; 95% Wilson 24.2–53.0%).
- garage: 10 valid; results `{"not_demonstrated": 10}`; abstention 0/10 (0.0%; 95% Wilson 0.0–27.8%).

### Arm C repetition

- Complete five-repetition groups: 10.
- Groups with disagreement: 0/10 (0.0%; 95% Wilson 0.0–27.8%).
- One episode group is incomplete because its first response failed closed; four later repetitions were not run.

## Reference metrics

Unavailable: clause agreement/confusion/macro-F1, exact verdict/action agreement, false advancement, unsafe-guess and escalation quality, the 90% reliability bar, and least-cost policy selection.

The support thresholds cannot be assessed from B/C because the reference and prediction schemas have no scoreable outcome field in common.

No real identities, source paths, row-level labels, or reversible mappings appear in this report.
