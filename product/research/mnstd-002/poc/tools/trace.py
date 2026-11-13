"""C5.3 containment, C5.4 trace table, and the resolved register of record (register + dispositions + trace).

Containment (mechanical, on the v2 SEMANTIC XML): for each accept/modify, the v2 counterpart (via C2.4 mapping)
of the resolved v1 element must contain normalise(expect_in_v2) (accept: == proposed_change; modify: == modified
text — both enforced by dispose.validate). Modes: element | range (union of from..to counterparts) |
insert (exactly one v2 element that is NEW in the C2.4 mapping contains the text).
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

from common import dump_csv, dump_json, dump_yaml, norm, text_of
from dispose import LABEL
from gitx import Git, trailers
from resolver import Doc

TRACE_FIELDS = ["id", "channel", "mb", "type", "locator", "disposition", "commit", "merge_commit",
                "v1_element_id", "v1_anchor", "v1_clause", "v2_element_id", "v2_anchor", "v2_clause",
                "renumbered", "containment"]


def commit_index(g: Git) -> tuple[dict, dict]:
    """comment id -> non-merge commit(s); comment id -> merge commit(s), from git history only."""
    by_id, merges = {}, {}
    for sha in g("rev-list", "--reverse", "v1..v2").split():
        parents = g("rev-list", "--parents", "-n", "1", sha).split()[1:]
        if len(parents) > 1:
            for i in trailers(g, sha, "Resolves"):
                merges.setdefault(i, []).append(sha)
        else:
            for i in trailers(g, sha, "Comment-Id"):
                by_id.setdefault(i, []).append(sha)
    return by_id, merges


def build(register: list[dict], disp: list[dict], mapping: dict, v2: Doc, g: Git, out) -> tuple[list, list, list]:
    dmap = {d["id"]: d for d in disp}
    m1 = {r["v1_id"]: r for r in mapping["elements"]}
    inserted_ids = {x["v2_id"] for x in mapping["inserted"]}
    by_id, merges = commit_index(g)
    trace, contain, resolved = [], [], []
    for r in sorted(register, key=lambda x: x["id"]):
        d = dmap[r["id"]]
        k = d["disposition"]
        row = {"id": r["id"], "channel": r["channel"], "mb": r["mb"], "type": r["type"], "locator": r["locator"],
               "disposition": k, "v1_element_id": r["resolved_id"], "v1_anchor": r["resolved_anchor"] or "(unanchored)",
               "v1_clause": r["resolved_clause"]}
        cres = {"id": r["id"], "disposition": k}
        if k == "reject":
            row.update({"commit": "none (reject: no source change)", "merge_commit": "n/a", "v2_element_id": "",
                        "v2_anchor": "", "v2_clause": "", "renumbered": "", "containment": "n/a"})
            cres.update({"mode": "n/a", "pass": None})
        else:
            commits = by_id.get(r["id"], [])
            row["commit"] = commits[0] if len(commits) == 1 else f"ERROR: {len(commits)} commits"
            ms = merges.get(r["id"], [])
            row["merge_commit"] = ms[0] if ms else "n/a (applied on main)"
            mode = d.get("containment", "element")
            want = norm(d["expect_in_v2"], strip_markup=True)
            v2e = None
            if mode == "insert":
                hits = [e for e in v2.tracked if want in v2.own_text(e) and e.get("id") in inserted_ids]
                hits = [e for e in hits if not any(v2._descends(o, e) and o is not e for o in hits)]
                ok = len(hits) == 1
                v2e = hits[0] if ok else None
                target = v2.own_text(v2e) if v2e is not None else ""
            else:
                ids = [r["resolved_id"]] + ([r["resolved_to_id"]] if mode == "range" and r.get("resolved_to_id") else [])
                v2ids = [m1.get(i, {}).get("v2_id", "") for i in ids]
                if all(v2ids):
                    els = [v2.by_id[i] for i in v2ids]
                    target = " ".join(norm(text_of(e)) for e in els)
                    v2e = els[0]
                    ok = want in target
                else:
                    ok, target = False, ""
            cres.update({"mode": mode, "expect": want, "v2_text": target[:300], "pass": bool(ok)})
            if v2e is not None:
                m = m1.get(r["resolved_id"], {})
                row.update({"v2_element_id": v2e.get("id"), "v2_anchor": v2e.get("anchor") or "(unanchored)",
                            "v2_clause": v2.clause_of(v2e)})
                old, new = r["resolved_clause"], row["v2_clause"]
                row["renumbered"] = "=" if old == new else f"{old}->{new}"
                if mode == "insert":
                    row["renumbered"] = f"new (inserted before v1 {old})"
            else:
                row.update({"v2_element_id": "ERROR", "v2_anchor": "", "v2_clause": "ERROR", "renumbered": "ERROR"})
            row["containment"] = "pass" if ok else "FAIL"
        trace.append(row)
        contain.append(cres)
        rr = dict(r)
        rr["observations"] = f"{LABEL[k]} {d['observation']}"
        rr["disposition"] = k
        rr["modified_text"] = d.get("modified_text", "")
        rr["v2_location"] = "" if k == "reject" else (v2e.get("anchor") if v2e is not None and v2e.get("anchor") else row["v2_element_id"])
        rr["v2_clause"] = "" if k == "reject" else row["v2_clause"]
        rr["commit"] = row["commit"]
        rr["merge_commit"] = row["merge_commit"]
        resolved.append(rr)
    out.mkdir(parents=True, exist_ok=True)
    dump_json(trace, out / "trace.json")
    dump_csv(trace, TRACE_FIELDS, out / "trace.csv")
    dump_yaml({"trace": trace}, out / "trace.yaml")
    dump_json(contain, out / "containment.json")
    dump_json(resolved, out / "register.resolved.json")
    return trace, contain, resolved
