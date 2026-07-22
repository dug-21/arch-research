# wfh-001 · Scout Candidates

**Run:** wfh-001 · **Theme:** `theme:workflow-harness` · **Phase:** scan (T1 competitive landscape).
**Status:** structure-only, pre-triage (`claimed`-at-best, mechanism-level). Leader-persisted (OBS-7 — subagent
writes blocked). Not yet graph-formalized — curator writes happen after triage.

- **Partition A** (agent-harness delivery + context-injection + control + tenancy) — below, complete.
- **Partition B** (workflow-viz + "what-the-LLM-sees" UX) — raw builder survey captured below; scout's
  synthesis + observability-tool coverage (LangSmith/Langfuse/Phoenix/Weave/OTEL) + white-space verdict pending.

---

## Partition A — agent-harness delivery + context-injection + control + tenancy

**Source signal:** `external-scan` (all candidates) · **Agent:** wfh-001-scout-A
**Firewall (scout side):** comparables surveyed for *mechanism*, not graded technologies. In-lens: the theme
names coding-agent mechanisms as *reference implementations to generalize from*. None is a JURATI application
(that is the hypothesizer's step). Per lesson #18/L1: literature settles *mechanism*, not *completion/quality* —
so control/injection mechanisms are the verifiable layer; every performance/pricing figure is secondary-sourced
and flagged unverified.

### Reuse-first / dedup note

The `shd` goal already holds graded `technology` nodes for five of these tools, under a **different lens**
(local-backend tool-call viability — native `tool_calls` vs text/XML degradation), NOT
delivery/tenancy/context-injection/control:

| Existing node | id | Grade | Prior lens (do NOT re-surface as new) |
|---|---|---|---|
| aider — text-edit-format harness | #11 | claimed | edit-format contract |
| OpenHands — CodeAct native-function-calling | #14 | claimed | native-tool-call dependence |
| Goose — native tool-calls + XML fallback | #15 | claimed | toolshim/format-drift |
| Continue — XML system-message-tools | #13 | claimed | XML system-message tools |
| Claude Code via local /v1/messages shim (T3a) | #12 | claimed | local shim |
| Finding: local viability = harness↔proxy↔model contract | #16 | — | — |
| Lesson L1: mechanism searchable, completion not | #18 | — | — |

**Dedup verdict:** aider/OpenHands/Goose/Continue/Claude-Code are known nodes, but none is tagged
`theme:workflow-harness` and none carries delivery/tenancy/context-injection/control characterization — this
scan adds a genuinely new lens; the curator should **extend/tag, not duplicate**. **Cline** is mentioned in #16
(`cline #4362`) but has no own node → new. **Cursor, Windsurf, Devin, Replit, Copilot, Factory.ai, Amp** are
absent → new.

### Per-tool characterization

Columns map to axes: Delivery/exec-locus (A1/A3) · Context-injection mechanism + owner (core lens) · Out-of-LLM
enforcement (control lens) · Monetization (A7) · New/Known.

| Tool | Delivery / exec-locus (A1/A3) | Context injection — mechanism (owner) | Control: enforcement OUTSIDE the LLM | Monetization (A7) | New/Known |
|---|---|---|---|---|---|
| **Cursor** (Anysphere) | Local VS Code fork + vendor cloud VMs for Background Agents. Closed. | `.cursor/rules/*.mdc` w/ frontmatter (4 apply-modes) + `AGENTS.md` + `@`-providers; auto AST-chunk→vector RAG. User owns content, tool scaffolds+injects. | Diff accept/reject; cmd allow/deny-list; `permissions.json` sandbox+classifier subagent (3.6). Backlash: YOLO safeguards bypassable. | Seat $20–200 + usage credits. 2025 pricing apology/refunds. | New |
| **Windsurf/Cascade** (Cognition) | Local IDE fork + cloud inference; Enterprise on-prem/air-gap. Closed. | Global+workspace rules `.md` (char caps) + `AGENTS.md` + auto **Memories** (tool-owned); "Riptide" RAG. Hybrid owner. | 4-tier terminal gates (Disabled→Allowlist→Auto→Turbo), deny>allow, admin ceilings, dedicated shell. No FS sandbox found. | Seat + shifting credit/quota model. | New |
| **Devin** (Cognition) | Cloud SaaS, per-session isolated env (shell+editor+browser); Enterprise VPC + CLI. Closed. | **Knowledge** (auto from repo) + **Playbooks** (user task "system prompt" w/ guardrails); auto-ingests rivals' rule files incl. `AGENTS.md`,`CLAUDE.md`. Tool auto-onboards + user authors. | `request_scope` approval to leave initial dir; least-priv repo; PR review/merge gate; CI checks. | Usage-based Agent Compute Units (~15min/ACU), $20 entry. Skeptical reviews ~15% unattended completion. | New |
| **Replit Agent 3** | Cloud SaaS, browser IDE, code in Replit cloud; built-in DB/auth/deploy. Closed. | `replit.md`/`AGENTS.md` (static, re-read each session — not conversational memory); checkpoints snapshot files+memory+DB. User file + tool checkpoints. | App-testing toggle; Max-Autonomy opt-in; checkpoints + DB excluded from rollback by default (post-incident). Backlash: deleted prod DB during code freeze (Jul 2025). | Effort-based per-request; Core bundle. ~$100M+ ARR. | New |
| **GitHub Copilot** (agent mode + coding agent) | Hybrid: agent mode local in VS Code; coding agent in GitHub-hosted Actions ephemeral env. Closed SaaS. | `.github/copilot-instructions.md` + `.instructions.md` (glob) + `AGENTS.md` + `copilot-setup-steps.yml`. User hand-edits, committed. | **Strongest structural gates:** agent cannot mark own PR ready / approve / merge; pushes only to `copilot/` branch under branch protection; Actions need human "Approve and run"; firewall allowlist ON by default. | Usage-based AI Credits (from 2026-06-01), seat $0–39. Signups halted amid cost. | New |
| **OpenHands** | Open-core, MIT core. Local Docker GUI/CLI / Cloud SaaS; model-agnostic. | **Microagents/"skills"** (MD+YAML, 3 load-modes) + `AGENTS.md`/`CLAUDE.md`; community registry. User/community-authored, agent can auto-gen repo.md. | **Docker sandbox per session** + **ConfirmationPolicy + deterministic SecurityAnalyzer** (rates each call, gates independent of model). | Free OSS/BYO-key; Cloud at-cost inference, no markup; Enterprise source-available. ~80k★. | Known #14 (new lens) |
| **Claude Code** (Anthropic) | Local CLI + IDE/desktop/Slack/CI + cloud sessions. Proprietary. | **CLAUDE.md** (layered, auto-loaded) + `.claude/rules/` + **skills** (auto-described, self-invoked) + **subagents** + **hooks** + **MCP** + `settings.json` perms. User files, tool auto-injects; managed-policy client-enforced. | Per-tool eval **hooks→deny→allow→ask→mode**; permission modes; deny rules + protected paths hold even in bypass; OS sandbox (Seatbelt/bubblewrap). Docs: CLAUDE.md = "request not guarantee"; hooks = hard layer, "LLM never controls hooks." | Subscription (Pro/Max/Team) or API/BYO. | Known #12 (new lens) |
| **aider** | Fully local CLI, no SaaS. Apache-2.0. | Auto **repo-map** (tree-sitter + PageRank) + user `/add`/`/read` + `CONVENTIONS.md` + `.aider.conf.yml`. Hybrid: auto map + user-curated edit set. | Directed pair-programmer, not autonomous loop; git auto-commit + `/undo` (every edit reversible). | Free, BYO-key (or $0 local). | Known #11 (new lens) |
| **Cline** (VS Code/JetBrains + CLI/SDK) | Local IDE ext; inference remote. Apache-2.0 core. | `.clinerules/` (team+global, glob) + community **Memory Bank** + `@`-mentions + MCP Marketplace (1-click). User-owned, tool-injected. | **Plan mode read-only (extension-enforced, non-bypassable)** vs Act; per-tool Auto-Approve (~8 cats); every edit/cmd needs approval by default. | Free OSS/BYO-key or Cline credits; Teams $20/user. $32M Series A. | New (in #16, no node) |
| **Continue** (→ Cursor, Jun 2026) | Local IDE ext/CLI. Apache-2.0 (repo now read-only; Hub winding down). | Rules `.continue/rules/` (globs/regex/alwaysApply) + `@`-providers + deprecated `@codebase`. User or agent (`create_rule_block`). | Modes (Autocomplete/Chat/Edit/Agent/Plan); tool policy Ask-First/Automatic/Excluded; user applies/rejects. | Was Solo-free / Teams $20 / Hub. Acquired — consolidation. | Known #13 (new lens) |
| **Goose** (Block) | Local Desktop+CLI, on-machine. Apache-2.0. | `.goosehints` (hierarchical auto-load) + `AGENTS.md` + **Recipes** (portable YAML: prompt+extensions+params+sub-recipes) + subagents + MCP + Memory. User-authored, tool auto-injects. | 4 `GooseMode`s (Auto/Approve/SmartApprove/Chat) read by runtime **PromptManager at startup** (outside LLM); per-tool overrides. Caveat: SmartApprove read-classification is LLM-judged. | Free OSS, BYO-key, Block does not resell tokens. ~27k★. | Known #15 (new lens) |
| **Factory.ai** (Droids) | Hybrid: local CLI + SaaS control-plane + optional cloud "Droid Computers" (BYO compute, firewalled); on-prem/air-gap. Proprietary. | `AGENTS.md` + user memory (`.factory/memories.md`, `.factory/rules/`) + custom Droids (MD+YAML subagents) + MCP; agentic search + real-time indexing. Mostly user-edited + tool indexing. | **Tiered autonomy enforced outside model, fail-fast:** read-only→`--auto low/med/high`→skip; **violations return non-zero exit codes**; `droid exec` git-worktree isolation; `--mission` worker/validator. | Token-based ($20→$200) + BYOK; enterprise. $1.5B valuation (Apr 2026). | New |
| **Sourcegraph Amp** (Amp Inc.) | Local CLI + remote "orbs" (server-side threads). Pivoted CLI-only (killed IDE ext Mar 2026). Proprietary (inferred). | `AGENTS.md`(→`CLAUDE.md` fallback) + `@`-includes + glob rules + **Skills (`SKILL.md`)** + TS plugins `.amp/plugins/` + **Librarian subagent** (searches public+private GitHub) + MCP. User-authored + tool subagents. | Tool-perm rules `ask/reject/allow/delegate` (first-match); plugin handlers inject confirm/reject outside LLM; MCP needs `amp mcp approve`. By default does NOT ask before running tools. | Usage at API rates, no markup (50% only Enterprise); Amp Free (ad-funded, then changed). | New |

**Notable structural mechanisms (control lens — "enforcement outside the LLM context"):**
- **Copilot coding agent** — cleanest example of the thesis: the harness structurally forbids the agent from approving/merging its own PR and confines writes to a protected `copilot/` branch — enforcement in GitHub's permission system, not the prompt.
- **Claude Code hooks** and **OpenHands deterministic SecurityAnalyzer** — the two clearest "gate is a program, not a prompt" designs; both explicitly contrast rules-as-context (a *request*) with hooks/analyzers-as-enforcement (a *guarantee*).
- **Cline Plan-mode** and **Factory `--auto` tiers with non-zero exit on violation** — two ways to make a *mode* an out-of-LLM invariant.
- **Devin `request_scope`** — capability-gating by directory, approval-mediated — closest comparable to JURATI's per-agent capability gating.

### Synthesis (a) — mechanisms worth the hypothesizer's attention
1. **The rules-file convergence is real and vendor-neutral.** All 13 have a markdown rules mechanism, user-owned + tool-auto-injected, and **`AGENTS.md` is now a near-universal cross-tool standard** (Cursor/Windsurf/Devin/Replit/Copilot/OpenHands/Goose/Amp/Factory read it; Devin auto-ingests rivals' `.cursorrules`/`CLAUDE.md`). **Bears on H4:** the market de-facto standardized a *flat file* vocabulary — JURATI's typed-graph ontology must subsume it losslessly or fight it.
2. **Enforcement-outside-the-LLM is a solved, shipped pattern — the theme's core thesis validated by comparables.** Hooks (Claude Code), deterministic analyzers + Docker sandbox (OpenHands), branch/PR gates (Copilot), exit-code autonomy tiers (Factory), non-bypassable read-only mode (Cline). **Supports "harness drives, LLM serves" + H1/H2.**
3. **"Recipes/Playbooks/Skills as portable, versioned, committable workflow artifacts"** — Goose Recipes, Devin Playbooks, Amp/Claude-Code Skills. **Bears on H7 and P10/P12** — the "workflow-definition as serializable artifact" object is already in the wild.
4. **Subagents-as-isolated-context** (Claude Code, Goose, Factory Droids, Amp Librarian) — convergent. **Bears on the multi-agent shape of H1/H3.**
5. **Auto-generated-context-from-repo** (Devin Knowledge, OpenHands `repo.md`, Claude Code `/init`) is the day-one-provisioning primitive (**A6**). **Bears on "day-one value = A2+A6."**
6. **Token-margin is NOT the winning monetization signal** — tools that advertise trust (OpenHands/Amp "no markup", Goose "Block does not resell tokens", BYO-key) treat *not* taking margin as a feature. **Relevant to A4/A7 and seam #5.**

### Synthesis (b) — delivery/tenancy lessons mapped to P1–P14
- **P1/P2/P13 (hosted/multi-tenant):** market **punished** hosted-only, non-portable, surprise-priced moves — Cursor (Jul 2025 apology+refunds), Copilot (signups halted, 10×–50× cost jumps), Replit (deleted a prod DB), Devin (~15%-completion skepticism). Corroborates the delivery-doc's "high sovereignty strain" for P1.
- **Licensing (P4/P5/P8/P11):** BSL/SSPL is a repeated own-goal — HashiCorp→BUSL spawned OpenTofu (CNCF); Redis→SSPL spawned Valkey then re-added AGPL; Elastic re-added AGPL. Market rewards *self-hostability + portability + realistic exit*; source-available-with-teeth reliably triggers a fork. Sentry's **FSL** (2-yr delayed-open, non-compete) is the current "least-hated" middle path. **Reinforces seam #4.**
- **P4/P10 (local-first credibility anchor):** aider (pure-local Apache-2.0, BYO-key) and Goose (local, no token resale) are the trust-credible end, near-zero backlash. The whole landscape has an `AGENTS.md`/git-committed-rules convention P10 plugs straight into.
- **P3 (split control-plane/local exec) is an emerging real topology:** Factory (SaaS control-plane + local CLI + optional BYO cloud) and Copilot (local agent-mode + hosted coding-agent) both ship it — evidence P3 is buildable and accepted.
- **A7 monetization reality:** industry moved en masse to usage/token/credit billing in 2025–26 — nearly every transition drew backlash for opacity; reward went to transparent pass-through / no-markup / BYO-key. Sharpens seams #5/#7.
- **Consolidation risk (P5/P12):** Continue acquired by Cursor (repo read-only, Hub deleted); Cognition owns both Devin and Windsurf. A workflow-artifact ecosystem on a single vendor's registry inherits that vendor's M&A risk — argues for the **registry-neutral** end of P12 (npm/OCI + sigstore) over a vendor registry.

### Flags for triage
- Everything is `claimed`-at-best and mechanism-level (lesson #18/L1). All performance/adoption/pricing numbers are secondary-sourced and unverified (star counts, ARR, ACU rates, exact tiers).
- **Curator action (post-triage):** extend/tag the five `shd` nodes (#11–#15, +#12) with `theme:workflow-harness` under the new lens — do not duplicate. File the eight net-new tools (Cursor, Windsurf, Devin, Replit, Copilot, Cline, Factory.ai, Amp) as new `technology` `grade:claimed`, tagged `theme:workflow-harness` + `wfh-001`, source `external-scan`.
- **Cross-partition:** Copilot branch/PR gate + Devin `request_scope` are the closest external analogues to JURATI's per-agent capability gating (issue #12 / ass-100/101).

**Return summary:** 13 candidates in-lens. New (8): Cursor, Windsurf, Devin, Replit, GitHub Copilot, Cline, Factory.ai, Sourcegraph Amp. Known/new-lens (5): aider #11, OpenHands #14, Goose #15, Continue #13, Claude Code #12 (+ finding #16, lesson #18).

---

## Partition B — workflow-viz + "what-the-LLM-sees" UX

**Status:** COMPLETE — Scout B synthesis below (white-space verdict + observability tier + best-ideas),
followed by **Appendix B1** (citation-complete builder survey from the sub-agent Scout B spawned, which
fills the confidence gap Scout B flagged on the builder rows). Source signal: `external-scan` (+ Claude Code
`/context` = `dogfood-signal`).

**Dedup (reuse-first).** Unimatrix has coding-agent *execution harness* nodes only (#11–#15, `theme:shd`)
and **zero** workflow-visualization or agent-observability nodes — all Partition B candidates are net-new.

### 1. Per-tool characterization

**Sub-lens A — workflow / agent builders & canvases** *(the question that matters: Q3 — does the canvas show
the resolved context the model received, or only static node config?)*

| Tool | Representation | Live exec state | Q3: resolved "what-the-LLM-saw" on the structure | Tokens / errors |
|---|---|---|---|---|
| **Cannoli** (Obsidian) ⭐ | Native `.canvas` DAG executes directly | Yes — node recolors by status, output streams into node | **Strongest OSS** — a `LoggingEdge` dumps the exact `request.messages` array (role-labeled + function-call JSON) **+ config block** onto a canvas node; upstream cards *are* the injected context (source-verified) | Errors → red error node wired to failure. Cost: pre-run estimate only, no live badge |
| **Rivet** (Ironclad) | Node-graph LLM editor | Yes — node-level execution | Yes — prompt/message nodes render the assembled prompt; most prompt-transparent commercial builder | Per-node data incl. tokens; cost aggregate, not live per-node badge |
| **MS Prompt Flow** | Authored DAG | Yes — per-node output in trace pane | Yes but *beside* the graph — resolved prompt in a trace panel, not on the node | Per-node tokens/cost/errors in trace pane |
| **LangGraph Studio** | Renders LangGraph state-graph; step/time-travel | Strong — step, inspect/fork state, time-travel | Partial→yes — shows accumulated state/messages per node; resolved LLM input via LangSmith Trace Mode | Tokens/cost/errors via LangSmith (0-token bug on long runs) |
| **Dify** | Visual canvas (OSS) | Yes — node run status | Partial — node config + I/O; leads remaining OSS canvases; full-context-per-call not confirmed | Node logs; per-step token/cost not confirmed |
| **Langflow / Flowise** | Drag-drop canvas | Partial — output panel | Partial — component I/O, not "exact messages sent" | Basic token/error in logs, not on nodes |
| **n8n** | Automation node-graph | Yes — per-node I/O JSON | **No** for LLM-context — node I/O JSON, not a resolved-prompt view | Log errors yes; LLM token cost not first-class |
| **Temporal / Windmill / Kestra / Prefect / Node-RED** | Orchestration timelines / DAGs | Yes — task/run state | **No** — general orchestration; no "what the LLM saw" concept | Task errors/retries; no LLM token/cost |

*Obsidian class also surveyed: Caret (abandoned), Canvas LLM (own graph, not native canvas), SystemSculpt AI (proprietary, transparency unverified) — none confirmed for prompt-transparency. Cannoli is the standout.*

**Sub-lens B — agent observability / tracing** *(Q2: does it show what the LLM saw? Q3: mapped onto a navigable workflow structure, or a flat run list?)*

| Tool | Metaphor | Q2: what the LLM saw | Q3: mapped onto navigable structure? | Tokens/errors · replay |
|---|---|---|---|---|
| **LangSmith** | Span waterfall + run tree; beta agent-graph | **Most faithful** — exact inputs/messages/tools/model config; Playground loads them | Partial (best of tracing) — thread + beta LangGraph graph + Studio Trace Mode; graph is LangGraph-specific, per-run | Per-child token+cost; edit+replay yes |
| **Arize Phoenix** | Waterfall + node **Agent Graph** | Yes — OpenInference spans embed messages, system prompt, retrieved docs, tool calls | **Closest to a graph** — but *derived per-run* from span parenting, not an authored reusable canvas | Per-span tokens/cost/errors; replay yes |
| **Langfuse** | Nested tree; beta LangGraph graph | Yes — full prompt, completion, model, tokens, latency, cost | Partial — sessions group traces; beta graph LangGraph-specific | Per-gen tokens+cost; replay yes |
| **W&B Weave** | Trace tree + chat view | Yes — auto-logs I/O; renders resolved messages | No reusable graph — per-run tree only | Tokens+cost; strongest edit+replay |
| **Helicone** | Request log + Sessions | Yes at request level — full request/response bodies | No — sessions grouping, no graph | Error filter; replay yes |
| **OpenLLMetry** (Traceloop) | Span waterfall (library) | Partial — captures prompts/responses as `gen_ai.*` attrs | No — per-run waterfall | Strong cost; span-status errors; no replay |
| **OTel GenAI conventions** | Spec, no UI | **Defined but OPT-IN/off by default** — `gen_ai.input.messages`, `.system_instructions`, `.tool.definitions` PII-flagged; no prompt content by default | No — spans parent/child only | Token counts; no cost attr; `error.type` |
| **Claude Code OTEL** (dogfood) | Metrics + events export | **Counts + metadata only by default; content REDACTED.** Prompt only under `OTEL_LOG_USER_PROMPTS`; full model-visible context only under `OTEL_LOG_RAW_API_BODIES` | No — has `workflow.run_id` attrs but no graph | `token.usage`, `cost.usage` (USD), edit-tool decisions; error/refusal events |

**The sharpest adjacency — Claude Code `/context` (dogfood-signal, nearest the owner's claim).** It ships an
interactive context-window visualization: every loaded block on a timeline, **sized by tokens**, tagged by
source (`System prompt`, `Auto memory`, `Skill descriptions`, `Project CLAUDE.md`, live `Read`/`grep`/path-scoped
`Rule:` blocks). **But precisely what it does NOT do is the crux:** (1) verbatim content is **hidden** (system
prompt annotated "you never see it"; skills/rules show label+size+prose, not the injected text); (2) it's a
**linear timeline of one session's cumulative fill**, not a navigable canvas of skills/agent-defs/gates as
reusable structure; (3) it's **retrospective** ("what loaded"), not **prospective** ("what will be injected
next, and why"); (4) it's **Claude-Code-specific**, not build-once/any-LLM.

### 2. Best UX ideas to pull into JURATI
1. **Cannoli's `LoggingEdge`, promoted to the primary view** — dump the exact role-labeled message array + model/param config onto the canvas node, so the canvas *is* the resolved-context graph. JURATI's live-debugger = this made first-class, prospective, queen-driven.
2. **Live node-status coloring + on-canvas error nodes** (Cannoli) — pending→executing→complete recoloring + a red error node wired to the failing step. Serves H2.
3. **Faithful edit-and-replay from a step** (LangSmith/Weave/Phoenix Playground) — "open this exact context, edit, re-run." For JURATI: "here's what the LLM got at gate X; change the injection, re-run the step."
4. **`/context`'s token-sized, source-tagged breakdown — but fix its two gaps:** show the **verbatim** injected content (CC hides it) and make it **prospective** (what's about to be injected, and why).
5. **Phoenix's derived agent-graph is the anti-pattern to beat** — everyone reconstructs the graph per-run from span parenting; JURATI's differentiator is an **authored, durable** graph a run *lights up*.
6. **OTel GenAI attribute vocabulary as the wire seam** (`gen_ai.system_instructions`, `.tool.definitions`, `.input.messages`) — adopting these names keeps telemetry portable/any-LLM; note they're opt-in/PII-flagged, so JURATI owns the capture decision the ecosystem defers.

### 3. White-space verdict — **PARTIAL** (real in combination; crowded component-by-component)

**Where the claim is WRONG / crowded:**
- "Show the exact context the LLM was given, per step" is **solved and crowded** — LangSmith, Langfuse, Phoenix, Weave, Helicone, Cannoli all render resolved messages/system-prompt/tool-defs. Pitch *this alone* → "LangSmith already does that."
- "On a workflow graph" is **partially occupied** — Phoenix, LangGraph Studio, Cannoli, Rivet map LLM I/O onto nodes.
- "Per-step token cost + errors" is **commoditized** (table-stakes). (Narrow gap: no tool paints a live per-node dollar/token badge *during* a run — minor, not a thesis.)

**Where the claim is RIGHT (genuine, defensible white space) — the combination nobody hits:**
1. **Subject = a *coding-agent's operating context* (skills / agent-defs / gates) as the first-class object.** Everyone traces *an app's LLM calls*; none models *this coding agent's* skills/subagents/gates as the navigable structure. `/context` tags them by size but hides content and isn't a graph; Cannoli/Rivet model *a workflow you authored*, not an agent-harness's operating context.
2. **Prospective + causal — "what is injected NEXT, and *why*."** Every surveyed tool is **retrospective** (a trace of what already happened). None shows the *forthcoming* injection as a control-plane decision with its rationale (which gate fired, which skill matched). This is the H1 "queen coordinates *and* is the live debugger" thesis.
3. **Authored + durable, not per-run-derived.** Existing graphs are reconstructed from one run's span parenting; JURATI's is a stable, versioned, authored operating-context graph a run illuminates (H4/H7).
4. **Harness-as-driver, any-LLM-pluggable.** All observers sit *beside* the LLM app and watch; JURATI inverts it — harness drives, LLM is a directed component, canvas renders the harness's control decisions. No analog in the set.

**Net:** differentiator is **real but must be stated precisely** — NOT "show what the LLM saw + token cost on
a graph" (crowded), but "a **live-debugger canvas of a coding-agent's operating context (skills/agent-defs/gates)
where the harness drives the run and shows what it's about to inject next and why** — authored / durable /
any-LLM." Components 1+2+4 in combination are **unoccupied**. **Honest risk:** the moat is the *control-plane
framing + coding-agent-context ontology*, not the visualization — a fast-follower (Cannoli-style OSS; LangGraph
Studio adding a "why this context" pane) could close the prospective gap, since the retrospective+resolved-context
substrate is everywhere.

**Scout flags:** observability tier + Obsidian class + `/context` are source-verified; several builder rows are
lower-confidence synthesis — Appendix B1 (below) is the citation-complete builder sub-survey that resolves it.
All rows net-new `technology` `grade:claimed`, tag `theme:workflow-harness` + `wfh-001`. Not graded/judged — that's triage.

### Appendix B1 — builder survey (citation-complete)
Per-tool, four questions: **Q1** visual representation · **Q2** live execution state · **Q3** resolved
context-per-step · **Q4** per-step token cost + errors.

- **LangGraph Studio** — Q1: true node-graph of the agent (nodes=functions/LLM calls, edges, shared State). Q2: yes — nodes traversed + intermediate states stream; interrupts/breakpoints + time-travel to any checkpoint. Q3: strong but indirect — State holds the `messages` list (viewable/editable per checkpoint); verbatim resolved prompt/IO lives in the attached LangSmith trace panel, not on the node. Q4: yes — per-step status/latency/tokens; LangSmith trace tree breaks down token/cost per run + marks errors.
- **Rivet** (Ironclad) — Q1: node-graph visual programming; Text/Prompt→Assemble Prompt→Chat wired explicitly. Q2: yes — "live debugging of AI chains as they run," input/output of every node + AI responses streamed in real-time. Q3: **best-in-class + structural** — Assemble Prompt node outputs the single combined message array, inspectable inline on the canvas after a run (not static config). Q4: weak — Chat node documents only `Response`; no per-node token/cost port; errors via live debugger, no per-node badge.
- **Langflow** — Q1: node-graph builder. Q2: partial — Playground real-time; per-component Inspect + Traces in a side pane, not overlaid live; active-node highlight unconfirmed. Q3: partial — Message Logs + Inspect + trace spans (model, tokens); verbatim prompt-as-sent on the node unconfirmed. Q4: yes in Trace Details pane (tokens, timing, errors per span); no currency cost native.
- **Flowise** — Q1: node-graph canvas (Chatflow/AgentFlow V2). Q2: weak natively; detailed step traces mainly via external Langfuse/LangSmith. Q3: not native to canvas — resolved messages via external LangSmith/Langfuse. Q4: not native to canvas — per-step token/cost via LangSmith/Langfuse; native Analytics gives node-level observability.
- **n8n** — Q1: node-graph editor; AI sub-nodes attach beneath a root AI Agent node; JSON dataflow. Q2: yes — green/red per node on canvas; past executions inspectable; live "running" animation inconsistent per community. Q3: partial — double-click a node post-run shows full actual input/output JSON, but the composed prompt string isn't cleanly broken out and token usage isn't in-workflow. Q4: errors yes (red icon); token cost NOT native — needs community nodes.
- **Dify** — Q1: node-based canvas (typed nodes). Q2: yes — node-by-node trace with tokens/latency; Variable Inspect shows all variable contents in real time; each node auto-saves last-run IO. Q3: **strongest OSS canvas** — single-step / "Last run" on an LLM node shows resolved inputs/outputs/metadata; Variable Inspect exposes resolved upstream variables; whole final message-list-as-one-payload only partially confirmed. Q4: yes — per-node tokens, latency, status, error messages.
- **Microsoft Prompt Flow** — Q1: DAG (flatten editor + read-only Graph view). Q2: yes — run status, single-node/full-flow runs, per-node Outputs, "Bypassed" status. Q3: **confirmed yes** — Jinja templates resolve at runtime; Trace tab shows span-tree with per-node input/output (the resolved prompt/messages). Caveat: tracing off by default. Q4: yes — per-node duration + token cost + status/errors (strongest native per-node token surfacing among general builders). Caveat: on retirement path (Apr 2027).
- **Temporal** (Web UI) — Q1: event-history timeline, not an authored canvas. Q2: yes — live timeline + Pending Activities. Q3: no LLM/prompt view; per-activity Input/Results shows a prompt only as generic payload. Q4: no token cost (Cloud "Billable Actions" only); failures per event.
- **Windmill** — Q1: true DAG canvas of code steps. Q2: yes — "Test flow" previews the DAG live with per-step status/results/logs. Q3: no LLM view; prompt-as-input shows as generic payload. Q4: no token cost; per-step errors in run view.
- **Kestra** — Q1: YAML-first + auto Topology graph + Gantt. Q2: yes — real-time task status/logs. Q3: no LLM view; generic payloads. Q4: no token cost; failed tasks marked, per-task logs, replay.
- **Prefect** — Q1: code-first; auto flow-run graph/DAG + timeline. Q2: yes — real-time state. Q3: no LLM view; per-task input args in UI is an open feature request (#11301) — weaker than peers. Q4: no token cost; Failed/Crashed states + logs.
- **Node-RED** — Q1: flow/wiring diagram. Q2: partial/indirect — no built-in active-node highlight; status dot via `node.status()`; message contents via wired Debug nodes in a sidebar. Q3: no inline-on-canvas view — nodes show static config; composed message only via a wired Debug node to the sidebar. Q4: no native token/cost; errors via wired Catch node / red status dot.

**Cross-set caveat (scout):** several Q3 "verbatim prompt exactly as sent" and some Q2 live-highlight
specifics (Langflow, Flowise, Dify single-payload rendering) are documented-but-not-screenshot-confirmed —
would need hands-on UI verification.

*(Superseded — see §3 White-space verdict above: **PARTIAL**. Scout B confirmed the domain gap and sharpened
it to the unoccupied combination of subject + prospective/causal + authored-durable + harness-as-driver.)*
</content>
