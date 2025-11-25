# pMemory SPARC Architecture

## Phase 3: Architecture

**Document Status**: Active
**Version**: 1.0.0
**Last Updated**: November 2024

---

## 1. Architecture Overview

### 1.1 System Context

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL ACTORS                                 │
├─────────────────┬─────────────────┬─────────────────┬───────────────────────┤
│   Human Users   │   AI Agents     │   LLM Providers │   External Systems    │
│   (CLI/API)     │   (agentic-flow)│   (Claude/GPT)  │   (Data Sources)      │
└────────┬────────┴────────┬────────┴────────┬────────┴───────────┬───────────┘
         │                 │                 │                     │
         ▼                 ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           pMemory Active Memory Layer                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Security Perimeter                              │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │  │
│  │  │ Auth/AuthZ  │ │ Threat Det. │ │ Encryption  │ │ Audit Logging   │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│  ┌───────────────────────────────────▼───────────────────────────────────┐  │
│  │                          API Gateway Layer                             │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │  │
│  │  │ REST API    │ │ gRPC API    │ │ SDK Bindings│ │ WebSocket       │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│  ┌───────────────────────────────────▼───────────────────────────────────┐  │
│  │                         Core Services Layer                            │  │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────────┐  │  │
│  │  │  Search   │ │  Ingest   │ │  Graph    │ │  Learning │ │  LLM    │  │  │
│  │  │  Service  │ │  Service  │ │  Service  │ │  Service  │ │  Router │  │  │
│  │  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └────┬────┘  │  │
│  └────────┼─────────────┼─────────────┼─────────────┼────────────┼───────┘  │
│           │             │             │             │            │          │
│  ┌────────▼─────────────▼─────────────▼─────────────▼────────────▼───────┐  │
│  │                        Storage Abstraction Layer                       │  │
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐                │  │
│  │  │ Vector Store  │ │ Document Store│ │ Graph Store   │                │  │
│  │  │ (HNSW Index)  │ │ (Content/Meta)│ │ (Causal Edges)│                │  │
│  │  └───────┬───────┘ └───────┬───────┘ └───────┬───────┘                │  │
│  └──────────┼─────────────────┼─────────────────┼────────────────────────┘  │
│             │                 │                 │                            │
│  ┌──────────▼─────────────────▼─────────────────▼────────────────────────┐  │
│  │                         Physical Storage Layer                         │  │
│  │  ┌───────────────────────────────────────────────────────────────┐    │  │
│  │  │  SQLite (Local)  │  AgentDB (Distributed)  │  Sync Layer      │    │  │
│  │  └───────────────────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Deployment Modes

| Mode | Description | Storage | Network | Use Case |
|------|-------------|---------|---------|----------|
| **Local** | Single-user, device-bound | SQLite | None | Privacy-first personal |
| **Synced** | Multi-device, user-owned | SQLite + Sync | P2P/QUIC | Personal across devices |
| **Team** | Multi-user, shared namespace | AgentDB | Internal | Team collaboration |
| **Enterprise** | Multi-tenant, managed | AgentDB Cluster | Mesh | Organization-wide |

---

## 2. Component Architecture

### 2.1 Security Perimeter

The outermost layer enforcing zero-trust principles.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Security Perimeter                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Request Pipeline                        │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │   │
│  │  │ TLS      │→ │ Rate     │→ │ Auth     │→ │ Threat  │  │   │
│  │  │ Termination  │ Limiter  │  │ Validator│  │ Detect  │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────┘  │   │
│  │        │            │             │             │        │   │
│  │        ▼            ▼             ▼             ▼        │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │              Security Context                    │    │   │
│  │  │  - Identity (user/agent/service)                 │    │   │
│  │  │  - Permissions (RBAC + ABAC)                     │    │   │
│  │  │  - Session state                                 │    │   │
│  │  │  - Audit trail reference                         │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Cryptographic Services                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │   │
│  │  │ Key Mgmt   │  │ Encryption │  │ Post-Quantum       │ │   │
│  │  │ (HSM/KMS)  │  │ Engine     │  │ (ML-KEM-768)       │ │   │
│  │  └────────────┘  └────────────┘  └────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Key Components**:

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| TLS Termination | rustls | TLS 1.3, certificate validation |
| Rate Limiter | Custom (token bucket) | Request throttling |
| Auth Validator | JWT (RS256/Ed25519) | Token validation |
| Threat Detector | Pattern + ML | Injection detection |
| Key Management | age/sodiumoxide | Key lifecycle |
| Encryption Engine | AES-256-GCM | At-rest encryption |
| Post-Quantum | ml-kem crate | PQ key exchange |

### 2.2 API Gateway Layer

```
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                          │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │    REST API     │  │    gRPC API     │  │   WebSocket     │ │
│  │   (axum/tower)  │  │    (tonic)      │  │   (tokio-ws)    │ │
│  │                 │  │                 │  │                 │ │
│  │  /v1/search     │  │  Search.Query   │  │  Real-time      │ │
│  │  /v1/add        │  │  Ingest.Add     │  │  subscriptions  │ │
│  │  /v1/graph      │  │  Graph.Traverse │  │                 │ │
│  │  /v1/feedback   │  │  Learn.Feedback │  │                 │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │          │
│  ┌────────▼────────────────────▼────────────────────▼────────┐ │
│  │                   Request Router                           │ │
│  │  - Version routing                                         │ │
│  │  - Request transformation                                  │ │
│  │  - Response formatting                                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   SDK Bindings                             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │ Rust Native  │  │ Node.js      │  │ Python           │ │ │
│  │  │              │  │ (NAPI-RS)    │  │ (PyO3)           │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**API Design Principles**:
- RESTful for CRUD operations
- gRPC for high-frequency agent calls
- WebSocket for real-time updates
- Native bindings for performance-critical paths

### 2.3 Core Services Layer

#### 2.3.1 Search Service

```
┌─────────────────────────────────────────────────────────────────┐
│                       Search Service                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Query Processor                         │   │
│  │  - Query parsing and normalization                       │   │
│  │  - Filter extraction                                     │   │
│  │  - Strategy selection (Thompson Sampling)                │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │                 Strategy Executor                        │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │  Semantic   │  │  Keyword    │  │  Graph-based    │  │   │
│  │  │  (HNSW)     │  │  (BM25)     │  │  (Causal)       │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘  │   │
│  │         └─────────────┬──┴───────────────────┘          │   │
│  │                       ▼                                  │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │           Result Fusion (RRF)                      │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Result Processor                         │   │
│  │  - Diversity enforcement                                 │   │
│  │  - Score normalization                                   │   │
│  │  - Metadata enrichment                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Performance Targets**:
| Operation | 1K vectors | 100K vectors | 1M vectors |
|-----------|------------|--------------|------------|
| HNSW search | <5ms | <20ms | <50ms |
| BM25 search | <3ms | <15ms | <40ms |
| Hybrid fusion | <2ms | <5ms | <10ms |
| Total p99 | <15ms | <50ms | <120ms |

#### 2.3.2 Ingest Service

```
┌─────────────────────────────────────────────────────────────────┐
│                       Ingest Service                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Source Handlers                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │   │
│  │  │  File    │  │  URL     │  │  API     │  │  Stream │  │   │
│  │  │  Handler │  │  Handler │  │  Handler │  │  Handler│  │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘  │   │
│  │       └──────────┬──┴──────────┬──┴─────────────┘       │   │
│  └──────────────────┼─────────────┼────────────────────────┘   │
│                     ▼             ▼                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Processing Pipeline                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │   │
│  │  │ Extract  │→ │ Chunk    │→ │ Embed    │→ │ Store   │  │   │
│  │  │          │  │          │  │ (Batch)  │  │         │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Duplicate Detection                      │   │
│  │  - Content hash check (exact)                            │   │
│  │  - Embedding similarity check (near-duplicate)           │   │
│  │  - Merge strategy for duplicates                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Chunking Strategy**:
- Semantic chunking (paragraph boundaries)
- Overlap for context preservation (10-15%)
- Maximum chunk size: 512 tokens
- Metadata inheritance from parent

#### 2.3.3 Graph Service

```
┌─────────────────────────────────────────────────────────────────┐
│                        Graph Service                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Graph Operations                       │   │
│  │  - Create/update causal edges                            │   │
│  │  - Traverse with depth/score limits                      │   │
│  │  - Calculate path scores                                 │   │
│  │  - Prune low-value edges                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Edge Scoring Model                      │   │
│  │                                                          │   │
│  │  score = base_uplift × decay(age) × log(interactions+1) │   │
│  │                                                          │   │
│  │  Decay function: exp(-λ × age_days)                      │   │
│  │  λ (decay rate): 0.01 (30-day half-life)                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Graph Storage                          │   │
│  │  - Adjacency list representation                         │   │
│  │  - Indexed by source node                                │   │
│  │  - Secondary index by target for reverse lookups         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.3.4 Learning Service

```
┌─────────────────────────────────────────────────────────────────┐
│                      Learning Service                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Episode Storage                         │   │
│  │  - Query + results + feedback                            │   │
│  │  - Timestamped for temporal analysis                     │   │
│  │  - Indexed by user/session                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Strategy Optimization                       │   │
│  │                                                          │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │          Thompson Sampling Engine                  │  │   │
│  │  │  - Per-user Beta priors for each strategy          │  │   │
│  │  │  - Continuous Bayesian updates                     │  │   │
│  │  │  - Decay to prevent prior ossification             │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  │                                                          │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │          Contextual Bandits                        │  │   │
│  │  │  - Feature extraction from context                 │  │   │
│  │  │  - LinUCB for strategy selection                   │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Preference Model                            │   │
│  │  - Topic weights                                         │   │
│  │  - Recency bias                                          │   │
│  │  - Diversity preference                                  │   │
│  │  - Source trust scores                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.3.5 LLM Router

```
┌─────────────────────────────────────────────────────────────────┐
│                        LLM Router                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Provider Registry                        │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────────┐  │   │
│  │  │ Claude  │ │ GPT-4   │ │ Gemini  │ │ Local (Ollama)│  │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └───────┬───────┘  │   │
│  │       └───────────┼──────────┼───────────────┘          │   │
│  │                   ▼          ▼                           │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │           Unified Provider Interface               │  │   │
│  │  │  - embed(text) -> Vec<f32>                         │  │   │
│  │  │  - complete(prompt, context) -> String             │  │   │
│  │  │  - token_count(text) -> usize                      │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Routing Engine                          │   │
│  │  - Cost optimization                                     │   │
│  │  - Latency optimization                                  │   │
│  │  - Privacy routing (local preference)                    │   │
│  │  - Fallback chains                                       │   │
│  │  - Health checking                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Embedding Cache                          │   │
│  │  - LRU cache with TTL                                    │   │
│  │  - Per-provider model versioning                         │   │
│  │  - Cache invalidation on model change                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Storage Abstraction Layer

```
┌─────────────────────────────────────────────────────────────────┐
│                  Storage Abstraction Layer                      │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Storage Trait                           │ │
│  │                                                            │ │
│  │  trait VectorStore {                                       │ │
│  │    fn insert(&mut self, id: Id, vec: Vec<f32>);           │ │
│  │    fn search(&self, query: Vec<f32>, k: usize) -> Results;│ │
│  │    fn delete(&mut self, id: Id);                          │ │
│  │  }                                                         │ │
│  │                                                            │ │
│  │  trait DocumentStore {                                     │ │
│  │    fn store(&mut self, doc: Document) -> Id;              │ │
│  │    fn get(&self, id: Id) -> Option<Document>;             │ │
│  │    fn update(&mut self, id: Id, doc: Document);           │ │
│  │    fn query(&self, filter: Filter) -> Vec<Document>;      │ │
│  │  }                                                         │ │
│  │                                                            │ │
│  │  trait GraphStore {                                        │ │
│  │    fn add_edge(&mut self, edge: Edge);                    │ │
│  │    fn get_edges(&self, node: Id) -> Vec<Edge>;            │ │
│  │    fn traverse(&self, start: Id, opts: TraverseOpts);     │ │
│  │  }                                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │               Backend Implementations                      │ │
│  │  ┌─────────────────┐  ┌─────────────────────────────────┐ │ │
│  │  │  SQLite Backend │  │  AgentDB Backend (Distributed)  │ │ │
│  │  │  - Local files  │  │  - Cluster deployment           │ │ │
│  │  │  - WAL mode     │  │  - Sharding                     │ │ │
│  │  │  - FTS5 for BM25│  │  - Replication                  │ │ │
│  │  │  - Custom HNSW  │  │  - Native HNSW                  │ │ │
│  │  └─────────────────┘  └─────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Sync Layer                              │ │
│  │  - CRDT-based conflict resolution                         │ │
│  │  - QUIC transport for low-latency sync                    │ │
│  │  - Delta sync for efficiency                              │ │
│  │  - End-to-end encrypted sync option                       │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Architecture

### 3.1 Data Model

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Data Model                                    │
│                                                                       │
│  ┌─────────────────┐       ┌─────────────────┐                       │
│  │   MemoryItem    │       │   CausalEdge    │                       │
│  │─────────────────│       │─────────────────│                       │
│  │ id: UUID        │◀──────│ source_id: UUID │                       │
│  │ content: Text   │       │ target_id: UUID │──────▶MemoryItem      │
│  │ embedding: Vec  │       │ relationship    │                       │
│  │ metadata: JSON  │       │ uplift_score    │                       │
│  │ source: Source  │       │ interactions    │                       │
│  │ created_at      │       │ created_at      │                       │
│  │ updated_at      │       └─────────────────┘                       │
│  │ access_count    │                                                  │
│  └────────┬────────┘       ┌─────────────────┐                       │
│           │                │ ReflexionEpisode│                       │
│           │                │─────────────────│                       │
│           │                │ query_id        │                       │
│           ▼                │ result_ids: []  │                       │
│  ┌─────────────────┐       │ feedback        │                       │
│  │     Source      │       │ outcome         │                       │
│  │─────────────────│       │ timestamp       │                       │
│  │ uri: String     │       └─────────────────┘                       │
│  │ type: Enum      │                                                  │
│  │ hash: String    │       ┌─────────────────┐                       │
│  │ captured_at     │       │ UserPreferences │                       │
│  └─────────────────┘       │─────────────────│                       │
│                            │ user_id: UUID   │                       │
│                            │ strategy_priors │                       │
│                            │ topic_weights   │                       │
│                            │ settings: JSON  │                       │
│                            └─────────────────┘                       │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 Index Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Index Architecture                               │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    HNSW Vector Index                            │  │
│  │                                                                  │  │
│  │  Parameters:                                                     │  │
│  │  - M (max connections): 16                                       │  │
│  │  - ef_construction: 200                                          │  │
│  │  - ef_search: 100 (tunable)                                      │  │
│  │  - Distance: Cosine similarity                                   │  │
│  │                                                                  │  │
│  │  Memory Layout:                                                  │  │
│  │  - Vectors: Memory-mapped file                                   │  │
│  │  - Graph: In-memory with disk backing                            │  │
│  │  - ~1KB per vector (384-dim float32 + graph links)               │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    BM25 Full-Text Index                         │  │
│  │                                                                  │  │
│  │  Implementation: SQLite FTS5                                     │  │
│  │  - Porter stemmer                                                │  │
│  │  - Trigram tokenizer for fuzzy match                             │  │
│  │  - BM25 ranking function                                         │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    Secondary Indexes                            │  │
│  │                                                                  │  │
│  │  - content_hash: B-tree (deduplication)                          │  │
│  │  - created_at: B-tree (temporal queries)                         │  │
│  │  - source_uri: Hash (provenance lookup)                          │  │
│  │  - graph_source: B-tree (outgoing edges)                         │  │
│  │  - graph_target: B-tree (incoming edges)                         │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.3 Caching Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Caching Architecture                             │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                      Cache Tiers                                │  │
│  │                                                                  │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │  L1: In-Process (Rust HashMap)                            │  │  │
│  │  │  - Hot embeddings (last 1000)                             │  │  │
│  │  │  - Recent search results                                  │  │  │
│  │  │  - Access: ~100ns                                         │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  │                           │                                     │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │  L2: Memory-Mapped (mmap)                                 │  │  │
│  │  │  - HNSW graph structure                                   │  │  │
│  │  │  - Frequently accessed vectors                            │  │  │
│  │  │  - Access: ~1µs                                           │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  │                           │                                     │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │  L3: Disk (SQLite/AgentDB)                                │  │  │
│  │  │  - Full vector store                                      │  │  │
│  │  │  - Document content                                       │  │  │
│  │  │  - Access: ~1-10ms                                        │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                   Embedding Cache                               │  │
│  │  - Key: hash(normalized_text + model_version)                   │  │
│  │  - Value: embedding vector                                      │  │
│  │  - TTL: 7 days (configurable)                                   │  │
│  │  - Max size: 10,000 entries (LRU eviction)                      │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Integration Architecture

### 4.1 agentic-flow Integration

```
┌──────────────────────────────────────────────────────────────────────┐
│                    agentic-flow Integration                           │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                   Agent Memory Interface                        │  │
│  │                                                                  │  │
│  │  // Agent retrieves context for task                             │  │
│  │  agent.memory.search(query, {                                    │  │
│  │    namespace: "agent-123",                                       │  │
│  │    top_k: 20,                                                    │  │
│  │    include_graph: true                                           │  │
│  │  });                                                             │  │
│  │                                                                  │  │
│  │  // Agent stores findings                                        │  │
│  │  agent.memory.store({                                            │  │
│  │    content: "discovered insight",                                │  │
│  │    causal_links: [prior_item_id],                                │  │
│  │    namespace: "agent-123"                                        │  │
│  │  });                                                             │  │
│  │                                                                  │  │
│  │  // Cross-agent memory sharing                                   │  │
│  │  agent.memory.share(item_id, "team-namespace");                  │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                   Swarm Coordination                            │  │
│  │                                                                  │  │
│  │  - Shared memory namespace for swarm tasks                       │  │
│  │  - Transaction semantics for concurrent writes                   │  │
│  │  - Event-driven updates (WebSocket)                              │  │
│  │  - Memory quotas per agent                                       │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 External System Integration

```
┌──────────────────────────────────────────────────────────────────────┐
│                  External System Integration                          │
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │
│  │   File Systems  │  │   Web Sources   │  │   API Connectors    │  │
│  │─────────────────│  │─────────────────│  │─────────────────────│  │
│  │ - Local files   │  │ - URL fetching  │  │ - Notion            │  │
│  │ - Cloud storage │  │ - robots.txt    │  │ - Obsidian          │  │
│  │ - Network shares│  │ - Rate limiting │  │ - Roam              │  │
│  │                 │  │ - Content extract│  │ - Custom webhooks   │  │
│  └────────┬────────┘  └────────┬────────┘  └──────────┬──────────┘  │
│           └────────────────────┼──────────────────────┘              │
│                                ▼                                      │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    Connector Framework                          │  │
│  │                                                                  │  │
│  │  trait SourceConnector {                                         │  │
│  │    fn fetch(&self, uri: &str) -> Result<Content>;               │  │
│  │    fn list(&self, path: &str) -> Result<Vec<Uri>>;              │  │
│  │    fn watch(&self, callback: Fn(Change));                       │  │
│  │  }                                                               │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Deployment Architecture

### 5.1 Local Deployment

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Local Deployment                                 │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                    Single Binary                                │  │
│  │                                                                  │  │
│  │  pmemory                                                         │  │
│  │  ├── Core Services (embedded)                                    │  │
│  │  ├── SQLite Storage                                              │  │
│  │  ├── HNSW Index (in-process)                                     │  │
│  │  └── REST API (localhost only)                                   │  │
│  │                                                                  │  │
│  │  Data Location: ~/.pmemory/                                      │  │
│  │  ├── data.db          (SQLite database)                          │  │
│  │  ├── vectors.idx      (HNSW index)                               │  │
│  │  ├── config.toml      (Configuration)                            │  │
│  │  └── keys/            (Encryption keys)                          │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Resource Requirements:                                               │
│  - RAM: 512MB base + ~4GB per 1M vectors                             │
│  - Disk: ~8GB per 1M vectors                                         │
│  - CPU: 2+ cores recommended                                         │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 Distributed Deployment

```
┌──────────────────────────────────────────────────────────────────────┐
│                   Distributed Deployment                              │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Load Balancer                             │    │
│  │              (nginx/HAProxy/cloud LB)                        │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│                              │                                        │
│  ┌───────────────────────────┼───────────────────────────────────┐  │
│  │                 API Gateway Cluster                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │  │
│  │  │ Gateway │  │ Gateway │  │ Gateway │  (stateless)           │  │
│  │  │   #1    │  │   #2    │  │   #3    │                        │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘                        │  │
│  └───────┼────────────┼────────────┼─────────────────────────────┘  │
│          └────────────┼────────────┘                                 │
│                       ▼                                               │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                  Service Mesh                                   │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────────┐  │  │
│  │  │  Search   │  │  Ingest   │  │  Graph    │  │  Learning  │  │  │
│  │  │  Service  │  │  Service  │  │  Service  │  │  Service   │  │  │
│  │  │  (3x)     │  │  (2x)     │  │  (2x)     │  │  (1x)      │  │  │
│  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └──────┬─────┘  │  │
│  └────────┼──────────────┼──────────────┼───────────────┼────────┘  │
│           └──────────────┼──────────────┼───────────────┘            │
│                          ▼              ▼                             │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                   AgentDB Cluster                               │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐                   │  │
│  │  │  Shard 1  │  │  Shard 2  │  │  Shard 3  │                   │  │
│  │  │  (Vector) │  │  (Vector) │  │  (Vector) │                   │  │
│  │  └───────────┘  └───────────┘  └───────────┘                   │  │
│  │                                                                  │  │
│  │  ┌─────────────────────────────────────────────────────────┐   │  │
│  │  │              Graph Store (replicated)                    │   │  │
│  │  └─────────────────────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 6. Cross-Cutting Concerns

### 6.1 Observability

```
Metrics (Prometheus-compatible):
- pmemory_search_latency_seconds{strategy}
- pmemory_ingest_total{source_type}
- pmemory_cache_hit_ratio{tier}
- pmemory_learning_updates_total
- pmemory_security_threats_detected{type}

Tracing (OpenTelemetry):
- Request traces through service mesh
- Latency breakdown by component
- Error propagation tracking

Logging (structured JSON):
- Security events (audit trail)
- Performance anomalies
- Learning events
```

### 6.2 Error Handling

```
Error Categories:
├── Transient (retry with backoff)
│   ├── Network timeout
│   ├── Rate limit exceeded
│   └── Service temporarily unavailable
├── Permanent (fail fast)
│   ├── Authentication failed
│   ├── Resource not found
│   └── Invalid input
└── Degraded (fallback)
    ├── Provider unavailable (use alternate)
    ├── Cache miss (fetch from source)
    └── Learning service down (use defaults)
```

---

## 7. Architecture Decision Records

### ADR-001: Rust for Core

**Decision**: Use Rust for all core services
**Rationale**: Performance requirements (<50ms latency) and memory safety
**Alternatives Considered**: Go (GC pauses), C++ (safety concerns)
**Consequences**: Steeper learning curve, excellent performance

### ADR-002: SQLite for Local Storage

**Decision**: Use SQLite with custom HNSW for local deployments
**Rationale**: Zero-dependency, proven reliability, portable
**Alternatives Considered**: RocksDB (complexity), PostgreSQL (heavyweight)
**Consequences**: Simple deployment, limited to single-node local

### ADR-003: Thompson Sampling for Strategy Selection

**Decision**: Use Thompson Sampling over epsilon-greedy or UCB
**Rationale**: Natural exploration/exploitation balance, Bayesian updates
**Alternatives Considered**: UCB (less adaptive), epsilon-greedy (suboptimal)
**Consequences**: Slightly more computation, better long-term performance

### ADR-004: Post-Quantum Key Exchange

**Decision**: Implement ML-KEM-768 for key exchange
**Rationale**: Future-proof against quantum attacks
**Alternatives Considered**: X25519 only (vulnerable), ML-KEM-1024 (overkill)
**Consequences**: Larger key sizes, quantum resistance

---

## 8. References

- **Specification**: `spec/01-specification.md`
- **Pseudocode**: `pseudocode/02-pseudocode.md`
- **Security**: `security/04-security.md`
- **Implementation**: `implementation/05-implementation.md`
- **Technology**: `implementation/06-technology.md`
