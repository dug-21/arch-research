# shd-002 — Agentic harness landscape for the self-hosted dev/research loop

**Status:** SCOPE
**Goal(s):** `shd` (primary, #3)
**Capability target(s):** **C2 — An agentic harness drives research+coding tasks to completion** (#5)
**Confidence-required:** directional
**Phase / area:** harness
**Cycle topic / Issue:** shd-002

Governing NFRs (via `About→ C2`): N1 owned-HW/budget (#7) · N2 no-outage (#8) · N4 multi-machine-ready (#10).

---

## The question

Survey the landscape of agentic harnesses that can drive multi-step research+coding tasks to
completion against a **self-hosted / local** model backend, and rank them — what's easy, what's
hard, what's a dream — to recommend a leading candidate and a validated follow-on.

> Which agentic harness can autonomously complete a multi-step research+code task on a local model
> backend — and which one do we POC first?

## Why it matters

C2 is the spine of `shd`: capable local inference (C1) is inert without a harness that can *drive*
it through multi-step work with no manual steps (C2's `done_when`). C2 is also the prerequisite
consumer of C1 and the host for C3's escalation. Picking the wrong harness re-foundations the loop.

## Known constraints & prior art  *(build on these — do not re-derive)*

- **Reuse-first:** no `technology` nodes exist for harnesses yet (KB has only the factory-plane
  bootstrap entries) — this scope establishes them. Curator searches `category:technology` before
  storing, per the access rules.
- **N1 / N2:** the harness must drive a **local** backend (OpenAI-compatible endpoint / litellm /
  Ollama) and keep working with no internet except deliberate C3 escalation.
- **N4 (D11):** weight distribution-compatibility as a **tie-breaker, not a gate** — does the
  harness architecture *foreclose* multi-machine coordination, or extend to it later?
- **Methodology §12 candidates** to confirm/expand: `T3a` Claude Code → local via OpenAI-compatible
  shim; `T3b` alternative OSS harness (aider / opencode).
- **Methodology §12 lesson L1:** harness viability needs a **live tool-call smoke test**, never
  doc-reading — several harnesses *claim* local support; only some stream tool-calls correctly.
  (This bites in the *validated* follow-on, not here, but the landscape should flag it per candidate.)

## Bounded investigation (workstreams)

- **W1 — Harness inventory.** Enumerate agentic harnesses that drive multi-step research+coding
  (Claude Code, aider, opencode, OpenHands, Cline, Goose, and any others surfaced). *Output:* a
  candidate list with a one-line capability profile each.
- **W2 — Local-backend compatibility.** For each candidate: can it target a self-hosted model
  (OpenAI-compatible shim / litellm / Ollama)? How cleanly (config vs fork)? *Output:* a
  local-compat matrix (N1/N2).
- **W3 — Multi-step autonomy & tool-calls.** Which candidates actually complete multi-step tasks
  with no manual steps, and what's known about tool-call/streaming reliability on local models
  (the L1 risk)? *Output:* an autonomy + tool-call assessment per candidate (claims vs evidence).
- **W4 — Distribution-compatibility (N4).** Does each candidate's architecture foreclose or extend
  to multi-machine coordination (coordinator-over-workers, remote task dispatch)? *Output:* a
  forecloses / extends flag per candidate — a tie-breaker, not a gate.
- **W5 — Synthesis & ranking.** Rank candidates easy / moderate / hard / dream with the determining
  constraint named; recommend the leading harness + a phasing; specify the **validated follow-on
  scope** (`shd-003`) and exactly what its POC must demonstrate. *Output:* ranked map + recommendation.

## Expected output (FINDINGS.md)

1. **Harness feasibility map** — each candidate tagged easy / moderate / hard / dream, determining constraint named.
2. **Local-backend compatibility matrix** (N1/N2).
3. **Distribution-compatibility flags** (N4) — forecloses / extends, per candidate.
4. **Recommendation** — the leading harness + reasoning, as a `position` finding.
5. **Validated follow-on** — a draft `shd-003` scope question + the POC bar it must clear (the L1 live tool-call smoke).

## Proof bar  *(directional)*

**Structure-only — no status change.** Produces `finding`s + `technology` nodes left `claimed` +
a `position` recommendation. It **spawns** a validated follow-on (`shd-003`) that will move a
technology to `proven`; this scope proves nothing itself.

## Explicitly out of scope

- Building, installing, or running any harness (that is `shd-003`, the validated follow-on).
- Local model **serving** itself (that is C1, a separate scope).
- The escalation/routing logic (that is C3).
- Final harness selection by benchmark — this scope *recommends a direction* and names what to POC.

## Coverage / done call  *(synthesis)*

Loop-until-dry: stop when **K=2** consecutive searches surface no new harness **and** **≥2**
independent findings corroborate the leading candidate. Agent proposes "sufficient"; **human
confirms** at the synthesis gate.
