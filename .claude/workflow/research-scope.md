# Protocol: research-scope

Researches ONE capability to a graded technology landscape (directional/empirical) or proves a
technology (validated). Run by `research-leader`. One research-scope per capability (1+ per capability
if needed); its own cycle (`topic`) and GitHub Issue. Phases: **scope → tech-discovery →
[feasibility] → synthesis**. (Methodology §14.2; runbook; scope template
`product/factory/templates/scope.md`.)

## Roles
`research-leader` · `factory-researcher` (×N, one per workstream) · `factory-curator` · `goal-owner`
(synthesis) · *validated only:* `factory-poc`, `factory-validator`.

## INIT
`context_cycle start` topic=`{goal}-NNN`, goal=`<capability-focused goal sentence>`,
next_phase=`scope`, agent_id=`{scope-id}-leader`. Stamp `wf:`. Create the Issue (body = SCOPE).

## Phase: scope
- `factory-researcher` drafts `SCOPE.md` from the template: **capability target** (Uni id),
  **confidence-required** (`directional|empirical|validated`), the question, prior-art (reuse),
  workstreams (each with an explicit `Output:`), proof bar, out-of-scope, coverage rule.
- **GATE (advisory → human):** approve scope — especially confidence-required + the boundary.
- `phase-end phase:"scope" next_phase:"tech-discovery"`.

## Phase: tech-discovery
- Leader spawns the `factory-researcher`s **in one message** (parallel), one per workstream → FINDINGS files.
- `factory-curator` **self-briefs first** (`context_search(category:"technology")` to **REUSE**), then
  distills → `technology` (`claimed`, `Prerequisite→` capability) + `finding` (`Motivates`, `cites`).
  Tag with the run-id.
- **GATE (blocking → coverage):** loop-until-dry K/N + **human confirm**. REWORK ≤2 → re-spawn researchers; else SCOPE-FAIL.
- `phase-end phase:"tech-discovery" outcome:"T claimed, R reused"`.

## Phase: feasibility  *(validated/empirical only — SKIPPED for directional)*
- `factory-poc` builds the artifact (the only compute-spending phase); `factory-validator` verifies it is real.
- `factory-curator` `context_correct` technology → `proven`/`partial`, set `proven_by` (the envelope).
- **GATE (blocking → FIREWALL, MANDATORY):** no `proven` without a verified, demonstrated-by-us artifact. REWORK ≤2 → SCOPE-FAIL.
- `phase-end phase:"feasibility" outcome:"X proven, Y partial"`.

## Phase: synthesis
- `factory-curator` writes the `position` finding + `REPORT.md`; marks capabilities `proven` where `done_when` clears.
- `goal-owner` runs the relevance/target review (advisory) → `reports/relevance.md`.
- **GATE (advisory → human):** synthesis review, including the goal-owner verdict. Directional output = ranked landscape + recommendation + a staged validated follow-on scope.
- `phase-end phase:"synthesis"` → `stop`.

## CLOSE
`context_cycle stop`. Git: research-stream PR `Closes #<issue>` (auto-merge after the synthesis gate).
Trigger `factory-retro`. **Frontier change (D3):** a discovered gap → curator updates the node + a
dated Extension (in-envelope), or a new `capability` node + a new research-scope Issue (surface-expanding).

## Output
- **Directional:** graded technologies (`claimed`) + a `position` recommendation + a staged validated follow-on.
- **Validated:** ≥1 technology `proven` with an attached artifact; the capability advanced.
