<!--
Factory scope template (D4 + D7). Copy into product/research/{scope-id}/SCOPE.md and into the
GitHub Issue body. One scope = one Issue = one context_cycle topic ({goal-tag}-NNN).
Delete these comments when filling in.
-->

# {SCOPE-ID} — {subject}

**Status:** SCOPE  <!-- scoped → researching → [feasibility] → synthesis → done -->
**Goal(s):** {primary goal} (primary){ · secondary goals}
**Capability target(s):** {capability name(s) + Unimatrix id(s) — the queue item this scope advances}
**Confidence-required:** directional | empirical | validated  <!-- D7: sets target status + proof bar -->
**Phase / area:** {grouping tag}
**Cycle topic / Issue:** {scope-id}  <!-- = context_cycle topic = GitHub Issue # -->

---

## The question

{2–3 sentences framing what this scope investigates.}

> {One-sentence blockquote core — the single question, sharp.}

## Why it matters

{How answering this advances the goal / the vision.}

## Known constraints & prior art  *(build on these — do not re-derive)*

- {Constraint, prior finding, or reusable technology already in the Unimatrix library.}
- {Search the `technology` library FIRST and list what to reuse, so nothing is re-researched.}

## Bounded investigation (workstreams)

Each workstream is one researcher's partition. State an explicit `Output:` per workstream.

- **W1 — {name}.** {Question.} *Output:* {the deliverable}.
- **W2 — {name}.** {Question.} *Output:* {the deliverable}.

## Expected output (FINDINGS.md)

1. {Enumerated, concrete deliverable.}
2. {…}

## Proof bar  *(D7 — what would move status)*

- **directional scopes:** *Structure-only — no status change.* Produces findings + `claimed`
  technologies + a `position` recommendation. May *spawn* follow-on validated scopes.
- **empirical / validated scopes:** the artifact that moves a technology to `partial` / `proven`,
  **at the claim's altitude** (runtime → benchmark; integration → smoke test; theoretical →
  reproduction) and **demonstrated by us** (literature/citation never proves — stays `claimed`).

## Explicitly out of scope

- {The boundary. Makes "is a discovered gap mine or a new scope?" mechanical (D3).}

## Coverage / done call  *(synthesis)*

Loop-until-dry: stop when **K** consecutive searches surface no new technology **and** **≥N**
independent findings corroborate the leading candidate. Agent proposes "sufficient"; **human
confirms** at the synthesis gate.

---

<!-- Amendments are append-only (D3). Never overwrite a validated verdict; explicitly reconcile any
this extension changes. -->
## Extension ({YYYY-MM-DD}): {title}

{Why this extension; added workstreams; which prior verdicts it reconciles or revises.}
