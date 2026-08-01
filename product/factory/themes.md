# Factory Research Themes

Standing **steering config**, not knowledge — a theme has no grade, no proof, no `done_when`; it is a
durable directive about *where the factory looks*. Themes therefore live **here, not in the Unimatrix
graph** (the graph holds graded evidence; putting steering in it is category bloat — D8). Design:
`proposals/theme-driven-scanning-methodology.md` §2.

**How this file is used.** The `theme-scan` workflow reads this file for the active theme(s) + budget
envelope. Every downstream artifact the scan produces (candidate `technology`, `hypothesis` finding,
promoted proof-goal) carries the theme's **`theme:<slug>` tag** + a run-id, so "everything under a theme"
stays one graph query even though the *definition* lives here. Definition = file; evidence = graph.

**Firewall.** A theme moves *structure* only. A scanned technology is `grade:claimed`; a hypothesis is an
unproven conjecture (`finding` + `hypothesis` tag); nothing reaches `proven` without a bounded proof-goal
whose POC clears its `done_when`, demonstrated by us.

**Status legend:** `active` (scanned on cadence) · `paused` (kept, not scanned) · `retired` (archived).

---

## The garage funnel — where themes sit

The platform is a **research & development garage**: a funnel from concept → trial → proof.

- **Wide mouth — divergent intake.** *Themes* (this file) scan for candidate technologies. The scout
  discovers, the hypothesizer conceives applications; range is rewarded, nothing is graded. This is
  where new possibility enters.
- **Neck — convergent triage.** The goal-owner triages each hypothesis *park / probe / build*,
  narrowing to a shortlist and promoting the survivors into a proof-goal.
- **Proving grounds — evidence-gated.** The **factory** machinery (decompose → tech-discovery →
  feasibility → **firewall**) turns a promoted candidate into `proven` — or kills it. "Cool idea"
  earns "proven" only on a real artifact demonstrated by us.

**"Garage" is the umbrella identity; "factory" is the precise name of the proving-grounds stage** at
the narrow end. The firewall sits at the very bottom: the funnel moves *structure* freely (a wild idea
is `claimed`) and *status* only on proof. A theme with no proving grounds is a hobby.

*Rebrand discipline (narrative only).* The Unimatrix `factory` **category**, the `factory-*` **agent
types**, and the `product/factory/` **paths** are load-bearing identifiers — they stay as-is. Only the
prose adopts "garage"; renaming the identifiers is a data migration, not a rebrand. (The full
narrative pass across CLAUDE.md / methodology / decisions / skills is a separate, deferred method-PR.)

---

## How a scan reads — four surfaces, two legs, one finish line

**Binding on every theme below.** This section replaces the per-theme `source-mix: TBD` that left every
scout defaulting to product pages and code repositories.

*Why it exists.* The first workflow-harness scan (wfh-001) came back with roughly thirty shipped tools and
no theory. The run that followed it (wfh-004) then generated 128 candidate abilities against **zero
research literature**, and the material that ultimately reframed the theme — a thirty-year body of work on
deriving authorization from process definitions, plus the capability-security lineage — arrived through an
owner conversation *outside the funnel entirely*. The aperture was set wrong, in configuration, and it cost
a full run.

### The four surfaces

Each surface answers a **different question**. A scout told only "read more widely" returns a bibliography;
a scout given the question returns a verdict.

| Surface | The question it must answer | A thin answer looks like |
|---|---|---|
| **Research literature** | Is this already solved, formally characterized, or proven impossible? What are the known bounds, complexity results, and named failure modes? | a reading list with no verdict |
| **Established products** | Does it exist commercially already? What is its **real scope against our need**, what does it cost, and what does adopting it lock us into? | a feature list instead of a scope-versus-need gap |
| **Active development** | Is someone building this *right now*, how far have they got, and is the window closing? | a star count |
| **Adjacent prior art** | Has another field solved the **structurally identical** problem under a different name? | "nothing found," without naming which fields were checked |

**An unread surface is a declared hole, never a silent omission.** Every scan states which surfaces it
touched and which it deliberately skipped, with the reason. This is the same honesty rule the methodology
applies to coverage (§6): a judgment is legitimate when it is visible and specific.

### Two legs on every recurring scan

- **Warm leg — what moved.** Walk the theme's watchlist and check for deltas since the last look. Cheap,
  fast, high signal density.
- **Cold leg — what nobody flagged.** A **protected minimum** of the scan's effort spent reading outside
  the watchlist, on a surface the theme has not touched recently.

The cold leg is protected because the warm leg is cheap, satisfying, and produces visible output — left
unprotected it crowds out cold searching inside about three cycles, and the theme becomes a very
well-organized echo. **A scan that reports no cold-leg spend has not completed.**

### The watchlist (steering config — lives here, not in the graph)

Four fields per entry, and no more: **what** we're watching · **which part of the theme** it feeds ·
**what change would make it interesting again** (the re-check condition) · **when we last looked**.
Entries may be people, organizations, repositories, products, standards bodies, or conference tracks.

*Derived, not curated.* A hand-tended list goes stale silently — the same failure the method rejects
everywhere else in favour of a live query. So the watchlist is **computed from our own evidence**: every
citation carries `author` / `org` / `year` provenance and the `surface` that found it (**D14**), which
makes "who keeps appearing" a calculation rather than a memory.

```
context_lookup(category:"finding", tags:["theme:<slug>"], limit:N)
  → parse each entry's cites: block
  → count distinct org / author across findings AND across scans
  → an entity in ≥K findings spanning ≥2 scans is a watchlist candidate
  → tally by `surface` — a surface that never appears in a citation is being staffed, not read
```

The `surface` tally is the honest check on this whole standard: it is how we find out whether the four
reading surfaces are actually being read.

*What it is not.* Sources remain a **field**, never a node and never a `Cites` edge (D8, unchanged), so
this is a fetch-and-parse rather than a native graph query — tractable because findings-per-theme number
in the tens. And there is **no backfill**: findings written before D14 carry unstructured citations, so
the derivation only becomes useful as new ones accumulate. Until then the watchlists below stay
hand-seeded, and the theme review reconciles the derived candidates against them — adding what the
computation surfaced, pruning what has gone quiet. Near-duplicate name spellings are reconciled at that
review, not by the schema.

### The coverage grid — the finish line

A theme declares the **dimensions** it cares about and the **lenses** it looks through. The grid is their
cross-product. A scan is complete when **every cell is either populated or explicitly declared a hole
naming which lens failed to see it.**

*Default lens set*, carried forward from the harness run that validated the shape — a theme overrides or
extends it, but does not silently drop it: **cross-domain transplant** (what does another field do here) ·
**constraint inversion** (what if the binding constraint were removed) · **adversarial / failure-mode**
(what breaks this, and how) · **scale extrapolation** (what changes at 10× or 1/10×) · **incumbent gap**
(what the existing thing structurally cannot express) · **minimality** (what is irreducible versus merely
current practice). The run that mapped harness abilities had to invent this mid-flight
because the method supplies a coverage rule for narrow research scopes and none at all for divergent
scanning; this generalizes it.

**"More research needed" is a legitimate verdict only when it names the specific empty cell driving it.**
That is what keeps the wide mouth honest without rushing it — the owner's gate lands on the holes, not on
a feeling.

### Assembly is the default answer

A scan exists partly to make building unnecessary. If the theme can be **assembled** from things that
already exist, that is the finding, and it is a good one. **A build recommendation carries a burden of
proof: it must name the specific thing assembly cannot deliver.** See the triage verdict set in
`.claude/agents/factory/goal-owner.md` §B.

Watch the eighty-percent case, because it is where the damage lives: existing pieces will usually cover
most of a theme, and the uncovered remainder is routinely the **load-bearing** part — the enforcement
seam, the thing that makes a guarantee rather than a tendency. An assembly verdict must therefore state
*which* part is uncovered and whether that part is the differentiating one. Otherwise "assemble" quietly
becomes "adopt something that does not do the important thing," and we learn it during the build, which is
the cost this whole section exists to avoid.

### A scan may reshape its own theme

A scan is permitted to return a **proposed revision to the theme itself** — a different framing, a changed
lens, a retired value-target — as a first-class output alongside its candidates. It goes to the owner at
the triage gate, where theme changes belong, and it **never rewrites the scan that produced it**.

This is a direct repair. The ontology run (wfh-002) closed early because a reframing arrived mid-run with
nowhere legitimate to go, became an unauthorized workstream, and took the run down with it. Capture is
free; commitment is gated; the reshaping is the owner's call.

---

## theme:smart-edge — smarter systems on edge-capable devices
**Status:** active · seeded 2026-07-07

**Lens.** Technologies that make systems *smarter on edge-capable / resource-constrained devices* —
especially **non-LLM** approaches to **text processing, sorting, and pattern recognition**, and
**low-memory** capabilities including Small Language models, quantized or otherwise. The bias is deliberately toward classical / lightweight / deterministic
techniques (grammars, automata, compact indexes, streaming/approximate algorithms, structured pattern
matchers) that buy capability *without* a large model or large memory footprint. LLM-centric approaches
are out of lens unless they materially reduce the resource envelope.

**Value-targets** *(kept as a distinct axis from the lens — a technology can serve the theme yet not a
use-case, or vice versa; score on both):*
- **#1 — Unimatrix** (`dug-21/unimatrix`, this repo's own MCP knowledge engine; dogfooded here, so its
  capability surface is fully knowable — the MCP tool set + the repo). First-class hunting ground for
  where a smart-edge technology could enhance an existing capability (e.g. `context_cycle_review`
  hotspot/pattern detection, `context_search` ranking, tag/text normalization).
  - **Implementation substrate (load-bearing for scoring):** the server is a **Rust binary**; the client
    is a **dumb JS/TS shim** (so intelligence must live server-side, in Rust). A candidate that has a
    **Rust-native crate** can live *in the server binary* (no external process/FFI) — this is a
    first-order fit/effort discriminator the surface inventory MUST carry, not just the MCP interface.
    Already built-in: a **PII scanner** (new safety ideas here are *improve the existing*, not greenfield).
    The owner **owns the platform** — so "platform walls" (e.g. mid-cycle buffer access, new endpoints)
    are *liftable*, not hard constraints; triage must not park a hypothesis on a wall the owner can move.
- *(others as they arise — the theme is not Unimatrix-only)*

**Reading surfaces** *(the four, per "How a scan reads"; owner-injection remains a valid entry at any time
and flows through triage identically):*
- **Research literature** — compact/succinct data structures, streaming and sketch algorithms, formal
  language theory and automata, information retrieval and learned-sparse ranking, quantization and
  distillation. Venues worth naming: SIGIR · VLDB · ALENEX/SEA · ACL and EMNLP efficiency tracks · arXiv
  `cs.IR`, `cs.DS`, `cs.CL`.
- **Established products** — embedded and edge search engines, on-device NLP toolkits, commercial
  small-model runtimes. The question is scope-versus-need and licence, not features.
- **Active development** — Rust crates in the text/index/automata space (this is the fit discriminator:
  the value-target's server is a Rust binary, so a Rust-native crate can live in-process), plus fast-moving
  quantized-runtime repos.
- **Adjacent prior art** — compiler and parser construction, spell-check and autocomplete, bioinformatics
  sequence indexing, telecom and network stream processing, spam and intrusion detection. All four have
  solved "recognize structure cheaply on constrained hardware" under different names.

**Coverage grid — dimensions** (crossed with the default lens set): search and ranking quality · pattern
and hotspot detection · text normalization and tagging · compact indexing and storage · safety and PII
scanning (improve the existing scanner, not greenfield) · resource-envelope reduction.

**Watchlist.** *Empty — populate on the next scan.* Seeded by hand until author and organization are
carried in the citation structure; prune at each theme review.

**Cadence.** Target **weekly** (owner intent: 1–2 days/week external research, other days closing goals).
**Wave-0 = manual kick** — autonomous scheduled scanning is gated on the budget-metering capability
(proposal §8) and is a later wave. Recommended path: prototype the hypothesizer manually (via AB-001)
and measure the funnel hit-rate before automating.

**Source signals to label** *(guard against dogfood over-fit — proposal §11):* tag each candidate's
origin as `owner-injection` · `external-scan` · `dogfood-signal` so the portfolio isn't accidentally fit
to one operator's friction.

**First candidate (seeded, not yet run).** Owner-injected generative-grammars / low-memory non-LLM text
processing — run end-to-end through the `theme-scan` (candidate → hypothesizer fan-out over Unimatrix's
capability surface → triage → shortlist) as the theme's first exercise.

---

## theme:daystrom — a world-class R&D garage that sharpens its own tools
**Status:** active · seeded 2026-07-08

**North-star.** Build a **world-class research & development capability** by continuously scanning for —
and rigorously vetting — external tools, techniques, and practices that could make the garage's *own*
process faster, better, or cheaper. Daystrom is the theme pointed **inward at the process plane**: where
`smart-edge` hunts technologies for research *goals*, daystrom hunts technologies for the **garage
itself**. (Named for the Daystrom Institute — the Federation's R&D house — and its M-5 cautionary tale:
a real breakthrough deployed *without proving* is a disaster. Every daystrom candidate is an M-5 that
must survive the proving grounds before it is trusted.)

**Lens.** External (often free/OSS) tools, frameworks, techniques, or practices that could
**accelerate, improve, or replace a garage *process* capability** — e.g. agent orchestration,
evaluation/telemetry, knowledge-graph & retrieval tooling, workflow/gate engines,
verification/testing harnesses, prompt/context tooling. In lens = it changes how the *garage runs*;
out of lens = it's a research subject for a goal (that belongs to a research-plane theme like
`smart-edge`).

**Value-target = the process plane itself.** Score each candidate on which garage capability it could
improve (the "am I autonomous yet" board under factory-goal #19):
- #25 orchestrate a phase-gated run · #26 decompose → board · #27 research → graded landscape ·
  #28 prove-with-artifact (firewall) · #29 synthesize · #30 live frontier query · #31 human-via-Issue ·
  **#66 improve-its-own-workflow (the reflexive loop).**
- A candidate with no line to a process capability is out of lens, however shiny.

**Outputs live on the process plane (§9).** A daystrom candidate is stored as
**`category:factory, kind:technology`** (an *enhancement idea* — the process-plane backlog), tagged
`theme:daystrom` + run-id, `grade:claimed`. Edges are **factory→factory only**; it never links to a
research node. This keeps it invisible to research retrieval and makes daystrom the standing
**generator** for the §9 A/B backlog.

**Firewall — process-proof is an A/B, not a POC.** A daystrom candidate reaches `proven` ONLY via
**comparative telemetry** — a `wf:`-sliced A/B yield comparison (the reflexive loop, §8), demonstrated
by us — never on "this tool looks better." Structure moves freely; status waits for the A/B. This is
the concrete work that finally advances capability #66 from `claimed`.
- **Augment > replace bar.** *Adding* a tool alongside the process clears the normal A/B bar.
  **Replacing** a core process tool clears a higher one — swapping load-bearing machinery mid-maturation
  destabilizes the operating model (current focus: single→multi-goal). Prefer augment; gate replace
  behind a stronger A/B + a human call.

**Budget & cadence.** Fits the owner's ~1–2 days/week external-research envelope; **wave-0 = manual
kick**. **Magpie guard:** the hazard of an inward tooling theme is chasing shiny tools instead of
closing goals — cap the spend and require a plausible process-capability line before a candidate
advances past scan.

**Reading surfaces** *(the four; label every candidate's origin `owner-injection · external-scan ·
dogfood-signal` — daystrom is inward by intent, so dogfood-fit is the point rather than the over-fit hazard
`smart-edge` guards, but origin still gets labelled for portfolio hygiene):*
- **Research literature** — empirical software engineering on developer productivity, agent evaluation and
  benchmark design, experiment design for A/B on small samples (our A/B population is *runs*, and there are
  few of them — the statistics matter), retrieval-augmented generation evaluation, knowledge-graph tooling.
- **Established products** — agent orchestration platforms, evaluation and observability suites, workflow
  and gate engines, research and knowledge management tooling. Cost and lock-in are first-class here
  because adopting one changes how the garage runs.
- **Active development** — agent-framework and evaluation-harness repos, MCP server ecosystem, prompt and
  context tooling. High churn; the warm leg earns its keep on this surface.
- **Adjacent prior art** — laboratory information management and electronic lab notebooks, systematic
  review methodology (the discipline that formalized "have we covered the literature?"), clinical trial
  protocol design, manufacturing process control and statistical quality control.

*Systematic-review methodology deserves the explicit call-out:* it is a mature field whose entire subject
is coverage, screening, and inclusion criteria for a literature scan. The garage keeps re-deriving pieces of
it by hand.

**Coverage grid — dimensions** (crossed with the default lens set): orchestration and spawn control ·
gate and verdict machinery · evaluation and telemetry · knowledge capture and retrieval · cost metering and
budget · human steering surfaces · reproducibility and audit.

**Augment before replace** (unchanged, and it binds triage): adding a tool alongside the process clears the
normal A/B bar; **replacing** load-bearing machinery mid-maturation clears a higher one plus a human call.

**Watchlist.** *Empty — populate on the first scan.* This theme has run **zero scans since it was seeded**;
that is the single largest coverage debt in the file.

**First candidate (not yet run).** Owner-injection, TBD — run one tool end-to-end (scan → hypothesizer
over the process-capability surface → triage → shortlist → A/B) as the theme's first exercise, and to
measure the funnel's process-plane hit-rate.

---

## theme:workflow-harness — the control plane that drives the LLM, made visible
**Status:** active · seeded 2026-07-22

**Lens.** Context-injection & control architectures for LLM **coding agents**: how a harness *owns and
injects* the operating context (skills, agent-definitions, protocols/workflows, tools, gates) into the
LLM, and *structurally enforces* gates + access boundaries the LLM cannot circumvent — the LLM a
**directed, supporting component, not the driver**. Deliberate bias toward **build-once / any-LLM-pluggable**
designs that reduce vendor-ecosystem lock-in (the durable asset is the harness + its graph; the LLM is a
swappable backend). Claude-Code / coding-agent mechanisms are in-lens as *reference implementations to
generalize from*, not endpoints.

**Value-target #1 — JURATI** (`dug-21/jurati`, "the Queen"). The deterministic control model in front of
the substrate — the single edge where all LLM calls originate; enforcement (identity, per-agent capability
gating, sequencing, budget) lives here, **outside the LLM context**. Grounded in the ratified
Unimatrix↔JURATI joint recommendation (**JURATI issue #12**), **ASS-009** (control-model PoC — "ship one
control model, the controller"), **ass-100/101** (edge-minted identity → single-root delegation → Anchor B).
Dogfoodable like Unimatrix (repo + capability board knowable). Proven findings hand off as issues to
`dug-21/jurati`'s SDLC (§7 product bridge) — the factory proves, JURATI ships.

**Plane — research (feeds JURATI's delivery).** This garage *researches and proves* the ontology +
injection/gating model; JURATI *productizes* it (queen executes, ships the UI/ecosystem). *Reflexive-for-
later (D10):* the Queen is a candidate to eventually become **this garage's own** harness (retiring the
current "LLM-is-the-harness" model here) — a `daystrom` / process-plane, higher-bar move, architected-now /
deferred, NOT this theme's build.

**Load-bearing boundary — workflow ≠ knowledge.** The executable workflow (agent-defs / skills / steps /
gates + edges) and its runtime state (token spend, live errors) are **not** Unimatrix knowledge and must
not be stored as graded, decaying, retrieval-ranked evidence — doing so makes Unimatrix an **orchestrator**,
which the joint rec (issue #12) explicitly forbids. **Three layers, three owners:** *Unimatrix* = knowledge;
*queen* = workflow definition + execution + telemetry; *canvas* = a view overlaying them across a
`cites:`-style **reference** seam (never a merged graph). Open fork this theme must resolve: does the
workflow-*definition* layer reuse Unimatrix's graph engine in a hard-isolated plane, or run on a separate
substrate?

**Reading surfaces** *(the four; label every candidate's origin `owner-injection · external-scan ·
dogfood-signal`. Owner-injection stays heavy here — the value-target already has a ratified architecture and
PoCs — but it is no longer the only surface, which is what the first scan effectively made it):*
- **Research literature** — workflow and task-based authorization, separation-of-duty and workflow
  satisfiability, capability security and confused-deputy avoidance, information-flow control, policy
  verification and symbolic policy analysis, and the recent agent-authorization / over-privilege
  measurement work. Venues: CCS · S&P · USENIX Security · ESORICS · SACMAT · OOPSLA · arXiv `cs.CR`.
- **Established products** — CI/CD platforms with derived job identity, workload-identity systems, policy
  engines, secrets and credential brokers, commercial agent platforms with an authorization story. Ask
  scope-versus-need and lock-in, not features.
- **Active development** — agentic-workflow compilers, MCP authorization proposals, agent frameworks with
  a gate or approval model, sandbox and tool-permission layers. Highest-churn surface in the theme.
- **Adjacent prior art** — operating-system capability models, business-process management and workflow
  engines, distributed-systems delegation and attenuation, supply-chain attestation, and safety-critical
  domains with a formal gate concept (aviation, nuclear operations, medical device approval). The harness
  run already mines these for *mechanism generation*; they are now also a **reading** surface.

**Verification debt — partially discharged by wfh-005 (2026-08-01). The absence-of-prior-art claim is
FALSIFIED and is struck.** An unconstrained conversation outside the funnel asserted roughly thirty
references and a novelty claim on phase-indexed derivation. wfh-005 attacked both from four reading
surfaces. What it found:

- **The novelty claim does not survive.** All three legs have prior art, reached independently by the
  literature and adjacent-prior-art surfaces via different routes. Phase-indexed authority is Task-Based
  Authorization Controls (Thomas & Sandhu, 1997) and the Workflow Authorization Model (Atluri & Huang,
  1996). Gate independence appears under four names for one invariant — Clark-Wilson enforcement rule E4
  (1987), DO-178C verification independence, SLSA Build L3 non-falsifiable provenance, and measured boot.
  A ceiling derived from declared demand ships in WASI, Bazel, Nix, in-toto, and `gh aw compile`.
  **What remains is a composition claim, not an absence claim, and it must be argued by name against that
  prior art rather than asserted.** Residual caveat: **patents were never searched**, so even the narrowed
  residual is an *unverified absence* rather than an established one.
- **The reference set itself was never recorded.** It is not in Issue #48's body or comments, nor anywhere
  under `product/research/wfh-004/`. An unrecorded citation set cannot be verified, deduped, re-checked by
  a later scan, or used to seed a derived watchlist — the failure mode D14 exists to prevent, one level
  upstream of where D14 operates. **Do not cite a count of references as evidence of anything.**
- **What was verified is the theme's description of six fields, not the citations.** Four clusters resolve
  to real, correctly attributed canonical work. Two do not: the "synthesis-to-runtime-monitor compiler" is
  a field rather than an identifiable work, and "five spec-derived capability systems" is a count with no
  members. **Both are marked unsupported.** A failure rate at cluster altitude is a floor for the failure
  rate at reference altitude, never a ceiling.
- **Naming, load-bearing:** do not ship the gate rule as "soundness" — that word is taken by workflow nets
  and guarantees a misread by the audience most likely to take the claim seriously. Use **gate-input
  independence**, stated in read-set/write-set vocabulary.

*Standing and open:* if the enumerated list is ever recovered, one literature pass discharges the debt
item-by-item. Until then the theme carries the cluster-level claims only. Full verdicts:
`product/research/wfh-005/reports/triage.md` and its two amendments.

**Coverage grid — dimensions** (the eight concerns, which survived the harness run's frame rebuild, crossed
with the default lens set): structure · context provisioning · security · introspection · cost transparency
and management · self-improvement · recovery and durability · human steering. Emergent concerns may be
promoted into the grid; the promotion test lives in that run's scope.

**Watchlist** *(reconciled at wfh-005 close, 2026-08-01 — derivation run first, then reconciled by hand):*

| Watching | Feeds | Re-check when | Last looked |
|---|---|---|---|
| GitHub Agentic Workflows (`gh-aw`) — **the incumbent to beat**; ships mechanisms in 7 of 8 concerns | structure · security · cost · self-improvement | it derives capability from an **author-declared** phase, or leaves technical preview | 2026-08-01 (wfh-005) |
| MCP authorization specification | security | **retightened** — a proposal for per-tool or per-resource scopes opens. The 2026-07-28 revision moved a lot and none of it was authorization granularity | 2026-08-01 (wfh-005) |
| `dug-21/jurati` issue #12 and the ratified joint recommendation | all eight | any amendment to the enforcement seam | 2026-07-25 (wfh-004) |
| Coding-agent permission and hook models (this harness included) | security · human steering | **retightened** — `anthropics/claude-agent-sdk-typescript` #172 closes, or subagent permission-mode inheritance becomes overridable | 2026-08-01 (wfh-005) |
| Agent over-privilege measurement work | security · introspection | a new benchmark or replication lands | 2026-08-01 (wfh-005) — confirmed a dense 2025–26 subfield with code |
| **Cisco Outshift / AGNTCY** — `outshift-casa`, `ASTRA`, `tbac-research-datasets` (Linux Foundation) | security · structure | CASA leaves alpha, gains a non-Istio data plane, or the task-based line publishes a reference implementation | 2026-08-01 (wfh-005) — **new, derived** |
| **`ruvnet`** — `ruflo`, `metaharness`, `agentic-flow` | security · self-improvement · cost | the policy engine ships **enforcing by default**, or the delegation propagator gains call sites | 2026-08-01 (wfh-005) — **new, derived** |
| **`adrianco/retort`** — design-of-experiments evaluation of coding stacks | *(evaluation — a concern the grid does not name)* | replicate counts rise above n=1 on published routes, or the routing feed gains a versioned schema | 2026-08-01 (wfh-005) — **new, derived** |
| Temporal agent plugins | recovery and durability · human steering | a plugin reaches general availability | 2026-08-01 (wfh-005) — **new, derived** |

**Surface tally (the honesty check on the four-surface standard — first measurement, wfh-005).**
158 structured citations across seven scout files: **active-dev 70 · products 32 · literature 30 ·
adjacent 26.** No surface was staffed and unread — the failure the standard was written to catch did not
occur. By type: 47 paper · 44 docs · 43 repo · 14 blog · 6 standard · 4 product. Organisations appearing
in ≥2 findings, which is what promoted the four new entries above: GitHub 18 · ruvnet 16 · OpenAI 5 ·
Cisco Outshift 5 · Amazon Web Services 5 · Microsoft 3 · Anthropic 3 · Temporal 2 · Model Context
Protocol 2.

**Method holes recorded against this list, not hidden.** Three of wfh-005's verdict-moving finds arrived
by owner injection rather than by the method. The active-development surface needs three instruments it
does not have: an **organization-walk**, a deliberately **low-star pass** (the decisive find had 17 stars),
and a **by-function rather than by-vocabulary sweep** (retort self-describes as a "Platform Evolution
Engine" and its README carries none of this theme's nouns). Unspent and still open: **patent prior art**,
and **commercial CD stage-scoped role binding** (Harness, Spinnaker, Azure DevOps).

**Cadence.** Weekly, wave-0 manual kick. First exercise = capture + triage of the seed hypotheses below
(structure-only); graph-formalization (`finding` + `hypothesis` tag, run-id, `theme:workflow-harness`)
happens on the first `theme-scan` run.

**Operating plan & artifacts.** Standing research plan (tracks T1–T5, run queue, systemic funnel):
`proposals/workflow-harness-research-plan.md`. Delivery-model design space (axes A1–A8, paths P1–P14):
`proposals/workflow-harness-delivery-model-paths.md`. First run: **wfh-001** (external landscape scan).

**Seed hypotheses** *(pre-triage, 2026-07-22 — file-captured, NOT yet graph nodes; owner-injection):*
- **H1 — control-plane-as-graph.** A graph structure lets the queen *coordinate* the workflow **and** be
  its *live debugger*, with the queen in control and the LLM given direction from it (one structure, both
  jobs). *Proof-direction: a run where the graph both drives step order and renders the live trace.*
- **H2 — harness-as-observability.** The same harness meters **token spend** and captures problems /
  feedback in **real time**, mapped onto the workflow structure. *Proof-direction: per-step token + error
  surfaced on the canvas as a run executes.*
- **H3 — one JURATI across many repos/domains.** One harness serves multiple projects/domains (this repo =
  research; `unimatrix` dev; `jurati` dev). Two variants: **(A)** the queen *dispatches* work to per-repo
  instances that share one workflow definition; **(B)** one workflow *spans* repos simultaneously. Rides on
  issue #12's **proven** per-slug data isolation + queen-side access governance. *Start with A (cleaner; B
  is architect-for-later). Proof-direction: stand up a new repo on the existing workflow with only a topic
  + Unimatrix-slug setup.*
- **H4 — ontology-first.** The load-bearing object is a **minimal typed vocabulary** of a coding-agent's
  operating context (skill / agent-def / step / gate / tool + a few edges); the canvas and the injection
  are downstream of getting it right. *Proof-direction: express this repo's own `.claude/` context in the
  vocabulary with no loss.*
- **H5 — anti-lock-in as consequence.** If the operating context is a portable typed graph, swapping the
  LLM swaps only the *executor*; the harness/graph stays. Lock-in-avoidance becomes a *property of the
  representation*, not a feature to build. *Proof-direction: run the same workflow graph against two
  different LLM backends.*
- **H6 — build-once ecosystem.** Domains / workflow-types = subgraphs on the shared ontology; "manage tens
  of products" = one engine + per-product knowledge slug. *(Generalizes H3; the multi-product vision.)*
- **H7 — definition vs events, two backends.** The workflow *definition* graph is **stable + versioned**
  (config-like, read-heavy, changes only when an improvement is deliberately tested); *outcomes / telemetry
  / events* are **high-churn, streamed runtime**. They want **different backends** — conflating them repeats
  the workflow≠knowledge error one level down. Net: **three stores** — Unimatrix (knowledge), a versioned
  *definition* store (queen), an *event/telemetry* sink (queen). *Proof-direction: a "right-backend" analysis
  picks a store per layer against its read/write/version/query profile.*
- **H8 — sovereignty-preserving SaaS.** JURATI is built **multi-tenant SaaS from the start** (not a
  single-user tool retrofitted later). Testable premise: it can be SaaS *without betraying the anti-lock-in
  thesis* — **iff** the tenant's workflow graph stays **portable / exportable / self-hostable**, the LLM
  stays pluggable (incl. local), and per-tenant isolation is **mechanical**. **Consequence (issue #12):**
  multi-tenant IS the explicit trigger that promotes the deferred **Anchor-B verifier** from "named seam,
  later" to **foundational, now** — SaaS-from-start pulls the hardest security substrate forward. *Proof-
  direction: a two-tenant deploy where A cannot address B's slug (mechanical, not assumed) AND a tenant can
  export its full workflow graph and run it self-hosted.*
