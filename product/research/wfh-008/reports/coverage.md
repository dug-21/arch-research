# wfh-008 tech-discovery coverage audit

**Role:** `factory-researcher` coverage auditor  
**Cutoff:** MetaHarness `6f8c60216f47eac391a076fe27fd804470a07e10`; ruflo `d33ef4bf8ab27a8f9ef08352c9c293b53312a861`; inspected 2026-08-28  
**Method:** independent static inspection only; no repository code, build, test, install, generator, service, or model was run  
**Recommendation:** **REWORKABLE**

## Decision

Do **not** confirm the blocking tech-discovery coverage gate yet. The seven findings substantially answer the scope, preserve the evidence firewall, and satisfy the owner amendment, but the completed-ledger claim is not internally consistent and one manifest-owned surface is absent from the W1/W2 cross-reference:

1. `crates/kernel-napi/package.json` is a real package/build manifest discovered by the independent manifest sweep. It is not assigned a W1 inventory ID and is not explicitly accounted as an npm packaging/build surface in W2. Its Rust crate is covered as R03, but the npm manifest is a separate declared artifact boundary required by predicates 1 and 2.
2. W1 reports **40** `examples-packages/*` manifests and **43** other package manifests. The checkout contains **38** example manifests. The correct other-manifest total is **42** when `crates/kernel-napi/package.json` is included (38 examples + web UI + service + Kimi + kernel-napi packaging). W4 repeats the incorrect 40-example count.
3. W2 reports **40** root workspace package manifests, while the literal `packages/*` workspace contains **42**. W1's 42-row inventory is correct. W2's edge table appears to name the full set, so this is probably a count/ledger defect rather than two missing dependency analyses, but “100%” cannot be certified until the ledger is corrected and the two affected packages are explicitly reconciled with the root lock.

These are bounded documentation/ledger defects. No evidence presently requires widening the single-target scope, so the outcome is **REWORKABLE**, not SCOPE-FAIL.

## Numbered coverage predicates

| # | Predicate | Audit result | Completed-ledger evidence / required repair |
|---:|---|---|---|
| 1 | 100% component accounting | **REWORKABLE** | W1 correctly inventories 42 npm workspace packages, 5 root Cargo members, major non-workspace applications, plugin/config projections, scripts, examples, experiments, submissions, and top-level families. Repair: add an owned row or explicit build-surface subrow for `crates/kernel-napi/package.json`; correct examples/non-workspace counts; cross-reference the npm packaging surface to W2. |
| 2 | 100% declared-edge accounting | **REWORKABLE** | W2 records three npm lock roots, unlocked Cargo surfaces, first-party edges, native/WASM relations, dynamic imports, undeclared/hoisted imports, external executables, and unresolved closures. Repair: correct 40→42 workspace count, explicitly reconcile all 42 package manifests to lock workspace links, and account for the kernel-napi npm manifest/build metadata. Missing Cargo/Kimi locks and open dynamic specifiers are honest unknowns, not omissions, once retained as unresolved. |
| 3 | 100% ecosystem-reference accounting | **PASS** | W3 performs both lexical and semantic sweeps, gives term/file counts, and classifies identity/contract families across manifests, locks, source, generated/config and docs. It distinguishes executable RuVector edges from ruflo ancestry, copied contracts, aliases, optional integration and claim-only naming. Repeated attribution strings are deliberately collapsed into owned residue families, not silently omitted. |
| 4 | Complete generation and authority chains | **PASS** | W4's G1–G14 ledger traces producer→artifact→consumer, including browser/CLI divergence, post-generation WASM, catalog/taxonomy, examples and distribution builds. W6 names decision point, protected operation, authority owner, defaults, mutation/bypass surfaces and evidence altitude for each gate. Orphans/dormant paths and missing sole-path call sites remain explicit. Correct W4's example count, but no generation class is presently unowned. |
| 5 | Delta closure | **PASS** | W7 provides a material wfh-005 MetaHarness/ruflo claim table and a separate wfh-007 concept table with `confirmed`, `changed`, `contradicted`, `still unverified`, partial, and not-applicable outcomes. It also applies the corrected persisted-but-self-asserted attribution rule rather than silently carrying forward the superseded wfh-007 wording. |
| 6 | Loop until dry | **REWORKABLE** | The researchers report two sweeps, and this auditor independently repeated both. Sweep 1 was not dry: it found `crates/kernel-napi/package.json` and exposed the count conflicts. Sweep 2 found no additional unowned semantic class after reconciliation with W3/W4/W6. Repeat both sweeps after the three ledger repairs and record a dry result. |

## Independent residue sweeps

### Sweep 1 — manifests, locks, and build metadata

The checkout contains 42 `packages/*/package.json` files, 38 `examples-packages/**/package.json` files, package manifests for the root, web UI, deprecated service, Kimi harness, and `crates/kernel-napi`, ten Cargo manifests including the root, and exactly three npm lockfiles. Build/config surfaces inspected include npm/Cargo scripts, TypeScript/Vite/Vitest/Playwright/Tailwind/PostCSS configuration, Docker/Compose/Terraform, Rust toolchain/deny, Renovate, plugin manifests, and GitHub workflows.

New residue: the unowned kernel-napi npm packaging manifest and the three count inconsistencies above. No fourth lock root or additional Cargo manifest was found. Absent Cargo/Kimi/example locks remain explicitly unresolved rather than inferred closed.

### Sweep 2 — source, configuration, documentation, and runtime references

The independent sweep covered ecosystem identities; import/dynamic-import and executable references; generated/build/catalog/template/taxonomy surfaces; filesystem/process/network/environment prerequisites; and policy, permission, approval, claim, dispatch, witness, credential and authorization call sites. It reconciles to W2's dynamic-edge rows, W3's ecosystem families, W4's G1–G14 chains, and W6's gate/bypass matrix.

No new unowned component class, ecosystem tie, generator/consumer class, authority gate class, or prior-art delta emerged. The remaining open specifiers, missing locks, copied-source revisions, published-artifact parity, native/WASM availability, runtime call-site liveness, trust-root custody, and deployed host precedence are honest unknowns at directional/static altitude.

## Owner amendment audit

**PASS across W1–W7.** Every workstream explicitly separates direct **CODE** reuse from portable **CONCEPTS** or clean-room patterns. The distinction is substantive, not merely labeled:

- CODE rows identify a smallest file/package boundary, dependency/license closure, and a limiting condition; none is called proven or generally adoptable.
- CONCEPT rows preserve invariants such as shared IR/projection loss, generation envelopes, explicit late binding, pre-operation decisions and post-operation receipts, deny precedence, monotone attenuation, degraded-mode truthfulness, and producer→artifact→consumer ledgers without transferring MetaHarness's same-authority placement or branded ecosystem contracts.
- W5 provides the controlling extraction dossiers and bounded dispositions; W7 synthesizes the split as low-to-moderate seam-specific code suitability versus moderate-to-high conceptual value.

## Curator outcome consistency

The stated curator result is method-consistent: claimed MetaHarness technology **#312** and findings **#313–#315**, reuse of **#200** and **#277**, no grade/capability advancement, and no `Prerequisite` edge because proposed `jurati-arch-002` has no capability ID. That preserves the directional firewall and avoids inventing an edge target. This audit did not write Unimatrix and does not independently attest the live contents of those IDs; the leader/curator should verify their current records before phase-end.

## Exact human decision requested

Request **REWORK**, limited to one correction pass:

1. amend W1/W2 to own and cross-reference `crates/kernel-napi/package.json`;
2. correct W1/W4 examples counts to 38 and W1's derived non-workspace manifest count;
3. correct W2's workspace count to 42 and explicitly reconcile all 42 workspace manifests against the root lock;
4. rerun and record both residue sweeps as dry.

After those repairs, ask the human to **confirm tech-discovery coverage sufficient and authorize transition to synthesis**. If the repeat sweep surfaces another unowned class, use the protocol's second and final rework allowance; only a boundary-expanding discovery or exhaustion of that allowance should become SCOPE-FAIL.
