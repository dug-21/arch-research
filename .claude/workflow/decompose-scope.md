# Protocol: decompose-scope

Produces a goal's **capability board**. Run by `research-leader`. One decompose-scope per goal; its
own cycle (`topic`) and GitHub Issue. Phases: **scope → decompose**. (Methodology §7, §14.2; runbook.)

## Roles
`research-leader` (coordinator) · `factory-researcher` (read-only) · `factory-curator` (single writer).

## INIT
`context_cycle start` topic=`{goal}-NNN`, goal=`<specific goal sentence (§7)>`, next_phase=`scope`,
agent_id=`{scope-id}-leader`. Stamp `wf:` (the method's `wf-vX.Y` tag). Create the GitHub Issue
(body = the SCOPE).

## Phase: scope
- `factory-researcher` drafts `SCOPE.md` — goal, success criteria, decomposition questions,
  out-of-scope boundary, and a prior-art search (`context_search(category:"technology")` for reuse).
- **GATE (advisory → human):** human approves the goal/scope framing.
- `phase-end phase:"scope" next_phase:"decompose"`.

## Phase: decompose
- `factory-researcher` → a decomposition file (candidate business capabilities + nfrs + dependencies).
- `factory-curator` distills → Unimatrix:
  - a `goal` node; `capability` (business) + `nfr` nodes, all `missing`/`claimed`;
  - edges: `Advances→goal` (each cap/nfr), `About→` (nfr→cap), `Prerequisite→` (cap→cap);
  - **tag every node with the run-id**.
- **GATE (advisory → human):** approve the board. Per §6, the set is **never assumed complete** —
  gaps get added later as new `missing` nodes (frontier-change, D3).
- `phase-end phase:"decompose" outcome:"N caps, M nfrs"`.

## CLOSE
`context_cycle stop`. The board is now the durable queue (the frontier); each capability spawns a
`research-scope`. Post the board summary to the Issue.

## Output
Goal + capability board in Unimatrix. The decompose-scope itself proves nothing — it is structure only.
