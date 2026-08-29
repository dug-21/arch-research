# wfh-011 · W2 — Software-case instantiation: `vnc-045` as Organizational Data Model V5

**Run:** `wfh-011` · theme `workflow-harness` · research-scope, **DIRECTIONAL** · phase `tech-discovery` · [Issue #70](https://github.com/dug-21/arch-research/issues/70)
**Workstream:** W2 — independent encoding of the Unimatrix `vnc-045` software delivery as V5 instances
**Agent:** `factory-researcher` · read-only · **zero Unimatrix writes, zero grade movement, no `proven`**
**Date:** 2026-08-29

> **Structure only.** Nothing here advances a status, creates a technology node, or recommends a build.
> W2 did not edit `organizational-data-model-v5.yaml` or any other M-alphabet file, and wrote nothing
> into `dug-21/unimatrix`. No network research and no material compute were used: every measurement
> below is a deterministic parse or a read-only inspection of the pinned local corpus.

---

## 1. Model verification (do not take this on trust — the commands are below)

`M01` was re-hashed before it was consumed, and parsed **as-is**. No quoting, normalising, in-memory
patching, or importing of M02's intended prose was applied at any point.

```
$ sha256sum product/factory/proposals/organizational-data-model-v5.yaml
bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060  product/factory/proposals/organizational-data-model-v5.yaml
```

**MATCHES the pin** recorded in the SCOPE's Premise-Recheck extension. Tooling: PyYAML 6.0.3, yq v4.44.3.

The six scalars that S1 reported split are complete at this digest — verified by an independent PyYAML
read, not by reading the file:

```
$ python3 -c "import yaml; m=yaml.safe_load(open('.../organizational-data-model-v5.yaml')); ..."
core 7 supporting 8 registries 6 catalogs 3 invariants 19 event_types 9
autonomy A0 = 'analyze, evaluate or recommend without discretionary work initiation'
autonomy A3 = 'adapt local tactics, composition or reversible method detail'
autonomy A5 = 'change Collective policy, authority structures or strategic objectives'
effect_disposition.def = 'EffectBoundary performs, refuses or cannot determine a request'
adaptation.def = 'authorized change to a definition, baseline, composition or method'
resume_requirements.def = 'baseline, preconditions, unresolved residue and next admissible transition'
```

**S1 is CLOSED at this digest.** W2 consumed the parsed values, and every clause that S1 said was lost
turned out to matter: A0's non-initiating clause is what places the validators and `uni-zero`;
`resume_requirements`' four clauses are what carry the Gate-3a rework; and `effect_disposition`'s
refusal clause is what makes the absence of any refusal in this case visible rather than silent.

---

## 2. Outputs

| Artifact | Path |
|---|---|
| Findings (this file) | `/workspaces/arch-research/product/research/wfh-011/findings-W2-software-instance.md` |
| Historical instance | `/workspaces/arch-research/product/research/wfh-011/artifacts/vnc-045-instance.yaml` |
| Coverage matrix (679 X rows) | `/workspaces/arch-research/product/research/wfh-011/artifacts/vnc-045-coverage.csv` |
| Counterfactuals (separate, `counterfactual` provenance) | `/workspaces/arch-research/product/research/wfh-011/artifacts/vnc-045-counterfactual-instance.yaml` |

The historical instance and the counterfactual file share **no identifiers**: historical entities are
`SC-/GO-/CP-/AC-/UN-/WF-/SK-/RO-/DL-/GT-/EB-/AT-/TE-/EV-/RC-`, counterfactual entities are `CF-*`, each
with an explicit `replaces:` source-link. No counterfactual is counted as observed coverage.

---

## 3. Reproduction — commands and raw output

Every load-bearing measurement in this file is one of these. `$UNI` =
`/tmp/claude-1000/-workspaces-arch-research/wfh-011-sources/unimatrix`, `$GH` = `.../wfh-011-sources/github`.

```
# C3 — squash-merge: the merge commit has ONE parent
$ git -C $UNI rev-list --parents -n 1 37c7b09a
37c7b09aa0db6ba16f5f95dadd24c58adb4e6e2b 9927de027184c6fa03f21b3f31abeb6967e1793f

# C4 — vnc-045 artefact count at the merge commit
$ git -C $UNI ls-tree -r --name-only 37c7b09a product/features/vnc-045/ | wc -l
43

# C5 — the Gate 3c report is ABSENT, against an established repository norm
$ git -C $UNI ls-tree --name-only 37c7b09a product/features/vnc-045/reports/
product/features/vnc-045/reports/gate-3a-report.md
product/features/vnc-045/reports/gate-3b-report.md
$ # over all 226 feature directories at 37c7b09a:
feature dirs: 226 | with gate-3a: 154 | gate-3b: 157 | gate-3c: 153
features with 3a AND 3b but NOT 3c: 1 ['vnc-045']

# C6 — the gate-3b report's open WARN was already fixed 24 minutes before the report was committed
$ git -C $UNI log --format='%h %ad %s' --date=iso -1 843d0049
843d0049 2026-07-07 03:50:17 +0000 chore(vnc-045): drop stale dead_code allow on ServiceLayer.store_tag (#928)
$ git -C $UNI log --format='%h %ad %s' --date=iso -1 bf7c4812
bf7c4812 2026-07-07 04:14:05 +0000 test(vnc-045): context_tag integration suites + risk coverage report + gate reports (#928)

# C7 — the governed activity did not edit its governing definition (I18)
$ git -C $UNI diff --name-only 9927de02 08a45c53 | grep -c '^\.claude/'
0

# C8 — the authored tool counts are wrong; the diff is not
$ git -C $UNI diff 9927de02 08a45c53 -- product/test/infra-001/suites/test_protocol.py | grep -E '^[-+]def test_list_tools'
-def test_list_tools_returns_fourteen(server):
+def test_list_tools_returns_fifteen(server):

# C9 — merge/issue-close lag; the forge records no approval and no inline review comment
merged_at 2026-07-07T11:29:07Z   issue closed_at 2026-07-07T11:29:09Z
unimatrix-pr-929-review-comments.json size = 2 bytes  (literally `[]`)
reviews: [('dug-21', 'COMMENTED')]
issue labels: ['enhancement', 'vinculum', 'goal:knowledge-integrity']

# C10 — every PR-head commit is authored and committed by one identity
$ git -C $UNI log --format='%h %an <%ae> | %cn' -11 08a45c53
  (all eleven: Doug <doug@sunstoneconsultingllc.com> | Doug)
$ git -C $UNI log -1 --format='A:%an <%ae>%nC:%cn <%ce>' 37c7b09a
A:dug-21 <angryweed@gmail.com>
C:GitHub <noreply@github.com>
```

The coverage CSV is regenerated deterministically by
`scratchpad/w2/enumerate_x.py` (which refuses to run on a digest mismatch) plus
`scratchpad/w2/build_coverage.py`. Both are reproduced verbatim in §11.

---

## 4. Source ledger

Every M and S item closes as `used`, `inspected-no-material-instance`, or `unavailable`.

### M — model and review

| id | Disposition | Note |
|---|---|---|
| `M01` `organizational-data-model-v5.yaml` | **used** | Digest re-verified; parsed as-is; 679 X items enumerated from it. |
| `M02` `codex-organizational-data-model-v4-review.md` | **used** | R1–R5/A1–A10 and S1–S8 consumed as coverage rows; §7's traversal obligation discharged in §7 below. Digest `aaecaf77…4249be` re-verified. |
| `M03` `wfh-010/SCOPE.md` | **inspected-no-material-instance** | Read for the falsified H1 and the "no successor model" boundary. Supplies no `vnc-045` instance value. |
| `M04` `wfh-010/findings-W1..W4` | **inspected-no-material-instance** | Read for the standing evidence limits (missing telemetry, raw test logs, generic stop/resume, common effect refusal). W2 preserved all four as missing rather than reconstructing them. |
| `M05` `wfh-010/reports/gate-coverage{,-r2}.md` | **inspected-no-material-instance** | Read for the coverage-audit shape this run's CSV must satisfy. |
| `M06` `themes.md` `theme:workflow-harness` | **used** | The load-bearing boundary ("operations ≠ knowledge"; "keep consequential governance and effect credentials outside the governed activity") is the lens under which EB-01/EB-02 were separated and under which no Jurati architecture or common enforcement point was inferred. |

### S — `vnc-045` case

| id | Disposition | Note |
|---|---|---|
| `S01` Issue #928 (+comments) | **used** | Body, 4 comments, labels, state, closed_at. Sources CP-01/CP-02, AR-01/AR-02, EV-01/EV-05 bounds. |
| `S02` PR #929 (+reviews, review-comments, issue-comments, commits, files) | **used** | Sources EB-01, EV-20/21/22/23, AT-12, AR-03, and the 57-file surface. **The review-comments file is the two bytes `[]` — there were no inline review comments. Recorded as an observed fact.** |
| `S03` the six `vnc-045` root documents | **used** | SCOPE, IMPLEMENTATION-BRIEF, ACCEPTANCE-MAP, ALIGNMENT-REPORT, RISK-TEST-STRATEGY, SCOPE-RISK-ASSESSMENT — all read in full. |
| `S04` `specification/**`, `architecture/**`, `pseudocode/**`, `test-plan/**` | **used** | SPECIFICATION and ARCHITECTURE read in full; ADR-008/009 read in full; ADR-001–007 headers and DEFERRED banners read. Pseudocode/test-plan consumed through the Gate 3a report and the agent reports (they are Records in the instance, not sources of new fields). |
| `S05` `agents/**` and `reports/**` | **used** | All 12 agent reports and both gate reports read in full. This is where the superseded-record finding lives. |
| `S06` implementation/test files per PR #929 and `a63d45f0`, `74bc1fd4`, `b68c2c43`, `bf7c4812`, `37c7b09a` | **used** | Consumed as the PR file list, the per-commit ordering on the **PR-head ref**, and the `843d0049`/`test_protocol.py` diffs. Source contents were not otherwise reviewed — W2 encodes organization, not code. |

### T — transitive sources (added before use, per the SCOPE's fixed-alphabet clause)

| id | Path @ `37c7b09a` | sha256 | Reason | Provenance |
|---|---|---|---|---|
| `T01` | `.claude/protocols/uni/uni-delivery-protocol.md` | `0975e4aa0ec34cf2bc7af055791c7fd8146f4fbae1900c4de2ccc904c667309b` | The **governing Workflow definition** for Stages 3a/3b/3c and Gates 3a/3b/3c. Without it, `Workflow` and `Gate` — the constructs whose promotion and identity are OPEN items under test — have no `method_statement`, `state_vocabulary`, `dependency_rules`, `allowed_outcomes`, `outcome_consequences`, `requires_assessor` or `independence_predicate` in this case, and the whole supporting layer collapses to `missing-history`. | `dug-21/unimatrix` at the pinned commit; referenced obliquely by S05 ("swarm fmt-churn rule", "Stage 3a/3b/3c", "max 2 rework iterations") but not enumerated in S03–S06. |
| `T02` | `.claude/protocols/uni/uni-design-protocol.md` | `5758bfa3fe8d17118b689c430c92e00cceac6163ac00386811e0999cd51523b5` | The governing Workflow definition for Session 1, its two human approval points, and — directly required by W2's preservation obligation — the prescribed **"Handling human-requested changes"** path by which the human scope reduction was executed. | as above |
| `T03` | `git ls-tree -r 37c7b09a product/features/**` (derived measurement, not a document) | n/a — reproduced by C5 | Establishes that `reports/gate-3c-report.md` is the repository norm (153 of 226 feature directories), so vnc-045's missing report is an **observation**, not an inference. | mechanical, over the pinned commit |

No other source was consulted. `product/PRODUCT-VISION.md` was deliberately **not** added: Goal
`success_criteria` and `claim_floor` stay `missing-history` rather than being partially reconstructed
from a document the alphabet does not name.

---

## 5. Coverage result

679 X items enumerated from `M01`; every one has exactly one disposition; no field is silently blank.

| Disposition | Rows |
|---|---:|
| `exercised` | 596 |
| `construct-pressure` | 47 |
| `not-applicable` (with reason) | 36 |
| `blocked-by-OPEN` | 0 |

**No X row was `blocked-by-OPEN`.** Every OPEN item in `M01` was either exercised (often adversely) or
recorded `not-exercised` with a reason; none prevented the instance from being written. That is a
directional point in V5's favour and it should not be over-read: it means the OPEN items are honest
about being unresolved, not that they are harmless.

| `open_pressure_disposition` | Rows |
|---|---:|
| `still-open` | 40 |
| `not-exercised` | 32 |
| `blocking-hole` | 3 |
| `resolved-by-instance` | 2 (`open.workflow_promotion`, `supporting.Workflow.status`) |
| `resolved-by-instance-at-document-altitude` | 1 (`core.Unit.open[0]` interruption and resume) |
| `model-pressure` | 1 (`core.Capability.fields.grade`) |

**Pressure classification tally** — 66 rows carry at least one cause; multi-cause rows retain every
applicable cause:

| Cause | Rows |
|---|---:|
| `historical-evidence-gap` | 43 |
| `project-evolution-candidate` | 20 (→ **5 distinct candidates**, CF-01…CF-05) |
| `enforcement-gap` | 19 |
| `model-defect` | 9 (→ **6 distinct defects**, F-01, F-08…F-12) |
| `unresolved` | 0 |

`project-evolution-candidate` is **never** used as a residual bucket: only 20 of the 66 pressure rows
carry it, and every one of the 20 names one of five candidates with all five required analyses present
(verified programmatically — zero rows are missing an analysis field).

---

## 6. Findings

Ordered by weight. Each states its evidence altitude explicitly.

### F-01 — `evidence_grade` is closed against a vocabulary the program has already ruled on  ·  `model-defect`

`values.evidence_grade` is `status: RESOLVED` with `values: [missing, claimed, partial, proven]`, no
registry, no `extension_owner` and no admission rule. The observed program's set is
`{proven, partial, missing, asserted}` (S03 `SCOPE-RISK-ASSESSMENT` SR-10, quoting
`uni-capability/SKILL.md`), and it did not arrive there by accident: the OQ-1 ruling in S01 comment
`4898695344` reads *"`asserted` is authoritative — confirmed against the vocabulary owner … `claimed` in
#928 is a slip. Use `asserted`."* V5 closes the vocabulary on the exact term the program rejected.

`CP-02` (SLN1 #5528) therefore has **no conforming value for a required field**. Writing `claimed` would
be silent normalisation of a decision in the record; the instance records `UNREPRESENTABLE` with the
observed value beside it.

This is a model defect and not a project problem. `principles.program_ownership` says *"Programs own
Workflows, proof bars, Record Categories and domain extensions"* — and the grade vocabulary **is** the
proof bar's vocabulary — while `principles.extend_by_registration` says variation "normally enters
through a registry or catalog". `evidence_grade` offers neither. The obvious project change (rename
`asserted` → `claimed`) is **circular** and is recorded as rejected candidate `CF-R01`: its only
justification would be conformity to the model under test, and it would erase an evidenced ruling.
*Evidence altitude: doc-claim (the vocabulary), demonstrated (V5's closure — parsed).*

### F-02 — Gate 3c was claimed passed with no assessment record  ·  `enforcement-gap` + `historical-evidence-gap` (+ `project-evolution-candidate` CF-05)

`product/features/vnc-045/reports/gate-3c-report.md` **does not exist** at `37c7b09a`. Of the 226 feature
directories in the tree at that commit, 154 carry `gate-3a-report.md`, 157 carry `gate-3b-report.md` and
153 carry `gate-3c-report.md` — and **vnc-045 is the only feature in the repository carrying 3a and 3b
but not 3c** (C5). T01 defines Gate 3c as a mandatory validator-assessed gate with that exact output
path. The claim "Gate 3c PASS" appears in the PR #929 body and in the security review's merge-readiness
line. The only Stage-3c record is `RISK-COVERAGE-REPORT.md`, authored by `vnc-045-agent-6-tester` — the
actor that wrote and ran the tests under assessment.

Under V5 the consequence is precise and typed: the `assessment` Event is **not writable** (`assessor_refs`
and `independence_check` have no admissible value), so no conforming `gate_outcome` Event exists, and
`Record.admitted_by` for the risk-coverage report is empty. `I8` — *"missing evidence is explicit and
never inferred as success"* — is exactly the rule the merged record breaks, and `I7`'s fail-closed
behaviour had nothing to enforce it.

**This is the strongest pro-V5 result in the software case.** V5 does not merely represent the history;
it makes a claim that the history does not support visible as a missing required Record. W2 does **not**
claim the gate did not run — only that the fixed alphabet does not evidence it, and that nothing in the
project would have noticed either way. *Evidence altitude: demonstrated (file absence and sibling
distribution, both mechanically reproducible).*

### F-03 — Deterministic test reports are actor accounts, and the case proves the distinction is not academic  ·  `historical-evidence-gap` (+ CF-04)

`RISK-COVERAGE-REPORT.md` asserts 6961 unit tests passed / 0 failed, integration smoke 32/32, protocol
14, security 23, and per-risk PASS for R-01…R-08. **None of that runner output survives anywhere in the
alphabet.** Under `I4` and the `observation` event type's `required_extension`, `capture_custody` and
`raw_evidence_ref` are both absent, so `EV-26` carries `epistemic_kind: reported-observation` and the
Record lists three unretained artefacts under `missing_or_unavailable_refs`.

The distinction is not academic here, and the case supplies its own proof. The report states the tool
guard moved **"12 → 15"**; the PR body calls `context_tag` **"the 13th tool"**; the committed diff of
`test_protocol.py` renames `test_list_tools_returns_fourteen` → `_fifteen`, i.e. **14 → 15** (C8). Three
authored numbers, one observable fact, and both authored records are wrong. Nobody caught it because
there was nothing to check against. *Evidence altitude: demonstrated (the diff), doc-claim (everything
the report asserts about test outcomes).*

### F-04 — There is no common runtime custody, and V5 says so in typed structure  ·  `enforcement-gap`

`EffectBoundary.enforces` is **empty for every Delegation in the case**. GitHub (`EB-01`) is the only
externally custodied boundary and it authenticates one principal (`dug-21`); it enforces nothing about
which agent, under which grant, produced a change. The `Capability::Write` gate (`EB-02`) fails the
"independently controlled" test for this unit of work outright: it is code the wave agents wrote during
the same Attempts it would be governing. The only refusal-shaped event described anywhere is a
trigger-injected `INSERT` abort inside a test fixture, evidenced solely by an authored report — **not
counted** as an `effect_disposition` witness, per the scope's prohibition.

`values.effect_disposition.refused` therefore has **no witness in this case**, and
`EffectBoundary.can_refuse` — a `required: true` bool whose own definition says *"a boundary that cannot
refuse enforces nothing"* — is recorded `unestablished` for `EB-01` (F-08). `I12`'s reading is the
correct verdict: autonomy is not authority, and nothing in this case demonstrates enforced authority.
V5 states that in a field (`Delegation.enforced_by` = `[]`, rule *"without a boundary authority is
declared only"*) rather than in prose. *Evidence altitude: demonstrated (forge records), doc-claim (the
test-fixture rollback).*

### F-05 — Delegation is the least-evidenced construct in the case  ·  `historical-evidence-gap` + `enforcement-gap`

Every one of the thirteen Delegations in the instance is an **inference**. The fixed alphabet contains
no artefact that states a grant. `autonomy_tier`, `effect_grants`, `escalation_conditions` and
`definition_custodian_ref` are reconstructed from T01/T02 spawn templates and role boundaries;
`resource_ceiling` — `required: true`, type `map` — has **no source at all** and is `unestablished` on
every row. Attenuation (`I17`) holds on the initiative axis (`A0`/`A1` < `A5`) and demonstrably **fails
on the effect axis**: every agent runs under the same OS/git/`gh` credentials as the authority root, so
no derived grant is actually narrower, and nothing detects it.

This is not a V5 defect — V5 names the property that is violated and provides the field
(`derived_from`, rule *"may not exceed parent on any axis"*) that makes the violation statable. It is
also **not** offered as a project-evolution candidate: the credentialed-identity change that would close
it relitigates a settled, human-locked decision (ADR-008: the security posture is human-LOCKED; the
declarative-attribution bound is an accepted residual risk). See rejected candidate `CF-R02`.
*Evidence altitude: inference (the delegations), demonstrated (the shared credential, from commit
authorship).*

### F-06 — The most consequential decision in the case has no primary record  ·  `historical-evidence-gap` (+ CF-03)

The human scope reduction (`EV-05`) voided the feature's only Critical risk, moved six of ten scope risks
out of test obligation, deprecated four ADRs and changed the deliverable. It survives **only** as the
dated phrase *"scope reduced by human 2026-07-07"*, repeated inside seven documents written by the actors
it governed. There is no issue comment, no commit, no forge object. Its `required` `occurred_at` cannot
be supplied at the declared `timestamp` type; only a two-hour window is inferable — after the
design-review comment at `2026-07-07T01:33:14Z`, before commit `afaa8385` at `02:50:37Z` — and that
window is recorded in the instance as an inference, not an observation.

The asymmetry is the finding, and it is the project's, not the model's: vnc-045's own thesis is that an
append-only record is *"the PRIMARY control"*, applied to a single tag mutation at millisecond precision
with prior and new value. The merge decision (`EV-29`) **is** forge-recorded to the second by an external
custodian. The scope decision is not recorded at all. *Evidence altitude: doc-claim (that it happened),
demonstrated (that no forge or git object records it).*

### F-07 — Records at incompatible baselines ship in one commit with no currentness marker  ·  `project-evolution-candidate` CF-01

Three agent reports in the merged tree describe the **pre-reduction** feature and are committed
unchanged, in commit `afaa8385`, beside the reduced sources that contradict them:

- `vnc-045-agent-1-architect-report.md` — *"with per-slug `protected_tags` value-hygiene policy"*,
  ADR-001…008 all delivered, ADR-005 "honor `protected_tags` on ALL THREE construction paths",
  ADR-008 "`min_trust_level` inert seam". Every one of those is DEFERRED at `37c7b09a`.
- `vnc-045-agent-2-spec-report.md` — *"SCOPE.md (14 SDs binding)"*, *"All 9 acceptance criteria
  (AC-01..AC-09)"*, a `protected_tags` config domain model. The committed SPECIFICATION has 12 SDs and
  AC-01…AC-07.
- `vnc-045-vision-guardian-report.md` — *"PASS 6 / WARN 0"* and `min_trust_level` "shipped + tested for
  INERTNESS (R-10, AC-09b)". `ALIGNMENT-REPORT.md`, in the same commit, says PASS 7 and that R-10/AC-09b
  no longer exist.

Add `SCOPE-RISK-ASSESSMENT.md`, whose header still describes the un-reduced feature and whose SR-03/04/
06/08/09/10 are all VOIDED-BY-DEFERRAL in the risk strategy, and the gate-3b report, whose open WARN was
already fixed 24 minutes earlier (C6). Nothing distinguishes any of them from a current record.

`core.Record.fields.currentness` and `Record.supersedes` express all of it exactly — this is a **V5
win**, not a V5 need. The mechanism is also fully explained and not sloppiness: T02's *"Handling
human-requested changes"* regenerates the brief and acceptance map (and the alignment report was re-run),
and says nothing about the agent reports. The project already pays the cost by hand: the
`ALIGNMENT-REPORT` itself records that Unimatrix pattern #5607 *"cites a now-stale clean instance"* and
hands the retro a manual reconciliation. *Evidence altitude: demonstrated (file contents at one commit).*

### F-08 — No `unestablished` member exists for a required typed field  ·  `model-defect` + `historical-evidence-gap`

Three required fields have no honest value in this case: `EffectBoundary.can_refuse` (`bool`),
`Capability.grade` / `Technology.grade` (`ref<value.evidence_grade>`), and `Event.occurred_at`
(`timestamp`). An encoder must either assert a claim or leave the instance non-conforming. This is
notable because V5 *does* carry the idea elsewhere — `values.currentness` has `unknown` and
`values.effect_disposition` has `unknown` — but the type system does not. The instance writes
`unestablished` and flags it; a checker would reject the instance. *Evidence altitude: demonstrated.*

### F-09 — Composite actors have nowhere to go  ·  `model-defect` + `historical-evidence-gap`

Every PR-head commit is authored by `Doug` with a `Co-Authored-By: Claude Opus 4.8` trailer. That is a
composite actor in practice. `Actor` is `versioned: false` with a single `declared_identity`, and
`Attempt.actors` is a flat list, so neither construct distinguishes "acted through" from "acted as".
`core.Actor.open[2]: composite Actors` is exercised adversely rather than left untouched.
*Evidence altitude: demonstrated (commit trailers).*

### F-10 — `Record.author_or_source_ref` is a single text where the case is two-valued  ·  `model-defect` (minor)

Every advisory review is `AC-16 (declared) / dug-21 (forge-attributed)`. GitHub attributes comments
`4898695344`, `4899256125` and `4900099734` to `dug-21`; their bodies declare `uni-zero-reviewer`. V5
offers one text field and no declared/attested distinction — even though `Actor.declared_identity`
draws exactly that line one construct away. *Evidence altitude: demonstrated.*

### F-11 — S4's non-atomicity bites, and it bites in both directions  ·  `model-defect`

Four of the seven invariants M02 S4 flagged as still-unsplit have clauses with **different verdicts** in
this one case:

- **I1** — "opaque identity distinct from name" holds (UN-01/UN-02 under one project name); "history is
  superseded, never overwritten" **fails** (SCOPE.md was overwritten in place; no prior version exists at
  any commit).
- **I15** — "Unit identity survives rework" and "each execution is an Attempt" both hold at the document
  altitude; both are **unverifiable** at the forge altitude (both Gate-3a attempts collapse into
  `3afc2c49`).
- **I18** — "custody sits outside the governed activity" is **demonstrated** (C7: zero `.claude/` files
  in a 57-file PR); "changes are adaptation Events" holds for the ADR deferral and **fails** for
  SCOPE.md, which was edited with no adaptation record of its own.
- **I4** — both clauses hold, but only because F-03's distinction was applied.

Reporting "I1 fails" would be wrong; reporting "I1 passes" would be wrong. A checker could not say which
clause failed. This is the one place where W2's coverage row is `blocking-hole`.
*Evidence altitude: demonstrated.*

### F-12 — `Unit` has no name and no external reference  ·  `model-defect` (minor)

`Scope`, `Capability`, `Workflow`, `Skill`, `Role`, `Gate`, `EffectBoundary` and `Technology` all carry
`name`. `Unit` carries `unit_kind`, `intended_outcome`, `scope_ref`, `current_state`, `baseline_ref` —
and nothing else. The project's own work identifier (`vnc-045`), its tracking artefact (issue #928) and
its branch (`feature/vnc-045`) have nowhere typed to live; the instance had to put them in
`baseline_ref` prose. `I19` forbids moving common semantics into free text, and *"which Unit is issue
#928?"* is the first question an auditor asks. *Evidence altitude: demonstrated (M01 parse).*

### F-13 — Where V5 does unusually well  ·  no pressure

Recorded because a run that only reports defects is not doing its job:

1. **`I16` + `Unit.replaces` capture the human scope reduction precisely.** Changing the intended outcome
   creates a new Unit, and `UN-02 replaces UN-01` is exactly right. The project reused one identifier and
   overwrote three documents in place; V5 represents what happened, not what was labelled.
2. **`I11` and `Technology.enables`' "no grade transfer" are the project's own pre-registered ruling.**
   *"Do NOT mark any capability `proven` off vnc-045"* was stated twice, in advance, by an independent
   reviewer, and honoured at delivery. `Unit.delivers` is empty by observation.
3. **The `assessment` / `gate_outcome` split (M02 R2) pays off immediately.** The Gate-3a iteration-0
   assessment exists with **no** surviving outcome payload. Under v4's merged form that event could not
   have been written at all, and an abandoned gate would be indistinguishable from one that never ran.
4. **`Event.authority_ref: ref<Delegation|Scope>` (M02 R4) is load-bearing.** The merge and the scope
   reduction are the authority *root* acting; pointing at an Actor would have bypassed the root.
5. **`Attempt.resume_requirements`' four clauses are all separately supplied** by the Gate-3a rework:
   baseline, precondition (*"read the gate report first"*), residue (Check 4), next admissible
   transition (re-spawn, max 2 iterations).
6. **`values.coupling` earns `ordered-best-effort` from data**, not from taxonomy: the merge lands at
   `11:29:07Z` and the issue closes at `11:29:09Z` — two effects, one request, two seconds apart.

### F-14 — Advisory review is representable without a vacuous Gate  ·  no pressure

T01/T02 state the product review is *"Advisory — does not block delivery"* and that the leader *"NEVER
parses, acts on, or gates on it."* The instance models `uni-zero`'s three reviews as `communication`
Events documented by `advisory-review` Records, **not** as Gates — because V5's `assessment` event type
requires a `gate_version_ref`, so "is there a Gate?" *is* the blocking/advisory discriminator. That is a
good property, and the non-adoption of the advisory recommendations is the case's clearest live
demonstration of `I6` (outcome, decision and consequence remain distinct): at least two recommendations
are observably not adopted at `37c7b09a` — the requested `goal:integrity` + `goal:self-learning` labels
(the issue carries `[enhancement, vinculum, goal:knowledge-integrity]`, C9), and the request to resolve
the *"audit is the PRIMARY control"* vs fire-and-forget contradiction (ADR-008 point 5 and ADR-009 both
stand unchanged, with the drop accepted in Residual Risk 2). Non-adoption of an advisory review is
**conforming behaviour**, not a defect.

---

## 7. The five preservation obligations

| Obligation | Where it is preserved | Result |
|---|---|---|
| **Human scope reduction** | `UN-01` → `UN-02` via `replaces`; `EV-05` (decision) + `EV-06` (adaptation, with `prior_baseline`/`new_baseline`) | **Preserved and improved.** V5 separates the two Units that the project collapsed into one identifier. The decision Event's `occurred_at` is `missing-history` (F-06). |
| **Deterministic test reports vs raw observations** | `EV-26` (`reported-observation`, `capture_custody: ABSENT`) vs `EV-27` (`mechanical-observation`, GitHub custody); `RC-14.missing_or_unavailable_refs` | **Preserved, and vindicated** by the 14→15 vs "12→15"/"13th tool" contradiction (F-03). |
| **Delegated attempts** | `AT-06`/`AT-07`/`AT-08` on `UN-06`/`UN-07`/`UN-08`, each `governed_by` a dynamic Delegation, in mechanical commit order on the PR-head ref | **Preserved structurally, unevidenced substantively** (F-05). The wave DAG is real and ordered; the grants that governed it are inferences. |
| **Product and security gates** | `GT-07` (security, `READY`, forge review state `COMMENTED`, zero inline comments) and `AR-01`/`AR-02`/`AR-03` (advisory, non-binding) | **Preserved and correctly separated** (F-14). The forge records **no approval** for this PR — only a `COMMENTED` review. |
| **Merge as a bounded forge effect** | `EV-20` request → `EV-21` disposition (`performed`, `atomic`, receipt = `merge_commit_sha` + `GitHub <noreply@github.com>` as committer) → `EV-23` (`performed`, `ordered-best-effort`) | **Preserved, and it is the case's only externally custodied effect receipt.** |
| **Absence of common runtime custody** | `EffectBoundary.enforces = []` on every Delegation; `EB-02` disqualified; `effect_disposition.refused` with no witness | **Preserved as an absence** (F-04). Never converted into a model failure, and no refusal was claimed. |

**Required traversals (M02 §7).** Both discharged with **no new relation added**:
`GO-01 → [WF-01, WF-02]` by index scan over `Workflow.applies_to`; `AC-09 → [AT-08]` by index scan over
`Attempt.actors`. Four further traversals are demonstrated in the instance's `traversal_checks`
(Delegation→Scope root, Delegation→EffectBoundary disposition (empty), Gate→assessment→outcome→Record,
Unit→Attempt→Delegation→Actor).

---

## 8. Project-evolution candidates

Five candidates, each with all five required analyses in
`artifacts/vnc-045-counterfactual-instance.yaml`. **None is a recommendation.** Each independent reason
is stated *without* reference to V5, and each was tested for circularity before being asserted.

| id | Change | Independent reason (not V5) | Post-evolution fit |
|---|---|---|---|
| **CF-01** | Stamp agent/gate reports with the SCOPE digest they were written against; the synthesizer stamps `superseded_by` when it regenerates after a scope change. | The project already pays this by hand: the alignment report records that pattern #5607 cites a now-stale vnc-045 instance and hands the retro a manual reconciliation. | `retain` |
| **CF-02** | Add `reviewed_commit: <sha>` to the gate-report template. | T01 already declares *"Gates check committed HEAD"*; a review that cannot name what it reviewed cannot be re-run — demonstrated by C6. | `retain` |
| **CF-03** | Post one issue comment recording a scope decision at the human gate, before regeneration. | The organisation audits a single tag mutation to the millisecond and left its own most consequential decision unrecorded. Its own thesis argues for it. | `retain` |
| **CF-04** | Retain the runner output (or digest + head/tail) beside the risk-coverage report. | The project treats a summary standing in for a record as a security defect for machine writes (R-03, the `"{}"` sentinel rule); the same standard on its own gate evidence would have caught an error that shipped. | `retain` |
| **CF-05** | Require the gate-3c report as a forge-side branch-protection check (or, weaker, a human pre-merge checklist item). | T01 already declares Gate 3c mandatory with an independent assessor and a fixed output path; 153 of 226 feature directories produce it. The change makes an already-documented, already-normal behaviour non-bypassable. | `retain`, **current-project fit for GT-06 stays `reject`** |

**Two candidates were considered and rejected** rather than asserted:

- `CF-R01` (rename `asserted` → `claimed`) — **circular**: the only justification is V5's preference, and
  it would erase an evidenced ruling. The mismatch is carried as a model defect (F-01) instead.
- `CF-R02` (credentialed per-agent identity) — **relitigates a settled, human-locked decision.** ADR-008
  records the posture as human-LOCKED and the declarative-attribution bound as an accepted residual risk.
  Existing authority and custody semantics are constraints on a counterfactual, not friction to remove.
  Carried as an enforcement gap (F-05) instead.

`CF-05` is the only candidate whose preservation analysis carries a **recorded, unresolved risk**: a
required check whose predicate is "a file exists" is satisfiable by writing a file. It raises the cost of
an unrecorded gate; it does not attest that the assessment happened. Saying otherwise would be exactly
the *"overstating defensive structure"* the project's own standing lesson warns against.

---

## 9. Review / adversarial concerns

**1. Parsed the pinned file, or imported the review's prose?** Parsed the pinned file. Digest re-verified
before consumption (§1); the six S1 scalars were read from the parse, not from the page. M02 was used
only as a source of coverage obligations (S1–S8, R1–R5, the §7 traversal consequence), never as an
overlay on M01.

**2. Does every purported common semantic live in a typed field?** Mostly. The failures are enumerated:
the grade vocabulary (F-01), the declared-vs-attested author split (F-10), the composite actor (F-09),
and the Unit's external identifier (F-12) all end up in prose. The blocking/advisory distinction does
**not** — it is carried by "is there a Gate?" (F-14).

**3. Are the registry extensions genuinely program-owned extensions?** Yes, and the CSV records the
behavioural justification per category. `agent-report` and `test-observation-report` earn existence on
distinct lifecycle and epistemic behaviour, not on labels: the first has no admission rule and no
lifecycle at all, the second is permanently pinned to `reported-observation` because the raw capture is
never retained. No extension weakens an invariant.

**4. Do actor-authored reports remain claims?** Yes, per Record, with `epistemic_kind` set explicitly and
`provenance:` on every row of the instance. The forge/git observations retain their custody. The
14→15 contradiction (F-03) is the demonstration that the distinction was not applied decoratively.

**5. Are retry, rework, interruption, adaptation, baseline, residue and resume separable?** Yes, and the
case separates them: `AT-07`'s self-corrected first-run test failure is a **retry inside one Attempt**
(same baseline); `AT-03`→`AT-04` is **rework across Attempts** (Gate-3a REWORKABLE FAIL);
`EV-06`/`EV-28` are **adaptations** with prior/new baselines; residue and next admissible transition are
carried by `resume_requirements`. The baseline is the discriminator and it works. What is missing is
evidence, not structure: `AT-03.baseline_ref` does not survive.

**6. Can a Delegation be traced to a Scope root and compared with its parent?** Traced: yes (2 hops,
demonstrated). Compared: partially — orderable on the tier axis, **not** on the effect axis (F-05).
Connected to an independent EffectBoundary disposition: **no** — `enforced_by` is empty everywhere, and
that is recorded as the case's answer, not worked around.

**7. Do gate assessment, outcome, decision, transition, effect request/disposition and Record remain
distinct and traversable?** Yes. `GT-05 → EV-11 → EV-12 → RC-09` is demonstrated. `transition` is the
weakest: T01's `context_cycle` rows live outside the alphabet, so every transition Event here is an
inference from the protocol.

**8. Do the one-way traversals work without method-biased inverses or silent global scans?** Yes — both
are index scans over a declared one-way relation, which is exactly the disposition M02 §7 adopted when
A3 was withdrawn. No relation was added.

**9. Were OPEN items exercised and honestly retained?** 40 `still-open`, 32 `not-exercised` with reasons,
3 `blocking-hole`, 3 resolved-ish (two of them `workflow_promotion`, affirmatively). **`autonomy_A3_A4`
is retained as insufficient-evidence: neither A3 nor A4 has a witness in this case, and no default was
invented.** Empty seeded registries received no invented canonical values — `record_category`,
`unit_kind` and `effect_class` were populated as *instance-level program extensions*, declared as such.

**10. Did the run record absent enforcement as absence?** Yes, 19 rows classified `enforcement-gap`, and
missing enforcement was never converted into model failure. F-02 and F-04 are the two places this
mattered most, and both are stated as absence.

**11. `lesson_vs_pattern`.** `not-exercised` and deliberately so: the software case produces patterns
(#5612, #5613) and no lesson-learned, and neither node's content is inside the alphabet, so no
behavioural distinction is observable. This OPEN belongs to W1's research case.

**12. Is the verdict limited?** Yes. One owner-operated software history, one program, one workflow
family, read-only, directional. It proves nothing about generality, runtime enforcement, portability, or
semantic compression outside this case.

**13. Circular conformance?** Tested explicitly on every candidate; two were rejected for it or for
relitigating a settled decision (§8). No candidate's independent reason mentions V5.

**14. Behaviour erasure?** No candidate deletes a domain distinction, exception path, proof obligation or
safe-interruption behaviour. All five are additive (metadata, a comment, a retained artefact, a check).

**15. Authority laundering?** Checked per candidate. CF-05 moves enforcement **away** from the governed
actors onto an externally custodied boundary — the safe direction. CF-03 moves the narration of a
decision away from the actors it governed. None moves method custody, decision authority, credentials,
gate inputs or effect performance toward the governed actor.

**16. Counterfactual confusion?** Separate file, separate `CF-` identifiers, explicit
`provenance: counterfactual`, explicit `replaces:` source-links, and `encodes_counterfactual: false` on
the historical instance. No proposed event appears as observed fact.

**17. Migration realism?** Every candidate states cost, affected surfaces, and what it does **not**
recover. CF-05 is explicitly the expensive one (repository-admin configuration, changes the merge path
for all features, needs an exemption path) and carries a recorded residual risk.

**18. Cause discrimination?** 43 `historical-evidence-gap`, 19 `enforcement-gap`, 9 `model-defect`,
20 `project-evolution-candidate`, 0 `unresolved`. Multi-cause rows retain every cause. F-02 alone carries
three.

---

## 10. What W2 could not verify — flags

- **Nothing contradicts a load-bearing premise of the SCOPE.** The M01 digest matches the pin; S1 is
  closed at that digest; the squash-merge property, the 43-file count and the PR-head commit ordering
  reproduce exactly as the leader recorded them. **One correction to a number the leader supplied via
  the corpus, not the scope:** a naive grep suggests ~185 sibling `gate-3c` artefacts; the precise
  measurement over `reports/` paths is **153 of 226 feature directories**, and the sharper fact is that
  **vnc-045 is the only feature with a 3a and a 3b report but no 3c report.**
- **Whether Gate 3c ran at all is unresolvable** from the fixed alphabet, and no project change settles
  it retrospectively (F-02, CF-05 `unresolved_discriminator`).
- **Every Delegation is an inference.** Treat the whole `delegations:` block as reconstruction.
- **Every capability grade is a doc-claim.** CP-01's `proven` is uni-zero's assertion; the Unimatrix
  nodes and their `proven_by` sets are outside the alphabet.
- **All test outcomes are doc-claims.** No raw runner output exists; one authored count is demonstrably
  wrong.
- **T01/T02 are living, unversioned files.** Their content at `37c7b09a` is what W2 read. If the
  protocol changed between the vnc-045 run (2026-07-07) and the pinned commit, the Workflow instance is
  anachronistic; nothing in the alphabet dates the protocol's revisions. **This is the single largest
  soft spot in W2's encoding** and W4 should weigh it.
- **`refused` and `unknown` effect dispositions have no witness.** No refusal was claimed anywhere.
- **W2 did not read the implementation source.** `S06` was consumed as file lists, commit ordering and
  two targeted diffs. W2 encodes organization, not code, and makes no claim about whether `context_tag`
  works.

---

## 11. Reproduction scripts

Both are read-only and deterministic. `enumerate_x.py` **refuses to run on a digest mismatch**.

- `vnc-045-coverage-enumerate-x.py` — re-hashes M01, aborts unless the digest is
  `bf8e5536…9841060`, then emits one `<class>\t<model_path>` line per X item (679 lines).
- `vnc-045-coverage-build.py` — re-runs the enumerator, joins an authored disposition table (prefix defaults
  plus ~120 explicit overrides), fills every non-applicable field with `not-applicable`, and writes
  `artifacts/vnc-045-coverage.csv`. It prints the tallies quoted in §5 and asserts zero invalid
  dispositions and zero silent blanks.

Both are committed beside the CSV so W3, W4 and the coverage auditor can re-derive it:

```
product/research/wfh-011/artifacts/vnc-045-coverage-enumerate-x.py
    # 679 X items from core/supporting/registries/catalogs/values/invariants/
    # excluded/open/changelog + M02 S1-S8 + the 2 required traversals

product/research/wfh-011/artifacts/vnc-045-coverage-build.py
    # -> product/research/wfh-011/artifacts/vnc-045-coverage.csv

$ python3 product/research/wfh-011/artifacts/vnc-045-coverage-build.py
rows: 679
dispositions: {'exercised': 596, 'construct-pressure': 47, 'not-applicable': 36}
cause classifications (rows may carry several): {'model-defect': 9, 'historical-evidence-gap': 43,
                                                 'enforcement-gap': 19, 'project-evolution-candidate': 20}
rows carrying >=1 cause classification: 66
project-evolution-candidate rows: 20
rows with invalid disposition: 0
rows with a silent blank field: 0
```

Self-check applied to W2's own artifacts (the S1 lesson, turned on the author): both YAML files parse
under PyYAML 6.0.3, and a scalar-integrity scan for comma-split flow-mapping keys returns only the six
intentional multi-word gate-outcome keys (`REWORKABLE FAIL`, `SCOPE FAIL`).

---

## 12. Citations

All sources are structured with provenance. Keys that could not be established are omitted, never guessed.

- `{type: repo, ref: "product/factory/proposals/organizational-data-model-v5.yaml", title: "Organizational Data Model V5 (sha256 bf8e5536…9841060)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/factory/proposals/codex-organizational-data-model-v4-review.md", title: "Review — codex-organizational-data-model-v4.yaml, with V5 sanity findings S1–S8 (sha256 aaecaf77…4249be)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/SCOPE.md", title: "wfh-011 — Organizational data-model instantiation and rejection test", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/factory/themes.md", title: "Standing research themes — theme:workflow-harness", org: "arch-research garage", year: 2026}`
- `{type: repo, ref: "dug-21/unimatrix@37c7b09aa0db6ba16f5f95dadd24c58adb4e6e2b", title: "[vnc-045] context_tag — in-place tag-mutate MCP op (mechanism)", org: "dug-21", year: 2026}`
- `{type: repo, ref: "https://github.com/dug-21/unimatrix/issues/928", title: "vnc-045: context_tag — in-place tag mutation (mechanism only; protected_tags deferred)", org: "dug-21", year: 2026}`
- `{type: repo, ref: "https://github.com/dug-21/unimatrix/pull/929", title: "PR #929 — context_tag, 11 commits, 57 files, squash-merged", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:product/features/vnc-045/SCOPE.md", title: "vnc-045 SCOPE — context_tag mechanism only, scope reduced by human 2026-07-07", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:product/features/vnc-045/architecture/ADR-008-authorization-posture-and-seams.md", title: "ADR-008 — Capability::Write gate IS the trust seam; agent_id audit-only", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:product/features/vnc-045/architecture/ADR-009-audit-event-contract.md", title: "ADR-009 — the complete generic context_tag audit-event shape is a retrofit-hard contract", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:product/features/vnc-045/testing/RISK-COVERAGE-REPORT.md", title: "vnc-045 Risk Coverage Report (Stage 3c)", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:product/features/vnc-045/reports/gate-3b-report.md", title: "Gate 3b Report: vnc-045", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:.claude/protocols/uni/uni-delivery-protocol.md", title: "Delivery Session Protocol (Session 2) (sha256 0975e4aa…67309b) [T01]", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:.claude/protocols/uni/uni-design-protocol.md", title: "Design Session Protocol (Session 1) (sha256 5758bfa3…1523b5) [T02]", org: "dug-21", year: 2026}`
- `{type: docs, ref: ".claude/rules/unimatrix-access.md", title: "Unimatrix Access Rules (factory agents) — recorded attribution is persisted self-assertion, not attestation", org: "arch-research garage", year: 2026}`

---

**Status: W2 complete.** Directional, structure-only. No Unimatrix write, no grade movement, no `proven`,
no model edit, no successor schema, no build recommendation. The seven-entity verdict is W4's to issue,
not W2's.
