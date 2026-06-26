# shd-005 / W7b — Platform capability-coverage extension (the multi-purpose lens)

**Run:** shd-005 · **Workstream:** W7b · **Agent:** shd-005-researcher-W7b · **Date:** 2026-06-26
**Mode:** read-only, directional. Every cell is **doc-claim / config-reference**, nothing demonstrated by us, nothing `proven`.
**Why this exists:** W1–W6 ranked the slate against **C3 alone** (routing). That under-values multi-purpose platforms (*platform-blindness*). W7b re-frames: grade each harness on **how much of the whole `shd` loop's need-set it covers** — what it bundles *beyond* C2/C3 that we would otherwise have to assemble (observability, cost governance, policy, audit, sub-agent orchestration, MCP) — **without** letting breadth paper over a hard-constraint gap (N3).

**Reuse base (not re-derived):** harness routing mechanics from `findings-W3.md`; router landscape from `findings-W2.md`; the N3 egress firewall from `findings-W4.md` (no harness enforces egress — the gate lives one layer down); the four-bar gap from `findings-W6.md`.

---

## 0. Two findings that frame every row

1. **C1 (local serving) is `✗` across the ENTIRE slate.** None of these tools *serves* a model — every one is a *client* of a C1 stack (Ollama / vLLM / llama.cpp / a gateway). A platform's breadth never delivers C1. Picking a "platform" does **not** shrink the C1 need; shd-004 still owns it.
2. **N3 (sensitive-code-local, HARD) enforcement is `✗` across the ENTIRE slate.** Per W4, *no harness gates LLM-prompt egress* — they all merely *configure an endpoint*. The egress gate is a layer below the harness (local gateway / network deny-by-default). For the **sensitive-code path role**, every harness is **⛔ disqualified as a sole N3 control**, regardless of how many ops features it bundles. **Breadth is soft-grade; N3 is hard-gated. The two never net against each other.**

**Grade-class tags:** **[H]** = hard / must-be-100%-or-gated (C1, C2-contract, N3). **[S]** = soft / convenience-grade.

---

## 1. The harness × need matrix

Legend: `✓` strong · `◑` partial · `✗` none · `⛔` disqualified-for-role-by-hard-constraint.

### Core + NFRs

| Need | Grade | **Goose** | **Roo/Cline** | **aider** | **Continue** | **OpenHands** | **Claude Code** | **ruflo** |
|---|---|---|---|---|---|---|---|---|
| **C1** local serving | [H] | ✗ client→Ollama | ✗ | ✗ | ✗ | ✗ LiteLLM-wrapped client | ✗ | ✗ orchestrates CC |
| **C2** agentic drive | [H] | ✓ Rust CLI+desktop | ✓ VS Code | ✓ CLI | ✓ Agent mode | ✓ sandboxed runtime | ✓ strongest CLI | ✓ meta-harness (CC-coupled) |
| **C3** routing/escalation | [H] | ◑ **lead/worker auto** (turn/fail heuristic) | ◑ per-mode+profile (manual) | ◑ architect/editor 2-tier (static) | ✗ roles≠routing (doc-confirmed) | ◑ named configs+draft_editor (manual) | ◑ weak 2-tier native, **owns egress choke-point** | ✓ **embedded 3-tier router** (WASM→cheap→Opus) |
| **N1** budget/cost | [S] | ◑ downshift; cost via Langfuse | ◑ in-UI per-task $; subtask agg missing (#5376) | ✓ native `/tokens` $+budget | ◑ weak native | ✓ **max-iter/retry + accumulated-cost caps** | ✓ native `/cost`+OTEL cost metrics | ✓ 3-tier "≤75%" (doc-claim) |
| **N2** resilience/offline | [S/H] | ◑ Ollama offline; no auto cloud→local failover | ◑ manual local profile | ◑ manual local | ◑ local roles | ◑ local config; LiteLLM under it | ◑ local base-URL=offline; server-fallback Anthropic-only | ◑ failover built-in but **CC-coupled load path** |
| **N3** sensitive-code-local | **[H]** | ⛔ no egress gate | ⛔ | ⛔ | ⛔ | ⛔ **sandbox≠egress gate** | ⛔ best choke-point ≠ enforced gate | ⛔ routing-local but no gate, CC-coupled |
| **N4** multi-machine | [S] | ◑ config travels | ◑ settings export | ✗ per-invocation CLI | ✗ config portable | ◑ runs as a **service/container** | ◑ env/settings replicable | ✓ **swarm/federation is its premise** |

### Adjacent / ops (all [S] — what it bundles beyond C2/C3)

| Need | **Goose** | **Roo/Cline** | **aider** | **Continue** | **OpenHands** | **Claude Code** | **ruflo** |
|---|---|---|---|---|---|---|---|
| observability/tracing | ✓ native Langfuse+OTEL | ◑ in-UI, no export | ◑ CLI cost, opt-in analytics | ◑ local `dev_data`; 2.0 dropped telemetry | ✓ **append-only EventLog**+SDK events | ✓ **native OTEL metrics/events/traces** (subagent spans nest) | ◑ 27 hooks + SONA trajectories (bespoke) |
| cost-tracking & attribution | ◑ via Langfuse | ◑ per-task; no subtask roll-up | ✓ native `/tokens` $ | ◑ dev_data usage | ✓ accumulated-cost + budget caps | ✓ `/cost`+OTEL+SDK stream | ◑ router cost-tiering (bespoke) |
| key/secret management | ◑ keyring | ◑ VS Code secret store | ◑ env/.env/yaml | ◑ env templating | ◑ fine-grained access control | ✓ apiKeyHelper+enterprise managed settings | ◑ inherits CC |
| caching | ◑ provider-level | ◑ Anthropic prompt-cache | ✓ `--cache-prompts` (30–70% doc) | ◑ provider-level | ◑ via LiteLLM | ✓ native prompt caching | ◑ memory/RAG layer |
| guardrails/policy | ✓ **4 modes incl SmartApprove** | ◑ auto-approve + per-mode tools + `.rooignore` | ✗ `--yes`; relies on git-undo | ◑ mode-scoped tools (Chat=none/Plan=RO/Agent=all) | ✓ **sandbox+access control+iter circuit-breaker** | ✓ **permissions allow/deny/ask + hooks (PreToolUse)** | ◑ hooks intercept tool calls (bespoke) |
| audit logging | ◑ session logs+Langfuse | ◑ shadow-git checkpoints | ✓ **git-native: every edit=commit, /undo,/diff** | ◑ local event logs | ✓ **append-only EventLog** | ✓ OTEL events (allowed/denied+decider)+hooks | ✓ memory store+trajectories (bespoke) |
| sub-agents/orchestration | ✓ recipes+subagent teams | ✓ **Orchestrator/Boomerang** (isolated-ctx subtasks) | ✗ (architect/editor=2-call, not orchestration) | ✗ | ◑ microagents/delegation | ✓ native subagents/Task+agent teams | ✓✓ **hive-mind queens, swarm, federation, 314 MCP tools** |
| MCP / tool-ecosystem | ✓ extensions (native) | ✓ native MCP | ◑ community aider-MCP-server (emerging) | ✓ native MCP provider | ✓ Bash+Py+browser+file+MCP | ✓ **reference MCP client** | ✓ exposes **314 MCP tools** |
| multi-provider breadth | ✓ 15+ incl Ollama | ✓ broad BYOK+local | ✓ LiteLLM→100+ | ✓ broad role-based | ✓ LiteLLM→broad | ✗ **Anthropic-native; breadth only via gateway** | ◑ any LLM via router, **Claude-coupled** |

---

## 2. Per-harness qualified / disqualified roles

Roles: **drive** (C2) · **router** (C3) · **sensitive-path** (N3-hard) · **ops backbone** · **orchestration layer** · **distribution** (N4) · **frontier conduit**.

- **Claude Code** — **Qualified:** ops backbone (best standards-based OTEL+cost+caching+policy+audit bundle), drive, frontier conduit, orchestration, **single egress choke-point** (pairs with a local gateway). **Disqualified:** C1 server, multi-provider router on its own (Anthropic-native — needs a gateway), **sensitive-path as a sole N3 control** (⛔).
- **ruflo** — **Qualified:** orchestration layer (maximal — swarm/federation/queens), router (only native multi-tier), distribution (N4 ✓). **Disqualified:** C1 server, **sensitive-path** (⛔, CC-coupled + no gate), standards-based ops (obs/audit are bespoke). **Caveat:** *platform on a platform* — inherits CC's posture plus a heavy bespoke, non-standard layer.
- **OpenHands** — **Qualified:** drive, ops backbone (EventLog audit + accumulated-cost caps), **runtime-isolation** (sandbox), distribution (service). **Disqualified:** C1 server, **sensitive-path** (⛔ — sandbox isolates execution, not egress), router (manual).
- **Goose** — **Qualified:** drive, **router** (only native runtime auto-escalation), guardrails (SmartApprove), observability (Langfuse/OTEL). **Disqualified:** C1 server, sensitive-path (⛔), orchestration-at-scale.
- **Roo/Cline** — **Qualified:** drive, orchestration (Boomerang), structured manual routing, checkpoint/rollback (shadow-git). **Disqualified:** C1 server, sensitive-path (⛔), cost attribution at depth (no subtask roll-up), distribution (N4 ✗).
- **aider** — **Qualified:** drive, **native cost transparency**, **audit-by-construction** (git commits), caching. **Disqualified:** C1 server, sensitive-path (⛔), orchestration (✗), distribution (✗), MCP (emerging), guardrails (✗).
- **Continue** — **Qualified:** drive (IDE), MCP, mode-scoped tool policy. **Disqualified:** C1 server, **router** (✗ doc-confirmed), sensitive-path (⛔), orchestration (✗).

---

## 3. Candidate new capabilities / NFRs `shd` has NOT decomposed

1. **Sub-agent / swarm orchestration** — Boomerang (Roo), native subagents (CC), recipes (Goose), hive-mind (ruflo). Loop is decomposed single-agent; orchestration is a distinct deliverable.
2. **MCP / tool-ecosystem access** — table-stakes across the slate; a "tool-access" capability/NFR is implicit and unowned.
3. **Observability / tracing (OTEL)** — CC/Goose/OpenHands native; load-bearing for a *self-improving* factory, not convenience.
4. **Run-time cost governance & attribution** — per-key/per-task caps + accumulated-cost circuit-breakers. Distinct from N1 (owned-HW posture); this is *live spend control on the escalation path*.
5. **Audit / session logging** — EventLog (OpenHands), git trail (aider), OTEL events (CC). Candidate **factory-plane** requirement for the demonstrated-vs-claimed firewall.
6. **Guardrails / tool-approval policy engine** — SmartApprove, permissions+hooks, mode-scoped tools, sandbox.
7. **Runtime sandbox isolation** (OpenHands) — a *security* capability **distinct from N3**: isolates execution, not egress. Needs its own node so it is not conflated with N3.
8. **Checkpoint / rollback** — Roo shadow-git, aider `/undo`. N2-adjacent resilience.

---

## 4. The sharpest hard-vs-soft trap

**Counting bundled built-ins and concluding "this platform covers N3" — when N3 enforcement is structurally absent from the entire slate.**

- **OpenHands' sandbox is the most seductive false-positive.** "Secure sandboxed runtime + fine-grained access control" *reads like* sensitive-code protection. It isolates **code execution** in a container; the **LLM prompt** — your source code — still egresses to whatever model the config targets. **Sandbox ≠ egress gate.** N3-⛔ like the rest.
- **Claude Code's global `ANTHROPIC_BASE_URL` is the best *lever*, not a *gate*.** A base-URL setting is not deny-by-default/fail-closed; nothing stops a config or subagent override pointing upstream. Enforcement lives one layer down (W4).

**The rule:** all the breadth here — OTEL, `/cost`, caching, SmartApprove, EventLog, 314 MCP tools, swarms — is **soft-grade [S]**. Genuine value (it's what we'd otherwise hand-assemble), but **no quantity of [S] satisfies the one [H] need it cannot touch.** A harness bundling twelve ops features and a weak N3 story is **still N3-disqualified for sensitive paths.**

---

## 5. Flags / could-not-verify

- All cells are doc-claim/config-reference; no harness run. ruflo's "≤75% cost"/SONA, Goose lead/worker content-blindness, OpenHands caps, CC OTEL completeness are vendor/community claims — POC questions.
- ruflo is fast-moving + CC-coupled; "314 MCP tools / 27 hooks / v3.5.x" shift release-to-release. Its breadth is bespoke and welded to Claude Code (won't front an arbitrary harness — W2 caveat).
- aider MCP is a community wrapper (aider-as-MCP-server), not a strong native client.
- Continue 2.0 removed anonymous telemetry — obs now local `dev_data` only.
- N3 is a *demonstrated-absence-by-construction* (W3/W4 corroborate). Carry it unsoftened.

## 6. Citations
`{guide, generalanalysis.com/guides/anthropic-claude-code-security-best-practices}` · `{doc, code.claude.com/docs/en/agent-sdk/observability}` · `{blog, developersdigest.tech/blog/claude-code-agent-teams-subagents-2026}` · `{doc, goose-docs.ai/docs/guides/managing-tools/goose-permissions/}` · `{doc, langfuse.com/docs/integrations/goose}` · `{repo, github.com/ruvnet/ruflo}` · `{wiki, github.com/ruvnet/ruflo/wiki/MCP-Tools}` · `{blog, alphasignalai.substack.com/p/how-ruflo-turns-claude-code-into}` · `{wiki, deepwiki.com/All-Hands-AI/OpenHands}` · `{doc, docs.openhands.dev/sdk/arch/sdk}` · `{doc, aider.chat/docs/git.html}` · `{doc, aider.chat/docs/usage.html}` · `{doc, docs.roocode.com/features/boomerang-tasks}` · `{issue, github.com/RooCodeInc/Roo-Code/issues/5376}` · `{doc, docs.continue.dev/reference}` · `{doc, docs.continue.dev/customize/deep-dives/mcp}` · `{kb, shd-005 findings-W3/W4/W2}`

---

## Summary

- **Most-of-the-loop coverage splits three ways, not one:** **Claude Code** wins the *standards-based ops backbone* (native OTEL traces/metrics/events + `/cost` + prompt caching + permissions/hooks policy + audit + native subagents + reference MCP) — the cleanest bundle of things we'd otherwise hand-build; **ruflo** wins *orchestration + routing maximalism* (embedded 3-tier router, hive-mind swarm/federation, 314 MCP tools, memory) but bespoke and welded to Claude Code; **OpenHands** wins *runtime-isolation + budget caps + append-only audit, runnable as a service*.
- **What each bundles beyond C2/C3:** CC → OTEL observability, cost metrics, caching, policy engine (hooks), MCP client, subagents; ruflo → multi-agent orchestration + the only native multi-tier router + persistent memory; OpenHands → sandbox + accumulated-cost circuit-breakers + EventLog audit; Goose → only native *runtime auto-escalation* (lead/worker) + SmartApprove policy; aider → cost transparency + git-native audit-by-construction; Roo → Boomerang sub-task orchestration + shadow-git checkpoints.
- **Standout multi-need harness:** **Claude Code** for breadth-of-ops-we'd-otherwise-build on open standards; **ruflo** is the orchestration-maximal alternative but its breadth is non-standard and coupled (platform-on-a-platform) — flag, don't default to it.
- **Hard invariants no breadth fixes:** **C1 (local serving) is ✗ on all seven** — every tool is a client; a "platform" does not shrink shd-004's C1 work. **N3 enforcement is ✗ on all seven** — none gates prompt egress; the gate is a layer below (W4).
- **Candidate new capabilities surfaced:** sub-agent/swarm orchestration · MCP/tool-ecosystem access · OTEL observability · run-time cost governance & attribution · audit/session logging · tool-approval policy engine · runtime sandbox isolation (distinct from N3) · checkpoint/rollback.
- **Sharpest hard-vs-soft trap:** mistaking bundled built-ins for N3 coverage — **OpenHands' sandbox isolates code *execution*, not prompt *egress* (sandbox ≠ egress gate)**, and CC's global base-URL is a *lever*, not an enforced gate. All the bundled breadth is soft-grade and never nets against the one hard-gated need; a feature-rich harness with a weak N3 story is still N3-disqualified for sensitive paths.
