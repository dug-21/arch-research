# wfh-005 — triage amendment 1

**Append-only (D3).** This amendment does **not** overwrite `reports/triage.md`. It reconciles two
owner-injected corrections against verdicts already written, and states exactly what changes and what stands.
Read `triage.md` first; read this second; where they conflict, **this file governs.**

**Trigger:** the owner, at the blocking gate, disputed the emergent position P6 and asked whether the `ruvnet`
projects had been looked at. Both challenges landed. One falsifies a position this run proposed; the other
exposed a coverage failure that changes the P4 routing's composition.

**Budget:** 7 of 10–12 spawns (one round-two active-development pass). **Status moves: still 0.**

---

## A. P6 is falsified as stated. The owner's evidence, and my error.

`triage.md` §4 proposes P6 — *the declared workflow is a fiction* — and recommends putting it in front of the
owner ahead of the five. **The second half of that position is now falsified, and the first half is much
narrower than stated.**

### The evidence

`dug-21/unimatrix/.claude/protocols/uni` holds five protocols: delivery (31KB), bugfix (27KB), design (21KB),
research (14KB), agent-routing (9KB). The oldest dates from 2026-02-22. Against them:

| Measure | Value |
|---|---|
| Merged PRs in `dug-21/unimatrix` | **354** |
| Closed issues | **467** |
| Revisions to `uni-delivery-protocol.md` | **31** (2026-02-22 → 2026-07-25) |
| Revisions to `uni-bugfix-protocol.md` | **30** |
| Revisions to `uni-design-protocol.md` | **21** |
| **Executions per phase-graph revision** | **≈ 11:1** |

That is the **high-repetition regime** W4's adjacent-field argument says phase-indexation requires. The
modelling cost is amortized across hundreds of executions, exactly as it is for an in-toto layout, a DO-178C
certification plan, or a Bazel action.

### Where my synthesis went wrong, stated plainly

The leader's spot-check in `scout-merged.md` §6 offered three signals: protocol-file commit counts,
wfh-004's eight mid-run amendments, and wfh-005's five declared deviations. **The second signal was a category
error, and it was mine.** wfh-004's amendments A-1…A-8 amended a **scope** — what that run investigated. They
did not amend the **phase graph**. I counted scope churn as evidence of phase-graph instability, and the two
are different objects. `triage.md` §4 inherited that error and cited it back.

The goal-owner had already flagged the adjacent problem — that P6's strongest evidence (20,574 interactive
coding-agent sessions) measured the wrong population, and that the spot-check established direction and not
magnitude. It correctly declined to treat P6 as established. The owner's evidence closes what remained.

### What P6 becomes

| Claim | Status |
|---|---|
| The phase graph is **not stable across runs** | **FALSIFIED.** 354 executions against 31 revisions of a protocol that has existed for five months |
| The phase graph is **not knowable before a run** | **FALSIFIED for protocol-authored work.** The protocol is complete before the first spawn; what gets amended mid-run is the scope |
| The phase graph is authored by the **same party that executes and grades it** | **STANDS.** This is W4's separate position P7, and the owner's evidence does not touch it — 354 executions of a protocol the executing party may edit is still self-restriction by the credential holder |
| Research protocols specifically churn | **STANDS, narrowly.** `theme-scan.md` 9 commits, `research-scope.md` 6, both edited 2026-08-01. A scan's phase graph is less settled than a delivery run's |

**P6 is downgraded from an emergent position to a scoping observation:** *phase-indexed authority fits
protocol-authored, repeated work — which this operation demonstrably runs — and fits interactive,
progressively-refined sessions poorly.* That belongs in the theme's **lens** as a scope statement, not in front
of the owner as a challenge to the five.

**Downstream corrections to `triage.md`:**
- §4's recommendation to put P6 ahead of the five is **withdrawn**.
- §4's falsifier is **discharged** — do not spend the hour; the counts are above.
- §3's note that *"the compiler's input is a declaration; the sixth position says that declaration does not
  exist"* is **withdrawn**. The declaration exists. W4's build ordering argument loses its stated basis, and
  the BUILD's remaining legs are re-derived in §B below on different evidence.
- **W4's P7 (the policy author is not outside the executor) is untouched and is now the stronger of the two.**

---

## B. The ruvnet miss, and what it changes

The owner asked whether `ruvnet/ruflo` and `ruvnet/metaharness` had been looked at. They had not. Round two ran
on the active-development surface; full evidence in `scout-active-dev-r2.md`.

**This was not a thin cell. It was a hole in method**, and it is the more important of the two corrections
because it changes a routing rather than a position.

### B1. The decisive find is not ruvnet — it is what ruvnet pointed at

`ruflo` (66,763★, MIT, ~97% one maintainer) is `claude-flow` renamed; the stars were earned over 14 months as
a Claude Code swarm orchestrator. It contains **more of the theme's object in real code than anything round
one found** — a blocking policy chokepoint on every MCP dispatch, monotone capability envelopes that throw
`capability-envelope-cannot-grow`, delegation attenuation, approvals with self-approval forbidden, receipts,
and an HMAC trust anchor outside the workspace. And essentially **all of it is inert by default**
(`mode: 'legacy'` → `enforcedOutcome: 'allowed'`), the delegation propagator has no call sites by its own
header, and the project maintains an **audited registry of 106 environment-variable escape hatches**.

Two days ago it shipped an ADR integrating **CASA — Continuous Agent Semantic Authorization** — which is a
**Cisco Outshift project under the Linux Foundation's AGNTCY programme**: `outshift-open/outshift-casa`,
Apache-2.0, alpha since 2026-04-17, seven Cisco engineers, **17 stars**. Envoy sidecar auto-injected per pod,
eBPF deny-by-default egress, a `MultiAgentSystem` CRD, tokens injected on egress and validated on ingress
*"without any changes to the application."*

**That is the BUILD's enforcement-plane leg, shipping.** Its siblings `outshift-open/ASTRA` (*"Authorization
with Semantic **Task-based** Restricted Access"*) and `outshift-open/tbac-research-datasets` show a sustained
research programme built on **TBAC — Task-Based Access Control**, the Thomas & Sandhu model W1 and W4 both
named when they falsified P2.

### B2. The BUILD does not collapse. It loses two of four legs.

`triage.md` §3's BUILD, decomposed:

| Leg | Status after round two |
|---|---|
| **A** — derive and enforce an authority bound | **NOT NOVEL.** ruflo's envelope engine; CASA's CRD |
| **B** — demand set **discovered during execution** rather than declared before it | **SURVIVES.** Everyone declares. ruflo's compiler parses the objective string once, up front; CASA takes the CRD plus the initial prompt. Nobody discovers |
| **C** — monotone: narrows freely, widens only on approval | **HALF NOT NOVEL.** ruflo ships monotonicity, unit-tested. But widening simply throws — it is not approval-gated, and approvals exist as a *separate, uncomposed* mechanism. **The composition survives** |
| **D** — enforced by a plane the principal holds no credential for | **FALSIFIED by Outshift CASA.** Sidecar + eBPF, application-transparent |

**The BUILD is now two legs: (B) deriving the bound from demand observed during execution, and (C) composing
monotonicity with an approval path whose issuer is not the principal.** Both are load-bearing; neither has a
shipping counter-example. Everything else in the §3 statement is somebody's released code.

**One honest counterweight:** CASA is alpha, `v1alpha1`, Istio-only, zero releases, and requires Kubernetes.
A harness that must run on a laptop cannot use it. That is a real escape route for the BUILD — **but it is an
argument about substrate, not about novelty**, and it must be stated that way rather than as "nobody has done
this."

### B3. Other verdict effects

- **P4 — routing unchanged (ASSEMBLE), composition changed, window shortened.** Add `outshift-casa` (or an
  Envoy+eBPF equivalent) as the **enforcement plane** the round-one assemble list lacked entirely, and
  `@claude-flow/security`'s `policy/` subtree (~2,150 lines, MIT, dependency-light) as the **envelope algebra**.
  *Adopt the subtree, not the product.* Window shortened from ~6–12 months to **~3–9**: seven Cisco engineers
  have been on the exact object since April under Linux Foundation governance. **The decisive question has
  changed from "can this be built" to "why would ours be adopted instead of Cisco's."**
- **P2 — wounded further.** Leg (i)'s *strong* form — which round one left standing — now has a shipped
  instance: ruflo's Capability Brain types every tool with `loopPhases` × `authority` × `risk`. It is
  **advisory metadata, not enforcement**, so the enforcement form survives. **The novelty is not "index
  capabilities by declared phase"; it is "enforce that index."** A new leg the theme never claimed but the
  BUILD statement does — monotone attenuation — is **NOT NOVEL**. Leg (ii), gate-input independence, gets a
  **second legible negative** across 174 ADRs and both CASA implementations: still nobody states the rule.
- **P3 — reinforced and extended.** ruvnet independently wrote this theme's P3 position as a load-bearing
  code invariant two days ago (*translation MAY use an LLM; enforcement MUST NEVER*) — so the position is
  becoming the field's default, not a differentiator. **And the upstream it names does the opposite:** CASA's
  `enabledToolChecks` lets an operator select *semantic* checks — an LLM verifier on the enforcement decision —
  at a vendor-claimed >90% accuracy. On an enforcement decision, ~10% error is precisely what "a tendency, not
  a guarantee" means, and Cisco ships it anyway. **New narrowing: the field is making the determinism/inference
  boundary a configuration field, per check, set by an operator. "Minimize inference" is not a position on that.**
- **P5 — sharpened uncomfortably.** An external benchmark (ClawArena, via ruflo #2768) names privilege-granting
  the #1 orchestration bottleneck. But across 1,550 ruflo issues and ~20 metaharness issues, **not one external
  report asks for an authority bound** — every authorization item is self-filed by the maintainer or by an
  automated paper-harvesting cycle. Users report silent data loss, install timeouts, broken verification.
  **This is currently supplier-side demand.** That does not make it unreal — supplier-side demand routinely
  precedes user-side, and Cisco's investment is a real signal — but P5's evidence base is *"vendors and
  researchers agree this matters,"* not *"users are asking."*
- **P1 — one leg strengthened, verdict unchanged.** Cisco publishing TBAC research datasets in 2026 is the
  strongest artifact-side support that P1's mid-1990s cluster is real. It verifies no identifier.
  **W1 must chase TBAC by name** — it serves P1's mid-1990s leg and P2's absence claim simultaneously.

### B4. Two traps the leader must not let through

1. **"Witness" is a name collision.** ruvnet's `witness.json` is a home-grown Ed25519 manifest **with the
   verifying key inside the document** — no external trust root, so anyone can re-sign a tampered manifest and
   it verifies. W4's ASSEMBLE names TestifySec's `witness`/in-toto: DSSE envelopes, external trust root, policy
   verification, transparency log. **Merging them would silently upgrade a self-signed blob into a supply-chain
   attestation.** Not merged here; flagged for the curator.
2. **`arXiv:2606.03518`** (*"Overlaying Governance: A Compositional Authorization Framework…"*, reported to
   introduce *authorization envelopes* as first-class constructs) was surfaced from a title and URL only and
   **is not verified**. If it holds it is a direct hit on P2's envelope residual. It must not enter any
   `cites:` field until W1 fetches it. Same for `2605.05440`, `2605.28914`, `2605.22333`, `2607.19430`, which
   were read out of ruflo's own source comments.

### B5. A third emergent position, and it may be the real one

**C-4 — the theme has never priced the enforcement plane.** Every system that genuinely achieves "a plane the
principal holds no credential for" buys it with infrastructure the principal cannot reach: gh-aw pays GitHub
Actions; CASA pays Kubernetes + Istio + eBPF; `rvm` pays a hypervisor. Every system that refuses to pay —
ruflo, metaharness, coding-agent hooks, every in-process policy gate — ends up same-uid with an agent that
holds `Bash`. **Round two found no counter-example: no system enforces from outside the principal's reach
without an operator running something.**

The theme, the five positions, and JURATI's "single edge" framing are all silent on what operational cost a
guarantee is permitted to have — **and that silence is the only reason "build it" and "adopt CASA" look like
comparable options.** If the answer is "must run on a laptop with no daemon," the credential-less plane is out
of reach by construction and the whole determinism argument is downstream of a sandboxing argument. If the
answer is "an operator may run a sidecar," CASA is most of the product.

**With P6 downgraded, C-4 is the run's leading emergent position**, alongside W4's P7. It is upstream of round
one's C-1 (runtime vs compiler), C-2 (single edge vs layered) and C-3 (pluggability breaks at enforcement) —
all three are different ways of spending the same unstated budget. Relayed verbatim to the owner, unsettled.

Also carried, not promoted: **C-5** — the theme's frame is one principal per run; every shipping system is
organized around a delegation graph, and this repo is itself a five-role delegation graph with no `tools:`
frontmatter on any role. **C-6** — "cost transparency and management" is two concerns, and round two found the
second one (pre-authorised spend per unit of work, checked before dispatch) **shipping**, which corrects
wfh-004 `W0-a` a fourth time.

---

## C. Method findings — both corrections were owner catches, and that is the finding

`triage.md` §7 reported 4-of-4 surface yield as the strongest possible first result for the wf-v0.17 standard.
That stands. Two amendments to it, and one which is uncomfortable:

1. **The round-two trigger is measuring the wrong thing — now confirmed twice.** The goal-owner already argued
   it should fire on *a hole load-bearing for a verdict or a routing*, not on *a thin or empty cell*. Round two
   fired only because the owner asked, and it changed a routing. **Both of this run's verdict-moving
   corrections came from outside the method, not from inside it.**
2. **The active-development surface needs two instruments it does not have: an organization-walk and a
   deliberately low-star pass.** Round one searched by mechanism vocabulary over popular repos. ruvnet's
   ecosystem self-describes as *swarm*, *flow*, *meta-harness*, *dream cycle* — words an authorization scan
   never emits. And the find that actually mattered has **17 stars**; its predecessor has 5; the dataset repo
   has 4. **No relevance- or star-ranked search reaches them.** On this surface the incumbent's answer arrives
   at four figures of stars and the research answer arrives at two.
3. **The standard gives scouts an alias-flagging duty *across* surfaces and no instrument for aliases *within*
   one.** That is the specific gap both misses fell through.

---

## D. What stands unchanged from `triage.md`

- **P2 FALSIFIED.** Round two wounds it further; nothing rehabilitates it.
- **P4's routing: ADOPT + ASSEMBLE + BUILD.** Composition and window change; the routing does not.
- **The ADOPT caveat.** Nobody has run `gh-aw`, and nobody has run any of this. The recommendation is to
  **evaluate**, not deploy — and it remains the cheapest route to this garage's first real artifact.
- **P3's core narrowing** — position relative to a deterministic checker, not call count; plus monotonicity
  and exemption surface.
- **P1's provenance sub-finding**, and the fact that the enumerated reference list still does not exist.
- **Everything in §6** — how the wfh-004 gate should be read, including the R2 correction. Round two adds a
  fourth contradiction to `W0-a` (pre-authorised spend) and does not disturb the rest.
- **The binding constraint: wfh-004's shortlist is untouched.** Nothing promoted, parked, or re-routed.
- **The firewall.** Status moves: **0**. Every find above is `claimed`; no code was run by us.

---

## E. Open to the owner, revised

1. The four theme-revision proposals in `triage.md` §5, **plus C-4**, which now leads.
2. The two holes the goal-owner said should have been closed — commercial CD stage-scoped RBAC, and the five
   unread USPTO grants — still unspent, still under the BUILD, and now under a **two-leg** BUILD rather than
   a four-leg one, which raises rather than lowers their value.
3. **A new question round two created:** *why would ours be adopted instead of Cisco's?* This run holds no
   position on the answer and should not.
4. P1's enumerated reference list, if it survives anywhere.
