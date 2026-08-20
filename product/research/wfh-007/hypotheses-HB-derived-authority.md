# hypotheses — H-B · derived authority: resource × intent × consequence

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · **agent_id:** `wfh-007-hB-hypothesizer`
**Partition:** the uncovered three-way join — no candidate in ~59 does *resource × intent × consequence* with per-caller authority. Owner's structural read carried and attacked: two legs are actor-independent (resource is enforceable by a credential-less plane; consequence is a property of the action), one is not (intent is the actor's own assertion) — so the legs may have to be layered by trust, not evaluated as a flat tuple.
**Firewall:** every item below is an unproven conjecture, `claimed` at most. Nothing here is a verdict, grade, or ranking. Zero graph writes.
**Settled ground not re-derived:** phase-indexed authority = TBAC/WAM; gate independence = gate-input independence (never "soundness"); HRU undecidability and RMP NP-hardness bound every least-privilege claim to decidable fragments.

Use-case throughout is **Jurati Core** (OWNER-DIRECTION §4), with the garage and the Unimatrix software-delivery workflow as the two concrete programs.

---

## A. What the derivation function derives *from* — five distinct source artifacts

### H1 — Derive the ceiling from the cross-program work contract itself
**Statement.** The demand-derived-ceiling pattern (WASI/Bazel/Nix/in-toto/`gh aw compile`, settled) could enhance Jurati's cross-program delegation capability by treating the **work contract of §8 as the build manifest**: its fields (objective, bounded deliverable, resources intentionally disclosed, authority delegated, budget, expiry) compiled into a sandbox profile + forge permissions + Unimatrix write scope before the called program's first token is generated.
**Mechanism.** The contract already enumerates resources and delegated authority as *fields*; a deterministic compiler over those fields is the same shape as `gh aw compile` emitting `permissions:` blocks — the input artifact is new, the derivation move is settled.
**Cheapest test.** Hand-derive profiles from 3–5 past runs' scope documents (wfh-005, wfh-007, jurati-001) and count the escape hatches each would have needed. If a research contract structurally cannot enumerate its resource set in advance (open-web discovery), the derivation under-determines — killing it for the research program while possibly sparing software delivery.
**Risk.** Assumes contracts are authored before work starts, i.e. the owner clears one more artifact per delegation. Risk: the compiler becomes a place where a generous default quietly re-creates ambient authority.
**Class:** obvious · **linear** · **Clusters:** C, merged §13 · **Attention:** one contract per delegation; near-zero if the contract is already required.

### H2 — Derive per-role ceilings statically from the protocol file, once, at protocol-authoring time
**Statement.** Static analysis of `.claude/workflow/*.md` + `.claude/agents/factory/*.md` could emit each role's ceiling **when the protocol is authored**, not when the run starts — the Bazel move: the BUILD file declares, the run only selects.
**Mechanism.** The protocols already state, in prose, who writes what (scouts read-only, curator sole writer, leader never generates content). Those sentences are ceiling declarations no plane currently consumes. One-time compilation to per-role sandbox profiles + per-role MCP tool lists turns S5's "phase-as-process (config selection, not minting)" into exactly what ships.
**Cheapest test.** Compile `theme-scan` by hand into per-role profiles; run one scout under its profile; count violations of legitimate work. OpenShell's static/dynamic split says which parts must be per-spawn vs per-turn — but its hot-reload latency/atomicity is **unpublished** (round-two trigger #1), the load-bearing unknown.
**Risk.** Assumes phase boundaries coincide with agent spawns (they mostly do here). Risk: prose→profile compilation drifts silently — the compiled profile becomes Cluster H unless a check diffs them.
**Class:** obvious · **linear** · **Clusters:** A, C · **Attention:** one review per protocol version, amortized over every run.

### H3 — Pure-drop derivation: phases only ever shed authority (pledge semantics)
**Statement.** OpenBSD-`pledge`-style monotone shedding could make the derivation function trivially safe: a run starts at the union of its phases' needs and each transition only drops; any phase needing *more* is not a transition but a **fresh spawn under a fresh derivation** — so widening never occurs inside a trust boundary.
**Mechanism.** Monotone-drop makes the transition function unable to escalate by construction; the spawn boundary relocates all widening to the one place (creation) where the static planes already enforce.
**Cheapest test.** Audit past runs' phase sequences: count transitions that genuinely needed re-widening (research→poc does). If >0 — and it is — the hypothesis survives only in the spawn-per-phase form, whose cost is measurable: spawn latency × phases per run.
**Risk.** "Start at the union" makes the *first* phase over-privileged — Granite's 46.6% failure re-created at run granularity; the fix (spawn-per-phase throughout) must be priced.
**Class:** adjacent · **linear** · **Clusters:** A, C · **Attention:** zero new gates; possibly fewer.

### H4 — Intent as an appended caveat on a Biscuit/IBCT chain: laundering by token mechanics
**Statement.** IBCT/macaroon caveat mechanics could make the intent declaration a **first-hop appended block that cryptographically may only narrow** the root grant — widening fails verification, so an untrusted intent assertion becomes structurally unable to add authority.
**Mechanism.** Measured and shipped: chained IBCT verifies in 0.049 ms (Rust), catches delegation-depth violation and audit-evasion-via-empty-context. The trust asymmetry lands exactly where the owner's read puts it: the two actor-independent legs live in the root, the actor's leg lives in the part that can only subtract.
**Cheapest test.** Wire Biscuit tokens through the Unimatrix JS/TS shim for one run: root = role ceiling, first caveat = declared phase intent; measure overhead and count rejected calls.
**Risk.** Assumes a verifier at each plane (the shim can verify; the OS sandbox cannot read tokens — so this covers MCP/graph actions only). Single-author protocol, no venue; and see H5 for what the attacker does *instead* of widening.
**Class:** adjacent · **step-function** if it works across programs · **Clusters:** C, D · **Attention:** none per-action; one signing ceremony per run.

---

## B. Monotone attenuation — developed, then attacked

### H5 — The under-declaration attack: narrowing launders escalation through the escalation channel
**Statement.** Monotone attenuation could *degrade* the owner-gate capability unless paired with an **escalation-budget meter**: an agent that under-declares intent fails visibly, triggers a human ceiling-raise, and converts the owner's approval channel into a fatigue-driven rubber stamp — the attacker gains not authority but *a habituated approver*.
**Mechanism.** Approval fatigue is the settled compliance-budget result (#191(d)); Nextcloud deleting its capability scoping under p99 pressure is the structural analogue. The counter-mechanism is cheap: count ceiling-raises per run/per class as a first-class audit metric, and make raise-frequency itself a gate input.
**Cheapest test.** Instrument past and next runs for "would have needed a raise" events; near-zero base rate ⇒ the meter is dead weight; high rate ⇒ monotone attenuation as designed is unusable and the derivation function is under-scoping.
**Risk.** The meter is itself a Cluster-H candidate — a metric nobody reads.
**Class:** non-obvious · **linear** · **Clusters:** C, H, G · **Attention:** proposes spending review attention on raise-*frequency* instead of per-raise content.

### H6 — Narrowing is the wrong move for compensation: mint the compensator grant *with* the action grant
**Statement.** The Saga limit could invert attenuation at one point: a compensable action is admissible **only if its compensation credential already exists** — derivation emits action-grant and compensator-grant as a pair, because the undo often needs authority ⊇ the do, and "intent may only narrow" would otherwise make every failure unrecoverable in-band.
**Mechanism.** Revisable-by-Design's taxonomy plus autogenous's shipped rule ("irreversible mutations are inadmissible — no rollback target, no admission") generalized: no rollback *credential*, no admission. The compensator grant derives from the consequence lookup (actor-independent leg), so it does not re-open the intent trust hole.
**Cheapest test.** Enumerate this repo's consequential actions (`context_correct`, `context_deprecate`, git push, Issue comment); for each write the compensator and its required authority; count cases where compensator-authority ⊋ action-authority.
**Risk.** Compensators are enumerable for graph and git; not for external sends. The compensator channel is a standing wider credential — an escalation surface that must be single-purpose and unforgeable or it becomes the new ambient authority.
**Class:** non-obvious · **step-function for autonomy** (recoverability is what earns §5.7 trust graduation) · **Clusters:** B, C.

### H23 — Attack the layering itself: consequence is only actor-independent under single-writer discipline
**Statement.** The owner's premise "consequence is a lookup, not an assertion" could fail under concurrency — Revisable-by-Design proves conflicting *compensable* actions impose unavoidable cost, i.e. a compensable action becomes effectively irreversible when a concurrent actor consumes its output — so the consequence leg silently degrades from lookup to runtime evaluation **unless a single-writer discipline holds**. The garage's curator rule is therefore not audit hygiene but the *condition under which the trust-layering is valid*.
**Mechanism.** Consequence class is a function of (action, state, other actors). Fix the other-actors term to one writer and the state term to append-mostly stores, and the class collapses back to a per-action property.
**Cheapest test.** Construct one concrete inversion inside current discipline: `context_correct` on a node another live agent holds a stale id for (D5 says the stale read is *marked deprecated* — the design already compensates). If no inversion is constructible inside the graph/repo, the layering is safe on owned planes and inverts only on external effects — H9's residue.
**Risk.** This quietly makes single-writer a load-bearing architectural invariant that growth pressure will want to relax.
**Class:** non-obvious/whitespace · **step-function as a design constraint** (it decides §8's federation question from the consequence side) · **Clusters:** B, D.

---

## C. Multi-plane enforcement — plane-per-leg, and what falls between

### H9 — Assign each leg the plane whose trust property matches it
**Statement.** Three legs enforced by three planes that already exist at ~zero cost: **resource → OS sandbox** (credential-less, actor cannot address it), **consequence → forge** (branch protection + required checks convert an irreversible push into a compensable PR — the forge is a consequence-*transformer*, not just a gate), **intent → the Unimatrix write path** (we own the server; the write path can check the declared phase against the registered run).
**Mechanism.** The owner's layered-by-trust read made physical: the assertion-shaped leg gets the plane we fully control and can audit; the actor-independent legs get planes the actor holds no credential for.
**Cheapest test.** Enumerate the full effect surface of one real run (every syscall class, git verb, graph call, network send) and mark which plane sees each. The residue is the finding either way.
**Risk — the known residue.** **External sends** (HTTP POST, email, Issue comment) touch only the OS egress allowlist, which is resource-shaped — an irreversible send to an *allowed* domain is invisible to all three consequence-aware planes. Plane-per-leg reads as complete and is not; the residue is exactly the owner's "public representation" boundary (§5.5).
**Class:** adjacent · **step-function** (smallest version of §11.5 that could run this quarter) · **Clusters:** A, B, D · **Attention:** near-zero new gates.

### H10 — The forge as the consequence plane: role-scoped credentials × path-scoped rulesets
**Statement.** GitHub's free machinery could give each role its **own credential** (deploy key or GitHub-App installation) with rulesets scoped by path/branch: the research role's key pushes only `research/*`; merge to `main` requires the validator's independent check. Required checks give gate-input independence for free — CI evaluates the commit, not the agent's report of it.
**Mechanism.** Today every agent shares the owner's credential, so the forge sees one principal and per-caller authority is impossible *at that plane*. Splitting credentials is the entire delta; the policy language already exists and Cluster G's survivor (Home Assistant) runs its whole ecosystem on exactly this plane.
**Cheapest test.** Mint two deploy keys, scope by ruleset, attempt the forbidden push from the wrong key. One afternoon; a demonstrated refusal.
**Risk.** Whether rulesets express per-actor-per-path at the needed granularity is **unverified**; if not, the plane's authority stops at branch names. Repo-shaped only.
**Class:** obvious · **linear** · **Clusters:** A, G, H · **Attention:** zero recurring.

### H11 — The Unimatrix write path as the intent plane
**Statement.** Owning the memory server could enable something unique among the 59 candidates: `context_cycle` registers the run's roles and phases, and the write path rejects a `context_store` from a caller whose registered role is scout — "scouts don't write" enforced where the write lands, not where it is asked for.
**Mechanism.** The MCP interception point is ours and the walls are liftable; nobody in the scan owns their store's write path. Intent is cross-checked against a second party's earlier assertion — weaker than cryptographic, stronger than self-report.
**Cheapest test / falsifier already on file.** **D6 — `agent_id` does not persist; writes record `created_by: anonymous`.** Until the transport carries unforgeable caller identity (per-role tokens on the shim — H4's degenerate form), this plane's authority stops at the honesty of a self-reported string. Test: add per-role bearer tokens; verify the server can distinguish two callers.
**Risk.** Enforcing in the server couples Jurati's policy to one store — provider-neutrality cuts against baking policy into Unimatrix rather than in front of it.
**Class:** adjacent · **step-function** — first per-caller authority anywhere in the estate · **Clusters:** C, H · **Attention:** one token per role, zero per-action gates.

### H12 — Jurati Core as *only* the residue router between planes
**Statement.** Enumerate what each free plane cannot see (OS: semantics; forge: non-repo effects; Unimatrix: filesystem and network), and hypothesize Jurati's smallest trusted core as a **routing table from effect-class to responsible plane, plus one escalation channel for unmapped effects** — no evaluator, no policy engine, no sandbox: those exist; only the mapping and the default-escalate are unowned.
**Mechanism.** Every candidate builds a plane; none builds the assignment *between* planes. §9's seam needs exactly one new component under this reading: the router, which is a table and therefore auditable, diffable, owner-legible.
**Cheapest test.** Build the table for the first vertical slice on paper. If the residue column is empty for real runs, Jurati Core has no enforcement job in slice 1 and the join is pure configuration — a decisive, cheap, either-way answer to §14 Q5.
**Risk.** A table is the easiest artifact to leave stale (Cluster H); it needs a check that diffs it against the observed effect surface.
**Class:** non-obvious/whitespace · **step-function** — reframes "build the join" as "own the seams between joins others built" · **Clusters:** A, B, C, D, G.

---

## D. The consequence leg — how an action gets a class, and who is trusted to say

### H7 — Consequence as an owner-curated registry; unclassified ⇒ tightest resource cell
**Statement.** Consequence as a **lookup against an owner-curated registry** (never the tool author — MCP hints are advisory by spec; never the caller — that is the intent hole), with the load-bearing choice at the default: an **unclassified action runs, but only inside the resource plane's tightest cell** — unclassifiability converts into confinement instead of into a prompt.
**Mechanism.** Legs substitute for each other: where consequence has no answer, resource tightens. This keeps the compliance budget unspent while making the dangerous default structurally cheap to trigger and useless to exploit. Arbitrary bash — the one unclassifiable family — gets exactly this treatment, which is what the OS sandbox already does.
**Cheapest test.** Classify the 15 `context_*` tools + ~10 git/gh verbs on the four-class taxonomy; measure authoring cost per action; project to domain N+1. **Cluster-E warning:** whoever must author classifications for domain N+1 determines who can add domain N+1 — if only the owner can classify, the registry is a growth bottleneck by construction.
**Risk.** State-dependence (H8's falsifier).
**Class:** adjacent · linear alone; **step-function combined with H13** · **Clusters:** B, E, A.

### H8 — Verify consequence declarations by demonstration: run it, reverse it, diff
**Statement.** A class label is a **falsifiable claim with a mechanical test** — idempotent: run twice, diff state; reversible: run + undo, diff; compensable: run + compensate, measure residue — so classifications are demonstrated, not asserted, closing the gap Cluster B names (Apple enforces but doesn't verify; MCP doesn't even enforce; *nobody verifies the declaration*).
**Mechanism.** Property-based testing over the action registry, in a scratch namespace/branch; autogenous already ships the receipt shape (signed `RollbackReceipt` after confirming hash and health).
**Cheapest test.** Pick five `context_*` tools and write the reversal probe for each. **Immediate falsifier:** consequence may be **state-dependent, not action-dependent** (`context_deprecate` on a node with dependents vs without) — if class varies per state, the registry entry must carry a predicate, and the lookup leg gets more expensive than the owner's read assumes.
**Risk.** A probe proves the class on tested states only; claiming more re-imports the assertion problem one level up.
**Class:** non-obvious · **step-function** — would be the first verified consequence declaration in any surveyed system · **Clusters:** B, D.

### H13 — Grade consequence classes on the firewall ladder itself
**Statement.** Every classification gets a grade: tool-author hint = `claimed`; demonstrated probe (H8) = `partial`; probe + production reversal actually exercised = `proven` — and policy strictness keys off the *grade*, e.g. a merely-`claimed` "reversible" is treated as irreversible for authority purposes.
**Mechanism.** Reuses the garage's one original running asset on a new claim type; conservative-by-grade means unverified optimism costs the agent authority rather than costing the owner risk. Graydon–Holloway supports the ordinal form and warns off numeric — this stays ordinal.
**Cheapest test.** Zero new machinery: express three classifications as `finding` nodes with grades in a scratch namespace (rate limit ~60 tag-writes/hr bounds any bulk sweep).
**Risk.** Two ladders (evidence grade, consequence class) compose into a matrix the owner must hold in their head; if it needs a spreadsheet, it fails the personal-scale test.
**Class:** adjacent · **linear** · **Clusters:** B, D.

---

## E. Semantic phase boundaries with no credential to mint (Class 2 — the jurati wedge)

### H14 — Project the semantic boundary onto the graph's type system
**Statement.** The Unimatrix write path could enforce S5's Class-2 examples without any credential existing to mint, because the semantic distinction is already a **typed distinction in the graph**: "the design role may propose a capability but not mutate the goal" = allow (`capability`, `context_store`) and deny (`goal`, `context_correct`) for that role — the meaning lives in the category/operation pair, so the filter is the credential.
**Mechanism.** D8 already restricts edge types globally for everyone; per-role restriction is the same check with one more key. The semantics "no syscall can see" are first-class node types at this plane.
**Cheapest test.** Take S5's two verbatim examples plus §8's open questions and try to express each as a write-path predicate. Count the residue. **Known residue:** "may not change the success bar" where the bar is a field *inside* node content — content-level semantics need a diff-checker (#263 territory), not a type filter.
**Risk.** Assumes caller identity at the write path (H11's dependency — D6 must close first). Boundaries drift into content as the ontology matures, eroding the projectable fraction.
**Class:** adjacent · **step-function for the wedge** — cheapest mechanism anyone has named for a Class-2 boundary · **Clusters:** C, D, singleton 1.

### H15 — Capability-safe code emission for the semantic residue: the ceiling as lexical scope
**Statement.** The Odersky-line capture-checking result could handle exactly the boundaries H14 cannot project: the agent **emits code into a restricted interpreter where the phase's capability objects are the only names in scope** — the research role's interpreter contains no `push` object to reference, and the type system proves the emitted code reaches only what it was handed. The no-credential-to-mint problem becomes a lexical-scope problem, which compilers solved decades ago.
**Mechanism.** *Capabilities: Effects for Free* (ICFEM 2018): effect bounds from type-checking alone; the 2026 agent application reports no significant task-performance loss. The degenerate version needs no Scala: a restricted eval where the tool objects passed in *are* the ceiling.
**Cheapest test.** One afternoon: restricted JS/Python eval harness with two tool objects injected, ask the model to do a scout task, count (a) capability escapes attempted, (b) task-quality loss on our workload — the published no-loss claim is on their benchmarks, not garage tasks.
**Risk.** Interpreter escape hardening is a real engineering tail; the honest framing is that this buys *semantic* granularity the OS sandbox structurally cannot express, at the cost of owning an interpreter.
**Class:** non-obvious · **step-function if it holds** — it collapses the intent leg into the resource leg (declared intent literally *selects the scope*, and the scope is then actor-independent) · **Clusters:** A, C; literature C4.

### H16 — CaMeL-style data-flow labels make the contract's disclosure fields enforceable
**Statement.** CaMeL's capability-metadata-on-values could make the contract's information-flow fields enforceable by attaching the disclosure list as **taint labels on the disclosed values themselves**, so onward disclosure is checked by dataflow rather than by trusting the called program's restraint.
**Mechanism.** In CaMeL a privileged planner emits code into a restricted interpreter carrying capability metadata on every value and enforcing policy on flows — the one published design that defeats the confused deputy *and* the rug-pull class. Here the labels are minted from contract fields — an actor-independent source.
**Cheapest test.** Label one real cross-program round trip at coarse granularity and replay its actual flows; count label-lattice blowup and needed declassifications. **The CaMeL primary was never fetched by any scout (S5's declared hole) — fetch it before anything leans on this.**
**Risk.** Highest of any hypothesis here; also the only mechanism in this file that addresses the owner's *exposure* failure class at the semantic level.
**Class:** non-obvious · **step-function for cross-program trust** · **Clusters:** C; S5 steelman.

### H17 — An IFC reading of §6's failure classes bounds what deterministic policy can ever cover
**Statement.** Mapping the failure classes onto IFC primitives yields a principled cut: *deletion* and *corruption* = integrity (no low-trust writer to high-trust store — Biba-shaped, enforceable on the two planes we own); *exposure* = confidentiality (no labeled value to a public channel — BLP-shaped, enforceable at egress); *misleading* and *bad advice* = provenance/evidence properties **with no IFC analogue** — they are the notary's job and cannot be bought with any authority mechanism.
**Mechanism.** Three of five owner failure classes reduce to label checks on graph + repo + egress; the irreducible two are the completion-record problem. The join, at its best, covers three-fifths of §6 — a bound worth having *before* triage prices it.
**Cheapest test.** Coarse-label the wfh-007 corpus (public/internal/sensitive) and replay the run's actual flows against the two label rules; count violations and false positives on a run known benign.
**Risk.** The mapping flatters the join by assigning it the tractable classes; the owner's hardest classes are the two it cannot touch.
**Class:** non-obvious/whitespace · linear as machinery, **step-function as a scoping instrument** · **Clusters:** D; §6.

---

## F. Aggregation — forty years old, unsolved; partial and ugly mitigations on purpose

### H18 — Consequence budgets: execution-count bounds per class per run
**Statement.** IBCT's budget-ceiling field, repurposed from money to consequence, bounds each class per run: **0 irreversible without escalation; N compensable; unbounded idempotent** — not a solution to Denning's problem, but a hard cap on the worst trajectory's damage, with C9's shape as a bonus (execution-count bounds are velocity-independent, D ≤ n, where TTL bounds scale O(v·TTL) — and a local agent fleet is the high-velocity case).
**Mechanism.** A per-run counter at whichever plane sees the action class; the ceiling is set in the root grant (actor-independent).
**Cheapest test.** Back-test: replay past runs' action logs against candidate budgets; count false triggers on benign runs vs coverage of the known failure inventory.
**Risk — known miss, stated plainly.** Exfiltrate-by-many-small-reads is N actions all individually idempotent — cross-class trajectories sail under any per-class budget. This buys a floor, not safety.
**Class:** obvious · **linear** · **Clusters:** B, C (C9).

### H19 — Trajectory checking at commit-review time over the typed write-set
**Statement.** Relocate aggregation from runtime prevention (undecidable-adjacent, forty years unsolved) to **cycle-review-time detection over a finite typed write-set**: a deterministic reducer over the run's nodes/edges/commits evaluates trajectory invariants — "no run may both lower a finding's grade and deprecate its contradicting finding," "no run may widen an authority table and consume the widening" — because at review time the trajectory is a bounded, typed, inspectable object.
**Mechanism.** `context_cycle_review` already exists as the hook; Cluster D's cost signal points exactly here — a *deterministic checker over a typed record* is the shape six regimes kept when they walked away from human verification. Detection suffices where the reversible planes make undo real.
**Cheapest test.** Write five trajectory invariants and back-test against past cycles: real violations caught, false positives, known-bad patterns missed. An afternoon of reducer code against exports.
**Risk.** Invariants must be enumerable in advance — the classic assurance-case limit; unknown-unknown trajectories pass. Detection-after-commit is too late for the irreversible residue (external sends again).
**Class:** adjacent · **step-function** — the only aggregation mitigation compatible with both the throughput evidence and the firewall's existing shape · **Clusters:** D, C, G.

### H20 — Taint-coupled derivation: past actions feed future ceilings (Rule-of-Two made continuous)
**Statement.** Aggregation's nastiest personal-scale instance (read-sensitive-then-send) could be structurally forbidden rather than detected by **coupling the legs across time**: an action that reads a sensitive class *narrows the resource ceiling* for the remainder of the run (egress drops to none), so the trifecta is broken continuously by derivation — consequence of past actions becomes an input to the resource derivation of future ones.
**Mechanism.** Meta's Rule of Two generalized from a static design constraint into a dynamic derivation rule; the OS sandbox and OpenShell both make network the hot-reloadable layer, exactly the layer this needs to move mid-run.
**Cheapest test.** (a) the OpenShell/sandbox hot-reload latency+atomicity question — already round-two trigger #1, this raises its value again; (b) count, in past runs, how often legitimate work needed read-sensitive-then-egress in one session — the utility cost is the real falsifier.
**Risk.** Assumes sensitivity labels exist (H17's labeling pass is a prerequisite). The mitigation teaches an agent to split work across sessions to shed taint — session boundary becomes the new laundering surface unless taint follows the contract, not the process.
**Class:** non-obvious · **step-function for the exposure failure class** · **Clusters:** A, C; S5 §3.

---

## G. Whitespace — the join as something other than an engine

### H21 — The join as a mandatory record format first, an engine never (or later, and derived from data)
**Statement.** The three-way join could enter the estate as **bookkeeping, not enforcement**: every action's (resource-touched, declared-intent, consequence-class) triple becomes a mandatory field of the append-only run record, checked lazily by the validator at the gate — and the derivation function is later *learned from the accumulated records* (which ceilings would have sufficed) rather than designed a priori. Enforcement planes are retrofitted only where the record shows they would have fired.
**Mechanism.** Cluster D's cost evidence applied to ourselves: across six regulated regimes, the machine-readable declaration half survived every cost-cutting pass and the human verification half was abandoned. Declare-first-enforce-later is what the best-measured field on earth converged to. It also answers "what does the derivation derive from" with the only actor-independent source not yet on the list: *our own history* — the same move as the Microsoft/Amazon patents (observation-derived ceilings), but observed from records we already trust.
**Cheapest test.** Add the triple to one run's records by hand; measure authoring friction and whether the validator's gate can consume it. Near-free.
**Risk.** The meta-risk is Cluster H verbatim: a record nobody checks is a control that is present, believed, and inert — mitigated only if at least one required check reads the record from day one. Second: observation-derived ceilings ratify past over-privilege (the patents' known weakness).
**Class:** non-obvious/whitespace · linear now, and it *purchases the data* that decides whether any step-function engine is justified · **Clusters:** D, H · **Attention:** lowest of any hypothesis here.

### H22 — Trust-layering as evaluation *order* inside an engine already routed ASSEMBLE: intent may only DENY
**Statement.** The owner's layering could be implemented as a **discipline over Cedar (#202) rather than a build**: resource and consequence facts populate principal/action/resource; intent goes in the `context` slot nobody fills — under one lint rule: *policies referencing `context` may appear only in `forbid` rules, never `permit`*. A forged or mistaken intent can subtract authority but structurally cannot contribute to an ALLOW — monotone restriction achieved by evaluation position, with zero token machinery.
**Mechanism.** In a flat tuple the untrusted leg co-signs permits; pinning it to forbid-only makes the trust asymmetry a syntactic property of the policy set, checkable by a linter rather than a runtime.
**Cheapest test.** Two hours: write three policies in Cedar's playground with intent-in-context, confirm forbid-overrides-permit composes as needed, and check whether "context only in forbids" is mechanically lintable. If yes, the intent leg of the entire partition reduces to *one lint rule over an ASSEMBLE verdict already on file*.
**Risk.** **Cedar semantics unverified this run** — no scout read Cedar's evaluation order. Forbid-only intent cannot express "this phase permits X that others don't" (positive phase grants must come from the actor-independent legs — arguably correct discipline, but it must be a choice, not an accident).
**Class:** adjacent · linear machinery, **step-function economy** (it may delete a build) · **Clusters:** C; #202.

---

## Flags for the leader

1. **Unverified load-bearing specifics:** Cedar evaluation-order/lintability (H22) — no scout read it this run; OpenShell/sandbox hot-reload latency+atomicity (H2, H20) — already round-two trigger #1, three hypotheses raise its price; CaMeL primary still unfetched (H16) — S5's declared hole, now load-bearing twice.
2. **Dependency spine:** H11 and H14 both hang on closing **D6** (unforgeable caller identity at the Unimatrix write path). If triage takes either, the per-role-token shim change is the common prerequisite and is itself a bounded, testable object.
3. **Instrument caveat carried:** all scouts hit the shared 200/200 cap; nothing above treats any surface as exhausted.
4. **Single-operator caveat, stated not ignored:** the S4 anti-correlation and the Nextcloud deletion both warn that non-structural checks die under pressure. For a single-operator estate the author-supply arm may not bind for ~2 years, but the Cluster-E reframe (who authors classifications for domain N+1 — H7) is where it re-enters, and every hypothesis above that adds per-action work was written to be structural (config, type, scope, or record) rather than latency-priced.

---

## The strongest argument against building the three-way join at all

**The evidence this run gathered does not show authority failing; it shows review failing and self-reporting failing.** Cluster G found the measured bottleneck at both real operating scales was *the rate at which a human can review what the machine produced*, and the join adds gates — spending the one resource the evidence says is binding. Meanwhile the harms actually documented at personal scale sort entirely into the two legs that are already free or already ours: the largest real credential harm (s1ngularity, 1,079 systems) is fully covered by the resource leg alone — a filesystem sandbox that is installed, credential-less, zero-ops; Home Assistant's decade at 668k installs produced *no* capability-scoping failure of an authenticated principal; and the failure class both large corpora rank highest and rising — fabricated success reports — is untouchable by any authority mechanism, because a true completion and a fabricated one are the same write by the same uid. On that record, the intent and consequence legs are two-thirds of a solution to a harm nobody has documented at this scale (S5 searched for the counter-instance and found absence), while the actually-unowned object is the notary. Worse, Cluster H says a built-but-unexercised join doesn't merely waste effort — six instances across four codebases show it becomes a control that is present, believed, and inert, which is *negative* safety, because it purchases misplaced trust. And Nextcloud shows the endgame under operational pressure: the per-action check was the thing deleted to save p99. The disciplined conclusion: take the free resource plane, spend the build budget on the completion-record problem, and let the intent×consequence legs enter — if at all — as H21's passive record until the records themselves demonstrate a fire that an enforcement plane would have caught.

**The counterweight, so triage hears both:** the owner's endgame (§2, §6 — finance, health, public representation, progressive autonomy) is precisely the regime where latent authority harm stops being latent, trust graduation (§5.7) *requires* per-class action records to even be recommendable, and several hypotheses above (H10, H13, H14, H21, H22) price the join at configuration-and-record rather than engine — at which cost the argument against loses most of its force while keeping all of its warning.

---

## Compact list

| # | One-line statement | Class | Target capability |
|---|---|---|---|
| H1 | Compile ceilings from the §8 work contract | obvious | cross-program delegation |
| H2 | Compile per-role ceilings from protocol files at authoring time | obvious | phase-indexed authority |
| H3 | Pledge-style pure-drop transitions; widening = fresh spawn | adjacent | phase transitions |
| H4 | Intent as an attenuation-only Biscuit/IBCT caveat | adjacent | intent leg, cross-program |
| H5 | Under-declaration launders escalation via approval fatigue; meter raises | non-obvious | owner gate integrity |
| H6 | Compensator grant minted with the action grant | non-obvious | consequence / recoverability |
| H23 | Consequence is a lookup only under single-writer; curator rule is load-bearing | whitespace | federation / write discipline |
| H9 | Plane-per-leg: OS=resource, forge=consequence, Unimatrix=intent | adjacent | multi-plane enforcement |
| H10 | Role-scoped forge credentials × path rulesets | obvious | semantic phase boundary (repo plane) |
| H11 | Unimatrix write path enforces role via cycle registration | adjacent | per-caller authority (graph plane) |
| H12 | Jurati Core = the residue router between existing planes | whitespace | smallest trusted core |
| H7 | Owner-curated consequence registry; unclassified ⇒ tightest resource cell | adjacent | consequence leg |
| H8 | Verify consequence classes by demonstration (run/reverse/diff) | non-obvious | consequence verification |
| H13 | Grade consequence classes on the D7 ladder; policy keys off grade | adjacent | consequence trust |
| H14 | Semantic boundaries as role→(category, edge, op) triples at the write path | adjacent | Class-2 boundaries (jurati wedge) |
| H15 | Capability-safe code emission; ceiling as lexical scope | non-obvious | Class-2 residue |
| H16 | CaMeL taint labels mint from contract disclosure fields | non-obvious | cross-program information flow |
| H17 | IFC mapping of §6 failure classes bounds what policy can cover | whitespace | criticality scoping |
| H18 | Per-class consequence budgets, execution-count bounded | obvious | aggregation (floor) |
| H19 | Trajectory invariants checked over the typed write-set at cycle review | adjacent | aggregation (detection) |
| H20 | Taint-coupled derivation: sensitive reads narrow future egress | non-obvious | aggregation / exposure |
| H21 | The join as mandatory record format; enforcement retrofitted from data | whitespace | evidence-first entry path |
| H22 | Intent may only DENY: forbid-only context discipline over Cedar | adjacent | intent leg at near-zero build |
