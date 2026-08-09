# Jurati product-authority control wedge

**Status:** PROPOSAL · options and evaluation agenda, not an architecture decision  
**Date:** 2026-08-09  
**Purpose:** define the smallest useful enforcement problem for Jurati and Unimatrix: protect product
vision and the capability roadmap behind one authenticated product principal, then use the result to
evaluate broader three-party workflow control.  
**Builds on:** `jurati-evolved-vision-2026-08-05.md`, `workflow-harness-scope-recut.md`, the current
Unimatrix goal/capability graph, and the `jurati-001` lesson that deterministic consequence is useful but
does not by itself establish delivery quality.

---

## 1. The problem

The current garage and Unimatrix SDLC already separate product, design, and delivery in their procedures.
Those boundaries are not security boundaries. Role files and prompts say who should author, implement, and
approve, while the effective process often shares credentials, filesystem authority, tool access, and a
self-declared `agent_id`.

An implementation agent can therefore be instructed not to alter its success bar without the platform
being able to prove or enforce that restriction. A differently named subagent is not independent if it
inherits the same undifferentiated authority. Deterministic transition logic only helps after trustworthy
criteria and verdicts exist; it does not prevent an agent from weakening criteria, manufacturing evidence,
or reaching a resource through an unmediated path.

The first enforcement target should be deliberately narrow:

> Bind product vision and the capability roadmap to one authenticated product principal, and demonstrate
> that every other principal—including delegated children—can read the approved surface but cannot create,
> alter, regrade, supersede, relink, or indirectly replace it without product authorization.

This wedge protects the upstream definition of success before attempting to govern every tool or delivery
operation.

## 2. The larger three-party model

The eventual model has three accountable principals:

| Principal | Owns | Must not be able to do alone |
|---|---|---|
| **Product** | vision, goals, outcome alignment, approval that the capability map covers the goal | implement delivery or attest design conformance |
| **Design** | capability proposals, specifications, acceptance/evidence contracts, conformance review | silently narrow product intent or implement and approve the same delivery |
| **Delivery** | implementation and evidence produced inside an approved authority envelope | change goals, capability bars, protected checks, approvals, or workflow state |

Product and design collaborate on the delivery contract. Product approves that the proposed capabilities
and success criteria cover the vision. Design approves that an artifact conforms. Product separately
approves that the result remains aligned with the product outcome. Jurati advances only when the contract's
required approvals refer to the same immutable contract, artifact, evidence bundle, and workflow attempt.

This proposal does **not** attempt to implement that whole model. It uses the product surface as the first
place to prove identity, delegation, authorization, denial, and audit semantics.

## 3. What exists today

Unimatrix has useful substrate:

- an administrative enrollment operation that can associate an agent identifier with trust and coarse
  capabilities such as read, write, search, and admin;
- typed knowledge categories including `goal` and `capability`;
- mutation surfaces for store, correction, tags, edges, and lifecycle operations;
- a graph that already represents product goals, capability decomposition, proof grades, and provenance;
- MCP and hook integration points through which agent activity can be observed or mediated.

These are ingredients, not the required control:

- `agent_id` is presently caller-supplied and is not a cryptographically authenticated principal;
- durable attribution is incomplete, so a claimed identity is not reliable audit evidence;
- enrollment grants coarse engine capabilities, not category-, field-, edge-, phase-, or attempt-specific
  authority;
- generic write authority can reach multiple mutation paths;
- Unimatrix cannot restrict filesystem, Git, shell, network, secret, or alternate tool paths it never sees;
- a hook is not an enforcement boundary when the acting process can bypass, replace, or disable it.

Jurati could extend this substrate by establishing principals and signed workflow context, then asking
Unimatrix to enforce graph-local policy while other enforcing planes control external effects.

## 4. The first protected surface

The wedge protects two related but distinct objects.

### 4.1 Product-owned goal

Only the enrolled product principal, or a child holding a valid product delegation, may:

- create or correct a goal;
- change its outcome statement, boundary, priority, or lifecycle;
- approve a capability-coverage proposal against it;
- authorize a replacement or supersession.

### 4.2 Design-proposed, product-approved capability roadmap

Design may propose capability nodes, behavioral `done_when` bars, and `Advances` links. Those proposals do
not become the approved roadmap until the product principal signs the coverage set against a specific goal
and graph digest.

After approval:

- design may not silently change the bar; it must submit an amendment;
- delivery has no mutation authority over goals, capabilities, their grades, or their approved edges;
- product may approve or reject an amendment, but should not impersonate design conformance;
- proof-grade advancement remains a separate evidence/firewall operation, not a side effect of product
  ownership.

This avoids collapsing product and design into one role while still linking the roadmap to one accountable
product principal.

## 5. Identity and delegation model to evaluate

Enrollment should evolve from registering a claimed name to binding a principal record to verifiable key
material. A principal record minimally needs:

- stable principal ID and public key;
- principal class (`product`, `design`, `delivery`, `harness`, or administrative);
- trust state, issue time, expiry, and revocation state;
- authorized workflow/project scope;
- the issuer and evidence supporting enrollment.

Subagents should act **for** a main principal without becoming indistinguishable from it. A parent signs a
short-lived delegation containing:

- child key or session identity;
- parent principal and complete delegation chain;
- workflow instance, phase, task, and resource scope;
- allowed operations and explicit exclusions;
- expiry, nonce, and maximum delegation depth.

Effective child authority is the intersection of parent authority, role policy, workflow phase, and the
delegation. A delivery child cannot acquire product authority by naming itself a product reviewer.

Whether every ephemeral child needs a durable registry entry is open. The invariant is not “register every
process forever”; it is “every effect is attributable to a verifiable principal plus delegation chain.”

## 6. Authorization must cover every mutation path

A category ACL on `context_store` would be an incomplete demonstration. The policy decision needs to cover:

- storing a competing goal or capability;
- correcting or superseding an existing entry;
- changing `grade:` or other privileged tags;
- adding, removing, or redirecting `Advances`, `Prerequisite`, or other relevant edges;
- deprecating, quarantining, or restoring entries;
- attaching an approval, proof envelope, or replacement;
- attempting the same effects through a child, alternate session, or replayed credential.

A useful authorization request is therefore closer to:

```text
(authenticated principal, delegation chain, workflow/phase/attempt,
 operation, category, entry/field/edge target, proposed content digest,
 contract/policy version, nonce, time)
```

The decision must be enforced by the component holding the useful credential or mutation capability. An
agent-readable denial is useful feedback; it is not the enforcement mechanism.

## 7. Where control could live: options to evaluate

The proposal deliberately keeps several architectures open.

### Option A — Unimatrix-local authorization

Unimatrix authenticates the caller and enforces product/design/delivery policy in every graph mutation
handler.

**Strength:** the graph protects itself even if callers or hooks are compromised.  
**Limit:** it governs only Unimatrix; delivery can still act through filesystem, Git, network, and other
services.

### Option B — one universal ecosystem hook evaluated by Jurati

Every agent tool request enters one hook. The hook sends the authenticated request and trusted workflow
context to Jurati, which permits, denies, or requires escalation.

**Strength:** one policy decision point, one visible audit stream, and a fast route to test cross-tool
policy.  
**Questions that must be proved rather than assumed:**

- Can every useful effect actually be forced through the hook?
- Who owns the credentials, and can the agent call the underlying service directly?
- Can shell, plugins, child agents, alternate MCP clients, or a second session bypass it?
- What is the safe behavior when Jurati is slow or unavailable?
- Can policy change between decision and use (time-of-check/time-of-use)?
- How are hook integrity, recursion, bootstrapping, and Jurati administration protected?

A universal hook is a plausible policy decision seam. It is a security boundary only when it is also a
non-bypassable enforcement seam.

### Option C — Jurati-issued capabilities, locally enforced

Jurati authenticates workflow principals and issues short-lived, resource-specific capabilities. Unimatrix,
Git, filesystem brokers, network gateways, and secret stores validate those capabilities locally.

**Strength:** policy is coordinated while enforcement stays next to each resource; outages and revocation
can be bounded explicitly.  
**Limit:** more integration work and the risk that enforcement semantics drift between planes.

### Option D — hybrid

Unimatrix protects its own graph mutations; Jurati establishes workflow identity and delegation; a common
hook observes and routes requests; resource-local brokers enforce capabilities for effects outside
Unimatrix.

This is the strongest current candidate, not a decision. The wedge should produce evidence that lets us
reject unnecessary layers or demonstrate why they are required.

## 8. Proposed first proof

### 8.1 Build only enough to protect one product surface

1. Enroll one product principal with verifiable key material.
2. Enroll or derive distinct design and delivery principals.
3. Bind one goal and its approved capability-roadmap digest to the product principal.
4. Permit design to submit capability proposals and amendments.
5. Require the product signature to approve the roadmap or an amendment.
6. Deny delivery goal/capability mutations through every Unimatrix mutation path.
7. Issue one bounded child delegation for each principal and test inheritance and attenuation.
8. Record signed allow/deny decisions with policy version, target digest, attempt, and delegation chain.

No shell, Git, network, or secret mediation is needed to prove this first graph-local boundary. Those planes
remain explicit holes, not implied coverage.

### 8.2 Attack it deliberately

The experiment should include:

- delivery creates a competing goal;
- delivery corrects, supersedes, tags, deprecates, or relinks an approved capability;
- delivery replays an old product approval against a changed roadmap;
- delivery spawns a child named as product or design;
- a product child exceeds its delegated target or expiry;
- design changes an approved `done_when` without a product amendment signature;
- an attacker substitutes a different artifact, graph, workflow attempt, or policy version;
- direct Unimatrix access bypasses the proposed Jurati hook;
- Jurati or the hook is unavailable;
- legitimate design proposal and product approval complete without administrative intervention.

### 8.3 What to measure

- unauthorized attempts denied / attempted, by mutation path;
- unauthorized state changes that nevertheless commit (**critical: target zero**);
- false denials of legitimate product/design operations;
- bypass paths found, including alternate clients and child delegation;
- replay, expiry, revocation, and cross-attempt isolation;
- attribution completeness: committed effects with a verifiable principal and delegation chain;
- approval binding: signatures verified against the exact goal, roadmap, policy, and attempt digests;
- decision latency and availability impact;
- administrative recovery cost and lockout risk;
- policy complexity and enforcement-plane count.

The proof succeeds only if the protected graph is unchanged after every unauthorized attempt, every
legitimate operation remains possible through the declared path, and the audit record can attribute both
allows and denials without trusting caller-supplied names.

## 9. Staged expansion if the wedge works

1. **Product surface:** authenticated product owner; protected goals and approved capability roadmap.
2. **Design contract:** immutable acceptance, evidence, and amendment contract jointly bound to product and
   design.
3. **Delivery graph authority:** delivery may submit artifact/evidence references but cannot approve,
   regrade, or alter its bar.
4. **Tool mediation:** derive phase/task capabilities and test the universal-hook and resource-local
   enforcement options.
5. **External planes:** Git paths, filesystem, secrets, network egress, compute, deployment, and child-agent
   creation.
6. **Two-key advancement:** independent design-conformance and product-alignment signatures over the same
   attempt; Jurati alone executes the transition.

Each stage needs its own demonstrated attack artifact. Success in Unimatrix does not imply filesystem or
network isolation.

## 10. Non-goals of the first proof

- solving general agent sandboxing;
- choosing Jurati's implementation language or deployment topology;
- proving one universal hook can mediate the ecosystem;
- autonomous product judgment;
- replacing human product approval;
- using an LLM's claimed role as authentication;
- treating signature validity as evidence that a decision is substantively good;
- protecting every Unimatrix category before the goal/capability wedge is understood.

## 11. Decisions this evaluation must enable

The result should let us decide:

1. Can Unimatrix extend enrollment into authenticated principals without becoming the workflow identity
   authority, or should Jurati issue identities and Unimatrix only validate capabilities?
2. Is product ownership best represented as category policy, entry ownership, signed approval over a graph
   digest, or a composition of all three?
3. Can one hook become a sole path in the target agent ecosystems, or is it necessarily advisory without
   resource-local enforcement?
4. Which policy belongs in Jurati and which invariant must each resource defend locally?
5. How should break-glass administration work without giving an everyday administrator silent product
   authority?
6. What child-identity granularity preserves accountability without making delegation unusable?
7. Which attacks or legitimate workflows make the small wedge too narrow to teach us anything?

## 12. Immediate next action

Turn this proposal into a bounded validated scope only after reviewing the product/design ownership split
and the attack matrix. The first artifact should be an authorization probe around one disposable goal and
capability roadmap—not a production identity migration and not a general Jurati gateway.

The desired outcome is evidence about the enforcement architecture. A successful demo of signed messages
without denied real mutations is insufficient.

---

<!-- This proposal expands the option space. Architectural decisions belong in Unimatrix only after the
evaluation settles them. -->
