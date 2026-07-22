# FINDINGS — W2: Lossless round-trip (wfh-002)

**Workstream:** W2 — Lossless round-trip · **Scope:** `wfh-002` (Issue dug-21/arch-research#46) · **Agent:** `wfh-002-w2-researcher`
**Status:** structure-only (research moves *structure*, never *status*). No grades asserted.
**Evidence classes:** `[demonstrated]` = read/verified by direct file read or command in this run · `[doc-claim]` = asserted by a file's prose, not behaviorally verified · `[inferred]` = behavior deduced from this session's own observed context, not from repo bytes.

---

## 0. Corpus inventory (verified by `find`, not the task brief)

`find /workspaces/arch-research/.claude -type f` returns **37 files** `[demonstrated]`:

| Class | Count | Files |
|---|---|---|
| SKILL.md | **20** (not 22 — see note) | `.claude/skills/*/SKILL.md` |
| Skill asset | 1 | `.claude/skills/opcost/opcost.py` |
| Agent-defs | 7 | `.claude/agents/factory/{factory-curator,factory-researcher,goal-owner,hypothesizer,research-leader,scout}.md` + `.claude/agents/sample-sm.md` |
| Rules | 1 | `.claude/rules/unimatrix-access.md` |
| Workflow protocols | 6 | `.claude/workflow/{decompose-scope,research-scope,theme-scan,sample-delivery,sample-design,sample-research}.md` |
| Settings | 2 | `.claude/settings.json` (2394 B, hooks only — **no permissions block exists**), `.claude/settings.local.json` (53 B) |

**Inventory correction:** the task brief and W1 say "22 skills." Exactly **20** `SKILL.md` files exist. The count 22 reconciles only under the W1 ontology itself: 20 SKILL.md + `CLAUDE.md` + `unimatrix-access.md` = **22 skill-typed nodes** (the merged `skill` type absorbs rules-files). Declared, not silent.

**Also in corpus (found, mapped):**
- `/workspaces/arch-research/CLAUDE.md` (3107 B)
- `/workspaces/arch-research/.mcp.json` (256 B) — MCP server definition (unimatrix bridge). Not listed in the task brief; found and included.
- Claude auto-memory: `~/.claude/projects/-workspaces-arch-research/memory/{MEMORY.md, garage-multi-project-platform.md, jurati-workflow-harness.md}` (S1 target).

**Declared omissions (found, NOT expressed — with reason):**
- `.devcontainer.json` + `.devcontainer/postCreate.sh` — environment provisioning (node/python/rust/docker/gh features, ssh mounts). Operating *environment*, not operating *context*; used below as an S3 witness only.
- `~/.claude/settings.json` (user scope: `{"theme":"dark","skipDangerousModePermissionPrompt":true}`) — user-level harness config outside the repo; S3 witness. Notably `skipDangerousModePermissionPrompt` is a **gate-bypass toggle** living entirely outside the corpus.
- Harness built-ins injected at runtime (built-in tools, plugin skills like `dataviz`, the system prompt itself) — not repo artifacts; their *referents* appear as `tool` stub nodes where repo files invoke them.
- GitHub repo-level settings (rebase-only, auto-merge, delete-branch-on-merge) — asserted by `factory-git/SKILL.md` prose `[doc-claim]`; the actual gate definitions live in GitHub, not in any repo byte. Expressed as `gate{locus:platform}` nodes with `source_ref: external`.

---

## 1. The expressed graph

Conventions used below (consumable by W4): every node carries `source_ref` (path, or `null` for stubs, or `external`) and an implicit `body: <file bytes, opaque>` per P-B. `activation` values follow W1 §1.1. Edge syntax: `A -edge(params)-> B`.

### 1.1 Skill nodes (25)

```yaml
skills:
  # --- 20 SKILL.md files. Claude Code skills are BOTH description-matched (harness/model
  # decides) AND explicitly invocable (/name) — see gap G-C: activation must be a set.
  - {name: factory-git,          activation: [matched, explicit], owner: user, source_ref: .claude/skills/factory-git/SKILL.md}
  - {name: factory-onboard,      activation: [matched, explicit], owner: user, source_ref: .claude/skills/factory-onboard/SKILL.md}
  - {name: factory-retro,        activation: [matched, explicit], owner: user, source_ref: .claude/skills/factory-retro/SKILL.md}
  - {name: opcost,               activation: [matched, explicit], owner: user, source_ref: .claude/skills/opcost/SKILL.md,
     assets: [.claude/skills/opcost/opcost.py]}
  - {name: uni-capability,       activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-capability/SKILL.md}
  - {name: uni-git,              activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-git/SKILL.md,
     note: "NO YAML frontmatter — name derived from directory, description from H1 [demonstrated]. Bar-1 witness G-G."}
  - {name: uni-init,             activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-init/SKILL.md}
  - {name: uni-knowledge-lookup, activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-knowledge-lookup/SKILL.md}
  - {name: uni-knowledge-search, activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-knowledge-search/SKILL.md}
  - {name: uni-query-patterns,   activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-query-patterns/SKILL.md}
  - {name: uni-release,          activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-release/SKILL.md}
  - {name: uni-retro,            activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-retro/SKILL.md}
  - {name: uni-review-pr,        activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-review-pr/SKILL.md}
  - {name: uni-seed,             activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-seed/SKILL.md}
  - {name: uni-store-adr,        activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-store-adr/SKILL.md}
  - {name: uni-store-lesson,     activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-store-lesson/SKILL.md}
  - {name: uni-store-pattern,    activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-store-pattern/SKILL.md}
  - {name: uni-store-procedure,  activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-store-procedure/SKILL.md}
  - {name: uni-zero,             activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-zero/SKILL.md}
  - {name: uni-zero-review,      activation: [matched, explicit], owner: user, source_ref: .claude/skills/uni-zero-review/SKILL.md}

  # --- rules-files absorbed by the skill type (W1 §2.1)
  - {name: claude-md,            activation: always, owner: user, source_ref: CLAUDE.md,
     scope: {path: /, precedence: "project layer of harness CLAUDE.md layering"}}
  - {name: unimatrix-access,     activation: always, owner: user, source_ref: .claude/rules/unimatrix-access.md,
     scope: {path: /, note: "injected alongside CLAUDE.md as project instructions [inferred: present verbatim in this session's own injected context]"},
     note: "binding-on-roles policy prose — S4 witness: its deny rules (curator-only writes) have NO mechanical gate"}

  # --- S1: tool-written auto-memory (owner:tool)
  - {name: memory-index,         activation: always, owner: tool,
     source_ref: ~/.claude/projects/-workspaces-arch-research/memory/MEMORY.md,
     note: "injected every session [inferred: present in this session's context]"}
  - {name: memory-garage-multi-project-platform, activation: matched, owner: tool,
     source_ref: ~/.claude/projects/-workspaces-arch-research/memory/garage-multi-project-platform.md,
     note: "loaded on demand via index line; frontmatter carries metadata.originSessionId — provenance the ontology has no field for (S1)"}
  - {name: memory-jurati-workflow-harness, activation: matched, owner: tool,
     source_ref: ~/.claude/projects/-workspaces-arch-research/memory/jurati-workflow-harness.md,
     note: "contains [[wiki-links]] between memory files — an intra-plane reference mechanism outside the 4 edges (body-level per P-B, acceptable)"}
```

### 1.2 Agent-def nodes (7 defined + 21 stubs + 1 human)

```yaml
agent_defs:
  - {name: research-leader,   type: coordinator, scope: broad,  source_ref: .claude/agents/factory/research-leader.md,
     capability_envelope: {tools: [context_cycle, gh, git, Task], closed: true,
       note: "'context_cycle ONLY' — an EXHAUSTIVE (closed-world) envelope stated in prose; S7 witness"}}
  - {name: factory-researcher, type: specialist, scope: targeted, source_ref: .claude/agents/factory/factory-researcher.md,
     capability_envelope: {tools: [context_search, context_get, context_graph], closed: true, mode: read-only}}
  - {name: factory-curator,   type: specialist, scope: targeted, source_ref: .claude/agents/factory/factory-curator.md,
     capability_envelope: {tools: [context_store, context_correct, context_tag, context_edge, context_search], closed: false},
     note: "single-writer rule — enforcement is prose-only (S4)"}
  - {name: goal-owner,        type: specialist, scope: targeted, source_ref: .claude/agents/factory/goal-owner.md,
     note: "dual-role (synthesis review + triage) — one def, two step-assignments; expresses as two invokes edges from different steps, no strain"}
  - {name: hypothesizer,      type: specialist, scope: exploratory, model: claude-fable-5,
     source_ref: .claude/agents/factory/hypothesizer.md,
     note: "the model field witness (W1 optional field: model) — model pinning is load-bearing (A/B telemetry pins it)"}
  - {name: scout,             type: specialist, scope: exploratory, source_ref: .claude/agents/factory/scout.md,
     capability_envelope: {tools: [context_search, context_get, context_graph, WebSearch, WebFetch, Read, Grep, Glob], closed: true}}
  - {name: uni-scrum-master,  type: coordinator, scope: broad, source_ref: .claude/agents/sample-sm.md,
     note: "invokes .claude/protocols/uni/{design,delivery,bugfix}-protocol.md — paths that DO NOT EXIST in this repo (G-D dangling refs)"}

  # --- STUB nodes: principals referenced by protocols/skills with NO definition file in this
  # repo. The vocabulary as specced cannot say 'this node has no source' — see gap G-D.
  - stubs (source_ref: null, defined: false):
      referenced_by_factory_protocols: [factory-poc, factory-validator]        # research-scope.md roles
      referenced_by_sample_protocols:  [uni-researcher, uni-architect, uni-specification,
        uni-risk-strategist, uni-vision-guardian, uni-synthesizer, uni-validator, uni-pseudocode,
        uni-tester, uni-rust-dev, uni-js-dev, uni-docs, uni-zero-reviewer,
        uni-spike-researcher, uni-external-researcher, uni-research-sm, uni-bug-investigator]
      referenced_by_skills: [uni-security-reviewer]                            # uni-review-pr
  - {name: human-owner, kind: human, source_ref: null,
     note: "S6 — the human appears as gate arbiter (covered) AND as initiating actor (Wave-0 kick, Issue replies, 'human starts Session 2'); admitted here as a principal per W1's anticipated resolution"}
```

### 1.3 Step nodes (composite steps = protocols; W1 §2.2)

```yaml
steps:
  - name: research-scope            # source_ref: .claude/workflow/research-scope.md
    children:                       # composite via invokes; sibling order via depends-on
      - {name: rs-init,  objective: "open all three surfaces (Issue, cycle, git)", output: "Issue + cycle(topic, wf-tag) + branch",
         invokes: [gh, context_cycle, git]}
      - {name: rs-scope, assigned: factory-researcher, output: SCOPE.md, gated_by: rs-scope-gate}
      - {name: rs-tech-discovery, assigned: [factory-researcher xN parallel, factory-curator],
         output: "FINDINGS files + claimed technology/finding nodes", gated_by: rs-coverage-gate}
      - {name: rs-feasibility, condition: "confidence-required in {validated, empirical}",   # <-- G-B: no condition field exists in W1
         assigned: [factory-poc, factory-validator, factory-curator], output: "verified artifact + proven/partial",
         gated_by: rs-firewall-gate}
      - {name: rs-synthesis, assigned: [factory-curator, goal-owner], output: "position finding + REPORT.md + relevance.md",
         gated_by: rs-synthesis-gate}
      - {name: rs-close, invokes: [context_cycle, git, factory-retro], output: "cycle stop + auto-merged PR"}
    depends_on_chain: rs-init -> rs-scope -> rs-tech-discovery -> [rs-feasibility] -> rs-synthesis -> rs-close
    telemetry: "context_cycle phase-end at every boundary (step invokes tool — expresses cleanly)"

  - name: theme-scan                # source_ref: .claude/workflow/theme-scan.md
    children:
      - {name: ts-init, output: "3 surfaces + theme/budget confirmation", gated_by: ts-init-gate}
      - {name: ts-scan, assigned: scout xN, output: scout-candidates.md,
         note: "'NO graph writes in this phase' — a phase-scoped deny with no gate (S4 witness)"}
      - {name: ts-hypothesize, assigned: hypothesizer x1-per-candidate, output: hypotheses.md, gated_by: ts-fanout-coverage}
      - {name: ts-triage, assigned: goal-owner, output: reports/triage.md, gated_by: ts-owner-gate}
      - {name: ts-formalize, assigned: factory-curator, output: "3-tier graph writes",
         condition: "post ts-owner-gate only"}
      - {name: ts-close, invokes: [context_cycle, git, factory-retro], output: "funnel counts + merged PR"}
    depends_on_chain: ts-init -> ts-scan -> ts-hypothesize -> ts-triage -> ts-formalize -> ts-close

  - name: decompose-scope           # source_ref: .claude/workflow/decompose-scope.md
    children:
      - {name: ds-init, output: "cycle + Issue"}
      - {name: ds-scope, assigned: factory-researcher, output: SCOPE.md, gated_by: ds-scope-gate}
      - {name: ds-decompose, assigned: [factory-researcher, factory-curator], output: "goal + capability board", gated_by: ds-board-gate}
      - {name: ds-close, invokes: [context_cycle], output: "board = durable queue"}

  # --- sample protocols (SDLC imports; all assigned principals are G-D stubs)
  - name: sample-research           # source_ref: .claude/workflow/sample-research.md
    children:
      - {name: sr-scope-precheck, objective: "verify SCOPE.md complete; missing field -> STOP and ask human",
         note: "a HALT-on-predicate written as prose — wants gate{trigger:step-boundary, effect:halt, arbiter:program} but is enforced by model compliance (S4)"}
      - {name: sr-route, condition: "3-case routing by Breadth/Confidence/Goal-question partitionability",  # G-B witness
         output: "researcher selection (Case 1/2/3)"}
      - {name: sr-execute, assigned: [uni-spike-researcher | uni-external-researcher | both-parallel], output: "FINDINGS*.md"}
      - {name: sr-synthesize, condition: "dual-track only", assigned: uni-spike-researcher, output: FINDINGS.md}
      - {name: sr-validate, objective: "checklist vs SCOPE", gated_by: sr-validation-gate}
      - {name: sr-route-out, invokes: [gh], output: "Issue comment; human closes"}

  - name: sample-design             # source_ref: .claude/workflow/sample-design.md
    children: [sd-p1-scope{uni-researcher}, sd-p1r-review{uni-zero-reviewer, advisory}, sd-p1-human-approve{gate},
      sd-p1b-scope-risk{uni-risk-strategist}, sd-p2a-arch+spec{uni-architect ∥ uni-specification, parallel},
      sd-p2a2-risk{uni-risk-strategist}, sd-p2b-vision{uni-vision-guardian}, sd-p2c-synthesis{uni-synthesizer},
      sd-p2c2-review{uni-zero-reviewer}, sd-p2d-return-to-human]
    note: "cycle stays OPEN across sessions (stop deferred to delivery) — cross-composite state the graph can express only in prose"

  - name: sample-delivery           # source_ref: .claude/workflow/sample-delivery.md
    children: [dl-init{precondition: brief-exists else STOP}, dl-3a-design{uni-pseudocode ∥ uni-tester},
      dl-map-update{leader, MANDATORY}, dl-gate-3a, dl-3b-impl{waves of uni-rust-dev|uni-js-dev,
        condition: "dev-agent selected per component language"},                                  # G-B witness
      dl-gate-3b, dl-3c-test{uni-tester}, dl-gate-3c, dl-p4-deliver{gh, uni-docs conditional,
        uni-review-pr skill, uni-zero-reviewer}]
```

### 1.4 Gate nodes (8 hook gates + 12 protocol gates + platform gates)

```yaml
gates:
  # --- settings.json hooks [demonstrated]. ALL 8 run the SAME external program
  # (@dug-21/unimatrix hook-client with the event name as argv). CRITICAL HONESTY (S2/G-F):
  # the `effect` of each gate is NOT recoverable from the corpus — settings.json declares
  # trigger + command only; effect lives in the hook program's exit-code/stdout behavior,
  # outside this repo. effect below is presumed-observe [doc-claim: W1 S2 characterization].
  - {name: hook-session-start,     trigger: {event: SessionStart,      matcher: ""},  predicate: {command: "node .../hook-client/index.js SessionStart"},
     effect: unknown/presumed-observe+inject, arbiter: program, locus: harness,
     note: "SessionStart output can inject context — the gate/skill{activation:event} blur, adjudicated in S2"}
  - {name: hook-stop,              trigger: {event: Stop,              matcher: ""},  predicate: {command: ".../index.js Stop"},              effect: unknown/presumed-observe, arbiter: program, locus: harness}
  - {name: hook-user-prompt,       trigger: {event: UserPromptSubmit,  matcher: ""},  predicate: {command: ".../index.js UserPromptSubmit"},  effect: unknown/presumed-observe, arbiter: program, locus: harness}
  - {name: hook-pre-tool-use,      trigger: {tool-call: "^context_cycle$|^mcp__unimatrix__context_cycle$"}, predicate: {command: ".../index.js PreToolUse"},
     effect: unknown/presumed-observe, arbiter: program, locus: harness,
     note: "the one matcher-scoped hook — clean witness for gated-by pair-specificity via predicate matcher (W1 §1.2)"}
  - {name: hook-post-tool-use,     trigger: {tool-call: "*", timing: post}, predicate: {command: ".../index.js PostToolUse"},        effect: unknown/presumed-observe, arbiter: program, locus: harness}
  - {name: hook-post-tool-failure, trigger: {tool-call: "*", timing: post-failure}, predicate: {command: ".../index.js PostToolUseFailure"}, effect: unknown/presumed-observe, arbiter: program, locus: harness}
  - {name: hook-pre-compact,       trigger: {event: PreCompact,        matcher: ""},  predicate: {command: ".../index.js PreCompact"},        effect: unknown/presumed-observe, arbiter: program, locus: harness}
  - {name: hook-subagent-start,    trigger: {event: SubagentStart,     matcher: "*"}, predicate: {command: ".../index.js SubagentStart"},     effect: unknown/presumed-observe, arbiter: program, locus: harness}

  # --- permission rules: NONE. Neither settings file contains a permissions block
  # [demonstrated]. The entire allow/deny surface of this repo is prose (S4).

  # --- protocol gates (research-scope / theme-scan / decompose-scope)
  - {name: rs-scope-gate,     trigger: step-boundary, arbiter: human, blocking: advisory, effect: ask}
  - {name: rs-coverage-gate,  trigger: step-boundary, arbiter: human, blocking: blocking, effect: deny-until-pass,
     failure_handling: "REWORKABLE re-spawn prior phase max 2, else SCOPE-FAIL"}          # G-E: loop topology is prose
  - {name: rs-firewall-gate,  trigger: step-boundary, blocking: blocking, effect: deny,
     arbiter: MIXED — predicate "verified demonstrated-by-us artifact" checked by factory-validator (an LLM agent) + curator rule,
     note: "G-A witness: the arbiter is an AGENT, not {program|human}"}
  - {name: rs-synthesis-gate, trigger: step-boundary, arbiter: human, blocking: advisory,
     inputs: "goal-owner verdict relayed VERBATIM (leader forbidden to act on it — itself an S4 prose invariant)"}
  - {name: ts-init-gate,      trigger: step-boundary, arbiter: human(owner), blocking: advisory}
  - {name: ts-fanout-coverage,trigger: step-boundary, arbiter: agent(research-leader), blocking: advisory, failure_handling: "re-spawn <=2"}
  - {name: ts-owner-gate,     trigger: step-boundary, arbiter: human(owner), blocking: blocking, effect: "promote 0..n"}
  - {name: ds-scope-gate,     trigger: step-boundary, arbiter: human, blocking: advisory}
  - {name: ds-board-gate,     trigger: step-boundary, arbiter: human, blocking: advisory}
  - {name: dl-gate-3a/3b/3c,  trigger: step-boundary, blocking: blocking,
     arbiter: agent(uni-validator) — G-A witness,
     failure_handling: "REWORKABLE max 2 -> SCOPE FAIL",
     note: "verdict produced BY an LLM subagent and enforced by the leader following prose — per P-A these are requests dressed as gates; the vocabulary cannot currently say so"}
  - {name: sr-validation-gate, trigger: step-boundary, arbiter: agent(leader-checklist), blocking: blocking}

  # --- platform/vcs gates (definitions live OUTSIDE the corpus; [doc-claim: factory-git,
  # uni-git prose])
  - {name: gh-rebase-only,          trigger: vcs-action(merge), arbiter: program, locus: platform, effect: deny, source_ref: external}
  - {name: gh-auto-merge,           trigger: vcs-action(pr),    arbiter: program, locus: platform, effect: allow, source_ref: external}
  - {name: gh-delete-branch,        trigger: vcs-action(merge), arbiter: program, locus: platform, effect: transform, source_ref: external}
  - {name: pre-commit-hooks,        trigger: vcs-action(commit), arbiter: program, locus: vcs, effect: deny,
     source_ref: external, note: "referenced only by uni-git prose ('never skip --no-verify')"}
```

### 1.5 Tool nodes (24)

```yaml
tools:
  mcp:      # provider: mcp; enablement chain: .mcp.json (server def) + settings.local.json enabledMcpjsonServers:["unimatrix"] [demonstrated]
    [context_search, context_get, context_graph, context_lookup, context_cycle, context_cycle_review,
     context_store, context_correct, context_tag, context_edge, context_deprecate, context_status, context_briefing]
  builtin:  # provider: builtin; no definition bytes in corpus (referents only)
    [Bash, Read, Grep, Glob, Write, Task(spawn), WebSearch, WebFetch]
  platform: [git, gh]
  script:
    - {name: opcost.py,   provider: script/asset, interface: "argparse: --days --repo --all --cost [demonstrated]", source_ref: .claude/skills/opcost/opcost.py}
    - {name: hook-client, provider: script, source_ref: "/home/vscode/.npm/_npx/39eded8816df3abb/node_modules/@dug-21/unimatrix/lib/hook-client/index.js",
       note: "MACHINE-SPECIFIC absolute path (npx cache hash) embedded in settings.json — byte-preservable, behaviorally non-portable (S3)"}
    - {name: mcp-bridge,  provider: script, source_ref: "same npx cache path .../mcp-bridge.js + instance arg 416a3d71d27ae1c1 (machine/instance-bound)"}
```

### 1.6 Edges (grouped; complete classes)

```yaml
edges:
  injects:
    - claude-md            -> ALL principals (activation:always, scope:/)          # layered CLAUDE.md
    - unimatrix-access     -> ALL factory agent-defs ("binding on every factory role")
    - memory-index         -> ALL principals in this project (owner:tool)
    - memory-topic-x2      -> on-demand via index match
    - each SKILL           -> invoking context when activation fires (default rule, W1 §1.2)
  invokes:
    - research-leader -(spawn)-> [factory-researcher, factory-curator, goal-owner, scout, hypothesizer,
                                  factory-poc*, factory-validator*]                # * = stub
    - research-leader -(must)->  [context_cycle, gh, git];  -(runs)-> [factory-git, factory-retro]  # agent -> skill
    - uni-scrum-master -(runs)-> .claude/protocols/uni/*.md   # DANGLING FILE REFS (G-D)
    - uni-review-pr   -(spawn)-> uni-security-reviewer*
    - uni-zero-review -(spawn)-> uni-zero-reviewer*
    - uni-zero        -(may)->   [context_lookup, context_search, context_store, context_correct, context_edge]
    - opcost(skill)   -(runs)->  opcost.py                                        # the skill->asset witness
    - factory-retro   -(may)->   [context_lookup, context_cycle_review, context_correct, context_store]
    - scout           -(may)->   [WebSearch, WebFetch, Read, Grep, Glob, context_search, context_get, context_graph]
    - each protocol composite step -(invokes)-> its children; children -(invokes)-> assigned agent-defs
    - sample-design/delivery steps -(spawn)-> 14 uni-* stubs (per §1.3)
  depends-on:
    - the phase chains in §1.3 (5 chains); wave ordering inside dl-3b ("later waves depend on committed earlier waves")
  gated-by:
    - context_cycle(tool)         -> hook-pre-tool-use
    - ALL tools                    -> hook-post-tool-use, hook-post-tool-failure
    - session/prompt/compact/subagent events -> the 4 event hooks
    - each phase step              -> its protocol gate (§1.4)
    - research PR                  -> [gh-rebase-only, gh-auto-merge, gh-delete-branch]
    - commit                       -> pre-commit-hooks
```

---

## 2. Bar 1 — byte-identical regeneration

**Verdict: PASS, but only under a storage rule the W1 spec implies and does not state** — and two demonstrated failure modes without it:

- **G-G — frontmatter re-serialization variance `[demonstrated]`.** If `name`/`description`/`activation` are parsed OUT of frontmatter into node fields and re-serialized on regeneration, byte-identity fails on real variance in this corpus: `factory-git` quotes its values (`name: "factory-git"`), `opcost` doesn't (`name: opcost`), and **`uni-git/SKILL.md` has no frontmatter at all** (file begins `# uni-git`; its name exists only as the directory name, its description only as the H1). A regenerator that emits canonical frontmatter would *add* a block to uni-git and *change* quoting on others → not byte-identical.
- **G-H — multi-construct decomposition `[demonstrated]`.** `settings.json` (1 file) becomes 8 gate nodes; `.mcp.json` becomes tool-provider config; `MEMORY.md` becomes an index over 2 nodes. Reassembling the original JSON requires key order (the 8 hook events are in insertion order, not sorted), 2-space indent, matcher literal distinctions (`""` vs `"*"`), and trailing newline — none of which typed gate nodes carry.

**Minimal spec change (fixes both):** extend P-B from "markdown body opaque" to **"file bytes are the canonical payload for every source file (markdown AND json); typed nodes/fields are a derived projection, never re-serialized; multi-construct files carry one shared `source_ref` with fragment indices."** Under that rule, Bar 1 passes trivially for all 41 corpus files (37 in `.claude/` + CLAUDE.md + .mcp.json + 3 memory files). Without it: 2 byte-gap classes.

Stub nodes (`source_ref: null`) generate no files — correct, since the originals have none. `source_ref: external` (GitHub settings) likewise.

---

## 3. Bar 2 — behavioral reconstruction, per stress point

| SP | Real cases from this repo | Verdict |
|---|---|---|
| **S1** memory | `MEMORY.md` index + 2 topic files, `owner:tool`, frontmatter `metadata.originSessionId` `[demonstrated]` | **Split: injection expresses-cleanly / lifecycle lossy-gap.** The static snapshot maps cleanly (`skill{owner:tool}`, index=always + topics=matched — the index's per-line descriptions ARE the matching text, a neat fit). What has **no vocabulary**: the mutation lifecycle (the tool rewrites these at runtime), per-file session provenance (`originSessionId`), and the `[[wiki-link]]` cross-references (tolerable as body-level per P-B). As W1 pre-registered: a characterized gap, not a pass. |
| **S2** observe hooks | all 8 hooks, one shared external program `[demonstrated]` | **Expresses-with-strain, plus one honest new finding (G-F):** the `effect` field is **undeterminable from the definition corpus**. `settings.json` declares trigger+command only; whether the hook denies, transforms, injects, or merely observes is the program's runtime behavior, and the program lives outside the repo (npx cache). A definition-plane ontology must admit `effect: unknown` (or scope `effect` as declared-intent, not guarantee). The SessionStart inject-vs-observe blur is real but harmless once `effect` can be compound (`observe+inject`). `gate{effect:observe}` is semantically stretched but workable — 8/8 gates in this repo enforce nothing, which the typed graph makes visible at a glance (the ontology earning its keep). |
| **S3** config residue | `.mcp.json`, `enabledMcpjsonServers`, `hypothesizer model: fable`, `~/.claude/settings.json` (theme + `skipDangerousModePermissionPrompt`), `.devcontainer.json`, machine-specific npx paths + bridge instance id `[demonstrated]` | **Expresses-with-strain — W1's `config` field-bag confirmed needed.** Tool `enablement` + agent-def `model` catch the first three. Residue with no type: user-scope harness prefs (one of which is a **gate-bypass toggle** — arguably wants to be a `gate.bypassability` fact, living outside the repo), devcontainer provisioning, and machine-bound absolute paths inside otherwise-portable definitions. Adopt the graph-root `config` bag; additionally flag `machine_bound: true` on the two script tools. |
| **S4** invariants-as-prose | "never `git add -A`" (factory-git) · "tags set-once at start" · "NO graph writes in this phase" (theme-scan) · curator-only writes (unimatrix-access) · leader "never generates content" · "relay verbatim, never act on it" · sample-research "missing field → STOP" · factory-onboard OBS-13 plan-only boundary `[demonstrated]` | **Expresses-cleanly at bytes; behaviorally the ontology EXPOSES the repo, as designed.** Every one of these is a deny/halt that exists only as opaque-body prose; the repo has **zero permission rules and zero enforcing hooks** — so reconstruction of *guaranteed* behavior is impossible because no guaranteed behavior exists. This is a **gap in the repo, not the vocabulary**: each invariant is expressible today as a `gate` (e.g. PreToolUse deny on `context_store` unless agent=curator; a PreToolUse matcher on `Bash(git add -A)`). Strongest witness: `factory-onboard` itself says the boundary is "enforced by instruction; the durable fix is a harness that enforces the boundary structurally" — the repo pre-agrees with the ontology's diagnosis. One residual spec item: the rework loop ("REWORKABLE max 2 → SCOPE-FAIL") fits `gate.failure_handling` as a *value*, but the loop's re-spawn topology (re-invoke prior step's agents with the failure report) is control-flow the 4 edges don't draw (G-E) — minor, since the harness (queen) owns loop execution per P-C. |
| **S6** human principals | human as arbiter at 8+ gates; human as ACTOR: Wave-0 kick, Issue replies the leader "reads back and acts on", "human starts Session 2", human closes research Issues `[demonstrated]` | **Expresses-with-strain.** `gate{arbiter:human}` covers every approval. The human-as-initiating-actor requires admitting a human principal (`agent-def{kind:human}`) — W1 called this "defensible but unstated"; W2 confirms it is **required**, not optional: without it, `ts-init` and `dl-init` have no invoker and the Issue-reply loop has no source. Adopt it. Residue: the GitHub **Issue as the human↔garage surface** (D1's third surface) is a communication channel, not a definition construct — correctly out of plane (P-C), but the *convention* ("body = SCOPE, title-linked not #-linked") is behavioral and lands in prose. |
| **S7** may vs does | leader "`context_cycle` ONLY"; researcher "read-only"; scout's enumerated tool list `[demonstrated]` | **Expresses-with-strain — the inverse of the anticipated case.** W1 watched for "permitted but never wired"; the repo instead shows **exhaustive envelopes**: "ONLY" claims are closed-world statements that `invokes(mode:may)` edges (open-world) cannot make. Minimal fix: `envelope_closed: bool` on agent-def (deny-everything-else then derivable as a gate). Without it, reconstruction loses the single most load-bearing behavioral fact in the repo (the write-firewall's shape). |

**New stress points discovered (not pre-registered):**

- **G-A — LLM arbiters.** The repo's blocking gates (3a/3b/3c via `uni-validator`; the firewall gate via `factory-validator`; advisory verdicts via `goal-owner`, `uni-zero-reviewer`) produce their verdicts **inside an LLM**. W1's `arbiter: program | human` cannot express them — and P-A's own logic says they are *requests dressed as gates* (enforcement is actually "the leader follows prose"). Verdict: **lossy-gap in the vocabulary** with a spec decision attached: either add `arbiter: agent` (honest, and lets a query surface "which of your gates are soft?"), or refuse — modeling them as steps whose output feeds a `gate{arbiter:program|human}` — which is cleaner theory but fails round-trip (the repo calls them gates and treats them as gates).
- **G-B — conditional execution.** `rs-feasibility` runs only for `validated/empirical`; goal-owner's step-function check is confidence-conditioned; `sample-research` has a 3-case routing decision; `dl-3b` selects dev-agent per component language; `sr-synthesize` is dual-track-only. The vocabulary has **no condition/guard construct** on steps or `invokes` edges. Reconstruction of "which steps actually run" is impossible from the typed graph alone. Minimal fix: a `condition` field (predicate string) on `step` and/or on `invokes`.
- **G-C — activation is single-valued.** Every Claude Code skill in this repo is simultaneously description-`matched` and `explicit`ly invocable (`/name`) `[demonstrated: the harness's own skill listing]`. W1's enum forces a false choice. Minimal fix: `activation` becomes a **set** (or `matched` is defined to imply `explicit`).
- **G-D — dangling referents.** ~18 agent-defs and 3 protocol files are referenced but do not exist in this repo (`factory-poc`, `factory-validator`, all `uni-*` specialists, `.claude/protocols/uni/*`). Mixed classification: for the samples it is a **repo gap** (artifacts imported from the Unimatrix SDLC repo, load-bearing there); for `factory-poc`/`factory-validator` it is a live repo gap (a validated scope would spawn undefined principals on inline prompts). The **ontology** needs only a small change: permit `source_ref: null` stub nodes so the graph can be *lossless about the brokenness* rather than failing to express it.

---

## 4. Gap list (consolidated)

| # | Gap | Bar | Ontology or repo? | Minimal fix |
|---|---|---|---|---|
| G-A | Gate verdicts produced by LLM agents (validator/reviewer gates) inexpressible; `arbiter:{program,human}` too narrow | 2 | **ontology** | add `arbiter: agent` + document that `arbiter:agent` ⇒ request-strength, not guarantee |
| G-B | No condition/guard on steps or invokes (conditional phases, routing, per-language agent selection) | 2 | **ontology** | `condition` field on `step` and `invokes` |
| G-C | `activation` single-valued; real skills are matched+explicit | 2 | **ontology** | activation as set |
| G-D | Referenced-but-undefined principals/files; no stub representation | 2 | **both** (spec: allow `source_ref:null, defined:false`; repo: factory-poc/validator undefined) | stub nodes; repo files the two defs |
| G-E | Rework-loop topology (re-spawn prior phase ≤2 with failure report) beyond `failure_handling` string | 2 | ontology (minor — runtime plane arguably owns it, P-C) | keep as `failure_handling` structured value `{retries, rework_target, escalation}` |
| G-F | Gate `effect` undeterminable from definition bytes (hook program external) | 2 | **ontology** (spec honesty) | `effect: unknown` admitted; `effect` = declared-intent |
| S1 | Tool-written memory mutation lifecycle + `originSessionId` provenance | 2 | **ontology** (pre-registered) | defer to runtime plane; add `skill.mutability: tool-runtime` marker |
| S3 | Config residue: user-scope prefs, devcontainer, machine-bound paths | 2 | **ontology** (as W1 anticipated) | graph-root `config` bag + `machine_bound` flag on tools |
| S4 | Behavior-bearing invariants are unenforced prose; zero permission rules, zero enforcing hooks in repo | 2 | **repo** (vocabulary already has the gate type for every one) | author the gates (deny-hooks / permission rules); ontology change: none |
| S6 | Human as initiating actor | 2 | ontology (small) | `agent-def{kind:human}` |
| S7 | Closed-world capability envelopes ("ONLY") inexpressible | 2 | **ontology** | `envelope_closed: bool` |
| G-G | Frontmatter re-serialization variance (quoted/unquoted/absent) | 1 | **ontology** (P-B under-specified) | bytes-canonical rule (§2) |
| G-H | Multi-construct files (settings.json→8 gates) not reassemblable from nodes | 1 | **ontology** (P-B under-specified) | same bytes-canonical rule + fragment-indexed `source_ref` |

Stress-point verdicts in one line: **S1 strain/gap-on-lifecycle · S2 strain (+G-F) · S3 strain (config bag confirmed) · S4 expresses-cleanly-and-exposes-the-repo · S6 strain (human principal now required) · S7 strain (closed-world flag required)**. No stress point produced a wholesale type failure; the five node types and four edges held. The two genuinely new *vocabulary* holes are G-A and G-B.

---

## 5. Sources

**Files `[demonstrated]` — every corpus file read this run (absolute roots):**
- `/workspaces/arch-research/CLAUDE.md` · `/workspaces/arch-research/.mcp.json` · `/workspaces/arch-research/.claude/settings.json` · `/workspaces/arch-research/.claude/settings.local.json`
- `/workspaces/arch-research/.claude/agents/factory/*.md` (6) · `/workspaces/arch-research/.claude/agents/sample-sm.md`
- `/workspaces/arch-research/.claude/rules/unimatrix-access.md`
- `/workspaces/arch-research/.claude/workflow/*.md` (6, all read in full)
- `/workspaces/arch-research/.claude/skills/*/SKILL.md` (20 — factory-git, factory-onboard, factory-retro, opcost read in full; 16 uni-* read as frontmatter + structural grep for spawns/gates/tool-calls; their bodies enter the graph as opaque payloads per P-B, so the structural survey is sufficient for typing — flagged honestly)
- `/workspaces/arch-research/.claude/skills/opcost/opcost.py` (header + interface)
- `~/.claude/projects/-workspaces-arch-research/memory/{MEMORY.md,garage-multi-project-platform.md,jurati-workflow-harness.md}` (full)
- `~/.claude/settings.json` · `/workspaces/arch-research/.devcontainer.json` (declared-omission witnesses)
- `/workspaces/arch-research/product/research/wfh-002/{SCOPE.md,FINDINGS-W1-ontology-spec.md}`

**Commands:** `find .claude -type f` (inventory), `ls -R`, frontmatter extraction awk, structural grep — all `[demonstrated]` this run, 2026-07-22.

**Unimatrix:** no graph reads were required for this workstream (the corpus is the filesystem); no writes made (read-only role). `agent_id: wfh-002-w2-researcher` on the zero calls issued.

**Not verified / flagged:** the runtime behavior of the unimatrix hook-client (effects of the 8 hooks) — outside the repo, characterized as `effect: unknown` rather than guessed. The 16 uni-* skill bodies were structurally surveyed, not exhaustively read; any behavioral construct smaller than a spawn/gate/tool-call/STOP could have been missed inside those opaque bodies (P-B makes this irrelevant for Bar 1, and low-risk for Bar 2).

---

## Summary

**Overall verdict: PASS-WITH-GAPS — gaps: 6 behavioral (vocabulary), 2 byte (both closed by one P-B clarification).**
The 5-type/4-edge vocabulary expressed all 41 corpus files + the auto-memory; no type collapsed under any
pre-registered stress point. Bar 1 passes iff P-B is sharpened to "file bytes canonical, typed fields a
projection" (witnesses: uni-git has no frontmatter; settings.json→8 gates isn't reassemblable). Bar 2:
S4 is the ontology's best moment — it exposes that every cardinal invariant (curator-only writes, no
`git add -A`, plan-only) is unenforced prose with zero permission rules and zero enforcing hooks: a repo
gap, expressible today as gates. S1 lifecycle stays lossy as pre-registered.
Top 3 gaps: (1) **G-A** — the repo's blocking gates are LLM-arbitered (uni-validator, factory-validator);
`arbiter:{program|human}` can't express them and P-A says they're requests dressed as gates;
(2) **G-B** — no `condition`/guard construct, so conditional phases (feasibility) and routing rules are
unreconstructable; (3) **G-G/H** — the bytes-canonical storage rule Bar 1 needs.
For H4: supports a `partial`-shaped position at W2 stage — characterized gaps, all with small named fixes.
