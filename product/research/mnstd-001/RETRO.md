# mnstd-001: Retrospective

**Role:** `factory-retro` · **Run:** `mnstd-001` (decompose-scope) · goal `mnstd` · [Issue #73](https://github.com/dug-21/arch-research/issues/73)
**Run method stamp:** `wf-v0.26-46-gc4b39f5` (it matches `git describe` at `c4b39f5`, so the stamp is correct) · **Repo state:** `main` at `ecac38f`
**Outcome under retro:** board produced, structure only. Goal #329, C1–C7 #330–#336, N1–N8 #337–#344,
all `grade:missing`, 53 edges. Nothing proven, which is correct for a decompose-scope. The program
continues as `mnstd-002` (in progress, not reviewed here).

---

## 1. Process telemetry: **AVAILABLE** (no "No observation data")

`context_cycle_review(feature_cycle:"mnstd-001", auto_close:true, format:"json", agent_id:"factory-retro")`
returned a full report: 1 session, 92 records, phases `scope` → `decompose`, phase gate text present,
one friction hotspot, and `curation_health` within normal range.

| | |
|---|---|
| wall time | 1 583 s (26 min). scope 208 s · decompose 1 183 s · unnamed tail 192 s |
| knowledge stored (run-tag lookup, authoritative) | **16** (#329–#344). The curator's BOARD.md and the lookup agree |
| rework | none. Both gates passed first time (the owner pre-authorized both) |
| hotspot | `sleep_workarounds` 7: the leader polled for file existence and then for mtime stability on SCOPE/DECOMPOSITION/BOARD |
| context before first write | 32 KB (baseline mean 629 KB) |

**The instrument contradicts itself again, in OBS-23's shape, with one new consequence.**

- `metrics.universal.knowledge_entries_stored: 0`, while `session_summaries[0].knowledge_stored: 16` and
  `phase_stats[decompose].knowledge_stored: 16` appear in the **same payload**. The session block attributes the
  stores correctly, so this is **not** OBS-14 subagent blindness. The universal scalar is simply not
  computed.
- `total_tool_calls: 0` against a `tool_distribution` summing to 84. `feature_knowledge_reuse.total_served: 0`
  against `knowledge_served: 9`. `attribution.total_session_count: 0` against `session_count: 1`.
- `agents_spawned: ["factory-curator"]` only. DECOMPOSITION.md was authored by a `factory-researcher`
  spawn (its header says so, and the leader's poll loop waited on that file).
- The close interval (192 s) is recorded as a phase named `""`.
- Every one of these is scored `Normal` against a `0.0 / 0.0` baseline.

**New consequence: a prior retro's claim is void.** The wfh-011 RETRO §1 row reads
"`knowledge_entries_stored` **0**: the zero-writes instruction is corroborated by the instrument, not
only attested". That field reads 0 whatever was written. #302 had already recorded it at 0 against 35
real stores (wfh-007) the day before wfh-011 cited it. wfh-011's zero-writes claim may well be true, but it
is **attested, not corroborated**. Stored as factory finding **#348** (`Motivates` → #302).

## 2. What worked

- **Owner brief recorded verbatim, before scoping** (`OWNER-BRIEF.md`, commit `91472ca`). Every specialist
  read the source rather than a relay. The four demos, the ISO flavor, and the "one research-scope, not four"
  placement rule all survived into SCOPE §Success criteria 2/6 and DECOMPOSITION §6–§7 unchanged.
- **The decomposition found the hidden prerequisite.** C2 (the anchor/addressing model) is what all four
  demos depend on. Making it a capability on the critical path (C1→C2→C3→{C4,C5,C6}), and not an NFR,
  means a C2 failure in mnstd-002 rules W1–W4 *blocked* rather than *failed*. This is the most valuable cut
  on the board. Stored as research lesson **#347**.
- **Supply and demand kept apart.** Every capability is `missing`, even where Metanorma docs claim the
  feature (C1, C6). Doc-claims are parked for technology nodes in mnstd-002 (DECOMPOSITION §5 grade
  rationale). This is the firewall applied at decompose time, and it was done without prompting.
- **Provenance of invented numbers stays on the node.** N7's 5 MB budget and the fixture sizes are labelled
  "researcher proposal, not an owner number" inside the node content (#343). This is good practice, but see §3.2.
- **The curator verified its own writes against the graph**, not against its report: two subgraph queries
  (16 nodes / 15 Advances, 38 About+Prerequisite). It also matched prior-board tag conventions (opcost, shd)
  and did not adopt the researcher's speculative `goal:`/`kind:` tags.
- **Fast and cheap.** 26 minutes, one session, no rework. A decompose-scope is the right size for a
  new standalone goal.

## 3. What cost budget, or carries risk forward

### 3.1 The leader polled files instead of waiting on spawn completion (7 sleep loops)
The research-leader definition (`.claude/agents/factory/research-leader.md` runbook step 2) says "poll, or
block on a wait". The leader polled for **file existence** and then added an **mtime-stability** loop
because the file appears before the writer finishes. This is a race guard invented in-run. The
authoritative completion signal is the spawn's notification or return, not the file. OBS-18 already records
the cost of sleep loops. The new point is that file presence is the wrong completion predicate: it races
with partial writes.

### 3.2 Defaulted owner questions become the firewall bar, and nobody has ratified them
The owner pre-authorized all advisory gates, so Q1–Q9 were "proceeding on defaults" (Issue #73,
decompose phase-end). Several defaults are now **inside done_when clauses that mnstd-002's validator will
rule against**: C7.2 ("owner-selected format (Q1; default HTML + YAML/CSV)"), C3's optional `line` field
(Q3), and N7.1 ("proposed: 5 MB"). Labelling them as proposals is honest. But a clause that reads
"proposed" or "default" leaves the bar open, and OBS-21 shows who closes an open bar under pressure:
the party being judged. A decompose-scope close should **freeze** the defaulted answers as the binding
bar, explicitly, in the gate comment.

### 3.3 Naming and convention drift (minor)
- SCOPE.md names the output `decomposition.md`, while the leader's tasking named `DECOMPOSITION.md`.
  The researcher had to add a path note. `decompose-scope.md` says only "a decomposition file".
- The researcher proposed `goal:mnstd` and `kind:business|nfr` tags "if that convention is in use". The curator had
  to infer the real convention from two prior boards. The board tag convention (`business|nfr`,
  `grade:<g>`, `{goal}`, `{run-id}`; NFRs are `category: capability` with `kind: nfr` in content) is not
  written down anywhere a decomposer reads.

### 3.4 Git push hung (environment, reported by the leader, reproduced in config)
`git push origin main` hung indefinitely. The configured `credential.helper` is the VS Code
remote-containers node helper (verified: `git config --get-all credential.helper` → the
`vscode-remote-containers-*.js git-credential-helper` wrapper, listed twice). It blocks on `get` once the IDE
websocket at 127.0.0.1 drops. In this retro session the `ide` MCP server also failed to connect with that
same websocket error. `git -c credential.helper= -c credential.helper='!gh auth git-credential' push`
succeeded immediately. For an autonomous run this is a silent hang, not an error, so nothing
surfaces it.

### 3.5 Research-side flag carried forward (not a process defect)
The light grounding relied on **stale docs**: rubydoc metanorma-standoc 1.0.x/1.1.x, and the current
metanorma.org pages returned 404 (DECOMPOSITION §9). Reviewer-note syntax, the render-annotations
attribute, and `commenter`'s scope are all doc-claims of uncertain age. mnstd-002 must verify each one on the
pinned image before building on it.

## 4. What surprised

- The decomposition's riskiest call, "ISO `line` field: optional", is driven by an **absence not proven**
  (no line numbering found in metanorma-iso docs). If mnstd-002 finds draft line numbers, Q3 flips and C3's
  done_when tightens. That is a cheap thing to check first in W0.
- The cycle review's "Knowledge reuse: unavailable (no served knowledge)" sits beside `knowledge_served: 9`
  in the same call.

## 5. Factory board movement

**#26 "Decompose a goal into a capability board": `partial` → `proven`** (corrected #26 → **#346**,
`grade:proven` set in the same `context_correct` that attaches `proven_by`, per D7).

- done_when: "from a goal, an AGENT produces the capability/nfr board (Advances/About/Prerequisite) with no
  human authoring the nodes inline." mnstd-001 clears it: a factory-researcher wrote the decomposition, a
  factory-curator wrote all 16 nodes and 53 edges, and the advisory gates were owner pre-authorized. The artifact is
  BOARD.md, `ecac38f`, plus nodes #329–#344. The prior proof was manual (shd-001), so it was rightly `partial`.
- **Caveat, recorded on #346:** this done_when tests *who held the pen*, not *whether the board is right*.
  Board quality is tested only downstream. If mnstd-002 shows a mis-cut or missing prerequisite that blocks
  a firewall ruling, re-open the grade. A sharper done_when (for example "and the downstream research-scope
  rules every capability without adding a prerequisite the board missed") is proposed below.
- #322 (orchestrate a phase-gated run) is not moved. This run was gate-light (both gates advisory and
  pre-authorized; no blocking gate exercised), so it adds no evidence for the blocking-gate path.

## 6. Unimatrix writes (agent_id `factory-retro`, all tagged `mnstd-001`)

| id | category | what |
|---|---|---|
| **#346** | factory (capability) | correction of #26: grade `proven`, proven_by mnstd-001 + caveat (14 incoming / 1 outgoing edges carried) |
| **#347** | lesson-learned (research plane) | Decomposing an N-demo goal: find the shared substrate and make it a prerequisite capability, not an NFR |
| **#348** | factory (finding) | `knowledge_entries_stored` never populated; wfh-011's "corroborated" claim void. `Motivates` → #302 |

Deliberately not written: a git-credential enhancement node (an environment hazard with a known fix
belongs in `factory-git`, not the testing backlog); a sleep-polling node (OBS-18 covers it); no
pattern/procedure (D8).

## 7. Proposed method changes (verbatim; for the leader's single method PR. NOT applied)

### 7.1 `product/factory/observations.md`: append

```markdown
## OBS-24 — `knowledge_entries_stored` is never populated, and wfh-011 cited it as corroboration
*2026-11-13 · from the mnstd-001 retro*

`context_cycle_review(mnstd-001)` reports `metrics.universal.knowledge_entries_stored: 0` beside
`session_summaries[0].knowledge_stored: 16` and `phase_stats[decompose].knowledge_stored: 16` in the
same payload; the run-tag lookup confirms 16 nodes. The session block attributes the stores correctly,
so this is not OBS-14's subagent blindness: the universal scalar is simply not computed. Same payload:
`total_tool_calls: 0` vs a distribution summing to 84; `total_served: 0` vs `knowledge_served: 9`;
`attribution.total_session_count: 0` vs `session_count: 1`; `agents_spawned` omits the
factory-researcher; the close interval is a phase named `""`. All scored `Normal` on a 0.0/0.0 baseline.

**Correction:** wfh-011 RETRO §1 says its zero-writes instruction was "corroborated by the instrument"
via `knowledge_entries_stored: 0`. That field reads 0 whatever was written (#302 recorded it at 0 vs 35
stores the day before), so the claim is attested, not corroborated. **Rule: never cite a
`metrics.universal` scalar as corroboration; yield comes from a run-tag `context_lookup` only.**
Unimatrix: #348 (Motivates #302).

## OBS-25 — `git push` hangs silently on the VS Code container credential helper
*2026-11-13 · from the mnstd-001 run (leader-reported, config verified in retro)*

The repo's `credential.helper` is the VS Code remote-containers node helper. When the IDE websocket at
127.0.0.1 drops (the `ide` MCP server fails with the same error), `git-credential-helper get` blocks
forever and `git push` hangs with no error. `git -c credential.helper= -c
credential.helper='!gh auth git-credential' push origin main` succeeds immediately. In an autonomous
run a hang is worse than a failure: nothing surfaces it. Fix lives in factory-git.

## OBS-26 — Defaulted owner answers become the firewall bar without being frozen
*2026-11-13 · from the mnstd-001 retro*

With advisory gates owner-pre-authorized, mnstd-001 proceeded on researcher defaults for Q1–Q9. Several
now sit inside done_when clauses the mnstd-002 validator rules against, still worded as open
("owner-selected format (Q1; default …)", "proposed: 5 MB"). Honest labelling — but an open bar is
closed later by whoever is under pressure (OBS-21). A decompose close must freeze defaulted answers as
the binding bar. Secondary: the leader's file-existence + mtime-stability poll loops (7) used file
presence as a completion predicate; it races with partial writes — the spawn notification is the
signal.
```

### 7.2 `.claude/skills/factory-git/SKILL.md`: add under push conventions

```markdown
- **Push with an explicit credential helper.** In the dev container the default helper is the VS Code
  remote-containers bridge, which hangs (no error) if the IDE connection has dropped. Always push as
  `git -c credential.helper= -c credential.helper='!gh auth git-credential' push origin <ref>` (same for
  tag pushes). If a push produces no output within ~30 s, assume this hang, not a network problem.
```

### 7.3 `.claude/workflow/decompose-scope.md`: three edits

1. Name the output file: replace "a decomposition file" with "`DECOMPOSITION.md` (exact name)".
2. Add a **board tag convention** line for the researcher and curator: "Tags: `business|nfr`, `grade:<g>`,
   `{goal}`, `{run-id}`; goal node tags `goal`, `{goal}`, `{run-id}`. NFRs are `category: capability`, `kind: nfr`
   in content. No `goal:`/`kind:` prefixed tags."
3. At the board gate: "If owner questions are answered by default (including pre-authorized gates), the
   gate comment lists each default that appears in a done_when clause and declares it **binding for the
   firewall**. Rewrite 'proposed'/'default' wording in those clauses to the fixed value before close."

### 7.4 `.claude/agents/factory/research-leader.md`: runbook step 2

Replace "Keep the turn alive until every spawn has reported: poll, or block on a wait" with: "Keep the
turn alive until every spawn has **reported**. The completion signal is the spawn's notification or
return, **never the presence of its output file** (a file appears before its writer finishes). If you must
wait in a shell, use `run_in_background` and the notification, not `sleep` loops."

### 7.5 Factory capability #346 (was #26): proposal only, curator's call later

Sharpen done_when to: "…with no human authoring the nodes inline, **and the downstream research-scope
rules every capability without adding a prerequisite the board missed**." This would make `proven`
measure board quality, not just authorship. If adopted, #346 drops back to `partial` until mnstd-002 closes.

## 8. Verification note

The telemetry figures are quoted from the json payload of the retro's own `context_cycle_review` call. Node
counts come from `context_lookup(tags:["mnstd-001"])` (16). The credential-helper config was checked with
`git config`. The wfh-011 quote is from `product/research/wfh-011/RETRO.md` line 49. The researcher-spawn
claim rests on the DECOMPOSITION.md header and the leader's poll target. No transcript evidence was retrievable
(the scoped transcript query returned no candidates).
