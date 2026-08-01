# scout-products.md — wfh-005 challenge scan, established-products surface

**Run:** wfh-005 · CHALLENGE mode · surface **W2 — established products** · `agent_id: wfh-005-scout-products`
**Read-only on the graph. Zero writes. Nothing here moves status; everything below is `claimed` at best.**
**Evidence discipline:** every capability and price statement sourced from a vendor page is a **vendor claim**, marked `[doc-claim]`. `[demonstrated]` appears nowhere in this file — I ran none of these products. Secondary/SEO-grade sources are marked `[secondary]` and are used only for orientation, never as the basis of a verdict.

---

## Surface coverage report

**Searched (venues / hunting grounds):**
- **The nearest shipping instance:** `github/gh-aw` — repo, and the docs site `github.github.com/gh-aw` (architecture, safe-outputs, threat-detection, engines, cost-management, frontmatter, firewall). Also its issue tracker (#18311, #23198).
- **Cloud agent runtimes with an authorization story:** Amazon Bedrock AgentCore (Runtime · Gateway · Identity · **Policy**, GA 2026-03-03), Microsoft Entra Agent ID + Agent 365 + Foundry agent identity, Google Vertex AI Agent Engine agent identity, OpenAI AgentKit / Agent Builder, CrewAI Enterprise, LangGraph Platform / LangSmith.
- **Policy engines:** Cedar (via AgentCore Policy), OPA/Gatekeeper, Kyverno.
- **Workload identity & credential brokers:** SPIFFE/SPIRE, HashiCorp Vault (SPIFFE auth method, dynamic secrets), GitHub Actions OIDC, GCP Workload Identity Federation.
- **CI/CD with derived per-job identity:** GitHub Actions (`permissions:`, environments, OIDC claims), Argo Workflows, Tekton, Airflow, Harness/Spinnaker (shallow — see skips).
- **AI gateways / cost enforcement:** Cloudflare AI Gateway spend limits, LiteLLM virtual keys, Portkey, Kong AI Gateway.
- **MCP gateway / tool-permission tier:** Docker MCP Gateway, Obot, agentgateway (Solo.io), Pomerium, MintMCP, MCPJungle, Composio, Arcade.dev.
- **Model-on-the-enforcement-path products:** gh-aw threat detection, Bedrock Guardrails, Azure Prompt Shields, Lakera Guard, OpenAI Guardrails, NeMo (shallow).
- **Coding-agent enterprise governance:** Claude Code managed-settings + MDM precedence, Anthropic Enterprise admin surface.
- **Standards:** MCP authorization specification (fetched the normative page directly).
- **Buyer-demand proxies:** CSA Labs research note (2026-04-03), EY/AIUC-1 consortium figures as quoted, Gartner Hype Cycle category naming, OpenAI's own deprecation notices.

**Deliberately skipped, with reason:**
- **Harness / Spinnaker / Azure DevOps stage-scoped RBAC** — one search returned integration marketing, not permission semantics. **Declared hole.** The specific unanswered question is whether any commercial CD platform binds a *credential set* to `(pipeline, stage, role)` as one derived object rather than three hand-configured knobs. Cheap to close; I ran out of budget before the primary docs.
- **n8n / Zapier / Dify / Windmill / Kestra** — re-projected already in wfh-004 `W0-a` family C/E; nothing in this run's positions turns on them.
- **Devin / Cursor / Windsurf / Replit / Factory** — held as `#139`–`#145`; re-scanning them answers none of the five positions.
- **Pricing behind sales calls** — AgentCore Policy per-tool-call charges, Entra Agent ID / Agent 365 list pricing, LangSmith Enterprise, Obot Enterprise. **Could not verify.** Every "Enterprise: contact sales" below is an admission of ignorance, not a finding.
- **Any hands-on evaluation.** No product below was installed, run, or measured by us.

**Exhaustion is bounded** to these five positions and this one surface. It is not absolute.

---

## P4 — **WOUNDED, severely** · routing: **ASSEMBLE + a narrow BUILD**

**The position as three runs implicitly held it — "nothing shipping or assemblable covers this, therefore build the harness" — does not survive contact with the products surface.** What survives is a much smaller claim about one layer.

The decisive find is that **`gh-aw` is no longer what wfh-001 characterized.** It has moved from `githubnext` to the **`github`** org, is **MIT-licensed**, ~4.8k stars, and now ships mechanisms in **seven of the eight concerns** — including two (cost *enforcement*, self-improvement) that `W0-a` recorded as "nobody ships," with `W0-a` §5 flag 3 already warning those verdicts were absences in *our evidence*. That warning was correct.

Second decisive find: **AgentCore Policy** (GA 2026-03-03) ships the exact sentence this theme's security thesis is built on, as marketing copy: *"Every agent action through Amazon Bedrock AgentCore Gateway is intercepted and evaluated at the boundary outside of agent's code — ensuring consistent, deterministic enforcement that remains reliable regardless of how the agent is implemented."* `[doc-claim]`

### Candidate table

| Product | Covers (of the 8 concerns) | Does **NOT** cover | Cost / licence | Lock-in & exit | Composability |
|---|---|---|---|---|---|
| **GitHub Agentic Workflows (`gh-aw`)** — markdown workflow compiled to a `.lock.yml` GH Actions workflow | **Structure** (durable authored `.md` → compiled multi-job pipeline; imports; SHA-pinned). **Context provisioning** (frontmatter declares tools/MCP servers/imports; agent prompt is the file). **Security** (read-only agent job by default; **safe-outputs** = agent emits JSON requests, a *separate* job with scoped `permissions:` executes them; Agent Workflow Firewall = container + iptables + Squid domain allowlist; tool allowlist; pre-activation role checks; compile-time scanners actionlint/zizmor/poutine). **Introspection** (`gh aw logs`/`audit`, OTLP export). **Cost** (`max-ai-credits` = *hard budget per run*, default 1000; `max-turns` on Claude). **Self-improvement** (`gh aw mcp-server` exposes logs/audit/compile to an agent — a scheduled meta-agent can inspect and rewrite other workflows). **Human steering** (pre-activation role gate; threat-detect warning → `REQUEST_CHANGES` review requiring human approval; PR as the gate) | **Recovery/durability** — a GH Actions job is the unit; no mid-run resume of a dead agent session. **Per-agent capability sets *within* a workflow** — docs describe per-*job* scoped permissions, not per-agent-role. **Mid-run redirection** — nothing enters a live agent job. **Prospective context statement** — no "what is about to be injected and why." **Any substrate but GitHub Actions.** **Tool least-privilege inside the agent** — open issue: all gh-aw workflows currently pass `--allow-all-tools` regardless of declared need (#23198) | **MIT.** Compute = GH Actions minutes + your own model account (Copilot/Claude/Codex/Gemini). No licence fee `[doc-claim]` | **Engine lock-in: low** — four engines, "pick whichever AI account you already have." **Substrate lock-in: total** — runs inside GH Actions; the `.md` is portable prose, the compiled `.lock.yml` is not. Exit = rewrite the execution layer, keep the prompts. Maturity caveat is the vendor's own: *"Use it with caution, and at your own risk"*; a billing bug spanned releases 0.68.4–0.71.3 | High *within* GitHub — composes with Actions environments, OIDC, branch protection, any MCP server. Zero outside it |
| **Bedrock AgentCore Policy + Gateway** | **Security** — Cedar policies at the Gateway; **default-deny, forbid-wins**; per-tool-call interception; `LOG_ONLY`/`ENFORCE`; CloudWatch decision logs. **Introspection** (decision audit). Adjacent AgentCore components add Runtime/Memory/Identity | **Structure** — no workflow definition; it authorizes calls, it does not sequence work. **Context provisioning** — none. **Cost enforcement** — separate billing surface, not a work-step budget. **Self-improvement** — none. **Recovery** — none. **Human steering** — none. **No phase.** Principals are only `AgentCore::OAuthUser` and `AgentCore::IamEntity`; there is no workflow, step, or task entity | Proprietary AWS. 12 independently billable components; **Policy's per-tool-call charge is not on the public pricing page** — **could not verify** `[secondary]` | Deep: Cedar policies are portable (open-source language), but the *enforcement point* is the AgentCore Gateway. Exit = re-host every tool behind a different gateway | Good as a **tool-call chokepoint** under any orchestrator. It wants to own the tool plane, not the workflow plane |
| **Temporal** | **Recovery/durability** (best in class — event-sourced replay; OpenAI runs Codex on it `[secondary]`). **Human steering** — **Signals** deliver external intent *into a running workflow*, which is the mechanism `W0-a` flagged as the counterexample to its own human-steering gap. **Structure** (workflow-as-code) | **Security** — no agent-authority model. **Context provisioning** — no concept of what a model was shown. **Cost** — counts actions, not tokens. **Self-improvement** — none | OSS (MIT) + Temporal Cloud (usage-based); Series D Feb 2026 `[secondary]` | Determinism constraint on workflow code is the real cost; self-host is a genuine exit | Excellent — sits under anything. This is the assemble-candidate for concerns 7 and 8 |
| **AI gateways** (Cloudflare AI Gateway / LiteLLM / Portkey / Kong) | **Cost — enforcement, not just transparency.** Cloudflare: spend-limit rules, up to 20/gateway, scoped by model/provider/custom metadata, split or filter mode; over budget → **`429` until the window resets**, or fallback to a cheaper model. LiteLLM: per-virtual-key budget caps. **Introspection** (per-request cost attribution) | Everything else. No structure, no authority model, no context provisioning | Cloudflare AI Gateway: platform pricing; LiteLLM: OSS; Portkey/Kong: tiered `[doc-claim]` | Low — a proxy base URL | Excellent. Drop-in |
| **MCP gateway tier** (Docker MCP Gateway, Obot, agentgateway, Pomerium, MintMCP) | **Security** — centralized identity, RBAC, per-user OAuth passthrough, policy-as-code, per-server sandboxing (Docker), audit `[secondary]` | Structure, context provisioning, cost enforcement, self-improvement, recovery, steering. Honest note from a competitor's own comparison: agentgateway *"allows simple rules like 'Agent X can access Tools A and B', but lacks RBAC, multi-tenancy, and audit logging"* `[secondary]` | Mixed: Docker MCP Gateway and Obot have OSS cores; enterprise editions gated | Moderate — MCP is a standard, gateways are swappable | Excellent, and this is where the tool-authority seam is being commoditized right now |
| **SPIFFE/SPIRE + Vault** | **Security** — attested workload identity → JWT-SVID → Vault policy → **short-lived dynamic credential per job**. This is per-job credential minting, shipping, mature | Everything else. No workflow, no agent semantics | OSS (Apache-2.0 / BUSL for Vault) | Low (both self-hostable); operational burden is high | Excellent — this is the credential-minting leg of any assembly |
| **Entra Agent ID / Agent 365** | **Security** (agent-as-first-class-identity in the IdP, lifecycle, least-privilege assignment), **Introspection** (end-to-end logging: identity, role, scope, tool, action, correlation IDs) `[doc-claim]` | Structure, context provisioning, cost, self-improvement, recovery, steering. No workflow phase | Enterprise licensing — **could not verify pricing** | Very deep — Microsoft identity plane | Composes only if you are already Entra-shaped |
| **Vertex AI Agent Engine agent identity** | **Security** — custom service account per agent, IAM Allow/Deny policies | As above; also no phase | GCP usage-based | Deep (GCP) | Same shape as Entra |
| **LangGraph Platform / LangSmith** | **Structure** (state graph), **Introspection** (best in class), **Recovery** (checkpointer), **Human steering** (interrupt → edit state → resume) | **Security** — RBAC on the *platform*, none on the *agent's authority*. Cost = observation, not enforcement | LangGraph Platform from ~$35/mo; Plus $39/seat/mo; **self-host is Enterprise-only** `[secondary]` | Framework-level lock-in (graph is Python/TS objects); self-host gated behind Enterprise pricing | Moderate |
| **Claude Code managed settings** | **Security / human steering** — admin policy at the top of the precedence chain that *"developers cannot override"*; the permission-bypass CLI flag removed entirely under policy; delivered by MDM or from Anthropic's servers. **Cost** (spend caps), **Introspection** (Compliance API) `[doc-claim]` | Structure, context provisioning, self-improvement, recovery. Single-vendor | Enterprise plan | Total vendor lock-in — this is *the* thing the theme's any-LLM-pluggable bias exists to avoid | Does not compose; it is a per-vendor control |
| **OpenAI AgentKit / Agent Builder** | *(was)* Structure (visual canvas), Guardrails, **User Approval node** (human checkpoint mid-flow), Connector Registry | — | — | **Deprecated 2026-06-03; read-only 2026-10-31; shut down 2026-11-30.** Export path: Agents SDK | See P5 |

### The uncovered remainder, named precisely

Assemble the best of the above — `gh-aw` for structure/context/compilation, AgentCore-Policy-or-an-MCP-gateway for per-tool-call authority, Temporal for durability and signals, Cloudflare/LiteLLM for hard budget, SPIRE+Vault for credential minting, Langfuse/OTel for introspection — and **~85% of the eight concerns is covered by shipping, mostly-OSS parts.** Four things are left, and they are the load-bearing four:

1. **One declared workflow object from which *every* enforcement plane's ceiling is derived.** Each product derives its ceiling from *its own* declaration and no other: gh-aw's compiler derives the Actions `permissions:` blocks from the `tools:`/`safe-outputs:` frontmatter; AgentCore auto-generates the Cedar **schema** from the gateway's tool definitions; Argo/Tekton take `serviceAccountName` from the template; SPIRE takes the SVID from attestation selectors; Cloudflare takes the budget from a rule. **Nobody derives all of them from one spec, because no shared spec exists.** The assembly is five ceilings with five authors and no consistency check between them.
2. **A join key.** Cost is enforced at the gateway, authority at the tool gateway, sequencing at the CI engine, identity at the IdP. There is no shared `(workflow, phase, role, run)` identifier that all four planes carry, so no single question — *"what was this role permitted to spend and do, at this phase, and why"* — is answerable from the assembly. This is the same defect `W0-a` named in family D (derived per-run units) reappearing across products instead of within one.
3. **Prospective context accountability.** Still nobody. Every product is retrospective. gh-aw's compiled `.lock.yml` is the closest thing shipping to a statement of what *will* be injected — and it states the tools and the permissions, not the resolved prompt or the exclusion rationale.
4. **Mid-run redirection into an LLM agent's live turn.** Temporal Signals deliver into a *workflow*; LangGraph interrupts *between* nodes; gh-aw admits nothing to a running agent job. Nothing changes what a model is doing without stopping it.

**Of these, (1) and (2) are the differentiating pair, and they are exactly the theme's thesis.** (3) and (4) are desirable and not differentiating — (3) is a diff of two files, (4) is a known-hard streaming problem that at least three vendors are pushing on.

### Routing recommendation (evidence, not a decision)

- **ADOPT — `gh-aw`, immediately, as the incumbent baseline to beat.** It is MIT, multi-engine, and covers seven concerns with real out-of-LLM mechanisms. **What we stop building:** the markdown-workflow compiler, the safe-outputs privilege-separation pattern, the egress firewall, the per-run hard budget, the compile-time permission derivation, and the `gh aw audit` introspection surface — all of which appear in wfh-004's 128 as candidate abilities. **This is the single most consequential line in this report:** any build-routed ability on that shortlist that `gh-aw` already implements must be re-routed before the wfh-004 gate is decided, and the burden is now on the ability to explain what it does that `gh-aw` does not.
- **ASSEMBLE — Temporal (durability + signals) · an MCP gateway or AgentCore Policy (per-call authority) · an AI gateway (hard budget) · SPIRE+Vault (credential minting) · OTel/Langfuse (introspection).** Uncovered part = items 1 and 2 above. **Yes, the uncovered part is the differentiating one.**
- **BUILD — one thing only: the derivation compiler and its join key.** The specific thing assembly cannot deliver is *a single declared workflow spec that emits, and keeps consistent, the ceilings of four independently-authored enforcement planes, carrying one identifier through all of them.* Note what this **is not**: it is not an enforcement plane. Every credible enforcement point above lives where the credential already lives (see cold leg, P6). The buildable object is a **compiler and an attestation**, not a runtime.
- **Consequence for wfh-004:** a 51-item build shortlist is not compatible with this evidence. The honest re-shape is roughly *adopt 20 / assemble 20 / build 5–10*, and the build set is one layer, not a harness.

---

## P3 — **WOUNDED**

*Position: inference anywhere on the enforcement path demotes a guarantee to a tendency.*

**Attack 1 — do vendors put a model on the enforcement path and still claim a hard guarantee?** They put the model there; **they do not claim the guarantee.** `gh-aw`'s **threat detection** runs the *same LLM engine* over the agent's buffered outputs before safe outputs are released, emitting `{prompt_injection, secret_leak, malicious_patch, reasons}`; on `true` the job fails and outputs are blocked; on a *warning* it downgrades to a `REQUEST_CHANGES` review requiring a human. GitHub's own text: *"Detection is advisory and should be combined with defense-in-depth controls… Do not treat a 'safe' result as a security guarantee. Use the output as one signal in a broader security review process."* Their docs publish **no false-positive/false-negative rates** and their troubleshooting section is titled "AI detection always fails." The independent PINT benchmark puts the whole classifier tier at **89–95%** detection `[secondary]`, and a published evasion study defeats six of them with homoglyphs, zero-width characters and diacritics. **P3's core claim is corroborated by the vendors themselves.** That is the strongest thing that happened to any position on this surface.

**Attack 2 — does anyone market determinism as the guarantee?** AWS does, verbatim, as a product benefit (quoted above). Cedar's design — default-deny, forbid-wins, schema validation, automated-reasoning analysis for always-allow/always-deny policies — is P3's thesis shipped and sold. Confirmation, not attack.

**Where it takes the wound — two narrowings P3 does not state:**

1. **The exemption surface, not the evaluation path, is where deployed guarantees die.** *Every* deterministic-enforcement product in this scan ships a first-class bypass because rollout without one fails: AgentCore Policy ships **`LOG_ONLY`** alongside `ENFORCE`; Gatekeeper ships **`dryrun`/`warn`** plus a `gatekeeper.sh/exempt: "true"` annotation that makes a resource skip policy entirely; Kyverno ships **`Audit`**; Cloudflare's spend limits are *"best-effort estimation"* and *"eventually consistent"*, so bursts overshoot. The received operational wisdom in the policy-as-code literature is the dryrun→warn→deny progression, because *"enforcing policies on day one breaks deploys and burns trust"* `[secondary]`. **This operation's two institutionalized bypasses are not our failure — they are the product norm, shipped as a feature.** The narrowing: *determinism makes a guarantee available; it does not make it durable. The durability property is "no exemption knob within the operator's reach," and no shipping product has it.*
2. **Authoring versus evaluation.** AgentCore ships natural-language → Cedar policy authoring: the model writes the policy, then the *deterministic* toolchain validates it against the auto-generated schema and runs automated reasoning for over-permissive/over-restrictive/unsatisfiable conditions before it can be enforced. That is a shipped, principled answer to *where a model may sit*: on the authoring path with a deterministic checker downstream, never on the evaluation path. This refines #185 (rule evaluation is queen-side) with its complement — **rule *authoring* is legitimately model-side iff the artifact is machine-checkable.** wfh-004's `inference-minimality` lens, as stated, does not distinguish these and would wrongly penalize the authoring case.

**Verdict: WOUNDED.** True as stated for the *evaluation* path, and unusually well corroborated there. Silent on the two places products actually lose the guarantee: the exemption knob and the authoring path. **Downstream:** the register's sort key is not wrong, but it is incomplete — "count of irreducible model calls" should be "count of irreducible model calls **on the evaluation path**, plus the size of the exemption surface."

---

## P2 — **WOUNDED; leg 3 FALSIFIED from this surface**

*Leg 1 — capability set derived from `(workflow, phase, agent-role)` is unclaimed.* **Partially present in products, and older than the theme.**
- **`(workflow, step) → identity`** ships in **Argo Workflows** and **Tekton**: `serviceAccountName` is set per template / per TaskRun, and via GKE Workload Identity that KSA maps to a cloud identity. This is per-step authority derived from the workflow definition, in production for years. Argo has a known defect where child-workflow pods inherit the parent's service account (#12642) — evidence the derivation is real and non-trivial.
- **`(workflow, phase) → credential`** ships in **GitHub Actions**: per-job `permissions:`, per-environment secrets plus deployment protection rules, and OIDC tokens whose claims carry *repository, branch, environment, actor and `job_workflow_ref`* — so a cloud trust policy can key a role on the phase.
- **`role`** appears only as a JWT tag on an AgentCore `OAuthUser` principal; **`phase` appears nowhere in any agent-authorization product I found.** AgentCore's entity model has exactly two principal types and no workflow/step/task entity.
- **Narrowing:** what is unclaimed is not "phase-indexed authority" — that ships — but **treating the triple as a single derived object with a consistency guarantee across planes**, rather than three independently hand-configured knobs on three products. Materially narrower than the claim as stated.

*Leg 2 — the gate-soundness rule (every gate-predicate input lies outside the exiting phase's write-set).* **Nothing on this surface, and I would not expect it here** — it is a static-analysis property, and no product I read performs any analysis over a gate predicate's data dependencies. Cedar's automated reasoning is the closest instrument and it analyses policy satisfiability, not phase write-sets. **Declared hole for the products surface**; this belongs to literature (W1) and adjacent prior art (W4), and I flag build systems as the likely alias.

*Leg 3 — deriving the over-granting ceiling from a declared spec rather than hand-writing it is unpublished.* **Falsified on this surface. Four independent instances:**
1. **`gh-aw`'s compiler** derives the GH Actions `permissions:` blocks of the downstream jobs from the declared `tools:`/`safe-outputs:` frontmatter. Issue **#18311** — `add-comment` generating `issues: write` but not `pull-requests: write` — is direct evidence the derivation is a real computation with real bugs, not marketing.
2. **AgentCore Policy** *"automatically generates a schema from the gateway's tool definitions, mapping each tool to an action and defining the expected input parameters"*, and validates every policy against it at creation time. The authorization vocabulary is derived from the tool spec (OpenAPI / Smithy / Lambda).
3. **Nix and Bazel** derive a build action's filesystem ceiling from its declared inputs and enforce it by sandbox — spec-derived least privilege, shipping, decades old. Named here because P2's own falsification hint says *"staged build systems."*
4. **MCP authorization** now specifies the *inverse* derivation: the server declares the scopes an operation needs in the `WWW-Authenticate` challenge and the client requests the union — least privilege driven by the resource's declared demand rather than a hand-written client policy.
5. *Different but adjacent:* **AWS IAM Access Analyzer** derives a least-privilege policy from CloudTrail **activity** — observation-derived, not spec-derived. Worth naming so the two are not conflated.

**Verdict: WOUNDED.** The absence claim fails on this surface for leg 3 and is materially narrowed on leg 1. What is left unclaimed is the *composite*: one spec deriving the ceiling across **multiple heterogeneous enforcement planes**, indexed by phase and role, with a cross-plane consistency check. **The moat is real but roughly a third the width it was asserted at, and it is an integration moat rather than a conceptual one.**

---

## P1 — **NEEDS-A-PROBE** (for the paper set) · the product/standards subset I could reach **checks out**

Not my surface for the ~30 papers — W1 owns that. What I can discharge:
- **MCP authorization specification: verified directly** against the normative page. It is real and says what the theme claims: MCP server = OAuth 2.1 **resource server**; **RFC 9728** Protected Resource Metadata **MUST**; **RFC 8707** Resource Indicators **MUST** in both authorization and token requests, with servers **MUST** validating audience and **MUST NOT** accepting or transiting other tokens; **RFC 9207** `iss` validation with an explicit acceptance table; a **step-up / scope-union** flow on `insufficient_scope`. **"Confused deputy" is named explicitly** in Security Considerations: *"covering token audience binding and validation, token theft, communication security, authorization code protection, mix-up and confused deputy attacks, open redirection…"*
- **Caveat I must state:** I fetched the `/specification/draft/` page. I did **not** verify a specific dated revision, so any citation of "the July 2026 revision" should be pinned to a dated URL by W1 or the leader before it is filed. The "July 28, 2026 revision / six requirements" framing came from a secondary blog, not the spec.
- **Cedar** is real, open-source, AWS-authored, and is the policy language of a GA AWS product — the spec-derived-capability-system claim has at least one verified product instance.
- **The one question a probe should answer:** are the ~30 references' **arXiv identifiers** resolvable and correctly attributed? A model asserting a bibliography in an unconstrained conversation is precisely the generation mode that fabricates identifiers, and recent arXiv IDs are the highest-risk subset. **What each answer decides:** all resolve → P1 SURVIVES and the other positions keep their footing; any fabrication → the whole owner-injected reference set is quarantined and P2's absence claim loses its supporting apparatus entirely.

---

## P5 — **WOUNDED**

*Position: the 128 abilities constitute a product requirement set, not a defect list.*

**What buyers demonstrably ask for** `[secondary — vendor/analyst surveys, not primary research; treat the numbers as directional]`:
- CSA Labs research note (2026-04-03): **92%** lack full visibility into AI agent identities · **95%** doubt they could detect or contain a compromised agent · **86% do not enforce access policies for AI identities** · only **16%** effectively govern AI access to core business systems.
- EY/AIUC-1 (Mar 2026, as quoted): only **38%** monitor AI traffic end-to-end across prompts, tool calls and outputs; **17%** monitor agent-to-agent interactions.
- Gartner named **"FinOps for Agentic AI"** a 2026 Hype Cycle category.
- Buyer-side demands hardening into procurement gates: kill switches, evidentiary audit trails, human-in-the-loop boundaries, model change control, ISO/IEC 42001 or SOC 2.
- Blockers to production: evaluation gaps **64%**, governance friction **57%**, model reliability **51%**.

**What that supports, and what it does not.** The demand is real, large, and independent of our incident log for exactly **three** of the eight concerns — **security (agent authority), introspection, cost**. Nothing in any buyer signal I found asks for **context-provisioning transparency**, **harness self-improvement**, or **phase-indexed capability derivation**. Two further mismatches the theme should not paper over:
1. **Wrong buyer.** These are CISO and platform-team demands about **enterprise agent fleets** — agent identity, containment, audit. The 128 were generated by a **solo operator's coding-agent friction**. Overlapping mechanisms, different purchaser, different budget line, different sales motion.
2. **A demonstrated commercial failure in the theme's own shape.** OpenAI announced deprecation of **Agent Builder** on 2026-06-03 (read-only 2026-10-31, shutdown 2026-11-30), together with the Evals platform, ~8 months after launch, steering users to a code SDK instead. The visual/authored agent-workflow-canvas category — wfh-004's family C, and half of what H1/H2 imagine — just failed at the top of the market. That is the single hardest external data point against the theme's product framing, and it is *not* explained away by "OpenAI deprecates things."

**Verdict: WOUNDED.** wfh-004's own triage was right that the register reads as a defect list; the external evidence rescues about three-eighths of it and is silent on the rest. **The narrowing:** demand is evidenced for *agent authority, observability and spend control*, aimed at platform/security buyers; it is unevidenced for the context-provisioning and self-improvement concerns, and there is a live negative for the canvas.

---

## Cold leg — assumptions nobody put on the list

Read cold: policy-as-code rollout practice, workload-identity architecture, build-system hermeticity, product deprecation notices, and vendor threat models. Three candidate sixth positions, in priority order.

### P6 (proposed) — **Enforcement is only severable where the harness is the sole credential path**

Every instance of *structural* enforcement in this entire scan lives in the plane that already holds the credential or the packet:
- `gh-aw` can enforce because it **compiles into GitHub's own permission system** — the agent job simply is not issued a write token; and because the **AWF containerizes the agent and forces all HTTP/HTTPS through a Squid proxy via iptables**, so egress is mediated by construction.
- AgentCore Policy can enforce because **all tool traffic must traverse its Gateway**.
- Copilot's coding agent can enforce (`#143`) because **GitHub owns branch protection**.
- Claude Code's managed settings can enforce because **MDM owns the binary's config precedence**.
- SPIRE/Vault can enforce because **they mint the credential**.

And note gh-aw's own trust model draws the boundary honestly in the other direction: *"The MCP gateway API key that is mounted into the agent container is not a strong security boundary against a compromised or malicious agent"* — the key is *"leaked by design."* Mediation works; possession does not.

**The unstated assumption:** that a *third-party* harness can enforce at all. It cannot, except over what it brokers. JURATI's enforcement is real precisely and only for the calls it mints or proxies — which makes **"the harness is the exclusive credential-minting and egress path"** a **hard architectural requirement**, not a design preference. The theme has never written it down. If it is not achievable in a given deployment, the harness's guarantees degrade to advice, and C-4 does not transfer.
**Consequence if adopted:** it reorders the register — sole-path mediation (proxy, credential broker, egress control) becomes a *prerequisite* ability rather than one candidate among 128, and any ability that presumes enforcement without it is infeasible as written, in the same way C-1 makes "the graph enforces X" infeasible.

### P7 (proposed) — **The build-once target is not stable enough to build once against**

H5/H6 assume a stable surface. Observed churn in a single scan: OpenAI deprecated Agent Builder **and** Evals eight months after launch; the MCP authorization spec is on a rolling revision cycle with a *"future revision is expected to upgrade… SHOULD to MUST"* note in the normative text; `gh-aw` shipped a billing bug spanning four releases and carries *"use it with caution, and at your own risk"*; `gh-aw` itself moved orgs. **A harness that owns the operating context absorbs 100% of that churn** — every engine's settings format, every MCP revision, every vendor's permission model. "Build once" is an assumption about the *world's* rate of change, not about our design, and the world's rate of change is currently quarterly.

### P8 (proposed) — **Anti-lock-in has already been commoditized, so it is not a moat**

H5 treats LLM-pluggability as an emergent asset of a portable representation. `gh-aw` ships **four engines** today under MIT, and the AI-gateway tier makes model substitution a base-URL change. Pluggability is table stakes. Worse, the theme's *own* value is now more exposed to **substrate** lock-in (GitHub Actions, AWS Gateway, Entra) than to model lock-in — and nothing in the theme's framing tracks that axis.

### One further flag, not yet a position

**The trusted-author assumption is load-bearing everywhere and is being broken by the field.** gh-aw's trust model has three layers and the middle one is *"Configuration trust: declarative specs and toolchains correctly instantiate components"* — i.e. **the workflow author is trusted**. This is also why `W0-a` family C ships zero security. But gh-aw *also* ships `gh aw mcp-server`, letting a scheduled meta-agent inspect, compile and optimize other workflows. **The self-improvement concern, implemented, hands the model write access to the artifact from which every enforcement ceiling is derived.** Nobody in this scan states who signs the workflow. If the derivation compiler of the P4 build is the whole moat, then *its input's integrity* is the whole moat, and no product I read has an answer.

---

## Suspected cross-surface aliases (flag, do not merge)

| Our name | Likely alias on another surface |
|---|---|
| phase-indexed capability derivation | *literature:* task-based / workflow authorization, workflow satisfiability · *adjacent:* per-stage service account (Argo/Tekton), hermetic sandbox derived from declared inputs (Bazel/Nix), staged deployment identity · *active-dev:* MCP **scope step-up** |
| gate soundness (inputs outside the exiting phase's write-set) | *literature:* non-interference, read/write-set disjointness, separation of duty · *adjacent:* build-system **hermeticity**, "no dependency on your own output" |
| safe outputs | *literature:* privilege separation, capability **attenuation** · *adjacent:* the broker/postMessage pattern, seL4-style capability passing |
| threat-detection job | *literature:* LLM-as-judge gate, checked output / verified generation, runtime monitor · *products:* guardrail classifier |
| Agent Workflow Firewall (container + iptables + proxy) | *literature:* **reference monitor**, complete mediation · *adjacent:* egress-only architectures, unikernel/jail |
| `max-ai-credits` hard budget | *literature:* resource-bounded computation, budget capability · *adjacent:* CPU/quota cgroups |
| derived over-granting ceiling | *products:* Cedar schema auto-generated from tool definitions · *adjacent:* IaC-generated IAM, IAM Access Analyzer (observation-derived — **do not merge**, different derivation source) |
| LOG_ONLY / dryrun / Audit mode | *literature:* the enforcement-adoption gap · *adjacent:* safety-critical **operational deviation permits** |

---

## Reuse/dedup notes (node ids)

- **Already held, do not re-file as new:** `#134` aider · `#135` Claude Code · `#137` OpenHands · `#139` Cursor · `#140` Windsurf · `#141` Devin · `#142` Replit · `#143` GitHub Copilot · `#144` Cline · `#145` Factory.ai · `#146` Amp · `#147` Cannoli · `#148` Rivet · `#149` LangGraph Studio · `#150` Dify · `#151` LangSmith · `#152–#155` observability tier · `#159` folded canvases · `#160` Temporal. This scan adds **fresh evidence** to `#160` (Signals as shipped mid-run intent injection — `W0-a` §5 flag 4(b) named it unverified; it is documented in Temporal's own HITL cookbook) and to `#135` (managed-settings precedence: admin policy developers cannot override; the permission-bypass flag removed from the CLI under policy).
- **`gh-aw` has no node.** It is on the theme's watchlist and was characterized in wfh-001's prose, but a `context_search` for it returns only `#143`. **This is a dedup gap, not a duplicate** — the theme's single nearest shipping instance is unrepresented in the graph while ten weaker tools are in it. Flagging for the curator; filing is post-triage and not mine.
- **Genuinely new to the graph** (all `claimed`, all doc-claim): Bedrock **AgentCore Policy/Gateway** · **Cedar** · **Entra Agent ID / Agent 365** · **Vertex Agent Engine agent identity** · **Cloudflare AI Gateway spend limits** (and the LiteLLM/Portkey/Kong tier) · the **MCP gateway tier** (Docker MCP Gateway, Obot, agentgateway, Pomerium) · **Arcade.dev** · **SPIFFE/SPIRE + Vault** · **Argo Workflows / Tekton per-task service account** · **OPA Gatekeeper / Kyverno enforcement modes** · **OpenAI AgentKit/Agent Builder (deprecating)**.
- **Corrections owed to held nodes** — three `W0-a` "nobody ships" verdicts are now contradicted on this surface: **cost enforcement** (gh-aw `max-ai-credits`; Cloudflare 429-on-budget), **self-improvement** (gh-aw meta-agent via `gh aw mcp-server`), **human steering / mid-run intent** (Temporal Signals). `W0-a` §5 flag 3 predicted exactly this. These are `Contradicts` candidates for the curator, not rewrites by me.

---

## cites:

```yaml
- type: repo
  ref: https://github.com/github/gh-aw
  title: "GitHub Agentic Workflows (gh-aw)"
  org: GitHub
  year: 2026
  surface: products
- type: docs
  ref: https://github.github.com/gh-aw/introduction/architecture/
  title: "Security Architecture | GitHub Agentic Workflows"
  org: GitHub
  year: 2026
  surface: products
- type: docs
  ref: https://github.github.com/gh-aw/reference/safe-outputs/
  title: "Safe Outputs | GitHub Agentic Workflows"
  org: GitHub
  year: 2026
  surface: products
- type: docs
  ref: https://github.github.com/gh-aw/reference/threat-detection/
  title: "Threat Detection | GitHub Agentic Workflows"
  org: GitHub
  year: 2026
  surface: products
- type: docs
  ref: https://github.github.com/gh-aw/reference/cost-management/
  title: "Cost Management | GitHub Agentic Workflows"
  org: GitHub
  year: 2026
  surface: products
- type: docs
  ref: https://github.github.io/gh-aw-firewall/
  title: "Agentic Workflow Firewall (AWF)"
  org: GitHub
  year: 2026
  surface: products
- type: repo
  ref: https://github.com/github/gh-aw/issues/18311
  title: "gh aw compile does not add pull-requests: write to safe_outputs job when add-comment is configured"
  org: GitHub
  year: 2026
  surface: products
- type: repo
  ref: https://github.com/github/gh-aw/issues/23198
  title: "Feature: allow restricting Copilot CLI built-in tools via frontmatter"
  org: GitHub
  year: 2026
  surface: products
- type: docs
  ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html
  title: "Policy in Amazon Bedrock AgentCore: Control Agent Interactions"
  org: Amazon Web Services
  year: 2026
  surface: products
- type: docs
  ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html
  title: "Policy in AgentCore — Core concepts (Cedar principals, schema, analysis)"
  org: Amazon Web Services
  year: 2026
  surface: products
- type: product
  ref: https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-bedrock-agentcore-policy-evaluations-preview
  title: "Amazon Bedrock AgentCore now includes Policy (preview), Evaluations (preview) and more"
  org: Amazon Web Services
  year: 2025
  surface: products
- type: standard
  ref: https://modelcontextprotocol.io/specification/draft/basic/authorization
  title: "Model Context Protocol — Authorization (draft)"
  org: Model Context Protocol
  year: 2026
  surface: products
- type: docs
  ref: https://learn.microsoft.com/en-us/security/zero-trust/sfi/least-privilege-for-ai-agents
  title: "Least privilege for AI agents with Microsoft Entra Agent ID"
  org: Microsoft
  year: 2026
  surface: products
- type: docs
  ref: https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview
  title: "Governing Agent Identities — Microsoft Entra ID Governance"
  org: Microsoft
  year: 2026
  surface: products
- type: docs
  ref: https://cloud.google.com/agent-builder/agent-engine/agent-identity
  title: "Use agent identity with Vertex AI Agent Engine"
  org: Google Cloud
  year: 2026
  surface: products
- type: docs
  ref: https://developers.cloudflare.com/ai-gateway/features/spend-limits/
  title: "Spend limits — Cloudflare AI Gateway"
  org: Cloudflare
  year: 2026
  surface: products
- type: docs
  ref: https://docs.temporal.io/ai-cookbook/human-in-the-loop-python
  title: "Human-in-the-Loop AI Agent — Temporal Platform Documentation"
  org: Temporal Technologies
  year: 2026
  surface: products
- type: product
  ref: https://temporal.io/solutions/ai
  title: "AI Applications & Agents With Temporal"
  org: Temporal Technologies
  year: 2026
  surface: products
- type: docs
  ref: https://developers.openai.com/api/docs/deprecations
  title: "Deprecations | OpenAI API (Agent Builder and Evals, shutdown 2026-11-30)"
  org: OpenAI
  year: 2026
  surface: products
- type: product
  ref: https://openai.com/index/introducing-agentkit/
  title: "Introducing AgentKit"
  org: OpenAI
  year: 2025
  surface: products
- type: docs
  ref: https://code.claude.com/docs/en/settings
  title: "Claude Code settings — managed policy precedence"
  org: Anthropic
  year: 2026
  surface: products
- type: docs
  ref: https://spiffe.io/docs/latest/keyless/vault/readme/
  title: "Using SPIRE and OIDC to Authenticate Workloads to Retrieve Vault Secrets"
  org: SPIFFE
  year: 2026
  surface: products
- type: docs
  ref: https://argo-workflows.readthedocs.io/en/latest/service-accounts/
  title: "Service Accounts — Argo Workflows"
  org: Argo Project / CNCF
  year: 2026
  surface: products
- type: repo
  ref: https://github.com/argoproj/argo-workflows/issues/12642
  title: "Step has Parent WorkflowTemplate's service account instead of its own"
  org: Argo Project
  year: 2026
  surface: products
- type: docs
  ref: https://tekton.dev/docs/pipelines/taskruns/
  title: "TaskRuns — serviceAccountName per task"
  org: Tekton / CD Foundation
  year: 2026
  surface: products
- type: docs
  ref: https://aws.amazon.com/iam/access-analyzer/
  title: "IAM Access Analyzer — policy generation from access activity"
  org: Amazon Web Services
  year: 2026
  surface: products
- type: docs
  ref: https://bazel.build/docs/sandboxing
  title: "Sandboxing — Bazel (action inputs derive the sandbox)"
  org: Bazel / Google
  year: 2026
  surface: products
- type: repo
  ref: https://github.com/lakeraai/pint-benchmark
  title: "PINT — a benchmark for prompt injection detection systems"
  org: Lakera AI
  year: 2026
  surface: products
- type: paper
  ref: arXiv:2504.11168
  title: "Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems"
  year: 2025
  surface: products
- type: blog
  ref: https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-agent-governance-framework-gap-20260403/
  title: "CSA Research Note — The AI Agent Governance Framework Gap"
  org: Cloud Security Alliance
  year: 2026
  surface: products
- type: docs
  ref: https://docs.arcade.dev/en/home/auth/auth-tool-calling
  title: "Authorized Tool Calling — Arcade.dev"
  org: Arcade.dev
  year: 2026
  surface: products
- type: blog
  ref: https://obot.ai/blog/the-13-best-mcp-gateways-for-enterprise-teams/
  title: "The 13 Best MCP Gateways for Enterprise Teams in 2026 (vendor-authored comparison)"
  org: Obot AI
  year: 2026
  surface: products
```

---

## Compact return

| Find | In-lens | New/known | Buy-before-build evidence present? |
|---|---|---|---|
| `gh-aw` (github org, MIT, 7/8 concerns) | in | **known-but-unfiled** (watchlist only; no node) | **yes** — scope-vs-need, cost, lock-in, composability |
| Bedrock AgentCore Policy + Gateway (Cedar, GA 2026-03) | in | new | yes (pricing partial — could not verify per-call charge) |
| Temporal (Signals = mid-run intent; durable resume) | in | known `#160` — **fresh evidence** | yes |
| AI-gateway tier (Cloudflare 429-on-budget, LiteLLM, Portkey, Kong) | in | new | yes |
| MCP gateway tier (Docker, Obot, agentgateway, Pomerium) | in | new | partial (vendor-authored comparisons only) |
| SPIFFE/SPIRE + Vault (per-job credential minting) | in | new | yes |
| Entra Agent ID / Agent 365 · Vertex agent identity | in | new | partial (pricing unverifiable) |
| Argo / Tekton per-task service account | in | new | yes |
| OPA Gatekeeper / Kyverno enforcement + exemption modes | in | new | yes (P3 evidence, not a P4 candidate) |
| Claude Code managed settings | in | known `#135` — fresh evidence | yes |
| OpenAI AgentKit / Agent Builder (deprecating 2026-11-30) | in | new | yes (as a lock-in/exit and demand datum) |

**Verdicts:** P4 **WOUNDED** (route **ADOPT `gh-aw` + ASSEMBLE + narrow BUILD**) · P3 **WOUNDED** · P2 **WOUNDED** (leg 3 falsified, leg 2 a declared hole for this surface) · P1 **NEEDS-A-PROBE** (products/standards subset verified) · P5 **WOUNDED**.

**Flags for the leader:**
1. **`gh-aw` must be re-characterized before the wfh-004 gate is read.** wfh-001's picture of it is a year stale and materially understates it; three `W0-a` "nobody ships" cells are contradicted by it.
2. **Cold-leg P6 is the highest-value item in this file** — sole-credential-path mediation is an unstated architectural requirement, not a preference.
3. **Declared hole:** commercial CD platforms' stage-scoped RBAC (Harness/Spinnaker/Azure DevOps) — products surface failed to see it, cheap to close in round two.
4. **Theme-revision signal (to the owner, verbatim):** *the theme's build framing and its anti-lock-in value-target are both aimed at axes the market has already commoditized (engine pluggability) while ignoring the axis that is actually tightening (substrate lock-in to the credential-holding plane). If the theme is reshaped, reshape it around "the derivation compiler and the sole-path attestation," not around "the harness."*
