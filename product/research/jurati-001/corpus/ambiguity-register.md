# Corpus ambiguity register

No item below may be silently converted into model error. `AR-*` items require independent review before
the corpus-freeze gate.

| ID | Episodes | Ambiguity | Required adjudication |
|---|---|---|---|
| AR-01 | A-D05 | Initial and rework gate-3b reports coexist. | Confirm initial verdict/action and whether rework1 is one later decision or merely amended evidence. |
| AR-02 | A-D06–07 | A failing earlier gate and later final pass can hide intermediate decisions. | Reconstruct chronology from git/report dates; label only actions actually taken. |
| AR-03 | A-D11–15, A-C03–08 | WARN/FAIL tokens occur in clause text as well as overall verdicts. | Read full reports; do not classify with regex. |
| AR-04 | A-C01 | Report says re-validation PASS. | Decide whether the episode is the initial failure, re-validation, or two episodes; packet must preserve chronology. |
| AR-05 | A-H* | Holdout outcomes are intentionally absent from main. | Reviewer writes sealed labels directly to generated branch artifact; record hash only at gate. |
| AR-06 | B-D01 | Strong artifact supported a draft `proven`, but target-hardware clause was unmet. | Reference is owner's `partial`; preserve rejected draft as disagreement evidence. |
| AR-07 | B-D03–04 | `wfh-002` failure combines boundary enforcement and product disposition. | Confirm two questions are independently labelable; otherwise merge or exclude one before freeze. |
| AR-08 | B-D05–06 | Amendment may supersede rather than follow triage. | Establish whether these are two decisions or one corrected decision lineage. |
| AR-09 | B-D07 | Findings may recommend a direction without evidence of executed next action. | Distinguish prescribed from observed action; exclude if no bounded consequence exists. |
| AR-10 | B-C01–03 | Research reports use directional language rather than a common verdict enum. | Quote the question and action; avoid forcing PASS/FAIL. |
| AR-11 | B-H* | Holdout outcomes and owner intervention are sealed. | Independent reviewer confirms labels and stores only their aggregate/hash on main. |
| AR-12 | corpus-wide | Some historical next actions are inferred from the next artifact. | Mark `observed`, `explicit`, or `inferred`; inferred actions need two-source corroboration. |

## Independent-review acceptance rule

A reviewer who did not select or extract the episode must compare the pinned source packet with the proposed
label. Disagreement is resolved by retaining both readings and either (a) an owner ruling, (b) a third
reviewer, or (c) exclusion. The selector may not break a tie. Reviewer identity and rationale are mandatory.
