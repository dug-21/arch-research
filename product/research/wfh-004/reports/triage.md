# W7 — Triage

**Run:** `wfh-004` · Issue #48 · theme `theme:workflow-harness` · value-target **JURATI**.
**Advisory. No graph writes. The owner holds the gate.**
**Input:** `W6-DISTILLED.md` (128 canonical abilities) · SCOPE §7 screens 1–10 · A-1…A-8.

---

## 0. Two facts verified before cutting, because both change a route

**(a) `#179` is not stale — it is half-stale, and W6 over-corrected it.** BRIEFING-v2 corrected "zero hooks." Inspection of `.claude/settings.json`: eight hook entries exist, **all of them Unimatrix knowledge-plane observation hooks**, and the only `PreToolUse` matcher in the repo is `^context_cycle$|^mcp__unimatrix__context_cycle$`. The `permissions` key is **absent from both settings files**. All six factory agent definitions (`factory-curator`, `factory-researcher`, `goal-owner`, `hypothesizer`, `research-leader`, `scout`) carry **no `tools:` and no `disallowedTools:`** — `factory-researcher` is "read-only" in prose while holding every write tool.

> **Hooks exist; enforcement does not.** W6's instruction to `context_correct` #179 should **narrow** it, not retract it. The §11 ambiguity is therefore *maximally* live: nothing is switched on, so nothing can be cut on "the incumbent probably does this."

**(b) The bypass is confirmed at both sites.** `.devcontainer/postCreate.sh:32-33` writes `dsp` **and `dspc`** (the `-c` continue variant, which W6 missed); both are live in `/home/vscode/.bashrc:163-164`. **Not a user deviation — provisioning.**

---

## 1. THE ROUTING TABLE — all 128

**B** = build (first increments, committed) · **Pq** = needs-a-probe · **Ps** = park, sequenced behind a named increment · **Pc** = park, revives on an external condition · **O** = out.

*`Ps` is a real park, not a soft build: the ability is real, it costs ~nothing once its increment lands, and it is not in committed scope.*

| ID | Route | Reason | Probe / killing result |
|---|---|---|---|
| C-01 | **Pq** | §5 row. Transcript may already hold the envelope | **A-13/A-19** — is the JSONL per-call addressable with exact bytes + demanded schema? **Kills** if yes: only the prospective/exclusion delta survives → C-38 |
| C-02 | **B** | Question-form registry; precondition for C-01/C-79/C-86 comparability. Fail-closed cost → ships with C-93 | — |
| C-03 | **B** | Census-backed at 5.2% leakage + `CONDITIONAL PASS` shipped. Evidence is measurement, not briefing priming | — |
| C-04 | **B** | The load-bearing half of the thesis: inference on the enforcement path demotes a guarantee to a tendency | — |
| C-05 | **B** | One handoff schema; makes spend/time/phase matchable by predicates (F3's gap). Falsifier gap noted, not fatal | — |
| C-06 | **B** | Closes "missing verdict read as pass" = `S-02`. Cheap | — |
| C-07 | **B** | Answer A to the unenumerated. Ships with C-93 | — |
| C-08 | **B** | 20 PRs merged before their last check completed. Measured | — |
| C-09 | **B** | Makes order *attestable*, not just enforced. Near-free once F1 exists | — |
| C-10 | **Pc** | Seal-and-continuity optimization; payoff needs a measured re-verification cost nobody has | Revives when re-verification cost is measured and non-trivial |
| C-11 | **B** | Trivial; populates graph hole #177; the key to C-108's one-product answer | — |
| C-12 | **Pq** | The ability is inside the build regardless; the probe sets the **SDLC integration profile**, not existence | **`git log --follow`** over gate-report paths. **Kills the SDLC *supply* case** if it recovers history cheaply — does **not** kill the research case (no git-backed gate reports there) |
| C-13 | **B** | Root of the C-4 family; collapses the largest single (P). Shared-origin evidence (#208 → P-05/P-06) | — |
| C-14 | **Ps** (inc 8) | Divergence detector is cheap once C-13 lands, but second-order | — |
| C-15 | **B** | **The one irreversible capture.** Config-in-force cannot be recovered later; `settings.local.json` is gitignored. All of F5 is worthless without it | — |
| C-16 | **B** | `S-07`: five weeks of silent audit stoppage, found 36 days later. Silence is the cheapest way to defeat a log | — |
| C-17 | **Pc** | **Cut against a 3-lens convergence.** Two stores exist by accident, not necessity — consolidate (C-22), don't institutionalize the duplication and its alarm stream | Revives when a second store is authoritative for a reason we cannot remove |
| C-18 | **Pc** | Reasoned only; our failure set is covered by C-08 ordering + C-12 immutability | Revives on a first observed destroy-before-inspect instance |
| C-19 | **Pc** | Reasoned; zero incumbent both domains | Revives when artifacts cross a trust boundary |
| C-20 | **B** | This run reproduced FP-3 inside itself with a filename census. Precondition for any self-measurement | — |
| C-21 | **O** | **Subsumed** — converts to C-77 + C-110 + C-43; no new primitive. Out on redundancy, not on an incumbent claim | — |
| C-22 | **B** | The spine of F1. `S-21`'s 20+ open issues show the incumbent cannot retrofit from outside the boundary | — |
| C-23 | **B** | `S-11` is both the field instance and the X-5 artifact: the repair applied was re-identifying the actor | — |
| C-24 | **B** | Census-backed, two-sided, near-free once C-22 lands. M4's 30-day-window bound cited honestly | — |
| C-25 | **Ps** (inc 8) | "Did anything happen no step declared" — the question nobody asks. Downstream of C-22 + C-34 | — |
| C-26 | **B** | **Verified live:** zero `tools:` on all six agent files while one is "read-only" in prose. A set comparison | — |
| C-27 | **Pq** | §5 row | **A-3/A-5** — do `tools:`/`disallowedTools:` bind a subagent's actual tool set? **Kills** if a per-agent allowlist fully constrains principals |
| C-28 | **Pq** | §5 row | **A-4** — do deny rules + MCP allowlists screen destinations? **Kills** if the deny plane covers components and egress |
| C-29 | **B** (inc 4) | Only structural answer to F-17, unsolvable at the model layer. Rel↓ declared → ships with C-93 | — |
| C-30 | **B** (inc 4) | Sealing; cheap given C-29. Otherwise "authority is whatever the last message argued for" | — |
| C-31 | **Pq** | §5 row — **the run's highest-value probe.** C-5 UNDECIDED makes every Security claim resting on it provisional | **A-6** — does the managed-settings tier supply a binding principal an agent cannot alter? **Kills increment 4's root** if negative |
| C-32 | **B** (inc 4) | The **phase** dimension is new, has two real instances, and is not a matchable predicate in either incumbent | — |
| C-33 | **Pc** | Purpose-bound grants are a finer cut than usable at n=6 agents | Revives when a dual-use tool is broadly granted |
| C-34 | **B** (inc 4) | Field both domains (`P-03`, `S-10`). Adopt the convergent **record-and-flag** disposition on the semantic half | — |
| C-35 | **B** (inc 0) | **Highest yield per unit cost in the register.** `S-15`: live bearer token in cleartext to a non-gitignored path. Needs no object model | — |
| C-36 | **Pc** | Sec↑/Rel↓ declared; deadlock mode real | Revives narrowed to the declared-irreversible class |
| C-37 | **Ps** (inc 8) | What survives the curator single-writer dissolution. Cheap, no live contention | — |
| C-38 | **B** | **The only concern with no detector at all.** The (P) capture is harness-emitted, therefore free. `#944` v1 read the retired oracle and no manifest said so | — |
| C-39 | **B** | Harness-emitted (P); precondition for C-40/C-121. Today a compromise cannot be scoped even in principle | — |
| C-40 | **Ps** (inc 7) | "A stored node is a self-delivering instruction to the entire future of the system." Sequenced behind C-39 | — |
| C-41 | **Ps** (inc 7) | Set difference at near-zero marginal cost once C-38 lands | — |
| C-42 | **Ps** (inc 7) | Falsifier live: agents may never use the channel. Free to log once C-38 exists | — |
| C-43 | **Pq** | §5 row | Hand-list is DEFINITION-layer; only *verifiability* is harness residue |
| C-44 | **Pq** | §5 row | Blinding is a definition choice; self-declared stylistic-fingerprint leakage caps its value |
| C-45 | **Ps** (inc 7) | Trivial; two real *opposite* instances make it genuine parameterization | — |
| C-46 | **B** | **Nothing observes the run.** Every census-backed failure happened with CI green. The residual's first face | — |
| C-47 | **Pq** | §5 row | **A-7** — does `SubagentStop` fire on crash; do turn/time bounds cover it? **Kills** the supply case if yes |
| C-48 | **Pq** | §5 row (reaping half). The *ownership* half is F1 and inside the build | **A-7**. 26 zombies over 6 sessions holding build and DB locks is standing evidence |
| C-49 | **B** | OBS-7 is binding on this very document — the run's live instance of its own catalogued defect | — |
| C-50 | **B** | The C-3 inversion: files-as-truth is the incumbent's best asset generalized, substrate-neutral | — |
| C-51 | **B** | Conservation of units; cheap given F1 | — |
| C-52 | **B** | Populates G-W1 (W5's deepest hole). The research firewall generalized to any workflow | — |
| C-53 | **B** | `P-21`: 14.8% of tool calls after completion, because "completion" was a sentence | — |
| C-54 | **B** | Trivial; two Issues for wfh-002, one still open. SDLC prevention `[V]` | — |
| C-55 | **B** | Harness-emitted (P), demonstrably known — the engine logged what it skipped and never surfaced it | — |
| C-56 | **Ps** (inc 8) | Field-real (~4 stalls/run; the access rules *instruct agents to reconnect by hand*). Accept the curator's flagged merge; re-split at build time | — |
| C-57 | **B** | E-1's implementation. `SCOPE FAIL` 0/231 and 62/63 missing retros are **obligation** failures, not observation failures | — |
| C-58 | **Pc** | New obligation class (type-triggered) but presupposes a fleet. **Architect-for-future: E-1's data model must admit a *type* carrier or it needs re-modelling** | Revives at ≥2 tenants or ≥3 instances of one definition |
| C-59 | **Pc** | M2's own argument defeats the general case: agents cannot be deterred, so enforcement must be substrate, not sanction | Revives narrowed to the irreversible class |
| C-60 | **Pc** | Chargeback presupposes an economic relationship we do not have | Revives at multi-tenant |
| C-61 | **B** | `SCOPE FAIL` declared and fired 0/231 — the census proof. X-1's workhorse. LCO consequence adopted | — |
| C-62 | **B** (inc 0) | **`S-06` is proof-by-instance:** the zombie-bug fix shipped `setsid` without `-w`, so every failing suite read PASS. Needs no object model | — |
| C-63 | **B** | Trivial given F2; "zero executions = unfalsified, not verified" | — |
| C-64 | **Ps** (inc 6) | `P-16`'s 61× undercount. The independence condition is what makes it non-vacuous — carry it or don't build it | — |
| C-65 | **Ps** (inc 6) | "A stale allowlist is a security hole with a timestamp." Sequenced behind having rules at all | — |
| C-66 | **B** | The ideal adversarial move is weakening a check; it looks like maintenance and produces a green build. **Ships with C-95 or it becomes the record-attack with a dashboard** | — |
| C-67 | **B** (inc 0) | **The run's headline discovery:** borrowed enforcement believed on, verified off. Needs no object model | — |
| C-68 | **Ps** (inc 8) | The HARNESS-lints-DEFINITION inversion is novel and cheap. A protocol contradicting itself made absence uninterpretable | — |
| C-69 | **Ps** (inc 8) | M3 nominates it the run's most important row. Sequenced late: **sampling with unverified instruments measures nothing** — must follow increment 6 | — |
| C-70 | **O** | **M2's own transplant argument kills it:** "agents can't be deterred," and C-70's mechanism is a sanction on misdeclaration. Keep C-69's harness-selected sampling instead | — |
| C-71 | **Pc** | Expensive; same machinery as C-96 | Revives if C-96's probe finds qualifying segments |
| C-72 | **B** (counterweight) | One of only two mechanisms that can allocate an **alarm budget**, and the only cost control on the strictness program | — |
| C-73 | **Pq** | Targets no face; it is a *practice*. But the only proposal that **creates** the missing evidence class | **The probe is the exercise.** Scoped red-team under RoE. **Kills X-4** if it finds nothing an existing control would not have caught |
| C-74 | **Pc** | M2's own sequencing flag: inert until record integrity exists; 62/63 means no history to chart | Revives at ≥20 comparable recorded runs |
| C-75 | **Ps** (inc 8), narrowed | F-7 measured (omission 2.3× fabrication, leaves no artifact). Narrow to summaries feeding an *automated* step | — |
| C-76 | **Ps** (inc 8) | Field: a triage report with a duplicated section, two recommendation lists, three inconsistent counts, consumed undetected 3 days. **This document is in that risk class** | — |
| C-77 | **B** | Two independent agent reviewers ratified a wrong diagnosis; the human caught it. Cheap | — |
| C-78 | **B** (counterweight) | Lowers apparent assurance to its true level. Pairs with C-77 | — |
| C-79 | **Pc** | N× cost, gains flat by N≈5–10, no field instance | Revives as the calibration instrument for C-86/C-87 |
| C-80 | **O** | **Subsumed + mechanism fails at our scale.** M2's own falsifier: with few verifier configurations, rotation permutes the same reader. C-78 + C-110 cover it | — |
| C-81 | **Ps** (inc 8) | W0-e's clean asymmetry case (O(1) vs O(analysis)) — "and we did not build it" | — |
| C-82 | **Ps** (inc 8) | FP-3 reproduced *inside* the run measuring FP-3. Requires addressable sets → downstream of F1 | — |
| C-83 | **B** | **The cheapest high-leverage capture in the reservoir** where the declarer is the definition author | — |
| C-84 | **Ps** (inc 8) | `#944` v1 traced a retired component. Catches referent errors only — stated honestly | — |
| C-85 | **B** | The firewall's own `proven_by` discipline generalized. `crt-056`'s validator did it by hand and named it recurring | — |
| C-86 | **Ps** (inc 8) | The "unavailable" default is the load-bearing half and costs nothing; the ledger half is the spend | — |
| C-87 | **Ps** (inc 8) | The linkage exists in the field and nobody joins it (52%). The clean answer to judge bias | — |
| C-88 | **Ps** (inc 8), narrowed | Build only the **origin field** on the defect record (near-zero, part of F1's schema). The rollup is F5, deferred | — |
| C-89 | **Ps** (inc 8) | `P-16`'s check was cheaper than the analysis and unbuilt for months because no predicate was stated | — |
| C-90 | **Ps** (inc 8) | "A system that learns from a corpus with the failures removed will conclude it is doing well" | — |
| C-91 | **B** (counterweight) | The thesis's honesty instrument, computable from the path. **Carry M1's altitude clause** | — |
| C-92 | **B** (counterweight) | **Ships *with* the determinism, not after.** Two blind class-A lenses built the identical antidote. The run's cleanest non-traditional item | — |
| C-93 | **B** (counterweight, precondition) | "A control is bypassed when compliance costs more than circumvention. `dsp` sets circumvention at two keystrokes" — verified, plus `dspc` | — |
| C-94 | **B** (counterweight, precondition) | `S-11` is the exact failure. **Clause (c) — provenance propagating to artifacts — is the always-omitted half** | — |
| C-95 | **B** (counterweight, precondition) | The bypass count is the one number that would have surfaced `dsp` as a finding | — |
| C-96 | **Pq** | §5 row | **Do real runs contain replay-qualifying segments of useful length?** An empty payoff set is itself a finding about the cut |
| C-97 | **Pc** | F5's flagship; may not resolve config effects at affordable N | Revives as a **query**, not a build, once C-15 has recorded config for ≥20 runs |
| C-98 | **B** (inc 4) | W0-e lists idempotent retry as a model *cannot-in-principle* — it must live in the harness. Five consecutive failed release runs | — |
| C-99 | **B** (inc 4) | Carry M3's clause: **classify by channel, not syscall** (→C-35) | — |
| C-100 | **B** (inc 4) | n=2 and thin, but near-zero inside C-99. "Any register keyed on success is wrong at exactly the moment it matters" | — |
| C-101 | **B** (inc 4) | Cheap given C-22 + C-99. Value is after-the-fact scoping, not deterrence | — |
| C-102 | **Ps** (inc 8) | `S-18`: 50,000 → 8,000 "at some point." **Must require the dependent set be named or it is theatre** | — |
| C-103 | **Pc** | An orchestration *policy*, DEFINITION-layer, once F1 makes units re-runnable | Revives as a cheap **experiment** after C-22/C-49 — not a build |
| C-104 | **Pq** | Contests graph #185/#184 | Measure **unique catches** vs upstream. **Kills** if every substrate refusal is already caught by the harness |
| C-105 | **Pc** | W0-b2b *is* the manual proof it works. Downstream of the whole record | Revives at ≥20 recorded runs |
| C-106 | **B** | E-1 applied to the retro. 62/63 despite the tool existing. **Discharges A-4 mechanically instead of by amendment** | — |
| C-107 | **Pc** | Nothing has decayed yet; `proven` is forever in both domains. **Architect-for-future: the status record needs room for a confirmed-at field** | Revives at first proven-node basis change, or 6 months of proven nodes |
| C-108 | **B** | **The resolution of one-product-or-two.** Makes the fault line named data instead of a product boundary | — |
| C-109 | **B** | Populates G-W3; two real *opposite* instances. Carry M6's caveat on the ≤2 constant | — |
| C-110 | **Ps** (inc 8) | Real; two opposite instances; no live pain | — |
| C-111 | **Ps** (inc 8) | M6's sharpest dissolution: five definitions converging on "parallel spawn in one message" is convergence on a **hole** | — |
| C-112 | **Ps** (inc 8) | `S-10`: 126 compile cycles, 4 orphaned worktrees. SDLC-today | — |
| C-113 | **B** (counterweight) | **HACCP's economy of enforcement — the ability that says *do not enforce everywhere*.** The run did not count this as a counterweight; it is one | — |
| C-114 | **Pc** | **The agent classifies its own act — self-report wearing a schema.** Contradicts C-13/C-14 directly | Revives only if an observer, not the actor, can emit the classification |
| C-115 | **Pc** | M2's own strain: tokens are conserved by construction, not physics | Revives once C-116 yields two independent measures — then it is exactly the reconciliation that matters |
| C-116 | **Pq** | **Reuse:** this is opcost B1–B4 (#125/#127/#128/#129, `grade:partial`) at a different altitude | **A-10** — does telemetry attribute per-agent cost with `parent_agent_id`? **Kills** the supply case if yes |
| C-117 | **Ps** (inc 8) | Domain-independent and empty on both sides. "A ceiling that only halts is a ceiling people will raise to infinity" → binds to C-95 | — |
| C-118 | **Pc** | Zero field data anywhere. **Architect-for-future: the unit object must carry a tenant field from day one, or the first stranger tenant is a migration** | Revives at first stranger tenant |
| C-119 | **Pc** | X-4 population; all `reasoned`, zero field | Revives if C-73's red-team produces a first field instance |
| C-120 | **Pc** | Same. **But its indictment is carried forward now:** it falsifies drop-list item 6 | Same |
| C-121 | **Pc** | Same; also downstream of C-39 | Same |
| C-122 | **Pc** | **Mechanism partly fails on the subject:** an LLM has no persistent memory to be tipped off. M2 states this and does not apply it | Revives if agents gain cross-run memory, or human insiders enter the threat model |
| C-123 | **Pc** | Rel↓risk declared; for our failure set, C-34 + C-29 cover it | Revives at irreversible ops if C-99 proves insufficient |
| C-124 | **Pc** | C-44's caveat bites: both sides running the same generator agree vacuously | Revives when handoffs cross a trust boundary |
| C-125 | **Pq** | §5 row | **A-8** — does any channel deliver into an in-flight subagent? **Recommendation stands either way: do not build a steering channel.** If A-8 is negative it is a platform requirement, not a harness ability |
| C-126 | **B**, reclassified | **Not steering — gate integrity.** M6's regression flag binds: the expiry default must itself be declared fail-closed. Single-lens after M6-28's withdrawal | — |
| C-127 | **B** | *"The most load-bearing control in every workflow definition we have — and the one control with no integrity binding at all."* | — |
| C-128 | **B**, narrowed | Field both domains (17 vs 33; the 500-line cap waived on every feature). **Narrow to the gate** — one typed number at approval | — |

> **Tally: 51 build · 14 needs-a-probe · 60 park (25 sequenced, 35 conditional) · 3 out.**

---

## 2. THE SHORTLIST, ARGUED

### Is it one product or a list? — the adversarial test of W6 §5

Attacked on five fronts. **It survives on one leg, not two, and is wrong in two specific places.**

**What fails.** The headline arithmetic — *116 of 128 target a face no configuration reaches* — is **near-tautological and must not be cited to the owner as evidence.** The five faces were *induced from this register*; a classification derived from a set will of course cover the set. **Strike that number.**

**What survives, and it is enough.** The **SDLC falsification test** is genuine independent evidence: SDLC had *more* configured than research, and every switch is a predicate over the wrong noun — tool calls, pipelines, sessions, files, branches. **The failures live on nouns no component holds.** A real experiment with a real negative result, not derived from the register.

**Where the claim is wrong.**

1. **F3 is not a property of the unit object.** Authority-as-data needs *principals and calls*, not units. Only C-32's **phase** dimension needs F1. The sharp statement: **F3-minus-phase is separable, cheaper, closer to the incumbent's shape, and carries the larger security payoff** — so the build has a cheap separable front half, **and a second root object (the principal) that the "one object model" framing hides.**
2. **F5 is not part of the product.** Largest face (28), least evidenced (mostly `reasoned`, zero-in-both), and an *emergent query capability* once F1+F2+C-15 exist. Shipping "a comparison substrate" as a deliverable is the second-system trap. **Buy exactly one thing from F5 now — C-15**, because config-in-force is the only capture unrecoverable after the fact.
3. **F4 is a thin layer on F1, not a face** — except C-58's type-carrier, which is genuinely new and is why the schema must admit it now.

> **The answer: not one product, and not 128 — two objects and one deferred layer.**
>
> - **Object A — the unit/run/verdict object model** (F1 + F2 + F4-as-a-layer). *This is the product.*
> - **Object B — authority as data on principals and calls** (F3-minus-phase). Separable, cheaper, **gated entirely on probe A-6**.
> - **Layer C — comparison and analytics** (F5). **Not built.** Falls out as queries once A exists and C-15 records config.

**And the sentence W6 buries in a table cell in §7, which is the most actionable thing in this run:** the missing object model **is graph node #183** — the JURATI typed operating-context ontology, already `grade:claimed`, already SPECIFIED (5 nodes / 4 edges), already stress-tested three times, whose run **closed early with no artifact.** M5's residual and #183 are the same object seen from demand and supply.

> **So the build decision is not "what should the harness do." It is: *do we build #183 and bind enforcement to it.*** That reframing is worth more than the register.

### The increments, in order

**Increment 0 — the three items that need no object model and no decision (start now).**
**C-35, C-62, C-67.** Each has a field instance where the failure *already happened*: a live bearer token written to a non-gitignored path; a fix that made every failing suite read PASS; enforcement believed on and verified off.
*Cost: days. Depends on nothing.* **If the owner decides not to build the harness at all, these three still ship.**

**Increment 1 — the unit object (F1 core).** C-22, C-46, C-49, C-50, C-51, C-13, C-15, C-09, C-53, C-54, C-55, C-16, C-20, C-24.
*Buys:* addressing — everything downstream is a predicate over this. *Costs:* the spawn/injection/terminal-transition boundaries must all route through the harness. **This is the migration cost nobody in the run priced.**

**Increment 2 — the verdict record (F2 core). Ships with Increment 3.** C-03, C-04, C-06, C-07, C-08, C-11, C-52, C-108, C-85, C-02.
*Buys:* gates that bind; converts 6.9%-visible / ≥13.9%-actual into one number. *Costs:* C-03's declared regression is real and is why Increment 3 is not optional.

**Increment 3 — the counterweight kit. Ships *with* 2, never after.** C-93, C-94, C-95, C-91, C-92, C-113, C-72, C-78. *Buys: survival.*

**Increment 4 — authority as data (Object B). Gated on probe A-6.** C-29, C-32, C-23, C-26, C-30, C-34, C-05, C-99, C-98, C-100, C-101.
*Buys:* the security half of the thesis. *Costs:* Rel↓ on the unenumerated, declared in three rows. **If A-6 is negative, do not build this here.**

**Increment 5 — obligations and instrument integrity, woven into 1–2.** C-57, C-83, C-106, C-109, C-61, C-63, C-66, C-77, C-127, C-38, C-39, C-126, C-128.
*Buys:* E-1 and X-1. **C-127 alone closes the only control every one of our five workflow definitions leans on and none of them binds.**

**Not in scope, explicitly:** all 60 `Ps`/`Pc` abilities — the entire F5 analytics layer, all six X-4 detectors, and reconciliation (C-17).

---

## 3. THE DROP-LIST AND CONFIGURATION BACKLOG — co-equal (A-6 §1)

### 3a. Do not build — with rulings on the two contested rows

**Ten of W6's twelve stand. Two do not, and W6 flagged both without ruling.**

| # | Ambition | Ruling |
|---|---|---|
| 1 | Retrospective resolved-context capture | **Stands**, both domains. Only the prospective + exclusion delta survives → C-38 |
| 2 | Raw cost measurement | **Stands, research-side only.** `opcost` solves it; the graph agrees (#125/#127/#128/#129). **SDLC has zero cost record, so "solved" does not transfer** |
| 3 | Per-call trace waterfall | **Stands**, both domains |
| 4 | Semantic context injection | **Stands.** Three live injection points; the residual is the *ledger* → C-38 |
| 5 | Named units, isolated windows, spawn events | **Stands** — the free thing is the **session**; the missing thing is the **unit** |
| 6 | Per-tool-call approval gating | **DOES NOT STAND AS WRITTEN — re-word it.** C-120's indictment is verified: the only `PreToolUse` matcher in this repo covers one MCP tool. **The per-call gate is free; aggregate screening across units, sessions and time is not, and decomposition evades the free gate today** |
| 7 | The durable-execution primitive | **Stands. Never build the engine.** Adoption is a HOW, out of scope |
| 8 | Session resume/fork | **Stands** — missing are the *run* and *subagent* layers → C-46/C-49 |
| 9 | OS sandbox, egress allowlist, credential shielding | **Stands, pending A-11** |
| 10 | Rollback of CLI-mediated edits | **Stands**, with the Bash/subagent exclusion residual |
| 11 | A blocking human gate as such | **DOES NOT STAND. C-127 is a build.** The deficiency is not "conditionality" — the gate has **no integrity binding at all**; present a summary for approval and execute something else, and F-7's omission asymmetry makes that the most dangerous instance of the dangerous middle in the system, because a human sits downstream of it |
| 12 | Telemetry pipeline construction | **Stands, pending A-10** |

**Added to the drop-list by this triage:**
- **Store reconciliation (C-17)** — cut against a 3-lens convergence. Do not build a reconciliation engine for two stores that exist by accident. **Consolidate.**
- **Bonded self-declaration (C-70)** — killed by its own transplant's stated limit.
- **Verifier rotation (C-80)** and **record-review-by-a-distinct-role (C-21)** — subsumed, no new primitive.
- **The whole F5 analytics layer as a deliverable** — a query surface, not a product.
- **A Cost generation lens in any successor round** — it would manufacture candidates into the one cell where the run cannot check them. *(See §5/8.)*

### 3b. Switch on instead of building — verified-unflipped today

Every item is **subtraction or one line of config**, not construction.

**Research side. R2 is the single highest-value switch and is confirmed unset: zero `tools:` / `disallowedTools:` across all six factory agent files** — including a "read-only" researcher holding every write tool. **R1** — no `permissions` key exists in either settings file. **R3** — a second blocking `PreToolUse` entry, *including the firewall's syntactic half: deny `grade:proven` lacking `proven_by`.* **That cardinal invariant is one rule away from being enforced and is currently prose.** **R7 — disable the provisioned bypass:** `dsp` **and `dspc`** are written by `postCreate.sh` into every fresh container; undoing that is subtraction. **R4** `SubagentStop` · **R5** telemetry+traces · **R6** sandbox · **R8** turn/time bounds (`#174`'s silent death had no timeout to trip) · **R9** version-control `settings.local.json` · **R10** managed-settings tier · **R11–R13**.

**SDLC side. S1** branch protection + required APPROVED review (`reviewDecision: ""` on 359/359 — the review plane is configured off). **S2 — the agent runs on its own token, not the human's.** The precondition for authority-as-data, and it is configuration, not build. **S3** CODEOWNERS on verifier/fixture/workflow paths — a config-grade approximation of "the graded party cannot modify the grader," which is *the exact altitude at which SDLC's configured enforcement failed: CI was external, the fixture was not.* **S4, S5.**

> **Money saved: if A-3/A-4/A-6/A-7/A-10 all land positive, five of the fourteen probe-routed abilities move to this list and never cost a line of product code.**

---

## 4. THE PROBE QUEUE — ordered by decision-value per unit cost

| # | Probe | What it decides | Cost |
|---|---|---|---|
| **1** | **A-6 — does the managed-settings tier supply a binding principal an agent cannot alter?** (with C-5, fresh-process escape) | **Increment 4's root.** Until A-6 settles, *every* Security claim resting on C-31 is provisional. Negative ⇒ authority-as-data is unbuildable on this platform and the product's core claim — guarantees, not tendencies — is unstateable here | hours |
| **2** | **The §11 configuration counterfactual** — flip R1/R2/R3/R7 + S1/S2, then deliberately attempt the OBS-5/10/13-class violations | **Converts the entire 12-row "may be re-buying" table from ambiguity to fact in one exercise** — and simultaneously measures **bypass economics** (does the operation route around the switches?), which is the X-5 evidence nobody has. Two findings, one probe | 1–2 days |
| **3** | **A research-side census** of the FINDINGS corpus | The evidence base is **census-heavy on SDLC and anecdote-heavy on research**; several "both-identically" claims rest on one census and one story. **The 14-pain spine justifies the whole build and half of it is anecdote** | ~1 day |
| **4** | **A-10 — per-agent cost attribution with `parent_agent_id`?** | C-116 + the cheapest half of C-22; the altitude question on the only `grade:partial` nodes this register touches | hours |
| **5** | **A-7 — does `SubagentStop` fire on crash?** | C-47 + C-48's reaping half; `#174` | hours |
| **6** | **`git log --follow`** over canonical gate-report paths | Converts ≥13.9% to exact; settles C-12's SDLC supply-vs-surface | ~1h (needs a full clone of `dug-21/unimatrix`) |
| **7** | **C-96 — do real runs contain replay-qualifying segments?** | C-96 + C-71. An empty payoff set is itself a finding about the cut | ~1 day |
| **8** | **C-73 — a scoped red-team under RoE** | Gates X-4's promotion and manufactures the run's missing evidence class | 3–5 days |
| **9** | **A-8 — does any channel deliver into an in-flight subagent?** | C-125 — **low decision-value, because the recommendation is "don't build it" either way** | hours |

**On `git log --follow` and first place — disagreeing with W6.** Run it; it is cheap and sharpens the number the business case cites. **But it does not go first, because nothing routes on it.** (i) The research side has no git-backed gate reports at all, so C-12 is *supply* there regardless; (ii) recovering an overwritten FAIL by archaeology is a different ability from a record that cannot be overwritten — the harness requirement is unchanged either way; (iii) **`--follow` is heuristic and `git log` cannot recover an overwrite that happened *within* a single commit's working tree — which is exactly the shape of an agent retrying in-session.** *The measurement's own ceiling is below the question it is meant to settle.* It changes an integration profile, not a build decision.

---

## 5. POSITION ON EACH OF THE NINE

**1 — The build decision.** §2. The residual claim **holds on the SDLC falsification test and only on that test**; the 116/128 figure is circular and is struck. **Two objects and one deferred layer.** And the object already exists as a specification: **#183**, `grade:claimed`, no artifact, run closed early.

**2 — Pricing the (P) reservoir.** M6's *"dissolves wholesale"* is **half right, and the half it gets wrong is the expensive half.** Sort the 24 by **who must emit**:

- **Harness-emitted (~10)** — P-a, P-b, P-c, P-f, P-i, P-j, P-k, P-r, P-x, half of P-g. **Genuinely free at generation time: the emitter is the codebase you are building anyway. No distributed bill. Buy all:** C-22, C-24, C-38/C-39, C-116, C-55, C-52/C-53, C-12, C-15.
- **Definition-author-emitted (~4)** — P-d, P-e, P-o, the definition half of P-l. One-time authoring cost per definition. **Buy C-83 and C-34.** Cheap, high leverage.
- **Agent-emitted (~7)** — P-t, P-u, P-n, P-p, P-m, P-q, the agent half of P-l. **These are not captures. They are self-report wearing a schema**, and they inherit every failure mode the same register forbids at C-13/C-14/F-11. **W6 files this contradiction at §8/7 and never connects it to the reservoir, which is where it bites hardest. C-114 is the clean case.** Buy **C-05** and the **origin field of C-88**; do not buy C-114's emission mandate; treat P-n/P-m/P-q as ordinary schema work on the harness's own write path, not a reservoir win.
- **Human-emitted (1)** — P-w. Worth it **at the gate and nowhere else** — one typed number at approval. The field evidence (17 authorized, 33 written) is exactly one number.
- **Unrecoverable — P-15.** Provider quota. Correct and honest.

> **The reservoir is worth buying wherever the harness is the emitter, and is a trap wherever an agent is. ~14 of 24, not 24.**

**3 — One product or two. Position: ONE, via C-108.** The evidence is a configuration diff, not an inference: the *same* hook binary, the *same* eight hook events, the *same* `context_cycle` phase API run under a research definition and an SDLC definition **in three repos today**, while the phase vocabularies differ entirely. M5's two-product reading rests on the evidence models differing *in kind*. **C-108 dissolves it: one verdict record carrying a verifier-kind field (C-11) and an optional re-execution handle.** SDLC populates the handle; research leaves it null and points at an artifact. **One interface, two sources — precisely M5's own settling observation, answered by a lens M5 never read.**
**Stated risk:** the null handle becomes a fault line the first time the harness must *re-run* research evidence to trust it. Our firewall doctrine says it never does — `proven_by` is an attached artifact demonstrated by us, past tense. **Safe on our doctrine; if the doctrine changes, the fault line reopens.** Recorded as the condition.

**4 — The steering cell. Decided: M2 is substantially right, and the grid is mis-reporting — for a reason M2 did not give.** Split the cell:
- **(a) Mid-run redirection of a running agent.** M2 is right, and our field record agrees from the other direction: **`P-01` is a file written specifically to steer a behaviour, and the behaviour recurred.** **Correctly thin. Do not build a steering channel** — it also makes run duration unbounded by design, which at fleet scale is unbounded cost.
- **(b) The human's decision as an object.** C-127, C-128, C-126 are **not steering — they are gate integrity**, and they are misfiled. Reclassify C-127/C-128 → Security/Structure; C-126 → Introspection/Structure.

> **The run does not have a steering coverage hole. It has a taxonomy error plus a design position.** Honest population after reclassification is **C-125 alone** — one member, correctly thin. **And the corollary is the finding: the most load-bearing control in every workflow definition we own has zero integrity binding, and it was filed under the concern everyone had agreed was empty.**

**5 — Emergent concerns. Promote three of six.**

- **E-1 — PROMOTE.** Two independent irreducibility arguments, neither rebutted; census-backed in both domains. ⟨C⟩ contamination is real and **M6's population evaporates with M6-16** — five lenses, not six. Promote anyway: `SCOPE FAIL` 0/231 and 62/63 are **measurements, not briefing artifacts.** **Placement:** downstream of Structure, *beside* Introspection.
- **X-1 (instrument integrity) — PROMOTE, and fold X-3 into it.** `S-06` is proof-by-instance. **X-3 is X-1's external-plane face**, not a peer (population 3, all overlapping). **Placement:** downstream of Introspection, *above* Self-improvement — self-improvement over unverified instruments is worse than none (C-90).
- **X-5 (control survivability) — PROMOTE, argued hardest.** Weakest-argued, strongest-evidenced; both artifacts verified. **If X-5 is not a concern carrying a coverage obligation, nothing in the next round is required to populate it, and the register stays 97.7% locks.** **Placement: beside Security, as Security's economic dual** — Security asks *is authority bounded*; X-5 asks *does the bound survive the people working under it.* Not under Human steering: its time constant is between runs, not within one.
- **X-2 (record integrity) — DECLINE, adopt M2's reading.** The census shows Introspection was **never delivered**, not delivered-and-insufficient. **Instead: amend the seeded Introspection concern to include trustworthiness against a party with motive and write access.** No new concern; fixes the actual defect.
- **X-4 (adversarial adaptation) — DECLINE, park behind C-73.** Promoting it creates a coverage obligation we cannot discharge. **Revival is clean and named: the first field instance from C-73's red-team.** That makes C-73 the probe that gates a concern.
- **X-6 (inference transaction) — DECLINE, fold.** M1's own doubt is correct; its population is entirely F2, and routing F2 serves it completely.

**6 — `git log --follow`.** §4. **The shortlist does not depend on it.** Run it sixth.

**7 — M6-16 and M6-28: WITHDRAWN. Confirmed from the register.** M6 §2 registers exactly 32 candidates, sequence `01–15, 17–27, 29–34`. **16 and 28 are absent.** Their content appears in M6 §1 prose — **stated as properties, never registered as candidates.** Curator inferences from a different section; they must not count as register entries.
**Consequences applied:** C-57 drops 4/6 → **3/6 [A×3]**; C-126 drops 2/6 → **1/6 [A]**; Human steering loses a slot; **E-1 is a five-lens concern, not six.** **None of these changes a route — which is itself worth reporting: the run's conclusions are not load-bearing on its convergence counts.**

**8 — The Cost column: an honest boundary above, a solved cell in the middle, a *method* hole at the bottom — not a coverage failure to remedy by generation.**
- **Above `P-15`:** a hard exterior ceiling. Report and stop.
- **Between P-15 and the unit:** **already solved and already `grade:partial`** — opcost B1–B4. The cell reads empty because the lenses generated *abilities* and the ability exists at a coarser altitude. **The register's most concrete reuse hit, and it belongs in the Cost answer, not only in §7.**
- **At the unit:** genuinely unmeasured. **M6's "hole in the world" is the weakest of the six claims** — 610 issues with zero cost incidents is *absence of instrument*, a statement about us.

> **Ruling: it needs a measurement, not a lens.** Remedy = probe #4 plus extending #125/#127/#128/#129's altitude to unit→run→tenant. **Do not spawn a Cost lens in a successor round.** That is a save, and it belongs on the drop-list.

**9 — The contradiction register: seven resolved, four to the owner, one resolved by the promotions.**

| # | Resolution |
|---|---|
| 1 Strictness vs bypass | **RESOLVED.** X-5 promoted; C-93/94/95 are **preconditions, not additions**. Ship rule in §7 |
| 2 Detection vs alarm fatigue | **RESOLVED.** No detector ships without an alarm budget. C-72 + C-126 are the allocation mechanism — and no lens connected them because neither read the other. Both routed build |
| 3 Enforcement vs the unenumerated | **RESOLVED — not rivals, different loci.** C-07 applies where the *harness* evaluates; C-59 where the *actor* departs. Take C-07 generally; park C-59 to the irreversible class, because a deviation record is a **sanction** and agents cannot be deterred |
| 4 Pre-authorized vs live steering | **RESOLVED** — item 4 |
| 5 Supply vs integrate | **RESOLVED.** Adopt M4's improved formulation verbatim, including *"the run-altitude observer the harness always supplies, because no incumbent plane in either domain has one."* Residual → probe #6 |
| 6 One surface vs reconcile two | **RESOLVED against the 3-lens majority.** Consolidate (C-22); do not reconcile (C-17 → park). The three reconciliation lenses never knew the consolidation reading existed, and M4 flagged its own candidate as possibly subsumed — **leaving reconciliation unopposed by default rather than by argument.** Opposed here by argument: reconciliation is right when two stores are authoritative for reasons you cannot remove. Ours are duplicated by accident |
| 7 Rehabilitated self-report | **RESOLVED against C-70**, killed by M2's own stated limit. Consequence propagated: C-114's emission mandate parked |
| 8 Thesis vs observability cost | **RESOLVED as a build rule.** C-92 ships **with** the determinism. *Any triage adopting the below-threshold abilities without the compensators is taking the observability regression silently.* **Not taken silently here** |
| 9 Declared regressions | Carried into every affected row; C-36/C-59 narrowed to the irreversible class; C-03 paired with C-93; C-126's expiry default declared fail-closed |
| 10 One product or two | **RESOLVED** — item 3 |
| 11 Dual control vs single writer | **OWNER DECISION.** The harness question is ruled (dissolve the *role*, keep C-37's declarability, no general dual control). But *"should the garage keep its single-writer curator"* is a definition-layer choice about our own operation, and the evidence cuts three ways |
| 12 Field-evidence asymmetry | **→ probe #3** |

**Left to the owner, with the trade named:**
1. **Accept an alarm budget as a hard build constraint** — trading detection coverage for operator attention.
2. **Keep or dissolve the curator single-writer rule** — audit concentration vs compromise concentration are the same property from two sides.
3. **Build Object B iff probe A-6 is positive** — and if negative, decide whether a harness whose enforcement is a *tendency* is still worth building.
4. **Ratify or reject the ship rule** in §7 — the only thing standing between this shortlist and the register's own predicted outcome.

---

## 6. THE COVERAGE STATEMENT

| Cell | Thin? | World or method |
|---|---|---|
| **Cost** | Yes (8 slots) | **Both, in layers.** Hard world-boundary above P-15; **already solved** in the middle; **method** at the unit. Not remediable by generation |
| **Human steering** | Yes (7 → 6) | **Neither — a taxonomy error plus a correct design position.** Three of four members are misfiled gate-integrity abilities |
| **Adversarial security** | Zero field evidence anywhere | **Method, and knowably so.** *An environment with no detector reports no incidents by construction.* Remediable only by C-73 |
| **Research-side evidence** | Anecdote where SDLC has census | **Method, cheap to fix** → probe #3. **The 14-pain spine justifies the whole build and half of it is anecdote** |
| **Tenancy / multi-owner** | Zero field data | **World, today.** Correctly parked (C-118), with the schema constraint recorded so it is not a migration later |
| **Convergence as evidence** | Structurally compromised | **Method, correctly declared.** Every ≥4-way convergence carries ⟨C⟩. **Nothing was ranked by convergence — two of the three highest-value builds (C-35, C-67) are 1-lens and 2-lens** |
| **Calibration base** | Narrow | **World-ish, declared:** one owner's authorship, one model family, one toolchain |
| **Users** | **Zero** | **Method, and nobody named it.** §7 |

**Not remediated:** Cost (needs a meter, not a lens) · Human steering (needs a decision, not candidates) · tenancy (needs a tenant).
**Remediated cheaply:** the research-side census (probe #3) and adversarial evidence (probe #8).

---

## 7. WHAT NOBODY IN THIS RUN HAS SAID

### Where this cut lands on the counterweight ratio

The register is **125 locks / 3 counterweights (2.3%)**, all three from one lens, against a field record where **both** of this operation's real encounters with an enforcement plane ended in an institutionalized bypass — one verified as written into `postCreate.sh`, in two variants.

**Of 51 build routes, 9 are counterweights or legibility rather than locks:** C-93, C-94, C-95 (appeal · override-with-propagating-provenance · control-effectiveness telemetry), C-91 (guarantee-vs-tendency labeling), C-92 (inference auditing determinism), **C-113 (economy of enforcement — the ability that says *do not enforce everywhere*; the run did not count this as a counterweight and it is one)**, C-72 (the only cost control on the whole program), C-78 (reports assurance *down* to its true level), C-108 (names a fault line instead of locking it). **18%, up from 2.3%.** Plus X-5 promoted to a concern carrying a coverage obligation, so the next round is *required* to populate it. Plus 60 abilities parked and 3 cut.

> ### The ship rule
> **No control ships without its appeal path (C-93), its override record with propagating provenance (C-94), and its override-rate telemetry (C-95) in the same increment. A lock shipped alone is a lock that will be bypassed, and we have a two-for-two record.**

**It is still a strict system, and 18% is a posture, not a proof.** If the owner thinks the ratio is still wrong, the cheapest correction is not more counterweights — it is **probe #2**, which measures whether *we* route around switches when they are on.

### Four things nobody said

**(1) This run has 128 abilities and zero users.** Every candidate is justified by a **failure of ours**. Not one is justified by a workflow someone wanted to run and could not. Read cold, the register is a **defect list, not a product requirement list** — a superb post-mortem machine for an operation whose incident log JURATI's buyer does not have. Note what it predicts: abilities cluster on Introspection, Security-as-bounding and Structure (127 of 205 slots) — **the three concerns that generate incidents** — and go empty on Cost and steering, **the two that generate value.** A-5 fixed the domain skew; A-6 fixed the layer skew. **Nobody fixed the source skew: pain is not demand.** Before Increment 1 is committed, someone should state **one workflow a stranger wants to run and cannot, without reference to our incident log.**

**(2) The register's answer to harness failure is more harness, and the harness is a single point of total failure.** 125 of 128 abilities make the harness a mandatory participant in every action. Now read the field record: a maintenance tick died and **all maintenance stopped forever with no observable indication** while the server kept serving (`S-08`); 26 zombie processes held build and DB locks unattributably; the Unimatrix rate limiter refused writes mid-run and **reshaped the filing policy around itself** (57 tagged, 3 deferred). **Every one of those is infrastructure failing, and the proposal is more infrastructure.** Exactly one candidate addresses it — C-104's defense-in-depth, single-lens — and W6 files it under a graph contest rather than under the risk. **Nobody asked what the degraded mode is.** For a product serving SDLC and research equally, *"what happens to work in flight when the harness is down"* is the first question a buyer asks, and this run never asks it. **Add it to the probe queue ahead of #7.**

**(3) The sequencing risk is the run's own most expensive object, pointed at itself.** The core claim is *guarantees, not tendencies*. C-91 states the mechanism: inference anywhere on the enforcement path demotes a guarantee to a tendency, and **a tendency presented as a guarantee is the most expensive object in the run.** Stack the facts: the binding principal is **UNDECIDED** (C-5); A-6 is unrun; permissions are unconfigured; and our two real encounters with enforcement both ended in bypass. **If Increment 4 is built before probe A-6 returns, what ships is a beautifully instrumented tendency wearing a guarantee label** — the exact object the register names as the most expensive one it found. **That is why A-6 is probe #1, and it is the one sequencing error here that would be unrecoverable.**

**(4) The reflexive one — and the under-reach call.** This run has spent three consecutive structure-only runs and ~thirty spawns to conclude that the thing to build is **#183** — a node that already exists, `grade:claimed`, SPECIFIED at 5 nodes and 4 edges, stress-tested three times, whose run **closed early with no artifact.** The garage's bottleneck is not knowing what to build. It is that **it has zero `proven` nodes on either board** and its last three runs each ended by mapping more territory.

> **So the step-function is not another ability. It is: the next run must attach an artifact.** Increment 0 — C-35, C-62, C-67 — is the cheapest possible way to get one. Three days, three field failures that already happened, no object model, no architecture decision, and it produces a real artifact against a real `done_when` **regardless of whether the harness is ever built. It buys the funnel a proving ground.** What it costs is that it is unglamorous next to a 128-ability register.
>
> **Worth it? Yes — and it should be a condition of the gate: wfh-004 closes with Increment 0 chartered as a proof-goal, or the garage will map a fifth space before it proves its first.**

*(Per A-4: `factory-retro` covering both wfh-002 — inherited, undischarged — and wfh-004 is due at CLOSE. **This is the fifth place that obligation has been written down.** C-106 is routed `build` specifically so there is a sixth time that is a machine check rather than a paragraph.)*
