# triage.md — theme-scan `smart-edge-001` (convergent gate)

**Theme:** `theme:smart-edge` · **Use-case:** #1 Unimatrix · **agent_id:** `smart-edge-001-goal-owner` · **Firewall:** advisory only — I score and route; the owner promotes, the curator files. No graph write.

**Discipline applied:** park by default. Of 24 generated, **16 park, 8 survive** — and the 8 survivors collapse to **6 spend-lines** (2 collision-merged, 2 bundled). Two of the six are pure *measurements*, not builds.

## Per-hypothesis verdict table

Axes: **Mech** = mechanism/capability-fit (primary — attack the mechanism) · **Theme** = lens AND value-target · **Nov** = application genuineness/non-redundancy · **E/P** = effort vs payoff.

| H# | Mech | Theme | Nov | E/P | Verdict | One-line rationale |
|----|------|-------|-----|-----|---------|--------------------|
| H1 | M | M | M | M | **PROBE** (bake-off) | Error-recovering parse is real, but a strict grammar fights the KB's deliberately free-form design; resolve the whole content-grammar slot cheaply first. |
| H2 | M | M | M | M | PARK | cycle_review is already covered runnable-now by H11; structural take is the harder residue, coupled to an unstable platform-owned transcript format. |
| H3 | L | M | M | M | PARK | Dies on platform access (mid-cycle buffer read; telemetry is named-cycle-only), not on tech; also depends on H2. |
| H4 | L | L | L | L | PARK | Corpus-thin — KB is mostly prose; too little code-bearing content for AST-chunking to register. |
| H5 | L | L | M | M | PARK | Subtree paths rot the instant `context_correct` reissues ids + rewrites content → dangling references. |
| H6 | M | L | L | L | PARK | Low standalone value; a rider on H1, not its own investment. |
| H7 | M | M | M | L | PARK | Same corpus-thinness as H4 — rises/falls on the same fact; park together. |
| H8 | L | M | L | M | PARK | Needs the H1 content-grammar substrate or only touches embedded code islands; amortization unproven. |
| H9 | M | M | **H** | M | **PROBE** (bake-off) | Deterministic extraction (no hallucinated fields, explicit misses) is a genuinely strong property; head-to-head vs H1 on the same corpus question. |
| H10 | M | L | L | L | PARK | Serves repo periphery, not a `context_*` capability; conventions here are semantic, not syntactically lintable. |
| **H11** | **H** | **H** | M | **L** | **BUILD** ★ | Archetypal smart-edge primitive; runnable NOW (no grammar, no platform change, no hardware); compounds via the lessons corpus (each lesson → a signature). |
| H12 | M | M | M | L | **PROBE** | Identifier-blindness is plausible; measure whether the miss-class is real BEFORE committing to rank-fusion (where hybrid search projects die). |
| **H13** | **H** | **H** | M | **L** | **BUILD** | Literally Hyperscan's DPI design center; cheapest test in the set (scan existing KB export); a safety property the write path wholly lacks. |
| H14 | M | M | L | M | PARK | Premature — shd-006's rule count is dozens, not thousands; engine swap buys integration cost for no felt gain. |
| H15 | L | M | H | M | PARK | The load-bearing risk (auto signature-derivation → alert fatigue) is NOT cut by the cheap test, which only exercises hand-picked signatures on the easy case. |
| H16 | M | L | M | H | PARK | Out of the include-test (RPQ shrinks no envelope) and it's a Unimatrix platform-roadmap change, not a bolt-on. |
| **H17** | **H** | M | L | **L** | **BUILD** (bundle) | Tag conventions are already regexes; near-zero-cost guard — too small to stand alone, bundle into H13 as write-path deterministic guards. |
| H18 | L | L | L | L | PARK | Near-dups are dominated by paraphrase (semantic); regex canonicalization can't touch it — embedding-similarity dedup is the real answer. |
| H19 | M | L | M | H | PARK | Agent-facing DSLs can underperform raw tool-calls (models pretrained on the tool idiom, not invented syntax) AND platform feature in the contested slot — double-discounted. |
| H20 | M | M | M | M | PARK | The content-grammar slot's weakest engine (pika: one 2020 impl vs tree-sitter's decade); excluded from the bake-off unless the slot proves out. |
| **H21** | **H** | **H** | M | M–H | **BUILD** (edge flagship) | The theme's center of gravity — determinism in the grammar, model is just fill; enables a *smaller* on-device model. Hardware-gated; sequence after the runnable-now win. |
| H22 | M | M | L | M | PARK | Binding uncertainty is a platform question (is review generated where a sampler can be constrained?), not resolvable by a cheap look on our side. |
| H23 | H | H | H | H | PARK (step-fn) | The named step-function, but not a first-mover: depends on H11 (locate) + H21 (emit-valid) proving first, and carries the garbage-yield risk. Defer-and-record. |
| H24 | M | M | **H** | **L** | **PROBE** | The "measure-first" (curator time: reformatting vs judging) is a cheap structure-only look that decides whether the whole inversion has a basis. |

★ = top recommendation.

## Shortlist (6 spend-lines)

### Builds

**H11 — Multi-pattern hotspot bank for `context_cycle_review` (RE2/Hyperscan). PROMOTE FIRST.**
Smallest, highest-leverage, runnable now, no firewall exposure, compounds with the lessons corpus.
`done_when`: *A CPU-only RE2/Hyperscan bank of ≥50 anti-pattern signatures derived from existing lesson-learned nodes + past retro observations, streamed over ≥1 complete real cycle observation buffer, (a) recovers a majority of the hotspots the manual retro of that cycle actually flagged, (b) surfaces ≥1 real hotspot the manual retro missed, and (c) reports measured first-party throughput (ms/MB) + peak memory on the actual buffer — no inherited secondary-sourced figures.*

**H13 + H17 — Write-path deterministic guards (`context_store` intake). BUILD SECOND.**
`done_when`: *A single-pass deterministic scan at intake (a) flags/quarantines any node matching a standard secret/PII/credential pattern set — validated by running the bank over the existing KB export (zero known secrets slip; every planted test secret caught), and (b) rejects any malformed tag against the tag grammar (`grade:`/`theme:`/run-id shapes, the "no tag named status" rule) — validated by counting real violations already present in the current tag set — at a measured per-write cost that does not regress the write path.*

**H21 — Grammar-constrained node emission from a small on-device model. BUILD (edge flagship, hardware-gated).**
`done_when`: *A ~3–4B quantized on-device model (llama.cpp + GBNF) constrained to the finding-template grammar achieves a materially higher valid-first-pass structural-correctness rate with 0 retries across 20 real authoring/extraction tasks vs the unconstrained baseline, AND the measured footprint (model + mask overhead, tokens/task) confirms a material envelope reduction vs a frontier-model-in-the-loop baseline — the envelope-exception the theme owes itself.* **Firewall clause (must be in scope):** grammar-validity buys *structure only*; every emitted node still enters `quarantine → enroll` and is graded by the curator — validity never touches grade. Grammar-valid ≠ true; a confidently-shaped hallucination is *more* dangerous than a malformed one.

### Probes (directional, structure-only, cut uncertainty before any build)

**Substrate bake-off (H1 vs H9; H20 excluded).** Cheap head-to-head on ~50 real nodes + their `cites:` blocks: does node content have a stable enough skeleton to grammatize (tree-sitter parse) or shape-extract (ast-grep meta-vars) *without* false-positive friction? Resolves whether the entire H1/H9/H20/H19 content-grammar slot is worth a build and picks the engine. If the corpus is too free-form, the whole slot parks. pika (H20) excluded up front — ecosystem-thin.

**H12 — identifier-channel reality check.** Measure recall@5 with vs without a deterministic identifier-pattern side-channel on ~10 real queries that demonstrably missed on exact-identifier intent. Confirms the miss-class exists *before* committing to rank-fusion engineering. Runnable now.

**H24 — curator time-split measurement.** Instrument one full run for curator time split between reformatting/structural-fixing vs judging. Not a build — a measurement. Material reformatting fraction (plausible at the current multi-goal-scale focus) → the validated-inbox inversion earns a pilot; otherwise it parks permanently.

## Parked set (16) — one reason each
H2 (covered runnable-now by H11; residue coupled to unstable platform format) · H3 (dies on mid-cycle platform access, not tech) · H4 (corpus-thin) · H5 (paths rot on `context_correct` id reissue) · H6 (rider on H1, no standalone value) · H7 (corpus-thin, twin of H4) · H8 (needs H1 substrate; amortization unproven) · H10 (repo periphery + semantic-not-syntactic) · H14 (premature; shd-006 rule count is dozens) · H15 (cheap test doesn't cut the binding signature-derivation risk) · H16 (out of include-test + platform feature) · H18 (paraphrase-dominated; embeddings are the real answer) · H19 (agent-DSL underperformance + platform, contested slot) · H20 (weakest engine in the content-grammar slot) · H22 (binding uncertainty is an unanswerable-on-our-side platform question) · H23 (step-function, but sequence-gated on H11+H21 + garbage-yield risk).

## Funnel telemetry (reflexive loop #66)
- **Generated 24 → survived triage 8** (16 parked). Survivors collapse to **6 spend-lines** (H1+H9 = one bake-off; H13+H17 = one build).
- **By novelty class (survived / generated):** obvious **4/5** · adjacent **2/9** · non-obvious+whitespace+inversion **2/10**.
- **Signal for the loop:** survival concentrated hard in the *obvious, runnable-now, deterministic* primitives; the non-obvious range mostly parked — but on **platform walls** (H3/H5/H16/H19/H22) and **unsolved hard parts** (H15), not on lack of imagination. The divergent generator's range was healthy; the terrain has platform-gating and corpus-thinness walls the hypothesizer correctly flagged and I confirmed. Watch across future scans whether non-obvious survival stays this low — if the pattern holds, it argues the smart-edge/Unimatrix value is genuinely in cheap deterministic primitives, not speculative level-ups.

## Step-function lens on survivors
H11 (locate hotspots cheaply, deterministically) + H21 (emit template-valid nodes from a small on-device model) are the two halves of **H23 — on-device knowledge extraction at cycle close**. That composition is the real level-up: *every* cycle tithes knowledge on-device (one quantized model + automata, no frontier call), not just the cycles that earn a full human retro. Yield-per-cycle is the factory's own compounding-asset metric — this is a step-function, not a linear gain. **Worth-it call: DEFER-AND-RECORD.** Do not chase it as a first proof (depends on both halves proving; garbage-yield risk of well-formed mediocre findings bloating the KB, which `quarantine/enroll` must gate from day one). Record it now as the named target the first two builds unlock, so it is never lost. Advisory — never mandates chasing it, never relaxes the firewall or budget.

## Top recommendation to the owner
Promote **exactly one** first proof-goal: **H11** (multi-pattern hotspot bank for `context_cycle_review`). It is the smallest and highest-leverage: runnable today with zero hardware and zero platform dependency, the cheapest real `done_when`, no firewall exposure (read-only deterministic analysis), and it compounds — the lessons-learned corpus *is* its pattern source, so review sharpens automatically as the KB grows. It also sits at the head of the value chain toward the H23 step-function. Sequence **H13+H17** (write-path guards) close behind — near-zero incremental cost, retroactively self-proving. Hold **H21** (edge flagship) for a second wave once hardware/local-model is in play. Run the three probes (bake-off, H12, H24) as cheap structure-only looks in parallel — they cost little and each one either opens or permanently closes a downstream build.

Hardware note: H11, H13, H17 and all three probes are **runnable now (CPU, no local model)**; **H21 (and parked H22/H23) are hardware-gated** on local/edge model compute.
