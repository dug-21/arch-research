# codex-hypotheses.md — wfh-007 independent Codex divergent pass

**Artifact identity:** `codex-wfh-007-hypothesizer`  
**Run:** `wfh-007` · `theme:workflow-harness` · Issue #64 · `wf-v0.24`  
**Phase:** hypothesize — structure only  
**Target:** Jurati Core as a provider-neutral coordination and trust substrate for independently-owned programs  
**First slice:** Unimatrix software delivery → bounded research request → Jurati-mediated work contract → research garage → evidence-graded response → contract acceptance → software delivery resumes  
**Authority:** `OWNER-DIRECTION.md` is owner-supplied constraint and working synthesis, not a research verdict or architecture decision.

Every item below is an **unproven conjecture**. Nothing is ranked, recommended, routed, or advanced toward `proven`.

## Boundary conditions carried into generation

- The “kernel” slot is the classical reference monitor and already has shipping implementations. Re-inventing isolation is spent range.
- SCOPE’s claim that neither exemplar built governance is false for ruvnet: `autogenous` contains a governance design, although the flagship workflow does not run on it.
- The second exemplar’s claimed basement stack could not be located.
- The personal-OS framing document named in SCOPE does not exist in the repository.
- The uncovered seam repeated across the scan is narrower than a general kernel: **declared task and phase → derived authority → deterministic enforcement → evidence-qualified commitment → acceptance or escalation**.
- Existing graph references are reused at their demonstrated altitude: #200 ruvnet/ruflo subtree, #202 AgentCore Policy+Cedar, #205 SPIFFE/SPIRE+Vault, #263 the partial bounded checker/reducer, #264 the inconclusive Jurati position, #256 the missing capability **Evidence-bound decision evaluation and deterministic next-action resolution**, #191 the wounded “minimize inference” position, and #196/#254 the inert-control position.
- The current capability surface is the existing repository-owned protocols, roles, skills, Git/GitHub exchange surfaces, per-project Unimatrix knowledge stores and `context_*` operations. No hypothetical current capability is assumed.
- Current inference is cloud-hosted. Provider and location neutrality are required; local inference is an incremental trajectory, not an entry condition.
- Project repositories, workflows, skills, roles, and Unimatrix instances retain local ownership unless a later architecture decision changes that.

## Hypotheses

### COD-H01 — Transport-neutral cross-program work envelope

**Statement.** A typed work-envelope format could enhance **bounded cross-program delegation** of the Unimatrix software-delivery and research-garage use cases by carrying objective, workflow/phase/role context, disclosed resources, delegated authority, evidence requirements, acceptance terms, budget, expiry, cancellation, provenance, and disposition independently of the transport used.

**Mechanism.** A canonical serialized envelope separates the semantic contract from GitHub Issues, queues, hosted runtimes, or local IPC. Adapters transport the same signed or digest-bound fields without redefining delegation and acceptance in each channel.

**Target.** Cross-program work exchange between independently-owned programs; composition of existing software-delivery protocols and the garage without merging their repositories or memories.

**Class.** obvious

**Level-up vs. linear.** Level-up: replaces owner-mediated semantic translation with a portable machine-addressable contract.

**Cheapest test.** Encode one existing bounded Unimatrix research request and its returned garage artifact in a transport-independent document; round-trip it through a GitHub Issue adapter and a local-file adapter; compare canonical digests and verify that both preserve every required field.

**Key assumption.** The common fields are stable across the two real programs without absorbing their local workflow vocabularies.

**Biggest risk.** The envelope becomes a universal workflow ontology and collapses the ownership boundary it was meant to preserve.

### COD-H02 — Attenuated work-envelope authority

**Statement.** Invocation-Bound Capability Tokens or macaroons could enhance **delegated authority for a cross-program work contract** by deriving a narrower, expiring grant from the requester’s authority and binding it to the work-envelope digest, phase, resources, and return channel.

**Mechanism.** Caveats and invocation binding make authority monotone: the called garage receives only explicitly packaged material and actions, while token verification is cheap and independent of the acting model. This reuses the shipped delegation mechanism in Cluster C rather than inventing a new credential system.

**Target.** Resource and information authority for the Unimatrix-development → research-garage invocation; existing delegation surface represented by #202/#205.

**Class.** obvious

**Level-up vs. linear.** Level-up: turns free-form inter-team requests into enforceable least-authority calls.

**Cheapest test.** Mint a token for a paper-only research request that permits reading a named artifact set and returning one report before expiry; attempt an undeclared repository write, onward delegation, replay after expiry, and access to an unlisted Unimatrix instance.

**Key assumption.** Work-envelope fields can be converted into enforceable caveats without provider-specific agent semantics.

**Biggest risk.** A sequence of individually permitted calls violates a system-level invariant; attenuation does not solve aggregation or trajectory assurance.

### COD-H03 — Phase-to-existing-credential selection

**Statement.** Commercial CD stage-role binding plus AgentCore Policy/Cedar could enhance **phase-aware external enforcement** of software delivery by selecting among pre-existing credentials and policies from declared workflow phase, without requiring Jurati to mint a novel credential type.

**Mechanism.** Spinnaker Fiat, Harness, and Azure DevOps already bind stages to roles or service connections; Cedar can deterministically authorize a call using principal, action, resource, task, and phase attributes.

**Target.** Declared workflow state, phase, role, and transitions in the existing Unimatrix software-delivery protocols; settled graph reference #202.

**Class.** adjacent

**Level-up vs. linear.** Linear for endpoint-scoped phases; potentially a level-up when coupled to a canonical work envelope.

**Cheapest test.** Map two real protocol phases to distinct existing credentials, prove that a delivery phase can push while a research phase cannot, and measure policy-decision and credential-selection overhead.

**Key assumption.** Enough meaningful authority differences map to separate endpoints, credentials, or resource attributes.

**Biggest risk.** Semantic distinctions within one credential—such as “may propose a capability but may not mutate the goal”—remain unenforceable.

### COD-H04 — Policy hot reload as an in-turn phase switch

**Statement.** OpenShell policy hot reload could enhance **fine-grained phase transition enforcement** by updating sandbox policy atomically when a workflow changes phase, while retaining the existing isolation plane.

**Mechanism.** OpenShell already intercepts filesystem, network, process, and inference access outside the model and exposes operator-controlled policy mutation. If reload is atomic and fast enough, Jurati could translate phase changes into sandbox-policy changes instead of building a new reference monitor.

**Target.** Security, workflow phase enforcement, and provider-neutral execution for the software-delivery slice.

**Class.** obvious

**Level-up vs. linear.** Level-up only if atomic reload can safely sit inside a turn; otherwise linear or unusable for this capability.

**Cheapest test.** On an instrumented sandbox, alternate two policies at phase boundaries while a hostile loop continuously attempts old and new permissions; record reload latency, atomicity, transient authorization overlap, dropped work, and audit ordering.

**Key assumption.** OpenShell exposes a stable hot-reload seam whose enforcement state changes atomically.

**Biggest risk.** No published latency or atomicity figure exists; a transient mixed-policy window would make phase binding decorative.

**Explicit round-two flag.** This directly targets the highest-value load-bearing hole in `scout-merged.md`.

### COD-H05 — Cloudflare OS package boundary as program federation

**Statement.** Cloudflare OS’s gadget/package isolation model could enhance **federated program composition** by letting each repository-owned program publish an isolated executable package with declared interfaces while Jurati coordinates packages without absorbing their local workflows or memory.

**Mechanism.** The Sandstorm-derived architecture packages applications behind isolation and capability-bearing interfaces; Cloudflare’s newer implementation may remove much of Sandstorm’s historical porting burden.

**Target.** Domain/program packages, repo ownership, extensibility, and the open topology question for Jurati Core.

**Class.** adjacent

**Level-up vs. linear.** Level-up if a new program can join without central workflow rewriting; linear if it is merely another container format.

**Cheapest test.** Package a minimal software-delivery requester and a read-only garage responder as two gadgets; exchange only a work-envelope reference and evidence artifact; identify every place local definitions must be rewritten or centralized.

**Key assumption.** Cloudflare OS retains meaningful interface/capability properties beyond its README-level presentation.

**Biggest risk.** The twelve-day-old project may hide the same integration and porting costs that killed prior personal-OS attempts.

**Explicit round-two flag.** Requires a source-depth pass; current evidence is README-only.

### COD-H06 — Consequence-typed action declaration

**Statement.** The *Revisable by Design* taxonomy combined with Apple App Intents-style action metadata could enhance **human steering and safe execution** by assigning each typed action an idempotent, reversible, compensable, or irreversible consequence class that controls approval, recovery, and evidence requirements.

**Mechanism.** A formally characterized consequence taxonomy supplies the semantics; a typed action manifest supplies machine-readable declarations at registration time; external policy maps consequence class to required owner gates and compensation plans.

**Target.** Typed actions, irreversibility and consequence, owner approval for spending/public representation, and recovery/durability across programs.

**Class.** obvious

**Level-up vs. linear.** Level-up: separates consequence from generic permission and makes recovery/approval policy composable.

**Cheapest test.** Classify ten real actions from software delivery and the garage, including push, issue comment, dependency purchase, knowledge correction, and file deletion; run adversarial cases where the author under-declares consequence and measure whether independent metadata can detect the mismatch.

**Key assumption.** Useful consequence classes can be assigned without solving arbitrary program semantics.

**Biggest risk.** Apple and MCP demonstrate the same weakness: self-declared annotations are not trustworthy enforcement inputs.

### COD-H07 — Independent consequence-declaration verification

**Statement.** A constrained effects/capture checker could enhance **consequence-typed policy** by deriving a conservative effect envelope from code or tool schemas and rejecting action declarations that claim less consequence than their reachable effects.

**Mechanism.** Capability-safe language techniques and step-level enforcement restrict or infer what an action can capture; the checker compares derived filesystem/network/process/resource effects with the declared consequence class before registration.

**Target.** Effectiveness verification, typed actions, and the inert-control problem represented by #196/#254.

**Class.** non-obvious

**Level-up vs. linear.** Level-up if declarations become checked inputs rather than promises.

**Cheapest test.** Define a closed action subset with read, append, overwrite, delete, network-send, and payment-stub effects; intentionally mislabel implementations and measure false acceptance, false rejection, and escape through dynamic calls.

**Key assumption.** A useful first-slice action surface can be closed enough for conservative checking.

**Biggest risk.** General capability safety is undecidable or intractable; dynamic tools may force declarations so broad that the mechanism loses value.

### COD-H08 — Evidence-kind floor at commit time

**Statement.** The PCAOB/ISA ordered evidence hierarchy combined with #263’s bounded checker/reducer could enhance capability **#256, Evidence-bound decision evaluation and deterministic next-action resolution**, by preventing a durable decision or completion claim when its declared evidence kind falls below the action-specific floor.

**Mechanism.** A small ordinal lattice names evidence kinds, comparative strength, insufficiency floors, and contradiction handling; the deterministic checker consumes typed evidence references and produces admit, reject, or escalate without relying on the acting model’s confidence.

**Target.** Capability #256; evidence-qualified decisions and durable commitments in both software delivery and the research garage.

**Class.** obvious

**Level-up vs. linear.** Level-up: moves evidence grading from retrospective description to a write precondition.

**Cheapest test.** Add a closed evidence lattice to the existing #263 checker/reducer and replay a small corpus containing assertion-only completion, test output, independent artifact inspection, contradictory artifacts, and missing provenance; use fixed expected results rather than semantic LLM judging.

**Key assumption.** Kinded ordinal evidence is sufficient for the first slice without quantified confidence.

**Biggest risk.** Evidence kind alone does not establish that the evidence actually supports the claim; jurati-001’s semantic-scoreability failure remains unresolved.

### COD-H09 — Digest-bound evidence package without a new log

**Statement.** in-toto predicates and DSSE could enhance **evidence-qualified cross-program return** by binding evidence kind, work-envelope identity, artifact digest, producer/runtime provenance, and acceptance-relevant metadata into a verifiable package, while reusing an existing transparency service rather than building one.

**Mechanism.** `predicateType` declares the evidence schema, DSSE authenticates type and payload, and digest binding prevents artifact substitution. A transparency-log reference can add inclusion evidence where warranted.

**Target.** Evidence and provenance on the garage → software-delivery return; graph reference #190 as settled base.

**Class.** obvious

**Level-up vs. linear.** Linear alone; a level-up when it becomes an input to COD-H08’s deterministic commit check.

**Cheapest test.** Package one garage report and its source manifest as an in-toto statement, alter the report, predicate type, runtime provenance, and request identifier independently, and verify rejection without storing payloads in Jurati.

**Key assumption.** Existing attestation formats can carry proposition-shaped research evidence without misleadingly equating supply-chain attestation with auditor attestation.

**Biggest risk.** Authenticity of a weak or irrelevant assertion may be mistaken for evidential sufficiency.

### COD-H10 — Bitemporal evidence-qualified commitment

**Statement.** Bitemporal records combined with digest-bound attestations could enhance **correction, supersession, and audit across project memories** by retaining both when a proposition was valid in its source program and when Jurati or the second brain learned, accepted, corrected, or withdrew it.

**Mechanism.** Valid time and transaction time preserve distinct histories; authenticated evidence packages bind each state transition to origin and declared evidence; corrections append rather than silently rewrite.

**Target.** Governed memory, provenance, correction, second-brain elevation, and cross-program acceptance.

**Class.** non-obvious

**Level-up vs. linear.** Level-up: makes later correction and source divergence representable without centralizing memories.

**Cheapest test.** Model one finding that is accepted by software delivery, corrected in the garage, and later superseded in an elevated owner store; query “what was believed when,” “what source said when,” and “what is current” under clock skew and delayed delivery.

**Key assumption.** Cross-instance references and signed transitions are sufficient; Jurati need not own the knowledge payload.

**Biggest risk.** Bitemporality × attestation is explicitly an open combination, and Rekor v2’s removal of integrated time weakens naive designs.

### COD-H11 — Governed second-brain publication

**Statement.** A publication-style elevation contract could enhance **cross-project reusable knowledge** by nominating a project-local entry, checking provenance/evidence/sensitivity, retaining its source identity, and authorizing a reference or copy into a separate owner-controlled Unimatrix instance.

**Mechanism.** Elevation is treated as a typed, evidence-qualified, information-flow-controlled action rather than automatic aggregation. Existing `context_*` correction and graph-reference behavior remains local; Jurati carries the publication contract and disposition.

**Target.** Second-brain elevation while preserving separate Unimatrix instances and repository ownership.

**Class.** adjacent

**Level-up vs. linear.** Level-up: enables cross-project learning without constructing one undifferentiated memory pot.

**Cheapest test.** Select three existing entries—one reusable engineering lesson, one project-private operational fact, and one corrected finding—and exercise nominate, approve, reject, correct-at-source, and delete-at-source behaviors across two test instances.

**Key assumption.** A small common publication vocabulary can coexist with different local ontologies and grades.

**Biggest risk.** Copy/reference semantics, deletion, contradiction, and evidence-grade translation may require an architecture decision that this scan is not authorized to make.

### COD-H12 — Provider/runtime guarantee profiles

**Statement.** Explicit provider/runtime guarantee profiles could enhance **model-, provider-, and location-neutral execution** by exposing which enforcement, identity, tool restriction, retention, data-use, replay, and provenance guarantees each Claude, Codex, Gemini, hosted, or local adapter actually supplies.

**Mechanism.** Jurati plans against normalized required guarantees rather than provider conversation formats. An adapter declares guarantees and gaps; deterministic admission rejects assignments whose required guarantees exceed the adapter profile.

**Target.** Provider/runtime adapters, incremental locality, and policy portability across the owner-controlled estate.

**Class.** obvious

**Level-up vs. linear.** Level-up: provider substitution becomes a checked compatibility decision rather than a workflow rewrite.

**Cheapest test.** Describe two current cloud coding-agent runtimes and one local stub against a closed guarantee schema; route the same read-only and write-capable work envelopes and verify that unsupported guarantees fail closed.

**Key assumption.** Guarantees can be stated behaviorally and verified independently of vendor marketing.

**Biggest risk.** Profiles become self-asserted controls; the open SDK tool-restriction bug demonstrates that declared restrictions may be inert.

### COD-H13 — Structural control-effectiveness probes

**Statement.** Continuous negative probes could enhance **introspection and control effectiveness** by exercising forbidden actions through the same runtime paths used by agents and withholding trust expansion when configured controls do not actually deny them.

**Mechanism.** Canary work envelopes invoke harmless sentinel resources for filesystem, network, credential, tool, and policy-mutation denials. Results are independently recorded and compared with declared policy, detecting default-open exemptions, unreachable permission systems, and miscalibrated monitors.

**Target.** Introspection, security, self-improvement, trust graduation, and #196/#254’s inert-control class.

**Class.** adjacent

**Level-up vs. linear.** Level-up: policy presence is separated from policy effectiveness.

**Cheapest test.** Build five harmless denial probes against the current coding-agent surface, including the known subagent tool-restriction path; run them before and after a workflow phase transition and record discrepancies.

**Key assumption.** Sentinel probes exercise the same enforcement seams as consequential work.

**Biggest risk.** Passing known probes creates false assurance against untested paths or runtime rug pulls.

### COD-H14 — Owner-authored trust graduation dossier

**Statement.** An append-only trust dossier could enhance **progressive autonomy** by presenting the owner with all eligible successes, denials, failures, interventions, near misses, reversals, control-probe results, and the precise incremental authority requested after at least twenty same-class runs.

**Mechanism.** Run records are grouped by action and consequence class; eligibility rules prevent incomparable successes from padding the count; only the owner may activate a policy change, while agents may generate a recommendation and evidence package.

**Target.** Human steering, trust graduation, autonomous/decision/event-triggered work distinctions.

**Class.** obvious

**Level-up vs. linear.** Linear in authority but level-up in auditability and resistance to success-only reporting.

**Cheapest test.** Construct a synthetic twenty-five-run history containing mixed outcomes and ask the system to produce a recommendation dossier; verify that failures and near misses cannot be omitted and that no policy activation occurs.

**Key assumption.** Action/consequence classes can be defined tightly enough for run comparability.

**Biggest risk.** The dossier optimizes presentation rather than truth, or reviewer fatigue turns owner activation into a rubber stamp.

### COD-H15 — Reviewer-throughput governor

**Statement.** Queueing and throughput controls could enhance **fleet supervision** by matching machine work production to available independent review capacity, limiting work-in-progress, aging, and autonomous fan-out before stale or unreviewed output accumulates.

**Mechanism.** A review-token budget, queue-age limits, explicit reviewer assignment, and admission control throttle new work when review debt exceeds policy. Unlike a generic cost budget, the scarce resource is qualified review attention.

**Target.** Reviewer/review-throughput matching, cost transparency, human steering, recovery, and the measured ruvnet/Home Assistant bottleneck.

**Class.** obvious

**Level-up vs. linear.** Level-up: changes the controlling resource from agent throughput to validated throughput.

**Cheapest test.** Replay ruvnet’s reported 80-night/4-adoption pattern through a queue simulator with review capacity, WIP limits, stale-work expiry, and priority classes; compare undetected stale work and completed accepted work.

**Key assumption.** Review work can be estimated and assigned before generation begins.

**Biggest risk.** Aggressive throttling suppresses valuable exploration, while weak estimates merely move the blind spot into queue metadata.

### COD-H16 — Selective deterministic acceptance before human review

**Statement.** Contract-specific deterministic acceptance checks could enhance **reviewer throughput** by automatically accepting mechanically decidable parts of a returned work package and routing only semantic residue or contradictions to an independent verifier or owner.

**Mechanism.** The work envelope declares acceptance predicates such as file existence, schema validity, digest match, test result, citation-field completeness, budget compliance, and scope boundaries. The requester’s checker—not the producer—evaluates them.

**Target.** Cross-program acceptance, capability #256, reviewer throughput, and gate-input independence.

**Class.** adjacent

**Level-up vs. linear.** Level-up if it materially reduces human review while preserving independent acceptance.

**Cheapest test.** Define acceptance predicates for one bounded garage report, inject missing citations, scope expansion, digest mismatch, unsupported claims, and a semantically wrong but schema-valid answer; measure which defects are caught and which remain for review.

**Key assumption.** A meaningful fraction of acceptance can be expressed without semantic LLM judging.

**Biggest risk.** Schema-valid but substantively false output passes, recreating jurati-001’s unresolved semantic premise at a different layer.

### COD-H17 — Software-delivery → garage → software-delivery round trip

**Statement.** Combining a work envelope, attenuated grant, evidence package, and requester-owned acceptance checker could enhance **bounded uncertainty resolution in software delivery** by completing one real round trip through the existing garage without the owner manually translating intent, evidence, or disposition.

**Mechanism.** The delivery workflow emits a request from a declared phase; Jurati mediates transport and authority; the garage runs its existing protocol and returns evidence references; the requesting workflow evaluates declared acceptance terms and resumes, escalates, or rejects.

**Target.** The owner-named first cross-program demonstration using the existing Unimatrix software-delivery protocols and research garage.

**Class.** obvious

**Level-up vs. linear.** Level-up: demonstrates composition of independently-owned programs rather than a single-program harness.

**Cheapest test.** Choose one small real Unimatrix enhancement with a bounded technology uncertainty and no implementation spend; run the full paper-and-adapter exchange through a GitHub Issue while preserving a transport-neutral canonical contract.

**Key assumption.** A real enhancement can be chosen whose research question and acceptance terms are narrow enough for a directional first demonstration.

**Biggest risk.** The GitHub Issue accidentally becomes the semantic protocol, or a hand-curated demonstration hides missing identity, cancellation, retry, and disclosure behavior.

### COD-H18 — Program-owned workflow registration by digest

**Statement.** Content-addressed workflow-package registration could enhance **federated composition** by allowing each repository to retain its own roles, workflows, skills, and protocol files while publishing a signed manifest of callable entry points and required guarantees to Jurati.

**Mechanism.** Jurati stores identity, digest, interfaces, and compatibility metadata rather than owning the workflow definitions. A request selects a registered package version; execution resolves the package from its owning repository and binds the exact digest into the work envelope.

**Target.** Structure, context provisioning, repo ownership, domain/program packages, and provider neutrality.

**Class.** adjacent

**Level-up vs. linear.** Level-up: shared coordination without a monorepo or global workflow registry that owns definitions.

**Cheapest test.** Manifest one software-delivery protocol and one garage protocol from their current repository paths; invoke them by versioned entry point, then change a local file and verify that the old digest cannot silently execute as the registered version.

**Key assumption.** Callable interfaces can be declared without centralizing the internal workflow ontology.

**Biggest risk.** Dependency resolution, schema evolution, and transitive skills turn the manifest into a package manager and recreate the porting wall.

### COD-H19 — Personal secret relationship broker as extensibility infrastructure

**Statement.** An adapter over an existing secret store plus provider-side credential injection could enhance **program extensibility** by letting a new program request a scoped credential relationship without receiving the underlying personal secret or requiring the program author to own every third-party OAuth registration.

**Mechanism.** A central owner-controlled integration service holds provider relationships, while OpenShell-style providers strip caller credentials and inject backend credentials under an expiring work-envelope-bound grant. Vault/SPIRE or a personal-scale secret store supplies existing storage and identity primitives.

**Target.** Secret use, new-program onboarding, attenuated delegation, and provider/location-neutral execution; reuse #205.

**Class.** adjacent

**Level-up vs. linear.** Level-up for adding independently-authored programs; linear for secret storage itself.

**Cheapest test.** Give a garage task access to one read-only external API through injected credentials; verify that neither task payload, model context, logs, nor returned artifact reveals the credential, and revoke access mid-run.

**Key assumption.** The owner or integrating service can sustainably hold third-party credential relationships.

**Biggest risk.** The service becomes the ecosystem bottleneck Thingpedia exposed, or existing personal secret products cannot express expiring, phase-indexed grants.

### COD-H20 — Trajectory guard over individually permitted actions

**Statement.** A stateful trajectory policy could enhance **aggregation safety** by evaluating the cumulative sequence of otherwise permitted actions against resource, information-flow, spending, publication, and consequence invariants.

**Mechanism.** Each accepted action advances a compact deterministic state machine keyed to the work contract; policy considers totals, combinations, disclosure paths, and irreversible thresholds rather than authorizing calls independently.

**Target.** Security, cost management, information flow, public representation, spending, and cross-domain aggregation.

**Class.** non-obvious

**Level-up vs. linear.** Level-up: addresses the surviving hard problem that per-call attenuation does not touch.

**Cheapest test.** Create sequences where every action is individually allowed but the aggregate exfiltrates a protected fact, exceeds a budget, reconstructs a sensitive profile, or incrementally publishes an owner position; test whether a small state machine blocks before the invariant is crossed.

**Key assumption.** High-value aggregate invariants can be enumerated for the first slice without general information-flow theorem proving.

**Biggest risk.** State explosion and false positives make the guard expensive or cause operators to disable it, repeating the inert-control pattern.

### COD-H21 — Compensation-first recovery contract

**Statement.** Typed compensation metadata plus append-only action receipts could enhance **recovery and durability** by requiring reversible and compensable actions to name and preflight their inverse or compensating operation before execution.

**Mechanism.** Consequence class controls the contract: idempotent actions carry a replay key; reversible actions name an inverse; compensable actions name a bounded compensator; irreversible actions require escalation. Signed receipts bind the executed action, result, and recovery handle.

**Target.** Recovery, deletion protection, durable-knowledge safety, event-triggered execution, and consequence-aware owner gates.

**Class.** non-obvious

**Level-up vs. linear.** Level-up: recovery becomes part of authorization rather than a post-failure hope.

**Cheapest test.** Exercise create/update/delete operations against disposable Git and Unimatrix fixtures; inject failures between effect and receipt, test retry, inverse, compensation, and escalation behavior.

**Key assumption.** The first-slice effects have reliable inverses or compensators.

**Biggest risk.** Declared compensation may fail precisely when needed, and false reversibility labels could lower approval barriers for consequential actions.

### COD-H22 — Public-representation policy as a distinct effect plane

**Statement.** A separate external-representation effect class could enhance **owner-controlled public action** by distinguishing private work, factual machine-generated status, proposed text, and speech attributable to the owner across Issues, pull requests, comments, email, and publishing.

**Mechanism.** Typed channel/action metadata and owner policy determine whether content may be drafted, posted under a machine identity, or posted as the owner. Work-envelope provenance and evidence requirements travel with the proposed communication.

**Target.** Human steering, information flow, typed actions, public representation, and provider-independent channel adapters.

**Class.** non-obvious

**Level-up vs. linear.** Level-up: separates “can call API” from “may represent the owner,” which generic IAM cannot express.

**Cheapest test.** Classify and route a matrix of GitHub actions—private draft, machine-labelled status comment, factual test result, recommendation, and owner opinion—through a mock policy engine and verify escalation boundaries.

**Key assumption.** Representation altitude can be encoded more reliably than arbitrary semantic truth.

**Biggest risk.** Content meaning remains semantic; a formally permitted factual update may imply an unauthorized opinion or commitment.

### COD-H23 — Event-triggered execution with authority snapshots

**Statement.** Event envelopes carrying identity, source, policy version, permitted objective, expiry, and cancellation semantics could enhance **safe proactivity** by initiating bounded workflows without granting an always-on agent ambient authority.

**Mechanism.** Events are untrusted inputs. Deterministic policy maps an authenticated event and current owner policy to a work envelope and authority snapshot; the resulting run cannot exceed that snapshot even if policy or event content later changes.

**Target.** Always-on/proactivity, supervision, cancellation, events, and incremental autonomy on hardware the owner already owns.

**Class.** adjacent

**Level-up vs. linear.** Level-up: proactivity becomes bounded event admission rather than permanent listening plus ambient authority.

**Cheapest test.** Feed authenticated, replayed, expired, malformed, and adversarial GitHub events into a read-only workflow; verify deduplication, bounded authority, cancellation, and lack of direct policy mutation.

**Key assumption.** Useful proactive behavior can begin from existing event sources without dedicated always-listening hardware.

**Biggest risk.** Prompt injection and tool rug pulls occur after event admission; an authority snapshot does not guarantee safe data flow inside the run.

### COD-H24 — Review-capacity-aware autonomous scheduling

**Statement.** An admission controller combining spend budget, consequence class, expected evidence burden, and available reviewer capacity could enhance **cost transparency and self-improvement** by scheduling only work whose downstream validation can be afforded.

**Mechanism.** Each proposed run estimates production cost and review/evidence cost separately. The controller reserves reviewer capacity before launch, expires unreviewable work, and feeds observed estimate error back into later admission without automatically expanding authority.

**Target.** Cost management, reviewer throughput, autonomous work, and the loop-engineering operating model.

**Class.** non-obvious

**Level-up vs. linear.** Level-up: optimizes accepted, reviewed outcomes rather than raw generated output or token spend.

**Cheapest test.** Replay a mixed queue of research, code, and maintenance tasks under fixed model and reviewer budgets; compare generated, reviewed, accepted, stale, and abandoned counts with a token-only scheduler.

**Key assumption.** Evidence and review burden can be estimated early enough to affect admission.

**Biggest risk.** Estimates systematically disfavor novel work whose evidence burden is uncertain, shrinking the garage’s wide mouth.

## Compact inventory

| ID | Statement shorthand | Class | Target |
|---|---|---|---|
| COD-H01 | Transport-neutral work envelope | obvious | cross-program coordination |
| COD-H02 | Work-bound attenuated authority | obvious | delegation and information authority |
| COD-H03 | Phase selects existing credentials | adjacent | phase-aware enforcement |
| COD-H04 | OpenShell hot reload as phase switch | obvious | in-turn external enforcement |
| COD-H05 | Cloudflare OS package federation | adjacent | independently-owned program composition |
| COD-H06 | Consequence-typed actions | obvious | irreversibility, approval, recovery |
| COD-H07 | Independent effect/declaration checker | non-obvious | control effectiveness |
| COD-H08 | Evidence-kind floor at commit | obvious | capability #256 |
| COD-H09 | Digest-bound evidence return | obvious | garage-to-delivery provenance |
| COD-H10 | Bitemporal authenticated commitment | non-obvious | correction and cross-memory history |
| COD-H11 | Second-brain publication contract | adjacent | governed memory elevation |
| COD-H12 | Provider/runtime guarantee profiles | obvious | provider and location neutrality |
| COD-H13 | Structural negative control probes | adjacent | #196/#254 effectiveness |
| COD-H14 | Owner-authored trust dossier | obvious | trust graduation |
| COD-H15 | Reviewer-throughput governor | obvious | review-capacity matching |
| COD-H16 | Selective deterministic acceptance | adjacent | review throughput and #256 |
| COD-H17 | Delivery→garage→delivery round trip | obvious | first cross-program slice |
| COD-H18 | Digest-registered local workflows | adjacent | federated workflow ownership |
| COD-H19 | Secret relationship broker | adjacent | extensibility and scoped secrets |
| COD-H20 | Stateful trajectory guard | non-obvious | aggregation safety |
| COD-H21 | Compensation-first recovery | non-obvious | recovery and durability |
| COD-H22 | External representation effect plane | non-obvious | owner speech/public action |
| COD-H23 | Event authority snapshots | adjacent | bounded proactivity |
| COD-H24 | Review-capacity-aware scheduling | non-obvious | cost and accepted throughput |

**Novelty counts:** obvious 10 · adjacent 8 · non-obvious 6 · total 24.

## Coverage-grid mapping

Legend: hypothesis IDs show generated coverage; `HOLE` means this bounded pass cannot responsibly populate the cell from the available characterization.

| Dimension | Cross-domain transplant | Constraint inversion | Adversarial / failure mode | Scale extrapolation | Incumbent gap | Minimality |
|---|---|---|---|---|---|---|
| Structure | H05, H18 | H01, H18 | H05 | H05, H18 | H01 | H01, H17 |
| Context provisioning | H01, H18 | H12 | H12 | H18 | H12 | H01 |
| Security | H02, H06, H20 | H03, H04 | H07, H13, H20, H23 | H20 | H04, H19 | H03 |
| Introspection | H09, H13 | H13 | H13 | H14 | H12 | H13 |
| Cost transparency and management | H15, H24 | H24 | H15 | H15, H24 | H24 | H16 |
| Self-improvement | H13, H14 | H14 | H13 | H14 | H13 | H14 |
| Recovery and durability | H10, H21 | H21 | H10, H21 | H10 | H21 | H21 |
| Human steering | H06, H14, H22 | H23 | H14, H22 | H15 | H22 | H14 |
| Irreversibility and consequence | H06, H21 | H21 | H07 | H06 | H06 | H06 |
| Domain vocabulary | H06, H18 | H01 | H07 | H18 | H07 | H01 |
| Person model | **HOLE** | **HOLE** | H22 only at representation boundary | **HOLE** | **HOLE** | **HOLE** |
| Always-on and proactivity | H23 | H23 | H23 | H23 | H23 | H23 |
| Reviewer/review-throughput matching | H15, H16, H24 | H15 | H16 | H15, H24 | H15 | H16 |
| Cross-program coordination | H01, H02, H17 | H01 | H02, H16 | H05, H18 | H01 | H17 |
| Provider/location neutrality | H12 | H12 | H12, H13 | H12 | H12 | H12 |
| Governed memory elevation | H10, H11 | H11 | H10 | H11 | H11 | H11 |

## Explicit coverage holes

1. **Person model remains a genuine hole.** None of the five scout surfaces characterized a mechanism for a durable owner model, preference model, identity continuity model, or conflict between present and past owner intent. H22 touches representation authority only and must not be counted as filling this dimension.
2. **Semantic evidential support remains unresolved.** H08/H16 can check evidence kind and mechanical acceptance, but neither establishes that an artifact semantically supports a claim. Capability #256 remains `grade:missing`; #263 remains bounded and `partial`; #264 remains inconclusive.
3. **Aggregation is characterized but not solved.** H20 names a bounded state-machine experiment, not a general solution to trajectory assurance or information-flow aggregation.
4. **Cross-instance deletion and correction semantics remain under-characterized.** H10/H11 expose the question; the current scout material does not determine copy versus reference behavior.
5. **Program/team principal identity remains open.** H01/H02 can carry either stable or per-objective principals; the available evidence does not select one.

## Load-bearing round-two flags

These are characterization gaps that could change later triage routing; they are not verdicts.

1. **OpenShell policy hot-reload latency and atomicity.** Required for COD-H04. No published figure supports an in-turn claim.
2. **Cloudflare OS at source depth.** Required for COD-H05. README evidence cannot establish its package boundary, policy semantics, porting cost, or suitability as a program-composition substrate.
3. **Commercial CD stage-scoped role binding is closed as a prior-art hole.** COD-H03 uses the narrower gap: incumbents bind phase to pre-existing credentials, not declared demand to a freshly derived semantic ceiling.
4. **`autogenous` source verification.** Current structural guarantees are maintainer assertions and the related flagship policy plane was inert by default.
5. **Manifest V3 developer attrition.** This bears directly on H18/H19.
6. **OpenClaw ecosystem.** Large and independently corroborated, but unread; it may alter range.
7. **Runtime rug pulls.** H07/H13/H20 only partially touch this possible fourth failure class.
8. **Patent prior art and rail interlocking.** Both remain unread method holes.

## Instrument and evidence flags

- All five scouts hit a **shared 200/200 WebSearch cap**. This bounded scan covered all staffed surfaces but did not exhaust any surface.
- The cap biases evidence toward guessable canonical URLs and against small projects, practitioner post-mortems, and emergent vocabulary. Thin cells are not evidence of territorial absence.
- “Attestation” remains split: supply-chain attestation binds a predicate to an artifact digest; auditor attestation is an opinion on an assertion.
- Local inference is not treated as a missing prerequisite. H12 tests portability across present cloud and future controlled/local runtimes.
- GitHub Issues are treated as an adapter and human-visible surface in H01/H17, never as the semantic work protocol.
- No hypothesis assumes that twenty successful runs grants authority. H14 preserves owner-only activation.
- No hypothesis merges program memories or workflow definitions. H10/H11/H18 preserve local ownership.
- No graph write, status change, design decision, proof claim, triage verdict, or implementation recommendation is made here.
