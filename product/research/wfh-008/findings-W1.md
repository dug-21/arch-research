# wfh-008 W1 — Repository architecture and component boundaries

**Role:** `factory-researcher` (read-only Unimatrix; no graph writes)  
**Target:** `ruvnet/metaharness` commit `6f8c60216f47eac391a076fe27fd804470a07e10`, checkout retrieved 2026-08-28  
**Method:** static inspection only. No install, build, test, generator, service, or repository code was run.  
**Evidence labels:** **SC** source claim; **SCE** static code/configuration evidence; **PDE** prior demonstrated evidence; **I/U** inference or unverified.

## Verdict

- **SCE:** MetaHarness is a polyglot monorepo with two explicit root workspaces: npm owns exactly `packages/*` (42 package manifests), while Cargo owns five `crates/*` members. The repository also contains three substantial executable/product surfaces outside both root workspace declarations: `apps/web-ui`, deprecated `services/apicompletions`, and the nested `kimi-k3-harness` project. Therefore neither root manifest is a complete repository architecture index. [C1][C2][C3]
- **SCE:** The repository's documented three-layer model—Rust kernel/bindings, adapters/applications, user-facing CLI/plugin/examples—is directionally recognizable, but incomplete at this cutoff. It omits numerous first-party evaluation, autonomy, benchmark, research-project, web/service, and nested-harness components present in the manifests. [C2][C4]
- **I/U:** The cleanest *structural* boundary is not “MetaHarness” as one library; it is a portfolio of independently versioned npm packages around a generator/CLI, host projections, a Rust kernel bridge, and many adjacent experimental/application packages. Runtime correctness and actual layer conformance are unverified here.

## Boundary/topology map

```text
Repository control/config
├── root npm orchestrator (private; workspace selector packages/*)
│   ├── generator/API: @ruvnet/agent-harness-generator
│   ├── product CLIs: metaharness/harness and specialist CLIs
│   ├── kernel JS bridge ↔ root Rust kernel / WASM / N-API crates
│   ├── ten host adapters
│   ├── SDK, verticals, integration and workflow-mechanism libraries
│   └── evaluation, benchmark, research and experimental packages
├── root Cargo workspace (5 members)
├── non-workspace products: web UI; deprecated API service
├── nested standalone product: kimi-k3-harness (+ its own 2 Rust crates)
├── distribution/config projections: Claude plugin; Codex skills
├── generated/published exemplars: examples-packages/* (37 manifests)
└── examples, experiments, benchmark submissions, docs/ADRs, CI and release scripts
```

**SC:** `docs/ARCHITECTURE.md` says Layer 1 must not import Layers 2/3 and calls the kernel portable. **SCE:** the manifests and paths establish intended package boundaries and binding crates, not compliance or portability; W2 owns edge enumeration. [C2][C4]

## Canonical component inventory

### A. Explicit root workspaces

| IDs | First-party components | Boundary / surface | Evidence |
|---|---|---|---|
| N01–N08 | `@ruvnet/agent-harness-generator`; `@metaharness/agntcy`; `arc-agi-3`; `arc-agi-3-chatgpt`; `avo`; `aws-finops`; `bench`; `metaharness` (`packages/create-agent-harness`) | generator library; integration; private controllers; autonomy/FinOps; benchmark; primary dual CLI | SCE: package manifests and `src/` trees [C3] |
| N09–N18 | `darwin`; `evals-extract`; `evals-hle`; `evals-math`; `evals-servedmodel`; `evals-sql`; `evals-toolcall`; `flywheel`; `harness`; `horizon` | evolution; six eval adapters; feedback/runtime libraries; hybrid TS/Rust horizon | SCE [C3] |
| N19–N28 | `host-claude-code`; `host-codex`; `host-copilot`; `host-github-actions`; `host-hermes`; `host-openclaw`; `host-opencode`; `host-pi-dev`; `host-prime-agent`; `host-rvm` | ten independently packaged host adapters/projections | SCE [C3] |
| N29–N36 | `jujutsu`; `kernel`; `oo-agents`; `projects`; `radio`; `redblue`; `router`; `sdk` | integration/bridge; JS kernel loader; hybrid TS/Rust agents; project/research runtime; signalling/security/routing/API | SCE [C3] |
| N37–N42 | `turn-credit`; `vertical-base`; `vertical-trading`; `weight-eft`; `workspace-lens`; `workspace-probe` | feedback; vertical composition; tuning; workspace analysis/probe (probe also has a direct `.mjs` bin) | SCE [C3] |
| R01–R05 | `ruflo-kernel`; `ruflo-kernel-wasm`; `ruflo-kernel-napi`; `template-catalog`; `poker-darwin` | root Cargo libraries/bindings/catalogue/poker evolution; all five are declared workspace members | SCE: root and crate `Cargo.toml` [C1][C5] |
| R03-P | `crates/kernel-napi/package.json` (`@metaharness/kernel-native`, private) | npm/N-API packaging and target-build metadata owned by the R03 binding crate; a declared artifact boundary separate from its `Cargo.toml`, outside the root npm `packages/*` workspace; cross-reference to W2 required | SCE [C5] |
| N03-PY | `packages/arc-agi-3/python/**` — `bridge.py` (868 lines) and `requirements.txt` | first-party **shipped cross-language component** owned by N03 `@metaharness/arc-agi-3`: authored Python program code, not a test fixture and not vendored. **Distribution boundary is explicit:** N03's npm `files` field is `["dist/**", "python/**", "README.md", "LICENSE"]`, so `python/**` is published inside the npm tarball alongside the compiled `dist/**`. It carries its own declared package-ecosystem surface (PyPI) and its own interpreter prerequisite, neither of which is expressible in `package.json`; cross-reference to W2 required (same treatment as R03-P) | SCE [C22] |

**SCE:** N03-PY is a *component* row, not a manifest row: `packages/arc-agi-3/python/` contains no `package.json`, so it changes no manifest count in the completeness ledger below. It is listed because W1's unit of ownership is a first-party component boundary, and a JS/Rust-only inventory alphabet cannot represent a shipped Python component at all. **SCE:** its dependency edges, lock absence and license closure belong to W2; its runtime/credential path belongs to W4/W6.

All N01–N42 are selected by the literal root npm workspace glob `packages/*`; `apps`, `services`, `kimi-k3-harness`, and `examples-packages` are not. All N packages contain a manifest; all except the private benchmark package declare a package license, predominantly MIT, with `horizon` and `oo-agents` Apache-2.0. **SCE:** package-level license declarations are metadata, not a completed dependency/license closure. [C1][C3]

### B. First-party components outside the root workspaces

| ID | Path/component | Ownership and boundary | Evidence |
|---|---|---|---|
| X01 | `apps/web-ui` | private Vite/React web application with its own lockfile; browser entry `src/main.tsx`; not a root npm member | SCE [C6] |
| X02 | `services/apicompletions` | private Node service with server entry, Docker/Compose and Terraform surfaces; its own lockfile; `DEPRECATED.md`; not a root npm member | SCE [C7] |
| X03 | `kimi-k3-harness` | standalone publishable CLI (`bin/cli.js`) with its own package, tests, TS config, harness/plugin state, and two Rust crates (`k3rs`, `k3-kernel-bench`) not in the root Cargo workspace | SCE [C8] |
| X04 | `.claude-plugin` | Claude marketplace/plugin manifest plus 13 skill definitions; distribution/configuration projection, not an npm package | SCE [C9] |
| X05 | `.codex` | Codex config example plus 13 skill projections; distribution/configuration projection, not an npm package | SCE [C9] |
| X06 | `examples-packages/*` | 37 individually manifested example/publishable package trees; excluded from root npm workspace and root lockfile ownership | SCE [C10] |
| X07 | `examples/*` | six authored runnable example/tour surfaces (`education`, `federation`, `host-tour`, `multi-host`, `quickstart`, `vertical-tour`) plus index documentation | SCE [C11] |
| X08 | `experiments/*` | five authored experiment batteries: credit feedback, router calibration, signal flywheel, turn-credit acceptance, user awareness | SCE [C12] |
| X09 | `submissions/*` | two checked-in SWE-bench submission/result bundles (`lite`, `verified`), evidence/data artifacts rather than packages | SCE [C13] |
| X10 | `scripts/*` | repository build, release, publish, audit, health, GCP, benchmark and generation orchestration; operational entrypoints, not libraries | SCE [C14] |
| X11 | `__tests__`, `.github/workflows` | root integration/contract tests and ten CI/release/security/pages/real-tool workflows; verification/config surfaces, not runtime packages | SCE [C15] |
| X12 | `docs`, root policy/config | ADRs and user/architecture/release docs; root npm/Cargo, Vitest, Rust toolchain, deny, Renovate, npm, editor and security configuration | SCE [C1][C4] |
| X13 | `.ruvnet-brain/checkpoint.json` | checked-in repository state/checkpoint surface; consumer and generation provenance unresolved in W1 | SCE [C16] |

### C. Authored, generated, and vendor-derived boundaries

| Material | Classification at cutoff | Evidence / unresolved point |
|---|---|---|
| `packages/darwin-mode/dist/**` | checked-in generated build output colocated with authored `src/**` | SCE: tracked JS, declarations and sourcemaps; freshness not tested [C17] |
| `apps/web-ui/src/generated/catalog.ts` | checked-in generated source | SCE: path/name; generator/freshness belongs to W4 [C17] |
| `packages/agntcy/src/oasf/taxonomy.generated.json` | checked-in generated copy derived from AGNTCY OASF | SCE: generator and comments name upstream; provenance/license closure requires W3/W5 [C18] |
| `packages/create-agent-harness/templates/**` and catalogue/genomes | authored generator inputs plus catalogue JSON/generated candidates | SCE: generator scripts and template extensions; producer/consumer chain belongs to W4 [C19] |
| `examples-packages/**` | generated/published exemplar outputs according to repository docs; checked in as first-party trees | SC + SCE: docs and 37 manifests; exact regeneration/freshness unverified [C10] |
| `kimi-k3-harness/upstream/**` | vendor-derived/upstream evidence: README, four patch files and `swarm-outcomes.json`; not a source checkout | SCE: tracked contents; source revision/license closure unresolved [C20] |
| golden fixtures, proof bundles, replay bundles, submissions | checked-in generated/evidence fixtures consumed by tests/tools | SCE: tracked paths; do not treat as authored runtime code or PDE from this run [C13][C17] |

No Git submodule declaration was found. **I/U:** absence of a submodule does not establish original authorship of copied assets.

## Top-level execution entrypoints

| Entrypoint | Owning component | Static role | Evidence |
|---|---|---|---|
| `metaharness` → `dist/bin.js`; `harness` → `dist/harness-bin.js` | N08 | generator and lifecycle/control CLI | SCE [C3] |
| `metaharness-darwin` → `dist/cli.js` | N09 | evolution CLI | SCE [C3] |
| `metaharness-arc-chatgpt` → `dist/cli.js` | N03 | private ARC MCP/server CLI | SCE [C3] |
| `metaharness-redblue`, `redblue` → `dist/cli/index.js` | N34 | red/blue CLI aliases | SCE [C3] |
| `weight-eft` → `dist/cli.js` | N40 | tuning/export CLI | SCE [C3] |
| `workspace-probe` → `bin/workspace-probe.mjs` | N42 | direct checked-in CLI | SCE [C3] |
| package exports / `dist/index.js` | most N packages | library entrypoints; generated `dist` is generally absent from checkout except Darwin | SCE; publish/build usability unverified [C3][C17] |
| `src/main.tsx` | X01 | browser application bootstrap | SCE [C6] |
| `src/index.ts`, `src/server.ts` | X02 | deprecated service bootstrap/server | SCE [C7] |
| `bin/cli.js` | X03 | nested Kimi harness CLI | SCE [C8] |
| root `scripts/*.mjs` / shell scripts | X10 | build/release/publish/audit/benchmark/GCP/generator operators | SCE; none executed [C14] |
| `examples/**/*.mjs`, `experiments/**/*.mjs` | X07/X08 | example and experiment runners | SCE; none executed [C11][C12] |
| Rust `src/lib.rs`, binding build scripts | R01–R05 and nested Rust crates | library/binding entry surfaces, not standalone binaries at manifest level | SCE [C5][C8] |

## OWNER AMENDMENT — reuse split

### A. Directly importable/reusable code

- **SCE:** The repository exposes many nominal import seams through package `exports`, especially the generator library, SDK, JS kernel bridge, host adapters, router, vertical base, and small analysis libraries. [C3]
- **I/U — determining constraint:** W1 cannot call any seam directly reusable because its *dependency and license closure* is not established here. Most workspace packages say MIT, two say Apache-2.0, but dependency closure belongs to W2/W5; checked-in generated/copy provenance also remains open. `apps/web-ui`, `services/apicompletions`, and private `bench` omit package-level license metadata, although a root MIT license exists; applicability of the root license to every copied/generated/upstream asset is not assumed.
- **I/U:** Direct importing is additionally weakened where manifest entrypoints target untracked/unbuilt `dist/**`. Only static source presence was established; no package was built or imported.
- **SCE + I/U — N03-PY:** the shipped Python bridge is a *bounded* file-level seam (two files, one of them a two-line pin list) and is stdlib-only apart from `arc_agi` and `arcengine`. But its closure is **worse** than the JS packages', not better: it pins two PyPI distributions whose licenses and transitive closure are unresolved at this cutoff, it has no lockfile, and importing it drags in a second runtime (`python3`) that no npm consumer of `@metaharness/arc-agi-3` declares. **Determining constraint for A: unresolved PyPI license/transitive closure plus an undeclared interpreter prerequisite.** Not directly reusable at this evidence level.

### B. Portable concepts for clean-room reimplementation

- **I/U:** The strongest W1-level portable concept is the *projection architecture*: one declarative/core surface projected into independently packaged host adapters and user-facing plugin/skill formats. This is a structural pattern, not evidence those projections are equivalent or secure. [C2][C9]
- **I/U:** A small native kernel with WASM and N-API bindings behind a JS loader is a portable boundary pattern, but the crate identities remain `ruflo-kernel*` and dependency/ecosystem coupling is delegated to W2/W3. [C1][C5]
- **I/U:** Keeping generator inputs, emitted exemplars, host adapters, validation commands, and release tooling as distinguishable surfaces is conceptually useful for Jurati; MetaHarness's actual repository partially blurs these with checked-in generated output and non-workspace products, so a clean-room version should require one authoritative component index and provenance markers.
- **SCE + I/U — N03-PY concept:** the portable idea is **cross-language component shipping with a version contract enforced at both ends**: the package ships its foreign-language sidecar inside its own distribution allow-list rather than assuming a host-installed script, and the sidecar refuses to start unless the installed SDK versions match its own pin table (`bridge.py` `EXPECTED_SDK_VERSIONS` / `_require_pinned_sdk_versions()` exits `2` with `CONFIGURATION_ERROR`). Jurati can reimplement that fail-closed version handshake cleanly. **The counter-lesson is equally portable:** the pin is *duplicated* — once in `requirements.txt`, once in `bridge.py` — with nothing that reconciles them, so the two copies can drift independently. A clean-room version should derive one from the other or assert their equality in CI.
- **I/U:** Separate stable definition/templates from experiment/submission/evidence bundles is also a useful governance concept; the current tree demonstrates separation by path only, not enforced custody or lifecycle.

## Completeness ledger and residue sweeps

**Reproducible enumeration rule (2026-08-28 rework):** counts use tracked/static files in the pinned checkout, with `.git` excluded and paths sorted under `LC_ALL=C`. Package manifests are enumerated by `find /tmp/wfh-008-metaharness -type f -name package.json -not -path '*/.git/*' -printf '%P\n' | LC_ALL=C sort`; Cargo manifests use the same command with `-name Cargo.toml`. Classification is path-exact: root npm members match `^packages/[^/]+/package.json$`; example manifests match `^examples-packages/[^/]+/package.json$`; root is exactly `package.json`; every remaining package manifest is “other non-workspace.” Root Cargo members match `^crates/[^/]+/Cargo.toml$`; other non-root Cargo manifests are every remaining `Cargo.toml` except root. This rule counts manifests, not directories, package names, or documentation claims. **SCE**.

| Ledger class | Expected | Accounted | Result |
|---|---:|---:|---|
| root npm workspace members (`packages/*`) | 42 | 42 (N01–N42) | closed |
| root Cargo members | 5 | 5 (R01–R05) | closed |
| root npm manifest | 1 | 1 (`package.json`) | closed; workspace orchestrator, not a member |
| example package manifests | 37 | 37 (X06) | closed |
| other non-workspace, non-root package manifests | 4 | 4: web UI X01, service X02, nested harness X03, kernel N-API packaging R03-P | closed |
| all `package.json` files | 84 | 42 workspace + 37 examples + 1 root + 4 other | closed |
| nested Cargo manifests outside root workspace | 4 | 4: horizon, oo-agents, k3rs, k3-kernel-bench | closed; first two are package-owned hybrid crates, last two nested-harness-owned |
| all `Cargo.toml` files | 10 | 1 root + 5 root members + 4 nested/non-members | closed |
| first-party app/service/CLI/plugin/host/generator/registry surfaces | enumerated above | X01–X13 plus package rows and entrypoint table | closed for W1 ownership; edges/behavior deferred |
| first-party shipped cross-language (non-JS/Rust) components | 1 | 1 (N03-PY) | closed; `packages/arc-agi-3/python/**`, the only authored non-JS/Rust program code inside a package `files` allow-list at this cutoff |
| top-level tracked directory families | 16 (`.claude-plugin`, `.codex`, `.github`, `.ruvnet-brain`, `__tests__`, `apps`, `crates`, `docs`, `examples`, `examples-packages`, `experiments`, `kimi-k3-harness`, `packages`, `scripts`, `services`, `submissions`) | 16 | closed |

**Manifest/build residue sweep (independent sweep 1, repeated after coverage rework):** the deterministic rule above returned 84 `package.json` files and 10 `Cargo.toml` files. Reconciliation found and assigned the formerly unowned `crates/kernel-napi/package.json` as R03-P and corrected the examples count from 40 to 37. It also rechecked the three npm lockfiles (root, web UI, service), root configs, Docker/Compose/Terraform, TS/Vite/Vitest/Playwright/Tailwind/PostCSS, Rust toolchain/deny, Renovate, plugin manifests, and workflow inventory. The repeated W1 sweep found no unowned manifest or build-surface component *within its own alphabet*. Absent Kimi/example/Cargo lockfiles remain explicit dependency-resolution unknowns for W2, not inferred closure. **SCE**.

**Enumeration-alphabet correction (rework pass 2).** **SCE:** the sweep above enumerated only `package.json`, `Cargo.toml` and `package-lock.json`. That alphabet is JS/Rust-only, so its "dry" result was a property of the *rule*, not of the repository — and it is precisely why a third package ecosystem was invisible to W1. The sweep was re-run over an ecosystem-agnostic filename alphabet: `package.json`, `package-lock.json`, `npm-shrinkwrap.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`, `Cargo.toml`, `Cargo.lock`, `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg`, `Pipfile(.lock)`, `poetry.lock`, `uv.lock`, `environment.y(a)ml`, `go.mod`, `go.sum`, `Gemfile(.lock)`, `composer.json`, `pom.xml`, `build.gradle(.kts)`, `Dockerfile`, `docker-compose*.y(a)ml`, `.tool-versions`, `rust-toolchain(.toml)`, `deny.toml`, `renovate.json`, `.nvmrc`, `flake.nix`, `Makefile`, `justfile`, `mix.exs`, `pubspec.yaml`, `*.csproj`, `CMakeLists.txt`. **Re-run result:** the widened rule returns every surface already owned above **plus exactly two previously unowned files** — `packages/arc-agi-3/python/requirements.txt` and `packages/darwin-mode/bench/terminal-bench/requirements.txt`. The first is now owned by N03-PY; both are *dependency-declaration* surfaces and their edges, lock absence and license closure are W2's. Nothing else appeared: no fourth npm lock root, no eleventh `Cargo.toml`, and no `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock`, `uv.lock`, `go.mod`, `Gemfile`, `composer.json`, `pom.xml`, `build.gradle`, `flake.nix`, `Makefile` or `justfile` anywhere in the tracked tree. **With the widened alphabet this sweep is dry; with the previous alphabet its dryness carried no information.** No count in the ledger above changes — a `requirements.txt` is not a package manifest. **SCE**.

**Source/config/docs/runtime-reference residue sweep (independent sweep 2, repeated after coverage rework):** re-enumerated tracked top-level families, executable/bin declarations, `src/main`, `src/server`, root scripts, examples/experiments, plugin/skill projections, `generated`/`dist`/`upstream` paths, submissions, and architecture/README claims. It produced no additional unowned W1 component class after R03-P reconciliation *within its own alphabet*, which was likewise JS/Rust-shaped. Open consumers, dynamic edges, generated freshness, copied-source revisions, and runtime liveness remain named W2–W5 questions rather than component-accounting closure. **SCE**.

**Enumeration-alphabet correction (rework pass 2).** **SCE:** the sweep was re-run language-agnostically, via (a) a census of every tracked file extension — 851 `.json`, 817 `.ts`, 446 `.md`, 337 `.mjs`, 314 `.tmpl`, 293 `.txt`, 275 `.sh`, 265 `.diff`, 96 `.jsonl`, 78 `.map`, 50 `.rs`, **48 `.py`**, 44 `.js`, 33 `.lean`, 25 `.toml`, 13 `.tf`, 13 `.svg`, 12 `.tsx`, 11 `.yml`, tail below ten — and (b) a spawn/exec literal frequency pass over `packages/*/src`, `packages/*/bin`, `scripts`, `apps/*/src`, `services/*/src` and `kimi-k3-harness`. **Re-run result — one new component class, then dry at W1's altitude.** The 48 `.py` files resolve exactly: **1** shipped component (N03-PY, `packages/arc-agi-3/python/bridge.py`); **4** authored benchmark-adapter scripts inside N09 `darwin` — `bench/terminal-bench/{darwin_terminal_agent.py,score.py}` and `bench/livecodebench/{build-manifest.py,eval-subset.py}` — which are *authored but not shipped*, since N09's `files` field is `["dist/**", "genomes/**", "README.md", "SECURITY.md", "LICENSE", "CHANGELOG.md", "LEARNINGS.md"]` and omits `bench/**`; **6** research analysis scripts under `docs/research/retort-placement/` (owned by X12); and **37** deliberately-vulnerable-or-clean corpus fixtures under `packages/darwin-mode/bench/security/**` (34) and `packages/projects/bench/fixtures/planted-vulns/` (3), which are data inputs to a benchmark, not program code. 1 + 4 + 6 + 37 = 48. The spawn/exec pass surfaced no new top-level family or entrypoint but did surface external-executable prerequisites of *shipped* package source, which are W2's row, not W1's. **Honest residue, not closure:** the shipped/not-shipped split above is derived from `files` allow-lists only — no tarball was packed, so actual published contents are unverified; and the *dependency* completeness of the `.py` surface is explicitly **not** closed here (undeclared imports are enumerated in W2's residue). **SCE**.

### Flags handed to other workstreams

- **W2:** explicitly own the N03-PY PyPI dependency surface (`packages/arc-agi-3/python/requirements.txt`, and the sibling declaration at `packages/darwin-mode/bench/terminal-bench/requirements.txt` owned by N09), its absent lockfile and absent license closure, and the `python3` interpreter prerequisite this shipped component imposes on N03; explicitly own the R03-P `@metaharness/kernel-native` npm packaging/build manifest alongside the `ruflo-kernel-napi` crate; resolve its build metadata/edges, all 42 root workspace package-to-lock links, actual root-workspace reachability, nested lockfiles, hybrid Rust crates, `dist` entrypoints, and whether the documented layer constraint holds.
- **W3:** classify `ruflo-kernel*`, `@ruvnet/agent-harness-generator`, host-RVM, `.ruvnet-brain`, AGNTCY copy provenance, and Kimi upstream identities.
- **W4:** trace template/catalogue/plugin/example generation, generated web catalogue, Darwin `dist`, OASF taxonomy, release scripts, and all producer→artifact→consumer chains.
- **W5:** establish dependency and license closure before any direct-code reuse; resolve root-license applicability to missing-license/private surfaces and copied/generated assets.
- **W6:** do not infer authority separation from package/process names; W1 establishes boundaries only.
- **W7:** reconcile the documented three-layer/CI/test claims with the expanded current tree and repository history.

## Citations

- **[C1]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/package.json · title: Root npm workspace manifest; and https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/Cargo.toml · title: Root Cargo workspace manifest · org: ruvnet · year: 2026
- **[C2]** type: docs · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/docs/ARCHITECTURE.md · title: MetaHarness Architecture · org: ruvnet · year: 2026
- **[C3]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/packages · title: MetaHarness npm workspace packages and manifests · org: ruvnet · year: 2026
- **[C4]** type: docs · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/README.md · title: MetaHarness README · org: ruvnet · year: 2026
- **[C5]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/crates · title: Root Rust workspace crates · org: ruvnet · year: 2026
- **[C6]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/apps/web-ui · title: MetaHarness web UI application · org: ruvnet · year: 2026
- **[C7]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/services/apicompletions · title: Deprecated API completions service · org: ruvnet · year: 2026
- **[C8]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/kimi-k3-harness · title: Nested Kimi K3 harness project · org: ruvnet · year: 2026
- **[C9]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/.claude-plugin · title: Claude plugin projection; and https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/.codex · title: Codex skill projection · org: ruvnet · year: 2026
- **[C10]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/examples-packages · title: Generated example package collection · org: ruvnet · year: 2026
- **[C11]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/examples · title: MetaHarness runnable examples · org: ruvnet · year: 2026
- **[C12]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/experiments · title: MetaHarness experiment batteries · org: ruvnet · year: 2026
- **[C13]** type: dataset · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/submissions · title: SWE-bench submission and result bundles · org: ruvnet · year: 2026
- **[C14]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/scripts · title: Repository operational and release scripts · org: ruvnet · year: 2026
- **[C15]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/.github/workflows · title: MetaHarness CI and release workflows; and https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/__tests__ · title: Root integration tests · org: ruvnet · year: 2026
- **[C16]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/.ruvnet-brain/checkpoint.json · title: Repository brain checkpoint · org: ruvnet · year: 2026
- **[C17]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/packages/darwin-mode/dist · title: Checked-in Darwin generated distribution; and https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/apps/web-ui/src/generated/catalog.ts · title: Generated web catalogue · org: ruvnet · year: 2026
- **[C18]** type: repo · ref: https://github.com/ruvnet/metaharness/blob/6f8c60216f47eac391a076fe27fd804470a07e10/packages/agntcy/src/oasf/taxonomy.generated.json · title: Generated OASF taxonomy copy · org: ruvnet · year: 2026
- **[C19]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/packages/create-agent-harness/templates · title: Harness generator templates and catalogue · org: ruvnet · year: 2026
- **[C20]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/kimi-k3-harness/upstream · title: Kimi K3 vendor-derived upstream inputs and patches · org: ruvnet · year: 2026
- **[C21]** type: docs · ref: https://gist.github.com/ruvnet/7368405b5882a194df567d466818679b · title: RuV Stack Daily SOTA Research and Implementation · org: ruvnet · year: 2026
- **[C22]** type: repo · ref: https://github.com/ruvnet/metaharness/tree/6f8c60216f47eac391a076fe27fd804470a07e10/packages/arc-agi-3/python · title: Shipped ARC-AGI-3 Python bridge component (`bridge.py`, `requirements.txt`) · org: ruvnet · year: 2026

The owner gist [C21] is a governance/roadmap source claim, not architectural evidence for component presence. No claim in this file is labeled PDE.
