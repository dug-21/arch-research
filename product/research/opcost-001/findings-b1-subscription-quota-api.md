# FINDINGS — B1/N-a: Is Claude subscription usage-quota programmatically observable?

*Run `opcost-001` · research-scope B1 (#114) / N-a (#118) · read-only researcher (factory-researcher) · 2026-07-10*
*Evidence class: all doc-claim / community-report — none demonstrated by us (no subscription OAuth token to exercise endpoints). Flagged per claim.*

**Blunt verdict: PARTIAL — YES-in-practice via an undocumented/unstable channel, NO officially.**

---

## 1. Subscription usage model (Max/Pro)
- **5-hour rolling window** — starts on first prompt, resets 5h later. Capacity tier-scaled (Pro ≈45 msgs; Max 5×≈225; Max 20×≈900 — approximate, model/length-weighted).
- **Weekly cap** — rolling 7-day from first prompt (not Monday reset); live since 2025-08-28. Effectively two caps: overall + a model-specific one (**FLAG:** sources disagree Opus vs Sonnet — unstable, verify at runtime).
- **Shared pool** across claude.ai + IDE + Claude Code.
- **Units:** presented as message counts / "compute hours" but **actually model-weighted & opaque**. The one clean machine-readable unit Anthropic exposes is a **utilization %** per window + `resets_at` — not tokens, not messages.

## 2. The gap — can a script read "% consumed / time-to-reset"?
**YES via an unsupported path; NO via any official API.**
- **Undocumented:** `GET https://api.anthropic.com/api/oauth/usage` → `{five_hour:{utilization, resets_at}, seven_day:{utilization, resets_at}}`. Auth: subscription **OAuth token** (not API key) + `anthropic-beta: oauth-2025-04-20`, `user:profile` scope. This is the source behind `/usage` + statusline HUD; consumed by community statusline projects.
  - **Risks:** undocumented, beta, marked **"not planned,"** and itself **429-prone** (issue #31021). Durability risk is real — reverse-engineering, not integration. **Not run by us.**
- **Secondary (version-dependent):** CC **≥2.1.x** may pass `rate_limits.five_hour`/`seven_day` (utilization % + reset) **directly on statusline stdin** → quota with zero API calls. Conflicting reports (version drift); same data origin. Least-fragile access **if** CC ≥2.1.x + statusline hook.
- **Proxies (inadequate for quota %):**
  - **Local JSONL token counts** (`~/.claude/projects/*`) — ⚠️ **10–100× inaccurate** vs internal totals (input undercounted 100–174×, output 10–17× off; open bug #22686). **Tokens, not quota.** *This directly qualifies R1's "parse transcripts" path — the keys exist but the token numbers may be unreliable; must be verified empirically.*
  - Statusline cumulative totals — more accurate, but still tokens, not the model-weighted cap.
  - $-at-list-price — notional only; not the subscription's real accounting.

## 3. API-billing path — the supported N-a exception (org/API-key accounts only)
- **Admin API key** (`sk-ant-admin01-…`), Console/Platform plan. *Unavailable for individual accounts.* Enterprise → separate Analytics API key.
- **Usage:** `GET /v1/organizations/usage_report/messages` — buckets `1m/1h/1d`; group/filter by `api_key`, `workspace`, `model`, `service_tier`, `context_window`, `inference_geo`, `speed`; typed token fields. **Per-key + per-workspace confirmed.**
- **Cost:** `GET /v1/organizations/cost_report` — USD cents, daily; group by workspace/description. ~5-min freshness.
- **Per-user Claude Code:** separate Claude Code Analytics API (estimated $ + productivity), managed/Enterprise.

## 4. Reconciliation — no common unit
Subscription = **utilization %** of an opaque model-weighted rolling window. API = **tokens + USD**. No authoritative conversion; only a lossy one-way token→$-estimate bridge (and the token source is unreliable). **Don't treat a $-estimate as real subscription consumption.**

## Honesty flags (not verified by us)
- Did not execute `/api/oauth/usage` or inspect live statusline stdin — field shapes are report-based.
- Whether the OAuth endpoint is still live today, and its ToS status for scripted use — **unassessed; a POC must probe before any design depends on it.**
- CC version threshold for stdin `rate_limits` passthrough — unconfirmed.

## Sources
platform.claude.com/docs usage-cost-api · docs.anthropic.com admin-api/usage-cost · support.claude.com models-usage-and-limits · claude-code issues #31021, #22686 · jtbr statusline gist · ohugonnot/claude-code-statusline · gille.ai jsonl-undercount · truefoundry / usagebar / sessionwatcher (2026)
