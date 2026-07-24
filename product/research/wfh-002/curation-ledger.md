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

---

## W5 — domain-agnosticism distillation (`wfh-002-curator`, 2026-07-24)

### Corrected (1)

- **#176 → #180** `technology` "JURATI typed operating-context ontology — SPECIFIED (5 nodes/4 edges) + stress-tested" — folded the W5 verdict into the node. Changes: "Stress-tested **twice** → **three times**" with a W5 bullet (AGNOSTIC-WITH-GAPS: no type collapse, no dead type, all 4 edges load, firewall types as a `gate` → rules out SDLC-locked; skeleton = actor/action/checkpoint/instrument/instruction; holes G-W1 graded-state, G-W2 budget, G-W3 loop + G-W6 SDLC-worded definitions; digitally-mediated `tool` caveat). Added a v0.3 line and updated `proven_by`/downstream to record **W4 is now gated on the v0.3 structural decision (G-W1/W2/W3)**. Added the W5 FINDINGS cite. **Grade unchanged: `grade:claimed`** (no artifact — grade tag preserved via correct's `tags` override; firewall untouched). Edges: 6 incoming Motivates auto-redirected (#156, #161, #164, #177, #178, #179); outbound `Prerequisite → #2` re-declared.

### Stored (1 finding, tagged `wfh-002`, topic `workflow-harness`)

- **#181** — W5 verdict: **AGNOSTIC-WITH-GAPS**. Second, non-software domain (our own research method, from its PROSE design, not `.claude/`) round-trips the 5/4 vocabulary → SDLC-locked ruled out; skeleton is the domain-neutral slots. Three structural general-workflow holes SDLC never stressed (G-W1 graded-state / G-W2 budget-envelope / G-W3 convergence-loop) + G-W6 prose leakage; load-bearing contrarian caveat that the `tool` round-trip was flattered by our instruments being software. **No grade asserted** (structure, no artifact). Edges: `Motivates → #180`, `Supports → #164` (H4) — both verified live.

### Reuse decisions / justification

- **Reused #176 (→#180)**, did not create a new tech node — W5 is another stress test of the same ontology, consistent with the W2/W3 folding pattern.
- **Chose to correct rather than leave W5 as an edge-only leaf:** W5 changes #176's *own* claims (third held stress test; stale "twice" count) and, decisively, its forward path — `proven_by`/downstream now record W4 gated on a v0.3 decision. That is node-level status, not a mere supporting finding.
- **Reused #164 (H4)** as the `Supports` target — confirmed live before linking.
- **Did NOT store** the expressed graph (§1), the gap-table (§5), or the ontology spec content — workflow ≠ knowledge; those stay in the FINDINGS file. Only the verdict ABOUT the ontology is graphed.

### Grade / firewall

`grade:claimed` unchanged on the ontology node (now #180). **No `proven` anywhere** — W5 produced no artifact.

### Rate-limit note

**Zero `context_tag` calls** this pass — grade did not move; `context_correct` preserves the grade tag via its `tags` override. Writes: 1 correct + 1 store.
