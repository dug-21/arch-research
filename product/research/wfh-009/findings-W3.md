# wfh-009 — findings W3: host projection, SDK surface, and vertical contracts

**Workstream question.** How is one definition projected onto many heterogeneous hosts, what is lost in each projection, and how is that loss represented — the portable half of "build once, run under any harness"?

**Target pin (confirmed by me):** `git -C /tmp/wfh-008-metaharness rev-parse HEAD` → `6f8c60216f47eac391a076fe27fd804470a07e10`. Static reading only. Nothing was installed, built, run, generated or fetched. **Nothing here is demonstrated-by-us evidence; nothing reaches `partial` or `proven`.**

**Packages owned.** Tier 1 (8, binding): `host-codex` · `host-copilot` · `host-hermes` · `host-openclaw` · `host-pi-dev` · `sdk` · `vertical-base` · `vertical-trading`. Tier 2 (5, non-binding): `host-claude-code` · `host-github-actions` · `host-opencode` · `host-prime-agent` · `host-rvm`.

**Headline.** `#316` records "stable definition → shared IR → host projections **with explicit loss reports**" as a portable concept taken from MetaHarness. Measured against the code: **the projection contract has no channel in which a loss could be reported, and 1 of 10 adapters reports loss at all.** The IR is not host-neutral — it is Claude Code's configuration schema promoted to shared status — so the loss is asymmetric by construction. That is the correction this workstream returns.

> **Persistence note (leader).** The authoring `factory-researcher` was blocked by the harness from writing this file directly and returned it verbatim. It is transcribed here unaltered by `research-leader`; no content was generated, summarised or edited in transit.

---

## 1. Declared alphabet (C6 / `#323`) — stated before any completeness claim

I swept the **question set** — *what a harness definition can express* × *what each host can receive* — not the set of adapters already named.

### A1 — what a definition can express (the shared IR's field set)

```bash
sed -n '31,51p' /tmp/wfh-008-metaharness/packages/kernel-js/src/types.ts \
  | grep -oE "^  [a-zA-Z]+\??:" | tr -d ' ?:'
```
→ `name description systemPrompt mcpServers tools agents hooks permissions statusLine autonomous` (10)

```bash
sed -n '49,58p' /tmp/wfh-008-metaharness/packages/sdk/src/index.ts   # author-facing HarnessDef
```
→ `name description systemPrompt agents skills tools hooks mcpServers` (8)

**Declared boundary crossing, stated rather than hidden:** `packages/kernel-js/` is outside my package list (wfh-008 examined it). I read exactly **lines 25–57 of `packages/kernel-js/src/types.ts`** — `HookSpec`, `HarnessSpec`, `HostAdapter` — because the projection contract cannot be stated without them, and nothing else in that package. I re-derive none of wfh-008's kernel ground; see `#316`/`#317`.

### A2 — what each host actually receives (consumption + emission)

```bash
cd /tmp/wfh-008-metaharness/packages
grep -ohE '\bspec\.[A-Za-z_]+' host-*/src/index.ts | sort -u          # fields read
for p in host-*; do awk '/generateConfig/,/^};/' $p/src/index.ts \
  | grep -ohE "'[^']*\.(json|toml|yaml|yml|md|sh|ts|py)'" ; done       # artifacts emitted
grep -rnE "\(spec as |as \{ claims" host-*/src/index.ts               # out-of-band fields
```

### A3 — the ecosystem test (C2), run at mechanism level

```bash
grep -rihoE "ruflo|RUFLO_[A-Z_]*|@ruvector|ruvector|claude-flow|agentic-flow|ruvnet" \
  <pkg>/src <pkg>/README.md <pkg>/package.json
```
…then, for every hit, the question asked was *"does the IDEA need this, or does this implementation merely sit on it?"* — never *"does the manifest name it?"*

### What this alphabet cannot see — stated, not implied

- **Runtime.** Every statement is about emission. No host was installed, no config loaded, no refusal exercised. An adapter that emits a config file is evidence of **emission**, never that the host **honours** it.
- **The generator.** Adapter selection, ordering and merge behaviour sit in `create-agent-harness` / `agent-harness-generator-lib` — wfh-008's ground, cited not re-derived.
- **The out-of-tree ADR corpus.** 11 of 13 packages cite internal ADR numbers resolving to `github.com/ruvnet/agent-harness-generator/docs/adrs/` — **a different repository**. Declared origin recorded (§5); **not fetched**.
- **Published state.** No package sets `private:`. Per `#324`: *publishable* and *release-ordered* are not *published*; a registry fetch is forbidden.
- **Dynamic surfaces**, generated harnesses, out-of-repo consumers — same limit `#319` §8 records.

---

## 2. The measured loss matrix — the workstream's primary evidence

**[static code evidence]** `✓` = the field reaches an emitted artifact; `—` = read by no code path in that adapter.

| IR field | codex | copilot | hermes | openclaw | pi-dev | cc | gha | opencode | prime | rvm | **hosts reached** | in `sdk`? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `name` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **10/10** | yes |
| `systemPrompt` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **10/10** | yes |
| `description` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | 9/10 | yes |
| `agents` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | 8/10 | yes |
| `mcpServers` | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓\* | — | 8/10 | yes |
| `permissions` | — | — | — | **—** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6/10 | **NO** |
| `tools` | — | — | — | — | ✓ | — | — | — | ✓ | — | 2/10 | yes |
| `hooks` | — | — | — | — | — | ✓ | — | — | ✓† | — | 1/10 | yes |
| `statusLine` | — | — | — | — | — | ✓ | — | — | ✓† | — | 1/10 | **NO** |
| `autonomous` | — | — | — | — | — | — | — | — | ✓ | — | **1/10** | **NO** |
| `claims` | — | — | — | — | — | — | — | — | — | ✓‡ | 1/10 | **NO** |
| **`skills`** | — | — | — | — | — | — | — | — | — | — | **0/10** | yes |

\* remote HTTP only; stdio explicitly declared unsupported. † read **only** to declare unsupported — the honest case. ‡ not a declared `HarnessSpec` field; read through a cast (C9).

Three facts, each verified by grepping every adapter at once (`#324`):

1. **`spec.skills` is read by zero adapters.** `grep -nE "spec\.skills" host-*/src/index.ts` returns nothing. `sdk` exports `defineSkill`, `SkillDef`, `HarnessDef.skills`; the skill vocabulary reaches no host. `host-openclaw/src/index.ts:23` states it emits "`SKILL.md` file per kernel skill" [source claim]; `skillMarkdown(spec)` (L88–124) emits exactly **one** harness-level file and never touches `spec.skills` [static code evidence].
2. **The security vocabulary is unreachable from the SDK.** `grep -icE "permission|statusLine|autonomous|claims|deny|allow" sdk/src/index.ts` → **0**. `defineHarness` cannot express `permissions`, `statusLine`, `autonomous` or `claims` — the four fields every control-shaped projection depends on.
3. **`autonomous` is silently dropped by 9 of 10 adapters**, against an explicit written obligation. `kernel-js/src/types.ts:42-43`: *"Host adapters must project this block per host or emit an explicit documented no-op — **never silently drop**."*

---

## 3. The projection contract, and why the obligation is unenforceable

**[static code evidence]** `kernel-js/src/types.ts:53-57`:

```ts
export interface HostAdapter {
  name: string;
  /** Return a map of file-path -> file-content for the host's config. */
  generateConfig(spec: HarnessSpec): Record<string, string>;
}
```

Two members. **No residual, no diagnostic, no coverage set, no refusal.** The "never silently drop" rule is a comment on a *different* interface, with no type in which a drop could be expressed. Compliance is per-adapter discipline, invisible to the compiler, measured at 1/10.

The one compliant adapter shows compliance is cheap — `host-prime-agent/src/index.ts`: L419–436 an **"Unsupported on this host"** section, *"listed here so nothing is silently dropped"*; L505–508 `SANDBOX-REQUIRED.md` emitted **iff** `permissions.deny` is non-empty — a conditional artifact whose *presence* is a machine-checkable loss signal; L27–31, L151–155 refusal to fabricate an execution target. All three live in **prose files**, not in the return type.

---

## 4. Concept register — 10 concepts (4 `new`, 6 `sharpens`)

### C1 — A projection contract must carry a residual channel, and total coverage must be a checkable closure

1. **Concept.** Define the projection from a portable definition to a host as a **total** function returning artifacts *and* the enumerated residual — every definition element the host cannot receive, with a reason code. Make `projected ∪ residual = definition` a mechanically checked closure at build time; an element in neither set is a build failure. The residual is structured data, not prose, so a deployment gate can read it.
2. **Why it matters.** Enforcement outside the governed party's reach requires knowing *which plane will enforce what*. An author who declares a deny-list and receives no residual cannot distinguish "enforced by the host" from "written to a file nothing reads." Silent loss of a control is indistinguishable from a control — the exact condition `#318`'s predicate exists to detect.
3. **How.** Jurati's definition compiles to N projections, each returning `{artifacts, residual[]}`. The deploy gate refuses any projection whose residual contains an `enforcement`-tagged element. `SANDBOX-REQUIRED.md` becomes a *derived* artifact of a non-empty enforcement residual, not a one-adapter special case.
4. **Novelty.** `sharpens #316`. `#316` records loss reports as a concept *taken from* MetaHarness. Correction: MetaHarness's contract has **no** loss channel, and the loss report exists in 1 of 10 adapters as generated Markdown. The concept is right; `#316`'s attribution reads stronger than the code supports.
5. **Custody verdict.** *Not control-shaped* — a completeness discipline. It is the **precondition** for the custody predicate being answerable: without a residual you cannot tell which controls survived the projection.
6. **Evidence.** static code evidence (contract shape; the §2 matrix; `host-prime-agent` L419–436, L505–508) + source claim (`kernel-js/src/types.ts:42-43`).
7. **Provenance.** `host-prime-agent` declares **ADR-247 §2.2**, **ADR-044**; the obligation cites **ADR-246 §2.2**. ADRs resolve to `github.com/ruvnet/agent-harness-generator/docs/adrs/` — **not read**.

### C2 — A shared IR derived from one host's schema relocates lock-in rather than removing it

1. **Concept.** When the portable representation is lifted from the richest incumbent host's config format, portability is an illusion with a measurable shape: the donor host is lossless by construction and every other host is a lossy translation whose loss is nobody's declared responsibility. Derive the vocabulary from *operating semantics* instead, and admit no element until **≥2 structurally dissimilar hosts** can receive it — a two-host admission rule for the ontology itself.
2. **Why it matters.** The direct test of **H5** (anti-lock-in as a *consequence* of a portable representation). H5 holds only if the representation is genuinely host-neutral. If the IR is one vendor's config schema, swapping the executor does not swap only the executor — it silently drops whatever the donor expressed and nobody else does. Here that is the entire hook and permission surface.
3. **How.** Under a two-host rule, `hooks` would not have been admitted in this shape: receivable by 1 of 10 hosts.
4. **Novelty.** **`new`.** `#316` treats the IR as a portable asset; `#317` covers closed surfaces; neither states the IR's *vocabulary* is one host's schema, nor that this makes the loss asymmetric by construction.
5. **Custody verdict.** *Not control-shaped* — an ontology property. Its consequence is control-shaped: the elements failing to project are disproportionately the enforcement elements (`permissions` 6/10, `hooks` 1/10, `statusLine` 1/10, `autonomous` 1/10), because those are exactly what the donor host has and others do not.
6. **Evidence.** static code evidence:
   - `sdk/src/index.ts:37` — `HookDef.event` is a closed union of ten literals: `SessionStart | UserPromptSubmit | PreToolUse | PostToolUse | PostToolUseFailure | Stop | SubagentStart | SubagentStop | FileChanged | Setup`. `host-claude-code/src/index.ts:13-14` documents Claude Code's event set as **the same ten names**.
   - `kernel-js/src/types.ts:39` — `permissions?: { allow?: string[]; deny?: string[] }`, pattern dialect Claude Code's (`Bash(rm:*)`, `mcp__srv__*`), per `host-claude-code:18` and `host-rvm:121-123`.
   - `host-claude-code/src/index.ts:82` — `permissions: spec.permissions` is a **verbatim pass-through**. The only adapter performing no translation, because for it the IR *is* the native format.
   - `statusLine`, `mcpServers` are likewise Claude Code surface names.
7. **Provenance.** None declared. No package states the vocabulary derives from Claude Code; identity is inferred from the literal name sets — graded on static evidence, not on a claim.

### C3 — Name normalisation in a projection is non-injective, and silently drops the loser

1. **Concept.** Every projection narrows an identifier charset (`^[a-z0-9-]+$`, ≤64 chars). Narrowing is non-injective: two distinct elements can normalise to one host name, and a flat destination map then **silently overwrites** — one element vanishes with no error, diff, or loss report. Treat identifier normalisation as a first-class lossy step: restore injectivity deterministically, and record every collision in the residual, because a renamed element and a dropped element are indistinguishable downstream.
2. **Why it matters.** Enforcement is addressed **by name**. If a deny rule and an allow rule normalise to one identifier, whichever is written last wins. A control lost to a charset collision is a control the governed party can *cause* — by choosing a name that collides with the rule constraining it.
3. **How.** One shared normaliser returning `(name, collidedWith?)`; any collision is a residual entry; a collision on an enforcement-tagged element is a hard build failure, never a suffix.
4. **Novelty.** **`new`.** Nothing in `#200 #277 #316 #317 #318 #319 #323 #324 #325 #326` covers identifier-space narrowing as a loss channel. Adjacent to `#323` but distinct: `#323` is about a *sweep's* vocabulary being unstated; this is about the *output* vocabulary being narrower than the input's in a mapping believed total.
5. **Custody verdict.** *Fails on input* where colliding names are author-supplied — which they are: `spec.tools[].name`, `spec.agents[].name`.
6. **Evidence.** static code evidence — `host-prime-agent/src/index.ts:81-97`, which names the class itself: *"'My Tool' and 'my_tool' → 'my-tool'; a flat Record would then silently overwrite the earlier entry — the ADR-046 silent-drop bug class"*, mitigated by `uniqueSkillName()` with deterministic spec-order suffixing. It is the **only** adapter that does this; `normalizeSkillName` (L57-79) is the narrowing step, and the other nine interpolate names into paths and keys with no collision check. Note `sdk`'s `defineHarness` (L126-136) checks agent and skill name collisions but **not** tool names.
7. **Provenance.** **ADR-046** (named in-repo as a bug *class*), **ADR-247**. Not read.

### C4 — The generated human runbook drifts from the generated machine config, and the human executes the stale one

1. **Concept.** A projection emits at least two artifacts with different consumers: machine-readable configuration, and a human-executed install runbook. They are generated from one source, corrected independently, and only the machine-facing one is corrected. The human then installs against a key the host does not read, and the configuration is inert while appearing installed. Derive the runbook's key names and paths **from the emitter**, never restate them in prose.
2. **Why it matters.** For a substrate whose enforcement must sit outside the governed party, the install step is frequently the *only* moment a human is in the loop. A stale runbook converts that one human control into a no-op, invisibly — the human reports "installed."
3. **How.** Render the runbook from the same structured record the config is serialised from; a test asserts every literal path/key in a runbook also appears in that projection's emitted artifact set.
4. **Novelty.** **`new`.** `#324` covers an *auditor* failing to re-read the sentence beside a verified one. This is the same shape in *generated* artifacts — a correction applied to the emitter and not to the prose the emitter also emits.
5. **Custody verdict.** *Fails on custody* in the sense that matters: the stale instruction directs the human to write into a location the host ignores, so no enforcement lands anywhere.
6. **Evidence.** static code evidence, all instances ruled at once (`#324` by-fact):
   - `host-openclaw`: `configJson` emits `{ mcp: { servers } }` (L79) because ADR-046 found the top-level `mcp_servers` shape *"was REJECTED — `config validate` reported `<root>: Invalid input`"* (L35). The **same file's** generated install script still instructs merging *"into ~/.openclaw/openclaw.json under `"mcp_servers"`"* (L144) — the rejected key.
   - `host-opencode`: L59-61 records real opencode 1.17.7 has **no** `mcp.permissions` key (*"it parsed our old one as a malformed MCP server"*); the emitter writes a top-level `permission` block (L99). The generated runbook still states *"The `mcp.permissions.deny` block is enforced BEFORE `allow`"* (L177-178) — an enforcement semantic for a key not emitted and not existing.
   - `host-pi-dev`: `README.md` lists three emitted files; `generateConfig` emits **four** — `trust.json` (L109) is absent from the README.
   - **Negative scope:** not checked in `host-codex`, `host-copilot`, `host-claude-code`, `host-github-actions`, `host-prime-agent`, `host-rvm` beyond the §1 A2 key grep.
7. **Provenance.** Both primary instances declare **ADR-046**. Not read.

### C5 — The governed party authors not only the control's input but the control's own parameters

1. **Concept.** `#318` says a control whose *input* sits inside the governed party is a label. The sharper statement: the governed party routinely authors the control's **configuration** — its trust grant, its required assurance level, its own pass predicate. Each is a *parameter* rather than an input, each is defeated by editing a value rather than defeating a mechanism, and each reads as *stronger* protection because it is expressed in security vocabulary.
2. **Why it matters.** The failure mode most likely to survive review of Jurati's own design, because the artifact *looks* like a capability system. A capability table with rights, expiries and proof tiers, generated from a file the holder writes and installed by a script the holder runs, is a self-issued credential wearing a capability system's clothes.
3. **How.** For every control name three parties separately — who supplies the input, who holds the artifact, **who sets the strength parameter**. If the third is the governed party, the control's strength is whatever that party chooses. Trust grants and assurance levels are issued by the plane that enforces, never carried in the applicant's payload.
4. **Novelty.** `sharpens #318`. `#318` records inputs, custody, call-site enumeration, and notes generated host permissions "generally live in project-controlled files." The sharpening is the **fourth face** — the control's own parameters — with three independent instances, in a supply-chain setting `#318` did not cover.
5. **Custody verdict.** Three instances:
   - **Self-issued trust grant** — `host-pi-dev/src/index.ts:79-100`. Pi *"gates extension tool execution behind a trust file"*; the adapter emits `trust.json` listing the harness's own extension as trusted *"so `pi install npm:<harness>` is trusted out of the box (rather than every tool prompting)"*. The applicant writes its own admission record. **Fails on input and on custody.** The host's consent prompt — the only independent step — is what the projection is designed to remove.
   - **Self-declared assurance level** — `host-rvm/src/index.ts:93-97, 106-117, 151-165`. Each emitted token carries `proof_tier` — *the verification strength required to exercise it* — computed inside the generated table. Default path: no issuer, no signature, `expires_at = DERIVED_CLAIM_EXPIRY = 0` ("non-expiring"), derived from `spec.permissions.allow`. README claims *"same security model, stronger backend"* [source claim]; the default path produces unsigned, non-expiring, self-scoped, self-graded tokens. **Fails on input and custody.** Widening is the default: `rightsFromPermission` (L128-136) falls through to `['EXECUTE']`, and `*` yields all seven rights including `GRANT`/`REVOKE`.
   - **Self-administered publish gate** — `vertical-base/src/index.ts:95-115` supplies `verifyTemplateFilesPresent()`, documented as *"Pack authors run this at publish time to catch dangling references before they ship."* The gate ships as a **library the gated party calls**. `vertical-trading/__tests__/pack.test.ts:24-35` is the call site, titled *"every template file referenced by manifest must exist (publish-gate)"* — and it **passes when the gate fails**: `if (!r.ok) expect(r.missing.length).toBeGreaterThan(0)`. All ten `.tmpl` files are absent (`find` returns only `templates/manifest.json`); `files: ["dist/**","templates/**","README.md"]`; the package is in `RELEASE_ORDER`. **Fails on input and on call-site enumeration.** Per `#324`: *packed* and *release-ordered*, **not** *published*.
6. **Evidence.** static code evidence throughout; the RVM "same security model" line is a **source claim**. Nothing was executed.
7. **Provenance.** `host-pi-dev` **ADR-044**, **ADR-022**; `host-rvm` **ADR-011**, **ADR-022**, **ADR-044**; `vertical-base` **ADR-013**. Not read.

### C6 — A projection between two permission algebras must be proved non-widening, and none of these is

1. **Concept.** Projecting a permission posture between algebras is a lattice translation, and translations widen unless proved otherwise. Require a **monotonicity obligation**: the projected posture permits no operation the source denied. Where the target cannot express a denial, the correct output is a **refusal to project**, not the nearest weaker value.
2. **Why it matters.** `#200` records the founding instance in ruflo's objective compiler. This is the same defect one layer down, in *projection* rather than *translation*, converting an author's deny into a runtime prompt the operator can approve.
3. **How.** Emit posture only through a checked lattice map with a property test: every operation denied at source is denied or unrepresentable at target; unrepresentable ⇒ residual ⇒ deploy gate refuses.
4. **Novelty.** `sharpens #200`. New: the widening occurs at the **host projection** step, is unaudited because the contract has no residual (C1), and is *hard-coded* rather than emergent.
5. **Custody verdict.** *Fails on input* — the posture is `spec.permissions`, authored by the harness author, and 13/13 adapters emit exclusively into locations the governed principal can write (§4a).
6. **Evidence.** static code evidence:
   - `host-opencode/src/index.ts:63-79` (`permissionBlock`): `webfetch: 'ask'` is a **constant** — a harness that denies web fetch projects to a prompt. `edit` is `'ask'` unless a `Write|Edit|MultiEdit(` deny exists — absence of a deny yields `ask`, not `deny`. Of `allow`, only exact `Bash(*)` is consulted; every other allow entry is **discarded**. Every deny that is neither `Bash(...)` nor `Write|Edit|MultiEdit(...)` is discarded. Patterns are rewritten `rm:*` → `rm *` (L70) into a different glob dialect with no equivalence check.
   - `host-github-actions/src/index.ts:44-53`: GitHub scopes derived by **substring regex over free-text allow strings** — `has(/issue|label|triage/i)` grants `issues: write`. Privilege derived from names the author chose. The `unmapped allow tokens do not widen permissions` test constrains the allow direction only; deny is not read by this adapter at all.
   - `host-openclaw/src/index.ts:71-78`: the **total** case — *"OpenClaw has NO top-level allow/deny `permissions` concept … Rather than invent a value the schema rejects, we emit only the (verified-valid) `mcp.servers` block and leave security to OpenClaw's own defaults."* The refusal to fabricate is correct; the entire posture is then dropped and the loss recorded **only in a source comment**. Its own test asserts the drop as intended: *"does not emit a top-level permissions block (not in openclaw schema)."*
7. **Provenance.** `host-opencode` **ADR-036/022/046**; `host-github-actions` **ADR-033/022**; `host-openclaw` **ADR-046**. Not read.

### C7 — The projection selects the enforcement plane, and never declares which plane it selected

1. **Concept.** Every host projection implicitly chooses *what will enforce* the definition's controls, and the planes differ by orders of magnitude in independence — from a token minted outside the process, to a config file the agent can rewrite, to a Markdown warning. A definition should carry a **required enforcement-independence level** per control; a projection that cannot reach it must refuse rather than emit a weaker artifact of the same name.
2. **Why it matters.** `#277`'s plane-per-leg admission map, read from the projection side. An author writing one deny-list against ten hosts is silently accepting ten enforcement strengths under one word.
3. **How.** Tag each control with the minimum plane class permitted (`minted-outside-process` / `os-enforced` / `config-honoured` / `advisory`). A projection declares the class it lands on; mismatch is a refusal; the class is part of the residual.
4. **Novelty.** `sharpens #277`. New: the **projection step is where the plane is chosen**, the choice is undeclared, and one of thirteen lands on a materially different plane.
5. **Custody verdict.** The instrument's most useful result here, and near-unanimous:
   - **13 of 13 packages emit exclusively into locations the governed principal can write** — project working-tree paths (`.claude/`, `.opencode/`, `.codex/`, `.prime/`, `.vscode/`, repo-root Markdown, `capability-table.json`, `openclaw.json`, `trust.json`, all `install*.sh|md`) or user-home paths under the same uid. Under the predicate, **every emitted artifact is a label**, with one partial exception.
   - **The exception: `host-github-actions`.** L18-23: enforcement *"shifts from the in-process mcp-policy.json gate to the workflow's own `permissions:` block — least-privilege GITHUB_TOKEN scopes."* The only projection whose artifact is consumed by a **minter the governed process does not run**: the agent inside the runner cannot widen a token already issued. **Passes on custody of the enforcement decision**; still **fails on input** (substring-derived from an author-written allow list, C6), and the workflow file lives in the repo, so an agent holding `contents: write` (L49) writes to the same tree the control lives in. The runbook's mitigation — *"don't hand-edit the workflow, or `harness mcp-scan` will flag the drift on your next PR"* (L195-197) — is **detection by a tool in the governed repo**, i.e. a label.
   - **Unverified-inference, flagged and not relied on:** whether GitHub evaluates the default branch's workflow for `issue_comment` triggers, which would place the file outside a feature-branch agent's reach. Needs GitHub documentation — a surface this run does not open.
   - `host-github-actions` alone names the residual and the host facility that must supply it — *"The `permissions:` block scopes the token; the Environment adds the human review the block cannot"* (L199-204). In prose, in a runbook.
6. **Evidence.** static code evidence for emission paths and the `permissions:` derivation; GitHub's token-minting semantics are **source claim** (the adapter's header). I did not run a workflow.
7. **Provenance.** **ADR-033**, **ADR-022**, **ADR-044**. Not read.

### C8 — Conformance for a projection must be host-side acceptance, not emitter-side assertion

1. **Concept.** A test comparing generated bytes to expected bytes proves the generator is deterministic. It cannot prove the host reads the file, accepts the schema, or acts on the values. A projection's conformance suite must submit the artifact to the target's own validator and assert acceptance; the golden-file test is a regression guard on top, never the conformance evidence. This is `#319` §2's "probe the real operation" with the protected operation being *the host loading the configuration*.
2. **Why it matters.** A well-formed file written into a key namespace the host ignores is indistinguishable, from inside the generator, from a working control. Every test passes; nothing is enforced.
3. **How.** Per-host CI submits each artifact to that host's own `config validate` equivalent and fails on rejection; a host with no validator is recorded as an enforcement-class downgrade (C7), not a pass.
4. **Novelty.** `sharpens #319` (§2), applied to a configuration projection rather than a capability probe.
5. **Custody verdict.** *Not control-shaped* — a verification discipline. Its absence is what lets the labels in C5/C6/C7 read as controls.
6. **Evidence.** static code evidence, ruled across all thirteen test suites at once by test title: **every test in all thirteen packages asserts a property of the emitted string or object** — escaping, key presence, JSON validity, byte-determinism, golden-file equality. **Not one loads an artifact into a target host.** The two adapters that *claim* host-side validation are decisive, because both found real defects:
   - `host-openclaw` L31-37: *"VERIFIED against a real `openclaw` 2026.6.8 install via `openclaw config schema`/`config validate` (ADR-046) … the earlier top-level `mcp_servers` map without `enabled` was REJECTED"* [source claim].
   - `host-opencode` L27-34, L57-62: *"VERIFIED against a real `opencode` 1.17.7 install (ADR-046) … The earlier `{ command, args }` shape (no `type`/`enabled`) is REJECTED by real opencode with a schema error"*; and real opencode has **no** `mcp.permissions` key [source claim].
   - `host-hermes` L115-130: the same class without a validator — the adapter previously emitted top-level `name`/`description`/`system_prompt`/`scrub_*` keys, *"those were assumed, never real"*, caught only by reading the upstream `cli-config.yaml.example` [source claim]. **Four phantom keys survived every emitter-side test.**
   - **Host-side validation ran twice in this package set and was rejected twice.** The other eight claim only *"Verified integration surface (from research)"* — documentation reading.
   - **Negative scope:** these are the **owners'** claims about their own validation. I ran nothing.
7. **Provenance.** **ADR-046** in `host-openclaw`, `host-opencode`, `host-hermes`, `host-prime-agent`. Not read.

### C9 — A missing vocabulary dimension reappears as an ad-hoc encoding inside a scalar, per host, undiscoverable from the schema

1. **Concept.** When the shared definition lacks a dimension a host needs, the dimension migrates into an out-of-band convention: a prefix on a string field, or a cast past the declared type. The convention is invisible to the schema, unvalidated, per-host, and silently inert everywhere it is not implemented. Treat a string-prefix convention or a type cast in a projection as a **defect report against the ontology**: the vocabulary is missing a dimension and must be widened, not overloaded.
2. **Why it matters.** **H4** (ontology-first) stated as a diagnostic. The observable symptom that a typed vocabulary is *under*-typed is that hosts start encoding meaning in string prefixes and casts. Where the smuggled dimension is authority — as here — an author writes a control the type system does not know exists, and no other host will honour it.
3. **How.** Any projection reading a field not on the declared type, or parsing structure out of a scalar, files an ontology change request. The dimension is admitted (subject to C2's two-host rule) or the feature is refused.
4. **Novelty.** **`new`.** Neither `#316` nor `#317` holds it. Constructive counterpart to C2: C2 says the vocabulary was borrowed from the wrong place; C9 says the symptom of it being too narrow is type-system evasion.
5. **Custody verdict.** *Fails on input* in the instance that matters: `host-rvm` reads its entire capability model from `spec.claims`, a field the declared `HarnessSpec` does not contain.
6. **Evidence.** static code evidence, three instances from one grep (`grep -rnE "\(spec as |as \{ claims" host-*/src/index.ts`):
   - `host-claude-code/src/index.ts:39-70` — `kernel-js/src/types.ts:25-29` declares `HookSpec { event: string; matcher?: string; handler: string }`. Claude Code has five handler **types**; the IR has none. The adapter encodes the type as a **string prefix** on `handler` (`https://…` → http, `mcp:server/tool` → mcp_tool, `prompt:…`, `agent:…`, else `node .claude/helpers/<h>.cjs`), explicitly *"keeping the kernel contract unchanged"*, noting *"previously every handler was forced to `command`, dropping the other 4 handler types."* No other adapter implements the convention. A definition using `mcp:` is meaningful on one host and a literal command name on the rest.
   - `host-rvm/src/index.ts:141, 152` — `(spec as { claims?: KernelClaim[] }).claims`. `claims` is **not** a member of `HarnessSpec` (`types.ts:31-51`). The comment calls it *"the 'Caller wires actual claims via spec extensions' path."*
   - `host-opencode/src/index.ts:92` — `(spec.permissions ?? (spec as any).mcpPolicy)`, a cast to a retired field name.
7. **Provenance.** **ADR-044** (all three), **ADR-046** (`host-opencode`). Not read.

### C10 — A conformance test that pins an enumeration to a literal converts drift into a guaranteed invariant

1. **Concept.** `expect(list).toEqual([...literals])` over a set that is *supposed to grow* does not detect staleness — it enforces it and paints it green. Worse than an unstated alphabet (`#323`), because the alphabet is stated, pinned, and *tested*, so the gap reads as verified coverage. Enumerations tracking a growing surface must be asserted against the surface (a derived set relation), never a literal.
2. **Why it matters.** A substrate that enumerates enforcement planes, hosts or protected operations in config and pins it in a test will silently stop covering new members while its suite stays green — `#323`'s failure with a passing test standing in for the claim.
3. **How.** Assert `set(choices) == set(discovered adapters)`, computed at test time from the package set.
4. **Novelty.** `sharpens #323`. New: the case where the alphabet **is** named, is stale, and a green test certifies the staleness.
5. **Custody verdict.** *Not control-shaped* here — but coupled to C5: this pinned enumeration sits four lines below the publish gate that passes on its own failure. Both are the gated unit writing its own predicate.
6. **Evidence.** static code evidence — `vertical-trading/templates/manifest.json` declares `"host"` choices `["claude-code","codex","pi-dev","hermes","openclaw","rvm"]` (6); `ls -d packages/host-*` returns **10**; `__tests__/pack.test.ts:39-45` is titled *"manifest declares all 6 hosts as host choices"* and asserts equality with the same six literals. Four adapters (`copilot`, `github-actions`, `opencode`, `prime-agent`) are unreachable from this pack and the test guarantees they stay unreachable. **I did not check** whether other verticals or the generator carry the same list — no other vertical is in my package set.
7. **Provenance.** `vertical-base` declares **ADR-013**; `vertical-trading` declares none. Not read.

---

## 4a. Custody-predicate sweep (C5 instrument) — where every emitted artifact lands

**[static code evidence]** Enumerated from the `generateConfig` bodies (§1 A2).

| Adapter | Emitted into | Governed principal can modify? | Predicate verdict |
|---|---|---|---|
| host-codex | `.codex/config.toml`, `AGENTS.md`, `install-mcp.sh` | yes (repo tree) | label |
| host-copilot | `.vscode/mcp.json`, `.github/copilot-instructions.md`, `install.md` | yes | label |
| host-hermes | `cli-config.yaml`, `optional-mcps/*.yaml` | yes | label |
| host-openclaw | `openclaw.json` (→ `~/.openclaw/`), `SKILL.md`, `install-openclaw.sh` | yes (same uid) | label; posture dropped entirely |
| host-pi-dev | `pi-extension/src/index.ts`, `AGENTS.md`, `SYSTEM.md`, `trust.json` (→ `~/.pi/agent/`) | yes | label; **self-issued trust grant** |
| host-claude-code | `.claude/settings.json`, `.claude/agents/*.md`, `CLAUDE.md`, `install-mcp.sh` | yes | label |
| host-github-actions | `.github/workflows/*.yml`, `.github/actions/*/action.yml`, `SYSTEM.md`, `mcp-servers.json`, `install.md` | file: yes; **token: minted by GitHub** | **partial pass** — enforcement decision off-process; fails on input |
| host-opencode | `.opencode/opencode.json`, `.opencode/agents/*.md`, `AGENTS.md`, `install.md` | yes | label; widening (C6) |
| host-prime-agent | `.prime/agent/**`, `SANDBOX-REQUIRED.md`, `install-prime-agent.md` | yes | label — **and says so**: host *"cannot enforce this harness's deny-list"* |
| host-rvm | `rvm-partition.toml`, `capability-table.json`, `wasm-guest.json`, `install-rvm.sh` | yes | label; **self-declared assurance level** |
| sdk / vertical-base / vertical-trading | n/a (libraries) | — | vertical-trading: **self-administered publish gate** |

**Result: the instrument caught four new instances** (self-issued trust grant; self-declared assurance level; self-administered publish gate; the near-universal project-controlled emission surface) and **one partial pass**. `#318`'s "generally live in project-controlled files" holds at **13 of 13** here, with that one qualification.

---

## 5. Provenance pattern — a finding about what MetaHarness is

**[source claim, from headers and manifests]** **11 of 13** packages cite internal **ADR** numbers: ADR-011, 013, 018, 022, 032, 033, 036, 044, 046, 246, 247. Three appear in `keywords` (ADR-032/033/036) — the ADR number is treated as package metadata. `sdk` and `vertical-trading` cite none.

1. **The ADRs resolve out of tree** — `github.com/ruvnet/agent-harness-generator/blob/main/docs/adrs/` (linked verbatim in `host-copilot`, `host-opencode`, `vertical-base`). The design rationale for these adapters is in **a different repository from the code**. Declared origin recorded; not followed.
2. **Zero of the thirteen declare an academic, standards, or third-party-mechanism origin.** Every external reference is a **host vendor's integration surface** — `openai/codex`, `NousResearch/hermes-agent` (+ issue #741), `badlogic/pi-mono`, `PrimeIntellect-ai/prime-agent`, `openclaw/openclaw`, `opencode.ai`, `code.claude.com`, `ruvnet/rvm`. This differs sharply from the Q4-flagged packages in W1/W2/W4 (arXiv ids, NIST AI RMF, OWASP, an NVIDIA clone). **W3's packages cite what they integrate with, not where their mechanisms came from.** The one mechanism with a declared source is `host-hermes`'s scrubber, declared as mirroring *ruflo's* `scrubReasoningBlocks()` — in-ecosystem ancestry, not external prior art.

---

## 6. C2 rulings — mechanism level, with the reason stated for each

The sweep returned hits in **all thirteen** packages. Ruled individually; **not one is disqualified by dependency list.**

| Hit | Where | Mechanism-level ruling |
|---|---|---|
| `"ruflo"` npm keyword (13/13) | `keywords` | **Not a coupling.** Branding. No idea depends on it. |
| `homepage`/`repository` → `ruvnet/agent-harness-generator` (12/13) | manifests, README | **Not a coupling.** Repository metadata + ADR corpus location. |
| `@metaharness/kernel` dependency (10/13) | manifests | **Not a coupling of the concepts.** Every concept above is stated over an abstract definition→projection contract; delete the kernel and each survives verbatim. Applying C2 as a manifest scan would disqualify the whole workstream and return a false negative. |
| ruflo `scrubReasoningBlocks()` | `host-hermes` L26-28, L39 | **Ancestry, not dependency.** No import; the regex logic is self-contained. The *idea* needs nothing upstream. Refused for other reasons — §7. |
| `RUFLO_TRADE_CONFIRM=YES_LIVE` | `vertical-trading/README.md:19` | **The one genuine namespace hit.** The live-trading interlock is keyed to a `RUFLO_*` env var — exactly what C2 names. The *concept* (default-safe mode requiring an out-of-band token to disarm) is trivially portable; **the interlock as specified is disqualified**, and it fails custody anyway (the var is set by whoever launches the process). Not registered. |
| `@ruvector/rvf`, `@ruvector/rvf-wasm`, `RuVector Format` | `host-rvm` L266-280 (emitted `wasm-guest.json`) | **Coupling of the emitted artifact**, marked `recommended: true` with *"Optional; the partition still boots"* [source claim]. Confirms `#316`/`#317`: the executable tie runs to **RuVector**. |
| `entrypoint: 'pkg/ruflo_kernel_wasm.js'` | `host-rvm` L266 | **Artefact-path coupling** — a ruflo-branded filename in the emitted guest manifest. |
| `github.com/ruvnet/rvm` | `host-rvm` throughout | **Mechanism-level disqualification, scoped.** Nothing outside ruvnet's RVM parses `capability-table.json` or `rvm-partition.toml`; the *hardware-isolated deployment via capability tokens* mechanism requires **ruvnet/rvm** to honour the tokens. **The C5 concept extracted from it needs nothing from RVM** — it is a statement about who authors a control's strength parameter, and stands over any token format. Hence a `concept found` row with a scoped disqualification, not a blanket one. |

**No row carries a bare `disqualified by ecosystem coupling` verdict.** One scoped mechanism-level disqualification (`host-rvm`'s deployment mechanism; upstream `ruvnet/rvm`, with `@ruvector/rvf` in the emitted artifact) and one refused mechanism (`RUFLO_TRADE_CONFIRM`; upstream the `RUFLO_*` namespace).

---

## 7. Coverage ledger — every package, one row, one verdict

`concept found` is used only where a **registered concept could not have been stated without that package**. Packages contributing corroborating evidence but holding no mechanism of their own are ruled `nothing portable` with the contribution named.

### Tier 1 — binding (8)

| # | Package | LOC | Verdict | Reason / concept |
|---|---|---|---|---|
| 1 | `host-codex` | 227 | **nothing portable** | A TOML serializer (`tomlEscape`, `serverToToml`) plus a `codex mcp add` command emitter and an `AGENTS.md` renderer. No mechanism of its own. Its one distinguishing fact — it emits into `.codex/config.toml`, the **project** path its own header (L9-10, L17) says is *"only honored for 'trusted' projects"* and names a *"known footgun (codex#3441)"* — is the cleanest instance of emission ≠ honouring, contributed to **C7/C8**. Compared line-by-line against `host-copilot` and `host-openclaw`; the difference is serialization format, not mechanism. |
| 2 | `host-copilot` | 275 | **nothing portable** | Structurally identical to `host-codex` with JSON. Its one candidate mechanism — emitting the server map under **both** `servers` and `mcpServers` (L71-75) *"for forward + backward compat"* — is **named and refused**: a workaround for one vendor's schema churn that produces two mutable copies of one truth in a single file with no consistency constraint. A defect to avoid, not an idea to build. Compared against `host-opencode`'s ADR-046 rewrite of the same problem, which chose one shape and validated it. |
| 3 | `host-hermes` | 355 | **nothing portable** | Two mechanisms, both refused. (a) `scrubHermesBlocks` — commodity reasoning-tag sanitization, **declared as mirroring ruflo's `scrubReasoningBlocks()`** (L26-28), irrelevant to enforcement outside the governed party; its one non-obvious detail (a tempered-greedy token replacing a lazy quantifier to defeat CodeQL `js/polynomial-redos`, L44-53) is a regex-performance fix. (b) YAML key/scalar escaping with a `YAML_RESERVED_BARE` guard (L66-86) — generic serialization hygiene. Its real contribution is the **ADR-046 phantom-key fact** (L115-130), the sharpest single evidence for **C8**. |
| 4 | `host-openclaw` | 327 | **concept found** | Source of **C6** (the total case: the entire permission posture dropped because the host has no allow/deny concept, loss recorded **only in a source comment**, L71-78 — no residual, and its own test asserts the drop as correct) and of **C4** (emitter writes `mcp.servers`, L79; the same file's runbook, L144, directs the user to the `mcp_servers` key ADR-046 found rejected). Contributes to **C1**, **C8**. |
| 5 | `host-pi-dev` | 196 | **concept found** | Source of **C5**'s self-issued trust grant (`trustJson`, L79-100). Also the negative-space case the brief flagged: the host ships **no MCP by design** [source claim, L20-22, quoting Pi's *"What we didn't build"*], and the projection responds by **escalating from configuration to code generation** — a TypeScript extension calling `pi.registerTool(...)` and dispatching through `loadKernel()`. Contributes to **C7**: a host that structurally cannot receive the primary transport forces the projection to change kind, and the contract has no way to say so. |
| 6 | `sdk` | 287 | **concept found** | Source of the **C1** vocabulary gap and a pillar of **C2**. `HarnessDef` (L49-58) exposes 8 fields; the IR has 10; the intersection excludes **all four** authority-bearing fields. `grep -icE "permission\|statusLine\|autonomous\|claims\|deny\|allow" sdk/src/index.ts` → **0**. Meanwhile `HookDef.event` (L37) is a closed union of Claude Code's exact ten event names. The author-facing vocabulary is simultaneously **narrower than the IR** (no security) and **narrower than host-neutral** (one host's event set). The `define*` wrappers are branded and shallow: kebab-case checks, non-empty checks, `Object.freeze`, collision detection on agent and skill names but **not** tool names (L126-136) — the omission `host-prime-agent` later repairs (**C3**). |
| 7 | `vertical-base` | 217 | **concept found** | Source of **C5**'s third instance. Supplies `verifyTemplateFilesPresent()` (L95-115), documented as the publish gate: *"Pack authors run this at publish time to catch dangling references before they ship."* The gate ships as a **library the gated party calls** — custody of the call site sits inside the gated unit, which makes the `vertical-trading` outcome structural rather than accidental. `validateVerticalManifest` (L69-89) is competent shape validation and explicitly *"Doesn't validate file existence — that's the loader's job at read time"*, so nothing else closes the gap. |
| 8 | `vertical-trading` | 74 | **concept found** | Source of **C10** (manifest pins 6 host choices against 10 `host-*` packages; `pack.test.ts:39-45` asserts equality with the literal six) and of **C5**'s publish-gate instance (`pack.test.ts:24-35` passes when the gate fails; all ten referenced `.tmpl` files absent; in `RELEASE_ORDER` — *packed and release-ordered, not verified published*, per `#324`). Carries the run's one **`RUFLO_*` namespace hit** (§6). The module itself (74 lines) is a manifest loader. |

**Tier 1 tally: 5 `concept found`, 3 `nothing portable`, 0 `disqualified by ecosystem coupling`.**

### Tier 2 — non-binding, same schema (5)

| # | Package | LOC | Verdict | Reason / concept |
|---|---|---|---|---|
| 9 | `host-claude-code` | 268 | **concept found** | Source of **C9** (`hookHandlerFor`, L39-70: five handler types encoded as string prefixes on a bare `handler: string`, *"keeping the kernel contract unchanged"*). Also the decisive evidence for **C2**: the only adapter whose permission projection is a **verbatim pass-through** (L82) — the IR *is* its native format, which is why it alone is lossless. |
| 10 | `host-github-actions` | 382 | **concept found** | Source of **C7**'s partial pass — the only projection shifting enforcement to an off-process token minter (L18-23) — and of **C6**'s substring-matched privilege derivation (L44-53). The only adapter naming the residual and the host facility that must supply it (L199-204), in prose. |
| 11 | `host-opencode` | 356 | **concept found** | Source of **C6**'s widening (L63-79) and of **C4** (runbook L177-178 asserts enforcement semantics for `mcp.permissions`, the key L59-61 records the host does not have). Contributes the second host-side rejection to **C8**. |
| 12 | `host-prime-agent` | 888 | **concept found** | The compliance case. Source of **C3** (`normalizeSkillName`/`uniqueSkillName`, L57-97, naming the *"ADR-046 silent-drop bug class"*) and the only positive evidence for **C1**: `SANDBOX-REQUIRED.md` as a conditional loss artifact (L300-324, L505-508), an "Unsupported on this host" residual section (L417-436), refusal to fabricate an execution target (L27-31). Its `SANDBOX-REQUIRED.md` carries the most honest sentence in the thirteen: *"Prime Agent cannot enforce this harness's deny-list."* Limit: honesty about a label, not a control — the file lands in the repo the governed party writes. |
| 13 | `host-rvm` | 579 | **concept found** | Source of **C5**'s self-declared assurance level (`proof_tier` computed inside the generated token table; `expires_at = 0`; rights suffix-matched from author-chosen names; fall-through to `EXECUTE`; `*` → all seven rights incl. `GRANT`/`REVOKE`). **Scoped C2 disqualification** on the *deployment* mechanism (upstream `ruvnet/rvm`; emitted artifact names `@ruvector/rvf` + `ruflo_kernel_wasm.js`) — §6; the custody concept survives it. |

**Tier 2 tally: 5 `concept found`. Full ledger: 13 of 13 packages owned by exactly one row. No package is silent.**

---

## 8. What I did NOT check (scope recorded negatively, per `#324`)

- **Anything at runtime.** No install, build, test, generator run, service, container or model run. I did not execute `vertical-trading`'s publish-gate test, `openclaw config validate`, `opencode`, `pi`, a GitHub workflow, or any adapter. Every "the host rejects X" statement is the **owner's** claim, labelled as such.
- **The out-of-tree ADR corpus.** ADR-011/013/018/022/032/033/036/044/046/246/247 recorded as declared origins and **not fetched**. Every "ADR-nnn says…" is quoted from the in-repo comment citing it.
- **The generator.** Adapter selection, ordering, and merge behaviour on colliding output paths across multi-host scaffolds. The collision risk is real and unexamined: `AGENTS.md` is emitted by `host-codex`, `host-pi-dev` and `host-opencode`; `install.md` by `host-copilot`, `host-github-actions` and `host-opencode`. `host-prime-agent` L47-49 is the only adapter host-qualifying its runbook name *"so multi-host scaffolds don't collide."* **I did not determine what happens when they do.** Handed to the leader.
- **`__tests__` bodies**, except `vertical-trading/pack.test.ts` (read in full) and test *titles* across all thirteen. I ruled on the titles as a class; I did not read every assertion.
- **README bodies in full** for `host-codex`, `host-copilot`, `host-hermes`, `host-openclaw`, `host-claude-code`, `host-github-actions`, `host-opencode`, `host-prime-agent`, `sdk`, `vertical-base` — greppped for origins, ecosystem tokens and emitted-file lists. Read in full: `vertical-trading`, `host-rvm`, `host-pi-dev`.
- **Runbook/emitter consistency (C4)** beyond the three instances found: not checked in `host-codex`, `host-copilot`, `host-claude-code`, `host-github-actions`, `host-prime-agent`, `host-rvm`.
- **Registry state.** No package sets `private: true`; ten of thirteen appear in `scripts/publish-workspace.mjs` `RELEASE_ORDER` (`sdk`, `host-claude-code`, `host-codex`, `host-pi-dev`, `host-hermes`, `host-openclaw`, `host-rvm`, `host-prime-agent`, `vertical-base`, `vertical-trading`); `host-copilot`, `host-github-actions`, `host-opencode` are publishable but absent from it. **Publishable and release-ordered are not published.**
- **Whether GitHub evaluates the default-branch workflow for `issue_comment` triggers** (would change C7's ruling on `host-github-actions`). Unverified-inference; needs a documentation surface this run does not open.
- **Other vertical packs and the generator's own host list** — whether C10's pinned enumeration recurs. No other vertical is in my package set.
- **Compiled `dist/` output.** Absent from the checkout; all claims are about source.

---

## 9. Cross-workstream handoffs

1. **`arc-agi-3-chatgpt` (W2) — the comparison would be materially better with it in.** My cross-adapter result rests on the claim that **all thirteen host projections emit exclusively into locations the governed principal can write**, with `host-github-actions` the single partial exception. That package leads with *"remote MCP harness for ChatGPT Developer Mode"* [source claim] — a **remote** transport and a vendor-hosted host, the one configuration in the repository that could place the projection's target outside the governed tree entirely. If it does, it is a second and possibly stronger data point for **C7**. **I did not open it.** Recommend the leader ask W2 for two facts only: (a) where the projection's artifacts land and who owns that location; (b) whether any control is honoured by a party other than the process running the agent.
2. **`turn-credit` (W2) — structurally the same shape as C6.** Its declared property *"advisory signals … Never reverses the verifier's decision"* is the **non-widening obligation** of C6 stated for a signal channel rather than a permission algebra. If W2 registers it, the two should be graded against each other; they may be one concept.
3. **`aws-finops` / `flywheel` (W1/W4) — the "human review gate" claim.** My C5 sweep found four instances of the governed party authoring a control's own parameters. Those owners should run the same third question (*who sets the strength parameter?*), not only the first two.
4. **For the curator, not absorbed:** `#316`'s portable-concept list attributes "host projections with **explicit loss reports**" to MetaHarness. §3 shows the contract carries no loss channel and 1 of 10 adapters reports loss. That line should be **corrected**, not merely supplemented.

---

## 10. Summary

- **Concepts registered: 10** — `new` × 4 (**C2** donor-host IR; **C3** normalisation collision; **C4** runbook drift; **C9** dimension smuggled into a scalar); `sharpens` × 6 (**C1** → `#316`; **C5** → `#318`; **C6** → `#200`; **C7** → `#277`; **C8** → `#319`; **C10** → `#323`); `already held by` × 0.
- **Coverage: 13/13 rows.** Tier 1: 5 `concept found`, 3 `nothing portable`, 0 disqualified. Tier 2: 5 `concept found`. One **scoped, mechanism-level** C2 disqualification and one refused mechanism. **No verdict was reached by dependency list.**
- **Custody instrument: four new instances plus one partial pass.** It did not come back empty; the most useful result was the unanimous one — 13 of 13 emit into the governed party's own tree.
- **Firewall:** nothing here is demonstrated by us. Structure only, `directional`, no grade past `claimed`.
