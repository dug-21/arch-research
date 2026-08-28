# wfh-008 — REPORT: MetaHarness architecture and ecosystem dependency analysis

**Run:** `wfh-008` · **Phase:** synthesis · **Author:** `factory-curator` (single writer)
**Goal / theme:** workflow-harness — inform the smallest defensible personal-OS/Jurati substrate
**Capability target:** proposed `jurati-arch-002`. It has no Unimatrix capability id. **No capability or
technology grade is advanced by this run.** `#316` (formerly `#312`) stays `grade:claimed`.
**Confidence-required:** directional.

**Target and pin:** `ruvnet/metaharness` @ **`6f8c60216f47eac391a076fe27fd804470a07e10`**, retrieved
**2026-08-28**. Origin comparison only: `ruvnet/ruflo` @ `d33ef4bf8ab27a8f9ef08352c9c293b53312a861`,
retrieved 2026-08-28. Pin independently verified by the round-2 auditor with a fresh clone plus explicit
checkout; `git ls-remote` showed the remote unmoved at the same SHA.

**Method and envelope:** static inspection only. Nothing was installed, built, generated, tested,
benchmarked, fetched from a registry, or executed — not by the researchers, not by either coverage
auditor, not by this curator. **Nothing in this run is demonstrated-by-us evidence.**

**Evidence labels** (every material claim below carries one):

- **[SC]** source claim — documentation, ADR, comment, name, or owner assertion.
- **[SCE]** static code evidence — a traced authored/generated code or configuration path. Establishes
  structure and reachable-*looking* paths; never that a path executes correctly.
- **[PDE]** prior demonstrated evidence — an artifact demonstrated by an earlier garage run.
- **[UI]** unverified-inference.

**Inputs:** `findings-W1.md` … `findings-W7.md` at commit `962a6c1`; `reports/coverage.md` (round 1,
REWORKABLE); `reports/coverage-r2.md` (round 2, REWORKABLE → **PASS** at §9 on rework pass 2 `3cd296d`).

---

## 0. Bottom line

**[SCE]** MetaHarness is a broad, fast-moving, pre-1.0 **generator portfolio across three package
ecosystems** — not one dependency closure, not a control plane, and not a live wrapper around ruflo. It
contains real deterministic mechanisms and several genuinely good ideas. It does not contain an authority
boundary Jurati could adopt, and its most reusable *code* is a handful of small source-level functions.

**The CONCEPT column is this run's higher-value half, and that is a finding rather than a consolation
prize.** [UI] The evidence for it is asymmetric in a way worth stating plainly:

- The **CODE** column is genuinely thin. One dependency-free router core is the strongest candidate. A
  probe function is worth extracting only if its wrapper is inverted. The ARC bridge is ruled
  `inseparable` on **license closure alone** — before any question of quality arises. Everything else is
  `reference only` or `insufficient evidence`.
- The **CONCEPT** column transfers directly to a theme whose value-target is **enforcement living outside
  the governed party's reach** — and MetaHarness supplies both the positive pattern and, in the same 131
  lines, its sharpest counter-example.

The CODE column is not padded in this report to make the two look balanced. It is short because it is
short.

---

## 1. Commit-pinned architecture and component-boundary map *(SCOPE output 1)*

**[SCE]** Two explicit root workspaces, three substantial surfaces outside both, and a third package
ecosystem no root manifest can express. Neither root manifest is a complete architecture index.

```text
ruvnet/metaharness @ 6f8c602
├── root npm orchestrator  (agent-harness-generator 0.1.0, private; workspaces = packages/* exactly)
│   └── 42 workspace packages: generator/API · dual CLI (metaharness 0.4.7) · JS kernel bridge
│       · 10 host adapters · SDK/verticals/integration · evaluation, benchmark, autonomy,
│         research and experimental packages
├── root Cargo workspace (5 members: kernel, kernel-wasm, kernel-napi, template-catalog, poker-darwin)
├── non-workspace products: apps/web-ui · services/apicompletions (DEPRECATED) · kimi-k3-harness (+2 crates)
├── distribution/config projections: .claude-plugin (13 skills) · .codex (13 skills)
├── generated/published exemplars: examples-packages/* (37 manifests)
├── cross-language component: packages/arc-agi-3/python/** (bridge.py, 868 lines + requirements.txt)
└── examples · experiments · submissions (1,071 files) · docs/ADRs · scripts · CI
```

**[SCE] Completeness ledger, independently re-derived twice and settled:** 84 `package.json` total = 1
root + 42 workspace + 37 `examples-packages/*` + 4 other (`apps/web-ui`, `services/apicompletions`,
`kimi-k3-harness`, `crates/kernel-napi`); 10 `Cargo.toml` = 1 root + 5 members + 4 non-members; exactly 3
npm lockfiles; 16 top-level tracked directory families. The round-1 audit's "38 examples" was an
over-count; the round-2 auditor could not attribute it to any path at any depth and **declined to invent
an attribution** — recorded as [UI], not as a named cause.

**[SCE]** One first-party component sits outside the JS/Rust alphabet entirely:
`packages/arc-agi-3/python/**`. It is the **only** authored non-JS/Rust program code inside any package
`files` allow-list at this cutoff — verified by expanding every `files` glob in all 84 manifests against
`git ls-files` and filtering for program extensions: exactly one hit.

**[SC]** `docs/ARCHITECTURE.md` describes a three-layer model (Rust kernel → adapters → CLI/plugin).
**[SCE]** directionally recognizable but incomplete: it omits the evaluation, autonomy, benchmark,
research, web/service and nested-harness components the manifests contain.

---

## 2. Complete dependency graph, including ruflo/ruvnet ties *(SCOPE output 2)*

**[SCE] It is not one closure.** Three separately locked npm installations (root workspace 420 non-link
packages; web UI 247; service 301 — overlapping, never to be summed), one **unlocked** five-member Cargo
workspace, a separate npm/N-API build manifest inside one Cargo member, four detached unlocked crates, a
separately manifested Kimi harness, 37 unlocked example manifests, and a **third package ecosystem**.

**[SCE] First-party npm edges:** 45 declared first-party edges across the 42 workspace packages; 18
incoming-edge-free roots; 15 leaves; **no declared first-party cycle**. All 42 workspace manifests
reconcile one-to-one with the 42 root-lock `packages/<name>` records — a true bijection, verified as sets
in both directions.

**[SCE] The third ecosystem (PyPI), recorded for the first time in rework pass 2:**

| Declaring file | Declared edges | Lock | Licence | Class |
|---|---|---|---|---|
| `packages/arc-agi-3/python/requirements.txt` | `arc-agi==0.9.8`, `arcengine==0.9.3` (exact) | **none** | **none** | runtime for any consumer constructing `PythonArcBridge` |
| `packages/darwin-mode/bench/terminal-bench/requirements.txt` | `terminal-bench>=0.2.18` (unbounded) | **none** | **none** | benchmark/dev-only, repo-local |

Plus **[SCE]** undeclared imports `pydantic`, `lcb_runner`, `pandas`; and a fourth distribution
`terminal-bench-core==0.1.1` declared by no manifest yet fetched and used by `run.sh` L14/L18/L20.
**[SCE]** The `arc-agi` pin is **duplicated** — `requirements.txt` and `bridge.py`'s
`EXPECTED_SDK_VERSIONS` — with nothing reconciling the copies.

**[SCE] External executables spawned from *package source*, not repository tooling:** `python3`,
`unshare`, `gcloud`, `npm`, `git`, `readlink`, `ps`, `powershell.exe`. **[SCE]** `python3` has **no
declared version floor anywhere in the tree** — no `pyproject.toml`, no `python_requires`, no
`.python-version`, no `.tool-versions`.

**[SCE] ruflo / wider ruvnet:** **no declared `ruflo`, `@claude-flow`, `claude-flow` or `agentic-flow`
package or crate edge exists** in any manifest or lockfile. 752 `ruflo`, 145 `claude-flow`, 47 `RUFLO_`
lexical occurrences resolve into ancestry/provenance naming, copied contracts (claims, witness, routing),
a one-way eject importer, registry-shape compatibility, `RUFLO_*` state/env namespaces, and generated
artifact names — coupled by *convention*, not by dependency. **[SCE] The executable ecosystem coupling is
RuVector, not ruflo:** `@ruvector/emergent-time` is a required dependency of `@metaharness/kernel`;
`@ruvector/rvf`, `ruvllm` and `tiny-dancer` are optional peers/deps that expand into ~19 platform packages
in the lock, with wrapper/native version skew (`rvf-node` 0.2.3 vs natives 0.2.2). **[SC]** the owner gist
mandates coordination across the RuV stack; **[SCE]** no checkout path enforces it.

**[SCE] Deferred/undeclared:** the deprecated service names future Firebase/PubSub/tokenizer/
`@midstream/wasm` deps in a `deferred-deps` field; `agntcy` imports `@bufbuild/protobuf` by hoisting;
generated `host-pi-dev` output imports an undeclared `pi-agent-sdk` type.

---

## 3. Producer → artifact → consumer chains and hidden prerequisites *(SCOPE output 3)*

**[SCE]** Seventeen chains, `G1…G17`, each with inputs, outputs and consumers **or a named orphan**.
Headlines:

- **G1–G8 (CLI path).** catalog definition → generated templates/catalog → walk/render → host and feature
  overlays → fingerprints/manifest → adjacent staging directory → rename. **[SCE]** `--with-wasm` mutates
  output *after* fingerprinting, so the provenance record omits it; `template_version` is hard-coded
  `0.0.0`; `--force` deletes the target before rename and the EXDEV fallback is explicitly non-atomic.
- **G9–G10 (browser path).** A **second, independent** producer with an incompatible manifest shape, no
  per-file hashes, an unsigned witness stub, and a hard-pinned kernel. **[SC]** the browser MCP scaffold
  claims a gated stdio/HTTP server; **[SCE]** `start()` contains no transport or dispatch loop and remote
  auth is imported then discarded. Registries plus a gate are not a server.
- **G15.** `crates/kernel-napi` → five-target `.node` artifacts uploaded by CI. **[SCE]** the workflow's
  own comment says those artifacts are **not yet consumed** by the publish job — a statically connected
  producer with an explicitly orphaned packaging step.
- **G16 / G17.** Terminal-Bench outputs and 1,071 checked-in `submissions/**` files. **[SCE]** neither is
  re-derivable from this repository: transient outputs are `.gitignore`d, the dataset is fetched
  out-of-repo, and a repo-wide grep finds **no writer** for `submissions/`. Owner-published evidence,
  **not** demonstrated-by-us evidence.

**[SCE] The sharpest hidden prerequisite is not in the JS graph at all.** `packages/arc-agi-3` installs
through npm, satisfies its declared `dependencies` and `engines` completely, and still cannot function
without: a `PATH`-resolved Python interpreter with no declared version floor; two unlocked PyPI
distributions whose pins are duplicated in code; unconditional network egress to
`https://three.arcprize.org` (default mode `online`, **no offline path** — the bridge refuses the SDK's
local modes with `CONFIGURATION_ERROR`); and an `ARC_API_KEY`. **A manifest-only or single-ecosystem view
cannot see any of it** — which is exactly why two earlier residue sweeps recorded "dry".

### 3.1 The publication claim, stated precisely

This was corrected in **six** places before distillation and is repeated here so it is not re-introduced a
seventh time.

**[SCE]** `@metaharness/arc-agi-3` is `"private": true`, and `scripts/publish-workspace.mjs` skips any
private package. **Nothing is published from it at this cutoff; no tarball exists.** Its `files`
allow-list enumerates `python/**`, but **a `files` list is a packing boundary, not a published one.**

The accurate framing is **distribution-shaped**: the allow-list *already* enumerates `python/**`, so the
whole prerequisite class — interpreter, two unlocked PyPI pins, one required network origin, one
credential — becomes consumer-facing **the moment `private` is dropped, with no other change**.
**[SCE]** `@metaharness/projects` 0.1.2 and `metaharness` 0.4.7 carry no `private` flag and are
**publishable**; both are absent from `RELEASE_ORDER`. **[UI]** whether either currently resolves on the
registry is unverified — settling it requires a registry fetch this envelope forbids.

Do not write, anywhere, that MetaHarness *ships* or *publishes* a Python bridge in an npm tarball.

---

## 4. Extraction dossiers *(SCOPE output 4)* — the CODE column, unpadded

**[SCE]** Bounded options are `reuse candidate` · `reference only` · `inseparable` · `insufficient
evidence`. None is an adoption recommendation; none is a grade.

| Unit (smallest coherent boundary) | Option | Determining constraint |
|---|---|---|
| `router/src/index.ts` core (k-NN / cost-bar, no runtime imports) | **reuse candidate** | keep the core closure distinct from the optional `tiny-dancer` provider closure |
| `renderer.ts` (`render`, `extractVarReferences`, `validateHarnessName`) | **reuse candidate** | callers must accept a deliberately small non-escaping language, or wrap it with typed encoders and strict unresolved-variable rejection |
| `sha256` / `fingerprintFiles` / `diffFingerprints` | **reuse candidate** | content-diff primitives only — no path metadata, modes, symlinks, or overlays; not a provenance envelope |
| `sandboxAvailable()` **alone** | **reuse candidate at probe-function altitude** | the wrapper must be inverted to fail closed; see §5 |
| `packages/projects/src/sandbox.ts` **as a module** | **reference only** | adopting the file adopts a fail-open default with no degraded-mode signal; inverting it rewrites the module's only decision |
| `walker.ts`, `writer.ts`, session-log copy-in, browser `zip.ts`, `eject.ts`, host emitters | **reference only** | ambiguous custody / conditional atomicity / copied protocol / external schemas |
| Kernel JS floor at **published-package** altitude | **inseparable** | importing the package imports RuVector, optional natives, generated WASM and a three-tier resolver |
| `@ruvnet/agent-harness-generator` alias | **inseparable** | a thin re-export of an *older* full CLI (`metaharness@0.1.5` vs workspace 0.4.7) |
| ARC bridge (`python-bridge.ts` + `python/bridge.py`) as **code** | **inseparable** | a second language runtime, two unlocked PyPI pins with **unresolved licences**, an external endpoint, and a live credential — four closure classes no other row carries |
| ARC bridge **framing layer** as a protocol | **reference only** | domain-neutral and cheap to re-derive; the payload/endpoint/credential are not separable |
| Generated MCP gate; host packages as runtime/enforcement units | **insufficient evidence** | no transport, no independent authority boundary, no compatibility result |

**[SCE] Licence and provenance are dependencies, and they bite.** Root and most packages are MIT
(`horizon`, `oo-agents` Apache-2.0); `ruflo-agntcy` is Apache-2.0. But: three root-lock entries carry no
licence field; RuVector packages, the copied OASF taxonomy, the Kimi upstream patches and the
ruflo-derived contracts have no closure; there is **no `Cargo.lock`** and no lock for Kimi, the 37
examples, or the Python surface — four independent unlocked closures; and `packages/projects` names a
`LICENSE` in its `files` that **does not exist** in the package directory. **[SCE]** the ARC bridge's
determining constraint is licence closure *alone* — it fails before quality is even discussed.

**[SCE] Upgrade mechanics are not closed.** `harness upgrade` re-renders only the bundled base template,
not the host/feature/post-generation overlays the original scaffold applied; `applyPlan()` neither deletes
`removed` files nor rewrites the manifest nor creates parent directories; there is no stored old content,
so no genuine three-way merge is possible; the sibling manifest hash is written but never read.
**[SCE]** fourteen independent drift domains with **no common invalidation event**, including a new one:
host isolation capability vs a probe cached once at import.

---

## 5. Security and authority boundary *(SCOPE output 5)*

**[SCE]** MetaHarness contains honest deterministic *mechanisms* that the same authority may omit, widen,
or walk past. It does not present one closed authority boundary.

| Asserted gate | Default | Determining defect |
|---|---|---|
| `PolicyGate` | **kernel omits it by default and allows** | in-process; caller owns rules, ceiling, action mapping and execution path |
| Claims dispatch | empty claims deny | signatures deferred; `dispatch_unauthenticated()` exported; host may invoke directly |
| Host permission projections | Claude copy-through · OpenCode `ask` · GHA `contents: read` | generated into project-owned files the governed party can edit |
| CASA compile → ruflo enforce | deny-precedence algebra | clean split at source level; **no established production sole-path call** to the checker; schema/path drift across repositories; `budget_usd` carried, not enforced |
| Witness | missing witness **accepted** | self-embedded public key; degraded verification returns `valid:true, unverified:true`; `--allow-unverified-witness` override |
| ARC bridge egress/credential | mode `online` | real hygiene (17-key env allowlist, `PYTHONPATH` dropped, `shell:false`, secret redaction, stderr never surfaced, both sides validate the origin) — but every input is supplied by the governed embedding process, which also holds the credential, and `options.env` is spread **after** the allowlist with no filter |
| `packages/projects/src/sandbox.ts` | **FAIL-OPEN** | see below |

### 5.1 The fail-open sandbox — stated at full strength, and no further

**[SCE]** `packages/projects/src/sandbox.ts` is 131 dependency-free lines wrapping `unshare -rn` (a new
user + network namespace with no interfaces), written — per its own header — because "the
discovery/verifier pipeline runs GENERATED and THIRD-PARTY code (proofs, candidate exploits, untrusted
snippets)" that "must never reach the network."

**[SCE] The probe is the best idea in the repository.** `sandboxAvailable()` runs `unshare -rn true`:
it performs the *exact protected operation under the exact flags the wrapper will use*, rather than
checking that a binary exists on `PATH`. **[SC]** the module names the failure mode this defeats, and it
is the right one — in containerized CI the binary is present and `--version` succeeds while unprivileged
user namespaces are restricted, so `-rn` fails with `EPERM` only at the moment isolation was supposed to
apply.

**[SCE] The default spends that answer.** On a false probe, `buildSandboxArgv()` returns
`{ cmd: bin, argv: args }` — the bare command. Three properties compound:

1. **No signal.** `SandboxResult` is `{ stdout, ok, error? }`. Nothing in the value, and nothing in any
   log, distinguishes a run inside a namespace from a run outside one.
2. **Cached once.** `const CACHED_AVAILABLE = sandboxAvailable()` is evaluated at module import. One probe
   at process start decides the posture of every later execution.
3. **Not on the path.** `runSandboxed()` has **no in-repo caller** — only its own tests and the blanket
   `export *`. The operations it exists to protect run at **ten** sites in the same package via
   `execFileSync('python3', ['-I','-B', …])`: `bin/darwin-discover.mjs` L130 plus nine `bench/*.bench.mjs`.

**[SCE] The bypass is contractual, not incidental.** `verifiers.ts` executes nothing at all (no
`child_process` import; its own header L13–14 says so) and instead **specifies** the vector once in the
shared registry — `PYTHON = { bin:'python3', args:(file,argsJson)=>['-I','-B',file,argsJson] }` (L102–105)
— which every consumer inherits. **[SCE] And it is *partial*, which is the precise part:** all ten sites
replicate the env-hygiene half (`-I`, `env:{PATH, PYTHONDONTWRITEBYTECODE}`, 5 s timeout, so no credential
reaches the child) and omit only the namespace half — leaving **network egress for untrusted generated
code** as the unmitigated exposure, exactly and only the threat the header names. **[UI]** the word
"isolated" is doing load-bearing work in two documentation headers that the code does not do at those call
sites; `-I` is Python *interpreter* isolation and confers no process, network or filesystem isolation.

**[SCE] The rail that names this failure cannot detect it.** `safety-rails.ts` ships a `no-bypass-sandbox`
rail that rejects a mutation when `c.bypassesSandbox` is true. **`bypassesSandbox` is a field of
`CandidateChange` (L33) — a boolean the *proposer* supplies**, i.e. authored by the very party the rail
governs. **[UI]** a guard whose only input is self-declared by the governed party is defeated by declaring
`false`: it is a label, not a control. This is structurally identical to the defect behind this
repository's own corrected `agent_id` rule — persisted self-assertion is reliable for *reconstructing what
happened* and useless for *establishing who is accountable*, and one must never build an authority check
on a field the guarded party writes.

**[UI] The lesson, at full strength and not softened into a caveat:** for a substrate that runs untrusted
generated code, a **fail-open isolation gate is net negative — worse than no gate**. No gate is honestly
frightening and forces a real containment decision. This one appears in the tree, in the exports, in the
safety-rail vocabulary, and in a test file carrying a network-exfiltration assertion — while that
assertion `skipIf`s out on precisely the hosts where isolation silently does not apply, and the production
path never calls it at all. Reviewers reasonably read that surface as containment. **A correct concept
with an unsafe default reads as protection while providing none.**

**And no further than that.** **[SCE]** `unshare` was never run, `sandboxAvailable()` was never evaluated,
no verifier or bench was executed, no exfiltration was attempted. **The fail-open branch is read from
source, never witnessed.** Static structure establishes that the branch exists and appears reachable — not
that it executes, not that the probe ever returns false on any real host, not that an operator ever
reaches the bypassing path. This is a **static reading of source**, not a vulnerability claim. **[SCE]**
`runSandboxed()`'s absent caller is static-grep evidence that *bounds* the dead-code claim, since an
out-of-repo consumer could import it — it does not repair the default or the in-repo bypass.

**[SCE]** W6 withdrew its own earlier closure claim: it now asserts only that its gate enumeration is
closed *against an operation-driven sweep at this cutoff*. The defect it names in its own first pass is
worth carrying: it had searched the **vocabulary of the gates already known** rather than the **vocabulary
of protected operations** — a gate named nothing like the gates you have found is invisible to a
name-driven sweep.

---

## 6. Maturity, credibility, and the wfh-005 / wfh-007 delta *(SCOPE output 6)*

**[SCE]** Active, broad, pre-1.0 portfolio: 929 commits in 74 days, 10 CI/release workflows, Renovate,
pinned Actions, CodeQL, SBOM, audits, extensive test source. **[SCE]** concentration is extreme —
872/929 commits (93.9%) from one email identity. **[SC/public metadata]** 67 issues, 160 PRs (134 merged),
external reporters finding real packaging/runner/scoring defects: credible falsification pressure, not
demonstrated operational success. **[SCE]** hygiene controls disclose their own soft edges: `cargo-deny`
and native builds are `continue-on-error`, native publication is TODO, most `dist/**` is untracked.

**[SCE] Two scorecard rows moved down this run** — dependency hygiene and security/release hygiene, each
**mixed → mixed/weak**. Stated plainly: an unlocked third ecosystem outside all dependency tooling, plus a
**second** subsystem failing open at consequence altitude, are not compatible with the previous reading.
Neither moves to `weak`: the controls that exist are real.

**Delta highlights** (full tables in W7; every material baseline claim has a status row, no silent
carry-forward):

| Baseline | Status | Reconciliation |
|---|---|---|
| wfh-005: "MetaHarness depends on ruflo to operate" | **contradicted** | no declared edge in any ecosystem; ties are ancestry/compatibility; RuVector is the executable coupling |
| wfh-005: `PolicyGate` is an 87-line in-process default-deny gate | **confirmed** | algebra remains; kernel makes it optional and allows when absent |
| wfh-005: witness is home-grown Ed25519, not in-toto/TestifySec | **confirmed** | name collision still load-bearing |
| wfh-005 P8: a present, configured control may be inert | **confirmed** | unusually clean new instance — an exported, tested, vocabulary-named isolation module with no caller |
| wfh-007: assemble shipped sandboxes; a kernel/isolation plane does not earn a bespoke build | **confirmed** | MetaHarness's own isolation is 131 lines wrapping a shipped OS primitive — and even that ships with an unsafe default |
| wfh-007: degraded/missing evidence must fail closed at consequence altitude | **contradicted by implementation, second independent instance** | previously the witness path; now also the execution boundary |
| wfh-007: gate-input independence is read-set/credential separation, not actor naming | **confirmed, sharpened** | new shape: a rail deciding on a proposer-supplied boolean |
| PyPI ecosystem · `python3` prerequisite · cross-language component · endpoint+credential path · fail-open OS gate | **new (×5)** | neither baseline nor wfh-008 round 1 recorded any of them; verified `new` by grep against the prior committed findings and both baselines |

**[PDE]** wfh-007 demonstrated contract/checker properties **only inside its own artifact envelopes**. It
demonstrated nothing about MetaHarness. Its portable inputs here are gate-input independence and
dependency-event invalidation — not code and not proof transfer.

---

## 7. Directional position for the `jurati-arch-002` proposer *(SCOPE output 7)*

**This is advice. It is not adoption, dependency selection, implementation, or ratification of
`jurati-arch-002`, and it does not design Jurati.** Recorded in Unimatrix as `#319` (`finding`, tagged
`position`).

**TAKE — the concepts, in priority order.**

1. **[SCE→UI] Probe the real operation, not the binary's presence.** A capability gate establishes its
   capability by *performing* the exact protected operation under the exact flags it will later use — not
   by finding an executable or reading a `--version` string. Generalize to every capability Jurati
   asserts: sandbox, signer, egress block, filesystem restriction, credential separation. **The probe is a
   rehearsal, not an inventory; an inventory-shaped check is a false-positive machine.** Take the layering
   too — a pure argv-computing function with an injectable capability flag is unit-testable without
   spawning.
2. **[UI] Its counter-lesson, at equal strength: a correct concept with an unsafe default is worse than no
   gate.** A probe answering "cannot isolate" must make the protected operation **incapable**, not
   unprotected; the degraded mode must be visible in the result (`isolated: boolean`); the answer must be
   re-evaluated or a cached negative treated as a startup failure; and the security property is the
   **enumeration of execution sites**, not the wrapper.
3. **[SCE→UI] A gate's input must be observed, never declared by the governed party.** Preserve the rail
   *vocabulary* — a small set of named, independently evaluable refusals screening a proposed mutation
   before it is benchmarked. Reject the input path. Derive each rail's input from something the proposer
   cannot author: the diff itself, static analysis of it, or the observed exec/syscall surface of the run.
4. **[SCE→UI] Fail-closed serial subprocess protocol with an *enumerated* inherited-env allowlist** — one
   in-flight request, id-matched JSON-lines envelopes, bounded line sizes, a terminal `failed` state on
   *every* protocol violation, stdout reserved as protocol-only, stderr drained but never surfaced into
   error text, secret redaction, startup refusal on dependency-version mismatch. Do not repeat its own
   undoing: caller-supplied `env` must not be merged *after* the allowlist.
5. **[UI] Generation envelopes must declare cross-language prerequisites** — interpreter identity and
   version floor, foreign-ecosystem pins, required network origins, required credentials — as first-class
   fields, so "install succeeded" and "prerequisites satisfied" are distinguishable and an
   ecosystem-agnostic audit can enumerate them.
6. **[UI]** Plus the durable set: stable definition → shared IR → host projections with an explicit loss
   report; immutable generation envelope closed only after *all* producers finish; explicit late-binding
   policy naming fail-open/fail-closed; one-way eject with a loss/provenance ledger; pre-operation
   decision separated from post-operation receipt; deny precedence and monotone delegation; degraded-mode
   truthfulness; definitions separated from events/evidence; **external custody as the admission condition
   for enforcement**.

**DO NOT TAKE.** [SCE] Any MetaHarness gate as an authority boundary. The ARC bridge as code. The
module-altitude sandbox. The published generator-library alias. Branded ecosystem contracts, registry
defaults, `RUFLO_*` state/env namespaces, or same-authority placement.

**CANDIDATE SEAMS MERITING A LATER VALIDATED SCOPE** [UI]: the router core; `sandboxAvailable()` with an
inverted wrapper; the renderer and fingerprint/diff primitives. One seam and one concept — not the
monorepo.

### 7.1 The gap register — travelling *with* this recommendation, not behind it

These ten items are the honest residual behind the coverage PASS. Read them as part of the recommendation
above, not as an appendix to it.

1. **PyPI closure open on every axis** — transitive deps, platform wheels and licences for
   `arc-agi==0.9.8`, `arcengine==0.9.3`, `terminal-bench>=0.2.18`. No lockfile exists; resolving requires
   a registry fetch outside this envelope. **This is the determining constraint that rules the ARC bridge
   not importable.**
2. **Undeclared Python imports** `pydantic`, `lcb_runner`, `pandas`; fourth distribution
   `terminal-bench-core==0.1.1` declared by no manifest.
3. **`retort` / `retort_metaharness`** — host-local, non-distributed, unresolvable by construction (§10).
   Captured as a follow-on candidate, not absorbed.
4. **`submissions/**` (G17)** — 1,071 checked-in files with no writer in any tracked script.
   Owner-published evidence, **not** demonstrated-by-us, and not re-derivable here.
5. **G16 Terminal-Bench outputs** — likewise not re-derivable: transient outputs are `.gitignore`d and the
   dataset is fetched out-of-repo.
6. **Whether any published consumer of `@metaharness/projects` calls `runSandboxed()`** — unanswerable
   from this repository.
7. **The fail-open branch, the ARC credential path, and every execution site are read from source, never
   witnessed.** Nothing in this run is demonstrated-by-us evidence.
8. **Class-level dryness holds against a static instrument at one commit** — dynamic-import,
   generated-harness and out-of-repo-consumer surfaces remain structurally out of reach (§8).
9. **No lockfile exists for Cargo, `kimi-k3-harness`, the 37 example packages, or the Python surface** —
   four independent unlocked closures.
10. **The round-2 audit performed no Unimatrix writes** and attests nothing about the live contents of the
    graph nodes; the curator's record is §11.

---

## 8. The boundary of this run's coverage PASS — stated, not footnoted

**[SCE]** Coverage was ruled sufficient on the basis of the auditor's **own third independent sweep**, run
over an ecosystem-agnostic filename alphabet and an operation-driven spawn/exec/interpreter pass — not on
the researchers' self-report, because the researchers' own pass-2 sweep came back *not dry* and a
self-reported sweep was the instrument that had already failed twice.

**That PASS holds against a static instrument at a single commit.** [SCE] Dryness is a property of what
the instrument can see. A component, dependency class, ecosystem tie, generator chain, authority path or
prior-art delta reachable **only** through a dynamic import, a generated harness, or an out-of-repo
consumer **would still be missed**. Three residues sit exactly on that line: the
`ARC_CONTROLLER_FACTORY_MODULE` / `ARC_MCP_OAUTH_MODULE` environment-selected specifiers, the `@latest`
late binding in example wrappers, and whether any published consumer calls `runSandboxed()`.

**[SCE]** W6 asserted this limit **about itself, unprompted** — withdrawing its own closure claim and
replacing it with the weaker, honest one. The auditor recorded that as the reason it believed the rest of
that ledger. That is worth carrying as a method observation: a ledger that names its own blind spot is
more trustworthy than one that reports closure.

---

## 9. Staged validated follow-on scope *(what a directional run owes)*

**Nothing below is authorized here.** A validated/empirical scope needs separate approval; this section
scopes it so the decision is cheap. **[UI]** throughout.

| Stage | What must be built | What must be independently validated (by us) | Clears |
|---|---|---|---|
| **S0 — pin and close** | pinned checkout + pinned published artifacts; registry fetch for the three PyPI distributions and the RuVector packages | licence texts and transitive/platform closure resolved or explicitly refused; published tarball compared byte-for-byte to source | gap-register items 1, 2, 9; the ARC bridge's determining constraint |
| **S1 — isolated extraction** | one named seam at its smallest boundary in a clean project (candidate: router core; or `sandboxAvailable()` with the wrapper inverted to fail closed) | it builds and imports with no MetaHarness dependency; the closure is exactly what the dossier claimed | moves *that seam* — and only that seam — toward `partial` |
| **S2 — focused behaviour tests** | a rig that exercises the **failed-probe path on a host where `unshare -rn` genuinely fails**; a rig that enumerates every execution site of the protected operation | what actually executes when the probe fails, observed rather than read; whether an inverted fail-closed variant is reachable from the ten direct sites without restructuring the bench harness | gap-register items 6, 7; the only route from "read from source" to witnessed |
| **S3 — upgrade / drift replay** | `harness upgrade` run with host/feature overlays; a frozen-input replay of `@latest`, CLI-vs-browser projections, and JS/WASM/native equivalence | removals applied, manifest refreshed, idempotence on repeat, projections structurally equal or a named loss report | the upgrade and drift dossiers |
| **S4 — authority admission test** | a clean-room envelope/checker with the enforcer's credential, clock and config under a **separate OS/service identity** | seed a forbidden action, policy omission, translator widening, expired envelope, wildcard claim, missing witness — and require an **externally recorded refusal** | the only test that could move an authority claim; MetaHarness itself does not pass it by structure |

**[SCE]** The proof bar is unchanged and binding: any later claim that a seam is reusable, secure,
compatible or operational requires an artifact **at that claim's altitude**, created and independently
validated **by us**. The owner's tests, CI runs, benchmark bundles and submissions are not demonstration
by us.

---

## 10. Follow-on candidate — `retort` *(not absorbed)*

**[SCE]** `docs/research/retort-placement/analyze{2,3,4}.py` import `retort` and `retort_metaharness` by
inserting an **absolute path into a transient agent-session scratchpad on the author's machine**
(`/tmp/claude-1000/-home-ruvultra-projects-agent-harness-generator/…/scratchpad/`), sibling to a `grid2`
results directory.

**[SCE]** These modules are therefore **host-local, non-reproducible research residue — unresolvable by
construction, not by omission**. They were never distributed, never vendored, and the path cannot be
reconstructed by any consumer. **[UI]** the `ruvultra` path segment is *circumstantially* owner-adjacent;
that is **not** evidence that `retort` is a `ruvnet` project. **The round-2 auditor declined to infer it,
and this report declines likewise.**

**Handling:** SCOPE legislates this case directly — "a newly discovered technology outside the
single-target boundary is captured as a **follow-on candidate**, not absorbed into this scope." It is
recorded here and in `#319` as a candidate for the coordinator. Predicate 3 is unaffected: it is lexically
scoped to `ruvnet`/`ruflo`/`claude-flow`, and `retort` is none of those.

**Consequence, and it belongs wherever G16/G17 are cited:** `docs/research/retort-placement/**` is
non-reproducible research residue, not runnable first-party code — its committed JSON outputs **cannot be
re-derived from this repository**, the same property already recorded for G16's Terminal-Bench outputs and
G17's `submissions/**` bundles. Three artefact families in this repository share it.

---

## 11. Unimatrix record for this phase

Written by `factory-curator`; every call carried `agent_id: "factory-curator"`.

| Before | After | Kind | Grade | Action |
|---|---|---|---|---|
| `#312` | **`#316`** | `technology` | **`grade:claimed` (unmoved)** | `context_correct` — added the third package ecosystem, the `python3` prerequisite, the corrected packing-vs-published framing, the fail-open execution boundary, and the probe concept + counter-lesson. 3 incoming edges redirected. |
| `#313` | **`#317`** | `finding` | — | `context_correct` — three ecosystems, not two; per-*component* closure rule; the enumeration-alphabet method note. `Motivates` → `#200`, `#316`. |
| `#315` | **`#318`** | `finding` | — | `context_correct` — added the ARC egress/credential gate and the fail-open sandbox with the proposer-declared rail; records W6's withdrawal of its own closure claim. `Motivates` → `#277`, `#316`. |
| — | **`#319`** | `finding`, tagged `position` | — | `context_store` — the directional position of §7. `Motivates` → `#316`. |
| `#314` | unchanged | `finding` | — | deliberately not corrected; its reuse-split claims survive the new evidence intact. Its edge resolves forward to `#316`. |

**Deliberately not moved:** no grade change anywhere; no `partial`, no `proven`; no capability advanced;
no `Prerequisite` edge (proposed `jurati-arch-002` has no capability id, so there is no legitimate target
and one was not invented); no `Cites` or `Tests` edges (sources are a `cites:` field, proof is a
`proven_by:` field).

---

## 12. Limits

**[SCE]** Every claim in this report is directional static evidence at one commit, or an explicitly
labelled inference from it. Presence of source, tests, CI, workflows, loaders, generated files,
submissions, or owner demonstrations is **not** demonstration by us. No technology or capability is
`partial` or `proven` as a result of this run, and `done_when` clears for nothing here.
