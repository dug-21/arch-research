# W0 — the effective serving envelope

**Captured 2026-08-04T03:06:56Z at run start**, not inherited from scope time. Raw responses:
`W0-envelope-raw.json`. This is the record `proven_by` cites; every W1–W7 result is proven *within* it,
and different hardware re-opens the claim to `partial` (methodology §4).

## Measured over HTTP — what the server itself reports

| Field | Value in force | Source |
|---|---|---|
| Ollama version | **0.32.5** | `/api/version` |
| Model | `qwen3-coder:30b` | `/api/ps` |
| Digest | `06c1097efce0431c2045fe7b2e5108366e43bee1b4603a7aded8f21689e90bca` | `/api/ps` |
| Quantization | **Q4_K_M** | `/api/ps` |
| Architecture | `qwen3moe` — 128 experts, **8 active**, 48 blocks, 30.53 B total params | `/api/show` |
| Attention | GQA, 32 heads / **4 KV heads** | `/api/show` |
| Applied `num_ctx` | **32768** | `/api/ps` |
| Model's native context | **262144** | `/api/show` |
| Resident size | **18.94 GiB** (20,331,909,610 B) | `/api/ps` |
| CPU spill | **none — `size_vram` == `size`, 100 % resident** | `/api/ps` |
| `keep_alive` | expires 2318-11-13 — effectively never | `/api/ps` |
| Capabilities | `completion`, **`tools`** (native tool-calling advertised) | `/api/show` |

**The 32768 is a configuration choice, not a hardware ceiling** — the model itself declares 262144. Anything
W5 says about capacity is bounded by `OLLAMA_CONTEXT_LENGTH`, which this run may not change (and which the
owner declined to push past at gate-1).

**100 % residency is the load-bearing line.** It means every number in this run is GPU/unified-memory
throughput with no CPU offload confound. Had `size_vram < size`, the throughput results would have been
measuring a hybrid path and would not have supported a clean claim.

## Owner-attested, NOT verified by us

The Ollama API exposes **no host hardware information**. These envelope fields come from the owner and are
recorded as attestation, not measurement:

- MacBook Pro **M4 Pro**, **48 GB** unified memory, **~273 GB/s** memory bandwidth.

This matters to the firewall. Our measurements are real and demonstrated by us; the *identity of the machine
they were taken on* is taken on trust. Any downstream claim of the form "an M4 Pro does X" inherits that
trust boundary. What we can state without it: "the machine serving `100.122.119.72:11434` on 2026-08-04 did
X." Bandwidth-model reasoning (W2, #67) depends on the 273 GB/s figure being right, so its verdict is
conditional on the attestation.

## Not capturable in this envelope

**Thermal and power state.** The scope asks for them; access is HTTP-only with no shell on the serving host,
and Ollama exposes neither. Recorded as **not measured** rather than guessed.

*Substitute (observable) proxy:* an identical drift probe run at run start and again at run end. Sustained
thermal throttling on a laptop shows up as decode-rate decay between the two. This detects throttling; it
does not measure temperature, and it cannot distinguish throttling from any other time-varying load on a
machine we do not control.

## Confounds carried forward

1. **Prefix KV caching is active and enormous** (see W1). Any throughput figure must state cold or warm.
   v1 of the measurement harness was discarded for conflating them.
2. **The serving host is a laptop in active use.** Other workloads on it are invisible to us.
3. **W2 will evict.** ~19 GB dense + 18.94 GiB MoE against 48 GB unified means the two arms cannot both stay
   resident; load time is reported separately from decode for exactly this reason.
