#!/usr/bin/env python3
"""wfh-011 W4 / RW-3 — measure, from the two case INSTANCES themselves, whether each
canonical X row has a populated instance witness. Read-only; neither instance is modified."""
import yaml, hashlib, sys
from collections import defaultdict

ROOT="/workspaces/arch-research"
ART=f"{ROOT}/product/research/wfh-011/artifacts"
M01=f"{ROOT}/product/factory/proposals/organizational-data-model-v5.yaml"
PIN="bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060"
if hashlib.sha256(open(M01,'rb').read()).hexdigest()!=PIN: sys.exit("M01 DIGEST MISMATCH")
M=yaml.safe_load(open(M01))

PLACEHOLDER={'missing-history','unestablished','UNREPRESENTABLE','ABSENT','not-applicable',
             'NOT-WRITABLE','none','None','EMPTY','n/a'}
def real(v):
    if v is None: return False
    if isinstance(v,str): return v.strip()!='' and v.strip() not in PLACEHOLDER
    if isinstance(v,(list,tuple)): return any(real(x) for x in v)
    if isinstance(v,dict): return any(real(x) for x in v.values())
    return True

W2SEC={'scopes':'Scope','goals':'Goal','capabilities':'Capability','actors':'Actor','units':'Unit',
       'events':'Event','records':'Record','workflows':'Workflow','skills':'Skill','roles':'Role',
       'delegations':'Delegation','gates':'Gate','effect_boundaries':'EffectBoundary',
       'attempts':'Attempt','technologies':'Technology'}

def load_w1(p):
    """W1 encoding: instances: {Construct: [{id, fields:{}, relations:{}}]}"""
    d=yaml.safe_load(open(p)); out=defaultdict(list)
    for cname,lst in (d.get('instances') or {}).items():
        if not isinstance(lst,list): continue
        for o in lst:
            if isinstance(o,dict):
                out[cname].append({'id':o.get('id'),'f':o.get('fields') or {},'r':o.get('relations') or {}})
    return out

def load_w2(p):
    """W2 encoding: top-level section lists; fields and relations are SIBLING keys."""
    d=yaml.safe_load(open(p)); out=defaultdict(list)
    for sec,lst in d.items():
        c=W2SEC.get(sec)
        if not c or not isinstance(lst,list): continue
        spec=(M['core'].get(c) or M['supporting'].get(c) or {})
        df=set((spec.get('fields') or {}).keys()); dr=set((spec.get('relations') or {}).keys())
        for o in lst:
            if not isinstance(o,dict): continue
            out[c].append({'id':o.get('id'),
                           'f':{k:v for k,v in o.items() if k in df},
                           'r':{k:v for k,v in o.items() if k in dr}})
    return out

def rel_entries(v):
    if v is None: return []
    if isinstance(v,list): return v
    return [v]
def entry_id(e):
    # A relation entry is either a bare id or an ATTRIBUTED record (M01 declares `attributes:`
    # on has_skill / holds_role / held_by / assigned_to but never says how one is written in an
    # instance). vnc-045-instance.yaml keys attributed entries on `actor:`.
    # CORRECTION 2026-08-29 (post-close, #70): the original key list ('id','ref','target','to')
    # OMITTED `actor` and returned None SILENTLY, so all 21 attributed entries in the software
    # case were read as non-closing edges. Key order and the loud failure now match
    # vnc-045-validate.py's `rel_target`, the reader that got this right in the same run.
    if isinstance(e,dict):
        for k in ('actor','target','ref','id'):
            if k in e: return e[k]
        raise KeyError(f"attributed relation entry carries no target key; keys={sorted(e.keys())}")
    return e

def witness(objs):
    """-> dict model_path -> count of witnessing objects"""
    W=defaultdict(int)
    byid={}
    for c,lst in objs.items():
        for o in lst: byid[o['id']]=(c,o)
    for section in ('core','supporting'):
        for cname,spec in M[section].items():
            lst=objs.get(cname,[])
            if lst: W[f"{section}.{cname}"]=len(lst)
            for fn in (spec.get('fields') or {}):
                n=sum(1 for o in lst if real(o['f'].get(fn)))
                if n: W[f"{section}.{cname}.fields.{fn}"]=n
            for rn,rspec in (spec.get('relations') or {}).items():
                base=f"{section}.{cname}.relations.{rn}"
                n=sum(1 for o in lst if real(o['r'].get(rn)))
                if n:
                    W[base]=n
                    W[base+".cardinality"]=n
                    if isinstance(rspec,dict) and 'rule' in rspec: W[base+".rule"]=n
                # inverse: witnessed only when a declared inverse edge actually CLOSES
                if isinstance(rspec,dict) and 'inverse' in rspec:
                    inv=str(rspec['inverse']); invname=inv.split('.')[-1]
                    closed=0
                    for o in lst:
                        for e in rel_entries(o['r'].get(rn)):
                            tid=entry_id(e)
                            if tid is None or tid not in byid: continue
                            tc,to=byid[tid]
                            back=to['r'].get(invname)
                            if back is None: continue
                            if any(entry_id(b)==o['id'] for b in rel_entries(back)): closed+=1
                    if closed: W[base+".inverse"]=closed
                # attributes: an attributed entry carrying >=1 declared attribute
                if isinstance(rspec,dict) and 'attributes' in rspec:
                    attrs=set(rspec['attributes'] or [])
                    na=0
                    for o in lst:
                        for e in rel_entries(o['r'].get(rn)):
                            if isinstance(e,dict) and any(real(e.get(a)) for a in attrs): na+=1
                    if na: W[base+".attributes"]=na
    # value members and registry seeds actually used anywhere
    used=set()
    def harvest(v):
        # a value-vocabulary member is WITNESSED wherever it appears in instance data,
        # including inside a declared map field such as Event.extension. Absence of a
        # TYPED carrier is a separate finding (W3 F-A15/F-A16), not absence of a witness.
        if isinstance(v,str): used.add(v.strip())
        elif isinstance(v,(list,tuple)):
            for x in v: harvest(x)
        elif isinstance(v,dict):
            for x in v.values(): harvest(x)
    for c,lst in objs.items():
        for o in lst:
            for v in list(o['f'].values())+list(o['r'].values()): harvest(v)
    for vn,vs in M['values'].items():
        mem=vs.get('values') if isinstance(vs,dict) else None
        for m in (mem or []):
            if str(m) in used: W[f"values.{vn}.values.{m}"]=1
    for rn,rs in M['registries'].items():
        for sk in (rs.get('seeded') or {}):
            if str(sk) in used: W[f"registries.{rn}.seeded.{sk}"]=1
    return W

w1=witness(load_w1(f"{ART}/wfh-008-instance.yaml"))
w2=witness(load_w2(f"{ART}/vnc-045-instance.yaml"))
import json
json.dump({"w1":dict(w1),"w2":dict(w2)},open(f"{ART}/w4-witness.json","w"))
print("W1 witnessed paths:",len(w1)," W2 witnessed paths:",len(w2))
print()
print("=== the auditor's six, measured ===")
for p in ["core.Goal.relations.is_advanced_by","core.Capability.relations.advances",
          "core.Capability.relations.delivered_by","core.Unit.relations.delivers",
          "core.Event.relations.supersedes","supporting.Delegation.fields.expires_at"]:
    print(f"  {p:52s} W1={w1.get(p,0):3d}  W2={w2.get(p,0):3d}")
print()
print("=== sanity: rows that SHOULD have witnesses ===")
for p in ["core.Unit.fields.intended_outcome","supporting.Attempt.relations.unit",
          "core.Event.fields.occurred_at","supporting.Delegation.relations.derived_from"]:
    print(f"  {p:52s} W1={w1.get(p,0):3d}  W2={w2.get(p,0):3d}")
