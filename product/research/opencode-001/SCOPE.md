# opencode-001 — OpenCode v2 as a platform for a Unimatrix-backed harness

**Status:** researching\
**Goal(s):** Run development and research workflows across eligible models while retaining continuous learning and useful context from Unimatrix. Related goal: sovereign local-first dev/research loop (Unimatrix #242).\
**Capability target:** Routing-capable agentic harness (Unimatrix #245). The declarative model-routing and escalation contract (#244) is an interface dependency.\
**Confidence-required:** directional\
**Phase / area:** workflow harness and memory integration\
**Cycle topic / Issue:** `opencode-001` / [#77](https://github.com/dug-21/arch-research/issues/77)

## The question

> Can a supported OpenCode v2 extension carry the Unimatrix observation and context-injection loop that runs in Claude Code today, while allowing our platform to choose eligible models per task and isolate memory by repository?

Establish what the released runtime supports, where adaptation is needed, and what requires a behavioral trial before OpenCode becomes a platform dependency. Compare the current Claude Code integration against the actual Unimatrix contract. Treat cross-repository memory as a separate opt-in capability.

## Why it matters

The immediate opportunity is to select among model families and allocate existing subscriptions across work without sacrificing the memory that compounds across sessions. A documented model picker or MCP connection alone cannot establish that the capture, learning, and injection loop survives the move.

## Known constraints and prior art

- Use Unimatrix #252 (OpenCode registry and earlier do-not-fork recommendation), #253 (provider transport), and #255 (harness–provider–model tool-call contract). Recheck their version-sensitive premises. #252 addressed a stronger authority claim than this investigation’s everyday workflow and memory requirements.
- Use [shd-002](../shd-002/FINDINGS.md) for historical local-model tool-call issues and [wfh-009 W3](../wfh-009/findings-W3.md) for OpenCode 1.17.7 adapter evidence and configuration projection gaps. Verify which conclusions survive v2.
- Start with the shipped [Unimatrix OpenCode observation plugin](https://github.com/dug-21/unimatrix), its documented `SubagentStart` injection gap, and project-scoped bundle attach. Trace the existing plugin’s compatibility with the [v2 migration contract](https://opencode.ai/docs/build/plugins/migrate-v1/) before proposing a replacement. Per-project stores are the baseline. Evaluate whether the Collective contract can carry deliberately published knowledge while raw telemetry stays repository-scoped.
- The [Claude Agent provider release](https://opencode.ai/changelog/v2.2.3) documents use of the installed Claude Code runtime and its login. Treat that delegation path and OpenAI’s documented ChatGPT sign-in as different runtimes, with separate implications for model control, who executes tools, event visibility, and duplicate capture. Confirm distribution channels and release pins from the [OpenCode releases](https://github.com/anomalyco/opencode/releases).
- Pin the OpenCode release and corresponding source, plugin package and runtime. Record the Unimatrix revision and the current Claude Code baseline used in each comparison. Label hosted docs, source-confirmed behavior, runtime evidence, and unknowns individually.

## Bounded investigation

- **W1 — Release and provider access.** Identify the available v2 build and map official ChatGPT and Claude sign-in, eligible plans, model picks, quota/usage attribution, CLI/TUI versus programmatic support, and documented limitations. Distinguish first-party subscriptions from API keys, OpenCode plans, partner offerings and community auth plugins. Check vendor support and terms for the exact route. *Output:* provider and credential matrix with dated, versioned sources and availability uncertainties.
- **W2 — OpenCode lifecycle and extension contracts.** Trace v2 plugin hooks, typed events and SDK/API calls to their source and ordering. Check session creation/resume/close, parent and child sessions, prompt submission, before/after tool execution and failures, compaction, cancellation, permissions, and per-request context construction. Identify registration scope, callback timing, payload IDs, writable fields, event loss/replay, and interactive versus headless coverage. Compare every load-bearing event and hook on the ChatGPT and Claude Agent paths separately. *Output:* lifecycle matrix with read/write timing, stability boundary, and available substitutes for gaps.
- **W3 — Unimatrix compatibility.** Trace the actual Claude hook configuration, event payload and transport through Unimatrix ingest, attribution and downstream use. Trace context injection independently from capture, including source selection, placement, deduplication and compaction. Map required fields to W2 and compare the existing plugin through the V1 compatibility path against a native v2 port. Check whether Claude Agent delegation yields OpenCode-side, Claude-side, or duplicate Unimatrix observations. *Output:* producer-to-consumer compatibility matrix covering required versus useful events and fields, loss consequences, and injection behavior.
- **W4 — Routing and memory boundaries.** Locate when primary/child agent and model selection become effective in interactive and SDK-controlled runs. Compare built-in defaults and per-agent overrides with external policy selection, including escalation, quota errors, and explicit fallback. Establish repository identity across subdirectories, worktrees, clones, and remote sessions. Compare per-repository storage with an opt-in collective sharing model using the actual Collective contract and repository where accessible. *Output:* candidate integration designs ranked by implementation surface, upgrade exposure, routing control, and memory isolation. Record where Collective evidence is unavailable.

## Expected output

1. Four findings files and one synthesis with source and release provenance, open questions, and an adopt, assemble, build, or park recommendation.
2. Separate conclusions for subscription access, observation fidelity, context injection, routing authority, repository identity, and collective sharing. State whether each gap blocks the platform decision or can be deferred.
3. A staged follow-on scope testing a pinned OpenCode integration on one representative real workflow against its Claude Code baseline and using a second repository to probe isolation.

## Proof bar

The owner approved the directional scope with one clarification. Derive the required capture, learning, context injection, routing, and isolation behavior from current Claude Code workflows and the intended platform. Evaluate the shipped Unimatrix OpenCode adapter against those requirements and identify missing host or Unimatrix capabilities even where the existing integration works as designed.

This directional scope produces a source-grounded recommendation and a validation plan. A follow-on would need a captured end-to-end trace showing Unimatrix receives and uses the required OpenCode events, places a relevant memory in the intended model request, and keeps another repository’s memory out of that request. Trace model assignment for both the main task and delegated work, quota/failure handling, attribution on resume and compaction, and recovery behavior when Unimatrix or the event connection is unavailable. Check each advertised subscription path independently against plan usage. Exercise collective sharing separately with a deliberately published memory and provenance.

## Explicitly out of scope

- Implementing the adapter, forking OpenCode, switching the primary harness, or changing live credentials, billing, Unimatrix data, or collective state.
- Treating source observations as end-to-end runtime evidence.
- Selecting hardware, benchmarking model quality, or designing the broader platform beyond the interfaces in the decision.

## Coverage / done call

Candidate surfaces include native v2 plugin hooks, the event stream plus SDK, and existing Unimatrix MCP integration where applicable. Stop after two consecutive source passes add no viable extension mechanism and the leading integration has at least two corroborating findings from independent boundaries, such as OpenCode source and Unimatrix ingest. Record documentation/source conflicts and empty cells explicitly. The owner confirms coverage.
