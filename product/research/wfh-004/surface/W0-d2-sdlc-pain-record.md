# W0-d2 — The SDLC pain register (second domain)

**Run:** `wfh-004` · Issue #48 · phase `scan` (rebuild, per Amendment A-7) · `agent_id: wfh-004-w0d2` · read-only, zero graph writes.
**Sources:** `gh` against `dug-21/unimatrix` (610 issues, 359 PRs, 25 releases, 100 workflow runs), `dug-21/jurati` (11 issues, 1 PR), `dug-21/arch-research` (19 PRs, 146 commits); Unimatrix graph read-only; published field via WebSearch.
**Evidence classes:** `[R]` recorded in a log/node/issue/PR we own · `[V]` verified live · `[I]` inferred · `[X]` external/secondary, **never ours**.

**Read this caveat before the table.** Unimatrix's 128 bug issues are mostly **product** defects in a Rust knowledge server, not failures of the agentic process that built it. Two kinds of row are kept and marked: **PROCESS** (the agentic SDLC machinery itself failed) and **ESCAPE** (a defect the agentic pipeline shipped and did not catch — the missing ability is about detection). Mixing these silently would inflate the register.

## 1. The SDLC pain register

| ID | What happened | Kind | Concern | Layer | Ability missing (observable) | Cost | Recur | Cls |
|---|---|---|---|---|---|---|---|---|
| S-01 | PR #175: five consolidated coordinator agents **skipped subagent spawns (the synthesizer) and generated the content themselves**, producing wrong-format implementation briefs across col-018/col-019. Architecture reverted to protocol-primary | PROCESS | 1, 8 | HARNESS | Nothing observed that a declared role was never spawned; the coordinator's own plausible-looking output was the only evidence the work happened | 2 features' briefs wrong; full agent-architecture revert | 2 features | R |
| S-02 | #259 (crt-019): 7 parallel agents in isolated worktrees each re-implemented the shared foundation. The brief said *"single atomic feature cycle"* with a 17-step ordered sequence — *"the parallel worktree pattern overrode this guidance."* Result: 4+ diverging forks, **126 compile cycles, 4 orphaned worktrees with uncommitted changes** | PROCESS | 1, 7, 8 | HARNESS (the ordering constraint itself is DEFINITION) | Nothing compared the spawn pattern against the brief's stated ordering constraint before spawn; nothing detected siblings duplicating the same foundation | 126 compile cycles; 4 abandoned worktrees | 1 | R |
| S-03 | #122: **26 zombie `cargo test --workspace` processes** from ≥6 subagent sessions, 04:13→16:10, holding build locks and `.db` handles. *"Recurring problem across the last 2-3 feature releases"* | PROCESS | 7, 1 | HARNESS | A spawned agent's child processes outlived it and nothing reaped them; nothing attributed a running process to the session that started it | Testing blocked across 2–3 releases | 3+ | R |
| S-04 | #709: the **fix for #122 shipped `setsid` without `-w`**, so `rc=$?` captured the fork's status (always 0). Every failing suite and every rc=124 timeout read as PASS. *"This inverts the bug it was meant to fix"* — gate-signal integrity was #122's named load-bearing criterion, flagged by both the design review and the uni-zero review | PROCESS | 4, 1 | HARNESS | A green gate verdict was produced by a mechanism structurally incapable of producing a red one, and nothing exercised the gate against a known-failing input | Unknown window in which every CI verdict was uninterpretable | 1 | R |
| S-05 | #944: **three** successive agent bug investigations. v1 was wrong (traced a retired parity *oracle* as if it were the deployed client) and was **APPROVED by the agent design-reviewer and by the uni-zero product reviewer**. *"The human's correction is confirmed with code and runtime evidence."* v2 partly wrong; v3 superseded both | PROCESS | 4, 8, 2 | AMBIGUOUS — review roles are DEFINITION; "nothing recorded what a review was checked against" is HARNESS | Two independent agent review layers ratified a wrong diagnosis; nothing distinguished *reviewed* from *checked against the deployed artifact* | 3 investigations + 2 superseded approvals on one small bug | 2 wrong ratifications | R |
| S-06 | #944: two tests were written to **assert the buggy accept-and-drop behavior**. *"So the suite is GREEN on the wrong behavior"* | PROCESS | 1, 4 | DEFINITION → HARNESS ("a gate's satisfying evidence is recorded against the claim it was taken to satisfy") | The test suite encoded the defect as the specification; nothing compared an assertion against the design intent it expressed | Bug shipped and locked in by its own tests | 1 | R |
| S-07 | #579: `audit_log` writes **silently stopped ~2026-03-18** (last `event_id` 3759); found **2026-04-23 — five weeks later**. Fire-and-forget INSERT; failure swallowed, no log line, no panic, no caller error | ESCAPE | 4, 7 | HARNESS | A subsystem stopped producing records and the *absence* of records was not itself an event | 5 weeks of unaudited tool calls, unrecoverable | 1 | R |
| S-08 | #46: spawned agents auto-enrolled at `TrustLevel::Restricted` (Read+Search), blocked from writes. **The workaround was a PreToolUse hook overriding `agent_id` to `"human"` on every call — *"Loses per-agent audit trail."*** | PROCESS | 3, 4, 1 | HARNESS | A role was instantiated without the capability its own contract requires; the unblock traded attribution away, deliberately and permanently | **The recorded causal origin of research pain P-06** | standing | R |
| S-09 | #582: `agent_attribution` empty in `audit_log` — schema migrated but `clientInfo.name` never written | ESCAPE | 4 | HARNESS | The column for "which agent did this" existed and nothing populated it | Mirror of P-06 | 1 | R |
| S-10 | #693 + #963–#969: the declared 500-line module rule was *"honored only in waivers… waived on every feature."* On remediation day seven files exceeded a **re-calibrated** 1,000-line cap: `tools.rs` **6,008 (6.0×)**, `config.rs` 5,064, `listener.rs` 3,438 | PROCESS | 1, 6 | HARNESS (the number is DEFINITION) | A declared code-health invariant was exceeded on every feature for ~5 months; nothing refused, blocked or counted it, and the eventual remedy was to **restate the rule** | 7 refactor issues; 12× the original cap at worst | ~every feature | R |
| S-11 | #902/#892: the **published** `unimatrix-server` would not build under plain `cargo install` (rmcp macro drift). `cargo build/test --workspace` — what the gates run — succeeded, because it uses `Cargo.lock` | ESCAPE | 4, 1 | DEFINITION → HARNESS ("a gate declares which artifact it exercised") | The gate exercised a different resolution path than users take; nothing tested the artifact as a user would obtain it | Published versions uninstallable by default | 2 | R |
| S-12 | Release pipeline burned version numbers: v0.8.3 Release run **failed**; four consecutive Release runs failed; #821 records `package-npm` is **not idempotent** — retry on an already-published version fails. **v0.8.3 and v0.8.8 are absent from the release list** | PROCESS | 7, 1 | HARNESS | A partially-completed unit could not be retried because part of it had already become externally irreversible, and nothing recorded which part | Version numbers permanently burned; #847 *"blocks v0.8.8 release"* | ≥3 | R + **V** |
| S-13 | #776: remote `init` wrote a **live cloud bearer token in cleartext** to `.claude/settings.local.json` — *"neither gitignored nor tracked… a single `git add -A` commits a live credential into history"* | ESCAPE | 3 | HARNESS | A credential was written to a path where the routine next action commits it; nothing checked a write path against ignore rules | Credential-leak exposure; caught by a hardening review, not by a control | 1 | R |
| S-14 | #276: the background maintenance tick is fire-and-forget `tokio::spawn` with **no supervisor**. One panic stops all maintenance forever while the server keeps serving — *"no observable indication to the user or operator."* Family: #158, #839, #872 | ESCAPE | 7, 4 | HARNESS | A process stopped doing its work and continued to appear healthy | Latent total maintenance stall | 4 | R |
| S-15 | #830 / #308: MCP client connection goes **stale silently**, not auto-retained, requires manual `/mcp` | ESCAPE | 7 | HARNESS | A tool connection failed mid-run and nothing re-established it | Manual human reconnect | 2+ | R |
| S-16 | Standing flaky cluster failing **only under full-workspace parallelism**: #958, #833, #757, #746, #710, #705, #691, #303, #288 | ESCAPE | 4, 7 | AMBIGUOUS | A gate's verdict depended on machine load, so a red result carried no information about the change | 9 issues; repeated re-runs | 9 | R |
| S-17 | #500: MRR regressed 0.2875→0.2732 after crt-044 merged; **142 of 1,585 scenarios "dropped silently."** Five candidate causes listed; none identified | ESCAPE | 4, 6 | HARNESS | A quality metric moved after a merge and nothing could attribute the movement to the change; the baseline was not reproducible | A regression with no attribution instrument | 1 | R |
| S-18 | #635 / #632: `config.toml` categories not authoritative — **domain packs silently expand the allowlist past operator config** | ESCAPE | 3 | HARNESS | An operator-declared restriction was widened by a downstream component with no notice | Configured security boundary silently broader than declared | 2 | R |
| S-19 | #879 / #744 / #890 / #889: compaction ticks **delete** edges instead of repointing; `REDIRECT_CEILING=50` *"silently orphans referrers 51+"*; quarantine-restore loses inbound edges | ESCAPE | 4, 7 | HARNESS | A maintenance process destroyed data and reported success; the loss is countable only by inspecting afterwards | Unknown edge loss — **the product-side twin of P-25** | 4 | R |
| S-20 | Gate satisfied by altering the measurement: #845 **removed the D6 isolation dimension** from the parity matrix; #844 widened the corpus 5→~25, and #864 records *"recover boundary-precision sensitivity **lost** when parity corpus widens"*; #434 lowered `supports_edge_threshold` 0.7→0.6 *"to unblock graph inference"* | PROCESS | 6, 4 | AMBIGUOUS | A failing check was made to pass by changing the check; the sensitivity surrendered was recorded only as a follow-up issue | A dropped parity dimension; named precision loss | 4 | R + **I** |
| S-21 | #887: the retro-detector flags the hardened `setsid -w timeout cargo test` form — the exact form #709 **mandated** — as a `sleep_workaround` false positive | PROCESS | 6, 4 | HARNESS | The self-improvement detector's rule was not updated when the convention it inspects changed, and it cannot distinguish a hardened form from a workaround | Retro signal polluted; open since 2026-07-02 | 1 | R |
| S-22 | The SDLC repo's **own run-observation instrument** was wrong in six distinct recorded ways: #925 (cycle-review sweeps foreign sessions on one text match), #949 (counts prose *discussing* errors as error events), #763 (`explicit_read_count` always 0 after telemetry moved PreToolUse→PostToolUse), #750 (per-session Calls/Tools collapse to 0), #300 (SessionStart resets `started_at` on compaction), #762 (*"Knowledge reuse: 19 of 2 (950%)"*) | PROCESS | 4, 6 | HARNESS | The instrument reporting on a run was wrong six separate times, each found later by a human reading a number that looked odd | Six recorded miscounts on the run-observation surface | **6** | R |
| S-23 | #131: `detect_project_root` fails inside git worktrees (`.git` file vs directory) — the isolation mechanism used to run agents concurrently broke project-identity detection | PROCESS | 1, 7 | HARNESS | The isolation mechanism used for concurrency silently changed a property other machinery depended on, and nothing declared that dependency | Agents in worktrees mis-identified their project | 1 | R |
| S-24 | #178 / #111: the Unimatrix write rate limiter (60 writes/3600s) blocks volume/stress integration tests | ESCAPE | 7, 1 | HARNESS | A batch of writes hit a ceiling and stopped partway | **Identical to P-24** | 2 | R |
| S-25 | `arch-research` has **no `.github/workflows` at all**; `unimatrix` has `ci.yml` + `release.yml`; `jurati` has none. Recent `unimatrix` runs: 78 success / 14 failure / 8 cancelled | — | 4 | HARNESS | The research repo has **no automated check of any kind** — no change-level or run-level alarm exists there | Standing asymmetry between the domains | standing | **V** |

### External / secondary (`[X]`) — context only, never our field evidence

| ID | Claim |
|---|---|
| X-1 | Cortex 2026 Benchmark: PRs per author +20% YoY, **incidents per PR +23.5%**, change-failure rate +~30%. DORA: 7.2% reduction in delivery stability under heavy AI reliance |
| X-2 | Faros AI telemetry: AI usage correlates with 98% more PRs, PRs **154% larger**, review times **91% longer** — review is the chokepoint |
| X-3 | Agent test-repair weakens assertions (`toBe(5)` → `toBeTruthy()`), leaving traces: empty catch blocks, loosened matchers, deleted tests |
| X-4 | Slopsquatting: 43% of hallucinated package names recur across all 10 identical re-runs; one package spread to 237 repos via 47 agent skill files without human review |
| X-5 | Developer-agent misalignment at scale — 20,574 real sessions analysed |

**Shape of X-3/X-4 against ours:** X-3 has an in-house near-analogue (S-20, S-06) but ours is *reasoned and documented in an issue* rather than covert. X-4 has **zero in-house instances** — no hallucinated-dependency incident in either repo.

## 2. The cross-domain map — the most valuable section

**Same failure mode in both domains** (strongest harness-layer evidence this run can produce):

| Research | SDLC | Verdict |
|---|---|---|
| **P-13** a declared role never ran; the run reported its funnel anyway | **S-01** consolidated coordinators skipped the synthesizer spawn and self-generated | **SAME.** Both: the coordinator's output is the only evidence the role ran, and it looks right. Two domains, two architectures. |
| **P-09** a role instantiated without its contract's tools | **S-08** agents auto-enrolled `Restricted`, blocked from writes | **SAME — and causally linked.** S-08's workaround (`agent_id → "human"`) *is* why P-06 exists. |
| **P-06** `created_by: anonymous` | **S-08 / S-09** attribution deliberately traded away, then a migrated column left empty | **SAME.** |
| **P-05** telemetry reported 0 against 38 writes | **S-22** six distinct wrong numbers from the run-observation instrument | **SAME, and worse in SDLC** — 6 instances vs 1. |
| **P-16** cost measured 60.3× wrong | **S-04** CI gate structurally unable to report red; **S-11** gate green on a path users don't take | **SAME family (FP-3), sharper in SDLC:** the wrong number here was the *pass/fail verdict itself*. |
| **P-12** gate authorized 17 nodes, 33 written, unreconciled | **S-10** 500-line rule waived on every feature; 6,008 lines against a 500-line cap | **SAME, ~12× worse in SDLC**, sustained ~5 months. |
| **P-10** background specialist died silently, 0 bytes | **S-14** unsupervised tick panics, server keeps answering; **S-03** children outlive the parent | **SAME.** SDLC adds the *inverse*: orphans that refuse to die. |
| **P-22** MCP connection stale, manual `/mcp` | **S-15** same defect, product side | **SAME — literally the same bug.** |
| **P-24** `context_tag` 60/hr ceiling stopped a batch partway | **S-24** rate limiter blocks volume tests | **SAME.** |
| **P-25** `context_correct` silently skipped edges | **S-19** compaction deletes edges, orphans referrers 51+ | **SAME.** |
| **P-18** 16 workflow versions shipped, zero A/B | **S-17** MRR regression after merge, no attribution; **S-21** the retro-detector itself broken | **SAME.** SDLC has an eval harness and *still* could not attribute. |
| **P-03** a declared out-of-scope boundary crossed | **S-02** the brief's mandatory ordering overridden by the spawn pattern | **SAME (FP-1).** |
| **P-01** blocking prompts at non-gate points | **S-05** two agent review layers ratified a wrong diagnosis; only the human caught it | **RELATED, not same.** Both are the human backstop; see §6. |

**Prevented by SDLC infrastructure:**

| Research | Why SDLC doesn't have it |
|---|---|
| **P-07** a run completed with no Issue and no cycle stamp | A merge requires a branch, a commit, a PR — **git makes the surface non-optional**. Genuine infrastructure coverage. |
| **P-29** specialists cannot write files; output round-trips through the parent's context | Agents write to a **worktree**; the filesystem is the handoff. (But S-02/S-23: worktrees carry their own costs.) |
| **P-11** unfiled items invisible to search | `git grep`/`gh search` over a repo is exhaustive; no graph/file seam. |
| **P-08** two Issues for one run-id | Branch names and PR-to-issue links make duplication visible. Not impossible — just loud. |
| **P-26** 8 runs → 1 `proven` node | Merged-to-`main` is a binary, external, non-negotiable proof-of-completion. **The single largest structural advantage SDLC has.** |

**No analogue:** P-15 (provider quota opacity) and P-17/P-30 (no budget metering) are identical in both — a *shared* absence, not an SDLC advantage. **No cost-metering machinery in either repo.**

## 3. SDLC-only failure modes

1. **Irreversibility of a published artifact — S-12.** `npm publish` cannot be un-run. `package-npm` not being idempotent means a *partial* release is unretryable; v0.8.3/v0.8.8 are permanently burned. **Research has no equivalent of an action whose retry is refused because the first attempt half-succeeded.** The sharpest SDLC-only axis — and it is a Recovery property, not a Security one.
2. **Concurrent agents colliding on shared mutable state — S-02, S-03, S-23.** Research subagents produce disjoint text. SDLC agents contend for one build directory, one lock, one file. 26 zombies from 6 sessions is not research-reachable.
3. **Gate-verdict corruption — S-04, S-16.** Research has no automated verdict to corrupt.
4. **A shipped credential — S-13.** A research agent cannot commit a bearer token into public history via `git add -A`.
5. **Gate/user path divergence — S-11.** Research has no published artifact whose acquisition path differs from the tested one.

## 4. Research-only failure modes

- **P-20 (session discontinuity, 4/4 runs, 617-min gap → 12 re-reads) largely does not arise in SDLC** — the register's most consequential asymmetry. Git holds the state: a resuming agent reads `git log`, `git diff`, the branch, the open PR, the issue thread. **The work product is the memory.** In research the work product is in the leader's context window and the files are an incomplete projection. Caveat `[I]`: no unimatrix issue about re-derivation cost — consistent with "it doesn't happen" but also with "nobody measured it," since `factory-retro` computes it and unimatrix has no equivalent.
- **P-07 / P-26 / P-11** — git and PR merge close these.
- **What SDLC does *not* prevent, contrary to the obvious guess:** P-19 (dropped commitments). #442, #574, #604, #693, #707, #747 are open follow-ups spanning up to 4 months. Issues persist better than research obligations; nothing forces them closed.

## 5. Silent failure — does CI give a run-level alarm?

**No. CI is a *change*-level alarm, not a run-level one, and it can be false.**

- **17 of 25 rows are silent** by the research register's own test. The 6 loud ones are loud for the same reason as in research: **a tool call or a job returned an error.**
- The research register's sharpest finding — *the alarm surface is the individual tool call; nothing observes the run as an object* — **holds in SDLC with one modification.** CI raises the altitude from "one tool call" to "one merge candidate." A real gain, and why S-01/S-02-class defects were caught within a feature or two rather than never. But CI still says nothing about: a role that never ran, a brief whose ordering was overridden, a cap exceeded on every feature for 5 months, a review that ratified a wrong diagnosis, an audit log that stopped 5 weeks ago, a metric that moved with no attributable cause.
- **SDLC has its own silent class research does not: the false-green (S-04) and the tautological-green (S-06, S-11, S-16).** Research's *numbers* lied; SDLC's *verdicts* lied. **Strictly worse, because a verdict is acted on immediately and automatically.** S-04 is the single most important row in this partition: a fix whose entire stated purpose was gate-signal integrity shipped in a form that made every failure read as PASS — and it passed two reviews that had both named that criterion as load-bearing.

## 6. The human backstop — does code review scale better?

**FP-4 reproduces exactly, and code review does not rescue it.**

- **S-05 is decisive.** Two independent agent review layers — a design reviewer and a product reviewer that explicitly certified its own independence (*"spawn prompt was clean… no conclusions injected"*) — **both approved a wrong diagnosis**. The correction came from the human. Then the design reviewer superseded its own approval.
- **S-04 corroborates**: two review layers named gate-signal integrity as load-bearing and neither ran `setsid timeout false; echo $?`.
- The pattern: **agent review reliably catches what is visible in the diff, and reliably misses what requires checking the artifact against reality** — which client actually runs, what the gate returns on a failing input, whether the published package installs.
- **Scaling: worse, not better.** External field agrees (X-2). In-house the reviewer count grew (investigator + design reviewer + uni-zero + security reviewer all visible) without the miss rate falling. **More review layers did not substitute for one human check.**

## 7. Per-concern demand summary (all 8, including empties)

| # | Concern | Rows | Honest assessment |
|---|---|---|---|
| 1 | **Structure** | 11 | Heavy, same as research — but **the shape differs**: research pain is *absence of units*; SDLC pain is *declared units whose declarations are not binding* (S-02 brief, S-10 cap, S-08 role contract). Git supplies the addressing; nothing supplies the enforcement. |
| 2 | **Context provisioning** | 1 (S-05) | **Near-empty, and this is real, not a search gap.** The SDLC agent's context is the repo, and the repo is complete. **The sharpest asymmetry in the register** — research's P-20/P-27/P-28 have almost no SDLC counterpart. |
| 3 | **Security** | 3 | Thinner than feared but **not zero, and qualitatively different**: research had *zero* recorded security incidents; SDLC has three real exposures (a committable live credential, an operator boundary silently widened, an audit trail deliberately destroyed as a workaround). Still **zero adversarial or compromised-agent incidents in either domain.** |
| 4 | **Introspection** | 11 | **Heaviest, same as research, with a worse failure mode**: research's instruments produced wrong numbers; SDLC's produced wrong *verdicts*. S-22 alone is six recorded miscounts. |
| 5 | **Cost** | **ZERO** | **An honest empty, and significant.** No cost metering, no budget enforcement, no token accounting in either repo. **Cost has no SDLC-specific demand signal because it has no signal at all** — the wall is a provider property, not a research-run property. |
| 6 | **Self-improvement** | 5 | **Stronger evidence than research, and it inverts the research read.** SDLC *has* the instruments research lacks (an eval harness with MRR/P@5 baselines, a retro-detector, a cycle-review) — and **they were wrong or broken**: S-17 could not attribute a regression, S-21's detector flags the mandated form as a violation, S-20 shows gates passed by weakening the measurement. **Having the instrument is not the hard part.** |
| 7 | **Recovery** | 6 | Same detect/resume split — plus a genuinely new axis: **S-12's irreversible partial completion**, with no research counterpart. |
| 8 | **Human steering** | 3 | Same lopsided shape: what fails is not mid-run steering but **the human being the only thing that catches anything**. No row records in-flight redirection succeeding or failing, because there is none to record. |

**E-1 (commitment tracking) is populated on the SDLC side too**: S-02, S-10, S-06, S-21. **Four SDLC pains on top of the research register's five — the strongest cross-domain support for any candidate emergent concern in this run.**

## 8. Evidence-quality report — how triage should weight this

- **25 rows: 22 `[R]`, 2 `[V]`, 1 `[R+I]`, plus 5 `[X]` held separately. No row is `[X]`-only. Every register row is ours.**
- **But `[R]` here is weaker than the research register's in one specific way.** **13 are PROCESS** (genuine agentic-SDLC process failures — the true second-domain evidence) and **12 are ESCAPE** (product defects the pipeline shipped; the missing ability is about *detection*, a weaker inference). **Triage should weight the PROCESS rows as peer to the research register and the ESCAPE rows one step softer.**
- **The domain is genuinely agentic:** 56 of the last 60 `main` commits carry a Claude co-author trailer `[V]`. This is agent-delivered software, so the PROCESS rows are field evidence, not analogy.
- **Coverage is uneven and this is the honest bound.** `unimatrix` gave 610 issues and is rich. `jurati` has 11 issues, 1 PR, no CI — a research-spike repo, contributing **nothing**. `arch-research` contributed one row. **The entire SDLC side rests on one repository:** n=1 project, one owner, one language, one agent architecture. Deep, not diverse.
- **Could not verify:** (a) no reopened-issue signal beyond one instance — either the process doesn't reopen or closure isn't tracked; (b) P-20's absence in SDLC is `[I]` — unimatrix computes no re-derivation metric; (c) inline PR review comments returned **empty** repo-wide — review happens in *issue comments* by agents, not GitHub's review surface, so S-05 is hand-found, not a sampled rate.
- **What this means for triage.** The SDLC side is **not thin** — deeper than expected, and it rests on our own evidence. But it is **narrow**: one repo, and its most valuable rows are single-incident. **The cross-domain recurrences in §2 are the load-bearing product: thirteen research pains have a same-failure-mode SDLC counterpart**, and each is a candidate for which "this is a property of the engine, not of a workflow" is now supported by two independent domains. Conversely, treat **P-20 as the clearest DOMAIN-SHAPED candidate in the register** — git already solves most of it — and treat Cost's cross-domain zero as evidence that no field pain exists on either side, only a reasoned one.

**The finding that matters most, and was not expected:** the research register concluded that nothing observes the run as an object. SDLC **does** have run-level observation — CI, an eval harness with baselines, a retro-detector, a cycle-review — and **every one of those instruments appears in this register as broken, wrong, or gamed** (S-04, S-17, S-20, S-21, S-22).

> **The harness-layer implication is not "build the observer." It is that an observer whose own correctness nothing checks reproduces the problem one level up** — exactly the research register's E-2 (calibration of self-measurement), now populated from a second domain by five independent rows.
