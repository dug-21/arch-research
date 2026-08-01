# wfh-005 — scout, ACTIVE DEVELOPMENT, round three (owner-directed)

**Target:** `adrianco/retort` · **Mode:** CHALLENGE · **Surface:** `active-dev` · **agent_id:** `wfh-005-scout-retort`
**Method:** repo cloned and read (~21,000 lines of Python under `src/retort`, plus the eleven-module `retort_metaharness` package, ~90 KB). **Nothing was executed.** Everything below is evidence *about the code*, which is not evidence that the code works. **Status moves: 0.**

**Reuse-first:** the graph holds **nothing** on evaluation harnesses, design-of-experiments, or measurement infrastructure. Top semantic score against "design-of-experiments evaluation harness ANOVA agent stacks" was **0.37**, and it was Sourcegraph Amp. `retort` appears nowhere in `wfh-005`'s five scout files or `themes.md`. **NEW node, `grade:claimed`.**

---

## 0. Headline

**Retort is real, unusually honest, and almost entirely orthogonal to this theme.** It is a design-of-experiments harness for measuring coding stacks, not a workflow harness for governing agents. It bears on the two surviving BUILD legs **not at all in mechanism** — and hard **in method**, twice, in ways that are more valuable than another prior-art hit would have been.

Three things worth the owner's time, in order:

1. **The `--routing-json` seam is not a contract.** It is a report over one man's SQLite file with a hand-curated stack list, its documented schema is already **wrong in three places** against the code it documents, it carries **no version field**, and it has **zero consumers by the author's own admission**. Anything we built on it we would be maintaining ourselves within a quarter.
2. **The statistics are honest at the module level and thin at the headline level.** The framework has residual diagnostics, credible intervals and prediction intervals. The *published routing table* is **24 of 29 records at n=1**. The project documents this against itself, in the file the leader sent the scout to read, better than the scout would have.
3. **The cold leg is the payload** (§7). Retort's five published wrong conclusions were **all** caused by a control that was set and never verified to take effect — none by an agent exceeding its authority. That is the same failure round two found in ruflo (all policy inert by default, 106 escape hatches). **Two unrelated projects, same defect: the mechanism was present and not in force.** The theme has no concern for it and neither BUILD leg detects it.

---

## 1. Built versus unbuilt in the metaharness branch

**Verdict: not a stub, and not what the README's framing implies either.** The doc is scrupulous; the *scope* is much smaller than "makes the agentic-orchestration harness a first-class design-of-experiments factor" suggests.

`docs/metaharness.md` opens by naming its own confusion — **"Three different things in this repo are called 'metaharness.'"** They are:

| # | Thing | Where | What is in the code |
|---|---|---|---|
| 1 | `metaharness` **playpen runner** | `src/retort/playpen/metaharness_runner.py` (319 lines), registered at `playpen/runner.py:200` | **Shipped and unit-tested — driving a solver that is not in this repo.** It shells out to `$METAHARNESS_SOLVER` (a Node binary) with `--lang --model --max-steps --out`. Unset ⇒ every cell returns `exit_code=1` with explanatory stderr rather than zeros |
| 2 | `retort_metaharness` **package** | top-level, console script `retort-metaharness` | **Shipped, three backends, two of which are not model measurements** |
| 3 | The **routing feed** | `reporting/optimal.py` + `retort report optimal --routing-json` | **Producer shipped and tested. Consumer: none.** §3 |

### Which claimed factors actually reach a runner

The claimed orchestration factors are `harness_config` ∈ {`base-ReAct`, `self-consistency-N`, `routed`, `+agenticow-memory`, `+darwin-evolved-genome`} and `scaffold` ∈ {`none`, `plan-and-solve`, `reflexion`}. Traced to execution across the three backends:

| Backend | What it is | Which factors reach real execution |
|---|---|---|
| `local-stub` | **A $0 deterministic fixture with no LLM in it at all.** It *fabricates* two failure modes so `diagnose` has something to classify | **None.** The doc says outright: *"It is explicitly **not** a model benchmark; never quote its numbers"* |
| `metaharness` | Shells out to `$METAHARNESS_RUNNER_CMD`; raises at construction if unset | **Unknowable from this repo.** The solver is external. Routing/memory/genome are *flags passed outward*, and nothing here can show they do anything |
| `local` | Composes retort's own pipeline in-process on Hermes + oMLX | **`base-ReAct`, `self-consistency-N`, `routed`, and all three `scaffold` levels.** `+agenticow-memory` and `+darwin-evolved-genome` are **N/A and degrade loudly to base-ReAct**, recorded in the cell's `notes` |

So of the five claimed factors: **routing, self-consistency and scaffold reach a runner** (on local models only, at $0, on a 64 GB Mac). **Memory and evolved genome reach no runner in this repository at all** — either they degrade with a printed note, or they are flags handed to a binary nobody here can inspect.

The scout checked the one thing most likely to be a silent lie, because the project's own `CLAUDE.md` warns about exactly it: the `local` backend passes the scaffold as `extra={"prompt_injection": …}`, and `_build_agent_command` reads `stack.extra["prompt"]`, a **different key**. It would have been a textbook set-but-not-verified factor. It is not one — `_build_agent_prompt` at `local_runner.py:1117` reads `stack.extra.get("prompt_injection")` through a deliberate escape hatch, commented *"for programmatic callers (e.g. the metaharness local backend injecting a scaffold)."* **The lever is wired.** Whether it *moves the model* is unverified — only that the string reaches the prompt.

### The honesty is load-bearing and should be credited

The degrade-loudly rule is stated with the right reason: *"a harness level that quietly behaves like another level would show up in the ANOVA as 'orchestration doesn't matter,' which is a **false null**."* That is a better articulation of the failure mode than anything in our own methodology, and it is the same shape as our firewall's concern — a mechanism that is present and inert produces a *confident* wrong answer, not a missing one.

### What the doc marks unbuilt

Three items, all on the routing-feed integration: **(1)** there is no `tooling: metaharness` factor level — `tooling` handles `beads` and `graphify` only; **(2)** no agreement with the metaharness maintainer on the schema; **(3)** the first factor sweep — *"does result-driven routing lower cost at equal pass-proportion? That is the question the whole integration exists to answer, and **it is unanswered**."*

**Unflattering summary: the metaharness branch is a well-built experimental apparatus whose headline hypothesis has never been tested, wired to a solver that is not in the repository, with two of its five orchestration factors unreachable and one of its three backends explicitly fictional.** All of that is disclosed by the author. None of it is hidden. It is still true.

### Name-collision discipline — and a correction to the brief

The brief said retort's `metaharness` is **not** `ruvnet/metaharness`. That is right about the code and **wrong about the relationship**, and the difference matters. The external solver retort shells out to is ruvnet's: `docs/metaharness.md` names the outstanding work as *"Agreement with the metaharness maintainer (**ruvnet**) on the schema"*, `docs/future-experiments.md` cites ruvnet's explainer site and says the local backend *"is NOT ruvnet's actual metaharness-generated harness"*, and **`ruvnet` is a contributor to this repo with 5 commits**.

> **State it this way and no other:** retort contains three things named "metaharness," **one of which is a hole shaped like ruvnet's project**. The two codebases are separate. The two *projects* are in contact, and round two's ruvnet find and this one are the same story from two ends.

**"Witness":** the word appears **nowhere** in retort — no source, no docs. No collision to propagate. Related and worth recording: retort has **no cryptographic attestation of any kind**. `provenance.json` is an unsigned self-report written by the runner about itself.

---

## 2. The conformance gate versus our firewall

**Answer: a different thing wearing similar words — and on one specific axis it is stronger than ours.**

### What is deterministic

**The mechanical gate is four lines and asserts almost nothing.** `cli._tests_did_not_run` (`cli.py:2460`) walks the score list, finds `test_coverage`, and returns `value == 0.0`. That is the whole gate. Its docstring is honest about the ambition — *"a run whose tests never executed is not a valid success: it offers no proof the code works"* — but the assertion is **"a coverage number was produced and it was not zero."** It does not check that tests *passed*, that they cover the requirement, or that they are non-trivial. The real work sits upstream in `test_coverage.py`'s `_tests_pass_rate`, which tries every runner whose project file is present and falls back to **`returncode == 0`** as *"the universal signal."*

Deterministic, and a **low bar** — this catches the catastrophic case (agent wrote nothing, tool was blocked, suite never ran) and nothing subtler.

Two other deterministic guards are better than the gate itself and are the transferable part:

- **The no-write abort.** Three consecutive runs writing zero files raises `HARNESS SUSPECTED` and **stops the whole experiment**: *"A model that can't do the task still writes something. Writing nothing, repeatedly, points at the harness — not the model."* This exists because a blocked file tool under macOS `/var/folders` silently cost **~10 experiments**; 41 of 48 runs in one were *"quietly fighting the harness."*
- **The usage-limit / tool-refusal regexes.** A run cut off by a rate limit is classified **not-attempted** rather than failed — it never got to do the work, so scoring it as a model failure would be a lie about the model.

Both are *firewall-adjacent in the direction we care about*: they refuse to record a data point whose provenance is contaminated. Neither has an analogue in our eight concerns.

### Where the LLM judgment enters — precisely

`cli._spec_conformance_passes` (`cli.py:1987`). Two passes, both LLM, both grading the same archived source:

1. **First opinion** — a judge CLI (`claude -p …` or `codex exec …`, `evaluation/judges.py`) follows the `evaluate-run` skill and writes `assessment.json` carrying `requirement_coverage` against a **pinned per-task `REQUIREMENTS.json`** so the denominator is constant.
2. **Second opinion** — *not* an independent re-roll. It is a **challenge**: `_build_challenge` hands the second pass the specific requirements the first claimed were missing, plus the first's evidence, and instructs it to go looking for the implementation.

Return contract, and it is the right shape: `True` on any single `coverage >= 1.0`; `False` only when **two real opinions both fall short**; `None` when the judge could not run — *"this keeps an infra hiccup from masquerading as a spec failure."* Only an explicit `False` fails the run.

Then a **default self-repair second chance**: a gate-failure (not a crash) is re-provisioned, re-seeded with its own code plus `FEEDBACK.md`, re-run and re-gated. A second-try pass is recorded and **flagged `_second_try` → half credit in analysis.**

### The honest statement of the limit — quoted

`README.md:65`:

> "Every run in it scores 1.00, yet they span **61× in wall clock and 29× in cost** — plus **a correctness defect the requirement checklist does not catch**."

And the sharper one, buried in a docstring at `cli.py:2005` rather than in the README:

> "measured across **22 paired reads of *identical* code, `requirement_coverage` moved by a mean of 0.18 and as much as 0.92**."

A gate whose instrument moves by 0.18 on identical input, on a metric whose pass threshold is exactly 1.00. The challenge design is a deliberate, reasoned trade against that noise — *"independence is exchanged for a targeted verification. Anchoring is the risk"* — and the author says so in the docstring rather than in the marketing. But note what it means: **the second opinion is prompted to find the implementation, and the burden of proof is placed on the claim that something is missing.** That is a design tuned to reduce **false failures**, which structurally raises the **false pass** rate. On a metric that gates every published headline, that is the direction of error you least want, and the README's own `1.00`-with-a-defect admission is what it looks like in practice.

### Is it our discipline?

**No. Different, and the two differences run in opposite directions.**

| | Our firewall (D7 / methodology §3) | Retort's conformance gate |
|---|---|---|
| What advances | A node's `grade` to `proven` | A run's `status` to `ok` |
| On what | An **attached real artifact** in `proven_by`, at the claim's altitude, **demonstrated by us** | Two LLM readings of code we generated, plus a non-zero coverage number |
| Deciding step | Human/deterministic; research moves structure, never status | **An LLM is on the deciding leg.** Unambiguously |
| Instrument noise | Not applicable — the artifact either exists or does not | **Measured at mean 0.18, max 0.92 on identical input** |
| Attestation | The artifact is the evidence | `provenance.json`, unsigned, self-reported by the runner |

Against P3's narrowing from `triage.md` §2, this lands cleanly and unfavourably: **retort puts a model call on the *deciding* leg, with a deterministic checker only *upstream* of it, not downstream.** The mechanical gate runs first and is a precondition; the LLM decides last. That is the configuration P3 says cannot carry a guarantee — and retort never claims one. It claims a **measurement**, and it publishes its instrument's error bar. That is a materially different and defensible epistemic posture, and it is not ours.

**Where it is stronger than ours, said plainly:** retort has **run its gate thousands of times and measured how much it lies.** We have run our firewall **zero times** and hold **zero `proven` nodes**. A noisy gate with a published error bar is a scientific instrument. A perfect gate that has never been used is a **posture** — which is `triage.md` §6(h)'s own conclusion, and this is a fourth independent argument for it.

---

## 3. Is `--routing-json` a real contract?

**No. It is an internal report shape, demonstrably.**

### The documented schema is already stale against the code — in three places

`docs/metaharness.md` calls itself *"Full interface spec, JSON contract."* Comparing it to `reporting/optimal.py` and the checked-in `optimal.json`:

| Item | The "contract" says | The code emits |
|---|---|---|
| Cell shape | `routes.<task>.<lang>` → `{stack, models, cost, pass, n}` | `{"cloud": {…} \| null, "local": {…} \| null}` — **an extra level of nesting** |
| Fields | five | **six** — an `effort` field the doc never mentions |
| `pass_bar` | *"1.00 for cloud, **0.50 for local**, which buys $0 at a reviewed lower bar"* | **1.00 for every stack**, with a source comment rebutting the doc: *"a stack being free is already expressed in the cost column, not by lowering the standard"* |

The function's own docstring **also** still documents the flat shape. The interface is described in two places and both are wrong, in a repo whose `CLAUDE.md` is otherwise obsessive about recording effective values.

### It has already broken once, silently, and there is a shim proving it

```python
def _best(rec, kind="cloud"):
    if kind in rec or "cloud" in rec:
        return rec.get(kind)
    return rec  # legacy flat record
```

A backward-compatibility branch for the pre-`{cloud, local}` shape — **in a producer the author states has no consumers.** The schema changed under a hypothetical consumer inside a four-month-old project.

**No `version` key. No `schema_version`. No `$schema`.** The only pin is `tests/unit/test_routing_feed.py`, which asserts the shape — and **skips entirely when `master.db` is absent**. In a fresh clone without the checked-in database, the only guard on the contract does not run.

### It is not a general facility

`DB = REPO / "master.db"` — hardcoded to **this repository's root**, a 278 KB SQLite of one author's own runs. Candidates come from **`FEATURED_STACKS`, nine entries hand-written in the source file**. The module's own docstring explains why the curation cannot be avoided: `master.db` has **no sampling or context columns** and **250+ local rows carry `model=''`**, so *"'the qualified config' cannot be filtered from the data"* — the curation exists *"until the pipeline records it."*

**Blast radius if retort refactors: total.** No version to negotiate, no consumer to break loudly, a producer keyed to a private corpus, a curated list that must be edited in Python to add a stack, and a documented shape that is already wrong. **Writing up an internal detail carefully does not make it an interface.**

---

## 4. What we would build, and what we must not rebuild

### The agent-runner abstraction, measured

`PlaypenRunner` is a `Protocol` with a three-method surface — `provision` / `execute` / `teardown` — and a `RunnerRegistry` with an entry-point plugin hook. Clean. But the six *agents* are **not** behind that abstraction. They are **six literal `if harness == "…"` branches inside `LocalRunner._build_agent_command`**, lines 789–990 of an 1,863-line file:

| Agent | Authority posture |
|---|---|
| `claude-code` | **all permission prompts disabled** |
| `hermes` | **`--yolo`** |
| `gemini` | **`--yolo --skip-trust`** |
| `omp` | self-terminates before the hard kill so output survives |
| `opencode` | `--pure` (required, else a plugin hangs) |
| `codex` | `--sandbox workspace-write` — the **only** sandboxed runner |

Each branch is 20–40 lines and each carries **a paragraph of comment recording a specific defeat**: gemini downgrades yolo in an untrusted folder and the run dies; opencode resolves its workspace from `--dir`, not cwd; hermes resolves a bare `-m` to "No LLM provider configured"; `--pure` without which a plugin hangs indefinitely. Plus a matched cross-vendor effort set (`low`…`max`) with `default` deliberately excluded because *"the two CLIs choose DIFFERENT defaults."*

**Cost of a new runner:** mechanically small — one branch, one usage parser, a model-alias row. **Honestly, days-to-weeks**, because the value is not the branch, it is the accumulated defeat log, and a new agent's defeats have not been paid for yet.

**Directly relevant to this theme, and not incidental: retort maximises agent authority on purpose.** Five of six runners disable every permission gate. That is correct for an evaluation harness — a bound is a confound; you are measuring capability, not governance. It is worth naming because it is a **live counter-example to a bounding-first framing**: here is a serious operator, 481 commits over four months, building substantial infrastructure for coding agents, whose entire eight-concern demand is *measurement and reproducibility*, and who spends a flag on removing every bound.

### Adoption surface — the number the owner decides against

| Dimension | Measured |
|---|---|
| Licence | Apache-2.0 |
| Age / activity | Created **2026-04-10**; pushed **2026-08-01**; weekly commits last 8 weeks: **53, 8, 10, 21, 10, 80, 57, 67** — very live |
| **Bus factor** | **1.** `adrianco` **481** commits, `maui314159` **7**, `ruvnet` **5** |
| Releases | **Zero releases. Zero tags.** `version = "0.1.0"`, `Development Status :: 3 - Alpha` |
| Runtime deps | **12** — click, numpy, **OApackage**, pandas, pluggy, pydantic, **pyDOE3**, pyyaml, scipy, sqlalchemy, **statsmodels**, alembic. A scientific stack, not a light one. OApackage is a compiled SWIG extension |
| Repo weight | **~45 MB**, including a checked-in **278 KB `master.db`** and a **293 KB `master.csv`** the reporting layer reads by absolute path |
| Config surface | 416-line pydantic schema; a `workspace.yaml` + `stacks.yaml` per experiment; nine hand-curated stacks in source |
| Tests | 43 unit modules + 2 integration; several **skip when `master.db` is absent** |
| Coupling | Assumes a macOS host, oMLX on port 8080 for local work, and **one experiment at a time on the machine** — a documented hard constraint, because concurrency corrupts wall-clock invisibly |
| Open issues | **1** |

**Not a library. A working laboratory, with the lab's data committed to it.** Vendoring `pricing.py` or `anova.py` is trivial; adopting `retort` means adopting the workspace model, the SQLite schema, the curation file, and someone else's macOS.

### Adopt / assemble / build — for the *evaluation* capability specifically

**ADOPT — the ideas and two files, not the product.**

*What we stop building, by name:* the second-opinion challenge gate design; the `None`-means-inconclusive tri-state that prevents an infra hiccup being recorded as a failure; the half-credit flag on a repaired pass; the no-write abort; the "record the **effective** value, not the configured one" provenance rule; the list-price-per-token normalisation in `pricing.py` (159 lines, zero retort imports, directly liftable, and it already encodes the cache-write and reasoning-token semantics we would otherwise get wrong once); and — the cheapest and highest-value item — **`CLAUDE.md`'s verify-before-you-run principle**, which is prose and free.

*Scope against our need, and the gap stated precisely:* retort answers **"which stack produces correct code most cheaply."** We need **"did this agent stay inside its authority, and can we prove it."** The overlap is one shared word — *harness* — and one shared instinct: refuse to record a result whose provenance is contaminated. **Retort measures the agent's output. Nothing in 21,000 lines observes the agent's *demand*.** That is not a gap in the eighty-percent sense; it is a different axis.

*Lock-in and exit:* lifting a module costs nothing (Apache-2.0, dependency-light at the leaf). Adopting the framework costs the macOS assumption, the one-run-at-a-time rule, the SQLite schema and the bus factor. **Exit from vendored files is free; exit from the framework is a rewrite.**

**ASSEMBLE — no.** There is nothing here to compose with `outshift-casa` or the `@claude-flow/security` policy subtree. Different plane, different question.

**BUILD — unchanged by this pass.** Retort does not touch either surviving leg. §6.

**Against the owner's stated philosophy** — *solve only the right problems with the smallest footprint; emit into genuine infrastructure, don't rebuild it* — retort is on the wrong side of the emit/rebuild line for us. It is not infrastructure we could emit into; it is a peer laboratory with an incompatible substrate. The right-sized action is **read it, lift `pricing.py` and the gate design, and cite `CLAUDE.md`'s verification principle in our own method.** Adopting the framework would be adopting a Mac.

---

## 5. Statistical honesty

**Split verdict, and the split is the finding: the machinery is more careful than most, and the numbers that get published are thinner than the machinery deserves.**

### What is done properly

- **`analysis/residuals.py` checks the ANOVA assumptions.** Shapiro-Wilk for normality, **Levene** for homoscedasticity, **Durbin-Watson** for independence, standardised-residual outlier flagging at |z| > 3, and an `all_ok` roll-up.
- **Confidence intervals exist.** `analysis/predict.py` carries `ci_lower`/`ci_upper`; `analysis/bayesian.py` implements a Normal-Inverse-Gamma conjugate posterior with a **marginal Student-t** on μ and `credible_interval(level=0.95)`.
- **The default response transform is `log`, not identity**, with a stated rationale and a documented shift at zero.
- **`OApackage` is genuinely used** — D-optimal coordinate exchange with real `intVector`/`arraydata_t` calls, plus `pyDOE3`. Not decoration.
- **Promotion gates are configurable thresholds** on `p_value`, `posterior_confidence`, `dominated_confidence` — the screening→trial→production ladder, correctly separated.
- **`aggregate.judge_for()`** records *which judge* graded each experiment, because an unrecorded judge *"would let two experiments graded by different models be averaged into one pass-proportion with nothing to indicate it."*

### Where it is thin — at the point of publication

**1. The headline routing table is essentially unreplicated.** From the checked-in `optimal.json`, across both tasks: **29 route records — 24 at n = 1, 5 at n = 3. Zero above 3.** Every "pass 1.0" in 24 of 29 cells is **one run**. `config/schema.py` defaults `replicates: 3`; `retort_metaharness/design.py` defaults **`replicates: 1`**.

**2. Pass-proportion is a mean of a 0/1 indicator with no interval.** `AVG(CASE WHEN requirement_coverage >= 1.0 …)`. At n=1 that is a Bernoulli draw reported to two decimals. **No Wilson interval, no Clopper-Pearson, no bootstrap anywhere in the codebase.**

**3. The selection rule is cost-argmin over unreplicated means.** `per_language_routing` sorts by `(cost, -n)` — so `n` breaks *exact float ties only*, which is approximately never. **A lucky cheap run wins a route.**

**4. `significance=0.10` is the default** — defensible for screening, generous for a headline, not flagged as screening-only at the call site.

**5. Binary responses through OLS.** `requirement_coverage` in `aggregate.RESPONSES` fed to `ols(...)` + `anova_lm(typ=2)` is a linear probability model — heteroscedastic by construction, which is precisely what `residuals.levene_p` would flag, in a module the reporting path does not invoke.

### The part that changes the verdict

**Retort states limitation 1 against itself, in `docs/metaharness.md`, more sharply than the scout would have.** A boxed warning — *"⚠️ Known limitation: the selection is cheapest-qualifying, and does not weight by `n`"* — with a **worked live example**: one cell routes to Opus 5 at $2.55 (n=1), a run that took 5.7 minutes against that stack's 43.8-minute average — *"a tail outlier"* — while Fable 5 clears the same cell at **n=3, mean ~$9.50**, *"weaker on the metric being sorted, far stronger as evidence."* It then **declines the obvious fix and says why**: requiring n≥3 *"would return `null` almost everywhere and be less useful, not more. The honest fix is more replicates."* And it names a worked failure: **exp-47, an n=3 result that did not survive n=5.**

The `routing_config` payload ships the caveat **inside the JSON**, in a `notes` block.

**So: the framework's statistics are sound; the corpus is too small; the author knows, measures it, publishes the caveat in the data itself, and refuses the cosmetic fix.** A design-of-experiments framework whose own N is too small *is* a serious finding — and the finding is **N, not integrity**.

**The one criticism that survives, and it is not small.** The caveats live in `docs/metaharness.md` and a JSON `notes` block. **The README's headline bullets do not carry them.** `README.md:72–73` states *"there is no language where Opus 5 is the necessary choice"* — a strong universal claim, resting on a table that is 24/29 single-run. The rigour is real and it is **one file away from the claims**. Anyone quoting retort's numbers — including us — will quote the README.

---

## 6. Bearing on the two surviving BUILD legs

**Leg (b) — deriving an authority bound from demand observed during execution: NO BEARING.**
**Leg (c) — monotonicity composed with an approval path whose issuer is not the principal: NO BEARING.**

The three things most likely to resemble demand-observation are all negative:

- **The per-run playpen is isolation, not a boundary.** A temp dir under `~/.retort/work` with `git init`, for **reproducibility and to stop runs contaminating each other** — not for containment. Five of six runners disable permissions. There is **no egress control, no syscall filter, no policy hook, no deny-list**. `DockerRunner` exists (211 lines) and is for environment reproducibility. **Nothing observes what the agent asked for.**
- **`provenance.json` records the *stack*, not the *demand*.** Versions, model revision hashes, sampling params, agent config, effective context length. It answers *"what was this measured on"*. It has **no record of tools invoked, files touched, or network reached**. Unsigned, written by the runner about itself. **Not an attestation.**
- **`stack.json` is the input configuration** handed to the playpen. Declared before the run, by us. **The exact declare-first assumption leg (b) exists to escape.**

The nearest thing to observed behaviour is telemetry — turns, tokens, wall-clock, peak prompt tokens, cost — which is **volume, not authority**. Retort can tell you an agent took 140 turns. It cannot tell you what it touched.

One adjacent observation, offered as a datum and not as a hit: **`retort diagnose`** classifies a failure as **HARNESS / TOOLING / GENUINE**. Structurally that is W3's promoted sleeper — *"tell you honestly which guarantees did not survive the compilation"* — implemented, shipping, and unit-tested, in the measurement domain rather than the enforcement domain. It is evidence that the sleeper's *shape* is buildable and useful, from a project with no interest in our problem. It is not prior art against it.

---

## 7. Cold leg — the assumption nobody put on the list

> **Every mechanism in this theme assumes that a declared enforcement mechanism is *in effect*. Nothing in the theme, the eight concerns, or either surviving BUILD leg detects a control that is present, configured, believed, and inert — and that is the failure mode two independent projects in this run's evidence base actually suffered.**

### The evidence, from two unrelated codebases

**Retort.** Its `CLAUDE.md` opens with one principle, ahead of everything else:

> "**Before starting any full experiment, RECORD every tuning parameter and VERIFY each one actually takes effect with a smoke test. A parameter set-but-not-verified is worse than none — it produces confident, wrong results.** Nearly every wrong conclusion this project has published came from a tuning parameter that was set-but-not-verified, or never recorded at all."

Five worked examples follow, each a published wrong answer: `temperature=1.0` unrecorded (oMLX's default — *"the 35B scores 0.38" really meant "0.38 at temp 1.0"*); playpens under `/var` where the file tool was silently refused, producing a false zero **read as a capability wall**; **context silently 128K while both the config file and `provenance.json` reported 262144**; `repetition_penalty` derailing the tool loop *at the value the model's own card recommended*; a compaction ceiling mistaken for a bug. The operational rule: **"'I set it' is not 'it took effect': oMLX silently STRIPS unsupported keys and IGNORES others."** And the terminal one: *"A parameter whose effect you cannot observe in a smoke test is not usable in the experiment — fix the plumbing or drop the factor."*

**ruflo** (round two, `triage-amendment-1.md` §B1). A blocking policy chokepoint on every MCP dispatch, monotone envelopes, delegation attenuation, receipts, an HMAC trust anchor — **and essentially all of it inert by default** (`mode: 'legacy'` → `enforcedOutcome: 'allowed'`), a delegation propagator with **no call sites by its own header**, and **106 audited environment-variable escape hatches**.

**These are the same defect.** One project's controls were tuning parameters, the other's were authorization gates. In both, the mechanism was present, believed, and not in force. In both, the resulting state was *indistinguishable from success*. In retort's case the mechanism was **reported as effective by the provenance file itself** — the artifact whose entire job is to record the truth said 262144 while the model ran at 131072.

### Why the theme cannot see it

Both surviving BUILD legs are blind to it by construction. **Leg (b)** derives a bound from observed demand — if the observation plane is misconfigured, it observes nothing and derives the tightest, most satisfying, most wrong bound available; a silent no-op and a perfectly compliant agent produce **identical evidence**. **Leg (c)** composes monotonicity with an approval path — if the enforcement point is in legacy mode, monotonicity holds vacuously and the approval path is never exercised. **A vacuous guarantee passes every test a non-vacuous one passes.**

And it is upstream of P3. P3's narrowing asks *is a model call on the deciding leg, is the decision monotone, how large is the exemption surface, does it fit the compliance budget.* All four presume **the decision happens**. `triage.md` §2 counts exemption surfaces — `LOG_ONLY`, `dryrun`/`warn`, `Audit`, exempt annotations, `threat-detection: false`, gh-aw #29171 — and reads them as **operator choices within a compliance budget**. Retort and ruflo say something worse: **the default was off, and nobody chose it.** An exemption surface you know about is a budget. **A default-off enforcement plane is a fiction, and this run has now found two.**

### It composes with the operation's own strongest asset

`triage.md` §2 (P5) already names the highest-signal external failure class as **fabricated success reports / deception / inaccurate self-reporting**, *"increasing over time,"* with **failure transparency** the required guardrail — and observes that capability gating cannot touch it, while this operation's artifact-backed proof discipline can. **This cold leg is the same failure one level down: not the agent misreporting its work, but the harness misreporting its own controls.** Retort has both a name for it (*set-but-not-verified*) and an instrument (smoke-test each lever before the grid; record the **effective** value, never the configured one; drop any factor whose effect you cannot observe).

### The concrete proposal, cheap and testable

> **An enforcement plane must be able to demonstrate, before the run it governs, that it is in force — and the artifact that records its configuration must record the *effective* value, not the declared one.**

Adapted to us: a **liveness probe per plane** — deliberately attempt one action the ceiling forbids, confirm it is refused by the plane that should refuse it, record the refusal — as a **precondition of the run**, not a post-hoc audit. Concretely: attach the probe to the BUILD's `done_when`, so *"refused by a plane the agent holds no credential for, with the refusal attested"* is preceded by *"and the plane demonstrated that refusal before the run began."* Without it, `done_when` can be satisfied by a plane that refuses everything, or by one whose enforcement was never reached.

**Cheapest falsifier, and it should be run before either BUILD leg is chartered:** take the three controls this repository already believes it has — the six factory agents' `tools:` frontmatter, `.claude/settings.json`'s permission rules, and whatever bounds the subagents actually run under — and probe whether each is **in force**. `triage.md` §6(g) already records the answer for two: **`.claude/agents/factory/*.md` carry no `tools:` frontmatter at all**, and **`.claude/settings.json` contains hooks only, with zero permission rules.** SDK issue #172 says `tools:`/`disallowedTools:` are **not enforced when the CLI spawns subagent child processes**, and wfh-004 filed that under *"switch on instead of building… one line of config."*

**Read through this cold leg, R2 is not a missing switch. It is the first confirmed instance of the defect, in our own repository.** The theme is preparing to derive authority bounds for agents while running five roles with no bound at all, under a mechanism the vendor's own tracker says would not have bound them anyway. One probe settles it, and it is the same probe as `A-3`/`A-5`.

**Cold-leg record — dry results included.** Also read: `docs/future-experiments.md`, `docs/past-experiments.md` (skimmed), `experiments/README.md` and 40+ experiment directories, `maturity-report.txt`, `skills/` (six agent skills), `tasks/registry.yaml`, `alembic.ini` and `storage/models.py`, `scheduler/{queue,budget,intake}.py`, `promotion/lifecycle.py`, `reporting/wardley.py`. **Dry on this theme:** the scheduler's `budget.py` is an *experiment* spend cap, **not** a per-agent authority budget — it does not corroborate wfh-004's cost-enforcement correction, recorded as a non-hit rather than inflated. `reporting/wardley.py` is Cockcroft-specific with no bearing. `promotion/lifecycle.py`'s screening→trial→production ladder is superficially our funnel and, read closely, is a **statistical** promotion ladder with no artifact requirement — a false cousin, flagged so nobody merges it with our firewall later.

---

## 8. Surface coverage report

**Searched:** the full clone at `e53be60a` — `docs/` (11 files), `src/retort/` (~21k lines, all of `cli.py`'s gate pipeline, the runner and scorer layers, all four `analysis/` modules, `reporting/optimal.py`, `pricing.py`, `evaluation/judges.py`, `promotion/gates.py`), the complete `retort_metaharness/` package, `tests/` inventory with targeted reads of `test_routing_feed.py`, `CLAUDE.md`, `README.md`, the checked-in `optimal.json` (parsed and counted), repo metadata via `gh api`.

**Deliberately skipped, declared as holes:**
- **The five `*-blog.md` files (~180 KB) were not read line by line.** They hold the published claims. If the leader wants the README's universal claims audited against the corpus rather than against the code, that is the file set, and it is an unspent read.
- **`master.db` was not queried directly.** The count is over `optimal.json`, the emitted artifact. A direct query would give the true replicate distribution across the whole corpus. Cheap, unspent.
- **`docs/past-experiments.md` (63 KB) skimmed, not read.**
- **The external `$METAHARNESS_SOLVER` is unreadable from here** — structurally. Everything about memory and evolved genome is therefore **unverifiable from this repository**, and was not guessed.
- **Nothing was run.** Every "shipped and tested" above means *a test file exists and asserts the behaviour*, not that it was seen to pass.
- **`maui314159`'s 7 commits and `ruvnet`'s 5 were not diffed.**

**Instrument check, against amendment §C2:** this pass was an **owner-directed single-target read**, the third consecutive verdict-relevant find to arrive that way rather than from the method. The organization-walk and low-star instruments amendment §C2 recommends were **not** available and were not improvised. Retort at 190★ would not have been reached by a mechanism-vocabulary search either — it self-describes as *"Platform Evolution Engine,"* emits none of this theme's vocabulary, and **its README does not contain the words authority, permission, or capability in our sense**. That is a **third** data point for §C2, from the opposite direction to the first two: **the incumbent arrives at four figures of stars, the research answer at two, and the adjacent-domain answer arrives under a name that shares no words with the query.**

---

## 9. Theme-revision signal (to the owner, verbatim, unsettled)

> **The theme has no concern for whether a control is in force, and two of the three serious codebases this run has read at depth were shipping controls that were not.** ruflo's enforcement was default-off with 106 escape hatches; retort's five published wrong conclusions were **every one** a parameter set and never verified, one of which was **misreported as effective by the provenance file itself**. The eight concerns can express *what the bound is* and *who enforces it*; none can express *and it was demonstrably switched on*. Both surviving BUILD legs pass every test vacuously if their plane is inert. **Recommend the theme carry effectiveness-verification as a first-class concern — a plane must demonstrate a refusal before the run it governs — and that the BUILD's `done_when` be amended to require it.** The cheapest test of the whole proposition is this repository's own three unverified controls, and `triage.md` §6(g) has already found two of them empty.

---

## 10. Citations (D14)

```yaml
- type: repo
  ref: https://github.com/adrianco/retort
  title: "retort — Platform Evolution Engine. Distill the best from the combinatorial mess."
  author: "Cockcroft; maui314159; ruvnet"
  year: 2026
  surface: active-dev
- type: docs
  ref: https://github.com/adrianco/retort/blob/main/docs/metaharness.md
  title: "Metaharness: the orchestration layer, and how Retort feeds it"
  author: "Cockcroft"
  year: 2026
  surface: active-dev
- type: docs
  ref: https://github.com/adrianco/retort/blob/main/CLAUDE.md
  title: "Working in this repo — verify tuning parameters before a full experiment"
  author: "Cockcroft"
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/adrianco/retort/blob/main/src/retort/cli.py
  title: "_spec_conformance_passes / _build_challenge / _tests_did_not_run — the two-gate conformance path"
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/adrianco/retort/blob/main/src/retort/reporting/optimal.py
  title: "per_language_routing / routing_config / FEATURED_STACKS — the routing feed producer"
  year: 2026
  surface: active-dev
- type: repo
  ref: https://github.com/adrianco/retort/blob/main/src/retort/pricing.py
  title: "Per-token cost estimation — list-price normalisation across metered stacks"
  year: 2026
  surface: active-dev
```

**Not cited, deliberately:** the external `$METAHARNESS_SOLVER`, ruvnet's metaharness explainer site (reached only via a URL inside retort's docs, **unverified** — must not enter any `cites:` field until fetched), and any figure from the `*-blog.md` files, which were not read.

---

## Compact list

| Find | Lens | New/known | Buy-before-build evidence |
|---|---|---|---|
| `adrianco/retort` — DoE harness for coding stacks | **IN, weakly** — a workflow harness by structure, not by purpose; measures agents, does not govern them | **NEW** (graph top score 0.37, absent from all 5 scout files) | **Yes** — §4, full adoption surface |
| `retort_metaharness` — orchestration as a DoE factor | IN | NEW | Yes — §1; 2 of 5 factors reach no runner |
| The `--routing-json` feed | **OUT** as a contract | NEW | **Yes, negative** — §3; not an interface |
| `pricing.py` | IN, narrow | NEW | **ADOPT by vendoring** — 159 lines, no retort imports |
| `retort diagnose` HARNESS/TOOLING/GENUINE | IN | NEW | Shape-evidence for W3's promoted sleeper |
| **Cold leg — the inert-control assumption** | IN, **upstream of both BUILD legs** | **NEW position** | §7; falsifier is in-repo and costs one probe |

## Flags

1. **Correction to the brief.** retort's metaharness and ruvnet's are separate **codebases** in **contact** — ruvnet is a retort contributor (5 commits) and named in the doc as the schema counterparty. Say "three things in retort are called metaharness, one of which is a hole shaped like ruvnet's project." Do not say they are unrelated.
2. **"Witness" is absent from retort.** No new collision. Related: **retort has no attestation of any kind**; `provenance.json` is an unsigned self-report.
3. **Suspected alias, for distillation.** `promotion/lifecycle.py`'s screening→trial→production ladder will read to a merger as our funnel. **It is not** — no artifact requirement. Do not merge it with the firewall.
4. **Quotation hazard.** Retort's caveats live in `docs/` and a JSON `notes` block; the README's headline claims do not carry them. **Any retort figure we cite must carry `n`.** 24 of 29 published route records are n=1.
5. **P4 routing: unchanged.** P2, P3, P5: unchanged by this pass. The two BUILD legs: unchanged. The only thing this pass moves is the **cold-leg position** and the **method finding** in §8.
6. **Everything here is `grade:claimed`.** None of it was run.
