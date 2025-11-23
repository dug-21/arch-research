# SPARC Pseudocode Specification: PKM 2035 System Algorithms

## Document Overview

**Phase**: Pseudocode (Phase 2 of SPARC Methodology)
**Purpose**: Translate 2035 PKM specifications into clear, efficient algorithmic logic
**Version**: 1.0.0
**Date**: 2025-11-23

---

## Performance Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Capture Latency | < 10ms | Zero-friction user experience |
| Search Latency (p50) | < 50ms | Real-time interaction |
| Search Latency (p99) | < 200ms | Consistent performance |
| Throughput | 5,000+ ops/sec | Scale to large knowledge bases |
| Memory per 100K vectors | < 200MB | Edge deployment feasibility |
| Recall @ k=10 | > 95% | High accuracy requirements |

---

## Algorithm 1: Knowledge Capture Pipeline

### 1.1 Main Algorithm

```
ALGORITHM: CaptureKnowledge
INPUT: input (CaptureInput)
OUTPUT: captureId (string)

DATA STRUCTURES:
    CaptureInput:
        content: string
        source: string (optional)
        metadata: object (optional)

    CaptureQueueItem:
        id: string
        content: string
        source: string
        timestamp: number
        priority: number

    ProcessedNote:
        id: string
        content: string
        embedding: Float32Array
        entities: Entity[]
        tags: string[]
        summary: string
        relationships: Edge[]

BEGIN
    // Phase 1: Immediate Capture (< 10ms target)
    captureId <- GenerateUUID()
    timestamp <- GetCurrentTimeMillis()

    // Calculate priority based on context
    priority <- CalculatePriority(input)

    // Queue for immediate return (non-blocking)
    queueItem <- {
        id: captureId,
        content: input.content,
        source: input.source OR "manual",
        timestamp: timestamp,
        priority: priority
    }

    // Async queue insertion (< 1ms)
    CaptureQueue.push(queueItem)

    // Schedule background processing
    ProcessQueue.schedule(captureId, priority)

    // Return immediately for fast UX
    RETURN captureId
END

SUBROUTINE: CalculatePriority
INPUT: input (CaptureInput)
OUTPUT: priority (number 1-10)

BEGIN
    priority <- 5  // Default medium

    // Boost for structured content
    IF ContainsCodeBlock(input.content) THEN
        priority <- priority + 2
    END IF

    // Boost for links/references
    IF ContainsWikiLinks(input.content) THEN
        priority <- priority + 1
    END IF

    // Boost for explicit tags
    IF input.metadata.tags EXISTS AND LENGTH(input.metadata.tags) > 0 THEN
        priority <- priority + 1
    END IF

    // Cap at maximum
    RETURN MIN(priority, 10)
END
```

### 1.2 Background Processing Pipeline

```
ALGORITHM: ProcessCapturedItem
INPUT: captureId (string)
OUTPUT: success (boolean)

BEGIN
    // Retrieve from capture queue
    item <- CaptureQueue.get(captureId)

    IF item IS NULL THEN
        LogError("Capture item not found: " + captureId)
        RETURN false
    END IF

    // Phase 2: Parallel Processing
    // Launch all processing tasks concurrently
    PARALLEL DO
        embedding <- GenerateEmbedding(item.content)
        entities <- ExtractEntities(item.content)
        tags <- AutoTagContent(item.content, entities)
        summary <- GenerateSummary(item.content)
    END PARALLEL

    // Phase 3: Store Processed Note
    processedNote <- {
        id: captureId,
        content: item.content,
        source: item.source,
        timestamp: item.timestamp,
        embedding: embedding,
        entities: entities,
        tags: tags,
        summary: summary,
        confidence: 0.80,  // Initial confidence
        accessCount: 0,
        lastAccessed: item.timestamp
    }

    // Insert into vector store
    VectorStore.insert(captureId, embedding, {
        title: ExtractTitle(item.content),
        tags: tags,
        entities: entities,
        created: item.timestamp
    })

    // Store full note
    NoteStore.save(processedNote)

    // Phase 4: Discover Relationships (async)
    RelationshipQueue.schedule(captureId)

    RETURN true
END

SUBROUTINE: GenerateEmbedding
INPUT: content (string)
OUTPUT: embedding (Float32Array[384])

BEGIN
    // Check embedding cache first
    contentHash <- HashContent(content)
    cached <- EmbeddingCache.get(contentHash)

    IF cached EXISTS THEN
        RETURN cached
    END IF

    // Chunk long content
    IF LENGTH(content) > 8192 THEN
        chunks <- ChunkContent(content, maxSize=8192, overlap=200)
        embeddings <- []

        FOR EACH chunk IN chunks DO
            emb <- EmbeddingModel.encode(chunk)
            embeddings.append(emb)
        END FOR

        // Mean pooling for final embedding
        embedding <- MeanPool(embeddings)
    ELSE
        embedding <- EmbeddingModel.encode(content)
    END IF

    // Cache result
    EmbeddingCache.set(contentHash, embedding, ttl=3600)

    RETURN embedding
END

SUBROUTINE: ExtractEntities
INPUT: content (string)
OUTPUT: entities (Entity[])

BEGIN
    entities <- []

    // Named Entity Recognition
    nerResults <- NERModel.extract(content)

    FOR EACH result IN nerResults DO
        entity <- {
            name: result.text,
            type: result.label,  // PERSON, ORG, CONCEPT, etc.
            start: result.start,
            end: result.end,
            confidence: result.score
        }
        entities.append(entity)
    END FOR

    // Extract explicit [[wiki links]]
    wikiLinks <- ExtractWikiLinks(content)
    FOR EACH link IN wikiLinks DO
        entity <- {
            name: link.target,
            type: "REFERENCE",
            start: link.start,
            end: link.end,
            confidence: 1.0
        }
        entities.append(entity)
    END FOR

    // Deduplicate by name (keep highest confidence)
    entities <- DeduplicateEntities(entities)

    RETURN entities
END

SUBROUTINE: AutoTagContent
INPUT: content (string), entities (Entity[])
OUTPUT: tags (string[])

BEGIN
    tags <- SET()

    // Extract explicit #tags from content
    hashTags <- ExtractHashTags(content)
    FOR EACH tag IN hashTags DO
        tags.add(NormalizeTag(tag))
    END FOR

    // Generate tags from entities
    FOR EACH entity IN entities DO
        IF entity.type == "CONCEPT" AND entity.confidence > 0.7 THEN
            tags.add(NormalizeTag(entity.name))
        END IF
    END FOR

    // Semantic tag suggestion (top-k similar existing tags)
    embedding <- GenerateEmbedding(content)
    similarTags <- TagIndex.search(embedding, k=5)

    FOR EACH tagMatch IN similarTags DO
        IF tagMatch.similarity > 0.75 THEN
            tags.add(tagMatch.tag)
        END IF
    END FOR

    RETURN ARRAY(tags)
END
```

### 1.3 Complexity Analysis

```
ANALYSIS: Knowledge Capture Pipeline

Time Complexity:
    CaptureKnowledge (synchronous path):
        - UUID generation: O(1)
        - Priority calculation: O(n) where n = content length
        - Queue insertion: O(1) amortized
        - Total: O(n) but constant in practice due to content limits

    ProcessCapturedItem (background):
        - Embedding generation: O(n * d) where d = model dimensions
        - Entity extraction: O(n)
        - Auto-tagging: O(n + k) where k = tag corpus size
        - Summary generation: O(n)
        - Vector store insertion: O(log m) where m = index size
        - Total: O(n * d) dominated by embedding

Space Complexity:
    - Input buffer: O(n)
    - Embedding: O(d) = O(384) = O(1)
    - Entities: O(e) where e = entity count
    - Tags: O(t) where t = tag count
    - Queue storage: O(q) where q = queue depth
    - Total: O(n + q)

Performance Optimizations:
    1. Immediate return pattern for < 10ms capture
    2. Content-addressed embedding cache reduces redundant computation
    3. Parallel processing of independent tasks
    4. Batch queue processing during idle periods
    5. Priority-based scheduling for important content
```

---

## Algorithm 2: Semantic Search Algorithm

### 2.1 Hybrid Search Engine

```
ALGORITHM: SemanticSearch
INPUT: query (string), options (SearchOptions)
OUTPUT: results (SearchResult[])

DATA STRUCTURES:
    SearchOptions:
        k: number (default: 10)
        filter: FilterObject (optional)
        includeMetadata: boolean (default: true)
        hybridWeight: number (0-1, default: 0.7)
        mmrLambda: number (0-1, default: 0.5)

    SearchResult:
        id: string
        content: string
        score: number
        metadata: object
        highlights: string[]

CONSTANTS:
    VECTOR_WEIGHT = 0.7
    KEYWORD_WEIGHT = 0.2
    GRAPH_WEIGHT = 0.1
    CACHE_TTL = 300  // 5 minutes

BEGIN
    // Check search cache first
    cacheKey <- HashSearch(query, options)
    cached <- SearchCache.get(cacheKey)

    IF cached EXISTS AND NOT options.bypassCache THEN
        RecordCacheHit(query)
        RETURN cached
    END IF

    // Phase 1: Query Preprocessing
    normalizedQuery <- NormalizeQuery(query)
    queryEmbedding <- GenerateEmbedding(normalizedQuery)
    queryTokens <- Tokenize(normalizedQuery)

    // Phase 2: Multi-Source Search (Parallel)
    PARALLEL DO
        vectorResults <- VectorSearch(queryEmbedding, options)
        keywordResults <- KeywordSearch(queryTokens, options)
        graphResults <- GraphSearch(normalizedQuery, options)
    END PARALLEL

    // Phase 3: Hybrid Score Fusion
    fusedResults <- FuseResults(
        vectorResults,
        keywordResults,
        graphResults,
        options.hybridWeight
    )

    // Phase 4: Apply MMR for Diversity
    diverseResults <- ApplyMMR(
        fusedResults,
        queryEmbedding,
        options.k,
        options.mmrLambda
    )

    // Phase 5: Re-rank and Format
    finalResults <- []
    FOR EACH result IN diverseResults DO
        formatted <- {
            id: result.id,
            content: TruncateContent(result.content, 500),
            score: result.finalScore,
            metadata: result.metadata IF options.includeMetadata,
            highlights: GenerateHighlights(result.content, queryTokens)
        }
        finalResults.append(formatted)
    END FOR

    // Cache results
    SearchCache.set(cacheKey, finalResults, ttl=CACHE_TTL)

    // Record for learning
    RecordSearchQuery(query, finalResults)

    RETURN finalResults
END
```

### 2.2 Vector Search with HNSW

```
SUBROUTINE: VectorSearch
INPUT: queryEmbedding (Float32Array), options (SearchOptions)
OUTPUT: results (VectorResult[])

BEGIN
    // Apply pre-filters to reduce search space
    filterMask <- NULL
    IF options.filter EXISTS THEN
        filterMask <- BuildFilterMask(options.filter)
    END IF

    // HNSW search parameters
    efSearch <- CalculateEfSearch(options.k)

    // Perform approximate nearest neighbor search
    rawResults <- HNSWIndex.search(
        queryEmbedding,
        k = options.k * 3,  // Over-fetch for re-ranking
        efSearch = efSearch,
        filter = filterMask
    )

    // Convert distances to similarity scores
    results <- []
    FOR EACH result IN rawResults DO
        // Cosine distance to similarity
        similarity <- 1 - result.distance

        results.append({
            id: result.id,
            score: similarity,
            metadata: result.metadata,
            embedding: result.vector
        })
    END FOR

    RETURN results
END

SUBROUTINE: CalculateEfSearch
INPUT: k (number)
OUTPUT: efSearch (number)

BEGIN
    // Dynamic ef based on k for recall/speed tradeoff
    // Higher k needs higher ef for good recall
    baseEf <- 100
    scaleFactor <- CEILING(k / 10)

    RETURN MIN(baseEf * scaleFactor, 500)
END
```

### 2.3 Maximal Marginal Relevance (MMR)

```
SUBROUTINE: ApplyMMR
INPUT: candidates (Result[]), queryEmbedding (Float32Array), k (number), lambda (number)
OUTPUT: selected (Result[])

BEGIN
    selected <- []
    remaining <- COPY(candidates)

    WHILE LENGTH(selected) < k AND LENGTH(remaining) > 0 DO
        bestScore <- -INFINITY
        bestIdx <- -1

        FOR i <- 0 TO LENGTH(remaining) - 1 DO
            candidate <- remaining[i]

            // Relevance to query
            relevance <- CosineSimilarity(candidate.embedding, queryEmbedding)

            // Maximum similarity to already selected
            maxSimilarity <- 0
            FOR EACH sel IN selected DO
                sim <- CosineSimilarity(candidate.embedding, sel.embedding)
                maxSimilarity <- MAX(maxSimilarity, sim)
            END FOR

            // MMR score balances relevance and diversity
            mmrScore <- lambda * relevance - (1 - lambda) * maxSimilarity

            IF mmrScore > bestScore THEN
                bestScore <- mmrScore
                bestIdx <- i
            END IF
        END FOR

        // Add best candidate and remove from remaining
        selected.append(remaining[bestIdx])
        remaining.remove(bestIdx)
    END WHILE

    RETURN selected
END
```

### 2.4 Hybrid Score Fusion

```
SUBROUTINE: FuseResults
INPUT: vectorResults, keywordResults, graphResults, hybridWeight
OUTPUT: fusedResults (FusedResult[])

BEGIN
    // Create unified result map
    resultMap <- MAP()

    // Process vector results
    FOR EACH result IN vectorResults DO
        IF NOT resultMap.has(result.id) THEN
            resultMap.set(result.id, {
                id: result.id,
                vectorScore: 0,
                keywordScore: 0,
                graphScore: 0,
                metadata: result.metadata,
                embedding: result.embedding
            })
        END IF
        resultMap.get(result.id).vectorScore <- result.score
    END FOR

    // Process keyword results
    maxKeywordScore <- MAX(keywordResults.map(r => r.score))
    FOR EACH result IN keywordResults DO
        IF NOT resultMap.has(result.id) THEN
            resultMap.set(result.id, {
                id: result.id,
                vectorScore: 0,
                keywordScore: 0,
                graphScore: 0,
                metadata: result.metadata
            })
        END IF
        // Normalize keyword score to 0-1
        normalizedScore <- result.score / maxKeywordScore
        resultMap.get(result.id).keywordScore <- normalizedScore
    END FOR

    // Process graph results
    FOR EACH result IN graphResults DO
        IF NOT resultMap.has(result.id) THEN
            resultMap.set(result.id, {
                id: result.id,
                vectorScore: 0,
                keywordScore: 0,
                graphScore: 0,
                metadata: result.metadata
            })
        END IF
        resultMap.get(result.id).graphScore <- result.score
    END FOR

    // Calculate final fused scores
    fusedResults <- []
    FOR EACH entry IN resultMap.values() DO
        finalScore <- (
            VECTOR_WEIGHT * entry.vectorScore +
            KEYWORD_WEIGHT * entry.keywordScore +
            GRAPH_WEIGHT * entry.graphScore
        )

        entry.finalScore <- finalScore
        fusedResults.append(entry)
    END FOR

    // Sort by final score descending
    fusedResults.sortByDescending(r => r.finalScore)

    RETURN fusedResults
END
```

### 2.5 Complexity Analysis

```
ANALYSIS: Semantic Search Algorithm

Time Complexity:
    SemanticSearch overall:
        - Query preprocessing: O(q) where q = query length
        - Embedding generation: O(q * d)
        - Tokenization: O(q)

    VectorSearch (HNSW):
        - Search: O(k * log(n)) where n = index size
        - With filter: O(k * log(n) + f) where f = filter evaluation

    KeywordSearch (BM25):
        - Inverted index lookup: O(t * log(n)) where t = query terms
        - Scoring: O(t * d_avg) where d_avg = avg matching docs

    GraphSearch:
        - Query to entities: O(q)
        - Graph traversal: O(e + r) where e = entities, r = relations

    FuseResults:
        - Map building: O(v + k + g) where v,k,g = result counts
        - Score calculation: O(v + k + g)
        - Sorting: O(m * log(m)) where m = merged results

    ApplyMMR:
        - Selection loop: O(k)
        - Per candidate scoring: O(k * m)
        - Total: O(k^2 * m)

    Total: O(q * d + k * log(n) + k^2 * m)

Space Complexity:
    - Query embedding: O(d)
    - Result sets: O(3k)
    - Fused map: O(m)
    - MMR working set: O(m)
    - Total: O(d + m)

Performance Optimizations:
    1. Search result caching with content-based keys
    2. Parallel multi-source search
    3. Early termination with score thresholds
    4. Adaptive ef_search based on k
    5. Pre-computed filter masks
    6. Embedding cache reuse

Cache Hit Targets:
    - Exact match: 30%+ hit rate
    - Semantic similarity: 15%+ hit rate
    - Combined: 40%+ hit rate
```

---

## Algorithm 3: Self-Learning System

### 3.1 Core Learning Algorithm

```
ALGORITHM: LearnFromUsage
INPUT: interaction (Interaction)
OUTPUT: learningOutcome (LearningOutcome)

DATA STRUCTURES:
    Interaction:
        type: string ("search" | "access" | "feedback" | "synthesis")
        query: string (optional)
        noteIds: string[]
        outcome: OutcomeData
        context: ContextData
        timestamp: number

    PatternRecord:
        id: string
        pattern: string
        confidence: number
        usageCount: number
        successRate: number
        trajectory: string ("improving" | "stable" | "declining")
        lastUpdated: number

    LearningOutcome:
        patternsUpdated: number
        confidenceChanges: ConfidenceChange[]
        newPatterns: PatternRecord[]

CONSTANTS:
    MIN_PATTERN_FREQUENCY = 3
    CONFIDENCE_BOOST = 0.02
    CONFIDENCE_DECAY = 0.01
    MAX_CONFIDENCE = 0.99
    MIN_CONFIDENCE = 0.01

BEGIN
    learningOutcome <- {
        patternsUpdated: 0,
        confidenceChanges: [],
        newPatterns: []
    }

    // Route to appropriate learning handler
    SWITCH interaction.type
        CASE "search":
            learningOutcome <- LearnFromSearch(interaction)

        CASE "access":
            learningOutcome <- LearnFromAccess(interaction)

        CASE "feedback":
            learningOutcome <- LearnFromFeedback(interaction)

        CASE "synthesis":
            learningOutcome <- LearnFromSynthesis(interaction)
    END SWITCH

    // Update global learning state
    UpdateTrajectories()

    // Periodic maintenance
    IF ShouldRunMaintenance() THEN
        PruneWeakPatterns()
        ConsolidatePatterns()
    END IF

    RETURN learningOutcome
END

SUBROUTINE: LearnFromSearch
INPUT: interaction (Interaction)
OUTPUT: outcome (LearningOutcome)

BEGIN
    outcome <- { patternsUpdated: 0, confidenceChanges: [], newPatterns: [] }

    query <- interaction.query
    results <- interaction.outcome.results
    selectedId <- interaction.outcome.selectedId

    // Track query pattern
    queryPattern <- ExtractQueryPattern(query)
    existingPattern <- PatternStore.find(queryPattern)

    IF existingPattern EXISTS THEN
        // Update existing pattern
        wasSuccessful <- selectedId IN results[0:3].map(r => r.id)

        IF wasSuccessful THEN
            newConfidence <- MIN(
                existingPattern.confidence + CONFIDENCE_BOOST,
                MAX_CONFIDENCE
            )
            existingPattern.successRate <-
                (existingPattern.successRate * existingPattern.usageCount + 1) /
                (existingPattern.usageCount + 1)
        ELSE
            newConfidence <- MAX(
                existingPattern.confidence - CONFIDENCE_DECAY,
                MIN_CONFIDENCE
            )
            existingPattern.successRate <-
                (existingPattern.successRate * existingPattern.usageCount) /
                (existingPattern.usageCount + 1)
        END IF

        existingPattern.confidence <- newConfidence
        existingPattern.usageCount <- existingPattern.usageCount + 1
        existingPattern.lastUpdated <- GetCurrentTimeMillis()

        PatternStore.update(existingPattern)

        outcome.patternsUpdated <- 1
        outcome.confidenceChanges.append({
            patternId: existingPattern.id,
            oldConfidence: existingPattern.confidence -
                (wasSuccessful ? CONFIDENCE_BOOST : -CONFIDENCE_DECAY),
            newConfidence: existingPattern.confidence
        })
    ELSE
        // Create new pattern if query is meaningful
        IF LENGTH(query) > 3 THEN
            newPattern <- {
                id: GenerateUUID(),
                pattern: queryPattern,
                confidence: 0.5,
                usageCount: 1,
                successRate: selectedId IN results[0:3].map(r => r.id) ? 1.0 : 0.0,
                trajectory: "stable",
                lastUpdated: GetCurrentTimeMillis()
            }

            PatternStore.insert(newPattern)
            outcome.newPatterns.append(newPattern)
        END IF
    END IF

    // Update causal memory for search strategies
    IF selectedId EXISTS THEN
        CausalMemory.addCausation(
            causes: [queryPattern, interaction.context.taskType],
            effects: [selectedId],
            confidence: 0.7
        )
    END IF

    RETURN outcome
END

SUBROUTINE: LearnFromAccess
INPUT: interaction (Interaction)
OUTPUT: outcome (LearningOutcome)

BEGIN
    outcome <- { patternsUpdated: 0, confidenceChanges: [], newPatterns: [] }

    FOR EACH noteId IN interaction.noteIds DO
        note <- NoteStore.get(noteId)

        IF note IS NULL THEN
            CONTINUE
        END IF

        // Update access metrics
        note.accessCount <- note.accessCount + 1
        note.lastAccessed <- interaction.timestamp

        // Recalculate importance score
        oldImportance <- note.importance
        note.importance <- CalculateImportance(note)

        // Boost confidence based on access
        oldConfidence <- note.confidence
        note.confidence <- MIN(
            note.confidence + CONFIDENCE_BOOST * 0.5,
            MAX_CONFIDENCE
        )

        NoteStore.update(note)

        IF oldConfidence != note.confidence THEN
            outcome.confidenceChanges.append({
                noteId: noteId,
                oldConfidence: oldConfidence,
                newConfidence: note.confidence
            })
            outcome.patternsUpdated <- outcome.patternsUpdated + 1
        END IF

        // Learn access context patterns
        IF interaction.context EXISTS THEN
            contextPattern <- {
                noteId: noteId,
                accessContext: interaction.context,
                timestamp: interaction.timestamp
            }
            AccessPatternStore.append(contextPattern)
        END IF
    END FOR

    RETURN outcome
END

SUBROUTINE: CalculateImportance
INPUT: note (Note)
OUTPUT: importance (number 0-1)

BEGIN
    // Recency factor (decays over time)
    daysSinceAccess <- (GetCurrentTimeMillis() - note.lastAccessed) / 86400000
    recencyScore <- 1 / (1 + daysSinceAccess * 0.1)

    // Frequency factor (logarithmic scale)
    frequencyScore <- MIN(LOG(note.accessCount + 1) / LOG(100), 1)

    // Connection factor (based on graph degree)
    connectionCount <- KnowledgeGraph.getDegree(note.id)
    connectionScore <- MIN(connectionCount / 20, 1)

    // Explicit importance (user-defined)
    explicitScore <- note.explicitImportance OR 0.5

    // Weighted combination
    importance <- (
        recencyScore * 0.25 +
        frequencyScore * 0.30 +
        connectionScore * 0.25 +
        explicitScore * 0.20
    )

    RETURN importance
END
```

### 3.2 Trajectory Tracking and Pattern Distillation

```
SUBROUTINE: UpdateTrajectories
INPUT: none
OUTPUT: none

BEGIN
    patterns <- PatternStore.getAll()

    FOR EACH pattern IN patterns DO
        // Get historical confidence values
        history <- PatternHistory.get(pattern.id, limit=10)

        IF LENGTH(history) < 3 THEN
            pattern.trajectory <- "stable"
            CONTINUE
        END IF

        // Calculate trend using linear regression
        slope <- CalculateSlope(history)

        IF slope > 0.005 THEN
            pattern.trajectory <- "improving"
        ELSE IF slope < -0.005 THEN
            pattern.trajectory <- "declining"
        ELSE
            pattern.trajectory <- "stable"
        END IF

        PatternStore.update(pattern)
    END FOR
END

SUBROUTINE: PruneWeakPatterns
INPUT: none
OUTPUT: prunedCount (number)

BEGIN
    prunedCount <- 0
    patterns <- PatternStore.getAll()

    FOR EACH pattern IN patterns DO
        shouldPrune <- false

        // Prune low-confidence declining patterns
        IF pattern.confidence < 0.3 AND pattern.trajectory == "declining" THEN
            shouldPrune <- true
        END IF

        // Prune unused patterns (no access in 90 days)
        daysSinceUpdate <- (GetCurrentTimeMillis() - pattern.lastUpdated) / 86400000
        IF daysSinceUpdate > 90 AND pattern.usageCount < MIN_PATTERN_FREQUENCY THEN
            shouldPrune <- true
        END IF

        IF shouldPrune THEN
            // Archive before deletion
            PatternArchive.store(pattern)
            PatternStore.delete(pattern.id)
            prunedCount <- prunedCount + 1
        END IF
    END FOR

    RETURN prunedCount
END

SUBROUTINE: ConsolidatePatterns
INPUT: none
OUTPUT: consolidatedCount (number)

BEGIN
    consolidatedCount <- 0
    patterns <- PatternStore.getAll()

    // Find similar patterns for consolidation
    FOR i <- 0 TO LENGTH(patterns) - 1 DO
        FOR j <- i + 1 TO LENGTH(patterns) - 1 DO
            similarity <- CalculatePatternSimilarity(patterns[i], patterns[j])

            IF similarity > 0.95 THEN
                // Merge into pattern with higher confidence
                IF patterns[i].confidence >= patterns[j].confidence THEN
                    MergePatterns(patterns[i], patterns[j])
                    PatternStore.delete(patterns[j].id)
                ELSE
                    MergePatterns(patterns[j], patterns[i])
                    PatternStore.delete(patterns[i].id)
                END IF

                consolidatedCount <- consolidatedCount + 1
            END IF
        END FOR
    END FOR

    RETURN consolidatedCount
END
```

### 3.3 Complexity Analysis

```
ANALYSIS: Self-Learning System

Time Complexity:
    LearnFromUsage:
        - Routing: O(1)
        - Pattern store lookup: O(log p) where p = pattern count

    LearnFromSearch:
        - Pattern extraction: O(q)
        - Pattern lookup: O(log p)
        - Causal memory update: O(1)
        - Total: O(q + log p)

    LearnFromAccess:
        - Note retrieval: O(1) with hash lookup
        - Importance calculation: O(1)
        - Graph degree lookup: O(1) with cached degrees
        - Total: O(n) where n = accessed notes

    UpdateTrajectories:
        - Pattern iteration: O(p)
        - History retrieval per pattern: O(1)
        - Linear regression: O(h) where h = history length
        - Total: O(p * h)

    PruneWeakPatterns:
        - Pattern iteration: O(p)
        - Archive and delete: O(1) per pattern
        - Total: O(p)

    ConsolidatePatterns:
        - Pairwise comparison: O(p^2)
        - Similarity calculation: O(1)
        - Merge operation: O(1)
        - Total: O(p^2) - but runs infrequently

Space Complexity:
    - Pattern store: O(p)
    - Pattern history: O(p * h)
    - Access patterns: O(a) where a = access events
    - Causal memory: O(c) where c = causation records
    - Total: O(p * h + a + c)

Performance Optimizations:
    1. Batch pattern updates during idle periods
    2. Incremental trajectory calculation
    3. Bloom filter for quick pattern existence checks
    4. Sampling-based consolidation for large pattern stores
    5. Asynchronous archival operations

Learning Convergence:
    - Initial success rate: ~70%
    - After 100 interactions: ~85%
    - After 1000 interactions: ~90%+
    - Execution speedup: 46% faster after adaptation
```

---

## Algorithm 4: Knowledge Graph Construction

### 4.1 Main Graph Builder

```
ALGORITHM: BuildKnowledgeGraph
INPUT: notes (Note[])
OUTPUT: graph (KnowledgeGraph)

DATA STRUCTURES:
    KnowledgeGraph:
        nodes: Map<string, GraphNode>
        edges: Map<string, Edge[]>
        clusters: Cluster[]

    GraphNode:
        id: string
        type: string ("note" | "entity" | "concept" | "tag")
        properties: object
        embedding: Float32Array

    Edge:
        source: string
        target: string
        type: string
        weight: number
        confidence: number

    Cluster:
        id: string
        name: string
        nodeIds: string[]
        centroid: Float32Array

BEGIN
    graph <- {
        nodes: MAP(),
        edges: MAP(),
        clusters: []
    }

    // Phase 1: Create note nodes
    FOR EACH note IN notes DO
        node <- {
            id: note.id,
            type: "note",
            properties: {
                title: ExtractTitle(note.content),
                created: note.timestamp,
                tags: note.tags
            },
            embedding: note.embedding
        }
        graph.nodes.set(note.id, node)
    END FOR

    // Phase 2: Extract and create entity nodes
    allEntities <- []
    FOR EACH note IN notes DO
        FOR EACH entity IN note.entities DO
            allEntities.append({
                entity: entity,
                sourceNoteId: note.id
            })
        END FOR
    END FOR

    // Deduplicate entities across notes
    uniqueEntities <- DeduplicateEntitiesGlobal(allEntities)

    FOR EACH entityRecord IN uniqueEntities DO
        entityId <- GenerateEntityId(entityRecord.entity)

        IF NOT graph.nodes.has(entityId) THEN
            entityNode <- {
                id: entityId,
                type: "entity",
                properties: {
                    name: entityRecord.entity.name,
                    entityType: entityRecord.entity.type,
                    mentions: entityRecord.sourceNoteIds.length
                },
                embedding: GenerateEmbedding(entityRecord.entity.name)
            }
            graph.nodes.set(entityId, entityNode)
        END IF

        // Create edges from notes to entities
        FOR EACH sourceNoteId IN entityRecord.sourceNoteIds DO
            CreateEdge(graph, sourceNoteId, entityId, "mentions", {
                weight: 1.0,
                confidence: entityRecord.entity.confidence
            })
        END FOR
    END FOR

    // Phase 3: Detect semantic relationships between notes
    DetectSemanticRelationships(graph, notes)

    // Phase 4: Calculate link strengths
    CalculateLinkStrengths(graph)

    // Phase 5: Automatic clustering
    graph.clusters <- ClusterGraph(graph)

    RETURN graph
END
```

### 4.2 Relationship Detection

```
SUBROUTINE: DetectSemanticRelationships
INPUT: graph (KnowledgeGraph), notes (Note[])
OUTPUT: none (modifies graph in place)

BEGIN
    // Build KD-tree for efficient similarity search
    embeddings <- []
    noteIds <- []

    FOR EACH note IN notes DO
        embeddings.append(note.embedding)
        noteIds.append(note.id)
    END FOR

    index <- BuildAnnIndex(embeddings)

    // Find semantic neighbors for each note
    FOR i <- 0 TO LENGTH(notes) - 1 DO
        // Find k nearest neighbors
        neighbors <- index.search(embeddings[i], k=10)

        FOR EACH neighbor IN neighbors DO
            // Skip self
            IF neighbor.index == i THEN
                CONTINUE
            END IF

            similarity <- neighbor.similarity

            // Only create edges for significant similarity
            IF similarity > 0.5 THEN
                // Classify relationship type
                relationType <- ClassifyRelationship(
                    notes[i].content,
                    notes[neighbor.index].content,
                    similarity
                )

                CreateEdge(graph, noteIds[i], noteIds[neighbor.index], relationType, {
                    weight: similarity,
                    confidence: 0.8
                })
            END IF
        END FOR
    END FOR

    // Detect explicit wiki-link relationships
    FOR EACH note IN notes DO
        wikiLinks <- ExtractWikiLinks(note.content)

        FOR EACH link IN wikiLinks DO
            targetId <- ResolveWikiLink(link.target, notes)

            IF targetId EXISTS THEN
                CreateEdge(graph, note.id, targetId, "references", {
                    weight: 1.0,
                    confidence: 1.0,
                    explicit: true
                })
            END IF
        END FOR
    END FOR
END

SUBROUTINE: ClassifyRelationship
INPUT: content1 (string), content2 (string), similarity (number)
OUTPUT: relationType (string)

BEGIN
    // High similarity suggests strong relation
    IF similarity > 0.85 THEN
        // Check for temporal relationship
        IF HasTemporalIndicators(content1, content2) THEN
            RETURN "sequence"
        END IF

        // Check for hierarchical relationship
        IF IsSubsetContent(content1, content2) THEN
            RETURN "extends"
        ELSE IF IsSubsetContent(content2, content1) THEN
            RETURN "summarizes"
        END IF

        RETURN "relates_to"

    ELSE IF similarity > 0.7 THEN
        // Check for complementary content
        IF HasComplementaryTopics(content1, content2) THEN
            RETURN "complements"
        END IF

        RETURN "similar_to"

    ELSE
        // Weak but significant connection
        RETURN "weakly_related"
    END IF
END
```

### 4.3 Link Strength Calculation

```
SUBROUTINE: CalculateLinkStrengths
INPUT: graph (KnowledgeGraph)
OUTPUT: none (modifies graph in place)

BEGIN
    // Calculate PageRank-style importance for nodes
    nodeImportance <- CalculateNodeImportance(graph)

    // Update edge weights based on multiple factors
    FOR EACH nodeId IN graph.edges.keys() DO
        edges <- graph.edges.get(nodeId)

        FOR EACH edge IN edges DO
            // Base weight from similarity
            baseWeight <- edge.weight

            // Factor in node importance
            sourceImportance <- nodeImportance.get(edge.source)
            targetImportance <- nodeImportance.get(edge.target)
            importanceFactor <- (sourceImportance + targetImportance) / 2

            // Factor in edge type
            typeFactor <- GetEdgeTypeFactor(edge.type)

            // Factor in confidence
            confidenceFactor <- edge.confidence

            // Calculate final strength
            edge.strength <- (
                baseWeight * 0.4 +
                importanceFactor * 0.3 +
                typeFactor * 0.2 +
                confidenceFactor * 0.1
            )
        END FOR
    END FOR
END

SUBROUTINE: CalculateNodeImportance
INPUT: graph (KnowledgeGraph)
OUTPUT: importance (Map<string, number>)

BEGIN
    // Initialize with uniform distribution
    n <- graph.nodes.size()
    importance <- MAP()

    FOR EACH nodeId IN graph.nodes.keys() DO
        importance.set(nodeId, 1 / n)
    END FOR

    // Power iteration for PageRank
    dampingFactor <- 0.85
    maxIterations <- 100
    tolerance <- 0.0001

    FOR iteration <- 1 TO maxIterations DO
        newImportance <- MAP()
        maxDelta <- 0

        FOR EACH nodeId IN graph.nodes.keys() DO
            // Sum contributions from incoming edges
            sum <- 0
            incomingEdges <- GetIncomingEdges(graph, nodeId)

            FOR EACH edge IN incomingEdges DO
                sourceOutDegree <- GetOutDegree(graph, edge.source)
                contribution <- importance.get(edge.source) / sourceOutDegree
                sum <- sum + contribution
            END FOR

            // Apply damping factor
            newValue <- (1 - dampingFactor) / n + dampingFactor * sum
            newImportance.set(nodeId, newValue)

            // Track convergence
            delta <- ABS(newValue - importance.get(nodeId))
            maxDelta <- MAX(maxDelta, delta)
        END FOR

        importance <- newImportance

        // Check for convergence
        IF maxDelta < tolerance THEN
            BREAK
        END IF
    END FOR

    RETURN importance
END
```

### 4.4 Automatic Clustering

```
SUBROUTINE: ClusterGraph
INPUT: graph (KnowledgeGraph)
OUTPUT: clusters (Cluster[])

BEGIN
    // Get all note nodes with embeddings
    noteNodes <- []
    FOR EACH node IN graph.nodes.values() DO
        IF node.type == "note" THEN
            noteNodes.append(node)
        END IF
    END FOR

    IF LENGTH(noteNodes) < 5 THEN
        RETURN []  // Not enough nodes for meaningful clustering
    END IF

    // Prepare embedding matrix
    embeddings <- []
    nodeIds <- []

    FOR EACH node IN noteNodes DO
        embeddings.append(node.embedding)
        nodeIds.append(node.id)
    END FOR

    // Determine optimal cluster count using elbow method
    optimalK <- FindOptimalClusters(embeddings, maxK=MIN(20, LENGTH(noteNodes) / 3))

    // Run k-means clustering
    assignments <- KMeansClustering(embeddings, k=optimalK)

    // Build cluster objects
    clusters <- []
    FOR clusterIdx <- 0 TO optimalK - 1 DO
        clusterNodeIds <- []
        clusterEmbeddings <- []

        FOR i <- 0 TO LENGTH(assignments) - 1 DO
            IF assignments[i] == clusterIdx THEN
                clusterNodeIds.append(nodeIds[i])
                clusterEmbeddings.append(embeddings[i])
            END IF
        END FOR

        IF LENGTH(clusterNodeIds) > 0 THEN
            // Calculate centroid
            centroid <- MeanPool(clusterEmbeddings)

            // Generate cluster name from top keywords
            clusterName <- GenerateClusterName(clusterNodeIds, graph)

            cluster <- {
                id: GenerateUUID(),
                name: clusterName,
                nodeIds: clusterNodeIds,
                centroid: centroid
            }

            clusters.append(cluster)

            // Create cluster node in graph
            clusterNode <- {
                id: "cluster:" + cluster.id,
                type: "cluster",
                properties: {
                    name: clusterName,
                    size: LENGTH(clusterNodeIds)
                },
                embedding: centroid
            }
            graph.nodes.set(clusterNode.id, clusterNode)

            // Create edges from cluster to member nodes
            FOR EACH memberId IN clusterNodeIds DO
                CreateEdge(graph, clusterNode.id, memberId, "contains", {
                    weight: 1.0,
                    confidence: 1.0
                })
            END FOR
        END IF
    END FOR

    RETURN clusters
END
```

### 4.5 Complexity Analysis

```
ANALYSIS: Knowledge Graph Construction

Time Complexity:
    BuildKnowledgeGraph overall:
        - Node creation: O(n) where n = note count
        - Entity extraction: O(n * e_avg) where e_avg = avg entities per note
        - Entity deduplication: O(E * log E) where E = total entities

    DetectSemanticRelationships:
        - ANN index building: O(n * d * log n)
        - Neighbor search: O(n * k * log n) where k = neighbors
        - Relationship classification: O(n * k)
        - Wiki-link resolution: O(n * l) where l = links per note
        - Total: O(n * d * log n + n * k * log n)

    CalculateLinkStrengths:
        - PageRank iterations: O(iter * (V + E))
        - Edge weight updates: O(E)
        - Total: O(iter * V + E)

    ClusterGraph:
        - Optimal k finding: O(maxK * n * d * iter)
        - K-means: O(k * n * d * iter)
        - Cluster naming: O(k * c_avg) where c_avg = avg cluster size
        - Total: O(maxK * n * d * iter)

    Total: O(n * d * log n + iter * (V + E) + maxK * n * d * iter)

Space Complexity:
    - Node storage: O(n + E)
    - Edge storage: O(E^2) worst case, O(n * k) typical
    - Embeddings: O((n + E) * d)
    - Clustering working memory: O(n * d)
    - PageRank vectors: O(V)
    - Total: O(n * d + E)

Performance Optimizations:
    1. Incremental graph updates instead of full rebuild
    2. Approximate PageRank for large graphs
    3. Hierarchical clustering for large note counts
    4. Edge pruning with minimum weight threshold
    5. Lazy evaluation of relationship classification
    6. Cached entity resolution index

Scaling Characteristics:
    - 1,000 notes: < 5 seconds
    - 10,000 notes: < 30 seconds
    - 100,000 notes: ~5 minutes (with optimizations)
```

---

## Algorithm 5: MCP Tool Handlers

### 5.1 Main Request Router

```
ALGORITHM: HandleMCPTool
INPUT: request (MCPRequest)
OUTPUT: response (MCPResponse)

DATA STRUCTURES:
    MCPRequest:
        jsonrpc: string ("2.0")
        id: string | number
        method: string
        params: object

    MCPResponse:
        jsonrpc: string ("2.0")
        id: string | number
        result: any (optional)
        error: MCPError (optional)

    MCPError:
        code: number
        message: string
        data: any (optional)

    ToolMetrics:
        invocations: number
        avgLatency: number
        errorRate: number
        lastInvoked: number

BEGIN
    startTime <- GetHighResolutionTime()
    toolName <- ExtractToolName(request.method)

    // Validate request structure
    validationError <- ValidateRequest(request)
    IF validationError EXISTS THEN
        RETURN CreateErrorResponse(request.id, -32600, validationError)
    END IF

    // Check tool exists
    toolHandler <- ToolRegistry.get(toolName)
    IF toolHandler IS NULL THEN
        RETURN CreateErrorResponse(request.id, -32601, "Tool not found: " + toolName)
    END IF

    // Check authorization
    IF NOT IsAuthorized(request, toolHandler.requiredCapabilities) THEN
        RETURN CreateErrorResponse(request.id, -32603, "Unauthorized")
    END IF

    // Validate parameters
    paramError <- ValidateParameters(request.params, toolHandler.schema)
    IF paramError EXISTS THEN
        RETURN CreateErrorResponse(request.id, -32602, paramError)
    END IF

    // Execute tool with timeout
    TRY
        timeout <- toolHandler.timeout OR 30000
        result <- ExecuteWithTimeout(toolHandler.handler, request.params, timeout)

        // Track metrics
        latency <- GetHighResolutionTime() - startTime
        RecordToolMetrics(toolName, latency, success=true)

        // Record for learning
        RecordToolUsage(toolName, request.params, result, latency)

        RETURN {
            jsonrpc: "2.0",
            id: request.id,
            result: result
        }

    CATCH error
        // Track error metrics
        latency <- GetHighResolutionTime() - startTime
        RecordToolMetrics(toolName, latency, success=false)

        RETURN CreateErrorResponse(request.id, -32000, error.message)
    END TRY
END
```

### 5.2 Core PKM Tool Implementations

```
SUBROUTINE: RegisterPKMTools
INPUT: none
OUTPUT: none

BEGIN
    // Tool: pkm/capture
    ToolRegistry.register({
        name: "pkm/capture",
        description: "Quick capture with minimal processing (< 10ms)",
        schema: {
            content: { type: "string", required: true },
            source: { type: "string" },
            metadata: { type: "object" }
        },
        handler: HandleCapture,
        timeout: 5000,
        requiredCapabilities: ["write"]
    })

    // Tool: pkm/search
    ToolRegistry.register({
        name: "pkm/search",
        description: "Hybrid semantic + keyword + graph search",
        schema: {
            query: { type: "string", required: true },
            k: { type: "number", default: 10 },
            filter: { type: "object" },
            hybridWeight: { type: "number", default: 0.7 }
        },
        handler: HandleSearch,
        timeout: 10000,
        requiredCapabilities: ["read"]
    })

    // Tool: pkm/link
    ToolRegistry.register({
        name: "pkm/link",
        description: "Create or update knowledge connection",
        schema: {
            sourceId: { type: "string", required: true },
            targetId: { type: "string", required: true },
            relationship: { type: "string", required: true },
            weight: { type: "number", default: 1.0 }
        },
        handler: HandleLink,
        timeout: 5000,
        requiredCapabilities: ["write"]
    })

    // Tool: pkm/context
    ToolRegistry.register({
        name: "pkm/context",
        description: "Get related context for current work",
        schema: {
            query: { type: "string", required: true },
            noteIds: { type: "array", items: "string" },
            depth: { type: "number", default: 2 }
        },
        handler: HandleContext,
        timeout: 10000,
        requiredCapabilities: ["read"]
    })

    // Tool: pkm/synthesize
    ToolRegistry.register({
        name: "pkm/synthesize",
        description: "Generate insights from multiple notes",
        schema: {
            topic: { type: "string", required: true },
            noteIds: { type: "array", items: "string" },
            format: { type: "string", enum: ["summary", "outline", "connections"] }
        },
        handler: HandleSynthesize,
        streaming: true,
        timeout: 60000,
        requiredCapabilities: ["read"]
    })

    // Tool: pkm/learn
    ToolRegistry.register({
        name: "pkm/learn",
        description: "Record interaction for system learning",
        schema: {
            type: { type: "string", enum: ["search", "access", "feedback", "synthesis"] },
            data: { type: "object", required: true }
        },
        handler: HandleLearn,
        timeout: 5000,
        requiredCapabilities: ["write"]
    })
END
```

### 5.3 Tool Handler Implementations

```
SUBROUTINE: HandleCapture
INPUT: params (object)
OUTPUT: result (object)

BEGIN
    captureInput <- {
        content: params.content,
        source: params.source OR "mcp",
        metadata: params.metadata OR {}
    }

    captureId <- CaptureKnowledge(captureInput)

    RETURN {
        id: captureId,
        status: "queued",
        timestamp: GetCurrentTimeMillis()
    }
END

SUBROUTINE: HandleSearch
INPUT: params (object)
OUTPUT: result (object)

BEGIN
    searchOptions <- {
        k: params.k,
        filter: params.filter,
        hybridWeight: params.hybridWeight,
        includeMetadata: true
    }

    results <- SemanticSearch(params.query, searchOptions)

    RETURN {
        results: results,
        count: LENGTH(results),
        query: params.query
    }
END

SUBROUTINE: HandleContext
INPUT: params (object)
OUTPUT: result (object)

BEGIN
    contextItems <- []

    // If noteIds provided, use as starting points
    IF params.noteIds EXISTS AND LENGTH(params.noteIds) > 0 THEN
        // Get related notes through graph traversal
        FOR EACH noteId IN params.noteIds DO
            related <- KnowledgeGraph.getNeighbors(noteId, depth=params.depth)
            contextItems <- contextItems UNION related
        END FOR
    END IF

    // Add semantically similar notes based on query
    IF params.query EXISTS THEN
        semantic <- SemanticSearch(params.query, { k: 10 })
        FOR EACH result IN semantic DO
            contextItems.append({
                id: result.id,
                content: result.content,
                score: result.score,
                type: "semantic"
            })
        END FOR
    END IF

    // Deduplicate and rank
    uniqueContext <- DeduplicateById(contextItems)
    rankedContext <- RankByRelevance(uniqueContext, params.query)

    RETURN {
        context: rankedContext,
        count: LENGTH(rankedContext),
        depth: params.depth
    }
END

SUBROUTINE: HandleSynthesize
INPUT: params (object)
OUTPUT: stream (AsyncGenerator)

BEGIN
    // Gather source notes
    notes <- []
    FOR EACH noteId IN params.noteIds DO
        note <- NoteStore.get(noteId)
        IF note EXISTS THEN
            notes.append(note)
        END IF
    END FOR

    // Stream synthesis results
    YIELD { status: "analyzing", progress: 0 }

    // Extract key concepts
    concepts <- ExtractCommonConcepts(notes)
    YIELD { status: "concepts", data: concepts, progress: 25 }

    // Find connections
    connections <- FindConnections(notes, concepts)
    YIELD { status: "connections", data: connections, progress: 50 }

    // Generate synthesis based on format
    SWITCH params.format
        CASE "summary":
            synthesis <- GenerateSummary(notes, concepts, connections)
        CASE "outline":
            synthesis <- GenerateOutline(notes, concepts)
        CASE "connections":
            synthesis <- GenerateConnectionMap(notes, connections)
    END SWITCH

    YIELD { status: "complete", data: synthesis, progress: 100 }

    // Record for learning
    LearnFromUsage({
        type: "synthesis",
        query: params.topic,
        noteIds: params.noteIds,
        outcome: { success: true }
    })
END
```

### 5.4 Complexity Analysis

```
ANALYSIS: MCP Tool Handlers

Time Complexity:
    HandleMCPTool (routing):
        - Validation: O(1)
        - Registry lookup: O(1) with hash map
        - Authorization check: O(c) where c = capabilities
        - Parameter validation: O(p) where p = param count
        - Total routing overhead: O(p)

    HandleCapture:
        - Input creation: O(1)
        - CaptureKnowledge call: O(n) where n = content length
        - Total: O(n)

    HandleSearch:
        - SemanticSearch call: O(q * d + k * log(n) + k^2 * m)
        - Response formatting: O(k)
        - Total: Same as SemanticSearch

    HandleContext:
        - Graph traversal: O(|V| + |E|) per starting node
        - Semantic search: O(q * d + k * log(n))
        - Deduplication: O(r * log r) where r = results
        - Ranking: O(r * log r)
        - Total: O(depth * (|V| + |E|) + q * d + k * log(n) + r * log r)

    HandleSynthesize:
        - Note gathering: O(s) where s = source notes
        - Concept extraction: O(s * n_avg)
        - Connection finding: O(s^2)
        - Synthesis generation: O(total_content)
        - Total: O(s^2 + total_content)

Space Complexity:
    - Request/response buffers: O(request_size + response_size)
    - Tool registry: O(t) where t = registered tools
    - Metrics storage: O(t)
    - Synthesis working memory: O(total_content)
    - Total: O(t + response_size)

Performance Optimizations:
    1. Connection pooling for database calls
    2. Request batching with JSON-RPC batching
    3. Response streaming for long operations
    4. Tool result caching for repeated calls
    5. Lazy parameter validation
    6. Concurrent tool execution for independent calls

Latency Targets:
    - pkm/capture: < 10ms
    - pkm/search: < 100ms
    - pkm/link: < 50ms
    - pkm/context: < 200ms
    - pkm/synthesize: Streaming (first chunk < 500ms)
```

---

## Algorithm 6: Obsidian Sync Protocol

### 6.1 File System Watcher

```
ALGORITHM: SyncWithObsidian
INPUT: vaultPath (string)
OUTPUT: syncStatus (SyncStatus)

DATA STRUCTURES:
    SyncStatus:
        status: string ("running" | "paused" | "error")
        lastSync: number
        pendingChanges: number
        indexedFiles: number

    FileChange:
        path: string
        type: string ("create" | "modify" | "delete" | "rename")
        timestamp: number
        oldPath: string (for rename)

    SyncState:
        fileHashes: Map<string, string>
        lastModified: Map<string, number>
        indexedCount: number

CONSTANTS:
    BATCH_SIZE = 50
    DEBOUNCE_MS = 500
    FULL_SYNC_INTERVAL = 3600000  // 1 hour

BEGIN
    // Initialize sync state
    syncState <- LoadSyncState(vaultPath) OR CreateInitialState()
    changeQueue <- []
    debounceTimer <- NULL

    // Set up file system watcher
    watcher <- CreateFileWatcher(vaultPath, {
        patterns: ["**/*.md"],
        ignorePatterns: [".obsidian/**", ".git/**", ".trash/**"],
        recursive: true
    })

    // Handle file events
    watcher.on("change", (event) => {
        change <- {
            path: event.path,
            type: event.type,
            timestamp: GetCurrentTimeMillis(),
            oldPath: event.oldPath
        }

        changeQueue.append(change)

        // Debounce processing
        IF debounceTimer EXISTS THEN
            ClearTimeout(debounceTimer)
        END IF

        debounceTimer <- SetTimeout(() => {
            ProcessChangeQueue(changeQueue, syncState)
            changeQueue <- []
        }, DEBOUNCE_MS)
    })

    // Start watcher
    watcher.start()

    // Schedule periodic full sync
    SetInterval(() => {
        PerformFullSync(vaultPath, syncState)
    }, FULL_SYNC_INTERVAL)

    // Perform initial sync
    PerformFullSync(vaultPath, syncState)

    RETURN {
        status: "running",
        lastSync: GetCurrentTimeMillis(),
        pendingChanges: 0,
        indexedFiles: syncState.indexedCount
    }
END
```

### 6.2 Incremental Indexing

```
SUBROUTINE: ProcessChangeQueue
INPUT: changes (FileChange[]), syncState (SyncState)
OUTPUT: none

BEGIN
    // Group changes by path to avoid duplicate processing
    changesByPath <- GroupBy(changes, c => c.path)

    // Process in batches
    paths <- KEYS(changesByPath)
    batches <- Chunk(paths, BATCH_SIZE)

    FOR EACH batch IN batches DO
        PARALLEL FOR EACH path IN batch DO
            lastChange <- GetLastChange(changesByPath.get(path))

            SWITCH lastChange.type
                CASE "create":
                    IndexNewFile(path, syncState)

                CASE "modify":
                    UpdateFileIndex(path, syncState)

                CASE "delete":
                    RemoveFromIndex(path, syncState)

                CASE "rename":
                    HandleRename(lastChange.oldPath, path, syncState)
            END SWITCH
        END PARALLEL
    END FOR

    // Persist sync state
    SaveSyncState(syncState)
END

SUBROUTINE: IndexNewFile
INPUT: filePath (string), syncState (SyncState)
OUTPUT: none

BEGIN
    // Read file content
    content <- ReadFile(filePath)

    IF content IS NULL THEN
        LogError("Failed to read file: " + filePath)
        RETURN
    END IF

    // Parse Obsidian markdown
    parsed <- ParseObsidianMarkdown(content)

    // Generate content hash
    contentHash <- HashContent(content)

    // Check if already indexed (duplicate detection)
    IF syncState.fileHashes.has(filePath) AND
       syncState.fileHashes.get(filePath) == contentHash THEN
        RETURN  // No changes
    END IF

    // Capture to PKM system
    captureInput <- {
        content: content,
        source: "obsidian:" + filePath,
        metadata: {
            frontmatter: parsed.frontmatter,
            tags: parsed.tags,
            links: parsed.links,
            aliases: parsed.frontmatter.aliases OR []
        }
    }

    noteId <- CaptureKnowledge(captureInput)

    // Update sync state
    syncState.fileHashes.set(filePath, contentHash)
    syncState.lastModified.set(filePath, GetFileModTime(filePath))
    syncState.indexedCount <- syncState.indexedCount + 1

    // Map file path to note ID for bidirectional sync
    FileNoteMapping.set(filePath, noteId)
    NoteFileMapping.set(noteId, filePath)
END

SUBROUTINE: UpdateFileIndex
INPUT: filePath (string), syncState (SyncState)
OUTPUT: none

BEGIN
    // Read updated content
    content <- ReadFile(filePath)

    IF content IS NULL THEN
        RETURN
    END IF

    // Check if content actually changed
    newHash <- HashContent(content)
    oldHash <- syncState.fileHashes.get(filePath)

    IF newHash == oldHash THEN
        RETURN  // No actual content change
    END IF

    // Get existing note ID
    noteId <- FileNoteMapping.get(filePath)

    IF noteId IS NULL THEN
        // File not previously indexed, treat as new
        IndexNewFile(filePath, syncState)
        RETURN
    END IF

    // Parse updated content
    parsed <- ParseObsidianMarkdown(content)

    // Update note in PKM system
    note <- NoteStore.get(noteId)

    note.content <- content
    note.metadata.frontmatter <- parsed.frontmatter
    note.metadata.tags <- parsed.tags
    note.metadata.links <- parsed.links

    // Re-generate embedding
    note.embedding <- GenerateEmbedding(content)

    // Re-extract entities
    note.entities <- ExtractEntities(content)

    NoteStore.update(note)

    // Update vector index
    VectorStore.update(noteId, note.embedding, {
        title: ExtractTitle(content),
        tags: parsed.tags,
        modified: GetCurrentTimeMillis()
    })

    // Trigger relationship discovery
    RelationshipQueue.schedule(noteId)

    // Update sync state
    syncState.fileHashes.set(filePath, newHash)
    syncState.lastModified.set(filePath, GetFileModTime(filePath))
END
```

### 6.3 Bidirectional Sync

```
SUBROUTINE: SyncBackToObsidian
INPUT: noteId (string)
OUTPUT: success (boolean)

BEGIN
    note <- NoteStore.get(noteId)

    IF note IS NULL THEN
        RETURN false
    END IF

    // Get mapped file path
    filePath <- NoteFileMapping.get(noteId)

    IF filePath IS NULL THEN
        // Create new file in vault
        filePath <- GenerateFilePath(note)
        NoteFileMapping.set(noteId, filePath)
        FileNoteMapping.set(filePath, noteId)
    END IF

    // Build Obsidian-compatible markdown
    markdown <- BuildObsidianMarkdown(note)

    // Write to file
    success <- WriteFile(filePath, markdown)

    IF success THEN
        // Update sync state to prevent re-indexing
        contentHash <- HashContent(markdown)
        syncState.fileHashes.set(filePath, contentHash)
        syncState.lastModified.set(filePath, GetCurrentTimeMillis())
    END IF

    RETURN success
END

SUBROUTINE: BuildObsidianMarkdown
INPUT: note (Note)
OUTPUT: markdown (string)

BEGIN
    lines <- []

    // Build frontmatter
    IF note.metadata.frontmatter EXISTS OR
       LENGTH(note.tags) > 0 OR
       LENGTH(note.metadata.aliases) > 0 THEN

        lines.append("---")

        IF note.metadata.aliases EXISTS THEN
            lines.append("aliases: " + JSON.stringify(note.metadata.aliases))
        END IF

        IF LENGTH(note.tags) > 0 THEN
            lines.append("tags: " + JSON.stringify(note.tags))
        END IF

        // Include other frontmatter properties
        FOR EACH [key, value] IN note.metadata.frontmatter DO
            IF key NOT IN ["aliases", "tags"] THEN
                lines.append(key + ": " + YAML.stringify(value))
            END IF
        END FOR

        lines.append("---")
        lines.append("")
    END IF

    // Add content
    lines.append(note.content)

    // Add PKM-generated connections as footer
    IF note.relationships EXISTS AND LENGTH(note.relationships) > 0 THEN
        lines.append("")
        lines.append("## Related Notes")
        lines.append("")

        FOR EACH rel IN note.relationships DO
            relatedNote <- NoteStore.get(rel.targetId)
            IF relatedNote EXISTS THEN
                title <- ExtractTitle(relatedNote.content)
                lines.append("- [[" + title + "]]")
            END IF
        END FOR
    END IF

    RETURN JOIN(lines, "\n")
END

SUBROUTINE: ParseObsidianMarkdown
INPUT: content (string)
OUTPUT: parsed (ParsedMarkdown)

BEGIN
    parsed <- {
        frontmatter: {},
        content: "",
        tags: [],
        links: []
    }

    // Extract frontmatter
    frontmatterMatch <- content.match(/^---\n([\s\S]*?)\n---/)

    IF frontmatterMatch EXISTS THEN
        parsed.frontmatter <- YAML.parse(frontmatterMatch[1])
        parsed.content <- content.substring(frontmatterMatch[0].length).trim()
    ELSE
        parsed.content <- content
    END IF

    // Extract inline tags
    tagMatches <- parsed.content.matchAll(/#[\w\/-]+/g)
    FOR EACH match IN tagMatches DO
        tag <- match[0].substring(1)  // Remove #
        parsed.tags.append(NormalizeTag(tag))
    END FOR

    // Include frontmatter tags
    IF parsed.frontmatter.tags EXISTS THEN
        FOR EACH tag IN parsed.frontmatter.tags DO
            parsed.tags.append(NormalizeTag(tag))
        END FOR
    END IF

    // Deduplicate tags
    parsed.tags <- UNIQUE(parsed.tags)

    // Extract wiki links
    linkMatches <- parsed.content.matchAll(/\[\[(.*?)(\|.*?)?\]\]/g)
    FOR EACH match IN linkMatches DO
        linkTarget <- match[1]
        parsed.links.append({
            target: linkTarget,
            display: match[2] ? match[2].substring(1) : linkTarget
        })
    END FOR

    RETURN parsed
END
```

### 6.4 Full Sync

```
SUBROUTINE: PerformFullSync
INPUT: vaultPath (string), syncState (SyncState)
OUTPUT: none

BEGIN
    LogInfo("Starting full sync of vault: " + vaultPath)

    // Get all markdown files in vault
    allFiles <- GlobFiles(vaultPath, "**/*.md", {
        ignore: [".obsidian/**", ".git/**", ".trash/**"]
    })

    // Find files that need indexing
    filesToIndex <- []
    filesToUpdate <- []
    filesToRemove <- []

    indexedFiles <- SET(syncState.fileHashes.keys())
    currentFiles <- SET(allFiles)

    // New files
    FOR EACH file IN allFiles DO
        IF NOT syncState.fileHashes.has(file) THEN
            filesToIndex.append(file)
        ELSE
            // Check if modified
            currentModTime <- GetFileModTime(file)
            lastModTime <- syncState.lastModified.get(file)

            IF currentModTime > lastModTime THEN
                filesToUpdate.append(file)
            END IF
        END IF
    END FOR

    // Deleted files
    FOR EACH file IN indexedFiles DO
        IF NOT currentFiles.has(file) THEN
            filesToRemove.append(file)
        END IF
    END FOR

    // Process in parallel batches
    LogInfo("New files: " + LENGTH(filesToIndex))
    LogInfo("Updated files: " + LENGTH(filesToUpdate))
    LogInfo("Deleted files: " + LENGTH(filesToRemove))

    // Index new files
    FOR EACH batch IN Chunk(filesToIndex, BATCH_SIZE) DO
        PARALLEL FOR EACH file IN batch DO
            IndexNewFile(file, syncState)
        END PARALLEL
    END FOR

    // Update modified files
    FOR EACH batch IN Chunk(filesToUpdate, BATCH_SIZE) DO
        PARALLEL FOR EACH file IN batch DO
            UpdateFileIndex(file, syncState)
        END PARALLEL
    END FOR

    // Remove deleted files
    FOR EACH file IN filesToRemove DO
        RemoveFromIndex(file, syncState)
    END FOR

    // Save sync state
    SaveSyncState(syncState)

    LogInfo("Full sync complete. Indexed: " + syncState.indexedCount)
END
```

### 6.5 Complexity Analysis

```
ANALYSIS: Obsidian Sync Protocol

Time Complexity:
    SyncWithObsidian (initialization):
        - Load state: O(s) where s = state size
        - Initial full sync: O(f * n) where f = files, n = avg content size

    ProcessChangeQueue:
        - Grouping: O(c) where c = changes
        - Batch processing: O(c / BATCH_SIZE)
        - Per file: O(n) for content processing
        - Total: O(c * n)

    IndexNewFile:
        - File read: O(n)
        - Parse markdown: O(n)
        - Hash generation: O(n)
        - CaptureKnowledge: O(n)
        - Total: O(n)

    UpdateFileIndex:
        - File read: O(n)
        - Hash comparison: O(n)
        - Embedding generation: O(n * d)
        - Vector update: O(log m)
        - Total: O(n * d)

    PerformFullSync:
        - File enumeration: O(f)
        - State comparison: O(f)
        - Batch processing: O(f * n * d / BATCH_SIZE)
        - Total: O(f * n * d)

    BuildObsidianMarkdown:
        - Frontmatter: O(p) where p = properties
        - Content: O(n)
        - Relationships: O(r)
        - Total: O(n + r)

Space Complexity:
    - Sync state: O(f) for file hashes and timestamps
    - Change queue: O(c)
    - File-Note mappings: O(f)
    - Watcher buffers: O(w) where w = watch events
    - Total: O(f + c)

Performance Optimizations:
    1. Debounced change processing (500ms default)
    2. Parallel batch processing
    3. Incremental hashing for large files
    4. Memory-mapped file reading
    5. Lazy frontmatter parsing
    6. Watch event coalescing

Sync Latency Targets:
    - Single file change: < 1 second
    - Batch (50 files): < 5 seconds
    - Full sync (1000 files): < 30 seconds
    - Full sync (10000 files): < 5 minutes
```

---

## Algorithm 7: Adaptive Workflow

### 7.1 Context-Aware Agent Selection

```
ALGORITHM: AdaptWorkflow
INPUT: context (WorkflowContext)
OUTPUT: result (WorkflowResult)

DATA STRUCTURES:
    WorkflowContext:
        task: string
        taskType: string
        complexity: number (1-10)
        urgency: number (1-10)
        resources: object
        history: InteractionHistory

    AgentProfile:
        id: string
        type: string
        capabilities: string[]
        performance: PerformanceMetrics
        currentLoad: number

    WorkflowResult:
        success: boolean
        output: any
        agentUsed: string
        duration: number
        confidence: number

CONSTANTS:
    AGENT_TYPES = ["researcher", "coder", "analyzer", "curator", "synthesizer"]
    COMPLEXITY_THRESHOLD_MULTI_AGENT = 7
    LEARNING_RATE = 0.1

BEGIN
    startTime <- GetHighResolutionTime()

    // Phase 1: Analyze task context
    taskAnalysis <- AnalyzeTask(context)

    // Phase 2: Select optimal agent(s)
    IF taskAnalysis.complexity >= COMPLEXITY_THRESHOLD_MULTI_AGENT THEN
        selectedAgents <- SelectMultipleAgents(taskAnalysis)
        result <- ExecuteWithSwarm(selectedAgents, context, taskAnalysis)
    ELSE
        selectedAgent <- SelectSingleAgent(taskAnalysis)
        result <- ExecuteWithAgent(selectedAgent, context, taskAnalysis)
    END IF

    // Phase 3: Learn from execution
    duration <- GetHighResolutionTime() - startTime

    outcome <- {
        success: result.success,
        duration: duration,
        agentUsed: result.agentUsed,
        taskType: taskAnalysis.taskType,
        complexity: taskAnalysis.complexity
    }

    LearnFromWorkflow(outcome)

    // Update result with metadata
    result.duration <- duration

    RETURN result
END
```

### 7.2 Task Analysis

```
SUBROUTINE: AnalyzeTask
INPUT: context (WorkflowContext)
OUTPUT: analysis (TaskAnalysis)

BEGIN
    analysis <- {
        taskType: NULL,
        complexity: 0,
        requiredCapabilities: [],
        estimatedDuration: 0,
        recommendedApproach: NULL
    }

    // Classify task type
    analysis.taskType <- ClassifyTaskType(context.task)

    // Estimate complexity
    analysis.complexity <- EstimateComplexity(context)

    // Determine required capabilities
    analysis.requiredCapabilities <- DetermineCapabilities(
        analysis.taskType,
        context.task
    )

    // Check for learned patterns
    similarTasks <- FindSimilarTasks(context.task)

    IF LENGTH(similarTasks) > 0 THEN
        // Use historical data to inform analysis
        bestMatch <- similarTasks[0]

        // Adjust complexity based on past performance
        IF bestMatch.wasSuccessful AND bestMatch.duration < bestMatch.estimatedDuration THEN
            analysis.complexity <- analysis.complexity * 0.9
        ELSE IF NOT bestMatch.wasSuccessful THEN
            analysis.complexity <- analysis.complexity * 1.1
        END IF

        analysis.recommendedApproach <- bestMatch.approach
        analysis.estimatedDuration <- bestMatch.duration * 1.1  // 10% buffer
    ELSE
        // Use heuristics for new task types
        analysis.estimatedDuration <- EstimateDuration(analysis.complexity)
        analysis.recommendedApproach <- DetermineDefaultApproach(analysis.taskType)
    END IF

    RETURN analysis
END

SUBROUTINE: ClassifyTaskType
INPUT: task (string)
OUTPUT: taskType (string)

BEGIN
    // Use embedding similarity to known task patterns
    taskEmbedding <- GenerateEmbedding(task)

    // Search task pattern index
    matches <- TaskPatternIndex.search(taskEmbedding, k=3)

    IF LENGTH(matches) > 0 AND matches[0].similarity > 0.7 THEN
        RETURN matches[0].taskType
    END IF

    // Fallback to rule-based classification
    task_lower <- LOWERCASE(task)

    IF Contains(task_lower, ["search", "find", "lookup", "retrieve"]) THEN
        RETURN "retrieval"
    ELSE IF Contains(task_lower, ["summarize", "synthesize", "combine"]) THEN
        RETURN "synthesis"
    ELSE IF Contains(task_lower, ["analyze", "compare", "evaluate"]) THEN
        RETURN "analysis"
    ELSE IF Contains(task_lower, ["create", "write", "generate"]) THEN
        RETURN "creation"
    ELSE IF Contains(task_lower, ["organize", "tag", "categorize"]) THEN
        RETURN "curation"
    ELSE IF Contains(task_lower, ["link", "connect", "relate"]) THEN
        RETURN "linking"
    ELSE
        RETURN "general"
    END IF
END

SUBROUTINE: EstimateComplexity
INPUT: context (WorkflowContext)
OUTPUT: complexity (number 1-10)

BEGIN
    complexity <- 5  // Base complexity

    // Factor 1: Task length and structure
    taskLength <- LENGTH(context.task)
    IF taskLength > 500 THEN
        complexity <- complexity + 2
    ELSE IF taskLength > 200 THEN
        complexity <- complexity + 1
    END IF

    // Factor 2: Required resources
    IF context.resources.noteCount > 100 THEN
        complexity <- complexity + 2
    ELSE IF context.resources.noteCount > 20 THEN
        complexity <- complexity + 1
    END IF

    // Factor 3: Urgency (high urgency = need efficiency)
    IF context.urgency > 7 THEN
        complexity <- complexity - 1  // Simplify for speed
    END IF

    // Factor 4: Historical difficulty
    similarTasks <- context.history.getSimilar(context.task)
    IF LENGTH(similarTasks) > 0 THEN
        avgDifficulty <- MEAN(similarTasks.map(t => t.difficulty))
        complexity <- (complexity + avgDifficulty) / 2
    END IF

    RETURN CLAMP(complexity, 1, 10)
END
```

### 7.3 Agent Selection

```
SUBROUTINE: SelectSingleAgent
INPUT: taskAnalysis (TaskAnalysis)
OUTPUT: agent (AgentProfile)

BEGIN
    candidateAgents <- []

    // Get all available agents
    allAgents <- AgentRegistry.getAll()

    // Filter by capabilities
    FOR EACH agent IN allAgents DO
        IF HasRequiredCapabilities(agent, taskAnalysis.requiredCapabilities) THEN
            candidateAgents.append(agent)
        END IF
    END FOR

    IF LENGTH(candidateAgents) == 0 THEN
        // Fallback to general-purpose agent
        RETURN AgentRegistry.get("general")
    END IF

    // Score candidates
    scoredCandidates <- []
    FOR EACH agent IN candidateAgents DO
        score <- CalculateAgentScore(agent, taskAnalysis)
        scoredCandidates.append({ agent: agent, score: score })
    END FOR

    // Sort by score descending
    scoredCandidates.sortByDescending(c => c.score)

    // Select best available agent (considering current load)
    FOR EACH candidate IN scoredCandidates DO
        IF candidate.agent.currentLoad < 0.8 THEN  // 80% load threshold
            RETURN candidate.agent
        END IF
    END FOR

    // All agents busy, return best scorer anyway
    RETURN scoredCandidates[0].agent
END

SUBROUTINE: CalculateAgentScore
INPUT: agent (AgentProfile), taskAnalysis (TaskAnalysis)
OUTPUT: score (number 0-1)

BEGIN
    // Factor 1: Task type alignment
    typeAlignment <- CalculateTypeAlignment(agent.type, taskAnalysis.taskType)

    // Factor 2: Historical performance on similar tasks
    perfScore <- agent.performance.getScoreForType(taskAnalysis.taskType)

    // Factor 3: Current load (prefer less loaded agents)
    loadPenalty <- agent.currentLoad * 0.3

    // Factor 4: Capability match
    capabilityMatch <- CalculateCapabilityMatch(
        agent.capabilities,
        taskAnalysis.requiredCapabilities
    )

    // Weighted combination
    score <- (
        typeAlignment * 0.30 +
        perfScore * 0.35 +
        (1 - loadPenalty) * 0.15 +
        capabilityMatch * 0.20
    )

    RETURN score
END

SUBROUTINE: SelectMultipleAgents
INPUT: taskAnalysis (TaskAnalysis)
OUTPUT: agents (AgentProfile[])

BEGIN
    // Decompose task into subtasks
    subtasks <- DecomposeTask(taskAnalysis)

    agents <- []
    usedAgents <- SET()

    // Select agent for each subtask
    FOR EACH subtask IN subtasks DO
        // Create mini-analysis for subtask
        subtaskAnalysis <- {
            taskType: subtask.type,
            complexity: subtask.complexity,
            requiredCapabilities: subtask.capabilities
        }

        // Select agent (avoiding duplicates when possible)
        candidate <- SelectSingleAgent(subtaskAnalysis)

        // Try to use different agents for diversity
        IF usedAgents.has(candidate.id) AND LENGTH(agents) < LENGTH(AGENT_TYPES) THEN
            alternatives <- GetAlternativeAgents(subtaskAnalysis, usedAgents)
            IF LENGTH(alternatives) > 0 THEN
                candidate <- alternatives[0]
            END IF
        END IF

        agents.append({
            agent: candidate,
            subtask: subtask
        })
        usedAgents.add(candidate.id)
    END FOR

    RETURN agents
END
```

### 7.4 Execution and Learning

```
SUBROUTINE: ExecuteWithAgent
INPUT: agent (AgentProfile), context (WorkflowContext), taskAnalysis (TaskAnalysis)
OUTPUT: result (WorkflowResult)

BEGIN
    // Update agent load
    agent.currentLoad <- agent.currentLoad + 0.1

    TRY
        // Execute task based on task type
        output <- NULL

        SWITCH taskAnalysis.taskType
            CASE "retrieval":
                output <- ExecuteRetrievalTask(agent, context)

            CASE "synthesis":
                output <- ExecuteSynthesisTask(agent, context)

            CASE "analysis":
                output <- ExecuteAnalysisTask(agent, context)

            CASE "creation":
                output <- ExecuteCreationTask(agent, context)

            CASE "curation":
                output <- ExecuteCurationTask(agent, context)

            DEFAULT:
                output <- ExecuteGeneralTask(agent, context)
        END SWITCH

        // Calculate confidence based on output quality
        confidence <- EvaluateOutputQuality(output, taskAnalysis)

        RETURN {
            success: true,
            output: output,
            agentUsed: agent.id,
            confidence: confidence
        }

    CATCH error
        LogError("Agent execution failed: " + error.message)

        RETURN {
            success: false,
            output: NULL,
            agentUsed: agent.id,
            confidence: 0,
            error: error.message
        }

    FINALLY
        // Release agent load
        agent.currentLoad <- MAX(0, agent.currentLoad - 0.1)
    END TRY
END

SUBROUTINE: LearnFromWorkflow
INPUT: outcome (WorkflowOutcome)
OUTPUT: none

BEGIN
    // Update agent performance metrics
    agent <- AgentRegistry.get(outcome.agentUsed)

    IF outcome.success THEN
        // Boost agent's score for this task type
        agent.performance.recordSuccess(outcome.taskType, outcome.duration)
    ELSE
        // Reduce agent's score for this task type
        agent.performance.recordFailure(outcome.taskType)
    END IF

    AgentRegistry.update(agent)

    // Store workflow trajectory for pattern learning
    trajectory <- {
        task: outcome.task,
        taskType: outcome.taskType,
        complexity: outcome.complexity,
        agentUsed: outcome.agentUsed,
        success: outcome.success,
        duration: outcome.duration,
        timestamp: GetCurrentTimeMillis()
    }

    WorkflowTrajectoryStore.append(trajectory)

    // Periodically consolidate learned patterns
    IF WorkflowTrajectoryStore.count() MOD 100 == 0 THEN
        ConsolidateWorkflowPatterns()
    END IF

    // Update task pattern index if successful
    IF outcome.success AND outcome.confidence > 0.8 THEN
        taskEmbedding <- GenerateEmbedding(outcome.task)
        TaskPatternIndex.upsert({
            embedding: taskEmbedding,
            taskType: outcome.taskType,
            approach: outcome.approach,
            duration: outcome.duration,
            confidence: outcome.confidence
        })
    END IF
END

SUBROUTINE: ConsolidateWorkflowPatterns
INPUT: none
OUTPUT: none

BEGIN
    // Get recent trajectories
    trajectories <- WorkflowTrajectoryStore.getRecent(limit=1000)

    // Group by task type and agent
    groupedTrajectories <- GroupBy(trajectories, t => t.taskType + ":" + t.agentUsed)

    FOR EACH [key, group] IN groupedTrajectories DO
        IF LENGTH(group) < 5 THEN
            CONTINUE  // Not enough data
        END IF

        // Calculate aggregate metrics
        successRate <- COUNT(group, t => t.success) / LENGTH(group)
        avgDuration <- MEAN(group.map(t => t.duration))
        avgComplexity <- MEAN(group.map(t => t.complexity))

        // Create or update pattern
        pattern <- {
            taskType: group[0].taskType,
            agent: group[0].agentUsed,
            successRate: successRate,
            avgDuration: avgDuration,
            avgComplexity: avgComplexity,
            sampleCount: LENGTH(group),
            confidence: MIN(successRate, LENGTH(group) / 100)
        }

        WorkflowPatternStore.upsert(key, pattern)
    END FOR
END
```

### 7.5 Complexity Analysis

```
ANALYSIS: Adaptive Workflow

Time Complexity:
    AdaptWorkflow:
        - Task analysis: O(t) where t = task length
        - Agent selection: O(a * c) where a = agents, c = capabilities
        - Execution: O(task_specific)
        - Learning: O(1) amortized
        - Total: O(t + a * c + execution)

    AnalyzeTask:
        - Classification: O(t + log p) where p = patterns
        - Complexity estimation: O(h) where h = history
        - Capability determination: O(1)
        - Total: O(t + log p + h)

    SelectSingleAgent:
        - Capability filtering: O(a * c)
        - Scoring: O(a)
        - Sorting: O(a * log a)
        - Total: O(a * c + a * log a)

    SelectMultipleAgents:
        - Task decomposition: O(t)
        - Per-subtask selection: O(s * a * c)
        - Total: O(t + s * a * c)

    LearnFromWorkflow:
        - Metric update: O(1)
        - Trajectory storage: O(1)
        - Pattern consolidation: O(n * log n) (periodic)
        - Index update: O(log p)
        - Total: O(log p) amortized

Space Complexity:
    - Agent registry: O(a)
    - Task pattern index: O(p * d)
    - Workflow trajectories: O(n)
    - Consolidated patterns: O(types * agents)
    - Total: O(p * d + n)

Performance Optimizations:
    1. Cached task type classifications
    2. Pre-computed agent capability matrices
    3. Incremental pattern consolidation
    4. Agent pooling with warm standby
    5. Predictive agent pre-selection
    6. Batch trajectory processing

Learning Convergence:
    - Initial task routing accuracy: ~70%
    - After 100 workflows: ~85%
    - After 1000 workflows: ~92%
    - Duration estimation accuracy: +/- 15% after adaptation

Adaptation Characteristics:
    - Cold start: Uses heuristics
    - Warm up (50 workflows): Basic patterns emerge
    - Steady state (500+ workflows): Optimal routing achieved
    - Continuous: Adapts to changing task distributions
```

---

## Data Structure Specifications

### Primary Data Structures

```
DATA STRUCTURES:

VectorIndex (HNSW):
    Type: Hierarchical Navigable Small World Graph
    Parameters:
        - M: 16 (max connections per layer)
        - efConstruction: 200
        - efSearch: 100 (dynamic based on k)
    Operations:
        - insert(id, vector, metadata): O(log n)
        - search(vector, k): O(k * log n)
        - delete(id): O(log n)
        - update(id, vector): O(log n)

EmbeddingCache (LRU):
    Type: Least Recently Used Cache with TTL
    Parameters:
        - maxSize: 10000 entries
        - ttl: 3600 seconds
    Operations:
        - get(key): O(1)
        - set(key, value): O(1)
        - evict(): O(1)
    Key: Content hash (64-bit)
    Value: Float32Array[384]

SearchCache (Semantic):
    Type: Multi-tier cache with semantic similarity
    Tiers:
        - L1: In-memory exact match (< 1ms)
        - L2: Local disk semantic (5-10ms)
        - L3: Distributed (10-50ms)
    Operations:
        - get(key): O(1) to O(log n)
        - set(key, value): O(1)
        - semanticGet(key, embedding): O(k * log n)

PatternStore:
    Type: B-tree with secondary embedding index
    Operations:
        - find(pattern): O(log p)
        - insert(pattern): O(log p)
        - update(pattern): O(log p)
        - search(embedding, k): O(k * log p)

KnowledgeGraph:
    Type: Adjacency list with property graph extensions
    Structures:
        - nodes: Map<string, GraphNode>
        - edges: Map<string, Edge[]>
        - clusters: Cluster[]
    Operations:
        - addNode(node): O(1)
        - addEdge(edge): O(1)
        - getNeighbors(id, depth): O(V + E) for BFS
        - shortestPath(from, to): O(V + E * log V)
        - getDegree(id): O(1) with cached degrees

CausalMemory:
    Type: Directed acyclic graph with confidence weights
    Operations:
        - addCausation(causes, effects, confidence): O(c + e)
        - findSimilarPatterns(pattern): O(log n)
        - getUtility(cause, effect): O(1)

SyncState:
    Type: Persistent hash map with timestamps
    Operations:
        - get(key): O(1)
        - set(key, value): O(1)
        - getModified(since): O(n * log n)
```

---

## Performance Summary

| Algorithm | p50 Latency | p99 Latency | Throughput | Space |
|-----------|-------------|-------------|------------|-------|
| Knowledge Capture | < 10ms | < 50ms | 1000/s | O(n) |
| Semantic Search | < 50ms | < 200ms | 500/s | O(d + m) |
| Self-Learning | < 5ms | < 20ms | 5000/s | O(p) |
| Graph Construction | N/A (batch) | N/A | 100 notes/s | O(n * d) |
| MCP Tool Handler | < 10ms | < 100ms | 1000/s | O(r) |
| Obsidian Sync | < 1s/file | < 5s/batch | 100 files/s | O(f) |
| Adaptive Workflow | < 100ms | < 500ms | 200/s | O(p * d) |

---

## Implementation Dependencies

### Core Libraries

```yaml
dependencies:
  embedding:
    - sentence-transformers (all-MiniLM-L6-v2)
    - dimension: 384

  vector_search:
    - HNSW library (hnswlib or faiss)
    - distance: cosine

  nlp:
    - spaCy (entity extraction)
    - tiktoken (tokenization)

  storage:
    - SQLite/PostgreSQL (metadata)
    - LevelDB/RocksDB (key-value)

  caching:
    - In-memory LRU
    - Redis (distributed)

  file_watching:
    - chokidar or similar
    - debouncing support
```

---

## Next Steps

1. **Architecture Phase**: Design system components and interfaces
2. **TDD Implementation**: Write tests for each algorithm
3. **Performance Profiling**: Benchmark against targets
4. **Integration Testing**: End-to-end workflow validation
5. **Optimization**: Profile and optimize hot paths

---

*Document prepared as part of SPARC Pseudocode Phase*
*Ready for Architecture and Refinement phases*
