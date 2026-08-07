# jurati-001 — technology-discovery curation

**Curator:** `jurati-001-curator`  
**Phase:** tech-discovery  
**Issue:** #58  
**Outcome:** **1 claimed technology created, 2 claimed technologies reused; 0 proof-grade moves**

## Graph changes

| ID | Category | Disposition | Grade | Graph relation |
|---:|---|---|---|---|
| #256 | capability | created — evidence-bound decision evaluation and deterministic next-action resolution | `missing` | target of technology `Prerequisite` edges |
| #257 | technology | created — Jurati Decision Contract Language v0.1-dev | `claimed` | `Prerequisite` → #256 |
| #200 | technology | reused — ruflo `policy/` subtree and envelope algebra | `claimed` | `Prerequisite` → #256; tagged `jurati-001` |
| #202 | technology | reused — Bedrock AgentCore Policy + Cedar | `claimed` | `Prerequisite` → #256; tagged `jurati-001` |
| #258 | finding | created — provisional shared closed-clause kernel | n/a | `Motivates` → #257; supported by prior position #191 |
| #259 | finding | created — risk-weighted selective-classification protocol | n/a | `Motivates` → #257 |
| #260 | finding | created — sealed replay protocol-ready but execution-blocked | n/a | `Motivates` → #257 |
| #261 | finding | created — adversarial seams specified, not demonstrated | n/a | `Motivates` → #257 |
| #262 | finding | created — cross-domain corpus feasible, not freeze-ready | n/a | `Motivates` → #257 |

Every created entry carries `jurati-001`. Reused technologies #200 and #202 also received the run tag.
Capability and technology grades remain queryable tags; no grade was written into their content and no
`grade:proven` or `grade:partial` mutation occurred.

## Curation judgment

The discovery evidence warrants a coherent candidate capability and a claimed language technology, but
not a feasibility or product claim. W2 derives a compact candidate kernel from two development episodes;
W1 has not frozen the corpus; W3 has produced no interpreter; W4's empirical arms have not run; W5 cannot
launch sealed replay; and W6 specifies fixtures without executing them. The graph therefore records
structure only.

The two reused technologies are narrower prior-art components, not substitutes for #257. Ruflo #200
supplies a deterministic envelope/evaluator seam but is inert by default and lacks the cross-domain gate
language. Cedar/AgentCore #202 supplies deterministic schema-checked policy evaluation but authorizes tool
calls rather than expressing workflow verdict algebra and next-action transitions. Their reuse prevents
the Jurati node from laundering established deterministic-policy machinery as novel.

## Rejected or deferred claims

- Rejected `grade:proven` and `grade:partial` for all jurati-001 technology/capability nodes: there is no
  demonstrated-by-us artifact at the claim's altitude.
- Rejected any claim that the corpus is frozen. W1 and its independent review explicitly retain the D15
  generation, digest, leakage, mapping, attestation, and final human freeze gate.
- Rejected cross-domain expressibility, safety, next-action agreement, false-advancement, and least-cost
  judge-policy claims as empirical results. The current documents are specifications or preregistrations.
- Rejected creation of separate technologies for W4, W5, and W6. They are experiment protocols and safety
  suites that shape #257, not independently evaluated technology candidates.
- Deferred any `position` finding until synthesis, as required by the research-scope protocol.

## Provenance gaps and blockers

- Unimatrix rejected #262 when its two W1 repository citations included pinned commit URLs, reporting a
  phone-number PII detection. The retry retained the three supplied local-document citations exactly but
  omitted the two rejected repository citations rather than altering their refs. The complete supplied
  provenance remains in `findings-W1.md`; this is an ingestion/filter gap, not a source-quality ruling.
- W1's sole remaining document correction is B-D06's source-exact routing wording. Generated packets,
  sealed mapping, hashes, leakage tests, and the corpus-freeze gate remain outstanding.
- W4 arms B–E remain blocked by the absent local endpoint/model declaration and absent paid-inference
  authorization/model declaration. W4 also requires quantified human-reference cost.
- W3 is absent, so no interpreter, schema validator, deterministic reducer, transition selector, or replay
  artifact exists. This blocks empirical W4, sealed W5, and executable W6.

## Counts

- **T claimed:** 1 new technology (#257)
- **R reused:** 2 technologies (#200, #202)
- **Capabilities:** 1 new, `grade:missing` (#256)
- **Findings:** 5 new (#258–#262)
- **Corrections:** 0
- **Proof-grade moves:** 0

