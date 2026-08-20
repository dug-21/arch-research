# verify-V4-dogwood.md — targeted verification: does Dogwood close the aggregation problem?

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · **agent_id:** `wfh-007-v4-scout` · targeted verification
**Origin:** flagged by scout V2 (`verify-V2-cedar.md` §5 item 3) against `scout-merged.md` Cluster C item 2. **Leader's call**, not an owner-named target.
**Reuse-first:** graph returns #202 (AgentCore + Cedar, ASSEMBLE), #199, #203, #205. **Dogwood is not in the graph.** #202's ASSEMBLE ruling is not re-litigated.
**Nothing cloned, installed, built or run.** Everything below is `claimed` at most.

---

## 1. What is actually shipped

**A single-contributor, two-week-old, internally-developed reference interpreter whose own README says it is not for production — mirrored out of Amazon, not developed in the open.** `[demonstrated — repo metadata + primary source]`

| Fact | Value |
|---|---|
| Repo | `dogwood-policy/dogwood` — *"Reference parser and interpreter for the Dogwood policy language"* |
| Licence | Apache-2.0. `NOTICE`: *"Copyright Amazon.com, Inc. or its affiliates."* Instantiated from `amazon-archives/__template_Apache-2.0`, carrying Amazon Bindle custom properties |
| Created / last push | **2026-07-27** / **2026-08-12** |
| Commits | **5, total.** First substantive commit 2026-08-06 |
| Contributors | **1**, plus a "Dogwood Publish Bot". Two of five commits are *"Sync from internal source"* — a one-way mirror |
| Stars / forks / **watchers** | 341 / 22 / **6** — launch-publicity stars, not a community |
| Releases / tags | **None** |
| Distribution | **Not on crates.io.** `Cargo.toml`: `publish = ["brazil"]` — pinned to Amazon's internal registry. Consumption is `{ git = "…" }` off `main` |
| Version | `1.0.0` in workspace metadata, unreleased |

**Its own README, verbatim:** *"This reference interpreter is **NOT** intended for production use."* It then enumerates nine things a production engine must add and it does not have: event timestamp integrity, event authentication, trace management (*"the built-in `InMemoryTemporalEngine` has no eviction or size cap"*), Rhai sandboxing (*"no CPU/memory limits configured by default"*), multi-tenancy isolation, audit logging, and SSRF (*"`http_get` … performs NO host or IP validation — it will connect to any address the URL specifies, including internal/private endpoints"*).

**Three distinct objects, and they must not be conflated:**
1. **The Dogwood *language*** — specified, ~68KB of formal spec prose + grammar, coherent.
2. **The Dogwood *reference interpreter*** — a semantics demonstrator, disclaimed for production.
3. **AgentCore Policy's temporal feature** — a GA AWS service in 16 regions, closed implementation, which *uses* the language. **The only shipped enforcement artifact, and we cannot read it.**

### The "every valid Cedar policy is also a valid Dogwood policy" claim is not borne out, and is not made by Dogwood

`[inferred from reading — primary sources on both sides]`

- The claim appears **only in AWS's AgentCore docs**, twice.
- **Dogwood's own docs never say it.** Grepping the guide and formal spec for "superset" / "every valid Cedar" returns **nothing**. The README says *"Cedar-derived syntax"*. The formal spec says: *"Dogwood is defined by **translation** into Cedar plus a stateful **monitor**."* **Translation is not superset.**
- **Divergence is being actively repaired.** The 2026-08-12 changelog: *"parser: Decode 'like' patterns with Cedar's escaper"*, *"parser: Decode string literals with Cedar's unescaper"*, *"testing: **Corpus cases for string-escape Cedar divergences**"*. Cedar compatibility is a **convergence target with a differential corpus**, not a proved property.
- **AgentCore adds an effect neither Cedar nor OSS Dogwood has:** `suppressOutput (…) when guardrails {…}`. Dogwood's grammar: *"The effect … must be exactly `permit` or `forbid`."* **The hosted dialect ≠ the open language.**

### The maturity contrast with Cedar is the most decision-relevant fact

V2 established Cedar's core is **machine-checked in Lean**, differential-random-tested against the Rust engine. **Dogwood has no equivalent.** Grepping the 67KB formal specification for "Lean", "theorem", "machine-checked", "formally verified" returns **zero hits** — every match is the word "boolean". Dogwood's assurance is a prose spec plus a test corpus. **The temporal layer is exactly the part with no proof, sitting on top of the part that has one.**

---

## 2. The temporal mechanism, and who owns the session boundary

**The answer is layered, and the layers disagree. This is the section that matters.**

### At the language level there is no session at all

`[inferred from reading — primary source]`

Dogwood's docs contain **no "policy session" concept**. The entry point is `pub fn is_authorized(&mut self, event: &Event) -> Option<Response>` — **`&mut self`: the `Authorizer` instance *is* the session.** *"No explicit session or trace identifier is required — the authorizer instance itself maintains the accumulated history."*

Slicing is done by **pins**, declared in the *event schema* (author-side, not caller-side):

> *"When the event schema declares a **universal symmetric pin** … every temporal condition is instead evaluated over the **slice** of the trace agreeing with the current request on the pinned field(s) … **The default event schema declares such a pin, on `callerPrincipal`**."*

This yields the **partition guarantee**: *"storage and evaluation may be sharded by the pinned key without changing any verdict."* **At the language level the boundary is the authenticated principal, chosen by the schema author — the bounded party cannot touch it.**

### At the AgentCore level the boundary is caller-chosen, and AWS says so under "Security considerations"

`[asserted — AWS vendor docs, concordant and self-incriminating]`

> *"Rate limiting with temporal policies applies within a single session. **Because temporal history is scoped to a session and the session ID is supplied by the caller**, a `count`-based limit such as 'at most N calls per session' counts only the events recorded for that session. **Starting a new session begins a new count**."*

And: *"**Session IDs are customer-managed.** … **A new session ID means a fresh temporal policy evaluation boundary.**"* The docs even list per-request session IDs as a strategy whose consequence is *"Temporal policies are effectively disabled — no history to evaluate."*

Mechanics: header `x-amzn-bedrock-agentcore-policy-session-id`, 1–128 chars, **the Gateway does not generate one**, implicit creation on first use, no create-session API; omit it and requests **fail closed** if a temporal policy exists.

### But "the caller" is the harness, not the model — and that distinction is load-bearing

**This is the finding that keeps the mechanism from being decorative.** `[asserted — AWS docs]`

In `User → Gateway → Runtime (agent) → Gateway (tool call) → Target`, the session id is set **once, by the application, at the first Gateway hop**. Thereafter it *"rides inside the WAT"* — an AWS-signed, opaque, 15-minute Workload Access Token carrying `sessionId`, `callerPrincipal` and an ordered workload chain, propagated on an internal header the docs say *"cannot be forged, tampered with, or decoded by callers or intermediaries"*.

| Bounded party's position | Can it reset its own session boundary? |
|---|---|
| LLM agent inside AgentCore Runtime whose **only** egress is the Gateway | **No.** The session id is in a signed opaque token minted upstream. A genuine out-of-reach interposition point. |
| Agent with independent network egress **and** the bearer token / IAM identity | **Yes, trivially.** It calls the Gateway URL directly with a fresh UUID. Nothing documented prevents this. |
| Any caller on an `authorizerType=NONE` gateway | Worse — *"One caller's actions count toward another's rate limits … Temporal policy on unauthenticated gateways is **advisory only**."* |

**Verdict on the header question: the mechanism is not decorative, but its integrity is entirely inherited from the harness's control of egress and identity — not from the policy language.** Dogwood contributes zero to keeping the boundary out of the agent's reach; the WAT and the network topology do all of that work.

### Two lifecycle facts nobody flagged

1. **Sessions cannot be closed and expire on a 24-hour idle timeout.** Explicit close: *"**Not supported**; sessions expire naturally."* **There is no revoke — you cannot terminate a running budget.**
2. **Editing a temporal policy wipes every open session's accumulated history.** *"Adding or updating a temporal policy on the engine invalidates the engine's active temporal policy sessions … The new session starts with an empty history."* **Tightening a budget resets every budget.** A real operational hazard for anything treating these as safety counters.

---

## 3. What state is retained, and where

**Open source: everything, in RAM, unbounded, lost on restart. AWS: undocumented.** `[demonstrated — README; asserted — AWS]`

`InMemoryTemporalEngine` appends **every ingested event**, decision-kind or not. README: *"**no eviction or size cap** … its **trace is lost after crash/restart** … requests/events may contain sensitive data, so some method of protecting and purging that data ought to be used."* A `TemporalEngine` trait exists for database-backed replacements; **none ships**. **No consistency guarantee is stated anywhere** — the formal spec is single-threaded, and `&mut self` means the reference type is not concurrently callable at all.

**AgentCore.** Storage backend, durability, per-session event cap and retention are **not documented on any page read**; the quotas page 404s to a stub. What is documented:

| Quota | Value |
|---|---|
| Temporal policies per policy engine | **25** |
| Temporal operators per policy | **3** |
| Maximum time window per temporal condition | **24 hours** |
| Session idle timeout | **24 hours** |

`TemporalLatency` metric exists, implying a measurable per-request cost, but **no latency figure is published.**

**The 24h ceiling is a hard architectural limit.** No temporal invariant longer than a day is expressible — no monthly spend cap, no "at most three per quarter."

---

## 4. Which aggregation cases it covers, and which it does not

Read from the operator semantics and grammar, not the feature bullets. `[inferred from reading — primary source]`

**Operators:** `formerly within W` (∃ in window), `previous within W`, `left since within W right` (∀ since anchor), `!`, `&&`, `exists (x: T). φ`, `tp(t)`, and `count` / `sum`. Windows mandatory and closed; strictly past-only.

### Covered — and covered properly

| Run's example | Covered? |
|---|---|
| **N calls of the same action in a window** | **Yes** — `(count for (t: Timepoint). where (formerly within 1h (…Action::"Transfer"::request{…} && tp(t)))) == 3` |
| **Cumulative numeric total crossing a threshold** | **Yes, within one action class** — `(sum a for (a: Long), (t: Timepoint). …) == total && total > 1000` |
| **Prior approval before a later action** | **Yes, and genuinely relational — not counting.** AWS's own: `permit(…, action == …"SellShares", …) when temporal { formerly within 1h …"ApproveSale"::response{ eventResource: resource, input.stock: context.input.stock, input.shares: context.input.shares, output.approved: true } };` — the approval must be *for this stock, this share count, this resource*. **Field correlation, not a counter.** |

**So "does it reduce to counting?" — no.** `since` with correlated variables expresses continuous-holding relational invariants (*"the user has not been revoked since they were granted"*). Pairwise ordering and taint-style rules are first-class. **That is more than the merge's framing anticipated and should be conceded plainly.**

### Not covered — structurally, not as a roadmap gap

**The cross-class case (exfiltrate-by-many-small-reads) is NOT expressible, for two compounding grammar reasons:**

1. **A predicate names exactly one fully-qualified action id.** Wildcards apply to **field patterns only**, never to the action segment.
2. **There is no disjunction.** Verbatim: *"The temporal sublanguage has exactly **one** boolean connective: conjunction, `&&`. There is **no `||`** … **If you need 'A or B,' write two separate policy rules**."*

An aggregate is legal *only* as the immediate operand of a single comparison, so it cannot span two rules. Therefore **`sum` and `count` cannot range over a set of distinct action classes.** You can budget `Read`, and separately `Export`, and separately `Send` — you **cannot** compute one running total across them.

**That is precisely H-B H18's self-declared miss, reproduced in the shipped artifact for the identical structural reason.**

| Case | Status |
|---|---|
| **Sequences spanning two sessions** | **No**, by construction and by AWS's own admission |
| **Sequences spanning two programs** | **No.** Requires unbroken WAT propagation; *"do not support cross-Region or cross-account propagation"*; any non-Gateway hop breaks it |
| **Semantic composition violations** | **No.** No vocabulary in which "the meaning of the composition is forbidden" can be stated |
| **Cross-class taint, generally** | **Only pairwise, hand-enumerated.** AWS's healthcare example is one source class → one sink class. With no disjunction, N sources × M sinks needs N×M rules against a **25-policy cap**. No propagation through derived values |

### Three footguns that bear on using this as a safety control

`[asserted — AWS docs, explicit]`

1. **Denied attempts are invisible to `response` conditions.** *"a condition that matches a `response` event considers only prior actions that were permitted."* **A probing agent's rejected attempts do not accumulate.**
2. **Self-reference includes the current request** — off-by-one, silently.
3. **Field-consistency silent weakening.** *"Supplying only one silently weakens either temporal or Cedar checks."* Action-name mismatch *"causes temporal predicates to silently not match while Cedar may still authorize the action."* **Both fail-open by omission — the same shape V2 found in Cedar's erroring-forbid path, in a new place.**

---

## 5. Guardrails / information providers

**An unconditional, evaluated-every-request computation whose output is injected into `context` before Cedar runs.** `[inferred from reading — OSS; asserted — AWS]`

**Open-source Dogwood.** Lowering hoists provider calls into `context.providers.<id>` **before Cedar ever sees the policy** — so from Cedar's side it is an ordinary context read, and V2's context-trust analysis applies unchanged. Dogwood *"evaluates every declared provider **unconditionally**"* regardless of rule scope — **a per-request cost on every request**.

- **Authorship:** the **policy/schema author**, via `providers.json`. **Not the bounded party.**
- **Failure:** *"This reference interpreter fails closed."* Explicitly implementation-specific.
- **Latency budget: none.** Rhai runs *"with no CPU/memory limits configured by default. A malicious or buggy provider script could infinite-loop or allocate unbounded memory, starving the authorizer."*
- **Network:** when enabled, `http_get` does **no SSRF validation at all**.

**AgentCore Guardrails.** A closed implementation of the same slot: extracts a declared `dataPath`, calls Bedrock `InvokeGuardrailChecks`, injects confidence scores. Three safeguards only; scores are **discrete** {0, 0.2, 0.4, 0.6, 0.8, 1.0}; `when guardrails {…}` **replaces** `when {…}` and cannot be mixed with standard Cedar conditions. Ships in **8 of 16** temporal-capable regions. **Failure/timeout behaviour undocumented** — declared hole.

### On "is this an intent-declaration hole in new clothes?"

**No, but only halfway.**
- **The provider *code* is author-side.** The bounded party cannot write, register or alter it — a real trust asymmetry, the opposite of an intent declaration.
- **The provider's *input* is agent-side.** Every documented example passes `context.input.*` — model-generated payload. So a provider is an **author-controlled function over attacker-controlled data**: stronger than an attacker-supplied claim, weaker than an out-of-band fact.
- **AWS's own caveat is the sharp end:** *"Guardrails are non-deterministic. The same input can result in different outputs."* **A probabilistic classifier in an evaluation position that reads as deterministic** — the Cluster H "present, believed, bypassable" shape. `permit … when guardrails { …lessThan(0.4) }` grants on a classifier's silence.

---

## DECISION LINE

**(b) — the merge's "aggregation is unsolved" claim NEEDS NARROWING, and (c) is falsified for one precisely nameable subclass. The claim as written is overbroad; the hard core is untouched.**

**Falsified for this subclass, by a shipped GA artifact:**

> *Within a single mediated session, at a single enforcement chokepoint, over a bounded window of ≤24h: counted repetitions of **one** action class, cumulative numeric totals over **one** action class, and pairwise ordering/taint constraints between **two named** action classes with field-level correlation between the past event and the current request.*

For that subclass, aggregation is not open, not a research problem, and not something to build. It is a policy language with an AWS GA implementation in 16 regions, and it is **configuration**.

**Stands unchanged — every part the merge actually leaned on:**

1. **Cross-class aggregation.** Not a roadmap gap — a **grammar impossibility**. One action id per predicate, no `||`, aggregates confined to one comparison operand.
2. **Cross-session.** AWS states the evasion itself, under "Security considerations."
3. **Cross-program.** Requires unbroken WAT propagation, single account, single region.
4. **Semantic composition.** No vocabulary for it exists.
5. **Anything beyond 24 hours.** Hard cap.

**The framing correction the merge should absorb:** *"aggregation reduces to counting"* is **wrong**. `since` with correlated variables expresses genuine relational trajectory invariants. The limit is not expressive power over a *trajectory* — it is expressive power over a *set of action classes*. **The barrier is disjunction, not statefulness.** Sharper, more actionable, and it points at what a real answer would need.

**Firewall note:** even the falsified subclass is `claimed`. We ran nothing. AWS's GA status is a vendor assertion; the open artifact is a disclaimed non-production interpreter with 5 commits, one author, no releases, no formal verification, and Cedar-divergence bugs fixed eight days ago.

### What changes for the five dependent hypotheses

| Hypothesis | Change |
|---|---|
| **H-B H18** — per-class consequence budgets, *"a floor, not safety"* | **Cheapest change, doubly vindicated.** Dogwood *is* per-class budgets, shipped — the mechanism moves from build toward configuration-over-#202 for the covered part. **And its self-declared miss is confirmed by the artifact having the identical miss for the identical structural reason.** H18's caveat is now backed by an external shipped artifact, not just our reasoning. Strongest update in the set |
| **H-B H19** — trajectory invariants at cycle-review time | **Narrowed, not killed.** A real subset moves from after-the-fact to **inline, pre-authorization**. H19's justification survives only for invariants that are cross-class, cross-session, cross-program, semantic, or >24h. **Re-scope to that residue rather than carry it whole** |
| **H-B H20** — taint-coupled derivation | **Partially anticipated.** One-hop source→sink taint is shipped. But pairwise, hand-enumerated, capped at 25 policies, **no propagation through derived values**. H20's genuinely novel leg — derivation tracking — is untouched |
| **H-A H20 / H26** — serial attenuated contracts | **Essentially untouched.** One adjacent lead: the WAT carries *"the workload chain — an ordered list of AgentCore services the request has traversed"*, but it is **not readable from policy**. The nearest shipped thing to H-A H20's object, and **the gap is one exposed field wide** |
| **H-D H7** — ownership boundaries as partial aggregation control | **Untouched, but gains a mechanism to borrow.** Dogwood's **universal symmetric pin** plus its **partition guarantee** is a formalised, verdict-preserving statement of exactly what H7 argues informally. H7 should cite the pin/partition construction as prior art |

**One cross-cutting correction for triage:** the strongest thing here is **not** the counters. It is that **the session boundary rides in a signed opaque token the agent cannot read, write or strip**, while the counting happens in an evaluation position downstream of the agent. **That is the Jurati interposition thesis, shipped, by AWS, in 16 regions.** The counters are the weak half; the WAT is the strong half. Anything adopting this should be adopting the boundary mechanism and treating the counting as a bounded convenience with a documented evasion.

---

## Cross-surface alias flag (for distillation)

**Dogwood's temporal sublanguage is, on its face, bounded past-time metric first-order temporal logic — the MonPoly / MFOTL family — wearing Cedar syntax.** `[inferred from reading — operator-set correspondence; MonPoly sources NOT fetched]`

The correspondence is too exact to be coincidence: `formerly` = ONCE (◆), `previous` = PREVIOUS (⊖), `since` = SINCE (S); mandatory bounded metric intervals; `count`/`sum` with explicit group-by and deduplication; and an acceptance discipline built entirely on **range-restriction and closure of every binder** — which is the classical **monitorability / safe-range** condition of MFOTL monitoring, not a Cedar idea. The absence of `||` and of future operators fits the same lineage.

**If that holds, four decades of runtime-verification literature (Basin, Klaedtke, Müller, Zălinescu et al.) bears directly on this run's aggregation question — including known complexity bounds and known expressiveness limits — and none of it was read by any surface in wfh-007.** The adjacent surface searched aggregation prior art from the *security* side (Denning/Tallam/Bertino); the **monitoring side appears unsearched**. Flagged as the single highest-value follow-up on the adjacent surface. Likely additional aliases: history-based access control (HBAC), stateful/temporal authorization, dynamic separation of duty, Brewer–Nash Chinese Wall.

---

## Graph recommendation (characterization only — not filed)

**Dogwood warrants its own node, distinct from #202** — a separable artifact (Apache-2.0 language + interpreter, own repo, own org, consumable without AWS), and evidence about it is not evidence about AgentCore. **But the three objects in §1 must not be merged into one node** — the language, the disclaimed reference interpreter, and AgentCore's closed feature have three different maturity stories, and a blurred node would assert production readiness the README explicitly disclaims. **Curator decision at formalize; flagged, not authored.**

---

## Declared holes

1. **AgentCore's temporal implementation is unreadable.** Storage, durability, per-session event cap, retention, concurrency under parallel tool calls, evaluation latency — all undocumented. **Everything in §3 about the AWS side is an absence of evidence, not evidence of absence.**
2. **Header-versus-WAT precedence is unspecified.** If a request carries **both** a service-propagated WAT and a caller-set session-id header, which wins? Not documented. **This is the exact hinge on which "can the agent reset its own boundary" turns for an agent with independent egress — the single most decision-relevant unknown remaining.**
3. **Guardrail failure and timeout behaviour on the AWS side.** The OSS interpreter fails closed and says so; AgentCore says nothing. A fail-open guardrail inverts every `forbid … when guardrails` rule.
4. **MonPoly / MFOTL correspondence unverified** — asserted from operator-set reading only.
5. **`10-provider-schema.md` and `06-macros.md` read via summary**, not source.
6. **The 1202-line formal specification was grepped, not read end to end.**
7. **Nothing was executed.** The cheapest real test — `dogwood replay` on a hand-built trace probing the cross-class case and the `request`-vs-`response` kind trap — remains untaken, and would be a few hours with no cloud spend.

---

## Citations (D14)

```
{type: repo, ref: https://github.com/dogwood-policy/dogwood, title: "dogwood — Reference parser and interpreter for the Dogwood policy language", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: repo, ref: https://github.com/dogwood-policy/dogwood/blob/main/README.md, title: "Dogwood README — key features and 'Security considerations when using the reference interpreter'", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: repo, ref: https://github.com/dogwood-policy/dogwood/blob/main/CHANGELOG.md, title: "Dogwood CHANGELOG 2026-08-12 — corpus cases for string-escape Cedar divergences", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: repo, ref: https://github.com/dogwood-policy/dogwood/blob/main/Cargo.toml, title: "Dogwood workspace manifest — version 1.0.0, publish = [brazil]", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: docs, ref: https://github.com/dogwood-policy/dogwood/blob/main/dogwood-docs/guide/04-temporal-expressions.md, title: "Dogwood guide — Temporal Expressions (formerly/previous/since, count/sum, universal symmetric pins)", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: docs, ref: https://github.com/dogwood-policy/dogwood/blob/main/dogwood-docs/guide/08-formal-specification.md, title: "Dogwood guide — Formal specification (translation into Cedar plus a stateful monitor; partition guarantee; grammar)", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: docs, ref: https://dogwood-policy.github.io/dogwood/guide/05-information-providers.html, title: "Dogwood guide — Information providers (lowering to context.providers, unconditional evaluation, fail-closed reference behaviour)", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: docs, ref: https://dogwood-policy.github.io/dogwood/guide/07-api-and-workflow.html, title: "Dogwood guide — API and workflow (is_authorized(&mut self), InMemoryTemporalEngine)", org: "Amazon.com, Inc.", year: 2026, surface: active-dev}
{type: docs, ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-temporal.html, title: "AgentCore Policy — Temporal policies (quotas, session invalidation, request/response event kinds, security considerations)", org: "Amazon Web Services", year: 2026, surface: products}
{type: docs, ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-session-based-temporal.html, title: "AgentCore Policy — Policy sessions and identity propagation (caller-supplied session id, WAT, authorizerType=NONE caveat)", org: "Amazon Web Services", year: 2026, surface: products}
{type: docs, ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-guardrails-in-policies.html, title: "AgentCore Policy — Guardrails in policies (when guardrails, suppressOutput, discrete confidence scores, non-determinism)", org: "Amazon Web Services", year: 2026, surface: products}
{type: docs, ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html, title: "AgentCore Policy — Core concepts (the 'every valid Cedar policy is also a valid Dogwood policy' claim)", org: "Amazon Web Services", year: 2026, surface: products}
```

**Source signal:** `external-scan` (targeted verification, originating from a scout V2 flag).
