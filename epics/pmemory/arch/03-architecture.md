# pMemory Architecture

## MCP-First Integration Design

**Document Status**: Revised
**Version**: 2.0.0
**Last Updated**: November 2024

---

## 1. Architecture Overview

### 1.1 Design Principle

**pMemory is an integration layer, not a platform.**

We build ~2,200 lines of orchestration code. We leverage:
- **AgentDB**: 29 MCP tools (memory, causal graphs, reflexion, skills)
- **aidefence**: Security scanning, PII filtering, audit logging
- **agentic-flow**: LLM routing, ReasoningBank
- **ruvector**: Scale tier (optional)

### 1.2 System Context

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM CONTEXT                                 │
│                                                                          │
│   ┌─────────────────┐                                                   │
│   │   Claude Code   │                                                   │
│   │  Claude Desktop │                                                   │
│   │  MCP Clients    │                                                   │
│   └────────┬────────┘                                                   │
│            │                                                            │
│            │  MCP Protocol (stdio/sse)                                  │
│            │                                                            │
│   ┌────────▼────────────────────────────────────────────────────────┐  │
│   │                    pMemory MCP Server                            │  │
│   │                                                                  │  │
│   │   ┌─────────────────────────────────────────────────────────┐   │  │
│   │   │                  Orchestration Layer                     │   │  │
│   │   │                    (~2,200 LOC)                          │   │  │
│   │   │                                                          │   │  │
│   │   │  • MCP protocol handling                                 │   │  │
│   │   │  • Tool routing (pmemory_* → underlying tools)          │   │  │
│   │   │  • Security enforcement                                  │   │  │
│   │   │  • Configuration management                              │   │  │
│   │   └─────────────────────────────────────────────────────────┘   │  │
│   │                              │                                   │  │
│   │       ┌──────────────────────┼──────────────────────┐           │  │
│   │       ▼                      ▼                      ▼           │  │
│   │  ┌─────────────┐      ┌─────────────┐      ┌──────────────┐    │  │
│   │  │  aidefence  │      │agentic-flow │      │   AgentDB    │    │  │
│   │  │             │      │             │      │              │    │  │
│   │  │ • Scan      │      │ • Route     │      │ • 29 MCP     │    │  │
│   │  │ • Filter    │      │ • Embed     │      │   tools      │    │  │
│   │  │ • Log       │      │ • Fallback  │      │              │    │  │
│   │  └─────────────┘      └─────────────┘      └──────────────┘    │  │
│   │                                                                  │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│   Optional (scale):                                                     │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                          ruvector                                │  │
│   │               (When >1M vectors, distributed)                    │  │
│   └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 MCP Server (We Build This)

```
┌────────────────────────────────────────────────────────────────────────┐
│                       pMemory MCP Server                                │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      Entry Point                                  │  │
│  │                                                                   │  │
│  │  src/index.ts                                                     │  │
│  │  • Initialize MCP server                                          │  │
│  │  • Register tool handlers                                         │  │
│  │  • Start stdio transport                                          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     Tool Registry                                 │  │
│  │                                                                   │  │
│  │  src/tools/                                                       │  │
│  │  ├── core.ts        (pmemory_init, store, search, delete)        │  │
│  │  ├── intelligence.ts (causal_link, causal_query, reflect, recall)│  │
│  │  ├── learning.ts    (skill_store, skill_find, learn)             │  │
│  │  ├── security.ts    (scan, audit)                                │  │
│  │  └── provider.ts    (embed, provider_set, provider_list)         │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    Service Layer                                  │  │
│  │                                                                   │  │
│  │  src/services/                                                    │  │
│  │  ├── security.ts    (wraps aidefence)                            │  │
│  │  ├── memory.ts      (wraps AgentDB)                              │  │
│  │  ├── llm.ts         (wraps agentic-flow)                         │  │
│  │  └── config.ts      (configuration management)                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                   Configuration                                   │  │
│  │                                                                   │  │
│  │  src/config/                                                      │  │
│  │  ├── schema.ts      (YAML schema validation)                     │  │
│  │  └── defaults.ts    (default configuration)                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 External Dependencies (Already Built)

```
┌────────────────────────────────────────────────────────────────────────┐
│                       AgentDB (npm: agentdb)                           │
│                                                                        │
│  29 MCP Tools:                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ Core Vector  │  │  Frontier    │  │  Learning    │                 │
│  │              │  │  Memory      │  │  System      │                 │
│  │ • init       │  │ • causal_*   │  │ • PPO        │                 │
│  │ • insert     │  │ • reflexion_*│  │ • Decision   │                 │
│  │ • search     │  │ • skill_*    │  │   Transformer│                 │
│  │ • delete     │  │ • recall     │  │ • MCTS       │                 │
│  │ • batch      │  │ • learner    │  │              │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                        │
│  Performance: p95 <50ms, 150x faster HNSW search                      │
│  Features: QUIC sync, causal graphs, reflexion memory                 │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                       aidefence (npm: aidefence)                       │
│                                                                        │
│  Security Layers:                                                      │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Detection (<10ms)    │ Analysis (<100ms)   │ Response (<50ms)    │ │
│  │                      │                     │                      │ │
│  │ • Pattern matching   │ • Behavioral       │ • Strategy select    │ │
│  │ • Prompt injection   │ • Anomaly detect   │ • Mitigation         │ │
│  │ • PII filter         │ • Temporal pattern │ • Logging            │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  Coverage: 98.3% test coverage, formal verification                   │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                    agentic-flow (npm: agentic-flow)                    │
│                                                                        │
│  LLM Routing:                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐ │
│  │ Multi-Model Router                                                │ │
│  │                                                                   │ │
│  │ • 100+ LLM providers                                              │ │
│  │ • 85-99% cost savings                                             │ │
│  │ • Intelligent selection (cost/latency/privacy)                   │ │
│  │ • Fallback chains                                                 │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  Additional: ReasoningBank, Agent Booster, QUIC transport            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow

### 3.1 Store Operation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      pmemory_store Data Flow                            │
│                                                                         │
│  1. MCP Request                                                         │
│     └── { tool: "pmemory_store", content: "...", causal_sources: [...]}│
│                              │                                          │
│  2. Validate Schema          ▼                                          │
│     └── Check required fields, types                                    │
│                              │                                          │
│  3. Security Scan            ▼                                          │
│     └── aidefence.scan(content)                                         │
│         ├── Pass: Continue                                              │
│         └── Fail: Return { error: "Threat detected", details }         │
│                              │                                          │
│  4. Generate Embedding       ▼                                          │
│     └── agentic-flow.embed(content)                                     │
│         └── Routes to optimal LLM provider                              │
│                              │                                          │
│  5. Store in AgentDB         ▼                                          │
│     └── agentdb.insert({ content, embedding, metadata })                │
│         └── Returns: item_id                                            │
│                              │                                          │
│  6. Create Causal Links      ▼                                          │
│     └── For each source_id in causal_sources:                           │
│         agentdb.causal_add_edge(source_id, item_id)                     │
│                              │                                          │
│  7. Audit Log                ▼                                          │
│     └── aidefence.log({ operation: "store", item_id, user, timestamp }) │
│                              │                                          │
│  8. MCP Response             ▼                                          │
│     └── { success: true, id: item_id }                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Search Operation

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     pmemory_search Data Flow                            │
│                                                                         │
│  1. MCP Request                                                         │
│     └── { tool: "pmemory_search", query: "...", top_k: 10 }            │
│                              │                                          │
│  2. Validate Query           ▼                                          │
│     └── aidefence.validate(query)                                       │
│         └── Check for injection patterns                                │
│                              │                                          │
│  3. Generate Embedding       ▼                                          │
│     └── agentic-flow.embed(query)                                       │
│                              │                                          │
│  4. Search AgentDB           ▼                                          │
│     └── agentdb.search({ embedding, top_k })                            │
│                              │                                          │
│  5. Optional: Causal Context ▼                                          │
│     └── If include_causal:                                              │
│         For each result: agentdb.causal_query(result.id)               │
│                              │                                          │
│  6. Audit Log                ▼                                          │
│     └── aidefence.log({ operation: "search", query, results_count })   │
│                              │                                          │
│  7. MCP Response             ▼                                          │
│     └── { results: [...], causal_context: [...] }                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. File Structure

```
pmemory/
├── package.json
├── tsconfig.json
├── README.md
│
├── src/
│   ├── index.ts              # MCP server entry point
│   │
│   ├── tools/                # MCP tool handlers
│   │   ├── index.ts          # Tool registry
│   │   ├── core.ts           # init, store, search, delete
│   │   ├── intelligence.ts   # causal, reflect, recall
│   │   ├── learning.ts       # skill, learn
│   │   ├── security.ts       # scan, audit
│   │   └── provider.ts       # embed, provider management
│   │
│   ├── services/             # External integrations
│   │   ├── memory.ts         # AgentDB wrapper
│   │   ├── security.ts       # aidefence wrapper
│   │   ├── llm.ts            # agentic-flow wrapper
│   │   └── config.ts         # Configuration loader
│   │
│   ├── config/
│   │   ├── schema.ts         # YAML validation
│   │   └── defaults.ts       # Default config values
│   │
│   └── types/
│       └── index.ts          # TypeScript types
│
├── tests/
│   ├── integration/
│   │   ├── store.test.ts
│   │   ├── search.test.ts
│   │   ├── security.test.ts
│   │   └── provider.test.ts
│   └── e2e/
│       └── demo.test.ts
│
└── bin/
    └── pmemory.js            # CLI entry point
```

---

## 5. Configuration Schema

```yaml
# ~/.pmemory/config.yaml

# Memory backend configuration
memory:
  backend: agentdb              # agentdb | ruvector
  namespace: default            # Memory namespace
  data_path: ~/.pmemory/data    # Local data directory

# Security configuration
security:
  enabled: true                 # Enable/disable security scanning
  level: balanced               # strict | balanced | permissive | off
  pii_filter: true              # Enable PII detection and filtering
  audit:
    enabled: true               # Enable audit logging
    retention_days: 30          # Days to retain audit logs

# LLM routing configuration
llm:
  default_provider: claude      # Default embedding provider
  fallback_chain:               # Provider fallback order
    - claude
    - openai
    - ollama
  routing_strategy: cost        # cost | latency | privacy
  cache_embeddings: true        # Cache embeddings locally

# Learning configuration
learning:
  reflexion: true               # Enable reflexion memory
  causal_tracking: true         # Enable causal graph building
  skill_library: true           # Enable skill storage
  reasoningbank: true           # Enable ReasoningBank integration
```

---

## 6. MCP Protocol Details

### 6.1 Server Registration

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "pmemory",
  version: "1.0.0",
}, {
  capabilities: {
    tools: {},
    resources: {},
  },
});

// Register tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    { name: "pmemory_init", ... },
    { name: "pmemory_store", ... },
    { name: "pmemory_search", ... },
    // ... all 17 tools
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  return await toolHandlers[name](args);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 6.2 Tool Handler Pattern

```typescript
// src/tools/core.ts
import { security } from "../services/security";
import { memory } from "../services/memory";
import { llm } from "../services/llm";

export async function pmemory_store(args: StoreArgs) {
  // 1. Security scan
  const scanResult = await security.scan(args.content);
  if (scanResult.threat) {
    return {
      content: [{ type: "text", text: JSON.stringify({
        error: "Threat detected",
        details: scanResult.details,
      })}],
      isError: true,
    };
  }

  // 2. Generate embedding
  const embedding = await llm.embed(args.content);

  // 3. Store in AgentDB
  const id = await memory.insert({
    content: args.content,
    embedding,
    metadata: args.metadata,
  });

  // 4. Create causal links
  if (args.causal_sources) {
    for (const sourceId of args.causal_sources) {
      await memory.addCausalEdge(sourceId, id);
    }
  }

  // 5. Audit log
  await security.log("store", { id, content_length: args.content.length });

  // 6. Return success
  return {
    content: [{ type: "text", text: JSON.stringify({ success: true, id })}],
  };
}
```

---

## 7. Deployment

### 7.1 npm Package

```json
{
  "name": "pmemory",
  "version": "1.0.0",
  "bin": {
    "pmemory": "./bin/pmemory.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "latest",
    "agentdb": "^1.6.0",
    "aidefence": "^2.1.0",
    "agentic-flow": "latest",
    "yaml": "^2.0.0"
  }
}
```

### 7.2 Claude Desktop Config

```json
{
  "mcpServers": {
    "pmemory": {
      "command": "npx",
      "args": ["pmemory", "mcp", "start"],
      "env": {
        "ANTHROPIC_API_KEY": "...",
        "OPENAI_API_KEY": "..."
      }
    }
  }
}
```

### 7.3 Usage

```bash
# Install globally
npm install -g pmemory

# Or use npx
npx pmemory mcp start

# Initialize config
pmemory init

# Configure provider
pmemory config set llm.default_provider openai
```

---

## 8. Performance Characteristics

### 8.1 Latency Breakdown

| Operation | pMemory Overhead | Underlying Tool | Total |
|-----------|------------------|-----------------|-------|
| Store | ~5ms | AgentDB 50ms + aidefence 10ms + embed 200ms | ~265ms |
| Search | ~2ms | AgentDB 50ms + aidefence 5ms | ~57ms |
| Causal query | ~1ms | AgentDB 20ms | ~21ms |
| Reflect | ~2ms | AgentDB 30ms | ~32ms |

**Note**: pMemory adds minimal overhead (<10ms). Performance is determined by underlying tools.

### 8.2 Memory Usage

| Component | Memory |
|-----------|--------|
| pMemory server | ~50MB |
| AgentDB | ~100MB + 4GB per 1M vectors |
| aidefence | ~100MB |
| agentic-flow | ~50MB |

---

## 9. Document References

- **Thesis**: `00-thesis.md`
- **Specification**: `spec/01-specification.md`
- **Implementation**: `implementation/05-implementation.md`
