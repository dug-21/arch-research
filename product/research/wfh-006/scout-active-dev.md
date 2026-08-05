# FINDINGS — scout / active-development surface / DISCOVERY

**Run:** wfh-006 (owner-directed single-target scout, no full protocol run)
**Target:** opencode · **Scan pin:** commit `66fdd51f0d6db8e47e876721c855ea155043b74c` (branch `dev`, 2026-08-05)
**Permalink base:** `https://github.com/anomalyco/opencode/blob/66fdd51f0d6db8e47e876721c855ea155043b74c/`
**Method:** full-history clone (15,311 commits, 1,020 `v*` tags) read locally at that SHA; GitHub API for repo/issue metadata. **Nothing was installed, built, or executed — no statement below is [demonstrated by us].**

**Why this scan ran.** The owner's thesis (2026-08-05) is that `theme:workflow-harness` (Jurati) and `shd` converge on one object: a privileged interposition point on the agent's tool-call boundary that the model can neither see nor edit — carrying security *denials* and Unimatrix knowledge *injection* as two payloads through one chokepoint. The architecture hypothesis is an inverted principal: a rules engine / workflow system as parent process, the LLM as a subordinate that returns proposals and holds NO tools, with exactly one proxied path for tool calls. opencode was scouted as a candidate fork/lift base for that harness.

---

## 0. Identity correction — `sst/opencode` is now `anomalyco/opencode`

[demonstrated by them, with artifact] `GET repos/sst/opencode` returns `"full_name": "anomalyco/opencode"` — the org renamed and GitHub redirects. The checked-in `package.json` already declares `"repository": {"url": "https://github.com/anomalyco/opencode"}`, and maintainer email domains moved `@sst.dev` → `@anoma.ly`. Same project, same 193k-star history, not a fork. Use `anomalyco/opencode` as the canonical `ref`.

**Collision check:** this is the SST/Dax Raad TypeScript project (`opencode.ai`, 2025-04-30, MIT). Not `opencode-ai/opencode` (the Charm/Kujtim Hoxha Go predecessor — the very first commit in this history is authored by *Kujtim Hoxha*, 2025-03-21, so the two are genealogically linked but the current tree is a complete TypeScript rewrite), and not the several unrelated PyPI/academic "opencode" packages.

---

## 1. Provider abstraction — the single strongest liftable asset

### What it is

[inferred from reading code] **Two provider layers exist in the tree simultaneously**, because a rewrite is mid-flight:

| Layer | Where | Basis |
|---|---|---|
| **v1 (shipping)** | `packages/core` + `packages/opencode` | Vercel AI SDK — ~20 `@ai-sdk/*` packages, three **locally patched** (`patches/@ai-sdk%2Fmistral@3.0.51.patch` is 27 KB) |
| **v2 (new, first-party)** | `packages/llm` | **Hand-written wire protocols. No AI SDK at all.** |

`packages/llm` implements the provider protocols from scratch — `anthropic-messages`, `openai-chat`, `openai-responses`, `openai-compatible-chat`, `gemini`, `bedrock-converse` (with its own eventstream codec) — behind one provider-neutral request/event schema.

### Is it liftable without the loop, TUI, or server?

**Yes, and unusually cleanly** [inferred from reading code — static read, not a build]:

- **Module boundary:** `packages/llm/src` — **56 files, 9,533 LOC**, plus 9,937 LOC of tests including 40+ recorded HTTP cassettes (`test/fixtures/recordings/**`) covering real tool loops on OpenAI, Anthropic, Gemini, Bedrock, Groq, OpenRouter, Together, DeepSeek, Cloudflare Workers AI.
- **Runtime dependencies — five, total:** `effect`, `@opencode-ai/schema` (workspace; itself 64 files / 3,387 LOC, depends only on `effect`), `aws4fetch`, `@smithy/eventstream-codec`, `@smithy/util-utf8`. The last three are **Bedrock-only and droppable**.
- **Coupling to the rest of the monorepo is two import lines.** `grep` across all of `packages/llm/src` finds exactly two files importing `@opencode-ai/schema/llm` (`src/schema/ids.ts:2`, `src/schema/messages.ts:2`). Nothing imports `core`, `opencode`, `server`, or `tui`.
- **Platform coupling is one import.** The only Node/Bun builtin anywhere in `src` is `import { Buffer } from "node:buffer"` (`src/protocols/shared.ts:1`).
- Declares 20 granular `exports` subpaths (`./providers/anthropic`, `./protocols/openai-chat`, …) — per-protocol lifting is a supported shape.
- Ships its own `README.md`, `DESIGN.md` (1,100+ lines), `AGENTS.md`, and a runnable `example/tutorial.ts`.

**The one real tax: Effect-TS.** `packages/llm` is Effect-native top to bottom — public methods return `Effect` or `Stream`, dispatch goes through `LLMClient.layer`. It is pinned to `effect@4.0.0-beta.83`, which the monorepo **patches** (`patches/effect@4.0.0-beta.83.patch`, 57 lines). Lifting means adopting a large functional-effects framework, at beta, with a local patch, as a load-bearing dependency of the harness core. That is the whole cost of the lift, and it is not small.

### Local models (Ollama / vLLM / OpenAI-compatible)

[inferred from reading code] `packages/llm` contains **zero** references to Ollama, vLLM, LM Studio, or llama.cpp — deliberately. Local endpoints are reached through the generic adapter:

`src/providers/openai-compatible.ts:9-36` — `configure({ baseURL, apiKey? })`, auth typed `ProviderAuthOption<"optional">`. Arbitrary base URL, optional key. Named profiles (`groq`, `cerebras`, `deepseek`, `fireworks`, `togetherai`, `baseten`, `deepinfra`) are thin `define()` wrappers over the same call. Ollama/vLLM are configuration, not code. New endpoint documented as "5-15 lines" [doc-claim, `packages/llm/README.md`].

### models.dev — runtime network dependency, but **not in the liftable layer**

- **`packages/llm` does not touch models.dev.** `DESIGN.md:637` states models.dev is a *release-time* source; the README says "Capability/catalog metadata lives outside this low-level package."
- **`packages/core` fetches it at runtime.** `packages/core/src/models-dev.ts:176` — `HttpClientRequest.get(\`${source}/api.json\`)`, where `source = Flag.OPENCODE_MODELS_URL || "https://models.opencode.ai"` (line 160 — **their own mirror**, not `models.dev` directly). Line 250: forked background refresh on `Schedule.spaced("60 minutes")`, disk-cached under a cross-process file lock, escape hatch `OPENCODE_DISABLE_MODELS_FETCH`.
- `packages/opencode` additionally vendors a **build-time snapshot** (`packages/opencode/script/generate.ts:10`).

Net: the registry is a runtime network dependency of the product, and **not** a dependency of the layer worth lifting.

---

## 2. Tool-grant model — harness holds the tools, and the default policy is inert

### Who holds the tools

[inferred from reading code] **The harness, unambiguously.** The model holds nothing; it emits a name and arguments, and the harness resolves them.

- **v2:** `packages/core/src/tool/registry.ts:106-122` — `materialize(permissions)` returns `{ definitions, settle }`. `settle(input)` looks up `registrations.get(input.call.name)` and, on a miss, returns `{ result: { type: "error", value: \`Unknown tool: ${name}\` } }` — an error string, not an execution. Lines 60-61 add a **staleness check**: if the registration identity differs from the one advertised for that turn, the call is rejected as `Stale tool call`. A real chokepoint, better than most harnesses have.
- **v1 (shipping):** `packages/opencode/src/tool/registry.ts:286-335` builds the advertised list; `packages/opencode/src/session/llm/request.ts:208-214` is the **single filter point**:

```ts
function resolveTools(input) {
  const disabled = Permission.disabled(Object.keys(input.tools),
    Permission.merge(input.agent.permission, input.permission ?? []))
  return Record.filter(input.tools, (_, k) => input.user.tools?.[k] !== false && !disabled.has(k))
}
```

### Can the tool set be reduced to exactly one tool from configuration?

[inferred from reading code] **Yes, two independent ways**, both visible above: a permission rule of `{pattern: "*", action: "deny"}` per tool removes it from the advertised set (`Permission.disabled`, `packages/opencode/src/permission/index.ts:204-214`), *and* a per-request `user.tools[name] = false` map suppresses it. v2 does the same at `packages/core/src/tool/registry.ts:112-113` via `whollyDisabled`.

### Is there a permission layer, and is it on by default?

**There is a good one, and it is switched off in the shipped configuration. This is the finding, not a feature.**

The engine defaults correctly. `packages/opencode/src/permission/index.ts:28-38` (and `packages/core/src/permission.ts:76-86`): when no rule matches, `evaluate()` returns `action: "ask"`. v2 goes further — `packages/core/src/permission.ts:15` sets `missingAgentPermissions = [{action:"*", resource:"*", effect:"deny"}]`, fail-closed if the agent cannot be resolved.

Then the shipped agent definition overrides it. `packages/opencode/src/agent/agent.ts:119-136`:

```ts
const defaults = Permission.fromConfig({
  "*": "allow",
  doom_loop: "ask",
  external_directory: { "*": "ask", ...whitelist },
  question: "deny",
  plan_enter: "deny",
  plan_exit: "deny",
  read: { "*": "allow", "*.env": "ask", "*.env.*": "ask", "*.env.example": "allow" },
})
```

Because `evaluate()` resolves by `findLast`, the leading `"*": "allow"` governs every action not specifically re-listed. **Bash, edit, write, apply_patch, webfetch, task, skill, and every MCP tool run without approval by default.** Only the doom-loop guard, out-of-whitelist filesystem access, and `.env` reads prompt out of the box.

[doc-claim, corroborating] `packages/web/src/content/docs/tools.mdx:8`: *"By default, all tools are enabled and don't need permission to run."*

The `"ask"` default is inert in the shipped product — but not inert *in the mechanism*: a user config of `{"permission": {"*": "ask"}}` merges after `defaults` (`agent.ts:145-150`, `Permission.merge(defaults, …, user)`) and wins under `findLast`. **The policy engine is sound and the shipped policy is permissive.** For a deny-by-default harness this is a config change, not a code change — but it must be made deliberately, and nothing in the product will remind you.

Also: `--auto` (documented, `permissions.mdx:22-38`) globally converts every `ask` to `allow`, leaving only explicit `deny` standing; and `packages/opencode/src/permission/index.ts:145-151` lets a single "always" reply write durable project-scoped allow rules.

### Adversarial: can the model reach an action outside the registered tool set?

Four routes, ranked by relevance to an inverted-principal design:

**(a) Self-registering tools via the filesystem — the serious one.**
`packages/opencode/src/tool/registry.ts:178-192`:

```ts
const dirs = yield* config.directories()
const matches = dirs.flatMap((dir) =>
  Glob.scanSync("{tool,tools}/*.{js,ts}", { cwd: dir, absolute: true, dot: true, symlink: true }))
...
const mod = yield* Effect.promise(() => import(pathToFileURL(match).href))
for (const [id, def] of Object.entries(mod)) {
  if (!isPluginTool(def)) continue
  custom.push(fromPlugin(id === "default" ? namespace : `${namespace}_${id}`, def))
}
```

`config.directories()` (`packages/opencode/src/config/paths.ts:23-41`) includes the **project's own `.opencode/` directory**, walked up from cwd. Any `.opencode/tool/*.ts` in the working tree is dynamically `import()`ed and becomes a registered tool with an arbitrary `execute()`. The model has `write` and `edit` with default-allow. It can author its own tool, and — given a restart or instance-state rebuild — the harness will load and advertise it. Note `symlink: true`, which widens this further. This is a documented product feature ("Custom tools ... can execute arbitrary code" — `tools.mdx:315`), not a bug. **For a design premised on one path for tool calls through a chokepoint the model cannot see or edit, this is a direct contradiction: the registry is writable from inside the sandbox.** Mitigable (`OPENCODE_DISABLE_PROJECT_CONFIG=1`, plus an `edit` deny on `.opencode/**`), but on by default.

**(b) MCP servers auto-connect and their tools are advertised unconditionally.**
`packages/opencode/src/mcp/index.ts:374,514` — servers from config connect unless `enabled === false`. `packages/opencode/src/session/tools.ts:390-410` iterates `mcp.tools()` and adds every one to the advertised set, each gated by `ctx.ask({ permission: key, patterns: ["*"] })` — which is `allow` under the default ruleset. Combined with (a), config is a writable surface that extends the tool set.

**(c) The shell tool is a general-purpose escape by construction.**
`packages/opencode/src/tool/shell.ts` parses commands with tree-sitter to derive permission patterns (`ask()` at 263-291, `BashArity` at `packages/opencode/src/permission/arity.ts`). Sophisticated, and irrelevant when the effective rule is `allow`. Even with `bash: "ask"`, static parsing of shell is a best-effort classifier, not a boundary.

**(d) Code mode — present but genuinely off.**
`packages/opencode/src/tool/code-mode.ts` exposes an `execute` tool running a confined interpreter over MCP tools. Gated behind `flags.experimentalCodeMode` (`registry.ts:113-114`), catalog permission-filtered (`code-mode.ts:210`). Declared, not a live hole.

Environment surface: `OPENCODE_PERMISSION`, `OPENCODE_CONFIG`, `OPENCODE_CONFIG_CONTENT`, `OPENCODE_CONFIG_DIR`, `OPENCODE_DISABLE_PROJECT_CONFIG`, `OPENCODE_SERVER_PASSWORD` (`packages/core/src/flag/flag.ts:19-76`). These are parent-process inputs, so a parent harness controls them — but any subprocess the model spawns via bash inherits and can override them for *its* children.

---

## 3. Loop separability — headless yes, subordinate-returning-proposals no

### Documented programmatic entry points

[doc-claim + inferred from reading code] **Several, first-class:**

- **`@opencode-ai/sdk`** — the only publicly published package in the monorepo (`packages/sdk/js`, MIT, v1.18.13, `files: ["dist"]`). Documented at `packages/web/src/content/docs/sdk.mdx`.
- **`opencode serve`** — headless HTTP server. Generated OpenAPI surface (`packages/sdk/openapi.json`) exposes ~80 routes including `/session`, `/event` (SSE), `/permission`, `/api/permission/request`, `/experimental/tool`, `/experimental/tool/ids`, `/config`.
- **`opencode run`** — one-shot headless CLI (`packages/opencode/src/cli/cmd/run/`).
- **ACP** — Agent Client Protocol support (`packages/opencode/src/acp/`, `@agentclientprotocol/sdk@0.21.0`), including `acp/permission.ts` and `acp/tool.ts`.

**But the SDK is out-of-process by design.** `packages/sdk/js/src/server.ts:35-40` shells out: `launch("opencode", ["serve", ...])` and scrapes stdout for `opencode server listening`. You drive a spawned binary over HTTP + SSE. Real separability from the TUI — but **not an in-process library**. The loop, the SQLite store, the event bus, and the tool registry all live inside the child.

### Separable from the TUI?

[inferred from reading code] **Yes — the TUI is one of several clients.** `flags.client` is `"cli" | "app" | "desktop" | ...` (`registry.ts:202`); separate `packages/tui` (31.7k LOC), `packages/app` (130k LOC web), `packages/desktop` (Electron), `packages/session-ui`. The loop lives in `packages/opencode/src/session/` (`prompt.ts`, `processor.ts` 718 LOC, `llm/`) and `packages/core/src/session/runner/`. No TUI imports in the loop.

### Can a parent drive it one turn at a time, returning proposals rather than executing?

**No, not without surgery.** [inferred from reading code]

- The v2 loop's public interface is `run({ sessionID, force }) → Effect<void>` (`packages/core/src/session/runner/index.ts:20-26`), documented as *"Drains eligible durable work."* A **durable-drain** API over persisted session state, not a step function. It owns its own continuation: `runner/llm.ts` checks `[x] Reload projected history and start the next explicit provider turn after local tool results`.
- Tool execution is **inside** the loop, not returned from it. The permission `assert`/`ask` fires *during* tool settlement (`packages/opencode/src/session/tools.ts:79-89`), after the call has been accepted and recorded. The parent's leverage is an **approval gate on an in-flight execution**, not a proposal returned for the parent to execute. Materially different control shape from the one being designed.
- Everything is welded to durable state: SQLite via drizzle, an event bus, projected message history, snapshots. There is no stateless "here is a context, give me one proposal" seam.

**What a parent realistically gets today:** spawn `opencode serve`, create a session, POST a prompt, subscribe to `/event`, answer `/permission` requests as they arrive — *approve/deny out-of-band while the child executes*. Achieving *model holds no tools, parent executes everything* means reducing the tool set to a stub and reimplementing execution on your side — at which point you are using opencode as a very heavy protocol client.

### Maturity caveat on v2 — the cleanest code is the least finished

`packages/core/src/session/runner/llm.ts:44-88` is a checklist in a doc comment, and the unchecked items are load-bearing:

> `[ ] Resolve policy-filtered built-in, MCP, plugin, and structured-output tool definitions.`
> `[ ] Bound provider retries and repeated identical tool calls.`
> `[ ] Mark busy, retrying, idle, interrupted, or terminal-failure status durably.`
> `[ ] Honor interruption and reject stale work after runtime attachment replacement.`

And `packages/core/src/tool/builtins.ts:26-29`: *"TODO: Port the remaining launch-follow-up leaves deliberately: edit fuzzy parity, task, LSP, repo_clone, repo_overview, plan_exit, and Rune/code mode."*

So the architecture most worth lifting (`core/tool/registry.ts` + `packages/llm`) is the **in-progress rewrite**, and what ships is the 176k-LOC v1 monolith on the Vercel AI SDK. **A fork inherits the migration.**

---

## 4. Adoption read

| Axis | Finding |
|---|---|
| **Licence** | MIT throughout — root `LICENSE` ("Copyright (c) 2025 opencode"), and every workspace `package.json` checked. No CLA in `CONTRIBUTING.md`. Clean. |
| **Maintainership / bus factor** | 1,031 all-time authors. All-time top: Dax Raad 1,965 · Adam 1,416 · `opencode-agent[bot]` 1,339 · Kit Langton 1,081. **Last 90 days (3,068 commits): `opencode-agent[bot]` 870 (28%) · Kit Langton 435 · Aiden Cline 241 · Brendan Allan 186 · Shoubhit Dash 181 · Adam 152 · Frank 147 · Luke Parker 123 · Dax Raad 86.** Two readings. Healthy: no single human above ~15% recently; the founder has visibly delegated. Unhealthy: **the largest single committer is a bot, by a factor of two** — this repo is substantially written by its own product, a novel and unquantified maintenance-quality risk. Commercial backer: Anomaly Co. (formerly SST), with a hosted "zen" inference product monetizing it. |
| **Release discipline** | Very high cadence, near-continuous. 1,020 `v*` tags. v1.18.9 → .13 spans **2026-07-28 to 2026-08-04** — five patch releases in eight days, two on the same day. v1.0.0 was 2025-10-31; v1.15.0 2026-05-15; v1.17.0 2026-06-10. Latest v1.18.13 with 37 binary assets. **Fast-moving, not stable**: a fork rebases against a target that changes daily, and the v1→v2 rewrite is landing under a patch-version stream. |
| **Dependency weight** | Heavy at product level, light at `llm` level. `bun.lock` is **871 KB**. `packages/core` alone pulls ~20 `@ai-sdk/*`, drizzle+SQLite, OpenTelemetry (4 pkgs), `@npmcli/arborist`, three AWS/Google auth SDKs, and Effect. **14 patched dependencies** in `patches/`, including `@modelcontextprotocol/sdk` (33 KB patch), `@ai-sdk/mistral` (27 KB), and `effect` itself. Patching your MCP SDK and your effect runtime is a real fork-maintenance signal. |
| **Compiled / native deps** | Several: `@lydell/node-pty` (with a `postinstall` fixup, `fix-node-pty`), `@parcel/watcher` (8 platform prebuilds), `web-tree-sitter` + `tree-sitter-bash` + `tree-sitter-powershell`, `@silvia-odwyer/photon-node` (patched), `protobufjs`, `electron`. `trustedDependencies` names eight postinstall-running packages. |
| **Repo size** | 344 MB packed git · 137 MB working tree · GitHub reports 436 MB. ~700k LOC of TS/TSX across 34 workspace packages. |
| **Platform assumptions** | **Bun is mandatory** (`packageManager: bun@1.3.14`; Bun-specific `#db`/`#sqlite`/`#pty`/`#fff` conditional imports; `bun test`). Ships as **cross-compiled single binaries** for 12 targets: linux/darwin/win32 × x64/arm64, plus musl and explicit non-AVX2 variants. Web UI embedded into the binary at build time. |
| **Open-issue health** | **4,889 open issues**, 24,714 forks, 193,362 stars. A **60-day stale-bot auto-closer** (`.github/workflows/close-issues.yml`, daily cron) means open-issue count understates the real backlog and **closed-issue status is not evidence of a fix**. |

### Local-model and tool-call reliability — the densest failure cluster, still open

- `#20995` (2026-04-04, **35 comments, open**) — Gemma 4 tool calling fails via Ollama OpenAI-compatible API; streaming `tool_calls` not recognized.
- `#33959` (2026-06-25, open) — *"OpenCode Desktop does not execute valid OpenAI tool calls from qwen3-coder:30b (Ollama)"* — **the exact model and serving stack from shd-007.**
- `#39164` (2026-07-27, open) — MCP tools not sent to local OpenAI-compatible models (empty tools array).
- `#26412` (2026-05-08, 10 comments, open) — custom OpenAI-compatible provider: `"Expected 'function.name' to be a string"` on streaming tool-call chunks.
- `#34126` (2026-06-26, open) — OpenAI Chat parser treats a standalone `</think>` before `tool_calls` as assistant text.
- `#36316`, `#35689`, `#40176` (open) — agent loop stops after first tool call on Kimi / DeepSeek / deepseek-v4-flash; `reasoning_content` dropped in multi-step.
- `#39357`, `#38854`, `#37543`, `#34988` (open) — Ollama connectivity/hangs/garbled output.

Consistent pattern: **failures cluster at the OpenAI-compatible streaming-tool-call parser**, recurring across models and across the v1 AI-SDK path.

---

## 5. Dedup resolution — correcting finding #228's opencode citation

[demonstrated by them, with artifact — GitHub API] **Both halves of the recorded framing need correcting.**

- **#20719 is CLOSED, `state_reason: not_planned`, 2026-07-04.** It was **not fixed**. It was auto-closed by the stale bot: the only maintainer-side comment is `github-actions[bot]` saying *"To stay organized issues are automatically closed after 60 days of no activity."* Zero human replies.
- The bot's earlier triage comment names two relatives:
  - **#14972** — *"Agent stops after tool execution with OpenAI-compatible providers (Gemini, LiteLLM)"* — closed `completed` 2026-04-02. But the triage bot's own note reads: *"Closed but apparently still affects v1.3.13."*
  - **#20669** — *"Default agent is brittle against local OpenAI-compatible tool-call quirks"* — also **auto-closed `not_planned`**, 2026-07-03.

**Interpretation.** Citing #20719 as a discrete bug is the wrong altitude in both directions. It is not a fixed bug (nobody fixed it), and it is not purely architectural either. The evidence supports something more precise, aligned with what shd-007 measured directly: **`finish_reason` / streaming-tool-call handling in the OpenAI-compatible path is a persistent, unresolved defect class in this harness** — one fix landed (#14972), the class did not close, three successors were auto-closed unread, and ten-plus siblings are open now. shd-007's amended reading ("prompt/template alignment, of which the tool-call contract is one expression") is compatible; the opencode-specific addition is that **the parser layer itself is also implicated**, not only the prompt (see #34126, #26412, #35689 — all parser-side).

Forward-looking wrinkle: `packages/llm`'s from-scratch `openai-compatible-chat` protocol is a **plausible fix to exactly this class**, and it postdates every issue above (first commit 2026-05-08). Whether it actually fixes it is unverified — the recorded cassettes cover Groq/OpenRouter/Together, **not Ollama, not vLLM, not LiteLLM**.

**Alias flag for distillation:** if literature or adjacent scouts surface work on *"tool-call protocol normalization"*, *"structured-output enforcement / constrained decoding"*, or *"chat-template–vs–system-prompt tool convention conflict,"* that is the same object as this cluster under a different name.

---

## 6. Buy-before-build evidence

**The need:** rules engine as parent, LLM as subordinate holding no tools, exactly one proxied path for tool calls through a chokepoint the model cannot see or edit.

| Our need | opencode's coverage | The gap |
|---|---|---|
| Provider abstraction, 4+ families incl. local | **Covered, well** — `packages/llm`, 9.5k LOC, protocol-level, cassette-tested | Local endpoints untested in the new layer; Effect-TS beta is the tax |
| Model holds no tools; harness holds them | **Covered architecturally** — registry-side `materialize`/`settle`, unknown-tool → error, staleness check | — |
| One path for tool calls | **Nearly covered, then broken by config** | `.opencode/tool/*.ts` dynamic import (`registry.ts:178-192`) lets the model author new tools; MCP auto-connect adds more |
| Chokepoint the model **cannot see or edit** | **Not covered** | The policy is a config file inside the model's writable working tree, with `edit` default-allow. Nothing is out-of-band. |
| Deny-by-default policy | **Mechanism yes, default no** | `"*": "allow"` in `agent.ts:120` — one config line to fix, but you must know to |
| Parent drives one turn, gets proposals back | **Not covered** | Loop is a durable self-continuing drain; permission fires mid-execution, not pre-execution |
| Headless / programmatic | **Covered** — SDK, `serve`, `run`, ACP | Out-of-process over HTTP+SSE; not an in-process library |

**Cost and licence.** Zero money. MIT, no CLA. Operational burden is the real cost: Bun toolchain, 34-package monorepo, 14 patched dependencies (including MCP SDK and effect), native deps with postinstall hooks, ~5 patch releases/week to rebase against.

**Lock-in and exit.** Sharply different by subtree:
- `packages/llm` — **very low lock-in.** Five deps, two cross-package import lines, one Node builtin. The real commitment is Effect-TS, not opencode.
- Forking the product — **high lock-in.** Inherits an unfinished v1→v2 migration, both provider stacks simultaneously, Bun, and the patch set.

**Composability.** `packages/llm` composes well with anything Effect-tolerant. `packages/core/src/tool/registry.ts` (147 lines) is a good *pattern* to reimplement rather than a component to import — welded to Effect layers, the event bus, and `ToolOutputStore`.

**The eighty-percent case, and the uncovered remainder.** opencode covers most of what is needed and misses the load-bearing part. It gets the principal/subordinate *inversion* right — the harness genuinely holds the tools and the model genuinely holds none. What it lacks is the **unforgeability** property: the policy lives in a file the agent can write, the tool registry can be extended from that same directory, the shipped default is allow-everything, and the approval hook fires after the call is accepted rather than returning a proposal for the parent to decide on. **Those four are precisely the properties the design exists to provide. The remainder is not a feature gap — it is the entire thesis.**

---

## 7. Cites

```
type: repo    | ref: https://github.com/anomalyco/opencode | title: opencode — AI coding agent
              | org: Anomaly Co. (formerly SST) | author: Raad, Dax; Langton, Kit; Cline, Aiden
              | year: 2025 | surface: active-dev
              | note: canonical; sst/opencode redirects here. MIT. Pinned at 66fdd51 (dev, 2026-08-05).
type: repo    | ref: packages/llm/ @66fdd51 | title: @opencode-ai/llm — schema-first LLM core
              | org: Anomaly Co. | year: 2026 | surface: active-dev
type: docs    | ref: packages/llm/README.md, packages/llm/DESIGN.md @66fdd51
              | title: @opencode-ai/llm architecture and provider contract | org: Anomaly Co. | surface: active-dev
type: repo    | ref: packages/core/src/tool/registry.ts @66fdd51 | title: v2 ToolRegistry — materialize/settle
              | org: Anomaly Co. | surface: active-dev
type: repo    | ref: packages/opencode/src/agent/agent.ts#L119-L136 @66fdd51
              | title: shipped default agent permission ruleset ("*": "allow") | org: Anomaly Co. | surface: active-dev
type: repo    | ref: packages/opencode/src/tool/registry.ts#L178-L192 @66fdd51
              | title: dynamic import of .opencode/tool/*.{js,ts} | org: Anomaly Co. | surface: active-dev
type: repo    | ref: packages/core/src/models-dev.ts#L160-L250 @66fdd51
              | title: runtime models registry fetch (models.opencode.ai, 60-min refresh) | org: Anomaly Co. | surface: active-dev
type: docs    | ref: https://opencode.ai/docs/permissions | title: Permissions | org: Anomaly Co. | surface: active-dev
type: docs    | ref: https://opencode.ai/docs/tools | title: Tools ("By default, all tools are enabled and don't need permission")
              | org: Anomaly Co. | surface: active-dev
type: docs    | ref: https://opencode.ai/docs/sdk | title: SDK — type-safe JS client for opencode server
              | org: Anomaly Co. | surface: active-dev
type: repo    | ref: https://github.com/anomalyco/opencode/issues/20719 | title: Agent loop stops after first LLM call
              with @ai-sdk/openai-compatible + LiteLLM (finish_reason: stop) | year: 2026 | surface: active-dev
              | note: CLOSED not_planned 2026-07-04 by 60-day stale bot — NOT fixed.
type: repo    | ref: https://github.com/anomalyco/opencode/issues/20669 | title: Default agent is brittle against local
              OpenAI-compatible tool-call quirks | year: 2026 | surface: active-dev | note: CLOSED not_planned, stale bot.
type: repo    | ref: https://github.com/anomalyco/opencode/issues/14972 | title: Agent stops after tool execution with
              OpenAI-compatible providers | year: 2026 | surface: active-dev | note: closed "completed"; triage bot records
              it still affected v1.3.13.
type: repo    | ref: https://github.com/anomalyco/opencode/issues/20995 | title: Gemma 4 tool calling fails via Ollama
              OpenAI-compatible API | year: 2026 | surface: active-dev | note: OPEN, 35 comments.
type: repo    | ref: https://github.com/anomalyco/opencode/issues/33959 | title: Desktop does not execute valid OpenAI
              tool calls from qwen3-coder:30b (Ollama) | year: 2026 | surface: active-dev | note: OPEN; same model as shd-007.
```

**Source signal:** `external-scan` (owner-directed single target).
**Lens rationale:** the theme is the inverted-principal workflow harness; opencode is the highest-adoption OSS harness with a first-party provider layer and a harness-side tool registry, evaluated as a fork/lift base.

---

## 8. Surface coverage report

**Searched:** full-history clone (15,311 commits, 1,020 `v*` tags) read at pin; complete `packages/llm`, `packages/core/src/{tool,permission,session,models-dev}`, `packages/opencode/src/{tool,permission,session,agent,config,mcp,acp,cli}`; `packages/sdk` + generated `openapi.json`; all 34 workspace `package.json` files; `patches/`; `.github/workflows/`; checked-in docs (`packages/web/src/content/docs/{permissions,tools,sdk}.mdx`); GitHub REST for repo metadata, four targeted issue lookups, four open-issue keyword searches.

**Deliberately skipped, declared as holes:**
- `packages/app` (130k LOC web UI), `packages/desktop` (Electron), `packages/tui`, `packages/ui`, `packages/session-ui`, `packages/console`, `packages/stats`, `packages/storybook` — presentation layers, out of scope.
- `packages/enterprise`, `packages/identity`, `packages/containers`, `packages/slack`, `packages/function` — hosted-product surfaces. **`packages/enterprise` (1,600 LOC) may contain policy or auth material relevant to a chokepoint design; not read.** Named as a hole.
- `packages/codemode` (11.2k LOC) — read only its consumer (`tool/code-mode.ts`). The sandbox's actual confinement properties are **unverified**; off by default.
- `packages/protocol`, `packages/httpapi-codegen`, `packages/http-recorder`, `packages/effect-*` — plumbing.
- **Nothing was built, installed, or run.** No test suite executed, no binary launched, no live model call. Every capability statement is a static code read or a vendor doc claim.
- Did not read the 4,889 open issues — four targeted keyword searches (`ollama`, `local model`, `finish_reason`, `tool_calls`) at 10 results each. Adjacent failure classes (auth, context management, compaction) unsampled.
- The v2 `packages/core` HTTP surface and `packages/sdk-next` (342 LOC) were not read; if v2 exposes a cleaner programmatic entry point than the v1 SDK, that was missed.

**Cold-leg record.** Single-target assignment; the entire target was cold (opencode has no Unimatrix node, appearing only as an unstructured citation string inside #228). Cold reading that yielded beyond the brief: (i) the org rename to `anomalyco`, which invalidates the brief's `ref`; (ii) the existence of `packages/llm` as a from-scratch protocol layer — a different and better answer to Q1 than the "does it use Vercel AI SDK" question anticipated; (iii) the `.opencode/tool/*.ts` dynamic-import path, found by chasing `config.directories()` rather than by looking for escape hatches; (iv) the stale-bot close policy, which retroactively changes how every "closed" opencode issue in our graph should be read. **Dry:** searched `packages/llm` and `packages/core` for Ollama/vLLM/llama.cpp-specific handling — genuinely nothing, by design; searched for a "propose-only" or dry-run mode across the loop — nothing.

**Theme-revision signal.** One, small. Our watchlist convention appears to record OSS harness evidence as bare issue numbers (`opencode #20719`). That convention silently loses the two facts that mattered most here: **which org owns the repo** (it changed) and **why an issue closed** (`not_planned` by stale bot ≠ `completed`). Recommend the watchlist schema require `org/repo#N` plus `state_reason` for any issue citation, and that a "closed" issue never be read as "fixed" without checking the close reason. Not urgent; does not alter this scan.

---

## 9. Flags for triage

1. **The brief's `ref` is stale.** `sst/opencode` → `anomalyco/opencode`. Correct before any node is filed.
2. **Two candidates hide inside one target, and they deserve separate verdicts.** `packages/llm` (9.5k LOC, 5 deps, near-zero coupling) and the opencode product (700k LOC, Bun, 14 patches, mid-rewrite) are not the same adoption decision.
3. **Inert-by-default control, confirmed and located.** `packages/opencode/src/agent/agent.ts:120` — `"*": "allow"`. The engine defaults to `ask`; the shipped agent overrides it. Corroborated by the vendor's own docs. Second instance of the wfh-005 inert-control position (#196), after ruflo (#200).
4. **The chokepoint is writable from inside the sandbox.** `registry.ts:178-192`. Most directly adverse to the design premise, and a documented feature — so it will not be fixed upstream.
5. **The clean architecture is the unfinished one.** The v2 registry and runner carry explicit unchecked TODOs including policy-filtered tool resolution. Adopting them means adopting a migration in flight, shipping under patch-version tags.
6. **`packages/llm` is a plausible unverified fix to finding #228's failure class** — first-party protocol parsers, cassette-tested. Its cassettes cover no local serving stack. Well-bounded proof-goal: run `packages/llm`'s `openai-compatible-chat` protocol against the shd-007 Ollama/qwen3-coder envelope. Not run; no claim about the outcome.
7. **Bot-authored majority.** `opencode-agent[bot]` is the largest single committer of the last 90 days at 28%. An unquantified maintenance-quality risk for a fork base, not a judgement.
8. **Nothing above is `proven`.** No artifact, no execution. `claimed` at best.

**Clone** left at `/tmp/claude-1000/-workspaces-arch-research/47761aa7-86fa-4e9b-8489-ace4c4e1ab7c/scratchpad/opencode` (pinned at `66fdd51`) for re-verification of any line reference.
