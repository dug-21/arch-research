# wfh-011 W1 — Research-case instantiation: `wfh-008` as Organizational Data Model V5 instances

**Role:** `factory-researcher` · **workstream:** W1 only · **run:** `wfh-011` (research-scope, **DIRECTIONAL**, phase `tech-discovery`, Issue #70)
**Method:** deterministic local parsing and read-only repository/forge/graph inspection. No compute, no external cost, no network research, no model edit, no Unimatrix write.
**Evidence labels:** **[MEASURED]** a command was run and its output is reproducible from the artifacts · **[DOC-CLAIM]** an actor-authored assertion in the fixed alphabet · **[INFERENCE]** my reasoning over the two.
**Nothing here is demonstrated-by-us evidence about V5's runtime behaviour.** No enforcement point for this model exists; every "check" below is one I wrote for this workstream.

---

## 0. Premise verification, first

**[MEASURED]** I re-verified the pinned model myself before consuming it, as required:

```
$ sha256sum product/factory/proposals/organizational-data-model-v5.yaml
bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060
```

Matches the pin in the SCOPE's Premise Recheck extension. An independent PyYAML 6.0.3 parse returns
`core=7 supporting=8 registries=6 catalogs=3 values=8 invariants=19 event_types=9 excluded=11 open=11`,
all six formerly-split S1 scalars complete (`A0` retains "…without discretionary work initiation";
`A5` retains "authority structures or strategic objectives"), and a whole-file stray-key scan finds
none. **S1 is closed for this digest.** The file was parsed as-is throughout: nothing quoted,
normalised, patched in memory, or imported from M02's intended prose.

---

## 1. Headline

**`wfh-008` encodes into V5 as 191 conforming instance objects across 14 of the 15 constructs, with
zero new common constructs, zero domain-specific core entities, and four program-owned registry
extensions. The fifteenth construct — `Capability` — could not be instantiated at all.**

The three results that matter most are not about whether the model fits. They are:

1. **The case demonstrates ZERO enforced authority.** `Delegation.enforced_by` is empty on 31 of 31
   Delegations. The single refusal receipt in the entire history is a *schema* refusal, not an
   authority refusal. I12's second clause — *only an EffectBoundary disposition demonstrates enforced
   authority* — has no witness. **[MEASURED]**
2. **A rebase reissued every `wfh-008` commit id, and `M04` explains the resulting mismatch
   incorrectly.** `wfh-010` W1 §1 attributes it to "differing displayed abbreviations"; `6acc952` and
   `7cf95b2` are distinct objects with the same tree, not two renderings of one. **That reading is
   wrong and I have the trees to prove it.** This is a documentation defect in a source document, not
   a break in the fixed alphabet — see the correction in §5.3, which retracts a stronger claim this
   line previously carried. **[MEASURED]**
3. **V5 could not represent the run's stated capability target, and refused to let its authored
   summaries pass as measurements.** The first is a gap; the second is the model working.

**Verdict I am entitled to at this altitude:** the seven-entity hypothesis is **not falsified by this
case**, and it is **not confirmed** either. Six core entities carried real work. The seventh was
untestable here. Compression is plausible on one domain and unproven generally — exactly where
`wfh-010` left it.

---

## 2. Outputs and how to reproduce them

| Artifact | Lines | SHA-256 |
|---|---:|---|
| `/workspaces/arch-research/product/research/wfh-011/artifacts/wfh-008-instance.yaml` | 5388 | `011de28058817c7f750c7450b8ca31d4d8aeb890659f3f69845ebf6e914361c9` |
| `/workspaces/arch-research/product/research/wfh-011/artifacts/wfh-008-counterfactual-instance.yaml` | 415 | `33887044db11028bb546ddb119a2e9c8714b23584089b0ad66119797e333f669` |
| `/workspaces/arch-research/product/research/wfh-011/artifacts/wfh-008-coverage.csv` | 469 (468 rows) | `e1977062fc3cfdc1cf0841760150f5ef9bc61af9c60aecc76b30b5ca7d86f645` |
| `/workspaces/arch-research/product/research/wfh-011/artifacts/wfh-008-validate.py` | 408 | `eed0485f42f32ec07661db26137811b6650552a4b078b3b97f2e332b1f8e621e` |
| `/workspaces/arch-research/product/research/wfh-011/artifacts/wfh-008-coverage-gen.py` | 462 | `174f0fbeba9fabc598572ed009b295449c7e3af139c55e080cf9ba3db8631b2f` |
| `/workspaces/arch-research/product/research/wfh-011/artifacts/wfh-008-validate.out.txt` | 115 | `5042d234ad31830f02955c02c96d465531a60b267c220b7e3bea69df157c9094` |
| `/workspaces/arch-research/product/research/wfh-011/artifacts/wfh-008-coverage-gen.out.txt` | 14 | `6576e352576a9684a3d99d7e44ea1653d1a4e13c153be69b42d642eab82ecf1a` |

```bash
cd /workspaces/arch-research
python3 product/research/wfh-011/artifacts/wfh-008-validate.py \
  product/factory/proposals/organizational-data-model-v5.yaml \
  product/research/wfh-011/artifacts/wfh-008-instance.yaml \
  product/research/wfh-011/artifacts/wfh-008-counterfactual-instance.yaml

python3 product/research/wfh-011/artifacts/wfh-008-coverage-gen.py \
  product/factory/proposals/organizational-data-model-v5.yaml \
  product/research/wfh-011/artifacts/wfh-008-instance.yaml \
  product/research/wfh-011/artifacts/wfh-008-counterfactual-instance.yaml \
  product/research/wfh-011/artifacts/wfh-008-coverage.csv
```

**Validation result — 0 errors:**

```
MODEL   product/factory/proposals/organizational-data-model-v5.yaml
        sha256 bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060  version 5.0.0
        core=7 supporting=8 registries=6 catalogs=3 values=8 invariants=19 event_types=9 excluded=11 open=11

INSTANCE .../wfh-008-instance.yaml
         counterfactual=False  provenance_class=observed-history
         model pin MATCHES parsed model digest
         191 instance objects across 14 constructs

         INVARIANT CHECKS (only those an instance can decide):
           I13 every Capability required by >=1 Goal ......... PASS  (vacuous: 0 Capability instances)
           I15 Unit identity survives rework (multi-Attempt) .. PASS  witnesses=['UN-RUN','UN-SCOPE','UN-W1',
               'UN-W2','UN-W4','UN-W5','UN-W6','UN-W7','UN-AUDIT-R2']
           I16 distinct intended_outcome per Unit ............ PASS
           I17 derived Delegation does not exceed parent ..... PASS  (tier + effect_grants only)
           I17 authority chain reaches a Scope root .......... PASS
           I12 enforced authority (a boundary enforcing a Delegation) NOT WITNESSED
           Delegation.enforced_by empty on 31/31 Delegations
           I4  observation Events with mechanical epistemic_kind ['EV-015'] (2 observation Events total)
           I1  Record supersession chains present ........... ['RC-COV-R2', 'RC-UNI-316']

         EXCLUDED-CONSTRUCT NEGATIVE TEST:
           excluded constructs appearing as instance sections: NONE — negative test PASSES

INSTANCE .../wfh-008-counterfactual-instance.yaml
         counterfactual=True  provenance_class=counterfactual
         4 instance objects across 3 constructs

RESULT: 0 error(s), 33 warning(s), 8 note(s)
```

The 33 warnings are the machine-visible record of model-forced approximations and unenforceable rules;
the 8 notes carry the S2 qualified-inverse special case and the counterfactual/history boundary. **A
zero-error run is not a claim that V5 is enforced anywhere.** `wfh-008-validate.py` is a checker I
wrote this session for this workstream. `M01.meta.enforcement_reality` says plainly that no common
cross-program checker implements this model, and that is still true.

### What the checker actually decides

| Class | Mechanically checked | Notes |
|---|---|---|
| Required/optional fields, types, enums, `ref<>` resolution, registry and value membership | **yes** | including `ref<Delegation\|Scope>` union targets |
| Relation targets, cardinalities | **yes** | caught the `Delegation.unit 0..1` violation |
| Declared inverse symmetry | **yes** | including the S2 dotted `Unit.gated_by` form, special-cased |
| Registry-extension conformance to each registry's declared `shape` | **yes** | key-by-key |
| Event `required_extension` completeness per registered type | **yes** | |
| `gate_outcome` vocabulary resolving through the assessment's pinned `gate_version_ref` | **partially** | degrades to WARN — see §6.5 |
| I13, I15, I16, I17 (two axes), I12 (witness count), I1 (id uniqueness, chains), I4 (witness count) | **yes** | |
| I2, I3, I5, I6, I7, I8, I9, I10, I11, I14, I18, I19 | **no** | `specified-not-enforced` in the CSV |

---

## 3. Disposition counts

From `wfh-008-coverage.csv`, **468 X-alphabet rows**, enumerated *mechanically from the pinned model*
so no item can be silently dropped:

| Disposition | Rows |
|---|---:|
| `exercised` | **339** |
| `construct-pressure` | **76** |
| `not-applicable` | **49** |
| `blocked-by-OPEN` | **3** |
| `inspected-no-material-instance` | **1** |

**Pressure classification tally** (row-weighted; 43 rows carry more than one cause, and multi-cause
rows retain every applicable classification):

| Cause | Rows |
|---|---:|
| `model-defect` | **65** |
| `historical-evidence-gap` | **40** |
| `project-evolution-candidate` | **14** |
| `enforcement-gap` | **14** |
| `unresolved` | **2** |

**28 distinct pressures** (`PR-*`), every one attached to at least one row; the generator asserts none
is declared-but-unused. **7 distinct project-evolution candidates**, each carrying all five required
analyses — verified mechanically, not by eye:

```
distinct project-evolution candidates: 7
  PR-RECORD-DIGEST: COMPLETE      PR-METHOD-CUSTODY: COMPLETE
  PR-ROLE-UNDEFINED-ASSESSOR: COMPLETE   PR-ATTEMPT-DISPOSITION: COMPLETE
  PR-BASELINE-REWRITE: COMPLETE   PR-OBSERVATION-RAW-EVIDENCE: COMPLETE
  PR-SKILL-NAME-COLLISION: COMPLETE
incomplete: 0
```

`project-evolution-candidate` appears on **14 of 155** pressure-bearing rows and never alone as a
residual bucket: every one of the seven co-classifies with `model-defect`, `enforcement-gap`,
`historical-evidence-gap` or `unresolved`.

---

## 4. What fitted, and fitted well

These are positives with witnesses, not encouragement.

**4.1 The theme's authority envelope IS a Delegation, field for field.** `themes.md`'s `coordinator:`
block maps onto `DL-COORD-STANDING` with nothing left over: `may_launch.confidence` and the
concurrency/depth caps into `resource_ceiling`; `may_spend` into `resource_ceiling`; `must_escalate`
into `escalation_conditions`; the tier into `autonomy_tier`; owner authorship into
`definition_custodian_ref`. **This is the strongest exclusion result in the case.** `wfh-010` W1
carried `Envelope` as candidate noun N7 and the project's own file literally calls it "the first
delegated-autonomy envelope". V5 excludes `Envelope` on the grounds that limits travel with
Delegation — and the historical envelope decomposes onto Delegation without residue. **[MEASURED]**

**4.2 I6's six-way separation held across the coverage gate.** `EV-013` (assessment) → `EV-014`
(gate_outcome) → `EV-024` (the coordinator's separate confirmation decision) → `EV-023` (transition)
→ `EV-017` (effect_request) → `EV-018` (effect_disposition) → `RC-COV-R2` (Record) are seven distinct
objects with different actors and different authority over one gate. The assessor could rule the
outcome and could not advance the phase; the coordinator could confirm and could not rule. That
distinction is carried by typed structure, not prose. **[MEASURED]**

**4.3 R2's assessment/gate_outcome split earns its keep.** `RC-COV-R2` is one Record carrying **two**
assessments and **two** gate outcomes over **two different subject baselines**, plus two in-place
amendments. The round-2 `REWORKABLE` (§7) and the final `PASS` (§9) are not a supersession — they rule
on different rework passes — and only the split lets the instance say so. **[MEASURED]**

**4.4 I15/I16 discriminate rework from redefinition, mechanically.** Nine Units carry multiple
Attempts under one intended outcome. `UN-AUDIT-R2` carries two Attempts against *different* baselines.
The pre-distillation correction pass is modelled as its own Unit (`UN-CORRECTIONS`) rather than more
Attempts of W1/W2/W4/W6, because its intended outcome differs — that is I16 doing work, not me
choosing. The checker confirms no two Units share an intended outcome. **[MEASURED]**

**4.5 A3's withdrawal is vindicated.** Both required one-way traversals ran against the instance with
no added relation and no global scan: `Goal → applicable Workflows` by filtering `Workflow.applies_to`
(both Goals resolve to `WF-RESEARCH-SCOPE`), and `Actor → participated Attempts` by filtering
`Attempt.actors` (19 Actors resolve; `AC-RWK-P2A → [AT-W1-3, AT-W2-3]`, `AC-CUR → [AT-SYNTH-1,
AT-CLOSE-1]`). Meanwhile the **declared** inverses are real constraints: **24 inverse edges had to be
closed mechanically** before the instance validated. The model's own rule — declare an inverse when it
expresses domain navigation, not backward-query convenience — separated the two correctly. **[MEASURED]**

**4.6 I17's checkable half caught a real error on the first run.** My first encoding gave the leader's
close-time grant `graph-write`, which its parent `DL-RUN-2` does not carry. The attenuation check
rejected it. The correct history is that the close-time writes of `#320`/`#321` ran under the
curator's own standing grant, and the instance now carries `DL-CUR-CLOSE`. **A model rule found a
modelling error in the case data.** That is the only place in this workstream where a V5 rule did work
a human reading had not already done. **[MEASURED]**

**4.7 `extend_by_registration` absorbed everything, including the awkward case.** Four program-owned
registry extensions (8 unit kinds, 9 record categories, 5 effect classes, 1 event type) and no new
common construct. The awkward case is instructive: an *unauthorized* change to a governing definition
does not fit `adaptation`, whose parsed definition and required `decision_ref` both presuppose
authorization — so it entered as a registered `unrecorded_change` type rather than by stretching
`adaptation` or adding a noun. **[INFERENCE from MEASURED parse]**

**4.8 V5 refused to let authored summaries pass as measurements.** `observation` requires
`raw_evidence_ref`. `wfh-008` retained **no** raw command output for any enumeration against the
target repository — only authored summaries. Under I4 those are claims, and the instance encodes them
as claims. Exactly **one** Event (`EV-015`) carries a real `raw_evidence_ref`, and only because git
objects are content-addressed. `EV-016` is an `observation` with `epistemic_kind:
reported-observation` — the A8 orthogonality rule restored to `values.epistemic_kind` is what makes
that expressible, and it is the correct reading. **[MEASURED]**

---

## 5. The five results that are adverse

### 5.1 `Capability` is not instantiable from this case — `PR-CAPABILITY-ABSENT`

**Classification: `historical-evidence-gap` + `model-defect`.**

`R01` states the capability target is "proposed `jurati-arch-002` — no Unimatrix capability id".
V5's `Capability` requires `name`, `observable_behavior`, `scope_ref`, `done_when` and `grade`. The
alphabet supplies neither an observable behavior nor a `done_when`, and inventing them is forbidden.
`Capability` also has **no `lifecycle_state` field** — `Goal`, `Actor` and `Record` all have one — and
no admissible "proposed / not yet specified" state.

So the instance has **zero Capability objects**, and with them go: I9, I13, I14 (all vacuous), the
whole `capability_classification` registry (4 seeds, none exercisable), `Capability.composed_of` /
`prerequisite_of` / `delivered_by` / `enabled_by`, `Unit.delivers`, `Technology.enables`, and
`Goal.claim_floor` (empty on both Goals).

**`current-project fit`: NOT REPRESENTABLE.** **`post-bounded-evolution fit`: not applicable —
no evolution is proposed.** Giving `jurati-arch-002` an `observable_behavior` and a `done_when` has
exactly one justification, that V5 requires them. That is the circular force-fitting the amendment
prohibits, and it is recorded in `CF-REJECTED`, not proposed. The `model-defect` half stands on its
own: a Goal may legitimately name a capability target that is not yet specified, and V5 has no shape
for it.

**Consequence for the run:** roughly a seventh of the core model is untested by this case. W2's
software case is where `Capability` gets its real test; if `vnc-045` also cannot instantiate one, that
is a much larger result than either case alone.

### 5.2 Zero enforced authority — `PR-ENFORCED-AUTHORITY-ABSENT`

**Classification: `enforcement-gap`.**

`Delegation.enforced_by` is empty on **31 of 31** Delegations **[MEASURED]**. The model's own rule
says it: *without a boundary authority is declared only.*

The one refusal receipt in the case is `EV-018`/`EV-019` — five `context_cycle` calls refused by
Unimatrix, once for a 512-character `outcome` cap and four times for control characters. The run's own
disclosure confirms `agent_id` was present on all five. **That is a schema refusal, not an authority
refusal.** So the sole boundary in the instance, `EB-UNIMATRIX`, carries `can_refuse: true` with a
real receipt and `enforces: []` — it enforced a payload shape, not a Delegation.

The garage's strongest custody claim — single-writer curator — has no enforcement point at all. Any
actor may call `context_store`; the server checks only that an identity *string* is present, and
`.claude/rules/unimatrix-access.md` says that string is persisted self-assertion, not attestation.

**`current-project fit`: representable and empty, which is a correct and important negative — not a
model failure.** No evolution proposed: making the curator rule enforced needs a credential boundary
that does not exist and cannot be costed from the fixed alphabet, and proposing it would be the build
recommendation this scope forbids.

### 5.3 A rebase reissued the commit ids, and `M04` explains it wrongly — `PR-BASELINE-REWRITE`

**Classification: `enforcement-gap` + `project-evolution-candidate` (CF-01).**

> **CORRECTION, 2026-08-29 — this section previously overclaimed and is retracted in part.**
> An earlier version of this finding said the run's durable records "cite ten commit ids that no
> longer exist on `main`", that "every `baseline_ref` the run recorded now dangles", and that a W3/W4
> row pinning a `wfh-008` commit id "will not resolve". **All three are retracted as wrong.** The
> measured position is below. The flag was also raised as contradicting a load-bearing premise of the
> scope; **it does not**, and it is downgraded to a documentation defect in `M04`. The retraction was
> prompted by an independent re-run whose result I reproduced before conceding.
>
> **Downstream effect, measured rather than asserted:** re-running the generator after the correction
> changes **2 of 468** CSV rows (`invariant:I1`, `notation:identity`), both text-only. **No row changed
> `disposition` and no row changed `cause_classification`** — because the cause was always the rebase
> itself, which is measured and unretracted, not the resolvability claim built on top of it. The
> `enforcement-gap` classification stands on the absence of any supersession link or adaptation Event
> for the rewrite; the `project-evolution-candidate` stands on a restated and smaller rationale.

**What is measured and stands.** A rebase reissued every `wfh-008` commit id after the run closed:

```
$ git log --format='%h  author=%ad  committer=%cd' --date=iso --reverse -- product/research/wfh-008
7cf95b2  author=2026-08-28 11:49:58 +0000  committer=2026-08-28 14:20:37 -0400
36e35e1  author=2026-08-28 12:27:02 +0000  committer=2026-08-28 14:20:37 -0400
...
b847cee  author=2026-08-28 15:12:31 +0000  committer=2026-08-28 14:20:37 -0400
```

Twelve spread author timestamps against **one uniform committer timestamp** — the rebase signature —
with the author identity `Claude Opus 4.8 <noreply@anthropic.com>` preserved and the committer
identity `dug-21 <angryweed@gmail.com>` applied uniformly, matching a reflog `rebase (finish)` at
2026-08-28 18:20 UTC. Trees are identical across pairs (`6acc952 == 7cf95b20`, `0c01522 == 36e35e1e`,
`17ebf2e == 9158a119`, `962a6c1 == 61b9b1de`).

**Therefore `M04` (`wfh-010/findings-W1.md` §1) is wrong where it says the difference is one of
"displayed abbreviations".** `6acc952` and `7cf95b2` are distinct objects. That is a real defect in a
document inside this run's fixed alphabet, and it is what W3/W4 need to know.

**What is retracted.** I claimed the mismatch left `wfh-008`'s recorded baselines unresolvable. It
does not:

```
$ for c in <the twelve full oids in M04's R08 ledger>; do git merge-base --is-ancestor $c main; done
  -> ANCESTOR-OF-MAIN for all twelve, zero exceptions

$ for c in 6acc952 0c01522 17ebf2e 7d28294 3cd296d 215942d 962a6c1 017f4fc c29a08f cd03ad0; do
    git merge-base --is-ancestor $c main; git cat-file -e $c; done
  -> ancestor=NO, object-present=YES  for all ten
```

`M04`'s R08 ledger pins the **post-rebase full oids, and all twelve are on `main`**. Nothing in the
fixed alphabet's commit ledger dangles. The ten *short* ids quoted in Issue #66 prose are not
ancestors of `main`, but every one still resolves as an object, because the pre-rebase branch
`workflow/agentic-organization-reframe` retains them — and that branch is **published on `origin`**,
not merely local, so a fresh clone that fetches all refs resolves them too.

**Epistemics, stated in both directions.** Those ten ids are *unreachable from `main`* and *reachable
from a published side branch*. That is not durability: nothing protects that branch, and deleting it
would make ten gate citations in the run's governance record unresolvable. It is also not breakage:
today they resolve, and their trees are identical to their `main` counterparts. I overclaimed in one
direction and will not now overclaim in the other.

**My instance was already correct and needs no change.** Every `baseline_ref` in
`wfh-008-instance.yaml` is a post-rebase full oid; all twelve verify as `ANCESTOR-OF-MAIN`. I never
routed a value through `EV-032`'s mapping. The mapping in `EV-032.extension` is a *record of the
rewrite*, not a substitution table anyone needs to apply.

**What survives as pressure on V5, at its correct and reduced weight.** `Unit.baseline_ref` and
`Attempt.baseline_ref` are `text`. The identity of a pinned baseline was reissued with **no adaptation
Event and no supersession link** — git carries no pointer from `9158a11` back to `17ebf2e`; the old
object survives only because a branch ref happens to retain it. Contrast Unimatrix, where the same
operation (`context_correct`) reissues an id **and** leaves a queryable chain: `#312` is deprecated,
`#316` is active, and `context_graph(mode:"chain")` walks between them (re-read live 2026-08-29).

So I1 — *history is superseded, never overwritten* — is **carried by one custody store and not by the
other**, and V5 has no way to say which store an identity lives in or whether that store preserves a
supersession link. That is S4's atomicity argument made concrete, and it is the finding. It is a
smaller finding than the one I first filed.

- **`current-project fit`: REPRESENTABLE, and unverifiable only in the narrow sense that `text`
  carries no integrity binding and no supersession link.**
- **`post-bounded-evolution fit` (CF-01): REPRESENTABLE** — identical V5 shape; a tree oid is
  invariant under rebase, so the pin survives the operation that reissued the commit id.
- **Independent reason (restated at its true weight):** ten gate citations in the run's governance
  record depend for resolvability on a side branch that no policy protects. That is a modest
  reproducibility exposure in a method whose product is reproducible evidence, and it is true with or
  without V5. It is **not** the "a reader cannot reproduce the audited tree" claim CF-01 originally
  carried, which is withdrawn.

### 5.4 An interrupted Attempt has no admissible disposition — `PR-ATTEMPT-DISPOSITION`

**Classification: `model-defect` + `project-evolution-candidate` (CF-03) + `historical-evidence-gap`.**

`AT-RUN-1` — the original leader's execution — terminated on platform credit exhaustion. **No actor
recorded a disposition.** `Attempt.disposition` is required with
`enum[continue,hold,cancel,rework,complete]`; none is true. The instance writes `hold` and marks it
`_approx`, so the checker reports it as `MODEL-FORCED-APPROXIMATION` rather than burying it.

This is the *same argument* M02's R2 finding made for splitting `gate_outcome` from `assessment` — an
abandoned assessment must leave a trace — applied to `Attempt`, where V5 did not apply it. The review
called merging assessment-with-outcome while splitting request-from-disposition "internally
inconsistent". `Attempt` carries the same inconsistency and nobody raised it.

- **`current-project fit`: NOT FAITHFULLY REPRESENTABLE.**
- **`post-bounded-evolution fit` (CF-03): STILL NOT FULLY REPRESENTABLE.** A typed interruption record
  supplies the *resume* side — which V5 already carries well, and `AT-RUN-2.resume_requirements` is
  the strongest positive witness for that field in the case — and leaves the *termination* side
  exactly where it was. **Per the amendment: the model defect survives the project evolution and stays
  adverse.**
- The counterfactual object `CF03-AT-RUN-1` deliberately **still carries `_approx` on `disposition`**.
  It exists to make the residue visible, not to show the model passing.

### 5.5 Independence is asserted and unverifiable — `PR-INDEPENDENCE-UNVERIFIABLE`

**Classification: `enforcement-gap`.**

`Gate.independence_predicate` and the assessment extension's `independence_check` are required text.
Both are populated from the auditors' own headers. At the custody layer nothing distinguishes them:
**every** `wfh-008` commit carries the git author `Claude Opus 4.8 <noreply@anthropic.com>`, and **all
nine** Issue #66 comments — including the owner's scope approval and the final synthesis verdict — are
posted by the single GitHub account `dug-21` **[MEASURED]**. Nothing in the forge record distinguishes
a human decision from an agent relay.

I7 (*gates fail closed when required independence cannot be established*) is therefore never
mechanically evaluable in this case. The round-2 auditor *behaved* correctly — it declined to clear
predicate 6 on the leader's reading "because the reading was offered by the party with an interest in
it" and ran its own third sweep — and that behaviour is a disposition, not an enforced constraint.

This is the case's own instance of `#320`, the custody predicate it discovered in MetaHarness: *a
control whose input, custody or call-site enumeration sits inside the governed party is a label, not a
control.* Applied to the run's own independence claim, it holds.

---

## 6. The remaining construct pressures, in brief

Full text and all superseding fields per row are in `wfh-008-coverage.csv`.

**6.1 `PR-SCOPE-AUTHORITY-ROOT` — `model-defect`.** `Scope.authority_root_ref` is required and defined
as "holder of undelegated authority for this Scope". `SC-MIS` and `SC-TEAM` are nested Scopes holding
*no* undelegated authority. Naming the owner (what the instance does) makes the field carry no
information below the collective; naming the leader would assert authority the leader did not hold.
The model forces one of two wrong answers on every nested Scope.

**6.2 `PR-BOUNDARY-CAN-REFUSE` — `model-defect` + `historical-evidence-gap`.**
`EffectBoundary.can_refuse` is a required `bool` with no `unknown`, while the sibling
`effect_disposition` vocabulary *does* carry `unknown`. Git and the forge performed effects throughout
and never refused one; neither `true` nor `false` is evidenced. The instance therefore **declines to
instantiate them as EffectBoundaries at all** rather than assert an unevidenced bool — which is why
`EV-005` carries a `target_boundary_ref` naming no instance. Not representable without a fabrication.

**6.3 `PR-DELEGATION-UNIT-CARDINALITY` — `model-defect`.** `Delegation.unit` is `0..1`. Three
historical rework directives each covered several Units (pass 1: W1+W2+W4; pass 2a: W1+W2; pass 2d:
W5+W7). Each had to be split, turning three organizational grants into six model objects and losing
the fact that they were one directive. The checker caught this — it is not a judgement call.

**6.4 `PR-GATE-PROCEDURE` — `model-defect`, disposition `blocked-by-OPEN`.**
`Gate.procedure` is `enum[deterministic,judgment]`. `GT-COVERAGE` ran deterministic enumerations (a
sorted-set path diff, a 42/42 lock bijection) **and** independent semantic judgment, and the final
PASS turned on the judgment half. Neither value is true; `judgment` is written and marked `_approx`.
`Gate.open[deterministic versus judgment procedures]` names exactly this hole. `wfh-010` W1 reached
the same conclusion from the other direction ("deterministic condition is too narrow").

**6.5 `PR-GATE-IDENTITY-VERSION` — `historical-evidence-gap` + `model-defect`.** The `assessment`
extension requires `gate_version_ref`. The historical gate has no identity and no version: it is a
paragraph in a protocol file. The instance pins `GT-COVERAGE@v1 (git:.claude/workflow/research-scope.md)`,
which the checker **cannot resolve to a versioned Gate object**, so `gate_outcome` vocabulary
resolution degrades from an ERROR to a WARN. `open.gate_identity` is exercised and unresolved.

**6.6 `PR-METHOD-CUSTODY` — `enforcement-gap` + `project-evolution-candidate` (CF-02).** I18 requires
Workflow/Gate/Delegation custody outside the governed activity. All method definitions live in
`.claude/` inside the repository the governed agents write to; **there is no `CODEOWNERS` file and no
branch-protection artifact in the tree [MEASURED]**. Two facts cut opposite ways: the method surface
was *not* edited during the run (no `.claude/` commit on 2026-08-28 — a positive behavioural
observation), and `research-scope.md`'s most recent revision (`9d7806a`, 2026-08-27) was authored by
the agent identity `Claude Opus 4.8`, i.e. the governed actor class edited its own governing
definition. Plus the evidenced incident: an `npx @dug-21/unimatrix@0.11.3` install silently overwrote
twelve method files with copies predating the D6 amendment, with no decision Event. **CF-02's manifest
DETECTS drift and does not establish custody** — the manifest itself lives inside the governed
repository, so `#320` applies to it. I18 stays unsatisfied in both the current and the evolved form.

**6.7 `PR-RECORD-DIGEST` — `model-defect` + `project-evolution-candidate` (CF-07).**
`Record.content_digest` is a required `digest`. Eleven file-backed Records carry a real sha256. Eleven
service-backed Records cannot: Unimatrix, the forge and the cycle service expose no content digest.
The instance writes sentinels; the checker reports every one.

**6.8 `PR-ACTOR-IDENTITY-SINGULAR` — `model-defect` + `unresolved`.** `Actor.declared_identity` is one
`text` field. Fifteen Actors share `"factory-researcher"`; two share `"research-leader"`; `AC-OWNER`
carries three identity strings across two custody stores. **The field does not individuate an Actor at
all** — the only individuator in the instance is the Delegation's `unit`. No evolution proposed: a
per-instance `agent_id` would individuate, but D6 rules the opposite explicitly, and relitigating a
ratified decision from outside its evidence is not this workstream's job.

**6.9 `PR-DELEGATION-SELF-GRANT` — `model-defect`.** `DL-SCOPE` has `grantor == grantee`: `AC-LEAD-1`
self-assigned the scope-authoring Unit and then requested its own gate on it. V5 neither forbids nor
detects this.

**6.10 `PR-RECORD-INPLACE-OVERWRITE` — `enforcement-gap`.** I1 and `Record.supersedes` say correction
never overwrites history. `RC-COV-R2` was amended in place **twice** after publication; the findings
Records were edited in place across three rework passes and one correction pass. No Record identity
was reissued. The prior versions survive only in git — whose identities were then rewritten (§5.3).
The run's genuinely honest practice of retaining the superseded verdict verbatim *inside* the amended
file is a convention, not a guarantee.

**6.11 `PR-DELEGATION-ATTENUATION-COMPARISON` — `model-defect`.** I17 says a derived Delegation may
not exceed its parent "on any axis". Two axes are decidable (`autonomy_tier` ordinal,
`effect_grants` a set) and were checked. Twenty derived Delegations are **UNDECIDABLE** on
`escalation_conditions` (a text list) and `resource_ceiling` (a heterogeneous map).
`open.delegation_attenuation` names it and it is still open.

**6.12 `PR-I19-BINDING-ALTITUDE` — `model-defect`.** This instance registers program-owned extensions
whose owners are `Workflow`, `Scope`, `Scope` and the registry. I19 is cited by `Workflow` **alone**,
so nothing binds it to three of the four. Review finding S6 raised this and the pinned file does not
resolve it.

**6.13 `PR-SKILL-EVIDENCE-ABSENT` — `historical-evidence-gap`.** `Actor.has_skill` declares attributes
`[evidence_refs, grade, currentness, expires_at]`. **Not one of the four is populated for any of the
22 Actor–Skill pairs.** Agents are assigned by type, never by evidenced competence.
`SK-BUDGET-CONTROL` is the sharpest case: the run failed on credit exhaustion while that Skill carried
no grade and no expiry.

**6.14 `PR-SKILL-NAME-COLLISION` — `project-evolution-candidate` + `unresolved` (CF-06).** The Skill
instances come from the `capabilities:` frontmatter key in `.claude/agents/factory/*.md`. The
project's word *capabilities* denotes V5 `Skill`, not V5 `Capability`. I10 exists to keep them apart
and the repository's own vocabulary runs them together.

**6.15 `PR-ROLE-UNDEFINED-ASSESSOR` — `historical-evidence-gap` + `project-evolution-candidate`
(CF-05).** `Gate.requires_assessor` is cardinality 1 to a Role. `GT-COVERAGE`'s assessor is
`RO-COVERAGE-AUDITOR` — a Role with **no definition file** under `.claude/agents/`. The protocol
reserves `factory-validator` for validated runs, so a directional run has no defined gate-assessor
Role. `wfh-010`'s equivalent gate was ruled by a `factory-validator`; `wfh-008`'s by a
`factory-researcher`. The same blocking gate, two role identities, consecutive runs.

**6.16 `PR-EVENT-IDENTITY-THRESHOLD` — `historical-evidence-gap` + `enforcement-gap`.** `EV-004`
(scope → tech-discovery) is a `durable: always` transition whose cycle event **never reached
Unimatrix**; it is attested only by an Issue comment. All phase boundaries for the scope phase and the
first tech-discovery pass are permanently missing and were deliberately not backfilled — which was the
right call and leaves the model unable to mark an Event as "occurred but unrecorded by its designated
carrier". `open.event_identity_threshold` is a live hole, not a theoretical one.

**6.17 `PR-LIST-REQUIRED` — `model-defect`.** `Goal.claim_floor` is `list<ref<Capability>>, required:
true`. `notation` does not say whether `required` on a list type means *key present* or *non-empty*.
The instance writes `[]` and no checker can decide whether that conforms — so no rejecting
counterexample can be built for it either.

**6.18 `PR-SCOPE-EFFECTIVE-AT`, `PR-ACTOR-CONTINUITY`, `PR-ATTEMPT-RESUME-OWNER`,
`PR-LESSON-VS-PATTERN`, `PR-CAPABILITY-CLASSIFICATION-UNUSED`.** Smaller; all in the CSV.
`PR-LESSON-VS-PATTERN` is worth one line: `wfh-008`'s most reusable method rule, the custody predicate,
was filed as a **`finding`** (`#320`), not a `lesson-learned`, with no separate admission or retrieval
behaviour. That is one weak data point *against* a behaviourally distinct lesson category — weak
because nobody tried the alternative. `open.lesson_vs_pattern` is exercised, not settled.

---

## 7. Excluded-construct negative tests

All eleven exclusions pass. The checker confirms no excluded construct appears as an instance section.
Three deserve naming:

- **`Envelope`** — the strongest, §4.1. Decomposes onto Delegation with no residue, against a project
  that literally uses the word.
- **`Signal | Decision | Transition | Assessment | Outcome | EffectRequest | EffectReceipt`** — all
  seven appear only as Event types. `wfh-010` W1 carried `Signal` as candidate noun N8; nothing in
  this case wanted it back.
- **`RecordVersion`** — `construct-pressure`, not a clean pass. There is no `RecordVersion` object and
  versions are a plain integer, which is fine. What is not fine is that the historical versions exist
  only in git, whose ids were rewritten. **The exclusion is right and the custody is not.**

`a merged effect event` is worth one line: one `effect_request` (`EV-017`) produced **five**
dispositions (four refused, one performed). A merged event could not represent that at all.

---

## 8. Counterfactuals — separately identified, never merged

`artifacts/wfh-008-counterfactual-instance.yaml` carries **seven** candidates (CF-01…CF-07) and three
explicitly **rejected** ones. Four candidates have encoded instance objects (`CF01-UN-W1`,
`CF03-AT-RUN-1`, `CF02-EV-DETECT`, `CF04-EV-OBS`); three (CF-05/06/07) have none because the evolved
form has the identical V5 shape and only a value's referent changes.

Enforced mechanically, not by discipline:

- every counterfactual object carries `provenance_class: counterfactual`; the checker errors if one
  appears in the historical file or if one in the counterfactual file lacks the marker;
- relations crossing the history/counterfactual boundary are **not** closed back into the historical
  objects — the checker emits `COUNTERFACTUAL BOUNDARY` notes instead of writing the inverse. A
  counterfactual cannot silently attach itself to observed history;
- **no counterfactual object is counted in any coverage number in §3.** The 468 CSV rows are
  dispositions of the *historical* instance.

**Circularity guard.** Each candidate states an independent reason that stands without reference to
V5, and the three rejected ones are rejected precisely because they do not:

- *Give every spawned agent a distinct `agent_id`* — attractive, but D6 rules the opposite and this
  workstream has not examined D6's evidence. Carried as `unresolved`.
- *Instantiate a Capability for `jurati-arch-002`* — **the circular candidate**. The only reason is
  that V5 requires it. Rejected.
- *Make the single-writer curator rule enforced* — would satisfy I12 handsomely and is exactly the
  shape of the build recommendation this scope forbids. Rejected.

---

## 9. Source ledger

Every M and R item closes. Two transitive sources were added before use, per the SCOPE's rule.

| Id | Path / identifier | Closure | Use |
|---|---|---|---|
| `M01` | `product/factory/proposals/organizational-data-model-v5.yaml` | **used** | the model under test; digest re-verified independently; parsed as-is |
| `M02` | `.../codex-organizational-data-model-v4-review.md` | **used** | S1–S8 dispositioned as X rows; R2's abandoned-assessment argument reused against `Attempt`; A3's withdrawal tested by the two traversals. **No intended prose was imported into the model.** |
| `M03` | `product/research/wfh-010/SCOPE.md` | **inspected-no-material-instance** | boundary context; supplies no `wfh-008` instance value |
| `M04` | `wfh-010/findings-W1..W4-data-model.md` | **used** | W1's `wfh-008` reconstruction cross-checked throughout; its A1/A2 tier readings reused. **Its R08 commit ledger is CORRECT — all twelve full oids verify as ancestors of `main` — and was relied on as such. Its *explanation* of the id mismatch ("displayed abbreviations") is contradicted here on measured evidence** (§5.3). Defect recorded, file untouched: it is fixed input. |
| `M05` | `wfh-010/reports/gate-coverage.md`, `gate-coverage-r2.md` | **used** | establishes that `wfh-010`'s equivalent gate was ruled by a `factory-validator` — the comparison behind `PR-ROLE-UNDEFINED-ASSESSOR` |
| `M06` | `product/factory/themes.md`, `theme:workflow-harness` | **used** | `SC-PROG`, `GO-WFH`, and the `coordinator:` block that becomes `DL-COORD-STANDING` field-for-field |
| `R01` | `wfh-008/SCOPE.md` | **used** | `UN-SCOPE`, `RC-SCOPE`, the six coverage predicates, the proof bar, the capability-target statement |
| `R02` | `wfh-008/findings-W1..W7.md` | **used** | seven Units, their intended outcomes, `RC-W1..RC-W7` with real digests, evidence-label discipline |
| `R03` | `wfh-008/reports/coverage.md`, `coverage-r2.md` | **used** | `GT-COVERAGE`, the three assessments and three gate outcomes, independence statements, gap registers |
| `R04` | `wfh-008/REPORT.md`, `reports/relevance.md` | **used** | `UN-SYNTH`, `UN-RELEVANCE`, the graph-write table, the goal-owner's live re-read (`EV-016`) |
| `R05` | Issue #66 body + comments (pinned JSON dumps) | **used** | every decision, adaptation, communication and effect Event; the handover; the five cycle rejections; the identity audit and the skill-overwrite incident |
| `R06` | commits named by R01–R05 | **used** | ordering, authorship, custody and repository effects. 12 commits on `main`; author/committer fields; the tree-equality and ancestry measurements of §5.3 |
| `T01` | **transitive, added** — `.claude/workflow/research-scope.md` (`bd3fa02b…`), `.claude/agents/factory/*.md`, `.claude/rules/unimatrix-access.md`, absence of `CODEOWNERS` | **used** | **Reason:** V5 requires `Workflow.method_statement`, `unit_kinds`, `dependency_rules`, `state_vocabulary` and `definition_custodian_ref`, plus `Role.responsibility` and `Skill.work_class`. The R alphabet contains *instances* of the method, not the method definition. Deriving a Workflow without it would be invention. **Provenance:** tracked files in `dug-21/arch-research` at `main`; read-only; digests recorded in the instance. |
| `T02` | **transitive, added** — read-only Unimatrix reads of `#312`, `#316`–`#321` (`context_graph`, `agent_id: factory-researcher`, 2026-08-29) | **used** | **Reason:** the case's knowledge-node Records and the I1 supersession comparison in §5.3 turn on whether the recorded ids are current and whether the chain is preserved. R05 asserts this; only a read establishes it. **Provenance:** live graph, read-only, four calls, no write. **Result:** `#312` deprecated → `#316` active with the chain queryable; `#317`–`#319` active with four `Motivates` edges into `#316`; `#320`/`#321` active and — a small correction to nobody's claim — carrying **no `Motivates` edge to `#316` at depth 1 in either direction**. |

*Lineage-only files* (`organizational-data-model.yaml`, `-v3`, `codex-…-v4.yaml`,
`agentic-organization-data-model.md`) were **not** consulted; they carry no coverage obligation.

---

## 10. Limits, and what I could not do

- **This is one case, one domain, one directional run.** It establishes nothing about generality,
  runtime enforcement, organizational effectiveness, a product boundary, or semantic compression
  outside `wfh-008`.
- **The zero-error validation is not proof of anything about V5.** `wfh-008-validate.py` is my own
  checker, written this session, and it decides 8 of 19 invariants. The other 11 are
  `specified-not-enforced` in the CSV and are marked as such row by row. **No rule was tested by
  paraphrase, and no missing enforcement was converted into a model failure or a claimed refusal.**
- **`Capability` is untested by this case** (§5.1). So are `capability_classification`, I9, I13 and
  I14. That is a seventh of the core hypothesis with no research-domain witness.
- **I built no invalid instances.** Rejection is W3's partition; I did not encroach on it beyond
  noting where a falsifiable counterexample *cannot* be built (`PR-LIST-REQUIRED`).
- **Independence of the historical auditors cannot be established from the alphabet** (§5.5), so every
  claim in this instance that rests on an audit's independence rests on an assertion.
- **Timestamps for several Attempt boundaries are bounded, not observed** — the alphabet gives commit
  times, not execution times. Marked `_approx` where the model required a value.
- I did not re-research Retort, MetaHarness, SPIFFE/Vault, workflow authorization or the external
  landscape; prior art `#270`, `#278`, `#269`, `#271`, `#275`, `#279` was reuse-only and none of it
  was needed to encode this case.

---

## 11. Flags for the leader, W3, W4 and the coverage auditor

1. **`M04`'s explanation of the SHA mismatch is wrong — but its ledger is right** (§5.3). `wfh-010`
   `findings-W1.md` §1 attributes the mismatch to "displayed abbreviations"; measured, they are
   distinct objects produced by a rebase. **`M04`'s R08 ledger itself is correct and usable** — all
   twelve full oids are ancestors of `main`. Re-read the sentence, keep the table.
2. **RETRACTED — `wfh-008`'s recorded baselines resolve normally.** An earlier version of this flag
   said a W3 fixture or W4 row pinning a `wfh-008` commit id "will not resolve" and directed readers
   to `EV-032.extension` as a substitution table. Both are withdrawn. Pin ids from `M04`'s R08 ledger
   or from my instance's `baseline_ref` values — all are on `main`. `EV-032.extension` is a record of
   the rewrite, not a mapping anyone needs to apply. **This is not a premise break and no scope change
   follows from it.**
3. **Zero enforced authority in the research case** (§5.2). If W2 finds the same in `vnc-045` — where
   a forge merge *is* an externally custodied effect — that is the sharper comparison, and the two
   cases together decide whether I12's second clause has any witness in this garage at all.
4. **`Capability` has no research-domain witness.** If `vnc-045` also cannot instantiate one, W4
   should treat that as a first-order result rather than two independent gaps.
5. **The `_approx` and sentinel markers are machine-readable.** `grep MODEL-FORCED-APPROXIMATION` over
   `wfh-008-validate.out.txt` returns every place the model forced a value the alphabet did not
   supply. That is the honest list, and it should not have to be reconstructed from prose.
6. **The checker is reusable.** `wfh-008-validate.py` takes any number of instance files against the
   pinned model and shares one id space across them, so W2's `vnc-045` instance can be validated with
   the same instrument — which is worth more for cross-case comparison than two independent checkers.

---

## Citations

- type: docs · ref: `product/factory/proposals/organizational-data-model-v5.yaml` · title: "Organizational Data Model — V5" · org: arch-research garage · year: 2026
- type: docs · ref: `product/factory/proposals/codex-organizational-data-model-v4-review.md` · title: "Review — codex-organizational-data-model-v4.yaml" · org: arch-research garage · year: 2026
- type: docs · ref: `product/factory/themes.md` · title: "Standing research themes — theme:workflow-harness" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-008/SCOPE.md` · title: "wfh-008 — MetaHarness architecture and ecosystem dependency analysis" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-008/findings-W1.md` through `findings-W7.md` · title: "wfh-008 delegated research findings W1–W7" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-008/reports/coverage.md` · title: "wfh-008 tech-discovery coverage audit" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-008/reports/coverage-r2.md` · title: "wfh-008 tech-discovery coverage re-audit — round 2" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-008/REPORT.md` · title: "wfh-008 — REPORT: MetaHarness architecture and ecosystem dependency analysis" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-008/reports/relevance.md` · title: "wfh-008 — RELEVANCE / TARGET REVIEW" · org: arch-research garage · year: 2026
- type: docs · ref: `https://github.com/dug-21/arch-research/issues/66` · title: "wfh-008 — Research(directional): MetaHarness architecture, boundaries, and ruflo dependencies" · org: arch-research garage · year: 2026
- type: repo · ref: `dug-21/arch-research` · title: "wfh-008 durable git history — 12 commits under product/research/wfh-008/, plus the pre-rebase branch workflow/agentic-organization-reframe" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-010/findings-W1.md` · title: "wfh-010 W1 — Research-domain reconstruction and vocabulary mapping" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-010/findings-W4-data-model.md` · title: "wfh-010 W4 — Common ontology/data-model specification" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-010/reports/gate-coverage.md` · title: "wfh-010 — Independent tech-discovery coverage gate" · org: arch-research garage · year: 2026
- type: docs · ref: `.claude/workflow/research-scope.md` · title: "Protocol: research-scope" · org: arch-research garage · year: 2026 · surface: adjacent *(transitive source T01)*
- type: docs · ref: `.claude/rules/unimatrix-access.md` · title: "Unimatrix Access Rules (factory agents)" · org: arch-research garage · year: 2026 · surface: adjacent *(transitive source T01)*
- type: dataset · ref: `unimatrix:#312, #316, #317, #318, #319, #320, #321` · title: "wfh-008 knowledge nodes, read-only re-resolution 2026-08-29" · org: arch-research garage · year: 2026 *(transitive source T02)*
