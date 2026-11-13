"""Font pinning (owner ruling 1, mnstd-002 rework 1): a manifest of the provisioned font set, committed in the repo
(the manifest only, never the fonts). `fontpin.py write` records it; `fontpin.py verify` recomputes and exits 1 on
any difference. `make fonts` runs verify when the manifest exists and write (first pin) when it does not.

Pinned: every file in <cache>/metanorma/fonts (the font files Metanorma loads; mounted at /root/.metanorma) by
sha256 + size, with the font's own version string (OpenType name table, nameID 5) and full name (nameID 4) where the
file is a parseable sfnt; and the commit of the fontist formulas checkout that resolved them
(<cache>/fontist/versions/v5/formulas, read from .git without running git). NOT pinned (declared): fontist index
YAML (rewritten with timestamps), fontist/downloads (transient), the warm-up outputs.
Usage: fontpin.py write|verify [--cache DIR] [--manifest FILE]
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import FONT_CACHE, POC, sha256  # noqa: E402

MANIFEST = POC / "fonts" / "MANIFEST.json"


def _name_table(path: Path) -> dict:
    """nameID 4 / 5 from an sfnt (TTF/OTF). Returns {} for anything else (zip, ttc, unparseable)."""
    try:
        with open(path, "rb") as f:
            head = f.read(12)
            if len(head) < 12 or head[:4] not in (b"\x00\x01\x00\x00", b"OTTO", b"true"):
                return {}
            n = struct.unpack(">H", head[4:6])[0]
            dirs = f.read(16 * n)
            for i in range(n):
                tag, _, off, ln = struct.unpack(">4sIII", dirs[16 * i:16 * i + 16])
                if tag != b"name":
                    continue
                f.seek(off)
                t = f.read(ln)
                _, count, soff = struct.unpack(">HHH", t[:6])
                out = {}
                for j in range(count):
                    pid, eid, lid, nid, l2, o2 = struct.unpack(">6H", t[6 + 12 * j:18 + 12 * j])
                    if nid not in (4, 5) or nid in out:
                        continue
                    raw = t[soff + o2:soff + o2 + l2]
                    if pid == 3 or pid == 0:
                        out[nid] = raw.decode("utf-16-be", "replace")
                    elif pid == 1 and eid == 0:
                        out[nid] = raw.decode("latin-1")
                return {"full_name": out.get(4), "version": out.get(5)}
    except (OSError, struct.error):
        return {}
    return {}


def _git_head(repo: Path) -> str | None:
    g = repo / ".git"
    try:
        h = (g / "HEAD").read_text().strip()
        if not h.startswith("ref: "):
            return h
        ref = h[5:]
        p = g / ref
        if p.exists():
            return p.read_text().strip()
        for line in (g / "packed-refs").read_text().split("\n"):
            if line.endswith(" " + ref):
                return line.split(" ", 1)[0]
    except OSError:
        return None
    return None


def compute(cache: Path) -> dict:
    fonts_dir = cache / "metanorma" / "fonts"
    files = []
    for p in sorted(fonts_dir.iterdir()) if fonts_dir.is_dir() else []:
        if p.is_file():
            e = {"file": p.name, "sha256": sha256(p), "bytes": p.stat().st_size}
            meta = _name_table(p)
            e["version"] = meta.get("version") or "not available (not an sfnt font file)"
            if meta.get("full_name"):
                e["full_name"] = meta["full_name"]
            files.append(e)
    return {"schema": "mnstd-002 font pin v1",
            "fontist_formulas_commit": _git_head(cache / "fontist" / "versions" / "v5" / "formulas") or "not available",
            "font_dir": "metanorma/fonts", "files": files}


def diff(want: dict, have: dict) -> list[str]:
    probs = []
    if want.get("fontist_formulas_commit") != have.get("fontist_formulas_commit"):
        probs.append(f"fontist formulas commit {have.get('fontist_formulas_commit')} != pinned {want.get('fontist_formulas_commit')}")
    w = {f["file"]: f for f in want.get("files", [])}
    h = {f["file"]: f for f in have.get("files", [])}
    probs += [f"missing font file: {n}" for n in sorted(set(w) - set(h))]
    probs += [f"unpinned font file: {n}" for n in sorted(set(h) - set(w))]
    for n in sorted(set(w) & set(h)):
        for k in ("sha256", "bytes", "version"):
            if w[n].get(k) != h[n].get(k):
                probs.append(f"{n}: {k} {h[n].get(k)} != pinned {w[n].get(k)}")
    if not h:
        probs.append("no font files found")
    return probs


def main(argv) -> int:
    mode = argv[0]
    cache = Path(argv[argv.index("--cache") + 1]) if "--cache" in argv else FONT_CACHE
    man = Path(argv[argv.index("--manifest") + 1]) if "--manifest" in argv else MANIFEST
    have = compute(cache)
    if mode == "write":
        if not have["files"]:
            print(f"fontpin: no font files under {cache}/metanorma/fonts", file=sys.stderr)
            return 1
        man.write_text(json.dumps(have, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"fontpin: wrote {man} ({len(have['files'])} files, formulas {have['fontist_formulas_commit']}); commit it")
        return 0
    if not man.exists():
        print(f"fontpin: manifest missing: {man}", file=sys.stderr)
        return 1
    probs = diff(json.loads(man.read_text(encoding="utf-8")), have)
    for p in probs:
        print(f"FONT-PIN MISMATCH: {p}", file=sys.stderr)
    print(f"fontpin: {'ok' if not probs else 'MISMATCH'} ({len(have['files'])} files in {cache}/metanorma/fonts)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
