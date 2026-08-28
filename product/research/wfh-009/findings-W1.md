# wfh-009 — findings W1: self-improvement and promotion gates

**Workstream question.** *What mechanism does a self-improving harness use to decide that a change earned promotion, and what part of that is statable without the model, the benchmark, or the ecosystem?*

**Target pin (confirmed by this agent):**
`git -C /tmp/wfh-008-metaharness rev-parse HEAD` → `6f8c60216f47eac391a076fe27fd804470a07e10`
(working tree clean; `git status --short` empty).

**Envelope.** Static reading only. Nothing was installed, built, tested, benchmarked, spawned, fetched or run. No registry query. **Nothing here is demonstrated-by-us evidence; nothing reaches `partial` or `proven`.** No Unimatrix node was written.

**Packages owned (9, all Tier 1):** `flywheel` · `evals-extract` · `evals-hle` · `evals-math` · `evals-servedmodel` · `evals-sql` · `evals-toolcall` · `bench` · `weight-eft`.

> **Persistence note (leader).** The authoring `factory-researcher` was blocked by the harness from writing this file directly and returned it verbatim. It is transcribed here unaltered by `research-leader`; no content was generated, summarised or edited in transit.

---

## 0. Ratified partition-rule disclosure (stated, not left for the auditor to find)

The scope's partition rule is *"mechanism family as declared by the package's own manifest `description`, and by its `README.md` where one exists."* **Six of my nine packages carry no `README.md`**, so their assignment ran on the `description` clause alone — the rule executed on one leg for two thirds of this workstream.

Verified directly [static code evidence]:

| package | `README.md` | `LICENSE` |
|---|---|---|
| `flywheel` | present | **absent** |
| `bench` | present | absent |
| `weight-eft` | present | present |
| `evals-extract` · `evals-hle` · `evals-math` · `evals-servedmodel` · `evals-sql` · `evals-toolcall` | **absent (all six)** | absent (all six) |

All six absent-README packages nonetheless declare `"files": ["dist", "README.md"]` — they enumerate a README they do not contain. The assignment stands (each `description` names a flywheel promotion gate explicitly), but it stands on one leg, and this is the same defect class `#323` names: a rule whose applicability condition is unstated cannot be audited.

**Inbound from W4 (coordinator Q1 ruling):** `aws-finops` remains in W4 `by-exception`. As of writing, W4 has handed W1 **no concept** from it. If one arrives after this file is committed it must be integrated by the leader with its origin named, not silently absorbed here.

---

## 1. My alphabet — declared before any sweep claim (`#323`, C6)

> **I enumerated over the TypeScript source of nine named package directories at one commit, classifying every *decision point* (a site that admits, rejects, drops, excludes, refuses, throws, or gates) and every *protected operation* (a site that mutates promoted state, emits a record downstream, spawns, or performs network I/O). Anything not expressible as a TypeScript source construct in those nine directories is out of my view.**

Reproducible, as run:

```bash
cd /tmp/wfh-008-metaharness/packages
P="flywheel evals-extract evals-hle evals-math evals-servedmodel evals-sql evals-toolcall bench weight-eft"

# A1 — the file alphabet (110 .ts files under src/, no node_modules, no dist)
for p in $P; do find $p/src -name '*.ts'; done

# A2 — decision-point candidate sites, swept over the QUESTION set (verbs of admission),
#      not over the answer set (names of gates already known)
grep -rnE "promot|\bgate\b|admit|accept|reject|drop|exclud|refus|throw new Error|assert|guard|verif|detect|leak|hack|drift|contaminat|eligib|significant" $P --include=*.ts

# A3 — protected operations the decisions are supposed to gate
grep -rnE "\bappend\(|writeFileSync|fetch\(|execFile|spawn\(|\.push\(commit" $P --include=*.ts

# A4 — inputs to a decision that are DEFAULTED rather than measured
grep -rnE "\?\? 0\.5|: 0\.5[,;)]|costUsd = 0;|costUsd: 0,|afterQuality: 0," $P --include=*.ts

# A5 — repository-wide fact audits (#324: audit by fact, not by location)
grep -rn "anchor:"                                   --include=*.ts --include=*.mjs .   # who populates PromotionEvidence.anchor
grep -rn "meetsPromotionRule\|runFlywheelGenerations\|verifyReplayBundle" --include=*.ts --include=*.mjs .
grep -rn "RELEASE_ORDER" -A 20 scripts/publish-workspace.mjs
```

Counts returned: A1 = **110** source files (flywheel 10, each `evals-*` 12 except `servedmodel` 9, `bench` 18, `weight-eft` 8). A2 = **859** candidate hits across the nine (flywheel 153, `bench` 126, the six `evals-*` 75–89 each, `weight-eft` 77), manually classified down. A3 = **24** sites in 10 files. A4 = **43** non-test sites.

**What this alphabet cannot see, stated as a limit not a footnote:**

- Anything reached by dynamic import, by a generated harness, or by an out-of-repo consumer.
- Anything expressed outside `.ts` — the `.mjs` drivers under `evals-math/bench/`, `evals-toolcall/experiments/` and `flywheel/scripts/` were *not* read (only grepped in A5).
- **The ADR corpus.** These nine packages reference **22 distinct ADR numbers** (`ADR-038` ×28, `ADR-037` ×25, `ADR-234` ×23, `ADR-226` ×11, `ADR-246` ×10, `ADR-040` ×9, `ADR-235` ×8, `ADR-198` ×6, `ADR-039` ×5, and 13 others once each). Those files **do exist**, at `docs/adrs/`, which is a **declared hole in this run's scope** — I did not open one. Every ADR reference below is therefore an unresolved pointer, recorded verbatim, never relied on.
- Runtime behaviour of any kind. Structure and reachable-looking paths only.
- Registry state. I did not query npm.

---

## 2. Coverage ledger — one row per package, one verdict each

| # | package | Tier | verdict | basis |
|---|---|---|---|---|
| 1 | `flywheel` | 1 | **concept found** | C-W1-1, C-W1-2, C-W1-3. The promotion engine itself: frozen conjunctive gate, gate fingerprint, Ed25519 receipts, lineage DAG, replay bundle, anytime-valid composition. |
| 2 | `evals-hle` | 1 | **concept found** | C-W1-6 (fail-closed leakage detector over the candidate's own text), C-W1-5 (verifier/calibration defaults). One of five sites of the anchor mis-claim (evidence for C-W1-2). |
| 3 | `evals-math` | 1 | **concept found** | Contributes the **recompute** rung of the verification ladder (C-W1-5): symbolic re-derivation of the arithmetic, compared to the produced answer. Otherwise a template sibling of `evals-hle`. |
| 4 | `evals-sql` | 1 | **concept found** | Contributes the **execute-and-compare** rung (C-W1-5): run the produced artefact against the DB and compare result-set fingerprints across sampled candidates — the highest verification rung in my alphabet. |
| 5 | `evals-toolcall` | 1 | **concept found** | Contributes the **schema-check + retry** rung (C-W1-5): required-arg presence, argument-type consistency, enum-domain membership against the declared tool schema. |
| 6 | `evals-extract` | 1 | **concept found** | Contributes the **structural-validate** rung (C-W1-5): JSON-schema validation, per-field type checks, cross-field consistency. |
| 7 | `evals-servedmodel` | 1 | **concept found** | C-W1-5 (refuse-rather-than-substitute for LIVE mode; and the `costUsd = 0` direction problem), plus the two-independent-guards split (structural pre-measurement guard + measured post-measurement retention guard). Ecosystem coupling present but **not disqualifying** — see §4. |
| 8 | `bench` | 1 | **concept found** | C-W1-4, the strongest positive-shaped idea in this workstream: an anti-gaming invariant made structural rather than detected. Also the metric-algebra ceiling argument. `private: true`. |
| 9 | `weight-eft` | 1 | **concept found** | C-W1-6 (contamination guard, reward-hacking monitor) and the null-control/rollback pattern folded into C-W1-3's *how*. |

**No package in my set is `nothing portable`. No package in my set is `disqualified by ecosystem coupling`** — §4 states the mechanism-level reason for every coupling I found and why none disqualifies.

**Honest weighting of that ledger.** Rows 3–6 are template siblings of row 2: the five non-`servedmodel` `evals-*` packages share an identical 12-file layout and near-identical file headers. Their per-package contribution is the *verification rung*, not a distinct mechanism. Reading them as five independent discoveries would inflate this workstream; they are one family with four instruments.

---

## 3. Concept register — 7 entries (2 `new`, 4 `sharpens`, 1 `already held`)

Every entry carries all seven ratified fields. Volume is an anti-goal; six further candidates were examined and discarded as restatements (§6).

---

### C-W1-1 — A gate that can be retried must price the retries

1. **Concept.** An acceptance rule applied repeatedly against the same evidence set is uncontrolled multiple testing: a governed party that may re-propose indefinitely wins by attrition, because each individual decision looks locally justified. The fix is an **anytime-valid** acceptance statistic — a non-negative process with expectation ≤ 1 under the null, so that by Ville's inequality `P(sup_t E_t ≥ 1/α) ≤ α` and the rule may be evaluated at *any* time with no pre-registered sample size, no alpha-spending schedule, and no penalty for looking. Only *discordant* observations (candidate wins where the incumbent loses, or the reverse) move the statistic; concordant ones carry no information. The anytime-valid requirement **composes with** the frozen rule rather than replacing it: the candidate must clear both.
2. **Why it matters.** For a substrate whose enforcement must sit outside the governed party's reach, the *threshold* is part of the enforcement. A control with a fixed per-attempt threshold and an unbounded attempt budget is not a control — it is a delay. This is the statistical form of the same defect the custody predicate names structurally: unlimited retries are a channel the governed party holds.
3. **How.** Wherever an autonomous loop asks a gate the same question more than once — a self-improving agent, a retrying proposer, a re-submitted plan — carry accumulated paired evidence across attempts and admit only when it crosses `1/α`. The wrapper stays a plain rule, so it remains freezable and fingerprintable as one object.
4. **Novelty grade — `sharpens #259`.** `#259` holds the pre-registration form of the multiplicity concern: *"repetitions, quorum, prompts, model identity, evidence, hashes, and selection rules must be fixed before results."* This sharpens it in a setting where pre-registration is impossible by construction — a compounding loop cannot fix its generation count in advance — and names the mechanism that makes optional stopping legitimate instead. Checked and **not** held by `#200`, `#277`, `#316`, `#317`, `#318`, `#319`, `#323`, `#324`, `#325`, `#326`.
5. **Custody verdict — fails on input.** `alpha`, `lambda` and the per-item paired outcomes all arrive from the caller's evaluator, i.e. the same party proposing the change; `alpha` may be set arbitrarily close to 1. And the composition **degrades to the base rule when the paired outcomes are absent** rather than blocking — the module says so explicitly, and calls it the deliberate choice. So as placed it is a voluntary discipline. The *principle* survives independent custody intact: move `alpha` and the outcome record outside the governed party and it becomes a control.
6. **Evidence — static code evidence** for the mechanism (`packages/flywheel/src/sequential.ts` L79–108 `sequentialEvidence`, L123–145 `withSequentialEvidence`, L132 the degrade-to-base branch). **Source claim** for the motivating numbers: the header asserts *"published measurements ... put the false-commit rate at 30-42%, and found 13-21 spurious modifications made even when NO true gains existed — degrading one agent by 4.9 points"* (L8–12) with **no citation of any kind**.
7. **Provenance — none declared.** The module names method families in prose — testing-by-betting, e-processes, Ville's inequality, the McNemar insight — but cites **no paper, arXiv id, author or year**, and the quantitative claim above is uncited. Recorded as: *published prior art asserted, upstream not identified by the package.*

---

### C-W1-2 — Attestation surface ≠ decision surface: a frozen-gate fingerprint is only as wide as what it hashes

1. **Concept.** "The rule was unchanged" and "the decision procedure was unchanged" are different claims. If a decision is made partly inside a fingerprinted rule and partly beside it — an extra check in the engine, a veto flag set by the scorer, a tie-break in the caller — then the fingerprint attests a **proper subset** of the procedure, and an auditor comparing fingerprints learns strictly less than they believe. The rule: *the attested object must be the whole decision procedure, or the attestation must state its own boundary.*
2. **Why it matters.** This is `#318`'s "the protected operation runs beside the gate, not through it" raised one level, to attestation. A substrate that publishes proofs about its own controls can be truthful about the hash and still misleading about the control, and the reader has no way to tell. An attestation that does not enumerate its scope is the audit-time twin of a fail-open gate.
3. **How.** Hash the complete decision closure, not one function reference; or emit the attested scope as a field beside the digest ("this fingerprint covers clauses 1–4; the anchor check and the hard-stop flag are outside it"). For Jurati: any "policy unchanged" claim must name what the digest covers.
4. **Novelty grade — `sharpens #318`.** `#318` holds the enforcement-altitude form (sole-path mediation; the operation running beside the gate). The sharpening is the attestation altitude, and the specific observation that a *composition* of frozen rule + engine check + evidence flag is unfingerprintable as a whole while looking fingerprinted.
5. **Custody verdict — fails on custody and on call-site enumeration.** The digest is computed by the producer, from the producer's own function, and the verifier's pin is **optional**: with no pin supplied the check is compared against the bundle's own self-declared value, and with neither pin nor rule supplied three of the six replay checks pass vacuously. The set of sites that contribute to a promotion decision is not enumerated anywhere.
6. **Evidence — static code evidence.**
   - `packages/flywheel/src/gate.ts` L34–36: the fingerprint is `sha256(rule.toString())`.
   - `packages/flywheel/src/gate.ts` L19–27: the default rule's clause 5 is the anti-Goodhart anchor check, `if (e.anchor && e.anchor.candidate < e.anchor.baseline)`.
   - `packages/flywheel/src/run.ts` L159: the engine calls the rule as `rule({ baseline: score, candidate: candScore })` — **`anchor` is never passed.** The anchor comparison lives at L169–172, in engine code, outside the fingerprinted rule.
   - **Fact audit, repo-wide (`#324` — one fact, every site, ruled on at once).** `grep -rn "anchor:"` across `packages/`, `apps/`, `services/`, `crates/` returns exactly **one** site that populates `PromotionEvidence.anchor`: `packages/flywheel/__tests__/units.test.ts` L29, a unit test of the rule in isolation. Every other `anchor:` hit is a `FlywheelConfig.anchor` *suite*, a `LiftPoint.anchor` scalar, or an unrelated regex/hash anchor. Clause 5 of the frozen default gate is exercised by its own unit test and by **no** driver path in the repository.
   - **Five source-claim sites assert the opposite.** `evals-hle/src/gate.ts` L19–21, `evals-extract/src/gate.ts` L18, `evals-math/src/gate.ts` L21, `evals-sql/src/gate.ts` L21, `evals-toolcall/src/gate.ts` L21 each state that the frozen base gate guarantees, for every promotion, *"the anchor never regresses."* `evals-servedmodel/src/gate.ts` does **not** make the claim. Five of six.
   - Two further clauses sit outside the fingerprint: the `Score.regressed` hard stop is set by the caller's evaluator (`evals-hle/src/evaluator.ts` L54 folds the leakage verdict into it), and the winner tie-break `sort((a,b) => b.score.primary - a.score.primary)` is engine code (`run.ts` L167).
7. **Provenance — internal only.** `ADR-235` is named as the origin of the sealed-score design (`flywheel/src/types.ts` L116, `replay.ts` L8). No external origin declared. `ADR-235` resolves to `docs/adrs/`, outside this run's alphabet; not read.

---

### C-W1-3 — The re-executable decision record: seal the decision's complete input tuple *inside* the signature

1. **Concept.** A promotion record should let an outsider **recompute the verdict**, not merely read it. That requires three things together: (a) the decision rule, identified by digest; (b) the *complete* input tuple the rule was applied to, sealed into the record; (c) the seal covering (b) — the signature's payload must include the inputs, or re-execution simply re-runs the rule on numbers the producer can still edit. A record satisfying all three converts "trust my verdict" into "run the rule yourself." A record satisfying only (a) and (b) is a **downgrade disguised as an upgrade**: it invites the reviewer to perform a check that cannot fail.
   Two companions in the same family, both worth taking: **every proposed change carries its own inverse** (path, parent bytes, content hash) recorded at proposal time, so reverting is a property of the record rather than a later recovery procedure that depends on the governed party still cooperating; and **the null change competes as a first-class candidate and is the default**, with the identity property that choosing it leaves the system byte-identical to its pre-change state.
2. **Why it matters.** This is the strongest available substitute for trusting the producer, and it is the half that survives when custody cannot be moved. But it inverts sharply when the seal is narrower than the sealed data — the reviewer performs a ritual and reports a pass. That is `#319` §3's counter-lesson ("a correct concept with an unsafe default is worse than no gate") relocated from enforcement to audit.
3. **How.** Sign a payload that contains the rule digest, the baseline and candidate evidence in full, the parent link, and the timestamp. Publish the verifier as a function that takes the record and the rule and re-runs it. State in the verifier's output which checks were *skipped* for want of a pin or a rule.
4. **Novelty grade — `new`.** Checked against `#200`, `#277`, `#316`, `#317`, `#318`, `#319`, `#323`, `#324`, `#325`, `#326`. The adjacent ground is `#316`/`#319`'s *"pre-operation decision separated from post-operation receipt"* — which concerns the **separation** of the two artefacts, not the receipt carrying enough to reconstitute the decision. `#200`'s approval machinery and signed policy state cover authorisation, not verdict recomputation. Nothing holds the recomputability requirement or its seal condition. Flagged for cheap downgrade if a reviewer reads `#319` §5 more broadly than I do.
5. **Custody verdict — fails on custody.** Three independent ways:
   - **The key.** `makeSigner()` generates an ephemeral Ed25519 keypair in the producer's own process and **embeds the public key in the receipt**; `verifyReceipt` verifies against that embedded key. There is no external trust root, and replay never checks that the commits on a chain share one key. Anyone can re-sign a rewritten chain and it verifies. **This half is `already held by #200`**, which records the identical defect in ruvnet's Rust `witness` ("the verifying key inside the signed document — no external trust root, so anyone can re-sign a tampered manifest and it verifies") and warns against laundering it into a supply-chain attestation. Two independent subsystems, same repository, same defect — worth recording as corroboration of `#200`, not as a new finding.
   - **The seal's scope.** The signed payload is `{ kind, id, target, verdict, primaryDelta }` (`run.ts` L187). The sealed evidence the re-execution reads — `baselineScore`, `candidateScore` (`run.ts` L189–190) — and the `parents` array are **outside the payload**. An adversary edits the scores freely; the receipt still verifies; re-execution then runs the correct rule on chosen numbers and returns `promote: true`.
   - **The re-executed rule is weaker than the original.** `replay.ts` L78 re-gates with `{ baseline, candidate }` only. The anchor pair is not in `LineageCommit` at all (only a single `anchorScore` scalar), so the anti-Goodhart clause is vacuous on re-execution and a promotion that failed *only* on the anchor cannot be caught by the re-run.
   - **The inverse is unverified.** `run.ts` L182 stores the proposer-supplied `inverse` verbatim. No source file checks `sha256(parentBytes) === hash`; the only such assertion is in `flywheel/__tests__/refine-evidence.test.ts` L77, where the test constructs both sides. The rollback record is proposer self-assertion.
   - **Reachability of the strong check.** The shipped `replay` CLI verb never passes `promotionRule`, so the ADR-235 re-execution is vacuously true on that path and is not printed among its six output lines (`cli.ts` L42–57). The one repository site that supplies both pin and rule is a driver in `packages/darwin-mode/` (wfh-008's package — not re-derived, cited only as a call site of *my* package's API).
6. **Evidence — static code evidence** throughout (`flywheel/src/receipts.ts` L17–29, L32–39; `replay.ts` L29–93; `run.ts` L124–140, L174–194; `types.ts` L26–29, L104–121; `weight-eft/src/genome.ts` L11–16, L41–45 for the null-control companion). **Source claim** for the README's *"trusting the signature, not you"* framing.
7. **Provenance — internal only.** `ADR-235` (sealed scores), `ADR-246 §2.1` (rollback-by-construction). No external origin declared. Both resolve to `docs/adrs/`, outside this alphabet; not read.

---

### C-W1-4 — Structural anti-gaming: bind the score-improving operation to its coupled cost at the same granularity

1. **Concept.** When a quality metric is a ratio (`supported / total`), the cheapest way to raise it is to delete the denominator — drop the unsupported items and keep the claims they were supposed to support. Detecting that after the fact is a losing game. Instead, **make the gaming move inexpressible**: perform the metric-improving operation at the granularity where the improvement and its cost are structurally bound, so that taking the benefit forces paying the price. Concretely, at the unit where support and claim are joined: a redundant support may be removed (the claim survives on its remaining support — a pure win, correctly free); a claim whose *only* support is removed is itself removed, and the coupled coverage metric falls accordingly. The transform then *predicts* exactly when improvement is honestly available — only where the removed items were redundant.
   The companion, from the same package: **derive the ceiling of an improvement loop from the algebra of its objective before spending on the loop.** If the objective is a fraction whose denominator every transform inflates, if selection is capped by the best single draw, and if union can only dilute, then no amount of harness engineering exceeds the unimproved baseline — and that is a *mechanism*, established before any run.
2. **Why it matters.** Every other control in this workstream is a **detector** — regexes over adversary-authored text, denylists of paths and tool names — and every detector is a vocabulary the adversary can step outside of. This is the only mechanism I found in nine packages that removes the incentive by construction instead of policing it. For a substrate whose enforcement must live outside the governed party's reach, a rule the governed party cannot express is stronger than a rule it can express and be caught at. It is also the exact inverse of the monotonicity hole `#200` records in ruflo's objective compiler, where an operation improves one axis by silently relaxing another.
3. **How.** Wherever a gate reads a derived ratio or a composite score, ask which single operation raises it most cheaply, and then re-express the operation so that it cannot be applied to the numerator without applying to the denominator. Before commissioning any improvement loop, write down the objective's algebra and check whether the transforms available to the loop can exceed the baseline at all.
4. **Novelty grade — `new`.** Checked against all ten nodes. `#200` records the *symptom* (a widening hole in a translator that unions into allow and removes from deny with no approval step) as a defect; nothing holds the construction rule that prevents that class. `#319`'s take-list holds probe-the-real-operation, fail-closed protocol, deny precedence, monotone delegation, degraded-mode truthfulness — none of them this.
5. **Custody verdict — not control-shaped.** As placed it is an offline scoring transform run by the party being scored, so the predicate finds no authority boundary to test. But the predicate does not apply cleanly here and I will not manufacture a verdict: this is a **construction rule for controls**, not a control. Its value is that a control built this way has no input the governed party can supply advantageously, because the advantageous move does not exist.
6. **Evidence — static code evidence** for the mechanism: `packages/bench/src/draco/grounding-gate.ts` L11–28 (the stated invariant), L58–90 (`applyGroundingGate`: per-sentence unit; dead URL sharing a sentence with a live one → strip the token only; sentence whose only citations are dead → drop the whole sentence; sentence with no URLs → kept verbatim), with the URL checker injected so the transform is a pure function of `(answer, liveness)`. **Source claim** for the falsification narrative — the README's ADR-038/039 results ("no tested harness arm exceeded the frontier vanilla ceiling"; "~10× lower cost"; "the frontier *fusion* harness costs ≥250× the cheap direct call and scores worse") are the owner's own measurements, reported by the owner, and are **not** demonstration by us.
7. **Provenance — internal, plus a named ruflo ancestry.** `grounding-gate.ts` L3–4 declares the shape as *"the ruflo intelligence-pipeline JUDGE→CONSOLIDATE stage applied to citations (ADR-038 follow-up)"*. `ADR-037` / `ADR-038` / `ADR-039` / `ADR-040`; the package README additionally cites **Mem0** (`arXiv:2504.19413`) and **ReasoningBank** (Google Research blog) as baseline shapes it reproduces without running. See §4 for why the ruflo mention does not disqualify.

---

### C-W1-5 — Measurement provenance: an unmeasured input must be represented as unmeasured, and every placeholder has a direction

1. **Concept.** When a decision consumes a measured quantity that is unavailable, substituting a "neutral" placeholder is not neutral — the rule reads the axis **directionally**, so every placeholder sits somewhere on that axis, and the convenient value is usually the favourable one. A cost-minimising clause reads an unmetered cost of `0` as the best possible result. An agreement-thresholding clause reads a defaulted `0.5` as halfway to agreement. The rule: **carry the measurement's provenance with the value — which instrument produced it, at which rung, or that it was defaulted — and let a defaulted input block the decision rather than default in the direction the decision rewards.**
   The companion is the **verification ladder** these packages implicitly define but never surface: structural validation (schema, types, cross-field) → independent recomputation (symbolic re-derivation) → execute-and-compare (run the produced artefact, compare outcome fingerprints across samples). The rung is what makes a verification signal mean anything, and the rung never reaches the score.
2. **Why it matters.** A gate whose inputs can be *withheld* rather than falsified is defeated without ever lying to it: the governed party simply declines to wire the expensive instrument, and the cheap default carries the promotion. That is a custody failure with no forged value anywhere in it, and it is invisible to a signature, a fingerprint, and a replay. For Jurati specifically: a budget or capability gate reading an unmetered axis as zero always passes.
3. **How.** Make every gate input a pair `(value, provenance)` where provenance is `measured@rung` or `defaulted`. Make the frozen rule reject on `defaulted` for any clause where the default is favourable. State the rung in the decision record so a replay can see it.
4. **Novelty grade — `sharpens #316`.** `#316` and `#319` hold *degraded-mode truthfulness* and *"the degraded mode must be visible in the result."* The sharpening is that untruthfulness is not the whole risk: the placeholder's **direction relative to the rule** is what converts a missing measurement into an advantage, and the fix is therefore not only to *report* the degradation but to make the defaulted input non-promotable.
5. **Custody verdict — fails on input, across seven of my nine packages.** The party choosing whether to inject the real instrument is the party seeking the promotion, and choosing not to inject it produces the favourable value with no lie told anywhere.
6. **Evidence — static code evidence.** **43** non-test placeholder sites in my alphabet (A4). Named instances:
   - `evals-servedmodel/src/ruvllmClient.ts` L85–89: no judge injected → `afterQuality = 0.5`; local endpoint → `costUsd = 0`, with the header stating *"Never invent a per-token USD figure for a local endpoint."* Zero is the most favourable possible value for the frozen gate's `costPerWin` clause.
   - Verifier defaults, identical in all five non-`servedmodel` adapters: `mode === 'none'` → `agreement: 0.5` (`evals-hle` L34, `evals-math` L36, `evals-sql` L36, `evals-toolcall` L46, `evals-extract` L35); empty check set → `agreement = 0.5` (same five, L56–68).
   - Calibration defaults: `logprob ?? 0.5`, `selfConsistency ?? 0.5`, `verifierAgreement ?? 0.5` in all five `calibration.ts` (L20–22 each), feeding `shouldEscalate` and `shouldAbstain`.
   - Every adapter's real instrument is an **injectable** whose default is explicitly *"a structural approximation so the adapter runs at $0 for replay; a real check is strictly better"* — `DomainChecker` (extract), `SqlExecutor` (sql), `SymbolicChecker` (math), the executable verifier (toolcall), `Judge` (hle). Nothing on `Score` records which was in effect.
   - The one place the discipline is applied correctly, and it is worth naming: `ruvllmClient.ts` L38–44 **throws** when LIVE mode is not explicitly enabled rather than silently returning synthetic data (*"never silently substitutes synthetic data — that would fabricate a LIVE result"*), and `weight-eft/src/train.ts` L209–217 **refuses** rather than proceeding. Both are fail-closed defaults, in the same repository whose isolation gate `#318` records as fail-open. The fail-open default at `#318` is therefore an **inconsistency**, not an architectural constraint of the design.
   - Counter-note on the second of those: `weight-eft/src/defaultDetectGpu` (L99–111) establishes capability by reading `WEIGHT_EFT_BASE_URL` / `OPENAI_BASE_URL` / `CUDA_VISIBLE_DEVICES` — an **inventory-shaped check**, the exact anti-pattern `#319` §2 names ("an inventory-shaped check is a false-positive machine"). A second independent instance, in a package wfh-008 never opened.
7. **Provenance — internal.** `ADR-226` (the measured "read-only strong advice added zero marginal resolves at 5.4× cost" claim that motivates the deterministic verifier design) ×11, `ADR-234` ×23. No external origin declared for the placeholder behaviour.

---

### C-W1-6 — Evidence is inadmissible if the run that produced it touched its own judge

1. **Concept.** An outcome is admissible as promotion evidence only if the run that produced it never **read the oracle** and never **wrote to the verifier**. Extend self-approval-forbidden from the approval act to the evidence-production act: the governed party must not be able to read the answer key, modify the scoring harness, or act outside the sanctioned surface, and any trajectory showing those signals is *dropped from the evidence set* rather than merely down-weighted. The family that implements it here is consistent and worth taking as a family: a **fail-closed pre-measurement screen** (a pure function of the proposed artefact, run before it can be scored, whose positive verdict marks the candidate hard-failed) plus a **measured post-measurement retention check**, deliberately kept independent — two guards that do not share an input.
   The accompanying discipline is as valuable as the guard: **every exclusion is counted and attributed to a named reason, and the surviving set is enumerated by id.** Nothing is silently lost.
2. **Why it matters.** This is the closest thing in nine packages to an enforcement rule stated in the right shape for Jurati — it constrains what the governed party may *touch*, not what it may *claim*. And its failure mode is the most instructive one I found: the guards are all **denylists**, and a denylist is a vocabulary. `#323`'s lesson — a sweep inherits the blindness of its own alphabet — applies verbatim to a runtime control's detection vocabulary. A control that enumerates the answer set is guaranteed to terminate cleanly and prove nothing.
3. **How.** Define admissibility as a predicate over the *observed* run record (which tools were invoked with which arguments), not over the party's declarations. Reserve a hard-stop channel on the evidence so a new veto can be added without changing (and re-fingerprinting) the acceptance rule — but see C-W1-2, because that channel then sits outside the attestation. Publish the drop-accounting.
4. **Novelty grade — `sharpens #200`.** `#200` holds the approval-side primitive: *"approval machinery enforcing self-approval-forbidden, untrusted-issuer rejection, unique ids, expiry."* The sharpening is the evidence side — **read access to the oracle disqualifies the evidence, not only write access to the verdict** — and the observation that this class of guard is only as wide as its enumerated vocabulary.
5. **Custody verdict — fails on input, fails on custody, and fails on call-site enumeration.** Three separate catches, all in packages wfh-008 never opened:
   - **Input.** `weight-eft`'s contamination guard decides on `ExportOptions.evalHoldout`, a set supplied by the caller — the same party that wants the lift — and the type comment says *"Required (may be [])."* Passing `[]` disables it completely. This is `#319` §4's defect (`no-bypass-sandbox` deciding on a proposer-supplied boolean) in a second, independent subsystem.
   - **Custody.** `ExportOptions.dropRewardHacked` defaults `true` but is caller-settable to `false` (*"Set false ONLY for debugging"*). The governed party can switch off its own reward-hacking filter.
   - **Call-site enumeration.** The reward-hacking monitor recognises reads and writes by a hardcoded set of **six read tool names** and **five write tool names**; a tool outside those sets skips the gold-read and verification-tamper branches entirely. The path patterns are likewise a fixed regex denylist. The governed party chooses the tool.
   - The leakage detectors are the same shape one level down: regexes over the candidate policy's own prose. Their *input derivation* is right — it is static analysis of the proposed artefact, exactly what `#319` §4 prescribes, and a genuine positive counter-example to `no-bypass-sandbox` in the same repository. But a derived input whose **content** the adversary still authors is a **detector, not a control**: a proposer optimising against a known regex routes around it in one generation. Derivation is necessary and not sufficient.
6. **Evidence — static code evidence.**
   - `weight-eft/src/reward-hack.ts` L24–59 (the three pattern sets and the two tool-name sets), L87–117 (`detectRewardHack`), L120–122 (`isRewardHacked`).
   - `weight-eft/src/export.ts` L109–126 (`assertTrainEvalDisjoint`, throws — *"fail loud, not silently filter"*), L156–213 (the ordered pipeline: holdout exclusion → assert → length filter → reward-hack filter, applied before SFT/DPO); `weight-eft/src/types.ts` L123–152 (the option contracts), L162–179 (`ExportReport`: `excludedByHoldout`, `droppedOverLength`, `truncatedOverLength`, `droppedRewardHacked`, `sftInstanceIds`, `dpoInstanceIds`, `notes`).
   - `evals-hle/src/leakage.ts` L20–21 (`ARTIFACT_RE`, `HACK_RE`), L24–54 (`detectLeakage`, `leaks`), wired at `evals-hle/src/evaluator.ts` L54 into `Score.regressed`; identical wiring in `evals-extract` L55, `evals-math` L54, `evals-sql` L56, `evals-toolcall` L53. **`evals-servedmodel` has no leakage detector** — it substitutes `driftguard.ts`.
   - `evals-servedmodel/src/driftguard.ts` L1–9 (the two-independent-guards rationale), L31–44 (`detectDriftRisk`, `driftRisky` — a pure structural function of the genome, no data needed), L46–54 (`driftPressure`, explicitly *"never fed back into `driftRisky`"* — the measured quantity is deliberately kept out of the structural gate); the measured half at `gate.ts` L37–43.
7. **Provenance — declared external, verbatim.** `weight-eft/src/reward-hack.ts` L3, L14–16: *"deterministic reward-hacking monitor (Ornith-1.0 borrow) ... Prior art: Ornith-1.0 (DeepReinforce) — self-scaffolding RL for agentic coding — uses a deterministic monitor that flags trajectories acting outside the sanctioned tool surface → zero reward + excluded. See ADR-198."* `evals-servedmodel` declares `ADR-234 §3` for the two-independent-guards split and names **EWC++** and **SONA / MicroLoRA** as the weights-level mechanisms. Per scope: the declared origins are recorded; the upstream was **not** read.

---

### C-W1-7 — Verification must be deterministic; a model's opinion is a signal, never a verdict *(reported as held, not as a finding)*

1. **Concept.** The check that decides admission is a deterministic function over the artefact — schema validation, type and cross-field consistency, symbolic recomputation, execute-and-compare — and never a model asked whether the artefact is good. A model's judgement may enter as a *routing* or *calibration* signal (escalate on disagreement, abstain under low confidence); it may not enter as the verdict.
2. **Why it matters.** It is the same invariant this theme has already adopted, arrived at here by a different argument.
3. **How.** Already in force in our own position.
4. **Novelty grade — `already held by #200`.** `#200` records ruflo's CASA invariant verbatim — *"translation MAY use an LLM; ENFORCING the envelope MUST NEVER"* — and explicitly concludes *"the determinism position is becoming the field's default, not a differentiator."* MetaHarness's W1 packages are a further independent instance of exactly that convergence and change nothing about our position. Recorded here so the register shows the check was made and the claim declined, rather than dressing a held position as a discovery.
   One detail is worth carrying even though the concept is held: MetaHarness reaches the rule by an **economic** argument, not a security one — its stated reason is a measurement that read-only strong advice added zero marginal resolves at 5.4× cost. Convergence from an unrelated premise is mild evidence the rule is robust.
5. **Custody verdict — not control-shaped** as placed: the verifier stack produces an agreement scalar consumed by routing and calibration inside the governed process, and does not mediate any operation.
6. **Evidence — static code evidence**, five identical file headers: `evals-extract/src/verifier.ts` L4–7, `evals-sql` L4–8, `evals-math` L4–8, `evals-toolcall` L4–8, `evals-hle` (same header). Each states the verifier is *"deliberately NOT a generic 'critic says yes' model"* and gives the ADR-226 cost measurement as the reason.
7. **Provenance — internal.** `ADR-226` (×11 across my packages). No external origin declared.

---

## 4. C2 — ecosystem coupling, tested at the MECHANISM level

**No package in my nine is disqualified.** The scope warns that applying C2 as a manifest scan would disqualify most of the repository and return a false negative; here is the mechanism-level reasoning for every coupling I found, so the auditor can check that no verdict was reached by dependency list.

| package | coupling found | mechanism-level test | verdict |
|---|---|---|---|
| `flywheel` | **none.** Zero runtime dependencies; `node:crypto` only. `devDependencies` are `typescript`, `vitest`. | Nothing to test. | clean |
| six `evals-*` | one first-party npm edge each: `@metaharness/flywheel ^0.1.1`. No other runtime dependency. | The composite-gate pattern (call a frozen base rule and AND stricter domain clauses) needs no MetaHarness code — it needs a rule type. | clean |
| `evals-servedmodel` | **`ruvllm serve`** — an upstream *service*, declared in no manifest: `RUVLLM_URL`, `RUVLLM_MODEL`, `EVALS_SERVEDMODEL_LIVE` env namespace, plus branded method names SONA / MicroLoRA / EWC++. | The endpoint contract is OpenAI-compatible `POST /v1/chat/completions`, not a branded shape. The two portable mechanisms — a fail-closed structural guard that is a **pure function of a typed genome** (`driftguard.ts`, no data, no network) and refuse-rather-than-substitute for LIVE mode — hold with `ruvllm` deleted; they refer to it only through a URL and a flag. | **not disqualifying**; coupling confined to the live client. |
| `bench` | `@metaharness/kernel` (which `#316` records as carrying a RuVector closure), 11 `@metaharness/host-*` packages, `@metaharness/router`; DRACO's live arms need OpenRouter and `OPENROUTER_API_KEY`. And `grounding-gate.ts` L3 names *"the ruflo intelligence-pipeline JUDGE→CONSOLIDATE stage"*. | Manifest-scanning this package would disqualify it outright and cost the run its single strongest concept. The concept (C-W1-4) is a **pure function of `(answer, liveness-checker)` with the checker injected**, explicitly designed to be evaluable offline; the metric-algebra ceiling argument needs no code at all. The ruflo mention is a **name in a comment** — nothing is imported from ruflo, which independently corroborates `#316`'s characterization ("ancestry, copied contracts, aliases and config names") from a package wfh-008 never opened. | **not disqualifying.** |
| `weight-eft` | `ruvllm` / MicroLoRA named as the training integration point; `WEIGHT_EFT_BASE_URL` / `OPENAI_BASE_URL` / `CUDA_VISIBLE_DEVICES`. `train.ts` L219–221 states the actual `spawn(command)` *"is intentionally NOT wired here."* | The three portable mechanisms — contamination guard, reward-hacking monitor, null-control gene — are pure functions of trajectory records and genome values, with no vendor in them. The training runner is a plan emitter. | **not disqualifying.** |

**Where the disqualifying test *would* bite, for contrast:** a mechanism whose statement requires the branded contract (e.g. anything that only means something given `@metaharness/kernel`'s type shapes, or a `RUFLO_*` state namespace). I found none of that shape in my nine.

---

## 5. Distribution and publication — the `#324` trap, checked explicitly

*Packed, published, exported, re-exported and reachable are five different claims. Ruled on together.*

- `bench` is **`"private": true`** → **publishes nothing at this cutoff.** Its DRACO run artefacts and corpora are tracked files, not distributed ones.
- The other **eight carry no `private` flag** → **publishable, NOT verified published.** Settling registry state needs a fetch this envelope forbids. I did not query npm.
- **None of my nine appears in `scripts/publish-workspace.mjs` `RELEASE_ORDER`** (12 entries: `kernel-js`, `sdk`, five `host-*`, `host-prime-agent`, `vertical-base`, `vertical-trading`, `create-agent-harness`). The script's own comment at L29 says so: *"not listed here (evals-*, flywheel, darwin-mode, redblue, weight-eft, …)."*
- **A tension, stated as tension not contradiction.** `scripts/healthcheck.mjs` L85–110 carries **six** comments asserting `@metaharness/flywheel` and five `evals-*` packages are each *"a standalone published adapter/library on its own semver"* — a **source claim** of publication, unverified here, and stale on its face: it says flywheel was *"published 0.1.1"* while the manifest reads `0.1.10`. The release script is not necessarily the only publish path, so this is not proof of a false claim; it is proof that the repository's own two statements about these packages do not reconcile from inside.
- `flywheel/src/cli.ts` exports `dispatch`, which is compiled into `dist` and inside the `files` allow-list, but is **not** re-exported from `src/index.ts`; the package declares no `exports` map, so a deep import is not blocked. Whether the `metaharness` umbrella CLI actually reaches it is a `create-agent-harness` question — wfh-008's ground, not re-derived here.
- `flywheel/README.md` L8 links a licence badge to `./LICENSE`; **no `LICENSE` file exists in that package directory.** Same class as `#316`'s note about `packages/projects`. Recorded as a fact, not priced — C1 forbids licence closure work.

---

## 6. Candidates examined and NOT reported as concepts

Recorded so the register's shortness is auditable rather than assumed.

| candidate | why not a register entry |
|---|---|
| The self-signed Ed25519 receipt with embedded verifying key | `already held by #200` verbatim. Folded into C-W1-3's custody verdict as corroboration. |
| The frozen anchor / never-optimized-against suite as the anti-Goodhart guard | Textbook held-out methodology; the only non-obvious part is the custody question (an anchor the optimising party holds and scores is a label), which is C-W1-2's and C-W1-5's ground already. |
| Schema-clamped proposal (`clampLever`: the LLM proposes, the harness coerces into the lever's type/range, never free prose) | The load-bearing half — *enforce the grammar where the mutation is ACCEPTED, not where it is PROPOSED* — is `#318`'s "route the operation through the gate, not beside it." The engine's `Proposer` type returns an arbitrary string and nothing constrains it; the clamp is this proposer's voluntary discipline. Restating it would be the exact over-grade `#319`'s goal-owner flagged. |
| Compounding lineage as a parent-linked DAG ("git for operating policies") | A data structure, not a mechanism; contributes nothing the recomputable-record concept does not. |
| Resume-from-checkpoint / observation-only hooks that cannot affect promotion | Genuinely good hygiene (`run.ts` L200–216 swallows hook errors so a bad checkpoint cannot kill a valid run), but it is separation-of-concerns, not an authority mechanism. |
| Mutation-effectiveness analysis (which levers earn promotions) | Read-only reporting over the ledger. Useful; not a control. |

---

## 7. Cross-workstream handoffs (to the leader — not absorbed, not analysed)

1. **→ W2, `avo`.** `packages/avo/src/flywheelGate.ts` L18, L60–64 contains what its own comment calls an *"EXACT mirror"* of flywheel's `meetsPromotionRule`, re-implemented in a second package, *"including the fixed reason ORDER."* Since flywheel's freshness proof is `sha256(rule.toString())`, two source copies can never produce a matching fingerprint and can silently drift. I did not open `avo` beyond confirming those line references exist. `ADR-271` is titled *avo receipts as flywheel gate evidence*.
2. **→ W4, `radio`.** `packages/radio/scripts/flywheel-radio.mjs` L184 calls `verifyReplayBundle(result.replayBundle)` with **neither a pinned fingerprint nor a rule**, in the same process that produced the bundle — the vacuous-pass path described in C-W1-2. Reported because it is a call site of *my* package's API; the package analysis is W4's.
3. **→ leader, for the theme.** `#316`'s "portable concepts" list should gain the recomputable decision record and the structural anti-gaming rule if the curator distils them; both extend `#319`'s TAKE list rather than contradicting it.

---

## 8. What MetaHarness *is*, on the provenance axis (the Q4 pattern — it holds)

Counted across my nine packages:

- **8 of 9 declare an external origin** for their benchmark, their method, or both: HLE / `cais/hle` and a named Artificial Analysis frontier figure (`evals-hle`), GSM8K (`evals-math`), Spider / BIRD (`evals-sql`), BFCL (`evals-toolcall`), Mem0 `arXiv:2504.19413` and ReasoningBank (`bench`), Ornith-1.0 / DeepReinforce and SWE-bench and TRL/axolotl/unsloth (`weight-eft`), EWC++ / SONA / MicroLoRA (`evals-servedmodel`). Only `evals-extract` names no external benchmark.
- **9 of 9 cite internal ADR numbers** — 22 distinct ones, 128 references.
- **The one package that declares no external origin at all is `flywheel`** — the engine, the thin part, and the only genuinely novel-looking machinery in the set. Its `sequential.ts` names four statistical method families in prose and cites none of them, while quoting an uncited quantitative result.

**The pattern is a finding about what this half of MetaHarness is:** an implementation surface over published benchmarks and named third-party methods, wrapped in a small first-party promotion engine. Where a concept here traces to a declared upstream, **the citation we should carry is the upstream, not MetaHarness.** Per scope, I recorded the declared origins and **did not read a single one** — following them would be a literature pass this run does not have.

---

## 9. Custody-predicate report (C5, as an instrument)

> *A control whose input, custody, or call-site enumeration sits inside the governed party is a label, not a control.*

Ten control-shaped mechanisms in my nine packages were run through it. **It caught nine.**

| mechanism | verdict |
|---|---|
| `flywheel` frozen promotion rule (injectable, caller-supplied) | fails on input |
| `gateFingerprint` / gate-unchanged claim (producer-computed; verifier pin optional) | fails on custody |
| Ed25519 promotion receipt (ephemeral in-process key, embedded pubkey, no chain-key consistency check) | fails on custody |
| `verifyReplayBundle` gate re-execution (seal narrower than sealed data; anchor dropped; unreachable from the shipped CLI verb) | fails on custody |
| `withSequentialEvidence` (caller sets α; degrades to base rule when outcomes absent) | fails on input |
| `evals-*` leakage detectors (regex over adversary-authored prose) | input correctly derived; **fails as an adversarial control** — a detector, not a control |
| `evals-servedmodel` drift guard (pure structural function of the genome) | fails on custody — the genome and the thresholds sit with the same party; **the closest thing to a pass in this set**, because its input is not a declaration |
| `weight-eft` contamination guard (`evalHoldout` caller-supplied, `[]` legal) | fails on input |
| `weight-eft` reward-hack filter (`dropRewardHacked` caller-disableable; tool-name enumeration) | fails on custody **and** on call-site enumeration |
| DRACO grounding gate | **not control-shaped** — a construction rule, not a control (see C-W1-4) |

**Nothing in my nine passes.** Nine independent subsystems, on top of the seven `#318`/`#319` recorded, and the failure is monotonously the same one: the input, the threshold and the switch all sit with the party seeking the promotion. That is a result about MetaHarness and it is also a result about the instrument — it has now caught sixteen subsystems by inspection without a single false positive that I can identify, which is either a very good instrument or a target with a uniform defect. I lean to the second and note that a predicate which never returns "pass" has not yet been calibrated against a system that should pass.

---

## 10. Limits — recorded negatively (`#324`)

What I checked is above. What I did **not** check:

- **`bench` is my largest unread surface.** 18 source files, 4,982 LOC. I read `README.md` and `src/draco/grounding-gate.ts`. I did **not** read `scorer.ts`, `routing.ts` (408 lines), `fusion.ts`, `ablation.ts` (515 lines), `judge.ts`, `live-citation.ts`, `self-consistency.ts`, `optimized.ts`, `cost-efficiency.ts`, `embed.ts`, `runner.ts`, `draco-bin.ts`, `bin.ts`, `host-bench.ts`, `host-bin.ts`, `augment.ts`, or any `draco/runs/*.json` artefact. **C-W1-4's mechanism is read from one file; the README claims about ADR-038/039 results are unverified source claims.**
- I did **not** read the evaluators of `evals-extract`, `evals-math`, `evals-sql`, `evals-toolcall`, `evals-servedmodel` — only `evals-hle`'s, plus the four verifier headers. I did not read any `data.ts`, `score.ts`, `routing.ts`, `classifier.ts`, `normalizer.ts` or `genome.ts` in that family beyond `evals-hle`'s calibration and `evals-servedmodel`'s state/driftguard.
- I did **not** read any `__tests__` file; the three test facts cited above come from grep with line numbers, not from reading the files whole.
- I did **not** read `flywheel/scripts/verify-dual.mjs`, `evals-math/bench/`, `evals-toolcall/experiments/`, or `bench/draco/*.json`.
- I did **not** read a single ADR. All 22 referenced numbers resolve to `docs/adrs/`, a declared hole in this run's scope. `ADR-226`'s "5.4× cost, zero marginal lift" measurement, `ADR-234`'s two-guards rationale, `ADR-235`, `ADR-246 §2.1`, `ADR-198` and `ADR-037`–`ADR-040` are all **unresolved pointers**. Opening `docs/adrs/` is a cheap, well-bounded follow-on scope and would materially firm up §8.
- I did **not** read any upstream cited by a package (Ornith-1.0, Mem0, ReasoningBank, HLE, GSM8K, Spider, BIRD, BFCL, EWC). Out of scope by ratification.
- I did **not** open `avo`, `radio`, `turn-credit`, `darwin-mode`, `create-agent-harness` or any other workstream's package beyond the two grep-confirmed line references handed off in §7.
- I did **not** run, install, build, test, spawn, fetch or probe anything, and did **not** query npm. Every publication statement in §5 is manifest-and-script derived; **none establishes registry state.**
- **Class-level negative claims in this file hold only against a TypeScript-source instrument at one commit.** A decision point reached by dynamic import, expressed in `.mjs` or `.json`, or supplied by an out-of-repo consumer is structurally outside my alphabet — including, specifically, whether some out-of-repo driver *does* pass `PromotionEvidence.anchor` and thereby activates clause 5. I claim only that no in-repository site does.
- No dynamic behaviour is asserted anywhere in this file. The re-execution weakness, the seal gap, and the unreachable anchor clause are **read from source, not witnessed**.
