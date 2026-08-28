# wfh-008 W4 — Generation pipeline and runtime composition

**Role:** `factory-researcher` (read-only Unimatrix; no graph writes)  
**Target:** `ruvnet/metaharness` commit `6f8c60216f47eac391a076fe27fd804470a07e10`, checkout retrieved 2026-08-28  
**Method:** static inspection only. No install, build, test, generator, service, model, or emitted code was run.  
**Evidence labels:** **SC** source claim; **SCE** static code/configuration evidence; **PDE** prior demonstrated evidence; **I/U** inference or unverified.

## Verdict

- **SCE:** MetaHarness has two first-class scaffold producers, not one: the published Node CLI walks packaged template directories and writes a directory; the browser UI independently synthesizes an in-memory file list and downloads a ZIP. A shared generated catalog supplies selectable metadata, but the scaffold implementations, manifest schemas, feature sets, and host projections are duplicated or divergent. [C1][C2][C3]
- **SCE:** The CLI chain is structurally coherent for its basic path: template files → flat rendered map → host/config and feature overlays → fingerprints/manifest → adjacent staging directory → rename into the requested target. Its generated package then resolves `@metaharness/kernel` dynamically as native → WASM → pure JS and imports a selected host adapter. This establishes a reachable-looking composition, not that it builds or operates. [C1][C4][C5]
- **SCE:** Generation introduces dependencies and ambient runtime assumptions that are not visible in the source template alone: selected host packages, default-on `@metaharness/darwin`, `npx -y <generated-name>@latest mcp start`, model-provider secrets, optional local HTTPS/bearer configuration, Node >=20, and optional native/WASM packages/tools. [C1][C4][C5]
- **SCE:** Several source claims overstate the emitted runtime. Most importantly, the browser MCP scaffold says it emits a JSON-RPC stdio/HTTP server, but `start()` contains no transport or dispatch loop and remote auth is imported then discarded. Its `maxToolCallsPerTurn` state is declared but never enforced. The static `dispatch()` policy gate is code, but no emitted transport reaches it without user implementation. [C6]
- **I/U:** The highest-value Jurati input is the producer→portable definition→host projection→runtime-loader pattern, plus explicit generated-state fingerprints. The present implementation is a reference for clean-room concepts, not evidence of an import-ready control plane: dependency/license closure belongs to W2/W5, projection parity is hand-maintained, and same-workspace configuration remains alterable by the governed principal.

## Producer → artifact → consumer ledger

| ID | Producer and input | Emitted / checked-in artifact | Static consumer | Hidden prerequisite or discrepancy | Evidence |
|---|---|---|---|---|---|
| G1 | `templates/catalog.def.mjs` → `scripts/gen-templates.mjs` | generated `templates/vertical_*` trees for `generate:true`; `templates/catalog.json`; `apps/web-ui/src/generated/catalog.ts` | CLI `loadCatalog()` and `templateDir()`; Rust `include_str!`; web gallery pools | Generator deletes/recreates only generated vertical dirs; `generate:false` templates remain hand-authored. Catalog metadata is shared, scaffold semantics are not. | **SCE** [C2][C3]
| G2 | packaged template dir + `{name,description,host}` → `walkTemplate()` / flat interpolation | rendered package, CLI, source, `.claude/**`, plugin files | generated package manager, host, and human/operator | `.tmpl` suffix selects rendering; unknown variables remain because scaffold calls `strict:false`; template `manifest.json` is skipped by the walker rather than driving emitted files. | **SCE** [C1]
| G3 | CLI host set → `hostConfigFiles()` plus package mutation | Codex/Claude/Pi/Hermes/OpenClaw/RVM/Copilot/OpenCode/GitHub Actions/Prime Agent config and instructions; added `@metaharness/host-*` deps for multi-host | each external host and npm | Claude config comes from templates; the other nine are code projections. Local MCP configs execute `npx -y <name>@latest mcp start`, hence registry/network resolution and package publication are runtime prerequisites. | **SCE** [C1][C4]
| G4 | CLI scaffold, Darwin default-on | package `devDependency @metaharness/darwin ^0.8.0`, `evolve` scripts, overwritten/generated skill | npm and `metaharness-darwin` CLI | Package running the generator declares `@metaharness/darwin ^0.9.1`, while output pins `^0.8.0`; generated dependency is introduced after template rendering. | **SCE** [C1]
| G5 | CLI `--sessions` | copy-in `src/sessions/log.ts` and README note | generated harness code, local JSONL session files | CLI-only; no browser parity. It is dependency-free code copied from kernel semantics, not an imported kernel API. | **SCE** [C1]
| G6 | rendered files → `emptyManifest()` / `fingerprintFiles()` | `.harness/manifest.json` and sibling SHA-256 | compare/diag/upgrade/publish tools | `template_version` remains `0.0.0`; manifest hashes cover the pre-manifest rendered map, not the manifest or later `--with-wasm` mutations. The sibling hash detects manifest byte changes but is not consulted by the upgrade planner. | **SCE** [C1][C7]
| G7 | `writeAtomic()` | adjacent random staging directory → target rename | filesystem/project | `--force` recursively removes the existing target immediately before rename; EXDEV fallback is copy+remove and explicitly loses atomicity. Parent directory must be writable and rename-compatible for the claimed atomic path. | **SCE** [C7]
| G8 | post-scaffold `--with-wasm <crate>` → `wasm-pack build` | `wasm/**`, CJS marker, `bin/wasm.mjs`, `src/wasm-doctor.mjs`, package mutations | Node `createRequire()` and generated CLI | Requires Cargo and `wasm-pack`; executes a shell command composed with quoted paths; outputs are added *after* the manifest and fingerprints, so drift/provenance state omits them. This path was not executed here. | **SCE** [C8]
| G9 | browser `HarnessConfig` + generated catalog → `buildScaffold()` | in-memory `GenFile[]`, browser manifest, witness stub, optional MCP source, then deterministic-date JSZip | downloaded ZIP, npm, selected hosts | Separate schema from CLI; manifest timestamp is literal `__GENERATED_AT__`; no per-file hashes; witness is explicitly unsigned; browser hard-pins kernel `^0.1.0`; sessions absent. | **SCE** [C3][C6]
| G10 | browser MCP selection | policy/capability JSON plus TS registries, gate, audit, auth/server stubs | intended stdio or HTTP transport | Transport dispatch loop is explicitly omitted; remote `authenticate` is not called; call counter is unused. Therefore generated MCP files are a policy/registry skeleton, not a complete server. | **SCE** [C6]
| G11 | `@ruvnet/agent-harness-generator` | thin re-export package | library consumers | Runtime implementation and templates remain in `metaharness`; importing the nominal library necessarily depends on that CLI package and its dependency closure. | **SCE** [C9]
| G12 | checked-in `examples-packages/*` synthesis or authored wrappers | exactly 37 manifested package trees at `examples-packages/*/package.json`; host/vertical wrappers shell to `metaharness@latest`; SDK showcase bundles copy stored JSON | end-user `npx @metaharness/<example>` | Reproducible count: `find examples-packages -mindepth 2 -maxdepth 2 -name package.json` yields 37 paths. `examples/**` contains six separate authored runnable example/tour surfaces but no `package.json`; those are not collapsed into the package count. Wrappers are late-bound to latest registry state rather than the repository cutoff; the synthesis script accepts prior swarm JSON and overwrites packages, so provenance depends on an external generated input not retained as the sole source. | **SCE** [C10]
| G13 | AGNTCY OASF checkout → taxonomy script stdout redirection | checked-in `taxonomy.generated.json` | `@metaharness/agntcy` source | Requires a separately obtained upstream checkout; command comment relies on shell redirection; freshness and upstream revision are not embedded sufficiently for this W4 trace. | **SCE** [C11]
| G14 | TypeScript/Rust build and release workflows | mostly untracked `dist/**`, native packages, WASM package; checked-in Darwin `dist/**`; marketplace entry, SBOM, release notes | package exports/bins, npm/GitHub release, Pages | Most manifests point at build-created `dist`; only Darwin has checked-in distribution output. Build/publish success was not tested. Marketplace output is produced into `dist` and uploaded by CI. | **SCE** [C12]
| G15 | `crates/kernel-napi/package.json` (`@metaharness/kernel-native`, private) + `Cargo.toml`/`build.rs` + publish target matrix | target-specific `crates/kernel-napi/*.node` artifacts named from N-API binary `kernel`; five declared compilation targets | `publish.yml` artifact uploader; intended downstream optional platform-package/native-loader chain | The npm manifest is outside root `packages/*`, has no independent lock, and contributes generation/build metadata plus `@napi-rs/cli ^3`; Cargo contributes the `cdylib`, path dependency on `ruflo-kernel`, N-API runtime/build crates. CI installs the CLI globally, builds per target, and uploads `.node` files, but its own comment says native artifacts are not yet consumed by the npm publish job. Therefore generation is statically connected to CI artifact upload, while incorporation into the five registry packages dynamically imported by `kernel-js` remains an unresolved/orphaned packaging step. | **SCE** [C5][C12][C17]

## Generated versus authored boundaries

| Boundary | Classification | Reconciliation |
|---|---|---|
| `catalog.def.mjs` | authored definition | **SCE:** authoritative for catalog metadata and generated vertical templates. [C2] |
| `templates/catalog.json`, web `generated/catalog.ts`, `generate:true` vertical dirs | checked-in generated | **SCE:** direct outputs named by the generator. No generated provenance hash or source commit is embedded. [C2] |
| `minimal` and `generate:false` vertical templates | hand-authored generator inputs | **SCE:** explicitly excluded from regeneration; uniform-looking template trees therefore have mixed custody. [C2] |
| CLI `host-config.ts` and browser `scaffold.ts` host emitters | authored duplicated projections | **SCE:** comments require lockstep/parity, but there is no shared callable implementation. The browser Pi projection omits the CLI's `trust.json`; feature parity is therefore already non-identical by inspection. [C3][C4] |
| generated harness `.harness/manifest.json` | generation-state artifact | **SCE:** CLI and browser use incompatible shapes and field names; only the CLI records hashes. [C1][C3] |
| witness file | generated provenance surface | **SCE:** browser emits a null-signature stub; CLI base scaffold does not emit `witness.json` in `scaffold()` despite skill/docs saying every scaffold does. Witness handling occurs in later commands/paths. [C1][C3][C13] |
| Darwin `dist/**` | checked-in build output | **SCE:** consumed by package exports and scripts, but source/build parity is unverified. [C12] |
| examples packages | checked-in generated/authored distribution wrappers | **SCE:** many wrappers late-bind to `metaharness@latest`; repository commit does not close their runtime artifact identity. [C10] |
| `crates/kernel-napi/package.json` | authored N-API packaging/build manifest owned with the Rust binding crate | **SCE:** declares private package identity, binary name, target matrix and build tool; it produces uploaded `.node` artifacts but is neither a root npm workspace member nor itself a runtime package. [C17] |

## Runtime-loading map

```text
host opens generated project
  ├─ reads project instruction/config projection
  ├─ local MCP projection → npx -y <generated-package>@latest mcp start
  │                         └─ requires published package + registry/network + generated CLI command
  └─ generated package CLI/source
       ├─ import @metaharness/kernel
       │    └─ loadKernel(): requested env override OR native optional package
       │                                  → packaged WASM shim → pure-JS floor
       └─ import @metaharness/host-<primary>

browser path
  catalog.def → generated catalog.ts → React configuration → buildScaffold()
  → optional MCP source skeleton → JSZip Blob → downloaded project
  → user must install/build and, for MCP, implement/wire the omitted transport loop
```

- **SCE:** Kernel late binding uses `METAHARNESS_KERNEL_BACKEND`; explicit `native`/`wasm` requests fail if unavailable, while auto mode silently descends to JS and caches the result. Native package names are platform/architecture-specific, and WASM expects `pkg/ruflo_kernel_wasm.js` inside the kernel package. [C5]
- **SCE:** The repository-side N-API producer is `crates/kernel-napi`: its npm/Cargo manifests and `build.rs` feed the five-target `publish.yml` matrix, which uploads `.node` artifacts. The workflow explicitly states those artifacts are not yet consumed by the publish job, so the producer→uploaded artifact edge is closed while uploaded artifact→optional native registry package→`kernel-js` consumer remains unresolved at this cutoff. [C5][C12][C17]
- **SCE:** Generated template package entry points import `loadKernel()` and one host adapter; the generated plain-JS `bin/cli.js` is intended to run without compiling the generated TypeScript, but npm must first resolve its dependencies. [C4]
- **SCE:** Host configuration is not a uniform execution boundary. Some projections configure MCP, some emit instructions/trust/capability files, GitHub Actions emits a workflow whose composite action only echoes a task, and Prime Agent emits guidance while declaring local stdio unsupported. [C4]
- **I/U:** A selected “host” therefore means a mixture of runtime registration, documentation, package dependency, and placeholder wiring—not one common adapter contract demonstrated across hosts.

## Hidden prerequisites and late dependencies

1. **SCE — package/distribution:** Node >=20, npm registry access, a published generated harness for `@latest` MCP configs, built `dist` for MetaHarness packages, and optional platform binaries/WASM. [C4][C5][C12]
2. **SCE — filesystem/process:** writable target parent; destructive target replacement under `--force`; `npx`, host executables, and for `--with-wasm`, Cargo/`wasm-pack`. Generated resources use CWD-relative `.harness/*` paths. [C6][C7][C8]
3. **SCE — network/secrets:** remote MCP points to `https://localhost:8787/mcp` with `HARNESS_MCP_TOKEN`; GitHub Actions passes one of three provider keys; publishing needs Pinata JWT; example wrappers resolve `latest`. These are deployment-time edges absent from a template-only graph. [C4][C10][C13]
4. **SCE — host ownership:** Claude Code consumes `.claude/settings.json`; Codex `.codex/config.toml` and `AGENTS.md`; Copilot workspace config; other hosts consume their native files. Correct host schema/version and workspace trust are external prerequisites, not enforced by the generated manifest. [C4]
5. **SCE — drift:** CLI manifest fingerprints precede post-generation WASM wiring; browser has no fingerprints; copied session code can drift from the kernel mirror; host logic is duplicated between CLI/browser/adapters; generated template/catalog artifacts depend on regeneration discipline. [C1][C2][C3][C8]

## Source-claim versus static-path reconciliation

| Claim | Static reconciliation | Result |
|---|---|---|
| “One canonical catalog keeps Rust, CLI and web UI in agreement.” | Catalog JSON is embedded/read by all three, but only metadata is shared; host and scaffold logic remain separate. | **SCE: partially confirmed; semantic parity unverified/contradicted by Pi output difference.** [C2][C3][C4] |
| CLI writes atomically. | Adjacent staging + rename is atomic on the normal path; EXDEV fallback explicitly is not, and `--force` deletes the old target before replacement. | **SCE: conditional, not universal.** [C7] |
| Browser output mirrors CLI and is install/test-ready. | Browser uses another builder, incompatible manifest, different dependency/version/features, and incomplete MCP transport. | **SCE: not established; material static divergence.** [C3][C6] |
| Every scaffold has a required witness manifest. | Browser emits an unsigned stub; core CLI `scaffold()` emits no witness file. Later verification/publish code accepts a missing witness and conditionally verifies one if present. | **SCE: contradicted for base CLI output.** [C1][C13] |
| MCP primitive is a gated stdio/HTTP server. | Gate and registries exist, but emitted `start()` does not start either transport and remote auth is not connected. | **SCE: policy skeleton exists; complete runtime claim contradicted.** [C6] |
| `--template-package` loads an external pack. | Argument parsing and a dynamic loader exist, but `main()` never uses `args.templatePackage`; scaffold resolves only bundled `templateDir()`. | **SCE: dormant/unreachable from documented CLI path.** [C1][C14] |
| Upgrade is regenerate–diff–merge. | Planner compares current files to old hashes and new hashes, but base manifest stores hashes rather than old content; application handles added/changed files but does not delete `removed` files or update the manifest in `applyPlan()`. | **SCE: partial mechanism, not the full claimed copier-style lifecycle.** [C7] |
| wfh-005: MetaHarness is principally a scaffolder and generated permissions are hand-derived rather than demand-derived. | Current cutoff still projects policy from booleans/static lists; no generation-time observation of actual runtime demand appears in this chain. | **SCE: confirmed at current cutoff for W4 chain; runtime efficacy remains unverified.** [C4][C6][C15] |

## OWNER AMENDMENT — reuse split

### A. Importable/reusable code, conditional on dependency and license closure

| Candidate | Smallest code boundary | Closure / constraint | W4 classification |
|---|---|---|---|
| renderer + walker + manifest hashing | `renderer.ts`, `walker.ts`, selected `manifest.ts` functions | Node built-ins; MIT headers; walker is UTF-8 text-only despite a binary-safe comment and uses non-strict rendering in scaffold. Full license/dependency closure remains W2/W5. | **I/U: plausible extraction candidate, not validated.** |
| adjacent staging writer | `writer.ts` | Node built-ins; behavior includes destructive force and non-atomic EXDEV fallback. | **I/U: reusable with explicit contract changes/tests.** |
| generator library package | `@ruvnet/agent-harness-generator` | Thin re-export of `metaharness`, hence inherits the CLI's runtime dependency graph and packaged templates. | **SCE: not an independent small closure.** |
| session log copy-in | emitted self-contained TypeScript | Node built-ins and MIT header; intentionally duplicates kernel wire semantics and creates a drift obligation. | **I/U: code seam exists, but clean-room/spec-first may be safer.** |
| browser zip utility | `zip.ts` | Requires JSZip; deterministic ZIP timestamps are explicit. | **I/U: narrow reusable utility, unrelated to control-plane enforcement.** |
| emitted MCP gate | generated `policy.ts` + `dispatch()` | Code is coupled to generated JSON/CWD and lacks transport/identity/approval completion. | **SCE: insufficient as a reusable runtime gate.** |

No row is called adoptable: **W4 does not establish transitive dependency or license closure, buildability, behavior, security, or compatibility.**

### B. Portable concepts/mechanisms for clean-room implementation

1. **I/U — producer→artifact→consumer ledger as architecture:** treat every definition, projection, manifest, host reader, runtime loader, and deployed prerequisite as a typed edge. This directly avoids the package-manifest blind spot exposed here.
2. **I/U — stable definition, deterministic projections:** one versioned definition should produce every host projection through one shared intermediate representation; generated artifacts should embed producer version/source hash and parity should be structural, not a comment requiring duplicated files to stay “byte-for-byte” aligned.
3. **I/U — projection adapters separate from authority:** host configuration is a projection, not an enforcement boundary. Jurati can clean-room the projection mechanism while keeping authority in an external controller/credential-owning plane.
4. **I/U — generation envelope:** bind template identity/version, normalized inputs, producer version, complete file hashes, dependency resolution, post-generation overlays, and witness in one immutable manifest. MetaHarness's split manifest/sibling hash and post-manifest WASM mutation illustrate why the envelope must close only after all producers finish.
5. **I/U — explicit late-binding policy:** represent registry tags, native/WASM fallback, environment-selected backends, dynamic template packages, network endpoints, and host schema versions as declared resolvers with fail-open/fail-closed semantics. Do not hide them behind generated config strings.
6. **I/U — authored/generated custody:** generated files should be non-authoritative projections; mixed hand-authored/generated template trees need explicit ownership markers and regeneration checks.
7. **I/U — portable runtime contract:** separate a host-neutral harness spec from host config emitters and from an actually complete runtime transport. The browser MCP skeleton is a useful negative example: registries plus a gate are not a server.
8. **I/U — code-copy governance:** if a self-contained primitive is copied into generated projects, publish its wire-format conformance suite/version and upgrade path; source comments claiming byte equivalence are not drift control.

## Coverage and residue sweeps

**Generator ledger closure:** every generator surfaced by the reworked W1/W2 handoff is assigned above: template/catalog (G1), CLI scaffold/host/manifest/write/WASM (G2–G8), browser/ZIP/MCP (G9–G10), library wrapper (G11), 37 path-qualified `examples-packages` manifests distinct from unmanifested `examples/**` runnable surfaces (G12), OASF taxonomy (G13), general build/release distributions (G14), and the separately manifested N-API producer/upload chain (G15). Darwin's *evolutionary runtime generation* is represented as a dependency/consumer of the scaffold chain, not re-analyzed as W4's main harness scaffolder; its internal mutation behavior belongs to its own package boundary and was not executed.

**Residue sweep 1 — manifests/locks/build metadata (rework pass 1):** pruned `node_modules`; enumerated all 84 tracked `package.json` paths and partitioned them as root (1), literal root workspaces `packages/*` (42), `examples-packages/*` (37), and separately owned Web UI, service, Kimi, and `crates/kernel-napi` surfaces (4). The six `examples/**` runnable surfaces contain no additional manifest. Re-enumerated all Cargo manifests, npm locks, package scripts/files/bin/exports, template manifests, Cargo embedded-catalog path, workflows, N-API target/build metadata, generated/package entrypoints, build-created `dist`, platform/WASM fallback, and marketplace/SBOM/release artifacts. The previously unowned N-API packaging surface is now G15; its missing independent lock and unresolved post-upload packaging remain explicit. **SCE: dry—no new unowned producer, artifact, consumer, manifest, lock, or build-metadata generation class surfaced.**

**Residue sweep 2 — source/config/docs/runtime references (rework pass 1):** repeated searches for writes/copies, dynamic imports, process spawns and external executables, filesystem/network/environment endpoints, native/WASM/`.node` artifact references, host config names, manifests, registries, witness/generated markers, and example/runtime identities. Reconciled dormant external-template loading, post-manifest WASM mutation, 37 `examples-packages` wrappers bound to `latest`, separate unmanifested `examples/**` runners, remote MCP/auth stubs, session copy-in, OASF external checkout, CWD-relative resources, and N-API build/upload/native-loader references to G1–G15. **SCE: dry—no new unowned producer→artifact→consumer or runtime-loading class surfaced.**

### Flags / handoffs

- **W2/W5:** close licenses and transitive dependencies before treating renderer/writer/session/ZIP code as reusable; include the nominal library's dependency on `metaharness`, JSZip, optional native packages, and emitted `@metaharness/*` packages.
- **W3:** classify `ruflo_kernel_wasm.js`, legacy repository/package names, marketplace schema provenance, RVM projection, and OASF external-source coupling.
- **W5:** prioritize drift dossiers for incompatible CLI/browser manifests, duplicated host emitters, `template_version: 0.0.0`, post-manifest WASM files, `@latest`, and generated/default Darwin version skew.
- **W6:** treat emitted allow/deny and MCP policy as same-project configuration; browser remote auth and transport are not connected; no authority conclusion follows from the presence of `dispatch()`.
- **Leader/curator:** premise-significant static discrepancy: MetaHarness currently demonstrates a multi-projection *generator portfolio*, not a complete synthesis-to-runtime compiler or a uniform host runtime.

## Citations

- **[C1]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/index.ts · title: MetaHarness CLI scaffold pipeline · org: ruvnet · year: 2026
- **[C2]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/scripts/gen-templates.mjs · title: Canonical catalog and template materializer · org: ruvnet · year: 2026
- **[C3]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/apps/web-ui/src/generator/scaffold.ts · title: Browser scaffold producer · org: ruvnet · year: 2026
- **[C4]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/host-config.ts · title: CLI host configuration projections; and https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/templates/minimal · title: Minimal generated harness template · org: ruvnet · year: 2026
- **[C5]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/kernel-js/src/index.ts · title: MetaHarness kernel runtime resolver · org: ruvnet · year: 2026
- **[C6]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/apps/web-ui/src/generator/mcp.ts · title: Browser-generated MCP primitive · org: ruvnet · year: 2026
- **[C7]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/writer.ts · title: Atomic scaffold writer; and https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/upgrade.ts · title: Scaffold upgrade planner and applier · org: ruvnet · year: 2026
- **[C8]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/with-wasm.ts · title: Post-scaffold WASM wiring · org: ruvnet · year: 2026
- **[C9]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/agent-harness-generator-lib/src/index.ts · title: Generator library re-export surface · org: ruvnet · year: 2026
- **[C10]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/scripts/write-example-packages.mjs · title: Example-package synthesis writer; and https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/examples-packages · title: Checked-in example package distributions · org: ruvnet · year: 2026
- **[C11]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/agntcy/scripts/generate-oasf-taxonomy.mjs · title: OASF taxonomy generator · org: ruvnet · year: 2026
- **[C12]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/.github/workflows · title: MetaHarness build, Pages, security, and publication workflows; and https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/packages/darwin-mode/dist · title: Checked-in Darwin distribution · org: ruvnet · year: 2026
- **[C13]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/publish.ts · title: Harness manifest publication and witness check · org: ruvnet · year: 2026
- **[C14]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/src/external-template.ts · title: External template dynamic loader · org: ruvnet · year: 2026
- **[C15]** type: repo · ref: https://github.com/dug-21/arch-research/blob/main/product/research/wfh-005/scout-active-dev-r2.md · title: wfh-005 active-development round-two findings on ruflo and MetaHarness · org: dug-21 · year: 2026
- **[C16]** type: blog · ref: https://gist.github.com/ruvnet/7368405b5882a194df567d466818679b · title: RuV Stack Daily SOTA Research and Implementation · author: ruvnet · year: 2026
- **[C17]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/crates/kernel-napi/package.json · title: Private N-API packaging and target manifest; and https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/crates/kernel-napi/Cargo.toml · title: ruflo-kernel-napi Rust binding manifest · org: ruvnet · year: 2026

## Limits

All findings are directional static evidence. Presence of tests, comments, workflows, loaders, or generated files does not show they execute successfully. No generated harness was produced, installed, built, imported, started, upgraded, published, or verified in this run; no claim is `partial` or `proven`.
