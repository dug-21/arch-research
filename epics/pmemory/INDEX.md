# pMemory: Active Memory Layer

## Integration-First Design

**Version**: 2.0.0
**Approach**: Integrate existing tools, don't reinvent

---

## Overview

**pMemory** is an MCP server that integrates existing tools into a unified, secure Active Memory Layer:

```
┌────────────────────────────────────────────────────────────────┐
│                    pMemory MCP Server                          │
│         (Thin orchestration layer - ~2,200 LOC)                │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  aidefence   │  │ agentic-flow │  │      AgentDB         │ │
│  │  Security    │  │  LLM Router  │  │   Memory Engine      │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

---

## Documents

| Document | Purpose |
|----------|---------|
| [00-thesis.md](./00-thesis.md) | Strategic thesis: why integration beats invention |
| [spec/01-specification.md](./spec/01-specification.md) | MCP tool specifications and requirements |
| [arch/03-architecture.md](./arch/03-architecture.md) | System architecture and data flows |
| [implementation/05-implementation.md](./implementation/05-implementation.md) | 3-week implementation plan |

---

## Key Principles

### What We're Building (~2,200 LOC)

- MCP server that unifies existing tools
- Security-first orchestration (all ops pass through aidefence)
- Configuration management (YAML-based)
- 17 MCP tools exposing unified `pmemory_*` namespace

### What We're NOT Building

- ❌ A new vector database (AgentDB exists)
- ❌ A new LLM router (agentic-flow exists)
- ❌ A new security system (aidefence exists)
- ❌ Custom algorithms (underlying tools have them)

---

## MCP Tools

| Tool | Category | Delegates To |
|------|----------|--------------|
| `pmemory_init` | Core | AgentDB |
| `pmemory_store` | Core | aidefence → AgentDB |
| `pmemory_search` | Core | aidefence → AgentDB |
| `pmemory_delete` | Core | AgentDB |
| `pmemory_causal_link` | Intelligence | AgentDB |
| `pmemory_causal_query` | Intelligence | AgentDB |
| `pmemory_reflect` | Intelligence | AgentDB |
| `pmemory_recall` | Intelligence | AgentDB |
| `pmemory_skill_store` | Learning | AgentDB |
| `pmemory_skill_find` | Learning | AgentDB |
| `pmemory_learn` | Learning | AgentDB |
| `pmemory_scan` | Security | aidefence |
| `pmemory_audit` | Security | aidefence |
| `pmemory_embed` | Provider | agentic-flow |
| `pmemory_provider_set` | Provider | Config |
| `pmemory_provider_list` | Provider | Config |

---

## Integrated Tools

| Tool | Capabilities | npm |
|------|--------------|-----|
| **AgentDB** | 29 MCP tools: vector store, causal graphs, reflexion, skills, HNSW (150x faster) | `agentdb ^1.6.0` |
| **aidefence** | Threat detection (<10ms), PII filtering, formal verification, 98.3% coverage | `aidefence ^2.1.0` |
| **agentic-flow** | 100+ LLM providers, 85-99% cost savings, fallback chains, ReasoningBank | `agentic-flow` |
| **ruvector** | <0.5ms p50, 500M+ concurrent, scale tier (optional) | `ruvector` |

---

## Timeline

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Scaffold + Core | MCP server with basic CRUD |
| 2 | Integration | aidefence + agentic-flow wired |
| 3 | Testing + Polish | Published npm package |

**Total**: 3 weeks to production

---

## Usage

```bash
# Install
npm install -g pmemory

# Or run directly
npx pmemory mcp start

# Configure in Claude Desktop
# ~/.config/claude/claude_desktop_config.json
{
  "mcpServers": {
    "pmemory": {
      "command": "npx",
      "args": ["pmemory", "mcp", "start"]
    }
  }
}
```

---

## Related Analysis

- [PKM Analysis 08-10](../pkm-analysis/) - Memory platform thesis validation
- [AgentDB](https://agentdb.ruv.io) - Memory engine documentation
- [agentic-flow](https://github.com/ruvnet/agentic-flow) - LLM routing
- [aidefence](https://www.npmjs.com/package/aidefence) - Security

---

*The novel contribution is the secure, unified, MCP-native orchestration—not reinventing the underlying capabilities.*
