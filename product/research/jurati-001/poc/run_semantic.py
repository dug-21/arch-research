#!/usr/bin/env python3
"""Frozen fail-closed B/C runner over sanitized, opaque custodian packets."""
import hashlib,json,sys,time,urllib.request
from pathlib import Path
from jurati import validate_judge_response
BASE=Path(__file__).resolve().parents[1]; ROOT=Path(__file__).resolve().parents[4]
PROMPT=(BASE/"task/semantic-prompt-v1.txt").read_text(); POLICY=json.loads((BASE/"task/semantic-policy-v1.json").read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
 if len(sys.argv)!=4 or sys.argv[1] not in {"B","C"}: raise SystemExit("usage: run_semantic.py B|C OPAQUE_EPISODE OUTPUT.jsonl")
 arm,eid,out=sys.argv[1],sys.argv[2],Path(sys.argv[3])
 attest=json.loads((BASE/"artifacts/non-inspection-attestations.json").read_text())
 if set(attest["roles"])!={"W2","W4","W5","W6"} or not all(x["attested"] for x in attest["roles"].values()): raise SystemExit("attestations incomplete")
 packet=json.loads((BASE/"corpus-generated/packets"/(eid+".json")).read_text()); domain=packet["domain"]
 if not eid.endswith(tuple(f"{i:02}" for i in range(1,9))) or "evidence" not in packet: raise SystemExit("not a sanitized opaque holdout packet")
 evidence=packet["evidence"]
 if not isinstance(evidence,str) or "[cycle]" not in evidence: raise SystemExit("custody sanitization marker absent")
 clause={"id":"semantic-1","evidence_ids":["primary"]}
 cfg=POLICY["arms"][arm]; request={"model":cfg["model"],"stream":False,"format":"json","options":POLICY["generation"]["options"],
  "prompt":PROMPT+"\nCLAUSE ID: semantic-1\nQUESTION: Assess the bounded "+packet["decision_type"]+" decision from the evidence.\nEVIDENCE ID primary:\n"+evidence}
 for rep in range(cfg["repetitions"]):
  t=time.perf_counter_ns(); req=urllib.request.Request(POLICY["endpoint"]+"/api/generate",data=json.dumps(request).encode(),headers={"Content-Type":"application/json"})
  with urllib.request.urlopen(req,timeout=POLICY["timeout_seconds"]) as response: result=json.loads(response.read())
  if result.get("model")!=cfg["model"]: raise SystemExit("model identity mismatch")
  parsed=json.loads(result["response"]); accepted=validate_judge_response(clause,parsed)
  record={"episode_id":eid,"arm":arm,"repetition":rep+1,"result":accepted,"rationale":parsed["rationale"],"evidence_refs":parsed["evidence_refs"],
          "model":cfg["model"],"model_digest":cfg["model_digest"],"prompt_sha256":sha(PROMPT.encode()),"policy_sha256":sha((BASE/"task/semantic-policy-v1.json").read_bytes()),"evidence_sha256":sha(evidence.encode()),"latency_ns":time.perf_counter_ns()-t}
  with out.open("a") as f: f.write(json.dumps(record,sort_keys=True,separators=(",",":"))+"\n"); f.flush()
if __name__=="__main__": main()
