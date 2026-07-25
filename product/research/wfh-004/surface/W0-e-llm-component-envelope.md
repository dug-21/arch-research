# W0-e — The LLM as a component of a control system: capability and failure envelope

**Run:** `wfh-004` · Issue #48 · phase `scan` (rebuild) · `agent_id: wfh-004-w0e` · read-only, zero graph writes.
**Charter:** SCOPE Amendment A-8 §3. Characterize the component. Not a model evaluation, not a recommendation, no candidate abilities proposed.

**Evidence classes (binding):** `[measured]` published benchmark/study · `[observed]` our own record · `[practitioner]` widely-reported lore without measurement · `[reasoned]` mechanical argument.

**Standing caveat on this partition's own evidence.** Almost every `[measured]` row is a *benchmark* result — a distribution, a task family, and a scoring function chosen by someone else. **Benchmark numbers transfer to a harness as *shape*, not as *rate*.** Where a number appears it is illustrative of shape; **do not carry any figure into a downstream calculation.** That is exactly FP-3's failure mode, and this document is the highest-leverage place to commit it.

---

## 1. The envelope table

| # | Function class | Verdict | Mechanism (why) | Failure presents | Evidence |
|---|---|---|---|---|---|
| F-1 | Translate NL → a formalism with an external checker (code that compiles, JSON matching a schema, a query that runs) | **Reliably good** | The checker, not the model, supplies the guarantee. Model failure becomes a parse/compile error | **Loud** | `[measured]` `[reasoned]` |
| F-2 | Single-label classification, small fixed label set, short input | **Reliably good** | Bounded output space: the model cannot fabricate an out-of-set answer under constrained decoding; error is a wrong choice, countable and comparable. Format restriction *improves* classification | **Semi-loud** — wrong but in-range | `[measured]` |
| F-3 | Extract a span explicitly present in a short provided document, **with a returned locator** | **Reliably good** *conditional on the locator being verified* | The harness can check the span exists at the cited position. Unverified extraction drops to the middle | **Loud if locator checked, silent if not** | `[reasoned]` `[measured]` |
| F-4 | Recall-oriented candidate generation for a downstream filter | **Reliably good** | Precision supplied downstream; the model is used for coverage, where over-generation is the desired bias. LLM+static-analysis hybrids eliminate 94–98% of false positives at high recall | **Loud** — the filter culls | `[measured]` |
| F-5 | Fuzzy/semantic equivalence where the criterion is inherently linguistic | **Reliably good, human-comparable** | No deterministic total function exists over the input; error rate comparable to inter-annotator disagreement | **Silent, but symmetric** | `[measured]` `[reasoned]` |
| F-6 | Prose for a human reader, where a human is the consumer | **Reliably good** | The human is the checking layer, in-loop, at read time | **Loud to the human** | `[reasoned]` |
| F-7 | **Summarization / synthesis feeding another automated step** | **Dangerous middle** | Omission is not represented in the output. Clinical summarisation measured 1.47% hallucination but **3.45% omission** — the more common failure has no artifact | **Silent** | `[measured]` `[observed]` P-16 |
| F-8 | **Carrying a quantitative claim through prose** | **Dangerous middle** | Numbers are tokens; nothing couples a restated figure to its source | **Silent** | `[observed]` P-16 (61×), P-05 (0 vs 38) |
| F-9 | **Semantic verdict over prose against a written criterion (LLM-as-judge)** | **Dangerous middle** | Real signal (≈80%+ human agreement on well-posed pairs) plus *systematic* biases: position, verbosity, self-preference. **Bias is not reduced by sampling** | **Silent, and correlated** | `[measured]` |
| F-10 | **Compliance with its own protocol over a long session** | **Dangerous middle** | Joint compliance across stacked constraints falls below 50% for some models; **terminal constraints are the most-dropped**. CoT can *lower* IF accuracy | **Silent** | `[measured]` `[observed]` P-01, P-03, P-13, P-21 |
| F-11 | **Self-report of what it did / whether it complied** | **Dangerous middle** | Reasoning traces are not a faithful record of the computation: models verbalised a decisive hint 41% / 19% of the time | **Silent by construction** | `[measured]` `[observed]` P-13 |
| F-12 | **Detecting an absence** (a missing step, an unfulfilled commitment, a contradiction across documents) | **Dangerous middle** | Attention is over what is present. **There is no token for the thing that isn't there** | **Silent** | `[reasoned]` `[observed]` P-14, P-19 |
| F-13 | **Planning/decomposing an unfamiliar task** | **Dangerous middle** | Plausible plans are cheap; error surfaces at execution, many steps later. MAST: system-design and inter-agent misalignment are 2 of the 3 top failure categories across 1600+ traces | **Deferred-loud** | `[measured]` |
| F-14 | **Confidence / uncertainty self-report** | **Dangerous middle → worthless in the common case** | RLHF systematically degrades calibration; verbalized confidence tracks formatting rather than correctness | **Silent, actively misleading** | `[measured]` |
| F-15 | **Aggregation / counting / arithmetic over a set in context** | **Dangerous middle** | No accumulator. Counting is emulated by next-token prediction; wrong totals are fluent | **Silent** | `[measured]` `[observed]` P-12 |
| F-16 | **Bounding its own authority** while holding the credentials | **Cannot — in principle** | Self-restriction by the credential-holder is not a weak guarantee, it is not a guarantee (C-4). Every shipped tool achieving this puts the check in a plane the agent has no credentials for | **Silent — a violation is indistinguishable from compliance** | `[observed]` `[reasoned]` |
| F-17 | **Guaranteeing that instructions arriving in data are not executed** | **Cannot — in principle, for this architecture** | Context is one channel; no privileged/unprivileged token distinction. Consensus across major-lab 2025 publications: not solvable at the model layer | **Silent** | `[measured]` |
| F-18 | **Knowing anything not in context or weights** | **Cannot — in principle** | Trivially true and the most-violated assumption in practice (P-27, P-28: the omission is invisible *to the agent*) | **Silent** | `[reasoned]` `[observed]` |
| F-19 | **Bitwise-reproducible output** | **Cannot as normally served** — reducible at ~34% cost | Not sampling: batch-size-dependent reduction kernels. 1,000 temp-0 completions of one prompt gave **80 distinct outputs**, diverging at token 103 | **Silent** | `[measured]` |
| F-20 | **Correcting its own reasoning without external signal** | **Cannot reliably** | Intrinsic self-correction does not improve and sometimes degrades performance; no independent error signal. With external feedback it works — **but then the feedback is doing the work** | **Silent** | `[measured]` |
| F-21 | **Idempotent retry** | **Cannot** | A retry is a fresh sample, not a replay. τ-bench: a >60% pass@1 agent drops to **<25% pass^8** on identical tasks | **Silent** | `[measured]` |

---

## 2. The dangerous middle, expanded

**The organizing property:** a function belongs here when the output is well-formed, the failure leaves no artifact, and the error rate is low enough that spot-checks pass. **A harness routing such a function without a checking layer does not acquire a 5% error rate — it acquires an *unknown and unobservable* error rate, which is a different kind of object.**

| Function | Why it looks dependable | How it actually fails | Detectable? | What a cheap detector must see |
|---|---|---|---|---|
| **F-7 Summarize-for-machine** | Fluent, on-topic, usually right | **Omission**, measured 2.3× more common than fabrication. The dropped qualifier is load-bearing because it was the least redundant token | **Not from the output alone** | Coverage over the *source*: every source claim mapped to present-or-deliberately-dropped. Requires the source to be enumerable — **structure upstream, not a better prompt** |
| **F-8 Number-through-prose** | Numbers are the most confidently stated things a model emits | The figure detaches from its derivation and is restated *by a second agent* with full confidence. **Our own instance:** a 61× wrong figure entered a findings chain, caught only because a POC built an independent instrument | **Yes, cheaply — but only if a predicate was stated in advance** | Every number carries machine-resolvable provenance; the detector re-derives and compares. O(1) vs O(analysis) — the clean case of §5's asymmetry, **and we did not build it** |
| **F-9 Semantic verdict / judge** | 80%+ human agreement on well-posed pairs; disagreements look like taste | Biases are **systematic**: presentation order, length, same-family authorship. **Systematic bias is invariant under sampling** — voting reduces variance, not bias | **Partially.** Order-swap and length-control probes detect position/verbosity bias; self-preference only with a different model family | Two presentations of the same pair and a disagreement rate. **A disagreement rate is the instrument; a single verdict is not** |
| **F-10 Own-protocol compliance** | Behaviour is *mostly* conformant, so the protocol appears to be in force | Compliance decays with constraint count and horizon position; **terminal constraints drop first — and "the last step" is where a harness puts its gates.** Our clearest instance: P-01, a memory file authored specifically to prevent a behaviour, which recurred anyway | **No.** A violation and a compliance produce the same artifact — nothing | An external check at the moment of the constrained action. **No output-side detector exists; structurally a pre-execution problem** |
| **F-11 Self-report** | Explanations are coherent and cite plausible causes | The trace is generated, not recorded. Models act on decisive information and omit it from the explanation the majority of the time | **No, from the report. Yes, from independent observation of actions** | Actions observed outside the model's narration, compared against it. **The narration is not evidence** |
| **F-12 Absence detection** | Asked "is anything missing?", answers confidently and sometimes correctly | Recall over absences is unbounded — the space of things-not-there has no enumeration. P-14: a document contradicting itself twice, undetected 3 days | **Only against an expected set** | A declared expectation at t0 and a set-difference at t1. **The moment such a set exists, the check stops being an inference problem** |
| **F-13 Plan/decompose** | The plan reads well and is usually structurally sensible | Failure surfaces at execution, far from the decision, by which time the plan is the shared premise of every downstream agent | **Deferred** | A cheap dry-run predicate: does every named step reference an existing unit/tool/artifact? Catches referent errors, not judgment errors |
| **F-14 Confidence** | A number in [0,1] with the affordances of a probability | Post-training pushes verbalized confidence high independent of correctness | **Only by ex-post scoring against outcomes** | A stored (confidence, outcome) history. Without one, **treat the number as unavailable — not as weak evidence** |
| **F-15 Count/aggregate** | Arithmetic is what we most expect a computer to get right | No accumulator; totals are predicted. P-12: 17 authorized vs 33 written, never reconciled | **Yes, trivially — recompute** | Deterministic recomputation over the same set. **Requires the set to be addressable, which is exactly what was missing** |

### The cross-cutting mechanism — the most important finding in this partition

**Seven of the nine rows share one shape:** *the model is asked to produce a claim about a body of material, and the harness holds no independent representation of that material against which the claim could be checked.* Where an independent representation exists (F-1's compiler, F-3's locator, F-15's set), **the function leaves the middle immediately.**

> **The dangerous middle is largely a property of missing structure, not of the model.**

Strong for a thesis that wants to move functions off the model — and a warning that **"route it elsewhere" is not the only cure.** "Give the model's output something to be checked against" is a second, distinct remedy for the same rows, and A-8's thesis names only the first.

---

## 3. The irreducibility analysis

### 3.1 Testing C-2 rather than assuming it

**C-2 survives, but it is stated too broadly and gives away more than it must.**

What is genuinely irreducible is narrower: **the mapping from unbounded natural language, authored at an arbitrary time, onto a bounded symbol.** No total computable function from English to truth-values can be authored, and no finite rule-set covers the input distribution `[reasoned]`. A real, permanent boundary for as long as the workflow's inputs are prose.

Three things C-2 does *not* entail:

1. **It does not entail that the question is large.** The irreducible core is a *categorisation*, not an essay. Forced-binary-with-fixed-schema is a different object from a paragraph: bounded output space, comparable across runs, votable, measurably more accurate under format restriction `[measured]`. **How small the question is made is a design variable with measured consequences, not a stylistic choice.**
2. **It does not entail that the verdict must be trusted.** The harness never needs the verdict to be *true*; it needs it **attributable, bounded, recorded before the dependent action, and re-checkable.** Everything in that list is deterministic `[reasoned]`.
3. **It does not entail that the whole judgment is semantic.** Most judgments that present as semantic decompose into a small semantic core plus several existence/equality checks that were only semantic because nobody recorded the fact. *"Does the evidence support the claim at the claim's altitude"* contains: does the cited artifact exist (deterministic) · does the locator resolve (deterministic) · does the number in the claim equal the number in the artifact (deterministic) · is the artifact's altitude the claim's altitude (**semantic, binary, small**).

### 3.2 How small can the question be made

| Form | What the harness guarantees regardless of answer quality | Support |
|---|---|---|
| Free prose verdict | That a call happened | — |
| + fixed schema, enumerated answer set | In-range, parseable, comparable across runs, storable as a typed value | `[measured]` |
| + minimal evidence span instead of whole document | Reduced length-degradation exposure; the exact bytes shown are recorded and replayable | `[measured]` |
| + required locator the harness resolves | Converts an unverifiable verdict into one with a machine-checkable component; **a hallucinated citation becomes loud** | `[reasoned]` |
| + reasoning emitted separately from the answer field | Recovers most of the accuracy constrained decoding costs on reasoning items | `[measured]`, **contested** |
| + N independent samples with a disagreement threshold | An *observable* disagreement rate — a signal even when the majority answer is wrong | `[measured]`, with the bias caveat |

**The guarantee the structure buys, precisely:** that a question was asked, of which model version, with exactly what shown, that an in-range answer was returned, that it was durably recorded *before* the dependent action executed, that the dependent action was gated on the recorded symbol rather than on prose, and that the whole tuple is replayable. **None of that requires the answer to be correct** — and it is a larger determinism budget than C-2's phrasing suggests.

### 3.3 The pseudo-irreducible (P) reservoir — where it bites hardest

**The diagnostic:** was the information needed to decide deterministically known to something in the system at the moment it was true, and simply not written down? If yes, the later inference call is (P), not (I).

| Pain | Needs inference because… | Deterministic if… |
|---|---|---|
| P-12 (17 authorized / 33 written) | The authorization was a sentence | The authorization is a typed count; the check is arithmetic |
| P-13 (a declared role never ran) | "Which roles ran" is recoverable only from a transcript | Roles are a declared set, spawns are recorded; the check is set-difference |
| P-19 (dropped retro obligation) | The commitment was prose in a close-out | A commitment is a record with a carrier and a due condition; the check is a query |
| P-21 (14.8% of calls after completion) | "Completion" was a statement in text | Completion is a state transition with a timestamp; the check is a comparison |
| P-08 (duplicate Issue for one run) | Nothing held "one run ⇒ one surface" | A uniqueness constraint on a run-id |
| P-05 / P-16 (0 vs 38; 61×) | Consumption reconstructed from transcripts by a parser | Each call emits an attributed usage record at the moment of the call |
| P-03 (out-of-scope workstream ran) | Scope boundaries are prose | Scope items are addressable IDs; the residual semantic core is a *tiny* binary |

> **The general law:** *inference is being used as a lossy reconstruction of information that existed earlier and was discarded.* `[reasoned]`

The bite is worst exactly where our record is worst — Introspection (12 pains) and Structure (14) — and **not** where the field assumes it is (judging prose quality). Note the asymmetry for a build decision: **collapsing (P)→(D) is not a modelling problem at all, it is an emission-and-schema problem**, and the cost falls on whoever writes the producers.

**Honest limit.** P-15 is the counterexample and it is severe: subscription quota is emitted by the provider at *no* granularity. **When the producer will not emit, the information was never in the system, and no amount of harness determinism recovers it.** (P) presumes we own or can instrument the producer.

---

## 4. The reliability levers — measured vs folklore

| Lever | Mechanism | Verdict | Class |
|---|---|---|---|
| **Constrained decoding / fixed schema** | Removes malformed output from the failure space *entirely* — mechanical, not probabilistic. Does **not** touch correctness | **Real for parseability; null for correctness.** Contested for reasoning; both readings agree on the mitigation (reason free-form, then emit into the schema) | `[measured]`, contested |
| **Forced binary / small enumerated answer set** | Shrinks output space so failure is a wrong choice not an unbounded fabrication; makes voting and disagreement-rate measurement possible at all | **Real**, and the **highest structure-to-cost ratio lever available** | `[measured]` `[reasoned]` |
| **Small context / minimal evidence span** | Length-degradation is measured independent of position: accuracy falls as input grows even with evidence fixed and favourably placed | **Real and underrated.** Caveat: much of the sharpest literature is vendor/practitioner rather than peer-reviewed | `[measured]` / partly `[practitioner]` |
| **Decomposition into checkable steps** | Each step's output is small enough for a predicate to exist. Decomposition + per-step verification + voting drove a million-step task to ~zero error | **Real, with a named cost:** decomposition moves error to the *seams*. MAST's largest failure category is inter-agent misalignment. **You trade an in-step error rate for a join error rate, and the join is usually unmeasured** | `[measured]` |
| **Self-consistency / N-sample voting** | Wrong chains disagree; right chains converge. **Reduces variance, not bias** | **Real but shrinking and conditional.** Gains flatten by N≈5–10; on frontier models, 0.4% (HotpotQA) and 1.6% (MATH-500) across 20 samples at near-linear cost. **Useless where error is systematic — precisely F-9, F-11, F-14** | `[measured]` |
| **Intrinsic self-critique ("check your work")** | — | **Folklore, and measurably harmful in some settings** | `[measured]` — one of the few places lore is directly contradicted |
| **External-feedback critique** (compiler, tests, schema, a resolver) | The feedback carries ground truth the model does not have | **Real, and the single strongest lever** — but the guarantee comes from the checker, not the model | `[measured]` `[reasoned]` |
| **"Think step by step" as a general reliability improver** | — | **Contested and task-dependent.** Measured to *reduce* instruction-following accuracy across 20+ models while helping reasoning items | `[measured]` |
| **Emphasis, repetition, capitals, "IMPORTANT:", memory files** | — | **Folklore.** Our own direct counterexample: **P-01** — a dedicated out-of-repo memory file written to stop a behaviour, and the behaviour recurred at the next run's gate | `[practitioner]` refuted `[observed]` |
| **Version pinning** | Removes silent distribution shift from the failure space | **Real and mechanical.** Separately: >60% of 63 studied APIs showed substantial performance change over time; 58.8% of prompt+model combinations lost accuracy across updates | `[measured]` |
| **Bigger/better model** | Raises the ceiling | **Real for rate, null for shape.** Every failure class in §2 persists at frontier; the horizon lengthens, **the envelope's geometry does not change** | `[reasoned]` |

---

## 5. The verification asymmetry

**Where it holds — the basis for any cheap checking layer:**

- A **machine-checkable predicate exists** over the output: compiles · parses · schema-validates · tests pass · locator resolves · referenced ID exists · number equals recomputed number · set membership. Cost O(1) against O(generation), and **the check is total — it never has an opinion.**
- A **second model armed with a tool the generator lacked.** The asymmetry comes from the tool, not the second model.
- The **generation–verification gap is real in reasoning domains** — but note the framing in that literature: the gap is being *shrunk* by aggregating many weak verifiers, i.e. **a single weak verifier is not enough.**

**Where it fails — four named cases:**

1. **The failure is an omission.** There is nothing in the output to check. Verifying an omission is *the same work* as generating, since you must traverse the source. **Kills the asymmetry for F-7 and F-12 — the two silent-est rows.**
2. **The verification is itself an unbounded semantic judgment.** A prose judge inherits the whole §2 envelope and adds position, verbosity and self-preference bias. Checking is then not cheaper — **same cost, new bias.**
3. **The error is systematic and shared.** Same family, same prompt frame, same training distribution ⇒ correlated errors between generator and verifier. **Independence must be bought** (different family, different framing, different presentation), not assumed.
4. **No ground truth exists yet.** For a novel research claim, verification and generation are the same act. **The garage's own domain sits here more than most.**

**The instructive case from our own record:** P-16 is the asymmetry at its most favourable — the check was vastly cheaper than the analysis that produced the wrong number, and worked immediately once built. It was not built for months because **no predicate had ever been stated.** *The asymmetry is not self-executing; it requires someone to have written down, in advance, what would have to be true.*

---

## 6. The cost of minimization — argued against the thesis

1. **Rules fail closed on the unenumerated; models degrade gracefully.** Regex-only security-document classification measured 52.7% against a fine-tuned model's 95.0%, with a 100pp gap on one category `[measured]`. A deterministic path that has never seen a case returns nothing — and **"returns nothing" in a control system is often indistinguishable from "no problem here."**
2. **The measured wins are frequently near-ties with a huge cost asymmetry in the *deterministic* direction.** BI-RADS: regex 89.20% vs LLM 87.69%, not significantly different, regex **28,120× faster** `[measured]`. Read honestly this cuts *for* the thesis on narrow well-specified extraction — and warns the payoff is **domain-shaped, not universal.**
3. **Somebody must author and maintain the deterministic path.** Every schema change is a code change. The model absorbs drift for free; a rule-set must be told. A standing tax proportional to how fast definitions evolve — and A-6 says definitions are the fast-moving layer.
4. **Collapsing (P)→(D) requires instrumenting every producer.** A coupling decision, not a local one. P-15 shows the failure mode when a producer refuses. **The (P) reservoir is an opportunity surface *and* a large distributed-engineering bill.**
5. **A wrong rule is wrong systematically; a wrong model is wrong stochastically.** The most counter-intuitive cost, and it is real: stochastic error is *detectable by repetition* (disagreement rates, voting, pass^k); **a deterministic error is invisible to every statistical instrument you might point at it and will be reproduced identically forever.** Minimizing inference can **reduce the observability of the residual error while reducing its rate.** FP-1 is already a version of this in our record: a written rule looked like a control and enforced nothing.
6. **Removing the model removes the recall.** The best-evidenced use of the component is F-4 — over-generate, then filter. **A deterministic filter with no generator has nothing to filter.**
7. **The human-facing surface is prose.** Steering, intent, correction and explanation all arrive in natural language. Requiring the human to speak the harness's formalism is C-3's "fight the ecosystem" cost one level up — **a minimization that pushes the formalism onto the human has moved the translation problem to the most expensive processor available.**

**The one place the thesis is unambiguously right, stated as its mechanism:** a *guarantee* is statable only over a path with no inference on it. Any inference on the enforcement path demotes a guarantee to a tendency, **and a tendency presented as a guarantee is the most expensive object in this document** — F-16 and F-17 are exactly that. The entire shipped field agrees by revealed preference: `[observed]` every enforcement mechanism across ~30 tools sits **outside** the model, and **zero** ship a defense against instructions arriving through data.

---

## 7. Expiry flags

**Properties of today's models** — needing re-check, with expected drift:

| Finding | Why it may expire | Direction |
|---|---|---|
| Self-consistency gains are small (0.4–1.6% at N=20) | Already expiring — worked much better on 2022-era models | Gains keep shrinking |
| Constrained decoding degrades reasoning | Contested; providers engineer around it | Likely fades; the parseability guarantee does not |
| CoT hurts instruction-following | Artifact of current post-training recipes | Unstable either direction |
| Specific horizon lengths, pass^8 <25% | Horizon doubling every ~4–7 months | Lengthens fast |
| Verbalized confidence carries no information | Targeted by calibration-aware research | May improve; **treat as unreliable until measured on our own distribution** |
| Long-context degradation onset | Moves with architecture and serving | Improves, unevenly |
| Hallucination/omission rates | Domain- and model-specific | Improves; **the ordering (omission > hallucination) is more durable than the rates** |

**Properties of the technology class** — expected to hold across generations `[reasoned]`; a harness design may lean on these:

- **F-16 / C-4** — no entity can bound its own authority while holding the credentials. Not a model property; a property of authority.
- **F-17** — one undifferentiated context channel means no architectural separation of instruction from data. **Expires only if the *architecture* changes, not if the model improves. Watch for this specifically — the single most consequential possible expiry in this table.**
- **F-18** — no context, no knowledge.
- **F-21 / F-19** — sampling is not replay; determinism must be bought, not assumed.
- **F-11** — a generated explanation is not a recording. Faithfulness may improve in degree; **the category difference between "narrated" and "observed" does not.**
- **F-12** — attention operates over what is present; absence has no token.
- **Voting reduces variance, not bias** — a statistical fact, not a model fact.

---

## 8. Flags for the leader

- **Under-claimed deliberately.** Every measured figure is benchmark-shaped and does not transfer as a rate to this harness's distribution. **If any downstream candidate rests on a *number* from this document rather than a *shape*, that is FP-3 reproducing through this partition, and it should route `needs-a-probe`.**
- **One finding cuts against the run's own framing:** the dangerous middle is largely produced by *missing independent representation of the material*, not by model weakness. **"Route it off the model" and "give the model's output something to be checked against" are two different remedies for the same rows, and A-8's thesis names only the first. Both belong in the frame.**
- **Not investigated, and it matters:** small/local models as a distinct component class (different cost and latency envelope, therefore different placement in a control system), and fine-tuning as a reliability lever. Genuinely open.
- **Contested claims not resolved:** the size of the constrained-decoding penalty; whether "context rot" is distinct from positional degradation; whether decomposition's seam-error exceeds its in-step gain at harness scales. All three would change design conclusions; none is settled.
