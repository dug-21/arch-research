#!/usr/bin/env python3
import hashlib,json,platform,subprocess,time,urllib.request
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]; OUT=BASE/"artifacts"; OUT.mkdir(exist_ok=True)
def get(url):
 t=time.perf_counter_ns()
 with urllib.request.urlopen(url,timeout=5) as r: body=r.read()
 return json.loads(body), (time.perf_counter_ns()-t)/1e6
version,vms=get("http://100.122.119.72:11434/api/version"); tags,tms=get("http://100.122.119.72:11434/api/tags")
allowed={"qwen2.5-coder:32b","qwen3-coder:30b"}
models=[{k:m[k] for k in ("name","digest","size","modified_at")} for m in tags["models"] if m["name"] in allowed]
record={"captured_at_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"python":platform.python_version(),"platform":platform.platform(),
 "ollama":{"endpoint":"http://100.122.119.72:11434","version":version.get("version"),"version_probe_ms":vms,"tags_probe_ms":tms,"models":models,
 "authorization":"existing listed models only; no pulls, evictions, or host configuration","residency":"not measured","host_hardware":"not measured"},
 "frontier":{"status":"blocked","reason":"no configured provider/model snapshot or ordinary task credential discovered"},
 "human_arm":{"status":"blocked","reason":"two raters and adjudicator not assigned"}}
(OUT/"effective-envelope.json").write_text(json.dumps(record,sort_keys=True,indent=2)+"\n")
print(json.dumps({"status":"captured","models":len(models)},sort_keys=True))
