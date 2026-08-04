#!/usr/bin/env python3
"""W5 -- size_vram as a function of num_ctx, bounded at 32768 by gate-1.

Method: issue a 1-token request carrying options.num_ctx = N, which makes Ollama
instantiate the model at that context size, then read /api/ps for the resident
footprint actually in force. num_ctx is a per-REQUEST option -- no process
environment on the serving host is touched, which keeps this inside the scope's
"runtime configuration cannot be changed by the run" constraint.

Cost, stated plainly: each distinct num_ctx reloads the model, so this evicts and
re-loads the pinned instance several times. It is run late, and the final step
restores num_ctx=32768 so the envelope the other workstreams were measured under
is put back.
"""
import json, time, urllib.request, pathlib, argparse

HOST = "http://100.122.119.72:11434"


def post(path, payload, timeout=600):
    req = urllib.request.Request(HOST + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def get(path, timeout=60):
    with urllib.request.urlopen(HOST + path, timeout=timeout) as r:
        return json.loads(r.read())


def probe(model, num_ctx):
    t0 = time.perf_counter()
    resp = post("/api/chat", {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "stream": False,
        "options": {"num_ctx": num_ctx, "num_predict": 1, "temperature": 0},
    })
    load_s = round(time.perf_counter() - t0, 2)
    ps = get("/api/ps")
    m = next((x for x in ps["models"] if x["name"] == model), None)
    return {
        "num_ctx_requested": num_ctx,
        "num_ctx_in_force": (m or {}).get("context_length"),
        "size_bytes": (m or {}).get("size"),
        "size_vram_bytes": (m or {}).get("size_vram"),
        "size_gib": round((m or {}).get("size", 0) / 2**30, 2),
        "size_vram_gib": round((m or {}).get("size_vram", 0) / 2**30, 2),
        "fully_resident": (m or {}).get("size") == (m or {}).get("size_vram"),
        "server_load_duration_s": round(resp.get("load_duration", 0) / 1e9, 2),
        "wall_s": load_s,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3-coder:30b")
    ap.add_argument("--ctxs", default="2048,4096,8192,16384,24576,32768")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rows = []
    for n in [int(x) for x in a.ctxs.split(",")]:
        try:
            r = probe(a.model, n)
        except Exception as e:
            r = {"num_ctx_requested": n, "error": repr(e)}
        rows.append(r)
        print(json.dumps(r), flush=True)
        pathlib.Path(a.out).write_text(json.dumps(rows, indent=2))

    # restore the envelope the rest of the run was measured under
    if rows and rows[-1].get("num_ctx_requested") != 32768:
        print(json.dumps({"restore": probe(a.model, 32768)}), flush=True)
