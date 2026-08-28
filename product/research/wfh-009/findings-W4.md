# wfh-009 — findings W4: agent state, coordination, and introspection signals

**Run:** `wfh-009` · [Issue #67](https://github.com/dug-21/arch-research/issues/67) · **Workstream:** W4
**Role:** `factory-researcher` (read-only; wrote no Unimatrix node, made no git commit)
**Target pin:** `ruvnet/metaharness` @ `6f8c60216f47eac391a076fe27fd804470a07e10`
**Pin confirmed by me:** `git -C /tmp/wfh-008-metaharness rev-parse HEAD` → `6f8c60216f47eac391a076fe27fd804470a07e10` ✔
**Envelope:** static reading only. Nothing installed, built, tested, generated, served, containerised or
model-run. **Nothing in this file is demonstrated-by-us evidence; nothing here reaches `partial` or
`proven`.**

**Path convention:** every citation is relative to the MetaHarness checkout root
(`/tmp/wfh-008-metaharness`), e.g. `packages/workspace-lens/src/decision.ts:20-22`.

**Evidence labels (C3), used on every material statement:** `[SC]` source claim (README, manifest
`description`, comment, name, marketing assertion) · `[SCE]` static code evidence (a traced authored or
configured path) · `[PDE]` prior demonstrated evidence · `[UI]` unverified-inference.

**W4's question.** *How is agent state versioned, shared between agents, and made observable — and can
any of it be stated without the upstream packages that supply it?*

**Headline answer, stated before the detail.** In all five assigned packages, **agent state is versioned
and observed nowhere in the package**. Every one of the five is a pure in-memory computation over
caller-supplied data: across the five `src/` trees there is **not one filesystem write, not one database,
not one signature, and exactly one cryptographic call** (a `sha256` of a prompt string). Persistence,
custody and binding-to-a-run are delegated wholly to the caller or to an optional native peer. That is
the single most consequential structural fact in my set, it is what the custody predicate keeps catching,
and it is a **positive** finding for C2: mechanisms that store nothing are trivially free of ecosystem
state namespaces.

---

## 0. Alphabet declaration (C6, binding — `#323`)

**I swept the question set, not the answer set.** The question W4 owns is *what state is written, by whom,
where does it land, and who can read or forge it*. I enumerated **state-affecting primitives**, not
"observability features already named". The alphabet is four nested rules, each a runnable command.

### A0 — package ownership (given by the partition, not chosen by me)

```
packages/{jujutsu,radio,workspace-lens,workspace-probe,aws-finops}
```
Tier 1: `jujutsu`, `radio`, `workspace-lens`, `workspace-probe`. Tier 2: `aws-finops` (`by-exception`, §6).

### A1 — the manifest self-statement of each package

```
python3 -c "import json;m=json.load(open('<pkg>/package.json'));print(m)"
```
Fields read on all five: `name version private description main types bin files exports
dependencies devDependencies peerDependencies scripts`. **Not expressible in A1:** any coupling not
declared in a manifest — which is exactly the C2 trap, and A1 in fact missed one (§4.5).

### A2 — the state-primitive census (the load-bearing rule)

Run over `--include=*.ts --include=*.mjs`, excluding `dist/` and `node_modules/`, across all five
packages. Seven disjoint sub-alphabets, one per way state can be created, moved or attested:

| # | what it enumerates | pattern |
|---|---|---|
| A2a | filesystem writes | `writeFile\|appendFile\|mkdir\|createWriteStream\|rmSync\|unlinkSync\|renameSync\|copyFile\|writeFileSync` |
| A2b | process spawn / exec | `execFile\|spawn\(\|spawnSync\|exec\(\|child_process` |
| A2c | network egress | `fetch\(\|fetchImpl\|node:http\|WebSocket\|net\.\|dgram\|axios\|undici` |
| A2d | environment reads | `process\.env` |
| A2e | crypto / identity / signing | `createHash\|createHmac\|node:crypto\|randomUUID\|generateKeyPair\|\bsign\(\|verify\(` |
| A2f | module-level mutable caches | `^(let\|const) _\|WeakMap\|new Map\(\)\|^let ` |
| A2g | dynamic import / require | `await import\|import\(\|createRequire\|require_\(` |

**A2 result (the sweep is not "dry" — it returned a small, complete, surprising set):**

- **A2a — zero `src/` writes in all five packages.** Every hit is in `bench/`, `scripts/` or `__tests__/`
  (`packages/radio/scripts/flywheel-radio.mjs:186-188`, `packages/aws-finops/bench/real-oracle.mjs:202`,
  `packages/workspace-lens/bench/detect-concepts-throughput.mjs:109`). `[SCE]`
- **A2b — three exec sites in `src/`**: `packages/jujutsu/src/capability.ts:109`,
  `packages/aws-finops/src/binaries.ts:12`, plus `aws-finops/bench/real-oracle.mjs` (bench only). All
  three are `--version`-shaped capability checks (§4.4). `[SCE]`
- **A2c — one egress surface**: `packages/workspace-lens/src/lens.ts:41-62` (`fromUrl` / `fromRegistry`).
  **No endpoint is hardcoded anywhere in the five packages**; `baseUrl` and `fetchImpl` are both caller
  parameters. `[SCE]`
- **A2d — three env reads, all in one package**: `INFRACOST_BIN` / `CHECKOV_BIN` / `TERRAFORM_BIN`
  (`packages/aws-finops/src/binaries.ts:19-27`). **No `RUFLO_*` or any branded namespace in any of the
  five.** `[SCE]`
- **A2e — exactly one crypto call in the entire W4 set**: `createHash('sha256')` at
  `packages/workspace-lens/src/receipt.ts:8,28`. **Zero signing, zero verification, zero keys.** `[SCE]`
- **A2f — four module-level caches**: `packages/jujutsu/src/loader.ts:11,13` (peer-module handles),
  `packages/workspace-lens/src/safety.ts:23` (`WeakMap` concept-norm cache),
  `packages/radio/src/sim.ts:531`. None persists across a process. `[SCE]`
- **A2g — one non-literal dynamic import**: `packages/jujutsu/src/loader.ts:41-42` (`const spec =
  'agenticow'; import(spec)`), deliberately non-static so an absent optional peer does not break
  resolution. `[SCE]`

### A3 — the ecosystem-coupling census (C2 support, at string altitude only)

```
grep -rniE "ruflo|claude-flow|agentic-flow|ruvector|rvf-node|RUFLO_|@ruvnet" \
  --include=*.ts --include=*.mjs --include=*.md --include=*.json \
  packages/{jujutsu,radio,workspace-lens,workspace-probe,aws-finops} | grep -v node_modules | grep -v /dist/
```
**Result: 13 hits, all in `jujutsu`, all naming RuVector/`@ruvector/rvf-node` in connection with one
sub-mechanism (§6.1). Zero `ruflo`, zero `claude-flow`, zero `agentic-flow`, zero `RUFLO_*`, zero
`@ruvnet` in all five packages.** `[SCE]`
**A3 is evidence, not the C2 test.** Every C2 verdict below is argued at mechanism level; A3 only tells me
where to look.

### What this alphabet cannot see — stated, not implied

1. **Anything in `dist/`.** I read `src/`, `bin/`, `scripts/`, `bench/`, `__tests__/`, `README.md` and
   `package.json`. I did not read a single compiled artifact.
2. **Anything the optional peers do.** `agentic-jujutsu` and `agenticow` are not installed in the
   checkout; their behaviour is entirely outside my alphabet, and every statement about them here is `[SC]`.
3. **Native/N-API behaviour.** `JjWrapper` and `QuantumSigner` are opaque bindings; I read only the
   structural interface MetaHarness declares for them (`packages/jujutsu/src/capability.ts:26-53`).
4. **Runtime.** A2 establishes that a write/exec/fetch site *exists and looks reachable*. It establishes
   nothing about whether any of it executes, ever.
5. **Registry state.** Whether any of these packages is actually published requires a network fetch this
   envelope forbids (§4.6).
6. **Out-of-repo consumers.** An importer outside this repository is structurally invisible.
7. **Semantic aliasing.** A2 is a lexical census. A state write performed through an indirection my
   patterns do not name (a helper re-exported under another name, an FS call reached through a peer) is
   out of view. This is the residual `#323` risk and I do not claim it is empty.

---

## 1. Coverage — one row per package, one verdict each (C6)

| # | package | tier | verdict | detail |
|---|---|---|---|---|
| 1 | `jujutsu` | 1 | **concept found**, with a **scoped** `disqualified by ecosystem coupling` on one sub-mechanism | Concept **C-3** (dual-plane paired-verb state) qualifies at mechanism level. The **accelerated cross-branch ANN** sub-mechanism is disqualified — upstream **RuVector** (`@ruvector/rvf-node`, "RuVector PR #617/#618") reached via `agenticow`. Mechanism-level reason in §6.1. |
| 2 | `radio` | 1 | **concept found** | Concepts **C-6** (driver-held work-unit meter) and **C-7** (disclosure-fed awareness is not observation). Also the site of the artifact evidencing **C-1**. |
| 3 | `workspace-lens` | 1 | **concept found** | Concepts **C-1** (instrument identity pinned in the receipt) and **C-2** (absence of observation is a denial clause). |
| 4 | `workspace-probe` | 1 | **concept found** | Concepts **C-4** (process-regression veto) and **C-5** (veto-only auxiliary channel). |
| 5 | `aws-finops` | 2 | **concept found — handed to W1** | Assigned to W4 `by-exception` (§6.3). Mechanism is promotion-gate family, as the scope gate predicted. I did **not** re-derive W1's ground; I contribute one custody verdict and one corroborating instance of **C-2**, and hand the rest to W1. |

**Tier-1 coverage: 4 / 4 owned, each by exactly one row with one verdict. Tier-2: 1 / 1 owned (non-binding).**
No package in my list is silent.

---

## 2. Concept register — 7 concepts, 7 fields each

Grades checked against the live graph, read via
`context_graph(mode:"current", id:<N>, detail:"full", agent_id:"factory-researcher")` for
**#200, #277, #316, #317, #318, #319, #323, #324, #325, #326** — all ten read in full before grading.

---

### C-1 — Pin the judging instrument by **identity inside the artifact it judged**

| field | content |
|---|---|
| **Concept** | A verdict record carries the **identity of the instrument and the rule that produced it**, as first-class fields, not as configuration alongside it: the receipt names the measuring artifact (`lensId`, `modelId`) and the promotion record names a hash of the gate that ruled (`gate_fingerprint`). A later reader can then answer *"were these two results judged by the same rule?"* without trusting anybody's account of the run. |
| **Why it matters** | Enforcement outside the governed party's reach needs two separable properties: the *input* must not be authorable by the governed party (already held at `#319` §4), and the **rule must not be quietly swapped between the run and the review**. Without a rule fingerprint, moving the goalposts is undetectable *even when every input is honest* — the whole record set silently changes meaning. This is the missing second half of gate-input independence. |
| **How it would be used** | Every artifact the queen accepts as evidence carries `{instrument_id, rule_fingerprint}`. The verifier's admission rule becomes: *reject evidence whose rule fingerprint is not the one currently in force, or whose instrument id is not on the enforcing plane's allow-list.* A promotion chain is then auditable by fingerprint grouping alone; a batch judged under a changed gate segregates itself. |
| **Novelty** | **`new`.** Nearest neighbours, checked and rejected: `#200` holds *policy state anchored outside the workspace by an HMAC* — that is integrity of the policy **store**, not identity of the rule recorded in the **outcome**. `#316` holds *immutable generation envelopes closed only after all post-processing* — closure of **inputs**, not of the judging rule. `#316`/`#319` hold *pre-operation decision separated from post-operation receipt* — separation, not instrument identity. No node holds "the rule's fingerprint travels inside the judged record." |
| **Custody verdict** | **Concept: passes** — an identity field the governed party cannot forge *if the enforcing plane computes it*. **As implemented: fails on custody.** `gate_fingerprint` and `makeSigner()` are both produced inside the same process that runs the evaluation (`packages/radio/scripts/flywheel-radio.mjs:36-41,176`), and the fingerprint is unsigned in the committed bundle. The idea is custody-compatible; this instance does not exercise it. |
| **Evidence** | `[SCE]` `packages/radio/.radio-flywheel/replay-bundle.json` carries `gate_fingerprint: a9141969…`, `verified_improvements`, `anchor_surviving_improvements`, a 40-entry `all_commits` chain and a 3-entry promoted `chain`. `[SCE]` `packages/workspace-lens/src/types.ts:107-125` and `src/receipt.ts:52-54` place `lensId` + `modelId` in every receipt. `[SC]` the README's characterisation of the bundle as "Ed25519-signed and replay-verified" — see §4.1, the signing is not in this package. |
| **Provenance** | `radio`: **declared** — AgentRadio, `arXiv:2607.28430`, plus internal ADR-241; the fingerprint mechanism itself is `@metaharness/flywheel`'s (a **W1** package) and carries **no declared origin** here. `workspace-lens`: **declared** — Anthropic 2026-07-06, *"Verbalizable Representations Form a Global Workspace in Language Models"*, and `anthropics/jacobian-lens`; the receipt-identity construction carries no declared origin. |

---

### C-2 — Absence of observation is a **denial clause**, not a neutral

| field | content |
|---|---|
| **Concept** | Make monitoring coverage an explicit **term in the acceptance rule**, so that an unobserved action is a *rejected* action rather than an unremarked one: `accept ⟺ … ∧ coverage == 1`, and, in the second instance, *a change requiring utilisation evidence with no evidence available is rejected, never estimated*. The rule is stated positively, in the decision function, not as a warning in a log. |
| **Why it matters** | `#318` records the opposite as MetaHarness's characteristic defect — Witness "accepts absence", the sandbox returns the bare unwrapped command on a failed probe. `#319` §3 gives the fix for *capability* probes. This states the same invariant on the **evidence plane**, which is the plane a personal-OS substrate actually runs on: most of what a queen must refuse is not "the sandbox failed" but "I have no record that this happened." A substrate that treats missing telemetry as silence has an unmonitored bypass by default. |
| **How it would be used** | The queen's admission rule for any state transition includes a coverage term computed by the queen: *of the N enforcement points this action must have crossed, how many produced a record I hold?* Anything below 1 refuses, and the refusal names the missing point. Degradation is then loud by construction, and the cheapest attack (suppress the telemetry) becomes the loudest. |
| **Novelty** | **`sharpens #318`.** `#318` holds the ground negatively (absence-allows as the defect, in four subsystems) and `#319` §3 holds the positive fix for the isolation plane. This sharpens it into a general, positive admission clause on the evidence plane, and shows it appearing independently in two unrelated packages — worth recording, because it means the idea is available in the target and simply never placed under custody. |
| **Custody verdict** | **Fails on input, in both instances, and the failure is total.** `receiptCoverage` is a plain `number` field on `DecisionInput` (`packages/workspace-lens/src/types.ts:133-134`), supplied by the caller — the README's own example hardcodes `receiptCoverage: 1` (`README.md:86`). The clause reading *"not every decision was witnessed"* is therefore decided on a number the governed party types. This is **structurally identical to `no-bypass-sandbox` deciding on `CandidateChange.bypassesSandbox`** (`#318`, `#319` §4). Same in the second instance: `input.utilization` is a caller-supplied map (`packages/aws-finops/src/oracle.ts:54-61`). |
| **Evidence** | `[SCE]` `packages/workspace-lens/src/decision.ts:20-22` — `if (input.receiptCoverage !== 1) reasons.push('receipt coverage … != 1 (not every decision was witnessed)')`. `[SCE]` `packages/aws-finops/src/oracle.ts:54-61` — `REJECT evidence: rightsizing requires CloudWatch utilization data (none available)`. `[SC]` `packages/aws-finops/README.md:31-33` "absent evidence ⇒ reject (never guess)". |
| **Provenance** | `workspace-lens`: **declared** (Anthropic 2026-07-06) for the lens, **none declared** for the decision rule. `aws-finops`: **declared internal** — ADR-168, deriving from ADR-155/ADR-167 ("Darwin Shield"), and ADR-166 for the human review gate. No third-party origin declared for either instance of this clause. |

---

### C-3 — Paired-plane state: an agent's **memory branch and action branch move as one verb**

| field | content |
|---|---|
| **Concept** | Treat an agent's *record of what it did* and its *learned state derived from doing it* as one versioned unit with four verbs — **spawn / learn / revert / merge** — such that no verb can touch one plane without the other. The failure it prevents is stated crisply by the target itself: *"you can revert the code but keep poisoned memory, or promote a memory delta whose ops you abandoned."* The bridge holds only **abstract ports** (`spawn/recordOp/finalize/opSequence/undo/merge` and `branch/ingest/checkpoint/rollback/promote/diff`), so either plane can be any implementation. |
| **Why it matters** | This is a custody problem wearing a consistency costume. If a rollback reaches the action log but not the derived state, **the governed party keeps state it was supposed to lose** — including whatever it learned from an action the enforcement plane retracted. For a substrate whose whole premise is that enforcement lives outside the governed party's reach, a retraction the governed party can partially survive is not a retraction. |
| **How it would be used** | Each agent run gets a branch pair: a VCS branch (git is sufficient — no exotic VCS required) and a copy-on-write branch of whatever knowledge store the agent writes to. `revert` drops both; `merge` promotes both; a partial promotion is refused. The queen holds the branch handles, not the agent. |
| **Novelty** | **`new`.** No node holds *"an agent's derived memory must be versioned in lockstep with its operation history."* `#316`'s *definitions separated from events/evidence* is a different axis (separation of stores, not lockstep of lifecycles). `#200`'s monotone delegation and `#277`'s plane-per-leg map are about authority, not about state retraction reaching every plane. Nothing collides. |
| **Custody verdict** | **Not control-shaped** as a mechanism — but it has a direct custody *consequence*: a rollback that does not reach the memory plane leaves un-retracted derived state inside the governed party. **And the implementation does not deliver the property it exists for.** `spawn`/`revert`/`merge` are sequential `await`s with no transaction, no compensation and no consistency check (`packages/jujutsu/src/bridge/bridge.ts:78-141`); if the second plane throws, the first stays advanced. Worse, an *absent* plane is silently skipped — `const op = this.opProvider.available ? await this.opProvider.spawn(agentId) : null` (`:82-83`) — so a one-plane run proceeds under the name of a two-plane guarantee. **Take the concept with the counter-lesson: a pairing that is not a transaction is a naming convention.** Credit where due: unlike `#318`'s sandbox, the degraded mode *is* visible in the result (`status()` at `:69-75`, `opPlane`/`memPlane` on `LearnResult` at `:44-45`) — this package gets degraded-mode truthfulness right and fail-closed wrong. |
| **Evidence** | `[SCE]` `packages/jujutsu/src/bridge/bridge.ts:78-141` (the four verbs, non-transactional, plane-optional); `packages/jujutsu/src/bridge/ports.ts:25-86` (the abstract ports — the reason C2 passes, §6.1). `[SC]` `packages/jujutsu/README.md:19-24` ("used separately they drift"), `:92-99` (the 1:1 lifecycle table), `:113-114` ("verified end-to-end with jj 0.35.0 bookmarks + agenticow COW" — the owner's claim, not demonstration by us). |
| **Provenance** | **Declared, densely** — `agentic-jujutsu` (npm) and `agenticow` (npm) as optional peers; `jj`/Jujutsu (an established third-party VCS, **not** a ruvnet product) as the op-log substrate; and named prior systems **QuantumDAG**, **ReasoningBank** and **ML-DSA** signing, all `[SC]` from the manifest `description` and README. Internal: ADR-150 (removable augmentation), ADR-202 (the bridge). No paper is cited. |

---

### C-4 — Reject an improvement whose **internal process degraded**, even when the outcome improved

| field | content |
|---|---|
| **Concept** | When a self-improvement loop optimises a proxy metric, judge each candidate on **two** observables: the outcome metric *and* a second, structurally harder-to-game signal drawn from how the outcome was produced. A candidate that raises the outcome while degrading the process signal is **rejected as structurally brittle**, on the theory that it found the metric rather than the task. The target's slogan for it is exact: *"final answer up, workspace grip down."* |
| **Why it matters** | A self-improving harness whose only judge is its own score function will eventually optimise the judge. The theme's substrate must run an improvement loop it cannot itself corrupt; a second observable the optimiser does not directly author is the cheapest structural defence available, and it is the difference between "the gate is hard to pass" and "the gate is hard to *fool*". It generalises far beyond LLM internals — the process signal can be a syscall trace, a step count, a tool-call shape, a diff shape. |
| **How it would be used** | Every candidate change to the queen's own workflow is scored twice: against the task suite, and against a process fingerprint of the runs that produced those scores. Promotion requires *outcome not worse* **and** *process not worse by more than a declared tolerance*. The tolerances are declared up front and fingerprinted per C-1, so relaxing them is itself a visible act. |
| **Novelty** | **`new`.** Checked against all ten nodes. `#316`'s portable-concept list and `#319`'s TAKE list contain nothing about proxy-metric overfitting or dual-observable promotion. `#200` holds envelope monotonicity, not evaluation integrity. The closest thing in the graph is `#319` §4's "derive gate inputs from what the proposer cannot author", which is about *authorship of the input*; this is about *what the input measures* — that a second observable should be about the process rather than the result. |
| **Custody verdict** | **Control-shaped. Fails on input custody and on call-site enumeration, as implemented.** `gradeMutationByWorkspace(baselineReceipts, mutantReceipts)` takes two plain JSON arrays (`packages/workspace-probe/src/probe.ts:108-134`); the CLI reads them from two caller-named files (`src/cli.ts:70-75`). Nothing binds a receipt to a run: no run id, no output hash, no signature, no completeness proof — so a set can be fabricated, truncated or cherry-picked without detection. **And nothing forces the call** — the function has no in-repo caller outside its own package's tests, README, demo and CLI (§4.2). **However, the concept is custody-compatible and interestingly so** (§3): the *substance* of the signal is an observation of the run rather than a declaration about it, which is precisely the shape `#319` §4 asks for. The defect is the plumbing, not the idea. |
| **Evidence** | `[SCE]` `packages/workspace-probe/src/probe.ts:97-134` (three rejection clauses: critical-rate rise, drift rise beyond tolerance, clean-fraction drop beyond tolerance). `[SC]` manifest `description` "reject structurally-brittle prompt/policy mutations (final answer up, workspace grip down)" — **a source claim until traced; now `[SCE]` as to structure**, and still unexecuted. `[SC]` `packages/workspace-lens/README.md:144-145` for the Darwin-Mode framing. |
| **Provenance** | **Declared** — inherits `workspace-lens`'s Anthropic 2026-07-06 citation for the *lens*; internal ADR-239. **The anti-overfitting veto framing itself carries no declared origin** in either package. Recording that distinction matters: the paper is cited for the instrument, not for this use of it. |
| **Determining constraint, stated plainly** | The *instrument* here needs open-weight models with activation access (`README.md:123-129` — "fitting is external … not a closed API"). Our platform is a closed API. **The concept transfers; this instrument does not.** Any adoption must substitute a different second observable. |

---

### C-5 — A **veto-only** auxiliary channel: it may subtract from a decision, never add to it

| field | content |
|---|---|
| **Concept** | When composing two gates of unequal authority, make the auxiliary gate **structurally incapable of approving**. It emits `keep: false` with reasons, or it is silent; there is no path by which a strong auxiliary score rescues a candidate the authority gate rejected. Stated as a composition rule: *the auxiliary channel's output is intersected with the authority channel's, never unioned.* |
| **Why it matters** | This is the one place in my set where the custody predicate returns a **clean pass on the concept itself**, and the reason is worth naming: a channel that can only deny is uninteresting to attack. Compromising it buys the attacker nothing but a refusal they could have caused by doing nothing. It converts "is this signal trustworthy?" — usually unanswerable — into "does it matter if it isn't?" — usually answerable. For a substrate that must ingest signals of mixed provenance, this is how untrusted signal is admitted safely. |
| **How it would be used** | The queen ingests advisory signals of any provenance — heuristics, third-party scanners, model-produced critiques — on a channel whose only expressible verdict is *deny, with reasons*. Approval flows solely from the authority channel. Adding a new advisory source then requires no trust analysis, only a check that its wiring cannot express an approval. |
| **Novelty** | **`sharpens #200`.** `#200` holds deny precedence and monotone envelopes *within* policy evaluation. This extends the same invariant to the **composition of independent gates**, and adds the property that makes it load-bearing: the asymmetry is what lets an *untrusted* signal be safely admitted. `#200` does not say that. |
| **Custody verdict** | **Passes** — uniquely in my set. The channel's input, custody and call-site set can all sit inside the governed party and the composition is still sound, because the worst outcome an adversary can force is a denial. (A genuine *pass*, reported because the brief asked whether the more interesting result holds. It does — but note it passes by being **unable to grant**, not by being independently custodied. It is a safe way to *use* an uncustodied signal, not a substitute for custody.) |
| **Evidence** | `[SCE]` `packages/workspace-probe/src/probe.ts:105-106,118-134` — the verdict is `keep = reasons.length === 0`; there is no clause able to clear a rejection raised elsewhere. `[SC]` `src/probe.ts:105-106` and `README.md:22-23` — "This is deliberately a VETO signal … Never weakens the answer gate." Declared intent and traced structure agree here, which is not true everywhere in this package set. |
| **Provenance** | **None declared** for the composition rule. `[UI]` The same shape is declared in `turn-credit` ("advisory signals … never reverses the verifier's decision") — **W2's package**, which I have not opened; handed to the leader, not asserted (§7). |

---

### C-6 — The **work-unit meter is held by the driver**, and free operations are kept at separate call sites

| field | content |
|---|---|
| **Concept** | Two things at once. (a) **Receiving information should not cost a unit of work** — an agent folds in what arrived at its next step boundary, at zero cost, rather than spending a turn to check. (b) The accounting for what *does* cost is performed by the **driver at the call boundary**, not self-reported by the metered party — and two operations with identical effect but different cost are deliberately exposed as **two different methods**, so a protocol cannot silently conflate the accounting modes. |
| **Why it matters** | Theme hypothesis **H2** is *harness-as-observability*: the harness meters token spend and maps it onto workflow structure. That hypothesis has a custody hole nobody has named yet — **if the metered party reports its own consumption, the meter is a label** (the `#277` invariant, applied to cost). Placing the meter in the driver's loop closes it. Part (b)'s "two methods, not one flag" is the cheap trick that makes the closure auditable: a mode conflation becomes a visible call-site change instead of an argument value. |
| **How it would be used** | The queen's step loop charges the budget itself, at the point it invokes a step, and records the charge alongside the step record. Free operations (reading accumulated context, folding in results that already arrived) are separate entry points unreachable through the charging path. Budget exhaustion then becomes a fact the queen holds, not a number an agent reports. |
| **Novelty** | **`sharpens #200`.** `#200` holds *pre-dispatch cost and token bounds … pre-authorised spend per unit of work*, and records that pre-authorised spend was "shipped nowhere". This sharpens it on the axis `#200` leaves open: **who defines and charges the unit**. The bound is held; the custody of the meter is not. |
| **Custody verdict** | **Passes.** The driver increments `steps[a.name]` at the two points it invokes the agent (`packages/radio/src/protocol.ts:312-313,318-319`); the agent's own hooks return work products and cannot write the counter. The metered party is downstream of the meter. Second clean pass in my set, and a stronger one than C-5 because it passes on custody rather than on harmlessness. |
| **Evidence** | `[SCE]` `packages/radio/src/watcher.ts:44-52` (`fold()` — a cursor advance over a range query, no cost) and `:58-60` (`blockingReceive()` returns `this.fold()` — **behaviourally identical**; the entire difference is that the driver charges a step for it). `[SCE]` `packages/radio/src/protocol.ts:301-319`. `[SC]` `src/watcher.ts:54-57` "Kept deliberately as a separate method so a protocol cannot silently mix the two accounting modes." **Honest reading:** the bus does not *enforce* the charge; the driver applies it by convention. The custody property comes from the driver holding the counter, not from the bus refusing an uncharged read. |
| **Provenance** | **Declared** — AgentRadio, `arXiv:2607.28430`, plus internal ADR-241, for the passive-awareness primitive. `[UI]` The underlying construction (append-only log, monotonic sequence number, per-consumer cursor, no wall clock) is standard distributed-systems prior art and carries **no declared origin** here; flagged as a caution against citing MetaHarness for it. I read no literature to establish this. |

---

### C-7 — **Disclosure-fed awareness is not observation**, and cannot carry an enforcement input

| field | content |
|---|---|
| **Concept** | A shared channel whose entire content is authored by the participants being coordinated is a **disclosure** channel, not an **observation** channel. It tells you what parties chose to say, never what they did. The design consequence is a hard partition: such a channel may inform coordination, and may never be an input to a control. The target states the bound honestly in its own words — *"visibility is not synthesis"*, and *"the bus only carries what some agent chose to post."* |
| **Why it matters** | The theme's `canvas` layer is *"a view over a reference seam"*, and H1/H2 both want the coordination structure to double as the live debugger. This concept names the exact failure that architecture invites: **a debugger fed by the debugged party's own posts looks like observability and is not** — and once it looks like observability, someone will hang a gate on it. Naming the partition up front is cheaper than discovering it after a gate has been built on a disclosure feed. |
| **How it would be used** | Two visually similar but formally separate feeds into the canvas: a **disclosure** feed (agent-authored messages, findings, self-reports) rendered as claims with an author, and an **observation** feed (harness-captured facts: step charges, tool invocations, exit codes, diffs) rendered as facts. Enforcement inputs may be drawn only from the second. The rendering difference is a UI decision; the admission rule is the mechanism. |
| **Novelty** | **`sharpens #277`.** `#277` holds *attribution is persisted self-assertion, not attestation, so it cannot authorize* — the same invariant, at the level of **identity**. This carries it to the level of **content**, and to a channel type (inter-agent coordination bus) the theme is actively considering building. |
| **Custody verdict** | **Fails on input, by construction — and the package says so.** Every message on the bus is produced by an agent calling `send()` (`packages/radio/src/bus.ts:49-64`); nothing derives from observation. The driver deliberately **never filters or ranks** mentions (`src/protocol.ts:31-35`), so relevance is entirely the sender's assertion. The instrument's catch here is not a defect finding against the package — the package makes no control claim — it is a **boundary result**: this channel type can never be promoted to an enforcement input, and no amount of hardening changes that. |
| **Evidence** | `[SCE]` `packages/radio/src/bus.ts:49-64`, `src/watcher.ts:41-52`. `[SC]` `packages/radio/src/protocol.ts:27-40` — the two "KNOWN FAILURE MODES the driver deliberately keeps visible": mentions can derail (the cited paper's accounting: 47 rubrics gained, 23 lost), and "the bus only carries what some agent chose to post … visibility is not synthesis." `[SC]` `src/sim.ts:130-136` repeats the second bound for the simulator. |
| **Provenance** | **Declared** — AgentRadio, `arXiv:2607.28430`; the derailment figures (47/23) are attributed to that paper `[SC]` and I did **not** read it. Also declared in `radio`: `arXiv:2510.01285`, `arXiv:2507.01701`, `arXiv:2502.14321`, `arXiv:2606.05304`, and internal ADR-241. |

---

**Register tally: 7 concepts — 3 `new` (C-1, C-3, C-4) · 4 `sharpens` (C-2 → #318; C-5 → #200; C-6 → #200;
C-7 → #277) · 0 `already held`.** No concept is reported without a checked grade, and the nearest neighbour
rejected is named for each `new`.

---

## 3. The custody predicate as an instrument (C5) — what it caught, and what it did not

> *A control whose input, custody, or call-site enumeration sits inside the governed party is a label,
> not a control.*

**Run against every control-shaped mechanism in the five packages. Result: 3 catches, 2 passes,
2 not-control-shaped.**

| mechanism | verdict | the reason in one line |
|---|---|---|
| `decide()` coverage clause (`workspace-lens`) | **fails on input** | `receiptCoverage` is a number the caller types; the README hardcodes `1`. |
| `gradeMutationByWorkspace()` (`workspace-probe`) | **fails on input + call-site enumeration** | Receipt sets are unbound JSON arrays with no run id, no signature, no completeness proof; nothing forces the call. |
| `verifyProposal()` (`aws-finops`) | **fails on input** | The "deterministic execution oracle" **executes nothing** — it is a pure function over `buildOk`, `delta`, `policyBefore/After` and `utilization`, all handed in by the caller (`src/oracle.ts:32-81`). Separately, the tool the bench *does* run is chosen by `INFRACOST_BIN`/`CHECKOV_BIN`/`TERRAFORM_BIN` (`src/binaries.ts:19-27`) — the governed process picks which binary answers the oracle. |
| Veto-only composition (`workspace-probe`) | **passes** | A channel that can only deny is safe to feed with untrusted signal. Passes by *inability to grant*, not by custody. |
| Driver-held step meter (`radio`) | **passes** | The driver increments the counter; the metered party is downstream of it. |
| `DualStateBridge` verbs (`jujutsu`) | **not control-shaped** | A state-consistency mechanism — but with a custody *consequence*: a non-transactional retraction leaves un-retracted derived state inside the governed party. |
| `RadioBus` / `Watcher` (`radio`) | **not control-shaped** | Coordination only; makes no control claim. The C-7 boundary result stands on its own. |

**The sharp case the brief named, answered directly.** `workspace-probe` rejects mutations on a score
derived from `workspace-lens` receipts. *Who computes the score?* The same process that proposes the
mutation, from arrays it supplies. *Does the governed party sit upstream of the judging signal?* **Yes, in
this implementation — completely.** So the verdict is the same defect as `no-bypass-sandbox` deciding on a
proposer-supplied boolean (`#318`, `#319` §4).

**But the more interesting half is true too, and it is the substantive result.** The *substance* of the
signal is categorically better than `bypassesSandbox`. A boolean about a proposal is a **declaration**; a
workspace readout is an **observation of the run the proposal caused** — and `#319` §4 names exactly that
class ("the diff itself, static analysis of it, or the observed exec/syscall surface of the run") as the
acceptable input class. What is missing is not the *kind* of signal but three pieces of plumbing: (i) the
receipt is not bound to a run, (ii) the receipt is not signed, and (iii) the concept library and lens
artifact — **the rubric** — are caller-supplied (`src/lens.ts:29-62`, `src/receipt.ts:19-20`). Fix those
three and the same mechanism passes. **That is the useful result: the gap between a label and a control
here is custody plumbing, not signal quality.**

**One custody defect is caused by a property that is otherwise good.** `workspace-lens` deliberately
embeds **no endpoint and no registry default** (`src/lens.ts:49-62`, "Keeps the package free of any
assumed/embedded endpoint") — exactly what C2 wants, and exactly what removes custody of the instrument.
**Portability of an instrument and custody of an instrument pull in opposite directions.** C-1 is the
resolution: pin the instrument by *identity recorded in the output* rather than by *location fixed in
config*, and you get both.

---

## 4. Verification by fact, not by adjacency (`#324`)

`workspace-lens` and `workspace-probe` are the paired set `#324` warns about, so I audited **by fact**:
each fact below was grepped across all five packages at once and ruled on in one pass, rather than
verified in one package and allowed to vouch for its neighbour.

### 4.1 The three cryptographic claims — one grep, one ruling

Three packages make cryptographic-sounding claims:
- `workspace-lens`: "a **signable** interpretability receipt" (manifest `description`; `README.md:6,48`;
  `src/types.ts:5,103`). `[SC]`
- `radio`: the replay bundle is "**Ed25519-signed** and replay-verified" (`README.md:40`). `[SC]`
- `jujutsu`: "**ML-DSA** signing", "Quantum signing (ML-DSA-65) is passed through" (`description`;
  `README.md:6,62`). `[SC]`

**Ruling, from alphabet A2e across all five packages at once: there is exactly one cryptographic call in
the entire W4 set — `createHash('sha256')` at `packages/workspace-lens/src/receipt.ts:8,28`. There is no
signing, no verification and no key material anywhere in these five packages.** `[SCE]`

Specifically:
- **"Signable" is an adjective, not an implementation.** `WorkspaceLensReceipt` (`src/types.ts:107-125`)
  has **no signature field**, and no function in the package signs or verifies anything. A receipt that is
  *signable* is not a receipt anyone has signed — and, as the brief notes, a signed receipt is still not a
  receipt verified by anyone. Two gaps, not one.
- **`radio` signs nothing.** `makeSigner()` and `verifyReplayBundle()` are imported from
  `@metaharness/flywheel` (a **W1** package) via a relative path into a sibling's build output
  (`scripts/flywheel-radio.mjs:36-41`). The claim is about flywheel's machinery, not radio's.
- **`jujutsu` signs nothing.** `quantumSigner()` returns the optional peer's class or `null`
  (`src/capability.ts:213-215`); with the peer absent — its state in this checkout — it returns `null`.

**This is the C3 firewall working as intended.** Three source claims, zero implementations in the packages
that make them, caught by one grep over the whole set rather than by reading one package carefully and
trusting its neighbour.

### 4.2 `workspace-probe` is not wired to Darwin Mode

`[SCE]` `workspaceProbeScore`, `gradeMutationByWorkspace` and `decide` have **no in-repo caller outside
their own package's tests, README, demo and CLI**. `packages/darwin-mode` contains its own, unrelated
`buildReceipt` and `decide` functions in `bench/swebench/` — a **name collision**, not a call site. The
"Darwin-Mode bridge" in the manifest `description` is a `[SC]` statement of intent; the static path does
not exist at this commit. Anyone grepping by function name would conflate the two.

### 4.3 The `radio` README is contradicted by `radio`'s own committed artifact

`[SC]` `README.md:40-42`: "The wheel re-discovering **`passive/immediate`** is the paper's ablation
direction, measured on our own machinery."
`[SCE]` `packages/radio/.radio-flywheel/tuned-policy.json`: the tuned policy is
`{mode: passive, foldEvery: "4", postPolicy: "silent", digest: "full", topology: "blackboard"}`.
**`postPolicy` is `silent`, not `immediate`.**
`[SCE]` And under `topology: blackboard` the package's own documentation states that `digest`, `foldEvery`
and `postPolicy` **have no effect** (`src/sim.ts:98-106`) — so the levers the README's claim rests on are
inert given the topology the wheel selected. The headline claim is wrong twice over.
*(The JSON is static evidence of what the repository asserts a prior run produced. It is not demonstration
by us, and I did not run the flywheel.)*

### 4.4 The "probe the real operation" concept is **not** applied across the repository

`#319` §2 records probe-the-real-operation as wfh-008's strongest single concept, and warns that an
inventory-shaped check is "a false-positive machine". My alphabet found **two counter-examples in packages
wfh-008 never opened**, both in `src/`, both named `probe`:

- `packages/jujutsu/src/capability.ts:106-114` — `resolveJjCli()` returns true on `existsSync(jjPath)` or
  a successful `jj --version`, with `stdio: 'ignore'`. It never rehearses a jj operation, and it
  **discards the version string it just asked for** — while the package's own README documents a failure
  caused by exactly a version mismatch (`README.md:132-138`: upstream calls the `jj branch` subcommand
  removed in jj ≥ 0.21). The check cannot detect the failure the package knows about. `[SCE]`
- `packages/aws-finops/src/binaries.ts:10-17` — a function literally called `probe()` that runs
  `<bin> --version`. `[SCE]`

**Ruling: the good concept is not a repository-wide property of MetaHarness. It appears once
(`sandbox.ts`, per `#318`/`#319`) and its inverse appears at least twice more.** This corroborates
`#319` §2 and rebuts any inference that the pattern is systematic in the target.

### 4.5 A coupling invisible to the manifest alphabet

`[SCE]` `packages/radio/package.json` declares **no** dependency on `@metaharness/flywheel`, yet
`packages/radio/scripts/flywheel-radio.mjs:36-41` imports three symbols from `../../flywheel/dist/index.js`
— a relative path into a sibling package's build output. It is a development script, not the package's
runtime, and `radio`'s `files` list (`["dist","README.md"]`) excludes `scripts/`, so it is not packed. But
it is a real first-party edge a manifest-only sweep cannot see — a small live instance of `#323` and of
C2's "it is not only npm edges" precision.

### 4.6 Publication status — five different words, kept apart

`[SCE]` **None** of the five packages sets `private: true`. **None** of the five appears in
`scripts/publish-workspace.mjs` `RELEASE_ORDER` (which lists twelve packages, none of them mine).
Therefore, precisely: all five are **publishable-shaped and not in the repository's own release train**.
Whether any is **published** requires a registry fetch this envelope forbids and **I did not check it**.
`packed` ≠ `published` ≠ `exported` ≠ `re-exported` ≠ `reachable`, per `#324`.

### 4.7 An internal contradiction inside one package — two source claims about the same fact

`[SC]` `packages/jujutsu/src/bridge/ports.ts:12-15` and `README.md:45,118`: native ANN across the COW
boundary is "**still in flight**" / "**pending**".
`[SC]` `packages/jujutsu/src/capability.ts:81-84` and
`src/bridge/adapters/agenticow-memory-provider.ts:7-8,166`: "agenticow@0.2.0 + @ruvector/rvf-node@0.2.0 …
**recall@10 = 1.0000 verified** (1200-vector L2, efSearch=300, Jun 2026)" — i.e. shipped.
**Two source claims in one package contradict each other about the same capability, in files two
directories apart.** Neither is demonstrated by us. Recorded because it is precisely the `#324` shape:
verifying either sentence would have vouched for nothing about the other.

---

## 5. Provenance — the declared-origin pattern (register field 7)

**My set has the run's highest declared-provenance density, and the pattern holds. It is worth reporting
as a finding about what MetaHarness *is*.**

| package | declared external origin | declared internal origin |
|---|---|---|
| `radio` | **AgentRadio, `arXiv:2607.28430`** (verbatim in the manifest `description`), plus `arXiv:2510.01285`, `arXiv:2507.01701`, `arXiv:2502.14321`, `arXiv:2606.05304` in `src/sim.ts` and `scripts/` — **five distinct arXiv identifiers** | ADR-241 |
| `workspace-lens` | **"Anthropic 2026-07-06, 'Verbalizable Representations Form a Global Workspace'"** (verbatim in the manifest `description`); reference implementation `anthropics/jacobian-lens`; explicit disclaimer "**not affiliated with Anthropic**" (`README.md:12`) | ADR-238 (named in `scripts/healthcheck.mjs`) |
| `jujutsu` | `agentic-jujutsu`, `agenticow`, `jj`/Jujutsu, **QuantumDAG**, **ReasoningBank**, **ML-DSA** — all named in the manifest `description` | ADR-150, ADR-202 |
| `aws-finops` | none (the *tools* — infracost, checkov, terraform — are third-party, but no method origin is claimed) | **ADR-168**, deriving from ADR-155 / ADR-167, plus ADR-166 |
| `workspace-probe` | inherits `workspace-lens`'s citation; declares no origin of its own | ADR-239 |

**The pattern, stated as a finding.** `[SCE]` **Four of my five packages declare an origin outside
themselves; three declare published third-party work; and `radio` alone cites five papers.** Across the
whole W4 set the recurring self-description is *implementation of someone else's published result*, not
*invention*. This bears directly on how the run's output should be cited: **for C-6 and C-7 the citation we
should carry is AgentRadio, not MetaHarness; for C-4's instrument it is the Anthropic result, not
MetaHarness.** Only C-1, C-3 and C-5 carry no declared upstream — and C-1's fingerprint mechanism belongs
to `flywheel`, a package I did not open.

**Boundary, held.** Recording the declared origin was in scope. **I read none of the cited papers, fetched
nothing, and verified none of the citations.** Every provenance entry above is `[SC]` — a claim the package
makes about itself. A concept graded `new` on the C4 axis may still be a well-known published result; this
table is what makes that visible, not what resolves it.

---

## 6. C2 rulings — stated at MECHANISM level, as required

**The test I applied to every concept:** *does the idea survive with ruflo, RuVector, agentic-flow, every
branded contract, every `RUFLO_*` namespace and every registry default deleted?* Not *does the manifest
name one*. Alphabet A3 (13 hits, all in `jujutsu`, all RuVector, all about one sub-mechanism) told me
where to look; it did not decide anything.

### 6.1 `jujutsu` — the one package needing a split ruling, and it is a split, not a disqualification

**Be precise about which upstream is being ruled on** — this package declares several, of different kinds.

| upstream | what it is | ruling |
|---|---|---|
| `jj` / **Jujutsu** | an established third-party VCS, **not a ruvnet product** | **Not an ecosystem coupling.** Depending on a public VCS is no different from depending on git — and C-3 does not need this one either, since the op-plane port is abstract. |
| `agentic-jujutsu` (npm) | third-party npm package, optional peer | **Not a coupling of the concept.** C-3's op plane is the `OpBranchProvider` port (`src/bridge/ports.ts:34-49`): `spawn/recordOp/finalize/opSequence/undo/merge`. Nothing in that vocabulary is branded, and the package ships mock adapters proving the bridge runs with the peer deleted (`src/bridge/adapters/mock-providers.ts`). |
| `agenticow` (npm) | third-party npm package, optional peer | **Not a coupling of the concept.** Same argument: `MemoryBranchProvider` is `branch/ingest/checkpoint/rollback/promote/diff` — implementable over any copy-on-write or snapshotting store. |
| **RuVector** (`@ruvector/rvf-node`, "RuVector PR #617/#618") | the ruvnet ecosystem | **DISQUALIFIED — for one sub-mechanism only.** |

**The mechanism-level reason for the one disqualification** (not a dependency-list reason): the
*accelerated* cross-branch ANN is not a mechanism this repository states — it is a **capability supplied
from upstream**. The interface is declared stubbed, `nativeAnn` is a boolean reporting whether the upstream
landed, and the bridge throws a message naming the upstream PR when no provider is injected
(`src/bridge/ports.ts:73-86`; `src/bridge/bridge.ts:143-163`). There is nothing here to restate as an idea
we could build: *"query fast across a copy-on-write boundary"* is a performance property of a specific
Rust index, not a portable design. **That is a coupling in disguise and it is disqualified. Named upstream:
RuVector.**

**What is not disqualified, and why the distinction matters:** the *semantic* of the query plane —
**read-through across a copy-on-write boundary with child-wins precedence** (`README.md:116-120`) — is
statable and buildable with no ruvnet code at all. Only the acceleration needs RuVector, and acceleration
is not a concept.

**Applying C2 as a manifest scan here would have disqualified the entire package** — and with it C-3, one
of the run's three `new` concepts — on the strength of thirteen comment strings about a pending PR. That is
exactly the false negative the scope warned about.

### 6.2 `radio`, `workspace-lens`, `workspace-probe` — qualified, with the reason

**Qualified.** No manifest edge, no branded contract, no env namespace, **no embedded endpoint or registry
default** in any of the three (A2c, A2d, A3). `radio`'s only first-party edge is an undeclared dev-script
import into `flywheel/dist` (§4.5), which touches the flywheel *tooling*, not C-6 or C-7. `workspace-probe`
imports `@metaharness/workspace-lens` — a **type-only** dependency (`import type { WorkspaceLensReceipt }`,
`src/probe.ts:12`); C-4 and C-5 restate cleanly as *"a second observable"* and *"a deny-only channel"* with
no reference to that package.

### 6.3 `aws-finops` — the `by-exception` assignment, recorded with my reasoning visible

**The exception is declared, not discovered.** Under the partition rule (mechanism family per the manifest
`description`), `aws-finops` reads as **W1**: "multi-tier cascade, deterministic execution oracle,
shrinking residual … only verified savings are reported, behind a human review gate" is a promotion-gate
family, not agent state, coordination or introspection. **The coordinator kept it in W4 deliberately**, on
the reasoning that a declared rule earns its value by surviving an awkward case, and that re-cutting on
judgement after the fact is precisely what the rule exists to prevent. It is Tier 2 and non-binding, so the
cost of the wrong lens is small; the cost of an unauditable partition is not.

**Mitigation, executed as instructed. I read it, confirmed the mechanism is promotion-gate-shaped, and am
handing it to W1 rather than re-deriving W1's ground.** What I kept, because it is W4-relevant and I did
the work:
- **One corroborating instance of C-2** — the evidence gate (`src/oracle.ts:53-69`), which is an
  *observability* clause living inside a promotion gate. It is the second independent appearance of
  "absence of observation denies" in my set, in a package with no code relationship to the first.
- **One custody verdict** (§3): the "deterministic execution oracle" **executes nothing** and rules on
  caller-supplied numbers; and `INFRACOST_BIN`/`CHECKOV_BIN`/`TERRAFORM_BIN` let the governed process
  choose which binary answers it.
- **One provenance row** (§5): ADR-168 ← ADR-155/167, plus ADR-166.

**Everything else in this package — the cascade, the residual, cost-per-verified-dollar, the
tier-escalation policy, the trap corpus — is W1's, and I did not analyse it.**

**C2 ruling for `aws-finops`:** qualified. Its dependencies are third-party CLI tools (terraform, checkov,
infracost); nothing ruvnet is referenced (A3: zero hits).

---

## 7. Cross-workstream handoffs — to the leader, not absorbed and not duplicated

1. **→ W1 (`flywheel`): C-1's implementing mechanism is not mine.** `gate_fingerprint`, `makeSigner()` and
   `verifyReplayBundle()` live in `@metaharness/flywheel`. I observed them only through a committed
   artifact and an undeclared dev-script import from `radio`. **W1 should rule on the mechanism itself** —
   in particular whether the gate fingerprint covers the rule or merely a config blob, and who holds the
   signing key. My C-1 is stated from the artifact and should be re-graded if W1 finds the mechanism
   different from what the artifact implies.
2. **→ W1 (`aws-finops`): the whole promotion-gate mechanism, per §6.3** — including the custody defect I
   found (a "deterministic execution oracle" that executes nothing and reads env-selected binaries), which
   W1 should weigh against `flywheel`'s and the `evals-*` adapters' gates rather than take from me in
   isolation.
3. **→ W2 (`turn-credit`): a possible convergence, flagged not asserted.** C-5 (veto-only auxiliary
   channel) may be the same shape as `turn-credit`'s declared "advisory signals … never reverses the
   verifier's decision" — which the scope gate's **Q2** already singled out as that package's interesting
   property. **I have not opened `turn-credit`.** If W2 finds the same structure, it is one concept found
   independently in two packages and the register should carry it once, not twice.
4. **→ W2 (`oo-agents`): a real first-party consumer edge into my set.** `packages/oo-agents/src/pod.ts:51-52`
   imports `runProtocol` from `@metaharness/radio`, and `scripts/build-ordered.mjs:31` orders the build
   accordingly. `oo-agents` is W2's Tier 2; **the radio protocol is a dependency of it, and I have not
   looked at what `oo-agents` does with the concepts.**
5. **→ the leader, as a target-level observation, not a concept.** §4.4's result — that
   probe-the-real-operation appears once in MetaHarness and its inverse at least twice — bears on how
   `#316`/`#319` should be read. It is corroboration of `#319` §2, not a new concept, and I am not filing
   it as a register row.

---

## 8. What I did **not** check — recorded negatively (`#324` item 3)

Stated as omissions, not as absences of findings.

1. **I did not open any package outside my five.** `flywheel`, `turn-credit`, `oo-agents` and `darwin-mode`
   are referenced above only through artifacts, imports or file names inside my own packages.
2. **I did not read any `dist/` output.** All structural claims are about `src/`, `bin/`, `scripts/`,
   `bench/`, `__tests__/`, `README.md` and `package.json`.
3. **I did not read any cited literature.** Not `arXiv:2607.28430`, not the Anthropic 2026-07-06 result,
   not the four other arXiv ids, not `anthropics/jacobian-lens`. Every provenance entry is what the package
   says about itself.
4. **I did not read the referenced ADRs.** ADR-150, ADR-166, ADR-167, ADR-168, ADR-202, ADR-238, ADR-239
   and ADR-241 all exist under `docs/adrs/` (I confirmed two filenames) — I read none of them. `docs/` is
   outside this run's alphabet.
5. **I did not check the npm registry.** Publication status of all five packages is unresolved (§4.6).
6. **I did not install, resolve or inspect `agentic-jujutsu` or `agenticow`.** Every statement about them
   is `[SC]` from MetaHarness's own text. In particular I did **not** establish who owns them, and I make
   no claim about their ownership — only about MetaHarness's declared and traced relationship to them.
7. **I did not exercise anything.** No `jj`, no `unshare`, no terraform/checkov/infracost, no flywheel run,
   no test suite, no CLI, no `smoke.mjs`, no bench. The `real-oracle.json` and `replay-bundle.json`
   receipts in the tree are the owner's prior outputs — `[SC]` about a run, never demonstration by us.
8. **I did not audit the `radio` simulator's 918 lines line-by-line.** I read its full 140-line design
   header and its bus/watcher/protocol dependencies. The staleness model, the blackboard topology and the
   digest levers are read from that header (`[SC]`), not traced through the implementation. **If a concept
   is hiding anywhere in my set, `src/sim.ts` is the most likely place**, and I am naming that gap rather
   than implying coverage.
9. **I did not verify that any traced path executes.** Static reading establishes structure and
   reachable-looking paths; it establishes nothing about runtime, on any statement in this file.
10. **My A2 alphabet is lexical.** A state write reached through an indirection my seven patterns do not
    name is out of view (§0). I do not claim the sweep is dry against a semantic instrument.

---

## 9. Firewall statement

Nothing in this file moves a status. This is directional, structure-only research at one commit under a
static instrument. No `Prerequisite`, `Cites` or `Tests` edge is proposed; no capability is advanced; no
grade past `claimed` is warranted by anything here. **The custody predicate's three catches are readings of
source, not demonstrated vulnerabilities**, and the two passes are readings of source too. Any claim that a
harvested concept *works* requires a separately approved scope building an artifact at that claim's
altitude, demonstrated and independently validated by us — and, per `#319` §7, built against our own
intended enforcement plane rather than against MetaHarness.
