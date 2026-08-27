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

- Only the **curator** writes nodes (`context_store` / `context_correct` / `context_tag` / edges).
  One writer keeps the firewall auditable.
- **Content/edge updates** go through **`context_correct`** (it deprecates + re-links + **reissues the
  id**); never deprecate-then-store.
- **Grade (firewall status) is a `grade:` tag, mutated by `context_tag`** — `action:"replace",
  tag:"grade:<missing|claimed|partial|proven>"` sets-or-swaps the grade **in place** (no id reissue,
  content/edges/embedding preserved; idempotent, namespace-scoped). Use it for every missing/claimed/
  partial move. `grade:` is distinct from the DB `status` field (lifecycle `active`/`deprecated`) — never
  put the grade in a tag literally named `status`. **Rate-limited ~60 tag-writes/hour** — a large grade
  sweep/backfill must batch under that.
- **Firewall (D7):** grade → `proven` ONLY on an attached real artifact in `proven_by`, matching the
  claim's altitude and demonstrated by us — and **`proven` is set via `context_correct`** (attach the
  artifact) **in the same step as `grade:proven`, never a bare `context_tag`**. Research moves *structure*
  (and non-proven grades), never *proof*.

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
- **Sources** = a `cites:` field on a `finding`, not a category/node. **Structured, with provenance (D14):**
  `type` (`paper|repo|product|standard|dataset|docs|blog`) · `ref` · `title` — all required; then
  `author` (`Surname; Surname`) · `org` · `year` where known, plus optional `venue` and `surface`
  (`literature|products|active-dev|adjacent`). **Omit an unknown key — never invent one.** `org` is the
  primary aggregation key. Full schema: methodology §4. This structures the field; it does **not** make
  sources nodes, and `Cites` edges stay forbidden.
- **Decisions** = a `finding` tagged `position`, not a category.

## agent_id (D6 — corrected 2026-08-27)

- Every agent/skill that touches Unimatrix defines a stable `agent_id` equal to its agent type (for
  example `research-leader`, `hypothesizer`, `factory-curator`). The run-id belongs in `topic`,
  `feature_cycle`, and tags — never splice it into identity.
- Pass that defined value on every `context_*` call. **It is mandatory repository policy on every call
  that can mutate Unimatrix**: content, edges, tags, lifecycle, cycle events, and review calls that may
  auto-close. `context_store` and `context_correct` additionally reject anonymous/missing identity at the
  server boundary; other tools may accept omission, but our agents never omit it on writes.
- Repeat the rule in each writer's loaded role/skill. This file is the shared semantic reference, not the
  only place an agent is expected to discover its identity.
- **It persists.** `created_by` carries the string you passed — verified on live nodes 2026-08-21
  (#266 records `jurati-001-retro-curator`; #97 and #260 likewise populated). **The former caveat that
  writes record `created_by: anonymous` is struck: it is no longer true, and it was cited across
  wfh-007 as grounds for conclusions that need re-reading.**
- **But it is persisted self-assertion, not attestation, and that distinction is the whole point.** The
  value is whatever the caller typed; nothing verifies the caller is who it claims. Attribution is
  therefore reliable for **reconstructing what happened** and unreliable for **establishing who is
  accountable** — it will not survive a party with a motive to misattribute.
  **Do not build an authority check on it.** A guard whose input is a field the guarded party writes
  is defeated by editing that field.
- If calls are rejected unexpectedly, the MCP connection may have dropped — reconnect via `/mcp`.
