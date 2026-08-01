# scout-merged.md — wfh-005 W5, cross-surface reconciliation

**Leader-authored** (scouts cannot see each other; they flag suspected aliases, the leader merges).
Inputs: `scout-literature.md` · `scout-products.md` · `scout-active-dev.md` · `scout-adjacent.md`.
**Nothing here is new evidence.** This file resolves aliases, records agreements and disagreements, fills the
coverage grid, and decides whether round two fires. Verdict synthesis is W6's, not this file's.

---

## 1. The alias merge — same idea, four names

Every scout independently flagged that its finds would be called something else elsewhere. They were right, and
the overlap is the single most important structural fact in this run: **five unrelated fields and two shipping
product classes converged on the same three mechanisms.** Convergence from independent surfaces is much stronger
evidence than four hits from one surface — but it also means the raw hit-count overstates the evidence base.
**Merged below; count each cluster once.**

### A1 — Phase-indexed authority *(the P2(i) cluster)*

| Surface | Name it arrived under | Independent? |
|---|---|---|
| literature | Task-Based Authorization Controls (Thomas & Sandhu 1997); Workflow Authorization Model (Atluri & Huang 1996); the SoD-in-workflow line (Bertino/Ferrari/Atluri 1999) | — |
| adjacent | **the same two papers**, reached through the BPM/van-der-Aalst line rather than the security line | **Yes — W1 and W4 found TBAC/WAM by different routes.** Merge; do not double-count |
| active-dev | GitHub Actions OIDC `job_workflow_ref` + `environment` subject claims; gh-aw's per-safe-output single-permission jobs; Lunar MCPX Tool Groups | Yes |
| products | Argo `serviceAccountName` per template, Tekton per-TaskRun; Actions per-job `permissions:` + environment protection | Yes |

**Merged:** one cluster, four independent confirmations, ~30 years deep, currently shipping at mass scale.

### A2 — Gate-input independence *(the P2(ii) cluster — four names, one invariant)*

Clark-Wilson enforcement rule **E4** (1987, certifier ≠ executor) · **DO-178C** verification independence
(verifier ≠ author) · **SLSA Build L3** non-falsifiable provenance (the control plane generates it; the build
step cannot reach the signing identity) · **measured boot / SRTM** (measure-before-execute into extend-only
registers). W1 reached DO-178C, SoD, SLSA and the non-interference line; W4 reached Clark-Wilson, DO-178C, SLSA
and measured boot. **The DO-178C and SLSA rows are the same finds, arrived at independently — merge.**

### A3 — Ceiling derived from declared demand *(the P2(iii) cluster)*

WASI/WIT worlds · Bazel and Nix hermetic sandboxing · in-toto `expected_materials`/`expected_products` ·
`gh aw compile` (declared `safe-outputs:` → the exact `permissions:` block) · AgentCore's Cedar schema
auto-generated from tool definitions · MCP's `WWW-Authenticate` scope declaration. Plus the **observation**-derived
variant, which is a different input and must not be merged into the same box: IAM Access Analyzer, `audit2rbac`,
Felt et al.'s Stowaway (2011), GitHub's `actions-permissions` monitor, Progent, MiniScope.
**Two boxes, not one: declaration-derived and observation-derived. All four surfaces hit at least one.**

### A4 — Inference on the path, guarantee intact *(the P3 counter-case)*

Progent (LLM authors the policy, an SMT solver decides narrow-vs-widen) · CaMeL (model plans, capability
interpreter enforces) · proof-carrying / certificate-checked generation · AgentCore's natural-language→Cedar
authoring with deterministic schema validation downstream · Claude Code's `auto` classifier sitting *after*
non-overridable deny rules · gh-aw threat detection gating writes *inside* a pipeline where the agent already
holds no write token · **DO-330's tool-qualification criterion** — an unassured tool is permitted on the path
precisely when its output is independently verified. Six instances, four surfaces, **one pattern**: untrusted
producer, trusted checker.

### A5 — Institutionalized bypass *(the P3 second flank)*

The compliance budget (Beautement/Sasse/Wonham 2008) · rational rejection of security advice (Herley 2009) ·
shadow security (Kirlappos 2014) · normalization of deviance (Vaughan) · practical drift (Snook) · drift to
danger (Rasmussen) · **DORA's measurement** that external change approval is negatively correlated with
delivery performance and uncorrelated with change-fail rate · and the shipped product form: `LOG_ONLY`,
`dryrun`/`warn`, `Audit`, Gatekeeper's exempt annotation, `threat-detection: false`, gh-aw issue **#29171**
requesting a runtime bypass, and the permission-bypass mode in coding agents.
**Four surfaces, one story, and it is a named theory with a measurement attached — not an anecdote about us.**

### A6 — `gh-aw` and Temporal *(product/active-dev overlap)*

W2 and W3 characterized the same two objects independently and agree on the substance. Both also independently
report the same graph defect: **`github/gh-aw` has no Unimatrix node** despite being the theme's first watchlist
entry and "the nearest shipping instance of the design," and **#160 (Temporal) carries a claim that is now
false** ("nobody has connected durable execution to agents" — Temporal ships plugins for LangGraph, OpenAI
Agents SDK, Google ADK and AWS Strands as of 2026-07-16). Curator items, post-gate.

### A7 — Naming collision the leader must not merge away

**"Soundness."** W4 flags it explicitly: in workflow nets, *soundness* already means deadlock/livelock freedom,
proper completion and no dead transitions (van der Aalst). Our "gate soundness rule" is a different property.
If W1's workflow-satisfiability material and W4's workflow-net material both reach the gate, they will look
like the same word. **They are not.** W4's proposed rename — **gate-input independence**, stated in the
read-set/write-set vocabulary database concurrency control already supplies — is adopted in this file.

**Also do not merge:** declaration-derived vs observation-derived ceilings (A3); `Cites`-style corroboration vs
independent discovery (A1/A2 above).

---

## 2. Disagreements between surfaces, resolved

**P2(ii) — active-dev says SURVIVES; literature and adjacent say FALSIFIED.** Not a contradiction; the surfaces
answered different questions. W3 searched for an *implementation* that states the rule and found none, reporting
a legible negative (Bazel, Nix, in-toto, SLSA, Earthly/Dagger all searched). W1 and W4 found the *principle*
established four ways in standards and formal models. **Merged reading: the principle is prior art; the
mechanically-checkable static condition over an author-declared workflow's phase write-sets was found by no
surface.** All three surfaces independently converge on that same residual, which makes it the most reliable
statement in this run — and it is a formalization claim, not a discovery.

**P5 — literature and active-dev say SURVIVES; products and adjacent say WOUNDED.** Again not a contradiction:
W1 and W3 tested *does the failure mode exist outside us* (yes, at scale, with issue trackers and 20,574-session
studies), while W2 and W4 tested *does anyone buy this shape* (mixed to negative — iBPMS retired, CAB measured
net-negative, AgentKit deprecated eight months after launch, buyer demand aimed at a different purchaser).
**Merged reading: the failures are real and external; the register is not evidence of the demand, and the
demand that exists is differently shaped and differently addressed.** W6 owns the verdict word.

**P1 — W4 says SURVIVES, everyone else says WOUNDED or NEEDS-A-PROBE.** W4 scoped its verdict to one cluster
(Hardy 1988) and said so explicitly, adding that confirming the easiest item in the set carries almost no
information about the rest. That is the correct reading and it is not a real disagreement.

---

## 3. Coverage grid — 5 positions × 4 surfaces

**20 of 20 cells populated. No empty cells. No unstaffed surface.** Sub-holes inside populated cells are named
in §4; per the standard, a hole must name the surface that failed to see it, and each one below does.

| | **W1 literature** | **W2 products** | **W3 active-dev** | **W4 adjacent** |
|---|---|---|---|---|
| **P1** citation set is real | **WOUNDED** — 4 of 6 clusters verified; C2 unresolvable, C4 unsupported (a count with no members); the enumerated list does not exist | **NEEDS-A-PROBE** — MCP authorization spec verified directly against the normative page; Cedar verified | **NEEDS-A-PROBE** — the 2026 cluster is real with code (FORTIS repo); one hit against: PCAS has no released artifact and disclaims synthesis | **SURVIVES** (this cluster only) — Hardy 1988 verified, `10.1145/54289.871709`; sharpened |
| **P2** novelty / absence | **FALSIFIED** — TBAC 1997; DO-178C/SLSA/SoD; Progent + Stowaway 2011 | **WOUNDED** — leg 3 falsified (gh-aw compiler, Cedar schema, Bazel/Nix, MCP); leg 2 a **declared hole for this surface** | **WOUNDED** — legs (i) and (iii) falsified in shipping code; **(ii) survives here**, legible negative | **FALSIFIED** — all three legs; five fields, structurally identical |
| **P3** minimize inference | **WOUNDED** — position, not count: proposal side vs deciding side, plus monotone semantics | **WOUNDED** — the exemption knob and the authoring path, neither of which P3 states | **WOUNDED** — inference ships *inside* a deterministic envelope, never as it; the binding constraint is friction | **WOUNDED** — DO-330 admits an unassured tool when its output is verified; DORA measures the deterministic gate as net-negative |
| **P4** build is necessary | **NEEDS-A-PROBE** — the eight-concern frame does not exist in the literature; probe named | **WOUNDED** → **ADOPT gh-aw + ASSEMBLE + narrow BUILD** | **WOUNDED** → **ASSEMBLE**; window closing ~6–12 months | **WOUNDED** → **ASSEMBLE**; build three things, not fifty-one |
| **P5** demand is real | **SURVIVES**, mis-weighted — concentrated on authority, constraint violation, evidence integrity | **WOUNDED** — right mechanisms, wrong buyer; AgentKit deprecation is a live negative on the canvas | **SURVIVES**, ranking wounded — issue trackers confirm 3 of 6; introspection and mid-run steering are ours alone | **WOUNDED** — the category ran twice and lost twice; 22 practitioners ask for the cells we score empty |

**Cold-leg compliance: 4 of 4 scouts returned cold-leg content.** No return was incomplete.

---

## 4. Named holes — inside populated cells

Each names the surface that failed to see it. None of them changes a verdict (see §5).

1. **Patent prior art — literature surface did not read it.** Five USPTO grants on automated least-privilege
   derivation surfaced incidentally and were not opened. Material for an absence claim in principle; immaterial
   here because P2 is already falsified from published work.
2. **Commercial CD stage-scoped RBAC (Harness, Spinnaker, Azure DevOps) — products surface did not reach it.**
   The unanswered question: does any commercial CD platform bind a credential set to `(pipeline, stage, role)`
   as one derived object rather than three hand-configured knobs?
3. **Rail interlocking, hardware sign-off flows, medical-device approval, TUF, SPKI/SDSI — adjacent surface did
   not search them.** W4 names rail interlocking as the one it most regrets: route locking is physically
   enforced phase-indexed authority where the actor cannot mint its own release.
4. **Non-English agent-framework ecosystems — active-dev surface did not search them.** A real hole on the
   highest-churn surface.
5. **The MDPI orchestration survey (`10.3390/fi18060326`) — literature surface left it unfetched.** The single
   most P4-relevant journal item not read.
6. **The gate-input-independence rule on the products surface** — W2 declared it out of reach by construction
   (no product performs data-dependency analysis over a gate predicate), which is a legitimate declared hole
   rather than a gap in effort.

---

## 5. Round two — **does not fire, and here is the reason**

The protocol makes round two grid-targeted, not automatic: cells left thin or empty get one further pass.
**No cell is empty and none is thin.** Every named hole in §4 sits inside a cell whose verdict is already
settled from other evidence, and each would only reinforce a verdict already reached:

- Holes 1, 2, 3 all bear on **P2**, which is **falsified from two independent surfaces** with structurally
  identical prior art. More prior art does not change *falsified*.
- Hole 4 bears on **P4**, already **wounded on all three surfaces that can see it**, with a converged routing.
- Hole 5 bears on **P4** likewise.
- Hole 6 is a declared structural hole, not a research gap.

**Budget consequence: 4 of the 10–12 spawns used, 0 round-two passes spent, 1 remaining for goal-owner triage.**
Spending round-two passes to further confirm a falsification would be waste, and the standard's own honesty rule
prefers a named hole to a redundant pass. Recorded so the decision is visible rather than implied.

**The one thing that would change P1's verdict is not a scout pass at all** — it is the owner pasting the
enumerated reference list into Issue #54. That is held open, non-blocking (`INIT.md`).

---

## 6. The emergent sixth position — four cold legs, two clusters

This is the run's highest-value output and the scouts converged on it without being able to see each other.

### Cluster 1 — **the declared workflow is a fiction** *(W1's P6 and W4's P6 are the same position)*

W1, from the literature: developers *"rarely specify tasks upfront; instead they refine requests progressively
and actively manage agent behavior throughout a session"* (20,574 sessions, 1,639 repos). So the phase graph is
not knowable **before a run**.

W4, from adjacent fields: every field where phase-indexed control worked is **high-repetition**, and the
modelling cost is amortized over hundreds of executions. BPM tried it on low-repetition knowledge work, failed,
and the OMG published CMMN in 2014 as the formal admission that the order of activities cannot be known in
advance. So the phase graph is not stable **across runs** either.

**These are the same assumption failing at two timescales, and together they are sharper than either alone:**

> Every mechanism in this theme takes a declared multi-phase workflow as its input. If that input is authored
> fresh per run, then "deriving the capability set from the phase" is **hand-writing the ceiling, moved one
> level up and renamed** — and the theme's entire value over TBAC (which already indexes to phase) evaporates.

**Leader spot-check — preliminary, and explicitly not the probe.** Three signals from this repo, gathered in
minutes and reported with their limits:
- `theme-scan.md` has **9** commits and `research-scope.md` **6**, both edited as recently as today. The phase
  graph is under continuous revision.
- **wfh-004 recorded 8 mid-run amendments (A-1…A-8) in one run**, including A-7, a full REFRAME that marked its
  own registers superseded.
- wfh-005 declares **5 protocol deviations** in its SCOPE.

*Limits, stated:* this is not the measurement W4 asked for. My scan for per-run deviations keyed on one
formatting convention that only wfh-005 uses, so it undercounts every other run; and protocol-file commit counts
measure method churn, not per-run phase-graph reuse. **Direction supports the position; magnitude is not
established.** The real probe — count how many runs executed a phase graph unchanged from a prior run — remains
unspent and is W4's named one-hour falsifier.

### Cluster 2 — **where enforcement can live** *(W2's P6, W3's C-1/C-2/C-3, W4's P7)*

Four related propositions, and two of them are in genuine tension, which is why they are worth carrying together:

- **W2 — enforcement is only severable where you are the sole credential or egress path.** Every structural
  enforcement instance in the whole scan lives in the plane that already holds the credential or the packet.
  A third-party harness cannot enforce except over what it brokers.
- **W3 — the harness is a compiler, not a runtime.** The most mature thing on the surface (`gh aw compile`)
  emits an artifact and gets out of the way; the guarantee is carried by a plane that already existed.
- **W3 — everything shipping is layered, and a single edge is a single bypass point.** *(Tension with W2: read
  together, the resolution is that **each layer must be a sole path for what that layer mediates** — sole-path
  is a per-plane property, not an architecture-wide one. Neither scout could see the other to say so.)*
- **W4 — every adjacent field puts the policy author outside the executor**, without exception. In the garage
  the same operation authors, executes and grades, and the definition is a markdown file any agent can edit.
  W2 reached the same place from the product side: gh-aw's self-improvement feature hands a model write access
  to the artifact every enforcement ceiling is derived from.

Also carried, not clustered: **W2's P7** (the build-once target changes quarterly), **W2's P8** (engine
pluggability is already commoditized; the tightening axis is substrate lock-in), and **W1's third finding** —
that the highest-signal failure class in both large corpora is **fabricated success reports**, which capability
gating cannot touch and which the eight concerns do not name at all.

---

## 7. Handoff to W6

Relay verbatim to the goal-owner: the merged clusters in §1, the resolved disagreements in §2, the filled grid
in §3, the named holes in §4, the round-two decision and its reason in §5, and **both cold-leg clusters in §6
with their attribution intact** — including the leader's own spot-check *and its stated limits*, so triage does
not read a direction as a measurement.

Four theme-revision signals were returned by scouts and must reach the owner **verbatim**, not summarized:
W2's reshape-around-the-compiler-and-attestation signal, W3's runtime-vs-compiler signal, W4's rename-and-
relabel-the-moat signal, and the merged sixth position.
