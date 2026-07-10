---
name: opcost
description: Report cost-weighted Claude usage across ALL your repos and pace it against a self-defined weekly budget. Reads local Claude Code transcripts (~/.claude/projects), prices each message's tokens per-model in $-equivalent, attributes spend by repo, and flags any repo running ahead of its paced share. Use when the user asks "what am I spending on Claude", "how much has this repo used", "am I on budget", "who's burning the most", or wants a per-repo Claude usage/budget breakdown. Portable — drop into ~/.claude/skills/ to run from any repo.
---

# opcost — cost-weighted, time-paced Claude usage bucket

Answers **"what are we spending on Claude, per repo, and are we on pace?"** — the buildable
answer to the `opcost` goal. It is a **passive HUD**: it reports, it does not block.

## What it does
- Reads every repo's transcripts under `~/.claude/projects/**/*.jsonl` (one place, all repos).
- Prices each assistant message's **four** `usage` fields per-model in **$-equivalent** (list price):
  `input`, `output`, `cache_creation` (1.25×), `cache_read` (0.10×). Cost-weighting matters —
  `cache_read` is ~86% of raw tokens but only 0.1× the price, so raw-token counts overweight it ~10×.
- Attributes spend by **repo** (the transcript `cwd`) and buckets it into a **self-defined week**.
- If a weekly budget is set, draws a **daily pace line** (`elapsed_fraction × budget × repo_share`)
  and flags any repo **ahead of pace** — catches an over-burn days before a hard cap would.

## Run it
```bash
python3 ~/.claude/skills/opcost/opcost.py     # or .claude/skills/opcost/opcost.py in-repo
```
First run creates `~/.claude/opcost.config.json`. Then set:
```json
{
  "weekly_budget_usd": 150,          // your self-defined ceiling ($-equiv); null = report only
  "reset_weekday": 0,                // 0=Mon .. 6=Sun — when your week resets
  "repo_shares": {"arch-research": 0.6, "hotspot-bank": 0.2}  // fractions; missing repos split the rest
}
```
Re-run to see week-to-date spend, per-repo share, pace target, and ⚠ flags.

## How to read the output
- **WEEK-TO-DATE** — total $-equiv this week vs budget and pace target. `⚠ AHEAD OF PACE` = burning
  faster than the elapsed fraction of the week allows.
- **Per-repo table** — `wk $` / `wk %` (attribution), `share` (your allocation), `pace $` (target so
  far), `ratio` (>1.0× = ahead). `ratio 1.89x ⚠` means that repo has used 1.89× its paced allowance.
- **rolling 7-day total** — the closest observable proxy to Anthropic's *real* rolling weekly cap.

## Honest limits (don't oversell)
- The unit is a **$-equivalent proxy**, not the actual **subscription quota** — that 5h/weekly meter
  is not programmatically exposed (only the undocumented `/api/oauth/usage` endpoint returns it; see
  `product/research/opcost-001/`). For a subscription, treat this as *relative* rationing, not a bill.
- Token-share ≈ quota-share only when the **model mix** is similar across repos (Opus weighs far more
  than Haiku). The `note:` line lists any unknown model priced as Opus.
- Cache-write assumes the **5-min TTL** (1.25×); 1-hour cache writes cost 2× and aren't distinguished
  in the transcript.
- Prices are **list** (governance-stable); `claude-sonnet-5` has intro pricing through 2026-08-31.

Design + evidence: goal `opcost` (Unimatrix #113), findings in `product/research/opcost-001/`.
