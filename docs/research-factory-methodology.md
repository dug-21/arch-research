# Research Factory Methodology

> A methodology for running an **autonomous research factory** on top of Unimatrix.
> The factory takes a *goal*, decomposes it into the business capabilities required to
> deliver it, researches the (often novel) technologies that could deliver those
> capabilities, and validates viability with real artifacts — mostly autonomously,
> within a budget. The Unimatrix knowledge base is the compounding asset: each goal
> enriches a shared, evidence-graded library of what works and what doesn't.

The methodology runs on **two axes** and **two planes**, both governed by one rule (the
firewall, §3):

- **Subject axis** — *is the research done?* A property of a **goal**. Tracked by the
  capability board (§6).
- **Process axis** — *is the factory running better?* A property of the **workflow**. Tracked
  by version-stamped run telemetry (§8).
- **Research plane** — external research goals (the factory's *output*). The default categories.
- **Process plane** — the factory improving itself (its *self*). A single sealed `factory`
  category (§9).

---

## 1. Purpose & operating model

This is a **research factory arm**: you pair with it to set a goal, then it runs structured,
mostly-autonomous workflows (within budget) to research the goal end to end. Goals vary in
character — targeted, exploratory/research-only, POC-required, linked (building on prior
research), or open-ended — and the factory adapts its depth to the goal's *mode* and budget.

The factory is explicitly **not** about delivering tried-and-true solutions. It is about
mapping a problem space and surfacing approaches — sometimes novel, never-before-tried — and
then **proving** which ones actually work. Because it runs autonomously, the methodology's
central safety mechanism is a hard separation between *what we think might work* (structure,
moved freely by research) and *what we have proven works* (status, moved only by evidence).

The **workflow itself is a first-class artifact**: it is versioned in the repo and improved
over time through a self-enhancement loop fed by `lesson-learned` entries and per-run telemetry
(§8). Crucially, the factory improves itself using its own methodology, reflexively — if it
cannot drive its own improvement under its own firewall, the methodology is wrong.

---

## 2. The taxonomy (5 research categories + 1 process category)

The number of categories is not chosen for its own sake. Too many categories cause agents to
**mislabel**; too few cause confusion. The right test is **boundary sharpness** — can an agent
holding an entry decide its category without judgment? Each category below earns its place by
having a **distinct scope and a distinct lifecycle**, which keeps boundaries sharp.

| Category | Plane | Scope | Lifecycle | What it is |
|---|---|---|---|---|
| `goal` | research | one mission | human-authored, stable intent | Why we are investigating. The north-star statement. |
| `capability` (`kind: business \| nfr`) | research | **goal-scoped** | decompose → prove `done_when` | What *this* goal needs to be true. |
| `technology` | research | **program-scoped, reusable** | discover → compete → select → prove → **reuse** | A (often novel) enabling approach that could deliver a capability. Viability-tracked. |
| `finding` | research | evidence | inert; `Motivates` a technology | An evidenced claim extracted from research. Stays out of agent-delivery retrieval until it graduates a node. |
| `lesson-learned` | research | the factory | improves the workflow | Dead ends and process learnings. The fuel for workflow self-enhancement. |
| `factory` (`kind:` mirrors the 5 roles) | **process** | the factory itself | the same methodology, reflexively | The sealed process plane: the factory's own capabilities, enhancement ideas, A/B results, and process lessons. Detailed in §9. |

### Why exactly these

- **`goal` vs `capability`** — intent vs. outcome. Boundary is enforced by *who writes it*
  (humans author goals; agents author capabilities), so agents rarely face this choice.
- **`capability` vs `technology`** — **scope**, not altitude, is the discriminator: *"does this
  belong to one goal, or to the whole program?"* Capabilities live and die with their goal;
  technologies are reusable assets any future goal can pull from. Scope is a far more mechanical
  boundary than "outcome vs. mechanism," which lowers the mislabel risk that motivated keeping
  the set small.
- **`technology` as its own category** — it is the one node type with a *compete → select →
  prove → reuse* lifecycle, and it is **cross-goal**. That difference in both scope and lifecycle
  is what earns it a category rather than a `kind`.
- **`finding`** — inert evidence with different retrieval visibility (it must not flood agent
  retrieval). Distinct visibility ⇒ distinct category.
- **`lesson-learned`** — about the *research process*, not the research subject. Sharp test:
  *"if the research target were completely different, would this still be useful?"* Yes ⇒ lesson.
- **`factory`** — a different *plane*, not a different subject. It must not pollute research
  retrieval, so it is isolated at the category level (§9). One category, not five, because five
  process-categories would re-introduce the bloat we are avoiding; its internal structure lives
  in a `kind` field.

### What is deliberately NOT a category

The single biggest source of category bloat is treating evidence artifacts as nodes. They are
**fields**, following Unimatrix's own rule that `delivered_by`/`proven_by` targets are not graph
nodes:

| Tempting category | Where it actually lives |
|---|---|
| `source` / citation | a `cites:` **field** on a `finding` (the paper/repo is not a graph node) |
| `experiment` / POC | a `proven_by:` **field** on a `technology` (the notebook/repo lives in git) |
| `decision` / position | a `finding` tagged `position` that references the evidence and the governing nfr |
| `synthesis` | a `finding` that cites many sources |
| `method` / `procedure` | the workflow, versioned in the repo (see §7) |
| `task` / `feature` / "actions to implement" | git (commits/PRs) — the work that *flips a capability to `proven`*, not a node |

---

## 3. The firewall (the rule that makes autonomy safe)

> **Status advances to `proven` ONLY on attached, real-artifact evidence.**
> Research, literature, and "it should work" move *structure*, never *status*.

This is borrowed directly from Unimatrix's capability model and is the load-bearing rule of the
whole factory. An autonomous loop that trusts "claimed = done" compounds rubble at machine speed.
It governs **both** axes: subject-proof is an artifact (a POC); process-proof is comparative
telemetry (an A/B). Neither advances on optimism.

Two sub-processes, kept strictly separate:

- **Structural management** — *what capabilities/technologies exist.* Low-frequency, judgment +
  research. Creates/splits/merges nodes, sharpens `done_when`, adds edges. The autonomous arm may
  do this freely within budget.
- **Status management** — *is it proven viable.* Evidence-driven, gated. A `technology` reaches
  `proven` only when a POC artifact is attached in `proven_by`. The arm may **not** do this on
  literature alone.

**Status values** (shared by `capability` and `technology`):

```
missing 🔴  → identified need, no path yet
claimed ⚪  → literature/asserted says yes, unvalidated here (a flag, not a resting state)
partial 🟡  → some evidence, done_when not fully cleared
proven  🟢  → real-artifact evidence clears done_when
```

---

## 4. Entry schemas

### goal
```
category: goal     (human-authored)
name:     <mission, one line>
intent:   <why the program is moving here — 2-3 sentences>
success:  <concrete, measurable; includes strategic constraints>
out-of-scope: <what is explicitly NOT part of this goal>
mode:     targeted | exploratory | poc-required | linked | open   (tag)
```
Goals may link to each other (`Advances` / `Prerequisite`) so research builds on research.

### capability  (`kind: business | nfr`)  — **goal-scoped**
```
category: capability
kind:     business | nfr
name:     business → an OUTCOME a user/operator experiences (never an implementation)
          nfr      → a quality PROPERTY in business terms (cost, sovereignty, privacy, latency…)
why:      one sentence — the problem it solves
done_when: 1-2 BEHAVIORAL, runnable statements (the proof gate AND definition of done)
status:   missing | partial | proven | claimed
proven_by: <real-artifact evidence ref>   (FIELD)
```
- **NFRs are goal-specific.** They are quality properties of *this* mission and `Advances` this
  goal. Another goal decomposes into different NFRs. (Cross-goal sharing via multiple `Advances`
  edges is the rare exception, not the design intent.)
- **Outcome altitude.** Name the outcome, never the mechanism. The HOW is a `technology`.

### technology  — **program-scoped, reusable**
```
category: technology
name:     the enabling approach / mechanism (this IS the HOW — the inverse of capability altitude)
why:      which capability it could deliver, and what makes it promising/novel
done_when: behavioral viability bar — what a POC must demonstrate
status:   missing | partial | proven | claimed
proven_by: "live: <hardware/context>, <result>, <artifact ref>"   (FIELD — captures the envelope)
```
- A technology is **proven within an envelope** recorded in `proven_by`. Reusing it under a
  materially different envelope (different hardware, quality bar, workload) **re-opens it to
  `partial`** until re-validated — the same "proven as of current surface" logic NFRs use.

### finding  — evidence, inert in retrieval
```
category: finding
content:  the evidenced claim (and a position, if it is a selection — tag: position)
cites:    <papers / repos / datasets / docs>   (FIELD — targets are not graph nodes)
```
Findings never author a node and never satisfy one. They `Motivates` a technology (PPR-neutral,
so raw evidence does not flood agent retrieval) and graduate structure, not status.

### lesson-learned  — process self-improvement
```
category: lesson-learned
content:  What happened → root cause → takeaway (the workflow change it implies)
```

### factory  — the process plane (see §9 for the full design)
```
category: factory
kind:     goal | capability | technology | finding | lesson-learned   (mirrors the research roles)
... same fields as the mirrored role ...
```
All `factory` edges connect **factory → factory only**. The subgraph is sealed.

---

## 5. Edges & the demand/supply architecture

The research taxonomy splits cleanly into a **demand side** (per goal) and a **supply side**
(whole program):

```
DEMAND (per goal)                              SUPPLY (whole program)
  goal                                           technology library
   └─ capability (business/nfr) ◀──Prerequisite──┘  (reusable, viability-graded)
        ▲                                          ▲
        │ Advances / About                         │ Motivates
        │                                        finding
```

Edge types (all built into Unimatrix; we map onto them, we do not invent new ones):

| Edge | Direction | Meaning |
|---|---|---|
| `Advances` | capability → goal | this capability advances the goal (PPR-neutral) |
| `About` | nfr → business capability | this NFR governs/constrains that capability (design constraint + regression checklist) |
| `Prerequisite` | technology → capability *(and capability → capability)* | the capability depends on this technology/capability (PPR-positive; source is the prerequisite) |
| `Motivates` | finding → technology | this research shaped this technology (PPR-neutral — keeps findings inert in retrieval) |
| `Supports` / `Contradicts` | finding ↔ finding | corroborating / contradictory claims |

**Edges are entry-level, not category-constrained.** Unimatrix applies edges between entries by
id; it does not restrict an edge type by the categories of its endpoints. So `technology →
capability` `Prerequisite` works natively — the `capability → capability` form is a semantic
convention, not an engine limit. (Confirmed against the engine.)

**Why the supply side compounds.** One `technology` node can `Prerequisite` capabilities across
**many** goals (one node, many edges). Research a technology once; every later goal that needs it
starts from a populated, evidence-graded shelf. This is the concrete mechanism by which the KB
"unlocks value over time" — the technology library is the asset that compounds.

**Competing options are not `Contradicts`.** Sibling technologies under the same capability (e.g.
two compute approaches) are *alternatives resolved by selection*, not contradictory claims. The
selection is a `finding` tagged `position`; losers move `partial → deprecated`. Reserve
`Contradicts` for claims that cannot both be true.

---

## 6. Tracking progress — the capability board & frontier ("what's done vs. not")

"What's been done?" is a **graph query**, not a maintained list. The factory runs it at the
**start of every cycle**; the graph is the durable memory across autonomous sessions.

```
context_graph(mode:"subgraph", seed_ids:[<goal-id>], max_depth:1,
              edge_types:["Advances"], direction:"incoming", detail:"full")
  → the capability set, hydrated in ONE call → read each node's grade → group
    🟢 proven · 🟡 partial · 🔴 missing · ⚪ claimed
```

This is a **single hydrated call**: `subgraph` returns the neighbor *nodes* (content + tags), not
just edges, and honors the `edge_types`/`direction` filter — no separate status fetch, no client-side
join. (`neighbors` mode returns edges only, even at `detail:"full"`; use it when you want the topology,
`subgraph` when you want the nodes. Both are live at depth 1; depth>1 reads the tick-cache.) Read the
firewall grade from each node's **`grade:<missing|claimed|partial|proven>` tag** — the queryable
projection of the grade, written by the curator (§14.1). It is **distinct from the entry's lifecycle
`status` field** (`active`/`deprecated`), which is a different axis; do not conflate them. To pull the
`technology` children in the same call, add `Prerequisite` to `edge_types` and `max_depth:2`.

But "done" has **two axes** and you must read them together. The **grade** answers *delivery*-done; it
does not tell you whether a capability has even been *researched*. That you read from whether it
has `technology` children and what *their* grade is. The pair yields a precise pipeline state —
**derived, never stored** (a stored `researched: true` flag would drift from reality; the `grade:` tag
is not such a flag — it mirrors the firewall grade the curator already sets, updated in the same
`context_correct` that moves it):

| Capability state | What you see in the graph | Done so far | Next action |
|---|---|---|---|
| **Unresearched** | 🔴 missing, **no** technology children | nothing yet | `tech-discovery` |
| **Researched** | 🔴/⚪, has technology children, all `claimed` | candidate HOWs found, none proven | `feasibility` / POC |
| **Validating** | 🟡 partial | POC underway, `done_when` not cleared | finish the POC |
| **Proven** | 🟢, ≥1 technology `proven` | done, with an artifact | — |
| **Blocked** | any, but an unmet `Prerequisite` capability | can't start | wait on the prereq |

The **actionable frontier** = `{unresearched, researched, validating}` minus `{blocked}`. That
set *is* the autonomous loop's work queue; it shrinks only when a capability hits 🟢, which the
firewall guarantees means a real artifact.

**Two honesty caveats:**
1. **"Researched enough" is a judgment, not an artifact.** Unlike delivery-done, research-done
   has no artifact. Close it with a **coverage rule** — *loop-until-dry*: stop researching a
   capability when K consecutive searches surface no new technology **and** ≥N independent
   findings corroborate the leading candidate. An **agentic evaluation** proposes "sufficient";
   a **human** confirms at the synthesis checkpoint. K/N are workflow parameters, tuned by
   `lesson-learned` over time.
2. **The capability set is never assumed complete.** Decomposition is itself research and can
   miss a capability. The board answers "what's done" *against the currently-known set*; gaps get
   added as new 🔴 nodes whenever a run, retro, or dogfood surfaces them. "Done" is always "done
   relative to what we currently know we need."

---

## 7. The workflow (first-class, self-enhancing)

A research run is a Unimatrix **cycle** (`context_cycle`, `topic: "<run-id>"`, e.g. `shd-001`).
The workflow definition lives in the repo as a versioned protocol + skills — it is an artifact
with a history, not a hardcoded behavior — so it can be improved over time.

**Scope unit (D2 — see §15).** A goal does not run as one goal-wide cycle; it runs as a set of
**scopes**, each its own cycle (`topic`) and GitHub Issue: one **decompose-scope** (`scope`→
`decompose`, producing the capability board) then one **research-scope per capability**
(`scope`→`tech-discovery`→[`feasibility`]→`synthesis`). The phases below define each scope's
lifecycle — a decompose-scope uses the first two; a research-scope uses the rest.

Phases (each closed with `context_cycle phase-end`):

| Phase | What happens | Gate |
|---|---|---|
| `scope` | confirm goal, success criteria, budget, mode | human pairing |
| `decompose` | research → business `capability` + `nfr` nodes (`missing`/`claimed`) | — |
| `tech-discovery` | research options → `technology` nodes (`claimed`), `finding`s w/ `cites` | coverage rule (§6) |
| `feasibility` | build POCs → move technologies to `proven`/`partial` | **budget + firewall** (only phase that spends real compute) |
| `synthesis` | `position` findings; mark capabilities `proven` where `done_when` clears; report | human review |

**`context_cycle` is the connective tissue — not bookkeeping.** It is the single component that
binds the repeatable workflow to retrieval *and* telemetry. The `goal` sentence passed at
`type:"start"` is **load-bearing**: briefing is goal-conditioned and pulls that sentence to steer
what knowledge surfaces during the run (which is also what keeps the planes apart — §9). The same
cycle declaration binds every entry stored during the run to its `topic`, which is what
`cycle_review` (§10) later analyzes, and it advances the phase signal that drives
phase-conditioned retrieval. A run that skips or weakens its `context_cycle start` gets worse
briefings *and* loses its telemetry. **Declare it first, with a specific goal sentence.**

**The self-enhancement loop** mirrors a retrospective: after each run, ask *"what wasted budget,
missed findings, or chased a dead end?"* and write `lesson-learned` entries. Those lessons drive
edits to the protocol file itself. Lessons are the fuel; the versioned protocol is the thing that
changes. How we know a change *helped* is the process axis (§8), proven by telemetry (§10).

> The **operational mechanics** — the coordinator/specialist split, the single-writer (curator)
> discipline, exact `context_cycle` placement, the gate/rework model, and the agent roster — are
> specified in **§14**. That section is the build spec for the factory workflow.

---

## 8. The process axis — version-stamping & self-improvement

The subject axis (§6) tracks whether a *goal's* research is done. The process axis tracks whether
the *factory* is running better. They are orthogonal: research can be fully done on goal X under
workflow v2, then a change to v3 only affects how the *next* goal runs — X's research is still done.

**Runtime pickup is automatic.** Skills and protocols are read from the repo at run time, so the
next cycle uses the new method with no deploy step beyond the commit.

**Meaning requires a version stamp.** Every run is tagged with the workflow version that produced
it — `wf:<version>` (a git short-SHA of the protocol/skills, or a semver). Without the stamp,
"it ran differently" is invisible and unmeasurable. The stamp does double duty:

1. **Efficiency comparison** — slice yield telemetry by version to compare v2-runs vs v3-runs.
2. **Blast-radius scoping for process defects** — if the *old process was defective* (e.g.
   "v2's feasibility gate was too lax and passed POCs it shouldn't have"), everything proven
   under that version must be re-opened to `partial`. The stamp answers "proven under which gate?"

**Process changes do NOT invalidate proven knowledge.** A technology proven by a real POC stays
proven regardless of which workflow found it — the artifact is the proof, not the process. The
only exception is the process-defect case above, scoped by the version stamp.

**The firewall applies to process improvement.** "v3 is better" is `claimed` until comparative
telemetry proves it. This is exactly how the factory's own capability *"improves its own
workflow"* (a `factory` entry, §9) reaches `proven`:

```
lesson-learned ("we stopped researching harnesses too early")
  → workflow edit (raise coverage K) → committed as wf:v3
  → next runs stamped wf:v3
  → cycle_review yield (§10) compares v3 runs vs v2 runs
  → better?  proven_by evidence for "improves its own workflow"  +  the lesson is validated
  → not better?  the lesson was wrong → revert or re-learn (a new lesson)
```

---

## 9. The process plane — the `factory` category

The factory improving itself is a **different plane** from the research it performs: tracking
enhancement ideas and A/B tests must not pollute the research base. Because the Unimatrix client
addresses a **single slug** (separate slugs are not differentiable from one client), isolation is
achieved at the **category** level, not the store level.

**Isolation mechanism (two leak paths, both closed):**
- **Search bleed** → closed by the `category` filter. Research queries scope to the research
  categories; factory queries scope to `factory`.
- **Graph bleed** → closed by **edge discipline**: never author an edge between a `factory` entry
  and a research-category entry. With no bridge, PPR/graph-expansion cannot cross. (Zero by
  construction.)
- **Residual path (low risk by design):** proactive **briefing / vector injection** is not
  category-filterable, but briefing is **goal-conditioned** — it takes the cycle's goal sentence
  (from `context_cycle start`, §7) to steer relevance. This makes the per-run goal sentence the
  **de facto plane selector**: a research run's goal (a research subject) steers briefing *away*
  from `factory` entries; a factory-improvement run's goal steers *toward* them. Combined with the
  engine's preference for no-info over bad-info, a `factory` entry surfacing in a research briefing
  is unlikely in practice. Not a hard guarantee, but an acceptable residual (§11).

**One category, structured by `kind`.** Five separate process-categories would re-introduce the
bloat we avoid; instead `factory` runs the identical 5-role methodology internally via `kind`:

| `factory` `kind` | = research role | In process terms |
|---|---|---|
| `goal` | goal | "a continuously-improving research factory" (the root) |
| `capability` | capability | what the factory must *do* — the "am I autonomous yet" board, status-tracked |
| `technology` | technology | **an enhancement idea** — a candidate process mechanism (the testing backlog), `claimed` until A/B |
| `finding` | finding | **an A/B / experiment result** — carries the version-sliced telemetry + verdict |
| `lesson-learned` | lesson | a process lesson that motivates the next enhancement |

**The A/B loop** (all entries `category=factory`, edges factory→factory only):
```
factory/technology  "loop-until-dry K=5"   (enhancement idea)            status: claimed   ← backlog
factory/finding     "A/B shd-002: K=5 reopened 0 caps vs K=3's 2; +12% budget, net win"
                    cites: cycle_review wf:v2 vs wf:v3        Motivates→ "loop-until-dry K=5"
→ context_correct   "loop-until-dry K=5"  status: proven, proven_by: "A/B shd-002, telemetry <ref>"
→ "parallel tech-discovery"  stays claimed until its OWN A/B
```

- **Ideas for testing** = `category=factory, kind=technology, status=claimed` — one query returns
  the whole enhancement backlog, invisible to research retrieval.
- **A/B without pollution** = experiment, comparison, and verdict are all `category=factory`; a
  research query filtered to research categories never sees them.

**The telemetry seam is a field, not an edge.** A factory `finding` references a research run's
`cycle_review` output by **ref in its `cites:` field** — not an edge. So the evidence flows from
research runs into factory proofs, but graph isolation is preserved (no bridge ⇒ no PPR leak).
The research plane *generates* the evidence; the process plane *consumes* it. Entries never cross;
only the measurement does.

---

## 10. Telemetry — using `context_cycle_review`

Telemetry is what makes both the subject axis (yield per run) and the process axis (yield per
*version*) measurable. The home is `context_cycle_review`.

### 10.1 What a cycle is

One research run = one cycle, keyed by `topic` (the run id, e.g. `shd-001`). `context_cycle`
opens it, marks phase boundaries, and closes it; `context_cycle_review` analyzes it.

### 10.2 The call sequence (per run)

```
# open the run — the goal sentence is LOAD-BEARING: it drives goal-conditioned briefing (and
# thereby plane selection, §9) AND binds this run's entries to telemetry. stamp the workflow version.
context_cycle({ type:"start", topic:"shd-001", goal:"<specific goal sentence>", next_phase:"scope" })
   # entries stored this run carry tag wf:v3 (the version that produced them)

# close each phase as it ends (advances the phase signal; records the outcome)
context_cycle({ type:"phase-end", topic:"shd-001", phase:"scope",          outcome:"…",                    next_phase:"decompose" })
context_cycle({ type:"phase-end", topic:"shd-001", phase:"decompose",      outcome:"6 capabilities mapped", next_phase:"tech-discovery" })
context_cycle({ type:"phase-end", topic:"shd-001", phase:"tech-discovery", outcome:"7 technologies, claimed", next_phase:"feasibility" })
context_cycle({ type:"phase-end", topic:"shd-001", phase:"feasibility",    outcome:"2 proven, 1 partial",   next_phase:"synthesis" })

# review at run end — auto_close shuts the final phase so it isn't mis-counted as never-closed
context_cycle_review({ feature_cycle:"shd-001", auto_close:true, format:"json" })
```

Parameters that matter:
- `feature_cycle` — the run's `topic`.
- `format` — `json` for the autonomous loop to parse; `markdown` for a human read.
- `auto_close: true` — writes the closing `cycle_stop` as part of the review so the final phase
  closes cleanly (idempotent; a no-op if already stopped).
- `force: true` — recompute fresh (the report is cached after first call).
- `evidence_limit` — cap evidence items per hotspot (json path).

### 10.3 What it gives today (observation telemetry — free)

`context_cycle_review` aggregates the observation stream (Claude Code hooks): per-phase
reckoning, tool-call activity, hotspots with evidence, and never-closed detection. This is
**process** telemetry — where time/effort went, which phases ran long, what was touched.

### 10.4 What we layer on (knowledge-yield telemetry — query today, engine-native later)

The metrics the factory needs to self-improve are about *knowledge produced*, and that data is
already in the KB, queryable by the run's `topic`. Until the engine emits it natively, compute it
with lookups scoped to the run:

```
context_lookup({ topic:"shd-001", category:"technology" })       → status histogram → proven/claimed ratio
context_lookup({ topic:"shd-001", category:"finding" })          → findings produced this run
context_lookup({ topic:"shd-001", category:"lesson-learned" })   → dead-ends this run
```

| Metric | Why it matters | Source today | After enhancement (§11.4) |
|---|---|---|---|
| budget spent vs. cap | did the run stay within budget | orchestrator ledger | orchestrator ledger |
| findings / run | research throughput | `context_lookup` by topic | cycle_review yield block |
| **technologies `proven` vs `claimed`** | **the firewall ratio** — validating, or just collecting optimism? | `context_lookup` status histogram | cycle_review yield block |
| dead-end rate (lessons / run) | how much was wasted exploration | `context_lookup` by topic | cycle_review yield block |
| cost per proven capability | the factory's marginal efficiency | derive: budget ÷ Δproven | cycle_review yield block |

### 10.5 Slicing by version (the process axis)

Because every run carries `wf:<version>`, comparing methods is "group the per-run yield by the
`wf` tag." Run `cycle_review` for each run and aggregate by version; the delta between v2-runs and
v3-runs is the **proof artifact** that a process change helped — i.e. the `proven_by` a
`factory/finding` cites in the A/B loop (§9). After the §11.4 enhancement, the yield block carries
the `wf` stamp directly, so the comparison is a single grouped read.

### 10.6 Two consumers

- **Human** — `format:"markdown"` at synthesis, to confirm the run and the "researched enough"
  gate (§6).
- **The factory loop** — `format:"json"`, to (a) read the frontier-adjacent yield and decide
  next actions within budget, and (b) feed the process-plane A/B as cited evidence (§9).

---

## 11. Open Unimatrix enhancements (identified through use)

These surfaced while designing the methodology against the live engine. (Unimatrix is developed
in-house, so "the model needs an enhancement" is a valid output.)

**Resolved during design (kept for traceability):**
- *Edge typing is a non-issue.* Edges are entry-level; the engine does not constrain an edge by
  endpoint category, so `technology → capability` `Prerequisite` works natively (§5).
- *Briefing isolation is acceptable.* Briefing is not category-filterable, but goal-conditioning
  plus the engine's preference for no-info-over-bad-info keeps the `factory` plane from bleeding
  into research context in practice (§9).

**Open:**

1. **Capability authoring guidance for the `technology` distinction.** The capability model's
   cardinal rule is *"name the outcome, never the implementation."* `technology` is the inverse
   (it *is* the mechanism). Now that they are separate categories, the authoring guidance must
   state the two altitudes explicitly so agents don't drift technologies up into capabilities.

2. **Context-qualified `proven` for reuse.** Encode the rule that reusing a `proven` technology
   under a materially different envelope re-opens it to `partial` until re-validated (the
   `proven_by` field already records the original envelope).

3. **Knowledge-yield in `cycle_review`** (see §10.4) — emit a per-cycle knowledge-production
   summary (entry counts/deltas by category · kind · status for the cycle's topic), carrying the
   `wf:` stamp so yield is sliceable by workflow version.

---

## 12. Worked example — goal `shd` (self-hosted dev/research capability)

**Goal.** Own the full dev+research loop locally — capable local models, public LLMs only when
targeted — so no single vendor's cloud is load-bearing. `mode: poc-required`.

**Business capabilities** (`kind: business`, each `Advances → goal`):
```
C1 "Capable LLM inference runs on local hardware"
   done_when: a local model serves a coding-grade completion for task P at ≥X tok/s on target HW
C2 "An agentic harness drives research+coding tasks to completion"
   done_when: the harness finishes a defined multi-step research+code task with no manual steps
C3 "Tasks selectively escalate to a targeted public LLM when local is insufficient"
   done_when: a task reaches a public LLM only when a local-confidence bar is unmet, and returns
C1 ─Prerequisite→ C2   (can't drive the harness on local models until local serving works)
```

**NFR capabilities** (`kind: nfr`, goal-specific; each `Advances → goal`, `About →` the C's it governs):
```
N1 "The stack runs on owned hardware within a fixed budget"     About→ C1,C2,C3
N2 "No task is blocked by internet loss or vendor outage"        About→ C1,C2,C3
N3 "Sensitive code never leaves local unless explicitly routed"  About→ C3
```

**Technologies** (own category, program-scoped/reusable; each `Prerequisite →` a capability; start `claimed`):
```
T1a "Apple-silicon unified-memory inference (MLX/llama.cpp)"  Prereq→ C1   claimed
T1b "Consumer multi-GPU rig (2×3090, vLLM)"                   Prereq→ C1   claimed
T2a "30B-class coder at 4-bit via llama.cpp/Ollama"          Prereq→ C1   claimed
T2b "Speculative decoding (draft model) for coding latency"  Prereq→ C1   claimed   ← possible novelty
T3a "Claude Code → local models via OpenAI-compatible shim"  Prereq→ C2   claimed
T3b "Alternative OSS harness (aider/opencode)"               Prereq→ C2   claimed
T4a "Local-confidence-gated escalation to public LLM"        Prereq→ C3   claimed
```

**Findings** (inert, `Motivates →` a technology; `cites` as field):
```
F1 "llama.cpp on M-series sustains ~X tok/s at 30B-4bit"   Motivates→ T1a,T2a   cites: <repo>,<blog>
F2 "Claude Code accepts custom model endpoints via config" Motivates→ T3a       cites: <docs>
F3 "aider drives local models through litellm"             Motivates→ T3b       cites: <docs>
F4 "spec-decoding shows 1.8× on similar HW (untested here)" Motivates→ T2b      cites: <paper>
```

**Selection (a position finding, not `Contradicts`):**
```
finding (tag: position): "Select T1a over T1b: equal coding quality; T1b draws 700W vs 120W —
  violates N1. T1b → deprecated."   cites: <power measurements>
```

**Lesson:**
```
L1 "Three harnesses 'claim' local support; only one streamed tool-calls correctly.
   Takeaway: harness viability needs a live tool-call smoke, never doc-reading." → workflow gate
```

**The firewall in action.** The arm may, unsupervised and within budget, create the T-nodes and
move them `missing → claimed` from literature. It may **not** mark any `proven` without an
artifact:
```
context_correct T1a → status: proven,
  proven_by: "live: M2 Ultra 192GB, Claude Code + local 30B-4bit completed shd harness task in N min, transcript <repo>"
```

**Reuse.** `T1a` proven here is `proven` globally. A future "self-hosted client demo" goal reuses
it by adding edges — no re-research — subject to the envelope rule (§4: a 16GB laptop re-opens it).

---

## 13. Configuration summary (Unimatrix)

- **Research categories:** `goal`, `capability`, `technology`, `finding`, `lesson-learned`
- **Process category:** `factory` (sealed plane; `kind` mirrors the 5 research roles — §9)
- **`capability.kind`:** `business | nfr`
- **Profile preset:** `authoritative` (evidence corpus; source-trust dominant, long half-life)
- **Boosted:** `lesson-learned` (cross-cutting wisdom surfaces harder)
- **Adaptive (lifecycle decay):** `finding`, `technology` (they evolve / get superseded);
  `goal` / `capability` near-zero decay
- **Edge discipline:** `factory` edges connect `factory → factory` only; cross-plane links are
  field refs (`cites:`), never edges
- **Run stamping:** every cycle tagged `wf:<version>`; yield sliced by version (§8, §10.5)
- **Cycle:** one per research run, `topic: <goal-tag>-NNN`, phases per §7
- **Pre-seed blockers: cleared.** Edges are entry-level (no category typing); briefing isolation
  is acceptable by goal-conditioning. Seeding is unblocked.

---

## 14. Operational model — how a research run executes

This is the build spec, adapted from the reference Unimatrix workflows (design / delivery /
research-spike). The factory run is a **phase-gated, coordinator-orchestrated, single-writer**
process. It keeps the firewall (§3) enforceable by concentrating all knowledge writes in one role.

### 14.1 Roles (coordinator / specialist split)

A single **coordinator** reads the protocol and executes it — it spawns all work to subagents and
**never generates content itself** (context-window protection depends on this). Specialists do the
work. The roster:

| Role | Type | Unimatrix access | Produces |
|---|---|---|---|
| `research-leader` | coordinator | **`context_cycle` only** | orchestration: phases, gates, budget, git; no knowledge writes |
| `factory-researcher` | specialist | **read-only** (`context_search`/`context_get`) | a `FINDINGS` **file** — the provisional narrative |
| `factory-curator` | specialist | **write** (`context_store`/`context_correct`/`context_edge`) | the **only** writer of knowledge nodes; distills files → graph, firewall-bound |
| `factory-poc` | specialist | none (writes code/artifacts to the repo) | the POC/experiment artifact + a result report |
| `factory-validator` | specialist | none (reads) | gate reports as **files** (not graph) |
| `factory-retro` | specialist | write (process plane) | `lesson-learned` + `factory`-plane entries (§9) |
| `goal-owner` | specialist (advisory) | read-only | **strategic-alignment review** at synthesis — guards **drift** (wrong question) and **under-reach** (a step-function level-up the objective missed; directional/empirical only, suppressed on proof unless stated). Advisory input to the human gate (OBS-1, OBS-4). |

**The cardinal write rule (reconciles the research-spike "no writes" stance with our compounding goal):**

> Researchers are **read-only and produce files**. A run's provisional narrative lives in files;
> only the **curator** distills it into the graph, under the firewall. This mirrors the reference
> workflows exactly — in design the *architect* (a judgment role) writes ADRs, not the researcher;
> in delivery no specialist writes at all. The curator is our architect-equivalent: the
> "vision judgment" that turns findings into outcome-phrased capabilities and viability-graded
> technologies. One writer keeps the firewall auditable and stops provisional claims from leaking
> in as settled knowledge.

### 14.2 The run, phase by phase

`research-leader` issues every `context_cycle` call (only it does). `{run-id}` is the cycle
`topic` (e.g. `shd-001`); `wf:<version>` stamps the run (§8).

```
# INIT — before any file-touching work. The goal sentence is load-bearing (§7).
context_cycle(type:"start", topic:"{run-id}", goal:"{specific goal sentence}",
              next_phase:"scope", agent_id:"{run-id}-leader")
```

| Phase | Who acts | Unimatrix touchpoints | Gate | `context_cycle` close |
|---|---|---|---|---|
| **scope** | researcher drafts `SCOPE.md` (goal-questions, breadth, approach, **confidence-required**, constraints Hard/Hypothesis, **prior-art**) | researcher `context_search(category:"technology")` for prior art / reuse | **human approves scope** (advisory review optional) | `phase-end phase:"scope" outcome:"scope approved, confidence={…}" next_phase:"decompose"` |
| **decompose** | researcher → decomposition file; **curator** distills | curator `context_store` capability+nfr (`missing`/`claimed`) + `Advances`/`About` edges | — | `phase-end phase:"decompose" outcome:"N caps, M nfrs" next_phase:"tech-discovery"` |
| **tech-discovery** | researchers in parallel (question-partitioned, read-only) → `FINDINGS` files; **curator** distills | curator **first** `context_search(category:"technology")` to **reuse**, then `context_store` technology (`claimed`) + finding (`Motivates`, `cites`) | **coverage** (agentic loop-until-dry K/N **+ human confirm**) | `phase-end phase:"tech-discovery" outcome:"T claimed, R reused" next_phase:"feasibility"` |
| **feasibility** *(only if confidence ≥ validated)* | `factory-poc` builds artifacts (the only compute-spending phase); validator verifies the artifact is real; **curator** records proof | curator `context_correct` technology → `proven`/`partial`, set `proven_by` | **firewall (MANDATORY BLOCK)** — no `proven` without a verified artifact; rework ≤2 → SCOPE FAIL | `phase-end phase:"feasibility" outcome:"X proven, Y partial" next_phase:"synthesis"` |
| **synthesis** | **curator** writes `position` findings + the run `REPORT`; marks capabilities `proven` where `done_when` clears | curator `context_store`/`context_correct`; losers `deprecated` | **human review** | `phase-end phase:"synthesis" outcome:"board: A proven/B partial/C claimed"` → `stop` |

```
# CLOSE
context_cycle(type:"stop", topic:"{run-id}",
              outcome:"Run complete. Board: A proven / B partial / C claimed. wf:{version}",
              agent_id:"{run-id}-leader")
```

```
# RETRO (process plane, §8–§9) — after the run, off the research cycle
factory-retro → lesson-learned (research plane) + factory-plane enhancement/A-B entries (process plane)
research-leader → context_cycle_review(feature_cycle:"{run-id}", auto_close:true, format:"json")  # yield → §10
```

### 14.3 Gates & rework

- **Advisory gates** (scope, synthesis): a reviewer's stance is *input to a human gate*; the leader
  relays it verbatim and never acts on it directly. The human decides. At **synthesis**, the
  **goal-owner** (§14.1) runs the relevance/target review as this advisory input.
- **Blocking gates** (coverage, **firewall/feasibility**): `uni-validator`-style check → PASS /
  REWORKABLE FAIL / SCOPE FAIL. REWORKABLE → re-spawn the prior phase's specialists, **max 2
  iterations**; on the 3rd failure escalate to **SCOPE FAIL → stop, return to human**.
- **Gate reports are files**, not graph (`product/research/{run-id}/reports/gate-*.md`) — they are
  coordination artifacts, not reusable knowledge.

### 14.4 Briefing — two layers

1. **Proactive (automatic):** the `context_cycle start` goal sentence drives goal-conditioned
   briefing for the whole run — and selects the plane (§9). The leader sets it; nobody calls
   `context_briefing` explicitly.
2. **Self-brief (targeted):** each specialist runs `context_search` at the top of its task. The
   **curator's self-brief is load-bearing for compounding**: it searches the `technology` library
   *before creating nodes*, so a proven approach is **reused** (a new `Prerequisite` edge), never
   re-researched. This is where "the library compounds" actually happens in practice.

### 14.5 The three surfaces (provisional / settled / live)

The factory uses **three** surfaces (D1), each owning a non-overlapping question:

| Artifact | Lives in | Role |
|---|---|---|
| `SCOPE.md`, `FINDINGS*.md`, `REPORT.md`, `reports/gate-*.md` | git (`product/research/{scope-id}/`) | provisional narrative + proof artifacts + audit trail |
| capability / technology / finding / lesson nodes | Unimatrix graph | curated, settled, queryable, compounding |
| the scope's **GitHub Issue** (one per scope) | GitHub | the **live human↔factory interface** — scope in the body, gates/status/approvals in comments; human inputs originate here and are distilled back |

The **curator is the bridge** between files and the firewalled graph; the **Issue** is a projection
of those two except for human inputs, which originate in it (a comment moves structure, never status).

### 14.6 Autonomy, budget, human checkpoints

- **Human touchpoints (3):** scope approval, coverage-gate confirm, synthesis review. Between them
  the run is autonomous, within budget.
- **Budget bites in `feasibility`** — the only phase spending real compute; the goal `mode` /
  `confidence-required` sets how far it may go (`directional` may skip feasibility entirely).
- **Context protection:** specialists read files themselves (never paste docs into prompts);
  agents return paths + summaries, not contents; rework capped at 2 per gate.
- **Spawn discipline:** all specialists within a phase spawned in one message (parallel); the
  leader waits for all before advancing the cycle.
```

---

## 15. Reconciliation with bootstrap practice (wf-v0.5)

The bootstrap runs (`shd-001`/`shd-002`) and the decisions log (`product/factory/decisions.md`)
evolved this design. The body above is reconciled inline; this section is the changelog, for
traceability (§11-style).

- **Scope unit (D2).** A goal runs as multiple **scopes**, each its own cycle/`topic`/Issue — one
  decompose-scope + one research-scope per capability — not a single goal-wide cycle. The §7/§14.2
  phases define each scope's lifecycle. *Provisional — revisit if goal-wide proves simpler.*
- **Goal-owner role (OBS-1).** Added to the §14.1 roster + §14.3: an advisory **relevance/target**
  review at synthesis (did the findings answer the goal-relevant question; NFRs weighted;
  decomposition gaps?), distinct from coverage and the firewall.
- **Three surfaces (D1).** The GitHub Issue is the **third** surface (§14.5) — the live
  human↔factory interface carrying the 3 checkpoints; one Issue per scope.
- **Confidence-required enum (D7) — clarification, already consistent.** The axis the doc references
  is `directional | empirical | validated` (sets a scope's target status); it replaces any "Type"
  field. The firewall is altitude-aware: `proven` needs an artifact at the claim's altitude,
  demonstrated by us — theory by reproduction, never by citation.
- **`wf:` (D12) — clarification, already permitted by §8.** A method **semver** (tag `wf-vX.Y`),
  bumped only on method-stream PRs — not a HEAD SHA. Git is two-stream (method vs research); see the
  `factory-git` skill.

Canonical detail for each lives in `decisions.md` (D-numbers above).
