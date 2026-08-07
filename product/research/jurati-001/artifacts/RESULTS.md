# jurati-001 W3/D15 feasibility handoff

## Result

The executable corpus candidate and deterministic interpreter pass their internal freeze and checker gates.
This is evidence that the contract/checking stack works; it is not a grade and does not establish holdout
agreement or the Jurati premise.

## Frozen-candidate corpus

- 45 episodes: 32 SDLC and 13 garage.
- Partitions: SDLC 16/8/8 and garage 7/3/3 decisions across development/calibration/holdout.
- Two earlier holdout allocations were invalidated: the first was reachable in `main` history; the first
  replacement exposed outcome-bearing evidence. W1 supplied a second replacement from six previously
  unused cycles as sanitized opaque packets. Handoff digest:
  `de2e87b179ed48e032756f36b2360269dd80c371af5632030bf6242f76092286`; packet-manifest digest:
  `1b310a137cf20e28339cb50e73757081c50f2b10287465fb9aa5f002e42d9590`; schema digest:
  `3a1c3d9e264231b5f0c7b0cb9332b5d617bfee9b603834538e62bfbdc51806e2`; encrypted-custody digest:
  `2006fea93c8be898b672e4f8538781f3ab8f67dcc19c9b5c4b64547e947c6fee`.
- Internal verifier: PASS for aggregate counts, cycle-exclusive partitions, three-episode cap, mapping
  completeness, packet integrity, reference-field leakage, clear-text holdout identity/path leakage, and
  final checksums.
- Identity mapping and labels remain encrypted under external W1 custody; its key was neither persisted nor
  returned. The public handoff is mode 0600. The PoC imported only its named judge packets, then removed 18
  lines matching frozen outcome-token, outcome-heading, result-table, or summary-field rules. A structural
  rescan passes. Per-role attestations are in `non-inspection-attestations.json`.
- The safe artifact was recreated in an independent clone/object database from `origin/main`, using file
  contents only. The four old leaked/rework object hashes are unknown and unrecoverable there; `git fsck`
  reports no unreachable objects.

## Checker and interpreter

Fourteen tests pass: known-green, known-red, mechanically tampered evidence, missing transition, undeclared
evidence, illegal transition, judge response widening, prompt injection in evidence, contradiction and
insufficiency no-advance, one-clause counterfactual locality, frozen policy validation, opaque packet
validation, and three fresh-process replays. The runtime
implements total transition validation, evidence digest verification, a pure deterministic reducer,
response confinement, and JSONL append-only run records.

## Measurements

Arm A ran five deterministic repetitions for each of 45 episodes (`n=225`). Every residual semantic
clause returned `insufficient_evidence`, every action escalated, repeated-run disagreement was 0/225, and
false advancement was 0/225. Reducer timing was 0.000710–0.003856 ms, mean 0.000944 ms. These are local
process timings, not end-to-end decision latency, and are physically plausible for a small pure function.

At final-rework capture, the authorized Ollama endpoint timed out in both the five-second Python probe and
a separate 15-second curl probe. Server version, current model list, residency, and host hardware therefore
were not measured in this run. The frozen policy retains the previously measured authorized model digest,
but B/C remains blocked on renewed reachability as well as the gate. No pull, eviction, or host
configuration occurred.

## Gate and blocked arms

The mandatory human corpus-freeze gate has not yet approved the reworked generated artifacts. Consequently, no
semantic model saw calibration or holdout material and arms B/C were not launched. After approval, the
frozen task/checker/language candidate may run B once and C five times per preregistration, without edits.

Arms D/E are blocked: the owner authorized a high provisional budget but no provider, eligible immutable
frontier snapshot, or configured ordinary task credential was specified or discovered. Arm F is blocked
pending two human raters and an adjudicator. These arms were not simulated.

## Caveats and recommendation

Generated holdout packets contain sanitized evidence and opaque IDs only. The frozen runner passes only the
bounded decision type and sanitized evidence to Ollama; it has no access to source identities or labels.
Until semantic arms run, exact-next-action agreement, expressibility, and least-cost reliable judge policy
are not measured.

Grade recommendation: **partial / rework**, pending corpus-freeze approval, B/C execution, and independent
validator review. Do not recommend `proven`.
