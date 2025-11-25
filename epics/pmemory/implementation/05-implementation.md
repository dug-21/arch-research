# pMemory Implementation Roadmap

## SPARC Refinement & Completion Phases

**Document Status**: Active
**Version**: 1.0.0
**Last Updated**: November 2024

---

## 1. Implementation Strategy

### 1.1 Development Philosophy

- **Test-Driven Development (TDD)**: Write tests before implementation
- **Incremental Delivery**: Working software at each milestone
- **Performance-First**: Optimize for latency from day one
- **Security-Integrated**: Security is not bolted on, it's built in

### 1.2 Phase Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      IMPLEMENTATION PHASES                                │
│                                                                          │
│  Phase 0         Phase 1         Phase 2         Phase 3         Phase 4 │
│  Foundation      Core Engine     Intelligence    Integration    Polish   │
│  ─────────────  ─────────────   ─────────────  ─────────────   ──────── │
│  │             │              │              │              │           │
│  │ Project     │ Vector Store │ Learning     │ LLM Router   │ Perf     │
│  │ Setup       │ Search API   │ Service      │ agentic-flow │ Tuning   │
│  │             │              │              │              │           │
│  │ Core Types  │ Graph Store  │ Reflexion    │ SDK Bindings │ Security │
│  │ Security    │ Document     │ Thompson     │ CLI          │ Audit    │
│  │ Foundation  │ Store        │ Sampling     │              │          │
│  │             │              │              │              │           │
│  └─────────────┴──────────────┴──────────────┴──────────────┴───────────│
│                                                                          │
│  Duration (estimate):                                                    │
│  2 weeks        4 weeks         3 weeks         3 weeks        2 weeks  │
│                                                                          │
│  Total: ~14 weeks to MVP                                                 │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase 0: Foundation (Weeks 1-2)

### 2.1 Objectives

- Project scaffolding and toolchain setup
- Core type definitions
- Security foundation
- CI/CD pipeline

### 2.2 Deliverables

#### D0.1: Project Structure

```
pmemory/
├── Cargo.toml                 # Workspace configuration
├── crates/
│   ├── pmemory-core/         # Core types and traits
│   ├── pmemory-storage/      # Storage implementations
│   ├── pmemory-search/       # Search algorithms
│   ├── pmemory-security/     # Security layer
│   ├── pmemory-learning/     # Learning service
│   ├── pmemory-llm/          # LLM integration
│   └── pmemory-api/          # API server
├── bindings/
│   ├── pmemory-napi/         # Node.js bindings
│   └── pmemory-pyo3/         # Python bindings
├── cli/                      # CLI tool
├── tests/
│   ├── integration/          # Integration tests
│   └── benchmarks/           # Performance benchmarks
└── docs/                     # Documentation
```

#### D0.2: Core Types

```rust
// pmemory-core/src/types.rs

/// Unique identifier for memory items
#[derive(Clone, Copy, PartialEq, Eq, Hash)]
pub struct ItemId(pub Uuid);

/// Memory item - the fundamental unit of storage
#[derive(Clone)]
pub struct MemoryItem {
    pub id: ItemId,
    pub content: String,
    pub embedding: Option<Embedding>,
    pub metadata: Metadata,
    pub source: Source,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub access_count: u64,
}

/// Dense vector embedding
pub struct Embedding {
    pub vector: Vec<f32>,
    pub model: String,
    pub dimension: usize,
}

/// Causal edge in the memory graph
pub struct CausalEdge {
    pub source_id: ItemId,
    pub target_id: ItemId,
    pub relationship: Relationship,
    pub uplift_score: f32,
    pub interaction_count: u64,
    pub created_at: DateTime<Utc>,
}

/// Search query specification
pub struct SearchQuery {
    pub text: String,
    pub filters: Vec<Filter>,
    pub top_k: usize,
    pub strategy: SearchStrategy,
    pub include_graph: bool,
}

/// Search result with score
pub struct SearchResult {
    pub item: MemoryItem,
    pub score: f32,
    pub strategy_used: SearchStrategy,
    pub graph_path: Option<Vec<ItemId>>,
}
```

#### D0.3: Security Foundation

```rust
// pmemory-security/src/lib.rs

/// Security context for requests
pub struct SecurityContext {
    pub identity: Identity,
    pub permissions: Permissions,
    pub session: Option<Session>,
    pub request_id: String,
}

/// Identity types
pub enum Identity {
    User(UserId),
    Agent(AgentId),
    Service(ServiceId),
    Anonymous,
}

/// Encryption service trait
pub trait EncryptionService: Send + Sync {
    fn encrypt(&self, data: &[u8]) -> Result<EncryptedData>;
    fn decrypt(&self, data: &EncryptedData) -> Result<Vec<u8>>;
}

/// Authentication service trait
pub trait AuthService: Send + Sync {
    async fn validate_token(&self, token: &str) -> Result<SecurityContext>;
    async fn create_token(&self, identity: &Identity) -> Result<String>;
}
```

### 2.3 Tasks

| Task | Description | Effort | Dependencies |
|------|-------------|--------|--------------|
| T0.1 | Initialize Cargo workspace | 2h | - |
| T0.2 | Configure CI/CD (GitHub Actions) | 4h | T0.1 |
| T0.3 | Define core types | 8h | T0.1 |
| T0.4 | Implement basic error types | 4h | T0.3 |
| T0.5 | Setup encryption primitives | 8h | T0.3 |
| T0.6 | Setup JWT validation | 8h | T0.5 |
| T0.7 | Write foundation tests | 8h | T0.3-T0.6 |
| T0.8 | Setup benchmarking harness | 4h | T0.1 |

### 2.4 Success Criteria

- [ ] All crates compile without warnings
- [ ] Core types have complete documentation
- [ ] Encryption round-trip tests pass
- [ ] JWT validation tests pass
- [ ] CI pipeline green on all commits

---

## 3. Phase 1: Core Engine (Weeks 3-6)

### 3.1 Objectives

- Vector storage and HNSW search
- Document storage with SQLite
- Graph storage for causal edges
- Basic REST API

### 3.2 Deliverables

#### D1.1: Vector Store

```rust
// pmemory-storage/src/vector.rs

/// HNSW-based vector store
pub struct VectorStore {
    index: HnswIndex,
    config: VectorConfig,
}

pub struct VectorConfig {
    pub dimension: usize,
    pub m: usize,                // Max connections per node (16)
    pub ef_construction: usize,  // Build-time search width (200)
    pub ef_search: usize,        // Query-time search width (100)
    pub distance: DistanceMetric,
}

impl VectorStore {
    /// Create new vector store
    pub fn new(config: VectorConfig) -> Result<Self>;

    /// Insert vector with ID
    pub fn insert(&mut self, id: ItemId, vector: &[f32]) -> Result<()>;

    /// Search for k nearest neighbors
    pub fn search(&self, query: &[f32], k: usize) -> Result<Vec<(ItemId, f32)>>;

    /// Delete vector by ID
    pub fn delete(&mut self, id: ItemId) -> Result<()>;

    /// Persist index to disk
    pub fn save(&self, path: &Path) -> Result<()>;

    /// Load index from disk
    pub fn load(path: &Path) -> Result<Self>;
}
```

#### D1.2: Document Store

```rust
// pmemory-storage/src/document.rs

/// SQLite-backed document store
pub struct DocumentStore {
    pool: SqlitePool,
}

impl DocumentStore {
    /// Store a memory item
    pub async fn store(&self, item: &MemoryItem) -> Result<ItemId>;

    /// Retrieve by ID
    pub async fn get(&self, id: ItemId) -> Result<Option<MemoryItem>>;

    /// Update existing item
    pub async fn update(&self, item: &MemoryItem) -> Result<()>;

    /// Delete item
    pub async fn delete(&self, id: ItemId) -> Result<()>;

    /// Query with filters
    pub async fn query(&self, filters: &[Filter]) -> Result<Vec<MemoryItem>>;

    /// Full-text search (BM25)
    pub async fn text_search(&self, query: &str, limit: usize) -> Result<Vec<(MemoryItem, f32)>>;
}
```

#### D1.3: Graph Store

```rust
// pmemory-storage/src/graph.rs

/// Causal graph store
pub struct GraphStore {
    pool: SqlitePool,
}

impl GraphStore {
    /// Add or update causal edge
    pub async fn add_edge(&self, edge: &CausalEdge) -> Result<()>;

    /// Get outgoing edges from node
    pub async fn edges_from(&self, id: ItemId) -> Result<Vec<CausalEdge>>;

    /// Get incoming edges to node
    pub async fn edges_to(&self, id: ItemId) -> Result<Vec<CausalEdge>>;

    /// Traverse graph with depth limit
    pub async fn traverse(
        &self,
        start: ItemId,
        max_depth: usize,
        min_score: f32,
    ) -> Result<Vec<(ItemId, f32, usize)>>;

    /// Prune low-value edges
    pub async fn prune(&self, threshold: f32) -> Result<usize>;
}
```

#### D1.4: Search Service

```rust
// pmemory-search/src/service.rs

pub struct SearchService {
    vector_store: Arc<VectorStore>,
    document_store: Arc<DocumentStore>,
    graph_store: Arc<GraphStore>,
}

impl SearchService {
    /// Execute search with strategy selection
    pub async fn search(&self, query: SearchQuery) -> Result<Vec<SearchResult>>;

    /// Semantic search only
    pub async fn semantic_search(&self, embedding: &[f32], k: usize) -> Result<Vec<SearchResult>>;

    /// Keyword search only
    pub async fn keyword_search(&self, text: &str, k: usize) -> Result<Vec<SearchResult>>;

    /// Hybrid search with fusion
    pub async fn hybrid_search(
        &self,
        text: &str,
        embedding: &[f32],
        k: usize,
        alpha: f32,
    ) -> Result<Vec<SearchResult>>;

    /// Graph-based search
    pub async fn graph_search(
        &self,
        start: ItemId,
        depth: usize,
        k: usize,
    ) -> Result<Vec<SearchResult>>;
}
```

### 3.3 Tasks

| Task | Description | Effort | Dependencies |
|------|-------------|--------|--------------|
| T1.1 | Implement HNSW index | 16h | T0.3 |
| T1.2 | Add HNSW serialization | 8h | T1.1 |
| T1.3 | Implement SQLite document store | 12h | T0.3 |
| T1.4 | Add FTS5 full-text search | 8h | T1.3 |
| T1.5 | Implement graph store | 12h | T1.3 |
| T1.6 | Implement search service | 16h | T1.1-T1.5 |
| T1.7 | Implement hybrid fusion | 8h | T1.6 |
| T1.8 | Create REST API endpoints | 16h | T1.6 |
| T1.9 | Add request validation | 8h | T1.8, T0.6 |
| T1.10 | Performance benchmarks | 12h | T1.1-T1.7 |
| T1.11 | Integration tests | 16h | T1.1-T1.8 |

### 3.4 Performance Targets

| Operation | Target p50 | Target p99 | Test Dataset |
|-----------|------------|------------|--------------|
| Vector insert | <1ms | <5ms | 10K vectors |
| Vector search (10K) | <5ms | <10ms | 10K vectors |
| Vector search (100K) | <20ms | <50ms | 100K vectors |
| Document store | <2ms | <10ms | 4KB doc |
| Document retrieve | <1ms | <5ms | By ID |
| Graph traverse (d=3) | <10ms | <30ms | 10K nodes |

### 3.5 Success Criteria

- [ ] HNSW recall@10 >= 95% vs brute force
- [ ] All performance targets met
- [ ] REST API functional tests pass
- [ ] Data persistence across restarts
- [ ] No memory leaks under load

---

## 4. Phase 2: Intelligence (Weeks 7-9)

### 4.1 Objectives

- Learning service with Thompson Sampling
- Reflexion episode storage
- User preference modeling
- Cognitive state detection (basic)

### 4.2 Deliverables

#### D2.1: Learning Service

```rust
// pmemory-learning/src/service.rs

pub struct LearningService {
    episode_store: EpisodeStore,
    preference_store: PreferenceStore,
    strategy_optimizer: StrategyOptimizer,
}

impl LearningService {
    /// Record a retrieval episode
    pub async fn record_episode(&self, episode: RetrexionEpisode) -> Result<()>;

    /// Get optimal strategy for context
    pub async fn select_strategy(&self, context: &SearchContext) -> SearchStrategy;

    /// Update strategy based on feedback
    pub async fn update_from_feedback(
        &self,
        strategy: SearchStrategy,
        positive: bool,
    ) -> Result<()>;

    /// Get user preferences
    pub async fn get_preferences(&self, user_id: UserId) -> Result<UserPreferences>;

    /// Learn from historical episodes
    pub async fn batch_learn(&self, user_id: UserId, lookback_days: u32) -> Result<()>;
}
```

#### D2.2: Strategy Optimizer

```rust
// pmemory-learning/src/optimizer.rs

/// Thompson Sampling optimizer
pub struct StrategyOptimizer {
    priors: HashMap<SearchStrategy, BetaDist>,
}

impl StrategyOptimizer {
    /// Sample from posterior to select strategy
    pub fn select(&self, context: &SearchContext) -> SearchStrategy;

    /// Update posterior with observation
    pub fn update(&mut self, strategy: SearchStrategy, success: bool);

    /// Apply decay to prevent stale priors
    pub fn decay(&mut self, factor: f32);

    /// Export priors for persistence
    pub fn export(&self) -> HashMap<SearchStrategy, (f32, f32)>;

    /// Import priors from storage
    pub fn import(&mut self, priors: HashMap<SearchStrategy, (f32, f32)>);
}
```

#### D2.3: Reflexion Storage

```rust
// pmemory-learning/src/reflexion.rs

pub struct EpisodeStore {
    pool: SqlitePool,
}

impl EpisodeStore {
    /// Store episode
    pub async fn store(&self, episode: &ReflexionEpisode) -> Result<EpisodeId>;

    /// Get episodes for user
    pub async fn get_user_episodes(
        &self,
        user_id: UserId,
        limit: usize,
        since: Option<DateTime<Utc>>,
    ) -> Result<Vec<ReflexionEpisode>>;

    /// Aggregate outcomes by strategy
    pub async fn strategy_stats(
        &self,
        user_id: UserId,
        since: DateTime<Utc>,
    ) -> Result<HashMap<SearchStrategy, StrategyStats>>;
}
```

### 4.3 Tasks

| Task | Description | Effort | Dependencies |
|------|-------------|--------|--------------|
| T2.1 | Implement Thompson Sampling | 8h | T0.3 |
| T2.2 | Implement episode storage | 8h | T1.3 |
| T2.3 | Implement preference storage | 6h | T1.3 |
| T2.4 | Create learning service | 12h | T2.1-T2.3 |
| T2.5 | Integrate with search | 8h | T2.4, T1.6 |
| T2.6 | Implement batch learning | 8h | T2.4 |
| T2.7 | Add causal edge updates | 6h | T2.5, T1.5 |
| T2.8 | Learning API endpoints | 8h | T2.4 |
| T2.9 | Unit tests for learning | 12h | T2.1-T2.7 |
| T2.10 | A/B testing framework | 8h | T2.5 |

### 4.4 Success Criteria

- [ ] Thompson Sampling converges to best strategy in tests
- [ ] Episode storage handles 100K+ episodes
- [ ] Learning improves relevance by >10% over baseline
- [ ] Strategy selection <1ms
- [ ] Causal graph updates correctly from feedback

---

## 5. Phase 3: Integration (Weeks 10-12)

### 5.1 Objectives

- LLM router with multi-provider support
- agentic-flow integration
- SDK bindings (Node.js, Python)
- CLI tool

### 5.2 Deliverables

#### D3.1: LLM Router

```rust
// pmemory-llm/src/router.rs

pub struct LlmRouter {
    providers: HashMap<String, Box<dyn LlmProvider>>,
    config: RouterConfig,
    cache: EmbeddingCache,
}

impl LlmRouter {
    /// Generate embedding
    pub async fn embed(&self, text: &str) -> Result<Embedding>;

    /// Batch embed
    pub async fn batch_embed(&self, texts: &[String]) -> Result<Vec<Embedding>>;

    /// Complete prompt with context
    pub async fn complete(
        &self,
        prompt: &str,
        context: &AssembledContext,
    ) -> Result<String>;

    /// Get best provider for request
    fn route(&self, request: &LlmRequest) -> Result<&dyn LlmProvider>;
}

// Provider implementations
pub struct ClaudeProvider { /* ... */ }
pub struct OpenAIProvider { /* ... */ }
pub struct GeminiProvider { /* ... */ }
pub struct OllamaProvider { /* ... */ }
```

#### D3.2: SDK Bindings

```typescript
// Node.js binding (pmemory-napi)
import { PMemory } from '@pmemory/core';

const memory = new PMemory({
  dataPath: './data',
  provider: 'claude',
});

// Search
const results = await memory.search('query', { topK: 10 });

// Add content
const id = await memory.add({
  content: 'New knowledge',
  metadata: { source: 'manual' },
});

// Feedback
await memory.feedback(id, 'positive');
```

```python
# Python binding (pmemory-pyo3)
from pmemory import PMemory

memory = PMemory(
    data_path="./data",
    provider="claude",
)

# Search
results = await memory.search("query", top_k=10)

# Add content
item_id = await memory.add(
    content="New knowledge",
    metadata={"source": "manual"},
)

# Feedback
await memory.feedback(item_id, positive=True)
```

#### D3.3: CLI Tool

```bash
# Search
pmemory search "query text" --top-k 10 --strategy hybrid

# Add content
pmemory add /path/to/file.md
pmemory add --url https://example.com/article

# Graph operations
pmemory graph show <item-id> --depth 2
pmemory graph stats

# Configuration
pmemory config set provider claude
pmemory config set api-key $ANTHROPIC_API_KEY

# Learning
pmemory feedback <item-id> positive
pmemory stats learning

# Export/Import
pmemory export ./backup.json
pmemory import ./backup.json
```

### 5.3 Tasks

| Task | Description | Effort | Dependencies |
|------|-------------|--------|--------------|
| T3.1 | Implement LLM provider trait | 8h | T0.3 |
| T3.2 | Implement Claude provider | 8h | T3.1 |
| T3.3 | Implement OpenAI provider | 6h | T3.1 |
| T3.4 | Implement Gemini provider | 6h | T3.1 |
| T3.5 | Implement Ollama provider | 6h | T3.1 |
| T3.6 | Build LLM router | 12h | T3.2-T3.5 |
| T3.7 | Implement embedding cache | 8h | T3.6 |
| T3.8 | Node.js NAPI bindings | 16h | All Phase 1-2 |
| T3.9 | Python PyO3 bindings | 16h | All Phase 1-2 |
| T3.10 | CLI implementation | 12h | All Phase 1-2 |
| T3.11 | Integration tests | 16h | T3.6-T3.10 |

### 5.4 Success Criteria

- [ ] All 4 LLM providers functional
- [ ] Provider switching without data migration
- [ ] Node.js SDK passes all tests
- [ ] Python SDK passes all tests
- [ ] CLI covers all core operations
- [ ] agentic-flow demo works end-to-end

---

## 6. Phase 4: Polish (Weeks 13-14)

### 6.1 Objectives

- Performance optimization
- Security hardening
- Documentation completion
- Release preparation

### 6.2 Tasks

| Task | Description | Effort | Dependencies |
|------|-------------|--------|--------------|
| T4.1 | Performance profiling | 8h | All prior |
| T4.2 | Optimize hot paths | 16h | T4.1 |
| T4.3 | Security audit | 12h | All prior |
| T4.4 | Fix security findings | 16h | T4.3 |
| T4.5 | Threat detection tuning | 8h | T4.3 |
| T4.6 | API documentation | 8h | All prior |
| T4.7 | User guide | 8h | All prior |
| T4.8 | Architecture docs | 4h | All prior |
| T4.9 | Release packaging | 8h | All prior |
| T4.10 | End-to-end demo | 8h | All prior |

### 6.3 Release Checklist

```
Code Quality:
[ ] All tests pass
[ ] No clippy warnings
[ ] cargo audit clean
[ ] Fuzz testing complete

Performance:
[ ] All latency targets met
[ ] Memory usage within bounds
[ ] No memory leaks
[ ] Benchmark results documented

Security:
[ ] Security audit complete
[ ] Findings remediated
[ ] Penetration test passed
[ ] Key rotation tested

Documentation:
[ ] API reference complete
[ ] User guide complete
[ ] Architecture documented
[ ] CHANGELOG updated

Release:
[ ] Version tagged
[ ] Binaries built for all platforms
[ ] npm package published
[ ] PyPI package published
[ ] GitHub release created
```

---

## 7. Validation Plan

### 7.1 Test Strategy

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         TEST PYRAMID                                      │
│                                                                          │
│                              ┌──────┐                                    │
│                              │ E2E  │  (~10 tests)                       │
│                             /│      │\                                   │
│                            / └──────┘ \                                  │
│                           /            \                                 │
│                          /  ┌────────┐  \                                │
│                         /   │ Integ. │   \  (~100 tests)                 │
│                        /   /│        │\   \                              │
│                       /   / └────────┘ \   \                             │
│                      /   /              \   \                            │
│                     /   /    ┌──────┐    \   \                           │
│                    /   /     │ Unit │     \   \  (~1000 tests)           │
│                   /   /      │      │      \   \                         │
│                  /   /       └──────┘       \   \                        │
│                 /___/________________________\___\                       │
│                                                                          │
│  Unit Tests:        Fast, isolated, comprehensive                        │
│  Integration Tests: Cross-component, database, API                       │
│  E2E Tests:         Full user scenarios, performance                     │
└──────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Benchmark Suite

```rust
// benchmarks/search.rs

#[bench]
fn bench_hnsw_search_10k(b: &mut Bencher) {
    let store = setup_vector_store(10_000);
    let query = random_vector(384);

    b.iter(|| {
        store.search(&query, 10).unwrap()
    });
}

#[bench]
fn bench_hnsw_search_100k(b: &mut Bencher) { /* ... */ }

#[bench]
fn bench_hnsw_search_1m(b: &mut Bencher) { /* ... */ }

#[bench]
fn bench_hybrid_search(b: &mut Bencher) { /* ... */ }

#[bench]
fn bench_graph_traverse(b: &mut Bencher) { /* ... */ }
```

### 7.3 Validation Demo

```
DEMO: Agent Swarm Research Task
================================

Setup:
- 100K memory items from knowledge base
- 5 parallel research agents via agentic-flow
- Mixed Claude/GPT providers

Task: "Research quantum computing implications for cryptography"

Execution:
1. Each agent makes ~100 memory queries
2. Total queries: ~500
3. Target completion: <30 seconds
4. All data stays local

Success Metrics:
- [ ] Total time < 30 seconds
- [ ] Average query latency < 50ms
- [ ] No provider errors
- [ ] Relevant results (human evaluation)
- [ ] Learning improves subsequent runs
```

---

## 8. Risk Mitigation

### 8.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| HNSW performance miss | High | Medium | Early benchmarking, GPU fallback |
| LLM API changes | Medium | High | Abstraction layer, version pinning |
| Memory usage at scale | High | Medium | Streaming, memory-mapped files |
| Cross-platform issues | Medium | Medium | CI on all platforms |

### 8.2 Contingency Plans

**If HNSW performance is insufficient**:
1. First: Optimize parameters (M, ef)
2. Second: Enable GPU acceleration
3. Third: Use approximate pre-filtering

**If LLM provider fails**:
1. Automatic fallback to secondary provider
2. Degrade to local embedding model
3. Cache embeddings aggressively

---

## 9. Resource Requirements

### 9.1 Development Team

| Role | FTE | Responsibilities |
|------|-----|------------------|
| Rust Engineer | 2 | Core engine, performance |
| Security Engineer | 0.5 | Security layer, audit |
| Full-Stack Developer | 1 | API, SDK bindings |
| DevOps Engineer | 0.5 | CI/CD, release |

### 9.2 Infrastructure

| Resource | Development | Staging | Production |
|----------|-------------|---------|------------|
| CPU | 4 cores | 8 cores | Scalable |
| RAM | 16 GB | 32 GB | Scalable |
| Storage | 100 GB SSD | 500 GB SSD | Scalable |
| GPU | Optional | 1x A10 | As needed |

---

## 10. Document Cross-References

- **Specification**: `spec/01-specification.md`
- **Pseudocode**: `pseudocode/02-pseudocode.md`
- **Architecture**: `arch/03-architecture.md`
- **Security**: `security/04-security.md`
- **Technology**: `implementation/06-technology.md`
