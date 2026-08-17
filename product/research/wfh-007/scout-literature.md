# scout-literature.md — wfh-007, research-literature surface, DISCOVERY

**Run:** `wfh-007` · Issue #64 · surface **S3 — research literature** · mode **DISCOVERY**
**agent_id:** `wfh-007-s3-scout` · read-only on Unimatrix, zero writes
**Date of reading:** 2026-08-17 · **Method stamp:** `wf-v0.24`
**Base taken as given, not re-derived:** wfh-005's settled prior art (TBAC/WAM · Clark-Wilson E4 / DO-178C / SLSA L3 / measured boot · WASI/Bazel/Nix/in-toto/`gh aw compile`). The property is called **gate-input independence**, never "soundness."
**Bounding statement:** nothing below moves status. Verifying a citation makes the citation real, not its claim `proven` (D7). **Hard stop declared:** the session's WebSearch budget (200/200) was exhausted mid-pass; the last two intended searches were not run and are named in §4.

---

## 1. Verdict per question

### Q1 — Capability vocabularies and their granularity failures → **FORMALLY BOUNDED, and the bound is negative. The sub-question about irreversibility is PARTLY SOLVED and much more recently than expected.**

**The trade-off the framing worries about is not folklore. It is two theorems and a measurement series.**

- **You cannot decide whether a vocabulary is safe.** Harrison, Ruzzo & Ullman (1976): in the general access-matrix protection model, *safety* — can subject *s* ever acquire right *r* over object *o* — is **undecidable** under surprisingly weak assumptions. Decidable only in restricted fragments (mono-operational: decidable; Take-Grant: linear time; Sandhu's TAM/SPM). The standard secondary reading is blunt: *most security policies of practical interest fall into the undecidable cases*. Any claim of the form "our vocabulary is least-privilege by construction" is either scoped to a decidable fragment or is not a claim.
- **You cannot cheaply compress one either.** The Role Mining Problem — recover a minimal role set from an observed user×permission relation — is **NP-complete** by reduction to Set Basis; Basic-RMP and Edge-RMP are both NP-hard (Vaidya, Atluri, Guo, *TISSEC* 13(3), 2010). A 2024 maximal-biclique approach is optimal on most instances and stalls on hard ones. So the engineering escape from role explosion is itself intractable in the worst case.
- **Both horns are measured, not theorised.** Coarse → over-privilege: Felt et al. 2011 (~1/3 of 940 Android apps); **Granite** (KTH/Chalmers, 2025-12) measures **46.6% of GitHub Actions jobs over-privileged** across 500 workflows / ~13k jobs, because permissions are job-level and steps within a job share them; **FORTIS** (2026) finds over-privilege in agent skills is "the norm rather than the exception" across ten frontier models. Fine → approval fatigue and the mining problem (settled base).

**The one genuinely positive result on this question is the type-system route, and it sidesteps mining entirely.** Instead of *deriving* a vocabulary from observation, make the vocabulary the type system and check the ceiling statically: capabilities as program variables regulating effects, with capability-safety as the property that untrusted code reaches only what it was handed. Craig, Potanin, Groves & Aldrich, *Capabilities: Effects for Free* (ICFEM 2018) shows effect bounds fall out of **type-checking alone** — no effect annotations, no whole-expression effect analysis. Odersky et al., **Tracking Capabilities for Safer Agents** (2026-03, rev. 2026-05) applies exactly this to agents: the agent emits Scala 3 code under **capture checking** rather than calling tools directly, which buys **local purity** (provably side-effect-free sub-computations) with, they report, no significant task-performance loss. This is the most credible thing I found on "a vocabulary expressive enough to be useful and fine-grained enough to gate."

**Irreversibility as a property the vocabulary must carry — this is the highest-value part of Q1 and it is NOT open.**

- **Planning has a formal definition and a decision procedure.** Faber, Morak & Chrpa, *Determining Action Reversibility in STRIPS Using Answer Set and Epistemic Logic Programming* (ICLP 2021): reversibility = effects revertible by applying other actions to return to the original state, with ASP/ELP encodings. Dead-end detection (states from which the goal is unreachable) is the classical treatment of the same property.
- **Agents now have a four-value taxonomy and an impossibility result.** Zhai, Li & Wang, **Revisable by Design** (2026-04-25) classifies every agent action as **Idempotent / Reversible / Compensable / Irreversible** and proves that *conflicting compensable actions impose unavoidable adaptation costs* and *conflicting irreversible actions make full specification satisfaction impossible* — and states the punchline the personal-OS framing needs verbatim: **"these costs are properties of the action space, not of the algorithm."** Their conclusion, "an agent's flexibility is bounded by its reversibility," is a design bound on any vocabulary, arrived at independently of us. Validated on StreamBench with real agents; code and benchmark published.
- **The compensation escape hatch has a named limit.** Sagas give compensation but not isolation or atomicity across external systems; compensation helps only when every externalised effect is reversible and has a correct handler — **it cannot prevent an irreversible send.**
- **Safety-critical domains define the class by irreversibility already.** The operative definition in the two-person-rule lineage is *a safety-critical operation is one which would or foreseeably could have irreversible physical consequences* (US AFI 91-104/91-117; the same definition appears in patent US9383740). A 0–1 irreversibility score per tool call is proposed in an ICLR-2026-workshop position paper (*The Controllability Trap*, 2026-03) — but the scale is **asserted, not validated**, and I say so.

**Verdict, stated for triage:** a vocabulary's *safety* is undecidable in general and its *minimisation* is NP-hard; a vocabulary that carries **consequence class** rather than only permission has a published taxonomy, a proved impossibility, and a planning-theoretic decision procedure. Anyone authoring a capability vocabulary who has not read Revisable-by-Design will re-derive its taxonomy badly.

### Q2 — Delegation and attenuation → **SOLVED as a mechanism · BOUNDED and known-expensive as revocation · GENUINELY OPEN as composition.**

- **Attenuation: solved, shipped, cheap.** Macaroons (Birgisson, Politz, Erlingsson, Taly, Vrable, Lentczner, NDSS 2014) — chained-HMAC bearer credentials with caveats that attenuate and contextually confine, with "expressiveness that rivals public-key-based mechanisms like SPKI/SDSI" at cookie-level cost. SPKI/SDSI itself carries an explicit delegation bit; X.509 carries `pathLenConstraint` for depth. There is no research question left in "pass reduced authority onward."
- **Depth-bounded delegation: solved, and now measured on the agent path.** Prakash, **AIP: Agent Identity Protocol** (2026-03-25) introduces **Invocation-Bound Capability Tokens (IBCT)**: a root block signed by the initiating human declares identity, initial scopes, a **budget ceiling**, a **maximum delegation depth**, and expiry; each hop appends a signed block that may only *narrow*, with widening rejected cryptographically. Compact mode = signed JWT; chained mode = Biscuit + Datalog. **Measured:** 0.049 ms verify (Rust) / 0.189 ms (Python), 0.22 ms over no-auth on MCP-over-HTTP, 2.35 ms (0.086% of end-to-end) in a real Gemini-2.5-Flash multi-agent deployment; 600 adversarial attempts, 100% rejection, with **delegation-depth violation** and **audit-evasion-via-empty-context** caught only by the chained model. Reference implementations in Python and Rust with cross-language interop.
- **Revocation: this is where the theory says it gets expensive, and there is now a bound worth knowing.** The settled statement is Chuat, Abdou, Sasse, Sprenger, Basin & Perrig, *SoK: Delegation and Revocation, the Missing Links in the Web's Chain of Trust* (EuroS&P 2020) — a 19-criterion framework, no dominating scheme, and the recommendation that short-lived delegated credentials plus an appropriate revocation system is what actually works. The agent-era sharpening: Parakhin, *The Bureaucracy of Speed* (2026-03) maps authorization revocation onto **cache coherence** and shows that **time-bounded (TTL) revocation has damage scaling O(v·TTL)** — proportional to agent velocity — while an **execution-count bound gives D ≤ n, independent of velocity**. A 60-second revocation window admits ~6×10³ unauthorised calls at 100 ops/tick, ~6×10⁵ at Lambda scale. **Single author, no venue, simulation only (120 runs, 120× reduction vs TTL lease)** — `claimed`, and I hold it as such. But the *shape* is the thing: TTL revocation is the wrong instrument for a fast actor, and that argument does not depend on the simulation.
- **Composition is the open leg, and it is the same open problem as 1980s database security.** Tallam, *Authorization Propagation in Multi-Agent AI Systems* (2026-05-06) names the three sub-problems as **transitive delegation, aggregation inference, and temporal validity**, and argues explicitly that this is not reducible to prompt injection and not addressed by RBAC/ABAC/ReBAC. Lotfi, Karmaker Shanto, Karim & **Bertino**, *Securing Agentic AI: From Per-Action Checks to Trajectory Assurance* (2026-08-03, ACM AI Leadership Summit visionary track) calls it "perhaps the most fundamental challenge": **sequences of individually permissible actions may collectively violate system-level constraints.** That is the *aggregation problem* — classifying a collection higher than any of its elements — which Denning's multilevel-security line raised in the 1980s and which secondary sources still describe as beyond the capability of available systems. **No one has solved it; two independent 2026 groups have re-named it.**

**Verdict:** attenuation and depth-bounding are done and cheap — adopt-shaped, not build-shaped. Revocation is hard, characterised, and the velocity-scaling result should govern any credential-lifetime choice. **Aggregation of individually-authorized actions is the surviving hard problem on this question**, it is forty years old, and it is the one a personal OS with six domains will hit first.

### Q3 — Workflow authorization on top of the settled base → **The complexity layer is SETTLED AND QUIESCENT. The agent layer moved, including since 2026-08-01.**

- **Workflow satisfiability: no movement, and the negative is legible.** WSP is NP-hard in general and **W[1]-hard**; **FPT for user-independent constraints**; variants exist for seniority, class-independent, valued and bi-objective forms; Wang & Li supply the resiliency bounds (settled base). I searched for 2024–2026 results and **found none** — the newest items returned were 2021–2022 solver-engineering papers. Treat the theoretical ceiling as set roughly a decade ago. If someone claims a new WSP complexity result, be suspicious.
- **What landed since wfh-005 closed (2026-08-01), in date order:**
  - **2026-08-03 — Bertino et al., trajectory assurance** (above). Position paper, no results, but a named research programme from a serious group, arguing per-action authorization is structurally insufficient. *This is the first post-wfh-005 item and it argues against the per-call gate the theme's architecture leans on.*
  - **2026-07-15/20 — Michael & Roesner (UW), *How Agents Ask for Permission: User Permissions for AI Agents, from Interfaces to Enforcement*.** Surveys **21 agent-permission proposals**, builds a taxonomy over (i) how policy is specified at the interface and internally, (ii) how internal policy is **derived from user input**, (iii) how it is enforced at runtime — then compares **five prominent commercial agents** against the literature and names the gaps. **This is the single most useful map for anyone about to design a personal-OS permission layer, and it is three weeks old.** Named academic authors at a real lab, unlike much of the 2026 preprint layer.
  - **2026-07 — *Toward cryptographically verifiable authorization for autonomous AI agents* (2607.21325).** Names the gap as: existing authn/authz establish identity and delegate authority but **do not produce cryptographic evidence that a concrete request satisfied policy in a specific execution context**. Surfaced, not fetched — do not cite downstream without opening it.
- **Over-privilege measurement — warm-leg re-check condition FIRED, twice.** Two benchmarks not in wfh-005's set: **FORTIS** (2026-05-09, v3 2026-06-14; 10 frontier models × 3 domains; finds failure is worst under *ordinary* conditions — incomplete specification, convenience framing, proximity to skill boundaries, **none adversarial** — and concludes the skill layer "is itself a primary source of privilege escalation"); and **ToolPrivBench** (2026-06-18, v2 2026-07-07; 8 domains, 5 risk patterns; **over-privileged tool selection is amplified by transient tool failures**, general safety alignment does not transfer, prompt-level controls give only limited mitigation, a privilege-aware post-training defence helps). Plus **Granite** (2025-12) as the non-agent measurement anchor at 46.6%.

**Verdict:** nothing since wfh-005 disturbs its base. Two things sharpen it: the granularity failure is now measured *below* the job/skill boundary (Granite, FORTIS), and the field's leading edge has moved from *per-action* to *trajectory* authorization — which is the aggregation problem of Q2 arriving under a third name.

### Q4 — The evidence-graded commit primitive → **PARTLY SOLVED, and the decomposition is the finding. This is the most decision-changing thing in this file.**

The framing sentence — *"a claim is cheap; a commitment requires declared-kind evidence and is append-only"* — is not one primitive. It is **five**, each separately named, formalized, and in four of five cases shipped. Stated plainly, in the order the sentence packs them:

| Clause of the framing | Its name in the literature | Status |
|---|---|---|
| a claim is not acceptable unless it traces to evidence | **Evidential Argumentation System** — Oren & Norman, *Semantics for Evidence-Based Argumentation*, COMMA 2008 (IOS Press, FAIA 172, pp. 276–284). Standard arguments must trace back to **prima facie** arguments, the only ones valid without support; e-grounded / e-preferred / e-stable extensions modify Dung's model to carry evidence. Alongside: **justification logic** (Artemov; Artemov & Fitting, CUP 2019) where `t:F` reads *t is evidence for F*, and van Benthem & Pacuit, *Dynamic logics of evidence-based beliefs* (Studia Logica, 2011) | **solved as formal semantics**, 18 years old |
| **declared-kind** evidence | **in-toto Attestation Framework**: a `Statement` binds a `subject` to a `predicate` whose schema is named by **`predicateType`** — the declared kind, with SLSA Provenance as one instance. In medicine: **GRADE**, four certainty levels with kind-indexed starting points (RCT → high, observational → low) and explicit up/down-grading criteria. In safety engineering: **CAE — Claims, Arguments, Evidence** (Bloomfield/Adelard, 1998), itself descended from **Toulmin (1958): claim / data / warrant / backing / qualifier / rebuttal** | **solved and shipped**, three times independently |
| **append-only**, verifiable | **history trees** — Crosby & Wallach, *Efficient Data Structures for Tamper-Evident Logging*, USENIX Security 2009: O(log n) inclusion **and consistency** proofs, ~3 KB proof for 80M events. Deployed as **RFC 6962 Certificate Transparency**, Trillian, CONIKS | **solved and deployed at internet scale** |
| when it happened vs when we learned it | **bitemporal modeling** — Jensen & Snodgrass, Bitemporal Conceptual Data Model (1994), basis of **ISO SQL:2011**. Event-sourced events must themselves carry both timelines or they cannot support bitemporal history | **solved and standardised** |
| where this value came from, by which derivation | **provenance semirings** — Green, Karvounarakis & Tannen, PODS 2007: semiring-annotated relations, from which why-provenance, bag semantics, incomplete and probabilistic databases all fall out of one algebra; extended to Datalog via ω-continuous semirings. Plus **W3C PROV** with a real model-theoretic semantics (PROV-SEM, ed. Cheney) and a formal validity notion in **PROV-CONSTRAINTS** — uniqueness, event-ordering, impossibility and type constraints; *a PROV instance is valid iff it has a model* | **solved as formal semantics and as a W3C spec** |

**The composition is also partly claimed, and this is what triage must weigh.** AIP's **IBCT** (§Q2) explicitly *"fuses identity, attenuated authorization, and provenance binding into a single append-only token chain"* — authority plus evidence plus append-only in one object, with two reference implementations and sub-millisecond verification, published 2026-03. And **PunkGo / "Right to History"** (Zhang, 2026-02-23) is a **Rust "sovereignty kernel"** unifying RFC 6962 Merkle audit logs + capability-based isolation + energy-budget governance + a human-approval mechanism, with five stated invariants and proof sketches, adversarially tested, at **sub-1.3 ms median action latency, ~400 actions/s, 448-byte inclusion proofs at 10k entries** — motivated by the EU AI Act's logging mandate and explicitly aimed at *agents running on personal hardware where no centralised provider controls the log*. That is a large fraction of the personal-OS kernel-plus-evidence-log, built and measured, by one author, six months ago.

**And there is a negative result the framing needs before it designs anything.** The one part of "evidence-graded" that has been tried hardest and has **failed** is the grading *arithmetic*. Graydon & Holloway, *An investigation of proposed techniques for quantifying confidence in assurance arguments* (**Safety Science**, 2017) surveyed the proposed quantitative confidence methods and **showed by counterexample that most produce implausible results**, while finding no empirical evidence of scalability; work is still ongoing on scalability of these methods in 2026 (arXiv 2606.15480). Thirty years of assurance-case practice grades evidence **categorically** — by kind, independence and coverage — and has repeatedly failed to make the grade **numeric**.

**Verdict:** the evidence-graded commit is **not novel and not unsolved**; it is a **known five-part decomposition** in which every part is separately settled and at least two 2026 systems have already attempted the fusion. What is genuinely unclaimed is narrower than the framing implies and must be stated against IBCT, in-toto's `Statement`/`predicateType`, PunkGo and PROV **by name**. Recording it plainly, per the assignment's instruction: **if the framing intends "evidence-graded commit" as a differentiator, that position does not survive contact with this surface in its current form.**

---

## 2. Candidates

Reuse-first, run against Unimatrix before writing (`context_search`, `agent_id: wfh-007-s3-scout`, k=15, two queries over `technology`+`finding`). **Result: the graph holds none of the works below.** Nearest neighbours returned were #190 (P2 falsification finding), #202 Cedar, #199 CASA, #205 SPIFFE/Vault — all products/active-dev nodes from wfh-005 — plus the jurati-001 cluster #256–#263. Top semantic score against a literature query was 0.48 and it was capability **#256**. **Every candidate below is NEW to the graph.** wfh-005's literature surface contributed 30 of 158 citations; this pass adds a distinct body with no collisions.

---

### C1 — Reversibility taxonomy with an impossibility result (*Revisable by Design*)
- **What it is / how it works.** Rejects the transaction model of agent execution in favour of a *stream* paradigm where user intervention and agent execution interleave. To make that tractable it classifies **every** action as **Idempotent / Reversible / Compensable / Irreversible**, and proves the two costs are properties of the *action space*: conflicting compensable actions impose unavoidable adaptation cost; conflicting irreversible actions make full specification satisfaction **impossible**. The algorithm (Revision Absorber, Earliest-Conflict Rollback) is structurally optimal under stated assumptions.
- **Resource envelope.** Algorithmic, not infrastructural: matches full-restart quality while wasting **an order of magnitude fewer completed steps**. Implementation cost is the classification of the action set — which is exactly the labour a capability vocabulary would incur anyway.
- **Maturity & evidence.** *Demonstrated:* StreamBench experiments with real LLM agents validating the predictions; code, data and benchmark published. *Claimed:* optimality "under mild assumptions" — I did not read the proofs. Three named authors, no affiliation established, no venue established (2026-04-25 preprint).
- **Source signal.** `external-scan` (cold leg — reached via a planning/reversibility query, not a security query).
- **Lens rationale.** Directly answers the run's proposed grid dimension *irreversibility and consequence*, at the level of what a vocabulary must carry.
- **Dedup.** NEW.
- **Alias flag.** S2 will meet this as Home Assistant's *absence* of a destructive-action class; S4 as *two-person rule / safety-critical operation*; active-dev as *dry-run / confirm / undo*.

### C2 — Invocation-Bound Capability Tokens (AIP)
- **What it is / how it works.** A delegation chain as an append-only signed token: root block (human-signed) declares identity, initial scopes, **budget ceiling**, **max delegation depth**, expiry; each hop appends a signed delegation block that may only attenuate — widening fails verification cryptographically. Compact mode = JWT (single hop); chained mode = **Biscuit + Datalog** (multi-hop). Every invocation is recorded append-only, giving provenance-oriented completion records over the same object that carries authority.
- **Resource envelope.** **0.049 ms verify (Rust) / 0.189 ms (Python); 0.22 ms over no-auth on MCP-over-HTTP; 2.35 ms (0.086%) end-to-end in a real Gemini-2.5-Flash multi-agent deployment.** Reference implementations in Python and Rust, cross-language interop.
- **Maturity & evidence.** *Demonstrated:* measured overheads; 600 adversarial attempts, 100% rejection; two attack classes (delegation-depth violation, audit evasion via empty context) caught only by the chained model. *Claimed:* the survey claim that no prior implemented protocol jointly combines these five properties — that is the author's absence claim and carries the same discount we apply to our own. Single author (Sunil Prakash), no affiliation established, no venue.
- **Source signal.** `external-scan`.
- **Lens rationale.** It is the composition — authority + attenuation + append-only evidence — the framing treats as its differentiator, already built.
- **Dedup.** NEW. Adjacent to #202 (Cedar per-call authority) but a different layer: token-carried rather than gateway-evaluated.
- **Alias flag.** Active-dev will find this as **Biscuit** / macaroons / "attenuable tokens"; products as "token exchange / on-behalf-of / downscoped credentials."

### C3 — PunkGo, a "sovereignty kernel" for verifiable agent execution
- **What it is / how it works.** Rust kernel unifying **RFC 6962 Merkle audit logs**, capability-based isolation, energy-budget governance and human approval, under five stated system invariants with proof sketches. Framed as an informational right (extending Floridi) to a complete verifiable record of agent actions **on the user's own hardware**, motivated by EU AI Act logging duties.
- **Resource envelope.** **Sub-1.3 ms median action latency; ~400 actions/s; 448-byte inclusion proofs at 10,000 log entries.**
- **Maturity & evidence.** *Demonstrated:* adversarial testing confirms all five invariants; performance figures published. *Claimed:* the invariants' proofs are sketches; I did not verify the implementation exists publicly or read it. Single author (Jing Zhang), no affiliation established, no venue (2026-02-23).
- **Source signal.** `external-scan`.
- **Lens rationale.** Personal-hardware agent kernel with an append-only evidence log and a capability model — the run's exact subject.
- **Dedup.** NEW.
- **Alias flag — flag hard for S5.** This is a working, measured instance of the position S5 is challenging ("a personal OS needs a trusted kernel that spawns agents, mints credentials and evaluates gates"). It is ammunition **both ways**: it shows the kernel is buildable at ~1 ms and 400 ops/s by one person, and it shows it has already been built by one person.

### C4 — Capability-safe language as the enforcement surface (capture checking / effects-for-free)
- **What it is / how it works.** The agent does not call tools; it emits code in a capability-safe language (Scala 3 with capture checking). Capabilities are program variables gating access to effects and resources; the type system tracks them statically, giving fine-grained control and **local purity** — provably side-effect-free sub-computations, which is what prevents leakage while classified data is being processed. The underlying theory (Craig/Potanin/Groves/Aldrich) is that effect bounds follow from **type-checking alone**, with no effect annotations.
- **Resource envelope.** Compile-time; runtime cost ≈ zero. The real cost is the language commitment and the requirement that the model can emit capability-safe code — which is the paper's main empirical claim.
- **Maturity & evidence.** *Demonstrated:* experiments show agents generate capability-safe code with "no significant loss in task performance," and the type system prevents information leakage and malicious side effects. *Claimed:* extensibility of the harness pattern. Authors include **Martin Odersky** — the strongest author provenance in this file. No venue established (2026-03-01, rev. 2026-05-07).
- **Source signal.** `external-scan` (cold leg — PL surface, not security).
- **Lens rationale.** The only positive answer found to Q1's expressiveness-vs-gateability trade-off, and it makes the ceiling *checkable* rather than *mined*.
- **Dedup.** NEW. **Related to #263** (Jurati Decision Contract Language v0.1-dev, `grade:partial`, "bounded deterministic checker/reducer") — same family of idea, different substrate. Flagged, not re-litigated.
- **Alias flag.** Products/active-dev will meet this as **WASI / WIT worlds** and component-model capability imports.

### C5 — Evidential Argumentation System + justification logic (the "claim needs evidence" formalism)
- **What it is / how it works.** Extends Dung's abstract argumentation with an evidence relation: **standard** arguments are acceptable only if they trace back through support to **prima facie** arguments, the only ones valid without support. Yields e-grounded / e-preferred / e-stable extensions. Justification logic supplies the proof-term version: the modality `t:F` means *t is evidence for F*, so evidence is a first-class syntactic object, not an annotation.
- **Resource envelope.** Formal semantics; implementation cost is whatever argumentation engine you choose. Extension computation for Dung-family semantics is generally intractable in the worst case — **I did not verify the specific complexity of the evidential variants** and will not assert it.
- **Maturity & evidence.** *Demonstrated:* nothing empirical; these are semantics papers. Established venues and authors (COMMA 2008; Studia Logica 2011; CUP 2019). Full texts unread.
- **Source signal.** `external-scan` (cold leg — logic/argumentation, entirely outside the theme's security reading).
- **Lens rationale.** It is the exact formal content of "a claim is cheap; a commitment requires evidence."
- **Dedup.** NEW.
- **Alias flag.** S4 is separately tasked with the evidence-commit question and will likely reach the same object via double-entry bookkeeping, LIMS/ELN or git's object model. **Merge, do not double-count.**

### C6 — Declared-kind evidence as a shipped pattern (in-toto `predicateType` · GRADE · CAE/Toulmin)
- **What it is / how it works.** One idea in three unrelated fields. in-toto: a `Statement` binds `subject` (what is being attested) to a `predicate` whose schema is identified by **`predicateType`** — provenance, SBOM, SAST results, review — so an attestation is *typed evidence about a named artifact*. GRADE: evidence kind determines starting certainty (RCT → high, observational → low), with explicit criteria to raise or lower, over four levels. CAE: **claim / argument / evidence** as the notation for a safety case, descended from Toulmin's claim / data / warrant / backing / qualifier / rebuttal.
- **Resource envelope.** in-toto is a spec plus signing; GRADE and CAE are human processes with no compute cost and substantial human cost.
- **Maturity & evidence.** *Demonstrated:* all three are deployed at scale in their own fields — but "deployed" is a doc-claim from spec pages and guideline bodies, not something I measured. wfh-005 already established in-toto's standing.
- **Source signal.** `external-scan`, plus **`dogfood-signal`**: this repo already runs the categorical form as `grade:missing|claimed|partial|proven` with `proven_by` carrying the artifact (D7). The literature's independent convergence on *categorical* grading — see C7 — is corroboration of a choice already made here, and I flag it as dogfood so it is not counted as external demand.
- **Lens rationale.** It is the "declared-kind" clause, already standardised.
- **Dedup.** in-toto is in the wfh-005 base as settled prior art for demand-derived ceilings; **its `predicateType`/`Statement` structure as an evidence-kind mechanism is a distinct reading and is NEW.** GRADE and CAE are new.
- **Alias flag.** S4 will almost certainly reach GRADE, CAE or clinical EDC independently.

### C7 — The negative result on quantified evidence confidence
- **What it is.** Graydon & Holloway (*Safety Science*, 2017) surveyed proposed techniques for quantitatively assessing confidence in assurance arguments and **showed by counterexample that most produce implausible results**, additionally noting no empirical evidence of scalability. The line is still live — a 2026 preprint is analysing scalability of quantitative confidence-assessment methods, and a competing "Assurance 2.0" line claims immunity to the counterexamples.
- **Maturity & evidence.** *Claimed by secondary sources* — I read the abstract-level characterisation and the citing literature, **not** the paper. Peer-reviewed journal, named NASA-adjacent authors; the counterexample result is repeatedly and consistently reported by independent citing works, which is why I carry it.
- **Source signal.** `external-scan` (cold leg).
- **Lens rationale.** It is the only *evidence about evidence-grading* found, and it is negative.
- **Dedup.** NEW.
- **Why it matters here, stated as a finding and not a design:** the literature's repeated failure is at making grades *numeric*, not at making them *kinded*. An ordinal, kind-indexed grade is the form that has survived thirty years of safety-case practice.

### C8 — Sub-boundary granularity enforcement, measured (Granite)
- **What it is / how it works.** Runtime proxy enforcing **step-level** permissions inside a GitHub Actions job, transparently monitoring requests from JavaScript and Composite actions against predefined step-level policies. Motivated by the fact that the job is the permission boundary and all steps in it share one token.
- **Resource envelope.** Proxy-mediated request interception; **I could not establish the measured overhead** — not reported in what I read. Declared unverified.
- **Maturity & evidence.** *Demonstrated:* 500 workflows / ~13k jobs analysed, **46.6% of jobs over-privileged**; 42 over-privileged jobs identified with ~59.8% High/Critical, with proof-of-concept exploits built; 52.7% of jobs protectable by Granite. Named authors, KTH Royal Institute of Technology and Chalmers (2025-12-12).
- **Source signal.** `external-scan`.
- **Lens rationale.** It is the *incumbent-gap* lens applied to the theme's incumbent's own substrate: the granularity at which permissions are declared is coarser than the granularity at which authority is used, and the gap is measured.
- **Dedup.** NEW.
- **Alias flag.** Products/active-dev will meet this as "step-level permissions," an open gh-aw/Actions feature request, or a CI proxy sidecar.

### C9 — Velocity-scaled revocation damage (*The Bureaucracy of Speed*)
- **What it is / how it works.** Defines a Capability Coherence System and constructs a structure-preserving map from MESI cache-coherence states to authorization states under bounded-staleness semantics; a safety theorem bounds unauthorised operations for an **execution-count** strategy at **D ≤ n independent of agent velocity**, versus **O(v·TTL)** for time-bounded strategies.
- **Resource envelope.** Requires per-capability operation counting and re-authorisation at count boundaries — cheap to implement, but it forces a round trip every *n* operations, which is a latency and availability cost the paper's simulation does not price against a real workload.
- **Maturity & evidence.** *Demonstrated:* tick-based discrete-event simulation, three scenarios, 120 runs, zero violations, 120× reduction vs TTL lease; simulation code on GitHub. **Simulation only — no deployment.** Single author, no affiliation established, arXiv cs.MA (2026-03-10). `claimed`.
- **Source signal.** `external-scan`.
- **Lens rationale.** Constraint-inversion lens on credential lifetime: for a fast actor, time-based revocation is the wrong axis.
- **Dedup.** NEW.
- **Alias flag.** Products will meet the same problem as "short-lived credentials / TTL tuning"; adjacent prior art as cache coherence and as PKI revocation latency.

### C10 — The 21-proposal permission-design map (Michael & Roesner)
- **What it is.** A survey of 21 agent-permission proposals with a taxonomy over policy specification (UI-level and internal), **derivation of internal policy from user input**, and runtime enforcement — then five commercial agents measured against it, with named themes and gaps.
- **Resource envelope.** n/a (survey).
- **Maturity & evidence.** *Demonstrated:* the survey and comparison exist. *Not established by me:* the 21 proposals are not enumerated in what I read, the taxonomy's axes are known only at the abstract level, and **I could not confirm whether irreversibility or consequence appears anywhere in it** — a specific gap I would close first with remaining budget.
- **Source signal.** `external-scan` (warm leg — over-privilege/permission-model entry).
- **Lens rationale.** It is the design-space map for exactly the layer the run is deciding whether to build, published 2026-07, by a well-identified academic group.
- **Dedup.** NEW.

**Also surfaced, deliberately not promoted to candidates** (relevant, insufficiently verified, listed so they are not lost): `arXiv:2607.21325` cryptographically verifiable agent authorization · `arXiv:2605.02682` hybrid inspection + TBAC in zero-trust agentic AI · `arXiv:2604.23280` AI Identity: Standards and Gaps · `arXiv:2605.04093` Decision Evidence Maturity Model (fetched; a four-category evidence-sufficiency classification aggregated into five capability levels, 140 synthetic scenarios plus three public incidents, 53.6–100% completeness explicitly labelled by its own author as *"implementation behaviour, not external validation"*, Apache-2.0 tool — I read it and judged the evidence too self-limited to promote, but it is the closest thing to a *grading* scheme for agent decision evidence and S4 may want it) · `arXiv:2603.03515` The Controllability Trap (irreversibility score, workshop position paper, scale unvalidated) · **"PAuth"** with NL-slices and provenance-bound envelopes — appeared only inside a search summary, **I could not establish an arXiv id or authors and am therefore not citing it**; it is a lead for a later pass.

---

## 3. Named failure modes a personal-OS vocabulary would walk into

Each attributed to the work that named it. The first four are the ones I would put in front of the owner.

| # | Failure mode | Named by | Why it bites a personal OS specifically |
|---|---|---|---|
| 1 | **Aggregation / trajectory violation** — a sequence of individually permitted actions violates a system-level invariant | Denning's aggregation & inference problem (1980s, multilevel DB security); re-named as *aggregation inference* by Tallam 2026-05 and as *behavioural containment / trajectory assurance* by Bertino et al. 2026-08 | Six domains plus an always-on voice surface is a machine for generating cross-domain action sequences nobody enumerated. Per-call authorization cannot see it, and forty years have not solved it |
| 2 | **Irreversibility conflict** — once irreversible effects land, the reachable outcome set is permanently reduced and full specification satisfaction is *impossible* | *Revisable by Design* 2026-04 (proved); saga/compensation's known limit (compensation cannot prevent an irreversible send) | An always-on proactive surface acts before the user can revise. The proof says no algorithm recovers this; only the action-space classification does |
| 3 | **Safety undecidability** — you cannot decide, in general, whether a vocabulary ever leaks a right | Harrison, Ruzzo & Ullman 1976 | Kills any "least-privilege by construction" claim that is not explicitly scoped to a decidable fragment |
| 4 | **Escalation-on-failure** — over-privileged tool selection is *amplified by transient tool failures*, and safety alignment does not transfer to least-privilege choice | ToolPrivBench 2026-06/07 | A home-scale personal OS has intermittently failing devices as its normal condition. The failure mode is triggered by ordinary flakiness, not by an attacker |
| 5 | **The abstraction layer as escalation source** — the skill/vocabulary layer meant to *contain* behaviour is itself the primary privilege-escalation surface, worst under incomplete specification, convenience framing and boundary proximity | FORTIS 2026 | This is the direct measured refutation of "give it a nice vocabulary and it will stay inside it" |
| 6 | **Role explosion, and the intractability of the cure** | Vaidya, Atluri & Guo, *TISSEC* 2010 (RMP NP-complete; Edge-RMP, min-noise NP-hard) | Six domains × verbs × entities × areas is precisely where hand-authored roles multiply and automated compression stops being cheap |
| 7 | **Coarse-boundary over-privilege** — the declared boundary is coarser than the used authority | Felt et al., CCS 2011 (~1/3 of Android apps); Granite 2025 (46.6% of Actions jobs) | Any "area" or "domain" boundary in a personal OS will be the job-level boundary again |
| 8 | **Confused deputy** | Hardy 1988 (settled base) | Named for completeness; the voice surface is a classic deputy |
| 9 | **Ambient authority** | the object-capability lineage | The design a home-automation-shaped system converges to by default. **S2's subject — flag** |
| 10 | **TTL revocation damage scales with actor velocity** — O(v·TTL) | *The Bureaucracy of Speed* 2026-03 (`claimed`, simulation) | A local fleet running continuously is the high-velocity case |
| 11 | **Delegation-depth and scope creep; audit evasion via empty context** | AIP 2026-03 (both caught only by chained delegation) | Sub-agents spawning sub-agents is the framing's normal operation |
| 12 | **Delegation + revocation as the structurally missing links** — 19 criteria, no dominating scheme | Chuat et al., EuroS&P 2020 | The honest prior on how much of this is buyable |
| 13 | **Quantified evidence confidence produces implausible results** | Graydon & Holloway, *Safety Science* 2017 | Points at kinded/ordinal grades and away from computed evidence scores |
| 14 | **Approval fatigue / compliance budget** | settled base (NSPW 2008; 2605.24309) | Re-listed only because #4 and #5 both push toward *more* prompts, straight into it |

---

## 4. Surface-coverage report

**Venues and corpora actually reached.** arXiv (`cs.CR`, `cs.SE`, `cs.AI`, `cs.MA`, `cs.CY`, `cs.PL`) by direct abstract-page fetch; ACM DL, SpringerLink, IOS Press, ScienceDirect, Semantic Scholar, ResearchGate and author/institution-hosted PDFs via search; W3C TR space (PROV-DM, PROV-CONSTRAINTS, PROV-SEM) and the in-toto/SLSA spec repos; **Google Patents** (two full patent records read); NCBI/PMC and clinical-guideline bodies for GRADE; Adelard and NASA CertWare for CAE; US Air Force doctrine publications for the safety-critical/two-person lineage. Named venues touched: **PODS 2007 · COMMA 2008 · USENIX Security 2009 · TISSEC 2010 · Studia Logica 2011 · NDSS 2014 · ICFEM 2018 · EuroS&P 2020 · ICLP 2021 · Safety Science 2017 · FSE 2026 (via base) · ICLR 2026 workshop · ACM AI Leadership Summit 2026 · ISO SQL:2011 · RFC 6962**.

**Query program run** (≈24 searches, 16 direct fetches, of which 2 were patent records): HRU safety undecidability · role explosion / role mining NP-hardness / granularity trade-off · macaroons attenuation · delegation revocation hardness and bounded depth (SPKI) · assurance-case confidence quantification (Graydon/Holloway) · provenance semirings and PROV formal semantics · justification logic and evidence logic · irreversibility in planning / dead-ends / sagas / safe exploration · tamper-evident logging and history trees · GRADE evidence levels · type-and-effect systems and capability safety · agent over-privilege benchmarks August 2026 · AGNTCY/Outshift TBAC reference implementation · arXiv cs.CR 2607/2608 agent authorization · workflow-satisfiability complexity 2024–2026 · in-toto predicateType · bitemporal and event-sourcing formal models · patent search on least-privilege derivation and on capability attenuation · database inference/aggregation problem · action ontology / PDDL operators / speech acts · safety-critical command classification and the two-person rule · Toulmin and CAE origins · evidential argumentation semantics · Granite.

**Date range.** Canonical layer 1958–2011 (Toulmin 1958 · HRU 1976 · Denning 1980s · Jensen–Snodgrass 1994 · CAE 1998 · Green/Karvounarakis/Tannen 2007 · Oren & Norman 2008 · Crosby & Wallach 2009 · Vaidya et al. 2010 · van Benthem & Pacuit 2011 · Felt et al. 2011). Middle layer 2014–2021 (Macaroons 2014 · Graydon & Holloway 2017 · Craig et al. 2018 · Artemov & Fitting 2019 · Chuat et al. 2020 · Faber/Morak/Chrpa 2021). Agent layer 2025-12 → **2026-08-03** (newest item fetched: Bertino et al., trajectory assurance).

**What I expected to find and did.** I expected the granularity question to have a formal negative core, and it does, twice over (HRU undecidability; RMP NP-completeness). I expected the delegation/attenuation question to be closed, and it is. I expected agent over-privilege to have kept moving, and it has.

**What I expected to find and did NOT.**
- **Any new WSP complexity result 2024–2026.** None. The line looks quiescent. Recorded as a legible negative: the theoretical ceiling was set roughly a decade ago.
- **Any published treatment stating a capability vocabulary's expressiveness-versus-gateability trade-off as a *theorem*.** Both horns are separately formal (undecidability; NP-hardness) and both are separately measured, but **no work states the trade-off itself as a bound.** That is a legible negative and I searched for it directly.
- **Any confirmation of whether the 21-proposal survey treats irreversibility.** I could not establish it from the abstract-level read; declared unverified.
- **A quantitative evidence-grading scheme that survives scrutiny.** The opposite: a peer-reviewed counterexample result against the whole class.

**Deliberately skipped, with reason.**
- **All full texts.** Every canonical work in §5's second block was verified for existence, authorship, venue, year and topical claim across ≥2 independent indexes; **none was read in full.** Attribution risk low, claim-support risk medium, flagged per item. This is wfh-005's standard and I held it.
- **The complexity of evidential-argumentation extension computation.** Relevant to C5's resource envelope; not established; I declined to guess.
- **Granite's runtime overhead.** Not reported in what I read; declared unverified rather than estimated.
- **Products and repos** — not my surface. S1/S2 own them. Where a find has an obvious product or repo shadow (Biscuit, Trillian, `agntcy/identity-service`, `hipvlady/prizm`, the Revisable-by-Design benchmark repo) I have flagged it as an alias rather than characterised it.
- **Non-English literature.** Unread, as in wfh-005. Standing declared hole.

**Hard stop.** The session's WebSearch budget (200/200) was exhausted before I could run two intended queries: (a) the identity and provenance of the **"PAuth"** work (NL-slices, provenance-bound envelopes) — a probable direct hit on declaration-derived ceilings from natural language, currently uncitable; and (b) a targeted sweep of **SACMAT 2025/2026** proceedings, the one named venue in the theme's own reading-surface list I did not reach by name. Both are cheap follow-ups.

### Cold-leg record (protected spend — this is where the file's best material came from)

The theme reads this surface as **security**. I spent a substantial share of the pass outside that reading, as instructed, and report it explicitly:

- **Programming languages and type theory** — capability safety, type-and-effect systems, capture checking. **Yield: C4**, the only positive answer to Q1's trade-off, and the strongest author provenance in the file.
- **Automated planning and knowledge representation** — PDDL/STRIPS operator structure (name, parameters, precondition, effect), situation calculus, dead-end detection, action reversibility as a decidable property, action ontologies (including corpus-derived ones such as IMAGACT). **Yield: the formal grounding for C1**, plus the observation that a "capability vocabulary" is structurally a *planning operator set* and inherits that field's representational choices whether or not anyone says so. **Dry sub-result:** I searched specifically for a formal treatment of *granularity* in action ontologies and found taxonomy-building and ontology→PDDL translation work, but **no granularity result**. Recorded as dry.
- **Argumentation, justification logic and epistemic logic** — **Yield: C5.** Entirely outside the theme's reading surface and it contains the exact formalism of the framing's headline sentence.
- **Database theory and provenance** — semirings, PROV formal semantics and validity, bitemporal models, event sourcing. **Yield: two of the five clauses in Q4's decomposition.** Note the dry part: I looked for a *formal semantics of event sourcing* as such and found practitioner treatments and the bitemporal-event-calculus line, but **no formal theory of event sourcing per se** — the formal content lives in bitemporal databases and in provenance, not under that name.
- **Safety engineering and evidence-based medicine** — assurance cases, CAE, Toulmin, GRADE, and the Graydon–Holloway negative. **Yield: C6 and C7**, including the file's one genuinely load-bearing negative result.
- **Patent prior art — the standing unspent method hole. Partially spent, not closed.** I read two full patent records:
  - **US11388163B2**, *Least-privilege resource permission management*, **Microsoft Technology Licensing LLC**, inventors Bargury & Malka, filed 2020-02-03, granted 2022-07-12. Claim 1: permission assignments as a graph of identities/permissions/resources, node embeddings to find similar identities, **forecast future resource usage** from comparable identities, set minimum permissions accordingly. **Prediction-derived**, not declaration-derived; not phase-indexed.
  - **US10803166B1**, *Automated determination of application privileges*, **Amazon Technologies Inc**, inventors Terkowitz & Xu, filed 2018-01-03, granted 2020-10-13. Claim 1: run the application in a production-replica test environment with maximum permissions, exercise use cases, observe operations, record the minimal sufficient permission set. **Observation-derived.**
  - Also surfaced, unread: **US6308274** (least privilege via restricted tokens), **US9383740** (control of safety-critical operations — notable because it defines a safety-critical operation by *foreseeably irreversible physical consequence*, the same definition as the two-person-rule doctrine).
  - **Honest report of the instrument's limits:** Google Patents' results pages did not render for WebFetch (JavaScript), so I could only read patents whose numbers I already had. Keyword patent *search* on this surface, via these tools, did not work. **The hole is narrowed, not closed.** What it narrows: both patents I read derive the ceiling from **observation or prediction**, not from a **declaration**, and neither indexes by phase — so wfh-005's residual survives its first two patent contacts. What it does not do: establish an absence. A patent sweep needs an instrument this surface does not have, and that should be recorded as a method finding rather than repeatedly re-attempted.

### Warm leg — last-looked table

| Watchlist entry | Re-check condition | Last looked | Delta found |
|---|---|---|---|
| **Agent over-privilege measurement work** | a new benchmark or replication lands | **2026-08-17 (wfh-007)** — prior 2026-08-01 | **FIRED.** Two benchmarks not in wfh-005's set: **FORTIS** (2605.09163, v3 2026-06-14) and **ToolPrivBench** (2606.20023, v2 2026-07-07), plus **Granite** (2512.11602) as a non-agent measurement anchor at 46.6%. Two new findings beyond "more of the same": over-privilege is worst under **ordinary non-adversarial** conditions, and is **amplified by transient tool failures** |
| **Cisco Outshift / AGNTCY** — task-based line | it publishes a reference implementation | **2026-08-17 (wfh-007)** | **AMBIGUOUS — routed to another surface.** `agntcy/identity-service` exists as OSS with a hosted SaaS, and **CoffeeAgntcy** is published as a multi-agent reference implementation for the AGNTCY ecosystem; AGNTCY is now under the Linux Foundation with 65+ vendors. But I could **not** establish from the literature surface whether the **task-based (TBAC) line specifically** has a reference implementation, as distinct from the identity line. Academic TBAC-for-agents work exists independently (`arXiv:2605.02682`, hybrid inspection + TBAC in zero-trust agentic AI, surfaced not fetched). **S1/S2 should close this** |
| CCS · S&P · USENIX Security · ESORICS · **SACMAT** · arXiv cs.CR (venue walk) | standing | **2026-08-17 (wfh-007)** | Reached all by name except **SACMAT**, which the budget stop prevented. **Declared hole** |

### Theme-revision signal (first-class — for the owner at the triage gate, not acted on in flight)

**1. The theme's literature reading surface is defined as security, and under the personal-OS re-cut that definition is now wrong.** Of this pass's four highest-value returns, **three came from fields the theme's reading-surface block does not name**: programming-language type theory (C4), argumentation/justification logic (C5), and safety-engineering assurance cases (C6/C7). The fourth (C1) came from automated planning. The declared venues — CCS, S&P, USENIX Security, ESORICS, SACMAT, arXiv `cs.CR` — would not have found any of them. If the theme is re-cut, the literature surface should name at least: **planning and action languages (ICAPS, KR, ICLP)** · **database provenance (PODS, TaPP)** · **argumentation and epistemic logic (COMMA, Studia Logica)** · **assurance and safety cases (SAFECOMP, Safety Science)** · **PL and type systems (POPL, OOPSLA, ICFP)**. I raise this as a configuration defect, not a conclusion.

**2. Evidence bearing on the run's proposed grid promotion, reported as evidence and not as a ruling.** Of the four candidate dimensions, **irreversibility and consequence** is the one this surface can speak to, and it says the dimension is **formally characterised, with a published taxonomy and an impossibility result** — not a soft or taste-level axis. **Domain vocabulary** is characterised negatively but firmly: undecidable to verify, NP-hard to minimise, and measured to leak at every granularity anyone has shipped. I found nothing bearing on **the person model** or **always-on and proactivity**; that is a hole in my surface, not evidence of their unimportance.

**3. One position-shaped observation, flagged and not argued.** wfh-005 struck the absence claim on phase-indexed derivation. This pass encountered a second absence-shaped claim in the run's framing — the **evidence-graded commit** as a differentiating primitive — and it does not survive this surface either: it decomposes into five separately-solved primitives, and two 2026 systems (IBCT, PunkGo) have already attempted the fusion with published overheads. **If the theme intends to keep the claim, it must be argued by name against those, exactly as wfh-005 required of the first one.** Routing it to the gate rather than deciding it is the whole of my role here.

---

## 5. `cites:`

**Fetched and read directly this pass** (abstract page or patent record opened; title, authorship, date and claims read verbatim):

```
- type: paper, ref: arXiv:2604.23283, title: "Revisable by Design: A Theory of Streaming LLM Agent Execution",
  author: "Zhai; Li; Wang", year: 2026, surface: literature
- type: paper, ref: arXiv:2603.24775, title: "AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A",
  author: "Prakash", year: 2026, surface: literature
- type: paper, ref: arXiv:2602.20214, title: "Right to History: A Sovereignty Kernel for Verifiable AI Agent Execution",
  author: "Zhang", year: 2026, surface: literature
- type: paper, ref: arXiv:2603.00991, title: "Tracking Capabilities for Safer Agents",
  author: "Odersky; Zhao; Xu; Bracevac; Pham", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.09163, title: "FORTIS: Benchmarking Over-Privilege in Agent Skills",
  author: "Li; Yu; Wang; Yang; Rossi; Dernoncourt; Hu; Yu; Xiao; Zhang; Zhao", year: 2026, surface: literature
- type: paper, ref: arXiv:2606.20023, title: "When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents",
  author: "Yang; Bu; Yi; Wang; Zhou; Dai; Hu; Yang", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.05440, title: "Authorization Propagation in Multi-Agent AI Systems: Identity Governance as Infrastructure",
  author: "Tallam", year: 2026, surface: literature
- type: paper, ref: arXiv:2607.13718, title: "How Agents Ask for Permission: User Permissions for AI Agents, from Interfaces to Enforcement",
  author: "Michael; Roesner", year: 2026, surface: literature
- type: paper, ref: arXiv:2608.01558, title: "Securing Agentic AI: From Per-Action Checks to Trajectory Assurance",
  author: "Lotfi; Karmaker Shanto; Karim; Bertino", venue: "ACM AI Leadership Summit 2026 (Visionary Track)", year: 2026, surface: literature
- type: paper, ref: arXiv:2603.09875, title: "The Bureaucracy of Speed: Structural Equivalence Between Memory Consistency Models and Multi-Agent Authorization Revocation",
  author: "Parakhin", year: 2026, surface: literature
- type: paper, ref: arXiv:2603.03515, title: "The Controllability Trap: A Governance Framework for Military AI Agents",
  author: "Sahoo", venue: "ICLR 2026 Workshop on Agents in the Wild", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.04093, title: "Decision Evidence Maturity Model for Agentic AI: A Property-Level Method Specification",
  author: "Solozobov", year: 2026, surface: literature
- type: paper, ref: arXiv:1906.10775, title: "SoK: Delegation and Revocation, the Missing Links in the Web's Chain of Trust",
  author: "Chuat; Abdou; Sasse; Sprenger; Basin; Perrig", venue: "IEEE EuroS&P 2020", year: 2019, surface: literature
- type: paper, ref: arXiv:2108.05428, title: "Determining Action Reversibility in STRIPS Using Answer Set and Epistemic Logic Programming",
  author: "Faber; Morak; Chrpa", venue: "ICLP 2021", year: 2021, surface: literature
- type: paper, ref: "IOS Press, Frontiers in Artificial Intelligence and Applications 172, pp. 276-284, ISBN 978-1-58603-859-5",
  title: "Semantics for Evidence-Based Argumentation", author: "Oren; Norman",
  venue: "COMMA 2008", year: 2008, surface: literature
- type: patent, ref: "US11388163B2", title: "Least-privilege resource permission management",
  author: "Bargury; Malka", org: "Microsoft Technology Licensing LLC", year: 2022, surface: literature
- type: patent, ref: "US10803166B1", title: "Automated determination of application privileges",
  author: "Terkowitz; Xu", org: "Amazon Technologies Inc", year: 2020, surface: literature
```

**Corroborated across ≥2 independent indexes; full texts NOT read** (existence, authorship, venue, year and topical claim verified; claim-support risk medium):

```
- type: paper, ref: "Communications of the ACM 19(8):461-471", title: "Protection in Operating Systems",
  author: "Harrison; Ruzzo; Ullman", year: 1976, surface: literature
- type: paper, ref: "doi:10.1145/1805974.1805983", title: "The Role Mining Problem: A Formal Perspective",
  author: "Vaidya; Atluri; Guo", venue: "ACM TISSEC 13(3)", year: 2010, surface: literature
- type: paper, ref: "https://theory.stanford.edu/~ataly/Papers/macaroons.pdf",
  title: "Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud",
  author: "Birgisson; Politz; Erlingsson; Taly; Vrable; Lentczner", org: "Google",
  venue: "NDSS 2014", year: 2014, surface: literature
- type: paper, ref: "USENIX Security Symposium 2009", title: "Efficient Data Structures for Tamper-Evident Logging",
  author: "Crosby; Wallach", org: "Rice University", year: 2009, surface: literature
- type: paper, ref: "doi:10.1145/1265530.1265535", title: "Provenance Semirings",
  author: "Green; Karvounarakis; Tannen", org: "University of Pennsylvania", venue: "ACM PODS 2007", year: 2007, surface: literature
- type: paper, ref: "doi:10.1016/j.ssci.2016.08.003",
  title: "An investigation of proposed techniques for quantifying confidence in assurance arguments",
  author: "Graydon; Holloway", venue: "Safety Science", year: 2017, surface: literature
- type: paper, ref: "doi:10.1007/978-3-030-02450-5_14", title: "Capabilities: Effects for Free",
  author: "Craig; Potanin; Groves; Aldrich", venue: "ICFEM 2018", year: 2018, surface: literature
- type: paper, ref: "Studia Logica 99(1-3):61-92", title: "Dynamic Logics of Evidence-Based Beliefs",
  author: "van Benthem; Pacuit", year: 2011, surface: literature
- type: paper, ref: "Cambridge University Press, ISBN 978-1-108-42891-2", title: "Justification Logic: Reasoning with Reasons",
  author: "Artemov; Fitting", org: "Cambridge University Press", year: 2019, surface: literature
- type: paper, ref: arXiv:2512.11602, title: "Granite: Granular Runtime Enforcement for GitHub Actions Permissions",
  author: "Moazen; Ahmadian; Balliu", org: "KTH Royal Institute of Technology", year: 2025, surface: literature
- type: paper, ref: arXiv:2606.15480, title: "A Scalability Analysis of Quantitative Confidence Assessment Methods for Assurance Cases",
  year: 2026, surface: literature
- type: standard, ref: "https://www.w3.org/TR/prov-constraints/", title: "Constraints of the PROV Data Model",
  org: "W3C", surface: literature
- type: standard, ref: "https://www.w3.org/TR/prov-sem/", title: "Semantics of the PROV Data Model",
  author: "Cheney", org: "W3C", surface: literature
- type: standard, ref: "https://github.com/in-toto/attestation/blob/main/spec/predicates/provenance.md",
  title: "in-toto Attestation Framework - Statement, predicateType, and the SLSA Provenance predicate",
  org: "in-toto", surface: literature
- type: standard, ref: "ISO/IEC 9075:2011 (SQL:2011) system-versioned and application-time period tables",
  title: "Bitemporal Conceptual Data Model, standardized as SQL:2011 temporal tables",
  author: "Jensen; Snodgrass", year: 1994, surface: literature
- type: docs, ref: "https://www.adelard.com/asce/cae/", title: "Claims, Arguments, Evidence (CAE) notation",
  author: "Bloomfield", org: "Adelard", year: 1998, surface: literature
- type: docs, ref: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC545647/",
  title: "Systems for grading the quality of evidence and the strength of recommendations I: Critical appraisal of existing approaches",
  org: "GRADE Working Group", year: 2004, surface: literature
- type: standard, ref: "AFI 91-117 / AFI 91-104 (two-person concept; safety-critical operation defined by foreseeably irreversible consequence)",
  title: "US Air Force Instruction - Safety Rules for Nuclear Weapons and the Two-Person Concept",
  org: "US Air Force", surface: literature
```

**Surfaced but NOT opened — do not cite downstream without a fetch:** `arXiv:2607.21325` (cryptographically verifiable agent authorization) · `arXiv:2605.02682` (hybrid inspection + TBAC, zero-trust agentic AI) · `arXiv:2604.23280` (AI Identity: standards and gaps) · `arXiv:2105.03273` (WSP via general-purpose solvers) · `arXiv:1205.0852` / `arXiv:1504.03561` / `arXiv:1512.07019` (WSP parameterized, class-independent, bi-objective — the FPT/W[1] claims in §Q3 rest on consistent secondary summaries, not on these texts) · `arXiv:2409.10665` / `arXiv:2604.00034` (Assurance 2.0 confidence) · **US6308274**, **US9383740** · the "PAuth" work, for which **I could not establish an identifier and am therefore not citing at all**.

---

## Compact return list

| Find | Lens | New/known | Adopt-assemble-build evidence |
|---|---|---|---|
| C1 Revisable-by-Design reversibility taxonomy + impossibility | in | NEW | n/a (literature; benchmark + code exist) |
| C2 AIP / Invocation-Bound Capability Tokens | in | NEW | **yes** — measured overheads, Python+Rust reference impls |
| C3 PunkGo sovereignty kernel | in | NEW | **yes** — latency/throughput/proof-size measured |
| C4 Capability-safe language (capture checking) | in | NEW (related to **#263**) | partial — task-performance measured, no runtime cost |
| C5 Evidential Argumentation System + justification logic | in | NEW | n/a (semantics only) |
| C6 Declared-kind evidence: in-toto `predicateType` · GRADE · CAE/Toulmin | in | in-toto **known** as base, this reading NEW; GRADE/CAE NEW | n/a |
| C7 Graydon–Holloway negative on quantified confidence | in | NEW | n/a |
| C8 Granite step-level enforcement (46.6% over-privileged) | in | NEW | partial — overhead **unverified** |
| C9 Velocity-scaled revocation damage (D ≤ n vs O(v·TTL)) | in | NEW | no — simulation only |
| C10 Michael & Roesner 21-proposal permission map | in | NEW | n/a (survey) |

**Flags for the leader.**
1. **S4 overlap is guaranteed, not possible** — S4's job (b) is the same evidence-commit question. C5/C6 and S4's double-entry / git-object-model / LIMS finds are one cluster. **Merge; wfh-005 collapsed ~15 apparent hits to three clusters and this is the same shape.**
2. **S5 ammunition, both directions** — C3 (PunkGo) is a built, measured instance of the kernel position S5 is challenging.
3. **S1/S2 routing** — the AGNTCY task-based re-check is ambiguous from this surface and needs a repo/product read.
4. **Two absence claims, one pattern** — the evidence-graded-commit differentiator does not survive this surface as stated; routed to the gate, not decided here.
5. **Patent hole narrowed, not closed, and the instrument is the blocker** — Google Patents does not render for WebFetch, so keyword patent search is unavailable on this surface. Recommend recording that as a method finding rather than re-tasking a scout to retry it.
