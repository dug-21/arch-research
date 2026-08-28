# wfh-008 W7 — maturity, credibility, and prior-art delta

**Role:** `factory-researcher` (read-only Unimatrix; no graph writes)  
**Target:** `ruvnet/metaharness` commit `6f8c60216f47eac391a076fe27fd804470a07e10`; retrieved 2026-08-28. `ruvnet/ruflo` commit `d33ef4bf8ab27a8f9ef08352c9c293b53312a861` is used only for MetaHarness-originating cross-repository delta.  
**Method:** static repository inspection and public GitHub metadata only. No install, build, test, generator, service, model, or repository code was run. GitHub metadata was retrieved 2026-08-28; where it post-dates the pinned commit it is identified separately.  
**Evidence labels:** **source claim** (documentation, owner material, third-party/public metadata); **static code evidence** (authored/generated code or configuration path); **prior demonstrated evidence** (artifact demonstrated by an earlier garage run); **unverified/inference**.

## Directional verdict

- **Static code evidence:** MetaHarness is an active, broad, pre-1.0 portfolio rather than a mature single product: 929 commits in 74 days, 42 npm workspace packages, five root Cargo members, several non-workspace products, 10 CI/release workflows, extensive test source, Renovate, pinned GitHub Actions, dependency audits, SBOM generation, CodeQL, and a publish pipeline. [C1][C2][C3]
- **Static code evidence:** development concentration is extreme. In pinned history, `ruv@ruv.net` authored 872/929 commits (93.9%); the next identity authored 49, and four other identities account for eight. GitHub's contributor endpoint similarly attributes 872 of 928 counted contributions to `ruvnet`. High velocity therefore does not imply independent maintenance depth. [C1][C4]
- **Source claim/public metadata:** by the cutoff the project had 67 issues and 160 PRs created, 134 PRs merged, and external reporters had found real packaging, generated-host, runner-coverage, scoring, and runtime defects. This is credible review/use signal, but not demonstrated operational success. [C4]
- **Static code evidence:** hygiene controls are substantial but internally disclose soft gates and incomplete release paths: `cargo-deny` and native builds are `continue-on-error`; native package publication is TODO; security audits carry explicit advisory ignores; most package entrypoints require untracked build output; generated projections and manifests have known drift holes. Presence of controls therefore raises credibility of engineering intent, not assurance at the claimed altitude. [C2][C5][C6]
- **Unverified/inference — determining constraint:** direct CODE reuse is limited by churn, one-account custody, inconsistent component/package indexing, unresolved third-party/copied-asset license closure, cross-package version drift, and source/documentation mismatches. Portable CONCEPTS are more mature than the product because several are small, deterministic, structurally visible, and not dependent on the repository's release train—but authority/security concepts remain unsuitable unless clean-roomed around an independently owned enforcement plane. [C7][C8][C9][C10]

## Maturity and credibility scorecard

Scores are directional (`strong`, `mixed`, `weak`), not proof grades.

| Dimension | Code/release assessment | Concept/pattern assessment | Evidence and ruling |
|---|---|---|---|
| Age and change rate | **Weak for stability.** 2026-06-13 first commit to 2026-08-26 cutoff; 929 commits; package versions span `0.1.x`–`0.9.x`; root is private `0.1.0`, CLI is `0.4.7`. | **Mixed/strong.** Fast iteration produced many explicit ADRs and negative-result fixes, but novelty and stability cannot be inferred from volume. | **Static code evidence** [C1][C2]. |
| Maintainer depth | **Weak.** 93.9% of commits from one email identity; five non-primary identities contribute 57 commits total. | **Mixed.** External issue/PR participation provides falsification pressure, but design and merge custody remain concentrated. | **Static code evidence + source claim/public metadata** [C1][C4]. |
| Releases/distribution | **Mixed/weak.** Six tags exist at retrieval, but only three GitHub release objects; several semver tags lack release objects. Pinned tree's main CLI says `0.4.7` while latest semver tag is `v0.4.5`; root workspace version is unrelated. Native publish remains TODO and most `dist` is absent. | **Not material** to clean-room concepts, except schemas require independent versioning. | **Static code evidence + source claim/public metadata** [C2][C4][C6]. Release count is not maturity proof. |
| License/provenance | **Mixed.** Root MIT license; nearly all workspace packages declare MIT, with `horizon` and `oo-agents` Apache-2.0. Root license does not close optional RuVector packages, copied OASF taxonomy, Kimi upstream patches/data, copied ruflo contracts, or every non-workspace/private surface. | **Strongest for abstract patterns**, which can be reimplemented without copying expression; provenance must still be recorded. | **Static code evidence** [C2][C7][C8]. No legal conclusion is made. |
| Dependency hygiene | **Mixed.** Root npm lockfile v3, separate app/service locks, pinned Rust toolchain, Renovate, npm/cargo audits, CodeQL and SBOM. No root `Cargo.lock` is checked in; dynamic/optional/native dependencies and `@latest` generated commands weaken reproducibility; RuVector wrapper/native versions diverge. | **Strong if dependency-light seams are selected:** router core, renderer/walker, manifest hashing, projection IR, deny-precedence algebra. | **Static code evidence** [C2][C5][C7][C8]. |
| Tests and CI | **Mixed/strong intent, incomplete coverage.** Hundreds of test-named files and ten workflows exist. Public checks associated with the pinned commit later reported successes, but this run did not execute them. External issue #194 reports four Rust crates and the nested Kimi Vitest suite outside runners. | **Mixed/strong:** testable deterministic contracts are portable; checked-in tests are specifications, not demonstrated evidence here. | **Static code evidence + source claim/public metadata** [C2][C4][C5]. |
| Documentation/code consistency | **Weak/mixed.** Architecture omits material components; browser MCP server lacks transport; CLI/browser projections diverge; security claims overstate witness trust and unsigned-publish exclusion; CASA paths drift across repositories; host and native-backend claims exceed static packaging. | **Strong as negative design evidence:** distinguish projection from enforcement, integrity from authority, declared from effective configuration, and registry compatibility from schema governance. | **Static code evidence** [C6][C9][C10]. |
| Generated-artifact discipline | **Weak/mixed.** A canonical catalog and CLI file fingerprints exist, but generated metadata omits producer/source hashes; CLI/browser manifests differ; post-scaffold WASM is outside fingerprints; Darwin `dist` freshness is unverified; examples use `@latest`; copied taxonomy lacks closed upstream revision. | **Strong portable concept:** one immutable generation envelope closed after all producers, with producer/input/dependency hashes and structural parity tests. | **Static code evidence** [C6]. |
| Security/release hygiene | **Mixed.** Security policy, pinned Actions, WIF/Secret Manager, provenance claims, audits and witness code are serious signals. Embedded witness key, accepted missing witness, degraded verification override, same-authority gates, `continue-on-error`, and TODO native publication prevent a mature-assurance reading. | **Mixed:** deny precedence, truthful degraded mode, pre-decision/post-receipt split, and external credential custody are stable concepts; the present trust boundary is not. | **Static code evidence** [C5][C9]. |
| Operational-use signal | **Mixed but unverified.** External issue reports and publish/smoke check records indicate users and distributed packages; 619 stars/74 forks at retrieval are discovery signals only. The owner gist mandates MetaHarness operationally but supplies no independently verifiable run artifact. | **Not needed** to judge conceptual portability; needed before claiming operational suitability. | **Source claim/public metadata** [C4][C11]. |

## Claim/evidence ledger

| Claim | Evidence label | Credibility disposition |
|---|---|---|
| “Portable Rust/WASM/N-API kernel” | **source claim** in README/security docs; **static code evidence** of crates/loaders | **Partially consistent, operationally unverified.** Most distributions are build-created, native publication is TODO, and external issue #172 reports only JS reachable in published packages at that time. |
| “Every scaffold/release is witness signed; unsigned publication has no path” | **source claim**; **static code evidence** | **Contradicted/sharpened.** Missing witness is accepted; degraded verification can be overridden; public key is self-selected inside the manifest. Integrity primitive exists; attested identity does not. |
| “One canonical catalog keeps Rust, CLI, and browser aligned” | **source claim**; **static code evidence** | **Changed to partial.** Metadata is shared; builders, manifests, host projections, and features diverge. |
| “Browser scaffold is CLI-equivalent/install-ready and emits a gated MCP server” | **source claim**; **static code evidence** | **Contradicted at static altitude.** Separate builder; incomplete transport/auth; no runtime dispatch loop. |
| “Generated state supports safe drift/upgrade management” | **source claim**; **static code evidence** | **Partial.** CLI hashes files, but producer identity, post-WASM mutation, removal application, browser parity, and copied-code drift are not closed. |
| “CI/audits block unsafe release” | **source claim**; **static workflow evidence** | **Changed to qualified.** Multiple real gates exist; some checks/build legs explicitly continue on error and advisory exceptions are recorded. No workflow was run by this research. |
| “Use MetaHarness with independent roles, scope, budget, capability limits, checkpoints, human approval, and no autonomous merge” | **source claim** in owner gist | **Still unverified as repository enforcement.** The gist is governance intent; static W6 found same-authority or optional gates and no general independent custody. |
| “MetaHarness depends on ruflo to operate” | **inference from branding/docs**, tested with **static code evidence** | **Contradicted.** No declared ruflo/`@claude-flow`/agentic-flow package edge; ties are ancestry, copied contracts, aliases, and optional interoperability. RuVector is the larger executable ecosystem dependency. |
| “MetaHarness is a mature control plane suitable for Jurati adoption” | **unverified/inference** | **Not supported.** Breadth and velocity are high; stability, authority custody, dependency/license closure, and released-artifact consistency are insufficient. |

## Direct CODE versus portable CONCEPTS

### A. Directly reusable code

| Candidate | Maturity at cutoff | Hygiene/liability | Directional status |
|---|---|---|---|
| `@metaharness/router` pure TS core | Small, dependency-free runtime seam; package MIT | Runtime behavior not validated; optional trainer dependency separate | **Best code candidate**, later isolated extraction + tests. |
| Renderer/walker/manifest hashing and adjacent-staging writer | Small Node-built-in closure; MIT headers | Non-strict templating, text-only walk, destructive `--force`, non-atomic EXDEV fallback | **Candidate with contract changes**, not drop-in. |
| Host adapters / generator | Packaged seams and broad tests | Projection parity drift, `dist` dependence, host-version semantics, late-bound `@latest`, thin library re-export inherits CLI closure | **Reference/extract selectively**, not wholesale import. |
| Kernel claims/witness/routing | Local MIT Rust source; explicit ruflo ancestry | Crypto/dependency closure; unauthenticated dispatch; no external trust root; RuVector npm coupling; authority semantics unsuitable | **Do not adopt as control boundary.** Possible utility extraction only after validated closure. |
| CASA compiler/checker pair | Small serializable envelope and deterministic checker split | Cross-repo duplicated schema, path drift, open scope strings, translator widening, no established sole-path runtime call site | **Reference only.** |
| Darwin/evaluation mechanisms | Large authored test/evaluation surface | High churn, checked-in `dist` freshness unknown, many self-generated “dream” changes; operational claims exceed isolation | **Mine individual algorithms/contracts**, not package-level adoption. |

**Unverified/inference:** code suitability is **low-to-moderate and seam-specific**. The later proof must pin a package and all transitive/runtime artifacts, close licenses, build/install it, compare published tarball to source, and replay an upgrade.

### B. Portable concepts suitable for clean-room implementation

| Concept | Stability despite code churn | What to preserve / reject |
|---|---|---|
| Stable definition → shared IR → host projections → explicit loss report | **High.** Repeated across packages and independently supports Jurati H4/H5. | Preserve typed projection and loss accounting; reject duplicated builders and treating config emission as enforcement. |
| Immutable generation envelope | **High.** Current failures make the invariant clearer. | Bind producer/input/dependency versions, all post-processors, complete artifact hashes and witness only after closure. |
| Pre-operation decision + post-operation receipt | **High.** Matches wfh-005/wfh-007 and is independent of implementation language. | Receipt never authorizes retrospectively; custody of decision path must be external. |
| Deny precedence, explicit allow, malformed-input denial, monotone delegation | **High as algebra; low as present authority.** | Clean-room a small checker and force every delegation/invocation through it; do not copy same-authority placement or wildcard/unauthenticated paths. |
| Degraded-mode truthfulness | **High.** `{unverified:true}` is useful semantics. | Make consequential operations incapable in degraded mode; reject override-by-bounded-party. |
| Definition/config state separated from events/evidence | **Moderate/high.** Repository paths and ledgers support the distinction but do not enforce custody. | Preserve separate lifecycle/backends and references, consistent with Jurati H7; never merge workflow/event state into knowledge. |
| One-way ecosystem eject with explicit loss ledger | **Moderate/high.** Small, understandable migration pattern. | Parse typed inputs, source-pin, hash, retain attribution, enumerate deliberately lost state. |
| Independent verifier / evidence-carrying completion | **Conceptually high; implementation unverified.** | Independence means separate credential/read-set custody, not a second role name in the same process. |

**Unverified/inference:** concept suitability is **moderate-to-high** because the valuable units are invariants and interfaces whose utility is reinforced by MetaHarness's own failure modes. This does not transfer its marketing claims, schemas, trust anchors, or ecosystem governance.

## wfh-005 complete MetaHarness/ruflo delta

| Material baseline claim | Status | Current reconciliation |
|---|---|---|
| MetaHarness is principally a scaffolder across hosts; authority relevance is weak | **changed** | It has expanded into a 42-package portfolio with kernel, policy, eval, Darwin, projects and controllers. Scaffolding remains the coherent product path; control-plane breadth is source-shaped, not mature assurance. |
| Host-emitter pattern is a useful “one declaration to many hosts” model | **confirmed** | Ten adapters plus plugin/skill projections exist; static divergence adds a required shared-IR/loss-report constraint. |
| Generated permissions are a small hand-written/static deny list, not demand-derived | **confirmed** | Host and browser generation still project declared lists/booleans; no observed-runtime demand derivation appears. |
| `PolicyGate` is an 87-line in-process default-deny gate | **confirmed** | Gate algebra remains, but kernel makes policy optional and allows when absent; caller owns rules/action mapping. Default-deny is object-local, not system-wide. |
| Same-UID/in-process policy is advice to an agent holding Bash | **confirmed** | No main MetaHarness gate establishes independently held credential/config custody. GitHub Actions can provide an external plane only under separately protected host administration. |
| Witness is home-grown Ed25519 with public key embedded; not TestifySec/in-toto | **confirmed** | Name collision remains load-bearing. Static paths also accept missing/degraded witness and an override. |
| Publish fails closed unless `--allow-unverified-witness` | **confirmed** | Current path retains explicit override; source claims of no unsigned path remain overstated. |
| MetaHarness is MIT and low-lock-in because it emits files and exits | **changed** | Root/packages are largely MIT, but direct reuse carries generated-state, npm/native/RuVector, registry and provenance closure. Conceptual projection lock-in is low; product closure is materially larger. |
| MetaHarness has no enforcement worth adopting | **changed** | It now contains multiple deterministic gate/checker implementations, but none closes independent custody/sole-path requirements. Useful as code/reference mechanisms, still not an authority plane. |
| Ruflo has richest policy primitives, inert/default-legacy enforcement and unwired delegation propagator | **changed** | Pinned ruflo now has additional engine/evaluation call sites and some envelope denials even in legacy; ordinary legacy/observe rules still allow, and the older propagator still declares no call sites. Not closed as authority. |
| Adopt `@claude-flow/security/policy`, not ruflo product | **still unverified** | MetaHarness does not depend on that package. Its local mechanisms show clean-room feasibility, but this run neither imports nor validates the ruflo subtree. |
| Ruflo/MetaHarness CASA was proposed/scaffolded and lacked execution call sites | **changed** | MetaHarness compiler and pinned ruflo Rust checker are implementation-shaped; static search still finds no established production sole-path call to the checker, and schema/path drift remains. |
| Monotone attenuation exists; approval-to-widen composition remains open | **confirmed** | Local/ruflo reduction checkers exist; no MetaHarness path demonstrates independent approval-gated widening through an externally owned plane. |
| Pre-authorized cost/token bounds exist but are gated behind enforcement mode | **changed / not applicable to MetaHarness runtime** | MetaHarness CASA carries `budget_usd`, but pinned ruflo Rust gate does not enforce it; broader ruflo policy remains separate. No MetaHarness operational closure shown. |
| No gate-input independence rule was found | **confirmed** | MetaHarness injects verifier objects/roles but does not establish independent read-set or credential custody. |
| Authorization demand is supplier-side; users mostly report correctness/install/durability | **confirmed and broadened** | External MetaHarness issues at cutoff focus on packaging, readiness, runner coverage, scoring and generated-host defects; no user demand establishes authority bounding as primary. |
| Ruflo is the operative dependency behind MetaHarness | **contradicted** | No declared ruflo/claude-flow dependency. Ruflo is ancestry/compatibility; executable ecosystem closure is more strongly RuVector. |
| `agentic-flow` was an unlicensed ecosystem concern | **not applicable** | No declared or executable MetaHarness edge at cutoff; it occurs only in prose. |
| “Witness-signed release” establishes operational provenance | **still unverified** | Static integrity code and CI claims exist; no externally anchored trust root or demonstrated-by-us published-artifact verification exists. |
| P8: a present/configured control may be inert; liveness probe required | **confirmed** | Optional gates, soft CI legs, unused generated MCP transport, absent sole-path CASA call sites, and generated-state omissions are new static instances. |

## wfh-007 concept delta invoked by this synthesis

| wfh-007 concept/baseline | Status | MetaHarness mapping |
|---|---|---|
| Kernel/isolation plane does not earn a bespoke build; assemble shipped sandboxes | **confirmed** | MetaHarness kernel is a library/dispatch layer, not a credential-owning OS isolation plane. It does not overturn the assemble ruling. |
| Sole-path mediation is per protected leg and requires external credential/config custody | **confirmed** | Main gates are optional/caller-owned; GHA is the only projection plausibly reaching an external token-minting plane, conditional on admin custody. |
| Trusted principal-side phase facts may grant; untrusted context may only deny | **still unverified** | No MetaHarness phase-minting identity chain or polarity-aware per-phase policy is established. |
| Delegation should use attenuated token chains; aggregation remains residue | **partially confirmed** | Claims/reduction code supports attenuation concepts; minting/signatures/sole-path placement and aggregation are absent or unverified. |
| Gate-input independence is read-set/credential separation, not actor naming | **confirmed** | Independent “verifier” roles/functions share embedder custody; no structural independence follows from role names. |
| Evidence needs typed/ordered acceptance and contradiction handling | **partially confirmed** | Receipts, witness, scores and completion artifacts exist, but no stable Jurati evidence lattice or externally anchored acceptance path is implemented. |
| Append-only evidence requires protected forge/settings audit | **still unverified** | GitHub workflows/receipts exist; this scope did not inspect repository rulesets/bypass credentials, and owner gist's “no autonomous merge” is a claim. |
| Stable definition and high-churn events/evidence require separate custody/lifecycles | **partially confirmed** | Templates/specs, manifests, receipts and logs are distinct paths, but generated artifact drift and same-repo custody prevent a mature implementation claim. |
| Cross-program work contract composes authority, sensitivity, consequence, evidence and owner gate | **not applicable as an accepted spec** | MetaHarness has fragments, not the composition. The later wfh-007 draft is unratified and received REWORKABLE FAIL; it is not a conformance target. |
| Caller-supplied identity cannot authorize even if persisted | **confirmed** | MetaHarness claims, caller options and registry trust fields lack an independently attested issuer in the main paths. This uses the corrected 2026-08-27 Unimatrix rule. |
| Degraded or missing evidence must fail closed at consequence altitude | **contradicted by current implementation** | Witness absence can be accepted; degraded verification has an override; browser emits unsigned stub. Truthful labeling exists, incapability does not. |
| Runtime enforcement liveness must be demonstrated before the run | **confirmed as unmet** | Static source/CI presence cannot prove the gate is reached; no liveness artifact was produced by this directional run. |
| Reviewer throughput and independent review are load-bearing for a single operator | **changed / risk increased** | High PR volume exists, but 93.9% commit authorship remains one identity and automation/one maintainer dominates custody. |
| Build only the unowned composition seam; adopt/assemble carriers | **confirmed directionally** | MetaHarness contributes reference carriers and projection concepts, not a credible reason to adopt its whole substrate or re-open a kernel build. |

## Residual credibility risks and follow-on proof

1. **Unverified:** published npm contents, provenance attestations, native/WASM availability, and GitHub releases were not compared byte-for-byte with the pinned source.
2. **Unresolved:** optional/copied/generated dependency licenses and source revisions—especially RuVector packages, OASF taxonomy, Kimi upstream inputs and ruflo-derived contracts—do not have a complete reuse ledger.
3. **Static code evidence:** package/repository version identities, generated manifests, CLI/browser behavior, examples using `@latest`, and cross-repo CASA paths expose drift surfaces large enough to make unpinned adoption indefensible.
4. **Source claim/public metadata:** CI check records and external user reports are evidence of activity and falsification, not prior demonstrated evidence by this garage.
5. **Determining validated follow-on:** select one small seam and one concept. For code, pin source plus published artifact, close licenses, build/install, run its focused tests, and replay one upstream upgrade. For authority, clean-room the envelope/checker behind a separately owned OS/service credential, seed forbidden actions and policy omission/mutation, and require an externally recorded refusal. Do not validate the whole monorepo first.

## Coverage and residue sweeps

- **Manifest/lock/build sweep:** root/workspace/non-workspace manifests, lock surfaces, license/security/community files, Renovate, tags/releases, and all workflows were reconciled. No new W7 maturity class remained; unresolved provenance is listed above.
- **Source/config/docs/runtime-reference sweep:** W1–W4/W6 handoffs were treated as indices and the cited paths were independently inspected for claims about packaging, generated parity, witness, CI, runtime loading and authority. Every material wfh-005 MetaHarness/ruflo claim and every wfh-007 concept used here has a status row; no silent carry-forward remains.

## Structured citations

- **[C1]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10 · title: MetaHarness repository and git history at research cutoff · org: ruvnet · year: 2026 · surface: active-dev
- **[C2]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/package.json · title: MetaHarness root npm workspace manifest and lock/build configuration · org: ruvnet · year: 2026 · surface: active-dev
- **[C3]** type: docs · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/docs/ARCHITECTURE.md · title: MetaHarness Architecture · org: ruvnet · year: 2026 · surface: active-dev
- **[C4]** type: repo · ref: https://github.com/ruvnet/metaharness · title: MetaHarness public repository, contributor, release, issue, pull-request and check metadata retrieved 2026-08-28 · org: ruvnet · year: 2026 · surface: active-dev
- **[C5]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/.github/workflows · title: MetaHarness CI, security, smoke and publish workflows · org: ruvnet · year: 2026 · surface: active-dev
- **[C6]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness · title: MetaHarness generator, release, manifest and browser scaffold paths · org: ruvnet · year: 2026 · surface: active-dev
- **[C7]** type: docs · ref: product/research/wfh-008/findings-W2.md · title: wfh-008 complete dependency graph handoff · org: arch-research garage · year: 2026
- **[C8]** type: docs · ref: product/research/wfh-008/findings-W3.md · title: wfh-008 ruflo and wider ecosystem coupling handoff · org: arch-research garage · year: 2026
- **[C9]** type: docs · ref: product/research/wfh-008/findings-W6.md · title: wfh-008 security and authority-boundary handoff · org: arch-research garage · year: 2026
- **[C10]** type: docs · ref: product/research/wfh-008/findings-W4.md · title: wfh-008 generation pipeline and runtime composition handoff · org: arch-research garage · year: 2026
- **[C11]** type: docs · ref: https://gist.github.com/ruvnet/7368405b5882a194df567d466818679b · title: RuV Stack Daily SOTA Research and Implementation · org: ruvnet · year: 2026 · surface: active-dev
- **[C12]** type: docs · ref: product/research/wfh-005/scout-active-dev-r2.md · title: wfh-005 round-two active-development findings · org: arch-research garage · year: 2026 · surface: active-dev
- **[C13]** type: docs · ref: product/research/wfh-005/reports/triage-amendment-1.md · title: wfh-005 triage amendment 1 · org: arch-research garage · year: 2026
- **[C14]** type: docs · ref: product/research/wfh-005/reports/triage-amendment-2.md · title: wfh-005 triage amendment 2 · org: arch-research garage · year: 2026
- **[C15]** type: docs · ref: product/research/wfh-007/reports/triage.md · title: wfh-007 triage report · org: arch-research garage · year: 2026
- **[C16]** type: docs · ref: product/research/wfh-007/specs/work-contract-v0-validator.md · title: wfh-007 work contract v0 independent checkability review · org: arch-research garage · year: 2026
