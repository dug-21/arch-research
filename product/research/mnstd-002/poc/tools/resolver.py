"""C2 resolver — any location in the draft resolves to exactly one element (or is rejected with a reason).

Inputs per build directory: draft.xml (semantic), draft.presentation.xml (numbers), srcmap.json (Asciidoctor
sourcemap dumped in-container by srcmap.rb), draft.adoc (the compiled source copy).

  * C2.1 resolve(clause, element)   ISO locator -> semantic element id
  * C2.2 resolve_line(file, line)   AsciiDoc file:line -> enclosing element id + clause number
  * C2.3 every failure is an Err(code, message); never a nearest match
  * C2.4 map_versions(v1, v2)       v1 element -> v2 element; renumbering as old->new pairs

Anchoring policy (declared, findings-W0 §3.3 option 1): structural elements (clauses, terms, tables, figures,
notes, annex) carry author [[anchors]]; paragraphs and lists are NOT anchored and are aligned by text.
Numbers come from the presentation XML, joined to semantic ids via @semx-id (findings-W0 §2.5).
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import difflib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import N, NS, dump_json, load_json, local, norm, text_of  # noqa: E402

CONTAINERS = {"foreword", "introduction", "clause", "terms", "references", "annex"}
NUMBERED = {"clause", "terms", "references", "annex", "term"}
LEAF_ANYWHERE = {"note", "table", "figure"}


class Err(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code, self.message = code, message


class Doc:
    def __init__(self, build: Path, stem: str = "draft"):
        self.build = Path(build)
        self.stem = stem
        self.sem = ET.parse(self.build / f"{stem}.xml").getroot()
        self.pres = ET.parse(self.build / f"{stem}.presentation.xml").getroot()
        self.src_lines = (self.build / f"{stem}.adoc").read_text(encoding="utf-8").split("\n")
        sm = load_json(self.build / "srcmap.json")
        self.blocks = sm["blocks"]
        self.parent = {c: p for p in self.sem.iter() for c in p}
        self.by_id = {e.get("id"): e for e in self.sem.iter() if e.get("id")}
        self.by_anchor = {e.get("anchor"): e for e in self.sem.iter() if e.get("anchor")}
        self.order = {e: i for i, e in enumerate(self.sem.iter())}
        self._numbers()
        self._tracked()
        self._join_blocks()

    # ---------------- numbers (presentation XML) ----------------
    def _numbers(self):
        self.number: dict[str, str] = {}
        for e in self.pres.iter():
            sid = e.get("semx-id")
            t = local(e.tag)
            if not sid or sid not in self.by_id:
                continue
            if t in ("table", "figure", "note"):
                num = e.get("autonum")
                kind = {"table": "Table", "figure": "Figure", "note": "Note"}[t]
                self.number[sid] = f"{kind} {num}" if num else f"{kind}"  # sole note: "Note" (unnumbered)
            elif t in NUMBERED:
                ft = e.find(N + "fmt-title")
                lab = None
                if ft is not None:
                    span = ft.find(f".//{N}span[@class='fmt-caption-label']")
                    if span is not None:
                        lab = norm("".join(span.itertext()))
                if lab is None and t == "term":
                    nm = e.find(N + "fmt-name")
                    if nm is not None:
                        span = nm.find(f".//{N}span[@class='fmt-caption-label']")
                        if span is not None:
                            lab = norm("".join(span.itertext()))
                if lab:
                    lab = re.sub(r"^Annex\s+", "", lab)
                    self.number[sid] = lab
        self.clause_index: dict[str, list[str]] = {}
        for sid, num in self.number.items():
            if local(self.by_id[sid].tag) in NUMBERED:
                self.clause_index.setdefault(num, []).append(sid)

    # ---------------- tracked element tree (for C2.4 and paragraph counting) ----------------
    def _is_tracked(self, e) -> bool:
        t = local(e.tag)
        p = self.parent.get(e)
        pt = local(p.tag) if p is not None else None
        if t in CONTAINERS:
            return not self._inside(e, {"bibdata", "boilerplate", "metanorma-extension", "annotation-container"})
        if t in LEAF_ANYWHERE:
            return not self._inside(e, {"table", "figure", "bibdata", "boilerplate", "annotation-container"})
        if t in ("p", "ul", "ol") and pt in CONTAINERS:
            return not self._inside(e, {"boilerplate", "annotation-container"})
        if t == "term" and pt == "terms":
            return True
        return False

    def _inside(self, e, tags) -> bool:
        p = self.parent.get(e)
        while p is not None:
            if local(p.tag) in tags:
                return True
            p = self.parent.get(p)
        return False

    def _tracked(self):
        self.tracked = [e for e in self.sem.iter() if self._is_tracked(e)]
        tset = set(self.tracked)
        self.tparent = {}
        for e in self.tracked:
            p = self.parent.get(e)
            while p is not None and p not in tset:
                p = self.parent.get(p)
            self.tparent[e] = p

    def own_text(self, e) -> str:
        t = local(e.tag)
        if t in CONTAINERS:
            ti = e.find(N + "title")
            return norm(text_of(ti)) if ti is not None else ""
        if t == "p":
            parts = [e.text or ""]
            for c in e:
                if local(c.tag) != "note":
                    parts.append(text_of(c))
                parts.append(c.tail or "")
            return norm("".join(parts))
        return norm(text_of(e))

    def clause_of(self, e) -> str:
        """Number of the nearest numbered clause-like element (itself included)."""
        x = e
        while x is not None:
            if x.get("id") in self.number and local(x.tag) in NUMBERED:
                return self.number[x.get("id")]
            if local(x.tag) in ("foreword", "introduction"):
                return local(x.tag)
            x = self.parent.get(x)
        return ""

    def container_of(self, e):
        x = self.parent.get(e)
        while x is not None and local(x.tag) not in CONTAINERS | {"term"}:
            x = self.parent.get(x)
        return x

    # ---------------- source blocks <-> elements (C2.2 join) ----------------
    @staticmethod
    def _src_norm(s: str) -> str:
        s = re.sub(r"<<[^>]*>>", "", s or "")
        s = re.sub(r"\[\[[^\]]*\]\]", "", s)
        return norm(s, strip_markup=True)

    def _join_blocks(self):
        self.block_elem: dict[int, object] = {}
        for b in self.blocks:
            e = self._map_block(b)
            if e is not None:
                self.block_elem[b["idx"]] = e
        self.authored = set(self.block_elem.values())

    def _map_block(self, b):
        if b.get("id") and b["id"] in self.by_anchor:
            return self.by_anchor[b["id"]]
        ctx = b["ctx"]
        par = self.blocks[b["parent"]] if b["parent"] is not None else None
        if ctx == "preamble":
            return self.sem.find(f".//{N}preface/{N}foreword")
        pe = self.block_elem.get(par["idx"]) if par is not None else None
        if pe is None and par is not None and par["ctx"] == "preamble":
            pe = self.sem.find(f".//{N}preface/{N}foreword")
        if pe is None:
            return None
        if local(pe.tag) == "term":  # definition text belongs to its term entry
            return pe
        if local(pe.tag) == "references":
            if ctx == "ulist":
                return pe
            if ctx == "list_item":
                sib = [x for x in self.blocks if x["parent"] == b["parent"] and x["ctx"] == "list_item"]
                items = [c for c in pe if local(c.tag) == "bibitem"]
                k = sib.index(b)
                return items[k] if k < len(items) else None
        if local(pe.tag) == "ul" and ctx == "list_item" and local(self.parent.get(pe).tag) == "references":
            return None
        if ctx == "paragraph":
            cands = [c for c in pe if local(c.tag) == "p"]
            want = self._src_norm(b.get("source") or "")
            best, score = None, 0.0
            for c in cands:
                if c in getattr(self, "block_elem", {}).values():
                    continue
                r = difflib.SequenceMatcher(None, want, self.own_text(c)).ratio()
                if r > score:
                    best, score = c, r
            return best if score >= 0.9 else None
        if ctx in ("ulist", "olist"):
            tag = "ul" if ctx == "ulist" else "ol"
            sib = [x for x in self.blocks if x["parent"] == b["parent"] and x["ctx"] == ctx]
            cands = [c for c in pe if local(c.tag) == tag]
            k = sib.index(b)
            return cands[k] if k < len(cands) else None
        if ctx == "list_item":
            sib = [x for x in self.blocks if x["parent"] == b["parent"] and x["ctx"] == "list_item"]
            cands = [c for c in pe if local(c.tag) == "li"]
            k = sib.index(b)
            if k >= len(cands):
                return None
            li = cands[k]
            if li.get("id"):
                return li
            p = li.find(N + "p")  # metanorma gives <li> no id; its first <p> carries the item's id
            return p if p is not None and p.get("id") else None
        return None

    # ---------------- C2.1 ----------------
    def resolve(self, clause: str, element: str | None = None) -> dict:
        clause = (clause or "").strip()
        element = (element or "").strip()
        if not clause:
            raise Err("clause_missing", "no clause/subclause given")
        if not re.fullmatch(r"(?:\d+|[A-Z])(?:\.\d+)*", clause):
            raise Err("clause_not_found", f"'{clause}' is not a clause/subclause/annex number (bare number or annex letter expected)")
        ids = self.clause_index.get(clause, [])
        if not ids:
            raise Err("clause_not_found", f"no clause, subclause, term or annex numbered '{clause}' in v1")
        if len(ids) > 1:
            raise Err("clause_ambiguous", f"'{clause}' matches {len(ids)} elements")
        ce = self.by_id[ids[0]]
        if not element:
            return self._ok(ce)
        m = re.fullmatch(r"para(?:graph)?\s*(\d+)?", element, re.I)
        if m:
            paras = [c for c in ce if local(c.tag) == "p" and c in self.authored]
            if m.group(1) is None:
                if len(paras) == 1:
                    return self._ok(paras[0])
                raise Err("element_ambiguous", f"'{element}' has no number and clause {clause} has {len(paras)} paragraphs")
            k = int(m.group(1))
            if not 1 <= k <= len(paras):
                raise Err("element_not_found", f"clause {clause} has {len(paras)} authored paragraph(s); 'para {k}' does not exist")
            return self._ok(paras[k - 1])
        m = re.fullmatch(r"(Table|Figure|Note)\s+([A-Z]\.\d+|\d+)", element)
        if not m:
            raise Err("element_unparseable", f"'{element}' is not 'para N', 'Table N', 'Figure N' or 'Note N'")
        kind, num = m.group(1), m.group(2)
        tag = kind.lower()
        if kind in ("Table", "Figure"):
            hits = [self.by_id[i] for i, n in self.number.items() if n == f"{kind} {num}" and local(self.by_id[i].tag) == tag]
            if not hits:
                total = sum(1 for i, n in self.number.items() if local(self.by_id[i].tag) == tag)
                raise Err("element_not_found", f"no {kind} {num} in v1 ({total} {tag}s exist)")
            if len(hits) > 1:
                raise Err("element_ambiguous", f"{kind} {num} matches {len(hits)} elements")
            if not self._descends(hits[0], ce):
                raise Err("element_not_in_clause", f"{kind} {num} exists but is in clause {self.clause_of(self.container_of(hits[0]))}, not {clause}")
            return self._ok(hits[0])
        # Note N: notes whose nearest container is this clause (not table/figure notes)
        notes = [e for e in self.tracked if local(e.tag) == "note" and self.container_of(e) is ce]
        if len(notes) == 1 and num == "1" and self.number.get(notes[0].get("id")) == "Note":
            r = self._ok(notes[0])
            r["normalized"] = "sole-note"
            return r
        hits = [e for e in notes if self.number.get(e.get("id")) == f"Note {num}"]
        if not hits:
            raise Err("element_not_found", f"clause {clause} has {len(notes)} note(s); 'Note {num}' does not exist")
        return self._ok(hits[0])

    def _descends(self, e, anc) -> bool:
        x = e
        while x is not None:
            if x is anc:
                return True
            x = self.parent.get(x)
        return False

    def _ok(self, e) -> dict:
        return {"id": e.get("id"), "anchor": e.get("anchor") or "", "tag": local(e.tag),
                "number": self.number.get(e.get("id"), ""), "clause": self.clause_of(e)}

    # ---------------- C2.2 ----------------
    def resolve_line(self, file: str, line: int) -> dict:
        if Path(file).name != f"{self.stem}.adoc":
            raise Err("line_unknown_file", f"'{file}' is not a source file of this document")
        if not 1 <= line <= len(self.src_lines):
            raise Err("line_out_of_range", f"line {line} is outside 1..{len(self.src_lines)}")
        header_end = self.src_lines.index("") + 1  # AsciiDoc header ends at the first blank line
        txt = self.src_lines[line - 1]
        if line <= header_end:
            raise Err("line_in_header", f"line {line} is in the document header (lines 1..{header_end}); it is not a body element")
        if not txt.strip():
            raise Err("line_blank", f"line {line} is blank; it belongs to no element")
        if txt.lstrip().startswith("//"):
            raise Err("line_comment", f"line {line} is an AsciiDoc comment; it is not rendered")
        located = [b for b in self.blocks if b.get("line")]
        if re.fullmatch(r"\s*(\[\[.*\]\]|\[.*\]|\.[^.\s].*)\s*", txt):
            # block metadata (anchor / attribute list / block title) belongs to the NEXT block
            nxt = [b for b in located if b["line"] > line]
            if not nxt:
                raise Err("line_unmapped", f"line {line} is block metadata with no following block")
            b = min(nxt, key=lambda x: (x["line"], -x["idx"]))
        else:
            prev = [x for x in located if x["line"] <= line]
            if not prev:
                raise Err("line_unmapped", f"line {line} precedes every body block")
            b = max(prev, key=lambda x: (x["line"], x["idx"]))
        e = self.block_elem.get(b["idx"])
        if e is None:
            raise Err("line_unmapped", f"line {line} falls in source block '{b['ctx']}' (line {b['line']}) that maps to no semantic element")
        r = self._ok(e)
        r["block_line"] = b["line"]
        r["block_ctx"] = b["ctx"]
        return r


# ---------------- C2.4 ----------------
def map_versions(d1: Doc, d2: Doc) -> dict:
    match: dict = {}
    rev: dict = {}
    t2set = set(d2.tracked)
    for a, e1 in d1.by_anchor.items():
        e2 = d2.by_anchor.get(a)
        if e1 in set(d1.tracked) and e2 is not None and e2 in t2set:
            match[e1], rev[e2] = e2, e1
    for e1 in d1.tracked:
        if e1 in match:
            continue
        p1 = d1.tparent[e1]
        if p1 is None:
            cands = [e for e in d2.tracked if d2.tparent[e] is None and local(e.tag) == local(e1.tag) and e not in rev]
        else:
            p2 = match.get(p1)
            if p2 is None:
                continue
            cands = [e for e in d2.tracked if d2.tparent[e] is p2 and local(e.tag) == local(e1.tag) and e not in rev]
        if not cands:
            continue
        t1 = d1.own_text(e1)
        exact = [c for c in cands if d2.own_text(c) == t1]
        if exact:
            best = exact[0]
        else:
            scored = [(difflib.SequenceMatcher(None, t1, d2.own_text(c)).ratio(), -d2.order[c], c) for c in cands]
            scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
            best = scored[0][2] if scored[0][0] >= 0.6 else None
        if best is not None:
            match[e1], rev[best] = best, e1
    rows, renum = [], []
    for e1 in d1.tracked:
        e2 = match.get(e1)
        n1 = d1.number.get(e1.get("id"), "")
        row = {"v1_id": e1.get("id"), "anchor": e1.get("anchor") or "", "tag": local(e1.tag),
               "v1_number": n1, "v1_clause": d1.clause_of(e1)}
        if e2 is None:
            row.update({"status": "deleted", "v2_id": "", "v2_number": "", "v2_clause": ""})
        else:
            n2 = d2.number.get(e2.get("id"), "")
            row.update({"status": "unchanged" if d1.own_text(e1) == d2.own_text(e2) else "modified",
                        "v2_id": e2.get("id"), "v2_number": n2, "v2_clause": d2.clause_of(e2)})
            if n1 and n2 and n1 != n2:
                renum.append({"anchor": row["anchor"], "tag": row["tag"], "old": n1, "new": n2})
        rows.append(row)
    inserted = [{"v2_id": e.get("id"), "anchor": e.get("anchor") or "", "tag": local(e.tag),
                 "v2_number": d2.number.get(e.get("id"), ""), "v2_clause": d2.clause_of(e),
                 "text": d2.own_text(e)[:80]} for e in d2.tracked if e not in rev]
    return {"elements": rows, "inserted": inserted, "renumbered": renum}


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("map")
    m.add_argument("v1")
    m.add_argument("v2")
    m.add_argument("out")
    a = ap.parse_args(argv)
    if a.cmd == "map":
        dump_json(map_versions(Doc(Path(a.v1)), Doc(Path(a.v2))), Path(a.out))


if __name__ == "__main__":
    main(sys.argv[1:])
