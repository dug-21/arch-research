# triage-v2.md — theme-scan `smart-edge-001` · PASS 2 (delta re-triage)

**Theme:** `theme:smart-edge` · **Use-case:** #1 Unimatrix · **agent_id:** `smart-edge-001-goal-owner` · **Firewall:** advisory only — I score and route; the owner promotes, the curator files. No graph write.

**Discipline stance:** the corrected surface lowered effort for many hypotheses — that is precisely the moment to hold the line. An effort drop raises E/P; it does **not** rescue a weak mechanism (H26 security bank), thin theme-fit (H16), or an unproven hard part (H15, H25 actuator). Park by default. Pass-1 verdicts are the baseline; Part C priors are unchanged and retain them.

**Novelty check (live graph):** nothing covers in-server automata / pattern-bank / real-time-governor / grade-transition-FSM applications. Nearest neighbors are shd-005/006 routing/egress nodes (#78 deny-by-default egress boundary, #81 routing-gate composition, #35 D7 firewall ADR) — a different mechanism (network egress gate / a decision record), not in-server transcript automata or a lifecycle DFA. The five new hypotheses are genuinely new *applications*.

## Delta verdict table — NEW (H25–H29) + Part B revivals

Axes: **Mech** (mechanism/fit — primary) · **Theme** (lens AND value-target) · **Nov** (genuineness/non-redundancy) · **E/P** (effort vs payoff, on the corrected surface).

| H# | Mech | Theme | Nov | E/P | Verdict | One-line rationale |
|----|------|-------|-----|-----|---------|--------------------|
| **H25** (S1) | M | H | H | M | **DIRECTIONAL-PROBE** | Detection is proven-class; the *actuator* (feedback channel into a running agent) is genuinely new, unproven surface. Replay-and-would-have-fired probe cuts the "precursors detectable early enough" uncertainty **before** any actuator build. A matching-only proof dodges the real question. |
| **H26** (S2) | M | H | M | M | **PARK** (absorb → H25) | Shares H25's actuator/kill channel — not an independent effort; reliability signatures are H28-bank content; security bank is a self-admitted tripwire (adversary paraphrases past a literal bank). Its distinct value rides the H25 probe. |
| **H27** (S3) | **H** | M | M | **L** | **SURVIVE** (probe + bundle) | Enumerate-not-ML edge-schema audit is cheap and *self-documenting* (the enumeration IS the violation report) → one-afternoon probe with retroactive value. Write-time enforcement folds into the write-path guard bundle (config-as-data, warn-before-reject). |
| **H28** | **H** | H | H | **L→poor-as-first** | **DEFER-AND-RECORD** (architect-for-future) | Sound economics, but building a shared multi-consumer substrate before any single consumer proves is textbook premature infrastructure — the hypothesizer's own note: fund at the **2nd consumer**. Its ~200-line economics benchmark piggybacks on H11's build. |
| **H29** | **H** | H | M | **L** | **BUILD** (write-path bundle) | A DFA over `{missing,claimed,partial,proven}` enforcing D7 verbatim — the automata family's center at ~50 lines, hardening the factory's most load-bearing rule while attribution is untrustworthy (D6). Audit-first proves need. |
| H2 (rev) | M | M | M | M | **PARK** (absorb → H25 structural tier) | Wall lifted, but it is now the *structural tier* of H25's stack (live tree-sitter tree), not standalone — higher effort, marginal value over the lexical bank unproven. Defer behind the lexical actuator. |
| H3 (rev) | M | M | M | M | **PARK** (absorb → H25 structural tier) | Same as H2 — the kill condition was the liftable wall, but the revived form is H25's structural-escalation tier, not a first-mover. Defer-and-record with H2. |
| H16 (rev) | M | **L** | M | (was H) | **PARK** (unchanged verdict) | The **discipline trap**: effort collapsed (roadmap→100-line feature), but pass-1's *other* kill stands — RPQ shrinks no resource envelope, so it fails the smart-edge include-test. Cheaper ≠ in-lens. |
| H1 (rev) | M | M | M | M | **PROBE** (bake-off, narrowed) | Effort drops (ast-grep-core/tree-sitter in-binary) but the core uncertainty — is KB content grammatizable without false-positive friction — is untouched. Bake-off narrows to tree-sitter vs ast-grep-core. |
| H9 (rev) | M | M | H | M | **PROBE** (bake-off) | Deterministic extraction still the strong property; effort lower, uncertainty unchanged. Head-to-head with H1 on the same corpus question. |
| H11 (rev) | **H** | **H** | M | **L** | **BUILD ★** (retained) | No Hyperscan FFI needed (`RegexSet`+`aho-corasick` in-binary); becomes the post-hoc consumer of the same bank H25 runs live. Guaranteed near-term yield; done_when now doubles as the H28 economics de-risk. |
| H13 (rev) | M | M | M | M | **PROBE** (characterization) — *demoted from BUILD* | PII scanner already exists → hypothesis reframes to "improve coverage/throughput." Must characterize the existing scanner first: if it is already `regex`-crate-based this collapses to a pattern-set contribution, **not** a proof-goal. |
| H17 (rev) | **H** | M | L | **L** | **BUILD** (write-path bundle) — *re-bundled* | Trivially in-binary; leaves the H13 bundle and joins H29+H27(write-time) as "write-path deterministic guards" — three tables, one enforcement pattern. |
| H12 (rev) | M | M | M | M | **PROBE** (retained) | In-server beside the embedding query, but the load-bearing risk (rank fusion worsening the common case) is untouched by the substrate correction. Measure the miss-class first. |
| H14 (rev) | M | M | L | M | **PARK** (retained, firmer) | Effort *and* urgency both drop — pure-Rust crates suffice at shd-006's dozens-of-rules scale; reinforces the premature-optimization park. |
| H15 (rev) | L | M | H | M | **PARK** (retained) | Matcher folds into H28, wall liftable — but the load-bearing bet (auto signature-derivation → alert fatigue) is explicitly unchanged. The cheap test still doesn't cut it. |
| H19 (rev) | M | L | M | M | **PARK** (retained) | Effort softens (PEG via `pest` in-binary) but the core doubt — agents underperform on invented syntax vs the trained tool-call idiom — is untouched. Moves on effort, not on the doubt. |

*Part C unchanged priors — H4, H5, H6, H7, H8, H10, H18, H20, H21, H22, H23, H24 — retain their pass-1 verdicts (not re-tabled).*

## Consolidated shortlist across all 29 — 7 spend-lines (2 builds · 5 probes)

### Builds

**1. H11 — Post-hoc hotspot bank for `context_cycle_review` (`RegexSet`+`aho-corasick`, in-binary). PROMOTE FIRST (see recommendation).** *Runnable now, CPU-only, zero firewall exposure, guaranteed yield.*
`done_when` (pass-1, corrected engine): *An in-binary `RegexSet`/`aho-corasick` bank of ≥50 anti-pattern signatures derived from existing lesson-learned nodes + past retro observations, streamed over ≥1 complete real cycle observation buffer, (a) recovers a majority of the hotspots that cycle's manual retro flagged, (b) surfaces ≥1 real hotspot the manual retro missed, and (c) reports first-party throughput (ms/MB) + peak memory measured at 100 / 1k / 10k compiled patterns on the actual buffer — this measurement is also the **H28-substrate economics de-risk**. No inherited secondary-sourced figures.*

**2. Write-path deterministic guard bundle — H17 (tag shape) + H29 (grade transitions) + H27-write-time (edge triples). BUILD (each gated on its audit finding real violations).** *Supersedes pass-1's H13+H17 bundle — H13 drops out (now a characterization probe); H29+H27 join.*
`done_when`: *A single in-server enforcement pass rejects, at write time, (a) malformed tags against the tag grammar (`grade:`/`theme:`/run-id shapes, the "no tag named status" rule), (b) any illegal grade transition per the D7 table (`proven` accepted ONLY on a `context_correct` attaching `proven_by`, never a bare `context_tag`), and (c) any `(source-category, edge-type, target-category)` edge outside the D8 whitelist — where **all three tables are owner-authored config-as-data (files the owner edits), warn-before-reject, with an explicit override path** (action policy in-scope, per false-positive-economics). Validated by: each table's **audit-first sweep** reporting the count of real existing violations in the current graph [nonzero = greenlight]; AND legitimate moves passing unblocked — notably `proven`→`partial` demotion on artifact rot and any D8-legitimated new triple; at a measured per-write cost that does not regress the write path.*

### Probes (directional, structure-only — each opens or permanently closes a downstream build)

**3. Substrate bake-off (H1 vs H9; H20 excluded).** Retained, **narrowed to tree-sitter vs ast-grep-core** (both in-binary; pika/H20 has no in-server deployment path). Does ~50 real nodes + `cites:` blocks have a stable enough skeleton to grammatize/shape-extract without false-positive friction? Free-form corpus → the whole H1/H9/H20/H19 slot parks.

**4. H12 — identifier-channel reality check.** Retained, runnable now. recall@5 with vs without a deterministic identifier side-channel on ~10 queries that missed on exact-identifier intent. Confirms the miss-class before any rank-fusion engineering.

**5. H13 — existing-PII-scanner characterization.** *New (demotion of the pass-1 build.)* Characterize the in-server scanner (engine, pattern set, recall on a labeled secret/credential corpus). If already `regex`-crate-based → collapses to a pattern-set contribution, **no proof-goal**. Only a measurable coverage/throughput delta justifies a scoped build.

**6. H24 — curator time-split measurement.** Retained (Part C). Not a build — a measurement gating the validated-inbox inversion.

**7. H25 — real-time-governor replay probe.** *New. The gate before any live-intervention build.* Replay ≥2 historical cycle buffers append-by-append through a standalone in-binary prototype (~50 lesson-derived + thrash-signature patterns): (a) confirm sub-ms, buffer-size-independent per-append latency; (b) log where each ladder rung *would* have fired vs what the human actually did mid-run — ≥1 "would have materially course-corrected earlier than the human noticed" at an acceptable false-positive rate confirms the precursor-detectability assumption. **Explicitly does NOT build the actuator channel** — the feedback-channel-into-a-running-agent is a *separate effort line and the genuine unknown*; this probe only decides whether that build is worth scoping. Null result parks the live-intervention line.

### Superseded / absorbed / recorded
- **H13** → out of the write-path bundle; demoted to characterization probe (#5).
- **H17** → out of the H13 bundle; into the write-path guard bundle (build #2).
- **H27-audit** → folded as the first step of build #2 (retroactive value); **H27-enforcement** → into build #2.
- **H11** → reframed as the *single-consumer* instantiation of the pattern-bank pattern (NOT the generalized H28 substrate).
- **Recorded (architect-for-future, D10/D11 — survived-as-recorded, not spend-lines):** **H28** (substrate — fund at 2nd consumer) · **H2/H3** (H25 structural tier — sequence after the lexical actuator) · **H21** (edge flagship, hardware-gated, unchanged) · **H23** (on-device extraction at cycle close, the named step-function, unchanged).

### Parked additions (one reason each)
H16 (revived on effort but still out of the smart-edge include-test — RPQ shrinks no envelope; the cheaper-≠-worth-building trap) · H26 (absorbed into H25's actuator; security bank is a self-admitted tripwire; reliability signatures are H28-bank content) · H14 (firmer park — Rust crates suffice at shd-006 scale, urgency dropped) · H15 (signature-derivation hard part explicitly unchanged) · H19 (invented-syntax-underperformance doubt untouched). *Plus the unchanged Part C parks: H4, H5, H6, H7, H8, H10, H18, H20, H22.*

## Funnel telemetry (reflexive loop #66) — 29 generated

**Buckets:** spend-line survivors **10** (feeding 7 spend-lines: H11, H17, H29, H27, H1, H9, H12, H13, H24, H25) · recorded/deferred **5** (H28, H2, H3, H21, H23) · parked **14**.

**By novelty class (survived-to-spend-line-or-recorded / generated):**
| Class | Pass-1 | Pass-2 | Δ |
|---|---|---|---|
| obvious | 4/5 | 4/5 | — |
| adjacent | 2/9 | **4/12** | +2 (H27, H29 survive; H26 parks) |
| non-obvious / whitespace / inversion | 2/10 | **4/12** | +2 (H25 probe, H28 recorded) |

**Signal — did lifting the walls revive the non-obvious? Yes, partially, and it validates the pass-1 read.** Pass-1 survival concentrated hard in obvious/runnable-now primitives, and I attributed the low non-obvious survival to **platform walls, not lack of imagination**. The corrected surface tests that claim directly: when the walls came down, non-obvious survival doubled (2→4) and adjacent doubled (2→4), while obvious was already saturated. So the wall-attribution was correct — the divergent generator's range was healthy and the terrain, not the ideas, was gating.

**But the important caveat:** the *revived* survivors are overwhelmingly the **cheap enforcement/discipline** plays (H27, H29 — low effort, high leverage, near-zero risk). The genuinely **ambitious** level-up (H25's real-time actuator) survived only to a **probe**, not a build — because its hard part (the actuator channel + false-positive-kill economics) is an unproven unknown, *not* a wall the owner can lift. Lesson for future scans: lifting platform walls revives *cheap* non-obvious ideas immediately; the *ambitious* non-obvious ideas still gate on genuine engineering unknowns that no owner decision removes.

## Step-function lens on survivors
- **H23 (on-device extraction at cycle close)** — unchanged: the named step-function, still **defer-and-record**, still gated on H11 (locate) + H21 (emit-valid) proving first, still carrying the garbage-yield risk `quarantine/enroll` must gate.
- **H25/H28 name a nearer step-function the corrected surface surfaced:** platform-as-**actuator** (H25) riding an executable-KB **substrate** (H28) — "stored lessons become live defenses on the next bank compile." This is a genuine capability-class change (recorder→actuator) and the specific level-up the owner seeded. **Worth-it call: DEFER-AND-RECORD, gated on the H25 replay probe.** Do not chase the actuator as a first build — the false-positive-kill economics and the novel feedback-channel are unproven, and a matching-only proof dodges the question. Record it as the target the H25 probe either opens or closes. Advisory — never mandates chasing it, never relaxes the firewall or budget.

## Top recommendation to the owner — does the corrected surface change the first proof-goal?

**Mostly no — H11 still stands as the first BUILD — but the corrected surface adds one cheaper-than-a-build first *look* that should decide the ordering.**

The seductive move is to leapfrog H11 with the now-trivially-cheap write-path guard bundle. Resist it *as a reflex* — cheapness is the trap this pass was warned about — but do not dismiss it either, because the bundle hardens the factory's **most load-bearing rule** (the D7 firewall, per CLAUDE.md) mechanically, at ~50 lines, precisely while attribution is untrustworthy (D6, anonymous writes). The honest tension:
- **H11**: guaranteed near-term yield (the buffer *will* surface hotspots), zero firewall exposure, and it de-risks the shared H28 substrate economics everything else rides on. Its payoff is a *linear* quality gain.
- **Write-path bundle**: potentially *higher* leverage (underwrites every grade in the graph), smaller code — but its retroactive value is **contingent on the audit finding violations**, which in a disciplined single-curator factory may be zero today. Its value skews to the imminent multi-goal / multi-agent scale (current factory focus).

**So let the cheapest possible audit decide, rather than guess.** Concretely:
1. **First spend (hours, structure-only): run the H29 grade-chain audit** — walk existing grade-bearing nodes for any past transition the D7 table would reject.
2. **If it surfaces any illegal transition** (or the multi-goal/multi-agent roadmap makes future ones near-certain — it does): the **write-path guard bundle is the first build** — highest leverage, smallest code, hardens the load-bearing rule.
3. **If the audit is clean**: **H11 is the first build** — guaranteed yield, no contingency, de-risks the substrate.

Either way, **H11 and the write-path bundle are the top two**, sequenced by that audit. Run the **H25 replay probe in parallel** — it is the cheap look that decides whether the ambitious recorder→actuator level-up has legs or parks. Hold **H21** (hardware-gated) and **H28** (fund at the 2nd consumer) as recorded. This respects the discipline (audits gate builds; the bundle must *earn* the build by finding real violations, not win it on cheapness), uses the corrected surface (the bundle is now feasible and in-binary), and keeps the actuator's genuine unknown out of a premature proof.

**Hardware note:** H11, the write-path bundle, the bake-off, H12, H13-characterization, H24, and the H25 *replay probe* are all **runnable now (CPU, in-binary, no local model)**. Only the H25 *actuator build*, H21, H22, H23 touch new platform surface or local-model compute and are second-wave.
