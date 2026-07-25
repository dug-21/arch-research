# SCOPE — wfh-002

**ID:** `wfh-002` — canonical key (= `context_cycle` topic = `feature_cycle` = path `product/research/wfh-002/`). GitHub Issue cross-linked by title, **opened by the execution session** (not here — plan-only).
**Title:** `research(validated): the minimal typed ontology of a coding-agent's operating context (P10 probe)`
**Status:** approved — owner approved 2026-07-22 (first gate passed); execution started under `wf-v0.16`.
**Theme / value-target:** `theme:workflow-harness` → JURATI (`dug-21/jurati`). Advances **H4** (ontology-first); relates **H7** (definition store), **H5** (portability).
**Confidence-required:** **validated** — must produce a real artifact demonstrated by us; can move H4 toward `proven`, or land `partial` + a characterized gap list.
**Phase / area:** workflow-harness · ontology.
**Prerequisite:** wfh-001 closed (triaged + survivors formalized to the graph) — its candidates are this scope's prior art.

## 1. The question
> Can a **minimal typed vocabulary** — nodes {skill · agent-def · step · gate · tool}, a few edges {invokes · depends-on · gated-by · injects} — capture a coding-agent's operating context such that (a) **THIS repo's own `.claude/`** expresses in it with **no loss**, and (b) it **subsumes the `AGENTS.md` standard** — proving the ontology H4 depends on, cheaply, via a git-native template (P10)?

## 2. Why it matters
The ontology is the **load-bearing, defensible core** of the theme — wfh-001's white-space verdict found the moat is the *coding-agent-context ontology + control-plane framing*, not the visualization. The canvas (H1/H2), context injection, portability/anti-lock-in (H5), and the delivery model all sit on it. This is the cheapest test that produces a **real artifact** and moves the firewall — independent of the tenancy decision.

## 3. Known constraints & prior art (build on — do not re-derive)
- **wfh-001 scan** (`product/research/wfh-001/scout-candidates.md`): the shipped mechanisms to generalize from — rules-files / `AGENTS.md` (user-owned, tool-injected; near-universal standard), skills (Claude Code / Amp / OpenHands), agent-defs / subagents, **gates** (Claude Code hooks, OpenHands SecurityAnalyzer, Copilot branch/PR, Factory exit-code tiers, Cline plan-mode), Recipes/Playbooks (portable workflow artifacts).
- **`AGENTS.md` is the de-facto standard** — the ontology MUST subsume it losslessly or it fights the ecosystem.
- **workflow ≠ knowledge (three stores)** — the ontology is queen-side *workflow-definition*, NOT Unimatrix knowledge; do not store it as graded knowledge.
- **issue #12** (JURATI queen): gates are enforcement *outside* the LLM — the `gate` node type derives from this.
- **Reference UX** (not built here): Cannoli `LoggingEdge`; Claude Code `/context` and its 4 gaps.

## 4. Bounded investigation (workstreams)
- **W1 — Ontology spec.** Draft the typed node/edge vocabulary from §3's mechanisms + the issue-#12 gate concept. *Output: the ontology spec (nodes, edges, required fields).*
- **W2 — Lossless round-trip.** Express this repo's `.claude/` (skills, `agents/factory/*`, rules, workflow protocols, CLAUDE.md) in the vocabulary; verify no loss (can the operating behavior be reconstructed?). *Output: the expressed graph + a gap list.*
- **W3 — `AGENTS.md` subsumption.** Map the standard into the vocabulary; confirm lossless. *Output: mapping + gaps.*
- **W5 — Second-domain round-trip (domain-agnosticism probe).** Express our **own research-factory method _as designed_** — the garage funnel (scan → triage → prove), its phases, roles, human/firewall gates, and the evidence-grading discipline — in the SAME vocabulary (v0.2). **Source of truth = the method's prose design** (`docs/research-factory-methodology.md` + funnel narrative), explicitly **NOT** its `.claude/` config implementation, which would silently re-test the software domain. *Output: the expressed graph of the research method + a domain-fit verdict (agnostic / SDLC-locked) with a gap list.* **Precedes W4** — the build hardens the vocabulary, so agnosticism must be settled first.
- **W4 — P10 template artifact.** Package the ontology as a git-native template + devcontainer that instantiates a new project's operating context from the vocabulary. *Output: the working template — the real artifact.* **Gated on W5** — build only after the vocabulary is shown domain-agnostic (or its gaps characterized).

## 5. Expected output (FINDINGS deliverables)
- The ontology spec (W1).
- Round-trip result: pass / gap list (W2).
- `AGENTS.md` subsumption verdict (W3).
- The P10 template artifact + a run showing it instantiates a new project (W4).
- A `position` finding on **H4**: proven / partial (+ gaps) / refuted.

## 6. Proof bar (what moves H4)
A real artifact, demonstrated by us: this repo's `.claude/` round-trips through the vocabulary with **no loss** AND `AGENTS.md` **subsumes** AND the template **instantiates** a new project → **validated** (H4 → proven). Any lossy gap → **partial** + the characterized gap list. Literature / assertion moves nothing.

**Domain-agnosticism precondition (W5, amendment 2026-07-24).** The vocabulary must round-trip a **second, non-software domain** (our own research method, expressed from its prose design) before W4 hardens it. Clean second-domain round-trip → agnosticism supported, proceed to build. Lossy/over-fit → characterize the gap (and, if structural, revise the spec to v0.3) before building. A vocabulary that only fits SDLC does not deserve a general template.

## 7. Explicitly out of scope
The UX canvas (T2 — later); the delivery/tenancy model (T4 — P14 settled, rest deferred); the runtime / execution engine (the queen's job, not this scope); multi-LLM portability testing (H5 — later); **any JURATI production code** (that's the §7 handoff to `dug-21/jurati`, not build-here).

## 8. Coverage / done call
The round-trip, subsumption, and template are objective artifacts (not loop-until-dry): done when they pass, or the gaps are fully characterized. Human confirms at synthesis.

## Amendments
*(append-only, dated; reconcile any changed verdicts — D3)*

- **2026-07-25 — CLOSED EARLY (owner-directed). Verdict: reset to a broader investigation of the problem space.**
  **Status: closed — no proof.** W4 (the artifact) was never executed, so the §6 proof bar was never met: no artifact, no `proven`, **H4 remains `claimed`**. The run is not SCOPE-FAIL (W1–W3 + W5 all returned usable verdicts); it is an owner-directed early close.
  **Why.** Architecture was chosen before the product's full purpose was defined. The mechanical expression of that: **W6** (comparative-architecture re-assessment, owner-raised 2026-07-24, decided 2026-07-25) ran **without an amendment to this scope** and decided a question §7 had explicitly placed **out of scope** — the runtime/execution engine, "the queen's job, not this scope." The guardrail existed in this document and was unenforced prose; nothing stopped the crossing. (Noted for the record: this run's own finding #179 had just established that this repo's cardinal invariants are 100% unenforced prose. wfh-002 then failed in exactly that way.)
  **Disposition of W6.** Its Option C verdict (graph declares, queen evaluates) is retained in `FINDINGS-W6-architecture.md` as reasoning trail and is recorded in the graph as **provisional / non-binding** — it does not bind the successor. The one durable, purpose-independent constraint it produced (a rules engine inside the knowledge substrate violates the jurati#12 / ADR-008 enforcement seam; evaluation is queen-side) is graphed on its own.
  **Successor.** A broader problem-space investigation, opened in a separate session. wfh-002 hands it evidence, not an architecture.
  **Deferred, not done here (owner):** the `factory-retro` method-plane extraction and any `wf:` bump — the successor session's lane.

- **2026-07-24 — W5 added (owner-authorized), W4 gated on it.** Owner raised the load-bearing question: is the ontology SDLC-specific? W1–W3 tested only software-development artifacts (this repo's coding-agent config + `AGENTS.md`). The vocabulary is domain-agnostic *by design* (typed on control semantics — actor / action / checkpoint / instrument / instruction — not file format), but *evidenced* in one domain only. **W5** adds a second-domain round-trip against our own research method (from its prose design, not its config) to test agnosticism directly. Sequencing changed to **analyze-then-build**: W5 precedes W4; W4 proceeds only once agnosticism is demonstrated or its gaps characterized. Naming-alignment with agentic tooling (skill/agent-def/tool vs. capability/actor/instrument) is **parked** per owner — agnostic *meaning* under familiar *names* is acceptable for now. Coverage gate now spans W1–W3 + W5.
