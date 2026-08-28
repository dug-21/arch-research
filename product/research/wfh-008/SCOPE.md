# wfh-008 — MetaHarness architecture and ecosystem dependency analysis

**Status:** done
**Goal(s):** workflow-harness — inform the smallest defensible personal-OS/Jurati substrate (primary)
**Capability target(s):** proposed `jurati-arch-002` — technology findings for its architecture proposal; no Unimatrix capability id or grade is advanced by this scope
**Confidence-required:** directional
**Phase / area:** workflow-harness · technology due diligence · Jurati architecture input
**Cycle topic / Issue:** `wfh-008` · [Issue #66](https://github.com/dug-21/arch-research/issues/66)

---

## The question

What is the complete static architecture of `ruvnet/metaharness` as it exists at the research cutoff,
including its component and dependency boundaries, its direct and transitive dependence on `ruvnet/ruflo`
and the wider `ruvnet` ecosystem, and the generated-output and runtime relationships that are not obvious
from package manifests alone? Which parts are credible extraction or reuse seams for proposed
`jurati-arch-002`, what upgrade, drift, security, and authority liabilities accompany them, and what does
this repository-level evidence change relative to wfh-005 and wfh-007?

> Which MetaHarness mechanisms are independently reusable for Jurati, and which are inseparable from its ruflo/ruvnet runtime, generation pipeline, or same-authority security model?  Also look for good concepts (for some reason the direct CODE may not be reusable, but the concept is solid and should be replicated)

## Why it matters

MetaHarness is already on the workflow-harness watchlist and superficially overlaps Jurati's desired
control-plane substrate. A complete dependency- and boundary-level account can prevent both rebuilding a
usable mechanism and adopting a component whose apparent boundary disappears once generated artifacts,
runtime loading, ecosystem coupling, or authority placement are traced. The result is technology input to
the proposed `jurati-arch-002`; it does not ratify that architecture or authorize adoption or implementation.

## Known constraints & prior art  *(build on these — do not re-derive)*

- **Fixed target and cutoff:** one target, `ruvnet/metaharness`, assessed as it exists at the run's recorded
  checkout/commit. The owner gist and repository are primary materials:
  [garage proposal gist](https://gist.github.com/ruvnet/7368405b5882a194df567d466818679b) and
  [`ruvnet/metaharness`](https://github.com/ruvnet/metaharness). Record the exact commit and retrieval date
  in every workstream that reads the checkout.
- **No external cost and no compute:** deep static analysis only. Reading, cloning, indexing, and local
  deterministic inspection are allowed; installation, builds, test execution, benchmarks, services,
  agents, models, containers, and generated-code execution are not. Do not infer runtime success from
  source presence.
- **Reuse wfh-005:** `product/research/wfh-005/scout-active-dev-r2.md` already characterizes MetaHarness,
  ruflo, agentic-flow, CASA integration, permission generation, the in-process `PolicyGate`, witness
  machinery, ecosystem maturity, and doc/code gaps. Its claims are baselines to confirm, revise, or mark
  outside the current cutoff—not topics to rediscover. Reuse the final verdict and reconciliation in
  `product/research/wfh-005/reports/triage.md` and both triage amendments.
- **Reuse wfh-007:** its scope, scouts, verification artifacts, and reports already establish the Jurati
  frame for contract/phase structure, derived authority, evidence acceptance, federation, autonomy,
  gate-input independence, delegation/attenuation, control-plane custody, and evidence grading. This run
  maps MetaHarness against that frame; it does not repeat the landscape or proof work.
- **Evidence firewall:** label every material statement as one of: **source claim** (documentation, ADR,
  comment, name, or marketing assertion), **static code evidence** (a traced authored/generated code or
  configuration path), **prior demonstrated evidence** (an artifact demonstrated by an earlier run), or
  **unverified/inference**. Static code evidence can establish structure and reachable-looking paths; it
  cannot establish that the path executes correctly. Nothing produced here is demonstrated-by-us evidence.
- **License and provenance are dependencies:** record repository/package/crate licensing and provenance
  where they affect extraction or reuse. Absence or ambiguity is a constraint, not permission.
- **Unimatrix:** researchers may read current knowledge to reuse it, but perform no Unimatrix writes. Only
  the curator may later distill this run, and directional research cannot advance a technology to `proven`.

## Bounded investigation (workstreams)

Each workstream owns a distinct ledger and hands cross-boundary references to the owning workstream rather
than duplicating analysis. All outputs cite repository-relative paths plus commit-pinned source URLs where
available, and carry the evidence label above.

- **W1 — Repository architecture and component boundaries.** Enumerate every first-party workspace,
  package, crate, application, service, CLI, plugin, host adapter, registry, schema, build/configuration
  surface, and top-level execution entrypoint. Identify ownership boundaries and authored versus vendored
  or generated material, but leave edge enumeration to W2 and behavioral/security judgments to W4/W6.
  *Output:* `findings-W1.md` with a canonical component inventory, boundary/topology map, entrypoint table,
  and a completeness ledger accounting for every top-level and workspace-owned component.
- **W2 — Complete dependency graph.** Resolve all first-party edges and all declared direct/transitive
  third-party dependencies from workspace manifests, lockfiles, build metadata, imports/re-exports, dynamic
  loading declarations, optional/peer/dev dependencies, native/WASM bindings, and artifact references.
  Classify build-time, development-only, generation-time, and runtime reachability without claiming that a
  statically reachable path ran. W3 exclusively owns ecosystem interpretation of `ruvnet` edges.
  *Output:* `findings-W2.md` with machine-readable-or-tabular nodes/edges, dependency classes, unresolved
  dynamic edges, cycles, roots/leaves, and per-component direct/transitive closure summaries.
- **W3 — ruflo and wider ruvnet ecosystem coupling.** Trace every direct and transitive reference or
  dependency from MetaHarness to `ruvnet/ruflo` (including legacy `claude-flow` identities),
  `agentic-flow`, and any other `ruvnet` repository, package, crate, hosted asset, copied protocol/schema,
  generated configuration, command, environment variable, network endpoint, or documentation-imposed
  operational prerequisite. Distinguish code-enforced dependency from naming, provenance, optional
  integration, and source claim; do not survey unrelated ruvnet repositories.
  *Output:* `findings-W3.md` with an exhaustive ruvnet-reference ledger, direct/transitive ecosystem graph,
  version/provenance evidence, and a coupled/replaceable/optional/claim-only classification for each tie.
- **W4 — Generation pipeline and runtime composition.** Statically trace generators from inputs and
  templates through emitted files, registries, manifests, host configuration, packaged distributions, and
  runtime consumers. Identify checked-in generated output, late binding, filesystem/process/network
  assumptions, host-owned prerequisites, and dependencies introduced only after generation or deployment.
  Do not execute generators or validate behavior.
  *Output:* `findings-W4.md` with producer→artifact→consumer chains, generated/authored boundaries,
  runtime-loading map, hidden prerequisites, and source-claim versus static-path reconciliation.
- **W5 — Extraction seams, upgrade mechanics, and drift.** Starting from W1–W4 inventories, assess each
  plausible reusable unit at its smallest coherent boundary: required files/APIs, dependency closure,
  state/config contracts, licensing, replacement points, version pins/ranges, migrations, compatibility
  promises, release/update automation, duplicated schemas or generated copies, and drift detection or lack
  thereof. Do not recommend adoption or design Jurati.
  *Output:* `findings-W5.md` with extraction dossiers, minimum dependency closures, seam quality,
  upgrade/drift failure modes, and bounded options (`reuse candidate`, `reference only`, `inseparable`, or
  `insufficient evidence`) with the determining constraint for each.
- **W6 — Security and authority boundary.** Trace where identities, credentials, policies, permissions,
  approvals, envelopes, risk decisions, witness/trust material, process boundaries, and enforcement calls
  originate and where they are consumed. For each asserted gate, identify the decision point, protected
  operation, read/write sets, bypass/configuration paths, default mode, and whether the governed principal
  shares the credential or authority needed to alter it. Reconcile—but do not re-prove—wfh-005's findings
  on permission lists, in-process policy, witness roots, ruflo policy/CASA coupling, and gate-input
  independence.
  *Output:* `findings-W6.md` with an authority/data-flow map, gate and bypass matrix, defaults, trust roots,
  source-claim/static-evidence discrepancies, and explicit limits of static assurance.
- **W7 — Maturity, credibility, and delta synthesis inputs.** Evaluate repository/package history,
  releases, contributor concentration, issue/PR evidence, dependency hygiene, documentation/code
  consistency, tests and CI presence (not execution), generated-artifact discipline, licensing, and signs
  of operational use. Build a claim-by-claim delta against the named wfh-005 and wfh-007 baselines, using
  owner materials as primary claims rather than demonstrated evidence. Do not use stars or release count
  alone as maturity proof and do not repeat other workstreams' code tracing.
  *Output:* `findings-W7.md` with a maturity/credibility scorecard, claim/evidence ledger, prior-finding delta
  table (`confirmed`, `changed`, `contradicted`, `still unverified`, `new`), and unresolved credibility risks.

## Expected output (FINDINGS.md)

1. A commit-pinned, complete architecture and component-boundary map for MetaHarness.
2. A complete internal and third-party dependency graph, including all direct/transitive ruflo and wider
   ruvnet ties and dependencies that appear only through generation or runtime composition.
3. Producer→generated artifact→runtime consumer chains, with authored/generated boundaries and hidden
   operational prerequisites.
4. Extraction dossiers identifying minimum coherent reuse closures, replacement seams, licensing and
   provenance constraints, and upgrade/drift liabilities—without an adoption decision.
5. A security and authority-boundary assessment that distinguishes policy description from static
   enforcement paths and identifies shared-authority, default-mode, trust-root, and bypass risks.
6. A maturity/credibility assessment and explicit delta from wfh-005/wfh-007, with every material claim
   labeled as source claim, static code evidence, prior demonstrated evidence, or unverified/inference.
7. A directional position for the `jurati-arch-002` proposer: what MetaHarness can inform, which candidate
   seams merit a later validated scope, and what evidence is still required. This is advice, not adoption,
   implementation, or architecture ratification.

## Proof bar  *(D7 — what would move status)*

- **Directional scope: structure-only, no status change.** This run produces findings, may identify
  `claimed` technologies, and may support a `position` recommendation. It does not execute MetaHarness,
  validate an extraction, establish runtime behavior, or advance any technology/capability to `partial` or
  `proven`.
- Any later claim that a seam is reusable, secure, compatible, or operational requires a separately
  approved empirical/validated scope with an artifact at that claim's altitude—for example a pinned build,
  isolated extraction, integration smoke test, adversarial boundary test, or upgrade/drift replay—created
  and independently validated by us.

## Explicitly out of scope

- Adoption, dependency selection, implementation, migration, procurement, architecture ratification, or
  creation/approval of `jurati-arch-002`.
- Installation, builds, tests, benchmarks, execution of generated output, network services, model/agent
  runs, containers, deployment, or any other compute-bearing proof.
- Any `partial`/`proven` grade advancement or claim of validated proof; presence of source, tests, CI, or
  demonstrations published by the owner is not demonstration by us.
- A general competitor scan, renewed workflow-authorization literature review, re-evaluation of all ruvnet
  repositories, or re-performance of wfh-005/wfh-007 findings except where current MetaHarness evidence
  directly confirms, changes, or contradicts them.
- Dynamic vulnerabilities, exploit development, secret access, intrusive security testing, supply-chain
  compromise analysis beyond static provenance/dependency evidence, or claims about deployed environments.
- Jurati product design, UI/canvas design, data-model selection, proof implementation, or a build
  recommendation. Any premise-changing theme revision, validated follow-on, material spend,
  cross-theme dependency, or build recommendation must be escalated under coordinator authority.

## Coverage / done call  *(synthesis)*

Coverage is ledger-based rather than candidate-count-based. Discovery is sufficient only when all of the
following are true:

1. **100% component accounting:** every root/workspace manifest member and every detected first-party
   package, crate, app, service, CLI, plugin, host adapter, generator, and registry is owned by exactly one
   W1 inventory row and cross-referenced to W2.
2. **100% declared-edge accounting:** every dependency declaration and lockfile-resolved direct/transitive
   edge is represented or explicitly marked unresolved/irrelevant with reason; import, dynamic-load,
   native/WASM, executable, filesystem, network, and generated-artifact residue sweeps are reconciled.
3. **100% ecosystem-reference accounting:** every `ruvnet`, `ruflo`, and `claude-flow` identity or reference
   found in manifests, locks, source, generated material, scripts, configuration, and documentation is
   classified by W3, including aliases and copied/embedded contracts.
4. **Complete generation and authority chains:** every identified generator has inputs, outputs, and
   consumers (or a named orphan), and every claimed enforcement gate has a decision point, protected
   operation, authority owner, default, bypass surface, and evidence label (or an explicit unknown).
5. **Delta closure:** every material wfh-005 MetaHarness/ruflo claim and every wfh-007 concept invoked in
   synthesis maps to `confirmed`, `changed`, `contradicted`, `still unverified`, or `not applicable`, with
   no silent carry-forward.
6. **Loop until dry:** after the ledgers are reconciled, run two independent residue sweeps—one from
   manifests/lockfiles/build metadata and one from source/config/docs/runtime references. Stop only when
   both surface no new unowned component, dependency class, ecosystem tie, generator/consumer chain,
   authority path, or prior-art delta. Unresolved dynamic or provenance questions remain visible as gaps;
   they do not become inferred closures.

The leader proposes coverage sufficient with the completed ledgers and residual gaps. **Human confirmation
at the synthesis gate is required.** A newly discovered technology outside the single-target boundary is
captured as a follow-on candidate, not absorbed into this scope.
