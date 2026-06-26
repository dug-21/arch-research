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
- **Research board** (the `shd` goal — `context_search "shd self-hosted goal"` to resolve its id):
  `context_graph(mode:"neighbors", id:<shd-goal>, direction:"incoming", edge_types:["Advances"])`
  → each capability's status (🟢proven / 🟡partial / 🔴missing / ⚪claimed); then the `technology`
  nodes (`Prerequisite→` each capability) and their status.
- **Factory board** (the `factory` goal — the "am I autonomous yet" plane): the same frontier query
  → the factory capabilities + status; the factory enhancements (`kind:technology`, `claimed` = the backlog).
- **Issues:** `gh issue list --repo dug-21/arch-research --label factory`.
- **Telemetry:** `context_cycle_review(feature_cycle:"<latest run topic>")`.
- Resolution per `.claude/rules/unimatrix-access.md` — default `context_graph(mode:"current")`; pass `agent_id`; if a `context_*` call is rejected, the MCP connection is stale → `/mcp` reconnect (unimatrix#830).

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
