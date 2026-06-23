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
