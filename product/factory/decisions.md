# Factory Decisions Log

Append-only record of decisions made while building the research factory. During the
manual bootstrap, this file is the single source of "what's settled vs. what we still owe."
Locked decisions graduate to the Unimatrix `factory` plane (as ADRs / position findings)
once a real run validates them; provisional ones are revisited after the first run.

**Status legend:** `locked` (decided, in effect) · `provisional` (trying it, will reassess) ·
`open` (not yet decided) · `finding` (observed fact / carry-forward, not a choice).

---

## Summary

| # | Decision | Status | Eventual home |
|---|---|---|---|
| D1 | Three-surface model (Unimatrix / git / GitHub Issue) | locked | factory ADR (Uni) |
| D2 | Scope unit = per-capability | provisional | factory ADR after run 1 |
| D3 | Frontier-change protocol (re-entrant capability board) | locked | factory ADR + scope template |
| D4 | Scope template / required fields | locked | template file |
| D5 | Unimatrix ID-resolution + tool-selection rule | locked | `.claude/rules/` + lesson-learned |
| D6 | `agent_id` attribution gap | finding | carry-forward |
| D7 | Confidence-required axis (replaces Type) + firewall refinement | locked | factory ADR + scope template |
| D8 | Research category set; sources = `cites:` field; pattern/decisions stay off | locked | factory ADR (Uni) |
| D9 | Run 1 = `shd`, decompose then C2 directional, inline-roles | locked | — |
| D10 | Principle: architect for the future, build for now | locked | factory ADR (Uni) |
| D11 | Distributed multi-machine objective (architected now, build deferred) | objective | factory goal + shd N4 |
| D12 | Git strategy — two-stream, parallel-safe, auto-merge | locked | factory-git skill |

---

## D1 — Three-surface model
**Status:** locked · 2026-06-22

Work and knowledge live across three surfaces, each answering a **non-overlapping** question:

| Surface | Holds | Canonical question it owns |
|---|---|---|
| **Unimatrix** | settled, compounding, cross-goal knowledge | "Is the research proven? / what do we know?" |
| **Git repo** | provisional narrative + the real proof artifacts | "What's the draft / audit trail / POC artifact?" |
| **GitHub Issue** | live human↔factory dialogue + run operational state | "What is the run doing now / what does it need from me?" |

**Rule:** machine→Issue is render-only (a projection of the canonical stores, never source of
truth). The **one exception**: human inputs (approvals, redirections, comments) *originate* in
the Issue and must be distilled back into Unimatrix/git before they count — the Issue is to human
dialogue what `FINDINGS.md` is to research narrative. A human "looks good" in a comment moves
*structure*, never *status*; only an artifact moves status (the firewall, D-pending O1).

**Rationale:** prevents N drifting mirrors of "what's done." Exactly one canonical owner per
question; everything else is a labeled projection.

---

## D2 — Scope unit = per-capability
**Status:** provisional · 2026-06-22

A research **scope** targets at most one capability. The run decomposes into:
- one **decompose-scope** (1 Issue) → produces the goal + capability board in Unimatrix;
- one+ **research-scopes** per capability (1 Issue each) → discover → [feasibility] → prove the
  technologies for that capability → update Unimatrix.

Each scope = one GitHub Issue = one `context_cycle` topic (one ID across all three surfaces).

**Deviation noted:** methodology §14 runs a single **goal-wide** cycle. We run multiple
**capability-scoped** cycles instead, because (a) it matches the proven "1+ scopes deliver a
capability" pattern from the other project, (b) feasibility is per-technology in reality, and
(c) a frontier-discovered gap (D3) cleanly becomes a new scope-Issue rather than reopening a
closed phase.

**Provisional:** adopt and reassess after run 1. If goal-wide cycles prove simpler in practice,
revert.

---

## D3 — Frontier-change protocol (re-entrant capability board)
**Status:** locked · 2026-06-22

The capability board in Unimatrix **is** the durable work queue; the frontier query (§6) runs at
the start of every cycle, so anything written between cycles is picked up next round. Decomposition
is never assumed complete (§6 caveat #2). When research surfaces a gap:

| What surfaced | Action | New Issue? | Gate |
|---|---|---|---|
| Gap **inside** the current capability's envelope | curator updates the node (add child / sharpen `done_when`); append a **dated Extension** to the scope; continue | no | none |
| A **new capability** (expands surface) | curator writes a new 🔴 `capability` node + `Advances→goal`; open a **new scope-Issue** linked to the current one; it re-enters the frontier | yes | advisory ping if it shifts goal scope/budget |
| A **redefinition** that invalidates done work | sharpen `done_when`; if it reopens something `proven`, status reverts toward `partial` (envelope/process-defect logic, §4/§8) | maybe | firewall — log, don't hide |

**Enablers:** (1) every scope carries an explicit out-of-scope boundary, so "mine or new scope?"
is a check, not a judgment; (2) the goal `mode` tunes the absorb-vs-split threshold and reserves
re-decomposition budget (`targeted` → exception worth a human ping; `exploratory`/`open` →
re-decomposition is expected).

**Firewall-safe:** discovering a gap moves *structure* (a new `missing`/`claimed` node), never
status. Worst case the board grows, which is correct.

**Amendment discipline** (from the other project's proven practice): a dated Extension block is
**append-only** — never overwrite validated verdicts; explicitly reconcile any the extension changes.

---

## D4 — Scope template / required fields
**Status:** locked · 2026-06-22

Adapted from the other project's standard research-request format (e.g. ASS-083), plus
factory-specific additions.

**Header (required, every scope):**
- **ID** — `{program}-NNN` — the **canonical key** (= `context_cycle` topic = `feature_cycle` =
  file path `product/research/{id}/`). The GitHub Issue is **cross-linked by title, NOT by number
  equality** (GitHub auto-numbers repo-wide; e.g. `shd-002` = Issue #16). *[corrected 2026-06-23 — bootstrap learning]*
- **Title** — `Type: subject`
- **Status** — scope lifecycle: scoped → researching → [feasibility] → synthesis → done
- **Goal(s)** — primary + secondary; links to Unimatrix `goal` node(s)
- **Capability target(s)** *(factory add)* — the Unimatrix capability the scope advances (the queue item)
- **Confidence-required** — directional | empirical | validated (sets target status + proof bar; see D7)
- **Phase / area** — grouping tag

**Body (required sections):**
1. **The question** — with a one-sentence blockquote core
2. **Why it matters** — goal/vision alignment
3. **Known constraints & prior art** — "build on these — do not re-derive" (reuse-first)
4. **Bounded investigation (workstreams)** — `Wn`, each with an explicit `Output:` (the fan-out partition)
5. **Expected output** — enumerated FINDINGS deliverables
6. **Proof bar** *(factory add)* — what artifact moves a technology to `proven`; directional
   scopes state "structure-only, no status change" (see D7)
7. **Explicitly out of scope** — the boundary
8. **Coverage / done call** *(factory add)* — folded into synthesis: the loop-until-dry "researched enough" verdict

**Amendment:** dated Extension block, append-only, reconcile changed verdicts (D3).

---

## D5 — Unimatrix ID-resolution + tool-selection rule
**Status:** locked (proven this session) · 2026-06-22

Unimatrix surrogate IDs are **version-pinned, not lineage-pinned**: `context_correct` reissues the
ID (entry #1 → #2 this session). Empirically verified on the same lineage root (id:1):
- `context_graph(mode:"current", id:1)` → returns **#2** (terminal active) — resolves forward.
- `context_get(id:1)` → returns **#1**, plainly stamped `Status: deprecated`.

So storing a **raw Uni ID** as a cross-surface anchor (Issue/git) is safe — it resolves *forward*
to current or *holds* as the historical pin, depending on the tool. No stable-key tag needed; the
**procedure** carries it. Deprecated entries are clearly marked (not silently wrong), so look-back
is safe and useful (the deprecated #1 still shows the original `cabability` typo — frozen history).

**Agent tool-selection rule** (to bake into `.claude/rules/`):

| Intent | Tool |
|---|---|
| Live truth / resolve a stale id forward | `context_graph(mode:"current")` |
| Traverse relations | `context_graph(mode:"neighbors" \| "subgraph")` |
| Lineage history | `context_graph(mode:"chain")` |
| Fetch a specific deprecated/historical version | `context_get(id)` |
| Quick active node + its edges, one call | `context_get(id)` |
| Discovery | `context_search` / `context_lookup(status:active)` |

`context_graph` is the superset/primary tool (resolve · traverse · provenance · discovery-by-predicate);
`context_get` is for pinned/deprecated retrieval and one-shot node+edges reads.

**Field-projection note:** `graph mode:current` returns the fullest raw entry (content + hashes,
version, trust_source, usage telemetry) but **no edges**; `context_get` returns content + edges but
drops the integrity/telemetry fields. Minor wart: `graph` reports `status:"Active"`, `get` reports
`"active"` — don't exact-string-match status.

---

## D6 — `agent_id` attribution gap
**Status:** finding (carry-forward) · 2026-06-22

The `agent_id` passed to context tools does **not** land as attribution — writes recorded
`created_by: "anonymous"` / `trust_source: "agent"` regardless. The firewall's audit value depends
on knowing *which* agent wrote a node, so the platform agent registry must formalize how `agent_id`
becomes durable attribution before the audit trail is trustworthy.

Separately observed: an idiosyncratic backend interaction can reject calls until the MCP connection
is reconnected (`/mcp`); reconnect clears it. Not `agent_id`-related.

---

## D7 — Confidence-required axis (replaces Type) + firewall refinement
**Status:** locked · 2026-06-22 (supersedes O1)

Every scope declares **Confidence-required** — how far it must go before its deliverable counts as
done. This replaces the old "Type" field (dropped: too generic, not descriptive enough). The enum
is agent-facing — it reads naturally to the researcher closest to the work:

| Confidence-required | Scope owes | Status it can move | "Done" = |
|---|---|---|---|
| **directional** | findings + a reasoned recommendation / ranked map (a `position`) | structure only — technologies stay `claimed` | human accepts the direction (loop-until-dry K/N) |
| **empirical** | some real, **bounded** evidence | → `partial` | the bounded result is demonstrated |
| **validated** | a real artifact that clears `done_when` | → `proven` | firewall cleared |

Internal mapping the curator uses (researcher speaks in confidence terms; curator translates to
status): directional → `claimed`/findings · empirical → `partial` · validated → `proven`.

**Firewall refinement (the universal rule, now altitude-aware).** `proven` requires an artifact
that (a) **we demonstrated ourselves** and (b) **matches the claim's altitude**. Literature/theory
*by citation* never reaches `proven` — it stays `claimed`. But theory is **not** barred from
`proven`: a claim we **reproduce / derive / probe ourselves** is proven by that artifact (a worked
derivation, a reproduced calculation, a live API probe), even when no code ships. The proof bar
scales to the claim: runtime → benchmark; integration → smoke test; theoretical → reproduction.

Result: **one axis (Confidence-required) and one universal gate (the firewall)** — not a separate
"Type permits status" rule. Type is gone.

**Under-scope guard.** Confidence-required is self-declared, which invites under-scoping ("just call
it directional") to dodge the validated path. Guard: the **capability's `done_when`** sets the
*required* confidence, not the scope author. A behavioral `done_when` cannot be closed by a
directional finding — the capability stays `missing`/`claimed` until a `validated` scope produces
the artifact. Directional scopes advance structure and recommend; only a validated scope **closes**
a behavioral capability.

**Cleanup noted.** The goal-level `mode` field (§4: targeted | exploratory | linked | open) is
separate and stays — it tunes the frontier-change absorb/split threshold (D3). Its old
`poc-required` value is now subsumed by Confidence-required=validated at scope level; goal `mode`
reduces to character only.

---

## D8 — Research category set; sources as `cites:` field; pattern/decisions stay off
**Status:** locked · 2026-06-22

**Enabled research category set** (per methodology §13): `goal · capability · technology ·
finding · lesson-learned · factory` (factory sealed, `factory→factory` edges only;
`capability.kind: business | nfr`). The factory needs **no other categories**.

**Sources are NOT a category or a node.** A citation is a **`cites:` field on a `finding`**
(§2: "the paper/repo is not a graph node"; §4 finding schema = `content` + `cites:`). Treating
evidence artifacts as nodes is §2's single biggest named source of category bloat — avoided.

**Tailoring `finding`:** make `cites:` a **structured/typed list** (`{type, ref, title}` —
type ∈ paper/repo/dataset/docs/blog) rather than free prose, so citations are machine-parseable
for later dedup/dashboards while staying "field, not node." Confirm `finding` supports the
`position` tag (selection findings) and adaptive lifecycle decay (§13).

**Pattern and decisions stay OFF.**
- *Decisions* are not a category — a `finding` tagged `position` (see D7 / §2). Re-enabling
  reintroduces bloat.
- *Pattern* is SDLC/implementation knowledge (`uni-store-pattern` is a delivery tool), not in the
  research taxonomy; an agent would mislabel it against `finding`/`lesson-learned`.

**Known limitation (accepted):** `cites:`-as-field means no cheap graph query for "all findings
citing paper X" or source-level dedup — sources aren't first-class. Accepted on purpose (keeps
findings inert in retrieval, §2). If source-level dedup later becomes load-bearing, the fix is
**structuring the `cites:` field**, not adding a source category/node.

**Config caveat:** Unimatrix currently has **no way to query available categories**; the enabled
set is human-confirmed, not machine-verified. Edge types are documented in the Unimatrix README
(github.com/dug-21/unimatrix).

**Edge set verified (2026-06-22)** against the README: all six §5 edges exist natively
(`Advances`, `About`, `Prerequisite`, `Motivates`, `Supports`, `Contradicts`), among 13
agent-declarable types. Confirmed: `Supersedes` is **system-only** (correction chains, not
agent-authored); **no per-category edge constraints** (so `technology→capability Prerequisite`
is native — §5/§11). Deliberately-unused alternatives the curator must avoid: `Cites` exists as
an *edge* but sources stay a `cites:` **field** (D8); `Tests` exists but proof routes through the
`proven_by:` **field**, never a `Tests` edge — keeps artifacts out of the graph as nodes.

---

## D9 — Run 1: goal `shd`, capability C2, directional, inline-roles  (resolves O2)
**Status:** locked · 2026-06-22

First manual run:
- **Goal:** `shd` — self-hosted dev/research capability (methodology §12). `mode: poc-required`.
- **Run mode:** inline-roles — operator plays leader/researcher/curator; human approves the 3 gates.
  No agent defs spawned (Tier 1, deferred until run 1 *defines* their contracts).
- **Decompose-scope (`shd-001`):** seed goal + capability board (C1/C2/C3 + NFRs N1–N3 from §12,
  **plus N4 distribution-compatibility per D11**) into Unimatrix (curator, structure-only, all
  `missing`/`claimed` — firewall-safe).
- **Research-scope (`shd-002`):** capability **C2** "an agentic harness drives research+coding tasks
  to completion," **Confidence-required: directional** — produces a ranked technology landscape +
  recommendation; no POC, no status change.
- **Run 2 (later):** a `validated` scope on whatever C2-directional recommends — the first real test
  of the feasibility/firewall machinery.

**Rationale:** a real research question with genuine unknowns (better than the reflexive "build the
factory," which is engineering not research — §2), already sketched in §12 so we debug the *method*
not the *subject*, and `directional` keeps run 1 within a near-zero budget.

**Tier-0 build (done 2026-06-22):** `product/factory/templates/scope.md` (D4+D7) ·
`.claude/rules/unimatrix-access.md` (D5+D6+D8) · `product/factory/runbook.md` (run procedure +
Issue conventions). Reuses `uni-capability` for decompose; the six factory agent defs + factory
protocols stay Tier 1.

---

## D10 — Principle: architect for the future, build for now
**Status:** locked (governing principle) · 2026-06-23

**Architect for the future; build for now.** Future-state objectives are **recorded in the
structure as visible goals/NFRs** so everyone knows the target — even when we consciously **defer
the build**. Deferral is an explicit, logged decision made along the way, never a silent omission.

Corollary (ties to D7): a future NFR constrains present choices as *"must not preclude / must not
require re-foundation,"* **not** *"must be built now"* — so it informs selection without inflating
present scope or budget. Applies to every factory architecture decision (D1–D9 and onward) and to
research technology selection. First application: D11.

---

## D11 — Distributed multi-machine objective (architected now, build deferred)
**Status:** locked as objective; build deferred · 2026-06-23

Long-term goal: a **coordinated research/development capability distributed across multiple
machines**, automated in **waves** (wave 0 = today's manual, single-operator factory). Two faces:

- **Factory process plane:** the factory itself becomes distributed + automated — the north star
  behind "manual now, automate in waves." Informs D1–D9 (e.g. the three-surface model, scope IDs,
  and `context_cycle` topics must not assume a single operator or single host). Recorded now; the
  `factory/goal` node + wave roadmap are authored when the factory plane is set up (Tier 1).
- **Research subject (`shd`):** the self-hosted stack scales across multiple *owned* machines
  (still sovereign, just bigger). Encoded as shd **N4** — *"the self-hosted stack extends to
  coordinated multi-machine operation without re-foundation,"* `About→ C1, C2, C3` — so directional
  C2 harness research weights distribution-compatibility.

Build deferred per D10; distribution-compatibility is a **tie-breaker/flag, not a hard gate**,
until a wave targets it. N4's `done_when` reads *"does not foreclose multi-machine coordination,"*
never *"achieves distribution."*

---

## D12 — Git strategy (two-stream, parallel-safe, auto-merge)
**Status:** locked · 2026-06-23

Adapted from `uni-git` (which is SDLC-shaped); a sibling **`factory-git`** skill will encode this.

**Two change-streams, never mixed in one commit** (so a research commit never moves the `wf:` version):
- **Method stream** (`.claude/**`, `product/factory/**`): the versioned workflow artifact (§7–8).
  `workflow/{desc}` branch → PR → main — reviewable, because it ripples to every future run. The
  method carries a **semver `wf:<version>`**, bumped on each method-PR merge — **NOT a HEAD SHA**
  (research commits also move HEAD; `wf:` must move only when the method changes; §8 allows semver).
  This session establishes **`wf:v0.1`**.
- **Research stream** (`product/research/{scope-id}/**`): per-scope. `research/{scope-id}` branch →
  PR that `Closes #<issue>` → **auto-merge (rebase)** after the synthesis gate (already human-reviewed
  on the Issue).

**Parallelism discipline (the load-bearing rule):**
- **Commit only your own paths — NEVER `git add -A` / `git add .`.** Each scope/agent stages only the
  files it owns (e.g. `git add product/research/{id}/`), so parallel scopes/agents commit
  concurrently without sweeping each other's WIP.
- **Always commit your work** before yielding — no uncommitted WIP left behind.
- Scopes live in **disjoint directories** → parallel branches rebase-merge to main conflict-free.
- *(Unimatrix side: each run's curator writes only its own scope's nodes; concurrent runs touch
  distinct entries — additive, no contention. Frontier-change to the shared board is append-only.)*

**Config:** rebase-only merge; auto-merge enabled at repo level; `.gitignore` excludes secrets,
build artifacts, **local model weights/venvs (shd-003)**, `.claude/worktrees/`,
`.claude/settings.local.json`. No worktrees for read-only research fan-out (revisit for the shd-003 POC).
