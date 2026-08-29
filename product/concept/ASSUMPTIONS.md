# Component Architecture — Assumptions

Input artifact for the component-architecture run. **Logical only.** An assumption names something the
architecture must accommodate; it never names a vendor, product, library, or protocol. "Model router" is
an assumption. "LiteLLM" is not.

Two tracks (Claude and Codex) consume this file unchanged and each produce an independent component
model. Convergence is by hand afterward. Neither track may edit this file — amendments are append-only
and owner-authorized.

---

## Why assumptions and not requirements

A requirement says what to build. An assumption says what must remain true while we work out what to
build. The component model is the *answer*; this file is the set of things the answer may not violate.

Much of this is already established in the `workflow-harness` theme evidence. Where it is, the
assumption **cites** it rather than re-deriving it — the architect treats it as settled input, not as a
question to reopen.

---

## Schema

```yaml
- id: A##
  type: capability | constraint | structural | evolution
  statement: <one sentence — what must be true or possible>
  basis: owner-declared | evidence-backed | provisional
  provenance: <where this is already established, or `owner-new`>
  implies: <the LOGICAL capability this demands — the component seed>
  variability: <what must be swappable or able to change without redesign>
  not_this: <technology/product choices this assumption does NOT make>
  falsifier: <what would show this assumption is wrong>   # optional
```

**The four types, and why the distinction is load-bearing** — each produces a different architectural
consequence, and conflating them is how a component model turns into a wish list:

| type | what it produces |
|---|---|
| `capability` | a **component** — something must do this |
| `constraint` | a **boundary or placement** — where a thing may or may not sit |
| `structural` | **topology** — how components relate |
| `evolution` | a **seam** — where change is expected and must not require redesign |

**The three bases, and what each licenses the architect to do:**

- `owner-declared` — take as given. Do not relitigate. May be *interpreted*, never challenged.
- `evidence-backed` — established by a cited run or finding. Challengeable only with contrary evidence.
- `provisional` — the owner's current belief, explicitly open to challenge. Say so if it doesn't hold.

**`not_this` is mandatory on every capability assumption.** It is the guard that keeps a logical
architecture logical. If you cannot state what technology choice the assumption is *not* making, the
assumption is written at the wrong altitude.

---

## Worked examples

```yaml
- id: A01
  type: capability
  statement: Work can be routed to different model providers and to locally operated models, and the
    routing decision is made outside the work being routed.
  basis: owner-declared
  provenance: target-concept-v1.md §Build vs Buy, §Determinism vs Non-deterministic
  implies: a logical model router — a placement point that selects an execution target per unit of
    work, and is not itself selectable by the work it routes
  variability: providers appear and disappear; the local/remote mix shifts toward local over time;
    no component above the router may know which target served it
  not_this: no gateway product, no proxy, no inference server, no provider, no local runtime chosen
  falsifier: a unit of work whose correctness depends on which target executed it

- id: A02
  type: constraint
  statement: Consequential governance and effect credentials sit outside the activity they govern;
    an agent cannot alter the rules constraining it during execution.
  basis: owner-declared
  provenance: target-concept-v1.md §Determinism vs Non-deterministic; themes.md workflow-harness lens
  implies: a control plane whose placement is outside every governed actor, holding effect credentials
  variability: what is governed grows over time; the placement must not
  not_this: no policy engine, secret store, or identity system chosen
  falsifier: a governed actor that can reach its own constraint definition at runtime

- id: A03
  type: capability
  statement: Programs communicate with one another — a finding in one program reaches another program
    that can act on it.
  basis: evidence-backed
  provenance: target-concept-v1.md §Structure/Methodology (garage → Unimatrix bugs); wfh-011 — V5 has
    NO construct for cross-Scope delivery; `Signal` was excluded into `Event`, and Events belong to a
    single Scope
  implies: a cross-program communication path with addressing and delivery, distinct from a program's
    internal event record
  variability: the number of programs is unbounded and unknown in advance
  not_this: no bus, queue, protocol, or message format chosen
  falsifier: cross-program need shown to be adequately served by shared storage alone

- id: A04
  type: constraint
  statement: Deterministic capability is preferred wherever it can carry the required semantics;
    non-deterministic reasoning is used where it adds value, never where a deterministic check exists.
  basis: owner-declared
  provenance: target-concept-v1.md §Determinism vs Non-deterministic
  implies: every gate or check has a declared determinism altitude, and mechanical checks are
    distinguishable from judgment at the point of use
  variability: the deterministic/non-deterministic boundary moves as capability improves
  not_this: no rules engine, validator, or model class chosen
  falsifier: a governance decision where determinism is achievable but demonstrably not desirable

- id: A05
  type: structural
  statement: Intent, constraints, consequential decisions and institutional memory are centralized;
    reasoning, exploration, planning, communication and reversible execution are distributed.
  basis: owner-declared
  provenance: themes.md workflow-harness lens; target-concept-v1.md §Structure/Methodology
  implies: a topology with a small centralized core and an unbounded distributed edge, and a stated
    rule for which side any new capability lands on
  variability: the edge grows without bound; the core must not grow proportionally
  not_this: no orchestration framework or repository topology chosen
  falsifier: a capability whose correct placement cannot be decided by the rule

- id: A06
  type: evolution
  statement: Capabilities we cannot currently name (a finance team, e.g.) must be addable without
    redesigning the organization.
  basis: owner-declared
  provenance: target-concept-v1.md §Build sequence
  implies: capability formation is itself a modeled process, not a schema change
  variability: the set of capabilities is open; the mechanism for adding one is closed
  not_this: no plugin system, registry implementation, or repo layout chosen
  falsifier: a plausible new capability that cannot be expressed without new common structure
```

---

## Coverage frame

The set is complete when every axis below holds at least one assumption, or is explicitly declared a
hole with the reason. Axes are `target-concept-v1.md`'s own sections, so the concept document is a
first-class input rather than background reading.

| Axis | Source section |
|---|---|
| Organization & structure | §Structure/Methodology |
| Communication pathways | §Structure/Methodology |
| Structured autonomy & authority | §Governance, §Determinism |
| Execution pathways | §Structure/Methodology, §Build sequence |
| Governance & checks/balances | §Governance/Checks and balances |
| Durable memory & cross-program learning | §Structure/Methodology |
| Security seams | §Security |
| Determinism boundary | §Determinism vs Non-deterministic |
| Provider & runtime flexibility | §Build vs Buy |
| Capability formation | §Build sequence |
| Cross-disciplinary recombination | §Core Principle |

An axis with no assumption is a **declared hole**, named as such. Silence is not coverage.

---

## Rules for both tracks

1. **Logical only.** No vendor, product, library, protocol or repository choice. If a component's name
   implies a technology, rename it.
2. **Cite, do not re-derive.** Where an assumption is `evidence-backed`, the cited run settled it.
3. **A challenge is welcome and must be explicit.** A `provisional` assumption you believe is wrong gets
   a named objection with a reason — not a silent workaround in the model.
4. **Do not resolve an assumption by narrowing it.** If A01 is inconvenient, that is a finding.
5. **Independence.** Neither track reads the other's output before convergence.

<!-- Amendments are append-only and owner-authorized. Never overwrite an assumption; supersede it explicitly. -->
