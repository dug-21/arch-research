# Curation ledger — wfh-002 tech-discovery

**Curator:** `wfh-002-curator` · **Phase:** tech-discovery distillation · **Date:** 2026-07-22

## Corrected (1)

- **#170 → #176** `technology` "JURATI typed operating-context ontology — SPECIFIED (5 nodes/4 edges) + stress-tested" — reused the wfh-001 node, no duplicate. Content now records: W1 spec exists (5 types, 4 edges, P-A/P-B/P-C, minimality argument), W2 PASS-WITH-GAPS, W3 SUBSUMES non-vacuously; W4 proof bar stated in `proven_by: (none)`. Cites all three FINDINGS files. **Grade unchanged: `grade:claimed`** (no artifact, so no partial/proven). Tags: `[grade:claimed, technology, theme:workflow-harness, wfh-001, wfh-002]`. Incoming Motivates (#156, #161, #164) auto-redirected to #176; outgoing `Prerequisite → #2` (capability) re-declared.

## Stored (3 findings, all tagged `wfh-002`, topic `workflow-harness`)

- **#177** — W2 round-trip verdict: PASS-WITH-GAPS; gap-list shape (6 behavioral — only G-A LLM-arbitered gates + G-B missing condition construct are genuine vocabulary holes; 2 byte gaps closed by one bytes-canonical P-B rule). Edges: `Motivates → #176`, `Supports → #164` (H4).
- **#178** — W3 subsumption verdict: file→graph lossless vs the standard; graph→file total-but-projective as falsifiable rules; ≥2 divergent precedence semantics in the wild (closest-wins vs Codex concat); W4 exit bar sharpened. Edges: `Motivates → #176`, `Supports → #156` (F1).
- **#179** — S4 exposure: this repo's cardinal invariants (single-writer, plan-only, no `git add -A`) are 100% unenforced prose — zero permission rules, zero enforcing hooks; repo gap, not vocabulary gap. Edges: `Motivates → #176`, `Supports → #157` (F2).

## Tags

Run-id `wfh-002` on all four writes; `grade:claimed` preserved on #176 via the correct's tag set (no grade moved anywhere). Findings carry no grade tags (grades index capability/technology only).

## Chose NOT to store (and why)

- The ontology spec's content (types, fields, edge definitions) — workflow ≠ knowledge; it lives in FINDINGS-W1 / future JURATI store. Only verdicts ABOUT it are graphed.
- W2's expressed graph (§1 inventories) and W3's generation rules (§3) — same reason; W4 consumes them from the files.
- A separate finding for the byte-bar gaps (G-G/G-H) — folded into #177; one spec sharpening, not an independent verdict.
- (a)+(b) kept as two findings, not merged: distinct claims (internal expressiveness vs external subsumption), distinct support targets (H4 vs F1), distinct citations.
- No grade moves on any other wfh-001 node; no `proven` anywhere — firewall untouched, W4's gate.
