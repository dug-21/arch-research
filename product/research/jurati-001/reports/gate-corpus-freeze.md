# jurati-001 corpus-freeze / internal-feasibility gate

**Verdict:** **REWORKABLE FAIL**  
**Artifact reviewed:** executable candidate at `2ae4b15`  
**Validator:** `jurati-001-validator` (gate-input independent; no build or advisory participation)  
**Recommendation:** **Do not freeze the corpus/language and do not launch semantic arms B–F.**

## Gate basis

The live capability fetched independently from Unimatrix is #256, **Evidence-bound decision evaluation and
deterministic next-action resolution**, currently `grade:missing`. Its `done_when` requires a frozen,
cycle-disjoint cross-domain corpus; one shared semantic model expressing at least 90% of eligible holdout
decisions without per-decision evaluator code; identical verdict/action replay for fixed clause results;
zero observed false advancements and at least 90% exact-next-action agreement in each domain; and localized,
fail-closed disagreement. Technology #257 is the `grade:claimed` v0.1-dev language candidate and explicitly
states that sealed replay and inference reliability remain untested.

This is an intermediate freeze gate, not a claim that #256 is complete. The candidate clears the mechanical
replay portion but does not yet establish an operationally sealed or runnable semantic experiment.

## Clause mapping

| Gate clause | Result | Independent evidence |
|---|---|---|
| Corpus size and cross-domain subject | PASS | 45 unique episodes: 32 SDLC and 13 research-garage. The selected subjects are real workflow decision episodes rather than an adjacent benchmark. |
| Cycle-disjoint split and contribution cap | PASS | Repeated verifier runs report the predeclared 16/8/8 SDLC and 7/3/3 garage decision split; every cycle is partition-exclusive and contributes at most three episodes. |
| Pinned source and packet integrity | PASS, bounded | `SHA256SUMS` verifies all 49 generated files at commit `2ae4b15`. All 11 holdout packet evidence digests independently match bytes from Unimatrix commit `7ac778d...` or garage commit `5d4ccdd...`. The co-located checksum list does not independently attest the checker/spec/task; the Git commit is the present outer integrity boundary. |
| Checker self-tests and deterministic replay | PASS, bounded | Twelve tests pass, including green/red, evidence tamper, missing transition, undeclared evidence, illegal advancement, judge widening, injection-as-data, fail-closed contradiction/insufficiency, locality, and three fresh-process replays. The corpus verifier passed four fresh invocations. |
| Repetition and physical plausibility | PASS, bounded | Arm A records `n=225` (45 episodes × 5), 0 disagreements, and 0 advancements because every synthetic residual clause is forced to `insufficient_evidence`. Sub-millisecond pure-reducer timing is plausible but is not end-to-end judge latency or semantic accuracy. |
| Holdout sealing and leakage control | **FAIL** | `corpus-generated/reference-labels.jsonl` contains plaintext reference class, exact next action, provenance, and state for all 11 holdout IDs. `corpus-generated/sealed/holdout-map.json` contains each real cycle, source path, and complete label and is an ordinary committed mode-0644 file. `verify_freeze.py` only excludes these fields from each packet's `judge_facing` object; it does not prevent W2–W5 or a semantic runner from reading the two label-bearing files. This fails the scope's sealed-holdout/non-inspection boundary and the independent review's requirement to keep labels outside broadly consumed artifacts. |
| Non-inspection attestations | **FAIL** | The sole attestation is from `jurati-001-poc`. The required W2–W5/language-author non-inspection attestations are absent, and the readable committed labels make the intended operational control unenforced. |
| Frozen runnable semantic task | **FAIL** | No semantic runner, frozen prompt, parsing policy, or evidence-retrieval/exclusion implementation exists. Packets carry source digests but not evidence bytes. `RESULTS.md` correctly says a future runner must retrieve and verify bytes and apply verdict-summary exclusion. Therefore B/C cannot be launched against a fully frozen task without adding experiment-defining code after this gate. |
| Effective environment and Ollama version | **FAIL** | Live `/api/version` returns `0.32.5`; `capture_environment.py` records that exact API field, and `effective-envelope.json` records `0.32.5`. `/api/tags` contains model metadata and no `0.11.4`. Repository search finds `0.11.4` only in `RESULTS.md`; no probe, field, model metadata, or artifact supports it. Thus `0.32.5` is the Ollama server version, while `0.11.4` denotes nothing demonstrated by this artifact and is an erroneous/unsupported prose value, not a second legitimate version dimension. |
| Measured versus attested boundary | PARTIAL | Endpoint version, model list/digests, Python/platform, checker behavior, corpus counts, and reducer timings are measured. Non-inspection, no pull/eviction, and no semantic launch are attestations. Residency and host hardware are explicitly unmeasured. `RESULTS.md` blurs this boundary only in the unsupported `0.11.4` sentence. |
| Capability proof / grade | NOT REACHED | No semantic holdout evaluation, expressibility score, per-domain exact-next-action result, or least-cost policy exists. #256 must remain `missing`; #257 must remain no higher than `claimed`. |

## Failing clauses and remedies

1. **Leakage-control failure.** Move holdout labels and opaque-to-real mappings outside the repository and
   outside the filesystem/read authority of language authors and semantic judges. Commit only opaque IDs,
   aggregate counts, and cryptographic commitments. Add a fail-closed launch wrapper that gives the judge
   only verified evidence/question bytes and never exposes reference outcomes or source-identity metadata.
2. **Attestation failure.** Obtain explicit non-inspection attestations from every W2–W5 participant that
   will touch grammar, prompts, policy, calibration, or holdout replay. Because the present files were
   broadly readable, confirm whether any intended author/judge inspected them; if so, allocate a new
   untouched holdout rather than reusing this one as blind.
3. **Incomplete frozen task.** Before approval, add and pin the B/C runner, prompt(s), decoding parameters,
   response parser, evidence retrieval with digest verification, verdict-summary exclusion, repetition and
   quorum rules, logging schema, and launch-time checks. Extend the integrity commitment to the spec,
   examples/contracts, checker, runner, prompts, policy, and public commitments—not only generated corpus
   files.
4. **Environment-report contradiction.** Replace `0.11.4` in `RESULTS.md` with the measured Ollama server
   version `0.32.5`, or attach a reproducible probe and name the distinct component/field if `0.11.4` was
   intended to describe something else. Current evidence supports only `0.32.5`.

After these repairs, rerun this independent gate. The existing corpus composition, source digests,
mechanical reducer, and self-tests need not be redesigned unless leakage audit shows an intended holdout
judge or language/prompt author saw the exposed labels.

## Grade recommendation

- Capability #256: **missing** — its sealed replay clauses are not reached.
- Technology #257: **claimed** — executable mechanical evidence now exists, but the operational freeze and
  semantic proof are absent; no `proven_by` envelope is supportable.

No Unimatrix write or grade mutation was made, and no semantic B/C call was run. The validator did not read
the values of the sealed holdout labels while performing the structural and digest checks.
