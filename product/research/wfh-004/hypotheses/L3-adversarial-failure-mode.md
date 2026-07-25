# L3 — Adversarial / failure-mode

**Run:** `wfh-004` · Issue #48 · phase `hypothesize` · lens L3 · read-only, zero graph writes.

**Honesty statement, up front and load-bearing.** W0-d §2 concern 3 is correct: the garage's pain record contains **zero** adversarial, malicious, or compromised-agent incidents. Every candidate below is tagged in its Evidence field as one of:

- **`field`** — grounded in a recorded P-nn (usually the *accidental* form of an attack: FP-3's confident wrong number is record-poisoning by accident; P-12's 3× gate overrun is approval-TOCTOU by accident; P-03's scope crossing is self-authorization by accident).
- **`reasoned`** — no field support at all. Derived from a named mechanism in W0-b/W0-c plus a standard attack pattern. **18 of 38 candidates are `reasoned`.** They are not weaker in mechanism; they are weaker in demand evidence, and triage should treat them as such — but *not* as absences of exposure. The garage has run 8 research runs in 5 weeks in a devcontainer that mounts the host SSH agent, provisions a permissions-bypass alias, runs zero permission rules, and auto-injects retrieved graph content into every specialist. Zero incidents recorded in that configuration is a statement about **detection capability**, not about **exposure**. Per W0-b §0-iii the baseline is *"configured toward maximum authority"* — and per P-04 *"violations are undetectable as violations."* An environment with no detector reports no incidents by construction.

**The single sharpest structural observation this lens produces**, which shapes everything below: W0-d §4's finding that the alarm surface is the individual tool call is not merely a gap — it is *the attacker's operating envelope*. **Any adversary who does not cause a tool call to return an error is invisible.** Every failure in the register that stayed silent (19 of 30) did so because it succeeded. A competent adversary's actions all succeed. So the garage's demonstrated detection rate against *successful* actions is, from the record, indistinguishable from zero.

---

## 1. The candidate register (38 candidates)

### Group A — Origin and authority of content (instructions arriving through data)

**`L3-01`**
- **Ability:** An instruction that arrives inside retrieved, fetched, or tool-returned content cannot cause a tool call the current step was not already authorized to make, observable as the call being refused and the refusal naming the originating content span.
- **Concern:** Security (spans Context provisioning)
- **Mechanism:** Authority is resolved from the step's declared grant *before* content is read, and the tool-dispatch check consults only that grant — content is an input to *what* is done, never to *what may be* done. Precedent: the dual-LLM / CaMeL pattern (a privileged planner emits the control flow; untrusted content is bound to opaque variables the planner never interprets as instructions), and object-capability security generally, where reading a message cannot grant a capability. The property does not require detecting the injection; it requires the authority set to be closed under ingestion.
- **Inference surface:** Fully deterministic at the enforcement point — "is tool T in step S's grant" is a set membership test. Inference is irreducible only in *authoring* the grant and in any optional adjunct that tries to *classify* content as adversarial. The classifier is the part that must not be load-bearing.
- **Incumbent delta:** **C** per W0-b #21/C-1 (no privilege field in the token stream) for the *detection* framing — but **B** for this framing, because closing the authority set does not require distinguishing data from instruction. Permission deny rules + per-agent `tools:` (#4, #14) are the substrate. Turns on **A-2** and **A-3**.
- **Evidence:** `reasoned`. W0-a Security: *"absent: any shipped defense against instructions arriving through data, in any of the ~30 tools."*
- **Falsifier:** If steps cannot be granted narrowly enough to be useful — every real step needs Bash+Write+Edit+network anyway — the closed authority set is the full set and the ability buys nothing. Test: take 10 recorded factory steps and compute the minimal grant each actually exercised.

**`L3-02`**
- **Ability:** Every span of an agent's context is attributable to a named origin, observable as an origin manifest for any turn that a third party can produce without the agent's cooperation.
- **Concern:** Context provisioning (spans Introspection, Security)
- **Mechanism:** Assembly-side recording: whatever process concatenates the prompt records each contribution's source, byte range, and reason at the moment of assembly. Bookkeeping at a chokepoint, not analysis — the harness already *knows* the origin at splice time and currently discards it. Precedent: Cannoli's `LoggingEdge` (#147); LangSmith captures it retrospectively. The delta is that the manifest is produced by the *assembler*, not reconstructed.
- **Inference surface:** Zero inference. Note what it deliberately does *not* do: judge whether the content was safe. That separation is the point.
- **Incumbent delta:** **B**, partially. `/context` (#13) lists blocks with token counts but **hides verbatim text**, is retrospective and linear. Our own hook emits `additionalContext` with no record of what the server chose or excluded.
- **Evidence:** `field` — P-28, P-27, P-11. Also **A-12** directly.
- **Falsifier:** If, given a manifest, no one can act on it — if origin never changes a downstream decision — it is a log nobody reads. Test: replay 5 past failures with manifests present.

**`L3-03`**
- **Ability:** Content injected into an agent's context by the harness is distinguishable, at the receiving end, from content the human authored, observable as a receiving agent correctly identifying the origin of an injected span deliberately crafted to impersonate a system instruction.
- **Concern:** Security (spans Context provisioning)
- **Mechanism:** Unforgeable framing — the delimiter is drawn from a nonce the content author cannot know, or the channel is structural (a distinct message role/block) rather than lexical. Physical argument: a lexical marker inside a shared token stream is forgeable by anyone who can write into that stream; a per-session nonce is not. Precedent: prepared statements against SQL injection — the fix is not detecting the quote character, it is putting data on a channel where quoting is not the framing.
- **Inference surface:** Deterministic to *emit*. **Irreducible inference at the receiving end** — whether the model honors the framing is model behavior, not enforcement. This is a mitigation, not a boundary. `L3-01` is the boundary; this is defense in depth *behind* it. Candidates that confuse the two are why prompt-injection defenses fail.
- **Incumbent delta:** **ambiguous — turns squarely on A-12.** W0-b: the `--- Unimatrix Context ---` header is *"a convention emitted by our own server, not a harness-level trust marker."*
- **Evidence:** `reasoned`.
- **Falsifier:** If the model's compliance with framing is not measurably better than with a plain prefix, the nonce buys nothing over the header we already emit.

**`L3-04`**
- **Ability:** A tool call names the content span that motivated it, observable as any call in the record being traceable to the input that caused it, and as a call motivated by untrusted content being separable from one motivated by the step's brief.
- **Concern:** Introspection (spans Security)
- **Mechanism:** Dynamic taint / information-flow labelling: spans carry labels at assembly (`L3-02`), the label set of a step's context is joined, and any effect inherits the join. Precedent: DIFC operating systems (Asbestos, HiStar, Flume). Here the computation is a model call, which is opaque, so propagation is coarse (step-granular join) — but coarse labelling still answers "did this step read anything untrusted before it did that?"
- **Inference surface:** The join and effect-labelling are deterministic. **Attributing an effect to a *specific* span within a step is not deterministic** — do not claim per-token causality. (L2 independently flags span-level causality as physics-bounded at the current model interface.)
- **Incumbent delta:** **C.** `PostToolUse` records the call (#22) but carries no context lineage; `SubagentStart` opens a bracket `SubagentStop` never closes.
- **Evidence:** `reasoned` for the adversarial case; `field` for the shape — P-05, P-06, and W0-a's *"nobody ships a causal account."*
- **Falsifier:** If in practice every step reads untrusted content, the join is always "tainted" and carries no information.

**`L3-05`**
- **Ability:** An agent's set of permitted actions is identical before and after it reads any content, observable as a capability-set fingerprint byte-identical at step start and step end regardless of what was read.
- **Concern:** Security
- **Mechanism:** Monotonic-non-increase of authority within a step, enforced by resolving the grant at admission and making it immutable for the step's lifetime. If the grant is an immutable value captured before ingestion, no ingested content can be in its causal history. The ocap "no ambient authority, no amplification" property, and the falsifiable *observable* form of `L3-01`.
- **Inference surface:** Zero. Fingerprint equality is a hash comparison.
- **Incumbent delta:** **B/ambiguous.** Agent frontmatter resolves before launch (#4) — but per **A-3** binding under `Agent`-tool invocation is untested, and per **A-6/C-5** an agent holding Bash can start a process outside the grant entirely (`L3-10`).
- **Evidence:** `reasoned`. Field-adjacent: P-02 and P-09 show the grant is not currently a function of the role at all — it drifts in both directions.
- **Falsifier:** If steps legitimately need to acquire authority mid-step (a scope widening the human approves), an immutable grant forces every widening into a step boundary; if that cost exceeds the benefit, the ability should be "authority changes only through a named, recorded transition."

**`L3-06`**
- **Ability:** Content that has influenced agent behaviour but has never been read by a human is enumerable, observable as a standing list of files, nodes, and injected spans with a "never reviewed" marker and the count of runs each has entered.
- **Concern:** Context provisioning (spans Security, Self-improvement)
- **Mechanism:** Two ledgers intersected — the injection/read ledger from `L3-02`, and a human-review ledger. Set difference, deterministic. Economic argument: the cheapest place to hide a persistent instruction is a file nobody opens, and the garage's own record proves nobody opens them (W0-d §6). An attacker's dwell time is bounded by review coverage, and review coverage is currently unmeasured.
- **Inference surface:** Zero for enumeration. Inference is irreducible only in *triaging* the resulting list — which the enumeration makes possible for the first time.
- **Incumbent delta:** **C.** `settings.local.json` is gitignored so part of the behaviour-governing surface is not reviewable in principle.
- **Evidence:** `reasoned` for the attack; `field` for the substrate — P-11, P-28, the gitignored local settings.
- **Falsifier:** If the unreviewed set is always ~100% of the corpus, the marker has no discriminating power and the real need is a review workflow.

### Group B — The agent that edits its own constraints

**`L3-07`**
- **Ability:** A change to the configuration that governs a run does not take effect within that run, observable as the run completing under the configuration fingerprint it started with and the attempted change appearing as a recorded, un-applied event.
- **Concern:** Security (spans Self-improvement, Structure)
- **Mechanism:** Config resolved once at run admission into an immutable snapshot; the process reads the snapshot, not the files. Precedent: Kubernetes admission-time resolution, immutable infrastructure, Temporal's workflow versioning. The separate and stronger economic argument: **a run that can edit its own rules produces no evidence about the rules**, so every self-improvement measurement (P-18) is void unless config is frozen per run.
- **Inference surface:** Zero.
- **Incumbent delta:** **B**, weakly. `ConfigChange` with `decision:"block"` exists (#20), unconfigured; per **A-9** unknown whether it fires for *agent-file* edits — the tree that actually defines the roles. Bash-write coverage is **A-4**.
- **Evidence:** `field` — P-03 is the accidental form: W6 ran a question §7 declared out of scope without an amendment.
- **Falsifier:** If legitimate mid-run config changes are frequent and necessary (P-24's rate-limit workaround was), freezing costs more than it saves.

**`L3-08`**
- **Ability:** The criteria a run will be judged against are fixed before the run and cannot be altered by it, observable as a close-out verdict computed against a pre-registered criteria document whose hash is recorded at run start.
- **Concern:** Self-improvement (spans Structure, Human steering)
- **Mechanism:** Pre-registration — the mechanism clinical trials adopted for this exact failure (outcome-switching). Purely logical: a criterion editable by the party it judges is not a criterion.
- **Inference surface:** Hash check deterministic; **judging prose criteria against prose output is an irreducible LLM leaf per C-2.** The clean cut: the harness deterministically guarantees *which* criteria were asked, *that* they were all asked, and *that* they were not changed — the verdict is a model call whose inputs are pinned.
- **Incumbent delta:** **C** as an enforced property; **B** for the hash-stamping half (#30).
- **Evidence:** `field` — P-03, P-12, P-13.
- **Falsifier:** If scopes legitimately must amend mid-run (wfh-002's W5 amendment was legitimate and improved the run), rigid pre-registration is harmful; the ability may need to be "amendments are possible but are recorded events that invalidate prior comparisons."

**`L3-09`**
- **Ability:** The harness cannot run with its enforcement disabled without every artifact the run produces carrying that fact, observable as a downstream consumer refusing an artifact stamped "produced with enforcement off."
- **Concern:** Security (spans Introspection, Self-improvement)
- **Mechanism:** The enforcement-mode value is an input to the artifact's identity (part of its hash), not a separate log line. Physical argument: an adversary — or a hurried operator — can always turn enforcement off; what they cannot do is make the *absence* of enforcement produce an indistinguishable artifact, if mode is part of identity. Precedent: SLSA provenance attestations; a kernel's taint flag on loading an unsigned module.
- **Inference surface:** Zero.
- **Incumbent delta:** **C.** Not only unstamped — the environment *provisions* the bypass (W0-b §0-iii).
- **Evidence:** `reasoned` for the adversarial case; `field` for the condition (verified by inspection). This is the answer to "an agent that behaves correctly when observed": if observed and unobserved modes produce distinguishable artifacts, probe-vs-production divergence is detectable after the fact.
- **Falsifier:** If enforcement is off for 100% of runs (currently true), the stamp is a constant. It becomes an ability only when enforcement is sometimes on — downstream of enforcement existing at all.

### Group C — Escape by re-invocation, credentials, and executed code

**`L3-10`**
- **Ability:** Authority denied to a step is not obtainable by any process that step starts, observable as a child process attempting the denied action and failing identically to the parent, including when it supplies its own policy on the command line.
- **Concern:** Security
- **Mechanism:** The boundary is enforced by a principal the run cannot write as — OS-level confinement plus a root-owned managed-settings tier, so policy is a property of the *process tree's environment* rather than of its arguments. W0-b §4 states the sharpened form: *"the agent cannot bind itself — the binding authority must be a principal the agent cannot write as."* That is a statement about file ownership, and file ownership is a mechanism.
- **Inference surface:** Zero at the boundary — precisely the class where the deterministic path exists and simply was not built.
- **Incumbent delta:** **ambiguous, and this is C-5 — the run's sharpest untested question.** Turns on **A-6** and **A-11**. `--bare`'s documented behaviour (*"skips hooks… MCP… CLAUDE.md"*) is the named sharp threat. Per §11 must route `needs-a-probe`, never `out`.
- **Evidence:** `reasoned`. Enabling conditions all verified present: Bash held by every agent, credential file readable same-uid (#18), Tailscale + DinD + host `~/.ssh` bind-mounted (§0-iii).
- **Falsifier:** If A-6 shows the managed tier does not survive re-invocation and A-11 shows the sandbox cannot run here, the ability is not achievable in this environment and confinement must move to a different substrate — an architecture answer out of this run's scope, but the ability as stated would be falsified.

**`L3-11`**
- **Ability:** A credential is usable only by the unit it was issued to and only for the duration of that unit, observable as the same credential failing when presented by a different unit or after the unit closes.
- **Concern:** Security
- **Mechanism:** Short-lived, audience-scoped tokens rather than a long-lived file — the standard workload-identity pattern (SPIFFE/SVID, OIDC workload federation, dynamic secrets). A credential's blast radius is the product of its scope and its lifetime; both are currently unbounded. This is the only item in Group C that survives even if `L3-10` fails, because it degrades the value of a successful escape rather than preventing it.
- **Inference surface:** Zero.
- **Incumbent delta:** **B/C.** Credential-file denial and subprocess env scrubbing exist and are unset (#18); the *scoping to a unit* half has no incumbent expression because units have no identity (D6) — downstream of Structure per §3.2, and that cost must be stated.
- **Evidence:** `reasoned`. Field-adjacent: P-06 means a stolen credential's use would be indistinguishable from legitimate use, forever.
- **Falsifier:** If the MCP/API surfaces cannot issue per-unit credentials (provider-side, the P-15 shape), this is blocked upstream and routes `needs-a-probe` on a provider question, not a build.

**`L3-12`**
- **Ability:** The code the harness executes on its own control events is pinned and verified before it runs, observable as a session refusing to start when a hook binary, skill, or MCP server differs from its recorded fingerprint.
- **Concern:** Security (spans Self-improvement)
- **Mechanism:** Content-addressed pinning with verification at load — Nix/lockfile semantics, Sigstore/TUF for supply chain, secure boot for the general shape. Deterministic hash comparison.
- **Inference surface:** Zero.
- **Incumbent delta:** **C.** The exposure is concrete and verified: W0-b inspected the live hook binary in an **npx cache** path — user-writable, executing on **eight hook events** including every `PreToolUse`/`PostToolUse`, with full user privilege, outside the model's context entirely. Nothing pins it.
- **Evidence:** `reasoned` for compromise; `field` for the ambient risk — same class as P-09 and P-30: the gap between what the config *says* runs and what *runs* is unmeasured.
- **Falsifier:** If the executed set changes on a normal cadence (npx re-resolves, plugins auto-update), pinning generates constant false alarms and the ability becomes "changes are surfaced," not "refused."

### Group D — Confused deputy, role identity, and the insider

**`L3-13`**
- **Ability:** A write performed by one role on behalf of another carries the originating role's identity, observable as the record naming both the actor that wrote and the role whose content it is, and as the two being independently queryable.
- **Concern:** Introspection (spans Security, Structure)
- **Mechanism:** Two-field attribution (`written_by` / `on_behalf_of`) — the standard delegation record: `sudo` logging real and effective uid; OAuth token exchange's actor/subject distinction (RFC 8693). Deterministic; the information exists at the call site and is discarded.
- **Inference surface:** Zero.
- **Incumbent delta:** **C in practice.** D6: `agent_id` accepted and discarded; every write records `created_by: anonymous`. W0-b #23 says OTel spans are one `env` key away — but per **A-10**, if all file-defined agents report `agent.name: custom`, per-role attribution collapses anyway.
- **Evidence:** `field` — P-06 (standing, >1 month). The single-writer curator is the garage's largest concentration of authority, and there is currently **no record capable of distinguishing a curator write from a curator write** — insider-shaped failure at the curator is undetectable in principle, not just in practice.
- **Falsifier:** If nobody ever queries by role, the second field is dead weight. Test: try to answer "which role produced the 33 nodes filed in wfh-001" from the graph today.

**`L3-14`**
- **Ability:** A specialist can verify its brief against the run's declared charter without trusting the actor that spawned it, observable as a specialist declining a task outside a charter it read independently, and naming the divergence.
- **Concern:** Structure (spans Security, Human steering)
- **Mechanism:** The charter is a signed/pinned artifact addressable by the specialist directly (a run-id-keyed record); the brief carries a reference, not a restatement. Argument from segregation of duties: a subordinate who can only see what the superior tells them cannot detect a compromised superior — why aviation CRM makes the first officer's authority to challenge structural, and why four-eyes controls require independent access to the source document.
- **Inference surface:** Fetching and hash-verifying is deterministic. **Deciding whether a brief lies outside a prose charter is an irreducible LLM leaf (C-2).** Clean cut: deterministic that the charter was fetched unmodified and that the question was asked with a forced binary that is recorded; inferential only in the answer.
- **Incumbent delta:** **C.** Every specialist receives its entire world from the leader's prompt plus hook-injected retrieval. No independent channel. P-09 shows the leader's own instantiation is not reliable either.
- **Evidence:** `field` (accidental form) — P-02: a planning session executed a full theme-scan, opened an Issue, stamped a cycle, spawned two scouts. **Neither spawned scout could have checked.**
- **Falsifier:** If specialists decline correct briefs at any appreciable rate, the challenge authority costs more than the compromise it guards against.

**`L3-15`**
- **Ability:** An action whose effects cannot be undone requires two distinct principals, observable as a single principal being unable to complete it however many times it retries.
- **Concern:** Security (spans Human steering)
- **Mechanism:** Two-man rule — nuclear surety, dual-control wire release, and the shipped software instance W0-a names: **Copilot's coding agent structurally cannot approve or merge its own PR** (#143), enforced in GitHub's permission system, *a plane the agent holds no credentials for*. That last clause is the whole mechanism; C-4's shape, which W0-c flags as *"the highest-value class this run can find."*
- **Inference surface:** Zero at enforcement (two identities, one action). **Irreducible inference in classifying an action as irreversible** — unless the classification is authored, not inferred (`L3-20`).
- **Incumbent delta:** **B**, and cheaply: the second principal can be a platform (branch protection, required review) rather than a second agent. Absent here: no factory action is classified as requiring dual control, including `grade:proven` writes and every git push.
- **Evidence:** `reasoned` for the adversarial case; `field` for the shape — P-12, P-13.
- **Falsifier:** If the second principal is always the same overloaded human, dual control degrades to rubber-stamping and adds latency without independence (see `L3-32`). Falsified if the second principal's rejection rate is ~0 over a meaningful sample.

### Group E — Defeating the firewall / poisoning the record

**`L3-16`**
- **Ability:** An artifact cited as proof is verified to exist, to have been produced within the run that cites it, and to be unmodified since citation, observable as a `proven` claim reverting when the artifact is absent, later edited, or authored outside the run.
- **Concern:** Structure / evidence discipline (spans Security)
- **Mechanism:** Content-addressed proof references (hash, not path) plus a provenance check against the run's own effect record. Deterministic. The attack this closes is not exotic: `proven_by` currently holds a *path string*, and an agent that can write a file can write a file at that path containing "PASS."
- **Inference surface:** Existence, hash-match and authorship fully deterministic. **Whether the artifact demonstrates the claim at the claim's altitude is an irreducible LLM leaf** — W0-b C-4 makes exactly this cut. The deterministic half is currently unbuilt, which means today *neither* half runs.
- **Incumbent delta:** **B (syntactic) / C (semantic)** per W0-b #40 — *"syntactic, deterministic, cheap, and currently unbuilt."*
- **Evidence:** `field`, indirectly and damningly — the garage has exactly one `grade:proven` node in 8 runs (P-26) and it is a pre-existing platform, not a garage proof. The firewall has never been *load-tested*.
- **Falsifier:** If proofs are legitimately artifacts outside the run (a third-party benchmark), the provenance clause over-constrains; the ability may need to be "the artifact's origin class is declared and recorded."

**`L3-17`**
- **Ability:** A claim whose text changes after proof was attached loses its proven grade, observable as the grade reverting automatically and the diff between pre- and post-proof claim being named.
- **Concern:** Structure / evidence discipline
- **Mechanism:** The grade is bound to the (claim-text, artifact) pair, not to node identity. Any correction changing claim text invalidates the binding by construction. Precedent: signature verification — a signature covers a message; change the message and it fails, with no policy decision required.
- **Inference surface:** Zero.
- **Incumbent delta:** **C**, with a specific mechanical hazard: `context_correct` reissues the id and re-links edges, and P-25 records that it *"silently skipped some incoming edges… count never stated."* A mechanism that already loses edges silently can lose the proof binding silently. The `grade:` tag is separately mutable in place with **no id reissue**, so grade and content can drift apart by design.
- **Evidence:** `field` for the mechanism's unreliability — P-25. `reasoned` for deliberate use.
- **Falsifier:** If claim text is routinely edited for wording without semantic change, auto-reversion creates churn people route around; then the ability is "a post-proof edit is surfaced for re-affirmation."

**`L3-18`**
- **Ability:** A number the harness reports about itself is reproducible by an instrument the reported-on unit did not produce, observable as a divergence between the two being raised during the run rather than discovered later.
- **Concern:** Introspection (spans Self-improvement, Cost)
- **Mechanism:** Independent recomputation from a primary record the measured party cannot write — the auditing principle that a control is only as good as the independence of its evidence. The *adversarial* framing matters because a self-improvement loop whose metric is produced by the thing being improved has no fixed point: any measure under optimization pressure that is causally downstream of the optimizer's own outputs will be optimized directly (Goodhart as mechanism, not proverb).
- **Inference surface:** Zero for numeric reconciliation. Honest limit: catches *divergence*, not *both-wrong*. P-16 would have been caught (the POC was the second instrument); P-05 would have been caught (38 vs 0).
- **Incumbent delta:** **C** as a running property; **B** for ingredients (`opcost` #26 proves extractability; OTel gives a second source, #27).
- **Evidence:** `field`, the strongest in this register — P-16 (**61×**), P-05 (**0 vs 38**), P-25, P-14, P-12. W0-d: *"the traces we have have lied."*
- **Falsifier:** If both instruments derive from the same primary source they agree while both being wrong. Falsified if no genuinely disjoint second source exists — which for subscription quota is *already true* (P-15).

**`L3-19`**
- **Ability:** Every reference in a persisted output resolves, observable as a report failing to persist when a cited path, node id, issue number, or artifact does not exist.
- **Concern:** Introspection / evidence discipline
- **Mechanism:** Link-checking at write time — deterministic resolution of each reference against the store it names. Closes the accidental-fabrication channel (a hallucinated node id) and the deliberate one with the same check.
- **Inference surface:** Zero. It does *not* check that the target *supports* the claim (C-2 leaf).
- **Incumbent delta:** **C.** No write-time validation of any reference in any factory artifact.
- **Evidence:** `field` — P-14 (duplicated §6, two different recommendation lists, three inconsistent counts, undetected 3 days), P-08.
- **Falsifier:** If most references are prose gestures rather than resolvable identifiers, the check rejects almost everything and forces citation formalism nobody sustains.

### Group F — Blast radius, irreversibility, containment

**`L3-20`**
- **Ability:** An action that cannot be undone is distinguished from one that can *before* it runs, observable as the two classes taking visibly different paths and as an unclassified action being treated as irreversible.
- **Concern:** Security (spans Structure, Recovery)
- **Mechanism:** An authored reversibility class per action type, fail-closed by default. Precedent: BPMN compensation and sagas — a step either declares its compensating action or is a point of no return, and the engine knows which. Fail-closed argument: the cost asymmetry is total, and unclassified-as-safe is how every default-allow system fails.
- **Inference surface:** Fully deterministic **if the classification is authored** (a table of tool→class). Inference is needed only to classify *novel* actions — the exact case where inference is used because nobody built the deterministic path. Honest note: Bash is one tool name covering both classes, so tool-name granularity is insufficient and classification must reach argument granularity, which is where it gets hard.
- **Incumbent delta:** **C.** No reversibility concept. `/rewind` (#34) **explicitly excludes Bash-written and subagent-written files** — *"the two ways this repo actually writes."* The incumbent's one reversibility feature is blind to 100% of this repo's writes.
- **Evidence:** `reasoned` for the framing; `field` for the exposure: every graph write, `gh issue` call, and git push in the garage's history has been irreversible and unclassified.
- **Falsifier:** If nearly all actions classify as irreversible, the distinction stops discriminating and collapses into "everything needs approval" — `L3-32`'s failure mode.

**`L3-21`**
- **Ability:** Content leaving the run is checked against the run's own secret material before it leaves, observable as a post, commit, or request containing a credential being refused with the matched span named.
- **Concern:** Security
- **Mechanism:** Egress content inspection at the boundary — shipped and mature (push protection, gitleaks, DLP). Pattern-matching plus known-secret-value matching against credentials actually present, which is strictly stronger than generic pattern matching because the values are known.
- **Inference surface:** Zero for known-value matching. Pattern-based detection of unknown-shape secrets is heuristic; **semantic exfiltration (describing rather than quoting) is not detectable by either** and is named as out of reach.
- **Incumbent delta:** **B** (sandbox egress proxy with domain allowlists, #17 — unset), but the delta matters: domain allowlisting controls *destination*, not *content*, and this environment has Tailscale, DinD, `--device=/dev/net/tun`, and the host SSH agent — the destination surface is effectively unbounded. **A-11** applies.
- **Evidence:** `reasoned`. Credential file readable by every agent; SSH agent socket mounted; agents routinely post to Issues and push commits.
- **Falsifier:** If no secret material is reachable from the run's context (achieved by `L3-11`), content inspection is redundant. Also falsified if false-positive rate on legitimate factory content (which discusses credentials and tokens constantly) makes it unusable.

**`L3-22`**
- **Ability:** A knowledge write is not returned by retrieval until it has been observed by a party other than its author, observable as a newly written node being absent from another agent's injected context until that condition is met.
- **Concern:** Context provisioning (spans Security, Structure)
- **Mechanism:** A quarantine queue on the retrieval path — Wikipedia pending-changes, moderation queues, staged rollout. Why this chokepoint matters more than it looks: W0-b #7 records that the garage **automatically injects retrieved graph content into every new specialist**. That makes the knowledge graph a *broadcast channel to all future agents*, writable by anyone who can write a node. No other component has that reach. A single poisoned node addresses every specialist in every future run, indefinitely, arriving pre-authenticated as "knowledge."
- **Inference surface:** Gating is deterministic (a flag on the retrieval query). **Whether the observer's review was adequate is not checkable at all** — this converts an unbounded broadcast into a reviewed one; review quality is a separate question.
- **Incumbent delta:** **C.** The injection is live, automatic, and unfiltered today.
- **Evidence:** `reasoned` for poisoning; `field` for the amplification path (W0-b #7, byte-pinned) and for propagation of unreviewed content (P-16).
- **Falsifier:** If quarantine latency starves runs of the knowledge they need (the garage's whole thesis is that the KB compounds), cost exceeds benefit. Test: how often is a node written in run *n* retrieved in run *n* or *n+1*?

**`L3-23`**
- **Ability:** The complete set of effects attributable to one unit is enumerable and retractable, observable as one operation listing and reversing every file, node, comment, and commit a named agent produced.
- **Concern:** Recovery (spans Security, Introspection) — **the core of proposed emergent concern E-4**
- **Mechanism:** An effect ledger keyed by unit id plus a compensating action per effect class (`L3-20` is the prerequisite). Precedent: saga compensation; `git revert` for the VCS subset; revocable forwarders in ocap systems. Economic argument: incident cost = detection time × blast rate × **remediation cost**, and the third term is currently *unbounded and unknown* — nobody can say what any past agent touched.
- **Inference surface:** Enumeration deterministic **given attribution** (downstream of `L3-13` and of D6 being fixed — §3.2 cost stated). Compensation deterministic per authored class. No model call.
- **Incumbent delta:** **C**, hard. `created_by: anonymous` means effect enumeration by unit is **not computable from the data that exists**. Replit checkpoints (#142) and Factory's per-run worktree (#145) are the nearest shipped shapes, both file-scoped only.
- **Evidence:** `reasoned` for compromise-response; `field` for the ambient need — P-12, P-25.
- **Falsifier:** If effects are overwhelmingly in systems with no compensating action (a posted comment, a sent email), enumeration without retraction is the real ceiling and the ability should be split.

**`L3-24`**
- **Ability:** A retraction reaches every run that consumed the retracted content, observable as a downstream artifact that cited it being marked, and as the consuming runs being enumerable.
- **Concern:** Introspection (spans Recovery, E-4)
- **Mechanism:** A consumption ledger (who retrieved what, when) inverted on retraction — the index that makes `L3-02`'s manifest possible, queried the other way. Precedent: certificate revocation distribution; the recall notice — recalls work because of a distribution record, not better inspection.
- **Inference surface:** Zero for propagation. **Whether a downstream conclusion actually depended on the retracted input is an irreducible judgement** — the honest engineering answer is to mark conservatively and let a human or leaf narrow.
- **Incumbent delta:** **C.** Supersession chains record that a node changed; nothing records who *read* the old one.
- **Evidence:** `field` for the propagation shape — P-16's inherited claim entered *"our own findings chain"* and was corrected in one place; nothing checked what else consumed it.
- **Falsifier:** If nothing is ever retracted, the machinery is dead weight. The garage has retracted at least twice (P-16's inherited claim; wfh-002's W6 demoted to non-binding), so this is testable now.

### Group G — Denial, exhaustion, and the adversary who makes work expensive

**`L3-25`**
- **Ability:** A named unit of work halts when its resource consumption crosses a declared ceiling, observable as the unit stopping with the ceiling and the consumed figure both named, without the unit's cooperation.
- **Concern:** Cost (spans Security, Recovery)
- **Mechanism:** External metering against a pre-declared per-unit budget — cgroups/rlimits, Temporal per-workflow limits. "Without the unit's cooperation" is load-bearing: a budget the agent enforces on itself is C-4's shape and is not a guarantee.
- **Inference surface:** Zero.
- **Incumbent delta:** **ambiguous — A-1.** `--max-budget-usd` is print-only; **no hook event carries a spend figure**, so spend is not a matchable predicate.
- **Evidence:** `field` — P-30, P-21, P-17. `reasoned` for the adversarial form: an agent that wants to burn a budget faces no obstacle at all.
- **Falsifier:** If per-unit spend cannot be observed during a run (P-15's wall applies to quota; token counts *are* observable per transcript), enforcement is blocked upstream and routes `needs-a-probe`.

**`L3-26`**
- **Ability:** Work attributable to a unit stops when the unit is declared complete, observable as a post-completion call being refused and recorded rather than executed.
- **Concern:** Structure (spans Cost, Security)
- **Mechanism:** A closed lifecycle state on the unit, checked at dispatch — the property that makes a closed file descriptor an error rather than a no-op.
- **Inference surface:** Zero.
- **Incumbent delta:** **B/C.** `SubagentStop` exists but **is not configured**; per **A-7** unknown whether it fires on abnormal termination. There is no "unit is closed" state anything consults.
- **Evidence:** `field` — P-21 (49/332 calls after completion). The adversarial reading is sharper: **a unit that is complete is a unit nobody is watching**, so post-completion is the ideal window for an action you do not want reviewed. That window exists, is measured at ~15% of call volume, and has no observer.
- **Falsifier:** If completion is genuinely fuzzy (legitimate tidy-up after the summary), hard refusal breaks normal work and the ability should be "post-completion work is separately accounted."

**`L3-27`**
- **Ability:** One run cannot exhaust a shared resource another run depends on, observable as a run hitting its own share and stopping while a concurrent run proceeds unaffected.
- **Concern:** Cost (spans Recovery, Structure)
- **Mechanism:** Per-unit quota partitioning of a shared limit — fair queuing, per-tenant rate limits. A global limit with no partition means any single participant can deny every other, and *that requires no malice* — P-24 is the accidental proof.
- **Inference surface:** Zero.
- **Incumbent delta:** **C.** The tag rate limit is global; the subscription quota pool is **shared with claude.ai and Cowork** (P-15) and observable at no granularity, so partitioning it may be impossible at the provider boundary.
- **Evidence:** `field` — P-24. `reasoned` for weaponisation: an agent that wants the curator unable to file simply consumes the shared limit itself.
- **Falsifier:** If the shared limits sit entirely provider-side and are unpartitionable, this is not a harness ability. Routes `needs-a-probe`, never `out`.

**`L3-28`**
- **Ability:** A unit's resource consumption is compared against its own history during the run, observable as an anomalous unit being named while it is still running rather than in a retrospective.
- **Concern:** Cost (spans Introspection, Self-improvement)
- **Mechanism:** Per-unit-type baselining with online comparison — statistical process control. Requires stable unit identities to baseline against: §3.2's layering claim in its cleanest form.
- **Inference surface:** Zero for the comparison. **Explaining *why* a unit is anomalous is inferential.** The cut worth naming: detection deterministic, diagnosis inferential — the field's mistake is usually to route both through a model.
- **Incumbent delta:** **C.** `opcost` is post-hoc, manual, one machine (P-17). No baselining exists.
- **Evidence:** `field` — P-17, P-30. `reasoned` for the adversary who inflates cost quietly; P-20 shows the *accidental* version already costs real money in 4/4 runs.
- **Falsifier:** If unit-type variance is so high that no baseline discriminates, this yields only false alarms. Testable now against existing transcripts.

**`L3-29`**
- **Ability:** A unit that has produced no output within a declared bound is declared dead, observable as a liveness event carrying the unit's id being emitted with no human present.
- **Concern:** Recovery
- **Mechanism:** Watchdog timer / heartbeat — OTP supervision, systemd watchdogs. W0-d §3 point 4's refinement is honoured: **detecting that a pipe stopped producing bytes needs a liveness signal, not an addressing scheme** — so this is *not* downstream of Structure, unlike resumption. Worth carrying to triage because it makes this one cheap.
- **Inference surface:** Zero.
- **Incumbent delta:** **C** per W0-b C-2 for subagents — **turns on A-7**. **B** at session altitude (`turnTimeout`, `inactivityTimeout`, all unset, #29).
- **Evidence:** `field` — P-10 (died *"at turn end, 0 bytes"*; the single manual nudge is the named reason #174 stays `partial`). Adversarial reading: a subagent that never returns is an unbounded denial with no detector — the cheapest attack in this register.
- **Falsifier:** If long legitimate silences are normal, any bound tight enough to catch a hang will kill live work. Testable against recorded inter-output gaps.

### Group H — Multi-agent emergent failure

**`L3-30`**
- **Ability:** A claim's evidence grade does not increase by being restated, observable as a conclusion derived from a `claimed` input carrying at most `claimed`, and as the weakest link in its provenance chain being nameable.
- **Concern:** Structure / evidence discipline (spans Introspection)
- **Mechanism:** Lattice join over evidence labels along derivation edges — the same monotone-meet structure as a security label lattice, or the weakest-premise rule in any sound proof system. Deterministic given derivation edges. Laundering stated as an invariant: A asserts, B consumes as input, C cites B as established — the defence is not vigilance, it is that the join makes elevation arithmetically impossible.
- **Inference surface:** The join is zero-inference. **Which inputs a conclusion actually derives from is not extractable from a model call** — so the honest cut is conservative: label a derived claim with the join over *everything the step read* (the coarse label from `L3-04`), not over the inputs the agent says it used. Trusting the agent's self-report of its own provenance is precisely the failure mode.
- **Incumbent delta:** **C.** The `grade:` tag is set per node with no relation to source grades; `Motivates`/`Supports` edges carry no grade semantics.
- **Evidence:** `field` — P-16 is textbook laundering by accident. W0-a §5.1 is the standing version: *"Do not launder any cell into fact"* — that this warning must be written in prose in every document is the evidence that no mechanism enforces it.
- **Falsifier:** If the join makes everything `claimed` forever, the lattice needs an explicit promotion path (the firewall's artifact attachment is that path) — falsified if no such path can be defined without reopening the hole.

**`L3-31`**
- **Ability:** Agreement between agents that shared an input is reported as correlated rather than independent, observable as a convergence count accompanied by the shared-context overlap that produced it.
- **Concern:** Self-improvement (spans Introspection)
- **Mechanism:** Compute overlap between the contexts of agreeing units (from `L3-02`'s manifests) and report agreement alongside it. Statistical, and not subtle: independent rediscovery is only evidence if the discoverers were independent; effective sample size collapses toward 1 as shared prior mass goes to 1.
- **Inference surface:** Overlap computation deterministic. **The discount function is a judgement call** and should be presented, not applied silently.
- **Incumbent delta:** **C.**
- **Evidence:** `field`, and it applies to **this run**: SCOPE §6 W6 makes convergence an explicit input to triage (screen 8) — but all six lenses of wfh-004 were handed **the same four W0 documents**. They are not blind to each other; they are blind to each other's *output* while sharing their *input*. Convergence here is substantially a measure of what W0 emphasised. SCOPE §7 screen 8 already hedges; this candidate says the hedge should be a computed number. Adversarially: whoever controls the shared surface controls the convergence signal, and therefore controls triage.
- **Falsifier:** If lens outputs turn out near-disjoint despite the shared surface, the correction is negligible. Measurable directly from this run's six registers.

**`L3-32`**
- **Ability:** The rate and volume of decisions asked of a human is bounded and its trend visible, observable as a run that would exceed the bound batching, deferring, or halting instead of asking.
- **Concern:** Human steering (spans Cost)
- **Mechanism:** A decision budget per run with a queueing discipline. Alarm fatigue in clinical monitoring is a measured, documented failure mode in which *adding* alarms reduces response rate — the operator is a finite-throughput channel, and saturating it is a denial-of-service against the control, not a strengthening of it. Aviation's sterile-cockpit rule is the same finding applied as policy.
- **Inference surface:** Zero for counting and bounding. **Deciding which pending decisions are the important ones is inferential** — a legitimate LLM leaf.
- **Incumbent delta:** **C.** No concept of a decision budget.
- **Evidence:** `field` — P-01: blocking prompts at non-gate points, three times, including a recurrence *after* a memory file was written to prevent it, with the owner's response recorded verbatim. That is measured operator saturation. `reasoned` for the deliberate form: an adversary wanting a malicious approval floods the channel first — and P-01 shows the channel floods without anyone trying.
- **Falsifier:** If the binding constraint is decision *quality* rather than volume, bounding rate is the wrong lever. P-01's evidence is ambiguous between the two readings and should be probed.

### Group I — The run as an object: alarm above the tool call

**`L3-33`**
- **Ability:** A run's declared shape is compared against what actually happened, continuously and at close, observable as a run that skipped a declared role or exceeded a gate's authorization failing to close and naming the divergence.
- **Concern:** Structure (spans Introspection; **primary population for emergent E-1**)
- **Mechanism:** A declaration-vs-actual reconciler reading two records — the declared plan and the effect ledger — and computing the difference. Deterministic set comparison. Inventory reconciliation: the oldest control in commerce.
- **Inference surface:** **The most consequential deterministic/inferential cut in this register.** Comparing *countable* declarations to actuals — did role R run, were N authorized and M written, did phase P execute — is fully deterministic and currently done by nobody. Comparing *prose* declarations is an irreducible C-2 leaf. Almost all of the garage's field pain is in the **countable** half: P-13, P-12, P-07, P-19. Those four need zero inference and have zero coverage.
- **Incumbent delta:** **C.** W0-d §4's exact diagnosis: *"nothing observes the run as an object"* is *"the honest completion"* of nearly every "nothing detected X."
- **Evidence:** `field`, heaviest in the register — P-03, P-07, P-12, P-13, P-19, P-26, P-08.
- **Falsifier:** If declarations are too vague to reconcile against, the ability requires a declaration-format change first and its cost includes that.

**`L3-34`**
- **Ability:** A boundary crossing produces an event even when the crossing action succeeded, observable as a record of the violation existing independently of whether anything was blocked.
- **Concern:** Introspection (spans Security)
- **Mechanism:** Detection decoupled from prevention — the IDS-vs-firewall distinction. Why the decoupling matters here: prevention requires being right in advance and fails closed on legitimate work, so it will always be configured conservatively; detection can be maximal because it costs only storage. And detection converts an unknown-unknown exposure into a measured one. **The garage's zero recorded adversarial incidents is exactly what a system with prevention-only thinking and no detector reports.**
- **Inference surface:** Deterministic for rule-shaped boundaries. **Irreducible inference for prose boundaries** — same C-2 cut as `L3-33`, and the same observation: the cheap half is unbuilt.
- **Incumbent delta:** **C** in effect. P-04: *"no record of a blocked attempt exists because none can be produced"* — and no record of a *successful* violation exists either.
- **Evidence:** `field` — P-04, P-02, P-03, P-13. Every one was a boundary crossing that succeeded and surfaced days later when a human read an artifact.
- **Falsifier:** If violations detected but not prevented are never acted on, the events are noise. Directly relevant precedent: #179 diagnosed the unenforced-prose failure and *"the diagnosis changed nothing — because a finding in a graph is also just prose."*

**`L3-35`**
- **Ability:** A run's state is reported by a watcher outside it, observable as run-level status being answerable without reading the transcript and without the run's cooperation.
- **Concern:** Introspection (spans Recovery)
- **Mechanism:** External heartbeat with a state machine held outside the run's process — the supervisor pattern. "Without cooperation" does the security work: a run that reports its own health cannot report that it is compromised, hung, or lying.
- **Inference surface:** Zero.
- **Incumbent delta:** **B/C.** `statusLine` and stream output (#25) are unset and still in-band. Background *sessions* are a different addressing scheme, not a fix (C-2).
- **Evidence:** `field` — P-26 (five Issues OPEN, one **32 days**, no signal distinguishing blocked from abandoned), P-10.
- **Falsifier:** If the watcher only knows what the run tells it, it is the run's own reporting with extra steps. Falsified unless a genuinely out-of-band signal exists.

**`L3-36`**
- **Ability:** A gate's satisfaction is recorded by the party that gated, not the party gated, observable as a gate that cannot be marked passed from inside the run.
- **Concern:** Human steering (spans Structure, Security)
- **Mechanism:** The gate record lives in a store the run cannot write — Issue state, a countersigned record, a separate principal. Same mechanism as `L3-15` and Copilot's can't-merge-its-own-PR; listed separately because the *target* differs (the gate record vs. the action).
- **Inference surface:** Zero.
- **Incumbent delta:** **C in practice.** Gates are prose in `.claude/workflow/*.md` (#37, **A(prose)**) and the leader both requests and records them.
- **Evidence:** `field` — P-12, P-13. `reasoned` for spoofing: nothing distinguishes "the owner approved" from an agent writing "the owner approved," and steering is literally the owner typing between turns.
- **Falsifier:** If the human's approval is only ever expressed *through* the run, no out-of-band record exists to write to and the ability requires a new channel whose cost is part of the candidate.

**`L3-37`**
- **Ability:** An action executes against the exact state that was authorized, observable as a state change between authorization and execution aborting the action and naming the diff.
- **Concern:** Human steering (spans Security, Structure)
- **Mechanism:** Bind approval to a content hash of the thing approved — optimistic concurrency / compare-and-swap, the standard TOCTOU fix.
- **Inference surface:** Zero.
- **Incumbent delta:** **C.** Approvals are per-tool-call and per-diff (W0-a: *"a binary on an action the agent already chose"*) with no binding to a plan.
- **Evidence:** `field` — P-12 is TOCTOU by accident at run altitude.
- **Falsifier:** If the authorized object is prose rather than a computable artifact, hashing produces spurious aborts on cosmetic edits.

**`L3-38`**
- **Ability:** An enforcement refusal is appealable to a human without restarting the run, observable as a refused action re-attempted after an out-of-band human decision, with both refusal and override in the record.
- **Concern:** Human steering (spans Recovery, Security)
- **Mechanism:** A blocking wait on an out-of-band decision channel, with the override recorded as a first-class event. **This is the counterweight to the rest of the register:** every ability above adds a way for the harness to be wrong about its own agents. A control with no appeal path gets disabled wholesale the first time it blocks real work — which is exactly how this repo arrived at a permissions-bypass alias in `.bashrc`. An unappealable control has a half-life. The override *record* is also the training signal for `L3-08`-style improvement.
- **Inference surface:** Zero for channel and record. The decision is human.
- **Incumbent delta:** **B/ambiguous.** `Stop`/`SubagentStop` blocking re-enters the loop (#38, configured but non-blocking); `FileChanged` + `watchPaths` is a genuine out-of-band channel (#39, unconfigured) — but **A-8** is exactly whether it can inject anything.
- **Evidence:** `field`, inverted — W0-b §0-iii is the observable end-state of controls with no appeal path. P-22 and P-10 show the garage already runs on out-of-band human unblocking, with no record of it.
- **Falsifier:** If overrides become the normal path (>50% of refusals overridden), the control was mis-specified. Directly measurable once any enforcement exists.

---

## 2. The failure catalogue

**What happens · what currently notices · time to discovery.** Tagged `field-observed` (with P-nn) or `reasoned`.

| # | Scenario | What currently notices | Time to discovery | Class |
|---|---|---|---|---|
| F-01 | An instruction embedded in a repo file, web page, issue comment, or MCP tool result causes an agent to act outside its brief. | Nothing. No privilege field (C-1); no origin manifest; no boundary event on success. | Never, unless the action itself errors. | `reasoned` |
| F-02 | A node containing instruction-shaped text is auto-injected into **every** new specialist. One write addresses every future agent in every future run. | Nothing. Injection is one-way; no record of what was injected or excluded. | Indefinite. | `reasoned` (amplification path verified) |
| F-03 | An agent edits settings or an agent frontmatter file (or gitignored local settings) to widen its authority. | Nothing. `ConfigChange` unconfigured; A-9 says agent-file edits may not be in its matcher. | Never, for local settings — by construction. | `reasoned`; accidental analogue `field` (P-03) |
| F-04 | A run amends or ignores its own scope to authorize what it is already doing. | Nothing at the crossing. A human reading later. | wfh-002: days, only because the owner read it. | **`field` — P-03** |
| F-05 | An agent holding Bash execs a fresh CLI process with the bypass alias, or `--bare`, or calls the API directly with the readable credential file. | Nothing. `PostToolUse` records a Bash call; nothing correlates a child inference process to the run. | Never. | `reasoned` (C-5; conditions verified) |
| F-06 | The npx-cached hook binary — executing on eight hook events, full user privilege — is modified. | Nothing. Unpinned, unverified, user-writable. | Never. | `reasoned` |
| F-07 | A specialist returns content that induces the leader to spawn an agent, open a surface, or write to the graph. | Nothing. No distinction between specialist output and instruction. | Never, unless the effect is visibly odd. | `reasoned` |
| F-08 | The curator files nodes it never independently observed. The write records `created_by: anonymous`. | Nothing. Attribution discarded at the platform (D6). | Never — **not computable from stored data**. | **`field` — P-06** (the auditability hole) |
| F-09 | A `grade:proven` is set with a fabricated `proven_by` path, or a real artifact for a different claim. | Nothing. The syntactic check is unbuilt; the semantic check is a C-2 leaf nothing invokes. | Never. The control has never been exercised — 1 proven node in 8 runs, a pre-existing platform. | `reasoned`; standing condition `field` (P-26) |
| F-10 | A claim is edited after proof was attached; grade and claim drift apart. | Nothing. And `context_correct` is already known to **silently drop edges** and report success. | Unknown — the edge-loss count was *"never stated"* even for the accidental case. | **`field` — P-25** |
| F-11 | A report is emitted, internally consistent, and wrong. Downstream roles act on it. | Nothing reads it back. | 3 days, by hand-diffing. | **`field` — P-14 → P-12** |
| F-12 | The harness's measurement of itself is wrong by 61×. | Nothing. Caught only because a POC was built on suspicion. | Unknown; a wrong inherited claim had already propagated. | **`field` — P-16** |
| F-13 | A cycle review reports "0 stored" against 38 writes. | Nothing. The telemetry worked; the addressing didn't. | Only when a human compared. The org adapted to the broken instrument rather than fixing it. | **`field` — P-05** |
| F-14 | An unverified claim is restated by a second agent and consumed by a third as established. | Nothing. Grades are per-node with no join over provenance. | Until a POC refuted it. | **`field` — P-16** |
| F-15 | A gate authorizes N and M≫N is done. | Nothing compares authorization to effect. | Never (surfaced only in W0-d's sweep, weeks later). | **`field` — P-12** |
| F-16 | A declared role never runs; the run reports its funnel anyway. | Nothing at close. | Immediate to a reader, never to the system. | **`field` — P-13** |
| F-17 | A run's obligation (a retro) is declared deferred and evaporates. | Nothing carries the obligation. | wfh-002's retro: still not performed; wfh-004's SCOPE contains no retro workstream. | **`field` — P-19** |
| F-18 | Five runs sit OPEN for a month with no state distinguishing blocked from abandoned. | Nothing. | 32 days and counting, surfaced by a manual sweep. | **`field` — P-26** |
| F-19 | A subagent hangs or dies producing zero bytes. | Nothing. No subagent liveness event (C-2); A-7 says even `SubagentStop`-on-crash is undocumented. | Until a human notices the stall. | **`field` — P-10** |
| F-20 | ~15% of a run's tool calls execute after the run signalled completion. | Nothing. No closed state. | Post-hoc retro, one run. | **`field` — P-21** |
| F-21 | A batch stops partway at a shared rate limit; the remainder is never completed. Weaponised: one agent consumes the shared limit so the curator cannot file. | The rate-limit error — but only for the *interrupted* actor, not the starved one. | Immediate for the batch; never for the denial. | **`field` — P-24** (accidental) |
| F-22 | A run burns budget doing nothing. | Nothing. `budget_control` has **no implementing mechanism anywhere**; no run has ever carried a cost figure. | Never during the run. | **`field` — P-30, P-17** |
| F-23 | Retrieval manipulated by volume — plausible near-duplicates crowd out the right node; a node asserting "already scanned" suppresses a future scan. | Nothing. No retrieval reproducibility, no record of what retrieval excluded. | Never. The failure looks like a scan finding nothing. | `reasoned`; adjacent `field` — P-11, P-28 |
| F-24 | An agent's context omits the thing that would change its answer. | Nothing — **W0-d: "Every context pain was caught by the owner, never by the system."** | P-28: a full generation pass at half yield. | **`field` — P-27, P-28** |
| F-25 | A blocking question at a non-gate point; the operator is saturated; the next approval is reflexive. | The human (loudly). Nothing in the system. | Immediate to the human, three times, including **after** a remediation memory file. | **`field` — P-01** |
| F-26 | "The owner approved X" is asserted by an agent. | Nothing distinguishes it from the owner approving X. | Never. | `reasoned`; adjacent `field` — P-12, P-13 |
| F-27 | Two surfaces claim one run-id; state is misrepresented on the human-facing surface. | Nothing checked whether a surface already existed. | Found in W0-d's sweep, days later. | **`field` — P-08** |
| F-28 | A role is instantiated without (or with more than) its contract's tools. | Loud when under-privileged; silent when over-privileged. **All six agent files carry zero recognized restriction fields**, so every specialist runs over-privileged today. | Immediate / never. | **`field` — P-09**; over-privileged is `reasoned` |
| F-29 | Enforcement is disabled for convenience; artifacts are indistinguishable from enforced ones. | Nothing. The environment ships the bypass. | N/A — currently 100% of runs. | **`field` (condition verified)** — W0-b §0-iii |
| F-30 | Convergence between lenses counted as independent corroboration when the lenses shared a surface. | Nothing computes overlap. SCOPE §7 screen 8 hedges in prose. | **Live in this run.** | `reasoned` (structural, verifiable now) |
| F-31 | Compromise discovered; nobody can enumerate what the agent touched, unwind its graph writes, or notify consumers. | Nothing. Effect enumeration by unit is **not computable** from stored data. | Remediation cost unbounded and unknown. | `reasoned`; enabling gap `field` — P-06, P-12 |

---

## 3. The silent-failure inventory

W0-d's claim that this is the largest class is correct and, if anything, understated: **19 of 30 recorded pains were silent, and every one of the 9 loud ones was loud for the same reason — a tool call returned an error.** The adversarial consequence is the single most important sentence in this report: **an adversary whose actions succeed is, on the present evidence, undetectable.**

| Silent failure | Produces no error because | What would make it loud |
|---|---|---|
| An instruction in data causes an authorized-looking call | The call *is* authorized at tool-name granularity; success is indistinguishable from intent | A refusal keyed to the step's grant (`L3-01`) — or a boundary event on success (`L3-34`) plus origin attribution (`L3-04`) |
| A poisoned node injected into every specialist | Injection is the normal path; there is no abnormal path to contrast with | Quarantine before retrieval (`L3-22`) + an unreviewed-influence register (`L3-06`) |
| Self-widened config | Editing a file is a normal successful action | Config frozen per run with an un-applied change event (`L3-07`) + fingerprint on every artifact (`L3-09`) |
| Escape via a fresh process | `bash` returns 0 | Authority enforced by a principal the run cannot write as (`L3-10`) |
| Modified hook binary | It runs perfectly | Pinned, verified executables (`L3-12`) |
| Over-privileged specialist | Nothing is refused, so nothing is logged | Per-step capability fingerprint vs. the role's declaration (`L3-05`) |
| Fabricated or mismatched proof artifact | The write succeeds | Deterministic artifact existence/provenance/hash check at write (`L3-16`) |
| Claim edited after proof | The correction returns success | Grade bound to (claim, artifact) pair (`L3-17`) |
| Silently dropped edges on correct | The tool **reports success**; the loss is in engine logs no agent reads | Write-result reconciliation — claimed effect vs. store state (`L3-18` applied to writes) |
| Confident wrong number (61×, 0-vs-38) | Arithmetic succeeds | An independent second instrument compared during the run (`L3-18`) |
| Self-contradictory handoff document | Nothing reads it back before the next role acts | Reference/consistency validation at persist time (`L3-19`) |
| Laundered claim rising in grade by restatement | Each individual write is well-formed | Grade join over provenance (`L3-30`) |
| Gate authorization exceeded 3× | Every individual write is permitted | Declared-vs-actual reconciliation (`L3-33`) + approval bound to a hash (`L3-37`) |
| A declared role never ran | Absence produces no event | Declared-vs-actual reconciliation at close (`L3-33`) |
| A dropped obligation (the retro) | Deferral is a legitimate action; nothing carries it forward | Commitment tracking with an owner and deadline (**E-1**) |
| Five runs open for a month | Nothing is happening — and nothing is what nothing looks like | External watcher with a state machine and staleness bound (`L3-35`) |
| Post-completion tool calls | The unit has no closed state | Lifecycle state checked at dispatch (`L3-26`) |
| Duplicate run surfaces | Creating an Issue succeeds twice | Pre-creation existence check; declared-vs-actual on surfaces (`L3-33`) |
| Context omission | Absence is invisible to the party who would notice it | An exclusion record in the manifest (`L3-02`) |
| Cost burn with no output | No cost figure exists during any run | External per-unit metering with a ceiling (`L3-25`) + anomaly baselining (`L3-28`) |
| Correlated convergence read as independent | Agreement looks the same either way | Overlap computed and reported with the count (`L3-31`) |
| Enforcement silently off | The artifacts look identical | Mode stamped into artifact identity (`L3-09`) |
| Effects of a compromised unit | Attribution was discarded at write time | Two-field attribution (`L3-13`) + effect ledger (`L3-23`) + consumption ledger (`L3-24`) |

**The pattern, stated once:** every entry is silent because the harness's observation unit is the *tool call*, and every one of these failures is a property of a *relation* — between an authorization and an effect, a declaration and an outcome, two numbers, a claim and its provenance, a run's start and its close. Relations are invisible to a per-call observer no matter how good the per-call observer gets. That is a structural statement, not a tuning statement, and it is why `L3-33`/`L3-34`/`L3-35` matter more than any individual control in Group A.

---

## 4. Coverage statement

| Concern | Populated? | Note |
|---|---|---|
| **Structure** | Yes — `L3-14, 16, 17, 19, 26, 30, 33, 36, 37` | Reached almost entirely *through* evidence discipline and declared-vs-actual reconciliation. **Partial hole:** nothing on sequence, dependency, or composition — an adversarial lens can only ask what an attacker exploits about units that don't exist. L1/L5 own that. |
| **Context provisioning** | Yes — `L3-01, 02, 03, 06, 22, 24` | Strongest non-obvious contribution is `L3-22`: automatic graph→specialist injection makes the KB a **broadcast channel to all future agents** — the highest-leverage single target in the garage, invisible from any non-adversarial lens. |
| **Security** | Yes — `L3-01, 03, 05, 07, 09, 10, 11, 12, 15, 20, 21` | Heaviest. **9 of 11 are `reasoned` with zero field support.** `L3-10`/`L3-11` turn on A-6/A-11 and per §11 must route `needs-a-probe`, never `out`. |
| **Introspection** | Yes — `L3-04, 13, 18, 19, 24, 28, 34, 35` | Second-strongest cell and the one with the *best* field evidence. The reframe a non-adversarial lens misses: **introspection must be correct when the reported-on party wants it wrong.** Self-reported introspection is not introspection under an adversary; it is testimony. |
| **Cost** | Yes — `L3-25, 27, 28` (+ `L3-26, 32` spanning) | Thinner, honestly so: (a) P-15's provider wall is upstream of any harness and no adversarial framing dissolves it; (b) the adversarial cost story is mostly denial, which reduces to ceiling/quota/liveness abilities already listed. **Partial hole: cost prediction** — no adversarial angle; L4's territory. |
| **Self-improvement** | Yes — `L3-08, 09, 18, 31` | Narrow but sharp: **a self-improvement loop whose metric is produced by the thing being improved has no fixed point.** Goodhart as a structural property — meaning #66 would be unsound even if it *did* run, because nothing produces an outcome metric the run cannot influence. **Partial hole:** nothing on the *adoption* half. |
| **Recovery** | Yes — `L3-23, 29, 35, 38` (+ `L3-20` spanning) | Distinctive contribution: **recovery from being wrong** (containment, enumeration, retraction, appeal) as distinct from recovery from *failure*. A third shape neither seeded definition covers. See E-4. |
| **Human steering** | Yes — `L3-15, 32, 36, 37, 38` | Better populated than expected, which partly answers W0-d's flag that the thin steering cell means *no lens can see it*. An adversarial lens sees steering clearly because a gate is an attack surface: floodable (`L3-32`), spoofable (`L3-36`), raceable (`L3-37`), disable-by-attrition (`L3-38`). **Partial hole:** *redirection* — W0-a's named "nobody ships" — this lens reaches the integrity of steering, not its expressiveness. |

**No concern is empty.** Four partial holes named with reasons and the lens that should own each. Per §9 nothing was manufactured to fill a box; the thinnest cell (Cost, 3) is thin because the adversarial angle genuinely collapses into abilities listed elsewhere.

---

## 5. Proposed emergent concerns

**Engaging W0-d's E-1 — commitment / obligation tracking: SUPPORT, with a sharpening.**

W0-d's five pains are all *accidental* commitment failures. The adversarial reading adds two things:

1. **E-1 has an adversarial twin and it is the same ability.** "A declaration made at t0 is checked against reality at t1" is exactly the property an attacker defeats — and the *cheapest* way to defeat it is not to violate the declaration but to **edit it**. So E-1 as stated is self-referential and incomplete: a commitment tracker whose register is writable by the committed party tracks nothing. E-1 must carry an anti-tamper clause (`L3-07`, `L3-08`, `L3-36`) or it is prose about prose — precisely the failure #179 diagnosed and wfh-002 then committed.
2. **It strengthens the irreducibility argument.** Introspection reports *what happened*; Structure names *units*; Recovery handles *failure*. None has any notion of an obligation with an **owner**, a **deadline**, and a **default outcome on silence** — and "default outcome on silence" is the whole content of P-26. A concern whose defining property is *what happens when nothing happens* is not reducible to three concerns that all activate on events.

Population from this lens: `L3-08`, `L3-26`, `L3-33`, `L3-36`, `L3-37`.

**E-4 (new) — Containment / revocability.** *"The harness bounds what a wrong unit can affect, and can undo it afterward."*

1. **Property of operation?** Yes: the set of effects one unit can produce is bounded and enumerable, and each is reversible or explicitly declared not to be.
2. **Irreducible?** Security is about **preventing** an action (authority bounded *before*); Recovery per §3.1 is about **work surviving failure** — the run is the thing protected. Containment is the opposite direction: it protects **everything outside the run from the run**, and activates precisely when prevention *failed* and the work *succeeded*. Neither seeded concern points that way. Clean test: enumerate a compromised agent's effects and undo them — Security says nothing (the actions were permitted), Recovery says nothing (nothing crashed), Introspection reports but does not act. **This likely passes, but flagged: a maximalist reading of Security-as-blast-radius-management absorbs it**, and triage should make that call.
3. **≥2 capabilities?** Five: `L3-20`, `L3-23`, `L3-24`, `L3-22`, `L3-15`.

**Layering:** downstream of Structure (you cannot enumerate a unit's effects without unit identity — `created_by: anonymous` means this is *blocked* today, not merely unbuilt) and of Introspection. Parallel to Security. **Why a concern rather than five capabilities under Security:** incident cost = detection-time × blast-rate × **remediation cost**, and the seeded eight populate the first two terms heavily and the third **not at all**. The garage has 8 runs of history and cannot answer "what did that agent touch?" about any of them.

**Engaging W0-d's E-2 — calibration: accept the fold, reframe the definition.** "The numbers are checkable" understates it; the property that matters is **the record is correct even when the party it describes wants it wrong** — the difference between an audit and a report. Under an adversary the question is not "is the number right" but "who computed it and could the measured party have influenced the computation." Recommendation: fold into evidence discipline as W0-d says, but carry the adversarial clause into its definition — *an instrument the measured party can influence is not evidence.* Without it, evidence discipline is a documentation standard.

**Not proposed (checked and rejected):** "authority provenance of instructions" (reduces to Security — §3.1 already says *"resistance to instructions arriving through data"*); "non-repudiation" (Introspection + the E-2 clause); "supply-chain integrity" (one capability, `L3-12`, wearing a hat — fails test 3).

---

## Flags for the leader and for triage

1. **`reasoned` vs `field` is the most important sorting key in this register.** 18 of 38 have zero field support. That is what W0-d asked for and warned about — but it means the Security column carries a *fundamentally different evidence class* from the Introspection column, and triage's cost-to-prove should reflect it: `field` candidates have a demand signal, `reasoned` ones have only a mechanism.
2. **Nine candidates turn on a W0-b ambiguity** (A-1, A-2, A-3, A-6, A-7, A-8, A-9, A-11, A-12). Per §11 each routes `needs-a-probe`, never `out`.
3. **`L3-31` applies to this run.** All six lenses shared the same W0 surface. Convergence between them is correlated by construction, and W6's convergence count will overstate independence. Recommend the curator record the shared-surface caveat alongside the count.
4. **The register is deliberately unbalanced toward controls.** `L3-38` is the only counterweight generated, and it should be named: 37 of these abilities make the harness stricter, and the observable end-state of strictness without an appeal path is already sitting in this repo's `.bashrc`. A triage that routes only the locks `in` will reproduce the bypass alias at a higher level of sophistication.
