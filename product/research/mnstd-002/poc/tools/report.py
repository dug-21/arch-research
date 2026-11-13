"""C7 — disposition report, generated from the resolved register ONLY (no other input, no hand edits).

Formats (Q1 default): report.html + report.yaml + report.csv. Columns: the eight ISO 2012-03 template columns in
template order, then Disposition and v2 location (from the C5.4 trace, carried in the register of record).
Usage: report.py <register.resolved.json> <outdir> <v2-html-relative-href>
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import html
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ISO_COLUMNS, ISO_KEYS, dump_csv, dump_yaml, load_json  # noqa: E402

EXTRA = [("disposition", "Disposition"), ("v2_location", "v2 location")]
COLS = ISO_COLUMNS + EXTRA


def counts(rows):
    return Counter((r["type"], r["disposition"], r["mb"]) for r in rows)


def main(argv):
    src, outdir, v2href = Path(argv[0]), Path(argv[1]), argv[2]
    reg = sorted(load_json(src), key=lambda r: r["id"])
    rows = []
    for r in reg:
        loc = ""
        if r["disposition"] != "reject":
            loc = f"{r['v2_clause']} #{r['v2_location']}"
        rows.append({"id": r["id"], **{k: r[k] for k in ISO_KEYS}, "disposition": r["disposition"], "v2_location": loc,
                     "v2_anchor": r["v2_location"], "channel": r["channel"]})
    outdir.mkdir(parents=True, exist_ok=True)
    fields = ["id"] + [k for k, _ in COLS]
    dump_csv(rows, fields, outdir / "report.csv", headers=["Comment id"] + [h for _, h in COLS])
    c = counts(rows)
    summary = [{"type": t, "disposition": d, "mb": m, "count": n} for (t, d, m), n in sorted(c.items())]
    dump_yaml({"source": src.name, "columns": [h for _, h in COLS],
               "comments": [{k: r[k] for k in fields} for r in rows], "counts_type_disposition_mb": summary,
               "total": len(rows)}, outdir / "report.yaml",
              header="# Disposition report (generated from the resolved register only).\n")
    th = "".join(f"<th>{html.escape(h)}</th>" for h in ["Comment id"] + [h for _, h in COLS])
    body = []
    for r in rows:
        cells = [f'<td class="id">{html.escape(r["id"])}</td>']
        for k, _ in COLS:
            v = html.escape(str(r[k]))
            if k == "v2_location" and r["disposition"] != "reject":
                v = f'<a class="v2loc" data-anchor="{html.escape(r["v2_anchor"])}" href="{html.escape(v2href)}#{html.escape(r["v2_anchor"])}">{v}</a>'
            cells.append(f'<td class="{k}">{v}</td>')
        body.append(f'<tr data-id="{html.escape(r["id"])}" data-type="{r["type"]}" data-disposition="{r["disposition"]}" data-mb="{r["mb"]}">' + "".join(cells) + "</tr>")
    srows = "".join(f'<tr class="count" data-key="{s["type"]}|{s["disposition"]}|{s["mb"]}"><td>{s["type"]}</td><td>{s["disposition"]}</td><td>{s["mb"]}</td><td>{s["count"]}</td></tr>' for s in summary)
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Disposition report - ISO/CD 99999-1 (fictitious)</title>
<style>body{{font-family:sans-serif;margin:1em}}table{{border-collapse:collapse}}td,th{{border:1px solid #999;padding:3px 5px;vertical-align:top;font-size:90%}}th{{background:#eee}}</style></head>
<body><h1>Compilation of comments and secretariat observations</h1>
<p>Document: ISO/CD 99999-1:2026 (fictitious prototype, mnstd-002). Generated from <code>{html.escape(src.name)}</code> only.
Columns 1-8 follow the ISO/IEC/CEN/CENELEC commenting template (version 2012-03); Disposition and v2 location are added.</p>
<table id="comments"><thead><tr>{th}</tr></thead><tbody>
{chr(10).join(body)}
</tbody></table>
<h2>Reconciliation: type x disposition x MB/NC</h2>
<table id="counts"><thead><tr><th>Type</th><th>Disposition</th><th>MB/NC</th><th>Count</th></tr></thead><tbody>{srows}</tbody>
<tfoot><tr><td colspan="3">Total</td><td id="total">{len(rows)}</td></tr></tfoot></table>
</body></html>
"""
    (outdir / "report.html").write_text(doc, encoding="utf-8")
    print(f"report: {len(rows)} comments")


if __name__ == "__main__":
    main(sys.argv[1:])
