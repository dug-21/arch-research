# theme:workflow-harness — Research Plan & Operating Model

**Status:** active plan · 2026-07-22 · owner-directed ("make this systemic; lay out our plan to begin
chasing these down"). Companion to `themes.md` (`theme:workflow-harness`) and
`workflow-harness-delivery-model-paths.md` (the P1–P14 / axes map).

---

## 0. What makes it *systemic* (not a one-off study)

This theme runs as a **standing funnel**, re-entered on a cadence — the factory machinery applied to one
question. Each cycle:

```
scout (external scan)  →  hypothesizer (divergent)  →  goal-owner (triage: park/probe/build)
   →  owner gate (promote 0..n to bounded proof-goals)  →  factory-poc + firewall  →  handoff to dug-21/jurati (§7)
```

- Every artifact tagged **`theme:workflow-harness` + run-id**; survivors formalized as graph
  `finding`+`hypothesis` / `technology` by the **curator** (single writer). Files are provisional;
  the graph is settled (D1).
- **Run discipline (OBS-10):** each run opens a **GitHub Issue + `context_cycle`** at INIT — not
  retroactively. Run-ids: `wfh-NNN`.
- **Cadence:** weekly, wave-0 manual kick.
- **Reflexive metric (§9):** funnel hit-rate — candidates → hypotheses → survive triage → proven →
  pulled into JURATI. Tuning targets: the scout source-mix + the hypothesizer/triage prompts.
- **Firewall:** structure moves freely; `proven` only on a demonstrated-by-us artifact. This plan moves
  *structure*.

**Two stances held simultaneously (owner directive):**
- **Learn from the field** — how others provision / inject / control / deliver is *input*, mined for best
  ideas to pull into JURATI.
- **Do better where nobody's looking** — the **UX / exposure of the workflow** (the live-debugger canvas;
  "what the LLM is given next, and why") is the claimed white space and the garage's highest-value
  proprietary output. *Learn broadly; differentiate sharply.*

## 1. Standing research tracks

| Track | What | Feeds | Status |
|---|---|---|---|
| **T1 — Competitive landscape (learn-from)** | How comparable agent-harness + workflow-viz tools provision, inject context, control the LLM, visualize, and deliver / tenant / monetize | delivery decision (P1–P14) + a best-ideas-to-pull list | **running (wfh-001)** |
| **T2 — UX / exposure differentiator (do-better)** | The live-debugger canvas + workflow-as-visible-graph (H1/H2) — the claimed white space; JURATI's moat | H1/H2 | gated on T1 validating the gap |
| **T3 — The ontology (load-bearing)** | Minimal typed vocabulary of a coding-agent's operating context (H4); everything downstream depends on it | H4/H7 | queued (P10 probe) |
| **T4 — Delivery / tenancy model** | Owner's own fleet = **P14** (one queen, N projects, one trust domain; #12-blessed, zero (b) cost) — buildable now. Stranger-facing SaaS = deferred, informed by T1 + T5 | H3/H6/H8 | P14 direction settled; SaaS deferred |
| **T5 — Sovereignty & security substrate** | Anti-lock-in invariants + the costs the scan surfaced: Anchor-B (b) (schedule-coupled to Unimatrix #5689), workflow-artifact supply-chain (sigstore-class), token-margin & push-upgrade lock-in vectors | H5/H8 + the #12 seam | tracked |

## 2. Track → hypothesis → handoff

T1 → H3/H6/H8 (delivery evidence) · T2 → H1/H2 · T3 → H4/H7 · T4 → H3/H6/H8 + P14 · T5 → H5/H8 + the
issue-#12 security seam. Proven pieces hand off as issues to **`dug-21/jurati`** (§7 bridge) — the factory
proves, JURATI ships.

## 3. Sequenced runs (the "begin chasing" queue)

1. **wfh-001 — external scan (T1) — NOW.** Two scouts:
   - **(A)** agent-harness delivery + context-injection + control model + business/tenancy model
     (Cursor, Windsurf, Devin, OpenHands, Replit, Claude Code, aider, Cline, Goose, Factory.ai, …).
   - **(B)** workflow-visualization + "what-the-LLM-sees" UX (LangGraph Studio, Langflow, Flowise, n8n,
     Rivet, Dify, PromptFlow, Temporal/Windmill; LangSmith/Langfuse/Phoenix traces) — **pressure-tests the
     owner's "nobody has exposed this" claim.**
   - → hypothesizer folds best ideas → goal-owner triage → owner promotes.
2. **wfh-002 — P10 ontology/value probe (T3) — next.** Build the git-native template from this repo's own
   `.claude/`; proves the day-one value hypothesis **and** the ontology, zero infra, independent of the
   tenancy decision. The cheapest kill/confirm of the whole value premise.
3. **wfh-003+ — as triage promotes** — e.g. the UX-canvas design spike (T2); the P14 fleet-provisioning
   proof (T4).

## 4. Discipline

Plane = **research** (feeds JURATI). Workflow ≠ knowledge (three stores) holds throughout. Nothing here
reaches `proven` without a demonstrated artifact. The owner is the human gate on triage; the goal-owner is
advisory (relevance + step-function). Method-stream `wf:` stamps each run.

## 5. Research register — the slate (single source of truth for "what's on the list")

Everything wfh is recorded; it was just spread across five surfaces. **This register is the index** so
nothing is lost. All items are **git-side / provisional** (`seed`) until triaged — graph-formalization
(curator) happens *after* triage. Nothing enters the graph un-triaged.

**Where each surface lives:**
- Hypotheses **H1–H8** → `themes.md` (`theme:workflow-harness`).
- Delivery-model design space (axes A1–A8, paths **P1–P14**) → `proposals/workflow-harness-delivery-model-paths.md`.
- **wfh-001** scan candidates (~20 tools) + white-space verdict → `product/research/wfh-001/scout-candidates.md`; live record → **Issue #41**; telemetry → `context_cycle wfh-001`.
- Tracks **T1–T5** + run queue → this file (§1, §3).

**Hypotheses (H1–H8):**

| ID | One-line | Status |
|---|---|---|
| H1 | control-plane-as-graph (coordinate + live debugger) | seed |
| H2 | harness-as-observability (token/error real-time) | seed |
| H3 | one JURATI across many repos/domains (A dispatch / B span) | seed (A ≡ P14 direction) |
| H4 | ontology-first (minimal typed vocab) — **must subsume `AGENTS.md` losslessly** (wfh-001) | seed |
| H5 | anti-lock-in as consequence (portable graph → swappable LLM) | seed |
| H6 | build-once ecosystem (subgraphs on shared ontology) | seed |
| H7 | definition vs events, two backends (three stores total) | seed |
| H8 | sovereignty-preserving SaaS (P14 fleet now; stranger-SaaS later) | seed (P14 settled) |

**Open questions surfaced by wfh-001 (new items on the slate):**
- **Q-a** — Can the typed-graph ontology subsume the `AGENTS.md` flat-file standard losslessly? (H4; market-standard risk.)
- **Q-b** — Is a **prospective + causal** context-injection view ("what's injected next, and why") buildable? (H1/H2 — the unoccupied moat per the wfh-001 verdict.)
- **Q-c** — Moat durability: is the coding-agent-context ontology + control-plane framing defensible vs a fast-follower canvas? (strategy/goal-owner.)
- **Q-d** — Best-idea probes to pull in: Cannoli `LoggingEdge` as a first-class view; fix Claude Code `/context`'s 4 gaps (hidden content, linear-not-graph, retrospective, CC-only); OTel GenAI attr vocabulary as the portable wire seam.

**Run log:**

| Run | Scope | Status |
|---|---|---|
| wfh-001 | external landscape scan (T1) | **done** → at triage gate (Issue #41) |
| wfh-002 | P10 git-native template probe (T3 ontology/value) | queued |
| wfh-003+ | promoted from triage | pending |

**Lifecycle:** item lives here (git) as `seed` → **triage** (goal-owner: park / probe / build) → a promoted
survivor gets a **GitHub Issue** (live surface) **and** a graph node (curator: `finding`+`hypothesis` or
`technology`, `grade:claimed`, tagged `theme:workflow-harness` + run-id). Parked items stay in this register.
The register is the **whole slate**; the graph holds only the triaged, evidence-bearing subset.
</content>
