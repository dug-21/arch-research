# SCOPE — wfh-004

**ID:** `wfh-004` — canonical key (= `context_cycle` topic = `feature_cycle` = path `product/research/wfh-004/`). GitHub Issue cross-linked by title, **opened by the execution session** (not here — plan-only). *(`wfh-003` is taken: Issue #44, H1 prospective+causal injection probe.)*
**Title:** `research(directional): what an agentic harness must provide — the capability space by concern`
**Status:** ACTIVE — owner-kicked 2026-07-25 (wave-0 manual kick = scope approval, per `theme-scan` INIT). Surfaces open: GitHub Issue **#48** · `context_cycle` topic `wfh-004` (stamp `wf-v0.16-11-g30dccf2`) · branch `research/wfh-004`. The five §12 deviations ride to the blocking triage gate for explicit sign-off.
**Theme / value-target:** `theme:workflow-harness` → JURATI (`dug-21/jurati`).
**Confidence-required:** **directional** — divergent generation + triage. **No artifact, no proof, no grade moves.** Per D7 this activates the goal-owner step-function dimension (OBS-4).
**Phase / area:** workflow-harness · capability space.
**Prerequisite:** wfh-002 closed (its four constraints are this scope's inputs); wfh-001 landscape is the precedent base.

## 1. The question

> **What must an agentic harness provide** to enable structure, security, introspection, cost transparency and management, self-improvement, recovery, human steering, context provisioning — **and any further ability that research or generation surfaces**?
>
> Of that space, which abilities *should* JURATI have, screened against real feasibility?

This is a **WHAT run.** It does not choose an architecture, does not decompose into a board, and does not build.

## 2. Why it matters

`theme:workflow-harness` has a supply side (H1–H8: mechanism hypotheses) and **no demand side** — no JURATI goal node, no capability board. Methodology §5 scopes runs against the demand side; without one, every run must justify itself against a *mechanism* hypothesis, so runs bend toward mechanism. wfh-002 is the worked example: chartered as an ontology feasibility probe, it drifted into a three-way architecture comparison and then into implementation detail.

The fix is not more discipline inside a run — it is building the missing demand side, **wide before narrow**, organized by *what the harness is for* rather than by *what it is made of*. Decomposition (`decompose-scope`) comes **after** this run, as its own scope. You cannot decompose a space you have not yet mapped.

## 3. The concern frame — seeded, but open

The concerns are the **coverage axis**: what the harness is *for*. Generation lenses (§6) are technique; concerns are the frame that generation must cover and triage must map to.

### 3.1 Seeded concerns

| Concern | The ability, stated as operation |
|---|---|
| **Structure** | The shape of work exists as addressable units — roles, steps, sequence, dependencies, gates — so that anything else can be said *about* something. |
| **Context provisioning** | What an agent knows at each step is decided, injected, and explainable: what goes in, when, why, and what was left out. |
| **Security** | Authority is bounded and enforced outside the agent — least privilege by role, isolation, egress control, resistance to instructions arriving through data. |
| **Introspection** | What is happening now, what happened, and why — live trace, causal explanation, durable audit record. |
| **Cost transparency & management** | Resource use is metered, attributed to units of work, predicted, and enforced against a budget. |
| **Self-improvement** | The harness measurably gets better at its job: outcomes attributed to configuration, changes A/B-compared, improvements adopted on evidence. |
| **Recovery / durability** | Work survives failure — a dead agent, a hung subprocess, an interrupted run is detected, resumable, and never silently abandoned. |
| **Human steering** | Intent enters mid-run and is acted on — gates, redirection, correction — so an autonomous run is correctable, not merely stoppable. |

*Evidence discipline* (the harness ensuring claims are backed by real artifacts at the claim's altitude) is **filed under Structure** as a gate property, provisionally. If generation populates it with ≥2 capabilities that do not reduce to Structure, promote it per §3.3.

### 3.2 The dependency layering (a claim, and falsifiable)

**Structure is the addressing scheme; the rest are attribution problems.** Total spend can be metered, raw logs kept, and a process isolated with no structure at all. What is impossible without named units is *attribution*: which step cost what, which role made that call, which config change caused that outcome.

```
Structure ──► Introspection ──► Cost management
     │              │        └─► Self-improvement
     │              └─────────► Security assurance (audit)
     └────────────────────────► Security enforcement (gate on named roles)
                              ► Context provisioning (inject at named steps)
                              ► Recovery (resume a named unit)
                              ► Human steering (gate at named points)
```

**Field evidence:** OBS-14 — the garage's telemetry produced numbers but reported "0 stored" against 38 actual writes, because work moved into *unnamed* subagent sessions. The measurement was not broken; the addressing was missing.

**Consequence for triage:** a capability whose concern sits downstream of an unmet upstream concern is not infeasible — but its cost-to-prove includes the upstream work, and that must be stated.

### 3.3 Emergent concerns (the open slot)

The seeded list is a starting frame, **not a closed set**. A fixed taxonomy would do to concerns exactly what a shipped-precedent screen does to capabilities: manufacture conformity one level up. Generation may propose new concerns, and is expected to.

**Two tiers, so the run still converges.** Seeded concerns carry this run's coverage obligation (§9). A proposed concern is recorded as a **finding in its own right** and enters the next round's frame; it does **not** retroactively expand this run's coverage grid.

**Promotion test** — a proposed concern must be all three:
1. **A property of operation, not a mechanism** (Rule 1, one level up).
2. **Irreducible** to a seeded concern. Most proposals are re-cuts — "auditability" is Introspection + evidence; "reliability" is Recovery; "portability" is a constraint on the representation, not an ability.
3. **Populated by ≥2 distinct capabilities.** A concern with one member is that capability wearing a hat.

Failing any test, it files as a capability under an existing concern, or as a mechanism. Promotion also requires placing it in the §3.2 layering.

## 4. The two run rules

**Rule 1 — WHAT-or-HOW test (admission).** Every candidate is phrased as **observable behavior**: *"the harness does X, observable as Y."* Never *"the harness uses Z."* A candidate statable only as a mechanism is a HOW and is rejected at admission — not triaged, not parked, rejected. This rule also governs mid-run amendments (the wfh-002 failure mode).

**Rule 2 — novelty pays in mechanism, not precedent.** The owner has explicitly asked for approaches never tried before, which forbids a "must have a shipped precedent" screen — that screen manufactures conformity. The screen is: **a candidate must name a mechanism by which it works.** A shipped precedent satisfies this; so does a physical, computational, or economic argument that stands on its own. What fails is *magic* — "an LLM could probably do it," "the system would learn to." Novelty is free; hand-waving is not.

## 5. Known constraints & prior art (inputs — do not re-derive)

Carried from wfh-002 as **inputs to generation**, not decisions to relitigate:

- **C-1 — Enforcement and evaluation are queen-side.** A knowledge substrate cannot enforce (jurati#12, ADR-008). "The graph enforces X" is infeasible; "the harness enforces X" is available.
- **C-2 — Semantic verdicts require LLM leaves.** Any capability stated as *deterministically decides* a prose claim is infeasible as written. Restate as *assists and records with a forced-binary audit trail*.
- **C-3 — Files stay source of truth** (W3 §4). Any capability requiring users to edit rows instead of files fights the ecosystem.
- **C-4 — Capability gating is the one thing an LLM structurally cannot do to itself.** It holds the credentials it would restrict. A *category* difference from every other harness function, which are gradients.

Prior art: `product/research/wfh-001/scout-candidates.md` (~20 shipped tools); `product/research/wfh-002/FINDINGS-W{1,2,3,5,6}`; jurati#12 / ASS-009 / ass-100/101.

## 6. Bounded investigation (workstreams)

### W0 — Build the generation surface (leader/researcher; precedes all generation)

Per **OBS-11**, the generator is only as good as the surface it is handed, and that surface must carry the **substrate**, not just the interface. Four inputs, assembled into one briefing:

- **W0-a — The landscape, re-cut by concern.** What ~20 shipped tools actually do, arranged against §3.1 (wfh-001 cut by *tool*; this cut is by *concern*, which is what makes gaps visible).
- **W0-b — The incumbent baseline.** What Claude-Code-as-harness **already provides free** — hooks, permission rules, settings, subagent types — by inspection. *Without this, generation produces capabilities we already have.* Live caveat (#179): this repo's cardinal invariants are unenforced prose with **zero** hooks and **zero** permission rules configured, so "the incumbent cannot do this" and "we never turned it on" are currently indistinguishable. See §11.
- **W0-c — The four constraints** (§5).
- **W0-d — The garage's own pain record**, as demand signal, mapped to concerns: OBS-5 (steering), OBS-10 (structure/introspection), OBS-13 (security/role boundary), OBS-14 (introspection/addressing), #174 silent subprocess death (recovery), #179 (security enforcement), D6 `created_by: anonymous` (introspection/provenance). The only field-observed failures of an LLM-driven harness we own — evidence, not anecdote.

### W1–W5 — Divergent generation (parallel hypothesizers, one lens each)

**Parallel, one lens per agent.** A single hypothesizer given five framings collapses to its dominant mode; agents locked to one lens each produce genuinely disjoint output. **Each lens works across all seeded concerns** and may propose emergent ones (§3.3). Output in Rule-1 form with a Rule-2 mechanism and a concern tag.

- **W1 — Cross-domain transplant (primary novelty engine).** The agent-harness field is ~3 years old and has borrowed almost nothing from the mature disciplines that solved authority-and-control before it. Mine deliberately: object-capability security and seL4; OS isolation (schedulers, cgroups, seccomp, supervision trees / OTP let-it-crash); aviation CRM, checklists, sterile-cockpit; the nuclear two-man rule; segregation of duties, four-eyes and audit trails from finance; air-traffic handoff; formal contracts and refinement; BPMN compensation and sagas; immunology and fault-tolerant control. **Empirical warrant:** the owner's RBAC/least-privilege observation — the highest-yield idea of wfh-002 — was itself an accidental transplant from access control, and out-performed everything generated inside the harness frame.
- **W2 — Constraint inversion.** For each of C-1…C-4 and each layering edge in §3.2: what becomes possible if it were false, or routed around? Which constraints are physics and which are merely current practice?
- **W3 — Adversarial / failure-mode.** What would a malicious, compromised, or merely misaligned agent do that this harness could not detect or prevent? What makes it fail catastrophically rather than loudly? Failures define required abilities; this lens reaches capabilities that "what should it do" never surfaces.
- **W4 — Scale extrapolation.** What is required at 100×: agent fleets, many repos, many owners, concurrent and long-running work, agents outliving a session? Abilities invisible at n=1 appear here.
- **W5 — Incumbent-gap.** Given W0-b, what can Claude-Code-as-harness **structurally** not do, however well configured? The honest opposite is equally in scope: which ambitions are already solved and should be dropped.

### W6 — Distillation (curator; mechanical, no merit judgment)

At full coverage the lenses will return 100+ candidates, most arriving several times in different clothing. Triage cannot take that raw, so a reduction step sits between generation and the cut — **mechanical only**:

- **Dedup and collapse re-cuts** across lenses into one canonical statement per ability.
- **Record convergence count and which lenses converged.** Independent rediscovery is the strongest signal this run produces — four lenses landing on the same ability, blind to each other by construction, is evidence in a way a single lens's enthusiasm is not. Convergence is an *input to triage* (screen 8), never a substitute for it.
- **Cluster by concern**; flag candidates spanning several.
- **Dedup against the existing graph** (reuse-first, per the curator contract) — wfh-001/wfh-002 nodes and the incumbent baseline.
- **Flag contradictions** between lenses rather than resolving them; a contradiction is triage's material.

**Boundary (load-bearing):** the curator distills; it does **not** rank, cut, or prioritize. That is the goal-owner's cut and then the human's gate. Merging the two loses the audit property single-writer discipline exists for — a candidate dropped in dedup would be indistinguishable from one cut on merit. Every drop carries a named reason and a named actor.

### W7 — Triage: COULD → SHOULD (goal-owner, the funnel's neck)

Route every candidate **in · out · needs-a-probe**, with a one-line reason. Screens in order:

1. **Rule 1** — is it a WHAT? (else reject)
2. **Rule 2** — is a mechanism named? (else reject)
3. **Concern mapping** — which concern does it serve? Serving none → out of frame. Proposing a *new* concern → §3.3 promotion test.
4. **Falsifiability** — what would show this ability is *not* worth having? An ability that cannot be wrong is a wish.
5. **Incumbent delta** — already free in the incumbent? (drop or downgrade)
6. **Differentiation** — binary (structurally impossible elsewhere) or gradient (done better here)? C-4 is the worked example of binary.
7. **Cost to prove** — the cheapest real artifact, **including any upstream concern work** implied by §3.2.
8. **Convergence** (from W6) — how many independent lenses reached it. A tie-breaker and a prior, **not** a screen: a single-lens candidate is not thereby weak (the highest-yield idea of wfh-002 came from one accidental transplant), and high convergence may only mean the idea is obvious.

Per the hypothesizer contract, generation **never grades itself**. That separation is what *permits* the dreaming — the wilder W1–W5 run, the more load triage carries.

## 7. Expected output

- **The capability space** — every candidate, by concern × lens, with mechanism and route. Rejected candidates retained with their reason (a rejected ability is a reusable finding; D10/D11).
- **The SHOULD shortlist** — routed `in`, ranked, each with its cheapest proof artifact named.
- **The probe queue** — `needs-a-probe`, each with the question that would settle it.
- **Emergent concerns** — proposed, tested against §3.3, recorded for the next round's frame.
- **A `position` finding** on the capability space, for the curator.
- Explicitly **not**: a capability board, a decomposition, an architecture, or any build.

**Graph hygiene (binding on the curator).** The full space stays in the FINDINGS files. The graph receives **verdicts about** the space — the position finding, the SHOULD shortlist, promoted concerns — never one node per dreamt candidate. A divergent run at this scale could otherwise deposit 100+ `grade:claimed` nodes of pure speculation into the KB, degrading every future retrieval. This is the wfh-002 curation discipline ("only the verdicts ABOUT it are graphed") applied to a much larger sprawl.

## 8. Proof bar

**None — deliberately.** Directional (D7): this run moves *structure* only. No candidate reaches `partial` or `proven`; nothing is demonstrated. The firewall is untouched by construction.

Honest cost, stated up front: this is the **third consecutive structure-only run**, and the garage still has zero `proven` nodes on either board. An accepted trade — mapping the space first should make the *next* proof target materially better-chosen than wfh-002's W4 template was. §11 is the one option that would break the streak.

## 9. Coverage / done call

**A lens × seeded-concern grid, checked for holes** — not per-lens dryness (which is unfalsifiable).

- A **cell** is done when a fresh pass on that lens produces no candidate for that concern that is substantively new.
- A **hole** (a cell no lens ever populated) is a finding, not an error — it may mean the concern is already solved, or that no lens can see it. Record which.
- **The concerns are a hole-detector, never a quota.** It is a legitimate and expected outcome for a concern to finish with **zero** `in` routes. Do not manufacture candidates to fill a box; a run that routes one capability per concern should be suspected of exactly that.
- Emergent concerns do **not** extend this run's grid (§3.3, two-tier).
- Human confirms coverage at the gate.

## 10. Explicitly out of scope

Architecture and mechanism selection (the point of the reframe); decomposition into a capability board (the *next* run); any build; and the three items parked from wfh-002 with reasons recorded — the definition-graph index substrate, the rules-engine internals, and the judge model tiering. Parked, not settled: they re-enter when an ability that needs them is routed `in`.

## 11. Experimentation — settled: after this review

**Owner decision (2026-07-25): all experimentation follows this review.** No probe, spike, or configuration test runs inside wfh-004. The hooks-and-permissions experiment (configure hooks + permission rules for the three cardinal invariants, then deliberately attempt OBS-5/10/13-class violations) is a **follow-on probe**, queued from this run's probe queue rather than run as a pre-step.

**Consequence to carry, not to fix:** W0-b's incumbent baseline is established **by inspection only**. It therefore cannot distinguish *"the incumbent cannot express this boundary"* from *"we never configured it"* (#179 — zero hooks, zero permission rules in this repo today). Every W5 incumbent-gap finding and every Security candidate inherits that ambiguity.

**Binding on triage:** any candidate whose `in`/`out` route depends on that distinction must be routed **`needs-a-probe`, never `out`** — and the probe named. Routing such a candidate `out` on an inspection-only baseline would be an unevidenced kill, which is the mirror image of an unevidenced proof and equally a firewall violation in spirit.

## 12. Governing protocol + deviations

**Protocol:** `.claude/workflow/theme-scan.md` — phases **scan → hypothesize → triage → formalize**, roles `research-leader` · `hypothesizer` (divergent) · `goal-owner` (convergent) · `factory-curator` (single writer), *"no POC/validator — this protocol never proves."* That matches this scope's directional, structure-only bar exactly. Its INIT (all three D1 surfaces open **before any specialist spawns**), its **no-graph-writes-until-post-triage** rule (lesson #172), and its three-tier formalize apply unchanged.

**This SCOPE is authoritative where the two differ.** Five deviations, each needing owner sign-off at the gate:

| # | Protocol says | wfh-004 does | Why |
|---|---|---|---|
| D-a | `scan` phase: scouts discover candidate **technologies** | **W0** builds a generation **surface** (landscape re-cut by concern · incumbent baseline · constraints · pain record) | This run is capability-pull at product altitude, not technology-push. Nothing external needs discovering; wfh-001 already scanned it. |
| D-b | one `hypothesizer` **per candidate** | one **per lens** (§6 W1–W5), each working all seeded concerns | The generative axis is the lens, not a technology. One agent given five framings collapses to its dominant mode. |
| D-c | curator appears only in `formalize`, post-gate | **W6 distillation** inserted **before** triage | 100+ candidates are not triageable raw. **File-only, zero graph writes** — so lesson #172 holds intact. The curator distills; it does not rank. |
| D-d | coverage = per-candidate fan-out thinness | **lens × seeded-concern grid**, checked for holes (§9) | Per-lens dryness is unfalsifiable; a grid hole is checkable and is itself a finding. |
| D-e | *(no equivalent)* | **§3.3 emergent concerns**, two-tier | The frame must stay open or it manufactures conformity one level up (§3.3). |

**Formalize maps onto the protocol's existing three tiers with no new machinery:** SHOULD-shortlist + promoted concerns → tier 1 (survivors); `needs-a-probe` with its re-enter-when condition → tier 2 (parked, few and load-bearing); everything routed `out` → tier 3 (fold-findings **naming** each, so the next scan's dedup still works). The `position` finding on the capability space is the synthesis verdict.

**Known operational hazards for the leader** (all field-observed, all live):
- **#173** — a leader running as a subagent has **twice** lacked the Task tool to spawn its specialists. This run needs 8+ spawns; verify the spawn path before the first phase, not after it stalls.
- **OBS-7** — specialists cannot write files; they return markdown inline and the **leader persists**. Five lenses of deliberately wide output is a heavy context load: persist each lens the moment it returns, do not collect all five first.
- **#174** — a background specialist died silently and needed a manual respawn nudge. Five parallel hypothesizers multiply that risk; checkpoint after each return.
- **OBS-5 / OBS-13** — blocking prompts at the **gates only**; an in-envelope steer is executed with defaults and surfaced in the Issue, never as a blocking question.

## Amendments

*(append-only, dated; every amendment must pass the Rule-1 WHAT-or-HOW test at admission — D3)*

### A-1 — 2026-07-25 · Budget envelope set (owner)

`themes.md` carries no budget envelope for `theme:workflow-harness`. Owner set it at the INIT gate:
**18–22 specialist spawns** — 3 surface (W0-a/b/d) · 6 round-1 lenses · ~6 targeted round-2 lenses ·
curator (W6) · goal-owner (W7). Exhausting the §9 grid is the done-condition, and it costs more than
one generation pass; the envelope is sized for two.

*Rule-1 admission: N/A — an operating parameter, not a candidate.*

### A-2 — 2026-07-25 · Exhaustion is the done-condition; generation runs ≥2 rounds (owner)

> *"the purpose of this run MUST exhaust the options, so we can set real product goals"* — owner, 2026-07-25.

Reinforces §9 and §4 Rule 1 against the run's dominant failure mode: **jumping to an architecture or a
POC before the WHAT space is mapped** (the wfh-002 failure, repeated). Operationalized as:

1. **Rule 1 enforced at the lens, not deferred to triage.** Each hypothesizer applies the WHAT-or-HOW
   test as a hard output filter *before writing a candidate down*. The ability statement and the
   mechanism are **separate required fields**, so a mechanism cannot smuggle itself into the ability.
   A candidate statable only as *"the harness uses <mechanism>"* is never recorded.
2. **Generation is ≥2 rounds.** Round 1 wide; round 2 re-spawns per lens against every §9 grid cell that
   returned thin or empty, **handed round 1's output** so it cannot re-emit. A cell closes when a fresh
   pass adds nothing substantively new. A cell no lens can populate is recorded as a **hole**, naming
   which lens failed to see it.
3. **Honest bound on the claim.** Exhaustion is **relative to the named lenses × named concerns**, plus
   any §3.3 emergent concern. A run claiming absolute exhaustion would be lying; this one claims grid
   closure with holes recorded.
4. **The drift guard binds the back half too.** W6 dedups and counts convergence — it does not rank or
   choose. W7 screen 7 ("cheapest proof artifact") is the one place HOW legitimately re-enters: naming
   what would *settle* a question is in scope; selecting a design is not. **Nothing in this run selects
   a substrate, a representation, or a build.**

*Rule-1 admission: N/A — a run-discipline amendment, not a candidate.*

### A-3 — 2026-07-25 · Inference minimality: a declared field, a triage screen, and a sixth lens (owner)

> *"I'm motivated to try something novel, because I've not seen something out there that IMO has nailed
> the solution, and really broken down the fewest number of parts in which inference is needed"* — owner, 2026-07-25.

The owner's design intuition is the **dual of C-2**: C-2 establishes that semantic verdicts bottom out
in a model call; this asks **where the minimal cut actually is**. Admitted in three places, deliberately
**not** as a generation constraint:

- **NOT a constraint on W1–L6 generation.** Inference-minimality is a *narrowing* criterion, and the
  funnel narrows at the neck, not the mouth. Applied during generation it would suppress candidates
  before they were written down — precisely the A-2 failure mode one level up.
- **A required field on every candidate — the inference surface.** Each candidate declares where a model
  call is **structurally irreducible** versus where it is **merely current practice**. Characterization,
  not constraint; costs the lens nothing and gives triage something real to score.
- **Triage screen 9 — inference minimality.** Appended to §7 W7's eight screens, scored on the declared
  field: how few irreducible inference points does this ability need, and is the rest deterministic?
- **A sixth round-1 lens, L6 — inference-minimality.** Charter: per concern, what is decidable
  **deterministically**, what **genuinely requires** inference, and what **uses inference today only
  because nobody built the deterministic path**. The third category is the novelty-with-benefit
  reservoir. No existing lens asks this squarely — W2 (constraint inversion) glances at it via C-2.

**Novelty posture — confirmed, not new.** Rule 2 (§4) already forbids a shipped-precedent screen and is
exactly the owner's stated position: novelty is free, hand-waving is not. One guard added: **W0-a's
landscape is a dedup reference, not a menu.** Its job is to stop us re-inventing what exists — never to
bound what we may want. Lenses are told this explicitly, because W0-a returned framed as "state of the
art / nobody ships X," which anchors toward incremental deltas off the incumbent.

*Rule-1 admission: passes — the lens and the screen govern candidates; they are not themselves
candidates. The declared inference surface is a property of a stated ability, not a mechanism claim.*
