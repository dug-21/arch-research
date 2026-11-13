# mnstd-002 — feasibility grade ledger

- **Writer:** factory-curator (`agent_id: factory-curator` on every write). **Date:** 2026-11-13.
- **Governing inputs:** owner firewall rulings (verbatim, `SCOPE.md`, last Extension; recorded on Issue #74 before
  any grade moved) · `reports/gate-feasibility.md` (clause mapping §5, recommended grades §6) ·
  `reports/gate-feasibility-rework1.md` (C5.3 checker PASS) · `artifacts/ENVELOPE.md`, `artifacts/RESULT.md`.
- **Owner rulings applied:** 1 fonts-as-environment (N1.1/N6.1; fonts pinned by `poc/fonts/MANIFEST.json`,
  922d004) · 2 C1.3 presentation-XML numbering · 3 C6.1 HTML glue is not native → C6 `partial`.
- **Conflict check:** every directed grade matches the validator's §6 table under rulings 1+2 with ruling 3 NO
  (column B for all nodes, plus C1 cleared by ruling 2; C6 stays partial on C6.1-HTML). **No conflict; nothing withheld.**
- **Proof commits on main** (PR #75 rebase-merged; `git diff` of poc/, task/, artifacts/ between each pre-rebase SHA and its
  rebased SHA is empty): c99d0bd (was 7953833) · 323a13f gated (was 17a7fa4) · 4ac942e · 922d004 · bbce28b ·
  417b83a (was 1bc97ca).

## Grade moves

| Node | Old id | New id | Grade | Write type |
|---|---|---|---|---|
| C1 | 336 | 365 | missing → **proven** | `context_correct` (proven_by + `grade:proven`, one step) |
| C2 | 335 | 366 | missing → **proven** | `context_correct` (same) |
| C3 | 334 | 367 | missing → **proven** | `context_correct` (same) |
| C4 | 332 | 368 | missing → **proven** | `context_correct` (same) |
| C5 | 333 | 369 | missing → **proven** | `context_correct` (same) |
| C6 | 331 | 371 | missing → **partial** | `context_correct` (evidence + ruling 3, grade unchanged) then `context_tag replace grade:partial` |
| C7 | 330 | 370 | missing → **proven** | `context_correct` (same as C1) |
| N1 | 337 | 372 | missing → **proven** | `context_correct` |
| N2 | 338 | 364 | missing → **proven** | `context_correct` |
| N3 | 339 | 373 | missing → **proven** | `context_correct` |
| N4 | 340 | 374 | missing → **proven** | `context_correct` |
| N5 | 341 | 375 | missing → **proven** | `context_correct` |
| N6 | 342 | 376 | missing → **proven** | `context_correct` |
| N7 | 343 | 377 | missing → **proven** | `context_correct` |
| N8 | 344 | 378 | missing → **proven** | `context_correct` |
| tech image + metanorma-iso | 349 | 379 | claimed → **proven** | `context_correct` |
| tech locator resolver | 350 | 380 | claimed → **proven** | `context_correct` |
| tech native annotations → PDF | 351 | 383 | claimed → **partial** | `context_correct` (evidence + ruling 3) then `context_tag replace grade:partial` |
| tech local git review | 352 | 381 | claimed → **proven** | `context_correct` (also records the refined C4.3 verdict rule) |
| tech ISO 2012-03 schema + glue | 353 | 382 | claimed → **proven** | `context_correct` |
| tech commenter 0.7.0 | 354 | 354 | claimed (unchanged) | none |

Each corrected node gained the `mnstd-002` run tag. Tag writes this session: **2** (well under ~60/h).

## Finding

No new finding stored. #358 (ISO HTML renders no native reviewer notes, metanorma-iso 3.5.14) and #359 (ISO PDF
renders them as native sticky notes) already state it. The owner's ruling that the HTML glue does not count is
recorded on C6 #371 and tech #383, not in a duplicate finding.

## Verification

- Board query `context_graph(subgraph, seed 329, Advances, incoming, full)`: all 15 board nodes come back at their new ids
  with the expected grades (14 `grade:proven`, C6 `grade:partial`). Goal #329 was not touched.
- All 74 authored edges (Advances / About / Prerequisite / Motivates) checked before and after, with old ids mapped to new.
  Every one is present between active nodes. 0 missing.
- **Observed, not a failure:**
  - (a) The board query lists each Advances edge **twice**. With supersession resolution on, the deprecated source's
    stored edge resolves to the same new id. Consumers should dedup on (source, type, target).
  - (b) System-inferred `Informs` edges among techs #349–#353 were not carried to the new ids. They remain only on
    the deprecated versions. They are not one of the six authored edge types.
  - (c) The correct calls reported "N skipped — invalid source". These were edges from already-deprecated sources.
    Their active successors' edges were present (verified above).
- **Failures:** none.
