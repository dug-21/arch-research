# REPORT — wfh-002 (close-out)

**Run:** `wfh-002` · Issue dug-21/arch-research#46 · cycle topic `wfh-002` · method stamp `wf-v0.16`
**Scope:** the minimal typed ontology of a coding-agent's operating context (P10 probe)
**Confidence-required:** `validated` · **Delivered:** structure only
**Verdict:** **CLOSED EARLY (owner-directed, 2026-07-25) — reset to a broader investigation of the problem space.**

---

## 1. The call

wfh-002 is closed without proof. W4 — the template artifact, the only workstream that could move the
firewall — was never executed, so the §6 proof bar was never met. **No artifact, no `proven`; H4
(ontology-first) remains `grade:claimed`.**

This is **not** SCOPE-FAIL. W1–W3 and W5 each returned a usable, honest verdict and the coverage they
were asked for. The close is an owner decision: the run began choosing an architecture before the
product's full purpose was defined, so the next increment is a wider problem-space investigation, not
a deeper build on a premise that was never settled.

## 2. What the run produced (durable — purpose-independent)

| Workstream | Output | Verdict |
|---|---|---|
| W1 | Ontology spec — 5 node types / 4 edge types, + 7 pre-registered stress points | specified |
| W2 | Round-trip of this repo's `.claude/` through the vocabulary | **PASS-WITH-GAPS** — 6 behavioral, 2 byte; only G-A (LLM-arbitered gates) and G-B (missing condition construct) are genuine vocabulary holes |
| W3 | `AGENTS.md` subsumption | **SUBSUMES** non-vacuously — file→graph lossless; graph→file total-but-projective; ≥2 divergent precedence semantics in the wild |
| W5 | Second-domain round-trip (our own research method, from its prose design) | **AGNOSTIC-WITH-GAPS** — SDLC-locked ruled out; 3 structural general-workflow holes (graded state, budget envelope, convergence loop) + prose leakage |

Incidental but load-bearing: **#179** — this repo's cardinal invariants (single-writer, plan-only, no
`git add -A`) are 100% unenforced prose: zero permission rules, zero enforcing hooks.

These four verdicts stand on their own evidence and survive the close. They are already in the graph.

## 3. What the run did not produce

- **W4 — the P10 template artifact.** Not started. It was gated first on W5, then on a v0.3
  structural decision, then on W6's architecture question. The gate chain outran the run.
- **Therefore: no movement on the firewall.** H4 stays `claimed`. Nothing in this run is `proven`,
  and nothing in it should be.

## 4. Why it closed — the process defect

Architecture was chosen before the product's purpose was defined. The mechanical expression:

**W6 ran outside the scope, without an amendment.** §7 of `SCOPE.md` explicitly placed the
runtime/execution engine out of scope — *"the queen's job, not this scope"* — and the delivery/tenancy
model with it. W6 then decided precisely that boundary (Option C: the graph declares, the queen
evaluates). W5, by contrast, was formally amended in on 2026-07-24; W6 never was. It appears in no
workstream list.

The guardrail existed, in writing, in this run's own scope document, and did not hold. **Finding #179
— produced by this run, days earlier — is the diagnosis of its own close-out:** an unenforced prose
invariant is not an invariant. Recorded here as the honest read; the method-plane response is the
successor session's call, not this close-out's.

Secondary, upstream: a `validated`-confidence scope was opened against a theme where wfh-001 had
established the moat but not the product purpose. Nothing in the scope gate asks whether the purpose
is defined well enough for the proof bar to mean anything — which is why W6 felt necessary mid-run.

## 5. Disposition of W6 (what is provisional)

- **Option C (graph declares / queen evaluates) is recorded as provisional and NON-BINDING.** It is
  retained in `FINDINGS-W6-architecture.md` and `architecture-option-c.html` as reasoning trail, and
  graphed as a `position` finding explicitly marked not-settled. It does **not** bind the successor —
  a decision taken before the purpose was defined does not get to inherit the authority of one taken
  after.
- **One durable constraint is kept on its own merit:** a rules engine inside the knowledge substrate
  violates the jurati#12 / ADR-008 enforcement seam — rule *evaluation* is queen-side. This is
  independent of which product purpose lands.
- **The H4 boundary correction** (the ontology *declares* its operating context and *references*
  governance by name; it does not own governance) is folded into the ontology node's narrative as a
  refinement, not a proof.
- `SPEC-v0.3-delta.md` remains superseded by W6, as recorded there.

## 6. Graph state at close

Written by `factory-curator` (single-writer firewall); detail in `curation-ledger.md`.

- Ontology technology node **#180 → #183** — **`grade:claimed`, unchanged.** Corrected to record the
  early close, that W4 was never built, and that the forward path is gated on the successor's purpose
  definition (replacing the now-dead "gated on the v0.3 structural decision" line). W1/W2/W3/W5
  stress-test record kept intact; 7 incoming `Motivates` redirected.
- Findings from W2/W3/W5 (#177, #178, #179, #181) — unchanged, still valid.
- Two findings added at close: **#184** — the Option C `position`, tagged `provisional` /
  `non-binding`; **#185** — the queen-side-evaluation constraint (durable, purpose-independent). Kept
  as two nodes deliberately: #185 binds the successor, #184 explicitly does not.
- **No grade moved anywhere. No `proven`. The firewall is untouched.**

## 7. Handoff

The successor is a **broader investigation of the problem space**, run in a separate session. wfh-002
hands it **evidence, not an architecture**: a stress-tested vocabulary with a characterized gap list,
a subsumption result against the de-facto standard, a domain-agnosticism result, and one architecture
option that is explicitly not a decision.

**Deferred by owner, not performed in this close-out:** the `factory-retro` method-plane extraction
(lessons, enhancements, `OBS-*`) and any `wf:` bump. Method-stream work belongs to the successor
session.

## 8. Surfaces closed

- **Cycle** — `context_cycle stop` on topic `wfh-002`.
- **Issue** — #46 closed with this verdict.
- **Git** — research-stream PR from `research/wfh-002`, `Closes #46`.
