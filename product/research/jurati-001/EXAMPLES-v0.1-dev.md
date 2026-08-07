# Jurati decision-contract examples — v0.1-dev

**Status:** provisional · **Corpus:** explicitly identified development episodes only

These examples test the shared semantics against `shd-007` and `wfh-002`. They are compact projections,
not replacements for W1 evidence packets or reference labels. Digests use syntactically valid placeholder
hex until W1 freezes exact artifact bytes; therefore evidence-integrity validation is intentionally
**blocked**, while structural validation is recorded below.

## Example A — shd-007 C1 firewall ruling

```json
{
  "language_version": "0.1-dev",
  "decision_id": "shd-007.firewall.c1",
  "revision": 1,
  "question": "Does the artifact clear capability C1's full done_when?",
  "contract_digest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "evidence": [
    {"evidence_id":"scope","media_type":"text/markdown","digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","locator":"product/research/shd-007/SCOPE.md","produced_by":"arch-research garage","admissibility":{"allowed_claims":["serving","coding","target-hardware"]}},
    {"evidence_id":"report","media_type":"text/markdown","digest":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","locator":"product/research/shd-007/REPORT.md","produced_by":"arch-research garage","admissibility":{"allowed_claims":["serving","coding","target-hardware"]}}
  ],
  "clauses": [
    {"clause_id":"serving","proposition":"The stack serves the required endpoint and sustained decode floor at stated context depth.","evidence_refs":["scope","report"],"evaluator":"semantic","policy_ref":"firewall-human","criticality":"blocking","rubric":{"demonstrated":"All required serving facts are evidenced.","contradicted":"Admissible evidence shows the serving requirement false.","not_demonstrated":"At least one required serving fact is unmet.","insufficient_evidence":"The packet cannot settle the serving requirement."}},
    {"clause_id":"coding","proposition":"A passing multi-file diff was produced through at least 6–8 sequential calls against the real proxy.","evidence_refs":["scope","report"],"evaluator":"semantic","policy_ref":"firewall-human","criticality":"blocking","rubric":{"demonstrated":"The required passing diff and call sequence are evidenced.","contradicted":"Admissible evidence establishes failure or invalidity.","not_demonstrated":"The required artifact or sequence is absent or unmet.","insufficient_evidence":"The packet cannot settle the coding requirement."}},
    {"clause_id":"target-hardware","proposition":"The demonstrated envelope is the selected target hardware.","evidence_refs":["scope","report"],"evaluator":"human_reserved","policy_ref":"firewall-human","criticality":"blocking","rubric":{"demonstrated":"The owner has selected this envelope as target hardware.","contradicted":"The owner identifies a different target envelope.","not_demonstrated":"Target hardware remains unselected.","insufficient_evidence":"The packet contains no authoritative target-hardware ruling."}}
  ],
  "reduction":{"algorithm":"blocking-conjunction-v1"},
  "transitions":{"pass":{"action_id":"grade-proven","kind":"advance","target":"c1.proven","authority_required":"firewall-owner"},"pass_with_advisory":{"action_id":"hold-for-advisory","kind":"escalate","target":"firewall-owner","authority_required":"firewall-owner"},"fail":{"action_id":"reject-c1","kind":"rework","target":"c1.rework","authority_required":"factory-leader"},"not_demonstrated":{"action_id":"record-partial","kind":"request_evidence","target":"c1.partial","authority_required":"firewall-owner"},"insufficient_evidence":{"action_id":"request-ruling","kind":"escalate","target":"firewall-owner","authority_required":"firewall-owner"}},
  "judge_policies":{"firewall-human":{"policy_id":"firewall-human","eligible":["human"],"repetitions":1,"independence":"not_applicable","agreement":"unanimous","on_disagreement":"abstain","on_abstention":"return_insufficient","max_escalations":0}}
}
```

Reference evaluation: `serving=demonstrated`, `coding=demonstrated`,
`target-hardware=not_demonstrated`. The reducer returns `not_demonstrated`; the only selected action is
`record-partial`. This reproduces the owner ruling without allowing strong evidence on two clauses to
erase the unmet trailing condition.

## Example B — wfh-002 close decision

```json
{
  "language_version":"0.1-dev",
  "decision_id":"wfh-002.close",
  "revision":1,
  "question":"May wfh-002 advance H4 as proven, and what is the declared next action?",
  "contract_digest":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
  "evidence":[
    {"evidence_id":"scope","media_type":"text/markdown","digest":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","locator":"product/research/wfh-002/SCOPE.md","produced_by":"arch-research garage","admissibility":{"allowed_claims":["artifact-built","scope-conformance"]}},
    {"evidence_id":"report","media_type":"text/markdown","digest":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","locator":"product/research/wfh-002/REPORT.md","produced_by":"arch-research garage","admissibility":{"allowed_claims":["artifact-built","scope-conformance"]}}
  ],
  "clauses":[
    {"clause_id":"artifact-built","proposition":"The proof-producing W4 template artifact was built and demonstrated.","evidence_refs":["scope","report"],"evaluator":"mechanical","criticality":"blocking","rubric":{"demonstrated":"W4 artifact and validation record both exist.","contradicted":"An integrity check invalidates the claimed artifact.","not_demonstrated":"The required artifact or validation record is absent.","insufficient_evidence":"Artifact locations cannot be inspected."}},
    {"clause_id":"scope-conformance","proposition":"Every binding architectural decision was authorized by the approved scope or an amendment.","evidence_refs":["scope","report"],"evaluator":"human_reserved","policy_ref":"owner-close","criticality":"blocking","rubric":{"demonstrated":"All binding decisions are in scope or amended in.","contradicted":"A binding decision crossed an explicit scope boundary without amendment.","not_demonstrated":"Required authorization is absent.","insufficient_evidence":"The packet cannot establish the authorization history."}}
  ],
  "reduction":{"algorithm":"blocking-conjunction-v1"},
  "transitions":{"pass":{"action_id":"advance-h4","kind":"advance","target":"h4.proven","authority_required":"firewall-owner"},"pass_with_advisory":{"action_id":"owner-review","kind":"escalate","target":"firewall-owner","authority_required":"firewall-owner"},"fail":{"action_id":"close-reset","kind":"stop","target":"broader-problem-space-investigation","authority_required":"owner"},"not_demonstrated":{"action_id":"request-proof","kind":"request_evidence","target":"w4","authority_required":"factory-leader"},"insufficient_evidence":{"action_id":"request-owner-ruling","kind":"escalate","target":"owner","authority_required":"owner"}},
  "judge_policies":{"owner-close":{"policy_id":"owner-close","eligible":["human"],"repetitions":1,"independence":"not_applicable","agreement":"unanimous","on_disagreement":"abstain","on_abstention":"return_insufficient","max_escalations":0}}
}
```

Reference evaluation: `artifact-built=not_demonstrated`; `scope-conformance=contradicted`. Precedence returns
`fail`, selecting `close-reset`. `stop` is not conflated with factual failure of W1–W3/W5, and the target is
authored before judging rather than invented by the assessor.

## Structural validation record

On 2026-08-07 both fenced JSON objects were parsed with `jq`, and these invariants were checked: unique
decision/evidence/clause IDs; every clause evidence reference resolves and is admissible for that clause;
the transition key set is exactly the five-verdict set; forbidden verdicts do not advance; policy
references resolve; and the reference result vectors reduce to the recorded verdict/action pairs.

**Blocked:** real contract/evidence digest verification awaits W1's frozen artifact paths and hashes.

## Citations

- type: docs · ref: `product/research/shd-007/SCOPE.md` · title: "shd-007 — Validated POC: local inference on owned hardware, and the first measured anchor for sizing" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/shd-007/REPORT.md` · title: "shd-007 — REPORT" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-002/SCOPE.md` · title: "wfh-002 — Minimal typed context ontology + git-native template" · org: arch-research garage · year: 2026
- type: docs · ref: `product/research/wfh-002/REPORT.md` · title: "REPORT — wfh-002 (close-out)" · org: arch-research garage · year: 2026
