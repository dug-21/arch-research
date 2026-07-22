# Protocol: theme-scan

The **recurring, technology-push** intake at the **wide mouth of the garage funnel** (`CLAUDE.md` Mission):
scan a **theme** for candidate technologies, fan each out into hypotheses (wide mouth), triage hard at the
**neck**, and hand a shortlist to the owner. Inverts research-scope
(which is capability-pull). Produces **structure only** — candidate technologies (`claimed`) and
hypotheses (`finding`+`hypothesis`); **nothing reaches `proven` here.** A promoted hypothesis becomes a
*separate* bounded proof-goal (a normal validated research-scope) where the firewall bites. Run by
`research-leader`. Its own cycle (`topic`) + GitHub Issue. Phases: **scan → hypothesize → triage → formalize.**
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
     next_phase=`scan`, **`tags:["{wf}"]`** (the derived `wf:` — `git describe --tags --match 'wf-*'`),
     agent_id=`{scan-id}-leader`. `tags` is **set-once at start** (no append, no retro-fix — get it right
     on the first call). The cycle is what makes the run **attributable and its transcript retained**
     (retention now works on stamped cycles — OBS-10); an unstamped run has no linked buffer at all.
     `phase-end` at **every** phase boundary; `stop` at CLOSE.
  3. **Git** — research-stream commits under `product/research/{scan-id}/` (the `wf:` version rides the
     cycle tag above; do not hand-type it).
- **GATE (advisory → owner):** confirm **theme + candidate source** (owner-injection vs external-scan)
  **+ budget envelope**. Wave-0 the owner's kick IS this approval; surface it, don't block on it.

## Phase: scan
- Leader spawns `scout` (parallel ×N if the source-mix partitions) → candidate technologies. Owner-
  injection enters here as a hand-fed candidate.
- `scout` applies the **lens include-test**, **dedups reuse-first** against Unimatrix (prior runs' filed
  nodes — incl. fold-findings' named tails) and characterizes each survivor (mechanism · **resource
  envelope** · demonstrated-vs-claimed · `cites` · source-signal). Read-only; returns markdown inline
  (OBS-7) → **leader persists** `product/research/{scan-id}/scout-candidates.md`.
- **NO graph writes in this phase** (lesson #172, wfh-001): the divergent output stays in git markdown
  until triage has compressed it — the neck's verdict shapes what the curator writes (see formalize).
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
- **NO graph writes in this phase** — hypotheses reach the graph only through formalize, post-triage.
- `phase-end phase:"hypothesize" outcome:"H hypotheses (obvious/adjacent/non-obvious split)"`.

## Phase: triage
- `goal-owner` runs the **convergent gate** (§6): scores mechanism-fit · theme-alignment · novelty ·
  effort-vs-payoff; **park by default**; routes **PARK / DIRECTIONAL-PROBE / VALIDATED-BUILD** (with a
  proposed `done_when` for builds). Advisory; writes `product/research/{scan-id}/reports/triage.md`.
- **GATE (blocking → owner):** the owner reviews the shortlist and **promotes 0..n** hypotheses to
  bounded proof-goals. Promoting nothing is a valid, common outcome.
- `phase-end phase:"triage" outcome:"P promoted, D probe, rest parked"`.

## Phase: formalize (post-gate — ALL graph writes live here)

The run's only curator phase. **The graph stores verdicts and re-entry conditions, never the spray**
(lesson #172; the divergent archive is git markdown). The persistence test for every item: *would a
future agent need to FIND this via `context_search` — to avoid re-spending, or to re-enter when a
condition flips?* If yes → the **cheapest searchable representation** below; if no → git only.

`factory-curator` **self-briefs first** (`context_search` — REUSE; extend existing nodes via
`context_correct`, never duplicate), then files in three tiers:

1. **Survivors** (promoted / probe, plus in-lens candidates worth individual reuse) → full `technology`
   nodes (`grade:claimed`, tagged `theme:<slug>` + `{scan-id}`, `cites`) and `finding`+`hypothesis`
   nodes with `Motivates→` their technology; the conjectured `technology Prerequisite→ capability` edge
   is authored for **survivors only** — speculative edges stay off the graph.
2. **Parked-with-a-reason** → a `finding` (`hypothesis`+`parked`) whose content IS the park reason with
   an explicit **re-enter-when** condition. These must be **few and load-bearing** — if triage parks
   many, compress further (fold) before filing; a large parked tier is spray with extra steps.
3. **Folded tail** (thrown out at triage) → NOT individual nodes. One or two **fold-findings that NAME
   every folded candidate** (this is what keeps future scan dedup working graph-side) + the git
   markdown as archive.

- Synthesis verdict (e.g. white-space) → a `position`-tagged `finding`.
- `phase-end phase:"formalize" outcome:"N nodes (S survivors, P parked, F folded-into-K findings)"` → `stop`.

## CLOSE
- `context_cycle stop`. Record the **funnel counts** (scanned → generated → survived → promoted, by
  novelty class), tagged `{scan-id}` + `theme:<slug>` — the reflexive-loop telemetry (§9, #66).
- Git: research-stream PR `Closes #<issue>` — merge after formalize (auto-merge if enabled at repo
  level; else the leader rebase-merges — the blocking gate already passed). Trigger `factory-retro`.
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
