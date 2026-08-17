# scout-adjacent.md — AMENDMENT 1 (self-hosted cluster returned)

**Run:** wfh-007 · Issue #64 · surface **S4 — adjacent prior art** · mode DISCOVERY · `wf-v0.24`
**agent_id:** `wfh-007-s4-scout` · read-only on Unimatrix, zero writes

> **Leader's note on file structure.** S4's return arrived as this amendment; the base
> `scout-adjacent.md` it amends was requested separately and is filed alongside. Read the base first
> for the original Axes A/B/C and candidates C1–C15; this amendment **corrects three of them**. The
> clinical-EDC portion of job (b) is filed as `scout-adjacent-annex-clinical-edc.md` (a sub-agent
> return that reached the leader directly when its peer was unreachable).

The hole declared in §4.2 is now closed, and it does not merely fill in — **it corrects Axis A, sharpens Axis B into a measured number, and adds a live find twelve days old that sits directly on this run's thesis.** All figures below are the agent's own reproducible measurements taken 2026-08-17 against git trees and public APIs, not published claims.

## A1. Three corrections to my own §1

**A1.1 — Axis A is wrong as a universal. Catalogue growth does not saturate; review capacity is the only ceiling.**

Home Assistant integration count, measured from git trees at release tags: **877 (Oct 2019) → 1,116 (Dec 2022) → 1,303 (Dec 2024) → 1,482 (Aug 2026).** That is **linear at ~+100/year for seven consecutive years with no slope change**, through a 70% increase in count. Over the last 12 months: **16,716 commits, 1,220 distinct commit authors, 14,326 merged PRs (~39/day)**, against a backlog of only 1,023 open PRs. All-time unique authors: 5,682.

So the corrected form of Axis A is: **third-party authorship absolutely can start and scale — it did not in any of the failed cases, and the discriminator is the review gate, not a ceiling on domains.** The cross-project table makes it unambiguous, because the unit of extension is *nominally identical* (a compose file) across four of these:

| Project | Catalogue | Distinct catalogue authors, 12 mo | Merged PRs, 12 mo |
|---|---:|---:|---:|
| Home Assistant core | 1,484 (+3,105 HACS, +4,245 registered brands) | **1,220** | **14,326** |
| Umbrel | 391 | 120 | 2,134 |
| Nextcloud | ≥583 (446 NC-31-compatible) | 160 | — |
| YunoHost | 704 | 49 | 408 |
| CasaOS/ZimaOS | 166 (+244 third-party) | 16 | 125 |
| Cloudron | 194 | **2** (the company) | — |
| **Sandstorm** | **98 (frozen)** | — | **9 commits total in 2026** |

**And when the first-party gate throttles, the ecosystem routes around it:** Big Bear's third-party CasaOS store (244) is *larger* than the official one (166); HA's third-party ecosystem (3,105–4,245) is 2–3× its first-party one.

**A1.2 — Axis B now has a measured price, and it is the most decision-relevant number in the amendment.**

HA's ADR 0022 (2024-11-20) introduced a Bronze/Silver/Gold/Platinum quality scale and **explicitly reset every existing integration to zero**, requiring voluntary re-certification by PR. Measured 21 months later across all 1,484 manifests:

| Tier | Count | % |
|---|---:|---:|
| *no `quality_scale` field* | **708** | **47.7%** |
| `legacy` / `internal` (non-scaled) | 484 | 32.6% |
| bronze / silver / platinum | 279 | 18.8% |
| **gold** | **13** | **0.9%** |

**Only 19.7% hold any scaled tier after nearly two years; gold has thirteen members.** This is as close to a controlled measurement as this surface will ever produce of the cost of retrofitting governance onto an existing catalogue. **Stated as the axis: an authority layer must be present at capability 1, or it recruits about a fifth of capability N.** Nextcloud's Config Lexicon (server 32.0.0, 2025) and ownCloud/Kiteworks' new per-app signing PKI (2026) are the same late move at the same late stage.

**A1.3 — Axis C is right about custody and wrong about representation being a bottleneck.**

HA's **ADR 0010 (2020-04-14)** forced UI-only configuration for device/service integrations, and its own Consequences section predicted the risk in writing: *"This might impact the number of integrations contributed. This requires configuration flows, which require tests."* **It did not.** From 18 months post-ADR to today: **+582 integrations, −115 removed**, slope unchanged; `config_flow` now on 920 of 1,484 manifests.

**Corrected Axis C: the config representation was never the constraint — config *ownership* was.** What let HA scale is moving configuration out of user-authored text into a typed, migratable, **machine-owned** store (`.storage/core.config_entries`, `STORAGE_VERSION_MINOR = 5`, with a mandated `async_migrate_entry` path and integrations forbidden from mutating entries directly), plus six sibling registries in which areas/floors/labels/categories form a genuinely *user-owned* organisational layer above the machine-owned device layer — and, decisively, **ADR 0021's user-facing repair channel**: a mandatory 6-month deprecation, automated migration where possible, and an in-product repair issue raised in the user's dashboard when config goes stale. **That last mechanism is the piece every other system in this cohort lacks entirely.**

NixOS is the counter-case that proves representation is not the limit: **24,502 typed options — the richest in the scan — covering ~2,200 programs against 118,005 packages, i.e. ~1.9%.** And 84% of those options sit under `services.*` — it is a *server* `/etc`. Its binding constraints are coverage and the boundary: **secrets cannot live in the model at all** (agenix's README: *"All files in the Nix store are readable by any system user"*), so both sops-nix and agenix decrypt at activation, bolting a second imperative plane onto the declarative one.

## A2. Sandstorm — Axis B's direct test, and the answer is *porting cost*, not user rejection

I named this the hole I most regretted. It closes cleanly, and it substantially exonerates the security model.

**Varda's primary accounts (2017-02-06 and 2024) never name the capability model as the cause.** He names: *"Sandstorm the business has now run out of money"*; *"almost no one has purchased Sandstorm for Work, despite hundreds of trials"*; the product being *"still alpha-quality"*; and *"We underestimated, in classic fashion, the challenge of enterprise sales — we never managed to do a 'real' sales call."* Two sales ever, four figures. **Cloudflare acquired the team for $0** (March 2017) with good offers for everyone; the entity dissolved in 2022; Varda maintained it nominally until Jan 2024. The long tail was dependency rot (stuck on MongoDB 2.6, which blocked Meteor, which blocked everything) and then the loss of the one regular outside contributor, Ian Denhardt, who forked to a rewrite in late 2022 **and died in an accident in mid-2023**.

**But the porting cost is undeniable and is the mechanism.** To be listed, an app had to: **rip out its own user accounts and access control** (trusting `X-Sandstorm-User-Id` headers); work immediately with no setup or database provisioning; reorganise so each grain is one document; and hand-implement the Powerbox `postMessage` RPC for any external access, because *"A Sandstorm app, by default, is totally isolated from the network. It cannot connect to anyone."* Varda's own 2014 framing — *"The modifications needed for typical Linux web apps tend to be light, but they are necessary"* — understates a rewrite of an app's identity, tenancy, storage and networking layers.

**Sandstorm shipped 98 apps, ever.** Core commits per year: 679 (2014) → 2,922 (2016) → **488 (2017)** → 9 (2026).

**The corrected Axis B statement: nobody in this cohort was killed by users refusing security. The strong-authority systems were priced out on the supply side — the reviewer (Cloudron: 194 apps, two people, 9–26/yr for eleven straight years) or the porter (Sandstorm: 98 apps, ever).** Compare directly on one primitive — the Docker socket: **Cloudron mediates it as a fenced capability with a superadmin install gate; Umbrel bans it in prose and 2 of 391 apps do it anyway; CasaOS has 6 of 166 mounting it with no comment; Home Assistant has no concept that could express the question.**

## A3. Two findings that were not in my assignment and that I think outrank most of it

**A3.1 — The only per-app capability scoping Nextcloud ever shipped was deleted for latency.**

AppAPI shipped `ApiScopes` — typed per-app capabilities (`TEXT_PROCESSING`, `MACHINE_TRANSLATION`), an `ex_app_scopes` table, an `occ app_api:scopes:list` command. Then, CHANGELOG v3.2.0, 2024-09-10: **"ApiScopes are deprecated and removed. #373"**, with the stated rationale *"unnecessary stuff removal to **reduce the number of requests during AppAPIAuth**."* Worse, a successful ExApp auth now sets a session key that **bypasses CORS, two-factor authentication and rate limiting**, with the documented mitigation being *"Deploy only trusted ExApps."*

**Capability checks lose to p99 latency unless they are structural.** For a run weighing a capability vocabulary as a load-bearing component, that is a named, dated, sourced failure of exactly that component under production pressure.

**A3.2 — Three credible projects placed three incompatible bets on agents within ten weeks, and this repo is a fourth.**

- **Umbrel (June 2026)** replaced its packaging documentation with agent skills. Commits `e0a982b8` (2026-06-18) and `263b3f73` (2026-06-25); the README now reads *"The easiest way to contribute is to send your coding agent to this repository and have it read `AGENTS.md`"*, routing to `.claude/skills/`, where `umbrel-package-app/SKILL.md` is **395 lines and is now the authoritative manifest contract** — the human-facing README no longer documents the fields. It coincides with Umbrel's steepest growth segment (+81 apps in H1 2026 vs +71 in H2 2025; two months of overlap, so not causation). **Structural hazard, stated plainly: the security boundary and the instruction to the agent are the same document.**
- **Cloudflare OS (`cloudflare/cloudflare-os`, created 2026-04-15, open-sourced Apache-2.0 on 2026-08-05, 8,487★)** is **Sandstorm's architecture restated, unchanged, with the porting cost removed.** Grain → **gadget**; Powerbox → **Gatekeepers**; the same sandboxed-iframe `postMessage` RPC (now Cap'n Web). README: *"Each agent, and each Gadget, by default has access to nothing… you must introduce each agent (or Gadget) to any particular resources you want it to access,"* and *"While you can code a Gadget by hand if you want, **the expectation is that AI writes the code for you**."* Varda: *"more or less the culmination of my secret 10-year master plan."*
- **Home Assistant (2026-07-20)** went the opposite way and **bans autonomous agents outright**: *"We do not allow autonomous agents to be used for contributing to our projects. We will close any pull requests or issues that we believe were created autonomously"* — on the explicit ground that *"maintainer time is the scarcest resource an open source project has."*

**Cloudflare OS is the single most consequential find in this scan and it is twelve days old.** It is a direct, funded, open-source instantiation of the thesis this run is circling: a capability-secured personal computing layer whose extension unit is written by a model rather than ported by a human. **The capability model was never falsified — what was falsified was the assumption that humans would port applications into it, and that assumption is exactly what changed.**

*Caveat, flagged:* Varda's 2026 retrospective quotes ("the world wasn't ready," the skill/patience thesis) come from secondary AI-adjacent coverage and an unfetchable X thread; the Cloudflare blog post (Jones; Carter) does not mention Sandstorm. **Treat those as unverified.** His 2017 and 2024 first-person accounts, quoted in A2, are primary.

## A4. One number that reframes what an extension catalogue is *for*

Of HA's 1,359 integrations reporting usage across 529,561 installs: **80% of all integration installs are covered by the top 84.** Only 16 are used by ≥50% of installs. **54.5% have fewer than 500 installs; 11.4% have fewer than 10; twenty report exactly 1.** Average integrations per install: **29** — the median user touches **~2% of the catalogue**.

**A catalogue of this shape is a coverage lottery, not a feature set.** Its value is the probability that *your particular* device is covered, which is the only reading under which maintaining 740 entries with sub-500 users is rational. HA pays for it visibly: **396 integrations (26.7%) have no code owner and are carried by the core team**, 58% are outside `.strict-typing`, 30.7% got ≤5 commits in a year — and yet 100% were touched, because global refactors drag the whole catalogue along.

## A5. Amended candidates

| # | Candidate | Why it matters | Dedup |
|---|---|---|---|
| **C16** | **Cloudflare OS** (`cloudflare/cloudflare-os`, Apache-2.0, 2026-08-05) | Sandstorm's capability architecture with an AI-authored extension unit. **The live instance of this run's thesis.** | **NEW — and near-certain to be S1's headline too; merge, do not double-count** |
| **C17** | **HA config entries + ADR 0021 repair channel** | Machine-owned typed config store with mandated migration *and an in-product user-facing repair issue*. The `/etc` mechanism that demonstrably scaled | **NEW.** S2 will find this as a Home Assistant feature — **same object as my Axis C** |
| **C18** | **Cloudron addon model** | The strongest shipped per-app capability system in the cohort — fenced `docker`, isolated per-app DBs, `ldap` that cannot be added to an existing app. **63% of apps opt into a managed identity addon** | **NEW** |
| **C19** | **YunoHost `[resources]` + `config_panel.toml` `bind`** | Declarative provisioning executed by the *core*, and the only system that **types the upstream app's native config file in place** (YAML/TOML/JSON/INI/PHP/.env/Python) rather than replacing or ignoring it. Also: repo custody is a *scored quality property* (level 6) | **NEW** |
| **C20** | **Umbrel's agent-skill packaging contract** | The extension contract as a 395-line `SKILL.md`. **Direct dogfood adjacency** — this repo runs the same pattern | **NEW** |

## A6. Amended flags for the leader

1. **Axis A is corrected, not withdrawn.** The wall at domain 1 holds for every *failed* case; the survivor shows the curve is linear and uncapped when the review gate is open. **The discriminator is reviewer throughput, not domain count** — which means the criticality report should ask "who reviews domain N+1," not "how many domains."
2. **Axis B now carries a number: 19.7% / gold=13 after 21 months.** Retrofitted governance recruits about a fifth of an existing catalogue. Present at capability 1, or not at all.
3. **Nextcloud deleted its only per-app capability scoping to save request latency.** Put this beside the framing's capability-vocabulary component; it is the sharpest counter-evidence on this surface.
4. **Cloudflare OS (12 days old) is the run's most consequential external event** and it revives, not refutes, the capability model — by removing the porting cost. **Expect S1 to surface it; reconcile, do not count twice.**
5. **HA bans autonomous contribution; Umbrel made agents the primary contributor; Cloudflare OS makes the model the author.** Three incompatible bets in ten weeks, and this repo has a stake in the answer.
6. **Sandstorm exonerates the security model and convicts the porting cost.** Varda's primary accounts name money and enterprise sales, never capabilities.
7. **Residual holes after this amendment:** rail interlocking (still, from wfh-005); patent prior art (still); Manifest V3 developer attrition; Android permission-vocabulary growth; Jibo. The WebSearch budget (200/200) was exhausted across the whole session — **neither job is exhaustive, and the bias runs against exactly the discoverable small-project sources a low-star pass would want.**
