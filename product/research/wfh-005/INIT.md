# wfh-005 — INIT record

**Opened:** 2026-08-01 · **Leader:** this session · **Method stamp:** `wf-v0.20` (derived,
`git describe --tags --match 'wf-*'`)

## Three surfaces opened before any spawn (D1 / OBS-10)

| Surface | State |
|---|---|
| **GitHub Issue** | [#54](https://github.com/dug-21/arch-research/issues/54) — `factory`, `scope:research`, `confidence:directional`; body = `ISSUE.md` as drafted |
| **Cycle** | `context_cycle start` topic `wfh-005`, `next_phase: scan`, `tags: ["wf-v0.20"]` (set-once), `agent_id: wfh-005-leader` |
| **Git** | **No branch.** Under **D15** research *documents* land on `main` continuously; this scan writes no executables, so it needs no branch and no PR. The pre-existing `research/wfh-005` branch (SCOPE + ISSUE, already merged to `main` at `fe6d23c`) is vestigial — it predates D15 by one commit. |

## Shape declared at INIT (the advisory gate; the owner's kick is the approval)

- **Mode:** challenge, on all four surfaces. No surface skipped — zero declared holes at the outset.
- **Surfaces staffed:** research literature (W1) · established products (W2) · active development (W3) ·
  adjacent prior art (W4). One scout each, spawned in a single message.
- **Position ownership:** W1 owns P1 (verification table) and leads the P2 attack from the literature ·
  W2 owns P4 and its adopt/assemble/build routing · W3 owns the window-closing call and is the strongest
  surface for P5 · W4 is the primary attack on P2 (the alias hunt) and carries the P3 counter-case from
  fields that have lived with a fallible judge inside a gate.
- **Cold-leg minimum:** protected on every scout, redefined per deviation D-d as the emergent-position
  slot — *"what assumption is this theme holding that nobody put on the list?"* A return with no
  cold-leg content is declared incomplete and sent back.
- **Deviations D-a … D-e** carried as written in `SCOPE.md` §Deviations.
- **Budget:** 10–12 specialist spawns. **Spent at INIT: 4.**
- **No hypothesizer** (D-e). No graph writes before triage (lesson #172).

## Coverage grid — 5 positions × 4 surfaces = 20 cells

Filled at W5 (cross-surface reconciliation). A cell is complete when it is populated **or** explicitly
declared a hole naming the surface that failed to see it.

| | W1 literature | W2 products | W3 active-dev | W4 adjacent |
|---|---|---|---|---|
| **P1** citation set is real | *owner* | | | |
| **P2** novelty / absence claim | *lead attack* | | | *primary attack* |
| **P3** minimize inference | | | | |
| **P4** build is necessary | | *owner* | | |
| **P5** demand is real | | | | |

## Finding at INIT — the P1 reference set is not written down anywhere

**Recorded here because it is a P1 sub-finding, and because it changes what W1 can do.**

`themes.md` → `theme:workflow-harness` → *Standing verification debt* asserts roughly thirty specific
owner-injected references and says: *"Full text: the owner conversation attached to Issue #48."*

It is not attached. The leader checked, at INIT:

- Issue #48 body and **both** of its comments — no reference list (the two comments are the wfh-004
  scope and its amendment; neither carries citations).
- `product/research/wfh-004/**` — the surface files, the two hypothesis rounds, `W6-DISTILLED.md`, and
  `reports/triage.md`. No enumerated reference list.
- Repo-wide grep for arXiv identifiers and for the confused-deputy lineage — hits only in
  `themes.md`, `decisions.md`, the methodology, this run's `SCOPE.md`, and two wfh-004 hypothesis
  lenses, none of which enumerate the injected set.

**Consequence.** P1 as literally scoped — *"confirm each reference exists and says what it is claimed to
say"* — is **not executable against the list**, because the list does not exist as an artifact. That is
itself a provenance failure worth more than a clean verification pass would have been: **the theme carries
a standing verification debt against a citation set that was never recorded.** An unrecorded citation set
cannot be verified, cannot be deduped, cannot seed a derived watchlist (D14), and cannot be re-checked by
a later scan. It is exactly the failure mode D14 was written to prevent, one level upstream of where D14
operates.

**What W1 was instructed to do instead.** Verify the six *described clusters* — the substantive test that
is still available. For each cluster (workflow authorization from the mid-1990s · a synthesis-to-runtime-
monitor compiler · workflow-satisfiability complexity results · five spec-derived capability systems ·
several 2026 agent-authorization papers · a confused-deputy lineage), identify the canonical work the
description can only be pointing at and establish whether it exists, is attributed correctly, and supports
the claim made of it. A cluster with **no such work** is the falsification. This tests the honest question
— *is there a real literature behind these claims?* — without pretending to audit a list nobody has.

**Open to the owner (non-blocking).** If the original conversation still exists, dropping the enumerated
list into Issue #54 makes an item-by-item verification pass possible; a grid-targeted round-two W1 would
discharge it. If it does not exist, the cluster-level verdict stands as the discharge of the debt, and the
theme's verification-debt paragraph should be rewritten to say what was actually verified.
