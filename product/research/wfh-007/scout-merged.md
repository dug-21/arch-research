# scout-merged.md — wfh-007 cross-surface alias reconciliation

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · reconciled by `research-leader` 2026-08-17
**Protocol:** `.claude/workflow/theme-scan.md` — **MANDATORY wherever more than two surfaces are staffed.**
Five surfaces were staffed; all five returned. Scouts cannot see each other and can only *flag* a
suspected alias. This file is the reconciliation, and it runs **before hypothesize**.

**Why it is a requirement and not a step.** wfh-005's four surfaces returned what read as ~15
independent hits on one position; the merge collapsed them to **three clusters, two of which were the
same works reached by different routes**. Unmerged, that run would have overstated its evidence base
roughly fourfold *and had no way to notice*.

---

## 0. The headline number

| | Count |
|---|---:|
| Raw candidates returned across S1–S5 + the S4 annex | **≈59** |
| Distinct objects after reconciliation | **8 clusters + 4 unmerged singletons** |
| Apparent independent corroborations that were the same object under a different name | **at least 21** |

**Inflation factor if unmerged: roughly 4–5×** — the same order as wfh-005. The merge held.

Three separate scouts flagged the collapse risk unprompted (S5 flag 1, S2 flag 1, S4 §3.1), and all
three were right. **S4 additionally flagged a false merge** that would have been the more damaging
error; it is honoured in Cluster 4.

---

## 1. Cluster A — The isolation plane *(the "kernel" slot)*

**Six names, one object.** This is the single largest collapse in the run.

| Surface | Name it arrived under | Instance |
|---|---|---|
| S5 | "the OS sandbox you already have" | bubblewrap+seccomp / Seatbelt / restricted-token+Job Object+WFP, via Claude Code `/sandbox` |
| S1 | **NVIDIA/OpenShell** (C1) | 8,232★, Apache-2.0, kernel-level policy over fs/net/proc/**inference** |
| S4 | **Cloudflare OS** (C16) | 8,487★, Apache-2.0, 2026-08-05 — Sandstorm's architecture, porting cost removed |
| S3 | **PunkGo / "Right to History"** (C3) | Rust "sovereignty kernel", RFC 6962 log + capability isolation, ~1.3 ms, ~400 actions/s |
| S4 | Genode capability delegation · seL4/Microkit · Plan 9 per-process namespace | the lineage |
| S5 | **reference monitor** (Anderson 1972) | *the actual name of the thing the framing calls a "trusted kernel"* |

**Reconciled statement.** The framing's **kernel** component is a fifty-four-year-old named object —
the **reference monitor** — with at least four shipping 2026 instances, two of which (OpenShell,
Cloudflare OS) appeared within the last six months at ~8,000 stars each and are backed by NVIDIA and
Cloudflare respectively. **Nothing in this component is unbuilt, and the two newest instances are
better resourced than anything this garage could field.**

**What genuinely differs across the instances, and it is the only axis triage needs:** OpenShell and
the OS sandbox scope authority *per sandbox, set at creation or hot-reloaded by an operator*.
Cloudflare OS scopes *per gadget, introduced by the user*. None of them scopes **per phase of a
declared task**. That gap is real, small in lines, and is the same gap Cluster C names.

**Do not count as four corroborations of "the kernel is necessary."** They are four implementations
of one well-understood component, and their existence is evidence *against* building it, not for.

**Cost correction carried forward:** S5 reads the OS sandbox as a **counter-example to graph node
#195** ("no system enforces from outside the principal's reach without requiring an operator to run
something"). At ≈0 ops cost on a laptop, #195's own falsifier may now be answerable. **Curator
decision at formalize; flagged, not authored.**

---

## 2. Cluster B — Per-action consequence declaration *(irreversibility)*

**Five names, one object — and this is the run's strongest convergence, because the five are
independent fields that have never cited each other.**

| Surface | Name | Form |
|---|---|---|
| S2 | Apple **`IntentAuthenticationPolicy`** | `.alwaysAllowed` / `.requiresAuthentication` / `.requiresLocalDeviceAuthentication` — OS-enforced, author-declared, ~1.5B devices |
| S2 | Google/Alexa **`secure_devices_pin`** | per-domain step-up, imported into Home Assistant from Google's ontology |
| S2 | HA **Assist exposure allowlist** | the degenerate case — a binary per-entity allowlist, wrong granularity, config-time |
| S3 | **Revisable by Design** (C1) | Idempotent / Reversible / Compensable / Irreversible, **with a proved impossibility result** |
| S4 | **MEL / LCO** (C5) + **14 CFR 43.9(a)** (C7) | typed, time-boxed permitted-non-compliance; licence class as a record field |
| S2 (flagged, unverified) | **MCP tool annotations** | `readOnlyHint` / `destructiveHint` / `idempotentHint` — *explicitly advisory and untrusted by spec* |

**Reconciled statement.** Consequence-as-a-property-of-an-action is **independently reinvented in at
least five unrelated fields**, which is what a real dimension looks like. It is *formally
characterised* (S3: taxonomy + impossibility proof + an ICLP decision procedure), *shipped at consumer
scale* (S2: Apple), and *regulated* (S4: aviation, nuclear, the two-person rule's definition of a
safety-critical operation as one with foreseeably irreversible consequence).

**The contrast that is worth more than either instance alone** — and S2 called it: Apple's annotation
is **OS-enforced but self-declared** by the app author; MCP's is **explicitly untrusted** by its own
spec. Same object, opposite trust postures. **Neither verifies the declaration.** That is the actual
open seam in this cluster, and it is small.

**Evidence bearing on the grid promotion:** three surfaces independently support promoting
**irreversibility and consequence** to a first-class dimension. S2 states it cannot file its
load-bearing finding anywhere in the existing eight; S3 says the dimension is formally characterised,
not taste; S4's whole Axis-D argument runs through it. **The strongest-supported of the four
candidate dimensions.**

---

## 3. Cluster C — Scoped, attenuated, revocable delegation

**Seven names, one object, and wfh-005 already settled its core.**

| Surface | Name |
|---|---|
| S2 | Matter **CATs** (C1) · **FDX consent** (C3) · Spinnaker Fiat's role-containment rule (C4) |
| S3 | **macaroons** · **AIP / Invocation-Bound Capability Tokens** (C2) · SPKI `pathLenConstraint` · **SoK: Delegation and Revocation** · velocity-scaled revocation (C9) |
| S1 | **autogenous** `Mutation::admissible` — monotone attenuation in the type system (C2) |
| S4 | Genode capability delegation · in-toto `functionary` + `threshold` · PROV `actedOnBehalfOf` · ICH E6(R3) §10.1 |
| settled base | **TBAC** (Thomas & Sandhu 1997) · **WAM** (Atluri & Huang 1996) |

**Reconciled statement.** Attenuation and depth-bounding are **solved, shipped, cheap and measured** —
IBCT verifies in 0.049 ms (Rust) and adds 0.086% to a real multi-agent deployment. Spinnaker has
shipped the attenuation invariant ("only users with every role the service account has may use it")
in production CD for years. **This is adopt-shaped, not build-shaped, and nothing in the scan
disturbs that.**

**Two things in this cluster are *not* settled and must not be merged away:**
1. **Revocation cost scales with actor velocity** — O(v·TTL) for time-bounded, D ≤ n for
   execution-count-bounded (S3 C9). Simulation only, single author, `claimed`. But the *shape* of the
   argument does not depend on the simulation, and it governs any credential-lifetime choice.
2. **Aggregation** — a sequence of individually-permitted actions violating a system-level invariant.
   **Forty years old** (Denning), re-named twice independently in 2026 (Tallam's *aggregation
   inference*; Bertino et al.'s *trajectory assurance*), and **unsolved**. S3 names it the surviving
   hard problem; it is the one a six-domain personal system hits first.

---

## 4. Cluster D — The evidence-graded commit *(the notary)*

**The run's centre of gravity. Six names, one object — with one false merge that must NOT be made.**

| Surface | Name |
|---|---|
| S5 | **the notary** — "a record of what was done that the doer cannot write" (the only surviving leg of the kernel position) |
| S3 | the **five-part decomposition**: evidential argumentation (Oren & Norman 2008) · in-toto `predicateType` · history trees / RFC 6962 · bitemporal (SQL:2011) · provenance semirings (PODS 2007) |
| S4 | **PCAOB AS 1105 .08 / ISA 500 A35 / AS 2201 .50** — evidence kinds enumerated **and ranked**, with an insufficiency floor |
| S4 annex | **CDISC Define-XML `def:Origin`** — Type + Source + DocumentRef, FDA-mandated since 2016/2022 |
| S1 | **autogenous** `witness` / `lineage` / `envelope` — ed25519 receipts from ≥2 pinned judges |
| S4 | **C15 — the garage's own D7 firewall**, running in production |

### ⚠ The false merge — honoured

**S4's collision alert is correct and I am enforcing it.** "**Attestation**" in the supply-chain sense
(a signed statement binding a predicate to an artifact *digest*) is **not** "attestation" in the SOX
sense (an auditor's opinion on management's *assertion*). Merging them would repeat exactly the
"soundness" error wfh-005 ruled on. **They stay separate objects in this file and must stay separate
in the graph.**

### Reconciled statement

The primitive is **not novel and not unsolved** — but it is **not assembled anywhere either**, and the
four surfaces disagree productively about which part is hard:

- **Append-only, proved rather than promised** → **solved** (transparency log; use Rekor, don't run one).
- **Declared-kind evidence, cryptographically bound** → **solved in one vertical** (in-toto
  `predicateType`, authenticated with the payload by DSSE's PAE). **KNOWN — graph #190.**
- **Evidence kinds *ranked*, with a floor** → **solved, and only outside computing.** PCAOB/ISA is a
  lattice with comparative operators, seven named procedure kinds, a hard floor ("inquiry alone does
  not provide sufficient evidence") and a contradiction-resolution rule. **Free. No computing artifact
  has an equivalent.** S4 calls it the best hit in its assignment and I agree.
- **Declared-kind evidence, machine-readable and *mandated*** → **shipped in clinical trials** since
  2016 (Define-XML), and it stops in five named places, of which the load-bearing one is that it is
  **retrospective, not enforcing** — a promise about the past, not a precondition on the write.
- **Bitemporality × attestation** → **genuinely open in combination.** S3 and S4 reach this
  independently. Rekor v2 *removed* integrated time. **The most defensible gap in the run.**

### The cost signal — three surfaces, one direction, and it cuts at S5's Class 1

S5's surviving leg rests on the claim that the cheap substitute (*a human reads the diff*) is
inadequate. **The most regulated version of that substitute on earth measured it and is walking away:**

- **~370 data points verified per error found** (Andersen 2015); SDV corrects **1.1%** of the dataset
  (TransCelerate, 1,168 studies); Cochrane finds extensive monitoring **non-inferior at up to 3.4× the
  cost**; I-SPY COVID spent **61,073 person-hours and $6.1M** to change **0.36% of fields and zero
  conclusions**.
- Site monitoring costs **~40× data management** ($1.6M vs $39K per Phase 3).
- **Six regimes reducing this primitive on cost grounds:** FDA suspended enforcement of its own
  audit-trail clause; FDA **deleted design-review independence on 2026-02-02**; SOX 404(b) was
  means-tested by exemption; ICH E6(R3) dropped "source data verification"; FRE 902(13)/(14) replaced
  a witness with paper; **AWS withdrew QLDB**.
- **One counter-signal, and it is the important one:** the only field with no authority model —
  scientific workflow provenance — is the only one that **failed** ("workflow decay").

**Net for triage:** the declaration half is cheap, machine-readable and survives; the human
*verification* half costs everything and finds little. That is an argument for a **deterministic
checker over a typed record**, and against a human review gate — which is precisely the shape S5's
notary and #263's bounded checker/reducer already have.

---

## 5. Cluster E — The secret broker

**Four names, one object — and S4 reframes what the component is *for*.**

| Surface | Instance |
|---|---|
| S2 | 1Password Service Accounts (**explicitly excludes the personal vault**) · Bitwarden Secrets Manager (**not AGPL — `bitwarden_license/`**) · **macOS Keychain ACLs** (code-signing identity as caller identity) |
| S1 | OpenShell **Providers** + **Privacy Router** (strips caller credentials, injects backend credentials) · `wisent-ai/skarbiec` (0★) |
| S4 | **Axis D** — OAuth app registration (Almond) · Mycroft's Selene · Magic Cap's PersonaLink · Zapier's counter-move |
| S3 | SPIFFE/SPIRE + Vault — **KNOWN, #205** |

**Reconciled statement, and it is a reframe rather than a merge.** S2 establishes that **nothing
ships an expiring, attenuable, phase-indexed secret grant for an individual** — the one product that
got scoped programmatic access right rules the personal vault out of scope by design, and the one
genuine per-caller broker (macOS Keychain, 25 years old) has no phase, no expiry, no attenuation and
no delegation chain.

**S4 then says the component's job is not security at all.** *Whoever must hold the credential
relationship for domain N+1 determines who is able to author domain N+1.* Thingpedia capped at
22-of-23-Stanford because a contributor structurally cannot author an OAuth app registration with a
third party. Zapier inverted it — the integrating service holds the relationship — and has **9,958+
apps against Thingpedia's 107**.

**This is the sharpest single reframe the scan produced about a named component**, and it belongs in
the criticality report as such: the secret broker is an **extensibility** component whose security
properties are incidental.

---

## 6. Cluster F — The loop *(the operating model)*

**Four names, one object, and the theme has no vocabulary for any of them.**

Dream Cycle (S1 C3) ≡ Ralph loop ≡ agent-in-a-loop ≡ **loop engineering** (S1 C5) — a self-named
discipline with **>30,000 aggregate stars** using *none of this theme's nouns*. Siblings:
`githubnext/agentics`, Umbrel's 395-line `SKILL.md` packaging contract (S4 C20), `continuous-claude`
(S1 C4).

**Reconciled statement.** This is a **vocabulary miss, not a technology find** — and it is the wfh-005
"Platform Evolution Engine" failure repeating at population scale. Two members already encode
positions this garage reached the hard way: `loop.js` ships a **skeptical, read-only Verify agent**
(gate-input independence, as a read-set restriction, at 135 stars) and `PlanWeave` is **file-backed**
(the `/etc`-as-versioned-files answer). **The theme's watchlist and every scan query to date have been
blind to a field this size.** Watchlist action at CLOSE.

---

## 7. Cluster G — Reviewer throughput is the binding constraint ★ EMERGENT

**Not flagged by any scout as a cluster. It is the strongest cross-surface convergence in the run and
it emerged only at the merge — which is the argument for doing merges.**

| Surface | The measurement |
|---|---|
| S1 | ruvnet: **80 nights → 4 shipped (5%)**, 75 never touched, some 2.5 months stale — for eleven weeks, unnoticed. The detector built to catch it (`zeroMergeStreak`) was itself **permanently miscalibrated and never fired** |
| S4 A1.1 | Home Assistant: **linear at ~+100 integrations/year for seven years**, 1,220 distinct authors, 14,326 merged PRs in 12 months. **Growth does not saturate; the review gate is the only ceiling** |
| S4 Axis A | Every *failed* case: third-party authorship **never started**. Chandler 11/0 in six years; Genode 20 namespaces all employees; Thingpedia 22-of-23 Stanford |
| S4 A1.2 | HA's quality-scale retrofit: **19.7% adoption after 21 months, gold = 13** |
| S4 | Home Assistant **bans autonomous contribution** (2026-07-20) — *"maintainer time is the scarcest resource an open source project has"* |
| S4 A4 | **80% of HA installs are covered by the top 84 integrations**; the median user touches ~2% of the catalogue |

**Reconciled statement — and it reframes the run's own question.** Across an operator running at real
throughput and a survivor running at ecosystem scale, **the measured bottleneck was neither authority
nor capability: it was the rate at which a human could review what the machine produced.** None of the
eight components the framing names addresses it.

**Consequence for output 6:** the criticality report was chartered to rank eight named components. The
empirically demonstrated failure at real scale is a **ninth thing nobody listed**. Ranking eight
components against evidence that says the ninth is binding would answer a question the evidence did
not ask. **Recommend the report carry it explicitly** — as S1 put it, ask *"who reviews domain N+1,"*
not *"how many domains."*

**Note the collision, and do not merge it away:** this is *adjacent to* but *not the same as* the
candidate grid dimension "always-on and proactivity." Proactivity is about the machine acting
unbidden; this is about throughput matching between the fleet and its reviewer. **The theme has no
dimension for the second.**

---

## 8. Cluster H — Controls that are present, believed, and inert

**Five new instances, one of them a meta-instance. Corroborates #196 / #254 from four independent
codebases.**

| Surface | Instance |
|---|---|
| S1 | ruvnet's **branch protection off and zero rulesets on all three repos**, while the loop's headline invariant is "the machine never merges" — enforced by asking the model |
| S1 | **`zeroMergeStreak` permanently miscalibrated (never fires)** — the detector for the 5%-adoption problem, dead. *A control watching for a broken control, broken* |
| S2 | Home Assistant's **entity-permission engine is fully built, fully enforced, and unreachable** — no group-create API, and `USER_POLICY` is entity-identical to `ADMIN_POLICY` |
| S2 | `claude-agent-sdk-typescript` **#172 open 5½ months, maintainer-silent, independently corroborated**: declared subagent tool restrictions are not an enforcement boundary **in the SDK this garage runs on** |
| S5 | **`dangerouslyDisableSandbox`** — the boundary's exemption is held, by default, by the bounded party |
| S4 | **Nextcloud deleted its only per-app capability scoping to cut request latency** (ApiScopes removed 2024-09-10), and a successful ExApp auth now bypasses CORS, 2FA and rate limiting |

**Reconciled statement.** wfh-005 recommended effectiveness-verification as a first-class concern on
one instance. This run adds **six**, from four unrelated codebases, including a *meta*-instance and one
where a capability system was **deliberately removed under production pressure**. The Nextcloud case
is the sharpest counter-evidence in the run to the capability-vocabulary component: **capability checks
lose to p99 latency unless they are structural.**

---

## 9. Unmerged singletons — genuinely independent, no alias found

1. **Home Assistant's vocabulary teardown** (S2 §1) — `homeassistant.turn_on`'s untyped fan-out, the
   script/scene calling-convention collapse, the `data:` dict, and the finding that **reloading a
   config file is admin-gated while executing a shell command on the host is not**. No other surface
   reached it.
2. **The audit-evidence *ranking*** (S4 C1) — every other evidence vocabulary in the scan is
   *enumerated*; only PCAOB/ISA is **ordered**, with a floor. That ordering is the singleton.
3. **The Graydon–Holloway negative** (S3 C7) — a peer-reviewed counterexample result against
   *quantified* evidence confidence. Uniquely, evidence *about* evidence-grading, and it is negative.
   Points at kinded/ordinal grades and away from computed scores — which is what this repo already runs.
4. **Sandstorm's post-mortem** (S4 A2) — the capability model was **exonerated**; the porting cost was
   convicted. Varda's primary 2017/2024 accounts name money and enterprise sales, never capabilities.

---

## 10. Corrections to the run's own premises, carried to the gate

Three, all from scout evidence, none authored by the leader.

1. **SCOPE:18 — "neither built the governance layer" — is FALSE for ruvnet, on artifact.** `autogenous`
   (2026-08-16) ships hash-pinned constitution, monotone attenuation in the types, and promotion that
   cannot consume caller-supplied booleans. The sharper true statement: **he built it and does not run
   on it.**
2. **The second exemplar is unlocatable.** Six formulations returned nothing for "Andre Lamego's
   basement stack / ~1B tokens per week / 99.999% local." The name resolves to SVP & CPO of SAP BTP
   Fabric — an enterprise agent-runtime executive whose actual work *is* the governance layer. **The
   assertion itself could not be recovered, which is strictly weaker than a weak source.** S5's
   challenge brief rested partly on it and should be read with that discount.
3. **The personal-OS framing document does not exist in this repository.** Confirmed independently by
   the leader (grep) and by S4 (§0). The six domains are unenumerated and the five-item domain-add
   contract is undefined; S4 derived failure axes empirically instead and declared the gap.

---

## 11. Coverage-grid input and the instrument caveat

**Grid promotions, on merged evidence:**

| Candidate dimension | Support after merge |
|---|---|
| **Irreversibility and consequence** | **Strong** — Cluster B: five independent fields, a formal taxonomy with an impossibility result, and a shipped consumer instance. S2 and S3 both support promotion; S2 cannot file its load-bearing finding without it |
| **Domain vocabulary** | **Strong, and negatively characterised** — undecidable to verify (HRU 1976), NP-hard to minimise (RMP), measured to leak at every shipped granularity (Felt 2011; Granite 46.6%; FORTIS) |
| **The person model** | **No evidence from any surface.** S3 and S2 both say so explicitly. A hole, not a refutation |
| **Always-on and proactivity** | **Adverse evidence** — S5 §6a: the wearable graveyard is unambiguous, and discomfort with always-on listening is *growing* (38% → 47%). Survives only as "voice on hardware the user already owns" |
| ★ **Reviewer / review-throughput matching** | **Unlisted, and the best-measured constraint in the run** (Cluster G). Recommend the owner consider it as a fifth candidate |

**⚠ Instrument caveat, binding on every coverage call this run makes.** All five scouts hit a
**200/200 WebSearch cap that was shared session-wide, not per-agent.** S1, S2, S3, S4 and S5 each
declared it. The bias runs *against* sources that must be discovered (blog post-mortems, practitioner
writing, small projects) and *toward* sources with guessable canonical URLs (regulations, RFCs, specs,
repos). **No surface may be called exhausted on this run**, and a thin result on any surface is the
instrument, not the territory. This must be stated in the coverage call, not buried.

**Standing method holes, still unspent after five surfaces:** patent prior art (S3 narrowed it —
Google Patents does not render for WebFetch, so keyword patent search is unavailable with these tools;
recommend recording that as a method finding rather than re-tasking a scout) · rail interlocking
(open since wfh-005) · Manifest V3 developer attrition (S4's highest-value missing evidence for Axis
B) · the OpenClaw ecosystem (51,996★, corroborated from three independent directions, entirely
unread).

---

## 12. Round-two triggers *(protocol #215: fires on a load-bearing hole, not a thin cell)*

Ranked by whether closing them would **change a verdict or a routing**:

1. **OpenShell's policy hot-reload latency and atomicity** — decides whether Cluster A's plane can sit
   inside a turn, which decides whether phase-indexed authority is an assembly or a build. **No figure
   published.** Highest value.
2. **Cloudflare OS at depth** — twelve days old, 8,487★, and it is the live instance of this run's
   thesis. Only S4 reached it, and only through a README.
3. **Commercial CD stage-scoped role binding, closed by S2 (C4)** — *already closed*, and the answer
   sharpens Cluster C: incumbents bind `phase → pre-existing credential`, never `declared demand →
   minted ceiling`. **The wfh-005 hole is now shut; record it.**
4. **`autogenous` source** — every structural guarantee is `[asserted]` at "the types enforce this,"
   from a maintainer whose flagship shipped its policy plane inert by default (#200).
5. **Manifest V3 developer attrition** — the cleanest available test of Axis B's anti-correlation.

---

## 13. Handoff to hypothesize

**What the hypothesizer receives:** the five scout files, the S4 amendment, the S4 clinical-EDC annex,
and this reconciliation. **It must read this file first**, because four of the eight clusters would
otherwise read as independent corroboration of a component's necessity when they are one object under
several names.

**Three things it must be told plainly, and they narrow the divergent space rather than widening it:**

- **The kernel is built, four times over, by better-resourced parties.** Generating hypotheses that
  re-invent it is spent range.
- **SCOPE:18's premise is falsified** (§10.1). Left uncorrected, the divergent step will spend its
  budget inventing what already ships.
- **The uncovered remainder across every cluster is the same pair:** *authority indexed to a phase of
  a declared task*, and *a commit whose evidence kind is checked at write time rather than promised
  retrospectively*. Everything else in the framing has a shipped owner.

**Nothing in this file is `proven`. Zero status moved. Structure only, by design.**
