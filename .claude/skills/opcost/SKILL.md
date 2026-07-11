---
name: opcost
description: Accurate per-repo Claude token reporting, broken down by model, rolled up daily and weekly. Reads this machine's local Claude Code transcripts (~/.claude/projects) and reports RAW token consumption (input / output / cache-write / cache-read) for the current repo. No dollars, no budget — just the honest, observable numbers so you can watch real activity and set a threshold from data later. Use when the user asks "how many tokens is this repo using", "usage by model", "daily/weekly Claude consumption", "which model is burning the most tokens here". Portable — drop into ~/.claude/skills/ to run from any repo.
---

# opcost — per-repo token reporting, by model, daily + weekly

Answers **"how many tokens is this repo consuming, by model, over time?"** — accurately,
from the one thing that's actually observable: local transcript token counts.

## Run it
```bash
python3 ~/.claude/skills/opcost/opcost.py           # current repo, last 14 days + weekly
python3 ~/.claude/skills/opcost/opcost.py --days 30 # widen the daily window
python3 ~/.claude/skills/opcost/opcost.py --repo NAME   # a specific repo
python3 ~/.claude/skills/opcost/opcost.py --all         # every repo on this machine
python3 ~/.claude/skills/opcost/opcost.py --cost        # add a NOTIONAL $-equiv column (see caveat)
```

## What it reports
- **BY MODEL** — per-model totals with the full four-class split: `input`, `output`,
  `cache_wr` (cache creation), `cache_rd` (cache read), and TOTAL. This is where the shape
  lives — cache-read is typically ~85% of tokens, output (the actual generated work) a few %.
- **WEEKLY** — total tokens per model per week (week boundary from `reset_weekday` in
  `~/.claude/opcost.config.json`, default Monday).
- **DAILY** — total tokens per model per day, over the last `--days`.

Accuracy note: token counts are trustworthy **only when all four usage classes are summed** —
a naive `input + output` sum captures <2% of real usage (cache dominates). This tool sums all
four. (The "Claude Code token counts are 10–100× off" reports are that field-selection error.)

## Scope — read this before trusting a percentage
Reads **only Claude Code transcripts on THIS machine** (`~/.claude/projects/`). It does **not**
see claude.ai web, Cowork, other machines, or the same account used elsewhere. So a per-repo
number is honest *for this machine's Claude Code*, not for your whole Claude footprint.

On a **Max/Pro subscription** there is no per-token bill and no exposed quota meter (the real
5h/weekly meter is not programmatically available — see `product/research/opcost-001/`). So
**tokens are the accurate primitive**; the optional `--cost` column is a *notional* list-price
weight (useful only for relative model comparison), **not** what your subscription costs you.

## Where this is headed
Let it accrue a couple of weeks, read the weekly by-model trend, then set a data-driven
threshold. Budget/pacing machinery exists (git history on branch `opcost-skill`) and can be
switched back on once there's a real baseline to pace against.

Design + evidence: goal `opcost` (Unimatrix #113); findings in `product/research/opcost-001/`.
