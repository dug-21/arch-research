# Codex repository instructions

`CLAUDE.md` and the non-sample material under `.claude/` are the canonical instructions for this
repository. Read `CLAUDE.md` before doing substantive work and follow it as repository policy.

For research-garage work, load the applicable source files directly:

- Protocols: `.claude/workflow/{decompose-scope,research-scope,theme-scan}.md`
- Roles: `.claude/agents/factory/*.md`
- Unimatrix rules: `.claude/rules/unimatrix-access.md`
- Reusable procedures: `.claude/skills/*/SKILL.md`

Do not use `.claude/agents/sample-sm.md` or `.claude/workflow/sample-*.md`; they are examples and are
not part of the active garage protocol.

Use `.codex/CLAUDE-COMPAT.md` only to translate Claude-specific execution vocabulary into Codex
operations. It is an adapter, not a second source of protocol truth. If the adapter and `.claude`
disagree about research method, `.claude` wins.

When a garage protocol assigns independent roles or parallel workstreams, use Codex subagents and
give each subagent the applicable canonical role file and artifact paths. Preserve every role boundary,
especially the research-leader/worker split and the curator-only Unimatrix write rule.
