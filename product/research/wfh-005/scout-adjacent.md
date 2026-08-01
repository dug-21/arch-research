# scout-adjacent.md — wfh-005 challenge scan, adjacent-prior-art surface

**Run:** `wfh-005` · Issue #54 · surface **W4 (adjacent prior art)** · **CHALLENGE mode** · read-only, zero graph writes.
**Agent:** `wfh-005-scout-adjacent`. **Citation surface label:** `adjacent` on every entry.
**Scope honesty:** exhaustion is relative to the five named positions and the fields named in §1. Nothing here
moves status; every external result is `claimed`, including the ones that damage our positions.

**Headline:** **P2 is falsified on all three sub-claims from this surface alone.** P3 and P5 are wounded in
specific, statable ways. P4 routes **ASSEMBLE** with a precisely-named uncovered remainder. P1 survives but
carries almost no diagnostic weight. The cold leg proposes a **sixth position** that I think is more dangerous
to the theme than any of the five.

---

## 1. Fields checked — every one, including the dry and the undone

| # | Field | What I expected to find | What I found |
|---|---|---|---|
| 1 | **OS capability models** (KeyKOS, EROS, seL4, Capsicum, object-capability discipline) | the confused-deputy lineage; attenuation; no-ambient-authority | P1's lineage confirmed (Hardy 1988). **Dry on phase-indexation** — ocap has no notion of a workflow phase; authority is a graph property, not a process property. Its live descendant is WASI (row 12) |
| 2 | **BPM / workflow nets / WfMC / van der Aalst line** | per-activity per-role authorization constraints; "soundness" | **Direct hits**: WAM (1996), TBAC (1997). Plus a **name collision** on "soundness" (row 3 of §2) and the CMMN/ACM admission (cold leg) |
| 3 | **Distributed delegation & attenuation** (macaroons, biscuit, SPKI/SDSI, Kerberos constrained delegation, OAuth token exchange/downscoping) | derivation of a narrowed authority along a chain | Attenuation is **monotone narrowing along a delegation chain**, not derivation from a process spec. *Analogous-weaker.* Kerberos S4U / OAuth RFC 8693 reasoned from prior knowledge, **not verified this run** |
| 4 | **Supply-chain attestation** (in-toto, SLSA, TUF, hermetic builds) | in-toto layouts deriving per-step permitted materials/products | **The single richest field for P2.** in-toto layouts, SLSA L3 non-falsifiable provenance, Bazel/Nix hermetic sandboxing. TUF **not read** |
| 5 | **Safety-critical formal gates** (DO-178C/DO-330, nuclear conduct-of-ops & tech specs, ITIL CAB) | independence between doer and verifier | Independence confirmed; and **DO-330's tool-qualification criterion is the sharpest counter-case to P3 I found anywhere** |
| 6 | **Trusted computing / measured boot** *(my addition)* | a gate whose input the gated party cannot rewrite | **Structurally identical to P2(ii)** — SRTM, measure-before-execute, PCR extend-only |
| 7 | **Formal integrity models** (Clark-Wilson, Biba) *(my addition)* | the person-level form of the gate rule | **Clark-Wilson enforcement rule E4, 1987** — the certifier of a transformation procedure may not execute it. P2(ii) at the person altitude, 39 years old |
| 8 | **Database transaction isolation / staged commit** *(my addition)* | read-set/write-set disjointness as a checkable condition | **Dry for prior art, valuable for naming.** The field supplies the exact vocabulary (read set, write set, conflict) in which P2(ii) should be stated, but has no gate-soundness analogue. Report as a vocabulary transplant, not a precedent |
| 9 | **Least-privilege derivation from observed behaviour** (IAM Access Analyzer, audit2rbac, `audit2allow`, seccomp-profile generation) *(my addition)* | someone deriving a ceiling rather than writing it | **Shipping, at cloud scale, since 2021.** Observation-derived rather than declaration-derived — that distinction is now the *only* thing left of P2(iii) |
| 10 | **Human-factors / safety science** (Vaughan, Snook, Rasmussen, Reason, Hollnagel) *(my addition)* | named theory for institutionalized bypass | Normalization of deviance · practical drift · drift-to-danger. **This is the named theory for our two-for-two bypass record** |
| 11 | **Usable-security economics** (Beautement/Sasse/Wonham; Herley) *(my addition)* | why controls get routed around even when they work | The compliance budget; rational rejection of security advice. **Bypass is predicted by the model, not a local failure of ours** |
| 12 | **WebAssembly component model / WASI Preview 2** *(my addition)* | capability set derived from a declared interface | **Structurally identical to P2(iii)** minus the phase axis — the WIT world *is* the declared demand set and the host grants exactly it |
| 13 | **Financial four-eyes / maker-checker** *(assigned)* | separation of duty as a gate condition | Subsumed by row 7. **Already mined by wfh-004 (L1-16).** No new mechanism; it is Clark-Wilson E4 wearing a bank's clothes |
| 14 | **Clinical-trial protocol gating** *(assigned)* | pre-registration and amendment discipline | **Already mined by wfh-004 (L1-33, L1-51).** One unmined angle survives and belongs to the cold leg: the *base rate of protocol amendments*, which I did **not** measure |

### Declared holes — named, not hidden

- **Rail interlocking — NOT SEARCHED, and I think this is the most costly hole.** Expected: route-locking as a
  genuinely phase-indexed authority model (a route may be set only while conflicting routes are locked out,
  and the lock is held by the interlocking, not by the signaller). That is closer to `(workflow, phase, role)`
  than anything in the BPM literature, because it is *physically* enforced and the actor cannot mint its own
  release. **Recommend this as the round-two target for this surface.**
- **Hardware design sign-off flows — NOT SEARCHED.** Expected: staged tapeout gates with independent DRC/LVS
  sign-off and an ECO discipline. Named in my assignment, not executed.
- **Medical-device approval (IEC 62304 / FDA design controls) — NOT SEARCHED.** Expected: a weaker cousin of
  DO-178C's independence.
- **TUF, SPKI/SDSI — NOT READ this run.**
- **Primary sources not retrieved** (secondary explanations only): Clark & Wilson 1987 (IEEE S&P); Vaughan 1996
  and Snook 2000 (books); the SLSA v1.0 requirements page; Gartner's own iBPMS retirement note. **Flagged to W1
  and the leader — I am reporting these as `claimed` at second hand, and a mis-summary in a secondary source
  would propagate.**

---

## 2. Translation table

*Their name · their field · what it is · how close · our name · what ours would still have to add.*

| Their name | Field | What it is | Closeness | Our name for it | What ours must still add |
|---|---|---|---|---|---|
| **Workflow Authorization Model (WAM)** | BPM security, 1996 | Authorizations granted to a subject **only during the execution of a task** and revoked immediately on completion; synchronized to workflow progression | **Structurally identical** to P2(i) | phase-indexed capability set | The *derivation* step. WAM synchronizes an **authored** authorization to a phase; it does not compute the set from the phase's declared demands |
| **Task-Based Authorization Controls (TBAC)** | BPM security, 1997 | Access control from a task-oriented rather than subject-object view; **each step carries a protection state whose permission set changes as the task progresses**; "just-in-time permissions" | **Structurally identical** to P2(i) | `(workflow, phase, agent-role) → capability set` | Same as WAM: derivation, plus a non-declarative actor |
| **in-toto layout** | supply-chain attestation | A signed policy naming the chain's **steps**, the **functionaries authorized to perform each step** (pubkeys + threshold), and per-step **expected_materials / expected_products** artifact rules (MATCH/ALLOW/CREATE/DELETE/MODIFY/DISALLOW) | **Structurally identical** to P2(i) *and* to a declared per-phase write-set | phase write-set + per-phase role binding | The layout is **hand-written**. Our claim to derive it from a spec's demands is the only surviving delta — and rows below take that too |
| **SLSA Build L3 non-falsifiable provenance** | supply-chain attestation | Provenance is generated by the build **platform**, in a trusted control plane; the build job cannot modify or forge it; the signing identity is not reachable from the build script | **Structurally identical** to P2(ii), at the data altitude | gate-input independence | Ours generalizes it to *any* gate predicate over *any* phase; SLSA states it for one predicate (provenance) in one domain |
| **Measured boot / SRTM, PCR extend** | trusted computing | Each stage **measures the next before executing it**; measurements land in registers that are **extend-only**, so measured code cannot rewrite its own measurement | **Structurally identical** to P2(ii) | write-set/read-set disjointness at a gate | Ours must state it as a *checkable property of a declared workflow*, not as a hardware invariant |
| **Clark-Wilson enforcement rule E4** | integrity models, 1987 | The **certifier** of a transformation procedure may not be its **executor**; IVPs verify CDIs independently of the TPs that produced them | **Structurally identical** to P2(ii), at the *person* altitude | independence of the gate principal | The data-flow form (inputs vs write-sets) rather than the person form (certifier vs executor) |
| **DO-178C "with independence"** | aviation certification | For objectives requiring independence, the verifier may not be the author; at DAL-A/B no requirement may be verified by its authors | **Analogous — weaker**, person-level and procedural | verifier ≠ producer | A machine-checkable version. DO-178C's independence is audited by humans, ours must be a predicate |
| **DO-330 tool-qualification criterion** | aviation certification | An unqualified (i.e. unassured) tool is permitted on the path **if its output is otherwise independently verified**; qualification is required only when the output is *not* verified | **Structurally identical** to the counter-case against P3 | checked-output, not checked-process | Nothing. **This is prior art against us, not for us** |
| **Bazel action sandboxing / Nix derivation** | hermetic builds | The action's execroot contains **only its declared inputs**; undeclared inputs are simply absent, so declaration errors surface as failures | **Structurally identical** to P2(iii), read-set half | ceiling derived from declared demands | The *write*-set half and the phase axis. Also: Bazel's sandbox is famously leaky at `/`; Nix is stricter |
| **WASI Preview 2 / component model WIT world** | wasm runtimes | A component starts with **no ambient authority**; its WIT world declares every interface it imports; the host grants exactly those and nothing else | **Structurally identical** to P2(iii) | spec-derived capability ceiling | The phase axis, and an actor whose demands are **not declarable in advance** — the load-bearing gap (see §6) |
| **IAM Access Analyzer policy generation / `audit2rbac`** | cloud IAM, k8s | Generate a least-privilege policy **from observed access activity** rather than hand-writing it | **Structurally identical** to P2(iii) via a different input (observation, not declaration) | derived over-granting ceiling | Ours claims derivation from *declaration*; theirs from *behaviour*. Both are "don't hand-write the ceiling," which is what the novelty claim actually asserted |
| **Macaroon caveats / biscuit datalog attenuation** | distributed authz | A bearer token can be **narrowed** by anyone holding it, offline, monotonically; biscuit expresses caveats in Datalog | **Analogous — weaker** | delegation attenuation | Attenuation constrains a *chain*; it never derives a set from a process definition. Useful mechanism, wrong claim |
| **Workflow-net "soundness"** | Petri nets / BPM | A WF-net is sound if it is deadlock/livelock-free, always reaches proper completion, and has no dead transitions | **Superficially similar only — and a naming hazard** | *(do not call ours "soundness")* | **Rename.** "A soundness rule for transition gates" will be read by anyone from BPM as van der Aalst soundness, which is an entirely different property. Suggest **"gate-input independence"** |
| **CMMN / adaptive case management** | BPM, OMG 2014 | Notation for **unpredictable, knowledge-intensive work** that cannot be pre-modelled as a sequence; event-condition-action rather than control flow | **Structurally identical to the problem the theme has and has not named** | *(none — this is the cold leg)* | See §8 |
| **Change Advisory Board / ITIL change management** | IT service management | External approval of every change before release | **Structurally identical** to our human gate — **and measured to fail** | blocking human gate | See P3/P5 |
| **Normalization of deviance · practical drift · drift-to-danger** | safety science | Unacceptable practice becomes acceptable through unremarkable repetition; practice steadily uncouples from written procedure under cost-effectiveness pressure | **Structurally identical** to our two bypass incidents | institutionalized bypass | Nothing. **This is the named theory wfh-004 lacked** |
| **The compliance budget** | usable-security economics | Users have a finite budget for compliance effort; once exhausted, non-compliance is the rational default | **Structurally identical** to our provisioned bypass | bypass economics | Nothing. It predicts our result |

---

## 3. P2 — **FALSIFIED** (primary attack; all three sub-claims)

### Sub-claim (i) — "deriving a capability set from `(workflow, phase, agent-role)` is unclaimed" → **FALSIFIED**

Two papers, thirty years old, do exactly the indexing.

- **WAM** (Atluri & Huang, ESORICS 1996): authorizations "granted to subjects **only during the execution of the
  task** and revoked immediately after the completion of the task," with the model providing "synchronization
  between granting and revoking of privileges with the progression of the workflow."
- **TBAC** (Thomas & Sandhu, IFIP WG11.3 1997): access control modelled "from a task-oriented perspective rather
  than the traditional subject-object one," where **"each step [is] associated with a protection state
  containing a set of permissions that change based on the task"** — explicitly named an **active** security
  model with **just-in-time permissions**, and explicitly motivated by *agent-based distributed computing and
  workflow management*.

The `(workflow, phase, role)` triple is TBAC's protection state indexed by task step and role. There is also a
whole downstream literature (role-based authorization for workflow with task-based separation of duty; safety
analysis of workflow authorization models; conflict detection for workflow authorization policies) — i.e. this
is not one obscure paper, it is a **sub-field**.

**What survives:** the word *deriving*. WAM and TBAC **bind** an authored authorization set to a phase; they do
not **compute** it. If the theme's claim is restated as *"computing the set from the phase's declared demands
is unclaimed,"* it is a different claim — and sub-claim (iii) kills that one too.

### Sub-claim (ii) — "a soundness rule for transition gates has no prior art" → **FALSIFIED**

The principle *every input to a gate predicate lies outside the write-set of the phase being exited* has at
least four independent prior instantiations, one of them from 1987:

1. **Clark-Wilson E4 (1987)** — the certifier of a transformation procedure may not execute it; IVPs verify
   independently of the TPs. Person altitude, but the same invariant: **the checked party cannot be the source
   of the check's inputs.**
2. **DO-178C independence** — at DAL-A/B, no requirement may be verified by its authors.
3. **SLSA Build L3 non-falsifiable provenance** — *data* altitude, and the closest match: provenance must be
   generated by the trusted control plane, the build job cannot modify or forge it, the signing identity is not
   accessible to the build script, and "even if the build script is fully compromised, it cannot produce a valid
   provenance attestation for an artifact it did not build." **That is our rule, stated for one predicate.**
4. **Measured boot / SRTM** — each stage measures the next *before* executing it, into extend-only registers.
   The measured code cannot rewrite its measurement. Structurally identical, in silicon, for two decades.

**What survives:** the *generalization*. Nobody I found states it as a **general soundness condition over an
arbitrary workflow's declared phase write-sets**, mechanically checkable at definition-authoring time. That is a
formalization contribution, not a discovery, and it should be claimed as one.

**Naming hazard, load-bearing:** **do not ship this as "soundness."** In the field this claim will be read
against — workflow nets — "soundness" already means deadlock/livelock freedom, proper completion, and no dead
transitions (van der Aalst). Calling ours a soundness rule guarantees a misread by exactly the audience that
would otherwise take it seriously. Proposed name: **gate-input independence**. State it in the
read-set/write-set vocabulary that database concurrency control already supplies — that vocabulary is precise,
universally understood, and free.

### Sub-claim (iii) — "deriving the over-granting ceiling from a spec's declared demands is unpublished" → **FALSIFIED**

- **WASI Preview 2 / component model.** A component "starts with no ambient authority and can only do what the
  host explicitly grants"; capabilities are expressed as WIT interfaces and **requested through imports**; the
  component "carries its own WIT world — a precise declaration of every interface it imports." A component
  importing only `wasi:io/streams` "cannot secretly open a raw socket." **That is verbatim the mechanism: the
  ceiling is the spec's declared demands, computed by the host, never hand-written.**
- **Bazel / Nix.** "Sandboxing enforces action-level hermeticity: each action runs in an execroot that contains
  **only declared inputs**… sandboxing guarantees that all build inputs are declared correctly, because
  otherwise the input files will simply not be available." Read-set ceiling, derived from declaration, shipping
  for over a decade at Google scale.
- **in-toto artifact rules.** Per-step `expected_materials` / `expected_products` with MATCH/ALLOW/CREATE/
  DELETE/MODIFY/DISALLOW **are** a declared per-step read-set and write-set, and the trailing `DISALLOW *` is
  precisely a default-deny ceiling.
- **And the observation-derived variant ships too:** IAM Access Analyzer generates a fine-grained least-privilege
  policy from CloudTrail activity (GA 2021, 50+ services); `audit2rbac` generates RBAC roles and bindings
  covering exactly the API requests a principal actually made.

**What survives:** essentially nothing of the claim as stated. The residual is the *conjunction* — a
declaration-derived ceiling that is **also** phase-indexed **and** whose gate inputs satisfy independence,
applied to an actor that cannot declare its own interface.

### P2 overall — **FALSIFIED**

All three sub-claims have prior art; two have prior art that is **structurally identical** and one has prior art
that is **shipping product**. The honest residual is a **composition claim**, which I did *not* find assembled
anywhere:

> phase-indexed authority (WAM/TBAC) × spec-derived ceiling (WASI/Bazel/in-toto) × gate-input independence
> (Clark-Wilson/SLSA/SRTM), applied to a **non-declarative actor**.

**A composition claim is a far weaker moat than an absence claim and must be relabelled as such at the gate.**
Every ingredient is public, mature, and in several cases has an off-the-shelf implementation (→ P4). The
defensible novelty is the *fourth* factor — the non-declarative actor — and that is a **research problem the
adjacent fields have never had to solve**, because every principal on their shelf declares its interface.

**What would have falsified my falsification:** a search of these fields returning only *analogous-weaker*
matches. It did not — rows 1, 3, 4, 5, 6, 10, 12 of §2 are marked structurally identical, from five unrelated
fields. That is not a marginal negative; it is a convergent positive against us.

---

## 4. P3 — **WOUNDED** (both flanks)

### Flank 1: the claim is too strong. Aviation permits inference on the path, by rule.

**DO-330 tool qualification.** The governing question is *"Is the output of the tool otherwise verified?"* — and
**"if you independently verify the tool's output through other means, the tool does not need to be qualified at
all."** The most conservative software assurance regime on Earth explicitly admits an **unassured component on
the development path** whenever a downstream check validates its output, and reserves qualification for the case
where the output is *not* verified.

Read against P3: *"inference anywhere on the enforcement path demotes a guarantee to a tendency"* is false as
written. The certification world's actual rule is finer and better:

> A component's assurance is irrelevant where its **output** is independently verified at the gate's altitude.
> It is decisive where the component **is** the verification.

DO-330 Criterion 2 makes exactly this cut — the heavy qualification burden lands on tools that *automate
verification* and whose output is used to **eliminate or reduce other verification**. That is the precise class
in which inference is fatal. And the safety-critical fields have lived with a fallible judge inside a gate for
decades and still claim assurance, via named devices: **independence** (verifier ≠ author), **diverse
redundancy**, **two-man rule**, **checklists as challenge-and-response**, and **defence in depth** — none of
which make the judge reliable; all of which make the *system's* claim survive the judge being wrong.

**The narrowing to carry to triage:**

> Inference on the path demotes a guarantee to a tendency **iff the inference's output is not checkable by a
> deterministic predicate at the gate's altitude.** Where a verifier/generator asymmetry exists — the checker is
> cheaper and deterministic while the generator is not — inference is free and the guarantee is intact.

This is not a cosmetic edit. wfh-004's register is sorted by `inference-minimality` as a scalar. The correct key
is **binary and positional**: is the model on the *generation* leg (fine, if checked) or the *checking* leg
(fatal)? Under the corrected key, C-04 stays; a number of abilities justified by "reduce inference" lose their
justification; and the whole "dangerous middle" framing needs re-derivation. **The shortlist is sorted by a key
that is right in direction and wrong in shape.**

### Flank 2: determinism is not sufficient — and this field has the best evidence against us

- **Normalization of deviance** (Vaughan): "the gradual process through which unacceptable practice or standards
  become acceptable." **Practical drift** (Snook): "the slow steady uncoupling of practice from written
  procedure," where behaviour that appears to work is "legitimized through unremarkable repetition."
  **Drift to danger** (Rasmussen): systemic migration toward accident under pressure toward cost-effectiveness.
- **The compliance budget** (Beautement, Sasse & Wonham, NSPW 2008) and **the rational rejection of security
  advice** (Herley, NSPW 2009): non-compliance is the *predicted* steady state once compliance cost exceeds the
  budget. Our own provisioned bypass, written into `postCreate.sh` in two variants, is a textbook instance —
  **not a local failure of discipline but the model's central prediction.**
- **The measured version — DORA.** External approval by a change manager or CAB is **negatively correlated with
  lead time, deployment frequency and time-to-restore, and has *no* correlation with change fail rate**;
  organisations with formal external approval are reported **2.6× more likely to be low performers**. This is
  the closest thing to a controlled experiment on "does a comprehensive deterministic control plane deliver
  assurance," and the answer was **no, and it costs you speed**.

wfh-004's triage already has the right instinct (the ship rule; the 18% counterweight ratio; probe #2). What
this surface adds is that **the ship rule is not a prudent hedge, it is the field's consensus finding**, and
that the counterweight ratio should be treated as a *design constraint with published support*, not a posture.

**Verdict: WOUNDED.** P3 survives only in the narrow form above. The strongest attack it withstood: nothing I
found shows a *hard* guarantee produced by an unchecked inferential component — the DO-330 case is checked
output, which concedes the core point about the checking leg.

---

## 5. P5 — **WOUNDED**, and the natural experiment is worse than wfh-004 feared

wfh-004's triage said the register is "a defect list, not a product requirement list." From this surface, the
question is sharper: **the comprehensive-control-plane product category has run before, twice, and lost twice.**

**Run 1 — WfMC-era workflow → BPM suites → iBPMS.** Gartner **retired the iBPMS Magic Quadrant in 2021**,
replacing it with a Market Guide, and the category dissolved into business-process-automation and low-code
application platforms. Growth of the BPMS market was reported as modest as early as 2017. The heavyweight
modelled control plane was displaced from below by lighter things (RPA, which explicitly required **no** process
model, and the connector/automation tools) and from the side by developer-facing embeddable engines. Practitioner
literature reports BPM programme failure rates around 70%, attributed to "rigid architectures, consultant
dependency, and interfaces designed for process engineers rather than the people who actually do the work."
*(Secondary sources; treat the 70% as an industry figure, not a measurement.)*

**Run 2 — ITIL change management.** The CAB is the enterprise's comprehensive gate. DORA measured it and found it
net-negative (§4). ITIL itself moved to "change enablement" and peer review.

**That is the natural experiment P5 asked for, and it returns: displaced, then measured as ineffective.**

**But the demand is not absent — it is differently shaped, and that is the actual narrowing.** Vu, Klievtsova,
Leopold, Rinderle-Ma & Kampik (Responsible BPM 2025) interviewed **22 BPM practitioners** about governing AI
agents in processes. External, not our incident log. They want: **clear business goals · legal and ethical
guardrails · human-agent collaboration and redefined human involvement · customized agent behaviour · risk
management · safe integration with fallback options**, and they name the traditional BPM frameworks as requiring
adaptation rather than being sufficient.

Now put that list beside wfh-004's register. The register's mass sits on **Introspection, Security-as-bounding
and Structure** (its own count: 127 of 205 slots) and reads **empty on Cost and Human steering**. The
practitioners' list is dominated by **goals, human-agent role definition, and fallback/degraded operation** —
i.e. **the two cells wfh-004 declared empty, plus a concern (degraded mode) wfh-004's own §7(2) says nobody
asked about.**

**Verdict: WOUNDED.** The narrowing:

> There is external demand for an agent control plane. There is **no** external evidence that its requirement
> set resembles ours. The one external practitioner sample I found asks predominantly for the things our
> register scores as empty cells, and does not ask for the things our register is 60% made of. Demand is real;
> **the register is not evidence of it.**

**Downstream implication:** the P5 answer is not "kill it" — it is that the **triage gate should not read the
128 as requirements**, and the cheapest correction is exactly the one wfh-004 already wrote and nobody executed:
*state one workflow a stranger wants to run and cannot, without reference to our incident log.* This surface
supplies three candidate strangers' workflows for free — agent fallback/degraded operation, human-agent role
definition, and per-run cost — and they are the ones we scored as holes.

---

## 6. P4 — **WOUNDED → route ASSEMBLE**, with the remainder named

There is a deep, mature, mostly-CNCF shelf, and it covers more of the eight concerns than the theme has ever
acknowledged.

**What the shelf covers**

| Concern | Off-the-shelf components | Coverage |
|---|---|---|
| **Security** | WASI/wasmtime (no ambient authority, ceiling from declared imports) · seL4 / Capsicum · macaroons / biscuit (attenuated delegation) · OPA-Rego, Cedar, admission control | **Strong.** The enforcement primitives exist and are proven at scale |
| **Introspection** | in-toto + **witness** + Archivista (attestation capture, normalization, graph storage, embedded Rego policy over attestation content) · SLSA · sigstore · OpenTelemetry | **Strong** for attestation and provenance |
| **Structure** | BPMN engines / Zeebe · workflow-net verifiers (Woflan, LoLA, ProM) · Temporal-class durable execution | **Good**, for pre-declarable processes |
| **Recovery & durability** | durable execution, sagas, compensation events | **Strong** |
| **Human steering** | BPMN user tasks, approval steps | **Partial**, and P3/P5 say the heavy version measures badly |
| **Cost transparency** | — | **Nothing** |
| **Self-improvement** | SPC/FOQA exist as *practices*, not as products for this | **Nothing** |
| **Context provisioning** | — | **Nothing** |

**The eighty-percent case, and the uncovered remainder — this is the part that matters.**

Every component on that shelf makes the same assumption, and it is the same one in each case: **the principal is
a program with a statically declared interface.** Bazel has `srcs`/`deps`. WASI has a WIT world. in-toto has a
layout written before the run. OPA has a policy over a known input schema. Attenuation narrows a chain whose
shape you knew when you minted the root.

**An LLM agent has none of these.** Its demand set is discovered while the work happens, varies per run, and is
precisely what nobody can enumerate in advance — which is *why* wfh-004's C-07 ("the unenumerated") and the
Rel↓ declarations exist. So:

> **The uncovered remainder is: deriving and enforcing a bound for an actor that cannot declare its interface.**
> It is small, it is the differentiating part, and no piece on the shelf addresses it.

Two further seams the assembly does not close: **(a) four policy languages and four identity models** — in-toto
functionary keys, OPA input schemas, WASI capability handles, Temporal namespaces — with no common principal;
**(b) three of the eight concerns (cost, self-improvement, context provisioning) have no component at all**, and
context provisioning is the one that is *specific to an inference-driven actor*.

**Routing: ASSEMBLE.**
- **Assemble:** the enforcement substrate (WASI-class capability boundary), the attestation/gate-record plane
  (in-toto + witness, or its shape), the policy evaluation (OPA/Cedar), the durable-execution/structure plane.
- **Build, and only this:** (1) the non-declarative-actor bound and the demand-discovery loop that feeds it —
  note that **IAM Access Analyzer and `audit2rbac` are the closest existing pattern and both derive from
  *observed* behaviour, which is exactly the input an LLM agent can supply**; (2) the context ledger (what was
  injected, what was excluded); (3) the per-unit cost meter. That is three things, not fifty-one.
- **Which part is differentiating:** (1). It is also the only one this surface could not find prior art for.

**Caveat, stated:** I have not priced any of this, tested composability in practice, or read the licences. Scope,
cost, lock-in and exit belong to W2/W3 and I am not substituting for them — this is the *adjacent-field* answer
to "does the shape exist elsewhere," which is **yes, most of it, in a form built for a different actor.**

---

## 7. P1 — **SURVIVES** (confused-deputy cluster only), with one sharpening and a warning about its weight

**Verified.** Norm Hardy, **"The Confused Deputy (or why capabilities might have been invented)," ACM SIGOPS
Operating Systems Review 22(4), October 1988**, DOI `10.1145/54289.871709`. Exists, correctly attributed,
correctly dated. The Tymshare compiler story checks out: a compiler holding write authority to a billing file
could be induced to overwrite it by a caller who *named* that file as the output. The paper's thesis is as
claimed — **authority should travel with the invoker's designation, not sit ambiently in the deputy.**
wfh-004's L1-13 states it accurately.

**One sharpening, so the theme prose does not overclaim.** Capability systems make the *correct* pattern
expressible and make the ambient-authority variant impossible; they do **not** automatically prevent a deputy
from misusing an authority it legitimately holds on a caller's behalf, and the capability-vs-ACL debate over the
confused deputy is a live one in the literature. **"Object-capabilities solved instruction-through-data" is too
strong; "object-capabilities dissolved the ambient-authority form of it" is right.**

**And the warning, which I think is the more useful output.** This cluster is the *easiest* item in P1's ~30
references to get right: one famous 38-year-old paper with a stable DOI. **Confirming it carries almost no
information about the rest of P1** — in particular about the 2026 arXiv identifiers, which is where fabrication
risk actually concentrates. An error here would have been diagnostic; the absence of an error here is not.
**P1's real verdict belongs to W1's per-reference table and this surface should not be counted as corroboration
of it.**

---

## 8. Cold leg — the assumption nobody put on the list

### Proposed **Position 6 — the theme assumes there is a repeating, pre-declarable process to index authority against.**

This is the assumption that every adjacent-field success in §2 quietly depends on, and it is the one the theme
has never stated.

Look at *where* phase-indexed control actually worked: pharmaceutical batch records, flight operations, nuclear
surveillance intervals, DO-178C stage gates, in-toto layouts, Bazel actions. **Every one is a high-repetition
process where the same phase graph executes many times**, and the modelling cost — writing the layout, the
tech spec, the master batch record, the certification plan — is amortized over hundreds or thousands of
executions. That amortization is not incidental; it is the entire economic basis of the mechanism.

Now look at where it was tried on low-repetition knowledge work: **BPM, and it failed.** The field's own
diagnosis is on record — BPMN "is best used for well-structured and highly predictable work," and the OMG
published **CMMN (2014)** specifically for "unpredictable, knowledge-intensive and weakly-structured processes,"
abandoning sequential control flow for event-condition-action because *the order of activities cannot be known
in advance*. **CMMN is the field's formal admission that phase-indexed process control does not fit knowledge
work** — and CMMN itself is widely described as having risen and fallen. *(That last, from a vendor blog title;
unverified, flagged.)*

**Which case are we?** Our own evidence says the second. wfh-005's SCOPE carries **five declared deviations
(D-a…D-e) from the theme-scan protocol in a single run**; wfh-002 closed early after drifting; wfh-004 rebuilt
its own frame mid-run. Across five runs the phase graph has been re-authored nearly every time.

**Why this is dangerous rather than merely interesting:** if the workflow definition is re-authored per run, then
"deriving the capability set from the phase" is not a derivation at all — **it is hand-writing the ceiling, moved
one level up and renamed.** The theme's entire value proposition over WAM/TBAC (which already index to phase)
is that the derivation removes the hand-writing. If the *phase graph itself* is hand-written per execution, the
saving is zero and the phase axis buys nothing.

**Falsifier — one hour, and it should be run before Increment 1 is committed:** take the five wfh SCOPE files
plus the SDLC protocol definitions and count how many runs executed a phase graph **unchanged** from a prior
run. If the answer is near zero, the phase axis is decoration, C-32 (the phase dimension, routed build in
increment 4) is unjustified, and the theme's value-target should be the *low*-repetition case — which points at
CMMN's answer, not BPMN's, and at a very different product.

### Proposed **Position 7 — the theme assumes the definition layer is trustworthy.** *(secondary, but clean)*

In every adjacent field, the policy is authored and signed by a principal **outside the executing party**:
in-toto layouts are signed by the project owner with keys functionaries do not hold; DO-178C plans are agreed
with the certification authority; nuclear technical specifications are licensed by the regulator; GMP master
batch records are QA-approved by a role distinct from production. **The separation of policy-author from
policy-executor is universal and load-bearing, and I did not find a single counterexample.**

In the garage, the same operation authors the workflow definition, executes it, and grades the result, and the
definition is a markdown file any agent in the run can edit. wfh-004's C-127 gets adjacent to this — *"the most
load-bearing control in every workflow definition we have, and the one control with no integrity binding at
all"* — but that is about the **gate**, not about **who may write the definition**.

**The sharp form:** if the phase graph and its write-sets are authored by a principal that can also execute them,
phase-indexed authority is **self-restriction by the credential holder** — W0-c's C-4 trap, one level up, and
C-4 is explicit that this is not a weak guarantee but *not a guarantee*. **Every mechanism in P2's prior art
places the layout outside the executor's reach. Ours does not, and nobody has noticed.**

**Cold-leg dry results, reported honestly:** database transaction isolation (vocabulary only, no precedent);
maker-checker (already mined, subsumed by Clark-Wilson); clinical-trial gating (already mined by wfh-004 — the
one unmined angle, amendment base rates, I did not measure).

---

## 9. Suspected cross-surface aliases — flag only, I cannot see the other scouts

- **"phase-indexed capability derivation"** ≡ *task-based authorization / active security model / just-in-time
  permissions* (literature) ≡ *step + functionary + artifact rules in a layout* (active-dev: in-toto/witness)
  ≡ *WIT world / capability imports* (active-dev: WASI). **W1 will almost certainly surface WAM/TBAC
  independently — merge, do not double-count as two hits.**
- **"gate soundness rule"** ≡ *verification independence* (DO-178C) ≡ *certifier ≠ executor* (Clark-Wilson E4)
  ≡ *non-falsifiable provenance* (SLSA) ≡ *measure-before-execute / extend-only* (TCG). **Four names, one
  invariant.**
- **"over-granting ceiling"** ≡ *least-privilege policy generation* (products: AWS/k8s) ≡ *hermeticity*
  (active-dev: Bazel/Nix) ≡ *no ambient authority* (literature: ocap).
- **"soundness"** — **collision alert.** If W1 returns workflow-net soundness and we return gate soundness, the
  leader must not merge them. Different properties, same word.
- **"confused deputy"** — expect W1/W3 to return the 2025–26 LLM-agent restatements (prompt-injection-as-
  confused-deputy, RAG confused deputy, capability-based defences, attenuating tokens for agent delegation
  chains — I saw an IETF draft on attenuating authorization tokens for agentic delegation chains in passing).
  **Those are the same lineage arriving on the active-dev surface**, and if W3 reports them as new, they are not.
- **"comprehensive control plane displaced"** ≡ *iBPMS category retirement* (products) ≡ *CAB ineffectiveness*
  (this surface) ≡ whatever W2 finds about agent-platform governance features. Same story, three vantage points.

---

## 10. Reuse / dedup notes

`context_search` over `technology` + `finding` for phase-indexed authorization, task-based access control, and
supply-chain attestation returned **only** wfh-001 product nodes — #137 OpenHands, #140 Windsurf, #143 Copilot,
#144 Cline, #145 Factory.ai, #146 Amp, #147 Cannoli, #148 Rivet, #149 LangGraph Studio, #150 Dify — plus #186
(wfh-004 retro) and two auto-extracted convention nodes (#187, #188). Top semantic score on the
workflow-authorization query was **0.39**, on the attestation query **0.36**.

> **Nothing in this report duplicates a graph node.** The graph contains **zero adjacent-field knowledge** —
> no WAM, no TBAC, no Clark-Wilson, no in-toto, no SLSA, no ocap literature beyond what sits inside wfh-004's
> unfiled hypothesis files. That is itself a finding for the curator: the theme's entire prior-art base lives in
> markdown, not in Unimatrix, which is why three consecutive runs could argue from premises nobody had checked.

I did not check whether wfh-001's #143/#146/#150 characterizations are stale — not my surface.

---

## 11. What I could not verify

- **Primary sources not retrieved** (working from secondary explanations): Clark & Wilson 1987 (IEEE S&P);
  Vaughan 1996; Snook 2000; the SLSA v1.0 requirements page; Gartner's own iBPMS-retirement note; the macaroons
  full author list (verified Birgisson; Politz only).
- **Not searched at all:** rail interlocking, hardware sign-off flows, medical-device approval, TUF, SPKI/SDSI.
- **Reasoned from prior knowledge, not verified this run:** Kerberos constrained delegation, OAuth token
  exchange/downscoping, seccomp/AppArmor profile generation, Temporal/Camunda/Cedar/SpiceDB capability claims in
  §6's table (the in-toto/witness and WASI rows *are* search-verified).
- **The 70% BPM failure figure and the "CMMN rise and fall" framing** are practitioner/vendor claims, not
  measurements. Do not cite them at the gate as evidence.
- **Nothing here is `proven`.** Literature and vendor documentation by citation stay `claimed`, including the
  results that damage our own positions.

---

## 12. cites:

```yaml
- type: paper
  ref: https://link.springer.com/content/pdf/10.1007/3-540-61770-1_27
  title: "An Authorization Model for Workflows"
  author: "Atluri; Huang"
  year: 1996
  venue: "ESORICS"
  surface: adjacent
- type: paper
  ref: https://profsandhu.com/confrnc/ifip/i97tbac.pdf
  title: "Task-Based Authorization Controls (TBAC): A Family of Models for Active and Enterprise-Oriented Authorization Management"
  author: "Thomas; Sandhu"
  year: 1997
  venue: "IFIP TC11 WG11.3 11th Intl. Conf. on Database Security"
  surface: adjacent
- type: paper
  ref: https://dl.acm.org/doi/10.1145/54289.871709
  title: "The Confused Deputy (or why capabilities might have been invented)"
  author: "Hardy"
  year: 1988
  venue: "ACM SIGOPS Operating Systems Review 22(4)"
  surface: adjacent
- type: standard
  ref: https://github.com/in-toto/docs/blob/master/in-toto-spec.md
  title: "in-toto specification (layouts, steps, expected_materials / expected_products, inspections, artifact rules)"
  org: "in-toto (CNCF)"
  surface: adjacent
- type: repo
  ref: https://github.com/in-toto/witness
  title: "witness — pluggable framework for software supply chain risk management; embedded Rego policy over attestations"
  org: "in-toto / TestifySec"
  surface: adjacent
- type: docs
  ref: https://slsa.dev/blog/2023/05/in-toto-and-slsa
  title: "in-toto and SLSA"
  org: "SLSA / OpenSSF"
  year: 2023
  surface: adjacent
- type: docs
  ref: https://doc.coreboot.org/security/vboot/measured_boot.html
  title: "Measured Boot"
  org: "coreboot"
  surface: adjacent
- type: docs
  ref: https://trustedfirmware-a.readthedocs.io/en/v2.14.0/design_documents/measured_boot.html
  title: "Measured Boot Design"
  org: "Trusted Firmware"
  surface: adjacent
- type: docs
  ref: https://www.cs.utexas.edu/~byoung/cs361/lecture24-4up.pdf
  title: "Foundations of Computer Security, Lecture 24: The Clark-Wilson Model"
  author: "Young"
  org: "University of Texas at Austin"
  surface: adjacent
  note: "secondary source for Clark & Wilson 1987 rule E4; primary not retrieved"
- type: docs
  ref: https://afuzion.com/do-330-introduction-tool-qualification/
  title: "DO-330 Introduction — Tool Qualification"
  org: "AFuzion"
  surface: adjacent
- type: docs
  ref: https://ldra.com/do-330/
  title: "DO-330 Software tool qualification considerations: applications and implications for tool selection"
  org: "LDRA"
  surface: adjacent
- type: docs
  ref: https://www.rapitasystems.com/do178c-testing
  title: "DO-178C testing (verification independence)"
  org: "Rapita Systems"
  surface: adjacent
- type: blog
  ref: https://www.tweag.io/blog/2022-09-15-hermetic-bazel/
  title: "How to keep a Bazel project hermetic?"
  org: "Tweag"
  year: 2022
  surface: adjacent
- type: docs
  ref: https://wasi.dev/
  title: "WASI — the WebAssembly System Interface (capability-based sandbox, no ambient authority)"
  org: "WebAssembly / Bytecode Alliance"
  surface: adjacent
- type: docs
  ref: https://aws.amazon.com/blogs/security/iam-access-analyzer-makes-it-easier-to-implement-least-privilege-permissions-by-generating-iam-policies-based-on-access-activity
  title: "IAM Access Analyzer makes it easier to implement least privilege permissions by generating IAM policies based on access activity"
  org: "Amazon Web Services"
  year: 2021
  surface: adjacent
- type: repo
  ref: https://github.com/liggitt/audit2rbac
  title: "audit2rbac — autogenerate RBAC policies based on Kubernetes audit logs"
  author: "Liggett"
  surface: adjacent
- type: paper
  ref: https://theory.stanford.edu/~ataly/Papers/macaroons.pdf
  title: "Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud"
  author: "Birgisson; Politz"
  year: 2014
  venue: "NDSS"
  surface: adjacent
  note: "full author list not verified"
- type: paper
  ref: https://www.vdaalst.com/publications/p44.pdf
  title: "Verification of Workflow Nets"
  author: "van der Aalst"
  surface: adjacent
- type: standard
  ref: https://www.omg.org/cmmn/
  title: "Case Management Model and Notation (CMMN)"
  org: "Object Management Group"
  year: 2014
  surface: adjacent
- type: paper
  ref: https://arxiv.org/abs/2504.03693
  title: "Agentic Business Process Management: The Past 30 Years And Practitioners' Future Perspectives"
  author: "Vu; Klievtsova; Leopold; Rinderle-Ma; Kampik"
  year: 2025
  venue: "Responsible BPM 2025"
  surface: adjacent
- type: docs
  ref: https://dora.dev/capabilities/streamlining-change-approval/
  title: "Streamlining change approval"
  org: "DORA (Google Cloud)"
  surface: adjacent
- type: product
  ref: https://www.gartner.com/en/documents/4003462
  title: "Quick Answer: Why Has Gartner Retired the Magic Quadrant for iBPMS?"
  org: "Gartner"
  surface: adjacent
- type: paper
  ref: https://www.nspw.org/papers/2008/nspw2008-beautement.pdf
  title: "The Compliance Budget: Managing Security Behaviour in Organisations"
  author: "Beautement; Sasse; Wonham"
  year: 2008
  venue: "NSPW"
  surface: adjacent
- type: paper
  ref: https://www.nspw.org/2009/proceedings/2009/nspw2009-herley.pdf
  title: "So Long, And No Thanks for the Externalities: The Rational Rejection of Security Advice by Users"
  author: "Herley"
  year: 2009
  venue: "NSPW"
  surface: adjacent
- type: docs
  ref: https://risk-engineering.org/concept/Rasmussen-practical-drift
  title: "Rasmussen and practical drift: drift towards danger and the normalization of deviance"
  org: "risk-engineering.org"
  surface: adjacent
- type: paper
  ref: https://study.sagepub.com/system/files/Vaughan,_Diane_-_The_Normalization_of_Deviance.pdf
  title: "The Normalization of Deviance"
  author: "Vaughan"
  surface: adjacent
```

---

## 13. Compact return

| Position | Verdict | One line |
|---|---|---|
| **P2** | **FALSIFIED** (i, ii, iii, and overall) | WAM/TBAC own (i); Clark-Wilson E4 + SLSA L3 + measured boot own (ii); WASI/Bazel/Nix + IAM Access Analyzer own (iii). Residual is a **composition claim**, not an absence claim. Also: **rename "soundness"** |
| **P3** | **WOUNDED** | DO-330 permits an unqualified tool on the path **if its output is verified** — the claim is true of the *checking* leg only. And DORA/compliance-budget/drift say determinism alone doesn't survive contact with operators |
| **P5** | **WOUNDED** | The comprehensive-control-plane category was retired (iBPMS, 2021) and its enterprise gate measured net-negative (DORA). External demand exists (22 BPM practitioners) but asks for **goals, human-agent roles and fallbacks** — the cells our register scores empty |
| **P4** | **WOUNDED → ASSEMBLE** | The shelf covers security, attestation, structure and recovery. Uncovered and differentiating: **bounding an actor that cannot declare its interface**, plus cost and context ledgers. Build three things, not fifty-one |
| **P1** | **SURVIVES** (this cluster only) | Hardy 1988 verified, DOI `10.1145/54289.871709`; sharpen "solved" → "dissolved the ambient-authority form." **Carries no weight for the rest of P1** |
| **Cold leg** | **2 new positions** | **P6:** the theme assumes a repeating, pre-declarable process — every field where phase-indexation worked was high-repetition, BPM's low-repetition attempt failed and produced CMMN. **P7:** every adjacent field puts the policy author outside the executor; we do not — C-4, one level up |

**Cheapest decisive probe this surface produced:** count how many of our runs executed an unchanged phase graph.
One hour, five SCOPE files. It decides whether the phase axis — and C-32, and half of increment 4 — is worth
anything.

**Flags for the leader:**

1. **P2's falsification is the run's headline** and it did not need the literature surface to land — five unrelated adjacent fields returned *structurally identical* matches. Expect W1 to return WAM/TBAC independently; **merge, do not count twice**.
2. **Naming collision, act on it:** "soundness" is taken by workflow nets. Shipping our rule under that word guarantees a misread.
3. **P3's narrowing changes the sort key of wfh-004's entire register** — from a scalar "minimize inference" to a binary "generation leg vs checking leg." That is a bigger downstream consequence than the verdict word suggests.
4. **Round-two target for this surface: rail interlocking.** It is the declared hole I most regret, and it is plausibly the closest physical analogue to phase-indexed authority that exists.
5. **Curator note:** the graph holds zero adjacent-field knowledge (top dedup score 0.39). Nothing here duplicates a node.
