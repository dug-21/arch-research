# jurati-001 W1 proposed corpus corrections

**Append-only reviewer proposal.** This document does not alter the selector's manifest, findings, packets,
labels, ambiguity register, or split assignment. The W1 owner must accept, reject, or supersede each item
explicitly.

| Episode | Proposed correction | Basis |
|---|---|---|
| A-D05 | Keep as initial `REWORKABLE FAIL`; exact action is the named registry-wiring rework. Add the rework-1 PASS only as chronology or a separate episode. | Initial and rework reports are distinct and explicit. |
| A-D06 | Replace `fail/rework` with `pass-after-rework → implementation`, or point to a separately pinned original-failure report. | Named `crt-025/reports/gate-3a-report.md` says “rework pass 1” and `PASS`. |
| A-D11 | Replace `fail/rework` with `pass-after-rework → risk gate`, or select the original failing validator artifact as primary. | Named `col-024/reports/gate-3b-report.md` says `PASS (rework iteration 1)`. |
| A-D13 | Replace `fail/rework` with `pass-after-rework → implementation`, or select a pinned original failure. | Named `crt-030/reports/gate-3a-report.md` says re-check after rework, `PASS`. |
| A-C01 | Define the selected question as the re-validation decision and retain `pass-after-rework`; otherwise split original FAIL and later PASS. | The canonical vnc-046 report embeds both iterations. |
| A-C03 | Replace `fail/rework` with `pass-after-rework → implementation`, or select a pinned original failure. | Named `col-022/reports/gate-3a-report.md` says `PASS`, rework 1. |
| A-C05 / A-C06 | Keep as two episodes: initial REWORKABLE FAIL then rework PASS. | Two separately named bugfix reports preserve chronology. |
| A-C07 | Replace `fail/rework` with `pass-after-rework → implementation`, or select a pinned original failure. | Named `crt-029/reports/gate-3a-report.md` is a retry after rework and says `PASS`. |
| B-D03 | Keep; verdict `owner-directed early close`, action `close wfh-002 and reset to broader problem-space investigation`, action provenance `explicit + observed`. | REPORT §§1, 4, 7, 8. |
| B-D04 | Exclude, or label `no binding decision / provisional only` with action `successor unconstrained`. | REPORT §5 calls Option C provisional and non-binding. |
| B-D05 | Either keep decision point P2 and change action to `strike and replace absence-of-prior-art claim`, or change decision point to P4 before using an assemble/build routing action. | Triage §§2–3 separate P2's falsification from P4's route. |
| B-D06 | Keep only if a second source proves owner acceptance of P8/done-when amendment; otherwise exclude as advisory. | Amendment 2 is owner-directed research but its consequence is proposed, not shown executed. |
| B-D07 | Keep `partial`; mark handoff action `prescribed` until a filed issue is cited. | FINDINGS-poc “Handoff” is imperative, not execution evidence. |
| B-C01 | Keep directional decision; mark route `prescribed`, not observed, unless downstream adoption/build sources are attached. | shd-005 REPORT is explicitly directional. |
| B-C02 | Keep as `insufficient evidence / missing`; exact next action is the three-part shd-006 POC proof gate. | shd-005 REPORT §§6–7. |
| B-C03 | Split into bounded owner questions and attach rulings, or exclude the omnibus triage row. | wfh-004 triage leaves four decisions to the owner. |

## Corpus-level additions

1. Add a qualifying garage scope-approval decision to satisfy the predeclared Domain-B stratum.
2. Add `action_provenance: explicit | observed | inferred | prescribed` to every reference row.
3. Require two pinned sources for `inferred`; a later artifact alone establishes chronology but not always
   the reason or exact action.
4. Store original and rework decisions as separate episode IDs when both are scored. Never let a canonical
   post-rework report stand in for an absent original report.
5. Replace direct holdout verdict-report paths in broadly consumed allocation metadata with opaque source
   bundle IDs where practical; retain the path mapping only in the sealed generator input.
