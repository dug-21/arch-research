# Theme-Driven Scanning — a standing generator above goals

**Status:** PROPOSED · design captured 2026-07-07 (owner + Claude design session) · not yet run
**Realizes:** owner intent — *"regularly look for new technologies that make Unimatrix better."* A new
**kind** of factory input: continuous, technology-push, feeding a live external product.
**Relates to:** `proposals/bidirectional-multi-goal-methodology.md` (multi-goal substrate this rides on)
· `experiments/ab-001-divergent-front-end.md` (the divergent front-end = this proposal's hypothesizer,
prototyped) · `experiments/mg-001-multi-goal-model-validation.md` (isolation the scan depends on).
**Firewall:** nothing here moves `status`. A **hypothesis is an unproven conjecture** — structure only —
and reaches `proven` ONLY when a bounded proof-goal's POC clears its `done_when`, demonstrated by us. The
scan generates *structure*, never *proof*.

---

## 0. The gap this fills

Every factory input to date is a **bounded goal**: an objective with a `done_when`, decomposed into a
finite capability board, driven to `proven`, then finished (shd, factory, platform-vision). The owner
wants something the model has no shape for: a **standing generator** — a recurring process that scans the
external world for technologies against themes we care about, and *emits* bounded research threads.

Four things are genuinely new (the rest reuses existing machinery):

1. **Continuous, not bounded.** A weekly scan never terminates. The factory has only one-shot scopes.
2. **Technology-push, not capability-pull.** Today: goal → decompose into capabilities (demand) →
   research technologies (supply) to fill them. This inverts it — start from a *technology* and ask
   *"which capability could this enhance?"* The edges exist (`Motivates`, `Prerequisite`); the
   *workflows* are built demand-first.
3. **The target is a live external product with its own SDLC.** Unimatrix (`dug-21/unimatrix`) ships and
   has its own delivery pipeline (the `uni-*` skills). A proven opportunity crosses a repo/plane boundary
   to become a real feature.
4. **A theme sits above goals.** "Edge-smart systems" is a hunting ground spanning use-cases (Unimatrix
   is #1, others likely). That's a level *above* goal→capability→technology.

**Scope boundary (load-bearing):** this theme takes ONLY the **novel/uncertain** slice — technologies
that *might* work and need proving. Routine Unimatrix improvement (bugs, UX, perf) goes straight to the
product's normal backlog and **bypasses the factory**. The factory's entire value is separating "might
work" from "proven works"; if the theme absorbs ordinary backlog it becomes a generic ticket queue.

## 1. The chain

```
Theme (standing, plural)
  → scan / owner-inject → Technology (candidate, grade:claimed, cited)
     → creative fan-out → Hypothesis (finding+hypothesis: "T could enhance capability C of use-case U")
        → triage (mostly kills) → Proof-goal (bounded, real done_when)
           → POC → proven (firewall)
              → handoff → Unimatrix issue (their SDLC decides)
```

Every arrow except *scan/inject*, *creative fan-out*, and *handoff* already exists in the factory. The
new machinery is the **theme**, the **hypothesis**, and the **creative fan-out** (hypothesizer).

## 2. Theme = steering config, NOT knowledge

The real axis is **evidence vs. steering**. The Unimatrix graph holds *graded evidence* — things with a
firewall status. A theme has no grade, no proof, no `done_when`; it is a standing *directive about where
to look*. Putting steering into the evidence graph is the category smell D8 warns against.

**Decision: theme is NOT a Unimatrix category.** It lives in a method-stream config doc,
**`product/factory/themes.md`** (sibling to `decisions.md` / `observations.md`), read on demand by the
theme-scan workflow, with a one-line pointer from `CLAUDE.md` for discoverability. CLAUDE.md is the right
*plane* (declarative, versioned, human-owned) but the wrong *file* — it is always-loaded and global;
themes grow/change and are only needed by scan runs, so they must not bloat global context.

**Queryability is preserved by tags, not the node.** The theme *definition* stays in the doc; every
downstream artifact (technology, hypothesis, proof-goal) carries a **`theme:<slug>` tag** (e.g.
`theme:edge-smart`). "Everything under this theme" is therefore one graph query. Definition = file;
evidence = graph.

**`themes.md` entry schema (per theme):**
- **slug** — `theme:<kebab>` (the tag namespace; e.g. `theme:edge-smart`)
- **lens** — the thematic hunting ground (e.g. *smarter systems on edge-capable devices; non-LLM
  text-processing / sorting / pattern-recognition; low-memory capabilities*)
- **value-targets** — the use-cases scored against (Unimatrix = #1; others as they arise). Two axes kept
  separate: *theme = hunting ground*, *use-case = value target*. A technology can serve the theme yet not
  the use-case, or vice versa; score on both.
- **source-mix** — where the scout looks (web / arXiv / GitHub-trending / HN / newsletters …). *(TBD;
  a config knob, not resolved here.)*
- **cadence** — target rhythm (e.g. weekly). Wave-0 = manual kick.

## 3. Modeling footprint (deliberately minimal — D8 discipline)

| Concern | Decision | Why |
|---|---|---|
| **Theme** | config doc `themes.md` + `theme:<slug>` tag | steering, not evidence (§2) |
| **Hypothesis** | a **`finding` tagged `hypothesis`** (mirrors `position`) | unproven conjecture = structure-only; fits the firewall; no category bloat |
| **Theme membership** | the `theme:<slug>` **tag** on artifacts | avoids inventing a `theme→goal` edge type |
| **Technology candidate** | existing `technology` category, `grade:claimed`, `cites:` the source | reuse |
| **Opportunity link** | conjectured `technology Prerequisite→ capability` edge; `finding Motivates→ technology` | existing edges |

**Net: 0 new categories, 0 new edge types.** New = 1 config doc, 1 tag namespace (`theme:*`), 1 finding
tag (`hypothesis`), 2 agent defs (§5), 1 workflow protocol (§5), 1 factory capability (§8).

## 4. The creative layer — where value and risk both concentrate

Hypothesis generation is *divergent* — the one thing the factory has never done (decompose, research,
prove are all convergent). It is the highest-value and highest-noise piece.

**Design (owner-specified, endorsed):** a precision-crafted **hypothesizer** agent def, on a
loose-reins deep-thinking model (**Fable 5 / `claude-fable-5`** — strongest with *less* prescriptive
direction), single step, whose sole job is to conceive potential applications of a technology under
review against our capability surface. Three constraints make it honest:

1. **Never let the generator grade its own ideas.** Split hard: the **generator** (Fable 5, loose reins,
   rewarded for *range*) and the **evaluator/triage** (skeptical, prescriptive rubric — the goal-owner,
   §6) are opposite prompting philosophies in *separate* agents. One agent that both dreams and judges
   rationalizes its own output. Divergent-then-convergent, adversarially split.
2. **"Better over time" only counts if measured.** The hypothesizer agent def is a versioned method
   artifact (`wf:` semver, method stream). Iterating its prompt *is* a method change — A/B-able against
   the funnel hit-rate (§9), i.e. the reflexive loop (#66) with the def as the independent variable.
   Without that metric, "getting better" is unfalsifiable fiddling. **Confound caution:** do not change
   the model and the prompt in the same iteration — pin the model when measuring a prompt change (cf.
   AB-001 §6 order-effect).
3. **Garbage-in ceiling.** The generator is only as good as (a) the scout's characterization of the
   technology and (b) a *current* map of the capability surface. For Unimatrix — use-case #1, which this
   repo dogfoods — that surface is fully knowable (the MCP tool set + the repo), so feed the generator a
   real, live capability inventory rather than letting it guess. A structural advantage for use-case #1.

**Failure mode to design against:** an LLM will happily conjecture that any technology enhances any
capability. The firewall protects the proven *end*; the *front* of the funnel has no quality control
except triage. So triage must be ruthless AND the hypothesis→proven hit-rate must be measured — if it is
near-zero, creative scanning is a budget sink dressed as innovation. That measured hit-rate is the
honesty check on the whole theme.

## 5. New agents + the `theme-scan` workflow

Two genuinely new roles; the rest reuse the existing roster.

| Role | New? | Contract |
|---|---|---|
| **scout** | NEW | External-world scanner per the theme's source-mix. *Discovers* candidate technologies (distinct from `factory-researcher`, which investigates a *known* partition — the scout finds the partitions). Read-only; returns candidate tech writeups (leader persists — OBS-7). |
| **hypothesizer** | NEW | Divergent generator (§4). Fable 5, loose reins. Input: a scout tech writeup + the current capability-surface inventory. Output: scored candidate hypotheses (conjectured `technology→capability` opportunities, incl. non-obvious). Structure-only; grades nothing. |
| **goal-owner** | reuse | The convergent triage/scorer (§6) — its relevance + step-function contract already fits. |
| **research-leader** | reuse | Orchestrates the scan, issues all `context_cycle` calls, persists artifacts, manages the gate. |
| **factory-curator** | reuse | Single writer — files candidate technologies + `hypothesis` findings, tags `theme:<slug>` + run-id. |
| **factory-researcher** | reuse | Deep-dive on a *promoted* hypothesis (the bounded directional/validated scope). |

**`theme-scan` protocol (recurring; sibling to decompose-scope / research-scope):**
1. Leader reads `themes.md` for the active theme(s) + budget envelope (§8).
2. **scout** surveys the source-mix → candidate technologies.
3. **hypothesizer** fans each candidate out across the capability surface → scored hypotheses.
4. **curator** files candidates (`technology`, `grade:claimed`) + hypotheses (`finding`+`hypothesis`),
   tagged `theme:<slug>` + run-id (per-run yield query, OBS-8).
5. **goal-owner** triages (§6) → shortlist.
6. Leader posts the shortlist to the owner (Issue) → owner promotes 0..n to bounded proof-goals.

Wave-0 = owner manually kicks the scan; the target is a scheduled agent (§8) that runs it and pings the
shortlist. Owner-injection (the LinkedIn-article path) enters at **step 2's output** — a hand-fed
candidate technology — and flows through 3–6 identically.

## 6. Triage/funnel discipline — the funnel's job is to say no

Weekly scans + serendipitous injections produce far more "interesting technologies" than can ever be
proven. Without a ruthless triage gate the board becomes a graveyard of `claimed` nodes and the scan
discredits itself. **The factory has no triage stage today** — every scope is assumed worth running.

Add an explicit cheap gate owned by **goal-owner**: score each hypothesis on
**novelty × capability-fit × effort × theme-alignment**, then route:

| Verdict | Action |
|---|---|
| **park** | record as `claimed` hypothesis, no further spend (the common case) |
| **directional-probe** | a bounded directional scope — cheap deeper look, structure-only |
| **validated-build** | promote to a bounded **proof-goal** with a real `done_when` → POC → firewall |

Most hypotheses die at *park*. Only survivors consume research budget.

## 7. Product bridge — report-and-handoff (owner-decided)

The factory **proves** an opportunity; it does **not** ship it. On `proven` (a POC clears the
proof-goal's `done_when`, demonstrated by us), the handoff is: **file an issue in `dug-21/unimatrix`**
with the proving artifact as evidence, and let Unimatrix's own SDLC decide. The factory does not PR into
the product. This keeps the research/delivery planes cleanly separated and the cross-repo surface thin
(one issue, not an integration). Architect for a deeper integration later (D10); build the thin handoff now.

## 8. Budget — the real gate on cadence

The weekly rhythm (owner's intent: 1–2 days/week external research, other days closing goals) depends on
**metering research spend against the subscription envelope — a capability still being built.** There is
a **factory-level budget**; shd's cost-governance research (#99) *originated* the thinking but must serve
the **entire factory**, not just the shd research subject.

- **Scoping instruction for #99:** architect factory-wide metering (D10), not an shd-specific solution
  that can't generalize. Dual customer: shd (research subject) + the factory (operational metering).
- **Two distinct pieces:** *in-run budget* already exists (the Workflow `budget` primitive:
  total/spent/remaining); *cross-run subscription accounting* — attribute spend per theme/goal/scope and
  allocate across the cadence — is the real gap (needs the token telemetry still unpopulated, OBS-6).
- **New factory capability:** *"meter + allocate research budget across the factory against the
  subscription envelope."* A **prerequisite to autonomous cadence** — NOT to the first manual scan
  (don't block the walk on the run).

## 9. Reflexive improvement — the funnel telemetry #66 needs

"Get better over time" = the reflexive loop (#66) applied to hypothesis yield. It requires a **funnel
metric** the factory does not yet capture:

```
candidates scanned → hypotheses generated → survive triage → reach proven → accepted by Unimatrix
```

Each stage is a tagged count (run-id + `theme:<slug>`), so the funnel is a graph query. Tuning targets:
the **hypothesizer agent def** (§4) and the **triage rubric** (§6) are the independent variables;
hit-rate (proven ÷ generated, and accepted ÷ proven) is the metric. This makes "getting better"
falsifiable rather than vibes — and is the mechanism that catches creative generation degrading into a
budget sink.

## 10. Convergence with in-flight work

- **AB-001's divergent front-end IS this proposal's hypothesizer.** The framing/whitespace/inversion pass
  is the creative fan-out. AB-001 stops being merely an A/B experiment — it is the *prototype* of the
  theme's core engine, measured against the same funnel.
- **MG-001** (multi-goal isolation) is the substrate the scan rides on — but a theme is *continuous and
  never parks*, a harder test than MG-001's one-active/one-parked design. This theme could be a **better,
  real second-goal vehicle** than the synthetic #92 wedge — or the thing MG-001 must de-risk first.
- **goal-owner** absorbs the triage scorer (§6) — an extension of its relevance/step-function contract,
  not a new role.

## 11. Threats to validity / failure modes (state them)

- **Plausible-nonsense generation** — the front of the funnel has no quality control but triage; mitigated
  only by ruthless triage + the measured hit-rate (§4/§9). If the hit-rate stays near-zero, kill or
  re-tune generation.
- **Unbounded backlog** — without park-by-default, `claimed` hypotheses accumulate and drift. Triage
  discipline (§6) is load-bearing.
- **Scope creep into product management** — the theme must take only the novel/uncertain slice (§0).
- **Dogfood bias** — opportunities noticed from *this repo's* friction over-fit one user's workflow. Label
  the source (dogfood-signal vs external-scan vs owner-injection) so the portfolio isn't accidentally
  fit to one operator.
- **Cadence outruns wave-0** — a weekly rhythm strains the manual factory; it is a *forcing function* for
  the scheduled runner (#25) and budget metering (§8), not something wave-0 sustains by hand.
- **Yield-by-tag is a convention, not engine-native** — the funnel depends on the curator tagging every
  node `theme:<slug>` + run-id. An untagged node is invisible to the funnel (cf. OBS-8, MG-001 §5).

## 12. Open decisions (owner)

- **`themes.md` seed** — author the first theme (`theme:edge-smart`) with its lens / value-targets /
  source-mix / cadence. Source-mix is TBD (§2).
- **Autonomy timing** — factory-autonomous scanning/hypothesizing is the highest-reach + highest-noise
  piece. Recommended: prototype the hypothesizer manually via AB-001 first, measure the hit-rate, *then*
  automate the scan on a schedule.
- **Sequencing vs. MG-001** — run MG-001 as designed first (validate isolation), then seed this as the
  concrete follow-on it de-risks; or let this theme *be* MG-001's real second goal (harder test).
- **First candidate** — the owner-injected generative-grammars / low-memory non-LLM text tech (from the
  LinkedIn article) is the natural first candidate technology to run end-to-end through §5 steps 3–6
  against Unimatrix's capability surface (`context_cycle_review` hotspot detection, `context_search`
  ranking, tag normalization — plus a whitespace pass for opportunities not yet listed).

## 13. To run this in a FRESH session (handoff — dogfoods "artifacts are the record")

1. `/factory-onboard` — derive status from canonical sources + live graph.
2. Read `proposals/bidirectional-multi-goal-methodology.md` (multi-goal substrate) + this proposal.
3. Author/confirm `product/factory/themes.md` for the active theme (§2, §12).
4. Build the two agent defs — `scout`, `hypothesizer` (Fable 5, §4) — under `.claude/agents/factory/`,
   and the `theme-scan` protocol under `.claude/workflow/` (§5). Method stream, `wf:` bump on merge.
5. Run one `theme-scan` on the seed candidate (§12) — curator tags every node `theme:<slug>` + run-id;
   goal-owner triages; shortlist to the owner Issue. Structure-only; the firewall is untouched until a
   promoted proof-goal produces a POC.
6. Record the funnel counts (§9) as the baseline the reflexive loop tunes against.

> If a fresh onboarded session cannot pick this up and run it from these artifacts alone, that gap is
> itself a `factory-retro` lesson — "artifacts are the system of record" failed, and that finding is as
> valuable as the scan.
