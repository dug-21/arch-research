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

---

## Feasibility rework 1 ruling — `d0905b4`

**Verdict:** **REWORKABLE FAIL**
**Validator recommendation:** **Do not freeze the replacement corpus/language and do not launch B/C.**

The rework closes the originally reported plaintext-files defect on the owned branch and supplies the
missing runner, policy, prompt, attestations, and integrity commitment. It does not yet establish the
claimed operational seal.

### Independent results

| Check | Result | Evidence |
|---|---|---|
| Owned branch ancestry | PASS, bounded | `research/jurati-001` is exactly `main` `4667db9` → gate record `99c3a60` → candidate `d0905b4`. Neither `2ae4b15` nor `7d8c28e` is an ancestor or contained by a branch. |
| Old leaked object unreachability | **FAIL** | Both leaked commits remain in the local object database and are enumerated by `git reflog --all`; `git fsck --no-reflogs --unreachable` identifies both commit objects. They remain directly readable by hash/reflog even though excluded from branch ancestry. The assertion that the old leaked material is unreachable is therefore false for the effective repository available to the semantic roles. |
| Strengthened corpus verifier | PASS, bounded | Three independent fresh invocations pass counts, split/cap, custody commitment, packet digests/schema, tracked-file scan, main-to-HEAD patch scan, and generated-file checksums. These scans omit reflogs/unreachable objects and therefore do not detect the preceding failure. |
| Checker and replay | PASS | All 14 tests pass, including frozen-policy and opaque-packet tests; the test fixture performs three fresh-process replays with identical verdict/action. |
| Freeze commitments | PASS | All 22 named file digests and the aggregate digest independently recompute exactly. |
| Arm A | PASS, bounded | 225 unique episode/repetition rows (45 × 5) match the summary; all are arm A, `insufficient_evidence`, and non-advancing. This demonstrates reducer stability only, not semantic accuracy. |
| Public custody handoff | PASS, bounded | Without opening restricted mapping/labels: public handoff is mode `0600`, SHA-256 `5b023908...`; its packet-manifest/schema commitments match the tracked commitment. Custody root and judge-input/restricted directories are mode `0700`. |
| Custody access separation | **FAIL** | The custody root, restricted directory, worktree, PoC, and semantic runner are all owned/run as Unix principal `vscode`. Mode `0700` excludes other principals but does not exclude this runner or any other role in the current execution environment. Thus “external W1 custody” is procedural, not a filesystem/read-authority boundary. The validator honored the role restriction and did not open the restricted files, but the runtime does not enforce it. |
| W2/W4/W5/W6 attestations | PASS, attested | All four named roles provide affirmative, role-specific non-inspection attestations with caveats. These are attestations, not measured access controls. |
| Frozen B/C runner surface | PARTIAL | Prompt, strict response validation, model names/digests, seed/temperature/top-p, B=1/C=5 repetitions, timeout, and JSONL logging are committed and integrity-bound. No tracked or untracked B/C result ledger was found, and no B/C call was made by this validator. |
| Evidence exclusion | **FAIL** | `semantic-policy-v1.json` declares verdict/recommendation/outcome line exclusions, but `run_semantic.py` never reads or applies `evidence_exclusion`; it sends packet evidence verbatim. Structural scanning without consulting labels finds outcome-bearing material in 9/11 holdout packets: two have explicit verdict/recommendation/outcome headings, nine have PASS/FAIL-style result tables, two have `Overall: PASS|FAIL|WARN`, and one has a direct result/status heading. This violates the scope rule that historical verdict summaries are withheld from judge inputs unless themselves the evidence under test. |
| Ollama envelope | PASS | Live `/api/version` returns `0.32.5`. Live `/api/tags` returns the frozen `qwen2.5-coder:32b` digest `b92d6a0b...` and `qwen3-coder:30b` digest `06c1097e...`. |
| Semantic launch status | NOT RUN | No B/C invocation or semantic result artifact was observed. This ruling made no model call. |

### Failing clauses and remedies

1. **Repository-object leakage:** use a clean clone/object store whose refs and reflogs have never contained
   `2ae4b15`/`7d8c28e`, or remove the leaked objects from the effective repository and independently prove
   they cannot be resolved through branches, tags, reflogs, alternate object stores, or direct object
   lookup. Merely rebuilding the branch is insufficient.
2. **Custody authority:** place restricted labels/mapping under a distinct OS principal or external service
   whose ACL denies the account executing the language author, PoC, and semantic runner. Provide the runner
   only the committed sanitized packets and the later scoring custodian only the sealed prediction ledger.
3. **Verdict-summary contamination:** regenerate replacement judge packets through the frozen exclusion
   policy, fail closed on residual outcome-bearing headings/tables, and have the verifier test the effective
   bytes sent to Ollama. Alternatively, preregister per-episode cases where an outcome is intentionally the
   evidence under test and exclude those fields from scoring the same historical outcome. The currently
   unused policy declaration is not an implemented control.

After repair, a second and final rework gate may rerun. Capability #256 remains `missing` and technology
#257 remains `claimed`; this intermediate artifact supports neither `partial` nor `proven` advancement.
No Unimatrix read/write beyond the prior independent live-node fetch was needed for this rework ruling,
and no restricted label/mapping value was inspected.
