# W0 — The generation surface (briefing for all lenses)

**Run:** `wfh-004` · Issue #48 · theme `theme:workflow-harness` · value-target JURATI (`dug-21/jurati`).
**Read this first, then the four inputs.** Per OBS-11, a generator is only as good as the surface it is
handed, and that surface must carry the **substrate**, not just the interface (P-28: a hypothesizer given
an interface-only surface produced half the yield; the corrected surface *doubled* non-obvious survival).

## The question you are generating against

> **What must an agentic harness provide** to enable structure, security, introspection, cost
> transparency and management, self-improvement, recovery, human steering, context provisioning — **and
> any further ability that research or generation surfaces**?

This is a **WHAT run.** It does not choose an architecture, does not decompose into a board, does not
build. Your output is *abilities*, not designs.

## The four inputs

| | File | What it is | How to use it |
|---|---|---|---|
| **W0-a** | `W0-a-landscape-by-concern.md` | ~30 shipped tools re-cut by concern; per-concern state-of-the-art, common denominator, and "nobody ships" | **A dedup reference, not a menu.** Its job is to stop you re-inventing what exists. It never bounds what you may want. |
| **W0-b** | `W0-b-incumbent-baseline.md` | Claude-Code-as-harness by inspection: A/B/C verdicts + a 12-item ambiguity register | Tells you what is already free. Note it **corrects** the premise that the repo has zero hooks. |
| **W0-c** | `W0-c-constraints.md` | The four wfh-002 constraints C-1…C-4 | Strong priors with named mechanisms — **not physics.** L2 is chartered to attack all four. |
| **W0-d** | `W0-d-pain-record.md` | 30 field-observed failures of an LLM-driven harness **we own**, mapped to concern | The only *evidence* on this surface. Everything else is survey or inspection. |

## The concern axis (SCOPE §3.1) — your coverage obligation

1. **Structure** — the shape of work exists as addressable units (roles, steps, sequence, dependencies, gates), so anything else can be said *about* something.
2. **Context provisioning** — what an agent knows at each step is decided, injected, and explainable: what went in, when, why, what was left out.
3. **Security** — authority is bounded and enforced *outside* the agent: least privilege by role, isolation, egress control, resistance to instructions arriving through data.
4. **Introspection** — what is happening now, what happened, and why: live trace, causal explanation, durable audit record.
5. **Cost transparency & management** — resource use metered, attributed to units of work, predicted, enforced against a budget.
6. **Self-improvement** — the harness measurably gets better: outcomes attributed to configuration, changes A/B-compared, improvements adopted on evidence.
7. **Recovery / durability** — work survives failure: a dead agent, hung subprocess, or interrupted run is detected, resumable, never silently abandoned.
8. **Human steering** — intent enters mid-run and is acted on: gates, redirection, correction. Correctable, not merely stoppable.

**You work all eight.** A concern where you have nothing is a **hole** — report it as a hole and say
*why your lens cannot see it*. That is a finding. **Never manufacture a candidate to fill a box**
(SCOPE §9: a run that routes one capability per concern should be suspected of exactly that).

**Emergent concerns (§3.3):** the seeded eight are a starting frame, not a closed set. Propose a new
concern if you find one. Test: (1) a property of *operation*, not a mechanism; (2) irreducible to a
seeded concern — most proposals are re-cuts; (3) populated by ≥2 distinct capabilities. W0-d already
proposes **E-1 commitment/obligation tracking** (5 pains) and argues **E-2 calibration** reduces to
evidence discipline. Engage with those rather than re-deriving them.

## The two run rules — hard, applied at admission

**Rule 1 — WHAT-or-HOW.** Every candidate is phrased as **observable behavior**: *"the harness does X,
observable as Y."* Never *"the harness uses Z."* A candidate statable only as a mechanism is rejected
**before you write it down**, not deferred to triage.

*The ability and the mechanism are separate required fields* — precisely so a mechanism cannot smuggle
itself into the ability statement.
- ✗ *"The harness uses an event-sourced log."* — mechanism wearing a hat.
- ✓ *"A run that dies mid-step resumes from the last completed step on a different machine, observable as
  the same run id continuing with no repeated side effects."* Mechanism: event-sourced replay (Temporal
  is the shipped proof it works).

**Rule 2 — novelty pays in mechanism, not precedent.** There is **no shipped-precedent screen** — that
screen manufactures conformity, and the owner has explicitly asked for approaches never tried before.
The bar is: **name a mechanism by which it works.** A shipped precedent satisfies this; so does a
physical, computational, or economic argument that stands on its own. What fails is *magic* — "an LLM
could probably do it," "the system would learn to."

> Owner, 2026-07-25: *"I'm motivated to try something novel, because I've not seen something out there
> that IMO has nailed the solution."* Wild is welcome. Hand-waving is not.

## Required output fields per candidate

| Field | Content |
|---|---|
| **ID** | `L<n>-<nn>` (your lens number) |
| **Ability** | Rule-1 form: *the harness does X, observable as Y*. One sentence. No mechanism. |
| **Concern** | One of the eight, or a proposed emergent one. Flag if it spans several. |
| **Mechanism** | Rule-2: *how* it could work. Name it. A precedent, or a standalone physical/computational/economic argument. |
| **Inference surface** | **Required (SCOPE A-3).** Where a model call is **structurally irreducible**, versus where inference is used today **only because nobody built the deterministic path**. Be concrete about the cut. |
| **Incumbent delta** | Free in W0-b already? A/B/C/ambiguous. If it turns on a W0-b ambiguity, say which (A-1…A-12). |
| **Evidence** | Any W0-d pain (P-nn) or W0-a gap it answers. `none` is acceptable — a candidate needs no field pain. |
| **Falsifier** | What would show this ability is *not* worth having. An ability that cannot be wrong is a wish. |

## Discipline

- **You generate. You do not grade, rank, prioritize, or decide.** That is triage (the funnel's neck) and
  then the human gate. The separation is what *permits* the dreaming — the wilder you run, the more load
  triage carries, and that is the intended trade.
- **Do not propose an architecture.** No substrate selection, no representation choice, no build plan.
  If your candidate only makes sense as one specific design, you have written a HOW.
- **Do not fill the inference-surface field with a preference for less inference.** Characterize the cut
  honestly, including where inference is genuinely irreducible. The *screening* on minimality happens at
  triage, not in your head — applying it during generation suppresses candidates before they exist.
- Read-only. **Write no files and no graph nodes.** Return markdown inline; the leader persists (OBS-7,
  P-29). Keep the register tight — one row per ability, prose only where a mechanism needs an argument.
