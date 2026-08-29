# wfh-011 — tech-discovery coverage gate, re-audit round 2

**Auditor:** `factory-validator` · **Run:** `wfh-011` · **Theme:** `workflow-harness` · **Issue #70**
**Phase:** `tech-discovery` · **Confidence-required:** directional, research-scope, structure-only
**Audited state:** `main` at `c9f8213` · **Range re-audited:** `b755bb5..c9f8213` · **Date:** 2026-08-29
**Round-1 record:** `reports/gate-coverage.md`, sha256 `f6e19e83…1de77960` — **byte-unchanged**, preserved
as history. This is a new file; nothing in round 1 was edited.

## RULING — `PASS` (round 2 of at most 2)

All four round-1 rework items (RW-1…RW-4) discharged, each verified at the artifact by my own
re-implementation rather than by reading the rework's account of itself. Coverage clauses **3, 9, 10
and 11** move from `NOT MET` to `MET`; clauses **1, 2, 4, 5, 6, 7** remain `MET`; clause **12** fires no
`REWORKABLE` trigger. No clause-8 `SCOPE-FAIL` trigger is present.

**Three defects survive and are recorded below (§4).** None is a rework failure, all three are
pre-existing and newly visible, and all three constrain *how the coverage may be read* rather than
whether the gate clears. They are conditions on synthesis, and the owner should see them before ruling.

**Recommended grade movement: NONE.** This scope forbids graph writes and grade movement, and I
recommend none. I performed zero Unimatrix calls of any kind in this round.

**Independence.** I authored no part of W1, W2, W3 or W4, advised on none of them, and built no part of
the rework I am judging. I was given no count, no workstream verdict, no correction history and no
expected ruling. Every number below is one I measured.

---

## 0. What moved, measured before reading anything about it

`git diff --name-status b755bb5..c9f8213` — **12 files, all under `product/research/wfh-011/`**, nothing
else in the repository:

| | file |
|---|---|
| **A** | `artifacts/vnc-045-validate.py` · `vnc-045-validate.out.txt` · `vnc-045-coverage-build.out.txt` |
| **A** | `artifacts/w4-witness.py` · `w4-witness.json` · `w4-build-ledger.py` · `w4-build-ledger.out.txt` |
| **M** | `artifacts/vnc-045-coverage-build.py` · `vnc-045-coverage.csv` |
| **M** | `findings-W2-software-instance.md` · `findings-W4-adjudication.md` · `reports/construct-pressure-ledger.csv` |

**Unchanged, therefore carrying their round-1 verdicts forward:** `SCOPE.md`,
`findings-W1-research-instance.md`, `findings-W3-rejection-suite.md`, `reports/gate-coverage.md`, and
every W1/W3 artifact — `wfh-008-instance.yaml`, `wfh-008-counterfactual-instance.yaml`,
`wfh-008-coverage.csv`, `wfh-008-coverage-gen.py`, `wfh-008-validate.py`, `v5_model_check.py`,
`v5_instance_check.py`, `invalid-instance-matrix.yaml`, `rejection-results.csv`,
`traversal-results.csv`, `w3-baseline-instance.yaml`, `vnc-045-counterfactual-instance.yaml`,
`vnc-045-instance.yaml`.

### Digests — re-derived by me, not quoted

| artifact | sha256 | at `b755bb5` | at `c9f8213` | worktree |
|---|---|---|---|---|
| `organizational-data-model-v5.yaml` (**M01**) | `bf8e5536…9841060` | ✓ | ✓ | ✓ |
| `wfh-008-instance.yaml` (W1 case) | `b8a2e034…5dcdec16` | ✓ | ✓ | ✓ |
| `vnc-045-instance.yaml` (W2 case) | `c65b2ba9…cca6d9eef` | ✓ | ✓ | ✓ |
| `w3-baseline-instance.yaml` | `b307260b…c1f0be2e4` | ✓ | ✓ | ✓ |
| `wfh-008-counterfactual-instance.yaml` | `beadfb5d…53a26f3` | ✓ | ✓ | ✓ |
| `vnc-045-counterfactual-instance.yaml` | `75731daa…191fb876` | ✓ | ✓ | ✓ |
| `invalid-instance-matrix.yaml` | `20259e61…dbd7b7162` | ✓ | ✓ | ✓ |

**M01 did not move. Neither case instance moved. Neither counterfactual moved.** The single most
important thing a rework of this shape could have done wrong — re-serialize the W2 instance so a checker
would swallow it — was not done. RW-2 forbade it explicitly and the digest proves compliance.

### Re-execution — every checker run, none read from its log

I re-ran each script inside an isolated mirror of the run tree, with the hard-coded absolute roots
rewritten to the mirror, so nothing in the repository was written. Deterministic, local, read-only,
zero external cost.

| script | result |
|---|---|
| `v5_model_check.py` | reproduces; the only delta is the echoed model path (mirror root) |
| `wfh-008-validate.py` | **byte-identical** to `wfh-008-validate.out.txt` |
| `wfh-008-coverage-gen.py` | `wfh-008-coverage.csv` **byte-identical**, 468 rows |
| `v5_instance_check.py suite` | `rejection-results.csv` **byte-identical**, 115 fixtures |
| **`vnc-045-validate.py`** (new) | `vnc-045-validate.out.txt` **byte-identical**; exit **1**; 151 objects; **69 errors, 285 warnings, 14 notes** |
| **`vnc-045-coverage-build.py`** (changed) | `vnc-045-coverage.csv` **byte-identical**, 679 rows; `vnc-045-coverage-build.out.txt` **byte-identical** |
| **`w4-witness.py`** (new) | `w4-witness.json` **byte-identical** |
| **`w4-build-ledger.py`** (new) | `construct-pressure-ledger.csv` **byte-identical**, 705 rows; `w4-build-ledger.out.txt` **byte-identical** |

Round 1 could not check this: **the ledger had no committed generator.** It does now
(`w4-build-ledger.py`), and it regenerates the 899 KB ledger byte-for-byte from the two case matrices
plus its authored adjudications. The run's largest artifact went from unreproducible to reproducible in
this round, which nobody asked for and which is a real improvement in the audit surface.

---

## 1. Did each rework item discharge? — mechanically, at the artifact

### RW-1 — join the W2 coverage table to its instance · **DISCHARGED**

I wrote my own witness extractor for the W2 section encoding and joined it to
`vnc-045-coverage.csv` independently of `vnc-045-coverage-build.py`.

- **Remaining violations: 0.** Across all 679 rows, **no** row in the four checkable classes
  (`core-field`, `core-relation`, `supporting-field`, `supporting-relation`) is dispositioned
  `exercised` at a model path the instance populates on zero objects.
- **0 blank cells** in the whole file. Dispositions `exercised` 588 · `construct-pressure` 48 ·
  `not-applicable` 43 = 679.
- All seven rows named in round 1 §1 clause 3(b) moved, and each now carries a measured witness string
  beginning `MEASURED n/m …`. `supporting.EffectBoundary.relations.enforces` is `construct-pressure` ·
  `enforcement-gap` with evidence and `current_project_fit` filled — the round-1 clause-12 unclassified
  pressure is gone.
- `supporting.Role.relations.requires` correctly stays `exercised` at a measured 3/13, with the false
  boilerplate replaced.
- An eighth row moved that I did not ask for: `core.Goal.fields.north_star`, under a rule W2 named
  `W2-EXTRA` and **counted separately** so my rule and theirs stay independently re-executable. Its
  own committed witness already read *"Optional; absent"* under `exercised`. I confirm the measurement:
  1 of 3 Goals carries the key and the value is the placeholder `missing-history`. This is the round-1
  defect on a row my assertion did not reach — a self-extension against the run's own interest, not
  scope creep.

*Envelope on the corrected instrument, stated because it is not stated in the rework:* the join tests
**population**, not **reference resolution**. A row can pass on a value whose every target dangles. One
such value exists (`WF-01.binds → GT-01/GT-02/GT-03`, none of which is an id in the instance); the row
survives legitimately because `WF-02` resolves all five of its targets. No coverage row cites GT-01…03.

### RW-2 — validate `vnc-045-instance.yaml` at least once · **DISCHARGED**

`vnc-045-validate.py` exists, is of the same class as `wfh-008-validate.py`, parses **151 objects across
all 15 constructs** (round 1 measured **zero** through both prior validators), reproduces
byte-identically, and exits non-zero. It prints its own `argv` in the header *and* beside the `RESULT`
line, because the note count is invocation-sensitive — an instrument disciplining its own printed value
after being caught by a gate.

Every place the reader was bent to the data is printed under `READER ACCOMMODATIONS`, and the instance
digest is unchanged. **The reader was fixed to the data; the data was not fixed to the reader.**

### RW-3 — condition the reconciliation rule on the witness · **DISCHARGED**

`w4-witness.py` reads both case instances natively and measures populated witnesses per canonical X
path; a declared inverse counts only where an edge actually **closes**. I re-implemented the guard's
predicate from scratch and ran it over the committed ledger:

> **witness-bearing rows reconciled `exercised` with zero measured witness in both cases: 0** — of 329
> witness-bearing rows, 244 of them `exercised`.

The six rows round 1 named are all off `exercised`: `is_advanced_by`, `Unit.delivers` and
`Delegation.expires_at` to `not-applicable`; `Capability.advances`, `Capability.delivered_by` and
`Event.supersedes` to `construct-pressure` with causes. Every one carries the measured fact in place of
the boilerplate, and `core.Event.relations.supersedes` carries its own sentence tying `F-E07` to the
measured 0/32 and 0/30 — exactly what RW-3 asked for. §4.1's headline counts are restated with the
round-0 column **retained beside** the new one rather than overwritten.

I independently reproduced W4 §13.5's inverse table **exactly**, computing closure myself over both
instances: of the 34 declared-inverse X rows, **18 close in both cases, 6 in W1 only, 4 in W2 only, 6 in
neither** — and all 6 of the "neither" rows are off `exercised` in the ledger. W4's claim that W2's
"34 rows" concern is true of W2's own matrix and not of the reconciled ledger is correct, and I verified
it rather than accepted it.

> **CORRECTION — 2026-08-29 (post-close; appended, the paragraph above not edited).** The split
> **18 / 6 / 4 / 6** is superseded by **21 / 3 / 4 / 6**: `w4-witness.py`'s `entry_id()` omitted the
> `actor` key and returned `None` silently, undercounting three rows to zero. **The paragraph's
> conclusion is unaffected** — the six "neither" rows are the same six and are still off `exercised`
> in the ledger, and the reconciled-versus-matrix distinction it verifies stands. Full note in §4.1;
> commit `0405a14`;
> <https://github.com/dug-21/arch-research/issues/70#issuecomment-5462364469>.

### RW-4 — carry W4's evolution rulings into the ledger · **DISCHARGED**

All five named rows now carry the identifier and the ruling:

| ledger row | `evolution_candidate_id` | `evolution_challenge_result` |
|---|---|---|
| `supporting.Gate.relations.requires_assessor` | `W1/CF-05` | survives |
| `invariants.I10` | `W1/CF-06` | survives, recorded defect — independent reasonableness not evidenced inside the fixed alphabet |
| `notation.types` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |
| `core.Record.fields.content_digest` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |
| `M02.sanity.S3` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |

`W1/unlabelled`: **0 occurrences.** `not-challenged`: **0 occurrences.** All **31** evolution rows carry
all five analyses, both fit verdicts and the dual-representability fields, with zero blanks. A reader of
the ledger alone now sees the failure W4 ruled in §7.

---

## 2. Did anything move that no rework item asked for?

I tested every out-of-scope boundary round 1 §4 set, at the cell level rather than by reading commit
messages.

| boundary | result |
|---|---|
| no edit to M01 or any M-alphabet file | **held** — M01 digest identical; no file outside `wfh-011/` touched |
| no re-encoding of either case instance | **held** — both instance digests identical, both counterfactuals identical |
| no V6, replacement schema, normative default for an OPEN, or build recommendation | **held** — added lines contain none; the only occurrence of "build recommendation" is a workstream refusing to make one |
| no verdict moved in `findings-W4-adjudication.md` §8 | **held** — the §8 block is **byte-identical** (`24c38d55…f425e18`) across the range |
| no synthesis | **held** — no `REPORT.md`, no `reports/relevance.md`; `reports/` gained only the ledger it already had |
| round-1 gate report untouched | **held** — `gate-coverage.md` byte-identical |
| no Unimatrix write | **attested, not measured** — see §6 |

**Cell-level footprint of the whole range.** Ledger: 705 rows in, 705 out; **0 rows added, 0 removed**.
153 rows changed, across exactly twelve columns: `value` 119 · `provenance` 77 ·
`divergence_adjudication` 39 · `w4_adjudication` 39 · `reconciled_disposition` 30 · `w2_disposition` 8 ·
`divergence_class` 8 · `cause_classification` 7 · `evolution_candidate_id` 5 ·
`evolution_challenge_result` 5 · `classification_evidence` 1 · `current_project_fit` 1. `vnc-045-coverage.csv`:
679 in, 679 out, 0 added, 0 removed; 119 rows changed — exactly the 119 rows the join checked.

**`w1_disposition` changed on zero rows.** Every one of the 5 evolution-column changes is one of RW-4's
five. Every one of the 8 `w2_disposition` changes is one of RW-1's eight. The two single-cell changes
(`classification_evidence`, `current_project_fit`) are both on
`supporting.EffectBoundary.relations.enforces` and are required by clause 9 once that row gained a
cause. **I found no changed cell that does not trace to a rework item.**

**And the direction is measurable.** All 30 reconciled-disposition changes move *away* from
`exercised` — 9 to `construct-pressure`, 21 to `not-applicable`. **Zero rows gained `exercised`.** All 8
`w2_disposition` changes likewise. A rework that cleared its gate by inflating its coverage would show
the opposite sign; this one reduced its own claimed coverage by 30 rows and its own `exercised` count
from 552 to 522.

---

## 3. Newly-visible defects versus rework-introduced defects

This is the distinction the round turns on, so I adjudicate each new finding explicitly.

**An instrument that starts working surfaces defects that were always there. Only defects the rework
*created* are a rework failure.** The mechanical test I applied: is the defect present in an artifact
that is byte-unchanged over `b755bb5..c9f8213`, or in a cell the rework did not touch? If yes, it is
pre-existing and newly visible.

| # | finding | side |
|---|---|---|
| N1 | **69 conformance errors in `vnc-045-instance.yaml`** — 55 of 210 declared-inverse edges do not close, 11 Delegations omit required `effective_at`, 3 `WF-01.binds` targets do not exist | **pre-existing, newly visible.** The instance is byte-unchanged; the errors were unmeasurable because no executed checker could parse the file. Recorded as W2 `F-15`. |
| N2 | **W1's generator counts key presence, not value population** — `core.Goal.fields.north_star` reconciled `exercised` on W1's *"set on 2/2 instances"* while the instance carries `north_star: []` on both Goals | **pre-existing, newly visible.** W1's artifacts are byte-unchanged. This is the round-1 defect on the side round 1 credited as sound; W4 found it against its own case (§13.4) and against the audit's reading. |
| N3 | **33 zero-witness rows beyond my six**, 24 of which had to leave `exercised` | **pre-existing, newly visible** — they were invisible precisely because no reconciler measured a value. |
| N4 | **12 inverse rows in `vnc-045-coverage.csv` `exercised` on the boilerplate `instantiated in vnc-045-instance.yaml` while the declared inverse closes on zero edges in that case** | **pre-existing, newly visible.** Those rows are byte-unchanged; RW-1's four named classes did not reach `*-relation-inverse`. Disclosed by W2 itself (`F-15` scope note, §10) and by W4 §13.5. See §4.1. |
| N5 | **`core.Capability.versioned` reconciled `exercised` with zero instance witness in either case** | **pre-existing, newly visible** — found by me, this round, testing the §13.3 scoping. See §4.2. |
| N6 | **W4 §13.3's disclosed scoping counts do not reproduce** | **introduced by the rework, and non-substantive** — it is prose arithmetic in a paragraph the rework wrote. See §4.3. |

**Rework-introduced substantive defects: none.** N6 is a wrong number in a disclosure, not a wrong
artifact; the disclosure it decorates is otherwise sound and the guard it describes is provably correct.
N1–N5 are all adverse evidence — about the W2 encoding, about W1's generator, and about how much of the
coverage table was label rather than measurement — and every one of them is *recorded as a finding*,
none repaired away.

**The instances are the proof of that.** The corrected validator emitted 69 errors against
`vnc-045-instance.yaml`, and the file's sha256 is identical before and after. The cheapest way to clear
this gate was to add three Gate objects, eleven `effective_at` values and fifty-five back-references and
publish a clean run. Nobody did. The run published the 69 and left the artifact alone.

---

## 4. The three defects that survive

### 4.1 The disclosure I was asked to rule on — §13.3's scoping, and the 12 inverse rows

**What §13.3 says:** the guard applies to classes where "a populated instance witness" is a defined
concept — fields, relations, relation sub-keys, value members, registry seeds — and not to principles,
notation, invariants, invariant bindings, `extension_owner`, construct attributes, catalogs, excluded
items, OPEN items, review concerns, changelog or traversal rows, "whose `exercised` asserts consumption
during encoding or analysis, not an instance witness."

**My ruling: the scoping is legitimate, with one demonstrated escape.** I partitioned the 278
non-witness-bearing `exercised` model-X rows and asked of each class whether an instance witness is even
definable:

- `registry-seed-field` (65), `invariant-binding` (34), `registry` (18), `extension_owner` (19),
  `catalog` (9), `value-group` (9), `value-rule` (3), `registry-seed-empty` (3), `excluded` (10),
  `invariant` (11), `principle` (4), `notation` (4), `changelog` (2), `review-concern` (3),
  `traversal` (2), `open` (1) — 197 rows in total; these are
  model-declaration or analysis rows. `exercised` on them means the clause was consulted, and the
  invariants are separately witnessed by W3's 115 fixtures, the traversals by 67 executed rows. **The
  scoping costs nothing here.**
- `core-attr` / `supporting-attr` (81, completing the 278) is the class where the scoping is arguable, because one of its
  six suffixes — `versioned` — *is* instance-witnessable. I measured it: W1 populates `version` on
  every object of every `versioned: true` construct that has objects; W2 populates it on **none**. The
  15 `versioned` rows therefore hold on W1's witness — **except `core.Capability.versioned`**, and that
  is N5, ruled at §4.2.

**On the 12 inverse rows (N4) — this is the sharper question, and I am ruling it explicitly.** Clause 3
reads *"a conforming witness **in each case where the history supplies one**, or an explicit
`not-applicable` / `blocked-by-OPEN` / `missing-history` ruling."* Read strictly per-case, those 12 rows
in `vnc-045-coverage.csv` are filled absence: the row says `exercised`, the witness string says
`instantiated in vnc-045-instance.yaml`, and the declared inverse closes on zero edges in that instance.

I rule clause 3 **MET** notwithstanding, for three reasons I want on the record because a different
reading is defensible:

1. **The reconciled artifact is correct, and I proved it independently.** All 34 inverse rows resolve
   correctly in the ledger; the 6 with no witness in either case are all off `exercised`. Synthesis
   consumes the ledger.
2. **Clause 3's alternative limb is satisfied at the class.** W2 named the rows, published the measured
   count (55 of 210), stated that it did not re-disposition them and why, and asked the re-audit to
   rule (`F-15` scope note, §10). W4 measured the same set from both sides and published the 18/6/4/6
   split. That is an explicit ruling with the evidence attached, not silence.
3. **RW-1's text named four classes and `*-relation-inverse` was not among them.** W2 complied with the
   instruction and refused to exceed it — which is the correct posture for a party reworking its own
   artifact under an auditor's specification, and the opposite of a party quietly widening a fix until
   the complaint disappears.

**What this costs, and what synthesis may not say:** `vnc-045-coverage.csv` overstates the software
case's inverse coverage on 12 rows. Any statement of the form *"the software case exercises N declared
inverses"* taken from that matrix is wrong by up to 12. The correct figure for the software case is
**22 of 34 declared inverses closing at least one edge**; the correct figure for the *run* is **28 of
34**. Those are my numbers, not the run's.

> **CORRECTION — 2026-08-29 (post-close; appended, nothing above edited or withdrawn).**
>
> **Old figure → new figure.** The software case's declared-inverse coverage is **25 of 34**, not
> **22 of 34**; the rows on which the boilerplate is false as a software-case witness number **9**,
> not **12**. The cross-case figure — **28 of 34 closing in at least one case** — is **unchanged**;
> it was already correct. The corrected split is **21 close in both cases, 3 in W1 only, 4 in W2
> only, 6 in neither** (published as 18 / 6 / 4 / 6).
>
> **Mechanical cause.** `artifacts/w4-witness.py`'s `entry_id()` searched the keys
> `('id','ref','target','to')`, **omitted `actor`**, and returned `None` **silently** when no key
> matched. `vnc-045-instance.yaml` keys its attributed relation entries on `actor:`, so all **21**
> such entries — 16 on `Role.assigned_to`, 5 on `Skill.held_by` — were scored as non-closing edges.
> Three rows were undercounted to zero: `core.Actor.relations.has_skill.inverse` (0 → 5),
> `supporting.Skill.relations.held_by.inverse` (0 → 5),
> `supporting.Role.relations.assigned_to.inverse` (0 → 16). The same run's
> `artifacts/vnc-045-validate.py` read the same file correctly, searching
> `('actor','target','ref','id')`, disclosing the accommodation, and **erroring** rather than
> returning `None` — two readers of one file, one of which failed silently. `w4-witness.py` now does
> both, and `artifacts/w4-witness.json` is regenerated from it.
>
> **`wfh-008` is unaffected.** `wfh-008-instance.yaml` carries **zero** dict-form relation entries,
> so the omission could not reach it: all 268 of its witnessed paths and every one of its inverse
> counts are identical before and after.
>
> **Downstream blast radius: empty.** `reports/construct-pressure-ledger.csv`, regenerated from the
> corrected witness map into a scratch location and diffed, is **byte-identical** to the committed
> ledger (md5 `54c035cda9a7a85d346d5fd6e8e2f6b6`, 706 lines), which is therefore left untouched. The
> mechanism: the ledger's RW-3 guard fires only where **both** cases measure zero, and all three
> corrected rows already carried a non-zero `wfh-008` witness (49, 49, 21). **No disposition,
> cause, adjudication or verdict moves.** The seven-entity `revise`, `current-project fit: revise`
> and `post-bounded-evolution fit: revise` rest on bar clause 2 and the two reject limbs, not on
> inverse closure; the round-2 `PASS` and its six clause verdicts stand exactly as ruled, and this
> note does not re-rule them.
>
> **Direction of the error, checked rather than repeated.** It ran **against** the run's interest —
> it understated coverage and overstated the defect count — so correcting it moves both figures in
> the **flattering** direction (22 → 25, 12 → 9). Stated plainly rather than as vindication: a
> correction that improves the corrector's own numbers earns more scrutiny, not less. The corrected
> reader was therefore also run in strict mode across both instances; every dict-form relation entry
> resolves a target key, so nothing is now failing silently in the opposite direction.
>
> **What was deliberately not done.** Neither instance was re-serialized: the finding is that the
> reader is fixed to the data, never the data to the reader. The referral to the owner on clause 3's
> strict per-case limb is unchanged in kind and now concerns **9** rows rather than 12; it remains
> the owner's call and is not touched here. The stale **22 of 34** also stands, uncorrected, in
> `reports/relevance.md` (three places) and `findings-W4-adjudication.md`; extending the correction
> to those surfaces is the owner's call and outside this correction's scope.
>
> **First raised:** Issue #70 comment
> <https://github.com/dug-21/arch-research/issues/70#issuecomment-5462364469>. That comment recorded
> the retro's recomputation (25 / 9); this correction independently reproduced **both** the erroneous
> 18 / 6 / 4 / 6 split and the corrected 21 / 3 / 4 / 6 split from the committed generator before
> adopting either.

### 4.2 `core.Capability.versioned` — the one demonstrated escape from the scoping

```
core.Capability.versioned   reconciled: exercised   w1=exercised  w2=exercised  divergence: agree
  value: [W1] versioned=True; the checker enforces presence/absence of a version on every instance
      || [W2] instantiated in vnc-045-instance.yaml
```

W1 instantiates **zero** `Capability` objects, so its checker enforced nothing at this construct. W2
instantiates two and populates `version` on neither — on any object, in fact. The row is `exercised`
with no instance witness in either case, and it survives only because construct-attr rows sit outside
the guard's scope.

Materiality is low — one row of 679, on a construct already ruled `revise`, where `exercised` under the
class's own disclosed semantics means "the attribute was read during encoding," which it was. But
W1's witness sentence is misleading at a construct with no instances, and I record the row so that no
reader takes it as evidence that any `Capability` was ever versioned. **Nothing in this run has
witnessed a versioned Capability.**

### 4.3 §13.3's two counts do not reproduce

§13.3 states the guard covered **274** `exercised` rows and left **269** outside it. Neither figure is
emitted by any executed artifact; both are authored in prose. Measured from the committed ledger:

| | W4 §13.3 | measured |
|---|---:|---:|
| witness-bearing rows `exercised` when the guard ran | 274 | **268** |
| non-witness-bearing rows `exercised`, left outside | 269 | **278** |
| sum | 543 | **546** |

546 is checkable against §13.2's own state-B row (`exercised` 546), which is correct; the split of it is
not. The derivation: 24 rows left `exercised` under the guard and 3 more moved `not-applicable` →
`construct-pressure` (27 changed in total), so 244 + 24 = 268 witness-bearing were `exercised` before it
ran, against 278 non-bearing that were never in reach.

No artifact depends on these two numbers, and every other count in §13 that I checked reproduces
exactly — 39 annotated, 27 changed, 18/6/4/6 on the inverses, the six, the 33 beyond the six, the
§4.1 and §13.2 tallies. But the error runs in the direction that **understates the excluded set by
nine**, and it appears in the one paragraph whose whole purpose is to disclose what the guard did not
cover. In a run whose subject is printed values that have quietly stopped naming one thing, a
hand-authored count inside a disclosure of scope is the wrong place to leave arithmetic unchecked.

---

## 5. Clause-by-clause, round 2

| # | Coverage clause | Round 1 | **Round 2** |
|---|---|---|---|
| 1 | M/R/S dispositioned; transitive sources ledgered before use | MET | **MET** — no source added in the range; W4 §13.8 states none and the citations block is unchanged; the two new instruments read only M01 and the two case instances, all in-alphabet |
| 2 | Every X item has one reconciled disposition | MET | **MET** — 705 rows (679 `model-X` + 23 + 3 appendix), **0 rows added or removed**, **0 blank cells**; M01 unchanged so my round-1 independent 663-item enumeration still resolves |
| 3 | Conforming witness per case, or an explicit ruling; **absence never filled** | **NOT MET** | **MET** — 0 witness-bearing rows `exercised` with zero witness in both cases, verified by my own predicate over all 329; residue at §4.1/§4.2 |
| 4 | Falsifiable rules have fixtures; results classified | MET | **MET** — artifacts byte-unchanged; suite re-executed byte-identical, 115 fixtures |
| 5 | Registries/catalogs/seeds/extension points exercised or dispositioned; empty seeds not invented | MET | **MET** — the three `registries.*.seeded<EMPTY>` rows still state explicitly that the empty seed was not filled |
| 6 | Required traversals + declared inverses demonstrated or recorded as a hole | MET | **MET** — both traversal rows unchanged and executed; **the inverse limb is now measured rather than asserted**: 28 of 34 close in at least one case, the other 6 are off `exercised` with causes. Round 1 recorded an altitude difference here; it has closed on the ledger and remains open in W2's matrix (§4.1) |
| 7 | W4 reconciles every row, dispositions every OPEN, returns retain/revise/reject, drafts no replacement | MET | **MET** — **0** rows reconciled `resolved-by-instance`; §8 verdict block byte-identical; no replacement schema |
| 9 | Every failure/pressure row carries ≥1 cause with evidence | **NOT MET** | **MET** — ledger: 124 pressure rows, **0 without a cause**. `vnc-045-coverage.csv`: 48 pressure rows, **0 without a cause**. The round-1 `EffectBoundary.enforces` unclassified pressure is classified `enforcement-gap` with evidence in **both** the case matrix and the ledger |
| 10 | Every evolution candidate: five analyses, separate identifiers, both fit verdicts | **NOT MET** | **MET** — 31 rows, 0 missing analyses, 0 `W1/unlabelled` |
| 11 | W4 independently challenges each candidate; current verdict preserved | **NOT MET** | **MET** — 0 `not-challenged`; `CF-05`/`CF-06`/`CF-07` present with §7's rulings including the failure; §8 unchanged |
| 12 | Auditor answers 13–18; circularity / erasure / conflation / unclassified pressure ⇒ `REWORKABLE` | **fired** | **no trigger fires** — see §5.1 |

**Clause 8 `SCOPE-FAIL` triggers, all absent:** no unreconciled X row (0 blanks, 705/679, 0 rows lost);
no silent model normalization (M01 digest holds, the new validator prints six reader accommodations
rather than editing the data, and both entry points abort on a digest mismatch); no missing applicable
rejection (115 fixtures re-executed byte-identical, all 19 invariants covered); no unresolved premise
mismatch (the SCOPE's Premise Recheck closes S1 at exactly the pinned digest).

### 5.1 Concerns 13–18, re-answered against the changed artifacts

- **13 circular conformance — NONE.** The evolution analysis columns are byte-unchanged apart from the
  two RW-4 identity columns; both self-rejected circular candidates stand.
- **14 behaviour erasure — NONE.** No candidate changed. Nothing was deleted from either instance;
  0 rows removed from either matrix.
- **15 authority laundering — NONE.** `semantic_proof_authority_custody_preservation` unchanged on
  every row. The three new `enforcement-gap` classifications all *record* absent enforced authority;
  none relocates custody toward a governed actor.
- **16 counterfactual confusion — NONE, still mechanically enforced.** Both counterfactual files are
  byte-unchanged; the new validator independently re-verifies zero id overlap and emits
  `COUNTERFACTUAL BOUNDARY`.
- **17 migration realism — the failure now reaches the ledger.** RW-4 discharged; this is the clause
  that was answered only in prose in round 1.
- **18 cause discrimination — PERFORMED, and the round-1 exception is gone.** `project-evolution-candidate`
  is on 31 of 183 caused rows and never residual. The 7 new cause classifications are 4
  `historical-evidence-gap`, 3 `enforcement-gap`, 1 `model-defect` (on `Event.supersedes`, jointly) —
  evidence gaps and enforcement absences recorded as absence, with the verdict moving only where a
  model defect was found. **Zero unclassified pressures in either the ledger or the W2 case matrix.**

---

## 6. What I could not verify

- **That the run performed zero Unimatrix writes.** I made no `context_*` call of any kind this round.
  W4 states no source was added and no graph write occurred; the citations block is byte-unchanged,
  which corroborates the source claim but not the write claim. As in round 1: **attested, not
  measured**, and the run's own `unimatrix-access.md` says recorded attribution is self-assertion, not
  attestation.
- **The dating of W2's `T01`/`T02`.** Unchanged and unchangeable from inside the alphabet. Still the
  largest soft spot in the software case, still weighed `unresolved`, still carried forward.
- **The round-0 provenance of the ledger.** `w4-build-ledger.py` was committed in this range, so the
  ledger is now reproducible going forward; I cannot re-derive the state it held at `b755bb5` from a
  committed generator, only diff it. That is an improvement realised, not a defect.
- **The ~400 encoded case objects.** As in round 1, I did not re-derive either instance from its source
  alphabet. I verified both instance→coverage joins and the instance→ledger witness map mechanically,
  and I re-measured every load-bearing number in this round myself. Where a row rests on a workstream's
  encoding judgment, my ruling rests on it too — and N1 now quantifies how much that judgment cost:
  69 conformance errors in the software case's instance.

## 7. Transitive sources I ledgered

**None.** This round consulted only artifacts already inside the run's alphabet, re-executed locally.
Round 1's `X-AUD-01` and `X-AUD-02` stand unchanged and were not re-used. Zero external cost, zero
network, no material compute.

---

## 8. Verdict, restated

**`PASS` — round 2 of at most 2.** RW-1, RW-2, RW-3 and RW-4 all discharge at the artifact. Coverage
clauses 3, 9, 10 and 11 move to `MET`; 1, 2, 4, 5, 6 and 7 remain `MET`; clause 12 fires nothing; no
clause-8 `SCOPE-FAIL` trigger exists.

**The one place this ruling could reasonably go the other way,** stated so the owner is ruling on a
reading and not on my conclusion: clause 3's *"in each case where the history supplies one"* limb, read
strictly per-case, is not met on 12 inverse rows of `vnc-045-coverage.csv` (§4.1). I ruled it MET
because the reconciled ledger — the artifact synthesis consumes — is provably correct on all 34, and
because the shortfall is named, counted and published by the workstream itself rather than concealed. An
owner who wants the case matrices to stand alone as coverage evidence has a legitimate basis to withhold
on that limb. That is the owner's call, not mine, and the remedy is one line of the same join.

**What synthesis must carry forward, and may not overstate:**
1. The software case's declared-inverse coverage is **22 of 34**, not what its matrix implies; the
   run's is **28 of 34**.
2. `vnc-045-instance.yaml` carries **69 conformance errors** against M01 as parsed. Every claim resting
   on the software case rests on an instance with that error load, now measured.
3. **W1's coverage generator counts key presence, not value population.** The reconciled ledger is
   protected at witness-bearing paths because the guard measures the instance directly; W1's own
   468-row matrix is not.
4. Nothing in this run witnesses a versioned `Capability`, and 205 canonical X rows still rest on a
   single case.

> **CORRECTION — 2026-08-29 (post-close; appended, item 1 above not edited).** Item 1's **22 of
> 34** is superseded by **25 of 34**, and the 12-row count by **9**; the run's **28 of 34** is
> unchanged. Cause: `w4-witness.py`'s `entry_id()` omitted the `actor` key and returned `None`
> silently, so 21 attributed relation entries in `vnc-045-instance.yaml` were scored as
> non-closing. Full note, blast-radius measurement and direction ruling in §4.1 above; first
> raised at <https://github.com/dug-21/arch-research/issues/70#issuecomment-5462364469>.
> Items 2, 3 and 4 are unaffected, and the `PASS` and its clause verdicts are not re-ruled.

**What is right about this rework, said plainly.** It was scoped exactly to what was asked and stopped
there. It reduced its own claimed coverage by 30 rows and increased it on none. It left both case
instances byte-identical while its own new instrument emitted 69 errors against one of them, and
published the errors. It found and reported the same defect on the side my round-1 report had credited
as sound, unprompted and against its own case. It refused to move a verdict, and then went and checked
whether the corrected evidence *should* have moved one, reporting the near-miss on `Goal` rather than
staying silent. It made the run's largest artifact reproducible from a committed generator for the first
time. A rework that clears a gate by quietly repairing the artifact the corrected instrument complained
about would look nothing like this.

**A `PASS` is necessary, not sufficient.** The firewall gate is the human owner's ruling; this report is
its input. I recommend **no grade movement**, and this run remains directional and structure-only. I do
not confirm my own ruling, and neither does the leader.
