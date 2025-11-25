# pMemory: Active Memory Layer

## Revised Thesis: Integration, Not Invention

**Document Status**: Revised
**Version**: 2.0.0
**Last Updated**: November 2024

---

## The Insight

The foundational capabilities for an Active Memory Layer **already exist**:

| Capability | Existing Tool | Status |
|------------|---------------|--------|
| High-speed vector memory | **AgentDB** | Production-ready, 29 MCP tools |
| LLM routing & cost optimization | **agentic-flow** | 100+ providers, 85-99% cost savings |
| Scalable vector search | **ruvector** | <0.5ms p50, 500M+ concurrent |
| AI security & threat detection | **aidefence** | Real-time detection, formal verification |

**pMemory is not a new database or framework.** It is an **orchestration layer** that integrates these capabilities into a unified, MCP-native Active Memory Layer.

---

## What We're Building

### The Integration Gap

These tools exist independently. What's missing:

1. **Unified MCP Interface**: Single entry point exposing all memory capabilities
2. **Security-First Orchestration**: aidefence protecting all memory operations
3. **Learning Coordination**: Connecting ReasoningBank patterns across sessions
4. **LLM Agnosticism**: Seamless provider switching via agentic-flow routing

### The Solution

```
┌────────────────────────────────────────────────────────────────┐
│                    pMemory MCP Server                          │
│         (Thin orchestration layer - ~2000 lines of code)       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │   aidefence  │  │  agentic-flow│  │      AgentDB         │ │
│  │   Security   │  │  LLM Router  │  │   Memory Engine      │ │
│  │              │  │              │  │                      │ │
│  │ • Threat det │  │ • 100+ LLMs  │  │ • 29 MCP tools       │ │
│  │ • PII filter │  │ • Cost optim │  │ • Reflexion memory   │ │
│  │ • Formal ver │  │ • Fallback   │  │ • Causal reasoning   │ │
│  └──────┬───────┘  └──────┬───────┘  │ • Skill library      │ │
│         │                 │          │ • HNSW search        │ │
│         └─────────────────┼──────────┴──────────────────────┘ │
│                           │                                    │
│                    ┌──────▼───────┐                           │
│                    │   ruvector   │  (Optional: Scale tier)   │
│                    │  500M+ scale │                           │
│                    └──────────────┘                           │
└────────────────────────────────────────────────────────────────┘
```

---

## Existing Capabilities (What We DON'T Build)

### AgentDB (29 MCP Tools Already Built)

**Core Vector Tools** (5):
- `agentdb_init` - Initialize memory
- `agentdb_insert` / `agentdb_insert_batch` - Store vectors
- `agentdb_search` - Semantic search
- `agentdb_delete` - Remove items

**Frontier Memory Tools** (9):
- `causal_add_edge` / `causal_query` - Causal reasoning
- `reflexion_store` / `reflexion_retrieve` - Self-critique memory
- `skill_create` / `skill_search` - Skill library
- `recall_with_certificate` - Verified recall
- `db_stats` - Database statistics
- `learner_discover` - Pattern discovery

**Learning System Tools** (10):
- PPO, Decision Transformer, MCTS
- Explainable AI
- HNSW indexing (150x faster)
- QUIC sync

### agentic-flow (Already Built)

- Multi-model router (100+ LLM providers)
- ReasoningBank (persistent learning)
- Agent Booster (352x faster code ops)
- QUIC transport (50-70% faster than TCP)
- Federation Hub (cross-agent memory)

### aidefence (Already Built)

- Detection Layer (<10ms): Pattern matching, PII sanitization
- Behavioral Analysis (<100ms): Anomaly detection
- Formal Verification (<500ms): Policy enforcement
- Adaptive Response (<50ms): Mitigation execution
- 98.3% test coverage

### ruvector (Already Built)

- <0.5ms p50 latency
- 50K+ QPS per instance
- 4-32x compression
- 500M+ concurrent streams
- WASM for browser/edge

---

## What We ARE Building

### 1. pMemory MCP Server

A thin orchestration layer that:

1. **Unifies MCP namespaces**: Single `pmemory_*` namespace that routes to underlying tools
2. **Applies security by default**: All operations pass through aidefence
3. **Manages LLM routing**: Embedding generation via agentic-flow router
4. **Coordinates learning**: Links ReasoningBank patterns to memory operations

### 2. MCP Tool Interface

```typescript
// Exposed MCP Tools (wrapping existing capabilities)

// Core Memory (delegates to AgentDB)
pmemory_init          // → agentdb_init + aidefence validation
pmemory_store         // → aidefence scan → agentdb_insert
pmemory_search        // → aidefence validate → agentdb_search
pmemory_delete        // → auth check → agentdb_delete

// Intelligence (delegates to AgentDB Frontier)
pmemory_causal_link   // → causal_add_edge
pmemory_causal_query  // → causal_query
pmemory_reflect       // → reflexion_store
pmemory_recall        // → reflexion_retrieve + recall_with_certificate

// Learning (delegates to AgentDB + ReasoningBank)
pmemory_skill_store   // → skill_create
pmemory_skill_find    // → skill_search
pmemory_learn         // → learner_discover + ReasoningBank update

// Security (delegates to aidefence)
pmemory_scan          // → aidefence threat detection
pmemory_audit         // → audit log query

// Provider Management (delegates to agentic-flow)
pmemory_embed         // → agentic-flow router → optimal LLM
pmemory_provider_set  // → configure preferred provider
pmemory_provider_list // → list available providers
```

### 3. Configuration Layer

```yaml
# pmemory.yaml
memory:
  backend: agentdb        # or ruvector for scale
  namespace: default

security:
  enabled: true
  threat_threshold: 0.7
  pii_filter: true
  audit_all: true

llm:
  router: agentic-flow
  default_provider: claude
  fallback_chain:
    - claude
    - openai
    - gemini
    - ollama

learning:
  reflexion: true
  causal_tracking: true
  reasoningbank: true
```

---

## Architecture: Integration Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Claude/Agent                                 │
│                              │                                       │
│                    MCP Protocol (stdio/sse)                         │
│                              │                                       │
├──────────────────────────────▼──────────────────────────────────────┤
│                      pMemory MCP Server                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Request Handler                            │   │
│  │  1. Parse MCP request                                         │   │
│  │  2. Route to appropriate service                              │   │
│  │  3. Apply security (aidefence)                                │   │
│  │  4. Execute via underlying tool                               │   │
│  │  5. Return MCP response                                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│         ┌────────────────────┼────────────────────┐                 │
│         ▼                    ▼                    ▼                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐   │
│  │  aidefence  │     │agentic-flow │     │     AgentDB         │   │
│  │             │     │   Router    │     │                     │   │
│  │ Scan all    │     │             │     │ • Vector store      │   │
│  │ inputs for  │     │ Route embed │     │ • Causal graph      │   │
│  │ threats     │     │ requests to │     │ • Reflexion         │   │
│  │             │     │ optimal LLM │     │ • Skills            │   │
│  └─────────────┘     └─────────────┘     └─────────────────────┘   │
│                                                                      │
│  Optional (scale tier):                                             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                        ruvector                               │   │
│  │            (When >1M vectors, distributed deployment)         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## What Makes This Novel

### 1. First Secure-by-Default Agent Memory

Every operation passes through aidefence:
- Prompt injection blocked at memory ingestion
- PII automatically filtered
- Formal verification of policy compliance
- Audit trail of all memory access

### 2. LLM-Agnostic Embedding

Store once, query with any provider:
- agentic-flow routes to optimal LLM for embedding
- 85-99% cost savings via intelligent routing
- Fallback chains for reliability
- Switch providers without re-embedding

### 3. Self-Learning Memory

Connected learning systems:
- AgentDB's reflexion stores successes/failures
- ReasoningBank persists patterns across sessions
- Causal graphs track what leads to what
- Skills library grows from experience

### 4. MCP-Native Interface

Not REST, not SDK—pure MCP:
- Works directly with Claude Code, Claude Desktop
- No additional infrastructure
- Portable across MCP-compatible clients
- Single installation: `npx pmemory`

---

## Implementation: What We Actually Build

### Code Volume

| Component | Estimated LOC | Purpose |
|-----------|---------------|---------|
| MCP Server | ~500 | Protocol handling |
| Tool Routing | ~300 | Map pmemory_* to underlying tools |
| Security Wrapper | ~200 | aidefence integration |
| LLM Routing | ~200 | agentic-flow integration |
| Config Management | ~300 | YAML parsing, validation |
| CLI | ~200 | Installation, config commands |
| Tests | ~500 | Integration tests |
| **Total** | **~2,200** | Thin orchestration layer |

### Dependencies (Not Building These)

```json
{
  "dependencies": {
    "agentdb": "^1.6.0",
    "aidefence": "^2.1.0",
    "agentic-flow": "latest",
    "@modelcontextprotocol/sdk": "latest"
  }
}
```

### Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Scaffold | 1 week | MCP server, basic routing |
| 2. Integration | 1 week | AgentDB + aidefence + agentic-flow wired |
| 3. Testing | 1 week | Integration tests, demo |
| **Total** | **3 weeks** | Production-ready MCP server |

---

## Validation

### Demo Scenario

```
Task: Agent researching "quantum computing impact on cryptography"

1. Agent calls pmemory_search("quantum cryptography")
   → aidefence validates query (no injection)
   → AgentDB searches vector store
   → Returns relevant memories

2. Agent synthesizes findings
   → Uses pmemory_embed (routed via agentic-flow to cheapest LLM)

3. Agent stores new insight
   → pmemory_store with content
   → aidefence scans for PII/threats
   → AgentDB stores with embedding
   → Causal link created to source memories

4. Agent reflects on success
   → pmemory_reflect with outcome
   → Reflexion memory updated
   → ReasoningBank pattern stored
```

### Success Metrics

- [ ] All AgentDB MCP tools accessible via pmemory_* namespace
- [ ] 100% of operations pass through aidefence
- [ ] Embedding generation routes through agentic-flow
- [ ] Works in Claude Code via `npx pmemory`
- [ ] <3 weeks to production

---

## Conclusion

**pMemory is an integration project, not a development project.**

We're not building:
- ❌ A new vector database (AgentDB exists)
- ❌ A new LLM router (agentic-flow exists)
- ❌ A new security system (aidefence exists)
- ❌ A REST API (MCP is the interface)

We're building:
- ✅ MCP server that unifies existing tools
- ✅ Security-first orchestration layer
- ✅ Configuration management
- ✅ ~2,200 lines of integration code

**The novel contribution is the secure, unified, MCP-native orchestration—not reinventing the underlying capabilities.**
