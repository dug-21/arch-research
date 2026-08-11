# jurati-001 — REPORT

**Status:** synthesis

**Issue:** #58

**Confidence required:** validated

**Feasibility verdict:** **SCOPE FAIL**

**Premise verdict:** **inconclusive — neither supported, narrow, nor refuted**

## Bottom line

The run demonstrated a bounded executable decision-contract checker/reducer: once clause results are
accepted, the contract selects a reproducible verdict and predeclared action; malformed or widened judge
responses fail closed. It did **not** measure whether semantic clause judgments were correct, whether they
matched historical verdicts or next actions, or whether a semantic production policy avoided false
advancement.

The failure was in the frozen proof schema. References exposed an episode verdict and exact next action;
predictions exposed one synthetic clause result. Opaque episode identity was their only common field. A
post-hoc mapping would have invented an evaluator after seeing results, violating the freeze. Required
agreement, safety, and routing measurements were therefore unavailable rather than low or zero.

## What was demonstrated

- The Python 3.14.6 interpreter/checker passed **14/14** tests, including known-green/red cases, evidence
  integrity, transition completeness, response confinement, prompt-injection fixtures, counterfactual
  locality, and fresh-process replay.
- Arm A ran **225/225** planned mechanical reductions: **45 episodes × 5 repetitions**. Every residual
  semantic clause escalated, repeated-run disagreement was **0/225**, and observed advancement was
  **0/225**. This measures conservative mechanical behavior, not semantic false-advancement performance.
- Arm B planned/attempted/accepted **11/11/10** local-model calls.
- Arm C planned/attempted/accepted **55/51/50** calls. Four repetitions were not run after the first
  response for one episode failed closed.
- Across B/C, **60** predictions were accepted. Two responses cited undeclared evidence and were rejected
  before append, without retry or repair.
- Arm C had **10** complete five-repetition episode groups; result disagreement was **0/10** (95% Wilson
  interval **0.0–27.8%**). This is internal repetition consistency, not reference accuracy.
- The recorded local envelope was Ollama **0.32.5**, `qwen2.5-coder:32b` digest `b92d6a0b...`, prompt hash
  `b54c86a3...`, and policy hash `3649607c...`.

## Failed proof gate

The terminal independent validator ruled **SCOPE FAIL** at commit `a415d6c`, reviewing builder commit
`ed81b1d` and independent custody/scoring commit `871466d` on top of frozen candidate `baf03aa`.

The following approved measurements had no common reference/prediction field and could not be computed:

- clause-result agreement, confusion matrix, or macro-F1;
- exact historical verdict agreement;
- exact next-action agreement in either domain;
- semantic-policy false advancement;
- unsafe guesses avoided or unnecessary escalations introduced;
- the 90% reliability qualification; and
- least-cost reliable policy by semantic clause class.

The shared language did run over both domains, but that is not proof of cross-domain historical-decision
coverage. The garage holdout also yielded only two valid episodes per local arm, and one semantic episode
group was incomplete. Frontier arms D/E remained blocked by the absence of a provider and eligible pinned
snapshot. Human arm F remained blocked by the absence of two assigned raters and an adjudicator. Host
hardware, model residency, energy, and monetary cost were not measured.

## Firewall ruling and Unimatrix

| Subject | Current graph identity | Grade | Ruling |
|---|---:|---|---|
| Evidence-bound decision evaluation and deterministic next-action resolution | capability **#256** | `missing` | Unchanged. Its expressibility, semantic safety, and per-domain agreement `done_when` clauses were not demonstrated. |
| Jurati Decision Contract Language v0.1-dev | technology **#257 → #263** | `partial` | Bounded to the checker/reducer, evidence confinement and fail-closed parser, fixed-result deterministic replay, and recorded local Ollama operational envelope. Never `proven`. |
| Synthesis position | finding **#264** | n/a | Records the inconclusive premise ruling and follow-on direction; `Motivates` → #263. |

The artifact envelope is recorded on active technology #263 as `demonstrated_envelope`, not as
`proven_by`. No capability or technology was marked `proven`.

## Interpretation

“Deterministic after judgment” survived at its bounded altitude: accepted results can be reduced and
routed without letting the judge change evidence, authority, verdict algebra, or transition. That is a
useful control-plane primitive, but it does not establish delivery quality. The experiment did not test
whether the semantic judgments inside that envelope were right.

Accordingly, this run cannot classify the broader Jurati premise as supported, narrow, or refuted. It
proved one downstream mechanism while failing to score the upstream quality claim.

## Recommended follow-on

The primary follow-on is the proposed **product-authority control wedge** in
`product/factory/proposals/jurati-product-authority-control-wedge.md`:

1. enroll a cryptographically authenticated product principal;
2. bind product vision and an approved capability-roadmap digest to that principal;
3. permit design to propose capabilities and amendments while denying delivery every goal/capability
   mutation path;
4. test Unimatrix-local enforcement, a Jurati-mediated universal hook, issued capabilities, and a hybrid
   without presupposing which architecture wins; and
5. require zero unauthorized committed graph mutations while preserving legitimate product/design work.

This moves the quality boundary upstream: the implementation authority cannot rewrite its own goal or
success bar. It also directly evaluates identity, delegation, authorization, replay, bypass, expiry, and
audit controls already latent—but unenforced—in the ecosystem.

If semantic decision accuracy is revisited, use a smaller fresh, cycle-disjoint corpus with independently
adjudicated reference labels at the **same clause, verdict, and next-action fields** emitted by every
prediction. Demonstrate the scoring pipeline end-to-end before adding frontier arms. Preserve #263 as a
partial checker/reducer result; do not reuse this holdout as if untouched.

## Evidence envelope

- Scope and preregistration: `product/research/jurati-001/SCOPE.md`
- Terminal validator report: `product/research/jurati-001/reports/gate-feasibility.md` at `a415d6c`
- Operational results: `product/research/jurati-001/artifacts/RESULTS.md` at `ed81b1d`
- Independent custody score: `product/research/jurati-001/artifacts/ARM-BC-CUSTODIAN-SCORE.md` at `871466d`
- Frozen executable candidate: `baf03aa`
- Product-authority proposal: `product/factory/proposals/jurati-product-authority-control-wedge.md`

No restricted holdout labels, reversible identity mapping, custody key, or real source paths are included
in this synthesis.
