# jurati-001 Arms B/C operational results

**Freeze:** owner-approved at `baf03aa` · **launch base:** validator report `61eb398` · **date:**
2026-08-08. No reference labels, custody key, real identities, or scoring were accessed.

## Preflight and integrity

Before and after execution, Ollama reported server version `0.32.5` and the frozen
`qwen2.5-coder:32b` digest
`b92d6a0bd47ee79114298de0177bf920c05a706d12633950b3936778492bef41`. The frozen runner, prompt, and
policy hashes remained `ffe31bd6…`, `b54c86a3…`, and `3649607c…`. The 14 checker tests and the corpus
verifier passed before and after. No frozen semantic artifact was edited.

## Operational results

- Arm B: 11 calls attempted; 10 valid predictions; one malformed response failed closed.
- Arm C: 51 calls attempted; 50 valid predictions across 10 complete five-repetition episodes; the first
  call for the final episode failed closed, so its remaining four repetitions were not run.
- Both malformed responses were for opaque episode `B2-H03` and cited an undeclared evidence reference.
  They were not appended, retried, repaired, or scored. No call timed out.
- Valid result counts: B — 1 `demonstrated`, 6 `not_demonstrated`, 3 `insufficient_evidence`; C — 5, 30,
  and 15 respectively. B had three abstentions; C had fifteen.
- All 10 complete C episodes returned one identical result across their five repetitions: 0/10 episode
  disagreement, measured only on complete episodes. The incomplete episode is excluded, not imputed.
- Measured request latency: B median 64.847 s, mean 92.862 s, range 14.433–250.117 s (`n=10`); C median
  11.749 s, mean 27.240 s, range 8.935–246.264 s (`n=50`). These are client-observed end-to-end call
  durations for valid responses, not server compute-only latency.
- Monetary cost and energy were not measurable. No host power telemetry or billing meter was available.
  The endpoint is locally operated, but zero marginal charge is not asserted from that fact.

## Evidence boundary and handoff

`arm-bc-predictions.jsonl` is the append-only opaque prediction ledger. It contains accepted clause
results, rationales, evidence references, model/config hashes, and latency. The frozen runner validates a
response before appending it, so rejected model response bodies and vendor timing/token metadata are not
retained; `arm-bc-errors.jsonl` records only the observed failure class and no invented raw response.

No agreement, false-advancement, expressibility, or accuracy claim can be made here. The next gate is
custodian scoring followed by independent validation of the sealed score outputs and disagreement dossiers.
Grade recommendation is deliberately withheld.
