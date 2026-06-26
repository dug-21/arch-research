# shd-005 / W3 — Harness-native routing (REUSE-FIRST)

**Question:** Per agentic harness (the C2 slate), how much of **C3 — intelligent multi-LLM routing** does it deliver *natively*, with **no extra router**? For each: routing class · selection mechanism · N3 egress-gate · N2 offline-fallback · N4 multi-machine · the gap a dedicated router still fills.

**Firewall note (directional):** all entries below are **doc-claim / config-reference** unless marked *demonstrated*. I read vendor docs + repos/issues; I ran no harness. Nothing here is `proven`. The completion question ("does this routing actually hold under load / gate egress reliably") is a later POC, not settled by me.

**Self-brief (read-only, shd-002 prior art):** finding #16 *local agentic viability = the harness↔proxy↔model tool-call contract*; tech #12 *Claude Code via local /v1/messages shim (T3a)*; tech #13 *Continue — XML system-message-tools harness*; tech #15 *Goose — native tool-calls + XML fallback*; lesson #18 *harness mechanism is searchable, completion is not*. W3 stays on **mechanism**, not completion.

## The determining distinction

"Routing" in this slate splits into two very different things, and the firewall lives on the seam:

1. **Static role/profile routing** — you *pre-assign* a model to a job (architect vs editor, chat vs autocomplete, mode-X vs mode-Y) or switch by hand mid-session. Deterministic, config-driven. **Five of six harnesses do this well.**
2. **Dynamic policy/auto routing** — the harness *decides at runtime* which model to call based on task state (escalate on failure, downshift when cheap suffices). **Only Goose ships this natively** (turn-count + failure-threshold heuristic — *not* content/confidence-aware).

**No harness in the slate does content-aware or sensitivity-aware routing, and none enforces egress.** That is the C3 gap a dedicated router/gateway owns.

## Per-harness routing-capability table

| Harness | Routing class (native) | How it selects the model | N3 — can it gate egress? | N2 — offline-fallback | N4 — multi-machine | Gap a dedicated router still fills |
|---|---|---|---|---|---|---|
| **Goose** (Rust CLI + desktop, AAIF, v1.38.0) | **Policy-driven auto-escalation** (`LeadWorkerProvider`) — closest to C3 | `GOOSE_LEAD_MODEL` runs first N turns (`GOOSE_LEAD_TURNS`), auto-switches to worker; escalates back on `GOOSE_LEAD_FAILURE_THRESHOLD`; `GOOSE_LEAD_FALLBACK_TURNS`. **Turn/failure heuristic, not content/confidence.** Also manual dropdown; 15+ providers incl. Ollama (auto-lists local models). | No native egress control. Per-provider endpoints only; gating external. Local-only by configuring Ollama as sole provider. | Configure local provider as lead+worker → fully offline. No automatic cloud→local failover. | env config travels; no built-in cross-machine routing. | Content/sensitivity-aware routing; egress enforcement; turn-heuristic is blunt vs a real cost/quality policy. |
| **Roo Code / Cline** (VS Code ext) | **Policy-by-mode + profile switch** (manual-but-structured) | **Per-mode model**: each mode (Architect/Code/Ask/Debug + custom) auto-selects its model on mode change. **API Configuration Profiles** = named provider/model/settings bundles switchable via dropdown; diff strategy per-profile. Switch is mode/user-triggered, not task-confidence. | No native egress gate; profile just picks an endpoint. Local-only by pointing all profiles at a local OpenAI-compatible endpoint. | Manual: select a local profile/mode. No auto failover. | Settings export/import, per-workspace. No cross-machine service. | Auto (non-mode) routing; egress enforcement; cost/fallback chains. |
| **aider** (CLI) | **Two-tier split (architect/editor) + weak-model**, manual switch | `--model`/`--architect` + `--editor-model`; `--weak-model`; `/model`,`/editor-model`,`/weak-model` swap mid-session. Architect→editor is an automatic *two-call* pipeline (*demonstrated in docs*), but model assignment is static config, not task-chosen. | No native egress gate. Point all three slots at local for offline. | Manual: set local models. No auto failover. | Per-invocation flags / `.aider.conf.yml`; no service. | Runtime task-aware routing; fallback chains; egress enforcement. Architect/editor is the *split*, not a *router*. |
| **OpenHands** (All-Hands) | **Multiple named LLM configs + reserved roles**, switchable | `config.toml` named `[llm.<name>]` blocks, switchable mid-conversation. Reserved roles: `[llm.draft_editor]`, condenser model. Assignment per-config/agent, manual; no runtime task pick. | No native egress gate; per-config base_url. Local-only via a local-model config. | Manual local config. No auto failover. | Server/container deploy; per-deployment configs. No cross-host layer. | Task/confidence routing; cost-aware fallback; egress enforcement. |
| **Continue** (VS Code/JetBrains ext) | **Static role routing** (richest taxonomy), manual | 6 roles — chat, autocomplete, edit, apply, embed, rerank — each gets model(s) in `config.yaml`; first = default; switch via dropdown. *Doc explicitly states no automatic/confidence routing* (**demonstrated absence**). | *Doc explicitly silent on egress/network control* — no native gate. Local-only by assigning all roles to local endpoints. | Manual local roles; no auto failover. | `config.yaml` portable; no service. | Any dynamic routing at all; fallback chains; egress enforcement. Roles ≠ routing. |
| **Claude Code** (Anthropic CLI; T3a shim) | **Two-tier (main + small/fast) + gateway base-URL**, weakest native split | `ANTHROPIC_MODEL` + `ANTHROPIC_SMALL_FAST_MODEL` = fixed 2-tier. Real multi-model routing happens **downstream of `ANTHROPIC_BASE_URL`** at a gateway. Subagent/skill override falls back to inherited/default if blocked. `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` (v2.1.129+) reads gateway `/v1/models`. Fallback-chain entries outside allowlist are dropped. | **Strongest single-point lever:** `ANTHROPIC_BASE_URL` → local gateway funnels **all** traffic through one egress point you control. CC speaks frontier Claude *and* a local `/v1/messages` endpoint, but the base URL is **global** — one upstream at a time, so cloud+local simultaneously needs the gateway to fan out. **Caveat:** must verify endpoint truly speaks Anthropic `/v1/messages` (OpenAI-format → garbled). | If base URL = local gateway, fully offline. No native auto cloud↔local failover. | Env-var driven; same `settings.json`/env replicable per machine; no cross-host routing. | **Essentially all of C3.** CC contributes the *single egress choke-point*; offloads routing brain to the gateway — pairs with, not replaces, a dedicated router. |

## Ranking — who delivers the most of C3 natively

1. **Goose** — only harness with **runtime auto-switching** (lead/worker escalation), no external router. But trigger is a turn/failure heuristic, *not* content/sensitivity-aware, and **no egress gate** — covers the *escalation* axis of C3, not the *intelligent* or *sovereign* axes.
2. **Roo Code / Cline** — best **structured manual** routing: per-mode model auto-selection + named profiles ≈ a human-driven "architect vs editor + provider" router. Limit: mode/user-triggered, never task-state-triggered.
3. **aider** / **OpenHands** — strong **two-tier / multi-config** static splits; pipelines automatic, *model choice* static.
4. **Continue** — richest **role taxonomy** but explicitly **no dynamic routing** (doc-confirmed).
5. **Claude Code** — weakest *native* split (main + small/fast), **but** owns the cleanest **egress choke-point** for N3 via a global base URL. Its routing story *is* the gateway.

## The biggest gap (cross-cutting — what reuse does NOT buy)

- **Egress enforcement for N3 (HARD) is not a harness feature — anywhere.** Every harness merely *configures endpoints*; none *prevents* a config from reaching a cloud model. N3 must be enforced one layer down (network firewall / local gateway denying non-local upstreams). **Claude Code's global `ANTHROPIC_BASE_URL` is the single best native lever** (one controllable point); the others spread endpoints across roles/profiles/providers, which is *harder* to gate.
- **Intelligent (content/cost/sensitivity-aware) routing exists in zero harnesses.** Goose's turn-heuristic is the high-water mark and it's blind to task content. "Send sensitive code local, route bulk reasoning to frontier" — the actual C3 ask — is **unmet natively**.
- **No native offline auto-failover (N2).** All offline stories are "configure a local model"; none auto-fail-over cloud→local on outage. Router/gateway territory.
- **N4 multi-machine foreclosed by none, extended by none.** All config-portable; none ship a cross-host routing service.

**Implication for the router decision (hand to W1/W2):** a thin gateway in front (LiteLLM-style) buys exactly the three things no harness has — egress enforcement (N3), content/cost-aware routing (the "intelligent" in C3), outage failover (N2) — while **Goose's lead/worker** and **Roo's mode/profile** already cover the *escalation* and *role-split* slices for free. Cheapest viable shape is likely **harness-native split (Goose or Roo) + a local egress gateway**, not a bespoke router rebuilding what harnesses already do.

## Surprising / flags

- **Continue's docs explicitly state there is no automatic/confidence routing** — a rare *demonstrated negative*. Roles look like routing but are static assignment.
- **Goose lead/worker is turn-count + failure-threshold** ("escalate after N turns / M failures") — much blunter than "intelligent routing"; not content-aware (doc-claimed, not demonstrated by me — flag for POC).
- **Claude Code base URL is global, one-upstream-at-a-time.** "Speaks frontier Claude AND a local endpoint" is true only *via a fan-out gateway*; confirm against the live T3a shim before relying on simultaneous dual-endpoint.
- **OpenAI-format vs Anthropic `/v1/messages` mismatch** silently garbles CC output — a real N3/N2 trap if a local shim is misconfigured.

## Citations

- {doc, https://aider.chat/docs/usage/modes.html, "Chat modes (architect/editor) | aider"}
- {doc, https://aider.chat/docs/config/adv-model-settings.html, "Advanced model settings | aider"}
- {doc, https://aider.chat/docs/config/aider_conf.html, "YAML config (weak/editor model) | aider"}
- {doc, https://docs.roocode.com/features/api-configuration-profiles, "API Configuration Profiles | Roo Code"}
- {doc, https://docs.roocode.com/basic-usage/using-modes, "Using Modes (per-mode model) | Roo Code"}
- {doc, https://docs.continue.dev/customize/model-roles/intro, "Intro to Roles | Continue"}
- {doc, https://docs.continue.dev/reference, "config.yaml Reference | Continue"}
- {doc, https://docs.openhands.dev/openhands/usage/settings/llm-settings, "LLM Settings | OpenHands"}
- {doc, https://docs.all-hands.dev/modules/usage/llms/custom-llm-configs, "Custom LLM Configurations (draft_editor, named configs) | OpenHands"}
- {doc, https://goose-docs.ai/docs/getting-started/providers/, "Configure LLM Provider | goose"}
- {repo, https://github.com/block/goose/issues/4036, "multi-model/provider auto-switching (lead/worker) | goose #4036"}
- {repo, https://github.com/block/goose/issues/4040, "notes on Lead/Worker (GOOSE_LEAD_* env) | goose #4040"}
- {doc, https://code.claude.com/docs/en/model-config, "Model configuration (ANTHROPIC_MODEL / SMALL_FAST_MODEL) | Claude Code"}
- {repo, https://github.com/anthropics/claude-code/issues/25146, "Multiple API endpoints for different models/agents | claude-code #25146"}
- {doc, https://www.morphllm.com/claude-code-litellm, "Claude Code + LiteLLM gateway (base URL routing) | Morph"}
- {kb, unimatrix:finding#16, "Local agentic viability = harness↔proxy↔model tool-call contract (shd-002)"}
- {kb, unimatrix:tech#12, "Claude Code via local /v1/messages shim (T3a)"}
- {kb, unimatrix:tech#13, "Continue — XML system-message-tools harness"}
- {kb, unimatrix:tech#15, "Goose — native tool-calls + XML fallback"}
