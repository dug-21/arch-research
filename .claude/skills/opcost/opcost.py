#!/usr/bin/env python3
"""opcost — accurate per-repo Claude token reporting, by model, daily + weekly.

Reports RAW token consumption for the current repo, broken down by model and by
the four usage classes (input / output / cache-write / cache-read), rolled up
daily and weekly. No dollars, no budget, no cross-repo denominator — just the
honest, observable numbers, so you can watch a couple of weeks of real activity
and then set a threshold from data.

Scope (be honest about it): reads only local Claude Code transcripts on THIS
machine (~/.claude/projects/**/*.jsonl). It does NOT see claude.ai web, Cowork,
other machines, or other repos. On a Max subscription there is no per-token bill
and no exposed quota meter (see product/research/opcost-001/), so token counts
are the accurate primitive; anything $-denominated would be a notional proxy.

Usage:
  python3 opcost.py                 # current repo (cwd), last 14 days + weekly
  python3 opcost.py --days 30       # widen the daily window
  python3 opcost.py --repo NAME     # a specific repo by name
  python3 opcost.py --all           # every repo on this machine
  python3 opcost.py --cost          # add a NOTIONAL $-equiv column (list price, NOT Max spend)
"""
import json, os, glob, argparse, collections
from datetime import datetime, timedelta

ROOT = os.path.expanduser("~/.claude/projects")
CONFIG_PATH = os.path.expanduser("~/.claude/opcost.config.json")
CLASSES = ["input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"]
SHORT = {"input_tokens": "input", "output_tokens": "output",
         "cache_creation_input_tokens": "cache_wr", "cache_read_input_tokens": "cache_rd"}

# Optional --cost only. $/1M tokens, list price. cache_wr=1.25x input (5m TTL), cache_rd=0.10x.
PRICING = {"claude-opus-4-8": (5, 25), "claude-opus-4-7": (5, 25), "claude-opus-4-6": (5, 25),
           "claude-fable-5": (10, 50), "claude-mythos-5": (10, 50),
           "claude-sonnet-5": (3, 15), "claude-sonnet-4-6": (3, 15), "claude-haiku-4-5": (1, 5)}


def reset_weekday():
    try:
        with open(CONFIG_PATH) as f:
            return int(json.load(f).get("reset_weekday", 0))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0


def week_start(d, rwd):
    ws = d - timedelta(days=(d.weekday() - rwd) % 7)
    return ws.date()


def notional_cost(model, c):
    inp, out = next((p for k, p in PRICING.items() if model.startswith(k)), (5, 25))
    return (c["input_tokens"] * inp + c["output_tokens"] * out
            + c["cache_creation_input_tokens"] * inp * 1.25
            + c["cache_read_input_tokens"] * inp * 0.10) / 1_000_000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--repo", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--cost", action="store_true")
    args = ap.parse_args()

    target = None if args.all else (args.repo or os.path.basename(os.getcwd()))
    rwd = reset_weekday()
    now = datetime.now().astimezone()
    daily_cutoff = (now - timedelta(days=args.days)).date()

    by_model = collections.defaultdict(lambda: collections.Counter())   # model -> class counts (+msgs)
    weekly = collections.defaultdict(lambda: collections.Counter())     # (weekstart, model) -> counts
    daily = collections.defaultdict(lambda: collections.Counter())      # (day, model) -> counts

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
                    u = (e.get("message") or {}).get("usage")
                    if not u:
                        continue
                    repo = os.path.basename((e.get("cwd") or "(unknown)").rstrip("/")) or "(unknown)"
                    if target is not None and repo != target:
                        continue
                    ts = e.get("timestamp", "")
                    if not ts:
                        continue
                    try:
                        t = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
                    except ValueError:
                        continue
                    model = (e.get("message") or {}).get("model") or "(unknown)"
                    counts = {cl: (u.get(cl, 0) or 0) for cl in CLASSES}
                    for agg, key in ((by_model, model),
                                     (weekly, (week_start(t, rwd), model)),
                                     (daily, (t.date(), model))):
                        agg[key].update(counts)
                        agg[key]["msgs"] += 1
        except (OSError, IOError):
            continue

    scope = "ALL repos" if target is None else f"repo '{target}'"
    print("=" * 78)
    print(f"opcost — token report · {scope} · this machine's Claude Code only")
    print("=" * 78)
    if not by_model:
        print("No transcripts found for this scope.")
        return

    # 1. Per-model totals (the headline) — full 4-class breakdown
    def tot(c):
        return sum(c[cl] for cl in CLASSES)
    print("\nBY MODEL (all-time in scope)")
    cols = f"{'model':<22}{'msgs':>6}" + "".join(f"{SHORT[cl]:>13}" for cl in CLASSES) + f"{'TOTAL':>15}"
    if args.cost:
        cols += f"{'~$(notional)':>14}"
    print(cols)
    print("-" * len(cols))
    for model in sorted(by_model, key=lambda m: -tot(by_model[m])):
        c = by_model[model]
        row = f"{model:<22}{c['msgs']:>6}" + "".join(f"{c[cl]:>13,}" for cl in CLASSES) + f"{tot(c):>15,}"
        if args.cost:
            row += f"{notional_cost(model, c):>13,.2f}"
        print(row)

    # 2. Weekly by model
    print(f"\nWEEKLY (week starts {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][rwd]})")
    wcols = f"{'week':<12}{'model':<22}{'msgs':>6}{'TOTAL tokens':>16}"
    print(wcols); print("-" * len(wcols))
    for (ws, model) in sorted(weekly, reverse=True):
        c = weekly[(ws, model)]
        print(f"{ws.isoformat():<12}{model:<22}{c['msgs']:>6}{tot(c):>16,}")

    # 3. Daily by model (last --days)
    print(f"\nDAILY (last {args.days} days)")
    dcols = f"{'day':<12}{'model':<22}{'msgs':>6}{'TOTAL tokens':>16}"
    print(dcols); print("-" * len(dcols))
    for (day, model) in sorted(daily, reverse=True):
        if day < daily_cutoff:
            continue
        c = daily[(day, model)]
        print(f"{day.isoformat():<12}{model:<22}{c['msgs']:>6}{tot(c):>16,}")


if __name__ == "__main__":
    main()
