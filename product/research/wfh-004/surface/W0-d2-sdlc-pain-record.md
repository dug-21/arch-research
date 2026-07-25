# W0-d2 — The SDLC pain register (second domain)

**Run:** `wfh-004` · Issue #48 · phase `scan` (rebuild, per Amendment A-7) · `agent_id: wfh-004-w0d2` · read-only, zero graph writes.
**Corpus:** `dug-21/unimatrix` (610 issues, 359 PRs, 231 `product/features/` units, **63 numbered `bugfix-*`**, 25 releases, CI+release workflows) · `dug-21/jurati` (12 issues, 1 PR) · this repo's SDLC-shaped history · `uni-bugfix-protocol.md` (yardstick only) · Unimatrix graph (read-only) · industry reports.
**Evidence classes:** `[R]` recorded in a log/node/issue/PR we own · `[V]` verified live this session · `[I]` inferred · `[X]` external/secondary.

## 0. Sampling method, and what it cannot support

**Reachability: resolved.** Both repos public. The bulk of this register is `[R]`/`[V]`; industry evidence is confined to §4 and marked `[X]`.

**What was done.** (a) Full git tree of `product/features/` in one call — **8,206 paths, `truncated:false`**, so the *file-store* census is complete. (b) Every GH Issue comment header for all 63 numbered `bugfix-*` units — the *Issue-store* census is also complete. (c) Full bodies for those 63. (d) The bugfix protocol, for the declared role set. (e) ~15 issue bodies and one full comment thread (#944) read in depth, chosen **by failure-signal, not at random**. (f) 100 recent CI runs and 25 releases labelled.

**Selection bias, stated.** Deep-read units were chosen by searching for failure language. That is valid for *existence* claims and **invalid for rate claims**. Every rate below (S-02, S-03, S-16, S-24) comes from a **complete census over all 63 units**, not from the deep reads.

**Three hard limits.** (1) No access to the unimatrix project's *own* Unimatrix graph — its `lesson-learned` nodes are invisible. (2) `product/features/` is a curated store; work that left no directory is invisible by construction, so **all counts are floors**. (3) A regex-based clustering of failure *modes* over-matched badly (48/63 for "wrong number" is not credible) — **discarded rather than reported.** The mode clusters below are hand-assigned from read issues.

**A prior that frames everything:** **56 of the last 60 commits on `unimatrix` main carry a Claude co-author trailer (93%)** `[V]`. This is a genuinely agent-authored codebase, so its defect record *is* agentic-SDLC field evidence.

## 1. The SDLC pain register

Concern keys: 1 Structure · 2 Context · 3 Security · 4 Introspection · 5 Cost · 6 Self-improvement · 7 Recovery · 8 Steering. Layer per A-6: **H**arness / **D**efinition / **A**mbiguous.

| ID | What happened | Con | Layer | Ability missing (observable) | Cost | Recur | Cls |
|---|---|---|---|---|---|---|---|
| S-01 | PR #175 **reverted** the agent architecture: 5 consolidated coordinators *"were skipping subagent spawns (synthesizer) and generating content themselves, producing wrong-format implementation briefs (col-018, col-019)"* | 1,8 | H | Nothing detected that a declared role's spawn never occurred; the coordinator's own prose was consumed as if the role had produced it | 2 features' briefs wrong-format; whole architecture reverted | 2 units | R |
| S-02 | **Census of 63 bugfix units, both stores:** no trace of the declared **security review** exists anywhere for #554, #881, #930; no trace of **gate validation** for #178, #358, #369, #930. #930 has neither and was closed *"Fixed and merged via #936 (squash)"* | 1,4 | H | A declared gate could be absent and the unit still merged; nothing at close compared roles-declared against roles-with-a-trace | 3/63 unreviewed-for-security merges, 4/63 ungated | **3–4 / 63** | **V** |
| S-03 | The protocol states outputs are GH Issue comments, *"never written to the filesystem"* — yet 64 unit directories hold agent reports. The two stores **disagree** on whether a role ran: gate **71%** agreement, security **78%**, design-review **79%**, **verify/test 44%** | 4,1 | H | No single surface answers "did this role run"; the answer requires unioning two stores that were never reconciled | 21 units have a verify *file* and no verify *comment*; 14 the reverse | standing | **V** |
| S-04 | #944: investigator v1 diagnosed the bug wrong; a **design reviewer approved it**; a **uni-zero product reviewer independently approved it**; the human corrected it. v2 also partly wrong (*"supersedes my v1 review"*); v3 finally correct | 8,4 | H | Two independent agent review layers ratified a wrong diagnosis; nothing but the human distinguished a confident wrong answer from a right one | 3 investigation cycles + 2 superseded design reviews on one bug | 1 (×3 iter) | R |
| S-05 | #944: `test_bare_mcp_cycle_tags_not_persisted` **asserted the defective behavior as intended**. *"So the suite is GREEN on the wrong behavior."* | 1,4 | A | The test suite recorded a defect as the specification; passing tests carried no information about correctness | Defect was gate-passing by construction | 1 | R |
| S-06 | #709: the fix for #122 shipped `setsid` **without `-w`**, so `rc=$?` captured the fork's status (always 0). Every failing suite and every timeout read PASS. *"This inverts the bug it was meant to fix"* — #122's entire point was gate-signal integrity | 4,1 | H | The instrument that decides pass/fail reported pass unconditionally, and nothing cross-checked the instrument | Unknown number of false-green gates between merge and detection | 1 | R |
| S-07 | #579: `audit_log` writes **silently stopped ~2026-03-18**; discovered **2026-04-23** (~5 weeks). Fire-and-forget INSERT, failure swallowed: *"no log line, no panic, no visible error to the caller"* | 4,7 | H | A durable record stopped being written and nothing observed the absence; the system reported healthy throughout | ~5 weeks of unattributable writes | 1 | R |
| S-08 | #276: the background maintenance tick is `tokio::spawn` fire-and-forget with no supervisor. One panic stops **all** maintenance forever while the server keeps serving MCP: *"no observable indication to the user or operator"* | 7,4 | H | A worker died and nothing detected it; liveness of the *unit* was invisible while liveness of the *process* looked fine | Permanent silent staleness | 1 | R |
| S-09 | #122: **26 zombie `cargo test --workspace` processes** from ≥6 subagent sessions, 04:13–16:10, holding cargo/DB locks. *"Recurring across the last 2–3 feature releases."* Workspace tests hung until killed by hand | 7,1,3 | H | Work spawned by a finished agent outlived it, and nothing reaped or attributed it | Workspace testing blocked repeatedly | ≥3 releases | R |
| S-10 | #259: crt-019 ran the standard parallel-worktree wave over 7 components with cascading signature changes. **The brief explicitly said "single atomic feature cycle" with a 17-step ordered sequence — *"the parallel worktree pattern overrode this guidance."*** → 4+ diverging forks, complex merge, **126 compile cycles**, 4 orphaned worktrees with uncommitted changes | 1,8,7 | H | A written execution constraint was overridden by the default spawn pattern and nothing refused it; agents each re-implemented a shared foundation with no view of the others' | One feature's implementation largely wasted | 1 | R |
| S-11 | #46: spawned agents auto-enroll `Restricted` and are blocked from writes. **The shipped workaround was a PreToolUse hook overriding `agent_id` to `"human"` on all Unimatrix calls** — *"Loses per-agent audit trail"* | 3,4,1 | H | A role could not act under its own identity, so identity was discarded to unblock it; the audit trail was traded for throughput deliberately, and no record of the trade travels with the writes | **The recorded cause of research pain P-06** | standing | R |
| S-12 | The 500-line module rule was *"honored only in waivers… waived on every feature"* (#693). `tools.rs` reached **6,008 code lines** — 12× the original cap. Seven refactor issues (#963–#969) filed in one day | 1 | A | A declared standard was exceeded on essentially every unit for months and nothing measured the breach at the moment of the change | 7 files over cap, 1.5×–6.0× | ~every feature | R |
| S-13 | #902/#892: `cargo install unimatrix-server` **failed to compile** without `--locked` — a *published* release users could not install. Gates passed because `cargo build/test` uses `Cargo.lock` and `cargo install` does not | 1,7 | H | The gate exercised a different resolution path than the shipped artifact, and nothing compared the two | A shipped release non-installable by default | 2 | R |
| S-14 | **Version numbers burned by failed releases:** v0.8.3 and v0.8.8 absent from the release list; the Release workflow failed 2026-06-20 and **4× consecutively 2026-06-27**; #847 records "blocks v0.8.8". #821: `package-npm` is not idempotent — re-running on an already-published version fails permanently | 7,1 | H | A partially-completed publish left irreversible external state, and the run could not be resumed — only restarted under a new version | 2 versions permanently unusable; 5+ failed release runs | 5+ | **V**+R |
| S-15 | #776: remote `init` wrote a **live cloud bearer token in cleartext** to `.claude/settings.local.json`, verified *not* gitignored — *"a single `git add -A` commits a live credential into history"* | 3 | H | A credential was written to a path with no check that the path was excluded from an irreversible publication channel | Near-miss; no leak recorded | 1 | R |
| S-16 | **33 of 63 bugfix issues (52%) name a prior internal feature unit as the defect's origin.** `infra-001` ×6, `ass-020` ×4, `nxs-011` ×3, `crt-040/041/043` ×2 each. **Four are bugfix-caused bugfixes:** 471→528, 476→528, 515→519, 650→652 | 6,4 | H | Over half of recorded defects came from our own prior delivered work, and nothing links a unit to the defects it later caused | 33/63 units of rework | **33/63** | **V** |
| S-17 | #528 opens: *"Follow-up identified during security review of bugfix-471."* bugfix-471's own gate had already passed; the same denylist-vs-allowlist error survived at a second call site | 1,6 | H | A gate passed a fix that left its own defect class un-swept; nothing checked whether the fix's *pattern* recurred elsewhere | A second bugfix cycle | 1 | R |
| S-18 | #652: the server's content limit was lowered **50,000 → 8,000 bytes** *"at some point"*; the integration test's docstring still said 50,000. No record of when or by whom | 4,2 | H | A contract changed with no record tying the change to a unit of work; the authoritative value and the documented value diverged undetected | Test failed months later; provenance unrecoverable | 1 | R |
| S-19 | #500: MRR fell 0.2875→0.2732 after crt-044 merged. In the same measurement, *"1,443 of 1,585 scenarios returned results — **142 dropped silently**"* | 4,6 | H | A quality metric moved after a merge and the run could not attribute the move; the measurement itself silently discarded 9% of its input | Regression un-attributable across 5 candidate causes | 1 | R |
| S-20 | Tests adjusted to pass: #844 widened the parity corpus 5→~25 and **#864 records the boundary-precision sensitivity *lost* by that widening**; #845 removed the D6 isolation dimension from the parity matrix; #434 lowered `supports_edge_threshold` 0.7→0.6 *"to unblock graph inference"* | 1,6 | A | A failing check was made to pass by changing the check, and the sensitivity given up was recorded only afterward, in a separate issue | Detection capability traded away | 3 | R |
| S-21 | **Attribution is the single most defect-prone subsystem in the project**: #11, #28, #59, #162, #198, #208, #300, #469, #560, #579, #582, #584, #587, #602, #633, #678, #694, #699, #700, #703, #832, #925 — **20+ issues across the full history**. #208 (2026-03-11) is *"Session topic attribution misses feature work done via subagents"* | 4,1 | H | Which unit of work a record belongs to could not be reliably established, across 5 months and ~20 attempts | **#208 is P-05's exact root cause, filed in SDLC four months earlier** | 20+ | R |
| S-22 | #830 / OBS-3: the MCP client connection goes stale silently and needs a manual `/mcp`. Also #178/#111: the 60-writes/3600s rate limiter blocks volume tests | 7 | H | A tool connection failed mid-run and nothing re-established it; a batch hit a ceiling and stopped partway | Identical to P-22 and P-24 | ~4+ | R |
| S-23 | #131: `detect_project_root` fails in git worktrees (`.git` is a file, not a directory) — the agent-parallelism mechanism broke project identity detection | 1,4 | H | The isolation mechanism used to parallelize agents invalidated the identity scheme used to attribute their work | Worktree runs mis-identified | 1 | R |
| S-24 | **Retro conformance: 1 of 63 bugfix units (#633) carries a retrospective comment** | 6 | A | A run closed with its lesson-extraction step leaving no trace, at n=62/63 | Analogue of P-19 at 63× the sample | **62/63** | **V** |
| S-25 | Cost: **no issue, PR, or unit in the 610-issue corpus records a token-spend, budget, or cost-attribution failure** — verified by keyword sweep | 5 | — | *(nothing observed — see §5)* | — | 0 | **V** |
| S-26 | This repo (`arch-research`) has **no `.github/workflows` at all** — `.github/` contains only `ISSUE_TEMPLATE/` | 4,7 | D | The research domain has no automated run-level check of any kind | Context | standing | **V** |

## 2. The cross-domain map — the run's most valuable output

**Same failure mode in both domains → strongest harness-layer evidence. 14 of 30.**

| Research P | SDLC analogue | Verdict |
|---|---|---|
| **P-05** telemetry reported 0 vs 38 writes | **S-21 / #208** *"Session topic attribution misses feature work done via subagents"*, filed **2026-03-11** | **SAME — and SDLC hit it first.** Not analogy: the same root cause, same product, **four months earlier** |
| **P-06** `created_by: anonymous` | **S-11 / #46** — the `agent_id → "human"` override *is* the mechanism producing P-06 | **SAME, causally identical.** The strongest single row in this table |
| **P-09** role instantiated without its contract's tools | **S-11 / #46** — spawned agents lack Write despite the contract requiring it | **SAME** |
| **P-10** background specialist died silently, 0 bytes | **S-08 / #276** — unsupervised tick dies, server looks healthy; **#158** server dies silently | **SAME.** SDLC infrastructure does *not* prevent it |
| **P-13** a declared role never ran | **S-01 / #175** + **S-02** (3–4 units with no gate/security trace) | **SAME — and SDLC lets us count it.** Research had n=1 and no case definition; here it is 3–4/63 mechanically |
| **P-12** gate authorized 17 nodes, 33 written | **S-12** — the 500-line rule breached on ~every feature, to 12× | **SAME shape**, far larger multiple |
| **P-19** retro deferred, never performed | **S-24** — 62/63 bugfix units carry no retro trace | **SAME, and worse in SDLC.** Research: 4 occurrences. SDLC: 62/63 |
| **P-16** cost undercount by 61× | **S-06 / #709** — the pass/fail instrument returned PASS unconditionally | **SAME class** (the instrument lied), different quantity |
| **P-14** a document contradicting itself, consumed by the next role | **S-04 / #944** — v1 diagnosis wrong, ratified by two reviewers, consumed downstream | **SAME.** SDLC review did *not* prevent it |
| **P-22** MCP connection stale, manual `/mcp` | **S-22 / #830** | **SAME — literally the same defect** |
| **P-24** `context_tag` 60/hr limit stopped a batch partway | **S-22 / #178, #111** | **SAME** |
| **P-25** `context_correct` silently skipped edges | **#879, #744** — compaction deletes past-ceiling inbound edges; `REDIRECT_CEILING=50` *"silently orphans referrers 51+"* | **SAME** |
| **P-27 / P-28** context omitted the need-set / the substrate | **S-18 / #652** and **#944 v1** (traced the retired Rust oracle instead of the deployed JS client) | **SAME.** #944 is P-28 exactly: the substrate was omitted and the agent could not see the omission |
| **P-03** a declared out-of-scope boundary crossed | **S-10 / #259** — the brief said sequential-atomic; the parallel pattern overrode it | **SAME** |

**Prevented or materially reduced by SDLC infrastructure. 5 of 30.**

| Research P | Why SDLC covers it |
|---|---|
| **P-07** run completed with no Issue and no cycle stamp | Prevented **only for merges** — a merge requires a PR. **Not** prevented for role artifacts: S-02 shows a merge with no gate trace |
| **P-08** two live Issues for one run-id | Reduced: branch/PR unique by construction; **zero** duplicate-unit incidents in 359 PRs `[V]` |
| **P-11** file-store items invisible to search | Reduced: git + GH index everything committed. **But S-03 shows the split-store problem reappears** as store-vs-store disagreement rather than invisibility |
| **P-21** 14.8% of tool calls after completion | Prevented at the unit boundary: a merged PR closes the unit. No analogue found `[V]` |
| **P-26** runs open a month, blocked vs abandoned indistinguishable | Partially: an open PR against a moving main becomes visibly conflicted. But **105/610 issues are open, some since February** `[V]` — only the *PR* is self-alarming |

## 3. SDLC-only failure modes

1. **Irreversible external publication.** S-13/S-14: a version number is consumed and a failed publish cannot be retried under the same number. **The axis the charter predicted, and it is real: 2 burned versions, 5+ failed release runs.**
2. **Credential exposure through an irreversible channel** (S-15) — git history. Research has no one-way door for a secret.
3. **Concurrent agents colliding on shared machine state** (S-09) — 26 orphaned processes across 6 sessions holding locks.
4. **Cascading-dependency parallelism** (S-10) — parallel research lenses are *designed* independent; parallel code components frequently are not, **and the harness cannot tell which case it is in.**
5. **The isolation mechanism breaking the identity mechanism** (S-23).
6. **Defects compounding into later defects** (S-16) — a wrong research finding degrades a later run's *inputs*; a wrong merge degrades the *substrate every later run executes on*.
7. **The test suite as an active carrier of a defect** (S-05/S-20) — research has no artifact that can *assert* a wrong answer is correct and thereby gate on it.

## 4. Research-only failure modes

**Genuinely absent from the SDLC corpus:** P-21 (merge is a hard terminator) `[V]` · P-08 (branch/PR uniqueness) `[V]` · P-02 (no analogue found, though the SDLC side may simply not detect it either).

**P-20 (session discontinuity — research's most recurrent pain, 4/4 runs): partially dissolved, and only weakly evidenced.** Git does hold the state, and **no** SDLC issue about re-deriving lost context was found `[V]`. But that is absence-of-record, and **the SDLC side has no measurement instrument for it either** — the research figures came from an auto-measured retro the SDLC side runs 1/63 times (S-24). What can be said: the artifacts a resuming agent needs (diff, branch, PR thread, failing test) are durable and addressable, whereas the research equivalents live in prose a resumer must re-read. **Directional, not demonstrated: git converts continuity from a memory problem into a lookup problem. It does not eliminate re-derivation — #944's three investigation rounds are re-derivation of exactly this kind.**

**P-15 / P-17 / P-30 (cost)** — no SDLC analogue, because **nobody in the SDLC corpus is trying to meter spend at all** (S-25).

**P-04 (zero permission rules / hooks) — inverted, and this is the sobering one.** The SDLC repo *does* configure enforcement (a PreToolUse hook exists, per #46) and *does* run CI. Per SCOPE §11 this makes the SDLC side the better evidence base for "what enforcement buys you" — and the answer is: **with hooks, CI, PR review, a security reviewer and a gate validator all configured, S-02 / S-04 / S-06 / S-13 still happened.**

**External `[X]`, subordinate and carrying no register row:** Cortex 2026 (PRs/author +20%, incidents/PR +23.5%, change-failure +~30%); DORA (7.2% lower delivery stability under heavy AI reliance); Faros (+98% PRs, +154% size, +91% review time); assertion-weakening as a documented agentic test-repair pattern (corroborates S-20); slopsquatting. **No in-house instance of a hallucinated dependency was found.**

## 5. Per-concern demand summary — all 8, including honest empties

| # | Concern | Assessment |
|---|---|---|
| 1 | **Structure** | Heavy, from independent evidence. **S-02/S-03 are the sharpest rows in the register** because they are complete censuses: the question *"did the declared role run on this unit?"* is unanswerable from either store alone, in a mature protocol with 63 executions |
| 2 | **Context provisioning** | Small count, high consequence — as in research. #944 v1 is P-28 verbatim: the agent read the retired parity oracle instead of the deployed client, could not see the omission, and the human supplied the correction |
| 3 | **Security** | Better than research but the same hole. **Zero adversarial, malicious, or compromised-agent incidents in 610 issues** `[V]`. Every security row is our own agents crossing a boundary. **An attacker model has no field support in *either* domain** |
| 4 | **Introspection** | **S-21 is decisive**: attribution consumed 20+ issues over 5 months and is still open. S-06/S-19 reproduce research's "the instrument lied." **Two domains, independently, spent their largest effort on knowing which unit of work a record belongs to** |
| 5 | **Cost** | **EMPTY — zero incidents in 610 issues** `[V]`. The most striking asymmetry here, and it will not be dressed up: **this is absence of *record*, not absence of cost.** The research side has 5 cost pains only because one dedicated run built an instrument and looked. The SDLC side never looked. **Triage must read this cell as *unmeasured*, not *solved*** |
| 6 | **Self-improvement** | Strongest convergence after Introspection. S-24 is P-19 at 63× the sample and lands the same way: **the step dropped at close is always the one that would have improved the next run.** S-16 supplies what research could not — a measured **52% self-inflicted defect rate** — and nothing links a unit to the defects it later caused |
| 7 | **Recovery** | Confirms the research register's split: **detection** failures (S-08, #158) are a different shape from **resumption** failures (S-14). S-14 adds a shape research does not have: **resumption blocked by irreversible external state** |
| 8 | **Human steering** | Thin and lopsided in the same direction. **S-04 is the whole finding**: the human was the only party that caught a wrong diagnosis two agent reviewers had approved. The SDLC record, like the research record, contains almost nothing about mid-run steering failing — **because there is no mid-run steering to fail** |

**Is CI a run-level alarm?** It is one the research side lacks (S-26: zero workflows here), and it is real — 14/100 recent runs failed `[V]`. **But it alarms on the pipeline, never on the unit of work.** Every one of S-02, S-03, S-06, S-07, S-16, S-18, S-19, S-20, S-24 happened with CI green — and S-06 is the sharpest case: *the alarm itself returned PASS unconditionally and CI could not tell.*

> **The research register's sharpest finding survives the domain change intact — nothing observes the run as an object. SDLC adds one observer at the wrong altitude.**

**Does the human backstop scale better?** **No — the least comfortable finding here.** Code review is the SDLC equivalent, it is *more* formalized than anything on the research side (design reviewer + product reviewer + gate validator + security reviewer), and it still failed: two reviewers ratified #944 v1; the gate passed #709's inverted fix; bugfix-471's gate passed a defect its own security review found one unit later (S-17). **FP-4 holds unchanged across the domain boundary — in every contained incident read, the containing agent was the owner.** The failure is not throughput; it is that **adding review *layers* does not add independence when every layer is the same kind of reader.**

## 6. Evidence-quality report

| Class | Rows | Share |
|---|---|---|
| `[V]` verified live | S-02, S-03, S-14(part), S-16, S-24, S-25, S-26 | **7 of 26** — carrying the register's only complete censuses |
| `[R]` recorded in an issue/PR we own | S-01, S-04…S-13, S-15, S-17…S-23 | **19 of 26** |
| `[I]` inferred | 0 | — |
| `[X]` external | §4 only | **0 register rows** |

**Bottom line for triage.** The charter's fear — that in-house SDLC evidence would be thin — **did not materialize. 26 of 26 register rows are ours.** Five rows (S-02, S-03, S-16, S-24, S-25) are complete censuses over all 63 bugfix units, which makes them **better evidence than anything on the research side**, where every recurrence count is an explicitly-stated floor with no case definition. **Triage should weight the SDLC side at least equally, and should prefer S-02/S-03/S-16/S-24 over any single research pain for any claim about rates.**

**Three caveats that bound that.** (1) Both domains are one owner, one toolchain, one model family — cross-domain convergence here is evidence about *this operation's* failure modes, not a universal. **Two domains beats one; it is not many.** (2) All counts are floors — and S-03 proves the writing-down itself is unreliable. (3) The Cost cell is a true blind spot, not a clean bill.

**The single strongest thing this partition produces:**

> Research pains **P-05 and P-06 do not have SDLC analogues — they have SDLC *origins*.** #208 filed the subagent-attribution failure on **2026-03-11**, and #46 recorded the deliberate trade of per-agent audit for throughput. Both **predate the research-side observations of the same failures by months**, in a different domain, on the same substrate.
>
> **That is not two domains agreeing. That is one harness-layer defect surfacing twice.**

**Flags for the leader:** (1) S-25 — the Cost concern is an *unmeasured* empty on the SDLC side, not a solved one; it must be labelled that way in the briefing or generation will read it as low demand. (2) S-02/S-03 give the run a **mechanically re-runnable conformance measure**; the same census can be extended to all 231 units. (3) The `[X]` industry material is confined to §4 and carries no register row — **do not let it migrate into the candidate evidence column.**
