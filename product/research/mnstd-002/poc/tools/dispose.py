"""C5.1 disposition-record validator (findings-W2 §2). Exit 0 valid, 1 invalid (every problem listed).
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DISPOSITIONS, dump_json, load_json, norm  # noqa: E402

LABEL = {"accept": "Accepted.", "modify": "Accepted with modifications.", "reject": "Rejected."}


def validate(register: list[dict], disp: list[dict]) -> list[str]:
    errs = []
    reg = {r["id"]: r for r in register}
    counts = Counter(d.get("id") for d in disp)
    for i, n in sorted(counts.items(), key=lambda x: str(x[0])):
        if n > 1:
            errs.append(f"duplicate_disposition: {i} has {n} records")
        if i not in reg:
            errs.append(f"unknown_id: {i} is not in the register")
    for i in sorted(set(reg) - set(counts)):
        errs.append(f"missing_disposition: register comment {i} has no disposition")
    for d in disp:
        i, k = d.get("id"), d.get("disposition")
        if k not in DISPOSITIONS:
            errs.append(f"bad_disposition: {i}: '{k}' not in accept|modify|reject")
            continue
        if not (d.get("observation") or "").strip():
            errs.append(f"missing_observation: {i}")
        edits = d.get("edits") or []
        if k == "reject":
            if edits or d.get("via_branch") or d.get("expect_in_v2"):
                errs.append(f"reject_with_change: {i}: a reject must carry no edits/branch/expectation")
            continue
        if not edits:
            errs.append(f"missing_edits: {i}: {k} requires edits")
        for e in edits:
            if not all(e.get(x) is not None for x in ("file", "find", "replace")) or not e.get("find"):
                errs.append(f"bad_edit: {i}: {e}")
        r = reg.get(i)
        if k == "accept" and r is not None and norm(d.get("expect_in_v2", "")) != norm(r["proposed_change"]):
            errs.append(f"accept_mismatch: {i}: expect_in_v2 != register proposed_change")
        if k == "modify":
            if not (d.get("modified_text") or "").strip():
                errs.append(f"missing_modified_text: {i}")
            elif norm(d.get("expect_in_v2", "")) != norm(d["modified_text"]):
                errs.append(f"modify_mismatch: {i}: expect_in_v2 != modified_text")
        if r is not None and r["channel"] == "pr" and d.get("via_branch") != r["source_branch"]:
            errs.append(f"pr_not_via_branch: {i}: PR comment must be resolved on its branch {r['source_branch']}")
    kinds = Counter(d.get("disposition") for d in disp)
    for k in DISPOSITIONS:
        if kinds.get(k, 0) < 1:
            errs.append(f"fixture_coverage: no '{k}' disposition")
    chans = Counter(reg[d["id"]]["channel"] for d in disp if d.get("id") in reg)
    for c in ("sheet", "pr"):
        if chans.get(c, 0) < 1:
            errs.append(f"fixture_coverage: no disposition for a '{c}' channel comment")
    return errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", required=True)
    ap.add_argument("--dispositions", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    errs = validate(load_json(Path(a.register)), load_json(Path(a.dispositions))["dispositions"])
    dump_json({"valid": not errs, "errors": errs}, Path(a.out))
    for e in errs:
        print("  INVALID", e)
    print(f"dispositions: {'valid' if not errs else f'{len(errs)} problem(s)'}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
