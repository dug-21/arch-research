# wfh-011 W4 — Independent cross-case adjudication and construct pressure

**Run:** `wfh-011` · theme `workflow-harness` · research-scope, **DIRECTIONAL** · phase `tech-discovery` ·
[Issue #70](https://github.com/dug-21/arch-research/issues/70)
**Workstream:** W4 — independent adjudicator. I authored none of W1, W2 or W3.
**Author:** `factory-researcher` (W4) · 2026-08-29
**Status:** findings only. **Zero Unimatrix writes.** No node, no edge, no tag, no grade movement, no
`proven`. No replacement schema, no V6, not even a sketch. No edit to `organizational-data-model-v5.yaml`
or any M-alphabet file. No build recommendation, no implementation plan, no normative default for any
OPEN item.

---

## 0. What I did, and what a result in this file means

I received W1–W3's **outputs**, not their conclusions. I opened every file myself, **re-executed every
checker rather than trusting a committed log**, re-derived the digests, and went to source whenever a
row's provenance needed checking.

**Nothing in this file is evidence that anything is enforced anywhere.** `M01.meta.enforcement_reality`
says no common cross-program checker implements this model. Every "rejection" below is a property of a
checker some workstream wrote from a YAML file. Every `enforcement-gap` is reported as an absence and
is **never** converted into a model failure or a claimed refusal.

### 0.1 Model verification — I re-hashed M01 myself

```
$ sha256sum product/factory/proposals/organizational-data-model-v5.yaml
bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060   (561 lines)
```

**MATCHES the pin** in the SCOPE's *Premise Recheck* and *Human resume* extensions. Verified again at
the end of my run, after five W1 commits landed mid-flight: unchanged. Parsed **as-is** — nothing
quoted, normalised, patched in memory, or imported from M02's prose. Tooling: PyYAML 6.0.3, yq v4.44.3.

### 0.2 Re-execution — every checker, not one log trusted

| Checker | Re-run result |
|---|---|
| `wfh-008-validate.py` (W1) | **Byte-identical** to the committed log. `RESULT: 0 errors, 33 warnings, 8 notes` |
| `wfh-008-coverage-gen.py` (W1) | **CSV byte-identical.** 468 rows; 339/76/49/3/1 |
| `vnc-045-coverage-enumerate-x.py` (W2) | 679 X items; digest guard fired and matched |
| `vnc-045-coverage-build.py` (W2) | **CSV byte-identical.** 679 rows; 596/47/36 |
| `v5_model_check.py` (W3) | **Log byte-identical** |
| `v5_instance_check.py validate` (W3) | baseline: 0 findings |
| `v5_instance_check.py suite` (W3) | **CSV byte-identical.** 82 / 18 / 9 / 5 / 1 |
| `v5_instance_check.py traverse` (W3) | **CSV byte-identical.** 67 rows |
| `gen_inverse_fixtures.py` (W3) | regenerates section B deterministically |

**Every artifact in this run is deterministically reproducible.** That is a real and unglamorous
positive, and it is why the divergences below can be adjudicated on evidence rather than on authority.

### 0.3 Mid-run instability — five W1 commits landed while I worked

`git log --oneline -- product/research/wfh-011/` at my start: `1dd034f` (W1) · `536103c` (W2) ·
`e831ca1` (W3). By my finish it read `72b98b9 · 83b75ad · f36f716 · dcdf408 · 1dd034f · …`. **I re-read
every changed file and re-ran the whole W1 chain against final HEAD; this adjudication is against
`72b98b9`, not `1dd034f`.** The corrections are treated in §3.

**Provenance of the trigger, recorded because it bears on my independence:** the `research-leader`
flagged W1's baseline claim to me before I reached it, later flagged that its *own* first message to me
was wrong, and finally withdrew its "working assessment" as a conclusion that was not its to hand me.
**I re-executed every measurement in all three messages and adopted no characterisation from any of
them.** My own execution found something none of them had assembled (§3.2a). I reached the same
disposition the leader had offered and withdrawn — independently, from the committed files, and after
its withdrawal — which is why it appears below as my ruling rather than its assessment.

---

## 1. Headline

**Verdict on the seven-entity hypothesis: `revise`.**

**`current-project fit: revise`** · **`post-bounded-evolution fit: revise`**. The pair is identical, and
that identity is the run's sharpest single result: **not one of the ten surviving project-evolution
candidates repairs a single model defect.** A better post-evolution result did not materialise, so
there was nothing for it to conceal.

Four findings carry the verdict.

1. **No material case behaviour requires an eighth common core entity.** Across 679 reconciled X rows
   and 115 executed rejection fixtures I found no row that does. W3 offered this reading and asked me
   to test rather than adopt it; I tested it and it holds. Every adverse row resolves to a missing
   *binding*, a closed vocabulary, an untyped carrier, or an evidence/enforcement gap — all
   `revise`-shaped under the SCOPE's literal bar.

2. **But the retain bar fails on its second clause.** Retain requires that *every material semantic
   fits typed structure or a conforming registered extension*. At least one does not: the observed
   program's evidence-grade value `asserted` has **no conforming home** — `values.evidence_grade` is
   `status: RESOLVED`, closed at `[missing, claimed, partial, proven]`, with no registry and no
   `extension_owner`. I verified the program's vocabulary at source (§4.3). Both cases refused the
   circular fix. Neither retain nor reject applies; `revise` does.

3. **`Capability` has no fully conforming witness in either case.** W1 instantiated zero. W2
   instantiated two — and `CP-02` carries `grade: UNREPRESENTABLE` and `done_when: missing-history`,
   both `required: true`. **This settles W1's flag #4 in a direction neither case could reach alone:**
   `Capability` is not untestable (W2 reached it), but a seventh of the core hypothesis still has no
   clean instance anywhere in the run.

4. **Zero OPEN items are resolved by these instances.** After adjudication: **45 still-open,
   3 not-exercised, 2 blocking-hole, 0 resolved-by-instance.** Both `resolved-by-instance` claims in
   the run were made by one workstream and contradicted by the other; I ruled against both (§5).

---

## 2. Outputs

| Artifact | Path |
|---|---|
| This file | `/workspaces/arch-research/product/research/wfh-011/findings-W4-adjudication.md` |
| Reconciled ledger | `/workspaces/arch-research/product/research/wfh-011/reports/construct-pressure-ledger.csv` |
| Witness extractor (rework round 1, §13.1) | `/workspaces/arch-research/product/research/wfh-011/artifacts/w4-witness.py` |
| Measured witness counts | `/workspaces/arch-research/product/research/wfh-011/artifacts/w4-witness.json` |

**705 ledger rows: 679 canonical model-X rows + 23 appendix rows (W1's instance-level registry
extensions, which are not model X items) + 3 appendix rows (W3 fixtures finer than any X path).** The
appendix rows are labelled `row_scope` and are **excluded from every X count**; they exist so that
nothing any workstream produced is silently dropped. Zero silent blanks; zero pressure rows without a
cause.

---

## 3. FLAGS — read these first

### 3.1 `accepted-defect` — 18 reproduced, and I can reproduce every one

W3's suite is deterministic and I re-ran it: **18 fixtures violate a rule M01 states and the checker
admits them.** Nine sit in the `mechanical × accepted-defect` cell — rules whose **both operands are
already typed** and which M01 simply never writes the sentence to join. Ranked by consequence:

| Fixture | What is accepted | Why it matters |
|---|---|---|
| `F-E12` | `Capability.grade: proven` with `evidence_record_refs` **deleted** | I9 and `evidence_grade.rule` state the garage's own firewall (`CLAUDE.md`, D7) and **no typed structure carries it.** `evidence_record_refs` is `required: false` and no rule makes it conditional on `grade`. |
| `F-E13` | `proven` on a behavioural claim citing only a `directional` Record | `Record` declares `evidence_altitude`; **`Capability` and `Technology` declare none**, so the altitude comparison I9 demands has only one typed side. |
| `F-E17` | `credential-issue` requested under a Delegation granting only `repository-write` | `effect_grants` and `requested_effect` are **both registry-typed**. This is the one authority check that could have been fully mechanical, and it is the one M01 does not write. |
| `F-E18` | a request aimed at a boundary whose `effect_classes` exclude it | same shape |
| `F-E19` | `can_refuse: false` on the boundary two Delegations name as their enforcement | the field whose own definition reads *"a boundary that cannot refuse enforces nothing"* is **read by no rule in M01** |
| `F-E26` | an **A5** Delegation derived from an **A1** parent | `autonomy_tier` is a map of definitions with **no declared order**. A5 is `held_by: human`. This is the theme's stated boundary — *keep consequential authority outside the agents being governed* — unenforced. |
| `F-E27` | `resource_ceiling: external_cost 500` derived from a parent granting `0` | `map`, interior undefined |
| `F-E06` | a human-authored account labelled `mechanical-observation`, human named as `instrument` | `instrument` is an untyped key inside `Event.extension`; `Actor.actor_type` is a typed enum. Every ingredient exists; the join does not. |
| `F-E09` | a `pass` gate outcome over an assessment recording `independence_check: false` | I7's fail-closed precondition is unreachable while the outcome *vocabulary* is checked |
| `F-E11` | `missingness: none` against an empty `evidence_set` | the model checks *that* missingness was declared, never *what* it says |
| `F-H09` | `lesson` **registered** as an event type, then emitted | the sharpest pair in the run: unregistered `lesson` is rejected (`F-A17`); registered `lesson` is accepted silently. One registry write by the program the exclusion binds. |
| `F-E08` | `effect_completed` spanning both effect seeds | reintroduces the merged effect event `excluded` forbids |
| `F-G02` | conforming, typed-clean data stating the executing agent holds the boundary's credentials | `EffectBoundary` has **no relation to any Actor**; nothing can contradict it |
| `F-E07` | an Event that supersedes itself | M01 declares `acyclic` three times elsewhere; the three `supersedes` relations declare none |
| `F-A15` | `effect_disposition: "maybe"` | the rule is stated in full and there is no typed carrier for the value it governs |
| `F-A16` | `coupling: "eventual"` | **`values.coupling` is referenced by no field anywhere in M01** |
| `F-H11` | autonomy carrying an ungranted effect | the exclusion is honoured in the *shape* and unenforced in the *values* |
| `F-E33` | `specified-not-enforced`: I19 — extensions may not weaken invariants | the invariant guarding every other invariant against the registries is the least checkable thing in the file |

**Adjudication: all 18 are `model-defect`, all 18 are `revise`-shaped, and none requires an eighth core
entity.** They concentrate almost entirely in one place — the Event layer and the firewall running
through it — because everything consequential lives in `Event.extension` (`map`, interior undefined),
`Event.subject_refs` (bare `list`), or a `rule:` string with no bindable subject.

### 3.2 Checker result contradicts author prose — three cases

My brief says the executed result governs. It does.

| # | Author prose | Executed result | Adjudication |
|---|---|---|---|
| **D1** | W1 §6.11 and CSV row `open:delegation_attenuation`: *"Twenty derived Delegations are UNDECIDABLE"* | `wfh-008-validate.out.txt` line 109: **`24 derived Delegations`** (26 derived in total, counted from the instance) | **24 governs.** W1 **understates** its own adverse finding. Corrected in the ledger. |
| **D2** | W1 §4.5: *"19 Actors resolve"* on the Actor→Attempt traversal | the log lists **21** Actors resolving | **21 governs.** W1 understates a positive. |
| **D3** | Leader message 1: the pre-rebase objects are *"a property of this working copy"*; W1 correction 1: they are *"published on `origin`"*; leader message 2: they survive only via *"a stale, unpruned remote-tracking ref"* | **All three incomplete.** I ran it myself | see §3.2a |

Neither D1 nor D2 changes a disposition or a verdict. Both are magnitude errors, and D1 runs in the
direction that flatters the model.

#### 3.2a The branch question — my own execution

```
$ git ls-remote --heads origin        -> 9 heads; NO workflow/* among them
$ git fetch --prune --dry-run origin  -> - [deleted] (none) -> origin/workflow/agentic-organization-reframe
$ git branch --contains 17ebf2e       -> workflow/agentic-organization-reframe   (a LOCAL branch, a real ref)
```

The accurate statement, which no message I received had assembled: the ten pre-rebase ids are (a)
**not ancestors of `main`**, (b) **on no branch published on `origin`** — the remote branch is gone,
(c) retained in this working copy by a **real local branch**, not merely by the stale remote-tracking
ref, and (d) reported by the leader as still answerable through the forge API by full oid — **which I
did not re-execute**, because it is a network call outside my zero-cost envelope and, more to the
point, cannot change my ruling: a forge answering for an unreachable object is an unguaranteed
retention behaviour, not a durability property a research method may rest a citation on. Recorded as
leader-reported, not adopted.

**This strengthens, not weakens, W1's CF-01 residual** — and W1 arrived at the same three-way reading
independently at commit `f36f716`, including the local-branch distinction. I note that I can see the
direction it cuts, precisely so that the auditor can see I did not take it on anyone's word.

### 3.3 Nothing contradicts a load-bearing premise of the SCOPE

- **M01 digest matches the pin** and did not move across five mid-run commits.
- **S1 is closed at this digest** — independently re-confirmed by all three workstreams and by me.
- The squash-merge property, the 43-file `vnc-045` surface, the PR-head ordering and the M01/M02
  digests all reproduce as the leader's S-alphabet extension recorded them.
- **W1's escalated flag is correctly retracted.** Its original claim that the baselines "dangle" was
  raised as contradicting a load-bearing premise; it does not, and W1 has downgraded it to a
  documentation defect in `M04`. I independently confirm that downgrade: `M04`'s R08 ledger pins the
  **post-rebase** oids and **all twelve are ancestors of `main`** (I ran it). `M04`'s *sentence*
  attributing the mismatch to "displayed abbreviations" is wrong — `6acc952` and `7cf95b20` are
  distinct objects with identical trees — but `M04`'s *table* is correct and usable. **The leader
  offered this same disposition and then withdrew it as a conclusion not its to hand me; I record that
  I reached it from the committed files, and that its arrival did not shorten my execution.**
- **W1's claim about the size of its own corrections is verified, with one qualification.** Across the
  full range `1dd034f..72b98b9` exactly **2 of 468** rows changed (`invariant:I1`, `notation:identity`),
  with **no `disposition` and no `cause_classification` change** — I diffed field-by-field rather than
  accept the assertion. **Qualification:** "text-only" understates it. `current_project_fit` and
  `post_evolution_fit` are **verdict-bearing fields** and both moved on both rows (`REPRESENTABLE BUT
  UNVERIFIABLE` → `REPRESENTABLE`). The claim is accurate where it is precise and generous where it is
  loose.

**Nothing here implies a change to V5 or to the SCOPE.** Every adverse finding is recorded as pressure
against the pinned model, which is exactly what the scope asked for.

### 3.4 One structural defect in the run itself — the two workstreams enumerated different alphabets

**W1 enumerated 468 X rows; W2 enumerated 679.** They are not two readings of one list; they are two
different granularities. The SCOPE's X clause names *"every status/form/identity/version/definition,
field, relation, cardinality, inverse, rule, attribute, extension-owner mapping, invariant binding, and
construct-local OPEN item."* **W2's enumeration matches that clause literally; W1's does not** — it
rolls relation sub-keys (`cardinality`/`inverse`/`rule`/`attributes`) into one row per relation, rolls
per-invariant bindings into one row per construct, and omits construct `definition` rows and registry
seed-field rows entirely.

Mapping W1's rows onto the canonical spine by roll-up, **W1 covers 474 of the 679 canonical rows;
205 canonical X items have no W1 disposition.** I have reconciled those 205 from W2 alone and marked
every one `w1-not-enumerated` in the ledger. **Absence is not filled.** This is a coverage matter for
the auditor, not a model finding — and I record it as W1's enumeration being coarser, not wrong.

### 3.5 Two internal-consistency defects in the coverage CSVs

- **W1: 40 of its 79 `construct-pressure`/`blocked-by-OPEN` rows carry `cause_classification:
  not-applicable`.** The amendment's coverage clause 9 requires a cause on every failure/pressure row.
  Nearly all 40 are construct-local OPEN items W1 labelled as pressure. **I supplied a cause rather
  than drop the rows**: `unresolved`, with an explicit note in `w4_adjudication`, because the evidence
  does not discriminate `model-defect` from `historical-evidence-gap` for an OPEN item a case merely
  did not settle. Per the amendment, `unresolved` counts as **neither conforming nor rejecting
  evidence**. W2 has zero such rows.
- **Both CSVs carry rows with a cause but `disposition: exercised`** — W1 27, W2 19. W2's
  `M02.sanity.S4` is the clearest: `disposition: exercised` on a row whose own
  `cause_classification` is `model-defect` and whose witness text reads *"CONFIRMED AND IT BITES."*
  The label diverged from the evidence; I ruled on the evidence (§4.2).

---

## 4. Cross-case reconciliation — 679 X rows

### 4.1 The reconciled row set

| Reconciled disposition | Rows | (round 0, superseded) |
|---|---:|---:|
| `exercised` | **522** | 552 |
| `construct-pressure` | **123** | 114 |
| `not-applicable` | **31** | 10 |
| `blocked-by-OPEN` | **3** | 3 |

**Restated after rework round 1 (§13).** The round-0 column is retained rather than overwritten. The
movement decomposes cleanly into two independent causes, measured separately in §13.2: W2's RW-1/RW-2
correction of its own coverage table, and my RW-3 witness guard.

**Reconciliation rule, stated so it can be audited:** pressure evidenced in *either* case stands for
the run and is never averaged away; `exercised` in one case and `not-applicable` in the other resolves
to `exercised` (the run has a witness); absence is never filled; no OPEN is normalised into a default.

**Reconciled cause tally (row-weighted; multi-cause rows retain every cause):**

| Cause | Rows | (round 0, superseded) |
|---|---:|---:|
| `historical-evidence-gap` | **85** | 81 |
| `model-defect` | **74** | 73 |
| `unresolved` | **33** | 33 |
| `project-evolution-candidate` | **31** | 31 |
| `enforcement-gap` | **33** | 30 |

**183** rows carry at least one cause. **Zero pressure rows without a cause. Zero silent blanks.**

`project-evolution-candidate` appears on 31 of 176 caused rows and **never as a residual bucket**:
every one of the twelve distinct candidates co-classifies with `model-defect`, `enforcement-gap`,
`historical-evidence-gap` or `unresolved`.

### 4.2 Divergence — 156 rows where W1 and W2 disagree

| Class | Rows | Adjudication |
|---|---:|---|
| both agree | 324 | — |
| `w1-not-enumerated` | 205 | §3.4 — reconciled from W2 alone |
| **divergent** | **150** | below |

*(Round 0 read 318 / 205 / 156. The six-row shift is entirely W2's RW-1 correction of its own
dispositions; my guard changes no `w1_disposition` or `w2_disposition` cell, only the reconciled
column — §13.2.)*

Of the 150, **123 are case-difference, not contradiction** — one history supplies a witness and the
other does not, or one strains where the other does not. Those two facts coexist and I recorded both:
the `exercised` side is a witness that the construct can carry *at least one* history; the
`construct-pressure` side is evidence it does not carry *every* history. Averaging them would destroy
the only comparative signal a two-case run produces.

**27 are model-intrinsic — a property of M01, which no case difference can explain.** Those I
adjudicated on the workstreams' own evidence text plus W3's execution. Seven required an override:

| X item | W1 | W2 | W4 ruling and why |
|---|---|---|---|
| `M02.sanity.S2` | pressure | exercised | **pressure.** W3 confirmed the dotted inverse still needs a resolver special case and `notation` still does not document the qualified form. W2's own witness text says so. |
| `M02.sanity.S3` | pressure | exercised | **pressure.** W3 confirmed *and extended* it (six undocumented keys, and `Event.identity` is a map where `notation` describes a scalar). W2's text: *"the reader is relying on inference."* |
| `M02.sanity.S4` | pressure | exercised | **pressure.** W2's row is internally inconsistent — `exercised` with cause `model-defect`. W3 supplies the executed proof: I17's chain clause mechanises (`F-E28` rejected) and its attenuation clause does not (`F-E26`/`F-E27` accepted). Non-atomicity is not cosmetic; it hides that half a rule is unenforceable. |
| `M02.sanity.S6` | pressure | exercised | **pressure.** `extension_owner` sits on six constructs; **five do not cite I19.** Both workstreams state the fact; only the labels differed. |
| `open.workflow_promotion` | still-open | **resolved-by-instance** | **still-open.** Two owner-operated histories inside one organisation cannot settle a cross-program promotion question. Review concern 12 binds the verdict to that limit, and W2's own §12 concedes it. |
| `core.Unit.open[0]` interruption and resume | still-open | **resolved-at-document-altitude** | **still-open.** This OPEN is the seat of W1's `PR-ATTEMPT-DISPOSITION`: an Attempt terminated with no actor-recorded disposition has no admissible enum value, and W1's own CF-03 explicitly does **not** repair it. |
| `open.delegation_attenuation` | pressure | exercised | **still-open and adverse.** `F-E26` and `F-E27` are both `accepted-defect`; the executed W1 checker reports 24 undecidable derived Delegations. |

### 4.3 The single strongest model-defect: the grade vocabulary — verified at source

W2's F-01 is the one finding I most wanted to check independently, because it is the only row in the
run that could plausibly have reached `reject`. It holds:

- `M01` lines 476–479: `values.evidence_grade` — `status: RESOLVED`, `values: [missing, claimed,
  partial, proven]`. **No registry. No `extension_owner`. No admission rule.**
- The observed program's vocabulary is `{proven, partial, missing, asserted}` — I read it at source in
  `SCOPE-RISK-ASSESSMENT.md` SR-10 at `37c7b09a`, quoting `uni-capability/SKILL.md`.
- It is not an accident. Issue #928 comment `4898695344` records SLN1 (#5528) as
  **`curve/nfr, asserted`**, and the OQ-1 ruling names `claimed` a slip.
- Consequence in the instance: `CP-02.grade` = `UNREPRESENTABLE`. A required field of a core entity has
  no conforming value for a real case value.

**This is a model defect and not a project problem**, and the discrimination is exactly what concern 18
asks for. `principles.program_ownership` says *"Programs own … proof bars"* — and the grade vocabulary
**is** the proof bar's vocabulary — while `principles.extend_by_registration` routes variation through
a registry. `evidence_grade` offers neither. Both cases identified the obvious project fix (rename
`asserted` → `claimed`) as **circular** and rejected it. I agree, and I add the sharper reason: the
rename would **erase an evidenced ruling**, which the amendment forbids independently of circularity.

**Bar test.** Does this need an eighth core entity? No. Does a core entity collapse independently
behaving concepts? No. It is a closed value vocabulary lacking an extension point — a changed-semantics
change within a viable seven-entity boundary. **`revise`, not `reject`.**

### 4.4 What the model does well — recorded because a run that only reports defects is not adjudicating

- **All 19 declared inverse pairs are enforceable and were individually falsified** (`F-B01`–`F-B19`
  all rejected) and demonstrated in both directions (34 rows). The post-A3 inverse discipline costs
  nothing in checkability, and W1's instance required 24 inverse edges to be closed mechanically before
  it validated — they are constraints, not decoration.
- **The `assessment` / `gate_outcome` split (M02 R2) pays off in both cases and in the suite.** W1's
  `RC-COV-R2` carries two assessments and two outcomes over two different baselines. W2's Gate-3a
  iteration-0 assessment exists with **no surviving outcome payload** — under v4's merged form it could
  not have been written at all. And `F-F02` shows the split's `rule` is **the only working Event-layer
  value check in the entire model** — the exact fix pattern the rest of the Event layer lacks.
- **`I18`'s first clause is checkable and enforced** (`F-E29`/`F-E30`/`F-E31` all rejected), and only
  because `definition_custodian_ref` is `ref<Actor>` and `Attempt.actors` is `ref<Actor>`. It is the
  model's clearest demonstration that **a typed reference buys a check and a text field buys nothing.**
- **The `Envelope` exclusion is vindicated against a project that literally uses the word.** The
  theme's `coordinator:` block decomposes onto `Delegation` field-for-field with no residue.
- **V5 makes a false claim visible.** W2's F-02: `gate-3c-report.md` does not exist at `37c7b09a`, and
  **vnc-045 is the only one of 226 feature directories carrying 3a and 3b but not 3c** — I reproduced
  the count (154 / 157 / 153) myself. Under V5 the `assessment` Event is simply **not writable**, so
  "Gate 3c PASS" cannot pass as fact. That is `I8` doing work.
- **V5 refuses to let authored summaries pass as measurements**, in both cases, and the software case
  supplies the proof: the report says the tool guard moved "12 → 15", the PR body calls `context_tag`
  "the 13th tool", and the committed diff says **14 → 15**. I re-ran that diff. Three authored numbers,
  one observable fact, both authored records wrong, and nothing to check against.

---

## 5. OPEN items — all 50 dispositioned

**11 top-level `open:` items + 39 construct-local OPEN items = 50.**

| Disposition | Count |
|---|---:|
| `still-open` | **45** |
| `not-exercised` | **3** |
| `blocking-hole` | **2** |
| `resolved-by-instance` | **0** |

**Zero OPEN items are resolved by these instances.** Both `resolved-by-instance` claims in the run were
asserted by one workstream and contradicted by the other, and I ruled against both (§4.2). This is the
honest reading of a two-case directional run and it matches concern 9 exactly: the OPEN items were
exercised — often adversely — and **not one was normalised into a convenient default**.

**`blocking-hole` (2):** `open.custody_enforcement` and `supporting.Gate.open[2]: external
enforcement`. Both are the same fact from two directions: **no common enforcement point exists**, and
the model says so itself. Reported as absence, per the standing rule.

**`not-exercised` (3):** `core.Capability.open[0]` recursive evidence rollup,
`core.Capability.open[1]` parent-child `done_when`, and `open.capability_rollup`. All three are
downstream of the Capability gap (§1.3). `wfh-010` left `capability_rollup` unexecuted and **this run
leaves it unexecuted too.**

Three further OPENs deserve naming because a workstream nearly closed one and should not have:
`open.autonomy_A3_A4` stays `insufficient-evidence` — W1 records A4 *used* by `DL-COORD-STANDING`
despite that status, and A3 with no witness in either case. One instance of a tier is not evidence
about a tier boundary. `open.semantic_compression` stays open by construction: two owner-operated
histories cannot settle a generality claim in either direction, and both workstreams say so.
`open.lesson_vs_pattern` stays open on one weak data point (W1: `#320`, the case's most reusable method
rule, filed as a `finding` rather than a `lesson-learned`, with no distinct admission or retrieval
behaviour) — weak because nobody tried the alternative.

---

## 6. Expressing pressure through an existing registered extension

- **Absorbed by a conforming registered extension — `extend_by_registration` working.** Both cases
  populated the three empty registries (`record_category`, `unit_kind`, `effect_class`) with
  program-owned entries and added event types, and **neither case needed a new common construct**. The
  instructive case is W1's: an *unauthorized* change to a governing definition does not fit
  `adaptation`, whose parsed definition and required `decision_ref` both presuppose authorization — so
  it entered as a registered `unrecorded_change` type rather than by stretching `adaptation` or adding
  a noun. That is the mechanism doing exactly its job.
- **NOT absorbable — the residue that drives the verdict.** `values.evidence_grade` (§4.3);
  `EffectBoundary.can_refuse`, `Event.occurred_at` and `Capability.grade`, which have **no
  `unestablished` member** even though `values.currentness` and `values.effect_disposition` both carry
  `unknown`; `Gate.procedure`'s `enum[deterministic,judgment]` with no mixed value;
  `Attempt.disposition`'s enum with no interruption value; `Unit`'s lack of any name or external
  reference. **None of these is a registry point, so no conforming extension reaches them.**
- **Absorbed but adversely — the registry as a door.** `F-H09`, `F-E08` and `F-H08` show the
  `excluded:` list is **re-openable through the registries** by exactly the program the exclusion
  binds. The exclusions that hold are those carried by type or closure; those carried by prose against
  a registry do not. That is a pressure the extension mechanism *creates*, not one it absorbs.

---

## 7. Challenging every project-evolution candidate

Twelve distinct candidates (W1 CF-01…CF-07, W2 CF-01…CF-05 — the identifiers collide, so I namespace
them). Each was challenged on circularity (13), independent reasonableness, semantic / proof /
authority / custody preservation and behaviour erasure (14), authority laundering (15),
counterfactual-versus-history separation (16), migration-cost completeness and realism (17), and dual
representability.

**Result: 9 survive cleanly · 2 survive with a recorded defect · 1 fails.**

| id | Change | Outcome |
|---|---|---|
| **W1/CF-01** | tree-oid baselines + no rebase after a gate has ruled | **survives, recorded defect (17).** The 2026-08-29 correction **narrowed** `affected_artifacts`, dropping the two errata surfaces — while my own measurement (§3.2a) **strengthened** the residual: the branch is already deleted on `origin`, so a fresh clone resolves nothing. Migration cost is now under-stated relative to its own rationale. **The leader deliberately declined to rule on this candidate and referred it to me; this is my ruling, not its.** |
| **W1/CF-02** | sha256 manifest over the method surface + drift check | **survives.** Grounded in an evidenced incident (an `npx` install silently overwrote twelve method files, caught by a human reading). States its own limit honestly: a manifest **detects** drift and does not establish custody, because the manifest lives inside the governed repository and `#320` applies to it. **I18 stays unsatisfied in both forms.** |
| **W1/CF-03** | typed interruption record on session death | **survives — and does not repair the model.** W1 declares `current_form_representable: false` and that the defect **survives the evolution**. Correct handling under the amendment, and the clearest case in the run of a project change that must not be allowed to hide a model defect. |
| **W1/CF-04** | audits retain the raw output they rule on | **survives.** Grounded in the phantom-38th-manifest incident that consumed part of a rework allowance. Explicitly refuses the laundering: raises altitude to `reported-observation`, **not** `mechanical-observation`, because capture custody stays inside the reporting actor. |
| **W1/CF-05** | declare the coverage-auditor duty as a Role | **survives.** Independent reason is measured: the same blocking gate was assessed under two different role identities in consecutive runs (`wfh-010` a `factory-validator`, `wfh-008` a `factory-researcher`). |
| **W1/CF-06** | rename agent frontmatter `capabilities:` → `skills:` | **survives, recorded defect.** Passes circularity — the Unimatrix `capability` category collision predates V5. **Fails the evidence bar on independent reasonableness:** the asserted harm is not evidenced inside the fixed alphabet, and W1's own `unresolved_discriminator` concedes *"whether the collision has ever caused a concrete error is not evidenced by this case."* |
| **W1/CF-07** | expose a content digest on knowledge-node reads | **FAILS concern 17 (migration realism).** W1 states plainly that the change targets a service outside this repository and *"this scope cannot cost it."* Cost, compatibility and coexistence are therefore **not explicit** — honestly incomplete rather than hidden, but incomplete. **The underlying `model-defect` is untouched by this failure** and stands on its own: `Record.content_digest` is a required `digest` with no `unestablished` member, and eleven service-backed Records in W1's instance carry sentinels the checker reports. |
| **W2/CF-01** | stamp reports with the SCOPE digest; stamp `superseded_by` on regeneration | **survives.** The project already pays this by hand — the alignment report records that pattern #5607 cites a now-stale instance and hands the retro a manual reconciliation. |
| **W2/CF-02** | `reviewed_commit: <sha>` in the gate-report template | **survives.** T01 already declares *"Gates check committed HEAD"*; the evidenced harm is a gate-3b open WARN already fixed 24 minutes before the report was committed. |
| **W2/CF-03** | record the scope decision on the tracking issue at the moment it is made | **survives, and moves authority the safe way** — narration moves *away* from the actors it governed. The independent reason is the project's own thesis: it audits a single tag mutation to the millisecond and left its most consequential decision with no primary record at all. |
| **W2/CF-04** | retain runner output beside the risk-coverage report | **survives — best-evidenced candidate in the run.** The project already treats a summary standing in for a record as a security defect for machine writes (R-03's `"{}"` sentinel rule). The harm is demonstrated, and **I reproduced it**: the committed diff says 14 → 15 while two authored records say otherwise. |
| **W2/CF-05** | Gate 3c report as a forge-side required check | **survives — the best-constructed candidate.** Independent reason is measured (I reproduced 153/226 and the uniqueness of vnc-045). Concern 15 analysed explicitly and passed: enforcement moves onto the externally custodied boundary, **away** from every governed actor. Concern 17 met including the exemption path. And critically it **refuses to let post-evolution fit conceal the current verdict** — `current-project fit for GT-06 stays reject`. It also records its own residual honestly: a required check whose predicate is *"a file exists"* is satisfiable by writing a file. |

**Five further candidates were considered and correctly NOT proposed**, and I endorse all five
refusals: per-agent `agent_id` (relitigates ratified D6 from outside its evidence — carried
`unresolved`); instantiating a Capability for `jurati-arch-002` (**the circular candidate**);
enforcing the single-writer curator rule (the build recommendation this scope forbids); renaming
`asserted` → `claimed` (**circular, and would erase an evidenced ruling**); credentialed per-agent
identity (relitigates a human-LOCKED ADR-008 posture whose declarative-attribution bound is an accepted
residual risk).

**Concern 13 — circular force-fitting: NONE FOUND.** No surviving candidate's independent reason
mentions V5, and both workstreams independently identified and rejected their own circular candidate.
The two changes V5 would most "prefer" are **the two that were rejected**.
**Concern 16 — counterfactual confusion: NONE FOUND.** Both counterfactual files carry distinct
identifiers, explicit `counterfactual` provenance and `replaces:`/`varies:` source links; W1's checker
*mechanically* errors if a counterfactual object appears in the historical file, and refuses to close
inverse edges across the boundary. No counterfactual object is counted in any coverage number in this
ledger.

---

## 8. Verdicts

### 8.1 The seven-entity hypothesis

> **`retain | revise | reject` → REVISE**
>
> **`current-project fit: revise`** · **`post-bounded-evolution fit: revise`**

Applied against the SCOPE's bar, literally, and to the projects **as they actually existed** first:

| Bar clause | Result |
|---|---|
| Both cases instantiate **without a domain-specific common construct** | **MET.** W1: 191 objects, 14 constructs, zero new common constructs, four program-owned registry extensions. W2: same, five extensions. |
| **Every material semantic** fits typed structure or a conforming registered extension | **NOT MET.** `values.evidence_grade` closes on a term the program explicitly rejected, with no registry and no owner (§4.3). Plus: no `unestablished` for three required typed fields; `Gate.procedure` admits no mixed value; `Attempt.disposition` admits no interruption; `Unit` has no name or external reference. |
| No authority / custody / evidence / effect / interruption / proof distinction **weakens** | **MET in the model, UNWITNESSED in the cases.** No distinction weakens; several are unenforceable (§3.1). Per the standing rule, **missing enforcement is reported as missing enforcement**, not converted into model failure. |
| **Reject** limb 1 — a material case behaviour needs an **eighth common core entity** | **NOT MET.** No such row exists in 679 reconciled X rows or 115 executed fixtures. |
| **Reject** limb 2 — a core entity **collapses independently behaving concepts** | **NOT MET.** The nearest candidates — `Actor` (declared vs attested vs composite identity) and `Event` (nine behaviourally distinct types over one untyped `extension`) — resolve to field and binding changes *within* the construct. Both workstreams' own analyses point at a field, not an entity, and W3 verified all seven event-shaped excluded constructs are exercised as event types. |

Retain fails on clause 2; reject fails on both limbs. **`revise`.**

**Why the two fit verdicts are identical, and why that is the result rather than a hedge.** The
original bar applies first to the projects as they existed: `revise`. Bounded evolution then produces
**the same** verdict, because **not one of the ten surviving candidates touches a model defect.** They
improve *evidence* (CF-04 raises evidence altitude; W2/CF-05 supplies the run's only proposed
enforcement point; CF-01/02/03 improve reproducibility and recovery) and repair *no* construct. The two
candidates that would have touched a model defect were rejected as circular by the workstreams
themselves. So there is no better post-evolution result, and therefore nothing concealing the current
one.

### 8.2 Supporting definitions (8)

| Definition | Verdict | Determining evidence |
|---|---|---|
| **Workflow** | **revise** | `versioned: true` with **no typed version carrier** (N1), which `Attempt.governed_by`'s *"pins immutable versions"* and the assessment extension's `gate_version_ref` both require. `supersedes` admits cycles. The `Goal → applicable Workflows` traversal is a **query-layer hole**: the declared-relation path is **both incomplete and unsound** (executed on the baseline), and the index route is a full extent scan the model does not bound. |
| **Skill** | **revise** | I10 holds **by absence** — a genuine strength: `F-E14`'s `Skill.proves → Capability` is structurally unrepresentable. But `Skill.required_by` names `Unit` as a target and `Unit` carries **no corresponding relation at all**, and it is the only `required_by` in the file with no inverse where two siblings declare one (S7). The unpopulated `held_by` attributes across 22 pairs are `historical-evidence-gap`, not defect. |
| **Role** | **retain** | Pressure 3/25 with **zero `model-defect`** — causes are enforcement and evidence gaps only. `Role.receives` (added per R5) is load-bearing and makes traversal T-05's standing arm work at all. The only pressure is an undefined Role in the repository — a project gap, correctly classified. |
| **Delegation** | **revise** | Highest supporting-layer pressure (13/40, `model-defect` 7), and it lands on the theme's load-bearing boundary. **I17 attenuation is undefined on two of three axes** (`F-E26`: A5 from A1 accepted; `F-E27`: `external_cost` 500 from a parent granting 0). `unit` `0..1` forced three organisational directives into six objects — checker-caught, not judgment. `grantor == grantee` is neither forbidden nor detected. S5's standing/dynamic discriminator is ambiguous and **not falsifiable**. |
| **Gate** | **revise** | `procedure: enum[deterministic,judgment]` admits **no mixed value**, and W1's coverage gate was demonstrably both — the only `blocked-by-OPEN` field row in the run. `gate_version_ref` names a version **no field can resolve**. `independence_predicate` is free text and `eligible_evidence` a **bare untyped list**, so `F-E09` (a `pass` over `independence_check: false`) and `F-E11` are accepted. |
| **EffectBoundary** | **revise** | Three of the eighteen accepted defects land here. `can_refuse` is `required: true` `bool` with **no `unknown`** while the sibling `effect_disposition` vocabulary has one — and **no rule in M01 reads it** (`F-E19`). The construct has **no relation to any Actor**, so a claim that the governed agent holds its credentials cannot be contradicted (`F-G02`) — on the construct whose entire purpose is custody. `enforces` is empty in both cases; that is reported as absence. |
| **Attempt** | **revise** | `disposition` is `required: true` with no admissible value for an execution terminated with no actor-recorded disposition — W1's instance writes `hold` and marks it `_approx`, and **CF-03 does not repair it**. This is precisely M02's R2 argument (an abandoned assessment must leave a trace) applied to the one construct where V5 did not apply it. Balanced against a real strength: `resume_requirements`' four clauses are separately supplied in both cases. |
| **Technology** | **retain** | Pressure 3/17, **zero `model-defect`**, one `historical-evidence-gap`. I11 and `enables`' *"no grade transfer"* held in both cases — and in the software case it was the project's own pre-registered ruling (*"do NOT mark any capability `proven` off vnc-045"*), stated twice in advance by an independent reviewer and honoured at delivery. |

### 8.3 Registries (6)

| Registry | Verdict | Determining evidence |
|---|---|---|
| **scope_type** | **retain** | Zero pressure across 23 X rows. Four seeds exercised in both cases; the `admission_rule` correctly records the RW1-D2 supersession. Its seeds' `required_fields`/`constraints` are empty, so a seed-level invalid fixture is not constructible — a checkability limit, not a defect at directional altitude. |
| **capability_classification** | **retain** | Zero pressure. Unexercised in the research case only because it has no Capability (`historical-evidence-gap`, 16 rows). **All four seeds exercised in the software case** — `functional`/`threshold` on CP-01, `nonfunctional`/`curve` on CP-02. |
| **event_type** | **revise** | Two independent defects. (a) **The registry's own `gate_outcome` seed carries a `rule:` key outside its declared shape**, so shape closure cannot be asserted without rejecting M01's own seed — and that key is exactly what makes the model's only working Event-value check possible. (b) The `excluded:` boundary is **re-openable through this registry**: `F-H09` registers `lesson` and is accepted silently; `F-E08` registers `effect_completed`, reintroducing the merged effect event. The `admission_rule` says *"never another core noun"* and nothing binds it. |
| **record_category** | **retain** | Empty seed by design; both cases populated it conformantly with behaviourally-justified entries (W1 nine categories differing on all five of I3's dimensions; W2 two earning existence on distinct lifecycle and epistemic behaviour). No extension weakens an invariant. The mechanism worked. |
| **unit_kind** | **revise** | Same exclusion-door defect, landing on a named exclusion: `F-H08` registers a `unit_kind` named `attempt`, **reintroducing Attempt as a Unit subtype**, and the result is `specified-not-enforced`. The `admission_rule` does not bind the exclusion. |
| **effect_class** | **revise** | The authority join is missing at exactly this registry. `Delegation.effect_grants` and the `effect_request` extension's `requested_effect` are **both typed against this registry and no rule binds them** (`F-E17`), nor does anything compare a request against the target boundary's `effect_classes` (`F-E18`). This is the one authority check that could have been fully mechanical from typed data on both sides. |

### 8.4 Catalogs (3)

All three share one defect: **`catalogs.*.scope` has no defined binding to any construct field**, and
`scope` is itself undocumented in `notation` (S3, extended). Under the SCOPE's adverse-evidence clause
— *a model rule that cannot identify its subject is adverse evidence* — none of the three can identify
its members.

| Catalog | Verdict | Determining evidence |
|---|---|---|
| **skill** | **revise** | Most severe. `Skill` carries **no scope field and no catalog field**, so the catalog has **no instance-level attachment point at all** (`F-D01`, not constructible). W1 authored a 16-member catalog as an instance-level convention the model does not support. `open.skill_catalog` still-open. |
| **workflow** | **revise** | Least severe: `Workflow.owner_scope_ref` is a candidate binding and both cases used it, but **M01 nowhere says the catalog's `scope` and `owner_scope_ref` are the same thing** (`F-D02`). Declared-but-unbound rather than unattachable. |
| **gate** | **revise** | `Gate` carries no scope or catalog field; `bound_by → Workflow` covers one of the three declared scopes. **A record-category-scoped Gate — one of the three the catalog declares — has no representation at all** (`F-D03`). `open.gate_identity` is downstream of this and stays open. |

### 8.5 Supplementary — not among the 17 required, but material

**`values` block: revise.** `evidence_grade` closes on a term the program rejected with no extension
point (§4.3); `autonomy_tier` has **no declared order** on a scale whose top value is `held_by: human`;
**`coupling` is referenced by no field in the entire model**; `effect_disposition`'s explicit rule has
no typed carrier. The value layer is where the most consequential unenforceability sits, and it is not
one of the seven entities — which is itself part of why the hypothesis survives as `revise`.

**Per-core-entity, for the auditor's convenience** (the hypothesis verdict above is the required one):
`Scope` revise (`authority_root_ref` forces one of two wrong answers on every nested Scope) ·
`Goal` retain · `Capability` revise (no altitude field; `evidence_record_refs` not conditional on
`grade`; no fully conforming witness in either case) · `Actor` revise (`declared_identity` does not
individuate — fifteen W1 Actors share one string; composite actors have nowhere to go) ·
`Unit` revise (no name, no external reference; `baseline_ref` is `text` with no integrity binding) ·
`Event` revise (the whole of §3.1 concentrates here) · `Record` revise (`content_digest` required with
no `unestablished`; five `extension_owner` keys name no field on the construct).

---

## 9. W3's suite against the evolved forms

The amendment **permits** W3 to challenge evolved forms once W1/W2 make them explicit but does not
require it. **W3 did not**, and its own §9 explains why: W1's instance was absent for W3's entire run
and W2's appeared only at the finish, inspected for encoding shape alone. Recorded, not held against
it — W3 derived its baseline from M01 precisely to avoid contaminating my independence, which was the
right call and is why the divergence analysis in §4.2 means anything.

**What this leaves untested, stated as an absence:** no evolved form in either counterfactual file has
been run against a rejection suite. In particular W2/CF-05's own recorded residual — *a required check
whose predicate is "a file exists" is satisfiable by writing a file* — is exactly the shape W3's suite
is built to falsify, and it was not falsified. That is a gap in the run's coverage, not a defect in W3.

**One cross-workstream cost W3 identified and I confirm:** W2's encoding (`scopes:`/`goals:`/…) and
W3's (`instances:`/`registered:`) are **different serializations of the same model**, because M01's
`notation` describes the model file and never describes an instance document. I had to reconcile across
two encodings and a third (W1's). **That reconciliation cost is a finding about the model, not about
any workstream** — and it is why §3.4's enumeration divergence happened at all.

### 9.1 A run-level observation, deliberately kept OUT of the ledger

W1's §5.3a records a method note the leader asked me to weigh: three instances in this run of one
shape — *a claim outrunning its measurement, with a mutable local artifact as the source* — and it
names the mechanism (`git branch -a --contains` reads local refs and is not evidence about `origin`;
`git ls-remote` is). W1 connects it to `#320`'s custody predicate: *a control whose input sits inside
the governed party is a label, not a control.*

**My ruling: it is on-subject and it does not belong in this ledger.** It is a first-party observation
about **this run's own instruments**, not about `wfh-008` or `vnc-045`. The X ledger dispositions the
model alphabet against two case histories; admitting a run-level observation would risk it being read
as observed coverage of a case, which the amendment forbids. **No ledger row was created for it.**

Recorded here instead, with its weight stated: three occurrences in one run — the leader's first
characterisation, W1's first correction, and the leader's second message — each corrected only after
re-execution. That is a stronger data point about the predicate than either case history supplies,
because it was observed rather than reconstructed. It belongs to the retro, not to this verdict, and it
changes nothing above.

---

## 10. Limits — what I could not establish

- **This is two owner-operated histories in one organisation, read-only, directional.** It proves
  nothing about generality, runtime enforcement, organisational effectiveness, portability, a product
  boundary, or semantic compression outside these two cases. `open.semantic_compression` stays open.
- **No enforcement claim anywhere.** Every mechanical result is a property of a checker written from a
  YAML file this week. No historical project refused anything on V5's account.
- **I did not re-execute the leader's `gh api` measurements** (§3.2a) — outside my zero-cost envelope,
  and they cannot change a ruling. Recorded as leader-reported, not adopted.
- **I did not re-derive either case's instance.** I re-executed the checkers and went to source for the
  load-bearing measurements (the rebase and ancestry, the Gate-3c absence and the 226-directory
  distribution, the tool-count diff, the grade vocabulary, the merge parentage, the `.claude/` count in
  the PR). I did **not** re-encode ~400 objects; where a row's value rests on a workstream's encoding
  judgment, my adjudication rests on it too.
- **W2's T01/T02 are living, unversioned protocol files** read at `37c7b09a`, not at the vnc-045
  delivery date. If the protocol changed in between, W2's `Workflow` and `Gate` instances are
  anachronistic and nothing in the alphabet dates the revisions. **W2 flagged this as its single
  largest soft spot and asked W4 to weigh it: I weigh it as unresolved and material** — every
  `Workflow`, `Gate`, `Role` and `Delegation` verdict in the software case inherits it. It does not
  change any verdict above, because each is carried by at least one research-case or W3 witness as
  well, but it caps the software case's independent weight.
- **Every `vnc-045` Delegation is an inference** and `resource_ceiling` has no source at all. Treat the
  whole `delegations:` block as reconstruction.
- **`unresolved` stays unresolved.** 33 rows carry it and none is counted as conforming or rejecting
  evidence.
- **Absence was never filled.** No missing event, evidence, timestamp or grade was invented anywhere in
  this adjudication.

---

## 11. Reconciled transitive-source ledger

| Ledgered by | Id | Source | Reason | Provenance |
|---|---|---|---|---|
| W1 | `T01` | `.claude/workflow/research-scope.md`, `.claude/agents/factory/*.md`, `.claude/rules/unimatrix-access.md`, absence of `CODEOWNERS` | V5 requires `Workflow.method_statement`/`unit_kinds`/`dependency_rules`/`state_vocabulary`/`definition_custodian_ref` plus `Role.responsibility` and `Skill.work_class`; the R alphabet holds instances of the method, not its definition | tracked files at `main`, read-only, digests recorded in the instance |
| W1 | `T02` | read-only Unimatrix reads of `#312`, `#316`–`#321` | the case's knowledge-node Records and the I1 supersession comparison turn on whether ids are current and the chain preserved; R05 asserts it, only a read establishes it | `context_graph`, `agent_id: factory-researcher`, four calls, **no write** |
| W1 | `T03` | read-only forge/remote queries about **current** repository state | correction 2 turns on whether a branch is published *now*; no pinned dump covers current remote state | read-only, zero-cost, non-mutating; bounded at `2026-08-29T02:57:42Z` |
| W2 | `T01` | `dug-21/unimatrix@37c7b09a:.claude/protocols/uni/uni-delivery-protocol.md` (`0975e4aa…`) | the governing Workflow definition for Stages/Gates 3a–3c; without it `Workflow` and `Gate` collapse to `missing-history` | pinned commit, read-only |
| W2 | `T02` | `…:.claude/protocols/uni/uni-design-protocol.md` (`5758bfa3…`) | Session 1's two human approval points and the prescribed *"Handling human-requested changes"* path that executed the scope reduction | pinned commit, read-only |
| W2 | `T03` | `git ls-tree -r 37c7b09a product/features/**` (derived measurement) | establishes that `gate-3c-report.md` is the repository norm, so vnc-045's absence is an **observation**, not an inference | mechanical over the pinned commit; **re-executed by W4** |
| W3 | `T-01`…`T-04` | the four lineage proposal files (`-v3`, `codex-…-v4`, `agentic-organization-data-model.md`, `organizational-data-model.yaml`) | S8 is a claim about files outside M01–M06 and cannot be checked without them | tracked at `6718049`; digests match the SCOPE extension; **grep/existence only, no content adopted** |
| W3 | `T-05` | `product/factory/proposals/target-concept-v1.md` | named in `M01.meta.derivation` | **existence and digest only; content not read** |
| W3 | `T-06` | `artifacts/vnc-045-instance.yaml` (in-flight W2 output) | top-level encoding shape only | **no W2 conclusion adopted** |
| **W4** | `T-W4-01` | read-only remote-state queries: `git ls-remote --heads origin`, `git fetch --prune --dry-run origin`, `git branch --contains`, `git for-each-ref` | **Reason:** two agents handed me contradictory characterisations of where the pre-rebase objects live; my brief forbids reasoning from a claim I did not execute, and a claim about `origin` cannot be checked from a local mirror of it. | read-only, zero-cost, non-mutating, against our own repository — the same class as W1's `T03`. **Result in §3.2a; I did not make the `gh api` calls.** |

**No other source was consulted.** The lineage files carry no coverage obligation. The pinned corpus at
`/tmp/claude-1000/-workspaces-arch-research/wfh-011-sources/` is transport for `S01`–`S06` and `R05`,
not a new source. Prior art `#270`, `#278`, `#269`, `#271`, `#275`, `#279` is reuse-only and none of it
was needed here.

---

## 12. Answers to the adversarial concern set (13–18)

**13 — Circular conformance.** None found. Both workstreams identified and rejected their own circular
candidate before I got to them, and no surviving candidate's independent reason mentions V5.

**14 — Behaviour erasure.** None found. All ten surviving candidates are additive. W1/CF-03 is the test
case and it passes explicitly: it preserves the distinction that the record is authored by the
**resuming** actor and does not claim to be the interrupted actor's disposition, and it names the
discipline no schema enforces (refusing to backfill what is permanently missing).

**15 — Authority laundering.** None found, and two candidates move authority in the **safe** direction:
W2/CF-05 puts enforcement on an externally custodied boundary, away from every governed actor;
W2/CF-03 moves narration away from the actors it governed. W1/CF-02 explicitly **declines** to claim it
establishes custody.

**16 — Counterfactual confusion.** None found, and in W1's case the separation is **mechanically
enforced** — the checker errors if a counterfactual object appears in the historical file and refuses
to close inverse edges across the boundary. No counterfactual is counted in any coverage number here.

**17 — Migration realism.** **One failure (W1/CF-07) and one recorded defect (W1/CF-01)** — §7. The
other ten state cost, affected surfaces, compatibility and what they do **not** recover.

**18 — Cause discrimination.** Performed: 81 `historical-evidence-gap`, 73 `model-defect`,
33 `unresolved`, 31 `project-evolution-candidate`, 30 `enforcement-gap`, every multi-cause row
retaining every cause. The separation is load-bearing in the verdict: the **enforcement** absences
(zero enforced authority in both cases; `EffectBoundary.enforces` empty everywhere) are reported as
absence and did **not** move the verdict; the **evidence** gaps (Delegations wholly inferred, no raw
runner output, no scope-decision record) prevented positive claims and did **not** move the verdict;
the verdict moved only on **`model-defect`** rows — the grade vocabulary, the missing bindings, the
enum gaps.

---

## 13. Rework round 1 — RW-3 and RW-4

Ruling: `gate-coverage.md` (`b755bb5`), `REWORKABLE`. RW-1/RW-2 were W2's and landed at `0421142`; I
verified `vnc-045-instance.yaml` is byte-unchanged there (`git diff 0421142^..0421142 --` on that path
is empty) and that W2's new validator reproduces byte-identically. RW-3 and RW-4 are mine.

**The audit is right and the defect is mine.** My §4.1 rule reads *"`exercised` in one case and
`not-applicable` in the other resolves to `exercised` (the run has a witness)"*. The rule is sound; I
applied it to the **disposition** column and never tested the **value**. A reconciler that trusts a
label is the same instrument failure as a coverage table that never opens its instance — one layer up.
I did catch the inverse defect (§3.5) and disclosed the enabling limit (§10), and the auditor is
correct that disclosure is not discharge.

### 13.1 What I built

`artifacts/w4-witness.py` reads **both case instances natively** — W1's `instances:` form and W2's
section form — and measures, per canonical X path, how many objects actually populate it. A value is a
witness only if it is non-empty and not one of the encodings' absence placeholders (`missing-history`,
`unestablished`, `UNREPRESENTABLE`, `ABSENT`, `NOT-WRITABLE`, `none`). A **declared inverse** counts as
witnessed only where an edge actually **closes**. Output: `artifacts/w4-witness.json`, consumed by the
ledger build. Deterministic; the ledger rebuilds byte-identically.

It reproduces the auditor's six independently: all six measure **0 witnesses in both cases**.

**One deliberate refinement.** A value-vocabulary member appearing inside a declared `map` field
(`Event.extension`) is counted as **witnessed**. Absence of a *typed carrier* is a separate finding
(W3 `F-A15`/`F-A16`: `values.coupling` is referenced by no field in M01) and must not be laundered into
absence of a *witness*. Without this, three `value-member` rows would have been wrongly flipped.

### 13.2 Decomposition — two independent causes, measured separately

The leader's instruction was to repair the instrument and report whatever comes out, without steering
or protecting the result. Both W2's rework and my guard moved counts, so reporting them merged would
hide which did what:

| | `exercised` | `construct-pressure` | `not-applicable` | `blocked-by-OPEN` | agree / divergent |
|---|---:|---:|---:|---:|---|
| **A** round 0 (committed `3b7efbe`) | 552 | 114 | 10 | 3 | 318 / 156 |
| **B** = A + W2's RW-1/RW-2 only | 546 | 114 | 16 | 3 | **324 / 150** |
| **C** = B + my RW-3 guard — **final** | **522** | **123** | **31** | **3** | 324 / 150 |

**W2's rework alone** moved 6 rows off `exercised` and is the entire source of the divergence shift.
**My guard alone** moved 24 further rows off `exercised` and 3 more onto pressure. My guard changes no
`w1_disposition` or `w2_disposition` cell — only the reconciled column and the adjudication text.

### 13.3 What the guard caught — the auditor's six versus everything else

RW-3's text is general: *"refuses `reconciled_disposition: exercised` for any row with no populated
instance witness on either side."* I ran it over every row, not only the six.

**Scoping, disclosed.** The guard applies to the row classes where "a populated instance witness" is a
defined concept: fields, relations, relation sub-keys, value members, registry seeds — **274** rows
reconciled `exercised`. It does **not** apply to principles, notation, invariants, invariant bindings,
`extension_owner`, construct attributes, catalogs, excluded items, OPEN items, review concerns,
changelog or traversal rows, whose `exercised` asserts consumption during encoding or analysis, not an
instance witness. Those **269** rows are reported here and **not silently flipped**; the re-audit
should rule on the scoping, which is my interpretation and not the auditor's text.

**Annotate and refuse are separate operations**, because W2's RW-1 rework had independently moved three
of the auditor's six off `exercised` before my guard ran. RW-3 still requires their boilerplate be
replaced by the measured fact, so the guard **annotates every zero-witness row** and **refuses only
those still reading `exercised`**.

| | count |
|---|---:|
| zero-witness rows annotated with the measurement | **39** |
| — the auditor's six | **6** (all annotated) |
| — found by the guard beyond the six | **33** |
| rows whose disposition the guard **changed** | **27** |
| — of the auditor's six | **3** (the other 3 were already correct via W2's RW-1) |
| — beyond the six | **24** |

Changed to `construct-pressure` with a cause (the emptiness is itself an evidenced finding):
`core.Capability.relations.advances` · `core.Capability.relations.delivered_by` ·
`core.Event.relations.supersedes` · `core.Goal.fields.north_star` ·
`core.Actor.relations.has_skill.attributes` · `core.Actor.relations.holds_role.attributes` ·
`supporting.EffectBoundary.relations.enforces.cardinality` and `.inverse` ·
`supporting.Delegation.relations.enforced_by.inverse`.
The remaining 18 moved to `not-applicable` with the measured reason: they are `cardinality`, `inverse`
and `rule` sub-rows of relations with no occurrence in either history, so the sub-rule has nothing to
be exercised by.

`core.Event.relations.supersedes` carries its own sentence, as RW-3 requires: `F-E07` is
`accepted-defect` — `Event.supersedes`, `Record.supersedes` and `Workflow.supersedes` declare **no
acyclicity**, so a correction chain can close on itself and erase the history `I1` exists to protect,
while M01 declares `acyclic` three times elsewhere. Measured alongside it: the relation is populated on
**0 of 32** W1 Events and **0 of 30** W2 Events. An adverse W3 result on a relation neither case
exercises is the weakest possible standing for the rule and the strongest for the defect.

### 13.4 A finding the audit did not have — the same defect exists in W1's generator

`core.Goal.fields.north_star` was reconciled `exercised` on W1's witness text *"set on 2/2 instances"*.
Measured: the W1 instance carries `north_star: []` on **both** Goals, and W2 carries the placeholder
`missing-history`.

**W1's generator counts key presence, not value population** (`fname in r.get('fields')`). That is the
same label-over-value defect the audit found in W2's table, on the side the audit credited as sound —
W1's generator does read its instance, which is why it was not suspected. Its consequences are narrower
than W2's because most W1 fields are genuinely populated, but the property is identical. It also ties
to W1's own `PR-LIST-REQUIRED`: M01's `notation` never says whether `required` on a `list<>` type means
key-present or non-empty, so `[]` is a value no checker can rule on — which is exactly how it survived.

### 13.5 W2's flag on the 34 declared-inverse rows — measured, not adopted

W2 reports that its new validator finds **55 of 210** declared-inverse edges broken in `vnc-045`, and
that 34 inverse X rows stay `exercised` on an authored basis. I re-executed the validator (byte-identical)
and then measured closure per row across **both** instances:

| inverse closes in | rows | reconciled |
|---|---:|---|
| **both** cases | 18 | `exercised` — correct |
| **W1 only** (zero closing edges in `vnc-045`) | 6 | `exercised` — W1 supplies the witness |
| **W2 only** (W1 has no `Capability`) | 4 | `exercised` — W2 supplies the witness |
| **neither** | **6** | **caught by the guard** |

**The guard's own text answers W2's question: 6 of the 34, not 34.** The other 28 have a real witness in
at least one case, and reconciling them to `exercised` is the rule working, not the rule failing. W2's
characterisation is true of its **own case matrix** and not of the **reconciled** ledger — the
distinction the guard exists to draw. W2 was right to flag it and right not to re-disposition it.

**The asymmetry is recorded, not resolved:** on 6 declared inverses the research case closes every edge
and the software case closes none. That is one more instance of the run's standing limit — a
construct carried by one history and not the other — and it caps how much either case can say alone.

### 13.6 RW-4 — my own rulings carried into the ledger

`W1/unlabelled` and `not-challenged` are gone (0 occurrences each). `CF-05`, `CF-06` and `CF-07` now
appear on 12 rows.

| Ledger row | `evolution_candidate_id` | `evolution_challenge_result` |
|---|---|---|
| `supporting.Gate.relations.requires_assessor` | `W1/CF-05` | survives |
| `invariants.I10` | `W1/CF-06` | survives, recorded defect — independent reasonableness not evidenced inside the fixed alphabet |
| `notation.types` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |
| `core.Record.fields.content_digest` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |
| `M02.sanity.S3` | `W1/CF-07` | **FAILS concern 17 (migration realism)** |

A reader of the ledger alone now sees what §7 ruled, including the failure.

### 13.7 Verdict tension — checked, and none found

Per the ruling I did not move any §8 verdict, and I checked whether the corrected evidence bears on one:

- The single new `model-defect` row is `core.Event.relations.supersedes`. **`Event` was already
  `revise`.**
- The three new `enforcement-gap` rows are all `EffectBoundary`/`Delegation` enforcement sub-rows.
  **Both were already `revise`**, and this is the same zero-enforced-authority absence already carrying
  those verdicts. Reported as absence, not converted into model failure.
- The four new `historical-evidence-gap` rows touch `Goal`, `Actor` and `Capability`. `Actor` and
  `Capability` were already `revise`. **`Goal` was `retain` and stays `retain`:** its new row carries
  `historical-evidence-gap` only, no `model-defect`, and a historical-evidence-gap prevents a positive
  claim at that altitude without being a model defect — the same test on which `Role` and `Technology`
  were retained. Recorded because it is the one verdict the correction came closest to touching.
- No registry, catalog or supporting-definition verdict has a changed cause profile.

**Nothing here moves the seven-entity verdict or its clause mapping.** The `revise` ruling turned on
`values.evidence_grade` having no conforming home (§4.3) and on no case behaviour requiring an eighth
core entity — neither is touched by a witness guard. Had the corrected ledger produced evidence that
did bear on a verdict, the instruction was to report the tension rather than act on it; there is none
to report beyond the `Goal` check above.

### 13.8 What I did not do

- I did **not** re-encode either case instance. `wfh-008-instance.yaml` and `vnc-045-instance.yaml` are
  untouched by me; the witness extractor opens them read-only.
- I did **not** apply the guard to the 269 non-witness-bearing `exercised` rows (§13.3) — scoping
  disclosed for the re-audit to rule on.
- I did **not** re-disposition the 28 inverse rows outside the guard's reach (§13.5).
- I did **not** correct W1's generator or its 27 cause-but-`exercised` rows; §13.4 is a finding about
  it, and W1 owns its own artifacts. The reconciled ledger is correct at those paths regardless,
  because the guard measures the instance rather than trusting either table.
- I did **not** rule on my own repair. The same independent `factory-validator` re-audits.

**Transitive sources: none added.** The witness extractor reads the two case instances and M01, all
already in the alphabet. My round-0 ledger entry `T-W4-01` (read-only remote-state queries) is
unchanged and nothing was added to it.

---

## Citations

- `{type: docs, ref: "product/factory/proposals/organizational-data-model-v5.yaml", title: "Organizational Data Model — V5 (pinned, sha256 bf8e5536…9841060, 561 lines; digest re-verified by W4)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/factory/proposals/codex-organizational-data-model-v4-review.md", title: "Review — codex-organizational-data-model-v4.yaml, incl. §9 V5 sanity findings S1–S8", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/SCOPE.md", title: "wfh-011 — Organizational data-model instantiation and rejection test, with the Premise Recheck, anti-force-fitting Amendment, and Human-resume extensions", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/findings-W1-research-instance.md", title: "wfh-011 W1 — Research-case instantiation of wfh-008 (adjudicated at commit 72b98b9, after two corrections)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/findings-W2-software-instance.md", title: "wfh-011 W2 — Software-case instantiation of vnc-045", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/findings-W3-rejection-suite.md", title: "wfh-011 W3 — Adversarial invalid-instance and traversal suite", org: "arch-research garage", year: 2026}`
- `{type: dataset, ref: "product/research/wfh-011/artifacts/rejection-results.csv", title: "115 executed rejection fixtures — 82 rejected-mechanically, 18 accepted-defect, 9 not-falsifiable, 5 specified-not-enforced, 1 negative test (re-executed byte-identical by W4)", org: "arch-research garage", year: 2026}`
- `{type: dataset, ref: "product/research/wfh-011/artifacts/traversal-results.csv", title: "67 traversal rows over the W3 synthetic baseline (re-executed byte-identical by W4)", org: "arch-research garage", year: 2026}`
- `{type: dataset, ref: "product/research/wfh-011/artifacts/wfh-008-coverage.csv", title: "wfh-008 case coverage — 468 rows (re-generated byte-identical by W4 at commit 72b98b9)", org: "arch-research garage", year: 2026}`
- `{type: dataset, ref: "product/research/wfh-011/artifacts/vnc-045-coverage.csv", title: "vnc-045 case coverage — 679 X rows (re-generated byte-identical by W4)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/factory/themes.md", title: "Standing research themes — theme:workflow-harness (lens, coordinator envelope, load-bearing operations≠knowledge boundary)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-010/findings-W1.md", title: "wfh-010 W1 — Research-domain reconstruction; §1 R08 transitive commit ledger (table verified correct by W4; its 'displayed abbreviations' explanation verified incorrect)", org: "arch-research garage", year: 2026}`
- `{type: repo, ref: "dug-21/arch-research", title: "wfh-008 durable git history — twelve post-rebase commits on main, all ancestors; ten pre-rebase objects on no published branch (verified by W4 via git ls-remote and fetch --prune --dry-run)", org: "arch-research garage", year: 2026}`
- `{type: repo, ref: "dug-21/unimatrix@37c7b09aa0db6ba16f5f95dadd24c58adb4e6e2b", title: "vnc-045 merge commit — single parent (squash), 43 files under product/features/vnc-045/, 226 feature directories with 154/157/153 gate-3a/3b/3c reports (all re-measured by W4)", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:product/features/vnc-045/SCOPE-RISK-ASSESSMENT.md", title: "vnc-045 SCOPE-RISK-ASSESSMENT — SR-10 records the program grade vocabulary {proven, partial, missing, asserted} (read at source by W4)", org: "dug-21", year: 2026}`
- `{type: repo, ref: "https://github.com/dug-21/unimatrix/issues/928", title: "Issue #928 comment 4898695344 — SLN1 (#5528) recorded as curve/nfr, asserted; OQ-1 rules 'claimed' a slip (read at source by W4)", org: "dug-21", year: 2026}`
- `{type: docs, ref: ".claude/rules/unimatrix-access.md", title: "Unimatrix Access Rules (factory agents) — recorded attribution is persisted self-assertion, not attestation", org: "arch-research garage", year: 2026}`

---

**Status: W4 complete.** Directional, structure-only, cross-case. No Unimatrix write, no grade
movement, no `proven`, no model edit, no replacement schema, no build recommendation. The coverage
audit and the human gate are next; synthesis is neither mine nor authorised by this file.
