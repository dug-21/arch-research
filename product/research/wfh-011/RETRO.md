# wfh-011 — RETROSPECTIVE

**Role:** `factory-retro` · **Run:** `wfh-011` · theme `workflow-harness` · [Issue #70](https://github.com/dug-21/arch-research/issues/70) (closed)
**Run method stamp:** `wf-v0.26-11-gaaa64b2` · **Repo state:** `main` at `7a80285`
**Outcome under retro:** directional, structure-only. Verdict `revise` / `current-project fit: revise` /
`post-bounded-evolution fit: revise`. Coverage gate `REWORKABLE` then `PASS` at round 2 of 2.

> **PEN CLOSED.** The owner's zero-Unimatrix-content-writes instruction for `wfh-011` holds through
> close and was not lifted for this retrospective. **This retro performed no `context_store`,
> `context_correct`, `context_tag`, `context_edge`, `context_deprecate` or `context_quarantine` — no
> node, no edge, no tag, no lifecycle move, no grade movement.** Read-only `context_*` and one
> `context_cycle_review(auto_close:false)` only. Every graph entry this run earned is listed unwritten
> at §6, for the owner to approve or refuse separately.

> **ONE ITEM NEEDS THE OWNER BEFORE ANYTHING ELSE HERE.** Issue #70's escalation 1 puts a number to the
> owner — *"all 34 declared-inverse rows … 22 are true by accident, 12 are false."* **That number is
> wrong. The correct split is 25 true / 9 false.** `w4-witness.py`'s reader silently drops every
> attributed relation entry, and three of the twelve "false" rows in fact close (5/5 and 16/16).
> Verified three ways at the artifacts (§2.5 row 13, §2.5.1). Rule on 25 / 9.

---

## 0. What this document is

The two halves the `factory-retro` skill requires: **knowledge extraction** (§2–§5) and **process
telemetry** (§1). It differs from every prior retro in this repo in one respect — its Phase 2 output is
**files, not graph nodes**, because the pen is closed. §6 is therefore not a record of what was written;
it is a **proposal of what would be written**, held pending the owner's ruling.

Everything asserted here was re-derived from the artifacts or the git history. Where I could not verify
a claim, I say so rather than relaying it.

---

## 1. Process telemetry — **AVAILABLE**, and it printed this run's own defect

The skill warns that telemetry is degraded by factory enhancement **#24** ("No observation data").
**That symptom did not occur.** `context_cycle_review(feature_cycle:"wfh-011", format:"json",
auto_close:false, agent_id:"factory-retro")` returned a full report: 1 session, 822 records, 3 phases
(`tech-discovery` · `synthesis` · `close`), 8 hotspots, populated `phase_stats` with gate outcome text,
and `curation_health` within normal range. **#24 should not be assumed blocking on the strength of its
last observation.**

**What the telemetry says.**

| | |
|---|---|
| duration | 36 609 s (10.2 h), one session |
| `knowledge_entries_stored` | **0** — the zero-writes instruction is corroborated by the instrument, not only attested |
| `rework_session_count` / rework rate | 0 of 1 — **wrong**; the run ran a full rework round (`0421142`, `7a3704c`, `c9f8213`) |
| session gap | 7.3 h — the leader lost to the session rate limit, and the resume |
| `cold_restart_events` | 1 |
| baseline outlier | `agent_hotspot_count` 4 vs mean 1.0 — the only flagged outlier |
| `feature_knowledge_reuse` | 20 served, all cross-feature; **0 stored, 0 intra-cycle** |

**And the instrument contradicts itself inside one response, in the run's own defect shape.** This is
not a side note; it is the retro's own instance of the thing the run measured:

- `metrics.universal.total_tool_calls: 0`, while `session_summaries[0].tool_distribution` in the same
  payload sums to **743** (execute 596 · other 86 · read 45 · write 14 · search 2).
- `metrics.universal.coordinator_respawn_count: 0`, while the hotspot block in the same payload claims
  **11 coordinator respawns detected**, `measured: 11.0`, with nine timestamped clusters.
- `metrics.phases: {}` and `domain_metrics: {}` are empty while `phase_stats` carries three fully
  populated phases.
- The markdown tail prints **"Knowledge reuse: 20 of 1 (2000%)"** — a ratio over the session count.
- Worst: `baseline_comparison` scores `total_tool_calls` **"Normal"** against `mean: 0.0, stddev: 0.0`.
  The broken zero is being compared to a history of broken zeros and certified normal.

That last line is the same failure `OBS-19` recorded for `gate_result` and it is the more dangerous
form: **a derived view that is wrong is recoverable; a baseline that has normalised the wrong value
silently launders it.** Recorded as `OBS-23`.

**Qualitative (the skill's three questions).** What worked: §4. What wasted budget or chased a dead end:
nothing large — the 7.3 h gap was an external rate limit, not a dead end; the one genuine cost was that
round 2 was spent discharging four named items while the discovery curve was still rising (§3.2). What
surprised: that the run's instruments failed the exact predicate the run was testing, repeatedly, among
agents primed against it (§2) — and that the enumeration of those failures is itself unjoined (§2.2).

---

## 2. RULING — the goal-owner's disagreement

`reports/relevance.md` §3.1 / §8, relayed verbatim in the Issue close, names one disagreement with how
the packet disposes of its own material:

> the label-versus-value occurrences are **a base rate, not carelessness**; they are the strongest
> evidence the `workflow-harness` theme holds; they **should reach the owner as theme evidence, not be
> filed to the retro as a note about agent sloppiness.**

**Ruling: UPHELD on substance. Two corrections. One refusal. Both destinations, neither substituting
for the other.**

### 2.1 Upheld — this is subject data, not process data

Three grounds, each independently sufficient.

**(a) It is mis-planed as a lesson.** The `factory-retro` plane test is *"if the research target were
different, would this still be useful?"* → yes ⇒ research-plane lesson. That test is the wrong
instrument here, because it is applied to material that is not about the research *process* at all. The
theme's central claim is a claim about **a class of control**: *a control whose input sits inside the
governed party is a label, not a control* (`#320`). This run produced first-party, command-recorded
instances of that exact class failing. Instances of the phenomenon under study are **evidence about the
subject**. Filing them as process hygiene puts the theme's own data in the wrong plane.

**(b) Its epistemic standing is higher than either case history's.** Both instantiated cases are
*reconstructed* from committed records. These occurrences were *observed as they happened*, with the
correcting commands recorded (`dcdf408` and `f36f716` are two retraction commits on one workstream in
one afternoon). W4 §9.1 states this itself — *"a stronger data point about the predicate than either
case history supplies, because it was observed rather than reconstructed"* — and then routes it to the
retro anyway. **W4's routing was correct for the ledger and does not license the inference that the
retro is the terminal destination.** Keeping a run-level observation out of a case-coverage ledger and
keeping it out of the theme's evidence are two different decisions; only the first was actually made.

**(c) Calling it carelessness would be the theme's own failure mode, applied to itself.** "Agent
sloppiness" is a label. The value under it is a specific, reproducible defect shape with an identical
repair. Accepting the label in place of the value is precisely what the run kept catching itself doing.

### 2.2 Correction 1 — "eight" is itself an unjoined label, and I am not passing the number forward

I did not adopt the enumeration. Checking it against the corpus produced the sharpest single result of
this retrospective: **three separate enumerations of this defect class exist in the run's own record,
and no two of them agree.**

| source | count | membership |
|---|---:|---|
| `findings-W4-adjudication.md` §9.1 | **3** | leader's first characterisation · W1's first correction · leader's second message |
| `reports/relevance.md` §3.1 | **8** | dual-validator vacuous pass · coverage table never opening its instance · reconciler on the disposition column · `north_star` key-presence · W1's `origin` claim from a local mirror · the leader repeating it twice · W1's ledger paragraph + a reviewer reading a mutable working tree · round-2's `Capability.versioned` + §13.3 arithmetic |
| the close relay / synthesis | **8** — *different eight* | adds: W4's findings file transcribed through the leader with no original to diff · W2's 55-inverse-error narrative decomposition · the 34 boilerplate-witness inverse rows. drops: the leader's repeat · the W1 ledger paragraph · `Capability.versioned` |

The two eights share five members. **Their union is at least eleven distinct occurrences**, and no
register anywhere in the run enumerates them, so no reader can join the scalar to the instances. Part of
the divergence has an innocent cause — `relevance.md` was written before `REPORT.md` existed and says so
at its head, so the curator's three synthesis-found inconsistencies were not available to it. That
explains *why* the lists differ. It does not explain why both printed the same number.

**Both parties printed "eight." Neither derived it.** The count is a label asserted over an unmaintained
set — the twelfth instance, occurring inside the sentence that reports the rate.

This does not weaken the goal-owner's case; it strengthens it. The recurrence reproduced one altitude
further up, unprompted, in the act of reporting it. But **the scalar must not travel.** What travels is
the register (§2.5), joined to artifacts.

### 2.3 Correction 2 — "base rate" is the right instinct and the wrong word

A base rate requires a denominator. **There is none.** Nobody counted the checks that joined correctly,
and no instrument in the run could have.

I verified one datum that both settles the carelessness question and shows why the denominator is large
and uncounted. In `artifacts/wfh-008-coverage-gen.py`, inside one function, nineteen lines apart:

```python
# line 348 — fields branch: KEY PRESENCE
hits = [r['id'] for r in insts if fname in (r.get('fields') or {})]
# line 367 — relations branch: POPULATION
hits = [r['id'] for r in insts if (r.get('relations') or {}).get(rname)]
```

Same author, same loop, both forms. **The agent knew how to write the join; it wrote it nineteen lines
away.** That refutes the carelessness hypothesis at zero cost — this is not a skill gap — and it shows
the correct form is the common case, uncounted.

So the defensible claim is **not** "the base rate is 8 in N." It is:

> **The defect recurs under priming, in both directions, inside single functions where the correct form
> is adjacent.** A *recurrence* claim, which is what the theme actually needs, and which requires no
> denominator.

Stated as a base rate, the first reviewer who asks "out of how many?" collapses it. Stated as recurrence
under adjacency and priming, it survives, and it is the stronger claim anyway.

### 2.4 Refusal — I will not route it, because routing it is a graph write nobody has authorised

The goal-owner's destination — *"reach the owner as theme evidence"* — resolves, under this repo's own
conventions, to a **research-plane `finding` on the `workflow-harness` theme**. That is exactly the
write the owner's zero-writes instruction forecloses, and `relevance.md` §7 flags it as an owner
decision while explicitly not authorising it.

**So I do the only thing my pen permits: I file it in both places, and let neither substitute for the
other.** The register goes here, artifact-verified and joinable (§2.5). The graph candidate goes to §6
as a **`finding`**, not a `lesson-learned`, for the owner to approve or refuse. What I refuse is the
framing under which the retro is where this material *dies*. It is where it is *held*.

### 2.5 The register — what should travel instead of the scalar

Fifteen distinct occurrences, enumerated and joined to artifacts. **Thirteen predate this
retrospective; two were produced by the retrospective itself, one of them by me.** Verification status
is per-row: `VERIFIED` means I or a verification agent recomputed it at the artifact this session.

| # | occurrence | status |
|---:|---|---|
| 1 | **Two validators pass green on `vnc-045-instance.yaml` parsing zero objects.** The pair is `v5_instance_check.py` and `wfh-008-validate.py` — *not* `vnc-045-validate.py`, which is the RW-2 remediation and is not vacuous. Both key on a top-level `instances:` map (`v5_instance_check.py:133`, `wfh-008-validate.py:160`); `vnc-045-instance.yaml` has no such key, using section names (`scopes:`, `goals:`, …). | **VERIFIED** — re-executed: `0 instance objects across 0 constructs` · `I13 … PASS (vacuous: 0 Capability instances)` · `RESULT: 0 error(s)` · `EXIT=0`. Parse counts measured: `wfh-008-instance.yaml` 191, `w3-baseline-instance.yaml` 37, `vnc-045-instance.yaml` **0**. |
| 2 | **`vnc-045-coverage-build.py` never opened its own instance.** 679 rows, 596 `exercised`, 346 of those carrying `see instance`. | **VERIFIED** at `536103c`: the script does not `import yaml`, and the only occurrence of the string `vnc-045-instance.yaml` in 97 KB is inside the boilerplate it emits (`value_or_witness="instantiated in vnc-045-instance.yaml"`). Post-RW-1 it imports `yaml` and its own log reports 119 checkable rows, 7 FAIL, 69 witness strings replaced as false-as-written. |
| 3 | **W4's reconciler applied its rule to the `disposition` column, never the `value` column.** | Recorded; discharged as RW-3. |
| 4 | **W1's generator counts key presence, not value population.** | **VERIFIED** — `wfh-008-coverage-gen.py:348` `if fname in (r.get('fields') or {})` versus `:367` `if (r.get('relations') or {}).get(rname)`, nineteen lines apart in one function. Blast radius exactly 4 coverage rows; on `north_star` and `claim_floor` the overstatement is total (claimed 2/2, actual 0/2). |
| 5 | **W1 asserted a fact about `origin` from a local mirror of it** (`git branch -a --contains` is not evidence about a remote). | **VERIFIED** — two retraction commits, `dcdf408` and `f36f716`. |
| 6 | **The leader made the same class of claim twice in successive messages and withdrew both.** | Recorded (`relevance.md` §3.1). |
| 7 | **W1 updated a ledger without re-reading the paragraph three lines above that counts its rows; the reviewer who caught it was reading a mutable working tree and reported it as committed state.** Two agents, one file, one error. | Recorded (`relevance.md` §3.1). |
| 8 | **`core.Capability.versioned` reconciled `exercised` with zero instance witness in either case.** | Recorded as round 2's `N5`. |
| 9 | **W4 §13.3's disclosed scoping counts do not reproduce** — 274/269 authored; auditor and curator independently both measure 268/278. Inside the one paragraph whose purpose is disclosing what the guard did not cover. | Recorded as `N6`; two independent reproductions agree against the authored pair. |
| 10 | **W4's findings file was transcribed through the leader with no original to diff.** | **NOT VERIFIABLE** — see §8. Two commits exist and no prior original, which is consistent with the claim and is also what makes it unfalsifiable. Not asserted. |
| 11 | **W2's narrative decomposition of its own 55 inverse errors misattributes the groups.** Prose names 19 + 18 + 3 = 40 of 55 and never mentions an 11-error group. | **VERIFIED** — measured from the 55 `ERROR INVERSE` lines: `Attempt.governed_by↔Delegation.governs` 19 · `Delegation.unit↔Unit.assigned_through` **11 (unmentioned)** · `Attempt.unit↔Unit.attempts` 8 · `Unit.gated_by↔Gate.evaluates` 6 · `Record.documents↔Event.documented_by` 5 · `Unit.directed_by↔Goal.directs` 2 · `Workflow.binds↔Gate.bound_by` 2 · `Capability.required_by↔Goal.requires` 1 · `Delegation.enforced_by↔EffectBoundary.enforces` 1 = **55**. The prose transposes the 19 onto the wrong relation and undercounts `gated_by↔evaluates` 3→6. **The log is correct** and reproduces byte-identically (sha256 `8fee6015…3ddcaeb2`, fresh versus committed). The round-1 auditor verified the log without checking the prose against it. |
| 12 | **All 34 declared-inverse rows in `vnc-045-coverage.csv` carry one identical boilerplate witness, so none was ever joined.** | **VERIFIED** — across all 34 rows: `value_or_witness` 1 distinct value (`instantiated in vnc-045-instance.yaml`), `provenance` 1 (`see instance`), `custody` 1, `applicable_checks` 1 (`not-applicable`), `disposition` 1 (`exercised`). Only `instance_ref` varies. RW-1's rebuild joined 119 field/relation rows and excluded these 34 from the join. |
| 13 | **NEW — the *correction* to #12 is itself unjoined, and it is a live owner escalation.** The Issue's escalation 1 reports the sharper measurement as **22 true by accident / 12 false**. That split comes from `w4-witness.py`, whose `entry_id()` (lines 57–61) searches `('id','ref','target','to')`, **omits `actor`, and returns `None` silently**. `vnc-045-instance.yaml` writes attributed relations keyed on `actor:`. | **VERIFIED three ways.** (a) 28 attributed entries in the instance are invisible to `entry_id()`, 21 of them keyed on `actor`. (b) `w4-witness.json`'s `w2` block carries **22** inverse keys and the three attributed relations are **absent**, not zero. (c) Direct recomputation with an actor-aware reader: `has_skill↔held_by` closes **5/5**; `assigned_to↔holds_role` closes **16/16**; the same computation with `entry_id()`'s key list scores **0**. **Corrected split: 25 true / 9 false, not 22 / 12.** See §2.5.1. |
| 14 | **NEW — mine.** Dispatching the verification of #2 I bound "W2's coverage table" to `artifacts/wfh-008-coverage.csv`. W2 is the *software* case (`vnc-045`); `wfh-008` is W1's *research* case. I took the label and bound it to the wrong value — in a prompt whose entire purpose was catching that. The agent refused the framing and went to the right file, which is why the row above is right. | **VERIFIED** — `wfh-008-coverage.csv` is 468 rows / 339 `exercised`; the 596/346 figures belong to `vnc-045-coverage.csv` at `536103c`. |
| 15 | **The count itself.** Three enumerations of this class exist (3, 8, and a different 8); no register is maintained; two parties printed the same number without deriving it. §2.2. | **VERIFIED** — this table is the first register. |

#### 2.5.1 Row 13 is not a retro curiosity — it changes a number now sitting with the owner

Issue #70's escalation 1 asks the owner to rule on twelve inverse rows and states the curator's sharper
measurement as *"all 34 … 22 are true by accident, 12 are false."* **That is wrong by three.** At least
three of the twelve — `core.Actor.relations.has_skill`, `supporting.Skill.relations.held_by`,
`supporting.Role.relations.assigned_to` — do close, 5/5 and 16/16 respectively. The correct split is
**25 true / 9 false.**

The cause is worth stating precisely, because it is the run's own subject in its purest form and the
contrast is inside one run's artifacts:

| reader | key list | behaviour on an unrecognised map |
|---|---|---|
| `vnc-045-validate.py :: rel_target` (lines 184–198) | `('actor','target','ref','id')` | calls `accom()` to **disclose** the accommodation, and `err()` if no target key is found — **fail-loud** |
| `w4-witness.py :: entry_id` (lines 57–61) | `('id','ref','target','to')` | `return None` — **fail-silent** |

Two readers of the same file, in the same run, by the same lineage. One discloses what it could not read
and errors; the other returns `None` and its caller records the relation as unwitnessed. **The
instrument built to catch label-over-value produced a label over value**, and the number it produced was
escalated to the owner as the corrective. This is the strongest single instance in the register and it
was not in anyone's list of eight.

**Action:** the owner's escalation-1 ruling should be taken on **25 / 9**, not 22 / 12. The direction
matters — the corrected figure is *less* adverse to the software case than the escalated one, so the
error was running against the run's own interest, not for it.

### 2.6 What I part company with the goal-owner on — there are two findings here, not one

The goal-owner asks that this not be filed as a note about agent sloppiness. Agreed. But its framing
implies the retro is the wrong destination *per se*, and that loses a second finding in the same
material that is genuinely process-shaped and belongs here:

> **Every one of these was caught by an independent second look, and not one by the party that made
> it.** Round 1's audit caught W2's table. Round 2's re-audit caught the 33 further zero-witness rows,
> `Capability.versioned`, and the twelve inverse rows. W4 caught W1's generator — on its own case's
> side, which the audit had credited as sound. The curator caught W2's narrative decomposition and
> W4's §13.3 arithmetic in synthesis. The leader caught its own claim only on re-execution.

That is a claim about the run's machinery rather than about the theme, and it is the reason the packet
is trustworthy at all. Both readings are true. The goal-owner asked for one; I am recording two.

**Ruling, in one line:** the material is theme evidence and should reach the owner as such — as an
enumerated register, as a *recurrence* claim rather than a base rate, and by a graph write the owner
must authorise, which I am flagging and not resolving.

---

## 3. What the run's process cost, and what the method does not say

### 3.1 Two gate rules were invented under pressure — both correct, both self-issued, neither written down

**(a) "A terminated auditor issued no ruling and therefore consumed no rework round."** The independent
re-audit died mid-execution on a session rate limit (HTTP 429, `req_011CeWNjUEishDUt2KZDikYW`).
`reports/gate-coverage-r2.md` was verified absent; no partial report existed. The leader asserted, in an
Issue comment in the moment: *"A terminated auditor issues no verdict, so the round is not consumed."*
That preserved round 2, and it is right.

**I checked whether it is written anywhere.** Grepped `docs/research-factory-methodology.md`,
`product/factory/runbook.md`, `product/factory/decisions.md`, `.claude/workflow/`, `.claude/rules/`,
`.claude/skills/`, `.claude/agents/`. **It is not.** The only adjacent text is methodology §14.6 —
*"rework capped at 2 per gate"* — one clause, under the heading **Context protection**.

**(b) The terminal auditor invented a third exit the SCOPE does not give it.** `SCOPE.md` lines 258–260
allow exactly two: *"`REWORKABLE` permits at most two targeted rounds; any unreconciled X row … after
round two is `SCOPE-FAIL`."* Round 2 found `N4` — twelve `*-relation-inverse` rows reconciled
`exercised` on a boilerplate witness while closing zero edges in the instance. That is literally an
unreconciled X row after round two, i.e. the `SCOPE-FAIL` trigger. The auditor instead ruled `PASS` and
**referred that single question to the owner**, stating in the close that withholding the `PASS` would
have been a legitimate alternative. That was the right call. Nothing in the method authorises it,
nothing requires it, and the next auditor under the same pressure has no reason to reach for it.

**The pattern, which is the finding:** *under time pressure the gate machinery generated its own
governing rules, and in both cases the party that benefited from the rule is the party that wrote it.*
Both happened to be right. The exposure is that neither is checkable and neither will recur reliably.
**This is the factory-plane instance of the theme's own predicate**, and it is this retro's sharpest
process result. → `OBS-21`; ADR candidate at §6.

### 3.2 The discovery curve never flattened, and the cap's rationale has come apart from its reading

- Round 1: **6** zero-witness rows.
- Round 2: **33 more** beyond those six (24 of which had to leave `exercised`), **plus two new classes**
  (`N4`, `N5`) round 1 never reached.
- The rework stopped on the SCOPE's two-round cap. **Not on exhaustion.** The `PASS` says four named
  items discharged; it does not say the class is closed, and `gate-coverage-r2.md` §4 does not claim it
  does.

Each independent look found more than the last. Meanwhile the cap is *written* as budget (§14.6,
"Context protection") and *read* as sufficiency ("`PASS` at round 2 of 2").

**Is a fixed rework cap the right instrument on a rising curve?** My answer: **the cap is fine; the
ruling is under-specified.** Raising the cap trades a known budget for an unknown one and still ends on
an arbitrary number — you would simply discover a rising curve at round 4. A cap that stops on budget is
honest. A `PASS` that cannot be distinguished from exhaustion is not.

**Proposed alternative — cheap, and it is a method change I am proposing, not making (§7):**

1. Require the **terminal** gate report to carry a computed **discovery-curve line**: defects found this
   round · defects found the prior round · new defect classes opened this round. One line, mechanical.
2. Qualify the ruling word: **`PASS (budget-terminal — curve rising)`** vs **`PASS (curve flat)`**.

Cost: one computed line per terminal gate. It converts an unbounded residual from something a
conscientious auditor *may* disclose in prose into something the ruling word **cannot omit**. The
current run disclosed it well; the next one is not obliged to.

### 3.3 Deferred and unrun — recorded so it is not lost

**W3's rejection suite was never run against the two counterfactual evolved forms.** The
anti-force-fitting amendment permitted it and did not require it. W4 §9 records the gap and explains why
it is not W3's fault: W1's instance was absent for W3's entire run, and W3 derived its baseline from M01
alone precisely to protect its independence from the case matrices — which is the reason the divergence
analysis means anything.

The sharpest untested target is named by the run itself: **W2/CF-05's own recorded residual —
*a required check whose predicate is "a file exists" is satisfiable by writing a file*** — is exactly the
shape W3's suite falsifies, and it was not falsified. Note what that residual is: **the same
label-versus-value defect a further time, at the design altitude.** A check whose predicate names the
artifact's existence rather than its content is a label check.

Carried as an architect-for-future item. Not worth a run on its own; it should ride the next
instantiation scope.

---

## 4. What worked — and the mechanism, named

Four behaviours are worth keeping, and they have **one mechanism** between them:

- 69 conformance errors published rather than the instance repaired to clear its gate;
- both instance digests byte-identical before and after the rework;
- all 30 reconciled-disposition changes moved *away* from `exercised`, none toward it;
- W4 self-reported the same defect class on W1's side — its own case's side, which the audit had
  credited as sound — unprompted.

**The mechanism: the cheap escape was closed by scope *before* anyone was asked to resist it, and the
direction of change was made measurable *after*. It is structural, not virtuous — and that is the
reusable part.**

Three components, all present, all portable:

1. **The artifact under test was digest-pinned and placed out of scope of the rework.** Round 1 §4 set
   the boundary explicitly ("no re-encoding of either case instance"). So when the corrected validator
   emitted 69 errors against `vnc-045-instance.yaml`, the only lever the rework had was the
   **instrument**. The run's own phrase for it, and it should become vocabulary:
   > **"The reader was fixed to the data; the data was not fixed to the reader."**
2. **The rework items were named narrowly (RW-1…RW-4) and the workstream refused to exceed them** — and
   said so. That refusal is why `N4` surfaced as a disclosed, unrepaired measurement rather than being
   quietly swept into a wider fix.
3. **The auditor measured the sign of the diff, not the story about it.** `gate-coverage-r2.md` §0
   re-derived every digest before reading anything about them and re-executed every checker rather than
   reading its log; §2 then computed the direction of every changed cell.

**I reproduced §2 independently** from git (`7a3704c` → `c9f8213`, `reports/construct-pressure-ledger.csv`):
705 rows in, 705 out; **30** `reconciled_disposition` changes; **9** `exercised`→`construct-pressure`,
**21** `exercised`→`not-applicable`, **0** toward `exercised`; model-X `exercised` **552 → 522** exactly.

**The generalisation, and the enhancement worth building:**

> **A rework round cannot be trusted on its report. It can be trusted on the sign of its own diff.**
> "Did claimed coverage go up or down?" is a one-line computation that no amount of authored narrative
> can fake, and it is the cheapest integrity instrument this run produced.

**And the reflexive point, which is worth more than either half.** The run behaved well exactly where
the control sat **outside** the governed party — the scope pinned the artifact; the auditor computed the
sign. It failed, fifteen times, exactly where the control sat **inside** the party — an agent
checking its own coverage claim. **The run is a positive and a negative instance of one law**, and the
pair is stronger evidence for the theme than the failures alone. §2 routes the failures; this routes the
positive with them.

Also worth keeping, from `REPORT.md` §2.5 — **the report records what the model does well** ("a report
that lists only defects is not adjudicating"). That is a norm, not a nicety, and this retro follows it.

---

## 5. Factory board — no grade movement is warranted, and the reason is the firewall on ourselves

Phase 2.4 of the skill asks whether the run moved a factory capability. **No — and not merely because
the pen is closed.**

The run was autonomous within its envelope and produced real artifacts, which would normally argue for
`partial` on the coverage-gate machinery. It argues the other way here: **the run's own coverage
instruments failed the exact class of check that capability exists to perform**, fifteen times, and
the terminal `PASS` was issued on a rising discovery curve. Evidence that an instrument is defective is
not evidence for advancing the capability that instrument implements.

Both the round-1 and round-2 auditors recommended grade movement **NONE**; none was made; and I concur
on the merits independently of the write restriction. **Nothing in `wfh-011` reaches `partial`, and
nothing comes near `proven`.**

---

## 6. What I would write to Unimatrix, pending owner approval

**NOT WRITTEN. NOTHING BELOW EXISTS IN THE GRAPH.** This is a proposal for the owner to approve or
refuse as a separate act. Every entry would be tagged `wfh-011`; research-plane entries additionally
`theme:workflow-harness`. `agent_id` on every write below is **`factory-curator`** — the repository's
single writer — not `factory-retro`; this retro would hand the list over, not write it.

Six entries. I have kept it short on purpose: the skill's bar is that more entries is not better.

### R1 — research plane · `finding` · the theme evidence (§2)

| | |
|---|---|
| **plane / category** | research · `finding` |
| **grade / status** | n/a — `finding` carries no `grade:` tag; graded material is `capability`/`technology` |
| **title** | Label-versus-value: ≥15 first-party recurrences among primed agents in one run, with one identical repair |
| **content** | The **fifteen-row register at §2.5**, per-row verification status included — the artifact-joined form of what the goal-owner asked to route. Plus the divergent-enumeration result (§2.2), the recurrence framing (§2.3 — **not** a base rate; no denominator exists), the adjacency datum (`wfh-008-coverage-gen.py` line 348 vs line 367, same function, both forms, nineteen lines apart), the fail-loud/fail-silent reader contrast (§2.5.1), and the sign result (every repair *reduced* claimed coverage: 30 changes, 0 toward `exercised`). Explicitly carries §2.6's second finding: every occurrence was caught by an independent second look, none by the party that made it. |
| **edges** | `Motivates →` a `technology` node for the theme's control-custody candidate **if and only if one already exists** — curator self-briefs first (`context_search(category:"technology")`) and adds no new technology node to hang an edge on. Otherwise **no edge.** |
| **`cites:`** | `{type: docs, ref: "product/research/wfh-011/RETRO.md", title: "wfh-011 retrospective §2 — the label-versus-value register and the ruling on its routing", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "product/research/wfh-011/reports/relevance.md", title: "wfh-011 goal-owner relevance review §3.1 — eight occurrences, one shape", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "product/research/wfh-011/findings-W4-adjudication.md", title: "wfh-011 W4 §9.1 — the run-level observation kept out of the ledger", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "product/research/wfh-011/reports/gate-coverage-r2.md", title: "wfh-011 coverage gate round 2 — N1..N6, newly-visible versus rework-introduced", org: "arch-research garage", year: 2026}` |
| **note** | **This is the goal-owner's disagreement, resolved into a concrete write.** It is a `finding`, not a `lesson-learned`, because it is evidence about the subject. Approving it is the act that answers `relevance.md` §7. |

### R2 — research plane · `lesson-learned` · the research-process half (§2.5)

| | |
|---|---|
| **plane / category** | research · `lesson-learned` |
| **title** | Independent re-look is the only mechanism that found anything in wfh-011 — the author's own second pass found nothing |
| **content** | The catch-attribution table from §2.5, plus §4's mechanism: the independent look works because the artifact under test is pinned out of the reworker's scope and the sign of the diff is computed by someone else. Passes the plane test — true if the research target were different. |
| **edges** | none |
| **`cites:`** | `{type: docs, ref: "product/research/wfh-011/RETRO.md", title: "wfh-011 retrospective §2.5, §4", org: "arch-research garage", year: 2026}` |

### R3 — factory plane · enhancement · sign-of-diff integrity check (§4)

| | |
|---|---|
| **plane / category** | `factory`, `kind: technology` |
| **grade** | **`claimed`** — asserted, not A/B-proven. Phase 3 keeps it there until comparative telemetry moves it. |
| **title** | Sign-of-diff integrity check: a rework round is trusted on the direction of its own diff, never on its report |
| **content** | Require every re-audit gate report to carry a computed block: rows in / rows out / added / removed; cells changed by column; and the **direction** of every disposition change. A rework that cleared its gate by inflating coverage shows the opposite sign. Worked example and reproduction: §4. |
| **edges** | `Prerequisite →` the `factory` capability covering the coverage gate — **only if one exists**; curator resolves by `context_search`/`context_lookup` first and asserts no edge rather than minting a target. `factory → factory` only. |
| **`cites:`** | `{type: docs, ref: "product/research/wfh-011/reports/gate-coverage-r2.md", title: "wfh-011 coverage gate round 2 §2 — cell-level footprint and the measured direction", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "product/research/wfh-011/RETRO.md", title: "wfh-011 retrospective §4 — independently reproduced 552→522", org: "arch-research garage", year: 2026}` |

### R4 — factory plane · enhancement · discovery-curve disclosure on a terminal ruling (§3.2)

| | |
|---|---|
| **plane / category** | `factory`, `kind: technology` |
| **grade** | **`claimed`** |
| **title** | A terminal gate ruling must state its discovery curve — `PASS (budget-terminal, curve rising)` is not `PASS (curve flat)` |
| **content** | The §3.2 proposal: a computed defects-this-round / defects-prior-round / new-classes line on every terminal gate report, and a qualified ruling word. Evidence: 6 → 33 + 2 new classes across two rounds, stopped by cap not exhaustion. |
| **edges** | as R3 — `Prerequisite →` the coverage-gate factory capability if one exists; otherwise none |
| **`cites:`** | `{type: docs, ref: "product/research/wfh-011/reports/gate-coverage.md", title: "wfh-011 coverage gate round 1 — REWORKABLE, six zero-witness rows", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "product/research/wfh-011/reports/gate-coverage-r2.md", title: "wfh-011 coverage gate round 2 — 33 further rows, classes N4 and N5", org: "arch-research garage", year: 2026}` |

### R5 — factory plane · ADR candidate · a rule invented by the party it governs is not a rule (§3.1)

| | |
|---|---|
| **plane / category** | `factory`, `kind: finding`, **tagged `position`** |
| **title** | Gate rules must pre-exist the gate: wfh-011 needed two, invented both mid-run, and in both cases the beneficiary wrote the rule |
| **content** | The §3.1 pair — (a) a terminated auditor consumes no rework round; (b) a terminal auditor may rule `PASS` with an explicit referral rather than being forced to `SCOPE-FAIL`. Both correct, both unwritten, both self-issued. The position: write both into the method so the next run does not reinvent them under pressure, and record that self-issuance is the exposure, not the rulings. |
| **edges** | none — this is a position, and `Cites` edges are forbidden |
| **`cites:`** | `{type: repo, ref: "https://github.com/dug-21/arch-research/issues/70", title: "Issue #70 — the terminated re-audit, the rate limit, and the round-budget assertion", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "product/factory/decisions.md", title: "Factory decisions log — the surface this position proposes to extend (D17 candidate)", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "docs/research-factory-methodology.md", title: "Research factory methodology §14.6 — rework capped at 2 per gate, stated as context protection", org: "arch-research garage", year: 2026}` |

### R6 — factory plane · observation · telemetry contradicts itself and the baseline launders it (§1)

| | |
|---|---|
| **plane / category** | `factory`, `kind: technology` |
| **grade** | **`claimed`** |
| **title** | `context_cycle_review` disagrees with itself inside one response, and `baseline_comparison` certifies the broken value as Normal |
| **content** | §1's five contradictions, with the sharpest being `total_tool_calls: 0` scored `Normal` against `mean 0.0, stddev 0.0`. Sharper and more dangerous than `OBS-19`/`OBS-17`: a wrong derived view is recoverable, a baseline that has absorbed the wrong value is not. Also records that **#24's "No observation data" symptom did not occur** — do not assume #24 blocking without re-testing. |
| **edges** | `Prerequisite →` the existing factory telemetry capability if one exists (the `OBS-17`/`OBS-19`/#24/#65 lineage); curator resolves the live id via `context_graph(mode:"current")` before asserting anything |
| **`cites:`** | `{type: docs, ref: "product/factory/observations.md", title: "Factory observations OBS-17 / OBS-19 / OBS-23 — the telemetry lineage this extends", org: "arch-research garage", year: 2026}` · `{type: docs, ref: "product/research/wfh-011/RETRO.md", title: "wfh-011 retrospective §1 — the cycle-review payload and its internal contradictions", org: "arch-research garage", year: 2026}` |

### Deliberately NOT proposed

- **No `technology` node for V5 or any successor.** No candidate technology was evaluated; V5 is a
  proposal under test, and the run authored no successor. A node here would be structure minted from a
  verdict.
- **No `capability` or `nfr` writes, and no grade movement of any kind.** §5.
- **No `position` finding ratifying `revise`.** The goal-owner is right that the verdict word carries
  almost no information and was near-certain before the run began. Storing it would file a foregone
  conclusion as a decision.
- **No `Cites` or `Tests` edges** anywhere above (D8). Sources stay `cites:` fields; artifacts never
  become nodes.

### One open question the owner must settle before any of this is written

`relevance.md` §7 records that **the theme's V5 track has produced zero graph nodes across two runs**
(`wfh-010`, `wfh-011`), correctly, under scopes that forbid writes — while `CLAUDE.md` names the KB as
the compounding asset. **Approving R1–R6 is the narrow version of that decision; it is not the whole
of it.** Whether the two runs' substantive yield (the typed-reference law; zero enforced authority in
two owner-operated histories) enters the graph is a larger, separate ruling I am flagging and not
resolving.

---

## 7. Method changes implied — proposed, not made

Per the run instruction, a method change carries a `wf:` bump and is the owner's call. **I have made
none.** Three are implied:

| # | surface | change | source |
|---|---|---|---|
| M1 | `docs/research-factory-methodology.md` §14.6 and/or `product/factory/decisions.md` (a **D17**) | Write down the two gate rules this run invented: a terminated auditor consumes no rework round; a terminal auditor may rule `PASS` with explicit referral of a named question rather than being forced to `SCOPE-FAIL`. | §3.1 |
| M2 | the coverage-gate contract (`.claude/agents/factory/factory-validator.md`, gate report template) | Require the discovery-curve line and the qualified terminal ruling word. | §3.2 |
| M3 | the same contract | Require the sign-of-diff block on any re-audit of a rework. | §4 |

M1 is the one I would do first: it is the cheapest, and it removes the need for a future agent to
invent a rule in favour of itself under a rate limit.

**Files written by this retro:** `product/research/wfh-011/RETRO.md` (this file) and three appended
entries in `product/factory/observations.md` (`OBS-21`, `OBS-22`, `OBS-23`). No method file was edited;
no `wf:` tag was cut.

---

## 8. Verification note

Claims in this document were re-derived rather than relayed. What I checked myself or had independently
recomputed at the artifacts, and what I could not:

**Verified** (see §2.5 for per-row detail). The 30 disposition changes and their direction (recomputed
from git `7a3704c`→`c9f8213`: 705/705 rows, 9 + 21, 552→522 model-X). The two vacuous validators, by
re-execution, with measured parse counts 191 / 37 / **0**. The pre-rebuild `vnc-045-coverage-build.py`
having no `yaml` import at `536103c`. The `north_star` key-presence defect and the adjacent population
check nineteen lines away in the same function. W2's 55-inverse-error decomposition (prose sums to 40 of
55; measured 19/11/8/6/5/2/2/1/1 = 55; log correct and byte-identical, sha256 `8fee6015…3ddcaeb2`). The
34 identical boilerplate witnesses. **The `w4-witness.py` reader bug and the corrected 25/9 split** —
confirmed by the reader's key list, by the three relations being absent rather than zero in
`w4-witness.json`, and by direct recomputation (5/5 and 16/16 closing where the run's reader scored 0).
The three divergent enumerations and the ≥15 union. The absence of the terminated-auditor rule from
every method surface. The SCOPE's two-exit terminal cap at lines 258–260. Round 1's six versus round 2's
thirty-three plus two new classes. The telemetry payload's internal contradictions.

**Corrected while verifying.** The relayed defect list names four items whose stated detail did not
survive checking: the vacuous pair is `v5_instance_check.py` + `wfh-008-validate.py`, not
`vnc-045-validate.py`; the 596/346 figures belong to `vnc-045-coverage.csv` at `536103c`, and I
compounded that by dispatching the check against `wfh-008-coverage.csv` (§2.5 row 14); the escalated
22/12 inverse split is 25/9 (§2.5.1). **None of these corrections weakens the underlying claims — every
one of the four is confirmed in substance and wrong in a stated value.** That is itself the pattern.

**Not verifiable from committed artifacts.** *"W4's findings file was transcribed through the leader
with no original to diff."* `findings-W4-adjudication.md` has exactly two commits (`fd7ab89`, `c9f8213`)
and no prior original exists to compare against — which is consistent with the claim and is also exactly
what makes it unfalsifiable. It is structurally consistent with the standing `OBS-2` / `OBS-7` hazard
(subagent file-writes blocked; the leader persists the text), but **no evidence trail establishes it and
I am not asserting it as verified.** Saying so is the point.
