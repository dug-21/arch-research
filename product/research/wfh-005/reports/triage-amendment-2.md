# wfh-005 — triage amendment 2

**Append-only (D3).** Does not overwrite `triage.md` or `triage-amendment-1.md`. Where they conflict, the
latest amendment governs.

**Trigger:** owner-directed read of `adrianco/retort`, prompted by the owner's JURATI priority #2 —
*enable multi coding-agent / multi-LLM workflows, and ultimately test and compare outcomes across different
uses.* Evidence: `scout-active-dev-r3.md`. **Budget: 8 of 10–12. Status moves: still 0.**

---

## A. Retort — verdict on the evaluation capability

**ADOPT the ideas and two files. Do not adopt the framework. Do not build a rival.**

Retort is a design-of-experiments harness for measuring coding stacks: factorial designs over
`language × model × tooling × thinking-level`, type-II ANOVA to decompose which factor moves which
outcome, six agent CLIs, thirteen languages. Apache-2.0, very live, and **more honest about its own limits
than most published benchmarks.**

**Why not adopt the framework.** The adoption surface is a laboratory, not a library: bus factor 1
(481 / 7 / 5 commits), **zero releases and zero tags**, twelve runtime dependencies including a compiled
SWIG extension, ~45 MB with the author's own 278 KB SQLite corpus committed to it, a macOS assumption, an
oMLX-on-port-8080 assumption, and a documented **one-experiment-at-a-time-per-machine** constraint because
concurrency corrupts wall-clock invisibly. Against the owner's stated philosophy — smallest usable
footprint, emit into genuine infrastructure rather than rebuild it — **retort is on the wrong side of the
emit/rebuild line: it is not infrastructure we can emit into, it is a peer laboratory with an incompatible
substrate.** Adopting it means adopting a Mac.

**What to take, by name.**
- **`pricing.py`** — 159 lines, zero retort imports, directly liftable, and it already encodes the
  cache-write and reasoning-token semantics we would otherwise get wrong once.
- **The two-opinion challenge gate design** — the second pass is *not* an independent re-roll; it is handed
  the specific requirements the first claimed missing and told to go find the implementation.
- **The tri-state return** — `True` on pass, `False` only when two real opinions both fall short, **`None`
  when the judge could not run**, so an infrastructure hiccup never masquerades as a spec failure.
- **The half-credit flag** on a self-repaired pass.
- **The no-write abort** — three consecutive runs writing zero files stops the whole experiment, because
  *"a model that can't do the task still writes something."*
- **`CLAUDE.md`'s verify-before-you-run principle**, which is prose and free. See §C.

**The seam the owner hoped for does not exist yet.** `retort report optimal --routing-json` looked like the
clean join — retort measures offline, JURATI consumes the routing table online. **It is not a contract.**
No `version` key of any kind; the documented schema is **wrong in three places** against the code that
emits it (an extra nesting level, an undocumented sixth field, and a `pass_bar` the source comment
explicitly rebuts); a backward-compatibility shim for a shape that already changed **under zero consumers**;
the producer hardcoded to one repository's `master.db`; candidate stacks hand-curated as nine entries in a
Python source file; and the only test pinning the shape **skips when the database is absent**. Blast radius
if retort refactors: total.

**The differentiation stated last turn survives and is now located.** Retort's spec gate is an LLM judge,
and the project measured its own instrument: across **22 paired reads of identical code,
`requirement_coverage` moved by a mean of 0.18 and as much as 0.92** — on a metric whose pass threshold is
exactly 1.00. Worse for us, the challenge design deliberately trades independence for targeted
verification, which reduces false *failures* and structurally raises false *passes*. The README's own
admission is what that looks like: runs scoring 1.00 that carry *"a correctness defect the requirement
checklist does not catch."* **Comparison anchored to artifact-backed proof rather than a model's opinion is
the real gap, and it is ours to fill.**

**One counterweight the owner should hold.** Retort has run its gate thousands of times and **published how
much it lies**. We have run our firewall zero times and hold zero `proven` nodes. A noisy gate with an
error bar is an instrument; a perfect gate that has never been used is a posture. That is `triage.md`
§6(h)'s conclusion reached a fourth independent way.

**Quotation hazard, binding on us.** Retort's caveats live in `docs/metaharness.md` and a JSON `notes`
block; **the README's headline claims do not carry them**, and 24 of 29 published route records are n=1.
**Any retort figure we cite must carry its `n`.**

**Correction to a claim made earlier in this run.** The leader told the scout that retort's `metaharness`
is unrelated to `ruvnet/metaharness`. That is right about the codebases and wrong about the relationship:
retort's `metaharness` runner shells out to an external solver that **is** ruvnet's, ruvnet is named in
retort's docs as the schema counterparty, and **ruvnet is a contributor to retort with 5 commits**. State it
as: *three things in retort are called metaharness, one of which is a hole shaped like ruvnet's project.*
Round two's find and this one are the same story from two ends.

---

## B. Bearing on the two surviving BUILD legs: none

Retort measures the agent's **output**. Nothing in ~21,000 lines observes the agent's **demand**. The three
things most likely to resemble demand-observation are all negative: the per-run playpen is a temp directory
for reproducibility with **no egress control, no syscall filter, no policy hook** (five of six runners
disable every permission gate on purpose — a bound is a confound when you are measuring capability);
`provenance.json` records the *stack*, not the demand, and is an **unsigned self-report**; `stack.json` is
the input configuration, declared before the run, which is the exact assumption leg (b) exists to escape.

**Recorded as a non-hit rather than inflated into one.** Also recorded: retort's scheduler `budget.py` is an
*experiment* spend cap, not a per-agent authority budget, and does **not** corroborate wfh-004's
cost-enforcement correction.

---

## C. The new position, and it is upstream of both BUILD legs

> **P8 — Nothing in this theme detects a control that is present, configured, believed, and inert.**

Two of the three serious codebases this run has read at depth were shipping controls that were not in force,
for entirely different reasons:

- **ruflo** (amendment 1): a blocking policy chokepoint, monotone envelopes, delegation attenuation,
  receipts, an HMAC trust anchor — **all inert by default**, a propagator with no call sites by its own
  header, and 106 audited environment-variable escape hatches.
- **retort**: **every one** of its five published wrong conclusions came from a parameter that was set and
  never verified to take effect. One of them — a context length silently halved — was **misreported as
  effective by the provenance file itself**, the artifact whose entire job is to record the truth.

**Why the theme cannot see it.** Leg (b) derives a bound from observed demand: if the observation plane is
misconfigured it observes nothing and derives the tightest, most satisfying, most wrong bound available —
and a silent no-op and a perfectly compliant agent produce **identical evidence**. Leg (c) composes
monotonicity with approval: if the enforcement point is in legacy mode, monotonicity holds vacuously and the
approval path is never exercised. **A vacuous guarantee passes every test a non-vacuous one passes.**

It is also upstream of P3. P3 asks whether a model call sits on the deciding leg, whether the decision is
monotone, how large the exemption surface is, whether the friction fits the compliance budget. **All four
presume the decision happens.** `triage.md` §2 reads exemption surfaces — `LOG_ONLY`, `dryrun`, `Audit`,
`threat-detection: false` — as operator choices within a budget. Retort and ruflo say something worse:
**the default was off and nobody chose it.** An exemption surface you know about is a budget. A default-off
enforcement plane is a fiction, and this run has now found two.

### The amendment to the BUILD's done_when

`triage.md` §3 proposed: *given one real run whose demand set was not declared in advance, the system
derives a bound from observed demand, and a subsequent attempt to exceed that bound is refused by a plane
the agent holds no credential for, with the refusal attested.*

**Add, as a precondition rather than an audit:**

> **…and the plane demonstrated that refusal before the run began.** A liveness probe per plane —
> deliberately attempt one action the ceiling forbids, confirm it is refused by the plane that should
> refuse it, record the refusal. And the artifact recording a plane's configuration must record the
> **effective** value, never the declared one.

Without it, `done_when` is satisfiable by a plane that refuses everything, or by one whose enforcement was
never reached.

### The falsifier is in this repository and costs one probe

Three controls this operation believes it has: the six factory agents' `tools:` frontmatter,
`.claude/settings.json`'s permission rules, and whatever bounds subagents actually run under.
`triage.md` §6(g) already answers two — **no `tools:` frontmatter on any factory agent, and hooks only with
zero permission rules in settings**. The vendor's own tracker (SDK issue #172) says `tools:` would not have
bound a CLI-spawned subagent anyway.

**Read through this position, wfh-004's R2 is not a missing switch. It is the first confirmed instance of
the defect, in our own repository** — the theme is preparing to derive authority bounds for agents while
running five roles under no bound at all. One probe settles it, and it is the same probe as A-3/A-5.

---

## D. Method finding — the third consecutive owner catch

Amendment 1 §C recorded that both verdict-moving corrections in this run came from the owner rather than
from the method. **This is the third**, and it arrived from a direction the first two did not.

Round two's finding was that the active-development surface needs an organization-walk and a low-star pass,
because the incumbent's answer arrives at four figures of stars and the research answer at two. Retort adds
the opposite failure: **it is at 190 stars and would not have been reached by a mechanism-vocabulary search
either.** It self-describes as *"Platform Evolution Engine,"* and its README does not contain the words
*authority*, *permission*, or *capability* in our sense. **The adjacent-domain answer arrives under a name
that shares no words with the query.**

Three instruments the active-development surface needs and does not have: an organization-walk, a
deliberately low-star pass, and **a by-function rather than by-vocabulary sweep** — asking *who else
measures or governs coding agents* without using any of this theme's nouns.

---

## E. What is unchanged

P1, P2, P3, P4 and P5 verdicts: unchanged by this pass. The P4 routing (adopt / assemble / build):
unchanged. The two surviving BUILD legs: unchanged in substance, amended in `done_when`. wfh-004's
shortlist: **untouched**. The firewall: untouched by construction. Everything in this amendment is
`grade:claimed`; none of retort was executed.

## F. Consequence for the proposed re-cut

`product/factory/proposals/workflow-harness-scope-recut.md` gains two things and loses one assumption:

1. **Evaluation is ADOPT-the-ideas, not build and not adopt-the-framework.** The differentiated piece is
   comparison anchored to artifact-backed proof rather than an LLM judge.
2. **The `done_when` carries the liveness probe** (§C).
3. **The routing-table seam is not free.** It was the cheapest-looking join between offline measurement and
   online workflow, and it is not a contract. If the owner wants that loop, we define the schema.
