---
name: "factory-retro"
description: "Research-run retrospective — extracts research lessons + factory-plane enhancements/ADRs from a completed run. The factory variant of uni-retro (which is SDLC). Triggered by a research cycle closing, not a PR merge. Plane-aware; no pattern/procedure."
---

# factory-retro — Research Run Retrospective

Extracts reusable knowledge from a completed research run into Unimatrix. The **factory variant of
`uni-retro`** (which is SDLC-shaped — PR-merge trigger, ARCHITECTURE/gate-3x artifacts, pattern/
procedure, `uni-architect`, cargo/worktree cleanup — none of which apply here).

> **Trigger:** a research cycle closes (`context_cycle stop`), not a PR merge.
>
> **Two halves:** (1) **knowledge extraction** works today; (2) **process telemetry** is degraded
> until the upstream Unimatrix observation-attribution bug is fixed (see factory enhancement #24 /
> the "No observation data" symptom). **Always run (1); attempt (2) and degrade gracefully.**

## Inputs

- `run-id` — the `context_cycle` topic (e.g. `shd-002`)
- the scope's GitHub Issue
- `wf:<version>` the run was stamped with

## Plane discipline (load-bearing — §9)

- **Research-process lessons** → research-plane `lesson-learned` (about the research process, not
  the subject: *"if the research target were different, would this still be useful?"* → yes ⇒ lesson).
- **Factory/process lessons, enhancement ideas, decision ADRs** → the **`factory` plane**
  (`category=factory`, `kind` mirrors the role), **`factory→factory` edges ONLY**. Cross-plane
  evidence is a `cites:` **field**, never an edge.
- **NO `pattern` / `procedure`** — `pattern` is disabled (D8); `procedure` is SDLC. Do not store them.

## Phase 1 — Gather

1. **Knowledge-yield (works now)** — query by the run-id tag (requires the run-id tagging convention):
   - `context_lookup(tags:["{run-id}"], category:"technology")` → status histogram → **proven/claimed ratio** (the firewall ratio: validating, or just collecting optimism?)
   - same for `finding` and `lesson-learned` → findings/run, dead-end rate.
2. **Process telemetry (degraded)** — `context_cycle_review(feature_cycle:"{run-id}", auto_close:true, format:"json")`. If it returns **"No observation data"**, note the upstream block and proceed on (1) + qualitative — do NOT fabricate telemetry.
3. **Qualitative (3 questions):** what worked · what wasted budget / chased a dead end · what surprised.

## Phase 2 — Extract (role: factory-retro/curator; SELECTIVE — more entries is not better)

1. **Research lesson-learned** — process lessons about the *research* (e.g. "harness research needs a live smoke"). Store research-plane.
2. **Factory enhancements** — friction, role gaps, operational hazards → `factory` `kind:technology`, `status:claimed` (the testing backlog). Each `Prerequisite→` the **factory capability** it improves.
3. **Decision ADRs** — decisions this run *validated* → graduate to `factory` `kind:finding` tagged `position`; `cites:` the run + `product/factory/decisions.md`.
4. **Factory board status** — did the run move any factory capability? **Manual** demonstration → `partial`; **autonomous** (an agent did it, with a run artifact) → `proven`. `context_correct` the capability node. (Never `proven` on a manual run — see Phase 3.)
5. **Operational learnings** — append new `OBS-*` to `product/factory/observations.md`.

## Phase 3 — The firewall, on ourselves

- Enhancement ideas stay `claimed` until **comparative A/B telemetry** proves them (§8) — not assertion.
- A factory capability reaches `proven` ONLY on an **autonomous-run artifact**; a human-inline run is `partial`. Do not let "it worked when I did it by hand" advance autonomy status.

## Phase 4 — Artifacts & version

- Research narrative / `REPORT.md` → committed via **factory-git research stream**.
- Any method change the retro implies (runbook/skill/rule edits) → **method stream**, bump `wf:`.
- The capability board is a **graph query, not a file** (§6) — do not write it to disk.

## Edges (HIGH bar, default few; factory→factory only)

Assert only when a future agent must traverse the link: enhancement `Prerequisite→` capability;
position-finding `cites:` (field) the run. Do not aim for coverage.
