# R2-1 — Cost transparency & management, all four verbs

**Run:** `wfh-004` · Issue #48 · phase `hypothesize` · round 2, targeted · read-only, zero graph writes.
**Charter:** the unowned Cost-prediction cell + anything substantively new on meter/attribute/enforce. Duplication treated as the failure mode; every candidate carries a differs-from clause naming its nearest round-1 neighbor.
**Inputs read:** BRIEFING, W0-a/b/c/d, SCOPE (§3.3, §4, §9, A-1/A-2/A-3), ROUND-1-COVERAGE, and the Cost material in all six round-1 registers (L1-19/26/27–30/32, L2-16/33 + L2 §2's Introspection→Cost edge verdict, L3-25/26/27/28, L4-28–32, L5-21–24, L6-25/26/27 + L6 §5).

---

## 1. The prediction verdict (headline)

**"Cost prediction is impossible at garage scale" is false — but not because run-grain forecasting works. It doesn't. It is false for three mechanical reasons, in descending order of confidence:**

**(a) The altitude error: the archive L4-31 says cannot exist already exists, one level down.** L4-31 is correct that regression over runs needs ~100 runs and the garage has ~8. But a run is not the natural observation unit — a *unit of work* is. Eight runs contain roughly 10–20 spawned units each plus thousands of metered events, all sitting in transcripts on disk, and the parser is proven (opcost, W0-b #26 verdict **A**; P-16's fix demonstrated correctness the hard way). **n≈8 at run grain is n≈10² at unit grain today, with zero additional runs.** Prediction at n=1 run-grain is composition over unit-grain distributions — bottom-up estimating, the oldest trick in the disciplines L1 mined. None of L5-23, L6-26, or L1-29 makes this argument; all three defer to a per-unit history *"that does not exist yet"* (L6-26's own delta note) without noticing it is harvestable now.

**(b) The structural estimator: variance concentrates at inference points, so a plan's quote is computable at n=0.** L6 §5 already states the physics — *"deterministic functions have knowable cost; each open-ended inference point adds a heavy-tailed term"* — but only as an argument for minimality, never as a forecasting instrument. Turned around: a plan's cost variance is approximately the sum of per-class variances over its declared inference points, and per-*class* priors (bounded leaf vs retrieval call vs open agentic loop) pool across all runs and units, so they converge at very small n. This yields the run's most interesting corollary:

> **The owner's A-3 inference-minimality axis is simultaneously a variance-reduction axis — prediction quality is purchasable by design.** A harness that narrows its inference surface doesn't just get cheaper and more testable; it gets *quotable*.

**(c) The substitution: where the forecast stays weak, the mature answer was never a better forecast — it was a better contract.** L1's own honesty note (*"almost none predict well; construction's variance record is poor"*) points at the resolution it didn't draw: construction, drilling, and venture finance survive bad forecasts through *bounds* (a maximum computable from structure), *staged commitment* (tranches whose default is stop), and *rolling re-projection* (EVM's estimate-at-completion). All three are abilities, none needs an archive, and the third converts prediction from a pre-run event into a continuous mid-run signal — which is what the garage actually lacked in P-26's month of silent open runs.

**Ordering that follows mechanically:** structural bound (R2-1-02) and tranche schedule (R2-1-04) are valid at n=0; unit-grain quote (R2-1-01) and inference-topology quote (R2-1-03) work now on the existing transcripts; EAC (R2-1-05) needs only completion events; L4-31's regression arrives later as **harvest, not build** — exactly L4's own closing point.

One more honest observation: **the owner's guess at the A-1 gate (18–22 spawns) was already the correct unit-grain computation, performed by a human holding no rate data.** The harness's prediction job, at this scale, is mostly to hand him the rates.

---

## 2. Candidate register

**`R2-1-01` — The unit-rate card and composed quote**
- **Ability:** Before a run starts, the harness quotes its cost as an interval composed from per-unit-type actuals harvested from all past run records, and maintains the standing per-unit rate card as a human-readable surface, observable as a quote on every run surface at admission and a rate card an owner can price a plan against.
- **Concern:** Cost (predict; spans Human steering).
- **Mechanism:** Bottom-up (engineer's) estimating over unit-type cost distributions — construction's unit-cost book applied at the unit grain, where the garage already has ~10² observations (verdict (a)). Composition by interval arithmetic or Monte Carlo over the declared plan.
- **Inference surface:** Zero for harvest, rate card, and composition. Mapping a prose plan onto unit types is a leaf today; removable by plans declaring their units as data (SCOPE A-1 already half-does this — it counted spawns).
- **Incumbent delta:** C — nothing harvests per-unit actuals; the raw material is A (transcripts + opcost).
- **Evidence:** SCOPE A-1 (envelope set by guess — the multiplication the owner did, the rates he lacked); P-17; P-30.
- **Falsifier:** If unit-type variance is as heavy-tailed as run variance (units no more homogeneous than runs), composition inherits the same useless width — **testable now against existing transcripts, before building anything.**
- **Differs from:** L5-23/L6-26/L1-29 all presuppose per-unit history as future accumulation and predict at run grain; the substance here is the observation-multiplication argument — the history already exists. L4-31 requires ~100 archived runs; this requires zero additional runs.

**`R2-1-02` — Structure-derived hard ceiling (bound, not forecast)**
- **Ability:** Before a run starts, a hard upper bound on its possible spend is computed from the declared plan's structure — unit count × per-unit caps × turn caps — and admission is refused for a plan whose bound exceeds its envelope, observable as the bound on the run surface at admission and no run ever exceeding it.
- **Concern:** Cost (predict/enforce seam — bounded-by-construction; spans E-1).
- **Mechanism:** Worst-case execution-time analysis (real-time systems): compute the maximum from structure rather than forecasting the actual, then make the maximum *real* by enforcing its terms — the per-unit caps are what make the multiplication valid. Valid at n=0; no history needed.
- **Inference surface:** Zero, given plans declare units and caps as data.
- **Incumbent delta:** C composite — `maxTurns` per agent exists unset (W0-b #29); nothing multiplies a plan out.
- **Evidence:** SCOPE A-1 (the 18–22-spawn envelope is exactly this arithmetic, done by hand, with no caps to make it binding); P-30.
- **Falsifier:** If research units legitimately vary ~100× so caps must sit far above typical actuals, a bound nobody approaches informs nothing — the tracked gap between bound and actual settles it.
- **Differs from:** L1-29/L6-26/L5-23 estimate the actual from history; this bounds the possible from structure. L4-29 carves runtime sub-budgets but computes no pre-run bound and gates no admission on one.

**`R2-1-03` — Inference-topology quote**
- **Ability:** A plan's quoted cost interval is derived from its declared inference topology — the count and class of its model-call points, with deterministic segments priced at known cost — observable as quote width that tracks inference count and narrows when a step moves to the deterministic path.
- **Concern:** Cost (predict; the A-3 axis made load-bearing).
- **Mechanism:** Variance decomposition per verdict (b): total variance ≈ Σ per-class variance over declared inference points; class priors pool across all runs and units, so they converge at tiny n. Standalone computational/economic argument; L6 §5 supplies the physics.
- **Inference surface:** Zero for the computation; requires inference points declared as data — which SCOPE A-3's required field already makes every candidate in this run do.
- **Incumbent delta:** C — nothing prices a plan; L6-27's inference ledger (B) is the natural calibration source once running.
- **Evidence:** No field pain directly; SCOPE A-3. This is what *"pricing inference density rather than tokens"* mechanically implies.
- **Falsifier:** If realized variance does not concentrate at inference points (deterministic retrieval dominates spend, or the "open loop" class is as heterogeneous as runs are), quote width won't track inference count — retrospectively testable from any inference ledger.
- **Differs from:** L6-26 predicts from per-step *history* irrespective of structure; L6-27 meters calls but predicts nothing. **The only estimator on the surface that works at n=1 with no per-unit history, and the mechanical bridge between the owner's minimality intuition and the Cost concern.**

**`R2-1-04` — Tranche funding: spend authority that expires by default**
- **Ability:** A run's envelope is released in tranches at its existing gates, with non-release the default; continuation consumes an affirmative release citing banked evidence, observable as no run holding spend authority more than one tranche ahead of demonstrated progress.
- **Concern:** Cost (enforce, and the substitute-for-prediction shape; spans Human steering, E-1).
- **Mechanism:** Stage-gate financing / real options (venture tranching, exploration drilling): under irreducible uncertainty the rational instrument is not a better forecast but a sequence of small commitments, each purchasable after the previous one pays information. The abandonment option's value *grows* with variance — precisely the garage's regime.
- **Inference surface:** The release decision is a human or leaf judgment at an already-existing gate; the tranche ledger and refusal of over-tranche spend are deterministic.
- **Incumbent delta:** C — the envelope exists as prose in one amendment; nothing releases or withholds anything.
- **Evidence:** P-26 (five runs open a month, each holding unbounded implicit spend authority nobody re-affirmed); P-03 (a drifted run kept spending its original grant).
- **Falsifier:** If gate cadence is too sparse (one gate per run), the tranche equals the envelope and this degenerates to L1-30 — measured as tranches actually released per run.
- **Differs from:** L1-30 is a one-shot precommitted *stop* criterion that fires at breach; this is a recurring **default-stop requiring affirmative renewal** — the polarity inversion L1-38 applied to liveness, applied here to money. L2-16 leases a step's budget mechanically; this is the run-altitude commitment schedule above it.

**`R2-1-05` — Rolling estimate-at-completion**
- **Ability:** Mid-run, the harness continuously projects cost-at-completion from spend-so-far against plan-progress-so-far, observable as a projection updating at step boundaries and an alarm firing when the projection exceeds the envelope while actual spend is still inside it.
- **Concern:** Cost (predict — the mid-run half; spans Introspection, Steering).
- **Mechanism:** Earned Value Management (CPI = work-performed/actual-cost; EAC = budget/CPI) — sixty years old, from exactly the disciplines L1 mined for pre-run estimates; their answer to their own poor forecasting record is re-projection at every reporting period, not better first guesses.
- **Inference surface:** Zero given unit-completion events; "percent complete" of a half-done open-ended unit would be a leaf — avoidable by counting only completed units (coarser, deterministic).
- **Incumbent delta:** C — no mid-run spend figure exists (P-17), no completion events exist (P-21).
- **Evidence:** P-26 (an EAC of ∞ nobody computed for a month); SCOPE A-1. **The ability that makes the meter an *input to* the run.**
- **Falsifier:** If early-run CPI does not predict late-run CPI for research work, EAC is noise dressed as foresight — **testable retroactively on the 8 archived runs.**
- **Differs from:** L6-26/L1-29 predict at start and score at close; nothing in round 1 re-projects *during*. L3-28 baselines a unit's consumption against history but projects nothing forward; L1-32 screens exceedances post-hoc.

**`R2-1-06` — Spend-admission control at expensive-action boundaries (the A-1-independent enforcement route)**
- **Ability:** When a run's measured spend crosses its envelope, subsequent expensive actions — agent spawns above all — are refused at admission with the meter reading cited, the current turn left to finish, observable as spawn denials rather than loop halts.
- **Concern:** Cost (enforce).
- **Mechanism:** Admission control at the boundaries the control plane can already match. **W0-b's diagnosis contains its own inversion:** *"spend is not a matchable predicate; control channels match tool calls"* — but the dominant future-spend quanta (spawns, each committing a fresh context and a full work transcript) **are tool calls**. A pre-execution deny whose check computes cumulative spend from the transcript record (parse proven cheap and correct by opcost/P-16) converts spend into a matchable predicate at exactly the points where most future spend is committed. Coarse by design: it cannot stop an in-turn burn and does not try.
- **Inference surface:** Zero.
- **Incumbent delta:** **B** — every part is shipped (PreToolUse deny, W0-b #15; transcript parse, #26). Turns on **A-2** (does a deny fire inside subagents), **not A-1**.
- **Evidence:** P-30; plus the round-1 registers' own pattern — L5-21, L1-27, L3-25, L6-25 all route enforcement through A-1's unprobed halt. **This is the route that does not wait for that probe.**
- **Falsifier:** If in-turn burn (cache-heavy long context, many fetches within one turn) dominates spawn-committed spend, gating spawns caps little — decidable now from opcost's per-event data.
- **Differs from:** L5-21/L1-27/L3-25/L6-25 all halt the running unit and inherit A-1; L2-16's lease requires an egress proxy we would have to build and operate. **The only enforcement shape on the surface expressible in the incumbent today, with its granularity limit priced honestly.**

**`R2-1-07` — Graduated degradation before any hard stop**
- **Ability:** A unit crossing spend thresholds is stepped down a declared degradation ladder — cheaper model, narrower fan-out, summarize-and-bank — before any hard stop, observable as recorded mode transitions with hard stops occurring only from the last rung.
- **Concern:** Cost (enforce; spans Recovery).
- **Mechanism:** Load shedding / brownout (power grids, adaptive-bitrate streaming): when the alternative to partial service is total loss of in-flight value, a declared degradation ladder dominates a binary kill. **This is the direct answer to the falsifier the entire round-1 enforcement family carries** (L1-27: *"suspension destroys more value than overrun costs"*; L2-16: *"a killed step forfeits all its spend"*) — degradation is what makes ceilings safe to actually enforce.
- **Inference surface:** Ladder transitions deterministic; the terminal "summarize-and-bank" rung deliberately spends one bounded leaf to preserve the unit's state.
- **Incumbent delta:** B/C — per-agent `model:` exists (one agent uses it); nothing switches anything on spend; shares R2-1-06's or A-1's substrate.
- **Evidence:** none direct — no enforcement has ever fired, so no forfeiture has ever been observed; stated honestly, this candidate answers a falsifier, not a pain.
- **Falsifier:** If degraded-mode output is systematically not worth banking, the ladder only delays the stop and adds spend — auditable by tracking whether banked degraded output is ever consumed.
- **Differs from:** L6-25 contains "(or degrading)" as four words with no mechanism; **no round-1 candidate specifies the *response policy* to a breached ceiling.** This is that policy.

**`R2-1-08` — Waste priced in the same currency as spend**
- **Ability:** Work that buys no forward progress — re-reads of already-read artifacts, repeated failed calls, post-completion calls, corrections of prior output, the full spend of abandoned runs — is metered, priced in the same unit as spend, and attributed to its cause class, observable as a cost-of-poor-quality figure beside every run's cost figure.
- **Concern:** Cost (meter/attribute — on the axis round 1 never metered; spans Self-improvement).
- **Mechanism:** Cost-of-poor-quality accounting (Juran; manufacturing scrap/rework ledgers): failure cost becomes comparable to prevention investment only when both are in currency. Every listed class is already mechanically detectable — P-20's re-read counts and P-21's 14.8% were extracted mechanically in retros; P-03's write-off is a run total.
- **Inference surface:** Zero for the listed classes (event patterns); attributing an event to a cause beyond its class may be a leaf, deferrable.
- **Incumbent delta:** C — opcost meters gross spend only; no waste taxonomy exists anywhere.
- **Evidence:** P-20 (4/4 runs — counted repeatedly, priced never), P-21, P-03. **Cost *was* being measured on the wrong axis — gross consumption rather than waste share.**
- **Falsifier:** If COPQ is a small stable fraction of spend (<~10%, flat), the ledger motivates nothing prevention wasn't already worth — the first harvest settles it.
- **Differs from:** L1-32 detects exceedance *events* for trend screening; L4-26 makes the archive queryable. Neither converts waste into currency on the same line as spend — and the pricing is the substance, because it is what lets triage weigh a harness ability against the waste it removes.

**`R2-1-09` — Unit economics: cost per unit of value**
- **Ability:** Every value-unit the garage produces — a proven node, a routed-in capability, a closed run's deliverable — carries the cumulative spend that produced it, observable as standing figures (cost-per-proven-capability, cost-per-routed-candidate) on the theme surface.
- **Concern:** Cost (attribute — to value, not to work; spans Self-improvement).
- **Mechanism:** Activity-based costing (Kaplan): allocate metered activity to outputs rather than organizational units. The allocation keys already exist — runs, findings, and filed nodes are linked by run-id tags.
- **Inference surface:** Zero given run-id linkage; allocation policy is configuration.
- **Incumbent delta:** C — spend has never once been joined to output (P-17 upstream; the output side of the join exists in the graph).
- **Evidence:** P-26 restated economically: 8 runs, ~5 weeks, one `proven` node not produced by us — **the garage's unit cost is currently undefined and no surface says so.**
- **Falsifier:** If value-units stay too rare for the figure to move any decision (n=1 proven), it is a vanity ratio until the funnel flows — which is itself the honest first reading: the figure's first job is to make the zero-throughput streak an economic fact on a surface instead of a concession in a SCOPE (§8).
- **Differs from:** L4-28 rolls up to run/role/step/tenant — units of *work*; L6-30 computes run outcomes but never their price. The spend × output join exists nowhere in round 1.

**`R2-1-10` — The agent's own fuel gauge**
- **Ability:** Each unit has its remaining budget and current burn rate available to it at step boundaries, observable as the figures present in its context record and as a measurable behavioral difference between meter-aware and meter-blind runs.
- **Concern:** Cost (steering signal, explicitly not enforcement; spans Context provisioning).
- **Mechanism:** Consumption feedback (smart-meter in-home displays: measured 5–15% reductions; the taxi meter's fare visibility). **Deliberately not C-4-shaped:** no guarantee is claimed — guarantees live in R2-1-06/L2-16; this is the information layer that makes economizing *possible at all*. Today an agent could not economize even in principle: it has no number. Quota is hidden (P-15) but session spend is countable and the injection channel already runs live.
- **Inference surface:** Zero to provide the number; the behavioral response is the model's — and is exactly the measured quantity.
- **Incumbent delta:** B — injection live (W0-b #7/#8), number extractable (#26); never joined.
- **Evidence:** none direct (no agent has ever seen a meter); FP-4 inverted — every cost containment in the record was the owner's attention, and this is the cheapest inward delegation of it.
- **Falsifier:** If meter-aware runs show no consumption difference — or Goodhart the visible number — the gauge is dead weight; the A/B is cheap and kills it cleanly. Stated plainly: **C-4 bounds this to a tendency forever.**
- **Differs from:** every round-1 cost candidate places the meter *outside* the agent (enforcement or reporting); none makes the reading an input to the agent. L2-19's ledger governs knowledge context, not budget state.

---

## 3. Sub-areas closed (round 1 suffices; nothing new added)

| Sub-area | Covered by | Note |
|---|---|---|
| Raw metering | opcost (W0-b #26, **A**) | Solved in-house; not re-derived. |
| Attribution to work units | L4-28, L5-22, L1-28 | Closed pending **A-10**. R2-1-09 is a different axis (value units), not a reopening. |
| Mid-loop halt enforcement | L5-21, L1-27, L3-25, L6-25 | Closed *as a question* pending **A-1**; additions only route around A-1 (R2-1-06) or supply the family's missing response policy (R2-1-07). |
| Hierarchical budgets, quota partitioning, shared-limit fairness | L4-29, L4-30, L3-27 | Nothing to add. |
| Post-completion spend refusal | L2-33, L3-26 | Nothing to add; R2-1-08 *prices* that window, distinct from refusing it. |
| Fleet-scale statistical prediction | L4-31 | Correct at its scale; wrong only in the implication that nothing exists below it — §1's verdict, not a new candidate. |
| Estimate-vs-actual calibration bookkeeping | L6-26, L1-29, L5-23 | Closed; round-2 candidates change what the estimate is *derived from*, never the bookkeeping. |
| One-shot precommitted stop criteria | L1-30 | Closed; R2-1-04 differs by recurrence and default polarity. |
| The provider wall | P-15, W0-d §5 | Honored throughout: no candidate touches subscription-quota visibility; all metering rests on transcript-countable tokens (P-16's distinction). Anything gate-dependent cites A-1/A-2/A-10 and routes `needs-a-probe` per §11. |

## 4. Emergent concerns

**None proposed.** Two engagements:

- **E-1 — additional population, supporting promotion without depending on it.** The budget envelope is a *declaration*: spend-vs-envelope reconciliation, tranche releases (R2-1-04), bound admission (R2-1-02), and quote-vs-actual scoring are all declared-at-t0/checked-at-t1 machinery — the same shape as L2-02's write allowance. Each candidate files cleanly under Cost regardless, so nothing rides on the promotion.
- **Considered and rejected: "value accounting / output economics" as a ninth concern** (prompted by R2-1-08/09). Fails §3.3 test 2 — it re-cuts Cost (attribute) + Self-improvement (outcome measurement). Filed as capabilities. One wording note for the next frame, short of a concern: **§3.1's Cost definition silently scopes to gross consumption**; the record's most expensive cost events (P-03, P-16, P-20) were waste and error, which are also resource use. A definition clarification, not a new box.

**Flag for the leader:** three candidates carry falsifiers **testable retroactively against transcripts already on disk before anything is built** — R2-1-01's unit-variance test, R2-1-05's CPI-stability test, R2-1-06's spawn-vs-in-turn spend split. Probe-queue material of the cheapest possible class, cheaper than A-1, and worth surfacing at W6 so triage sees them as near-free evidence.
