# wfh-001 Curator Filing Report

**Run:** wfh-001 · `theme:workflow-harness` · `agent_id: wfh-001-curator` · owner-approved (Issue #41)
**Idempotency check:** `context_lookup tags:["wfh-001"]` → zero prior nodes; clean slate, no skips.

## Extensions (reissued ids)

| Original | Reissued | Title | Change |
|---|---|---|---|
| #11 | **#134** | aider | + wfh-001 delivery/injection/control lens; tags `theme:workflow-harness`,`wfh-001` |
| #12 | **#135** | Claude Code (T3a) | + lens **+ dogfood-signal: `/context`+CC OTEL, four gaps** (hidden content · linear-not-graph · retrospective · CC-only); + `dogfood-signal` tag |
| #13 | **#136** | Continue | + lens + consolidation note (Cursor-acquired, repo read-only, no further spend) |
| #14 | **#137** | OpenHands | + lens (SecurityAnalyzer, Docker sandbox, no-markup) |
| #15 | **#138** | Goose | + lens (GooseModes/PromptManager, Recipes-as-artifact) |

All grades unchanged (`grade:claimed`); all incoming/outgoing edges carried/redirected by `context_correct` (some incoming skips = pre-existing invalid sources, per engine logs — not authored here).

## New nodes

| Action | Category | Title | Id | Tags (beyond `theme:workflow-harness`+`wfh-001`) | Edges |
|---|---|---|---|---|---|
| store | technology | Cursor | #139 | technology, harness, grade:claimed | — |
| store | technology | Windsurf/Cascade | #140 | ″ | — |
| store | technology | Devin | #141 | ″ | — |
| store | technology | Replit Agent 3 | #142 | ″ | — |
| store | technology | GitHub Copilot (agent mode + coding agent) | #143 | ″ | — |
| store | technology | Cline | #144 | ″ | — |
| store | technology | Factory.ai Droids | #145 | ″ | — |
| store | technology | Sourcegraph Amp | #146 | ″ | — |
| store | technology | Cannoli (LoggingEdge, Q-d design input) | #147 | technology, workflow-viz, grade:claimed | — |
| store | technology | Rivet | #148 | ″ | — |
| store | technology | LangGraph Studio | #149 | ″ | — |
| store | technology | Dify | #150 | ″ | — |
| store | technology | LangSmith | #151 | technology, observability, grade:claimed | — |
| store | technology | Langfuse | #152 | ″ | — |
| store | technology | Arize Phoenix (anti-pattern to beat) | #153 | ″ + anti-pattern | — |
| store | technology | W&B Weave | #154 | ″ | — |
| store | technology | OTel GenAI conventions (wire seam) | #155 | ″ + standard | — |
| store | finding | F1 — AGENTS.md de-facto standard | #156 | finding | Motivates → #170 |
| store | finding | F2 — enforcement-outside-the-LLM shipped/validated | #157 | finding | — |
| store | finding | F3 — market rewards no-markup/BYO/portable | #158 | finding | — |
| store | finding | F4 (fold) — mid-tier canvases/tracing = crowded | #159 | finding, fold | — |
| store | finding | F5 (fold) — general orchestration, no LLM-context concept | #160 | finding, fold | — |
| store | finding | H1 — probe → wfh-003 (sequenced) | #161 | finding, hypothesis | Motivates → #170 |
| store | finding | H2 — PARKED | #162 | finding, hypothesis, parked | none (parked) |
| store | finding | H3 — PARKED | #163 | ″ | none (parked) |
| store | finding | H4 — VALIDATED-BUILD → wfh-002 (+done_when +H7 rider) | #164 | finding, hypothesis | Motivates → #170 |
| store | finding | H5 — PARKED | #165 | finding, hypothesis, parked | none (parked) |
| store | finding | H6 — PARKED | #166 | ″ | none (parked) |
| store | finding | H7 — PARKED + wfh-002 rider | #167 | ″ | none (parked) |
| store | finding | H8 — PARKED | #168 | ″ | none (parked) |
| store | finding | **Position — white space PARTIAL; moat = the combination** | #169 | finding, position | Supports → #161, Supports → #164 |
| store | technology | JURATI typed operating-context ontology + prospective injection canvas (survivor line) | #170 | technology, grade:claimed | Prerequisite → #2 |
| store | factory | wfh-001 funnel telemetry | #171 | factory, telemetry | — |

## Totals

- **Nodes new:** 33 (technology 18 · finding 14 · factory 1) · **extended:** 5 (#134–#138)
- **Edges authored:** 6 — `Supports` 2 (#169→#161, #169→#164) · `Prerequisite` 1 (#170→#2) · `Motivates` 3 (#164→#170, #161→#170, #156→#170)
- **Grades:** all new nodes `grade:claimed` at store time (zero separate `context_tag` calls — rate limit untouched); **zero `proven` moves** (no artifacts this run)
- **Folded, not filed:** ~14 (Langflow/Flowise/n8n/Helicone/OpenLLMetry/Prompt Flow → F4 #159; Temporal/Windmill/Kestra/Prefect/Node-RED → F5 #160) · **do-not-file:** Obsidian class (Caret, Canvas LLM, SystemSculpt)
- **Skips (idempotency):** none · **Could-not-file:** none
