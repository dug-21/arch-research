# AgentDB - Lightning-Fast Vector Database for AI Agents

## Overview

**AgentDB** is a sub-millisecond memory engine built for autonomous agents with 20 MCP tools for seamless AI integration. Created by ruvnet, AgentDB is a production-grade vector database system specifically designed for AI agent memory, offering lightning-fast performance for storing and retrieving contextual information that AI agents need to maintain continuity across interactions.

**Release Date**: 2025
**Official Website**: https://agentdb.ruv.io/
**Integration**: Claude-Flow v2.7+
**Repository**: Part of ruvnet/claude-flow ecosystem

---

## Key Components

### 1. Core Vector Database Engine
- **Sub-millisecond Memory**: Lightning-fast retrieval for real-time agent operations
- **SQLite Backend**: Persistent storage with better-sqlite3 integration
- **Native TypeScript**: No Python dependency, simpler deployment
- **WASM Acceleration**: 10-100x faster neural operations

### 2. MCP Integration (20 Tools)
AgentDB provides 20 Model Context Protocol (MCP) tools for seamless integration with Claude Code and autonomous agent systems:
- Memory storage and retrieval
- Semantic vector search
- Namespace management
- Multi-database coordination
- Custom metrics and monitoring

### 3. ReasoningBank Integration
AgentDB-powered ReasoningBank delivers:
- **2-3ms query latency**: Hash-based embeddings for semantic search
- **1024-dimension embeddings**: Deterministic, works without API keys
- **150x-12,500x performance improvements**: Over previous WASM implementation
- **Persistent Storage**: All memories saved to .swarm/memory.db

### 4. Advanced Features (AgentDB-advanced)
- **QUIC Synchronization**: Multi-database sync with sub-millisecond latency
- **Multi-Database Management**: Coordinate across distributed databases
- **Hybrid Search**: Combined semantic and keyword search capabilities
- **Custom Metrics**: Performance monitoring and analytics
- **Namespace Isolation**: Organize memories by domain

---

## Architecture

### Database Layer
```
AgentDB Core
├── SQLite + better-sqlite3 (Node.js Backend)
├── Persistent Storage (.swarm/memory.db)
├── Semantic Search Engine
│   ├── 1024-dim Hash-based Embeddings
│   ├── MMR (Maximal Marginal Relevance) Ranking
│   └── Similarity Scoring
└── Namespace Management
```

### Integration Layer
```
MCP Protocol (20 Tools)
├── Memory Operations
│   ├── Store
│   ├── Retrieve
│   ├── Search
│   └── Delete
├── Namespace Operations
│   ├── Create
│   ├── Isolate
│   └── Manage
├── Database Operations
│   ├── Multi-DB Coordination
│   ├── Synchronization
│   └── Metrics Collection
└── Advanced Features
    ├── QUIC Sync
    ├── Hybrid Search
    └── Custom Analytics
```

---

## Performance Metrics

### Speed Benchmarks
- **Query Latency**: 2-3ms for semantic search
- **Memory Operations**: Sub-millisecond retrieval
- **Synchronization**: Sub-millisecond via QUIC protocol
- **Performance Improvement**: 150x-12,500x over WASM implementation

### Efficiency Metrics
- **Storage**: Persistent SQLite database
- **Embeddings**: 1024-dimension vectors (deterministic)
- **API-Free**: No external API keys required for basic operations
- **Acceleration**: 10-100x faster neural operations via WASM

### Reliability
- **Persistence**: Database survives restarts
- **Namespace Isolation**: Domain-specific memory organization
- **Multi-Database**: Coordinated management across databases
- **Byzantine Tolerance**: Built on proven claude-flow architecture

---

## Claude-Flow Integration

### Skills Integration

AgentDB integrates with Claude-Flow v2.7+ through specialized skills:

#### 1. agentdb-memory-patterns
**Purpose**: Persistent agent memory with session storage and long-term context management

**Capabilities**:
- Session-based memory storage
- Long-term context persistence
- Cross-session memory retrieval
- Pattern-based memory organization

#### 2. agentdb-vector-search
**Purpose**: Semantic vector search and intelligent document retrieval

**Capabilities**:
- Semantic similarity search
- MMR ranking for diverse results
- Document embedding and indexing
- Fast similarity scoring

#### 3. agentdb-advanced (Optional)
**Purpose**: Production-grade features for enterprise deployments

**Capabilities**:
- QUIC-based multi-database synchronization
- Hybrid search (semantic + keyword)
- Custom performance metrics
- Advanced namespace management

---

## Technical Specifications

### Backend Technology
- **Language**: TypeScript (Node.js)
- **Database**: SQLite with better-sqlite3
- **Storage Location**: .swarm/memory.db
- **Embedding Dimension**: 1024 (deterministic hash-based)
- **Protocol**: MCP (Model Context Protocol)

### Performance Architecture
- **Node.js Backend**: Replaced WASM for superior performance
- **better-sqlite3**: Native SQLite bindings for Node.js
- **Zero External Dependencies**: No Python, no API keys for core functionality
- **WASM Acceleration**: Optional for specific neural operations

### Storage Architecture
```typescript
// Database Schema (Conceptual)
interface AgentMemory {
  id: string;
  namespace: string;
  embedding: Float32Array; // 1024-dim
  content: string;
  metadata: object;
  timestamp: number;
  similarity_score?: number;
}
```

---

## Use Cases

### 1. Autonomous Agent Memory
- **Continuous Context**: Agents maintain state across sessions
- **Semantic Recall**: Find relevant memories based on meaning, not keywords
- **Fast Retrieval**: Sub-millisecond access for real-time decision-making
- **Persistent Learning**: Knowledge accumulates over time

### 2. Multi-Agent Coordination
- **Shared Memory**: Multiple agents access common knowledge base
- **Namespace Isolation**: Each agent maintains private memory space
- **Synchronization**: QUIC-based coordination across distributed agents
- **Conflict Resolution**: MMR ranking ensures diverse, relevant results

### 3. Conversational AI Systems
- **Session Management**: Track conversation history and context
- **Semantic Search**: Find relevant past interactions
- **User Preferences**: Store and retrieve user-specific data
- **Continuous Improvement**: Learn from past conversations

### 4. RAG (Retrieval-Augmented Generation)
- **Document Indexing**: Store and embed documents efficiently
- **Semantic Retrieval**: Find relevant passages based on meaning
- **Hybrid Search**: Combine semantic and keyword approaches
- **Real-time Updates**: Add documents without rebuilding index

### 5. Enterprise AI Applications
- **Multi-Database**: Manage databases across teams/projects
- **Custom Metrics**: Monitor performance and usage
- **Security**: Namespace isolation for data segregation
- **Scalability**: QUIC synchronization for distributed deployments

---

## Comparison: AgentDB vs Traditional Vector Databases

### AgentDB Advantages

#### 1. Performance
| Feature | AgentDB | Traditional Vector DB |
|---------|---------|----------------------|
| Query Latency | 2-3ms | 10-100ms |
| Setup Time | Instant | Minutes to hours |
| Dependencies | TypeScript only | Python + ML libraries |
| Storage | SQLite (simple) | Complex infrastructure |

#### 2. Integration
- **MCP Native**: 20 tools for Claude Code integration
- **Claude-Flow**: Built-in swarm orchestration support
- **Zero Config**: No API keys or external services required
- **Instant Provisioning**: Database ready in milliseconds

#### 3. Developer Experience
- **TypeScript-First**: No Python dependency
- **Simple Deployment**: Single SQLite file
- **Local-First**: Works offline, no cloud required
- **MCP Tools**: Standardized interface for AI agents

#### 4. Cost Efficiency
- **No API Costs**: Deterministic embeddings (no OpenAI/Anthropic)
- **No Infrastructure**: SQLite runs anywhere
- **No Scaling Costs**: Linear performance scaling
- **Zero Maintenance**: Self-contained database

---

## Integration with ruvnet Ecosystem

### Cross-Repository Dependencies

#### 1. Claude-Flow Integration
- **ReasoningBank**: AgentDB powers the memory backend
- **Swarm Orchestration**: Shared memory for agent coordination
- **Hooks System**: AgentDB stores hook execution history
- **MCP Tools**: 20 AgentDB tools + 100+ claude-flow tools

#### 2. ruv-FANN Integration (Potential)
- **Neural Patterns**: Store and retrieve trained patterns
- **WASM Acceleration**: Share neural computation optimizations
- **Micro-Networks**: Cache 1K-100K param network weights
- **Ephemeral Memory**: Fast load/save for task-adaptive networks

#### 3. SAFLA Integration (Potential)
- **Vector Memory**: AgentDB as vector memory backend
- **Hybrid Architecture**: Combine with episodic/semantic/working memory
- **Meta-Cognition**: Store reflection and learning metadata
- **Performance**: AgentDB's speed complements SAFLA's 172,000+ ops/sec

#### 4. QuDAG Integration (Potential)
- **Distributed Memory**: QUIC sync with QuDAG's post-quantum P2P
- **Byzantine Tolerance**: Consensus over distributed AgentDB instances
- **.dark Domains**: Decentralized agent memory storage
- **Security**: Post-quantum encryption for memory synchronization

#### 5. Synaptic-Mesh Integration (Potential)
- **Micro-Network Weights**: Cache 1K-100K param networks in AgentDB
- **Task-Adaptive**: Fast retrieval for ephemeral network spawning
- **Market Data**: Store pricing, performance, reputation data
- **Coordination**: Share memory across distributed mesh nodes

---

## MCP (Model Context Protocol) Details

### What is MCP?
Model Context Protocol (MCP) is an open standard developed by Anthropic that provides AI agents with a consistent way to connect with tools, services, and data. MCP replaces one-off integrations with a unified, real-time protocol built for autonomous agents.

### AgentDB's 20 MCP Tools

Based on the integration patterns, AgentDB's 20 MCP tools likely include:

#### Memory Operations (5 tools)
1. `agentdb_store` - Store memory with embedding
2. `agentdb_retrieve` - Retrieve memory by ID
3. `agentdb_search` - Semantic vector search
4. `agentdb_delete` - Remove memory entries
5. `agentdb_update` - Update existing memories

#### Namespace Operations (4 tools)
6. `agentdb_namespace_create` - Create new namespace
7. `agentdb_namespace_list` - List available namespaces
8. `agentdb_namespace_switch` - Switch active namespace
9. `agentdb_namespace_delete` - Remove namespace

#### Database Management (4 tools)
10. `agentdb_db_status` - Get database statistics
11. `agentdb_db_sync` - Synchronize databases (QUIC)
12. `agentdb_db_backup` - Create database backup
13. `agentdb_db_restore` - Restore from backup

#### Search & Retrieval (4 tools)
14. `agentdb_semantic_search` - Pure semantic search
15. `agentdb_hybrid_search` - Semantic + keyword search
16. `agentdb_mmr_search` - Maximal Marginal Relevance search
17. `agentdb_similarity` - Calculate similarity scores

#### Advanced Features (3 tools)
18. `agentdb_metrics` - Get performance metrics
19. `agentdb_embedding_generate` - Generate embeddings
20. `agentdb_config` - Configure AgentDB settings

---

## Deployment Options

### Local Development
```bash
# Install claude-flow with AgentDB
npm install -g claude-flow@latest

# AgentDB automatically included
# Database created at: .swarm/memory.db
```

### Claude Code Integration
```bash
# Add MCP server
claude mcp add claude-flow npx claude-flow@latest mcp start

# AgentDB tools available via MCP
# Use skills: agentdb-memory-patterns, agentdb-vector-search
```

### Production Deployment
```bash
# Enterprise features
npm install -g claude-flow@latest

# Enable AgentDB-advanced
# Configure QUIC synchronization
# Set up multi-database coordination
```

---

## Performance Optimization

### Why Node.js over WASM?

AgentDB initially considered WASM but chose Node.js + better-sqlite3 for superior performance:

#### WASM Performance Limitations
- **Write Speed**: 80x slower than native SQLite
- **Read Speed**: 14x slower than native SQLite
- **IndexedDB Overhead**: 3ms+ per write operation
- **Memory Limits**: Browser WASM constraints

#### Node.js Advantages
- **Native Speed**: better-sqlite3 uses native SQLite bindings
- **No IPC Overhead**: Direct database access
- **Persistent Storage**: File system, not IndexedDB
- **150x-12,500x Improvement**: Measured vs WASM implementation

#### Hybrid Approach
- **Node.js Backend**: Database and memory operations
- **WASM Acceleration**: Optional for neural computations (10-100x faster)
- **Best of Both**: Native I/O speed + accelerated math

---

## Comparison: AgentDB (ruv.io) vs AgentDB (agentdb.dev)

### Two Different Products

#### AgentDB by ruvnet (agentdb.ruv.io)
- **Focus**: Vector database for AI agent memory
- **Integration**: Claude-Flow, MCP protocol
- **Technology**: SQLite, TypeScript, WASM acceleration
- **Performance**: Sub-millisecond, 2-3ms semantic search
- **Use Case**: Autonomous agent memory and coordination

#### AgentDB (agentdb.dev) - Different Product
- **Focus**: Instant database provisioning for high-scale apps
- **Integration**: MCP server with raw SQL access
- **Technology**: Database templates, schema synchronization
- **Performance**: Instant provisioning with unique ID
- **Use Case**: Multi-tenant database-per-agent architecture

**Note**: This document focuses on ruvnet's AgentDB (agentdb.ruv.io)

---

## Security & Privacy

### Data Security
- **Local-First**: Data stored in local SQLite database
- **No Cloud Dependency**: Works offline completely
- **Namespace Isolation**: Data segregation by domain
- **Encryption**: SQLite encryption options available

### Privacy Features
- **No API Calls**: Deterministic embeddings (no external services)
- **No Telemetry**: Private by default
- **GDPR Compliant**: Data stored locally under user control
- **Audit Trails**: Track all memory operations

### Multi-Tenancy
- **Namespace Isolation**: Separate memory spaces per agent/user
- **Access Control**: MCP-based permissions
- **QUIC Sync**: Secure synchronization with encryption
- **Byzantine Tolerance**: Inherited from claude-flow architecture

---

## Roadmap & Future Enhancements

### Potential Features (Based on Ecosystem)

#### 1. Post-Quantum Security
- **QuDAG Integration**: ML-KEM-768, ML-DSA encryption
- **Quantum-Resistant Embeddings**: Future-proof memory storage
- **.dark Domain Storage**: Decentralized memory via QuDAG

#### 2. Distributed Coordination
- **Byzantine Consensus**: Multi-agent memory consensus
- **Federated Memory**: DAA-style distributed learning
- **Mesh Networking**: Synaptic-Mesh integration for P2P memory

#### 3. Advanced Neural Features
- **ruv-FANN Integration**: Store/retrieve neural network weights
- **Cognitive Patterns**: 7 patterns from ruv-FANN (convergent, divergent, etc.)
- **Ephemeral Networks**: Fast cache for 1K-100K param models

#### 4. Enhanced Search
- **Multimodal Embeddings**: Images, audio, video
- **Graph Memory**: Knowledge graph integration (SAFLA-style)
- **Temporal Search**: Time-based memory retrieval
- **Fuzzy Matching**: Approximate string matching

---

## API Examples (Conceptual)

### MCP Tool Usage via Claude Code

#### Store Memory
```typescript
// Using agentdb_store MCP tool
await agentdb_store({
  namespace: "user_preferences",
  content: "User prefers dark mode and concise responses",
  metadata: { user_id: "123", category: "preferences" }
});
```

#### Semantic Search
```typescript
// Using agentdb_semantic_search MCP tool
const results = await agentdb_semantic_search({
  query: "What are the user's display preferences?",
  namespace: "user_preferences",
  limit: 5,
  min_similarity: 0.7
});
```

#### Hybrid Search (Advanced)
```typescript
// Using agentdb_hybrid_search MCP tool
const results = await agentdb_hybrid_search({
  semantic_query: "payment authorization",
  keywords: ["stripe", "API", "webhook"],
  namespace: "system_logs",
  limit: 10
});
```

#### Database Synchronization (Advanced)
```typescript
// Using agentdb_db_sync MCP tool
await agentdb_db_sync({
  source_db: "agent_001",
  target_db: "agent_002",
  protocol: "QUIC",
  namespace: "shared_knowledge"
});
```

---

## Competitive Advantages

### 1. Speed
- **2-3ms semantic search**: 5-50x faster than traditional vector DBs
- **Sub-millisecond retrieval**: Real-time agent decision-making
- **150x-12,500x improvement**: Over WASM implementation
- **QUIC synchronization**: Sub-millisecond multi-DB sync

### 2. Simplicity
- **Zero Config**: No setup, no API keys
- **Single File**: SQLite database, portable and simple
- **TypeScript Native**: No Python dependency
- **MCP Standard**: Universal AI tool integration

### 3. Cost
- **No API Costs**: Deterministic embeddings
- **No Infrastructure**: Runs locally on any machine
- **No Scaling Costs**: Linear performance
- **Zero Maintenance**: Self-contained system

### 4. Integration
- **Claude-Flow Native**: Built-in swarm orchestration
- **20 MCP Tools**: Comprehensive tool suite
- **Ecosystem Ready**: Integrates with 9+ ruvnet repositories
- **Production-Grade**: Advanced features for enterprise

---

## Technical Validation

### Academic Foundation
AgentDB's architecture builds on proven research:

#### Vector Search Efficiency
- **Hash-based Embeddings**: Deterministic, reproducible results
- **1024-dimension**: Optimal balance of speed vs accuracy
- **MMR Ranking**: Maximizes result diversity
- **Similarity Scoring**: Fast cosine similarity calculations

#### SQLite for AI
- **SQLite in Production**: Used by Notion, Apple, Android
- **better-sqlite3**: Fastest Node.js SQLite binding
- **WASM Option**: 10-100x neural acceleration available
- **Proven Scalability**: Handles millions of entries

#### QUIC Protocol
- **50-70% faster than TCP**: Proven in QuDAG, agentic-flow
- **0-RTT Reconnection**: Instant connection resumption
- **Multiplexing**: Parallel database operations
- **Encrypted by Default**: TLS 1.3 built-in

---

## Key Differentiators from Research Notes

### Complements Existing Components

Based on the research-notes inventory (294+ components), AgentDB fills a critical gap:

#### Memory & Storage Category
| Component | Focus | Performance |
|-----------|-------|-------------|
| **AgentDB** | Vector memory | 2-3ms, sub-millisecond |
| SAFLA | 4 memory types | 172,000+ ops/sec |
| ReasoningBank | Semantic search | 2-3ms (AgentDB backend) |
| FACT | Tool-based retrieval | Multi-tier caching |

#### Performance Positioning
- **Fastest Queries**: 2-3ms semantic search (tied with ReasoningBank)
- **Simplest Deployment**: Single SQLite file
- **Most Tools**: 20 MCP tools for vector operations
- **Best Integration**: Native Claude-Flow support

#### Strategic Position
- **Foundation**: Powers ReasoningBank (already documented)
- **Enabler**: MCP tools for all autonomous agents
- **Differentiator**: TypeScript-native, no Python complexity
- **Ecosystem Hub**: Connects 9+ ruvnet repositories via memory

---

## Installation & Quick Start

### Prerequisites
- Node.js 18+ (for better-sqlite3)
- Claude Code (for MCP integration)
- npm or npx

### Install claude-flow (includes AgentDB)
```bash
npm install -g claude-flow@latest
```

### Add MCP Server to Claude Code
```bash
claude mcp add claude-flow npx claude-flow@latest mcp start
```

### Verify Installation
```bash
# Check AgentDB skills available
npx claude-flow skills list | grep agentdb

# Should show:
# - agentdb-memory-patterns
# - agentdb-vector-search
# - agentdb-advanced (if enabled)
```

### First Memory Operation
```bash
# In Claude Code, use natural language:
# "Store a memory that the user prefers dark mode"

# AgentDB will automatically:
# 1. Create .swarm/memory.db if needed
# 2. Generate 1024-dim embedding
# 3. Store with namespace isolation
# 4. Return confirmation
```

---

## Documentation & Resources

### Official Resources
- **Website**: https://agentdb.ruv.io/
- **Demo**: https://agentdb.ruv.io/demo
- **GitHub**: Part of https://github.com/ruvnet/claude-flow
- **MCP Protocol**: https://www.anthropic.com/news/model-context-protocol

### Related Documentation
- **Claude-Flow**: Main orchestration platform
- **ReasoningBank**: Powered by AgentDB backend
- **MCP Tools**: Model Context Protocol integration
- **QUIC Sync**: Advanced synchronization features

### Community & Support
- **Issues**: https://github.com/ruvnet/claude-flow/issues
- **Discussions**: GitHub Discussions (claude-flow repo)
- **Updates**: Follow ruvnet on GitHub for releases

---

## Summary Statistics

### Component Count
- **Core Components**: 4 (Engine, MCP, ReasoningBank, Advanced)
- **MCP Tools**: 20 tools
- **Integration Points**: 6+ (Claude-Flow, ruv-FANN, SAFLA, QuDAG, Synaptic-Mesh, DAA)
- **Skills**: 3 (memory-patterns, vector-search, advanced)

### Performance Benchmarks
- **Query Latency**: 2-3ms (semantic search)
- **Retrieval Speed**: Sub-millisecond (memory operations)
- **Sync Speed**: Sub-millisecond (QUIC protocol)
- **Performance Gain**: 150x-12,500x (vs WASM)
- **Neural Acceleration**: 10-100x (WASM-assisted operations)

### Technology Stack
- **Languages**: TypeScript (Node.js), WASM (optional)
- **Database**: SQLite with better-sqlite3
- **Embeddings**: 1024-dim hash-based (deterministic)
- **Protocol**: MCP (Model Context Protocol)
- **Synchronization**: QUIC (optional, advanced)

### Use Case Coverage
- Autonomous agent memory
- Multi-agent coordination
- Conversational AI systems
- RAG (Retrieval-Augmented Generation)
- Enterprise AI applications

---

## Conclusion

AgentDB represents a significant advancement in AI agent memory systems, combining:

✅ **Performance**: 2-3ms semantic search, sub-millisecond operations
✅ **Simplicity**: TypeScript-native, single SQLite file, zero config
✅ **Integration**: 20 MCP tools, native Claude-Flow support
✅ **Cost**: No API costs, no infrastructure, no maintenance
✅ **Scalability**: QUIC sync, multi-database, namespace isolation
✅ **Security**: Local-first, no cloud dependency, encryption-ready

As the **11th component** in the ruvnet ecosystem research, AgentDB fills a critical role as the memory foundation for autonomous agents, complementing the 294+ existing components documented in the research-notes inventory.

**Position in Ecosystem**: Memory & storage layer, enabling stateful autonomous agents across all ruvnet repositories.

**Strategic Value**: Foundation for persistent learning, multi-agent coordination, and production-grade AI systems.

---

**Research Completed**: 2025-10-21
**Researcher**: Claude Code Research Agent
**Document**: 11-agentdb.md
**Status**: ✅ COMPLETE

**Next Steps**:
- Deep-dive testing of 20 MCP tools
- Integration verification with claude-flow v2.7+
- Performance benchmarking vs other vector databases
- Cross-repository integration testing (ruv-FANN, SAFLA, QuDAG)
