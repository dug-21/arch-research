# FINDINGS — B1 feasibility: Claude Code usage/cost telemetry & subscription-quota observability

*Run `opcost-001` · research-scope B1 (#114) · read-only researcher (claude-code-guide) · verified against this machine (Claude Code v2.1.205)*

**Bottom line:** Per-repo usage attribution is **feasible today** by parsing local session transcripts keyed on `cwd`. Subscription-**quota** consumption (5h rolling window / weekly cap) is **NOT programmatically observable** — interactive `/usage`·`/status` display only.

---

## 1. Claude Code native OTEL — YES, but no repo attribution
Opt-in (`CLAUDE_CODE_ENABLE_TELEMETRY=1`), disabled by default. Exports metrics + events (+ traces in beta).

- Metrics: `claude_code.session.count`, `claude_code.cost.usage` (USD **estimate**, local, API-pricing-based), `claude_code.token.usage` (input/output/cache separately), `lines_of_code.count`, `commit.count`, `active_time.total`.
- Events: `user_prompt`, `api_request`, `api_error`, `tool_result`, `tool_decision`, `mcp_server_connection`, `auth` — linked by `prompt.id`.
- Attribute fields: `user.id`, `session.id`, `organization.id`, `user.email`, `model`. **NO `cwd` / `project` / `repo`** — native OTEL cannot be sliced per-repo in a remote collector without custom instrumentation.
- Workaround: per-project `.claude/settings.json` env block injecting `OTEL_RESOURCE_ATTRIBUTES="project=<repo>"`, or a self-hosted Claude apps gateway (Bedrock/etc.).

**Confidence:** HIGH (official `monitoring-usage.md`).

## 2. `/cost` and `/usage` commands — token counts, not quota
- `/cost`: token counts + local $ estimate; not billing-relevant on subscription.
- `/usage` (recommended for subscription): session token block + **plan usage bars** (24h/7d), breakdown by skills/subagents/MCP. Figures are **local estimates** (this machine only). Does **NOT** expose 5h-window / weekly-cap consumption programmatically.
- `/usage --json` / statusline JSON: **requested, pending** (issues #21943, #28999, #48660).

**Confidence:** HIGH.

## 3. Local session transcripts — the usable substrate ✅
`~/.claude/projects/<slug>/*.jsonl`, one JSONL per session, one message per line. **Inspected directly on this machine.**

Per-assistant-message: `message.usage.{input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens}` + `model`.
Attribution keys on every entry: **`cwd`** (repo/working-dir), `gitBranch`, `sessionId`, `timestamp`, `entrypoint` (cli/vscode/web), `version`.

→ **Per-repo, per-branch, per-session token usage is reconstructable post-hoc** by grouping transcripts on `cwd` and summing `message.usage.*`. No subscription-quota field present.

**Confidence:** HIGH (direct inspection).

## 4. Subscription-quota observability — **NO (programmatic)**
Quota model: 5-hour rolling window + weekly cap, **shared across Claude Code + claude.ai + Cowork** on one subscription (Max ~5–20× Pro).

Remaining/consumed quota is exposed via **none** of: env vars · HTTP response headers · local files · OTEL export · CLI `--json` flag. Only the interactive `/usage`·`/status` UI display. Feature requests pending as of Jul 2026.

**Verdict:** subscription-quota programmatic observability = **NO**.

## 5. Attribution verdict — PARTIAL (local-only, post-hoc)
- Attributable: local transcripts by `cwd` (repo) / `gitBranch`; session-level in OTEL (needs external session→repo map).
- Not attributable: native OTEL has no repo label; quota not exposed per-repo; beta traces don't carry `cwd`.
- Real-time *remote* per-repo attribution needs custom tooling (gateway resource-attrs or a hook that stamps `cwd`).

---

## Implication for the board
- **B1 (measure) + B2 (attribute) are feasible now** via a transcript-parsing artifact keyed on `cwd` — no new platform dependency. Strongest, cheapest path.
- **N-a (subscription-faithful unit) cannot be met as written** — the 5h/weekly quota meter is not observable. The honest unit is **tokens consumed (+ optional $-equivalent estimate)** per repo, NOT "% of subscription quota."
- **B3/B4 must re-scope** off a token/proxy meter rather than live quota headroom, OR depend on an unbuilt platform feature (`/usage --json`).

## Sources
- code.claude.com/docs/en/costs · /monitoring-usage.md · /claude-apps-gateway.md
- github.com/anthropics/claude-code issues #21943, #28999, #48660
- truefoundry.com/blog/claude-code-limits-explained · voitanos.io statusline
