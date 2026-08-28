# wfh-008 — W2 findings: complete static dependency graph

**Role:** `factory-researcher` · **workstream:** W2 only  
**Target:** `ruvnet/metaharness` checkout `6f8c60216f47eac391a076fe27fd804470a07e10` · retrieved 2026-08-28  
**Method:** static inspection only. Nothing was installed, built, generated, tested, benchmarked, or run. Therefore every repository result below is **static code evidence**, never demonstrated runtime evidence.

## Verdict

**[Static code evidence]** MetaHarness is not one dependency closure. It is three separately locked npm installations (root workspace, Web UI, API-completions service), one unlocked five-member Cargo workspace, a separate npm/NAPI build manifest inside one Cargo member, four detached/unlocked Rust crates, a separately manifested Kimi harness, and **37 manifests under `examples-packages/*/package.json`** outside the npm workspace. The root npm workspace contains **42** first-party packages and 45 declared first-party dependency edges; it has no declared first-party cycle. Its lock contains 420 non-link `node_modules` entries, while the Web UI and service locks contain 247 and 301 respectively. Those counts overlap and must not be summed as unique packages.

**Determining constraint:** **[Static code evidence + inference]** the credible reuse unit is a named package or mechanism with its own complete manifest/import/artifact/license closure—not “MetaHarness.” Several apparent seams are only clean after replacing a dynamic loader, generated artifact, optional native package family, undeclared hoisted import, or external executable. **A (direct code reuse)** is therefore conditional and package-specific. **B (clean-room concept reuse)** is materially broader: tiered backend fallback, adapter-per-host, manifest-to-artifact generation, and optional integration boundaries can be reimplemented behind Jurati-owned interfaces without importing their dependency closures. W3 owns what the ruvnet relationships mean strategically.

## 1. Installation and lockfile roots

| Root | Declared surface | Lock closure | Classification / gap |
|---|---|---:|---|
| repository root | npm workspaces=`packages/*`; **42** package manifests | 420 non-link packages; 197 marked dev; 156 marked optional | **[Static code evidence]** production, dev, optional and platform packages are co-recorded in lock v3. The lock contains exactly 42 top-level `packages/<name>` records, one for every literal workspace manifest; nested `packages/*/node_modules/*` records were excluded from this reconciliation. |
| `apps/web-ui` | independent React/Vite app | 247; 151 dev; 55 optional | **[Static code evidence]** outside root workspaces and audited separately by repository tooling. |
| `services/apicompletions` | independent Express service | 301; 221 dev; 76 optional | **[Static code evidence]** outside root workspaces; its manifest additionally names future undeclared Firebase, Pub/Sub, tokenizer and `@midstream/wasm` dependencies. |
| root Cargo workspace | 5 members | **none** (`Cargo.lock` absent) | **[Static code evidence]** direct Rust constraints are known; exact transitive versions and license closure are unresolved. |
| `crates/kernel-napi/package.json` | private `@metaharness/kernel-native` 0.1.15 NAPI build manifest inside the Cargo member | no independent npm lock; dev-only `@napi-rs/cli ^3` | **[Static code evidence]** this is a packaging/build surface, not a sixth root npm workspace member and not a published runtime package. It declares five compilation targets and drives `.node` production in `publish.yml`; the Rust crate supplies the runtime dependencies. |
| detached Rust crates | `horizon-core`, `ooa-cell-vm`, `k3-kernel-bench`, `k3rs` | none | **[Static code evidence]** each declares `[workspace]` locally and has no lock; all are dependency-free as authored. |
| `kimi-k3-harness` | independent npm manifest | no lock | **[Static code evidence]** direct versions are ranges; transitive closure is unresolved at cutoff. |
| `examples-packages/*/package.json` | 37 independent package manifests | no locks | **[Static code evidence]** these currently declare no package dependencies; `examples/**` contains zero package manifests, and generated/configured host relationships are not an npm closure. |

**License ledger.** **[Static code evidence]** repository root and `@metaharness/kernel-native` are MIT. The root npm lock's non-link entries report predominantly MIT, with ISC, BSD, Apache-2.0 and dual-license expressions also present; three non-link entries omit a license field. Rust workspace packages inherit MIT; `horizon-core` and `k3rs` declare Apache-2.0; `ooa-cell-vm` and `k3-kernel-bench` declare MIT. **[Inference]** missing Cargo locks and missing locks for Kimi/examples/kernel-native prevent a full version-pinned license closure, so direct code reuse from those surfaces is not cleared merely by the repository's MIT license.

## 2. First-party npm edge ledger

Every edge below is **[static code evidence]** from a package manifest. `R`=runtime dependency, `P`=peer, `O`=optional, `D`=development-only.

| Component | Direct first-party edges | Third-party direct edge(s) relevant to closure | First-party transitive closure |
|---|---|---|---|
| `@ruvnet/agent-harness-generator` | `metaharness` R | — | `metaharness`, darwin, weight-eft, redblue, flywheel, turn-credit; kernel only as peer of CLI |
| `metaharness` | darwin R; weight-eft R; redblue R; flywheel R; turn-credit R; kernel P | `kolorist`, `prompts`; `@ruvector/ruvllm` O | listed direct nodes only |
| `arc-agi-3-chatgpt` | arc-agi-3 R; kernel R | MCP ext-apps/sdk, `zod` | plus harness through arc-agi-3 |
| `arc-agi-3` | harness R; kernel R | — | harness, kernel |
| `avo` | horizon R | `agenticow` peer+dev | horizon |
| `bench` | kernel + all 10 host adapters + router R | — | kernel through every host; no further runtime edge from router |
| `evals-{extract,hle,math,servedmodel,sql,toolcall}` | flywheel R | — | flywheel |
| `host-{claude-code,codex,copilot,github-actions,hermes,openclaw,opencode,pi-dev,prime-agent,rvm}` | kernel R | — | kernel |
| `oo-agents` | radio R | — | radio |
| `sdk` | kernel R | — | kernel |
| `vertical-trading` | vertical-base R | — | vertical-base |
| `workspace-probe` | workspace-lens R | — | workspace-lens |
| `kernel` | — | `@ruvector/emergent-time` R; `@ruvector/rvf` optional peer; five `@metaharness/kernel-*` O | none first-party in repository (platform packages are registry artifacts) |
| `agntcy` | — | `agntcy-dir` R | none first-party |
| `jujutsu` | — | `agenticow`, `agentic-jujutsu` peers | none |
| `router` | — | `@ruvector/tiny-dancer` peer+dev | none |
| `agent-harness-generator-lib`, `aws-finops`, `darwin`, `flywheel`, `harness`, `horizon`, `projects`, `radio`, `redblue`, `turn-credit`, `vertical-base`, `weight-eft`, `workspace-lens` | no other first-party edge beyond those shown above | TypeScript/Vitest tooling where declared | none |

**[Static code evidence]** There are 18 incoming-edge-free first-party roots: agent-harness-generator library, agntcy, arc-agi-3-chatgpt, avo, aws-finops, bench, the six eval packages, jujutsu, oo-agents, projects, sdk, vertical-trading, and workspace-probe. There are 15 first-party leaves: agntcy, aws-finops, flywheel, harness, horizon, jujutsu, kernel, projects, radio, redblue, router, turn-credit, vertical-base, weight-eft, and workspace-lens. **[Static code evidence]** a depth-first pass over declared non-dev first-party edges found no cycle.

## 3. Rust and native/WASM graph

| Node | Direct edge | Class / artifact relationship |
|---|---|---|
| `ruflo-kernel-napi` | path→`ruflo-kernel`; `napi`, `napi-derive`, serde/json; build→`napi-build` | **[Static code evidence]** generation/build-time `cdylib`; compiled into npm platform artifacts, not published as a crate. |
| `ruflo-kernel-wasm` | path→`ruflo-kernel`; serde/json, wasm-bindgen, serde-wasm-bindgen, js-sys | **[Static code evidence]** generation/build-time WASM/CJS shim into `packages/kernel-js/pkg`. |
| `ruflo-kernel` | serde/json, thiserror, ed25519-dalek, sha2, hex; dev anyhow/criterion | **[Static code evidence]** authored Rust core; exact transitive versions unresolved without Cargo.lock. |
| `template-catalog` | serde/json | **[Static code evidence]** authored embedded catalog library. |
| `poker-darwin` | serde/json/thiserror; optional `ruvector-core`, candle core/nn, `rs_poker`; dev criterion | **[Static code evidence]** all heavy integrations feature-gated; default feature set is empty. |
| detached four crates | no external dependencies | **[Static code evidence]** compiled WASM or standalone Rust artifacts, but no lock/version closure exists. |

**[Static code evidence]** `@metaharness/kernel` resolves at runtime in order native→WASM→pure JS. Native package specifiers are selected from a platform map and loaded dynamically; the WASM shim is a generated relative artifact; JS is authored fallback. `METAHARNESS_KERNEL_BACKEND` can force one tier. This creates three behavioral implementations behind one interface. **[Inference]** direct extraction of the loader requires accepting and auditing all selected tiers, or deliberately deleting tiers and making the replacement interface explicit; concept reuse can retain the tiered resolver while Jurati owns implementations and conformance tests.

**NAPI packaging cross-reference.** **[Static code evidence]** `crates/kernel-napi/package.json` and `crates/kernel-napi/Cargo.toml` describe two faces of the same build boundary: npm metadata names the private build package, NAPI binary name, target matrix, and `@napi-rs/cli` dev tool; Cargo metadata names the `cdylib`, internal path dependency, Rust runtime crates, and `napi-build`. `.github/workflows/publish.yml` installs the CLI globally, runs `napi build` in that directory, and uploads `crates/kernel-napi/*.node`. It does **not** appear among the root lock's 42 workspace records because root workspaces are limited to `packages/*`, and it has no separate lock. Its npm edge is therefore **development/build-only and range-unlocked**; its emitted `.node` files become generation-time inputs to the optional platform-package/runtime-loader chain.

## 4. Dynamic, undeclared, generated, and executable edges

| Edge | Evidence | Resolution status / ownership |
|---|---|---|
| `ARC_CONTROLLER_FACTORY_MODULE` and `ARC_MCP_OAUTH_MODULE` → arbitrary module specifier | **[Static code evidence]** `arc-agi-3-chatgpt/src/cli.ts` imports environment-selected paths/packages | unresolved dynamic runtime edges; consumers supply implementations. |
| kernel → five native npm packages | **[Static code evidence]** dynamic import map + optionalDependencies | resolved names, platform-selected; artifacts are absent as first-party workspace nodes. |
| kernel → generated `pkg/ruflo_kernel_wasm.js` + `.wasm` | **[Static code evidence]** relative dynamic import and build script | generation-time producer→runtime-consumer edge; source presence does not establish artifact parity or execution. |
| `host-pi-dev` generated extension → `pi-agent-sdk` | **[Static code evidence]** emitted source imports a type from `pi-agent-sdk`; package manifest does not declare it | unresolved consumer-side/type-tooling dependency. The host package itself imports only kernel. |
| `agntcy` → `@bufbuild/protobuf` and `@buf/agntcy_dir...` | **[Static code evidence]** authored runtime imports, but only `agntcy-dir` is declared directly | dependency-by-hoisting/transitive implementation detail. Direct code reuse must promote these imports to explicit dependencies or wrap the SDK. |
| packages/scripts → `cargo`, `wasm-pack`, npm/npx, git, gcloud, Docker/host CLIs | **[Static code evidence]** `execFile`/scripts and package scripts | external executable dependencies; versions generally not locked by npm manifests. W4/W5 own behavior and generated-output semantics. |
| API service → Firebase/PubSub/tokenizers/future `@midstream/wasm` | **[Source claim]** `deferred-deps` field in service manifest | intentionally undeclared and unresolved; not part of present install closure. |

## 5. Direct code reuse (A) versus portable concepts (B)

| Seam | A — code and closure | B — clean-room mechanism |
|---|---|---|
| Host adapters | **[Static code evidence + inference]** small package boundaries exist, but all ten depend on kernel and at least one emits an undeclared host SDK type. Import only after per-adapter emitted-artifact closure review. | **[Inference]** portable: host-neutral spec→host adapter→generated configuration/source. Jurati can own the spec and adapter interface. |
| Kernel JS fallback | **[Static code evidence + inference]** strongest importable seam: authored TS with one declared runtime dependency and optional peer/native packages; however its public package includes memory/dispatch subpaths and a three-tier resolver, so extraction must select a narrower export or accept that closure. | **[Inference]** portable: deterministic JS floor plus optional accelerated backends, explicit forced-backend failure, and cross-backend conformance. |
| Rust kernel | **[Static code evidence + inference]** MIT and internally bounded, but the no-lock transitive/license closure and duplicate JS/WASM/NAPI implementations block a fully pinned lift decision. | **[Inference]** portable: canonical implementation with generated bindings and independent fallback, provided drift checks are Jurati-owned. |
| CLI/generator | **[Static code evidence + inference]** not a clean library: the published library re-exports the `metaharness` CLI package, whose runtime fan-out includes five first-party packages and optional ruvllm. | **[Inference]** portable: split authoring schema, deterministic generator, generated output, and upgrade/eject ledger. Reimplement against Jurati's vocabulary. |
| AGNTCY/CASA envelope compiler | **[Static code evidence]** code is bounded in `agntcy`, but runtime imports rely on transitive hoisting and comments state enforcement lives elsewhere. W3 owns ecosystem meaning. | **[Inference]** portable: compile intent into a bounded envelope at an replaceable interface; do not copy same-authority enforcement assumptions into Jurati. |
| Router / optional intelligence | **[Static code evidence + inference]** peer-only dependency shapes (`tiny-dancer`, `agenticow`) shift runtime installation responsibility to consumers; not self-contained imports. | **[Inference]** portable: optional policy/routing providers behind a fail-loud capability interface. |
| Example/Kimi/service surfaces | **[Static code evidence + inference]** absent locks, external executables, deferred deps, or environment-selected modules prevent complete importable closure. | **[Inference]** examples remain useful as contract fixtures and interface probes without importing implementations. |

**Replaceable-interface rule.** **[Inference]** dependency-induced coupling becomes acceptable only when the Jurati-owned side specifies: input/output schema, failure mode when provider/artifact is absent, version/provenance field, and conformance fixtures. A package name, optional peer, environment-selected import, or generated file path is not by itself a replaceable interface.

## 6. Delta against prior work

- **[Prior demonstrated evidence]** none from this W2 static run. wfh-005's execution-oriented findings remain prior research evidence, not promoted here.
- **[Static code evidence] Confirmed/narrowed:** wfh-005's “subtree, not product” instinct is stronger at this cutoff: the repository exposes package seams, but the actual closure has multiple independent locks, optional platform binaries, dynamic imports, generated WASM, and consumer-supplied peers.
- **[Static code evidence] Changed:** the assessed repository is materially larger than the earlier MetaHarness snapshot described by wfh-005; the current root manifest is `metaharness` 0.4.7 and includes many new packages. Earlier dependency counts must not be carried forward.
- **[Static code evidence] Still unverified:** runtime success, fallback equivalence, published package contents, native/WASM parity, external executable availability, security posture, and whether optional/peer paths are exercised.
- **[Inference] wfh-007 bearing:** its concern that dependency events should invalidate evidence is directly applicable: three locks plus unlocked Rust and generated artifacts yield several independent drift triggers. This is an architecture input, not acceptance of wfh-007's unratified work-contract draft.

## 7. Residue sweeps and gaps

**Manifest/lock/build-metadata sweep (rework pass 1):** **[Static code evidence]** the deterministic enumeration rule was: prune `node_modules`; enumerate every `package.json` in the checkout; partition the results into root, immediate `packages/*`, exact `examples-packages/*/package.json`, Web UI, service, Kimi, and any remaining path; enumerate every `Cargo.toml` and every `package-lock.json`; then compare the 42 immediate workspace directories against root-lock keys matching exactly `^packages/[^/]+$` (excluding nested package-local `node_modules`). Build metadata was swept across root/package scripts, GitHub workflows, TypeScript/Vite/Vitest/Playwright/Tailwind/PostCSS configuration, Docker/Compose/Terraform, Rust toolchain/deny, Renovate, and plugin manifests. Result: all **84 package manifests** partition as root 1 + workspace 42 + `examples-packages/*/package.json` 37 + Web UI/service/Kimi/kernel-napi 4; `examples/**` contains zero package manifests. **42/42 workspace manifests reconcile to 42 root-lock workspace records**; 10 Cargo manifests including the root and exactly 3 npm locks are accounted. No additional manifest, lock root, Cargo member, or build-metadata dependency class emerged. Honest residue: Cargo transitive versions/licenses; Kimi/example/kernel-native transitive closures; three missing npm-lock license fields; platform package source/provenance.

**Source/config/runtime-reference sweep (rework pass 1):** **[Static code evidence]** repeated import/dynamic-import, native/WASM/artifact, executable, environment, generated/catalog/template, and ecosystem-token searches after adding the NAPI packaging surface. It reconciled to the existing ARC modules, kernel native/WASM paths, generated Pi SDK reference, transitive-hoisted Buf imports, deferred service dependencies, external executables, and the now-explicit NAPI build chain. **Dry result:** no new unowned dependency or artifact class emerged. Residue remains visible because the specifier/environment or generated artifact is intentionally open.

**W3 handoff:** `@ruvector/{ruvllm,emergent-time,rvf,tiny-dancer}`, optional `ruvector-core`, the `ruflo-*` Rust naming, companion-ruflo enforcement comments, and `@ruvnet/agent-harness-generator` naming are enumerated here only as edges. Their ecosystem significance, upstream drift, and strategic coupling are exclusively W3's interpretation.

## Citations

1. `type: repo` · `ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10` · `title: MetaHarness repository at research cutoff` · `author: rUv` · `org: ruvnet` · `year: 2026`.
2. `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/package.json` · `title: Root npm workspace manifest` · `org: ruvnet` · `year: 2026`.
3. `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/package-lock.json` · `title: Root npm lockfile v3` · `org: ruvnet` · `year: 2026`.
4. `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/Cargo.toml` · `title: Root Rust workspace manifest` · `org: ruvnet` · `year: 2026`.
5. `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/kernel-js/src/index.ts` · `title: Kernel native/WASM/JS runtime resolver` · `org: ruvnet` · `year: 2026`.
6. `type: repo` · `ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/agntcy/src/oasf/publish.ts` · `title: AGNTCY publisher imports and SDK boundary` · `org: ruvnet` · `year: 2026`.
7. `type: docs` · `ref: product/research/wfh-005/scout-active-dev-r2.md` · `title: wfh-005 active-development round-two findings` · `org: arch-research garage` · `year: 2026`.
8. `type: docs` · `ref: product/research/wfh-007/SCOPE.md` · `title: wfh-007 evolved scope and authority ledger` · `org: arch-research garage` · `year: 2026`.
