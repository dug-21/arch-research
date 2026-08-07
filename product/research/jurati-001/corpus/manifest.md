# jurati-001 corpus manifest candidate v0.2

**State:** reworked candidate; supersedes v0.1 at commit `f1fbfa8`. Labels marked `review` are not frozen.
**SDLC repository:** `dug-21/unimatrix` at `7ac778dfe3aa352d475dddc7897384191419ddf8`.
**Garage repository:** `dug-21/arch-research` at `5d4ccdd92cac1ee0b13fd3c7aaa207e9720059de`.
**Sampling unit:** cycle. No cycle crosses partitions; no cycle contributes more than three episodes.

The corpus contains 45 decisions: 32 SDLC decisions from 16 cycles and 13 garage decisions from eight
cycles. Partition counts are 23 development, 11 calibration, and 11 sealed holdout decisions; cycle counts
are 12/6/6. The slightly decision-heavy development partition preserves the exact 50/25/25 cycle split.

## Domain A — SDLC (32 decisions, 16 cycles)

| ID | Split | Cycle | Decision point | Primary artifact | Reference class | Next action | Provenance | State |
|---|---|---|---|---|---|---|---|---|
| A-D01 | development | vnc-047 | design gate 3a | `product/features/vnc-047/reports/gate-3a-report.md` | pass/advisory | implementation | prescribed: primary report | accepted |
| A-D02 | development | vnc-047 | code gate 3b | `product/features/vnc-047/reports/gate-3b-report.md` | pass/advisory | risk gate | prescribed: primary report | accepted |
| A-D03 | development | vnc-047 | final risk gate 3c | `product/features/vnc-047/reports/gate-3c-report.md` | pass | alignment/close | prescribed: primary report | accepted |
| A-D04 | development | col-023 | design gate 3a | `product/features/col-023/reports/gate-3a-report.md` | pass/advisory | implementation | prescribed: primary report | review |
| A-D05 | development | col-023 | initial code gate 3b | `product/features/col-023/reports/gate-3b-report.md` | reworkable fail | registry-wiring rework | explicit: primary report; later rework report is chronology | accepted-reviewer |
| A-D06 | development | crt-025 | post-rework design gate 3a | `product/features/crt-025/reports/gate-3a-report.md` | pass-after-rework | implementation | prescribed: primary report | accepted-reviewer |
| A-D07 | development | crt-025 | final risk gate 3c | `product/features/crt-025/reports/gate-3c-report.md` | pass/advisory | alignment/close | prescribed: primary report | accepted-reviewer |
| A-D08 | development | bugfix-444 | bug-fix gate | `product/features/bugfix-444/reports/gate-bugfix-report.md` | pass | merge/close | prescribed: primary report | accepted |
| A-D09 | development | vnc-044 | design gate 3a | `product/features/vnc-044/reports/gate-3a-report.md` | pass | implementation | prescribed: primary report | accepted |
| A-D10 | development | vnc-044 | code gate 3b | `product/features/vnc-044/reports/gate-3b-report.md` | pass/advisory | risk gate | prescribed: primary report | accepted |
| A-D11 | development | col-024 | post-rework code gate 3b | `product/features/col-024/reports/gate-3b-report.md` | pass-after-rework | risk gate | prescribed: primary report | accepted-reviewer |
| A-D12 | development | col-024 | final risk gate 3c | `product/features/col-024/reports/gate-3c-report.md` | pass/advisory | alignment/close | prescribed: primary report | accepted-reviewer |
| A-D13 | development | crt-030 | post-rework design gate 3a | `product/features/crt-030/reports/gate-3a-report.md` | pass-after-rework | implementation | prescribed: primary report | accepted-reviewer |
| A-D14 | development | crt-030 | code gate 3b | `product/features/crt-030/reports/gate-3b-report.md` | pass/advisory | risk gate | prescribed: primary report | accepted-reviewer |
| A-D15 | development | bugfix-458 | bug-fix gate | `product/features/bugfix-458/reports/gate-bugfix-report.md` | pass/advisory | merge/close | prescribed: primary report | accepted-reviewer |
| A-D16 | development | vnc-038 | design gate 3a | `product/features/vnc-038/reports/gate-3a-report.md` | pass | implementation | prescribed: primary report | accepted |
| A-C01 | calibration | vnc-046 | post-rework design re-validation | `product/features/vnc-046/reports/gate-3a-report.md` | pass-after-rework | implementation | prescribed: primary report; initial fail is chronology | accepted-reviewer |
| A-C02 | calibration | vnc-046 | final risk gate 3c | `product/features/vnc-046/reports/gate-3c-report.md` | pass/advisory | alignment/close | prescribed: primary report | accepted |
| A-C03 | calibration | col-022 | post-rework design gate 3a | `product/features/col-022/reports/gate-3a-report.md` | pass-after-rework | implementation | prescribed: primary report | accepted-reviewer |
| A-C04 | calibration | col-022 | final risk gate 3c | `product/features/col-022/reports/gate-3c-report.md` | pass/advisory | alignment/close | prescribed: primary report | accepted-reviewer |
| A-C05 | calibration | bugfix-381 | initial bug-fix gate | `product/features/bugfix-381/reports/gate-bugfix-report.md` | reworkable fail | named bug-fix rework | explicit: primary report | accepted-reviewer |
| A-C06 | calibration | bugfix-381 | revised bug-fix gate | `product/features/bugfix-381/reports/gate-bugfix-v2-report.md` | pass | merge/close | prescribed: primary report | accepted-reviewer |
| A-C07 | calibration | crt-029 | post-rework design gate 3a | `product/features/crt-029/reports/gate-3a-report.md` | pass-after-rework | implementation | prescribed: primary report | accepted-reviewer |
| A-C08 | calibration | crt-029 | final risk gate 3c | `product/features/crt-029/reports/gate-3c-report.md` | pass/advisory | alignment/close | prescribed: primary report | accepted-reviewer |
| A-H01 | holdout | `A-HC01` | design gate | `A-HB01` | sealed | sealed | sealed mapping | sealed |
| A-H02 | holdout | `A-HC01` | code gate | `A-HB02` | sealed | sealed | sealed mapping | sealed |
| A-H03 | holdout | `A-HC01` | final risk gate | `A-HB03` | sealed | sealed | sealed mapping | sealed |
| A-H04 | holdout | `A-HC02` | design gate | `A-HB04` | sealed | sealed | sealed mapping | sealed |
| A-H05 | holdout | `A-HC02` | code gate | `A-HB05` | sealed | sealed | sealed mapping | sealed |
| A-H06 | holdout | `A-HC03` | design gate | `A-HB06` | sealed | sealed | sealed mapping | sealed |
| A-H07 | holdout | `A-HC03` | final risk gate | `A-HB07` | sealed | sealed | sealed mapping | sealed |
| A-H08 | holdout | `A-HC04` | bug-fix gate | `A-HB08` | sealed | sealed | sealed mapping | sealed |

The `vnc-047` packet includes the complete chain artifacts (`SCOPE.md`, `ACCEPTANCE-MAP.md`, gate 3a/3b/3c,
and `ALIGNMENT-REPORT.md`) while treating only its three gates as decision episodes.

## Domain B — research garage (13 decisions, eight cycles)

| ID | Split | Cycle | Decision point | Primary artifact | Reference class | Next action | Provenance | State |
|---|---|---|---|---|---|---|---|---|
| B-D01 | development | shd-007 | feasibility/firewall grade C1 | `product/research/shd-007/REPORT.md` | refused proven; partial | retain partial; human-gated follow-on | explicit + observed: owner ruling and final scope/report state | accepted-owner |
| B-D02 | development | shd-007 | feasibility/firewall grade C2 | `product/research/shd-007/REPORT.md` | partial | retain partial; follow-on | explicit + observed: owner ruling and final scope/report state | accepted-owner |
| B-D03 | development | wfh-002 | owner early-close decision | `product/research/wfh-002/REPORT.md` | owner-directed early close | close; reset to broader problem-space investigation | explicit + observed: REPORT §§1/4/7/8 and SCOPE amendment | accepted-reviewer |
| B-D04 | development | wfh-002 | scope-approval gate | `product/research/wfh-002/SCOPE.md` | approved | begin bounded workstreams | explicit + observed: status line and produced W1–W3/W5 artifacts | accepted-reviewer |
| B-D05 | development | wfh-005 | premise P2 triage | `product/research/wfh-005/reports/triage.md` | falsified/narrowed | strike and replace absence-of-prior-art claim | explicit/prescribed: triage §§2–3 | accepted-reviewer |
| B-D06 | development | wfh-005 | P4 routing | `product/research/wfh-005/reports/triage.md` | wounded; narrow build | adopt gateway, assemble composition, build one residual only after holes close | prescribed: triage §3 | accepted-reviewer |
| B-D07 | development | smart-edge-002 | validated POC disposition | `product/research/smart-edge-002/FINDINGS-poc.md` | partial | file in-server integration issue | prescribed: handoff section; execution uncorroborated | accepted-reviewer |
| B-C01 | calibration | shd-005 | capability/routing synthesis | `product/research/shd-005/REPORT.md` | directional | adopt commodity gateway/harness; build only two hard layers | prescribed: report | accepted-reviewer |
| B-C02 | calibration | shd-005 | evidence sufficiency | `product/research/shd-005/REPORT.md` | insufficient; C3 missing | run three-part shd-006 POC proof gate | prescribed: report §§6–7 | accepted-reviewer |
| B-C03 | calibration | wfh-004 | scope-approval gate | `product/research/wfh-004/SCOPE.md` | approved | execute bounded hypothesis workstreams | explicit + observed: scope status and produced workstream artifacts | review |
| B-H01 | holdout | `B-HC01` | directional triage | `B-HB01` | sealed | sealed | sealed mapping | sealed |
| B-H02 | holdout | `B-HC01` | formalization gate | `B-HB02` | sealed | sealed | sealed mapping | sealed |
| B-H03 | holdout | `B-HC02` | evidence/routing gate | `B-HB03` | sealed | sealed | sealed mapping | sealed |

## Eligibility and exclusions

- Included only a decision with an identifiable question, evidence-bearing artifact, bounded historical
  outcome, and observable or explicitly prescribed next action.
- Excluded raw private transcripts, credentials, model weights, ordinary implementation notes, duplicate
  copies under `agents/`, and reports whose only decision is subsumed by a selected later re-review.
- Excluded the old B-D04 provisional Option-C routing, B-D06 amendment proposal, and B-C03 omnibus triage.
  They were respectively non-binding, uncorroborated as accepted, and unresolved. Their episode IDs now
  select bounded scope approval/P4/scope approval decisions; this is replacement, not relabeling.
- `owner intervention` is explicit for `shd-007`; likely owner-corrected garage cases remain in the ambiguity
  register until an independent reviewer confirms the record.
- Holdout cycle identities, paths, outcomes, actions, and identity-to-bundle mapping are absent from main.
  They belong only in a sealed generated mapping on `research/jurati-001`; main may publish its digest and
  aggregate counts after generation.

## Structured citations

- type: repo · ref: `https://github.com/dug-21/unimatrix/tree/7ac778dfe3aa352d475dddc7897384191419ddf8/product/features` · title: `Unimatrix feature-cycle corpus` · org: `dug-21` · year: 2026
- type: repo · ref: `https://github.com/dug-21/arch-research/tree/5d4ccdd92cac1ee0b13fd3c7aaa207e9720059de/product/research` · title: `Research garage run corpus` · org: `dug-21` · year: 2026
- type: docs · ref: `product/research/jurati-001/reports/corpus-review.md` · title: `jurati-001 W1 independent corpus review` · org: `arch-research garage` · year: 2026
