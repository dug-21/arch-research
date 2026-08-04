"""Fairness rules applied to a parsed roster."""

from .parser import Shift

MIN_REST_HOURS = 10
MAX_CONSECUTIVE_DAYS = 5


def rest_violations(shifts: list[Shift]) -> list[tuple[Shift, Shift]]:
    """Pairs of consecutive shifts for one person with too little rest between."""
    out = []
    for name in {s.name for s in shifts}:
        own = sorted((s for s in shifts if s.name == name), key=lambda s: s.start_abs)
        for earlier, later in zip(own, own[1:]):
            rest = later.start_abs - (earlier.day * 24 + earlier.end)
            if rest < MIN_REST_HOURS:
                out.append((earlier, later))
    return out


def consecutive_day_violations(shifts: list[Shift]) -> list[str]:
    """Names working more than MAX_CONSECUTIVE_DAYS days in a row."""
    out = []
    for name in {s.name for s in shifts}:
        days = sorted({s.day for s in shifts if s.name == name})
        run = 1
        longest = 1
        for prev, cur in zip(days, days[1:]):
            run = run + 1 if cur == prev + 1 else 1
            longest = max(longest, run)
        if longest > MAX_CONSECUTIVE_DAYS:
            out.append(name)
    return sorted(out)
