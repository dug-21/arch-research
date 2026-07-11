#!/usr/bin/env python3
"""opcost-001 B1 POC — parse Claude Code transcripts into a per-repo, per-day token bucket.

Tests two things:
  1. Feasibility: can we attribute token usage per-repo (cwd) and per-day from local transcripts?
  2. The R2 '10-100x off' flag: is it a real inaccuracy, or a field-selection artifact
     (summing bare input_tokens while ignoring cache_* fields that dominate under prompt caching)?
"""
import json, os, glob, collections
from datetime import datetime, timezone

ROOT = os.path.expanduser("~/.claude/projects")

# per (repo, day) -> token sums
buckets = collections.defaultdict(lambda: collections.Counter())
repo_totals = collections.defaultdict(lambda: collections.Counter())
n_msgs = collections.Counter()
models = collections.Counter()

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
                cwd = e.get("cwd") or "(unknown)"
                repo = os.path.basename(cwd.rstrip("/")) or cwd
                ts = e.get("timestamp", "")
                day = ts[:10] if ts else "(no-date)"
                inp = u.get("input_tokens", 0) or 0
                out = u.get("output_tokens", 0) or 0
                cc = u.get("cache_creation_input_tokens", 0) or 0
                cr = u.get("cache_read_input_tokens", 0) or 0
                key = (repo, day)
                for name, val in (("input", inp), ("output", out), ("cache_creation", cc), ("cache_read", cr)):
                    buckets[key][name] += val
                    repo_totals[repo][name] += val
                n_msgs[repo] += 1
                m = msg.get("model")
                if m:
                    models[m] += 1
    except (OSError, IOError):
        continue

def naive(c):   # what a naive parser sums
    return c["input"] + c["output"]
def full(c):    # true consumption incl. cache
    return c["input"] + c["output"] + c["cache_creation"] + c["cache_read"]

print("=" * 78)
print("PER-REPO TOTALS  (all-time, all sessions on this machine)")
print("=" * 78)
print(f"{'repo':<28}{'msgs':>6}{'naive(in+out)':>16}{'full(+cache)':>16}{'ratio':>8}")
grand_naive = grand_full = 0
for repo, c in sorted(repo_totals.items(), key=lambda kv: -full(kv[1])):
    nv, fl = naive(c), full(c)
    grand_naive += nv; grand_full += fl
    ratio = fl / nv if nv else 0
    print(f"{repo:<28}{n_msgs[repo]:>6}{nv:>16,}{fl:>16,}{ratio:>7.1f}x")
print("-" * 78)
gr = grand_full / grand_naive if grand_naive else 0
print(f"{'TOTAL':<28}{sum(n_msgs.values()):>6}{grand_naive:>16,}{grand_full:>16,}{gr:>7.1f}x")

print()
print("=" * 78)
print("FIELD BREAKDOWN  (where the tokens actually live)")
print("=" * 78)
agg = collections.Counter()
for c in repo_totals.values():
    agg.update(c)
tot = sum(agg.values())
for name in ("input", "output", "cache_creation", "cache_read"):
    print(f"  {name:<18}{agg[name]:>16,}  ({100*agg[name]/tot:5.1f}% of all tokens)")

print()
print("=" * 78)
print("arch-research — PER-DAY bucket  (full consumption incl. cache)")
print("=" * 78)
this = sorted([(d, c) for (r, d), c in buckets.items() if r == "arch-research"])
for day, c in this:
    print(f"  {day}   {full(c):>14,} tokens   (in {c['input']:,} / out {c['output']:,} / cache {c['cache_creation']+c['cache_read']:,})")

print()
print("Models seen:", dict(models.most_common()))
