---
name: "factory-git"
description: "Git conventions for the research factory — two-stream (method vs research), parallel-safe path-scoped commits, semver wf: stamp, auto-merge. Use when committing factory standards or research-run artifacts. Distinct from uni-git (SDLC)."
---

# factory-git — Git Conventions for the Research Factory

The factory's git model is shaped by one constraint `uni-git` doesn't have: **the workflow is a
versioned artifact (methodology §7–8), and every run is stamped `wf:<version>`.** That forces a
two-stream split; the factory's parallelism forces a path-scoped commit discipline. Source: D12.

> This is the FACTORY git skill. `uni-git` is the SDLC variant — do not mix them.

## Two streams — never mixed in one commit

A research commit must never move the `wf:` version (it would break the §8 "proven under which
method?" blast-radius logic). So keep them in separate commits, ideally separate branches:

| Stream | Paths | Branch | Merge |
|---|---|---|---|
| **Method** (the factory itself) | `.claude/**`, `product/factory/**` | `workflow/{desc}` | PR → reviewed → **bumps `wf:`** |
| **Research** (run output) | `product/research/{scope-id}/**` | `research/{scope-id}` | PR `Closes #<issue>` → **auto-merge** after the synthesis gate |

## Parallelism discipline (load-bearing)

The factory runs scopes/agents in parallel. The rule that makes that safe in git:

- **Stage only your own paths — NEVER `git add -A` / `git add .` / `git add -u`.**
  Each scope/agent stages exactly the files it owns: `git add product/research/{scope-id}/`.
- **Always commit your work before yielding** — leave no uncommitted WIP. A later broad commit by
  another unit would sweep it (this exact failure was observed during the bootstrap).
- Scopes live in **disjoint directories**, so parallel branches rebase-merge to main conflict-free.
- A failed commit LEAVES files staged — re-check `git status` before the next commit so you don't
  sweep another unit's staged work. (Set git identity first; an identity failure is a common cause.)

## The `wf:` version stamp (§8)

- `wf:` is a **semver of the METHOD**, bumped when a `workflow/*` PR merges — **NOT a HEAD SHA**
  (research commits also move HEAD; `wf:` must move only when the method changes).
- On each method-PR merge: tag the **method commit** `wf-vX.Y` (annotated), and bump.
- Every run records its `wf:` in `context_cycle` outcomes + the run REPORT, so yield is sliceable by
  method version and a defective method's blast radius is scopable.
- Current baseline: **`wf-v0.1`**.

## Branch naming

| Context | Pattern | Example |
|---|---|---|
| Method / workflow change | `workflow/{desc}` | `workflow/factory-git` |
| Research scope | `research/{scope-id}` | `research/shd-002` |
| Ad-hoc docs | `docs/{short-desc}` | `docs/methodology-fix` |

## Commit format

```
{prefix}: {description} (#{issue})

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

| Prefix | When |
|---|---|
| `method:` | method-stream change (standards, rules, skills, runbook, templates) |
| `decompose:` | a decompose-scope's board artifacts |
| `research:` / `research({scope}):` | a research-scope's findings / FINDINGS |
| `synthesis:` | synthesis artifacts / REPORT |
| `poc({scope}):` | a validated scope's POC code / artifacts |
| `docs:` | standalone docs |

## Merge & PR

- **Rebase-only** (merge commits disabled at repo level). **Auto-merge + delete-branch-on-merge** enabled.
- **Research PR:** `Closes #<scope-issue>`; auto-merges after the synthesis gate (already
  human-reviewed on the Issue, D1). Body = the run summary.
- **Method PR:** reviewable (it ripples to every future run); on merge, tag + bump `wf:`.

## .gitignore essentials

Exclude: secrets (`.env*`), build artifacts, **local model weights (`*.gguf`, `*.safetensors`) and
POC venvs (`.venv/`, `__pycache__/`) — shd-003+**, `target/`, `.claude/worktrees/`,
`.claude/settings.local.json`.

## Worktrees

- **Not needed** for read-only research fan-out (researchers don't mutate shared files).
- Use Claude Code's `isolation: "worktree"` only for **POC scopes** where parallel agents write code
  that would conflict; clean up after the scope's artifacts are committed.

## Rules

- Never force-push `main`. (Force-pushing your own unmerged feature branch, or a `wf-*` tag, is OK.)
- Never `git add -A` — path-scoped only (parallelism).
- Never commit secrets, model weights, or build artifacts.
- Always co-author commits (trailer above); set git identity before committing.
