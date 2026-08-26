# Protocol: theme-scan

The **recurring, technology-push** intake at the **wide mouth of the garage funnel** (`CLAUDE.md` Mission):
scan a **theme** for candidate technologies, fan each out into hypotheses (wide mouth), triage hard at the
**neck**, and hand a shortlist to the owner. Inverts research-scope
(which is capability-pull). Produces **structure only** — candidate technologies (`claimed`) and
hypotheses (`finding`+`hypothesis`); **nothing reaches `proven` here.** A promoted hypothesis becomes a
*separate* bounded proof-goal (a normal validated research-scope) where the firewall bites. Run by
`research-leader`. Its own cycle (`topic`) + GitHub Issue. Phases: **scan → hypothesize → triage → formalize.**
Design: `product/factory/proposals/theme-driven-scanning-methodology.md` (§5 flow · §6 triage · §9 funnel).
A `theme-coordinator` may select and launch this run within the theme's declared authority envelope, but
the spawned `research-leader` still owns the run and every gate below.

**The wide-mouth standard** (`product/factory/themes.md` → "How a scan reads") binds this protocol:
scanning runs across **four reading surfaces** — research literature · established products · active
development · adjacent prior art — in one of **two modes** (discovery, or challenge against a position we
hold), on **two legs** (warm watchlist deltas plus a protected cold leg), and finishes against a **coverage
grid** rather than against fatigue. Triage returns **five verdicts** — adopt · assemble · build · probe ·
park — because a scan that can only park, probe, or build cannot report that the work is already done.

## Roles
`research-leader` (orchestrate, persist, budget) · `scout` (×1+, discovery) · `hypothesizer` (Fable 5,
divergent fan-out) · `factory-curator` (single writer) · `goal-owner` (convergent triage). No POC/
validator — this protocol never proves.

## INIT
- Read `product/factory/themes.md` — the shared **"How a scan reads"** standard, then the **active theme**:
  lens · value-targets · **reading surfaces** · **coverage grid dimensions** · **watchlist** · cadence ·
  **budget envelope** (§8). Resolve `scan-id` = `{theme-slug}-NNN` (e.g. `smart-edge-001`).
- **Declare the scan's shape** in the Issue body, because these choices decide what the scan can possibly
  find: which **surfaces** are staffed (and which are deliberately skipped, with the reason), which
  **mode** each scout runs (discovery / challenge, and against which position), and the **cold-leg
  minimum**. An unstaffed surface is a declared hole from the outset, not a discovery made at the end.
- **Governor — do not scan past the neck's throughput.** If the theme already carries an untriaged
  shortlist from a prior scan, or a promoted proof-goal that has not run, **surface that to the owner
  before spawning**. The wide mouth outrunning the proving grounds is how a graph fills with `claimed`
  nodes nobody proves (the magpie hazard, `themes.md` → theme:daystrom).
- **Open all three surfaces (D1) — MANDATORY, before any specialist spawns. A run that skips these is
  invisible on two of three surfaces (OBS-10, learned the hard way on smart-edge — no Issue, no cycle
  stamp for the whole line):**
  1. **GitHub Issue** — `gh issue create --repo dug-21/arch-research --label factory,scope:research,confidence:directional`,
     title `{scan-id} — theme-scan: <theme> …`, body = scan intent + out-of-scope. Cross-linked by
     **title, not # equality** (D4). This is the live human↔garage surface; it is not optional.
  2. **Cycle** — `context_cycle start` topic=`{scan-id}`, goal=`scan <theme> for candidate technologies`,
     next_phase=`scan`, **`tags:["{wf}"]`** (the derived `wf:` — `git describe --tags --match 'wf-*'`),
     agent_id=`{scan-id}-leader`. `tags` is **set-once at start** (no append, no retro-fix — get it right
     on the first call). The cycle is what makes the run **attributable and its transcript retained**
     (retention now works on stamped cycles — OBS-10); an unstamped run has no linked buffer at all.
     `phase-end` at **every** phase boundary; `stop` at CLOSE.
  3. **Git** — path-scoped commits under `product/research/{scan-id}/`, **straight to `main` as each
     artifact is produced** (D15) — no branch, so a parked or slow scan is still readable by every other
     run. Stage only your own scope's paths; with no branch isolating a mistake, that rule is now
     load-bearing. Keep the scope's `Status:` line current — on `main` it is what distinguishes in-flight
     from concluded. (The `wf:` version rides the cycle tag above; do not hand-type it.)
- **GATE (advisory → owner):** confirm **theme + candidate source** (owner-injection vs external-scan)
  **+ budget envelope**. The owner is either the human or an authorized `theme-coordinator`. The latter
  may approve only within `product/factory/themes.md` → `Coordinator authority`; otherwise this remains a
  human gate.

## Phase: scan
- Leader spawns **one `scout` per staffed reading surface, all in one message** (parallel). The four
  surfaces are heterogeneous jobs with different outputs — one agent doing four passes produces four
  shallow ones. Each scout gets its surface, its mode, and the watchlist entries for that surface.
  Owner-injection enters here as a hand-fed candidate and flows on identically.
- Each `scout` applies the **lens include-test**, **dedups reuse-first** against Unimatrix (prior runs'
  filed nodes — incl. fold-findings' named tails), characterizes each survivor (mechanism · **resource
  envelope** · demonstrated-vs-claimed · `cites` incl. author/org · source-signal), and — on the products
  and active-development surfaces — gathers the **buy-before-build evidence** triage needs to answer
  adopt-versus-assemble-versus-build (scope-versus-need gap · cost and licence · lock-in and exit ·
  composability). Read-only; returns markdown inline (OBS-7) → **leader persists**
  `product/research/{scan-id}/scout-{surface}.md`.
- **Cross-surface alias merge (leader, after all scouts return) — MANDATORY wherever more than two surfaces
  are staffed (wfh-005).** The same idea routinely appears under four names — one in the literature, one as
  a product category, one as a repo, one in an adjacent field. Scouts cannot see each other and can only
  *flag* a suspected alias; the leader reconciles them into `product/research/{scan-id}/scout-merged.md`
  before hypothesize. Deduping against the graph does not catch this; nothing else in the protocol does
  either. **Why it is now a requirement, not a step:** wfh-005's four surfaces returned what read as ~15
  independent hits on one position; the merge collapsed them to **three clusters, two of which were the same
  works reached by different routes**. Unmerged, that run would have overstated its evidence base roughly
  fourfold *and had no way to notice*. A scan that skips the merge reports inflated convergence and cannot
  tell.
- **Instruments the active-development surface must carry (wfh-005).** Searching by mechanism vocabulary and
  ranking by relevance or popularity is blind in two directions at once, and both fired on the first
  challenge scan. Each scout on this surface runs, and reports, all three:
  1. **An organization-walk** — enumerate the repositories of an organization something else has named.
  2. **A deliberately low-star pass.** In wfh-005 the incumbent's answer sat at ~4,800 stars and the
     *research* answer at **17**, its predecessor at 5, its dataset repo at 4. No ranked search reaches two
     digits.
  3. **A by-function sweep** — *who else does this job*, using none of the theme's own nouns. The find that
     independently reinvented our proof discipline carries none of this theme's vocabulary anywhere.
- **Coverage record.** Collect each scout's surface-coverage report (what was searched, found, and
  deliberately skipped) and cold-leg record, and open the **coverage grid** for the theme. The grid travels
  with the run and is filled in as hypothesize proceeds.
- **NO graph writes in this phase** (lesson #172, wfh-001): the divergent output stays in git markdown
  until triage has compressed it — the neck's verdict shapes what the curator writes (see formalize).
- `phase-end phase:"scan" outcome:"C finds across S surfaces (N new, K known/parked); U surfaces unread"`.

## Phase: hypothesize
- Leader hands the scout writeup **+ the current capability-surface inventory** (for Unimatrix: the live
  `context_*` tool set + repo — the real surface, not an imagined one) to `hypothesizer` (one per
  candidate, spawned in one message).
- `hypothesizer` (Fable 5, loose reins) generates for **range** — mechanism-grounded `T→C of U`
  hypotheses incl. non-obvious/whitespace. Grades nothing; decides nothing. Returns markdown inline →
  **leader persists** `product/research/{scan-id}/hypotheses.md`.
- **Coverage (advisory, non-blocking):** if a candidate's fan-out is thin or its scout writeup too thin
  to reason from, leader re-spawns for more range (≤2) or flags the candidate as under-characterized.
- **Grid-targeted second round.** Map the output onto the theme's **coverage grid** (dimensions × lenses).
  Where cells are thin or empty, re-spawn **aimed at those cells**, handing back round one's output. A cell
  no lens can populate is recorded as a **hole naming which lens failed to see it** — that is a finding, not
  a gap to hide. Exhaustion here is honestly bounded: it is relative to the named lenses and dimensions,
  never absolute, and the record should say so.
- **Round two fires on a load-bearing hole, not on an empty cell (wfh-005).** The cell test is necessary and
  not sufficient. **Also re-spawn when a named hole is load-bearing for a verdict or a routing**, however
  well-populated its cell is. wfh-005 was **20 of 20 on cells**, so the trigger correctly never fired —
  while two named holes sat directly under the run's only **build** recommendation, either of which would
  have converted it to assemble. The goal-owner dissented at the gate and was right. **The question is not
  "is this cell thin," it is "would closing this hole change what we decide."** A run can be complete on
  every cell and still have left unread the one thing that decides what gets built.
- **NO graph writes in this phase** — hypotheses reach the graph only through formalize, post-triage.
- `phase-end phase:"hypothesize" outcome:"H hypotheses (obvious/adjacent/non-obvious split)"`.

## Phase: triage
- `goal-owner` runs the **convergent gate** (§6). In order: **call coverage** (COVERED, or NOT COVERED
  naming the specific empty cell / unread surface, plus the cold-leg check) → run the **buy-before-build
  pass** (does it already exist? can it be assembled?) → score mechanism-fit · theme-alignment · novelty ·
  effort-vs-payoff → **park by default** → route **ADOPT / ASSEMBLE / BUILD / PROBE / PARK**, each with its
  required field. Advisory; writes `product/research/{scan-id}/reports/triage.md`.
- **Required fields are load-bearing, not stylistic.** ASSEMBLE names which part is uncovered and whether
  it is the differentiating one; BUILD names the specific thing assembly cannot deliver; PARK names its
  re-enter-when. A verdict missing its field is incomplete — route it back or downgrade it.
- **Theme-revision proposals** returned by scouts or hypothesizers are relayed **verbatim** to the gate
  with the goal-owner's assessment. A scan may reshape its own theme; it may not do so unilaterally or
  mid-flight (the failure that closed wfh-002).
- **GATE (blocking → owner):** the owner reviews the coverage call, the shortlist, and any theme-revision
  proposal, then **promotes 0..n** items to bounded proof-goals and accepts or rejects the reframing.
  Promoting nothing is a valid, common outcome; so is coming out of the scan with a differently-shaped
  theme than went in. A theme coordinator may park or launch a bounded directional follow-up inside its
  envelope; theme revision, material spend, BUILD commitment, and `proven` changes go to the human.
- `phase-end phase:"triage" outcome:"coverage=<COVERED|NOT COVERED:cell>; A adopt, S assemble, B build, D probe, rest parked"`.

## Phase: formalize (post-gate — ALL graph writes live here)

The run's only curator phase. **The graph stores verdicts and re-entry conditions, never the spray**
(lesson #172; the divergent archive is git markdown). The persistence test for every item: *would a
future agent need to FIND this via `context_search` — to avoid re-spending, or to re-enter when a
condition flips?* If yes → the **cheapest searchable representation** below; if no → git only.

`factory-curator` **self-briefs first** (`context_search` — REUSE; extend existing nodes via
`context_correct`, never duplicate), then files in three tiers:

1. **Survivors** (promoted / probe, plus in-lens candidates worth individual reuse) → full `technology`
   nodes (`grade:claimed`, tagged `theme:<slug>` + `{scan-id}`, `cites`) and `finding`+`hypothesis`
   nodes with `Motivates→` their technology; the conjectured `technology Prerequisite→ capability` edge
   is authored for **survivors only** — speculative edges stay off the graph.
   - **ADOPT / ASSEMBLE verdicts file too, and they matter most.** "We do not need to build this" is
     expensive knowledge that is re-derived every time it is lost. File the existing thing (or the
     composition) as a `technology` (`grade:claimed` — adoption is not proof; using it in anger is what
     would move it), plus a **`position`-tagged `finding`** carrying the buy-versus-build call, the
     scope-versus-need gap, and — for ASSEMBLE — what sits in the seams and whether that part is the
     differentiating one. Without that finding, the next scan re-runs the same evaluation.
2. **Parked-with-a-reason** → a `finding` (`hypothesis`+`parked`) whose content IS the park reason with
   an explicit **re-enter-when** condition. These must be **few and load-bearing** — if triage parks
   many, compress further (fold) before filing; a large parked tier is spray with extra steps.
3. **Folded tail** (thrown out at triage) → NOT individual nodes. One or two **fold-findings that NAME
   every folded candidate** (this is what keeps future scan dedup working graph-side) + the git
   markdown as archive.

- Synthesis verdict (e.g. white-space) → a `position`-tagged `finding`.
- `phase-end phase:"formalize" outcome:"N nodes (S survivors, P parked, F folded-into-K findings)"` → `stop`.

## CLOSE
- `context_cycle stop`. Record the **funnel counts** (scanned → generated → survived → promoted, by
  novelty class), tagged `{scan-id}` + `theme:<slug>` — the reflexive-loop telemetry (§9, #66).
- **Git (D15):** the scan's documents — scout files, hypotheses, the coverage grid, the triage report —
  are already on `main`, committed as the scan produced them. A scan writes no executables, so it
  normally needs **no branch and no PR at all**. Close the **Issue** with the verdict comment; that is
  the gate's record (D1). Set the scope's `Status:` to `done`. Trigger `factory-retro`.
- **Promotion (frontier-change, D3):** each promoted hypothesis → a new **validated research-scope**
  Issue (a bounded proof-goal, real `done_when`), linked to this scan. That run — not this one — does the
  POC and the firewall, and on `proven` files the **Unimatrix issue** handoff (§7). The scan hands off;
  it does not prove and does not ship.

## Cadence
Recurring per the theme's cadence. **Wave-0 = manual owner kick.** Fully autonomous scheduled scanning is a
later wave, **gated on the budget-metering capability** (§8) — do not assume it here.

**Cadence declared is not cadence run.** Across the three themes' first month, two scans happened, both at
seeding, against a declared weekly cadence — the wide mouth fired once per theme and the funnel then drained
downward for the rest of the month. A cadence that lives only in a file is a cadence of zero. Until the
metering gate clears, the interim discipline is: **a theme review at each scan close** that either kicks the
next scan, or records why not and when it should re-fire.

**A first scan and a recurring scan are different runs.** The first maps the space against the coverage
grid. Every one after it runs the two legs — warm deltas over the watchlist, plus the protected cold leg —
and asks what moved. Say which kind you are running in the Issue body.

## Watchlist maintenance (every scan, at CLOSE)
**Run the derivation first, then reconcile — do not just edit the list from memory.** Per D14, citations
carry `author` / `org` / `year` / `surface`, so the candidate set is computed:

```
context_lookup(category:"finding", tags:["theme:<slug>"], limit:N)
  → parse cites: → count org / author across findings and across scans
  → tally by `surface`
```

Then update `product/factory/themes.md` for the theme just scanned: record **last-looked** dates on the
entries walked, **add** what the derivation surfaced (each with the change that would make it interesting
again), and **prune** entries that have gone quiet or stopped feeding a live dimension. Reconcile
near-duplicate name spellings here — the schema does not do it for you.

**Report the `surface` tally in the run's close.** A surface that appears in no citation was staffed and
not read, and that is a finding about the scan, not a footnote. This is steering config, a method-stream
commit, and it is the only thing keeping the warm leg from decaying into a stale list nobody notices.

*Interim:* findings written before D14 carry unstructured citations, so early derivations will be thin and
the hand-seeded entries carry the load. That is expected; it resolves as findings accumulate, not by
backfilling (D14, limit 2).

## Output
A triaged **shortlist** to the owner — adopt / assemble / build / probe, each with its required field —
carried on an explicit **coverage call** (covered, or the named empty cell). Plus a graph enriched with
`claimed` candidate technologies, `hypothesis` findings, and the **`position` findings that record any
buy-versus-build call** (all `theme:<slug>`-tagged); any **theme-revision proposal**, relayed for the
owner's decision; an updated **watchlist**; and the funnel baseline the reflexive loop tunes against.
**Zero status moved to `proven`** — by design.
