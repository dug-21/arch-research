#!/usr/bin/env python3
"""
Validate the W2 `vnc-045` V5 instance against organizational-data-model-v5.yaml AS PARSED.

wfh-011 RW-2. Same class of checker as `wfh-008-validate.py`; the difference is the READER,
not the rules. `vnc-045-instance.yaml` uses a flat section encoding
(`scopes:` / `goals:` / `actors:` / ...) with model fields and relations as sibling keys on
each object, while `wfh-008-instance.yaml` uses `instances: {Construct: [{fields:, relations:}]}`.

THE INSTANCE FILE IS NOT MODIFIED AND MUST NOT BE RE-SERIALIZED. The three-encoding divergence
across this run's case instances is itself a finding about M01 (M01 `notation` describes the model
document and never describes an instance document), and it has to survive this fix. This checker is
therefore written to the data; every accommodation it makes is printed as an explicit
READER-ACCOMMODATION line so that "the reader was bent" is visible rather than silent.

Deterministic, read-only, no network, no model mutation, zero external cost.

Usage:
  python3 vnc-045-validate.py <model.yaml> <instance.yaml> [<counterfactual.yaml>]

Exit 0 = no ERRORs. WARN/NOTE never fail the run.
"""
import sys, re, hashlib, yaml
from collections import Counter

ERRORS, WARNS, NOTES, ACCOM = [], [], [], []
def err(m):  ERRORS.append(m)
def warn(m): WARNS.append(m)
def note(m): NOTES.append(m)
def accom(m):
    if m not in ACCOM: ACCOM.append(m)

def load(p):
    raw = open(p, 'rb').read()
    return yaml.safe_load(raw.decode()), hashlib.sha256(raw).hexdigest()

model_path, inst_paths = sys.argv[1], sys.argv[2:]

# The note count is invocation-sensitive: the counterfactual file contributes two
# COUNTERFACTUAL-BOUNDARY notes, so the same script over the same instance prints 12 notes
# without it and 14 with it (errors, warnings and object count are identical either way).
# A printed number whose meaning depends on an unrecorded input is a label that has quietly
# stopped naming one thing, so the invocation travels with the counts.
print("INVOCATION")
print(f"        argv     : {' '.join(sys.argv)}")
print(f"        model    : {model_path}")
print(f"        instances: {len(inst_paths)} -> {inst_paths}")
print()

M, MSHA = load(model_path)
PIN = "bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060"
print(f"MODEL   {model_path}")
print(f"        sha256 {MSHA}")
print(f"        pin    {PIN}   MATCH={MSHA == PIN}")
if MSHA != PIN:
    sys.exit("REFUSING TO VALIDATE: model digest does not match the wfh-011 SCOPE pin.")
print(f"        version {M['meta']['version']}  core={len(M['core'])} supporting={len(M['supporting'])} "
      f"registries={len(M['registries'])} catalogs={len(M['catalogs'])} values={len(M['values'])} "
      f"invariants={len(M['invariants'])} event_types={len(M['registries']['event_type']['seeded'])}")

CONSTRUCTS = {}; CONSTRUCTS.update(M['core']); CONSTRUCTS.update(M['supporting'])

# --------------------------------------------------------------- reader: section -> construct
SECTION_MAP = {
    'scopes': 'Scope', 'goals': 'Goal', 'capabilities': 'Capability', 'actors': 'Actor',
    'units': 'Unit', 'events': 'Event', 'records': 'Record',
    'workflows': 'Workflow', 'skills': 'Skill', 'roles': 'Role', 'delegations': 'Delegation',
    'gates': 'Gate', 'effect_boundaries': 'EffectBoundary', 'attempts': 'Attempt',
    'technologies': 'Technology',
}
# Top-level keys that are deliberately NOT construct collections in the W2 encoding.
NON_CONSTRUCT = {
    'meta', 'registry_extensions', 'traversal_checks', 'advisory_reviews',
    'skill_catalog_note', 'delegation_gap_note', 'non_adoption_evidence',
    'attempt_governed_by_rule_note',
}
# Placeholder tokens the W2 encoding uses to record an absence rather than invent a value.
PLACEHOLDER = {'missing-history', 'unestablished', 'UNREPRESENTABLE', 'ABSENT',
               'not-applicable', 'NOT-WRITABLE', 'none'}
def is_placeholder(v):
    return isinstance(v, str) and v.strip() in PLACEHOLDER

# --------------------------------------------------------------- registries / values
def registry_keys(rname, inst):
    keys = set((M['registries'][rname].get('seeded') or {}).keys())
    ext = (inst.get('registry_extensions') or {}).get(rname) or {}
    if isinstance(ext, dict):
        for k, v in ext.items():
            # W2 shape A: {key: {definition:..., status:...}}   (unit_kind, record_category, effect_class)
            if isinstance(v, dict) and k not in ('used_seeds', 'unused_seeds'):
                keys.add(k)
            # W2 shape B: {used_seeds: [...], unused_seeds: {...}}  (scope_type, capability_classification)
            elif k == 'used_seeds' and isinstance(v, list):
                keys |= set(v)
            elif k == 'unused_seeds' and isinstance(v, dict):
                keys |= set(v.keys())
    return keys

def value_members(vname):
    v = M['values'][vname]
    if isinstance(v.get('values'), list): return set(v['values'])
    if isinstance(v.get('values'), dict): return set(v['values'].keys())
    return set()

TYPE_RE_REF  = re.compile(r'^ref<([^>]+)>$')
TYPE_RE_LIST = re.compile(r'^list<ref<([^>]+)>>$')
TYPE_RE_ENUM = re.compile(r'^enum\[(.*)\]$')

def check_ref(ctx, fname, target, val, byid):
    if is_placeholder(val):
        warn(f"RECORDED-ABSENCE {ctx}: `{fname}` = {val!r} (a ref recorded as absent, not invented)")
        return
    if target.startswith('registry.'):
        rname = target.split('.', 1)[1]
        if val not in REG_KEYS[rname]:
            err(f"{ctx}: `{fname}`={val!r} is not a member of registry.{rname}")
        return
    if target.startswith('value.'):
        vname = target.split('.', 1)[1]
        if val not in value_members(vname):
            err(f"{ctx}: `{fname}`={val!r} is not a member of value.{vname}")
        return
    targets = [t.strip() for t in target.split('|')]
    if val not in byid:
        err(f"{ctx}: `{fname}` -> {val!r} does not resolve to any instance id")
        return
    if byid[val][0] not in targets:
        err(f"{ctx}: `{fname}` -> {val!r} is a {byid[val][0]}, expected one of {targets}")

def check_scalar(ctx, fname, ftype, val, byid):
    if val is None:
        warn(f"RECORDED-ABSENCE {ctx}: `{fname}` is explicitly null"); return
    if is_placeholder(val):
        warn(f"RECORDED-ABSENCE {ctx}: `{fname}` = {val!r}"); return
    m = TYPE_RE_LIST.match(ftype)
    if m:
        if not isinstance(val, list):
            err(f"{ctx}: `{fname}` expects list<ref<{m.group(1)}>>, got {type(val).__name__}"); return
        for v in val: check_ref(ctx, fname, m.group(1), v, byid)
        return
    m = TYPE_RE_REF.match(ftype)
    if m: check_ref(ctx, fname, m.group(1), val, byid); return
    m = TYPE_RE_ENUM.match(ftype)
    if m:
        allowed = [x.strip() for x in m.group(1).split(',')]
        if val not in allowed: err(f"{ctx}: `{fname}`={val!r} not in enum{allowed}")
        return
    if ftype == 'timestamp':
        import datetime as _dt
        if isinstance(val, (_dt.datetime, _dt.date)):
            accom("an unquoted ISO-8601 timestamp accepted in PyYAML's implicitly-resolved "
                  "datetime form; the file holds the ISO string and the reader, not the data, "
                  "was adjusted")
            return
        if not (isinstance(val, str) and re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', val)):
            err(f"{ctx}: `{fname}`={val!r} is not an ISO-8601 Z timestamp")
        return
    if ftype == 'digest':
        if not isinstance(val, str): err(f"{ctx}: `{fname}` digest must be text")
        elif not re.match(r'^sha256:[0-9a-f]{64}$', val):
            warn(f"MODEL-FORCED-APPROXIMATION {ctx}: `{fname}` is a required digest recorded as a "
                 f"custody-store locator rather than sha256:<64hex> -> {val!r}")
        return
    if ftype == 'bool':
        if not isinstance(val, bool): err(f"{ctx}: `{fname}` must be bool, got {val!r}")
        return
    if ftype == 'map':
        if not isinstance(val, dict): err(f"{ctx}: `{fname}` must be a map, got {type(val).__name__}")
        return
    if ftype in ('list',) or ftype.startswith('list<text>'):
        if not isinstance(val, list): err(f"{ctx}: `{fname}` must be a list, got {type(val).__name__}")
        return
    if ftype == 'text':
        if not isinstance(val, (str, int, float, bool)): err(f"{ctx}: `{fname}` must be text")
        return
    note(f"{ctx}: `{fname}` has unhandled type `{ftype}` — not checked")


def rel_target(ctx, rname, v, declared_attrs=()):
    """A relation entry is either a bare id or an attributed record. M01 declares `attributes:`
    on has_skill / holds_role / held_by, so an attributed entry is legitimate; M01 does not say
    how one is written in an instance. Read the target out of it and check the declared
    attributes are present."""
    if not isinstance(v, dict):
        return v
    accom("an attributed relation entry accepted as a map; M01 declares `attributes:` on some "
          "relations but never specifies how an attributed entry is written in an instance")
    tid = None
    for k in ('actor', 'target', 'ref', 'id'):
        if k in v: tid = v[k]; break
    if tid is None:
        err(f"{ctx}: relation `{rname}` entry is a map with no target key "
            f"(looked for actor/target/ref/id): keys={sorted(v)}")
        return None
    for a in declared_attrs:
        if a not in v:
            note(f"{ctx}: relation `{rname}` -> {tid}: declared attribute `{a}` not carried")
    return tid

def card_ok(card, n):
    card = str(card)
    return {'1': n == 1, '0..1': n <= 1, '1..*': n >= 1, '0..*': True}.get(card)

# --------------------------------------------------------------- load instances
LOADED = {p: load(p) for p in inst_paths}
REG_KEYS = {}
for rn in M['registries']:
    ks = set()
    for p, (I, _) in LOADED.items(): ks |= registry_keys(rn, I)
    REG_KEYS[rn] = ks

# one shared id space so the counterfactual file may reference historical ids
BYID = {}
for p, (I, _) in LOADED.items():
    for sec, rows in I.items():
        if sec in NON_CONSTRUCT or sec not in SECTION_MAP: continue
        for r in rows or []:
            if isinstance(r, dict) and 'id' in r:
                BYID.setdefault(r['id'], (SECTION_MAP[sec], r, p))

TOTAL_OBJ = 0
for path in inst_paths:
    INST, ISHA = LOADED[path]
    print(f"\nINSTANCE {path}\n         sha256 {ISHA}")
    meta = INST.get('meta') or {}
    is_cf = (meta.get('form') == 'counterfactual') or bool(meta.get('provenance') == 'counterfactual')
    print(f"         form={meta.get('form')}  encodes_observed_history={meta.get('encodes_observed_history')}")
    pin = meta.get('model_digest')
    if pin and pin != MSHA: err(f"{path}: pinned model digest {pin} != parsed model {MSHA}")
    elif pin: print("         model pin MATCHES the parsed model digest")

    if is_cf:
        # The counterfactual file is a candidate register, not a V5 object graph. It is checked
        # for boundary hygiene only; validating it as instances would treat proposals as history.
        cfs = INST.get('counterfactuals') or []
        rej = INST.get('rejected_candidates') or []
        ids = [c.get('id') for c in cfs]
        print(f"         {len(cfs)} counterfactual candidate(s) {ids}, {len(rej)} rejected")
        if meta.get('encodes_observed_history') is not False:
            err(f"{path}: counterfactual file does not declare encodes_observed_history: false")
        hist_ids = {i for i, (c, r, p) in BYID.items() if p != path}
        leaked = [i for i in ids if i in hist_ids]
        if leaked: err(f"{path}: counterfactual id collides with a historical id: {leaked}")
        else: note(f"{path}: COUNTERFACTUAL BOUNDARY — zero id overlap with the historical instance")
        for c in cfs:
            for e in (c.get('cf_entities') or []):
                if e.get('provenance') != 'counterfactual':
                    err(f"{path}:{c['id']}: cf_entity lacks provenance: counterfactual")
                if not e.get('replaces'):
                    note(f"{path}:{c['id']}: cf_entity carries no `replaces` source-link")
        accom("counterfactual file validated as a candidate register (its own declared form), "
              "not as a V5 object graph")
        continue

    # ---- collect objects ----
    objs, seen = [], {}
    for sec, rows in INST.items():
        if sec in NON_CONSTRUCT: continue
        if sec not in SECTION_MAP:
            note(f"{path}: top-level key `{sec}` is neither a construct section nor a declared "
                 f"non-construct key — skipped"); continue
        cname = SECTION_MAP[sec]
        for r in rows or []:
            if not isinstance(r, dict) or 'id' not in r:
                err(f"{path}:{sec}: entry without an `id`"); continue
            if r['id'] in seen:
                err(f"{path}:{r['id']}: duplicate instance id (I1: identity must be unique)")
            seen[r['id']] = cname
            objs.append((cname, r))
    TOTAL_OBJ += len(objs)
    by_c = Counter(c for c, _ in objs)
    print(f"         {len(objs)} instance objects across {len(by_c)} constructs: "
          + ", ".join(f"{k}={v}" for k, v in sorted(by_c.items())))
    accom("section names mapped to constructs (scopes->Scope, ...); the W2 encoding carries no "
          "`construct:` key per object")
    accom("model fields and relations read as SIBLING keys on each object; the W2 encoding has no "
          "`fields:`/`relations:` nesting")

    ann_keys = Counter(); notwritable = []
    for cname, r in objs:
        spec = CONSTRUCTS[cname]
        ctx = f"{r['id']}({cname})"
        declared_f = spec.get('fields') or {}
        declared_r = spec.get('relations') or {}

        if str(r.get('STATUS', '')).strip() == 'NOT-WRITABLE':
            notwritable.append(r['id'])
            note(f"{ctx}: object declares STATUS: NOT-WRITABLE — the encoding records that a "
                 f"conforming object CANNOT be written from the alphabet. Field/relation checks "
                 f"skipped; the declaration is the finding. reason={str(r.get('blocking_reason'))[:90]}...")
            continue

        # ---- fields ----
        for fname, fspec in declared_f.items():
            if not isinstance(fspec, dict): continue
            if fname not in r:
                if fspec.get('required', False):
                    err(f"{ctx}: MISSING required field `{fname}`")
                continue
            check_scalar(ctx, fname, str(fspec.get('type')), r[fname], BYID)

        # ---- relations ----
        for rname, rspec in declared_r.items():
            if not isinstance(rspec, dict): continue
            if rname not in r: continue
            vals = r[rname]
            if is_placeholder(vals):
                warn(f"RECORDED-ABSENCE {ctx}: relation `{rname}` = {vals!r}"); continue
            if vals is None: vals = []
            if not isinstance(vals, list):
                if str(rspec.get('cardinality')) in ('1', '0..1'):
                    accom("a relation of cardinality 1 or 0..1 accepted as a bare scalar; M01 "
                          "`notation` describes the MODEL document and never specifies the shape of "
                          "an instance relation (W4 §9)")
                    vals = [vals]
                else:
                    err(f"{ctx}: relation `{rname}` must be a list (cardinality "
                        f"{rspec.get('cardinality')}), got {type(vals).__name__}")
                    continue
            ok = card_ok(rspec.get('cardinality'), len(vals))
            if ok is False:
                err(f"{ctx}: relation `{rname}` has {len(vals)} target(s); cardinality is "
                    f"{rspec.get('cardinality')}")
            targets = [t.strip() for t in str(rspec.get('target')).split('|')]
            declared_attrs = rspec.get('attributes') or []
            for v in vals:
                v = rel_target(ctx, rname, v, declared_attrs)
                if v is None or is_placeholder(v): continue
                if v not in BYID:
                    err(f"{ctx}: relation `{rname}` -> {v!r} does not resolve to any instance id")
                elif BYID[v][0] not in targets:
                    err(f"{ctx}: relation `{rname}` -> {v!r} is a {BYID[v][0]}, expected {targets}")

        # ---- key census: model key vs annotation ----
        for k in r:
            if k == 'id' or k in declared_f or k in declared_r: continue
            ann_keys[k] += 1

        # ---- versioned ----
        if spec.get('versioned') is True and 'version' not in r:
            warn(f"O-W2-1 {ctx}: construct is versioned:true and the object carries no `version`. "
                 f"M01 declares `versioned` on the construct; its `notation` never states that an "
                 f"instance object must carry a version key, so this is an OPERATIONALIZATION and "
                 f"is not counted as a model-discriminated failure.")
        if spec.get('versioned') is False and 'version' in r:
            err(f"{ctx}: construct is versioned:false but the object carries a `version`")

    # ---- declared inverse symmetry (qualified S2 form handled) ----
    inv_checked = inv_broken = 0
    for cname, r in objs:
        if str(r.get('STATUS', '')).strip() == 'NOT-WRITABLE': continue
        for rname, rspec in (CONSTRUCTS[cname].get('relations') or {}).items():
            if not isinstance(rspec, dict) or 'inverse' not in rspec: continue
            inv = str(rspec['inverse']); qual = None
            if '.' in inv:
                qual, inv = inv.split('.', 1)
            vals = r.get(rname)
            if vals is None or is_placeholder(vals): continue
            if not isinstance(vals, list): vals = [vals]
            for v in vals:
                v = rel_target(f"{r['id']}({cname})", rname, v, rspec.get('attributes') or [])
                if v is None or is_placeholder(v) or v not in BYID: continue
                tc, tr, tp = BYID[v]
                if qual and tc != qual: continue
                if str(tr.get('STATUS', '')).strip() == 'NOT-WRITABLE': continue
                back = tr.get(inv)
                if back is None: back = []
                if is_placeholder(back): back = []
                if not isinstance(back, list): back = [back]
                back = [rel_target('', inv, b) for b in back]
                inv_checked += 1
                if r['id'] not in back:
                    inv_broken += 1
                    err(f"INVERSE {r['id']}({cname}).{rname} -> {v}, but {v}.{inv} does not contain {r['id']}")
    note(f"{path}: declared-inverse edges checked={inv_checked} broken={inv_broken}")
    for cname, spec in CONSTRUCTS.items():
        for rname, rspec in (spec.get('relations') or {}).items():
            if isinstance(rspec, dict) and '.' in str(rspec.get('inverse', '')):
                note(f"S2: {cname}.{rname} declares the QUALIFIED inverse "
                     f"`{rspec['inverse']}`; checked only where the target is a {str(rspec['inverse']).split('.')[0]}")

    # ---- Event extension conformance ----
    ev_types = dict(M['registries']['event_type']['seeded'])
    ext_ev = (INST.get('registry_extensions') or {}).get('event_type') or {}
    for k, v in ext_ev.items():
        if isinstance(v, dict) and k not in ('used_seeds', 'unused_seeds'): ev_types[k] = v
    used = set()
    for cname, r in objs:
        if cname != 'Event': continue
        if str(r.get('STATUS', '')).strip() == 'NOT-WRITABLE': continue
        et = r.get('event_type'); used.add(et)
        spec = ev_types.get(et)
        if not spec:
            err(f"{r['id']}(Event): event_type {et!r} is not a registered type"); continue
        need = set(spec.get('required_extension') or [])
        have = set((r.get('extension') or {}).keys())
        miss = need - have
        if miss:
            err(f"{r['id']}(Event/{et}): extension omits required key(s) {sorted(miss)}")
        for k in sorted(need & have):
            v = (r.get('extension') or {}).get(k)
            if v is None or is_placeholder(v):
                warn(f"RECORDED-ABSENCE {r['id']}(Event/{et}): extension.{k} = {v!r}")
    unused = sorted(set(ev_types) - used)
    if unused: note(f"{path}: event types registered but not exercised: {unused}")

    # ---- gate_outcome vocabulary resolves through the assessment's pinned gate ----
    for cname, r in objs:
        if cname != 'Event' or r.get('event_type') != 'gate_outcome': continue
        if str(r.get('STATUS', '')).strip() == 'NOT-WRITABLE': continue
        ext = r.get('extension') or {}
        aref = ext.get('assessment_ref')
        a = BYID.get(aref)
        if not a:
            err(f"{r['id']}: gate_outcome.assessment_ref {aref!r} does not resolve"); continue
        gref = str((a[1].get('extension') or {}).get('gate_version_ref', ''))
        gid = gref.split('@')[0].strip()
        g = BYID.get(gid)
        if not g:
            warn(f"{r['id']}: the assessment's gate_version_ref {gref!r} does not resolve to a Gate "
                 f"object — the outcome vocabulary cannot be checked against allowed_outcomes")
            continue
        allowed = g[1].get('allowed_outcomes') or []
        outcome = ext.get('outcome')
        if outcome not in allowed:
            warn(f"{r['id']}: gate_outcome.outcome {outcome!r} is not verbatim in "
                 f"{gid}.allowed_outcomes {allowed}")

    # ---- registry extension shape conformance ----
    for rname, ext in (INST.get('registry_extensions') or {}).items():
        if rname not in M['registries']:
            err(f"{path}: registry_extensions.{rname} is not a registry in the model"); continue
        shape_keys = set((M['registries'][rname].get('shape') or {}).keys()) - {'key'}
        for k, e in (ext or {}).items():
            if k in ('used_seeds', 'unused_seeds') or not isinstance(e, dict): continue
            missing = shape_keys - set(e.keys())
            if missing:
                warn(f"{path}: registry {rname} extension `{k}` omits declared shape key(s) "
                     f"{sorted(missing)}")

    # ---- annotation-key census ----
    print(f"         NOT-WRITABLE objects: {len(notwritable)} {notwritable}")
    print(f"         annotation keys (declared neither as a field nor a relation of their "
          f"construct): {len(ann_keys)} distinct, {sum(ann_keys.values())} occurrences")
    accom("keys that are neither a declared field nor a declared relation are counted as "
          "ANNOTATION rather than erroring; the W2 encoding carries provenance/evidence/witness "
          "prose inline, which M01 neither forbids nor describes")

print("\n--- READER ACCOMMODATIONS (the reader was bent to the data; the data was not touched) ---")
for a in ACCOM: print("  * " + a)
print(f"\n--- FINDINGS ---")
for m in ERRORS: print("ERROR " + m)
for m in WARNS:  print("WARN  " + m)
for m in NOTES:  print("NOTE  " + m)
print(f"\nOBJECTS VALIDATED: {TOTAL_OBJ}")
print(f"RESULT: {len(ERRORS)} error(s), {len(WARNS)} warning(s), {len(NOTES)} note(s)")
print(f"        produced by: {' '.join(sys.argv)}")
sys.exit(1 if ERRORS else 0)
