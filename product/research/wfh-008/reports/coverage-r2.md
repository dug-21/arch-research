# wfh-008 tech-discovery coverage re-audit — round 2

**Role:** `factory-researcher`, independent coverage re-auditor (did not author W1–W7; did not author round-1 `coverage.md`)
**Target cutoff:** `ruvnet/metaharness` @ `6f8c60216f47eac391a076fe27fd804470a07e10`
**Pin verification:** fresh `git clone` + explicit `git checkout 6f8c60216f47eac391a076fe27fd804470a07e10`; `git rev-parse HEAD` returns the pinned SHA; `git ls-remote https://github.com/ruvnet/metaharness HEAD` returns `6f8c60216f47eac391a076fe27fd804470a07e10` (remote unmoved). Working tree clean (`git status --porcelain` empty).
**ruflo:** `d33ef4bf8ab27a8f9ef08352c9c293b53312a861` — **not cloned this round**; no check required it.
**Rework under audit:** commit `17ebf2e` (`+14/-7` W1, `+9/-7` W2, `+8/-4` W4). W3, W5, W6, W7 untouched.
**Retrieval date:** 2026-08-28
**Method:** static inspection only — clone, checkout, `git ls-files`, `git grep`, `find`, `python3 -c` on JSON text. No install, build, test, benchmark, generator, service, container, model, or repository code was executed. Nothing in this report is demonstrated-by-us evidence.

**Recommendation: REWORKABLE**  
**Superseded 2026-08-28 by the final ruling in §9: PASS.** The REWORKABLE call above stands as the round-2 record; §9 rules on rework pass 2 (`3cd296d`), which discharged it.

> **Correction note — amended 2026-08-28, after first publication.**
> The `research-leader` relayed two factual errors found during rework pass 2. I re-verified both
> against the same pinned checkout rather than accepting the relay, and **agreed with both**:
> **(1)** §3 P4 and §5 stated that `packages/projects/src/verifiers.ts` calls `execFileSync`. It does
> not — it has no `child_process` import and its header L13–14 states "This module performs NO process
> execution." It *specifies* the unsandboxed vector; the ten actual call sites are
> `bin/darwin-discover.mjs` L130 plus nine `bench/*.bench.mjs` files. The corrected form is a
> **sharper** finding, not a weaker one — the sandbox bypass is written into the shared verifier
> contract, not scattered across incidental callers — and the bypass is **partial** (env hygiene
> present, namespace isolation absent ⇒ network egress is the unmitigated exposure).
> **(2)** §3 P4 described "W6's 37-row gate matrix." W6 has **10 authority-map rows + 7 gate-matrix
> rows**; 37 was my own raw count of every `^|` line in the file (four tables plus their header and
> separator rows) mislabelled as a gate count. W6 never asserted 37.
> The recommendation, the §1 count resolution, every predicate verdict, the four-repair verdicts and
> the sweep outcomes are **unchanged**. Nothing else in this report was rewritten.


Not for the count. The count question is settled **in the rework's favour** — the rework is right and round 1 over-counted. The rework must be reworked for a different reason: an entire **third package ecosystem (PyPI) plus its interpreter prerequisite, its shipped bridge component, its network endpoint/credential path, and a first-party OS-level isolation gate** appear nowhere in W1–W7, and were also missed by round 1. Both residue sweeps come back **not dry**.

---

## 1. The count conflict — resolved

### Deciding command

```
$ cd <checkout> && git rev-parse HEAD
6f8c60216f47eac391a076fe27fd804470a07e10

$ git ls-files '*package.json' | wc -l
84
$ find . -path ./.git -prune -o -name node_modules -prune -o -name package.json -print | wc -l
84
$ diff <(git ls-files '*package.json' | sort) \
       <(find . -path ./.git -prune -o -name node_modules -prune -o -name package.json -print \
         | sed 's|^\./||' | sort)   # -> no output: SETS IDENTICAL
$ find . -path ./.git -prune -o -name package.json -print | wc -l   # no node_modules prune at all
84
$ git check-ignore -v $(git ls-files '*package.json')   # -> no output: none ignored
```

`git ls-files` and `find` agree **exactly, as sets, not merely as counts**. There is no manifest tracked-but-ignored, ignored-but-present, or hidden inside a `node_modules` that a prune would drop. **Total = 84.**

### The specific hypothesis under test: FALSIFIED

The leader's hypothesis was that `-maxdepth 2` could structurally hide a manifest at `examples-packages/<a>/<b>/package.json` or deeper. It does not, at this commit:

```
$ find examples-packages -mindepth 2 -maxdepth 2 -name package.json | wc -l
37
$ find examples-packages -name node_modules -prune -o -name package.json -print | wc -l
37
$ git ls-files 'examples-packages/**package.json' | wc -l
37
```

**Any-depth = depth-2 = 37.** Every one of the 37 is `examples-packages/<name>/package.json`; there is no third path segment anywhere under `examples-packages/`. The directory holds 39 entries: 37 package directories plus `README.md` and `GISTS.md`. The depth-2 rule is *narrow but not lossy at this commit* — a latent fragility, not an active defect (see §7).

The same check for `packages/`:

```
$ git ls-files 'packages/**package.json' | wc -l
42
$ find packages -mindepth 2 -maxdepth 2 -name package.json | wc -l
42
```

**42 = 42.** Not a depth-bounded artifact either.

### The partition

| Partition | Count | Paths |
|---|---:|---|
| root | 1 | `package.json` |
| root npm workspace (`packages/*`) | 42 | matches root `"workspaces": ["packages/*"]` exactly |
| `examples-packages/*` | 37 | listed above |
| other non-workspace | 4 | `apps/web-ui/package.json`, `crates/kernel-napi/package.json`, `kimi-k3-harness/package.json`, `services/apicompletions/package.json` |
| **total** | **84** | 1 + 42 + 37 + 4 |

Supporting counts, independently confirmed:

```
$ git ls-files '*Cargo.toml' | wc -l      -> 10   (find, target/node_modules pruned -> 10)
$ git ls-files '*package-lock.json'       -> 3    (root, apps/web-ui, services/apicompletions)
```

10 Cargo manifests = 1 root + 5 root workspace members (`crates/{kernel,kernel-wasm,kernel-napi,template-catalog,poker-darwin}`) + 4 non-members (`packages/horizon/crate`, `packages/oo-agents/crate`, `kimi-k3-harness/crates/k3rs`, `kimi-k3-harness/crates/k3-kernel-bench`). Exactly 3 npm locks. No fourth lock root.

### Verdict on the two ledgers

**The rework pass (W1/W2/W4) is correct. Round 1's `coverage.md` over-counted.**

- Correct numbers: **84 total; 37 examples; 42 workspace; 4 other; 1 root; 10 Cargo; 3 npm locks.**
- Round-1's 38 examples / implied 85 total is wrong by exactly one example manifest.
- **I could not attribute the over-count to a specific path.** No path at any depth, tracked or untracked, ignored or not, pruned or unpruned, produces 38 under `examples-packages/`. The 38th manifest does not exist in the pinned tree, so I cannot name it. The most likely mechanism is a counting artifact in the round-1 auditor's own working checkout (e.g. an installed `node_modules` entry, or a `wc -l` over a listing that included a non-manifest line) rather than a real path — **but that is unverified-inference, and I state it as such rather than manufacturing an attribution.**

**Is the off-by-one cosmetic or load-bearing?** Load-bearing in principle — an unowned manifest is exactly the class predicate 1 exists to catch, so "38 vs 37" had to be settled rather than waved through. Settled, it turns out to be **cosmetic in effect**: the missing manifest does not exist, no component was hidden, and sweep 1's dryness does not turn on it. Sweep 1 is not dry — but for an entirely different reason (§5).

**[Static code evidence]** throughout this section.

---

## 2. The four required repairs

| # | Required repair | Verdict | Evidence |
|---:|---|---|---|
| 1 | `crates/kernel-napi/package.json` owned | **PASS — substantive** | The file exists and every descriptive detail checks out. `{"name":"@metaharness/kernel-native","version":"0.1.15","private":true,"license":"MIT"}`, `napi.binaryName="kernel"`, exactly the 5 targets W2/W4 state (`x86_64-unknown-linux-gnu`, `aarch64-unknown-linux-gnu`, `x86_64-apple-darwin`, `aarch64-apple-darwin`, `x86_64-pc-windows-msvc`), `devDependencies: {"@napi-rs/cli":"^3"}`. Cargo side confirms `crate-type=["cdylib"]`, `ruflo-kernel = { path = "../kernel" }`, `napi`/`napi-derive` workspace deps, `napi-build = "2"` build-dep, `build.rs` calling `napi_build::setup()`, `publish = false`. `.github/workflows/publish.yml` L65–79 installs `@napi-rs/cli@^3` globally, runs `napi build --platform --release --target <t>` with `working-directory: crates/kernel-napi`, uploads `crates/kernel-napi/*.node` — and its own inline comment states the per-platform `.node` artifacts "are not yet consumed by the publish job (native publish is a TODO)", exactly as G15 reports. Ownership is a **real inventory row** (`R03-P`, W1 L46) with a ledger line (W1 L126) and a W2 cross-reference block (W2 L67), not a passing mention. **[Static code evidence]** |
| 2 | Example/non-workspace counts corrected | **PASS** | W1 L29/L60/L77/L122–127 and W4 L31 all now state 37 examples / 84 total / 4 other. §1 confirms every one of those numbers. W1's stated enumeration rule (`find … -name package.json -not -path '*/.git/*'`) is any-depth and reproduces 84. **[Static code evidence]** |
| 3 | W2 workspace count → 42 with 42/42 lock reconciliation | **PASS — verified independently, one-to-one** | Root `package-lock.json` (lockfileVersion 3, 517 records) contains **exactly 42** records matching `^packages/[^/]+$`. Set-compared against the 42 filesystem directories holding a `packages/*/package.json`: **`in lock not fs: []`, `in fs not lock: []`** — a true bijection, no mismatch. Also 42 `node_modules/*` records whose `resolved` points into `packages/`. 12 additional lock records are nested `packages/*/node_modules/*` paths, correctly excluded by W2's stated rule. **[Static code evidence]** |
| 4 | Both sweeps repeated and recorded dry | **FAIL — substantive in form, wrong in conclusion** | The recorded sweeps are *substantive*, not merely asserted: W1 L133/L135, W2 L105, W4 L126/L128 each state a deterministic enumeration rule, name the surfaces re-checked, and retain honest residue. I reproduced W2's stated rule and it does what it says. **But the rule is JS/Rust-only** — it enumerates `package.json`, `Cargo.toml`, `package-lock.json` and nothing else — so the recorded "dry" is an artifact of the rule's alphabet, not a property of the repository. Both sweeps are **not dry** (§5). |

Repairs 1–3 clear. Repair 4 does not.

---

## 3. Per-predicate table (all six SCOPE predicates)

| # | Predicate | Verdict | Evidence |
|---:|---|---|---|
| 1 | 100% component accounting | **REWORKABLE** | The npm/Cargo side is now closed and correct: 42 workspace rows (N01–N42), 5 root Cargo members (R01–R05), R03-P, X01–X13, 16 top-level tracked directory families (I confirmed exactly 16: `.claude-plugin .codex .github .ruvnet-brain __tests__ apps crates docs examples examples-packages experiments kimi-k3-harness packages scripts services submissions`). **Unowned:** `packages/arc-agi-3/python/**` — a 868-line first-party Python component (`bridge.py`) that the package's own npm `files` field ships (`"files": ["dist/**","python/**","README.md","LICENSE"]`). It is a distributed first-party component in a language W1's inventory never admits exists. 48 tracked `*.py` files in total; most are benchmark fixtures, but `packages/arc-agi-3/python/bridge.py` and `packages/darwin-mode/bench/terminal-bench/darwin_terminal_agent.py` are authored program code. **[Static code evidence]** |
| 2 | 100% declared-edge accounting | **REWORKABLE** | 42/42 lock reconciliation is genuine and complete (§2.3). **Unowned:** two tracked dependency-declaration files in a third ecosystem — `packages/arc-agi-3/python/requirements.txt` (`arc-agi==0.9.8`, `arcengine==0.9.3`) and `packages/darwin-mode/bench/terminal-bench/requirements.txt` (`terminal-bench>=0.2.18`). No lockfile, no license closure, no transitive resolution, no W2 row. Worse than omission: **W2 L37 records `arc-agi-3`'s third-party column as `—` (none)**, which is affirmatively wrong. Also unowned: `python3` as an external executable. W2 L78 lists external executables as "cargo, wasm-pack, npm/npx, git, gcloud, Docker/host CLIs" scoped to `packages/scripts`; my independent sweep of `packages/*/src` + `packages/*/bin` + `scripts` + `apps/*/src` + `services/*/src` + `kimi-k3-harness` returns spawn-literal frequencies `gcloud 7, git 4, npm 2, node 2, unshare 1, readlink 1, python3 1, ps 1, powershell.exe 1, cargo 1` — `python3` and `unshare` are neither listed nor script-scoped: both are spawned from *shipped package source*. **[Static code evidence]** |
| 3 | 100% ecosystem-reference accounting | **PASS (unaffected by rework)** | W3 untouched by `17ebf2e`. Spot-checked its lexical ledger against the checkout: `ruflo` 752 (W3: 752), `claude-flow` 145 (145), `agentic-flow` 5 (5), `RUFLO_` 47 (47), `ruvector` 1078 (W3: 1073), `github.com/ruvnet` 425 (W3: 429), ruflo-family files 153 (W3: 156). Four exact matches and three within <1%, consistent with a slightly different matcher/prune. The sweep is real and independently reproducible. The Task-1 correction does not touch it. The Python surface introduces no new `ruvnet` identity (`arc-agi`/`arcengine`/`terminal-bench` are third-party, not `ruvnet`), so §5's residue does not ripple into P3. |
| 4 | Complete generation and authority chains | **REWORKABLE** | G1–G14 closure survives G15: G15 is purely additive, no row renumbered, ledger reads `G1…G15` contiguously, and W4's closure paragraph re-enumerates all fifteen. The 37-count correction inside G12 is consistent with §1. **Unowned authority paths:** (a) `packages/arc-agi-3/src/python-bridge.ts` (983 lines) — a network endpoint (`DEFAULT_ARC_BASE_URL='https://three.arcprize.org'`), a host allowlist (`DEFAULT_ALLOWED_ARC_HOSTS=['three.arcprize.org']`), a default operation mode of `'online'`, and **credential forwarding to a subprocess** (`ARC_API_KEY` on the inherited-env allowlist), with stderr deliberately never mirrored into errors "where it could expose credentials". None of this appears in W6's authority-and-data-flow map (10 rows) or gate-and-bypass matrix (7 rows), nor in W4's hidden-prerequisite list. (b) `packages/projects/src/sandbox.ts` — a first-party OS-level isolation gate (`unshare -rn`) whose **default is fail-open**: `buildSandboxArgv()` returns the command *unwrapped* when the probe fails, and the probe result is cached once at module load. `runSandboxed()` has **no production caller** — the only importers are its own module and `packages/projects/__tests__/sandbox.test.ts`; `index.ts` re-exports it and `safety-rails.ts` merely names a `no-bypass-sandbox` rail. Meanwhile `packages/projects/src/verifiers.ts` *specifies* the unsandboxed vector in the shared verifier contract (`PYTHON = { bin:'python3', args:(file,argsJson)=>['-I','-B',file,argsJson] }`, L102–105) without routing it through `buildSandboxArgv()`, and **ten** direct call sites consume that vector — `packages/projects/bin/darwin-discover.mjs` L130 plus nine `bench/*.bench.mjs` files (`zero-day-discovery` L125, `proposer-bakeoff` L76, `model-bakeoff` L88, `escalation-llm` L86, `learning-loop` L53, `learning-loop-large` L54, `frontier-multiseed` L49, `frontier-multiseed-large` L88, `chinese-frontier-bakeoff` L61) — each calling `execFileSync('python3', …)` **directly, bypassing the sandbox**. The bypass is **partial**: all ten replicate the env-hygiene half (`-I -B`, `env:{PATH, PYTHONDONTWRITEBYTECODE}`, 5s timeout) but none the namespace half, so the specific unmitigated exposure is **network access for untrusted generated code** — precisely what `sandbox.ts` L5–11 says the module exists to prevent. That is a decision-point / protected-operation / default / bypass-surface row of exactly the kind predicate 4 requires, and it is absent. **[Static code evidence]** |
| 5 | Delta closure | **PASS (unaffected by rework)** | W7 untouched by `17ebf2e`; its wfh-005 claim table and wfh-007 concept table remain intact (35 outcome-token lines). No Task-1 correction ripples into it. One accuracy note, non-blocking: **W2 L101 states "the current root manifest is `metaharness` 0.4.7"**. The root manifest is `agent-harness-generator` 0.1.0 (private, `workspaces:["packages/*"]`); `metaharness` 0.4.7 is `packages/create-agent-harness`. The substantive delta claim ("materially larger than the wfh-005 snapshot; do not carry earlier dependency counts forward") is unaffected, but the sentence names the wrong manifest. **[Static code evidence]** |
| 6 | Loop until dry | **REWORKABLE** | Both of my independent sweeps returned **not dry** (§5). The researchers' recorded sweeps are procedurally substantive but conclude "dry" on the strength of a JS/Rust-only enumeration alphabet. |

---

## 4. Independent residue sweep 1 — manifests, lockfiles, build metadata

**Method:** ecosystem-agnostic. Rather than enumerating `package.json`/`Cargo.toml`/`package-lock.json`, I enumerated *every* dependency- or build-declaring filename pattern across all tracked files:

```
$ git ls-files | grep -Ei '(^|/)(package\.json|package-lock\.json|Cargo\.toml|Cargo\.lock|pyproject\.toml|
    requirements[^/]*\.txt|setup\.py|Pipfile|go\.mod|Gemfile|composer\.json|pom\.xml|build\.gradle|
    Dockerfile|docker-compose[^/]*\.ya?ml|\.tool-versions|rust-toolchain\.toml|deny\.toml|renovate\.json|
    \.nvmrc|flake\.nix|Makefile|justfile)$'
```

**Result: NOT DRY.** The sweep returns everything W1/W2/W4 already own (84 `package.json`, 10 `Cargo.toml`, 3 `package-lock.json`, `deny.toml`, `renovate.json`, `rust-toolchain.toml`, `services/apicompletions/{Dockerfile,docker-compose.emulators.yml}`, 13 `*.tf` of which 3 are the service's Terraform and 10 are `packages/aws-finops` benchmark corpus fixtures) **plus two files no workstream owns**:

- `packages/arc-agi-3/python/requirements.txt` → `arc-agi==0.9.8`, `arcengine==0.9.3` (exact pins, no lock)
- `packages/darwin-mode/bench/terminal-bench/requirements.txt` → `terminal-bench>=0.2.18` (unbounded range, no lock; comment claims verification against `terminal-bench==0.2.18` + `terminal-bench-core==0.1.1`)

**New unowned dependency class:** a **third package ecosystem (PyPI)** with declared direct edges, zero lockfile coverage, zero license/provenance closure, and no representation in W2's node/edge tables — while W2 records `arc-agi-3`'s third-party dependencies as `—`. `bridge.py` itself hard-codes `EXPECTED_SDK_VERSIONS = {"arc-agi": "0.9.8", "arcengine": "0.9.3"}`, so the pin is duplicated in code and will drift against the manifest independently.

No fourth npm lock root, no eleventh Cargo manifest, no other ecosystem (no Go, Ruby, PHP, Java, Nix, Make). Absent Cargo/Kimi/example locks remain honest unknowns.

**[Static code evidence]**

---

## 5. Independent residue sweep 2 — source, config, docs, runtime references

**Method:** independent of the researchers' narrative. Spawn/exec literal frequency across shipped source and bins; tracked-source enumeration by extension; ecosystem-token counts (§3, P3); interpreter/network/credential/isolation call-site tracing.

**Result: NOT DRY.** Four specific unowned items, all one connected class:

1. **`python3` as a runtime prerequisite of shipped code.** `packages/arc-agi-3/src/python-bridge.ts` L492 `const executable = options.pythonExecutable ?? 'python3'` and L494 resolves `../python/bridge.py` relative to `import.meta.url`; `packages/projects/src/verifiers.ts` L103–104 declares `PYTHON: VerifierSpec = { language:'python', bin:'python3', … }`, compiled into `dist/**` which is the package's only shipped payload. Not a script-only tool — a hard operational prerequisite of two published packages. W2's external-executable row does not list it.

2. **A shipped cross-language component.** `packages/arc-agi-3` `files` includes `python/**`; the tarball carries a 868-line Python bridge to the ARC-AGI-3 SDK. `PythonArcBridge` is a long-lived, serial, fail-closed JSON-lines subprocess client, 983 lines. No W1 component row, no W2 edge, no W5 extraction dossier.

3. **An unowned network + credential authority path.** Default base URL `https://three.arcprize.org`, host allowlist `['three.arcprize.org']`, default operation mode `'online'`, `ARC_API_KEY` forwarded into the child via an explicit inherited-env allowlist, stderr drained-but-never-surfaced to avoid credential leakage, `PYTHONPATH` scrubbed (the test suite asserts `spawnOptions.env.PYTHONPATH` is `undefined`). Absent from W6's gate/bypass matrix and from W4's hidden-prerequisite ledger.

4. **An unowned isolation gate with a fail-open default and no live call site.** `packages/projects/src/sandbox.ts` wraps commands in `unshare -rn` (new user + network namespace, no interfaces) specifically because "the discovery/verifier pipeline runs GENERATED and THIRD-PARTY code (proofs, candidate exploits, untrusted snippets)". `sandboxAvailable()` probes the *real operation* (`unshare -rn true`), not the binary's presence — a genuinely good pattern. But `buildSandboxArgv()` returns the bare command when unavailable (**fail-open**), the probe is cached once at import, and `runSandboxed()` has no production caller (only its own test suite). `verifiers.ts` performs **no process execution at all** — it has no `child_process` import and its own header L13–14 says so — but it *specifies* the unsandboxed vector (`PYTHON = { bin:'python3', args:(file,argsJson)=>['-I','-B',file,argsJson] }`, L102–105), which never routes through `buildSandboxArgv()`. Ten direct call sites execute that vector: `bin/darwin-discover.mjs` L130 and nine `bench/*.bench.mjs` files. That makes the bypass **contractual rather than incidental** — specified once in the shared registry, inherited by every consumer. It is also **partial**: all ten carry the env-hygiene half (`-I -B`, `env:{PATH, PYTHONDONTWRITEBYTECODE}`, 5s timeout, commented “clean env — no API key in the child”) but not the namespace half, leaving **network egress** as the unmitigated exposure — the exact risk `sandbox.ts` L5–11 names. `unshare` also never appears in W2's executable list.

**Confirmation that this is a true gap, not a wording difference:** a case-insensitive grep for `terminal-bench|arcengine|pypi|\bpip\b|\.py\b|python` across `findings-W1.md` … `findings-W7.md` **and** round-1 `reports/coverage.md` returns **zero matches**. A grep for `arcprize|three\.arc|allowlist.*host|network endpoint` returns only two generic late-binding-policy sentences (W4 L117, W5 L97) that name the *category* without owning any instance. A grep for `unshare|sandbox|namespace|isolat` in W6 returns only the Prime Agent `SANDBOX-REQUIRED.md` row and a generic caveat — nothing about `packages/projects`.

**[Static code evidence]** for every path and literal above; **[Unverified-inference]** only where noted.

---

## 6. Owner-amendment check (Issue #66, 2026-08-28T12:27Z)

**PASS — not degraded, but now incomplete on the same axis as the sweeps.**

The rework was additive and preserved the CODE/CONCEPT split everywhere it touched. Both new entries carry it: W2 L67 gives R03-P a CODE disposition (build-only, range-unlocked, no independent lock) and W4 G15 gives it a CONCEPT read (statically-connected generation with an explicitly orphaned packaging step). W3/W5/W6/W7 are byte-identical to round 1, so the round-1 PASS across those stands unchanged.

The amendment is not *degraded*. It is *under-served* on the unowned surface: `packages/projects/src/sandbox.ts` is one of the strongest clean-room CONCEPT candidates in the whole repository for Jurati — **probe the actual capability, not the binary's presence** — and the run currently proposes neither its code nor its concept, because it never saw the file. Likewise the `PythonArcBridge` fail-closed serial subprocess protocol with an env allowlist and scrubbed `PYTHONPATH` is a portable concept the run does not carry. This is upside the rework should capture, not a defect in what it wrote.

---

## 7. Recommendation

### REWORKABLE

This consumes the run's final rework allowance. I would not spend it on §1 — the counts are correct and I say so plainly. I spend it because sweep 1 and sweep 2 both return a **genuinely unowned class**, not cosmetic wording: a third package ecosystem with unlocked declared edges, a shipped cross-language component, an interpreter prerequisite of published packages, a network/credential authority path, and a fail-open isolation gate that the live execution sites bypass. Predicate 6 cannot be certified dry against that.

It is **not** SCOPE-FAIL. Every item is inside `ruvnet/metaharness` at the pinned commit. No boundary expansion, no build recommendation, no cross-theme dependency, no spend, no validated follow-on. **Nothing here requires escalation.**

### Minimal repair list

1. **W2** — add a Python/PyPI dependency class: both `requirements.txt` files, their declared edges (`arc-agi==0.9.8`, `arcengine==0.9.3`, `terminal-bench>=0.2.18`), the absent lock/license closure as explicit unresolved residue, and **correct L37's `arc-agi-3` third-party column from `—`**. Add `python3` and `unshare` to the external-executable row and de-scope that row from "packages/scripts" to shipped source.
2. **W1** — own `packages/arc-agi-3/python/**` as a first-party shipped cross-language component (note the `files: ["python/**"]` distribution boundary).
3. **W6** — add two gate rows: (a) the ARC Python bridge (decision point, protected operation, `ARC_API_KEY` custody, host allowlist, default `online`, `PYTHONPATH` scrub, evidence label); (b) `packages/projects/src/sandbox.ts` (protected operation = execution of generated/third-party code; default = **fail-open** when `unshare -rn` probe fails; bypass surface = the unsandboxed vector specified in `verifiers.ts` L102–105 and executed directly by `bin/darwin-discover.mjs` L130 plus nine `bench/*.bench.mjs` files, with env hygiene but no namespace isolation ⇒ network egress; `runSandboxed()` has no production call site).
4. **W4** — record the Python bridge's runtime prerequisites (interpreter, two PyPI SDKs at exact pins duplicated in `bridge.py`'s `EXPECTED_SDK_VERSIONS`, network reachability of `three.arcprize.org`, credential) as hidden operational prerequisites.
5. **W5/W7** — carry the CONCEPT the sandbox module offers ("probe the real operation, not the binary") and the bridge's fail-closed subprocess protocol; note the fail-open default as the counter-lesson.
6. **Optional, non-blocking:** correct W2 L101's "root manifest is `metaharness` 0.4.7" to `agent-harness-generator` 0.1.0 (`metaharness` 0.4.7 is `packages/create-agent-harness`).
7. **Optional, non-blocking:** widen W4 L31's `-mindepth 2 -maxdepth 2` rule to any-depth-with-`node_modules`-pruned. It is correct at this commit (37 = 37, verified) but is a rule that *could* hide a manifest at a future cutoff; W1's rule is already any-depth. Do not change the number — 37 is right.

**No count in W1/W2/W4 needs to change.** 84 / 42 / 37 / 4 / 1 / 10 / 3 are all correct as written.

---

## 8. Residual gaps — honest unknowns, not inferred closures

- The **round-1 over-count is unattributed**. No path in the pinned tree yields 38; I decline to name a cause I cannot evidence.
- **PyPI transitive closure and licensing** for `arc-agi`, `arcengine`, `terminal-bench` are unresolved. Resolving them needs a registry fetch this envelope does not permit.
- **No lockfile exists** for Cargo, for `kimi-k3-harness`, for the 37 example packages, or for the Python surface. Transitive version and license closure is open on all four.
- The `unshare` sandbox's **effectiveness was not tested** — I did not run `unshare -rn`, `python3`, or any verifier. That it *appears* fail-open in `buildSandboxArgv()` is static structure; whether an operator ever reaches the bypassing path is unverified.
- `runSandboxed()`'s **absence of an in-repo caller** is static-grep evidence at this commit. It does not prove the function is dead — a consumer outside the repo could import it from `@metaharness/projects`'s exports.
- Root script `build:napi` emits `--output-dir ../../packages/kernel-js/native`, but `packages/kernel-js` `files` omits `native/**`, its `tsconfig` excludes `native`, and `loadNative()` imports only the five `@metaharness/kernel-{platform}` registry names — never a relative `./native` path. That output directory has **no static consumer**. This *strengthens* G15's "orphaned packaging step" call rather than contradicting it, but G15 names only the CI `crates/kernel-napi/*.node` output, not this second producer path. Minor, within an already-owned generator; listed here rather than in the repair list.
- **Nothing in this report is demonstrated-by-us evidence.** No code was executed. Static structure can establish that a path exists and is reachable-looking; it cannot establish that it runs.
- This audit performed **no Unimatrix writes** and does not attest the live contents of `#312`–`#315`, `#200`, or `#277`.


---

## 9. Final verification note — amended 2026-08-28 (second amendment)

**Ruling on rework pass 2 (`3cd296d`): PASS.** Coverage sufficient, with the gap register below as the honest residual. Subject to the coordinator's mechanical confirmation and the human synthesis gate.

Same envelope as §1–§8: fresh pinned checkout at `6f8c60216f47eac391a076fe27fd804470a07e10`, static inspection only, nothing executed, no Unimatrix writes. Read-only `git diff 7d28294..3cd296d` and `git show` in the research repo; nothing staged or committed by me.

### 9.1 Task A — the six repairs, verified against the repository

| Repair | Verdict | Independent evidence |
|---|---|---|
| W1 owns `packages/arc-agi-3/python/**` (row `N03-PY`) | **PASS** | Row present, correctly typed as a *component* row rather than a manifest row. I tested W1's strongest new claim — that `bridge.py` is "the only authored non-JS/Rust program code inside a package `files` allow-list at this cutoff" — by expanding every `files` glob in all 84 manifests against `git ls-files` and filtering for program extensions (`.py .sh .rb .pl .php .lua .r .jl .go .java .ps1`). Exactly one hit: `packages/arc-agi-3/python/bridge.py`. **The claim is exactly true.** |
| W2 Python/PyPI class; L37 `—` corrected; external-executable row rebuilt | **PASS, with wording defects (§9.3)** | §4a exists with both `requirements.txt` files, their pins, ship/no-ship split, and zero-lock/zero-license residue. L38 now carries the PyPI edges where `—` stood. The widened-alphabet claim holds: no `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock`, `uv.lock`, `go.mod`, `Gemfile`, `composer.json`, `pom.xml`, `build.gradle`, `flake.nix`, `Makefile` or `justfile` exists in the tracked tree. `packages/scripts` genuinely does not exist — the scope correction is right. Undeclared-import list verified exhaustively: the complete non-stdlib import set across all 48 tracked `.py` files is `flask, lcb_runner, pandas, pydantic, retort, retort_metaharness, terminal_bench, yaml` — exactly what W2 enumerates and classifies. |
| W4 hidden prerequisites; G12 widened to any-depth; new G16/G17 | **PASS** | `G1…G17` contiguous, no renumbering, closure paragraph re-enumerates all seventeen, every row carries inputs/outputs/consumers or a named orphan. G17's counts verified exactly: `git ls-files submissions \| wc -l` = **1071**; `submissions/**/*.sh` = **265**; `git grep 'submissions/' -- ':!submissions/'` returns exactly the two prose references W4 names and **no writer**. G16 verified: `run.sh` L10 `OPENROUTER_API_KEY=…$(cat /tmp/.orkey)`, L13 `uv tool install terminal-bench`, L14 `tb datasets download -d terminal-bench-core==0.1.1`. |
| W6 two gate rows; sweep-completeness claim withdrawn | **PASS, with one numeric defect (§9.3)** | Both rows present with decision point, protected operation, authority owner, default, bypass surface and evidence label. The withdrawal is explicit and correctly scoped: W6 "no longer asserts that its gate enumeration is closed… only that it is closed *against an operation-driven sweep at this cutoff*." It also records that the fail-open branch is **read from source, not witnessed**. That is the right epistemic posture and the strongest single signal in this pass. |
| W5/W7 dossiers, dispositions, concepts + counter-lesson, six `new` delta rows | **PASS** | Verified W5's falsifiable claims: `sandbox.ts` is 131 lines (`wc -l` = 131); `packages/projects/` contains **no `LICENSE` file** despite its `files` naming one — the license gap is real; `packages/darwin-mode/src/sandbox.ts` exists and contains **zero** occurrences of `unshare`, so the naming-collision warning is warranted; `safety-rails.ts` L33 declares `bypassesSandbox: boolean` inside `interface CandidateChange`, confirming the rail's only input is authored by the governed proposer. W7's six `new` rows are correctly graded `new` and its two scorecard revisions (mixed → mixed/weak) follow from the evidence rather than from mood. |

**Counts: unmoved and correct.** W1's ledger still reads 42 / 5 / 1 / 37 / 4 / 84 / 4 / 10 / 16, and W2 L131 states explicitly that a `requirements.txt` is not a package manifest so "84 / 42 / 37 / 4 / 1 / 10 / 3 stand exactly as written." Re-verified against the checkout. The new W1 ledger line ("first-party shipped cross-language components: 1") adds a class without disturbing a count.

**W5 and W6 do not contradict each other on `sandbox.ts`.** Both reach the same two-altitude disposition independently: **reuse candidate at probe-function altitude** (`sandboxAvailable()` extracted alone, wrapper inverted to fail closed) and **reference only at module altitude**. W5 §67 states the match explicitly; W5's dossier table and W6's reuse table agree. No conflict.

### 9.2 Task B — the ruling on SCOPE predicate 6

**These are unresolved edge/provenance questions that predicate 6 permits, not a new unowned class. The leader's reading of the predicate is correct — but I did not clear it on that reading alone, because the reading was offered by the party with an interest in it. I tested each item against the predicate's own six stop-condition categories.**

Predicate 6 stops when neither sweep surfaces a new unowned **component · dependency class · ecosystem tie · generator/consumer chain · authority path · prior-art delta**, and then states: "Unresolved dynamic or provenance questions remain visible as gaps; they do not become inferred closures." Item by item:

| Open item | Category test | Ruling |
|---|---|---|
| `retort` / `retort_metaharness` | Not a component (the importing files sit in W1's `docs` family, X12). Not a dependency *class* (the Python class is owned; this is an undeclared *edge* within it, explicitly enumerated). Not an ecosystem tie under predicate 3, which is lexically scoped to `ruvnet`/`ruflo`/`claude-flow`. | **Permitted gap.** The refusal to infer first-party was correct, and §9.4 adds evidence that makes the gap *characterizable* rather than merely open. |
| Undeclared imports `pydantic`, `lcb_runner`, `pandas`; fourth distribution `terminal-bench-core==0.1.1` | Edges inside the now-owned PyPI class, each named with its file. | **Permitted gap.** |
| PyPI transitive / platform / license closure | Requires a registry fetch **this scope's own envelope forbids**. A predicate cannot be failed for a gap its own constraints mandate — and SCOPE's known-constraints already prescribe the handling: "Absence or ambiguity is a constraint, not permission." W5 executes exactly that, making unresolved licensing the *determining constraint* that rules the ARC bridge not importable. | **Permitted gap, correctly handled.** |
| `G17` / `submissions/**` — 1,071 files, no writer | Predicate 4's own text admits this shape verbatim: "every identified generator has inputs, outputs, and consumers **(or a named orphan)**." G17 names the orphan and shows the grep. | **Permitted, explicitly, by the predicate's own parenthetical.** |
| Whether a *published* consumer calls `runSandboxed()` | Unanswerable from this repository; answering it means surveying npm consumers, outside both the single-target boundary and the envelope. W6/W5 bound the claim correctly (`export *` re-export) and note it "only bounds the dead-code claim" without repairing the fail-open default or the in-repo bypass. | **Permitted gap, correctly bounded.** |

**Why I am not passing this on the researchers' word.** Their own pass-2 sweep 1 came back **not dry** — it is what surfaced the two `requirements.txt`. Read strictly, predicate 6's loop therefore requires a further sweep after the pass-2 repairs to establish dryness, and a self-reported one would be exactly the instrument that failed twice. So the basis for PASS is **my own third independent sweep**, run this round over an ecosystem-agnostic filename alphabet and an operation-driven spawn/exec/interpreter pass: it surfaced **no new component, dependency class, ecosystem tie, generator/consumer chain, authority path, or prior-art delta**. Only JS, Rust and Python exist in this tree; every external executable my sweep returned (`gcloud, git, npm, node, unshare, readlink, python3, ps, powershell.exe, cargo`) is now owned by W2. **Both sweeps are dry at the class level. That is the finding, and it is mine, not theirs.**

**Not SCOPE-FAIL.** No item expands the boundary. `retort` points outside `ruvnet/metaharness`, but SCOPE legislates that case directly — "A newly discovered technology outside the single-target boundary is captured as a follow-on candidate, not absorbed into this scope" — so the prescribed handling is a follow-on candidate, not a boundary breach. I judged this below the escalation bar and say so rather than leaving it implied.

**Not REWORKABLE.** The four defects in §9.3 are precision and wording inside classes that are owned. By the standard I set for myself in §7 — spend an allowance only on a genuinely unowned class, never on cosmetic wording — none qualifies, and there is no allowance to spend. They are curator instructions, not rework triggers.

**One honest qualification on the verdict.** Dryness is established against a *static* instrument at a *single* commit. A class reachable only through a dynamic import, a generated harness, or an out-of-repo consumer would still be missed. W6 says this about itself, unprompted, and that self-limitation is why I believe the rest of its ledger.

### 9.3 Asserted but not true — four defects, all corrections rather than rework

Ordered by consequence for the curator, who carries claims into the graph verbatim.

1. **W2 §4a overstates "shipped."** It calls `packages/arc-agi-3/python/requirements.txt` "**shipped** … so the tarball carries `python/bridge.py`." `@metaharness/arc-agi-3` is `"private": true` (verified), so there is no published tarball. W6 row 73 and W7 both get this right — "`files` … is a packing boundary, not a published one" — and W2 itself draws exactly this distinction correctly for `kernel-napi` at L21. **Reconcile W2's wording to W6/W7 before distillation**; "MetaHarness ships a Python bridge in its npm tarball" would enter the graph as a wrong fact. (It also slightly softens my own §3 P1 wording, which W7 flagged; W7's sharpening is correct and I accept it.)
2. **W6 miscounts the env allowlist.** It says "the 18-key `INHERITED_ENV_KEYS` allowlist (L35–53)." The array at L35–53 contains **17** keys (`PATH, Path, PATHEXT, SYSTEMROOT, SystemRoot, WINDIR, COMSPEC, TMPDIR, TEMP, TMP, LANG, LC_ALL, LC_CTYPE, MPLCONFIGDIR, ARC_API_KEY, ARC_BASE_URL, ARC_OPERATION_MODE`). Line range correct, count off by one.
3. **W2 residue item 3 is too narrow.** `terminal-bench-core==0.1.1` is not "named only in a comment": `run.sh` L14 executes `tb datasets download -d terminal-bench-core==0.1.1`. W4's G16 cites the download correctly. W2's wording should follow W4's.
4. **W2 §4 external-executable row repeats the `verifiers.ts` conflation.** The row is headed "`execFileSync`/`spawn` literals inside `packages/*/src` and `packages/*/bin`" and then cites `verifiers.ts` L104. `verifiers.ts` contains no `execFileSync`/`spawn` — it *specifies* the vector and executes nothing (its own header L13–14). This is the identical error corrected in my first amendment above; W5 §161 and W6 both state it correctly. The underlying finding — `python3` is a runtime prerequisite of shipped source — is independently true via `python-bridge.ts` L492 and `bin/darwin-discover.mjs` L130 and is unaffected.

### 9.4 New evidence this round — it closes nothing, but it characterizes the `retort` gap

`docs/research/retort-placement/analyze2.py` L18–23 reads:

```
G2 = Path("/tmp/claude-1000/-home-ruvultra-projects-agent-harness-generator/ec35bf87-…/scratchpad/grid2")
RETORT = G2.parent / "retort"
sys.path.insert(0, str(RETORT / "src")); sys.path.insert(0, str(RETORT))
from retort_metaharness import analysis as mz_analysis
from retort.analysis.pareto import pareto_analysis
```

`retort` is loaded by absolute path from a **transient agent-session scratchpad on the author's machine** (`/home/ruvultra/projects/agent-harness-generator`), a sibling of a `grid2` results directory. So these modules are **unresolvable by construction, not by omission**: they were never distributed, never vendored, and the path cannot be reconstructed by any consumer. This *strengthens* the researcher's refusal to call them first-party rather than weakening it, and it upgrades the entry in the gap register from "resolves to nothing" to "host-local, non-reproducible research residue." The `ruvultra` path segment is circumstantially owner-adjacent, which is **not** evidence that `retort` is a `ruvnet` project; I decline to infer it, and record `retort` as a **follow-on candidate** for the coordinator under SCOPE's out-of-boundary rule. Predicate 3 is unaffected — it is lexically scoped to `ruvnet`/`ruflo`/`claude-flow`, and `retort` is none of those.

Consequence for `docs/research/retort-placement/**`: it is **non-reproducible research residue**, not runnable first-party code. Its committed JSON outputs cannot be re-derived from this repository — the same property W4 records for G16 and G17. Worth one line wherever those two are cited.

### 9.5 Gap register — the honest residual behind this PASS

1. PyPI transitive, platform-wheel and license closure for `arc-agi==0.9.8`, `arcengine==0.9.3`, `terminal-bench>=0.2.18`: open on every axis; no lockfile exists; resolving requires a registry fetch outside this envelope.
2. Undeclared Python imports `pydantic`, `lcb_runner`, `pandas`; fourth distribution `terminal-bench-core==0.1.1` declared by no manifest.
3. `retort` / `retort_metaharness`: host-local, non-distributed, unresolvable by construction (§9.4). Captured as a follow-on candidate, not absorbed.
4. `submissions/**` (G17): 1,071 checked-in files with no writer in any tracked script; owner-published evidence, **not** demonstrated-by-us evidence, and not re-derivable here.
5. G16's Terminal-Bench outputs: likewise not re-derivable — transient outputs are `.gitignore`d and the dataset is fetched out-of-repo.
6. Whether any published consumer of `@metaharness/projects` calls `runSandboxed()`: unanswerable from this repository.
7. The fail-open sandbox branch, the ARC credential path, and every execution site are **read from source, never witnessed**. Nothing in this run is demonstrated-by-us evidence.
8. Class-level dryness holds against a static instrument at one commit; dynamic-import, generated-harness and out-of-repo-consumer surfaces remain structurally out of reach.
9. No lockfile exists for Cargo, `kimi-k3-harness`, the 37 example packages, or the Python surface — four independent unlocked closures.
10. This audit performed **no Unimatrix writes** and attests nothing about the live contents of `#312`–`#315`, `#200`, or `#277`.
