# SCOPE — smart-edge-002

**ID:** `smart-edge-002` (canonical key = `context_cycle` topic = `feature_cycle` = `product/research/smart-edge-002/`)
**Title:** Validated POC — deterministic in-server hotspot bank for `context_cycle_review`
**Status:** scoped
**Promoted from:** `smart-edge-001` / **H11** (theme-scan; triage-v2 build #1, first-build per the H29 grade-chain audit = CLEAN → H11).
**Theme / use-case:** `theme:smart-edge` · use-case #1 Unimatrix.
**Confidence-required:** **validated** (→ a real, demonstrated-by-us artifact can move the technology to `proven`).
**Phase / area:** knowledge-quality / observability.

## The question
> Can a deterministic, in-server automata pattern-bank (Rust `RegexSet` + `aho-corasick`), fed by the factory's own accumulated lessons/observations, recover the hotspots a human retro finds in a real cycle buffer — and surface ones the human missed — at a negligible, measured resource footprint?

## Why it matters
`context_cycle_review` hotspot detection is heuristic text-scanning today. A deterministic multi-pattern bank makes review **structural, compounding, and cheap** — every stored lesson can become a signature (the H28 substrate this de-risks), and it is the runnable-now head of the value chain toward the H23 on-device-extraction step-function. First real exercise of the theme's proof path (scan → hypothesis → **proof-goal → firewall**).

## Known constraints & prior art (build on these — do not re-derive)
- **Corrected substrate:** Unimatrix server is a **Rust binary**; the bank lives **in-binary** (pure-Rust `regex`/`RegexSet`/`regex-automata`/`aho-corasick` — no FFI, no Hyperscan needed at this scale). Client is a dumb JS/TS shim → intelligence is server-side.
- **Signature source:** the factory's own `lesson-learned`/`finding` nodes + `observations.md` OBS-* + past retro output.
- **Real buffer available:** `context_cycle_review(feature_cycle:"shd-005", transcript:{…})` (shd-005 had ~186 records) — a real, completed cycle buffer with a human retro to compare against (`factory-retro` shd-005 → OBS-7/OBS-8).
- **Do not inherit** the scout's secondary-sourced ms/MB figures — measure first-party.

## Bounded investigation (workstreams)
- **W1 — signature bank.** Derive ≥50 anti-pattern signatures from real lessons/observations/retros (retry loops, gate-failure markers, permission-prompt storms, tool-call thrash n-grams, cold-restart signatures). *Output: the signature set + provenance (which lesson each came from).*
- **W2 — the bank artifact.** A `RegexSet`+`aho-corasick` bank (in-binary Rust for the validated bar; a scripted proof-of-mechanism is the *cheapest-test* precursor, graded `partial` not `proven`). *Output: the built bank + how it streams a buffer.*
- **W3 — run over a real buffer.** Stream ≥1 complete real cycle buffer (shd-005) through the bank. *Output: the hit list (signature → span).*
- **W4 — compare + measure.** Compare hits vs what the manual retro actually flagged; measure first-party throughput (ms/MB) + peak memory at 100 / 1k / 10k compiled patterns. *Output: recall vs manual, novel-catch, the envelope numbers (also the H28-substrate economics de-risk).*

## Proof bar (what moves the technology to `proven`)
The technology (in-server automata hotspot bank) → **`proven`** iff a demonstrated-by-us artifact shows, on a real buffer:
(a) **recovers a majority** of the hotspots that cycle's manual retro flagged, **AND**
(b) **surfaces ≥1 real hotspot the manual retro missed**, **AND**
(c) reports **first-party** throughput (ms/MB) + peak memory at 100/1k/10k patterns.
- **Altitude honesty:** a scripted (non-Rust, non-in-binary) proof-of-mechanism that clears (a)+(b) but not the in-binary/throughput bar earns **`partial`** (empirical — the mechanism is demonstrated, the in-server envelope claim is not). Only the in-binary artifact with the measured envelope clears **`proven`**. The firewall does not round up.

## Explicitly out of scope
- The **H28 shared substrate** (fund at the 2nd consumer) — this scope is the single consumer.
- The **H25 live/actuator** path (this is *post-hoc* review only — no feedback-channel-into-a-running-agent).
- Hyperscan/vectorscan FFI (pure-Rust crates suffice at this scale).
- Any change to how grades are set (that's the write-path bundle, smart-edge-003 candidate).

## Coverage / done call
Folded into synthesis: the artifact either clears the proof bar (→ `proven`, altitude-scoped) or lands `partial` with the exact gap named; on `proven`, **handoff = file a `dug-21/unimatrix` issue** with the artifact as evidence (the theme's product bridge, §7). No Unimatrix capability board is created — a proof-goal proves a *technology*, tagged to the theme + use-case.

## Amendment log
*(append-only, dated — reconcile any changed verdicts)*
