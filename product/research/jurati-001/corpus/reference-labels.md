# Reference-label policy and development labels

The historical report is evidence, not unquestionable truth. A label is accepted only when the record
supports both the verdict and the exact action that actually followed.

## Label record

`episode_id`, bounded clause results, verdict, exact next action, source references, owner intervention,
adjudication state (`accepted | accepted-owner | review | excluded`), reviewer identity, rationale, and
adjudication timestamp.

## Deterministic normalization

- `PASS` maps to an advance action only when the report identifies the next gate/phase and no blocking
  finding remains.
- `PASS (WARN)` retains advisory clauses; warnings are not discarded merely because advancement occurred.
- `FAIL`, `BLOCK`, or a required rework maps to the named rework action, never to generic `stop`.
- `insufficient evidence` maps to evidence acquisition or escalation, never failure of the underlying claim.
- A later owner ruling supersedes the draft recommendation as the reference, while both remain in the
  packet chronology.
- Exact actions remain domain terms (`implementation`, `risk_gate`, `human_firewall`, `assemble`, etc.);
  cross-domain aliases may be added only as a secondary field.

## Accepted anchors

| Episode | Verdict | Exact next action | Why accepted |
|---|---|---|---|
| A-D01 | pass with advisory | implementation | report and subsequent gate chronology agree |
| A-D02 | pass with advisory | risk gate | report explicitly says `Gate result: PASS`; gate 3c follows |
| A-D03 | pass | alignment/close | final risk gate and alignment artifact agree |
| A-D08 | pass | merge/close | bug-fix gate status is explicit |
| B-D01 | partial (not proven) | retain partial; human-gated follow-on | owner corrected initial recommendation |
| B-D02 | partial | retain partial; follow-on | owner ruling is explicit |

Everything else marked `review` in the manifest needs a second reader. Holdout values must never be added
to this main-branch document.

## Provenance basis

- type: docs · ref: `product/research/shd-007/REPORT.md` · title: `shd-007 REPORT — owner firewall ruling` · org: `arch-research garage` · year: 2026
- type: docs · ref: `product/research/shd-007/SCOPE.md` · title: `shd-007 SCOPE — predeclared proof clauses` · org: `arch-research garage` · year: 2026
- type: docs · ref: `product/features/vnc-047/reports/gate-3b-report.md` · title: `vnc-047 gate 3b report` · org: `dug-21` · year: 2026
