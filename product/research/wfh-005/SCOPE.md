# wfh-005 — Challenge scan: attack the five positions `theme:workflow-harness` is standing on

**Status:** SCOPE
**Goal(s):** `theme:workflow-harness` → value-target **JURATI** (`dug-21/jurati`)
**Capability target(s):** none directly — this run tests the *premises* under the harness capability
space produced by wfh-004; it advances no capability and closes no `done_when`
**Confidence-required:** directional — **structure only, nothing reaches `proven`**
**Phase / area:** wide mouth → neck (theme-scan, **challenge mode**)
**Cycle topic / Issue:** `wfh-005`
**Method stamp:** derived at INIT (`git describe --tags --match 'wf-*'`) — first run under the
wide-mouth standard (wf-v0.17 / wf-v0.18 / wf-v0.19)

---

## The question

wfh-001 scanned the harness landscape. wfh-002 specified an ontology and closed early without an
artifact. wfh-004 mapped 128 candidate abilities and sits parked at its owner gate. Every one of those
runs added structure on top of premises **nobody has attacked** — most of them arriving by owner
injection or from our own incident log, none of them read against the research literature.

> **Are the five things this theme is standing on actually true — and if they are not, what shape does
> the theme take instead?**

This is a **challenge scan**, not a discovery scan. Discovery finds what we lack; it structurally cannot
report that something we already believe is solved, superseded, or wrong. That is this run's entire job.

## Why it matters

Three consecutive structure-only runs, zero `proven` nodes on either board, and a shortlist of 51
build-routed abilities waiting at a gate. Committing to any of them means committing to premises that
have never been tested. **The cheapest possible moment to discover a false premise is now** — before the
gate, before a proof-goal, and long before a build. If the premises hold, the gate decision is made on
firmer ground. If one breaks, we save the run it would otherwise have cost.

## Known constraints & prior art *(build on these — do not re-derive)*

- **wfh-002's four durable verdicts** (#177, #178, #179, #181): the ontology round-trip passed with two
  genuine vocabulary holes (LLM-arbitered gates, missing condition construct); `AGENTS.md` is subsumed
  non-vacuously; the vocabulary is domain-agnostic with three structural general-workflow holes; and this
  repo's cardinal invariants are unenforced prose. These stand — do not re-litigate them.
- **#185** — rule *evaluation* is queen-side, independent of product purpose. Durable; not under test.
- **#184** — the Option C architecture position is explicitly **provisional and non-binding**. Not under
  test here, and this run must not settle it.
- **#183** — the ontology technology node, `grade:claimed`. Not under test.
- **wfh-004's surface work** — `W0-a` landscape (~30 shipped tools), `W0-c` constraints C-1…C-4,
  `W0-e` LLM component envelope, `W0-f` conformance census. Reuse as reference; do not regenerate.
- **wfh-001's filed technologies** (#143, #146, #150, #159 and siblings). Dedup against these first.
- **The theme's own standing verification debt** (`themes.md` → `theme:workflow-harness`) — this run is
  the one that discharges it.

## The five positions under test

Each is stated as the theme currently holds it, with its origin, what would falsify it, and why it
matters. **A scout's job is to attack, not to confirm.** A position that survives an honest attack is
worth far more than one nobody tried to break.

### P1 — The citation set is real and says what it is claimed to say
*Asserted:* roughly thirty references surfaced by owner injection (2026-08-01) — workflow authorization
from the mid-1990s, a published synthesis-to-runtime-monitor compiler, workflow-satisfiability complexity
results, five spec-derived capability systems, several 2026 agent-authorization papers, and a
confused-deputy lineage.
*Origin:* an unconstrained conversation outside the funnel. All `claimed`; none verified.
*Falsified by:* a reference that does not exist, is misattributed, or does not support the claim made of
it. Recent arXiv identifiers deserve the most scrutiny, older canonical work the least.
*Why it matters:* every other position below is argued partly from these. If the foundation is
fabricated, the argument built on it is worthless — and mechanically checkable in hours.

### P2 — The novelty claim: phase-indexed derivation and gate independence are unpublished
*Asserted:* deriving a capability set from `(workflow, phase, agent-role)` is unclaimed; a soundness rule
for transition gates (*every input to a gate predicate lies outside the write-set of the phase being
exited*) has no prior art; deriving the over-granting **ceiling** from a spec's declared demands, rather
than hand-writing it, is unpublished.
*Origin:* the same conversation, as an absence-of-prior-art claim.
*Falsified by:* anyone doing it. Look hardest where it would be named differently — business-process
authorization, capability security, workflow satisfiability, information-flow control, staged build
systems, supply-chain attestation.
*Why it matters:* this is the theme's moat. **An absence claim is the hardest thing to establish and the
easiest for a model to assert**, and this one was asserted by a model. Report the venues searched and what
you expected to find, so a negative result is legible rather than merely unopposed.

### P3 — The product thesis: minimize inference; determinism is what makes a guarantee
*Asserted:* inference anywhere on the enforcement path demotes a guarantee to a tendency, so the harness
minimizes the number of parts where a model call is structurally irreducible (wfh-004 amendment A-8;
candidate C-04; the `inference-minimality` lens).
*Origin:* owner position, elaborated inside wfh-004. Never attacked from outside.
*Falsified by:* either direction — systems achieving hard guarantees **with** inference on the path
(checked output, verified generation, adjudicated proposals); or evidence that deterministic enforcement
is insufficient in practice. Note our own field record cuts against the naive version: **both** of this
operation's real encounters with an enforcement plane ended in an institutionalized bypass.
*Why it matters:* wfh-004's entire register is organized around this thesis. If it is wrong, or right only
under conditions nobody stated, the shortlist is sorted by the wrong key.

### P4 — Build is necessary: nothing shipping or assemblable covers this
*Asserted:* implicitly, by three runs that never asked. wfh-004 generated 128 abilities with **no
buy-before-build evidence** — that requirement did not exist until wf-v0.17.
*Origin:* never stated, never tested. The nearest shipping instance (GitHub Agentic Workflows) was
characterized in wfh-001 and never evaluated for adoption or assembly.
*Falsified by:* a product, or a composition of products, whose scope covers the eight concerns well
enough. Gather the buy-before-build evidence properly: **scope against our need — specifically what it
does not cover** · cost and licence · lock-in and exit · composability.
*Why it matters:* this is the position whose falsification would be the **best** outcome available. It is
also the one the new triage verdicts (adopt / assemble) exist to receive, and this is their first use.
Watch the eighty-percent case: name the uncovered remainder precisely, because it is routinely the
load-bearing part.

### P5 — The demand is real: this answers someone's problem, not only our incident log
*Asserted:* that the 128 abilities constitute a product requirement set.
*Origin:* wfh-004's own triage said the opposite out loud — *"128 abilities and zero users… every
candidate is justified by a failure of ours… read cold, the register is a defect list, not a product
requirement list."* Nobody acted on it.
*Falsified by:* absence — no external evidence that others hit these failures, or evidence that the
problems people actually report are different ones. Look for practitioner accounts, incident write-ups,
issue trackers on comparable tools, and what buyers of adjacent products ask for.
*Why it matters:* it decides whether this is a product or a very well-engineered post-mortem machine.

## Bounded investigation (workstreams)

**One scout per reading surface, all four spawned in one message, each attacking all five positions from
its own surface.** (Deviation D-a — see §Deviations.) Each carries the theme's watchlist entries for its
surface, and a protected **cold leg**.

- **W1 — Research literature.** Is this already solved, formally characterized, or proven impossible?
  Verify P1's references directly; attack P2 hardest here; find the counter-case for P3.
  Venues: CCS · S&P · USENIX Security · ESORICS · SACMAT · OOPSLA · arXiv `cs.CR`.
  *Output:* `scout-literature.md` — per-position verdict with evidence, plus a per-reference
  verification table for P1 (exists · attributed correctly · supports the claim made of it).
- **W2 — Established products.** Does it ship? Owns **P4**. Also: what do vendors claim about P3?
  *Output:* `scout-products.md` — per-position verdict, plus buy-before-build evidence per serious
  candidate (scope-vs-need gap, cost, lock-in, composability).
- **W3 — Active development.** Is someone building it now, how far, is the window closing? Second
  opinion on P4 and P2 (an unpublished idea may still be *implemented*).
  *Output:* `scout-active-dev.md` — per-position verdict; maturity separated from ambition.
- **W4 — Adjacent prior art.** Has another field solved the structurally identical problem under a
  different name? Primary attack on P2, secondary on P3 and P5. Hunting grounds: operating-system
  capability models, business-process management, distributed-systems delegation and attenuation,
  supply-chain attestation, safety-critical domains with a formal gate concept.
  *Output:* `scout-adjacent.md` — per-position verdict, each find named in **its** field's vocabulary and
  translated into ours.

- **W5 — Cross-surface reconciliation (leader, after W1–W4 return).** The same idea will appear under
  four names. Scouts cannot see each other and can only flag suspected aliases; the leader merges.
  *Output:* `scout-merged.md` + the filled **coverage grid**.
- **W6 — Verdict synthesis (`goal-owner`).** Per-position verdict, the coverage call, the buy-before-build
  routing for P4, and any theme-revision proposal, relayed verbatim.
  *Output:* `reports/triage.md`.

**Round two is grid-targeted, not automatic:** cells left thin or empty after W5 get one further pass,
handing back round one's output. A cell no surface can populate is recorded as a **hole naming which
surface failed to see it** — that is a finding, not a gap to hide.

## Coverage — the finish line

The grid is **five positions × four surfaces = 20 cells**. The scan is complete when **every cell is
populated or explicitly declared a hole naming the surface that failed to see it.** (Deviation D-b.)

Exhaustion is honestly bounded: it is relative to these five named positions and these four named
surfaces, never absolute. Say so in the report.

**Cold leg (required, and it is the emergent-position slot).** Each scout reserves a protected minimum of
effort for reading *outside* both the watchlist and the five positions, answering: **what assumption is
this theme holding that nobody put on the list?** A sixth position surfaced here is the single
highest-value thing this run can produce. **A scout return with no cold-leg content is incomplete.**

## Verdicts

Per position (Deviation D-c):

| Verdict | Means |
|---|---|
| **SURVIVES** | attacked honestly from every staffed surface and held. Say what the strongest attack was. |
| **WOUNDED** | true only in a narrower form. **State the narrowing** — this is the most common and most useful outcome. |
| **FALSIFIED** | demonstrably wrong. Name the counter-evidence and what it implies downstream. |
| **NEEDS-A-PROBE** | not resolvable cheaply from outside. Name the one question, and what each answer would decide. |

**P4 additionally routes** through the standard triage verdicts — **ADOPT / ASSEMBLE / BUILD** — with
their required fields: assemble names which part is uncovered and whether it is the differentiating one;
build names the specific thing assembly cannot deliver.

## Expected output

1. Four per-surface scout files with per-position verdicts and cold-leg records.
2. A **per-reference verification table** discharging the theme's standing verification debt (P1).
3. The filled **coverage grid**, holes named by surface.
4. `reports/triage.md` — the five verdicts, the coverage call, P4's adopt/assemble/build routing, and any
   emergent sixth position.
5. A `position` finding per resolved position, with structured `cites:` carrying `author` / `org` / `year`
   / `surface` (D14) — this run seeds the theme's **derived watchlist**.
6. `Contradicts` findings wherever external evidence opposes a claim we hold.
7. Any **theme-revision proposal**, relayed verbatim to the owner gate.
8. The **surface-yield tally** — which of the four reading surfaces actually produced anything. This is
   the first measurement of whether the wf-v0.17 standard works.

## Proof bar

**None — structure only. The firewall is untouched by construction.**

One distinction the run must not blur: **verifying that a citation exists does not make its claim
`proven`.** It makes the citation real. Literature by citation stays `claimed` no matter how well
attributed — proof requires an artifact demonstrated by us, at the claim's altitude (D7). A challenge scan
may *lower* our confidence in a claim, sharpen a node's content, or record a contradiction. It never
raises status.

## Explicitly out of scope

- **Architecture and mechanism selection.** This run does not settle Option C (#184), does not choose a
  substrate, and does not decide the definition-versus-events backend question (H7).
- **Any build, POC, or artifact.**
- **Decomposition into a capability board** — that is a later run.
- **The premises H6 (build-once ecosystem), H7 (two backends), H8 (SaaS-from-start).** Real and untested,
  but this run is already carrying five positions; adding three more guarantees none are done properly.
  Parked, re-enter as a second challenge scan.
- **The hooks-and-permissions probe** — already queued from wfh-004's probe queue as a follow-on.
- **wfh-004's triage gate itself.** This run **informs** that decision; it does not make it, and it does
  not promote, park, or re-route anything on that shortlist.

## Relationship to wfh-004 (read this before spawning)

wfh-004 is **open and parked at its blocking owner gate** (Issue #48, branch `research/wfh-004` at the W7
triage commit, cycle still running). The wf-v0.17 governor says: do not scan a theme that already carries
an untriaged shortlist — surface it to the owner first. **That governor fired, and this run is the owner's
answer to it:** a bounded challenge scan run *specifically to inform* the wfh-004 gate, because the
verification debt sits directly upstream of the build-versus-assemble decisions waiting there.

That makes one rule binding: **wfh-005 must not touch wfh-004's shortlist.** It tests premises and hands
back verdicts. The gate stays the owner's, unresolved, until they rule on it.

## Deviations from the theme-scan protocol *(carried for owner sign-off at the INIT gate)*

- **D-a — workstreams are surfaces, not question-partitions.** Four scouts, one per reading surface, each
  attacking all five positions. The standard protocol partitions by question; a challenge scan partitions
  by *where you look*, because the same position gets different answers from literature and from products.
- **D-b — the coverage grid is positions × surfaces**, not dimensions × lenses. The standard permits a
  theme to override the default lens set; for a challenge scan the surfaces *are* the lenses.
- **D-c — verdict vocabulary is per-position** (survives / wounded / falsified / needs-a-probe), with the
  standard adopt/assemble/build routing applied only to P4.
- **D-d — the cold leg is redefined** as "name an assumption nobody put on the list," making it the
  emergent-position slot rather than general cold reading.
- **D-e — no hypothesizer.** A challenge scan does not generate candidates; the divergent step is the four
  surfaces attacking in parallel. If the run wants a hypothesizer it has drifted back into discovery.

## Budget envelope

**10–12 specialist spawns**: 4 surface scouts · up to 4 grid-targeted round-two passes · 1 curator ·
1 goal-owner. Deliberately under wfh-004's 18–22 (which overran to ~30) — a challenge scan is bounded by
the number of positions, not by generative range. **An out-of-envelope change is a blocking question to
the owner, not an in-envelope steer the leader absorbs.**

## Gates

1. **INIT (advisory → owner).** The scan's declared shape: surfaces staffed, challenge mode, the five
   positions, the cold-leg minimum, the budget, and the five deviations above. The owner's kick is the
   approval.
2. **Triage (blocking → owner).** The owner reviews the five verdicts, the coverage call, P4's routing,
   and any theme-revision proposal — then decides what, if anything, changes about the theme and how the
   wfh-004 gate should now be read. **Concluding that a premise is false is a successful run.**

---

<!-- Amendments are append-only (D3). Never overwrite a validated verdict; explicitly reconcile any
this extension changes. -->
