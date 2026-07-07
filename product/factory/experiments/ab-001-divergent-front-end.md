# AB-001 — First reflexive A/B: the divergent front-end

**Status:** DESIGNED · not yet run · authored 2026-07-01 (design session)
**Realizes:** proposal `proposals/bidirectional-multi-goal-methodology.md` §7 + graduation checklist §9.
**Advances:** factory capability **#66** (improve-own-workflow, reflexive/telemetry-proven) — mission
objective 3. This experiment *is* the first real exercise of the reflexive loop.
**Firewall:** the A/B result is the artifact. A method change advances to `proven` **only** if this
experiment (a real, demonstrated-by-us comparison) shows it; otherwise it stays `claimed` or becomes a
`lesson-learned`. No status moves on assertion.

---

## 1. Purpose (in priority order)

1. **Prove the reflexive loop runs end-to-end.** Can the factory measure a real yield/cost delta from
   **one** controlled method change, and act on it under its own firewall? Until this works, every
   extension in the proposal is unfalsifiable `claimed`. This is the primary deliverable — *the loop
   working* matters more than the specific verdict.
2. **Test one real lever:** the divergent front-end (proposal §2).
3. **First multi-goal exercise** (secondary): #92 is a *distinct* goal from shd — this is the first
   time two research goals are live, so it also shakes out the "graph-definitive / briefing-
   associative" model (proposal §1; open-Q #4).

> Keep these in order. Do **not** bundle the scout arm (§3) or the budget governor (§5) into this run —
> multiple levers at once destroys attribution. One lever.

## 2. The lever (independent variable)

**Divergent front-end** = a `framing` phase *before* `decompose` (proposal §2): landscape/product
scan → whitespace/inversion pass → forced narrowing gate → carry one framing forward. Everything else
is held at the current baseline flow (wf:v0.9): same coverage rule, same roles, same gates.

- **Control (A):** baseline wf:v0.9 — scope → decompose → tech-discovery → synthesis. No framing phase.
- **Treatment (B):** baseline **+ the framing phase** inserted before decompose.

## 3. Vehicle — a BOUNDED SLICE of #92 (not the full vision)

Full #92 (the whole platform vision) is too large and is build-deferred (D10) — wrong size for a first
A/B. Run instead a **single contained sub-question**: the **wedge** — *"enforced egress + a complete
audit trail"* framing/landscape — **directional** (no hardware, no build; structure-only).

Why this vehicle:
- **Real** — advances #92's actual wedge (not a synthetic goal).
- **Cheap enough to run twice** — bounding the scope makes the *clean* single-lever design (same goal
  slice, run A then B) affordable. Bounded slice + run-twice = clean **and** cheap.
- **Multi-goal for real** — #92 ≠ shd, so it exercises the portfolio/isolation model as a side effect.

## 4. Design

- Same bounded goal-slice, run **twice**: once under Control (A), once under Treatment (B).
- **Single lever** — the only difference between the runs is the framing phase. Hold roles, coverage
  K/N, gates, and operator constant.
- Tag **every** node produced by each run with its run-id (e.g. `ab001-A`, `ab001-B`) — the per-run
  yield query depends on it (validated on shd-005, OBS-8).
- Run order/independence: B sees the framings A could not (that's the point); to limit "second run
  knows more" contamination, keep A's and B's *research* partitions identical — only B's **framing
  phase** differs. Note residual order-effect as a validity threat (§6).

## 5. Metrics — only what the platform can measure TODAY

Token-level cost telemetry does **not** exist yet (proposal §5); use proxies. Yield-by-tag works now.

| Metric | Source (works today) | Reads on |
|---|---|---|
| findings / run | `context_lookup(tags:["ab001-A" \| "ab001-B"], category:"finding")` | throughput |
| technologies claimed / run | `context_lookup(tags:[…], category:"technology")` | option-space found |
| **distinct framings surfaced** | count `position` findings from the framing phase (B only) | **the lever's whole point** |
| alignment ratio | # nodes attributed into the goal subgraph via edges ÷ nodes produced (reachability, §1) | drift / relevance |
| cost **proxy** | `cycle_review` records + phase durations + agent count + wall-clock | efficiency (until §5 tracker exists) |

## 6. Decision rule (pre-registered — decide BEFORE running)

**Front-end is "better" (→ advance the enhancement toward `proven`) iff:**
- B surfaces **≥1 material framing or whitespace that A did not** (the step-function the front-end
  exists to catch), **AND**
- B's alignment ratio is **not worse** than A's (divergence didn't cause drift), **AND**
- B's cost proxy is within a pre-agreed band of A (e.g. ≤ ~1.5× — the framing phase should be cheap).

- **All three met** → the A/B is the `proven_by` artifact for the front-end enhancement; lock the
  `framing` phase as a decision (D13+) and fold it into the runbook; bump `wf:`.
- **Not met** → `lesson-learned` (front-end didn't pay off *for this goal type*); revise or drop.
- **Either way** → #66 advances the moment the *loop itself* produces a defensible verdict, because
  that proves reflexive measurement works — independent of which way the lever falls.

## 7. Threats to validity (state them; don't hide them)

- **n = 1 goal, 1 operator** — proves the loop runs, not a statistically strong result. First A/B is a
  mechanism proof, not a law.
- **Order effect** — B runs after A on the same slice (§4). Residual; noted, not eliminated.
- **Cost is a proxy** — no token tracker yet (§5). Real cost-per-proven awaits that build.
- **Yield-by-tag is a convention, not engine-native** (§10.4) — depends on the curator tagging every
  node. If a node is untagged, it's invisible to the delta.

## 8. To run this in a FRESH session (the handoff — and a dogfood test)

The design lives here + in the graph, **not** in the prior chat (per proposal §1: artifacts are the
record, chat is associative). A clean session should execute it from:

1. `/factory-onboard` — derive current status from canonical sources + live graph.
2. Read `proposals/bidirectional-multi-goal-methodology.md` (the framing phase = §2; why = §0/§1).
3. Read **this spec**.
4. Scope the #92 wedge slice → `product/research/{id}/SCOPE.md` + a GitHub Issue (D2/D4).
5. Run **Control (A)**, then **Treatment (B)**; curator tags every node with the run-id.
6. `cycle_review` both runs; compute the §5 deltas; apply the §6 decision rule; record the verdict as a
   `factory` finding (the A/B result) + advance/park #66 accordingly.

> If a fresh onboarded session **cannot** pick this up and run it from these artifacts alone, that gap
> is itself a `factory-retro` lesson — the "artifacts are the system of record" principle failed, and
> that finding is as valuable as the A/B.
