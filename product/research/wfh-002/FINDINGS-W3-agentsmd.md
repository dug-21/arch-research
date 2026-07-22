# FINDINGS — W3: AGENTS.md subsumption (wfh-002)

**Workstream:** W3 — `AGENTS.md` subsumption · **Scope:** `wfh-002` (Issue dug-21/arch-research#46) · **Agent:** `wfh-002-w3-researcher`
**Status:** structure-only (research moves *structure*, never *status*). Nothing here asserts a grade; the graph→file direction is verified **on paper only** — the executable proof is W4's template (H4 done_when Q-a, node #164: "a generated AGENTS.md from the typed graph is consumable by at least one third-party tool … demonstrated, not asserted").
**Evidence classes:** `[demonstrated]` = fetched/read this run · `[doc-claim]` = vendor documentation, quoted but behavior not executed by us.

---

## 0. The S5 discipline (read first)

W1 pre-registered stress point **S5**: since the standard mandates nothing, "one `skill{activation:always, scope:{path, precedence:'closest wins'}, owner:user}` node per file, body preserved" subsumes it trivially — and a W3 that stops there has declared victory on a vacuous mapping. This document is structured to refuse that out: §2 does the trivial half honestly (file→graph), §3 does the half that can fail (graph→file generation, specified deterministically and worked on paper), and §4 answers the vacuousness question head-on. The verdict in §5 is conditional on W4 executing §3, not on §2.

---

## 1. The standard, characterized precisely

### 1.1 Normative surface of https://agents.md `[demonstrated: fetched 2026-07-22, first attempt, no retry needed]`

The standard's entire normative content is eight behaviors. Quoted wording is from the site/FAQ.

| # | Behavior | Exact wording (where normative) |
|---|---|---|
| N1 | **Format: no inner structure.** | "No. AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide." (FAQ, *Are there required fields?*) |
| N2 | **Placement.** Root of the repository; monorepos: one per package. | "Create an AGENTS.md file at the root of the repository" · "Place another AGENTS.md inside each package" |
| N3 | **Discovery.** | "Agents automatically read the nearest file in the directory tree" |
| N4 | **Precedence among files.** | "The closest AGENTS.md to the edited file wins" |
| N5 | **Precedence vs the user.** | "explicit user chat prompts override everything" |
| N6 | **Executable checks.** Commands listed in the file are expected to be *run* by the agent. | "Yes—if you list them. The agent will attempt to execute relevant programmatic checks and fix failures before finishing the task." (FAQ) |
| N7 | **Mutability.** User-owned living documentation. | "Treat AGENTS.md as living documentation." |
| N8 | **Compatibility aliasing.** Tools reading other filenames are served by symlinks or tool config. | `ln -s AGENTS.md AGENT.md`; Aider via `.aider.conf.yml`; Gemini CLI via `.gemini/settings.json` |

Adoption claim: 20+ supporting tools listed (OpenAI Codex, Google Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, UiPath, JetBrains Junie, Cursor, Gemini CLI, GitHub Copilot, …) `[doc-claim: agents.md listing; consistent with wfh-001 node #156/F1]`.

### 1.2 Flagship-implementation variance (Codex) — the standard is looser than its biggest reader

The official Codex documentation `[doc-claim: learn.chatgpt.com/docs/agent-configuration/agents-md.md, fetched 2026-07-22 via 308 redirect from developers.openai.com]` implements semantics that **diverge from N4's "closest wins" and extend N2/N3**:

- **Merge, not winner-take-all:** "Codex concatenates files from the root down, joining them with blank lines." Proximity gives *soft* precedence ("Files closer to your current directory override earlier guidance because they appear later in the combined prompt") — recency-weighting, not exclusion.
- **A global layer outside the repo:** `~/.codex/AGENTS.md` (or `CODEX_HOME`) loads before all project files.
- **Intra-directory priority chain:** `AGENTS.override.md` > `AGENTS.md` > `project_doc_fallback_filenames` (config.toml) — "Codex includes at most one file per directory."
- **A byte budget:** "stops adding files once the combined size reaches … `project_doc_max_bytes` (32 KiB by default)."
- **Chain built once per session,** not per edit.

This matters for the ontology: **"precedence" is not one rule but a small family**, and the subsumption target must carry which family member applies (see gap G-2).

### 1.3 Real-world usage sample (6 public repos, fetched this run `[demonstrated]`)

| Repo | Constructs in actual use |
|---|---|
| `openai/codex` | **Real nesting witness**: root `AGENTS.md` (Rust conventions, sandbox env-var rules, lint/lockfile procedures) + nested `codex-rs/tui/src/bottom_pane/AGENTS.md` (directory-scoped doc-sync rules for two state machines). |
| `nocobase/nocobase` | **Dedup bridge**: "`CLAUDE.md` is a one-line bridge (`@AGENTS.md`) so Claude Code reads the same content" — one body, two filenames, maintained by hand. Also a **nonstandard extension convention**: `AGENTS.local.md` "personal rules that extend (but never override) the team rules." Test commands, migrations policy, commit conventions. |
| `DataDog/stratus-red-team` | **Cross-mechanism reference**: "use the `create-attack-technique` skill" — an AGENTS.md pointing at a *skill* by name, in prose. Plus run/test commands. |
| `nextdns/nextdns` | Principles + agent instructions + testing guidance + dependency checklist — pure behavioral prose. |
| `radareorg/radare2` | Code-style and memory-management rules, file-location map, conditional instruction ("Do not run `clang-format-radare2` unless clearly specified by the user"). |
| `google/benchmark` | **Pure policy**: AI-usage disclosure rules aimed at *humans and agents both* — no commands, no style; the file used as a governance notice. |

Observed spread confirms N1: content ranges from executable commands to governance prose, with zero shared structure. Anything that parses the *semantics* would already be broken on this sample; W1's P-B (opaque-body preservation) is the only viable lossless strategy — now witnessed, not just asserted.

---

## 2. file→graph mapping (the trivial half, done honestly)

Every normative behavior lands in the W1 vocabulary. Per-behavior:

| Behavior | Landing zone in W1 spec | Notes |
|---|---|---|
| N1 (no structure) | `skill.body` — markdown, opaque, byte-preserved (P-B) | One node per file. `skill.name` = repo-relative path. |
| N2 (placement) | `skill.scope.path` = directory containing the file | Root file → `scope.path:"/"`. |
| N3 (discovery) | `skill.activation: always` + `scope` | Harness-placed, not model-matched: `always` within scope is exact. |
| N4 (closest wins) | `skill.scope.precedence: "closest-wins"` | Exactly the field W1 §1.1 defined for this purpose. |
| N5 (chat overrides) | **P-A semantics, not a field** | A skill is a *request*; "explicit user prompts override everything" is the definition of request-not-guarantee. Carried by the type's semantics (every `skill` is overridable by the principal's live instruction) — no per-node data needed, but the spec should state it as a type-level invariant (see G-0). |
| N6 (checks run) | `skill.body` (prose) — **with an optional typed promotion** | In AGENTS.md-world the model *chooses* to run checks: a request. Lossless as body. But the same intent is expressible as `gate{trigger:step-boundary, predicate:<command>, arbiter:program}` + `tool` nodes — see §4; this is the single biggest value-add of typing. |
| N7 (living doc) | `skill.owner: user` + `version`/`source_ref` | |
| N8 (aliasing) | **Not an ontology concern** — generator-profile emission rule | The graph holds one node; which filenames/symlinks/config-stanzas get emitted per consuming tool is serialization (§3.4). Optional `aliases` field if wanted; not required. |

Real-world constructs beyond the letter of the standard:

- `stratus-red-team`'s "use the create-attack-technique skill" → representable as an **`invokes` edge (skill → skill)** — legal in W1 §1.2's range. In the flat file it is unverifiable prose; in the graph it is a checkable reference (dangling-skill detection). Import automation cannot extract it reliably (it's prose), so the *lossless* import keeps it in the body; the edge is an optional enrichment. No gap.
- `nocobase`'s `AGENTS.local.md` ("extend but never override") → a second `skill` node, same `scope.path`, the extend-don't-override semantics living in prose (a request, per P-A). Representable; exposes gap G-1 (intra-directory ordering) for the *typed* version of that guarantee.
- Codex's `AGENTS.override.md` chain, global layer, byte budget → gaps G-1, G-3, G-4 below.

### Gap list (file→graph), each with a minimal fix

| # | Gap | Minimal fix | Severity |
|---|---|---|---|
| G-0 | N5 (chat-prompt override) is carried implicitly by P-A but the W1 spec never states it as an invariant | One sentence in the spec: "every `skill` is a request; live principal instructions outrank all skill bodies" | cosmetic |
| G-1 | Intra-directory priority (override-file > main > fallbacks; local-extends-team) has no field — `scope` orders *directories*, not files *within* one | `scope.priority: int` (or a params slot on `precedence`) | low — needed only for the Codex *extension*, not the standard |
| G-2 | `scope.precedence` is free-text in W1; the wild has ≥2 distinct semantics (winner-take-all "closest-wins" vs Codex "concat-root-down, nearest-last") | Make it an enum: `closest-wins \| concat-nearest-last` (open) | low, but real — a generator must know which to assume |
| G-3 | Global-layer files (`~/.codex/AGENTS.md`) sit outside any repo; W1's graph is implicitly per-project | `scope.layer: global \| project \| directory` (default `directory`) | low |
| G-4 | Instruction byte-budget (`project_doc_max_bytes`) is neither content nor capability | Confirms W1's **S3** residue: harness-config field-bag, not a type | none (pre-registered) |

**No gap requires a new node type or a new edge type.** All fixes are field-level. The standard's core (N1–N8) maps with zero gaps; G-1..G-3 are triggered only by the flagship implementation's extensions.

---

## 3. graph→file generation (the non-vacuous half — H4 done_when Q-a, paper spec)

**Claim under test:** given a typed graph, a deterministic procedure generates a valid AGENTS.md file tree that any conforming tool consumes. Specified here, verified on a worked example **on paper**; W4's template is the executable proof.

### 3.1 Selection rule (which nodes)

A `skill` node S is **selected** for the `agentsmd` target iff:

1. `S.activation == always` — the standard has no matched/explicit/event activation; and
2. `S.owner == user` — tool-written memory (W1 S1) is excluded; and
3. `S.scope`, if present, names a directory subtree (not a glob) — see downgrade rule D-1.

Non-`skill` nodes are never *selected*; they may be *rendered* by downgrade rules (3.3).

### 3.2 Placement + ordering rules (where files land, how nesting derives)

- **P-1 (placement).** Group selected skills by `scope.path` (absent → `/`). Each group emits exactly one `AGENTS.md` at that directory. Nesting therefore *derives* from `scope`: distinct scope paths ⇒ nested files; the standard's own N3/N4 discovery then reproduces the intended precedence by construction.
- **P-2 (ordering within a file).** Topological by `depends-on` where present; ties broken by stable name-sort. Bodies emitted verbatim, joined by one blank line.
- **P-3 (round-trip stability).** A file imported as one node (the §2 rule) re-emits **byte-identical** — trivially, since P-1 puts one body in one file. An *authored* graph folding k>1 nodes into one file emits a deterministic concatenation; re-import yields one node, so the cycle is idempotent from the first regeneration but the k-node structure is not recoverable from the file alone. **A generator manifest (sidecar in the template, W4's design space) is required if the graph, not the files, is the source of truth.** Flagged, not hidden.

### 3.3 Downgrade rules (constructs richer than the standard)

The ontology strictly exceeds AGENTS.md; generation is **total but projective**. Every loss is explicit:

- **D-1 (glob scopes).** `scope` carrying a glob (e.g. `**/*.ts`) has no placement equivalent — AGENTS.md's only scoping mechanism is directory position. Render into the nearest covering directory's file under a deterministic preamble ("Applies to `*.ts`: …"). *Semantic downgrade: harness-placed → model-interpreted.*
- **D-2 (gates).** A `gate` reachable from selected scope MAY render as check-prose — e.g. `gate{trigger:step-boundary, predicate:"make test", arbiter:program}` → "Run `make test` and fix failures before finishing." This is precisely idiom N6, i.e. **the standard's own check-idiom is the prose shadow of a gate**. *Downgrade: guarantee → request* — the exact P-A axis, so the type system names the loss.
- **D-3 (agent-def, step, tool, non-always skills).** No landing zone. Omitted from `agentsmd` output; generator reports them as `[unrepresentable in target]`. They are NOT lost from the graph — they emit to richer targets (`.claude/` etc., W2/W4's side).

### 3.4 Aliasing (N8) as a generator profile

Per-tool emission rules live outside the type system: profile `claude-code` may emit `CLAUDE.md` containing `@AGENTS.md` (exactly nocobase's hand-maintained bridge, §1.3 — evidence the need is real and currently solved manually); profile `aider` emits the `.aider.conf.yml` stanza; symlink emission for `AGENT.md` readers. One node, n serializations — dedup by construction.

### 3.5 Worked example (paper verification)

**Input graph** (7 nodes, 4 edges):

```
skill  S1 {name:"repo-conventions",  activation:always, owner:user, scope:{path:"/", precedence:"closest-wins"}}
       body: "Use pnpm, not npm. TypeScript strict mode everywhere."
skill  S2 {name:"api-package-rules", activation:always, owner:user, scope:{path:"/packages/api", precedence:"closest-wins"}}
       body: "All endpoints need an OpenAPI entry. No direct DB access outside /packages/api/src/db."
skill  S3 {name:"security-review",   activation:matched, owner:user, description:"security-sensitive changes"}
tool   T1 {name:"pnpm", provider:builtin}
gate   G1 {name:"tests-pass", trigger:step-boundary, predicate:"pnpm test", effect:deny, arbiter:program, locus:harness}
gate   G2 {name:"lint-on-pr", trigger:vcs-action(pr), predicate:"pnpm lint", effect:deny, arbiter:program, locus:platform}
agent-def A1 {name:"reviewer", ...}
edges: S1 -invokes→ T1 · S2 -depends-on→ S1 · (step)*-gated-by→ G1 · A1 -invokes→ T1
```

**Generation (`agentsmd` target), rule by rule:**

1. Selection: S1 ✓, S2 ✓ (always+user+dir-scope). S3 ✗ (`matched` — D-3). T1, G1, G2, A1 ✗ (non-skill).
2. Placement (P-1): S1 → `/AGENTS.md`; S2 → `/packages/api/AGENTS.md`.
3. Downgrade (D-2, gates elected for rendering): G1 → root file, "## Checks — Run `pnpm test` and fix failures before finishing." `[downgraded: gate→prose]`; G2 → "PRs must pass `pnpm lint` (enforced by CI)." `[downgraded: gate→prose; enforcement remains at locus:platform]`.
4. Report: S3, A1, T1 `[unrepresentable in target — emitted only to richer targets]`.

**Generated tree:**

```
AGENTS.md                      ← S1 body + G1/G2 check-prose
packages/api/AGENTS.md         ← S2 body
```

**Consumption check (against the quoted semantics, on paper):** a conforming tool editing `packages/api/src/routes.ts` reads the nearest file (N3): `packages/api/AGENTS.md`; under N4 it wins over root; under Codex's variant both load, package file last (nearest-last recency precedence) — **both semantics produce the intended behavior** (S2 refines S1 in API scope), because P-1 derived the nesting from `scope` exactly as the standard's discovery expects. A user chat prompt saying "use npm just this once" overrides S1 (N5) — consistent with the graph, where S1 is a `skill`, i.e. a request. G1's *intent* survives only as strongly as the model's compliance — the D-2 flag says so, and the same graph emits G1 as a real enforcing hook for a harness target that has one.

**This is a paper verification.** Nothing here was executed against a third-party tool. Q-a is met only when W4's template generates these files and a standard-reading tool demonstrably consumes them.

---

## 4. The vacuousness question, answered head-on

**What does the typed representation ADD over the flat file?**

1. **Multi-target generation / dedup.** One graph → `AGENTS.md` + `CLAUDE.md` + tool config stanzas. nocobase maintains exactly this bridge *by hand today* (§1.3) — demonstrated evidence the problem exists and the ecosystem's current answer is manual symlinks and `@`-includes.
2. **Request→guarantee promotion.** The standard's own N6 ("run checks, fix failures") is an *unenforced request*. Typed as `gate` + `tool`, the same intent emits as prose for AGENTS.md-only tools AND as a real hook for harnesses with enforcement — the P-A axis made actionable. This is the ontology's core thesis (#157/F2) applied to the standard's weakest point.
3. **Queryable structure + conflict detection.** Which scopes exist; two skills claiming one directory; prose references to skills (stratus §1.3) become checkable `invokes` edges; dangling references detectable. None of this is expressible over a pile of flat files.
4. **Precedence made explicit.** The wild has ≥2 divergent precedence semantics (§1.2) that users discover by surprise; `scope.precedence` as an enum names the behavior per node instead of leaving it to implementation folklore.

**What does it LOSE?**

1. **Byte-identity beyond 1-node-per-file.** Folding multiple typed nodes into one file needs a manifest to invert (P-3). If the *files* stay the source of truth (git-native, W4's premise), this cost vanishes.
2. **The standard's core virtue is user-owned simplicity** ("just Markdown"). A graph that requires users to edit nodes instead of files would fight the ecosystem the same way a 25th rules-format would. Consequence for W4: the template must keep files as the editing surface and treat the graph as derived-or-synced, not as a replacement UI.
3. **Nothing semantic.** No normative behavior of the standard failed to map (§2); the losses are representational overhead, not dropped semantics.

**Is the mapping vacuous?** The file→graph half alone would be (S5's warning — it types nothing the file didn't already say). The subsumption claim is rescued from vacuity by the generation direction: §3 commits to deterministic, falsifiable rules (selection, placement, ordering, downgrades) that can *fail* when W4 runs them — a third-party tool either consumes the generated tree correctly or it doesn't. A claim that can fail is not vacuous; it is merely unproven until W4.

---

## 5. Subsumption verdict

**file→graph: LOSSLESS** for the standard's full normative surface (N1–N8), with zero gaps against the standard proper and four field-level gaps (G-0..G-3, minimal fixes named, no new types/edges) against flagship-implementation extensions. The lossless strategy is P-B by necessity — §1.3's sample shows there is no shared inner structure to type.

**graph→file: TOTAL but PROJECTIVE** — every graph generates a valid, standard-conforming AGENTS.md tree; constructs richer than the standard downgrade with explicit flags (glob→prose, gate→check-prose, agent-def/step/tool omitted-for-this-target). The asymmetry is correct and expected: subsumption requires standard ⊆ ontology, which holds; ontology ⊆ standard does not and should not.

**Verdict: SUBSUMES, non-vacuously specified, pending executable demonstration (W4).** On the S5 scale: this is a paper-verified generation spec, deliberately short of Q-a's bar, which demands a third-party tool consuming generated output.

**Spec feedback to W1** (structure only): adopt G-0 (state N5 as a type invariant) and G-2 (precedence enum); G-1/G-3 optional until a target needs Codex's extensions.

---

## 6. Sources

**External `[demonstrated]` — fetched this run, 2026-07-22:**
- https://agents.md — standard + FAQ (N1–N8 quotes; supporting-tools list). Fetched first attempt.
- https://learn.chatgpt.com/docs/agent-configuration/agents-md.md (308-redirect from developers.openai.com/codex/guides/agents-md.md) — Codex discovery/merge/override/budget semantics `[doc-claim as to runtime behavior — quoted, not executed]`.
- Repo files via `gh api` `[demonstrated — raw content read]`: `openai/codex` `AGENTS.md` + `codex-rs/tui/src/bottom_pane/AGENTS.md`; `nocobase/nocobase`, `DataDog/stratus-red-team`, `nextdns/nextdns`, `radareorg/radare2`, `google/benchmark` `AGENTS.md`.
- `gh search code --filename AGENTS.md` — sample frame (casing variants `AGENTS.md`/`agents.md`/`Agents.md` observed in the wild; the standard names only `AGENTS.md`).

**Files:**
- `/workspaces/arch-research/product/research/wfh-002/SCOPE.md` — W3 charge, proof bar.
- `/workspaces/arch-research/product/research/wfh-002/FINDINGS-W1-ontology-spec.md` — the spec under test (skill/activation/scope/owner; P-A/P-B/P-C; S5 pre-registration).

**Unimatrix (read-only, `agent_id: wfh-002-w3-researcher`):**
- #156 (F1 — AGENTS.md de-facto standard; subsume losslessly) · #164 (H4 — done_when Q-a: "generated AGENTS.md from the typed graph is consumable by at least one third-party tool … demonstrated, not asserted").

**Not verified / flagged:** Codex's runtime merge behavior is quoted from official docs, not executed by us; casing-tolerance of readers (`agents.md` vs `AGENTS.md`) unverified; the 20+ supporting-tools list is the site's own claim; whether each listed tool implements N4 ("closest wins") vs Codex-style concatenation is unknown per tool — only Codex's variant was doc-verified. None of this affects the file→graph mapping; it affects which `precedence` enum value a generator should assume per consuming tool (G-2).

---

## Summary

Verdict: **AGENTS.md SUBSUMES into the W1 ontology — file→graph lossless (zero gaps vs the standard, 4 field-level gaps vs Codex extensions, no new types/edges needed); graph→file total-but-projective, specified as deterministic falsifiable rules and worked on paper.** The vacuity trap (S5) is escaped by the generation spec, not the mapping. Spec feedback to W1: make `scope.precedence` an enum (closest-wins | concat-nearest-last) and state the chat-override invariant.

**W4 must demonstrate, to make Q-a executable:** run §3's rules from a typed graph in the template repo, generating at least (a) a root `AGENTS.md` and one *nested* directory-scoped `AGENTS.md`, (b) one gate→check-prose downgrade explicitly flagged in output, and (c) have a third-party standard-reading tool (Codex or Gemini CLI are doc-verified readers) actually consume the generated tree and follow a scoped instruction — plus decide the P-3 manifest question (files-as-source-of-truth vs graph-with-sidecar).
