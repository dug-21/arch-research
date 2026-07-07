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

## theme:smart-edge — smarter systems on edge-capable devices
**Status:** active · seeded 2026-07-07

**Lens.** Technologies that make systems *smarter on edge-capable / resource-constrained devices* —
especially **non-LLM** approaches to **text processing, sorting, and pattern recognition**, and
**low-memory** capabilities. The bias is deliberately toward classical / lightweight / deterministic
techniques (grammars, automata, compact indexes, streaming/approximate algorithms, structured pattern
matchers) that buy capability *without* a large model or large memory footprint. LLM-centric approaches
are out of lens unless they materially reduce the resource envelope.

**Value-targets** *(kept as a distinct axis from the lens — a technology can serve the theme yet not a
use-case, or vice versa; score on both):*
- **#1 — Unimatrix** (`dug-21/unimatrix`, this repo's own MCP knowledge engine; dogfooded here, so its
  capability surface is fully knowable — the MCP tool set + the repo). First-class hunting ground for
  where a smart-edge technology could enhance an existing capability (e.g. `context_cycle_review`
  hotspot/pattern detection, `context_search` ranking, tag/text normalization).
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
