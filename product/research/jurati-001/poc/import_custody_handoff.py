#!/usr/bin/env python3
"""Import only a custodian's public handoff and named sanitized judge packets."""
import hashlib,json,re,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/"corpus-generated"; EXPECTED_HANDOFF="de2e87b179ed48e032756f36b2360269dd80c371af5632030bf6242f76092286"
OUTCOME=re.compile(r"(^|[^A-Za-z])(PASS|FAIL|WARN|PENDING|APPROVE[D]?|REJECT(?:ED)?|REWORK(?:ABLE)?|PROVEN|PARTIAL|DEMONSTRATED|CONTRADICTED|NOT[_ ]DEMONSTRATED|INSUFFICIENT[_ ]EVIDENCE)([^A-Za-z]|$)",re.I)
SUMMARY=re.compile(r"^\s*(?:#{1,6}\s+|[-*]>?\s*)?(?:\*\*)?(verdict|outcome|recommendation|conclusion|decision summary|gate result|next action|result|status)(?:\*\*)?\s*[:|—-]",re.I)
TABLE_HEADER=re.compile(r"\|.*\b(verdict|outcome|result|status|next action|transition|recommendation)\b.*\|",re.I)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(x): raise SystemExit("FAIL: "+x)
def main():
 if len(sys.argv)!=2: fail("usage: import_custody_handoff.py public-handoff.json")
 handoff_path=Path(sys.argv[1]).resolve()
 if handoff_path.stat().st_mode&0o777!=0o600 or sha(handoff_path)!=EXPECTED_HANDOFF: fail("handoff mode/digest")
 handoff=json.loads(handoff_path.read_text()); judge=Path(handoff["judge_input_path"]).resolve()
 if handoff["digests"]["packet_manifest_sha256"]!="1b310a137cf20e28339cb50e73757081c50f2b10287465fb9aa5f002e42d9590": fail("manifest commitment")
 if handoff["digests"]["schema_sha256"]!="3a1c3d9e264231b5f0c7b0cb9332b5d617bfee9b603834538e62bfbdc51806e2": fail("schema commitment")
 if handoff["digests"]["encrypted_custody_sha256"]!="2006fea93c8be898b672e4f8538781f3ab8f67dcc19c9b5c4b64547e947c6fee": fail("encrypted custody commitment")
 if sha(judge/"SHA256SUMS")!=handoff["digests"]["packet_manifest_sha256"]: fail("packet manifest digest")
 sums={line.split("  ",1)[1]:line.split("  ",1)[0] for line in (judge/"SHA256SUMS").read_text().splitlines()}
 if len(sums)!=11 or any(sha(judge/name)!=dig for name,dig in sums.items()): fail("packet count/digest")
 expected={f"A2-H{i:02}.json" for i in range(1,9)}|{f"B2-H{i:02}.json" for i in range(1,4)}
 if set(sums)!=expected: fail("opaque ID set")
 forbidden={"label","reference","real_cycle","source_path","next_action","verdict_summary","historical_outcome"}
 manifest=[json.loads(x) for x in (OUT/"manifest.jsonl").read_text().splitlines()]
 old=sorted((x for x in manifest if x["partition"]=="holdout"),key=lambda x:x["episode_id"])
 new_ids=sorted(name[:-5] for name in expected)
 if len(old)!=len(new_ids): fail("public holdout placeholder count")
 for row,eid in zip(old,new_ids):
  row["episode_id"]=eid
  n=int(eid[-2:]); row["cycle"]=(eid.split("-")[0]+"-HC"+("01" if n<=3 else "02" if n<=5 else "03" if n<=7 else "04")) if eid.startswith("A2") else ("B2-HC01" if n<=2 else "B2-HC02")
 for p in (OUT/"packets").glob("[AB]-H*.json"): p.unlink()
 removed={}
 for name in sorted(sums):
  obj=json.loads((judge/name).read_text()); eid=name[:-5]
  if set(obj)&forbidden or obj.get("episode_id")!=eid or obj.get("domain") not in {"sdlc","garage"}: fail("packet schema/leakage")
  text=(judge/name).read_text()
  if re.search(r"product/(features|research)/[^\s`]+",text): fail("real source path leakage")
  kept=[]; dropped=0; in_result_table=False
  for line in obj["evidence"].splitlines():
   if TABLE_HEADER.search(line): in_result_table=line.lstrip().startswith("|"); dropped+=1; continue
   if in_result_table and line.lstrip().startswith("|"): dropped+=1; continue
   if in_result_table: in_result_table=False
   if SUMMARY.search(line) or OUTCOME.search(line): dropped+=1; continue
   kept.append(line)
  obj["evidence"]="\n".join(kept)+"\n"; removed[eid]=dropped
  transformed=json.dumps(obj,sort_keys=True,indent=2)+"\n"
  if SUMMARY.search(obj["evidence"]) or TABLE_HEADER.search(obj["evidence"]) or OUTCOME.search(obj["evidence"]): fail("outcome exclusion incomplete for "+eid)
  (OUT/"packets"/name).write_text(transformed)
  row=next(x for x in manifest if x["episode_id"]==eid); row["packet_sha256"]=sha(OUT/"packets"/name); row["custody_schema_sha256"]=handoff["digests"]["schema_sha256"]
 (OUT/"manifest.jsonl").write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n" for x in manifest))
 splits={p:sorted(x["episode_id"] for x in manifest if x["partition"]==p) for p in ["development","calibration","holdout"]}
 (OUT/"splits.json").write_text(json.dumps(splits,sort_keys=True,separators=(",",":"))+"\n")
 (OUT/"evidence-exclusion-summary.json").write_text(json.dumps({"schema":"jurati-evidence-exclusion-v1","removed_lines_by_opaque_episode":removed,"total_removed_lines":sum(removed.values())},sort_keys=True,indent=2)+"\n")
 commitment={"schema":"jurati-custody-handoff-commitment-v2","handoff_sha256":EXPECTED_HANDOFF,"packet_manifest_sha256":handoff["digests"]["packet_manifest_sha256"],"schema_sha256":handoff["digests"]["schema_sha256"],"encrypted_custody_sha256":handoff["digests"]["encrypted_custody_sha256"],"record_count":11,"custody":"encrypted identity/reference custody held by W1; key not persisted or returned; PoC consumes sanitized judge packets only"}
 (OUT/"restricted-map-commitment.json").write_text(json.dumps(commitment,sort_keys=True,separators=(",",":"))+"\n")
 files=sorted(p for p in OUT.rglob("*") if p.is_file() and p.name!="SHA256SUMS")
 (OUT/"SHA256SUMS").write_text("".join(f"{sha(p)}  {p.relative_to(OUT)}\n" for p in files))
 print(json.dumps({"status":"PASS","imported":11,"packet_manifest_sha256":commitment["packet_manifest_sha256"]},sort_keys=True))
if __name__=="__main__": main()
