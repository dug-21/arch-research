---
name: "factory-onboard"
description: "Catch a fresh-context agent up to the research & development garage's CURRENT status — read the canonical sources, query the live Unimatrix graph + git, then report where things stand. PLAN-ONLY: orients and recommends a next action; does NOT execute research runs (execution is a separate protocol session). Status is DERIVED from the graph, never a stored snapshot. Use when a new session/agent needs to orient from scratch."
---

# factory-onboard — Fresh-Context Catch-Up

Bring an agent that has **no prior context** current on the autonomous research & development **garage**
(built on Unimatrix; Claude is the platform; the **factory** is its firewall-gated proving-grounds stage —
see `CLAUDE.md` Mission). The whole point is to orient from **self-updating canonical
sources + live queries** — never a hand-maintained status file, which would drift the moment a run
lands (methodology §6: "what's done is a graph query, not a maintained list").

## 0. Role boundary — plan, don't execute (load-bearing)

`factory-onboard` is a **planning / ownership** context — the factory analog of the SDLC **product-owner**
pair, and of `uni-zero` ("does not run delivery protocols"). Its deliverable is **orientation + a
recommendation**; it does **not** execute research.

- **MAY:** read canonical sources, run the status queries (§2), plan/scope hypotheses, triage, and
  **recommend** a next action.
- **MUST NOT** (this session): launch a run — no spawning specialists (scout / researcher / hypothesizer /
  curator), no `context_cycle start`, no opening a run Issue, no graph writes.

Executing a run is a **separate, deliberate session** invoking the research / theme-scan protocol
(`.claude/workflow/{theme-scan,research-scope,decompose-scope}.md`), spun up per-hypothesis on the human's
go, with **scope-approval as its explicit first gate**. This keeps the human gate meaningful and stops an
orienting agent from sliding from "recommended next action" straight into running it (**OBS-13**). Wave-0
hygiene enforced by instruction; the durable fix is a harness that enforces the boundary structurally, not
the agent's compliance.

## 1. Orient — read in order
1. `CLAUDE.md` — mission, how-to-work, the firewall.
2. `docs/research-factory-methodology.md` — the method (esp. §3 firewall · §6 board-as-graph-query · §14 operational model · §15 reconciliation changelog).
3. `product/factory/decisions.md` — locked decisions **D1–D12** (the operating standards).
4. `product/factory/observations.md` — **OBS-*** (learnings surfaced by runs → wave-1 needs).
5. Method artifacts: `product/factory/runbook.md` · `.claude/workflow/{decompose-scope,research-scope}.md` · `.claude/agents/factory/*.md` · `.claude/rules/unimatrix-access.md` · `.claude/skills/factory-{git,retro}/SKILL.md`.

## 2. Determine current status — RUN these (status is derived; trust no snapshot)
- **Method version:** `git describe --tags --match 'wf-*'` (the derived live stamp — clean `wf-vX.Y` on a tagged commit, or `wf-vX.Y-N-gSHA` when method HEAD is N commits past the last tag) + `git log --oneline -15`.
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

**Then STOP — do not execute the recommended action in this session (§0).** The recommendation is the
handoff; execution is a separate, human-gated protocol session.

**Flag anything where the canonical sources were insufficient to orient** — those are
factory-process gaps and become `factory-retro` lessons. Every onboarding doubles as a
self-sufficiency test of the method.
