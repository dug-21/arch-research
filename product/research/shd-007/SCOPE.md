# shd-007 — Validated POC: local inference on owned hardware, and the first measured anchor for sizing

**Status:** RUNNING (gate-1 scope approved 2026-08-04 — see *Gate-1 decisions* below)
**Goal(s):** `shd` (primary, #3)
**Capability target(s):** **C1 — Capable LLM inference runs on local hardware** (#4) ·
**C2 — An agentic harness drives research+coding tasks to completion** (#5, merged from shd-003 at gate-1).
**Graded independently** — a C2 failure must not drag C1, nor the reverse.
**Confidence-required:** **validated** (spends real compute; moves status on a demonstrated-by-us artifact)
**Phase / area:** inference / feasibility
**Cycle topic / Issue:** shd-007

Governing NFRs (via `About→ C1`): N1 owned-HW/budget (#7) · N2 no-outage (#8) · N4 multi-machine-ready (#10, tie-breaker only — D11) · #98 observability/audit.

Discharges the validated follow-on specified in position **#67** (shd-004 synthesis), which named itself
"shd-005" — an id since consumed by the C3 routing landscape. This scope carries that bar under a new id.

---

## The question

This scope answers **two** questions with one hardware window, and they must not be conflated:

1. **The proof (C1's actual bar).** Does local inference serve a coding-grade agentic contract on owned
   hardware — demonstrated by us? This is what moves status.
2. **The anchor (why we widen while the hardware is free).** Position #67 ranked six engines, five models,
   five quants and four hardware tiers, and flagged every figure `[REPORTED] — NOTHING proven by us`. One
   properly-measured machine converts that landscape from documentation into something calibrated.

> Does the local stack serve a coding-grade agentic contract on owned hardware — and what does measuring
> it tell us about the hardware the development environment actually needs?

**A single machine cannot establish hardware requirements.** It establishes one measured point and a
calibration for the model used to reason about the rest. That distinction is load-bearing and is enforced
in the proof bar below.

## Why it matters

C1 (#4) is `missing` and is the `Prerequisite` for C2 (#5) — every downstream shd scope stands on it.
The hardware is free and available now, which makes this the cheapest proof on the board.

Beyond the subject axis, this is the **first artifact-producing run the garage has ever attempted** — all
five prior runs were directional. It is the first exercise of the feasibility/firewall machinery, and the
only thing that moves factory capability **#28 (prove-with-artifact)** off `claimed`.

## Known constraints & prior art  *(build on these — do not re-derive)*

- **Position #67** — the ranked direction and the `done_when` template this scope instantiates.
  Determining constraints, in its order: (1) serving-protocol fit — *necessary, disqualifying*;
  (2) tool-call/streaming reliability — *necessary but unproven*; (3) memory-bandwidth × VRAM.
  Its central claim — **bandwidth, not capacity, sets dense decode** — is the thing W2 calibrates.
- **Mechanism finding #16** — native-tool-call harnesses break on the local proxy/model contract. The
  test must **exercise** that contract, not avoid it.
- **Methodology §12 L1** — harness viability needs a live tool-call smoke, never doc-reading.
- **Reliability is multiplicative** — 95%/call ≈ 66% over 8 steps. Measure **completion**, not per-call.
- **Technologies already on the shelf** (reuse, do not re-research): #45 Qwen3-Coder-30B-A3B ·
  #40 Ollama · #49 GGUF k-quants · #44 Qwen2.5-Coder-32B (dense arm) · #42 MLX-LM (unused).
- **C1's `done_when` is currently unclosable as written** — *"serves a coding-grade completion for task P
  at ≥X tok/s"* leaves both P and X unbound. This scope **fixes P** (a held-out task, set before the first
  arm) and **measures X**. Proposing a bound threshold is a synthesis output (see below).

### Envelope deviations from #67 — reconciled, not overwritten (D3)  ·  *owner-accepted 2026-08-04*

| | #67 (2026-06-26, `[REPORTED]`) | shd-007 (actual) | Why |
|---|---|---|---|
| Hardware Y | used RTX 3090, 24 GB, ~936 GB/s | **MacBook Pro M4 Pro, 48 GB unified, ~273 GB/s** | the owned machine |
| Model X | Qwen2.5-Coder-32B **dense** | **Qwen3-Coder-30B-A3B (MoE, ~3B active)** | #67's own bandwidth finding predicts a 32B dense lands ~10–12 tok/s here, below its stated agentic floor. **A prediction under test (W2), not a settled result.** |
| Engine E | llama.cpp | **Ollama 0.32.5** | #67's constraint #1 is protocol fit; Ollama serves OpenAI `/v1/chat/completions` **and** a native Anthropic `/v1/messages` — both verified live, so the T3a leg needs no shim |
| Quant Q | Q4_K_M / Q5_K_M | **Q4_K_M** (18.6 GB on disk, 20.3 GB resident at 32k ctx) | as specified; 48 GB leaves KV headroom |
| Floor Z | *"the usable floor the POC MEASURES"* | **measured, not asserted** | unchanged — #67 is explicit that Z is an output |

### Gate-1 decisions — human, 2026-08-04  *(reconciled, not overwritten — D3)*

| Question put to the gate | Decision | Consequence carried into the run |
|---|---|---|
| **W2 dense arm** — approve `ollama pull qwen2.5-coder:32b` (~19 GB disk, eviction churn against the pinned 30B)? | **Approved — run W2.** | #67's bandwidth model gets checked, not restated. **Load/eviction churn is a recorded confound:** ~40 GB of models against 48 GB unified means Ollama will evict and reload between arms, so "identical hardware isolates the one variable" holds for the hardware but *not* for the working set. Report load time separately from decode. |
| **W5 ceiling** — how far to push `num_ctx` toward failure on a laptop in active use? | **Stay at or below 32768.** | **Expected output #6 is no longer obtainable.** W5 yields a `size_vram` × `num_ctx` *slope* within the configured envelope, **not** the capacity boundary. Any "next machine" number derived from it is an extrapolation and stays `claimed`. Note 32768 is a *configuration* limit (`OLLAMA_CONTEXT_LENGTH`), not a hardware one — the model's native context is 262144. |
| **shd-003 merge** — one hardware window, real overlap? | **Merged in.** | C2 (#5) becomes a second capability target. shd-003's **P1** is discharged by W0 and its **P2** by W4; its **P3** enters here as **W7**. Two proof bars behind one gate — graded independently. shd-003 is closed as *superseded by shd-007*, not as done. |

**Executability of the merge, verified 2026-08-04** (shd-003's staging note said the harnesses were absent):
PyPI + npm egress reachable from the devcontainer; `uv` 0.12.1 / `pipx` 1.16.5 present → aider installable.
Claude Code 2.1.221 present → the T3a arm needs no install. **Continue (#13) has no headless driver** and was
already gated on the #6677 metadata gate — it is **parked**, not run, unless both prior harnesses fail.

### Operational constraints (this envelope)

- **Access is HTTP-only, over Tailscale ACL to `100.122.119.72:11434`.** No shell on the serving host.
- **Runtime configuration cannot be changed by the run.** `OLLAMA_CONTEXT_LENGTH`, `OLLAMA_KEEP_ALIVE`,
  flash-attention and KV-cache type are process environment on the Mac. Any change needed mid-run is a
  **HARD STOP → hand back to the human**, recorded with the reason. Do not work around it.
- **Model inventory is reachable but human-gated by decision.** `/api/pull` and `keep_alive` are exposed
  on 11434 and would work. A pull or eviction spends the human's disk and working set: **stop and ask.**
  Reachability is not authorisation.
- **The serving host is a laptop.** Thermal throttling and power state are confounds; record them.

## Bounded investigation (the POC)

- **W0 — Effective-envelope capture.** Record the configuration **in force**, never the declared one:
  model digest, applied `num_ctx`, residency, `size_vram`, KV type, power/thermal state. *Output:* the
  envelope record `proven_by` will cite. **Re-capture at run start — do not inherit the scope-time
  reading.** *(wfh-005 #196: a control that is present, believed and inert passes every test a real one
  passes. At scope time `/api/ps` read empty three times while the config was in fact correct.)*
- **W1 — Throughput curve at agentic depth.** Decode tok/s **and prefill/TTFT** across ≥3 context depths
  spanning realistic agentic load (not 512-token toys). Prefill is the weak axis on Apple silicon and
  agentic harnesses re-send long context on every call. *Output:* a throughput table, depth × metric.
- **W2 — The dense/MoE calibration arm** *(load-bearing; requires a human-approved pull of #44).* Same
  task, same depths, dense Qwen2.5-Coder-32B. Identical hardware isolates the one variable, which is what
  makes #67's bandwidth model checkable rather than assumed. *Output:* a paired comparison and a verdict
  on the bandwidth model — or an explicit "not run" with the reason.
- **W3 — Protocol contract under sequential load.** Drive **both** `/v1/chat/completions` and
  `/v1/messages` through **≥6–8 sequential tool calls**. Record *where* the contract breaks (malformed
  call, dropped stream, silent truncation), not merely whether. *Output:* per-route transcript + failure
  taxonomy. **This is where #16 predicts failure.**
- **W4 — The held-out coding task.** One fixed multi-file task requiring the same ≥6–8 sequential tool
  calls and producing a **diff that passes its own test**. Fixed before the first arm, unchanged between
  arms. *Output:* task spec + resulting diff + pass/fail.
- **W5 — Memory/context curve** *(bounded at gate-1)*. `size_vram` as a function of `num_ctx`, **up to but
  never exceeding 32768** — the `OLLAMA_CONTEXT_LENGTH` in force. Pushing to failure was **declined** by the
  owner: the serving host is a laptop in active use. *Output:* the `size_vram` × `num_ctx` slope **within the
  configured envelope**. **Not** a capacity boundary — the run states the boundary as unmeasured.
- **W7 — Harness slate smoke** *(merged from shd-003 P3; grades C2, not C1)*. Drive the **W4 task** to
  completion through the shd-002 slate in position-#17 order: **aider** (#11) → **Claude Code + local
  `/v1/messages`** (#12, T3a) → **Continue** (#13, parked — no headless driver). Measure **completion with no
  manual steps**, not per-call success (reliability is multiplicative). *Output:* per-harness transcript +
  completion verdict. **W3 tests the contract raw; W7 tests whether a harness survives it.**
- **W6 — Record proof.** Curator attaches artifacts and sets grades **for C1 and C2 separately**. Envelope
  recorded in `proven_by` (§4: proven **within an envelope**; different hardware re-opens it to `partial`).

## Expected output

1. The **effective**-envelope record (W0).
2. Throughput curve — decode and prefill, across depths, both model arms (W1, W2).
3. Verdict on #67's bandwidth model: calibrated, or contradicted (W2).
4. Per-route tool-call transcripts + failure taxonomy (W3).
5. The task diff and its pass/fail result (W4).
6. ~~The memory/context capacity boundary (W5).~~ **Withdrawn at gate-1** — replaced by the `size_vram` ×
   `num_ctx` slope to 32768, plus an explicit statement that the boundary was **not measured** and why.
6b. Per-harness completion verdict + transcripts, and the first C2 technology graded (W7).
7. **A proposed bound for C1's `done_when` X** — derived from what the harness actually needed, not from
   the community heuristic. Advisory to the human; sharpening `done_when` is in-envelope structure (D3).
8. **A sizing note for the development environment** — explicitly `claimed`, never `proven` (see below).
9. `lesson-learned` entries: this is the firewall's first real exercise, so how the machinery behaves is
   a first-class output.

## Proof bar  *(validated — what moves status; demonstrated by us)*

**C1 (#4) → `proven`** requires **all** of: the stack serves the C2-slate endpoint; sustained decode at a
measured floor **stated with its context depth**; and a **passing** multi-file coding diff produced through
≥6–8 sequential tool calls against the real proxy. Artifacts in `proven_by` with the full envelope
(M4 Pro / 48 GB / Ollama 0.32.5 / qwen3-coder:30b Q4_K_M / applied `num_ctx`).

**C2 (#5) → `proven`** *(merged in at gate-1)* requires: a harness from the #17 slate finishes the **W4 task
with no manual steps** on the local backend, demonstrated by us, with the **transcript** attached in
`proven_by` under the same envelope. Partial completion (task advanced but needed human rescue) → `partial`,
with the rescue point recorded. **C1 and C2 are graded on separate evidence** — a serving stack that meets
C1's floor while every harness fails W7 yields `C1 proven / C2 missing`, and that is a legitimate outcome,
not a run failure.

**The sizing output is NOT proof, and the firewall applies to it unchanged.** Measurements on this machine
are proven for *this machine*. Every statement about hardware we do not own — "a 3090 would do X", "you
need Y GB for Z" — is an **extrapolation from one point** and stays `claimed` however well the model fits.
Say "measured here, inferred there," and never merge the two in one sentence.

**Partial and negative outcomes are first-class and must not be rounded up:**
- Serves reliably but below a usable agentic floor → **`partial`**, floor recorded. A measured envelope
  boundary, not a failure.
- Tool-call contract breaks in motion → **#16 confirmed**. C1 may still grade on serving alone; the
  harness verdict is **not** graded here.
- W2 not run → the dense/MoE inversion **stays a prediction** and is reported as one. It does not become
  a finding by having been asserted twice.
- Config needs changing → **HARD STOP**, reported blocked, not failed.

## Explicitly out of scope

- ~~**C2 (#5) — the harness verdict.**~~ **No longer out of scope.** The advisory below was put to the human
  at gate-1 and **accepted**: shd-003 is merged in as W7 and C2 is graded here, independently of C1.
  *(Original text: "This proves the serving stack, not that a harness drives a task to completion with no
  manual steps. C2 evidence is handed to shd-003, not graded here. Advisory: merging shd-003 into this run is
  defensible — one hardware window, real overlap. Human's call at gate.")*
- **The rest of shd-003's slate beyond a first pass.** W7 runs the slate in order and stops at the first
  harness that completes; it is not an exhaustive harness bake-off. Continue (#13) stays parked.
- **Model-quality comparison between harnesses.** W7 measures completion, not output quality.
- **C3 (#103) routing / escalation** — shd-006, separately scoped.
- **Model-quality benchmarking.** W2 compares throughput and completion, not coding ability.
- **Quantization sweeps** beyond the single dense contrast arm.
- **Purchasing recommendations.** The sizing note characterises what was measured and what it implies; it
  does not recommend spending money on hardware nobody has benchmarked.
- **Multi-machine distribution (N4)** — architected, not built (D11); tie-breaker only.
- **Changing the serving host's configuration.** Out of reach by construction; escalate instead.

## Coverage / done call  *(synthesis)*

A validated scope is done when the artifacts clear `done_when`, **or** the measured envelope is recorded
with an honest negative and a `lesson-learned`. Loop-until-dry does not apply — this is a proof scope; its
finish line is the artifact. Human reviews at the **firewall** gate and at synthesis.

## Dependencies

- Serving host reachable at `100.122.119.72:11434` — **verified live 2026-08-04**: model resident,
  `context_length` 32768 in force, `keep_alive` never-expire, both routes returning valid responses.
- The held-out task spec (W4), fixed before the first arm runs.
- W2 only: human-approved `ollama pull qwen2.5-coder:32b` (~19 GB). **Granted at gate-1, 2026-08-04.**
- ~~`gh` auth failing `401 Bad credentials`~~ — **cleared 2026-08-04**: authenticated as `dug-21` on
  `github.com` with `repo` scope; `dug-21/arch-research` resolves. The Issue is created at INIT, not
  retroactively (OBS-10).
- W7 only: `aider` installed into the devcontainer from PyPI (egress verified). Claude Code 2.1.221 is
  already present for the T3a arm.
