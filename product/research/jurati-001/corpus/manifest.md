# jurati-001 frozen corpus manifest candidate

**State:** candidate for corpus-freeze gate; labels marked `review` are not frozen until independently adjudicated.
**SDLC repository:** `dug-21/unimatrix` at `7ac778dfe3aa352d475dddc7897384191419ddf8`.
**Garage repository:** `dug-21/arch-research` at `5d4ccdd92cac1ee0b13fd3c7aaa207e9720059de`.
**Sampling unit:** cycle. No cycle crosses partitions; no cycle contributes more than three episodes.

The corpus contains 45 decisions: 32 SDLC decisions from 16 cycles and 13 garage decisions from eight
cycles. Partition counts are 23 development, 11 calibration, and 11 sealed holdout decisions; cycle counts
are 12/6/6. The slightly decision-heavy development partition preserves the exact 50/25/25 cycle split.

## Domain A — SDLC (32 decisions, 16 cycles)

| ID | Split | Cycle | Decision point | Primary artifact | Reference class | Actual next action | Label state |
|---|---|---|---|---|---|---|---|
| A-D01 | development | vnc-047 | design gate 3a | `product/features/vnc-047/reports/gate-3a-report.md` | pass/advisory | implementation | accepted |
| A-D02 | development | vnc-047 | code gate 3b | `product/features/vnc-047/reports/gate-3b-report.md` | pass/advisory | risk gate | accepted |
| A-D03 | development | vnc-047 | final risk gate 3c | `product/features/vnc-047/reports/gate-3c-report.md` | pass | alignment/close | accepted |
| A-D04 | development | col-023 | design gate 3a | `product/features/col-023/reports/gate-3a-report.md` | pass/advisory | implementation | accepted |
| A-D05 | development | col-023 | code gate 3b | `product/features/col-023/reports/gate-3b-report.md` | fail/rework | revised code gate | review |
| A-D06 | development | crt-025 | design gate 3a | `product/features/crt-025/reports/gate-3a-report.md` | fail/rework | revised design gate | review |
| A-D07 | development | crt-025 | final risk gate 3c | `product/features/crt-025/reports/gate-3c-report.md` | pass/advisory | alignment/close | review |
| A-D08 | development | bugfix-444 | bug-fix gate | `product/features/bugfix-444/reports/gate-bugfix-report.md` | pass | merge/close | accepted |
| A-D09 | development | vnc-044 | design gate 3a | `product/features/vnc-044/reports/gate-3a-report.md` | pass | implementation | accepted |
| A-D10 | development | vnc-044 | code gate 3b | `product/features/vnc-044/reports/gate-3b-report.md` | pass/advisory | risk gate | accepted |
| A-D11 | development | col-024 | code gate 3b | `product/features/col-024/reports/gate-3b-report.md` | fail/rework | implementation rework | review |
| A-D12 | development | col-024 | final risk gate 3c | `product/features/col-024/reports/gate-3c-report.md` | pass/advisory | alignment/close | review |
| A-D13 | development | crt-030 | design gate 3a | `product/features/crt-030/reports/gate-3a-report.md` | fail/rework | design rework | review |
| A-D14 | development | crt-030 | code gate 3b | `product/features/crt-030/reports/gate-3b-report.md` | pass/advisory | risk gate | review |
| A-D15 | development | bugfix-458 | bug-fix gate | `product/features/bugfix-458/reports/gate-bugfix-report.md` | pass/advisory | merge/close | review |
| A-D16 | development | vnc-038 | design gate 3a | `product/features/vnc-038/reports/gate-3a-report.md` | pass | implementation | accepted |
| A-C01 | calibration | vnc-046 | design gate 3a | `product/features/vnc-046/reports/gate-3a-report.md` | pass-after-rework | implementation | review |
| A-C02 | calibration | vnc-046 | final risk gate 3c | `product/features/vnc-046/reports/gate-3c-report.md` | pass/advisory | alignment/close | accepted |
| A-C03 | calibration | col-022 | design gate 3a | `product/features/col-022/reports/gate-3a-report.md` | fail/rework | revised design gate | review |
| A-C04 | calibration | col-022 | final risk gate 3c | `product/features/col-022/reports/gate-3c-report.md` | pass/advisory | alignment/close | review |
| A-C05 | calibration | bugfix-381 | bug-fix gate | `product/features/bugfix-381/reports/gate-bugfix-report.md` | fail/rework | revised bug-fix gate | review |
| A-C06 | calibration | bugfix-381 | revised bug-fix gate | `product/features/bugfix-381/reports/gate-bugfix-v2-report.md` | pass | merge/close | review |
| A-C07 | calibration | crt-029 | design gate 3a | `product/features/crt-029/reports/gate-3a-report.md` | fail/rework | revised design | review |
| A-C08 | calibration | crt-029 | final risk gate 3c | `product/features/crt-029/reports/gate-3c-report.md` | pass/advisory | alignment/close | review |
| A-H01 | holdout | vnc-045 | design gate 3a | `product/features/vnc-045/reports/gate-3a-report.md` | sealed | sealed | sealed |
| A-H02 | holdout | vnc-045 | final risk gate 3c | `product/features/vnc-045/reports/gate-3c-report.md` | sealed | sealed | sealed |
| A-H03 | holdout | col-020 | design gate 3a | `product/features/col-020/reports/gate-3a-report.md` | sealed | sealed | sealed |
| A-H04 | holdout | col-020 | code gate 3b | `product/features/col-020/reports/gate-3b-report.md` | sealed | sealed | sealed |
| A-H05 | holdout | crt-018 | design gate 3a | `product/features/crt-018/reports/gate-3a-report.md` | sealed | sealed | sealed |
| A-H06 | holdout | crt-018 | final risk gate 3c | `product/features/crt-018/reports/gate-3c-report.md` | sealed | sealed | sealed |
| A-H07 | holdout | bugfix-230 | bug-fix gate | `product/features/bugfix-230/reports/gate-bugfix-report.md` | sealed | sealed | sealed |
| A-H08 | holdout | vnc-045 | code gate 3b | `product/features/vnc-045/reports/gate-3b-report.md` | sealed | sealed | sealed |

The `vnc-047` packet includes the complete chain artifacts (`SCOPE.md`, `ACCEPTANCE-MAP.md`, gate 3a/3b/3c,
and `ALIGNMENT-REPORT.md`) while treating only its three gates as decision episodes.

## Domain B — research garage (13 decisions, eight cycles)

| ID | Split | Cycle | Decision point | Primary artifact | Reference class | Actual next action | Label state |
|---|---|---|---|---|---|---|---|
| B-D01 | development | shd-007 | feasibility/firewall grade C1 | `product/research/shd-007/REPORT.md` | refused proven; partial | retain partial; human gate | accepted-owner |
| B-D02 | development | shd-007 | feasibility/firewall grade C2 | `product/research/shd-007/REPORT.md` | partial | retain partial; follow-on | accepted-owner |
| B-D03 | development | wfh-002 | scope-boundary decision | `product/research/wfh-002/REPORT.md` | boundary crossed | corrective close | review |
| B-D04 | development | wfh-002 | product routing | `product/research/wfh-002/REPORT.md` | scope failure/redirection | no runtime build | review |
| B-D05 | development | wfh-005 | premise P2 triage | `product/research/wfh-005/reports/triage.md` | falsified/narrowed | assemble residual | review |
| B-D06 | development | wfh-005 | frontier amendment | `product/research/wfh-005/reports/triage-amendment-2.md` | expanded/corrected | amend synthesis | review |
| B-D07 | development | smart-edge-002 | validated POC disposition | `product/research/smart-edge-002/FINDINGS-poc.md` | directional disposition | route per findings | review |
| B-C01 | calibration | shd-005 | capability/routing synthesis | `product/research/shd-005/REPORT.md` | directional | follow recommended route | review |
| B-C02 | calibration | shd-005 | evidence sufficiency | `product/research/shd-005/REPORT.md` | insufficient/partial | preserve hole | review |
| B-C03 | calibration | wfh-004 | triage | `product/research/wfh-004/reports/triage.md` | frontier expansion | second sweep | review |
| B-H01 | holdout | wfh-001 | tier triage | `product/research/wfh-001/reports/triage.md` | sealed | sealed | sealed |
| B-H02 | holdout | wfh-001 | formalization decision | `product/research/wfh-001/reports/formalization.md` | sealed | sealed | sealed |
| B-H03 | holdout | shd-004 | evidence/routing decision | `product/research/shd-004/findings-W4b.md` | sealed | sealed | sealed |

## Eligibility and exclusions

- Included only a decision with an identifiable question, evidence-bearing artifact, bounded historical
  outcome, and observable or explicitly prescribed next action.
- Excluded raw private transcripts, credentials, model weights, ordinary implementation notes, duplicate
  copies under `agents/`, and reports whose only decision is subsumed by a selected later re-review.
- `owner intervention` is explicit for `shd-007`; likely owner-corrected garage cases remain in the ambiguity
  register until an independent reviewer confirms the record.
- Holdout outcome and next-action cells above are deliberately sealed. Their values belong in a separate
  generated label artifact on `research/jurati-001`, not in judge-facing documents on `main`.

## Structured citations

- type: repo · ref: `https://github.com/dug-21/unimatrix/tree/7ac778dfe3aa352d475dddc7897384191419ddf8/product/features` · title: `Unimatrix feature-cycle corpus` · org: `dug-21` · year: 2026
- type: repo · ref: `https://github.com/dug-21/arch-research/tree/5d4ccdd92cac1ee0b13fd3c7aaa207e9720059de/product/research` · title: `Research garage run corpus` · org: `dug-21` · year: 2026
