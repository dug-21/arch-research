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

### A-4 — 2026-07-25 · The inherited retro obligation, discharged into this run's CLOSE (leader)

**Found by the run, about the run.** Two round-1 lenses independently flagged that **P-19 has reproduced
into wfh-004**:

- L5: *"P-19 has reproduced into this run: wfh-004's SCOPE carries no retro workstream — L5-27's pain,
  live in the run that is cataloguing it."*
- L1-49 (evidence field): *"the obligation is **currently evaporating again**, live."*

The facts: wfh-002's close-out deferred `factory-retro` to its successor in writing — *"Not performed,
not partially performed"* — the successor is this run, and this SCOPE was written without a retro
workstream. That is the **fourth** occurrence of the same failure mode (P-19 records three), and it was
about to happen inside the run whose own pain register documents it. Left alone it would have been
discovered by a future W0-d sweep, exactly as P-12/P-14/P-26 were.

**Recorded as a binding obligation on this run's CLOSE**, per `theme-scan` CLOSE (*"Trigger
`factory-retro`"*):

1. `factory-retro` runs at CLOSE, covering **both** wfh-002 (inherited, undischarged) and wfh-004.
2. The close-out states the obligation as discharged or names it as breached. **Not silently omitted** —
   the failure mode is silence, not refusal.
3. If the owner defers it again, the deferral is recorded *here* with its carrier named, so the next
   successor inherits a written obligation rather than a gap.

**Scope discipline:** this is not scope expansion. `factory-retro` is already in the governing
protocol's CLOSE; A-4 records an inherited obligation that was about to evaporate, and names where it
discharges. No workstream is added and no generation is affected.

*Rule-1 admission: N/A — an obligation record, not a candidate. Noted for the irony and for W6: the
cheapest possible instance of emergent concern **E-1** (commitment tracking) is a run writing its own
obligations down where the successor must read them. This amendment is that mechanism, executed by hand,
at n=1.*

### A-5 — 2026-07-25 · The target is agentic workflows in general, not the garage (owner)

> *"we're not just thinking about creating this for our garage… this is for all agentic workflows… SDLC
> and research and potentially others. Don't get narrow."* — owner, 2026-07-25

**The risk this names is real and specific to this run's construction.** The W0 surface is
garage-shaped by design: **W0-b** is an inspection of *this repo's* incumbent, and **W0-d** is *this
garage's* pain register. Generation was handed a research-domain evidence base, so an
un-corrected triage would silently select for research-run abilities.

**The honest structural read, which shapes the correction.** The skew is in the **evidence column**,
not the **ability column**. The mechanisms the lenses paid in come from aviation, nuclear operations,
finance, medicine, insurance, epidemiology, power grids, maritime, ocap security, distributed systems,
military doctrine, manufacturing — **not one of them is a research discipline.** L2's inversions are
structural, L3's adversarial work is domain-free, L4's scale axes are domain-free, L6's D/I/P partition
is domain-free. So the candidate *abilities* are largely domain-neutral already; what is garage-shaped
is which pain each cites. That means the correction belongs at **triage and distillation**, not in a
re-generation pass — and it is therefore free.

**Four binding consequences:**

1. **Triage screen 10 — domain generality (appended to §7 W7's screens).** Every candidate is classified:
   - **DOMAIN-NEUTRAL** — the ability and its mechanism hold unchanged across research, SDLC, ops,
     support, data engineering. Most of the register is expected here.
   - **DOMAIN-SHAPED** — the ability generalizes but its *statement* is research-flavored and must be
     restated at the general altitude before it is routed `in`. The restatement is required, not optional.
   - **GARAGE-SPECIFIC** — the ability only makes sense for this operation. **Demoted or dropped**, with
     the reason recorded (a dropped ability is still a reusable finding — §7, D10/D11).
2. **The second-domain substitution test.** For each candidate routed `in` or `needs-a-probe`, triage
   substitutes **an SDLC delivery run** for the research run and asks whether the ability's *argument*
   survives — not whether the example does. An ability whose argument dies under substitution is
   DOMAIN-SHAPED at best. SDLC is the named substitute because JURATI's own value-target set spans it and
   because the garage already runs an SDLC protocol family (`uni-*`) alongside the research one, so the
   contrast is available in-house rather than imagined.
3. **Prior art is binding, not optional.** **wfh-002's W5 ran exactly this test on the ontology** and
   returned **AGNOSTIC-WITH-GAPS: the skeleton is neutral, with three structural general-workflow holes.**
   W6 must read `product/research/wfh-002/FINDINGS-W5*` and carry those three named holes into
   distillation; if this run's register does not populate them, that is a **coverage hole to report**, not
   a silence. Do not re-derive what W5 already established.
4. **Evidence-class honesty stays as-is.** A candidate whose only evidence is a garage pain is not thereby
   GARAGE-SPECIFIC — P-19 (a dropped commitment) and P-01 (an interruption policy that would not bind) are
   research-run instances of failure modes any multi-agent operation has. **Triage classifies on the
   argument's reach, never on where the anecdote came from.** Conversely, "no field pain" does not mean
   "not general" — L3's 18 `reasoned` rows and the entire steering-redirection cell are precedent-free by
   construction, and their generality rests on mechanism alone.

**Not changed:** the run stays directional and structure-only; no re-generation pass is spawned; the
budget envelope (A-1) is unaffected. If triage finds the register genuinely narrow — more than a small
minority routed GARAGE-SPECIFIC — that is a finding to report to the owner, and the remedy is a
second-domain generation round in a *successor* run, not a mid-flight expansion of this one.

*Rule-1 admission: N/A — a screen and a classification discipline governing candidates; not itself a
candidate.*

### A-6 — 2026-07-25 · The layer test, and what this run's output is *for* (owner)

> *"we're determining the potential functionality in a harness we're considering to build over the LLMs.
> It would be built in Jurati, and the intention is for it to work SDLC and research somewhat equally,
> obviously the workflows themselves are different."* — owner, 2026-07-25

Refines A-5 in three ways. The third corrects a question A-5 framed wrongly.

**1. The deliverable is a build-decision input, not a build backlog.** The harness is *being considered*,
not committed. Therefore **L5's "residual after full configuration" is as load-bearing as the SHOULD
shortlist**, and the **drop-list is a first-class output, not a byproduct**. L5's finding stands as the
honest frame: if the W0-b probes land favourably, the case for building anything rests entirely on five
named absences, and any proposed ability that does not target one of them is re-buying something already
free in the incumbent. **Triage must report the case *against* building with the same rigour as the case
for.** §7's expected output is amended accordingly: the shortlist, the probe queue, **and** the
drop-list-with-reasons are co-equal deliverables.

**2. JURATI's constraints are design context, not hypotheticals.** The harness would be built in JURATI,
so C-1 (enforcement is queen-side), the workflow≠knowledge three-store boundary, and H8's
multi-tenant-from-the-start posture are live constraints on what "available" means — and L4's tenancy
step-function (isolation *believed* → isolation *demonstrable to a stranger*) is on the real roadmap
rather than a scale hypothetical.

**3. The layer test — supersedes A-5's trichotomy as the primary cut.**

> **"The workflows themselves are different"** is the load-bearing clause. The **harness** is domain-general;
> the **workflow definitions** that run on it are domain-specific. SDLC and research are two different
> *definitions*, not two different *harnesses*.

A-5 asked "does this ability generalize across domains?" That is the wrong first question, because it
mis-files a whole class of candidate. The right first question is:

**Is this a property of the harness, or a property of a workflow definition?**

- **HARNESS-LAYER** — the ability belongs to the engine: it holds for any workflow definition running on
  it. *(A unit that stops emitting is declared dead. A gate's satisfaction is recorded by the party that
  gated. Spend is metered per named unit.)* These are the run's product.
- **DEFINITION-LAYER** — the ability is really a feature of a *particular* workflow: the garage's
  firewall, its `grade:` vocabulary, its theme-scan phase order, its curator single-writer rule. **These
  are not garage-specific *defects* — they are correct content at the wrong layer.** The harness's job is
  to make such a rule *expressible and enforceable*; authoring it is the definition's job. A
  DEFINITION-LAYER candidate therefore converts into a HARNESS-LAYER requirement: *"the harness can
  express and enforce a declared single-writer constraint"* rather than *"the harness enforces the
  curator rule."* **Triage performs that conversion; it does not simply drop these.**
- **AMBIGUOUS** — argued both ways; state both readings.

**Why this matters more than A-5's version:** under A-5 alone, a candidate drawn from a garage pain risked
being classed GARAGE-SPECIFIC and dropped, when it was in fact a *correct harness requirement stated in
garage vocabulary*. The layer test recovers it at the right altitude instead of discarding it. A-5's
DOMAIN-NEUTRAL/SHAPED/SPECIFIC classes remain, applied **only within the HARNESS-LAYER set** — that is
where "does it hold for SDLC as well as research?" is the meaningful question.

**Sharper cross-check available in-house:** SDLC and research definitions already coexist here (`uni-*`
vs the factory protocols), so for any HARNESS-LAYER candidate triage can ask concretely — *would the
`uni-*` delivery protocol need this too, and would it need it differently?* An ability both definitions
need identically is the strongest class the run can produce. An ability they need *differently* is
evidence about the harness's **parameterization surface**, which is itself a finding worth recording.

*Rule-1 admission: N/A — a classification discipline and a scope-of-output clarification; not a candidate.*

### A-7 — 2026-07-25 · REFRAME: rebuild, do not patch (owner directive)

> *"completely redo anything that had the wrong frame"* — owner, 2026-07-25

A-5 and A-6 corrected the frame **at triage and distillation**, on the leader's judgment that the skew
sat in the evidence column rather than the ability column. **The owner overrode that judgment.** The
correction is a rebuild. This amendment records what was wrong-framed, what survives, and why —
so the rebuild is auditable and the salvage is not sunk-cost reasoning in disguise.

**The frame error, stated exactly.** The run generated against a surface assembled from **one domain**:
W0-b inspected this repo's *research* configuration; W0-d catalogued 30 incidents, all from *research*
runs. The target is a harness serving **SDLC and research roughly equally**. A single-domain demand
signal cannot establish a two-domain requirement, and no amount of downstream classification repairs an
input that was never gathered.

**Wrong-framed — rebuilt, not amended:**

| Artifact | Defect |
|---|---|
| `surface/BRIEFING.md` | Garage as implicit subject; no harness/definition layer cut (A-6); no build-decision framing |
| `surface/W0-b-incumbent-baseline.md` | Inspected only the research-side configuration |
| `surface/W0-d-pain-record.md` | 30 incidents, all research runs — single-domain demand signal |
| All 11 registers in `hypotheses/` | Generated against the above |
| `hypotheses/ROUND-1-COVERAGE.md` | §9 grid computed on the wrong frame |

**Survives — with the reason, so this is checkable rather than convenient:**

- **`W0-a-landscape-by-concern.md`** — characterizes ~30 *externally shipped tools*. Never garage
  evidence; most of those tools are coding agents, so if anything it is SDLC-weighted already.
- **`W0-c-constraints.md`** — C-1…C-4 are substrate and JURATI constraints (enforcement locus, semantic
  verdicts, files-as-source-of-truth, self-binding). Domain-independent by construction.
- **§3.1's eight concerns** — structure, context provisioning, security, introspection, cost,
  self-improvement, recovery, human steering are *harness* concerns. An SDLC harness has the same eight.
  The **axis** survives; the **evidence populating it** did not.
- **The ~330 candidate mechanisms** — sourced from aviation, nuclear operations, insurance, epidemiology,
  power grids, maritime, object-capability security, distributed systems, military doctrine,
  manufacturing, medicine, finance. **Not one is a research discipline.** They are re-admitted to the
  rebuild in exactly the status W0-a holds: **a dedup reference, not a menu** — they stop the rebuild
  re-deriving object-capability security from scratch, and they bound nothing about what it may want.
  Every re-admitted mechanism must be **re-stated at the harness layer against two-domain evidence** or
  dropped; carrying a candidate forward unchanged is the patch this amendment forbids.

**In flight:** `W0-b2` (SDLC incumbent baseline) and `W0-d2` (SDLC pain record) — the missing second
domain. The W6 distillation task was **stopped mid-run**: it was distilling the wrong-framed corpus, and
a well-audited answer to the wrong question is worse than none, because its audit trail lends it
authority.

**Budget:** the rebuild exceeds A-1's 18–22 envelope (~30 projected). Surfaced to the owner as a
blocking question before regeneration spawns — per §12's hazard note, an out-of-envelope change is not an
in-envelope steer and is not the leader's to absorb silently.

*Rule-1 admission: N/A — a run-direction record, not a candidate. Filed under E-1's own logic: a
superseded artifact that is not recorded as superseded is a live artifact wearing a stale frame, which is
exactly the P-19 shape this run has now hit twice.*

### A-8 — 2026-07-25 · The product thesis, and the rebuilt question (owner)

> *"I really want this done right… worth the spend… a lot cheaper at this stage than after we start
> building. This focus is for a new product, potentially a novel one. I want to minimize dependence on
> LLMs while raising security and reliability, but keep them for what they are good at. But this
> 'harness' we're talking about is critical, and I'm trying to ensure we have fully done our research
> assessment, to look at regular, and maybe non-traditional approaches to solve the challenges."*
> — owner, 2026-07-25

**Budget: released.** A-1's 18–22 envelope is superseded; the rebuild runs to completion. Rationale
recorded because it is the standing justification for every subsequent spend decision in this run:
*research is cheaper than rework once building starts.*

**The thesis, stated as the run's organizing question.** A-3 admitted inference-minimality as one lens
among six and one triage screen. That was an under-reading. It is **the product thesis**, and the rebuilt
run is organized around it:

> **What must an agentic workflow harness provide such that the LLM is required in as few places as
> possible — and the places it *is* required are the ones it is genuinely good at — while security and
> reliability go *up*, not down?**

This is not the same question the superseded run asked ("what must a harness provide?"). It is
strictly harder and strictly more useful, because it forces every candidate to declare **what it takes
off the model's plate, what it deliberately leaves there, and what security or reliability is bought by
the move.** It also aligns the run with the theme's own lens — *the LLM a directed, supporting component,
not the driver* — which the superseded run cited but never made load-bearing.

**Four binding consequences for the rebuild:**

1. **Inference minimality is promoted from lens to frame.** Every candidate, from every lens, carries the
   A-3 inference-surface field as a **required and scored** property, not an annotation. L6's D / I / P
   partition (decidable · irreducible · pseudo-irreducible-because-nobody-built-the-deterministic-path)
   becomes the rebuild's shared vocabulary. **The (P) reservoir is the product's opportunity surface.**
2. **Security and reliability are co-equal raised bars, not constraints to satisfy.** A candidate that
   removes inference but *lowers* either is a regression and must say so. A candidate that raises both
   *because* it removed inference is the thesis working, and should be named as such — L6 §5 already
   argues the mechanism (a guarantee is statable only over a deterministic path; any inference on the
   enforcement path demotes a guarantee to a tendency).
3. **"Keep them for what they are good at" requires knowing what that is — and we never established it.**
   The superseded surface characterized the *shipped field* (W0-a), the *incumbent* (W0-b), our
   *constraints* (W0-c), and our *pain* (W0-d). It never characterized **the component itself**. A run
   whose thesis is "use the LLM only where it is genuinely good" cannot proceed on an unexamined
   assumption about where that is. **New surface input W0-e** is chartered: the honest capability and
   failure envelope of the LLM *as a component of a control system* — what it is reliably good at, what
   it is unreliably good at (the dangerous middle), what it cannot do, and how each of those degrades
   under adversarial input, long horizons, and scale.
4. **Non-traditional approaches are explicitly in scope and will be resourced.** Rule 2 already forbids a
   shipped-precedent screen; A-8 goes further and makes unconventional mechanism a **deliberate search
   target**. The superseded run's single highest-yield vein was cross-domain transplant, and its own
   authors flagged unmined ground twice (L1: aviation over-concentration; R2-5: insurance-fraud/AML
   named as the un-mined adversarial-economics field). The rebuild resources that hunt properly rather
   than treating it as one lens of six.

**What this does not change:** the run stays **directional and structure-only**. It maps the space and
produces a build-decision input — shortlist, probe queue, and drop-list as co-equal outputs (A-6). It
does not select an architecture, choose a representation, or build (§10). The thesis sharpens *what is
generated and how it is scored*; it does not license the run to start designing.

*Rule-1 admission: N/A — a framing and resourcing directive. Note it passes the WHAT-or-HOW test anyway:
"the LLM is required in as few places as possible" is a property of the system's operation, observable as
a count of load-bearing inference points, not a mechanism.*
