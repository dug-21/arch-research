# verify-V2-cedar.md — targeted verification: Cedar forbid-only-context discipline (H-B H22)

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · **agent_id:** `wfh-007-v2-scout` · targeted verification, not a discovery scan
**Reuse:** #202 (Bedrock AgentCore Policy + Cedar, `grade:claimed`, ASSEMBLE, wfh-005) is the existing node. This pass adds **no new candidate** — it adds evidence *about a discipline that would ride on #202*, and should be filed as a `finding`, not a technology. The ASSEMBLE ruling is not re-litigated.
**Nothing was installed, built, or run.** Everything below is `claimed` at most.

---

## 1. Evaluation order — does `forbid` unconditionally override `permit`?

**Yes, unconditionally, with no ordering, precedence, or template exception — and it is machine-checked in Lean, not merely documented.** `[inferred from reading — primary source]`

The definitional semantics (the artifact AWS differential-random-tests the Rust engine against) is 14 lines and admits no special case:

```lean
public def isAuthorized (req : Request) (entities : Entities) (policies : Policies) : Response :=
  let forbids := satisfiedPolicies .forbid policies req entities
  let permits := satisfiedPolicies .permit policies req entities
  let erroringPolicies := errorPolicies policies req entities
  if forbids.isEmpty && !permits.isEmpty
  then { decision := .allow, determiningPolicies := permits, erroringPolicies }
  else { decision := .deny,  determiningPolicies := forbids, erroringPolicies }
```
— `cedar-spec/cedar-lean/Cedar/Spec/Authorizer.lean`

No policy list order, no priority field, no per-policy weight. The proved theorem:

```lean
/-- Forbid trumps permit: if a `forbid` policy is satisfied, the request is denied. -/
theorem forbid_trumps_permit
  (request : Request) (entities : Entities) (policies : Policies) :
  (IsExplicitlyForbidden request entities policies) →
  (isAuthorized request entities policies).decision = .deny
```
— `cedar-spec/cedar-lean/Cedar/Thm/Authorization.lean`

Companion theorems, all proved, in the same file: `allowed_only_if_explicitly_permitted`, `default_deny`, `allowed_iff_explicitly_permitted_and_not_denied`, `denied_iff_explicitly_denied_or_not_permitted`, **`order_and_dup_independent`** (decision invariant under policy-set permutation and duplication — this is the one that kills "precedence tricks"), `unchanged_deny_when_add_forbid`.

Docs match the proof verbatim: *"forbid overrides permit: even if a `permit` policy is satisfied, any satisfied `forbid` policy overrides it, producing a `Deny` decision."* `[asserted — vendor doc, concordant with the proof]`

**Templates do not invert it.** Two slots only, `?principal` and `?resource`; *"Placeholders can appear in **only** the policy scope on the right-hand side of the `==` or `in` operators"* — never in the action scope, never in `when`/`unless`. A linked template instantiates to an ordinary policy with an ordinary effect. `[inferred from reading]`

**The formal lineage is real.** `cedar-policy/cedar-spec` (Apache-2.0, 195★, pushed 2026-08-19) holds the Lean definitional engine, validator and symbolic compiler, plus proofs of authorization basics, sound policy slicing, sound type checking, sound level-based entity slicing.

### ⚠ The one thing that *does* break "forbid always denies": **erroring forbids fail open**

`satisfied` is `(evaluate policy.toExpr req entities) = .ok true`. A policy that **errors** is not `.ok true`, so it is **not** in `forbids`; it is recorded separately in `erroringPolicies` and **has no effect on the decision**. `[inferred from reading — primary source]`

Consequence for H22, load-bearing: a forbid rule reading `context.intent` where the caller **omits** `intent` raises a missing-attribute error, the forbid is silently skipped, and surviving permits carry the request to **Allow**. **The attack on a forbid-only-context design is not forging an intent — it is omitting or mistyping one.**

Mitigation exists and is cheap: `Request::new(principal, action, resource, context, Some(&schema))` — *"If `schema` is present, this constructor will validate that the `Request` complies with the given `schema`"* — rejects a non-conforming context at construction. But it is a **PEP-side obligation, not a language guarantee**, and must be designed in or the discipline is fail-open.

---

## 2. Is the discipline lintable? — **Yes, via a supported API. Named.**

**`cedar_policy::pst`** — *"a syntax tree representation of Cedar policies designed for programmatic manipulation."* Added in **cedar-policy 4.11.0 (2026-05-18)**; current release **4.12.0 (2026-07-28)**; in the crate's **default public API**, not behind an experimental feature flag. Reached via `Policy::to_pst()` / `try_into_pst()`, `Template::to_pst()`, `PolicySet::to_pst()`.

It exports exactly what the lint needs:
- **`pst::Clause`** — `When` / `Unless` variants, and **`pst::Expr`** (`#[non_exhaustive]`), fully walkable (`BinaryOp{left,right}`, `UnaryOp`, `GetAttr`, …).
- **`pst::Var`** — four variants: `Principal`, `Action`, `Resource`, **`Context`** (*"the request context record"*).

Combined with **`Policy::effect() -> Effect`** (`Permit | Forbid`), the enumeration H22 asks for — *which policies reference `context`, and what is each policy's effect* — is a straightforward walk over `PolicySet`. Perhaps 40–80 lines of Rust. No text parsing, no private crates.

Fallbacks: **`Policy::to_json()`** → EST JSON, stable, walkable from Python/JS; **`cedar-wasm`** exists in-repo, so the same walk is reachable from JS.

**What the lint is NOT:** there is no shipped `cedar lint` subcommand and no off-the-shelf rule. The CLI ships `validate`, `authorize`, `format`, and (experimental flavour, external cvc5) `cedar symcc`. **You would write this rule yourself.** Small, but yours to write and maintain.

**On AWS Verified Permissions:** partial, and worse than the crate. `ListPolicies` → `PolicyItem` returns `effect` and scope but **not the policy body**; detecting a `context` reference requires `GetPolicy` per policy then parsing with the crate anyway.

### ⚠ The rule as stated in H22 is **under-specified and admits a bypass**

The sharpest technical finding of the pass. `[inferred from reading — Cedar operator/clause semantics]`

H22's rule is *"policies referencing `context` may appear only in `forbid` rules, never `permit`."* That rule is **neither sufficient nor necessary**:

- **Not sufficient.** `forbid(...) unless { context.intent == "maintenance" };` satisfies the rule — the reference is in a forbid. But `unless {e}` ≡ `when {!e}`, so **a forged intent suppresses a deny**, and suppressing a deny is operationally indistinguishable from contributing to an allow. Same hole via `forbid(...) when { !context.… }` or any negation-parity flip inside a forbid condition. **A naive "context only in forbids" linter passes this policy.**
- **Not necessary.** `permit(...) unless { context.intent == "danger" };` violates the rule, yet the context reference can only ever *subtract* from that permit — exactly the property H22 wants.

The correct rule is **polarity-scoped, not effect-scoped**: context may appear only in **positive polarity within a `forbid` `when`**, or **positive polarity within a `permit` `unless`**; never under an odd number of negations, never in a `forbid` `unless`. Polarity tracking over `Expr` (counting `!` and the implicit negation of `Unless`) is still mechanical over the PST and still small — but it is **not** the one-line rule the hypothesis describes, and the naive version ships a control that is present, believed and bypassable, which Cluster H already names as *negative* safety.

### The stronger alternative: verify semantically instead of syntactically

`cedar-policy-symcc` (in-repo, formally modelled in Lean) compiles to SMT-LIB and verifies against cvc5-1.3.1:

```rust
pub async fn check_implies(&mut self, pset1: &WellTypedPolicies,
                           pset2: &WellTypedPolicies, symenv: &SymEnv) -> Result<bool>
// "Returns true iff the authorization decision of `pset1` implies that of `pset2`
//  for every well-formed input in the `symenv`."
```

So the discipline can be a **semantic obligation** rather than a syntactic one: let `P` be the full policy set and `P∖ctx` be `P` with every context-referencing policy deleted; **`check_implies(P, P∖ctx)`** asserts everything the intent leg allows, the intent-free set already allowed — i.e. **intent can only subtract**, proved over all well-formed requests, with a concrete counterexample when it fails. Polarity-blind; cannot be fooled by the `unless` bypass.

Price: cvc5 as an external runtime dependency, experimental-flavour CLI only, *"Surface area of these features can change between releases."* **Syntactic lint = cheap, stable, needs polarity care. Symbolic check = correct by construction, experimental, external solver.** Not the same price.

---

## 3. Who populates `context`, and is it trusted?

**Cedar's own security model assumes the whole authorization input — context included — is attacker-*un*modifiable. The hypothesis uses the slot against its designed grain.** `[inferred from reading]`

- **Who supplies it:** the calling application / PEP. *"Your application must gather all of the relevant information and provide it to Cedar's authorization engine when making the request."* Cedar never fetches context itself.
- **The stated trust assumption, verbatim from the security page:** *"Ensure that data used for authorization decisions… can't be accessed or modified by potential attackers."* Also *"Security is a shared responsibility"*; *"Normalize input data prior to invoking the authorization APIs"*; Cedar *"does not perform authentication."*
- **Best-practice page** frames context as *"information unique to a particular request, such as http headers, time of day, the caller's authentication or device posture"* — and warns only against putting principal/resource-natural data there. **It says nothing about trust in either direction.**

**Plain reading:** Cedar has **no documented notion of a partially-trusted request component**. There is no "this slot is untrusted" affordance. H22 deliberately places attacker-influenceable data into a slot whose documented contract is the opposite. That is **not forbidden** — the evaluation-position argument in §1 stands on its own — but it means:

1. **Zero** support from Cedar's guidance, validators or defaults for the trust asymmetry. The asymmetry lives entirely in your linter.
2. The fail-open-on-error behaviour in §1 is exactly the hazard the "keep authorization data unmodifiable" assumption makes irrelevant. Removing the assumption re-arms it.

---

## 4. Expressiveness cost — is "no positive phase grants from intent" actually forced?

**Yes, forced, and no Cedar feature relieves it.** `[inferred from reading]`

- **Forced by the semantics.** Allow requires a satisfied permit (`allowed_only_if_explicitly_permitted`, proved). If no permit may reference `context`, no permit's satisfaction can depend on the intent declaration; positive grants must be functions of `principal`/`action`/`resource` only. Theorem-level, not doc convention.
- **Templates do not help.** Slots are `?principal`/`?resource` only, scope-position only. A template cannot inject a phase into a permit's condition and cannot reference context at all.
- **The entity hierarchy gives a clean answer, and it is the answer H22 should adopt.** Make phase part of the **principal**: mint a per-phase principal entity (`Agent::"planner@run-42"`) `in` a phase group entity (`Phase::"plan"`), and write positive grants against the group. Cedar's group-membership over the entity hierarchy is designed for exactly this. Then:
  - **Phase-as-principal-attribute = trusted, may grant.** Bound at spawn/credential-issue time by whoever mints the identity.
  - **Phase-as-context-claim = untrusted, may only deny.** Whatever the running agent says it is doing.

  **These are two different facts that H22's framing conflates.** The expressiveness "cost" largely evaporates once separated — but only because the positive half stops being *intent* and becomes *identity*, which is a real design commitment, not a workaround. **The genuine residue:** a positive grant conditioned on a claim only the agent knows and no issuer can bind at mint time. If such a case exists, forbid-only-context cannot serve it, full stop.

---

## 5. The `context` slot in practice

**Yes — and the shipped instance is stronger evidence than the hypothesis assumed, because it puts *exactly the untrusted payload* in `context`.** `[asserted — AWS vendor docs, not verified by us]`

**Bedrock AgentCore Policy (#202) populates `context.input` with the tool call's arguments**, verbatim: *"`context.input` contains the arguments passed to the tool call."* Worked example — a call to `RefundTool___process_refund` with `{"orderId":"12345","amount":450,"reason":"Defective product"}` surfacing as `context.input.amount`, with the sample policy:

```
when {
  principal.hasTag("username") &&
  principal.getTag("username") == "refund-agent" &&
  context.input.amount < 500
}
```

**Read what that is.** In the one GA product doing per-tool-call agent authorization, `context` is **the model-generated argument payload** — the most attacker-influenceable object in the request, downstream of any prompt injection. Three consequences:

1. **The slot is already the untrusted-payload channel in practice**, notwithstanding §3's doc silence. But the precedent runs the *other* way: AWS's shipped example uses that untrusted value in a **`permit`** (`context.input.amount < 500` gating an allow) — precisely the pattern H22 wants to outlaw, shipped as the vendor's canonical example. **Adopting AgentCore Policy and the forbid-only-context discipline simultaneously means forbidding the vendor's documented idiom.** Composability cost; belongs in triage's view.
2. **`context.input` is already occupied.** An intent declaration would be a sibling key, and whether AgentCore permits arbitrary non-tool-argument context fields **could not be established** — see holes.
3. **New adjacent find, not previously in the graph: "Dogwood."** AgentCore's core-concepts page names an open-source Cedar-**compatible superset** (*"every valid Cedar policy is also a valid Dogwood policy"*) adding (a) **temporal conditions** evaluated over a **policy session** — *"requiring a prior approval, limiting how often an action runs, or keeping a running total under a threshold"* — and (b) **"information providers"** (Guardrails) computing a signal inline at evaluation time, with `when guardrails {…}` / `unless guardrails {…}` clause forms. Session id supplied by the caller in `x-amzn-bedrock-agentcore-policy-session-id`.

   **Flagged for distillation, deliberately not characterised here:** "limiting how often an action runs / keeping a running total under a threshold, evaluated over a session" is a direct hit on **Cluster C item 2 — aggregation** (Denning; Tallam's *aggregation inference*; Bertino's *trajectory assurance*), which scout-merged called *"the surviving hard problem"* and *"unsolved."* If Dogwood ships session-scoped counting and running totals as first-class policy conditions, **that claim needs re-testing against a shipped artifact.** Likely aliases: *stateful/temporal authorization*, *history-based access control*, *Chinese Wall / dynamic separation of duty*. Entry point: `dogwood-policy.github.io/dogwood/`. **Recommend a dedicated look.**

---

## DECISION LINE

**(a) Enforceable and lintable — with two qualifications that change the size of the job, neither fatal.**

- **Enforceable: yes, robustly.** Forbid-unconditionally-overrides-permit is proved in Lean (`forbid_trumps_permit`), order/duplicate-independent (`order_and_dup_independent`), with no template or precedence escape. H22's core mechanism — *monotone restriction by evaluation position* — is sound.
- **Lintable: yes, via a named supported API** — `cedar_policy::pst` (`Policy::to_pst()`, `pst::Clause::When`/`Unless`, `pst::Expr`, **`pst::Var::Context`**) × `Policy::effect()`, cedar-policy 4.12.0, default features, no text parsing.
- **Qualification 1 — the rule as written is wrong, not just imprecise.** `forbid(...) unless { context.… }` and negation inside a forbid `when` both let a forged intent **suppress a deny**. The lint must track **polarity**, not effect. Still mechanical, still small — but not one line.
- **Qualification 2 — erroring forbids fail open.** Missing or mistyped `context.intent` makes the forbid error, and erroring policies are excluded from the decision. **The attack is omission, not forgery.** Requires schema-validated request construction as a PEP-side obligation — not a language guarantee.
- **Available upgrade:** `check_implies(P, P∖ctx)` proves the intended property semantically over all well-formed requests, immune to both qualifications. Price: cvc5, experimental flavour, unstable surface.

**Net for triage:** H22's economic claim mostly survives — the intent leg is **configuration-plus-a-small-linter over a component already routed ASSEMBLE**, not a build. The correction is that the linter is a polarity-aware AST walk plus a request-validation obligation; and §4 shows the honest design splits "phase" into a trusted principal-side fact (may grant) and an untrusted context-side claim (may only deny) — a design commitment triage should make deliberately.

---

## Declared holes

1. **Whether AgentCore Policy permits injecting arbitrary caller-supplied context fields beyond `context.input`.** If not, the intent leg cannot use AgentCore's context slot and needs a different PEP. **The single most decision-relevant unknown remaining**, and a one-page read.
2. **Whether AgentCore/AVP expose a policy-enumeration API returning bodies in bulk.** AVP's shape confirmed; AgentCore's policy-management surface unread.
3. **Dogwood** — read only the AgentCore summary paragraph. Its temporal/session semantics vs Cluster C's aggregation problem is unassessed. Flagged, deliberately not half-characterised.
4. **`pst::Expr`'s exact variant list** — `BinaryOp`, `UnaryOp`, `GetAttr`, `Literal`, `VariadicOp` confirmed, `#[non_exhaustive]` confirmed; not exhaustively enumerated. `#[non_exhaustive]` means new variants can appear in a minor release — **the linter needs a catch-all arm that fails closed**, or a Cedar upgrade silently opens a hole.
5. **The Cedar OOPSLA/FSE papers** — not fetched; the Lean proofs were cited directly instead, which is stronger evidence. Noted as a skipped venue, not a gap.
6. **Nothing was executed.** H22's "cheapest test" (two hours in the playground) remains **untaken**; this pass replaces the *semantics* half with source reading and sharpens what the *lint* half must test — specifically, `forbid ... unless { context }` is the first case any POC should write.

---

## Citations (D14)

```
{type: repo, ref: https://github.com/cedar-policy/cedar-spec, title: "cedar-spec — Definitional implementation of Cedar and utilities for DRT", org: "Cedar Policy", year: 2026, surface: active-dev}
{type: repo, ref: https://github.com/cedar-policy/cedar-spec/blob/main/cedar-lean/Cedar/Spec/Authorizer.lean, title: "Cedar Lean definitional authorizer (isAuthorized, satisfied, satisfiedPolicies)", org: "Cedar Policy", surface: active-dev}
{type: repo, ref: https://github.com/cedar-policy/cedar-spec/blob/main/cedar-lean/Cedar/Thm/Authorization.lean, title: "Cedar Lean authorization theorems (forbid_trumps_permit, default_deny, order_and_dup_independent)", org: "Cedar Policy", surface: active-dev}
{type: repo, ref: https://github.com/cedar-policy/cedar/blob/main/cedar-policy/CHANGELOG.md, title: "cedar-policy CHANGELOG — 4.11.0 pst module; 4.12.0", org: "Cedar Policy", year: 2026, surface: active-dev}
{type: repo, ref: https://github.com/cedar-policy/cedar/blob/main/cedar-policy-symcc/README.md, title: "Symbolic Cedar Compiler (SymCC) — verified properties and cvc5 setup", org: "Cedar Policy", year: 2026, surface: active-dev}
{type: docs, ref: https://docs.rs/cedar-policy/latest/cedar_policy/pst/index.html, title: "cedar_policy::pst — public syntax tree (Var::Context, Clause, Expr)", org: "Cedar Policy", year: 2026, surface: active-dev}
{type: docs, ref: https://docs.rs/cedar-policy/latest/cedar_policy/struct.Policy.html, title: "cedar_policy::Policy — effect(), to_pst(), to_json()", org: "Cedar Policy", year: 2026, surface: active-dev}
{type: docs, ref: https://docs.rs/cedar-policy/latest/cedar_policy/struct.Request.html, title: "cedar_policy::Request::new — optional schema-based request validation", org: "Cedar Policy", year: 2026, surface: active-dev}
{type: docs, ref: https://docs.rs/cedar-policy-symcc/latest/cedar_policy_symcc/struct.CedarSymCompiler.html, title: "CedarSymCompiler — check_implies / check_equivalent / check_always_denies", org: "Cedar Policy", year: 2026, surface: active-dev}
{type: docs, ref: https://docs.cedarpolicy.com/auth/authorization.html, title: "Cedar — Authorization (permit/forbid combination, default deny)", org: "Cedar Policy", surface: products}
{type: docs, ref: https://docs.cedarpolicy.com/policies/templates.html, title: "Cedar — Policy templates (?principal / ?resource slot restrictions)", org: "Cedar Policy", surface: products}
{type: docs, ref: https://docs.cedarpolicy.com/other/security.html, title: "Cedar — Security (shared responsibility; protect authorization data from attackers)", org: "Cedar Policy", surface: products}
{type: docs, ref: https://docs.cedarpolicy.com/bestpractices/bp-using-the-context.html, title: "Cedar best practices — Using the context", org: "Cedar Policy", surface: products}
{type: docs, ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-conditions.html, title: "AgentCore Policy — Policy conditions (context.input holds tool call arguments)", org: "Amazon Web Services", year: 2026, surface: products}
{type: docs, ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html, title: "AgentCore Policy — Core concepts (forbid-wins engine, auto-generated Cedar schema, Dogwood, temporal policies, guardrails, policy sessions)", org: "Amazon Web Services", year: 2026, surface: products}
{type: docs, ref: https://docs.aws.amazon.com/verifiedpermissions/latest/apireference/API_PolicyItem.html, title: "AWS Verified Permissions — PolicyItem (effect, scope; no statement body)", org: "Amazon Web Services", surface: products}
{type: docs, ref: https://dogwood-policy.github.io/dogwood/index.html, title: "Dogwood — Cedar-compatible policy language with temporal conditions and information providers", surface: active-dev}
```

**Source signal:** `external-scan` (targeted verification, owner-directed question).
