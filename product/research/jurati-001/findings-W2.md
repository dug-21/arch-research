# jurati-001 — W2 findings: smallest shared decision-language semantic model

**Status:** provisional pending W1 corpus freeze · **Date:** 2026-08-07

## Finding

The smallest model supported by the clearly identified development material is a **closed blocking
conjunction over four-valued clause results, followed by a total verdict-to-action function**. It needs no
general expression language and no domain-specific verdict semantics.

The shared kernel is:

1. an immutable, digest-bound question and admissible evidence set;
2. stable atomic clauses typed `mechanical`, `semantic`, or `human_reserved`;
3. `demonstrated | contradicted | not_demonstrated | insufficient_evidence` per clause;
4. blocking versus advisory criticality;
5. a conservative total reducer;
6. exactly one predeclared transition for every verdict; and
7. a judge allow-list/quorum/escalation policy whose output is only clause results.

`shd-007` supplies the decisive counterexample to evidence-weighted scoring: multiple strong clauses did
not compensate for one unmet trailing condition. `wfh-002` supplies the decisive distinction between
assessment and authority: a useful body of findings could coexist with no proof advancement, and an
out-of-scope architecture choice could not bind the successor merely because an assessor made it.

## Determining constraints

- **Monotone safety:** adding evidence for one clause cannot turn another blocking
  `not_demonstrated`/`contradicted` clause into advancement.
- **Question integrity:** changing the question, evidence set, rubric, or transition creates a new revision;
  it cannot happen inside a judge response.
- **Consequence closure:** a judge never emits a next action. Accepted clause results determine one verdict,
  and the contract determines one action.
- **Abstention is semantic data:** disagreement, missing admissible evidence, and exhausted escalation return
  `insufficient_evidence`; they are not coerced into failure or a guess.
- **Authority is a second check:** deterministic action selection does not authorize execution.

## Directional verdict

**Promising but not yet a cross-domain result.** The two identified episodes fit one compact kernel without
bespoke reduction logic. This moves structure only. Expressibility, transition completeness across the
corpus, and the claim that the kernel is “smallest” remain contingent on W1's development partition and
ambiguity adjudications.

## Flags and dependencies

- **BLOCKED ON W1:** frozen development episode IDs, exact evidence paths/digests, clause/reference labels,
  and ambiguity rulings. Placeholder hashes in the examples are not evidence-integrity proof.
- **Potential language expansion:** W1 may expose genuine disjunction, numeric aggregation, temporal
  windows, or multi-stage owner intervention. Add a primitive only when at least two development episodes
  need it; otherwise encode it as a typed mechanical checker or record the episode unexpressible.
- **Transition vocabulary risk:** `partial` is a grade/state in `shd-007`, while `not_demonstrated` is the
  decision verdict here. The transition target may record `partial`; the two must not be collapsed.
- **Historical-label risk:** `wfh-002`'s owner-directed close is not generic `FAIL`. W1 adjudication must
  distinguish proposition verdict from workflow action.
- **No holdout contact:** this work used no W1-designated calibration or sealed-holdout examples.

## Outputs

- `SPEC-v0.1-dev.md` — normative provisional semantics.
- `EXAMPLES-v0.1-dev.md` — two structurally validated development examples and validation limits.

## Citations

- type: docs · ref: `product/research/jurati-001/SCOPE.md` · title: "jurati-001 — Validated probe: a decision-contract language for deterministic next action" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/shd-007/REPORT.md` · title: "shd-007 — REPORT" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-002/REPORT.md` · title: "REPORT — wfh-002 (close-out)" · org: arch-research garage · year: 2026
- type: docs · ref: `product/factory/proposals/jurati-evolved-vision-2026-08-05.md` · title: "Jurati — evolved vision: a phase-aware queen for governed agent work" · org: arch-research garage · year: 2026
