# wfh-007 — theme-scan (recurring, discovery + challenge): if we build a personal operating system, what do we actually build — and what is critical

**Status:** in-flight — INIT gate cleared 2026-08-17 (governor surfaced, owner ruled *go, as scoped, five scouts*); phase `scan`
**Protocol:** `.claude/workflow/theme-scan.md` — **recurring** scan (warm leg + protected cold leg), not a first map. Prior scan: wfh-005, closed 2026-08-01.
**Theme:** `theme:workflow-harness` — **scanned under its current name deliberately.** The personal-OS reframe would change the theme's lens; the scan may *propose* that revision but must not assume it, so the run keeps the old key until the triage gate rules (themes.md → "A scan may reshape its own theme"; the failure that closed wfh-002).
**Confidence-required:** **directional** — structure only. No status reaches `partial` or `proven`. No compute-spending arm.
**Roles:** `research-leader` · `scout` ×5 · `hypothesizer` · `factory-curator` · `goal-owner`. **No `factory-poc`, no `factory-validator`** — this protocol never proves.
**Cycle topic / Issue:** `wfh-007` · GitHub Issue **#64** · `wf-v0.24`

---

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
