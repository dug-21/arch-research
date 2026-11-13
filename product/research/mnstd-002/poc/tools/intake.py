"""C3 intake — validate ISO comment sheets (CSV) and PR-channel candidates against v1, emit ONE register.

One validator, two adapters (findings-W1 §3.3): sheet rows and PR review comments go through the same rule set.
Rules (all evaluated per row; every reason collected):
  S0 sheet header/columns/version/document           -> whole sheet rejected, exit 2
  R1 missing_field:<f>   mb, clause (sheet) / line (pr), type, comment non-empty
  R2 bad_mb              ^[A-Z]{2}$ and equal to the sheet/review header MB
  R3 bad_type            exactly ge|te|ed (N4.2; full words rejected, not normalised)
  R4 bad_id / duplicate_id   reviewer id pattern; first occurrence wins in deterministic order
  R5 clause_*  R6 element_*  locator resolved through the C2 resolver (reason passed through verbatim)
  R7 bad_line            line, if given, is a positive integer (Q3: informational, not resolved for sheets)
  R8 observations_not_empty
  PR only: line_* (C2.2 reasons), line_not_in_diff (from the normaliser)
Exit: 0 all accepted · 1 any row rejected · 2 structural error / missing prerequisite.
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ISO_COLUMNS, ISO_KEYS, TYPES, die, dump_csv, dump_json, dump_yaml, load_json, N  # noqa: E402
from resolver import Doc, Err  # noqa: E402

SHEET_COLUMNS = ["id"] + ISO_KEYS
HEADER_KEYS = ["version", "document", "date", "project", "reviewer", "mb"]
SRC_ID_RE = re.compile(r"^[A-Z]{2,3}-\d{2,3}(-\d{3})?$")  # commenter's id pattern (findings-W1 §1)

REGISTER_FIELDS = (["id"] + ISO_KEYS +
                   ["source_id", "reviewer", "date", "channel", "source", "locator",
                    "resolved_id", "resolved_anchor", "resolved_tag", "resolved_clause", "resolved_to_id",
                    "source_branch", "source_commit", "source_path", "source_side", "source_line",
                    "source_start_line", "v1_line"])


def element_locator(doc: Doc, rid: str) -> str:
    """ISO 'Paragraph/Figure/Table' value for a resolved element (used for PR rows)."""
    e = doc.by_id[rid]
    tag = e.tag.split("}")[1]
    if tag in ("table", "figure", "note"):
        return doc.number.get(rid, "")
    if tag == "p":
        cont = doc.parent.get(e)
        paras = [c for c in cont if c.tag == N + "p" and c in doc.authored]
        return f"para {paras.index(e) + 1}" if e in paras else ""
    return ""


def read_sheet(path: Path):
    meta, lines = {}, path.read_text(encoding="utf-8").split("\n")
    body = []
    for ln in lines:
        if ln.startswith("#"):
            k, _, v = ln[1:].partition(":")
            meta[k.strip()] = v.strip()
        elif ln.strip():
            body.append(ln)
    rows = list(csv.reader(body))
    return meta, (rows[0] if rows else []), rows[1:]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--v1", required=True, help="v1 build dir (draft.xml, presentation, srcmap.json)")
    ap.add_argument("--sheets", nargs="*", default=[])
    ap.add_argument("--pr-candidates", default=None)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    out = Path(a.out)
    doc = Doc(Path(a.v1))
    docid = doc.sem.find(f"{N}bibdata/{N}docidentifier[@type='ISO']")
    docid = docid.text if docid is not None else ""

    accepted, rejects, structural = [], [], []
    seen_src = {}
    mb_ordinal: dict[tuple, int] = {}

    def ordinal(channel, mb, reviewer):
        key = (channel, mb)
        mb_ordinal.setdefault(key, [])
        if reviewer not in mb_ordinal[key]:
            mb_ordinal[key].append(reviewer)
        return mb_ordinal[key].index(reviewer) + 1

    def check_common(r, hdr_mb, reasons):
        for f in ("mb", "type", "comment"):
            if not (r.get(f) or "").strip():
                reasons.append(f"missing_field:{f}")
        if (r.get("mb") or "").strip() and not (re.fullmatch(r"[A-Z]{2}", r["mb"]) and r["mb"] == hdr_mb):
            reasons.append(f"bad_mb ('{r['mb']}' vs header '{hdr_mb}')")
        if (r.get("type") or "").strip() and r["type"] not in TYPES:
            reasons.append(f"bad_type ('{r['type']}' not in ge|te|ed)")
        if (r.get("line") or "").strip() and not re.fullmatch(r"[1-9]\d*", r["line"].strip()):
            reasons.append(f"bad_line ('{r['line']}')")
        if (r.get("observations") or "").strip():
            reasons.append("observations_not_empty (secretariat column must be empty at intake)")

    # ---------------- sheet adapter ----------------
    for sp in sorted(a.sheets):
        p = Path(sp)
        meta, header, rows = read_sheet(p)
        problems = []
        if header != SHEET_COLUMNS:
            problems.append(f"columns {header} != {SHEET_COLUMNS}")
        for k in HEADER_KEYS:
            if not meta.get(k):
                problems.append(f"header key '{k}' missing")
        if meta.get("version") and meta["version"] != "2012-03":
            problems.append(f"version {meta['version']} != 2012-03")
        if meta.get("document") and meta["document"] != docid:
            problems.append(f"document '{meta['document']}' != v1 docidentifier '{docid}'")
        if problems:
            structural.append({"sheet": str(p), "problems": problems})
            continue
        rr = ordinal("sheet", meta["mb"], meta["reviewer"])
        for i, cells in enumerate(rows, start=1):
            r = dict(zip(SHEET_COLUMNS, cells + [""] * (len(SHEET_COLUMNS) - len(cells))))
            src = f"{p.name}:row{i}"
            reasons = []
            check_common(r, meta["mb"], reasons)
            if not r["clause"].strip():
                reasons.append("missing_field:clause")
            sid = r["id"].strip()
            if sid and not SRC_ID_RE.fullmatch(sid):
                reasons.append(f"bad_id ('{sid}')")
            key = (p.name, sid)
            if sid and key in seen_src:
                reasons.append(f"duplicate_id ('{sid}' first used at {seen_src[key]})")
            elif sid:
                seen_src[key] = src
            res = None
            if r["clause"].strip():
                try:
                    res = doc.resolve(r["clause"], r["element"])
                except Err as x:
                    reasons.append(f"{x.code} ({x.message})")
            if reasons:
                rejects.append({"channel": "sheet", "source": src, "source_id": sid, "reasons": reasons})
                continue
            rid = f"{meta['mb']}-{rr:02d}-{i:03d}"
            accepted.append({
                "id": rid, **{k: r[k].strip() for k in ISO_KEYS},
                "source_id": sid, "reviewer": meta["reviewer"], "date": meta["date"], "channel": "sheet",
                "source": f"sheets/{p.name}:row{i}",
                "locator": " ".join(x for x in (r["clause"].strip(), r["element"].strip()) if x),
                "resolved_id": res["id"], "resolved_anchor": res["anchor"], "resolved_tag": res["tag"],
                "resolved_clause": res["clause"], "resolved_to_id": "",
                "source_branch": "", "source_commit": "", "source_path": "", "source_side": "",
                "source_line": "", "source_start_line": "", "v1_line": "",
            })

    # ---------------- PR adapter (candidates from prsim.normalize) ----------------
    if a.pr_candidates:
        for c in load_json(Path(a.pr_candidates)):
            reasons = list(c.get("pre_reasons", []))
            r = {"mb": c.get("mb", ""), "type": c.get("type", ""), "comment": c.get("comment", ""),
                 "line": str(c.get("v1_line") or ""), "observations": c.get("observations", "")}
            check_common(r, c.get("header_mb", ""), reasons)
            res = res_to = None
            if not reasons or all(not x.startswith("line_") for x in reasons):
                if c.get("v1_line"):
                    try:
                        res = doc.resolve_line(c["source_path"], int(c["v1_line"]))
                    except Err as x:
                        reasons.append(f"{x.code} ({x.message})")
                    if res and c.get("v1_end_line") and c["v1_end_line"] != c["v1_line"]:
                        try:
                            res_to = doc.resolve_line(c["source_path"], int(c["v1_end_line"]))
                        except Err as x:
                            reasons.append(f"range_end_{x.code} ({x.message})")
                elif not any(x.startswith("line_") for x in reasons):
                    reasons.append("missing_field:line")
            src = f"{c['review_file']}#{c['local_id']}"
            if reasons:
                rejects.append({"channel": "pr", "source": src, "source_id": str(c["local_id"]), "reasons": reasons})
                continue
            rr = ordinal("pr", c["mb"], c["reviewer"])
            rid = f"PR-{c['mb']}-{rr:02d}-{int(c['local_id']):03d}"
            accepted.append({
                "id": rid, "mb": c["mb"], "line": str(c["v1_line"]), "clause": res["clause"],
                "element": element_locator(doc, res["id"]), "type": c["type"], "comment": c["comment"],
                "proposed_change": c.get("proposed_change", ""), "observations": "",
                "source_id": str(c["local_id"]), "reviewer": c["reviewer"], "date": c["date"], "channel": "pr",
                "source": f"{c['source_branch']}@{c['source_commit']}:{c['source_path']}:{c['source_line']}",
                "locator": f"{c['source_path']}:{c['v1_line']}" + (f"-{c['v1_end_line']}" if res_to else ""),
                "resolved_id": res["id"], "resolved_anchor": res["anchor"], "resolved_tag": res["tag"],
                "resolved_clause": res["clause"], "resolved_to_id": res_to["id"] if res_to else "",
                "source_branch": c["source_branch"], "source_commit": c["source_commit"],
                "source_path": c["source_path"], "source_side": c["side"], "source_line": str(c["source_line"]),
                "source_start_line": str(c.get("start_line") or ""), "v1_line": str(c["v1_line"]),
            })

    ids = [r["id"] for r in accepted]
    if len(ids) != len(set(ids)):
        die("internal: register id collision", 2)
    accepted.sort(key=lambda r: r["id"])
    rejects.sort(key=lambda r: (r["channel"], r["source"]))
    out.mkdir(parents=True, exist_ok=True)
    dump_json(accepted, out / "register.json")
    dump_yaml({"register": accepted}, out / "register.yaml",
              header="# Comment register (projection of register.json). ISO 2012-03 fields first; see RESULT.md N4 mapping.\n")
    dump_csv(accepted, REGISTER_FIELDS, out / "register.csv")
    dump_json(rejects, out / "rejects.json")
    dump_csv([{**r, "reasons": "; ".join(r["reasons"])} for r in rejects],
             ["channel", "source", "source_id", "reasons"], out / "rejects.csv")
    dump_json(structural, out / "structural.json")
    print(f"intake: accepted={len(accepted)} rejected={len(rejects)} structural={len(structural)}")
    for r in rejects:
        print(f"  REJECT {r['source']} [{r['source_id']}]: {'; '.join(r['reasons'])}")
    if structural:
        for s in structural:
            print(f"  STRUCTURAL {s['sheet']}: {s['problems']}")
        return 2
    return 1 if rejects else 0


if __name__ == "__main__":
    sys.exit(main())
