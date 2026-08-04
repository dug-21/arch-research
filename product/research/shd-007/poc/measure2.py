#!/usr/bin/env python3
"""shd-007 measurement harness v2 -- cold/warm prefill separated.

v1 was contaminated: identical filler across reps let Ollama reuse the KV
prefix cache, so "prefill" reported 27k-33k tok/s -- a cache hit timed as if it
were compute. v2 controls the prefix explicitly.

  cold  -- a unique nonce at position 0 invalidates the whole prefix. This is
           true prefill compute: what you pay on first contact with context.
  warm  -- the identical prompt re-sent. This is what an agentic loop actually
           pays from turn 2 onward, when the harness re-sends its transcript.

Both are reported. Neither is "the" prefill number; the gap between them is the
result that matters.
"""
import json, sys, time, uuid, urllib.request, pathlib, argparse

HOST = "http://100.122.119.72:11434"
FILLER = pathlib.Path(
    "/workspaces/arch-research/product/research/shd-007/task/fixture/roster/parser.py"
).read_text()
QUESTION = "\n\nIn one short paragraph, describe what the parse() function does."


def build_prompt(target_tokens: int, nonce: str) -> str:
    need = int(target_tokens * 3.4)
    body = (FILLER + "\n\n# ---\n\n") * (need // len(FILLER) + 1)
    # nonce FIRST -- prefix caching matches on longest common prefix, so a
    # trailing nonce would not invalidate anything.
    return f"# session {nonce}\n" + body[:need] + QUESTION


def call(model, prompt, num_predict, timeout=1200):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "options": {"num_predict": num_predict, "temperature": 0},
    }
    req = urllib.request.Request(
        HOST + "/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.perf_counter()
    ttft, final = None, None
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
            if not raw.strip():
                continue
            ch = json.loads(raw)
            if ttft is None and ch.get("message", {}).get("content"):
                ttft = time.perf_counter() - t0
            if ch.get("done"):
                final = ch
    wall = time.perf_counter() - t0
    ns = 1e9
    pe_c, pe_d = final.get("prompt_eval_count", 0), final.get("prompt_eval_duration", 0) / ns
    ev_c, ev_d = final.get("eval_count", 0), final.get("eval_duration", 0) / ns
    return {
        "prompt_tokens": pe_c,
        "prefill_s": round(pe_d, 4),
        "prefill_tps": round(pe_c / pe_d, 1) if pe_d else None,
        "ttft_s": round(ttft, 3) if ttft else None,
        "decode_tokens": ev_c,
        "decode_s": round(ev_d, 3),
        "decode_tps": round(ev_c / ev_d, 2) if ev_d else None,
        "load_s": round(final.get("load_duration", 0) / ns, 3),
        "wall_s": round(wall, 3),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3-coder:30b")
    ap.add_argument("--depths", default="1000,4000,8000,16000,28000")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--num-predict", type=int, default=200)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rows = []
    for d in [int(x) for x in a.depths.split(",")]:
        for i in range(a.reps):
            nonce = uuid.uuid4().hex          # unique -> cold
            p = build_prompt(d, nonce)
            for kind in ("cold", "warm"):     # warm re-sends the SAME prompt
                try:
                    r = call(a.model, p, a.num_predict)
                except Exception as e:
                    r = {"error": repr(e)}
                r.update(model=a.model, target_tokens=d, rep=i, kind=kind,
                         utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
                rows.append(r)
                print(json.dumps(r), flush=True)
                pathlib.Path(a.out).write_text(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
