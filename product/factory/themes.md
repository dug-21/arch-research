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

**Source-mix.** *TBD (config knob, not yet resolved — proposal §2/§12).* Candidate surfaces to settle:
web search · arXiv · GitHub-trending · Hacker News · practitioner newsletters/blogs. Until set, the theme
runs on **owner-injection** (the owner hand-feeds a candidate technology — e.g. the generative-grammars /
low-memory non-LLM text article that seeded this theme) which enters the `theme-scan` at the candidate
step and flows through triage identically.

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

**Source-mix.** *TBD (shared knob with `smart-edge` — proposal §2/§12).* Until set, runs on
**owner-injection** + obvious hunting grounds (agent-framework / eval / KG-tooling release feeds). Label
each candidate's origin `owner-injection · external-scan · dogfood-signal`. (Daystrom is inherently
inward, so dogfood-fit is the *intent*, not the over-fit hazard `smart-edge` guards against — but still
label origin for portfolio hygiene.)

**First candidate (not yet run).** Owner-injection, TBD — run one tool end-to-end (scan → hypothesizer
over the process-capability surface → triage → shortlist → A/B) as the theme's first exercise, and to
measure the funnel's process-plane hit-rate.
