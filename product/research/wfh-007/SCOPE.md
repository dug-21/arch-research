# wfh-007 — theme-scan (recurring, discovery + challenge): if we build a personal operating system, what do we actually build — and what is critical

**Status:** research corpus complete; scope reconciled retrospectively 2026-08-27. Repository artifacts include a completed bounded scan, owner-directed hypothesis/verification/triage work, and a post-triage architecture draft plus checkability review. This status does **not** assert GitHub Issue, cycle, or Unimatrix closure.
**Protocol:** `.claude/workflow/theme-scan.md` — **recurring** scan (warm leg + protected cold leg), not a first map. Prior scan: wfh-005, closed 2026-08-01.
**Theme:** `theme:workflow-harness` — **scanned under its current name deliberately.** The personal-OS reframe would change the theme's lens; the scan may *propose* that revision but must not assume it, so the run keeps the old key until the triage gate rules (themes.md → "A scan may reshape its own theme"; the failure that closed wfh-002).
**Confidence-required (INIT and retained):** **directional** — structure only. No status reaches `partial` or `proven`. No compute-spending arm.
**Roles declared at INIT:** `research-leader` · `scout` ×5 · `hypothesizer` · `factory-curator` · `goal-owner`. **No `factory-poc`, no `factory-validator`** — this protocol never proves. The actual-run extension later added one bounded `factory-architect` assignment and an independent `factory-validator` checkability review; see the evolution ledger.
**Cycle topic / Issue:** `wfh-007` · GitHub Issue **#64** · `wf-v0.24`

---

## Scope reconciliation — authority and reading order

**Amendment date:** 2026-08-27

**Authority:** retrospective human ruling: document the full scope actually run and show how it evolved.

**Method provenance:** `wf-v0.24`, preserved from INIT. This amendment does not restamp the run to a later
workflow version.

This file now contains two kinds of truth that must not be collapsed:

1. **The original INIT charter**, preserved below as the historical authorization under which the scan
   began. Its exclusions and directional proof bar were real at INIT.
2. **The evolved actual-run scope**, recorded after the original charter. It accounts for work that entered
   after evidence and owner direction changed the target, including work that exceeded the INIT charter.

The amendment is a scope-reconciliation artifact, not retroactive authorization. In particular, it does
not pretend the INIT charter included architecture authoring or validation, and it does not convert the
later specification into an accepted or proven result.

---

## Part I — Original INIT charter (preserved as historical truth)

## The question

The Jurati framing has been re-cut: not an agentic coding harness that grows features, but a **personal
operating system** whose first userland program is agentic coding, carrying six domains plus an always-on
voice surface. No Jurati code exists in this repo, so nothing is sunk. Two exemplars motivate the reframe
— ruvnet's 2026 output, and Andre Lamego's basement stack running ~1B tokens/week at 99.999% local — and
**neither built the governance layer the reframe assumes is load-bearing.**

> If we build a personal operating system, what do we actually build — measured against the people already
> operating at this scale — and which parts are critical to it succeeding rather than merely desirable?

Two halves, and the second is the one that has never been asked here. **"What do we build"** is the
five-verdict triage the protocol already runs. **"What is critical"** is a separate, empirical claim:
of everything the framing names — kernel, capability vocabulary, delegation, secret broker, evidence-graded
commit, `/etc`, init and supervision, the shell — which are load-bearing, and on what evidence?

## Why it matters

The owner's stated blocker is unwillingness to build toward an unsatisfying end state, and ten open factory
Issues are circling the same unresolved decision. A directional scan is the cheapest instrument that can
settle it, and it is only honest if it is permitted to come back with *"build almost none of this"* or
*"the kernel does not earn its place."* Those are successful outcomes of this run, not failures of it.

## Descoped — deliberately, and what survives the cut

**Not produced by this run:** a capability vocabulary v0, the irreversibility list, a composability verdict
on `derive()`, or any other authored design artifact. The garage has **no architect role** — scout reads,
hypothesizer diverges, goal-owner triages, curator transcribes, leader orchestrates, and none of them can
author a design. Handing that to the curator would make the single write-capable role also the design
authority, which is the concentration the firewall exists to prevent. The role gap is real and is filed as
a method question; this run does not paper over it.

**What survives, and it is most of the substance:** the *evidence* about vocabularies, delegation,
commit primitives and person-models is still gathered, characterized, and triaged — as findings about what
exists, what it costs, and where it fails. The line is: **describing how Home Assistant's vocabulary fails
the irreversibility test is a finding; authoring ours is design.** Only the second is out.

## Known constraints & prior art *(build on these — do not re-derive)*

**Settled by wfh-005, use as base:** the absence-of-prior-art claim is **falsified and struck**.
Phase-indexed authority is Task-Based Authorization Controls (Thomas & Sandhu 1997) and the Workflow
Authorization Model (Atluri & Huang 1996); gate independence appears as Clark-Wilson E4, DO-178C
verification independence, SLSA Build L3, measured boot; demand-derived ceilings ship in WASI, Bazel, Nix,
in-toto, `gh aw compile`. What survives is a **composition claim, not an absence claim**. Call the property
**gate-input independence**, never "soundness."

**Graph — reuse, do not re-litigate:** **#200** ruvnet/ruflo + `@claude-flow/security` (*assemble the
subtree, not the product*) · **#202** Bedrock AgentCore Policy + Cedar (*assemble, per-call authority leg*)
· **#263** Jurati Decision Contract Language v0.1-dev (`grade:partial`, bounded checker/reducer) · **#264**
jurati-001 position · **#256** the orphaned capability · **#191** the position that wounded "minimize
inference."

**Repo:** the personal-OS framing document (2026-08-17) · `proposals/jurati-evolved-vision-2026-08-05.md`
· `proposals/workflow-harness-scope-recut.md` (six ranked goals) · `wfh-006/scout-active-dev.md`
(**lift `packages/llm`, do not fork**) · `jurati-001/` incl. lesson **#265**.

**Standing method holes, still unspent:** patent prior art; commercial CD stage-scoped role binding
(Harness, Spinnaker, Azure DevOps).

## Scan shape — declared up front (protocol INIT requirement)

Five scouts, staffed across all four surfaces, spawned in one message. Every surface is read; none is
declared a hole at the outset.

- **S1 — active development · DISCOVERY · the exemplars.** *How must they actually be operating?* Not what
  they built — the machinery, the division of labour between human and fleet, the spend, the failure
  handling. Owner-injected candidates (ruvnet, Lamego) enter here and flow on identically. **Runs and
  reports all three instruments (#216, never yet exercised): organization-walk · deliberate low-star pass ·
  by-function sweep using none of the theme's nouns.** Mark every claim `[demonstrated by them, with
  artifact]` / `[inferred from reading]` / `[asserted]`, and inventory explicitly **what they do not have**.
- **S2 — established products · DISCOVERY.** Home Assistant as primary subject — its verb/entity/area
  vocabulary, `homeassistant.turn_on`, script and scene collapse, the arbitrary `data` dict — asked as
  *scope-versus-need, cost, and lock-in*, never as a feature list. Plus personal-assistant and
  personal-data platforms with an authorization story.
- **S3 — research literature · DISCOVERY.** Capability vocabularies and their granularity failures;
  delegation and attenuation; workflow authorization **on top of** the settled wfh-005 base.
- **S4 — adjacent prior art · DISCOVERY.** Two jobs. (a) **Personal-OS attempts and how they failed** —
  Urbit, Solid, Anytype, Stanford Almond/ThingTalk, Mycroft/OVOS, NixOS-as-personal-config, the
  self-hosted movement, agent-memory systems. (b) **The evidence-graded commit primitive** — is *"a claim
  is cheap; a commitment requires declared-kind evidence and is append-only"* already named and solved?
  Event sourcing, bitemporal stores, W3C PROV, LIMS/ELN, double-entry bookkeeping, clinical EDC,
  in-toto attestation, git's object model.
- **S5 — CHALLENGE · cross-surface.** Against the position we hold: *a personal OS needs a trusted kernel
  that spawns agents, mints phase credentials and evaluates gates.* S1's exemplars are the ammunition —
  they reach very high throughput with none of it, and Home Assistant runs millions of homes on ambient
  authority. What is the **evidence** the governance layer is necessary rather than tasteful? What is the
  cheapest thing reaching 80%, and what precisely does it fail to deliver?

**Warm leg:** the theme's watchlist — gh-aw (the incumbent), MCP authorization spec, jurati #12,
coding-agent permission and hook models, agent over-privilege measurement, Cisco Outshift/AGNTCY, ruvnet,
adrianco/retort, Temporal plugins. Record last-looked on each entry walked.
**Cold leg:** protected minimum, spent on S4 and on the S1 low-star and by-function passes. **A scan
reporting no cold-leg spend has not completed.**
**Cross-surface alias merge is MANDATORY** (>2 surfaces staffed) — leader reconciles into
`scout-merged.md` before hypothesize. wfh-005's four surfaces returned what read as ~15 independent hits
and collapsed to three clusters; unmerged, it would have overstated its evidence base fourfold with no way
to notice.

## Coverage grid

Run against the theme's declared eight dimensions (structure · context provisioning · security ·
introspection · cost transparency and management · self-improvement · recovery and durability · human
steering), crossed with the default lens set (cross-domain transplant · constraint inversion ·
adversarial/failure-mode · scale extrapolation · incumbent gap · minimality).

**Four candidate dimensions are proposed for promotion**, evaluated in this run and ratified or dropped at
the triage gate (the protocol puts the promotion test in the run's scope): **the person model** ·
**domain vocabulary** · **always-on and proactivity** · **irreversibility and consequence**. The eight
existing dimensions are coding-agent-harness-shaped; whether they survive the reframe is itself a finding.

**Round two fires on a named hole that is load-bearing for a verdict or a routing** — not on a thin cell
(#215). wfh-005 was 20-of-20 on cells with two holes sitting under its only build recommendation.

## Expected output

1. Five `scout-*.md` files + `scout-merged.md`, every citation carrying D14 provenance (`type`/`ref`/
   `title` required; `author`/`org`/`year`/`surface` where known — **omit unknown keys, never invent one**).
2. An **operating-model teardown** of ≥2 exemplars, every claim marked demonstrated / inferred / asserted,
   with an explicit inventory of what they lack.
3. A **failure taxonomy** of prior personal-OS attempts, each entry tested against the domain-add contract:
   which of its five items was violated, and at which domain number it showed.
4. `hypotheses.md` — mechanism-grounded candidates across the personal-OS surface, generated for range.
5. **`reports/triage.md` — what we actually build.** Five verdicts, park by default, burden of proof on
   build. Required fields are load-bearing: ASSEMBLE names which part is uncovered **and whether it is the
   differentiating one**; BUILD names the specific thing assembly cannot deliver; PARK names its
   re-enter-when.
6. **`reports/criticality.md` — what is critical.** Each component the framing names, ranked
   load-bearing / valuable / optional, with the evidence for the ranking: what happened to attempts that
   omitted it, and at what scale or domain count it started to matter. **A ranking without that evidence
   is taste and does not ship.**
7. A **position finding on whether the kernel earns its place** (S5), stated either way.
8. A **theme-revision proposal** — relayed verbatim to the gate with the goal-owner's assessment; it never
   rewrites the scan that produced it.
9. Coverage grid with every cell populated or declared a hole naming which lens failed to see it;
   cold-leg spend statement; surface tally; funnel counts.
10. Watchlist derivation run **first**, then reconciled by hand into `themes.md` (method-stream commit).

## Proof bar *(D7)*

**Directional — structure only.** Findings, `grade:claimed` technologies, `position` findings. **Zero
status moved to `proven`, by design.** No code, no POC, no measurement arm, no compute spend. Stated
explicitly because the prior run did the opposite: jurati-001 was `validated`, spent real compute, and
returned SCOPE FAIL on a proof-schema defect.

## Explicitly out of scope

- **Any authored design artifact** (see Descoped above) and any Jurati code — zero lines.
- **Re-testing jurati-001's semantic-judging premise.** A later validated scope, gated on enhancement
  **#266** (executable scoreability preflight) existing first — lesson #265.
- **Building any of the six domains.** 3D printing and travel remain paper tests.
- **Hardware purchase decisions** (#246: no cross-run measurement instrument currently survives its run).
- **Multi-tenant / SaaS (H8).** Personal-first; returns as its own scope if it returns.
- **Re-litigating settled wfh-005 verdicts** or #200/#202's assemble rulings.

## Coverage / done call

Loop-until-dry: **K = 2** consecutive passes surfacing nothing new on a staffed surface, **N ≥ 3**
independent findings per leading candidate. Cross-surface reconciliation mandatory (#217). Goal-owner calls
coverage — COVERED, or NOT COVERED naming the specific cell or unread surface — then the owner confirms at
the triage gate.

---

## The governor fires before any scout spawns *(protocol INIT requirement)*

theme-scan: *"do not scan past the neck's throughput — if the theme already carries an untriaged shortlist
from a prior scan, or a promoted proof-goal that has not run, surface that to the owner before spawning."*

`theme:workflow-harness` carries **both**. wfh-005's assemble verdicts (#200, #202) sit unacted, and
jurati-001 — the promoted proof-goal — returned inconclusive. Ten open factory Issues are circling one
decision. **The leader must put this in front of the owner and get an explicit go before spawning.** The
protocol already knows the mouth is outrunning the neck; this run must not widen the gap it is meant to
close.

## Open items for the owner at the INIT gate

1. **Go, given the governor.** This scan is justified only if it *resolves* the untriaged backlog rather
   than adding to it — which is what output 6 is for. Confirm that reading.
2. **The orphan.** Capability **#256** has three incoming `Prerequisite` edges and **no `Advances` edge to
   any goal**; there is no Jurati goal node. Recommend a one-line curator write at `formalize` to author
   the goal and re-parent it, so the largest active line of work is visible to a board query. Full
   decomposition stays a separate scope.
3. **The architect gap.** Descoped here, but the vocabulary and the irreversibility list are the artifacts
   that cannot be retrofitted. Decide whether a `factory-architect` role is authored before the follow-on
   scope, or whether you author those two documents yourself.

---

## Part II — Scope evolution ledger

| Date | Evolution | Why it entered | Authority and status |
|---|---|---|---|
| 2026-08-17 | **INIT: recurring directional theme scan.** Five scouts covered active development, established products, literature, adjacent prior art, and a cross-surface challenge; the leader merged aliases before hypothesis generation. | The original personal-OS/Jurati reframe and criticality question required a wide scan before another build commitment. | Owner cleared the governor and authorized *go, as scoped, five scouts*. This is the original charter above. Authored design, validators, code, proof, and graph-grade movement were excluded. |
| 2026-08-17 | **Scan corpus expanded within the charter.** S4 added a clinical-EDC annex and a self-hosted amendment; the cross-surface merge reduced 59 raw candidates to eight clusters and named load-bearing holes. | Cold-leg discoveries and missing adjacent evidence materially affected the evidence-graded-commit and personal-system failure analysis. | Normal scan execution under the INIT charter; still directional discovery/challenge. |
| 2026-08-19 to 2026-08-20 | **Owner-directed target correction and hypothesis expansion.** The target changed from a monolithic six-domain “personal operating system” reading to Jurati Core as coordination for independently owned programs in a growing personal digital organization. Cross-program exchange, federation, provider/location neutrality, second-brain elevation, reviewer throughput, and the real software-delivery → garage first slice entered explicitly. Five partitioned hypothesis passes plus an independent Codex pass generated about 147 candidates. | `OWNER-DIRECTION.md` records that the scouts had researched a framing the owner then clarified. The clarification was necessary to finish hypothesis generation and triage against the intended product rather than the superseded metaphor. | Owner direction and working synthesis, explicitly **not** a research verdict, architecture decision, design authorization, proof run, graph write, or status advancement. It authorized steering of hypothesize and triage while keeping the run directional. |
| 2026-08-20 | **Targeted verification was added before triage.** V1 tested OpenShell reload latency/atomicity; V2 tested Cedar forbid-only-context discipline; V3 tested CaMeL information-flow enforcement and cost; V4 tested Dogwood’s aggregation coverage. The coverage grid was amended with their results. | The merge and hypotheses exposed four named holes that were load-bearing for verdicts or routing. Carrying them unresolved would have distorted adopt/assemble/build/probe decisions. | Research-leader-directed verification within the evolved directional research scope. These were primary-source/checkability investigations, not POCs or proof-grade demonstrations by this garage; no grade advanced. |
| 2026-08-21 | **Goal-owner triage and criticality completed the bounded research scan.** The result was `COVERED` as a bounded scan, 3 ADOPT, 4 ASSEMBLE, 1 BUILD, 3 PROBE, about 136 PARK, plus criticality rankings, theme-revision proposals, open architecture decisions, and a recommendation for a separate architecture scope. | The run needed to resolve the governor backlog and answer what to build, what is critical, whether a trusted core earns its place, and what should follow. | Goal-owner advisory verdict under the directional scan. It did not authorize implementation, proof, graph writes, or automatic adoption. It explicitly recommended that architecture be chartered separately after the architect-role prerequisite. |
| 2026-08-21 | **Post-triage architecture extension: cross-program work-contract v0 draft.** A `factory-architect` authored `specs/work-contract-v0-draft.md`, including the record family, clauses, provenance, enforcement accounting, examples, exclusions, objections, and owner questions. | Triage identified the cross-program contract schema as the differentiating, unowned object and recommended `jurati-arch-001`. The architect role gap had by then been filled, and the leader assigned one bounded authoring job. | This work **exceeded the original INIT charter** and did not receive a separate charter or `context_cycle`; the draft says so explicitly. Its authority is the leader’s bounded assignment to the architect, not retroactive INIT authority. It remains **DRAFT, claimed, unproven, and unratified**, and had not passed goal-owner review. |
| 2026-08-21 | **Independent checkability review of the draft.** A separate `factory-validator` reviewed all 34 clauses and both examples and returned `REWORKABLE FAIL`, iteration 1 of a maximum 2. | The architect role requires independent review, and a specification intended for implementation needed its checkability tested before any ratification. | This was a checkability review only, not a firewall gate, proof ruling, design-merit verdict, or grade recommendation. It moved nothing in Unimatrix and repaired nothing. The specification remains `claimed`. |
| 2026-08-27 | **Scope reconciliation.** This ledger and the final actual-run scope were added without altering the specification. | The accumulated corpus no longer matched the INIT-only scope description. The owner ruled that the scope should truthfully reflect its evolution. | Human-authorized documentation amendment. It records, but does not launder, the post-triage scope extension. It claims no Issue/cycle/Unimatrix closure. |

## Part III — Final actual-run scope

The complete `wfh-007` run, as actually executed, comprised:

1. **Recurring theme scan and challenge.** Five independently staffed surfaces, protected cold-leg work,
   cross-surface alias reconciliation, the exemplar operating-model teardown, personal-system failure
   taxonomy, evidence-graded-commit prior art, kernel necessity challenge, watchlist deltas, and the declared
   coverage grid.
2. **Owner-directed reframing.** Completion of the scan against Jurati Core as a federating coordination
   layer for independently owned programs—not an operating-system implementation—while preserving the
   original personal-OS framing as the question that launched the scouts.
3. **Divergent hypothesis generation.** Five mechanism-oriented partitions (contract/phase, derived
   authority, evidence/acceptance, federation, progressive autonomy) plus an independent unpartitioned
   pass, with attacks, falsifiers, and coverage mapping.
4. **Four narrowly targeted verification passes.** Primary-source evaluation of the specific OpenShell,
   Cedar, CaMeL, and Dogwood holes needed to support triage, including explicit corrections and remaining
   unknowns.
5. **Neck-stage disposition.** Buy-before-build analysis, criticality ranking, funnel accounting,
   theme-revision proposals, open architecture decisions, and adopt/assemble/build/probe/park routing.
6. **One bounded architecture artifact after triage.** A draft cross-program work-contract definition
   derived from the run corpus, followed by an independent checkability review. This extension documented
   a proposed contract; it did not implement, ratify, or prove one.

### Final objective actually served

Determine the smallest credible boundary for Jurati Core in a federated personal digital organization:
what can be adopted, what must be assembled, which seams are genuinely differentiating, whether
cross-program work exchange is core, what responsibility a trusted core may hold, and whether a proposed
cross-program work-contract record is precise and checkable enough to become a candidate for later
ratification and implementation.

This objective includes the late architecture/checkability question because the run actually answered it.
It does **not** imply that the contract passed review: the answer on 2026-08-21 was `REWORKABLE FAIL`.

### Actual deliverables

- Five scout returns, two S4 supplements, and `scout-merged.md`.
- `OWNER-DIRECTION.md` as owner input and working synthesis.
- Five partitioned hypothesis files plus `codex-hypotheses.md`.
- `coverage-grid.md` and four verification reports.
- `reports/triage.md` and `reports/criticality.md`.
- `specs/work-contract-v0-draft.md` and its independent
  `specs/work-contract-v0-validator.md` checkability review.

### Retained exclusions and authority ceilings

Across the entire evolved run:

- No Jurati implementation, capability vocabulary v0, irreversibility list, implementation-language
  decision, multi-tenant/SaaS design, domain build, hardware purchase, or re-test of the jurati-001
  semantic-judging premise was authorized or produced.
- No POC or garage-demonstrated artifact advanced any finding to `partial` or `proven`; the run remained
  directional, and the architecture draft remained `claimed`.
- No specification ratification or implementation decision was made. The validator judged checkability
  only and explicitly did not judge design merit or adoption.
- No repair of `specs/work-contract-v0-draft.md` is part of this reconciliation. Its validator defects and
  unresolved owner questions remain on the record.
- No Unimatrix write, grade movement, Issue closure, cycle stop, theme-file rewrite, or portfolio cleanup is
  claimed by this amendment. Those surfaces require their own authorized reconciliation actions.

### Unresolved scope discrepancy

The post-triage architecture draft and validator review are now accurately included in the **actual-run
scope**, but the corpus records that they were performed without the separately chartered `jurati-arch-001`
scope and without a `context_cycle`. This amendment cannot erase that process discrepancy. It makes the
discrepancy explicit and preserves the authority ceiling: the draft is a claimed input to any follow-on,
not an accepted result of the original theme-scan charter.
