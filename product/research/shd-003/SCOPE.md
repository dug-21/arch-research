# shd-003 — Live multi-step tool-call smoke test for the C2 harness slate

**Status:** SCOPE (staged — blocked on local hardware; see below)
**Goal(s):** `shd` (primary, #3)
**Capability target(s):** **C2 — An agentic harness drives research+coding tasks to completion** (#5)
**Confidence-required:** validated
**Phase / area:** harness
**Cycle topic / Issue:** shd-003

Governing NFRs (via `About→ C2`): N1 owned-HW/budget (#7) · N2 no-outage (#8) · N4 multi-machine-ready (#10).
Builds on shd-002: position finding **#17**, mechanism finding **#16**, technologies **#11–#15**.

---

## The question

Does a harness from the shd-002 slate **actually complete a multi-step research+code task on a
self-hosted/local model backend** — with reliable tool-calls across the whole task, not just a
one-shot demo?

> Which harness clears C2's `done_when` on local hardware, on a live smoke test — and becomes the
> first `proven` technology for C2?

## Why it matters

This is the firewall step for C2. shd-002 was directional — it ranked candidates by *mechanism* but
**proved nothing** (methodology §12 L1: viability needs a live tool-call smoke, never doc-reading).
shd-003 is where a technology moves to `proven`/`partial` on a real artifact.

## Known constraints & prior art  *(build on these — do not re-derive)*

- **Slate + order from position #17:** (1) **aider** (#11), (2) **Claude Code + local /v1/messages
  shim** (#12, T3a), (3) **Continue** (#13, only if #6677 metadata gate is overridable). opencode
  and Cline excluded until their fix-PRs (#20719 / #4362) are confirmed.
- **Mechanism finding #16:** native-tool-call harnesses break on the local proxy/model contract;
  the test must exercise that contract, not avoid it.
- **Reliability is multiplicative** (95%/call ≈ 66% over 8 steps) — measure *completion*, not
  per-call success.

## Bounded investigation (the POC)

- **P1 — Local backend stand-up.** A local proxy (Ollama / vLLM / LiteLLM) serving a tool-capable
  coder model (e.g. Qwen3-Coder-class). *Output:* a reachable local endpoint + recorded config.
- **P2 — Defined task.** One fixed multi-step research+code task requiring **≥6–8 sequential tool
  calls** (read → edit → run → fix loop). *Output:* the task spec, identical across harnesses.
- **P3 — Smoke-test the slate in order.** Drive aider → Claude Code(T3a) → Continue against P1+P2.
  *Output:* per-harness transcript + completion verdict (completed with no manual steps? yes/no).
- **P4 — Record proof.** For the first harness that completes: the curator moves its technology to
  `proven` with `proven_by` capturing the **envelope** (hardware, model, task); partial completions
  → `partial`.

## Expected output

1. Per-harness completion result + **transcript artifact** (the real evidence).
2. The first technology moved to `proven`/`partial`, envelope recorded.
3. If the slate fails: a `lesson-learned` + a revised slate (frontier-change → maybe a new scope).

## Proof bar  *(validated)*

**Moves status.** A technology reaches `proven` ONLY on an attached real artifact (transcript) that
demonstrates C2's `done_when` — the harness finishes the P2 task with no manual steps on the local
backend, **demonstrated by us**. Partial evidence → `partial`. This is the firewall in action.

## Explicitly out of scope

- Exhaustive benchmarking / model selection (one capable model is enough to prove the harness).
- C1 (local serving), C3 (escalation) — separate capabilities.
- Distribution/multi-machine (N4 is architected, not built — D11).

## Coverage / done call

A validated scope is done when a technology clears `done_when` with an artifact (or the slate is
exhausted and a `lesson-learned` + revised slate is recorded). Human reviews at synthesis.

---

## ⚠ Staging note (2026-06-23)

**Blocked on local hardware.** shd-003 requires a machine with a capable local model + serving
proxy + the harnesses installed — not available in the current devcontainer. Staged at its scope
gate; runs when hardware is available. This is the first scope to spend **real compute** (the only
phase the budget bites — methodology §14.6).
