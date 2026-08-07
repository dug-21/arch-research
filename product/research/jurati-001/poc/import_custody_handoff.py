#!/usr/bin/env python3
"""Import only a custodian's public handoff and named sanitized judge packets."""
import hashlib,json,os,re,shutil,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/"corpus-generated"; EXPECTED_HANDOFF="5b0239085a70bcfacde6f9b77a09c280d3c34fb70a3cedce1869aa495b74c7c1"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(x): raise SystemExit("FAIL: "+x)
def main():
 if len(sys.argv)!=2: fail("usage: import_custody_handoff.py public-handoff.json")
 handoff_path=Path(sys.argv[1]).resolve()
 if handoff_path.stat().st_mode&0o777!=0o600 or sha(handoff_path)!=EXPECTED_HANDOFF: fail("handoff mode/digest")
 handoff=json.loads(handoff_path.read_text()); judge=Path(handoff["judge_input_path"]).resolve()
 if handoff["digests"]["packet_manifest_sha256"]!="68367443efc7adb5f71aa99b6f36676bc8f44e462eda722202b05612dc34134c": fail("manifest commitment")
 if handoff["digests"]["schema_sha256"]!="12e143feb80b5615d6bfa744520316b54f0fbcea1bac6bad6ff11ebd0f7785fb": fail("schema commitment")
 if sha(judge/"SHA256SUMS")!=handoff["digests"]["packet_manifest_sha256"]: fail("packet manifest digest")
 sums={line.split("  ",1)[1]:line.split("  ",1)[0] for line in (judge/"SHA256SUMS").read_text().splitlines()}
 if len(sums)!=11 or any(sha(judge/name)!=dig for name,dig in sums.items()): fail("packet count/digest")
 expected={f"A-H{i:02}.json" for i in range(1,9)}|{f"B-H{i:02}.json" for i in range(1,4)}
 if set(sums)!=expected: fail("opaque ID set")
 forbidden={"label","reference","real_cycle","source_path","next_action","verdict_summary","historical_outcome"}
 manifest=[json.loads(x) for x in (OUT/"manifest.jsonl").read_text().splitlines()]
 for name in sorted(sums):
  obj=json.loads((judge/name).read_text()); eid=name[:-5]
  if set(obj)&forbidden or obj.get("episode_id")!=eid or obj.get("domain") not in {"sdlc","garage"}: fail("packet schema/leakage")
  text=(judge/name).read_text()
  if re.search(r"product/(features|research)/[^\s`]+",text): fail("real source path leakage")
  shutil.copyfile(judge/name,OUT/"packets"/name)
  row=next(x for x in manifest if x["episode_id"]==eid); row["packet_sha256"]=sha(OUT/"packets"/name); row["custody_schema_sha256"]=handoff["digests"]["schema_sha256"]
 (OUT/"manifest.jsonl").write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n" for x in manifest))
 commitment={"schema":"jurati-custody-handoff-commitment-v1","handoff_sha256":EXPECTED_HANDOFF,"packet_manifest_sha256":handoff["digests"]["packet_manifest_sha256"],"schema_sha256":handoff["digests"]["schema_sha256"],"record_count":11,"custody":"references and identity mapping remain with W1 custodian; PoC consumes sanitized judge packets only"}
 (OUT/"restricted-map-commitment.json").write_text(json.dumps(commitment,sort_keys=True,separators=(",",":"))+"\n")
 files=sorted(p for p in OUT.rglob("*") if p.is_file() and p.name!="SHA256SUMS")
 (OUT/"SHA256SUMS").write_text("".join(f"{sha(p)}  {p.relative_to(OUT)}\n" for p in files))
 print(json.dumps({"status":"PASS","imported":11,"packet_manifest_sha256":commitment["packet_manifest_sha256"]},sort_keys=True))
if __name__=="__main__": main()
