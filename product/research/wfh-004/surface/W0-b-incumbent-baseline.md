# W0-b — The incumbent baseline: Claude-Code-as-harness, by inspection

**Run:** `wfh-004` · Issue #48 · phase `scan` · `agent_id: wfh-004-w0b` · read-only, zero graph writes, **zero experiments run** (SCOPE §11)

**Inspected:** `/workspaces/arch-research/.claude/{settings.json,settings.local.json,agents/,skills/,workflow/,rules/}` · `/workspaces/arch-research/{CLAUDE.md,.mcp.json,.devcontainer.json,.devcontainer/postCreate.sh,.gitignore,.github/}` · `~/.claude/{settings.json,plugins/,agents,skills,commands,hooks}` (last four absent) · the configured hook binary at `/home/vscode/.npm/_npx/39eded8816df3abb/node_modules/@dug-21/unimatrix/lib/hook-client/` (source read) · `claude --version` = **2.1.220**, `claude --help` · docs at `code.claude.com/docs/en/{hooks,settings,permissions,sub-agents,sandboxing,monitoring-usage,memory,sessions,checkpointing,headless}` · graph reads #157, #174, #179.

## 0. Four corrections to the §11 premise, before the table

**(i) The repo is not hook-free.** `.claude/settings.json` configures **eight** hook events — `SessionStart`, `Stop`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PreCompact`, `SubagentStart` — all pointing at one binary, the Unimatrix hook-client. #179's wording ("zero **enforcing** hooks") survives; "zero hooks" does not.

**(ii) Mechanically *why* they do not enforce.** The client is non-blocking **by construction**, not by omission. Its source states it twice: `index.js:434` — *"No process.exit() — let the event loop drain; exitCode stays 0"* — and the catch-all at `:432` — *"Last-resort guard: NEVER stdout, NEVER nonzero exit."* `transform.js` is *"the ONLY module that writes stdout"*, and it emits exactly one shape: a `hookSpecificOutput.additionalContext` envelope (or a bare body). It never emits `permissionDecision`, never `decision:"block"`, never a non-zero code. Further, `build-request.js` returns a `null` sentinel for non-`context_cycle` `PreToolUse` (*"observation retired"*), and the `PreToolUse` matcher in settings is already narrowed to `^context_cycle$|^mcp__unimatrix__context_cycle$`. **The one blocking-capable channel wired in this repo is scoped to one tool and short-circuits before it could speak.** This is telemetry-and-injection, deliberately; it is not a policy plane.

**(iii) The environment actively provisions bypass.** `~/.claude/settings.json` sets `"skipDangerousModePermissionPrompt": true`, and `.devcontainer/postCreate.sh` writes a `--dangerously-skip-permissions` shell alias into `~/.bashrc`. `.devcontainer.json` adds docker-in-docker, Tailscale, `--device=/dev/net/tun`, and bind-mounts the host `~/.ssh` plus `SSH_AUTH_SOCK`. So the container is not a confinement boundary either. The baseline is not "unconfigured"; it is **configured toward maximum authority**.

**(iv) Role separation is inert at the field level.** All six `.claude/agents/factory/*.md` use frontmatter keys `type`, `scope`, `capabilities` — **none of which Claude Code reads**. The recognized restriction fields (`tools`, `disallowedTools`, `permissionMode`, `maxTurns`, `hooks`, `mcpServers`, `isolation`, `memory`, `effort`) are absent from every agent; only `model: fable` on `hypothesizer.md` is a live field. Every specialist therefore inherits the full subagent tool pool. "factory-researcher is read-only", "only the curator writes nodes" — the garage's cardinal invariants — are prose in the markdown body, enforced by model compliance alone.

---

## 1. The baseline table

Legend: **A** configured & running · **B** supported, not set up · **C** cannot be expressed · **?** B/C-ambiguous.

| # | Capability, as observable behavior | Concern | Verdict | Mechanism (exact key/event/field) | Evidence |
|---|---|---|---|---|---|
| 1 | A named specialist runs in its own context window and returns only a summary | Structure | **A** | `.claude/agents/**/*.md`, `Agent` tool | 6 agent files; docs `sub-agents` |
| 2 | Work is phased and gated; phases named, ordered, gate-blocking | Structure | **A**(prose) | markdown protocols read by the model | `.claude/workflow/theme-scan.md` (109 ln), `research-scope.md` |
| 3 | A named unit's step boundary is machine-observable | Structure | **A** | `SubagentStart` hook fires per spawn, carries `agent_type` | `settings.json` SubagentStart matcher `*` |
| 4 | A spawned specialist is denied a tool it should not have | Structure/Security | **B** | `tools:` allowlist / `disallowedTools:` denylist in agent frontmatter — CLI-enforced, resolves before launch | absent from all 6 agents; docs `sub-agents#available-tools` |
| 5 | A specialist cannot spawn further specialists | Structure | **A**(default) | `Agent` is removed from subagents unless nested spawning enabled | docs `sub-agents` L326 |
| 6 | Which subagent types an agent may spawn is restricted | Structure | **B** | `tools: Agent(worker, researcher)`; or `permissions.deny: ["Agent(name)"]` | not set |
| 7 | Retrieved knowledge is injected into a new specialist automatically | Context | **A** | `SubagentStart` → server `ContextSearch` → stdout `hookSpecificOutput.additionalContext` | `transform.js:46-58` (byte-pinned envelope) |
| 8 | Retrieved knowledge is injected on each user prompt | Context | **A** | `UserPromptSubmit` → `ContextSearch` (≥N words) → plain stdout | `build-request.js:78-97` |
| 9 | Compaction is intercepted and re-seeded from the KB | Context | **A** | `PreCompact` → `CompactPayload` (sync, injects) | `build-request.js:100` |
| 10 | Standing instructions load into every session | Context | **A** | `CLAUDE.md`, `.claude/rules/*.md` | root `CLAUDE.md`; `rules/unimatrix-access.md` |
| 11 | Rules load only when relevant files are touched | Context | **B** | `paths:` frontmatter on `.claude/rules/*.md` | no `paths:` in `unimatrix-access.md` |
| 12 | Skill content is pre-loaded into a specialist at spawn | Context | **B** | `skills:` frontmatter field (injects full body) | not set |
| 13 | What went into context is enumerable with token counts | Context/Introspect | **B** | `/context`, `/context all` | never run in-repo |
| 14 | A command is refused before execution by a matched rule | Security | **B** | `permissions.deny` entries for Bash/Edit/Read/MCP/Agent patterns | **no `permissions` key in any settings file** |
| 15 | A tool call is refused by a policy program at call time | Security | **B** | `PreToolUse` → `hookSpecificOutput.permissionDecision:"deny"` | present but scoped + non-blocking (§0-ii) |
| 16 | Bash writes outside the working tree fail at the OS level | Security | **B** | `sandbox.enabled`, `sandbox.filesystem.{allowWrite,denyRead,denyWrite}` (bubblewrap) | no `sandbox` key; bubblewrap/socat not installed |
| 17 | Network egress is confined to an allowlist | Security | **B** | `sandbox.network.{allowedDomains,deniedDomains}` via out-of-sandbox proxy | not set; Tailscale + DinD present |
| 18 | Credential files are unreadable to spawned commands | Security | **B** | `sandbox.credentials.files`, `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | `~/.claude/.credentials.json` readable (mode 600, same uid) |
| 19 | Bypass mode is unavailable however invoked | Security | **B** (managed tier) | `permissions.disableBypassPermissionsMode`, `allowManagedPermissionRulesOnly` in **managed-settings** | inverse configured (§0-iii) |
| 20 | Config edits mid-session are refused | Security | **B** | `ConfigChange` hook, `decision:"block"`, matcher `project_settings`\|`local_settings` | not configured |
| 21 | An instruction arriving inside tool output is stripped of authority | Security | **C** | — see §4-C1 | — |
| 22 | Every tool call is recorded durably with its inputs and result | Introspection | **A** | `PostToolUse`/`PostToolUseFailure` matcher `*` → `RecordEvent`; JSONL transcript | `settings.json`; `~/.claude/projects/**/*.jsonl` |
| 23 | A run's events carry an `agent_id` and `parent_agent_id` | Introspection | **B** | `CLAUDE_CODE_ENABLE_TELEMETRY=1` + enhanced-telemetry beta spans | no `env` key set; OBS-14 / D6 `created_by: anonymous` are this hole |
| 24 | Work in a subagent is attributable to a named unit | Introspection | **B** | `SubagentStart`/`SubagentStop` matcher = agent name; OTel `agent.name`, `query_source` | Start configured, **Stop is not** |
| 25 | Live progress is visible mid-run | Introspection | **B** | `statusLine`, `--output-format stream-json`, `--include-hook-events` | not set |
| 26 | Token spend is reported per model per day for this repo | Cost | **A** | `opcost` skill parsing `~/.claude/projects/**` transcripts | `.claude/skills/opcost/opcost.py` |
| 27 | Cost is attributed to a subagent / skill / MCP tool | Cost | **B** | `claude_code.cost.usage` with `agent.name`, `skill.name`, `query_source`, `mcp_tool.name` | telemetry off |
| 28 | A run halts when spend exceeds a ceiling | Cost | **?** | `--max-budget-usd` (**`--print` only**); no settings key, no hook carries cost | docs `headless`; `--help` |
| 29 | A turn or subagent is bounded in length | Cost/Recovery | **B** | `maxTurns:` per agent, `--max-turns`, `turnTimeout`, `inactivityTimeout` | none set |
| 30 | Outcome is attributable to the configuration that produced it | Self-improve | **B** | `SessionStart` hook could stamp a config hash; `ConfigChange`, `InstructionsLoaded` events exist | none; `.claude/settings.local.json` is **gitignored** (`.gitignore:166`) — local config is unversioned and unauditable |
| 31 | A specialist carries lessons across sessions | Self-improve | **B** | `memory: user\|project\|local` per agent → `.claude/agent-memory/<name>/` | not set |
| 32 | Two configurations are compared on outcome | Self-improve | **C** | see §4-C3 | — |
| 33 | A session survives interruption and resumes | Recovery | **B** | `--resume/-c/--fork-session`; transcripts persisted | never used in-protocol |
| 34 | File edits are snapshot and reversible | Recovery | **B** | `fileCheckpointingEnabled`, `/rewind` (100 snapshots; **Bash-written and subagent-written files excluded**) | not set |
| 35 | A dead/hung **subagent** is detected and resumed from where it stopped | Recovery | **C** | see §4-C2 | #174 |
| 36 | A long-running unit survives the parent session | Recovery | **B** | `--bg` / `claude agents` (background agents are *sessions*), `isolation: worktree` | not used |
| 37 | The run stops at a gate and waits for a human | Steering | **A**(prose) | protocol text; `AskUserQuestion` (disabled by user memory) | `theme-scan.md`; OBS-5/OBS-13 |
| 38 | A human's mid-run instruction is forced into the loop | Steering | **B** | `Stop` hook → `decision:"block"` + `reason` re-enters the agentic loop; `SubagentStop` likewise | `Stop` configured but non-blocking |
| 39 | An out-of-band instruction reaches a running agent | Steering | **B** | `FileChanged` hook (watch a control file) + `SessionStart.watchPaths`; `SendMessage` to a running agent | not configured |
| 40 | `grade:proven` without a `proven_by` artifact is refused | Structure/Evidence | **B** (syntactic) / **C** (semantic) | `PreToolUse` matcher on the Unimatrix write tools → `deny` | §4-C4 |

---

## 2. Per-concern verdict

**Structure — high coverage, low binding.** The incumbent gives real addressable units for free: named subagent types, isolated context windows, a spawn event per unit, and default-off nested spawning. What it does *not* give is a sequence: phases, dependencies, and gates exist only as prose in `.claude/workflow/*.md` interpreted by the model. Residual: an ordering/dependency representation that something other than the model can read.

**Context provisioning — the strongest configured concern, and the surprise of this partition.** Three live injection points (`UserPromptSubmit`, `SubagentStart`, `PreCompact`) already do semantic retrieval and splice results into context via `additionalContext`. This is genuinely running today and is the one concern where the garage is ahead of its own baseline. Residual: no record of *what was left out* — the injection is one-way and its budget is server-side (`transform.js`: *"no client-side budget"*). Explainability of an injection is absent.

**Security — near-zero coverage, and it is a configuration choice, not a ceiling.** The incumbent ships four independent enforcement planes: permission rules (pre-execution, all tools), `PreToolUse` deny (programmatic), OS sandbox (bubblewrap/Seatbelt, filesystem + egress proxy, binds child processes), and per-agent tool allowlists. **This repo runs none of them**, and additionally provisions bypass. Residual after full configuration is small but real and named in §4.

**Introspection — good raw capture, no addressing.** `PostToolUse`/`PostToolUseFailure` on `*` plus the JSONL transcript give a durable record. What is missing is exactly OBS-14's diagnosis: units are not named in the record. `SubagentStart` is configured; `SubagentStop` is not, so a specialist's work has an opening bracket and no closing one. OTel with `agent_id`/`parent_agent_id` spans and `agent.name` on cost — the direct fix — is one `env` key away and unset.

**Cost — measurement yes, management no.** `opcost` proves the raw numbers are extractable, and OTel would attribute them per subagent/skill/tool. Enforcement is the gap: the only ceiling primitive, `--max-budget-usd`, is `--print`-only, and no hook event carries a spend figure — the CLI's control channels match on *tool calls*, not on *spend*, so spend is not a matchable predicate. See ambiguity A-1.

**Self-improvement — nothing configured, and the substrate is thin.** Per-agent `memory:` would give cross-session learning for free. Attribution of outcome→config is possible-but-unbuilt (nothing stamps a config fingerprint on a run, and `settings.local.json` is gitignored, so part of the config is not even versioned). Controlled comparison is the residual (§4-C3).

**Recovery / durability — asymmetric.** Sessions are durable and resumable; **subagents are not** (§4-C2). Since the garage puts all specialist work in subagents, the incumbent's durability lands entirely on the layer the garage does not use. `/rewind` explicitly excludes both Bash-written and subagent-written files — the two ways this repo actually writes.

**Human steering — one live prose gate, zero mechanism.** `Stop`/`SubagentStop` blocking is the incumbent's real steering primitive (a hook re-injects and forces the loop to continue), and `FileChanged` + `watchPaths` is a genuine out-of-band channel. Both unconfigured. The garage's steering today is the human typing between turns.

---

## 3. The configured-vs-available delta for THIS repo

Ranked by distance between what is running and what one settings block would give:

1. **`permissions.deny` is empty.** Every cardinal invariant is one rule away from CLI-level enforcement: the `.claude/**` tree, the `product/factory/**` tree, and the Unimatrix write tools for non-curator roles. Rules merge across scopes and deny wins.
2. **Six agent files carry zero recognized restriction fields.** `factory-researcher` is "read-only" in prose while holding `Write`, `Edit`, and every `mcp__unimatrix__*` write tool. `tools:`/`disallowedTools:` are CLI-enforced and resolve before launch.
3. **The only enforcement-capable hook channel is spent on telemetry.** `PreToolUse` is matched to one tool and returns a null sentinel; a second `PreToolUse` entry with a different matcher and a blocking script would coexist with it.
4. **`SubagentStop` is not configured** while `SubagentStart` is — units open and never close in the record. This is half of OBS-14.
5. **Telemetry is off.** Enabling it plus the beta traces flag delivers per-subagent cost and `parent_agent_id` spans — the direct remedy for both OBS-14 and D6's `created_by: anonymous`.
6. **No sandbox.** bubblewrap/socat are not even installed, while the devcontainer adds Tailscale, DinD, and the host SSH agent.
7. **Bypass is provisioned, not merely unconfigured** (§0-iii).
8. **No `maxTurns`, `turnTimeout`, `inactivityTimeout`, `--max-turns`.** #174's silent death had no timeout to trip.
9. **No `memory:`, no `isolation: worktree`, no `skills:` preload, no `paths:` scoping on rules.**
10. **`.claude/settings.local.json` is gitignored** — part of the harness config is outside version control, so "what configuration produced this run" is unanswerable even in principle today.

**The honest headline: on Security and Introspection, "the incumbent is inadequate" is not yet an available claim. Nearly every named gap is a switch we did not flip.**

---

## 4. Structural limits, argued mechanically

**C-1 — Authority-stripping of instructions arriving in data.** Tool results, file contents, MCP responses, and hook `additionalContext` all enter the model as tokens in one stream with no privilege field. `PostToolUse.updatedToolOutput` can rewrite or redact output — a real content filter — but the rewritten text lands in the same stream at the same trust level. A hook cannot restore a distinction the representation does not carry. *Cannot be expressed*, not *hard to configure*: there is no key whose value is "this span is data".

**C-2 — A subagent is not a resumable unit.** Docs: subagents "work within a single session" and "run in the same process as the parent session." `--resume`/`--continue`/`--fork-session` operate on session ids; a subagent has none. There is no hook event for a subagent that *dies* or *hangs* (only `SubagentStop`, on normal finish), and `maxTurns` counts turns, not wall-clock. Mechanically: recovery requires a durable checkpoint keyed to the unit, and the unit has no key. The incumbent's answer is to change the unit — background agents (`--bg`) *are* sessions — which is a different addressing scheme, not a fix to this one.

**C-3 — Controlled comparison of two configurations.** Requires (a) the config as a versioned value, (b) two runs differing only in it, (c) an outcome metric. (a) is (B). (b) is structurally blocked: a run's trajectory depends on model sampling and on context assembled by retrieval whose corpus mutates between runs — the garage writes to Unimatrix during the run it would compare. No configuration key holds the corpus fixed. *A/B comparison is not expressible without an external replay substrate*, which is outside the harness.

**C-4 — Semantic evidence adjudication.** A `PreToolUse` deny on the Unimatrix tag tool can refuse any `grade:proven` lacking a `proven_by` field — syntactic, deterministic, cheap, and currently unbuilt. Whether the named artifact *demonstrates the claim at its altitude* is a prose judgment; per SCOPE C-2 that needs an LLM leaf, and an LLM leaf is not a deterministic gate. The syntactic half is (B); the semantic half is (C) by C-2, not by any Claude Code limitation.

**Explicitly NOT structural — the SCOPE C-4 case, refined.** "An LLM cannot restrict itself because it holds the credentials" is *not* a flat structural limit in this incumbent. A root-owned managed-settings tier, bypass-mode disabling, credential-file denial, domain allowlisting, and a deny on re-invoking the CLI together **do** bound an agent that holds Bash. What is structurally true is narrower and sharper: **the agent cannot bind itself — the binding authority must be a principal the agent cannot write as.** That is a statement about who owns the policy file, not about what the harness can express. State it that way in generation; the untested residual is C-5.

**C-5 (candidate, untested) — escape via a fresh process.** Even fully configured in-repo, an agent with Bash and a readable credential file can exec a *new* CLI process (or hit the API directly) whose policy is whatever it passes on the command line. Closing it requires the managed tier plus OS confinement, i.e. a principal outside the run. Whether the managed tier actually closes it is **A-6** below — not tested, and must not be (SCOPE §11).

---

## 5. The ambiguity register (B/C-AMBIGUOUS — probe queue raw material)

Each: the claim, why inspection cannot settle it, and the single cheapest test. **None run** (SCOPE §11). Triage is bound to route anything turning on these `needs-a-probe`.

| ID | Ambiguous claim | Cheapest settling test |
|---|---|---|
| **A-1** | *Spend can be capped mid-run outside `--print`.* `--max-budget-usd` is print-only; but a `PostToolUse`/`Stop` hook could parse the transcript's usage records and return a stop directive. Whether that terminates an interactive run — and whether it terminates a *subagent's* loop or only the parent's turn — is undocumented. | Register a `Stop` hook that stops the loop once a transcript-derived token total crosses a low threshold; run one interactive turn and one Agent spawn. Observe whether each halts. |
| **A-2** | *A `PreToolUse` deny actually fires inside a subagent.* Docs say hooks run for subagents and carry `agent_id`, but the repo's only `PreToolUse` short-circuits, so we have never seen a deny land in a subagent — nor whether `settings.json` hooks or only frontmatter `hooks:` apply there. | One `PreToolUse` matcher on `Write` returning a deny decision; spawn one subagent; ask it to write a file. |
| **A-3** | *`tools:`/`disallowedTools:` on an agent bind when the parent invokes it via the `Agent` tool with its own arguments.* Docs describe file-defined restriction; the interaction with `--agents` JSON, plugin agents (which ignore `permissionMode`), and background-mode tool filtering is version-sensitive. | Add `disallowedTools: Write, Edit` to `factory-researcher.md`; spawn it; instruct it to write a file. |
| **A-4** | *Deny rules protect the config that defines the roles.* A deny on the `.claude/**` tree should stop an agent rewriting its own restrictions — but `Write` vs `Edit` vs Bash-shell-write coverage differs, and Bash wrapper-stripping is documented as built-in and not configurable. | Set the deny rule; attempt the edit via Edit, Write, and three Bash spellings. Count which are refused. |
| **A-5** | *The single-writer firewall is enforceable at the MCP boundary.* The Unimatrix write tools can appear in `permissions.deny` — but per-*role* scoping requires the rule to live somewhere role-specific, and per-agent `permissions` is not a frontmatter field (only `permissionMode` is). Session-wide deny would block the curator too. | Put the MCP writes in `disallowedTools:` on the five non-curator agents, leave the curator's empty, and attempt a write from each. |
| **A-6** | *Managed settings actually bound an agent holding Bash* (the C-5 escape). The relevant keys are documented; whether they survive a re-invocation with its own settings path, an overridden config dir, `--bare` (which "skips hooks… MCP… CLAUDE.md"), or safe-mode is exactly the question. `--bare`'s documented behavior is the sharpest threat. | Install a managed policy denying one tool; from inside a run, attempt the same tool via each of those three re-invocation routes. |
| **A-7** | *`SubagentStop` fires on abnormal termination* (#174's silent death). Docs say it fires "when a subagent finishes." Crash/hang/kill are unaddressed. | Spawn a subagent whose first act is to kill its own process; observe whether `SubagentStop` fires and with what payload. |
| **A-8** | *A `FileChanged` hook is a working mid-run steering channel.* Documented as fires-on-watched-file-change, cannot block, cannot inject. If it cannot inject, it cannot steer — unless `SessionStart.watchPaths` + some other event carries the payload. | Register a watch path and a `FileChanged` hook; write the watched file mid-run; observe whether anything reaches the model's context. |
| **A-9** | *Config-tampering is detectable.* `ConfigChange` can block, matcher includes `local_settings`/`project_settings`/`skills` — but whether it fires for an *agent-file* edit (agents are not in the matcher list) is unstated. | Register `ConfigChange` logging all invocations; edit `settings.json`, then an agent file; compare. |
| **A-10** | *OTel spans attribute cost to a named factory specialist.* `agent.name` is documented as "subagent type name (or `custom` for user-defined)" — if our file-defined agents all report `custom`, per-role cost attribution collapses and OBS-14 is not fixed by turning telemetry on. | Enable telemetry + console exporter, spawn `scout` and `hypothesizer`, read `agent.name` on the cost metric. |
| **A-11** | *The sandbox can run here at all.* bubblewrap needs user namespaces; this is an unprivileged devcontainer with DinD, and a weaker-nested-sandbox flag exists precisely for that failure. Every Security (B) resting on OS enforcement may be (C)-in-this-environment. | Install bubblewrap/socat, enable the sandbox, run one write outside cwd. |
| **A-12** | *Injected `additionalContext` is distinguishable, to the model, from user instruction.* The `--- Unimatrix Context ---` header is a convention emitted by our own server, not a harness-level trust marker. Whether it is structurally separated or merely prefixed bears directly on C-1. | Inspect a raw transcript entry for a `SubagentStart` injection and check whether the harness wraps it in a distinct role/block or concatenates it. |

**Under-reported risk:** items 4, 14, 15, 16, 17, 18, 19, 20, 24, 27, 38, 39 in the table are marked **B** on documentation alone. Each is (B) *if and only if* the corresponding probe lands. Treat the entire Security column as provisional-B pending A-2 through A-6 and A-11.
