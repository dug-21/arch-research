# pMemory SPARC Pseudocode

## Phase 2: Pseudocode

**Document Status**: Active
**Version**: 1.0.0
**Last Updated**: November 2024

---

## 1. Core Data Structures

### 1.1 Memory Item

```
STRUCTURE MemoryItem:
    id: UUID                      // Unique identifier
    content: String               // Raw content text
    embedding: Vector<f32>        // Dense vector representation
    metadata: Map<String, Value>  // Flexible metadata
    source: SourceInfo            // Provenance tracking
    created_at: Timestamp
    updated_at: Timestamp
    access_count: u64
    last_accessed: Timestamp

STRUCTURE SourceInfo:
    uri: String                   // Original location
    type: SourceType              // FILE | URL | API | MANUAL
    hash: String                  // Content hash for change detection
    captured_at: Timestamp
```

### 1.2 Causal Edge

```
STRUCTURE CausalEdge:
    source_id: UUID               // Memory item that led to...
    target_id: UUID               // ...this memory item
    relationship: RelationType    // PRECEDED | CAUSED | RELATED
    uplift_score: f32             // How much source helped find target
    interaction_count: u64        // Times this path was taken
    created_at: Timestamp
    decayed_score: f32            // Time-decayed score

FUNCTION calculate_decayed_score(edge, current_time):
    age = current_time - edge.created_at
    decay_factor = exp(-DECAY_RATE * age.as_days())
    RETURN edge.uplift_score * decay_factor * log(edge.interaction_count + 1)
```

### 1.3 Search Query

```
STRUCTURE SearchQuery:
    text: String                  // Query text
    embedding: Option<Vector>     // Pre-computed embedding
    filters: Vec<Filter>          // Metadata filters
    top_k: usize                  // Number of results
    strategy: SearchStrategy      // SEMANTIC | KEYWORD | HYBRID | GRAPH
    context: SearchContext        // User/agent context

STRUCTURE SearchContext:
    user_id: UUID
    session_id: UUID
    recent_queries: Vec<SearchQuery>
    recent_results: Vec<ItemId>
    cognitive_state: CognitiveState
```

### 1.4 Learning Structures

```
STRUCTURE ReflexionEpisode:
    query: SearchQuery
    results: Vec<SearchResult>
    feedback: FeedbackType        // POSITIVE | NEGATIVE | NEUTRAL
    outcome: Option<String>       // What happened after retrieval
    timestamp: Timestamp

STRUCTURE StrategyStats:
    strategy: SearchStrategy
    attempts: u64
    successes: u64
    avg_latency_ms: f32
    recent_rewards: RingBuffer<f32, 100>

STRUCTURE UserPreferences:
    strategy_priors: Map<SearchStrategy, Beta>  // Thompson Sampling priors
    topic_weights: Map<TopicId, f32>
    recency_bias: f32
    diversity_preference: f32
```

---

## 2. Core Algorithms

### 2.1 Vector Search (HNSW-based)

```
ALGORITHM search_vectors(query_embedding, index, top_k, ef_search):
    """
    HNSW approximate nearest neighbor search
    Target: <50ms for 1M vectors with >95% recall
    """

    // Enter at top layer
    entry_point = index.entry_point
    current_layer = index.max_layer

    // Greedy search through upper layers
    WHILE current_layer > 0:
        entry_point = search_layer(
            query_embedding,
            entry_point,
            ef=1,
            layer=current_layer
        )
        current_layer -= 1

    // Exhaustive search at bottom layer with ef candidates
    candidates = search_layer(
        query_embedding,
        entry_point,
        ef=ef_search,  // Typically 100-200 for high recall
        layer=0
    )

    // Return top-k from candidates
    RETURN select_top_k(candidates, query_embedding, top_k)

ALGORITHM search_layer(query, entry_points, ef, layer):
    """
    Layer-specific beam search
    """
    visited = Set()
    candidates = MinHeap()  // By distance (closest first)
    results = MaxHeap()     // By distance (furthest first)

    FOR ep IN entry_points:
        distance = compute_distance(query, ep.embedding)
        candidates.push((distance, ep))
        results.push((distance, ep))
        visited.add(ep.id)

    WHILE NOT candidates.is_empty():
        (dist, current) = candidates.pop()
        furthest_result = results.peek()

        IF dist > furthest_result.distance:
            BREAK  // No closer candidates possible

        FOR neighbor IN get_neighbors(current, layer):
            IF neighbor.id NOT IN visited:
                visited.add(neighbor.id)
                neighbor_dist = compute_distance(query, neighbor.embedding)

                IF neighbor_dist < furthest_result.distance OR results.len() < ef:
                    candidates.push((neighbor_dist, neighbor))
                    results.push((neighbor_dist, neighbor))

                    IF results.len() > ef:
                        results.pop()  // Remove furthest

    RETURN results.to_vec()
```

### 2.2 Hybrid Search

```
ALGORITHM hybrid_search(query, index, top_k, alpha=0.7):
    """
    Combine semantic and keyword search
    alpha: weight for semantic (1-alpha for keyword)
    """

    // Parallel execution
    PARALLEL:
        semantic_results = search_vectors(query.embedding, index.vector, top_k * 2)
        keyword_results = search_bm25(query.text, index.fulltext, top_k * 2)

    // Reciprocal Rank Fusion
    fused_scores = Map()

    FOR (rank, result) IN enumerate(semantic_results):
        rrf_score = alpha / (60 + rank)  // RRF constant = 60
        fused_scores[result.id] = fused_scores.get(result.id, 0) + rrf_score

    FOR (rank, result) IN enumerate(keyword_results):
        rrf_score = (1 - alpha) / (60 + rank)
        fused_scores[result.id] = fused_scores.get(result.id, 0) + rrf_score

    // Sort by fused score
    sorted_results = fused_scores.items()
        .sort_by(|(_, score)| -score)
        .take(top_k)

    RETURN enrich_results(sorted_results, index)
```

### 2.3 Causal Graph Traversal

```
ALGORITHM find_related_via_graph(item_id, graph, max_depth, min_score):
    """
    Breadth-first traversal with score threshold
    """

    visited = Set([item_id])
    results = []
    queue = Queue()

    // Initialize with direct edges
    FOR edge IN graph.edges_from(item_id):
        decayed = calculate_decayed_score(edge, now())
        IF decayed >= min_score:
            queue.push((edge.target_id, decayed, 1))  // (id, score, depth)

    WHILE NOT queue.is_empty():
        (current_id, path_score, depth) = queue.pop()

        IF current_id IN visited:
            CONTINUE

        visited.add(current_id)
        results.push((current_id, path_score, depth))

        IF depth < max_depth:
            FOR edge IN graph.edges_from(current_id):
                decayed = calculate_decayed_score(edge, now())
                combined_score = path_score * decayed  // Multiplicative decay

                IF combined_score >= min_score AND edge.target_id NOT IN visited:
                    queue.push((edge.target_id, combined_score, depth + 1))

    RETURN results.sort_by(|(_, score, _)| -score)

ALGORITHM update_causal_edge(source_id, target_id, graph, positive):
    """
    Update edge weight based on feedback
    """

    edge = graph.get_or_create_edge(source_id, target_id)

    IF positive:
        // Increase uplift with diminishing returns
        increment = LEARNING_RATE / (1 + log(edge.interaction_count))
        edge.uplift_score = min(1.0, edge.uplift_score + increment)
    ELSE:
        // Decrease uplift
        decrement = LEARNING_RATE / 2
        edge.uplift_score = max(0.0, edge.uplift_score - decrement)

    edge.interaction_count += 1
    graph.save_edge(edge)
```

### 2.4 Thompson Sampling for Strategy Selection

```
STRUCTURE Beta:
    alpha: f32  // Successes + 1
    beta: f32   // Failures + 1

ALGORITHM select_strategy(context, preferences):
    """
    Thompson Sampling: sample from each strategy's posterior
    Select strategy with highest sample
    """

    available_strategies = get_available_strategies(context)
    best_strategy = None
    best_sample = -Infinity

    FOR strategy IN available_strategies:
        prior = preferences.strategy_priors.get(strategy, Beta(1.0, 1.0))

        // Sample from Beta distribution
        sample = sample_beta(prior.alpha, prior.beta)

        // Adjust for context
        IF strategy == GRAPH AND context.recent_results.is_empty():
            sample *= 0.5  // Penalize graph search with no history

        IF sample > best_sample:
            best_sample = sample
            best_strategy = strategy

    RETURN best_strategy

ALGORITHM update_strategy_posterior(strategy, success, preferences):
    """
    Update Beta posterior based on outcome
    """

    prior = preferences.strategy_priors.get(strategy, Beta(1.0, 1.0))

    IF success:
        prior.alpha += 1
    ELSE:
        prior.beta += 1

    // Decay to prevent stale priors
    decay_factor = 0.99
    prior.alpha = max(1.0, prior.alpha * decay_factor)
    prior.beta = max(1.0, prior.beta * decay_factor)

    preferences.strategy_priors.set(strategy, prior)
```

### 2.5 Reflexion Learning

```
ALGORITHM record_episode(query, results, feedback, context, store):
    """
    Store retrieval episode for learning
    """

    episode = ReflexionEpisode(
        query: query,
        results: results,
        feedback: feedback,
        outcome: None,  // Updated later if known
        timestamp: now()
    )

    store.save_episode(episode)

    // Update strategy statistics
    strategy = query.strategy
    success = feedback == POSITIVE
    update_strategy_posterior(strategy, success, context.preferences)

    // Update causal edges if using graph strategy
    IF strategy == GRAPH AND results.len() > 0:
        FOR i IN 0..min(results.len()-1, 3):
            FOR j IN i+1..min(results.len(), 4):
                update_causal_edge(
                    results[i].id,
                    results[j].id,
                    store.graph,
                    success
                )

ALGORITHM learn_from_history(user_id, store, lookback_days):
    """
    Batch learning from episode history
    """

    episodes = store.get_episodes(user_id, lookback_days)

    // Aggregate patterns
    strategy_outcomes = Map()
    topic_outcomes = Map()

    FOR episode IN episodes:
        strategy = episode.query.strategy
        outcomes = strategy_outcomes.get_or_default(strategy, [])
        outcomes.push(episode.feedback == POSITIVE)

        FOR topic IN extract_topics(episode.query.text):
            topic_outcomes.get_or_default(topic, []).push(episode.feedback)

    // Update preferences
    preferences = store.get_preferences(user_id)

    FOR (strategy, outcomes) IN strategy_outcomes:
        success_rate = outcomes.filter(|x| x).len() / outcomes.len()
        // Weighted update towards observed success rate
        preferences.strategy_priors[strategy] = Beta(
            alpha: success_rate * outcomes.len() + 1,
            beta: (1 - success_rate) * outcomes.len() + 1
        )

    store.save_preferences(user_id, preferences)
```

---

## 3. Security Algorithms

### 3.1 Zero-Trust Request Validation

```
ALGORITHM validate_request(request, security_context):
    """
    Zero-trust validation: verify everything, trust nothing
    """

    // Step 1: Token validation
    token = request.auth_token
    IF NOT validate_jwt(token, security_context.public_keys):
        RETURN Err(AuthError::InvalidToken)

    claims = decode_jwt(token)

    // Step 2: Check token expiration (short-lived)
    IF claims.exp < now():
        RETURN Err(AuthError::TokenExpired)

    // Step 3: Verify token hasn't been revoked
    IF security_context.revocation_list.contains(claims.jti):
        RETURN Err(AuthError::TokenRevoked)

    // Step 4: Rate limiting
    rate_key = (claims.sub, request.endpoint)
    IF NOT rate_limiter.check(rate_key, RATE_LIMIT):
        RETURN Err(AuthError::RateLimited)

    // Step 5: Request integrity (if signed)
    IF request.signature:
        IF NOT verify_signature(request.body, request.signature, claims.public_key):
            RETURN Err(AuthError::InvalidSignature)

    // Step 6: Authorization check
    IF NOT authorize(claims.sub, request.resource, request.action):
        RETURN Err(AuthError::Forbidden)

    RETURN Ok(ValidatedRequest(claims, request))

ALGORITHM authorize(subject, resource, action):
    """
    RBAC + ABAC authorization
    """

    // Get subject's roles
    roles = get_roles(subject)

    // Check role permissions
    FOR role IN roles:
        permissions = get_permissions(role)
        IF permissions.allows(resource, action):
            RETURN True

    // Check attribute-based policies
    attributes = get_attributes(subject)
    resource_attrs = get_attributes(resource)

    FOR policy IN get_abac_policies(action):
        IF policy.evaluate(attributes, resource_attrs):
            RETURN True

    RETURN False
```

### 3.2 Encryption Operations

```
ALGORITHM encrypt_item(item, encryption_key, algorithm):
    """
    Encrypt memory item for storage
    Default: AES-256-GCM
    """

    // Generate random nonce
    nonce = random_bytes(12)  // 96 bits for GCM

    // Serialize item
    plaintext = serialize(item)

    // Encrypt
    ciphertext = aes_gcm_encrypt(plaintext, encryption_key, nonce)

    // Return encrypted blob with metadata
    RETURN EncryptedItem(
        nonce: nonce,
        ciphertext: ciphertext,
        algorithm: algorithm,
        key_id: encryption_key.id  // For key rotation
    )

ALGORITHM decrypt_item(encrypted, encryption_key):
    """
    Decrypt memory item from storage
    """

    // Verify key matches
    IF encrypted.key_id != encryption_key.id:
        // Need to fetch correct key (for rotation support)
        encryption_key = get_key(encrypted.key_id)

    // Decrypt
    plaintext = aes_gcm_decrypt(
        encrypted.ciphertext,
        encryption_key,
        encrypted.nonce
    )

    RETURN deserialize(plaintext)
```

### 3.3 Post-Quantum Key Exchange (ML-KEM/Kyber)

```
ALGORITHM pq_key_exchange_initiator():
    """
    Post-quantum key exchange using ML-KEM-768
    Initiator (client) side
    """

    // Generate ephemeral keypair
    (public_key, secret_key) = ml_kem_keygen()

    // Send public key to responder
    send(public_key)

    // Receive encapsulated shared secret
    ciphertext = receive()

    // Decapsulate to get shared secret
    shared_secret = ml_kem_decapsulate(ciphertext, secret_key)

    // Derive session key
    session_key = hkdf(shared_secret, "pMemory-session-key", 32)

    // Zeroize sensitive data
    zeroize(secret_key)
    zeroize(shared_secret)

    RETURN session_key

ALGORITHM pq_key_exchange_responder(peer_public_key):
    """
    Post-quantum key exchange using ML-KEM-768
    Responder (server) side
    """

    // Encapsulate shared secret using peer's public key
    (ciphertext, shared_secret) = ml_kem_encapsulate(peer_public_key)

    // Send ciphertext to initiator
    send(ciphertext)

    // Derive session key
    session_key = hkdf(shared_secret, "pMemory-session-key", 32)

    // Zeroize sensitive data
    zeroize(shared_secret)

    RETURN session_key
```

### 3.4 Agentic Threat Detection

```
ALGORITHM detect_prompt_injection(input, context):
    """
    Multi-layer prompt injection detection
    """

    score = 0.0
    flags = []

    // Layer 1: Pattern matching (fast path)
    FOR pattern IN INJECTION_PATTERNS:
        IF regex_match(input, pattern.regex):
            score += pattern.weight
            flags.push(pattern.name)

    IF score > FAST_PATH_THRESHOLD:
        RETURN ThreatDetected(score, flags, "pattern_match")

    // Layer 2: Semantic analysis (if enabled)
    IF context.enable_semantic_detection:
        input_embedding = embed(input)

        FOR known_injection IN context.injection_embeddings:
            similarity = cosine_similarity(input_embedding, known_injection)
            IF similarity > SEMANTIC_THRESHOLD:
                score += similarity * SEMANTIC_WEIGHT
                flags.push("semantic_match")

    // Layer 3: Structural analysis
    IF contains_role_override(input):
        score += 0.3
        flags.push("role_override_attempt")

    IF contains_instruction_delimiter(input):
        score += 0.2
        flags.push("delimiter_injection")

    // Decision
    IF score > THREAT_THRESHOLD:
        RETURN ThreatDetected(score, flags, "multi_layer")
    ELSE:
        RETURN Safe(score)

ALGORITHM validate_agent_identity(agent_request, trust_store):
    """
    Verify agent is who they claim to be
    """

    // Check agent certificate
    cert = agent_request.certificate
    IF NOT validate_certificate_chain(cert, trust_store.root_ca):
        RETURN Err(AgentError::InvalidCertificate)

    // Verify request signature
    IF NOT verify_signature(
        agent_request.payload,
        agent_request.signature,
        cert.public_key
    ):
        RETURN Err(AgentError::InvalidSignature)

    // Check agent is registered
    agent_id = cert.subject.common_name
    IF NOT trust_store.registered_agents.contains(agent_id):
        RETURN Err(AgentError::UnknownAgent)

    // Check capabilities match request
    requested_caps = extract_capabilities(agent_request)
    granted_caps = trust_store.agent_capabilities.get(agent_id)

    IF NOT requested_caps.is_subset_of(granted_caps):
        RETURN Err(AgentError::ExcessiveCapabilities)

    RETURN Ok(ValidatedAgent(agent_id, granted_caps))
```

---

## 4. LLM Integration Algorithms

### 4.1 Provider Abstraction

```
ALGORITHM route_llm_request(request, router_config):
    """
    Route to optimal LLM provider based on context
    """

    // Determine requirements
    requirements = analyze_requirements(request)

    // Score each provider
    provider_scores = []
    FOR provider IN router_config.providers:
        IF NOT provider.supports(requirements):
            CONTINUE

        score = 0.0

        // Cost factor
        estimated_tokens = estimate_tokens(request)
        cost = provider.cost_per_token * estimated_tokens
        score += (1.0 / cost) * router_config.cost_weight

        // Latency factor
        avg_latency = provider.avg_latency_ms
        score += (1.0 / avg_latency) * router_config.latency_weight

        // Quality factor (from historical data)
        quality = provider.quality_score
        score += quality * router_config.quality_weight

        // Privacy factor
        IF request.requires_privacy AND provider.is_local:
            score += router_config.privacy_bonus

        provider_scores.push((provider, score))

    // Select highest scoring available provider
    provider_scores.sort_by(|(_, score)| -score)

    FOR (provider, _) IN provider_scores:
        IF provider.is_available():
            RETURN provider

    RETURN Err(NoAvailableProvider)

ALGORITHM context_assembly(query, memory_results, provider):
    """
    Assemble context for LLM within token limits
    """

    token_limit = provider.context_window - RESERVED_FOR_OUTPUT
    current_tokens = count_tokens(query, provider.tokenizer)

    context_items = []

    // Sort by relevance score
    sorted_results = memory_results.sort_by(|r| -r.score)

    FOR result IN sorted_results:
        item_tokens = count_tokens(result.content, provider.tokenizer)

        IF current_tokens + item_tokens <= token_limit:
            context_items.push(result)
            current_tokens += item_tokens
        ELSE:
            // Try truncated version
            truncated = truncate_to_tokens(
                result.content,
                token_limit - current_tokens - 100,  // Safety margin
                provider.tokenizer
            )
            IF truncated.len() > MIN_USEFUL_LENGTH:
                context_items.push(result.with_content(truncated))
            BREAK

    RETURN AssembledContext(
        query: query,
        items: context_items,
        total_tokens: current_tokens,
        provider: provider.name
    )
```

### 4.2 Embedding with Caching

```
ALGORITHM embed_with_cache(text, provider, cache):
    """
    Generate embedding with intelligent caching
    """

    // Normalize text for cache key
    normalized = normalize_text(text)
    cache_key = hash(normalized + provider.embedding_model)

    // Check cache
    cached = cache.get(cache_key)
    IF cached:
        cache.touch(cache_key)  // Update LRU
        RETURN cached

    // Generate embedding
    embedding = provider.embed(text)

    // Cache with TTL based on text type
    ttl = determine_ttl(text)
    cache.set(cache_key, embedding, ttl)

    RETURN embedding

ALGORITHM batch_embed_with_cache(texts, provider, cache):
    """
    Batch embedding with partial cache hits
    """

    results = Map()
    uncached = []

    // Check cache for all texts
    FOR text IN texts:
        normalized = normalize_text(text)
        cache_key = hash(normalized + provider.embedding_model)

        cached = cache.get(cache_key)
        IF cached:
            results[text] = cached
        ELSE:
            uncached.push((text, cache_key))

    // Batch embed uncached texts
    IF uncached.len() > 0:
        uncached_texts = uncached.map(|(t, _)| t)
        embeddings = provider.batch_embed(uncached_texts)

        FOR ((text, cache_key), embedding) IN zip(uncached, embeddings):
            results[text] = embedding
            cache.set(cache_key, embedding, default_ttl())

    RETURN results
```

---

## 5. Utility Algorithms

### 5.1 Content Hashing for Deduplication

```
ALGORITHM content_hash(content):
    """
    Semantic-aware content hashing
    """

    // Normalize whitespace and case
    normalized = content
        .lowercase()
        .replace_regex(/\s+/, " ")
        .trim()

    // Generate hash
    RETURN blake3_hash(normalized)

ALGORITHM detect_duplicate(new_item, index):
    """
    Detect if content already exists (exact or near-duplicate)
    """

    // Exact duplicate check via hash
    hash = content_hash(new_item.content)
    IF index.hash_exists(hash):
        existing_id = index.get_by_hash(hash)
        RETURN DuplicateResult::Exact(existing_id)

    // Near-duplicate check via embedding similarity
    similar = search_vectors(new_item.embedding, index, top_k=5)
    FOR result IN similar:
        IF result.similarity > NEAR_DUPLICATE_THRESHOLD:
            // Verify with text similarity
            text_sim = jaccard_similarity(new_item.content, result.content)
            IF text_sim > TEXT_SIMILARITY_THRESHOLD:
                RETURN DuplicateResult::Near(result.id, result.similarity)

    RETURN DuplicateResult::None
```

### 5.2 Diversity Maintenance

```
ALGORITHM ensure_diversity(results, min_diversity):
    """
    Rerank results to ensure topical diversity
    """

    IF results.len() <= 1:
        RETURN results

    // Compute pairwise similarities
    similarities = Matrix(results.len(), results.len())
    FOR i IN 0..results.len():
        FOR j IN i+1..results.len():
            sim = cosine_similarity(
                results[i].embedding,
                results[j].embedding
            )
            similarities[i][j] = sim
            similarities[j][i] = sim

    // Greedy diversity selection
    selected = [0]  // Start with top result

    WHILE selected.len() < results.len():
        best_idx = -1
        best_score = -Infinity

        FOR i IN 0..results.len():
            IF i IN selected:
                CONTINUE

            // Score = relevance - penalty for similarity to selected
            relevance = results[i].score
            max_sim_to_selected = max(similarities[i][j] FOR j IN selected)

            diversity_penalty = max_sim_to_selected * DIVERSITY_WEIGHT
            score = relevance - diversity_penalty

            IF score > best_score:
                best_score = score
                best_idx = i

        selected.push(best_idx)

        // Check if diversity threshold met
        avg_diversity = 1.0 - mean(
            similarities[selected[-1]][j] FOR j IN selected[:-1]
        )
        IF avg_diversity >= min_diversity:
            BREAK

    RETURN [results[i] FOR i IN selected]
```

---

## 6. Validation Criteria

### Performance Validation

| Algorithm | Target Latency | Test Dataset |
|-----------|---------------|--------------|
| search_vectors (1M) | <50ms | Synthetic 1M vectors |
| hybrid_search | <100ms | Real queries + 100K docs |
| find_related_via_graph | <20ms | 10K nodes, 50K edges |
| Thompson Sampling select | <1ms | 10 strategies |
| encrypt_item | <5ms | 4KB item |
| detect_prompt_injection | <10ms | 1000 test cases |

### Correctness Validation

| Algorithm | Test Method |
|-----------|-------------|
| search_vectors | Recall@10 >= 95% vs brute force |
| hybrid_search | NDCG@10 improvement vs single strategy |
| causal_graph | Edge weight convergence test |
| Thompson Sampling | Regret bounds verification |
| encryption | Round-trip integrity + NIST test vectors |
| threat_detection | F1 score >= 0.95 on test set |

---

## 7. Cross-Reference

- **Specification**: See `spec/01-specification.md` for requirements
- **Architecture**: See `arch/03-architecture.md` for system design
- **Security**: See `security/04-security.md` for detailed security design
- **Implementation**: See `implementation/05-implementation.md` for roadmap
