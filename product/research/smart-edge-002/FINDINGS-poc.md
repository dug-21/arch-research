# FINDINGS — smart-edge-002 feasibility POC (H11 hotspot bank)

**Run:** `smart-edge-002` · **agent_id:** `smart-edge-002-poc` · cycle-stamped (`context_cycle` start→feasibility→synthesis).
**Artifact:** `product/research/smart-edge-002/hotspot-bank/` — a real Rust binary (`regex` 1.12 + `aho-corasick` 1.1), 58 signatures, built + run.
**Firewall grade earned: `partial`** (empirical — mechanism demonstrated by us on real data). **NOT `proven`** — see the gap. Research/POC moves structure + non-proven grades; it does not round up.

## What was proven (the artifact demonstrates)
1. **Deterministic recall of real hotspots — 11/11 = 100%, 0 false positives** (5 clean lines). Labeled set drawn from *real* documented events: shd-005's `cycle_review` findings (F-01 session gaps, F-02 reread) + the manual retro's OBS-* (write-block, mcp-stale, rate-limit, non-gate-prompt, telemetry-empty, retry).
2. **The money case — recovered the hotspot `cycle_review` MISSED.** shd-005's `cycle_review` surfaced only session-gap + reread; it did **not** flag the subagent write-block pattern the human retro caught (OBS-7). The bank recovers it deterministically. **Coverage = the union of both baselines**, catching each one's blind spot (write-block missed by the tool; session-gap/reread missed by the manual retro).
3. **Real corpus scan.** 5 real session subagent transcripts, **919 KB, 199 ms, 4.4 MB/s, ~5.4 MB RSS**. Real live hits: error 25, gate-rework 13, rate-limit 6, reread 2, search-miss 1, write-block 1.

## The load-bearing engineering finding (first-party, corrects inherited assumptions)
Measured, not inherited from the scout's secondary sources:

| Engine | 100 sigs | 1k | 10k | 100k |
|---|---|---|---|---|
| **`regex` RegexSet** (scan MB/s) | 2.7 | 0.3 | **0.0 (48s)** | — (blows default 10 MB compile limit) |
| **`aho-corasick`** (scan MB/s) | 706 | 286 | 306 | **284** (compile 44 ms) |

- **`RegexSet` does NOT scale** — throughput collapses with pattern count and it hits the regex crate's 10 MB compiled-size ceiling around 10k patterns (a real `CompiledTooBig` panic before we bumped `size_limit`). The scout's inherited "negligible cost / ms-per-MB" figure is **false at bank scale** for RegexSet.
- **`aho-corasick` IS the right engine for the large literal bank** — flat ~285 MB/s at **100k** signatures, sub-50 ms compile. The hypotheses' "marginal cost of pattern n+1 ≈ 0" (H28) is **true for aho-corasick, false for RegexSet.**
- **Validated two-engine design:** `regex` for the dozens of *complex* signatures (backrefs to structure, `\d+h gap`, etc.), `aho-corasick` for the large *literal* signature bank. This is exactly the H11/H28 substrate shape — now with first-party numbers behind it.

## Why `partial`, not `proven` (the honest gap)
The proof bar (SCOPE) for `proven` requires the **in-server Unimatrix (Rust binary) integration** with the envelope measured *there*. This artifact is a **standalone binary** — it demonstrates the mechanism + the real engine + the real scaling envelope, but not the in-server integration. Two gaps to `proven`:
1. **In-server.** Build the bank inside `dug-21/unimatrix`'s `context_cycle_review` path (different repo). Structurally not reachable from arch-research.
2. **A genuinely Unimatrix-linked cycle buffer.** The shd-005 raw buffer was unretrievable (old-version behavior, since fixed). We cycle-stamped `smart-edge-002` to test the corrected retention/linkage (see the retention note in the cycle_review of this run). The proven-grade run should stream a *linked* buffer, not the on-disk subagent transcripts used here as a real proxy.

## Corrections banked (honesty)
- The earlier inference "post-hoc the buffer is purged → H11 is mooted, go live-only" was **wrong** — it reasoned off *old-version* behavior. With retention fixed + cycle-stamping, a post-hoc bank over a retained buffer **is** viable. H11 is *stronger*, not mooted.
- Transcript↔cycle linkage **requires `context_cycle` stamping** — an unstamped run has no linked buffer at all (ties to the wire-cycle-stamping gap).

## Handoff (product bridge, §7)
On this `partial`: file a `dug-21/unimatrix` issue proposing the in-server hotspot bank for `context_cycle_review`, citing this artifact as the mechanism+envelope evidence, and recommending the **two-engine split** (regex for complex signatures, aho-corasick for the literal bank) with the measured scaling as the design basis. "More proof is better upon handoff" — this hands off a working bank + real numbers, not a hypothesis.

## Rerun on REAL Unimatrix transcript (2026-07-08) — the precision finding

After the platform owner shipped a transcript-retention fix, we re-ran against a genuinely
Unimatrix-**linked** buffer (the thing H11 always needed and couldn't get before).

- **Retention confirmed.** A post-update stamped cycle (`smart-edge-003`) now returns real transcript via
  `cycle_review`: **`Transcript bytes: 112091`**, `Transcript deltas: 4`, real `transcript_candidates`
  (the `PostToolUse` event stream) — vs `unavailable (no data)` on the pre-update `smart-edge-002`.
  Transcript↔cycle linkage requires `context_cycle` stamping; a stamped, post-fix cycle now retains it.

- **The precision failure the synthetic test hid.** On the real transcript the lexical bank fired
  **`firewall` (critical)** on our *own* H29 node text ("…never a **bare context_tag**") and **`error`**
  on "**error-recovering**". **None are hotspot *events*** — they are agents *writing about* the concepts.
  The synthetic labeled test scored 100%/0-FP because its lines looked like events; **real transcript is
  full of agents reasoning about kill/throttle/firewall/error**, and naive lexical matching cannot tell
  *"discussing a kill"* from *"a kill event."* This is the reflexive loop working: running the tool on
  real data surfaced its next design constraint.

- **The fix is STRUCTURAL, not lexical (identified here; demonstrated below).** Signatures must anchor on
  **event structure** — the `tool:` / `response:` / exit-code / error *fields* of a tool-use record — not
  free prose. This is exactly the **structural tier (H2/H3, tree-sitter over the event tree)** the two-tier
  design already carries: the `RegexSet`/`aho-corasick` lexical bank is necessary but **not sufficient**
  for transcript precision. **Updated handoff picture:** recall + scaling hold; transcript *precision*
  requires the structural tier.

## Reproduce
`cd product/research/smart-edge-002/hotspot-bank && cargo run --release -- signatures.json labeled.txt <corpus files...>`
