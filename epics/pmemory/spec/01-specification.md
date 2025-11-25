# pMemory SPARC Specification

## Phase 1: Specification (Revised)

**Document Status**: Revised for Integration Approach
**Version**: 2.0.0
**Last Updated**: November 2024

---

## 1. Product Vision

### 1.1 Problem Statement

The capabilities for a secure, intelligent, LLM-agnostic memory layer exist but are fragmented:

- **AgentDB**: 29 MCP tools for memory, but no integrated security
- **aidefence**: Threat detection, but not wired into memory operations
- **agentic-flow**: LLM routing, but not coordinated with memory
- **ruvector**: Massive scale, but separate deployment

**No unified system exists that secures agent memory by default while enabling LLM-agnostic operation.**

### 1.2 Solution Overview

**pMemory** is an MCP server that integrates existing tools into a unified, secure Active Memory Layer:

```
┌─────────────────────────────────────────────────────────────┐
│                   pMemory MCP Server                        │
│            (Integration Layer - ~2,200 LOC)                 │
├─────────────────────────────────────────────────────────────┤
│  Input: MCP requests (pmemory_*)                           │
│  Output: Secured, routed responses                          │
│                                                             │
│  Integrates:                                                │
│  • AgentDB (29 existing MCP tools)                         │
│  • aidefence (security scanning)                           │
│  • agentic-flow (LLM routing)                              │
│  • ruvector (optional scale tier)                          │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Success Criteria

| Criterion | Target | Validation |
|-----------|--------|------------|
| MCP tools exposed | 15 unified tools | Tool listing |
| Security coverage | 100% operations scanned | Integration test |
| LLM providers | 3+ routable | Provider test |
| Installation | Single `npx` command | Manual test |
| Timeline | 3 weeks | Delivery date |

---

## 2. Functional Requirements

### 2.1 MCP Interface

#### FR-001: MCP Server Implementation
**Priority**: P0 (Critical)

The system MUST:
- Implement MCP protocol (stdio transport)
- Register `pmemory_*` tool namespace
- Handle concurrent requests
- Support MCP resources for configuration

**Acceptance Criteria**:
- [ ] Server starts via `npx pmemory mcp start`
- [ ] Tools visible in Claude Code
- [ ] Concurrent requests handled correctly

#### FR-002: Core Memory Tools (Delegates to AgentDB)
**Priority**: P0 (Critical)

| Tool | Delegates To | Security |
|------|-------------|----------|
| `pmemory_init` | `agentdb_init` | Config validation |
| `pmemory_store` | `agentdb_insert` | aidefence scan |
| `pmemory_store_batch` | `agentdb_insert_batch` | aidefence batch scan |
| `pmemory_search` | `agentdb_search` | Query validation |
| `pmemory_delete` | `agentdb_delete` | Auth check |

**Acceptance Criteria**:
- [ ] All 5 tools delegate correctly to AgentDB
- [ ] Security applied before delegation
- [ ] Errors propagate with context

#### FR-003: Intelligence Tools (Delegates to AgentDB Frontier)
**Priority**: P1 (High)

| Tool | Delegates To | Purpose |
|------|-------------|---------|
| `pmemory_causal_link` | `causal_add_edge` | Create cause-effect relationship |
| `pmemory_causal_query` | `causal_query` | Query causal graph |
| `pmemory_reflect` | `reflexion_store` | Store success/failure episode |
| `pmemory_recall` | `reflexion_retrieve` | Retrieve past episodes |

**Acceptance Criteria**:
- [ ] Causal graphs build correctly over time
- [ ] Reflexion episodes persist across sessions
- [ ] Recall returns relevant episodes

#### FR-004: Learning Tools (Delegates to AgentDB + ReasoningBank)
**Priority**: P1 (High)

| Tool | Delegates To | Purpose |
|------|-------------|---------|
| `pmemory_skill_store` | `skill_create` | Store reusable skill |
| `pmemory_skill_find` | `skill_search` | Find relevant skills |
| `pmemory_learn` | `learner_discover` | Trigger pattern discovery |

**Acceptance Criteria**:
- [ ] Skills persist and are searchable
- [ ] Learning discovers useful patterns
- [ ] ReasoningBank integration functional

#### FR-005: Security Tools (Delegates to aidefence)
**Priority**: P0 (Critical)

| Tool | Purpose |
|------|---------|
| `pmemory_scan` | Explicit threat scan |
| `pmemory_audit` | Query audit log |

**Acceptance Criteria**:
- [ ] Scan detects known threat patterns
- [ ] Audit log captures all operations

#### FR-006: Provider Tools (Delegates to agentic-flow)
**Priority**: P1 (High)

| Tool | Purpose |
|------|---------|
| `pmemory_embed` | Generate embedding via routed LLM |
| `pmemory_provider_set` | Set preferred provider |
| `pmemory_provider_list` | List available providers |

**Acceptance Criteria**:
- [ ] Embedding routes to configured provider
- [ ] Provider switching works without data loss
- [ ] Fallback chain activates on failure

### 2.2 Security Integration

#### FR-007: Default Security Scanning
**Priority**: P0 (Critical)

The system MUST:
- Scan ALL store operations via aidefence before storage
- Validate ALL search queries for injection attempts
- Log ALL operations to audit trail
- Filter PII when configured

**Security Flow**:
```
Request → aidefence.scan() → if safe → delegate → respond
                           → if threat → reject with reason
```

**Acceptance Criteria**:
- [ ] Known injection patterns blocked
- [ ] PII filtered from stored content
- [ ] Audit log complete and queryable

#### FR-008: Configurable Security Levels
**Priority**: P2 (Medium)

| Level | Behavior |
|-------|----------|
| `strict` | Block any threat score >0.5 |
| `balanced` | Block threats >0.7, warn >0.5 |
| `permissive` | Block only high-confidence (>0.9) |
| `off` | No scanning (not recommended) |

**Acceptance Criteria**:
- [ ] Security level configurable via YAML
- [ ] Behavior matches documented levels

### 2.3 LLM Routing Integration

#### FR-009: Intelligent Embedding Routing
**Priority**: P1 (High)

The system MUST:
- Route embedding requests via agentic-flow
- Select provider based on cost/latency/privacy
- Cache embeddings to reduce LLM calls
- Support fallback chains

**Acceptance Criteria**:
- [ ] Embedding requests route to configured provider
- [ ] Cost savings measurable vs direct API
- [ ] Fallback activates when primary fails

#### FR-010: Provider Configuration
**Priority**: P1 (High)

```yaml
# pmemory.yaml
llm:
  default_provider: claude
  fallback_chain:
    - claude
    - openai
    - ollama
  embedding_model: text-embedding-3-small
  routing_strategy: cost  # cost | latency | privacy
```

**Acceptance Criteria**:
- [ ] Configuration loaded from YAML
- [ ] Runtime provider switching via tool
- [ ] Environment variable overrides work

### 2.4 Configuration

#### FR-011: Configuration File
**Priority**: P1 (High)

```yaml
# pmemory.yaml (complete example)

# Memory backend
memory:
  backend: agentdb          # agentdb | ruvector
  namespace: default
  data_path: ~/.pmemory

# Security settings
security:
  enabled: true
  level: balanced           # strict | balanced | permissive | off
  pii_filter: true
  audit_retention_days: 30

# LLM routing
llm:
  router: agentic-flow
  default_provider: claude
  fallback_chain:
    - claude
    - openai
    - gemini
    - ollama
  routing_strategy: cost

# Learning features
learning:
  reflexion: true
  causal_tracking: true
  skill_library: true
  reasoningbank: true
```

**Acceptance Criteria**:
- [ ] Config file parsed correctly
- [ ] Defaults applied for missing values
- [ ] Validation errors reported clearly

---

## 3. Non-Functional Requirements

### 3.1 Performance

| Operation | Target | Source |
|-----------|--------|--------|
| Store (with security) | <100ms | aidefence <10ms + AgentDB <50ms |
| Search | <50ms | AgentDB p95 |
| Embedding | <500ms | LLM provider dependent |
| Causal query | <20ms | AgentDB |

**Note**: Performance depends on underlying tools, not our code.

### 3.2 Reliability

| Requirement | Target |
|-------------|--------|
| Error handling | All errors include context |
| Fallback | LLM fallback chain activates |
| Graceful degradation | Works without security (if configured) |

### 3.3 Compatibility

| Requirement | Target |
|-------------|--------|
| Node.js | >=18.0.0 |
| MCP SDK | Latest |
| AgentDB | ^1.6.0 |
| aidefence | ^2.1.0 |
| agentic-flow | Latest |

---

## 4. MCP Tool Specifications

### 4.1 Tool Schema

#### pmemory_init

```json
{
  "name": "pmemory_init",
  "description": "Initialize pMemory with configuration",
  "inputSchema": {
    "type": "object",
    "properties": {
      "namespace": {
        "type": "string",
        "description": "Memory namespace",
        "default": "default"
      },
      "config_path": {
        "type": "string",
        "description": "Path to pmemory.yaml"
      }
    }
  }
}
```

#### pmemory_store

```json
{
  "name": "pmemory_store",
  "description": "Store content in memory (security scanned)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "content": {
        "type": "string",
        "description": "Content to store"
      },
      "metadata": {
        "type": "object",
        "description": "Optional metadata"
      },
      "causal_sources": {
        "type": "array",
        "items": { "type": "string" },
        "description": "IDs of items that led to this"
      }
    },
    "required": ["content"]
  }
}
```

#### pmemory_search

```json
{
  "name": "pmemory_search",
  "description": "Search memory semantically",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query"
      },
      "top_k": {
        "type": "number",
        "description": "Number of results",
        "default": 10
      },
      "include_causal": {
        "type": "boolean",
        "description": "Include causal context",
        "default": false
      }
    },
    "required": ["query"]
  }
}
```

#### pmemory_embed

```json
{
  "name": "pmemory_embed",
  "description": "Generate embedding via routed LLM",
  "inputSchema": {
    "type": "object",
    "properties": {
      "text": {
        "type": "string",
        "description": "Text to embed"
      },
      "provider": {
        "type": "string",
        "description": "Override default provider"
      }
    },
    "required": ["text"]
  }
}
```

#### pmemory_reflect

```json
{
  "name": "pmemory_reflect",
  "description": "Store reflection episode for learning",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task": {
        "type": "string",
        "description": "Task description"
      },
      "outcome": {
        "type": "string",
        "enum": ["success", "failure", "partial"],
        "description": "Task outcome"
      },
      "reflection": {
        "type": "string",
        "description": "What was learned"
      },
      "related_memories": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Memory IDs involved"
      }
    },
    "required": ["task", "outcome", "reflection"]
  }
}
```

### 4.2 Complete Tool List

| Tool | Category | Delegates To |
|------|----------|-------------|
| `pmemory_init` | Core | `agentdb_init` |
| `pmemory_store` | Core | `agentdb_insert` |
| `pmemory_store_batch` | Core | `agentdb_insert_batch` |
| `pmemory_search` | Core | `agentdb_search` |
| `pmemory_delete` | Core | `agentdb_delete` |
| `pmemory_causal_link` | Intelligence | `causal_add_edge` |
| `pmemory_causal_query` | Intelligence | `causal_query` |
| `pmemory_reflect` | Intelligence | `reflexion_store` |
| `pmemory_recall` | Intelligence | `reflexion_retrieve` |
| `pmemory_skill_store` | Learning | `skill_create` |
| `pmemory_skill_find` | Learning | `skill_search` |
| `pmemory_learn` | Learning | `learner_discover` |
| `pmemory_scan` | Security | `aidefence.scan` |
| `pmemory_audit` | Security | `aidefence.audit` |
| `pmemory_embed` | Provider | `agentic-flow.embed` |
| `pmemory_provider_set` | Provider | config update |
| `pmemory_provider_list` | Provider | config read |

---

## 5. Integration Architecture

### 5.1 Dependency Graph

```
pMemory MCP Server
    │
    ├── @modelcontextprotocol/sdk  (MCP protocol)
    │
    ├── agentdb                     (Memory engine)
    │   ├── Vector storage
    │   ├── Causal graphs
    │   ├── Reflexion memory
    │   └── Skill library
    │
    ├── aidefence                   (Security)
    │   ├── Threat detection
    │   ├── PII filtering
    │   └── Audit logging
    │
    └── agentic-flow                (LLM routing)
        ├── Multi-provider router
        └── ReasoningBank
```

### 5.2 Request Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                       MCP Request Flow                           │
│                                                                  │
│  Claude/Agent                                                    │
│      │                                                           │
│      │ MCP: pmemory_store({ content: "..." })                   │
│      ▼                                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   pMemory Server                          │   │
│  │                                                           │   │
│  │  1. Parse MCP request                                     │   │
│  │  2. Validate input schema                                 │   │
│  │  3. aidefence.scan(content)  ────────────────────────┐   │   │
│  │                                                       │   │   │
│  │     ┌─────────────────────────────────────────────────┤   │   │
│  │     │ If threat detected:                             │   │   │
│  │     │   Return error with threat details              │   │   │
│  │     └─────────────────────────────────────────────────┤   │   │
│  │                                                       │   │   │
│  │  4. agentic-flow.embed(content)  ◄────────────────────┘   │   │
│  │                                                           │   │
│  │  5. agentdb.insert({ content, embedding, metadata })     │   │
│  │                                                           │   │
│  │  6. If causal_sources provided:                          │   │
│  │       agentdb.causal_add_edge(source, new_id)            │   │
│  │                                                           │   │
│  │  7. aidefence.log(operation)  (audit trail)              │   │
│  │                                                           │   │
│  │  8. Return MCP response { id, success }                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│      │                                                           │
│      ▼                                                           │
│  Claude/Agent receives response                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Installation & Usage

### 6.1 Installation

```bash
# Global install
npm install -g pmemory

# Or run directly
npx pmemory mcp start
```

### 6.2 Claude Code Integration

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "pmemory": {
      "command": "npx",
      "args": ["pmemory", "mcp", "start"],
      "env": {
        "PMEMORY_CONFIG": "~/.pmemory/config.yaml"
      }
    }
  }
}
```

### 6.3 CLI Commands

```bash
# Start MCP server
pmemory mcp start

# Initialize configuration
pmemory init

# Set provider
pmemory config set llm.default_provider openai

# View stats
pmemory stats

# Export data
pmemory export ./backup.json
```

---

## 7. Testing Strategy

### 7.1 Integration Tests

| Test | Validates |
|------|-----------|
| `test_store_with_security` | aidefence scans before storage |
| `test_store_blocks_injection` | Known injection patterns rejected |
| `test_search_routes_correctly` | Query reaches AgentDB |
| `test_embed_routes_to_provider` | agentic-flow routing works |
| `test_fallback_activates` | Fallback chain on provider failure |
| `test_causal_links_persist` | Causal graph builds correctly |
| `test_reflexion_persists` | Episodes survive restart |

### 7.2 E2E Demo Test

```typescript
// Demo: Agent research task
async function testAgentResearch() {
  // 1. Initialize
  await pmemory.init({ namespace: "research" });

  // 2. Store some knowledge
  const id1 = await pmemory.store({
    content: "Quantum computing threatens RSA encryption",
    metadata: { source: "research-paper" }
  });

  // 3. Search for related content
  const results = await pmemory.search({
    query: "encryption vulnerabilities",
    top_k: 5
  });

  // 4. Store derived insight with causal link
  const id2 = await pmemory.store({
    content: "Post-quantum cryptography adoption is urgent",
    causal_sources: [id1]
  });

  // 5. Reflect on success
  await pmemory.reflect({
    task: "Research quantum crypto impact",
    outcome: "success",
    reflection: "Causal linking helped connect ideas"
  });

  // Assertions
  expect(results.length).toBeGreaterThan(0);
  expect(await pmemory.causalQuery({ target: id2 })).toContain(id1);
}
```

---

## 8. Document References

- **Thesis**: `00-thesis.md` - Integration approach
- **Architecture**: `arch/03-architecture.md` - System design
- **Implementation**: `implementation/05-implementation.md` - Timeline

---

## Appendix: Underlying Tool References

- [AgentDB MCP Tools](https://agentdb.ruv.io) - 29 tools, v1.6.0
- [aidefence](https://www.npmjs.com/package/aidefence) - Security, v2.1.1
- [agentic-flow](https://github.com/ruvnet/agentic-flow) - LLM routing
- [ruvector](https://github.com/ruvnet/ruvector) - Scale tier
