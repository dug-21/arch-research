# theme:workflow-harness — JURATI delivery/tenancy/delivery-model design space

**Status:** hypothesizer output · 2026-07-22 · structure-only, pre-triage (`claimed` at most; nothing graded).
**Provenance:** `hypothesizer` agent (Fable 5, divergent), wave-0 manual kick of `theme:workflow-harness`.
Grounded in `product/factory/themes.md` (`theme:workflow-harness`, H1–H8) + the ratified Unimatrix↔JURATI
JOINT RECOMMENDATION on `dug-21/jurati#12`.
**Not yet formalized:** no run-id/cycle/Issue (OBS-10) and no graph `finding`+`hypothesis` nodes yet —
those happen if/when survivors are promoted through goal-owner triage on a proper `theme-scan` run.

> The divergent generator maps the space; it grades nothing and decides nothing. Triage (goal-owner) +
> the human gate decide what to park/probe/build. The full raw output is preserved below.

---

## Decision under map
How JURATI is delivered/deployed/tenanted so a new project gets **day-one provisioning** (versioned
workflow → vision/capability map → building) **without** betraying the sovereignty thesis (portable graph,
pluggable/local LLM, mechanical isolation).

## The 8 axes (the real design space)
The named "models" are bundles of positions on ~8 independent axes; the answer is a *point* (or a
*trajectory*) in this space, not necessarily any named bundle.

| Axis | Range |
|---|---|
| A1. Queen execution locus | tenant laptop → tenant cloud (BYOC) → vendor cloud → split (vendor control-plane / tenant data-plane) |
| A2. Workflow-definition custody + distribution | local git → template repos → package ecosystems (npm/OCI) → community registry → vendor registry → vendor DB |
| A3. Knowledge-substrate (Unimatrix) custody | local daemon → tenant personal-cloud → vendor dedicated-per-tenant → vendor shared, slug-per-tenant |
| A4. LLM custody | local model → tenant's own key (BYO) → vendor-proxied (token margin) |
| A5. Trust-domain topology | 1 queen:1 project → 1 queen:N projects:1 domain → N tenants:dedicated → N tenants:shared |
| A6. Provisioning mechanism | git-template → CLI `init` (versioned artifact) → control-plane API → web console |
| A7. Monetization surface | OSS → support → registry/marketplace → hosted subscription → open-core enterprise → LLM-token margin |
| A8. Upgrade channel | tenant pulls a pinned version (sovereign) → vendor pushes (soft lock-in) |

**Two facts that fall out of the axes before any bundle:**
- **The Anchor-B (b) trigger is a function of A3+A5 only** — it fires exactly when one Unimatrix instance
  serves >1 trust domain, or the queen isn't provably sole client. Every other axis varies freely.
- **The day-one value prop is a function of A2+A6 only** — provisioning is a property of the workflow
  *artifact* + instantiation mechanism, not of where anything is hosted. Value and delivery model are on
  different axes.

## The 14 paths (one line each; full detail in the raw output)
- **P1 — Pure multi-tenant SaaS** (shared stack, slug-per-tenant). Max friction-kill; **crosses (b) head-on**; hosts the crown jewels; highest lock-in risk.
- **P2 — Per-tenant cells** (vendor-operated dedicated stack each). SaaS UX, single-trust-domain underneath; mostly escapes (b); ops scales ×N; shares its artifact with P9.
- **P3 — Hosted control-plane + local execution.** Vendor hosts account/registry/canvas; queen+Unimatrix+LLM local. Escapes (b) on the data plane; **H2 monetized**; risk = telemetry-protocol coupling.
- **P4 — Local-first CLI + versioned templates.** `jurati init`; all local; **zero (b)**; max sovereignty; the credibility anchor; monetization is the hard part.
- **P5 — Self-host + hosted workflow registry.** Moat moves runtime→ecosystem (H6); **new risk: workflow supply-chain**; two-sided-market cold-start.
- **P6 — Hosted queen, BYO substrate.** Own your memory, rent your brainstem; pulls (b) from the *tenant* side; worst-of-both perception risk.
- **P7 — Local queen, hosted Unimatrix.** Hosts the compounding asset (graph) — the one thing the thesis most forbids hosting; may belong to the *Unimatrix* product line.
- **P8 — Open-core** (OSS core + paid enterprise = the (b)-trigger feature set). Monetization gradient aligns with security architecture; depends on Unimatrix #5689; works best combined with P5.
- **P9 — Appliance / BYOC** (one-command stack on tenant infra). Per-project friction dies after a one-time org setup; shares artifact with P2; the enterprise landing.
- **P10 — Git-native template** (workflow = template repo + devcontainer). **Dogfoodable this week from this repo's own `.claude/`**; doubles as H4's ontology proof-direction; a wedge, not a business.
- **P11 — Federated commons** (self-hosted queens + shared upstream workflow lineage). Strongest sovereignty; the garage's own reflexive A/B method *becomes* the federation protocol; slow governance.
- **P12 — Workflows as packages on existing registries (npm/OCI + sigstore).** Supply-chain solved with existing tooling; cedes the marketplace fee; may flatten a graph-shaped definition.
- **P13 — Hosted trial → local graduation.** SaaS as onboarding funnel, not steady-state; demonstrates exportability to every user; "trial-grade isolation" is a claim needing its own proof.
- **P14 — Personal fleet: 1 queen, N projects, ONE trust domain.** Targets the stated demand driver *most literally*; **#12-blessed shape, zero (b)**; the *unit* every hosted path multiplies; concentrates blast radius as N grows.

## Compact comparison

| # | Path | Queen | Graph custody | Trust domains | Forces (b)? | Day-one kill | Sovereignty strain | Ops |
|---|---|---|---|---|---|---|---|---|
| P1 | Pure multi-tenant SaaS | vendor | vendor (shared) | many | **Yes, head-on** | Maximal | High (all 3) | vendor |
| P2 | Per-tenant cells | vendor | vendor (dedicated) | one/cell | Mostly no (vendor-ops remains) | Maximal | Medium | vendor ×N |
| P3 | Control-plane + local exec | tenant | tenant | one | No (data plane) | High after 1 install | Low–med | split |
| P4 | Local-first CLI | tenant | tenant | one | No | High (CLI persona) | Minimal | tenant |
| P5 | Self-host + registry | tenant | tenant | one | No; **supply-chain** | High | Low | vendor (registry) |
| P6 | Hosted queen, BYO substrate | vendor | tenant | one (remote) | Tenant-side prove-not-assume | Medium | Medium | split |
| P7 | Local queen, hosted Unimatrix | tenant | **vendor** | one/instance | Vendor bearer-custodian | Good | High (graph) | split |
| P8 | Open-core enterprise | tenant | tenant | one (until paid) | **(b) = the paid tier**; needs #5689 | Inherits P4/P5 | Low if export free | tenant + deals |
| P9 | Appliance / BYOC | tenant infra | tenant | one/appliance | No (until intra-org distrust) | High after setup | Low | tenant |
| P10 | Git-native template | tenant | tenant | one | No | Very high (GitHub) | Minimal | ~none |
| P11 | Federated commons | tenant | tenant | one | No; **provenance/anon** | Compounds | Lowest | community |
| P12 | Packages on existing registries | tenant | tenant | one | No; supply-chain via existing tools | High | Low | ~none |
| P13 | Hosted trial → graduation | vendor→tenant | vendor→tenant | many (transient) | Crossed; blast-radius shrunk not escaped | Maximal at trial | Honest-by-design | vendor (bounded) |
| P14 | Personal fleet (1 domain, N projects) | tenant | tenant | **one, many slugs** | **No — #12-blessed** | Total (stated persona) | None | tenant |

## Seams / non-obvious tensions (the decision-movers)
1. **"Many projects" ≠ "many tenants."** The stated demand driver (one dev, many projects, heavy per-project groundwork) is satisfied at trust-domain=1 (P14/P10/P4) with **zero deferred-security cost** — #12 pre-approved that shape. Tenancy enters only when the *buyer changes* (teams, non-self-hosters, monetization). The "SaaS decision" is really **two decisions in one coat**: how the owner's own fleet works (near-settled by #12) vs. how strangers get it (open). Conflating them imports P1's security bill into P14's problem.
2. **Value prop ⟂ delivery model.** Day-one provisioning is A2+A6; every path delivers it. "We need SaaS for the day-one experience" is falsifiable cheaply — **P10 (git-native template) is buildable from this repo's own `.claude/` in ~a week** and tests the whole value hypothesis with zero infra: the cheapest kill/confirm probe, whatever ships eventually.
3. **The Anchor-B bill is a step function that lands partly on the other crown.** (b) triggers on one condition (one Unimatrix instance >1 trust domain / unprovable sole-client); when triggered, the *verifier* is Unimatrix's L2 seam (#5689/ass-102), JURATI supplying issuer policy. Any tenancy choice crossing the trigger makes JURATI's delivery **schedule-dependent on the Unimatrix roadmap** — real sequencing, not just governance.
4. **Whoever hosts the graph becomes the lock-in vendor.** Data gravity is in the knowledge substrate, not the queen. Paths hosting Unimatrix (P1/P2/P7) owe *continuous mechanical* export (tenant-held replica) — a manual "export button" under commercial gravity is the honor-system the vision forbids, applied reflexively to JURATI.
5. **Two unnamed lock-in vectors:** (i) vendor-proxied **LLM token margin** (A4) — BYO-key/local must stay first-class or pluggability decays into a pricing tier; (ii) **vendor-push upgrades** (A8) — soft lock-in that survives even fully-local deployment; pull-with-pinning (this factory's own semver discipline) is the sovereign default.
6. **Distribution creates a supply-chain surface bigger than the tenancy one.** A versioned workflow is *executable authority* (it programs agents with gates/permissions). In registry/commons paths (P5/P11/P12) a malicious artifact is a deeper compromise than cross-tenant access — and it lands on the **most** sovereign paths. Signing/provenance (sigstore-class) is foundation work **not** on the Anchor-B list and in **no** seed hypothesis.
7. **Provisioning has COGS.** "Day one it builds your capability map" = LLM calls at signup. Vendor-token paths burn money per curious visitor; BYO/local paths move cost+friction to key-setup. A minute-zero billing/key handshake is a seam every hosted path must design.
8. **Packaging back-pressures the ontology (H4/H7).** Shipping workflows as artifacts (P5/P10/P12) forces the definition to become serializable/versioned early (enforces H7) — but flat package formats can calcify a file-shaped schema that fights H1's workflow-as-graph. Delivery choice is quietly an ontology-sequencing choice.
9. **Trajectory beats point-choice.** Bundles compose over time: P10/P4 (credibility+dogfood) → P5/P12 (distribution) → P3 (hosted canvas = H2 monetized) → P8 (enterprise = the (b) trigger *as* price list) → P2/P9 (cells/appliances); P13 top-of-funnel, P11 long-game moat. Several paths share artifacts (P2≡P9; P4⊂P3; P13→P10). Triage may score *sequences*, not points.

## Flags for triage
- Input leaned **owner-injection** (ratified architecture + H1–H8). An **external scan** of how comparable products actually deliver (Cursor local/cloud split, Devin hosted, OpenHands OSS+cloud, Replit Agents, HashiCorp registry economics + BSL backlash) would pressure-test P3/P5/P8/P13 against market reality — out of scope for this pass.
- **P13's "trial-grade isolation"** and **P6's tenant-side trust** are the two paths whose security stories most need their own cheapest-test before any weight is put on them.
- Seam #2 names the cheapest global probe: **P10 template from this repo's own context** — kills or confirms the value hypothesis independently of the tenancy decision.
</content>
</invoke>
