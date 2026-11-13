"""Shared helpers for the mnstd-002 POC glue (Python 3.14 stdlib only — N2.3: no third-party deps).

Authored by factory-poc. Everything here is deterministic: sorted keys, LF line endings, no clocks.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

POC = Path(__file__).resolve().parent.parent
NS = "https://www.metanorma.org/ns/standoc"
N = "{" + NS + "}"
MN_IMAGE = "metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da"
FONT_CACHE = Path(os.environ.get("MNSTD_FONT_CACHE", str(Path.home() / ".cache" / "mnstd-002-fonts")))
SOURCE_DATE_EPOCH = "1794528000"  # 2026-11-13T00:00:00Z — fixed, never the clock

# ISO 2012-03 commenting template, column order (findings-W1 §3.1). Register key on the left.
ISO_COLUMNS = [
    ("mb", "MB/NC"),
    ("line", "Line number"),
    ("clause", "Clause/Subclause"),
    ("element", "Paragraph/Figure/Table/Note"),
    ("type", "Type of comment"),
    ("comment", "Comments"),
    ("proposed_change", "Proposed change"),
    ("observations", "Observations of the secretariat"),
]
ISO_KEYS = [k for k, _ in ISO_COLUMNS]
TYPES = ("ge", "te", "ed")
DISPOSITIONS = ("accept", "modify", "reject")
REGISTER_ID_RE = re.compile(r"^(?:PR-)?[A-Z]{2}-\d{2}-\d{3}$")
ANY_REGISTER_ID_RE = re.compile(r"(?<![A-Za-z0-9-])(?:PR-)?[A-Z]{2}-\d{2}-\d{3}(?![0-9-])")


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def local(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def text_of(e) -> str:
    return "".join(e.itertext())


# ---------- text normaliser (declared in RESULT.md; findings-W2 §5) ----------
_MARKUP = [
    (re.compile(r"\*([^*]+)\*"), r"\1"),
    (re.compile(r"_([^_]+)_"), r"\1"),
    (re.compile(r"`([^`]+)`"), r"\1"),
    (re.compile(r"\^([^^]+)\^"), r"\1"),
    (re.compile(r"~([^~]+)~"), r"\1"),
]


def norm(s: str, strip_markup: bool = False) -> str:
    s = unicodedata.normalize("NFC", s or "")
    if strip_markup:
        for rx, rep in _MARKUP:
            s = rx.sub(rep, s)
    s = (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
         .replace("…", "...").replace("​", "").replace(" ", " ").replace(" ", " ")
         .replace(" ", " "))
    s = re.sub(r"\s*—\s*", " -- ", s)
    return re.sub(r"\s+", " ", s).strip()


# ---------- deterministic serialisation ----------
def dump_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=False, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _yaml_scalar(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    # JSON string syntax is valid YAML double-quoted scalar syntax.
    return json.dumps(str(v), ensure_ascii=False)


def to_yaml(obj, indent: int = 0) -> str:
    """Minimal deterministic YAML emitter (output only) for dict/list/scalar trees."""
    pad = "  " * indent
    out = []
    if isinstance(obj, dict):
        if not obj:
            return pad + "{}\n"
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                out.append(f"{pad}{k}:\n{to_yaml(v, indent + 1)}")
            elif isinstance(v, (dict, list)):
                out.append(f"{pad}{k}: {'{}' if isinstance(v, dict) else '[]'}\n")
            else:
                out.append(f"{pad}{k}: {_yaml_scalar(v)}\n")
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and item:
                body = to_yaml(item, indent + 1)
                first, _, rest = body.partition("\n")
                out.append(f"{pad}- {first.strip()}\n{rest}")
            elif isinstance(item, list) and item:
                out.append(f"{pad}-\n{to_yaml(item, indent + 1)}")
            else:
                out.append(f"{pad}- {_yaml_scalar(item)}\n")
    else:
        out.append(pad + _yaml_scalar(obj) + "\n")
    return "".join(out)


def dump_yaml(obj, path: Path, header: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + to_yaml(obj), encoding="utf-8")


def dump_csv(rows: list[dict], fields: list[str], path: Path, headers: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(headers or fields)
    for r in rows:
        w.writerow(["" if r.get(f) is None else r.get(f) for f in fields])
    path.write_text(buf.getvalue(), encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- process helpers ----------
def run(cmd: list[str], check: bool = True, **kw) -> subprocess.CompletedProcess:
    p = subprocess.run(cmd, text=True, capture_output=True, **kw)
    if check and p.returncode != 0:
        die(f"command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p


def docker_base(workdir: Path) -> list[str]:
    """Every gated container run: pinned digest, --network none (N2.1, N6.1/R1)."""
    return [
        "docker", "run", "--rm", "--network", "none",
        "-e", f"SOURCE_DATE_EPOCH={SOURCE_DATE_EPOCH}",
        "-v", f"{FONT_CACHE / 'fontist'}:/config",
        "-v", f"{FONT_CACHE / 'metanorma'}:/root/.metanorma",
        "-v", f"{workdir}:/metanorma", "-w", "/metanorma",
        MN_IMAGE,
    ]


def mn_compile(workdir: Path, adoc: str, exts: str = "xml,html,pdf,rxl", log: Path | None = None) -> int:
    """Compile inside the pinned image as root, then chown back (findings-W0 §2.3: --user breaks fontist;
    -o is broken when xml is requested, so compile in place in a per-build copy)."""
    uid, gid = os.getuid(), os.getgid()
    inner = (f"metanorma compile -t iso --agree-to-terms --no-install-fonts -x {exts} {adoc}; rc=$?; "
             f"chown -R {uid}:{gid} /metanorma; exit $rc")
    p = subprocess.run(docker_base(workdir) + ["sh", "-c", inner], text=True, capture_output=True)
    # An aborted mn2pdf leaves randomly named scratch (_tmp_images_<uuid>/, <stem><date>-<rand>.xml_tmp).
    # It is toolchain debris, not an output; remove it so the artefact set is comparable across runs (N1.2).
    import shutil as _sh
    for d in Path(workdir).glob("_tmp_images_*"):
        _sh.rmtree(d, ignore_errors=True)
    for f in Path(workdir).glob("*.xml_tmp"):
        f.unlink()
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(f"$ metanorma compile -t iso --agree-to-terms --no-install-fonts -x {exts} {adoc}\n"
                       f"{p.stdout}\n--- stderr ---\n{p.stderr}\n--- exit {p.returncode} ---\n", encoding="utf-8")
    return p.returncode


def srcmap(srcdir: Path, adoc: str, out: Path) -> None:
    """Asciidoctor sourcemap, run with the image's Ruby (N2.2: no host Ruby)."""
    cmd = ["docker", "run", "--rm", "--network", "none",
           "-v", f"{srcdir}:/metanorma:ro", "-v", f"{POC / 'tools'}:/tools:ro", "-w", "/metanorma",
           MN_IMAGE, "ruby", "/tools/srcmap.rb", adoc]
    p = run(cmd)
    out.write_text(p.stdout, encoding="utf-8")


# ---------- err.html parser (validation log) ----------
_ROW = re.compile(r'<tr class="severity(\d)">\s*<td>(.*?)</td>\s*<th><code>(.*?)</code></th>\s*<td>(.*?)</td>\s*'
                  r'<td>(.*?)</td>\s*<td><pre>(.*?)</pre></td>\s*<td>(\d)</td></tr>', re.S)
_UUID = re.compile(r"_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s).replace("​", "").replace("­", "")
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'").replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip()


def parse_errhtml(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for m in _ROW.finditer(path.read_text(encoding="utf-8", errors="replace")):
        rows.append({
            "severity": int(m.group(7)),
            "code": _clean(m.group(4)),
            "location": _UUID.sub("_UUID", _clean(m.group(3))),
            "message": _UUID.sub("_UUID", _clean(m.group(5))),
        })
    return rows


ASCIIDOCTOR_DIAG = re.compile(r"^asciidoctor: (ERROR|WARNING|FATAL)\b.*$", re.M)
