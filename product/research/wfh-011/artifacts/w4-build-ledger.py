#!/usr/bin/env python3
"""wfh-011 W4 — build reports/construct-pressure-ledger.csv.
Reconciles W1 + W2 X dispositions onto one canonical spine (the SCOPE-literal X enumeration),
attaches W3 fixture evidence, and adds W4's independent adjudication. Read-only over inputs.
"""
import csv, re, json, hashlib, sys
from collections import Counter, defaultdict

ROOT="/workspaces/arch-research"
ART=f"{ROOT}/product/research/wfh-011/artifacts"
OUT=f"{ROOT}/product/research/wfh-011/reports/construct-pressure-ledger.csv"
M01=f"{ROOT}/product/factory/proposals/organizational-data-model-v5.yaml"
PIN="bf8e55364e36f15ddaf5241cfbb1339ac9672fd04746c14a96306d6fa9841060"
dig=hashlib.sha256(open(M01,'rb').read()).hexdigest()
if dig!=PIN: sys.exit(f"M01 DIGEST MISMATCH {dig}")
NA="not-applicable"

w1L=list(csv.DictReader(open(f"{ART}/wfh-008-coverage.csv")))
w2L=list(csv.DictReader(open(f"{ART}/vnc-045-coverage.csv")))
w3L=list(csv.DictReader(open(f"{ART}/rejection-results.csv")))
trL=list(csv.DictReader(open(f"{ART}/traversal-results.csv")))
w1={r['model_path']:r for r in w1L}; w2={r['model_path']:r for r in w2L}
CANON=[r['model_path'] for r in w2L]; CSET=set(CANON)

def w1_targets(p):
    if p in CSET: return [p]
    if re.match(r'^(core|supporting)\.\w+\.open\[\d+\]$',p): return [c for c in CANON if c.startswith(p+':')]
    if re.match(r'^(core|supporting)\.\w+\.relations\.\w+$',p): return [c for c in CANON if c==p or c.startswith(p+'.')]
    if re.match(r'^(core|supporting)\.\w+\.invariants$',p): return [c for c in CANON if c.startswith(p+'.')]
    if re.match(r'^registries\.\w+$',p): return [c for c in (f"{p}.status",f"{p}.seeded<EMPTY>") if c in CSET]
    if re.match(r'^registries\.\w+\.seeded\.[\w-]+$',p): return [c for c in CANON if c==p or c.startswith(p+'.')]
    if re.match(r'^registries\.\w+\.extension\.',p): return []
    if re.match(r'^catalogs\.\w+$',p): return [c for c in CANON if c.startswith(p+'.')]
    if re.match(r'^values\.\w+$',p): return [c for c in (f"{p}.status",f"{p}.definition") if c in CSET]
    m=re.match(r'^values\.(\w+)\.([\w\-]+)$',p)
    if m and not p.endswith('.rule'):
        t=f"values.{m.group(1)}.values.{m.group(2)}"; return [t] if t in CSET else []
    for pre,fmt in (('invariant:','invariants.{}'),('principle:','principles.{}'),('notation:','notation.{}'),
                    ('open:','open.{}'),('review-concern:','M02.sanity.{}'),('changelog:','changelog.{}')):
        if p.startswith(pre):
            t=fmt.format(p.split(':',1)[1]); return [t] if t in CSET else []
    if p.startswith('excluded:'):
        n=p.split(':',1)[1]; return [c for c in CANON if c.startswith(f"excluded[{n}]:")]
    if p=='traversal:Goal->Workflow': return ["traversal.Goal->applicable_Workflows"]
    if p=='traversal:Actor->Attempt': return ["traversal.Actor->participated_Attempts"]
    return []

w1cov=defaultdict(list); w1extra=[]
for r in w1L:
    t=w1_targets(r['model_path'])
    if not t: w1extra.append(r)
    for c in t: w1cov[c].append(r)

def w3_targets(p):
    for cand in (p,f"core.{p}",f"supporting.{p}"):
        if cand in CSET: return [cand]
    for cand in (p,f"core.{p}",f"supporting.{p}"):
        sub=[c for c in CANON if c.startswith(cand+'.') or c.startswith(cand+':')]
        if sub: return sub
    return []
w3cov=defaultdict(list); w3orphan=[]
for r in w3L:
    t=w3_targets(r['model_path'])
    if not t: w3orphan.append(r)
    for c in t: w3cov[c].append(r)

def cz(s): return [c.strip() for c in (s or '').replace(';','|').split('|') if c.strip() and c.strip()!=NA]
def pick(vals):
    """merge two workstream field values, labelled by origin; drop not-applicable."""
    out=[f"[{k}] {v}" for k,v in vals if v and v!=NA and v!='none']
    return " || ".join(out) if out else NA

# ---- W4 adjudication rules -------------------------------------------------
# ---- RW-3: instance-witness measurement (read from the two case INSTANCES themselves) ----
import subprocess, json as _json
subprocess.run([sys.executable, f"{ART}/w4-witness.py"], check=True, capture_output=True)
_W=_json.load(open(f"{ART}/w4-witness.json")); WIT1=_W['w1']; WIT2=_W['w2']
# Classes where "a populated instance witness" is a defined concept. Rows outside these
# classes assert consumption during encoding/analysis, not an instance witness, so the
# guard is not defined for them; they are reported in the findings, never silently flipped.
WITNESS_BEARING={'core-field','supporting-field','core-relation','supporting-relation',
 'core-relation-cardinality','supporting-relation-cardinality','core-relation-inverse',
 'supporting-relation-inverse','core-relation-rule','supporting-relation-rule',
 'core-relation-attributes','supporting-relation-attributes','value-member','registry-seed'}
AUDITOR_SIX={"core.Goal.relations.is_advanced_by","core.Capability.relations.advances",
 "core.Capability.relations.delivered_by","core.Unit.relations.delivers",
 "core.Event.relations.supersedes","supporting.Delegation.fields.expires_at"}
# Measured dispositions for rows the guard catches. `construct-pressure` where the emptiness
# is itself an evidenced finding; `not-applicable` with the measured reason otherwise.
GUARD_PRESSURE={
 "core.Event.relations.supersedes":("model-defect|historical-evidence-gap",
   "W3 ADVERSE: F-E07 is accepted-defect — Event.supersedes, Record.supersedes and Workflow.supersedes declare NO acyclicity, so an Event may supersede itself and a correction chain can close on itself, erasing the history I1 exists to protect. M01 declares `acyclic` three times elsewhere. Separately MEASURED: the relation is populated on 0/32 W1 Events and 0/30 W2 Events, so the run has no conforming witness for it in either case. An adverse W3 result on a relation no case exercises is the weakest possible standing for the rule and the strongest for the defect."),
 "supporting.EffectBoundary.relations.enforces.cardinality":("enforcement-gap",
   "MEASURED 0 populated in both cases. Inherits the run's central custody result: no EffectBoundary enforces any Delegation anywhere (W1 31/31 empty, W2 every Delegation empty). Reported as absence, never as model failure or claimed refusal."),
 "supporting.EffectBoundary.relations.enforces.inverse":("enforcement-gap",
   "MEASURED: 0 declared-inverse edges close in either case, because the relation is empty in both. The inverse is not falsified — it is untested, because enforced authority has no witness in this run."),
 "supporting.Delegation.relations.enforced_by.inverse":("enforcement-gap",
   "MEASURED: 0 closing edges in either case. Same fact from the Delegation side; `without a boundary authority is declared only` has no instance to constrain."),
 "core.Capability.relations.advances":("historical-evidence-gap|model-defect",
   "MEASURED 0 populated: W1 has zero Capability objects; W2 has two and populates `advances` on neither. W2's committed witness text read `instantiated in vnc-045-instance.yaml`, which the instance contradicts."),
 "core.Capability.relations.delivered_by":("historical-evidence-gap|model-defect",
   "MEASURED 0 populated in both. W2's own text says `EMPTY, deliberately` — the project pre-registered that vnc-045 delivers no capability — and the row was still dispositioned exercised."),
 "core.Actor.relations.has_skill.attributes":("historical-evidence-gap",
   "MEASURED: 0 attributed entries carry any of the four declared attributes [evidence_refs, grade, currentness, expires_at] in either case. This is W1's PR-SKILL-EVIDENCE-ABSENT measured on the relation itself: actors are assigned by type, never by evidenced competence."),
 "core.Actor.relations.holds_role.attributes":("historical-evidence-gap",
   "MEASURED: 0 attributed entries carry any declared attribute [scope_ref, effective_at, expires_at] in either case."),
 "core.Goal.fields.north_star":("historical-evidence-gap",
   "MEASURED 0 populated. W1's committed row reads `set on 2/2 instances`; the instance carries `north_star: []` on both Goals, and W2 carries the placeholder `missing-history`. W1's generator counts KEY PRESENCE, not value population — the same label-over-value defect the audit found in W2's table, on W1's side. Related to PR-LIST-REQUIRED: M01's `notation` does not say whether `required` on a list type means key-present or non-empty."),
}
def guard_reason(p):
    a=WIT1.get(p,0); b=WIT2.get(p,0)
    return (f"RW-3 GUARD: measured directly from both case instances — populated witnesses "
            f"wfh-008={a}, vnc-045={b}. Neither history supplies a witness, so `exercised` is a "
            f"label promoted over an untested value. Absence is not filled.")

PRIO={'construct-pressure':4,'blocked-by-OPEN':3,'exercised':2,'inspected-no-material-instance':1,'not-applicable':0}
INTRINSIC=('principles.','notation.','invariants.','excluded[','open.','M02.sanity.','changelog.','traversal.')
ADVERSE_W3={'accepted-defect','specified-not-enforced'}

# rows where W4 overrides on evidence (model-intrinsic disagreements resolved against
# the workstream whose own evidence text contradicts its label, corroborated by W3)
W4_OVERRIDE={
 'M02.sanity.S2':('construct-pressure','W3 CONFIRMED S2 mechanically: the dotted inverse needs a resolver special case, and notation still does not document the qualified form. W2 labelled the row exercised while its own witness text confirms the defect; the label, not the evidence, is what diverged.'),
 'M02.sanity.S3':('construct-pressure','W3 CONFIRMED and EXTENDED S3 (form/owner/extension_owner plus definition/invariants/open, and Event.identity is a map where notation describes a scalar). W2 labelled exercised while its own witness text says "undocumented ... the reader is relying on inference".'),
 'M02.sanity.S4':('construct-pressure','W3 CONFIRMED S4 with one executed proof (I17: one clause mechanizes via F-E28, the other does not via F-E26/F-E27). W2 dispositioned the row exercised while carrying cause model-defect on the same row - internally inconsistent; W1 and W3 agree it is pressure.'),
 'M02.sanity.S6':('construct-pressure','W3 CONFIRMED S6 mechanically: extension_owner sits on 6 constructs and 5 of them do not cite I19. Both workstreams state this fact; only the labels differed.'),
 'open.workflow_promotion':('construct-pressure','W2 ruled resolved-by-instance; W1 ruled still-open ("one case is not adjudication"). W4 rules STILL-OPEN: two owner-operated histories inside one organization cannot settle a cross-program promotion question, and review concern 12 binds the verdict to that limit.'),
 'core.Unit.open[0]:interruption and resume':('construct-pressure','W2 ruled resolved-by-instance-at-document-altitude; W1 ruled still-open and it is the seat of PR-ATTEMPT-DISPOSITION. W4 rules STILL-OPEN: an Attempt terminated with no actor-recorded disposition has no admissible enum value, and W1 CF-03 explicitly does NOT repair it.'),
 'open.delegation_attenuation':('construct-pressure','STILL-OPEN and adverse. W3 F-E26 (A5 derived from A1) and F-E27 (resource_ceiling 500 from a parent granting 0) are both accepted-defect. Executed W1 checker: 24 derived Delegations UNDECIDABLE on the non-numeric axes (W1 prose says 20 - the executed result governs).'),
}

COLS=["x_id","x_class","row_scope","source_id","model_path","instance_id","instance_version","value",
      "provenance","custody","invariant_check_ids","enforcement_reality","open_pressure_disposition",
      "w1_disposition","w2_disposition","reconciled_disposition","divergence_class","divergence_adjudication",
      "w3_fixture_ids","w3_results","w3_adverse",
      "cause_classification","classification_evidence","current_project_fit","evolution_change",
      "independent_reason","semantic_proof_authority_custody_preservation","migration_cost",
      "affected_artifacts","current_form_representable","evolved_form_representable","post_evolution_fit",
      "unresolved_discriminator","evolution_candidate_id","evolution_challenge_result","w4_adjudication"]

# evolution candidate challenge outcomes (authored by W4; see findings section 7)
CHAL={
 'W1/CF-01':'survives-with-recorded-defect (concern 17: after the 2026-08-29 correction the affected_artifacts list DROPPED the two errata surfaces, while W4 measurement STRENGTHENED the residual - origin has no workflow/* branch at all)',
 'W1/CF-02':'survives (all six challenges; states its own limit - a manifest detects drift and does not establish custody)',
 'W1/CF-03':'survives (and correctly declares that the model defect is NOT repaired by the evolution)',
 'W1/CF-04':'survives (refuses the laundering: raises altitude to reported-observation, not mechanical-observation)',
 'W1/CF-05':'survives',
 'W1/CF-06':'survives-with-recorded-defect (independent reason asserted but unevidenced inside the fixed alphabet; W1 own unresolved_discriminator concedes no concrete error is evidenced)',
 'W1/CF-07':'FAILS concern 17 (migration realism): the change targets a service outside the alphabet and W1 states the cost cannot be established; cost, compatibility and coexistence are therefore not explicit. The underlying model-defect is unaffected.',
 'W2/CF-01':'survives',
 'W2/CF-02':'survives',
 'W2/CF-03':'survives (authority moves away from the governed actors)',
 'W2/CF-04':'survives (best-evidenced candidate in the run; the 14->15 contradiction is W4-reproduced)',
 'W2/CF-05':'survives (only candidate that supplies an enforcement point, analyses concern 15 explicitly, and refuses to let post-evolution fit conceal the current reject on GT-06)',
}
def cand_id(x1,x2):
    ids=[]
    e1=(x1 or {}).get('evolution_change',NA); e2=(x2 or {}).get('evolution_change',NA)
    m=re.search(r'CF-0\d',e1 or '')
    if m: ids.append('W1/'+m.group(0))
    elif e1 not in (NA,'','not-proposed') : ids.append('W1/unlabelled')
    m=re.search(r'CF-0\d',e2 or '')
    if m: ids.append('W2/'+m.group(0))
    return ';'.join(ids) if ids else NA


RW4={
 "supporting.Gate.relations.requires_assessor":("W1/CF-05","survives"),
 "invariants.I10":("W1/CF-06","survives, recorded defect — independent reasonableness not evidenced inside the fixed alphabet"),
 "notation.types":("W1/CF-07","FAILS concern 17 (migration realism)"),
 "core.Record.fields.content_digest":("W1/CF-07","FAILS concern 17 (migration realism)"),
 "M02.sanity.S3":("W1/CF-07","FAILS concern 17 (migration realism)"),
}

rows=[]
for c in CANON:
    b=w2[c]; a=None
    al=w1cov.get(c,[])
    if al: a=sorted(al,key=lambda r:-PRIO.get(r['disposition'],0))[0]
    d1=a['disposition'] if a else 'not-enumerated'
    d2=b['disposition']
    if not a: dk='w1-not-enumerated'
    elif d1==d2: dk='agree'
    else: dk='divergent'
    ds=[d for d in (d1,d2) if d!='not-enumerated']
    rec=sorted(ds,key=lambda d:-PRIO.get(d,0))[0]
    f3=w3cov.get(c,[])
    adverse=sorted({r['actual_result'] for r in f3} & ADVERSE_W3)
    # divergence adjudication
    if dk=='agree': adj='not-applicable (both workstreams agree)'
    elif dk=='w1-not-enumerated':
        adj=('W1 did not enumerate this X item. Its 468-row enumeration rolls relation sub-keys, per-invariant '
             'bindings, construct `definition` and registry seed-fields up into coarser rows; W2\'s 679-row '
             'enumeration matches the SCOPE X clause literally and is adopted as the canonical spine. '
             'Reconciled from W2 alone - absence is not filled.')
    elif c.startswith(INTRINSIC):
        adj=('MODEL-INTRINSIC divergence: the property is a property of M01, so a case difference cannot explain it. '
             'Adjudicated on the workstreams\' own evidence text plus W3 execution.')
    else:
        s=set((d1,d2))
        if s=={'exercised','not-applicable'}:
            adj=('CASE-DIFFERENCE, not contradiction: one history supplies a witness and the other does not. '
                 'Reconciled to `exercised` - the run as a whole has a witness. Neither case is corrected by the other.')
        elif 'construct-pressure' in s and 'not-applicable' in s:
            adj=('CASE-DIFFERENCE: pressure observed in one history, the construct absent from the other. '
                 'Reconciled to `construct-pressure` - pressure evidenced in either case stands for the run and is never averaged away.')
        elif 'construct-pressure' in s and 'exercised' in s:
            adj=('MATERIAL DIVERGENCE: one case carries the construct without strain and the other strains against it. '
                 'Both stand: the `exercised` side is a witness that the construct can carry at least one history, '
                 'the `construct-pressure` side is evidence the construct does not carry every history. '
                 'Reconciled to `construct-pressure`; the positive witness is retained in `value`.')
        else:
            adj=('DIVERGENCE adjudicated to the higher-pressure disposition; absence is never filled and '
                 'no OPEN is normalised into a default.')
    if c in W4_OVERRIDE:
        rec,ovr=W4_OVERRIDE[c]; adj=adj+" || W4 OVERRIDE: "+ovr
    causes=sorted(set(cz((a or {}).get('cause_classification')))|set(cz(b.get('cause_classification'))))
    # W4 supplies a cause where a pressure row carries none (W1 coverage clause 9 defect)
    w4note=[]
    if rec in ('construct-pressure','blocked-by-OPEN') and not causes:
        if c.endswith(tuple(f"open[{i}]" for i in range(6))) or ':' in c.split('.')[-1] or '.open[' in c:
            causes=['unresolved']
            w4note.append('W4-SUPPLIED CAUSE: W1 dispositioned this row construct-pressure with cause_classification '
                          'not-applicable, which the amendment\'s coverage clause 9 forbids. W4 classifies it `unresolved`: '
                          'the row records an unsettled OPEN item, and the evidence does not yet discriminate '
                          'model-defect from historical-evidence-gap. It counts as neither conforming nor rejecting evidence.')
        else:
            causes=['unresolved']
            w4note.append('W4-SUPPLIED CAUSE: pressure row carried no cause classification in either workstream; '
                          'classified `unresolved` rather than assigned a cause the evidence does not support.')
    if adverse:
        w4note.append('W3 ADVERSE at this path: '+';'.join(r['fixture_id']+'='+r['actual_result'] for r in f3 if r['actual_result'] in ADVERSE_W3))
    cid=cand_id(a,b)
    chal=';'.join(CHAL.get(i,'not-challenged') for i in cid.split(';')) if cid!=NA else NA
    # ---- RW-4: carry W4 section 7's own rulings into the ledger ----
    if c in RW4:
        _id,_res = RW4[c]
        cid = _id if cid==NA or 'unlabelled' in cid else (cid+';'+_id if _id not in cid else cid)
        cid = cid.replace('W1/unlabelled;','').replace(';W1/unlabelled','').replace('W1/unlabelled',_id)
        chal = _res
    # ---- RW-3: refuse `exercised` where no populated instance witness exists on either side ----
    # ANNOTATE every zero-witness row in a witness-bearing class; REFUSE `exercised` on it.
    # The two are separate: W2's RW-1 rework independently moved several of the auditor's six
    # off `exercised` before this guard ran, so they are no longer refused — but RW-3 still
    # requires the boilerplate on them be replaced by the measured fact.
    guard_hit=False
    if b['x_class'] in WITNESS_BEARING and WIT1.get(c,0)==0 and WIT2.get(c,0)==0:
        guard_hit=True
        was=rec
        gp=GUARD_PRESSURE.get(c)
        if gp:
            rec='construct-pressure'
            causes=sorted(set(causes)|set(gp[0].split('|')))
            w4note.append("RW-3 GUARD (measured): "+gp[1])
        elif rec=='exercised':
            rec='not-applicable'
            w4note.append(guard_reason(c)+" Dispositioned `not-applicable` on the measured reason: "
              "the construct or relation has no occurrence in either history, so the sub-rule has nothing to be exercised by.")
        else:
            w4note.append(guard_reason(c)+f" Disposition `{rec}` was already correct before this guard ran "
              "(W2's RW-1 rework reached it independently); the row is annotated with the measurement, not moved.")
        if was!=rec: w4note.append(f"RW-3 DISPOSITION CHANGE: {was} -> {rec}.")
        adj=(("[AUDITOR-SIX] " if c in AUDITOR_SIX else "[GUARD-FOUND beyond the auditor's six] ")
             + guard_reason(c)
             + " The prior boilerplate (\"one history supplies a witness and the other does not\") is REPLACED: on this row neither did.")
    ev=[(k,v) for k,v in (('W1',(a or {}).get('evolution_change',NA)),('W2',b.get('evolution_change',NA)))]
    rows.append({
      "x_id":c, "x_class":b['x_class'],
      "row_scope":"model-X",
      "source_id":pick([('W1',(a or {}).get('source_id',NA)),('W2','M01,M02,M06,S01-S06,T01-T03')]),
      "model_path":c,
      "instance_id":pick([('W1',(a or {}).get('instance_id',NA)),('W2',b.get('instance_ref',NA))]),
      "instance_version":(a or {}).get('instance_version',NA),
      "value":pick([('W1',(a or {}).get('value',NA)),('W2',b.get('value_or_witness',NA))]),
      "provenance":pick([('W1',(a or {}).get('provenance',NA)),('W2',b.get('provenance',NA))]),
      "custody":pick([('W1',(a or {}).get('custody',NA)),('W2',b.get('custody',NA))]),
      "invariant_check_ids":pick([('W1',(a or {}).get('invariant_check_ids',NA)),('W2',b.get('applicable_checks',NA)),
                                  ('W3',';'.join(r['fixture_id'] for r in f3) or NA)]),
      "enforcement_reality":pick([('W1',(a or {}).get('enforcement_reality',NA)),('W2',b.get('enforcement_reality',NA))]),
      "open_pressure_disposition":pick([('W1',(a or {}).get('open_pressure_disposition',NA)),('W2',b.get('open_pressure_disposition',NA))]),
      "w1_disposition":d1,"w2_disposition":d2,"reconciled_disposition":rec,
      "divergence_class":dk,"divergence_adjudication":adj,
      "w3_fixture_ids":';'.join(r['fixture_id'] for r in f3) or NA,
      "w3_results":';'.join(sorted({r['actual_result'] for r in f3})) or NA,
      "w3_adverse":';'.join(adverse) or NA,
      "cause_classification":'|'.join(causes) if causes else NA,
      "classification_evidence":pick([('W1',(a or {}).get('classification_evidence',NA)),('W2',b.get('classification_evidence',NA))]) if causes else NA,
      "current_project_fit":pick([('W1',(a or {}).get('current_project_fit',NA)),('W2',b.get('current_project_fit',NA))]) if causes else NA,
      "evolution_change":pick(ev),
      "independent_reason":pick([('W1',(a or {}).get('independent_reason',NA)),('W2',b.get('independent_reason',NA))]),
      "semantic_proof_authority_custody_preservation":pick([('W1',(a or {}).get('semantic_proof_authority_custody_preservation',NA)),('W2',b.get('semantic_proof_authority_custody_preservation',NA))]),
      "migration_cost":pick([('W1',(a or {}).get('migration_cost',NA)),('W2',b.get('migration_cost',NA))]),
      "affected_artifacts":pick([('W1',(a or {}).get('affected_artifacts',NA)),('W2',b.get('affected_artifacts',NA))]),
      "current_form_representable":pick([('W1',(a or {}).get('current_form_representable',NA)),('W2',b.get('current_form_representable',NA))]),
      "evolved_form_representable":pick([('W1',(a or {}).get('evolved_form_representable',NA)),('W2',b.get('evolved_form_representable',NA))]),
      "post_evolution_fit":pick([('W1',(a or {}).get('post_evolution_fit',NA)),('W2',b.get('post_evolution_fit',NA))]),
      "unresolved_discriminator":pick([('W1',(a or {}).get('unresolved_discriminator',NA)),('W2',b.get('unresolved_discriminator',NA))]),
      "evolution_candidate_id":cid,"evolution_challenge_result":chal,
      "w4_adjudication":' || '.join(w4note) if w4note else NA,
    })

# --- appendix A: W1 rows that are NOT model-X items (instance-level registry extensions)
for r in w1extra:
    rows.append({**{c:NA for c in COLS},
      "x_id":r['model_path'],"x_class":"instance-extension","row_scope":"instance-extension (NOT a model X item)",
      "source_id":r['source_id'],"model_path":r['model_path'],"instance_id":r['instance_id'],
      "instance_version":r['instance_version'],"value":r['value'],"provenance":r['provenance'],
      "custody":r['custody'],"invariant_check_ids":r['invariant_check_ids'],
      "enforcement_reality":r['enforcement_reality'],"open_pressure_disposition":r['open_pressure_disposition'],
      "w1_disposition":r['disposition'],"w2_disposition":"not-enumerated","reconciled_disposition":r['disposition'],
      "divergence_class":"w1-only","divergence_adjudication":(
        "W1 enumerated the program-owned registry entries it AUTHORED as coverage rows. These are instance-level "
        "extensions, not items of the model X alphabet, so they carry no X coverage obligation and are excluded "
        "from the 679-row spine. Retained here so nothing W1 produced is silently dropped."),
      "cause_classification":r['cause_classification'] if cz(r['cause_classification']) else NA,
      "w4_adjudication":"counted separately; NOT part of the reconciled X count"})

# --- appendix B: W3 fixtures with no canonical X home
for r in w3orphan:
    rows.append({**{c:NA for c in COLS},
      "x_id":"W3-orphan:"+r['fixture_id'],"x_class":"w3-fixture","row_scope":"w3-fixture (no canonical X path)",
      "model_path":r['model_path'],"value":r['x_item'],
      "w1_disposition":"not-enumerated","w2_disposition":"not-enumerated",
      "reconciled_disposition":"construct-pressure" if r['actual_result'] in ADVERSE_W3 else "exercised",
      "divergence_class":"w3-only",
      "divergence_adjudication":("W3 fixture whose model_path is finer than any canonical X row (a required_extension "
        "key or a registry shape key). Retained so no executed rejection result is dropped."),
      "w3_fixture_ids":r['fixture_id'],"w3_results":r['actual_result'],
      "w3_adverse":r['actual_result'] if r['actual_result'] in ADVERSE_W3 else NA,
      "cause_classification":"model-defect" if r['actual_result'] in ADVERSE_W3 else NA,
      "classification_evidence":r['note'] or r['mutation'],
      "enforcement_reality":"specified-not-enforced" if r['actual_result']=='specified-not-enforced' else "checker built from M01 only; no runtime enforcement exists",
      "w4_adjudication":"counted separately; NOT part of the reconciled X count"})

for r in rows:
    for c in COLS:
        if r.get(c) in (None,""): r[c]=NA
with open(OUT,"w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=COLS); w.writeheader()
    for r in rows: w.writerow(r)

X=[r for r in rows if r['row_scope']=='model-X']
print("ledger rows total:",len(rows))
print("  model-X rows:",len(X))
print("  appendix instance-extension rows:",sum(1 for r in rows if r['row_scope'].startswith('instance-extension')))
print("  appendix w3-fixture rows:",sum(1 for r in rows if r['row_scope'].startswith('w3-fixture')))
print()
print("reconciled disposition:",dict(Counter(r['reconciled_disposition'] for r in X)))
print("divergence class:",dict(Counter(r['divergence_class'] for r in X)))
cc=Counter()
for r in X:
    for c in cz(r['cause_classification']): cc[c]+=1
print("RECONCILED cause tally (row-weighted):",dict(cc))
print("rows carrying >=1 cause:",sum(1 for r in X if cz(r['cause_classification'])))
print("pressure rows with NO cause:",sum(1 for r in X if r['reconciled_disposition'] in ('construct-pressure','blocked-by-OPEN') and not cz(r['cause_classification'])))
print("rows with a silent blank:",sum(1 for r in rows for c in COLS if r[c]==""))
print("W3-adverse rows:",sum(1 for r in X if r['w3_adverse']!=NA))
print("evolution-candidate rows:",sum(1 for r in X if r['evolution_candidate_id']!=NA))
