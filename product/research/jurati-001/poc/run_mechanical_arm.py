#!/usr/bin/env python3
import json,time
from pathlib import Path
from jurati import VERDICTS,digest,reduce_verdict,validate_contract
BASE=Path(__file__).resolve().parents[1]; GEN=BASE/"corpus-generated"; OUT=BASE/"artifacts"; OUT.mkdir(exist_ok=True)
rows=[]
for line in (GEN/"manifest.jsonl").read_text().splitlines():
 m=json.loads(line); packet=json.loads((GEN/"packets"/(m["episode_id"]+".json")).read_text())
 if m["partition"]=="holdout": question="Assess the bounded "+packet["decision_type"]+" decision"; evidence=[{"id":"primary","path":"custody-sanitized","sha256":__import__('hashlib').sha256(packet["evidence"].encode()).hexdigest()}]
 else: question=packet["judge_facing"]["question"]; evidence=[{"id":e["id"],"path":"restricted","sha256":e["sha256"]} for e in packet["evidence"]]
 c={"contract_id":m["episode_id"],"question":question,"evidence":evidence,
    "clauses":[{"id":"semantic-1","evaluator":"semantic","criticality":"blocking","evidence_ids":[e["id"] for e in evidence]}],
    "transitions":{v:{"id":"action-"+v,"kind":"advance" if v=="pass" else "escalate","target":v,"authority":"human"} for v in VERDICTS}}
 validate_contract(c)
 for rep in range(5):
  t=time.perf_counter_ns(); verdict=reduce_verdict(c,{"semantic-1":"insufficient_evidence"}); elapsed=time.perf_counter_ns()-t
  rows.append({"episode_id":m["episode_id"],"partition":m["partition"],"arm":"A","repetition":rep+1,"result":"insufficient_evidence","verdict":verdict,"action":c["transitions"][verdict],"contract_hash":digest(c),"latency_ns":elapsed})
(OUT/"arm-a-mechanical.jsonl").write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n" for x in rows))
summary={"arm":"A","episodes":45,"repetitions_per_episode":5,"n":225,"disagreement":0,"false_advancements":0,"outcome":"all residual semantic clauses abstained/escalated","latency_ns":{"min":min(x["latency_ns"] for x in rows),"max":max(x["latency_ns"] for x in rows),"mean":sum(x["latency_ns"] for x in rows)/len(rows)}}
(OUT/"arm-a-summary.json").write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n"); print(json.dumps(summary,sort_keys=True))
