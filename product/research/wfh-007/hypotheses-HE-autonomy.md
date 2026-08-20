# hypotheses — H-E · progressive autonomy under an attention ceiling

**Run:** wfh-007 · Issue #64 · `wf-v0.24` · agent `wfh-007-hE-hypothesizer` · 2026-08-20
**Inputs read:** OWNER-DIRECTION.md (§5–§7, §12), scout-merged.md (Cluster G ground, read first), scout-active-dev.md (ruvnet teardown at depth). **Status moves: 0. Nothing below is graded, decided, or recommended. Every item is a `claimed` conjecture with a named mechanism and a falsifier.**
**Input-quality flag:** scout input is thick and honest; no thin-input caveat needed. One caveat of my own: hypotheses touching `context_cycle` fields assume the capability surface as handed to me (15 tools, phase-boundary records with outcomes, OBS-10 retention); each such hypothesis carries a falsifier that checks the assumption rather than leaning on it.

U throughout = Jurati Core's progressively-autonomous fleet, with the garage as the live dogfood instance.

---

## A. The track record as a data structure (§5.7)

**H1 — Gate-event stream ≠ audit log; capture at presentation time.**
*Statement:* `context_cycle` outcome records (T) could enhance §5.7's track record (C) of U by treating every owner gate as a phase boundary whose outcome field carries a typed disposition — approved / denied / modified / expired / escalated — plus consequence class and elapsed owner time, stamped when the gate is presented, not reconstructed later.
*Mechanism:* the garage already emits phase-boundary records with outcomes; a gate is a phase boundary. Audit says what happened; the track record must also say what was *asked and refused*, which only the gate mechanism itself witnesses.
*Falsifier (cheapest test):* attempt to backfill one month of gate dispositions from Issue #64 history alone. If denials, modifications, and owner latency are recoverable, write-time capture is unnecessary; prediction: they are not, which is the proof that this can never be backfilled.
*Class:* obvious · *level-up:* linear · *Clusters:* G, D.

**H2 — Denials are the scarce asset, and only a deterministic policy plane produces them.**
*Statement:* an OpenShell-style enforcement plane (T) could enhance the near-miss record (C) of U by emitting structured denial events as a side effect of enforcement — the S1 grid already credits OpenShell with "denials are logged."
*Mechanism:* a prompt-level refusal leaves no artifact; a policy-engine DENY is a machine event with principal, action, resource, and rule id. §5.7 explicitly demands near misses; near misses *are* denials plus intercepted intents. No deterministic decision point → no denial stream → the track record is structurally incomplete no matter how diligently successes are logged.
*Falsifier:* count structured denial records the current garage can produce in one week. Prediction: zero — every refusal today is conversational. One non-zero week kills the hypothesis's urgency.
*Class:* adjacent · *level-up:* step-function (an event class that cannot exist otherwise) · *Clusters:* H, G, A.

**H3 — Bootstrap the consequence vocabulary now from Cluster B's shipped taxonomies; don't wait for the architecture scope.**
*Statement:* Revisable-by-Design's four-way taxonomy (idempotent / reversible / compensable / irreversible) composed with Apple's three-level `IntentAuthenticationPolicy` (T) could enhance the action-and-consequence indexing (C) of U by giving the track record a coarse write-time class tag today, even though the real vocabulary is deferred to a later architecture scope.
*Mechanism:* records tagged coarse can be re-binned finer when the real vocabulary lands; untagged records can never be binned at all. The asymmetry means a provisional vocabulary has positive value even if 100% superseded. This is the answer to "what is buildable now vs. must wait": the *index* can start now; only the *graduation semantics over the index* must wait.
*Falsifier:* tag 20 recent garage actions with the four-way, owner and agent independently. Low inter-rater agreement kills it — a class two raters can't agree on can't anchor "same consequence class" counting.
*Class:* adjacent · *level-up:* linear but unlocks H6/H7 · *Clusters:* B.

**H4 — Near misses require declared-intent-before-authorization; the record is the delta.**
*Statement:* the TBAC-lineage pattern of intent declared before authority (T, Cluster C's settled base) could enhance near-miss capture (C) of U by making every gated action state its intended effect machine-readably *before* the gate, so the record can store the counterfactual — what would have executed absent the gate — which is the substance of a near miss.
*Mechanism:* without a pre-gate intent artifact, a "near miss" is an anecdote; with one, it is a diff between declared intent and disposed outcome.
*Falsifier:* inspect current garage gate presentations: is the intended action stated in any structured form before approval? Prediction: free prose only.
*Class:* non-obvious · *level-up:* step-function for the near-miss category specifically · *Clusters:* C, D.

**H5 — Reversals are minable from git, until they aren't.**
*Statement:* git history mining (T) could enhance the reversal record (C) of U by detecting owner reverts/removals of agent-authored commits mechanically — the one §5.7 record type that may be *partially* backfillable.
*Mechanism:* a reversal after acceptance leaves a revert commit touching agent-authored content; authorship metadata plus revert detection recovers it.
*Falsifier:* script the scan over this repo's main. If reversals in practice happen conversationally (owner tells the agent to redo it, no revert artifact) the miner returns empty against known reversals — proving reversals also need an explicit write-time event.
*Class:* adjacent · *level-up:* linear · *Clusters:* G.

**H6 — Name the object: the track record is a calibration corpus, not audit and not memory.**
*Statement:* framing §5.7's structure as a labeled calibration dataset — rows of (declared intent, class, disposition, outcome, owner time) used to fit and later challenge the trust function (T = calibration-corpus discipline from measurement science) — could enhance retention and sensitivity policy (C) of U.
*Mechanism:* the naming settles three design questions mechanically: retention (keep forever — it appreciates, unlike working context), sensitivity (it encodes the owner's judgment patterns — among the most private data in the system, per §6's exposure failure class), and write discipline (labels at event time, per H1–H4). Audit is immutable history; memory is knowledge; a calibration corpus is *training signal about the owner-fleet boundary* — a third thing the current design vocabulary lacks.
*Falsifier:* if the three policy questions get different answers when derived independently (e.g., owner rules track-record rows deletable-on-request like working context), the framing is wrong.
*Class:* non-obvious/whitespace · *level-up:* linear (a lens) · *Clusters:* G, D.

---

## B. Making trust graduation computable (§5.7, without moving the owner's activation authority)

**H7 — The graduation recommendation is a SELECT, never a stored judgment.**
*Statement:* typed event records (T, from H1–H5) could enhance trust-graduation recommendation (C) of U by making the recommendation a deterministic query result: n eligible runs in class · denial rate · intervention count · near-miss list · reversal list · the precise new authority *expressed in the policy engine's own language* · a policy diff before/after. The owner activates; the machine only assembles.
*Mechanism:* a query inherits the record's integrity — the agent cannot narrate its way to graduation, which is precisely the property §5.1 demands (no LLM as final authority) applied to trust expansion itself.
*Falsifier:* compose the report today for one recurring garage action class ("commit research documents to main"). Enumerate missing fields. Prediction: eligible-run count is approximable; denials, near misses, and owner time are absent (per H2/H22). The enumeration *is* the buildable-now backlog.
*Class:* obvious given §5.7's own wording · *level-up:* linear · *Clusters:* G, D.

**H8 — Eligibility is a write-time stamp; ambiguous runs never count.**
*Statement:* the garage's own `wf:` version-stamping discipline (T, OBS-10 lineage) could enhance the "twenty eligible runs" counter (C) of U by stamping each run eligible/ineligible-for-class-X at execution time — a run whose class was ambiguous while it ran cannot be promoted into the count later.
*Mechanism:* retroactive classification is exactly the self-serving reconstruction §5.7 exists to prevent; stamping is the same move that made retention work on cycles.
*Falsifier:* retroactively classify the garage's last 20 runs into action-and-consequence classes and measure the ambiguity rate. A near-zero rate would show retroactive counting is safe and the stamp unnecessary.
*Class:* adjacent · *level-up:* linear · *Clusters:* B, G.

**H9 — Graduation counters must reset or discount on model, policy, or class-boundary change.**
*Statement:* hash-pinning the constitution and model id into every run record — ruvnet's `autogenous` pattern (T), which the garage's own "model pinned when a prompt change is measured" rule already mirrors — could enhance the integrity of the twenty-run baseline (C) of U by making the counter provably *about the same system* across runs.
*Mechanism:* "same action and consequence class" silently assumes "same actor under the same rules"; a model swap or policy edit changes the actor. Without pins, twenty runs can span three effectively different systems and the count is fiction.
*Falsifier:* check whether current cycle records carry model id and policy/config hash alongside `wf-v0.24`. If they already do, this is free; if the owner rules that counters should survive model swaps, the hypothesis is wrong about the semantics.
*Class:* adjacent · *level-up:* linear · *Clusters:* D, H.

---

## C. Bounding gate load (the attention ceiling itself)

**H10 — Gate coalescing over consequence classes: review the distribution, not the events.**
*Statement:* consequence typing (T, Cluster B) could enhance owner gate throughput (C) of U by letting the system present *batch dispositions* — "14 actions of class reversible-repo-write this week; 2 outliers, here they are" — instead of 14 gates.
*Mechanism:* outlier presentation requires a type to be an outlier *against*; this is the attention-side payoff of Cluster B, independent of its safety payoff. HA's head-heavy distribution (top 84 integrations cover 80% of installs) is the empirical shape: attention belongs on the head and the anomalies, not the uniform tail.
*Falsifier:* log one garage week of would-be gate events and cluster by class. If events don't cluster (flat distribution), batching saves nothing.
*Class:* adjacent · *level-up:* step-function on gates/day if distribution is head-heavy · *Clusters:* G, B.

**H11 — Unanswered gates expire into default-deny-and-park *on the merge path*, never default-approve.**
*Statement:* continuous-claude's commit-on-merge-path memory choice (T) could enhance gate backlog visibility (C) of U by parking expired-gate work as durable, countable state on main rather than in unmerged branches.
*Mechanism:* ruvnet's deepest failure wasn't the 5% rate — it was that the other 95% was *invisible* and the loop's memory stalled behind it (7 of 9 nights traceless on main). A parked queue that is itself a first-class, measured object converts silent decay into a visible number the fleet can react to.
*Falsifier:* ask the owner today: how many undecided gates exist across the garage right now? If the answer requires an audit rather than a lookup, the queue is already invisible at n=1 and the hypothesis's premise stands.
*Class:* adjacent · *level-up:* step-function on the ruvnet failure mode specifically · *Clusters:* G, F.

**H12 — A gate may delegate to a deterministic check only after the check demonstrates a refusal.**
*Statement:* OpenShell's runnable refusal demo (T — one command, published transcript) could enhance safe gate-shedding (C) of U by making a *recorded refusal of a seeded violation* the admission criterion for any check that replaces an owner gate.
*Mechanism:* `zeroMergeStreak` is the proof-by-counterexample: the detector built for exactly this class of problem was permanently miscalibrated and never fired, unnoticed. A control's existence and its effectiveness are independent facts; only a witnessed "no" ties them. This is the negative-control discipline from lab science applied to gate delegation.
*Falsifier:* seed a violation against one believed garage control (a non-curator agent attempting a graph write) and check whether a refusal event is produced *and recorded*. If refusal artifacts appear for free, the ceremony is redundant.
*Class:* non-obvious as a *precondition for delegation* (obvious as a test) · *level-up:* step-function — it is the only mechanism in this set that makes gate-shedding safe rather than hopeful · *Clusters:* H, G.

**H13 — Refusal demos on cron: controls rot, so re-demonstrate on schedule.**
*Statement:* Claude Code cloud routines (T, already in the surface) could enhance inert-control detection (C) of U by re-running each control's seeded-violation demo nightly and filing the transcript — turning Cluster H's six instances from a lesson into a standing instrument.
*Mechanism:* every Cluster H instance rotted *silently over time* (branch protection off while advertised; #172 open 5½ months; a permission engine unreachable; ApiScopes deleted under latency pressure). Point-in-time verification cannot catch decay; only recurrence can. Cost: one cron routine, the surface the garage already runs.
*Falsifier:* run the demo suite twice, two weeks apart, over the garage's believed controls (curator single-writer, firewall, sandbox, settings precedence, SDK subagent restrictions). Prediction from #172: at least one believed control fails its demo on day one.
*Class:* adjacent (OpenShell ships the demo; scheduling it is the addition) · *level-up:* linear · *Clusters:* H.

**H14 — Gate dispositions are macaroon-shaped: caveated, expiring, non-accreting.**
*Statement:* macaroon-style attenuation (T, Cluster C — verified at 0.049 ms) could enhance the semantics of an owner approval (C) of U by making each disposition a time-limited, use-limited capability, so batch approvals (H10) cannot accrete into standing authority.
*Mechanism:* Cluster C's named unsolved problem — aggregation, forty years old — appears at the gate layer as "twenty individually-approved actions become a de facto policy nobody activated," which is §5.7's twenty-runs-confer-nothing rule violated by accretion rather than by decision. Expiry caveats are the cheap, shipped countermeasure.
*Falsifier:* find one current garage approval that is de facto standing (approved once, exercised repeatedly across sessions). Prediction: "commit to main" already is.
*Class:* non-obvious · *level-up:* linear, but closes a hole H10 opens · *Clusters:* C, G.

**H15 — The honest ceiling is a measurement, not an estimate: instrument owner disposition latency.**
*Statement:* GitHub Issue timestamps (T, already the gate surface) could enhance ceiling knowledge (C) of U by measuring presented→disposed latency per gate class for two weeks, yielding the owner's sustainable dispositions/day empirically — with ruvnet's ~20:1 overrun and HA's seven-year linear ceiling as outside anchors.
*Mechanism:* both sides of every gate already leave timestamps on the Issue surface; the number exists, unread.
*Falsifier:* if measured latency fails to predict backlog growth over the same period, attention is not the binding term at this scale (see closing section — this falsifier is live, not rhetorical).
*Class:* obvious · *level-up:* linear · *Clusters:* G.

**H16 — Absence-of-gate as the exception: allowlist-by-graduation couples the two problems into one mechanism.**
*Statement:* an owner-signed allowlist consulted by the policy engine (T = deterministic policy + §5.7 graduation) could enhance both gate load and trust progression (C) of U simultaneously: every effectful action gates by default; graduation's only effect is moving a (class, context) pair onto the allowlist; gate load therefore falls *exactly* as earned trust grows.
*Mechanism:* the direction matters and the evidence picks it. ruvnet started autonomous and tried to retrofit review — 5%. Every failed personal-OS case shows third-party authorship never starting. The ramp must start supervised and shed gates, not start free and add them; this makes trust graduation and attention relief the *same event*, so neither can silently outrun the other.
*Falsifier:* replay the garage's last month under this policy; count gates that an honest graduation query (H7) could already have shed. If near zero, the coupling produces no relief at current scale and is premature machinery.
*Class:* adjacent · *level-up:* step-function — it is the architecture-shaped answer to "the system stalls at ruvnet's 5%" · *Clusters:* G, C, B.

---

## D. Escalation as a first-class behaviour (§5.6)

**H17 — The three buckets are policy-verdict outputs, not agent judgments.**
*Statement:* a deterministic policy decision point (T, Cluster A's reference-monitor lineage) could enhance §5.6's tripartition (C) of U by making the bucket mechanical: PERMIT → autonomous work; DENY-with-escalate → owner decision; event-source matching a standing policy → event-triggered execution. The verdict record doubles as H2's denial stream — one mechanism, two §5 obligations.
*Mechanism:* if the acting model chooses its own bucket, §5.1 is violated at the routing layer even while honored at the action layer; routing *is* an authority decision.
*Falsifier:* express one real garage decision ("may this agent set `grade:proven`") as a deterministic verdict. If evaluation requires LLM judgment, that action class is owner-bucket *by construction* — which is itself a useful, mechanical classification rule, so the test is informative either way.
*Class:* adjacent · *level-up:* linear · *Clusters:* A, C, H.

**H18 — Escalation calibration is the fleet's real report card.**
*Statement:* two counters — escalations-the-owner-rubber-stamped (over-escalation, wasted attention) and autonomous-actions-the-owner-reversed (under-escalation, spent trust) — (T = calibration-curve discipline over H1/H5 records) could enhance graduation recommendations (C) of U by charting the fleet's escalation calibration per class over time.
*Mechanism:* the ratio is exactly what an owner reviewing a trust recommendation needs and exactly what no current record captures; a fleet that always escalates is safe and useless, one that never does is ruvnet. The curve *is* progressive autonomy, made visible.
*Falsifier:* attempt to compute both counters for current garage agents from Issue history. Prediction: rubber-stamps are partially recoverable, reversals are not — re-proving H1's write-time claim from a second direction.
*Class:* non-obvious · *level-up:* linear · *Clusters:* G.

---

## E. The first slice's real success metric (§7, developing and attacking the leader's proposal)

**H19 — Touch-count instrumentation over the five named acts, baselined on the one artifact that exists.**
*Statement:* owner-authored Issue messages (T — timestamped, attributable artifacts) could enhance the first-slice success metric (C) of U by coding each against §8's five manual acts (transfer context, translate vocabulary, authorize disclosure, decide satisfaction, route the next step), with the single existing cross-team GitHub-Issue exchange as the baseline; the slice succeeds iff the coded count drops while the round trip still completes.
*Mechanism:* the five acts each leave a distinguishable artifact type: a pasted context blob, a rephrasing message, an approval, an acceptance verdict, a routing instruction.
*Falsifier:* have two coders (owner, agent) independently code the existing exchange transcript. If the five acts can't be reliably distinguished in it, the metric needs explicit event capture in the work contract instead of transcript coding — a cheap discovery either way.
*Class:* obvious (developing the leader's proposal) · *level-up:* linear · *Clusters:* G.

**H20 — The "moved not removed" detector: three signatures of burden-shifting, and touch count alone catches none of them.**
*Statement:* instrumenting owner *minutes* and *words-presented-per-gate* alongside touch count (T = the SDV cost-accounting lesson, Cluster D: ~370 data points verified per error found — effort and outcome can diverge enormously) could enhance the honesty of the §7 metric (C) of U by detecting the three ways a falling touch count lies: (a) fewer, heavier touches — count drops, latency per touch rises; (b) off-channel migration — the owner starts editing files or briefing agents outside the instrumented surface; (c) pre-gate comprehension load — each disposition demands more reading.
*Mechanism:* from the inside, "moved the burden" looks exactly like success on the naive metric; only a second, orthogonal instrument exposes it. This is the attack the leader asked for: the round-trip-completes demo and even the touch-count demo are both gameable by consolidation.
*Falsifier:* run one slice; if touch count falls but total owner minutes (message-timestamp deltas) hold flat or rise, the burden moved. If both fall together, the naive metric was sufficient and (a)–(c) are paranoia at this scale.
*Class:* non-obvious · *level-up:* linear, but it protects the metric everything else reports against · *Clusters:* G, D.

**H21 — "Decide satisfaction" is the one act deterministically eliminable — iff acceptance criteria ride in the contract, with a ranked evidence floor for free.**
*Statement:* the PCAOB/ISA evidence ranking with its insufficiency floor (T, Cluster D's best free hit — the only *ordered* evidence vocabulary in the scan) could enhance acceptance (C) of U by letting the §8 contract's evidence-and-acceptance field specify machine-checkable criteria plus a minimum evidence kind, so a validator disposes returned work without the owner reading it — deleting one of the five touches outright rather than compressing it.
*Mechanism:* Cluster D's cost signal points exactly here — the declaration half is cheap and survives across six regimes; the human-verification half costs everything and finds little. A deterministic checker over a typed record is the shape #263 already has.
*Falsifier:* write acceptance criteria for one real garage spike; have a validator dispose it; count owner overrides of the validator's verdict. High override rate kills it for that class.
*Class:* adjacent · *level-up:* step-function on that single touch · *Clusters:* D, G.

---

## F. The garage's own telemetry (non-obvious partition)

**H22 — What the garage already has vs. what it conspicuously lacks: four absences, one of them philosophical.**
*Statement:* an audit of one closed run's records (T = the garage's own telemetry: cycle phase-boundary outcomes, `wf:` stamps, funnel counts, Issue-timestamped gates) could enhance the §5.7 build plan (C) of U by confirming four predicted absences: (a) denial events, (b) owner-time-per-gate, (c) consequence-class tags on actions, and (d) any record distinguishing *owner approved* from *owner did not object* — silence and consent are currently the same record, and a track record that cannot tell them apart will overcount successes systematically, in the agent's favor, forever.
*Mechanism:* (d) is the sharp one: every "success" row in a naive backfill includes every action the owner never saw. That bias is unfixable retrospectively and directly corrupts the twenty-run counter.
*Falsifier:* the audit itself, one closed run, an afternoon. Any of the four present → strike it from the backlog.
*Class:* obvious-once-said; (d) non-obvious · *level-up:* linear · *Clusters:* G, D.

**H23 — An n=1 supervisory-throughput A/B is a within-subject crossover, and the garage has already committed to the posture.**
*Statement:* single-subject experimental design (T — ABAB crossover, standard where n=1 is structural, not a defect) could enhance gate-policy evaluation (C) of U by alternating matched run-classes between two gate policies, with owner-minutes-per-accepted-deliverable and backlog growth as outcomes — the same measured-not-asserted posture as the garage's model-pinned prompt A/Bs (reflexive loop #66).
*Mechanism:* one operator over time is a within-subject design with the owner as their own control; it needs class-matching (H3/H8) to work, which is another reason the vocabulary bootstrap pays before the architecture scope lands.
*Falsifier:* measure between-run variance first. If task variance swamps any plausible policy effect, the honest finding is "unmeasurable at n=1 — instrument anyway and wait for volume," which is itself a result the criticality report should carry.
*Class:* non-obvious/whitespace · *level-up:* linear · *Clusters:* G.

**H24 — Settings precedence is an enforcement plane already above the agents' write reach — the garage owns a small reference monitor and doesn't use it as one.**
*Statement:* Claude Code's user/managed-over-project settings precedence (T, in the verified surface) could enhance deterministic policy (C) of U at zero build cost: deny-rules placed at user level are structurally beyond any agent's edit reach, unlike project `.claude/` files, which agents can modify — with SDK issue #172 as the standing caveat that *declared subagent restrictions* are specifically **not** this plane.
*Mechanism:* §5.2 ("agents cannot change active policy") is currently honored by convention in this repo; precedence honors it by construction, for the subset of policy expressible as settings. Small, real, present.
*Falsifier:* in sandbox, have an agent edit project settings attempting to lift a user-level deny; the deny should hold. Then run the same test through the SDK subagent path — #172 predicts that leg fails, which bounds the plane's coverage honestly.
*Class:* adjacent · *level-up:* linear, but it is the only enforcement plane in this list that exists today with zero assembly · *Clusters:* A, H.

---

## Closing brief — the strongest case that attention throughput is NOT the binding constraint

Cluster G emerged at the merge, was challenged by no scout, and now anchors half this run's framing. Per instruction, here is the full-strength attack. These are threads for the goal-owner to pull, not a verdict.

**1. The 5% may measure demand, not capacity.** ruvnet's 75 untouched proposals were *unsolicited output*. Nobody asked for them; nobody reviewing them was blocked on them. A human who needed those results would have found the time — the measured quantity may be *relevance*, with review capacity as the innocent bystander. The ledger's own v2 fix is evidence for this reading: "propose fewer things and evaluate them harder" is as much a relevance correction as a throughput correction. And the garage's own funnel design *depends* on over-production at the mouth with cheap kills at the neck — by Cluster G's accounting, the hypothesizer you are reading is itself a 20:1 overrun. The framing conflates "produced more than was reviewed" with "produced more than could be reviewed."

**2. The Home Assistant anchor disanalogizes at the trust boundary.** HA's review ceiling governs *third-party code entering a shared trust domain* — 1,220 strangers pushing, maintainers defending, incentives structurally adversarial. Its autonomous-contribution ban protects maintainers from *other people's* fleets. The owner's system is single-principal: reviewer and beneficiary are the same person, the fleet works only on what the owner commissioned, and the adversarial queue dynamics that make HA's gate the ceiling do not exist. Extrapolating an ecosystem-scale, multi-principal ceiling to an n=1, single-principal system imports the number while discarding the mechanism that produced it.

**3. Constraints should be ranked by cost of violation, not by measurability — and Cluster G is the best-measured partly because throughput is the easiest thing to measure.** Every §6 failure priority — deletion, corruption, exposure, misleading advice, authority expansion — is a consequence/authority failure; none is a throughput failure. A fleet stalled at 5% adoption is embarrassing and fully recoverable; one irreversible authority failure (health data exposed, money moved, the second brain corrupted) can end the project. Throughput failures are continuous and self-announcing; authority failures are rare-event and silent — exactly the class a 200/200-capped scan under-samples. The run may have found the streetlight, not the keys.

**4. The ruvnet datum contains an unremoved confound.** The loop's cross-night memory rode in unmerged draft PRs, so STEP 1 read a ledger up to four nights stale — each night proposed with degraded knowledge of what had already been proposed and ignored. Some unknown fraction of the 5% is therefore a *memory-staleness and compounding* failure wearing a review-failure costume. continuous-claude commits memory on the merge path and doesn't exhibit the stall. Until someone fixes the memory path and re-measures adoption, "the human was the bottleneck" and "the loop starved its own memory" are observationally equivalent on this data.

**5. At the owner's actual scale, the constraint is prospective while the trust constraints bind now.** "Hundreds of gate-events a day" is a projection; the garage's present gate rate is plausibly single digits per day (H15 measures it — cheaply, and this argument loses if the measurement says otherwise). Building throughput-matching machinery ahead of the fleet that would saturate it is premature scaling; §5's seven constraints, by contrast, are load-bearing on day one of the first slice.

**What survives the attack, honestly:** the write-time instrumentation hypotheses (H1–H5, H8, H22) survive *all five arguments*, because their cost is near zero now and infinite later regardless of which constraint binds — denials, consequence tags, and approved-vs-unobjected are unbackfillable whether attention turns out to be the ceiling or merely a wall. The hypotheses that lean hardest on Cluster G holding are H10, H11, and H16; the goal-owner should price them accordingly.

---

**Flags for the leader:** (1) H-E performed no fresh Unimatrix dedup searches; graph anchors cited (#190, #195, #196, #200, #254, #263) are taken from scout-merged/scout-active-dev as handed to it. (2) H24 depends on the settings-precedence behavior described in the verified surface plus #172's independently corroborated status; its falsifier tests both legs before anything is built on it. (3) Nothing here is graded; the twenty-four falsifiers are seeds for proof-goals, not commitments.
