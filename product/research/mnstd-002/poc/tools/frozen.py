"""Freeze / verify the task: fixtures, pass-check expectations, the v1 source and the warnings map.
`frozen.py write` records sha256 of every frozen file into task/FROZEN.sha256 (done once, committed BEFORE the
first gated run). `frozen.py verify [root]` recomputes and fails on any difference (tampered tests are detected
mechanically, not by reading a transcript). Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import POC, sha256  # noqa: E402

SCOPE = POC.parent


def frozen_files(root: Path) -> list[Path]:
    files = sorted(p for p in (root / "task").rglob("*") if p.is_file() and p.name != "FROZEN.sha256")
    files += sorted(p for p in (root / "poc" / "src").rglob("*") if p.is_file())
    files += [root / "poc" / "warnings-explained.json"]
    return files


def write(root: Path = SCOPE):
    lines = [f"{sha256(p)}  {p.relative_to(root)}" for p in frozen_files(root)]
    (root / "task" / "FROZEN.sha256").write_text("\n".join(lines) + "\n")
    print(f"frozen: {len(lines)} files")


def verify(root: Path = SCOPE) -> list[str]:
    man = root / "task" / "FROZEN.sha256"
    if not man.exists():
        return ["task/FROZEN.sha256 missing"]
    want = {}
    for l in man.read_text().split("\n"):
        if l.strip():
            h, p = l.split("  ", 1)
            want[p] = h
    have = {str(p.relative_to(root)): sha256(p) for p in frozen_files(root)}
    probs = [f"changed: {p}" for p in sorted(want) if p in have and have[p] != want[p]]
    probs += [f"missing: {p}" for p in sorted(set(want) - set(have))]
    probs += [f"unfrozen new file: {p}" for p in sorted(set(have) - set(want))]
    return probs


if __name__ == "__main__":
    if sys.argv[1] == "write":
        write()
    else:
        root = Path(sys.argv[2]) if len(sys.argv) > 2 else SCOPE
        p = verify(root)
        for x in p:
            print("FROZEN-CHECK:", x, file=sys.stderr)
        print(f"frozen: {'ok' if not p else 'TAMPERED'}")
        sys.exit(1 if p else 0)
