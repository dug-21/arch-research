# FINDINGS — W1: Ontology spec (wfh-002)

**Workstream:** W1 — Ontology spec · **Scope:** `wfh-002` (Issue dug-21/arch-research#46) · **Agent:** `wfh-002-w1-researcher`
**Status:** structure-only (research moves *structure*, never *status*). Nothing here is `proven`; the spec is a
hypothesis that W2 (round-trip), W3 (AGENTS.md subsumption), and W4 (template artifact) will test.
**Evidence classes used:** `[demonstrated]` = verified by direct read in this run · `[doc-claim]` = vendor/standard
documentation, secondary-sourced via the wfh-001 scan, not re-verified here.

---

## 0. Design principles (derived before the types)

Three principles fell out of the mechanism landscape before any type did; they constrain everything below.

**P-A. The load-bearing axis is control semantics, not file format.** On disk, nearly every shipped mechanism is
markdown-plus-YAML-frontmatter (rules, skills, agent-defs, recipes, playbooks) `[demonstrated: this repo's
.claude/; doc-claim: wfh-001 scan rows]`. File format is therefore useless as a type discriminator. What actually
distinguishes mechanisms is **who acts, and with what force**: content the harness *places into* a context (a
request), a unit the harness *schedules*, a principal the harness *spawns*, a capability a principal *calls*, and a
program that *enforces outside the LLM* (a guarantee). The request/guarantee split is stated verbatim in the
Claude Code docs per the wfh-001 scan ("CLAUDE.md = request not guarantee; hooks = hard layer") and is the
core of Unimatrix node #157 (F2). The type system follows this axis.

**P-B. Lossless = mechanism-level typing + opaque body preservation.** The ontology types the *mechanism*
(how a unit activates, scopes, and binds), never the *semantics of the prose*. Every node carries its markdown
body as an opaque, byte-preserved payload. This is what makes lossless round-trip (W2) and AGENTS.md
subsumption (W3) achievable at all: `AGENTS.md` is explicitly "just standard Markdown … any headings you
like" with **no required fields** `[demonstrated: https://agents.md FAQ, fetched 2026-07-22]` — there is no
inner structure to type, so the lossless landing zone must be a body-preserving node, not a parse.

**P-C. Definition plane only.** This ontology is the *workflow-definition* store (H7's "definitions vs events"
split, node #167): the durable, authored, versioned graph a run later lights up. Run events, traces, transcripts,
and tool-call outcomes are a different plane and are out of W1 scope. Consequence pre-registered in §3:
tool-*written* runtime memory (Windsurf Memories, Devin Knowledge, Claude auto-memory) straddles the
planes and is the ontology's most likely lossy edge. Per the scope constraint: this ontology is NOT Unimatrix
knowledge and is not stored there.

---

## 1. The ontology spec

### 1.1 Node types (5 — the candidate set survives, with one redefinition)

The candidate set {skill · agent-def · step · gate · tool} is kept at five, but **`skill` is generalized**: it absorbs
rules-files/`AGENTS.md`/`CLAUDE.md` via a required `activation` field, rather than adding a sixth `rule` type.
Justification in §2.1 — the short version: OpenHands ships this exact unification (microagents with three
load-modes spanning always-on rules to invoked skills), so the merge is generalizing a shipped mechanism,
not inventing one.

---

#### `skill` — injectable instruction unit

**Definition.** A unit of instruction/procedure content that the harness places into an LLM context according to
an activation policy. Covers the whole activation spectrum: always-on rules, path/glob-scoped rules,
description-matched skills, and explicitly invoked skills. A skill is a *request*, never a guarantee (P-A).

**Required fields**

| field | type | notes |
|---|---|---|
| `name` | string | unique within the graph |
| `body` | markdown (opaque) | byte-preserved; the lossless payload (P-B) |
| `activation` | enum + params | `always` \| `scoped` (path/glob) \| `matched` (description/keyword, model- or harness-decided) \| `explicit` (user/agent invokes by name) \| `event` (fires on a harness event) |
| `owner` | enum | `user` \| `tool` \| `community` — who authors/mutates the content |

**Optional fields**

| field | notes |
|---|---|
| `scope` | paths/globs + precedence rule (e.g. "closest file wins" — required to express nested `AGENTS.md`) |
| `description` | the matching text for `activation:matched` (Claude Code auto-described skills) |
| `assets` | attached executable/data files (e.g. this repo's `opcost.py` beside its `SKILL.md`) |
| `version`, `source_ref` | provenance of the file/registry it round-trips to |

**Provenance (what it generalizes).**
- Rules-files: `AGENTS.md` (near-universal standard, node #156/F1), `CLAUDE.md` layered auto-load,
  `.claude/rules/` `[demonstrated: /workspaces/arch-research/CLAUDE.md, .claude/rules/unimatrix-access.md]`;
  `.cursor/rules/*.mdc` with **4 apply-modes** (the activation enum in miniature), `.clinerules/` globs,
  `.goosehints` hierarchical, `CONVENTIONS.md` (aider), `.github/copilot-instructions.md` + glob-scoped
  `.instructions.md` `[doc-claim: wfh-001 scout-candidates.md §A table; nodes #134–#146]`.
- Skills proper: Claude Code skills (auto-described, self-invoked), Amp `SKILL.md`, OpenHands
  microagents (MD+YAML, **3 load-modes** — the unification witness), this repo's 22 `SKILL.md` files
  `[demonstrated: .claude/skills/]`.
- Recipes/Playbooks (Goose, Devin) are *partially* here — see the `step` boundary discussion, §2.3.

---

#### `agent-def` — principal definition

**Definition.** The definition of an executable principal: a named context with role instructions, an identity, and
a capability envelope (which tools/skills/steps it may touch). An agent-def *is* a context; a skill is loaded *into*
one. It is the unit that permissions and attribution attach to — per jurati#12, per-agent identity and capability
gating are queen-side concerns, and the agent-def is where they bind `[demonstrated: gh issue view 12
--repo dug-21/jurati, fetched 2026-07-22 — single-root delegation: "every per-agent `_attested_identity` the
queen stamps is a trusted delegated claim"]`.

**Required fields**

| field | type | notes |
|---|---|---|
| `name` | string | doubles as the identity stem (`{scope-id}-{role}` pattern in this repo) |
| `role_instructions` | markdown (opaque) | the body |
| `capability_envelope` | via `invokes` edges (+ optional allowlist field) | which tools/skills this principal may use; deny-side lives in gates, not here (§1.2) |

**Optional fields**

| field | notes |
|---|---|
| `model` | model pinning/preference |
| `isolation` | own-context subagent vs inline |
| `spawnable_by` | which agent-defs may spawn it (leader→specialist topology) |
| `identity_seam` | attestation/delegation hook (jurati#12 Anchor-B seam) — a *field*, since trust-binding is runtime |
| `type/scope/capabilities` | free metadata (this repo's frontmatter: `type: specialist`, `scope: targeted`, `capabilities:` list) `[demonstrated: .claude/agents/factory/factory-researcher.md]` |

**Provenance.** Claude Code subagents; Goose subagents; Factory custom Droids (MD+YAML subagents); Amp
Librarian; this repo's six `.claude/agents/factory/*.md` role defs `[demonstrated]`; `[doc-claim: wfh-001 §A,
synthesis (a)#4 — "subagents-as-isolated-context is convergent"]`.

---

#### `step` — schedulable unit of a workflow

**Definition.** A unit of work the *harness* schedules: it has an objective, a completion criterion, ordering
relative to other steps, and (optionally) an assigned principal. Steps compose — a protocol/phase is a
composite step that `invokes` its children; ordering among siblings is `depends-on`. No separate
`workflow`-container type (§2.2).

**Required fields**

| field | type | notes |
|---|---|---|
| `name` | string | |
| `objective` | markdown (opaque) | what the step must accomplish |
| `output` | string/spec | the completion criterion — every workstream in this repo's protocols carries an explicit `Output:` `[demonstrated: .claude/workflow/research-scope.md]` |

**Optional fields**

| field | notes |
|---|---|
| `inputs` | consumed artifacts/paths |
| `assigned` | via `invokes` → agent-def |
| `rework_policy` | e.g. "REWORKABLE max 2 → SCOPE-FAIL" — but see stress point S4: this may belong on the gate |
| `telemetry` | phase-boundary calls (e.g. `context_cycle phase-end`) — expressible as step `invokes` tool |

**Provenance.** This repo's `.claude/workflow/*.md` protocols (research-scope: scope → tech-discovery →
[feasibility] → synthesis; theme-scan; decompose-scope) `[demonstrated]`; Goose Recipes (portable YAML:
prompt+extensions+params+**sub-recipes** — the composition witness), Devin Playbooks, JURATI wave
sequencing (jurati#12: the queen "owns the control-flow an LLM does unreliably — state machine, wave
sequencing") `[demonstrated: issue text; doc-claim: recipe/playbook internals]`.

---

#### `gate` — out-of-LLM enforcement point

**Definition.** A harness-owned decision point bound to a trigger, whose verdict is produced *outside the LLM*
— by a deterministic program or by a human — and enforced by the harness/platform regardless of what the
model "wants." The type derives directly from jurati#12: enforcement (security, capability gating, determinism)
is deliberately *declined* by the knowledge substrate and owned by the driver/queen; a gate is that ownership
reified `[demonstrated: issue #12 — "the queen is the root of trust"; ADR-008 audit-only vs enforcement
ceiling]`. A gate is a *guarantee*; a skill is a *request* (P-A).

**Required fields**

| field | type | notes |
|---|---|---|
| `name` | string | |
| `trigger` | enum + matcher | `tool-call` \| `event` (session-start, prompt-submit, compact, subagent-start…) \| `step-boundary` \| `vcs-action` (push/PR/merge) \| `mode` (plan/act, autonomy tier) |
| `predicate` | program \| matcher \| policy-doc | the thing that decides — a command, a regex/glob matcher, a branch-protection rule, an analyzer |
| `effect` | enum | `deny` \| `allow` \| `ask` \| `halt` \| `transform` \| `observe` (telemetry/side-effect — see S2) |
| `arbiter` | enum | `program` \| `human` — unifies deterministic hooks with this repo's advisory/blocking human gates |
| `locus` | enum | `harness` \| `platform` (e.g. GitHub branch protection) \| `os` (sandbox) \| `vcs` — where enforcement physically lives |

**Optional fields**

| field | notes |
|---|---|
| `bypassability` | e.g. "deny rules hold even in bypass mode" vs "YOLO safeguards bypassable" — the honesty field the wfh-001 scan shows vendors differ on |
| `failure_handling` | rework loop, exit-code tier, escalation target |
| `blocking` | `advisory` \| `blocking` — this repo's two gate classes `[demonstrated: research-scope.md]` |

**Provenance.** Claude Code hooks (this repo's `settings.json`: 8 hook events with matchers → commands
`[demonstrated]`) and permission allow/deny/ask rules; OpenHands ConfirmationPolicy + deterministic
SecurityAnalyzer; Copilot structural branch/PR gates (cannot approve/merge own PR); Factory `--auto` tiers
with non-zero exit on violation; Cline non-bypassable Plan-mode; Devin `request_scope`; Windsurf 4-tier
terminal gates `[doc-claim: wfh-001 §A + "notable structural mechanisms"; nodes #143, #144, #145, #137,
#157/F2]`. Human-arbiter flavor: this repo's advisory (scope, synthesis) and blocking (coverage, firewall)
gates `[demonstrated: .claude/workflow/research-scope.md, .claude/agents/factory/research-leader.md §3]`.

---

#### `tool` — callable capability

**Definition.** A capability a principal can invoke at runtime: built-in harness tools, MCP servers/tools, attached
scripts, platform actions. The tool is the *object* of most gating (permission rules match on tool names) and
the target of most capability envelopes — it earns its type because gates and agent-defs both need something
stable to point at.

**Required fields**

| field | type | notes |
|---|---|---|
| `name` | string | the invocation name (e.g. `context_search`, `Bash`, `mcp__unimatrix__*`) |
| `provider` | enum | `builtin` \| `mcp` \| `script/asset` \| `platform` |
| `interface` | schema/ref | params schema or the command contract |

**Optional fields**

| field | notes |
|---|---|
| `side_effect_class` | `read` \| `write` \| `execute` \| `network` — what autonomy tiers and analyzers classify on |
| `enablement` | config toggle (this repo: `settings.local.json` `enabledMcpjsonServers: ["unimatrix"]` `[demonstrated]`) |
| `credential_seam` | BYO-key / server auth — definition-plane pointer only |

**Provenance.** MCP across effectively all 13 scanned tools `[doc-claim: wfh-001 §A]`; Claude Code tool
permission surface; this repo's Unimatrix MCP tools and access tiers (read-only vs `context_cycle`-only vs
curator-writes — tiers that only make sense with tools as first-class referents) `[demonstrated:
.claude/rules/unimatrix-access.md, agents/factory/*.md]`.

---

### 1.2 Edge types (4 — candidate set survives unchanged)

| edge | domain → range | semantics | provenance |
|---|---|---|---|
| `invokes` | (agent-def \| step \| skill) → (tool \| agent-def \| skill \| step) | Definition-plane "actively uses / spawns / runs / may-call." Optional field `mode: may\|must\|spawn`. Covers: leader spawns researchers (agent→agent) `[demonstrated: research-leader.md §2]`; phase assigns role (step→agent-def); skill runs its asset (skill→tool: opcost `SKILL.md`→`opcost.py` `[demonstrated]`); composite step → child steps (§2.2); agent-def → tool = capability envelope (allow-side only; deny-side is a gate). | subagent spawning (CC/Goose/Factory/Amp); recipes invoking extensions `[doc-claim]` |
| `depends-on` | step → step (also skill → skill, tool → tool) | Prerequisite / ordering. Acyclic within one composite. Carries the sequencing jurati#12 assigns to the queen ("wave sequencing"). | this repo's phase order scope→tech-discovery→[feasibility]→synthesis `[demonstrated]`; Goose sub-recipe ordering `[doc-claim]` |
| `gated-by` | (tool \| step \| agent-def) → gate | The source cannot proceed past the gate's trigger without the gate's verdict. Pair-specific gating (this agent × that tool) is expressed in the gate's `predicate` matcher, not by edges-on-edges. | PreToolUse matcher `^context_cycle$` → hook `[demonstrated: settings.json]`; feasibility step → firewall gate `[demonstrated: research-scope.md]`; PR → branch protection `[doc-claim: Copilot row]` |
| `injects` | skill → (agent-def \| step) | The harness places the skill's body into the target's context when the skill's `activation` fires. Passive placement — the *request* half of P-A, vs `invokes`' active call. A skill with no `injects` edge but `activation:always` + a `scope` defaults to "all principals within scope" (how flat rules-files behave in the wild). | rules auto-injection in all 13 scanned tools `[doc-claim: wfh-001 synthesis (a)#1; #156/F1]`; layered CLAUDE.md; `.claude/rules` path-scoped injection `[demonstrated: this session's own context]` |

**Rejected edge candidates:** `permits` (agent-def→tool allowlist) — merged into `invokes(mode:may)`
because this is a definition-plane graph, where "wired to use" and "permitted to use" coincide; deny-lists are
gates (`effect:deny`), keeping all *negative* authority in one type. `contains` (workflow→step) — merged into
`invokes` on composite steps (§2.2). `cites/refs` (doc cross-references) — a body-level concern, not a typed
edge; typing it would violate P-B's opaque-body rule and explode the graph.

---

## 2. Minimality argument

### 2.1 The one redefinition: rules-files merge into `skill` (a 6th `rule` type rejected)

The candidate five had **no home for the single most universal mechanism in the landscape** — the flat
rules-file (`AGENTS.md`/`CLAUDE.md`/`.cursor/rules`/…, shipped by all 13 scanned tools, #156/F1). Without a
home, W3 fails on arrival. Two options:

- **Add a 6th type `rule`.** Rejected. The rule/skill boundary is not a dichotomy but a spectrum of activation:
  Cursor alone ships **four** apply-modes for one mechanism (always / auto-attached by glob / agent-decided /
  manual) `[doc-claim: #139]`, and OpenHands microagents span always-loaded rules to keyword-triggered to
  task-invoked in **one** MD+YAML construct with a load-mode field `[doc-claim: #137]`. A type boundary
  placed anywhere on that spectrum is arbitrary and is already contradicted by shipped mechanisms.
- **Generalize `skill` with a required `activation` field.** Adopted. The market's own convergence (microagents,
  apply-modes) demonstrates the unification; the field carries the distinction the types would have.

Honest cost: the *name* "skill" is semantically strained for an always-on rules-file. The name is cosmetic; the
type contract is what W2/W3 test. If the strain matters, rename the type `directive` at zero structural cost.

### 2.2 Rejected type: `workflow` container

A protocol (this repo's `research-scope.md`) is a named collection of ordered, gated steps. A dedicated
container type was rejected: a **composite step** (a step that `invokes` child steps, with `depends-on` among
them) expresses it, and Goose's sub-recipes demonstrate recursion is how the wild does it `[doc-claim: #138
row]`. Cost pre-registered as stress point S4: protocol-level metadata (roles table, INIT invariants, CLOSE
semantics) must land in the composite step's fields/body, which W2 may show is strained.

### 2.3 Retained despite merge pressure: `step` vs `skill`

The strongest collapse candidate: a Recipe/Playbook is markdown, invocable, portable — why isn't it a skill?
Because the two types differ on the load-bearing axis (P-A): a skill's body is *interpreted by the model* after
injection; a step is *scheduled by the harness*, has ordering, completion criteria, and gate attachment, and
per jurati#12 the whole point of the queen is that sequencing is done deterministically outside the LLM. Merging
them would re-blur exactly the request/guarantee line the ontology exists to draw. Boundary case flagged: a
Goose Recipe is a skill *that expands into* steps (skill —invokes→ step is legal for this reason).

### 2.4 Each type's one-line earn

- `skill` — the universal injection mechanism (13/13 tools); remove it and nothing carries content into contexts.
- `agent-def` — the unit identity, attribution, and capability envelopes attach to (jurati#12 single-root
  delegation needs a principal to delegate *to*); remove it and gates have no subject.
- `step` — the only carrier of ordering/completion; remove it and the queen's determinism claim has no object.
- `gate` — the reified request/guarantee distinction (#157/F2: enforcement-outside-the-LLM is the theme's
  validated core thesis); remove it and the ontology collapses into "prompt files."
- `tool` — the stable referent gates and envelopes point at; remove it and `gated-by`/`invokes` lose their range.

Every candidate 6th type found a field, an edge, or an existing type instead: `rule`→skill.activation;
`workflow`→composite step; `permission`→gate(effect) + invokes(mode); `approval`→gate(arbiter:human);
`memory`→deferred to the runtime plane (S1); `artifact`→step.output field.

---

## 3. Anticipated stress points (pre-registered for W2/W3, honest)

- **S1 — Tool-written runtime memory.** Windsurf Memories, Devin Knowledge, Claude auto-memory
  (`MEMORY.md`) are *mutated by the tool at runtime* but *injected like rules*. They straddle the
  definition/event plane split (P-C). Current answer — `skill{owner:tool}` — captures injection but not the
  mutation lifecycle. If W2 round-trips this repo including auto-memory, expect a characterized gap, not a pass.
- **S2 — Observe-only hooks.** This repo's `settings.json` hooks are (mostly) telemetry taps — SessionStart /
  PostToolUse / SubagentStart feeding Unimatrix — not enforcement `[demonstrated]`. Modeling them as
  `gate{effect:observe}` works mechanically but stretches "gate" semantically; and hooks that *inject context
  on an event* (SessionStart output) overlap `skill{activation:event}`. The gate/skill boundary at `event`
  triggers is the spec's fuzziest line. W2 should adjudicate with real cases.
- **S3 — Environment/config that is neither content nor capability.** `enabledMcpjsonServers`, env vars, model
  selection, permission *modes* as session state. Tool `enablement` and agent-def `model` fields catch some;
  a residue of harness-configuration may fit no type. Candidate resolution if W2 confirms: a `config` field-bag
  on the graph root, not a new type.
- **S4 — Protocol-level invariants and policy prose.** research-scope.md's INIT ("open all three surfaces
  FIRST"), CLOSE, rework policy ("REWORK ≤2 → SCOPE-FAIL"), and factory-git's cross-cutting invariants
  ("never `git add -A`") are behavior-bearing prose that lands in opaque bodies. Lossless by P-B (bytes
  preserved), but *behaviorally* it tests W2's harder reading of "can the operating behavior be reconstructed?"
  — the reconstruction relies on the model re-reading prose, which is exactly the request-not-guarantee
  weakness the ontology is supposed to expose. Expect W2 to find the rework policy wants to be a gate field,
  and some invariants want to be gates that don't exist yet (an honest finding about the *repo*, not the spec).
- **S5 — AGENTS.md subsumption is trivially lossless but shallowly so.** Since the standard mandates nothing
  (`[demonstrated: agents.md]`), one `skill{activation:always, scope:{path, precedence:"closest wins"},
  owner:user}` node per file, body preserved, subsumes it — including nested-file precedence. The risk is W3
  declaring victory on a vacuous mapping. The non-vacuous test: *generating* a valid AGENTS.md from a typed
  graph that a third-party tool consumes (H4's done_when Q-a, node #164) — direction matters (graph→file),
  not just file→graph.
- **S6 — Human principals.** `gate{arbiter:human}` covers approvals, but the goal-owner/human appears in
  this repo's protocols as an *actor* (runs reviews, replies on Issues). If W2 needs the human as an assignable
  step principal, `agent-def` would have to admit human principals — defensible but currently unstated.
- **S7 — Definition-plane `invokes` conflates "may" and "does".** The merge of allowlist into
  `invokes(mode:may)` (§1.2) is clean until someone needs "permitted but never wired." Watch in W2.

---

## 4. Sources

**Files (all `[demonstrated]` — read this run):**
- `/workspaces/arch-research/product/research/wfh-002/SCOPE.md` — the question, constraints, H4 proof bar.
- `/workspaces/arch-research/product/research/wfh-001/scout-candidates.md` — mechanism landscape (Partition A table, notable structural mechanisms, syntheses (a)/(b)); all per-vendor rows therein are `[doc-claim]`, secondary-sourced.
- `/workspaces/arch-research/.claude/settings.json` (8 hook events), `/workspaces/arch-research/.claude/settings.local.json` (MCP enablement), `/workspaces/arch-research/.claude/rules/unimatrix-access.md`, `/workspaces/arch-research/.claude/agents/factory/factory-researcher.md`, `/workspaces/arch-research/.claude/agents/factory/research-leader.md`, `/workspaces/arch-research/.claude/skills/factory-git/SKILL.md`, `/workspaces/arch-research/.claude/workflow/research-scope.md`, `/workspaces/arch-research/CLAUDE.md` — the W2 round-trip corpus, skimmed for construct inventory (full mapping is W2's job).
- `.claude/` full file listing: 7 agent-defs, 22 skills (1 with executable asset `opcost.py`), 1 rules file, 6 workflow protocols, 2 settings files.

**Unimatrix nodes (read-only, `agent_id: wfh-002-w1-researcher`):**
- #156 (F1 — AGENTS.md de-facto standard, must subsume losslessly) · #157 (F2 — enforcement-outside-the-LLM shipped/validated) · #164 (H4 — ontology-first; done_when incl. Q-a generation test) · #167 (H7 — definitions vs events) · #170 (conjectured JURATI ontology line, grade:claimed) · #169 (position — moat is ontology+framing).
- Mechanism provenance rows: #134–#146 (harness technologies), #137/#138/#139/#143/#144/#145 cited individually above. All `grade:claimed` — nothing in this spec upgrades any of them.

**External (`[demonstrated]` — fetched this run, 2026-07-22):**
- https://agents.md — standard definition; "just standard Markdown … any headings you like"; no required fields; nested files, "closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."
- `gh issue view 12 --repo dug-21/jurati` — gates/enforcement outside the LLM; queen owns state machine, wave sequencing, gate invocation, capability gating, single-root delegation (Anchor B); Unimatrix deliberately declines enforcement (ADR-008 audit-only).

**Not verified / flagged:** every per-vendor mechanism detail inherited from the wfh-001 scan (apply-mode
counts, load-mode counts, gate tier details) is secondary-sourced `[doc-claim]` and was not re-verified against
vendor docs in this run — the spec's *provenance* citations inherit that confidence level. The spec itself is a
structural hypothesis; its truth-test is W2/W3/W4, not this document.
