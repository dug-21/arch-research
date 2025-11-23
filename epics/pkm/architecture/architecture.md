# PKM 2035 System Architecture

## SPARC Architecture Document | November 2025

---

## Executive Summary

This architecture document defines a 2035-ready Personal Knowledge Management (PKM) system designed for sub-millisecond performance, autonomous self-learning, and seamless AI integration. The system leverages MCP-first design patterns, ruvector's high-performance vector engine, and agentic-flow's adaptive learning mechanisms to create an intelligent cognitive partner.

**Key Performance Targets:**
- Capture latency: < 10ms
- Search latency: < 50ms (cached < 5ms)
- Vector query: < 0.5ms (p50)
- Throughput: 50K+ queries/second
- Recall accuracy: 95%+

---

## 1. System Overview

### 1.1 High-Level Architecture

```
+------------------------------------------------------------------+
|                        CLIENT LAYER                               |
+------------------------------------------------------------------+
|                                                                    |
|  +------------------+  +------------------+  +------------------+  |
|  |  Obsidian Plugin |  |   CLI Interface  |  |   Web Client     |  |
|  |  (TypeScript)    |  |   (Rust/Node)    |  |   (WASM)         |  |
|  +--------+---------+  +--------+---------+  +--------+---------+  |
|           |                     |                     |            |
+-----------|---------------------|---------------------|------------+
            |                     |                     |
            +---------------------+---------------------+
                                  |
                          +-------v-------+
                          |   MCP HOST    |
                          | (Orchestrator)|
                          +-------+-------+
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
+-------v-------+         +-------v-------+         +-------v-------+
|   CAPTURE     |         |    SEARCH     |         |    GRAPH      |
|   MCP Server  |         |   MCP Server  |         |   MCP Server  |
+-------+-------+         +-------+-------+         +-------+-------+
        |                         |                         |
+-------v-------+         +-------v-------+         +-------v-------+
|  Quick Entry  |         |  Hybrid Index |         |  Knowledge    |
|  Queue        |         |  (Vector+FTS) |         |  Graph        |
+-------+-------+         +-------+-------+         +-------+-------+
        |                         |                         |
        +-------------------------+-------------------------+
                                  |
                          +-------v-------+
                          |   LEARNING    |
                          |   MCP Server  |
                          +-------+-------+
                                  |
                    +-------------+-------------+
                    |             |             |
            +-------v---+  +------v------+  +---v-------+
            | Reflexion |  | Trajectory  |  |   Skill   |
            | Memory    |  | Storage     |  |  Library  |
            +-----------+  +-------------+  +-----------+
                                  |
+------------------------------------------------------------------+
|                      PERSISTENCE LAYER                            |
+------------------------------------------------------------------+
|                                                                    |
|  +------------------+  +------------------+  +------------------+  |
|  |  ruvector        |  |   TypeDB/Neo4j   |  |   File System    |  |
|  |  (Vector Store)  |  |   (Graph DB)     |  |   (Markdown)     |  |
|  +------------------+  +------------------+  +------------------+  |
|                                                                    |
|  +------------------+  +------------------+  +------------------+  |
|  |  Redis/Valkey    |  |   SQLite         |  |   Ollama         |  |
|  |  (Cache)         |  |   (Metadata)     |  |   (Embeddings)   |  |
|  +------------------+  +------------------+  +------------------+  |
|                                                                    |
+------------------------------------------------------------------+
```

### 1.2 Component Responsibilities

| Component | Responsibility | Performance Target |
|-----------|----------------|-------------------|
| **MCP Host** | Request routing, capability negotiation, response aggregation | < 5ms overhead |
| **Capture Server** | Quick entry, queue management, async processing | < 10ms capture |
| **Search Server** | Hybrid search (vector + FTS + graph), ranking | < 50ms search |
| **Graph Server** | Relationship management, traversal, clustering | < 100ms query |
| **Learning Server** | Pattern recognition, confidence scoring, skill extraction | Background |
| **Vector Store** | HNSW indexing, similarity search, quantization | < 0.5ms query |
| **Graph DB** | Entity storage, relationship modeling, path finding | < 50ms traversal |
| **Cache Layer** | Multi-level caching (L1/L2/L3), TTL management | < 1ms hit |

### 1.3 Data Flow

```
CAPTURE FLOW:
User Input --> Obsidian Plugin --> MCP Host --> Capture Server
    |
    v
Quick Queue (< 10ms) --> Background Processor --> Embedding Service
    |                                                   |
    v                                                   v
Metadata Store <------ Knowledge Entry -----> Vector Store
    |                         |
    v                         v
Graph Server ----------> Link Discovery --> Knowledge Graph

RETRIEVAL FLOW:
Query --> MCP Host --> Search Server
    |
    +---> L1 Cache (hit) --> Return (< 1ms)
    |
    +---> L2 Cache (hit) --> Return (< 5ms)
    |
    +---> Parallel Search:
          |
          +---> Vector Search (ruvector)
          +---> Full-Text Search (FTS)
          +---> Graph Traversal
          |
          v
    Merge + Rank --> Learning Update --> Return (< 50ms)
```

---

## 2. Core Components

### 2.1 MCP Server Layer

#### Tool Definitions

```typescript
// Core PKM MCP Tools
const pkmTools = {
  // CAPTURE TOOLS
  "pkm/capture": {
    description: "Quick capture with minimal processing",
    inputSchema: {
      type: "object",
      properties: {
        content: { type: "string", description: "Note content" },
        source: { type: "string", enum: ["manual", "voice", "image", "import"] },
        context: {
          type: "object",
          properties: {
            activeNote: { type: "string" },
            selectedText: { type: "string" },
            tags: { type: "array", items: { type: "string" } }
          }
        }
      },
      required: ["content"]
    },
    handler: "captureHandler",
    latencyTarget: "10ms"
  },

  "pkm/capture_voice": {
    description: "Capture from voice transcription",
    inputSchema: {
      type: "object",
      properties: {
        audioPath: { type: "string" },
        language: { type: "string", default: "en" }
      },
      required: ["audioPath"]
    },
    handler: "voiceCaptureHandler",
    latencyTarget: "500ms"
  },

  // SEARCH TOOLS
  "pkm/search": {
    description: "Hybrid semantic + keyword + graph search",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query" },
        k: { type: "number", default: 10, description: "Number of results" },
        mode: {
          type: "string",
          enum: ["semantic", "keyword", "hybrid", "graph"],
          default: "hybrid"
        },
        filters: {
          type: "object",
          properties: {
            tags: { type: "array", items: { type: "string" } },
            dateRange: {
              type: "object",
              properties: {
                start: { type: "string", format: "date" },
                end: { type: "string", format: "date" }
              }
            },
            noteType: { type: "string" }
          }
        },
        includeContext: { type: "boolean", default: true }
      },
      required: ["query"]
    },
    handler: "searchHandler",
    latencyTarget: "50ms"
  },

  "pkm/find_related": {
    description: "Find semantically related notes",
    inputSchema: {
      type: "object",
      properties: {
        noteId: { type: "string" },
        k: { type: "number", default: 5 },
        minSimilarity: { type: "number", default: 0.7 }
      },
      required: ["noteId"]
    },
    handler: "findRelatedHandler",
    latencyTarget: "30ms"
  },

  // GRAPH TOOLS
  "pkm/link": {
    description: "Create knowledge connection between notes",
    inputSchema: {
      type: "object",
      properties: {
        sourceId: { type: "string" },
        targetId: { type: "string" },
        relationship: {
          type: "string",
          enum: ["references", "supports", "contradicts", "extends", "questions", "related"]
        },
        bidirectional: { type: "boolean", default: false },
        confidence: { type: "number", default: 1.0 }
      },
      required: ["sourceId", "targetId", "relationship"]
    },
    handler: "linkHandler",
    latencyTarget: "100ms"
  },

  "pkm/graph_query": {
    description: "Query knowledge graph with path finding",
    inputSchema: {
      type: "object",
      properties: {
        startNode: { type: "string" },
        endNode: { type: "string" },
        maxDepth: { type: "number", default: 3 },
        relationshipTypes: { type: "array", items: { type: "string" } }
      },
      required: ["startNode"]
    },
    handler: "graphQueryHandler",
    latencyTarget: "100ms"
  },

  "pkm/cluster": {
    description: "Find concept clusters in knowledge base",
    inputSchema: {
      type: "object",
      properties: {
        topic: { type: "string" },
        algorithm: { type: "string", enum: ["kmeans", "dbscan", "hierarchical"], default: "dbscan" },
        minClusterSize: { type: "number", default: 3 }
      },
      required: ["topic"]
    },
    handler: "clusterHandler",
    latencyTarget: "500ms"
  },

  // LEARNING TOOLS
  "pkm/learn_pattern": {
    description: "Record successful pattern for future use",
    inputSchema: {
      type: "object",
      properties: {
        patternType: { type: "string", enum: ["search", "link", "workflow", "synthesis"] },
        context: { type: "object" },
        outcome: { type: "string", enum: ["success", "partial", "failure"] },
        trajectory: { type: "array", items: { type: "object" } }
      },
      required: ["patternType", "context", "outcome"]
    },
    handler: "learnPatternHandler",
    latencyTarget: "50ms"
  },

  "pkm/get_recommendations": {
    description: "Get AI-powered recommendations based on context",
    inputSchema: {
      type: "object",
      properties: {
        currentNoteId: { type: "string" },
        recentActivity: { type: "array", items: { type: "string" } },
        goalContext: { type: "string" }
      }
    },
    handler: "recommendationsHandler",
    latencyTarget: "100ms"
  },

  "pkm/synthesize": {
    description: "Generate insights from multiple notes",
    inputSchema: {
      type: "object",
      properties: {
        noteIds: { type: "array", items: { type: "string" } },
        topic: { type: "string" },
        outputFormat: { type: "string", enum: ["summary", "outline", "essay", "questions"] },
        depth: { type: "string", enum: ["brief", "standard", "comprehensive"] }
      },
      required: ["noteIds"]
    },
    handler: "synthesizeHandler",
    streaming: true,
    latencyTarget: "streaming"
  }
};
```

#### Request Routing

```typescript
interface MCPRouter {
  // Route configuration
  routes: Map<string, RouteConfig>;

  // Capability-based routing
  capabilities: {
    caching: boolean;
    streaming: boolean;
    batching: boolean;
    learning: boolean;
  };

  // Request handling
  async route(request: MCPRequest): Promise<MCPResponse> {
    // 1. Check cache first
    const cached = await this.cache.get(request.hash);
    if (cached) return cached;

    // 2. Determine optimal handler
    const handler = this.selectHandler(request);

    // 3. Execute with timeout
    const result = await Promise.race([
      handler.execute(request),
      this.timeout(handler.latencyTarget)
    ]);

    // 4. Update learning system
    await this.learning.recordInteraction(request, result);

    // 5. Cache successful results
    if (result.success) {
      await this.cache.set(request.hash, result, handler.cacheTTL);
    }

    return result;
  }
}
```

#### Response Formatting

```typescript
interface PKMResponse {
  // Standard fields
  success: boolean;
  data: any;

  // Performance metadata
  meta: {
    latency: number;
    cacheHit: boolean;
    source: string;
  };

  // Learning signals
  learning: {
    confidence: number;
    patternId?: string;
    suggestedLinks?: string[];
  };

  // Pagination for large results
  pagination?: {
    total: number;
    offset: number;
    limit: number;
    hasMore: boolean;
  };
}
```

### 2.2 Vector Engine (ruvector)

#### HNSW Index Configuration

```rust
// ruvector configuration for PKM workloads
pub struct PKMVectorConfig {
    // Core HNSW parameters
    pub hnsw: HNSWConfig {
        // Max connections per layer
        // Higher = better recall, more memory
        m: 16,

        // Construction-time search depth
        // Higher = better index quality, slower build
        ef_construction: 200,

        // Query-time search depth
        // Higher = better recall, slower query
        ef_search: 100,

        // Maximum layers in hierarchy
        max_level: 16,
    },

    // Vector dimensions
    // 384 for all-MiniLM-L6-v2
    // 768 for larger models
    // 1536 for OpenAI ada-002
    dimensions: 384,

    // Distance metric
    distance_metric: DistanceMetric::Cosine,

    // Storage path
    storage_path: PathBuf::from("./data/pkm-vectors"),

    // Memory mapping for large indexes
    mmap_enabled: true,
}
```

#### Quantization Settings

```rust
// Quantization for memory efficiency
pub struct QuantizationConfig {
    // Enable quantization
    enabled: bool,

    // Quantization type
    quantization_type: QuantizationType::ProductQuantization {
        // Number of subvectors
        // Higher = better accuracy, less compression
        num_subvectors: 8,

        // Bits per code
        // 8 = 32x compression with ~95% recall
        // 4 = 64x compression with ~90% recall
        bits_per_code: 8,
    },

    // Compression ratio target
    // 16x = good balance for PKM
    compression_ratio: 16,

    // Training samples for codebook
    training_samples: 10000,
}

// Performance by quantization level
// +------------------+------------+-----------+--------+
// | Type             | Compression| Recall    | Memory |
// +------------------+------------+-----------+--------+
// | Float32 (none)   | 1x         | 100%      | 1.5MB  |
// | Int8             | 4x         | 98%       | 375KB  |
// | Product (8-bit)  | 16x        | 95%       | 94KB   |
// | Binary           | 32x        | 90%       | 47KB   |
// +------------------+------------+-----------+--------+
// (Per 1000 vectors at 384 dimensions)
```

#### Caching Strategy

```typescript
// Multi-level cache configuration
interface VectorCacheConfig {
  // L1: In-memory hot cache
  l1: {
    type: "lru",
    maxSize: 10000,      // entries
    maxMemory: "100MB",
    ttl: 3600,           // 1 hour
    eviction: "lru",
  },

  // L2: Vector similarity cache
  l2: {
    type: "semantic",
    maxSize: 100000,
    similarityThreshold: 0.95,  // Cache hit if query >95% similar
    ttl: 86400,          // 24 hours
  },

  // L3: Persistent disk cache
  l3: {
    type: "disk",
    path: "./cache/vectors",
    maxSize: "1GB",
    compression: "zstd",
    ttl: 604800,         // 7 days
  },

  // Cache warming strategy
  warming: {
    enabled: true,
    schedule: "0 3 * * *",  // 3 AM daily
    topK: 1000,             // Pre-cache top 1000 queries
    recentDays: 7,          // Based on last 7 days access
  },
}

// Cache access pattern
async function vectorSearch(query: Float32Array, k: number): Promise<SearchResult[]> {
  const queryHash = hashVector(query);

  // L1: Exact match (< 1ms)
  let result = await l1Cache.get(queryHash);
  if (result) return result;

  // L2: Semantic similarity (< 5ms)
  result = await l2Cache.findSimilar(query, 0.95);
  if (result) {
    await l1Cache.set(queryHash, result);
    return result;
  }

  // L3: Disk cache (< 20ms)
  result = await l3Cache.get(queryHash);
  if (result) {
    await l1Cache.set(queryHash, result);
    return result;
  }

  // Vector database (< 0.5ms for index, total < 50ms)
  result = await vectorDB.search(query, k);

  // Populate caches
  await Promise.all([
    l1Cache.set(queryHash, result),
    l2Cache.set(query, result),
    l3Cache.set(queryHash, result),
  ]);

  return result;
}
```

### 2.3 Knowledge Graph

#### Entity Storage

```typescript
// Entity schema for PKM
interface KnowledgeEntity {
  // Core identity
  id: string;                    // UUID
  name: string;                  // Display name
  type: EntityType;              // note, concept, person, project, tag

  // Content
  content?: string;              // Full content for notes
  summary?: string;              // Auto-generated summary

  // Vector representation
  embedding: Float32Array;       // Semantic embedding
  embeddingModel: string;        // Model used for embedding
  embeddingVersion: number;      // For re-embedding on model change

  // Metadata
  properties: Record<string, any>;
  tags: string[];

  // Temporal
  createdAt: number;
  modifiedAt: number;
  accessedAt: number;

  // Learning metadata
  importance: number;            // 0-1, learned from usage
  confidence: number;            // 0-1, data quality score
  accessCount: number;

  // Source tracking
  source: {
    type: "obsidian" | "import" | "synthesis";
    path?: string;
    url?: string;
  };
}

// Entity types for PKM domain
enum EntityType {
  NOTE = "note",           // Primary knowledge units
  CONCEPT = "concept",     // Extracted concepts/topics
  PERSON = "person",       // People mentioned
  PROJECT = "project",     // Projects/initiatives
  TAG = "tag",             // Organizational tags
  CLUSTER = "cluster",     // Auto-generated groupings
  QUESTION = "question",   // Open questions
  INSIGHT = "insight",     // Synthesized insights
}
```

#### Relationship Model

```typescript
// Edge/Relationship schema
interface KnowledgeRelation {
  // Identity
  id: string;

  // Connection
  source: string;              // Source entity ID
  target: string;              // Target entity ID
  type: RelationType;          // Relationship type

  // Strength and confidence
  weight: number;              // 0-1, connection strength
  confidence: number;          // 0-1, how confident in this link

  // Provenance
  createdBy: "user" | "system" | "ai";
  evidence?: string[];         // Supporting evidence

  // Temporal
  createdAt: number;
  lastValidated: number;

  // Learning
  usageCount: number;          // Times traversed
  successRate: number;         // How often useful in retrieval
}

// Relationship types for PKM
enum RelationType {
  // Structural
  REFERENCES = "references",       // A cites B
  EXTENDS = "extends",             // A builds on B
  SUMMARIZES = "summarizes",       // A is summary of B

  // Semantic
  SUPPORTS = "supports",           // A provides evidence for B
  CONTRADICTS = "contradicts",     // A conflicts with B
  RELATED = "related",             // General semantic similarity

  // Causal
  CAUSES = "causes",               // A leads to B
  ENABLES = "enables",             // A makes B possible

  // Temporal
  PRECEDES = "precedes",           // A comes before B
  FOLLOWS = "follows",             // A comes after B

  // Hierarchical
  CONTAINS = "contains",           // A includes B
  PART_OF = "part_of",             // A is part of B

  // Questioning
  QUESTIONS = "questions",         // A raises questions about B
  ANSWERS = "answers",             // A answers B
}

// Hypergraph support for multi-way relationships
interface Hyperedge {
  id: string;
  entities: string[];              // Multiple connected entities
  type: string;
  properties: Record<string, any>;
  weight: number;
}
```

#### Query Patterns

```cypher
// TypeDB/Cypher query patterns for PKM

// 1. Find all notes related to a concept within 2 hops
MATCH path = (n:Note)-[*1..2]-(c:Concept {name: $conceptName})
WHERE n <> c
RETURN n, relationships(path), length(path) as distance
ORDER BY distance ASC, n.importance DESC
LIMIT 20;

// 2. Find contradiction clusters
MATCH (a:Note)-[:CONTRADICTS]->(b:Note)
WHERE a.confidence > 0.7 AND b.confidence > 0.7
RETURN a, b,
       a.summary as claim_a,
       b.summary as claim_b
ORDER BY a.importance + b.importance DESC;

// 3. Knowledge path between two notes
MATCH path = shortestPath(
  (start:Note {id: $startId})-[*..5]-(end:Note {id: $endId})
)
RETURN path,
       [r in relationships(path) | r.type] as relationship_types,
       length(path) as hops;

// 4. Concept clusters with high interconnection
MATCH (c:Concept)<-[:REFERENCES]-(n:Note)
WITH c, collect(n) as notes, count(n) as noteCount
WHERE noteCount > 5
MATCH (n1:Note)-[r]-(n2:Note)
WHERE n1 IN notes AND n2 IN notes AND n1 <> n2
RETURN c.name as concept,
       noteCount,
       count(r) as interconnections,
       count(r) / (noteCount * (noteCount-1)) as density
ORDER BY density DESC;

// 5. Learning trajectory - successful retrieval patterns
MATCH (q:Query)-[:RETRIEVED]->(n:Note)
WHERE q.success = true AND q.timestamp > $since
WITH n, count(q) as retrievalCount, avg(q.satisfaction) as avgSatisfaction
SET n.importance = 0.7 * n.importance + 0.3 * (retrievalCount / 100)
RETURN n.id, n.importance, retrievalCount;

// 6. Find knowledge gaps (questions without answers)
MATCH (q:Question)
WHERE NOT (q)-[:ANSWERS]->()
  AND q.createdAt > $since
RETURN q.content, q.context, q.importance
ORDER BY q.importance DESC;
```

### 2.4 Self-Learning Engine

#### Pattern Recognition

```typescript
// SAFLA-inspired pattern recognition system
class PatternRecognitionEngine {
  private patterns: Map<string, LearnedPattern>;
  private trajectories: Trajectory[];
  private vectorStore: VectorDB;

  // Pattern structure
  interface LearnedPattern {
    id: string;
    type: "search" | "link" | "workflow" | "synthesis";

    // Pattern definition
    trigger: {
      context: ContextVector;
      query: string;
      entities: string[];
    };

    // Learned response
    action: {
      strategy: string;
      parameters: Record<string, any>;
      expectedOutcome: string;
    };

    // Performance metrics
    metrics: {
      usageCount: number;
      successRate: number;
      avgLatency: number;
      lastUsed: number;
    };

    // Confidence tracking
    confidence: number;           // 0-1, increases with success
    trajectory: "improving" | "stable" | "declining";
  }

  // Pattern matching
  async matchPattern(context: Context): Promise<LearnedPattern[]> {
    // Generate context embedding
    const contextVector = await this.embedContext(context);

    // Find similar patterns
    const similar = await this.vectorStore.search(contextVector, {
      k: 10,
      minSimilarity: 0.7,
      filter: { type: context.taskType }
    });

    // Filter by confidence and recency
    return similar
      .filter(p => p.confidence > 0.6)
      .filter(p => this.isRecentlySuccessful(p))
      .sort((a, b) => b.confidence * b.metrics.successRate -
                      a.confidence * a.metrics.successRate);
  }

  // Pattern extraction from trajectories
  async extractPatterns(): Promise<void> {
    // Find successful action sequences
    const successful = this.trajectories.filter(t => t.success);

    // Cluster similar trajectories
    const clusters = await this.clusterTrajectories(successful);

    for (const cluster of clusters) {
      if (cluster.size >= 3) {  // Minimum frequency threshold
        const pattern = this.synthesizePattern(cluster);
        await this.storePattern(pattern);
      }
    }
  }

  // Update pattern from feedback
  async updatePattern(patternId: string, success: boolean, latency: number): Promise<void> {
    const pattern = this.patterns.get(patternId);
    if (!pattern) return;

    // Update metrics
    pattern.metrics.usageCount++;
    pattern.metrics.successRate =
      (pattern.metrics.successRate * (pattern.metrics.usageCount - 1) + (success ? 1 : 0)) /
      pattern.metrics.usageCount;
    pattern.metrics.avgLatency =
      (pattern.metrics.avgLatency * (pattern.metrics.usageCount - 1) + latency) /
      pattern.metrics.usageCount;
    pattern.metrics.lastUsed = Date.now();

    // Update confidence
    const delta = success ? 0.02 : -0.01;
    pattern.confidence = Math.max(0.1, Math.min(1.0, pattern.confidence + delta));

    // Update trajectory
    pattern.trajectory = this.calculateTrajectory(pattern);

    await this.persistPattern(pattern);
  }
}
```

#### Confidence Scoring

```typescript
// Multi-factor confidence scoring system
class ConfidenceScorer {
  // Confidence factors
  private weights = {
    dataQuality: 0.25,      // Source reliability
    recency: 0.15,          // Temporal relevance
    usage: 0.20,            // Access frequency
    connections: 0.20,      // Graph centrality
    userFeedback: 0.20,     // Explicit ratings
  };

  async calculateConfidence(entity: KnowledgeEntity): Promise<number> {
    const scores = await Promise.all([
      this.dataQualityScore(entity),
      this.recencyScore(entity),
      this.usageScore(entity),
      this.connectionScore(entity),
      this.userFeedbackScore(entity),
    ]);

    // Weighted combination
    let confidence = 0;
    const factors = Object.keys(this.weights);
    for (let i = 0; i < factors.length; i++) {
      confidence += scores[i] * this.weights[factors[i]];
    }

    return confidence;
  }

  private async dataQualityScore(entity: KnowledgeEntity): Promise<number> {
    let score = 0.5;  // Base score

    // Has complete metadata
    if (entity.properties && Object.keys(entity.properties).length > 3) {
      score += 0.1;
    }

    // Has valid embedding
    if (entity.embedding && entity.embedding.length > 0) {
      score += 0.15;
    }

    // Has summary
    if (entity.summary && entity.summary.length > 50) {
      score += 0.1;
    }

    // Source reliability
    if (entity.source.type === "obsidian") {
      score += 0.15;  // User-created
    }

    return Math.min(1.0, score);
  }

  private recencyScore(entity: KnowledgeEntity): number {
    const now = Date.now();
    const age = now - entity.modifiedAt;
    const oneWeek = 7 * 24 * 60 * 60 * 1000;
    const oneMonth = 30 * 24 * 60 * 60 * 1000;
    const oneYear = 365 * 24 * 60 * 60 * 1000;

    if (age < oneWeek) return 1.0;
    if (age < oneMonth) return 0.8;
    if (age < oneYear) return 0.5;
    return 0.3;
  }

  private async usageScore(entity: KnowledgeEntity): Promise<number> {
    // Normalize access count
    const maxAccess = await this.getMaxAccessCount();
    return Math.min(1.0, entity.accessCount / maxAccess);
  }

  private async connectionScore(entity: KnowledgeEntity): Promise<number> {
    // PageRank-style centrality
    const connections = await this.graphDB.getConnectionCount(entity.id);
    const avgConnections = await this.graphDB.getAverageConnections();
    return Math.min(1.0, connections / (avgConnections * 2));
  }
}

// Confidence thresholds for PKM operations
const CONFIDENCE_THRESHOLDS = {
  autoLink: 0.80,           // Auto-create links above this
  suggest: 0.60,            // Suggest to user above this
  archive: 0.30,            // Consider archiving below this
  verify: 0.50,             // Flag for verification below this
};
```

#### Trajectory Storage

```typescript
// Trajectory storage for learning from workflows
interface Trajectory {
  id: string;
  sessionId: string;

  // Sequence of actions
  steps: TrajectoryStep[];

  // Outcome
  outcome: {
    success: boolean;
    satisfaction: number;    // User satisfaction 0-1
    completionTime: number;
    errors: string[];
  };

  // Context
  context: {
    goal: string;
    initialState: StateSnapshot;
    finalState: StateSnapshot;
  };

  // Metadata
  timestamp: number;
  userId?: string;
}

interface TrajectoryStep {
  action: string;            // MCP tool called
  parameters: Record<string, any>;
  result: any;
  duration: number;
  success: boolean;

  // State changes
  stateChange: {
    entitiesCreated: string[];
    entitiesModified: string[];
    linksCreated: string[];
  };
}

class TrajectoryStore {
  private db: SQLite;
  private vectorStore: VectorDB;

  async store(trajectory: Trajectory): Promise<void> {
    // Store trajectory metadata
    await this.db.insert('trajectories', trajectory);

    // Index by goal for pattern matching
    const goalEmbedding = await this.embed(trajectory.context.goal);
    await this.vectorStore.insert(trajectory.id, goalEmbedding, {
      success: trajectory.outcome.success,
      stepCount: trajectory.steps.length,
      actions: trajectory.steps.map(s => s.action)
    });
  }

  async findSimilar(goal: string, k: number = 5): Promise<Trajectory[]> {
    const goalEmbedding = await this.embed(goal);
    const similar = await this.vectorStore.search(goalEmbedding, {
      k,
      filter: { success: true }
    });

    return Promise.all(
      similar.map(s => this.db.get('trajectories', s.id))
    );
  }

  async getSuccessfulPatterns(action: string): Promise<TrajectoryStep[]> {
    return this.db.query(`
      SELECT steps
      FROM trajectories
      WHERE outcome_success = true
        AND steps LIKE '%"action":"${action}"%'
      ORDER BY outcome_satisfaction DESC
      LIMIT 100
    `);
  }
}
```

### 2.5 Obsidian Plugin

#### Bridge Architecture

```typescript
// Obsidian Plugin Bridge to MCP
import { Plugin, App, TFile, WorkspaceLeaf } from 'obsidian';

export default class PKMEnhancedPlugin extends Plugin {
  private mcpClient: MCPClient;
  private vectorIndex: LocalVectorIndex;
  private syncManager: SyncManager;
  private uiManager: UIManager;

  async onload() {
    // Initialize MCP connection
    this.mcpClient = new MCPClient({
      transport: "stdio",
      serverCommand: "npx",
      serverArgs: ["pkm-mcp-server", "start"],
      capabilities: {
        caching: true,
        streaming: true,
        learning: true,
      }
    });
    await this.mcpClient.connect();

    // Initialize local vector index (for offline support)
    this.vectorIndex = new LocalVectorIndex({
      dimensions: 384,
      storagePath: this.manifest.dir + "/vectors",
    });

    // Initialize sync manager
    this.syncManager = new SyncManager(this.app.vault, this.mcpClient);

    // Register event handlers
    this.registerEvents();

    // Register commands
    this.registerCommands();

    // Register views
    this.registerViews();

    // Initial sync
    await this.syncManager.fullSync();
  }

  private registerEvents() {
    // Note creation
    this.registerEvent(
      this.app.vault.on('create', async (file) => {
        if (file instanceof TFile && file.extension === 'md') {
          await this.handleNoteCreated(file);
        }
      })
    );

    // Note modification
    this.registerEvent(
      this.app.vault.on('modify', async (file) => {
        if (file instanceof TFile && file.extension === 'md') {
          await this.handleNoteModified(file);
        }
      })
    );

    // Note deletion
    this.registerEvent(
      this.app.vault.on('delete', async (file) => {
        if (file instanceof TFile && file.extension === 'md') {
          await this.handleNoteDeleted(file);
        }
      })
    );

    // Note rename
    this.registerEvent(
      this.app.vault.on('rename', async (file, oldPath) => {
        if (file instanceof TFile && file.extension === 'md') {
          await this.handleNoteRenamed(file, oldPath);
        }
      })
    );

    // Active note change (for context)
    this.registerEvent(
      this.app.workspace.on('file-open', async (file) => {
        if (file) {
          await this.updateContext(file);
        }
      })
    );

    // Metadata cache update
    this.registerEvent(
      this.app.metadataCache.on('changed', async (file, data, cache) => {
        await this.handleMetadataChanged(file, cache);
      })
    );
  }

  private async handleNoteCreated(file: TFile) {
    const content = await this.app.vault.read(file);
    const frontmatter = this.app.metadataCache.getFileCache(file)?.frontmatter;

    // Quick capture to MCP
    await this.mcpClient.call('pkm/capture', {
      content,
      source: 'obsidian',
      context: {
        path: file.path,
        frontmatter,
        links: this.extractLinks(file),
      }
    });
  }

  private async handleNoteModified(file: TFile) {
    // Debounced to avoid excessive updates
    await this.syncManager.queueUpdate(file);
  }
}
```

#### Event Handling

```typescript
// Event handling patterns for Obsidian integration
class EventHandler {
  private debounceMap: Map<string, NodeJS.Timeout> = new Map();
  private mcpClient: MCPClient;

  // Debounced modification handler
  async handleModification(file: TFile, vault: Vault): Promise<void> {
    const existingTimeout = this.debounceMap.get(file.path);
    if (existingTimeout) {
      clearTimeout(existingTimeout);
    }

    const timeout = setTimeout(async () => {
      const content = await vault.read(file);

      // Check if content actually changed (vs just metadata)
      const hash = await this.hashContent(content);
      const prevHash = await this.getStoredHash(file.path);

      if (hash !== prevHash) {
        // Content changed - full re-index
        await this.mcpClient.call('pkm/capture', {
          content,
          source: 'obsidian',
          context: { path: file.path, type: 'update' }
        });
        await this.storeHash(file.path, hash);
      } else {
        // Only metadata changed
        await this.mcpClient.call('pkm/update_metadata', {
          noteId: file.path,
          metadata: this.extractMetadata(file)
        });
      }

      this.debounceMap.delete(file.path);
    }, 2000);  // 2 second debounce

    this.debounceMap.set(file.path, timeout);
  }

  // Link change detection
  async handleLinkChange(
    file: TFile,
    oldLinks: string[],
    newLinks: string[]
  ): Promise<void> {
    const added = newLinks.filter(l => !oldLinks.includes(l));
    const removed = oldLinks.filter(l => !newLinks.includes(l));

    // Create new graph edges
    for (const link of added) {
      await this.mcpClient.call('pkm/link', {
        sourceId: file.path,
        targetId: link,
        relationship: 'references',
        createdBy: 'user'
      });
    }

    // Remove old graph edges
    for (const link of removed) {
      await this.mcpClient.call('pkm/unlink', {
        sourceId: file.path,
        targetId: link
      });
    }
  }

  // Context tracking for recommendations
  async handleContextChange(file: TFile): Promise<void> {
    await this.mcpClient.call('pkm/update_context', {
      activeNote: file.path,
      timestamp: Date.now(),
      session: this.sessionId
    });

    // Prefetch related notes for faster access
    const related = await this.mcpClient.call('pkm/find_related', {
      noteId: file.path,
      k: 10
    });

    await this.prefetchNotes(related);
  }
}
```

#### UI Components

```typescript
// UI Components for Obsidian Plugin
import { ItemView, WorkspaceLeaf, Modal, Setting } from 'obsidian';

// Smart Connections View
export const VIEW_TYPE_CONNECTIONS = 'pkm-connections-view';

export class ConnectionsView extends ItemView {
  private mcpClient: MCPClient;
  private currentNoteId: string;
  private connections: Connection[] = [];

  getViewType(): string {
    return VIEW_TYPE_CONNECTIONS;
  }

  getDisplayText(): string {
    return 'Knowledge Connections';
  }

  getIcon(): string {
    return 'git-branch';
  }

  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass('pkm-connections-container');

    // Header
    const header = container.createDiv('pkm-header');
    header.createEl('h4', { text: 'Related Notes' });

    // Search input
    const searchContainer = container.createDiv('pkm-search');
    const searchInput = searchContainer.createEl('input', {
      type: 'text',
      placeholder: 'Search connections...'
    });
    searchInput.addEventListener('input',
      debounce((e) => this.filterConnections(e.target.value), 300)
    );

    // Connections list
    this.connectionsEl = container.createDiv('pkm-connections-list');

    // Load initial connections
    await this.loadConnections();
  }

  async loadConnections() {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile) return;

    this.currentNoteId = activeFile.path;

    const result = await this.mcpClient.call('pkm/find_related', {
      noteId: this.currentNoteId,
      k: 20
    });

    this.connections = result.data;
    this.renderConnections();
  }

  renderConnections() {
    this.connectionsEl.empty();

    // Group by relationship type
    const grouped = this.groupByType(this.connections);

    for (const [type, items] of Object.entries(grouped)) {
      const group = this.connectionsEl.createDiv('pkm-connection-group');
      group.createEl('h5', { text: this.formatType(type) });

      for (const item of items) {
        const itemEl = group.createDiv('pkm-connection-item');

        // Title with click handler
        const titleEl = itemEl.createEl('span', {
          text: item.title,
          cls: 'pkm-connection-title'
        });
        titleEl.addEventListener('click', () => {
          this.app.workspace.openLinkText(item.path, '', false);
        });

        // Confidence indicator
        const confidenceEl = itemEl.createDiv('pkm-confidence');
        confidenceEl.style.width = `${item.confidence * 100}%`;
        confidenceEl.addClass(this.getConfidenceClass(item.confidence));

        // Preview on hover
        itemEl.addEventListener('mouseenter', () => {
          this.showPreview(item);
        });
      }
    }
  }
}

// Quick Capture Modal
export class QuickCaptureModal extends Modal {
  private mcpClient: MCPClient;
  private onCapture: (noteId: string) => void;

  constructor(app: App, mcpClient: MCPClient, onCapture: (noteId: string) => void) {
    super(app);
    this.mcpClient = mcpClient;
    this.onCapture = onCapture;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.addClass('pkm-quick-capture');

    // Title
    contentEl.createEl('h2', { text: 'Quick Capture' });

    // Content input
    const textarea = contentEl.createEl('textarea', {
      placeholder: 'Capture your thought...',
      cls: 'pkm-capture-input'
    });
    textarea.rows = 5;

    // Tags input
    const tagsContainer = contentEl.createDiv('pkm-tags-container');
    const tagsInput = tagsContainer.createEl('input', {
      type: 'text',
      placeholder: 'Tags (comma separated)'
    });

    // Submit button
    const submitBtn = contentEl.createEl('button', {
      text: 'Capture',
      cls: 'mod-cta'
    });

    submitBtn.addEventListener('click', async () => {
      const content = textarea.value.trim();
      if (!content) return;

      const tags = tagsInput.value
        .split(',')
        .map(t => t.trim())
        .filter(t => t);

      const result = await this.mcpClient.call('pkm/capture', {
        content,
        source: 'manual',
        context: {
          tags,
          activeNote: this.app.workspace.getActiveFile()?.path
        }
      });

      this.onCapture(result.data.id);
      this.close();
    });

    // Focus textarea
    textarea.focus();

    // Keyboard shortcuts
    this.scope.register([], 'Enter', (e) => {
      if (e.ctrlKey || e.metaKey) {
        submitBtn.click();
        return false;
      }
    });
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

// Search Results View
export class SearchResultsView extends ItemView {
  private results: SearchResult[] = [];
  private query: string = '';

  getViewType(): string {
    return 'pkm-search-results';
  }

  getDisplayText(): string {
    return 'Search Results';
  }

  async search(query: string) {
    this.query = query;

    const result = await this.mcpClient.call('pkm/search', {
      query,
      k: 50,
      mode: 'hybrid',
      includeContext: true
    });

    this.results = result.data;
    this.render();
  }

  render() {
    const container = this.containerEl.children[1];
    container.empty();

    // Results header
    container.createEl('h4', {
      text: `${this.results.length} results for "${this.query}"`
    });

    // Results list
    const list = container.createDiv('pkm-results-list');

    for (const result of this.results) {
      const item = list.createDiv('pkm-result-item');

      // Title
      const title = item.createEl('div', {
        text: result.title,
        cls: 'pkm-result-title'
      });
      title.addEventListener('click', () => {
        this.app.workspace.openLinkText(result.path, '', false);
      });

      // Snippet with highlights
      const snippet = item.createEl('div', {
        cls: 'pkm-result-snippet'
      });
      snippet.innerHTML = this.highlightQuery(result.snippet, this.query);

      // Metadata
      const meta = item.createDiv('pkm-result-meta');
      meta.createSpan({ text: result.type });
      meta.createSpan({ text: `${Math.round(result.similarity * 100)}% match` });
      meta.createSpan({ text: this.formatDate(result.modifiedAt) });
    }
  }
}
```

---

## 3. Data Architecture

### 3.1 Storage Layers

```
+------------------------------------------------------------------+
|                      STORAGE ARCHITECTURE                         |
+------------------------------------------------------------------+

HOT TIER (< 1ms access)
+------------------+  +------------------+  +------------------+
| L1 Memory Cache  |  | Active Sessions  |  | Working Context  |
| - Recent queries |  | - User state     |  | - Current note   |
| - Embeddings     |  | - Navigation     |  | - Related items  |
| (LRU, 100MB)     |  | (TTL: session)   |  | (TTL: 5min)      |
+------------------+  +------------------+  +------------------+

WARM TIER (< 50ms access)
+------------------+  +------------------+  +------------------+
| Redis/Valkey     |  | Vector Index     |  | Graph Index      |
| - Query cache    |  | - HNSW index     |  | - Hot paths      |
| - Session data   |  | - Quantized      |  | - Freq clusters  |
| (TTL: 1hr)       |  | (Memory-mapped)  |  | (TTL: 24hr)      |
+------------------+  +------------------+  +------------------+

COLD TIER (< 500ms access)
+------------------+  +------------------+  +------------------+
| SQLite/Postgres  |  | ruvector Files   |  | TypeDB/Neo4j     |
| - Metadata       |  | - Full vectors   |  | - Full graph     |
| - Trajectories   |  | - Archived       |  | - History        |
| - Patterns       |  | (Disk)           |  | (Disk)           |
+------------------+  +------------------+  +------------------+

ARCHIVE TIER (seconds access)
+------------------+  +------------------+  +------------------+
| Compressed       |  | Backup Storage   |  | Sync Storage     |
| Archives         |  | - S3/B2         |  | - Delta sync     |
| - Old notes      |  | - Disaster      |  | - Multi-device   |
| (zstd)           |  | recovery        |  |                  |
+------------------+  +------------------+  +------------------+
```

### 3.2 Index Structures

```typescript
// Index configuration for each data type
const indexConfiguration = {
  // Primary note index (fast full-text search)
  notes: {
    type: "full-text",
    engine: "tantivy",  // or PostgreSQL FTS
    fields: {
      title: { boost: 2.0, tokenizer: "ngram" },
      content: { boost: 1.0, tokenizer: "standard" },
      tags: { boost: 1.5, tokenizer: "keyword" },
    },
    settings: {
      stopWords: "english",
      stemming: true,
      synonyms: "./synonyms.txt",
    }
  },

  // Vector index (semantic search)
  vectors: {
    type: "hnsw",
    engine: "ruvector",
    configuration: {
      dimensions: 384,
      metric: "cosine",
      m: 16,
      efConstruction: 200,
      efSearch: 100,
    },
    quantization: {
      type: "product",
      subvectors: 8,
      bits: 8,
    }
  },

  // Graph index (relationship traversal)
  graph: {
    type: "property-graph",
    engine: "typedb",  // or Neo4j
    indexes: [
      { field: "entity.type", type: "hash" },
      { field: "entity.createdAt", type: "btree" },
      { field: "entity.importance", type: "btree" },
      { field: "relation.type", type: "hash" },
      { field: "relation.weight", type: "btree" },
    ],
    constraints: [
      "entity.id UNIQUE",
      "relation.id UNIQUE",
    ]
  },

  // Metadata index (filtering and faceting)
  metadata: {
    type: "document",
    engine: "sqlite",
    schema: {
      notes: {
        id: "TEXT PRIMARY KEY",
        path: "TEXT UNIQUE",
        title: "TEXT",
        type: "TEXT",
        created_at: "INTEGER",
        modified_at: "INTEGER",
        accessed_at: "INTEGER",
        importance: "REAL",
        confidence: "REAL",
        word_count: "INTEGER",
        tags: "TEXT",  // JSON array
        properties: "TEXT",  // JSON object
      },
      indexes: [
        "CREATE INDEX idx_type ON notes(type)",
        "CREATE INDEX idx_created ON notes(created_at)",
        "CREATE INDEX idx_modified ON notes(modified_at)",
        "CREATE INDEX idx_importance ON notes(importance)",
      ]
    }
  },

  // Learning index (pattern retrieval)
  learning: {
    type: "hybrid",
    patterns: {
      engine: "sqlite",
      vectorIndex: "ruvector",
    },
    trajectories: {
      engine: "sqlite",
      timeSeriesIndex: "btree",
    },
    skills: {
      engine: "ruvector",
      clustering: "dbscan",
    }
  }
};
```

### 3.3 Cache Hierarchy

```typescript
// Cache hierarchy implementation
class CacheHierarchy {
  // L1: In-memory LRU (fastest)
  private l1 = new LRUCache<string, CacheEntry>({
    max: 10000,
    maxSize: 100 * 1024 * 1024,  // 100MB
    sizeCalculation: (entry) => JSON.stringify(entry).length,
    ttl: 1000 * 60 * 60,  // 1 hour
  });

  // L2: Redis/Valkey (shared across processes)
  private l2: Redis;

  // L3: Disk cache (persistence across restarts)
  private l3: DiskCache;

  // Cache entry structure
  interface CacheEntry {
    data: any;
    embedding?: Float32Array;  // For semantic cache
    metadata: {
      createdAt: number;
      accessCount: number;
      lastAccessed: number;
      source: string;
    };
  }

  async get(key: string, options?: CacheOptions): Promise<any | null> {
    // L1 check
    const l1Result = this.l1.get(key);
    if (l1Result) {
      this.recordHit('l1', key);
      return l1Result.data;
    }

    // L2 check
    const l2Result = await this.l2.get(key);
    if (l2Result) {
      const entry = JSON.parse(l2Result);
      this.l1.set(key, entry);  // Promote to L1
      this.recordHit('l2', key);
      return entry.data;
    }

    // L3 check
    const l3Result = await this.l3.get(key);
    if (l3Result) {
      await this.l2.set(key, JSON.stringify(l3Result), 'EX', 3600);  // Promote to L2
      this.l1.set(key, l3Result);  // Promote to L1
      this.recordHit('l3', key);
      return l3Result.data;
    }

    this.recordMiss(key);
    return null;
  }

  async set(key: string, data: any, options?: CacheSetOptions): Promise<void> {
    const entry: CacheEntry = {
      data,
      embedding: options?.embedding,
      metadata: {
        createdAt: Date.now(),
        accessCount: 0,
        lastAccessed: Date.now(),
        source: options?.source || 'unknown',
      }
    };

    // Write to all tiers
    this.l1.set(key, entry);
    await this.l2.set(key, JSON.stringify(entry), 'EX', options?.ttl || 3600);
    await this.l3.set(key, entry);
  }

  // Semantic cache lookup (find similar cached queries)
  async getSemantic(embedding: Float32Array, threshold: number = 0.95): Promise<any | null> {
    // Check semantic index for similar queries
    const similar = await this.semanticIndex.search(embedding, {
      k: 1,
      minSimilarity: threshold
    });

    if (similar.length > 0) {
      return this.get(similar[0].id);
    }

    return null;
  }

  // Cache warming (pre-populate with frequent queries)
  async warm(): Promise<void> {
    // Get top queries from analytics
    const topQueries = await this.analytics.getTopQueries(1000);

    for (const query of topQueries) {
      const result = await this.executeQuery(query);
      await this.set(query.hash, result, {
        source: 'warming',
        ttl: 86400  // 24 hours
      });
    }
  }
}
```

---

## 4. Integration Points

### 4.1 MCP Protocol Handlers

```typescript
// MCP Protocol Handler Implementation
class MCPProtocolHandler {
  private jsonRpc: JSONRPCHandler;
  private capabilities: ServerCapabilities;
  private tools: Map<string, ToolHandler>;

  // Initialize protocol handler
  async initialize(): Promise<InitializeResult> {
    return {
      protocolVersion: "2025-06-18",
      capabilities: {
        tools: { listChanged: true },
        resources: { subscribe: true, listChanged: true },
        prompts: { listChanged: true },
        experimental: {
          learning: true,
          batching: true,
          streaming: true,
        }
      },
      serverInfo: {
        name: "pkm-enhanced",
        version: "1.0.0"
      }
    };
  }

  // Handle tool calls
  async handleToolCall(request: ToolCallRequest): Promise<ToolCallResponse> {
    const tool = this.tools.get(request.params.name);
    if (!tool) {
      throw new MCPError(-32601, `Tool not found: ${request.params.name}`);
    }

    // Validate parameters
    const validated = this.validateParams(tool.inputSchema, request.params.arguments);

    // Execute with timeout
    const startTime = performance.now();
    const result = await Promise.race([
      tool.handler(validated),
      this.timeout(tool.latencyTarget)
    ]);
    const duration = performance.now() - startTime;

    // Record metrics
    await this.metrics.record({
      tool: request.params.name,
      duration,
      success: true
    });

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result)
        }
      ],
      isError: false
    };
  }

  // Handle resource requests
  async handleResourceRead(uri: string): Promise<ResourceContent> {
    const parsed = this.parseResourceURI(uri);

    switch (parsed.type) {
      case 'note':
        return this.readNote(parsed.id);
      case 'graph':
        return this.readGraph(parsed.query);
      case 'pattern':
        return this.readPattern(parsed.id);
      default:
        throw new MCPError(-32602, `Unknown resource type: ${parsed.type}`);
    }
  }

  // Handle batch requests
  async handleBatch(requests: JSONRPCRequest[]): Promise<JSONRPCResponse[]> {
    // Group independent requests
    const independent = this.findIndependentRequests(requests);

    // Execute independent requests in parallel
    const results = await Promise.all(
      independent.map(group =>
        Promise.all(group.map(req => this.handleRequest(req)))
      )
    );

    return results.flat();
  }

  // Streaming response handler
  async *handleStreaming(request: ToolCallRequest): AsyncGenerator<ToolCallChunk> {
    const tool = this.tools.get(request.params.name);
    if (!tool.streaming) {
      throw new MCPError(-32602, `Tool does not support streaming`);
    }

    for await (const chunk of tool.streamHandler(request.params.arguments)) {
      yield {
        type: "tool_call_chunk",
        content: chunk
      };
    }
  }
}
```

### 4.2 Obsidian API Hooks

```typescript
// Obsidian API Integration Layer
class ObsidianAPIHooks {
  private app: App;
  private mcpClient: MCPClient;
  private eventQueue: EventQueue;

  // Vault API hooks
  setupVaultHooks() {
    // Hook into file creation
    this.app.vault.on('create', this.wrapHandler(async (file) => {
      if (this.isMarkdownFile(file)) {
        await this.mcpClient.call('pkm/capture', {
          content: await this.app.vault.read(file),
          source: 'obsidian',
          context: {
            path: file.path,
            event: 'create'
          }
        });
      }
    }));

    // Hook into file modification with intelligent debouncing
    this.app.vault.on('modify', this.wrapHandler(async (file) => {
      if (this.isMarkdownFile(file)) {
        await this.eventQueue.enqueue({
          type: 'modify',
          file: file.path,
          handler: () => this.handleModification(file)
        }, 2000);  // 2 second debounce
      }
    }));

    // Hook into file deletion
    this.app.vault.on('delete', this.wrapHandler(async (file) => {
      if (this.isMarkdownFile(file)) {
        await this.mcpClient.call('pkm/delete', {
          noteId: file.path
        });
      }
    }));

    // Hook into file rename
    this.app.vault.on('rename', this.wrapHandler(async (file, oldPath) => {
      if (this.isMarkdownFile(file)) {
        await this.mcpClient.call('pkm/rename', {
          oldId: oldPath,
          newId: file.path
        });
      }
    }));
  }

  // Metadata cache hooks
  setupMetadataHooks() {
    this.app.metadataCache.on('changed', this.wrapHandler(async (file, data, cache) => {
      // Extract link changes
      const oldLinks = this.previousLinks.get(file.path) || [];
      const newLinks = (cache.links || []).map(l => l.link);

      // Handle link additions
      const added = newLinks.filter(l => !oldLinks.includes(l));
      for (const link of added) {
        await this.mcpClient.call('pkm/link', {
          sourceId: file.path,
          targetId: this.resolveLink(link, file.path),
          relationship: 'references',
          createdBy: 'user'
        });
      }

      // Handle link removals
      const removed = oldLinks.filter(l => !newLinks.includes(l));
      for (const link of removed) {
        await this.mcpClient.call('pkm/unlink', {
          sourceId: file.path,
          targetId: this.resolveLink(link, file.path)
        });
      }

      this.previousLinks.set(file.path, newLinks);

      // Update tags
      const frontmatter = cache.frontmatter;
      if (frontmatter?.tags) {
        await this.mcpClient.call('pkm/update_tags', {
          noteId: file.path,
          tags: frontmatter.tags
        });
      }
    }));

    // Resolve complete event (cache fully built)
    this.app.metadataCache.on('resolve', this.wrapHandler(async (file) => {
      // Trigger full analysis for this note
      await this.mcpClient.call('pkm/analyze', {
        noteId: file.path,
        depth: 'full'
      });
    }));
  }

  // Workspace hooks for context tracking
  setupWorkspaceHooks() {
    // Track active file changes
    this.app.workspace.on('file-open', this.wrapHandler(async (file) => {
      if (file) {
        // Update context for recommendations
        await this.mcpClient.call('pkm/update_context', {
          activeNote: file.path,
          timestamp: Date.now()
        });

        // Prefetch related notes
        const related = await this.mcpClient.call('pkm/find_related', {
          noteId: file.path,
          k: 10
        });
        this.prefetchCache.set(file.path, related);

        // Record access for learning
        await this.mcpClient.call('pkm/learn_pattern', {
          patternType: 'access',
          context: {
            noteId: file.path,
            previousNote: this.previousActiveFile
          },
          outcome: 'success'
        });

        this.previousActiveFile = file.path;
      }
    }));

    // Track editor selections for context
    this.app.workspace.on('editor-selection-change',
      debounce(this.wrapHandler(async (editor) => {
        const selection = editor.getSelection();
        if (selection && selection.length > 10) {
          // Update context with selected text
          await this.mcpClient.call('pkm/update_selection_context', {
            selectedText: selection,
            activeNote: this.app.workspace.getActiveFile()?.path
          });
        }
      }), 500)
    );
  }
}
```

### 4.3 External AI Services

```typescript
// External AI Service Integration
class AIServiceIntegration {
  private providers: Map<string, AIProvider>;
  private router: ModelRouter;
  private fallback: FallbackHandler;

  // Provider configurations
  private providerConfigs = {
    ollama: {
      type: 'local',
      baseUrl: 'http://localhost:11434',
      models: {
        embedding: 'nomic-embed-text',
        chat: 'llama3.1:8b',
        analysis: 'mixtral:8x7b'
      },
      cost: 0,  // Free, local
      latency: 'fast'
    },
    openai: {
      type: 'cloud',
      baseUrl: 'https://api.openai.com/v1',
      models: {
        embedding: 'text-embedding-3-small',
        chat: 'gpt-4o-mini',
        analysis: 'gpt-4o'
      },
      cost: 'per-token',
      latency: 'medium'
    },
    anthropic: {
      type: 'cloud',
      baseUrl: 'https://api.anthropic.com/v1',
      models: {
        chat: 'claude-sonnet-4-20250514',
        analysis: 'claude-sonnet-4-20250514'
      },
      cost: 'per-token',
      latency: 'medium'
    }
  };

  // Intelligent model routing
  async route(request: AIRequest): Promise<AIResponse> {
    const provider = this.selectProvider(request);

    try {
      return await this.providers.get(provider).execute(request);
    } catch (error) {
      // Fallback to next provider
      return await this.fallback.handle(request, error);
    }
  }

  private selectProvider(request: AIRequest): string {
    // Priority 1: Local for privacy-sensitive or frequent operations
    if (request.privacySensitive || request.type === 'embedding') {
      return 'ollama';
    }

    // Priority 2: Route by complexity
    switch (request.complexity) {
      case 'simple':
        return 'ollama';  // Fast, free
      case 'medium':
        return 'openai';  // Good balance
      case 'complex':
        return 'anthropic';  // Best reasoning
    }

    return 'ollama';  // Default to local
  }

  // Embedding service (prioritize local)
  async embed(text: string): Promise<Float32Array> {
    // Always use local embeddings for privacy
    const provider = this.providers.get('ollama');
    const response = await provider.embed(text);
    return new Float32Array(response.embedding);
  }

  // Chat/completion service
  async chat(messages: Message[], options?: ChatOptions): Promise<string> {
    const provider = this.selectProvider({
      type: 'chat',
      complexity: options?.complexity || 'medium',
      privacySensitive: options?.privacySensitive || false
    });

    const response = await this.providers.get(provider).chat(messages, options);

    // Record for cost tracking
    await this.costTracker.record(provider, response.usage);

    return response.content;
  }

  // Synthesis service (streaming)
  async *synthesize(
    notes: string[],
    topic: string
  ): AsyncGenerator<string> {
    const provider = this.selectProvider({
      type: 'analysis',
      complexity: 'complex',
      privacySensitive: false
    });

    const systemPrompt = `You are a knowledge synthesis assistant.
Analyze the provided notes and generate insights about: ${topic}

Notes to analyze:
${notes.join('\n\n---\n\n')}`;

    for await (const chunk of this.providers.get(provider).stream([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: `Generate a comprehensive synthesis of these notes regarding "${topic}"` }
    ])) {
      yield chunk;
    }
  }
}
```

---

## 5. Performance Architecture

### 5.1 Latency Targets per Operation

| Operation | Target | P50 | P99 | Strategy |
|-----------|--------|-----|-----|----------|
| **Quick Capture** | < 10ms | 5ms | 15ms | Queue + async processing |
| **Vector Search** | < 0.5ms | 0.3ms | 2ms | HNSW + memory-mapped |
| **Hybrid Search** | < 50ms | 30ms | 100ms | Parallel + merge |
| **Cache Hit** | < 1ms | 0.5ms | 3ms | LRU in-memory |
| **Graph Traversal** | < 100ms | 50ms | 200ms | Indexed paths |
| **Link Creation** | < 100ms | 80ms | 200ms | Background indexing |
| **Embedding Gen** | < 50ms | 30ms | 100ms | Local Ollama |
| **Synthesis** | Streaming | First chunk < 500ms | - | SSE streaming |
| **Context Update** | < 20ms | 10ms | 50ms | Async with prefetch |
| **Pattern Match** | < 30ms | 15ms | 60ms | Vector + filter |

### 5.2 Caching Strategy

```typescript
// Comprehensive caching strategy
const cachingStrategy = {
  // Query result caching
  queryCache: {
    // Exact match caching
    exact: {
      enabled: true,
      ttl: 3600,  // 1 hour
      maxSize: 10000,
      eviction: 'lru',
    },

    // Semantic similarity caching
    semantic: {
      enabled: true,
      ttl: 86400,  // 24 hours
      similarity: 0.95,  // Cache hit if >95% similar
      maxSize: 100000,
    },

    // Result set caching
    resultSet: {
      enabled: true,
      ttl: 1800,  // 30 minutes
      strategy: 'hash-based',
    }
  },

  // Embedding caching
  embeddingCache: {
    // Pre-computed embeddings
    precomputed: {
      enabled: true,
      storage: 'ruvector',
      updateTrigger: 'content-change',
    },

    // Query embedding cache
    queryEmbeddings: {
      enabled: true,
      ttl: 3600,
      maxSize: 5000,
    }
  },

  // Graph caching
  graphCache: {
    // Frequently accessed paths
    hotPaths: {
      enabled: true,
      ttl: 86400,
      topK: 1000,
    },

    // Subgraph cache
    subgraphs: {
      enabled: true,
      ttl: 3600,
      maxDepth: 3,
    },

    // Centrality scores
    centrality: {
      enabled: true,
      refreshInterval: 86400,  // Daily
    }
  },

  // Learning cache
  learningCache: {
    // Pattern predictions
    patterns: {
      enabled: true,
      ttl: 3600,
      confidence: 0.7,
    },

    // Recommendations
    recommendations: {
      enabled: true,
      ttl: 300,  // 5 minutes
      contextSensitive: true,
    }
  },

  // Cache invalidation
  invalidation: {
    // Content-based
    onContentChange: ['queryCache', 'embeddingCache'],

    // Graph-based
    onGraphChange: ['graphCache', 'learningCache.recommendations'],

    // Time-based
    scheduled: {
      'graphCache.centrality': '0 3 * * *',  // 3 AM daily
      'learningCache.patterns': '0 */6 * * *',  // Every 6 hours
    }
  },

  // Cache warming
  warming: {
    enabled: true,
    schedule: '0 4 * * *',  // 4 AM daily
    strategies: [
      'top-queries',      // Most frequent queries
      'recent-access',    // Recently accessed notes
      'high-importance',  // High importance notes
    ]
  }
};
```

### 5.3 Batch Processing

```typescript
// Batch processing for efficiency
class BatchProcessor {
  private queues: Map<string, BatchQueue>;
  private config: BatchConfig = {
    maxBatchSize: 100,
    maxWaitTime: 500,  // ms
    concurrency: 4,
  };

  // Embedding batch processor
  async batchEmbed(texts: string[]): Promise<Float32Array[]> {
    // Group into optimal batches
    const batches = this.createBatches(texts, 32);  // 32 per batch

    // Process batches in parallel
    const results = await Promise.all(
      batches.map(batch => this.embedBatch(batch))
    );

    return results.flat();
  }

  // Index batch processor
  async batchIndex(notes: Note[]): Promise<void> {
    // Generate embeddings in batch
    const contents = notes.map(n => n.content);
    const embeddings = await this.batchEmbed(contents);

    // Batch insert to vector store
    const entries = notes.map((note, i) => ({
      id: note.id,
      vector: embeddings[i],
      metadata: note.metadata
    }));

    await this.vectorStore.insertBatch(entries);

    // Batch update graph
    const graphUpdates = notes.map(note => ({
      entity: this.noteToEntity(note),
      relations: this.extractRelations(note)
    }));

    await this.graphStore.batchUpdate(graphUpdates);
  }

  // Search batch processor (for multiple queries)
  async batchSearch(queries: Query[]): Promise<SearchResult[][]> {
    // Generate query embeddings in batch
    const queryTexts = queries.map(q => q.text);
    const embeddings = await this.batchEmbed(queryTexts);

    // Parallel search execution
    const results = await Promise.all(
      queries.map((query, i) =>
        this.search({
          embedding: embeddings[i],
          filters: query.filters,
          k: query.k
        })
      )
    );

    return results;
  }

  // Background processing queue
  async queueBackgroundTask(task: BackgroundTask): Promise<void> {
    const queue = this.queues.get(task.type);

    queue.add(task);

    // Process when batch is full or timeout
    if (queue.size >= this.config.maxBatchSize || queue.age > this.config.maxWaitTime) {
      await this.processBatch(queue);
    }
  }

  private async processBatch(queue: BatchQueue): Promise<void> {
    const tasks = queue.drain();

    switch (queue.type) {
      case 'index':
        await this.batchIndex(tasks.map(t => t.data));
        break;
      case 'graph':
        await this.graphStore.batchUpdate(tasks.map(t => t.data));
        break;
      case 'learn':
        await this.learningEngine.batchLearn(tasks.map(t => t.data));
        break;
    }
  }
}
```

---

## 6. Security Architecture

### 6.1 Local-First Privacy

```typescript
// Privacy-preserving architecture
const privacyArchitecture = {
  // Data residency
  dataResidency: {
    // All primary data stays local
    local: [
      'notes',
      'embeddings',
      'graph',
      'patterns',
      'trajectories',
    ],

    // Optional cloud sync (encrypted)
    cloudSync: {
      enabled: false,  // Opt-in
      encryption: 'aes-256-gcm',
      keyManagement: 'local',  // Keys never leave device
    }
  },

  // Processing location
  processing: {
    // Always local
    local: [
      'embedding-generation',
      'vector-search',
      'graph-queries',
      'pattern-matching',
    ],

    // Optionally cloud (with consent)
    cloudOptional: [
      'synthesis',      // For complex synthesis
      'advanced-nlp',   // For entity extraction
    ],

    // Privacy measures for cloud
    cloudPrivacy: {
      anonymization: true,
      minimalData: true,
      noStorage: true,
    }
  },

  // AI service selection
  aiServices: {
    // Prefer local models
    default: 'ollama',

    // Cloud only for explicit user actions
    cloudTriggers: [
      'explicit-synthesis-request',
      'advanced-analysis',
    ],

    // Never send to cloud
    neverCloud: [
      'personal-notes',
      'private-tags',
      'access-patterns',
    ]
  }
};
```

### 6.2 Encryption at Rest

```typescript
// Encryption configuration
const encryptionConfig = {
  // File encryption
  files: {
    algorithm: 'aes-256-gcm',
    keyDerivation: 'argon2id',
    keyStorage: 'system-keychain',  // OS-level protection
  },

  // Database encryption
  databases: {
    // SQLite encryption
    sqlite: {
      cipher: 'sqlcipher',
      kdf: 'pbkdf2-hmac-sha512',
      iterations: 256000,
    },

    // Vector store encryption
    vectors: {
      atRest: true,
      algorithm: 'aes-256-ctr',
    },

    // Graph database encryption
    graph: {
      atRest: true,
      algorithm: 'aes-256-gcm',
    }
  },

  // Key management
  keys: {
    // Master key
    master: {
      derivation: 'argon2id',
      salt: 'random-per-user',
      storage: 'system-keychain',
    },

    // Data encryption keys
    dek: {
      perDatabase: true,
      rotation: '90-days',
      encrypted: 'master-key',
    },

    // Backup keys
    backup: {
      type: 'recovery-key',
      format: '24-word-mnemonic',
      storage: 'user-responsibility',
    }
  },

  // Cache encryption
  cache: {
    l1Memory: false,  // Encrypted in-process memory
    l2Redis: true,    // Encrypted at rest
    l3Disk: true,     // Encrypted files
  }
};

// Encryption implementation
class EncryptionService {
  private masterKey: Buffer;
  private dekCache: Map<string, Buffer>;

  async encrypt(data: Buffer, keyId: string): Promise<EncryptedData> {
    const dek = await this.getOrCreateDEK(keyId);
    const iv = crypto.randomBytes(12);

    const cipher = crypto.createCipheriv('aes-256-gcm', dek, iv);
    const encrypted = Buffer.concat([
      cipher.update(data),
      cipher.final()
    ]);
    const authTag = cipher.getAuthTag();

    return {
      ciphertext: encrypted,
      iv,
      authTag,
      keyId,
      algorithm: 'aes-256-gcm'
    };
  }

  async decrypt(encrypted: EncryptedData): Promise<Buffer> {
    const dek = await this.getDEK(encrypted.keyId);

    const decipher = crypto.createDecipheriv(
      'aes-256-gcm',
      dek,
      encrypted.iv
    );
    decipher.setAuthTag(encrypted.authTag);

    return Buffer.concat([
      decipher.update(encrypted.ciphertext),
      decipher.final()
    ]);
  }
}
```

### 6.3 Access Control

```typescript
// Access control configuration
const accessControl = {
  // Authentication
  authentication: {
    // Local authentication
    local: {
      type: 'password',
      hashing: 'argon2id',
      biometric: true,  // If available
    },

    // Session management
    sessions: {
      timeout: '30-minutes-inactive',
      maxConcurrent: 1,
      deviceBinding: true,
    }
  },

  // Authorization
  authorization: {
    // Resource-level permissions
    resources: {
      notes: ['read', 'write', 'delete', 'share'],
      graphs: ['read', 'write'],
      patterns: ['read'],  // System-managed
      settings: ['read', 'write'],
    },

    // MCP tool permissions
    tools: {
      capture: 'write',
      search: 'read',
      link: 'write',
      delete: 'delete',
      synthesize: 'read',
      export: 'read',
    }
  },

  // Audit logging
  audit: {
    enabled: true,
    events: [
      'authentication',
      'authorization-failure',
      'data-access',
      'data-modification',
      'export',
      'share',
    ],
    retention: '90-days',
    encryption: true,
  },

  // Data sharing controls
  sharing: {
    // Export controls
    export: {
      formats: ['markdown', 'json'],
      stripPrivate: true,  // Remove private tags/metadata
      approval: 'user-confirmation',
    },

    // Sync controls
    sync: {
      enabled: false,  // Opt-in
      encryption: 'end-to-end',
      selective: true,  // Choose what to sync
    }
  }
};
```

---

## 7. Deployment Architecture

### 7.1 Local Deployment

```yaml
# Local deployment configuration
deployment:
  type: local

  # Core services
  services:
    # MCP Server (main process)
    mcp-server:
      runtime: node
      entry: ./dist/mcp-server.js
      port: null  # stdio transport

    # Vector database
    vector-db:
      engine: ruvector
      storage: ./data/vectors
      memory_map: true

    # Graph database
    graph-db:
      engine: typedb
      storage: ./data/graph
      port: 1729

    # Cache
    cache:
      engine: valkey
      port: 6379
      maxmemory: 256mb

    # Embedding service
    embeddings:
      engine: ollama
      model: nomic-embed-text
      port: 11434

  # Storage paths
  storage:
    base: ~/.pkm-enhanced
    vectors: ${base}/vectors
    graph: ${base}/graph
    cache: ${base}/cache
    logs: ${base}/logs
    backups: ${base}/backups

  # Resource limits
  resources:
    memory: 2GB
    cpu: 4
    disk: 10GB

  # Startup sequence
  startup:
    - ollama  # Start embedding service first
    - valkey  # Then cache
    - typedb  # Then graph
    - mcp-server  # Finally MCP server

  # Health checks
  health:
    interval: 30s
    timeout: 5s
    retries: 3
```

### 7.2 Cloud Sync Options

```typescript
// Cloud sync architecture (optional)
const cloudSyncConfig = {
  // Sync providers
  providers: {
    // Self-hosted options
    selfHosted: {
      nextcloud: {
        type: 'webdav',
        encryption: 'client-side',
      },
      syncthing: {
        type: 'p2p',
        encryption: 'end-to-end',
      }
    },

    // Commercial options
    commercial: {
      icloud: {
        platform: 'apple',
        encryption: 'platform',
      },
      dropbox: {
        type: 'cloud',
        encryption: 'client-side',
      }
    }
  },

  // Sync strategy
  strategy: {
    // What to sync
    include: [
      'notes',           // Markdown files
      'metadata.db',     // SQLite metadata
      'vectors.idx',     // Vector index
      'graph.db',        // Graph database
    ],

    // What to exclude
    exclude: [
      'cache',
      'logs',
      'temp',
    ],

    // Conflict resolution
    conflicts: {
      strategy: 'latest-wins',
      backup: true,  // Keep conflicting versions
    },

    // Delta sync
    delta: {
      enabled: true,
      algorithm: 'rsync',
    }
  },

  // Encryption
  encryption: {
    // Client-side encryption before upload
    clientSide: {
      enabled: true,
      algorithm: 'aes-256-gcm',
      keyDerivation: 'argon2id',
    },

    // Key management
    keys: {
      storage: 'local-only',  // Never upload keys
      backup: 'user-mnemonic',
    }
  }
};

// Sync implementation
class CloudSync {
  private provider: SyncProvider;
  private encryptor: EncryptionService;
  private differ: DeltaDiff;

  async sync(): Promise<SyncResult> {
    // Get local changes
    const localChanges = await this.getLocalChanges();

    // Get remote changes
    const remoteChanges = await this.provider.getChanges();

    // Resolve conflicts
    const resolved = await this.resolveConflicts(localChanges, remoteChanges);

    // Upload local changes (encrypted)
    for (const change of resolved.toUpload) {
      const encrypted = await this.encryptor.encrypt(change.data);
      const delta = await this.differ.createDelta(change);
      await this.provider.upload(change.path, delta);
    }

    // Download remote changes (decrypt)
    for (const change of resolved.toDownload) {
      const delta = await this.provider.download(change.path);
      const data = await this.differ.applyDelta(delta);
      const decrypted = await this.encryptor.decrypt(data);
      await this.applyChange(change.path, decrypted);
    }

    return {
      uploaded: resolved.toUpload.length,
      downloaded: resolved.toDownload.length,
      conflicts: resolved.conflicts.length
    };
  }
}
```

### 7.3 Multi-Device Support

```typescript
// Multi-device architecture
const multiDeviceConfig = {
  // Device registration
  devices: {
    // Device identity
    identity: {
      id: 'uuid',
      name: 'user-defined',
      type: 'desktop|mobile|tablet',
      lastSeen: 'timestamp',
    },

    // Capability declaration
    capabilities: {
      processing: 'full|limited',
      storage: 'full|partial',
      offline: 'full|limited',
    },

    // Device-specific settings
    settings: {
      syncEnabled: true,
      syncFrequency: 'realtime|hourly|daily',
      cacheSize: '1GB',
    }
  },

  // Sync topology
  topology: {
    // Primary device (full data)
    primary: {
      hasFullData: true,
      isSourceOfTruth: true,
    },

    // Secondary devices
    secondary: {
      syncSubset: true,
      subsetRules: {
        recentDays: 30,
        importanceThreshold: 0.5,
        specificFolders: [],
      }
    },

    // Sync relationships
    sync: {
      type: 'hub-spoke',  // Primary is hub
      realtime: 'via-provider',
      conflictResolution: 'timestamp',
    }
  },

  // Offline support
  offline: {
    // Data available offline
    available: {
      notes: 'subset-or-full',
      vectors: 'compressed',
      graph: 'subset',
      patterns: 'cached',
    },

    // Offline operations
    operations: {
      capture: true,
      search: true,
      link: true,
      synthesize: false,  // Requires AI
    },

    // Sync on reconnect
    reconnect: {
      strategy: 'queue-based',
      priority: 'user-edits-first',
    }
  },

  // Cross-device features
  features: {
    // Handoff
    handoff: {
      enabled: true,
      context: ['activeNote', 'searchQuery', 'selection'],
    },

    // Notifications
    notifications: {
      syncConflicts: true,
      newInsights: true,
      reminders: true,
    },

    // Shared clipboard
    clipboard: {
      enabled: true,
      encrypted: true,
    }
  }
};
```

---

## 8. Technology Stack

### 8.1 Core Technologies

```yaml
technology_stack:
  # Core runtime
  core:
    primary: "Rust"
    secondary: "TypeScript"
    reason: "Performance-critical in Rust, application logic in TypeScript"

  # Vector database
  vector:
    engine: "ruvector"
    version: "0.1.0+"
    features:
      - "HNSW indexing"
      - "Product quantization"
      - "MCP integration"
      - "Self-learning (causal memory, skill library)"
    bindings:
      - "Node.js (NAPI-RS)"
      - "WASM (browser)"
      - "Rust native"

  # Graph database
  graph:
    primary: "TypeDB"
    alternative: "Neo4j"
    version: "2.x"
    features:
      - "Hypergraph support"
      - "Inference rules"
      - "Schema validation"
    selection_criteria:
      typedb: "Complex reasoning, schema validation"
      neo4j: "Simpler setup, better tooling"

  # Cache
  cache:
    engine: "Redis/Valkey"
    version: "7.x"
    features:
      - "In-memory speed"
      - "Persistence options"
      - "Pub/sub for events"
    alternative: "DragonflyDB"

  # Metadata storage
  metadata:
    engine: "SQLite"
    version: "3.40+"
    features:
      - "FTS5 for full-text search"
      - "JSON functions"
      - "Encryption (SQLCipher)"

  # Embeddings
  embeddings:
    local:
      engine: "Ollama"
      model: "nomic-embed-text"
      dimensions: 768
      features:
        - "Local processing"
        - "Privacy-preserving"
        - "Fast (< 50ms)"
    cloud:
      engine: "OpenAI"
      model: "text-embedding-3-small"
      dimensions: 1536
      use_case: "Optional, user consent"

  # MCP framework
  mcp:
    sdk: "@modelcontextprotocol/sdk"
    version: "latest"
    transport:
      - "stdio (Obsidian)"
      - "HTTP (API)"

  # Frontend
  frontend:
    obsidian:
      api: "obsidian (npm)"
      version: "1.4.0+"
    web:
      framework: "Svelte"
      bundler: "Vite"
      wasm: "ruvector-wasm"

  # AI services
  ai:
    local:
      engine: "Ollama"
      models:
        - "llama3.1:8b"
        - "mixtral:8x7b"
    cloud:
      providers:
        - "Anthropic (Claude)"
        - "OpenAI (GPT)"
      routing: "complexity-based"

  # Build tools
  build:
    rust: "cargo"
    typescript: "npm/pnpm"
    bundler: "esbuild"
    testing:
      - "vitest (TypeScript)"
      - "cargo test (Rust)"
```

### 8.2 Dependency Matrix

```yaml
dependencies:
  # Rust crates
  rust:
    # Core
    ruvector-core: "0.1.0"
    tokio: "1.0"
    serde: "1.0"
    serde_json: "1.0"

    # Vector operations
    ndarray: "0.15"
    rayon: "1.0"

    # Persistence
    rocksdb: "0.21"

    # Networking
    quinn: "0.10"  # QUIC

    # Crypto
    ring: "0.17"
    argon2: "0.5"

  # Node.js packages
  node:
    # MCP
    "@modelcontextprotocol/sdk": "^1.0.0"

    # Obsidian
    "obsidian": "^1.4.0"

    # Database clients
    "better-sqlite3": "^9.0.0"
    "ioredis": "^5.0.0"

    # AI
    "@anthropic-ai/sdk": "^0.20.0"
    "openai": "^4.0.0"

    # Utilities
    "zod": "^3.0.0"  # Validation
    "gray-matter": "^4.0.0"  # Frontmatter
    "lru-cache": "^10.0.0"

  # Optional
  optional:
    # Graph database drivers
    "typedb-client": "^2.0.0"
    "neo4j-driver": "^5.0.0"

    # Cloud sync
    "webdav": "^5.0.0"
```

### 8.3 Performance Comparison

```
+------------------+------------+-------------+--------------+
| Component        | This Stack | Alternative | Improvement  |
+------------------+------------+-------------+--------------+
| Vector Search    | < 0.5ms    | 10-50ms     | 20-100x      |
|                  | (ruvector) | (ChromaDB)  |              |
+------------------+------------+-------------+--------------+
| Embedding Gen    | < 50ms     | 100-500ms   | 2-10x        |
|                  | (Ollama)   | (API)       |              |
+------------------+------------+-------------+--------------+
| Graph Query      | < 100ms    | 200-500ms   | 2-5x         |
|                  | (TypeDB)   | (Generic)   |              |
+------------------+------------+-------------+--------------+
| Cache Access     | < 1ms      | 5-10ms      | 5-10x        |
|                  | (Valkey)   | (Disk)      |              |
+------------------+------------+-------------+--------------+
| Memory Usage     | 800MB      | 2-4GB       | 3-5x less    |
|                  | (quant)    | (float32)   |              |
+------------------+------------+-------------+--------------+
```

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up Rust + TypeScript project structure
- [ ] Implement MCP server with basic tools (capture, search)
- [ ] Integrate ruvector for vector storage
- [ ] Create Obsidian plugin skeleton
- [ ] Basic file sync between Obsidian and vector store

### Phase 2: Core Features (Weeks 3-4)
- [ ] Implement hybrid search (vector + FTS)
- [ ] Add graph database integration (TypeDB)
- [ ] Build knowledge graph from links
- [ ] Add multi-level caching
- [ ] Implement embedding generation pipeline

### Phase 3: Intelligence (Weeks 5-6)
- [ ] Build pattern recognition engine
- [ ] Implement confidence scoring
- [ ] Add trajectory storage and learning
- [ ] Create recommendation system
- [ ] Implement auto-linking

### Phase 4: Polish (Weeks 7-8)
- [ ] Optimize performance (< 50ms search)
- [ ] Add synthesis with streaming
- [ ] Implement full Obsidian UI components
- [ ] Add encryption and security
- [ ] Testing and documentation

---

## 10. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Search latency P50 | < 30ms | Prometheus metrics |
| Search latency P99 | < 100ms | Prometheus metrics |
| Capture latency | < 10ms | Event timing |
| Cache hit rate | > 80% | Cache metrics |
| Recall @ k=10 | > 95% | Benchmark tests |
| Learning improvement | > 20% | A/B testing |
| User satisfaction | > 4.5/5 | User surveys |

---

## Appendix A: Configuration Examples

### A.1 MCP Server Configuration

```json
{
  "server": {
    "name": "pkm-enhanced",
    "version": "1.0.0",
    "transport": "stdio"
  },
  "vector": {
    "dimensions": 384,
    "storagePath": "./data/vectors",
    "hnsw": {
      "m": 16,
      "efConstruction": 200,
      "efSearch": 100
    },
    "quantization": {
      "enabled": true,
      "type": "product",
      "subvectors": 8,
      "bits": 8
    }
  },
  "graph": {
    "engine": "typedb",
    "host": "localhost",
    "port": 1729,
    "database": "pkm"
  },
  "cache": {
    "redis": {
      "host": "localhost",
      "port": 6379
    },
    "ttl": {
      "queries": 3600,
      "embeddings": 86400,
      "patterns": 3600
    }
  },
  "learning": {
    "enabled": true,
    "minPatternFrequency": 3,
    "confidenceThreshold": 0.7,
    "trajectoryRetention": 90
  },
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "host": "http://localhost:11434"
  }
}
```

### A.2 Obsidian Plugin Configuration

```json
{
  "mcpServer": {
    "command": "npx",
    "args": ["pkm-enhanced-mcp", "start"],
    "timeout": 30000
  },
  "sync": {
    "enabled": true,
    "debounceMs": 2000,
    "batchSize": 50
  },
  "ui": {
    "showConnectionsPane": true,
    "showConfidenceIndicators": true,
    "quickCaptureHotkey": "Ctrl+Shift+N"
  },
  "learning": {
    "trackAccess": true,
    "showRecommendations": true,
    "autoLink": {
      "enabled": true,
      "minConfidence": 0.8
    }
  },
  "privacy": {
    "localOnly": true,
    "cloudAI": false
  }
}
```

---

## Appendix B: API Reference

### B.1 MCP Tool Signatures

```typescript
// Full API reference for MCP tools
interface PKMToolAPI {
  // Capture
  "pkm/capture": (params: {
    content: string;
    source: "manual" | "voice" | "image" | "import";
    context?: {
      activeNote?: string;
      selectedText?: string;
      tags?: string[];
    };
  }) => Promise<{ id: string; processed: boolean }>;

  // Search
  "pkm/search": (params: {
    query: string;
    k?: number;
    mode?: "semantic" | "keyword" | "hybrid" | "graph";
    filters?: {
      tags?: string[];
      dateRange?: { start: string; end: string };
      noteType?: string;
    };
    includeContext?: boolean;
  }) => Promise<SearchResult[]>;

  // Graph
  "pkm/link": (params: {
    sourceId: string;
    targetId: string;
    relationship: RelationType;
    bidirectional?: boolean;
    confidence?: number;
  }) => Promise<{ edgeId: string }>;

  // Learning
  "pkm/learn_pattern": (params: {
    patternType: "search" | "link" | "workflow" | "synthesis";
    context: Record<string, any>;
    outcome: "success" | "partial" | "failure";
    trajectory?: TrajectoryStep[];
  }) => Promise<{ patternId: string; confidence: number }>;

  // Synthesis
  "pkm/synthesize": (params: {
    noteIds: string[];
    topic?: string;
    outputFormat?: "summary" | "outline" | "essay" | "questions";
    depth?: "brief" | "standard" | "comprehensive";
  }) => AsyncGenerator<string>;
}
```

---

*Architecture Document Version: 1.0.0*
*Created: 2025-11-23*
*SPARC Phase: Architecture*
