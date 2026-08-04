# shd-007 W4 — the held-out coding task

**Frozen 2026-08-04, before the first measurement arm.** Identical across every arm (MoE / dense) and
every harness (aider / Claude Code T3a). Any change to this file or to `fixture/` after the first arm
invalidates the comparison and must be recorded as a deviation, not edited in silently.

## Why this task and not a public benchmark

A published benchmark (SWE-bench, HumanEval, Aider's exercism set) is in the training data of every model
under test. This fixture is bespoke and unpublished, so a pass is evidence the model *worked the problem*
rather than recalled it. That matters more here than comparability to other people's numbers, because
shd-007's claim is about **our** stack on **our** hardware.

## The task, as given to the harness

> The test suite in `tests/` is the specification and is correct. It currently fails. Fix the code under
> `roster/` until `python -m pytest` passes. **Do not edit anything under `tests/`.** The docstrings in
> `roster/` describe the intended behaviour — where the code and its own docstring disagree, the docstring
> is right.

## Shape of the problem

Four defects across three modules. They interact: the parser bug changes the numbers every other module
sees, so a fix applied to `report.py` alone looks wrong until the parser is also fixed. This is deliberate
— it defeats one-shot single-file pattern matching and forces a read → edit → run → re-read loop.

| # | File | Defect | Only observable when |
|---|---|---|---|
| 1 | `roster/parser.py` | `parse_line` subtracts 1 from the end hour — the spec's end hour is exclusive-of-nothing, i.e. taken as given | any shift is parsed at all |
| 2 | `roster/rules.py` | rest is measured from `day*24 + end` instead of `end_abs`, ignoring midnight wrap | the earlier shift wraps past midnight |
| 3 | `roster/report.py` | `totals_by_person` buckets by raw name though its docstring specifies case-insensitive identity | the roster spells one person two ways |
| 4 | `roster/report.py` | `busiest` breaks ties with `max`, which picks the alphabetically *last* name | two people tie on hours |

Defects 2 and 4 are invisible until 1 and 3 are fixed — the agent cannot see all four failures at the
start, so it must re-run the suite rather than plan once and execute.

## Verified before freeze

- Seeded fixture: **5 failed, 3 passed** (`python -m pytest -q`).
- Reference solution: **8 passed**. The task is solvable; a failure is the harness's or the model's, not
  the fixture's.
- Runtime: ~0.05 s, no network, no non-determinism. The suite is not a confound in any timing measurement.

## Tool-call floor

The scope requires **≥6–8 sequential tool calls**. A minimum honest path is: list files → read `parser.py`
→ run pytest → edit `parser.py` → read `report.py` → edit `report.py` → run pytest → read `rules.py` →
edit `rules.py` → run pytest. Ten calls, of which none can be skipped without guessing. Actual call counts
are recorded per harness in the W7 transcripts, and a run that completes in materially fewer calls is
flagged for inspection rather than credited.

## Pass criterion

`python -m pytest` exits 0 on a clean copy of `fixture/`, with `git diff` confined to `roster/`. A run that
edits `tests/` **fails**, however green the suite goes — that is the task's built-in reward-hacking check,
and it is checked mechanically, not by reading the transcript.
