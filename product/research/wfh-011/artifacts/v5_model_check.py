#!/usr/bin/env python3
"""wfh-011 W3 — model-level structural checker for the pinned Organizational Data Model V5.

RESEARCH ARTIFACT, NOT A RUNTIME PRODUCT. Running this demonstrates nothing about enforcement
in wfh-008, vnc-045, or anywhere else. It reads the pinned file as-is: no quoting, no
normalization, no in-memory patching, no import of intended prose from the review.

Deterministic. Stdlib + PyYAML only. Read-only.

Usage:  python3 v5_model_check.py [--model PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys

import yaml

PINNED_SHA256 = "bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060"
DEFAULT_MODEL = (
    "/workspaces/arch-research/product/factory/proposals/organizational-data-model-v5.yaml"
)

CORE = ["Scope", "Goal", "Capability", "Actor", "Unit", "Event", "Record"]
SUPPORTING = [
    "Workflow", "Skill", "Role", "Delegation", "Gate",
    "EffectBoundary", "Attempt", "Technology",
]


def load(path):
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    return yaml.safe_load(raw), digest, raw


def constructs(m):
    out = {}
    for name in CORE:
        out[name] = m["core"][name]
    for name in SUPPORTING:
        out[name] = m["supporting"][name]
    return out


def rel_targets(spec):
    """Split a relation target string into its union alternatives."""
    tgt = spec.get("target")
    if not isinstance(tgt, str):
        return []
    return [t.strip() for t in tgt.split("|")]


def report(section, rows):
    print(f"\n== {section} ==")
    for r in rows:
        print("  " + r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    m, digest, raw = load(args.model)
    print("wfh-011 W3 — V5 model-level structural check")
    print(f"model      : {args.model}")
    print(f"sha256     : {digest}")
    print(f"pin match  : {'YES' if digest == PINNED_SHA256 else 'NO — ABORT'}")
    if digest != PINNED_SHA256:
        sys.exit(2)
    print(f"lines      : {len(raw.splitlines())}")

    C = constructs(m)

    # --- MC1 census (reproduces M02 s9 counts) --------------------------------
    ev = m["registries"]["event_type"]["seeded"]
    rows = [
        f"core={len(m['core'])} supporting={len(m['supporting'])} "
        f"registries={len(m['registries'])} catalogs={len(m['catalogs'])} "
        f"invariants={len(m['invariants'])} event_types={len(ev)} "
        f"values={len(m['values'])} excluded={len(m['excluded'])} open={len(m['open'])}",
    ]
    report("MC1 census", rows)

    # --- MC2 scalar integrity (S1) -------------------------------------------
    # Detect the S1 defect class generically: any scalar value that terminates at a comma
    # while a sibling key looks like a sentence fragment.
    def walk(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                yield from walk(v, f"{path}.{k}" if path else str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from walk(v, f"{path}[{i}]")
        else:
            yield path, node

    frag = []
    for p, v in walk(m):
        key = p.split(".")[-1].split("[")[0]
        # a key that reads as prose (contains a space) is the S1 signature
        if " " in key and key not in ("",):
            frag.append(f"S1-signature key at {p}")
    known_split = {
        "registries.event_type.seeded.effect_disposition.definition",
        "registries.event_type.seeded.adaptation.definition",
        "values.autonomy_tier.values.A0.definition",
        "values.autonomy_tier.values.A3.definition",
        "values.autonomy_tier.values.A5.definition",
        "supporting.Attempt.fields.resume_requirements.definition",
    }
    lens = {}
    for p in known_split:
        cur = m
        for part in p.split("."):
            cur = cur[part]
        lens[p] = cur
    rows = [f"prose-fragment keys found: {len(frag)} (S1 defect class)"]
    for p in sorted(known_split):
        rows.append(f"S1 site OK-len={len(lens[p]):3d} :: {p} = {lens[p]!r}")
    report("MC2 scalar integrity (S1)", rows + frag)

    # --- MC3 invariant binding (R1 / S6) -------------------------------------
    cited = {}
    for name, c in C.items():
        for i in c.get("invariants", []):
            cited.setdefault(i, []).append(name)
    all_inv = list(m["invariants"].keys())
    uncited = [i for i in all_inv if i not in cited]
    nociting = [n for n, c in C.items() if not c.get("invariants")]
    ext_owners = [n for n, c in C.items() if "extension_owner" in c]
    i19_missing = [n for n in ext_owners if "I19" not in C[n].get("invariants", [])]
    report("MC3 invariant binding", [
        f"invariants total={len(all_inv)} cited={len(cited)} uncited={uncited or 'none'}",
        f"constructs citing >=1 invariant: {len(C) - len(nociting)}/{len(C)}; "
        f"non-citing={nociting or 'none'}",
        f"extension_owner present on {len(ext_owners)}: {ext_owners}",
        f"S6 — extension_owner constructs NOT citing I19: {i19_missing}",
    ])

    # --- MC4 relation targets + inverse symmetry (incl. S2 qualified form) ----
    known = set(C) | {"Program", "Collective"}
    dangling, inv_ok, inv_broken, inv_asym, oneway = [], [], [], [], []
    reldecl = {}
    for name, c in C.items():
        for rname, spec in (c.get("relations") or {}).items():
            if not isinstance(spec, dict):
                continue
            reldecl[(name, rname)] = spec
            for t in rel_targets(spec):
                if t not in known:
                    dangling.append(f"{name}.{rname} -> unknown target {t!r}")
    for (name, rname), spec in reldecl.items():
        inv = spec.get("inverse")
        tgts = rel_targets(spec)
        if inv is None:
            # is there a relation on any target pointing back and naming us as its inverse?
            back = [f"{t}.{rn}" for (t, rn), s in reldecl.items()
                    if t in tgts and s.get("inverse") == rname]
            if back:
                inv_asym.append(
                    f"{name}.{rname} declares NO inverse, but {', '.join(back)} "
                    f"declares inverse: {rname}")
            else:
                oneway.append(f"{name}.{rname} -> {spec.get('target')}")
            continue
        if "." in str(inv):  # S2 qualified form
            qt, qr = str(inv).split(".", 1)
            if (qt, qr) in reldecl:
                inv_ok.append(f"{name}.{rname} <-> {inv} (QUALIFIED — S2 form)")
            else:
                inv_broken.append(f"{name}.{rname} -> qualified inverse {inv} unresolvable")
            continue
        hit = [t for t in tgts if (t, inv) in reldecl]
        if hit:
            inv_ok.append(f"{name}.{rname} <-> {hit[0]}.{inv}")
        else:
            inv_broken.append(
                f"{name}.{rname} declares inverse {inv!r} — no such relation on {tgts}")
    report("MC4 relations + inverses", [
        f"relations declared: {len(reldecl)}",
        f"dangling targets: {dangling or 'none'}",
        f"resolvable declared inverses: {len(inv_ok)}",
        f"BROKEN declared inverses: {inv_broken or 'none'}",
        f"ASYMMETRIC inverse declarations ({len(inv_asym)}):",
    ] + ["    " + a for a in inv_asym] + [
        f"one-way relations (legitimate under principles.inverse_relations) "
        f"({len(oneway)}):",
    ] + ["    " + o for o in oneway])

    # --- MC5 ref<> resolution in fields --------------------------------------
    unresolved, untyped_lists, ref_named_text = [], [], []
    reftype = re.compile(r"ref<([^>]+)>")
    for name, c in C.items():
        for fname, spec in (c.get("fields") or {}).items():
            if not isinstance(spec, dict):
                continue
            t = str(spec.get("type", ""))
            for inner in reftype.findall(t):
                for alt in inner.split("|"):
                    alt = alt.strip()
                    if alt.startswith("registry."):
                        if alt.split(".", 1)[1] not in m["registries"]:
                            unresolved.append(f"{name}.{fname} -> {alt}")
                    elif alt.startswith("value."):
                        if alt.split(".", 1)[1] not in m["values"]:
                            unresolved.append(f"{name}.{fname} -> {alt}")
                    elif alt not in known:
                        unresolved.append(f"{name}.{fname} -> {alt}")
            if t == "list" or t == "map" and False:
                untyped_lists.append(f"{name}.{fname}: bare 'list' (no element type)")
            if fname.endswith(("_ref", "_refs")) and "ref<" not in t:
                ref_named_text.append(f"{name}.{fname}: type={t!r}")
    report("MC5 ref resolution / typing", [
        f"unresolved ref<> targets: {unresolved or 'none'}",
        f"bare untyped 'list' fields ({len(untyped_lists)}):",
    ] + ["    " + u for u in untyped_lists] + [
        f"fields named *_ref/_refs that are NOT ref-typed ({len(ref_named_text)}):",
    ] + ["    " + r for r in ref_named_text])

    # --- MC6 registry seed conformance + emptiness ---------------------------
    rows = []
    for rname, r in m["registries"].items():
        shape = set((r.get("shape") or {}).keys()) - {"key"}
        seeded = r.get("seeded") or {}
        rows.append(f"{rname}: shape={sorted(shape)} seeds={len(seeded)}")
        for k, v in seeded.items():
            if not isinstance(v, dict):
                rows.append(f"    SEED NON-MAP {k}")
                continue
            missing = shape - set(v.keys())
            extra = set(v.keys()) - shape
            if missing:
                rows.append(f"    NONCONFORMING seed {k}: missing {sorted(missing)}")
            if extra:
                rows.append(f"    seed {k}: extra keys {sorted(extra)} (beyond declared shape)")
        if not seeded:
            rows.append(f"    EMPTY registry — required refs to it are unsatisfiable "
                        f"until a program registers an entry")
    report("MC6 registries", rows)

    # --- MC7 extension_owner key binding -------------------------------------
    rows = []
    bound = unbound = 0
    for name in ext_owners:
        c = C[name]
        fkeys = set((c.get("fields") or {}).keys()) | set((c.get("relations") or {}).keys())
        for k, owner in c["extension_owner"].items():
            if k in fkeys:
                bound += 1
                rows.append(f"    BOUND   {name}.extension_owner.{k} (owner={owner}) -> field {k}")
            else:
                unbound += 1
                rows.append(f"    UNBOUND {name}.extension_owner.{k} (owner={owner}) "
                            f"-> no field/relation named {k!r}")
    report("MC7 extension_owner binding",
           [f"extension_owner keys: bound-to-same-named-field={bound} unbound={unbound}"] + rows)

    # --- MC8 notation coverage (S3) ------------------------------------------
    used = set()
    for c in C.values():
        used |= set(c.keys())
    documented = set(m["notation"].keys())
    report("MC8 notation coverage (S3)", [
        f"construct keys used: {sorted(used)}",
        f"notation documents : {sorted(documented)}",
        f"UNDOCUMENTED keys  : {sorted(used - documented)}",
        f"Event.identity is a {type(m['core']['Event']['identity']).__name__}, "
        f"while notation.identity describes a scalar 'opaque stable id'",
    ])

    # --- MC9 invariant atomicity heuristic (S4) ------------------------------
    rows = []
    for iid, text in m["invariants"].items():
        clauses = [c.strip() for c in re.split(r";|\band\b(?![^,]*of)", str(text)) if c.strip()]
        if len(clauses) > 1:
            rows.append(f"{iid}: {len(clauses)} independently-failable clause(s) (heuristic) "
                        f":: {text}")
    report("MC9 invariant atomicity (S4, heuristic — judgment)",
           [f"invariants with >1 heuristic clause: {len(rows)}"] + rows)

    # --- MC10 changelog assertions ------------------------------------------
    cl = m["changelog"][0]
    report("MC10 changelog 5.0.0 assertions", [
        f"version={cl['version']} date={cl['date']}",
        f"'bound invariants'          -> uncited={uncited or 'none'}, non-citing={nociting or 'none'}",
        f"'extension ownership bound' -> present on {len(ext_owners)}/15",
        f"'restored form'             -> form present on "
        f"{sum(1 for c in C.values() if 'form' in c)}/15",
        f"'split assessment/gate_outcome' -> "
        f"{'assessment' in ev and 'gate_outcome' in ev}",
        f"'Event authority Scope|Delegation' -> "
        f"{m['core']['Event']['fields']['authority_ref']['type']}",
        f"'Role navigable to standing Delegation' -> "
        f"{'receives' in m['supporting']['Role']['relations']}",
        f"'completed semantic inverses' -> asymmetric declarations remaining: {len(inv_asym)}",
        f"'Scope seeds conform'       -> see MC6",
        f"'invariants atomic'         -> non-atomic remaining (heuristic): {len(rows)}",
        f"'inverse rule in principles'-> "
        f"{'inverse_relations' in m['principles']}",
    ])

    print("\n-- end of model-level check --")


if __name__ == "__main__":
    main()
