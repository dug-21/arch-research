# mnstd-002: Retrospective

**Role:** `factory-retro` · **Run:** `mnstd-002` (validated research-scope with feasibility) · goal `mnstd` #329 · [Issue #74](https://github.com/dug-21/arch-research/issues/74) · [PR #75](https://github.com/dug-21/arch-research/pull/75)
**Run method stamp:** `wf-v0.26-50-gecac38f` (matches `git describe --tags ecac38f`; correct) · **Repo state at retro:** `main` at `b69e32c` (`wf-v0.26-67-gb69e32c`)
**Outcome under retro:** 14 of 15 board nodes `proven`, C6 #371 `partial` (ISO HTML has no native review notes).
Techs #379–#382 `proven`, #383 `partial`, #354 `claimed`. Position #384. Builds on the mnstd-001 retro
(`product/research/mnstd-001/RETRO.md`) and does not repeat its entries. Where a point recurs, it is cited by
number (OBS-24/25/26 and §7.x there).

---

## 1. Process telemetry: **AVAILABLE**

`context_cycle_review(feature_cycle:"mnstd-002", auto_close:true, format:"json", agent_id:"factory-retro")`
returned a full report: 1 session, 748 records, attributed 1/1, `is_in_progress: false`.

| | |
|---|---|
| wall time | 11 961 s (3 h 19 m). scope 200 s · tech-discovery 1 532 s · **feasibility 9 893 s (83 %)** · synthesis 333 s · unnamed tail 3 s |
| spawns | 14: factory-researcher ×6, factory-poc, factory-validator ×3, factory-curator ×3, goal-owner. `coordinator_respawn_count 0` |
| knowledge yield (run-tag lookup, authoritative) | 31 active nodes tagged `mnstd-002`: 6 tech, 10 finding (incl. position #384), 15 capability (re-tagged by the grade corrections). New stores 16 (#349–#363, #384) plus 20 `context_correct` grade moves |
| firewall ratio (tech) | 4 proven · 1 partial · 1 claimed of 6. Capabilities 14 proven · 1 partial. Lessons from the run itself: 0 (two added by this retro) |
| gates | coverage PASS first time. Firewall: **SCOPE FAIL → owner rulings → rework 1 → spot-check PASS** (`gate_result: rework`) |
| hotspots | `tool_failure_hotspot` Bash ×20 (14 in the poc worktree, mostly probe/dev compiles: Warning) · `sleep_workarounds` 3 · `file_breadth` 60 · `mutation_spread` 57 · `bash_for_search_count` 221 (**Outlier** vs mean 39) |
| context before first write | 104 KB (baseline mean 598 KB) |

**Instrument notes.** These are new or changed since mnstd-001. OBS-24 itself is not restated.

- **Improved:** `agents_spawned` now lists every specialist, including the researchers mnstd-001's payload omitted.
  `feature_knowledge_reuse.total_stored: 16` equals the real new-store count.
- **Recurs (OBS-24, n=2):** `metrics.universal.knowledge_entries_stored: 0` and `total_tool_calls: 0` sit beside
  `session_summaries[0].knowledge_stored: 18` and a tool distribution summing to 701. All are scored `Normal`.
- **New, cross-cycle mis-binning:** `knowledge_stored: 18` = 16 mnstd-002 stores **+ #347 and #348**, which were
  written by the *mnstd-001 retro*. That retro ran in this same session during mnstd-002's scope phase (the
  `mutation_spread` evidence shows `mnstd-001/RETRO.md` written at 1794588622). `phase_stats[scope].knowledge_stored: 2`
  is therefore the other cycle's yield. `knowledge_curated: 21` = 20 grade corrections + #346 (also mnstd-001's).
  Attribution is by session time window, not by `feature_cycle`. This is direct evidence for #302 (cycle review
  must reconcile against run-tag knowledge).
- `phase_stats[feasibility].knowledge_stored: 0`, although all 20 grade moves happened in that phase. Corrections
  are counted as `curate`, not `store`, so per-phase yield under-reads any phase whose output is grade movement.
- The sleep detector matched 3 loops: two leader file polls and one poc probe. The leader reports that it kept
  its turn alive with until-loops over the spawned agents' transcript-JSONL `stop_reason`. Those loops are not
  among the 3 matched. I cannot verify their form, so the count is a floor.
- The review's recommendation reads "Use `run_in_background` + `TaskOutput`". **`TaskOutput` is not a tool in this
  harness.** The tool the harness itself documents for waits is `Monitor` with an until-loop (the Bash tool blocks
  foreground `sleep`). The recommendation is a stale template, so do not copy it into a runbook.
- `auto_close` wrote a system entry **#385** "Retrospective findings: mnstd-002" (lesson-learned, `source:retrospective`).
  This retro did not author it.

## 2. What worked

- **The firewall refused strong evidence, mechanically, with no human watching.** The validator fetched
  done_when from the nodes and re-ran the rig from a clean detached checkout (n=6 runs, byte-identical identity
  set). It wrote its own tamper tests and ruled 37 clauses one at a time. The builder had recommended proven for
  C1–C5 and C7; the validator returned SCOPE FAIL on four literal clauses. This is the first method-caught instance of the
  shd-007 trap (#250, there human-caught). The ADR is now graduated as **#388**.
- **The validator returned the decision in a shape the human could rule on in minutes.** For each failing clause
  it gave the reason, whether a rework could clear it, and what would clear it. It also gave a three-column grade table:
  bar as written / fonts as environment / all four readings. The owner picked a column per item, and the curator
  found "no conflict; nothing withheld". This pattern is now written into #388's procedure.
- **Independent re-derivation kept the C5.3 ruling honest despite a broken checker.** The validator caught the
  checker trusting a pipeline-written file and re-derived containment itself (10/10) before ruling PASS. After
  the rework it wrote 7 *new* tamper cases rather than re-running the builder's (§3.4; lesson **#391**).
- **The curator handled rebase-merge provenance without being told.** It mapped pre-rebase to rebased SHAs, verified
  that the poc/task/artifacts trees were identical, and cited only on-main SHAs in `proven_by` (#365 etc.). It also re-verified all
  74 authored edges after id reissue. This is better than the method asks; see §3.3 for why it was necessary.
- **Honest partial.** C6 stayed `partial` on the owner's NO. The finding was recorded once (#358/#359), not
  duplicated, and the PDF native route is separated from the HTML glue in #383.
- **The goal-owner found the real miss itself.** "Show" meant owner viewing, and the committed evidence is JSON
  (relevance §1). It also found the unprobed native Word route (§2.1). Neither came from the owner, which is the
  judgement half of #322's bar (§5).
- **The leader ran four phases and a failed blocking gate unattended.** It also recovered the Issue that the PR
  merge auto-closed (§3.3).

## 3. What cost budget, or carries risk forward

### 3.1 Bar wording guessed at decompose time became three literal FAILs (the biggest cost)
N1.1 ("only Docker, Node 24 and Python 3.14"), N6.1 ("the only network access is the image pull") and C1.3
("semantic XML … number") encoded guesses about the toolchain. They were made before anyone had compiled anything,
from docs mnstd-001 already flagged as stale (mnstd-001 RETRO §3.5). Every substantive check passed, yet all
seven capabilities were `partial` as written, because N1 governs all of them. This is the step mnstd-001's OBS-26
anticipated, one level further: OBS-26 says to *freeze* defaulted answers. This run shows that a frozen bar can
still sit at the wrong **altitude**. Research lesson **#390**: write done_when at the behaviour, not the layer. The goal-owner made the same
note (relevance §1, §6). It also qualifies mnstd-001's #346 `proven`: the board's *structure* held (no prerequisite
was missed, and C2-first worked), but its *wording* was the weakest link in the proof.

### 3.2 Known literal conflicts were deferred to the most expensive gate
The leader's R1 and R2 (tech-discovery Extension) identified the N6.1 and C6.1 conflicts **before any compute**.
R1/R2 correctly left the bar unamended, because the judged party must not rewrite its own bar (#388). But the
coverage gate was pre-authorized, so the owner first saw the conflict as a SCOPE FAIL after a 2.7 h feasibility
phase. C1.3's conflict was knowable from findings-W0 and was not raised at all. The owner then ruled in minutes.
Factory enhancement **#392** (claimed, `Prerequisite→` #386): post literal conflicts as owner bar questions at
coverage time. Feasibility proceeds, and the question is not covered by pre-authorization.

### 3.3 Two git-convention defects, both from following the method as written
- **`Closes #74` auto-closed the scope Issue mid-run.** `factory-git` SKILL line 113 instructs exactly this: "Research
  PR (executables only): … `Closes #<scope-issue>`". The leader followed it. Under D15 the Issue's closing verdict
  is the gate record, so an executables PR must use `Refs #N`. The skill contradicts itself: line 112 says "The
  leader closes the Issue at CLOSE with the verdict comment".
- **Pre-rebase SHAs are cited in artifacts that outlive them.** RESULT.md (rework table: 9988331, 53a9d68, fdb8338,
  1bc97ca), gate-feasibility.md (17a7fa4, 7953833) and several Issue #74 comments cite SHAs that are **not on main**.
  The branch is deleted on merge (`git ls-remote --heads origin research/mnstd-002` is empty). They resolve only in
  this container's object store, so from a fresh clone they dangle. The curator's map in GRADES.md is the only
  bridge, and it is there by initiative, not by method.

### 3.4 The C5.3 checker trusted a pipeline-written file, and checker code was outside the freeze
Both are covered in lesson **#391**. The rule in `factory-poc.md` ("make the pass-check self-testing") was followed to
the letter: there were 33 self-tests, but every one altered *expectations*, never the primary artifact. The freeze
hashed fixtures and source but not `checks.py`. The C2.4 checker still trusts `mapping.json` (REPORT §8, F2).

### 3.5 Persistence and liveness rest on workarounds (autonomy risk)
- A harness hook ("Subagents should return findings as text, not write report files") blocked .md writes by every
  researcher, by the synthesis curator **and by the leader's own Write tool**. The leader persisted findings-W0..W4,
  REPORT.md and GRADES.md by extracting each agent's final fenced markdown block from its transcript JSONL, using a
  scratchpad `extract.py`, and writing via Bash. Writes the hook did not catch: SCOPE.md, validator gate reports,
  relevance.md. So the block keys on name or intent, not on path. **The de-facto contract is evasion of a harness
  policy by the one agent allowed to persist.** It fails silently if an agent returns zero or two fenced blocks. #21 →
  **#389** now records this evidence and options A/B/C. It is an owner decision (option B is a harness-config change).
- Liveness: the leader blocked on until-loops over the transcript `stop_reason` to keep its turn alive. mnstd-001
  §7.4 already proposes "notification, not file presence". The concrete instrument is `Monitor` with an until-loop
  on the completion condition (§1 note on `TaskOutput`).

### 3.6 Minor
- **#357 is still `unresolved` in the graph** although RESULT.md settled it empirically. REPORT F6 and the goal-owner
  both list it, and it has not been corrected. That is a curator action, not a retro write.
- Follow-on lists diverge: REPORT §9 has F1–F6, while #384 lists F1–F4 (goal-owner note (b), not acted on).
- `bash_for_search_count` 221 (outlier) is mostly the poc's probe compiles and XML greps inside the container.
  The work required it, so it is not a defect.

## 4. What surprised

- **Exit codes lie for broken sources.** Two of three seeded broken branches exit 0 (#356), and the "W0 rule" designed
  for the gate would have passed them. The gate verdict rule had to be rebuilt on log and err.html content (#381). This
  is a subject finding, but it generalizes as a method warning: *never accept a tool's exit code as a gate verdict
  without a seeded-red branch that proves the verdict rule fails it.*
- **The docs were wrong in both directions.** ISO HTML renders no review notes (docs say it does), and the PDF renders them
  regardless of stage gating (docs say it is gated). Both were found by measurement, not reading (#358/#359).
  mnstd-001's "stale docs" flag was right to worry.
- **Rework touched the rig; the owner added the font-pin condition, and it was done in-run.** This was cheap (45-file
  manifest) and turned an unpinned 833 MiB host dependency into a checked one. It is still enforced only by
  `make fonts`, not by `make demo` (F5).

## 5. Factory board movement

| Node | Move | Basis |
|---|---|---|
| **#251 → #386** Prove a technology with a real artifact (firewall) | `partial` → **`proven`** | The move-to-proven condition recorded on shd-007 is met: "clause check and grade recommendation produced by the method, human ruling only at the by-design blocking gate and NOT supplying a correction the method missed". A POC moved 4 techs to proven and 1 to partial, and #354 correctly stayed claimed. `proven_by` was attached in the same `context_correct` as `grade:proven` (D7). |
| **#322 → #387** Orchestrate a phase-gated run | `partial` → **`proven`** | The leader agent ran every phase and gate, including a *failed* blocking gate, rework and an independent re-check, with no inline human orchestration and no restart (`coordinator_respawn_count 0`). It clears both accumulated bars: judgement (wfh-005), since no verdict-moving owner injection occurred, and liveness (wfh-008). |
| #346 Decompose a goal | none | Structure held (no prerequisite added). Wording altitude failed (§3.1). Recorded here, not on the node. mnstd-001 §7.5's sharper done_when stays a proposal. |

**Counter-case, stated so the next retro can check it.**

- **#386:** the owner upgraded one validator call. The C5.3 defect was rated "changes no ruling". The owner made it
  a pre-merge blocker and added the font-pin condition. Grades did not depend on either, so I read these as
  severity calls at the gate, not as missed catches. A stricter reader could call the C5.3 upgrade a correction.
  If a later proof scope shows the owner supplying a grade-moving correction, drop #386 to `partial`.
- **#387:** autonomy rests on the two workarounds in §3.5. If either path closes, autonomy breaks, so they are
  recorded as reopen conditions on the node. In both cases n=1, and the advisory gates were pre-authorized.

## 6. Unimatrix writes (agent_id `factory-retro`, all tagged `mnstd-002`)

| id | category | what |
|---|---|---|
| **#386** | factory (capability) | correction of #251: grade `proven`, proven_by mnstd-002 + counter-case (1 out / 14 in edges carried) |
| **#387** | factory (capability) | correction of #322: grade `proven`, proven_by mnstd-002 + workaround caveats (1 out / 21 in carried) |
| **#388** | factory (finding, `position`) | correction of #250: clause-by-clause firewall ADR **VALIDATED** (method-caught, n=2) + boundary (fix upstream, not a looser gate; present readings as alternatives) |
| **#389** | factory (technology, claimed) | correction of #21: persistence contract, with mnstd-002 evidence (leader's own Write blocked, JSONL extraction) and options A/B/C |
| **#390** | lesson-learned (research plane) | Write done_when at the altitude of the behaviour, not a guessed toolchain layer or environment |
| **#391** | lesson-learned (research plane) | Checker must recompute from primary outputs; checker code inside the freeze (extends #239) |
| **#392** | factory (technology, claimed) | Enhancement: escalate pre-feasibility literal bar conflicts to the owner at coverage. `Prerequisite→` #386 |

Not written by me: #385 (system, `auto_close`).

Deliberately not written:
- a `Closes`/SHA-provenance node: a convention fix belongs in factory-git (§7.2), as mnstd-001 ruled for the credential helper;
- a telemetry node: the cross-cycle mis-binning is evidence for the existing #302, and is recorded in OBS-29;
- a sleep-polling node: OBS-18 and mnstd-001 §7.4 cover it;
- #357: a curator correction;
- pattern/procedure: D8.

Tag writes: 0 (`grade:` set inside the `context_correct` tag override).

## 7. Proposed method changes (verbatim; for the leader's single method PR combined with mnstd-001 §7. NOT applied)

OBS numbering: observations.md ends at OBS-23. mnstd-001 proposes OBS-24/25/26, so these are **OBS-27, 28, 29**.

### 7.1 `product/factory/observations.md`: append after the mnstd-001 OBS-26

```markdown
## OBS-27 — The report-file hook blocks the leader too; persistence now runs on transcript extraction
*2026-11-13 · from the mnstd-002 run (leader-reported) and retro*

A harness hook ("Subagents should return findings as text, not write report files") blocked .md writes by every
factory-researcher (W0–W4), the synthesis curator (REPORT.md, GRADES.md) **and the research-leader's own Write
tool**. SCOPE.md, validator gate reports and relevance.md were not blocked, so the block is name/intent-shaped,
not path-shaped. The leader persisted every blocked file by extracting the agent's final ```markdown block from
its transcript JSONL (scratchpad `extract.py`) and writing via Bash. OBS-7's "leader persists" contract now
depends on evading a harness policy, and fails silently if an agent returns zero or two fenced blocks. Not a
subject finding. Unimatrix: #389 (was #21), options A sanction-the-extractor / B harness config / C curator persists.
**Owner decision needed (B is a settings change).**

## OBS-28 — `Closes #N` on an executables PR auto-closes the scope Issue; rebase-merge orphans cited SHAs
*2026-11-13 · from the mnstd-002 run*

PR #75's body said "Closes #74", as factory-git instructs. The rebase-merge closed the scope Issue mid-run
(synthesis not yet done); the leader reopened it. Under D15 the Issue's CLOSE verdict comment is the gate
record, so an executables PR must say `Refs #N`. Second hazard, same merge: rebase rewrote every POC SHA and the
branch was deleted on merge, so SHAs cited in RESULT.md (9988331, 53a9d68, fdb8338, 1bc97ca), the gate report
(7953833, 17a7fa4) and Issue comments are not on main and dangle from a fresh clone. Only the curator's
pre→post map in GRADES.md bridges them — by initiative, not method.

## OBS-29 — The literal firewall worked; the bar it read was written at the wrong altitude, and the known conflicts reached the owner last
*2026-11-13 · from the mnstd-002 retro*

The validator re-ran the artifact (n=6, byte-identical), ruled 37 clauses, and returned SCOPE FAIL on four
(N1.1, N6.1, C1.3, C6.1-HTML) with every substantive check passing — the first method-caught instance of the
shd-007 trap (#388, ADR now validated). Three of the four were decompose-time guesses about the toolchain ("only
Docker, Node, Python"; "only network access is the image pull"; "semantic XML … number"). The owner cleared them
by ruling in minutes, choosing among the validator's A/B/C grade columns. Two were known at tech-discovery
(leader rulings R1/R2 correctly left the bar unamended) but the pre-authorized coverage gate meant the owner saw
them only after a 2.7 h feasibility. Lessons: #390 (done_when altitude), #391 (checker must recompute from primary
outputs; checker code inside the freeze — the C5.3 checker read a pipeline-written file). Enhancement #392
(escalate literal conflicts at coverage). Telemetry side-note: mnstd-001's retro ran in this session during
mnstd-002's scope phase and its stores (#347/#348) are counted as mnstd-002's — attribution is by session time
window, not feature_cycle (evidence for #302). The review's "run_in_background + TaskOutput" recommendation names
a tool this harness does not have; the documented wait is Monitor with an until-loop.
```

### 7.2 `.claude/skills/factory-git/SKILL.md`: line 113, "Research PR (executables only)" bullet

Replace:

```markdown
- **Research PR (executables only):** for POC code and datasets. `Closes #<scope-issue>`; the leader
  rebase-merges after the gate. Body = the run summary.
```

with:

```markdown
- **Research PR (executables only):** for POC code and datasets. **`Refs #<scope-issue>` — never `Closes`/
  `Fixes`/`Resolves`**: the merge happens before synthesis, and an auto-close would end the Issue before its
  CLOSE verdict comment, which is the gate record (D15; mnstd-002 OBS-28). The leader rebase-merges after the
  gate. Body = the run summary.
- **After a rebase-merge, re-anchor provenance.** Rebase rewrites every branch SHA and the branch is deleted on
  merge. Record a pre→post SHA map (with `git diff <pre> <post> -- <paths>` empty per pair) in the run's ledger,
  and cite only on-`main` SHAs in anything written after the merge (`proven_by`, REPORT, CLOSE comment).
```

### 7.3 `.claude/workflow/decompose-scope.md`: board gate (line 30), add after mnstd-001 §7.3 item 3

```markdown
- **done_when altitude check (before approving the board).** For each clause ask: *"if the tool satisfies the
  need through a different layer, file or one-time setup step than this wording assumes, should the clause
  FAIL?"* If no, rewrite at the need (e.g. "machine-readable number joinable from the compile's XML outputs",
  not "in the semantic XML"; "no network during the gated run; one-time provisioning declared and pinned",
  not "only network access is the image pull"). Keep layer-specific wording only where the layer IS the
  requirement (e.g. "native, not a bespoke overlay"). (Lesson #390; mnstd-002 OBS-29.)
```

### 7.4 `.claude/workflow/research-scope.md`: coverage gate (line 42), append to the bullet

```markdown
  **Bar questions at coverage.** The leader lists every clause the findings show cannot pass on its literal
  text (clause id + the finding that shows it) and posts them on the Issue as **owner bar questions**. Gate
  pre-authorization does not cover these items. Feasibility may proceed; the leader never answers them, and the
  validator still rules literally. (Enhancement #392, claimed; mnstd-002 OBS-29.)
```

### 7.5 `.claude/agents/factory/factory-poc.md`: "Make the pass-check self-testing" bullet (line 28), append

```markdown
  **The checker recomputes; it never reads the pipeline's verdict.** Every checker input written by the
  pipeline under test is re-derived from a primary output (compiled XML, git history) or cross-checked against
  one, and disagreement FAILs. Self-tests include ≥1 tamper of the **primary artifact** per clause, not only of
  the expectation. The freeze (`task/FROZEN.sha256`) covers checker, self-test and freeze code too.
  *(mnstd-002: the C5.3 checker read `containment.json` and passed a reverted v2; `checks.py` was outside the
  freeze. Lesson #391.)*
```

### 7.6 `.claude/agents/factory/research-leader.md`: runbook step 2, merge with mnstd-001 §7.4

Use mnstd-001 §7.4's replacement sentence, with its last sentence changed to:

```markdown
If you must wait in a shell, use **`Monitor` with an until-loop on the completion condition** (foreground
`sleep` is blocked); do not use bare `sleep` loops or file presence, and ignore cycle-review advice naming
`TaskOutput` (not a tool in this harness).
```

and add a new sub-bullet under step 2:

```markdown
   - **When a specialist's (or your own) report-file write is blocked** (OBS-7, OBS-27): persist its inline
     markdown yourself and stamp the file with a provenance comment naming the agent and the extraction. Until
     the owner rules on #389 (options A/B/C), treat a return with zero or several fenced blocks as a FAILED
     return and re-request; never hand-repair the content.
```

### 7.7 Curator follow-ups (not method; for the next curator spawn)

- Correct #357 with the empirical result in RESULT.md (both severities; full compile exits 1). This is REPORT F6.
- Reconcile #384's follow-on list (F1–F4) with REPORT §9 (F1–F6), as the goal-owner recommended in note (b).

## 8. Verification note

- Telemetry figures are quoted from this retro's own `context_cycle_review` json payload.
- Yield comes from `context_lookup(tags:["mnstd-002"])` (31 active).
- The cross-cycle attribution claim rests on the payload's `mutation_spread` evidence timestamp for
  `mnstd-001/RETRO.md` (1794588622, inside scope phase 1794588432–1794588632), on `knowledge_stored: 18` vs 16
  mnstd-002 stores, and on mnstd-001 RETRO §6 (#347/#348 written by that retro).
- SHA reachability was checked with `git merge-base --is-ancestor <sha> main` (the 6 pre-rebase SHAs: no; the 6
  rebased SHAs: yes) and `git ls-remote --heads origin research/mnstd-002` (empty).
- The factory-git line 113 quote is from the file.
- The harness-hook, extract.py and stop_reason-loop facts are **leader-reported**. I did not inspect the transcripts.
  The persisted-file provenance comment in GRADES.md/REPORT.md corroborates the extraction path.
