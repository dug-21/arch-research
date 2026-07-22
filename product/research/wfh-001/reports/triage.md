# wfh-001 · Triage — theme:workflow-harness

**Run:** wfh-001 · **Theme:** `theme:workflow-harness` · **Date:** 2026-07-22 · **Role:** goal-owner (B — convergent gate) · `agent_id: wfh-001-goal-owner`
**ADVISORY ONLY.** No graph writes, no status moves. The owner decides at the blocking gate (Issue #41); the curator files.
**Protocol deviation absorbed:** no hypothesizer ran; hypothesis set = owner-injected H1–H8 + scan-surfaced Q-a–Q-d.
**Dedup spot-check (read-only `context_search`):** confirmed — graph holds only the five shd-lens harness nodes (#11–#15) + #16/#18; **zero** workflow-viz/observability/delivery-lens nodes. Scout's dedup verdict stands.

---

## 1. Hypothesis triage — H1–H8

| H | Mechanism/fit | Theme-align | Novelty | Effort-vs-payoff | Route | Rationale (one line) | Q's |
|---|---|---|---|---|---|---|---|
| **H4** ontology-first | **high** | **high** | **high** | **high** — wfh-002 already queued, zero infra | **VALIDATED-BUILD** (= wfh-002, confirm queued run — do not open a second) | The white-space verdict says the moat IS the ontology+framing, not the viz; wfh-002 is the cheapest kill/confirm of the entire theme premise | Q-a |
| **H1** control-plane-as-graph | high (Cannoli is an existence proof of one-structure-both-jobs — for authored workflows, not agent operating context) | high | med-high — components crowded; the **combination** (subject + prospective/causal + authored-durable + harness-driver) is unoccupied | med — full build heavy; a structure-only design spike is cheap | **DIRECTIONAL-PROBE** — T2 design spike, **sequenced strictly after wfh-002 reports** | The gap is real but PARTIAL; the prospective+causal view (Q-b) is the one genuinely unoccupied claim, and its substrate is H4's ontology — probing before wfh-002 risks specifying a canvas over an ontology that fails | Q-b, Q-c, Q-d (as design inputs) |
| **H2** harness-as-observability | high (trivially — harness sits at the single edge) | high | **low** — per-step token/cost/errors is commoditized table-stakes (LangSmith/Langfuse/Phoenix/Weave/Cannoli); "live per-node badge" is a minor gap, not a thesis | low as standalone | **PARK** — fold into H1's probe as a *requirement*, not a bet | Novelty fails: standalone H2 re-proves known ground; it survives only inside H1's combination. Adopt OTel GenAI attrs (Q-d) at build time | Q-d (partial) |
| **H3** one JURATI, many repos | med-high (variant A rides proven #12 slug isolation; P3 split topology shipped by Factory/Copilot) | high | med | low now — proof needs an existing workflow definition | **PARK** | Sequencing: upstream ontology (wfh-002) unproven, and T4 already settled the P14 direction — no live uncertainty a probe would cut | — |
| **H5** anti-lock-in as consequence | med — a consequence claim, untestable until an executable definition graph exists | high | med (market rewards BYO/portable — the *value* is corroborated, the *mechanism* untested) | low — no cheapest test exists yet | **PARK** | Not falsifiable before H4+H1 produce a runnable graph; two-backend test re-enters then | — |
| **H6** build-once ecosystem | med (generalizes H3) | high | med | very low — vision-scale, no cheap test; consolidation evidence (Continue→Cursor) only sharpens a *later* registry choice (P12 registry-neutral) | **PARK** | No cheapest test; pure architecture-for-later | — |
| **H7** definition vs events, two backends | high (sound; scan corroborates — Recipes/Playbooks/Skills show definition-as-versioned-artifact in the wild) | high | med | med — proof is a paper analysis, but nothing is blocked on it yet | **PARK, with rider** | No decision blocked until a build is promoted; instead **flag wfh-002 to report backend implications** (seam #8: flat package formats can calcify against workflow-as-graph) — absorbed spend, not new spend | — |
| **H8** sovereignty-SaaS | med (premise coherent; (b) cost is a step function schedule-coupled to Unimatrix #5689) | med (lens yes; the *buyer* doesn't exist yet) | med | very low — the proof is the most expensive test on the slate | **PARK** | Owner already deferred stranger-SaaS (T4: P14 now); scan evidence hardens the park — market *punished* hosted-only/surprise-priced moves (Cursor apology, Copilot halt, Replit incident) | — |

**H4 proposed `done_when` (wfh-002):** this repo's complete `.claude/` operating context (CLAUDE.md, rules, skills, agent-defs/roles, hooks/gates, settings/permissions) is expressed in the minimal typed vocabulary such that (a) it **round-trips losslessly** back to functioning flat files, (b) a **generated `AGENTS.md`** from the typed graph is consumable by at least one third-party tool that reads the standard (Q-a — lossless subsumption demonstrated, not asserted), and (c) the residual-gap list is empty or each gap is explicitly named and owner-accepted. Artifact = the template repo + the round-trip diff, demonstrated by us. Rider: a one-page backend-implications note (H7/seam #8).

---

## 2. Candidate triage — curator actions

**Partition A (13 tools) — file/extend, no probes motivated.** The knowledge is already bought; filing is cheap ledger work. All pricing/adoption figures stay flagged **unverified secondary** in `cites:` — they are context, not evidence.

| Group | Curator action |
|---|---|
| aider #11, Claude Code #12, Continue #13, OpenHands #14, Goose #15 | **Extend/tag known nodes** (`context_correct` to add the delivery/injection/control lens; tag `theme:workflow-harness` + `wfh-001`). Do NOT duplicate. Continue: add the consolidation note (acquired, repo read-only) — no further characterization spend on a winding-down product |
| Cursor, Windsurf, Devin, Replit, GitHub Copilot, Cline, Factory.ai, Amp | **File new** `technology`, `grade:claimed`, tag `theme:workflow-harness` + `wfh-001`, source `external-scan` |
| Synthesis findings | **File 3 `finding` nodes** (the durable yield of Partition A): **F1** — `AGENTS.md` is a de-facto cross-tool flat-file standard (→ `Motivates` H4 node; carries Q-a). **F2** — enforcement-outside-the-LLM is shipped/validated (hooks, SecurityAnalyzer, branch/PR gates, exit-code tiers, Plan-mode) — the theme's core thesis corroborated by comparables. **F3** — market rewards no-markup/BYO-key/portable; hosted-only + surprise pricing is punished; BSL/SSPL triggers forks (→ supports the H8 park and the P14/P10 direction) |
| Copilot PR-gates + Devin `request_scope` | Note inside F2 as the closest external analogues to JURATI per-agent capability gating (feeds issue #12 — already ratified work, **no new probe**) |

**Partition B (~22 tools) — file selectively; fold the long tail.** All net-new, but 22 individual nodes is graph bloat for a lens where most rows exist only to prove crowdedness. Mind the ~60 tag-writes/hour limit — batch.

| Group | Curator action |
|---|---|
| **The white-space verdict itself** | **Highest-value artifact of the run.** File as a `finding`: "workflow-viz white space = PARTIAL; unoccupied = the combination (coding-agent operating context as subject + prospective/causal injection view + authored-durable graph + harness-as-driver); risk = fast-follower, moat is framing+ontology not viz." `Supports` edges toward the H1/H4 nodes |
| Cannoli, Rivet, LangGraph Studio, Dify | File new `grade:claimed` — the four builders with load-bearing mechanisms (LoggingEdge; inline assembled-prompt; time-travel state; strongest-OSS-canvas). Cannoli's `LoggingEdge` = named design input to the H1 probe (Q-d) |
| LangSmith, Langfuse, Phoenix, Weave | File new `grade:claimed` — the observability tier that *defines* the crowded component; Phoenix's per-run-derived graph filed as the named **anti-pattern to beat** |
| OTel GenAI conventions | File new — the portable wire seam (Q-d); note opt-in/PII-flagged, so JURATI owns the capture decision |
| Claude Code `/context` + CC OTEL | **Extend node #12** (dogfood-signal), don't file separately — record the four gaps (hidden content, linear-not-graph, retrospective, CC-only) as the sharpest adjacency |
| Langflow, Flowise, n8n, Helicone, OpenLLMetry, MS Prompt Flow | **Do-not-file individually** — fold into one `finding`: "mid-tier canvases/tracing confirm the crowded component; Prompt Flow on retirement path" |
| Temporal, Windmill, Kestra, Prefect, Node-RED | **Do-not-file individually** — fold into one `finding`: "general orchestration has no what-the-LLM-saw concept" |
| Obsidian class (Caret, Canvas LLM, SystemSculpt) | **Do-not-file** — abandoned/unverified/off-mechanism; Cannoli carries the class |

No Partition B candidate motivates its own probe; their value routes entirely into the H1 probe's design inputs (Q-d) and the white-space finding.

---

## 3. Parked set — one reason each

| Item | The one reason |
|---|---|
| H2 | Commoditized component — survives only inside H1's combination, not as its own bet |
| H3 | Upstream ontology unproven (wfh-002); P14 direction already settled — nothing to cut |
| H5 | Not falsifiable until an executable definition graph exists |
| H6 | Vision-scale generalization with no cheapest test |
| H7 | No decision blocked yet; backend-implications flag absorbed into wfh-002 (zero new spend) |
| H8 | Owner-deferred (T4) and the scan's market evidence hardens the deferral |
| Langflow / Flowise / n8n / Helicone / OpenLLMetry / Prompt Flow (as nodes) | Only prove crowdedness — folded into one finding |
| Temporal / Windmill / Kestra / Prefect / Node-RED (as nodes) | No LLM-context concept at all — folded into one finding |
| Obsidian class (Caret / Canvas LLM / SystemSculpt) | Abandoned / off-mechanism / unverified |
| Continue deep re-characterization | Product winding down post-acquisition |
| Any probe on P13 trial-isolation / P6 tenant-trust | Downstream of a SaaS decision that is itself parked (H8) |

---

## 4. Funnel telemetry

**Hypotheses (owner-injection; no hypothesizer ran — novelty classes assessed at triage, a deviation to note in the run retro):**
- Generated: **8** (+ 4 attached questions Q-a–Q-d)
- → VALIDATED-BUILD: **1** (H4, via already-queued wfh-002) · DIRECTIONAL-PROBE: **1** (H1, sequenced) · PARK: **6**
- By novelty class: non-obvious **2** (H4, H1 — both carry the unoccupied combination) → both survived. Obvious/linear **1** (H2) → parked. Adjacent/consequence **5** (H3, H5, H6, H7, H8) → all parked. The funnel is behaving: only the non-obvious survived.
- Q routing: Q-a → inside H4's `done_when` · Q-b, Q-c, Q-d → inputs to the H1 probe. Zero questions promoted as standalone spend.

**Candidates (external-scan + 1 dogfood-signal):**
- Generated: **~35** (Partition A 13; Partition B ~22)
- → individual graph nodes: **17** (A: 8 new + 5 extended; B: 9 new + 1 extension of #12) · folded into findings: **~14** · do-not-file: **3–4**
- Findings filed: **5–6** (3 from A, white-space verdict + 2 fold-findings from B)
- By novelty: net-new 30 → 17 filed individually; known/new-lens 5 → 5 extended (0 duplicated). Zero candidates motivate a new probe — telemetry consistent with a *learn-from* track: the yield is findings + design inputs, not new bets.

---

## 5. Step-function check (survivors: H4 build, H1 probe)

Two adjacent level-ups worth naming — both **defer-and-record**, neither pursued now:

1. **Ontology-as-open-standard (the compile-target play).** If wfh-002 proves the typed vocabulary subsumes `AGENTS.md` losslessly, the level-up is publishing the ontology as an open spec whose compiler *emits* every tool's flat format (AGENTS.md, CLAUDE.md, .cursor/rules…) from one typed graph — JURATI becomes the **authoring layer above every harness**, not a competitor canvas. **Buys:** converts the fast-follower risk (Q-c) into the moat — a canvas can be copied; an ontology with adoption compounds. A step-function, not linear. **Costs:** spec + multi-format compat maintenance; open-spec publication invites the very followers Q-c fears, betting authorship beats imitation. **Call: defer-and-record** — a candidate wfh-003, decidable only *after* wfh-002 shows the ontology holds. Worth it *then*; premature now.
2. **The reflexive D10 move** (JURATI as this garage's own harness, retiring LLM-is-the-harness). **Buys:** a step-function on process capability #66 — structural gates + metering for the funnel itself. **Costs:** high; explicitly a daystrom/process-plane higher-bar move; pursuing it inside this research theme would derail both. **Call: defer-and-record** — already recorded in themes.md as reflexive-for-later (D10); no new action, just confirming it is not lost.

Neither relaxes the firewall or the budget; both are options on the owner's table, not mandates.

---

## 6. Overall recommendation to the owner (blocking gate, priority order)

1. **Promote H4 → confirm wfh-002 proceeds as the VALIDATED-BUILD**, adopting the concrete `done_when` above (lossless round-trip + generated-`AGENTS.md` subsumption + owner-accepted gap list) plus the H7 backend-implications rider. This is the whole theme's cheapest kill/confirm, zero infra, already queued — the week's one research spend.
2. **Authorize the curator sweep** (bounded ledger work, no research spend): extend 5 + file 8 (Partition A), file ~9 + extend #12 (Partition B), file 5–6 findings including the white-space verdict; batch under the tag-write rate limit.
3. **Pre-approve the H1 DIRECTIONAL-PROBE contingent on wfh-002 passing** — a structure-only T2 design spike: the data model for "what's injected next, and why" (Q-b), a moat-durability memo (Q-c), Q-d best-ideas (Cannoli `LoggingEdge`-as-primary-view, the four `/context` gaps, OTel GenAI vocabulary) as inputs. If wfh-002 *fails*, H1's substrate is gone and the probe is dead — do not start it early.
4. **Promote nothing else.** Six of eight hypotheses park; zero candidates motivate probes. One build, one contingent probe, no new runs opened — that is the correct shape for a first scan of a theme whose load-bearing object is still unproven.
 naming (H8's "SaaS-from-start" is the inverse — a step-function *bill*, not a level-up).

---

## 6. Overall recommendation to the owner (blocking gate, priority order)

Budget shape: the theme's envelope is ~1–2 days/week; wfh-002 is already queued and zero-infra. This triage adds **one** new bounded spend (the H1 probe) and otherwise converts the scan into graph structure. Promoting nothing beyond wfh-002 would also be defensible — the probe earns its slot only because it attacks the single highest-value uncertainty the scan surfaced (Q-b, the moat's unproven component).

1. **Confirm wfh-002 (H4/P10) as the sole VALIDATED-BUILD** with the `done_when` above (Q-a inside it, H7 rider attached). It is the cheapest kill/confirm of the entire value premise and everything downstream — including the moat — depends on the vocabulary it produces.
2. **Promote the H1 DIRECTIONAL-PROBE as wfh-003, explicitly sequenced after wfh-002** (it consumes the vocabulary). Structure-only, kill criterion stated, no status move. T2 stays gated until this probe survives.
3. **Authorize the curator filing batch** (§2): 11 new nodes + 5 findings + 6 extensions, one batched pass. The findings (F1–F5), not the tool rows, are the compounding asset.
4. **Park the remaining six hypotheses** as routed. In particular: resist re-opening H8 — the scan is the strongest evidence yet that the deferral is correct — and record the two defer-and-record step-functions (§5) so they are not lost.

**Bottom line:** the scan validated the theme's control thesis, *narrowed* the claimed white space from "nobody shows this" to one precise unoccupied combination, and identified its weakest link (prospective+causal, Q-b). Spend accordingly: one build already queued, one cheap probe aimed at exactly that link, everything else parked.

---
*Advisory only. Graph writes are the curator's; promotion is the owner's. Nothing in this report moves status.*
