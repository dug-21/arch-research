# W0-c — The four constraints (generation-surface input)

**Run:** `wfh-004` · Issue #48 · phase `scan` · authored by `research-leader` (restatement, not new research).
**Status:** these are **inputs to generation**, not decisions to relitigate. A lens may attack a constraint (that is exactly W2's job) but must do so by naming the mechanism that breaks it — not by ignoring it.

Carried from **wfh-002** (`product/research/wfh-002/FINDINGS-W{1,2,3,5,6}.md`), grounded in jurati#12 / ADR-008 / ASS-009.

---

## C-1 — Enforcement and evaluation are queen-side

A knowledge substrate cannot enforce. Unimatrix stores, ranks, and serves graded evidence; it does not
decide, gate, or block. The joint Unimatrix↔JURATI recommendation (**jurati#12**, **ADR-008**) makes this
a boundary, not a preference: putting enforcement in the substrate turns the knowledge engine into an
orchestrator, which #12 explicitly forbids.

- **Infeasible as written:** *"the graph enforces X."*
- **Available:** *"the harness enforces X"* — enforcement lives at the queen, outside the LLM context.
- **Generation consequence:** any candidate ability that reads *the store prevents / the store decides*
  must be restated with the harness as the actor, or it is a HOW dressed as a WHAT.

## C-2 — Semantic verdicts require LLM leaves

Any capability stated as *deterministically decides* a **prose** claim is infeasible as written. Whether
a paragraph of English satisfies a written criterion is not a computation the harness can perform; it
bottoms out in a model call.

- **Infeasible as written:** *"the harness deterministically decides whether the evidence supports the claim."*
- **Available:** *"the harness assists and records the decision with a forced-binary audit trail"* — the
  judgement is a leaf LLM call, but the *shape* of the decision (who was asked, what they were shown,
  what they answered, that they had to answer yes or no) is deterministic and durable.
- **Generation consequence:** the determinism budget buys **structure around** the verdict, never the
  verdict itself. Candidates should say where the LLM leaf sits and what is deterministic around it.

## C-3 — Files stay source of truth

(wfh-002 W3 §4.) The operating context lives in files — `.claude/` trees, markdown protocols, agent
definitions, skills. Any capability requiring users to edit **rows** instead of **files** fights the
ecosystem: it breaks git, review, diff, branch, and every editor and tool the user already has.

- **Infeasible as written:** *"the user maintains the workflow in the harness's database."*
- **Available:** the harness **derives**, **indexes**, **validates**, or **projects** from files; a
  canvas or graph is a *view* and a *round-trippable* projection, not the master copy.
- **Generation consequence:** a candidate whose value depends on owning the master copy carries the
  cost of defeating the file ecosystem, and must say so.

## C-4 — Capability gating is the one thing an LLM structurally cannot do to itself

The agent holds the credentials it would be restricting. Self-restriction by an entity holding the keys
is not a weak guarantee — it is **not a guarantee**. This is a **category difference**, not a gradient:
every other harness function (better context, better tracing, better cost attribution) is something an
LLM-driven harness does *worse*, and could in principle do better. Capability gating is something it
**cannot do at all**, no matter how well prompted or how disciplined.

- **Generation consequence:** C-4 is the worked example of **triage screen 6, "binary"** (SCOPE §7 W7) —
  structurally impossible elsewhere, rather than merely done better here. Candidates that share C-4's
  shape (an authority the actor cannot bound for itself) are the highest-value class this run can find,
  and lenses should be actively hunting for more of them.

---

## Standing caution for all five lenses

These four are **wfh-002's** constraints — a run that **closed early after drifting** from ontology
feasibility into architecture comparison. They are the most durable thing it produced, but they are
`claimed`, not `proven`. Treat them as strong priors with named mechanisms, not as physics. **W2
(constraint inversion) is chartered to attack all four**: for each, ask what becomes possible if it were
false or routed around, and say which are physics and which are merely current practice.
