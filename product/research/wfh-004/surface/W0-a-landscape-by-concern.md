# W0-a — The shipped landscape, re-cut by concern

**Run:** wfh-004 · Issue #48 · phase `scan` · `agent_id: wfh-004-w0a` · read-only, zero graph writes.
**Evidence base:** `product/research/wfh-001/scout-candidates.md` (~30 tools, two lenses), `wfh-001/reports/{triage,formalization}.md`, Unimatrix `#134`–`#171` (`grade:claimed`), `wfh-002/FINDINGS-W1` (`gate`/`skill`/`agent-def` provenance rows), `#183`.
**Nothing here was re-scanned.** This is a re-projection of held evidence onto the §3.1 concern axis.

Tools are grouped into five families. The family is defined by **where the work-shape lives**, which turns out to predict every other cell.

- **A · Local coding-agent harness** — aider #134, Continue #136, Goose #138, Claude Code #135, Cursor #139, Windsurf #140, Cline #144
- **B · Platform-gated agent** — GitHub Copilot #143, Devin #141, Replit Agent 3 #142, Factory.ai #145, OpenHands #137, Amp #146
- **C · Authored workflow canvas** — Cannoli #147, Rivet #148, LangGraph Studio #149, Dify #150 (+ Langflow/Flowise/n8n, folded #159)
- **D · LLM observability** — LangSmith #151, Langfuse #152, Phoenix #153, Weave #154, OTel GenAI #155, CC OTEL #135 (+ Helicone/OpenLLMetry, folded #159)
- **E · Durable orchestration** — Temporal, Windmill, Kestra, Prefect, Node-RED (folded #160)

## 1. The matrix

| | **Structure** | **Context provisioning** | **Security** | **Introspection** | **Cost** | **Self-improvement** | **Recovery** | **Human steering** |
|---|---|---|---|---|---|---|---|---|
| **A · Local harness** | names reusable task artifacts (Goose Recipes w/ sub-recipes, CC skills+subagents); no addressable steps or dependencies | loads markdown rules by always/glob/agent-choice at turn start; Windsurf + CC auto-memory write notes back | evaluates every tool call against user-authored deny→allow→ask rules before it runs; Cline's read-only Plan mode is enforced by the extension | prints the diff/command before running it; CC `/context` lists loaded blocks sized by tokens but **hides their verbatim text** | shows a cumulative session token/dollar total; CC exports `cost.usage` over OTEL | — (memory accumulates notes; no outcome is attributed to a config) | aider auto-commits each edit and `/undo` reverts it; otherwise a killed session loses in-flight work | blocks per tool call / per diff for approve-or-deny; a *new instruction* enters only by interrupting the turn |
| **B · Platform-gated** | Devin Playbooks / Factory `--mission` worker-validator name a task shape + role split; execution is still one agent stream | ingests the repo into a knowledge store at onboarding (Devin Knowledge, OpenHands `repo.md`) and re-reads a committed rules file per session | **strongest shipped**: Copilot refuses the agent approval/merge of its own PR and confines writes to a protected branch; OpenHands rates each action with a deterministic analyzer inside a per-session Docker sandbox; Factory exits non-zero on tier violation; Devin `request_scope` blocks leaving its start directory | streams a live shell/editor/browser a human can watch; Copilot leaves a PR diff as the durable record | meters vendor units (Devin ACU ≈ 15 min) and bills them; the unit is wall-clock, not a work step | — | Replit snapshots files+memory+DB per checkpoint and rolls back to one; Factory isolates each run in a git worktree | gates at the PR and at scope-escalation requests; Devin asks mid-run to widen its own scope |
| **C · Authored canvas** | **strongest shipped**: the work IS a durable authored graph of typed nodes/edges that the run executes; it outlives the run | Cannoli's `LoggingEdge` writes the exact role-labeled `request.messages` array + model config onto a node; Rivet's Assemble Prompt emits the combined array inline | — (assumes the author is trusted; runs whatever the graph says) | recolors each node by status and streams output into it; wires failures to a red error node; LangGraph steps, forks state, time-travels | Dify shows per-node tokens/latency/status; no live per-node dollar badge during a run | — | LangGraph checkpoints state per node and resumes or forks from it | **LangGraph interrupts at a breakpoint, lets a human edit state, then resumes** — the closest shipped thing to correction |
| **D · Observability** | reconstructs a call tree per run from span parenting; the structure is derived and dies with the run (#153, the named anti-pattern) | records the exact messages, system prompt, tool definitions and retrieved docs per call and reloads them into a playground | — (OTel ships prompt content off-by-default and PII-flagged — a privacy control, not an authority control) | **strongest shipped**: a durable, queryable waterfall of every call with inputs, outputs, latency and errors | attributes tokens + dollars to each span and rolls up per trace/session/user | dataset-replay + evaluator scoring exists in this tier — **outside wfh-001's evidence, see §5** | — (observes; when the observed run dies, the trace just ends) | edit-and-replay a *recorded* call after the fact (Weave strongest); nothing enters a live run |
| **E · Durable orchestration** | names every task, its dependencies and its retry policy as a definition the engine owns | — (passes payloads; has no concept of what a model was shown) | not characterized in our evidence | renders a live event-history timeline with per-task state/logs; the history *is* the audit record | — (counts billable actions, not model spend) | — | **strongest shipped**: persists the event history so a crashed worker's run resumes from the last completed event, on another machine | signals deliver external messages into a running workflow — **outside wfh-001's evidence, see §5** |

## 2. Per concern

### Structure
**State of the art:** family C. A Cannoli `.canvas` file or a LangGraph state-graph is a durable, authored, re-runnable object; the run *lights it up* rather than creating it. Family E does the same for non-LLM tasks and adds declared dependencies and retry policy. Mechanism: the definition is a serialized artifact the engine reads, not a transcript the engine emits.
**Common denominator:** a markdown rules-file plus, increasingly, named sub-agents and a portable task artifact (Recipes, Playbooks, Skills). `AGENTS.md` is read by nine of the scanned tools (#156). This is a *vocabulary* convergence, not a structure one — a flat file has no addressable units.
**Nobody ships:** a durable authored structure for **a coding agent's own operating context** — its roles, gates, skills and steps — that the run then executes. C authors *an application's* workflow; A/B author *prompts for one agent*. Confidence this is a real absence: **high** — it is wfh-001's central verdict (#169) and survived a second look.

### Context provisioning
**State of the art:** Cannoli `LoggingEdge` (#147) — the exact message array plus model/param config is deposited onto a canvas node, so the graph *is* the resolved-context record. Rivet's Assemble Prompt is the same idea as a first-class node. LangSmith (#151) captures the same fidelity retrospectively.
**Common denominator:** committed markdown, injected by the tool, with a load-mode enum (Cursor ships four apply-modes; OpenHands microagents span always-loaded to keyword-triggered). Every tool treats rules-as-context as a *request*.
**Nobody ships:** a statement of what is **about to be** injected and **why** — which rule matched, which gate fired, what was excluded and on what basis. Every surveyed tool is retrospective. Claude Code `/context` is the nearest and fails three ways: hidden verbatim content, linear-timeline-not-graph, retrospective (#135). Confidence: **high** — this was the specific gap wfh-001 was hunting and it looked hard.

### Security
**State of the art:** GitHub Copilot's coding agent (#143). The agent structurally cannot approve or merge its own PR and can push only to a protected branch — enforcement in GitHub's permission system, a plane the agent holds no credentials for. That is C-4 in the wild: an incapacity, not a gradient. Runner-up: OpenHands (#137) — a deterministic analyzer rates every action inside a per-session Docker sandbox.
**Common denominator:** a per-tool-call allow/deny/ask matcher evaluated in the runtime before execution, plus an autonomy mode. Universally understood as separate from the prompt — "the LLM never controls hooks" (#157/F2).
**Nobody ships:** authority bound to a **role within a step**. Every shipped gate matches on a *tool name*, a *path*, or a *VCS action* — never on "this agent, at this step, may call this tool." Also absent: any shipped defense against instructions arriving through data, in any of the ~30 tools. Confidence: **medium-high** on role×step (wfh-001's control lens was thorough); **medium** on prompt-injection (the scan did not ask the question directly).

### Introspection
**State of the art:** family D. LangSmith/Langfuse/Phoenix/Weave retain a per-call waterfall with verbatim inputs, outputs, latency and errors, durably and queryably, and reload any call into a playground.
**Common denominator:** per-step I/O visible somewhere, plus errors. Commoditized (#159).
**Nobody ships:** a **causal** account — not "node B ran after node A" but "B ran *because* gate G returned deny." Structure is derived from span parenting (#153) so it exists only per-run and cannot be compared across runs. Confidence: **high** for the causal absence; the derived-structure claim is directly evidenced.
**Honest counter:** retrospective resolved-context capture is *solved*. Wanting it is wanting LangSmith.

### Cost transparency & management
**State of the art:** family D attributes tokens and dollars to individual spans and rolls up per trace/session/user. Claude Code exports `token.usage` and `cost.usage` (USD) over OTEL.
**Common denominator:** a session total, and per-call token counts wherever tracing exists.
**Nobody ships:** **enforcement.** Nothing in our evidence stops a run because a named unit of work exceeded a budget. Vendor units (ACUs, credits) meter *compute time*, not work steps; the only shipped stop is the billing cap. Also absent: any prediction of a run's cost before it starts. Confidence: **medium** — wfh-001's cost axis was "per-step tokens/errors visible?" (Q4) and "monetization" (A7); it never asked "can you cap a step?" This may be an absence in our evidence.

### Self-improvement
**State of the art:** in our evidence, **nothing**. No tool in wfh-001 was characterized as attributing an outcome to a configuration, or as comparing two configurations on evidence.
**Common denominator:** nothing.
**Nobody ships:** confidence **low that this is a real absence.** wfh-001 never asked. Dataset-replay + evaluator scoring is a known feature area of the D tier and would partially populate this cell; see §5. What I can say with confidence is *why* the cell is structurally hard for the field: outcome attribution requires stable units to attribute to, and D derives its units per-run. **This is the one cell where "we don't know" is the honest answer, and it should be flagged to triage as a scan gap rather than a white space.**

### Recovery / durability
**State of the art:** family E, decisively. Temporal event-sources the workflow so a crashed worker's run resumes from the last completed event on another machine; retries and compensations are declared. LangGraph brings the same idea (a pluggable checkpointer) into the LLM world. Replit snapshots files+memory+DB.
**Common denominator:** in the agent families (A/B) — essentially nothing. aider's git auto-commit and Replit's checkpoints are the only shipped recovery, and both are *rollback*, not *resume*. A dead agent session is lost work.
**Nobody ships:** detection and resumption of a dead **agent** — the E-tier guarantee applied to LLM work. Confidence: **medium-high**. The absence in A/B is well-evidenced; whether an agent-native durable-execution product now exists was outside wfh-001's lens.
**Honest counter:** durable execution as a *mechanism* is a solved, mature discipline. The gap is that nobody has connected it to agents — not that the primitive needs inventing.

### Human steering
**State of the art:** LangGraph Studio (#149) — interrupt at a breakpoint, *edit the accumulated state*, resume. That is correction, not approval. Devin's `request_scope` is the other shape: the agent asks mid-run and a human widens its authority.
**Common denominator:** approve-or-deny, per tool call or per PR. A binary on an action the agent already chose.
**Nobody ships:** **redirection** — new intent entering a running unit of work and changing what it does next, without stopping it. Everything shipped is a veto or an interrupt-and-restart. Confidence: **medium-high**; Temporal signals are the mechanism-level counterexample and are outside our evidence (§5).

## 3. Cross-concern observations

**The field's fault line is who owns the work-shape, and it predicts everything else.** Families C and E own a durable definition and get introspection, recovery and steering comparatively cheaply. Families A and B own no definition and pay downstream in every concern: cost is a session total, recovery is start-over, steering is approve/deny. This is SCOPE §3.2's layering claim observed from the outside — and it is corroborated by a *negative*: D has the field's best introspection and its worst self-improvement, because its units are derived per-run and therefore not comparable across runs.

**Security and structure are anti-correlated in what ships.** The strongest security (B) comes from the family with the weakest work-structure, because enforcement was bought by pushing it into a platform — git, Docker, an exit code — that knows nothing about the agent's steps. Consequence: no shipped gate can express "this role, at this step." The strongest structure (C) ships *zero* security, because a canvas assumes a trusted author.

**Introspection is coupled to structure backwards.** The field derives the graph from the trace. Nobody lights up an authored graph with a trace (#153 filed as the anti-pattern).

**Single-concern point solutions:** Cannoli (context provisioning), Helicone/OpenLLMetry (introspection), OTel GenAI (a vocabulary, not a tool). **Multi-concern platforms:** Claude Code, OpenHands, Factory, LangSmith. **Nothing spans all eight.** The widest is Claude Code — six concerns touched, self-improvement and recovery entirely empty.

**Strength bought with weakness, named:** Copilot's structural security costs steering latency (everything routes through PR review — no mid-run correction exists). Devin's autonomy costs introspection (you watch a screen; you do not get a record). C's structure costs all security. D's introspection fidelity is bought by sitting *beside* the run — it can explain anything and prevent nothing.

## 4. Substrate notes

- **Claude Code (#135):** flat markdown + a `settings.json` matcher table. Hooks are shell commands the CLI process runs; permission rules are matched in the runtime *before* the tool executes; sandboxing is OS-level (Seatbelt/bubblewrap). Enforcement locus: runtime + OS. The vendor's own docs draw the line — CLAUDE.md is "a request, not a guarantee." **No graph anywhere.**
- **GitHub Copilot (#143):** enforcement lives in GitHub's permission system and branch protection — a plane outside the agent's credentials entirely. The only shipped instance of authority the agent cannot reach.
- **OpenHands (#137):** open-core, self-hostable; per-session Docker; the SecurityAnalyzer is a deterministic program, not a model. Microagents are markdown+YAML with three load-modes.
- **Factory.ai (#145):** SaaS control plane + local CLI; autonomy tier is a process flag and violations surface as a **non-zero exit code** — enforcement at the process boundary, legible to CI.
- **Cannoli (#147):** an Obsidian `.canvas` JSON file *is* the program; local, no server. `LoggingEdge` is a **node type** — transparency is authored into the graph, not provided by the tool. Self-host by construction.
- **LangGraph/LangSmith (#149/#151):** code-first (Python/TS graph objects); the checkpointer is a pluggable persistence layer — that is the recovery mechanism. Studio renders what code declares. LangSmith is hosted (enterprise self-host).
- **Phoenix / OTel GenAI (#153/#155):** OTLP spans; structure is span parent/child, entirely derived; vendor-neutral, self-hostable. Prompt-content attributes are opt-in and PII-flagged — the ecosystem defers the capture decision to the operator.
- **Temporal (#160):** event-sourced durable execution — workflow state is a replayable event history in a database. The price is a determinism constraint on workflow code. Self-host or cloud.
- **Cursor / Windsurf / Devin / Replit (#139–#142):** closed, hosted, substrate not inspectable. Everything we hold is vendor documentation.

## 5. Evidence quality flags

1. **All wfh-001 nodes are `grade:claimed`, mechanism-level, from vendor docs and secondary sources.** Nothing in this matrix except the Claude Code cells was demonstrated by us. Do not launder any cell into fact.
2. **The only `[demonstrated]` evidence in this re-cut** is Claude Code's `/context` behaviour and this repo's `settings.json` hook/permission surface (dogfood-signal on #135; wfh-002 W1/W2 mark those rows demonstrated). Everything else is doc-claim.
3. **wfh-001's scan axes did not include cost *management*, self-improvement, or recovery.** Its axes were delivery/exec-locus, context-injection mechanism, out-of-LLM enforcement, monetization (Partition A) and representation/live-state/resolved-context/tokens-errors (Partition B). The "nobody ships" verdicts for **Cost enforcement, Self-improvement and Recovery are therefore weakest** — they are absences in our evidence, not demonstrated absences in the world. Triage should treat any candidate resting on them as `needs-a-probe`, and the cheapest probe is a scan, not a build.
4. **Three claims injected from outside wfh-001's evidence, flagged as unverified in this run:** (a) dataset-replay + evaluator scoring in the LangSmith/Langfuse/Phoenix tier — would partially populate the Self-improvement cell; (b) Temporal **signals** as shipped mid-run intent injection — a direct counterexample to the Human-steering gap; (c) Temporal namespace RBAC. None is graph-backed. Each is a named target for a cheap confirming scan.
5. **The scout's own caveat carries forward:** several Q3 "verbatim prompt exactly as sent" rows (Langflow, Flowise, Dify) are documented-but-not-screenshot-confirmed.
6. **Pricing, ARR, star-count and adoption figures throughout wfh-001 are unverified secondary.** Deliberately none reused; no cell in this matrix rests on a market number.
7. **wfh-002 relevance is narrow.** Its FINDINGS cite shipped tools only as *provenance rows* for ontology types (`gate`, `skill`, `agent-def`) — it added no new tool characterization. `#183` records that wfh-002 closed early **with no artifact**; nothing in this re-cut inherits proof from it.
