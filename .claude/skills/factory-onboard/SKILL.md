---
name: "factory-onboard"
description: "Catch a fresh-context agent up to the research factory's CURRENT status — read the canonical sources, query the live Unimatrix graph + git, then report where things stand. Status is DERIVED from the graph, never a stored snapshot. Use when a new session/agent needs to orient from scratch."
---

# factory-onboard — Fresh-Context Catch-Up

Bring an agent that has **no prior context** current on the autonomous research factory (built on
Unimatrix; Claude is the platform). The whole point is to orient from **self-updating canonical
sources + live queries** — never a hand-maintained status file, which would drift the moment a run
lands (methodology §6: "what's done is a graph query, not a maintained list").

## 1. Orient — read in order
1. `CLAUDE.md` — mission, how-to-work, the firewall.
2. `docs/research-factory-methodology.md` — the method (esp. §3 firewall · §6 board-as-graph-query · §14 operational model · §15 reconciliation changelog).
3. `product/factory/decisions.md` — locked decisions **D1–D12** (the operating standards).
4. `product/factory/observations.md` — **OBS-*** (learnings surfaced by runs → wave-1 needs).
5. Method artifacts: `product/factory/runbook.md` · `.claude/workflow/{decompose-scope,research-scope}.md` · `.claude/agents/factory/*.md` · `.claude/rules/unimatrix-access.md` · `.claude/skills/factory-{git,retro}/SKILL.md`.

## 2. Determine current status — RUN these (status is derived; trust no snapshot)
- **Method version:** `git tag -l 'wf-*' | sort -V | tail -1` + `git log --oneline -15`.
- **Board = ONE call per goal.** Resolve the goal id (`context_search`), then:
  `context_graph(mode:"subgraph", seed_ids:[<goal-id>], max_depth:1, edge_types:["Advances"], direction:"incoming", detail:"full")`
  → returns the capability nodes **hydrated** (content + tags) in a single call — no separate status
  fetch, no client-side join. Read each capability's **firewall grade from its `grade:` tag**
  (🟢proven / 🟡partial / 🔴missing / ⚪claimed); for nodes predating the grade-tag convention (no
  `grade:` tag), parse the `status:` line in `content`. **Do NOT read the node's `status` field for
  the firewall grade** — that field is the lifecycle (`active`/`deprecated`), a different axis.
  - **Research board:** `<shd-goal>` (`context_search "shd self-hosted goal"`).
  - **Factory board** ("am I autonomous yet"): `<factory-goal, id 19>` — same call → factory
    capabilities + grades; enhancements are `kind:technology` still at `grade:claimed` = the backlog.
  - **+ technology landscape (optional, one call):** bump to `max_depth:2, edge_types:["Advances","Prerequisite"]`
    to pull goal ← capabilities ← technologies together (depth>1 reads the tick-cache, ~30-60s lag —
    fine for orientation).
- **Issues:** `gh issue list --repo dug-21/arch-research --label factory`.
- **Telemetry:** `context_cycle_review(feature_cycle:"<latest run-id>")`.
- Resolution per `.claude/rules/unimatrix-access.md` — `subgraph`/`neighbors` at depth 1 are live
  (reflect committed writes immediately); pass `agent_id`. Note: `neighbors` returns **edges only**
  (even with `detail:"full"`) — use `subgraph` when you want the nodes. If a `context_*` call is
  rejected, the MCP connection is stale → `/mcp` reconnect.

## 3. Interpret with the firewall (§3)
`proven` ONLY on a real, demonstrated-by-us artifact. `partial` = manually demonstrated, not yet
autonomous. Nothing advances on assertion. `wf:` = the method's semver — the A/B baseline for the
reflexive loop (FC-Improve).

## 4. Report
A concise status: method `wf:` version · research-board state for `shd` (what's proven/partial/
missing) · factory-board autonomy state · open blockers · recommended next action.

**Flag anything where the canonical sources were insufficient to orient** — those are
factory-process gaps and become `factory-retro` lessons. Every onboarding doubles as a
self-sufficiency test of the method.
