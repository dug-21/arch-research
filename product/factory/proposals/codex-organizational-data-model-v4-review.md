# Review — codex-organizational-data-model-v4.yaml

**Reviewer:** Claude track (theme-coordinator, workflow-harness)
**Subject:** `product/factory/proposals/codex-organizational-data-model-v4.yaml` @ 2026-08-29
**Purpose:** input to **v5**. The converged line continues on the Codex track; the Claude track
(`organizational-data-model.yaml`) is marked superseded and retained for lineage only.
**Supersedes:** the review of `organizational-data-model-v3.yaml`, whose findings are dispositioned in §1.
**Method:** mechanical validation (parse · relation targets · inverse symmetry · invariant binding ·
registry/value reference resolution · seed conformance · v3→v4 key diff) plus a semantic pass against the
gated wfh-010 rulings, the owner's corrections of 2026-08-28/29, and `target-concept-v1.md`.

**Verdict:** a large step forward. v4 closed four of five blocking defects and most of the high and medium
ones, and the model is now structurally sound: 7 core · 8 supporting · 6 registries · 3 catalogs ·
16 invariants · 8 event types. It parses clean with no dangling targets and no broken inverse declarations.

**But v4 introduced four regressions, one of them serious**, and they are all losses of *binding* — the
model still says the right things, and says less about which construct each thing applies to. Fix those
and v5 is the first version I would put in front of an instantiation test.

---

## 1. Disposition of the v3 review

| v3 finding | v4 |
|---|---|
| **B1** extension-weakening invariant dropped | **Fixed** — `I16` |
| **B2** Skill re-admits "reusable method" | **Fixed** — "Competence, never Capability, authority or Workflow" |
| **B3** no attenuation; standing/dynamic unrepresentable | **Fixed** — `Delegation.derived_from`, `unit` absent/present rule, `I14`, `delegation_template` removed |
| **B4** `autonomy_tier` on both Role and Delegation | **Fixed** — Delegation only (but see R5) |
| **B5** Record has no admission link | **Fixed** — `Record.admitted_by` |
| **H1** orphan invariant `I13` | **Regressed** — see R1; all 16 are now orphaned |
| **H2** invariants not atomic | **Partly fixed** — `I10`, `I12`, `I13` still bundle two or three rules each |
| **H3** firewall not an invariant | **Fixed** — `I9` |
| **H4** `Goal.directs` / `Unit.goals` duplicate | **Fixed** — single relation with `directed_by` inverse |
| **H5** one-way `delivered_by` / `is_advanced_by` | **Fixed** — `Capability.advances`, `Unit.delivers` |
| **H6** `coupling` / `disposition` undefined | **Partly fixed** — `coupling` and `currentness` now in `values`; `disposition` and `outcome` still undefined |
| **H7** `carrier` dropped | **Fixed** — field and vocabulary restored |
| **M1** scope_type openness departs from gated RW1-D2 | **Open** — still not recorded as a supersession |
| **M2** scope_type seeds do not conform to their shape | **Open** — all four still omit `required_fields`, `constraints` |
| **M3** Attempt disposition free text | **Fixed** — typed, plus `resume_requirements` |
| **M4** Capability classification dropped | **Fixed, and better** — `registry.capability_classification` with a `dimension` key |
| **M5** `Scope.owns` duplicates `scope_ref` | **Fixed** — removed |
| **M6** stale `supersedes_for_review` | **Fixed** — `derivation` now names both tracks |

---

## 2. Regressions introduced in v4

### R1 — Every invariant is now unbound  *(blocking)*
v3 cited invariants per construct (`Goal: [I3]`, `Gate: [I9,I10,I12]`, …). v4 removed the `invariants:`
key from **all fifteen** constructs. Sixteen invariants now float free.

The v3 review flagged one orphaned invariant. v4 resolved that by orphaning all of them. Nothing now tells
a reader looking at `Delegation` which rules constrain it, and nothing tells a future checker which
constructs to evaluate a given invariant against. This is the single largest loss between the two versions
and it undoes the property that made the invariant list worth numbering.
**Fix:** restore `invariants: [...]` on every construct. Every invariant should be cited by at least one
construct, and every construct should cite at least one invariant — both are mechanically checkable.

### R2 — `assessment` and `gate_outcome` re-merged  *(high)*
v3 correctly split them. v4 folds the terminal outcome back into the `assessment` extension
(`outcome, missingness, consequence_disposition`) and drops `gate_outcome`.

I originally argued for this merge and then **conceded the split was right**, because it is the same
absence-detection argument that justifies keeping `effect_request` and `effect_disposition` apart — which
v4 still correctly does, and lists in `excluded`. The concrete failure: an assessment that begins and is
abandoned, or that fails closed under `I7` before any verdict can be issued, has no outcome. With `outcome`
required in the assessment extension, that event cannot be written at all, so an abandoned or
fail-closed assessment leaves no trace and is indistinguishable from an assessment that never started.
**Fix:** restore `gate_outcome` as its own event type referencing the assessment, exactly as v3 had it.
Merging assessment with its outcome while splitting request from disposition is internally inconsistent —
the model should apply one rule to both.

### R3 — `extension_owner` removed from every construct  *(high)*
v3 carried `extension_owner` on Capability, Unit, Event, Record, Workflow and Gate. v4 drops it entirely,
leaving ownership expressed only by `owner:` on supporting definitions and by the `program_ownership`
principle in prose. The core entities no longer say who may extend them.

This matters more in v4 than it did in v3, because v4 has six open registries and a construct admission
bar. "Who may extend what" is the load-bearing half of *agents cannot change the rules*; in prose it is a
statement of intent, per-construct it is a check.
**Fix:** restore `extension_owner` on the constructs that have extension points.

### R4 — `Event.authority_ref` reverted to the weaker form  *(medium)*
v3 had `ref<Delegation|Scope>`. v4 has `ref<Delegation|Actor>` — the Claude track's version, which that
track's own comparison identified as the worse of the two. Authority is rooted in a **Scope**, whose
`authority_root_ref` then names the Actor; pointing an Event's authority directly at an Actor bypasses the
root and weakens `I14`'s chain.
**Fix:** revert to `ref<Delegation|Scope>`.

### R5 — `Role` promises latitude no field carries  *(medium)*
Removing `autonomy_tier` from Role was correct (v3 B4), but Role's definition still reads *"a reusable
organizational responsibility with required Skills and **permitted decision latitude**."* No field or
relation on Role now carries latitude, and Role has no link to the standing Delegation that would.
**Fix:** either state in the definition that latitude reaches the Role through its standing Delegation, or
add `receives: {target: Delegation, cardinality: "0..*"}` so a Role's standing grant is navigable. As
written, a standing Delegation to a Role is reachable from the Delegation but not from the Role.

---

## 3. Remaining

| ID | Finding | Fix |
|---|---|---|
| **A1** | `Skill` has no `held_by` inverse for `Actor.has_skill`. From a Skill you cannot see who holds it — the first question a shared skill catalog must answer, and the catalog is already declared in `catalogs:`. | Add `held_by` with the evidence/grade/currentness attributes. |
| **A2** | `Workflow.requires` and `Role.requires` do not declare `inverse: required_by`, though `Skill.required_by` exists. Same for `Unit.gated_by` against `Gate.evaluates`. Back-pointers exist but are undeclared, so nothing binds them. | Declare the inverses. |
| **A3** | `Workflow.applies_to → Goal` and `Attempt.actors → Actor` have no back-pointer at all. "Which methodologies pursue this Goal" and "what has this Actor worked on" are unanswerable. | Add inverses or mark one-way with a reason. |
| **A4** | `disposition` and `outcome` are required by event extensions but defined nowhere in `values`. `effect_disposition` needs `performed \| refused \| unknown`; assessment/gate outcomes are Gate-owned by design and should say so explicitly rather than be silently absent. | Define the effect disposition vocabulary; note that outcome vocabularies come from each Gate's `allowed_outcomes`. |
| **A5** | `scope_type` seeds omit the `required_fields` and `constraints` their own shape declares — a validator would reject the file's own examples. | Populate, or narrow the shape. |
| **A6** | Making `scope_type` registry-extensible supersedes wfh-010 RW1-D2, which fixed the set at exactly four. The change is defensible; the silence is not. | Record the supersession in `changelog` and in the registry's `admission_rule`. |
| **A7** | `I10`, `I12` and `I13` still bundle two or three rules each. A checker cannot report which clause failed. | One rule per id. |
| **A8** | `epistemic_kind` lost its orthogonality rule (*independent of Event type, significance, authority and carrier*). That statement is the whole reason the axis exists — it is what stops `decision` reappearing as an epistemic kind. | Restore the rule line. |
| **A9** | `payload` and `extension` are both on Event, `extension` required. The distinction between them is unstated. | Define both, or drop `payload`. |
| **A10** | `form:` was dropped from every construct. Low severity — Event's definition carries it in prose — but it was what stopped the "noun or occurrence" argument recurring. | Restore, or note the omission is deliberate. |

---

## 4. Do not change these

`construct_admission_bar` · the `effect_request` / `effect_disposition` split · six registries with
per-registry `admission_rule` · `catalogs:` · `EffectBoundary` naming · `Delegation.derived_from` with the
standing/dynamic rule and `I14` · `Attempt.resume_requirements` · `registry.capability_classification`
with its `dimension` key, which is better than the fixed enum either track carried · `I16` ·
`Record.admitted_by` · `small_core` framed as *"a hypothesis to test, not a fixed ceiling."*

That last line is the right posture and should survive into v5 unchanged.

---

## 5. Mechanical appendix

Parses clean · 7 core · 8 supporting · 6 registries · 3 catalogs · 16 invariants · 8 event types.
No dangling relation targets. No broken inverse declarations. All `ref<registry.X>` and `ref<value.X>`
resolve.

| Check | Result |
|---|---|
| Invariant binding | **0 of 16** cited by any construct |
| `extension_owner` | present on 6 constructs in v3, **0** in v4 |
| `form` | present on 15 constructs in v3, **0** in v4 |
| Registry seed conformance | 4 failures, all `scope_type` |
| Undefined vocabulary | `disposition`, `outcome` |
| One-way relations | 11 flagged; 3 material (A1, A3), 4 declaration-only (A2), 4 acceptable as one-way |

Reproduce with the checker used for this review: parse, resolve every relation target and declared
inverse, resolve every `ref<registry.*>` / `ref<value.*>`, diff construct keys against v3, and assert
that invariant citation is non-empty in both directions.

---

## 6. Standing caveats — unchanged

- **Workflow remains ungated.** Authored, not adjudicated by wfh-010, which referenced `workflow_ref` and
  never defined it. `open.workflow_promotion` correctly says so.
- **`I14` and `I15` have no enforcement point** anywhere in the garage today. Attenuation and custody are
  claims about intended behavior, checkable only against instance data.
- **Semantic compression remains plausible, not proven.** Two owner-operated programs, read-only, never
  instantiated. Nothing in v4 or v5 changes that until a representation is built and something external
  rejects a non-conforming case.

---

## 7. Disposition — agreed with the Codex track, 2026-08-29

**Accepted for v5:** R1–R5 and A1, A2, A4–A10.

**A3 — withdrawn by the reviewer.** The finding was method bias, not a defect. The checker used for this
review flags every one-way relation, which encodes "all relations must be navigable from both ends" — a
property of what was cheap to implement, not a modeling principle. The Codex track's rule is adopted
instead, and belongs **in the model file**, not only in this review:

> Declare an inverse when it expresses meaningful domain navigation or constrains both sides — not merely
> because someone might query backward.

Under that rule: `Skill.held_by` stands (possession is an attributed domain relation);
`Workflow.requires ↔ Skill.required_by`, `Role.requires ↔ Skill.required_by` and
`Gate.evaluates ↔ Unit.gated_by` stand (both constructs already model the relationship);
`Actor.participated_in_attempts` and `Goal.pursued_by_workflows` are withdrawn — they are queries served
by an index. The review checker is corrected to report one-way relations as informational.

**Consequence to carry forward:** once one-way relations are legitimate, the schema stops being a complete
statement of what an implementation must support. The traversals that must work become a separate
obligation list belonging to the instantiation round. Recorded here so it is not discovered there.

**A7 — reviewer's phrasing superseded.** "One rule per id" is replaced by the Codex track's test: *can the
clauses fail independently?* Sharper, and it still splits `I10`, `I12` and `I13`.

**R3 — per-construct, limited to the six constructs with actual extension points.** A central mapping is a
second place to drift, and the model's own `separation_is_the_product` logic puts ownership with the thing
owned. Local checkability was the point of the finding.

**R2 addition.** When `gate_outcome` is restored, state in its registry entry that its outcome vocabulary
resolves through the assessment's pinned `gate_version_ref`. Both remain Event types; no noun is added.

**Also agreed:** drop `Event.payload`, retain `extension` only (A9).

---

## 8. Coordinator note — where review stops

With the above applied, v5 is structurally clean, internally consistent, and still never tested against a
single instance. Every version so far was improved by argument, and the arguments were sound — but they are
two readers reasoning about the same two histories. The return on a further review round is now below the
return on encoding `wfh-008` and `vnc-045` as instance data and observing what will not fit.

**v5 should be the last version produced by review.** After it, only an instance can find a real defect.
wfh-010 remains open until then, and the instantiation round — not a sixth model revision — is the next
bounded question worth scoping. That round leaves the current read-only directional envelope and requires
an owner-approved scope extension.

---

## 9. Sanity check — organizational-data-model-v5.yaml, 2026-08-29

**Result: v5 lands the agreed disposition in full.** Verified mechanically: 19/19 invariants cited, every
construct cites at least one; `extension_owner` present on the six constructs with extension points; `form`
restored on all fifteen; `gate_outcome` split out with its vocabulary-resolution rule; `authority_ref`
corrected to `ref<Delegation|Scope>`; `Role.receives` and `Skill.held_by` added; `effect_disposition`
vocabulary defined; `scope_type` seeds conform; the RW1-D2 supersession recorded in the registry's
`admission_rule`; the inverse rule carried into `principles`; `payload` dropped. Withdrawn A3
back-pointers correctly absent. Parses clean, no dangling targets.

Eight findings remain. One must be fixed before the file can be used by a machine.

### S1 — Six values are silently split by YAML  *(must fix)*
Unquoted flow-mapping values containing a comma are parsed as additional keys, so the file **reads**
correctly and **parses** wrong. Definitions are truncated at the first comma:

| Location | Parses as | Stray key created |
|---|---|---|
| `event_type.effect_disposition.definition` | `"EffectBoundary performs"` | `refuses or cannot determine a request` |
| `event_type.adaptation.definition` | `"authorized change to a definition"` | `composition or method` |
| `values.autonomy_tier.A0.definition` | `"analyze"` | `evaluate or recommend without discretionary work initiation` |
| `values.autonomy_tier.A3.definition` | `"adapt local tactics"` | `composition or reversible method detail` |
| `values.autonomy_tier.A5.definition` | `"change Collective policy"` | `authority structures or strategic objectives` |
| `Attempt.fields.resume_requirements.definition` | `"baseline"` | `unresolved residue and next admissible transition` |

`A0` currently parses as "analyze" — the clause that makes A0 *non-initiating* is gone. `A5` loses
"authority structures or strategic objectives," which is the reserved-authority definition.
**Fix:** quote each value or use a block scalar. **Inherited, not introduced by v5** — v4 has the same six
and v3 has five. Recommend a whole-file scalar-integrity pass, not six spot fixes.

### S2 — `Gate.evaluates` declares a dotted inverse  *(should fix)*
`inverse: Unit.gated_by`. Every other inverse in the file is a bare relation name, so a resolver looking
up a relation named `Unit.gated_by` on the target finds nothing. The intent — an inverse that applies only
to the Unit subset of a multi-target relation — is legitimate and worth keeping.
**Fix:** document the qualified form in `notation`, or express it as a bare name plus the existing
subset rule.

### S3 — `notation` does not document three keys it uses  *(should fix)*
`form`, `owner` and `extension_owner` appear on constructs throughout but are absent from `notation`,
which v3 documented.

### S4 — Atomicity was applied where flagged, not as a rule  *(should fix)*
`I10`, `I12` and `I13` were correctly split — those were the three named in the review. Seven invariants
still carry clauses that can fail independently: **I1** (opaque identity · history never overwritten),
**I4** (capture provenance · authored account is claim-or-inference), **I5** (immutability · correction is
a new Event · occurrence ≠ truth), **I12** (autonomy ≠ authority · only a boundary disposition
demonstrates), **I15** (identity survives rework · each execution is an Attempt), **I17** (attenuation ·
authority reaches an Actor through a chain), **I18** (custody sits outside · changes are adaptation
Events). Applying the agreed test — *can the clauses fail independently?* — splits all seven.

### S5 — Standing versus dynamic has two discriminators that can disagree  *(decide)*
`Delegation.definition` says *standing when it names a Role and no Unit; dynamic when it names an Actor
and a Unit* — two conditions — while the only enforced rule is on `unit` (*absent means standing*). A
Delegation whose grantee is a Role **and** which names a Unit is undefined. Raised by the track that
proposed the construct.
**Fix:** state `grantee = Role ⟺ unit absent` as the rule, or define the mixed case and say what it means.

### S6 — `I19` is bound to Workflow only  *(decide)*
*Program extensions may not weaken common invariants* is cited by `Workflow` alone, which reads as a
Workflow concern. It is a model-level constraint over every construct carrying `extension_owner`.
**Fix:** cite from all six, or mark it model-level and exempt it from the per-construct binding rule.

### S7 — `receives` is handled asymmetrically  *(minor)*
`Role.receives` declares `inverse: grantee`; `Actor.receives` declares none, though both are the inverse
of the same `Delegation.grantee` relation.

### S8 — Five model files, no superseded markers  *(hygiene)*
`organizational-data-model-v3.yaml`, `codex-organizational-data-model-v4.yaml` and
`agentic-organization-data-model.md` carry no pointer to v5. Only the Claude track file is marked.
Someone will read the wrong file.

### Reviewer's own defect, recorded
The Claude track file has **40** split scalars — the worst of the four — because its `invariants:` block
used flow mappings whose sentences contain commas, shredding nearly every invariant. The checker used in
the v4 review reported that file "integrity clean," because it validated structure and never validated
scalars. This class of defect is invisible to reading and to a structural checker, and it is the sharpest
available argument for the instantiation round: a model that reads correct and parses wrong is only
caught by something that consumes it.
