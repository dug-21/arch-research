# wfh-008 — RELEVANCE / TARGET REVIEW (advisory)

**Role:** `goal-owner` · the funnel's neck · **advisory to the human gate only**
**Reviewing:** `product/research/wfh-008/REPORT.md` (506 lines, commit `017f4fc`)
**Against:** the theme objective — *the smallest defensible personal-OS/Jurati substrate, preferring
adopt and assemble over build*
**Envelope:** static reading of committed artifacts at one commit, plus read-only Unimatrix. Nothing
built, run, installed or witnessed. No graph write. No git write. **Nothing here moves a grade;
`#316` stays `grade:claimed`.** I do not ratify `jurati-arch-002` and I make no build recommendation.

---

## 0. Stance

**Would I send this to the human as-is? Yes — with three corrections relayed alongside it, and one
framing caveat. I would not hold it for rework.**

This is a good report and its central negative is sound. It resists the two failure modes that
usually kill a run like this: it does not inflate a thin result, and it does not launder static
reading into proof. The `[SCE]/[SC]/[PDE]/[UI]` discipline holds all the way through; §5.1's "and no
further than that" paragraph and §8's coverage boundary are the two places most reports would have
overclaimed, and this one does not. W6 withdrawing its own closure claim unprompted, and the round-2
auditor refusing to invent an attribution for the round-1 over-count, are the strongest credibility
signals in the packet — stronger than any finding in it.

Where I part company with the curator is not on evidence. It is on **what the neck should do with
it**. The report ends with a five-stage follow-on staircase, four stages of which spend validated
budget characterizing a technology the same report recommends not adopting. And its
"the CODE column is short because it is short" is not established by the work performed — it is
established over the units W5 actually opened, which is roughly a third of the repository, and the
run's two best units were found by someone else, outside that third. Those are my two substantive
findings.

**Verdict: ALIGNED on drift. UNDER-REACH on the CODE column's search, and on one CONCEPT-column
level-up the report leaves on the table.**

---

## 1. Seam dispositions — bounded, with the determining constraint

Options: `adopt` · `assemble` · `reference-only` · `inseparable` · `insufficient evidence`.
None is an adoption decision; all are advice. Where I differ from the report's §4, the row is marked
**Δ** and my reasoning is in §4 below.

| Seam (smallest coherent boundary) | Report §4 | **My disposition** | Determining constraint |
|---|---|---|---|
| `@metaharness/router` core (k-NN + cost bar, no runtime imports) | reuse candidate | **reference-only** **Δ** | Re-derivation is cheaper than extraction. A k-NN over caller-supplied vectors with a cost bar is not a differentiating unit; extracting it costs a validated scope plus licence/provenance closure on a pre-1.0, 93.9%-single-author repo. The cost side of that trade is never priced in §4. |
| `sandboxAvailable()` at probe-function altitude | reuse candidate (wrapper inverted) | **reference-only — take the concept, not the lines** **Δ** | The unit is ~8 lines running `unshare -rn true`. Its entire value is the *idea*, and the idea is free. Importing eight lines under a third-party header buys nothing and acquires a provenance obligation. This is the run's best concept and its worst extraction candidate. |
| `packages/projects/src/sandbox.ts` as a module | reference only | **reference-only** (agree) | Adopting the file adopts a fail-open default with no degraded-mode signal; inverting it rewrites the module's only decision. Correct, and correctly reasoned. |
| `renderer.ts` (`render`, `extractVarReferences`, `validateHarnessName`) | reuse candidate | **reference-only** **Δ** | §4's own constraint says callers "must wrap it with typed encoders and strict unresolved-variable rejection" — i.e. rewrite the decision. A deliberately non-escaping templater that must be wrapped to be safe is a specification, not a component. |
| `sha256` / `fingerprintFiles` / `diffFingerprints` | reuse candidate | **reference-only** **Δ** | Node `crypto` plus a string-map diff. The constraint §4 names (no path metadata, modes, symlinks, overlays) means a real consumer writes the missing parts, at which point nothing of the original survives. |
| `walker.ts`, `writer.ts`, session-log copy-in, browser `zip.ts`, `eject.ts`, host emitters | reference only | **reference-only** (agree) | Ambiguous custody, conditional atomicity, copied protocol, external schemas. Correct. |
| Kernel JS floor — **source-slice** altitude | reuse candidate (W5) | **reference-only** **Δ** | An interface plus one JSON-shape validator. Same re-derive test. |
| Kernel — **published-package** altitude | inseparable | **inseparable** (agree) | Importing the package imports `@ruvector/emergent-time` (required), optional natives, generated WASM and a three-tier resolver. Determining and correct. |
| `@ruvnet/agent-harness-generator` alias / generator package | inseparable | **inseparable** (agree) | A thin re-export of an *older* full CLI (`metaharness@0.1.5` vs workspace `0.4.7`) — already version-skewed at cutoff. |
| ARC bridge (`python-bridge.ts` + `python/bridge.py`) **as code** | inseparable | **inseparable** (agree) | Licence closure alone, before quality: two unlocked PyPI pins with unresolved licences, plus a second language runtime, an external endpoint and a live credential. The report is right that this fails before the quality question is reached, and right to say so plainly. |
| ARC bridge **framing layer** as a protocol | reference only | **reference-only** (agree) | Domain-neutral and cheap to re-derive; payload, endpoint and credential are not separable. One of the four genuinely new concepts this run produced. |
| CASA schemas / compiler | **absent from §4** | **insufficient evidence — and a named omission** **Δ** | The schema is duplicated by convention across two repositories with documented path drift (`plugins/ruflo-agntcy/src/casa/enforce.ts` vs `v3/crates/ruflo-agntcy/src/envelope.rs`) and an open scope vocabulary; no established production sole-path call site. **Additionally:** the theme already holds `#200` **ASSEMBLE the ruflo `policy/` subtree as the envelope algebra**. CASA needs a novelty check against `#200` before it gets a fresh disposition, not a new row. §4 skipping it entirely leaves the human without the one place the two runs actually collide. |
| Witness machinery | **absent from §4** (W6: "integrity primitive only") | **reference-only** **Δ** | What is reusable is Ed25519 canonicalise/sign/verify — that is a library call. What would be valuable (external trust anchor, key custody, revocation, artifact coverage) is precisely what is absent. Missing witness is accepted and degraded verification returns `valid:true, unverified:true`. |
| Authority primitives — `PolicyGate`, claims dispatch, host permission projections | §4: host packages "insufficient evidence"; `PolicyGate` absent | **reference-only as negative design evidence; not adoptable at any altitude** **Δ** | Every one sits inside the governed party's own process or writes into files the governed party edits. That is a **structural** property, not a maturity gap — no later evidence repairs it, so "insufficient evidence" understates the finality. Say *not adoptable*, not *unproven*. |
| Generated MCP gate; host packages as runtime/enforcement units | insufficient evidence | **insufficient evidence** (agree) | No transport, no independent authority boundary, no compatibility result. `start()` contains no dispatch loop and remote auth is imported then discarded. |
| `packages/projects/src/verifiers.ts` — language-agnostic verifier registry | **never dispositioned** | **insufficient evidence — omission** **Δ** | This is the specification surface for *how untrusted code is executed and its result checked* — the single most substrate-relevant unit in `packages/projects` for a personal OS. The run characterises it only as the bypass vector (`PYTHON = {bin:'python3', args:…}`), never as a seam. It may well disposition out; it was never asked. |
| `packages/projects/src/safety-rails.ts` — the rail vocabulary | **never dispositioned** | **reference-only** **Δ** | §7 item 3 instructs the proposer to "preserve the rail *vocabulary*" but no row states what that module is or what preserving it costs. A TAKE instruction pointing at an undispositioned unit. |
| The ten-site execution-surface enumeration (`darwin-discover.mjs` + nine benches) | not framed as a seam | **reference-only, as method** | The transferable artifact is the *enumeration technique* — "the security property is the enumeration of execution sites, not the wrapper" (§7 item 2). The report states this and then does not carry it into the disposition table. It is the most portable thing in §5. |

**Nothing on this table is an `adopt` or an `assemble`.** That is the correct outcome for this
target, and it is worth stating explicitly to the human: a run whose honest answer is "take four ideas
and none of the code" has done its job. It is also why the follow-on staircase matters so much — see
§4.

---

## 2. Drift assessment — **ALIGNED**

The run answered the question it was scoped to answer. Every SCOPE expected-output (1–7) maps to a
report section; the position in §7 is advice and is labelled as such in six places; the proof bar in
§9 is restated verbatim and binding; §11 records no grade movement, and I verified that against the
live graph (§7 below). No sub-metric substitution: the run did not answer "is MetaHarness good" in
place of "what can Jurati use."

Two drift-adjacent observations, neither of which is a drift verdict:

**(a) The SCOPE is narrower than the theme objective, structurally.** "Prefer adopt and assemble over
build" cannot be served by a single-target static run — assembly needs a comparison set, and the
SCOPE explicitly forbids a competitor scan. So the run's *shape* is the shape that produces build
gravity, whatever its conclusions. The report does not drift; the packet's geometry does. The human
should know that the next question the theme objective actually poses is a comparison question, and
this run cannot have answered it.

**(b) The report's own delta table contains a recommendation it then contradicts.** §6 records
wfh-007's *"assemble shipped sandboxes; a kernel/isolation plane does not earn a bespoke build"* as
**confirmed** — reinforced, in fact, by MetaHarness's own isolation being 131 lines wrapping a shipped
OS primitive. §9 then proposes S1 (isolated extraction of `sandboxAvailable()` with an inverted
wrapper) and S2 (a rig exercising the failed-probe path on a host where `unshare -rn` fails). If the
assemble-shipped-sandboxes prior is confirmed, the next spend belongs on candidate *shipped* isolation
primitives, not on characterizing MetaHarness's wrapper. This is an internal inconsistency in the
recommendation, not drift in the findings, but it is the one place the report's advice pulls away
from the theme objective.

---

## 3. Under-reach assessment — **UNDER-REACH, two findings**

### 3.1 The CODE column is thin *and* under-searched. Both are true; the report claims only the first.

The report states, as a finding: *"The CODE column is not padded in this report to make the two look
balanced. It is short because it is short."* I tested that and it does not survive.

**W5's seam assessment covers roughly a third of the repository.** Against W5's text, these workspace
packages receive **zero** mentions: `avo`, `aws-finops`, the six `evals-*`, `flywheel`, `horizon`,
`jujutsu`, `oo-agents`, `radio`, `redblue`, `turn-credit`, `vertical-base`, `vertical-trading`,
`weight-eft`, `workspace-lens`, `workspace-probe`, `arc-agi-3-chatgpt`. That is ~25 of 42. W5's
coverage note declares them "outside W5's plausible reuse set unless a later scope names a specific
mechanism" — a self-issued exemption with no stated criterion applied per package.

**The run contains its own falsification of that exemption.** The two highest-value units in the
entire report — `packages/projects/src/sandbox.ts` (the probe concept and its counter-lesson) and the
ARC bridge framing protocol — were **not found by W5**. Both were found by the round-2 coverage
auditor's third independent sweep, in packages W5 had not opened, using an *operation-driven* alphabet
rather than a *seam-name-driven* one. W6 diagnosed exactly this failure about itself and named it
precisely: *"it had searched the vocabulary of the gates already known rather than the vocabulary of
protected operations."* W5's search had the same defect and no equivalent self-correction was applied
to it.

So the honest form of the report's claim is: **the CODE column is thin across the units assessed; the
assessment did not cover ~25 of 42 packages; and the last two packages opened by an outsider yielded
the run's two best units.** A base rate of two-for-two is not proof that more exists, but it is
squarely inconsistent with "it is short because it is short."

**Is closing it worth it? Partly — and the bounded version is cheap.** Most of the 25 are plainly
out-of-lens for a *substrate*: the six `evals-*`, the verticals, `aws-finops`, `turn-credit`,
`weight-eft`, `radio` are application and evaluation surfaces. The substrate-shaped unassessed set is
short: `projects` (only three files ever opened), `sdk`, `harness`, `jujutsu`, `workspace-lens`,
`workspace-probe`, `flywheel`. That is a bounded directional pass over ~7 packages with the
operation-driven alphabet that already worked twice — a fraction of a run, zero compute, static only.
Sweeping all 25 is not worth it. Opening seven is.

**This is advice requiring spend, so I am flagging it for escalation rather than presenting it as a
decision** (see §6).

### 3.2 The CONCEPT column stops one level below the step-function that is sitting in its own evidence

The report lists ten-plus portable concepts. That list is real, but it is a *list*, and it is the
wrong shape for "smallest defensible substrate."

**The level-up the report has the evidence for and does not name:** every one of MetaHarness's
authority failures is the *same* failure, and the report notices the rhyme twice without ever drawing
the law. Seven independent subsystems, one defect:

| Subsystem | Who controls the control's input / custody / call-site set |
|---|---|
| `PolicyGate` | the caller supplies rules, ceiling, action mapping — and may omit the gate |
| Claims dispatch | the caller mints the claims; signatures deferred; `dispatch_unauthenticated()` exported |
| Host permission projections | generated into files the governed project owner edits |
| Witness | the signer embeds its own public key; missing witness accepted |
| ARC bridge egress | the governed embedding process supplies the allowlist *and* holds the credential |
| `sandbox.ts` | the probe is cached in the governed process; no caller; fail-open |
| `no-bypass-sandbox` rail | decides on `bypassesSandbox`, a boolean **the proposer supplies** |

The general form: **a control whose input, custody, or call-site enumeration is inside the governed
party is a label, not a control.** That is one mechanically checkable predicate, not ten patterns to
remember. It would have caught all seven MetaHarness instances by inspection, it is exactly the shape
of this repository's own corrected `agent_id` rule, and it converts a reading-comprehension exercise
into an **admission condition a substrate can enforce**: every control in the register names the party
who can change it, and a control naming the governed party is refused at admission.

**Why this is a step-function and not a linear gain for the theme objective.** "Smallest defensible"
needs a *stopping rule*. A list of good patterns has no stopping rule — you keep adding patterns. A
custody predicate gives one: enumerate the controls, apply the predicate, and the minimum set is
whatever survives. It also supplies the general form of the report's own S4, which is currently
written as a MetaHarness-specific test.

**Second, smaller level-up, same evidence:** the run establishes that MetaHarness has ~7 gate classes
and **zero** boundaries. That is direct evidence for a positive claim about the theme objective the
report never makes — *the smallest defensible substrate likely needs exactly one externally-custodied
enforcement point, not seven in-process ones*, because seven in-process gates produced no boundary
while costing seven subsystems of maintenance and seven surfaces of false assurance. That inference is
one paragraph from evidence already in hand, and it is more on-objective than most of §7's TAKE list.

**Worth it? Yes, and it costs nothing.** Both are findings, not builds. **Recommendation:
defer-and-record** — record the custody predicate and the one-enforcement-point inference so they are
not lost, and let the `jurati-arch-002` proposer decide what to do with them. **I am not recommending
that anything be built.**

### 3.3 What is *not* under-reach — and where the CONCEPT column is over-counted instead

Running the novelty axis against the live graph cuts the other way on part of §7. `#200` already holds
**ASSEMBLE the ruflo `policy/` subtree as the envelope algebra**; `#277` already holds *"OS sandbox
owns resource effects"* and *"attribution is persisted self-assertion, not attestation, so it cannot
authorize."* Several §7 items — deny precedence and monotone delegation, external custody as the
admission condition, gate-input independence, pre-decision/post-receipt — are **sharpenings of
already-`claimed` ground**, not new concepts. W7's delta table grades them honestly ("confirmed,
sharpened"); §7 then presents them in a TAKE list without that provenance.

The genuinely **new** concepts this run produced are four:

1. probe the real operation, not the binary's presence — **and its fail-closed counter-lesson**;
2. the gate-input predicate in its sharpened form (a rail deciding on a proposer-supplied boolean);
3. the fail-closed serial subprocess protocol with an enumerated inherited-env allowlist;
4. cross-language prerequisites as first-class fields of a generation envelope.

Four new concepts from a directional run is a good yield. The report's claim that the CONCEPT column
is the higher-value half is **better supported by those four than by the list of twelve**, and stating
it that way would make it harder to argue with, not easier.

---

## 4. Where I disagree with the curator

**D1 — The follow-on staircase is inverted, and four of its five stages are off-objective.** This is
my strongest disagreement.

- **S0** (registry fetch to close PyPI/RuVector licences) clears "the ARC bridge's determining
  constraint" — for a unit §4 rules `inseparable` and §7 puts on DO-NOT-TAKE. Closing a constraint on
  something we are not taking buys nothing.
- **S1** (isolated extraction of the router core) extracts a unit I disposition `reference-only`
  because re-derivation is cheaper.
- **S2** (a rig exercising the failed-probe path; testing whether a fail-closed variant is reachable
  "from the ten direct sites without restructuring the bench harness") is spend on **MetaHarness's
  internal refactor**. We do not maintain MetaHarness. We already know the fix — invert the default.
  Observing the defect executing tells Jurati nothing it does not already have.
- **S3** (upgrade/drift replay of `harness upgrade`) tests a path already closed by §4's `inseparable`
  ruling on the generator alias and CLI closure.
- **S4** (authority admission test under a separate OS/service identity) is **the only stage that
  serves the theme objective — and the only one that does not need MetaHarness at all.**

**My advice: collapse the staircase to S4, generalized** — a clean-room admission test of the custody
predicate in §3.2, against whichever enforcement plane the theme actually intends to assemble
(`#200`/`#277` are the live candidates, not MetaHarness). That is one decision for the human, not
five stages. **Advisory; I authorize nothing and I am not proposing it be run.**

**D2 — §4 never asks the reuse-versus-rewrite question.** Every row prices the *constraint* on
extraction and none prices the *cost* of extraction against the cost of writing the thing. For four of
the report's five reuse candidates, writing it is cheaper. At the neck, "reuse candidate" that nobody
should reuse is a `reference-only` with extra steps, and it invites an S1 that should not happen.

**D3 — "insufficient evidence" understates the finality on the authority primitives.** The gates fail
on a *structural* property — the governed party controls the input, the custody, or the call-site set.
No further evidence repairs that. "Not adoptable at any altitude" is the accurate disposition;
"insufficient evidence" reads as "come back with more data," which is exactly the wrong instruction.

**D4 — three units carry TAKE instructions with no disposition row:** `verifiers.ts`,
`safety-rails.ts`, and the execution-site enumeration method. §7 tells the proposer to preserve the
rail vocabulary and to treat site-enumeration as the security property, while §4 dispositions neither.
A required field is missing on both.

**D5 — the §0 blanket negative is very slightly overstated at one row.** See §5.

---

## 5. Overstated / understated

### The load-bearing negative — "MetaHarness contains no authority boundary Jurati could adopt"

**I checked this independently against W6 and the `sandbox.ts` evidence. It holds, with one
correction.**

It holds because it does not rest on the gate enumeration being exhaustive — which is fortunate,
since W6 explicitly withdrew that claim and now asserts only closure "against an operation-driven
sweep at this cutoff." It rests on a **structural** property that would survive discovering an eighth
gate: every gate found sits inside the governed party's process or writes into artifacts the governed
party edits. The `sandbox.ts` evidence supports it independently and by a different route — a gate
with **no caller** mediates nothing regardless of its default, and the `no-bypass-sandbox` rail
deciding on a proposer-supplied boolean is the cleanest single instance in the packet. As an **ADOPT**
verdict the negative is unambiguously sound: nothing in §4 or W6's reuse table is adoptable as a
boundary at any altitude.

**The correction: the negative is mildly overstated at the CASA row, and the report knows it
elsewhere.** CASA compile→enforce is the one place MetaHarness has an architecturally *external*
custody shape — compilation in one repo/language, enforcement in another. W6 rules it "conceptually
compatible, operationally unverified": the split is clean at source level, and what fails is
**sole-path mediation** (no established production call site to `check_authorization()`) plus
cross-repo schema/path drift — *not* same-authority placement. That is a different failure from the
other six, and it matters, because it changes what a follow-on would test. The precise form of the
negative is:

> MetaHarness contains no authority boundary that is *demonstrated* to be both externally custodied
> and sole-path. Six of its seven gate classes fail on same-authority placement — a structural defect
> no evidence repairs. The seventh (CASA compile→enforce) fails on unverified sole-path mediation and
> cross-repository schema drift — a defect a test could in principle clear.

§9's S4 already scopes the right test, so the follow-on is correct; it is the §0 sentence that
flattens the seventh row into the other six. **One sentence, worth relaying.**

One further precision the report gets right in §5 and blurs in §0: fail-open is a **safety** defect,
not an **authority** defect. The load-bearing part of the sandbox evidence for the *authority* claim
is "no caller + governed-party-controlled input," not "fail-open." §5 keeps these apart; §0's summary
runs them together.

### Also overstated

- **"It is short because it is short."** Not established by the work performed (§3.1).
- **The §7 TAKE list's implied novelty.** Roughly half is already-`claimed` ground at `#200`/`#277`,
  sharpened. W7 grades this honestly; §7 does not carry the grading (§3.3).
- **"Reuse candidate" on four units** that should not be reused (§4 D2).

### Understated

- **The four genuinely-new concepts** are undersold by being buried in a twelve-item list (§3.3).
- **The finality of the authority negative** (§4 D3).
- **The execution-site enumeration as the portable method** — stated once in §7 item 2 and never
  dispositioned, though it is the most transferable thing in §5.
- **The method observation in §8** — that a ledger naming its own blind spot is more trustworthy than
  one reporting closure. This run produced that behaviour twice (W6's withdrawal, the auditor's
  refusal to invent an attribution) and it is a reusable finding about *the garage*, not about
  MetaHarness. It sits at the end of §8 as an aside.

---

## 6. What the human should actually decide at this gate

1. **Accept the report as the run's synthesis output.** Yes, in my judgement — with the §5 CASA
   sentence and the §3.1 search-coverage caveat relayed alongside it, so neither enters the graph
   flattened.
2. **`#316` stays `grade:claimed`.** Confirm. Nothing in this run is demonstrated-by-us evidence and
   no grade should move. Verified against the live graph (§7).
3. **The follow-on staircase: five stages, or one?** This is the real decision. My advice is that
   S0–S3 spend validated budget characterizing a technology the report recommends not adopting, and
   that only S4 serves the theme objective. Approving §9 as written commits the theme to a
   single-target track it has already concluded is not worth adopting. **Nothing is authorized either
   way at this gate.**
4. **Whether to spend a bounded directional pass on the ~7 substrate-shaped unassessed packages.**
   Escalated below rather than recommended — it needs spend, so it is the human's call, not mine.
5. **Whether the custody predicate and the one-enforcement-point inference get recorded** as
   defer-and-record architect-for-future items, so they are not lost with the run.
6. **`retort`** — the report handles it correctly as a follow-on candidate, not absorbed. Nothing to
   decide beyond noting it for the coordinator.

---

## 7. Verified this review — closing gap-register item 10

The round-2 auditor recorded, as gap-register item 10, that it *"performed no Unimatrix writes and
attests nothing about the live contents of the graph nodes."* Nobody had checked §11 against the live
graph. I did, read-only, `agent_id: goal-owner`:

- `#316` — `technology`, **`status: active`, `grade:claimed`** — unmoved, as §11 states.
- `#317`, `#318`, `#319` — all present and `active`; `#319` carries the `position` tag.
- Edges match §11 exactly: `#317 → #200`, `#317 → #316`, `#318 → #277`, `#318 → #316`,
  `#319 → #316`, all `Motivates`. `#314` is unchanged and its edge resolves forward to `#316`.
- No `Prerequisite`, `Cites` or `Tests` edge was created. No grade tag other than `claimed` on `#316`.

**§11 is accurate as written.** Gap-register item 10 can be marked closed at the structural level (ids,
status, grade, edge set). I did not audit node *content* against the findings files.

---

## 8. Limits of this review

Static reading of committed artifacts at one commit, plus read-only Unimatrix. I did not clone,
build, run, install or witness anything, and I did not re-verify the researchers' repository claims
against the MetaHarness checkout — where I rely on a repository fact, I rely on the run's own
`[SCE]` labelling and on the round-2 auditor's independent re-derivation. My package-coverage finding
in §3.1 is derived from the wfh-008 findings files themselves, not from the target repository. Every
disposition in §1 is directional advice at the same altitude as the report it reviews: none
establishes buildability, runtime behaviour, licence sufficiency, or security, and none moves a
grade. **This document is advisory. The human decides; the curator files.**
