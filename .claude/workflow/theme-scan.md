# Protocol: theme-scan

The **recurring, technology-push** intake at the **wide mouth of the garage funnel** (`CLAUDE.md` Mission):
scan a **theme** for candidate technologies, fan each out into hypotheses (wide mouth), triage hard at the
**neck**, and hand a shortlist to the owner. Inverts research-scope
(which is capability-pull). Produces **structure only** — candidate technologies (`claimed`) and
hypotheses (`finding`+`hypothesis`); **nothing reaches `proven` here.** A promoted hypothesis becomes a
*separate* bounded proof-goal (a normal validated research-scope) where the firewall bites. Run by
`research-leader`. Its own cycle (`topic`) + GitHub Issue. Phases: **scan → hypothesize → triage.**
Design: `product/factory/proposals/theme-driven-scanning-methodology.md` (§5 flow · §6 triage · §9 funnel).

## Roles
`research-leader` (orchestrate, persist, budget) · `scout` (×1+, discovery) · `hypothesizer` (Fable 5,
divergent fan-out) · `factory-curator` (single writer) · `goal-owner` (convergent triage). No POC/
validator — this protocol never proves.

## INIT
- Read `product/factory/themes.md` for the **active theme** — lens · value-targets · source-mix ·
  cadence · **budget envelope** (§8). Resolve `scan-id` = `{theme-slug}-NNN` (e.g. `smart-edge-001`).
- **Open all three surfaces (D1) — MANDATORY, before any specialist spawns. A run that skips these is
  invisible on two of three surfaces (OBS-10, learned the hard way on smart-edge — no Issue, no cycle
  stamp for the whole line):**
  1. **GitHub Issue** — `gh issue create --repo dug-21/arch-research --label factory,scope:research,confidence:directional`,
     title `{scan-id} — theme-scan: <theme> …`, body = scan intent + out-of-scope. Cross-linked by
     **title, not # equality** (D4). This is the live human↔garage surface; it is not optional.
  2. **Cycle** — `context_cycle start` topic=`{scan-id}`, goal=`scan <theme> for candidate technologies`,
     next_phase=`scan`, agent_id=`{scan-id}-leader`. The stamp is what makes the run **attributable and
     its transcript retained** (retention now works on stamped cycles — OBS-10); an unstamped run has no
     linked buffer at all. `phase-end` at **every** phase boundary; `stop` at CLOSE.
  3. **Git** — stamp `wf:` (derive it, never hand-type: `git describe --tags --match 'wf-*'`); research-stream commits under `product/research/{scan-id}/`.
- **GATE (advisory → owner):** confirm **theme + candidate source** (owner-injection vs external-scan)
  **+ budget envelope**. Wave-0 the owner's kick IS this approval; surface it, don't block on it.

## Phase: scan
- Leader spawns `scout` (parallel ×N if the source-mix partitions) → candidate technologies. Owner-
  injection enters here as a hand-fed candidate.
- `scout` applies the **lens include-test**, **dedups reuse-first** against Unimatrix, and characterizes
  each survivor (mechanism · **resource envelope** · demonstrated-vs-claimed · `cites` · source-signal).
  Read-only; returns markdown inline (OBS-7) → **leader persists** `product/research/{scan-id}/scout-candidates.md`.
- `factory-curator` **self-briefs first** (`context_search category:"technology"` — REUSE), then files
  each **new, in-lens** candidate → `technology` (`grade:claimed`), tagged `theme:<slug>` + `{scan-id}`,
  `cites`. Known/out-of-lens candidates are NOT re-filed (note the existing node id).
- `phase-end phase:"scan" outcome:"C candidates (N new, K known/parked)"`.

## Phase: hypothesize
- Leader hands the scout writeup **+ the current capability-surface inventory** (for Unimatrix: the live
  `context_*` tool set + repo — the real surface, not an imagined one) to `hypothesizer` (one per
  candidate, spawned in one message).
- `hypothesizer` (Fable 5, loose reins) generates for **range** — mechanism-grounded `T→C of U`
  hypotheses incl. non-obvious/whitespace. Grades nothing; decides nothing. Returns markdown inline →
  **leader persists** `product/research/{scan-id}/hypotheses.md`.
- **Coverage (advisory, non-blocking):** if a candidate's fan-out is thin or its scout writeup too thin
  to reason from, leader re-spawns for more range (≤2) or flags the candidate as under-characterized.
- `factory-curator` files each hypothesis → `finding` tagged `hypothesis` + `theme:<slug>` + `{scan-id}`,
  with `Motivates→` its technology. **The conjectured `technology Prerequisite→ capability` edge is NOT
  authored yet** — only survivors get it (triage), to keep speculative edges off the graph; parked
  hypotheses carry the target in `content`.
- `phase-end phase:"hypothesize" outcome:"H hypotheses (obvious/adjacent/non-obvious split)"`.

## Phase: triage
- `goal-owner` runs the **convergent gate** (§6): scores mechanism-fit · theme-alignment · novelty ·
  effort-vs-payoff; **park by default**; routes **PARK / DIRECTIONAL-PROBE / VALIDATED-BUILD** (with a
  proposed `done_when` for builds). Advisory; writes `product/research/{scan-id}/reports/triage.md`.
- For **survivors only**, `factory-curator` authors the conjectured `technology Prerequisite→ capability`
  edge. Parked hypotheses stay `claimed` findings, re-enterable — no further spend.
- **GATE (blocking → owner):** the owner reviews the shortlist and **promotes 0..n** hypotheses to
  bounded proof-goals. Promoting nothing is a valid, common outcome.
- `phase-end phase:"triage" outcome:"P promoted, D probe, rest parked"` → `stop`.

## CLOSE
- `context_cycle stop`. Record the **funnel counts** (scanned → generated → survived → promoted, by
  novelty class), tagged `{scan-id}` + `theme:<slug>` — the reflexive-loop telemetry (§9, #66).
- Git: research-stream PR `Closes #<issue>` (auto-merge after the triage gate). Trigger `factory-retro`.
- **Promotion (frontier-change, D3):** each promoted hypothesis → a new **validated research-scope**
  Issue (a bounded proof-goal, real `done_when`), linked to this scan. That run — not this one — does the
  POC and the firewall, and on `proven` files the **Unimatrix issue** handoff (§7). The scan hands off;
  it does not prove and does not ship.

## Cadence
Recurring per the theme's cadence. **Wave-0 = manual owner kick.** Autonomous scheduled scanning is a
later wave, **gated on the budget-metering capability** (§8) — do not assume it here.

## Output
A triaged **shortlist** to the owner + a graph enriched with `claimed` candidate technologies and
`hypothesis` findings (all `theme:<slug>`-tagged), and the funnel baseline the reflexive loop tunes
against. **Zero status moved to `proven`** — by design.
