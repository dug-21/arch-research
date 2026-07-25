# FINDINGS — W6: Architecture re-assessment (which design carries the ontology?)

**Workstream:** W6 — comparative-architecture re-assessment · **Scope:** `wfh-002` (Issue dug-21/arch-research#46)
**Agents:** `wfh-002-w6-researcher-A/B/C` (three independent steelmans) + `wfh-002-leader` (synthesis)
**Status:** structure-only. No grades asserted, no `proven`, no artifact attached, no status moved. This decides a **representation/architecture** question; it does not touch the firewall. The ontology node (#180) stays `grade:claimed`.
**Owner-driven:** raised by the owner 2026-07-24 ("does this simply belong in a rules engine?"), decided 2026-07-25.
**Supersedes:** `SPEC-v0.3-delta.md` (the interim three-patch spec — its three additions collapse into this design's single seam; see §6).
**Companion:** `architecture-option-c.html` (the visual of the chosen design).

---

## §0 Why W6

W1–W5 refined a *specification* (the 5-node/4-edge ontology) through three stress tests and a domain-agnosticism probe. W5 surfaced three "structural" gaps (graded-state, budget, loop-until-dry), and the interim fix (`SPEC-v0.3-delta.md`) bolted three constructs onto the vocabulary to close them. The owner then asked the load-bearing question: **those three additions are all "evaluate a predicate / meter a quantity / drive a loop" — is that a rules engine wearing an ontology costume? What is the *simplest* design that enables our solution?**

**Goal (unchanged):** the simplest design that captures a coding-agent's operating context such that this repo's `.claude/` round-trips losslessly, it subsumes `AGENTS.md`, it stays domain-agnostic, and it feeds JURATI (the queen).

**Decision criterion (owner, verbatim intent):** *"Best = simplest that enables our capabilities, and is the easiest to manage / change the rules."* The **rule-change axis is the explicit tie-breaker.**

**Three candidate architectures assessed:**
- **A — typed graph alone** (the current hypothesis / v0.3 taken literally): the graph carries everything, governance as prose in bodies + v0.3's declarative hooks. No separate engine.
- **B — rules engine + relational/SQL**: model context *and* governance as rules over tables; drop the bespoke typed graph.
- **C — hybrid**: the typed graph **declares** the static operating context; a rules engine (the queen) **evaluates** the rules; the graph *references* named rules the engine owns.

Each was steelmanned by an independent researcher and required to make the strongest case **against** itself.

---

## §1 The three assessments (honest headlines)

### Option A — typed graph alone · simplest 4/5 · change-rules 3/5
Enables all four capabilities; three of them (round-trip, subsumption, agnosticism) strongly and natively. Governance is **bimodal**, not uniform: `cost_model` and `loop` are genuinely typed and deterministic; **the firewall and coverage *bars* are prose an LLM re-reads.** v0.3 pulled the branch *skeleton* into named objects (a real gain — a rule is now findable in one place), but by explicit design left the rule *content* as prose. So A can change any rule fast in one spot but **cannot prove the change took effect**, and the typed skeleton can silently drift from what's actually enforced (structure says `branches_on: floor`; enforcement is an LLM reading the prose). Its own steelman's verdict: A "renames buried prose to named prose" for the one rule that matters most (the firewall), and it re-implements a small rules engine **field-by-field, with prose leaves and no evaluator**. Honest floor: if you accept the owner's premise that rule-content is prose-plus-human by design, A is the true minimum and hard to beat on simplicity.

### Option B — rules engine + relational/SQL · simplest 3/5 · change-rules 4/5
Splits in two, and the whole verdict turns on which is meant:
- **B2 (drop the typed ontology, generic condition→action rules):** **rejected by its own steelman.** It dissolves exactly the defensible core wfh-001 identified (the moat is *the ontology + control-plane framing*, #169/#180). A bag of rules over tables is a commodity BRMS; the typed coding-agent operating-context ontology is the differentiator. B2 optimizes the change-axis by discarding the asset — a bad trade.
- **B1 (typed relational — same ontology as tables):** legitimate, arguably-simpler *storage* for the *same* ontology. Two findings matter here and generalize beyond B:
  1. **A rules *engine* in the knowledge substrate violates the deliberate enforcement seam** (jurati#12: enforcement/determinism/orchestration are queen-owned; ADR-008: the substrate is audit-only). So the engine is either the queen (out of this scope's representation question) or an illegal enforcer in the substrate. **Evaluation must be queen-side** — an architecture-level constraint on *every* option.
  2. **Storage (graph vs SQL) is not the real decision variable.** Both keep **git-native files as source of truth** (W3 §4 — a store that makes users edit rows instead of files fights the ecosystem the same way a 25th rules format would); the store is a derived index either way.
- One genuine technique to borrow regardless of option: **cost roll-up is cleanest as a recursive query** (`sum` for tokens/dollars, `max` for wall-clock across parallel branches).
- Correction to the framing premise: the three W5 gaps are **not** uniformly "rules-engine-shaped." Only **G-W2 (cost)** is; **G-W1 (graded state)** is a wash (a named reference either way); **G-W3 (loop)** is **control-flow the queen owns**, not a rule at all.

### Option C — hybrid (graph declares, queen evaluates) · simplest 4/5 (of the core) · change-rules 5/5
The seam is **P-C's definition/runtime plane boundary reified as a system boundary**, and it is **not new** — it is the split jurati#12 + ADR-008 already committed to, finally held consistently. The graph declares the nouns, the wiring, the opaque bodies, and — the one addition — **which named criteria each gate/step branches on** (`branches_on`, a *reference*, not the rule). The queen evaluates: floor/north-star tests, cost metering, loop-until-dry, escalation, the firewall verdict.

- **v0.3 collapses to a single seam construct.** Its four additions (`criteria`, `cost_model`, `branches_on`, `loop`) reduce to essentially one reference field; **floor, cost-cap, and loop-condition become three *examples* of "a named rule the engine evaluates,"** not three bespoke ontology features.
- **Wins the tie-breaker outright.** All three of the owner's named rule-changes (firewall bar / cost cap / coverage predicate) are **pure engine-rule edits with the ontology untouched** — deterministic, testable, auditable, versioned as engine artifacts, while the graph stays stable through rule churn. No candidate separates the stable part (structure) from the churny part (rules) this cleanly.
- **Preserves H4's defensible core** (the ontology) while handing governance to a *proper* engine instead of leaving it as un-evaluable prose.
- **Honest costs:** a formal **seam contract** (what a criterion reference means, what runtime state the engine may read, how a verdict returns) — owed anyway under jurati#12/ADR-008, but now explicit; and a **two-artifact worst case** when a *new* rule needs graph data it doesn't yet expose (the three named changes do **not** straddle — the frequent case is engine-only). The whole case rests on one premise: **the engine is a given (the queen), not a new system this option introduces.** Grant that — the architecture already does — and C is the best-of-both the criterion asks for.

---

## §2 The convergence (the real signal)

Each option's own steelman, forced to argue against itself, pointed at the same three conclusions:

1. **Keep the typed ontology — it is the moat** (#169/#180). "Replace the ontology" is rejected by the very argument for replacing it.
2. **Graph-vs-database is a storage detail, not an architecture.** Files stay source of truth (W3 §4); the store is an index. B collapses to "the same ontology, stored differently."
3. **Rule *evaluation* does not belong inside the definitions artifact** — it belongs to the queen. (B: an engine in the substrate breaks the seam; C: that is the thesis; A: its one unsolved hole is exactly the firewall rule it can't evaluate.)

So the three-way question collapses to **two**: do the rules live as **prose inside the graph** (A), or does the graph **name them and the queen evaluate them** (C)?

---

## §3 Scorecard (owner's two axes)

| Option | Simplest that enables | Easiest to change rules |
|---|---|---|
| **A — pure graph** | **4/5** — one artifact; but the firewall rule is prose + LLM, not enforceable | **3/5** — change the words fast; cannot verify the behavior changed; skeleton can drift from enforcement |
| **B — rules+SQL** | **3/5** — over-machinery for ~5 binary rules; de-typing (B2) kills the moat; simple only once reduced to "just tables" | **4/5** — great for cost/numeric rules; **evaporates at the firewall** (still prose+human); *shape* changes need schema migrations while the spec is still churning |
| **C — hybrid** | **4/5** — thinnest ontology (v0.3's 4 constructs → 1 seam); rests on "engine = the queen" | **5/5** — all three named changes are clean engine edits, ontology untouched; deterministic, testable, auditable |

---

## §4 Verdict

**Option C — the hybrid: the typed ontology *declares* on the graph; the queen (one rules engine) *evaluates* every rule and drives the run.**

**Load-bearing premise — CONFIRMED by owner 2026-07-25: the queen owns rule-evaluation.** This is the one input the whole verdict rests on; the researchers flagged it explicitly and the owner locked it.

Why C, not A (the honest runner-up): on the owner's tie-breaker it is not close (5/5 vs 3/5). A's typed skeleton is, for the firewall, decorative over an LLM — it makes the rule *visible*, not *binding*, and it grows a bad rules engine one field at a time. C gives the same declaration graph with **deterministic, testable, auditable rules** the moment the queen is present.

**Graceful degradation (why C is strictly "A-plus"):** hand the graph to a third-party tool with **no** queen, and the named rules fall back to prose that tool's own agent interprets — exactly where A already lives. Same floor when nothing is driving; deterministic rules when the queen is. C dominates A rather than trading against it.

**What C changes about the design:** the ontology gets *smaller*, not richer. v0.3's three patches (floor/cost/loop) collapse into the single `branches_on` seam; governance moves wholesale to the queen. Borrow one technique from the SQL assessment — cost roll-up as a recursive `sum`/`max` query — as an engine implementation detail, not an architecture choice.

---

## §5 What this does to H4 (boundary correction — record this)

**H4 (ontology-first) is refined, not refuted.** "A typed ontology is the load-bearing, defensible core" survives — the ontology is preserved intact and is still the moat. What is corrected is an unstated over-reach: **the ontology does NOT own its own governance.** The precise claim going forward:

> The ontology **declares** the operating context (nouns, wiring, opaque bodies) and **references** governance by name; a rules engine (the queen) **evaluates** the rules and drives the run. Declaration is the ontology's job; evaluation is the queen's.

This is a `partial`-shaped sharpening of H4 with a clean boundary, not a knock-down — and it *strengthens* the moat argument (the differentiator is the typed context ontology + control-plane framing, never a bespoke rules engine, which is a commodity).

**Adjacent (not in scope, noted):** this design is exactly the substrate H1 (control-plane-as-graph → wfh-003) would sit on — "one structure that both drives step order and renders the live trace." wfh-003 is sequenced strictly *after* wfh-002; recorded here only as the natural next layer, not pursued.

---

## §6 What this changes for the build (W4)

The artifact to build is no longer "a template whose graph contains the rules." It is:
1. **The declaration graph** — the typed ontology instantiating a new project's operating context, generating a git-native tree (still the `AGENTS.md`-generation proof bar, W3's Q-a — a third-party tool must consume it).
2. **The seam, demonstrated end-to-end** — the queen evaluating **one named rule** (the firewall floor is the flagship) against a real run: graph declares `branches_on: floor-of-X`, engine evaluates it, verdict returns and is enforced.
3. **Graceful degradation shown** — the same graph consumed with no engine, rules reading as prose.

`proven` still requires a real artifact demonstrated by us (the firewall is untouched). If the seam is only specified and not demonstrated, W4 lands `partial`, honestly. Standing risk carried from W2 (finding G-D): `factory-poc`/`factory-validator` agent-defs are undefined — substitute or define before the build.

The interim `SPEC-v0.3-delta.md` is **superseded** by this design; its three-patch content is retained there as the reasoning trail, with a pointer to this file.

---

## §7 Status / firewall

- No grade moved. No `proven`. No artifact. The ontology node (#180) stays `grade:claimed`.
- This is a representation/architecture decision (structure), the firewall's to keep. It is recorded as a `position`-shaped finding for the curator to distill (Option C chosen; H4 boundary-corrected).
- Companion visual: `architecture-option-c.html` (committed).

**Curator hand-off:** record (a) the architecture position (Option C — graph declares, queen evaluates) as a `finding` tagged `position`, `Motivates → #180`, `Supports → #164` (H4); (b) fold the H4 boundary correction (declares, not owns governance) into the #164/#180 narrative; (c) the load-bearing constraint "a rules engine in the substrate violates jurati#12/ADR-008; evaluation is queen-side" — a general architecture finding worth its own node. **No grade moves.**
