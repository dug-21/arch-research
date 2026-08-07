# W1 findings — corpus and reference adjudication v0.2

This version supersedes the v0.1 selector reading at commit `f1fbfa8` and incorporates the independent
review in `reports/corpus-review.md` without inspecting sealed holdout verdict summaries.

## Directional result

A cross-domain corpus is feasible from repository artifacts, but it is **not ready to freeze**. The
candidate manifest reaches the requested minimums (32 SDLC decisions and 13 garage decisions), includes a
complete mature chain and a bug-fix gate, contains rework and owner-corrected firewall cases, and separates
cycles across development/calibration/holdout. Independent review corrected five post-rework PASS labels,
replaced provisional or mismatched garage decisions, added scope approval, and required action provenance.

The determining constraint is not document availability. It is whether an independent reviewer can recover
the exact historical question and next action without silently treating a report's summary as ground truth.
Rework reports and research directional decisions are the highest-risk strata.

## What is demonstrated

- The pinned Unimatrix tree contains 232 feature-cycle directories and the expected gate/report families.
- The selected corpus can satisfy the SDLC minimum of 30 decisions/15 cycles and garage minimum of 12
  decisions while keeping cycles partition-exclusive and contributions at three or fewer.
- `vnc-047` supplies a complete source chain while yielding three bounded decisions.
- `shd-007` supplies the required false-advancement control: the owner's ruling prevented a strong but
  clause-incomplete artifact from advancing C1 to `proven`.
- Domain B now includes explicit scope-approval episodes and no longer scores `wfh-002`'s provisional
  Option C or `wfh-004`'s unresolved omnibus triage as binding decisions.
- Every visible row distinguishes explicit, observed, inferred, and prescribed action provenance; no
  inferred action remains in v0.2.
- Holdout labels can be physically separated from judge-facing packets; D15 requires those generated
  datasets and extraction code to live on `research/jurati-001`.

## What remains claimed or blocked

- Rows still marked `review`, including B-C03, need independent adjudication.
- Holdout identities, paths, outcomes, and actions are absent from v0.2 main-visible metadata; opaque IDs
  are not proof until a restricted mapping is generated and checked.
- Final manifest/split/packet hashes do not exist until generated artifacts are created on the executable
  branch.

## Corpus-freeze gate recommendation

**Do not approve yet.** Residual blockers are exactly: (1) independently adjudicate remaining `review`
rows; (2) generate integrity-addressed packets, labels, split data, and restricted opaque-to-real holdout
mapping on `research/jurati-001`; (3) demonstrate fail-closed digest, action-provenance, partition, cap, and
holdout-leakage tests; (4) record W2–W5 non-inspection attestations; and (5) publish only aggregate holdout
counts plus final manifest/label/packet/split/mapping hashes on main.

## Artifacts

- `corpus/manifest.md` — candidate selection and provenance
- `corpus/evidence-packets.md` — extraction contract and special-case packet rules
- `corpus/reference-labels.md` — label algebra and accepted anchors
- `corpus/ambiguity-register.md` — unresolved adjudications
- `corpus/splits.md` — cycle assignments and hash policy

## Citations

- type: repo · ref: `https://github.com/dug-21/unimatrix/tree/7ac778dfe3aa352d475dddc7897384191419ddf8/product/features` · title: `Unimatrix feature-cycle corpus` · org: `dug-21` · year: 2026
- type: repo · ref: `https://github.com/dug-21/arch-research/tree/5d4ccdd92cac1ee0b13fd3c7aaa207e9720059de/product/research` · title: `Research garage run corpus` · org: `dug-21` · year: 2026
- type: docs · ref: `product/research/shd-007/REPORT.md` · title: `shd-007 REPORT — owner firewall ruling` · org: `arch-research garage` · year: 2026
- type: docs · ref: `product/research/wfh-002/REPORT.md` · title: `wfh-002 REPORT — boundary failure and disposition` · org: `arch-research garage` · year: 2026
- type: docs · ref: `product/research/jurati-001/SCOPE.md` · title: `jurati-001 validated probe scope` · org: `arch-research garage` · year: 2026

No Unimatrix writes were made. Research changes structure only; nothing here establishes `proven` status.
