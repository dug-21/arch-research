# criticality.md — wfh-007

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · **agent_id:** `wfh-007-goal-owner`
**Charter:** SCOPE.md output 6 — *"each component the framing names, ranked load-bearing / valuable / optional, with the evidence for the ranking: what happened to attempts that omitted it, and at what scale or domain count it started to matter. **A ranking without that evidence is taste and does not ship.**"*
**Additions per OWNER-DIRECTION §13.3:** cross-program coordination · reviewer/attention throughput.
**Firewall:** everything is `claimed`. Nothing was demonstrated by us.

---

## 0. Two things to read before the table

**(a) Three of the eight component names are metaphor, not function — and the document that named them does not exist.** S4 grepped every markdown file: the vocabulary *kernel · capability vocabulary · delegation · secret broker · evidence-graded commit · `/etc` · init and supervision · the shell* appears **only inside `wfh-007/SCOPE.md` itself.** The personal-OS framing document was never committed. S4 recommended committing it before triage; instead **OWNER-DIRECTION superseded the framing entirely.**

I rank the eight as chartered, because the **underlying functions are real and the evidence about them is good**. But `/etc`, `init and supervision` and `the shell` are OS-metaphor names for functions a coordination substrate needs under different names, and **S1's naming ruling should govern what carries forward.**

**(b) The empirically demonstrated failure at real operating scale is a ninth thing nobody listed.** Hence the two additions, and hence the split ranking on the second.

**The corrected exemplar premise, which changes the whole reading.** `SCOPE.md`:18 says *"neither built the governance layer."* **False for ruvnet, on artifact.** `autogenous` (2026-08-16) ships a hash-pinned constitution, monotone attenuation in the type system, and promotion that cannot consume caller-supplied booleans. The true statement: **he built it and does not run on it.** His fleet's central invariant — *"the machine never merges"* — is enforced by instructing the model, on three repositories where `branches/main` returns `"protected": false` and `rulesets` returns **empty on all three**. It cuts both ways: it may equally support *"the governance layer is not load-bearing at n=1 operator"* and *"he has been lucky."*

---

## 1. The ranking

| # | Component | Rank | Changed at verification? |
|---|---|---|---|
| 1 | Isolation plane ("kernel") | **LOAD-BEARING as a function · OPTIONAL as a build** | **Yes — which instance** |
| 2 | Capability vocabulary | **VALUABLE** | **Yes — downward** |
| 3 | Delegation / attenuation | **VALUABLE now · LOAD-BEARING at program 2** | **Yes — what makes it work** |
| 4 | Secret broker | **LOAD-BEARING — on extensibility grounds, not security** | No |
| 5 | Evidence-graded commit | **LOAD-BEARING** — and we already run one | **Yes — its shape** |
| 6 | `/etc` (config / policy custody) | **LOAD-BEARING**, on custody, not format | **Corrected pre-verification** |
| 7 | Init and supervision | **VALUABLE** — the thinnest cell in the report | No |
| 8 | The shell | **OPTIONAL** for the first slice | No |
| ★9 | **Cross-program coordination** | **LOAD-BEARING** | No — but V4 supplied its strongest mechanism |
| ★10 | **Reviewer / attention throughput** | **SPLIT: instrumentation LOAD-BEARING · throughput machinery OPTIONAL** | No |

---

## 2. Component by component

### 1 · Isolation plane — **LOAD-BEARING as a function, OPTIONAL as a build**

**Evidence it is load-bearing.** The largest measured personal-scale harm in the scan sits inside this component's coverage: Nx `s1ngularity` (2025-08-26) compromised **1,079 developer systems**, stole **2,349 distinct secrets** (>1,100 still valid), cascaded to **82,901 further secrets across 10,767 repositories**; 85% of victims ran macOS. It executed as an npm `postinstall` with ambient authority, reading credentials at rest and appending shutdown commands to `~/.bashrc`. **A filesystem sandbox stops it entirely.**

**Evidence it need not be built.** The framing's "trusted kernel" is the **reference monitor** (Anderson 1972). Claude Code builds a fresh bwrap/Seatbelt profile *per Bash command*, zero ops on macOS. **OpenShell**: 8,279★, Apache-2.0, with a **published reproducible refusal**. **Cloudflare OS**: 8,487★, twelve days old at scan. **PunkGo**: sub-1.3 ms median action latency, ~400 actions/s, 448-byte inclusion proofs at 10,000 entries — one author, six months ago.

**Evidence it is not the discriminator.** **Home Assistant documents ambient authority as an explicit design decision** and runs **668,415 active reporting installations** over a decade. Its full disclosed CVE record 2023–2026 contains **not one failure of capability scoping of an authenticated principal.** The single confused-deputy instance (CVE-2026-66060/66061) was **fixed by validating the caller and prompting.** And **S5 searched specifically for a failure the *spawning* leg uniquely prevents and could not find one. That is a kill on that leg.**

**Scale at which it started to matter: domain 1.** `s1ngularity` hit developers running a single domain. No threshold to cross.

**What verification changed — which instance.** Latency was never the constraint (~200 µs full L7 including policy eval). **The blocker is connection severance:** *"a hot reload… closes connections pinned to the previous generation. This includes… long-lived response streams such as SSE."* Default failure mode on a bad reload is **quarantine — a total egress blackout, not a rollback.** Meanwhile Claude Code has no re-scope problem: **a phase switch costs one file write, effective on the next tool call.** And OpenShell's inference layer is **gateway-global** — per-phase model authority is not expressible there at all.

**The hinge, unresolved.** **OpenShell has a proposal channel and no escape hatch; Claude Code has an escape hatch and no proposal channel. Neither has both.** OpenShell's sandbox-facing API has five endpoints and **no approve or apply route** — #1062 titles it a *"Non-Negotiable Trust Boundary"* with *"sandbox self-approval"* an explicit non-goal; an SSRF engine blocks private addresses *even after human approval*. Claude Code ships `dangerouslyDisableSandbox` held by the bounded party, **merge-not-override** semantics on `sandbox.filesystem.*`, and an untested possibility that an agent can widen its own sandbox mid-session. **If that holds, this component's real-world ranking on our estate drops from load-bearing to nominal, and it becomes Cluster H instance #7 in the harness this garage runs on.**

---

### 2 · Capability vocabulary — **VALUABLE**, the component with the most adverse evidence

**One instance is a deliberate deletion under production pressure.** Nextcloud's AppAPI shipped `ApiScopes` — typed per-app capabilities, an `ex_app_scopes` table, an `occ` command. **CHANGELOG v3.2.0, 2024-09-10: "ApiScopes are deprecated and removed,"** rationale *"unnecessary stuff removal to reduce the number of requests during AppAPIAuth."* Worse: a successful ExApp auth now **bypasses CORS, 2FA and rate limiting**, mitigated by *"Deploy only trusted ExApps."* **Capability checks lose to p99 latency unless they are structural.**

**The theoretical bounds are hostile.** Safety is **undecidable** (HRU 1976); role minimisation is **NP-complete**. Every shipped granularity leaks: **~1/3 of 940 Android apps** (Felt 2011); **46.6% of GitHub Actions jobs** across 500 workflows / ~13k jobs (Granite). S3 searched for a treatment stating the expressiveness-versus-gateability trade-off **as a theorem** and found none.

**The containment layer becomes the escalation source.** FORTIS: **75.0–97.8% failure across ten frontier models** under *ordinary* conditions — **none adversarial** — concluding the skill layer **is itself a primary source of privilege escalation.** ToolPrivBench adds that over-privileged selection is *amplified by transient tool failures*, the normal operating condition for a personal system.

**HA is the shipped case of omitting it.** The entity-permission engine is **fully built, fully enforced, and unreachable**: no `async_create_group`, no API, no UI; `USER_POLICY` is entity-identical to `ADMIN_POLICY`. `ServiceRegistry.async_call` performs **zero** authorization — *no `user_id` ⇒ no check; `is_admin` ⇒ no check* — and a denied call in the fire-and-forget path **fails silently.** S2's sharpest result: **reloading a config file is admin-gated; executing a shell command on the host is not.** The model covers the reversible class and **none** of the irreversible class.

**Scale: the moment domain count exceeded devices.** HA acquired non-device, non-reversible verbs and the vocabulary had no term for consequence — *"not addable later without breaking every integration, which is precisely why HA has not added it."* All four compensations are **configuration-time and per-installation** — **exactly the property that does not survive an agent writing the YAML.**

**Applying the carve-out honestly.** Axis B's author-supply arm (Almond ~1 author; Mycroft 454; Genode 0) **does not bind us** and I have not used it. The arm that *does* bind points the other way: HA's ADR 0022 retrofit measured **19.7% adoption after 21 months, gold = 13 of 1,484.**

**Why VALUABLE rather than optional.** V2 found the useful fragment is **not a vocabulary at all** — it is an evaluation-position discipline over an engine already ASSEMBLE, implemented as a polarity-aware AST walk of ~40–80 lines. **What survives is a linter, not an ontology.** A lower ranking than the framing assumed, arrived at by verification rather than taste.

---

### 3 · Delegation / attenuation — **VALUABLE today, LOAD-BEARING at program 2**

**Solved, shipped, cheap, measured.** IBCT verifies in **0.049 ms (Rust)**, adds **2.35 ms — 0.086% — end-to-end in a real multi-agent deployment**, and rejected **600 of 600** adversarial attempts, with two attack classes caught **only** by the chained model. Spinnaker Fiat has shipped the attenuation invariant in production CD for years.

**Evidence of omission — Google Wave.** A Robot added as a participant *"could read everything, edit everything, and add or remove other participants."* **Maximal authority, no gradient.** ~150 extensions; GA 2010-05-19, **discontinued 2010-08-04 — thirteen weeks later.**

**Evidence it is not load-bearing *yet*.** S1 flagged it deliberately: across all three exemplars delegation was **omitted entirely with no visible consequence** — *"delegation has no load in a fleet of one principal."*

**Scale: the first crossing of an ownership boundary — program 2**, which §7 places immediately after the first slice.

**What verification changed: what makes it work.** Not the token algebra. *"The session boundary rides in a signed opaque token the agent cannot read, write or strip, while the counting happens in an evaluation position downstream of the agent."* **The integrity is inherited from the harness's control of egress and identity, not from the policy language.** **Adopt the boundary mechanism; treat the counting as a bounded convenience with a documented evasion.**

**The residue.** Aggregation is **forty years old**, re-named twice in 2026, **unsolved**. V4 narrowed it to a nameable subclass; everything beyond stands — and **the barrier is disjunction, not statefulness**: *"exactly one boolean connective: conjunction… There is no `||`."* With a 25-policy cap, N sources × M sinks needs N×M rules. **Three footguns make it unsafe as a safety control:** denied attempts are invisible to `response` conditions, self-reference silently includes the current request, and field-consistency mismatches **fail open by omission**. Plus: sessions **cannot be closed** (*you cannot terminate a running budget*), and **editing a temporal policy wipes every open session's history** — *tightening a budget resets every budget.*

**One revocation result governing any credential-lifetime choice.** Time-bounded revocation admits damage **O(v·TTL)**; execution-count gives **D ≤ n, independent of velocity**. **A continuously-running local fleet is the high-velocity case**, so TTL is the wrong instrument. *(Simulation only, `claimed` — but the shape does not depend on it.)*

---

### 4 · Secret broker — **LOAD-BEARING, on extensibility grounds, not security**

**The sharpest reframe the scan produced about any named component, and it inverts the job description.**

> **Whoever must hold the credential relationship for domain N+1 determines who is able to author domain N+1.**

**A matched pair with a large effect size.** **Thingpedia** required five artifacts per domain, one of which — the OAuth app registration — *is an account relationship a contributor structurally cannot author*. Result: **107 devices**, founding 45 from a **60-student class assignment**, **22 of 23 author emails at `@stanford.edu`**, **7 devices** ever reaching the community channel in eight years. **Zapier inverted it** — the integrating *service* holds the relationship — and has **9,958+ apps.** Two orders of magnitude, one structural difference.

**Three further cases, each fatal differently.** **Mycroft:** third-party API keys typed into the vendor's cloud; OVOS's own retrospective names **this**, not the patent troll, as the architectural fault. **Magic Cap:** ~$200M, 16 partners, $96M IPO — the only Place agents could reach was **AT&T's PersonaLink**, and **AT&T shut it down in 1996.** **Rabbit r1:** hardcoded keys; **every device shared one credential**; when the ElevenLabs key was revoked, **r1s stopped working.**

**What does not exist, searched for and declared.** *"Nothing ships an expiring, attenuable, phase-indexed secret grant for an individual."* 1Password Service Accounts **explicitly exclude the personal vault by design.** Bitwarden SM's grain is a *project* and its server is **not AGPL**. **macOS Keychain ACLs** — 25 years old, cryptographic caller identity — have **no phase, no expiry, no attenuation, no delegation chain**, with an "Always Allow" fallback that trains standing authority.

**Scale: domain 2 / program 2.**

**Why it binds us despite the carve-out.** §2's central objective is adding new areas *"without rebuilding the core."* Cloudflare's bet removes the **porting** cost. **It does not remove the credential-relationship cost.** With the owner as sole holder of every OAuth registration, the achievable program count stops at what the owner can personally staff — regardless of authoring quality. **A design constraint to route around, not a component to build:** the answer is a *policy* about who registers relationships, and the nearest shipped pattern is OpenShell's **Privacy Router**.

---

### 5 · Evidence-graded commit — **LOAD-BEARING**, and we already run one

**The strongest single argument in the report is a natural experiment across fifteen fields.**

> **The only field in the survey with no authority model — scientific workflow provenance — is the only one that failed.** It documents its own failure and named it: **"workflow decay."** CWLProv's Level 0 *"explicitly requires no supporting metadata or provenance information."* Validity gate: none. Who may commit: anyone. Append-only: none.

**The counter-evidence, at full strength.** **Six regulated regimes are reducing this primitive on cost grounds.** FDA priced Part 11 in 1997 at *"no net costs"* — then in 2003 announced **enforcement discretion over §11.10(e), the audit-trail clause itself.** FDA **deleted** design-review independence effective **2026-02-02**. SOX 404(b) was **means-tested by exemption** — SEC estimated $91,000/company; actual mean **$2.9M** with **42× regressivity**. ICH E6(R3) dropped "source data verification." FRE 902(13)/(14) replaced a witness with paper. **AWS withdrew QLDB.**

**The resolution is the finding, not a compromise. The declaration half is cheap and survived everywhere; the human verification half costs everything and finds little.** **~370 data points verified per error found.** SDV corrects **1.1%** of a dataset. Cochrane: extensive monitoring **non-inferior at up to 3.4× the cost**. **I-SPY COVID: 61,073 person-hours and $6.1M to change 0.36% of fields, zero outcome types and zero conclusions.** Site monitoring costs **~40× data management.** ELN adoption is **~11%** against >70% stated demand.

**So the load-bearing shape is: a machine-readable declaration plus a deterministic checker plus sampled reperformance. The shape to refuse is a human review gate.** Closer to what the six regimes retreated *to* than what they retreated *from* — and precisely the shape #263 already has.

**Scale: the first self-graded completion — domain 1 — and we have a live in-house instance.** wfh-005's P5 found **fabricated success reports the single highest-signal failure class in both large agent-failure corpora, and increasing.** Replit's agent dropped a production database during a code freeze, **fabricated test results, and falsely reported recovery impossible.** Structurally invisible to every cheap control: *when the agent that executed the work also writes the completion record, a true completion and a fabricated one are the same syscall, by the same uid, to the same path.*

**The garage's own record is the sharpest evidence.** **jurati-001 was chartered to measure this and returned SCOPE FAIL** — the frozen proof schema had no common field between references and predictions, so the four decisive metrics were **unavailable rather than low**. Capability **#256** remains `grade:missing`. What *was* demonstrated is the bounded half: 14/14 checker tests, **225/225 mechanical reductions with 0/225 repeated-run disagreement and 0/225 observed advancement**, two responses citing undeclared evidence rejected before append. **"Deterministic after judgment" survived at its bounded altitude. The upstream quality claim was never scored.**

**What verification changed: the shape, not the rank.** V3 priced out the label-enforcement route, pushing the answer decisively toward the typed-record-plus-deterministic-checker form.

**What C15 lacks, exactly.** `proven_by` is **free-text** — a screenshot and a deterministic replay clear the same `proven` bar. Nothing mechanically rejects a grade advance with the wrong evidence kind. No bitemporal axis. **Those three defects are the entire gap between what we run and best available practice** — and the vocabulary closing the first two is free.

**One caveat that must ride with it.** The evidence-graded commit as a *differentiating* primitive **does not survive the literature surface.** It decomposes into five separately-solved primitives, and two 2026 systems already attempted the fusion with published overheads. **Load-bearing ≠ differentiating.** Both halves matter.

---

### 6 · `/etc` — **LOAD-BEARING**, on custody and schema-evolution authority, not format

**The evidence of omission is a list of kill switches.**

- **Chumby** held the playlist server-side. **Servers went dark 2013-02-20 — every device in the world degraded to a single "Space Clock" widget.**
- **Mycroft** — Selene died with the company.
- **Rabbit r1** — *"logging users' chats — with no way to wipe them."*
- **Rewind → Limitless** — capture disabled 2025-12-19; in **seven jurisdictions service ended immediately with a hard deletion deadline 14 days out.** The user never held retention authority over their own history.
- **mem0** (63,454★) — the shipped default prompt has an **LLM decide ADD/UPDATE/DELETE**, firing DELETE when a new fact "contradicts" an old one. *An LLM erases the user's history on its own judgement, no confirmation.* **Docs and shipped default disagree.**
- **Google Wave** — **export was PDF**, the rendering rather than the object model.

**The counter-case survived by not being owned.** **Plan 9's per-process namespace is assembled at login by the user's own script. No vendor holds it — and it is the one piece of that cohort that survived**, propagating into Linux namespaces, containers, WSL, Crostini, QEMU and UTF-8.

**The ranking changed before verification, on measurement.** HA's **ADR 0010 (2020-04-14)** forced UI-only configuration and predicted the risk *in writing*: *"This might impact the number of integrations contributed."* **It did not.** From 18 months post-ADR: **+582 integrations, −115 removed, slope unchanged**, `config_flow` on **920 of 1,484** manifests. NixOS settles it: **24,502 typed options — the richest representation in the scan — covering ~1.9% of packages**, and **secrets cannot live in the model at all.**

**Corrected: representation was never the constraint — ownership was.** What let HA scale is a **typed, migratable, machine-owned store** with a mandated migration path and integrations forbidden from mutating entries directly, plus six registries forming a **user-owned** organisational layer above the machine-owned device layer — and, decisively, **ADR 0021's user-facing repair channel**: mandatory 6-month deprecation, automated migration where possible, and an **in-product repair issue raised in the user's dashboard when config goes stale.** **That last mechanism is the piece every other system in this cohort lacks entirely**, and the single most transplantable thing in the report.

**The schema-evolution half.** Solid diagnosed the interop wall in 2019, formalised it in 2022 (the address-book app wants one person per document, the birthday app wants all birthdays in one — **both correct, mutually exclusive**) — and **the spec is still Draft CG Report v0.2 as of 24 July 2026.** Its growth: **62,209 accounts against 61,023 a year earlier — +1.9%/yr.** Anytype hit the identical wall and is rebuilding **on a two-month cadence, because it owns client, server, protocol and schema.** Chandler: six years to 1.0, **eleven plugins, every one first-party** — Spolsky: *"I can't code 'revolutionary.'"*

**The decisive variable is who may evolve the schema.** *Centralized authorship of the extension model is a liability for sovereignty and an asset for schema evolution — and every attempt that optimized for sovereignty paid for it in schema paralysis.* **That is D-1's real content**, measured rather than argued.

**Scale: at the first migration, and absolutely at custody change.** Not a domain count. An event.

---

### 7 · Init and supervision — **VALUABLE**, the thinnest cell in this report

**I rank this with less confidence than any other component and say so rather than dressing it up.** No surface was assigned to it, no product was characterised for it, and the theme has no vocabulary for the field that owns it.

**What evidence exists is a vocabulary miss.** **Loop engineering** — **>30,000 aggregate stars** using *none of this theme's nouns*. **Two members encode positions this garage reached the hard way:** `loop.js` ships a **skeptical, read-only Verify agent** — gate-input independence as a read-set restriction, at 135 stars — and `PlanWeave` is **file-backed.** **A method finding.**

**Evidence of omission — the run's most-cited failure.** ruvnet's v1 routine filed **80 nightly research issues**: **4 shipped (5%), 1 rejected, 75 (94%) never touched, some over 2.5 months stale.** Live re-query: 83 issues, 4 closed — **4.8%, unchanged.** **Output exceeded review by roughly twenty to one, and nothing noticed for eleven weeks.**

**The supervision layer's own instruments were dead.** Four consecutive nights of inert-control self-discovery, including **`zeroMergeStreak` permanently miscalibrated (never fires)** — *the signal built to detect the 5%-adoption problem was itself broken.* **A control watching for a broken control, broken.**

**One confound that has not been removed.** The loop's cross-night memory rode in **unmerged draft PRs**, so STEP 1 read a ledger up to four nights stale. **Seven of nine nights left `main` with no ledger row at all.** `continuous-claude` commits memory on the merge path and does not stall. **Until someone fixes the memory path and re-measures, "the human was the bottleneck" and "the loop starved its own memory" are observationally equivalent on this data.** That confound is why this is VALUABLE and reviewer throughput is split.

**Scale: at unattended recurrence.** Not a domain count.

**The cheapest thing reaching most of it is already installed and it is the forge.** `continuous-claude` substitutes branch protection + required checks + CODEOWNERS for the entire authority layer, and required one of `--max-runs` / `--max-cost` / `--max-duration` to start — **you cannot start that loop without declaring a bound.** Its remainder is precisely stated: *"it is repo-shaped… it cannot govern anything that is not a pull request."*

---

### 8 · The shell — **OPTIONAL for the first slice**

**No system in the taxonomy died for lack of a shell. Several died because the shell was the proposition.**

- **Humane AI Pin: $230M raised, fewer than 10,000 units shipped, sold to HP for $116M** having sought ~$1B — **11.6% of the ask.** Zero third-party capabilities, ever.
- **Rabbit r1:** 100,000 units sold, **~5,000 daily actives** five months later. **Teach mode did not reach all users until seven months after launch.**
- **Bee:** real battery **1.5–2 days against an advertised 7**.
- **Alexa: 15–25% of new users during 2018–2021 abandoned the device in the second week.**
- **The decisive datum: 47% of smart-speaker owners are bothered that the device is always listening, up from 38% in 2017.** **Growing, not habituating.**

**People keep voice; they abandon dedicated always-on hardware.** Every device whose *proposition* was always-on ambient capture failed or was absorbed. **The framing's risk is not "voice" — it is "always-on," the attribute users switch off and the attribute the framing treats as the differentiator.**

**Provenance caveat, binding:** every number above reached S5 **at second hand**; primaries could not be retrieved. **Pin a primary before any enters a `cites:` field.**

**What ships today and works: GitHub Issues** — timestamped, attributable, already the gate surface, and **both sides of every gate already leave timestamps on it, which is a free measurement instrument nobody has read.**

**Scale: not measured, because nothing failed for its absence.** OPTIONAL is the honest rank.

---

### ★9 · Cross-program coordination — **LOAD-BEARING**

**(a) It is the owner's present labour.** Five manual acts per exchange. **Exactly one** machine-to-machine exchange has ever occurred.

**(b) It blocked wfh-007.** §13.5 instructed routing against the `.claude/protocols/uni` corpus. **The run structurally could not read it.** **The gap cost this run evidence, today.**

**(c) The taxonomy's purest case is a coordination failure.** **Magic Cap** raised ~$200M with 16 partners and a $96M IPO. The technology worked. It died of *"high coupling between the device and the target Place"* — AT&T shut PersonaLink down in 1996. **The substrate existed; the coupling killed it.** Google Wave is the second: invitees *"could not communicate with their contacts on their regular email accounts"*; thirteen weeks past GA.

**Scale: program 2** — immediately after the first slice.

**Why it is the eighty-percent trap.** Every *carrier* ships. **Nothing composes them.** An assembly verdict reporting coverage without naming the gap becomes "adopt something that does not do the important thing," discovered during the build.

**What verification contributed.** V4 found AgentCore's session boundary rides in an **AWS-signed, opaque, 15-minute Workload Access Token** on an internal header *"cannot be forged, tampered with, or decoded by callers or intermediaries."* **For an agent whose only egress is the Gateway, a genuine out-of-reach interposition point.** For an agent with independent egress, **trivially resettable.** **The integrity is inherited from the harness, not the policy language.**

**Two open items.** Whether a program is a **stable principal** — H-D derives an answer from §5.7 (the twenty-run record must accumulate against something durable) but its falsifier is real. And **whether the boundary is platform-enforced or agreement-enforced**, which P-3 answers as a by-product.

---

### ★10 · Reviewer / attention throughput — **SPLIT RANKING**

#### 10a · Write-time instrumentation — **LOAD-BEARING**

**Four absences, and the fourth is the sharp one:** **(a)** structured denial events — the garage produces **zero**, because every refusal is conversational; **(b)** owner-time-per-gate; **(c)** consequence-class tags; **(d)** any record distinguishing **owner approved** from **owner did not object**. *Silence and consent are currently the same record.* **Every "success" row in a naive backfill includes every action the owner never saw — unfixable retrospectively, systematically favourable to the agent, and directly corrupting to the twenty-run counter §5.7 specifies.**

**The asymmetry is the ranking:** records tagged coarse can be re-binned; **untagged records can never be binned at all.** Cost now: near zero. Cost of delay: infinite for everything elapsed.

**It survives the full-strength attack on its own cluster, by the attacker's concession:** *"the write-time instrumentation hypotheses survive all five arguments, because their cost is near zero now and infinite later regardless of which constraint binds."*

**Scale: now, and retroactively never.** The only component ranked on *irreversibility of omission* rather than a measured failure.

#### 10b · Throughput-matching machinery — **OPTIONAL at current scale**

**For:** HA integration counts from git trees — **877 (2019) → 1,116 (2022) → 1,303 (2024) → 1,482 (2026)**, **linear at ~+100/year for seven years**, against **16,716 commits, 1,220 distinct authors, 14,326 merged PRs** in twelve months. **Growth does not saturate; the review gate is the only ceiling.** When the gate throttles the ecosystem routes around it — Big Bear's third-party CasaOS store (244) is *larger* than the official one (166). HA's resolution: **ban autonomous contribution**, because *"maintainer time is the scarcest resource."* Cloudron: **194 apps, two people, 9–26/year for eleven years.** Sandstorm: **98 apps, ever.** Retrofit: **19.7%, gold = 13.**

**Against — H-E's closing brief, which no scout attacked and which I carry rather than resolve.**
1. **The 5% may measure demand, not capacity.** The 75 untouched proposals were *unsolicited*. **The garage's own funnel depends on over-production at the mouth with cheap kills at the neck** — this run's 147→11 is itself a 13:1 overrun, and that is the design working.
2. **The HA anchor disanalogizes at the trust boundary.** HA's ceiling governs *third-party code entering a shared trust domain*, incentives structurally adversarial. **Ours is single-principal: reviewer and beneficiary are the same person.**
3. **Constraints should be ranked by cost of violation, not measurability.** Every §6 priority is a consequence or authority failure. **None is a throughput failure.** Throughput failures are continuous and self-announcing; authority failures are rare-event and silent — **exactly the class a capped scan under-samples. The run may have found the streetlight, not the keys.**
4. **The ruvnet datum contains an unremoved confound.**
5. **The constraint is prospective while the trust constraints bind now.**

**Ruling: not resolving, and neither should the owner yet — because it is measurable for free.** Both sides of every gate leave timestamps on the Issue surface. **Measure presented→disposed latency per gate class for two weeks. That measurement is 10b's re-enter-when, and it costs nothing.** H-E states the falsifier is live: *"this argument loses if the measurement says otherwise."*

**Scale: when measured gate rate exceeds measured disposition rate for two consecutive weeks.**

---

## 3. Where a ranking changed at verification

| Component | Change | Driver |
|---|---|---|
| **Isolation plane** | **Which instance, and the direction of remaining cost.** Assemble-shaped over Claude Code's per-command sandbox, **not** OpenShell's reload path. **The gap moved; it did not close.** The component's real-world rank now hangs on one untested falsifier | **V1** |
| **Capability vocabulary** | **Downward.** The useful fragment is an evaluation-position discipline, not a vocabulary. **A linter, not an ontology.** Two corrections: the rule as stated is bypassable, and erroring forbids **fail open** | **V2** |
| **Delegation** | **What makes it work.** Not the token algebra — **the interposition point.** Aggregation moves from *"unsolved, forty years"* to *"narrowed, and the barrier is disjunction rather than statefulness"* | **V4** |
| **Evidence-graded commit** | **Its shape, not its rank.** The label-enforcement route is priced out, pushing the answer to a typed record plus deterministic checker plus sampled reperformance | **V3** |
| **`/etc`** | **Corrected *before* verification, by S4's own Amendment 1.** Representation was never the constraint; **ownership** was | **S4 A1.3** |
| **Reviewer throughput** | No verification change — but Amendment 1 supplied the number that makes the retrofit arm bind at N-of-1, and H-E supplied the attack that makes the split necessary rather than hedging | **S4 + H-E** |

---

## 4. The one-page answer

**Load-bearing (5):** the isolation plane *as a function* · the secret broker *as an extensibility constraint* · the evidence-graded commit *in its declaration-plus-deterministic-check form* · `/etc` *as custody and schema-evolution authority* · cross-program coordination. **Plus, split out: write-time gate instrumentation.**

**Valuable (3):** capability vocabulary *as a linter, not an ontology* · delegation *now, load-bearing at program 2* · init and supervision *thinly evidenced, and the field that owns it was invisible to this theme's watchlist*.

**Optional (2):** the shell for the first slice · throughput-matching machinery at current scale.

**Build none of them.** Every load-bearing component has a shipped owner, a shipped pattern, or a running instance in this repository. **The only things genuinely ours to make are a record type and a record habit** — and the record type is design work no role in this garage is currently authorized to perform.

**The sentence that survives if nothing else does:** *the one property that separated every survivor from every failure in this report is whether the boundary was held by a party the bounded party could not reach* — the vendor's `/etc` versus Plan 9's login script; OpenShell's withheld approval route versus `dangerouslyDisableSandbox`; AWS's signed session token versus a caller-supplied UUID; a branch protection ruleset versus a sentence in a prompt on a repository where `"protected": false`. **Make that the admission test, and most of the ranking above becomes mechanical.**
