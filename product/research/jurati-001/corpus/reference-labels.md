# Reference-label policy and development labels v0.2

The historical report is evidence, not unquestionable truth. A label is accepted only when the record
supports both the verdict and the exact action that actually followed.

## Label record

`episode_id`, bounded clause results, verdict, exact next action, source references, owner intervention,
adjudication state (`accepted | accepted-owner | review | excluded`), reviewer identity, rationale, and
adjudication timestamp, `action_provenance`, and ordered action-source spans.

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
- `prescribed` is not execution. `inferred` requires two independent pinned sources; one later artifact
  establishes chronology, not necessarily causation or the exact action.

## Accepted anchors

| Episode | Verdict | Exact next action | Provenance | Why accepted |
|---|---|---|---|---|
| A-D01 | pass with advisory | implementation | prescribed | report states gate consequence |
| A-D02 | pass with advisory | risk gate | prescribed | report states PASS and consequence |
| A-D03 | pass | alignment/close | prescribed | final gate states consequence |
| A-D05 | reworkable fail | registry-wiring rework | explicit | reviewer reconciled initial/rework reports |
| A-D06 | pass-after-rework | implementation | prescribed | selected artifact is post-rework PASS |
| A-D08 | pass | merge/close | prescribed | bug-fix report states consequence |
| A-D11 | pass-after-rework | risk gate | prescribed | selected artifact is post-rework PASS |
| A-D13 | pass-after-rework | implementation | prescribed | selected artifact is post-rework PASS |
| A-C03 | pass-after-rework | implementation | prescribed | selected artifact is post-rework PASS |
| A-C07 | pass-after-rework | implementation | prescribed | selected artifact is post-rework PASS |
| B-D01 | partial (not proven) | retain partial; human-gated follow-on | explicit + observed | owner ruling and final state agree |
| B-D02 | partial | retain partial; follow-on | explicit + observed | owner ruling and final state agree |
| B-D03 | owner-directed early close | close; reset to broader investigation | explicit + observed | REPORT and SCOPE amendment agree |
| B-D04 | scope approved | begin bounded workstreams | explicit + observed | status and produced artifacts agree |
| B-D05 | P2 falsified/narrowed | strike and replace absence claim | prescribed | corrected question/action coupling |
| B-D06 | P4 wounded | ADOPT `github/gh-aw`; ASSEMBLE Temporal + policy + MCP gateway + AI gateway + SPIRE/Vault + OTel/Langfuse + sandbox; BUILD only the non-declarative-actor residual after the two unread falsifier cells close | prescribed | source-exact bounded triage routing |

Everything else marked `review` in the manifest needs a second reader. Holdout identities and values must never be added
to this main-branch document.

## Provenance basis

- type: docs · ref: `product/research/shd-007/REPORT.md` · title: `shd-007 REPORT — owner firewall ruling` · org: `arch-research garage` · year: 2026
- type: docs · ref: `product/research/shd-007/SCOPE.md` · title: `shd-007 SCOPE — predeclared proof clauses` · org: `arch-research garage` · year: 2026
- type: docs · ref: `product/features/vnc-047/reports/gate-3b-report.md` · title: `vnc-047 gate 3b report` · org: `dug-21` · year: 2026
