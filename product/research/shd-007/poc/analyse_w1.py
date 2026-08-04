#!/usr/bin/env python3
"""Render the W1 throughput table from the raw sweep, cold and warm kept apart."""
import json, statistics as st, sys, pathlib

rows = json.loads(pathlib.Path(sys.argv[1]).read_text())
rows = [r for r in rows if "error" not in r]

by = {}
for r in rows:
    by.setdefault((r["target_tokens"], r["kind"]), []).append(r)

def agg(rs, k):
    v = [r[k] for r in rs if r.get(k) is not None]
    return (st.mean(v), (max(v) - min(v)) / 2 if len(v) > 1 else 0.0) if v else (None, None)

depths = sorted({d for d, _ in by})
print(f"model: {rows[0]['model']}   reps/cell: {len(by[(depths[0],'cold')])}\n")
hdr = ("| prompt tok | cold prefill s | cold prefill tok/s | cold TTFT s "
       "| warm prefill s | warm TTFT s | decode tok/s | decode drop vs shallowest |")
print(hdr); print("|" + "---|" * 8)

base = None
for d in depths:
    c, w = by[(d, "cold")], by[(d, "warm")]
    ptok = round(st.mean([r["prompt_tokens"] for r in c]))
    cps, _ = agg(c, "prefill_s"); ctps, _ = agg(c, "prefill_tps"); cttft, _ = agg(c, "ttft_s")
    wps, _ = agg(w, "prefill_s"); wttft, _ = agg(w, "ttft_s")
    dtps, dsd = agg(c + w, "decode_tps")
    if base is None: base = dtps
    print(f"| {ptok} | {cps:.2f} | {ctps:.0f} | {cttft:.2f} | {wps:.3f} | {wttft:.2f} "
          f"| {dtps:.1f} ±{dsd:.1f} | {(dtps/base-1)*100:+.0f}% |")

print("\nspeedups (warm vs cold):")
for d in depths:
    c, w = by[(d, "cold")], by[(d, "warm")]
    cs, _ = agg(c, "prefill_s"); ws, _ = agg(w, "prefill_s")
    ct, _ = agg(c, "ttft_s"); wt, _ = agg(w, "ttft_s")
    ptok = round(st.mean([r["prompt_tokens"] for r in c]))
    print(f"  {ptok:6d} tok: prefill {cs/ws:8.0f}x   TTFT {ct/wt:6.1f}x  ({ct:.1f}s -> {wt:.2f}s)")
