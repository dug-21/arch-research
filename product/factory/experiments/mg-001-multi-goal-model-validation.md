# MG-001 — Validate the multi-goal MODEL (isolation-by-reachability)

**Status:** DESIGNED · not yet run · authored 2026-07-03 (onboarding/planning session)
**Realizes:** proposal `proposals/bidirectional-multi-goal-methodology.md` §1 (graph-definitive / briefing-associative)
+ §4 (multi-goal portfolio) + **open-Q #4** ("the model has never run with >1 active research goal").
**Advances:** factory maturity toward multi-goal operation. Distinct from **AB-001**, which tests the
*framing lever* and gets multi-goal only as a side effect. MG-001 makes **multi-goal isolation the
first-class, measured objective.**
**Firewall:** structure/narrative only. Nothing here moves `status`. The isolation model graduates from
`claimed` (proposal §1/§4) toward a locked decision **only** on the artifact this experiment produces
(the measured alignment/bleed audit). No status moves on assertion.

---

## 0. Why this before the portfolio build

The factory's **data model is already multi-goal** (goals #3 shd, #92 platform, #19 factory; a shared
technology library; multi-`Advances`). Its **operating model has never run >1 goal** — every run
shd-001…006 was single-goal, single-scope, sequential. The proposal's portfolio layer (§4: cross-goal
frontier, per-goal budget, WIP limit, scheduler, concurrent curators) is a **heavy build that assumes
the model holds.** MG-001 falsifies that assumption **cheaply, before** any of it is built.

**Two sub-questions inside "multiple goals" — MG-001 answers only the first:**

| | (a) Does the MODEL hold? | (b) Can we EXECUTE concurrently? |
|---|---|---|
| Question | alignment decidable by reachability; briefing bleed harmless | scheduler, per-goal budget, WIP, concurrent curators |
| Cost | cheap — one more *live* goal in the graph | heavy build |
| Writer | **single serialized curator** (firewall intact) | concurrent curators → **needs the `agent_id` fix (D6)** |
| MG-001 | **THIS** | out of scope (deliberately) |

> MG-001 tests two goals **present and tracked**, not two goals **executing concurrently.** Concurrency
> is (b); it is gated on durable attribution (`agent_id` declared in the agent def + passed on writes —
> the D6 gap). Do not bundle (b) into this run.

## 1. The lever / variable

None. MG-001 is **not** an A/B. It is a **single directional run of a second live goal**, instrumented
to measure whether the isolation model holds. Everything else is baseline `wf:v0.9`.

## 2. Vehicle — bring #92's wedge live as goal #2, shd parked

- **Goal #2 = #92** (Sovereign auditable agentic platform), already in the graph as `build-deferred`.
  "Live" = a single **directional** research scope opens against its **wedge capability #93** (auditable
  sovereign boundary). No hardware, no build, structure-only.
- **shd stays parked** — blocked-as-normal (proposal §4). shd's proof column is hardware-blocked; MG-001
  does not touch it. This is the realistic portfolio state: one goal parked at a blocked gate, a second
  goal draining directional work.
- **Scope-id:** `mg-001` (= `context_cycle` topic = `feature_cycle` = `product/research/mg-001/`).
  Cross-linked to a GitHub Issue by title (D4). Curator tags **every** node `mg-001` (per-run yield
  query, OBS-8).

Why this vehicle: #92 is a **real** second goal (not synthetic); its wedge is directional-cheap; and it
**already shares structure with shd** — the perfect isolation stress test (see §3, shared node #81).

## 3. What we measure — isolation, using only what the platform measures TODAY

| Probe | How (works today) | Passes if |
|---|---|---|
| **Alignment-by-reachability** | every node the run produces → is it reachable into #92's subgraph via valid `Advances`/`About`/`Prerequisite` edges? `context_graph(mode:"subgraph", seed_ids:[92])` | 100% of the run's own nodes are attributed into #92 (or explicitly parked); **zero orphans** |
| **Briefing-bleed audit** | during reuse-first `context_search`, does **shd** content surface in #92's briefing? For each bleed hit: was it treated as *context* (no edge) or wrongly *attributed* (edge into #92 without justification)? | bleed may occur (expected/useful) but **zero mis-attributions** — no shd node pulled into #92's subgraph without a genuine shared-capability justification |
| **Shared-node semantics** | #81 is `Prerequisite→` C3/#103 (shd) **and** #93 (platform). Read it from each goal's frontier. | #81 shows **shared alignment** (both edges valid) but **unshared status** — proving it for #93's `done_when` does NOT mark it done for shd's C3, and vice-versa (proposal §4 discriminator) |
| **Frontier query under 2 goals** | run the §6 frontier query with two goals live; does it return a correct **#92-only** frontier, or does it need a goal filter? | either it returns clean per-goal frontiers, **or** the required fix is documented as a concrete finding (a real result either way) |

Cost proxy (until a token tracker exists, proposal §5): `cycle_review` records + phase durations +
agent count + wall-clock, tagged `mg-001`.

## 4. Decision rule (pre-registered — decide BEFORE running)

**The multi-goal model HOLDS iff all four:**
1. Alignment-by-reachability = 100% for the run's own nodes (no orphans), **AND**
2. Zero cross-goal mis-attributions (bleed stayed associative, never became a false edge), **AND**
3. Shared node #81 reads correctly per-goal — alignment shared, **status/achievement not shared**, **AND**
4. The frontier query returns a correct #92-only frontier, **or** the exact gap is documented as a
   required portfolio-layer fix.

- **Holds** → the isolation model is the `proven_by` artifact; graduate proposal §1/§4 toward a locked
  decision (**D13**: graph-definitive / alignment-by-reachability); the portfolio *execution* build (b)
  is cleared to proceed on a sound substrate.
- **Fails** → `lesson-learned`: the isolation model needs revision **before any portfolio build**. This
  is the highest-value outcome to catch *now* rather than after building the scheduler on a broken model.

## 5. Threats to validity (state them; don't hide them)

- **Tests presence, not concurrency.** Two goals *tracked*, one serialized curator — this validates the
  *model*, not concurrent execution (b). By design. Do not over-claim.
- **n = 1 second goal, 1 operator.** A mechanism proof, not a statistical result.
- **shd is parked, not actively running.** So "two live goals" here means one active + one parked. A
  fuller test (two *active* goals) awaits (b) and the `agent_id` fix.
- **Yield/alignment-by-tag is a convention, not engine-native** (proposal §10.4) — depends on the
  curator tagging every node `mg-001`. An untagged node is invisible to the audit.

## 6. Relationship to AB-001 and the reflexive loop (#66)

MG-001 and AB-001 are **complementary, and MG-001 should run first:**
- MG-001 proves the **multi-goal substrate** is sound (cheap, no lever, single curator).
- AB-001 then runs the **framing-phase A/B** on the same #92 wedge, knowing isolation already holds — so
  its multi-goal aspect is validated, not a confounded side effect, and it can focus cleanly on the one
  lever + closing reflexive loop #66.

Running AB-001 first inverts the risk: you'd be measuring a framing lever *and* discovering multi-goal
breakage in the same run, unable to attribute which caused what. One variable at a time (AB-001's own §1
rule) argues for isolating the multi-goal substrate test first.

## 7. To run this in a FRESH session (handoff — dogfoods "artifacts are the record")

1. `/factory-onboard` — derive status from canonical sources + live graph.
2. Read `proposals/bidirectional-multi-goal-methodology.md` §1, §4, open-Q #4.
3. Read **this spec**.
4. Scope the #92 wedge slice → `product/research/mg-001/SCOPE.md` + a GitHub Issue (D2/D4),
   Confidence-required: **directional**, out-of-scope: hardware/build/concurrent-execution.
5. Run one directional scope on #93's wedge; curator tags every node `mg-001`; **shd untouched**.
6. Run the §3 probes; apply the §4 decision rule; record the verdict as a `factory` finding
   (the isolation-audit artifact) + graduate/park the model accordingly.

> **Prerequisites to confirm before running:** (i) whether the `agent_id`-in-agent-def write path is
> needed even for a single serialized curator (correction from the human, 2026-07-03) — MG-001 assumes
> **not** (one curator, sequential writes), but confirm the curator's agent def carries a valid
> `agent_id` so its #92 writes attribute correctly. (ii) #92 is `build-deferred` (D10) — opening a
> *directional* scope on its wedge does not violate deferral (directional moves structure only); confirm
> with the human that bringing #92 to *directional-live* is intended.
