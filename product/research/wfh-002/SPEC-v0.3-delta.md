# SPEC v0.3 — delta over v0.2 (wfh-002)

> **⚠ SUPERSEDED (2026-07-25) by `FINDINGS-W6-architecture.md`.** The owner's W6 re-assessment
> chose the hybrid (Option C): the graph *declares*, the queen *evaluates*. The three additions
> below collapse into a **single `branches_on` seam** — floor, cost-cap, and loop-condition become
> three rules the queen evaluates, not three ontology constructs. Retained as the reasoning trail;
> do not build from it. See W6 §6.

**What this is.** The three structural additions the W5 second-domain round-trip said the vocabulary
needs before a template hardens it (`FINDINGS-W5-domain-agnosticism.md`, gaps G-W1/G-W2/G-W3),
worked through with the owner on 2026-07-24 and folded into his framing. This is a **delta**, not a
rewrite: v0.3 = v0.2 (the W1 spec + the W2 fixes) **plus** the three additions below.

**Status:** structure-only. No grades asserted, no artifact attached, firewall untouched. The five node
types and four edge types of v0.2 are **unchanged**; v0.3 adds root-level declarations and a small
number of fields. Principles P-A (control semantics), P-B (opaque bodies), P-C (definition plane, not
runtime) all hold.

---

## 0. The governing principle (owner, 2026-07-24)

> **The vocabulary branches only on binary predicates — is the floor met? is cost over the cap? has
> coverage gone dry? Never on a rated scale. Anything that needs judgment on a spectrum is a human
> review, and stays out of the type system.**

This is the through-line of all three changes. It is *more* domain-agnostic than a graded ladder, and it
keeps the firewall honest: binary condition in, binary verdict out. Rated/subjective assessment is a
human gate, deliberately un-typed.

---

## 1. Change — named binary criteria (floor + north-star). Closes G-W1.

**What v0.2 could not say.** The method's central object — *how sure are we* — collapsed into prose
inside a gate's predicate. The firewall gate's whole rule ("advance only on a real artifact at altitude")
was an untyped string; you could see *that* there was a mandatory gate, not *what it tested*.

**The correction (owner).** "How sure are we" is the wrong question — it imports a rated scale nobody
wants to maintain. What a target actually has is **two binary bars**:

- a **floor** — met or not; meeting it means the capability can be *advertised*;
- a **north-star** — also binary, plainly higher reach;
- **between them: subjective human review, deliberately un-typed** (no rungs, no rating).

**The floor *is* the firewall.** "Floor met = advertisable" is exactly "proven = real artifact attached at
altitude, demonstrated by us." So this does not add a concept — it makes the proof bar a **first-class,
named, binary criterion** a gate can point at, instead of burying the rule in prose. The old `partial`
grade stops being a typed rung and becomes what it is: *floor not met yet, human's read on progress.*

**Spec change (field-level).**

- **New graph-root block `criteria`** — the named binary conditions the workflow branches on:

  | field | type | notes |
  |---|---|---|
  | `name` | string | referenced by gates / steps / loops |
  | `kind` | enum | `floor` \| `north-star` \| `coverage` \| `cost-cap` \| `other` |
  | `of` | ref | the target it judges (a capability/goal in the *knowledge* plane, referenced, not owned) |
  | `test` | markdown (opaque) | the actual bar — **stated as a binary met/not-met condition**, byte-preserved (P-B) |

  A criterion is always binary. Its `test` prose is still prose — but it is now a *named, typed, binary*
  criterion attached to a target, not an anonymous string inside one gate. The workflow declares *what
  conditions it branches on* (definition plane); it does **not** model the domain data behind them (P-C).

- **New field `branches_on: [criterion-name…]`** on `gate` and `step`. The firewall gate becomes
  `branches_on: [floor-of-<capability>]`; a north-star check is a second gate `branches_on:
  [north-star-of-<capability>]`. A query can now surface "which gates test which bar" — the state
  machine is visible without a rules engine inside the vocabulary.

**Explicitly rejected:** a 6th node type; a graded-state enum (`missing/claimed/partial/proven`) as
typed structure. The middle of the ladder is human-subjective and stays out of the type system.

**Honest ceiling.** This makes the *branch structure* visible, not the *exact rule*. The firewall's boolean
stays prose in `criterion.test`. Modeling the full logic would mean a rules engine in the vocabulary,
which breaks P-C. This is the proportionate fix and the honest limit.

---

## 2. Change — cost accrual + roll-up (budget deferred). Opens G-W2, first layer only.

**What v0.2 could not say.** A standing resource constraint had no home; it got mis-typed as a discrete
checkpoint.

**The correction (owner).** Budget is the right long-term goal, but **model cost first**: every action has
a cost, the overall cost is tracked, and there are **multiple levels of cost that roll up** — action → step
→ phase → goal. Budget (a *cap* you compare cost against) is a later layer built on top.

**This splits cleanly across our definition/runtime line.**

- **Definition plane (in v0.3):** *what* we count and *how it aggregates* — declared once at root. The
  roll-up path is the composition tree the vocabulary **already draws** (`invokes`, composite → child),
  so this costs almost nothing structurally.
- **Runtime plane (out, per P-C):** the actual accrued amounts. Sourced from telemetry
  (`context_cycle_review`, transcripts), not authored.

**Spec change (field-level).**

- **New graph-root block `cost_model`:**

  | field | type | notes |
  |---|---|---|
  | `dimensions` | list of `{name, unit, rollup}` | e.g. `{tokens, count, sum}`, `{dollars, usd, sum}`, `{wall-clock, seconds, max}` |
  | `rollup` (per dimension) | enum | **`sum`** \| **`max`** — **roll-up is not always "add."** Tokens/dollars sum up the tree; wall-clock takes the max across parallel branches (two things running 5 min in parallel is 5 min of clock, not 10). |

- Cost accrues on every `step` (runtime) and aggregates along the composition tree per each
  dimension's `rollup` rule, up to the goal. No new per-step field is required to *declare* this — it is a
  property of the tree; the root `cost_model` names the dimensions.

**Deferred to a later layer (documented, NOT built in v0.3):** **budget** = a `cap` per dimension
(optionally scoped to a sub-step, e.g. a feasibility-only cap) + a gate `trigger: cap-breach` referencing
a `kind: cost-cap` criterion. Named here so the shape is known; out of scope until cost tracking exists.

---

## 3. Change — bounded loop with escalate-to-human. Closes G-W3.

**What v0.2 could not say.** "Keep going until nothing new turns up" is a loop; v0.2 had only straight-line
ordering (`depends-on` is an acyclic DAG). The W2 bounded-retry is a different shape.

**The correction (owner): the loop must be able to give up loudly.** It cannot spin forever and it cannot
stop silently. Three exits:

- **Clean exit** — the done-test flips true (coverage has gone dry) → success.
- **Give-up exit** — it isn't converging. Cap at **2 strikes**, then **escalate to a human** (notify; hand
  them the call: continue / redirect / kill). A **strike** = one full rework round that still fails to clear the
  coverage bar (the human cannot confirm "we've covered it").
- **(later)** cost cap tripped — halts (the deferred budget layer, §2).

**This merges what W5 split.** W5 called the loop and our existing "rework ≤2 → escalate" *different
shapes*. They are the same: the loop's ceiling **is** the strikes-and-escalate we already run on the
coverage gate (`failure_handling: {retries: 2, escalation: SCOPE-FAIL}`). So v0.3 invents no new failure
mechanism — the loop **borrows the existing one**. The only genuinely new piece is the
*repeat-body-until-done* part.

**Spec change (field-level).**

- **New field `loop` on a composite `step`:**

  | field | type | notes |
  |---|---|---|
  | `body` | ref | the child step(s) that repeat |
  | `until` | criterion-name | a **binary** `kind: coverage` criterion (§1) — the clean-exit test |
  | `on_no_progress` | `{strikes, then}` | `strikes` (int, **default 2**); `then: escalate` |
  | `escalate_to` | agent-def ref | a `kind: human` principal (v0.2 S6 human-principal) |

- The loop reuses gate `failure_handling` semantics rather than a parallel construct. It is bounded
  (strikes) and never silent (escalation). It is **not** "the model decides to loop" — it is the harness
  running a declared, capped loop, which is exactly the deterministic control-flow the queen owns
  (strengthens the determinism story, not weakens it).

**Wired loose end (not a new build item).** The escalation points at a human on a channel — the
human-as-actor (v0.2 S6) and the Issue-as-conversation (W5 G-W5) residues. They are *why* those
pieces exist; the loop references them. Optional minor marker `tool.kind: channel` may tag the Issue as
a stateful bidirectional medium; deferrable.

---

## 4. Parked / flagged (not folded without owner sign-off)

- **G-W4 — reflexive plane-isolation.** Out of the workflow-definition plane (it is a property of the
  *operated-on* knowledge graph). **Documentation only, no node change.**
- **G-W5 — Issue as stateful human channel.** Referenced by §3's escalation; optional `tool.kind:
  channel` marker. Minor; deferrable.
- **G-W6 — SDLC-worded definitions/enums.** The *renaming* (type names, `arbiter: program|human|agent`
  → neutral words) is **parked by owner** — agnostic meaning under familiar names is acceptable for
  now. **One adjacent sub-item is structural, not cosmetic, and is OPEN pending owner review:** make
  the leaf enums (`tool.provider`, `tool.side_effect_class`, `gate.arbiter`) **open / extensible** rather
  than a closed software-only set, keeping SDLC values as *examples*. That is the difference between "a
  non-software instrument cannot be expressed" and "it can." Flagged for the concept-by-concept review.

---

## 5. What did NOT change (firewall + scope integrity)

- The **five node types** (`skill · agent-def · step · gate · tool`) and **four edge types** (`invokes ·
  depends-on · gated-by · injects`) — unchanged. v0.3 adds **zero node types and zero edge types**;
  it adds two graph-root blocks (`criteria`, `cost_model`), one gate/step field (`branches_on`), and one
  step field (`loop`).
- **P-A / P-B / P-C** — intact. Everything added is definition-plane; runtime amounts and domain data
  stay out.
- **Firewall** — no grade moved, no `proven` asserted, no artifact attached. The ontology node stays
  `grade:claimed`. v0.3 is desk-work; it earns nothing on the firewall until a template is built and
  demonstrated (W4).
