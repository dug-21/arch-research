#!/usr/bin/env python3
"""opcost — cost-weighted, time-paced Claude usage bucket across all your repos.

Reads local Claude Code transcripts (~/.claude/projects/**/*.jsonl), prices each
message's four usage fields per-model in $-equivalent (list price), attributes by
repo (cwd), and paces spend against a self-defined weekly budget.

Portable: put this skill at ~/.claude/skills/opcost/ and it sees every repo from
anywhere. Config lives at ~/.claude/opcost.config.json (auto-created on first run).

Design (opcost goal, run opcost-002):
  - unit  = $-equivalent, cost-weighted (cache_read is ~0.1x input, so raw tokens
            overweight it ~10x; see findings-b1). NOT the subscription quota meter,
            which isn't observably exposed — this is the buildable proxy (N-a).
  - bucket= a SELF-DEFINED weekly budget you set; per-repo shares split it.
  - pace  = a daily pace line (elapsed_fraction_of_week x budget); flags a repo
            running AHEAD of pace before the weekly cap is hit.
Passive HUD: this reports, it does not block. (A PreToolUse hook is a later step.)
"""
import json, os, glob, sys, collections
from datetime import datetime, timedelta, timezone

ROOT = os.path.expanduser("~/.claude/projects")
CONFIG_PATH = os.path.expanduser("~/.claude/opcost.config.json")

# $ per 1M tokens, list price (verified via claude-api skill, 2026-07). The unit is
# a governance proxy, not a subscription bill — list price keeps the weight stable.
# NOTE: claude-sonnet-5 has intro pricing $2/$10 through 2026-08-31; list $3/$15 used
# here for a durable weight. Cache-write assumes 5-min TTL (1.25x); 1h TTL is 2x.
PRICING = {  # model-id prefix -> (input, output) $/Mtok
    "claude-opus-4-8":   (5.00, 25.00),
    "claude-opus-4-7":   (5.00, 25.00),
    "claude-opus-4-6":   (5.00, 25.00),
    "claude-fable-5":    (10.00, 50.00),
    "claude-mythos-5":   (10.00, 50.00),
    "claude-sonnet-5":   (3.00, 15.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-haiku-4-5":  (1.00, 5.00),
}
FALLBACK = (5.00, 25.00)  # unknown model -> price as Opus (conservative)
CACHE_WRITE_MULT = 1.25   # 5-min TTL
CACHE_READ_MULT = 0.10

DEFAULT_CONFIG = {
    "weekly_budget_usd": None,       # set this to enable pace checks (e.g. 150)
    "reset_weekday": 0,              # 0=Mon .. 6=Sun; the self-defined week boundary
    "repo_shares": {},               # {"arch-research": 0.6, ...}; missing -> even split
    "_comment": "opcost budget config. Set weekly_budget_usd and per-repo shares (fractions summing to <=1).",
}


def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return dict(DEFAULT_CONFIG), True
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    for k, v in DEFAULT_CONFIG.items():
        cfg.setdefault(k, v)
    return cfg, False


def price(model, u):
    """$-equivalent for one message's usage block, cost-weighted per model."""
    inp, out = FALLBACK
    for prefix, (i, o) in PRICING.items():
        if model and model.startswith(prefix):
            inp, out = i, o
            break
    dollars = (
        (u.get("input_tokens", 0) or 0) * inp
        + (u.get("output_tokens", 0) or 0) * out
        + (u.get("cache_creation_input_tokens", 0) or 0) * inp * CACHE_WRITE_MULT
        + (u.get("cache_read_input_tokens", 0) or 0) * inp * CACHE_READ_MULT
    ) / 1_000_000
    return dollars


def week_start(now, reset_weekday):
    d = now - timedelta(days=(now.weekday() - reset_weekday) % 7)
    return d.replace(hour=0, minute=0, second=0, microsecond=0)


def main():
    cfg, created = load_config()
    if created:
        print(f"Created default config at {CONFIG_PATH}")
        print("Set 'weekly_budget_usd' and 'repo_shares' to enable pace checks.\n")

    now = datetime.now().astimezone()
    wk_start = week_start(now, cfg["reset_weekday"])
    elapsed_frac = min(1.0, (now - wk_start).total_seconds() / (7 * 86400))
    rolling_start = now - timedelta(days=7)

    week = collections.defaultdict(float)     # repo -> $ this self-defined week
    rolling = collections.defaultdict(float)  # repo -> $ last rolling 7 days
    unknown_models = set()

    for path in glob.glob(os.path.join(ROOT, "**", "*.jsonl"), recursive=True):
        try:
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        e = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if e.get("type") != "assistant":
                        continue
                    msg = e.get("message", {})
                    u = msg.get("usage")
                    if not u:
                        continue
                    model = msg.get("model", "")
                    if model and not any(model.startswith(p) for p in PRICING):
                        unknown_models.add(model)
                    ts = e.get("timestamp", "")
                    if not ts:
                        continue
                    try:
                        t = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
                    except ValueError:
                        continue
                    repo = os.path.basename((e.get("cwd") or "(unknown)").rstrip("/")) or "(unknown)"
                    d = price(model, u)
                    if t >= wk_start:
                        week[repo] += d
                    if t >= rolling_start:
                        rolling[repo] += d
        except (OSError, IOError):
            continue

    budget = cfg["weekly_budget_usd"]
    shares = cfg["repo_shares"]
    repos = sorted(set(week) | set(rolling) | set(shares), key=lambda r: -week.get(r, 0))

    def repo_share(repo):
        if repo in shares:
            return shares[repo]
        unassigned = [r for r in repos if r not in shares]
        remaining = max(0.0, 1.0 - sum(v for k, v in shares.items() if k in repos))
        return remaining / len(unassigned) if unassigned else 0.0

    print("=" * 74)
    print(f"opcost — cost-weighted Claude spend ($-equiv, list price)")
    print(f"self-defined week: {wk_start:%Y-%m-%d %a} 00:00  ->  now ({elapsed_frac*100:.0f}% elapsed)")
    print("=" * 74)

    wk_total = sum(week.values())
    if budget:
        pace_total = budget * elapsed_frac
        flag = "  ⚠ AHEAD OF PACE" if wk_total > pace_total else ""
        print(f"WEEK-TO-DATE: ${wk_total:,.2f} of ${budget:,.2f} budget "
              f"(pace target ${pace_total:,.2f}){flag}")
    else:
        print(f"WEEK-TO-DATE: ${wk_total:,.2f}   (set weekly_budget_usd for pace checks)")
    print()

    hdr = f"{'repo':<24}{'wk $':>10}{'wk %':>7}"
    if budget:
        hdr += f"{'share':>7}{'pace $':>10}{'ratio':>8}"
    print(hdr)
    print("-" * len(hdr))
    for repo in repos:
        w = week.get(repo, 0.0)
        pct = 100 * w / wk_total if wk_total else 0
        row = f"{repo:<24}{w:>10.2f}{pct:>6.0f}%"
        if budget:
            sh = repo_share(repo)
            pace = budget * sh * elapsed_frac
            ratio = w / pace if pace else 0
            mark = " ⚠" if w > pace and pace > 0 else ""
            row += f"{sh*100:>6.0f}%{pace:>10.2f}{ratio:>7.2f}x{mark}"
        print(row)

    print()
    roll_total = sum(rolling.values())
    print(f"rolling 7-day total: ${roll_total:,.2f}  (closest proxy to Anthropic's real rolling weekly cap)")
    if unknown_models:
        print(f"note: priced-as-Opus (unknown model): {', '.join(sorted(unknown_models))}")


if __name__ == "__main__":
    main()
