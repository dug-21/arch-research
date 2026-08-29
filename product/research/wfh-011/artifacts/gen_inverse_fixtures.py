#!/usr/bin/env python3
"""wfh-011 W3 — generate one invalid fixture per DECLARED inverse pair in the pinned V5 model.

Emits YAML fixture rows that were appended once to invalid-instance-matrix.yaml (section B).
Re-running it reproduces that section verbatim. Read-only with respect to the model.

  python3 gen_inverse_fixtures.py            # print the YAML to stdout
"""
import sys

import yaml

sys.path.insert(0, "/workspaces/arch-research/product/research/wfh-011/artifacts")
from v5_instance_check import (  # noqa: E402
    DEFAULT_MODEL, Instance, Model, as_list, parse_card, ref_of,
)

BASELINE = "/workspaces/arch-research/product/research/wfh-011/artifacts/w3-baseline-instance.yaml"


def main():
    M = Model(DEFAULT_MODEL)
    inst = Instance(yaml.safe_load(open(BASELINE, "rb").read()))
    idx = inst.by_id()

    seen, rows = set(), []
    for a, r, b, ir, qual in M.inverse_pairs():
        key = tuple(sorted([(a, r), (b, ir)]))
        if key in seen:
            continue
        seen.add(key)
        edge = None
        for row in inst.inst.get(a, []):
            for v in as_list((row.get("relations") or {}).get(r)):
                t = ref_of(v)
                if b in {c for c, _ in idx.get(t, [])}:
                    edge = (row["id"], t)
                    break
            if edge:
                break
        if not edge:
            rows.append((a, r, b, ir, qual, None, None))
            continue
        src, tgt = edge
        brow = inst.get(b, tgt)
        cur = [ref_of(v) for v in as_list((brow.get("relations") or {}).get(ir))]
        remaining = [x for x in cur if x != src]
        lo, _ = parse_card((M.C[b]["relations"][ir]).get("cardinality", "0..*"))
        op = ({"op": "set", "path": f"{b}/{tgt}/relations/{ir}", "value": remaining}
              if remaining else {"op": "delete", "path": f"{b}/{tgt}/relations/{ir}"})
        rows.append((a, r, b, ir, qual, op, lo))

    out, n = [], 0
    for a, r, b, ir, qual, op, lo in rows:
        n += 1
        fid = f"F-B{n:02d}"
        if op is None:
            out.append({
                "fixture_id": fid, "x_item": f"declared inverse {a}.{r} <-> {b}.{ir}",
                "model_path": f"{a}.relations.{r}.inverse",
                "mutation": "no witness edge in the baseline",
                "violated_rule": "declared inverse symmetry",
                "expected_rejection_point": "CK-INVERSE",
                "expected_check_kind": "mechanical",
                "mechanizability": "determined-by-M01",
                "actual_result": "not-falsifiable-from-alphabet",
                "operationalization": "none",
                "evidence_path": "findings-W3-rejection-suite.md", "mutation_ops": []})
            continue
        note = f"deleting the back-edge on {b}.{ir}"
        if lo and lo > 0:
            note += f"; CK-CARD also fires because {b}.{ir} has minimum cardinality {lo}"
        if qual:
            note += ("; QUALIFIED dotted inverse name (S2) — the resolver needs a special case, "
                     "and a resolver looking up a relation literally named 'Unit.gated_by' "
                     "finds nothing")
        out.append({
            "fixture_id": fid, "x_item": f"declared inverse {a}.{r} <-> {b}.{ir}",
            "model_path": f"{a}.relations.{r}.inverse",
            "mutation": f"break the inverse: remove the back-reference from "
                        f"{b}/{op['path'].split('/')[1]}.{ir}",
            "violated_rule": "declared inverse symmetry (principles.inverse_relations)",
            "expected_rejection_point": "CK-INVERSE",
            "expected_check_kind": "mechanical",
            "mechanizability": "determined-by-M01",
            "operationalization": "none",
            "evidence_path": "artifacts/rejection-results.csv",
            "note": note, "mutation_ops": [op]})

    sys.stdout.write(yaml.safe_dump(out, sort_keys=False, width=95,
                                    default_flow_style=False, allow_unicode=True))


if __name__ == "__main__":
    main()
