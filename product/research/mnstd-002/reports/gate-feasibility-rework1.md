# mnstd-002 — Gate spot-check: feasibility rework 1 (C5.3 checker)

- **Validator:** factory-validator (agent_id `factory-validator`). I did not build this artifact or advise on building it.
- **Scope:** a bounded spot-check of C5.3 only, as the owner ruling requires ("fix the C5.3 checker so it actually
  recomputes its result … factory-validator confirm the fix"). This is not a re-gate of any other clause.
- **Subject:** branch `research/mnstd-002` @ `1bc97ca`, diffed against the gated `17a7fa4`. I made my own detached
  worktree and built in it.
- **Bar:** C5 #333 (fetched live via `context_graph(mode:"current")`; Active, v1). C5.3: *"v2 compiles via C1 to
  HTML, PDF and XML. For each accepted or modified comment, the v2 element reached through C2.4 contains the change,
  checked mechanically against the comment's `proposed_change` (accept) or the recorded modified text (modify)."*
- **Prior defect (gate-feasibility.md §4.1):** `checks.c5` trusted `trace/containment.json` and did not detect a
  post-hoc revert in v2 XML.

## Verdict: **PASS** (C5.3 checker fix confirmed)

The checker now re-derives containment from `v2/draft.xml`. It goes red when an accepted or modified change is
removed from v2, and red when `containment.json` alone is tampered. It is green on the untouched v2. Grade
recommendation for C5 is unchanged from the main gate report. This spot-check clears the merge precondition only.

## 1. Diff scope (17a7fa4..1bc97ca, 4 commits, 20 files)

| Claimed | Found |
|---|---|
| Checker recomputes C5.3 | `checks.py`: new `c5_3()`. It parses v2 XML with ElementTree (not the pipeline's resolver or trace code), takes expected text from the register (accept) or the frozen dispositions (modify), requires it to equal the frozen `expect_in_v2`, follows `map/mapping.json` with a tag and anchor agreement check, and cross-checks `containment.json` as a record, not as an input |
| Self-tests | `selftest.py`: +`v2-xml-accepted-change-reverted` (GB-01-003), +`containment-record-disagrees`, +`checker-file-tampered`, +`font-pin-byte-changed` |
| Font pin | `fonts/MANIFEST.json`, `tools/fontpin.py`, `tools/fonts.sh`, Makefile comment |
| Re-freeze | `FROZEN.sha256`: **3 lines added** (checks.py, selftest.py, frozen.py). **The 20 original lines are byte-identical.** No file under `task/` or `poc/src/` appears in the diff |
| Evidence | `artifacts/evidence/*`, `invocations/demo-3.json`, RESULT.md, SNAPSHOT.md, README |

Nothing outside the claim was changed. `frozen.py verify` → `frozen: ok` in my checkout.

## 2. My demonstration (n=1 build, my worktree)

`make once` → exit 0, 37 clause checks, 0 FAIL (4m46s; pinned image, `--network none`). Then I ran `checks.run_all`
on scratch copies of `build/run-a`. I chose the edits myself. None of them is the builder's GB-01-003 case.

| # | Tamper (scratch copy only) | Kind | C5.3 | Problem reported |
|---|---|---|---|---|
| T0 | none | — | **PASS** 10/10 | 0 |
| T1 | GB-01-001 reverted to its v1 text in v2 XML (`250 Hz`→`200 Hz`) | accept | **FAIL** | not contained in `_38a0bd5b…`; record disagrees |
| T2 | GB-02-001 inserted safety sentence deleted from v2 XML | accept/insert | **FAIL** | not contained in inserted ids |
| T3 | PR-US-01-001 sentence deleted from v2 XML | modify/range | **FAIL** | not contained in range union |
| T4 | FR-01-004 `for ten days` removed in v2 XML | modify | **FAIL** | not contained |
| T5 | `containment.json` only: FR-01-002 pass→false (v2 intact) | record | **FAIL** | recorded False ≠ recomputed True |
| T6 | `containment.json` only: GB-01-001 row deleted | record | **FAIL** | recorded None ≠ recomputed True |
| T7 | FR-01-001 text moved out of its mapped element into another element (still present in the document) | accept | **FAIL** | element-scoped, not document-wide |

In every v2-XML case `containment.json` was left as the pipeline wrote it (pass=true). So the red result comes from
recomputation, not from the record. This is the exact case that the main gate's tamper found the checker missed.

The builder's recorded self-test (`selftest.json`, 37/37 detected) includes the required case
`v2-xml-accepted-change-reverted` (green PASS → tampered FAIL). I reproduced its behaviour class independently on
4 other comments, covering all three containment modes (element, insert, range).

**Font pin (optional check, ruling 1):** `make fonts` on the provisioned cache ran offline and printed
`fontpin: ok (45 files)`. On a scratch copy of the cache, one corrupted byte in NotoSans-Bold.ttf failed with a
sha256 mismatch (make exit 2). A deleted font file also failed.

## 3. Residual (does not change the C5.3 verdict; recorded for reuse)

**A coordinated two-file forgery passes C5.3 and C2.4.** I relocated FR-01-004's text into another `<p>`
(GB-01-001's) in v2 XML and redirected FR-01-004's v2 id in `map/mapping.json` to that `<p>`. Results:
C5.3 **PASS**, C2.4 **PASS**, N5.1 **FAIL** ("v2 element not the C2.4 counterpart"), so `run_all` overall is red.

- C5.3 trusts "the v2 element reached through C2.4", which is what the clause says. The tag and anchor guard catches
  redirects that cross element types. A figure-to-p redirect went red in my test. It cannot catch a redirect from
  one anchorless `<p>` to another.
- The gap is in the **C2.4 checker**: it accepted a forged `mapping.json`, so it does not re-derive the mapping
  either. This is the same trust-the-pipeline pattern as §4.1, one layer down. Today N5.1 is the only check that
  catches it.
- **Remedy for reuse (not a merge blocker under the owner ruling's scope):** recompute the v1→v2 mapping in the
  C2.4 checker, or have C5.3 assert that the mapped v2 element is the C2.4 counterpart the same way N5.1 does. Then
  add this forgery as a self-test.

Other caveats:
- Containment is substring-based, which matches the clause's "contains". A revert that leaves the expected substring
  in place elsewhere in the same element would not be detected.
- n=1 build by me. The builder's demo-3 reports two runs from clean.

## 4. Clause mapping

| C5.3 sub-clause | Evidence | Ruling |
|---|---|---|
| v2 compiles to HTML, PDF and XML via C1 | my `make once` exit 0, all three outputs present | PASS |
| v2 element reached through C2.4 contains the change, for each accept and modify | 10/10 recomputed from v2 XML by the checker; T1–T4 and T7 go red | PASS |
| checked mechanically against `proposed_change` / modified text | expected text sourced from the register and the dispositions, equal to the frozen `expect_in_v2`; T5–T6 show the record is not trusted | PASS |

The merge precondition in the owner ruling is met: the checker fails when an accepted change is removed from v2,
the case exists as a tamper test, and an independent validator has confirmed it.
