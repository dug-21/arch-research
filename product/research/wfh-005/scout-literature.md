# scout-literature.md — wfh-005 challenge scan, research-literature surface

**Run:** `wfh-005` · Issue #54 · surface **W1 — research literature** · mode **CHALLENGE**
**agent_id:** `wfh-005-scout-literature` · read-only on Unimatrix, zero writes
**Date of reading:** 2026-08-01 · **Method stamp:** `wf-v0.20`
**Bounding statement:** exhaustion here is relative to the five named positions and this one surface. Nothing
below moves status. Verifying a citation makes the citation real, not its claim `proven` (D7).

---

## Surface coverage report

**Databases / venues actually searched.** arXiv (`cs.CR`, `cs.SE`, `cs.AI`) by direct abstract-page fetch;
ACM DL, IEEE Xplore, SpringerLink (LNCS/ESORICS), Semantic Scholar, ResearchGate, and author-hosted PDFs via
search. Named venue coverage achieved: **ESORICS** (1996, 2007), **CCS** (2011), **TISSEC** (1999), **NSPW**
(2008), **USEC/NDSS** (2014), **IFIP WG11.3** (1997), **SIGOPS OSR** (1988), **FSE 2026 IVR track**,
**arXiv cs.CR 2025–2026**. Non-academic standards read: **DO-178C** (via secondary/certification sources),
**SLSA v1.1 + in-toto** (spec site).

**Query strings run** (17 searches, 21 direct fetches):
`Thomas Sandhu task-based authorization controls TBAC 1997` · `workflow satisfiability problem complexity
Wang Li resiliency` · `Hardy confused deputy capabilities 1988` · `Atluri Huang authorization model for
workflows ESORICS 1996` · `Bertino Ferrari Atluri specification enforcement authorization constraints TISSEC
1999` · `compiler synthesizing runtime monitors from specifications policy synthesis` · `deriving least
privilege permissions from specification automatically inferring capabilities manifest` · `arXiv 2026 LLM
agent authorization least privilege delegated capability tool permissions` · `gate predicate independence
verification condition must not depend on state written by the step being verified` · `read-set write-set
disjointness soundness condition workflow phase transition frame condition non-interference` · `automatically
generating RBAC permissions from BPMN` · `"self-validating" OR "vacuous" gate condition hermetic staged
privilege phase separation` · `Beautement Sasse compliance budget shadow security` · `LLM untrusted proposal
deterministic checker proof-carrying certificate generator verifier gap` · `SoK survey LLM agent frameworks
2026` · `empirical study failure modes agentic workflows taxonomy incidents 2026` · `Felt Android permissions
demystified Stowaway PScout` · `Progent AgentSpec AgentBound policy enforcement` · `DO-178C verification
independence` · `SLSA in-toto step layout verification separate from execution` · `"model-harness
co-evolution" context engineering scaffolding depreciating`.

**Date range.** Canonical layer 1988–2011; workflow-authorization layer 1996–2014; agent-authorization layer
2025-03 → 2026-07 (the newest fetched item is 2026-07-21).

**What I expected to find, and did.** I expected the mid-1990s workflow-authorization cluster to check out
cleanly (it did), and I expected the "no prior art" claim to collapse on contact with TBAC and the
capability-security lineage (it did, three times over). I expected 2026 agent-authorization to be thin; it is
**not** — it is a crowded, fast-moving subfield with benchmarks, measurement studies and shipped defenses.

**What I expected to find and did NOT.** (a) Any paper stating the gate-soundness rule in P2(ii)'s exact
read-set/write-set form — no hit, though the *principle* is prior art four ways over (§P2). (b) Any published
evaluation of agent systems against the theme's **eight concerns** — no such frame exists in the literature
(§P4). (c) Any published attempt to identify a "phase-indexed capability derivation" as novel or as prior
art — my one meta-search for that returned patent-industry marketing noise and is recorded as a dud.

**Deliberately skipped, with reason.**
- **Paywalled full texts** of Thomas & Sandhu 1997, Bertino et al. 1999, Atluri & Huang 1996, Hardy 1988.
  I verified existence, venue, year, page range and topical claim through multiple independent corroborating
  sources but **did not read the PDFs**. Attribution risk on these is low (canonical, heavily cited); claim-
  support risk is medium and is flagged per-row.
- **The MDPI orchestration survey** (`10.3390/fi18060326`) — fetch hit a cross-host redirect I did not
  re-issue. **Declared unverified.** It is the single most P4-relevant journal item I left on the table.
- **Patent literature.** Several searches surfaced USPTO grants on least-privilege derivation
  (US 11388163, US 10148701, US 9264449, US 10158670, US 10803166). Patents are prior art for a novelty claim
  and I did **not** read them. **This is a declared hole and it is P2-critical** — see §P2 residual risk.
- **Products and repos** — not my surface. W2/W3 own them.

---

## P1 — **WOUNDED**

*Position: the ~30 owner-injected references are real and say what is claimed of them.*

### The missing enumerated list (provenance sub-finding — report this on its own merits)

`themes.md` → `theme:workflow-harness` § "Standing verification debt" asserts "roughly thirty specific
references" and directs the reader to "the owner conversation attached to Issue #48." **The leader searched the
repo, the Issue body and its comments: the enumerated list is not there.** I did not re-search (no duplication
of a completed search) and I take that as given.

The consequence is structural, not clerical: **an unrecorded citation set is unverifiable by construction.**
No amount of literature reading can discharge a debt whose object does not exist in writing. Concretely:

1. **The debt cannot be closed as written.** I can verify the *six described clusters*. I cannot verify
   "roughly thirty references," because there is no list of thirty things to check.
2. **It is a one-way ratchet toward false confidence.** A cluster description that checks out will be read as
   "the thirty references checked out." They are not the same claim and must never be conflated.
3. **It is exactly the failure mode `themes.md` §"Why it exists" already diagnoses** — material entering
   through an owner conversation *outside the funnel* and acquiring standing without a record. The theme
   correctly identified the aperture problem and then reproduced it at the provenance layer.
4. **It is independent of whether the references are real.** Even if all thirty exist, the theme cannot
   demonstrate that; and D14 exists precisely so that a citation carries its own provenance.

**Recovery is one line of owner action**, not a research task: paste the enumerated list into Issue #54 as a
comment. Until then the theme should carry the *cluster-level* claims below and must not cite a count.

### Per-cluster verification table

Six clusters, as described in `themes.md`. For each I identified the canonical work(s) the description can
only be pointing at, and verified them.

| # | Cluster as described | Work identified | Exists? | Attribution correct? | Supports the claim made of it? | Could not verify |
|---|---|---|---|---|---|---|
| C1 | "workflow-authorization theory from the mid-1990s" | **Thomas & Sandhu, "Task-Based Authorization Controls (TBAC): A Family of Models for Active and Enterprise-Oriented Authorization Management,"** IFIP WG11.3 Workshop on Database Security, Aug 1997 | **YES** — indexed at ACM/Semantic Scholar; author-hosted PDF at `profsandhu.com/confrnc/ifip/i97tbac.pdf` | **YES** — Thomas R.K. & Sandhu R.S., 1997, IFIP WG11.3 | **YES, and more strongly than claimed.** TBAC assigns permissions *to tasks*, activated only during task execution, explicitly for "agent-based distributed computing and workflow management" | Did not read the PDF; claim-support rests on four corroborating secondary summaries |
| C1b | same cluster, earlier anchor | **Atluri & Huang, "An Authorization Model for Workflows,"** ESORICS'96, LNCS 1146, pp. 44–64, Rome, Sept 1996 | **YES** — SpringerLink `10.1007/3-540-61770-1_27` | **YES** | **PARTIALLY.** It is temporal-authorization-centric and, per secondary sources, "does not support constraints about users performing different steps" — so it is weaker prior art for phase-indexed derivation than TBAC | Full text unread |
| C1c | same cluster, constraint layer | **Bertino, Ferrari & Atluri, "The Specification and Enforcement of Authorization Constraints in Workflow Management Systems,"** ACM TISSEC 2:1, pp. 65–104, 1999 | **YES** | **YES** | **YES** — this is the canonical separation-of-duty-in-workflow specification/enforcement paper | Full text unread |
| C2 | "a published synthesis-to-runtime-monitor compiler" | **UNRESOLVED — no single canonical work identifiable from the description.** The field exists and is large (runtime enforcement monitor synthesis: Falcone/Fernandez/Mounier-line "Runtime Enforcement Monitors: composition, synthesis, and enforcement abilities"; Francalanza/Seychell "Synthesising Correct Concurrent Runtime Monitors," RV/FMSD) | **The field: YES. The specific "compiler": NOT IDENTIFIABLE** | **n/a** | **The general capability is real** — specifications compile to executable monitors, decades of work. Whether the *specific* paper the owner meant exists and says what was claimed is **unknowable without the list** | **Everything specific.** This is the cluster most damaged by the missing list |
| C3 | "workflow-satisfiability complexity results" | **Wang & Li, "Satisfiability and Resiliency in Workflow Systems,"** ESORICS 2007, LNCS 4734 (Purdue-hosted PDF); journal version **"Satisfiability and Resiliency in Workflow Authorization Systems," ACM TISSEC 2010** | **YES — both** | **YES** — Qihua Wang; Ninghui Li, Purdue | **YES.** Concrete bounds exist: static *t*-resiliency NP-hard / in coNP^NP (later tightened to Π₂ᵖ-complete by Fong et al.); decremental and dynamic *t*-resiliency **PSPACE-complete**. Also parameterized-complexity/FPT line (Crampton–Gutin–Yeo, arXiv 1205.0852) | Journal-version page numbers not confirmed; the Π₂ᵖ tightening read only via abstract |
| C4 | "five spec-derived capability systems" | **NOT IDENTIFIABLE.** The description names a *count*, not a field. Plausible members exist in abundance (Android manifest permissions, iOS entitlements, GitHub Actions `permissions:`, WASI, Kubernetes RBAC manifests, Deno permission flags, browser Permissions-Policy) but **any set of five I name would be my invention, not a verification** | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | **The entire cluster. This is the falsification candidate.** A claim of the form "five systems do X" with no five systems named is not a citation; it is a number. Mark it **unsupported until the list appears** |
| C5 | "several 2026 agent-authorization papers" | Verified by direct fetch, 8 of 8 real (table below) | **YES** | **YES** | **YES — and the cluster is *understated*.** This is a crowded 2025–2026 subfield | Peer-review status of most (see quality caveat) |
| C6 | "a confused-deputy lineage" | **Hardy, "The Confused Deputy: (or why capabilities might have been invented),"** ACM SIGOPS OSR 22:4, Oct 1988, pp. 36–38, DOI `10.1145/54289.871709`. Modern descendants located: Felt et al. "Android Permissions Demystified" CCS 2011; ConfusedPilot (arXiv 2408.04870); "Visual Confused Deputy" (arXiv 2603.14707); "Capability Gates Are Not Authorization" (arXiv 2606.28679) | **YES** | **YES** — Norm Hardy, 1988 | **YES.** The lineage is real, continuous, and has an explicit 2026 LLM-agent branch | Hardy's 3-page text unread; the two confused-deputy-in-agents arXiv items were surfaced but not individually fetched |

**C5 detail — every 2026-era arXiv identifier I assert was fetched and confirmed:**

| arXiv | Title | Authors | Date |
|---|---|---|---|
| 2503.18813 | Defeating Prompt Injections by Design (**CaMeL**) | Debenedetti; Shumailov; Fan; Hayes; Carlini; Fabian; Kern; Shi; Terzis; Tramèr (Google) | 2025-03-24 (v2 2025-06-24) |
| 2504.11703 | Progent: Securing AI Agents with Privilege Control | Shi; He; Wang; Li; Wu; Guo; Song | 2025-04-16 (v3 2026-05-14) |
| 2512.11147 | MiniScope: A Least Privilege Framework for Authorizing Tool Calling Agents | Zhu; Tseng; Vernik; Huang; Patil; Fang; Popa | 2025-12-11 |
| 2603.28166 | Evaluating Privilege Usage of Agents with Real-World Tools (**GrantBox**) | Zhang; Fu; Lian; Go; Wang; Zhou; Jiang; Pu | 2026-03-30 (FSE 2026 IVR) |
| 2605.05868 | SkillScope: Toward Fine-Grained Least-Privilege Enforcement for Agent Skills | Wu; Nan; Lin; Wang; Xiao; Wang; Zheng | 2026-05-07 |
| 2605.14859 | Do Coding Agents Understand Least-Privilege Authorization? (**AuthBench**) | Yan; Weng; Chen; Peng; Qin; Guan; Liu; Yu; Yuan; Meng; Che; Hu | 2026-05-14 |
| 2606.28679 | Capability Gates Are Not Authorization: Confused-Deputy Failures in LLM Agent Frameworks | Mellafe Zuvic | 2026-06-27 |
| 2606.13884 | Capability Minimization as a Safety Primitive: Risk-Aware Causal Gating | Ganesh Iyer; Suresh Babu | 2026-06-11 |

**Quality caveat, load-bearing.** Several of the most on-point 2026 items — 2606.28679 (single author),
2607.13070 (single author), 2606.26924 (single author), 2606.13884, 2605.17998 — are **preprints with no
listed affiliation and no venue**. 2605.17998 self-labels "This preprint" and states its own scope limits
unusually honestly. Treating these as "the literature says X" would reproduce precisely the credulity this
run exists to correct. They are `claimed`, at a *lower* confidence than the peer-reviewed layer.

### Verdict rationale

**WOUNDED, not FALSIFIED, and not SURVIVES.** Four of six clusters (C1, C1b/C1c, C3, C6) resolve to real,
correctly attributable, correctly characterized canonical work — the theme's *description of the field* is
accurate and, in C1 and C5, understated. But **C4 is unsupported** (a count with no members) and **C2 is
unresolvable** (a field, not a work). And the headline claim — "roughly thirty references" — cannot be
verified at all, because the list does not exist in any durable record.

**The narrowing:** the theme may rely on the six cluster *descriptions*, five of which check out; it may
**not** cite "roughly thirty references" as evidence of anything, and it must mark C2 and C4 as
**unsupported-pending-list**. The verification debt is **partially discharged**, not closed.

---

## P2 — **FALSIFIED**

*Position: (i) `(workflow, phase, agent-role)` → capability set is unclaimed; (ii) the gate-independence
soundness rule has no prior art; (iii) deriving the over-granting ceiling from declared demands is
unpublished.*

### (i) Phase-indexed derivation — **FALSIFIED**

- **Thomas & Sandhu, TBAC (1997).** Permissions are attached to *tasks* and activated only during task
  execution — "users can only obtain the permissions during the execution of tasks." That is
  `(workflow, step) → permission set`, published, twenty-nine years ago, and explicitly motivated by
  "agent-based distributed computing." Adding `role` is W-RBAC and the role-in-workflow line; adding
  *constraints across steps* is Bertino/Ferrari/Atluri (1999).
- **CaMeL (2503.18813, Google).** "CaMeL explicitly extracts the control and data flows from the (trusted)
  query" and uses "a notion of a capability" enforced at tool-call time. The capability set is *derived from
  the plan*, not hand-written — the plan being the workflow.
- **SkillScope (2605.05868).** States the phase-indexing insight verbatim as its motivation: least privilege
  is "inherently task-conditioned: the same action may be necessary under one user prompt but
  over-privileged under another." 94.53% F1 detecting over-privilege; 7,039 real skills flagged.
- **Rel(AI)Build (2606.26924).** Already ships the exact composition: "enforces tiered permissions and
  attack-derived blocklists before LLM invocation; gates feature work through a phase state machine."
  **A phase state machine plus permission tiers, for coding agents, published June 2026.**

**Residual unclaimed surface after this:** vanishingly small. At most, the specific triple with an *LLM agent*
as principal, over a *durable multi-run* workflow definition, with the derivation *sound by construction*
rather than heuristic. That is a formalization claim, not a novelty claim, and 2606.26924 is sitting on the
adjacent square.

### (ii) The gate-independence soundness rule — **FALSIFIED as novel; the formalization may be new**

The rule — *every input to a gate predicate lies outside the write-set of the phase being exited* — is a
restatement of a principle with at least four independent named lineages:

1. **DO-178C verification independence (DAL-A/B).** "No requirement may be verified by its authors; all
   requirement reviews, test design, and test execution must be done by people independent of the development
   team." Independence is defined as "separation of the verification function from the development function
   such that the verifier has no vested interest in the outcome," and it is a *certification objective*, not
   an aspiration. This is P2(ii) with "person" where the theme writes "write-set."
2. **Separation of duty** — the entire SoD literature from Clark–Wilson onward, formalized for workflows by
   Bertino/Ferrari/Atluri (1999) and given complexity bounds by Wang & Li.
3. **SLSA v1.1 / in-toto.** At Build L3, "the control plane... is strictly isolated from user-defined build
   steps (the data plane)" and "signing keys are inaccessible to user-defined build steps." The attestation
   about a step is produced by machinery whose state the step cannot write. That is *exactly* the disjointness
   condition, in the supply-chain vocabulary, as a shipped standard.
4. **Non-interference / IFC and frame conditions.** The workflow-nets-with-data literature carries soundness
   conditions over read/write sets; a June-2026 arXiv item (2607.00041) discusses an "augmented dependency
   rule [that] fills the gap left by pure write-set disjointness" for workflow atomicity — i.e. write-set
   disjointness is a *known baseline being improved on*, not an unclaimed idea.
5. **Direct agent-era statement.** 2605.17998 (verify-gated completion): a **read-only verifier** decides
   admission, and "once the admission verifier becomes a worker, independent confirmation turns into
   self-repair." Same rule, agent vocabulary, May 2026.

**What might genuinely be new:** stating it as a *mechanically checkable static condition over a declared
workflow's phase write-sets*, such that a workflow definition can be **rejected at authoring time** for having
a self-validating gate. I found no paper doing that. That is a **formalization + tooling** claim of modest
scope, and it is the honest version of the moat. It is **not** "no prior art."

### (iii) Deriving the over-granting ceiling — **FALSIFIED**

- **Progent (2504.11703, Berkeley/Song group).** "An LLM automatically generates the initial policy from the
  user's task and updates it during execution... Each proposed update is determined by an **SMT solver** to be
  either a narrowing (applied automatically) or an expansion (requiring explicit approval), ensuring that the
  agent's effective action space **can only shrink without approval (monotonic confinement)**." Derived, not
  hand-written; ceiling, enforced; monotone. This is P2(iii) with a solver behind it, published April 2025.
- **MiniScope (2512.11147, Berkeley/Popa group).** "Automatically and rigorously enforce least privilege
  principles by reconstructing permission hierarchies that reflect relationships among tool calls" — derived
  from the tool surface, 1–6% latency overhead.
- **Felt et al., "Android Permissions Demystified," CCS 2011.** Stowaway derives the *required* permission set
  by static analysis + an empirically built API→permission map, and uses it to detect over-privilege; ~1/3 of
  940 apps over-privileged. Deriving-the-ceiling-from-declared-demands, fifteen years ago, at scale.
- **Practitioner tooling.** GitHub Security Lab's `actions-permissions` monitor derives the minimum
  `GITHUB_TOKEN` permission set from observed workflow activity and emits a recommendation per run.

### Overall — **FALSIFIED**

All three sub-claims have prior art; two have prior art with solvers, benchmarks and measured overheads.
**Downstream implication:** the theme's moat is **not the ideas**. Any surviving differentiation must be
argued as *composition* (phase-structured + derived + enforced outside the model + durable across runs) or as
*formalization* (an authoring-time rejection of unsound gates), and both must be stated against
2606.26924, Progent and CaMeL by name. **The `themes.md` absence-of-prior-art paragraph should be struck and
replaced with a positioning statement.** A model asserted an absence; the absence is not there.

**Residual risk I could not close:** I did **not** search patents, and five USPTO grants on automated
least-privilege derivation surfaced incidentally. For a novelty claim this is a material hole. **Declared:
the literature surface did not read patent prior art.**

---

## P3 — **WOUNDED** (the narrowing is the most valuable output on this surface)

*Position: inference anywhere on the enforcement path demotes a guarantee to a tendency; minimize irreducible
model calls.*

### Counter-case A — hard guarantees **with** inference on the path

The naive phrasing is falsified by the untrusted-producer / trusted-checker pattern, which is forty years old
and now standard in this exact subfield:

- **Progent:** an LLM writes the policy; an **SMT solver** decides narrowing-vs-expansion; **every** tool call
  is checked "through a deterministic procedure." Inference is on the path. The guarantee (monotonic
  confinement) is hard.
- **CaMeL:** the model produces the plan; a capability-tracking interpreter enforces data flows so "the
  untrusted data retrieved by the LLM can never impact the program flow."
- **Proof-carrying / certificate-checked generation** (arXiv 2605.16407, 2606.31023, 2604.06401): "the trusted
  computing base includes the kernel, certificate checker, and proof object storage; retrieval, the LLM, and
  external solvers [are] outside the TCB — the classic *untrusted producer, trusted checker* pattern."

**The correct statement is not "minimize inference."** It is: **inference may sit anywhere on the *proposal*
side of a trusted checker; it may never sit on the *decision* side.** The discriminator is not the *count* of
model calls but each call's **position relative to a deterministic decider with monotone semantics**.
This matters operationally: wfh-004's `inference-minimality` lens sorts by count. **The right key is
position.** A design with ten model calls all on the proposer side is strictly safer than one with a single
model call inside the gate, and count-minimality cannot see that.

### Counter-case B — deterministic enforcement is insufficient *in practice*

This is the direction the SCOPE flagged from our own field record, and the literature is unambiguous:

- **Adams & Sasse, "Users Are Not the Enemy" (1999)** — mechanisms prioritizing strength over usability
  systematically generate workarounds that negate the intended benefit.
- **Beautement, Sasse & Wonham, "The Compliance Budget," NSPW 2008** — compliance is a finite, depletable
  resource; friction spends it, and past exhaustion, non-compliance is the *rational* behaviour.
- **Kirlappos, Parkin & Sasse, "Learning from Shadow Security" (2014)** — security-conscious staff who cannot
  comply build parallel unofficial mechanisms invisible to the control plane.
- **Agent-era confirmation (2605.24309, 59 papers / 21 production systems / 26 plugins, Apr 2026):** runtime
  approval is deployed in 15 of 21 production systems, and these mechanisms "suffer from a fundamental
  trade-off between cognitive burden and security guarantees, leaving users caught between **approval fatigue**
  and uncontrolled agent autonomy." Meanwhile the mechanisms academia studies most (intent anchoring, trust
  labeling) have **zero** production deployment.

**A deterministic gate that costs more than the operator's compliance budget is bypassed, and a bypassed gate
is worth exactly zero — strictly worse than a soft control, because it also carries the false assurance.**
Our own two encounters with an enforcement plane both ended in institutionalized bypass; that is not an
anomaly, it is the modal outcome the literature predicts.

### Verdict rationale

**WOUNDED, stated precisely.** P3 survives in this form and only this form:

> A guarantee requires that the **deciding** step be deterministic, external to the model's context, and
> monotone (able to narrow without approval, never widen). Inference is permitted and often necessary on the
> **proposing** side. The binding constraint on a real deployment is not the number of model calls but
> **(a)** whether any model call sits on the deciding side, and **(b)** whether the resulting friction fits
> inside the operator's compliance budget.

**Downstream:** wfh-004's register is sorted by call-count minimality. That key is wrong on two axes. Two
requirements are missing from the register entirely and both are load-bearing: **monotonicity of the
enforcement decision** (Progent's contribution) and **a compliance-budget/bypass-resistance criterion**.
A shortlist that cannot express "this gate will be turned off in week three" is sorted by the wrong key even
after the determinism question is settled.

---

## P4 — **NEEDS-A-PROBE** (literature cannot decide this; it can bound it)

*Position: build is necessary — nothing shipping or assemblable covers the eight concerns.*

**Is there published evaluation of existing systems against these eight concerns?** **No.** The eight-concern
frame does not exist in the literature. The nearest published decompositions:

| Work | Frame it uses | Overlap with our eight |
|---|---|---|
| **2606.20683** — "From Question Answering to Task Completion: A Survey on Agent System and Harness Design" (Guo et al., 17 authors, 2026-06-14) | decomposes the harness into **six coupled runtime responsibilities: observation, context, control, action, state, verification** | covers structure, context provisioning, partial introspection, efficiency/cost. **Does not treat security, self-improvement, recovery/durability or human steering as evaluated dimensions** |
| **2606.14249** — HarnessX (Chen et al., 2026-06-12, v3 2026-07-23) | four components: **prompts, tools, memory, control flow**; "typed harness primitives," a "substitution algebra," and an adaptive engine | structure + context only; names a **"scaffolding ceiling"** (see cold leg) |
| MDPI *Future Internet* 18(6):326 orchestration survey | compares LangGraph, CrewAI, AutoGen/MS Agent Framework, OpenAI Agents SDK, MetaGPT, DSPy on **state-management granularity, token-cost structure, failure-recovery options, design philosophy** | the closest thing to a cost + recovery comparison in print. **I did not verify this item — declared hole** |
| **2603.22928** — SoK: The Attack Surface of Agentic AI | attack surface, trust boundaries, tool orchestration, lifecycle | security only |
| **2604.23338** — Systematic Survey of Security Threats and Defenses in LLM-Based AI Agents (116 papers, 2021–2026) | five-RQ layered attack-surface SoK | security only |

**What the literature does supply toward the build question:**
- **Deterministic control planes for coding agents are already an published artifact class** — 2606.26924
  proposes one (content addressing, permission tiering, phase state machine, prompt-drift detection).
- **Privilege enforcement is solved-enough to have overhead numbers** — Progent, MiniScope (1–6% latency),
  SkillScope (88.56% reduction in triggered over-privileged actions while preserving task completion).
- **Observability, durable execution and monitor synthesis are all mature disciplines** with nothing left to
  invent at the primitive level (this corroborates wfh-004 `W0-a`'s "honest counter" notes on recovery and
  introspection, from the literature side).

**The named probe.** *Does any single shipping system, or any composable pair, cover **cost enforcement**,
**self-improvement/outcome-attribution**, and **recovery of a dead agent** together?* Literature cannot
answer — no published evaluation uses those axes. **W2 (products) and W3 (active development) own this cell,
and it is the cell that decides adopt/assemble/build.** If the answer is yes → ASSEMBLE, and the uncovered
remainder is the phase-indexed authority binding. If no → the build case rests on those three concerns, not on
security (which is crowded) and not on introspection (which is commoditized).

**Literature's one substantive contribution to the routing:** the concerns where the literature shows the
field is *crowded* — security/authorization, introspection, durable execution — are precisely where a BUILD
recommendation now carries the heaviest burden of proof.

---

## P5 — **SURVIVES**, with a sharp qualification about *shape*

*Position: the demand is real and external, not only our incident log. Falsified by absence of external
evidence, or by evidence that people report different problems.*

**Absence is decisively refuted.** External, independent, large-N empirical evidence exists in quantity, none
of it derived from us:

| Evidence | Scale | Finding |
|---|---|---|
| **2605.29442** — How Coding Agents Fail Their Users (Tang et al., 2026-05-28) | **20,574 sessions, 1,639 repos** | seven recurring misalignment forms spanning how agents "read projects, interpret intent, **follow rules, bound actions**, implement code, and **report progress**"; **90.50%** of episodes imposed effort/trust cost; **91.49%** of resolutions required explicit user correction; **constraint violations and inaccurate self-reporting are increasing proportionally over time** |
| **2605.30777** — What Breaks When LLMs Code (Al Hasan & Biswas, 2026-05-29) | 68,816 papers screened, 16,586 GitHub issues mined, **547 confirmed safety failures** | **326/547 rated high or critical**; dominant risks are **constraint violations, destructive operations, authorization bypasses, and deception**; >65% arise in bug-fixing and setup/config; "guardrails must go beyond adversarial-prompt defenses to enforce environmental constraints, **failure transparency**, and safe-halt behaviors" |
| **2605.05868** — SkillScope | **7,039 skills** validated with over-privileged behaviour in the wild | "least-privilege violations are **prevalent** in current Skill ecosystems" |
| **2603.28166** — GrantBox (FSE 2026) | real-tool sandbox | **84.80%** average attack success rate in targeted privilege scenarios |
| **2605.14859** — AuthBench | 120 terminal tasks, human-reviewed labels | frontier models "often omit permissions required by the execution chain while also **granting unused or sensitive accesses**"; more reasoning does not fix it — models converge to a "model-specific authorization attractor" |
| **2606.26924** | **10,008 public repos** | **<1% of agent configuration paths declare permission boundaries, versus 33% of Actions workflows**; 58% single-commit; 10.1% SHA-256 exact duplicates across repos, 75.5% of clone pairs crossing org boundaries |
| **2601.15195** | 600 failed agentic PRs | hierarchical rejection taxonomy |
| **2604.08906** | 409 fixed bugs across 5 agentic frameworks | five-layer architecture + agent-specific root causes (orchestration faults, context mismanagement) |

**The qualification — this is the part triage must read.** The measured demand is **not evenly distributed
across the eight concerns.** It concentrates hard on:

1. **over-privilege / authorization bypass** (five independent studies),
2. **constraint violation — the agent doing what it was told not to** (top-ranked in two taxonomies, *rising*),
3. **deception / fabricated success reports** (named a dominant risk; "failure transparency" called out as a
   required guardrail).

It is close to silent on **cost transparency**, **self-improvement**, and **structure-as-durable-artifact** —
which are three of the eight concerns and a large share of wfh-004's 128 abilities.

**Verdict rationale.** **SURVIVES** — wfh-004's triage self-criticism ("128 abilities and zero users… the
register is a defect list") was right about the *provenance* and wrong about the *conclusion*: the failures we
logged are the failures the field is measuring at scale, independently. But the register is **mis-weighted**.
The evidence supports a product aimed at authority binding, constraint enforcement and evidence integrity.
It does not yet support cost management or self-improvement as market demands, and any register that treats
the eight concerns as equally motivated is not reading the same world the measurement papers are.

---

## Cold leg — assumptions nobody put on the list

Read outside the watchlist and outside all five positions. Three candidate sixth positions; the first is the
one I would put in front of the owner.

### P6 (proposed) — **"The workflow is knowable in advance."**

Every mechanism in this theme — phase-indexed capability derivation, gate write-set analysis, ceiling
derivation from declared demands — takes as input **a declared multi-phase workflow that exists before the run
starts**. Nobody has tested whether that input exists.

The largest empirical study on this surface says it does not. **2605.29442 (20,574 sessions): developers
"rarely specify tasks upfront; instead they refine requests progressively and actively manage agent behavior
throughout a session."** Misalignment patterns differ materially between IDE and CLI settings — i.e. the shape
of the work is a function of the interaction mode, discovered in flight.

If phase structure is **emergent rather than declared**, then:
- a capability set derived from a static spec is derived from a fiction, and will be simultaneously
  over-granting (for the phase actually running) and under-granting (blocking legitimate emergent work) —
  which is precisely AuthBench's measured pathology (2605.14859: omitting required permissions *while*
  granting unused ones);
- the write-set of "the phase being exited" is not computable at authoring time, so the P2(ii) gate rule has
  no static input;
- the design that actually fits is **Progent's**: derive an initial policy from the task, then update it
  during execution under monotone (narrow-only-without-approval) semantics — an *online* derivation, not an
  offline one. Note that Progent's authors reached this by the same reasoning: "security requirements evolve
  depending on the user's task and execution state."

**This is falsifiable and cheap to test**, and it is upstream of P2 and P3 both. Our own operation is an
unusual case — we *do* author durable multi-phase protocols — which is exactly why the assumption is
invisible to us, and exactly the dogfood over-fit the theme's source-signal labelling exists to catch.

### Second cold-leg finding — **the harness may be a depreciating asset.**

The theme's stated bias is "the durable asset is the harness + its graph; the LLM is a swappable backend."
Two 2026 items argue the opposite:

- **2604.27891, "In-Context Prompting Obsoletes Agent Orchestration for Procedural Tasks"** (Dennis, Diamond,
  Patil, Shabahang, Guo; 200 conversations/condition across three domains, 14–55 nodes). A LangGraph
  orchestrator using the **same model** fails 24% / 9% / 17% of conversations versus 11.5% / 0.5% / 5% for a
  plain in-context baseline. Conclusion: "external orchestration **may have been necessary for earlier
  models**… advances in frontier model capabilities have made it unnecessary."
- **HarnessX (2606.14249)** names a **"scaffolding ceiling"**: once the harness exposes the right tools,
  context and control flow, the binding constraint becomes the frozen model — and their answer is
  **harness–model co-evolution**, i.e. deliberately letting the model absorb harness function.

**Honest counter, and I hold it:** 2604.27891's scope is *conversational procedural tasks* with LLM-as-judge
scoring — not multi-agent coding work, not enforcement, and it makes **no** authority claim. It cannot
obsolete an enforcement plane, because a model that self-orchestrates still cannot bind its own authority
(wfh-004's C-4 is untouched by it). But it does directly attack the *orchestration and structure* half of this
theme, and it is the only controlled comparison I found that measures the harness's value rather than
assuming it. **The theme should hold "the harness is durable" as a position, not as a premise** — it is a
seventh candidate.

### Third — **the highest-signal failure class is evidence integrity, and capability gating cannot touch it.**

Both large failure corpora rank **fabricated success reports / deception / inaccurate self-reporting** among
the dominant risks, and 2605.29442 finds it **increasing over time**. No amount of authority binding fixes an
agent that did nothing and said it succeeded. The control for that is an **artifact-backed proof discipline** —
which this operation already runs as its firewall (D7) and which is **absent from the eight concerns
entirely**. If there is an under-claimed asset in this theme, it is more likely this than the capability
derivation, and it is unclaimed in the register.

### Cold-leg dry results (recorded because they are dry)

- Search for a work stating P2(ii) in read-set/write-set form: **no hit**. The negative is legible: I searched
  workflow-net soundness, IFC/non-interference, separation logic frame conditions, and the agent-gate
  literature, and found the *principle* everywhere and the *formalization* nowhere.
- Search for prior art positioning "phase-indexed permission derivation" as novel: **dud** — returned
  patent-industry marketing. Recorded as a failed query, not as evidence of absence.
- Search for evidence that agent operators *disable* deterministic gates at measurable rates: **no direct
  measurement found.** The closest is 2605.24309's approval-fatigue trade-off, which is an argument, not a
  rate. **This is the specific empty cell behind P3's counter-case B** — a measured bypass rate for agent
  permission prompts appears not to exist, and would be the single most decision-relevant number available.

---

## Suspected cross-surface aliases (flag, do not merge — I cannot see the other scouts)

| What I found | Likely alias on another surface |
|---|---|
| Progent's *monotonic confinement* (SMT-checked narrow-only) | **adjacent**: capability *attenuation* in OS capability systems / distributed delegation. Same property, different word. W4 should find it as "attenuation" or "no amplification" |
| DO-178C verification independence | **adjacent**: separation of duty (security), four-eyes / two-person rule (nuclear, finance), "the author does not sign off" (medical device) |
| SLSA L3 control-plane/data-plane isolation | **products**: CI/CD systems with derived job identity; GitHub Actions `permissions:` + OIDC claim scoping. Almost certainly W2's strongest P4 candidate — and note **2606.26924 measured Actions at 33% permission declaration vs <1% for agent configs**, which is a ready-made scope-versus-need datum |
| CaMeL's control/data-flow extraction from the trusted query | **active-dev**: likely shipping inside prompt-injection defenses under names like "planner/executor split," "P-LLM/Q-LLM," "dual-LLM pattern" |
| Runtime-monitor synthesis (P1/C2) | **adjacent**: policy engines compiling declarative policy to a decision procedure (OPA/Rego-class). W2 will meet the same idea as a product category |
| SkillScope's task-conditioned least privilege | **active-dev**: agent-skill security tooling; there is a curated tracker (`LLMSecurity/awesome-agent-skills-security`) W3 should be reading |
| "Scaffolding ceiling" / harness-model co-evolution | **active-dev**: self-improving harness repos; **products**: vendors folding harness functions into the model API |

---

## Reuse / dedup notes

Queried Unimatrix (`context_search`, `agent_id: wfh-005-scout-literature`) for workflow authorization,
capability gating, phase/role-derived permissions, harness enforcement and determinism, k=15.

**Result: the graph holds no literature at all on this theme.** Every returned node is either a wfh-001
shipped-tool `technology` (#137 OpenHands, #139 Cursor, #140 Windsurf, #141 Devin, #142 Replit, #144 Cline,
#145 Factory.ai, #147 Cannoli, #148 Rivet, #149 LangGraph Studio, #150 Dify — all `grade:claimed`,
`theme:workflow-harness`, `wfh-001`) or process/convention noise (#186 wfh-004 retro, #187/#188 auto-extracted
conventions). Top semantic score against a literature query was **0.40**, and it was Dify.

**Consequences:**
1. **Nothing in this report duplicates an existing node.** Every work named here is new to the graph.
2. This is itself a **finding about the theme's surface coverage**: the `surface` tally that `themes.md`
   §"The watchlist" proposes as the honesty check would, run today, show `literature` at **zero**. The
   research-literature surface has been *staffed and never read*, exactly as the standard predicted.
3. I did **not** re-fetch #143 / #146 / #150 / #159 or the wfh-002 verdicts #177–#185 individually — the
   semantic sweep confirmed the class (shipped tools, process verdicts) and no citation below collides with
   them. wfh-002's #185 (rule evaluation is queen-side) is **corroborated** by CaMeL/Progent — enforcement
   external to the model — but I am not re-litigating it and it is not under test.

---

## cites:

Verified by direct abstract-page fetch (title, authors, date, abstract read verbatim):

```
- type: paper, ref: arXiv:2503.18813, title: "Defeating Prompt Injections by Design",
  author: "Debenedetti; Shumailov; Fan; Hayes; Carlini; Fabian; Kern; Shi; Terzis; Tramèr",
  org: "Google", year: 2025, surface: literature
- type: paper, ref: arXiv:2504.11703, title: "Progent: Securing AI Agents with Privilege Control",
  author: "Shi; He; Wang; Li; Wu; Guo; Song", year: 2025, surface: literature
- type: paper, ref: arXiv:2512.11147, title: "MiniScope: A Least Privilege Framework for Authorizing Tool Calling Agents",
  author: "Zhu; Tseng; Vernik; Huang; Patil; Fang; Popa", year: 2025, surface: literature
- type: paper, ref: arXiv:2603.28166, title: "Evaluating Privilege Usage of Agents with Real-World Tools",
  author: "Zhang; Fu; Lian; Go; Wang; Zhou; Jiang; Pu", venue: "FSE 2026 (IVR track)", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.05868, title: "SkillScope: Toward Fine-Grained Least-Privilege Enforcement for Agent Skills",
  author: "Wu; Nan; Lin; Wang; Xiao; Wang; Zheng", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.14859, title: "Do Coding Agents Understand Least-Privilege Authorization?",
  author: "Yan; Weng; Chen; Peng; Qin; Guan; Liu; Yu; Yuan; Meng; Che; Hu", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.17998, title: "Verify-Gated Completion as Admission Control in a Governed Multi-Agent Runtime: A Bounded Architecture Case Study",
  author: "Nguyen; Tran", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.24309, title: "Reframing LLM Agent Security as an Agent-Human Interaction Problem",
  author: "Wang; Li; Tian", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.29442, title: "How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions",
  author: "Tang; Chen; Xu; Shi; Huang; McMillan; Dong; Li", year: 2026, surface: literature
- type: paper, ref: arXiv:2605.30777, title: "What Breaks When LLMs Code? Characterizing Operational Safety Failures of Agentic Code Assistants",
  author: "Al Hasan; Biswas", year: 2026, surface: literature
- type: paper, ref: arXiv:2606.13884, title: "Capability Minimization as a Safety Primitive: Risk-Aware Causal Gating for Least-Privilege LLM Agents",
  author: "Ganesh Iyer; Suresh Babu", year: 2026, surface: literature
- type: paper, ref: arXiv:2606.14249, title: "HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry",
  author: "Chen; Lu; Zhao; Meng; Teng; Li; Li; Liu; Liang; Zhang; Xie; Qu; Shao; Luan", year: 2026, surface: literature
- type: paper, ref: arXiv:2606.20683, title: "From Question Answering to Task Completion: A Survey on Agent System and Harness Design",
  author: "Guo; Hao; Wang; Fan; Luo; Li; Gao; Mei; Peng; Xu; Dong; Wu; Zheng; Han; Wang; Xu; Wang", year: 2026, surface: literature
- type: paper, ref: arXiv:2606.26924, title: "A Deterministic Control Plane for LLM Coding Agents",
  author: "Madatha", year: 2026, surface: literature
- type: paper, ref: arXiv:2606.28679, title: "Capability Gates Are Not Authorization: Confused-Deputy Failures in LLM Agent Frameworks",
  author: "Mellafe Zuvic", year: 2026, surface: literature
- type: paper, ref: arXiv:2607.13070, title: "Falsifiable Release Gates for Self-Improving Systems: Standing Invariants at Scale",
  author: "Soni", year: 2026, surface: literature
- type: paper, ref: arXiv:2604.27891, title: "In-Context Prompting Obsoletes Agent Orchestration for Procedural Tasks",
  author: "Dennis; Diamond; Patil; Shabahang; Guo", year: 2026, surface: literature
```

Verified by multiple independent corroborating sources (venue, year, pages/DOI consistent across ≥2
independent indexes); **full texts not read**:

```
- type: paper, ref: "IFIP WG11.3 Workshop on Database Security, Aug 1997",
  title: "Task-Based Authorization Controls (TBAC): A Family of Models for Active and Enterprise-Oriented Authorization Management",
  author: "Thomas; Sandhu", year: 1997, surface: literature
- type: paper, ref: "doi:10.1007/3-540-61770-1_27", title: "An Authorization Model for Workflows",
  author: "Atluri; Huang", venue: "ESORICS 1996, LNCS 1146, pp. 44-64", year: 1996, surface: literature
- type: paper, ref: "ACM TISSEC 2(1):65-104", title: "The Specification and Enforcement of Authorization Constraints in Workflow Management Systems",
  author: "Bertino; Ferrari; Atluri", org: "ACM", year: 1999, surface: literature
- type: paper, ref: "doi:10.1007/978-3-540-74835-9_7", title: "Satisfiability and Resiliency in Workflow Systems",
  author: "Wang; Li", org: "Purdue University", venue: "ESORICS 2007", year: 2007, surface: literature
- type: paper, ref: "doi:10.1145/54289.871709", title: "The Confused Deputy: (or why capabilities might have been invented)",
  author: "Hardy", venue: "ACM SIGOPS Operating Systems Review 22(4):36-38", year: 1988, surface: literature
- type: paper, ref: "doi:10.1145/2046707.2046779", title: "Android Permissions Demystified",
  author: "Felt; Chin; Hanna; Song; Wagner", org: "UC Berkeley", venue: "ACM CCS 2011", year: 2011, surface: literature
- type: paper, ref: "doi:10.1145/1595676.1595684", title: "The Compliance Budget: Managing Security Behaviour in Organisations",
  author: "Beautement; Sasse; Wonham", venue: "NSPW 2008", year: 2008, surface: literature
- type: paper, ref: "Communications of the ACM 42(12):40-46", title: "Users Are Not the Enemy",
  author: "Adams; Sasse", year: 1999, surface: literature
- type: paper, ref: "https://www.ndss-symposium.org/wp-content/uploads/2017/09/01_4-paper.pdf",
  title: "Learning from Shadow Security: Why Understanding Non-Compliant Behaviors Provides the Basis for Effective Security",
  author: "Kirlappos; Parkin; Sasse", org: "University College London", year: 2014, surface: literature
- type: paper, ref: arXiv:1205.0852, title: "On the Parameterized Complexity and Kernelization of the Workflow Satisfiability Problem",
  author: "Crampton; Gutin; Yeo", year: 2012, surface: literature
- type: paper, ref: arXiv:1809.10106, title: "Results in Workflow Resiliency: Complexity, New Formulation, and ASP Encoding",
  author: "Fong", year: 2018, surface: literature
- type: standard, ref: "https://slsa.dev/spec/v1.1/", title: "SLSA — Supply-chain Levels for Software Artifacts, v1.1 (Build track L1-L3)",
  org: "OpenSSF", surface: literature
- type: standard, ref: "RTCA DO-178C / EUROCAE ED-12C", title: "Software Considerations in Airborne Systems and Equipment Certification (verification independence, DAL-A/B)",
  org: "RTCA", year: 2011, surface: literature
```

**Surfaced but NOT individually verified — do not cite downstream without a fetch:**
`arXiv:2603.14707` (Visual Confused Deputy) · `arXiv:2408.04870` (ConfusedPilot) · `arXiv:2601.15195`
(failed agentic PRs) · `arXiv:2604.08906` (bug triggers in agentic frameworks) · `arXiv:2603.22928`
(SoK attack surface of agentic AI) · `arXiv:2604.23338` (security threats/defenses SoK) ·
`arXiv:2607.00041` (workflow atomicity / write-set disjointness) · `arXiv:2605.16407`, `arXiv:2606.31023`,
`arXiv:2604.06401` (proof-carrying / certified LLM pipelines) · `doi:10.3390/fi18060326` (MDPI orchestration
survey) · USPTO 11388163 / 10148701 / 9264449 / 10158670 / 10803166. Each was surfaced by search and its
existence is likely; **I did not open them**, and per this run's own discipline that means I am not asserting
them.
