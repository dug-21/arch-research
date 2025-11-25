# pMemory SPARC Specification

## Phase 1: Specification

**Document Status**: Active
**Version**: 1.0.0
**Last Updated**: November 2024

---

## 1. Product Vision

### 1.1 Problem Statement

Current AI memory solutions force users into platform lock-in:
- Memory stored in provider clouds creates switching costs
- Slow retrieval (>500ms) breaks cognitive flow and agentic workflows
- No active intelligence—static retrieval only
- Security is an afterthought, not architectural foundation
- No learning from user patterns

### 1.2 Solution Overview

**pMemory** is an Active Memory Layer providing:
- LLM-agnostic personal/team memory infrastructure
- Sub-100ms retrieval at scale (1M+ vectors)
- Active intelligence with self-learning capabilities
- Zero-trust, quantum-resistant security architecture
- Full user ownership of data

### 1.3 Success Criteria

| Criterion | Target | Validation Method |
|-----------|--------|-------------------|
| Retrieval latency | <50ms @ 1M vectors | Benchmark suite |
| Security compliance | OWASP LLM Top 10 | Automated scan |
| LLM portability | 3+ providers | Integration tests |
| Learning improvement | 15% relevance gain/month | A/B testing |
| User data ownership | 100% exportable | Export verification |

---

## 2. Functional Requirements

### 2.1 Core Memory Operations

#### FR-001: Vector Storage and Retrieval
**Priority**: P0 (Critical)

The system MUST:
- Store text content with associated vector embeddings
- Support multiple embedding models (OpenAI, Cohere, local)
- Retrieve top-k similar items in <50ms for 1M vectors
- Support hybrid search (vector + keyword + metadata filters)
- Enable batch operations for bulk ingest

**Acceptance Criteria**:
- [ ] Single vector retrieval <50ms @ 1M vectors
- [ ] Batch ingest 10K documents in <30 seconds
- [ ] Hybrid search with metadata filters
- [ ] Embedding model pluggability

#### FR-002: Causal Memory Graphs
**Priority**: P0 (Critical)

The system MUST:
- Track relationships between memory items (A led to B)
- Calculate uplift scores for causal relationships
- Support graph traversal queries
- Enable temporal relationship analysis
- Prune stale relationships automatically

**Acceptance Criteria**:
- [ ] Create causal edges with timestamps and scores
- [ ] Query related items via graph traversal
- [ ] Time-decay scoring for relationship freshness
- [ ] Automatic pruning of low-value edges

#### FR-003: Multi-Source Ingestion
**Priority**: P1 (High)

The system MUST:
- Ingest from local files (text, PDF, markdown)
- Ingest from web sources (URL scraping with robots.txt respect)
- Ingest from API sources (custom connectors)
- Support incremental updates (delta sync)
- Track source provenance for all content

**Acceptance Criteria**:
- [ ] File ingestion for common formats
- [ ] Web ingestion with content extraction
- [ ] Custom API connector framework
- [ ] Delta sync for updated sources
- [ ] Full provenance tracking

### 2.2 Active Intelligence

#### FR-004: Pattern Learning
**Priority**: P0 (Critical)

The system MUST:
- Track user interaction patterns (searches, retrievals, ratings)
- Learn retrieval preferences via reinforcement learning
- Adapt search strategies based on context
- Maintain per-user preference models
- Enable preference export/import

**Acceptance Criteria**:
- [ ] Thompson Sampling for strategy selection
- [ ] Contextual bandit for query adaptation
- [ ] User preference model persistence
- [ ] Measurable relevance improvement over time

#### FR-005: Cognitive State Detection
**Priority**: P2 (Medium)

The system SHOULD:
- Detect user cognitive state from interaction patterns
- Adapt retrieval behavior based on detected state
- Support explicit state switching
- Track state transitions over time

**Acceptance Criteria**:
- [ ] State detection via rule-based classifier
- [ ] Behavior adaptation per state
- [ ] Manual state override capability

#### FR-006: Reflexion Episodes
**Priority**: P1 (High)

The system MUST:
- Store retrieval episodes with outcomes
- Learn from successful/failed retrievals
- Generate retrieval critiques
- Apply learned patterns to future queries

**Acceptance Criteria**:
- [ ] Episode storage with outcome tracking
- [ ] Success/failure classification
- [ ] Pattern extraction from episodes
- [ ] Pattern application to queries

### 2.3 LLM Integration

#### FR-007: Multi-Provider Support
**Priority**: P0 (Critical)

The system MUST:
- Integrate with Claude (Anthropic)
- Integrate with GPT (OpenAI)
- Integrate with Gemini (Google)
- Integrate with local models (Ollama, vLLM)
- Support provider switching without data migration

**Acceptance Criteria**:
- [ ] Unified API abstraction layer
- [ ] Per-provider configuration
- [ ] Hot-swap between providers
- [ ] Fallback chain configuration

#### FR-008: Agentic Workflow Support
**Priority**: P0 (Critical)

The system MUST:
- Support high-frequency retrieval (100+ calls/task)
- Enable agent memory coordination
- Provide transaction semantics for agent writes
- Support multi-agent concurrent access
- Track agent-specific memory namespaces

**Acceptance Criteria**:
- [ ] <50ms retrieval under agentic load
- [ ] Concurrent access without corruption
- [ ] Agent namespace isolation
- [ ] Transaction rollback support

#### FR-009: Context Assembly
**Priority**: P1 (High)

The system MUST:
- Assemble relevant context for LLM queries
- Respect token limits per provider
- Prioritize by relevance and recency
- Support custom assembly strategies

**Acceptance Criteria**:
- [ ] Token-aware context assembly
- [ ] Configurable prioritization
- [ ] Strategy pluggability

### 2.4 Data Portability

#### FR-010: Full Export
**Priority**: P0 (Critical)

The system MUST:
- Export all user data in standard formats (JSON, SQLite)
- Export memory graphs in standard graph formats
- Export learned preferences and models
- Enable complete system migration

**Acceptance Criteria**:
- [ ] One-click full export
- [ ] Standard format compliance
- [ ] Migration validation tooling

#### FR-011: Import Compatibility
**Priority**: P1 (High)

The system MUST:
- Import from competitor formats where possible
- Import from standard knowledge base formats
- Support incremental import
- Validate import integrity

**Acceptance Criteria**:
- [ ] Common format import support
- [ ] Import verification
- [ ] Conflict resolution for duplicates

---

## 3. Non-Functional Requirements

### 3.1 Performance

#### NFR-001: Latency Requirements
| Operation | Target | Maximum |
|-----------|--------|---------|
| Vector search (1K vectors) | <10ms | 50ms |
| Vector search (100K vectors) | <30ms | 100ms |
| Vector search (1M vectors) | <50ms | 200ms |
| Graph traversal (depth 3) | <20ms | 100ms |
| Batch ingest (1K docs) | <3s | 10s |
| Learning update | <100ms | 500ms |

#### NFR-002: Throughput Requirements
| Scenario | Target |
|----------|--------|
| Concurrent queries | 1000+ QPS |
| Concurrent agents | 100+ |
| Concurrent users | 10,000+ |
| Ingestion rate | 100K docs/hour |

#### NFR-003: Resource Constraints
| Resource | Limit |
|----------|-------|
| Memory per 1M vectors | <4GB |
| Storage per 1M vectors | <8GB |
| CPU cores (baseline) | 2-4 |
| GPU (optional) | CUDA 11+ |

### 3.2 Reliability

#### NFR-004: Availability
- **Target**: 99.9% uptime for hosted service
- **Local mode**: Graceful degradation on failure
- **Recovery**: <30 second restart on crash

#### NFR-005: Durability
- **Data durability**: 99.999999999% (11 nines)
- **Write confirmation**: Sync to disk before acknowledgment
- **Backup**: Automated daily with 30-day retention

#### NFR-006: Consistency
- **Read-after-write**: Guaranteed
- **Cross-device sync**: Eventually consistent (<5s)
- **Conflict resolution**: Last-write-wins with history

### 3.3 Security (Detailed in Security Architecture)

#### NFR-007: Authentication
- Multi-factor authentication support
- API key rotation capabilities
- Session management with expiration

#### NFR-008: Authorization
- Role-based access control (RBAC)
- Resource-level permissions
- Namespace isolation for multi-tenant

#### NFR-009: Encryption
- At-rest: AES-256
- In-transit: TLS 1.3
- End-to-end option: Zero-knowledge

#### NFR-010: Quantum Resistance
- Post-quantum key exchange (ML-KEM)
- Hybrid classical/PQ modes
- Migration path for future algorithms

### 3.4 Scalability

#### NFR-011: Horizontal Scaling
- Stateless query handlers
- Sharded vector indices
- Distributed graph storage

#### NFR-012: Vertical Scaling
- Memory-mapped storage
- GPU acceleration support
- SIMD-optimized operations

---

## 4. Constraints

### 4.1 Technical Constraints

| Constraint | Rationale |
|------------|-----------|
| Rust for core | Performance and memory safety requirements |
| SQLite for local | Proven, portable, zero-dependency |
| HNSW for vectors | Best performance/accuracy tradeoff |
| No network for local mode | Privacy requirement |

### 4.2 Business Constraints

| Constraint | Rationale |
|------------|-----------|
| Open source core | Build trust, enable verification |
| Self-hostable | Enterprise requirement |
| No telemetry default | Privacy-first positioning |

### 4.3 Regulatory Constraints

| Constraint | Requirement |
|------------|-------------|
| GDPR | Right to deletion, data portability |
| CCPA | Data disclosure, opt-out |
| SOC 2 | Audit logging, access controls |
| HIPAA | BAA-eligible option required |

---

## 5. Interfaces

### 5.1 User Interfaces

#### CLI Interface
```bash
# Core operations
pmemory search "query text" --top-k 10
pmemory add /path/to/document
pmemory graph show --depth 2

# Configuration
pmemory config set provider claude
pmemory config set latency-target 50ms

# Learning
pmemory feedback <item-id> positive
pmemory stats learning
```

#### REST API
```yaml
# Core endpoints
POST /v1/search
POST /v1/add
GET  /v1/item/{id}
DELETE /v1/item/{id}

# Graph endpoints
GET  /v1/graph/{id}/related
POST /v1/graph/edge

# Learning endpoints
POST /v1/feedback
GET  /v1/stats/learning

# Admin endpoints
GET  /v1/health
POST /v1/export
POST /v1/import
```

#### SDK (Rust, Node.js, Python)
```rust
// Rust
let memory = PMemory::new(config)?;
let results = memory.search("query", SearchOptions::default()).await?;

// Node.js (NAPI)
const memory = new PMemory(config);
const results = await memory.search("query", { topK: 10 });

// Python (PyO3)
memory = PMemory(config)
results = await memory.search("query", top_k=10)
```

### 5.2 External Interfaces

#### LLM Provider Interface
```rust
trait LLMProvider {
    async fn embed(&self, text: &str) -> Result<Vec<f32>>;
    async fn complete(&self, prompt: &str, context: &Context) -> Result<String>;
    fn token_limit(&self) -> usize;
    fn name(&self) -> &str;
}
```

#### Storage Backend Interface
```rust
trait StorageBackend {
    async fn store(&self, item: &MemoryItem) -> Result<ItemId>;
    async fn retrieve(&self, id: &ItemId) -> Result<MemoryItem>;
    async fn search(&self, query: &SearchQuery) -> Result<Vec<SearchResult>>;
    async fn delete(&self, id: &ItemId) -> Result<()>;
}
```

#### Security Provider Interface
```rust
trait SecurityProvider {
    fn encrypt(&self, data: &[u8]) -> Result<Vec<u8>>;
    fn decrypt(&self, data: &[u8]) -> Result<Vec<u8>>;
    fn sign(&self, data: &[u8]) -> Result<Signature>;
    fn verify(&self, data: &[u8], sig: &Signature) -> Result<bool>;
}
```

---

## 6. Use Cases

### UC-001: Personal Knowledge Management

**Actor**: Individual user
**Precondition**: pMemory installed locally
**Flow**:
1. User ingests personal documents
2. User searches for information
3. System returns relevant items with context
4. User provides feedback on relevance
5. System learns and improves

### UC-002: Agentic Research Task

**Actor**: AI agent (via agentic-flow)
**Precondition**: Memory populated, agent authenticated
**Flow**:
1. Agent receives complex research task
2. Agent makes 50-100 memory queries
3. System returns results in <50ms each
4. Agent synthesizes findings
5. Agent stores new knowledge with causal links

### UC-003: Team Knowledge Sharing

**Actor**: Team members
**Precondition**: Shared memory namespace configured
**Flow**:
1. Member A adds knowledge to shared namespace
2. System syncs to team members
3. Member B searches shared knowledge
4. System returns results with attribution
5. Team learning improves from collective usage

### UC-004: LLM Provider Migration

**Actor**: System administrator
**Precondition**: Currently using Provider A
**Flow**:
1. Admin configures Provider B credentials
2. Admin switches active provider
3. System re-embeds using new provider (background)
4. All queries now use Provider B
5. No data migration required

---

## 7. Risks and Mitigations

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Performance target miss | High | Medium | Incremental optimization, GPU fallback |
| Security vulnerability | Critical | Low | Formal verification, audit |
| LLM API changes | Medium | High | Abstraction layer, version pinning |
| Learning effectiveness | Medium | Medium | A/B testing, fallback to static |

### Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Big Tech feature parity | High | High | Differentiate on privacy/openness |
| Adoption barrier | Medium | Medium | Clear migration path, free tier |
| Maintenance burden | Medium | Low | Modular architecture, strong typing |

---

## 8. Glossary

| Term | Definition |
|------|------------|
| Active Memory | Memory layer with intelligence that learns and adapts |
| Causal Graph | Graph structure tracking cause-effect relationships |
| HNSW | Hierarchical Navigable Small World (vector index algorithm) |
| Reflexion | Learning pattern storing episodes with outcomes |
| Thompson Sampling | Probabilistic strategy for exploration/exploitation |
| Zero-Trust | Security model assuming no implicit trust |

---

## 9. Appendices

### A. Reference Materials

- PKM Analysis Documents (epics/pkm-analysis/08-10)
- AIMDS Security Framework (gist reference)
- AgentDB Documentation (agentdb.ruv.io)
- agentic-flow Documentation (github.com/ruvnet/agentic-flow)

### B. Related Documents

- 02-pseudocode.md - Algorithm designs
- 03-architecture.md - System architecture
- 04-security.md - Security architecture
- 05-implementation.md - Implementation roadmap
- 06-technology.md - Technology selection
