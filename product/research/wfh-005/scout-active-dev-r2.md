# scout-active-dev-r2.md — wfh-005 round two, active-development surface

**Run:** `wfh-005` · Issue #54 · **CHALLENGE mode** · surface **W3 active development, round two** · `agent_id: wfh-005-scout-active-dev-r2` · read-only, zero graph writes.
**Extends, does not replace,** `scout-active-dev.md` (round one). Every round-one verdict is reconciled explicitly below.
**Trigger:** owner-injected. The owner asked whether the `ruvnet` projects had been looked at. They had not.
**Discipline:** star counts are reported only where checked against peer ratios; nowhere offered as evidence of maturity. Every claim is traced to a file read in a cloned checkout, an API response, or a named document — and where only vendor prose was available, it says so.
**Honest bound:** exhaustion is relative to the ruvnet ecosystem (~100 repos), the Outshift/AGNTCY ecosystem it led to, and the five named positions. Not absolute.

---

## 0. Headline

The ruvnet ecosystem is real, is enormous by distribution, and is **not** where the theme's object is being solved. What it did was act as a **pointer**: two days ago `ruflo` and `metaharness` shipped a paired ADR (`ADR-380` / `ADR-240`) integrating **CASA — Continuous Agent Semantic Authorization**, and CASA turns out to be **a Cisco Outshift open-source project under the Linux Foundation's AGNTCY program** (`outshift-open/outshift-casa`, Apache-2.0, **17 stars**, 7 Cisco engineers, alpha since 2026-04-17, pushed today), described as *"Intent-scoped authorization for Kubernetes multi-agent systems, **enforced at the network layer**."* Envoy sidecar auto-injected per pod, eBPF deny-by-default egress, a `MultiAgentSystem` CRD, tokens injected on egress and validated on ingress "without any changes to the application." **That is the BUILD's enforcement-plane leg — a plane the principal holds no credential for — shipping, from Cisco, at 17 stars.** The sibling repos `outshift-open/ASTRA` ("Authorization with Semantic **Task-based** Restricted Access") and `outshift-open/tbac-research-datasets` (**TBAC = Task-Based Access Control**, the Thomas & Sandhu mid-1990s model) show this is a sustained research programme, not a launch. Round one missed it because it searched by mechanism vocabulary over popular repos, and this entire line is filed under a different name at two-digit star counts.

**The BUILD does not collapse — but it loses two of its four legs**, and the remaining two are now the whole of it.

---

## 1. What actually works today versus what is claimed

### 1a. `ruvnet/ruflo` — 66,763★ — **it is `claude-flow`, renamed**

`gh api repos/ruvnet/claude-flow` **redirects to `ruvnet/ruflo`**, created 2025-06-02. The npm package is still **`@claude-flow/cli`** (`ruflo` is a thin wrapper); the source tree is literally `v3/@claude-flow/*`. So the 66k stars were accumulated over ~14 months as **claude-flow, a Claude Code swarm orchestrator** — not as "the original agent meta-harness," which is a repositioning applied to an existing star base. That is the honest answer to *what the stars are for*.

**On whether the stars are inorganic — checked, no anomaly found.** Ratios against peers:

| repo | stars | forks | fork % | watchers | star:watch |
|---|---|---|---|---|---|
| ruvnet/ruflo | 66,763 | 7,961 | 11.9% | 425 | 157:1 |
| microsoft/autogen | 60,155 | 9,061 | 15.1% | 525 | 115:1 |
| crewAIInc/crewAI | 56,469 | 8,029 | 14.2% | 391 | 144:1 |
| browser-use/browser-use | 107,506 | 11,820 | 11.0% | 451 | 238:1 |
| github/gh-aw | 4,849 | 475 | 9.8% | 39 | 124:1 |

ruflo sits inside the normal band on both ratios. **No evidence of star inflation, and none is asserted.**

**Who builds it:** `ruvnet` **6,853 commits**; a `claude` bot **50**; the next-largest human contributor **7**. That is ~97% one person plus an agent. metaharness is the same shape: `ruvnet` 837, `claude` 49, two others with 1 each.

**Release cadence:** 30 tags reachable, but the release feed runs `v3.32.28 → v3.32.41` inside ~48 hours — roughly seven named releases per day, each with a marketing-shaped title. One release is titled *"honest routing scores, honest MoE metrics, real pattern transfer"*, which tells you what the previous ones were. **This is a machine-authored release train, and a release here is not the maturity signal a release normally is.**

**Real issue traffic — and this is where it gets genuinely credible.** 1,550 issues (520 open), 1,223 PRs. Distribution of the last 100 issue authors: `ruvnet` 35, `vidaunited` 20, `sparkling` 10, then a long thin tail of 1s. So roughly a third is self-filed (including automated `[Dream Cycle YYYY-MM-DD]` issues the project files against itself, and `[verification]` issues its own scheduled runner opens). **But the external reports are excellent.** #2887 has two independent outside users tracing a silent-data-loss bug to a specific line in shipped `dist/`, reproducing across machines, one of them volunteering a correction against their own evidence. #2886 has an outside contributor filing a PR and then publicly downgrading their own impact estimate from +3 to +1. **That is real users doing real forensics on a real product.** The stars are not hollow; the maintainership is one person.

**What is in code vs. README (verified by reading a `--depth 1` clone):**

| Claim | Status | Evidence |
|---|---|---|
| Deterministic policy chokepoint on **every** MCP tool call | **In code, working** | `v3/@claude-flow/cli/src/mcp-client.ts:257` — `const decision = await authorizeMcpTool(...)`; throws `policy-${outcome}:${reason}; receipt=${id}` before `tool.handler` runs. ADR-324. Policy-admin tools explicitly not exempt. |
| …but it is **inert by default** | **In code** | `policy/evaluator.ts:124` — `enforcedOutcome: mode === 'enforce' ? outcome : 'allowed'`. Engine default is `mode: options.mode ?? 'legacy'`; `legacy` also yields `reason: 'legacy-default-allow'`. **The gate evaluates and records on every call, and blocks nothing unless an operator sets `enforce`.** |
| Monotone capability envelopes | **In code, tested** | `security/src/policy/envelope.ts` — `isEnvelopeReduction()` requires subset on 7 list fields, `≤` on 5 numeric bounds, forbids turning `network`/`destructive` on if the parent had them off. `delegateEnvelope()` decrements `delegationDepth` and **throws `capability-envelope-cannot-grow`**. |
| Monotone delegation across agent hops | **Library only — no call sites** | `security/src/authorization/propagator.ts`, its own header: *"P1 (this file): the component, the envelope, the type-level invariants. **No call sites yet** — adding the wrapping/enforcement in P2-P4."* Grep confirms `wrapOutbound`/`checkToolCall` appear only in `__tests__`. Default is *"legacy permissive mode (all tools allowed, depth unlimited, server auth unchecked)"*. |
| Approval machinery | **In code** | `policy/engine.ts` — `issueApproval()` enforces `self-approval-forbidden`, `untrusted-approval-issuer`, unique id, `expiresAt > issuedAt`, integer `maxUses`, plus `revokeApproval()`. |
| Policy state anchored outside the workspace | **In code** | `services/policy-runtime.ts` — HMAC-SHA256 anchor keyed by a 32-byte random key at `~/.config/ruflo/policy-trust/<sha256(realpath(root))>/anchor.key` (0600), verified with `timingSafeEqual`, throws `policy-state-authentication-failed`. |
| Worker cannot escape to permissive local state | **In code, a genuinely good defence** | `authorizeMcpTool()` — if `CLAUDE_FLOW_CAPABILITY_ENVELOPE` is set, projectRoot is re-derived from `git rev-parse --git-common-dir` so a worker in a linked worktree resolves to the coordinator's policy state. |
| "Capability Brain" classifies 353 MCP tools with authority/risk boundaries | **In code, explicitly advisory** | `mcp-tools/capability-brain.ts` header: *"This module is **deliberately data-only**… prevents documentation from being mistaken for runtime availability."* 858 lines of metadata. |
| `policy_evaluate` MCP tool | **Reported broken today** | Issue **#2894**, opened 2026-08-01, open: *"MCP: `policy_evaluate` crashes (-32603); validation errors returned in-band with `isError` never set."* |
| Witness-signed releases | **Signature primitive works; verification pipeline broken, 5 consecutive scheduled runs** | Issue **#2883** — `missing=99, drift=18`, `"precondition": "dist-not-built"` on all three platforms. Ed25519 itself verifies. |
| npx install | **Broken/degraded** | Issue **#2884** — `npx -y @claude-flow/cli@alpha --version` times out at 60s on cold cache, 3 consecutive runs; 69.5s warm. |
| Memory persistence | **Silent data loss, reproduced on 3.34.0** | Issue **#2887** — `agentdb_hierarchical-store` returns `success:true`, persists nothing, recall returns `[]`. |

**Escape hatches:** `scripts/audit-env-var-precedence.mjs` — the project maintains an audited registry of **106 `CLAUDE_FLOW_*`/`RUFLO_*` environment variables**, and ADR-144 explicitly calls the strict-auth variable *"a documented escape hatch (registered in `audit-env-var-precedence.mjs`)."* A project that needs a registry of its own bypasses has 106 of them.

**Honest summary of ruflo:** it contains **more of the theme's object, in real code, than anything round one found** — a blocking dispatch chokepoint, monotone capability envelopes with a named `cannot-grow` invariant, delegation attenuation, approval issuance with self-approval forbidden, receipts, and an out-of-workspace trust anchor. And essentially **all of it is off by default, partly unwired, and maintained by one person against a tracker with open silent-data-loss bugs.** Both halves are true and neither cancels the other.

### 1b. `ruvnet/metaharness` — 534★, 1 watcher, 64 forks, created 2026-06-13

A pnpm monorepo: 35 `packages/`, 5 Rust `crates/`, `apps/web-ui`, `services/`. Scaffolds a branded agent harness with per-host config emitters (`host-claude-code`, `host-codex`, `host-copilot`, `host-github-actions`, `host-hermes`, `host-openclaw`, `host-opencode`, `host-pi-dev`, `host-rvm`). Only **2 GitHub releases** against an npm version of **0.4.2**. ~20 lifetime issues, from a handful of genuine external reporters about CLI ergonomics, dependency pins, and proxy auth. **Zero issues about authority bounds.**

Its `policyLists()` (`create-agent-harness/src/host-config.ts:42`) is the whole of its generated permission model: an allow list of the harness's own MCP namespace, and a **six-entry hand-written deny list** (dotenv reads, `rm`, `git push`, optionally `Write`/`Edit`) emitted into each host's config format. That is scaffolding, not derivation.

Its `packages/harness/src/safety.ts` is an **87-line in-process `PolicyGate`** — default-deny, allow/deny rules whose `match` is a JavaScript closure, max-risk scoring against a ceiling, with a `safeMatch` wrapper so a throwing matcher never silently allows. Competently written; it is a library in the same Node process as the agent loop. **In-process advice, by construction.**

### 1c. The rest of `ruvnet`'s ~100 repos — checked, mostly out of lens

`agentic-flow` (785★, **no licence**, 82 open issues) is the any-LLM-pluggable thesis shipping — OpenRouter/Gemini model switching behind the Claude Agent SDK — but it is **invocation-level plurality only**, exactly the distinction round one's cold-leg C-3 already made; the absent licence is a live adoption blocker. `rvm` (123★, no licence, **not pushed since 2026-05-23**) is a Rust micro-hypervisor with `capability` and `witness` in its topics — in-lens on paper, dormant in fact. `rudevolution` (123★) is a decompiler; its "cryptographic witness chains" are the same home-grown Ed25519 manifest applied to decompilation steps — **out of lens**. `SAFLA`, `sparc`, `flow-nexus`, `daa`, `Synaptic-Mesh`, `QuDAG` — dormant or off-theme. `RuView` (88,041★) is WiFi sensing, out of lens entirely. **Nothing else in the ~100 is in-lens.**

---

## 2. Does either one already do the BUILD?

**The BUILD as triage stated it, decomposed into four legs:**

> *deriving and enforcing an authority bound for a principal* **(A)** *whose demand set is discovered during execution rather than declared before it* **(B)** *— monotonically, such that the bound can narrow without approval and can never widen without one* **(C)** *— and enforced by a plane the principal holds no credential for* **(D)**.

| Leg | ruflo / metaharness | Outshift CASA | Verdict |
|---|---|---|---|
| **A — derive & enforce an authority bound** | **Yes, twice.** `compileObjectiveToEnvelope()` compiles free text → `{objective, allow, deny, budget_usd, expires_at}`; `checkCapabilityEnvelope()` + `AgenticPolicyEngine.evaluate()` enforce a richer envelope (actions/resources/tools/servers/environments/read+write namespaces/maxCostUsd/maxTokens/maxConcurrency/network/destructive/expiresAt) on every MCP dispatch. | **Yes.** `MultiAgentSystem` CRD declares agents, MCP servers, clients, `enabledToolChecks`; scopes enforced per request. | **NOT NOVEL** |
| **B — demand set discovered during execution** | **No.** The compiler runs once, up front, over the objective string; ruflo's envelope arrives declared. The Capability Brain discovers the **supply** surface (353 available tools), never the **demand** set. | **No.** Scope comes from the CRD plus the initial user prompt captured at `promptFieldJsonPath`; mid-session change is not addressed. | **SURVIVES** |
| **C — monotone; narrows freely, widens only on approval** | **Half.** `isEnvelopeReduction` + `capability-envelope-cannot-grow` + `AuthScope` *"monotonically reducing — each hop can drop tools or servers but never add them"* is monotonicity, shipped and unit-tested. But it is **stricter and dumber than the claim**: widening is not approval-gated, it simply throws. Approvals exist as a *separate* mechanism, not composed into a widen-on-approval path. And the delegation propagator **has no call sites**. | **No.** Unaddressed. | **NOT NOVEL as monotonicity; SURVIVES as monotone-with-approval-to-widen** |
| **D — a plane the principal holds no credential for** | **No, and this is the sharp gap.** Everything is same-uid, in-process. The strongest measure is an HMAC anchor key at `~/.config/ruflo/policy-trust/…/anchor.key` (0600) — *outside the workspace*, which stops a worktree-scoped worker, but is readable and writable by **any process running as the user**, which includes the agent's own `Bash` tool. ruvnet says so himself on #2768: *"**durable enforcement across processes** … remain work for this issue. The release supplies **the guidance and policy substrate, not completion**."* | **YES.** Envoy sidecar **auto-injected into every pod** in a CASA-enabled namespace, intercepting inbound and outbound HTTP; **eBPF deny-by-default network policies**; the sidecar *"injects tokens on egress and validates tokens on ingress — without any changes to the application."* The agent is a container that holds nothing. | **FALSIFIED by Outshift CASA** |

**Answer: neither ruflo nor metaharness does the BUILD. Outshift CASA does leg D and leg A; ruflo does leg C's monotonicity. Nobody does leg B, and nobody composes C's approval half.**

**Also relevant, and unflattering to ruvnet's version:** the ruvnet CASA implementation is **two days old, `Status: Proposed`, in `optionalDependencies`, with an estimated 15–25 days of work remaining**, and **has no call sites in the execution path**. `plugins/ruflo-agntcy/skills/agntcy-status/SKILL.md` says it plainly: *"Scaffolding stub — not yet implemented… no such upstream package exists yet publicly."* `npm view @claude-flow/agntcy` → **404**. The Rust crate ships a `SlimTransport` **stub** because *"no `agntcy`/`slim` Rust crate is published on crates.io yet."*

**One thing ruvnet's version has that Outshift's does not,** and it deserves recording because it is the theme's own P3 position written independently by someone else, in a code comment, two days ago:

> *"Translating free-text intent INTO a `CasaEnvelope` MAY use an LLM… **ENFORCING** the envelope — checking a requested action against `allow`/`deny`/`expires_at` — **MUST NEVER call an LLM** or any nondeterministic judgment… Any change to this file that introduces async behavior, an API call, or lets a model's runtime judgment influence the `allowed` result is a security regression, not a feature."* — `plugins/ruflo-agntcy/src/casa/enforce.ts`

**Outshift's own CASA does the opposite** (see P3). ruvnet reimplemented the name with a determinism invariant the original does not carry.

**And ruvnet's compiler has a monotonicity hole worth naming.** `compileObjectiveToEnvelope`'s optional `translator` (the declared future LLM extension point) merges a patch by **unioning into `allow` and then removing those scopes from `deny`**. A translator can therefore move `git.push` out of the deny list with no approval step. The code comment claims the merge rule stops a translator *"silently pulling a dangerous scope out of `deny` without also explicitly adding it to `allow`"* — that is a **consistency** guarantee, not a monotonicity one. **Widening is exactly what it permits.** The compiler itself is a 6-row regex table over a 5-scope vocabulary, self-described as *"a first, honest pass."*

---

## 3. "Witness-signed releases" — the actual mechanism

**It is not in-toto, not `witness` (TestifySec), not sigstore, not cosign, not Rekor, not SLSA, and not GPG.** Grep for all of those across the metaharness tree returns hits only in prose (README, SECURITY.md, CHANGELOG, ADRs) — **zero in code or dependencies**.

**What it actually is:** a home-grown scheme in `crates/kernel/src/witness.rs` (272 lines) — an Ed25519 signature via `ed25519-dalek` over a custom canonicaliser, producing a `witness.json` of `{schema, harness, version, entries[{id,desc,marker,sha256}], public_key, signature}`. Plus a separate hash-chained receipt log where each receipt's `thisHash` chains over `prevHash`.

**The load-bearing weakness: there is no trust root.** `verify_manifest()` decodes `public_key` **from the manifest itself** and verifies the signature against it. That proves the entries are internally consistent with the signature; it proves **nothing about who signed it**. Anyone can re-sign a tampered manifest with their own key and it verifies. Trust is instead a **registry attribute** — `registry.ts` carries `trustLevel: 'official' | 'community' | 'unverified'` assigned at registration, defaulting to `'community'`. They demonstrably know how to do better: `meta-proxy.ts` **pins** a release Ed25519 key in the client for its SHA256SUMS check. They did that for the proxy binary and not for harness witness manifests.

**Fail-open behaviour, stated honestly then partly undone.** `witness-client.ts` returns `{valid: true, unverified: true}` when the kernel is unavailable, with a comment that a caller acting on the signature *"MUST treat `unverified` as 'not actually signed'."* `publish.ts:141` honours that — it **fails closed by default**. But `publish-cmd.ts:26` ships `--allow-unverified-witness`. So the README line *"there is no path to publish an unsigned or tampered harness"* is **overstated by exactly one CLI flag**, and the escape hatch shipped with the feature — the same pattern round one documented for gh-aw's `threat-detection: false`.

**And in ruflo, the equivalent pipeline is broken.** Issue **#2883**, HIGH, five consecutive scheduled runs: witness verification reports `missing=99, drift=18` on all three platforms because the scheduled runner never builds `dist/`, so every manifest entry references a non-existent artifact. The Ed25519 signature verifies; **the thing it signs isn't there.**

**Flag for the leader, load-bearing:** this must **not** be merged with the adjacent-prior-art scout's ASSEMBLE recommendation naming `witness`/in-toto as the attestation plane. **It is a name collision.** ruvnet's "witness" and TestifySec's `witness` share a word and nothing else — no DSSE envelope, no in-toto predicate, no attestation collection, no policy verification, no transparency log. Merging them would silently upgrade a self-signed JSON blob into a supply-chain attestation.

---

## 4. Coverage against the eight concerns, and the buy-before-build fields

| Concern | ruflo + metaharness | Grade | vs. round one's `gh-aw` composition |
|---|---|---|---|
| **Structure** | 174 ADRs; TS+Rust monorepo; per-host config emitters. But the workflow is prompts + skills + MCP tools, **not a compiled artifact**. No `.lock`-equivalent. | **Weak** | gh-aw far stronger (compiler → `.lock.yml`) |
| **Context provisioning** | AgentDB/RuVector HNSW memory, adaptive memory, RAG, `.swarm/` stores | **Strong on paper — and #2887 says a core write path silently drops data on 3.34.0, reproduced by two outside users** | comparable claim, worse evidence |
| **Security** | Blocking dispatch chokepoint on every MCP call; monotone capability envelopes; delegation attenuation (unwired); approvals with self-approval forbidden; ChannelGuard deterministic injection sanitiser at the inter-agent routing boundary; HMAC-anchored policy state | **Richest primitives on this surface — and inert by default with 106 registered env escape hatches** | *deeper* than gh-aw in authority modelling, *far weaker* in enforcement: gh-aw's guarantee comes from Actions, ruflo's comes from the same process as the agent |
| **Introspection** | Signed policy receipts; hash-chained receipt log; OTel attributes package; `casa-receipts.jsonl`; Capability Brain readouts | **Strong** | comparable |
| **Cost transparency & management** | `budget_usd` in the envelope; `maxCostUsd`/`maxTokens` as envelope bounds checked **before dispatch**; `BudgetLimit` with periods and usage in signed policy state; meta-llm gateway cost-tier routing | **The strongest cost story on this surface — and gated behind `enforce` mode.** Closer to *pre-authorised spend per unit of work* than anything round one found, which called it "shipped nowhere" | **round one's "Weak / enforcement absent" needs amending** |
| **Self-improvement** | Automated `[Dream Cycle]` issues filed by the project against itself, harvesting new papers into ADRs; `harness-improvement-ledger.ts` with a monotonic accepted-champion chain; Darwin-mode; flywheel | **Strongest on this surface by a distance** | far beyond gh-aw's health reports |
| **Recovery & durability** | `recovery.ts`, worker daemons, workspace leases, atomic state writes with lock files | **Weak — no durable-execution engine.** The tracker's loudest failures are durability failures | Temporal-class composition remains better |
| **Human steering** | Approvals with expiry/maxUses/revoke; `policy` CLI; separately-authorised publish step | **Adequate for approve/deny; no redirection** | comparable |

### Buy-before-build evidence

**`ruvnet/ruflo`**
- **Scope against our need — and specifically what it does not cover.** Covers: authority-envelope modelling, monotone attenuation, a real blocking dispatch chokepoint, receipts, budgets-as-bounds, self-improvement. **Does not cover:** (i) any enforcement plane the agent lacks credentials for — same-uid, same-process, and the agent has `Bash`; (ii) enforcement being on by default — `legacy` mode allows everything and is the default; (iii) durable execution; (iv) a compiled workflow artifact; (v) derivation from an author-declared phase at the *enforcement* layer (the phase taxonomy exists only as advisory metadata); (vi) the delegation propagator's wiring, stated as unwritten. **The eighty-percent trap here is acute:** the primitives read like coverage, and the two things that make a primitive a guarantee — being on, and being out of the principal's reach — are precisely what is missing.
- **Cost and licence.** MIT, free. **Operational burden is the real cost:** cold `npx` install times out at 60s (#2884), a large deprecated dependency tree, 520 open issues including silent data loss in the memory layer.
- **Lock-in and exit.** Moderate-to-high in practice, low on paper. MIT and self-hostable, but adoption means a 540MB repo, 174 ADRs, `.swarm/` and `.claude-flow/` state layouts, 106 environment variables, and a release train that moves seven times a day. **Bus factor 1.**
- **Composability.** Good — the `@claude-flow/security` policy package is a clean, dependency-light unit (`policy/` is 2,150 lines across 7 files). **Taking `envelope.ts` + `engine.ts` + `evaluator.ts` as a library and enforcing them somewhere else is a genuinely viable assemble move,** and is the single most reusable thing in the ecosystem. The seam: it gives you the *bound*, not the *plane*.

**`ruvnet/metaharness`**
- **Scope vs. need.** Covers harness *scaffolding* across 9 hosts and release signing. **Does not cover** enforcement of anything; the generated policy is a six-entry hand-written deny list. **ADOPT-as-scaffolder at best; irrelevant to the authority question.**
- **Cost/licence:** MIT, free. **Lock-in:** low — it emits config files and gets out of the way. **Composability:** the `host-*` emitter pattern is a decent model for "compile one declaration to several hosts," which is round one's cold-leg C-1 in miniature.

**`outshift-open/outshift-casa`** — *the one that matters*
- **Scope vs. need — and what it does not cover.** Covers: intent-scoped authorization declared in a `MultiAgentSystem` CRD; per-request tool checks in both a deterministic and a semantic flavour, selectable via `enabledToolChecks`; **enforcement at a plane the agent holds no credential for** (Envoy sidecar auto-injected per pod + eBPF deny-by-default egress + token injection on egress / validation on ingress, application-transparent); an operator, an SDK, and a `casa-explorer-ui` with auth-request tables, deny-reason charts, session traces and a MAS graph view. **Does not cover:** (i) discovery of the demand set during execution — scope is static from the CRD plus the initial prompt; (ii) monotonicity or approval-gated widening — unaddressed; (iii) anything outside Kubernetes — **"currently only Istio is supported, Cilium is on the roadmap"**; (iv) phase indexing of any kind; (v) gate-predicate independence.
- **Cost and licence.** **Apache-2.0.** Free. **The operational cost is the entire story: you must run Kubernetes, Istio, and eBPF-capable nodes.** That is what buys you the credential-less plane.
- **Lock-in and exit.** Low on licence, high on substrate. The CRD is portable; the guarantee is Istio's.
- **Composability.** High and directly relevant. **This is the missing enforcement plane in the ASSEMBLE.**
- **Maturity, stated honestly.** **Alpha/PoC by its own README.** Helm chart v0.1.5, CRD `v1alpha1` with *"field-level changes possible before a stable release."* 580 files, 42 open issues, **zero GitHub releases or tags**. Real CI (`ci.yml`, `pytest.yml`, `go-test.yml`, `pre-commit.yml`, `helm-publish.yaml`, `build-push-ghcr.yaml`, `demo-ci.yml`). **7 identifiable Cisco engineers — not bus-factor-1.** Vendor material claims *"better than 90% accuracy"* at identifying authorized vs unauthorized actions; **that number could not be verified from the repository and is `claimed`.**

---

## 5. Per-position verdicts

### P4 — **WOUNDED FURTHER** · verdict **ASSEMBLE (unchanged routing, changed composition)** · **window shortened to ~3–9 months**

**Changes round one and changes the triage report's merged verdict — on composition and on timing, not on routing.**

Round one's ASSEMBLE was `gh-aw` + Temporal-class durability + MCP gateway + sandbox, with the uncovered remainder being *"a capability set derived from the workflow author's own declared `(workflow, phase, agent-role)` triple, compiled into whichever enforcement plane the run targets."* That remainder is now smaller in two places and the assemble list gains two members:

- **Add `outshift-open/outshift-casa` (or an Envoy-sidecar + eBPF equivalent) as the enforcement plane.** Round one's list had no member that enforced an *authority envelope* from outside the principal's process. This one does, at the network layer, application-transparent, Apache-2.0.
- **Add `@claude-flow/security`'s `policy/` package as the envelope algebra.** Monotone reduction, delegation depth, expiry, cost/token/concurrency bounds, approvals with self-approval forbidden — ~2,150 lines, dependency-light, MIT. **Do not adopt ruflo; adopt this subtree.**

**What the BUILD reduces to after this.** Two legs, and they are the load-bearing ones:
1. **Deriving the bound from the demand set observed during execution**, rather than from a CRD or an objective string parsed once up front. Nobody on this surface does it. Everyone declares.
2. **Composing monotonicity with approval** — narrowing freely and unilaterally, widening only through an approval whose issuer is not the principal. Both halves exist in ruflo as *separate* mechanisms; nothing joins them, and Outshift does not address the question.

Everything else in the triage BUILD statement — deriving an authority bound at all, enforcing it deterministically, enforcing it from a plane the principal holds no credential for — **is shipping code somewhere.**

**On the window.** Round one called ~6–12 months on gh-aw's velocity and vocabulary convergence. **Shorten to ~3–9 months, on a sharper signal:** a Cisco team of seven has been building the exact object since April 2026 under a **Linux Foundation-governed** program (AGNTCY), with a research lineage running back through `ASTRA` (October 2025) to **TBAC** (mid-1990s); and a solo operator with a 66,763-star distribution channel found it and shipped an integration ADR pair within about 48 hours of deciding to. **The decisive question has changed from "can this be built" to "why would ours be adopted instead of Cisco's."** No position is held on the answer — that is the owner's call at the gate — but the question is now the right one and it was not the question round one handed forward.

**One counterweight, honestly.** CASA is alpha, `v1alpha1`, Istio-only, 17 stars, zero releases, and requires Kubernetes. A harness that must run on a laptop cannot use it. **That is a real, non-trivial escape route for the BUILD** — but it is an argument about *substrate*, not about *novelty*, and it should be stated that way rather than as "nobody has done this."

### P2 — **WOUNDED (further)** · residue now **one sub-claim only**

- **Leg (i) — phase-indexed derivation.** Round one falsified the weak form and left the strong form ("from an author-declared phase as a first-class construct") standing. **It no longer stands cleanly.** `capability-brain.ts` types every capability domain and every tool with `loopPhases: Array<'discover'|'recall'|'authorize-claim'|'route-plan'|'branch-propose'|'execute'|'validate-critique'|'commit-validated'|'observe'|'publish'>` **and** `authority: 'advisory'|'capability-plane'|'control-plane'` **and** `risk: 'read-only'|'reversible'|'privileged'` **and** an 11-value `riskFlags` set including `spend`, `promotion`, `approval`, `concurrency`. That is a first-class, author-declared phase construct with capability and authority indexed against it, shipped in a released npm package. **It is advisory metadata, not enforcement** — the module says so — so the *enforcement* form survives. **Narrowing to carry: the novelty is not "index capabilities by declared phase"; it is "enforce that index."** And `outshift-open/tbac-research-datasets` names the prior art out loud: **Task-Based Access Control**.
- **Leg (ii) — gate-soundness. SURVIVES, second legible negative.** **Searched:** all 174 ruflo ADRs, the `@claude-flow/security` policy engine, evaluator, envelope, propagator and product-plane, the CASA compiler/schema/enforce on both sides, metaharness's `harness/src/` (consensus, verifier, safety, recovery, score), the `flywheel` and `darwin-mode` packages, and `outshift-casa`'s file tree. **What was expected and not found:** any statement, in code or ADR, that a validation predicate must not read what the validated step produced. **What exists instead is adjacent but different**: ruflo's `harness-improvement-ledger.ts` requires each accepted champion to *strictly beat* its baseline (monotonicity over scores), and `redblue` enforces cross-actor review — separation of *actors*, not separation of *reads*. Round one's verdict on this leg is unchanged and now doubly attested.
- **Leg (iii) — spec-derived ceiling. FALSIFIED, reinforced twice.** `compileObjectiveToEnvelope()` derives the ceiling from free-text intent; Outshift CASA derives it from a `MultiAgentSystem` CRD. Round one's caveat — *"derive from a closed enumeration is shipped; derive from an open declaration is not"* — **still holds**: ruvnet's compiler is a 6-row table over 5 fixed scopes; CASA's CRD is a declared enumeration.
- **New leg (iv), which the theme never claimed but the BUILD statement does — monotone capability attenuation. NOT NOVEL.** `isEnvelopeReduction`, `capability-envelope-cannot-grow`, `delegationDepth` decrement, and an `AuthScope` documented as *"the same shape as OAuth scope reduction."* Shipped, unit-tested, in npm. **If any downstream document treats monotonicity as the novel part, it is wrong.**

**Overall: WOUNDED further. The residue is gate-predicate independence, plus the composition of monotonicity with an approval path, plus enforcement of a phase index. Everything else has a shipping counter-example.**

### P3 — **WOUNDED** · round one's narrowing **reinforced and extended**

1. **Someone else wrote the theme's P3 position, verbatim, in code, two days ago.** ruvnet's `enforce.ts` and `compile.ts` both carry a "LOAD-BEARING INVARIANT" block stating that translation *may* use an LLM and enforcement *must never*. That is convergent, independent, and it means the position is not a differentiator — it is becoming the field's default.
2. **And the upstream it was copied from does the opposite.** Outshift CASA's `enabledToolChecks` selects, **per multi-agent system**, between *"Deterministic Checks — rule-based validations, fast, no AI required"* and *"Semantic Checks — AI-powered validation that matches the requested tool against the original user intent using embeddings or an LLM verifier."* Vendor material claims *"better than 90% accuracy"* — **on an enforcement decision, ~10% error is precisely what "a tendency, not a guarantee" means**, and Cisco ships it anyway, because a deterministic rule cannot answer "does this tool call still match the user's intent."
3. **The bypass evidence is heavier than round one's.** ruflo's enforcement is **off by default**, delegation enforcement sits behind a strict-auth env var, and the project maintains an **audited registry of 106 environment-variable escape hatches** in which that variable is explicitly *registered as a documented escape hatch*. This is round one's #29171 pattern, industrialised. **Three for three now on institutionalised bypass** — ours twice, gh-aw once, ruflo systemically.

**The new narrowing to carry forward:** the field is not choosing between determinism and inference. It is making **the determinism/inference boundary a configuration field, set by an operator, per check, and recorded** (`enabledToolChecks`, `policy mode`, `translator`). **The theme has no position on that, and "minimize inference" is not a position on it.** The design question is *which checks may be probabilistic, who decides, and where the decision is recorded* — a different and more useful piece of work than counting model calls.

### P5 — **SURVIVES, ranking wounded** · **sharpened, and one new problem named**

**For:** ruflo issue **#2768** — *"[Dream Cycle 2026-07-24] swarm: **ClawArena shows privilege-granting is the #1 orchestration bottleneck** (ADR-320)"*. An external benchmark naming our #1 concern as the field's #1 bottleneck. Reinforced by citations embedded in ruflo's own code: arXiv **2605.05440** on authorization propagation (*"RBAC/ABAC on agent roles do not solve this — roles don't compose under dynamic LLM delegation"*), **2605.28914**, **2605.22333**, **2607.19430**. And Cisco has funded a seven-person team against it for four months.

**Against, and it is the sharper half.** On a 66,763-star harness with 1,550 issues, the loud user reports are: **silent memory-write data loss** (#2887, independently reproduced), **cold-install timeout** (#2884), **broken release verification** (#2883), **routing accuracy** (#2886), **backup integrity** (#2895), **concurrent-write loss** (#2878). On metaharness's ~20 lifetime issues, external reporters ask for `proxy whoami`, auth-readiness reporting, dependency-pin bumps, and `--force` honouring. **Not one external issue on either tracker asks for an authority bound.** Every authorization item found was **self-filed by the maintainer or by an automated dream-cycle** harvesting papers.

**The sharpened verdict:** the demand for authority-bounding is loud in **research and vendor** channels (arXiv clusters, Cisco, benchmarks) and **near-silent in user** channels, where the demand is for durability, correctness, and install weight. Round one said the ordering is wrong. **The more specific and more uncomfortable statement: this is currently a supplier-side demand.** That does not make it unreal — supplier-side demand precedes user-side demand routinely, and Cisco's investment is a genuine signal — but P5's evidence base is *"vendors and researchers agree this matters"*, not *"users are asking."*

### P1 — **NEEDS-A-PROBE** (unchanged) · **one leg strengthened**

Round one's declared hole stands: the ~30-reference list is still not visible, and this surface still cannot discharge P1. **W1 owns it.**

**One leg strengthened, from artifacts rather than citations.** The claimed *"workflow authorization from the mid-1990s"* lineage has a **live, funded descendant**: `outshift-open/tbac-research-datasets` — **TBAC, Task-Based Access Control** — alongside `outshift-open/ASTRA`, *"Authorization with Semantic **Task-based** Restricted Access."* A Cisco research team building datasets and a reference implementation on a mid-1990s task-based authorization model, in 2026, is the strongest available artifact-side support that this leg of P1 is real and not a plausible-sounding invention. **This does not verify any specific identifier** — a real subfield existing is exactly the condition under which a fabricated citation hides.

**No change to round one's one hit against** (the claimed "published synthesis-to-runtime-monitor compiler," nearest instance PCAS, code unreleased, synthesis explicitly disclaimed).

---

## 6. Why round one missed it — the method finding

Round one searched **by mechanism vocabulary** — "policy compiler," "capability derivation," "MCP gateway," "sandbox," "durable execution," "agent authorization" — and it searched **where those words are used**, which is popular repos, vendor docs, arXiv, and standards blogs. That method is structurally blind in two directions at once, and both fired here. **First, vocabulary:** ruvnet's entire ecosystem self-describes as *swarm*, *hive-mind*, *flow*, *meta-harness*, *dream cycle* — the words a scan for authorization mechanisms never emits. The one query that would have surfaced ruflo directly is not a mechanism query at all: `gh search repos --topic harness --topic claude-code --sort stars`, or simply enumerating `ruvnet`'s repos, which takes one API call. **Second, and worse, popularity:** the thing that actually matters — `outshift-open/outshift-casa` — has **17 stars**, its predecessor `ASTRA` has **5**, and the dataset repo has **4**. No star-ranked or relevance-ranked search reaches them; they are found only by walking an *organization* after something else names it, which is exactly the path taken here (ruflo's ADR-380 → AGNTCY → Outshift → CASA). Round one's own declared holes were honest and in the right spirit, but they were holes in *coverage*, and this was a hole in *method*. **The method finding for the leader: the four-surface standard tells each scout what to look at and gives it an alias-flagging duty across surfaces, but it gives no instrument for aliases *within* a surface. An active-development scout needs at least one organization-walk and one deliberately low-star pass, because on this surface the incumbent's answer arrives at four figures of stars and the *research* answer arrives at two.** Timing is a partial mitigation and not an excuse: ruvnet's CASA integration was 24–48 hours old when round one ran, but `outshift-casa` has existed since 2026-04-17 and `ASTRA` since 2025-10-28, and both were reachable the whole time.

---

## 7. Cold leg — assumptions nobody put on the list

### C-4 (candidate position) — the theme has never priced the enforcement plane. **A credential-less plane is bought with operational surface, and there is no zero-ops instance of one.**

Round one's C-1 asked *runtime or compiler*. This is the question underneath it. Every system that genuinely achieves "a plane the principal holds no credential for" pays for it in infrastructure the principal cannot reach: gh-aw pays **GitHub Actions**; Outshift CASA pays **Kubernetes + Istio + eBPF**; `rvm` pays **a hypervisor**. Every system that refuses to pay — ruflo, metaharness, Claude Code hooks, every in-process `PolicyGate` — ends up same-uid with the agent, at which point the bound is advice to a principal holding `Bash`. **No counter-example was found on this surface: no system enforces from outside the principal's reach without requiring an operator to run something.** The theme's five positions, JURATI's "single edge where all LLM calls originate," and the whole shortlist are silent on what operational cost the guarantee is permitted to have — and that silence is doing load-bearing work, because it is the only reason "build it ourselves" and "adopt Outshift CASA" look like comparable options. **They are not comparable until someone states the ops budget.** If the answer is "it must run on a laptop with no daemon," the credential-less plane is out of reach by construction and P3's whole determinism argument is secondary to a sandboxing argument. If the answer is "an operator may run a sidecar," CASA is most of the product. **The run should decide the ops budget before it decides anything else** — upstream of round one's C-1, C-2 and C-3 alike, since a compiler, layered enforcement, and enforcement-layer pluggability are all just different ways of spending that budget.

### C-5 — the theme assumes **one principal per run**. Everything shipping assumes **a delegation graph**.

All five positions say "an agent," "a principal," "the harness." Every serious system read here is organized around *many* agents handing work to each other: CASA's CRD is literally a `MultiAgentSystem`; ruflo's propagator exists because *"when agent A delegates to agent B via SendMessage, B can escalate the granted scope by calling tools A was never authorized to invoke"*; ChannelGuard exists because *"individually-safe agents still propagate prompt-injection payloads to peers through inter-agent message channels — each hop's own safety check can pass, because the payload is a legitimate output of that hop."* **If the unit of authority is a delegation chain rather than a principal, the central object is attenuation-across-hops, not a phase-indexed bound** — and this repo is itself a five-role delegation graph (leader → scouts → curator → goal-owner) with, per round one's dogfood-signal, no `tools:` frontmatter on any of them. The theme has a single-principal frame and a multi-principal artifact.

### C-6 — "cost transparency and management" is **two concerns**, and this surface proves the second one is tractable.

Round one flagged that this concern fuses metering (solved everywhere) with pre-authorisation of spend (shipped nowhere) and predicted the fusion would hide the real gap at triage. **It did, and the gap is smaller than round one thought.** `checkCapabilityEnvelope` evaluates `action.costUsd <= envelope.maxCostUsd` and `action.tokens <= envelope.maxTokens` **before dispatch**, alongside `BudgetLimit` with periods and rolling usage in signed policy state, and `budget_usd` is a first-class field of the CASA envelope on both sides of the ruvnet integration. That is pre-authorised spend per unit of work, at the tool-call boundary, in released code — **the thing round one recorded as "shipped nowhere."** It is gated behind `enforce` mode and none of it was run, so it is `claimed`. But **the concern must be split before triage reads it again**, or the register will keep scoring a solved item as open.

---

## Reuse / dedup notes

- **Dedup performed** against wfh-001's filed technologies (#137, #141, #143, #144, #146, #149, #150, #159, #160) and against round one's file. **Nothing in this file duplicates a filed node.**
- **New to the graph:** `ruvnet/ruflo` (né `claude-flow`), `ruvnet/metaharness`, `@claude-flow/security` policy package, **`outshift-open/outshift-casa`**, `outshift-open/ASTRA`, `outshift-open/tbac-research-datasets`, the AGNTCY/Outshift Internet-of-Agents programme.
- **Round one's flag ① stands and widens:** neither `github/gh-aw` **nor** anything in the ruvnet or Outshift ecosystems has a Unimatrix node. The theme's watchlist does not name any of them.
- **Correction candidate for the curator, not a new candidate:** any node carrying wfh-004/W0-a's *"no framework ships pre-authorized spend per unit of work"* needs the same treatment round one proposed for #160 — a content correction with fresh evidence (C-6 above).
- **Source signal:** `external-scan` throughout. No dogfood-signal in this round.
- **Firewall:** every find is `claimed` at best. No code was run — cloned checkouts, API responses, and vendor prose, with which is which stated at each claim. **No status moves.**

## Suspected cross-surface aliases — flag, do not merge

- **`(workflow, phase, agent-role)` → capability set** is called **Task-Based Access Control (TBAC)** in W1's literature — Thomas & Sandhu, mid-1990s — and Cisco Outshift is publishing **research datasets under exactly that name** in 2026 (`tbac-research-datasets`), with `ASTRA` as the "semantic task-based" variant. **This is the single strongest alias flag in the run and it directly serves P1's mid-1990s leg and P2's absence claim.** W1 must chase TBAC by name.
- **"Authority envelope" / "capability envelope"** is almost certainly W1's **arXiv 2606.03518, *"Overlaying Governance: A Compositional Authorization Framework for Delegation and Scope in Agentic AI"***, described as introducing *authorization envelopes* with delegation, scope and contextual constraints as first-class constructs. **Not verified beyond a title and URL — W1 owns it**, and if it holds it is a direct hit on P2.
- **Four more arXiv identifiers are cited inside ruflo's own source comments** and should go to W1: **2605.05440**, **2605.28914** (AIRGuard), **2605.22333** (MCP auth survey), **2607.19430** (ChannelGuard). Note that ruflo assigns its own grades to citations — treat the grade as the project's opinion, not evidence.
- **"Witness" is a name collision and must not be merged.** ruvnet's `witness.json` is a home-grown Ed25519 manifest with the verifying key inside the document; TestifySec's `witness` / in-toto is DSSE-enveloped attestation with an external trust root and policy verification. W4's ASSEMBLE recommendation refers to the latter.
- **Outshift CASA's "semantic checks"** will appear in W2 as **"AI guardrails"** and in W1 as **model-based intent-alignment with measured accuracy**. The **>90% accuracy** figure is the number to chase — round one noted gh-aw ships no numbers at all, and this is the first vendor on this surface to publish one.
- **"Intent-scoped authorization"** is likely W2's **"agent authorization gateway"** and W4's **task-based / activity-based access control**.

## Theme-revision signal, for the owner gate (relayed, not acted on)

**C-4 — the ops budget for the enforcement plane is unstated, and it is upstream of the build-versus-adopt decision.** Until the theme says what operational surface a guarantee is allowed to cost, "build the plane ourselves" and "adopt an Envoy/eBPF sidecar" are not comparable options and the P4 routing cannot be read honestly. This run is not permitted to settle it and should not; it should reach the owner verbatim alongside round one's C-1.

## `cites:`

```yaml
cites:
  - type: repo
    ref: https://github.com/ruvnet/ruflo
    title: "ruflo — the original agent meta-harness (formerly ruvnet/claude-flow; npm @claude-flow/cli)"
    author: "ruvnet"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/blob/main/v3/@claude-flow/security/src/policy/envelope.ts
    title: "checkCapabilityEnvelope / isEnvelopeReduction / delegateEnvelope — monotone capability envelopes, throws capability-envelope-cannot-grow"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/blob/main/v3/@claude-flow/security/src/authorization/propagator.ts
    title: "AgentAuthorizationPropagator — monotonically reducing AuthScope across delegation hops (ADR-144 P1; header states no call sites yet)"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/blob/main/v3/@claude-flow/cli/src/mcp-client.ts
    title: "ADR-324 policy chokepoint — authorizeMcpTool on every MCP dispatch, throws before tool.handler"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/blob/main/v3/@claude-flow/security/src/policy/evaluator.ts
    title: "evaluatePolicy — enforcedOutcome is 'allowed' unless mode === 'enforce'; legacy-default-allow"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/blob/main/v3/@claude-flow/cli/src/mcp-tools/capability-brain.ts
    title: "Ruflo Capability Brain — loopPhases, authority (advisory|capability-plane|control-plane), risk flags; 'deliberately data-only'"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://github.com/ruvnet/ruflo/blob/main/v3/docs/adr/ADR-380-agntcy-outshift-runtime-integration.md
    title: "ADR-380 — AGNTCY/Outshift Runtime Integration: SLIM Transport, CASA Enforcement, IOC Coordination Events (Status: Proposed, 2026-07-30)"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agntcy/src/casa/enforce.ts
    title: "CASA checkAuthorization — pure deterministic deny-by-default gate; 'ENFORCEMENT must NEVER call an LLM' invariant; no call sites outside tests"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/issues/2768
    title: "[Dream Cycle 2026-07-24] ClawArena shows privilege-granting is #1 orchestration bottleneck (ADR-320); maintainer concedes durable cross-process enforcement remains open"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/issues/2883
    title: "[verification] HIGH: Witness verification reports missing artifacts for all 3 platforms (missing=99, drift=18; dist-not-built)"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/issues/2887
    title: "agentdb_hierarchical-store returns success:true but persists NOTHING — silent data loss, independently reproduced on 3.34.0"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/issues/2894
    title: "MCP: policy_evaluate crashes (-32603); validation errors returned in-band with isError never set"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/ruflo/issues/2884
    title: "[verification] HIGH: @claude-flow/cli@alpha --version times out (>60s, SIGTERM) in cold-cache npx"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/metaharness
    title: "metaharness — meta-harness for AI agents; scaffolds a branded harness with npx CLI, MCP server, memory, learning loop, witness-signed releases"
    author: "ruvnet"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/metaharness/blob/main/crates/kernel/src/witness.rs
    title: "Witness manifest — home-grown Ed25519 (ed25519-dalek) over a custom canonicaliser; verifying key embedded in the manifest, no external trust root"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/metaharness/blob/main/packages/create-agent-harness/src/witness-client.ts
    title: "verifyWitness — degraded shape-only mode returns valid:true with unverified:true; publish fails closed unless --allow-unverified-witness"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/metaharness/blob/main/packages/agntcy/src/casa/compile.ts
    title: "compileObjectiveToEnvelope — deterministic 6-rule regex table over 5 scopes; optional translator patch unions into allow and removes from deny (widening path)"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/metaharness/blob/main/packages/harness/src/safety.ts
    title: "PolicyGate — 87-line in-process default-deny policy gate with JS-closure matchers and max-risk ceiling"
    org: ruvnet
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/outshift-open/outshift-casa
    title: "outshift-casa — Continuous Agent Semantic Authorization: intent-scoped authorization for Kubernetes multi-agent systems, enforced at the network layer (Envoy sidecar + eBPF; Apache-2.0; alpha/PoC, Helm v0.1.5, CRD v1alpha1)"
    org: "Cisco Outshift"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/outshift-open/ASTRA
    title: "ASTRA — Authorization with Semantic Task-based Restricted Access"
    org: "Cisco Outshift"
    year: 2025
    surface: active-dev
  - type: repo
    ref: https://github.com/outshift-open/tbac-research-datasets
    title: "TBAC Research Datasets — Task-Based Access Control research artifacts"
    org: "Cisco Outshift"
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://outshift.cisco.com/the-internet-of-agents
    title: "Internet of Agents — AGNTCY programme (Linux Foundation)"
    org: "Cisco Outshift"
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://www.linkedin.com/pulse/agents-reach-consensus-93-time-introducing-mycelium-casa-uvqfe
    title: "Agents that reach consensus 93% of the time: Introducing Mycelium and CASA (claims CASA identifies authorized vs unauthorized actions at >90% accuracy — UNVERIFIED)"
    org: "Cisco Outshift"
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://docs.agntcy.org/dir/hosted-agent-directory/
    title: "AGNTCY — Hosted Outshift Agent Directory"
    org: AGNTCY
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2606.03518
    title: "Overlaying Governance: A Compositional Authorization Framework for Delegation and Scope in Agentic AI (authorization envelopes — UNVERIFIED, flagged to W1)"
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2605.05440
    title: "Authorization Propagation (cited in ruflo propagator: roles do not compose under dynamic LLM delegation)"
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2607.19430
    title: "ChannelGuard — prompt-injection propagation through inter-agent message channels"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ruvnet/agentic-flow
    title: "agentic-flow — low-cost model switching for Claude Code / Agent SDK (NO LICENCE declared)"
    author: "ruvnet"
    year: 2026
    surface: active-dev
```

---

## Compact return

| Find | In/out of lens | New/known | Buy-before-build evidence present? |
|---|---|---|---|
| **`outshift-open/outshift-casa`** (Cisco, Apache-2.0, 17★, alpha) | **In** | **New** | **Yes — full.** The enforcement plane the ASSEMBLE was missing. Gap named: no runtime demand discovery, no monotonicity, Istio/K8s only |
| `ruvnet/ruflo` (66.8k★, MIT, bus factor 1) | In | New | **Yes — full.** Adopt the `@claude-flow/security` `policy/` subtree, not the product |
| `ruvnet/metaharness` (534★, MIT) | In (weakly) | New | Yes. Scaffolder; irrelevant to authority. Witness ≠ in-toto |
| `outshift-open/ASTRA` + `tbac-research-datasets` | In | New | Partial — research artifacts. **Alias goldmine for W1** |
| `ruvnet/agentic-flow`, `rvm`, `rudevolution`, `SAFLA`, `sparc`, ~90 others | Mostly out | — | n/a — checked and cleared |

| Position | Verdict | Effect on round one / triage |
|---|---|---|
| **P4** | **WOUNDED further** → **ASSEMBLE**, window **~3–9 months** | **Changes both.** Assemble list gains `outshift-casa` (enforcement plane) + `@claude-flow/security` `policy/` (envelope algebra). BUILD shrinks to two legs: **demand discovered during execution**, and **monotone-with-approval-to-widen** |
| **P2** | **WOUNDED further** | **Changes leg (i)**: the strong form has a shipped instance (`loopPhases` × `authority`), advisory not enforced. **Reinforces leg (ii)** SURVIVES with a second legible negative. **Reinforces leg (iii)** FALSIFIED. **Adds leg (iv): monotone attenuation is NOT novel** |
| **P3** | **WOUNDED** | **Reinforces + extends.** ruvnet wrote our position verbatim in code; Outshift ships **inference on the enforcement path** at a claimed >90% accuracy, selectable per-check. New narrowing: **the determinism/inference boundary is becoming a config field** |
| **P5** | **SURVIVES, ranking wounded** | **Reinforces + sharpens.** ClawArena names privilege-granting #1. But **zero external issues on either tracker ask for an authority bound** — this is currently **supplier-side demand** |
| **P1** | **NEEDS-A-PROBE** (unchanged) | **Strengthens the mid-1990s leg** via TBAC artifacts. Still cannot see the list; W1 owns it |
| **Cold leg** | **C-4 (candidate position) + 2** | C-4: **the ops budget for a credential-less plane is unstated and upstream of build-vs-adopt.** C-5: single-principal frame vs. delegation-graph reality. C-6: pre-authorised spend is **shipped**, correcting W0-a |

**Flags for the leader:** ① **"Witness" is a name collision** — do not merge ruvnet's self-signed Ed25519 manifest with W4's in-toto attestation plane. ② **TBAC is the alias W1 must chase**; it serves P1's mid-1990s leg and P2's absence claim simultaneously. ③ **arXiv 2606.03518 needs verification by W1** — if it holds, it is a direct hit on P2's envelope novelty. ④ **Method finding:** the active-dev surface needs an organization-walk and a low-star pass; the decisive find here has 17 stars and no relevance-ranked search reaches it. ⑤ **Theme-revision signal C-4 goes verbatim to the owner** alongside round one's C-1. ⑥ **Correction candidate:** wfh-004/W0-a's "no framework ships pre-authorized spend per unit of work" is out of date.
