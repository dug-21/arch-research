# scout-active-dev.md — wfh-005 challenge scan, active-development surface

**Run:** `wfh-005` · Issue #54 · **CHALLENGE mode** · surface **W3 active development** · `agent_id: wfh-005-scout-active-dev` · read-only, zero graph writes.
**Discipline applied throughout:** maturity ≠ ambition. A README, a roadmap, or "code will be released soon" is **ambition**. A merged compiler, a shipped release train, a spec that reached RC, an open bug with a reproduction, a plugin in public preview — that is **maturity**. No star count is offered as evidence anywhere below.
**Honest bound:** exhaustion here is relative to the five named positions and this one surface, over roughly the last 12 months. It is not absolute.

---

## Surface coverage report

**Searched (warm):** `github/gh-aw` repo + docs site (architecture, threat-detection, network, safe-outputs) + its blog and the 2026-02-13 changelog · `github/gh-aw-firewall` · `github/gh-aw-threat-detection` · gh-aw issue tracker and discussions · MCP specification blog (2026-07-28 RC and release notes) + community critique of its authorization scope · Claude Agent SDK / Claude Code permission + hooks documentation · `anthropics/claude-agent-sdk-typescript` issue tracker · this repo's own `.claude/settings.json` and `.claude/agents/factory/*.md` (dogfood-signal).

**Searched (cold, outside the watchlist):** agentic-workflow compilers and policy compilers (PCAS, SPL, cross-layer policy compilation, Oracle Open Agent Specification, CNCF Serverless Workflow, `salesforce/agentscript`) · agent-framework gate/approval models (OpenAI Agents SDK guardrails+approvals, Google ADK 1.0 GA, LangGraph interrupts, AWS Strands, `microsoft/agent-framework`) · durable-execution-for-agents (Temporal plugin line) · sandbox layer (E2B/Firecracker, Modal/gVisor, Daytona, Fly Machines, Dagger `container-use`) · MCP gateway category (Docker MCP Gateway, Lunar MCPX, IBM ContextForge) · GitHub Actions OIDC subject claims and per-job permissions · Bazel/Nix hermetic sandboxing · in-toto/SLSA step attestation · Cedar/OPA policy generation and AWS Bedrock AgentCore Policy · the 2026 agent-over-privilege paper cluster and its repos · the emerging "harness engineering" literature.

**Deliberately skipped, with reasons:**
- **Commercial pricing, ARR, adoption figures** — the products surface (W2) owns cost/licence/lock-in evidence; duplicating it here would produce unverified secondary numbers, which wfh-001 already poisoned once (W0-a flag 6).
- **Closed-source hosted agents (Devin, Cursor, Windsurf, Replit)** — no observable development surface; nothing but vendor docs, which is W2's material, not mine.
- **The full ~30-item P1 reference list** — **declared hole.** It lives in an owner conversation attached to Issue #48; I read #48's body and comments and the list is not there. I could not obtain it, so I could not check per-reference artifact existence. See P1.
- **Chinese/Japanese-language agent-framework ecosystems** — not searched; a real hole on a high-churn surface.

---

## Warm-leg deltas

### 1. GitHub Agentic Workflows (`gh-aw`) — last looked 2026-07-22 (wfh-001). Re-check when *"it gains multi-phase workflows or per-phase roles."*

> **The condition fired. Both halves. It fired roughly six months ago and nobody looked.**

**What actually moved, dated:**
- **2026-01-13** — multi-phase workflows shipped as a documented, installable pattern ("Daily Perf Improver": research → setup → implement, state carried across days via `repo-memory`). Working examples live in `githubnext/agentics`.
- **2026-02-13** — entered **technical preview** via the GitHub changelog. Not GA. Version series is `0.x` (0.68–0.77+), with 0.68.4–0.71.3 retired for a billing bug — *a real release train with real regressions*, not a demo.
- **Collaboration:** GitHub Next + Microsoft Research + Azure Core Upstream. MIT. ~15.6k commits on main; issue numbers in the **29,000 range**; automated "Safe Output Health Report" discussions run on a cadence. Velocity is the highest of anything on this surface, by a wide margin.
- **A compiler exists.** `gh aw compile` turns a markdown workflow into a `.lock.yml` GitHub Actions artifact, gated by schema validation, expression allowlisting, action pinning, and three external scanners (actionlint, zizmor, poutine). **The enforcement is in the compiled artifact and in GitHub Actions — a plane the agent holds no credentials for.**
- **Per-phase role/permission binding exists,** over a fixed three-stage pipeline: *agent phase* (read-only token, MCP tools from an explicit `allowed:` list, all writes buffered to artifacts) → *detection phase* (artifacts only, no external access, no writes) → *safe-output phase* (deterministic writes, **each safe output in its own job holding exactly one permission**, e.g. `issues: write`).
- **`gh-aw-firewall` (AWF)** — the agent container is bound to a Docker network, HTTP/HTTPS redirected by iptables through a Squid proxy on a domain allowlist. Default is `network: defaults`. Egress control is shipped, deterministic, and outside the model.
- **MCP Gateway** — spawns isolated MCP server containers with per-server tool filtering and env-var injection.

**The precise scope-versus-need gap** (this is the field that matters, and it is easy to get wrong): gh-aw's per-phase tool binding is over **its own fixed security pipeline** (agent / detect / write), **not over the workflow author's declared phases**. The multi-phase improver's research/setup/implement stages are *prompt structure plus repo-memory*, not three separately-authorized principals. **Nothing in gh-aw derives a capability set from `(workflow, phase, agent-role)` as the author declared it.** That is the uncovered remainder, and it is exactly the load-bearing part.

**Second gap:** engine-plurality is invocation-level. Copilot, Claude, Codex and Gemini all run behind the same AWF/safe-outputs plane — which is genuinely build-once — but the *guarantee* comes from GitHub Actions, so "any-LLM" is bought with "only-GitHub."

### 2. MCP authorization specification — last looked 2026-07-22. Re-check when *"scope granularity changes, or a derived-permission path appears."*

**Delta: the spec moved a lot and the re-check condition did NOT fire.**
- **2026-05-21** release candidate; **2026-07-28** final — described as the largest revision since launch. Six authorization SEPs landed: `iss` validation per RFC 9207 (mix-up defence), OIDC `application_type` at Dynamic Client Registration, credential-to-issuer binding with re-registration on resource migration, refresh-token retrieval documentation (SEP-2207), **scope accumulation during step-up authorization (SEP-2350)**, and a standardized `.well-known` discovery suffix. Resource Indicators (RFC 8707) are mandatory for clients.
- **What did not happen:** no per-tool scope, no derived-permission path, no scope-granularity change in the direction we care about. Everything that moved is **authentication hardening and OAuth conformance**. Independent critique states it plainly: the spec tells a server *which client is calling and which issuer vouched for it*, and never specifies *what that tool is allowed to do once authenticated*; authorization remains "beyond the scope of this specification."
- Rich Authorization Requests remain a community discussion item, not a SEP that landed. The 2026-07-28 Extensions framework is a generic escape valve, explicitly trading interoperability for flexibility.

**Verdict on the entry:** the standards body has decided authorization granularity is an implementer problem. **That is a durable structural gap and it is not closing on the spec's timeline.** Re-check condition should be tightened to "a SEP proposing per-tool or per-resource scopes is opened," because "the spec changed" will otherwise keep firing on auth work that is irrelevant to us.

### 3. Coding-agent permission and hook models (this harness included) — **last looked: never.** Re-check when *"a per-agent tool binding becomes enforceable rather than advisory."*

**This one was directly checkable and the answer is: partially, with a documented hole and an open bug.**

Enforceable today (Claude Agent SDK / Claude Code, per vendor docs):
- **Deny rules beat everything**, including the permission-bypass mode. A **bare-name deny (`Bash`, `mcp__*`, `*`) removes the tool definition from the request entirely** — the model never sees it. That is structural incapacity, not a gradient. It is the strongest per-agent binding shipped in this class.
- **Hooks run first** and a `PreToolUse` deny applies in every mode.
- `permissionMode: "dontAsk"` + `allowedTools` gives a hard-deny default.

Advisory or broken:
- **`AgentDefinition.tools` / `disallowedTools` are documented as constraining a subagent and are not enforced when the CLI spawns subagent child processes** — `anthropics/claude-agent-sdk-typescript` **issue #172, opened 2026-02-12, still open**. The SDK passes the flags; the CLI's `Task` handler does not map them. Observed consequence: recursive `Task` chains and a crash. The published workaround is a hand-written `PreToolUse` hook. *(Unverified: whether file-based `.claude/agents/*.md` frontmatter follows the same broken path as the programmatic `AgentDefinition`. I could not establish this and will not guess.)*
- **Subagents inherit the parent's permission mode and cannot override it.** A loosely-permissioned parent silently grants every child the same access.
- **`allowed_tools` does not constrain the permission-bypass mode** — vendor's own warning.
- **Auto-approved tools never reach `canUseTool`** — vendor's own warning: "permission checks you put there are silently bypassed for that tool."

**Dogfood-signal, this repo, verified by inspection:** `.claude/agents/factory/*.md` carry **no `tools:` frontmatter at all** — curator, scout, researcher, goal-owner all resolve to the full tool set. The single-writer firewall ("only the curator writes nodes") and the scout's read-only constraint are **prose in an agent definition**, enforceable by nothing. `.claude/settings.json` contains **hooks only** (Unimatrix telemetry), **zero permission rules**. This is #179/#181 confirmed live, and it sharpens the picture: the field's *strongest available* per-agent binding is sitting unused in the repo that wrote the position paper about needing it.

**Verdict on the entry:** the re-check condition has **half-fired**. Set it to "issue #172 closes, or subagent permission-mode inheritance becomes overridable."

---

## P4 — **WOUNDED, severely** · verdict **ASSEMBLE** · **the window is closing, ~6–12 months**

The assertion under test — *nothing shipping or assemblable covers this* — was never stated and never tested. From this surface it does not survive intact. A large fraction of the eight concerns is now covered by shipping code, and the parts that are covered are covered by **the exact architecture the theme proposes** (compile a declared workflow into an enforcement plane the LLM has no credentials for).

### Per-find: what works TODAY vs announced

| Find | Works today | Announced / aspirational | Velocity & who |
|---|---|---|---|
| **`github/gh-aw`** (repo, MIT) | markdown→Actions compiler with 3 external scanners; read-only agent token; per-safe-output single-permission jobs; AWF egress firewall (iptables+Squid, domain allowlist); MCP Gateway with per-server tool allowlists; secret redaction; multi-phase workflows with `repo-memory`; human approval gates; role/permission pre-activation checks | GA (still technical preview since 2026-02-13); per-**author-declared**-phase roles | Extreme. ~15.6k commits, 0.x release train with a retired-for-billing-bug series, issue #29k+, automated health reports. GitHub Next + MSR + Azure Core Upstream |
| **Claude Agent SDK / Claude Code** (docs, Anthropic) | 6 permission modes; hook-first evaluation; deny rules that survive bypass; **tool-definition removal**; scoped path rules; `dontAsk`; dynamic mid-session mode change | per-agent `tools` enforcement (**documented but broken**, #172 open) | Continuous; version-pinned behaviours documented to the patch (`v2.1.198`, `v2.1.212`) |
| **Temporal agent plugins** (blog, 2026-07-16) | LangGraph plugin in **public preview** — durable execution, crash recovery, free HITL waits via signals/timers, LangSmith trace propagation across workflow/activity boundaries. Same line already covers OpenAI Agents SDK, Google ADK, AWS Strands | GA | Steady, vendor-backed |
| **MCP gateway category** (Lunar MCPX, IBM ContextForge, Docker MCP Gateway) | centralized proxy; MCPX ships **Tool Groups — tool subsets per team, workflow, or agent** | org-wide policy on Docker's (explicitly not multi-tenant governance) | Active, crowded |
| **Sandbox layer** (E2B/Firecracker, Modal/gVisor, Daytona, Fly Machines, Dagger `container-use`) | kernel-level isolation, per-agent containerized git worktrees | — | Commoditized; four+ funded vendors |
| **`majiayu000/harness`** (repo, MIT, Rust, **individual** maintainer) | Rust control plane over Claude Code + Codex CLI; **Starlark policy engine evaluated outside the LLM** (hardened parser: no `load`/`def`/`lambda`); per-phase and per-agent policy; isolated git worktrees with 3 sandbox modes; cross-agent review (no self-review); OTel; REST API failing closed; embedded dashboard; TOML config with project overrides | GA, org backing | Beta; ~1.6k commits, 44 open issues, CI + integration tests. **Single maintainer — bus factor 1** |
| **PCAS** (paper 2602.16708) | *nothing public* — "code will be released soon" | Datalog reference monitor over a causal dependency graph, deterministic, compiled to Rust via DDlog | UW–Madison + Langroid (+ Google per secondary). **Ambition, not maturity** |

### Coverage of the eight concerns — best shipping composition

| Concern | Covered by | Grade |
|---|---|---|
| **Structure** | gh-aw compiler (`.md` → `.lock.yml`, versioned, in-repo) | **Strong** |
| **Context provisioning** | markdown workflow + `repo-memory`; MCP Gateway env injection | Adequate; still no *pre*-injection statement of what/why |
| **Security** | gh-aw read-only token + single-permission write jobs + AWF egress + MCP tool allowlist; Claude deny-rules/tool-removal; sandbox layer | **Strong — except role×author-declared-phase** |
| **Introspection** | Actions logs; OTel; LangSmith trace propagation | **Strong (commoditized)**; still no causal account |
| **Cost transparency & management** | metering everywhere | **Weak — enforcement still absent.** Practitioner consensus: iteration caps are "a crash barrier, not a smoke alarm"; the cap fires after the spend |
| **Self-improvement** | gh-aw's automated Safe Output Health Reports are the closest thing seen | **Weak** |
| **Recovery & durability** | **Temporal plugin line — this is now SHIPPED.** wfh-004's "nobody connected durable execution to agents" is **out of date** | **Solved as a mechanism** |
| **Human steering** | gh-aw approval gates; Actions `environment` protection rules; LangGraph interrupt + Temporal durable waits | Adequate for approve/deny; redirection still absent |

### My read

**ASSEMBLE.** `gh-aw` (structure + compiled enforcement) + Temporal-class durable execution + an MCP gateway with per-agent tool groups + a sandbox layer covers roughly **six of eight concerns at a quality no reasonable build reaches quickly**.

**The uncovered part, named precisely — and yes, it is the differentiating one:**
> **A capability set derived from the workflow author's own declared `(workflow, phase, agent-role)` triple, compiled into whichever enforcement plane the run targets, with the gate predicates checked for independence from the exiting phase's write-set.**

Everything shipped derives permissions from *the tool's or the platform's* fixed stages (gh-aw's agent/detect/write; Actions' job/environment). Nobody derives them from *the author's* phases. That is the ~20% remainder, and the eighty-percent case is doing exactly what the standard warns about: it looks like coverage.

**What assembly cannot deliver (the build burden, if the owner routes that way):** portability of the *enforcement* across planes. gh-aw's guarantee is GitHub Actions; Claude's is the CLI runtime; MCPX's is the proxy. An any-LLM/any-plane harness has to compile one declared authority model down to several dissimilar enforcement substrates and *tell you honestly which guarantees survived the compilation*. Nothing shipping attempts that, and it is the only part that is genuinely both hard and unclaimed.

**Window-closing call: yes, closing, ~6–12 months.** Three independent signals: (a) gh-aw is at GitHub's velocity with three orgs behind it and has already absorbed compiler, firewall, gateway, and per-phase binding — the remainder is one design decision away; (b) "agent harness engineering" became a **named field** in the last year, with awesome-lists, a coined term, and Addy Osmani's observation that competing harnesses "look more like each other than their underlying models do" — convergence is the danger sign; (c) the demand is showing up as *feature requests on incumbents' trackers* (below), which is how a gap gets closed by the incumbent rather than by a new entrant.

---

## P2 — **WOUNDED (badly), one sub-claim survives**

**Sub-claim (i) — deriving a capability set from `(workflow, phase, agent-role)` is unclaimed: FALSIFIED in the weak form, WOUNDED in the strong form.**
- **GitHub Actions OIDC** issues a token whose `sub` claim carries `job_workflow_ref` (the reusable workflow actually executing) and `environment` — and **GitHub only includes `environment` in the claim once that environment's protection rules are satisfied**. The cloud trust policy then keys the assumable role off that claim. That is a shipped, mass-deployed, deterministic pipeline from *(which workflow, which stage, has the gate passed)* to *what capabilities you hold*, enforced by a plane the job cannot forge. Immutable subject claims became default for repos created on/after **2026-07-15**. Whatever else this is, it is not unclaimed.
- **gh-aw** puts each safe output in its own job with exactly one permission — per-stage capability derivation, shipped.
- **Lunar MCPX Tool Groups** — "tool subsets per team, workflow, or agent."
- **AWS Bedrock AgentCore Policy + Cedar** — the gateway injects the OpenAPI `operationId` as `context.toolName` at runtime and evaluates deny-by-default Cedar policies over multi-agent chains.
- **The strong form that survives:** none of these derive from *phase* as an author-declared, first-class workflow construct. Actions' `environment` is the nearest and it is a deployment target, not a phase; gh-aw's stages are the tool's, not the author's. **Narrowing to carry forward:** the claim must be restated as *"deriving from an author-declared phase in a portable workflow definition"* — and stated that way it is thin novelty resting on a construct nobody else has, not on a derivation nobody else does.

**Sub-claim (ii) — the gate-soundness rule (*every input to a gate predicate lies outside the write-set of the phase being exited*): SURVIVES on this surface. Legible negative below.**
- **Searched:** Bazel sandboxing docs and issue tracker, Nix hermeticity, Bazel+Nix integration writeups, in-toto layouts and artifact rules, SLSA provenance and `slsa-verifier`, Earthly/Dagger, staged-pipeline design writeups.
- **What I expected to find and did not:** a build system or attestation framework that states, as a *rule*, that a verification predicate must not read anything the verified step produced. **What exists instead is the adjacent-but-different thing:** Bazel enforces *declared* read-sets and write-sets (actions cannot use undeclared inputs or create unknown outputs) — a hermeticity property, not an independence property. in-toto layouts name authorized actors per step and `MATCH` rules *link* one step's products to the next step's materials — the opposite direction from exclusion. SLSA's separation is "the build service, not the builder, generates provenance," which is the same *intuition* but scoped to provenance generation, not to gate predicates generally.
- **Caveat, honestly:** this is the sub-claim most likely to exist unnamed in formal literature (information-flow / non-interference) rather than in code. **W1 and W4 own that; from active development I found no implementation.**

**Sub-claim (iii) — deriving the over-granting ceiling from a spec's declared demands rather than hand-writing it: FALSIFIED.**
- **`gh aw compile` does precisely this.** The author declares `safe-outputs: create-issue`; the compiler emits a job holding `issues: write` and nothing else. The permission ceiling is *computed from declared demand*, and hand-writing it is not an option the format offers.
- Reinforcing: AgentCore's Cedar `toolName` context is derived from the OpenAPI schema, not hand-mapped.
- **Counter-counter (in our favour, narrowly):** gh-aw derives from a *fixed enumeration* of safe-output types, not from an open spec. And I found **no** tool that automatically synthesizes Cedar/OPA policy from an arbitrary manifest — the AWS material shows schema-derived *context*, hand-written *policy*. PCAS states outright: *"We do not address automatic synthesis of formal policies from natural language policy documents in this work."* So "derive the ceiling from a closed enumeration" is shipped; "derive it from an open declaration" is not.

**Overall P2: WOUNDED.** Two of three sub-claims have shipping counter-examples. The residual novelty is narrow and specific — *author-declared phases* and *gate-predicate independence* — and it should be restated in those terms before anything is built on it.

---

## P3 — **WOUNDED. The narrowing is important and cuts both ways.**

**The counter-case is live, shipped, and by the vendors themselves. Inference is on the enforcement path in production, twice:**
1. **Claude Code `auto` permission mode (shipped since ~March 2026).** A **model classifier** approves or denies permission prompts, clearing the ~93% of prompts users approve anyway and escalating to a human after 3 consecutive or 20 total denials. It is documented as a permission *mode* — it sits inside the six-step evaluation flow, alongside the bypass mode. It was introduced explicitly as the safer replacement for the permission-bypass flag.
2. **gh-aw threat detection.** A job running "the same AI engine as your main workflow, but with a security-focused system prompt" scans buffered outputs and patches for prompt injection, secret leaks, and malicious patches. **If it fails, every downstream safe-output write job is skipped.** A model call is a hard blocking gate on write.

**But the narrowing that saves the thesis is structural, and every one of these systems respects it:** in **no** case is inference the *sole* thing standing between the agent and the capability. Claude's `auto` sits *after* hooks and deny rules, which it cannot override, and *before* nothing that matters — the tool-definition-removal deny is still absolute. gh-aw's detector runs *inside* a pipeline where the agent already holds a read-only token, has no secrets, sits behind an egress firewall, and cannot write at all; the detector only decides whether an already-buffered, already-powerless artifact gets handed to a deterministic single-permission writer. **The shipped pattern is exactly proposal-then-deterministic-check: inference narrows or vetoes within an envelope that determinism has already made safe. Nobody ships inference as the envelope.**

**The vendors decline the word "guarantee" for the model layer.** gh-aw's own docs call threat detection "an additional security layer" and offer no completeness claim; the troubleshooting section acknowledges false positives with no rate ("refine prompt with specific exclusions, adjust tool thresholds").

**Evidence that deterministic enforcement gets bypassed in practice — the open-source version of our own story, and it is strong:**
- **`github/gh-aw` issue #29171** — *"allow `safe-outputs.threat-detection` to be controlled by `workflow_call` inputs."* Verbatim shape: threat-detection is compile-time and won't take `${{ inputs.enable-threat-detection }}`, so a reusable workflow "cannot expose a simple input that lets callers select stricter or lighter-weight safe-output handling at runtime." **That is an institutionalized bypass being requested, on the ticket, with a business justification.**
- `threat-detection: false` and `engine: false` are **already documented, supported ways to turn the model gate off.** The escape hatch shipped with the feature.
- **False rejects are documented in practice:** when the detection job errors for infrastructure reasons the condition `needs.detection.result == 'success'` evaluates false and **valid agent outputs are blocked** — the gate fails closed onto correct work, which is precisely the pressure that produces #29171.
- **The permission-bypass mode.** Widely used, community-nicknamed "YOLO mode," with a documented destructive incident (an `rm -rf` from `/`). The stated reason is friction: "dozens of prompts… most developers just spam yes anyway, which defeats the purpose." Anthropic's response was not to harden the deterministic gate — it was to **put a model classifier on the path** to remove the friction that caused the bypass.

**The narrowing to carry:** *inference on the enforcement path demotes a guarantee to a tendency* is **true and unchallenged**. What is false is the operational corollary the theme has been running on — that minimizing inference is therefore the right global objective. The shipped evidence says the binding constraint is **friction**, not inference: a deterministic gate with high friction gets an escape hatch built for it, and then the guarantee is zero. **Inference is being used, deliberately, as a friction reducer inside a deterministic envelope, in order to keep the deterministic envelope switched on.** That is a design pattern the theme has no position on, and it is the one the field converged to.

---

## P5 — **SURVIVES, with the ranking wounded**

Issue trackers are the honest record. The wfh-004 register's failure modes are demonstrably **other people's problems** — but they are not weighted the way our register weights them.

**Confirmed as other people's problems, with artifacts:**
- **Per-tool authorization (agents exceeding permissions).** `openai/openai-agents-python` **#2868**, *"Per-tool authorization middleware for agent tool calls"* (2026-04-09, closed as enhancement request). Its gap statement is the cleanest external articulation of our position I found: **"Guardrails check content. Authorization checks permission. Both are needed but they solve different problems."** It asks for identity/scope/rate-limit/session-context evaluation with ALLOW/DENY/MODIFY/DEFER/STEP_UP and structured audit records. Sibling: **#2775**, *"Runtime governance guardrails."* Reinforced by the whole 2026 measurement cluster (FORTIS: over-privileged behaviour "the norm rather than the exception" across ten frontier models; SkillScope's 68,312-bundle measurement).
- **Recovery / lost context / unrecoverable runs.** `microsoft/agent-framework` discussion **#1092**; `strands-agents/sdk-python` **#1138**; a public critique titled *"Still Not Durable: MS Agent Framework & Strands."* The named mechanism is exact and matches ours: the **atomicity gap** — crash after the step, before the checkpoint flush, and the agent restarts mid-sequence with steps 1–4 in context and no knowledge it was mid-execution, so it repeats, skips, or diverges. **Maintainers fixed this by adopting Temporal**, not by inventing checkpointing.
- **Runaway cost.** Widely reported across LangGraph/CrewAI/AutoGen; the recurring formulation is that iteration caps are "a crash barrier, not a smoke alarm" — the cap fires after the money is gone. **No framework ships pre-authorized spend per unit of work.** This one matches our register almost exactly.
- **Enforcement friction and bypass.** gh-aw #29171; the YOLO-mode phenomenon.

**Where the field's problems are NOT ours — the honest falsification pressure:**
- **Introspection barely registers as a complaint.** LangSmith/Langfuse/OTel/Temporal-trace-propagation is commoditized and people are satisfied with it. Our register treats introspection as a major gap (12 pains). Read from the outside, **most of what we call an introspection gap is a structure gap wearing introspection's clothes** — which W0-e already argued from a different direction.
- **"No way to steer mid-run" is close to absent** from external trackers. People ask for durable *waits* and approval, not redirection. Redirection may be a genuine white space, or it may be a want nobody has.
- **"No introspection into what an agent did" appears mostly as a cost/tracing question**, not an authority-audit question. The demand for *authorization audit records* exists (#2868 asks for it) but is much quieter than the demand for durability.

**Verdict:** the demand is real — three of six failure modes are actively-filed issues on major trackers, one of them with a verbatim match to our framing. But **the ordering is wrong**: the field's loudest demands are **durability** (which is now solved by adoption, not by us) and **per-tool authorization** (which is genuinely open). Cost enforcement is a real, quiet, unmet demand. Introspection and mid-run steering are ours more than theirs. P5 survives; the register's *priority order* should be rebuilt against this.

---

## P1 — **NEEDS-A-PROBE from this surface** (partial support, one specific hit against)

**The one question:** *what is the actual list?* I could not obtain the ~30 references — Issue #48's body and comments do not contain them, and I will not check a list I cannot see. **Declared hole; this surface cannot discharge P1. W1 owns it.**

What I can report from the artifact angle:
- **"Several 2026 agent-authorization papers" is not fabricated as a category.** A real, dense, dated cluster exists and several have code: **FORTIS** (arXiv 2605.09163) with a working repo at `lili0415/FORTIS-Benchmark`; **SkillScope** (2605.05868); **SkillTester** (2603.28815); **When Lower Privileges Suffice** (2606.20023); **Capability Minimization as a Safety Primitive** (2606.13884); **Capability Gates Are Not Authorization / ScopeGate** (2606.28679). There is also a curated `LLMSecurity/awesome-agent-skills-security` list, which is what a real subfield looks like. **This does not verify the specific IDs the owner supplied** — a plausible-looking cluster existing is exactly the condition under which a fabricated ID hides.
- **One specific hit against, and it matters:** the claimed *"published synthesis-to-runtime-monitor compiler."* The nearest 2026 instance I found is **PCAS** (arXiv 2602.16708, Palumbo/Choudhary/Choi/Chalasani/Jha, UW–Madison + Langroid), and **its code is not released** — the paper says "code for evaluations will be released soon," and I found no repo under Langroid or elsewhere. On this surface that is **a paper without an artifact**, and PCAS also explicitly disclaims the synthesis half: *"We do not address automatic synthesis of formal policies from natural language policy documents in this work."* If the reference in question is PCAS, the claim as stated is **overreached in two directions at once** (no artifact; no synthesis). If it is an older, genuinely-published compiler, W1 must name it.
- **`SPL` (arXiv 2607.07727, Wen G. Gong, 2026)** — declarative deterministic-probabilistic composition; single author, no repository found, PDF only. Ambition.

**What each answer decides:** if the list checks out (W1), P1 survives and P2's absence claim retains its foundation. If the synthesis-to-runtime-monitor compiler turns out to be PCAS, **P2 sub-claim (iii) gains rather than loses**, because PCAS disclaims synthesis — but the theme loses a citation it thought was a shipped precedent.

---

## Cold leg — assumptions nobody put on the list

Three, in descending order of consequence. The first is a candidate **sixth position**.

### C-1 (proposed P6) — the theme assumes the harness is a **runtime**. The field's answer is a **compiler.**
Every position, and JURATI's whole framing ("the single edge where all LLM calls originate," "the queen executes"), presumes a long-lived process that owns execution. The most mature thing on this surface does the opposite: **`gh aw compile` emits a `.lock.yml` and then gets out of the way.** The guarantee is carried by an enforcement plane that already existed (GitHub Actions: job permissions, environment protection rules, OIDC claims, branch protection) and that the harness never runs inside. `majiayu000/harness` is a hybrid — a Rust control plane, but its policy is a **Starlark program evaluated outside the LLM**, i.e. a compiled artifact again.

This is not a mechanism preference; it reorders the theme. If the durable asset is **a compiler plus an intermediate representation of declared authority**, then: H7's two-backend split (versioned definition store + event sink) is answered by *git plus whatever the target plane already logs*; C-3 (files stay source of truth) stops being a constraint and becomes the architecture; "build-once / any-LLM" becomes **compile-to-many-enforcement-planes**, which is a harder and more defensible claim than plugging in model backends; and the honest deliverable becomes *"here is what your declared authority model compiles to on Actions / on the Claude CLI / on an MCP gateway, and here is which guarantees did not survive the compilation."* **Nobody ships that, and it is a better statement of the moat than P2's current one.** The run should decide whether the harness is a runtime or a compiler before it decides anything else.

### C-2 — the theme assumes enforcement belongs at **one edge**. Everything shipping is **layered**, and layering is why bypass doesn't kill it.
The single-edge premise is stated as a virtue (one place to audit). The shipped systems put enforcement at five independent planes at once — token scope, container/kernel, network egress, per-job permission, VCS branch protection — none of which is sufficient alone and no two of which fail together. **A single edge is a single bypass point,** and our own record is two-for-two on institutionalized bypass. The layered design is also what makes gh-aw's *inference* gate tolerable (P3): the model gate can be turned off and the agent is still powerless. **Untested premise, load-bearing, and the evidence runs against it.**

### C-3 — "any-LLM pluggable" is assumed to be a property of the *harness*. It breaks at the *enforcement* layer, not the invocation layer.
gh-aw supports four engines, so pluggability looks solved. But each engine has a different enforcement model — Claude has hooks and deny-rules that remove tool definitions; Codex has a sandbox mode; Copilot has none of that. gh-aw achieves plurality by **enforcing nothing at the engine and everything at the plane below**, which is the only way it works. Consequence the theme has not stated: **an any-LLM harness inherits the weakest engine's enforcement model, unless it refuses to rely on any engine's enforcement at all.** H5 ("anti-lock-in as a consequence of representation") is true for the *workflow definition* and unproven for the *guarantee*. That distinction should be written into H5 before it is proved.

*(Also noted, lower value: the eight concerns have no **composition/seam** concern, despite W0-e naming inter-agent misalignment as a top failure category; and "cost transparency and management" silently fuses metering — solved everywhere — with pre-authorization of spend — shipped nowhere. Two concerns wearing one name will hide the real gap at triage.)*

---

## Suspected cross-surface aliases (flag, do not merge)

- **`(workflow, phase, agent-role)` → capability set** is almost certainly called **"task-based / workflow authorization"** in W1's literature (mid-1990s onward), **"OIDC subject-claim-scoped role assumption"** in W2's CI/CD products, and **"step-level attestation" or "authorized actor per step (in-toto layout)"** in W4's supply-chain material. Same object, four names.
- **Gate-predicate independence from the exiting phase's write-set** is very likely **non-interference / information-flow control** in W1, and possibly **"separation of duty"** in W4's BPM material. My negative on this surface is only about *implementations*.
- **gh-aw's `safe-outputs`** is structurally the **proposal-then-deterministic-check / "propose, don't act"** pattern; W1 will meet it as *reference monitor* + *capability attenuation*, and W4 as the **two-man rule** or the **plant-operations "recommend vs execute" split**. arXiv 2604.12986 (*"Parallax: Why AI Agents That Think Must Never Act"*) is likely W1's name for the same shape.
- **"Threat detection" / LLM-as-security-judge** will appear in W2 as **"AI guardrails"** and in W1 as **model-based prompt-injection defence with measured false-accept rates**. Cross-check the rates: gh-aw ships no numbers at all.
- **"Agent harness engineering"** (Viv Trivedy's coinage; Osmani's writeup) is probably the practitioner-surface alias of what W2 will call **"agent orchestration platform"** and W1 will not have a name for at all.

---

## Reuse/dedup notes (node ids)

- **Dedup performed** against wfh-001's filed technologies via `context_search` (`agent_id: wfh-005-scout-active-dev`, read-only). Nearest existing nodes to this surface's finds: **#143** (GitHub Copilot, structural PR/branch gates), **#141** (Devin `request_scope`), **#144** (Cline non-bypassable Plan mode), **#137** (OpenHands), **#149** (LangGraph Studio), **#150/#159** (canvas/observability folds), **#160** (Temporal, folded).
- **Finding that should go to the leader: `github/gh-aw` has no node in Unimatrix.** Three separate searches (incl. a direct-name query) return nothing. The theme's watchlist calls it "the nearest shipping instance of the design" and says it was "characterized in wfh-001"; the graph does not agree. Either it was folded into #159/#160 without a name, or it was never filed. Given it is now the single most important object on this surface, that is a filing gap, not a naming quibble.
- **Nothing else here duplicates a filed node.** `majiayu000/harness`, the MCP-gateway category, the Temporal agent-plugin line, PCAS, and the 2026 over-privilege paper cluster are all **new to the graph**.
- **#160 (Temporal) needs correcting, not re-proposing:** wfh-004/W0-a records "the gap is that nobody has connected [durable execution] to agents." As of 2026-07-16 that is false — Temporal ships plugins for LangGraph, OpenAI Agents SDK, Google ADK and AWS Strands. Route to the curator as a content correction with fresh evidence, not as a new candidate.
- **Source signal for everything in this file: `external-scan`**, except the `.claude/settings.json` + `.claude/agents/factory/*.md` inspection, which is **`dogfood-signal`**.
- **Firewall:** every find above is `claimed` at best. Nothing here was demonstrated by us except the local file inspection. No status moves.

---

## cites:

```yaml
cites:
  - type: repo
    ref: https://github.com/github/gh-aw
    title: "gh-aw — GitHub Agentic Workflows"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://github.github.com/gh-aw/introduction/architecture/
    title: "GitHub Agentic Workflows — Security Architecture"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://github.github.com/gh-aw/reference/threat-detection/
    title: "GitHub Agentic Workflows — Threat Detection"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://github.github.com/gh-aw/reference/network/
    title: "GitHub Agentic Workflows — Network Permissions"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://github.github.io/gh-aw-firewall/
    title: "Agent Workflow Firewall (AWF)"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-multi-phase/
    title: "Meet the Workflows: Multi-Phase Improvers"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/
    title: "GitHub Agentic Workflows are now in technical preview"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/github/gh-aw/issues/29171
    title: "Feature: allow safe-outputs.threat-detection to be controlled by workflow_call inputs"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/github/gh-aw-threat-detection
    title: "gh-aw-threat-detection"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: standard
    ref: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
    title: "The 2026-07-28 MCP Specification Release Candidate"
    org: Model Context Protocol
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://www.rockcybermusings.com/p/mcp-authorization-scope-spec-gap
    title: "MCP Authorization Scope Is the Hole the New Spec Handed You"
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://code.claude.com/docs/en/agent-sdk/permissions
    title: "Claude Agent SDK — Configure permissions"
    org: Anthropic
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/anthropics/claude-agent-sdk-typescript/issues/172
    title: "AgentDefinition.tools and disallowedTools are not enforced for subagent child processes"
    org: Anthropic
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2602.16708
    title: "Policy Compiler for Secure Agentic Systems (PCAS)"
    author: "Palumbo; Choudhary; Choi; Chalasani; Jha"
    org: "University of Wisconsin–Madison; Langroid"
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2607.07727
    title: "SPL: Orchestrating Workflows with Declarative Deterministic-Probabilistic Composition"
    author: "Gong"
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2605.09163
    title: "FORTIS: Benchmarking Over-Privilege in Agent Skills"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/lili0415/FORTIS-Benchmark
    title: "FORTIS-Benchmark"
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2605.05868
    title: "SkillScope: Toward Fine-Grained Least-Privilege Enforcement for Agent Skills"
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2606.28679
    title: "Capability Gates Are Not Authorization: Confused-Deputy Failures in LLM Agent Frameworks (ScopeGate)"
    year: 2026
    surface: active-dev
  - type: paper
    ref: arXiv:2606.20023
    title: "When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/LLMSecurity/awesome-agent-skills-security
    title: "awesome-agent-skills-security"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/openai/openai-agents-python/issues/2868
    title: "Per-tool authorization middleware for agent tool calls"
    org: OpenAI
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/openai/openai-agents-python/issues/2775
    title: "Runtime governance guardrails for OpenAI Agents SDK"
    org: OpenAI
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
    title: "OpenAI Agents — Guardrails and human review"
    org: OpenAI
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://temporal.io/blog/temporal-langgraph-plugin-durable-execution
    title: "Temporal LangGraph Plugin adds Durable Execution"
    org: Temporal
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/microsoft/agent-framework/discussions/1092
    title: "Thoughts on supporting Durable execution"
    org: Microsoft
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://www.diagrid.io/blog/still-not-durable-how-microsoft-agent-framework-and-strands-agents-repeat-the-same-mistake
    title: "Still Not Durable: MS Agent Framework & Strands"
    org: Diagrid
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/majiayu000/harness
    title: "harness — Rust control plane for Claude Code & Codex"
    author: "majiayu000"
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://addyosmani.com/blog/agent-harness-engineering/
    title: "Agent Harness Engineering"
    author: "Osmani"
    year: 2026
    surface: active-dev
  - type: repo
    ref: https://github.com/ai-boost/awesome-harness-engineering
    title: "awesome-harness-engineering"
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://docs.github.com/en/actions/reference/security/oidc
    title: "GitHub Actions — OpenID Connect reference (subject claims, job_workflow_ref, environment)"
    org: GitHub
    year: 2026
    surface: active-dev
  - type: docs
    ref: https://bazel.build/docs/sandboxing
    title: "Bazel — Sandboxing (declared inputs and outputs)"
    org: Bazel
    surface: active-dev
  - type: blog
    ref: https://aws.amazon.com/blogs/security/enforce-least-privilege-authorization-in-multi-agent-ai-chains-using-cedar/
    title: "Enforce least-privilege authorization in multi-agent AI chains using Cedar"
    org: AWS
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://www.lunar.dev/post/the-best-open-source-mcp-gateways-in-2026
    title: "Open-source MCP gateways in 2026 (MCPX Tool Groups; ContextForge; Docker MCP Gateway)"
    org: Lunar.dev
    year: 2026
    surface: active-dev
  - type: blog
    ref: https://ralphloop.sh/blog/bypass-permissions-yolo-mode-safely/
    title: "Running Agents in YOLO Mode Safely"
    year: 2026
    surface: active-dev
  - type: docs
    ref: /workspaces/arch-research/.claude/settings.json
    title: "arch-research harness configuration — hooks only, zero permission rules (dogfood-signal)"
    org: dug-21
    year: 2026
    surface: active-dev
```

---

## Compact return

| Position | Verdict | One line |
|---|---|---|
| **P4** | **WOUNDED (severely)** → **ASSEMBLE** | gh-aw + Temporal-class durability + MCP gateway + sandbox covers ~6/8 concerns; remainder = capability derived from the *author's* declared phase, portable across enforcement planes. **Window closing ~6–12 months.** |
| **P2** | **WOUNDED** | (i) falsified in weak form (Actions OIDC `job_workflow_ref`+`environment`, gh-aw safe-output jobs); (ii) **survives** (legible negative: Bazel/in-toto/SLSA searched, none states the independence rule); (iii) **falsified** (`gh aw compile` derives the permission ceiling from declared demand). |
| **P3** | **WOUNDED** | Inference *is* shipping on the enforcement path (Claude `auto` model classifier; gh-aw threat detection blocking writes) — but always **inside** a deterministic envelope, never as the envelope. Bypass evidence strong: gh-aw #29171, `threat-detection: false`, YOLO mode. The real binding constraint is **friction**, not inference. |
| **P5** | **SURVIVES, ranking wounded** | Per-tool authz (`openai-agents-python` #2868), durability (`agent-framework` #1092, Strands #1138), cost caps ("crash barrier, not a smoke alarm") are demonstrably others' problems. Introspection and mid-run steering are largely ours alone. |
| **P1** | **NEEDS-A-PROBE** (this surface cannot discharge it) | Reference list not obtainable from Issue #48 → declared hole for W1. Partial support: the 2026 agent-authorization cluster is real with code (FORTIS repo). One hit against: the "published synthesis-to-runtime-monitor compiler" — nearest instance PCAS has **no released code** and explicitly disclaims synthesis. |
| **Cold leg** | **Proposed P6 + 2 more** | (C-1, candidate sixth position) the theme assumes a **runtime**; the field's mature answer is a **compiler**. (C-2) single-edge enforcement vs. shipped layered enforcement. (C-3) any-LLM pluggability breaks at the enforcement layer, not the invocation layer. |

**Flags for the leader:** ① `github/gh-aw` has **no Unimatrix node** despite being the theme's #1 watchlist entry — filing gap. ② **#160 (Temporal) needs a content correction, not a new candidate** — wfh-004/W0-a's "nobody connected durable execution to agents" is out of date as of 2026-07-16. ③ Both watchlist re-check conditions that fired should be **retightened** (MCP: "a SEP proposing per-tool scopes"; permission models: "SDK issue #172 closes"). ④ **Theme-revision signal, for the owner gate:** C-1 (runtime vs compiler) is upstream of H7, C-3 and the Option C question, and this run is not permitted to settle it — but it should be surfaced verbatim, because it changes what "build" would even mean.
