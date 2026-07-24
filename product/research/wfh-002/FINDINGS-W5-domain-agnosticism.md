# FINDINGS — W5: Second-domain round-trip (the research method itself)

**Workstream:** W5 — Domain-agnostic vs SDLC-locked · **Scope:** `wfh-002` (Issue dug-21/arch-research#46) · **Agent:** `wfh-002-w5-researcher`
**Status:** structure-only. No grades asserted. This tests whether the v0.2 vocabulary is domain-neutral by round-tripping a *second, non-software* domain — the garage's own research method — through the same 5 nodes / 4 edges.

---

## §0 Method & honesty pre-registration

**Source of truth (prose design, NOT `.claude/`):** `docs/research-factory-methodology.md` (the funnel, phases §7/§14, firewall §3, grading §3/§6, roles §14.1, telemetry §10, process plane §8/§9); `product/factory/themes.md` (garage funnel: wide mouth → neck → proving grounds); `CLAUDE.md` Mission. I read the `.claude/*` implementation in W1/W2 only; here I deliberately did **not** derive from it — the whole validity of W5 depends on expressing the *abstract* method, because our research workflow happens to be *authored* as coding-agent config, and pointing the vocabulary at that config silently re-tests the software domain.

**Spec under test:** v0.2 = W1's 5 nodes (`skill · agent-def · step · gate · tool`) + 4 edges (`invokes · depends-on · gated-by · injects`), **with the W2 minimal fixes folded in**: activation-as-set, a `condition` guard, `arbiter:{program|human|agent}`, bytes-canonical P-B, a human principal (`agent-def{kind:human}`), `envelope_closed`, `scope.precedence`, `effect` compound/unknown. I test against the *repaired* spec so a gap here is a v0.3 finding, not a re-litigation of W2.

**Pre-registered non-force-fits** — constructs I commit to FLAGGING rather than bending into a node type if they don't type cleanly:
1. **The evidence-grade ladder** (`missing→claimed→partial→proven`) — the method's central object. If it lands only as an opaque string in `step.output` / `gate.predicate`, I say so; I will **not** mint a 6th `knowledge`/`artifact` node type.
2. **Budget / the compute envelope** — if there is no home for a standing resource constraint, I flag it, not squeeze it into a gate and call it done.
3. **Loop-until-dry** (the coverage convergence rule) — if `depends-on` (a DAG) and `gate.failure_handling` can't express a convergence iteration, I flag the missing loop construct.
4. **The two-plane / reflexive meta-structure** (factory improves itself under its own firewall) and **the GitHub Issue as a stateful human channel** — flag if they fall outside the workflow-definition plane rather than pretending an edge covers them.

**Contrarian stance (CLAUDE.md):** the interesting result is a real hole. I actively hunted under-reach and SDLC leakage rather than confirming H4.

---

## §1 The expressed graph

Conventions per W2: `A -edge(params)-> B`; every node carries an opaque byte-preserved body per P-B; `source_ref` is the prose section it derives from (this domain has no `.claude` file backing — a point I return to in §3).

### 1.1 skill nodes (9) — injected instruction / standing policy

```yaml
skills:
  - {name: firewall-rule,        activation: always, owner: user, source_ref: methodology§3 + CLAUDE.md-Mission,
     note: "the cardinal rule: status→proven ONLY on attached real artifact. Injected into every role. Its ENFORCEMENT is a gate (firewall-gate); this skill is the REQUEST half."}
  - {name: methodology,          activation: always, owner: user, source_ref: methodology(whole),
     note: "the operating manual; the composite-step bodies (§1.3) are projections of it"}
  - {name: grading-discipline,   activation: scoped,  owner: user, source_ref: methodology§3/§6,
     scope: {applies_to: [curator, validator], precedence: closest-wins},
     note: "the missing/claimed/partial/proven ladder + carrier rules (grade is a tag, not status). The LADDER ITSELF is domain data the vocabulary cannot type — G-W1."}
  - {name: coverage-rule,        activation: matched, owner: user, source_ref: methodology§6,
     note: "loop-until-dry: stop when K consec searches surface no new tech AND ≥N findings corroborate. The K/N predicate injects fine; the ITERATION it governs does not type — G-W3."}
  - {name: cardinal-write-rule,  activation: always, owner: user, source_ref: methodology§14.1,
     scope: {applies_to: [factory-researcher, factory-curator, all-specialists]},
     note: "researchers read-only + produce files; curator is sole graph writer. Deny-side is a gate; this is the request half."}
  - {name: confidence-altitude,  activation: matched, owner: user, source_ref: methodology§15(D7),
     note: "directional|empirical|validated sets a scope's target status; firewall is altitude-aware (theory by reproduction, never citation). Feeds firewall-gate.predicate + rs-feasibility.condition."}
  - {name: three-surfaces,       activation: always, owner: user, source_ref: methodology§14.5,
     note: "files=provisional / graph=settled / Issue=live. The Issue surface does not type as a node — G-W5."}
  - {name: factory-git,          activation: [matched, explicit], owner: user, source_ref: methodology§8 + factory-git-skill,
     note: "two-stream (method vs research); wf:vX.Y derived via git describe, never hand-typed"}
  - {name: budget-discipline,    activation: always, owner: user, source_ref: methodology§14.6,
     note: "'within budget'; bites in feasibility. No resource-envelope construct exists — G-W2."}
```

### 1.2 agent-def nodes (10) — principals / roles (methodology §14.1)

```yaml
agent_defs:
  - {name: research-leader,   type: coordinator, source_ref: §14.1,
     capability_envelope: {tools: [context_cycle, git, gh, Task(spawn)], closed: true},
     note: "context_cycle ONLY; never generates content. envelope_closed=true (W2 S7 fix used)."}
  - {name: factory-researcher, type: specialist, source_ref: §14.1,
     capability_envelope: {tools: [context_search, context_get, context_graph], closed: true, mode: read-only},
     produces: "FINDINGS file"}
  - {name: factory-curator,   type: specialist, source_ref: §14.1,
     capability_envelope: {tools: [context_store, context_correct, context_tag, context_edge, context_search], closed: false},
     note: "the ONLY node writer; firewall-bound; the files→graph bridge"}
  - {name: factory-poc,       type: specialist, source_ref: §14.1,
     capability_envelope: {tools: [build/compute/repo], closed: false},
     note: "the only compute-spending principal; writes artifacts to git, no graph access"}
  - {name: factory-validator, type: specialist, source_ref: §14.1,
     capability_envelope: {tools: [Read], mode: read-only}, produces: "gate report FILE",
     note: "verifies the artifact is real; its verdict arbiters the firewall gate → arbiter:agent (W2 G-A fix used)"}
  - {name: factory-retro,     type: specialist, source_ref: §14.1 + §8/§9,
     capability_envelope: {tools: [context_store, context_correct, context_cycle_review], plane: process}}
  - {name: goal-owner,        type: specialist, scope: advisory, source_ref: §14.1 + §14.3,
     note: "DUAL role: (A) synthesis relevance/drift/under-reach review; (B) theme-scan triage (park/probe/build). Two step-assignments, one def — no strain."}
  - {name: scout,             type: specialist, scope: exploratory, source_ref: themes.md(wide-mouth),
     capability_envelope: {tools: [WebSearch, WebFetch, context_search], mode: read-only}}
  - {name: hypothesizer,      type: specialist, scope: exploratory, source_ref: themes.md(wide-mouth),
     note: "divergent application generator; range-rewarded; never grades"}
  - {name: human-principal,   kind: human, source_ref: §14.5/§14.6,
     note: "W2 S6 fix used. Acts AND arbiters: pairs on scope, confirms coverage, reviews synthesis, replies on the Issue, kicks Wave-0. Without kind:human, theme-scan and every advisory gate has no actor."}
```

### 1.3 step nodes — the funnel (composite steps per W1 §2.2)

```yaml
steps:
  - name: garage-funnel                    # top composite; source_ref: themes.md "the garage funnel"
    invokes: [theme-scan, decompose-scope, research-scope]
    note: "concept→trial→proof; wide mouth → neck → proving grounds"

  # --- WIDE MOUTH + NECK ---
  - name: theme-scan                       # source_ref: themes.md + methodology(garage)
    children:
      - {name: ts-scan,        assigned: scout,        output: "candidate technologies (claimed)"}
      - {name: ts-hypothesize, assigned: hypothesizer, output: "application hypotheses (finding+hypothesis tag)"}
      - {name: ts-triage,      assigned: goal-owner,   output: "park/probe/build cut; promoted proof-goal",
         gated_by: triage-gate}
    depends_on_chain: ts-scan -> ts-hypothesize -> ts-triage
    note: "structure-only; nothing graded here (firewall not yet applied)"

  # --- PROVING GROUNDS: board build ---
  - name: decompose-scope                  # source_ref: §7/§14.2 (first two phases)
    children:
      - {name: ds-scope,     assigned: factory-researcher, output: SCOPE.md, gated_by: scope-gate}
      - {name: ds-decompose, assigned: [factory-researcher, factory-curator],
         output: "business capability + nfr nodes (missing/claimed) + Advances/About edges"}
    depends_on_chain: ds-scope -> ds-decompose

  # --- PROVING GROUNDS: per-capability research ---
  - name: research-scope                   # source_ref: §7/§14.2
    children:
      - {name: rs-scope,          assigned: factory-researcher,
         output: "SCOPE.md (goal-questions, breadth, confidence-required, constraints, prior-art)",
         gated_by: scope-gate}
      - {name: rs-tech-discovery, assigned: [factory-researcher xN parallel, factory-curator],
         output: "FINDINGS files + technology(claimed) + finding(Motivates,cites) nodes",
         gated_by: coverage-gate,
         note: "curator self-briefs the technology library FIRST → reuse, not re-research (§14.4). This 'reuse-first' has no edge — see §3."}
      - {name: rs-feasibility,    condition: "confidence-required >= validated",     # W2 G-B fix used — types cleanly
         assigned: [factory-poc, factory-validator, factory-curator],
         output: "verified artifact + technology→proven/partial (proven_by set)",
         gated_by: [firewall-gate, budget-gate],
         note: "the ONLY compute-spending step; directional scopes skip it entirely via the condition"}
      - {name: rs-synthesis,      assigned: [factory-curator, goal-owner],
         output: "position finding + capability→proven where done_when clears + REPORT.md",
         gated_by: synthesis-gate}
      - {name: rs-close,          assigned: [research-leader, factory-retro],
         invokes: [context_cycle, context_cycle_review, git],
         output: "cycle stop + lesson-learned + factory-plane A/B entries"}
    depends_on_chain: rs-scope -> rs-tech-discovery -> [rs-feasibility] -> rs-synthesis -> rs-close

  # --- REFLEXIVE PLANE (the factory improving itself, §8/§9) ---
  - name: process-ab-loop                  # source_ref: §8 self-enhancement loop
    children:
      - {name: pa-lesson,   assigned: factory-retro, output: "lesson-learned"}
      - {name: pa-edit,     assigned: human-principal, output: "workflow edit committed as wf:vN"}
      - {name: pa-measure,  assigned: research-leader, invokes: [context_cycle_review],
         output: "version-sliced yield: wf:vN vs wf:vM"}
      - {name: pa-verdict,  assigned: factory-curator, gated_by: process-firewall-gate,
         output: "factory/technology → proven (proven_by: A/B telemetry) OR revert"}
    depends_on_chain: pa-lesson -> pa-edit -> pa-measure -> pa-verdict
    note: "the SAME step/gate/role types, pointed at the factory itself. Reflexivity expresses as a self-referential step graph — but the PLANE ISOLATION that makes it safe is a property of the knowledge graph, not the workflow — see §3, G-W4."
```

### 1.4 gate nodes (7)

```yaml
gates:
  - {name: triage-gate,    trigger: step-boundary, arbiter: human(goal-owner), blocking: blocking,
     effect: "promote 0..n (park/probe/build)", source_ref: themes.md-neck}
  - {name: scope-gate,     trigger: step-boundary, arbiter: human, blocking: advisory, effect: ask,
     source_ref: §14.2/§14.3}
  - {name: coverage-gate,  trigger: step-boundary, arbiter: [agent(leader), human(confirm)], blocking: blocking,
     predicate: "K consec searches no new technology AND >=N corroborating findings  [LOOP predicate — G-W3]",
     effect: deny-until-pass,
     failure_handling: {rework_target: prior-phase, retries: 2, escalation: SCOPE-FAIL}}
  - {name: firewall-gate,  trigger: step-boundary, arbiter: [agent(factory-validator), curator-rule], blocking: blocking(MANDATORY),
     predicate: "grade→proven ONLY IF a real artifact attached in proven_by, AT the claim's altitude, demonstrated BY US  [references the grade ladder + altitude = domain data — G-W1]",
     effect: deny, source_ref: §3/§14.2,
     note: "the load-bearing gate of the whole method. Types as a gate; its DECISION RULE reduces to prose because grade/altitude/artifact are untyped."}
  - {name: budget-gate,    trigger: "step-boundary + CONTINUOUS (spend accrues across the whole run)", arbiter: program,
     predicate: "cumulative spend < cap", effect: halt, source_ref: §14.6,
     note: "STRAINED: budget is a standing envelope on every autonomous step, not a discrete checkpoint. The CAP is definition; the SPEND is runtime (P-C). — G-W2."}
  - {name: synthesis-gate, trigger: step-boundary, arbiter: human, blocking: advisory,
     inputs: "goal-owner relevance/drift/under-reach verdict, relayed VERBATIM (leader may not act on it)",
     source_ref: §14.3}
  - {name: process-firewall-gate, trigger: step-boundary, arbiter: program(telemetry), blocking: blocking,
     predicate: "wf:vN yield > wf:vM by comparative A/B  [the process-plane firewall — proof is an A/B, not a POC]",
     effect: deny, source_ref: §8/§9,
     note: "the firewall applied to the process axis. Same gate type; predicate again references graded state."}
```

### 1.5 tool nodes (5 classes) — the instruments

```yaml
tools:
  - {name: knowledge-base, provider: mcp,
     interface: "context_search/get/graph/lookup (read); context_store/correct/tag/edge (write, curator-only)",
     note: "the compounding asset. Types as a callable capability — but the KB is ALSO durable cross-session STATE, which 'tool' does not model — see §3."}
  - {name: cycle,          provider: mcp, interface: "context_cycle {start,phase-end,stop} + context_cycle_review",
     note: "connective tissue: goal-conditioned briefing + telemetry + phase signal + wf: stamp carrier"}
  - {name: capability-board, provider: "derived-view (a context_graph subgraph query)",
     interface: "context_graph(subgraph, seed:goal, edge:Advances/Prerequisite)",
     note: "'what's done is a QUERY, derived never stored'. Types awkwardly: an instrument whose value is a live derived result, not a stateless call."}
  - {name: vcs,            provider: platform, interface: "git (two-stream, wf-vX.Y tag), gh",
     note: "version-stamps the workflow definition; blast-radius scoping for process defects"}
  - {name: issue,          provider: platform, interface: "GitHub Issue: body=scope, comments=gates/approvals",
     note: "the live human↔factory channel. A STATEFUL CONVERSATION, not a stateless call — types poorly as 'tool' — G-W5."}
  - {name: poc-env,        provider: "build/compute", interface: "repo + runtime",
     note: "where feasibility spends real compute and the proof artifact is produced"}
```

### 1.6 edges (complete classes)

```yaml
edges:
  injects:
    - firewall-rule        -> ALL agent-defs            # the cardinal rule everywhere
    - methodology          -> ALL agent-defs
    - grading-discipline   -> [factory-curator, factory-validator]
    - cardinal-write-rule  -> [factory-researcher, factory-curator, all specialists]
    - coverage-rule        -> [factory-researcher, research-leader]
    - budget-discipline    -> ALL agent-defs
    - three-surfaces       -> [research-leader, factory-curator]
  invokes:
    - garage-funnel   -> [theme-scan, decompose-scope, research-scope]        # composite → children
    - research-leader -(spawn)-> [factory-researcher, factory-curator, factory-poc, factory-validator, goal-owner, factory-retro]
    - research-leader -(must)->  [cycle, vcs, gh]
    - each phase step -(assign)-> its principal(s)      # step → agent-def
    - rs-* / ds-* steps -(call)-> [knowledge-base, cycle, poc-env]   # step → tool
    - ts-triage       -(assign)-> goal-owner
    - human-principal -(initiate)-> [theme-scan, rs-scope]           # human as actor (S6)
  depends-on:
    - the 5 phase chains in §1.3 (theme-scan, decompose-scope, research-scope, process-ab-loop)
    - NOTE: the loop-until-dry iteration inside rs-tech-discovery is NOT drawable here (DAG only) — G-W3
  gated-by:
    - ts-triage        -> triage-gate
    - ds-scope/rs-scope-> scope-gate
    - rs-tech-discovery-> coverage-gate
    - rs-feasibility   -> [firewall-gate, budget-gate]
    - rs-synthesis     -> synthesis-gate
    - pa-verdict       -> process-firewall-gate
```

---

## §2 Round-trip bar

**Judged the way W2 judged its behavioral bar (can the operating behavior be reconstructed from the graph?): PASS-WITH-GAPS.**

What reconstructs cleanly from the graph alone: the funnel topology (wide mouth → neck → proving grounds), all 10 roles and their capability envelopes, the phase order and the conditional skip of feasibility, which principal produces what, which step each gate guards, the single-writer discipline (only `factory-curator` has write tools), and the reflexive process loop as a self-referential step graph. An engineer handed only the graph could re-run the method's *choreography*.

What does **not** reconstruct — and this is the same failure shape W2 found, sharpened by the domain: **every one of the method's *defining* decision rules collapses into an opaque `gate.predicate` string.** The firewall's altitude-matched-artifact rule, the coverage rule's K/N convergence, the budget cap, and the grade-transition logic are the *reason the method exists*, and none of them is typed structure — they are prose the graph carries but cannot represent. You can reconstruct *that there is a mandatory blocking gate at feasibility*; you cannot reconstruct *what it actually checks* without reading the body. Per P-A this is the request-not-guarantee weakness, and the research domain stresses it harder than SDLC because the research domain's control-flow branches on **evidence grade** — a typed concept the vocabulary refuses to model (§3, G-W1).

Verdict: **pass-with-gaps** — the behavior is reconstructable at the choreography level, lossy at the decision-rule level.

---

## §3 Domain-fit analysis (the core of W5)

### Node-type usage

| Node type | Instances | Load-bearing here? | Notes |
|---|---|---|---|
| `skill` | 9 | **Yes** | The method's SOPs (firewall rule, grading discipline, coverage rule, git conventions) are exactly "reusable instruction given to an actor." Clean neutral reading = *instruction*. |
| `agent-def` | 10 | **Yes** | 10 distinct roles; the coordinator/specialist split and capability envelopes are pure org-chart. Neutral reading = *actor/principal*. |
| `step` | ~20 (5 composites) | **Yes** | Phases and sub-steps; cleanest of the five — *action/stage* is domain-free. |
| `gate` | 7 | **Yes** | The firewall — the method's whole point — **is** a gate. Neutral reading = *binding checkpoint*. Strong agnosticism signal. |
| `tool` | 6 | **Yes, with strain** | All instruments are load-bearing, but 3 of 6 strain (board = derived view; KB = also state; Issue = conversation). Neutral reading = *instrument*, but the field vocabulary is SDLC (see leakage). |

**No node type is unused.** This is the single strongest domain-agnostic signal: an over-fit-to-SDLC vocabulary would leave a type dead in a non-software domain (nothing to point it at). Every one of the five carries independent load in the research method, and each has a clean neutral reading — *actor / action / checkpoint / instrument / instruction* — which is the universal skeleton of *any* workflow.

### Edge usage

| Edge | Instances | Load-bearing? | Notes |
|---|---|---|---|
| `invokes` | ~15 | **Yes** | spawn (leader→specialists), assign (step→role), call (step→tool), composite→children — all four senses used. |
| `depends-on` | 5 chains | **Yes** | phase ordering. But **DAG-only**: cannot draw the loop-until-dry iteration (G-W3). |
| `gated-by` | 7 | **Yes** | every phase→its gate; the firewall is the exemplar. |
| `injects` | 7 | **Yes** | the cardinal rule / grading discipline / budget discipline injected into all roles — the request half of every policy. |

All four edges carry load. `depends-on` is the only one that hit a wall (no cyclic/convergence form).

### Failed-to-type constructs (the most important findings — hunted hard)

- **G-W1 — the evidence-grade ladder (`missing→claimed→partial→proven`).** *The method's central object does not type.* It is neither actor, action, checkpoint, instrument, nor instruction — it is the **graded knowledge state** the workflow produces and branches on. It lands only as an opaque string inside `step.output` and `gate.predicate`. This is defensible *as far as it goes* — the vocabulary is a workflow-*definition* vocabulary (P-C), and domain data (like source code in SDLC) is legitimately out of plane. **But here is the sharp, non-obvious finding:** unlike SDLC, the research method's *control-flow branches on this untyped state*. The firewall gate's verdict IS "is the grade proven-eligible?"; tech-discovery's output IS "claimed nodes"; the whole funnel is a state machine over the grade ladder. SDLC hides this because its control-flow branches on things the vocabulary *does* reference (a test result surfaces as a `gate` verdict; a PR as a `vcs-action` trigger). Research **exposes** it: the workflow's decisions depend on typed domain state the vocabulary has no way to name, so the method's core logic is unreconstructable from structure. This is **under-reach**, not SDLC-lock — but it is the deepest hole W5 found.

- **G-W2 — budget / the resource envelope.** "Within budget," "budget bites in feasibility," "cost per proven capability" — a *standing constraint on every autonomous step*, plus a *metered runtime quantity*. There is no construct for a resource envelope. Forcing it into `budget-gate` is a lie of altitude: a gate is a discrete checkpoint; budget is ambient and continuous. The cap is definition-plane (could be a gate constant); the accruing spend is runtime (P-C). Genuinely homeless, and **domain-agnostic-relevant** — every autonomous or long-running workflow has a resource envelope.

- **G-W3 — loop-until-dry (convergence iteration).** The coverage rule is "repeat tech-discovery until K consecutive dry searches AND ≥N corroborations." That is a *while-loop with a convergence predicate*. The vocabulary has no iteration: `depends-on` is an acyclic DAG, and `gate.failure_handling` (W2's G-E fix) models a *bounded rework retry*, which is a different shape (retry-on-failure ≤2, not iterate-until-converged). "Researched enough" — the method's definition of research-done — is therefore unexpressible as typed structure. **Domain-agnostic-relevant:** any exploratory/search/sampling workflow has convergence loops.

- **G-W4 — the two-plane reflexive structure.** The factory improving itself under its own firewall (§8/§9) expresses *partially*: the `process-ab-loop` step graph reuses the same step/gate/role types (a good sign — reflexivity doesn't break the vocabulary). But the **plane isolation** that makes it safe (category filter + factory→factory-only edge discipline) is a property of the *knowledge graph*, not the workflow, so it falls outside the workflow-definition plane entirely. The vocabulary cannot express "this workflow operates on a sealed subgraph." Arguably correctly out of plane — flagged, not forced.

- **G-W5 — the GitHub Issue as a stateful human channel.** The Issue is "the live human↔factory interface — human inputs originate here." It is neither a stateless `tool` call nor a `gate`; it is a *durable conversation medium* where structure moves both ways. Typed as `tool{provider:platform}` it loses everything that matters about it (statefulness, bidirectionality, that human inputs *originate* rather than *return* there). W2 hit the same residue (S6) and parked it out-of-plane; W5 confirms it is a **general** gap (any human-in-the-loop workflow has a conversational surface), not a research quirk.

- **Minor — the KB as compounding state, and the board as derived view.** `tool` models a capability you *call*; the KB is also the durable cross-session *asset that compounds*, and the board is a *live derived query result*, not a stateless call. Both type, both strain. Domain-agnostic-relevant (stateful stores and derived views recur), low severity.

### SDLC leakage check

This is where H4 is most exposed. **The five type *slots* are domain-neutral; the v0.2 *definitions and field enums* are pervasively SDLC-worded.** I had to mentally translate throughout, and the translation succeeded — which is the good news — but the spec prose did not travel:

- `skill` is defined as content "the harness places into an **LLM context** according to an activation policy," and its `activation` enum (`matched` = model/keyword-decided, `event` = harness event) is about *model-context injection*. The neutral concept is "a standing instruction/SOP and when it applies." It survives, but the definition imports the LLM.
- `agent-def` is "an executable principal: a named **context**... which tools/**skills** it may **spawn**." `model`, `isolation`, "spawn," "context" are LLM-agent assumptions. Neutral = "an actor with a role and a permission envelope." Survives with softening.
- `gate` is "a verdict produced **outside the LLM**." That framing *is* the request/guarantee distinction, but "outside the LLM" is the SDLC spelling of "binding vs advisory." The `arbiter` enum `{program|human|agent}` is SDLC-specific — `program` and `agent(LLM)` are software; the neutral trio is `{automated|human|delegated}`.
- `tool` is the worst leaker: `provider: {builtin|mcp|script|platform}`, `side_effect_class: {read|write|execute|network}`, `interface: params-schema`. These are *entirely* software assumptions. Our research method types cleanly against them **only because our instruments happen to be software** (context_*, git, gh) — i.e. the round-trip is flattered by the fact that this second domain is still digitally mediated. A genuinely non-digital research process (wet-lab assays, physical prototyping) would have instruments with none of these fields. `tool`'s *slot* (instrument) is neutral; its *field vocabulary* is SDLC-locked.
- `step` is the cleanest — "a unit of work the harness schedules" with objective/output/depends-on carries almost no software assumption.

**Did I have to soften a definition to fit?** Yes — for `skill`, `agent-def`, `gate`, and `tool` I read the *slot* (instruction / actor / checkpoint / instrument) rather than the *written definition* (LLM-context / spawnable-context / outside-the-LLM / mcp-provider). The types are structurally neutral; the spec text is not. That distinction is the core §3 result.

---

## §4 Verdict

**AGNOSTIC-WITH-GAPS.**

Justification against §3: The vocabulary round-trips a second, non-software domain — no type collapsed, no type went unused, all four edges carried load, and the method's central mechanism (the firewall) types cleanly as a `gate`. That rules out **SDLC-locked** (a locked vocabulary would leave a dead type or fail structurally in a non-software domain; neither happened). But it is not cleanly **domain-agnostic** either, for two independent reasons:

1. **Characterized holes (N=5):** the evidence-grade ladder (G-W1), budget/resource envelope (G-W2), and loop-until-dry convergence (G-W3) are all *general-workflow* concepts the vocabulary cannot express in **either** domain — SDLC simply never stresses them, so W2 didn't fully surface them. Plus the reflexive-plane (G-W4) and stateful-human-channel (G-W5) residues.
2. **Prose leakage:** the type slots are neutral but the v0.2 *definitions and enums* are written in LLM/harness/software language, and `tool`'s round-trip here was flattered by our method still being digitally mediated.

The honest reading: **the skeleton is domain-agnostic; the flesh is SDLC.** The five slots are the universal actor/action/checkpoint/instrument/instruction of any workflow — a genuinely strong result — but a v0.3 that wants to *claim* domain-agnosticism must neutralize the definitions and close the general-workflow holes.

---

## §5 Gap list → spec feedback

| # | Gap | What failed | Minimal fix | Structural or cosmetic? | Agnostic-relevant or research quirk? |
|---|---|---|---|---|---|
| **G-W1** | Grade ladder / graded workflow-state untyped; control-flow branches on it, so firewall & coverage predicates reduce to prose | The vocabulary types workflow *definition* but not the *typed state the workflow branches on*. In SDLC this is hidden (branches on gate-verdicts/vcs-actions the vocab references); research exposes it. | Do **not** add a 6th node type. Add a **typed-state / data-model reference** the spec can name in `gate.predicate` and `step.output` — a `branches_on: <enum ref>` field on `gate`/`step` pointing at a named controlled vocabulary declared once at graph root. Lets a query surface "which gates branch on which state" without modeling the domain data itself. | **Structural** (needs a v0.3 decision before W4 builds a template — the firewall gate is the flagship and currently can't express its own rule) | **Agnostic-relevant** — any state-machine workflow branches on domain state |
| **G-W2** | Budget / resource envelope has no home | A standing continuous constraint + a metered runtime quantity; `budget-gate` mis-types it as a discrete checkpoint | Graph-root `envelope` bag `{resource, cap}` (definition-plane); the runtime spend stays out-of-plane (P-C). A `gate{trigger:envelope-breach}` references the cap. | **Structural** (small) — a v0.3 field, but decide before W4 | **Agnostic-relevant** — every autonomous/long-running workflow |
| **G-W3** | No convergence-loop construct; loop-until-dry unexpressible | `depends-on` is a DAG; `failure_handling` is bounded-retry, not iterate-until-converged | Add a `loop` form on `step`: `{iterate: <child>, until: <predicate>, max: <n>}` — distinct from `failure_handling` (retry-on-fail) | **Structural** — the coverage gate is a core phase gate; W4 template needs it | **Agnostic-relevant** — every search/sampling/exploration workflow |
| **G-W4** | Reflexive plane-isolation not expressible | Category-filter + edge-discipline are knowledge-graph properties, outside the workflow plane | Likely **out of scope** — document that plane isolation is a property of the *operated-on graph*, not the workflow. No node change. | **Cosmetic** (documentation) | Research quirk (specific to the two-plane design), though reflexive workflows recur |
| **G-W5** | Issue = stateful human channel typed poorly as `tool` | Bidirectional durable conversation where human inputs *originate*; `tool{platform}` loses statefulness/bidirectionality | Either accept as out-of-plane (per §14.5 the Issue is a *projection*), or add `tool.kind: channel` marking a stateful bidirectional medium | **Cosmetic-to-minor** | **Agnostic-relevant** — every human-in-the-loop workflow has a conversational surface |
| **G-W6** | Spec *definitions/enums* are SDLC-worded though slots are neutral | Had to translate "LLM context"→working context, "outside the LLM"→binding, `provider:mcp`→instrument to make the round-trip; `tool` fields (`mcp/network/params-schema`) are software-only | Neutralize the five definitions and the `arbiter`/`provider`/`side_effect_class`/`activation` enums to domain-free language (`arbiter:{automated|human|delegated}`, `provider` open-vocab). Keep SDLC values as examples, not the enum. | **Structural** if v0.3 wants to *claim* domain-agnosticism; **cosmetic** if the vocabulary stays explicitly SDLC-scoped | **Agnostic-relevant** — this IS the agnosticism question |

**Bottom line for H4:** a second, non-software domain round-tripped through the 5/4 vocabulary with no type collapse and no dead type — the strongest evidence yet that the *type slots* are domain-agnostic. But the round-trip is **pass-with-gaps, not clean**: three general-workflow holes (graded-state, budget, convergence-loop) that SDLC never stressed, and the spec prose is SDLC-worded throughout. Supports a `partial`-shaped position: **agnostic-with-gaps**, with G-W1/G-W2/G-W3 pre-registered as **structural** v0.3 changes W4 should not build a template without.

---

**Flags for the leader/curator:**
- **Contrarian note:** did not score a clean pass just because our own method round-tripped. It round-tripped *because our research method is still digitally mediated* (its instruments are software). The `tool`-type success in particular is flattered by that; a non-digital research process would break `tool`'s field vocabulary. That caveat is load-bearing for any "domain-agnostic" claim.
- **Consistency with W2:** G-W1 sharpens W2's S4/G-F (prose predicates) into a structural claim; G-W3 relates to W2's G-E but is a *distinct* shape (convergence ≠ bounded-retry); G-W2 (budget) is genuinely new — it appears in the prose method but not in `.claude/`, so W2 could not have found it. This is exactly the payoff of testing the *prose design* rather than the config.
