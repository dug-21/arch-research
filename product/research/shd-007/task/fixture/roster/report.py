"""Aggregate a roster into a fairness report."""

from .parser import Shift
from . import rules


def totals_by_person(shifts: list[Shift]) -> dict[str, int]:
    """Total hours worked per person.

    People are identified by name case-insensitively -- rosters are typed by
    hand and "ana" and "Ana" are the same person -- but the canonical spelling
    reported back is the one that sorts first.
    """
    out: dict[str, int] = {}
    for s in shifts:
        out[s.name] = out.get(s.name, 0) + s.hours
    return out


def build_report(spec_shifts: list[Shift]) -> dict:
    """Assemble the fairness report.

    "busiest" is the person with the most hours. Where two people are tied on
    hours the alphabetically first name wins, so the report is stable no matter
    what order the roster was typed in. An empty roster has no busiest person.
    """
    totals = totals_by_person(spec_shifts)
    return {
        "totals": totals,
        "busiest": max(totals, key=lambda k: (totals[k], k)) if totals else None,
        "rest_violations": [
            (a.name, a.day, b.day) for a, b in rules.rest_violations(spec_shifts)
        ],
        "overworked": rules.consecutive_day_violations(spec_shifts),
    }
