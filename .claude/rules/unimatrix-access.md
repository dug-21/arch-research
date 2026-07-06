# Unimatrix Access Rules (factory agents)

Binding on every factory role that touches `context_*`. Source decisions: `product/factory/decisions.md`.

## ID resolution — pick the tool by intent (D5)

Unimatrix IDs are **version-pinned, not lineage-pinned**: `context_correct` reissues the id, and a
`context_get(stale_id)` returns the **deprecated** node (plainly marked `deprecated`, never silently
wrong). Choose by intent:

| Intent | Tool |
|---|---|
| Live/authoritative value, or resolve a stale id forward | `context_graph(mode:"current")` |
| Traverse relations, need the **edges** (topology) | `context_graph(mode:"neighbors")` — returns edge records only, even at `detail:"full"` |
| Traverse relations, need the **nodes hydrated** (e.g. the board — one call) | `context_graph(mode:"subgraph", seed_ids:[…], edge_types:[…], direction:…, detail:"full")` — filtered + hydrated |
| Lineage / supersession history | `context_graph(mode:"chain")` |
| A specific deprecated/historical version (audit, look-back) | `context_get(id)` |
| Active node + its edges, one call | `context_get(id)` |
| Discovery | `context_search` / `context_lookup(status:"active")` |

- **Default to `context_graph(mode:"current")`** for "what's true now." Never treat a `context_get`
  result as current without checking `status`.
- `context_graph` is the primary instrument (resolve · traverse · provenance); `context_get` is for
  pinned/deprecated reads and one-shot node+edges.

## Write discipline (curator only)

- Only the **curator** writes nodes (`context_store` / `context_correct` / edges). One writer keeps
  the firewall auditable.
- Updates go through **`context_correct`** (it deprecates + re-links); never deprecate-then-store.
- **Firewall (D7):** status → `proven` ONLY on an attached real artifact in `proven_by`, matching the
  claim's altitude and demonstrated by us. Research moves *structure*, never *status*.

## Edges (D8 — verified against the README)

Use only these six, mapped in methodology §5:

- `Advances` (capability → goal) · `About` (nfr → capability) · `Prerequisite` (technology → capability,
  also capability → capability) · `Motivates` (finding → technology) · `Supports` / `Contradicts`
  (finding ↔ finding).
- **Do NOT author `Cites` or `Tests` edges** — sources are a `cites:` field, proof is a `proven_by:`
  field. Artifacts and citations never become nodes.
- `Supersedes` is **system-only** (correction chains).
- **Factory plane:** `factory → factory` edges ONLY; cross-plane links are `cites:` field refs, never edges.

## Categories (D8)

- Research: `goal · capability · technology · finding · lesson-learned`. Process: `factory`.
- **Sources** = a `cites:` field on a `finding` (structured `{type, ref, title}`), not a category/node.
- **Decisions** = a `finding` tagged `position`, not a category.

## agent_id (D6 — open)

- Pass `agent_id` on every call (e.g. `{run-id}-{role}`). **Caveat:** attribution does not yet persist
  (writes record `created_by: anonymous`); treat audit attribution as not-yet-trustworthy until the
  platform agent registry lands.
- If calls are rejected unexpectedly, the MCP connection may have dropped — reconnect via `/mcp`.
