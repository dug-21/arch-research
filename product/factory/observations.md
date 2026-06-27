# Factory Observations Log

Running notes from **manual runs** that inform Tier-1 automation — agent contracts, role gaps,
reviewer needs, operational hazards. Distinct from `decisions.md` (settled choices); these are
**needs/observations surfaced in practice**, candidates to graduate into the factory roster or the
`factory` plane once a pattern is confirmed.

---

## OBS-1 — A "goal-owner" relevance review is a distinct, currently-missing gate
*2026-06-23 · from shd-002*

**Observed need.** Beyond "is the evidence real?" (validator/firewall) and "did we research
enough?" (coverage), there is a third, separate question: **did the findings answer the question
that is RELEVANT to the broader goal?** — i.e. target/relevance review. A run can be evidence-clean
and well-covered yet drift off the goal's actual need.

**Reviewer needs surfaced this run** (→ future `goal-owner` agent contract):
- **Relevance / target fidelity:** did shd-002's harness landscape actually answer C2's `done_when`
  in service of the `shd` goal — or optimize a sub-metric? (Here: yes; recommendation defers the
  real proof to shd-003, which is appropriate.)
- **Constraint alignment:** were the governing NFRs weighted correctly? (N1/N2 local — yes; N4
  distribution correctly down-weighted as a tie-breaker, not a gate; N3 N/A to C2.)
- **Gap check:** did decomposition miss a capability the findings imply? (None surfaced this run.)

**Automation implication.** `goal-owner` is an **advisory gate at synthesis** (analogous to
`uni-zero-review` / vision-guardian in the reference workflows), distinct from the validator
(firewall) and the coverage gate. Add to the Tier-1 roster; its checklist = the bullets above.

## OBS-2 — Subagent file-writes are blocked; the researcher contract must account for it
*2026-06-23 · from shd-002*

Researchers W1/W2/W4 wrote their findings files via Bash; **W3 was fully blocked** from file writes
and returned its markdown inline for the parent (curator) to persist. The runbook's
"researcher → FINDINGS file" step is not reliably executable by a subagent.

**Automation implication.** Either grant researcher agents a write path to
`product/research/{id}/`, **or** make the curator/leader responsible for persisting
researcher-returned findings. Pick one and bake it into the Tier-1 researcher + curator contracts.

## OBS-3 — Unimatrix connection goes stale mid-run (issue #830)
*2026-06-23*

`context_cycle` / `context_store` calls were interrupted ~4× by the stale-connection symptom; each
cleared on a manual `/mcp` reconnect. Filed `dug-21/unimatrix#830`.

**Automation implication.** An automated leader needs **retry/reconnect resilience** around
`context_*` calls, or unattended runs will stall. Not a blocker in manual mode (human reconnects).

## OBS-4 — Goal-owner needs a step-function / ambition review (directional only)
*2026-06-24 · from shd-004*

The goal-owner checklist (OBS-1) guards relevance / constraint / gap — all of which **assume the
stated objective is the right altitude.** shd-004 optimized the stated (single-box, N1-bounded)
objective efficiently and correctly, but nothing in the process pressure-tested whether the
**objective itself under-reached**. The human did it manually: *"if we leveled up, what does that
buy us — and is it worth it?"*

**Need.** A 4th goal-owner dimension — **step-function check**: given the landscape, name any
higher-value level-up beyond the stated objective (what it buys, its cost) → pursue /
defer-and-record / decline. Guards against tunnel vision from a tightly-scoped objective. The
"worth it" cost/benefit + advisory-to-human keeps it from becoming scope-creep; deferred level-ups
are **recorded** (D10/D11) so they aren't lost.

**Confidence-conditioned.** Active on **directional/empirical** (mapping terrain is when you can
assess a level-up); **suppressed on validated/proof** unless the scope explicitly stated it (a proof
is a bounded commitment; re-opening ambition mid-proof derails it).

Baked into `goal-owner.md` (wf:v0.8); enhancement #20 updated. The reflexive loop (§8) operating
manually — a real run surfaced a process gap → a workflow edit.

## OBS-5 — Non-gate interactive prompts break the autonomous run; gates are the ONLY stops
*2026-06-26 · from shd-004 (first AUTONOMOUS run)*

shd-004 was the first run executed autonomously (research-leader spawning real specialist agents,
not inline roles). The leader twice used `AskUserQuestion` at a **non-gate** point — to refine an
in-envelope steer ("add a $5K hardware tier") — and it **blocked the autonomous flow**; the human
flagged it directly ("STEP WITH THE QUESTION CONTEXT. This blocks autonomous … it stopped our
autonomous workflow earlier").

**Rule surfaced.** The research-leader must confine **blocking/interactive** prompts to the **3
human gates ONLY** (scope approval · coverage confirm · synthesis review). An in-envelope steer is
executed with sensible **defaults** + surfaced in **Issue comments / the work product** — never a
blocking question. A non-gate question is a defect, not diligence. (→ factory enhancement, claimed;
`Prerequisite→` #25 Orchestrate a phase-gated run.)

## OBS-6 — Observation telemetry now flows: the attribution fix is confirmed (#24 partially unblocked)
*2026-06-26 · from shd-004*

The prior symptom (enhancement #24 "process-axis telemetry wiring"; capability #32 tagged `blocked`)
was `context_cycle_review` returning **"No observation data."** On shd-004 it now returns rich data:
`total_records: 186`, `attributed_session_count: 1/1`, `knowledge_stored: 22`, per-phase stats with
gate outcomes, `cold_restart_events: 3` (the real session gaps). **Confirmed: the attribution fix
landed.**

**Still partial (not complete):** `total_tool_calls: 0`, `knowledge_curated: 0`,
`feature_knowledge_reuse.total_served: 0` remain unpopulated — the cycle/phase/attribution stream is
wired, but the per-tool-call and curation sub-streams are not yet. Enhancement #24 → `partial`, not
`proven`; the reflexive capability #32 stays `blocked` until telemetry can power an A/B improvement.

## OBS-7 — Subagent file-writes are blocked for EVERY specialist; the contract must flip to leader-persists
*2026-06-27 · from shd-005 (first multi-specialist autonomous run)*

shd-005 spawned **8 read-only researchers** (W1–W6 + W7a/W7b). **Every one had its file-write
blocked** and returned its FINDINGS markdown inline for the leader to persist (the leader wrote all
8 `findings-*.md` + the two REPORT/synthesis files). This is no longer an intermittent symptom
(OBS-2, n=1 partial on shd-002) — it is **deterministic in this harness**: a spawned specialist
cannot write to the repo.

**Rule surfaced (supersedes the OBS-2 "pick one" ambiguity).** The researcher contract is
**read-only, returns-markdown**; the **leader/curator is responsible for persisting** every
researcher artifact (and must budget context for it — inline returns of 8 large findings files are
heavy). The runbook's "researcher → FINDINGS file" step is **not executable**; rewrite it to
"researcher → returns markdown → leader persists." (→ factory enhancement #21, now strongly
evidenced; should move toward `partial`/contract-locked.)

## OBS-8 — Two method wins confirmed: run-id-tag yield query works, and the goal-owner step-function fired
*2026-06-27 · from shd-005*

1. **Telemetry-tag fix works (#65).** shd-004's per-run yield query returned empty (curator hadn't
   tagged). shd-005's curator tagged every node `shd-005`; `context_lookup(tags:["shd-005"])` returns
   all 20 nodes — **per-run knowledge-yield is now queryable by tag** (note: by *tag*, not the `topic`
   field, which the curator set to `shd-routing`). The runbook's run-id-tag convention is validated.
2. **Goal-owner step-function dimension (OBS-4) fired productively, manually.** A human "what if we
   level up?" steer mid-run surfaced the platform-coverage reframe and then the platform-vision goal
   (#92) — captured build-deferred (D10) without derailing the directional run. The reflexive loop
   (§8) operating by hand: a run produced a methodology lesson (#90/#91, platform-blindness) **and** a
   new product-vision goal, both firewall-clean. Evidence the goal-owner role earns its place.
