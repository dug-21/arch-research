# W0-f — Declared-vs-actual conformance over the SDLC corpus

**Run:** `wfh-004` · Issue #48 · phase `scan` (rebuild) · read-only, zero graph writes.
**Method:** shallow-cloned `dug-21/unimatrix` rather than fetching files — this converted the exercise **from a sample to a census**. Every number is over all **231 units** unless marked. `gh` code search was never used (it is broken on this corpus).

---

## 1. Case definitions (stated before any count)

| Term | Definition used |
|---|---|
| **Unit** | A directory directly under `product/features/`. **231** `[V]`. 167 feature-named, 64 `bugfix-*` |
| **Delivered unit** | A unit with ≥1 **merged** PR whose head branch is `feature/<unit>` or `design/<unit>`, or whose title carries `[<unit>]`. **161 of 167** feature units `[V]` |
| **Gate report** | A blob whose basename contains `gate-(3a\|3b\|3c\|bugfix)` **and** `report`, excluding `agent-\d` basenames. **719 files** `[V]` |
| **Canonical gate report** | A gate report under `<unit>/**/reports/`. **553**. The other **166** live under `<unit>/agents/` — a second, unstandardised filing of the same verdict |
| **Gate instance** | A distinct `(unit, gate-kind, bugfix-issue)` triple — what the ≤2 bound applies to |
| **Rework iteration** | An additional *attempt* at one gate instance, evidenced by a distinctly-labelled attempt artifact |
| **Gate failure** | The gate's `Result:`/`Verdict:` line resolving to `REWORKABLE FAIL` or `SCOPE FAIL`. Distinct from a **check-level `FAIL`** cell inside the Summary table |
| **Declared vocabulary** | `uni-validator.md` §Step 4 + report template: gate result ∈ `{PASS, REWORKABLE FAIL, SCOPE FAIL}`; check status ∈ `{PASS, WARN, FAIL}` `[V]` |

## Two corrections to W0-b2b, before anything else `[V]`

1. **The corpus is 6,781 files, not 7,975.** 7,975 counted tree entries minus unit directories — i.e. **files plus sub-directories**. Actual blob count: **6,781**.
2. **`WARN` *is* defined.** `uni-validator.md:196` — *"**WARN**: Minor gap that doesn't block progress"* — and line 203, *"All checks PASS (WARNs acceptable) → PASS"*. W0-b2b read the *protocols* and concluded the field invented a verdict; **the definition lives in the agent definition, not the protocol.** The real defect is different, and is quantified in §3.

---

## 2. The conformance table — and why the "29-unit attrition gap" does not exist

**The 224 / 226 / 195 figures are FILE counts, not UNIT counts.** This classifier reproduces them exactly (224+226+195+74 = 719), confirming W0-b2b's method — and thereby showing the *"224 units produced Gate 3a, 195 produced Gate 3c, 29 units left no final gate"* claim **compared two file counts as if they were unit counts.** At unit level: **157 units have a 3a file, 157 have a 3c file** `[V]`. The gap is an artifact of duplicate filings (166 `agents/` aliases) and rework attempts.

**Corrected — census over 161 delivered feature units** `[V]`:

| Gate | Report present | Rate | Units missing it |
|---|---|---|---|
| 3a | 155 / 161 | 96.3% | `684-685`, `nan-013`, `col-014`, `crt-012`, `nxs-007`, `vnc-010` |
| 3b | 155 / 161 | 96.3% | same six |
| **3c** | **154 / 161** | **95.7%** | the six, **plus `crt-043`** |

**What the gap is made of** — every unit chased to a merge record `[V]`:

| Class | n | Units | Reading |
|---|---|---|---|
| Scoped, never started | 4 | `col-016`, `vnc-029`, `vnc-032`, `vnc-036` (1 file each) | Legitimate — no PR exists |
| Abandoned at design | 1 | `alc-003` (19 files, full design set) — **PR #301 CLOSED, not merged** | Legitimate |
| Misfiled report dumps | 2 | `684-685`, `nan-013` — stray agent reports; both merged as *bugfix* branches | Naming nonconformance, not attrition |
| Gated normally, no branch-matched PR | 1 | `nxs-001` (full 3a/3b/3c) | Merge path not resolvable by branch name — not a gate gap |
| **Shipped to main with NO gate artifact of any kind** | **4** | **`nxs-007`** (PR#102, 2026-03-05), **`col-014`** (PR#140), **`vnc-010`** (PR#142), **`crt-012`** (PR#148, all 2026-03-08) | **Confirmed conformance failure** |
| **Shipped without a final gate** | **1** | **`crt-043`** (PR#506, 2026-04-03) | **Confirmed — the sharpest case in the corpus** |

The four ungated units' Issues (#79, #113, #43) and PRs were checked for a gate recorded elsewhere: **none exists** — only "Implementation Complete" comments and, on two, a security review `[V]`. The gate protocol was demonstrably live: **14 feature units merged in 2026-02 with 100% Gate-3c presence** `[V]`.

### `crt-043` — the single sharpest instance

No Gate 3c report exists at any path. What exists instead is a line in the **PR body checkbox list** `[V]`:

```
- [x] Gate 3c risk coverage: CONDITIONAL PASS — server-level embed stub tests deferred to #505
```

**A final gate, self-declared by the delivery leader rather than a validator, in an artifact the protocol does not designate, with a verdict — `CONDITIONAL PASS` — that appears in no definition.** The unit merged. **Three days later `bugfix-505` (PR#533) landed against exactly the gap the conditional pass had deferred.**

**Time series — the failure is not ongoing** `[V]`: Gate-3c conformance by merge month = **100%** (Feb, n=14) · **95.1%** (Mar, n=81) · **94.1%** (Apr, n=17) · **100%** (May/Jun/Jul, n=47). **All 5 confirmed failures fall inside a 30-day window, 2026-03-05 → 2026-04-03.**

### The bugfix side — and the inference deliberately *not* made

Filenames say **18 of 61 merged bugfix units shipped with zero gate artifact** — which would read as a live, ongoing 30% conformance failure. **It is not.** `uni-bugfix-protocol.md:631`: *"All phase outputs … are posted as **GH Issue comments** — never written to the filesystem"* `[V]`. All 18 Issues' comments were fetched: **16 carry a full Bug Fix Validation gate comment with a verdict** `[V]`.

**Confirmed bugfix gate absence: 2 of 61** — `bugfix-358` and `bugfix-369` `[V]`.

**This is itself a finding about the definition, not just the field:** the same protocol says `git add product/features/{issue-number}/` at line 389 and *"never written to the filesystem"* at line 631. The field split ~2:1 between the two readings (42 filesystem / 19 not). **A definition that contradicts itself produces a corpus in which absence is uninterpretable without a second lookup** — which is exactly why the naive filename count would have been wrong by **9×**.

---

## 3. The verdict distribution

Census, all 719 gate reports. The two populations behave differently and are reported separately `[V]`.

**Canonical (`reports/`), n = 553 — 100% parsed:**

| Verdict | n | % |
|---|---|---|
| PASS | 499 | 90.2% |
| PASS, qualified (`PASS (2 WARNs)`, `PASS (re-validation…)`) | 16 | 2.9% |
| **REWORKABLE FAIL** | **38** | **6.9%** |
| **SCOPE FAIL** | **0** | **0.0%** |

By gate: 3a — 147 PASS / 15 FAIL (n=165) · 3b — 152/16 (n=174) · 3c — **155/4** (n=160) · bugfix — 45/3 (n=54).

**Alias (`agents/`), n = 166:** 24.1% REWORKABLE FAIL, and **29 files (17%) have no parseable verdict line at all.** This population is free-form; the canonical one is templated. Only **2 of 553** canonical reports lack a `Result:` line.

### `SCOPE FAIL` fired zero times in 231 units

Every `SCOPE FAIL` string in the corpus (7 files) is a *negation* — *"NOT a SCOPE FAIL"* `[V]`. The declared escalation branch — *"If iteration count reaches 2 for any gate, escalate to SCOPE FAIL"* — **never executed once.**

> That is the SDLC instance of a declared step that never ran, and unlike the 29-unit claim **it is exact.**

### The `WARN` question, restated correctly

`WARN` is a **check-level** status and is properly defined. Its use is heavy and legitimate: **276 WARN cells across 4,181 check cells (6.6%)**; **186 of 553 reports (33.6%) carry ≥1 WARN** `[V]`.

The actual nonconformance is **vocabulary leakage upward**: **16 canonical reports put WARN in the gate-level `Result:` line** (`PASS (3 WARNs)`), where the template permits exactly three literals. Plus 12 with free-text qualifiers and 1 with no Result line — **29 / 553 = 5.2% template nonconformance at the one field the orchestrator branches on** `[V]`. Add `CONDITIONAL PASS` from crt-043: **at least four verdict values circulate that the definition does not contain.**

**Also: 89 of 553 canonical reports (16.1%) have no recognisable `| Check | Status |` summary table** — the template's central structure is absent from a sixth of the corpus `[V]`.

### Is the low failure rate excellence, or a non-binding gate? The evidence *can* distinguish — and the answer is neither

**6.9% is a floor, and a badly-biased one.** Every canonical report was searched for text evidencing an earlier failed attempt `[V]`:

- **22** such reports have a sibling attempt artifact — the failure is preserved.
- **53** have **no sibling**: the gate report was **overwritten in place**, the FAIL destroyed, only a PASS on disk.

Worked example, both halves surviving *by accident* `[V]`:

- `crt-056/agents/…gate-3c-report.md` → *"Result: **REWORKABLE FAIL** … FAIL on test-coverage completeness: AC-1 and AC-2 have NO implementing test; RISK-COVERAGE-REPORT marks both PASS **vacuously**"*
- `crt-056/reports/gate-3c-report.md` → *"Gate: 3c — RE-VALIDATION after REWORKABLE FAIL … Result: **PASS**"*

The canonical path retains only the PASS. **The FAIL survives solely because a duplicate filing convention nobody standardised happened to preserve it.**

> **At least 75 of ~538 gate instances (≥13.9%) failed at least once, against 38 (6.9%) visible in the canonical record.** The gate *does* bind — it produces real FAILs with substantive findings — but **the artifact record systematically under-reports its own failure rate, because the evidence is a mutable file with no append discipline and no immutable attempt identity.**

---

## 4. The rework bound (≤2, then escalate)

Distinct attempts per gate instance, deduped across the `reports/`⁄`agents/` double-filing and across bugfix-issue within a unit `[V]`:

| Attempts | Reworks | Gate instances |
|---|---|---|
| 1 | 0 | 505 |
| 2 | 1 | 31 |
| 3 | **2 — exactly at the bound** | 2 |
| **4+** | **>2 — violation** | **0** |

The two at the bound: `crt-043` gate-3a and `vnc-018` gate-3b. A full-corpus grep for third/fourth-iteration language returns **one** hit, unrelated `[V]`.

**Verdict: the ≤2 bound was honoured — no violation found.** This is the one place the SDLC corpus is *cleaner* than the research register's 17-authorized/33-written.

**But confidence is bounded by the same defect as §3.** 53 reworks left no artifact; if any unit reworked twice within one overwritten file, the count is invisible. What *can* be said: (a) no unit exceeded 2 in any observable form, and (b) **the bound's declared consequence — escalate to `SCOPE FAIL` — never fired, so nothing was ever *stopped* by the bound. A bound whose enforcement branch has zero executions in 231 units is unfalsified, not verified.**

---

## 5. Detection failures — verification ran, and the defect shipped anyway

Cross-referenced all 64 bugfix units' report text against feature-unit IDs and `Files Modified` sections `[V]`.

- 41 of 64 bugfix units name ≥1 feature unit in their own reports; 57 of 64 contain regression/root-cause language.
- **35 bugfix→feature links** where the named feature unit had **Gate 3b PASS + Gate 3c PASS + a security-reviewer report** before the bugfix.

Name-mention is weak, so the load-bearing evidence is **file-level** — source files named in `Files Modified` of **two or more distinct bugfix units** `[V]`:

| Source file | Distinct bugfixes | Feature units that shipped it (all 3a/3b/3c PASS + security review) |
|---|---|---|
| `…/src/background.rs` | **10** | col-023, col-031, crt-014, crt-018b, crt-019, crt-021 |
| `…/src/mcp/tools.rs` | **7** | col-022, col-023, col-025, col-026, col-028, col-031 |
| `…/src/infra/config.rs` | 5 | col-031, crt-022, crt-023, crt-024, crt-026, crt-029 |
| `…/src/server.rs` | 4 | col-001, col-009, col-010b, col-022, col-023, col-025 |
| `…/src/uds/listener.rs` | 4 | col-018, col-022, col-023, col-025, col-027, col-028 |
| `…/src/services/nli_detection_tick.rs` | 4 | crt-029, crt-037, crt-039, crt-040 |

**22 source files were fixed by ≥2 separate bugfix units; 44 of 53 files named in bugfix change-sets had previously shipped through the full three-gate + security-review pipeline** `[V]`.

Individually confirmed by reading root-cause statements `[V]`:

| Bugfix | Against | The defect the verification layer passed |
|---|---|---|
| **505 → crt-043** | crt-043 | Gate 3c self-declared `CONDITIONAL PASS` in the PR body, deferring the exact tests; #505 supplied them 3 days later. **The gate named its own gap and merged anyway** |
| **469 → crt-037** | crt-037 | Three guard sites with inverted semantics |
| **421 → crt-029** | crt-029 | `nli_detection_tick.rs` made zero progress after the first tick — a *functional dead-end*, passed by 3a, 3b, 3c and a security review |
| **286 → crt-014** | crt-014 | `get_embedding` iterated only HNSW layer 0; ~1/16 of points per level above 0 unreachable. **A probabilistic correctness bug — invisible to any test that does not exceed the level-assignment threshold** |
| **473 → crt-037/039** | crt-037/039 | Informs phase starved of per-tick budget |
| **crt-056 (self)** | crt-056 | Gate 3c caught `RISK-COVERAGE-REPORT` marking two ACs **PASS vacuously** — a report asserting coverage no test implements. The validator named it *"the #4202/#3935 pattern"* — a **recurring, named** failure mode |

**What this says at the harness altitude.** Three of the six mechanisms are **structurally invisible to "run a reviewer"**: a *vacuous* coverage claim (a report row with no implementing test), a *probabilistic* reachability bug, and a *deferred* gate that recorded its own deferral as a pass. The first is a **machine-checkable join** (does the cited test exist and assert?) — and `crt-056`'s validator performed it **by hand, by reading**. The last needed only a check that the final gate's artifact exists at the declared path before merge is allowed.

---

## 6. Method and limits

**Censused** `[V]`: all 231 unit directories · all 6,781 file paths · all 719 gate reports' verdict lines and Summary tables · all 359 PRs · rework-attempt labels across all gate instances · `Files Modified` across all 64 bugfix units.

**Sampled** `[V]`: 18 Issue comment threads (a census of the filesystem-gate-less subset, not of all 61) · 6 bugfix root-cause reports in full · 5 feature-side PR/Issue threads.

**Established:** the 29-unit attrition gap is a **file-vs-unit category error**; real Gate-3c conformance is **95.7%** · **5 feature units shipped without declared gates**, all inside a 30-day window, none since · **2 bugfix units** with no gate record anywhere · **`SCOPE FAIL` has zero occurrences in 231 units** · **the ≤2 rework bound was not violated** · **≥53 gate failures were overwritten in place**, making 6.9% a biased floor against ≥13.9% actual.

**Not established, and why:**
- **Whether an unrecorded gate *ran*.** Filesystem, Issue and PR all checked; nothing found. But *"no artifact anywhere we looked"* is not *"did not run."* **Settled by: nothing in this corpus. Only a harness that records gate execution independently of the gate's own output could answer it.**
- **The true rework distribution.** The 53 overwrites make the upper bound unknown. **Settled by:** `git log --follow` on each canonical gate-report path (needs a full clone) — would recover every overwritten verdict and convert §3's floor into an exact number. **The single cheapest remaining measurement.**
- Whether the other 43 bugfix units carry duplicate or contradictory Issue-comment verdicts.
- Whether a bugfix's target feature is causally correct — six links read and confirmed; the remaining 29 rest on ID co-occurrence plus shared file paths (`[I]`, not `[V]`).

**Parse failures, reported rather than dropped** `[V]`: 29/719 reports with no parseable verdict · 89/553 canonical reports with no standard check table · 166 duplicate filings under a second naming convention **with no rule declaring which is authoritative** · 2 unit directories not following the naming convention · **`uni-bugfix-protocol.md` contradicts itself on output location (line 389 vs 631).**

**Scope caveat.** These are operating facts of **one owner's SDLC**, n=1 on the definition. **What generalises is not the rate but the class:** a mutable per-gate artifact with no attempt identity · a verdict vocabulary that leaked at 5.2% because nothing validated the field · an escalation branch with zero executions · a definition whose two halves disagree about where its own outputs go — **none of which any of the five workflow definitions can detect about itself.**
