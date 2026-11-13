# mnstd-001: Board ledger (Unimatrix ids)

**Run:** `mnstd-001` (decompose-scope, phase `decompose`) · **Writer:** `factory-curator` · **Source:** `DECOMPOSITION.md`
**Prior-art check:** goal + semantic search found no Metanorma/standards-authoring nodes; no duplicates. No technology nodes created (deferred to mnstd-002 per DECOMPOSITION §5).

## Conventions used (matched to opcost #113 and shd #242 boards)
- NFRs are `category: capability` with `kind: nfr` in content and tag `nfr`; business caps tag `business`.
- Tags per node: `business|nfr`, `grade:missing`, `mnstd`, `mnstd-001`. Goal tags: `goal`, `mnstd`, `mnstd-001`.
- Topic `mnstd`; feature_cycle `mnstd-001`. Grade lives only in the tag, set at store time (0 `context_tag` calls).
- `goal:mnstd` and `kind:` prefixed tags from DECOMPOSITION §5 were **not** used, because no prior board uses them.

## Id map

| Decomp id | Unimatrix id | Kind | Grade |
|---|---|---|---|
| goal `mnstd` | **#329** | goal | n/a |
| C1 | #336 | business | missing |
| C2 | #335 | business | missing |
| C3 | #334 | business | missing |
| C4 | #332 | business | missing |
| C5 | #333 | business | missing |
| C6 | #331 | business | missing |
| C7 | #330 | business | missing |
| N1 | #337 | nfr | missing |
| N2 | #338 | nfr | missing |
| N3 | #339 | nfr | missing |
| N4 | #340 | nfr | missing |
| N5 | #341 | nfr | missing |
| N6 | #342 | nfr | missing |
| N7 | #343 | nfr | missing |
| N8 | #344 | nfr | missing |

## Edges written (all at store time, verified by subgraph query)

| Type | Expected | Written | Failed |
|---|---|---|---|
| `Advances` → #329 | 15 | 15 | 0 |
| `Prerequisite` (cap→cap) | 6 | 6 | 0 |
| `About` (nfr→cap) | 32 | 32 | 0 |

- Prerequisite: C1→C2 (336→335), C2→C3 (335→334), C3→C4 (334→332), C3→C5 (334→333), C3→C6 (334→331), C5→C7 (333→330).
- About: N1→C1..C7 (7), N2→C1..C7 (7), N3→C1,C5,C6,C7 (4), N4→C3,C4,C7 (3), N5→C3,C4,C5,C7 (4), N6→C4,C7 (2), N7→C1,C5,C6,C7 (4), N8→C1 (1).
- N6 is attached only to C4 and C7, as listed. The optional 5 extra edges to all seven were not written; the content of #342 says so.

Verification: `context_graph(mode:"subgraph", seed_ids:[329], max_depth:1, edge_types:["Advances"], direction:"incoming")` returned 16 nodes (goal + 15) and 15 edges. A second subgraph query seeded on C1..C7 with About+Prerequisite returned 38 edges (32 + 6).
