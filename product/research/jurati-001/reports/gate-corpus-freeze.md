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

---

## Final ruling after feasibility rework 2/2 — `baf03aa`

**Verdict:** **PASS**  
**Human-freeze recommendation:** **Approve the corpus/language freeze.**  
**B/C launch now:** **No — the authorized Ollama endpoint is presently unreachable. Launch B/C without
edits when the pinned endpoint returns and its live version/model-digest preflight passes.**

This PASS is necessary input to the human freeze ruling, not proof of capability #256 and not permission to
advance a graph grade. The prior two failed rulings above remain preserved as the audit trail.

### Independent clause mapping

| Clause | Result | Evidence |
|---|---|---|
| Fresh repository/object boundary | PASS | The validator operated in independent clone `/tmp/jurati-001-fresh.IOh3Zj/repo`, with its own `.git`. Its branch ancestry is exactly `origin/main`/`4667db9` → `baf03aa`. `git fsck --full` is clean. Old hashes `2ae4b15`, `7d8c28e`, `d0905b4`, and `27c30b4` are unknown to `git cat-file` and cannot be resolved in this object database. |
| Failed-ruling preservation | PASS | This report retains the original `2ae4b15` REWORKABLE FAIL and the `d0905b4` rework-1 REWORKABLE FAIL, including their evidence and remedies. |
| Encrypted Custody2 commitment | PASS, bounded | Without opening restricted labels or possessing a key: custody root is mode `0700`; public handoff is mode `0600` and hashes to committed `de2e87b1...`; the opaque encrypted blob is mode `0600` and hashes to committed `2006fea9...`. Public metadata declares AES-256-CBC, PBKDF2-HMAC-SHA256/200,000 iterations, salt, no persisted key, and wrong-key rejection. No key-like file exists under the fresh clone or Custody2 directory. The 11-file judge-input manifest and every packet digest independently match commitment `1b310a13...`. |
| Corpus invariants and packet integrity | PASS | Three fresh verifier invocations pass 45 episodes, 32/13 domain counts, exact per-domain split, cycle isolation, three-episode cap, 11 replacement holdouts, packet/final hashes, sanitized schema, and tracked/reachable-history leakage scans. |
| Identity/path/reference leakage | PASS | Independent scans find no real source paths, identity fields, reference labels, next actions, verdict summaries, or historical-outcome fields in any replacement holdout packet. Serialized label fields occur only in the explicitly non-holdout reference file and generator schema code. Branch history contains no prior leaked objects. |
| Outcome exclusion applied | PASS | `import_custody_handoff.py` actually transforms evidence before writing effective packets, deleting result-table blocks and summary/outcome-token lines, then fails closed if any remain. The committed exclusion summary records 18 removed lines. Independent scans of all 11 effective A2/B2 packets find zero outcome tokens, summary headings, result/status/transition tables, or real repository paths. |
| W2/W4/W5/W6 non-inspection | PASS, attested | All four roles provide affirmative named attestations and caveats; none reports inspecting replacement identities, labels, or outcomes. |
| Frozen task/checker/runner | PASS | All 26 freeze-commitment file hashes and aggregate hash independently match at candidate commit `baf03aa`; these cover scope/spec/examples, prompt, policy, runner, checker, importer, corpus commitments, exclusion summary, environment, Arm A summary, and attestations. The validator gate report is appended after that candidate commitment and is intentionally the only subsequent changed artifact. |
| Checker self-tests / fresh replay | PASS | All 14 tests pass, including opaque sanitized packets and frozen policy, with three fresh-process deterministic replays producing one verdict/action. The verifier passes three separate invocations. |
| Arm A repetition and plausibility | PASS, bounded | 225 unique episode/repetition rows equal 45 × 5; every row is Arm A, returns `insufficient_evidence`, and selects a non-advancing action. This demonstrates the deterministic reducer only, not semantic agreement. |
| No semantic launch | PASS | No B/C result ledger or Arm B/C record exists. This validator made no `/api/generate` call. |
| Ollama preflight | TEMPORARILY BLOCKED | Independent `/api/version` and `/api/tags` probes each timed out. The frozen effective envelope also records the endpoint as unreachable and version/models as unmeasured. This does not invalidate the offline corpus/language freeze, but it blocks B/C launch now. Before launch, require live server version `0.32.5` and `qwen2.5-coder:32b` digest `b92d6a0b...` exactly as frozen; otherwise fail closed without changing task artifacts. |

### Ruling

The human may freeze this replacement corpus and language at `baf03aa`. The experiment may launch Arms B
and C only after the unchanged runner performs a successful live endpoint/model preflight; current timeout
means **not now**. Endpoint recovery alone does not require another corpus-freeze gate because availability
is outside the frozen semantic artifact, but any change to corpus, language, prompt, policy, checker,
runner, model identity/digest, or exclusion logic invalidates this freeze and requires a new untouched
holdout under the scope's leakage rule.

Capability #256 remains `missing` and technology #257 remains `claimed` until sealed semantic replay and
the later firewall evidence clear their own clauses. No graph write or grade mutation was made, and no
restricted identity, mapping, label, or decryption key was inspected.
