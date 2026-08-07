#!/usr/bin/env python3
"""Fail-closed corpus freeze verifier. Does not print restricted values."""
import hashlib,json,re,subprocess,sys
from collections import Counter,defaultdict
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/"corpus-generated"
OUTCOME=re.compile(r"(^|[^A-Za-z])(PASS|FAIL|WARN|PENDING|APPROVE[D]?|REJECT(?:ED)?|REWORK(?:ABLE)?|PROVEN|PARTIAL|DEMONSTRATED|CONTRADICTED|NOT[_ ]DEMONSTRATED|INSUFFICIENT[_ ]EVIDENCE)([^A-Za-z]|$)",re.I)
SUMMARY=re.compile(r"^\s*(?:#{1,6}\s+|[-*]>?\s*)?(?:\*\*)?(verdict|outcome|recommendation|conclusion|decision summary|gate result|next action|result|status)(?:\*\*)?\s*[:|—-]",re.I|re.M)
TABLE_HEADER=re.compile(r"\|.*\b(verdict|outcome|result|status|next action|transition|recommendation)\b.*\|",re.I)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(x): raise SystemExit("FAIL: "+x)
ROOT=Path(__file__).resolve().parents[4]
def main():
    manifest=[json.loads(x) for x in (OUT/"manifest.jsonl").read_text().splitlines()]
    labels=[json.loads(x) for x in (OUT/"reference-labels-nonholdout.jsonl").read_text().splitlines()]
    commitment=json.loads((OUT/"restricted-map-commitment.json").read_text())
    if commitment.get("handoff_sha256")!="de2e87b179ed48e032756f36b2360269dd80c371af5632030bf6242f76092286" or commitment.get("encrypted_custody_sha256")!="2006fea93c8be898b672e4f8538781f3ab8f67dcc19c9b5c4b64547e947c6fee" or commitment.get("record_count")!=11: fail("custody commitment")
    if len(manifest)!=45 or Counter(x["domain"] for x in manifest)!={"sdlc":32,"garage":13}: fail("count")
    if len({x["episode_id"] for x in manifest})!=45: fail("duplicate episode")
    by=defaultdict(set); cap=Counter()
    for x in manifest: by[x["cycle"]].add(x["partition"]); cap[x["cycle"]]+=1
    if any(len(x)!=1 for x in by.values()) or max(cap.values())>3: fail("partition/cap")
    if Counter((x["domain"],x["partition"]) for x in manifest)!={('sdlc','development'):16,('sdlc','calibration'):8,('sdlc','holdout'):8,('garage','development'):7,('garage','calibration'):3,('garage','holdout'):3}: fail("split")
    label_ids={x["episode_id"] for x in labels}; hold={x["episode_id"] for x in manifest if x["partition"]=="holdout"}
    if label_ids!={x["episode_id"] for x in manifest if x["partition"]!="holdout"} or len(hold)!=11: fail("mapping")
    forbidden={"reference_class","next_action","verdict","label","source_path","real_cycle"}
    for x in manifest:
        p=OUT/"packets"/(x["episode_id"]+".json")
        if sha(p)!=x["packet_sha256"]: fail("packet digest")
        pkt=json.loads(p.read_text())
        if forbidden & set(pkt) or forbidden & set(pkt.get("judge_facing",{})): fail("reference leakage")
        if x["partition"]=="holdout":
            if set(pkt)!={"allowed_results","decision_type","domain","episode_id","evidence","required_output"}: fail("holdout schema")
            if re.search(r"product/(features|research)/[^\s`]+",p.read_text()) or "[cycle]" not in pkt["evidence"]: fail("holdout identity/path sanitization")
            if SUMMARY.search(pkt["evidence"]) or TABLE_HEADER.search(pkt["evidence"]) or OUTCOME.search(pkt["evidence"]): fail("holdout outcome exclusion")
    # Scan every tracked artifact and every owned reachable commit patch for serialized restricted fields.
    # New real identities are intentionally unavailable to this role; their absence is established by the
    # custodian's sanitized schema/digest, while this scanner catches any structural reintroduction.
    leak_patterns=[r'"(?:real_cycle|source_path|historical_outcome|reference_label|verdict_summary)"\s*:']
    tracked=subprocess.check_output(["git","-C",str(ROOT),"ls-files","--cached"],text=True).splitlines()
    for name in tracked:
        p=ROOT/name
        if p.is_file():
            text=p.read_text(errors="ignore").lower()
            if any(re.search(pattern,text,re.I) for pattern in leak_patterns): fail("tracked-artifact leakage in "+name)
    merge_base=subprocess.check_output(["git","-C",str(ROOT),"merge-base","main","HEAD"],text=True).strip()
    branch_patch=subprocess.check_output(["git","-C",str(ROOT),"log","-p",f"{merge_base}..HEAD"],text=True).lower()
    # The preserved validator report names the formerly unsafe filename as a coordination record; scan
    # added JSON records, not prose/file-name discussion.
    if re.search(r'^\+.*"(?:real_cycle|source_path|historical_outcome|reference_label|verdict_summary)"\s*:',branch_patch,re.I|re.M): fail("reachable branch-object/patch leakage")
    sums={line.split("  ",1)[1]:line.split("  ",1)[0] for line in (OUT/"SHA256SUMS").read_text().splitlines()}
    if any(sha(OUT/name)!=dig for name,dig in sums.items()): fail("final digest")
    print(json.dumps({"status":"PASS","episodes":45,"holdout":11,"tests":["counts","partition","cycle_cap","encrypted_custody_commitment","packet_integrity","reference_leakage","holdout_schema","identity_path_sanitization","outcome_heading_table_token_exclusion","tracked_artifact_leakage","reachable_branch_patch_leakage","final_hashes"]},sort_keys=True))
if __name__=="__main__": main()
