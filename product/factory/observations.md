# Factory Observations Log

Running notes from **manual runs** that inform Tier-1 automation — agent contracts, role gaps,
reviewer needs, operational hazards. Distinct from `decisions.md` (settled choices); these are
**needs/observations surfaced in practice**, candidates to graduate into the factory roster or the
`factory` plane once a pattern is confirmed.

---

## OBS-1 — A "goal-owner" relevance review is a distinct, currently-missing gate
*2026-06-23 · from shd-002*

**Observed need.** Beyond "is the evidence real?" (validator/firewall) and "did we research
enough?" (coverage), there is a third, separate question: **did the findings answer the question
that is RELEVANT to the broader goal?** — i.e. target/relevance review. A run can be evidence-clean
and well-covered yet drift off the goal's actual need.

**Reviewer needs surfaced this run** (→ future `goal-owner` agent contract):
- **Relevance / target fidelity:** did shd-002's harness landscape actually answer C2's `done_when`
  in service of the `shd` goal — or optimize a sub-metric? (Here: yes; recommendation defers the
  real proof to shd-003, which is appropriate.)
- **Constraint alignment:** were the governing NFRs weighted correctly? (N1/N2 local — yes; N4
  distribution correctly down-weighted as a tie-breaker, not a gate; N3 N/A to C2.)
- **Gap check:** did decomposition miss a capability the findings imply? (None surfaced this run.)

**Automation implication.** `goal-owner` is an **advisory gate at synthesis** (analogous to
`uni-zero-review` / vision-guardian in the reference workflows), distinct from the validator
(firewall) and the coverage gate. Add to the Tier-1 roster; its checklist = the bullets above.

## OBS-2 — Subagent file-writes are blocked; the researcher contract must account for it
*2026-06-23 · from shd-002*

Researchers W1/W2/W4 wrote their findings files via Bash; **W3 was fully blocked** from file writes
and returned its markdown inline for the parent (curator) to persist. The runbook's
"researcher → FINDINGS file" step is not reliably executable by a subagent.

**Automation implication.** Either grant researcher agents a write path to
`product/research/{id}/`, **or** make the curator/leader responsible for persisting
researcher-returned findings. Pick one and bake it into the Tier-1 researcher + curator contracts.

## OBS-3 — Unimatrix connection goes stale mid-run (issue #830)
*2026-06-23*

`context_cycle` / `context_store` calls were interrupted ~4× by the stale-connection symptom; each
cleared on a manual `/mcp` reconnect. Filed `dug-21/unimatrix#830`.

**Automation implication.** An automated leader needs **retry/reconnect resilience** around
`context_*` calls, or unattended runs will stall. Not a blocker in manual mode (human reconnects).

## OBS-4 — Goal-owner needs a step-function / ambition review (directional only)
*2026-06-24 · from shd-004*

The goal-owner checklist (OBS-1) guards relevance / constraint / gap — all of which **assume the
stated objective is the right altitude.** shd-004 optimized the stated (single-box, N1-bounded)
objective efficiently and correctly, but nothing in the process pressure-tested whether the
**objective itself under-reached**. The human did it manually: *"if we leveled up, what does that
buy us — and is it worth it?"*

**Need.** A 4th goal-owner dimension — **step-function check**: given the landscape, name any
higher-value level-up beyond the stated objective (what it buys, its cost) → pursue /
defer-and-record / decline. Guards against tunnel vision from a tightly-scoped objective. The
"worth it" cost/benefit + advisory-to-human keeps it from becoming scope-creep; deferred level-ups
are **recorded** (D10/D11) so they aren't lost.

**Confidence-conditioned.** Active on **directional/empirical** (mapping terrain is when you can
assess a level-up); **suppressed on validated/proof** unless the scope explicitly stated it (a proof
is a bounded commitment; re-opening ambition mid-proof derails it).

Baked into `goal-owner.md` (wf:v0.8); enhancement #20 updated. The reflexive loop (§8) operating
manually — a real run surfaced a process gap → a workflow edit.

## OBS-5 — Non-gate interactive prompts break the autonomous run; gates are the ONLY stops
*2026-06-26 · from shd-004 (first AUTONOMOUS run)*

shd-004 was the first run executed autonomously (research-leader spawning real specialist agents,
not inline roles). The leader twice used `AskUserQuestion` at a **non-gate** point — to refine an
in-envelope steer ("add a $5K hardware tier") — and it **blocked the autonomous flow**; the human
flagged it directly ("STEP WITH THE QUESTION CONTEXT. This blocks autonomous … it stopped our
autonomous workflow earlier").

**Rule surfaced.** The research-leader must confine **blocking/interactive** prompts to the **3
human gates ONLY** (scope approval · coverage confirm · synthesis review). An in-envelope steer is
executed with sensible **defaults** + surfaced in **Issue comments / the work product** — never a
blocking question. A non-gate question is a defect, not diligence. (→ factory enhancement, claimed;
`Prerequisite→` #25 Orchestrate a phase-gated run.)

## OBS-6 — Observation telemetry now flows: the attribution fix is confirmed (#24 partially unblocked)
*2026-06-26 · from shd-004*

The prior symptom (enhancement #24 "process-axis telemetry wiring"; capability #32 tagged `blocked`)
was `context_cycle_review` returning **"No observation data."** On shd-004 it now returns rich data:
`total_records: 186`, `attributed_session_count: 1/1`, `knowledge_stored: 22`, per-phase stats with
gate outcomes, `cold_restart_events: 3` (the real session gaps). **Confirmed: the attribution fix
landed.**

**Still partial (not complete):** `total_tool_calls: 0`, `knowledge_curated: 0`,
`feature_knowledge_reuse.total_served: 0` remain unpopulated — the cycle/phase/attribution stream is
wired, but the per-tool-call and curation sub-streams are not yet. Enhancement #24 → `partial`, not
`proven`; the reflexive capability #32 stays `blocked` until telemetry can power an A/B improvement.

## OBS-7 — Subagent file-writes are blocked for EVERY specialist; the contract must flip to leader-persists
*2026-06-27 · from shd-005 (first multi-specialist autonomous run)*

shd-005 spawned **8 read-only researchers** (W1–W6 + W7a/W7b). **Every one had its file-write
blocked** and returned its FINDINGS markdown inline for the leader to persist (the leader wrote all
8 `findings-*.md` + the two REPORT/synthesis files). This is no longer an intermittent symptom
(OBS-2, n=1 partial on shd-002) — it is **deterministic in this harness**: a spawned specialist
cannot write to the repo.

**Rule surfaced (supersedes the OBS-2 "pick one" ambiguity).** The researcher contract is
**read-only, returns-markdown**; the **leader/curator is responsible for persisting** every
researcher artifact (and must budget context for it — inline returns of 8 large findings files are
heavy). The runbook's "researcher → FINDINGS file" step is **not executable**; rewrite it to
"researcher → returns markdown → leader persists." (→ factory enhancement #21, now strongly
evidenced; should move toward `partial`/contract-locked.)

## OBS-8 — Two method wins confirmed: run-id-tag yield query works, and the goal-owner step-function fired
*2026-06-27 · from shd-005*

1. **Telemetry-tag fix works (#65).** shd-004's per-run yield query returned empty (curator hadn't
   tagged). shd-005's curator tagged every node `shd-005`; `context_lookup(tags:["shd-005"])` returns
   all 20 nodes — **per-run knowledge-yield is now queryable by tag** (note: by *tag*, not the `topic`
   field, which the curator set to `shd-routing`). The runbook's run-id-tag convention is validated.
2. **Goal-owner step-function dimension (OBS-4) fired productively, manually.** A human "what if we
   level up?" steer mid-run surfaced the platform-coverage reframe and then the platform-vision goal
   (#92) — captured build-deferred (D10) without derailing the directional run. The reflexive loop
   (§8) operating by hand: a run produced a methodology lesson (#90/#91, platform-blindness) **and** a
   new product-vision goal, both firewall-clean. Evidence the goal-owner role earns its place.

## OBS-9 — Grade becomes a tag-canonical field via `context_tag`; and its ~60/hr write rate limit
*2026-07-07 · platform update*

Two Unimatrix updates reshaped how the board is stored and read:
1. **`context_graph(mode:"subgraph")` now honors an `edge_types`+`direction` filter** → the §6 board
   query is a **single hydrated call** (was `neighbors` edges-only + a bulk `context_lookup` + a
   client-side join). `neighbors` still returns edges only, even at `detail:"full"`.
2. **`context_tag(id, action, tag)`** — an **in-place single-tag mutation** that preserves the id,
   content hash, edges, and embedding (**unlike `context_correct`, which reissues the id**). `replace`
   is namespace-scoped (`grade:*`) and sets-or-swaps in one idempotent call. This made the firewall
   grade a **tag-canonical field** (`grade:<missing|claimed|partial|proven>`) — moved cheaply without id
   churn, read straight from the lean `subgraph … detail:"summary"` projection. **Distinct from the DB
   `status` field** (lifecycle `active`/`deprecated`) — the grade tag must never be named `status`.
   Adopted across methodology §3/§4/§6, `unimatrix-access`, `factory-curator`, runbook.

**Hazard — write rate limit.** `context_tag` is rate-limited to **~60 writes / 3600s**. Backfilling the
existing board (~60 capabilities+technologies) hit it: 57 tagged, **3 deferred** (`retry after ~56m`).
**Automation implication:** a curator that flips many grades in one burst — a large decompose, a mass
reopen (process-defect blast-radius, §8), or a backfill — must **throttle/batch under 60/hr** or stall.
The firewall is unchanged: `grade:proven` is still set only alongside a `context_correct` that attaches
`proven_by`; `context_tag` carries the missing/claimed/partial moves.

## OBS-10 — The whole smart-edge line ran with NO GitHub Issue (D1 third-surface gap) — and NO `context_cycle` stamping
*2026-07-08 · from smart-edge-001/002/003 (first theme-scan + first promoted proof-goal)*

Two surfaces the protocol assumes were **silently skipped** for the entire run until caught late:
1. **No GitHub Issue.** The scan (`smart-edge-001`), the proof-goal (`smart-edge-002`), and the rerun
   (`smart-edge-003`) ran to a `partial` artifact + a product handoff with **no Issue** — D1's third
   surface (the live human↔garage interface) was absent. Created retroactively (`#37` scan, `#38` proof).
2. **No `context_cycle` stamping** (until `smart-edge-002` onward). The scan phases were bare agent
   spawns → no telemetry, and (pre-fix) **no retained transcript at all** — transcript↔cycle linkage
   *requires* stamping.

**Rule surfaced.** The `theme-scan` and `research-scope` protocols must **create the Issue AND
`context_cycle start` at INIT — not optionally, not retroactively.** An un-stamped, un-Issue'd run is
invisible on two of the three surfaces. (→ wire both into protocol INIT; the cycle-stamping half is the
standing wire-stamping enhancement.) The retention/transcript-linkage itself is now **fixed on the
platform** (verified: stamped `smart-edge-003` returns `Transcript bytes: 112091` where pre-fix
`smart-edge-002` returned "no data").

## OBS-11 — The capability-surface inventory must carry the IMPLEMENTATION SUBSTRATE, not just the interface
*2026-07-08 · from smart-edge-001*

The hypothesizer's first pass reasoned against Unimatrix's MCP **interface** (`context_*` tools) and
missed that the server is a **Rust binary** — so nearly the whole candidate family is Rust-native and can
live **in-server** (a first-order fit/effort discriminator). The owner supplied the correction; a second
pass on the corrected surface **doubled** non-obvious/adjacent survival. **Rule:** the surface inventory
handed to the generator must include the use-case's **tech stack / language / existing components** (e.g.
"a PII scanner already exists"), because in-server-native-vs-external-bolt-on changes the verdict.

## OBS-12 — Real linked-transcript testing beat the synthetic test; the firewall's "on real data" bar earned its keep
*2026-07-08 · from smart-edge-002 rerun*

The H11 bank scored 100%/0-FP on a **synthetic** labeled set, then **over-fired on a real linked
transcript** — flagging an agent's stored text ("…never a bare context_tag") as a firewall *violation*.
Naive lexical matching cannot tell *discussing* a hotspot from a hotspot *event*. The synthetic test hid
it; only real data exposed it. The **structural fix** (match the event outcome field, not raw prose) was
then demonstrated (FP 3/3 → 0/3, recall preserved). **Lesson:** for transcript/agent-output tools, a
`partial`/`proven` claim must be demonstrated on **real captured data**, not a hand-built proxy — the
proxy flatters. This is the reflexive loop working: running the tool on real data surfaced its next
design constraint (the two-tier requirement).

## OBS-13 — factory-onboard had no "plan, don't execute" boundary; an orienting session slid into running a full scan
*2026-07-22 · from wfh-001 (theme:workflow-harness first scan)*

A `/factory-onboard` session (planning/ownership) slid straight from "recommended next action" into
**executing** a theme-scan — opening Issue #41, stamping `context_cycle` wfh-001, and spawning two scouts —
because nothing in the skill said to stop at the recommendation. The SDLC repos already solve this: a
**product-owner pair** whose agent def *cannot* build/bugfix (cf. `uni-zero`: "does not run delivery
protocols"). The factory had the executor roles defined (research-leader, scout, curator…) but **no
guardrail keeping the planning/onboarding session out of the executor's chair.**

**Rule surfaced.** `factory-onboard` is plan-only: orient → plan → scope → triage → **recommend, and stop**.
Executing a run (spawn specialists · `context_cycle start` · open the run Issue · graph writes) is a
**separate, deliberate session** invoking the research/theme-scan protocol, **scope-approval as its first
gate**. Baked into `factory-onboard` §0. **Honest limit:** instruction-enforced (honor-system) until a
harness enforces the role boundary structurally — the workflow-harness/JURATI thesis applied reflexively to
the factory itself. (Also a `factory-retro` candidate for a wave-1 role/agent-def that bars execution.)

## OBS-14 — Cycle telemetry is blind to subagent sessions: the converge legs' 38 writes recorded as "0 stored"
*2026-07-22 · from wfh-001 retro*

`context_cycle_review(wfh-001)` saw only the scan-phase sessions. The converge legs — run by a
research-leader **subagent** in its own sessions — were invisible: the review reported **"Stored this
cycle: 0"** while the curator demonstrably stored **38 nodes** (PR #45); the phase timeline showed
`scan → triage` though `formalize` and `synthesis` phase-ends were acknowledged; and the cycle showed
IN PROGRESS after an acknowledged `stop`. Consequence: **the more autonomous a run (more work pushed
into agent sessions), the less its telemetry attributes** — the reflexive loop's §9 funnel/yield metrics
under-count exactly the runs we most want to measure. Related upstream: the known observation-attribution
gap (enhancement #24) and D6 (agent_id not persisted). Until fixed, treat cycle-review yield numbers as
a **floor**, and take authoritative counts from a run-id `context_lookup` (as this retro did).

Smaller operational notes from the same run: repo-level auto-merge is disabled (protocol says
"auto-merge after the triage gate" — enable it or amend the protocol) *[resolved 2026-08-01 — the
protocol was amended, not the setting: `factory-git` now derives repo settings via `gh api` instead of
asserting them, and says the leader rebase-merges by hand. Two other settings claims in that skill were
wrong at the same time, undetected for two weeks — a hard-coded setting rots exactly like a hard-coded
version stamp]*; WebFetch failed 4× clustered
during scan (retry/backoff or alternate fetcher for scouts); `context_correct` re-links on #11–#15
skipped pre-existing invalid incoming sources (engine-side data quirk — pre-existing, not authored this
run; watch whether it recurs).

## OBS-15 — The theme mechanism, the garage's only divergent-reach engine, has effectively never run
*2026-08-01 · from the wfh-004 direction review*

The theme scan is designed to be exactly what an R&D funnel needs at the wide mouth: a recurring, divergent
sweep that finds relevant, adjacent, and contrarian material and feeds it into structure. It is not missing.
It has barely run. Across the first month: `smart-edge` seeded 2026-07-07, **one** scan (at seeding);
`daystrom` seeded 2026-07-08, **zero** scans ever; `workflow-harness` seeded 2026-07-22, **one** scan (at
seeding). Roughly seven scans owed against declared weekly cadence, two delivered, both at seed time. The
mouth fired once per theme and the funnel drained downward for the rest of the month.

**Four mechanical causes, all configuration rather than design:**
1. **Cadence lives in a file and is scheduled nowhere.** "Scanned on cadence" plus "wave-0 = manual kick"
   yields a cadence of zero, predictably.
2. **The aperture was set to shipped tools.** Every theme's `source-mix` read *TBD*, so scouts defaulted to
   product pages and repos. The first harness scan returned ~30 tools and no theory; the run that followed
   generated 128 candidate abilities against **zero research literature**.
3. **The scout had one mode.** *Discover candidates we lack* — with no mode for *take a position we hold and
   find its prior art and counter-case*. Discovery cannot report that something we believe is already
   solved, superseded, or wrong.
4. **Dedup narrows and nothing widens.** Each scan filters against what the graph already knows, anchored
   to a value-target, with no counter-pressure.

**Measured cost.** The material that reframed `theme:workflow-harness` — a thirty-year workflow-authorization
literature, the capability-security lineage, and a buy-versus-build question nobody had asked — arrived
through an **owner conversation outside the funnel entirely**. The garage's divergent reach was, in practice,
outsourced to the human, with no intake for the result except opening a new scope.

**Response (this method change, wf-stream):** four declared reading surfaces each with its own question;
a challenge mode alongside discovery; warm-leg/cold-leg discipline with the cold leg protected; a coverage
grid as the scan's finish line; adopt and assemble added to the triage verdict set with a burden of proof on
build; and a legal channel for a scan to propose reshaping its own theme. **Still open:** scheduling is
interim (a theme review at each scan close), and the watchlist is hand-curated until author/organization are
carried in the citation structure — the derived form D8 already points at.

---

## OBS-16 — The four reading surfaces worked; their *instruments* are vocabulary-bound and popularity-bound
*2026-08-03 · from wfh-005 (the first challenge scan, and the first run under the wide-mouth standard)*

**The standard passed its first test, measurably.** 158 structured citations across seven scout files —
active-dev 70 · products 32 · literature 30 · adjacent 26. **No surface was staffed and left unread**, which
is the specific failure OBS-15 predicted and the `surface` field exists to catch. All four surfaces changed
at least one verdict, and **no verdict in the run was reachable from a single surface**. The two surfaces
that had never been staffed before — research literature and adjacent prior art — are the two that falsified
the theme's central claim, from five unrelated fields, independently of each other.

**And every verdict-moving correction still arrived from outside the method.** Three times:

1. The run's own proposed sixth position was **falsified by the owner** with a repository the scan never
   queried (354 merged pull requests against 31 protocol revisions).
2. A 66,763-star ecosystem was missed entirely — **the owner asked about it by name.** It self-describes as
   *swarm · flow · meta-harness · dream cycle*; a scan searching for *policy compiler · capability
   derivation · agent authorization* emits none of those words and never collides with it.
3. A third find — an evaluation harness whose conformance discipline independently reinvented our firewall —
   **the owner named it from something they had been reading.** Its README contains none of the theme's
   nouns at all.

**The diagnosis is not effort, it is instrumentation.** A scout searches *by mechanism vocabulary* and
*ranks by relevance or popularity*. Both are structurally blind in the same two directions:

- **Vocabulary.** Adjacent work is filed under words the theme does not use. No amount of thoroughness inside
  the theme's own lexicon reaches it.
- **Popularity.** In this run the incumbent's answer arrived at **4,849 stars**, the *research* answer at
  **17**, its predecessor at **5**, and its dataset repository at **4**. No star-ranked or relevance-ranked
  search reaches two digits. Those were found only by walking an **organization** after something else named
  it.

**Response (method change, wf-stream):** three instruments added to the active-development surface — an
**organization-walk**, a deliberately **low-star pass**, and a **by-function rather than by-vocabulary
sweep** (*who else does this job, without using any of our nouns*). Cross-surface reconciliation is promoted
from a leader step to a **requirement** wherever more than two surfaces are staffed. And the round-two
trigger is re-keyed from *thin or empty cells* to *a named hole load-bearing for a verdict or a routing* —
wfh-005 was 20-of-20 on cells while two holes sat under its only build recommendation, and the trigger
correctly never fired.

**Still open:** none of the three new instruments has run yet. They are `claimed`, on the same terms as
every other enhancement.

---

## OBS-17 — Cycle telemetry is healthy for the leader session; OBS-14's subagent blindness persists, with a sharper shape
*2026-08-03 · from the wfh-005 retro*

`factory-retro` carries a standing caveat that its process-telemetry half is degraded pending an upstream
attribution fix. **For wfh-005 it was not degraded at all.** `context_cycle_review` returned 439 records,
1-of-1 session attribution, complete per-phase statistics carrying each phase's gate-outcome text, a
friction hotspot with twelve timestamped evidence items, and a baseline comparison across eleven prior
cycles. That is the full instrument. #63's partial unblock now reads as substantially complete **for the
coordinating session**.

**OBS-14 is not closed, and the retro must not read the above as closing it.** Two specifics from this run:

- **`agents_spawned` returned empty** against **nine** specialist spawns.
- **All 24 knowledge stores were attributed to the leader session.** The leader wrote none of them — the
  curator did, in a subagent. The telemetry is not merely blind to subagent sessions; **it silently
  reassigns their work to the parent**, which is worse than a gap because it reads as a complete record.

**Consequence for the reflexive loop.** Any future comparison of *which role produced what* is unusable, and
the single most useful autonomy question — *did an agent do this, or did the human steer it* — is invisible
in the telemetry and recoverable only from the narrative. **#65 stays `partial` and stays blocked.**

**Held against ourselves:** wfh-005 was heavily human-directed, so no factory capability advances on it.
`grade:proven` on an autonomy capability requires an autonomous-run artifact, and three owner injections at
the gate is the opposite of one.

**Amendment (same day, from the retro's own curator).** The curator re-ran `context_cycle_review` rather
than take the leader's brief on trust — correct behaviour — and **could not verify two of its claims**: it
saw `Gate: UNKNOWN` on all four phases and no baseline-comparison section at all. Both of us were right.
The leader called it with `format:"json"`; the curator took the **default `markdown` render**, and the
markdown render **drops `gate_outcome_text` and the entire `baseline_comparison` block** that the JSON
render carries. Same call, same cycle, materially different picture.

**Why this matters beyond a formatting quibble.** An agent taking the default render sees no gate outcomes
and no baseline, and would reasonably conclude the telemetry is degraded — the exact conclusion
`factory-retro`'s standing caveat primes it to reach. **The data was there and the default view did not show
it.** That is this run's own emergent position (#196) one level over: a mechanism present, believed, and
not in force from where the reader stands. **Operational rule until parity lands: run
`context_cycle_review` with `format:"json"` in any retro, and treat the markdown render as a summary, not
as the record.**
