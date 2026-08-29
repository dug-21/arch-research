#!/usr/bin/env python3
"""
Validate a V5 instance file against organizational-data-model-v5.yaml AS PARSED.

Deterministic, read-only, no network, no model mutation. The model is parsed with
PyYAML exactly as it sits on disk; nothing is quoted, normalised or patched.

Usage:
  python3 wfh-008-validate.py <model.yaml> <instance.yaml> [<instance2.yaml> ...]

Exit 0 = no ERRORs. WARN/NOTE lines never fail the run; they are the machine-visible
record of model-forced approximations and unenforceable rules.
"""
import sys, re, hashlib, yaml

ERRORS, WARNS, NOTES = [], [], []
def err(m):  ERRORS.append(m)
def warn(m): WARNS.append(m)
def note(m): NOTES.append(m)

def load(p):
    raw = open(p, 'rb').read()
    return yaml.safe_load(raw.decode()), hashlib.sha256(raw).hexdigest()

model_path, inst_paths = sys.argv[1], sys.argv[2:]
M, MSHA = load(model_path)
print(f"MODEL   {model_path}\n        sha256 {MSHA}  version {M['meta']['version']}")

CONSTRUCTS = {}
CONSTRUCTS.update(M['core'])
CONSTRUCTS.update(M['supporting'])
CORE = set(M['core']); SUPP = set(M['supporting'])

# ---- structural self-check of the model, so a model change is visible here ----
print(f"        core={len(M['core'])} supporting={len(M['supporting'])} "
      f"registries={len(M['registries'])} catalogs={len(M['catalogs'])} "
      f"values={len(M['values'])} invariants={len(M['invariants'])} "
      f"event_types={len(M['registries']['event_type']['seeded'])} "
      f"excluded={len(M['excluded'])} open={len(M['open'])}")

ALL_REG_EXT = {}   # populated once every instance file is loaded
def registry_keys(name, inst):
    keys = set((M['registries'][name].get('seeded') or {}).keys())
    ext = ((inst.get('registry_extensions') or {}).get(name) or {}).get('entries') or {}
    keys |= set(ext.keys())
    keys |= set((ALL_REG_EXT.get(name) or {}).keys())
    return keys

def value_members(name):
    v = M['values'][name]
    if 'values' in v and isinstance(v['values'], list):
        return set(v['values'])
    if 'values' in v and isinstance(v['values'], dict):
        return set(v['values'].keys())
    return set()

TYPE_RE_REF   = re.compile(r'^ref<([^>]+)>$')
TYPE_RE_LIST  = re.compile(r'^list<ref<([^>]+)>>$')
TYPE_RE_ENUM  = re.compile(r'^enum\[(.*)\]$')

def check_scalar(ctx, fname, ftype, val, byid, inst):
    if val is None:
        err(f"{ctx}: field `{fname}` is null"); return
    m = TYPE_RE_LIST.match(ftype)
    if m:
        if not isinstance(val, list):
            err(f"{ctx}: field `{fname}` expects list<ref<{m.group(1)}>>, got {type(val).__name__}")
            return
        for v in val: check_ref(ctx, fname, m.group(1), v, byid, inst)
        return
    m = TYPE_RE_REF.match(ftype)
    if m:
        check_ref(ctx, fname, m.group(1), val, byid, inst); return
    m = TYPE_RE_ENUM.match(ftype)
    if m:
        allowed = [x.strip() for x in m.group(1).split(',')]
        if val not in allowed:
            err(f"{ctx}: field `{fname}`={val!r} not in enum{allowed}")
        return
    if ftype == 'timestamp':
        if not (isinstance(val, str) and re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', val)):
            err(f"{ctx}: field `{fname}`={val!r} is not an ISO-8601 Z timestamp")
        return
    if ftype == 'digest':
        if not isinstance(val, str):
            err(f"{ctx}: field `{fname}` digest must be text")
        elif val.startswith('unavailable:') or 'unavailable' in val:
            warn(f"MODEL-FORCED-APPROXIMATION {ctx}: `{fname}` is a required digest the custody store does not expose -> {val!r}")
        elif not re.match(r'^sha256:[0-9a-f]{64}$', val):
            err(f"{ctx}: field `{fname}`={val!r} is not sha256:<64 hex>")
        return
    if ftype == 'bool':
        if not isinstance(val, bool): err(f"{ctx}: field `{fname}` must be bool")
        return
    if ftype == 'map':
        if not isinstance(val, dict): err(f"{ctx}: field `{fname}` must be a map")
        return
    if ftype == 'list':
        if not isinstance(val, list): err(f"{ctx}: field `{fname}` must be a list")
        return
    if ftype == 'text':
        if not isinstance(val, (str, int, float)):
            err(f"{ctx}: field `{fname}` must be text")
        return
    if ftype.startswith('list<text>'):
        if not isinstance(val, list): err(f"{ctx}: field `{fname}` must be list<text>")
        return
    note(f"{ctx}: field `{fname}` has unhandled type `{ftype}` — not checked")

def check_ref(ctx, fname, target, val, byid, inst):
    if target.startswith('registry.'):
        rname = target.split('.', 1)[1]
        if val not in registry_keys(rname, inst):
            err(f"{ctx}: `{fname}`={val!r} not a member of registry.{rname}")
        return
    if target.startswith('value.'):
        vname = target.split('.', 1)[1]
        if val not in value_members(vname):
            err(f"{ctx}: `{fname}`={val!r} not a member of value.{vname}")
        return
    targets = [t.strip() for t in target.split('|')]
    if val not in byid:
        err(f"{ctx}: `{fname}` -> {val!r} does not resolve to any instance id")
        return
    if byid[val]['construct'] not in targets:
        err(f"{ctx}: `{fname}` -> {val!r} is a {byid[val]['construct']}, expected one of {targets}")

def card_ok(card, n):
    card = str(card)
    if card == '1':    return n == 1
    if card == '0..1': return n <= 1
    if card == '1..*': return n >= 1
    if card == '0..*': return True
    return None

# Pre-load every instance file into ONE id space so a counterfactual file may reference
# the historical objects it varies. Each file is still validated separately.
LOADED = {ip: load(ip) for ip in inst_paths}
GLOBAL = {}
for ip, (I, _) in LOADED.items():
    for rn, rx in (I.get('registry_extensions') or {}).items():
        ALL_REG_EXT.setdefault(rn, {}).update(rx.get('entries') or {})
for ip, (I, _) in LOADED.items():
    for cname, rows in (I.get('instances') or {}).items():
        for r in rows or []:
            GLOBAL.setdefault(r['id'], r)

for ip in inst_paths:
    INST, ISHA = LOADED[ip]
    print(f"\nINSTANCE {ip}\n         sha256 {ISHA}")
    is_cf = bool(INST['meta'].get('counterfactual'))
    print(f"         counterfactual={is_cf}  provenance_class={INST['meta'].get('provenance_class')}")
    pin = INST['meta'].get('model_under_test', {}).get('sha256')
    if pin and pin != MSHA:
        err(f"{ip}: pinned model sha256 {pin} != parsed model {MSHA}")
    else:
        print(f"         model pin MATCHES parsed model digest")

    objs, byid = [], dict(GLOBAL)
    for cname, rows in (INST.get('instances') or {}).items():
        if cname not in CONSTRUCTS:
            err(f"{ip}: `{cname}` is not a construct in the model"); continue
        for r in rows or []:
            if r.get('construct') != cname:
                err(f"{ip}:{r.get('id')}: construct key {r.get('construct')!r} != section {cname!r}")
            if byid.get(r['id']) is not r:
                err(f"{ip}:{r['id']}: duplicate instance id (I1: identity must be unique)")
            byid[r['id']] = r; objs.append((cname, r))
    print(f"         {len(objs)} instance objects across "
          f"{len([c for c in (INST.get('instances') or {}) if (INST['instances'][c] or [])])} constructs")

    # counterfactual hygiene
    if is_cf:
        for cname, r in objs:
            if r.get('provenance_class') != 'counterfactual':
                err(f"{ip}:{r['id']}: counterfactual file object lacks provenance_class: counterfactual")
    else:
        for cname, r in objs:
            if r.get('provenance_class') == 'counterfactual':
                err(f"{ip}:{r['id']}: counterfactual object inside the historical instance file")

    # ---- fields ----
    for cname, r in objs:
        spec = CONSTRUCTS[cname]
        ctx = f"{ip}:{r['id']}({cname})"
        fields = r.get('fields') or {}
        declared = spec.get('fields') or {}
        for fname, fspec in declared.items():
            if not isinstance(fspec, dict):
                note(f"{ctx}: field spec for `{fname}` is not a map — skipped"); continue
            req = fspec.get('required', False)
            if fname not in fields:
                if req: err(f"{ctx}: MISSING required field `{fname}`")
                continue
            check_scalar(ctx, fname, str(fspec.get('type')), fields[fname], byid, INST)
        for fname in fields:
            if fname not in declared:
                err(f"{ctx}: undeclared field `{fname}`")
        for fname, pr in (r.get('_approx') or {}).items():
            warn(f"MODEL-FORCED-APPROXIMATION {ctx}: `{fname}` -> pressure {pr}")
        if spec.get('versioned') is True and 'version' not in r:
            err(f"{ctx}: construct is versioned:true but the instance carries no version")
        if spec.get('versioned') is False and 'version' in r:
            err(f"{ctx}: construct is versioned:false but the instance carries a version")

    # ---- relations, cardinality, targets ----
    for cname, r in objs:
        spec = CONSTRUCTS[cname]
        ctx = f"{ip}:{r['id']}({cname})"
        rels = r.get('relations') or {}
        declared = spec.get('relations') or {}
        for rname in rels:
            if rname not in declared:
                err(f"{ctx}: undeclared relation `{rname}`")
        for rname, rspec in declared.items():
            if not isinstance(rspec, dict): continue
            vals = rels.get(rname, [])
            if not isinstance(vals, list):
                err(f"{ctx}: relation `{rname}` must be a list"); continue
            ok = card_ok(rspec.get('cardinality'), len(vals))
            if ok is False:
                err(f"{ctx}: relation `{rname}` has {len(vals)} target(s), cardinality is {rspec.get('cardinality')}")
            targets = [t.strip() for t in str(rspec.get('target')).split('|')]
            for v in vals:
                if v not in byid:
                    err(f"{ctx}: relation `{rname}` -> {v!r} does not resolve")
                elif byid[v]['construct'] not in targets:
                    err(f"{ctx}: relation `{rname}` -> {v!r} is a {byid[v]['construct']}, expected {targets}")

    # ---- declared inverse symmetry (S2 qualified form handled) ----
    for cname, r in objs:
        spec = CONSTRUCTS[cname]
        for rname, rspec in (spec.get('relations') or {}).items():
            if not isinstance(rspec, dict) or 'inverse' not in rspec: continue
            inv = str(rspec['inverse']); qual = None
            if '.' in inv:
                qual, inv = inv.split('.', 1)
                note(f"S2: {cname}.{rname} declares a QUALIFIED inverse `{qual}.{inv}`; "
                     f"checked only for targets of construct {qual}")
            for v in (r.get('relations') or {}).get(rname, []) or []:
                if v not in byid: continue
                tgt = byid[v]
                if qual and tgt['construct'] != qual: continue
                if r.get('provenance_class') != tgt.get('provenance_class'):
                    note(f"COUNTERFACTUAL BOUNDARY: {r['id']}.{rname} -> {v} crosses history/counterfactual; "
                         f"the inverse is deliberately NOT written back into the other provenance class")
                    continue
                back = (tgt.get('relations') or {}).get(inv, []) or []
                if r['id'] not in back:
                    err(f"INVERSE {ip}:{r['id']}({cname}).{rname} -> {v}, but {v}.{inv} does not contain {r['id']}")

    # ---- registry extension conformance to each registry's declared shape ----
    for rname, ext in (INST.get('registry_extensions') or {}).items():
        if rname not in M['registries']:
            err(f"{ip}: registry_extensions.{rname} is not a registry in the model"); continue
        shape = M['registries'][rname].get('shape') or {}
        shape_keys = set(shape.keys()) - {'key'}
        for k, e in (ext.get('entries') or {}).items():
            missing = shape_keys - set(e.keys())
            extra   = set(e.keys()) - shape_keys - {'admission_justification'}
            if missing: err(f"{ip}: registry {rname} seed `{k}` omits shape keys {sorted(missing)}")
            if extra:   note(f"{ip}: registry {rname} seed `{k}` carries extra keys {sorted(extra)}")

    # ---- seeded-registry shape conformance (S1/A5 regression check on the model itself) ----
    for rname, rspec in M['registries'].items():
        shape_keys = set((rspec.get('shape') or {}).keys()) - {'key'}
        for k, e in (rspec.get('seeded') or {}).items():
            if not isinstance(e, dict): continue
            missing = shape_keys - set(e.keys()) - {'rule'}
            if missing: note(f"MODEL: seeded {rname}.{k} omits shape keys {sorted(missing)}")

    # ---- event extension conformance ----
    ev_types = dict(M['registries']['event_type']['seeded'])
    ev_types.update(((INST.get('registry_extensions') or {}).get('event_type') or {}).get('entries') or {})
    for cname, r in objs:
        if cname != 'Event': continue
        et = (r.get('fields') or {}).get('event_type')
        spec = ev_types.get(et)
        if not spec: continue
        need = set(spec.get('required_extension') or [])
        have = set((r['fields'].get('extension') or {}).keys())
        miss = need - have
        if miss:
            err(f"{ip}:{r['id']}(Event/{et}): extension omits required keys {sorted(miss)}")
    used = {(r.get('fields') or {}).get('event_type') for c, r in objs if c == 'Event'}
    unused = sorted(set(ev_types) - used)
    if unused: note(f"{ip}: event types registered but not exercised: {unused}")

    # ---- gate_outcome vocabulary resolves through the assessment's pinned gate ----
    for cname, r in objs:
        if cname != 'Event' or r['fields'].get('event_type') != 'gate_outcome': continue
        ext = r['fields'].get('extension') or {}
        a = byid.get(ext.get('assessment_ref'))
        if not a:
            err(f"{ip}:{r['id']}: gate_outcome.assessment_ref does not resolve"); continue
        gref = (a['fields'].get('extension') or {}).get('gate_version_ref', '')
        gid = gref.split('@')[0].strip()
        g = byid.get(gid)
        if not g:
            warn(f"{ip}:{r['id']}: assessment's gate_version_ref {gref!r} does not resolve to a Gate instance "
                 f"— outcome vocabulary cannot be mechanically resolved"); continue
        allowed = g['fields'].get('allowed_outcomes') or []
        if ext.get('outcome') not in allowed:
            err(f"{ip}:{r['id']}: outcome {ext.get('outcome')!r} not in {gid}.allowed_outcomes {allowed}")

    # ---- selected invariants that ARE mechanically checkable on instance data ----
    print("\n         INVARIANT CHECKS (only those an instance can decide):")
    caps = [r for c, r in objs if c == 'Capability']
    bad13 = [r['id'] for r in caps if not ((r.get('relations') or {}).get('required_by'))]
    print(f"           I13 every Capability required by >=1 Goal ......... "
          f"{'PASS' if not bad13 else 'FAIL ' + str(bad13)}"
          f"{'  (vacuous: 0 Capability instances)' if not caps else ''}")
    if not caps:
        warn(f"{ip}: I13/I14/I9 and Capability's whole field/relation set are VACUOUS — "
             f"the case instantiates zero Capability objects")

    units = [r for c, r in objs if c == 'Unit']
    atts  = [r for c, r in objs if c == 'Attempt']
    multi = [u['id'] for u in units if len((u.get('relations') or {}).get('attempts', [])) > 1]
    print(f"           I15 Unit identity survives rework (multi-Attempt) .. "
          f"{'PASS' if multi else 'NOT WITNESSED'}  witnesses={multi}")
    outs = {}
    for u in units:
        outs.setdefault(u['fields']['intended_outcome'], []).append(u['id'])
    dup = {k: v for k, v in outs.items() if len(v) > 1}
    print(f"           I16 distinct intended_outcome per Unit ............ "
          f"{'PASS' if not dup else 'COLLISION ' + str(list(dup.values()))}")

    TIER = {'A0': 0, 'A1': 1, 'A2': 2, 'A3': 3, 'A4': 4, 'A5': 5}
    dels = [r for c, r in objs if c == 'Delegation']
    i17_fail, i17_undec = [], []
    for d in dels:
        for p in (d.get('relations') or {}).get('derived_from', []) or []:
            par = byid.get(p)
            if not par: continue
            ct, pt = d['fields']['autonomy_tier'], par['fields']['autonomy_tier']
            if TIER[ct] > TIER[pt]:
                i17_fail.append(f"{d['id']}({ct}) > {par['id']}({pt})")
            cg, pg = set(d['fields']['effect_grants']), set(par['fields']['effect_grants'])
            if not cg <= pg:
                i17_fail.append(f"{d['id']} effect_grants {sorted(cg - pg)} not in parent {par['id']}")
            if set(d['fields']['escalation_conditions']) != set(par['fields']['escalation_conditions']):
                i17_undec.append(f"{d['id']} vs {par['id']}: escalation_conditions differ")
    print(f"           I17 derived Delegation does not exceed parent ..... "
          f"{'PASS' if not i17_fail else 'FAIL ' + str(i17_fail)}  (tier + effect_grants only)")
    if i17_undec:
        warn(f"{ip}: I17 UNDECIDABLE on non-numeric axes for {len(i17_undec)} derived Delegations — "
             f"the model supplies no ordering for escalation_conditions or resource_ceiling maps "
             f"(open.delegation_attenuation)")
    roots = [d['id'] for d in dels
             if not ((d.get('relations') or {}).get('derived_from'))
             and (d.get('relations') or {}).get('grantor')
             and byid[d['relations']['grantor'][0]]['construct'] == 'Actor']
    unrooted = []
    for d in dels:
        g = (d.get('relations') or {}).get('grantor', [])
        if not g: continue
        gr = byid.get(g[0])
        chain_ok = bool((d.get('relations') or {}).get('derived_from')) or any(
            gr['id'] == s['fields']['authority_root_ref'] for c, s in objs if c == 'Scope')
        if not chain_ok: unrooted.append(d['id'])
    print(f"           I17 authority chain reaches a Scope root .......... "
          f"{'PASS' if not unrooted else 'FAIL ' + str(unrooted)}")

    boundaries = [r for c, r in objs if c == 'EffectBoundary']
    enforcing = [b['id'] for b in boundaries if (b.get('relations') or {}).get('enforces')]
    print(f"           I12 enforced authority (a boundary enforcing a Delegation) "
          f"{'WITNESSED ' + str(enforcing) if enforcing else 'NOT WITNESSED — zero enforced authority in this case'}")
    if not enforcing:
        warn(f"{ip}: I12 second clause NOT WITNESSED — no EffectBoundary enforces any Delegation; "
             f"every authority in this case is declared only")
    unenforced = [d['id'] for d in dels if not ((d.get('relations') or {}).get('enforced_by'))]
    print(f"           Delegation.enforced_by empty on {len(unenforced)}/{len(dels)} Delegations")

    obs = [r for c, r in objs if c == 'Event' and r['fields']['event_type'] == 'observation']
    mech = [o['id'] for o in obs if o['fields'].get('epistemic_kind') == 'mechanical-observation']
    print(f"           I4  observation Events with mechanical epistemic_kind {mech or 'NONE'} "
          f"({len(obs)} observation Events total)")

    supers = [r['id'] for c, r in objs if c == 'Record' and (r.get('relations') or {}).get('supersedes')]
    print(f"           I1  Record supersession chains present ........... {supers or 'NONE'}")

    # ---- excluded-construct negative test ----
    print("\n         EXCLUDED-CONSTRUCT NEGATIVE TEST:")
    ex_names = ['Feature', 'Qualification', 'Envelope', 'AuthorityBasis', 'EvidenceItem',
                'RecordVersion', 'Signal', 'Decision', 'Transition', 'Assessment', 'Outcome',
                'EffectRequest', 'EffectReceipt']
    present = [n for n in ex_names if n in (INST.get('instances') or {})]
    print(f"           excluded constructs appearing as instance sections: {present or 'NONE — negative test PASSES'}")

    # ---- required one-way traversals (M02 §7) ----
    print("\n         REQUIRED TRAVERSALS (one-way relations, served by index not inverse):")
    goals = [r for c, r in objs if c == 'Goal']
    wfs   = [r for c, r in objs if c == 'Workflow']
    for g in goals:
        hits = [w['id'] for w in wfs if g['id'] in ((w.get('relations') or {}).get('applies_to') or [])]
        print(f"           Goal {g['id']} -> applicable Workflows: {hits or 'NONE'}")
    for a in [r for c, r in objs if c == 'Actor']:
        hits = [t['id'] for t in atts if a['id'] in ((t.get('relations') or {}).get('actors') or [])]
        if hits: print(f"           Actor {a['id']} -> participated Attempts: {hits}")

print("\n" + "=" * 78)
for m in NOTES:  print("NOTE  " + m)
for m in WARNS:  print("WARN  " + m)
for m in ERRORS: print("ERROR " + m)
print("=" * 78)
print(f"RESULT: {len(ERRORS)} error(s), {len(WARNS)} warning(s), {len(NOTES)} note(s)")
sys.exit(1 if ERRORS else 0)
