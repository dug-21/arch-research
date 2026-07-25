# W0-b2 — The SDLC-side incumbent

**Run:** `wfh-004` · Issue #48 · phase `scan` (rebuild, per Amendment A-7) · `agent_id: wfh-004-researcher-W0-b2` · read-only · zero graph writes · no experiments (SCOPE §11).

**Inspected (all reachable):** `/workspaces/arch-research/.claude/{skills/uni-*,skills/factory-git,workflow/sample-delivery.md,settings.json,.mcp.json}` · `dug-21/unimatrix` (359 PRs, 300 issues, 8 releases, `ci.yml`, `release.yml`, `.claude/{settings.json,hooks,rules,protocols,agents}`) · `dug-21/jurati` (1 PR, 11 issues, `.claude/*`, `CLAUDE.md`) · `dug-21/arch-research` (19 PRs, repo settings) · `surface/W0-a-landscape-by-concern.md` (re-read, not re-scanned).

**Verdicts:** **A** configured and running · **B** available but unconfigured · **C** structurally absent.

---

## 0. The headline, stated first

**The premise handed to this partition — *SDLC gets a machine-enforced merge gate for free* — is false in this owner's actual operation, and it is demonstrable.**

Across all 354 merged PRs in `dug-21/unimatrix`: 1642 SUCCESS / 22 FAILURE check conclusions; **6 PRs merged with a red check present**, and **20 merged before their last check completed**. Branch protection is unreadable (HTTP 403, token lacks admin), `rulesets` returns `[]`, and every one of the 359 PRs has `reviewDecision: ""` — **the GitHub-native APPROVED review has never been used**; the `uni-review-pr` security review posts as `COMMENTED`, authored by `dug-21`, on a PR authored by `dug-21`, merged by `dug-21`.

So the SDLC gate is a **98.3% discipline, not an enforcement plane** — structurally the same posture as the research firewall it was supposed to contrast with.

What SDLC actually gets free is **not enforcement**. It is **an external, non-model verifier producing a durable verdict**, plus **a durable addressable work record**. Those two are real and they are large. The enforcement is borrowed authority the operation has not switched on.

---

## 1. The SDLC incumbent table

| # | Capability as observable behavior | Concern | Layer | Verdict | Mechanism | Evidence |
|---|---|---|---|---|---|---|
| S-1 | Every change lands as an atomic, addressable, durable unit that survives the agent that made it | Structure / Recovery | HARNESS | **A** | git commit + branch; `uni-git` "all workflows produce PRs, no workflow commits directly to main" | `uni-git/SKILL.md`; 354 merged PRs |
| S-2 | A non-model verifier runs on every change and emits a machine-readable verdict | Structure / Introspection | HARNESS | **A** | `ci.yml` — 15 checks (Node 18/20/22/24 × ubuntu/macos/windows + inference-site script + GitGuardian), `on: pull_request` | `.github/workflows/ci.yml`; 1642 SUCCESS conclusions |
| S-3 | That verdict blocks the merge | Security / Structure | HARNESS | **C (as operated)** | would be branch protection; none readable, `rulesets: []` | 6/354 merged red; 20/354 merged pre-completion |
| S-4 | A human signature on a change is recorded by the platform | Human steering / Security | HARNESS | **C (as operated)** | GitHub review APPROVED unused | `reviewDecision: ""` on 359/359 PRs |
| S-5 | A fresh-context reviewer reads the diff cold and can block | Security | DEFINITION | **A** | `uni-review-pr` spawns a subagent, comments via `gh`, `gh pr review --request-changes` if blocking | `uni-review-pr/SKILL.md`; review bodies on #959/#946/#943/#936/#929 |
| S-6 | Work is reviewed as a *diff* — a bounded, addressable delta | Structure / Introspection | HARNESS | **A** | git; PR diff is the durable review unit | W0-a family B |
| S-7 | An interrupted run resumes from committed state | Recovery | HARNESS | **A** | commit-per-wave (`impl: wave {N}`), commit at every gate PASS; resume = re-issue `context_cycle(type:"start")` (idempotent, `AlreadyMatches`) | `sample-delivery.md` §Wave Execution, §Initialization |
| S-8 | A change can be undone after landing | Recovery | HARNESS | **B** | `git revert` / tag deletion available; used **once** in 359 PRs | PR title sweep |
| S-9 | Parallel writers are isolated | Recovery / Security | HARNESS | **B** | worktree isolation documented (`isolation:"worktree"`) but delivery explicitly spawns dev agents **without** it | `uni-git` §Worktree Isolation vs `sample-delivery.md` |
| S-10 | Stage order and gates are declared and blocking | Structure | DEFINITION | **A (prose) / C (enforced)** | 3a/3b/3c gates, "MANDATORY BLOCK", PASS / REWORKABLE FAIL / SCOPE FAIL, max 2 rework iterations — all markdown read by an LLM; **no engine reads it** | `sample-delivery.md` L167–202, L531–551 |
| S-11 | Each gate emits a durable verdict file | Introspection / Structure | DEFINITION | **A** | `product/features/{id}/reports/gate-3{a,b,c}-report.md`, verified by `uni-review-pr` Step 1 | PR #911 body "Gates: 3a PASS · 3b PASS · 3c PASS" |
| S-12 | Status advances only on behavioral evidence | Structure (evidence discipline) | DEFINITION → HARNESS req. | **A** | `uni-capability`: `delivery:{proven,partial,missing,asserted}` tag, `proven_by` field, "**Firewall holds** — `delivery:proven` ONLY with behavioral evidence" | `uni-capability/SKILL.md` |
| S-13 | Phase-conditioned context is injected at named steps | Context provisioning | HARNESS | **A** | Unimatrix hook-client on 8 events + `context_cycle` phase declarations; **identical binary in all three repos** | `settings.json` × arch-research, unimatrix, jurati |
| S-14 | Each spawned agent is handed only its own slice | Context provisioning | DEFINITION | **A** | "Each agent receives ONLY its component's pseudocode and test plan"; §Agent Context Budget | `sample-delivery.md` L277; unimatrix `implementation-protocol.md` L258 |
| S-15 | Authority is bounded per role/step outside the agent | Security | HARNESS | **B → C** | permission rules + sandbox exist in the incumbent; **no `permissions` key in any of the three `settings.json`** | all three settings.json |
| S-16 | Spend is metered and attributed to a unit of work | Cost | HARNESS | **C** | nothing. "Agent Context Budget" is prose about pasting, not metering | grep across unimatrix protocols |
| S-17 | Run telemetry is harvested and turned into stored lessons | Self-improvement | DEFINITION (on HARNESS input) | **A** | `context_cycle_review(feature_cycle, transcript:{})` → hotspots, baseline outliers, recommendations → `uni-store-{lesson,pattern,procedure}` | `uni-retro/SKILL.md` |
| S-18 | A change's outcome is attributed to a configuration and configurations compared | Self-improvement | HARNESS | **C** | absent both here and in the field (W0-a) | — |
| S-19 | A release is an irreversible external event with a declared trigger | Recovery / Structure | HARNESS | **A** | `release.yml` `on: push: tags ['v*']` → build → npm publish; `uni-release` pre-flight | 8 releases v0.8.7→v0.11.3 |
| S-20 | Method version is separable from product version | Introspection / SI | DEFINITION | **A (research) / C (SDLC)** | `factory-git` `wf:` semver from annotated tag; SDLC semver stamps the *product* only | `factory-git/SKILL.md` |
| S-21 | Pre-existing failures are distinguished from failures this change caused | Introspection | DEFINITION | **A** | Gate 3c: xfail markers must carry GH Issues, "confirm the failures are genuinely unrelated" | `sample-delivery.md` L368–376; PR bodies #943/#959 |
| S-22 | Work identity is externally addressable end-to-end | Structure | HARNESS | **A** | issue → branch → PR → commit → tag; `Closes #{N}` | PR #943 "Closes #940", #929 "Closes #928" |
| S-23 | Agent identity is preserved in the durable record | Introspection | HARNESS | **C** | all 359 PRs authored/merged by `dug-21`; agents act under the human's token — **the SDLC twin of D6 `created_by: anonymous`** | PR author sweep |

---

## 2. Per-concern verdict (all eight)

| Concern | SDLC ecosystem coverage | Residual after the ecosystem |
|---|---|---|
| **Structure** | **A for the delivery record, C for the run.** Git/GitHub supply durable, addressable, externally-named units (S-1, S-6, S-22) that outlive every agent. | The *stages, gates, roles and sequence* (S-10) exist only as markdown an LLM reads. No engine holds them; nothing detects a skipped stage. **Identical residual to research** — W0-a's #169 verdict holds in SDLC unchanged. |
| **Context provisioning** | **A.** Same hook-client, same `context_cycle` phases, in both domains (S-13); protocol prescribes per-agent slicing in every spawn prompt (S-14). | Same as research: no prospective statement of what is about to be injected, why, or what was excluded. Retrospective only. |
| **Security** | **B/C.** The field ships platform-plane enforcement (W0-a: Copilot cannot approve or merge its own PR); **this operation ships none of it** — no permission rules, no branch protection readable, no APPROVED reviews, agent runs on the human's token. | Everything. Role×step authority absent structurally. Here, even the available planes (S-15) are off — so *"the incumbent cannot"* vs *"we never turned it on"* is **as ambiguous on the SDLC side as SCOPE §11 says it is on the research side.** |
| **Introspection** | **A, and materially better than research.** A merged diff, a CI log, three gate-report files and a PR conversation are durable, queryable, and comparable across runs. | Causal account (S-11 reports are prose); agent-level attribution (S-23); cross-run comparison of *why* a gate failed. |
| **Cost** | **C.** Nothing meters model spend per unit of work in either domain (S-16). CI compute is metered by GitHub — off-model, non-attributable to a work step. | Total. **This concern is domain-independent and empty on both sides.** |
| **Self-improvement** | **B, the strongest of any cell in either domain.** `uni-retro` + `context_cycle_review` produce hotspots, baseline outliers and recommendations automatically from hook data, routed into stored lessons/patterns/procedures (S-17). | Adoption is manual and un-compared: no configuration A/B'd, no outcome attributed to a config change (S-18). **The measurement half exists; the attribution half does not.** |
| **Recovery** | **A for work product, C for the agent.** Committed waves + gate commits mean a dead session loses at most one wave (S-7); the repo on disk *is* the checkpoint; rollback exists (S-8). | Liveness detection. A dead subagent is still silently lost (#174) — **git saves the *bytes*, nothing declares the *unit* dead.** |
| **Human steering** | **B.** Human enters at the merge (real, external) and on SCOPE FAIL / rework exhaustion. | Mid-run redirection absent, exactly as W0-a found for the whole field. And the one gate the platform *could* enforce (S-3/S-4) is unused, so even the approval half is convention. |

---

## 3. The free-for-SDLC list (headline deliverable)

What git/CI/GitHub supply that a research run has **no equivalent for**:

1. **A durable atomic unit that outlives its author.** A commit exists whether or not the leader remembers to persist it. Research specialists cannot write files (OBS-7); their output exists only as inline markdown until a leader writes it — a strictly weaker guarantee. *(HARNESS)*
2. **An external, non-model verifier with a machine-readable verdict.** 15 CI checks decide green/red without an LLM. C-2 says research's verdicts bottom out in a model call; **SDLC's bottom out in an exit code. This is the single largest structural asymmetry between the domains.** *(HARNESS)*
3. **A rollback primitive.** `git revert`. The research substrate's nearest analogue, `context_correct`, is append-with-supersession — lineage, not undo. *(HARNESS)*
4. **An isolation boundary with merge semantics.** A branch. Research parallelism is safe only by convention ("never `git add -A`", disjoint directories), which is a rule, not a boundary. *(HARNESS)*
5. **A bounded review unit.** The diff. Research reviews prose findings files; there is no delta semantics, so "what changed since the last pass" is unanswerable. *(HARNESS)*
6. **End-to-end external addressing.** issue → branch → PR → commit → tag, resolvable by a stranger with no session context. Research's run identity is carried by naming discipline across a SCOPE file, an Issue, a cycle topic and a path. *(HARNESS)*
7. **A versioned, published artifact with a changelog derived from the record itself.** `uni-release` computes the changelog from conventional commits — the work record *is* the release-note source. *(HARNESS)*
8. **A pre-existing-failure baseline.** Because the verifier ran on the previous commit, "was this already broken?" is answerable. Research has no prior-state verifier, so a bad finding has no baseline. *(HARNESS)*

**Consequence for the build decision:** items 1–8 are things a harness must **integrate with**, not supply — *for SDLC*. For research they have **no incumbent at all**. So a harness supplying them generically buys research a whole substrate and buys SDLC an adapter. **That asymmetry belongs in triage's cost-to-prove column.**

---

## 4. The harder-in-SDLC list

1. **Irreversibility.** `release.yml` publishes npm packages on tag push. A published version cannot be cleanly unpublished; a wrong finding can be corrected. **Research has no irreversible operation at all.**
2. **Blast radius beyond the operation.** A merged migration or bad release reaches users; a bad finding reaches the next reader.
3. **Multi-repo coupling with no shared enforcement.** Three repos hard-code the hook-client path in `settings.json` — two point at an npx cache path, one at a dogfood-client path. A change in one repo's client ripples into the other two, and nothing checks it.
4. **Concurrency and volume.** 359 PRs vs ~5 research runs; wave-ordered dependencies; long-lived branches; rebase conflicts. Research runs occupy disjoint directories by construction.
5. **Verifier latency as a first-class cost.** CI is 4 Node versions × 3 OSes; merge-minus-last-check gaps reach **538 minutes**. Research's verifier is another LLM call — slower per unit of judgment, but not a wall-clock dependency.
6. **An environment exists and can be wrong.** `release.yml` installs ONNX Runtime, strips the binary, and *verifies the RUNPATH is baked* — build-environment correctness is a gate. Research has no deploy target.
7. **Shared mutable substrate under many concurrent writers** — the codebase. Hence the xfail-with-GH-Issue discipline (S-21). Research's analogous substrate (the graph) is protected by a single-writer rule instead, which is cheaper and **does not scale to 359 changes**.

---

## 5. The same-but-different register — the parameterization surface

Every row is an ability **both** definitions need, needed **differently**. This is the harness's configurable surface.

| # | Ability (HARNESS-layer statement) | SDLC form | Research form | What must be parameterizable |
|---|---|---|---|---|
| P-1 | A unit of work is named and addressable | commit / PR / feature-id `vnc-048` | workstream / finding / run-id `wfh-004` | The atomic unit and its addressing scheme are declared by the definition |
| P-2 | A gate's verdict is produced and recorded | Gate 3c = LLM validator **plus** CI exit code | synthesis gate = LLM + human | **Verifier type per gate** — deterministic command \| model judgment \| human signature. Not per-domain: **SDLC uses all three** |
| P-3 | Status advances only on evidence | `delivery:{proven…}` + `proven_by` behavioral test | `grade:{proven…}` + `proven_by` artifact | The **status vocabulary and the evidence predicate per transition** are definition-authored; the enforcement is harness-supplied. `uni-capability`'s stated motive ("features marked delivered against criteria they only *structurally* satisfied") is **the research firewall's motive verbatim** |
| P-4 | A failing unit is retried within a bound | **max 2 rework iterations per gate**, then SCOPE FAIL | **exhaustion is the done-condition**, ≥2 generation rounds (A-2) | Loop policy: bounded-rework vs exhaust-until-dry. **Opposite defaults on the same mechanism** |
| P-5 | Parallel units are isolated | worktrees available; delivery deliberately runs dev agents **without** them | "Not needed for read-only research fan-out" | Isolation keyed on **declared write-scope of the unit**, not on domain |
| P-6 | Write authority is bounded | many writers to code, one coordinator | **one curator writes graph nodes, ever** | Declared **write-authority per resource per role** |
| P-7 | A human enters mid-run | blocking at merge; re-entry only on SCOPE FAIL | blocking **at gates only**; in-envelope steers must not block | Per-gate policy: **blocks** vs **surfaces** |
| P-8 | The lifecycle emits an event that triggers learning | `uni-retro` on **PR merge** | `factory-retro` on **cycle close** | The definition binds retro to **its own** lifecycle event |
| P-9 | Artifacts are persisted to a durable sink | git | git **and** the graph | Declared persistence sinks per artifact class |
| P-10 | The method itself is versioned | semver stamps the **product** | `wf:` semver stamps the **method** | What the version identifies is declared |
| P-11 | Phase-conditioned context is injected | phases `spec → spec-review → develop → test → pr-review` | research phases | **Phase vocabulary is definition-layer; phase-conditioned injection is harness-layer** — demonstrated by the same hook binary + same `context_cycle` API serving both, in three repos, today. **The strongest layer evidence in this file** |

**SDLC's firewall equivalent:** the **same harness ability with different content**. `uni-capability`'s `delivery:proven`-only-on-behavioral-evidence is structurally identical to `grade:proven`-only-on-artifact — same tag mechanism, same `proven_by` field, same stated motive. The one genuine harness difference: **SDLC's evidence can be a program that re-runs** (a test, a CI conclusion); **research's is a record of a past demonstration.** The harness must therefore accept both an *executable predicate* and an *attested artifact* as evidence sources — a real requirement, not a vocabulary difference.

---

## 6. Reachability report

**Inspected successfully:** all files in the header; `gh` authenticated as `dug-21`; both owner repos public; full PR/issue/release/check history for `unimatrix` (354 merged PRs with check rollups), `jurati` (1 PR, 11 issues, no `.github/workflows` — HTTP 404), `arch-research` (19 PRs, 1 check: GitGuardian).

**Could not inspect — flagged, with the cheapest settling test:**

| Unresolved | Why | Cheapest test (not run) |
|---|---|---|
| Branch protection on `main` in all three repos | HTTP 403 "Resource not accessible by integration" — token lacks admin scope. `rulesets` returns `[]` (readable, empty) | One `gh api repos/{r}/branches/main/protection` with an admin-scoped token. Pure read |
| Merge settings for `unimatrix`/`jurati` | returned `null` (scope). `arch-research`: auto_merge=false, rebase+squash+merge true, delete-on-merge true | same admin-scoped read |
| Whether the 6 red-check merges were overrides, admin bypasses, or post-merge re-runs | check rollup is current state, not merge-time state | `gh api repos/…/commits/{sha}/check-runs` at the merge SHA per PR |
| `unimatrix/.claude/agents/{ndp,uni}/*` and `.claude/protocols/uni/*` contents | directory listings only; not fetched (budget) | direct `gh api contents` reads |
| `product/features/vnc-*/reports/gate-*.md` | not fetched; would convert S-11 from doc-claim to demonstrated | one contents read of any feature's `reports/` |
| Whether unconfigured permission rules are a ceiling or a choice | SCOPE §11 forbids the experiment | **inherits the §11 ambiguity identically on the SDLC side — a new fact: the ambiguity is not research-specific** |

**Evidence-class note.** S-1, S-2, S-3, S-4, S-6, S-7, S-19, S-22, S-23 are **demonstrated by inspection of live repository state**. S-5, S-10, S-11, S-12, S-14, S-17, S-20, S-21 are **doc-claim from protocol files** — artifacts verified only for S-11 (PR #911 body) and S-5 (five review bodies). S-8, S-9, S-15, S-16, S-18 are **absence claims within this evidence base**, not demonstrated absences in the world.
