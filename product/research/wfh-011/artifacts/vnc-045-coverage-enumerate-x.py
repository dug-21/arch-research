#!/usr/bin/env python3
"""Deterministically enumerate the wfh-011 X alphabet from the pinned V5 file.
Read-only. Emits one line per X item: <class>\t<model_path>
"""
import sys, hashlib, yaml

PATH = "/workspaces/arch-research/product/factory/proposals/organizational-data-model-v5.yaml"
EXPECT = "bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060"

raw = open(PATH, "rb").read()
dig = hashlib.sha256(raw).hexdigest()
sys.stderr.write(f"sha256={dig} match={dig==EXPECT}\n")
if dig != EXPECT:
    sys.exit("DIGEST MISMATCH — refusing to enumerate")
M = yaml.safe_load(raw)

rows = []
def add(cls, path):
    rows.append((cls, path))

# --- principles / notation ---
for k in M["principles"]:
    add("principle", f"principles.{k}")
for k in M["notation"]:
    add("notation", f"notation.{k}")

# --- core + supporting constructs ---
for section in ("core", "supporting"):
    for cname, c in M[section].items():
        for key in ("status", "form", "identity", "versioned", "definition", "owner"):
            if key in c:
                add(f"{section}-attr", f"{section}.{cname}.{key}")
        for fname, f in (c.get("fields") or {}).items():
            add(f"{section}-field", f"{section}.{cname}.fields.{fname}")
        for rname, r in (c.get("relations") or {}).items():
            add(f"{section}-relation", f"{section}.{cname}.relations.{rname}")
            for sub in ("cardinality", "inverse", "rule", "attributes"):
                if isinstance(r, dict) and sub in r:
                    add(f"{section}-relation-{sub}", f"{section}.{cname}.relations.{rname}.{sub}")
        if "extension_owner" in c:
            for eo in c["extension_owner"]:
                add(f"{section}-extension_owner", f"{section}.{cname}.extension_owner.{eo}")
        if "invariants" in c:
            for iv in c["invariants"]:
                add(f"{section}-invariant-binding", f"{section}.{cname}.invariants.{iv}")
        for i, o in enumerate(c.get("open") or []):
            add(f"{section}-open", f"{section}.{cname}.open[{i}]:{o}")

# --- registries ---
for rname, r in M["registries"].items():
    add("registry", f"registries.{rname}.status")
    add("registry", f"registries.{rname}.shape")
    add("registry", f"registries.{rname}.admission_rule")
    seeded = r.get("seeded") or {}
    if not seeded:
        add("registry-seed-empty", f"registries.{rname}.seeded<EMPTY>")
    for sk, sv in seeded.items():
        add("registry-seed", f"registries.{rname}.seeded.{sk}")
        if isinstance(sv, dict):
            for f in sv:
                add("registry-seed-field", f"registries.{rname}.seeded.{sk}.{f}")

# --- catalogs ---
for cname, c in M["catalogs"].items():
    for k in c:
        add("catalog", f"catalogs.{cname}.{k}")

# --- values ---
for vname, v in M["values"].items():
    if isinstance(v, dict) and "values" in v and isinstance(v["values"], dict):
        add("value-group", f"values.{vname}.status")
        if "definition" in v: add("value-group", f"values.{vname}.definition")
        for mk in v["values"]:
            add("value-member", f"values.{vname}.values.{mk}")
        if "rule" in v: add("value-rule", f"values.{vname}.rule")
    else:
        add("value-group", f"values.{vname}.status")
        for mk in (v.get("values") or []):
            add("value-member", f"values.{vname}.values.{mk}")
        if "rule" in v: add("value-rule", f"values.{vname}.rule")
        if "definition" in v: add("value-group", f"values.{vname}.definition")

# --- invariants ---
for iv in M["invariants"]:
    add("invariant", f"invariants.{iv}")

# --- excluded ---
for i, e in enumerate(M["excluded"]):
    add("excluded", f"excluded[{i}]:{e}")

# --- top-level open ---
for k in M["open"]:
    add("open", f"open.{k}")

# --- changelog ---
for c in M["changelog"]:
    add("changelog", f"changelog.{c['version']}")

# --- review obligations (M02 §9 S1-S8 + traversals) ---
for s in ["S1","S2","S3","S4","S5","S6","S7","S8"]:
    add("review-concern", f"M02.sanity.{s}")
add("traversal", "traversal.Goal->applicable_Workflows")
add("traversal", "traversal.Actor->participated_Attempts")

for cls, p in rows:
    print(f"{cls}\t{p}")
sys.stderr.write(f"TOTAL X ITEMS = {len(rows)}\n")
