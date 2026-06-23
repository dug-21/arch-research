# shd-002 / W4 — Distribution-compatibility (NFR N4)

**Workstream:** W4 — does each harness's architecture FORECLOSE multi-machine coordination or EXTEND to it?
**Date:** 2026-06-23
**Researcher:** read-only, directional. No installs, no runs. **Doc-claims only — nothing here is demonstrated evidence.**
**Lens discipline:** N4 is a **tie-breaker, not a gate** (SCOPE.md L36–37, D11). We are *not* building distribution now. The only question is whether the architecture forecloses a future coordinator-over-workers / remote-dispatch topology, or leaves room for / explicitly supports it.

## Classification scheme

- **FORECLOSES** — single-machine-bound by design; coordinating across hosts requires re-foundation (e.g. process is structurally welded to a local GUI/editor with no headless or API exit).
- **NEUTRAL** — single-machine in practice, but **scriptable** (headless/CLI, exit codes, stdin/stdout, JSON). An external coordinator (SSH, queue, CI) could fan it out across machines without modifying the tool. The tool itself does no distribution.
- **EXTENDS** — ships **explicit** remote/distributed/server features: a networked HTTP/WebSocket server, remote-sandbox-over-network execution, or an officially-driven SDK built to be embedded and multiplexed.

> Note: NEUTRAL is **sufficient** for N4. N4 asks only "does it foreclose?" A clean headless CLI already satisfies the tie-breaker because the coordination can live *above* the harness. EXTENDS is a bonus, not a requirement — and EXTENDS features (remote sandbox, managed cloud) often pull toward vendor infra that can collide with N1 (owned-HW/budget) and N2 (no-outage). Flag, don't over-weight.

---

## Per-harness classification

| Harness | Class | Determining feature |
|---|---|---|
| **Claude Code** | **EXTENDS** | `claude -p` headless + Python/TS **Agent SDK** (same agent loop, embeddable, multiplexable); `--output-format json/stream-json`, `--resume <session_id>`, `--bare` for reproducible CI. Built to be driven by an external orchestrator. |
| **OpenHands (V1 SDK)** | **EXTENDS** | Native **agent-local / sandbox-remote split over WebSocket** (`APIRemoteWorkspace`); one controller per host, Docker-per-task. Distributed execution is a first-class architecture, not a bolt-on. |
| **opencode** | **EXTENDS** | `opencode serve` = headless **HTTP server with OpenAPI 3.1 spec** + generated SDK; configurable `--hostname`/`--port`/`--cors`, `OPENCODE_SERVER_PASSWORD`; clients attach to a remote backend, sessions survive SSH/disconnect. Client-server by design. |
| **Goose** | **EXTENDS** | CLI **headless mode** + **recipes** (YAML workflows run sequentially/parallel) + **subagents** (independent parallel agent processes); roadmap is an explicit "meta-agent orchestrator." Orchestration primitives are native. |
| **Cline** | **EXTENDS** (trending) | Originally IDE-bound, but **Cline 2.0 / Cline SDK** extracted the agent loop into a stateless, product-agnostic **runtime as a shared service**; sessions move across surfaces; SDK + CLI now exist. No longer welded to VS Code. |
| **Continue** | **NEUTRAL** (→EXTENDS-ish) | Standalone **CLI with headless mode** for CI/CD + async PR agents; IDE-agnostic. Coordination is external. *Caveat:* acquired by Cursor (2026), repo read-only at v2.0.0 — **maintenance/continuity risk** that overrides the architecture lens. |
| **aider** | **NEUTRAL** | Pure **stdin/stdout single-process CLI** against the local filesystem; fully scriptable, CI-ready, model-agnostic. No server, no remote features. Coordinatable only by an external driver. (Browser mode is still single-process/local.) |
| **Roo Code** | **NEUTRAL** (was FORECLOSES) | Core is a **VS Code-only extension** (one task at a time, local editor process). A newer **`@roo-code/cli` headless build via a VS Code-API shim** lifts it out of strict IDE-binding; optional Roo Code Cloud agents exist but are vendor-hosted. The shim is what saves it from FORECLOSES. |

**No harness in the candidate set lands on FORECLOSES.** Every one either ships a headless/CLI exit (NEUTRAL floor) or an explicit server/SDK/remote feature (EXTENDS). The IDE-native tools (Cline, Roo, Continue) all grew CLI/SDK escape hatches by 2026, so "IDE extension" no longer implies single-machine lock-in. This makes N4 a **weak discriminator** across this field — consistent with its tie-breaker status.

---

## Ranking on distribution-future (best → weakest), tie-breaker weight only

1. **OpenHands (V1 SDK)** — only candidate where *remote execution itself* (agent-here, sandbox-there over WebSocket) is the native architecture. Strongest pure distribution story. **But** the remote-sandbox path leans on `runtime.all-hands.dev` / Cloud Workspace (self-host via Docker sandbox is possible) — watch the N1/N2 collision before treating this as free.
2. **opencode** — clean, standards-based: a real HTTP/OpenAPI server you self-host and bind to any interface, with persistent reconnectable sessions. Distribution lives in *your* infra, not a vendor's → best N1/N2 alignment among the EXTENDS group.
3. **Claude Code** — `claude -p` + Agent SDK is purpose-built to be embedded and multiplexed by an external coordinator; session resume enables fan-out/fan-in. Coordination is an SDK-driver pattern rather than a built-in server, but the substrate is explicitly there. (Caveat outside W4: the **local-backend** question — N1/N2 / methodology T3a shim — is W2's call, not distribution's.)
4. **Goose** — recipes + parallel subagents give in-process orchestration today and a stated meta-orchestrator roadmap; headless CLI makes external fan-out trivial.
5. **Cline** — SDK extraction is the right architectural direction and removes the IDE weld, but it is newer/less proven as a distribution substrate than opencode/OpenHands.
6. **aider** — NEUTRAL but *clean*: a perfectly scriptable unit you can wrap in your own coordinator. Does nothing itself, forecloses nothing. Ideal "dumb worker" in a coordinator-over-workers topology.
7. **Continue** — architecturally fine (headless CLI) but **continuity risk** (Cursor acquisition, read-only repo) outweighs the distribution lens.
8. **Roo Code** — weakest: distribution depends on a shim-based CLI bolted onto a VS-Code-only core; cloud agents are vendor-hosted. Not foreclosed, but the least natural fit.

### Tie-breaker takeaway
Because nothing forecloses, **N4 does not eliminate any candidate** and should only nudge between otherwise-close options. If two harnesses tie on the load-bearing constraints (W2 local-backend, W3 autonomy/tool-call reliability), N4 favors, in order: **opencode** (self-hosted HTTP server, best N1/N2-aligned distribution) and **Claude Code** (SDK-driven orchestration). **OpenHands** ranks #1 on raw distribution capability but its remote-sandbox path tilts toward vendor infra — discount accordingly under N1/N2. Do **not** let N4 pull the recommendation toward OpenHands' managed runtime on the strength of distribution alone.

---

## Citations (all doc-claims, retrieved 2026-06-23)

- Claude Code headless / Agent SDK: https://code.claude.com/docs/en/headless (`-p`, `--output-format json|stream-json`, `--resume`, `--bare`, Python/TS SDK); SDK rename + programmatic agent loop per https://hidekazu-konishi.com/entry/claude_agent_sdk_complete_guide.html
- OpenHands V1 SDK distributed runtime: https://docs.openhands.dev/sdk/guides/agent-server/api-sandbox (APIRemoteWorkspace, WebSocket agent<->remote runtime); SDK paper https://arxiv.org/html/2511.03690v2 ; V0->V1 transition https://deepwiki.com/OpenHands/OpenHands
- opencode server mode: https://opencode.ai/docs/server/ (`opencode serve`, OpenAPI 3.1, `--hostname/--port/--cors`, `OPENCODE_SERVER_PASSWORD`); client-server + persistent sessions https://opencode.ai/docs/
- Goose: https://goose-docs.ai/ and https://github.com/aaif-goose/goose (headless CLI, recipes, subagents); meta-orchestrator roadmap https://github.com/aaif-goose/goose/discussions/6973
- Cline SDK / runtime extraction: https://cline.ghost.io/introducing-cline-sdk-the-upgraded-agent-runtime/ ; repo tagline "SDK, IDE extension, or CLI" https://github.com/cline/cline
- Continue CLI/headless + Cursor acquisition: https://github.com/continuedev/continue ; https://vibecoding.app/blog/continue-dev-review ; https://docs.continue.dev/
- aider single-process stdin/stdout: https://aider.chat/docs/ ; browser mode https://aider.chat/docs/usage/browser.html
- Roo Code VS-Code-only core + `@roo-code/cli` shim: https://deepwiki.com/RooCodeInc/Roo-Code/15-cli-application ; CLI/headless issue https://github.com/RooCodeInc/Roo-Code/issues/3835 ; https://github.com/RooCodeInc/Roo-Code

## Limits of this finding
- 100% doc-claim / vendor-doc derived. Per methodology **L1**, none of these distribution paths were exercised; a live test could reveal that a "server mode" or "remote sandbox" doesn't actually coordinate as advertised. W4 only establishes that the architecture *leaves room* — it does not prove distribution works.
- "EXTENDS" here means a documented feature exists, not that it's production-grade or N1/N2-clean. The vendor-infra tilt of OpenHands' and Continue's/Roo's cloud paths is the main caveat to carry into W5.
