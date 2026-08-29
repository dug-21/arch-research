# wfh-011 — tech-discovery coverage gate

**Auditor:** `factory-validator` · **Run:** `wfh-011` · **Theme:** `workflow-harness` · **Issue #70**
**Phase:** `tech-discovery` · **Confidence-required:** directional, research-scope, structure-only
**Audited state:** `main` at `fd7ab89` · **Date:** 2026-08-29

## RULING — `REWORKABLE` (round 1 of at most 2)

Four blocking defects, all in the same seam and all cheaply fixable. **None is a `SCOPE-FAIL`
trigger** under coverage clause 8: there is no unreconciled X row, no silent model normalisation, no
missing applicable rejection, and no unresolved premise mismatch. Clause 12 is what bites — an
unclassified pressure, plus filled absence.

**Recommended grade movement: NONE.** This scope forbids graph writes and grade movement, and I
recommend none. Nothing in the evidence would support anything above `claimed` if a grade were
sought; the run does not seek one and should not be read as having earned one.

**Independence.** I authored no part of W1, W2, W3 or W4 and advised on none of them. I was given no
workstream verdict, no count and no correction history; every number below is one I measured.

---

## 0. What I re-executed, and what reproduced

I re-ran every checker rather than read its committed log.

| Artifact | Result |
|---|---|
| `v5_model_check.py` | re-run; output **byte-identical** to `v5_model_check.out.txt` |
| `wfh-008-validate.py` (instance + counterfactual) | re-run; **byte-identical**; 0 errors, 33 warnings, 8 notes |
| `wfh-008-coverage-gen.py` | regenerated; `wfh-008-coverage.csv` **byte-identical**; 468 rows |
| `vnc-045-coverage-build.py` | regenerated in place; `vnc-045-coverage.csv` **byte-identical**; 679 rows |
| `v5_instance_check.py validate` (W3 baseline) | re-run; 0 findings |
| `v5_instance_check.py suite` | re-run; `rejection-results.csv` **byte-identical**; 115 fixtures |
| `v5_instance_check.py traverse` | re-run; `traversal-results.csv` **byte-identical**; 67 rows |

**M01 digest verified by me:** worktree file and the `HEAD` blob both hash
`bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060` — matches the SCOPE pin. The
model was parsed as-is; I found no quoting, normalisation, in-memory patching, or import of the
review's intended prose in any checker.

**Independent X enumeration.** I enumerated the X alphabet from M01 myself (663 items) without
reading either workstream's enumerator. Every one of my items resolves to a ledger row; the ledger is
finer than mine only on `extension_owner` sub-keys. The ledger's X coverage is a superset of an
independent reading of the SCOPE's X clause.

**Independent source checks.** I went to the pinned corpus rather than accept a quotation:
`37c7b09a` has a **single parent** `9927de02` and none of `a63d45f0`/`74bc1fd4`/`b68c2c43`/`bf7c4812`
is an ancestor — the SCOPE extension's squash-merge property holds. `product/features/vnc-045/`
carries **43 files**. **226** feature directories exist; **153** carry a `reports/gate-3c-report.md`,
and 153 carry a gate-3c artifact *anywhere* — **`vnc-045` carries none, in `reports/` or `agents/`**,
which independently verifies W2's F-02 and W2/CF-05's factual base. `SCOPE-RISK-ASSESSMENT.md` SR-10
does record the program vocabulary `{proven, partial, missing, asserted}`, so W4's "single strongest
model-defect" (M01's `values.evidence_grade` closes without `asserted`) is real at source.

---

## 1. Clause-by-clause

| # | Coverage clause | Verdict |
|---|---|---|
| 1 | Every M/R/S item `used` / `inspected-no-material-instance` / `unavailable`; transitive sources added before use | **MET** |
| 2 | Every X item has one reconciled disposition in the pressure ledger | **MET** |
| 3 | Every applicable X item has a conforming witness, or an explicit ruling — **absence never filled** | **NOT MET — RW-1, RW-3** |
| 4 | Every applicable falsifiable rule has a minimal invalid fixture + expected rejecting check; results classified | **MET** |
| 5 | Registries/catalogs/seeds/extension points exercised or dispositioned; empty seeds not invented | **MET** |
| 6 | Required traversals + declared inverses demonstrated or recorded as a hole | **MET** (with a recorded altitude difference) |
| 7 | W4 reconciles every row, dispositions every OPEN, returns retain/revise/reject, drafts no replacement | **MET** |
| 9 | Every failure/pressure row carries ≥1 cause with evidence | **NOT MET in the case matrix — RW-1** |
| 10 | Every evolution candidate: five analyses, separate identifiers, both fit verdicts | **NOT MET — RW-4** |
| 11 | W4 independently challenges each candidate; current verdict preserved | **NOT MET in the artifact — RW-4** |
| 12 | Auditor answers 13–18; circularity / erasure / conflation / unclassified pressure ⇒ `REWORKABLE` | **answered in §3; one unclassified pressure ⇒ `REWORKABLE`** |

### Clause 1 — MET
M01–M06 dispositioned by both W1 and W2 (three `inspected-no-material-instance` in W2, one in W1,
with reasons); R01–R06 by W1; S01–S06 by W2. Ten transitive sources are ledgered with identifier,
reason and provenance across W1 (T01–T03), W2 (T01–T03), W3 (T-01–T-06) and W4 (T-W4-01), and W4 §11
reconciles them. I found no source consulted outside that set.

### Clause 2 — MET
705 ledger rows: 679 `model-X`, 23 `instance-extension (NOT a model X item)`, 3 `w3-fixture (no
canonical X path)`. **Zero blank cells anywhere in the file.** Zero rows with an empty
`divergence_adjudication` or `w4_adjudication`. My own enumeration finds no X item missing.

W1 enumerated 468 rows and W2 679 — a real granularity divergence, correctly disclosed by W4 §3.4
and correctly resolved onto W2's spine, with 205 canonical rows marked `w1-not-enumerated` rather
than silently attributed. I re-checked all 171 W1 ids absent from the ledger by name: every one is a
naming-scheme variant or a roll-up of rows the ledger carries at finer grain. **No W1 row was
dropped.** Not a defect — but it does mean 205 canonical X items rest on a single case, which caps
their weight and should be stated in synthesis.

### Clause 3 — **NOT MET**

This is the ruling's centre. Three measured facts, in order.

**(a) `artifacts/vnc-045-instance.yaml` has never been mechanically validated against M01 by any
executed checker in this run.** Both validators key on a top-level `instances:` map; the W2 file uses
`scopes:` / `goals:` / `actors:` / … . I instrumented both and measured the objects each actually
parses from each file:

| Instance file | objects seen by `v5_instance_check.py` | objects seen by `wfh-008-validate.py` |
|---|---:|---:|
| `wfh-008-instance.yaml` | 191 | 191 |
| `w3-baseline-instance.yaml` | 37 | — |
| **`vnc-045-instance.yaml`** | **0** | **0** |

`v5_instance_check.py validate --instance vnc-045-instance.yaml` prints *"0 finding(s)"* and
`wfh-008-validate.py` prints *"RESULT: 0 error(s)"* on the same file. **Both green results are
vacuous** — they are what a broken instrument prints. No field type, cardinality, registry
reference, declared inverse or invariant in the software case has been mechanically checked.

**(b) `vnc-045-coverage-build.py` never opens its own instance.** The script imports only
`csv, subprocess, sys, os` — no `yaml`, no read of `vnc-045-instance.yaml`. Every one of its 596
`exercised` dispositions, 346 of which carry the provenance string `see instance`, is an authored
assertion that nothing joins back to the artifact. This is the exact property W1's generator was
built to have and documents in its own header ("*derived from the instance … so the witness column
cannot drift from the artifact*"). W2's does not have it.

I therefore performed the join myself. All 1 111 id tokens in W2's `instance_ref` column resolve to
real ids in the instance — the table is not fabricated. But on the 118 field/relation rows where the
claim is mechanically checkable, **9 diverge (7.6 %)**, and 7 of those are `exercised` against a key
the instance populates on **zero** objects:

| `model_path` | populated in `vnc-045-instance.yaml` | W2 witness text as committed |
|---|---:|---|
| `core.Goal.relations.is_advanced_by` | 0 / 3 goals | "EMPTY BY OBSERVATION" |
| `core.Capability.relations.advances` | 0 / 2 capabilities | "instantiated in vnc-045-instance.yaml" — **false as written** |
| `core.Capability.relations.delivered_by` | 0 / 2 | "EMPTY, deliberately" |
| `core.Unit.relations.delivers` | 0 / 8 units | "EMPTY BY OBSERVATION" |
| `core.Event.relations.supersedes` | 0 / 30 events | prose asserting the events are *separate*, not superseding |
| `supporting.EffectBoundary.relations.enforces` | 0 / 3 | "EMPTY. The case's central custody result" |
| `supporting.Delegation.fields.expires_at` | 0 / 13 delegations | "instantiated in vnc-045-instance.yaml" — **false as written** |

(`supporting.Role.relations.requires` is the ninth: `exercised` with the same boilerplate, populated
3 / 13.)

Four of these seven say plainly in their own witness column that the value is empty, and are
dispositioned `exercised` anyway. The SCOPE's rule is unambiguous — *"Absence is never filled"* — and
*"A rule is not counted as tested by paraphrase. It needs at least one conforming witness."*

**(c) W4's reconciliation rule then promoted the label without testing the witness.** The rule, stated
in `findings-W4-adjudication.md` §4.1, is sound as written: *"`exercised` in one case and
`not-applicable` in the other resolves to `exercised` (the run has a witness); absence is never
filled."* But it was applied to the **disposition** column, not the **value** column. Six ledger rows
now read `reconciled_disposition: exercised` where **neither case supplies a witness**:

| `x_id` | W1 | W2 | reconciled | actual witness |
|---|---|---|---|---|
| `core.Goal.relations.is_advanced_by` | `not-applicable` | `exercised` | **`exercised`** | none in either case |
| `core.Capability.relations.advances` | `not-applicable` | `exercised` | **`exercised`** | none |
| `core.Capability.relations.delivered_by` | `not-applicable` | `exercised` | **`exercised`** | none |
| `core.Unit.relations.delivers` | `not-applicable` | `exercised` | **`exercised`** | none |
| `core.Event.relations.supersedes` | `not-applicable` | `exercised` | **`exercised`** | none — and the row's own `w4_adjudication` reads *"W3 ADVERSE at this path: F-E07=accepted-defect"* |
| `supporting.Delegation.fields.expires_at` | `not-applicable` | `exercised` | **`exercised`** | none |

Each carries the same boilerplate adjudication: *"CASE-DIFFERENCE, not contradiction: one history
supplies a witness and the other does not."* On all six, **neither history does.** The ledger row's
own `value` column contradicts its own `divergence_adjudication`, in the same row.

W4 disclosed the enabling limit honestly (§10: *"I did not re-derive either case's instance … where a
row's value rests on a workstream's encoding judgment, my adjudication rests on it too"*), and it
caught the *inverse* defect — 27 W1 and 19 W2 rows carrying a cause while labelled `exercised`,
overriding 7 of them (§3.5, §4.2). Disclosure is not discharge: clause 3 asks for witnesses, and six
are missing.

This is not a large number against 552 reconciled `exercised` rows. It is blocking because of *what*
it is: a coverage table that never reads its own instance, feeding a reconciler that trusts the
label, behind two validators that pass a file they cannot parse. That is a green light from an
instrument that is not looking at the thing — in a run whose whole subject is what happens when a
check is offered a reading by a party with an interest in it.

### Clause 4 — MET
115 fixtures; results `rejected-mechanically` 82 · `accepted-defect` 18 · `not-falsifiable-from-alphabet`
9 · `specified-not-enforced` 5 · `negative-test` 1 (the exclusion negative test the SCOPE separately
requires). I confirmed **all 19 invariants have at least one fixture** in
`invalid-instance-matrix.yaml`, and that **all 115 fixture ids are linked into ledger rows** with
none orphaned and none dangling. The suite reproduces byte-identically. The disclosed
operationalizations (O1–O12) and the `--illustrative` separation are exactly the right discipline:
checks M01 does not state are never counted as model discrimination.

*Traceability observation, non-blocking:* seven invariant X rows (`I3`, `I5`, `I6`, `I10`, `I11`,
`I12`, `I13`) carry `w3_fixture_ids: not-applicable` although fixtures exist for each — they are
anchored at the field/relation path instead (`F-E20` at `core.Capability.relations.required_by`,
`F-E14` at `supporting.Skill.relations.held_by`, and so on). No rejection is missing; the
cross-reference is.

### Clause 5 — MET
M01 seeds `record_category`, `unit_kind` and `effect_class` **empty**. Both cases registered
program-owned extensions (W1: 9 / 8 / 5; W2: 7 / 3 / 4) and the three `registries.*.seeded<EMPTY>`
ledger rows state explicitly that the empty seed was **not** filled with invented canonical values.
`scope_type` and `capability_classification` seeds are exercised — all four classification seeds in
the software case. The mechanism did its job, and W4 §6 correctly records the adverse counterpart
(`F-H09` / `F-E08` / `F-H08`: the `excluded:` list is re-openable through the registries).

### Clause 6 — MET, with a recorded altitude difference
67 executed traversal rows. Both required traversals are demonstrated **and** recorded as
query-layer holes with cost: `Goal → applicable Workflows` via a full-extent index scan the model
does not bound, and the declared-relation path shown to be **both incomplete and unsound** on the
baseline. No inverse relation was added to the model to make a traversal work — concern 8 is
answered honestly, including the silent global scan.

*Altitude difference, recorded not held:* the traversals are executed on the W3 synthetic baseline and
on `wfh-008-instance.yaml`. For `vnc-045` they exist as an authored `traversal_checks:` block, not an
executed result — a consequence of the same defect as clause 3(a).

### Clause 7 — MET
50 OPEN items (11 top-level + 39 construct-local) all dispositioned: 45 `still-open`, 3
`not-exercised`, 2 `blocking-hole`, **0 `resolved-by-instance`**. Both `resolved-by-instance` claims
raised by a workstream were overridden. That is the honest reading and it answers concern 9 squarely:
not one OPEN was normalised into a convenient default. Verdicts returned for the hypothesis, all 8
supporting definitions, 6 registries and 3 catalogs. No replacement schema, no V6, no normative
default, no build recommendation — I checked, and found none.

**W4's headline counts reproduce exactly** against the committed ledger, restricted to the 679
`model-X` rows: `exercised` 552 · `construct-pressure` 114 · `not-applicable` 10 · `blocked-by-OPEN`
3; causes `historical-evidence-gap` 81 · `model-defect` 73 · `unresolved` 33 ·
`project-evolution-candidate` 31 · `enforcement-gap` 30, on 176 caused rows.

### Clause 9 — NOT MET in the case matrix
**Zero** ledger rows dispositioned `construct-pressure` lack a cause — W4 supplied `unresolved` for
W1's 40 uncaused pressure rows rather than drop them, which is correct handling. But one case-matrix
row remains an unclassified pressure, and it is not a marginal one:
`supporting.EffectBoundary.relations.enforces` in `vnc-045-coverage.csv` carries
`disposition: exercised`, `enforcement_reality: specified-not-enforced`, and
`cause_classification: not-applicable` — on the software case's own stated **central custody
result**. Clause 12 names an unclassified pressure as `REWORKABLE` explicitly. W4 corrected the
reconciled row (`construct-pressure` / `enforcement-gap`); the case matrix was not corrected.

### Clauses 10 and 11 — NOT MET in the artifact
`findings-W4-adjudication.md` §7 challenges twelve candidates and rules **W1/CF-07 FAILS concern 17
(migration realism)** and **W1/CF-06 survives with a recorded defect**. The reconciled ledger — the
artifact synthesis will consume — **contains no occurrence of `CF-05`, `CF-06` or `CF-07`.** Five
rows carry `evolution_candidate_id: W1/unlabelled` and `evolution_challenge_result: not-challenged`.
A reader of the ledger alone would see three unchallenged candidates where W4 in fact challenged all
three and **failed one**. All 31 evolution rows do carry the five required analyses, both fit
verdicts and dual-representability fields with no blanks — the defect is identity and challenge
recording, not analysis.

---

## 2. Non-blocking observations (record; do not rework)

- **`wfh-008` instantiates zero `Capability` objects.** Defensible: R01 states the capability target
  is *proposed* `jurati-arch-002` and that *"no Unimatrix capability id or grade is advanced by this
  scope"* — encoding one anyway would have filled absence, and W1 correctly refused (its own
  circular-candidate rejection names exactly this). The consequence should be stated in synthesis:
  the entire `Capability` construct, the `capability_classification` registry, and I13/I14 rest on
  **W2's two objects alone**, in a two-case run.
- **Three mutually incompatible instance serializations** (W1 `instances:`, W2 `scopes:`/`goals:`,
  W3 `instances:`/`registered:`). W4 §9 correctly rules this a finding about M01 — `notation`
  describes the model file and never describes an instance document. It is also the mechanical cause
  of the clause-3 failure. Do **not** re-serialize to make a checker happy; the divergence is
  evidence.
- **W1 understates its own adverse finding** at `open:delegation_attenuation` (20 vs the executed 24
  undecidable derived Delegations). W4 caught this (D1) and noted it runs in the direction that
  flatters the model. Corrected in the ledger; the W1 prose still reads 20.

---

## 3. Answers to adversarial concerns 13–18

**13 — Circular conformance: NONE FOUND.** I read the `independent_reason` cell on all 31 evolution
rows and both `rejected_candidates` blocks. No surviving candidate's independent reason references
V5. Both workstreams identified and rejected their own circular candidate *before* adjudication —
W1 refused to instantiate a `Capability` for `jurati-arch-002`, and W2's `CF-R01` refused to rename
the program's `asserted` grade to `claimed` to land inside `values.evidence_grade`. The two changes
V5 would most prefer are the two that were rejected. That is the strongest available evidence against
force-fitting, and it is first-party.

**14 — Behaviour erasure: NONE FOUND.** Every surviving candidate is additive. W1/CF-03 is the test
case and passes explicitly: it declares `current_form_representable: false` and states that the model
defect **survives** its own evolution rather than being repaired by it. W1/CF-02 states its own limit
— a manifest detects drift and does not establish custody. No candidate deletes an exception path, a
proof obligation or a safe-interruption behaviour.

**15 — Authority laundering: NONE FOUND.** I checked the
`semantic_proof_authority_custody_preservation` cell on every evolution row. None relocates method
custody, decision authority, credentials, gate inputs or effect performance toward the governed
actor. Two move authority the safe way: W2/CF-05 puts enforcement on an externally custodied
boundary, away from every governed actor; W2/CF-03 moves narration away from the actors it governed.
W1/CF-04 explicitly refuses the laundering, raising evidence altitude to `reported-observation`
rather than `mechanical-observation` because capture custody stays inside the reporting actor.

**16 — Counterfactual confusion: NONE FOUND, and it is mechanically enforced.** `wfh-008-instance.yaml`
carries 191 ids and `wfh-008-counterfactual-instance.yaml` 4 — **zero overlap**, verified. The
counterfactual file declares `provenance_class: counterfactual`, `counterfactual: True`,
`historical_instance_ref: INST-WFH008-V5` and an explicit `anti_circularity_declaration`; the
validator emits `COUNTERFACTUAL BOUNDARY` notes and refuses to close inverse edges across the
boundary. W2's file declares `encodes_observed_history: False`. No counterfactual object appears in
any coverage or ledger count I measured.

**17 — Migration realism: ONE FAILURE, ONE RECORDED DEFECT — correctly found, incorrectly recorded.**
W4 §7's rulings are sound: W1/CF-07 fails because it targets a service outside this repository and
the run *"cannot cost it"*, and W1/CF-01's migration cost is now understated relative to its own
rationale. The defect is that **neither ruling reaches the ledger** (RW-4). Concern 17 is therefore
currently answered only in prose.

**18 — Cause discrimination: PERFORMED, and load-bearing — with one exception.** The four causes are
kept genuinely distinct and the separation drives the verdict: enforcement absences (zero enforced
authority in both cases; `EffectBoundary.enforces` empty everywhere) are reported as absence and did
not move the verdict; evidence gaps (every `vnc-045` Delegation an inference, no raw runner output,
no scope-decision record) prevented positive claims and did not move the verdict; the verdict moved
only on `model-defect` rows. `project-evolution-candidate` is never a residual bucket — all 31 rows
co-classify. **Exception:** the `EffectBoundary.enforces` row in `vnc-045-coverage.csv` is an
unclassified pressure (§ clause 9), which clause 12 names as `REWORKABLE`.

---

## 4. Rework instructions — round 1, four items

Execute all four; nothing here requires asking me a follow-up question.

### RW-1 — `vnc-045-coverage.csv` must be joined to its own instance · clauses 3, 9
Owner: W2.

Add to `artifacts/vnc-045-coverage-build.py` a verification pass that loads
`artifacts/vnc-045-instance.yaml` and, for every emitted row whose `x_class` is `core-field`,
`core-relation`, `supporting-field` or `supporting-relation` **and** whose `disposition` is
`exercised`, asserts that at least one object of the named construct carries a non-`None`,
non-empty value for the named key. Any row failing the assertion must be re-dispositioned
`not-applicable` (with the measured reason) or `construct-pressure` (with a cause classification) —
never left `exercised`. Write the pass/fail tally to `artifacts/vnc-045-coverage-build.out.txt` and
commit it.

The seven rows that fail this assertion today, with the populations I measured, are listed in §1
clause 3(b). Three of them (`core.Capability.relations.advances`,
`supporting.Delegation.fields.expires_at`, and `supporting.Role.relations.requires` at 3/13) carry
the witness string `instantiated in vnc-045-instance.yaml` with provenance `see instance`, which is
false as written; replace with the measured value.

`supporting.EffectBoundary.relations.enforces` must additionally receive a `cause_classification` —
it is at minimum `enforcement-gap`, and its own `enforcement_reality` cell already says
`specified-not-enforced`. `not-applicable` on that row is the unclassified pressure clause 12 names.

### RW-2 — `vnc-045-instance.yaml` must be mechanically validated at least once · clause 3
Owner: W2 (or W3, whichever holds the checker).

Both validators parse **zero objects** from that file. Either (a) add a section-name mapping option
to one existing checker so it reads the W2 encoding, or (b) commit a `vnc-045-validate.py` of the
same class as `wfh-008-validate.py`. Commit the executed `.out.txt` either way.

**Do not re-serialize `vnc-045-instance.yaml` to fit a checker.** The three-encoding divergence is
itself a finding about M01 (W4 §9) and must survive the fix. If the validation surfaces real
conformance findings, record them as findings — do not silently repair the instance to clear them.

### RW-3 — repair the reconciliation rule, then re-emit the ledger · clause 3
Owner: W4.

The rule in `findings-W4-adjudication.md` §4.1 must be conditioned on the `exercised` side actually
carrying a witness, not merely the label. Add a guard to the ledger build that refuses
`reconciled_disposition: exercised` for any row with no populated instance witness on either side,
and re-emit `reports/construct-pressure-ledger.csv`.

The six rows currently reconciled `exercised` with zero witness in either case are:
`core.Goal.relations.is_advanced_by` · `core.Capability.relations.advances` ·
`core.Capability.relations.delivered_by` · `core.Unit.relations.delivers` ·
`core.Event.relations.supersedes` · `supporting.Delegation.fields.expires_at`.

Each currently carries the boilerplate *"one history supplies a witness and the other does not"* —
replace it with the measured fact. `core.Event.relations.supersedes` additionally carries
`w4_adjudication: W3 ADVERSE at this path: F-E07=accepted-defect`; an adverse W3 result on a row
reconciled `exercised` with no witness needs its own sentence.

Restate the corrected §4.1 headline counts (currently 552 / 114 / 10 / 3 over 679 `model-X` rows).

### RW-4 — carry W4's own evolution rulings into the ledger · clauses 10, 11
Owner: W4.

`reports/construct-pressure-ledger.csv` contains no occurrence of `CF-05`, `CF-06` or `CF-07` on the
W1 side. Set `evolution_candidate_id` and `evolution_challenge_result` on these five rows to match
§7:

| Ledger row (`x_id`) | `evolution_candidate_id` | `evolution_challenge_result` |
|---|---|---|
| `supporting.Gate.relations.requires_assessor` | `W1/CF-05` | survives |
| `invariants.I10` | `W1/CF-06` | survives, recorded defect — independent reasonableness not evidenced inside the fixed alphabet |
| `notation.types` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |
| `core.Record.fields.content_digest` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |
| `M02.sanity.S3` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |

`W1/unlabelled` is not an identifier, and `not-challenged` contradicts §7 on all five rows.

### What is explicitly NOT in scope for this rework
Do not edit `organizational-data-model-v5.yaml` or any M-alphabet file. Do not author a V6, a
normative default for an OPEN item, a replacement schema, or a build recommendation. Do not perform
synthesis. Do not write Unimatrix. Do not re-encode either case instance beyond the dispositions
named above. Do not change any verdict in `findings-W4-adjudication.md` §8 — none of these four
defects touches the `revise` verdict or its clause mapping, and a rework that moves a verdict will be
read as the run correcting its result to clear its gate.

---

## 5. What I could not verify

- **That the run performed zero Unimatrix writes.** The artifacts consistently assert read-only
  access (W1's `T02` records four `context_graph` reads with `agent_id: factory-researcher` and no
  write), and I performed none myself. I have no independent audit surface on the graph and did not
  query it. This remains attested, not measured.
- **The dating of W2's `T01`/`T02`.** The two governing protocol files are living, unversioned
  documents read at `37c7b09a` rather than at the `vnc-045` delivery date. If they changed in
  between, every `Workflow`, `Gate`, `Role` and `Delegation` instance in the software case is
  anachronistic. W2 flagged it as its largest soft spot; W4 weighs it `unresolved` and material; I
  concur and cannot date them either.
- **The leader's `gh api` forge measurements** (W1 `T03`, W4 §3.2a). Neither W4 nor I re-executed
  them; they are network calls outside the zero-cost envelope. Recorded as leader-reported, adopted
  by nobody, and they change no ruling.
- **The ~400 encoded case objects.** Like W4, I did not re-derive either instance from the source
  alphabets. I verified the instance→coverage join mechanically (§1 clause 3) and went to source for
  the load-bearing measurements; where a row rests on a workstream's encoding judgment, my ruling
  rests on it too. Stated so it is visible, not to excuse it.

## 6. Transitive sources I ledgered

| Id | Source | Reason | Provenance |
|---|---|---|---|
| `X-AUD-01` | the SCOPE's pinned read-only clone `/tmp/claude-1000/-workspaces-arch-research/wfh-011-sources/unimatrix` @ `37c7b09a` | verify at source, rather than accept quotation: the squash-merge parentage and S06 non-ancestry; the 43-file `vnc-045` surface; the 226 / 153 gate-3c distribution and the absence of any `vnc-045` gate-3c artifact; SR-10's grade vocabulary | transport for `S02`–`S06` already named by the SCOPE extension; `git ls-tree` / `git show` / `git merge-base` only, read-only, zero cost, no content adopted beyond the measurements above |
| `X-AUD-02` | `product/research/wfh-008/SCOPE.md` header (already `R01`) | test W1's zero-`Capability` ruling against the history's own capability-target sentence rather than against W1's account of it | in-alphabet; read-only; no expansion |

No source outside M/R/S/X and the SCOPE's pinned corpus was consulted. All re-execution was
deterministic, local and read-only; zero external cost, no material compute.

---

## 7. Verdict, restated

**`REWORKABLE` — round 1 of at most 2.** Coverage clauses **3, 9, 10 and 11** are not met. Clause 12
independently compels `REWORKABLE` on the unclassified `EffectBoundary.enforces` pressure. Clauses 1,
2, 4, 5, 6 and 7 are met, several of them well.

**The failing clause, in one sentence:** six X items are counted `exercised` with no conforming
witness in either case, because the software case's coverage table never reads its own instance, no
executed checker can parse that instance, and the reconciler trusted the label instead of the
witness — which is precisely the "absence is never filled" prohibition, arrived at through a green
result from an instrument that was not looking at the artifact.

**What would clear it:** RW-1 through RW-4 as written. All four are mechanical, bounded, and none
requires re-encoding a case, touching the model, or moving a verdict.

**What is not wrong with this run, said plainly** — because a gate report that lists only defects is
not adjudicating. Every checker reproduces byte-identically. The model digest holds and the model was
parsed as-is. The X alphabet is complete against an independent enumeration with zero blank cells.
All 19 invariants have fixtures and all 115 are linked. Fifty OPEN items are dispositioned with
**zero** resolved by instance. The counterfactual/history boundary is enforced *mechanically*, not
merely declared. Both workstreams found and killed their own circular candidate before anyone asked.
W4 caught the alphabet divergence, caught the label-versus-evidence divergence, overrode seven
workstream dispositions against the direction that flattered the model, and disclosed the exact limit
that produced the defect I am ruling on. This is a strong run with a fixable seam, not a weak one.

**A `PASS` is necessary, not sufficient, and this is not a `PASS`.** The human owner rules on
sufficiency. I do not confirm my own ruling, and neither does the leader.
