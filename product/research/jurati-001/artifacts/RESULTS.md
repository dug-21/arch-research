# jurati-001 W3/D15 feasibility handoff

## Result

The executable corpus candidate and deterministic interpreter pass their internal freeze and checker gates.
This is evidence that the contract/checking stack works; it is not a grade and does not establish holdout
agreement or the Jurati premise.

## Frozen-candidate corpus

- 45 episodes: 32 SDLC and 13 garage.
- Partitions: SDLC 16/8/8 and garage 7/3/3 decisions across development/calibration/holdout.
- The original 11 holdouts were invalidated because their allocation was reachable in `main` history.
  W1 supplied 11 replacement episodes from six previously unused cycles as sanitized opaque packets.
  Handoff digest: `5b0239085a70bcfacde6f9b77a09c280d3c34fb70a3cedce1869aa495b74c7c1`;
  packet-manifest digest: `68367443efc7adb5f71aa99b6f36676bc8f44e462eda722202b05612dc34134c`;
  schema digest: `12e143feb80b5615d6bfa744520316b54f0fbcea1bac6bad6ff11ebd0f7785fb`.
- Internal verifier: PASS for aggregate counts, cycle-exclusive partitions, three-episode cap, mapping
  completeness, packet integrity, reference-field leakage, clear-text holdout identity/path leakage, and
  final checksums.
- Identity mapping and labels remain under external W1 custody and were not exposed to this role. The
  consumed public handoff is mode 0600. Per-role attestations are in `non-inspection-attestations.json`.
  The owned branch was rebuilt from `main`; no owned reachable commit contains the invalid generated map
  or labels.

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
false advancement was 0/225. Reducer timing was 0.000711–0.002583 ms, mean 0.000966 ms. These are local
process timings, not end-to-end decision latency, and are physically plausible for a small pure function.

At run-start capture, the Ollama server API reported version `0.32.5` at the authorized endpoint. No
separate client-library version was measured. Available authorized models:

- `qwen2.5-coder:32b`, digest `b92d6a0bd47ee79114298de0177bf920c05a706d12633950b3936778492bef41`;
- `qwen3-coder:30b`, digest `06c1097efce0431c2045fe7b2e5108366e43bee1b4603a7aded8f21689e90bca`.

Model residency and host hardware were not measured. No pull, eviction, or host configuration occurred.

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
