# The generation surface — v2 (rebuilt, two-domain)

**Run:** `wfh-004` · Issue #48 · theme `theme:workflow-harness`.
**Supersedes `BRIEFING.md`**, which framed the garage as the implicit subject and was built on a single-domain surface (SCOPE Amendment **A-7**).

**Read this in full, then the eight inputs.** Per OBS-11 a generator is only as good as the surface it is handed — and per **P-28**, a hypothesizer given an interface-only surface produced half the yield; the corrected surface **doubled** non-obvious survival. The surface *is* the run.

---

## 1. What is being decided

The owner is **considering building an agentic workflow harness**, in JURATI, over the LLMs. Not committed. This run produces the input to that decision.

> *"This focus is for a new product, potentially a novel one. I want to minimize dependence on LLMs while raising security and reliability, but keep them for what they are good at."* — owner, 2026-07-25

**The question you generate against:**

> **What must an agentic workflow harness provide such that the LLM is required in as few places as possible — and the places it *is* required are ones it is genuinely good at — while security and reliability go *up*, not down?**

It must serve **SDLC and research roughly equally.** The workflow *definitions* differ; the *harness* is one thing.

**Three co-equal outputs**, per A-6 — this is a build **decision**, not a build backlog:
1. The **shortlist** of abilities worth having.
2. The **probe queue** — what must be settled before anything is decided.
3. The **drop-list** — ambitions already solved, or solvable by configuration, with reasons. **Money saved is worth as much as money spent well.**

---

## 2. The layer cut — your first question about every candidate

> The **harness** is domain-general. The **workflow definitions** running on it are domain-specific.

- **HARNESS-LAYER** — a property of the engine; holds for any definition running on it. **This is the run's product.**
- **DEFINITION-LAYER** — a property of *a particular workflow*: a specific gate, role vocabulary, phase order, status alphabet. **Not a defect — correct content at the wrong altitude.** It **converts**: *"the harness enforces the curator single-writer rule"* → *"the harness can express and enforce a declared single-writer constraint."* **Convert; never drop.**
- **AMBIGUOUS** — argued both ways. State both.

**This is no longer a judgment call.** W0-b2b diffed five real workflow definitions (2 research authors × 3 SDLC protocols) and found the split empirically:

> The **same** hook-client binary, the **same** eight hook events, and the **same** `context_cycle` phase API run under a research definition *and* an SDLC definition, **in three repos, today** — while the phase vocabularies (`spec/develop/test/pr-review` vs `scan/hypothesize/triage/formalize`) differ entirely.
>
> **Phase-conditioned observation and injection is HARNESS-LAYER. The phase vocabulary is DEFINITION-LAYER. That is a configuration diff, not an inference.**

**Ten things all five definitions share** — the strongest harness-layer evidence available: a run identity that simultaneously names directory/branch/issue/cycle-topic/agent-id-prefix · a coordinator that never generates content · parallel spawn in one message · declared phase transitions · a blocking human checkpoint plus a rule for when the human may *not* be asked · **bounded rework at ≤2 then escalate (independent convergence on the same number)** · the file is the deliverable, the agent's message is not · retrieve prior art before generating · a scope guard · deliberately context-starved reviewers.

---

## 3. The eight inputs

| | File | What it is | How to use it |
|---|---|---|---|
| **W0-a** | `W0-a-landscape-by-concern.md` | ~30 shipped tools re-cut by concern | **A dedup reference, not a menu.** Stops you re-inventing what exists; never bounds what you may want |
| **W0-b** | `W0-b-incumbent-baseline.md` | Claude-Code-as-harness, research side, A/B/C + a 12-item ambiguity register | What is already free. Note it **corrects** the "zero hooks" premise |
| **W0-b2** | `W0-b2-sdlc-incumbent.md` | The SDLC-side incumbent; the free-for-SDLC list; an 11-row parameterization surface | **The merge gate is a 98.3% discipline, not an enforcement plane** |
| **W0-b2b** | `W0-b2b-protocol-diff-and-corpus.md` | The five-definition diff + artifact-corpus census | **Your layer-test instrument** |
| **W0-c** | `W0-c-constraints.md` | The four wfh-002 constraints C-1…C-4 | Strong priors with named mechanisms — **not physics**. W0-e already narrowed C-2 |
| **W0-d** | `W0-d-pain-record.md` | 30 research-run failures | Field evidence, research domain |
| **W0-d2** | `W0-d2-sdlc-pain-record.md` | 26 SDLC failures, **five rows census-backed over all 63 bugfix units** | Field evidence, SDLC domain. **Better than W0-d for any rate claim** |
| **W0-e** | `W0-e-llm-component-envelope.md` | The component itself: 21 function classes, reliably-good / **dangerous middle** / cannot | **What you may and may not route through the model** |

**Superseded, retained as a dedup reference:** `../hypotheses/` — 11 registers, ~330 candidates, built on the old frame (see `SUPERSEDED-FRAME.md`). Their **mechanisms** came from aviation, nuclear ops, insurance, epidemiology, power grids, maritime, object-capability security, distributed systems, military doctrine, manufacturing, medicine, finance — not one is a research discipline, so that work is not domain-contaminated. **A mechanism may be re-admitted only if re-stated at the harness layer against two-domain evidence.** Carrying a candidate forward unchanged is exactly the patch A-7 forbids.

---

## 4. The concern axis (SCOPE §3.1) — unchanged; an SDLC harness has the same eight

1. **Structure** — work exists as addressable units (roles, steps, sequence, dependencies, gates).
2. **Context provisioning** — what an agent knows at each step is decided, injected, and explainable, including what was left out.
3. **Security** — authority bounded and enforced *outside* the agent.
4. **Introspection** — what is happening, what happened, and why.
5. **Cost transparency & management** — metered, attributed, predicted, enforced.
6. **Self-improvement** — outcomes attributed to configuration, compared, **adopted** on evidence.
7. **Recovery / durability** — work survives failure; nothing silently abandoned.
8. **Human steering** — intent enters mid-run and is acted on.

**Emergent concerns (§3.3)** stay open. Two-tier test: a property of *operation* not a mechanism · irreducible to a seeded concern · populated by ≥2 distinct capabilities. **E-1 (commitment/obligation tracking)** was endorsed by all six prior lenses and is now populated from **both** domains — engage it, do not re-derive it.

---

## 5. What the two domains actually showed — the findings you must not re-derive

**The cross-domain result.** **14 of 30 research pains have same-failure-mode SDLC counterparts.** A failure recurring in two domains, two architectures, two protocols is the strongest harness-layer evidence this run can produce — **treat those 14 as the spine.**

**Sharper than agreement — shared origin.** P-05 and P-06 do not have SDLC *analogues*; they have SDLC **origins**. Issue #208 (2026-03-11) filed the subagent-attribution failure four months before the research side saw it; #46 recorded the deliberate trade of per-agent audit for throughput. *One harness-layer defect surfacing twice.*

**What SDLC gets free, and research must build:** a durable atomic unit that outlives its author · **an external non-model verifier with a machine-readable verdict** (research's verdicts bottom out in a model call; SDLC's bottom out in an exit code — **the largest structural asymmetry between the domains**) · a rollback primitive · a branch as a real isolation boundary · the diff as a bounded review unit · end-to-end external addressing · a pre-existing-failure baseline · **parking with a machine-checked re-entry condition** (xfail + mandatory issue, gate-verified) · a retro trigger that fires by itself.

→ For SDLC these are **integration** requirements; for research they have **no incumbent at all**. State which you mean.

**What enforcement actually bought — the sobering datum.** The SDLC side *does* configure enforcement: a PreToolUse hook, CI on every PR, PR review, a security reviewer, a gate validator. **And a merge still happened with no gate trace; a fix still shipped that made every failure read PASS; a published release still could not be installed.** Enforcement at the wrong altitude does not catch run-level failure.

**CI alarms on the pipeline, never on the unit of work.** Every census-backed failure happened with CI green — including the case where *the alarm itself returned PASS unconditionally and CI could not tell*. **Nothing observes the run as an object; SDLC adds one observer at the wrong altitude.**

**Review layers do not substitute for independence.** Two independent agent reviewers ratified a wrong diagnosis; the human caught it. **Adding review layers does not add independence when every layer is the same kind of reader.**

**Census-backed rates (prefer these over any single anecdote):** 62/63 units carry no retrospective trace · **52%** of bugfixes name a prior internal unit as the defect's origin, including four bugfix-caused-bugfixes · the two record stores disagree on whether a role ran — gate 71%, security 78%, design 79%, **verify/test 44%**.

**Cost — read this cell correctly.** The SDLC corpus records **zero** cost incidents in 610 issues. **That is absence of *record*, not absence of cost.** The research side has cost pains only because one run built an instrument and looked. **Unmeasured, not solved.**

**Two named blind spots, both domains:** **zero** adversarial / malicious / compromised-agent incidents anywhere — an attacker model has no field support in either domain, and must be generated from mechanism. And **almost nothing about mid-run steering failing, because there is no mid-run steering to fail** — read that as *no lens can see it*, not *solved*.

---

## 6. The component (W0-e) — binding on every candidate

**Reliably good:** NL→formalism with an external checker · small-label classification · span extraction **with a verified locator** · recall-oriented generation for a downstream filter · linguistic equivalence judgments · prose for a human reader.

**The dangerous middle** — well-formed output, no artifact on failure, error rate low enough that spot-checks pass. **You do not inherit a 5% error rate; you inherit an unknown and unobservable one.** Members: summarization feeding a machine (omission ~2.3× more common than fabrication, and omission leaves nothing to check) · carrying a number through prose · LLM-as-judge (biases are **systematic**, so voting reduces variance but **not** bias) · own-protocol compliance (**terminal constraints drop first — and that is where gates live**) · self-report · **absence detection** (attention is over what is present; there is no token for the thing that isn't there) · planning an unfamiliar task · confidence · counting.

**Cannot, in principle:** bound its own authority while holding the credentials (C-4) · guarantee instructions arriving in data are not executed (one undifferentiated channel) · know what is not in context · bitwise reproducibility as normally served · self-correct without an external signal · idempotent retry.

**The finding that revises the thesis:** seven of the nine dangerous-middle rows share one shape — *the model is asked to produce a claim about a body of material, and the harness holds no independent representation of that material to check it against.* Where such a representation exists, **the function leaves the middle immediately.**

> **The dangerous middle is largely a property of missing structure, not of the model.** So there are **two remedies**: route it off the model, **or** give its output something to be checked against. Generate for both.

**C-2, narrowed by evidence.** It survives, but the irreducible core is a **categorisation, not an essay**, and **the harness never needs the verdict to be *true*** — only attributable, bounded, recorded *before* the dependent action, and re-checkable. All four are deterministic. That is a much larger determinism budget than C-2's phrasing implies.

**The (P) reservoir — your opportunity surface.** *Inference is being used as a lossy reconstruction of information that existed earlier and was discarded.* Worked examples: an authorization that was a sentence instead of a typed count · "which roles ran" recoverable only from a transcript · a commitment that was prose in a close-out · "completion" that was a statement in text · consumption reconstructed by a parser. **Honest limit:** when the *producer* will not emit (provider quota), the information was never in the system and no harness determinism recovers it.

**Argue against the thesis where it's due.** Rules fail closed on the unenumerated; models degrade gracefully. Somebody must author and maintain the deterministic path. Collapsing (P)→(D) means instrumenting every producer — a distributed engineering bill. **And the sharpest one: a wrong rule is wrong *systematically*; a wrong model is wrong *stochastically*. Stochastic error is detectable by repetition; a deterministic error is invisible to every statistical instrument and reproduced identically forever.** Minimizing inference can reduce the *observability* of residual error while reducing its rate.

**Where the thesis is unambiguously right:** a guarantee is statable only over a path with no inference on it. **Inference on the enforcement path demotes a guarantee to a tendency** — and a tendency presented as a guarantee is the most expensive object in the run.

**Folklore, refuted:** emphasis, "IMPORTANT:", memory files (**P-01 is the direct counterexample — a file written specifically to stop a behaviour, and it recurred**) · intrinsic self-critique without an external signal. **Real:** forced binary / small answer set · minimal evidence span · external-feedback checking · version pinning · decomposition (**cost: it moves error to the seams, and the seams are usually unmeasured**).

---

## 7. The two run rules — hard, applied at admission

**Rule 1 — WHAT-or-HOW.** Every candidate is **observable behavior**: *"the harness does X, observable as Y."* Never *"the harness uses Z."* Rejected **before you write it down**. Ability and mechanism are **separate required fields** so a mechanism cannot smuggle itself into the ability.

**Rule 2 — novelty pays in mechanism, not precedent.** **No shipped-precedent screen.** Name a mechanism: a precedent, or a physical/computational/economic argument that stands alone. What fails is *magic*.

> The owner has asked for **regular and non-traditional approaches**. Wild is welcome; hand-waving is not. And note what the superseded round found: the deterministic answers were mostly **mature and boring** — double-entry, watchdogs, capabilities, flight plans, load shedding. **The novelty is likely in the *cut* — which functions come off the model — not in the parts.**

---

## 8. Required fields per candidate

| Field | Content |
|---|---|
| **ID** | `<lens>-<nn>` |
| **Ability** | Rule-1 form, one sentence, no mechanism |
| **Concern** | One of eight, or a proposed emergent one |
| **Layer** | HARNESS / DEFINITION→(converted statement) / AMBIGUOUS |
| **Mechanism** | Rule-2: how it could work. Named. |
| **Inference surface** | **D** decidable · **I** irreducible (say why) · **P** pseudo-irreducible (say what capture makes it D). **State what it takes off the model and what it deliberately leaves.** |
| **Security / reliability delta** | Does it raise, lower, or not touch each? **A candidate that removes inference but lowers either is a regression and must say so.** |
| **Domain** | Both-identically (**strongest class**) / both-differently → **name the parameterization** / one-domain-only (say which and why) |
| **Incumbent delta** | Research side and SDLC side separately — they differ. Cite W0-b ambiguities (A-nn) where it turns on one |
| **Evidence** | P-nn / S-nn / F-nn. Mark `field` vs `reasoned`. `none` is acceptable — Rule 2 does not require field pain |
| **Falsifier** | What would show this is *not* worth having |

---

## 9. Discipline

- **You generate. You do not grade, rank, prioritize, or decide.** That separation is what permits the dreaming — the wilder you run, the more load triage carries, and that is the intended trade.
- **Do not propose an architecture.** No substrate selection, no representation choice, no build plan. If a candidate only makes sense as one specific design, you have written a HOW. (SCOPE §10.)
- **Do not filter for less inference during generation.** Characterize the cut honestly, including where inference is genuinely irreducible. Minimality is scored at **triage**, not in your head — applying it during generation suppresses candidates before they exist.
- **A hole is a finding.** A concern you cannot populate: say so and say *why your lens cannot see it*. **Never manufacture a candidate to fill a box.**
- **The shared-surface caveat is live.** All prior lenses read the same W0 documents; convergence between them overstates independence. If you read the superseded registers, your agreements with them are **not** independent corroboration — say so.
- Read-only. **Write no files, no graph nodes.** Return markdown inline; the leader persists (OBS-7, P-29).
