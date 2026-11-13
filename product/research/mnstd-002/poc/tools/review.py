"""C6 — project the register into a DERIVED v1 build input as native Metanorma reviewer annotations.

* The committed v1 source is never written (D4/C6.3). The derived copy differs from v1 only by:
  (1) `:presentation-metadata-render-document-annotations: true` in the header (C6.4 mechanism; stage stays 30 = CD),
  (2) anchor-only lines/inline anchors `[[rv-eN]]` on targets that have no author anchor (paragraphs, list items)
      or that must not be targeted whole (tables: anchored on the first header cell — a whole-table `from` makes
      the PDF fail, findings-W4 §0.5),
  (3) one `[reviewer=…,date=…,from=…,to=…]` + `****` sidebar per register comment, appended at the end
      (review_cleanup moves every annotation into <annotation-container>, findings-W4 §2).
* HTML: metanorma-iso 3.5.14 renders no annotations in HTML (findings-W4 §0.3). Per ruling R2 we inject
  <aside class="mn-review-glue"> nodes from the native semantic <annotation> data, labelled as glue, into a
  separate file draft.review-glue.html. The native draft.html is left as produced.
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import html
import re
import shutil
import zlib
from pathlib import Path

from common import N, dump_json, local, text_of
from resolver import Doc

RENDER_ATTR = ":presentation-metadata-render-document-annotations: true"


def project(v1: Doc, v1_src: Path, register: list[dict], out: Path) -> dict:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for f in sorted(v1_src.iterdir()):
        if f.is_file():
            shutil.copy(f, out / f.name)
    lines = (out / "draft.adoc").read_text(encoding="utf-8").split("\n")
    elem_block = {}
    for b in v1.blocks:
        e = v1.block_elem.get(b["idx"])
        if e is not None and e.get("id") not in elem_block:
            elem_block[e.get("id")] = b
    anchors: dict[str, str] = {}
    inserts: list[tuple[int, str, str]] = []  # (0-based line, kind, anchor)

    def target(eid: str) -> str:
        if eid in anchors:
            return anchors[eid]
        e = v1.by_id[eid]
        tag = local(e.tag)
        b = elem_block.get(eid)
        if tag == "table":
            if b is None:
                raise SystemExit(f"review: no source block for table {eid}")
            a = f"rv-e{len(anchors) + 1}"
            ln = b["line"]  # the |=== line; first header row follows
            k = ln
            while not lines[k].startswith("|"):
                k += 1
            inserts.append((k, "cell", a))
        elif e.get("anchor"):
            a = e.get("anchor")
        elif tag == "li":
            a = f"rv-e{len(anchors) + 1}"
            inserts.append((b["line"] - 1, "item", a))
        elif b is not None:
            a = f"rv-e{len(anchors) + 1}"
            inserts.append((b["line"] - 1, "block", a))
        else:
            raise SystemExit(f"review: element {eid} has neither an anchor nor a source block")
        anchors[eid] = a
        return a

    blocks = []
    for r in sorted(register, key=lambda x: x["id"]):
        frm = target(r["resolved_id"])
        to = target(r["resolved_to_id"]) if r.get("resolved_to_id") else frm
        where = r["clause"] + (f"/{r['element']}" if r["element"] else "")
        body = (f"[{r['id']}] MB/NC {r['mb']} | type {r['type']} | {where} | {r['channel']}: {r['comment']}"
                + (f" Proposed change: {r['proposed_change']}" if r["proposed_change"] else ""))
        blocks.append({"id": r["id"], "from": frm, "to": to, "reviewer": f"{r['reviewer']} ({r['mb']})", "date": r["date"],
                       "text": body})
    for ln, kind, a in sorted(inserts, key=lambda x: x[0], reverse=True):
        if kind == "block":
            lines.insert(ln, f"[[{a}]]")
        elif kind == "cell":
            lines[ln] = re.sub(r"^\|\s*", f"| [[{a}]]", lines[ln], count=1)
        elif kind == "item":
            lines[ln] = re.sub(r"^(\*+|\.+)\s+", lambda m: f"{m.group(1)} [[{a}]]", lines[ln], count=1)
    hdr_end = lines.index("")
    lines.insert(hdr_end, RENDER_ATTR)
    while lines and lines[-1] == "":
        lines.pop()
    for bl in blocks:
        lines += ["", f'[reviewer="{bl["reviewer"]}",date={bl["date"]},from={bl["from"]},to={bl["to"]}]', "****",
                  bl["text"], "****"]
    (out / "draft.adoc").write_text("\n".join(lines) + "\n", encoding="utf-8")
    plan = {"blocks": blocks, "inserted_anchors": {k: v for k, v in sorted(anchors.items()) if v.startswith("rv-")}}
    dump_json(plan, out.parent / "projection-plan.json")
    return plan


# ---------------- counting (C6.2) ----------------
def sem_annotations(xml: Path) -> list[dict]:
    root = __import__("xml.etree.ElementTree", fromlist=["x"]).parse(xml).getroot()
    out = []
    for a in root.iter(N + "annotation"):
        out.append({"reviewer": a.get("reviewer"), "type": a.get("type"), "from": a.get("from"), "to": a.get("to"),
                    "date": a.get("date"), "text": " ".join(text_of(a).split())})
    return out


def _pdf_str(raw: bytes) -> str:
    raw = raw.strip()
    if raw.startswith(b"<") and raw.endswith(b">"):
        b = bytes.fromhex(re.sub(rb"\s", b"", raw[1:-1]).decode())
    else:
        s = raw[1:-1]
        b = bytearray()
        i = 0
        while i < len(s):
            c = s[i]
            if c == 0x5C and i + 1 < len(s):
                n = s[i + 1]
                m = {ord("n"): 10, ord("r"): 13, ord("t"): 9, ord("b"): 8, ord("f"): 12}
                if n in m:
                    b.append(m[n]); i += 2
                elif 0x30 <= n <= 0x37:
                    j = i + 1
                    oct_ = b""
                    while j < len(s) and len(oct_) < 3 and 0x30 <= s[j] <= 0x37:
                        oct_ += bytes([s[j]]); j += 1
                    b.append(int(oct_, 8) & 0xFF); i = j
                elif n in (10, 13):
                    i += 2
                else:
                    b.append(n); i += 2
            else:
                b.append(c); i += 1
        b = bytes(b)
    if b.startswith(b"\xfe\xff"):
        return b[2:].decode("utf-16-be", errors="replace")
    return b.decode("latin-1")


_STR = rb"(\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f\s]*>)"


def pdf_annotations(pdf: Path) -> list[dict]:
    data = pdf.read_bytes()
    chunks = [data]
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        try:
            chunks.append(zlib.decompress(m.group(1)))
        except zlib.error:
            pass
    allb = b"\n".join(chunks)
    out = []
    for m in re.finditer(rb"<<((?:(?!<<|>>).|<<(?:(?!>>).)*>>)*?/Subtype\s*/Text\b(?:(?!<<|>>).|<<(?:(?!>>).)*>>)*?)>>", allb, re.S):
        d = m.group(1)
        t = re.search(rb"/T\s*" + _STR, d, re.S)
        c = re.search(rb"/Contents\s*" + _STR, d, re.S)
        out.append({"T": _pdf_str(t.group(1)) if t else "", "Contents": _pdf_str(c.group(1)) if c else ""})
    return out


def inject_html(native: Path, anns: list[dict], out: Path) -> int:
    h = native.read_text(encoding="utf-8")
    n = 0
    for a in anns:
        if a["reviewer"] == "Metanorma":
            continue
        aside = ('<aside class="mn-review-glue" data-glue="mnstd-002 R2: injected from native semantic &lt;annotation&gt;" '
                 f'data-comment-id="{html.escape(a["cid"])}" data-from="{html.escape(a["from"] or "")}" data-to="{html.escape(a["to"] or "")}" '
                 'style="border:1px solid #c60;background:#fff4e5;margin:4px 0;padding:4px;font-size:90%">'
                 f'<b>Reviewer:</b> {html.escape(a["reviewer"] or "")} &#183; <b>Date:</b> {html.escape((a["date"] or "")[:10])}'
                 f'<br/>{html.escape(a["text"])}</aside>')
        m = re.search(r'<([a-zA-Z0-9]+)\b[^>]*\bid="' + re.escape(a["from"] or "") + r'"[^>]*>', h)
        if not m:
            continue
        pos = m.end()
        if m.group(1).lower() == "a" and h[pos:pos + 4] == "</a>":
            pos += 4
        h = h[:pos] + aside + h[pos:]
        n += 1
    style = '<style>aside.mn-review-glue:before{content:"review annotation (glue rendering of native data)";display:block;font-style:italic;color:#c60}</style>'
    h = h.replace("</head>", style + "</head>", 1)
    out.write_text(h, encoding="utf-8")
    return n
