# wfh-011 — REPORT: directional position

**Run:** `wfh-011` · **Theme:** `workflow-harness` · **Issue:** [#70](https://github.com/dug-21/arch-research/issues/70)
**Confidence-required:** directional · research-scope · **structure-only**
**Phase:** `synthesis` · **`feasibility` SKIPPED** (no POC, no compute spend)
**Method stamp:** `wf-v0.26-11-gaaa64b2` (set-once at cycle INIT; recorded in the SCOPE's human-resume extension)
**Synthesized at:** `main` @ `1663c65` · **Author:** `factory-curator` · 2026-08-29
**Coverage gate:** `PASS`, round 2 of at most 2 — `reports/gate-coverage-r2.md`, independent `factory-validator`

**Model under test (pinned, unmoved):**
`product/factory/proposals/organizational-data-model-v5.yaml`
sha256 `bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060` — re-hashed by this
synthesis at `1663c65`; matches the SCOPE pin and every workstream's independent verification.

---

## 0. What this report is, and what it is not

This is the directional position for a run that tested a **published model by consuming it**, not a
proposal for a new one.

**This run performed zero Unimatrix writes.** No node, no edge, no tag, no lifecycle move, no grade
movement, no `technology`, no `finding`, no `position` node, no capability advancement. The SCOPE
forbids graph writes and grade movement explicitly; both independent coverage audits recommended
grade movement **NONE**; and the curator's pen was closed for this run by owner instruction. Nothing
in this report may be read as having earned a grade. Under the firewall, nothing here is `proven` —
there is no attached, demonstrated-by-us artifact at any claim's altitude, and none is claimed.

**No successor model was authored and none may be inferred from this report.** There is no V6, no
replacement schema, no sketch of one, no normative default for any OPEN item, and no build
recommendation. Where this report names a defect it names the defect; it does not name the fix.

**Every mechanical result below is a property of a checker some workstream wrote from a YAML file
this week.** `M01.meta.enforcement_reality` states that no common cross-program checker implements
this model, and that is still true. No historical project ever refused anything on V5's account.

**Numbers in this report were measured by the curator from the artifacts**, not carried over from
prose about the artifacts. Where a workstream's stated count and an auditor's measurement disagree,
both are reported and attributed (§5.5, §5.6, §5.7).

---

## 1. The directional position

> **V5 can carry both histories, and it cannot yet carry the parts of them that matter most.**
>
> Two independently encoded owner-operated histories — a research run (`wfh-008`) and a software
> delivery (`vnc-045`) — instantiate into the pinned seven-entity model without a single
> domain-specific common construct and without an eighth core entity, using only program-owned
> registered extensions. That is the compression hypothesis surviving its first contact with real
> data, and it is a real result. But the structural layer is where V5 holds. **The layer the theme
> calls load-bearing — authority, custody, evidence grade, effect refusal, interruption and proof —
> is where V5 states rules it cannot bind to its own typed data.** A checker generated from the model
> alone admits 18 of 115 adversarial fixtures, and nine of those eighteen are rules whose *both
> operands are already typed* and which the model simply never writes the sentence to join. The
> hypothesis is therefore **revised, not rejected**: nothing in either case demands a new entity;
> what is missing is bindings, an extension point on a closed vocabulary, and members of enums that
> cannot say "unestablished".
>
> The run's sharpest single result is that **`current-project fit` and `post-bounded-evolution fit`
> are identical (`revise` / `revise`)**. Twelve bounded project-evolution counterfactuals were
> constructed and independently challenged; **not one repairs a model defect.** There is no better
> post-evolution verdict, and therefore nothing for one to conceal.
>
> This holds for two owner-operated histories inside one organisation, read-only, at directional
> altitude. It establishes nothing about generality, runtime enforcement, organizational
> effectiveness, a product boundary, or semantic compression outside these two cases.

---

## 2. The verdict, and the findings that carry it

### 2.1 The required verdicts, side by side

W4 (independent cross-case adjudication; authored none of W1–W3) returned, and the rework did **not**
move:

| Verdict | Ruling |
|---|---|
| Seven-entity hypothesis — `retain \| revise \| reject` | **`revise`** |
| **`current-project fit`** (the projects as they actually existed) | **`revise`** |
| **`post-bounded-evolution fit`** (bounded counterfactuals, after challenge) | **`revise`** |

The round-2 auditor verified the `findings-W4-adjudication.md` §8 verdict block **byte-identical**
(`24c38d55…f425e18`) across the whole rework range. The verdict was not moved by the correction that
reduced the run's own claimed coverage by 30 rows.

### 2.2 Applied to the SCOPE's literal bar

| Bar clause | Result | Evidence |
|---|---|---|
| Both cases instantiate **without a domain-specific common construct** | **MET** | W1: **191 objects across 14 of 15 constructs**, 0 errors, four program-owned registry extensions. W2: **151 objects across all 15 constructs**, five extensions. Neither case added a common construct. |
| **Every material semantic** fits typed structure or a conforming registered extension | **NOT MET** | `values.evidence_grade` is `status: RESOLVED`, closed at `[missing, claimed, partial, proven]`, with **no registry, no `extension_owner`, no admission rule** — while the observed program's own vocabulary is `{proven, partial, missing, asserted}`. Plus: no `unestablished` member for three required typed fields; `Gate.procedure` admits no mixed value; `Attempt.disposition` admits no interruption; `Unit` has no name and no external reference. |
| No authority / custody / evidence / effect / interruption / proof distinction **weakens** | **MET in the model, UNWITNESSED in the cases** | No distinction weakens. Several are unenforceable. Missing enforcement is reported as missing enforcement (§3d), never converted into model failure. |
| **Reject** limb 1 — a case behaviour needs an **eighth common core entity** | **NOT MET** | No such row exists in 679 reconciled X rows or 115 executed fixtures. |
| **Reject** limb 2 — a core entity **collapses independently behaving concepts** | **NOT MET** | The nearest candidates (`Actor` identity; `Event`'s nine behaviourally distinct types over one untyped `extension`) resolve to field and binding changes *within* the construct. |

Retain fails on clause 2. Reject fails on both limbs. **`revise`.**

### 2.3 The four findings that carry the verdict

**(1) The grade vocabulary has no conforming home — the single strongest `model-defect`.**
`values.evidence_grade` closes on four values with no extension point, while the observed program
records `asserted` as a real grade — read at source in `dug-21/unimatrix@37c7b09a`
`SCOPE-RISK-ASSESSMENT.md` SR-10, and confirmed deliberate by Issue #928 comment `4898695344`
(SLN1/#5528 recorded `curve/nfr, asserted`; the OQ-1 ruling names `claimed` a slip). The consequence
lands in the instance: `CP-02.grade` is `UNREPRESENTABLE` — a **required** field of a **core** entity
with no conforming value for a real case value. `principles.program_ownership` says programs own
proof bars; `principles.extend_by_registration` routes variation through registries; `evidence_grade`
offers neither. **Both cases independently identified the obvious project fix (rename `asserted` →
`claimed`) and rejected it as circular**, and W4 added the sharper reason: the rename would erase an
evidenced ruling, which the amendment forbids independently of circularity. This is a model defect,
not a project problem — the discrimination concern 18 exists to force.

**(2) The firewall is stated twice and bound nowhere.** W3's suite, generated from `M01` alone,
executed 115 fixtures. Curator-verified from `artifacts/rejection-results.csv`:

| actual result | count |
|---|---:|
| `rejected-mechanically` | **82** |
| `accepted-defect` (adverse) | **18** |
| `not-falsifiable-from-alphabet` | **9** |
| `specified-not-enforced` | **5** |
| negative test (must not reject; passed) | **1** |

Cross-tabulated against the kind of check that *could* reject at all (**89 mechanical · 26
judgment**), the finding is the **9 mechanical × accepted-defect** cell. A judgment rule a checker
cannot reach is unremarkable; a rule whose both operands are already typed and still cannot be
checked is a missing binding. The concentration is not random — it is the Event layer and the
firewall running through it:

- `F-E12` accepts `Capability.grade: proven` with `evidence_record_refs` **deleted**. I9 and
  `evidence_grade.rule` state the garage's own D7 firewall and **no typed structure carries it**:
  `evidence_record_refs` is `required: false` and no rule makes it conditional on `grade`.
- `F-E13` accepts `proven` on a behavioural claim citing only a `directional` Record — `Record`
  declares `evidence_altitude`, `Capability` and `Technology` declare none, so I9's altitude
  comparison has only one typed side.
- `F-E17` / `F-E18` accept a `credential-issue` request under a Delegation granting only
  `repository-write`, and a request aimed at a boundary whose `effect_classes` exclude it — though
  `effect_grants` and `requested_effect` are **both** registry-typed. This is the one authority check
  that could have been fully mechanical from typed data on both sides.
- `F-E19` accepts `can_refuse: false` on the boundary two Delegations name as their enforcement — a
  field whose own definition reads *"a boundary that cannot refuse enforces nothing"* and which **no
  rule in M01 reads**.
- `F-E26` accepts an **A5** Delegation derived from an **A1** parent. `autonomy_tier` has **no
  declared order**, and A5 is `held_by: human`. That is the theme's own stated boundary — keep
  consequential authority outside the agents being governed — unenforced.

**(3) `Capability` has no fully conforming witness anywhere in the run.** W1 instantiated **zero**
(the case's stated capability target is a proposed id with no `observable_behavior` and no
`done_when`; inventing them is the circular force-fitting the amendment prohibits, and it was
refused — recorded as a rejected candidate, not proposed). W2 instantiated **two**, and `CP-02`
carries `grade: UNREPRESENTABLE` and `done_when: missing-history`, both `required: true`. This
settles a question neither case could reach alone: `Capability` is not untestable, but a seventh of
the core hypothesis has no clean instance in either history. Downstream, I9/I13/I14 are vacuous in
the research case and `capability_classification` is unexercised there. **Nothing in this run
witnesses a versioned `Capability`.**

**(4) Zero OPEN items are resolved by these instances.** 50 OPEN items — mechanically verifiable from
the ledger: 20 `core-open` + 19 `supporting-open` + 11 top-level `open`. W4's adjudicated split:
**45 still-open · 3 not-exercised · 2 blocking-hole · 0 resolved-by-instance.** Both
`resolved-by-instance` claims made in the run were asserted by one workstream and contradicted by the
other; W4 ruled against both. The two `blocking-hole` items — `open.custody_enforcement` and
`supporting.Gate.open[2]` external enforcement — are the same fact from two directions: **no common
enforcement point exists, and the model says so itself.**

### 2.4 Per-construct verdicts (W4 §8.2–§8.5, unmoved by the rework)

| Layer | `retain` | `revise` |
|---|---|---|
| **Core (7)** | `Goal` | `Scope`, `Capability`, `Actor`, `Unit`, `Event`, `Record` |
| **Supporting (8)** | `Role`, `Technology` | `Workflow`, `Skill`, `Delegation`, `Gate`, `EffectBoundary`, `Attempt` |
| **Registries (6)** | `scope_type`, `capability_classification`, `record_category` | `event_type`, `unit_kind`, `effect_class` |
| **Catalogs (3)** | — | `skill`, `workflow`, `gate` — all three share one defect: `catalogs.*.scope` has no defined binding to any construct field, and `scope` is itself undocumented in `notation`. Under the SCOPE's adverse-evidence clause, none of the three can identify its members. |
| **Values (supplementary)** | — | `revise` — `evidence_grade` closed with no extension point; `autonomy_tier` unordered on a scale whose top value is `held_by: human`; **`coupling` is referenced by no field anywhere in M01**; `effect_disposition`'s explicit rule has no typed carrier |

The three `retain` rulings are load-bearing in the other direction and worth naming: `Role`,
`Technology` and `record_category` carry **zero `model-defect` rows** between them. `Technology`'s
I11 and its `enables` *"no grade transfer"* rule held in **both** cases — and in the software case it
was the project's own pre-registered ruling (*"do NOT mark any capability `proven` off vnc-045"*),
stated twice in advance by an independent reviewer and honoured at delivery.

### 2.5 What the model does well — recorded because a report that lists only defects is not adjudicating

- **All 19 declared inverse pairs are mechanically enforceable and were individually falsified**
  (`F-B01`–`F-B19` all rejected). W1's instance required 24 inverse edges to be closed before it
  validated: they are constraints, not decoration.
- **The `assessment` / `gate_outcome` split pays off in both cases.** W2's Gate-3a iteration-0
  assessment exists with no surviving outcome payload — under the merged v4 form it could not have
  been written at all. And the split's `rule:` is **the only working Event-layer value check in the
  entire model** — the exact fix pattern the rest of the Event layer lacks.
- **`I18`'s first clause is checkable and enforced** (`F-E29`/`F-E30`/`F-E31` all rejected), and only
  because `definition_custodian_ref` and `Attempt.actors` are both `ref<Actor>`. The model's clearest
  demonstration that a typed reference buys a check and a text field buys nothing.
- **The `Envelope` exclusion is vindicated against a project that literally uses the word** — the
  theme's `coordinator:` block decomposes onto `Delegation` field-for-field with no residue. All
  eleven exclusions pass their negative test in the research case.
- **V5 makes a false claim visible.** `gate-3c-report.md` does not exist at `37c7b09a`, and vnc-045 is
  the only one of **226** feature directories carrying a 3a and a 3b report but not a 3c (measured
  154/157/153, re-measured independently by W4). Under V5 the `assessment` Event is simply **not
  writable**, so "Gate 3c PASS" cannot pass as fact. That is `I8` doing work.
- **V5 refuses to let authored summaries pass as measurements**, and the software case supplies the
  proof: the report says the tool guard moved "12 → 15", the PR body calls `context_tag` "the 13th
  tool", and the committed diff says **14 → 15**. Three authored numbers, one observable fact, both
  authored records wrong, and nothing to check against.

---

## 3. Construct pressure, classified

Per the SCOPE's anti-force-fitting amendment, pressure is reported under five separate causes, and
the synthesis reports each separately rather than treating every mismatch alike.

**Reconciled ledger — curator-measured** from `reports/construct-pressure-ledger.csv`: **705 rows =
679 canonical `model-X` + 23 `instance-extension` appendix + 3 `w3-fixture` appendix.** Appendix rows
are excluded from every X count. **Zero blank cells in the file (0 of 25,380). Zero pressure rows
without a cause.**

| Reconciled disposition (679 model-X rows) | Rows |
|---|---:|
| `exercised` | **522** |
| `construct-pressure` | **123** |
| `not-applicable` | **31** |
| `blocked-by-OPEN` | **3** |

| Cross-case divergence | Rows |
|---|---:|
| both cases agree | **324** |
| `w1-not-enumerated` (reconciled from W2 alone) | **205** |
| divergent | **150** |

**Cause tally (row-weighted; multi-cause rows retain every cause).** 183 of the 679 model-X rows
carry at least one cause; **60 carry more than one**:

| Cause | Rows |
|---|---:|
| `historical-evidence-gap` | **85** |
| `model-defect` | **74** |
| `enforcement-gap` | **33** |
| `unresolved` | **33** |
| `project-evolution-candidate` | **31** |

### (a) Model failure — `model-defect`, 74 rows

The verdict moved **only** on these. They concentrate in the value layer, the Event layer and the
extension-ownership bindings (by row class: 12 `core-extension_owner`, 11 `core-field`, 7
`core-relation`, 7 `supporting-extension_owner`, 5 `supporting-field`, 5 `invariant`). The named ones:

- `values.evidence_grade` closed on a term the program rejected, with no registry and no owner (§2.3).
- **No `unestablished` member** for `EffectBoundary.can_refuse`, `Event.occurred_at` and
  `Capability.grade` — three *required* typed fields — while the sibling `values.currentness` and
  `values.effect_disposition` both carry `unknown`. In the research case this is why git and the
  forge are **not instantiated as EffectBoundaries at all**: neither `true` nor `false` is evidenced,
  and asserting one would be a fabrication.
- `Gate.procedure` is `enum[deterministic,judgment]` with **no mixed value**, and `wfh-008`'s
  coverage gate was demonstrably both — a sorted-set path diff and a 42/42 lock bijection *and*
  independent semantic judgment, with the final PASS turning on the judgment half. This is the run's
  only `blocked-by-OPEN` field row.
- `Attempt.disposition` is required with **no admissible value for an execution terminated with no
  actor-recorded disposition**. W1's instance writes `hold` and marks it `_approx`.
- `Scope.authority_root_ref` is required and defined as the holder of undelegated authority, which
  **forces one of two wrong answers on every nested Scope**.
- `Actor.declared_identity` **does not individuate an Actor**: fifteen W1 Actors share
  `"factory-researcher"`; two share `"research-leader"`; one owner carries three identity strings
  across two custody stores. The only individuator in the instance is the Delegation's `unit`.
- `Delegation.unit` is `0..1`, so three organisational directives each covering several Units became
  six model objects, losing the fact that they were one directive — checker-caught, not a judgment
  call. `grantor == grantee` (`DL-SCOPE`) is neither forbidden nor detected.
- `Unit` has **no name and no external reference**; `baseline_ref` is `text` with no integrity binding.
- I17 attenuation is **undefined on two of its three axes**: 24 derived Delegations are undecidable
  on `escalation_conditions` (a text list) and `resource_ceiling` (a heterogeneous map).
- I19 is cited by `Workflow` alone, so **five of the six constructs carrying `extension_owner` do not
  cite the invariant that guards extensions against weakening invariants**.
- The `excluded:` list is **re-openable through the registries by exactly the program the exclusion
  binds** — `F-H09` registers `lesson` as an event type and it is accepted silently (while
  *unregistered* `lesson` is correctly rejected by `F-A17`); `F-E08` registers `effect_completed`,
  reintroducing the merged effect event; `F-H08` registers a `unit_kind` named `attempt`,
  reintroducing Attempt as a Unit subtype. **The exclusions that hold are those carried by type or
  closure; those carried by prose against a registry do not.** That is a pressure the extension
  mechanism *creates*, not one it absorbs.
- Supersession chains admit cycles: `Event.supersedes`, `Record.supersedes` and `Workflow.supersedes`
  declare **no acyclicity**, while M01 declares `acyclic` three times elsewhere. Measured alongside
  it: the relation is populated on **0 of 32** W1 Events and **0 of 30** W2 Events — the weakest
  possible standing for the rule and the strongest for the defect.

### (b) Accidental or independently evolvable project complexity — `project-evolution-candidate`, 31 rows

Twelve distinct candidates. Reported in full in §4, including the ones that failed challenge. Five
ledger rows carry `project-evolution-candidate` as their **sole** cause (two `Record` rows and I15,
under W2/CF-01 and W2/CF-02); every one of the twelve *candidates* co-classifies with at least one
other cause, so the class is not used as a residual bucket for model pressure.

### (c) Historical evidence insufficiency — `historical-evidence-gap`, 85 rows (the largest class)

Absence stayed absence. Nothing was backfilled.

- **Every `vnc-045` Delegation is an inference**, and `resource_ceiling` has no source at all — treat
  the whole `delegations:` block as reconstruction.
- **All test outcomes in the software case are actor-authored doc-claims.** No raw runner output
  exists; one authored count is demonstrably wrong (the 14 → 15 diff, §2.5).
- **Every capability grade in the software case is a doc-claim** — the Unimatrix nodes and their
  `proven_by` sets are outside the alphabet.
- **Not one of the four `Actor.has_skill` attributes** (`evidence_refs`, `grade`, `currentness`,
  `expires_at`) is populated for any of the 22 Actor–Skill pairs in the research case. Agents are
  assigned by type, never by evidenced competence — sharpest at `SK-BUDGET-CONTROL`, where the run
  failed on credit exhaustion while that Skill carried no grade and no expiry.
- **`EV-004` (scope → tech-discovery) never reached Unimatrix.** All phase boundaries for the scope
  phase and the first tech-discovery pass are permanently missing and were **deliberately not
  backfilled** — the right call, and it leaves the model unable to mark an Event as "occurred but
  unrecorded by its designated carrier".
- The most consequential decision in the software case — the human scope reduction — **has no primary
  record**.
- `open.autonomy_A3_A4` stays `insufficient-evidence`: A4 is recorded *used* by a standing Delegation
  despite that status, and A3 has no witness in either case. One instance of a tier is not evidence
  about a tier boundary.
- `Capability`'s absence in the research case is jointly `historical-evidence-gap` and `model-defect`:
  the alphabet supplies neither an `observable_behavior` nor a `done_when` for the stated target, and
  V5 has no shape for a Goal legitimately naming a capability target that is not yet specified —
  `Capability` carries no `lifecycle_state` field where `Goal`, `Actor` and `Record` all do.

### (d) Enforcement absence — `enforcement-gap`, 33 rows

Reported as absence. **None of these moved the verdict.**

- **Zero enforced authority in the research case.** `Delegation.enforced_by` is empty on **31 of 31**
  Delegations. The single refusal receipt in the entire history — five `context_cycle` calls refused
  for a 512-character `outcome` cap and control characters — is a **schema** refusal, not an
  authority refusal. `EffectBoundary.enforces` is empty in **both** cases. I12's second clause has no
  witness anywhere in this garage.
- **The garage's strongest custody claim — the single-writer curator rule — has no enforcement point
  at all.** Any actor may call `context_store`; the server checks only that an identity *string* is
  present, and that string is persisted self-assertion, not attestation.
- **I18 custody is unsatisfied.** All method definitions live in `.claude/` inside the repository the
  governed agents write to; there is no `CODEOWNERS` file and no branch-protection artifact in the
  tree. Two evidenced facts cut opposite ways: the method surface was *not* edited during `wfh-008`
  (a positive behavioural observation), and `research-scope.md`'s most recent revision was authored
  by the governed actor class itself. Plus a real incident: an `npx` install silently overwrote
  twelve method files with copies predating the D6 amendment, with no decision Event, caught by a
  human reading.
- **`EffectBoundary` has no relation to any `Actor`**, so a conforming, typed-clean claim that the
  executing agent holds the boundary's credentials **cannot be contradicted** (`F-G02`) — on the
  construct whose entire purpose is custody.
- **I1's no-overwrite rule is a convention, not a guarantee.** `RC-COV-R2` was amended in place twice
  after publication; findings Records were edited in place across three rework passes. No Record
  identity was reissued. Prior versions survive only in git — **whose identities were then rewritten
  by a rebase**, and whose pre-rebase branch is already deleted on `origin`, so a fresh clone
  resolves nothing.
- **`refused` and `unknown` effect dispositions have no witness in either case.** No refusal was
  claimed anywhere.

### (e) Unresolved ambiguity — `unresolved`, 33 rows

Per the amendment these count as **neither conforming nor rejecting evidence**, and they stay
unresolved through synthesis.

- **W2's `T01`/`T02` are living, unversioned protocol files** read at `37c7b09a`, not at the vnc-045
  delivery date. If the protocol changed in between, the software case's `Workflow`, `Gate`, `Role`
  and `Delegation` instances are anachronistic, and **nothing in the fixed alphabet dates the
  revisions**. W2 named this its single largest soft spot; W4 weighed it `unresolved` and material;
  the round-2 auditor recorded it as unchanged and unchangeable from inside the alphabet. It changes
  no verdict — each is carried by at least one research-case or W3 witness as well — but it **caps
  the software case's independent weight**.
- **Whether Gate 3c ran at all is unresolvable** from the fixed alphabet, and no project change
  settles it retrospectively.
- **40 of W1's 79 pressure rows carried `cause_classification: not-applicable`**, which coverage
  clause 9 forbids. W4 supplied `unresolved` rather than drop the rows, on the ground that the
  evidence does not discriminate `model-defect` from `historical-evidence-gap` for an OPEN item a
  case merely did not settle. Those rows are adjudicator-supplied, not workstream findings, and 30 of
  the 50 OPEN rows carry `unresolved` as a result.
- `open.lesson_vs_pattern` rests on **one weak data point** — `wfh-008`'s most reusable method rule,
  the custody predicate, filed as a `finding` (`#320`) rather than a `lesson-learned`, with no
  distinct admission or retrieval behaviour. Weak because nobody tried the alternative.
- `open.semantic_compression` stays open **by construction**: two owner-operated histories cannot
  settle a generality claim in either direction, and both workstreams say so.

---

## 4. Project-evolution candidates and the circularity challenge

Twelve distinct bounded counterfactuals were constructed (W1 CF-01…CF-07, W2 CF-01…CF-05; the
identifiers collide, so W4 namespaced them) and each was independently challenged on circularity
(13), independent reasonableness, semantic/proof/authority/custody preservation and behaviour erasure
(14), authority laundering (15), counterfactual-versus-history separation (16), migration-cost
realism (17) and dual representability. **31 ledger rows carry an evolution candidate; the curator
verified all 31 carry all five analyses, both fit verdicts, the dual-representability fields, and a
challenge result — zero blanks, zero `not-challenged`, zero `W1/unlabelled`.**

**These are directional counterfactuals. None is a recommendation, and none is authority to change
anything.** Conformity to V5 is never itself a reason a project should evolve, and nothing below may
be read as advice to change either project.

### 4.1 The challenge results, in full

**Curator-measured from the ledger's `evolution_challenge_result` column: 9 survive cleanly · 2
survive with a recorded defect · 1 FAILS.**

| id | Change | Challenge result |
|---|---|---|
| **W1/CF-07** — expose a content digest on knowledge-node reads | **FAILED — concern 17 (migration realism).** Carried on **3** ledger rows (`notation.types`, `core.Record.fields.content_digest`, `M02.sanity.S3`), each reading `FAILS concern 17 (migration realism)` verbatim. W1 states plainly that the change targets a service outside this repository and that *"this scope cannot cost it."* Cost, compatibility and coexistence are therefore **not explicit** — honestly incomplete rather than hidden, but incomplete. **The underlying `model-defect` is untouched by this failure and stands on its own:** `Record.content_digest` is a required `digest` with no `unestablished` member, and eleven service-backed Records in the research instance carry sentinels the checker reports (27 `MODEL-FORCED-APPROXIMATION` warnings on that field). |
| **W1/CF-01** — tree-oid baselines; no rebase after a gate has ruled | **Survives with a recorded defect (concern 17).** Its 2026-08-29 correction *narrowed* `affected_artifacts`, dropping two errata surfaces, while W4's own execution *strengthened* the residual: the branch holding the ten pre-rebase objects is already deleted on `origin`. **Migration cost is understated relative to its own rationale.** |
| **W1/CF-06** — rename agent frontmatter `capabilities:` → `skills:` | **Survives with a recorded defect.** Passes circularity (the Unimatrix `capability` category collision predates V5). **Fails the evidence bar on independent reasonableness:** the asserted harm is not evidenced inside the fixed alphabet, and W1's own `unresolved_discriminator` concedes that whether the collision has ever caused a concrete error is not evidenced by this case. |
| W1/CF-02 — sha256 manifest over the method surface + drift check | Survives all six challenges. Grounded in the evidenced `npx`-overwrite incident. States its own limit honestly: a manifest **detects** drift and does not establish custody, because the manifest lives inside the governed repository. **I18 stays unsatisfied in both forms.** |
| W1/CF-03 — typed interruption record on session death | Survives — **and explicitly declares that the model defect is NOT repaired by the evolution.** W1 sets `current_form_representable: false`. The clearest case in the run of a project change that must not be allowed to hide a model defect. |
| W1/CF-04 — audits retain the raw output they rule on | Survives. Grounded in an evidenced incident. Explicitly refuses the laundering: raises altitude to `reported-observation`, **not** `mechanical-observation`, because capture custody stays inside the reporting actor. |
| W1/CF-05 — declare the coverage-auditor duty as a Role | Survives. Independent reason is measured: the same blocking gate was assessed under two different role identities in consecutive runs (`wfh-010` a `factory-validator`, `wfh-008` a `factory-researcher`). |
| W2/CF-01 — stamp reports with the SCOPE digest; stamp `superseded_by` on regeneration | Survives. The project already pays this by hand — the alignment report records a pattern citing a now-stale instance and hands the retro a manual reconciliation. |
| W2/CF-02 — `reviewed_commit: <sha>` in the gate-report template | Survives. T01 already declares *"Gates check committed HEAD"*; the evidenced harm is a gate-3b open WARN already fixed 24 minutes before the report was committed. |
| W2/CF-03 — record the scope decision on the tracking issue when it is made | Survives, and **moves authority the safe way** — narration moves *away* from the actors it governed. |
| W2/CF-04 — retain runner output beside the risk-coverage report | Survives — best-evidenced candidate in the run, and W4 reproduced the harm itself (the 14 → 15 diff). |
| W2/CF-05 — Gate 3c report as a forge-side required check | Survives — best-constructed candidate. Enforcement moves onto an externally custodied boundary, **away** from every governed actor. And it **refuses to let post-evolution fit conceal the current verdict**: `current-project fit for GT-06 stays reject`. Records its own residual honestly: *a required check whose predicate is "a file exists" is satisfiable by writing a file.* |

### 4.2 Five candidates were considered and correctly NOT proposed

Recorded because the refusals are themselves evidence: per-agent `agent_id` (relitigates ratified D6
from outside its evidence); instantiating a Capability for `jurati-arch-002` (**the circular
candidate**); enforcing the single-writer curator rule (the build recommendation this scope forbids);
renaming `asserted` → `claimed` (**circular, and would erase an evidenced ruling**); credentialed
per-agent identity (relitigates a human-LOCKED ADR-008 posture whose declarative-attribution bound is
an accepted residual risk).

### 4.3 Why the two fit verdicts are identical

**Not one of the surviving candidates repairs a model defect.** They improve *evidence* (CF-04 raises
evidence altitude; W2/CF-05 supplies the run's only proposed enforcement point; CF-01/02/03 improve
reproducibility and recovery) and repair *no* construct. The two changes V5 would most "prefer" are
**the two that were rejected as circular**. So there is no better post-evolution result, and
therefore nothing concealing the current one.

**Concern 13 — circular force-fitting: none found.** No surviving candidate's independent reason
mentions V5, and both workstreams identified and rejected their own circular candidate before the
adjudicator reached them. **Concern 16 — counterfactual confusion: none found**, and in the research
case the separation is *mechanically* enforced: the checker errors if a counterfactual object appears
in the historical file and refuses to close inverse edges across the boundary. No counterfactual is
counted in any coverage number in this run.

---

## 5. What was NOT established

**This section is the reason the report exists.** Every number below was verified by the curator
against the artifacts.

### 5.1 The three defects that survive the `PASS` — `gate-coverage-r2.md` §4

The round-2 auditor ruled `PASS` and recorded three surviving defects, all pre-existing and newly
visible, none rework-introduced. **They are conditions on how this coverage may be read.**

**(i) Twelve `*-relation-inverse` rows in `vnc-045-coverage.csv` are `exercised` on a boilerplate
witness while closing zero edges in the software instance — and the auditor named this the one place
its own ruling could reasonably have gone the other way, and referred it to the owner.**

Curator measurement, which goes one step further than the auditor's: **all 34** declared-inverse X
rows in that matrix are `exercised`, and **all 34 carry the identical witness string** `instantiated
in vnc-045-instance.yaml` — there is exactly **one distinct witness string across the 34**, so none of
them was ever joined to its instance. (Whole-file context: **259 of the 679 rows** in that matrix
carry that same boilerplate.) Measuring closure across both instances myself from `w4-witness.json`
and the two instance files: **18 close in both cases, 6 in W1 only, 4 in W2 only, 6 in neither.** So
**22 of 34 close in `vnc-045`** and **28 of 34 in at least one case** — the boilerplate is true by
accident on 22 rows and **false as a software-case witness on 12**. Any statement of the form *"the
software case exercises N declared inverses"* taken from that matrix is wrong by up to 12. In the
reconciled ledger those same 34 rows resolve correctly: `exercised` 28, `not-applicable` 4,
`construct-pressure` 2.

The auditor ruled coverage clause 3 `MET` notwithstanding — because the reconciled ledger (which
synthesis consumes) is provably correct on all 34; because W2 named, counted and published the
shortfall itself rather than concealing it; and because the rework instruction named four row classes
and `*-relation-inverse` was not among them. **The auditor then put the alternative reading on the
record and referred it to the owner:** clause 3's *"in each case where the history supplies one"*
limb, read strictly per-case, is **not met** on those 12 rows, and *"an owner who wants the case
matrices to stand alone as coverage evidence has a legitimate basis to withhold on that limb. That is
the owner's call, not mine, and the remedy is one line of the same join."*

**This report does not resolve that. It is open, and it is the owner's.**

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

**(ii) `vnc-045-instance.yaml` carries 69 conformance errors and was NOT repaired to clear them.**
Curator-verified from `artifacts/vnc-045-validate.out.txt`: `RESULT: 69 error(s), 285 warning(s), 14
note(s)`, exit 1, over 151 objects across all 15 constructs. Measured decomposition of the 69:

| n | class |
|---:|---|
| **55** | declared-inverse edges that do not close — of **210** checked (73.8 % closure) |
| **11** | missing required field `Delegation.effective_at` (`DL-03`…`DL-13`) |
| **3** | dangling relation targets: `WF-01.binds → GT-01/GT-02/GT-03`, ids that do not exist |

The errors are the workstream's encoding defects, not V5's. Two things must be said about them.

First, **the file's sha256 is byte-identical before and after the validator that found them**
(`c65b2ba9…cca6d9eef`, verified unchanged across the whole rework range by the round-2 auditor and
again here). The cheapest way to clear the gate was to add three Gate objects, eleven timestamps and
fifty-five back-references and publish a clean run. Nobody did. The run published the 69 and left the
artifact alone.

Second, **every claim resting on the software case rests on an instance with that error load.** Until
this round no executed checker in the run could read the file at all: both prior validators key on a
top-level `instances:` map, the W2 file uses flat sections, and **both therefore printed a green
result over zero objects.** The file read correct and parsed wrong, and it passed through a coverage
table, a cross-case reconciliation and a full coverage audit before an instrument was pointed at it.

The same pass also emitted 285 warnings that are **not** counted as errors and should not be read as
conformance: **167 `RECORDED-ABSENCE`** (required fields and event-extension keys carrying
`missing-history` / `unestablished` / `UNREPRESENTABLE` / `ABSENT` — the evidence gaps of §3c made
machine-visible per object), **82 `O-W2-1`** (construct marked `versioned: true`, object carries no
`version` — the instance cannot say which revision of `SCOPE.md` any Unit followed), and **27
`MODEL-FORCED-APPROXIMATION`** on `Record.content_digest`.

**(iii) W4 §13.3's disclosed scoping counts do not reproduce.** See §5.6.

### 5.2 W1's 468-row matrix is not protected by the witness guard

The reconciled ledger is protected at witness-bearing paths, because W4's guard measures the
instances directly. **`wfh-008-coverage.csv` is not.** Curator-verified: 468 rows — `exercised`
**339**, `construct-pressure` **76**, `not-applicable` **49**, `blocked-by-OPEN` **3**,
`inspected-no-material-instance` **1**.

And W4 disclosed a defect in W1's generator **against its own case, unprompted**: it counts **key
presence, not value population** (`fname in r.get('fields')`). `core.Goal.fields.north_star` was
reconciled `exercised` on W1's witness text *"set on 2/2 instances"*; measured, the instance carries
`north_star: []` on **both** Goals, and the software case carries the placeholder `missing-history`.
This is the same label-over-value defect the round-1 audit found in W2's table, on the side that
audit had credited as sound. It ties to W1's own `PR-LIST-REQUIRED`: `M01`'s `notation` never says
whether `required` on a `list<>` type means *key present* or *non-empty*, so `[]` is a value **no
checker can rule on** — which is exactly how it survived, and why no rejecting counterexample can be
built for it either.

### 5.3 205 canonical X rows rest on a single case

**W1 enumerated 468 X rows; W2 enumerated 679. They are two different granularities, not two readings
of one list**, and W2's matches the SCOPE's X clause literally while W1's does not — W1 rolls
relation sub-keys (`cardinality`/`inverse`/`rule`/`attributes`) into one row per relation, rolls
per-invariant bindings into one row per construct, and omits construct `definition` and registry
seed-field rows entirely. (The two files do not even share a class vocabulary: W1's column is
construct-named `x_kind` and contains **no** `*-relation-inverse` value at all; W2's is shape-named
`x_class`.)

Curator-verified from the ledger's `divergence_class` column: **`w1-not-enumerated` on 205 of 679
rows**, `agree` on **324**, `divergent` on **150**. Those 205 rows are reconciled **from the software
case alone** and are marked as such. Absence was not filled — but their weight is capped at one case,
and that case is the one carrying 69 conformance errors (§5.1 ii).

The asymmetry runs the other way too, and is recorded rather than resolved: **on 6 declared inverses
the research case closes every edge and the software case closes none.**

### 5.4 An unreported ledger state: 52 rows are `exercised` and carry a cause

Curator measurement, published here for the first time at the reconciled altitude: **52 of the 679
model-X rows are reconciled `exercised` while carrying a pressure cause, and 36 of those 52 carry
`model-defect`.** W4 §3.5 flagged this shape as an internal-consistency defect in the *case* matrices
(W1 27 rows, W2 19) and adjudicated one instance of it on the evidence rather than the label
(`M02.sanity.S4`: `exercised` on a row whose own witness text read *"CONFIRMED AND IT BITES."*).
Neither W4 nor either auditor states the reconciled count.

**This is not necessarily wrong** — a construct can be genuinely exercised and still be under
recorded pressure. But **neither `M01` nor the ledger defines semantics for the combination**, and a
reader who takes `exercised` to mean "no problem found" will be wrong on 52 rows.

A related legibility gap: **W4's OPEN split (45 / 3 / 2 / 0) is authored in its §5 and is carried in
no ledger column.** The `open_pressure_disposition` column still shows the workstreams' original
claims, including three `resolved-by-instance`(-at-document-altitude) strings that W4 explicitly
overruled in prose. Only the total is mechanically verifiable (50 OPEN rows). The closest mechanical
proxy — `reconciled_disposition` over those 50 rows — reads 45 `construct-pressure` / 3
`not-applicable` / 1 `exercised` / 1 `blocked-by-OPEN`. **A reader of the ledger alone cannot recover
W4's OPEN adjudication.**

### 5.5 Three internal inconsistencies in the findings that no audit caught

All three are prose-arithmetic defects in findings files, not artifact defects, and **none changes a
verdict.** They are reported because this run's own subject is printed values that have quietly
stopped naming one thing.

- **W4: "ten surviving candidates" versus eleven.** W4 §7 rules *"9 survive cleanly · 2 survive with
  a recorded defect · 1 fails"* over twelve candidates — **eleven surviving**. W4 §1, §8.1 and §12
  (concern 14) each say *"the ten surviving candidates."* The curator reproduced §7's split from the
  ledger: 3 rows `FAILS concern 17` (all W1/CF-07), 2 rows `survives-with-recorded-defect`
  (W1/CF-01), 1 row `survives, recorded defect` (W1/CF-06), 25 rows `survives` in some form.
  **Eleven survive.** The load-bearing claim is unaffected: none of the eleven repairs a model
  defect, so the two fit verdicts remain identical for exactly the same reason.
- **W4 §12's cause tally is stale.** Concern 18 restates *81 / 73 / 33 / 31 / 30* — the round-0
  figures W4's own §4.1 marks superseded. The final measured figures are **85 / 74 / 33 / 31 / 33**
  (§3 above). §4.1 retains the round-0 column beside the new one; §12 was not updated with it.
- **W2's decomposition of its own 55 inverse errors transposes two relations and undercounts a
  third.** W2 §F-15 states *"19 are `Attempt.unit ↔ Unit.attempts` and 18 are `Attempt.governed_by ↔
  Delegation.governs`"*, and *"three more are `Unit.gated_by ↔ Gate.evaluates`"*. Curator-measured
  from the executed log: `Attempt.governed_by ↔ Delegation.governs` is **19**, `Attempt.unit ↔
  Unit.attempts` is **8**, `Unit.gated_by ↔ Gate.evaluates` is **6** (3 from each side), and the
  group W2's prose does not mention at all — `Delegation.unit ↔ Unit.assigned_through` — is **11**.
  The remaining 11 are `Record.documents ↔ Event.documented_by` 5, `Unit.directed_by ↔ Goal.directs`
  2, and 1 each on `Workflow.binds ↔ Gate.bound_by`, `Gate.bound_by ↔ Workflow.binds`,
  `Capability.required_by ↔ Goal.requires`, `Delegation.enforced_by ↔ EffectBoundary.enforces`.
  W2's stated groups sum to 40 of 55; the measured decomposition sums to 55. **The 55 total, the 69
  total and the 210-edge denominator are all correct** — only the narrative attribution is wrong, and
  the round-2 auditor verified the log reproduces byte-identically without checking the prose
  decomposition against it.

### 5.6 W4 §13.3's own disclosed counts do not reproduce

W4 §13.3 states the witness guard covered **274** `exercised` rows and left **269** outside its
scope. The round-2 auditor measured **268** and **278**. **The curator independently reconstructed
the class partition and reproduces the auditor:** **329** witness-bearing rows of which **244** are
finally `exercised`; **350** non-witness-bearing rows of which **278** are `exercised`;
244 + 278 = 522, which is the final `exercised` total. Adding back the 24 rows the guard moved off
`exercised` gives **268** witness-bearing rows `exercised` when the guard ran.

| | W4 §13.3 | round-2 auditor | curator |
|---|---:|---:|---:|
| witness-bearing rows `exercised` when the guard ran | 274 | **268** | **268** |
| non-witness-bearing rows `exercised`, left outside | 269 | **278** | **278** |
| sum | 543 | **546** | **546** |

**Both figures are reported and attributed. The auditor's measurement is corroborated by mine; W4's
authored pair is not.** No artifact depends on the two numbers, and every other §13 count the auditor
and the curator checked reproduces exactly — including the 18/6/4/6 inverse split, the 39 annotated
rows and the 27 changed. But **the error runs in the direction that understates the excluded set by
nine, and it sits in the one paragraph whose whole purpose is to disclose what the guard did not
cover.**

### 5.7 What this run proves nothing about

- **Generality.** Two owner-operated histories inside one organisation.
  `open.semantic_compression` stays open by construction, exactly where `wfh-010` left it.
- **Runtime enforcement.** Every mechanical result is a property of a checker written this week from
  a YAML file. No historical project refused anything on V5's account. `EffectBoundary.enforces` is
  empty in both cases; the two `blocking-hole` OPENs both say the same thing — **no common
  enforcement point exists.**
- **Organizational effectiveness.** Nothing here measures whether either project worked better or
  worse for being shaped this way.
- **A product boundary.** Nothing here says what should be built, by whom, or where a runtime would
  sit. The SCOPE forbids a build recommendation and this report makes none.
- **Semantic compression outside these two cases.** `wfh-010` left it plausible and unproven; this
  run leaves it exactly there.
- **Portability, external cost, validated scope, or material compute.** All out of scope, none
  touched. Zero external cost, zero network research, no material compute.
- **The evolved forms.** No counterfactual in either file was run against a rejection suite — W3
  derived its baseline from `M01` precisely to avoid contaminating the adjudicator's independence,
  which was the right call and leaves this gap. W2/CF-05's own recorded residual — *a required check
  whose predicate is "a file exists" is satisfiable by writing a file* — is precisely the shape W3's
  suite is built to falsify, and it was **not falsified.** That is a gap in this run's coverage.
- **The ~400 encoded case objects.** Neither W4 nor either coverage auditor re-derived either
  instance from its source alphabet. Where a row rests on a workstream's encoding judgment, every
  downstream ruling rests on it too — and §5.1 (ii) quantifies what that cost in the software case.
- **That the run performed zero Unimatrix writes.** The round-2 auditor made no `context_*` call and
  states this as **attested, not measured**. This report inherits that limit and repeats the reason:
  recorded attribution is persisted self-assertion, not attestation, so it is reliable for
  reconstructing what happened and unreliable for establishing who is accountable.

### 5.8 No successor model exists

**No V6, no replacement schema, no sketch, no normative default for any OPEN item, and no build
recommendation** was authored by any workstream, by the adjudicator, by either auditor, or by this
report. **None may be inferred from anything above.** A `revise` verdict names where the pinned model
is inadequate; it does not describe, imply, or authorize its successor. `M01` was parsed as-is
throughout — nothing quoted, normalized, patched in memory, or imported from the review's intended
prose — and its digest did not move at any point in the run.

---

## 6. Proposed staged follow-on — a proposal, not a commitment

Offered for the owner to accept, reorder, or discard. **None of this is a build recommendation, none
is authority to change either project, and none is a commitment of budget.** Each stage is
independently killable and each is scoped so that failing it is cheap.

**Stage A — resolve the one referred question (owner decision, no run).** The round-2 auditor
explicitly referred clause 3's strict per-case reading on the 12 inverse rows to the owner (§5.1 i).
That is a ruling on what the case matrices are allowed to stand for, not a research question. It
costs one decision, and the auditor states the remedy is one line of the same join.

**Stage B — the cheapest adverse re-test, on artifacts that already exist.** Three gaps in this run
are closable without new sources: run W3's rejection suite against the two counterfactual files
(never done — §5.7); re-derive `wfh-008-coverage.csv` with a population-measuring generator rather
than a key-presence one (§5.2); and extend W2's join to the 34 `*-relation-inverse` rows (§5.1 i).
All three are deterministic, zero external cost, and all three can only produce adverse or neutral
results — which is the point of doing them before anything more expensive.

**Stage C — a third case, chosen to break the run's standing limit rather than confirm it.** The
binding constraint on everything above is **two owner-operated histories inside one organisation**. A
third case adds nothing unless it is outside that envelope. The highest-value target is a history
that supplies what neither of these could: a **`Capability` with a real `observable_behavior` and
`done_when`** (unwitnessed in both cases), an **actual `EffectBoundary` refusal receipt** (unwitnessed
in both cases — no refusal was claimed anywhere), and a **method surface under custody the governed
actor cannot write** (I18 unsatisfied in both the current and every evolved form). If a candidate
history supplies none of those three, it will re-derive this run's verdict at this run's cost and
should not be run.

**Stage D — deliberately not proposed.** Authoring a successor model is *not* proposed as a follow-on
here. The `revise` verdict names the defects; it does not establish that the right response is a new
schema rather than bindings on the existing one, a narrower scope, or nothing at all. That question
is upstream of this report and belongs to the owner and the theme, not to this run's synthesis.

---

## 7. Provenance

| Artifact | Path |
|---|---|
| SCOPE (with all three append-only extensions) | `product/research/wfh-011/SCOPE.md` |
| W1 — research-case instantiation (`wfh-008`) | `product/research/wfh-011/findings-W1-research-instance.md` |
| W2 — software-case instantiation (`vnc-045`) | `product/research/wfh-011/findings-W2-software-instance.md` |
| W3 — adversarial invalid-instance and traversal suite | `product/research/wfh-011/findings-W3-rejection-suite.md` |
| W4 — independent cross-case adjudication | `product/research/wfh-011/findings-W4-adjudication.md` |
| Reconciled construct-pressure ledger (705 rows) | `product/research/wfh-011/reports/construct-pressure-ledger.csv` |
| Coverage gate round 1 — `REWORKABLE` | `product/research/wfh-011/reports/gate-coverage.md` |
| Coverage gate round 2 — `PASS` | `product/research/wfh-011/reports/gate-coverage-r2.md` |
| Instances, counterfactuals, checkers, executed outputs | `product/research/wfh-011/artifacts/` |

**Reproducibility.** Every checker in this run re-executes byte-identically, verified independently by
W4 and by both coverage audits in isolated mirrors: `v5_model_check.py`, `wfh-008-validate.py`
(0 errors / 33 warnings / 8 notes, 191 objects), `wfh-008-coverage-gen.py` (468 rows),
`vnc-045-validate.py` (69 / 285 / 14, 151 objects), `vnc-045-coverage-build.py` (679 rows),
`v5_instance_check.py suite` (115 fixtures) and `traverse` (67 rows), `w4-witness.py`, and
`w4-build-ledger.py` (705 rows). The run's largest artifact went from unreproducible to reproducible
from a committed generator during the rework — which nobody asked for.

**Traversals.** 67 executed rows over the W3 synthetic baseline: 34 `demonstrated-both-directions`,
18 `partial-proxy`, 8 `demonstrated-by-index`, 5 `equivalent-on-this-instance`, 2 `demonstrated`. Both
required one-way traversals (`Goal → applicable Workflows`, `Actor → participated Attempts`) resolve
only by **full-extent index scan**, recorded as **query-layer holes** rather than closed by adding a
model relation — and the `Goal → Workflow` declared-relation path is both incomplete and unsound.

**Citations** (structured; provenance carried through exactly as the source files supplied it —
unknown keys omitted rather than invented):

- `{type: docs, ref: "product/factory/proposals/organizational-data-model-v5.yaml", title: "Organizational Data Model — V5 (pinned, sha256 bf8e5536…9841060, 561 lines; digest re-verified at synthesis)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/factory/proposals/codex-organizational-data-model-v4-review.md", title: "Review — codex-organizational-data-model-v4.yaml, incl. §9 V5 sanity findings S1–S8 and the traversal obligation", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/SCOPE.md", title: "wfh-011 SCOPE with the Premise Recheck, anti-force-fitting Amendment, and Human-resume extensions", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/findings-W1-research-instance.md", title: "wfh-011 W1 — Research-case instantiation of wfh-008 (191 objects, 14 constructs, zero Capability)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/findings-W2-software-instance.md", title: "wfh-011 W2 — Software-case instantiation of vnc-045 (151 objects, 15 constructs, 69 conformance errors)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/findings-W3-rejection-suite.md", title: "wfh-011 W3 — Adversarial invalid-instance and traversal suite (115 fixtures, 67 traversal rows)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/findings-W4-adjudication.md", title: "wfh-011 W4 — Independent cross-case adjudication; verdict revise, current-project revise, post-bounded-evolution revise", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: "product/research/wfh-011/reports/gate-coverage-r2.md", title: "wfh-011 coverage gate round 2 — PASS, with three surviving defects and one reading referred to the owner", org: "arch-research garage", year: 2026}`
- `{type: dataset, ref: "product/research/wfh-011/reports/construct-pressure-ledger.csv", title: "Reconciled construct-pressure ledger — 705 rows (679 model-X + 26 appendix); 522/123/31/3; causes 85/74/33/33/31 over 183 caused rows", org: "arch-research garage", year: 2026}`
- `{type: dataset, ref: "product/research/wfh-011/artifacts/rejection-results.csv", title: "115 executed rejection fixtures — 82 rejected-mechanically, 18 accepted-defect, 9 not-falsifiable, 5 specified-not-enforced, 1 negative test", org: "arch-research garage", year: 2026}`
- `{type: dataset, ref: "product/research/wfh-011/artifacts/vnc-045-validate.out.txt", title: "vnc-045 instance validation — 69 errors (55 inverse of 210 checked, 11 missing effective_at, 3 dangling binds), 285 warnings, 14 notes, 151 objects", org: "arch-research garage", year: 2026}`
- `{type: repo, ref: "dug-21/unimatrix@37c7b09aa0db6ba16f5f95dadd24c58adb4e6e2b", title: "vnc-045 merge commit — single parent (squash-merged), 43 files under product/features/vnc-045/, 226 feature directories with 154/157/153 gate-3a/3b/3c reports", org: "dug-21", year: 2026}`
- `{type: docs, ref: "dug-21/unimatrix@37c7b09a:product/features/vnc-045/SCOPE-RISK-ASSESSMENT.md", title: "SR-10 records the program grade vocabulary {proven, partial, missing, asserted}", org: "dug-21", year: 2026}`
- `{type: repo, ref: "https://github.com/dug-21/unimatrix/issues/928", title: "Issue #928 comment 4898695344 — SLN1 (#5528) recorded as curve/nfr, asserted; the OQ-1 ruling names claimed a slip", org: "dug-21", year: 2026}`
- `{type: docs, ref: "product/factory/themes.md", title: "Standing research themes — theme:workflow-harness authority/objective/lens/load-bearing-boundary block", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: ".claude/rules/unimatrix-access.md", title: "Unimatrix Access Rules (factory agents) — recorded attribution is persisted self-assertion, not attestation", org: "arch-research garage", year: 2026}`

---

**Status: synthesis complete — directional, structure-only.** Zero Unimatrix writes, zero grade
movement, no `proven`, no model edit, no successor schema, no build recommendation, no project change
authorized. A coverage `PASS` is necessary and not sufficient: the firewall gate is the human owner's
ruling, and the reading referred at §5.1 (i) is open and awaiting it.
