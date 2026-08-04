# shd-007 — REPORT

**Run:** shd-007 · Issue #55 · cycle `shd-007` · method stamp `wf-v0.21-1-gb18da7f`
**Envelope:** Ollama 0.32.5 · `qwen3-coder:30b` Q4_K_M (`06c1097efce0`) · applied `num_ctx` 32768 ·
MacBook Pro M4 Pro / 48 GB unified *(owner-attested — see W0)* · HTTP-only over Tailscale
**Date:** 2026-08-04

---

## Verdict in one paragraph

The local stack **does** serve a coding-grade agentic contract on this hardware. Over 107 sequential
tool calls across six runs and two serving protocols there were **zero** protocol failures, and the
held-out multi-file coding task was driven to a **passing, verified diff in 4 of 6 runs**. The binding
constraint is not decode speed, which stays workable at agentic depth — it is **cold prefill**, which
reaches **131 seconds** at 26k tokens and is invisible to `done_when` as currently written. Prefix KV
caching removes that cost almost entirely (**16.3 s → 0.32 s TTFT** at 7.4k), which makes cache-preserving
context handling a *harness requirement*, not an optimisation. On the harness axis the result is worse:
**no slate harness completed the task**. aider reached 7/8 before hitting its own reflection cap; Claude
Code over local `/v1/messages` failed outright, and the cause is isolated to **its system prompt**, not
the serving stack. The dense arm ran: position #67's bandwidth model is **calibrated** — it predicted
10–12 tok/s for a 32B dense here and we measured **11.61** — but its *dense-first stack conclusion does not
transfer*, because the MoE beats #67's own reported 3090-dense figure by 2× on a machine with 3.4× less
bandwidth.

---

## W0 — the effective envelope

Full record: `artifacts/W0-ENVELOPE.md`. Re-captured at run start, not inherited.

100 % resident (`size_vram == size`), so every number here is unified-memory throughput with **no CPU
offload confound**. MoE confirmed: 128 experts, 8 active, 48 blocks, GQA 32:4. Applied context 32768
against a **native 262144** — the ceiling is configuration, not hardware.

**Trust boundary:** the Ollama API exposes no host hardware. "M4 Pro / 48 GB / ~273 GB/s" is
**owner-attested, not measured by us**. Our measurements are real; the identity of the machine is taken on
trust, and the W2 bandwidth verdict is conditional on it. **Thermal/power state was not capturable** and is
recorded as not measured rather than guessed.

## W1 — throughput at agentic depth

Raw: `artifacts/W1-throughput-moe.json`. 3 reps/cell; cold-prefill variance ≤ 0.05 %.

| prompt tok | cold prefill | cold prefill tok/s | cold TTFT | warm prefill | warm TTFT | decode tok/s |
|---|---|---|---|---|---|---|
| 980 | 1.26 s | 775 | 1.49 s | 0.027 s | 0.24 s | **60.4** |
| 3,722 | 6.20 s | 601 | 6.46 s | 0.032 s | 0.28 s | 50.0 |
| 7,388 | 16.57 s | 446 | 16.86 s | 0.038 s | 0.30 s | 42.4 |
| 14,725 | 48.67 s | 303 | 49.11 s | 0.041 s | 0.37 s | 32.0 |
| 25,740 | **130.77 s** | 197 | **131.37 s** | 0.055 s | **0.46 s** | **24.0** |

Three results:

1. **Cold prefill is superlinear** — 26× the tokens costs 104× the time. That is attention cost, not
   memory bandwidth.
2. **Warm prefill is effectively flat** — 0.027 → 0.055 s across the whole range, a **2,366×** speedup at
   26k. TTFT stays under half a second at every depth.
3. **Decode degrades 60 %** with depth (60.4 → 24.0 tok/s). This *is* the bandwidth effect position #67
   predicted, but it arrives through **growing KV-cache reads**, not weight reads — a mechanism #67 did
   not separate.

**A methodological note that is itself a result.** The first version of this harness was **discarded**.
It reused identical filler across reps, so Ollama served a cached prefix and "prefill" reported
27,000–33,000 tok/s — a cache hit timed as if it were compute. Had it been believed, this report would
have claimed prefill was free. v2 separates cold (unique nonce at position 0) from warm (prompt re-sent).

## W3 — the protocol contract, and W4 — the held-out task

Raw: `artifacts/W3-*.json`. Task spec and fixture frozen **before** the first arm: `task/TASK.md`.

| route | rep 1 | rep 2 | rep 3 | completion |
|---|---|---|---|---|
| `/v1/chat/completions` | ✗ (30 steps) | ✓ (11) | ✓ (11) | 2/3 |
| `/v1/messages` | ✓ (14) | ✗ (30) | ✓ (11) | 2/3 |

- **Protocol failures: 0 out of 107 sequential tool calls.** No malformed arguments, no unknown tools, no
  dropped streams, no truncation, on either route. **Finding #16 is contradicted at the protocol level in
  this envelope.**
- **Completion: 4/6 (67 %).** Successful runs took 11–14 tool calls and 54–73 s wall. Every failure is the
  same mode: three of four defects fixed fast, then thrash on the fourth until the step cap — including
  stretches of `run_tests` with no intervening edit.
- Passing runs produce a **real diff**: `int(end)-1 → int(end)`, case-folded name grouping with a canonical
  spelling, and a `min()` tie-break. `tests/` verified pristine mechanically, so the reward-hacking check
  holds.

**Repeats earned their cost.** At n=1 the routes read "Anthropic completes, OpenAI does not." At n=3 each
they are **identical at 2/3**. Reporting the n=1 result would have put a false protocol finding into the
graph.

## W5 — memory/context curve *(bounded at 32768 by gate-1)*

| num_ctx | 2,048 | 4,096 | 8,192 | 16,384 | 24,576 | 32,768 |
|---|---|---|---|---|---|---|
| VRAM (GiB) | 17.30 | 17.40 | 17.60 | 18.01 | 18.42 | 18.82 |

Fully resident at every point. Slope **50.6 KiB/token**, against a GQA prediction of 48 KiB
(4 KV heads × 64 dim × 48 layers × 2 × 2 B) — agreement to ~5 %, which **confirms an unquantized f16 KV
cache**. Base weights ≈ 17.2 GiB. The envelope was restored to 32768 afterwards.

**The capacity boundary was not measured.** The owner declined to push a laptop in active use to failure.
Scope output #6 is withdrawn, not downgraded.

## W7 — the harness slate *(merged shd-003 P3)*

| harness | result | where it stopped |
|---|---|---|
| **aider 0.86.2** (#11), single-pass | 6/8 | never runs tests without `--auto-test`; one edit round then exit |
| **aider, `--auto-test`** (#11) | **7/8** | its own `Only 3 reflections allowed` cap. 4 LLM turns, 13 edits, context 1.7k→9.0k, `tests/` pristine, no protocol errors |
| **Claude Code 2.1.221 + local `/v1/messages`** (#12, T3a) | **total failure** | model returns native tool syntax as **text**; harness sees no `tool_use`, executes nothing, exits with the fixture untouched |
| **Continue** (#13) | **not run — parked** | no headless driver; was already gated on the #6677 metadata gate |

### The Claude Code failure, isolated

Captured on the wire through a logging proxy (`artifacts/W7-claudecode-wire-capture.json`) and bisected:

| variant | input tok | structured tool call? |
|---|---|---|
| verbatim replay | 19,230 | ✗ |
| minus `thinking` / `output_config` / `context_management` | 19,230 | ✗ |
| also `max_tokens` 32000 → 4096 | 19,230 | ✗ |
| **also plain system prompt** | 17,662 | **✓** |
| CC system prompt, **one** tool | **3,609** | ✗ |

**Ruled out by direct test:** tool count, prompt size, nested schemas, `system`-as-array, `cache_control`,
streaming, `max_tokens`. A synthetic request matching Claude Code's *shape* at 21,970 tokens streams
structured `tool_use` correctly.

**The trigger is the content of Claude Code's system prompt**, which specifies a tool-calling convention
that overrides the chat template's, so the model emits `<function=…>` as prose and Ollama never sees a
tool call to parse. **#16 is confirmed for this harness — but the mechanism is prompt-level, not
protocol-level.** That distinction matters: the serving stack is not at fault, and it parses tool calls
correctly for aider and for our own loop. A fix lives in prompt/template alignment, not in the proxy.

## W2 — dense/MoE calibration arm  *(run; human-approved pull)*

Raw: `artifacts/W2-throughput-dense.json`. `qwen2.5-coder:32b` Q4_K_M, 32.76 B dense, GQA 40:8, 64 layers.
2 reps/cell (MoE variance was ≤0.05 %, so 2 suffices, and it limits eviction churn on the owner's laptop).

**The MoE was evicted to load the dense model**, exactly as the gate-1 confound note predicted. During the
load `/api/ps` read **empty** — the same signature wfh-005 #196 warns about, here a benign load window
rather than a broken control. Resident dense footprint: 22.54 GiB at `num_ctx` 32768.

| depth (tok) | MoE decode | dense decode | **MoE advantage** | MoE cold prefill | dense cold prefill |
|---|---|---|---|---|---|
| 1,001 | 60.4 | **11.61** | **5.2×** | 775 tok/s | 100 tok/s |
| 3,744 | 50.0 | 10.75 | 4.6× | 601 | 90 |
| 7,406 | 42.4 | 10.02 | 4.2× | 446 | 82 |
| 14,746 | 32.0 | 8.61 | 3.7× | 303 | 69 |
| 25,761 | 24.0 | 7.44 | 3.2× | 197 | 57 |

Dense cold TTFT at 25,761 tokens: **452.6 s — seven and a half minutes to first token.** Warm: 0.57 s.

### Verdict on #67's bandwidth model: **CALIBRATED**

1. **Its numeric prediction was right.** #67's model implies a 32B dense lands **10–12 tok/s** on a
   ~273 GB/s machine. **Measured: 11.61.**
2. **One constant explains both arms.** Dense decode × full weights = 11.61 × 18.49 GiB ⇒ **230 GB/s
   effective**, i.e. **84 % of the attested 273 GB/s** — the signature of a bandwidth-bound decode. Holding
   that same 230 GB/s, the MoE's 60.4 tok/s implies **3.81 GB read per token = 21 % of its weights**,
   consistent with 8-of-128 experts plus shared layers. The model predicts *both* arms without adjustment.
3. **Direction check against #67's own citation.** Scaling our dense figure by the 936/273 bandwidth ratio
   gives **39.8 tok/s** for a 3090 — same order as #67's `[REPORTED]` ~30. The thesis "bandwidth, not
   capacity, sets dense decode" **survives contact with measurement.**

### …but its *stack conclusion* does not transfer to this hardware class

#67 treats Qwen3-Coder-30B-A3B as "the agentic / long-context **alternative**" and concludes a used 3090 is
the value floor because unified-memory machines "decode dense models SLOWER than the cheap card." Both
halves are true **for dense models** and misleading here:

> **Our MoE on ~273 GB/s delivers 60.4 tok/s — 2.0× #67's `[REPORTED]` ~30 tok/s for a 3090 running 32B
> dense.** A 3.4× bandwidth deficit is not merely recovered by the MoE; it is overturned.

**Architecture is a bigger lever than bandwidth on this hardware.** MoE-vs-dense moved decode 5.2×; the
3090's bandwidth edge is 3.4×. On low-bandwidth unified memory the MoE is not an alternative — it is the
determining choice, and #67's dense-first ordering (protocol fit → tool-call reliability → bandwidth × VRAM)
should gain **model architecture** as a first-class term above raw bandwidth.

**Two honesty bounds on this comparison.** #67's 3090 figure is `[REPORTED]`, so this is our measurement
against their citation — **not a head-to-head**; we do not own a 3090. And the 273 GB/s denominator is
**owner-attested**, so the 84 %-of-bandwidth result is conditional on it. The *ratio* between our two arms
(5.2×) is measured on identical hardware and depends on neither.

### A second-order result worth keeping

Dense decode degrades **less** with depth (−36 %) than the MoE (−60 %), despite dense KV costing ~5× more
per token (256 KiB vs 50.6 KiB). Both are consistent: KV reads are a *small fraction* of the dense model's
18.49 GiB per-token read but a *large fraction* of the MoE's 3.81 GB. The MoE's advantage therefore
**narrows with context** — 5.2× at 1k down to 3.2× at 26k. Extrapolating the trend is not supported by five
points, but the direction matters for long-context agentic work and is a candidate for a follow-on scope.

---

## Proposed bound for C1's `done_when` X  *(advisory — human's call)*

C1 currently reads *"serves a coding-grade completion for task P at ≥X tok/s."* This run fixed P and
measured X, and in doing so found that **`done_when` is measuring the wrong axis**.

Decode was never the binding constraint. Runs that completed did so at **42–50 tok/s**, ~4–5 s per tool
call — comfortable. What actually threatens usability is **time to first token on a cold context: 131 s at
26k**. A stack could pass "≥20 tok/s" and still be unusable if every turn paid cold prefill.

**Proposed:** *"serves task P to a passing diff in ≥N of M attempts, sustaining ≥20 tok/s decode **and
≤2 s TTFT** at a stated context depth of ≥16k."* Measured here: 32 tok/s and 0.37 s warm TTFT at 14.7k —
clears it. The additions that carry the lesson are **TTFT**, **the stated depth**, and **a success rate
rather than a single attempt** (67 % observed; reliability is multiplicative, and one lucky run is not a
capability).

## Sizing note — `claimed`, never `proven`

Measured **here**, on this machine, at this envelope. Everything below is inference from **one point**:

- KV cache costs **50.6 KiB/token** at f16 with this architecture. Extrapolated, 262k native context would
  need ~12.6 GiB of KV on top of ~17.2 GiB of weights — **~30 GiB, which would fit 48 GB**. Not measured;
  the owner capped the sweep at 32768.
- A machine with less unified memory than ~24 GB could not hold this model at useful depth.
- **Effective memory bandwidth measured 230 GB/s** (dense decode × weights), 84 % of the attested 273. That
  constant predicts both arms, so it is the right number to reason with — for **this** machine.
- **Architecture beats bandwidth on this hardware class.** MoE-vs-dense is worth 5.2× at shallow depth;
  the 3090's bandwidth edge is 3.4×. A sizing decision that optimises bandwidth while ignoring model
  architecture optimises the smaller term.
- **Nothing here sizes a machine we do not own.** The 3090 comparison is our measurement against #67's
  `[REPORTED]` figure, not a head-to-head, and the whole bandwidth-efficiency result is conditional on the
  owner-attested 273 GB/s.
- **The serving host was left as found** — MoE reloaded, 18.94 GiB, `num_ctx` 32768, never-expire pin
  restored, matching the W0 opening capture. The dense model remains pulled (~18.5 GiB of the owner's disk),
  which is a durable side effect of the approved W2 and is the owner's to reclaim.

## Recommended firewall grades  *(advisory — the gate is the human's)*

- **C1 (#4) → `proven`, within this envelope.** All three clauses are met by attached artifacts: the stack
  serves the C2-slate endpoint (aider drives it end-to-end); sustained decode is measured with its depth
  (24.0 tok/s @ 25.7k, 42.4 @ 7.4k); and a **passing** multi-file diff was produced through 11–14
  sequential tool calls against the real proxy, verified green with `tests/` pristine. Different hardware
  re-opens this to `partial`.
- **C2 (#5) → `partial`, not `proven`.** The bar is a **slate** harness finishing with no manual steps.
  None did. aider reached 7/8 unaided and stopped on its own cap; Claude Code failed at the tool-call
  contract. Our bespoke loop completed 4/6 — evidence the *task and stack* are viable, but it is not a
  slate harness and must not be counted toward C2.
- **Finding #16 → amended, not simply confirmed.** Confirmed for Claude Code; contradicted at the protocol
  level (0/107 failures). The mechanism is prompt-level.

## Lessons learned *(first real exercise of the firewall machinery)*

1. **A control that is present, believed and inert passes every test a real one passes** (wfh-005 #196,
   met again). Prefix caching made prefill look 400× faster than it is. The tell was physical
   implausibility — 27,000 tok/s on a ~273 GB/s machine — not anything the harness reported.
2. **n=1 completion claims are worthless.** The routes looked different at n=1 and identical at n=3.
3. **Freeze the task before the first arm, and check the reward hack mechanically.** `verify.sh` self-tests
   on green / red / tests-edited; a transcript reading is not evidence.
4. **"Harness fails" is not a finding; the mechanism is.** Bisecting to the system prompt turned an
   unusable "#16 confirmed" into an actionable, fixable diagnosis.
5. **Distinguish a harness's own caps from the model's limits.** aider stopped at 7/8 because of its
   3-reflection default, not because the model could not continue.
6. **Ask before spending someone's hardware, then record what the answer cost.** The W5 cap was the owner's
   call; the consequence is a withdrawn output, stated as withdrawn.
