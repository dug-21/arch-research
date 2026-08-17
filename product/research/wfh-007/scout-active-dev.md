# FINDINGS — scout S1 / active-development surface / DISCOVERY / the exemplars

**Run:** wfh-007 · `theme:workflow-harness` · Issue #64 · `wf-v0.24`
**Agent:** `wfh-007-s1-scout` · **Date of read:** 2026-08-17
**Method:** GitHub REST API (`gh api`) for enumeration, metadata, issue/PR state, branch-protection and ruleset queries, and base64 content reads of READMEs, ledgers and issue bodies. `WebSearch`/`WebFetch` for the Lamego trace until the session's web-search budget was exhausted (200/200) — see §5. **Nothing was cloned, installed, built, or executed. No statement below is `[demonstrated by us]`. Status moves: 0.**

**Headline, stated first because the run's framing rests on it:**

1. **The premise "neither built the governance layer" is false for ruvnet, on artifact.** As of 2026-08-16 he ships `autogenous` — a Rust crate set with a hash-pinned constitution outside the loop, monotone authority attenuation enforced in the type system, an AND-gate over a fitness vector, ed25519 witness chains, and promotion that consumes signed receipts from ≥2 pinned judges rather than caller-supplied booleans. That is the governance layer, by name, component for component.
2. **And the premise is nevertheless directionally right, for a different reason.** He does not *run* on it. His actual operating loop — the Dream Machine, nightly against ruflo and metaharness — enforces its central safety invariant ("never merge, never self-promote") **as a sentence in a compiled prompt**, on three repositories with **branch protection disabled and zero rulesets**. The governance layer is a product he sells; the fleet he operates has none of it.
3. **The second exemplar could not be located.** "Andre Lamego's basement stack, ~1B tokens/week at 99.999% local" did not survive contact. See §1.3 — this is the most important negative in the return, and I substituted a real, published, measurable second exemplar rather than leave the teardown at n=1.
4. **The strongest find on this surface is not an exemplar at all.** `NVIDIA/OpenShell` (8,232★, Apache-2.0, Rust, alpha, created 2026-02-24, pushed today) occupies the *kernel* slot of the framing directly — kernel-level isolation, declarative YAML policy over filesystem/network/process/**inference**, credentials brokered so they never touch the sandbox filesystem, "single-player mode" as the explicit starting posture, and SAP embedding it as the security layer for all its agents. It is not in the graph. **This is the window-closing evidence the surface question asks for.**

---

## 1. Operating-model teardown

### 1.1 ruvnet (Reuven Cohen) — `owner-injection`

**Standing dedup:** `ruflo` + `@claude-flow/security` is **known — #200** (`grade:claimed`, wfh-005, ASSEMBLE the subtree not the product). Everything below is *new material about the operator*, not a re-characterization of #200. The inert-control position **#196** and its second instance **#254** are load-bearing to what follows and are cited, not re-derived.

#### The machinery

**[demonstrated — with artifact]** The account is 204 public repos, 10,994 followers. `gh api users/ruvnet/events/public?per_page=100` returns **100 public events spanning 48 hours** — 25 on 2026-08-16, **75 on 2026-08-17** — across 8 repositories (`RuVector`, `RuView`, `autogenous`, `dream-machine`, `llm-stream-reformat`, `metaharness`, `midstream`, `ruflo`). Breakdown: 41 PushEvent, 18 IssuesEvent, 18 IssueCommentEvent, 12 PullRequestEvent, 9 CreateEvent. The public event feed cannot reach further back than two days because the rate of events exhausts it. **That is the throughput measurement, and it is a real one** — it does not depend on anyone's self-report.

**[demonstrated — with artifact]** The operating loop has a name and a published implementation: **the Dream Cycle**, generalized into `ruvnet/dream-machine` (12★, created 2026-08-13, MIT). Its README states it is "the generalization of two routines already running nightly against `ruvnet/ruflo` and `ruvnet/metaharness`. Both are ~800-line prompts running the same 26-step pipeline; they differ only in a small, well-defined per-repo delta."

The pipeline, quoted:

```
ledger → research → frozen hypothesis → concrete candidate → baseline
  → evaluation → adversarial critique → bounded Darwin evolution
  → flywheel evidence → witness → issue → draft PR → durable ledger row
```

**[demonstrated — with artifact]** It runs as a **Claude Code cloud routine on cron**. The ruflo ledger names the trigger by id: `trig_01HpEqAcEP7wzrxy3TzakrQ2`, "`.github`-external, runs 06:00 UTC daily". `dream-machine` runs `0 9 * * *` against itself. Observed issue-creation times on 2026-08-17 corroborate the staggering: ruflo 06:32Z, metaharness 08:30Z, dream-machine 09:22Z. There is a fallback path for people without a cloud agent: `.github/workflows/dream-nightly.yml`, running the research half from a plain CI runner against OpenRouter.

**[demonstrated — with artifact]** The routine is **compiled from committed config, not frozen as a prompt** — `npx dream-machine compile dream.config.json --out /tmp/tonight.md`, with the stated rationale "so the schedule can never drift from the repo." The scheduled prompt is a 3-step bootstrap that builds the engine, compiles tonight's instructions, and follows them. This is a real `/etc`-shaped move: the operating instruction is a versioned artifact in the repository, and the scheduler holds only a pointer to it.

#### The human ↔ fleet division of labour — and the number that matters

**[demonstrated — with artifact]** The ruflo ledger contains a one-time backfill, computed 2026-08-13 from `gh issue list`, that measures the operating model's own yield. Quoting it:

> the v1 routine (2026-05-25 through 2026-08-13) filed 80 nightly research issues with no durable follow-through signal — each night only checked whether it was repeating itself, never whether anyone had acted on what it proposed. Backfilled from the full issue history below: **4 shipped (5%), 1 rejected, 75 (94%) never touched**, some over 2.5 months stale.

I counted the table independently: **80 rows — 60 STALE, 15 OPEN, 4 MERGED, 1 CLOSED.** A live `search/issues` query today returns **83 `dream-cycle` issues on ruflo, 4 closed** — 4.8%, unchanged.

**This is the single most valuable operating-model datum in the return.** Eighty nights of autonomous, competent, evidence-backed research, and the human consumed five percent of it. The ledger names the mechanism of failure precisely, and it is not authority, not safety, not sandboxing: **the fleet's output rate exceeded the human's review rate by roughly twenty to one, and nothing in the system noticed for eleven weeks.**

**[demonstrated — with artifact]** The v2 response to that discovery is instructive: the ledger exists so "the v2 prompt uses this table to bias toward attempting a real Flywheel evaluation over another docs-only proposal **when the merge rate over the trailing 14 nights is 0**." The fix for *nobody is reading my proposals* was *propose fewer things and evaluate them harder* — a throughput-matching move, not a governance move.

**[demonstrated — with artifact]** The division of labour is visible in the PR list. Across `dream-machine`, `metaharness` and `ruflo`, every `dream(...)` PR from the last four nights is **draft and open**: dream-machine #9, #11, #15, #17; metaharness #200, #205, #207; ruflo #3034, #3044, #3049. Meanwhile the human's own PRs merge same-day — metaharness #189/#191/#193/#196/#197 and ruflo #3037/#3039/#3040/#3041 all merged within hours. **Two dream PRs did merge** (metaharness #188 on 08-14, dream-machine #7 on 08-13), so the rate is not zero, but the pattern holds: *the fleet writes, and the human mostly merges what the human wrote.*

**[demonstrated — with artifact]** The machine has begun detecting this itself. metaharness issue #206 (2026-08-17) contains, under "Learning Signals": "2/4 candidate PRs merged, 2 open-not-stale — **an early 'review latency' signal**, not yet a pattern."

#### Spend, and where it goes

**[demonstrated — with artifact]** Per-night evaluation spend is recorded in the ledger and it is negligible. metaharness 2026-08-13: "**live spend $0.00042**". 2026-08-14: "**no live spend**" (deterministic before/after repro). Issue #206 for 2026-08-17: "`LLM_EVAL=available` (`OPENROUTER_API_KEY` present) — **used only by research agents; the candidate itself is $0**."

**[inferred from reading]** The spend structure is therefore: research reads cost tokens; **evaluation costs nothing because it is deterministic** (real test suites, before/after repro, byte-identity checks). The expensive thing is the *reading*, not the *proving*.

**The gap, and it is a real one: the harness's own cost is not metered anywhere.** A 26-step pipeline running in a Claude Code cloud session against a monorepo with 2,254 tests consumes a substantial and entirely unrecorded amount. The ledger's `Effect` column meters the experiment. Nothing meters the operator. **[inferred from reading]** — I could not find a per-night session cost in any ledger, gist reference, or issue body I read.

**[asserted]** The published cost-performance claims are separate and are the *product's* claims, not the operator's: metaharness's Cost-Pareto leaderboard reports SWE-bench Verified results with Wilson 95% CIs and LiveCodeBench (n=100) lifting **44% → 62%** via cost-cascade. The README itself flags that "SWE-bench Verified cost is an **estimate** (per-instance cost not captured in predictions)" and that the "deepseek snapshot cutoff [is] unpinned." Honest caveats, author-reported, unverified by me.

#### What happens when a run fails at 3am

**[demonstrated — with artifact]** Every night terminates in exactly one of three verdicts — `ACCEPT`, `REJECT`, `INCONCLUSIVE` — "never a fourth, never silence." The README states the design intent plainly: "A rejected hypothesis with a clean measurement is a *successful* night. The system optimizes for shrinking tomorrow's search space, not for producing PRs." A night with no API key "still runs — it reports `LLM_EVAL=blocked`, an honest `INCONCLUSIVE`, rather than faking a result." A wasm/NAPI build failure is "a recorded degradation, not a stop."

**[demonstrated — with artifact]** REJECT is shipped, not discarded. ruflo #3034 — `dream(performance): HNSWIndex efSearch query-time default (**evaluated, REJECTED**)` — and #3027 — `dream(swarm): power-of-two-choices mesh load-balancing (**evaluated, REJECTED**)` — are open draft PRs whose title advertises their own negative result. That is an evidence-graded commit primitive working exactly as the framing describes one.

**[demonstrated — with artifact]** The falsification protocol inside one night, from issue #206: "Deterministic, not sampled. Before/after repro: source fix stashed (test kept) → the 4 new tests fail exactly as predicted (`evaluateVariant is not a function`); 5 pre-existing tests unaffected. Fix restored → package suite **632 passed, 14 skipped, 0 regressions**." Plus bounded diffs ("Well under 300 lines") and a scored gist ("**Prior Gist Score — 9/10**", losing a point for 1650 words against a 1500-word cap, with tonight's gist trimmed to 1477 to fix the recurring miss).

**This is a more disciplined proof protocol than most human teams run**, and it is worth saying so plainly before the criticism that follows.

#### Queueing, resumption, review — and the structural flaw in the durable memory

**[demonstrated — with artifact]** Queueing is a **rotation**: `DATE=2026-08-17 DEEP=darwin-evolution SCAN=weight-eft,learn SLOT=2 COMMIT=5453c8c9… BRANCH=main`. Resumption is the **ledger**, read at STEP 1 "before the agent touches `gh` at all — a fresh cloud checkout otherwise has zero memory of prior nights." Review is GitHub: a public gist, a labelled issue, a draft PR.

**[demonstrated — with artifact] The durable memory is gated behind the bottleneck it exists to measure.** The one-row-per-night ledger append travels *inside the draft PR*. Since draft PRs mostly don't merge, the ledger on `main` mostly doesn't advance. Observed: metaharness has **4 dream-cycle issues (08-14, 08-15, 08-16, 08-17) and 2 ledger rows (08-13, 08-14)**; dream-machine has **5 issues and 1 ledger row**. Seven of nine nights across the two repos left no durable trace on `main`.

**And the machine caught it, diagnosed it correctly, and was right** — issue #206, "Ledger Check":

> Ledger on `main` has only 2 rows (2026-08-13, 2026-08-14) despite 4 nights of prior runs. Verified this is **cosmetic, not a pipeline failure**: `git ls-remote --heads origin` shows `dream/2026-08-15-generator-genome` and `dream/2026-08-16-flywheel-promotion` both exist, and PR #200 / PR #205 are real, open, draft, non-stale … each with a full "(evaluated)" writeup and their own ledger-row commit sitting on their own unmerged branch.

I reached the same conclusion independently from the issue/ledger mismatch before reading that paragraph. I record it as *cosmetic-in-mechanism but load-bearing-in-effect*: the cross-night memory that STEP 1 depends on is only as fresh as the human's merge queue, which is running at 5%.

#### The finding that matters most, and it corroborates #196 from an independent codebase

**[demonstrated — with artifact]** `gh api repos/ruvnet/{dream-machine,ruflo,metaharness}/branches/main` returns `"protected": false` on all three. `gh api repos/ruvnet/{…}/rulesets` returns **empty on all three**. The Dream Machine's headline safety property — "**Evaluation is not promotion** — the machine never merges; a human does", restated in the scheduled prompt as "NEVER merge, NEVER self-promote" — **is enforced by instructing the model, and by nothing else.** The agent runs with a token that can merge, against a branch that will accept a merge, and is asked not to.

This is not a hypothetical concern; it is **#196 (the inert-control position) at its third independent site**, after ruflo's default-off enforcement (#200) and opencode's neutering product config (#254). And the pattern is now *self-evidencing* — three consecutive Dream Cycle nights each found an inert control in ruvnet's own code:

| Night | Repo | Issue | The finding, in its own words |
|---|---|---|---|
| 2026-08-15 | metaharness | #199 | `scorePublishReadiness` locked python/go out of `'ready'` |
| 2026-08-16 | metaharness | #204 | flywheel-promotion: `verifyReplayBundle` **didn't verify** the full diagnostic |
| 2026-08-16 | dream-machine | #14 | ledger-signals: `zeroMergeStreak` **permanently miscalibrated (never fires)** |
| 2026-08-17 | metaharness | #206 | darwin-evolution: **"ADR-249's cost seam was shipped but never wired" — "the seam was structurally unreachable"** |

The dream-machine one is the sharpest: **the signal built to detect the 5%-adoption problem was itself broken and never fired.** A control watching for a broken control, broken.

**Recording it as evidence, not as a verdict:** three codebases, three independent scans, one defect class. wfh-005's amendment already recommended the theme carry effectiveness-verification as a first-class concern. This run adds a fourth and fifth instance and — new — an instance where the *meta*-control failed. I do not rank concerns; the goal-owner does.

#### What ruvnet built that the framing says he didn't — `autogenous`

**[demonstrated — with artifact]** `ruvnet/autogenous`, created **2026-08-16**, 11★, MIT, Rust, badge `status: research prototype`. Sub-headline: "**Governed Evolutionary Software**". Self-described as "a governed operating system for software that can learn from production, redesign parts of itself, prove the redesign is better, deploy it safely, and reverse it when wrong … an **evolutionary control plane**."

Its stated structural guarantees, quoted, "in the types, not in policy docs":

- "**Authority never silently expands** — a mutation may request *less* authority than its parent's ceiling, never more (`agl-types`, enforced in `Mutation::admissible`)." — **monotone attenuation.**
- "**The constitution is outside the loop** — hash-pinned, externally governed; `MutationScope::Constitutional` is *never* auto-promotable." — **`/etc` that the runtime cannot rewrite.**
- "**Promotion is a hard AND-gate over a fitness vector** — `min`-semantics; exceptional quality can never compensate for a safety or governance miss."
- "**Irreversible mutations are inadmissible** — no rollback target, no admission." — **an irreversibility test, shipped.**
- "**Statistical triggers can't authorize irreversible actions** — a learned detector may quarantine or buffer, never terminate."
- "**Zero unsigned promotions.**"

And the crate `envelope` (ADR-394), which is the part that should be read twice:

> the promotion transition depends on **independently-verified, content-bound evidence, never caller-supplied booleans or strings.** `promote("")` is impossible; the verifier consumes **ed25519-signed evaluation receipts from ≥2 distinct pinned judges** measuring candidate-vs-parent on the same corpus.

**That is gate-input independence, stated in read-set terms, implemented, by someone who has never read this theme.** The crate `deployment` extends it to the reverse direction: "rollback is **executed and confirmed**, not merely decided," emitting a signed `RollbackReceipt` after confirming the active artifact hash and health. `witness` is an "append-only signed witness chain"; `lineage` an "append-only content-addressed provenance DAG" that retains poor performers rather than deleting them. `generator` "**never sees the evaluator's labels** (separation)."

**[asserted — author-reported, reproducible in principle, unverified by me]** Measured envelope, release build on a Ryzen host: stream observation **≈0.9 µs/chunk** with 1 armed antibody, **≈14 µs with 16** — "~350× inside the <5 ms p99 SLO"; replay of **100,000 labeled streams in ~7 ms**; canary decision **≈2 ns**; ed25519 sign **~39k frames/s**. Detectors are "serializable artifacts (a closed combinator algebra with enforced resource bounds — **no closures, no regex engine**)". 71 tests including an end-to-end acceptance lifecycle. Live run 2026-08-16: 114 signed frames across four frontier models in 14.5 s, 114/114 verified, **$0.048/run**.

**The honest reading of the two halves together:** ruvnet has built, in the last 48 hours, a technically serious governance layer that names and solves the exact failure mode his own operating loop exhibits — and his operating loop does not use it. The distance between `autogenous`'s `promote("")`-is-impossible and dream-machine's please-do-not-merge is the whole subject of this run.

---

### 1.2 `AnandChowdhary/continuous-claude` — substituted second exemplar · `external-scan`

Reached through the by-function sweep (§4.3), **not** the watchlist. 1,370★, MIT, **Shell**, created 2025-11-15, **last pushed 2026-07-13 — a month stale**, which is itself a signal. I include it because the run requires an operating-model teardown of ≥2 exemplars, the named second exemplar evaporated (§1.3), and this one is published, specific, and makes the *opposite* architectural choice from ruvnet at the single most important seam.

**Origin, in the author's words [asserted]:** "I was contractually obligated to write unit tests for a codebase with hundreds of thousands of lines of code and go from 0% to 80%+ coverage in the next few weeks."

**The machinery [demonstrated — with artifact, README + flags]:** a Bash conductor that repeatedly invokes Claude Code (or Codex CLI). Each iteration: run the agent on the prompt → open a PR → `gh pr checks` for CI and reviews → **merge on success, close and discard on failure**.

**The seam that matters.** ruvnet's machine *never merges*. This one *always merges* — and delegates the entire gate to the forge: "if your repo requires code owner approval or specific CI checks, **it will respect those constraints**." **This is the cheapest thing that reaches most of the governance layer: GitHub branch protection + required checks + CODEOWNERS.** No kernel, no capability vocabulary, no credential broker, no evidence store. The forge already had all of it.

And it names its own boundary precisely: "Self-hosted Git forges such as **Gitea are not supported** … because they use different pull request, check, and review APIs." **The gate is GitHub-shaped, and that is the lock-in.**

**Gate-input independence, shipped in a bash script [demonstrated — with artifact, CLI flags]:** `--review-provider` runs "reviewer passes" on a **different provider than the builder** (`claude` builds, `codex` reviews), with a default review prompt that "reviews the diff, runs available checks, simplifies changed code, and verifies the app." Two model families, one gate, independent inputs — the property wfh-005 told us to call *gate-input independence*, at 1,370 stars, in `bash`.

**Spend, and it is the only exemplar that meters itself [demonstrated — with artifact, CLI flags]:** `--max-cost` (USD ceiling), `--max-duration` (`2h`), `--max-runs` (`0` = infinite), `--max-calls-per-hour` (throttle, "sleeping until capacity is available"), and explicit `--codex-{input,output,cached-input}-cost-per-million` rates for estimating Codex budgets. One of `--max-runs`/`--max-cost`/`--max-duration` is **required**. **You cannot start this loop without declaring a bound.** That is a budget primitive ruvnet's stack does not have.

**Failure at 3am [demonstrated — with artifact]:** "When an iteration fails, it closes the PR and discards the work. This is wasteful, but with knowledge of test failures, the next attempt can try something different." Plus `--stall-threshold <n>` — "pause after this many consecutive failures and append diagnostics to the notes file for human intervention." A stall detector wired to a human handoff.

**Queueing and resumption [demonstrated — with artifact]:** `SHARED_TASK_NOTES.md`, a single shared markdown file as external memory, with an explicit anti-verbosity instruction — "think of it as a relay race where you're passing the baton" — plus `--knowledge-file CLAUDE.md` for durable project knowledge. Note that it does **not** hide behind an unmerged branch: the notes file is committed on the merge path, so unlike the Dream Machine's ledger, the memory advances at the same rate as the work.

**The failure-tolerance philosophy [asserted, quoted from Don Syme, GitHub Next]:** "The fault-tolerance of Agent in a Loop is really important. If things go wrong it just hits the resource limits and tries again. Or the user just throws the generated PR away … It's so much better than having a frustrated user trying to guide an agent that's gone down a wrong path." The author generalizes: each run is near-idempotent — "if GitHub Actions kills the process after six hours, you only lose some dirty files that the next agent will pick up anyway."

**Human touches per day:** write one prompt, set one bound, review PRs. That is the whole interface.

---

### 1.3 "Andre Lamego's basement stack" — **could not be located. Reported as a null.**

I ran six distinct search formulations before the session's web-search budget was exhausted (200/200 — the budget was consumed by this session, and the last three of my own queries returned before it closed):

1. `Andre Lamego basement 1 billion tokens per week local agents`
2. `"99.999% local" agents basement rig tokens per week`
3. `Lamego AI agents local inference homelab coding agents fleet`
4. `runs a billion tokens a week in his basement local LLM agent swarm 2026`
5. `"Lamego" claude code agents tokens week local X post`
6. `"André Lamego" OR "Andre Lamego" AI agents infrastructure interview 2026`

**Nothing matching the description exists in reachable public search.** No blog, no repo, no thread, no video, no measurement.

**What the name does resolve to [asserted — press/vendor sources, unverified by me]:** **André Lamego is SVP & Chief Product Officer of SAP BTP Fabric**, publicly associated with SAP's embedding of **NVIDIA OpenShell** — "an open source secure runtime for autonomous AI agents" — into the SAP Business AI Platform, with SAP engineers contributing "runtime hardening, policy modeling, enterprise identity integration, and auditing and governance." An enterprise agent-runtime executive. Approximately the antipode of a basement operator, and — pointedly — **a person whose actual work is the governance layer the run's premise says he lacks.**

**Verdict, stated the way the assignment requires:** the headline numbers **~1B tokens/week** and **99.999% local** are **`[asserted]`**, with an additional and worse problem — **I could not locate the assertion itself**, only the run's restatement of it. An unrecoverable source is a strictly weaker position than a weak source, and it is exactly the failure wfh-005 recorded against wfh-004's thirty unrecorded references. **Do not cite these numbers as evidence of anything, including as evidence that "people are operating at this scale."**

**What would move it:** a primary artifact — a named URL (post, repo, video, invoice), a provider dashboard export or OpenRouter/vLLM accounting log covering ≥7 consecutive days, a hardware manifest with measured tok/s, and a definition of what "99.999% local" is a percentage *of* (requests? tokens? wall-clock? dollars?). Absent that, the reframe should not lean on it.

**One nearby, real, and cite-able datapoint** so the scale question is not left empty: a 2026 SitePoint piece on local inference reports **~17,000 tok/s sustained** on a consumer rig (≈1.47B tokens/day) at a build cost of **$3,000–4,000** for an RTX 5090 class machine. I could **not verify it** — the URL returned **HTTP 403** to WebFetch; I have only the search-result summary. **`[asserted]`, at second hand.** It establishes that ~1B tokens/week is not physically absurd; it establishes nothing about anyone actually running that way.

**Theme-revision signal (§5.4) carries the consequence.**

---

## 2. The absence inventory — eight components × exemplars

Legend: **P** present · **A** absent · **S** substituted by something cheaper · **U** unknown/not checked.

| # | Component | ruvnet — *operated* (Dream Machine on ruflo/metaharness) | ruvnet — *shipped* (autogenous / metaharness) | continuous-claude | NVIDIA OpenShell |
|---|---|---|---|---|---|
| 1 | **Kernel** (trusted spawner) | **S** — Claude Code cloud routine + cron trigger. No trusted component; the agent *is* the runtime | **P** — `@metaharness/kernel` (Rust→WASM+NAPI-RS, "7 subsystems", shipped); `autogenous::runtime` "self-running loop on the closed path" | **S** — a Bash `while` loop and GitHub Actions | **P** — Gateway (control plane + auth boundary) + Policy Engine "from application layer **down to kernel**" |
| 2 | **Capability vocabulary** | **A** — the night's authority is "what the cloud session's token can do" | **P** — AGL typed mutations declaring change/rationale/validity/**authority required**/invariants/tests/expiry/reversal; metaharness MCP default-deny + `harness mcp-scan` | **S** — GitHub token scopes + `permissions:` | **P** — declarative YAML over 4 domains; network at **HTTP method + path** granularity |
| 3 | **Delegation / attenuation** | **A** | **P** — `Mutation::admissible`: may request *less* than parent's ceiling, never more. (Note #200: ruflo's propagator still has **no call sites**; re-check condition **not met**) | **A** | **A** — no sub-delegation or attenuation model surfaced in the README |
| 4 | **Secret broker** | **S** — `OPENROUTER_API_KEY` as an env var in the cloud session | **P** — for *publishing*: GCP Workload Identity Federation → Secret Manager → `npm publish --provenance` (SLSA L2). **Not** a runtime broker for agents | **A** — provider keys in the environment | **P** — **Providers**: named credential bundles injected as env at creation, "credentials never leak into the sandbox filesystem". Privacy Router "**strips caller credentials, injects backend credentials**" on the inference path |
| 5 | **Evidence-graded commit** | **P-but-broken** — LEDGER.md one-row-per-night + ed25519 witness + gist + verdict; **the append rides in an unmerged draft PR, so it advances at the human's merge rate (5%)** | **P** — `witness` append-only signed chain; `lineage` append-only content-addressed DAG retaining poor performers; `envelope` signed receipts from ≥2 pinned judges | **S** — the git history plus `SHARED_TASK_NOTES.md`; committed on the merge path, so it does not stall | **A** — denials are logged; no append-only graded evidence primitive |
| 6 | **`/etc`** | **P** — `dream.config.json` compiled to tonight's prompt, "so the schedule can never drift from the repo" | **P** — `constitution` crate: hash-pinned, externally governed, ≥2 signers + migration path, `Constitutional` scope **never auto-promotable** | **S** — CLI flags + `CLAUDE.md` | **P** — policy YAML with an explicit **static/dynamic split**: filesystem+process **locked at sandbox creation**, network+inference **hot-reloadable** |
| 7 | **Init & supervision** | **P** — cron trigger `trig_01HpEqAcEP7…` @06:00Z, GH Actions fallback, degradation recorded not fatal, always one of 3 verdicts | **P** — `promotion` staged canary 1→10→50→100% with auto-rollback on first gate violation; `runtime` with a `Clock` and measured rollback SLOs | **S** — loop + `--max-*` bounds + `--stall-threshold` pause-for-human | **P** — Gateway coordinates sandbox lifecycle over Docker/Podman/MicroVM/K8s; container supervision; health auto-refresh |
| 8 | **The shell** | **S** — GitHub issues, gists and draft PRs are the UI | **P** — `dream-machine tui` + browser dashboard; metaharness Studio + `npx <your-brand>` CLI + `harness doctor/validate/diag` | **S** — terminal + the GitHub PR page | **P** — `openshell term`, a k9s-inspired live TUI; `sandbox connect` (SSH) |

### Where absence visibly broke something

| Absent component | Exemplar | What they do instead | Did anything visibly break? |
|---|---|---|---|
| Kernel (a *trusted* one) | ruvnet, operated | Ask the model not to merge, in the prompt | **Not yet — and the guard is absent, not merely off.** `protected: false`, zero rulesets, on all three repos. No incident found; nothing prevents one. This is #196's failure mode: a control that is believed and inert cannot be distinguished from a working one until it is tested |
| Evidence-graded commit **that advances** | ruvnet, operated | Ledger row rides in the draft PR | **Yes, demonstrably.** 7 of 9 nights across two repos left `main` with no ledger row; the machine's own STEP 1 cross-night memory therefore reads a ledger that is up to 4 nights stale |
| Cost metering of the *harness itself* | ruvnet, both | Meter the experiment ($0.00042); the operator is unmetered | **Unknown-but-unfalsifiable** — there is no artifact by which anyone, including him, could tell. That is the break |
| Anything matching fleet output to human review capacity | ruvnet, operated | Nothing, for 11 weeks | **Yes, catastrophically.** 80 nights → 4 shipped (5%), 75 untouched, some 2.5 months stale. Then the fix for the detector (`zeroMergeStreak`) was itself found **"permanently miscalibrated (never fires)"** on 2026-08-16 |
| Delegation / attenuation | all three exemplars | Nothing | **No** — single-operator, single-agent-per-run. Delegation has no load in a fleet of one principal. **This is a real datapoint for the criticality question and I flag it deliberately: nobody at this scale needed it** |
| Secret broker (runtime) | ruvnet, continuous-claude | Env vars | **No visible break** — and OpenShell shipping exactly this suggests the demand is real at the *multi-agent-per-host* boundary, not the single-operator one |
| Capability vocabulary | continuous-claude | GitHub token scopes + CODEOWNERS + required checks | **No.** It reached 0%→80% coverage on a several-hundred-thousand-line codebase with the forge's own permission model and nothing else |

**The load-bearing sentence in this table:** across three operators running at real throughput, **the components that visibly broke were the memory, the meter, and the human-throughput match. The components nobody missed were delegation, the capability vocabulary, and the runtime secret broker.**

---

## 3. Candidates

### C1 — `NVIDIA/OpenShell` — the kernel slot, shipping, personal-first · **NEW**

**Dedup:** `context_search` over `technology` + `finding` for kernel isolation / sandbox runtime / policy-below-the-agent returns **#202** (Bedrock AgentCore + Cedar, ASSEMBLE) and **#199** (outshift-casa, ASSEMBLE) — same *cluster* (deterministic enforcement at a chokepoint the agent cannot reach), **materially different instance**. OpenShell is **not in the graph**. **NEW.**

**Mechanism.** Each sandbox is an isolated container (Docker / Podman / **MicroVM** / K8s) whose egress is routed through a policy engine. Every outbound connection is intercepted and does one of three things, quoted: "**Allows** — destination and binary match a policy block. **Routes for inference** — strips caller credentials, injects backend credentials, forwards to the managed model. **Denies** — blocks and logs." Four protection layers with an explicit mutability split:

| Layer | Protects | When it applies |
|---|---|---|
| Filesystem | reads/writes outside allowed paths | **locked at sandbox creation** |
| Network | unauthorized outbound | **hot-reloadable at runtime** |
| Process | privilege escalation, dangerous syscalls | **locked at sandbox creation** |
| Inference | reroutes model API calls to controlled backends | **hot-reloadable at runtime** |

**Demonstrated vs claimed.** The README carries a **runnable refusal demo** (`examples/sandbox-policy-quickstart/demo.sh`) with the transcript inline: bare sandbox → `curl: (56) Received HTTP code 403 from proxy after CONNECT`; apply a read-only GitHub policy → `GET /zen` succeeds; `POST /repos/.../issues` → `{"error":"policy_denied","detail":"POST /repos/octocat/hello-world/issues not permitted by policy"}`. **A published refusal, reproducible in one command.** That is precisely what wfh-005's amendment asked for ("a plane must demonstrate a refusal before the run it governs") and it is `[demonstrated by them, with artifact]`. I did **not** run it — `[demonstrated by us]` remains empty.

**Resource envelope.** Install: single binary via `install.sh`, or `uv tool install openshell`, or Helm/OCI. Host requirements: Linux / macOS Apple Silicon / Windows-WSL2 (experimental), plus Docker/Podman or host virtualization. Per-sandbox cost is one container (base image ships `claude`, `opencode`, `codex`, `copilot`, python 3.14, node 22, `gh`, `git`, networking tools). **No latency or throughput figures are published for the proxy hop**, and that is the number that decides whether this can sit on a hot path — an unfilled hole I am flagging, not guessing at. `--gpu` passthrough (experimental, CDI or `--gpus all`) enables **local inference inside the sandbox**; Ollama and Pi ship as community sandboxes.

**Buy-before-build.**
- **Scope against our need.** Covers, well: kernel, `/etc` (with a genuine irreversibility distinction — static sections locked at creation), secret broker (both directions: injection at creation, credential swap on the inference path), init/supervision, the shell. Covers, partially: capability vocabulary — rich at the *network* layer (method+path), coarse at filesystem/process, and **there is no notion of a phase or a task that authority is indexed by**; policy is per-sandbox, set at creation or hot-reloaded by the operator. **Does not cover at all:** delegation/attenuation (no sub-delegation model surfaced), the evidence-graded commit primitive (it logs denials; it does not grade or append evidence), any person model, any domain vocabulary beyond coding, always-on/proactivity.
- **The eighty-percent case, named precisely.** OpenShell covers roughly five of eight components at a quality no small team will match — it has NVIDIA's kernel and container expertise behind it. **The uncovered remainder is exactly the pair the reframe treats as differentiating: phase-indexed authority derived from what a task declared, and the evidence-graded commit.** OpenShell's policy answers *what may this sandbox reach*; it does not answer *what may this sandbox reach **during this step of this task***, and it has no opinion about what constitutes a commitment versus a claim. That remainder is small in lines and large in consequence.
- **Cost and licence.** Apache-2.0, free, open source. Operational burden: run a gateway, keep policy YAML, accept a container/MicroVM dependency. **Status: alpha, "single-player mode … proof-of-life: one developer, one environment, one gateway. Expect rough edges." 459 open issues.** The Helm/K8s path is separately flagged experimental.
- **Lock-in and exit.** Low-to-moderate. Policy is declarative YAML you own; the agents inside are unmodified upstream binaries (`claude`, `codex`, `opencode`, `copilot`); exit is deleting the sandbox and running the agent directly. The real coupling is **the inference-rerouting layer** — if you build on OpenShell's Privacy Router as your model boundary, you have adopted their interposition point, and that is the one this theme most wants to own. **Adopting OpenShell for isolation is cheap to leave; adopting it for the inference seam is not.**
- **Composability.** High and directly relevant. OpenShell supplies the *plane*; #200's `@claude-flow/security` policy subtree supplies an *envelope algebra*; #199 CASA supplies *intent-scoped* K8s network authorization (and would overlap heavily). **What sits in the seams:** OpenShell's policy is set at creation or hot-reloaded by an operator, so anything that wants authority to change *per phase, derived from a declared task* has to drive `openshell policy set` from a compiler — which is #194's shape ("a compiler emitting into planes that already hold the credential"), and the seam is whether the hot-reload path is fast enough and atomic enough to sit inside a turn. **Unverified — no latency figure published.**

**Window.** 8,232★ and 1,219 forks in under six months, NVIDIA-owned, SAP embedding it as the security layer for all its agents with SAP engineers contributing upstream, and it already wraps the four major coding agents. **This is the clearest "someone is building this right now and the window is closing" signal the surface has produced in three scans.**

**Alias flag (cross-surface).** S2 will likely meet this as a *product* ("SAP Business AI Platform agent security"). S3 may meet the same idea as *sandboxing / reference-monitor / information-flow enforcement*. S4 may meet it as *OS capability models* or *jail/zone/namespace isolation*. **Same object; four names. Merge at distillation.**

**Source signal:** `external-scan` (arrived by chasing the Lamego trace — an accident of an honest null, and I record the provenance rather than dress it up).

**`cites:`**
```yaml
- type: repo
  ref: https://github.com/NVIDIA/OpenShell
  title: "OpenShell — the safe, private runtime for autonomous AI agents"
  org: NVIDIA
  year: 2026
  surface: active-dev
- type: docs
  ref: https://docs.nvidia.com/openshell/about/overview
  title: "Overview of NVIDIA OpenShell"
  org: NVIDIA
  surface: active-dev
- type: blog
  ref: https://blogs.nvidia.com/blog/secure-autonomous-ai-agents-openshell/
  title: "How Autonomous AI Agents Become Secure by Design With NVIDIA OpenShell"
  org: NVIDIA
  year: 2026
  surface: active-dev
- type: blog
  ref: https://news.sap.com/2026/05/secure-ai-agents-how-sap-and-nvidia-co-define-enterprise-grade-agent-execution/
  title: "Shaping the Future of Secure AI Agents: How SAP and NVIDIA Are Co-Defining Enterprise-Grade Agent Execution"
  org: SAP
  year: 2026
  surface: active-dev
```

---

### C2 — `ruvnet/autogenous` — the governance layer as a Rust crate set · **NEW** (adjacent to known **#200**)

**Dedup:** `#200` covers `ruflo` + `@claude-flow/security`. `autogenous` is a **different repository, created 2026-08-16**, and is not covered by #200's ASSEMBLE ruling. **NEW.** It should be filed as a sibling, and #200's re-check condition ("the policy engine ships enforcing by default") should be read against it: **in `autogenous` the enforcement is by construction — but in a repo that is one day old and badged `research prototype`, not in `ruflo`. The #200 re-check condition remains formally unmet.**

**Mechanism.** Typed mutations (AGL) that must declare change · rationale · validity scope · **authority required** · invariants preserved · test evidence · expiry · reversal. A `verifier` producing deterministic, independently re-runnable admission verdicts with full failure explanations. An `envelope` where promotion consumes ed25519-signed receipts from **≥2 distinct pinned judges** on the same corpus with a beat-parent non-inferiority margin. `promotion` as a staged canary (1→10→50→100%) with auto-rollback on the first gate violation. `deployment` closing the loop with a confirmed, signed `RollbackReceipt`. `constitution` hash-pinned outside the loop.

**Resource envelope [asserted — author-reported].** ≈0.9 µs/chunk stream observation (1 antibody), ≈14 µs (16); 100k labeled streams replayed in ~7 ms; canary decision ≈2 ns; ed25519 sign ~39k frames/s. Detectors are serializable artifacts under a closed combinator algebra with enforced resource bounds — **no closures, no regex engine** (a deliberate, and notable, capability-security-shaped restriction on what a detector may be). 71 tests. Rust 1.74+.

**Demonstrated vs claimed.** The invariants are `[asserted]` at the level of "the types enforce this" — verifiable by reading the crates, which I did **not** do (README only, plus repo metadata). The lifecycle acceptance test is described as proving the flow offline including a capability-expansion rejection at perfect fitness and a mid-canary auto-rollback. `cargo test` is one command away; **nobody has run it but him.** P7 (invented representations) is explicitly and honestly deferred: "a specified contract, not fake results."

**Buy-before-build.**
- **Scope against our need.** Covers, on paper and unusually completely: capability vocabulary (typed mutations with declared authority), delegation/attenuation (monotone, in `Mutation::admissible`), evidence-graded commit (`witness` + `lineage`, both append-only), `/etc` (`constitution`), init/supervision (`runtime`, `promotion`, `deployment`). **Does not cover:** the kernel/isolation plane (it governs *mutations to software*, not *what a running agent may reach*), the shell, secret brokering, or anything outside the software-evolution domain. **Its subject is a codebase, not a person's life** — the six-domain reframe would require re-hosting the abstractions, not adopting the product.
- **Cost and licence.** MIT, free. Real cost: it is a **1-day-old research prototype by a single author with 11 stars**, in Rust, from a maintainer whose flagship (`ruflo`, #200) shipped its equivalent policy plane **inert by default with 106 escape hatches**. The prior is not favourable and the graph already records why.
- **Lock-in and exit.** Low as a dependency (MIT crates, per-crate boundaries), high as a *conceptual* commitment — AGL is a vocabulary, and adopting someone's vocabulary at v0.1 from a single author is the expensive kind of lock-in.
- **Composability.** Its natural complement is C1: OpenShell governs *what a running agent may reach*, autogenous governs *what a change must prove before it lands*. Together they cover seven of eight. **In the seams:** nothing connects them — autogenous has no notion of a sandbox and OpenShell has no notion of a promotion.

**Alias flag.** S4 will very likely meet `witness`/`lineage` under **in-toto attestation**, **content-addressed provenance**, or **event sourcing**; `constitution` under **policy-as-code** or **separation of the reference monitor from the subject**; `envelope`'s ≥2-pinned-judges rule under **verification independence (DO-178C)** or **Clark-Wilson E4**, which wfh-005 already settled. **Same invariant, four names.**

**Source signal:** `owner-injection` (ruvnet was owner-injected; this repo was found by the organization-walk).

**`cites:`**
```yaml
- type: repo
  ref: https://github.com/ruvnet/autogenous
  title: "Autogenous — Governed Evolutionary Software"
  author: "Cohen"
  org: ruvnet
  year: 2026
  surface: active-dev
```

---

### C3 — `ruvnet/dream-machine` + the Dream Cycle operating model · **NEW**

**Dedup:** not in the graph. **NEW.** Distinct from #200 (`ruflo`) — this is the *routine that runs against* ruflo, factored out.

**Mechanism.** A config-compiled nightly routine: `dream.config.json` → `compile` → tonight's 26-step prompt → cloud cron session → one of three verdicts → gist + labelled issue + **draft** PR + one ledger row. CLI surface: `init`, `compile`, `schedule`, `ledger verify`, `ledger signals`, `witness stamp`, `witness verify`, `tui`.

**Resource envelope.** npm package, `npx dream-machine`. Runtime cost is one agent session per repo per night plus a research-agent token spend; the paid portion is small and metered at the experiment ($0.00042–$0.048/run observed) and **unmetered at the harness**. A no-API-key night still completes as an honest `INCONCLUSIVE`.

**Demonstrated vs claimed.**
- `[demonstrated]` — the schedule runs (trigger id, timestamped issues on 4 consecutive nights across 3 repos); the three-verdict discipline holds; REJECT is published; the before/after falsification protocol is real and detailed; the ledger backfill measuring 4/80 adoption is a genuine self-audit; the machine detects its own review-latency signal.
- `[demonstrated — and it is a defect]` — **branch protection is off and there are zero rulesets on all three repos**; the "never merges" invariant is prompt-only. And the ledger's one-row-per-night invariant fails on `main` 7 nights out of 9 because the append rides in a draft PR.
- `[asserted]` — that the ~800-line predecessor routines were "the same 26-step pipeline"; that the config→prompt compilation prevents drift (plausible, unverified).

**Buy-before-build.**
- **Scope against our need.** Covers `/etc`, init/supervision, the shell, and a real (if stalling) evidence-graded commit. **Does not cover:** kernel, capability vocabulary, delegation, secret broker. And the thing it most conspicuously does not cover is **the bottleneck it discovered** — nothing in it matches production rate to review rate.
- **Cost and licence.** MIT, free. Operational cost: one cloud agent routine per repo per night, plus the human review capacity it will immediately outrun. **The 5% adoption figure is the true cost of this pattern and it should be read as a purchase price, not a footnote.**
- **Lock-in and exit.** Very low — it is a prompt compiler over a JSON config; the artifacts are GitHub issues, gists and PRs you already own. Exit is deleting the cron.
- **Composability.** It is the *shape* of a nightly self-improvement loop, and it composes with anything that supplies the missing gate. The obvious composition — Dream Machine's discipline + continuous-claude's forge-delegated gate and budget bounds + branch protection actually switched on — costs almost nothing and closes the demonstrated hole.

**Alias flag.** S4/S2 will meet this pattern under **"Ralph loop"**, **"agent in a loop"**, and — most importantly — **"loop engineering"** (§4.3). `githubnext/agentics` is the GitHub-side sibling. **Four names, one operating model.**

**Source signal:** `owner-injection`.

**`cites:`**
```yaml
- type: repo
  ref: https://github.com/ruvnet/dream-machine
  title: "Dream Machine — a config-driven engine for nightly, cloud-scheduled, evidence-gated repository evolution"
  author: "Cohen"
  org: ruvnet
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/ruvnet/ruflo/blob/main/docs/dream-cycle/LEDGER.md
  title: "Ruflo Dream Cycle Ledger — 80-night backfill, 4 shipped / 1 rejected / 75 untouched"
  org: ruvnet
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/ruvnet/metaharness/issues/206
  title: "[Dream Cycle 2026-08-17] darwin-evolution: ADR-249's cost seam was shipped but never wired"
  org: ruvnet
  year: 2026
  surface: active-dev
```

---

### C4 — `AnandChowdhary/continuous-claude` — forge-delegated governance + mandatory budget bound · **NEW**

**Dedup:** not in the graph. **NEW.**

**Mechanism, resource envelope, evidence:** §1.2 above. Bash + PowerShell runner; dependencies are `gh`, `git`, and a coding-agent CLI. Negligible footprint. Cost is bounded by construction: one of `--max-runs` / `--max-cost` / `--max-duration` is **required**.

**Buy-before-build.**
- **Scope against our need.** Covers, cheaply: init/supervision, cost bounds, failure handling with a human handoff, cross-iteration memory, **and gate-input independence via a cross-provider reviewer pass**. Substitutes the forge for the entire authority layer. **Does not cover:** kernel, capability vocabulary beyond token scopes, delegation, secret broker, evidence grading beyond git history.
- **The eighty-percent case, named.** For a **single operator on GitHub**, branch protection + required checks + CODEOWNERS + a cross-provider reviewer pass reaches most of the governance layer for zero build cost. **The uncovered remainder: it is repo-shaped.** It cannot govern anything that is not a pull request — no voice surface, no 3D-printer job, no travel booking, no consequence outside a diff. The moment the framing's six domains arrive, the forge stops being a gate, and there is no second gate behind it.
- **Cost and licence.** MIT, free. Real cost: **GitHub-only** by the author's own statement (Gitea unsupported), and **one month stale** (last push 2026-07-13).
- **Lock-in and exit.** Exit is trivial (delete a bash script). The *pattern's* lock-in is GitHub's review API.
- **Composability.** Composes cleanly with C3 (discipline) and C1 (isolation). Its `--max-cost`/`--max-calls-per-hour` primitives are the smallest useful thing anyone in this scan built for the cost dimension, and they are ~40 lines of shell.

**Alias flag.** Same cluster as C3 — "Ralph loop", "loop engineering", `githubnext/agentics`.

**Source signal:** `external-scan` (by-function sweep).

**`cites:`**
```yaml
- type: repo
  ref: https://github.com/AnandChowdhary/continuous-claude
  title: "Continuous Claude — Ralph loop with PRs: run Claude Code in a continuous loop, autonomously creating PRs, waiting for checks, and merging"
  author: "Chowdhary"
  year: 2026
  surface: active-dev
```

---

### C5 — "Loop engineering" — a named discipline the theme has no vocabulary for · **NEW (vocabulary find, not a product)**

**Dedup:** the *term* appears nowhere in `themes.md`, in wfh-005's 158 citations, or in the graph. **NEW.**

**What it is.** A self-named, fast-growing field for exactly the job this theme calls "workflow harness", using **none of this theme's nouns**. Its vocabulary is *loop · round · goal · verify · plan · worker · board · doctrine*. Representative population found in a single query (§4.3):

| Stars | Repo | Self-description (verbatim, abridged) |
|---|---|---|
| 16,365 | `HKUDS/DeepCode` | "Open Agentic Coding (Agent Harness & **Loop Engineering** & Multi-Agent Orchestration)" |
| 10,439 | `cobusgreyling/loop-engineering` | "Practical patterns, starters & CLI tools for loop engineering with AI coding agents" |
| 1,082 | `alchaincyf/loop-engineering-orange-book` | "A plain-language guide to loop engineering (中文 + English PDF)" |
| 807 | `valkor-ai/loom` | "Loop engineering for agentic software delivery" |
| 488 | `agentic-in/inferoa` | "Inference-native **Tokenmaxxing** Agent Harness for Loop Engineering" |
| 470 | `baidu-baige/LoongFlow` | "expert-grade Agent framework for Loop Engineering … Plan-Execute-Summa[rize]" |
| 337 | `GaosCode/PlanWeave` | "**file-backed** loop engineering system for long-running coding agents" |
| 135 | `loop-js/loop.js` | "state a Goal; Rounds run until a skeptical, **read-only Verify agent** [approves]" |
| 88 | `brittanyellich/loop-board` | "skills and workers to run loop engineering with Claude Code" |
| 75 | `rafmacalaba/armada` | "Turn any repository into a self-organizing AI engine" |

**Why it is a candidate rather than trivia.** Two of these encode positions this theme reached the hard way. `loop.js` ships a **skeptical, read-only Verify agent** — gate-input independence, expressed as a read-set restriction, in a 135-star package. `PlanWeave` is **file-backed** — the `/etc`-as-versioned-files answer. And `inferoa`'s "**tokenmaxxing**" names the cost dimension as a design center in one word this theme does not have.

**Buy-before-build.** Not a single artifact, so no adopt/assemble/build verdict attaches. **What it changes is the search:** the theme's watchlist and every scan query to date have used vocabulary that misses a field with >30,000 aggregate stars. That is the wfh-005 "Platform Evolution Engine" failure repeating at population scale, and instrument 3 is what caught it.

**Alias flag — the important one.** `theme:workflow-harness` ≈ **loop engineering**. If S2/S3/S4 return anything shaped like "iterative agent execution with a verification round", it is this. **Merge at distillation.**

**Source signal:** `external-scan`.

**`cites:`**
```yaml
- type: repo
  ref: https://github.com/cobusgreyling/loop-engineering
  title: "loop-engineering — practical patterns, starters & CLI tools for loop engineering with AI coding agents"
  author: "Greyling"
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/loop-js/loop.js
  title: "loop.js — a loop engineering framework; Rounds run until a skeptical, read-only Verify agent approves"
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/HKUDS/DeepCode
  title: "DeepCode: Open Agentic Coding (Agent Harness & Loop Engineering & Multi-Agent Orchestration)"
  org: HKUDS
  year: 2026
  surface: active-dev
```

---

### C6 — Sub-20-star implementations of five named components · **NEW** (the low-star instrument's payload)

Not one candidate — a **demonstration that five of the eight components have working-shaped implementations no ranked search reaches.** Characterized thinly and deliberately; each is a lead, not a verdict.

| Stars | Repo | Component it occupies | Verbatim |
|---|---|---|---|
| **7** | `sattyamjjain/ferrumdeck` | kernel + evidence-graded commit | "AgentOps control plane for AI agent execution. **Rust policy plane, hash-chained audit, deny-by-d[efault]**" |
| **1** | `hherb/kastellan` | the whole reframe, in miniature | "A **personal, always-on** AI agent, **contained by design** — sandboxed tools, vendor-neutral" — Rust, **AGPL-3.0**, created 2026-05-06, **pushed today** |
| **0** | `wisent-ai/skarbiec` | secret broker | "**Credential Management and Authentication for the AI Agent Era.** Get any credential, even if you…" |
| **0** | `voidcorp-core/void-harness` | `/etc` + compile-to-host | "A **development-doctrine operating system for coding agents. One doctrine, compiled to** Claude Cod[e]…" |
| **13** | `Lexus2016/hermes-agent-evolution` | init/supervision + self-improvement | "Self-evolving AI Agent with autonomous research, proposal generation, and **self-update**" |
| **0** | `akdira/self-smarter-everyday` | init/supervision | "Autonomous **daily** self-improvement system for AI agents. **Nightly self-reflection, self-audit**" |
| **118** | `jigripokri/POHA` | always-on / proactivity | "**Personal Overnight Helper Agent. Runs while you sleep. Serves up a morning brief** before yo[u wake]" |

`kastellan` is the closest single object to the reframe I found anywhere — personal, always-on, contained by design, vendor-neutral, Rust, actively developed **today**, at **one star**. **Note its licence: AGPL-3.0.** That is a hard fork/lift constraint and the reason it is flagged rather than recommended.

**Buy-before-build:** not gathered per-item; these were surfaced to prove the instrument works and to give the leader leads. **Declared as a partial characterization, not a hole.**

**Source signal:** `external-scan`.

**`cites:`**
```yaml
- type: repo
  ref: https://github.com/hherb/kastellan
  title: "Kastellan — a personal, always-on AI agent, contained by design: sandboxed tools, vendor-neutral"
  author: "Herborn"
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/sattyamjjain/ferrumdeck
  title: "ferrumdeck — AgentOps control plane: Rust policy plane, hash-chained audit, deny-by-default"
  author: "Jain"
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/wisent-ai/skarbiec
  title: "skarbiec — credential management and authentication for the AI agent era"
  org: wisent-ai
  year: 2026
  surface: active-dev
```

---

### C7 — `github/gh-aw` — the incumbent moved, and the move is the delta · **KNOWN (watchlist), material change**

**Dedup:** the theme's declared **incumbent to beat**, watchlist re-check condition: *"it derives capability from an author-declared phase, or leaves technical preview."*

**[demonstrated — with artifact] `gh api repos/githubnext/gh-aw` now returns `"full_name": "github/gh-aw"`.** The repository **graduated out of the GitHub Next incubator into the main `github` organization** — the same rename-and-redirect evidence pattern wfh-006 used for `sst/opencode` → `anomalyco/opencode`. 4,944★, MIT, pushed today.

**Re-check condition, ruled:** **partially met.** Leaving `githubnext` for `github` is a productization signal of exactly the kind the condition was written to catch. It is not fully met — releases remain prerelease (v0.87.0 2026-08-16, v0.86.3 2026-08-15; last non-prerelease v0.86.2 2026-08-11), and I found **no occurrence of "preview" or "experimental"** in the current README, which is itself a change worth noting. **The second leg — deriving capability from an author-declared phase — is still not met**; the README describes YAML frontmatter configuring "triggers, permissions, tools, and the AI engine", compiled by `gh aw compile` into a `.lock.yml`, with "safe outputs" buffering and validating writes into separate jobs with scoped permissions. Author-declared *permissions*, not an author-declared *phase*.

**New in the README since wfh-005:** built-in engines now include **GitHub Copilot, Claude Code, OpenAI Codex, Google Gemini, and Pi**. Agent jobs "are read-only and sandboxed by default."

**Window:** the incumbent got closer. **Last looked: 2026-08-17.**

**Source signal:** `external-scan`.

**`cites:`**
```yaml
- type: repo
  ref: https://github.com/github/gh-aw
  title: "GitHub Agentic Workflows (gh-aw)"
  org: GitHub
  year: 2026
  surface: active-dev
```

---

## 4. The three instruments — method, queries, yield, reported separately

**Standing note (#216):** all three had never been exercised in this garage. All three fired. All three produced material no ranked mechanism-vocabulary search would have reached, and **the by-function sweep and the low-star pass were the two highest-yield instruments of the scan.**

### 4.1 Instrument 1 — the organization-walk

**Method.** Enumeration, not search. `gh api --paginate users/ruvnet/repos?per_page=100&sort=pushed&direction=desc` → all 204 public repos in push-recency order, with stars, language, created/pushed dates, fork flag, description. Then `users/ruvnet/orgs` (empty — a purely personal account), then `users/ruvnet/events/public?per_page=100` as an activity walk, then targeted content reads on the repos the enumeration surfaced.

**Queries:** three API calls, zero search terms.

**Yield: high, and unreachable any other way.** The enumeration surfaced, ordered by push recency, a 2026 output the theme had no idea existed:

- `autogenous` **11★, created 2026-08-16** — **C2, the governance layer.** No search I would have written finds an 11-star, one-day-old repo.
- `dream-machine` **12★, created 2026-08-13** — **C3, the operating model.**
- `metaharness` 590★ — "a factory for agent frameworks", 10 hosts, `@metaharness/kernel` (Rust→WASM+NAPI-RS, 7 subsystems), MCP default-deny, `harness mcp-scan` ("npm audit for agent tools" — flags shell/network grants, wildcard permissions, unguarded secrets; exits 1 on any HIGH), Ed25519 witness manifests byte-deterministic across runners, SBOM SPDX-2.3, GCP WIF→Secret Manager→`npm publish --provenance` (SLSA L2), a Cost-Pareto leaderboard, `@metaharness/router`, `weight-eft`, `turn-credit`.
- `helix` 40★ — "a private, **local-first**, anti-hallucination **Personal Health Intelligence** platform on the ruvnet stack (Ruflo + RuVector + Cognitum Seed + MetaHarness/Darwin)". **A second domain, on the same personal stack.**
- `ruos-macair` 10★ — "**ruOS** for MacBook Air 2012 — custom Linux with DJ, Spotify, Tailscale, and ruOS agent stack." He has literally shipped a thing called an OS.
- `rvm` 136★ — "The Virtual Machine Built for the Agentic Age, in Rust" (metaharness calls it a "hardware-isolated sandbox" host).
- `RuView` 90,462★, `worldgraph`, `rvcsi`, `rufield`, `wifi-veil`, `RuCelium` — an **ambient RF/presence sensing stack**, which is the structural analogue of the reframe's always-on surface.
- `unsorry` 2★ (fork) — "Autonomous agents proving theorems in Lean 4… **Git is the queue, the kernel is the gate, no sorry survives**." A one-sentence statement of the whole architecture, at two stars.
- `retort` 6★ — **ruvnet has forked `adrianco/retort`.** wfh-005 established the two projects are in contact (ruvnet is a retort contributor, 5 commits); the fork is a further datapoint.
- `ruvn` 11★ — "AI research harness that turns a question into a **graded, cited evidence dossier**." That is this garage's own shape, built by someone else, at eleven stars.

**What the enumeration cost:** three API calls and about two minutes. **What it returned:** two of the seven candidates in this file, including the one that falsifies the run's premise. On this evidence the organization-walk should be a standing instrument, not a one-off.

### 4.2 Instrument 2 — the deliberately low-star pass

**Method.** Two halves. (a) The organization-walk *is* a low-star pass by construction — it returns an author's whole output regardless of popularity, which is how `autogenous` (11★) and `dream-machine` (12★) arrived. (b) An explicit `stars:<N` filter on GitHub repository search, outside ruvnet.

**Queries (all with an explicit stars ceiling and a recency floor):**
1. `nightly self-improving repository evolution in:readme pushed:>2026-06-01 stars:<60`
2. `"personal operating system" in:readme,description pushed:>2026-05-01 stars:<40`
3. `"append-only" receipts evidence signed in:readme pushed:>2026-05-01 stars:<40`

**Yield: high on (1) and (3), and a valuable negative on (2).**

- **(1)** → `Lexus2016/hermes-agent-evolution` (13★), `akdira/self-smarter-everyday` (0★). Also, incidentally, `ChaoYue0307/awesome-loop-engineering` (51★) — which is what put me onto instrument 3's decisive term.
- **(3)** → the four most valuable low-star hits in the scan: `ferrumdeck` (7★, kernel + hash-chained audit + deny-by-default), `skarbiec` (0★, the secret broker), `void-harness` (0★, doctrine-compiled-to-host), and via query (2)'s neighbourhood `kastellan` (1★, the reframe in miniature). **C6.**
- **(2) is a declared negative and it matters.** The phrase "personal operating system" at low star counts returns almost entirely **productivity / second-brain / life-dashboard projects** — `LifeOS`, `LifeOperatingSystem`, `MasterDash`, `PRANAV-OS`, `Personal-OS-UI`, `lifestack-*`, `fallseed-creator-os`. **The term is already owned by a different field and carries none of the runtime semantics the reframe intends.** This is the same class of hazard wfh-005 flagged for "soundness": a name that guarantees a misread by the audience most likely to encounter it. It goes to the owner in §5.4.

**Calibration against wfh-005:** that run's decisive find sat at 17 stars, its predecessor at 5, its dataset repo at 4. This run's finds sit at 11, 12, 7, 1, and 0. **No ranked search reaches single digits. The instrument is the only thing that does.**

### 4.3 Instrument 3 — the by-function sweep (no theme nouns)

**Constraint honoured:** no query below contains *harness*, *agent*, *capability*, *gate*, *orchestration*, or *control plane*.

**Method.** Describe the job in plain function words and search that. The job, stated without jargon: *something runs unattended while I sleep, decides what to change, proposes it, and leaves a record I can check in the morning.*

**Queries.**
1. WebSearch — `software that runs unattended overnight proposes changes a person approves in the morning keeps a record of what it decided` → **not executed; the session's WebSearch budget (200/200) closed on this call.** Declared, not hidden.
2. `gh` repo search — `"while you sleep" review morning in:readme pushed:>2026-05-01`
3. `gh` repo search — `"single-user" daemon supervisor "append-only" in:readme pushed:>2026-04-01`
4. `gh` repo search — `"loop engineering"` (the term surfaced by instrument 2, itself containing none of the theme's nouns)

**Yield: the highest of the three, and it validates the instrument exactly as designed.**

- Query 2 returned **`AnandChowdhary/continuous-claude` (1,370★)** — **C4**, an entire published operating model with budget bounds and a cross-provider independent reviewer, whose README uses "loop" and "iteration" and never once uses this theme's vocabulary. It also returned `jigripokri/POHA` (118★, "Personal Overnight Helper Agent. Runs while you sleep. Serves up a morning brief"), `CronusL-1141/AI-company` (343★, "Multi-agent team **operating system** for Claude Code"), and `eugeniughelbur/obsidian-second-brain` (4,064★, "Persistent memory for Claude Code and 6 other CLI agents, stored as plain markdown").
- Query 3 returned `kastellan`, `ferrumdeck`, `skarbiec`, `void-harness` — feeding **C6**.
- Query 4 returned **C5**: a >30,000-aggregate-star named discipline the theme has never read, including `loop.js`'s "skeptical, **read-only Verify agent**" and `inferoa`'s "**Tokenmaxxing**".

**One further cross-cutting observation from the sweep:** **OpenClaw** appears independently in three places — `VoltAgent/awesome-openclaw-skills` at **51,996★**, ruvnet's metaharness host list, and NVIDIA OpenShell's supported-agent table (via `NVIDIA/NemoClaw`) — plus a low-star "privacy-first OpenClaw alternative" (`Bazza1982/HASHI`). **A 52k-star ecosystem that the theme's watchlist does not name**, corroborated across three independent sources. Flagged for the derived watchlist; **not characterized** — declared hole.

**Verdict on #216:** all three instruments produced verdict-relevant material that the theme's existing method would have missed. wfh-005's diagnosis was correct and the remedy works.

---

## 5. Surface-coverage report

### 5.1 What I searched

**Hunting grounds.** GitHub REST API — user profile, full paginated repo enumeration (204 repos), public event feed, repository metadata, **branch-protection and ruleset endpoints**, issue and PR listings, issue-search with label and state filters, and base64 content reads of `README.md`, `docs/dream-cycle/LEDGER.md` (×3), package and crate directory listings, and full issue bodies. GitHub repository **search** with `stars:<N`, `pushed:>DATE`, and `in:readme` qualifiers for instruments 2 and 3. `WebSearch`/`WebFetch` for the Lamego trace and the OpenShell/SAP corroboration, until the budget closed.

**Read at depth:** `ruvnet/dream-machine` (README, ledger), `ruvnet/ruflo` (ledger — all 80 backfill rows counted, PR list), `ruvnet/metaharness` (README, top-level tree, 38 packages, 5 crates, ledger, PR list, full body of issue #206, `turn-credit` README), `ruvnet/autogenous` (README), `NVIDIA/OpenShell` (README, repo metadata), `AnandChowdhary/continuous-claude` (README, full flag reference), `github/gh-aw` (README, releases).

**Unimatrix dedup:** four `context_search` calls over `technology` + `finding` — ruvnet/ruflo/policy/delegation; personal-OS/fleet/local-throughput; sandbox-kernel-isolation-policy-below-the-agent; nightly-loop/draft-PR/evidence-ledger. Anchors confirmed: **#200** (known), **#196**/**#254** (cited, not re-derived), **#199**/**#202** (nearest cluster to C1), **#194** (bears on C1's seam).

### 5.2 What I deliberately skipped, and why — declared holes, not silent omissions

| Skipped | Why |
|---|---|
| **Temporal agent plugins** (watchlist) | WebSearch budget exhausted before I reached it; the re-check condition ("a plugin reaches general availability") is a release-status question that `gh api` cannot answer for a non-GitHub-primary product. **Unwalked. Declared hole.** |
| **MCP authorization specification** (watchlist) | Same cause. Re-check condition ("a proposal for per-tool or per-resource scopes opens") requires reading the spec repo's open PRs/discussions; I ran out of instrument before I ran out of intent. **Unwalked. Declared hole.** |
| **`anthropics/claude-agent-sdk-typescript` #172** and subagent permission-mode inheritance (watchlist) | Not checked. The gh-aw half of "coding-agent permission and hook models" *was* walked (safe-outputs, default read-only, `permissions:`). **The SDK half is a declared hole.** |
| **`dug-21/jurati` issue #12** (watchlist) | Not reachable from this scout's position. |
| **`adrianco/retort` at depth** | Walked at metadata only — 196★, Apache-2.0, pushed 2026-08-17, plus the new fact that **ruvnet has forked it**. wfh-005 read the full 21k-line clone 16 days ago; its re-check condition ("replicate counts rise above n=1 on published routes") requires re-parsing `optimal.json`, which I judged a poor use of remaining effort against a scan whose question is the exemplars. **Partial. Declared.** |
| **`outshift-casa` at depth** | Metadata only — 17★, Apache-2.0, pushed 2026-08-16, still alpha-shaped. Re-check condition ("leaves alpha, gains a non-Istio data plane, or a task-based reference implementation lands") **not verified either way. Declared hole**, and a relevant one given C1 sits in the same cluster. |
| **`autogenous` and `@metaharness/kernel` source** | READMEs only. Every structural guarantee in C2 is `[asserted]` at "the types enforce this"; verifying would mean reading Rust, which is a round-two ask. **Declared.** |
| **Running anything** | The run's proof bar is directional; no compute arm. Correct by scope, and it caps every claim here at `claimed`. |
| **`RuView` (90,462★) and the RF-sensing stack** | Enumerated and named, not characterized. Out of lens as *technology*; in lens only as evidence that ruvnet's stack spans domains. **Deliberate.** |
| **OpenClaw ecosystem (51,996★)** | Surfaced from three independent directions and **not characterized**. The largest single unread thing this scan touched. **Declared hole — recommend it enters the watchlist.** |

### 5.3 Cold-leg record — spend stated explicitly

**Instruments 2 and 3 were the cold leg, as the assignment specified, and they were the majority of the scan's discovery value.**

Rough effort split: **warm leg ≈ 35%** (ruvnet walk — though note the *walk* is warm and its *findings* were entirely unflagged; gh-aw; retort/casa metadata), **cold leg ≈ 45%** (instruments 2 and 3: seven search formulations, four of which produced candidates), **≈20%** on the Lamego trace, **which returned nothing and is reported as nothing.**

**Read cold, dry or thin:**
- Low-star query (2) — `"personal operating system"` under 40 stars. **Dry for candidates, productive as a negative** (§4.2, and §5.4 below).
- The six Lamego search formulations. **Completely dry.** Reported as such, at length, because a scan that quietly drops an owner-named exemplar is worse than one that reports it missing.
- The SitePoint 17k tok/s local-inference article — **unfetchable, HTTP 403.** Cited nowhere as fact.
- `ruvnet/orgs` — empty. A dry call that is nonetheless informative: **there is no organization behind any of this. It is one person.**

**Cost of the cold leg relative to the warm leg:** the warm leg was cheap and immediately productive — three API calls into ruvnet returned two candidates. The cold leg was roughly three times the effort per unit of output and produced **C1's corroboration, C4, C5, and C6 — four of seven candidates, including the field-level vocabulary miss and the strongest single-object find.** The warm leg would have returned a competent report about ruvnet and nothing else. **On this run the cold leg was not a tax; it was the scan.**

### 5.4 Theme-revision signal — three, for the owner at the triage gate

Relayed as signal, not as change. I do not alter the scan in flight (the failure that closed wfh-002).

**(a) The name "personal operating system" is already taken, and by the wrong field.** Instrument 2 established that a low-star search on the exact phrase returns life-dashboards and second-brain apps almost exclusively. Anyone who encounters the reframe under that name will file it with `LifeOS` and `MasterDash`. This is structurally identical to wfh-005's "do not call it soundness" ruling, and it deserves the same treatment: **choose the name against the audience most likely to take it seriously.** Note that the field which *is* doing this work has already named itself — **loop engineering** (C5) — and that the runtime layer has named itself too: NVIDIA calls it a **shell**.

**(b) The run's stated premise about the exemplars is half wrong, and the correction sharpens rather than weakens the run.** "Neither built the governance layer" is false for ruvnet on artifact (C2). What is true, and more interesting, is that **he built it and does not run on it** — his own fleet's central invariant is a sentence in a prompt on three repos with branch protection disabled. The honest restatement is: *at this scale, operators build governance as a product and operate without it, and nothing has visibly broken yet.* That is a much better question for the criticality report than the original premise, and it is not rhetorical — it may equally support "the governance layer is not load-bearing at n=1 operator" as "he has been lucky."

**(c) The measured bottleneck at this scale was human review throughput, not authority.** Eighty nights, 4 shipped, 75 untouched, and the detector built to catch it was itself found dead. None of the eight named components addresses this. If the criticality report ranks eight components and the empirically demonstrated failure at real scale is a ninth thing nobody listed, the ranking will be answering a question the evidence did not ask. **Recommend the coverage grid's proposed promotions be read against this** — "always-on and proactivity" is adjacent but not the same thing; what the evidence names is closer to *throughput matching between the fleet and its reviewer*, and the theme has no dimension for it.

### 5.5 Warm-leg table — last looked and what moved

| Watchlist entry | Last looked | Re-check condition | Ruled |
|---|---|---|---|
| **GitHub Agentic Workflows (`gh-aw`)** — the incumbent | **2026-08-17** | derives capability from an author-declared phase, **or leaves technical preview** | **PARTIALLY MET — material.** Repo moved `githubnext/gh-aw` → **`github/gh-aw`** (API redirect, demonstrated). No "preview"/"experimental" left in the README. Still prerelease (v0.87.0). Phase-derivation leg **still not met** — author-declared *permissions*, not phase. 4,944★ |
| **`ruvnet`** — `ruflo`, `metaharness`, `agentic-flow` | **2026-08-17** | policy engine ships **enforcing by default**, or the delegation propagator gains call sites | **NOT MET in `ruflo`** — no evidence either leg moved. **BUT: a new repo, `autogenous` (2026-08-16), ships enforcement by construction** (monotone attenuation in `Mutation::admissible`, promotion that cannot consume caller-supplied booleans). **Recommend splitting this watchlist entry** — the re-check condition now needs a target |
| **MCP authorization specification** | *not walked* | a per-tool/per-resource scope proposal opens | **DECLARED HOLE** — WebSearch budget exhausted |
| **`dug-21/jurati` #12** | *not walked* | any amendment to the enforcement seam | **DECLARED HOLE** — out of this scout's reach |
| **Coding-agent permission & hook models** | **2026-08-17** *(partial)* | claude-agent-sdk-typescript #172 closes, or subagent permission-mode inheritance becomes overridable | **PARTIAL.** gh-aw's model walked (read-only default, sandboxed, safe-outputs with scoped write jobs). **SDK leg is a declared hole** |
| **Agent over-privilege measurement** | *not walked* | a new benchmark or replication lands | **DECLARED HOLE** — literature-shaped; S3's ground |
| **Cisco Outshift / AGNTCY** — `outshift-casa` | **2026-08-17** *(metadata only)* | CASA leaves alpha, gains a non-Istio data plane, or a task-based reference implementation lands | **UNRULED.** 17★, Apache-2.0, active (pushed 2026-08-16). Not read at depth. **Relevant hole** — C1 sits in the same cluster and is 480× more popular |
| **`adrianco/retort`** | **2026-08-17** *(metadata only)* | replicate counts rise above n=1, or the routing feed gains a versioned schema | **UNRULED.** 196★, active (pushed today). **New fact: `ruvnet` has forked it** (`ruvnet/retort`, 6★) |
| **Temporal agent plugins** | *not walked* | a plugin reaches general availability | **DECLARED HOLE** |

---

## 6. Compact return

| Find | Lens | New / known | Adopt-assemble-build evidence present? |
|---|---|---|---|
| **C1 `NVIDIA/OpenShell`** — kernel-level agent runtime, YAML policy over fs/net/proc/**inference**, credential broker, personal-first, 8,232★, Apache-2.0, alpha | **IN** | **NEW** (cluster-adjacent to #199, #202) | **Yes — full.** Scope-vs-need gap named (no phase-indexed authority, no delegation, no evidence-graded commit); cost/licence; lock-in (low for isolation, **high for the inference seam**); composability + the seam. **Latency of the proxy hop = unfilled hole** |
| **C2 `ruvnet/autogenous`** — governance layer as Rust crates; constitution outside the loop, monotone attenuation in the types, ≥2 pinned judges, append-only witness+lineage | **IN** | **NEW** (sibling of known **#200**) | **Yes.** Covers 5 of 8 on paper; **1-day-old research prototype, 11★, single author with a prior of shipping enforcement inert (#200)** |
| **C3 `ruvnet/dream-machine`** + the Dream Cycle | **IN** | **NEW** | **Yes.** Purchase price named explicitly: **5% adoption over 80 nights** |
| **C4 `continuous-claude`** — forge-delegated gate, cross-provider independent reviewer, **mandatory budget bound** | **IN** | **NEW** | **Yes.** The 80% case and its remainder named: **it cannot govern anything that is not a pull request** |
| **C5 "loop engineering"** — a >30k-star named discipline using none of this theme's nouns | **IN** (vocabulary) | **NEW** | n/a — not a single artifact. **Changes the search, not the build** |
| **C6 sub-20-star component implementations** (`ferrumdeck` 7★, `kastellan` 1★ **AGPL-3.0**, `skarbiec` 0★, `void-harness` 0★) | **IN** | **NEW** | **Partial — leads, deliberately thin.** Declared |
| **C7 `github/gh-aw`** — the incumbent left the incubator | **IN** | **KNOWN** (watchlist) | Re-check ruled partially met; **material window signal** |
| **"Andre Lamego's basement stack"** | — | **UNLOCATABLE** | **No.** Six formulations, zero primary sources. Headline numbers `[asserted]` with the assertion itself unrecoverable |

### Flags for the leader

1. **The run's premise needs amending before the hypothesizer runs.** "Neither built the governance layer" is false for ruvnet on artifact. The true and sharper statement is in §5.4(b). Left uncorrected it will bias the divergent step toward inventing what already exists.
2. **The second exemplar does not exist in reachable form.** §1.3. I substituted `continuous-claude` so the teardown is n=2, and flag that S5's challenge brief ("they reach very high throughput with none of it") **rests partly on a number nobody can source.** S5 should be told.
3. **Alias merges required at distillation** — C1 with S2's SAP/enterprise-product read, S3's reference-monitor/IFC literature, S4's OS-capability and jail/namespace prior art. C2's `witness`/`lineage` with S4's in-toto / event-sourcing / content-addressed-provenance job (b), and its ≥2-pinned-judges rule with wfh-005's settled Clark-Wilson E4 / DO-178C ground. C3+C4+C5 are one cluster under four names (Dream Cycle · Ralph loop · agent-in-a-loop · loop engineering).
4. **Two new inert-control instances, plus a meta-instance** — ruvnet's branch protection absent while advertised (#196's third site), and dream-machine's `zeroMergeStreak` "permanently miscalibrated (never fires)": **the detector for the detector, dead.** Corroborates #196/#254 from an independent codebase. Evidence, not a verdict.
5. **`context_search` returned no hit for OpenShell, dream-machine, continuous-claude, or loop engineering.** Four genuinely new objects. #200 is the only prior-art collision and it is correctly scoped.
6. **Three declared holes I would fill first if round two fires:** (a) OpenShell's policy hot-reload latency and atomicity — it decides whether C1 can sit inside a turn; (b) `outshift-casa` at depth, since C1 supersedes it in the same cluster and the graph currently records the weaker instance as ASSEMBLE; (c) the OpenClaw ecosystem, 52k stars, corroborated from three independent directions and entirely unread.
