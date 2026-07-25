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

---

## CLOSE-OUT — wfh-002 closed early (`wfh-002-curator`, 2026-07-25)

Verdict recorded: **CLOSED EARLY (owner-directed) — reset to a broader investigation of the problem
space.** W4 was never executed; the proof bar was never met. Distilled from `REPORT.md`,
`SCOPE.md` (2026-07-25 amendment) and `FINDINGS-W6-architecture.md`. Note: the curator hand-off in
W6 §7 was written before the close decision and is superseded by the close-out brief — it was not
followed verbatim (it treated Option C as settled; it is not).

### Corrected (1)

- **#180 → #183** `technology` "JURATI typed operating-context ontology — SPECIFIED (5 nodes/4 edges)
  + stress-tested 3x; **wfh-002 CLOSED EARLY, no artifact**". Resolved live via
  `context_graph mode:"current"` before writing (#180 was the active terminal). Changes:
  - **Close recorded** — wfh-002 closed early 2026-07-25, W4 never built, no artifact exists, proof
    bar never met, root cause named (architecture chosen before purpose; W6 ran without a scope
    amendment against SCOPE §7's explicit out-of-scope boundary).
  - **Dead forward path removed** — the W5-era line "W4 gated on the v0.3 structural decision
    (G-W1/W2/W3)" is replaced: SPEC-v0.3-delta is superseded, W4 is not re-gated but *unscheduled*,
    and the forward path is now **gated on a broader problem-space investigation that defines the
    product purpose first** (successor run, separate session). G-W1/G-W2/G-W3 explicitly handed
    forward as **open gaps / evidence, not a build plan**.
  - **W1/W2/W3/W5 stress-test record kept intact** — flagged in-node as surviving the close on its
    own evidence.
  - **H4 boundary refinement folded in (W6 §5)** — the ontology *declares* the operating context and
    *references* governance by name; it does **not** own governance. Written explicitly as a
    **refinement, not a proof**, asserted under no artifact.
  - `proven_by:` restated as `(none)` with the reason (W4 never executed). Added `cites:` for
    `REPORT.md`, `SCOPE.md`, `FINDINGS-W6-architecture.md` alongside the existing W1/W2/W3/W5 cites.
  - **Grade unchanged: `grade:claimed`**, preserved via the correct's `tags` override —
    verified on #183: `[grade:claimed, technology, theme:workflow-harness, wfh-001, wfh-002]`.
  - Edges: **7 incoming Motivates auto-redirected** (0 failed); outbound `Prerequisite → #2`
    re-declared. Verified post-write: 1 outgoing / 9 incoming (7 redirected + #184 + #185).

### Stored (2 findings, both tagged `wfh-002`, topic `workflow-harness`)

- **#184** — `position`, **PROVISIONAL / NON-BINDING**: Option C (the typed graph *declares* the
  static operating context; the queen — one rules engine — *evaluates* every rule and drives the
  run). Records the criterion (simplest-that-enables + easiest-to-change-rules, with the rule-change
  axis as tie-breaker; 5/5 vs A 3/5, B 4/5) and the load-bearing premise (**the queen owns
  rule-evaluation**, owner-confirmed 2026-07-25 — if a successor's purpose changes what the queen
  owns, the position collapses with it). The node **leads** with its own not-settled warning: taken
  before the product purpose was defined, outside SCOPE §7 without an amendment, retained as
  reasoning trail only, does **not** bind the successor, which must re-derive architecture after
  purpose. Tags include `provisional`, `non-binding` so the caveat survives a tag-only read.
  Edges (verified live): `Motivates → #183`, `Supports → #164` (H4 — confirmed active before
  linking).
- **#185** — the durable, **purpose-independent architecture constraint**: a rules *engine* inside
  the knowledge substrate violates the deliberate enforcement seam (jurati#12 — enforcement /
  determinism / orchestration are queen-owned; ADR-008 — the substrate is audit-only), so **rule
  evaluation is queen-side**, a constraint on *every* candidate architecture rather than a property
  of one option. Carries the secondary result that **storage (graph vs relational) is not the real
  decision variable** — git-native files stay source of truth (W3 §4), the store is a derived index
  either way — plus the W5-gap-framing corollary (only the budget gap is rules-engine-shaped) and the
  recursive-query cost roll-up technique as an engine detail. Edge (verified live):
  `Motivates → #183`.

### Reuse decisions / justification

- **Reused #180 (→#183)**, no new tech node — the close is a status change to the *same* ontology
  line, consistent with the W2/W3/W5 folding pattern. Resolved live rather than assuming the id.
- **Reused #164 (H4)** as the `Supports` target for #184 — verified `Active` before linking.
- **Self-briefed before writing** (`context_search` on the enforcement-seam and graph-declares/
  queen-evaluates claims): nearest neighbors were wfh-001 hypotheses (#157 F2 enforcement-outside-
  the-LLM, #161 H1 control-plane-as-graph, #167 H7) and the #169 moat position — none asserts either
  new claim, so no correct-in-place candidate existed. Both new findings were stored, not folded.
- **Kept #184 and #185 as two nodes, not one.** Deliberate: #185 survives the close and binds the
  successor; #184 explicitly does not. Merging them would let a provisional option inherit the
  authority of a durable constraint — the exact failure this close-out is recording.
- **Corrected #183 rather than leaving the close as an edge-only leaf** — the close changes the
  node's *own* status and forward path (W4 unscheduled, purpose-first gating), which is node-level,
  not merely supporting.

### Chose NOT to store (and why)

- **The W6 scorecard, the three option write-ups, and the seam-contract detail** — workflow ≠
  knowledge; they stay in `FINDINGS-W6-architecture.md`. Only the position ABOUT them is graphed, and
  only enough of the reasoning to make its provisionality legible.
- **The ontology spec content and the v0.3 delta constructs** — unchanged policy from the earlier
  passes; they live in the FINDINGS files.
- **No successor `capability` node and no new research-scope Issue** — owner opens the successor in a
  separate session; out of the curator's lane.
- **No `factory-retro` extraction** — lessons, factory-plane enhancements, `OBS-*` and any `wf:` bump
  are owner-deferred to the successor session. Not performed, not partially performed.
- **No node for the process defect itself** (W6 crossing an unenforced scope boundary) — it is the
  method plane's material and belongs to the deferred retro; #179 already carries the general
  "unenforced prose invariant" finding this run's close instantiates.
- **No file edits, no commits** (OBS-7 — specialists don't persist; the leader does).

### Grade / firewall

**Nothing moved.** `grade:claimed` preserved on the ontology node (now **#183**), verified in the
post-write tag set. H4 (#164) untouched. **No `proven` anywhere** — W4 produced no artifact, and both
new findings assert no grade in their own words. The firewall is untouched by this close-out.

### Rate-limit note

**Zero `context_tag` calls** — no grade moved, and the correct preserved `grade:claimed` via its
`tags` override. Writes this pass: **1 `context_correct` + 2 `context_store`** (edges declared inline
at write time, so **0 standalone `context_edge` calls**). Nothing counted against the ~60/hour tag
budget.
