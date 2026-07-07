# Factory Run Runbook (manual / inline-roles)

How to run one research goal through the pipeline **by hand**. The operator plays the roles
(leader / researcher / curator / poc / validator) inline; the human approves at **3 gates**.
Automation (agent defs, auto-spawn, the full protocol) is deferred until a manual run validates
these steps (Tier 1).

**Surfaces (D1):**
- **Unimatrix** — settled knowledge (the capability board, technologies, findings).
- **git** (this repo, `product/research/{scope-id}/`) — `SCOPE.md`, `FINDINGS*.md`, `REPORT.md`, artifacts.
- **GitHub Issue** — live status + the 3 human gates. One Issue per scope.

## Scope unit (D2)

One **decompose-scope** per goal (produces the capability board) → one **research-scope** per
capability (researches/proves its technologies). Each scope = one Issue = one `context_cycle` topic
(`{goal-tag}-NNN`).

## A run, phase by phase

The leader issues **every** `context_cycle` call. Access rules: `.claude/rules/unimatrix-access.md`.

0. **INIT** — `context_cycle(type:"start", topic, goal:"<specific sentence>", next_phase:"scope")`.
   The goal sentence is load-bearing (drives briefing + plane selection).
1. **scope** — author `SCOPE.md` from `templates/scope.md`; post a summary to the Issue.
   **GATE: human approves scope.** → `phase-end phase:"scope"`.
2. **decompose** *(decompose-scope only)* — curator writes goal + `capability` + `nfr` nodes
   (`missing`/`claimed`) with `Advances`/`About` edges, via `uni-capability`. → `phase-end phase:"decompose"`.
3. **tech-discovery** — researcher (read-only) → `FINDINGS` file; curator **searches the `technology`
   library FIRST** (reuse → new `Prerequisite` edge), then stores `technology` (`claimed`) + `finding`
   (`Motivates`, `cites`). **GATE: coverage** (loop-until-dry K/N + human confirm).
   → `phase-end phase:"tech-discovery"`.
4. **feasibility** *(empirical/validated scopes only)* — build the POC artifact; validate it's real;
   curator `context_correct` → `proven`/`partial` with the envelope in `proven_by`.
   **GATE: firewall.** → `phase-end phase:"feasibility"`.
5. **synthesis** — curator writes `position` finding(s) + `REPORT.md`; marks capabilities `proven`
   where `done_when` clears. **GATE: human review.** → `phase-end phase:"synthesis"` → `stop`.

**Directional scopes** stop after synthesis with **structure only** (skip feasibility) — D7.

## Gates (3 human touchpoints)

scope approval · coverage confirm · synthesis review. Between them the run is autonomous within budget.

## Frontier change (D3)

A mid-run gap →
- **in-envelope:** curator updates the node + appends a dated **Extension** to the scope; continue.
- **surface-expanding:** new `capability` node + a **new research-scope Issue**; it re-enters the frontier.
- **redefinition reopening `proven`:** revert status toward `partial`; log, don't hide.

## GitHub Issue conventions

- **One Issue per scope.** Body = the `SCOPE` (from template). Comments = phase-end updates + gate
  requests/approvals + the final `REPORT` link.
- Title: `{scope-id} — {subject}`. Suggested labels: `factory`, `scope:decompose|research`,
  `confidence:directional|empirical|validated`, and a status label tracking the phase.
- **Human inputs** (approvals, redirections) originate in the Issue; the curator **distills them back**
  to git/Unimatrix before they count (D1). A comment moves *structure*, never *status*.

## Telemetry (close every run)

`context_cycle_review(feature_cycle:"{scope-id}", auto_close:true, format:"json")` → yield (§10).
Stamp the run with the workflow version `wf:<semver>` (§8) — the method's `wf-vX.Y` tag (factory-git).

**Run-id tagging convention:** the curator **tags every stored entry with the run-id** (e.g.
`shd-002`) so per-run knowledge-yield is queryable by tag — `context_lookup`'s `feature_cycle` is
NOT a filter. (Observation-stream telemetry is upstream-blocked; see factory enhancement #24.)

**Firewall-grade tagging convention (the board index):** the curator tags every
`capability`/`technology` with a **`grade:<missing|claimed|partial|proven>`** tag mirroring its
firewall grade. This makes the board (§6) a **one-call query** —
`context_graph(mode:"subgraph", seed_ids:[<goal>], max_depth:1, edge_types:["Advances"], direction:"incoming", detail:"full")`
returns every capability hydrated and its grade is read straight from the tag, no content parse and no
separate status fetch. `grade:` is **distinct from the DB `status` field** (`active`/`deprecated`) —
never overload that field, never name a tag `status`. **Mutate the grade with `context_tag`** —
`context_tag(id, action:"replace", tag:"grade:<g>")` sets-or-swaps the grade **in place** (idempotent,
namespace-scoped, no id reissue, edges/embedding preserved). This is what makes the grade a first-class,
cheaply-maintained field — and makes **backfill anchor-safe** (no id churn), unlike `context_correct`.
**Firewall unchanged:** `grade:proven` is set only alongside `context_correct` attaching `proven_by` (the
audited artifact event) — never a bare tag flip. **Rate limit:** ~60 tag-writes/hour; a bulk grade sweep
must batch under it (see OBS-9).
