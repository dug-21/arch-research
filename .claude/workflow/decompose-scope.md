# Protocol: decompose-scope

Produces a goal's **capability board** — the demand map the **proving grounds** (the factory stage of the
garage funnel) researches against. Run by `research-leader`. One decompose-scope per goal; its own cycle
(`topic`) and GitHub Issue. Phases: **scope → decompose**. (Methodology §7, §14.2; runbook.)

## Roles
`research-leader` (coordinator) · `factory-researcher` (read-only) · `factory-curator` (single writer).
Every Unimatrix mutation carries the acting role's defined identity: `research-leader` for cycle events,
`factory-curator` for content/edge/tag/lifecycle writes.

## INIT
`context_cycle start` topic=`{goal}-NNN`, goal=`<specific goal sentence (§7)>`, next_phase=`scope`,
**`tags:["{wf}"]`** (the derived `wf:` — `git describe --tags --match 'wf-*'`; **set-once at start**, no
append/retro-fix, so get it right on the first call), agent_id=`research-leader`. Create the GitHub Issue
(body = the SCOPE).

## Phase: scope
- `factory-researcher` drafts `SCOPE.md` — goal, success criteria, decomposition questions,
  out-of-scope boundary, and a prior-art search (`context_search(category:"technology")` for reuse).
- **GATE (advisory → human):** human approves the goal/scope framing.
- `phase-end phase:"scope" next_phase:"decompose"`.

## Phase: decompose
- `factory-researcher` → `DECOMPOSITION.md` (exact name) (candidate business capabilities + nfrs + dependencies).
- **Board tag convention** (researcher and curator): Tags: `business|nfr`, `grade:<g>`, `{goal}`, `{run-id}`;
  goal node tags `goal`, `{goal}`, `{run-id}`. NFRs are `category: capability`, `kind: nfr` in content. No
  `goal:`/`kind:` prefixed tags.
- `factory-curator` distills → Unimatrix:
  - a `goal` node; `capability` (business) + `nfr` nodes, all `missing`/`claimed`;
  - edges: `Advances→goal` (each cap/nfr), `About→` (nfr→cap), `Prerequisite→` (cap→cap);
  - **tag every node with the run-id**.
- **GATE (advisory → human):** approve the board. Per §6, the set is **never assumed complete** —
  gaps get added later as new `missing` nodes (frontier-change, D3).
  - If owner questions are answered by default (including pre-authorized gates), the gate comment lists each
    default that appears in a done_when clause and declares it **binding for the firewall**. Rewrite
    'proposed'/'default' wording in those clauses to the fixed value before close. *(mnstd-001 OBS-26.)*
  - **done_when altitude check (before approving the board).** For each clause ask: *"if the tool satisfies the
    need through a different layer, file or one-time setup step than this wording assumes, should the clause
    FAIL?"* If no, rewrite at the need (e.g. "machine-readable number joinable from the compile's XML outputs",
    not "in the semantic XML"; "no network during the gated run; one-time provisioning declared and pinned",
    not "only network access is the image pull"). Keep layer-specific wording only where the layer IS the
    requirement (e.g. "native, not a bespoke overlay"). (Lesson #390; mnstd-002 OBS-29.)
- `phase-end phase:"decompose" outcome:"N caps, M nfrs"`.

## CLOSE
`context_cycle stop`. The board is now the durable queue (the frontier); each capability spawns a
`research-scope`. Post the board summary to the Issue.

## Output
Goal + capability board in Unimatrix. The decompose-scope itself proves nothing — it is structure only.
