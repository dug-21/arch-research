# verify-V1-openshell.md — targeted verification: policy hot-reload latency and atomicity (merge round-two trigger #1)

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · **agent_id:** `wfh-007-v1-scout` · targeted verification (CHALLENGE-shaped, against S1's C1)
**Read-only; no Unimatrix writes; nothing cloned, installed, built, or run.** Everything below is `claimed`; every number is theirs, not ours.

WebSearch was not needed. `gh api` against `NVIDIA/OpenShell` worked throughout — issues, code search, base64 content reads — and `WebFetch` worked on `code.claude.com`. **The hole S1 declared is closed on four of five axes and partly on the fifth, and the answer is not the one the trigger expected.**

Repo state at read (2026-08-20): 8,279★, 1,227 forks, 457 open issues, 119 open PRs, Apache-2.0, latest release **v0.0.109** (2026-08-19), last push 2026-08-20T01:15Z. Still `0.0.x`. Alpha holds.

---

## 1. Latency

### 1a. Steady-state proxy hop — **published, benchmarked, and fast** `[demonstrated — with artifact, by a third party]`

S1 said no figures are published. There are, in issue **#2219**, with a reproducible harness, controls, and medians over 30 repetitions per cell.

| Path | before | after `TCP_NODELAY` fix | host loopback floor |
|---|---|---|---|
| L4 passthrough, keep-alive marginal | 43.58 ms | **0.27 ms** | 0.06 ms |
| **L7 terminate + inspect**, keep-alive marginal | 44.49 ms | **0.45 ms** | 0.06 ms |
| Single-shot, 1 KB response (incl. TLS connect) | 62.64 ms | 14.66 ms | — |

The number that matters, verbatim:

> "the entire L7 stack (TLS termination, header parse, **policy eval**, OCSF emit, credential rewrite) measures on the close order of **200 µs per request** (effectively 0) against L4 passthrough"

Controls: plain `docker run` with no OpenShell proxy is 15–20 ms single-shot; the ~44 ms was a Nagle × delayed-ACK stall, not inspection cost, and it inverted with payload size (1 KB → 63 ms, 100 KB → 15 ms — the classic signature). Fixed by #2208 / #2220 (both closed).

**Grade.** Reproducible harness published on a branch, one-command ladder, analyser included — stronger than a README claim, but **not demonstrated by us**, and **#2577 is open**, proposing a `clippy::disallowed_methods` lint to *enforce* `TCP_NODELAY` at all TCP dial sites, which implies coverage on main is not provably complete. Treat 0.45 ms as the figure for the benchmarked egress path, not a guarantee across every hop.

**The steady-state proxy hop is not the constraint. Policy evaluation costs ~200 µs.**

### 1b. The reload path — **seconds, not milliseconds** `[inferred from reading + asserted]`

No end-to-end `policy set → enforcement` benchmark is published. What bounds it, from three independent reads:

- **Default settings-poll interval is 10 s.** `crates/openshell-sandbox/src/lib.rs`: `std::env::var("OPENSHELL_POLICY_POLL_INTERVAL_SECS")…unwrap_or(10)`. Env-tunable; the repo's own e2e override image sets it to `1`.
- **Docs assert ~5 s**, twice: *"Changes propagate within about 5 seconds by default"* and *"Provider, model, and timeout changes are picked up by running sandboxes within about 5 seconds by default. No sandbox recreation is required."* `[asserted — vendor docs]`. Five seconds is the mean of a uniform 10 s tick — consistent.
- **In-code corroboration**, `policy_local.rs`: `RELOAD_WAIT_MIN_FLOOR = 500ms`, commented *"500ms is well below typical supervisor poll latency."*

Propagation is a gateway→supervisor **watch-notify plus poll** loop (the watch bus wakes the poller; the 10 s tick is fallback), so the expected case is watch-driven and 10 s is a ceiling. Corroborating history: the Python e2e this replaced was *"flaky due to hard-coded 90 s poll timeouts"*; the current Rust e2e passes `--timeout 120`.

There **is** a real synchronous barrier: `openshell policy set|update --wait`, exit codes **0 = loaded, 1 = validation failed, 124 = timeout**.

**Order of magnitude: single-digit seconds at defaults, tunable toward ~1 s. Not a per-tool-call primitive as shipped.**

---

## 2. Atomicity — the finding that decides the question

**Commit is transactional at the gateway.** The gateway validates the *complete effective candidate* — sandbox policy composed with provider policy — **before persistence**. A preflight rejection returns `FAILED_PRECONDITION` and, verbatim, *"leaves the currently active policy unchanged regardless of failure mode because the candidate is never persisted or distributed."* Multiple `policy update` flags in one command apply as *"one atomic merge batch and persist at most one new revision."* `UpdateConfig`'s atomic branch is a CAS retry loop.

**Propagation is eventually-consistent with an explicit, readable ack.** The gateway holds a *desired* revision; the supervisor reports `ReportPolicyStatus: status=loaded(v)`; the gateway tracks *current*. Convergence is observable and gateable — genuinely good design, and it means a caller can block on convergence rather than guess.

### ⚠ In-flight connections are severed, deliberately

The load-bearing sentence, quoted in full from `docs/sandboxes/policies.mdx`:

> "When a hot reload changes rules, the supervisor publishes a new **policy generation** and **closes connections pinned to the previous generation**. This includes HTTP keep-alive tunnels, `tls: skip`, non-HTTP payloads, HTTP upgrades such as WebSocket, and **long-lived response streams such as SSE**. Most clients reconnect automatically, and the next connection or request is evaluated against the current policy. A parsed WebSocket relay closes with code `1012` when its attached policy generation becomes stale."

So "do old and new both apply?" — **no**, the generation switch is clean for new connections. "What happens to in-flight?" — **they die.** Not "the old policy continues for them." **Any mid-turn reload cuts every open stream through the proxy.**

**Windows where *neither* policy applies exist, three of them:**

1. **Quarantine (the default).** If a candidate reaches a supervisor and fails *runtime* validation, `policy_validation_failure_mode = "fail_closed"` (default) means the supervisor *"publishes a quarantine generation, denies new egress, and closes connections pinned to the previous generation. The previous policy is not active."* A later valid policy exits quarantine automatically. **A bad reload is a total egress blackout, not a rollback.**
2. **`retain_last_valid`** is the opt-out, explicitly framed as availability-over-security. Gateway-wide and operator-only — *"Individual sandboxes cannot override it"* — and still fails closed with no prior valid generation.
3. **#1942, open, `state:stale`** — startup stale-generation race; an allowed request can observe a stale generation and get a transient **403**. Mitigated at startup by deferring `accept()` until symlink resolution; the code comment names the class (*"the race where an in-flight request observes a generation transition during the OPA engine reload"*). Product fix undecided, DoD unticked.

**Two convergence-stall bugs shipped, both fixed within ~2 weeks:** #2517 (atomic commit did not wake watchers → connected sandbox blocked indefinitely) and #2518 (a newer revision with an unchanged policy hash never acknowledged → desired 2 / current 1, permanent non-convergence). Exactly the class of bug that makes an ack-gated design unsafe, and both were real in a shipped release (v0.0.91).

**And ack does not imply traffic flows.** #2752 (closed 2026-08-19): reporter observed `status=loaded` for the new revision and matching traffic still rejected — root cause a *separate SSRF engine* denying after the OPA allow (§3). **#2514 remains open:** allowed `NET:OPEN` + allowed `HTTP:POST` followed by `NET:FAIL`, intermittent, no policy denial.

---

## 3. Granularity of the reloadable set

**Locked at creation — confirmed verbatim**, docs and the e2e's own comment (*"updates retain the same startup-only filesystem, landlock, and process fields"*):

> "A policy has static sections `filesystem_policy`, `landlock`, and `process` that are **locked at sandbox creation**… Changing them requires **destroying and recreating the sandbox**."

**Hot-reloadable:** `network_policies` and `network_middlewares` only.

**Network granularity — S1's "HTTP method + path" is confirmed and is an understatement.** The reloadable surface expresses: endpoint `host:port` with wildcard and exact selectors · **per-binary** authorization (`binaries: [/usr/bin/gh]`, resolved through `/proc/<pid>/root`) · protocol selector (`rest`, `websocket`, L4 passthrough, `tls: skip`) · **REST method + path with wildcards**, allow *and* deny, with subtree carve-outs · **GraphQL** operation and root-field matchers · **MCP `method` / `tool`** rules · generic **JSON-RPC `method`** rules · `access` levels (`read-only`/`full`), `enforce` vs advisory, credential-rewrite flags. **Not yet:** JSONPath predicates on REST bodies (#1848, open).

**A hard floor sits *beneath* the reloadable policy.** An SSRF engine evaluates *after* the OPA allow and blocks private, loopback, link-local and unspecified addresses plus protected control-plane ports. Maintainer, verbatim on #2752:

> "**Policy-advisor-generated rules deliberately cannot authorize private-address access, even after human approval.**"

An operator-declared exact hostname may resolve to private space; an agent-proposed rule may not. **A second, non-liftable ceiling, already shipped.**

### ⚠ Material correction to C1: the inference layer is NOT equally granular

It is hot-reloadable — but the unit of reload is **the whole gateway**:

> "**One provider and one model define sandbox inference for the active gateway. Every sandbox on that gateway sees the same `inference.local` backend.**"

The route surface is a **fixed per-provider allowlist** compiled into the privacy router, plus a per-provider header allowlist; it is not policy-authored and not per-sandbox. **Per-phase or per-sandbox model authority is not expressible at this layer at all.** The escape hatch: treat `api.anthropic.com` as an ordinary external host and model traffic falls under `network_policies` at full method+path granularity. So per-sandbox model control **is** reachable — through the network layer, never the inference layer. C1's row *"Inference | hot-reloadable at runtime"* is true and misleading; it should read **"hot-reloadable, gateway-global, one provider + one model."**

---

## 4. Who may call reload — **the Cluster H test does not fire on OpenShell**

The sandbox-facing API is `policy.local`, loopback-only, and its complete shipped route set is:

```
GET  /v1/policy/current
GET  /v1/denials
POST /v1/proposals                          ← submit
GET  /v1/proposals/{chunk_id}               ← status
GET  /v1/proposals/{chunk_id}/wait?timeout= ← long-poll, default 60s, min 1, max 300
```

**There is no approve or apply route.** The design statement is explicit and titled *"Non-Negotiable Trust Boundary"* (#1062):

> "The proposing in-sandbox agent can submit policy proposals and read proposal outcomes. **It cannot act as its own reviewer, directly approve or deny chunks, bypass the configured approval policy, or mutate live policy.**"
> — and under Explicit Non-Goals: "**sandbox self-approval**."

Mutation happens gateway-side over authenticated mTLS + bearer-JWT gRPC, by an operator or a control-plane reviewer that *"must evaluate structured proposal context from outside the proposing sandbox."* The agent's only affordance is to be denied with structured context, propose the narrowest rule, and **sleep on one long-lived request** (`/wait`) rather than burn tokens polling.

Note `wait_for_local_policy_to_cover` — the reload signal returned to the agent is a **semantic containment check** (does the loaded policy cover *this* proposed rule), not version equality. **That is the right primitive and it is already built.**

**The organization ceiling is in flight, not shipped.** #2109 + draft PR #2168 add gateway-managed *maximum* policies: `effective authority = sandbox policy + provider policy + credential reach + approved grants`, with `candidate effective authority <= applicable managed policy envelope`, evaluated on the fully composed live candidate immediately before sandbox creation, policy revision, proposal application, and provider change. Modes **`ask`** (all proposals pend) and **`auto`** (proposals *inside* the maximum apply automatically, at agent speed; outside-maximum rejected with a counterexample). Unmodelled authority surfaces — GraphQL, remote MCP — **fail closed** until containment lands. The PR is a net *reduction* (4,432 additions / 4,732 deletions across 83 files) because it deletes the legacy approval-mode paths. Draft, open, currently limited to single-replica SQLite storage.

**Verdict on the Cluster H test: OpenShell is the counter-example, not an instance.** The bounded party cannot lift its own boundary, cannot approve its own proposals, and cannot cross the SSRF floor even *with* human approval. What Cluster H says is usually absent is here, shipped, and architected as non-negotiable.

---

## 5. The cheap substitute — not the fallback, the *faster* instrument

The question assumed "spawn-per-phase is the only route" was the likely honest answer. **It is not.**

**Claude Code's sandbox is not a long-lived sandboxed process. It builds a fresh bwrap (Linux/WSL2) or Seatbelt (macOS) profile per Bash command**, from current settings, covering that command and all its children. **There is no "re-scope a running sandbox" problem to solve.** And the docs state the re-scope path explicitly:

> "When you edit these lists during a session, Claude Code **applies the change to the running session**, so **the next sandboxed command runs under the new paths**."

and generally:

> "Claude Code watches your settings files and reloads them when they change, so edits to most keys apply to the running session without a restart. This includes `permissions`, `hooks`… The reload covers user, project, local, and **managed** settings."

**Cost of a phase switch: one file write, effective on the next tool call.** The bwrap spawn was happening anyway. Milliseconds and in-turn — roughly **three orders of magnitude cheaper than OpenShell's ~5 s reload** — and already installed on this machine (`/usr/bin/bwrap` and `linux/landlock.h` both present).

**Granularity available today:** `sandbox.filesystem.allowWrite / denyWrite / allowRead / denyRead` (path-scoped, specificity-ordered — an exact deny holds inside a wider allow) · `network.allowedDomains` / `deniedDomains` with optional `:port` · **`deniedDomainReasons`** — a model-facing reason string delivered in the violations line, i.e. **a structured deny channel of the same shape as OpenShell's** · `excludedCommands` · unix-socket controls.

**And there is a programmatic driver.** `@anthropic-ai/sandbox-runtime` (5,016★, Apache-2.0, pushed 2026-08-19, research preview) exposes `SandboxManager`, `SandboxRuntimeConfig`, per-invocation `commandId`/`commandText` attribution, `getViolationsForCommand`, and experimental `network.tlsTerminate` + `network.filterRequest` for filtering *decrypted* requests in-process — method-and-path L7 filtering driveable from your own predicate.

**Two holes on this path, both material, neither closed:**

**(a) The ceiling may not hold where it matters most.** Managed settings are documented as highest precedence and not overridable — but the sandbox filesystem arrays specifically are documented as **merged, not overridden**: *"paths from every scope are combined, not replaced."* **Union across scopes is the opposite of a ceiling for exactly the field a phase compiler would drive.** Whether managed scope is exempt sits in an "exceptions to managed settings precedence" section not read. **Unresolved, and it is the difference between a ceiling and a suggestion.**

**(b) Cluster H fires here — twice, where it did not fire on OpenShell.**
- `dangerouslyDisableSandbox` is held by the bounded party by default: *"Claude analyzes the failure and may retry the command with the `dangerouslyDisableSandbox` parameter."* Closable via `"allowUnsandboxedCommands": false` (Strict sandbox mode), which makes the parameter *"completely ignored."*
- **Sharper, and unverified:** if `.claude/settings.json` sits under the default-writable cwd, and settings edits apply to the running session, **the agent may be able to widen its own sandbox with an Edit.** V1 did not test this and declined to — *"it is a configuration mutation, and my instructions forbid it."* **It is the single highest-value falsifier on this path, and it is the owner's call to authorize.**

**The clean contrast for the run: OpenShell has a proposal channel and no escape hatch. Claude Code has an escape hatch and no proposal channel. Neither has both.**

---

## Decision line

**On this evidence alone, phase-indexed authority is assemble-shaped — but the assembly is over Claude Code's per-command sandbox, not over OpenShell's reload path.**

OpenShell's plane is real, transactional at commit, structurally correct on authority, and richly granular at L7. It is also a **seconds-scale, eventually-consistent control loop that severs every in-flight connection on reload, including SSE**, whose default failure mode is a total egress blackout, and whose inference layer is one gateway-global knob. That is a **between-turn** instrument — excellent for a phase boundary measured in tasks, wrong for one measured in tool calls.

S1's framing — *is the hot-reload path fast enough and atomic enough to sit inside a turn* — gets the answer **no, and the blocker is connection severance rather than latency.**

The in-turn instrument is already installed and costs a file write. What remains build-shaped is the same remainder S1 named — **the compiler from a declared phase to a policy delta** — plus one thing S1 did not: **the ceiling**. OpenShell is building it (#2109, draft) and has a non-liftable floor already shipped; Claude Code's equivalent is unproven for the sandbox arrays, and the bounded party holds both the escape hatch and, possibly, the pen on its own settings file.

---

## What could not be established, and what would establish it

| # | Unclosed | What closes it |
|---|---|---|
| 1 | End-to-end wall clock for `openshell policy set --wait` | `time openshell policy update <n> --add-allow … --wait` with `OPENSHELL_POLICY_POLL_INTERVAL_SECS=1`; or the repo's own golden e2e flow, which prints "live reload" |
| 2 | **Whether `inference.local` SSE streams are severed by a *network* policy generation bump** — the crux for in-turn use | Read `crates/openshell-supervisor-network/src/l7/relay.rs` and `inference_routes`; or empirically: open a long stream, reload, observe. **Highest-value remaining OpenShell read** |
| 3 | Whether the `TCP_NODELAY` fix covers all hops on main (#2577 open) | `grep set_nodelay` across the workspace against the dial sites |
| 4 | Whether a sandbox can reach the gateway's authenticated gRPC mutation API at all (requires mTLS certs the sandbox is not issued) — `[inferred]`, not verified | Read the sandbox's issued credential set and the gateway auth path |
| 5 | Whether Claude Code's **managed** scope overrides or merges `sandbox.filesystem.*` arrays | Read "exceptions to managed settings precedence" in the settings docs |
| 6 | **Whether an agent can edit `.claude/settings.json` and widen its own sandbox mid-session** | One Edit to a sandbox key in a throwaway repo, observing whether a guard fires. **Highest-value falsifier in this writeup — owner authorization required** |

**Nothing here is demonstrated by us.** The strongest item — #2219 — is `[demonstrated with a reproducible artifact]` by an external contributor; everything else is `[asserted]` (docs, issue text) or `[inferred from reading]` (code). Firewall status for all of it: **`claimed`**.

---

## Coverage

**Searched:** `NVIDIA/OpenShell` issues via `search/issues` on `reload` (101 hits), `latency` (78), `atomic` (93), `race` (96), `revision` (215), `performance` (31), `benchmark` (21), `throughput` (13), `overhead` (44), `in-flight` (67); bodies read in full for #2219, #2517, #2518, #1942, #1062, #2109, #2168, #2752, #2514 plus #2752's comment thread. Code read: `policy_local.rs` (80 KB, full route table + wait semantics), `openshell-sandbox/src/lib.rs` (poll loop + interval default), `supervisor-network/src/run.rs` (generation-transition race mitigation), `e2e/rust/tests/live_policy_update.rs` (full). Docs: `docs/sandboxes/policies.mdx` (833 lines), `docs/sandboxes/inference-routing.mdx` (339 lines). Then `code.claude.com/docs/en/sandboxing` (full), `/en/settings` (targeted), `anthropic-experimental/sandbox-runtime` README.

**Deliberately skipped, declared:** `docs/reference/policy-schema.mdx` and `default-policy.mdx` (the normative schema — §3's granularity list is assembled from the prose guide and e2e fixtures, so treat it as complete-in-spirit rather than exhaustive) · `crates/openshell-policy` and `openshell-prover` (the OPA compilation path) · RFC 0005 and RFC 0011 · the 119 open PRs beyond #2168 · `docs.nvidia.com/openshell` hosted docs (the in-repo `docs/` is the same source, version-pinned to main) · the NVIDIA engineering blog.

---

## Flags for the leader

1. **C1 needs an amendment, not just an annex.** Two statements are now wrong or materially incomplete: the inference layer's reloadability is **gateway-global**, and *"no latency figures published"* is **false**.
2. **Cluster H needs a split.** OpenShell belongs in the **counter-example** column — the cleanest instance in the run of a plane whose exemption is structurally withheld from the bounded party. Claude Code's sandbox stays in Cluster H and gains a second, sharper instance (settings-file self-edit) pending the §6 falsifier.
3. **Cluster A's "none of them scopes per phase of a declared task" survives**, but the cost of adding it just fell dramatically on the Claude Code path and rose on the OpenShell path. **The gap moved; it did not close.**
4. **H-B H2, H-B H20 and COD-H04 should be re-read against §2 rather than §1.** Latency was never the binding constraint. **Connection severance is.**

---

## `cites:`

```yaml
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/2219, title: "~45 ms added latency on sandbox tunnels/egress tinygrams due to Nagle x delayed-ACK", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/2517, title: "[Bug] UpdateConfig does not wake sandbox watchers after an atomic policy revision commit", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/2518, title: "[Bug] Supervisor does not acknowledge newer sandbox policy revisions with an unchanged policy hash", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/1942, title: "fix(sandbox): eliminate startup stale-policy forward proxy race", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/1062, title: "OpenShell Agent-Driven Policy Management (Non-Negotiable Trust Boundary)", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/2109, title: "Enterprise permission modes with managed maximum policies", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/pull/2168, title: "feat(policy): add managed maximum permission modes", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/2752, title: "process_binary_aware_network_policy: approved + reloaded draft chunks still reject matching traffic", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/issues/2514, title: "[Bug] Intermittent external egress failure: allowed request followed by NET:FAIL", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/blob/main/crates/openshell-supervisor-network/src/policy_local.rs, title: "openshell-supervisor-network — policy.local sandbox-facing HTTP API", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/blob/main/crates/openshell-sandbox/src/lib.rs, title: "openshell-sandbox — settings poll loop and OPENSHELL_POLICY_POLL_INTERVAL_SECS default", org: NVIDIA, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/NVIDIA/OpenShell/blob/main/e2e/rust/tests/live_policy_update.rs, title: "E2E tests for live policy updates on a running sandbox", org: NVIDIA, year: 2026, surface: active-dev}
- {type: docs, ref: https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/policies.mdx, title: "Sandbox Policies — static vs dynamic sections, hot reload, policy generations, validation failure modes", org: NVIDIA, year: 2026, surface: active-dev}
- {type: docs, ref: https://github.com/NVIDIA/OpenShell/blob/main/docs/sandboxes/inference-routing.mdx, title: "Inference Routing — inference.local, privacy router, provider/model configuration and hot refresh", org: NVIDIA, year: 2026, surface: active-dev}
- {type: docs, ref: https://code.claude.com/docs/en/sandboxing, title: "Configure the sandboxed Bash tool", org: Anthropic, year: 2026, surface: active-dev}
- {type: docs, ref: https://code.claude.com/docs/en/settings, title: "Claude Code settings — precedence, scopes, and when edits take effect", org: Anthropic, year: 2026, surface: active-dev}
- {type: repo, ref: https://github.com/anthropic-experimental/sandbox-runtime, title: "Anthropic Sandbox Runtime (srt) — OS-level filesystem and network sandboxing without a container", org: Anthropic, year: 2026, surface: active-dev}
```
