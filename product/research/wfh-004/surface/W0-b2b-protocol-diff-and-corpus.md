# W0-b2b — The five-definition diff + the artifact corpus census

**Run:** `wfh-004` · Issue #48 · phase `scan` (rebuild) · `agent_id: wfh-004-researcher-W0-b2` · read-only, zero graph writes.
**Companion to** `W0-b2-sdlc-incumbent.md`. This file carries the material that partition could not: the **empirical layer test** across five workflow definitions, and the **artifact-corpus census**.

## What was sampled (stated, not implied)

| Source | Coverage |
|---|---|
| `dug-21/unimatrix` PR history | **census** — all 359 PRs (354 merged), with check conclusions and merge/check timestamps |
| `product/features/` artifact corpus | **full filename census** (231 units, **7,975 files**, one recursive tree call) + **read sample of 6 unit inventories** and **4 report bodies** |
| SDLC definitions | `uni-research-protocol.md`, `uni-agent-routing.md`, `swarm-protocol.md` in full; `uni-delivery/bugfix/design-protocol.md` by structure + targeted sections; this repo's `sample-delivery.md` in full |
| Research definitions | `theme-scan.md`, `research-scope.md` in full |
| Harness config | `.claude/settings.json` in all three repos; `ci.yml`, `release.yml` |

**Not sampled:** the ~225 units not opened; `.claude/agents/uni/*` bodies; CI logs. **GitHub code search returned 0 for a string that demonstrably exists in the corpus** — code search is unusable here, so a verdict census requires file fetches. Branch protection **403 on all three repos**.

---

## 1. Corpus census — what the SDLC definition actually produced

| Artifact class | Count |
|---|---|
| Delivery/bugfix units | **231** |
| Files in the corpus | **7,975** |
| Gate reports | **719** (224 × Gate 3a, 226 × Gate 3b, **195 × Gate 3c**, 74 × bugfix gate) |
| Retry / rework / revision reports | **83** |
| Security-reviewer reports | **146** |
| Retro-architect reports | **49** |
| Vision-alignment reports | **161** |

> ## ⚠ CORRECTED BY W0-f — read `W0-f-conformance-census.md` §1–2 before using anything in this section
>
> **Two errors in this file, both established by census:**
>
> 1. **The corpus is 6,781 files, not 7,975.** The 7,975 figure counted tree entries minus unit directories — i.e. **files plus sub-directories**.
> 2. **The "29-unit attrition gap" does not exist.** The 224 / 226 / 195 figures are **file counts, not unit counts**, and comparing them as units was a category error. At unit level, 157 units have a 3a file and 157 have a 3c file. **Real Gate-3c conformance over 161 delivered feature units: 154/161 = 95.7%.** The apparent gap is duplicate filings (166 `agents/` aliases) plus rework attempts.
> 3. **`WARN` *is* defined** — in `uni-validator.md`, not in the protocols this file read. The real defect is *vocabulary leakage upward*: 29/553 (5.2%) of canonical reports put a non-template value in the gate-level `Result:` field.
>
> **What survives, sharper than the original claim:** **5 feature units genuinely shipped without their declared gates** (4 with none at all; `crt-043` with a self-declared `CONDITIONAL PASS` in its PR body — a verdict in no definition), all inside a 30-day window. And **`SCOPE FAIL` fired zero times in 231 units** — a declared escalation branch that never executed once. Unlike the 29-unit claim, that one is exact.

**The signal originally read from this table** — *224 units produced a Gate 3a report; only 195 a Gate 3c* — **was a file-vs-unit category error.** It is retained here, struck, because the error itself is instructive: **a count taken from filenames, compared across two populations with different filing conventions, produced a confident wrong number that read as a major finding.** That is FP-3 reproducing inside this run's own surface work, caught only because a second pass censused it. See W0-f §2.

---

## 2. Additions to the incumbent table

| # | Capability as observable behavior | Concern | Layer | V | Mechanism | Evidence |
|---|---|---|---|---|---|---|
| 6 | Each gate emits a durable per-check verdict with attached evidence | Structure / Introspection | DEFINITION (checks) over HARNESS (require-an-artifact) | **A** | validator subagent writes `reports/gate-*.md` | 719 gate reports; `bugfix-458` = a 12-row check table, each row with a command or a diff |
| 7 | Gate failure re-spawns the producer with the failure attached, bounded | Structure | HARNESS | **A** | "max 2 rework iterations per gate"; the re-spawn carries the report path | 83 retry/rework reports; `crt-022/gate-3b-retry-report.md` names the previously-failed check and re-verifies unchanged ones |
| 8 | A second opinion is produced by an agent holding no context from the producing session | Security / Introspection | HARNESS | **A** | fresh-context subagent, prompt deliberately stripped of framing | 146 security-reviewer reports; *"the fresh, disconnected context is the point"* |
| 11 | Secret leakage is detected before merge | Security | HARNESS | **A** | GitGuardian check | present on every PR in unimatrix and arch-research |
| **21** | **Deferred work is parked with a machine-checked re-entry condition** | Structure | HARNESS | **A — the strongest thing SDLC has that research lacks** | `xfail` marker + **mandatory** GH Issue; Gate 3c verifies every xfail has one | delivery Gate 3c integration-validation block |
| **24** | A definition's claimed invariants are verified against the platform that would enforce them | Security / Introspection | HARNESS | **C** | none | **`factory-git` asserts "merge commits disabled at repo level · auto-merge enabled"; the API reports `allow_merge_commit=true, allow_auto_merge=false`.** Same class as #179 |

**Item 24 is a new failure mode neither domain's register had named:** a workflow definition states an invariant about its enforcing plane, the plane is configured otherwise, and **nothing compares the two.** The definition is not merely unenforced — it is *wrong about the world* and confidently so.

---

## 3. The five-definition diff — the layer test, done empirically

Two research authors (this repo's `theme-scan` + `research-scope`; unimatrix's `uni-research-protocol`) × three SDLC protocols (`uni-delivery`, `uni-bugfix`, `uni-design`).

### Shared by all five — strongest HARNESS-LAYER evidence in the run

1. **A run identity that simultaneously names** the directory, the branch, the issue, the cycle topic, and every agent-id prefix. All five. **One primitive doing five jobs, invented independently by both authors.**
2. **A coordinator that never generates content**, spawning specialists that return to it. All five state it explicitly.
3. **Parallel spawn in one message** as an instruction. All five.
4. **Declared phase transitions** with a `phase-end` call at every boundary — 4 of 5 (`uni-research-protocol` forbids all Unimatrix writes and so has no cycle at all).
5. **A blocking human checkpoint at a named point, and a rule for when the human may *not* be asked.** All five.
6. **Bounded rework: ≤2, then escalate.** All five — SDLC "max 2 rework iterations", research-scope "REWORK ≤2 → SCOPE-FAIL", theme-scan "re-spawns for more range (≤2)". **Independent convergence on the same number.**
7. **The file is the deliverable; the agent's message is not.** `uni-research-protocol` states it three times; the garage learned the same thing the hard way as OBS-7.
8. **Retrieve prior art before generating.** All five.
9. **A scope guard** — out-of-boundary discoveries are recorded, never pursued.
10. **Deliberately context-starved reviewers.** `uni-synthesizer` (fresh window), `uni-security-reviewer` ("read the PR diff cold"), `uni-zero-reviewer` ("carries ONLY agent ID… the fresh, disconnected context is the point"), and the research side's one-lens hypothesizer isolation.

### Research-only (both research authors, absent from all three SDLC protocols)

- A **confidence-required field that changes which phases run** (`directional` skips feasibility).
- A **divergent phase followed by a convergent one** — **SDLC has no divergence anywhere**; its options are settled by one architect.
- A **prohibition on writing knowledge until after convergence**.

### SDLC-only (all three, absent from both research authors)

- A branch/PR terminal artifact; a **deterministic verifier *inside* a gate**; a **routing table mapping work to agent type by file path/language**; wave planning with dependency order; a documentation-trigger table; **irreversibility reasoning**; and a **gate that validates process compliance by reading GH issue comments**.

### Unique to one (DEFINITION-LAYER by construction)

theme-scan's three-tier formalize and fold-findings; research-scope's firewall phase; the bugfix protocol's "all phase outputs are GH Issue comments, never the filesystem"; the design protocol's vision-alignment agent.

### The single sharpest layer datum

> The **same** hook-client binary, the **same** eight hook events, and the **same** `context_cycle` phase API run under a research definition and an SDLC definition **today, in three repos**. Phase-conditioned observation and injection is demonstrably **HARNESS-LAYER**; the phase *vocabulary* (`spec/develop/test/pr-review` vs `scan/hypothesize/triage/formalize`) is demonstrably **DEFINITION-LAYER**.
>
> **That is not an inference — it is a configuration diff.**

---

## 4. What the verification layer actually checks — bears directly on A-8

From the sampled gate and reviewer reports, the checks partition cleanly, **and the partition is not domain-determined**:

- **Deterministic, no inference needed:** test pass counts · clippy exit · `grep` for `unsafe`/`todo!`/`unimplemented!` · smoke-suite result · file line counts · `git diff` proving a failure pre-exists · a zero-dependency audit · a CI convention script.
- **Model-judged, irreducibly:** "fix is minimal" · "the new tests would catch the original bug" · "root cause addressed" · blast-radius narrative · OWASP applicability · "code matches validated pseudocode".
- **Model-judged but mechanizable — the (P) reservoir, observed in the wild:** *"stewardship block present in the GH issue comment"* (a string check the validator performs by reading and judging) · *"xfail has a corresponding GH Issue"* (an API join) · *"no tests deleted"* (a diff query) · *"PR references the issue"*.

**A fourth verdict exists in practice that no protocol defines: `WARN`** — used in both sampled gate reports for non-blocking defects (a file over the line limit; a missing stewardship block that other evidence compensated for). **A binary PASS/FAIL gate vocabulary is already insufficient in the field, and the definitions have not caught up.**

---

## 5. Reachability and the unclaimed evidence

| Unresolved | Cheapest settling test |
|---|---|
| Is green CI a machine-enforced merge precondition? | One read of the branch-protection endpoint with an admin-scoped token. The 6-merged-red / 20-merged-early counts already make **"hard-enforced" unlikely** |
| Are `permissions`/sandbox absent by choice or by ceiling? | Inherits #179's ambiguity verbatim — **the already-queued hooks-and-permissions probe settles it for *both* domains at once** |
| **Gate verdict distribution across the 719 gate reports, and the 224→195 attrition gap** | Fetch and count. Code search is broken here, so it needs file fetches. **Real, cheap, and unclaimed** |
| `jurati`'s SDLC posture | It is **greenfield** — 1 PR, 11 issues, **no CI workflows**, no `product/features/`. The harness's own repo currently runs on the SDLC definition's *ambition*, not its record |

**Load-bearing caveat for triage:** the two operational failures found (no recorded human signature; documented git invariants contradicted by the platform's actual settings) are **operating facts of this owner's SDLC, not properties of SDLC.** Do not generalize them to the domain. What *does* generalize is the harness gap they reveal: **nothing checks that a definition's claimed invariants match what the enforcing plane is actually configured to do.**

**Volume flag (per the leader's instruction):** the protocol diff and incumbent characterization are complete and evidenced. The 231-unit corpus is characterized by **full filename census plus a 6-unit read sample** — enough for role/gate structure and the verification layer, **not** enough for failure analysis. The verdict distribution and the 224→195 gap were left unclaimed rather than faked.
