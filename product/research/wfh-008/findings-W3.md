# wfh-008 W3 — ruflo and wider ruvnet ecosystem coupling

**Role:** `factory-researcher` (read-only Unimatrix; no graph writes)  
**Cutoff:** MetaHarness `6f8c60216f47eac391a076fe27fd804470a07e10`; ruflo `d33ef4bf8ab27a8f9ef08352c9c293b53312a861`; both retrieved 2026-08-28.  
**Method:** static inspection only. No install, build, test, generator, service, benchmark, or repository code was executed.  
**Evidence labels:** **[source claim]**, **[static code evidence]**, **[prior demonstrated evidence]**, **[unverified/inference]**.

## Position

**[static code evidence] MetaHarness is not a thin wrapper around a live ruflo or `agentic-flow` dependency.** Neither its npm nor Cargo dependency closure declares `ruflo`, `@claude-flow/*`, `claude-flow`, or `agentic-flow`. Its executable first-party kernel, generators, adapters, Darwin simulator, and policy code are housed in MetaHarness. The remaining ruflo relationship is mainly ancestry and interoperability: copied/ported contracts and names, a one-way ruflo-eject importer, compatible registry/config shapes, and optional operational paths. This revises the shallow reading “MetaHarness requires ruflo” to “MetaHarness was factored from ruflo and deliberately retains several compatibility surfaces.”

**[static code evidence] The larger executable ecosystem coupling is now RuVector, not ruflo.** `@metaharness/kernel` directly requires `@ruvector/emergent-time`; it optionally peers with `@ruvector/rvf`; repository analysis optionally loads `@ruvector/ruvllm`; the router optionally peers with and develops against `@ruvector/tiny-dancer`. The lockfile expands those into native platform packages. Those are genuine package closures even though most are optional. Conversely, Darwin’s `RuvSecurityMemory` and “RuFlo swarm” are local, deterministic stand-ins: their names and ADR prose overstate external runtime coupling.

**[unverified/inference] For Jurati, the cleanest value is the portable mechanism set, not the branded ecosystem contract.** The local deterministic policy/envelope, generated-host normalization, manifest/drift ledger, receipts, typed memory/ranking, and one-way import ideas can be reimplemented without ruflo. Direct code reuse is plausible only after per-package license/dependency closure and behavioral validation; ecosystem-compatible registry, claims, witness, state-dir, and env-name surfaces should be treated as coupled contracts until replaced explicitly.

## Direct/transitive ecosystem graph

```text
MetaHarness repository
├─ no declared ruflo / @claude-flow / agentic-flow package or crate edge
├─ @metaharness/kernel
│  ├─ required @ruvector/emergent-time ^0.1.0
│  └─ optional peer @ruvector/rvf ^0.2.0
├─ create-agent-harness
│  └─ optional @ruvector/ruvllm ^2.5.6
│     └─ platform packages @ruvector/ruvllm-{darwin,linux,win32} 2.0.1
├─ @metaharness/router
│  └─ optional peer + dev @ruvector/tiny-dancer ^0.1.21
│     └─ eight platform packages @ruvector/tiny-dancer-* 0.1.21
├─ workspace lock closure also contains @ruvector/rvf-node 0.2.3
│  └─ five platform packages @ruvector/rvf-node-* 0.2.2
├─ ruflo compatibility/ancestry (copied shapes, names, importer; no package edge)
├─ RVM host output + documentation link (optional generated target)
├─ CVE-bench clone in benchmark-only shell scripts (explicit external operational edge)
└─ owner gist requires core-memory federation + MetaHarness + self-improvement loops
   (governance claim, not repository-enforced prerequisite)
```

## Exhaustive ruvnet-reference ledger

The classification unit is an identity/contract family rather than every repeated prose occurrence. Two independent residue sweeps covered manifests/locks and source/config/docs. The broad lexical sweep found 752 `ruflo`, 145 `claude-flow`, 5 `agentic-flow`, 96 `@claude-flow`, 1,073 `ruvector`, 429 `github.com/ruvnet`, 9 `raw.githubusercontent.com/ruvnet`, and 47 `RUFLO_` occurrences (case-insensitive where applicable). Ruflo-family terms occurred in 156 files: 70 doc-like and 86 other/generated/config/source surfaces. Repeated homepage, author, badge, keyword, changelog, and template attribution strings are represented by the provenance/naming rows below.

| Tie / residue family | Evidence and location | Class | Replaceability / determining constraint |
|---|---|---|---|
| ruflo / `@claude-flow/*` package dependency | **[static code evidence]** Absent from all `package.json`, `package-lock.json`, Cargo manifests, and Cargo lock as dependency identities. `agentic-flow` occurs only in architectural prose. | optional/claim-only (negative dependency result) | Replaceable: no package removal required. Compatibility behavior still needs separate rows. |
| Kernel provenance | **[source claim]** ADR-001/002 say the kernel was extracted/ported from ruflo; `claims.rs`, `routing.rs`, and `witness.rs` say they mirror ruflo ADRs/contracts. **[static code evidence]** implementations are local Rust under `crates/kernel/`; Cargo packages are locally named `ruflo-kernel*`. | coupled by provenance/naming; executable code local | Renameable mechanically, but semantic independence requires contract comparison and clean provenance accounting. MIT permits reuse with notice; ancestry is not evidence of behavioral equivalence. |
| Claims envelope | **[static code evidence]** `crates/kernel/src/claims.rs` implements a local claims format explicitly described as mirroring ruflo ADR-010 for federation. | replaceable compatibility contract | Direct code can be extracted with the kernel closure; clean-room concept is a signed/typed capability claim. Replacing the wire shape breaks claimed federation, not local operation. |
| Witness manifest/history | **[static code evidence]** `crates/kernel/src/witness.rs` locally implements the format while naming ruflo ADR-103. | replaceable compatibility contract | Mechanism is portable; format compatibility is coupled. Security/trust suitability belongs to W6 and must not be inferred from the shared name. |
| Routing lineage | **[source claim]** ADRs and comments cite ruflo ADR-026/143 and RuVector precedents. **[static code evidence]** current routing code is local; `@metaharness/router/src/index.ts` is dependency-free at runtime. | replaceable provenance tie | Local k-NN/cost-bar code is directly separable under MIT. Optional native training acceleration is a separate RuVector edge. |
| Ruflo project detector | **[static code evidence]** `detectRufloProject()` recognizes any two of `CLAUDE.md`, `.claude/`, `.claude-flow/`, `.mcp.json`; only `.claude-flow/` is ruflo-specific. | optional integration | Replaceable adapter. Its heuristic can false-positive generic Claude projects; it is not a ruflo API dependency. |
| One-way eject importer | **[static code evidence]** `eject.ts` reads ruflo-owned agents/skills/commands/config, rewrites four legacy identities, renames `mcpServers.claude-flow`, intentionally drops `.claude-flow/`, and records `ejected_from`. | optional but source-format-coupled | Portable importer pattern; direct implementation is coupled to undocumented ruflo filesystem/text conventions. State and provenance are intentionally lost. |
| Plugin registry/IPFS shape | **[source claim]** ADR-001/002/015 describe ruflo’s IPFS CID/marketplace. **[static code evidence]** `registry.ts`, `publish.ts`, and `scripts/marketplace-entry.mjs` emit a locally defined compatible entry shape. | optional compatibility | Replaceable behind a registry adapter. Default CID/branding, if emitted, couples discovery and trust policy to ruflo; schema compatibility is not schema governance. |
| Host adapters branded “ruflo-native” | **[source claim]** README labels Claude Code “Ruflo-native”; host package keywords contain `ruflo`. **[static code evidence]** adapters import local MetaHarness packages, not ruflo. Hermes locally reproduces a reasoning-block scrubber attributed to ruflo. | naming/provenance | Renameable. The copied scrubber pattern merits its own tests/license review before direct reuse. |
| State/env namespace | **[static code evidence]** meta-proxy reads `RUFLO_STATE_DIR` or `~/.ruflo/proxy-token` and `proxy-config.toml`; kernel embeds `RUFLO_KERNEL_{GIT_SHA,TARGET}`; trading template uses `RUFLO_TRADE_CONFIRM`; AGNTCY OTel constants carry `RUFLO_ADR324_*`. | coupled configuration contract | Replaceable only with migration/aliasing. These names create operational coupling even without ruflo code. |
| Generated WASM/native artifact names | **[static code evidence]** bindings and tests use `ruflo_kernel_wasm.js`; crates are `ruflo-kernel`, `ruflo-kernel-wasm`, and `ruflo-kernel-napi`, while npm distribution is `@metaharness/kernel`. | coupled build/artifact naming | Renameable with coordinated build, loader, CI, and packaging changes; no external ruflo runtime implied. |
| Darwin “RuFlo swarm” | **[source claim]** ADR-155 depicts RuFlo coordination. **[static code evidence]** `packages/darwin-mode/src/security/swarm.ts` is an in-process deterministic function pipeline with no ruflo import, subprocess, network call, or client. | claim-only for external RuFlo; local mechanism replaceable | Portable concept/code; do not claim actual multi-agent/process isolation or ruflo coordination from the name. |
| Darwin “ruVector memory” | **[source claim]** ADR-074/155/161 describe a RuVector fabric. **[static code evidence]** `security/memory.ts` calls itself “a thin in-memory ruVector stand-in” and uses local arrays/deterministic embeddings. | claim-only for external RuVector in this path | Portable typed-memory/ranking concept and local code. Persistence, native vector search, and cross-run fabric remain unverified. |
| `@ruvector/emergent-time` | **[static code evidence]** required dependency of `@metaharness/kernel` at `^0.1.0`, lock-resolved `0.1.0`; imported by kernel JS memory code. | coupled direct runtime package | Direct kernel npm reuse carries it unless decay is replaced. Package license was not established from the checkout/lockfile: license closure is open. |
| `@ruvector/rvf` / `rvf-node` | **[static code evidence]** optional peer `@ruvector/rvf ^0.2.0`; lock contains `@ruvector/rvf-node 0.2.3` plus five native packages pinned `0.2.2`. | optional native/storage integration | Replaceable through optional adapter, but lock/version skew (wrapper 0.2.3 vs native 0.2.2) is an upgrade surface. Licenses unresolved here. |
| `@ruvector/ruvllm` | **[static code evidence]** optional dependency `^2.5.6`; `analyze-repo.ts` dynamically `require()`s it only for `--embed`, and falls back to lexical scoring when unavailable. Lock pins wrapper 2.5.6 and native packages 2.0.1. | optional acceleration | Clean optional seam, but the native-wrapper version split and package licenses need validation. Core analyzer does not require it. |
| `@ruvector/tiny-dancer` | **[static code evidence]** optional peer + dev dependency `^0.1.21`; lock pins wrapper/platform packages 0.1.21. Router runtime implementation accepts caller-supplied vectors and has no import. | optional training/reference integration | Router code is directly reusable without it; native training pipeline is a separate closure. License unresolved here. |
| RVM | **[source claim]** README calls `ruvnet/rvm` a bare-metal microhypervisor. **[static code evidence]** host generation emits only `rvm.manifest.toml` plus local harness files; no RVM package dependency exists. | optional generated operational prerequisite | Adapter/manifest is replaceable. Actual deployment semantics, CLI, token compatibility, and hardware isolation are unverified. |
| CVE-bench | **[static code evidence]** two benchmark-only shell scripts clone `https://github.com/ruvnet/CVE-bench.git` into `/opt`. | optional benchmark-only external repo | Exclude from production closure; executing those scripts would introduce mutable-network provenance unless commit-pinned. |
| MetaHarness/agent-harness-generator aliases | **[static code evidence]** repository metadata and many generated templates still link to `ruvnet/agent-harness-generator` while current clone/origin is `ruvnet/metaharness`; published library is `@ruvnet/agent-harness-generator`. | coupled provenance/distribution naming | Not an external dependency, but a high-drift identity alias. Consumers, issue URLs, raw URLs, Pages links, and upgrade provenance span both names. |
| Owner gist stack mandate | **[source claim]** the owner gist says to map work across RuVector, RuFlo, MetaHarness, RVM, RVF and many other RuV projects, and “always coordinate” through core-memory federation, MetaHarness, and self-improvement loops. | governance claim-only | Not enforced by this checkout. It establishes same-owner strategic coupling, not a runtime prerequisite or independent security boundary. |

## A — Directly reusable/importable code and closure

| Candidate | Static closure | License closure | W3 assessment |
|---|---|---|---|
| `@metaharness/router` pure TypeScript k-NN/cost-bar router | `packages/router/src/index.ts`; no runtime imports; `tiny-dancer` optional peer/dev only | **[static code evidence]** package/repo MIT. Optional peer license unresolved. | Best direct-code seam. Importing core router need not import ruflo or RuVector. Runtime behavior remains unvalidated here. |
| Ruflo eject adapter | `packages/create-agent-harness/src/eject.ts` + Node fs/path | **[static code evidence]** SPDX MIT/repo MIT; copied source content retains its own provenance obligations. | Small code seam, but format-coupled and risky as a generic migration primitive. Prefer adapter-specific reuse, never silent bulk rewrite. |
| Local registry entry generator | `registry.ts` / marketplace script + local types | **[static code evidence]** repository MIT. Originating ruflo schema provenance is named but no versioned schema/license artifact is attached. | Code separable; wire contract governance is weak. Pin a local schema before reuse. |
| Deterministic Darwin receipt/ranking/memory code | local `darwin-mode/src/security/*`; no RuFlo/RuVector import in the named paths | **[static code evidence]** files SPDX MIT/repo MIT. | Reusable as simulation/evaluation primitives, not as evidence of distributed swarm or persistent vector fabric. |
| `@metaharness/kernel` | local Rust + JS loaders; required `@ruvector/emergent-time`; optional `@ruvector/rvf`; native/WASM packaging | **[static code evidence]** MetaHarness MIT; third-party package licenses not established in checkout. | Not dependency-light at npm distribution altitude. Direct source extraction may avoid RuVector pieces only after module-level closure and behavior tests. |
| Claims/witness/routing modules | local Rust modules plus shared kernel types/crypto dependencies | **[static code evidence]** MetaHarness MIT; explicit ruflo ADR ancestry. | Importable in principle, but compatibility/security semantics and copied-contract provenance require a validated extraction. Do not equate MIT license with suitable authority design. |

## B — Portable concepts for clean-room reimplementation

1. **[static code evidence] One-way ecosystem eject with an explicit loss ledger.** Plan first; enumerate copied and intentionally skipped state; rewrite only declared identities; preserve marked attribution; stamp the result as ejected. Improve it by parsing structured formats instead of global text substitution and by hashing/source-pinning imported artifacts.
2. **[static code evidence] Separate local kernel behavior from branded harness content.** MetaHarness’s most valuable architectural move is the kernel/content/host split. Reimplement the boundary, not the ruflo-compatible names or marketplace defaults.
3. **[static code evidence] Host-normalized generation from one declarative harness.** Per-host adapters produce host configuration while shared policy/manifest logic stays central. Jurati can copy the mechanism without copying the RuV registry, state namespace, or CLI identities.
4. **[static code evidence] Optional acceleration with deterministic fallback.** `--embed` dynamically loads RuVector and falls back to lexical scoring; the router accepts embeddings rather than owning an embedding runtime. This is a strong anti-lock-in pattern if fallback equivalence and observability are tested.
5. **[static code evidence] Typed negative memory and explicit ranking weights.** Darwin exposes the scoring weights and stores confirmed findings separately from false positives. Clean-room value is the auditable ranking contract; the present in-memory stand-in does not establish durable recall.
6. **[static code evidence] Deterministic receipts over canonical inputs.** Darwin hashes genome, corpus version, task, and seed and emits a fixed timestamp in simulation. Jurati can adopt the evidence-envelope idea while using stronger canonicalization/hashes and an external verifier.
7. **[source claim] Registry protocol separated from registry choice.** ADR-002 says the kernel owns a protocol while a harness owns its registry. The concept is portable; MetaHarness’s default CID and ruflo-compatible schema should not be inherited without independent governance.
8. **[unverified/inference] Treat ecosystem compatibility as an adapter plane.** Claims, witness, registry, state-dir, and env aliases should live behind versioned adapters so the control plane is not governed by same-authority upstream drift.

## Reconciliation with wfh-005 / wfh-007

- **[static code evidence] Confirms wfh-005’s central correction:** MetaHarness is primarily a scaffolder/factoring project, and its ruflo coupling is not a mandatory package/runtime dependency.
- **[static code evidence] Refines wfh-005:** the repository has grown far beyond the earlier “six-entry deny list + 87-line gate” characterization; however, W3 does not reassess enforcement. The relevant ecosystem delta is that current MetaHarness contains local copies/ports and RuVector package edges rather than delegating core behavior to ruflo.
- **[static code evidence] Confirms the wfh-005 name-collision warning:** MetaHarness witness code is a local ruflo-derived format. Nothing in the ecosystem tie makes it in-toto/TestifySec Witness or supplies an independent trust root.
- **[static code evidence] Maps to wfh-007’s gate-input-independence frame:** no external ruflo process is the independent decision plane in the traced paths. Local compatibility and same-owner governance therefore cannot be treated as independent authority merely because they cross repository/package names.
- **[prior demonstrated evidence] wfh-007 demonstrated contract/authority mechanisms in its own artifacts; no such prior artifact demonstrates MetaHarness compatibility, extraction, or enforcement.** This W3 output changes structure only.

## Gaps and follow-on flags

- **License gap:** MetaHarness and ruflo checkouts are MIT, but the checkout does not establish licenses for `@ruvector/emergent-time`, `@ruvector/rvf(-node)`, `@ruvector/ruvllm`, `@ruvector/tiny-dancer`, their native packages, RVM, or CVE-bench. A package/repository license audit is required before direct-code adoption.
- **Provenance gap:** ADRs say multiple kernel contracts were extracted/ported from ruflo, but no commit-to-commit provenance map establishes which lines/shapes are copied versus independently reimplemented.
- **Compatibility gap:** claims, witness, registry, and host/config compatibility have no version-negotiation or conformance result in this static review.
- **Alias/drift gap:** `metaharness` and `agent-harness-generator` coexist across repository URLs, npm identity, Pages/raw links, docs, and issue references.
- **Static-only limit:** source presence, comments, tests, and workflows were not executed. No seam is `partial` or `proven` by this work.
- **Residue result:** after manifest/lock and source/config/docs sweeps, no additional MetaHarness-originating ruflo, `agentic-flow`, or wider ruvnet dependency class was found. Repeated RuVector benchmark/prose mentions reduce to the package, local-stand-in, attribution, and benchmark-reference classes above.

## Citations

- `type: repo` · `ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10` · `title: MetaHarness repository at W3 cutoff` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: https://github.com/ruvnet/ruflo/tree/d33ef4bf8ab27a8f9ef08352c9c293b53312a861` · `title: ruflo repository at W3 comparison cutoff` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/eject.ts` · `title: Ruflo eject importer` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/analyze-repo.ts` · `title: Repository analyzer with optional RuVector embeddings` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/darwin-mode/src/security/swarm.ts` · `title: Darwin Shield local deterministic swarm pipeline` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/darwin-mode/src/security/memory.ts` · `title: Darwin Shield in-memory RuVector stand-in` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/docs/adrs/ADR-002-kernel-boundary.md` · `title: ADR-002 Kernel Boundary` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/package-lock.json` · `title: MetaHarness npm lockfile` · `org: ruvnet` · `year: 2026`
- `type: docs` · `ref: https://gist.github.com/ruvnet/7368405b5882a194df567d466818679b` · `title: RuV Stack Daily SOTA Research and Implementation` · `org: ruvnet` · `year: 2026`
- `type: repo` · `ref: product/research/wfh-005/scout-active-dev-r2.md` · `title: wfh-005 active-development round-two scout` · `org: arch-research` · `year: 2026`
- `type: repo` · `ref: product/research/wfh-007/reports/triage.md` · `title: wfh-007 triage report` · `org: arch-research` · `year: 2026`
