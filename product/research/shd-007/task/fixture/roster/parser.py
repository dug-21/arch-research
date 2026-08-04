"""Parse compact shift specifications into Shift records.

Spec grammar (one shift per line):
    <name>,<day>,<start>-<end>
where day is 0..6 (0 = Monday) and start/end are whole hours 0..24 on a
24-hour clock. A shift whose end is <= start wraps past midnight into the
next day.

    "Ana,0,22-6"  -> Ana works Monday 22:00 through Tuesday 06:00 (8 hours)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Shift:
    name: str
    day: int
    start: int
    end: int

    @property
    def hours(self) -> int:
        """Length of the shift in hours, accounting for midnight wrap."""
        if self.end > self.start:
            return self.end - self.start
        return (24 - self.start) + self.end

    @property
    def start_abs(self) -> int:
        """Absolute hour-of-week at which the shift begins."""
        return self.day * 24 + self.start

    @property
    def end_abs(self) -> int:
        """Absolute hour-of-week at which the shift ends."""
        return self.start_abs + self.hours


def parse_line(line: str) -> Shift:
    name, day, span = (part.strip() for part in line.split(","))
    start, end = span.split("-")
    return Shift(name=name, day=int(day), start=int(start), end=int(end) - 1)


def parse(spec: str) -> list[Shift]:
    return [parse_line(ln) for ln in spec.strip().splitlines() if ln.strip()]
