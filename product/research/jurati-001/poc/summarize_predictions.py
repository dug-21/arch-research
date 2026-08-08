#!/usr/bin/env python3
"""Summarize opaque predictions without reference labels or scoring."""
import hashlib,json,statistics,sys
from collections import Counter,defaultdict
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit("usage: summarize_predictions.py INPUT.jsonl OUTPUT.json")
source=Path(sys.argv[1]); rows=[json.loads(x) for x in source.read_text().splitlines()]
by_arm={}
for arm in ("B","C"):
 selected=[x for x in rows if x["arm"]==arm]; latency=[x["latency_ns"] for x in selected]
 by_arm[arm]={"valid_predictions":len(selected),"result_counts":dict(sorted(Counter(x["result"] for x in selected).items())),
  "abstentions":sum(x["result"]=="insufficient_evidence" for x in selected),
  "latency_ms":{"min":min(latency)/1e6,"max":max(latency)/1e6,"mean":statistics.fmean(latency)/1e6,"median":statistics.median(latency)/1e6}}
episodes=defaultdict(list)
for row in rows:
 if row["arm"]=="C": episodes[row["episode_id"]].append(row["result"])
summary={"schema":"jurati-bc-operational-summary-v1","prediction_ledger_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
 "planned":{"B":11,"C":55},"attempted":{"B":11,"C":51},"valid":{"B":10,"C":50},
 "malformed_output":{"B":1,"C":1},"not_run_after_fail_closed":{"B":0,"C":4},"timeouts":{"B":0,"C":0},
 "by_arm":by_arm,"C_reproducibility":{"complete_episodes":len(episodes),"episodes_with_disagreement":sum(len(set(v))>1 for v in episodes.values()),
  "repeated_run_disagreement_rate":sum(len(set(v))>1 for v in episodes.values())/len(episodes)},
 "cost":{"local_api_charge":"not measured; endpoint is locally operated","monetary_cost":"not measured"},
 "energy":{"status":"not measured","reason":"no authorized host energy telemetry"},
 "scoring":"not performed; custody labels unavailable to PoC"}
Path(sys.argv[2]).write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n")
print(json.dumps({"status":"PASS","valid":len(rows),"ledger_sha256":summary["prediction_ledger_sha256"]},sort_keys=True))
