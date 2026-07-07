# Proposal — Bidirectional, Multi-Goal, Divergence-Fronted Factory

**Status:** PROPOSAL · provisional · surfaced in design session 2026-06-28 · author: human + Claude
**Firewall:** this document moves *structure/narrative only*. Nothing here is `proven`, `locked`,
or in Unimatrix yet. Each extension stays `claimed` until a telemetry A/B proves it (§8).
**Graduation path:** this file (narrative) → curator distills a `lesson-learned` + `factory`
enhancement nodes → locked items become **D13+** in `decisions.md`. See §9 below.

---

## 0. The thesis

The factory as built is **single-goal, demand-pull, and convergent**:

- **Single-goal** — every workflow assumes one goal; the frontier query (§6) is single-goal.
- **Demand-pull** — work flows goal → decompose → hunt technologies *to serve a capability*.
  Technologies only enter the graph because a capability reached out and pulled them in.
- **Convergent** — a run starts focused (a scoped question) and *stays* focused to synthesis.

This is disciplined and it works for proving a known question. But it has three structural gaps
(all surfaced by real runs), a lifecycle gap, and a missing enforcement substrate:

1. **No divergent front-end.** The funnel has a narrow mouth. The only divergence mechanism
   (goal-owner under-reach check, #59/OBS-4) sits at *synthesis* — the most expensive place to
   discover you framed it wrong. Divergence is evaluative ("did we under-reach?"), never
   generative ("what else could this be?"). **Already bit us once:** shd-005's platform reframe
   (#92) came from a market scan a *human* had to inject mid-run (OBS-8); the factory didn't
   generate it.
2. **No supply-side intake.** §5 describes the supply side (technologies are program-scoped,
   reusable, the library compounds) — but §7/§14 only ever enter from the demand side. There is no
   process by which a technology enters because it *appeared and looks promising* and then goes
   looking for a goal to serve.
3. **Single-goal operating model over a multi-goal data model.** The graph already supports many
   goals (multi-`Advances`, capability→capability `Prerequisite`, a shared technology library).
   The *workflow* does not.
4. **"Blocked" is treated as an exception.** shd's proof column is hardware-blocked, so the *whole
   factory* reads as stalled. Walls are not one-offs — they are the normal state of research until
   a gap is solved.
5. **Budget is assumed, never enforced.** The methodology says "within budget" throughout (§1, §7,
   §14.6) and sources cost from a hand-waved "orchestrator ledger" (§10.4) — but there is no token
   tracker and no governor. Every budget discipline in this proposal rests on a mechanism that does
   not exist.

This proposal extends the factory to **multi-goal, bidirectional (demand-pull + supply-push), with
a divergent front-end, all metered by a token-budget governor**, governed by one principle (§1) and
the existing firewall throughout.

---

## 1. Governing principle — the graph is definitive, briefing is associative

The load-bearing idea that makes the rest safe:

> **The graph is the definitive record of a goal's alignment and achievement. Briefing is a soft,
> associative surface that may cross any boundary — and that is a feature, not a leak.**

| | Briefing | The graph |
|---|---|---|
| Nature | soft, associative, may cross goals/planes | hard, typed, definitive |
| Role | *surfaces* candidates (reuse, serendipity) | **records** alignment & achievement |
| Counts toward a goal? | no — until an edge attributes it | yes — membership in the goal's subgraph |

A finding or technology that surfaces in a briefing is **context, not achievement**, until the
curator draws a typed edge connecting it into the goal's subgraph. **The edge is the act of
attribution.** This is the firewall philosophy applied one altitude up:

> *briefing : graph :: literature : proof* — soft signal never counts; typed structure is truth.

**Consequences:**

- **Alignment = reachability.** "Is this work aligned to goal G?" = "does its node connect into
  G's subgraph via valid `Advances`/`About`/`Prerequisite` edges, and does it move G's frontier?"
  This upgrades the goal-owner relevance gate (#59) from *judgment* to a **graph query** (the
  step-function/drift nuance stays advisory; the relevance check becomes mechanical).
- **We do NOT try to isolate briefing.** The earlier worry ("goal-A's briefing might bleed goal-B
  content") is retired: bleed is expected and useful. Rigor lives in **edge discipline**, not in
  retrieval purity.
- **Decomposition's bar rises (see §6).** A goal whose subgraph is vague cannot track alignment at
  all — every briefing hit looks arguably-relevant and drift is undetectable. "Well-defined graph"
  is the precondition for everything here.

---

## 2. Extension 1 — A divergent front-end (the funnel mouth)

**Convergent vs divergent breadth.** The factory already fans out (parallel researchers,
loop-until-dry) — but that is *coverage* breadth inside an already-accepted framing. What's missing
is *framing* breadth: competing definitions of the problem itself, generated before commitment.

**New phase before `decompose` — `framing`:** mirror the compete→select lifecycle the factory
already runs on *technologies* (§2), one altitude up, on *problem framings*:

1. **Generate** N competing framings — deliberately contrarian/orthogonal: by-inversion ("what if
   the constraint is wrong"), by-analogy ("how does another domain solve this"), by-first-principles,
   by-step-function (10× not 10%), by-"is this even the right problem." Each is cheap: a paragraph +
   what it buys + what it bets on + **how you'd kill it.**
2. **Grounded divergence via a landscape/product scan** (the engine for step 1). Existing products
   are *framings that already survived contact with reality* — a finite, falsifiable set, not
   infinite brainstorming. This is what produced #92 in shd-005.
3. **Mandatory whitespace / inversion pass.** A product scan biases toward *incremental* framings;
   step-functions live in the **whitespace no product occupies**. Forced question: *"given what
   they all do — what does none of them do, what do they all assume, and is that gap a moat or a
   graveyard?"* (shd-005's moat was the integrated spine **no** product offered.)
4. **Forced narrowing gate.** Rank framings against goal intent + a "what does it buy / cost" bar.
   Human picks 1 or a small portfolio. **You must exit with ≤N framings and a kill-reason for each
   loser.** This mandatory convergence is what keeps the phase from becoming unfalsifiable
   vision-burn.
5. **Record losers** as `position` findings (D10 architect-for-future) — divergence memory.

**Goal-owner becomes a bookend role:** generate-wide at entry, under-reach-check at exit; the exit
check now *verifies* the entry divergence was honored, instead of being the only line of defense.

**Risk & discipline.** A broad front-end is the classic way disciplined research dies. It is only
safe if it inherits the firewall apparatus: **budgeted, convergent-by-construction, explicit kill
criteria.** Diverge wide → narrow hard → hand one winner to the existing convergent flow.

---

## 3. Extension 2 — A supply-push scout arm (the second intake)

**Inverts the direction of flow.** Demand-pull: goal → hunt technologies. **Technology-push:** a
new capability *appears in the market* → ask **"how could this advance one of our goals — or what
new goal does it unlock?"** Same graph, `Prerequisite`/`Advances` traversed **backward** (tech →
which capability/goal). This is the supply-side intake §5 implies and §7 never built.

**Two speeds — already the firewall's gearbox (D7):**

- **Cheap — directional creative thought** = `directional`: a finding + a "could this matter?"
  position; moves *structure only* (a `claimed` tech node + **hypothesized** goal edges); near-zero
  budget.
- **Real promise → POV** = graduate to `empirical`→`validated`: a bounded eval (Proof of Value),
  then — only if it clears — a POC against a **specific goal's envelope.**

**The firewall holds with zero new rules.** A pushed technology is `claimed` until a POV/POC proves
it *in a real goal's envelope* (§4 envelope rule). The arm **populates and nominates; it can never
inflate status.** That is the safety property that makes a "scan for new tech" arm survivable.

**One scout capability, two intake modes:**
- **Pull** — landscape scan at the *front of a goal run* (§2).
- **Push** — the same scan as a *standing, goal-agnostic arm* that stocks the shelf ahead of demand.

This is also the concrete realization of `mode: open` — the exploratory goal mode the taxonomy
named (§4) but never operationalized.

**Risk & discipline.** A standing "scan for cool new tech" arm is the single best way to destroy
focus — and it *feels* like productivity. Containment:
1. **The question is goal-anchored, mandatory** — "how could this achieve *one of our goals*," not
   "is this cool." No credible path to an existing goal (or a compelling new goal worth authoring)
   → it dies on the spot. The goal portfolio is the filter.
2. **Separate, tiny budget; the POV is the kill gate.** The cheap arm runs on a fixed near-zero
   budget and cannot draw from goal-delivery. POV is where speculation competes for real budget —
   against goal-pull work, on equal terms.
3. **High kill-rate is the health metric, not graduation rate.** A healthy arm kills 95%+ before
   POC. If everything graduates, the gate is broken. Cadenced (scheduled sweep), not always-on.

**Payoff:** the technology library populates *proactively*, so the marginal cost of every future
goal drops — §5 compounding at full strength.

---

## 4. Extension 3 — Multi-goal portfolio + blocked-as-normal

**The data model is already multi-goal; the operating model is single-goal.** §5 makes technologies
reusable across goals; capabilities/NFRs are goal-scoped by design (§4). What's missing is a
**portfolio layer:**

- a **cross-goal frontier** (frontier-of-frontiers),
- **per-goal budgets** (one goal can't starve another; a parked goal's budget isn't burned),
- a **WIP limit** (finite knowledge engine + finite agents — bounded concurrency),
- a **value-weighted scheduler** with first-class blocked handling.

**Blocked is a first-class, granular, condition-tagged state:**
- **Per-phase, not per-goal.** shd's *feasibility* is hardware-blocked, but its discovery,
  synthesis, framing, and scout work are not. **Drain everything a goal can do directionally, then
  park precisely at the blocked gate**, with an explicit unblock-condition recorded (e.g. "unblocks
  when a GPU box exists"). This is what happened to shd — but ad-hoc (Issue tags), not modeled.
- **Multi-goal routes around walls; it does not solve them.** The contrarian risk: a portfolio that
  perpetually flees hard, high-value blocked goals for easy unblocked ones — feeling productive the
  whole time. The scheduler must be **value-weighted, not unblocked-weighted**, with periodic
  re-evaluation of parked high-value goals.

**Sharing — demand is a DAG, not a forest:**
- **Capabilities CAN be shared** (multi-`Advances`; capability→capability `Prerequisite`, §5). Some
  capability nodes are shared hubs; all attach to the shared technology library beneath. Sharing now
  happens at *two* layers — supply (technologies) **and** demand (capabilities).
- **Sharing shares *alignment* (the edge), not *achievement* (status).** A capability proven for
  goal A's `done_when`/envelope is **not** automatically achieved for goal B (same logic as the §4
  technology envelope rule). The edge says "relevant to both"; it does **not** say "done for both."
- **Discriminator:** share a capability **only when its `done_when` is genuinely common** across
  the goals. If A and B need different behavior from "the same" capability, it is *two* capabilities
  wearing one name — a `proven` node that means different things to different goals is a firewall
  blur. **Business capabilities share readily; NFRs share least** ("within budget", N3-style
  sensitivity are exactly the goal-specific properties §4 warns about).

**Composes with D11.** Multi-goal (many goals) and D11 (many machines) are the same axis from two
ends: **goals are the parallel work units; machines are the parallel executors.** Multi-goal is what
*motivates* distribution. And it is not hypothetical — **goal #2 already waits:** the platform-vision
(#92, build-deferred). The portfolio begins forming the moment shd parks on hardware.

---

## 5. Extension 4 — Token budget: tracking + governor

**Budget is referenced everywhere in the methodology and mechanized nowhere.** §1 "within budget,"
§7 feasibility "budget + firewall," §10.4 "budget spent vs cap — *source: orchestrator ledger*,"
§14.6 "autonomous, within budget." The "orchestrator ledger" is hand-waved — there is no tracker and
no governor. And every discipline in this proposal *assumes one exists*: the front-end must be
"budgeted" (§2 above), the scout arm needs a "separate tiny budget" and a POV that "competes for real
budget" (§3 above), the portfolio needs "per-goal budgets" and a "value-weighted scheduler" (§4
above). Without this extension those are unenforceable promises. **This is the enforcement substrate
under §2–§4.**

**Two distinct mechanisms — do not conflate them:**

| | Tracker (monitoring) | Governor (enforcement) |
|---|---|---|
| Question | "how much did we spend, attributed to what?" | "may we spend the next batch?" |
| Nature | observability (telemetry) | control |
| Output | spend per run / phase / agent / goal / arm | allow · degrade · halt |

**Nested budget hierarchy.** A spawn must fit within *every* enclosing cap:
`portfolio total → per-goal allocation → per-scope/run cap → per-phase → per-arm (the scout's separate
tiny line)`. The governor enforces the hierarchy; the tracker attributes spend to each level.

**The governor is a dial, not a wall (firewall-preserving).** A hard mid-run halt wastes everything
spent and yields a half-researched goal with no synthesis. Better: **budget modulates convergence
aggression.** As a cap depletes — tighten loop-until-dry (lower K/N), switch from "explore more" to
"converge on what we have," and at the ceiling **force a synthesis/checkpoint, not a kill.** A
budget-truncated run produces *less structure*, never false *status* — the firewall is untouched.

**Token budget ≠ value (the failure mode to avoid).** A dumb per-run ceiling optimizes for
*cheapness* — it will kill a run 95% of the way to a breakthrough while ten low-value runs each burn
90% of their cap. The real metric is **cost per proven capability** (§10.4), not raw tokens. So the
governor is an *input to the value-weighted scheduler* (§4 above), not a standalone kill switch:
budget buys prioritization, and the cheapest run is not the best one.

**Enforcement point — what's buildable now.** Tokens are spent inside agents; a clean mid-agent
hard-kill may not be a harness capability we have. The realistic v1 enforces at **phase and
spawn-boundary checks**: the leader reads cumulative attributed spend before each phase and before
each parallel spawn batch, and refuses to proceed past the cap (coarse but enforceable today). *(Prior
art: the Workflow tool already exposes a `budget` primitive — `total` / `spent()` / `remaining()` —
that throws when the cap is hit; the factory needs the same contract at run/portfolio altitude.)*

**Attribution dependency — and a three-for-one payoff.** Per-goal / per-arm / per-phase enforcement
requires spend *attributed* to those dimensions — but D6 says attribution does not persist
(`created_by: anonymous`). Token attribution is the **same mechanism** as (a) the platform-wedge
audit trail (#92: "complete audit trail") and (b) the A/B's cost telemetry (§6 below).
**One attributed-accounting mechanism, three payoffs: governor + audit-wedge + reflexive-cost-metric.**
Build it once.

**Where the cap lives.** The scope template (D4) gains a **`budget` field** (per-run token cap); the
goal gains a **portfolio allocation**; the scout arm carries its own fixed near-zero line.

**Staging.** v1 = per-run + per-phase tracker, a scope-level cap enforced at phase/spawn boundaries,
graceful degradation. v2 = portfolio value-weighted allocation + finer per-agent/per-goal attribution
(rides the D6 fix). Don't build the full hierarchical governor before v1 proves the dial works.

---

## 6. Decomposition — the bar this raises

If the well-defined goal-subgraph is the definitive instrument (§1), decomposition's job is no
longer "list some capabilities." It is to make the goal's graph **complete and sharp enough that
alignment is decidable by reachability.** A vague subgraph makes drift undetectable and the whole
portfolio ungovernable. This is a higher quality bar than the current flow enforces, and it is the
precondition for §1–§5 to work.

---

## 7. How it proves itself (firewall on the process plane)

Every extension here is `claimed` until comparative telemetry proves it (§8) — the factory must not
adopt method changes on "it should work," the very thing its firewall forbids on the research plane.

**The divergent front-end (§2) is the natural first reflexive A/B (#66):** run one goal through the
focused-only flow vs. the divergence-fronted flow; compare relevance, yield, and step-function hits.
That closes **mission objective 3** *and* tests this proposal with the same move. The thing we are
proposing and the thing the factory most needs to prove are the same experiment.

---

## 8. Open questions (resolve at draft/distill time)

1. **Edge semantics — finding → upstream.** A landscape/scout finding `Motivates` a *framing,
   capability, or goal*, which is upstream of the current `finding → technology` convention (§5).
   Decide: extend `Motivates` targets, or route framing findings as `position` findings cited by the
   framing decision (the #102 pattern).
2. **POV as artifact/gate.** Is POV a new named phase/artifact between `directional` and the
   validated flow, or a labeled `empirical` scope? Define its template and kill criteria.
3. **Where the portfolio scheduler lives.** A new coordinator altitude above `research-leader`? A
   skill? Its budget/WIP/value policy needs a home.
4. **Goal-isolation validation.** The "graph is definitive, briefing is associative" model (§1) has
   **never run with >1 active research goal.** Validate that alignment-by-reachability holds and that
   briefing association is genuinely harmless before scaling the portfolio. (#92 is the natural
   second goal to test it.)

---

## 9. Graduation checklist

- [ ] Curator distills a `lesson-learned` (origin: shd-005 platform reframe came from a market scan
      a human had to inject — the factory lacked a divergent/supply-side intake).
- [ ] Curator stores `factory` enhancement nodes (`kind: technology`, `claimed`): **framing/landscape
      phase** · **scout capability (pull+push)** · **POV gate** · **portfolio layer** · **first-class
      blocked state** · **graph-as-definitive / alignment-by-reachability** · **token-budget tracker +
      governor** (carries the attributed-accounting dependency shared with the audit-wedge + D6).
- [ ] Run the first reflexive A/B (§7); on a win, advance the relevant enhancement to `proven` and
      lock the corresponding decisions as **D13+** in `decisions.md`.
- [ ] Fold the locked phases into `runbook.md` / the agent contracts; bump `wf:`.
