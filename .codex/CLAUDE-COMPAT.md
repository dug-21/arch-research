# Claude-to-Codex execution adapter

This file translates platform mechanics only. Research policy and workflow remain canonical in
`CLAUDE.md` and `.claude/`.

## Execution vocabulary

| Claude protocol term | Codex operation |
|---|---|
| `Task(...)` or `Agent(...)` | Spawn a Codex subagent with the named role file's full path, run/agent ID, task boundary, and artifact paths. |
| Multiple task calls "in one message" | Spawn the independent Codex subagents concurrently, then wait for all required returns before advancing the gate. |
| `subagent_type: NAME` | Read `.claude/agents/factory/NAME.md` (or the role path named by the active protocol) and use it as the subagent's role contract. |
| `Read`, `Grep`, `Glob` | Use Codex filesystem tools; prefer `rg`/`rg --files` for search. |
| `WebSearch`, `WebFetch` | Use Codex web search/open tools and retain source URLs in the required citation schema. |
| `/skill-name` | Invoke the corresponding discovered Codex skill, whose canonical `SKILL.md` remains under `.claude/skills/`. |
| `/mcp` reconnect | Diagnose/restart the Codex Unimatrix MCP connection, then retry the rejected call; never silently omit a cycle event. |

## Role loading

Codex does not infer a runnable named agent from Claude frontmatter. Before spawning a factory role,
the coordinator must read its complete file under `.claude/agents/factory/` and identify it in the
spawn prompt. Frontmatter such as `model: fable` is advisory unless an explicit Codex model mapping is
configured; the role boundaries and output contract remain binding.

## Tool names

Treat `context_*` and `mcp__unimatrix__context_*` as equivalent references to the tools exposed by the
configured `unimatrix` MCP server. Use the actual tool name available in the current Codex session.

## Non-portable material

- Ignore `.claude/agents/sample-sm.md` and `.claude/workflow/sample-*.md`.
- `opcost` is Claude-transcript-specific and is intentionally not exposed as a Codex skill.
- Claude hook configuration in `.claude/settings.json` is not itself loaded by Codex. Codex MCP is
  configured separately in `.codex/config.toml`; lifecycle-hook parity must use Codex-native hooks.
