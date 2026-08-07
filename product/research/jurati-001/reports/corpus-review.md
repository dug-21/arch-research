# jurati-001 W1 independent corpus review

**Reviewer:** `jurati-001-researcher-W1-review`  
**Recommendation:** **REWORKABLE** — do not freeze the corpus yet.  
**Reviewed:** 2026-08-07 against the two commits pinned in `corpus/manifest.md`.

## Gate finding

The candidate satisfies the numerical floor and cycle-level split invariant: 32 SDLC episodes from 16
cycles, 13 garage episodes from eight cycles, an 8/4/4 and 4/2/2 cycle split, no cross-partition cycle,
and no cycle contributing more than three episodes. The source paths resolve at the pinned commits and the
selected set includes a complete mature chain, bug-fix gates, rework, and an owner-corrected firewall case.

It is not freezeable because the manifest does not yet reliably distinguish an initial failure from the
post-rework report that replaced or summarized it. Four rows label a `FAIL/rework` while their named primary
artifact says `PASS` at the pinned SHA: A-D06 (`crt-025`), A-D11 (`col-024`), A-D13 (`crt-030`), and A-C03
(`col-022`). A-C07 has the same provenance defect: its primary artifact is explicitly a retry-after-rework
`PASS`, not the proposed initial-failure episode. These are reference-label defects, not model ambiguity.

The garage sample also misses a required stratum: no selected Domain-B episode is a scope-approval gate.
The scope requires the garage set to span scope approval and coverage gates; synthesis, firewall, and close
decisions do not substitute for scope approval.

## Ambiguity adjudication

| Register | Adjudication | Required corpus action |
|---|---|---|
| AR-01 / A-D05 | The initial `col-023` gate 3b is a distinct **REWORKABLE FAIL** followed by a distinct rework-1 **PASS**. The selected initial episode is valid; its exact action is the named registry-wiring rework. | Keep A-D05. Include both reports in chronology and do not merge the later PASS into its label. If the later decision is useful, add it as a separate episode subject to the three-per-cycle cap. |
| AR-02 / A-D06–07 | A-D06 is mislabeled: the named canonical `crt-025` gate-3a report is “rework pass 1” and `PASS`. The earlier failure is only antecedent chronology unless a separately pinned original report is selected. A-D07 is a valid later final-risk PASS, but it does not repair A-D06's provenance. | Relabel A-D06 as the post-rework PASS, replace its primary artifact with a pinned original-failure artifact, or exclude it. Keep A-D07 as PASS with advisory chronology. |
| AR-03 / A-D11–15, A-C03–08 | Full-report reading confirms A-D11 is `PASS (rework iteration 1)`, A-D12 PASS, A-D13 PASS after rework, A-D14 PASS, A-D15 PASS, A-C03 PASS after rework, A-C04 PASS, A-C05 initial FAIL, A-C06 rework PASS, A-C07 PASS after rework, and A-C08 PASS. | Correct A-D11, A-D13, A-C03, and A-C07 or select separate original reports. Keep A-C05/A-C06 as two chronological decisions. Do not derive overall verdicts from clause tokens. |
| AR-04 / A-C01 | The canonical report contains two decisions: an original REWORKABLE FAIL and a re-validation PASS. The manifest's `pass-after-rework` reading is the later decision only. | Keep as one later PASS only if the packet includes the original as chronology and asks the later question. Otherwise split into two episodes; do not label the initial failure `pass-after-rework`. |
| AR-05 / A-H* | Holdout values were not inspected in this review. The main-branch manifest does not print verdicts, but it publishes holdout cycle names and direct paths to verdict-bearing reports. That makes accidental unsealing one repository read away. | Treat the current manifest as allocation metadata, not a sealed-label boundary. The generator must exclude reference report verdict sections from judge packets, and language/prompt authors must attest they did not inspect the named holdout reports. Prefer a private/separate reference-label artifact with only hashes on main. |
| AR-06 / B-D01 | The owner's 2026-08-04 ruling is unambiguous: C1 remains `partial`, because “on target HW” is unmet; the withdrawn draft `proven` recommendation is disagreement evidence. | Keep accepted-owner label: `partial`; action `retain partial / human-gated follow-on`. |
| AR-07 / B-D03–04 | The report supports B-D03 as an owner-directed early-close decision caused by an unenforced scope boundary. B-D04 is not an accepted product-routing decision: Option C is explicitly provisional, non-binding, and does not bind the successor. | Keep B-D03 with exact action `close early; reset to broader problem-space investigation`. Exclude B-D04, or recast it as `no binding decision / abstain`; never label “no runtime build” as an executed Option-C routing outcome. |
| AR-08 / B-D05–06 | Amendment 2 explicitly says P1–P5 verdicts and P4 routing are unchanged. It adds P8 and amends the BUILD `done_when`; it does not supersede the P2 triage. B-D05 currently pairs P2's falsification with “assemble residual,” an action belonging to the P4 routing discussion. B-D06 is a separate proposed amendment, but acceptance/execution is not established by this artifact. | Correct B-D05's exact action to the P2 consequence actually stated (strike/replace the absence-of-prior-art claim), or change the decision point to P4 routing. Retain B-D06 only as an advisory/proposed decision with corroborated owner acceptance; otherwise exclude. |
| AR-09 / B-D07 | The POC establishes `partial` and explicitly prescribes filing a Unimatrix issue for in-server integration. The artifact proves the recommendation, not that the handoff occurred. | Label next action `prescribed` unless a second pinned source shows the issue was filed; do not call it observed. |
| AR-10 / B-C01–03 | B-C01 is a bounded directional position: adopt a commodity gateway/harness and build only the two hard layers. B-C02 is a distinct evidence-sufficiency/firewall ruling: C3 stays `missing` until a three-part POC. B-C03 is an advisory triage with four owner decisions still open, not one fully executed “frontier expansion” action. | Keep domain-native verdicts. Mark B-C01/B-C02 actions `prescribed` unless downstream execution is cited. Split B-C03 into bounded questions with owner rulings or exclude it; the whole triage is not one deterministic episode. |
| AR-11 / B-H* | Holdout outcomes were not inspected. The same direct-report-path leakage risk as AR-05 applies. | Seal labels outside judge-facing/main artifacts; publish hashes and aggregate counts only. Require reviewer and language-author non-inspection attestations. |
| AR-12 / corpus-wide | The current tables do not carry the required `explicit | observed | inferred` action provenance, and several “actual” actions are merely recommendations. | Add action-provenance to every row. An inferred action needs two independent pinned sources; otherwise mark prescribed or exclude. |

## Freeze blockers

1. Correct or replace A-D06, A-D11, A-D13, A-C03, and A-C07 so the selected primary artifact and
   reference verdict describe the same decision in time.
2. Exclude or recast B-D04; correct B-D05's question/action coupling; establish acceptance for B-D06;
   split or exclude B-C03.
3. Add at least one qualifying garage scope-approval episode without violating cycle partitioning or the
   three-episode cap.
4. Add per-row action provenance and two-source corroboration for every inferred “actual next action.”
5. Generate integrity-addressed packets and labels, prove fail-closed digest and leakage checks, and publish
   final hashes. The present markdown packet specification is a claim about a future executable, not proof.
6. Resolve holdout operational secrecy: direct verdict-report paths are public in the allocation manifest.
   At minimum, keep reference fields out of judge packets and record non-inspection attestations for W2–W5.

## Provenance

- type: repo · ref: `https://github.com/dug-21/unimatrix/tree/7ac778dfe3aa352d475dddc7897384191419ddf8/product/features` · title: `Unimatrix feature-cycle corpus` · org: `dug-21` · year: 2026
- type: repo · ref: `https://github.com/dug-21/arch-research/tree/5d4ccdd92cac1ee0b13fd3c7aaa207e9720059de/product/research` · title: `Research garage run corpus` · org: `dug-21` · year: 2026
- type: docs · ref: `product/features/col-023/reports/gate-3b-report.md` and `gate-3b-rework1-report.md` at the pinned Unimatrix SHA · title: `col-023 initial and rework gate 3b reports` · org: `dug-21` · year: 2026
- type: docs · ref: `product/features/{crt-025,col-024,crt-030,col-022,crt-029}/reports/gate-*.md` at the pinned Unimatrix SHA · title: `Post-rework canonical gate reports used by the candidate manifest` · org: `dug-21` · year: 2026
- type: docs · ref: `product/research/{shd-007,wfh-002}/REPORT.md` at the pinned arch-research SHA · title: `Owner firewall and early-close rulings` · org: `arch-research garage` · year: 2026
- type: docs · ref: `product/research/wfh-005/reports/{triage,triage-amendment-2}.md` at the pinned arch-research SHA · title: `wfh-005 triage and append-only amendment` · org: `arch-research garage` · year: 2026

No holdout verdict summary was inspected, no Unimatrix write was made, and no W1 source artifact was
silently rewritten.

---

## Re-review — v0.2 at `90380e5` (2026-08-07)

**Recommendation for proceeding to D15 corpus generation:** **REWORKABLE**.  
**Final corpus-freeze gate after D15 generation:** **mandatory**.

The v0.2 rework closes almost all document defects from the first ruling:

- A-D06, A-D11, A-D13, A-C03, and A-C07 now select and label the post-rework PASS decisions actually
  contained in their pinned primary artifacts.
- A-D05 and A-C05/A-C06 preserve initial-failure versus rework chronology rather than collapsing it.
- B-D04 and B-C03 now select genuine scope-approval decisions. At the pinned garage SHA, `wfh-002/SCOPE.md`
  explicitly says owner-approved and its later artifacts demonstrate execution; `wfh-004/SCOPE.md` says
  owner-kicked/active and the bounded workstream artifacts exist. A-D04's remaining `review` state is also
  adjudicated here as accepted: its pinned report is an explicit design-gate PASS with implementation as
  the prescribed consequence.
- The provisional Option-C row, unaccepted amendment row, and omnibus triage row are no longer scored as
  binding decisions. B-D03, B-D05, B-D07, B-C01, and B-C02 now have bounded, source-supported consequences.
- Every visible row carries `explicit`, `observed`, or `prescribed` action provenance; no `inferred` action
  remains. The packet schema correctly requires two independent pinned sources if inference is later added.
- Counts and splits remain valid: 32/16 SDLC, 13/8 garage, 23/11/11 decisions, 12/6/6 cycles, exact
  per-domain 50/25/25 cycle allocation, partition-exclusive cycles, and at most three episodes per cycle.
- The current `jurati-001` working tree no longer contains the previously published clear-text holdout cycle
  identities or source paths. Opaque IDs preserve cycle grouping and episode counts without exposing the
  mapping. The old identities remain recoverable from git history, so opacity is an operational control,
  not retroactive secrecy; W2–W5 non-inspection attestations and generator leakage tests remain mandatory.

### Sole remaining document blocker

B-D06's next action is not source-exact. The v0.2 manifest says **“adopt gateway, assemble composition”**.
The pinned `wfh-005/reports/triage.md` §3 instead says:

1. **ADOPT `github/gh-aw`** as incumbent baseline/reference implementation, explicitly as a recommendation
   to evaluate rather than deploy;
2. **ASSEMBLE** durable execution, an MCP gateway or AgentCore Policy, an AI gateway, SPIRE/Vault,
   OTel/Langfuse, and a sandbox; and
3. **BUILD exactly one residual** only after the two named unread cells are closed.

Calling the ADOPT object “gateway” moves an ASSEMBLE ingredient into a different route and changes the
historical decision. Correct B-D06 in the manifest and reference-label anchor to the three source-exact legs.
No new independent review is needed if that correction is mechanical and cites triage §3 verbatim.

### D15 work that is expected, not a present document defect

The absence of generated JSONL, packets, sealed mapping, digests, and executable leakage tests is not a
second v0.2 document failure: D15 intentionally puts datasets and extraction code on
`research/jurati-001`. After the B-D06 correction, W1 may proceed to that executable work.

The later final freeze gate cannot be skipped. It must verify the restricted opaque-to-real mapping,
source and packet digests, action-source spans, partition/cap/count invariants, clear-text identity/path and
reference-field leakage tests, verdict-summary contamination tests, adjudicator identity, non-inspection
attestations, and published aggregate counts/hashes. No language or prompt finalization may precede that
gate.

No sealed holdout verdict summary was inspected during this re-review and no Unimatrix write was made.
