#!/usr/bin/env python3
"""wfh-011 W3 — instance validator + traversal engine for the pinned Organizational Data Model V5.

RESEARCH ARTIFACT, NOT A RUNTIME PRODUCT, NOT EVIDENCE OF ENFORCEMENT ANYWHERE.
The checks below are generated from the pinned V5 file's own typed declarations. A rejection here
means "a checker W3 built from M01 can discriminate this case" — it does NOT mean wfh-008, vnc-045,
Unimatrix, or any workflow refuses anything. Missing enforcement is reported as missing enforcement.

The model is parsed AS-IS: no quoting, no normalization, no in-memory patching, no prose imported
from the review.

DISCLOSED OPERATIONALIZATIONS (choices M01 does not make for us; every check tagged with one is
reported as `operationalizable`, not `determined`):
  O1  Declared field/relation/construct sets are treated as CLOSED. M01 never states closure; it is
      inferred from construct_admission_bar + extend_by_registration + explicit extension points.
  O2  `digest` = "<alg>:<hex>" or 64 hex chars.
  O3  `timestamp` = ISO-8601 date or date-time.
  O4  A registered registry entry must carry exactly its registry's declared shape keys (minus
      `key`). Extra keys are reported separately (the model's own gate_outcome seed carries one).
  O5  Unit.current_state ("Workflow-owned") must be a member of the governing Workflow's
      state_vocabulary.
  O7  Unit.replaces rule ("used when intended outcome changes") = string inequality of
      intended_outcome.
  O8  I16 = two versions of one unit_id may not differ in intended_outcome.
  O9  I17 attenuation on the effect_grants axis = set inclusion in the parent's grants.
  O10 I17 chain = grantor/derived_from chain must reach an Actor named by some Scope.authority_root_ref.
  O12 I14 = one Capability identity may not carry differing observable_behavior.
  O11 I18 "outside the governed activity" = the definition_custodian_ref of a Workflow/Gate/Delegation
      may not appear in Attempt.actors of an Attempt that the construct governs/gates.

ILLUSTRATIVE checks (--illustrative) implement bindings M01 DOES NOT STATE. They exist only to show
what a checker could catch if the model stated the rule. Their firing is never counted as model
discrimination; the corresponding matrix rows are `accepted-defect`.

Usage:
  python3 v5_instance_check.py validate --instance BASELINE.yaml [--illustrative]
  python3 v5_instance_check.py suite --instance BASELINE.yaml --matrix MATRIX.yaml --out RESULTS.csv
  python3 v5_instance_check.py traverse --instance BASELINE.yaml --out TRAVERSALS.csv
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import re
import sys

import yaml

PINNED_SHA256 = "bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060"
DEFAULT_MODEL = (
    "/workspaces/arch-research/product/factory/proposals/organizational-data-model-v5.yaml"
)
CORE = ["Scope", "Goal", "Capability", "Actor", "Unit", "Event", "Record"]
SUPPORTING = ["Workflow", "Skill", "Role", "Delegation", "Gate",
              "EffectBoundary", "Attempt", "Technology"]

TS = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})?)?$")
DIGEST = re.compile(r"^([a-z0-9]+:)?[0-9a-f]{40,128}$")
ENUM = re.compile(r"^enum\[(.*)\]$")
REF = re.compile(r"^ref<(.+)>$")
LREF = re.compile(r"^list<ref<(.+)>>$")


class Model:
    def __init__(self, path):
        raw = open(path, "rb").read()
        self.digest = hashlib.sha256(raw).hexdigest()
        if self.digest != PINNED_SHA256:
            sys.exit(f"ABORT: model digest {self.digest} != pinned {PINNED_SHA256}")
        self.m = yaml.safe_load(raw)
        self.C = {n: self.m["core"][n] for n in CORE}
        self.C.update({n: self.m["supporting"][n] for n in SUPPORTING})
        self.registries = self.m["registries"]
        self.values = self.m["values"]

    def value_members(self, vname):
        v = self.values[vname]
        vals = v.get("values")
        if isinstance(vals, dict):
            return set(vals.keys())
        return set(vals or [])

    def inverse_pairs(self):
        """[(A, rel, B, invrel, qualified_to)] for every declared inverse."""
        out = []
        for a, c in self.C.items():
            for r, spec in (c.get("relations") or {}).items():
                if not isinstance(spec, dict):
                    continue
                inv = spec.get("inverse")
                if not inv:
                    continue
                tgts = [t.strip() for t in str(spec["target"]).split("|")]
                if "." in str(inv):
                    qt, qr = str(inv).split(".", 1)
                    out.append((a, r, qt, qr, qt))
                else:
                    for t in tgts:
                        if (self.C.get(t, {}).get("relations") or {}).get(inv):
                            out.append((a, r, t, inv, None))
        return out


def parse_card(c):
    c = str(c)
    if c == "1":
        return 1, 1
    if c == "0..1":
        return 0, 1
    if c == "1..*":
        return 1, None
    if c == "0..*":
        return 0, None
    return 0, None


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def ref_of(x):
    return x["ref"] if isinstance(x, dict) and "ref" in x else x


class Instance:
    def __init__(self, doc):
        self.doc = doc
        self.registered = doc.get("registered") or {}
        self.inst = doc.get("instances") or {}

    def all(self):
        for cname, rows in self.inst.items():
            for row in rows:
                yield cname, row

    def by_id(self):
        idx = {}
        for cname, row in self.all():
            idx.setdefault(row["id"], []).append((cname, row))
        return idx

    def get(self, cname, iid):
        for row in self.inst.get(cname, []):
            if row["id"] == iid:
                return row
        return None


class Validator:
    def __init__(self, model: Model, illustrative=False):
        self.M = model
        self.illustrative = illustrative

    # ---------- helpers -------------------------------------------------
    def registry_keys(self, inst: Instance, rname):
        seeded = set((self.M.registries[rname].get("seeded") or {}).keys())
        return seeded | set((inst.registered.get(rname) or {}).keys())

    def registry_entry(self, inst: Instance, rname, key):
        return ((self.M.registries[rname].get("seeded") or {}).get(key)
                or (inst.registered.get(rname) or {}).get(key))

    def resolve(self, inst: Instance, iid, allowed):
        """allowed: list of construct names. Returns error string or None."""
        idx = inst.by_id()
        if iid not in idx:
            return f"unresolvable reference {iid!r}"
        kinds = {c for c, _ in idx[iid]}
        if not (kinds & set(allowed)):
            return f"reference {iid!r} is {sorted(kinds)}, not {allowed}"
        return None

    def check_type(self, inst: Instance, where, fname, t, val):
        """Yield (check_id, message) for a field value against its declared M01 type."""
        loc = f"{where}.{fname}"
        m = ENUM.match(t)
        if m:
            members = [x.strip() for x in m.group(1).split(",")]
            if val not in members:
                yield ("CK-ENUM", f"{loc}: {val!r} not in enum{members}")
            return
        m = LREF.match(t)
        if m:
            if not isinstance(val, list):
                yield ("CK-TYPE", f"{loc}: expected list<ref<...>>, got {type(val).__name__}")
                return
            for v in val:
                yield from self.check_ref(inst, loc, m.group(1), ref_of(v))
            return
        m = REF.match(t)
        if m:
            yield from self.check_ref(inst, loc, m.group(1), ref_of(val))
            return
        if t == "text":
            if not isinstance(val, str):
                yield ("CK-TYPE", f"{loc}: expected text, got {type(val).__name__}")
        elif t == "timestamp":
            if not (isinstance(val, str) and TS.match(val)):
                yield ("CK-TYPE", f"{loc}: {val!r} is not a timestamp (O3)")
        elif t == "digest":
            if not (isinstance(val, str) and DIGEST.match(val)):
                yield ("CK-TYPE", f"{loc}: {val!r} is not a digest (O2)")
        elif t == "bool":
            if not isinstance(val, bool):
                yield ("CK-TYPE", f"{loc}: expected bool, got {type(val).__name__}")
        elif t == "map":
            if not isinstance(val, dict):
                yield ("CK-TYPE", f"{loc}: expected map, got {type(val).__name__}")
        elif t == "list":
            if not isinstance(val, list):
                yield ("CK-TYPE", f"{loc}: expected list, got {type(val).__name__}")
        elif t == "list<text>":
            if not isinstance(val, list) or any(not isinstance(x, str) for x in val):
                yield ("CK-TYPE", f"{loc}: expected list<text>")
        else:
            yield ("CK-TYPE-UNKNOWN", f"{loc}: unhandled declared type {t!r}")

    def check_ref(self, inst: Instance, loc, inner, val):
        alts = [x.strip() for x in inner.split("|")]
        errs = []
        for alt in alts:
            if alt.startswith("registry."):
                r = alt.split(".", 1)[1]
                if val in self.registry_keys(inst, r):
                    return
                errs.append(f"{val!r} not a registered {r} key "
                            f"(seeded+registered: {sorted(self.registry_keys(inst, r))})")
            elif alt.startswith("value."):
                v = alt.split(".", 1)[1]
                if val in self.M.value_members(v):
                    return
                errs.append(f"{val!r} not in value.{v} "
                            f"{sorted(self.M.value_members(v))}")
            else:
                if self.resolve(inst, val, [alt]) is None:
                    return
                errs.append(f"{val!r} is not an instance of {alt}")
        cid = ("CK-REGISTRY-REF" if any(a.startswith("registry.") for a in alts)
               else "CK-VALUE-REF" if any(a.startswith("value.") for a in alts)
               else "CK-REF-TARGET")
        yield (cid, f"{loc}: " + " | ".join(errs))

    # ---------- checks --------------------------------------------------
    def validate(self, inst: Instance):
        E = []  # (check_id, message)
        M, C = self.M, self.M.C
        idx = inst.by_id()

        # CK-CONSTRUCT-KNOWN (O1)
        for cname in inst.inst:
            if cname not in C:
                E.append(("CK-CONSTRUCT-KNOWN", f"undeclared construct {cname!r} (O1 closure)"))

        # CK-REGISTRY-SHAPE (O4)
        for rname, entries in inst.registered.items():
            if rname not in M.registries:
                E.append(("CK-REGISTRY-KNOWN", f"undeclared registry {rname!r}"))
                continue
            shape = set((M.registries[rname].get("shape") or {}).keys()) - {"key"}
            for k, v in (entries or {}).items():
                if not isinstance(v, dict):
                    E.append(("CK-REGISTRY-SHAPE", f"{rname}.{k}: entry is not a map"))
                    continue
                miss = shape - set(v.keys())
                if miss:
                    E.append(("CK-REGISTRY-SHAPE",
                              f"{rname}.{k}: missing shape keys {sorted(miss)}"))
                extra = set(v.keys()) - shape
                if extra:
                    E.append(("CK-REGISTRY-SHAPE-EXTRA",
                              f"{rname}.{k}: keys beyond declared shape {sorted(extra)}"))
                if "workflow_ref" in v and v["workflow_ref"]:
                    err = self.resolve(inst, v["workflow_ref"], ["Workflow"])
                    if err:
                        E.append(("CK-REGISTRY-SHAPE", f"{rname}.{k}.workflow_ref: {err}"))

        for cname, row in inst.all():
            if cname not in C:
                continue
            spec = C[cname]
            fields = spec.get("fields") or {}
            rels = spec.get("relations") or {}
            fvals = row.get("fields") or {}
            rvals = row.get("relations") or {}
            where = f"{cname}/{row['id']}"

            # CK-FIELD-UNKNOWN / CK-REL-UNKNOWN (O1)
            for k in fvals:
                if k not in fields:
                    E.append(("CK-FIELD-UNKNOWN", f"{where}: undeclared field {k!r} (O1)"))
            for k in rvals:
                if k not in rels:
                    E.append(("CK-REL-UNKNOWN", f"{where}: undeclared relation {k!r} (O1)"))

            # CK-FIELD-REQUIRED
            for fname, fs in fields.items():
                if not isinstance(fs, dict):
                    continue
                if fs.get("required") and fname not in fvals:
                    E.append(("CK-FIELD-REQUIRED", f"{where}: missing required field {fname!r}"))

            # CK-TYPE / CK-ENUM / CK-VALUE-REF / CK-REGISTRY-REF / CK-REF-TARGET
            for fname, val in fvals.items():
                fs = fields.get(fname)
                if not isinstance(fs, dict):
                    continue
                t = str(fs.get("type", "text"))
                for err in self.check_type(inst, where, fname, t, val):
                    E.append(err)

            # CK-CARD / CK-REF-TARGET on relations
            for rname, rs in rels.items():
                if not isinstance(rs, dict):
                    continue
                lo, hi = parse_card(rs.get("cardinality", "0..*"))
                vals = as_list(rvals.get(rname))
                if len(vals) < lo:
                    E.append(("CK-CARD",
                              f"{where}.{rname}: {len(vals)} target(s), cardinality "
                              f"{rs.get('cardinality')} requires >= {lo}"))
                if hi is not None and len(vals) > hi:
                    E.append(("CK-CARD",
                              f"{where}.{rname}: {len(vals)} target(s), cardinality "
                              f"{rs.get('cardinality')} allows <= {hi}"))
                allowed = [x.strip() for x in str(rs["target"]).split("|")]
                for v in vals:
                    err = self.resolve(inst, ref_of(v), allowed)
                    if err:
                        E.append(("CK-REF-TARGET", f"{where}.{rname}: {err}"))

        # CK-INVERSE (incl. S2 qualified form)
        for a, r, b, ir, qual in M.inverse_pairs():
            fwd = set()
            for row in inst.inst.get(a, []):
                for v in as_list((row.get("relations") or {}).get(r)):
                    tid = ref_of(v)
                    kinds = {c for c, _ in idx.get(tid, [])}
                    if b in kinds:
                        fwd.add((row["id"], tid))
            back = set()
            for row in inst.inst.get(b, []):
                for v in as_list((row.get("relations") or {}).get(ir)):
                    sid = ref_of(v)
                    kinds = {c for c, _ in idx.get(sid, [])}
                    if a in kinds:
                        back.add((sid, row["id"]))
            for e in fwd - back:
                E.append(("CK-INVERSE",
                          f"{a}.{r} {e[0]}->{e[1]} has no inverse edge "
                          f"{b}.{ir}{' (qualified)' if qual else ''}"))
            for e in back - fwd:
                E.append(("CK-INVERSE",
                          f"{b}.{ir} {e[1]}->{e[0]} has no forward edge {a}.{r}"))

        # CK-ACYCLIC (rules that name acyclicity explicitly)
        for cname, rel in (("Scope", "parent"), ("Capability", "composed_of"),
                           ("Unit", "depends_on")):
            edges = {}
            for row in inst.inst.get(cname, []):
                edges[row["id"]] = [ref_of(v) for v in
                                    as_list((row.get("relations") or {}).get(rel))]
            for cyc in find_cycles(edges):
                E.append(("CK-ACYCLIC", f"{cname}.{rel}: cycle {' -> '.join(cyc)}"))

        # CK-EVENT-EXT — registered event_type required_extension keys present
        for row in inst.inst.get("Event", []):
            et = (row.get("fields") or {}).get("event_type")
            entry = self.registry_entry(inst, "event_type", et) if et else None
            if not entry:
                continue
            ext = (row.get("fields") or {}).get("extension") or {}
            for k in entry.get("required_extension") or []:
                if k not in ext:
                    E.append(("CK-EVENT-EXT",
                              f"Event/{row['id']} ({et}): extension missing required key {k!r}"))

        # CK-GATE-OUTCOME-VOCAB — the gate_outcome seed's own stated resolution rule
        for row in inst.inst.get("Event", []):
            f = row.get("fields") or {}
            if f.get("event_type") != "gate_outcome":
                continue
            ext = f.get("extension") or {}
            aid = ext.get("assessment_ref")
            arow = inst.get("Event", aid) if aid else None
            if not arow:
                E.append(("CK-GATE-OUTCOME-VOCAB",
                          f"Event/{row['id']}: assessment_ref {aid!r} does not resolve to an Event"))
                continue
            gvr = ((arow.get("fields") or {}).get("extension") or {}).get("gate_version_ref")
            grow = None
            for g in inst.inst.get("Gate", []):
                if g["id"] == gvr or str(gvr).startswith(g["id"]):
                    grow = g
            if not grow:
                E.append(("CK-GATE-OUTCOME-VOCAB",
                          f"Event/{row['id']}: gate_version_ref {gvr!r} does not resolve to a Gate"))
                continue
            allowed = (grow.get("fields") or {}).get("allowed_outcomes") or []
            if ext.get("outcome") not in allowed:
                E.append(("CK-GATE-OUTCOME-VOCAB",
                          f"Event/{row['id']}: outcome {ext.get('outcome')!r} not in "
                          f"{grow['id']}.allowed_outcomes {allowed}"))

        # CK-UNIT-STATE (O5)
        for row in inst.inst.get("Unit", []):
            wf = [ref_of(v) for v in as_list((row.get("relations") or {}).get("follows"))]
            for w in wf:
                wrow = inst.get("Workflow", w)
                if not wrow:
                    continue
                vocab = (wrow.get("fields") or {}).get("state_vocabulary") or []
                st = (row.get("fields") or {}).get("current_state")
                if st is not None and st not in vocab:
                    E.append(("CK-UNIT-STATE",
                              f"Unit/{row['id']}: current_state {st!r} not in "
                              f"{w}.state_vocabulary {vocab} (O5)"))

        # CK-REPLACES-OUTCOME (O7) and CK-I16-VERSION (O8)
        for row in inst.inst.get("Unit", []):
            for v in as_list((row.get("relations") or {}).get("replaces")):
                other = inst.get("Unit", ref_of(v))
                if other and ((row.get("fields") or {}).get("intended_outcome")
                              == (other.get("fields") or {}).get("intended_outcome")):
                    E.append(("CK-REPLACES-OUTCOME",
                              f"Unit/{row['id']} replaces {other['id']} with an identical "
                              f"intended_outcome — Unit.replaces rule is 'used when intended "
                              f"outcome changes' (O7)"))
        byid = {}
        for row in inst.inst.get("Unit", []):
            byid.setdefault(row.get("identity", row["id"]), []).append(row)
        for k, rows in byid.items():
            outs = {(r.get("fields") or {}).get("intended_outcome") for r in rows}
            if len(rows) > 1 and len(outs) > 1:
                E.append(("CK-I16-VERSION",
                          f"Unit identity {k}: {len(rows)} versions with differing "
                          f"intended_outcome — I16 requires a new Unit (O8)"))

        # CK-ATTENUATION-GRANTS (O9) + CK-AUTHORITY-CHAIN (O10)
        roots = {(r.get("fields") or {}).get("authority_root_ref")
                 for r in inst.inst.get("Scope", [])}
        for row in inst.inst.get("Delegation", []):
            parents = [ref_of(v) for v in
                       as_list((row.get("relations") or {}).get("derived_from"))]
            mine = set((row.get("fields") or {}).get("effect_grants") or [])
            for p in parents:
                prow = inst.get("Delegation", p)
                if not prow:
                    continue
                theirs = set((prow.get("fields") or {}).get("effect_grants") or [])
                if not mine <= theirs:
                    E.append(("CK-ATTENUATION-GRANTS",
                              f"Delegation/{row['id']}: effect_grants {sorted(mine - theirs)} "
                              f"exceed parent {p} grants {sorted(theirs)} — I17 (O9)"))
            # chain to a Scope authority root
            seen, cur, ok = set(), row, False
            while cur is not None:
                g = [ref_of(v) for v in as_list((cur.get("relations") or {}).get("grantor"))]
                if any(x in roots for x in g):
                    ok = True
                    break
                nxt = [ref_of(v) for v in
                       as_list((cur.get("relations") or {}).get("derived_from"))]
                if not nxt or nxt[0] in seen:
                    break
                seen.add(nxt[0])
                cur = inst.get("Delegation", nxt[0])
            if not ok:
                E.append(("CK-AUTHORITY-CHAIN",
                          f"Delegation/{row['id']}: grantor chain does not reach any "
                          f"Scope.authority_root_ref {sorted(x for x in roots if x)} — I17 (O10)"))

        # CK-CUSTODY-OUTSIDE (O11)
        E += self.custody_check(inst)

        # CK-I1-OPAQUE — I1 clause "identity ... distinct from name" (the "opaque" clause is
        # not decidable from a snapshot and is NOT checked)
        for cname, row in inst.all():
            nm = (row.get("fields") or {}).get("name")
            if nm is not None and nm == row["id"]:
                E.append(("CK-I1-OPAQUE",
                          f"{cname}/{row['id']}: identity equals the name field — I1"))

        # CK-I14-MEANING (O12) — one Capability identity may not carry different
        # observable_behavior at different organizational levels
        bycap = {}
        for row in inst.inst.get("Capability", []):
            bycap.setdefault(row.get("identity", row["id"]), []).append(row)
        for k, rows in bycap.items():
            beh = {(r.get("fields") or {}).get("observable_behavior") for r in rows}
            if len(rows) > 1 and len(beh) > 1:
                E.append(("CK-I14-MEANING",
                          f"Capability identity {k}: {len(rows)} versions with differing "
                          f"observable_behavior — I14 (O12)"))

        # CK-ADMIT-ASSESSMENT — Record.admitted_by rule: "assessment Events only"
        for row in inst.inst.get("Record", []):
            for v in as_list((row.get("relations") or {}).get("admitted_by")):
                ev = inst.get("Event", ref_of(v))
                if ev and (ev.get("fields") or {}).get("event_type") != "assessment":
                    E.append(("CK-ADMIT-ASSESSMENT",
                              f"Record/{row['id']}: admitted_by {ev['id']} is event_type "
                              f"{(ev.get('fields') or {}).get('event_type')!r}; the relation rule "
                              f"is 'assessment Events only'"))

        # CK-EVENT-AUTHORITY — Event.authority_ref definition: "required for decisions and
        # effect requests"
        for row in inst.inst.get("Event", []):
            f = row.get("fields") or {}
            if f.get("event_type") in ("decision", "effect_request") and not f.get("authority_ref"):
                E.append(("CK-EVENT-AUTHORITY",
                          f"Event/{row['id']} ({f.get('event_type')}): authority_ref absent; the "
                          f"field definition requires it for decisions and effect requests"))

        # CK-I13 — every Capability required by >= 1 Goal (also carried by cardinality 1..*)
        for row in inst.inst.get("Capability", []):
            if not as_list((row.get("relations") or {}).get("required_by")):
                E.append(("CK-I13", f"Capability/{row['id']}: no requiring Goal — I13"))

        if self.illustrative:
            E += self.illustrative_checks(inst)
        return E

    def custody_check(self, inst: Instance):
        E = []
        # Units governed by each Workflow, gated by each Gate, and Attempts each Delegation governs
        actors_of_unit = {}
        for at in inst.inst.get("Attempt", []):
            u = [ref_of(v) for v in as_list((at.get("relations") or {}).get("unit"))]
            for uu in u:
                actors_of_unit.setdefault(uu, set()).update(
                    ref_of(v) for v in as_list((at.get("relations") or {}).get("actors")))
        for wf in inst.inst.get("Workflow", []):
            cust = (wf.get("fields") or {}).get("definition_custodian_ref")
            units = [ref_of(v) for v in as_list((wf.get("relations") or {}).get("governs"))]
            for u in units:
                if cust in actors_of_unit.get(u, set()):
                    E.append(("CK-CUSTODY-OUTSIDE",
                              f"Workflow/{wf['id']}: custodian {cust} is an Attempt actor on "
                              f"governed Unit {u} — I18 (O11)"))
        for g in inst.inst.get("Gate", []):
            cust = (g.get("fields") or {}).get("definition_custodian_ref")
            for v in as_list((g.get("relations") or {}).get("evaluates")):
                t = ref_of(v)
                if cust in actors_of_unit.get(t, set()):
                    E.append(("CK-CUSTODY-OUTSIDE",
                              f"Gate/{g['id']}: custodian {cust} is an Attempt actor on gated "
                              f"Unit {t} — I18 (O11)"))
        for d in inst.inst.get("Delegation", []):
            cust = (d.get("fields") or {}).get("definition_custodian_ref")
            for v in as_list((d.get("relations") or {}).get("governs")):
                at = inst.get("Attempt", ref_of(v))
                if not at:
                    continue
                acts = {ref_of(x) for x in as_list((at.get("relations") or {}).get("actors"))}
                if cust in acts:
                    E.append(("CK-CUSTODY-OUTSIDE",
                              f"Delegation/{d['id']}: custodian {cust} is an actor on governed "
                              f"Attempt {at['id']} — I18 (O11)"))
        return E

    def illustrative_checks(self, inst: Instance):
        """Bindings M01 DOES NOT STATE. Firing here is never model discrimination."""
        E = []
        for ev in inst.inst.get("Event", []):
            f = ev.get("fields") or {}
            ext = f.get("extension") or {}
            if f.get("event_type") == "effect_request":
                d = inst.get("Delegation", ext.get("delegation_ref"))
                if d:
                    grants = set((d.get("fields") or {}).get("effect_grants") or [])
                    if ext.get("requested_effect") not in grants:
                        E.append(("XX-REQUEST-WITHIN-GRANT",
                                  f"Event/{ev['id']}: requested_effect "
                                  f"{ext.get('requested_effect')!r} not in delegation "
                                  f"{d['id']} effect_grants {sorted(grants)} — UNSTATED IN M01"))
                b = inst.get("EffectBoundary", ext.get("target_boundary_ref"))
                if b:
                    classes = set((b.get("fields") or {}).get("effect_classes") or [])
                    if ext.get("requested_effect") not in classes:
                        E.append(("XX-BOUNDARY-CLASS",
                                  f"Event/{ev['id']}: boundary {b['id']} does not carry effect "
                                  f"class {ext.get('requested_effect')!r} — UNSTATED IN M01"))
        for c in list(inst.inst.get("Capability", [])) + list(inst.inst.get("Technology", [])):
            f = c.get("fields") or {}
            if f.get("grade") == "proven" and not (f.get("evidence_record_refs") or []):
                E.append(("XX-PROVEN-NEEDS-EVIDENCE",
                          f"{c['id']}: grade=proven with empty evidence_record_refs — "
                          f"I9/evidence_grade.rule state the bar; UNSTATED AS A TYPED RULE"))
        return E


def find_cycles(edges):
    out, seen = [], set()

    def dfs(n, stack):
        if n in stack:
            out.append(stack[stack.index(n):] + [n])
            return
        if n in seen:
            return
        seen.add(n)
        for m in edges.get(n, []):
            dfs(m, stack + [n])

    for n in edges:
        dfs(n, [])
    return out


# ---------------- patching ------------------------------------------------
def apply_patch(doc, ops):
    d = copy.deepcopy(doc)
    for op in ops:
        kind = op["op"]
        if kind == "add_instance":
            d.setdefault("instances", {}).setdefault(op["construct"], []).append(op["value"])
            continue
        if kind == "register":
            d.setdefault("registered", {}).setdefault(op["registry"], {})[op["key"]] = op["value"]
            continue
        path = op["path"].split("/")
        if path[0] == "registered":
            node = d["registered"]
            for p in path[1:-1]:
                node = node[p]
        else:
            cname, iid = path[0], path[1]
            row = None
            for r in d["instances"][cname]:
                if r["id"] == iid:
                    row = r
            if row is None:
                raise KeyError(f"no instance {cname}/{iid}")
            node = row
            for p in path[2:-1]:
                node = node.setdefault(p, {})
        last = path[-1]
        if kind == "set":
            node[last] = op["value"]
        elif kind == "delete":
            node.pop(last, None)
        elif kind == "append":
            node.setdefault(last, []).append(op["value"])
        else:
            raise ValueError(kind)
    return d


# ---------------- traversals ---------------------------------------------
def traverse(model: Model, inst: Instance):
    """Every required traversal, using ONLY relations declared in M01. No new relation is added."""
    rows = []
    idx = inst.by_id()

    def add(tid, question, method, declared_path, result, status, note, cost):
        rows.append(dict(traversal_id=tid, question=question, method=method,
                         declared_path=declared_path, result=result, status=status,
                         note=note, cost=cost))

    n_wf = len(inst.inst.get("Workflow", []))
    n_at = len(inst.inst.get("Attempt", []))

    # ---- T-01 / T-02 : Goal -> applicable Workflows -----------------------
    for g in inst.inst.get("Goal", []):
        gid = g["id"]
        # index (full scan over the Workflow extent)
        via_index = sorted(w["id"] for w in inst.inst.get("Workflow", [])
                           if gid in [ref_of(v) for v in
                                      as_list((w.get("relations") or {}).get("applies_to"))])
        add("T-01", f"Goal {gid} -> applicable Workflows",
            "implementation index over Workflow.applies_to (built by full scan)",
            "Workflow.applies_to (one-way; A3 withdrawn in M02 s7)",
            ",".join(via_index) or "(none)",
            "demonstrated-by-index",
            "M01 declares no index, no query layer and no Scope bound on the scan; the index is "
            "an implementation artifact outside the model",
            f"O(|Workflow|)={n_wf} full scan")
        # declared-relation path only
        units = [ref_of(v) for v in as_list((g.get("relations") or {}).get("directs"))]
        via_units = sorted({ref_of(v) for u in units
                            for v in as_list(((inst.get("Unit", u) or {}).get("relations")
                                              or {}).get("follows"))})
        missing = sorted(set(via_index) - set(via_units))
        extra = sorted(set(via_units) - set(via_index))
        add("T-02", f"Goal {gid} -> applicable Workflows",
            "declared relations only",
            "Goal.directs -> Unit.follows -> Workflow",
            ",".join(via_units) or "(none)",
            "partial-proxy",
            f"incomplete: misses applicable Workflows with no Unit yet {missing or '[]'}; "
            f"unsound: returns governing Workflows never declared applies_to {extra or '[]'}. "
            f"M01 states no rule linking Unit.follows to Workflow.applies_to.",
            f"O(|directs|+|units|) bounded by the Goal")

    # ---- T-03 / T-04 / T-05 : Actor -> participated Attempts --------------
    for a in inst.inst.get("Actor", []):
        aid = a["id"]
        via_index = sorted(at["id"] for at in inst.inst.get("Attempt", [])
                           if aid in [ref_of(v) for v in
                                      as_list((at.get("relations") or {}).get("actors"))])
        add("T-03", f"Actor {aid} -> participated Attempts",
            "implementation index over Attempt.actors (built by full scan)",
            "Attempt.actors (one-way; A3 withdrawn in M02 s7)",
            ",".join(via_index) or "(none)",
            "demonstrated-by-index",
            "M01 declares no index and no Scope bound; Actor carries no scope_ref, so the scan "
            "cannot even be narrowed by Scope",
            f"O(|Attempt|)={n_at} full scan")
        # dynamic delegations: Actor.receives -> Delegation.governs -> Attempt
        dyn = [ref_of(v) for v in as_list((a.get("relations") or {}).get("receives"))]
        via_dyn = sorted({ref_of(x) for d in dyn
                          for x in as_list(((inst.get("Delegation", d) or {}).get("relations")
                                            or {}).get("governs"))})
        # standing delegations: Actor.holds_role -> Role.receives -> Delegation.governs
        roles = [ref_of(v) for v in as_list((a.get("relations") or {}).get("holds_role"))]
        stand = [ref_of(x) for r in roles
                 for x in as_list(((inst.get("Role", r) or {}).get("relations")
                                   or {}).get("receives"))]
        via_std = sorted({ref_of(x) for d in stand
                          for x in as_list(((inst.get("Delegation", d) or {}).get("relations")
                                            or {}).get("governs"))})
        both = sorted(set(via_dyn) | set(via_std))
        missing = sorted(set(via_index) - set(both))
        extra = sorted(set(both) - set(via_index))
        add("T-04", f"Actor {aid} -> participated Attempts",
            "declared relations only (dynamic grant path)",
            "Actor.receives -> Delegation.governs -> Attempt",
            ",".join(via_dyn) or "(none)", "partial-proxy",
            "reaches only Attempts governed by a Delegation this Actor personally received",
            "O(|receives|)")
        add("T-05", f"Actor {aid} -> participated Attempts",
            "declared relations only (standing grant path)",
            "Actor.holds_role -> Role.receives -> Delegation.governs -> Attempt",
            ",".join(via_std) or "(none)", "partial-proxy",
            "reaches only Attempts governed by the Actor's standing Delegations",
            "O(|roles|x|receives|)")
        add("T-06", f"Actor {aid} -> participated Attempts",
            "declared relations only (union of T-04 and T-05)",
            "Actor.receives U (Actor.holds_role -> Role.receives) -> Delegation.governs",
            ",".join(both) or "(none)",
            "partial-proxy" if (missing or extra) else "equivalent-on-this-instance",
            f"unreachable participation {missing or '[]'} (participants named in Attempt.actors "
            f"who are not the grantee of a governing Delegation — M01 states no invariant tying "
            f"Attempt.actors to governed_by); over-reach {extra or '[]'} (co-governed Attempts "
            f"the Actor did not participate in)",
            "O(|receives|+|roles|)")

    # ---- declared inverses, both directions -------------------------------
    seen = set()
    for a, r, b, ir, qual in model.inverse_pairs():
        key = (a, r, b, ir)
        if key in seen:
            continue
        seen.add(key)
        fwd = [(row["id"], ref_of(v)) for row in inst.inst.get(a, [])
               for v in as_list((row.get("relations") or {}).get(r))
               if b in {c for c, _ in idx.get(ref_of(v), [])}]
        back = [(ref_of(v), row["id"]) for row in inst.inst.get(b, [])
                for v in as_list((row.get("relations") or {}).get(ir))
                if a in {c for c, _ in idx.get(ref_of(v), [])}]
        ok = set(fwd) == set(back) and len(fwd) > 0
        add(f"T-INV-{a}.{r}", f"{a}.{r} <-> {b}.{ir}",
            "declared inverse, traversed both directions",
            f"{a}.{r} -> {b}; {b}.{ir} -> {a}"
            + (" [QUALIFIED inverse name — S2]" if qual else ""),
            f"forward={len(fwd)} backward={len(back)}",
            "demonstrated-both-directions" if ok else
            ("no-witness-in-instance" if not fwd and not back else "asymmetric-in-instance"),
            "qualified dotted inverse name requires a resolver special case (S2)" if qual else "",
            "O(1) per edge")

    # ---- authority chain --------------------------------------------------
    roots = {(s.get("fields") or {}).get("authority_root_ref") for s in inst.inst.get("Scope", [])}
    for d in inst.inst.get("Delegation", []):
        chain, cur, guard = [d["id"]], d, 0
        while cur is not None and guard < 20:
            guard += 1
            nxt = [ref_of(v) for v in as_list((cur.get("relations") or {}).get("derived_from"))]
            if not nxt:
                break
            chain.append(nxt[0])
            cur = inst.get("Delegation", nxt[0])
        top = inst.get("Delegation", chain[-1])
        gr = [ref_of(v) for v in as_list((top.get("relations") or {}).get("grantor"))] if top else []
        add("T-07", f"Delegation {d['id']} -> Scope authority root",
            "declared relations only", "Delegation.derived_from* -> Delegation.grantor",
            " -> ".join(chain) + f" ; grantor={gr}",
            "demonstrated" if any(g in roots for g in gr) else "hole",
            "I17 chain clause is traversable; the attenuation clause is not comparable on "
            "autonomy_tier (M01 declares no order over A0..A5) or resource_ceiling (opaque map)",
            "O(chain depth)")

    # ---- Delegation -> EffectBoundary disposition -------------------------
    for d in inst.inst.get("Delegation", []):
        bs = [ref_of(v) for v in as_list((d.get("relations") or {}).get("enforced_by"))]
        disp = []
        for ev in inst.inst.get("Event", []):
            f = ev.get("fields") or {}
            if f.get("event_type") != "effect_disposition":
                continue
            ext = f.get("extension") or {}
            req = inst.get("Event", ext.get("request_ref"))
            if req and ((req.get("fields") or {}).get("extension")
                        or {}).get("delegation_ref") == d["id"]:
                disp.append(ev["id"])
        add("T-08", f"Delegation {d['id']} -> independent EffectBoundary disposition",
            "declared relation + untyped Event.extension map traversal",
            "Delegation.enforced_by -> EffectBoundary ; effect_disposition.extension"
            ".request_ref -> effect_request.extension.delegation_ref",
            f"boundaries={bs} dispositions={disp}",
            "partial-proxy",
            "the request/disposition/delegation linkage lives inside Event.extension (type: map, "
            "opaque) and Event.subject_refs (type: bare list, untyped). M01 declares NO relation "
            "from Event to Delegation, EffectBoundary, Gate or Unit, so this traversal is by "
            "convention, not by the model.",
            "O(|Event|) full scan")

    # ---- Gate -> assessment -> outcome ------------------------------------
    for g in inst.inst.get("Gate", []):
        asr = [e["id"] for e in inst.inst.get("Event", [])
               if (e.get("fields") or {}).get("event_type") == "assessment"
               and str((((e.get("fields") or {}).get("extension")) or {})
                       .get("gate_version_ref", "")).startswith(g["id"])]
        outs = [e["id"] for e in inst.inst.get("Event", [])
                if (e.get("fields") or {}).get("event_type") == "gate_outcome"
                and (((e.get("fields") or {}).get("extension")) or {}).get("assessment_ref") in asr]
        add("T-09", f"Gate {g['id']} -> assessments -> gate outcomes",
            "untyped Event.extension map traversal",
            "Gate <- assessment.extension.gate_version_ref ; "
            "gate_outcome.extension.assessment_ref",
            f"assessments={asr} outcomes={outs}",
            "partial-proxy",
            "gate_version_ref names a Gate VERSION, but no construct in M01 declares a version "
            "field; the reference has no typed carrier to resolve against",
            "O(|Event|) full scan")
    return rows


# ---------------- CLI ------------------------------------------------------
def load_inst(path):
    return Instance(yaml.safe_load(open(path, "rb").read()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["validate", "suite", "traverse"])
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--instance", required=True)
    ap.add_argument("--matrix")
    ap.add_argument("--out")
    ap.add_argument("--illustrative", action="store_true")
    a = ap.parse_args()

    M = Model(a.model)
    print(f"# model sha256 {M.digest} (pin match: {M.digest == PINNED_SHA256})")

    if a.cmd == "validate":
        inst = load_inst(a.instance)
        errs = Validator(M, a.illustrative).validate(inst)
        print(f"# instance {a.instance}: {len(errs)} finding(s)")
        for cid, msg in errs:
            print(f"  [{cid}] {msg}")
        return 0 if not errs else 1

    if a.cmd == "traverse":
        inst = load_inst(a.instance)
        rows = traverse(M, inst)
        cols = ["traversal_id", "question", "method", "declared_path", "result", "status",
                "note", "cost"]
        with open(a.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"# {len(rows)} traversal rows -> {a.out}")
        for r in rows:
            print(f"  {r['traversal_id']:<28} {r['status']:<28} {r['question']}")
        return 0

    # suite
    base_doc = yaml.safe_load(open(a.instance, "rb").read())
    base = Instance(base_doc)
    V = Validator(M)
    VI = Validator(M, illustrative=True)
    base_errs = V.validate(base)
    print(f"# BASELINE conformance: {len(base_errs)} finding(s)")
    for cid, msg in base_errs:
        print(f"  [{cid}] {msg}")
    if base_errs:
        print("# ABORT: baseline must be conforming before fixtures are meaningful")
        return 2

    matrix = yaml.safe_load(open(a.matrix, "rb").read())
    out_rows = []
    for fx in matrix["fixtures"]:
        fid = fx["fixture_id"]
        if fx.get("kind") == "negative":
            doc = apply_patch(base_doc, fx.get("mutation_ops") or [])
            errs = V.validate(Instance(doc))
            fired = [e for e in errs if e[0] in (fx.get("must_not_fire") or [])]
            observed = "accepted (correct — negative test)" if not errs else \
                       "; ".join(f"[{c}] {m}" for c, m in errs)
            out_rows.append(dict(fx, _observed=observed,
                                 _actual="negative-test-passed" if not fired and not errs
                                 else "negative-test-FAILED"))
            continue
        if not fx.get("mutation_ops"):
            out_rows.append(dict(fx, _observed="no fixture constructible", _actual=None))
            continue
        doc = apply_patch(base_doc, fx["mutation_ops"])
        errs = V.validate(Instance(doc))
        ill = [e for e in VI.validate(Instance(doc)) if e[0].startswith("XX-")]
        new = [e for e in errs if e not in base_errs]
        out_rows.append(dict(fx, _observed="; ".join(f"[{c}] {m}" for c, m in new) or "ACCEPTED",
                             _illustrative="; ".join(f"[{c}] {m}" for c, m in ill),
                             _actual=None, _fired=[c for c, _ in new]))

    cols = ["fixture_id", "x_item", "model_path", "mutation", "violated_rule",
            "expected_rejection_point", "expected_check_kind", "mechanizability",
            "actual_result", "checker_output", "illustrative_output", "operationalization",
            "evidence_path", "note"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in out_rows:
            fired = r.get("_fired") or []
            declared = r.get("expected_rejection_point", "")
            actual = r.get("actual_result")
            if actual is None:
                if r.get("_actual"):
                    actual = r["_actual"]
                elif fired:
                    actual = "rejected-mechanically"
                else:
                    actual = r.get("actual_result_when_accepted", "accepted-defect")
            w.writerow({**r,
                        "actual_result": actual,
                        "checker_output": r.get("_observed", ""),
                        "illustrative_output": r.get("_illustrative", "")})
    print(f"# {len(out_rows)} fixture rows -> {a.out}")
    tally = {}
    for r in out_rows:
        fired = r.get("_fired") or []
        actual = r.get("actual_result") or r.get("_actual") or \
            ("rejected-mechanically" if fired else
             r.get("actual_result_when_accepted", "accepted-defect"))
        tally[actual] = tally.get(actual, 0) + 1
    for k, v in sorted(tally.items()):
        print(f"  {k:<40} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
