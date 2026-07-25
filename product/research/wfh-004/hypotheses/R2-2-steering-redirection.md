# R2-2 — Human steering: the expressiveness of mid-run intent

**Run:** `wfh-004` · Issue #48 · phase `hypothesize` round 2, targeted · `agent_id: wfh-004-r2-2` · read-only, zero graph writes.

**Evidence posture, stated once and repeated per row:** this cell has almost no field evidence *and cannot have any* — the demand signal for redirection cannot exist because no redirection channel exists to fail (W0-d §2, W0-a, L3/L4/L5 concurring). Every `Evidence: none` below means exactly that, not weakness. The exceptions (P-01, P-03, P-27, P-28) are used only where they genuinely bear. Per the charter, every candidate is precedent-free by construction where it touches redirection; each pays in mechanism (Rule 2).

---

## 1. The taxonomy of mid-run intent (headline artifact)

The field — and round 1 — models human input to a running agent as **a binary on an action the agent already chose** (W0-a: *"approve-or-deny, per tool call or per PR"*). Enumerating what a human actually needs to say mid-run shows how small a fraction of the intent space that is.

### Axis 1 — the operation (what the intent does to the run)

| # | Intent shape | Expressible today? | Would be observable as | Coverage |
|---|---|---|---|---|
| 1 | **Approve/deny** an agent-chosen action | **Yes** — the only shipped shape | tool call proceeds/refuses | shipped everywhere; integrity covered L3-36/37 |
| 2 | **Halt** everything | Yes (interrupt/kill) | run stops | shipped; andon generalization L1-48 |
| 3 | **Interrupt-and-restate** (restart with new brief) | Yes, at the cost of all in-flight work | new run | shipped; handover form L1-07 |
| 4 | **Append guidance** (say more, hope it lands) | Yes, unreliably — no binding, no acknowledgment | maybe nothing | delivery/ack: L1-47, L2-21, L5-34, L6-39 (A-8/A-15) |
| 5 | **Subtract scope** ("drop X, keep the rest") | **No** — remaining work is not addressable | dropped sub-goal absent; rest undisturbed | **R2-2-01** |
| 6 | **Widen scope** ("also do Y") | No, without restart | new unit admitted to the live plan | R2-2-01 (union is the easy dual) |
| 7 | **Reorder priorities** ("Z first") | **No** — no visible remaining-work order to permute | execution order changes, same run | **R2-2-02** |
| 8 | **Reject a premise** + redo only what depended on it | **No** | named redo-set; disjoint retention | L5-35 (excision) + **R2-2-04** |
| 9 | **Add a forward constraint** | Marginally (appended text; unverifiable) | subsequent actions conform, checkably | policy-entry: L1-12 family |
| 10 | **Add a constraint that binds retroactively** | **No** | completed-work compliance sweep | **R2-2-05** |
| 11 | **Issue a standing rule** ("stop asking me about X; here is the rule") | **No** — P-01's memory file is the failed attempt | rule fires on future instances unseen by the human | **R2-2-03** |
| 12 | **Demonstrate** ("not that, this" — contrast, not specification) | No, as anything binding | subsequent outputs shift on the demonstrated dimension | **R2-2-12** |
| 13 | **Amend what counts as done** | **No** | done-check cites the amended criteria version | **R2-2-11** |
| 14 | **Interrogate** ("what are you doing and why") truthfully, without perturbing | Partially — asking injects into the very context being asked about | record-derived answer; behavior unchanged | **R2-2-06** |
| 15 | **Grant/revoke authority** live | No (unconfigured) | pre/post behavior flip, no restart | **closed** — L1-12 |
| 16 | **Withdraw a previous steer** | **No** — steers have no identity to withdraw | prior course restored without restart | **R2-2-09**, **R2-2-14** |
| 17 | **Correct the record** the run consumes | Partially (`context_correct` for the KB; nothing for the run's working record) | post-correction reads return the corrected value | folded into R2-2-04 |

### Axis 2 — the entry point (what the intent acts on)

Round 1 assumed intent steers **the run**. Five distinct entry points exist, each with a different observable: the **plan** (rows 5–7 — R2-2-01/02), the **context** it sees (R2-2-10), the **policy** bounding it (row 15, closed via L1-12), the **criteria** judging it (R2-2-11), and the **record** it consumes (R2-2-04). **"Steer the run" conflates five different abilities.**

### Axis 3 — extent (how long and how far the intent binds)

This action · this unit · this run · standing; and reach: forward-only vs retroactive. **No shipped or round-1 candidate gives a steer an extent at all** — every steer today is implicitly either eternal (a memory file) or one-shot (a chat message), and *which* it is, is undecidable from the record. **R2-2-14**; retroactive reach is **R2-2-05**.

### Axis 4 — initiation and shape

Human-initiated vs **run-solicited** (R2-2-07), and the interaction shape it arrives in — blocking widget, inline text, deferrable notification, ambient annotation (**R2-2-08**). Round 1 policed *whether* the agent may interrupt (L1-42, L2-22, L5-36, L6-37); nobody worked *which shape the interaction takes when it legitimately happens*.

### The structural claim the taxonomy forces

Every inexpressible row bottoms out in the **same missing substrate**: remaining work, binding intent, acceptance criteria, and derivation provenance do not exist as addressable data — they exist only as the model's private intentions. SCOPE §3.2's edge `Structure → Human steering ("gate at named points")` is real but was read by round 1 as addressing the **past and present**. **Redirection requires addressing the future**: the plan-not-yet-executed as first-class units. That is a dependency statement (per §3.2 discipline, these candidates' cost-to-prove includes that upstream Structure work), not an architecture. It also explains W0-a's cross-concern observation from inside: families C/E get steering *"comparatively cheaply"* precisely because they own a durable work-shape that includes the future; families A/B own no future and can therefore only veto the present.

**The composite case (W0-a's honest note taken literally):** a general redirect — *"stop pursuing A as planned; do B instead, keeping what still serves B"* — is not a new primitive. Its mechanics are exactly R2-2-01's set operation over the plan plus R2-2-04's provenance traversal over completed work, with L1-07's handover as the degenerate fallback when neither substrate exists. Recorded so W6 does not hunt for a missing "redirection primitive": **redirection decomposes**, and the decomposition is this register.

---

## 2. Candidate register

All candidates: **Concern: Human steering** (spans noted). Each carries a differs-from clause naming the nearest round-1 candidate.

**`R2-2-01` — Scope subtraction against a live run**
- **Ability:** A human removes a named sub-goal from a running unit's remaining work, and the unit drops it plus all pending work solely serving it while everything else continues undisturbed — observable as the dropped sub-goal absent from all subsequent activity, the retained work proceeding under the same run id, and the dropped/retained partition recorded.
- **Mechanism:** Remaining work as an addressable set with dependency edges; subtraction is set difference plus reachability pruning — the mechanics of build-target pruning (Make/Bazel) and cancellation scopes in durable orchestrators (Temporal cancellation propagates to child activities). The dual (widening) is set union and mechanically simpler.
- **Inference surface:** Resolving *which* sub-goal the free text names is a leaf; subtraction, pruning, and the partition record are deterministic **given an addressable plan** — which does not exist today, and that absence, not inference, is the whole gap.
- **Incumbent delta:** **C** — remaining work lives in the model's intentions; there is nothing to subtract from.
- **Evidence:** none — no redirection exists to have failed. (P-03's drift is the inverse shape: scope that could not be *held*, let alone edited.)
- **Falsifier:** If real runs' sub-goals are so entangled that pruning reliably drops too much or too little, subtraction degenerates to interrupt-and-restate and L1-07's handover dominates.
- **Differs from:** L2-21/L5-34/L1-47 deliver *an* instruction but leave its content opaque; this names a specific operation the channel must carry and what the plan must be for the operation to exist.

**`R2-2-02` — Priority reorder without restart**
- **Ability:** A human reorders a running unit's remaining work and the unit visits units in the new order — observable as execution order changing mid-run under the same run id, with the reorder event recorded.
- **Mechanism:** Priority as mutable data on declared pending units (a priority queue whose keys an external principal can rewrite — ubiquitous in schedulers; novel only in that the "scheduler" here is an agent's intentions).
- **Inference surface:** Mapping the utterance to a permutation is a leaf; the reorder is deterministic given the plan substrate.
- **Incumbent delta:** **C.**
- **Evidence:** none — no redirection exists to have failed.
- **Falsifier:** If dependency structure determines order so tightly that legal permutations are trivial, reordering has no degrees of freedom worth steering.
- **Differs from:** L4-13 resolves precedence *between two conflicting humans*; this is one human permuting one run's future.

**`R2-2-03` — Standing correction: a steer that generalizes (case → rule)**
- **Ability:** A correction issued once on one instance binds all future similar decisions in the run (optionally across runs), checked at each decision point rather than recalled — observable as the correction firing on later instances the human never saw, with a count of automatic re-applications recorded.
- **Mechanism:** Case-to-rule promotion: the steer is distilled into a predicate over decision features and stored where the decision point *consults* it, not where the model *may remember* it. Precedent: common law (adjudication → binding rule), military standing orders, "mark as spam trains the filter." **The mechanical distinction from the failed memory-file attempt: a rule checked at the decision site vs prose hoped to be recalled** — P-01 recurring *after* the memory file is the field's demonstration that recall-based standing rules do not bind.
- **Inference surface:** Distilling free text into a predicate is a leaf (once, at capture); matching future decisions is deterministic where features are structured, a leaf where prose. The *binding* — that the rule is consulted at all — is fully deterministic.
- **Incumbent delta:** **C** in the binding sense. Memory files exist and demonstrably do not bind (P-01 ×3).
- **Evidence:** **P-01, inverted** — the owner already steers by standing rule; the harness silently downgraded his standing rule to a suggestion. The one expressiveness row with direct field pain.
- **Falsifier:** If generalized corrections over-fire more than they save, humans revert to per-instance steering and the rule store rots. Measurable as override rate on rule firings (L3-38's metric, reused).
- **Differs from:** L6-38 records steers and reconciles disposition at close; it never *generalizes* one — an L6-38 steer binds exactly the instance it targeted.

**`R2-2-04` — Premise retraction with selective downstream invalidation**
- **Ability:** A human marks a premise the run has adopted as wrong; the harness identifies everything derived from it, invalidates exactly that set, and retains everything independent — observable as a named redo-set with its justification chain, the retained set continuing undisturbed, and post-correction reads returning the corrected value.
- **Mechanism:** Justification links from premises to derived work, then retraction as graph traversal — precisely a truth-maintenance system (Doyle's TMS/ATMS) and, in engineering form, build-system dirty-propagation. The record-correction half has an in-house precedent: `context_correct` deprecates-and-relinks in the KB; nothing does this for a run's working record.
- **Inference surface:** With recorded justification links, invalidation is deterministic traversal. *Without* them, deciding whether a work product depends on the premise is a leaf per item — so the deterministic form has a provenance-capture prerequisite, and its cost-to-prove includes it (§3.2 rider).
- **Incumbent delta:** **C**, and sharper than configuration: L5-35 established the working state is an append-only token stream; this adds that even after excision, nothing knows *which completed work* the excised premise contaminated.
- **Evidence:** thin — P-27/P-28 are wrong-premise runs, but both were corrected by full-pass redo, which is exactly the cost this ability exists to avoid.
- **Falsifier:** If provenance capture costs more per run than the occasional full redo it saves, restart dominates — economic, directly measurable once either path exists.
- **Differs from:** L5-35 excises the premise from the unit's *working state*; it is silent on *already-produced artifacts* downstream of the premise. This is the other half: what must be redone, and equally what must not be.

**`R2-2-05` — Retroactive constraint sweep**
- **Ability:** A constraint added mid-run binds backward as well as forward: the harness re-checks completed work against it and reports which completed items now violate — observable as a compliance sweep listing retro-violations, distinct from forward enforcement.
- **Mechanism:** The constraint applied as a filter over the ledger of completed items — the recall-campaign / regulatory-retroactivity pattern. Requires only that completed work is enumerable (the E-1/effect-ledger machinery round 1 already generated) plus the constraint as a checkable predicate.
- **Inference surface:** Deterministic for rule-shaped constraints over enumerable items; an irreducible C-2 leaf per item for prose constraints.
- **Incumbent delta:** **C** — mid-run constraint *addition* has no channel at all, let alone backward reach.
- **Evidence:** none — no channel exists to have failed.
- **Falsifier:** If constraints humans actually add mid-run are overwhelmingly forward-only in intent, the backward sweep is unneeded ceremony.
- **Differs from:** L1-51 binds *the run* to amend-before-deviating; this is the *human's* new rule reaching backward over work that was compliant when performed.

**`R2-2-06` — Interrogation answered from the record, not the agent**
- **Ability:** A human asks a running unit what it is doing and why, and receives an answer derived from the externally-observed record rather than the unit's self-report, without perturbing the run — observable as the answer citing ledger events, and the run's subsequent trajectory unchanged by having been asked.
- **Mechanism:** Read-replica pattern: the query is served from the event stream, never injected into the running context. The "truthful" property is inherited, not asserted: a self-report can be confabulated (FP-3's whole family); a record-derived account is bounded by what the record shows. The no-perturbation property is structural — nothing enters the run's context.
- **Inference surface:** Composing the causal narrative from events is a leaf; the events, the citation discipline, and the no-injection guarantee are deterministic. Honest note: the leaf can still narrate wrongly *about* true events — the citations make that checkable.
- **Incumbent delta:** **C** — today "what are you doing?" is a context injection answered by the same model it interrupts; **observation is intervention**.
- **Evidence:** none directly; FP-4 context — every contained incident began with the owner *noticing*, and noticing today costs either an interruption or a raw-transcript read.
- **Falsifier:** If record-derived answers are systematically less informative than self-reports, the perturbation-free property is not worth the fidelity loss — head-to-head testable.
- **Differs from:** L3-35 is an external watcher reporting *liveness/state*; this is on-demand *intent-level explanation as steering input* — the ability that tells a human whether steering is needed at all.

**`R2-2-07` — Divergence-solicited steering with an intervention window**
- **Ability:** The run detects that its trajectory is diverging from its charter or from prior human intent and surfaces a *non-blocking, deferrable* steer opportunity — announcing its default and proceeding on it after a declared window — observable as flagged divergence points on the human-facing surface, work never stalling, and the human able to intervene inside the window before the divergence hardens.
- **Mechanism:** Two parts. Divergence scoring against declared intent (a leaf). Then the *lazy-consensus / negative-option* discipline — "I will do X in N hours unless objection" (Apache governance, change-control practice): silence is consent, but consent was actually solicited, at the moment it was cheap. **This addresses the L3-32/L1-42 tension directly rather than ignoring it:** zero blocking prompts (sterile-cockpit safe), attention consumed only when the human chooses to spend it, compatible with a decision budget because a deferrable flag is not a decision demand.
- **Inference surface:** Divergence scoring is irreducibly inferential (C-2 territory); the window, the default, the flag, and proceed-on-timeout are deterministic. **Inference proposes, the deterministic shell disposes.**
- **Incumbent delta:** **C** — nothing observes the run as an object (W0-d §4), so nothing can notice it diverging.
- **Evidence:** P-03 (drift surfaced only at close, when correction cost a run), P-27/P-28 (owner steers arrived late because nothing surfaced the divergence early — both caught by the owner noticing, unaided).
- **Falsifier:** If divergence false-positives swamp the surface, this recreates P-01's saturation one level up — measurable as human intervention rate on flagged points.
- **Differs from:** L4-11 queues decisions *the agent chose to ask*; this generates the steer opportunity from observed divergence, unasked, and never blocks. L1-30 is a precommitted binary abort; this is graduated and correctable.

**`R2-2-08` — Interaction shape as policy, not agent choice (the P-01 resolution)**
- **Ability:** The *shape* of every human-facing interaction — blocking modal, inline text, deferrable notification, ambient annotation — is a property of the interaction's declared class and phase, chosen by policy outside the agent, never by the agent — observable as identical intent content arriving through different shapes per class, and no modal prompt ever issuing where policy says inline.
- **Mechanism:** Presentation decoupled from content, with interruption level owned by the platform — the mobile-OS notification model (the OS, not the app, decides what may interrupt); triage levels in clinical alarm design.
- **Inference surface:** Zero at runtime — class membership and phase are lookups. Classifying a novel interaction into a class is a leaf at worst.
- **Incumbent delta:** **C** — the agent picks its own interruption modality every time.
- **Evidence:** **This sharpens the P-01 ambiguity L3-32's falsifier left open.** P-01 confounds three variables: timing (non-gate), volume (saturation), and modality (the blocking widget). The recorded remediation discriminates between them: the owner's standing fix bans the *modality* unconditionally while explicitly permitting the *same decisions* as plain text at gates. Volume is never named in the record. **Reading: the binding variable is modality-first, timing-second — the owner rejects being *modally seized*, not being consulted.** L3-32's volume-bounding remains valid but answers the second-order problem; the first-order fix is shape. Offered as a sharpening, not a resolution — the volume reading stays live until probed.
- **Falsifier:** If, with shapes fixed by policy, the owner still saturates at the same question count, modality was cosmetic and volume (L3-32) was the binding variable — a clean discriminating experiment.
- **Differs from:** L1-42/L2-22/L5-36/L6-37 govern *whether/when* an agent may issue a blocking prompt; none governs *what shape a permitted interaction takes* — and L1-42's own falsifier (refusal converts questions into silent worst-assumption guesses) is exactly the failure this candidate's degrade-to-deferrable-shape prevents.

**`R2-2-09` — Provisional steer with revert**
- **Ability:** A steer can be issued as provisional: applied immediately, with the pre-steer course retained such that withdrawing the steer restores it without restart — observable as a withdrawn steer producing resumption of the prior course under the same run id, both events recorded.
- **Mechanism:** The steer as a stacked overlay on plan-state rather than a destructive edit — savepoint/undo semantics; feature-flag-with-kill-switch is the operational precedent.
- **Inference surface:** Zero for stack, apply, revert, record — given the plan substrate.
- **Incumbent delta:** **C** — a steer today is words in a context window; it cannot be withdrawn, only argued with.
- **Evidence:** none — no redirection exists to have failed. Rationale is economic: humans steer more freely when steering is cheap to undo — reversibility raises the usable bandwidth of the channel (§4).
- **Falsifier:** If real steers are essentially never withdrawn, revert machinery is dead weight.
- **Differs from:** L5-35 excises a *wrong agent premise*; this reverts a *human's own instruction* — the mirror case, and the one that makes tentative steering rational.

**`R2-2-10` — Live context steer (pin / exclude)**
- **Ability:** A human alters what a running unit sees — pinning an artifact into its context or excluding a named source — effective at the unit's next step without restart, observable as the pin/exclusion appearing in the unit's context manifest from that step on.
- **Mechanism:** The context-assembly pipeline already exists and runs (W0-b #7–9: three live injection points); the mechanism is admitting a human-pinned entry/blocklist as an assembly input. The nearest live precedent is in-house: `SubagentStart` injection — the same splice with a human, not a retrieval server, as source.
- **Inference surface:** Zero for pin, exclude, manifest.
- **Incumbent delta:** **B-leaning** — the seam exists and runs; the human-sourced live path does not. Turns partly on A-8/A-15.
- **Evidence:** **P-27 and P-28 directly** — both were context-composition defects that the owner could only fix by re-running the whole pass. A live context pin was the precise correction both needed; **the expressiveness row with the strongest field pain.**
- **Falsifier:** If mid-unit context changes degrade coherence more than a respawn-with-corrected-surface costs, restart-with-amended-surface dominates for our unit sizes.
- **Differs from:** L5-34/L6-39 deliver an *instruction*; this delivers *material* — steering what the unit knows rather than what it is told to do. Round 1's context candidates decide injection *by policy*; this is injection *by live human act*.

**`R2-2-11` — Criteria amendment with a versioned done-check**
- **Ability:** A human amends what counts as done for a named unit mid-run, and the unit's completion check evaluates against the amended criteria — observable as the done-check citing the criteria version it evaluated, and the amendment event recorded.
- **Mechanism:** `done_when` as versioned data consulted at completion rather than prose recalled from the charter. Precedent: construction change-order practice — mid-build scope change is routine, priced, and tracked against the contract version, because unversioned targets make "done" unlitigatable.
- **Inference surface:** Version bookkeeping and which-version-applied citation are deterministic; evaluating a prose criterion remains a C-2 leaf — the amendment changes *which* prose the leaf is shown, verifiably.
- **Incumbent delta:** **C** — criteria live in SCOPE prose; nothing consults a versioned target at completion.
- **Evidence:** none directly; P-12 is adjacent (an unversioned target drifting).
- **Falsifier:** If mid-run criteria churn correlates with worse outcomes than close-and-recharter, live amendment is an attractive nuisance and criteria should be immutable per run.
- **Differs from:** L1-51 requires amendment-before-deviation; this is the human *changing the declaration* with version discipline, so E-1's machinery has a moving target it can still reconcile against.

**`R2-2-12` — Contrast steering ("not that, this")**
- **Ability:** A human steers by supplying a contrast pair — a rejected output plus a preferred exemplar or direction — and the run applies the differential to remaining similar work, observable as subsequent outputs shifting on the demonstrated dimension without per-item instruction.
- **Mechanism:** Contrastive exemplars routed to matching decision sites. The argument is cognitive-economic and is the strongest bandwidth mechanism in this register: comparative judgment is far cheaper for humans than specification — the insight underlying pairwise preference collection, and the reason design review works by markup, not by restated requirements.
- **Inference surface:** Honest: **mostly inference.** Applying an exemplar's differential is irreducibly a model judgment. The deterministic part is real but thin: capturing the pair, routing it to matching sites, recording where it applied. Declared per A-3 without apology; screen 9 will price it.
- **Incumbent delta:** **C** as a *binding* channel — you can paste an example into chat today; nothing routes it, scopes it, or records where it applied.
- **Evidence:** none as steering-failure; note the owner's actual recorded steers have exactly this shape (P-27's "level up" was a contrast, not a specification).
- **Falsifier:** If exemplar steers over-fit — the run generalizes the wrong feature of the contrast — articulated rules (R2-2-03) dominate and demonstration is a trap. Discriminable head-to-head.
- **Differs from:** L1-45 verifies comprehension of an *articulated instruction* by readback; this replaces articulation with demonstration for the class of intent the human cannot cheaply articulate. R2-2-03 distills a rule; this deliberately does not.

**`R2-2-13` — Attention-anchored delta digest (trust calibration)**
- **Ability:** A human can see, at any moment, what has changed since *they last looked* — a per-principal delta over the run's record, ranked by divergence-relevance — observable as a steer-or-not decision being makeable in bounded time without reading the transcript, and the record tracking each principal's last-reviewed mark.
- **Mechanism:** A high-water mark per human principal over the event record, plus render-what-changed-since — mechanically the code-review pattern (diff against last-reviewed commit) — and, for the "is action needed" framing, the nursing shift-change/SBAR discipline, which exists precisely to make "do I need to act" decidable in minutes at handoff. **The ability is the decision being makeable in bounded time; a dashboard is one mechanism and not the claim.**
- **Inference surface:** The mark, the diff, and the event set are deterministic; ranking by divergence-relevance and any summarization are leaves. FP-3 tension addressed, not ignored: a *summary* can be a confident wrong number — the digest must be derived from the same record R2-2-06 cites, with citations, or it becomes the next P-05.
- **Incumbent delta:** **C** — "what changed since I last looked" is answerable today only by re-reading (the human mirror of P-20's 12 re-reads).
- **Evidence:** FP-4 (the owner's attention is the compensating control in every contained incident — and it currently spends itself on reconstruction, not judgment); P-20's re-read pattern applies to the human as much as the agent.
- **Falsifier:** If the digest is not trusted (one FP-3-style wrong digest) the owner reads transcripts anyway and the digest is pure overhead — trust, once lost, is the falsifier firing.
- **Differs from:** L3-35 reports the run's *state* without cooperation; L4-15 captures decisions for a *different person's* cold handoff; this is bookkeeping over the *same* person's intermittent attention — when the scarce channel should be spent, not what it should know.

**`R2-2-14` — Steer extent: every steer carries a declared scope-in-time**
- **Ability:** Every steer carries an explicit extent — this action, this unit, this run, standing — chosen or defaulted at capture, and ceases to bind outside it — observable as the record answering, at any moment, exactly which past steers currently bind, and expired steers demonstrably not firing.
- **Mechanism:** TTL/scope on instruction records. Precedent: military orders practice, which invented precisely this distinction under bandwidth pressure — a FRAGO (binds this operation) vs an SOP (binds until superseded), two extents, first-class, never confused. Without extent the harness must treat every steer as either eternal (accumulating contradictory intent — L4-13's conflict problem arising at n=1 across time) or one-shot (P-01's re-asking).
- **Inference surface:** Zero for extent bookkeeping, expiry, and which-binds-now. Inferring the *intended* extent of a free-text steer is a leaf — with a declared default so the leaf is never load-bearing.
- **Incumbent delta:** **C** — a steer's extent today is undecidable from the record; the memory file is the ambiguous artifact (meant as standing, stored out-of-repo, silently non-binding).
- **Evidence:** none beyond that reasoned reading of the P-01 remediation; marked honestly as reasoned.
- **Falsifier:** If real steers cluster entirely at two extents (one-shot, permanent), a binary flag suffices and a graduated taxonomy is ceremony.
- **Differs from:** L6-38 captures a steer's target and disposition and reconciles at close; it gives a steer no temporal extent. R2-2-03 generalizes over *cases*; this scopes over *time*. The three compose.

---

## 3. Sub-areas closed (covering IDs — no round-2 candidates emitted)

| Sub-area | Covered by | Note |
|---|---|---|
| Gate integrity: spoofing, TOCTOU, appeal of refusals | L3-36, L3-37, L3-38 | complete as a set |
| Blocking-prompt suppression outside gates | L1-42, L2-22, L5-36, L6-37 | four independent arrivals; R2-2-08 adds only the *shape* dimension they all omit |
| Delivery plumbing for mid-run intent (channel, receipt, ack) | L1-47, L2-21, L5-34, L6-39 (+ probes A-8, A-15) | genuinely covered; every R2-2 candidate *presupposes* one of these channels and adds the payload semantics |
| Decision queues, latency budgets, default-on-timeout, escalation to roles, multi-owner precedence, principal identity | L4-11 … L4-14 | closed |
| Steer capture + close-time reconciliation | L6-38 | closed; R2-2-03/-14 extend, not replace |
| Working-state excision of a wrong premise | L5-35 | closed for the state half; R2-2-04 is the artifact half |
| Readback / comprehension verification | L1-45 | closed |
| **Policy entry point** (grant/revoke authority live) | **L1-12** | declared closed — human-initiated live narrowing/widening is L1-12's mechanism with the sign flipped; a separate candidate would be padding |
| Handoff between humans; the conn; go/no-go polls; andon; precommitted aborts | L4-15, L1-44, L1-46, L1-48, L1-30 | closed |
| Record correction in the KB plane | `context_correct` (shipped, in-house) | the run-plane half folded into R2-2-04 |

---

## 4. The bandwidth argument

**The problem at its worst:** the human channel is a few sentences per hour against thousands of decisions; FP-4 shows the owner's attention is the compensating control in every contained incident, and it does not scale. If steering stays per-decision, human attention is simply the binding constraint and no channel design fixes it — L4-11's queue only rations the shortage.

**The argument that high-leverage steering is achievable:** the problem is not novel — it is the defining condition of every command structure ever run at human bandwidth over superhuman decision volume. Organizations solved it, and their solution decomposes into exactly four multipliers, each present in this register:

1. **Generalization** — one utterance binds a class, not an instance (R2-2-03). **The largest multiplier:** it converts channel capacity from decisions/hour to *rules/tenure*.
2. **Cheap encoding** — contrast instead of specification (R2-2-12). Lowers cost per utterance for the intent classes humans articulate worst.
3. **Timed spending** — attention lands where divergence is, while it is still cheap (R2-2-07, R2-2-13; management-by-exception is the discipline's actual name). Doesn't increase capacity; stops wasting it on reconstruction and on-track work.
4. **Reversibility** — steering that can be withdrawn is issued more freely (R2-2-09, R2-2-14). Raises usable bandwidth by lowering the stakes per utterance.

**The honest counterweight:** leverage amplifies error identically. A wrong per-instance steer costs one instance; a wrong standing rule misfires across its whole extent, silently. High-leverage steering therefore *requires* the extent and revert machinery as a package, not as options — **leverage without reversibility is how organizations get destroyed by their own SOPs.**

**Verdict offered to triage:** human attention is the binding constraint **only under the per-decision steering model the field shipped** — and this register is the escape from that model. The floor that remains is irreducible: novel situations demand per-instance judgment, and P-01's evidence is that even that floor is only acceptable to the human in the right interaction shape (R2-2-08). **FP-4 is not refuted; it is re-priced.**

---

## 5. Emergent concerns (§3.3, engaged honestly)

**No new concern proposed.** The tempting candidate — "intent management": the set of instructions currently binding on a run as an object with lifecycle (capture → extent → generalization → expiry → reconciliation) — fails test 2: it is Human steering's own machinery plus E-1's ledger discipline plus the Structure substrate. A *cluster*, and clusters file as capabilities. Recorded so W6 does not re-derive it.

**E-1, engaged rather than re-derived:** endorsed, consistent with all six round-1 lenses. This register's contribution is one observation, not a new population: **steers are the human-issued half of the obligation space.** L6-38 already files "was the steer honored" there; R2-2-14 adds that an obligation without a declared *extent* cannot be reconciled even in principle (you cannot ask "does this still bind?" of a record that never said until-when), and R2-2-11 adds that E-1's reconciliation needs versioned targets to survive legitimate mid-run amendment — otherwise every human criteria-change reads as a run breaking its declaration.

**Flags for the leader / W6:**
- **The structural finding (§1):** every expressiveness candidate bottoms out in the same upstream absence — **the future is not addressable data.** Per §3.2's cost-to-prove rider, nearly every candidate here inherits that Structure prerequisite; W6 should cluster them with it rather than counting them as independent arrivals.
- **L3-31 applies doubly:** this agent was handed round 1's registers *as well as* the shared W0 surface. Any convergence between R2-2 rows and round-1 rows is maximally non-independent and must be discounted accordingly.
- **P-01 sharpening (R2-2-08):** the modality-vs-volume discrimination is this register's one contribution of new *evidence reading*, not just new candidates; it bears directly on L3-32's declared falsifier and should reach triage even if the candidate is cut.
- **Evidence honesty:** of 14 candidates, 3 carry real field pain (R2-2-03 via P-01 inverted, R2-2-10 via P-27/P-28, R2-2-13 via FP-4/P-20), 4 carry adjacent-shape evidence, and 7 are marked `none — no redirection exists to have failed`. **That distribution is the hole made legible, and it is the expected result, not a defect of the cell.**
