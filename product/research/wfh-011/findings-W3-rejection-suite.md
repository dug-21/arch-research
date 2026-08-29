# wfh-011 W3 — Adversarial invalid-instance and traversal suite

**Run:** `wfh-011` · theme `workflow-harness` · research-scope, **DIRECTIONAL** · phase `tech-discovery` ·
[Issue #70](https://github.com/dug-21/arch-research/issues/70)
**Workstream:** W3 — model/rejection test against the pinned Organizational Data Model V5
**Author:** `factory-researcher` (W3) · 2026-08-29
**Status:** findings only. No Unimatrix write, no grade movement, no model edit, no V6, no build
recommendation, no normative default for any OPEN item.

---

## 0. Provenance, and what a result in this file does and does not mean

**Model under test (M01), digest re-verified by W3 before consumption:**

```
$ sha256sum product/factory/proposals/organizational-data-model-v5.yaml
bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060   (561 lines)
```

This **matches the pin** recorded in the SCOPE's *Premise Recheck* and *Human resume* extensions. The
file was parsed **as-is**: no quoting, no normalization, no in-memory patching, and no intended prose
imported from M02. Where W3's parse and M02's prose disagree, the disagreement is recorded (§7), never
repaired. Independently re-confirmed: all six S1 scalar-split sites now parse to their complete
values, and a generic scan for the S1 defect signature (a prose fragment promoted to a mapping key)
finds **0** occurrences anywhere in the file.

**Three statements that govern every row below.**

1. **A `rejected-mechanically` result means only this:** a checker that W3 generated from M01's own
   typed declarations refuses the document. It is **not** evidence that `wfh-008`, `vnc-045`,
   Unimatrix, git, a forge, or any workflow refuses anything. `meta.enforcement_reality` in M01 says
   no common checker implements this model, and W3 found no reason to doubt it. **The checkers in
   `artifacts/` are research artifacts. Their existence is not enforcement, in either historical
   project or anywhere else.**
2. **Every fixture is a deliberately constructed counterexample.** None is observed history. The
   conforming baseline they mutate (`artifacts/w3-baseline-instance.yaml`, ids prefixed `SYN-`) is
   constructed **from M01**, not from either case, precisely so that no reader can mistake a fixture
   for something that happened. Per the SCOPE amendment, W3 encodes **no counterfactual project
   evolution**; W1/W2 own that, and W3 may challenge evolved forms only once they are explicit.
3. **W3 authored these fixtures and W3 ran the checker.** W3 is therefore *not* an independent judge
   of them. The vocabulary value `rejected-by-independent-judgment` is used **zero** times, and
   deliberately: the only rejecting judgments available in the fixed alphabet that are independent of
   W3 are M02's, which are dispositioned separately in §7. Rows whose invalidity is semantic and
   which no checker can reach are reported as `specified-not-enforced`, not as a judgment W3 awards
   itself. **W4 is the independent adjudicator.**

### Reproduction

```bash
cd /workspaces/arch-research
sha256sum product/factory/proposals/organizational-data-model-v5.yaml     # must match the pin

python3 product/research/wfh-011/artifacts/v5_model_check.py              # model-level structure

python3 product/research/wfh-011/artifacts/v5_instance_check.py validate \
  --instance product/research/wfh-011/artifacts/w3-baseline-instance.yaml # 0 findings

python3 product/research/wfh-011/artifacts/v5_instance_check.py suite \
  --instance product/research/wfh-011/artifacts/w3-baseline-instance.yaml \
  --matrix   product/research/wfh-011/artifacts/invalid-instance-matrix.yaml \
  --out      product/research/wfh-011/artifacts/rejection-results.csv

python3 product/research/wfh-011/artifacts/v5_instance_check.py traverse \
  --instance product/research/wfh-011/artifacts/w3-baseline-instance.yaml \
  --out      product/research/wfh-011/artifacts/traversal-results.csv

python3 product/research/wfh-011/artifacts/gen_inverse_fixtures.py        # regenerates section B
```

Deterministic; stdlib + **PyYAML 6.0.3** only (verified present; `yq` v4.44.3 used only for the
independent scalar re-read). No network, no external cost, no material compute. Raw output is
committed verbatim: `v5_model_check.out.txt`, `baseline-validate.out.txt`, `rejection-suite.out.txt`,
`traversal.out.txt`.

### Disclosed operationalizations

M01 leaves some rules evaluable only after a choice it does not make. Every such choice is numbered,
disclosed in the checker header, and carried in the matrix's `mechanizability` and `operationalization`
columns, so a reader can see exactly where W3 supplied a rule the model did not.

| id | choice | consequence if a program chose otherwise |
|---|---|---|
| **O1** | declared field/relation/construct sets are **closed** | an open-world implementer accepts F-A33, F-A34, F-E14 and all seven excluded-construct fixtures |
| O2/O3 | lexical forms for `digest` and `timestamp` | M01 declares neither |
| O4 | a registered registry entry must carry its shape's keys | see F-C07 — M01's own `gate_outcome` seed carries a key **outside** the shape |
| O5 | `Unit.current_state` in the governing `Workflow.state_vocabulary` | the strongest extension-ownership check in the suite exists only by this choice |
| O7/O8/O12/O13 | string comparison for `intended_outcome`, `observable_behavior`, id-vs-name | the only comparisons available |
| O9 | "may not exceed parent" on `effect_grants` = set inclusion | the only Delegation axis on which the comparison is defined at all |
| O10 | I17 chain = `grantor`/`derived_from` reaches a `Scope.authority_root_ref` | — |
| O11 | I18 "outside the governed activity" = not an `Attempt.actors` member of a governed/gated Unit | a different reading gives a different verdict on the same instance |

**Illustrative checks** (`--illustrative`, prefix `XX-`) implement bindings M01 **does not state**. They
exist to show what a stated rule would buy. Their firing is recorded in the CSV's
`illustrative_output` column and is **never** counted as model discrimination; those rows are
`accepted-defect`.

---

## 1. Headline result

**82 of 115 fixtures are refused by a checker generated from M01 alone. 18 are accepted, and nine of
those eighteen are cases where M01 states the rule, types the data on both sides, and simply never
writes the sentence that joins them.**

The pinned V5 discriminates its **structural** layer very well: types, enumerations, value
vocabularies, registry membership, reference targets, cardinalities and all nineteen declared inverses
are mechanically enforceable exactly as written. What it does not discriminate is concentrated in one
place and it is not random: **the Event layer, and the firewall that runs through it.** Everything
consequential — evidence, refusal, admission, independence, authority-in-use — is carried in
`Event.extension` (`type: map`, interior undefined), in `Event.subject_refs` (`type: list`, no element
type), or in a `rule:` string with no subject a checker can bind to.

| actual result | count | what it means here |
|---|---:|---|
| `rejected-mechanically` | **82** | a checker built from M01's typed declarations refuses it |
| `accepted-defect` | **18** | the instance violates a rule M01 states, and the checker admits it — **adverse** |
| `specified-not-enforced` | **5** | M01 states the constraint; no checker is constructible without inventing the rule |
| `not-falsifiable-from-alphabet` | **9** | M01 declares nothing the fixture could violate, or the property is temporal |
| `rejected-by-independent-judgment` | **0** | by discipline — see §0.3 |
| negative test (must **not** reject) | **1** | F-E16 passed: the checker correctly accepts it |

**Mechanical versus judgment.** Classified by the kind of check that *could* reject the fixture at all:
**89 mechanical · 26 judgment**. Cross-tabulated against outcome:

| expected check kind | rejected-mech. | accepted-defect | spec-not-enforced | not-falsifiable | negative |
|---|---:|---:|---:|---:|---:|
| mechanical | 78 | **9** | 0 | 1 | 1 |
| judgment | 4 | 9 | 5 | 8 | 0 |

The **9 mechanical x accepted-defect** cell is the finding. A judgment rule that a checker cannot reach
is expected and unremarkable. A rule whose *both operands are already typed* and which still cannot be
checked is a missing binding — cheap to fix, and adverse until it is.

Of the 82 mechanical rejections, 56 rest on `determined-by-M01` checks and 26 on a disclosed
operationalization (11 of those on O1 closure alone).

---

## 2. Adverse findings — the 18 accepted defects

Ordered by consequence. Each is a fixture in `artifacts/invalid-instance-matrix.yaml` with its checker
output in `artifacts/rejection-results.csv`.

### 2.1 The firewall is stated twice and bound nowhere — `F-E12`, `F-E13`  [ADVERSE]

`I9` — *"Proven requires evidence at the claim's own altitude, demonstrated by the organization"* — is
stated as an invariant, restated as `values.evidence_grade.rule`, and cited by both `Capability` and
`Gate`. It is carried by **no typed structure**:

- `Capability.evidence_record_refs` is `required: false`, and **no rule makes it conditional on
  `grade`**. `F-E12` sets `grade: proven` with the evidence list deleted; the checker accepts.
- `Record` declares `evidence_altitude: enum[directional,behavioral]`. **`Capability` and `Technology`
  declare no altitude at all.** `F-E13` proves a behavioral-shaped claim with a `directional` Record;
  the comparison I9 demands has only one typed side, so the checker accepts.

This is the garage's own load-bearing rule (`CLAUDE.md`: *status advances to `proven` ONLY on attached
real-artifact evidence*; D7). Nothing here says the firewall is wrong — it says a program instantiating
V5 as written gets **no help from the model** in holding it. The illustrative check
`XX-PROVEN-NEEDS-EVIDENCE` fires on `F-E12`, which is the point: a conditional requirement and an
altitude field on the claim side would make it mechanical without adding a construct.

### 2.2 The authority join is missing — `F-E17`, `F-E18`, `F-E19`, `F-H11`  [ADVERSE]

M01 declares `Delegation.effect_grants: list<ref<registry.effect_class>>` and the
`effect_request` extension key `requested_effect`. **Both are registry-typed values. No rule in M01
binds one to the other.** `F-E17` requests `credential-issue` under a Delegation that grants only
`repository-write`; the checker accepts. `F-E18` aims a request at an `EffectBoundary` whose
`effect_classes` do not include it; accepted. `F-E19` sets `can_refuse: false` on the boundary two
Delegations name as their enforcement — the field whose own definition reads *"a boundary that cannot
refuse enforces nothing"* — and **no rule in M01 reads that field**; accepted.

This is the one authority check that could have been *fully* mechanical from typed data on both sides,
and it is the one the model does not write. `I12` ("autonomy is not authority; only an EffectBoundary
disposition demonstrates enforced authority") and the `excluded` item *"autonomy as effect authority"*
are honoured in the **shape** (separate fields) and unenforced in the **values**.

### 2.3 Claim-versus-observation cannot be contradicted — `F-E06`  [ADVERSE]

`I4` — *"an actor-authored account is a claim or inference"* — is one of the separations
`separation_is_the_product` names, and review concern 4. `F-E06` labels a human-authored account
`epistemic_kind: mechanical-observation`, names the human as the `instrument`, and passes: `instrument`
is an untyped key inside `Event.extension`, so nothing joins it to `Actor.actor_type` — which is a
**typed enum**. Every ingredient exists; the join does not. What *is* enforced is key **presence**
(`F-E05` correctly rejects an observation missing `capture_custody`/`raw_evidence_ref`), so the
provenance clause of I4 has a foothold and the authorship clause has none.

### 2.4 Gate fail-closed and missingness — `F-E09`, `F-E11`

`I7` requires gates to fail closed when independence cannot be established. `F-E09` records
`independence_check: false` on the assessment and still issues a `pass` gate outcome; accepted —
`independence_check` is a map key and `Gate.independence_predicate` is free text. `F-E11` declares
`missingness: none` while the assessment's `evidence_set` is empty against a Gate that declares
eligible evidence; accepted — `Gate.eligible_evidence` is a **bare untyped `list`**.
Note the contrast with `F-E10`, which **is** rejected: deleting the `missingness` key breaks the
`required_extension`. So the model checks *that* missingness was declared and never *what* it says.

### 2.5 The `excluded:` list is re-openable through the registries — `F-E08`, `F-H09`, `F-H08`

The sharpest pair in the suite: `F-A17` sets `event_type: lesson` **unregistered** and is rejected
mechanically; `F-H09` **registers** `lesson` as an event type first and is accepted silently. The
difference is one registry write by exactly the program the exclusion is meant to bind. Likewise
`F-E08` registers `effect_completed`, an event type whose `required_extension` spans both the
`effect_request` and `effect_disposition` seeds — reintroducing the merged effect event that
`excluded` forbids and that R2's absence-detection argument was built to prevent. And `F-H08`
registers a `unit_kind` named `attempt`, reintroducing *Attempt as a Unit subtype*.

The exclusions that hold are exactly those carried by **type or closure**: `Goal as Scope` (`F-A28`,
`ref<Scope>`), and the seven excluded constructs (`F-H01`–`F-H07`, and only under O1). Those carried
by prose against a registry do not hold. `I19` — *"program extensions may not weaken common
invariants"* — is the invariant that guards every other invariant against the registries, and it is
the least checkable thing in the file (`F-E33`, `specified-not-enforced`). **S6 is the binding half of
the same problem** (§7).

### 2.6 Attenuation is undefined on two of its three axes — `F-E26`, `F-E27`  [ADVERSE]

`I17` says a derived Delegation *"may not exceed its parent on any axis."* Of the axes that exist:

- `effect_grants` — checkable as set inclusion (`F-E25` **rejected**, under O9).
- `autonomy_tier` — `values.autonomy_tier.values` is a **map of definitions with no declared order**.
  `F-E26` derives an **A5** Delegation from an **A1** parent and is accepted. A5 is
  `held_by: human` and defined as *"change Collective policy, authority structures or strategic
  objectives"*; A1 is bounded judgment inside one assigned Unit. The numbering *looks* ordinal and the
  model never says it is. This is `open.delegation_attenuation` ("comparison of non-numeric grants") at
  its sharpest, and it is the exact shape of the theme's stated boundary — *keep consequential
  authority outside the agents being governed*.
- `resource_ceiling` — `type: map`, interior undefined. `F-E27` derives `external_cost: 500` from a
  parent granting `0`; accepted.

The **chain** clause of I17 is a different story: it *is* traversable and checkable (`F-E28` rejected,
T-07 demonstrated). S4's "can the clauses fail independently?" test is vindicated here by execution
rather than by argument — one clause of I17 mechanizes and the other does not.

### 2.7 Common vocabularies with no typed carrier — `F-A15`, `F-A16`

`values.effect_disposition.rule` states explicitly that effect-disposition Events use
`[performed, refused, unknown]`. `F-A15` writes `maybe`; accepted, because the value lives inside
`Event.extension`. Worse, **`values.coupling` is referenced by no field anywhere in M01** — a declared
vocabulary reachable only as a key in an opaque map (`F-A16`, `eventual` accepted). Common **refusal**
vocabulary — the thing that lets absence be detected across programs — is unreachable by any checker.

Contrast `F-F02`, which **is** rejected: the `gate_outcome` seed's own `rule` spells out a multi-hop
resolution (assessment -> pinned `gate_version_ref` -> that Gate version's `allowed_outcomes`), and it
works. **The R2 addition is the only Event-layer *value* check in the entire model, and it
demonstrates the exact fix pattern the rest of the Event layer is missing.**

### 2.8 Supersession chains admit cycles — `F-E07`

`Event.supersedes`, `Record.supersedes` and `Workflow.supersedes` declare **no acyclicity**, though
M01 declares it three times elsewhere (`Scope.parent`, `Capability.composed_of`, `Unit.depends_on`).
`F-E07` makes an Event supersede itself; accepted. A correction chain that closes on itself erases the
history `I1` exists to protect. Cheap to fix; the model already knows how to say `acyclic`.

### 2.9 Effect custody is prose on the construct whose job is custody — `F-G02`

Three custody surfaces exist: `definition_custodian_ref` (`ref<Actor>` — typed, and the only one that
supports a check, §2.10), `Event.custody` (`text`) and `EffectBoundary.custody` (`text`).
`F-G02` states, in fully conforming typed-clean data, that the executing agent holds the boundary's
credentials. `EffectBoundary` has **no relation to any Actor**, so nothing can contradict it. The one
distinction `themes.md` calls load-bearing — *keep consequential governance and effect credentials
outside the governed activity* — is written in prose on the construct that exists to enforce it.

### 2.10 What custody *does* enforce

Reported for balance: `I18`'s first clause **is** checkable, and `F-E29`/`F-E30`/`F-E31` are all
rejected (under O11) — Workflow, Gate and Delegation custodians who are actors on the Attempts they
govern. That works **only** because `definition_custodian_ref` is `ref<Actor>` and `Attempt.actors` is
`ref<Actor>`. It is the model's clearest demonstration that a typed reference buys a check and a text
field buys nothing.

---

## 3. Model-level structural findings

From `v5_model_check.py` (full output in `artifacts/v5_model_check.out.txt`). These are properties of
M01 itself, not of any instance.

**Census (reproduces M02 §9):** core 7 · supporting 8 · registries 6 · catalogs 3 · invariants 19 ·
event types 9 · value vocabularies 8 · excluded 11 · open 11 · relations 57 · declared inverses 34
directed (19 unordered pairs) · **0 dangling relation targets** · **0 broken inverse declarations** ·
**0 unresolved `ref<registry.*>` / `ref<value.*>`**. Invariant binding: **19/19 cited, 15/15 constructs
cite at least one**. `extension_owner` on exactly the six constructs M02 §9 names. `form` on 15/15.

Four findings W3 believes are **new** (not in M02's S1–S8):

**N1 — `versioned: true` has no typed carrier anywhere.** Twelve constructs are `versioned: true` and
**not one declares a version field**. Three dependent rules require a version identifier the model
never provides: `Attempt.governed_by`'s rule *"pins immutable versions"*, the `assessment` extension's
`gate_version_ref`, and `I1`'s *"distinct from name and version"*. `F-E32` and `F-E24`'s O8 note carry
the consequence: I18's "changes are adaptation Events" is **not falsifiable** from instance data, and
the I16 check works only because W3's *encoding* supplied a version axis the model did not.

**N2 — 13 of 19 `extension_owner` keys name no field or relation on their own construct.** Bound:
`Unit.unit_kind`, `Event.event_type`, `Workflow.unit_kinds`, `Workflow.dependency_rules`,
`Gate.procedure`, `Gate.bar`. Unbound: `Capability.{behavior_schema, evidence_bar, classification}`,
`Unit.{states, transitions}`, `Record.{schema, admission, retrieval, lifecycle, correction}`,
`Workflow.states`, `Gate.{outcomes, consequences}`. R3's argument was **local checkability**; the
ownership is local and, for 13 keys, the extension point it names is absent (`F-F06`).

**N3 — four bare untyped `list` fields, and six `*_ref`/`*_refs` fields that are not ref-typed.**
Untyped lists: `Event.subject_refs`, `Record.provenance_refs`, `Workflow.dependency_rules`,
`Gate.eligible_evidence`. Ref-named but not ref-typed: `Unit.baseline_ref` (text),
`Attempt.baseline_ref` (text), `Record.author_or_source_ref` (text), plus the three above that are
lists. **`Event` declares no relation to `Delegation`, `EffectBoundary`, `Gate`, `Unit` or `Actor`
other than through `actor_refs`** — every other Event linkage lives in `subject_refs` (untyped) or
`extension` (opaque). This single fact explains most of §2 and most of §5's traversal limits.

**N4 — the `event_type` registry's own `gate_outcome` seed carries a key outside its declared shape.**
The shape is `{key, definition, required_extension, durable, status}`; the seed adds `rule:` — and
that key is precisely the R2 addition that makes `F-F02` (the model's only working Event-layer value
check) possible. So registry shape closure cannot be asserted without rejecting the model's own seed
(`F-C07`, `not-falsifiable-from-alphabet`). Not a defect so much as an undeclared shape extension the
model relies on.

Also confirmed mechanically: the three registries M01 seeds **empty** (`record_category`, `unit_kind`,
`effect_class`) make `Record.category`, `Unit.unit_kind` and `Delegation.effect_grants` — all three
`required: true` — **unsatisfiable until a program registers an entry**. No conforming instance of
Record, Unit or Delegation exists in V5 as published. That is by design (`extend_by_registration`) and
worth stating plainly: **V5 alone cannot represent anything; a program registry is a precondition.**

---

## 4. Where the model is genuinely strong

Reporting this because a rejection suite biased toward its own findings is worthless.

- **Every one of the 19 declared inverse pairs is enforceable and was individually falsified**
  (fixtures `F-B01`–`F-B19`, all `rejected-mechanically`), and every one was demonstrated in **both
  directions** on the conforming baseline (34 `demonstrated-both-directions` rows in
  `traversal-results.csv`). The post-A3 inverse discipline — declare an inverse only where it expresses
  domain navigation — costs nothing in checkability.
- **`I13` is the model's cleanest invariant**: stated as an invariant, carried by a `1..*` cardinality,
  and restated as a relation rule (*"no requiring Goal means no Capability"*). Three consistent
  expressions of one constraint; `F-E20` trips two checks at once.
- **`I10` holds by absence.** There is no relation from `Skill` to `Capability` or to any authority
  construct, so `F-E14`'s `Skill.proves -> Capability` is structurally unrepresentable (under O1).
- **`R4`'s correction has mechanical force**: `Event.authority_ref: ref<Delegation|Scope>` rejects a
  Role (`F-A30`), and the conditional requirement buried in its `definition:` string — *"required for
  decisions and effect requests"* — is checkable too (`F-F05`). A naive schema generator would miss
  the latter entirely, because the conditional is in prose rather than in `required:`.
- **`A8`'s orthogonality rule survives** where it is carried by a closed vocabulary: `F-A13` rejects
  `epistemic_kind: decision`, which is exactly the reappearance the rule exists to stop.
- **`Record.admitted_by`'s rule names an event type, so it is checkable** (`F-F04`). This is the
  discriminator across all of M01's relation rules: *a rule that names a registry key or a type is
  mechanizable; a rule that names a semantic property is not.*

---

## 5. Traversals

`artifacts/traversal-results.csv` — 67 rows: 34 `demonstrated-both-directions`, 18 `partial-proxy`,
8 `demonstrated-by-index`, 5 `equivalent-on-this-instance`, 2 `demonstrated`. **No new model relation
was added for any of them.**

### 5.1 Goal -> applicable Workflows — **query-layer hole**

`Workflow.applies_to -> Goal` is one-way; M02 §7 withdrew the back-pointer as "a query served by an
index." W3 tested both routes.

- **T-01, by index:** answered — `SYN-GO-1 -> {SYN-WF-A, SYN-WF-B}`. But the index is built by a **full
  scan of the Workflow extent**, and **M01 declares no index, no query layer, and no Scope bound on
  the scan.** `Workflow.owner_scope_ref` and `Goal.scope_ref` exist but no rule requires them to
  relate, so the scan cannot even be narrowed by Scope without inventing a rule.
- **T-02, by declared relations only** (`Goal.directs -> Unit.follows -> Workflow`): **both incomplete
  and unsound**, demonstrated on the baseline. Incomplete — `SYN-GO-1` returns only `SYN-WF-A`,
  missing `SYN-WF-B`, which *applies to* the Goal but governs no Unit yet. Unsound — `SYN-GO-2`
  returns `SYN-WF-A`, which governs a Unit the Goal directs but **never declared `applies_to`** that
  Goal. **M01 states no rule linking `Unit.follows` to `Workflow.applies_to`,** so the relation path is
  not a sound proxy in either direction.

**Verdict: `blocking/query-layer hole`.** M02 §7 explicitly recorded that once one-way relations are
legitimate, "the traversals that must work become a separate obligation list belonging to the
instantiation round." This round finds that the obligation is real and unmet by the model file: the
traversal is answerable *only* by brute force over an extent the model does not bound. Per the task's
own standard — *a scan that only works by brute force is itself the finding* — this is the finding.

### 5.2 Actor -> participated Attempts — **query-layer hole, with a partially sound declared path**

`Attempt.actors -> Actor` is one-way. W3 found that M01 **does** supply a forward path that needs no
new relation:

```
T-04  Actor.receives -> Delegation.governs -> Attempt                      (dynamic grants)
T-05  Actor.holds_role -> Role.receives -> Delegation.governs -> Attempt   (standing grants)
T-06  union of the two
```

This is a genuine and, W3 believes, under-noticed navigability result: `Role.receives` (added in V5 per
R5) is what makes the standing arm work at all. But the union is **incomplete**, and the baseline
demonstrates it: `SYN-AC-REVIEWER` is named in `SYN-AT-1.actors` and is the grantee of no Delegation,
so T-06 returns **nothing** while the index returns `SYN-AT-1`. **M01 declares no invariant tying
`Attempt.actors` to the actors reachable from `Attempt.governed_by`.** The delegation path answers
"which Attempts was this Actor *granted*", not "which Attempts did this Actor *participate in*" — and
the second is the question M02 §7 named. It can also over-reach (a co-grantee reachable through a
Delegation governing an Attempt they took no part in).

**T-03, by index:** answered, by a full scan of the Attempt extent. `Actor` carries **no `scope_ref`
at all**, so this scan cannot be narrowed by Scope even in principle. **Verdict: query-layer hole.**

### 5.3 Other required traversals

| id | traversal | result |
|---|---|---|
| T-07 | `Delegation.derived_from*` -> `grantor` -> Scope authority root | **demonstrated** for both baseline Delegations. The I17 *chain* clause traverses; the *attenuation* clause does not compare (§2.6). |
| T-08 | Delegation -> independent EffectBoundary disposition | **partial-proxy.** `Delegation.enforced_by -> EffectBoundary` is declared, but reaching the actual disposition requires `effect_disposition.extension.request_ref -> effect_request.extension.delegation_ref` — two hops **inside opaque maps**, over a full Event scan. Review concern 6 (connect a Delegation to an independent EffectBoundary disposition) is answerable **by convention, not by the model.** |
| T-09 | Gate -> assessments -> gate outcomes | **partial-proxy.** Works through `extension` keys; `gate_version_ref` names a Gate *version* that no field can resolve (N1). Review concern 7 — are assessment, outcome, decision, transition, request, disposition and Record *distinct and traversable*? **Distinct: yes**, all nine seeded event types are separately exercised in the baseline. **Traversable: only by convention.** |
| S2 form | `Gate.evaluates` <-> `Unit.gated_by` | **demonstrated**, and the qualified dotted inverse name **requires a resolver special case** — a resolver looking up a relation literally named `Unit.gated_by` finds nothing. The subset semantics work: the baseline deliberately gives `Gate.evaluates` a **Record** target as well, and the checker correctly requires no back-edge for it. |

---

## 6. Excluded constructs — negative dependency

The SCOPE requires each excluded construct to have either a negative test showing the instance does not
depend on it, or a pressure entry. All eleven are dispositioned; the conforming baseline is the
negative-dependency witness.

| excluded item | fixture | negative dependency demonstrated in the baseline |
|---|---|---|
| Feature | F-H01 rejected (O1) | change-shaped work carried by `unit_kind: change` |
| Qualification | F-H02 rejected (O1) | competence evidence as `Actor.has_skill` attributes |
| Envelope | F-H03 rejected (O1) | limits on `Delegation` fields |
| AuthorityBasis | F-H04 rejected (O1) | T-07 traverses `authority_root_ref` + `derived_from` |
| EvidenceItem | F-H05 rejected (O1) | evidence as Records — though both carriers are untyped (§2.4) |
| RecordVersion | F-H06 rejected (O1) | `Record.supersedes` — but see N1 |
| Signal/Decision/.../EffectReceipt | F-H07 rejected (O1) | all seven exercised as seeded event types (9/9 seeds used) |
| merged effect event | **F-E08 accepted-defect** | re-openable through the registry |
| Goal as Scope | F-A28 rejected (typed) | `Unit.scope_ref: ref<Scope>` |
| Attempt as Unit subtype | **F-H08 specified-not-enforced** | registrable as a `unit_kind` |
| lesson as Event type | F-A17 rejected / **F-H09 accepted-defect** | the pair in §2.5 |
| universal lifecycle / closed taxonomy | F-H10 not-falsifiable | verified against M01 directly: no construct declares a state enumeration; all 6 registries and 3 catalogs carry an `admission_rule` and `status: OPEN` |
| autonomy as effect authority | **F-H11 accepted-defect** | §2.2 |

---

## 7. Review obligations — S1–S8 and the changelog

### S1–S8 disposition

| id | W3 finding | falsifiable by W3? |
|---|---|---|
| **S1** scalar splits | **CLOSED at the pinned digest.** All six sites parse complete; a generic scan for the defect signature returns 0 hits file-wide. Independently re-confirmed with `yq`. | **yes — falsified (defect absent)** |
| **S2** dotted inverse `Unit.gated_by` | **CONFIRMED.** Still the only qualified inverse in the file; a bare-name resolver finds nothing and needs a special case. `notation` still does not document the qualified form (the fix M02 proposed). The *semantics* are sound and were demonstrated (§5.3). | **yes — confirmed** |
| **S3** `notation` gaps | **CONFIRMED and wider than reported.** Undocumented construct keys: `form`, `owner`, `extension_owner` (M02's three) **plus `definition`, `invariants`, `open`**. Additionally `Event.identity` is a **map** while `notation.identity` describes a scalar. `catalogs`' `scope` key is also undocumented (see F-D01/D03). | **yes — confirmed, extended** |
| **S4** atomicity | **CONFIRMED.** M02 named 7 remaining; W3's independent clause heuristic flags **13** of 19 (I1,I2,I3,I4,I5,I6,I8,I10,I11,I12,I15,I17,I18). The heuristic is judgment, but the *executed* evidence is decisive for I17: one clause mechanizes (F-E28) and the other does not (F-E26/27) — non-atomicity is not cosmetic, it hides that half a rule is unenforceable. | **partly — heuristic + one executed proof** |
| **S5** standing/dynamic discriminators | **CONFIRMED as an ambiguity, and it is worse than "undefined".** Under the enforced rule (`unit` absent means standing) a Role-granted Delegation naming a Unit is *dynamic*; under the definition it is neither. No fixture can be invalid, because **no rule renders the mixed case invalid or valid**. | **no — `not-falsifiable-from-alphabet`** |
| **S6** I19 bound to Workflow only | **CONFIRMED mechanically.** `extension_owner` is on 6 constructs; **5 of them do not cite I19** (Capability, Unit, Event, Record, Gate). §2.5's `F-E33` is the semantic half of the same gap. | **yes — confirmed** |
| **S7** `receives` asymmetry | **CONFIRMED and wider.** Three asymmetric inverse declarations, not one: `Actor.receives` (no inverse, while `Role.receives` declares `grantee`); `Actor.holds_role` (no inverse, while `Role.assigned_to` declares `holds_role`); `Skill.required_by` (no inverse, while both `Workflow.requires` and `Role.requires` declare `required_by`). Also `Skill.required_by` names **`Unit`** as a target and `Unit` carries no corresponding relation at all. | **yes — confirmed, extended** |
| **S8** no superseded markers | **CONFIRMED at the pinned digests.** `organizational-data-model-v3.yaml`: `supersedes_for_review` points **backward** to v2, nothing forward. `codex-organizational-data-model-v4.yaml`: **no supersession key at all.** `agentic-organization-data-model.md`: **none.** `organizational-data-model.yaml` (Claude track): `superseded_by` points at **v4, not v5** — so even the one marked file now misdirects. | **yes — confirmed** (requires the transitive sources in §9) |

### V5 changelog assertions (`changelog[0]`, version 5.0.0)

| assertion | verified |
|---|---|
| bound invariants to constructs | **TRUE** — 19/19 cited, 15/15 constructs cite at least one |
| bound extension ownership to constructs | **TRUE as a key list; PARTLY FALSE as a binding** — 13 of 19 keys name no field (N2) |
| restored `form` | **TRUE** — 15/15 |
| split `assessment` from `gate_outcome` | **TRUE**, and the split's rule is the model's only working Event-value check (F-F02) |
| Event authority corrected to Scope or Delegation | **TRUE** — `ref<Delegation\|Scope>`, enforceable (F-A30) |
| standing Delegations navigable from Role | **TRUE**, and load-bearing for traversal T-05 |
| **"completed semantic inverses"** | **OVERSTATED** — three asymmetric declarations remain (S7) |
| defined extension payload and effect disposition | **TRUE as declarations; both unenforceable** (§2.7) |
| Scope seeds conform | **TRUE** — all four now carry `required_fields` and `constraints` (both empty, so they constrain nothing: an invalid-Scope fixture on seed-declared required fields is **not constructible**) |
| RW1-D2 supersession recorded | **TRUE** — in both `changelog` and the registry's `admission_rule` |
| **"made independently testable invariants atomic"** | **OVERSTATED** — applied to the three named; 13 flagged by W3's heuristic, and S4 stands |
| inverse rule carried into `principles` | **TRUE** |

Two changelog claims are overstated. Neither is a fabrication — both describe work that was really
done — but both assert completion of a class where only the named instances were fixed.

### OPEN items — which are falsifiable at all

W4 owns the dispositions; W3 reports only what a rejection suite can and cannot reach. Falsifiable and
**exercised adversely**: `delegation_attenuation` (F-E26/27), `lesson_vs_pattern` (F-H09),
`event_identity_threshold` (partially — `Event.identity`'s conditional `required_when` is prose, so no
fixture can violate it), `capability_rollup` (F-E13's altitude gap is upstream of any rollup).
Falsifiable and **confirmed unresolved**: `skill_catalog` and `gate_identity` — both are worse than
"untested", because the three catalogs have **no instance-level attachment point at all** (F-D01,
F-D03: `Skill` and `Gate` carry no scope or catalog field; a record-category-scoped Gate, one of the
three declared catalog scopes, has no representation). **Not falsifiable by any instance:**
`custody_enforcement` (an absence), `workflow_promotion` (a governance question),
`collective_boundary` (succession is temporal), `autonomy_A3_A4` (an evidence question),
`semantic_compression` (a generality claim two cases cannot settle either way).

---

## 8. Limits — what W3 did **not** establish

- **No enforcement claim, anywhere.** Not for `wfh-008`, not for `vnc-045`, not for the garage. Every
  mechanical rejection here is a property of a checker W3 wrote from a YAML file.
- **No case coverage.** The baseline is synthetic and constructed from M01. It contributes **zero**
  rows to either case's coverage ledger. W1 and W2 own the historical instances.
- **No independent judgment.** W3 authored and ran everything in this file (§0.3).
- **No verdict on the seven-entity hypothesis.** That is W4's. W3 offers one observation toward it:
  **not a single accepted defect in §2 requires an eighth core entity.** Every one is a missing
  *binding* — a conditional requirement, a subset rule, an ordering, an acyclicity declaration, a
  field where prose now stands. That is `revise`-shaped evidence rather than `reject`-shaped evidence,
  and W4 should test that reading rather than adopt it.
- **The 18 accepted defects are not equally weighted.** §2.1, §2.2, §2.3 and §2.6 touch the firewall
  and the authority boundary the theme calls load-bearing; §2.7 and §2.8 are hygiene by comparison.
- **O1 (closure) carries 11 of the 82 rejections**, including every excluded-construct fixture. A
  program that reads V5 open-world loses all of them. M01 never states closure; that silence is worth
  a sentence in any successor, and W3 is not authorized to write it.
- **`vnc-045-instance.yaml` (W2) appeared on disk mid-run** and was inspected for **encoding shape
  only** (§9, T-06). Observation recorded without adopting any W2 conclusion: W2's encoding
  (`scopes:`/`goals:`/`registry_extensions:` ...) and W3's (`instances:`/`registered:`) are **different
  serializations of the same model**, because **M01's `notation` describes the model file and never
  describes an instance document.** W4 must reconcile across two encodings; that reconciliation cost
  is itself a finding about the model, not about either workstream.

---

## 9. Alphabet and transitive-source ledger

**M alphabet used:** `M01` (parsed, digest verified) · `M02` (S1–S8, R1–R5/A1–A10, §7 traversal
obligation, §9 sanity — all consumed) · `M06` `themes.md` `theme:workflow-harness` block (lens,
load-bearing boundary, coordinator envelope) · SCOPE and its three append-only extensions.
`M03`/`M04`/`M05` (`wfh-010` scope, findings, coverage reports): **inspected-not-materially-consumed** —
W3's suite is a model/rejection test derived from M01, and importing `wfh-010`'s conclusions would
contaminate the independence W4 needs. **R and S alphabets: deliberately not consumed** — W3 was
directed to derive baselines from M01, and consuming case material would risk encoding history into
fixtures, which the SCOPE amendment forbids.

**Transitive sources added (grep/existence only, no content adopted):** required to verify S8, which is
a claim about files outside M01–M06.

| id | path | reason | provenance |
|---|---|---|---|
| T-01 | `product/factory/proposals/organizational-data-model-v3.yaml` | S8 — does it point to V5? | tracked at commit `6718049`; sha256 `faad526c...5da0ed`, matches the SCOPE extension |
| T-02 | `product/factory/proposals/codex-organizational-data-model-v4.yaml` | S8 | sha256 `c5db5c3f...8ebb1fb`, matches |
| T-03 | `product/factory/proposals/agentic-organization-data-model.md` | S8 | sha256 `cb9d319f...1aac302`, matches |
| T-04 | `product/factory/proposals/organizational-data-model.yaml` | S8 | sha256 `1f80e42b...4edca44a23`, matches |
| T-05 | `product/factory/proposals/target-concept-v1.md` | named in `M01.meta.derivation`; **existence and digest only, content not read** | sha256 `893952df3a84f132346c412a89811c334408a1ebbf432a793eba3e1b50a30b75` |
| T-06 | `product/research/wfh-011/artifacts/vnc-045-instance.yaml` | in-flight W2 output; **top-level encoding shape only**, no conclusion adopted | produced by W2 during this run |

**W1/W2 concurrency, recorded as required.** At W3's start (02:05Z) `wfh-008-instance.yaml`,
`vnc-045-instance.yaml`, `findings-W1-research-instance.md` and `findings-W2-software-instance.md` were
**all absent**. At W3's finish, `vnc-045-instance.yaml` and `vnc-045-counterfactual-instance.yaml` were
present and `wfh-008-instance.yaml` was still absent. W3 blocked on neither, derived its baseline from
M01, and adopted no W1/W2 conclusion.

---

## 10. Artifacts

| path | contents |
|---|---|
| `product/research/wfh-011/findings-W3-rejection-suite.md` | this file |
| `product/research/wfh-011/artifacts/invalid-instance-matrix.yaml` | 115 fixtures, each a minimal mutation with expected rejecting check |
| `product/research/wfh-011/artifacts/rejection-results.csv` | 115 rows with actual results and raw checker output |
| `product/research/wfh-011/artifacts/traversal-results.csv` | 67 traversal rows |
| `product/research/wfh-011/artifacts/w3-baseline-instance.yaml` | conforming synthetic baseline (0 findings) |
| `product/research/wfh-011/artifacts/v5_model_check.py` + `.out.txt` | model-level structural checker and raw output |
| `product/research/wfh-011/artifacts/v5_instance_check.py` | instance validator + traversal engine |
| `product/research/wfh-011/artifacts/gen_inverse_fixtures.py` | regenerates matrix section B |
| `.../baseline-validate.out.txt`, `rejection-suite.out.txt`, `traversal.out.txt` | raw run output |

---

## Citations

- `{type: docs, ref: product/factory/proposals/organizational-data-model-v5.yaml, title: "Organizational Data Model V5 (pinned, sha256 bf8e5536...9841060)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: product/factory/proposals/codex-organizational-data-model-v4-review.md, title: "Review — codex-organizational-data-model-v4.yaml, incl. section 9 V5 sanity check S1-S8", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: product/research/wfh-011/SCOPE.md, title: "wfh-011 — Organizational data-model instantiation and rejection test", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: product/factory/themes.md, title: "Standing research themes — theme:workflow-harness", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: product/factory/proposals/organizational-data-model-v3.yaml, title: "Organizational Data Model v3 (S8 transitive source T-01)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: product/factory/proposals/codex-organizational-data-model-v4.yaml, title: "Codex Organizational Data Model V4 (S8 transitive source T-02)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: product/factory/proposals/agentic-organization-data-model.md, title: "Agentic Organization — Data Model (S8 transitive source T-03)", org: "arch-research garage", year: 2026}`
- `{type: docs, ref: product/factory/proposals/organizational-data-model.yaml, title: "Organizational Data Model — Claude track (S8 transitive source T-04)", org: "arch-research garage", year: 2026}`
- `{type: repo, ref: https://github.com/yaml/pyyaml, title: "PyYAML 6.0.3 — the only dependency of the W3 checkers", year: 2026}`
